"""Croyance bayésienne isolée, Ticks discrets 1..3 et révision muette 2.2 (stdlib PyPy 3.11)."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from engine.core_engine import (
    DEC_HUMAIN_CHAMAN_2_1,
    DEC_MAMMIFERE_DUEL_2,
    DEC_OISEAU_PLUME_2,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    advance_step2_to_2_2,
    apply_mammifere_duel_choice,
    apply_oiseau_plume_choice,
    apply_step2_def1,
    apply_step2_def2,
    clear_step2_pending_wait,
    finish_step2_to_3_1,
    list_legal_targets,
)
from engine.primitives import DecisionRequest
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CANONICAL_DOTATION,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_NONE,
    CHAMAN_TAMBOUR,
    DUEL_TERRITOIRE_TENU,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    NUM_PARCELS,
    PIEGE_ACTIF,
    PLUME_CALME,
    PLUME_CHAUD,
    PLUME_KIND_RAY,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    TACTIQUES_SPEC,
    TRACK_LEN,
    TRIG_RESONANCE,
    GameConfig,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    machine_card_code,
    machine_threat_key_3_2,
    resolve_reve_rank_cancellations,
    unpack_machine_card,
)

__all__ = (
    "BeliefSummary",
    "DecisionCallback",
    "TargetFilter",
    "TargetScorer",
    "any_tile_text_active",
    "build_belief_summary",
    "compute_private_urgency",
    "is_tile_text_active",
    "order_seats_by_tick_and_urgency",
    "resolve_step2_2_from_state",
    "resolve_step2_full_with_ticks",
    "softmax_select_index",
)

# Loi exacte de M = min(D1, D2) sur 2D6 équilibrés : P(M = k) = (13 - 2k) / 36 pour k = 1..6
_MIN_2D6_PROBS: tuple[float, ...] = (
    11.0 / 36.0,
    9.0 / 36.0,
    7.0 / 36.0,
    5.0 / 36.0,
    3.0 / 36.0,
    1.0 / 36.0,
)

TargetScorer = Callable[[PlayerObservation, GameConfig, "BeliefSummary", tuple[Any, ...], bool], float]
TargetFilter = Callable[[tuple[Any, ...], bool], bool]
DecisionCallback = Callable[[GameState, DecisionRequest, Any], None]


def is_tile_text_active(cfg: GameConfig, tile_id: str | None) -> bool:
    """Vrai si `tile_id` a son pouvoir texte actif (Mode >= 3 et profil non `NEUTRE`)."""
    if cfg.mode < 3 or not tile_id:
        return False
    return cfg.profile_for_slot(tile_id) is not None


def any_tile_text_active(cfg: GameConfig, tile_ids: tuple[str, ...] | None = None) -> bool:
    """Vrai si au moins une tuile en jeu (`cfg.lisiere_slots` ou `tile_ids`) possède un texte actif."""
    if cfg.mode < 3:
        return False
    slots = tile_ids if tile_ids is not None else cfg.lisiere_slots
    return any(cfg.profile_for_slot(tid) is not None for tid in slots)


@runtime_checkable
class HeldAwareScorer(Protocol):
    retreat_orphans: bool

    def __call__(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        target: tuple[Any, ...],
        is_first_defender: bool,
    ) -> float: ...

    def held_score(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        cur_spot: tuple[Any, ...],
    ) -> float: ...


@dataclass(frozen=True, slots=True)
class BeliefSummary:
    """Résumé bayésien calculé exclusivement depuis PlayerObservation (zéro fuite _buf)."""

    p_neighbor_sabotage: float
    drew_sabotage_or_none: bool
    own_machine_cancelled_by_reve: bool
    parcel_strike_prob: tuple[float, ...]
    parcel_expected_seuil: tuple[float, ...]
    parcel_bulldo_prob: tuple[float, ...]
    reve_open_prob_by_rank: tuple[float, ...]
    coop_lisiere_signals: int
    coop_furtivite_signals: int
    parcel_charge_prob: tuple[float, ...] = ()
    own_machine_cancel_prob: float = 0.0


def _next_non_razed_obs(obs: PlayerObservation, p_max: int, r: int, from_p: int) -> int | None:
    for p_cand in range(from_p + 1, p_max + 1):
        if not obs.is_route(r, p_cand):
            return p_cand
    return None


def _machine_effective_tokens_obs(
    machines: tuple[Any, ...], r: int, m_type: int
) -> tuple[int, int]:
    """Jetons physiques (rouges, bleus) de la machine (v6.2 : zéro +1 virtuel en Ratissage, INV-12)."""
    m_self = machines[r * 2 + m_type]
    return m_self.rouges, m_self.bleus


def _prob_at_least_k(probs: list[float], k: int) -> float:
    """Probabilité exacte P(sum X_i >= k) pour des Bernoulli indépendantes X_i ~ Bern(p_i)."""
    if k <= 0:
        return 1.0
    if not probs or len(probs) < k:
        return 0.0
    # dp[j] = P(exactement j succès), tronqué à k (j == k agrège >= k)
    dp = [0.0] * (k + 1)
    dp[0] = 1.0
    for p_raw in probs:
        p = max(0.0, min(1.0, p_raw))
        if p <= 0.0:
            continue
        q = 1.0 - p
        dp[k] = dp[k] + dp[k - 1] * p
        for j in range(k - 1, 0, -1):
            dp[j] = dp[j] * q + dp[j - 1] * p
        dp[0] *= q
    return max(0.0, min(1.0, dp[k]))


def _prob_unseen_beats_known(
    unseen_key4: tuple[int, int, int, int],
    known_key4: tuple[int, int, int, int],
    known_seat: int,
    unknown_seats: list[int],
) -> float:
    """Probabilité qu'une machine adverse inconnue batte une machine connue selon `machine_threat_key_3_2`."""
    if unseen_key4 > known_key4:
        return 1.0
    if unseen_key4 < known_key4:
        return 0.0
    if not unknown_seats:
        return 0.0
    # À égalité exacte sur (active, is_rat, eff_red, pos), la priorité va au plus petit siège (-seat)
    wins = sum(1 for s_u in unknown_seats if s_u < known_seat)
    return wins / len(unknown_seats)


