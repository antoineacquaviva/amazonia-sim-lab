"""Bot Baseline B0 (Réflexe, K_max = 0) — 100 % stdlib PyPy 3.11, isolation stricte."""

from __future__ import annotations

from typing import Any

from engine.core_engine import (
    DEC_CHOIX_CASE_GARDIEN,
    DEC_COLONIE_A_OPEN,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_ORDRE_CONSTRUCTION_3_1,
    DEC_PLACEMENT_NID_3_1,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_RETRAIT_APPRENTISSAGE_6_1,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import DecisionRequest, GameOver
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CARD_SABOTAGE,
    FAMILLE_CROISSANCE,
    FAMILLE_REVE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    SYNERGY_META,
    TACTIQUES_SPEC,
    GameConfig,
    GameState,
    HandObs,
    PlayerObservation,
    is_tactique_code,
    unpack_machine_card,
)

__all__ = (
    "BotB0",
    "choose_b0",
    "play_game_b0",
)


def _tiebreak_u64(cfg: GameConfig, obs: PlayerObservation, opt_idx: int) -> int:
    """Bris d'égalité déterministe sans biais de siège 0 via rng.py."""
    salt = (obs.step * 31 + opt_idx) & 0xFFFFFFFF
    return rand_u64(
        cfg.exp_seed,
        cfg.rep_id,
        SRC_BOT_TIEBREAK,
        obs.tour,
        obs.observer_seat,
        salt,
    )


def _compute_threat_and_machine_masks(
    obs: PlayerObservation,
    cfg: GameConfig,
    own_hand: HandObs,
) -> tuple[int, int]:
    """Calcule en entier 30 bits (zéro allocation) les masques de menaces connues et de machines."""
    threat_mask = 0
    machine_mask = 0
    n = obs.n_players
    p_max = cfg.p_max

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                bit = 1 << (r * MAX_P + (pos - 1))
                machine_mask |= bit
                if st == MACHINE_STATUS_RATISSAGE:
                    threat_mask |= bit

    if own_hand.card is not None and 1 <= own_hand.card <= 2 * n:
        ray, m_type = unpack_machine_card(own_hand.card)
        lec_m = own_hand.lecture_m
        if lec_m is not None and 1 <= lec_m <= 6:
            t_code, _, _ = obs.tactique_code_bugs_app(lec_m - 1)
            if is_tactique_code(t_code):
                pos, st = obs.machine_pos_status(ray, m_type)
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    spec = TACTIQUES_SPEC[t_code]
                    for c_kind in spec.cibles:
                        if c_kind == "SUR_PLACE":
                            if not obs.is_route(ray, pos):
                                threat_mask |= 1 << (ray * MAX_P + (pos - 1))
                        elif c_kind == "DEVANT":
                            for p_cand in range(pos + 1, p_max + 1):
                                if not obs.is_route(ray, p_cand):
                                    threat_mask |= 1 << (ray * MAX_P + (p_cand - 1))
                                    break

    return threat_mask, machine_mask


