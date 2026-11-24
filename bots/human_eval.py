"""Journalisation de parties humaines (`human_trace_1.0` JSONL) et mesure d'accord bot/humain.

100 % stdlib (PyPy 3.11 / CPython 3.12), zéro accès `_buf`, zéro dépendance externe.
Permet de :
1. Enregistrer / recharger des décisions humaines (poses `2.1` et révisions `2.2`) au format JSONL léger.
2. Reconstruire l'état `GameState` correspondant via les seuls mutateurs publics.
3. Mesurer l'accord top-1, top-k, le rang moyen, la log-vraisemblance softmax et l'écart d'espérance
   en arbres (via déroulements CRN) contre `B0`, `B1`, `B2` et `B2_OPEN`.
4. Calibrer directement la température `tau_b1` de `B1` par maximum de vraisemblance sur des traces humaines.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from bots.b2_rollouts import evaluate_gardien_reve_candidates_crn
from bots.belief_and_ticks import build_belief_summary
from bots.bot_b0 import BotB0
from bots.heuristic_engine import (
    DEFAULT_TAU_B1,
    choose_b2,
    score_target_b1,
    score_target_b2,
)
from engine.core_engine import (
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    apply_step2_def1,
    list_legal_targets,
)
from engine.primitives import DecisionRequest
from engine.state import (
    CARD_NONE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    TRACK_LEN,
    GameConfig,
    GameState,
    PlayerObservation,
)

__all__ = (
    "HUMAN_TRACE_SCHEMA_VERSION",
    "HumanDecisionRecord",
    "calibrate_tau_b1_on_human_traces",
    "evaluate_bot_human_agreement",
    "extract_board_state_dict",
    "load_human_traces_jsonl",
    "rank_targets_for_bot",
    "reconstruct_state_from_trace_record",
    "record_human_decision_from_state",
    "write_human_traces_jsonl",
)

HUMAN_TRACE_SCHEMA_VERSION: str = "human_trace_1.0"


def _normalize_target(raw: Any) -> tuple[Any, ...]:
    assert isinstance(raw, (list, tuple)) and len(raw) >= 1, f"Cible invalide : {raw!r}"
    kind = str(raw[0])
    return (kind, *(int(x) for x in raw[1:]))


@dataclass(frozen=True, slots=True)
class HumanDecisionRecord:
    """Enregistrement d'une décision humaine en Étape 2.1 ou 2.2."""

    schema_version: str
    game_id: str
    decision_id: int
    config: dict[str, Any]
    tour: int
    step: int
    seat: int
    is_first_defender: bool
    board_state: dict[str, Any]
    legal_targets: tuple[tuple[Any, ...], ...]
    chosen_target: tuple[Any, ...]
    player_level: str = "humain"
    notes: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "game_id": self.game_id,
            "decision_id": self.decision_id,
            "config": self.config,
            "tour": self.tour,
            "step": self.step,
            "seat": self.seat,
            "is_first_defender": self.is_first_defender,
            "board_state": self.board_state,
            "legal_targets": [list(t) for t in self.legal_targets],
            "chosen_target": list(self.chosen_target),
            "player_level": self.player_level,
            "notes": self.notes,
        }

    @classmethod
    def from_json_dict(cls, raw: dict[str, Any]) -> HumanDecisionRecord:
        schema = str(raw.get("schema_version", ""))
        if schema != HUMAN_TRACE_SCHEMA_VERSION:
            raise ValueError(
                f"schema_version invalide : {schema!r} (attendu {HUMAN_TRACE_SCHEMA_VERSION!r})"
            )
        cfg_dict = dict(raw["config"])
        legal = tuple(_normalize_target(t) for t in raw["legal_targets"])
        chosen = _normalize_target(raw["chosen_target"])
        if legal and chosen not in legal:
            raise ValueError(f"chosen_target {chosen!r} absent de legal_targets")
        return cls(
            schema_version=schema,
            game_id=str(raw["game_id"]),
            decision_id=int(raw["decision_id"]),
            config=cfg_dict,
            tour=int(raw["tour"]),
            step=int(raw["step"]),
            seat=int(raw["seat"]),
            is_first_defender=bool(raw["is_first_defender"]),
            board_state=dict(raw["board_state"]),
            legal_targets=legal,
            chosen_target=chosen,
            player_level=str(raw.get("player_level", "humain")),
            notes=str(raw.get("notes", "")),
        )