def build_belief_summary(obs: PlayerObservation, cfg: GameConfig) -> BeliefSummary:
    """Infère la carte bayésienne des menaces et signaux uniquement depuis `obs`."""
    n = obs.n_players
    p_max = cfg.p_max
    own_seat = obs.observer_seat
    own_hand = obs.hand_of(own_seat)
    machines = obs.machines

    drew_sab = (not own_hand.has_card) or (own_hand.card in (CARD_SABOTAGE, CARD_ECAILLE))
    own_cancelled = False
    own_cancel_prob = 0.0

    strike_prob = [0.0] * NUM_PARCELS
    seuil_sum = [0.0] * NUM_PARCELS
    seuil_w = [0.0] * NUM_PARCELS
    bulldo_prob = [0.0] * NUM_PARCELS
    charge_prob = [0.0] * NUM_PARCELS
    reve_prob = [0.0] * TRACK_LEN

    # Signaux coopératifs ALLIÉS (en excluant strictement les propres pions de `own_seat` !)
    own_l1 = obs.player_def1_lisiere_slot(own_seat)
    own_l2 = obs.player_def2_lisiere_slot(own_seat)
    lis_signals = 0
    if obs.mode >= 2:
        for slot_idx in range(2 * n):
            _, st_l, nb_c = obs.lisiere_tile_info(slot_idx)
            own_on_slot = (1 if own_l1 == slot_idx else 0) + (1 if own_l2 == slot_idx else 0)
            if st_l == LISIERE_UNCONSTRUCTED and nb_c == 1 and own_on_slot == 0:
                lis_signals += 1

    own_f1 = obs.player_def1_furtivite_target(own_seat)
    own_f2 = obs.player_def2_furtivite_target(own_seat)
    furt_signals = 0
    furt_sab_signals = 0
    for r_idx in range(n):
        own_on_r0 = (1 if own_f1 == (r_idx, 0) else 0) + (1 if own_f2 == (r_idx, 0) else 0)
        if obs.furtivite_ray_rive_defs(r_idx, 0) == 1 and own_on_r0 == 0:
            furt_signals += 1
        own_on_r1 = (1 if own_f1 == (r_idx, 1) else 0) + (1 if own_f2 == (r_idx, 1) else 0)
        if obs.furtivite_ray_rive_defs(r_idx, 1) == 1 and own_on_r1 == 0:
            furt_signals += 1
            furt_sab_signals += 1

    def _add_strike(
        r: int,
        m_type: int,
        target_p: int,
        mod_seuil: int,
        prob: float,
        *,
        is_charge: bool = False,
    ) -> None:
        if prob <= 0.0 or obs.is_route(r, target_p):
            return
        idx = r * MAX_P + (target_p - 1)
        rouges, bleus = _machine_effective_tokens_obs(machines, r, m_type)
        if is_charge:
            rouges = 0
        base_s = CANONICAL_DOTATION[target_p - 1]
        s_eff = float(max(1, base_s + rouges - bleus + mod_seuil))
        strike_prob[idx] = min(2.5, strike_prob[idx] + prob)
        seuil_sum[idx] += prob * s_eff
        seuil_w[idx] += prob
        if m_type == MACHINE_BULLDOZER:
            bulldo_prob[idx] = min(1.0, bulldo_prob[idx] + prob)
        if is_charge:
            charge_prob[idx] = min(2.0, charge_prob[idx] + prob)

    def _add_tactique_strikes(r: int, m_type: int, pos_m: int, t_code: int, prob: float) -> None:
        if prob <= 0.0 or not is_tactique_code(t_code):
            return
        spec = TACTIQUES_SPEC[t_code]
        chg = is_tactique_charge(t_code, obs.tour)
        for c_kind in spec.cibles:
            if c_kind == "SUR_PLACE":
                _add_strike(r, m_type, pos_m, spec.mod_seuil, prob, is_charge=chg)
            elif c_kind == "DEVANT":
                p_dev = _next_non_razed_obs(obs, p_max, r, pos_m)
                if p_dev is not None:
                    _add_strike(r, m_type, p_dev, spec.mod_seuil, prob, is_charge=chg)

    # 1. Machines en Ratissage : certitude publique (prob = 1.0, ASSAUT permanent : SUR_PLACE, jetons physiques)
    normal_deck_machines: list[tuple[int, int, int]] = []
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            if st == MACHINE_STATUS_RATISSAGE:
                _add_strike(r, mt, pos, 0, 1.0, is_charge=False)
            elif st == MACHINE_STATUS_NORMAL:
                normal_deck_machines.append((machine_card_code(r, mt), r, mt))

    # 2. Collecte des mains visibles et inconnues
    known_machine_cards: set[int] = set()
    known_sabotages = 0
    unknown_seats: list[int] = []
    # (seat, card, r_m, mt_m, pos_m, st_m, eff_red_m) groupés par rank_idx 0..5
    known_by_rank: list[list[tuple[int, int, int, int, int, int, int]]] = [
        [] for _ in range(TRACK_LEN)
    ]

    for s in range(n):
        h = obs.hand_of(s)
        if not h.has_card:
            continue
        if h.card is None:
            unknown_seats.append(s)
            continue
        if h.card in (CARD_SABOTAGE, CARD_ECAILLE):
            known_sabotages += 1
            continue
        if 1 <= h.card <= 2 * n:
            known_machine_cards.add(h.card)
            r_m, mt_m = unpack_machine_card(h.card)
            pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
            lec = h.lecture_m
            if st_m == MACHINE_STATUS_NORMAL and pos_m > 0 and lec is not None and 1 <= lec <= 6:
                eff_red_m = obs.machine_effective_rouges(r_m, mt_m)
                known_by_rank[lec - 1].append((s, h.card, r_m, mt_m, pos_m, st_m, eff_red_m))

    unknown_holders = len(unknown_seats)

    # 3. Paravents ouverts (zéro main inconnue) : résolution EXACTE partagée avec le moteur !
    if unknown_holders == 0:
        p_sab_post = 0.0
        for rank_idx in range(TRACK_LEN):
            entries = known_by_rank[rank_idx]
            if not entries:
                continue
            case_1_6 = rank_idx + 1
            t_code, _ = obs.tactique_code_bugs(rank_idx)
            if is_reve_code(t_code):
                reve_prob[rank_idx] = 1.0
                n_def_r = obs.reve_activation_defenders(case_1_6)
                cancelled_seats = resolve_reve_rank_cancellations(
                    [(e[0], e[4], e[5], e[6]) for e in entries],
                    n_def_r,
                )
                for s_e, _c_e, r_m, mt_m, pos_m, _st_m, _red_m in entries:
                    if s_e in cancelled_seats:
                        if s_e == own_seat:
                            own_cancelled = True
                            own_cancel_prob = 1.0
                        continue
                    # Machine non annulée sous un Rêve -> exécute la Tactique imprimée T{case_1_6}
                    _add_tactique_strikes(r_m, mt_m, pos_m, case_1_6, 1.0)
            else:
                for _s_e, _c_e, r_m, mt_m, pos_m, _st_m, _red_m in entries:
                    _add_tactique_strikes(r_m, mt_m, pos_m, t_code, 1.0)
    else:
        # 4. Paravents fermés : loi bayésienne des mains adverses + priorité exacte Rêves (Poisson-Binomiale)
        unseen_machines = [
            item for item in normal_deck_machines if item[0] not in known_machine_cards
        ]
        m_rem = len(unseen_machines)
        sab_rem = max(0, obs.sabotage_deck_count + obs.ecaille_deck_count - known_sabotages)
        denom = max(1, m_rem + sab_rem)
        p_sab_prior = sab_rem / denom

        # Mise à jour bayésienne par les seuls signaux ALLIÉS corrélés au Sabotage
        coop_evidence = min(3, lis_signals + furt_sab_signals)
        if p_sab_prior > 0.0 and coop_evidence > 0:
            lr = 1.0 + 0.28 * coop_evidence
            odds = (p_sab_prior / max(1e-6, 1.0 - p_sab_prior)) * lr
            p_sab_post = odds / (1.0 + odds)
        else:
            p_sab_post = p_sab_prior

        expected_active_draws = unknown_holders * (1.0 - p_sab_post)

        # Pré-calcul des probabilités de tirage et clés de menace des machines inconnues
        unseen_info: list[tuple[int, int, int, int, tuple[int, int, int, int], float]] = []
        if m_rem > 0 and expected_active_draws > 0.0:
            weights: list[float] = []
            w_total = 0.0
            for _, r_u, mt_u in unseen_machines:
                pos_u, _ = obs.machine_pos_status(r_u, mt_u)
                defs_near = obs.parcel_defenseurs(r_u, pos_u) if pos_u > 0 else 0
                p_dev_u = _next_non_razed_obs(obs, p_max, r_u, pos_u) if pos_u > 0 else None
                if p_dev_u is not None:
                    defs_near += obs.parcel_defenseurs(r_u, p_dev_u)
                own_on_piege = (1 if own_f1 == (r_u, 0) else 0) + (
                    1 if own_f2 == (r_u, 0) else 0
                )
                own_on_sab = (1 if own_f1 == (r_u, 1) else 0) + (1 if own_f2 == (r_u, 1) else 0)
                ally_piege_sig = max(0, obs.furtivite_ray_rive_defs(r_u, 0) - own_on_piege)
                ally_sab_sig = max(0, obs.furtivite_ray_rive_defs(r_u, 1) - own_on_sab)
                w_m = 1.0 + 0.35 * min(2, defs_near) + 1.15 * min(1, ally_piege_sig)
                if ally_sab_sig >= 1 and ally_piege_sig <= 0:
                    w_m = max(0.35, w_m - 0.25)
                weights.append(w_m)
                w_total += w_m

            for idx_u, (_, r_u, mt_u) in enumerate(unseen_machines):
                pos_u, st_u = obs.machine_pos_status(r_u, mt_u)
                if pos_u <= 0 or st_u == MACHINE_STATUS_RETIRED:
                    continue
                p_card = min(0.95, expected_active_draws * (weights[idx_u] / max(1e-6, w_total)))
                eff_red_u = obs.machine_effective_rouges(r_u, mt_u)
                k4_u = (1, 1 if st_u == MACHINE_STATUS_RATISSAGE else 0, eff_red_u, pos_u)
                unseen_info.append((r_u, mt_u, pos_u, st_u, k4_u, p_card))

        # 4a. Résolution des mains connues (ex. own_seat) sous la loi exacte des mains adverses compatibles
        for rank_idx in range(TRACK_LEN):
            entries = known_by_rank[rank_idx]
            if not entries:
                continue
            case_1_6 = rank_idx + 1
            t_code, _ = obs.tactique_code_bugs(rank_idx)
            if not is_reve_code(t_code):
                for _s_e, _c_e, r_m, mt_m, pos_m, _st_m, _red_m in entries:
                    _add_tactique_strikes(r_m, mt_m, pos_m, t_code, 1.0)
                continue

            reve_prob[rank_idx] = 1.0
            n_def_r = obs.reve_activation_defenders(case_1_6)
            p_m_val = _MIN_2D6_PROBS[rank_idx]
            for s_e, _c_e, r_m, mt_m, pos_m, st_m, red_m in entries:
                if n_def_r <= 0:
                    p_exec_k = 1.0
                else:
                    my_key = machine_threat_key_3_2(s_e, pos_m, st_m, red_m)
                    known_ahead = sum(
                        1
                        for e2 in entries
                        if e2[0] != s_e
                        and machine_threat_key_3_2(e2[0], e2[4], e2[5], e2[6]) > my_key
                    )
                    rem_def = n_def_r - known_ahead
                    if rem_def <= 0:
                        p_exec_k = 1.0
                    elif rem_def > unknown_holders:
                        p_exec_k = 0.0
                    else:
                        my_key4 = my_key[:4]
                        ahead_probs: list[float] = []
                        for _ru, _mtu, _posu, _stu, k4_u, p_card in unseen_info:
                            p_beat = _prob_unseen_beats_known(k4_u, my_key4, s_e, unknown_seats)
                            if p_beat > 0.0:
                                ahead_probs.append(p_card * p_m_val * p_beat)
                        p_exec_k = _prob_at_least_k(ahead_probs, rem_def)
                p_cancel_k = 1.0 - p_exec_k
                if s_e == own_seat:
                    own_cancel_prob = p_cancel_k
                    own_cancelled = p_cancel_k >= 0.5
                if p_exec_k > 0.0:
                    _add_tactique_strikes(r_m, mt_m, pos_m, case_1_6, p_exec_k)

        # 4b. Résolution des mains inconnues adverses sous la même règle de priorité Rêves
        if unseen_info:
            rem_unknown_scale = (
                max(0.0, expected_active_draws - 1.0) / max(1e-6, expected_active_draws)
                if unknown_holders > 1
                else 0.0
            )
            for idx_u, (r_u, mt_u, pos_u, _st_u, k4_u, p_card_u) in enumerate(unseen_info):
                for rank_idx in range(TRACK_LEN):
                    p_m_val = _MIN_2D6_PROBS[rank_idx]
                    p_joint = p_card_u * p_m_val
                    t_code, _ = obs.tactique_code_bugs(rank_idx)
                    case_1_6 = rank_idx + 1
                    p_exec = p_joint
                    if is_reve_code(t_code):
                        reve_prob[rank_idx] = 1.0 - (1.0 - reve_prob[rank_idx]) * (1.0 - p_joint)
                        n_def_r = obs.reve_activation_defenders(case_1_6)
                        if n_def_r > 0:
                            # Probabilités exactes que chaque concurrent (connu ou inconnu) batte `u`
                            ahead_all: list[float] = []
                            for s_k, _ck, _rk, _mtk, pos_k, st_k, red_k in known_by_rank[rank_idx]:
                                k4_k = machine_threat_key_3_2(s_k, pos_k, st_k, red_k)[:4]
                                p_k_beats_u = 1.0 - _prob_unseen_beats_known(
                                    k4_u, k4_k, s_k, unknown_seats
                                )
                                if p_k_beats_u > 0.0:
                                    ahead_all.append(p_k_beats_u)
                            if unknown_holders > 1:
                                for idx_v, (_rv, _mtv, _posv, _stv, k4_v, p_card_v) in enumerate(
                                    unseen_info
                                ):
                                    if idx_v == idx_u:
                                        continue
                                    if k4_v > k4_u:
                                        p_v_beats = 1.0
                                    elif k4_v == k4_u:
                                        p_v_beats = 0.5
                                    else:
                                        p_v_beats = 0.0
                                    if p_v_beats > 0.0:
                                        ahead_all.append(
                                            min(0.95, p_card_v * rem_unknown_scale)
                                            * p_m_val
                                            * p_v_beats
                                        )
                            p_not_cancelled = _prob_at_least_k(ahead_all, n_def_r)
                            p_exec = p_joint * p_not_cancelled
                    _add_tactique_strikes(r_u, mt_u, pos_u, case_1_6, p_exec)

    expected_seuil: list[float] = []
    for r in range(n):
        for p in range(1, MAX_P + 1):
            idx = r * MAX_P + (p - 1)
            if p <= p_max and seuil_w[idx] > 1e-6:
                expected_seuil.append(seuil_sum[idx] / seuil_w[idx])
            elif p <= p_max:
                expected_seuil.append(float(max(1, CANONICAL_DOTATION[p - 1])))
            else:
                expected_seuil.append(1.0)

    return BeliefSummary(
        p_neighbor_sabotage=p_sab_post,
        drew_sabotage_or_none=drew_sab,
        own_machine_cancelled_by_reve=own_cancelled,
        parcel_strike_prob=tuple(strike_prob),
        parcel_expected_seuil=tuple(expected_seuil),
        parcel_bulldo_prob=tuple(bulldo_prob),
        reve_open_prob_by_rank=tuple(reve_prob),
        coop_lisiere_signals=lis_signals,
        coop_furtivite_signals=furt_signals,
        parcel_charge_prob=tuple(charge_prob),
        own_machine_cancel_prob=own_cancel_prob,
    )