def _active_machine_mask(obs: PlayerObservation) -> int:
    mask = 0
    for r in range(obs.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                mask |= 1 << (r * MAX_P + (pos - 1))
    return mask


def _score_defender_target(
    obs: PlayerObservation,
    cfg: GameConfig,
    target: tuple[Any, ...],
    threat_mask: int,
    machine_mask: int,
    drew_sabotage_or_none: bool,
) -> int:
    """Score heuristique réflexe (entier, zéro allocation) d'une pose de Défenseur."""
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        defs = obs.parcel_defenseurs(r, p)
        cur_def = defs + obs.parcel_insectes(r, p)
        seuil_base = cfg.dotation_arbres[p - 1] + cfg.offset_seuil_parade
        bit = 1 << (r * MAX_P + (p - 1))
        score = 100

        if obs.parcel_piege(r, p) == PIEGE_ACTIF and cur_def == 0:
            score += 550
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r, p):
            score += 480
        if (threat_mask & bit) and cur_def < seuil_base:
            score += 600 if r == obs.observer_seat else 520
        if (machine_mask & bit) and cur_def < seuil_base:
            score += 180
        if obs.parcel_arbres(r, p) == 1:
            score += 60
        return score

    if kind == "LISIERE":
        _, slot_idx = target
        if obs.mode < 2 or slot_idx >= 2 * obs.n_players:
            return 0
        tile_id, _, constructors = obs.lisiere_tile_info(slot_idx)
        fam, _, _ = SYNERGY_META[tile_id]
        fam_bonus = 90 if fam == FAMILLE_REVE else (70 if fam == FAMILLE_CROISSANCE else 50)
        if constructors == 1:
            return 580 + fam_bonus
        if drew_sabotage_or_none and obs.tour <= 6:
            return 420 + fam_bonus
        return 240 + fam_bonus

    if kind == "FURTIVITE":
        _, l_idx, p, rive = target
        nb_d, f_ins = obs.furtivite_defs_and_ins(l_idx, p)
        t_ray = l_idx if rive == 0 else (l_idx + 1) % obs.n_players
        has_m = bool(machine_mask & (1 << (t_ray * MAX_P + (p - 1))))

        partner_ready = (nb_d == 1) or (f_ins >= 1)
        useful_trap = (not has_m) and obs.parcel_piege(t_ray, p) == PIEGE_AUCUN
        useful_sabotage = has_m and obs.tour <= 6

        if partner_ready and (useful_trap or useful_sabotage):
            return 510 if useful_sabotage else 490
        if drew_sabotage_or_none and (useful_trap or useful_sabotage):
            return 340
        return 140

    if kind == "GARDIEN_PARI":
        _, case_c = target
        c_i = int(case_c)
        if not obs.gardien_pari_enabled or not obs.gardien_present_at_case(c_i):
            return 0
        own_c = obs.player_def2_gardien_pari_case(obs.observer_seat)
        allies_c = obs.gardien_pari_defenders(c_i) - (1 if own_c == c_i else 0)
        if allies_c >= 1:
            return 0
        total_mob = obs.total_gardien_pari_defenders() + obs.total_reve_activation_defenders()
        if obs.tour <= 7 and total_mob >= obs.n_players - 1 and drew_sabotage_or_none:
            return 450
        if obs.tour <= 7 and total_mob >= 1 and drew_sabotage_or_none:
            return 280
        return 100

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        c_i = int(case_c)
        if obs.reve_at_case(c_i) <= 0:
            return 0
        own_hand = obs.hand_of(obs.observer_seat)
        own_hits = (
            own_hand.card is not None and 1 <= own_hand.card <= 12 and own_hand.lecture_m == c_i
        )
        allies = obs.reve_activation_defenders(c_i)
        act_mode = cfg.reve_activation_mode
        if act_mode == "1_DEF_1_MACHINE":
            return 435 if own_hits else 70
        if act_mode == "1_DEF_ALL_RANK":
            if allies >= 1:
                return 30
            return 450 if own_hits else 70
        # BINOME_ALL_RANK
        if allies >= 2:
            return 30
        if allies == 1:
            return 460 if own_hits else (260 if drew_sabotage_or_none else 120)
        return 330 if own_hits else 60

    return 0