def extract_board_state_dict(state: GameState) -> dict[str, Any]:
    """Sérialise l'état de plateau via les seuls accesseurs publics (lisible et éditable)."""
    cfg = state.cfg
    n = cfg.n_players
    p_max = cfg.p_max

    parcels: list[list[dict[str, int]]] = []
    for r in range(n):
        row: list[dict[str, int]] = []
        for p in range(1, p_max + 1):
            nid_id, nid_act = state.get_parcel_nid(r, p)
            row.append(
                {
                    "arbres": state.get_parcel_arbres(r, p),
                    "souches": state.get_parcel_souches(r, p),
                    "insectes": state.get_parcel_insectes(r, p),
                    "piege": state.get_parcel_piege(r, p),
                    "nid_id": nid_id,
                    "nid_active": 1 if nid_act else 0,
                }
            )
        parcels.append(row)

    machines: list[dict[str, int]] = []
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st_m, pending = state.get_machine_pos_status(r, mt)
            rouges, bleus = state.get_machine_tokens(r, mt)
            machines.append(
                {
                    "ray": r,
                    "m_type": mt,
                    "pos": pos,
                    "status": st_m,
                    "pending_siege": 1 if pending else 0,
                    "rouges": rouges,
                    "bleus": bleus,
                }
            )

    hands: list[list[int]] = []
    for s in range(n):
        hands.append(list(state.get_player_hand(s)))

    tactiques = [state.get_tactique_at_rank(rk) for rk in range(TRACK_LEN)]
    gardiens: list[list[int]] = [list(state.get_gardien_at_case(c)) for c in range(1, TRACK_LEN + 1)]
    bugs_by_case = [state.get_bugs_at_case(c) for c in range(1, TRACK_LEN + 1)]
    colonie_by_case = [state.get_colonie_at_case(c) for c in range(1, TRACK_LEN + 1)]
    lisieres: list[list[int]] = (
        [list(state.get_lisiere_tile_state(i)) for i in range(2 * n)] if cfg.mode >= 2 else []
    )

    defenders: list[dict[str, Any]] = []
    for s in range(n):
        for d_idx in (0, 1):
            raw_loc = state.get_player_def_loc_raw(s, d_idx)
            if raw_loc in (0, 255):
                continue
            kind, a, b, c = state.decode_def_loc(raw_loc)
            face = (
                FACE_DEFINITIF
                if (d_idx == 0 or state.is_player_def2_definitif(s))
                else FACE_REFLEXION
            )
            defenders.append(
                {"seat": s, "def_idx": d_idx, "kind": kind, "a": a, "b": b, "c": c, "face": face}
            )

    return {
        "tour": state.tour,
        "step": state.step,
        "coordonnateur": state.coordonnateur,
        "paravents_ouverts": state.paravents_ouverts,
        "sabotage_deck_count": state.sabotage_deck_count,
        "sabotage_pending_count": state.sabotage_pending_count,
        "reshuffle_count": state.reshuffle_count,
        "parcels": parcels,
        "machines": machines,
        "hands": hands,
        "piste_tactiques": tactiques,
        "piste_gardiens": gardiens,
        "bugs_by_case": bugs_by_case,
        "colonie_by_case": colonie_by_case,
        "lisieres": lisieres,
        "defenders": defenders,
    }