def compute_private_urgency(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary | None = None,
    *,
    is_first_defender: bool = True,
) -> tuple[int, float]:
    """Calcule `(tick_1_2_3, U_i)` avec `U_i in [0, 1]` exclusivement depuis `PlayerObservation`.

    - Tick 1 (`U_i >= 0.80`) : joueur ayant tiré `CARD_SABOTAGE` / sans carte (émetteur altruiste
      naturel sur tuile G/R/M ou Furtivité), complétion certaine `Rive Piège` (`m(r) == 2`), ou urgence vitale.
    - Tick 2 (`0.45 <= U_i < 0.80`) : menace machine directe non couverte ou signal partenaire ouvert.
    - Tick 3 (`U_i < 0.45`) : main annulée par un Rêve ou déjà couverte (attend les signaux Tick 1/2).
    """
    bel = belief if belief is not None else build_belief_summary(obs, cfg)
    own_seat = obs.observer_seat
    own_hand = obs.hand_of(own_seat)
    p_max = cfg.p_max

    # 1. Émetteur altruiste Sabotage / pénurie : agit prioritairement au Tick 1 !
    if bel.drew_sabotage_or_none:
        has_coop_slot = obs.mode >= 2 or bel.coop_furtivite_signals > 0 or obs.tour <= 6
        u_sab = 0.94 if has_coop_slot else 0.84
        if bel.coop_lisiere_signals > 0 or bel.coop_furtivite_signals > 0:
            u_sab = min(0.99, u_sab + 0.04)
        return 1, u_sab

    # Urgence haute dédiée Furtivité Rive Piège si nous détenons la 2e machine (indépendant d'une annulation Rêve !)
    u_piege_cert = 0.0
    if own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players:
        r_c, mt_c = unpack_machine_card(own_hand.card)
        _, st_c = obs.machine_pos_status(r_c, mt_c)
        if st_c == MACHINE_STATUS_NORMAL and obs.is_ray_furtivite_open(r_c):
            _, st_other = obs.machine_pos_status(r_c, 1 - mt_c)
            own_f1 = obs.player_def1_furtivite_target(own_seat)
            ally_piege_d1 = obs.furtivite_ray_def1_rive_count(r_c, 0) - (
                1 if own_f1 == (r_c, 0) else 0
            )
            if not is_first_defender and obs.furtivite_ray_rive_defs(r_c, 0) == 1:
                if ally_piege_d1 >= 1 or st_other == MACHINE_STATUS_RATISSAGE:
                    u_piege_cert = 0.89
            elif is_first_defender and st_other == MACHINE_STATUS_RATISSAGE:
                u_piege_cert = 0.85

    # 2. Carte Machine annulée par un Rêve : faible urgence privée sauf complétion certaine Rive Piège !
    if bel.own_machine_cancelled_by_reve and u_piege_cert < 0.80:
        if bel.coop_lisiere_signals > 0 or bel.coop_furtivite_signals > 0:
            return 2, 0.56
        return 3, 0.28

    # 3. Joueur détenant une carte Machine active (y compris Tactique imprimée sous Rêve non annulé !)
    u_val = max(0.35, u_piege_cert)
    if own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players:
        r_m, mt_m = unpack_machine_card(own_hand.card)
        pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
        lec = own_hand.lecture_m
        if st_m == MACHINE_STATUS_NORMAL and pos_m > 0 and lec is not None and 1 <= lec <= 6:
            t_code, _ = obs.tactique_code_bugs(lec - 1)
            eff_t_code = lec if is_reve_code(t_code) else t_code
            if is_tactique_code(eff_t_code):
                spec = TACTIQUES_SPEC[eff_t_code]
                cand_ps: list[int] = []
                for c_kind in spec.cibles:
                    if c_kind == "SUR_PLACE" and not obs.is_route(r_m, pos_m):
                        cand_ps.append(pos_m)
                    elif c_kind == "DEVANT":
                        p_dev = _next_non_razed_obs(obs, p_max, r_m, pos_m)
                        if p_dev is not None:
                            cand_ps.append(p_dev)
                for tp in cand_ps:
                    cur_def = obs.parcel_defenseurs(r_m, tp) + obs.parcel_insectes(r_m, tp)
                    idx = r_m * MAX_P + (tp - 1)
                    seuil_est = bel.parcel_expected_seuil[idx]
                    piege_armed = obs.parcel_piege(r_m, tp) == PIEGE_ACTIF
                    if not piege_armed and cur_def < seuil_est:
                        # Menace directe non parée
                        own_ray_access = (not is_first_defender) or (r_m == own_seat)
                        arbres = obs.parcel_arbres(r_m, tp)
                        danger = 0.62 if own_ray_access else 0.52
                        if arbres <= 1 or mt_m == MACHINE_BULLDOZER:
                            danger += 0.16
                        if len(spec.cibles) >= 2:
                            danger += 0.06
                        u_val = max(u_val, min(0.86, danger))

    # Bonus d'opportunité si un voisin a ouvert un chantier ou binôme Furtivité
    if bel.coop_lisiere_signals > 0 or bel.coop_furtivite_signals > 0:
        u_val = max(u_val, 0.54)

    u_clamped = max(0.0, min(1.0, u_val))
    if u_clamped >= 0.80:
        return 1, u_clamped
    if u_clamped >= 0.45:
        return 2, u_clamped
    return 3, u_clamped