class BotB0:
    """Agent réflexe B0 (K_max = 0) opérant exclusivement sur PlayerObservation."""

    @staticmethod
    def choose(obs: PlayerObservation, decision: DecisionRequest, cfg: GameConfig) -> Any:
        opts = decision.options
        assert len(opts) >= 1
        if len(opts) == 1:
            return opts[0]

        dtype = decision.decision_type

        if dtype in (DEC_POSE_DEFENSEUR_1, DEC_POSE_DEFENSEUR_2):
            own_hand = obs.hand_of(obs.observer_seat)
            drew_sab = (not own_hand.has_card) or (own_hand.card == CARD_SABOTAGE)
            threat_mask, machine_mask = _compute_threat_and_machine_masks(obs, cfg, own_hand)

            best_choice = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0

            if dtype == DEC_POSE_DEFENSEUR_1:
                for idx, opt in enumerate(opts):
                    sc = _score_defender_target(
                        obs, cfg, opt, threat_mask, machine_mask, drew_sab
                    )
                    if sc > best_sc:
                        best_sc = sc
                        best_tb = -1
                        best_idx = idx
                        best_choice = opt
                    elif sc == best_sc:
                        if best_tb < 0:
                            best_tb = _tiebreak_u64(cfg, obs, best_idx)
                        tb = _tiebreak_u64(cfg, obs, idx)
                        if tb > best_tb:
                            best_tb = tb
                            best_idx = idx
                            best_choice = opt
                return best_choice

            # DEC_POSE_DEFENSEUR_2 (K_max = 0 : pose directe en choix définitif)
            for idx, opt in enumerate(opts):
                act_kind, target = opt
                if act_kind != "POSER_DEFINITIF":
                    continue
                sc = _score_defender_target(
                    obs, cfg, target, threat_mask, machine_mask, drew_sab
                )
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_choice = opt
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_choice = opt
            return best_choice

        if dtype == DEC_REVISION_DEFENSEUR_2:
            for opt in opts:
                if opt[0] == "VERROUILLER_DEFINITIF":
                    return opt
            return opts[0]

        if dtype == DEC_COLONIE_A_OPEN:
            return "OUVRIR" if "OUVRIR" in opts else opts[0]

        if dtype == DEC_ORDRE_CONSTRUCTION_3_1:
            best_slot = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, slot_idx in enumerate(opts):
                tid, _, _ = obs.lisiere_tile_info(int(slot_idx))
                fam, _, _ = SYNERGY_META[tid]
                prio = 3 if fam == FAMILLE_REVE else (2 if fam == FAMILLE_CROISSANCE else 1)
                if prio > best_sc:
                    best_sc = prio
                    best_tb = -1
                    best_idx = idx
                    best_slot = slot_idx
                elif prio == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_slot = slot_idx
            return best_slot

        if dtype == DEC_CHOIX_CASE_GARDIEN:
            best_case = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, c_num in enumerate(opts):
                c_int = int(c_num)
                w = (
                    60
                    if c_int == 1
                    else (
                        55
                        if c_int == 6
                        else (50 if c_int == 4 else (45 if c_int == 2 else (35 if c_int == 3 else 30)))
                    )
                )
                if w > best_sc:
                    best_sc = w
                    best_tb = -1
                    best_idx = idx
                    best_case = c_num
                elif w == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_case = c_num
            return best_case

        if dtype == DEC_PLACEMENT_NID_3_1:
            best_nid_pos = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, (r, p) in enumerate(opts):
                sc = int(p) * 100 + obs.parcel_arbres(int(r), int(p))
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_nid_pos = (r, p)
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_nid_pos = (r, p)
            return best_nid_pos

        if dtype == DEC_LIBERATION_BATISSEUR_3_1:
            m_mask = _active_machine_mask(obs)
            best_lib = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, opt in enumerate(opts):
                _, _, r, p = opt
                has_m = bool(m_mask & (1 << (int(r) * MAX_P + (int(p) - 1))))
                sc = 100 if has_m else 50
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_lib = opt
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_lib = opt
            return best_lib

        if dtype == DEC_MIGRATION_INSECTE_4_3:
            src = decision.context.get("source", ("FORET", 0, 1))
            src_kind, src_a, src_p = src
            if src_kind == "FORET":
                sr, sp = int(src_a), int(src_p)
                if (
                    obs.parcel_piege(sr, sp) == PIEGE_ACTIF
                    and obs.parcel_defenseurs(sr, sp) == 0
                    and obs.parcel_insectes(sr, sp) == 1
                ):
                    return ("RESTER",)

            m_mask = _active_machine_mask(obs)
            best_mv = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, mv in enumerate(opts):
                mk = mv[0]
                sc = 50
                if mk == "COLONIE":
                    sc = 500 if obs.gardien_available_at_case(int(mv[1])) else 260
                elif mk == "BUG":
                    t_code, t_bugs, _ = obs.tactique_code_bugs_app(int(mv[1]) - 1)
                    sc = 420 if (is_tactique_code(t_code) and t_bugs == 0) else 220
                elif mk == "FORET":
                    dst_r, dst_p = int(mv[1]), int(mv[2])
                    if (
                        obs.parcel_piege(dst_r, dst_p) == PIEGE_ACTIF
                        and obs.parcel_defenseurs(dst_r, dst_p) + obs.parcel_insectes(dst_r, dst_p)
                        == 0
                    ):
                        sc = 480
                    elif obs.mode >= 2 and src_kind == "FORET" and dst_p > int(src_p):
                        sc = 300
                    elif m_mask & (1 << (dst_r * MAX_P + (dst_p - 1))):
                        sc = 250
                    else:
                        sc = 80
                elif mk == "RESTER":
                    sc = 150

                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_mv = mv
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_mv = mv
            return best_mv

        if dtype == DEC_RETRAIT_APPRENTISSAGE_6_1:
            best_r = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, opt in enumerate(opts):
                if opt == "PASSER":
                    sc = 0
                else:
                    _, _, app = obs.tactique_code_bugs_app(int(opt))
                    sc = 100 + app * 10
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_r = opt
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_r = opt
            return best_r

        best_gen = opts[0]
        best_u_gen = _tiebreak_u64(cfg, obs, 0)
        for idx in range(1, len(opts)):
            u = _tiebreak_u64(cfg, obs, idx)
            if u > best_u_gen:
                best_u_gen = u
                best_gen = opts[idx]
        return best_gen


def choose_b0(state: GameState, decision: DecisionRequest) -> Any:
    """Point d'entrée isolé : extrait uniquement PlayerObservation pour decision.decideur."""
    obs = state.get_observation(decision.decideur)
    return BotB0.choose(obs, decision, state.cfg)


def play_game_b0(
    state: GameState,
    *,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
) -> GameOver:
    """Exécute une partie complète pilotée par B0 jusqu'à GameOver avec garde-fou max_steps."""
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            cfg = state.cfg
            raise RuntimeError(
                f"Garde-fou max_steps={max_steps} dépassé : "
                f"mode={cfg.mode}, chassis_id={chassis_id}, n_players={cfg.n_players}, "
                f"exp_seed={cfg.exp_seed}, rep_id={cfg.rep_id}, tour={state.tour}, "
                f"step={state.step}, continuation={state._continuation!r}, "
                f"state_hex={state.raw_used_bytes().hex()}"
            )
        out = step_until_decision(
            state, max_internal_steps=max(2000, max_steps), telemetry=telemetry
        )
        if isinstance(out, GameOver):
            return out
        choice = choose_b0(state, out)
        apply_choice(state, choice, telemetry=telemetry)
