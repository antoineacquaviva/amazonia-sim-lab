"""Audit Ockham des choix internes v6.4 et extraction de parties remarquables (`human_trace_1.0`).

100 % stdlib PyPy 3.11 / CPython 3.12 (zéro dépendance tierce, zéro mutation du noyau).
Fournit :
1. `V64DecisionAuditRecorder` : callback lecture seule (`delta == 0`) comptabilisant tous les
   dilemmes internes v6.4 (accessoires + `DEC_EFFET_TUILE`) pour détecter les faux dilemmes (> 90 %).
2. `RemarkableBookmarkTracker` & `select_top_remarkable_bookmarks` : sélection légère en flux
   des parties remarquables (effondrement, meilleur score, Sommeil éclair, Éveil, cascade,
   Tour 8 serré, écart B3 vs B2).
3. `extract_remarkable_traces_jsonl` : rejoue déterministiquement les K parties retenues et
   exporte un fichier JSONL `human_trace_1.0` directement ouvrable dans `docs/human_logger.html`
   et validé par `bots/human_eval.py`.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from bots.human_eval import (
    HumanDecisionRecord,
    load_human_traces_jsonl,
    record_human_decision_from_state,
    write_human_traces_jsonl,
)
from engine.core_engine import (
    DEC_BOUCLIER_LISIERE_5_3,
    DEC_CHOIX_CASE_GARDIEN,
    DEC_DEPLOIEMENT_NID_4_2,
    DEC_ENRACINEMENT_6_1,
    DEC_HUMAIN_CHAMAN_2_1,
    DEC_MAMMIFERE_DUEL_2,
    DEC_OISEAU_CHOIX_DE_1_3,
    DEC_OISEAU_PLUME_2,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_SABOTAGE_CIBLE_3_2,
)
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    DEC_EFFET_TUILE,
    DecisionRequest,
    GameOver,
)
from engine.state import (
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    PLUME_CALME,
    PLUME_CHAUD,
    GameConfig,
    GameState,
)

__all__ = (
    "REMARKABLE_CATEGORIES",
    "RemarkableBookmarkTracker",
    "RemarkableGameBookmark",
    "V64DecisionAuditRecorder",
    "extract_remarkable_traces_jsonl",
    "merge_v64_ockham_audits",
    "select_top_remarkable_bookmarks",
    "summarize_v64_ockham_audit",
)

REMARKABLE_CATEGORIES: tuple[str, ...] = (
    "collapse_worst",
    "best_score",
    "early_sommeil",
    "eveil_success",
    "high_drama_cascade",
    "tour8_clutch",
    "b3_vs_b2_outlier",
)


def _normalize_effect_branch(opt: Any) -> str:
    """Regroupe une option de `DEC_EFFET_TUILE` par branche sémantique (évite l'explosion de coordonnées)."""
    if opt == "PASSER":
        return "PASSER"
    if isinstance(opt, tuple) and opt:
        head = opt[0]
        if isinstance(head, str):
            return head
        if len(opt) == 2 and all(isinstance(x, int) for x in opt):
            return "CIBLE_PARCELLE_OU_MACHINE"
        return f"TUPLE_{len(opt)}"
    if isinstance(opt, str):
        return opt
    if isinstance(opt, int):
        return f"VAL_{opt}"
    return type(opt).__name__


class V64DecisionAuditRecorder:
    """Enregistreur lecture seule (`delta == 0`) des dilemmes internes v6.4 et effets de tuiles."""

    __slots__ = ("internal_choices", "tile_effect_choices")

    def __init__(self) -> None:
        self.internal_choices: dict[str, dict[str, int]] = {}
        self.tile_effect_choices: dict[str, dict[str, int]] = {}

    def _inc(self, bucket: dict[str, dict[str, int]], key: str, branch: str) -> None:
        sub = bucket.get(key)
        if sub is None:
            bucket[key] = {branch: 1}
        else:
            sub[branch] = sub.get(branch, 0) + 1

    def __call__(self, state: GameState, decision: DecisionRequest, choice: Any) -> None:
        dtype = decision.decision_type
        opts = decision.options

        if dtype == DEC_OISEAU_CHOIX_DE_1_3 and len(opts) >= 2:
            branch = "D1_PREMIER" if choice == opts[0] else "D2_SECOND"
            self._inc(self.internal_choices, "oiseau_de_1_3", branch)
            return

        if dtype == DEC_HUMAIN_CHAMAN_2_1 and len(opts) >= 2:
            branch = "TAMBOUR" if choice == CHAMAN_TAMBOUR else ("CHANT" if choice == CHAMAN_CHANT else str(choice))
            self._inc(self.internal_choices, "chaman_2_1", branch)
            return

        if dtype == DEC_MAMMIFERE_DUEL_2 and len(opts) >= 2:
            branch = "POSER_DUEL_DEFI" if choice == "POSER_DUEL_DEFI" else "PASSER"
            self._inc(self.internal_choices, "mammifere_duel_2", branch)
            return

        if dtype == DEC_OISEAU_PLUME_2 and len(opts) >= 2:
            if choice == "PASSER":
                branch = "PASSER"
            elif isinstance(choice, tuple) and choice:
                branch = "CHAUD" if choice[0] == PLUME_CHAUD else ("CALME" if choice[0] == PLUME_CALME else str(choice[0]))
            else:
                branch = str(choice)
            self._inc(self.internal_choices, "oiseau_plume_2", branch)
            return

        if dtype == DEC_SABOTAGE_CIBLE_3_2 and len(opts) >= 2:
            has_red = False
            has_cold = False
            for cand in opts:
                if isinstance(cand, tuple) and len(cand) >= 2:
                    r_m, mt_m = int(cand[0]), int(cand[1])
                    rouges, _ = state.get_machine_tokens(r_m, mt_m)
                    if rouges >= 1:
                        has_red = True
                    else:
                        has_cold = True
            if has_red and has_cold and isinstance(choice, tuple) and len(choice) >= 2:
                r_c, mt_c = int(choice[0]), int(choice[1])
                rouges_c, _ = state.get_machine_tokens(r_c, mt_c)
                branch = "REFROIDIR_ROUGE" if rouges_c >= 1 else "RECULER_MOBILE"
                self._inc(self.internal_choices, "sabotage_cible_3_2", branch)
            return

        if dtype == DEC_DEPLOIEMENT_NID_4_2 and len(opts) >= 2:
            kinds = {str(o[0]) for o in opts if isinstance(o, tuple) and o}
            if len(kinds) >= 2 and isinstance(choice, tuple) and choice:
                self._inc(self.internal_choices, "deploiement_nid_4_2", str(choice[0]))
            return

        if dtype == DEC_BOUCLIER_LISIERE_5_3 and len(opts) >= 2:
            self._inc(self.internal_choices, "bouclier_lisiere_5_3", str(choice))
            return

        if dtype == DEC_ENRACINEMENT_6_1 and len(opts) >= 2 and "PASSER" in opts:
            branch = "PASSER" if choice == "PASSER" else "ENRACINER"
            self._inc(self.internal_choices, "enracinement_6_1", branch)
            return

        if dtype == DEC_CHOIX_CASE_GARDIEN and len(opts) >= 2:
            self._inc(self.internal_choices, "choix_case_gardien_3_1", f"CASE_{int(choice)}")
            return

        if dtype == DEC_EFFET_TUILE and len(opts) >= 2:
            eff_kind = str(decision.context.get("effect_kind", "GENERIC"))
            distinct_branches = {_normalize_effect_branch(o) for o in opts}
            if len(distinct_branches) >= 2:
                self._inc(self.tile_effect_choices, eff_kind, _normalize_effect_branch(choice))

    def to_compact_dict(self) -> dict[str, Any]:
        return {
            "internal": {k: dict(v) for k, v in self.internal_choices.items()},
            "tile_effects": {k: dict(v) for k, v in self.tile_effect_choices.items()},
        }


def merge_v64_ockham_audits(audits: list[dict[str, Any]]) -> dict[str, dict[str, dict[str, int]]]:
    """Fusionne une liste de dictionnaires compacts `V64DecisionAuditRecorder`."""
    merged_internal: dict[str, dict[str, int]] = {}
    merged_effects: dict[str, dict[str, int]] = {}
    for item in audits:
        if not item:
            continue
        for key, counts in (item.get("internal") or {}).items():
            dst = merged_internal.setdefault(str(key), {})
            for b_name, cnt in counts.items():
                dst[str(b_name)] = dst.get(str(b_name), 0) + int(cnt)
        for key, counts in (item.get("tile_effects") or {}).items():
            dst = merged_effects.setdefault(str(key), {})
            for b_name, cnt in counts.items():
                dst[str(b_name)] = dst.get(str(b_name), 0) + int(cnt)
    return {"internal": merged_internal, "tile_effects": merged_effects}


def _summarize_choice_bucket(
    bucket: dict[str, dict[str, int]],
    *,
    false_dilemma_threshold_pct: float = 90.0,
    min_samples: int = 20,
) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key in sorted(bucket):
        counts = bucket[key]
        total = sum(counts.values())
        if total <= 0:
            continue
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        dom_name, dom_cnt = ranked[0]
        dom_pct = round(100.0 * dom_cnt / total, 2)
        k_opts = len(counts)
        if k_opts <= 1:
            h_norm = 0.0
        else:
            ent = -sum((c / total) * math.log2(c / total) for c in counts.values() if c > 0)
            h_norm = round(ent / math.log2(k_opts), 4)
        is_false = total >= min_samples and dom_pct >= false_dilemma_threshold_pct
        out[key] = {
            "n_decisions": total,
            "dominant_choice": dom_name,
            "dominant_pct": dom_pct,
            "entropy_norm": h_norm,
            "is_false_dilemma": is_false,
            "distribution": {k: int(v) for k, v in ranked},
        }
    return out


def summarize_v64_ockham_audit(
    merged: dict[str, dict[str, dict[str, int]]],
    *,
    false_dilemma_threshold_pct: float = 90.0,
    min_samples: int = 20,
) -> dict[str, Any]:
    """Synthétise les dilemmes internes v6.4 et les effets de tuiles avec détection de faux dilemmes."""
    internal_s = _summarize_choice_bucket(
        merged.get("internal") or {},
        false_dilemma_threshold_pct=false_dilemma_threshold_pct,
        min_samples=min_samples,
    )
    effects_s = _summarize_choice_bucket(
        merged.get("tile_effects") or {},
        false_dilemma_threshold_pct=false_dilemma_threshold_pct,
        min_samples=min_samples,
    )
    false_internal = [k for k, v in internal_s.items() if v["is_false_dilemma"]]
    false_effects = [k for k, v in effects_s.items() if v["is_false_dilemma"]]
    return {
        "threshold_pct": false_dilemma_threshold_pct,
        "min_samples": min_samples,
        "v64_internal_dilemmas": internal_s,
        "tile_effect_dilemmas": effects_s,
        "flagged_false_dilemmas": {
            "internal": false_internal,
            "tile_effects": false_effects,
            "total_flagged": len(false_internal) + len(false_effects),
        },
    }


@dataclass(frozen=True, slots=True)
class RemarkableGameBookmark:
    """Signet ultra-léger permettant de rejouer et d'exporter une partie remarquable en `human_trace_1.0`."""

    category: str
    metric_value: float
    bot: str
    variant_id: str
    n_players: int
    mode: int
    peuples: tuple[str, ...]
    exp_seed: int
    rep_id: int
    chassis_id: int
    tile_profiles: tuple[tuple[str, str], ...]
    score_arbres: int
    ratio_arbres: float
    cause_fin: str
    tour_fin: int
    cascade_max: int = 0
    assise_key: str = ""
    max_revision_passes: int = 3
    coordonnateur_initial: int = 0
    note: str = ""

    def to_json_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["peuples"] = list(self.peuples)
        d["tile_profiles"] = [list(p) for p in self.tile_profiles]
        return d

    @classmethod
    def from_json_dict(cls, raw: dict[str, Any]) -> RemarkableGameBookmark:
        return cls(
            category=str(raw["category"]),
            metric_value=float(raw["metric_value"]),
            bot=str(raw["bot"]),
            variant_id=str(raw.get("variant_id", "BASELINE")),
            n_players=int(raw["n_players"]),
            mode=int(raw["mode"]),
            peuples=tuple(str(p) for p in raw["peuples"]),
            exp_seed=int(raw["exp_seed"]),
            rep_id=int(raw["rep_id"]),
            chassis_id=int(raw.get("chassis_id", -1)),
            tile_profiles=tuple((str(p[0]), str(p[1])) for p in raw.get("tile_profiles", [])),
            score_arbres=int(raw["score_arbres"]),
            ratio_arbres=float(raw["ratio_arbres"]),
            cause_fin=str(raw["cause_fin"]),
            tour_fin=int(raw["tour_fin"]),
            cascade_max=int(raw.get("cascade_max", 0)),
            assise_key=str(raw.get("assise_key", "")),
            max_revision_passes=int(raw.get("max_revision_passes", 3)),
            coordonnateur_initial=int(raw.get("coordonnateur_initial", 0)),
            note=str(raw.get("note", "")),
        )

    def replay_identity(self) -> tuple[Any, ...]:
        return (self.bot, self.variant_id, self.peuples, self.exp_seed, self.rep_id, self.mode)


class RemarkableBookmarkTracker:
    """Conserve au plus 1 signet remarquable par catégorie au fil d'une unité de simulation."""

    __slots__ = ("_best",)

    def __init__(self) -> None:
        self._best: dict[str, RemarkableGameBookmark] = {}

    def _consider(self, bm: RemarkableGameBookmark, *, prefer_lower: bool) -> None:
        cur = self._best.get(bm.category)
        if cur is None:
            self._best[bm.category] = bm
            return
        if prefer_lower:
            if (bm.metric_value, bm.rep_id) < (cur.metric_value, cur.rep_id):
                self._best[bm.category] = bm
        else:
            if (bm.metric_value, -bm.rep_id) > (cur.metric_value, -cur.rep_id):
                self._best[bm.category] = bm

    def observe(
        self,
        *,
        cfg: GameConfig,
        res: GameOver,
        bot: str,
        variant_id: str,
        chassis_id: int = -1,
        cascade_max: int = 0,
        assise_key: str = "",
    ) -> None:
        def _mk(category: str, metric_value: float) -> RemarkableGameBookmark:
            return RemarkableGameBookmark(
                category=category,
                metric_value=metric_value,
                bot=bot,
                variant_id=variant_id,
                n_players=cfg.n_players,
                mode=cfg.mode,
                peuples=cfg.peuples,
                exp_seed=cfg.exp_seed,
                rep_id=cfg.rep_id,
                chassis_id=chassis_id,
                tile_profiles=cfg.tile_profiles,
                score_arbres=res.score_arbres,
                ratio_arbres=round(res.ratio_arbres, 6),
                cause_fin=res.cause_fin,
                tour_fin=res.tour_fin,
                cascade_max=cascade_max,
                assise_key=assise_key,
                max_revision_passes=cfg.max_revision_passes,
                coordonnateur_initial=cfg.coordonnateur_initial,
            )

        # 1. Effondrement le plus brutal (score_arbres == 0) ou score le plus bas
        collapse_key = (0.0 if res.score_arbres <= 0 else 10.0) + res.ratio_arbres + 0.01 * res.tour_fin
        self._consider(_mk("collapse_worst", collapse_key), prefer_lower=True)
        # 2. Meilleure survie
        self._consider(_mk("best_score", res.ratio_arbres), prefer_lower=False)
        # 3. Sommeil le plus précoce
        if res.cause_fin == CAUSE_REVE_RANG_1:
            som_metric = float(res.tour_fin) - 0.5 * res.ratio_arbres
            self._consider(_mk("early_sommeil", som_metric), prefer_lower=True)
        # 4. Éveil des Gardiens réussi
        if res.cause_fin == CAUSE_REVEIL_GARDIENS:
            ev_metric = res.ratio_arbres - 0.02 * res.tour_fin
            self._consider(_mk("eveil_success", ev_metric), prefer_lower=False)
        # 5. Plus grande cascade dramatique
        if cascade_max >= 2:
            self._consider(
                _mk("high_drama_cascade", float(cascade_max) + 0.1 * res.ratio_arbres),
                prefer_lower=False,
            )
        # 6. Fin Tour 8 sur le fil (proche de 45-55 % de survie)
        if res.cause_fin == CAUSE_TOUR_8:
            clutch_dist = abs(res.ratio_arbres - 0.50)
            self._consider(_mk("tour8_clutch", clutch_dist), prefer_lower=True)

    def to_json_list(self) -> list[dict[str, Any]]:
        return [self._best[k].to_json_dict() for k in sorted(self._best)]


def select_top_remarkable_bookmarks(
    raw_bookmarks: Sequence[dict[str, Any] | RemarkableGameBookmark],
    *,
    max_games: int = 8,
) -> list[RemarkableGameBookmark]:
    """Agrège tous les signets des shards et sélectionne les K parties les plus remarquables (sans doublon)."""
    if max_games <= 0 or not raw_bookmarks:
        return []
    parsed: list[RemarkableGameBookmark] = [
        bm if isinstance(bm, RemarkableGameBookmark) else RemarkableGameBookmark.from_json_dict(bm)
        for bm in raw_bookmarks
    ]
    prefer_lower_cats = {"collapse_worst", "early_sommeil", "tour8_clutch"}
    by_cat: dict[str, list[RemarkableGameBookmark]] = {}
    for bm in parsed:
        by_cat.setdefault(bm.category, []).append(bm)
    for cat, lst in by_cat.items():
        if cat in prefer_lower_cats:
            lst.sort(key=lambda b: (b.metric_value, b.rep_id, b.variant_id))
        else:
            lst.sort(key=lambda b: (-b.metric_value, b.rep_id, b.variant_id))

    selected: list[RemarkableGameBookmark] = []
    seen_ids: set[tuple[Any, ...]] = set()
    # Sélection équilibrée en tourniquet (1 champion par catégorie à chaque passe jusqu'à max_games)
    made_progress = True
    while len(selected) < max_games and made_progress:
        made_progress = False
        for cat in REMARKABLE_CATEGORIES:
            if len(selected) >= max_games:
                break
            for bm in by_cat.get(cat, ()):
                rid = bm.replay_identity()
                if rid not in seen_ids:
                    seen_ids.add(rid)
                    selected.append(bm)
                    made_progress = True
                    break
    return selected


def _play_for_trace_extraction(
    state: GameState,
    bot_name: str,
    on_decision: Any,
    b3_kwargs: dict[str, Any] | None = None,
) -> GameOver:
    from bots.bot_b0 import play_game_b0
    from bots.bot_b3_rh import play_game_b3
    from bots.heuristic_engine import play_game_b1, play_game_b2, play_game_b2_open

    b = bot_name.upper()
    if b == "B0":
        return play_game_b0(state, on_decision=on_decision)
    if b == "B1":
        return play_game_b1(state, on_decision=on_decision)
    if b == "B2_OPEN":
        return play_game_b2_open(state, on_decision=on_decision)
    if b == "B3":
        kw = dict(b3_kwargs or {})
        return play_game_b3(state, on_decision=on_decision, **kw)
    return play_game_b2(state, on_decision=on_decision)


def _make_trace_capturer(
    bm: RemarkableGameBookmark,
    game_id: str,
    game_records: list[HumanDecisionRecord],
    max_decisions_per_game: int,
) -> Any:
    def _capture(st: GameState, dec: DecisionRequest, choice: Any) -> None:
        if len(game_records) >= max_decisions_per_game:
            return
        dtype = dec.decision_type
        if dtype not in (DEC_POSE_DEFENSEUR_1, DEC_POSE_DEFENSEUR_2):
            return
        is_first = dtype == DEC_POSE_DEFENSEUR_1
        if is_first:
            tgt = choice
        else:
            if not isinstance(choice, tuple) or len(choice) < 2:
                return
            tgt = choice[1]
        if not isinstance(tgt, tuple) or not tgt or tgt[0] == "PASSER_IMPASSE":
            return
        phase_str = str(dec.context.get("phase", "2.1" if is_first else "2.2"))
        note_txt = (
            f"[{bm.category}] variant={bm.variant_id} bot={bm.bot} "
            f"phase={phase_str} cause={bm.cause_fin} ratio={bm.ratio_arbres:.3f}"
        )
        if bm.note:
            note_txt = f"{note_txt} | {bm.note}"
        try:
            rec = record_human_decision_from_state(
                st,
                dec.decideur,
                tgt,
                game_id=game_id,
                decision_id=len(game_records) + 1,
                is_first_defender=is_first,
                player_level=bm.bot,
                notes=note_txt,
            )
        except ValueError:
            return
        game_records.append(rec)

    return _capture


def extract_remarkable_traces_jsonl(
    bookmarks: list[RemarkableGameBookmark],
    output_path: Path,
    *,
    campaign_name: str = "campagne",
    max_decisions_per_game: int = 200,
    b3_kwargs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Rejoue les parties remarquables et écrit un fichier JSONL `human_trace_1.0` validé."""
    import engine.effects  # noqa: F401 — enregistre les 30 tuiles v6.4

    all_records: list[HumanDecisionRecord] = []
    games_meta: list[dict[str, Any]] = []

    for g_idx, bm in enumerate(bookmarks, start=1):
        cfg = GameConfig(
            n_players=bm.n_players,
            mode=bm.mode,
            peuples=bm.peuples,
            exp_seed=bm.exp_seed,
            rep_id=bm.rep_id,
            coordonnateur_initial=bm.coordonnateur_initial,
            max_revision_passes=bm.max_revision_passes,
            tile_profiles=bm.tile_profiles,
        )
        state = GameState(cfg)
        game_id = f"{campaign_name}__{g_idx:02d}_{bm.category}_{bm.bot}_{bm.assise_key or ''.join(bm.peuples)}_r{bm.rep_id}"
        game_records: list[HumanDecisionRecord] = []
        capturer = _make_trace_capturer(bm, game_id, game_records, max_decisions_per_game)
        res = _play_for_trace_extraction(state, bm.bot, capturer, b3_kwargs=b3_kwargs)
        all_records.extend(game_records)
        games_meta.append(
            {
                "game_id": game_id,
                "category": bm.category,
                "bot": bm.bot,
                "variant_id": bm.variant_id,
                "assise_key": bm.assise_key or f"N{bm.n_players}-{''.join(bm.peuples)}",
                "peuples": list(bm.peuples),
                "exp_seed": bm.exp_seed,
                "rep_id": bm.rep_id,
                "score_arbres": res.score_arbres,
                "ratio_arbres": round(res.ratio_arbres, 4),
                "cause_fin": res.cause_fin,
                "tour_fin": res.tour_fin,
                "cascade_max": bm.cascade_max,
                "n_decisions_exported": len(game_records),
                "note": bm.note,
            }
        )

    write_human_traces_jsonl(output_path, all_records)
    # Validation stricte aller-retour via le parseur officiel `human_trace_1.0`
    validated = load_human_traces_jsonl(output_path)
    assert len(validated) == len(all_records), "Divergence de relecture sur les traces human_trace_1.0"
    return {
        "schema_version": "human_trace_1.0",
        "path": str(output_path),
        "n_games": len(games_meta),
        "n_decisions": len(validated),
        "games": games_meta,
    }