def order_seats_by_tick_and_urgency(
    items: list[tuple[int, int, float]],
    cfg: GameConfig,
    tour: int,
    sous_etape: int,
) -> list[int]:
    """Trie `(seat, tick, U_i)` par Tick croissant puis `U_i` décroissant avec bris d'égalité PRNG sans biais."""
    keyed: list[tuple[int, int, int, int]] = []
    for seat, tick, u_val in items:
        tb = rand_u64(cfg.exp_seed, cfg.rep_id, SRC_BOT_TIEBREAK, tour, sous_etape, seat)
        # Clé entière déterministe : tick ascendant, -U_i descendant, -tb descendant
        keyed.append((tick, -round(u_val * 1_000_000), -tb, seat))
    keyed.sort()
    return [item[3] for item in keyed]


_U64_NORM_SOFTMAX: float = float(1 << 64)


def softmax_select_index(
    scores: list[float],
    tau: float,
    cfg: GameConfig,
    obs: PlayerObservation,
    salt: int,
) -> int:
    """Sélectionne un indice dans `scores` par softmax déterministe (`rand_u64`) à température `tau`.

    - Si `tau <= 0.0` ou `len(scores) <= 1` : argmax exact avec bris d'égalité déterministe `rand_u64`.
    - Si `tau > 0.0` : tirage inverse-CDF sur `exp((s_i - max_s) / tau)` (100 % stdlib, sans `random`).
    """
    m = len(scores)
    assert m >= 1
    if m == 1:
        return 0
    if tau <= 0.0:
        best_idx = 0
        best_sc = scores[0]
        best_tb = -1
        for idx in range(1, m):
            sc = scores[idx]
            if sc > best_sc + 1e-9:
                best_sc = sc
                best_idx = idx
                best_tb = -1
            elif abs(sc - best_sc) <= 1e-9:
                if best_tb < 0:
                    best_tb = rand_u64(
                        cfg.exp_seed,
                        cfg.rep_id,
                        SRC_BOT_TIEBREAK,
                        obs.tour,
                        obs.observer_seat,
                        (salt * 64 + best_idx) & 0xFFFFFFFF,
                    )
                tb = rand_u64(
                    cfg.exp_seed,
                    cfg.rep_id,
                    SRC_BOT_TIEBREAK,
                    obs.tour,
                    obs.observer_seat,
                    (salt * 64 + idx) & 0xFFFFFFFF,
                )
                if tb > best_tb:
                    best_tb = tb
                    best_idx = idx
        return best_idx

    max_s = max(scores)
    inv_tau = 1.0 / tau
    weights: list[float] = []
    total_w = 0.0
    for s_val in scores:
        z = (s_val - max_s) * inv_tau
        w = math.exp(z) if z > -60.0 else 0.0
        weights.append(w)
        total_w += w

    if total_w <= 0.0:
        return 0

    u_raw = rand_u64(
        cfg.exp_seed,
        cfg.rep_id,
        SRC_BOT_TIEBREAK,
        obs.tour,
        obs.observer_seat,
        (salt * 97 + 13) & 0xFFFFFFFF,
    )
    threshold = (float(u_raw) / _U64_NORM_SOFTMAX) * total_w
    acc = 0.0
    for idx, w in enumerate(weights):
        acc += w
        if acc >= threshold:
            return idx
    return m - 1