def reconstruct_state_from_trace_record(record: HumanDecisionRecord) -> GameState:
    """Reconstruit un `GameState` fidèle depuis un `HumanDecisionRecord` via les seuls mutateurs publics."""
    c_raw = record.config
    tp_raw = c_raw.get("tile_profiles", [])
    tile_profiles = tuple((str(pair[0]), str(pair[1])) for pair in tp_raw)
    cfg = GameConfig(
        n_players=int(c_raw["n_players"]),
        mode=int(c_raw["mode"]),
        peuples=tuple(str(p) for p in c_raw["peuples"]),
        exp_seed=int(c_raw.get("exp_seed", 42)),
        rep_id=int(c_raw.get("rep_id", 0)),
        tile_profiles=tile_profiles,
    )
    st = GameState(cfg)
    bs = record.board_state
    st.tour = int(bs.get("tour", record.tour))
    st.step = int(bs.get("step", record.step))
    st.coordonnateur = int(bs.get("coordonnateur", 0))
    st.paravents_ouverts = bool(bs.get("paravents_ouverts", False))
    st.sabotage_deck_count = int(bs.get("sabotage_deck_count", 0))
    st.sabotage_pending_count = int(bs.get("sabotage_pending_count", 0))
    st.reshuffle_count = int(bs.get("reshuffle_count", 0))

    for r_idx, row in enumerate(bs.get("parcels", [])):
        for p_off, cell in enumerate(row):
            p_num = p_off + 1
            st.set_parcel_arbres_souches(r_idx, p_num, int(cell["arbres"]), int(cell["souches"]))
            st.set_parcel_insectes(r_idx, p_num, int(cell.get("insectes", 0)))
            st.set_parcel_piege(r_idx, p_num, int(cell.get("piege", 0)))
            nid_id = int(cell.get("nid_id", 0))
            if nid_id > 0:
                st.set_parcel_nid(r_idx, p_num, nid_id, active_ce_tour=bool(cell.get("nid_active", 0)))

    for m_item in bs.get("machines", []):
        r_m = int(m_item["ray"])
        mt_m = int(m_item["m_type"])
        st.set_machine_pos_status(
            r_m,
            mt_m,
            int(m_item["pos"]),
            int(m_item["status"]),
            bool(m_item.get("pending_siege", 0)),
        )
        st.set_machine_tokens(r_m, mt_m, int(m_item.get("rouges", 0)), int(m_item.get("bleus", 0)))

    for rk, code in enumerate(bs.get("piste_tactiques", [])):
        st.set_tactique_at_rank(rk, int(code))

    if cfg.mode >= 2:
        for c_off, g_pair in enumerate(bs.get("piste_gardiens", [])):
            st.set_gardien_at_case(c_off + 1, int(g_pair[0]), int(g_pair[1]))
        for c_off, b_cnt in enumerate(bs.get("bugs_by_case", [])):
            st.set_bugs_at_case(c_off + 1, int(b_cnt))
        for c_off, col_cnt in enumerate(bs.get("colonie_by_case", [])):
            st.set_colonie_at_case(c_off + 1, int(col_cnt))
        for l_idx, l_pair in enumerate(bs.get("lisieres", [])):
            # Les bâtisseurs en lisière sont replacés ci-dessous via place_defender_lisiere_tile (évite le double-comptage)
            st.set_lisiere_tile_state(l_idx, int(l_pair[0]), 0)

    # Reconstruire la pioche cohérente puis appliquer les mains et retirer les cartes tenues
    saved_pend = st.sabotage_pending_count
    st.sabotage_pending_count = 0
    st.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    st.sabotage_pending_count = saved_pend

    for s_idx, h_vals in enumerate(bs.get("hands", [])):
        c_code = int(h_vals[0])
        st.set_player_hand(
            s_idx, c_code, int(h_vals[1]), int(h_vals[2]), int(h_vals[3]), int(h_vals[4])
        )
        if c_code != CARD_NONE:
            st.remove_machine_card_from_deck_if_present(c_code)

    for d_item in bs.get("defenders", []):
        s_d = int(d_item["seat"])
        d_i = int(d_item["def_idx"])
        kind = str(d_item["kind"])
        a, b, c = int(d_item["a"]), int(d_item["b"]), int(d_item["c"])
        face = int(d_item.get("face", FACE_DEFINITIF))
        if kind == "FORET":
            st.place_defender_foret(s_d, d_i, a, b, face)
        elif kind == "FURTIVITE":
            st.place_defender_furtivite(s_d, d_i, a, c // 2, face, preferred_twin=c % 2)
        elif kind == "LISIERE" and cfg.mode >= 2:
            st.place_defender_lisiere_tile(s_d, d_i, a, face)
        elif kind == "GARDIEN_PARI" and cfg.mode >= 2:
            st.place_defender_gardien_pari(s_d, a, face)
        elif kind == "REVE_ACTIVATION" and cfg.mode >= 2:
            st.place_defender_reve_activation(s_d, a, face, def_idx=d_i)

    return st


def record_human_decision_from_state(
    state: GameState,
    seat: int,
    chosen_target: tuple[Any, ...],
    *,
    game_id: str,
    decision_id: int,
    is_first_defender: bool | None = None,
    player_level: str = "humain",
    notes: str = "",
) -> HumanDecisionRecord:
    """Capture une décision humaine depuis un `GameState` courant au format `human_trace_1.0`."""
    cfg = state.cfg
    is_first = (state.step == STEP_2_1_DEF1) if is_first_defender is None else bool(is_first_defender)
    legal = list_legal_targets(state, seat, is_first_defender=is_first, exclude_own_def2=(not is_first))
    chosen_norm = _normalize_target(chosen_target)
    if legal and chosen_norm not in legal:
        raise ValueError(f"Action humaine illégale {chosen_norm!r} hors de {legal!r}")
    return HumanDecisionRecord(
        schema_version=HUMAN_TRACE_SCHEMA_VERSION,
        game_id=game_id,
        decision_id=decision_id,
        config={
            "n_players": cfg.n_players,
            "mode": cfg.mode,
            "peuples": list(cfg.peuples),
            "exp_seed": cfg.exp_seed,
            "rep_id": cfg.rep_id,
            "tile_profiles": [list(pair) for pair in cfg.tile_profiles],
        },
        tour=state.tour,
        step=state.step,
        seat=seat,
        is_first_defender=is_first,
        board_state=extract_board_state_dict(state),
        legal_targets=tuple(_normalize_target(t) for t in legal),
        chosen_target=chosen_norm,
        player_level=player_level,
        notes=notes,
    )


def write_human_traces_jsonl(path: Path, records: list[HumanDecisionRecord]) -> None:
    """Écrit une liste de décisions humaines en JSONL UTF-8 sans BOM (`\n`)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        json.dumps(rec.to_json_dict(), ensure_ascii=False, separators=(",", ":"))
        for rec in records
    ]
    path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8", newline="\n")


def load_human_traces_jsonl(path: Path) -> list[HumanDecisionRecord]:
    """Charge et valide un fichier JSONL `human_trace_1.0`."""
    out: list[HumanDecisionRecord] = []
    for line_no, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = raw_line.strip()
        if not stripped:
            continue
        try:
            obj = json.loads(stripped)
            out.append(HumanDecisionRecord.from_json_dict(obj))
        except Exception as exc:
            raise ValueError(f"Erreur trace humaine {path}:{line_no} : {exc}") from exc
    return out


def _softmax_log_prob(scores: list[float], target_idx: int, tau: float) -> float:
    if tau <= 0.0 or not scores:
        return 0.0
    max_s = max(scores)
    inv_tau = 1.0 / tau
    exps = [math.exp(max(-60.0, (s - max_s) * inv_tau)) for s in scores]
    z = sum(exps)
    if z <= 0.0:
        return -60.0
    p = max(1e-15, exps[target_idx] / z)
    return math.log(p)


def rank_targets_for_bot(
    obs: PlayerObservation,
    cfg: GameConfig,
    legal_targets: tuple[tuple[Any, ...], ...],
    *,
    bot_name: str,
    is_first_defender: bool,
) -> list[tuple[tuple[Any, ...], float]]:
    """Classe toutes les cibles légales par ordre décroissant de préférence pour `bot_name`."""
    b = bot_name.upper()
    if b == "B0":
        dtype = DEC_POSE_DEFENSEUR_1 if is_first_defender else DEC_POSE_DEFENSEUR_2
        if is_first_defender:
            req_opts: tuple[Any, ...] = legal_targets
        else:
            req_opts = tuple(("POSER_DEFINITIF", t) for t in legal_targets)
        req = DecisionRequest(obs.observer_seat, dtype, req_opts, {"tour": obs.tour})
        b0_raw = BotB0.choose(obs, req, cfg)
        b0_pick = _normalize_target(b0_raw if is_first_defender else b0_raw[1])
        ranked: list[tuple[tuple[Any, ...], float]] = []
        for idx, t in enumerate(legal_targets):
            sc = 100.0 if t == b0_pick else (10.0 - 0.01 * idx)
            ranked.append((t, sc))
        ranked.sort(key=lambda pair: -pair[1])
        return ranked

    belief = build_belief_summary(obs, cfg)
    if b == "B1":
        scored = [
            (t, float(score_target_b1(obs, cfg, belief, t, is_first_defender)))
            for t in legal_targets
        ]
    elif b in ("B2", "B2_OPEN"):
        scored = [
            (t, float(score_target_b2(obs, cfg, belief, t, is_first_defender)))
            for t in legal_targets
        ]
    else:
        raise ValueError(f"Bot non supporté dans human_eval : {bot_name!r}")

    scored.sort(key=lambda pair: (-pair[1], legal_targets.index(pair[0])))
    return scored


def evaluate_bot_human_agreement(
    records: list[HumanDecisionRecord],
    *,
    bots: tuple[str, ...] = ("B0", "B1", "B2"),
    top_k: int = 3,
    tau_b1: float = DEFAULT_TAU_B1,
    n_crn_rollouts: int = 8,
    evaluate_regret: bool = True,
) -> dict[str, Any]:
    """Mesure l'accord top-1 / top-k, le rang moyen, la vraisemblance et l'écart d'arbres CRN."""
    n_rec = len(records)
    per_bot: dict[str, dict[str, Any]] = {}

    for bot in bots:
        b_upper = bot.upper()
        top1_hits = 0
        topk_hits = 0
        ranks: list[int] = []
        log_liks: list[float] = []
        tree_gaps: list[float] = []

        for rec in records:
            st = reconstruct_state_from_trace_record(rec)
            cfg = st.cfg
            if b_upper == "B2_OPEN" and not st.paravents_ouverts:
                st.paravents_ouverts = True
            obs = st.get_observation(rec.seat)
            legal = rec.legal_targets
            if not legal:
                legal = tuple(
                    _normalize_target(t)
                    for t in list_legal_targets(
                        st,
                        rec.seat,
                        is_first_defender=rec.is_first_defender,
                        exclude_own_def2=(not rec.is_first_defender),
                    )
                )
            ranked = rank_targets_for_bot(
                obs, cfg, legal, bot_name=b_upper, is_first_defender=rec.is_first_defender
            )
            ordered_targets = [t for t, _ in ranked]
            ordered_scores = [sc for _, sc in ranked]

            human_rank = (
                ordered_targets.index(rec.chosen_target) + 1
                if rec.chosen_target in ordered_targets
                else len(ordered_targets) + 1
            )
            ranks.append(human_rank)
            if human_rank == 1:
                top1_hits += 1
            if human_rank <= top_k:
                topk_hits += 1

            if rec.chosen_target in ordered_targets:
                h_idx = ordered_targets.index(rec.chosen_target)
                tau_eval = tau_b1 if b_upper == "B1" else 100.0
                log_liks.append(_softmax_log_prob(ordered_scores, h_idx, tau_eval))

            if evaluate_regret and ordered_targets:
                bot_top1 = ordered_targets[0]
                if bot_top1 == rec.chosen_target:
                    tree_gaps.append(0.0)
                elif not rec.is_first_defender and st.step == STEP_2_2_DEF2:
                    deltas = evaluate_gardien_reve_candidates_crn(
                        st,
                        obs,
                        rec.seat,
                        rec.chosen_target,
                        (bot_top1,),
                        chooser=choose_b2,
                        n_rollouts=n_crn_rollouts,
                    )
                    tree_gaps.append(float(deltas.get(bot_top1, 0.0)))
                else:
                    # En 2.1 : comparer via clones CRN après pose du 1er défenseur sur human vs bot
                    st_h = st.clone()
                    apply_step2_def1(st_h, rec.seat, rec.chosen_target, check_legal=False)
                    st_b = st.clone()
                    apply_step2_def1(st_b, rec.seat, bot_top1, check_legal=False)
                    bel_h = build_belief_summary(st_h.get_observation(rec.seat), cfg)
                    bel_b = build_belief_summary(st_b.get_observation(rec.seat), cfg)
                    v_h = score_target_b2(obs, cfg, bel_h, rec.chosen_target, True) / 100.0
                    v_b = score_target_b2(obs, cfg, bel_b, bot_top1, True) / 100.0
                    tree_gaps.append(v_b - v_h)

        per_bot[b_upper] = {
            "n_decisions": n_rec,
            "top1_agreement": (top1_hits / float(n_rec)) if n_rec > 0 else 0.0,
            f"top{top_k}_agreement": (topk_hits / float(n_rec)) if n_rec > 0 else 0.0,
            "mean_human_rank": (sum(ranks) / float(len(ranks))) if ranks else 0.0,
            "mean_softmax_log_likelihood": (
                sum(log_liks) / float(len(log_liks)) if log_liks else None
            ),
            "mean_tree_gap_bot_minus_human": (
                sum(tree_gaps) / float(len(tree_gaps)) if tree_gaps else None
            ),
        }

    return {
        "schema_version": HUMAN_TRACE_SCHEMA_VERSION,
        "n_decisions": n_rec,
        "top_k": top_k,
        "tau_b1": tau_b1,
        "by_bot": per_bot,
    }


def calibrate_tau_b1_on_human_traces(
    records: list[HumanDecisionRecord],
    *,
    tau_grid: tuple[float, ...] = (25.0, 50.0, 80.0, 115.0, 160.0, 220.0),
) -> dict[str, Any]:
    """Calibre `tau_b1` par maximum de vraisemblance softmax sur des décisions humaines journalisées."""
    if not records:
        return {"n_decisions": 0, "best_tau_b1": DEFAULT_TAU_B1, "log_likelihood_by_tau": {}}

    score_rows: list[tuple[list[float], int]] = []
    for rec in records:
        st = reconstruct_state_from_trace_record(rec)
        obs = st.get_observation(rec.seat)
        bel = build_belief_summary(obs, st.cfg)
        legal = rec.legal_targets
        if not legal:
            legal = tuple(
                _normalize_target(t)
                for t in list_legal_targets(
                    st,
                    rec.seat,
                    is_first_defender=rec.is_first_defender,
                    exclude_own_def2=(not rec.is_first_defender),
                )
            )
        if not legal or rec.chosen_target not in legal:
            continue
        scores = [
            float(score_target_b1(obs, st.cfg, bel, t, rec.is_first_defender)) for t in legal
        ]
        score_rows.append((scores, legal.index(rec.chosen_target)))

    ll_by_tau: dict[str, float] = {}
    best_tau = DEFAULT_TAU_B1
    best_ll = -1e18
    for tau in tau_grid:
        if tau <= 0.0:
            continue
        ll = (
            sum(_softmax_log_prob(scores, h_idx, tau) for scores, h_idx in score_rows)
            / float(len(score_rows))
            if score_rows
            else 0.0
        )
        ll_by_tau[str(tau)] = round(ll, 6)
        if ll > best_ll:
            best_ll = ll
            best_tau = float(tau)

    return {
        "n_decisions": len(score_rows),
        "best_tau_b1": best_tau,
        "best_mean_log_likelihood": round(best_ll, 6) if score_rows else None,
        "log_likelihood_by_tau": ll_by_tau,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Évaluation d'accord bot/humain et calibration softmax B1 sur traces JSONL."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_eval = sub.add_parser("evaluate", help="Évaluer B0/B1/B2 sur un fichier JSONL human_trace_1.0")
    p_eval.add_argument("jsonl_path", type=Path)
    p_eval.add_argument("--top-k", type=int, default=3)
    p_eval.add_argument("--tau-b1", type=float, default=DEFAULT_TAU_B1)
    p_eval.add_argument("--rollouts", type=int, default=8)
    p_eval.add_argument("--no-regret", action="store_true")

    p_fit = sub.add_parser("fit-tau", help="Calibrer tau_b1 par maximum de vraisemblance")
    p_fit.add_argument("jsonl_path", type=Path)

    args = parser.parse_args(argv)
    records = load_human_traces_jsonl(args.jsonl_path)
    if args.cmd == "evaluate":
        report = evaluate_bot_human_agreement(
            records,
            top_k=args.top_k,
            tau_b1=args.tau_b1,
            n_crn_rollouts=args.rollouts,
            evaluate_regret=not args.no_regret,
        )
    else:
        report = calibrate_tau_b1_on_human_traces(records)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