def _pick_best_target_isolated(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    targets: tuple[Any, ...],
    scorer: TargetScorer,
    *,
    is_first_defender: bool,
    sous_etape_salt: int,
) -> tuple[tuple[Any, ...], float]:
    assert len(targets) >= 1
    tau = float(getattr(scorer, "softmax_tau", 0.0))
    if tau > 0.0 and len(targets) > 1:
        scores = [scorer(obs, cfg, belief, cand, is_first_defender) for cand in targets]
        chosen_idx = softmax_select_index(scores, tau, cfg, obs, sous_etape_salt)
        return targets[chosen_idx], scores[chosen_idx]

    best_t = targets[0]
    best_sc = scorer(obs, cfg, belief, best_t, is_first_defender)
    best_tb = -1
    best_idx = 0

    for idx in range(1, len(targets)):
        cand = targets[idx]
        sc = scorer(obs, cfg, belief, cand, is_first_defender)
        if sc > best_sc + 1e-9:
            best_sc = sc
            best_tb = -1
            best_idx = idx
            best_t = cand
        elif abs(sc - best_sc) <= 1e-9:
            if best_tb < 0:
                best_tb = rand_u64(
                    cfg.exp_seed,
                    cfg.rep_id,
                    SRC_BOT_TIEBREAK,
                    obs.tour,
                    obs.observer_seat,
                    (sous_etape_salt * 64 + best_idx) & 0xFFFFFFFF,
                )
            tb = rand_u64(
                cfg.exp_seed,
                cfg.rep_id,
                SRC_BOT_TIEBREAK,
                obs.tour,
                obs.observer_seat,
                (sous_etape_salt * 64 + idx) & 0xFFFFFFFF,
            )
            if tb > best_tb:
                best_tb = tb
                best_idx = idx
                best_t = cand
    return best_t, best_sc


def _get_isolated_obs(
    state: GameState, seat: int, *, counterfactual_open_paravents: bool = False
) -> PlayerObservation:
    if not counterfactual_open_paravents or state.paravents_ouverts:
        return state.get_observation(seat)
    # Uniquement pour micro_fork contrefactuel (mesure de C_prive sur clone isolé)
    saved = state.paravents_ouverts
    state.paravents_ouverts = True
    try:
        return state.get_observation(seat)
    finally:
        state.paravents_ouverts = saved


def _current_def2_target_public(state: GameState, seat: int) -> tuple[Any, ...] | None:
    raw = state.get_player_def_loc_raw(seat, 1)
    if raw == 0:
        return None
    kind, a, b, c = state.decode_def_loc(raw)
    if kind == "FORET":
        return ("FORET", a, b)
    if kind == "FURTIVITE":
        return ("FURTIVITE", a, c // 2)
    if kind == "LISIERE":
        return ("LISIERE", a)
    if kind == "GARDIEN_PARI":
        return ("GARDIEN_PARI", a)
    if kind == "REVE_ACTIVATION":
        return ("REVE_ACTIVATION", a)
    return None


def _filter_legal_targets(
    targets: tuple[Any, ...],
    target_filter: TargetFilter | None,
    *,
    is_first_defender: bool,
    fallback_if_empty: bool,
) -> tuple[Any, ...]:
    if target_filter is None:
        return targets
    filtered = tuple(t for t in targets if target_filter(t, is_first_defender))
    if filtered or not fallback_if_empty:
        return filtered
    return targets


def _apply_step2_tick_accessories(
    state: GameState,
    seat: int,
    target: tuple[Any, ...],
    obs: PlayerObservation,
    belief: BeliefSummary,
    *,
    on_decision: DecisionCallback | None = None,
) -> None:
    """Active les accessoires Step 2 (M Duel DEFI, O Plume de Vigie) de manière isolée sur `obs`."""
    cfg = state.cfg
    if not cfg.accessories_enabled:
        return
    p_code = cfg.peuples[seat]
    if p_code == "M" and target[0] == "FORET":
        r_m, p_m = int(target[1]), int(target[2])
        if obs.duel_state != DUEL_TERRITOIRE_TENU and not obs.is_route(r_m, p_m):
            idx_m = r_m * MAX_P + (p_m - 1)
            chose_duel = belief.parcel_strike_prob[idx_m] >= 0.15 or obs.duel_state == 0
            if on_decision is not None:
                on_decision(
                    state,
                    DecisionRequest(
                        seat,
                        DEC_MAMMIFERE_DUEL_2,
                        ("POSER_DUEL_DEFI", "PASSER"),
                        {"tour": state.tour, "ray": r_m, "p": p_m},
                    ),
                    "POSER_DUEL_DEFI" if chose_duel else "PASSER",
                )
            if chose_duel:
                apply_mammifere_duel_choice(state, True, r_m, p_m)
    elif p_code == "O" and not obs.oiseau_plume[3]:
        own_h = obs.hand_of(seat)
        plume_choice: Any = "PASSER"
        if own_h.card is not None and 1 <= own_h.card <= 2 * obs.n_players:
            r_o, _ = unpack_machine_card(own_h.card)
            plume_choice = (PLUME_CHAUD, PLUME_KIND_RAY, r_o)
        elif (not own_h.has_card) or own_h.card in (CARD_SABOTAGE, CARD_ECAILLE):
            plume_choice = (PLUME_CALME, PLUME_KIND_RAY, seat)
        if on_decision is not None:
            on_decision(
                state,
                DecisionRequest(
                    seat,
                    DEC_OISEAU_PLUME_2,
                    (
                        (PLUME_CHAUD, PLUME_KIND_RAY, seat),
                        (PLUME_CALME, PLUME_KIND_RAY, seat),
                        "PASSER",
                    ),
                    {"tour": state.tour},
                ),
                plume_choice,
            )
        if plume_choice != "PASSER":
            apply_oiseau_plume_choice(state, plume_choice)


def resolve_step2_2_from_state(
    state: GameState,
    scorer: TargetScorer,
    *,
    k_max_passes: int | None = None,
    epsilon_base: float = 28.0,
    epsilon_step: float = 12.0,
    counterfactual_open_paravents: bool = False,
    target_filter: TargetFilter | None = None,
    post_revision_hook: Callable[[GameState], int] | None = None,
    telemetry: Any | None = None,
    on_decision: DecisionCallback | None = None,
) -> dict[str, int]:
    """Résout l'Étape 2.2 (pose initiale Ticks 1..3 + jusqu'à K_max passes de révision muette).

    Sépare strictement chaque évaluation de siège via `PlayerObservation`.
    Retourne les compteurs `{passes_executed, revision_moves}` pour télémétrie et micro-forks.
    """
    cfg = state.cfg
    n = cfg.n_players
    max_passes = (
        min(4, max(0, k_max_passes))
        if k_max_passes is not None
        else min(4, max(0, cfg.max_revision_passes))
    )
    clear_step2_pending_wait(state)

    # 1. Pose initiale du 2e Défenseur en Ticks discrets t = 1, 2, 3
    remaining = [s for s in range(n) if state.get_player_def_loc_raw(s, 1) == 0]
    for current_tick in (1, 2, 3):
        if not remaining:
            break
        tick_candidates: list[tuple[int, int, float]] = []
        for s in remaining:
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            bel_s = build_belief_summary(obs_s, cfg)
            t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=False)
            if t_s <= current_tick or current_tick == 3:
                tick_candidates.append((s, current_tick, u_s))

        ordered = order_seats_by_tick_and_urgency(
            tick_candidates, cfg, state.tour, 220 + current_tick
        )
        for s in ordered:
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            bel_s = build_belief_summary(obs_s, cfg)
            legal_2 = _filter_legal_targets(
                list_legal_targets(state, s, is_first_defender=False),
                target_filter,
                is_first_defender=False,
                fallback_if_empty=True,
            )
            if not legal_2:
                if on_decision is not None:
                    on_decision(
                        state,
                        DecisionRequest(
                            s,
                            DEC_POSE_DEFENSEUR_2,
                            (("POSER_DEFINITIF", ("PASSER_IMPASSE",)),),
                            {"tour": state.tour, "step": "2.2", "phase": "init"},
                        ),
                        ("POSER_DEFINITIF", ("PASSER_IMPASSE",)),
                    )
                apply_step2_def2(
                    state,
                    s,
                    ("POSER_DEFINITIF", ("PASSER_IMPASSE",)),
                    check_legal=False,
                    telemetry=telemetry,
                )
            else:
                target_2, _ = _pick_best_target_isolated(
                    obs_s,
                    cfg,
                    bel_s,
                    legal_2,
                    scorer,
                    is_first_defender=False,
                    sous_etape_salt=220 + current_tick,
                )
                act_kind = "POSER_REFLEXION" if max_passes > 0 else "POSER_DEFINITIF"
                if on_decision is not None:
                    on_decision(
                        state,
                        DecisionRequest(
                            s,
                            DEC_POSE_DEFENSEUR_2,
                            tuple((act_kind, t) for t in legal_2),
                            {"tour": state.tour, "step": "2.2", "phase": "init"},
                        ),
                        (act_kind, target_2),
                    )
                apply_step2_def2(
                    state, s, (act_kind, target_2), check_legal=False, telemetry=telemetry
                )
                _apply_step2_tick_accessories(
                    state, s, target_2, obs_s, bel_s, on_decision=on_decision
                )
            remaining.remove(s)

    # 2. Passes de révision 1..max_passes par gain marginal Delta_V_i > epsilon_r
    passes_done = 0
    total_rev_moves = 0
    for pass_idx in range(1, max_passes + 1):
        refl_seats = [
            s
            for s in range(n)
            if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s)
        ]
        if not refl_seats:
            break

        passes_done += 1
        eps_r = epsilon_base + (pass_idx - 1) * epsilon_step
        pass_items: list[tuple[int, int, float]] = []
        for s in refl_seats:
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            bel_s = build_belief_summary(obs_s, cfg)
            t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=False)
            pass_items.append((s, t_s, u_s))

        ordered_rev = order_seats_by_tick_and_urgency(
            pass_items, cfg, state.tour, 230 + pass_idx
        )
        moved_in_pass = 0
        for s in ordered_rev:
            cur_spot = _current_def2_target_public(state, s)
            if cur_spot is None:
                continue
            legal_alt = _filter_legal_targets(
                tuple(
                    t
                    for t in list_legal_targets(
                        state, s, is_first_defender=False, exclude_own_def2=True
                    )
                    if t != cur_spot
                ),
                target_filter,
                is_first_defender=False,
                fallback_if_empty=False,
            )
            if not legal_alt:
                apply_step2_def2(
                    state, s, ("GARDER_REFLEXION", None), check_legal=False, telemetry=telemetry
                )
                continue

            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            bel_s = build_belief_summary(obs_s, cfg)
            # Valeur du maintien sur place (évaluée dans l'état courant où notre pion y figure déjà :
            # on soustrait temporairement 1 pion virtuel en scorant cur_spot via _score_current_held)
            cur_val = _score_held_spot(obs_s, cfg, bel_s, cur_spot, scorer)
            best_alt, best_alt_val = _pick_best_target_isolated(
                obs_s,
                cfg,
                bel_s,
                legal_alt,
                scorer,
                is_first_defender=False,
                sous_etape_salt=230 + pass_idx,
            )
            if best_alt_val - cur_val > eps_r:
                if on_decision is not None:
                    on_decision(
                        state,
                        DecisionRequest(
                            s,
                            DEC_POSE_DEFENSEUR_2,
                            tuple(("DEPLACER_REFLEXION", t) for t in legal_alt),
                            {"tour": state.tour, "step": "2.2", "phase": "revision", "pass": pass_idx},
                        ),
                        ("DEPLACER_REFLEXION", best_alt),
                    )
                moved = apply_step2_def2(
                    state,
                    s,
                    ("DEPLACER_REFLEXION", best_alt),
                    check_legal=False,
                    telemetry=telemetry,
                )
                if moved:
                    _apply_step2_tick_accessories(
                        state, s, best_alt, obs_s, bel_s, on_decision=on_decision
                    )
                    moved_in_pass += 1
                    total_rev_moves += 1
            else:
                apply_step2_def2(
                    state, s, ("GARDER_REFLEXION", None), check_legal=False, telemetry=telemetry
                )

        # Arrêt immédiat dès qu'une passe produit 0 mouvement (retournement simultané en définitif)
        if moved_in_pass == 0:
            break

    # 3. Retrait propre en fin de passes « en réflexion » si un Réveil n'a pas atteint son quota Q
    #    (évite les Défenseurs orphelins inutiles, strictement sur observation publique PlayerObservation)
    # 3a. Retrait propre en fin de passes « en réflexion » pour le Pari d'activation des Gardiens :
    #     sur tout Gardien sans texte actif (Mode 2 ou slot NEUTRE en Mode 3/4), un 2e pion ou un pari
    #     sur un Gardien déjà Face 2 (ou au Tour 8) n'apporte aucun gain et risque l'échec :
    #     tout 2e Défenseur encore en réflexion se replie vers la meilleure cible hors GARDIEN_PARI.
    if max_passes > 0 and cfg.mode >= 2 and cfg.nb_animaux_sauvages >= 1:
        for s in range(n):
            if state.get_player_def_loc_raw(s, 1) == 0 or state.is_player_def2_definitif(s):
                continue
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            pari_c = obs_s.player_def2_gardien_pari_case(s)
            if pari_c <= 0:
                continue
            need_gard_retreat = False
            g_slot_c = obs_s.piste_gardiens[pari_c - 1]
            if not is_tile_text_active(cfg, g_slot_c.tile_id):
                # Gardien neutre (Mode 2 ou NEUTRE en Mode 3/4, Éveil cumulatif A+1 Face 2, Tours 1..7) :
                # parier 1 pion sur un Gardien Face 1 le promeut vers Face 2 ; un 2e pion ou un pari
                # sur un Gardien déjà Face 2 (ou au Tour 8) n'apporte aucun gain et risque l'échec.
                g_face_c = obs_s.gardien_face_at_case(pari_c)
                if (
                    obs_s.tour >= 8
                    or g_face_c >= 2
                    or obs_s.gardien_pari_defenders(pari_c) >= 2
                ):
                    need_gard_retreat = True
            if pari_c == TRIG_RESONANCE:
                res_bets = obs_s.gardien_pari_defenders(TRIG_RESONANCE)
                distinct_other_cases = sum(
                    1
                    for ck in (1, 2, 3, 4, 5)
                    if obs_s.gardien_present_at_case(ck)
                    and obs_s.gardien_pari_defenders(ck) >= 1
                )
                if distinct_other_cases < res_bets:
                    # Impossible d'allumer 6. Résonance assez de fois pour consommer tous les paris dessus !
                    need_gard_retreat = True
            if need_gard_retreat:
                legal_non_pari = _filter_legal_targets(
                    tuple(
                        t
                        for t in list_legal_targets(
                            state, s, is_first_defender=False, exclude_own_def2=True
                        )
                        if t[0] != "GARDIEN_PARI"
                    ),
                    target_filter,
                    is_first_defender=False,
                    fallback_if_empty=False,
                )
                if legal_non_pari:
                    bel_s = build_belief_summary(obs_s, cfg)
                    fallback_t, _ = _pick_best_target_isolated(
                        obs_s,
                        cfg,
                        bel_s,
                        legal_non_pari,
                        scorer,
                        is_first_defender=False,
                        sous_etape_salt=249,
                    )
                    if on_decision is not None:
                        on_decision(
                            state,
                            DecisionRequest(
                                s,
                                DEC_POSE_DEFENSEUR_2,
                                tuple(("DEPLACER_REFLEXION", t) for t in legal_non_pari),
                                {"tour": state.tour, "step": "2.2", "phase": "retreat_gardien"},
                            ),
                            ("DEPLACER_REFLEXION", fallback_t),
                        )
                    moved = apply_step2_def2(
                        state,
                        s,
                        ("DEPLACER_REFLEXION", fallback_t),
                        check_legal=False,
                        telemetry=telemetry,
                    )
                    if moved:
                        _apply_step2_tick_accessories(
                            state, s, fallback_t, obs_s, bel_s, on_decision=on_decision
                        )
                        total_rev_moves += 1

    # 3b. Retrait propre en fin de passes « en réflexion » des Défenseurs restés seuls (1/2) sur un
    #     chantier de Lisière ou une rive de Furtivité (0 effet sans binôme complet), pour B2.
    if max_passes > 0 and isinstance(scorer, HeldAwareScorer) and scorer.retreat_orphans:
        for s in range(n):
            if state.get_player_def_loc_raw(s, 1) == 0 or state.is_player_def2_definitif(s):
                continue
            cur_sp = _current_def2_target_public(state, s)
            if cur_sp is None or cur_sp[0] not in ("FURTIVITE", "LISIERE"):
                continue
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            is_orphan = False
            if cur_sp[0] == "FURTIVITE":
                _, ray_o, rv_o = cur_sp
                is_orphan = obs_s.furtivite_ray_rive_defs(int(ray_o), int(rv_o)) == 1
            elif cur_sp[0] == "LISIERE" and obs_s.mode >= 2:
                _, sl_o = cur_sp
                _, st_lo, nb_co = obs_s.lisiere_tile_info(int(sl_o))
                is_orphan = st_lo == LISIERE_UNCONSTRUCTED and nb_co == 1
            if not is_orphan:
                continue

            def _is_viable_fallback(cand_t: tuple[Any, ...], o_ref: PlayerObservation) -> bool:
                ck = cand_t[0]
                if ck == "GARDIEN_PARI":
                    return False
                if ck == "FURTIVITE":
                    return o_ref.furtivite_ray_rive_defs(int(cand_t[1]), int(cand_t[2])) == 1
                if ck == "LISIERE":
                    if o_ref.mode < 2:
                        return False
                    _, st_c, nb_cc = o_ref.lisiere_tile_info(int(cand_t[1]))
                    return st_c == LISIERE_UNCONSTRUCTED and nb_cc == 1
                return True

            legal_viable = _filter_legal_targets(
                tuple(
                    t
                    for t in list_legal_targets(
                        state, s, is_first_defender=False, exclude_own_def2=True
                    )
                    if _is_viable_fallback(t, obs_s)
                ),
                target_filter,
                is_first_defender=False,
                fallback_if_empty=False,
            )
            if legal_viable:
                bel_s = build_belief_summary(obs_s, cfg)
                cur_sc_o = _score_held_spot(obs_s, cfg, bel_s, cur_sp, scorer)
                fallback_t, fallback_sc = _pick_best_target_isolated(
                    obs_s,
                    cfg,
                    bel_s,
                    legal_viable,
                    scorer,
                    is_first_defender=False,
                    sous_etape_salt=253,
                )
                if fallback_sc - cur_sc_o > epsilon_base:
                    if on_decision is not None:
                        on_decision(
                            state,
                            DecisionRequest(
                                s,
                                DEC_POSE_DEFENSEUR_2,
                                tuple(("DEPLACER_REFLEXION", t) for t in legal_viable),
                                {"tour": state.tour, "step": "2.2", "phase": "retreat_orphan"},
                            ),
                            ("DEPLACER_REFLEXION", fallback_t),
                        )
                    moved = apply_step2_def2(
                        state,
                        s,
                        ("DEPLACER_REFLEXION", fallback_t),
                        check_legal=False,
                        telemetry=telemetry,
                    )
                    if moved:
                        _apply_step2_tick_accessories(
                            state, s, fallback_t, obs_s, bel_s, on_decision=on_decision
                        )
                        total_rev_moves += 1

    if post_revision_hook is not None and max_passes > 0:
        total_rev_moves += int(post_revision_hook(state))

    finish_step2_to_3_1(state, telemetry=telemetry)
    return {"passes_executed": passes_done, "revision_moves": total_rev_moves}


def _score_held_spot(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    cur_spot: tuple[Any, ...],
    scorer: TargetScorer,
) -> float:
    """Évalue la valeur marginale du poste déjà occupé par le 2e Défenseur du joueur."""
    if isinstance(scorer, HeldAwareScorer):
        return scorer.held_score(obs, cfg, belief, cur_spot)
    kind = cur_spot[0]
    base = scorer(obs, cfg, belief, cur_spot, False)
    # Correction d'auto-occupation : dans `obs`, notre propre 2e Défenseur est déjà compté sur cur_spot !
    if kind == "GARDIEN_PARI":
        tot_on_track = obs.total_gardien_pari_defenders()
        if obs.tour <= 7 and tot_on_track >= obs.n_players:
            # Tous les N 2es Défenseurs sont sur la piste -> fort bonus de maintien pour verrouiller l'Éveil !
            return base + 420.0
        if obs.tour <= 7 and tot_on_track >= 2:
            return base + 55.0
        return base - 90.0
    if kind == "REVE_ACTIVATION":
        _, case_c = cur_spot
        c_i = int(case_c)
        own_hand = obs.hand_of(obs.observer_seat)
        own_hits = (
            own_hand.card is not None
            and 1 <= own_hand.card <= 2 * obs.n_players
            and own_hand.lecture_m == c_i
            and obs.player_def1_reve_case(obs.observer_seat) != c_i
        )
        return base + (180.0 if own_hits else -120.0)
    if kind == "LISIERE":
        _, slot_idx = cur_spot
        _, st_l, nb_c = obs.lisiere_tile_info(int(slot_idx))
        if st_l == LISIERE_UNCONSTRUCTED and nb_c == 2:
            # Notre pion complète actuellement le 2/2 obligatoire -> valeur haute de complétion !
            return base + 420.0
        if st_l == LISIERE_UNCONSTRUCTED and nb_c == 1:
            # Nous sommes seuls dessus (personne ne nous a rejoint) -> faible valeur de maintien !
            return base - 260.0
    elif kind == "FURTIVITE":
        _, ray_i, rv = cur_spot
        d_rv = obs.furtivite_ray_rive_defs(int(ray_i), int(rv))
        if d_rv == 2:
            return base + 310.0
        return base - 210.0
    elif kind == "FORET":
        _, r, p = cur_spot
        r_i, p_i = int(r), int(p)
        defs = obs.parcel_defenseurs(r_i, p_i)
        tot_def = defs + obs.parcel_insectes(r_i, p_i)
        idx = r_i * MAX_P + (p_i - 1)
        seuil_e = belief.parcel_expected_seuil[idx]
        s_prob = belief.parcel_strike_prob[idx]
        if obs.mode >= 2 and obs.parcel_has_nid(r_i, p_i) and defs == 1:
            return base + 350.0
        if s_prob > 0.15 and (tot_def - 1) < seuil_e <= tot_def:
            return base + 360.0 * min(1.5, s_prob)
        if tot_def - 1 >= seuil_e:
            # Sur-défense redondante : quitter ce poste ne fait pas tomber la parade !
            return base - 190.0
    return base


def resolve_step2_full_with_ticks(
    state: GameState,
    scorer: TargetScorer,
    *,
    k_max_passes: int | None = None,
    epsilon_base: float = 28.0,
    epsilon_step: float = 12.0,
    counterfactual_open_paravents: bool = False,
    target_filter: TargetFilter | None = None,
    post_revision_hook: Callable[[GameState], int] | None = None,
    telemetry: Any | None = None,
    on_decision: DecisionCallback | None = None,
) -> dict[str, int]:
    """Résout intégralement l'Étape 2 (2.1 en Ticks 1..3 puis 2.2 en Ticks 1..3 + révision)."""
    cfg = state.cfg
    n = cfg.n_players
    clear_step2_pending_wait(state)

    if state.step == STEP_2_1_DEF1:
        rem_1 = [s for s in range(n) if state.get_player_def_loc_raw(s, 0) == 0]
        for current_tick in (1, 2, 3):
            if not rem_1:
                break
            tick_items: list[tuple[int, int, float]] = []
            for s in rem_1:
                obs_s = _get_isolated_obs(
                    state, s, counterfactual_open_paravents=counterfactual_open_paravents
                )
                bel_s = build_belief_summary(obs_s, cfg)
                t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=True)
                if t_s <= current_tick or current_tick == 3:
                    tick_items.append((s, current_tick, u_s))

            ordered_1 = order_seats_by_tick_and_urgency(
                tick_items, cfg, state.tour, 210 + current_tick
            )
            for s in ordered_1:
                obs_s = _get_isolated_obs(
                    state, s, counterfactual_open_paravents=counterfactual_open_paravents
                )
                bel_s = build_belief_summary(obs_s, cfg)
                legal_1 = _filter_legal_targets(
                    list_legal_targets(state, s, is_first_defender=True),
                    target_filter,
                    is_first_defender=True,
                    fallback_if_empty=True,
                )
                if not legal_1:
                    if on_decision is not None:
                        on_decision(
                            state,
                            DecisionRequest(
                                s,
                                DEC_POSE_DEFENSEUR_1,
                                (("PASSER_IMPASSE",),),
                                {"tour": state.tour, "step": "2.1"},
                            ),
                            ("PASSER_IMPASSE",),
                        )
                    apply_step2_def1(
                        state, s, ("PASSER_IMPASSE",), check_legal=False, telemetry=telemetry
                    )
                else:
                    t_best, _ = _pick_best_target_isolated(
                        obs_s,
                        cfg,
                        bel_s,
                        legal_1,
                        scorer,
                        is_first_defender=True,
                        sous_etape_salt=210 + current_tick,
                    )
                    if on_decision is not None:
                        if (
                            cfg.accessories_enabled
                            and cfg.peuples[s] == "H"
                            and state.get_humain_chaman_archetype(0) == CHAMAN_NONE
                        ):
                            inferred_ch = (
                                CHAMAN_TAMBOUR
                                if (t_best[0] == "FORET" and int(t_best[1]) != s)
                                else (
                                    CHAMAN_CHANT
                                    if t_best[0] == "REVE_ACTIVATION"
                                    else CHAMAN_TAMBOUR
                                )
                            )
                            on_decision(
                                state,
                                DecisionRequest(
                                    s,
                                    DEC_HUMAIN_CHAMAN_2_1,
                                    (CHAMAN_TAMBOUR, CHAMAN_CHANT),
                                    {"tour": state.tour, "step": "2.1"},
                                ),
                                inferred_ch,
                            )
                        on_decision(
                            state,
                            DecisionRequest(
                                s,
                                DEC_POSE_DEFENSEUR_1,
                                legal_1,
                                {"tour": state.tour, "step": "2.1"},
                            ),
                            t_best,
                        )
                    apply_step2_def1(state, s, t_best, check_legal=False, telemetry=telemetry)
                    _apply_step2_tick_accessories(
                        state, s, t_best, obs_s, bel_s, on_decision=on_decision
                    )
                rem_1.remove(s)
        advance_step2_to_2_2(state, telemetry=telemetry)

    if state.step == STEP_2_2_DEF2:
        return resolve_step2_2_from_state(
            state,
            scorer,
            k_max_passes=k_max_passes,
            epsilon_base=epsilon_base,
            epsilon_step=epsilon_step,
            counterfactual_open_paravents=counterfactual_open_paravents,
            target_filter=target_filter,
            post_revision_hook=post_revision_hook,
            telemetry=telemetry,
            on_decision=on_decision,
        )
    return {"passes_executed": 0, "revision_moves": 0}
