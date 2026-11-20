"""Croyance bayésienne isolée, Ticks discrets 1..3 et révision muette 2.2 (stdlib PyPy 3.11)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from engine.core_engine import (
    advance_step2_to_2_2,
    apply_step2_def1,
    apply_step2_def2,
    clear_step2_pending_wait,
    finish_step2_to_3_1,
    list_legal_targets,
)
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CARD_SABOTAGE,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    NUM_PARCELS,
    PIEGE_ACTIF,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameConfig,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_code,
    machine_card_code,
    unpack_machine_card,
)

__all__ = (
    "BeliefSummary",
    "TargetScorer",
    "build_belief_summary",
    "compute_private_urgency",
    "order_seats_by_tick_and_urgency",
    "resolve_step2_2_from_state",
    "resolve_step2_full_with_ticks",
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


def _next_non_razed_obs(obs: PlayerObservation, p_max: int, r: int, from_p: int) -> int | None:
    for p_cand in range(from_p + 1, p_max + 1):
        if not obs.is_route(r, p_cand):
            return p_cand
    return None


def _machine_effective_tokens_obs(
    machines: tuple[Any, ...], cfg: GameConfig, r: int, m_type: int
) -> tuple[int, int]:
    m_self = machines[r * 2 + m_type]
    rouges = m_self.rouges + (1 if m_self.status == MACHINE_STATUS_RATISSAGE else 0)
    bleus = m_self.bleus
    if cfg.synergie_binome_machines == "MUTUALISATION_PUISSANCE_MEME_PARCELLE":
        other = machines[r * 2 + (1 - m_type)]
        if (
            m_self.status != MACHINE_STATUS_RETIRED
            and other.status != MACHINE_STATUS_RETIRED
            and m_self.position > 0
            and m_self.position == other.position
        ):
            rouges += other.rouges + (1 if other.status == MACHINE_STATUS_RATISSAGE else 0)
            bleus += other.bleus
    return rouges, bleus


def build_belief_summary(obs: PlayerObservation, cfg: GameConfig) -> BeliefSummary:
    """Infère la carte bayésienne des menaces et signaux uniquement depuis `obs`."""
    n = obs.n_players
    p_max = cfg.p_max
    own_seat = obs.observer_seat
    own_hand = obs.hand_of(own_seat)
    machines = obs.machines

    drew_sab = (not own_hand.has_card) or (own_hand.card == CARD_SABOTAGE)
    own_cancelled = False

    strike_prob = [0.0] * NUM_PARCELS
    seuil_sum = [0.0] * NUM_PARCELS
    seuil_w = [0.0] * NUM_PARCELS
    bulldo_prob = [0.0] * NUM_PARCELS
    reve_prob = [0.0] * TRACK_LEN

    # Signaux coopératifs déjà visibles publiquement sur le plateau (Lisières à 1 bâtisseur, Furtivité à 1 pion)
    lis_signals = 0
    if obs.mode >= 2:
        for slot_idx in range(2 * n):
            _, st_l, nb_c = obs.lisiere_tile_info(slot_idx)
            if st_l == LISIERE_UNCONSTRUCTED and nb_c == 1:
                lis_signals += 1

    furt_signals = 0
    for l_idx in range(n):
        for p in range(1, p_max + 1):
            nb_d, f_ins = obs.furtivite_defs_and_ins(l_idx, p)
            if nb_d == 1 and f_ins == 0:
                furt_signals += 1

    def _add_strike(
        r: int, m_type: int, target_p: int, mod_seuil: int, prob: float
    ) -> None:
        if prob <= 0.0 or obs.is_route(r, target_p):
            return
        idx = r * MAX_P + (target_p - 1)
        rouges, bleus = _machine_effective_tokens_obs(machines, cfg, r, m_type)
        base_s = cfg.dotation_arbres[target_p - 1] + cfg.offset_seuil_parade
        s_eff = float(max(1, base_s + rouges - bleus + mod_seuil))
        strike_prob[idx] = min(2.5, strike_prob[idx] + prob)
        seuil_sum[idx] += prob * s_eff
        seuil_w[idx] += prob
        if m_type == MACHINE_BULLDOZER:
            bulldo_prob[idx] = min(1.0, bulldo_prob[idx] + prob)

    # 1. Machines en Ratissage : certitude publique (prob = 1.0, profil T1 : SUR_PLACE, +1 rouge imprimé, mod_seuil = 0)
    normal_deck_machines: list[tuple[int, int, int]] = []
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            if st == MACHINE_STATUS_RATISSAGE:
                _add_strike(r, mt, pos, 0, 1.0)
            elif st == MACHINE_STATUS_NORMAL:
                normal_deck_machines.append((machine_card_code(r, mt), r, mt))

    # 2. Mains connues (uniquement own_seat si paravents_ouverts == False ; toutes si paravents ouverts)
    known_machine_cards: set[int] = set()
    known_sabotages = 0
    unknown_holders = 0

    for s in range(n):
        h = obs.hand_of(s)
        if not h.has_card:
            continue
        if h.card is None:
            unknown_holders += 1
            continue
        if h.card == CARD_SABOTAGE:
            known_sabotages += 1
            continue
        if 1 <= h.card <= 2 * n:
            known_machine_cards.add(h.card)
            r_m, mt_m = unpack_machine_card(h.card)
            pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
            lec = h.lecture_m
            if st_m == MACHINE_STATUS_NORMAL and pos_m > 0 and lec is not None and 1 <= lec <= 6:
                t_code, _, _ = obs.tactique_code_bugs_app(lec - 1)
                if is_reve_code(t_code):
                    reve_prob[lec - 1] = 1.0
                    n_def_r = obs.reve_activation_defenders(lec)
                    act_mode = cfg.reve_activation_mode
                    is_cancelled = (
                        (act_mode == "1_DEF_ALL_RANK" and n_def_r >= 1)
                        or (act_mode == "BINOME_ALL_RANK" and n_def_r >= 2)
                        or (
                            act_mode == "1_DEF_1_MACHINE"
                            and (
                                (s == own_seat and obs.player_def2_reve_case(own_seat) == lec)
                                or (s != own_seat and n_def_r >= 1)
                            )
                        )
                    )
                    if is_cancelled:
                        if s == own_seat:
                            own_cancelled = True
                        continue
                    # Rêve inactif : la Tactique imprimée T{lec} menace toujours la parcelle
                    t_code = lec
                if is_tactique_code(t_code):
                    spec = TACTIQUES_SPEC[t_code]
                    for c_kind in spec.cibles:
                        if c_kind == "SUR_PLACE":
                            _add_strike(r_m, mt_m, pos_m, spec.mod_seuil, 1.0)
                        elif c_kind == "DEVANT":
                            p_dev = _next_non_razed_obs(obs, p_max, r_m, pos_m)
                            if p_dev is not None:
                                _add_strike(r_m, mt_m, p_dev, spec.mod_seuil, 1.0)

    # 3. Inférence bayésienne sur les mains adverses masquées sous paravent
    if unknown_holders == 0:
        p_sab_post = 0.0
    else:
        unseen_machines = [item for item in normal_deck_machines if item[0] not in known_machine_cards]
        m_rem = len(unseen_machines)
        sab_rem = max(0, obs.sabotage_deck_count - known_sabotages)
        denom = max(1, m_rem + sab_rem)
        p_sab_prior = sab_rem / denom

        # Mise à jour bayésienne légère par les signaux coopératifs observés en lisière/furtivité :
        # les joueurs Sabotage émettent préférentiellement sur G/R/M et Furtivité dès le Tick 1.
        coop_evidence = min(3, lis_signals + furt_signals)
        if p_sab_prior > 0.0 and coop_evidence > 0:
            lr = 1.0 + 0.28 * coop_evidence
            odds = (p_sab_prior / max(1e-6, 1.0 - p_sab_prior)) * lr
            p_sab_post = odds / (1.0 + odds)
        else:
            p_sab_post = p_sab_prior

        expected_active_draws = unknown_holders * (1.0 - p_sab_post)
        if m_rem > 0 and expected_active_draws > 0.0:
            # Pondération bayésienne par présence de Défenseurs déjà posés en forêt par les voisins
            weights: list[float] = []
            w_total = 0.0
            for _, r_u, mt_u in unseen_machines:
                pos_u, _ = obs.machine_pos_status(r_u, mt_u)
                defs_near = obs.parcel_defenseurs(r_u, pos_u) if pos_u > 0 else 0
                p_dev_u = _next_non_razed_obs(obs, p_max, r_u, pos_u) if pos_u > 0 else None
                if p_dev_u is not None:
                    defs_near += obs.parcel_defenseurs(r_u, p_dev_u)
                # Vraisemblance bayésienne : une défense posée sur le rayon augmente la probabilité que la carte circule
                w_m = 1.0 + 0.35 * min(2, defs_near)
                weights.append(w_m)
                w_total += w_m

            for idx_u, (_, r_u, mt_u) in enumerate(unseen_machines):
                p_card_drawn = min(0.95, expected_active_draws * (weights[idx_u] / max(1e-6, w_total)))
                pos_u, _ = obs.machine_pos_status(r_u, mt_u)
                if pos_u <= 0:
                    continue
                for rank_idx in range(TRACK_LEN):
                    p_m_val = _MIN_2D6_PROBS[rank_idx]
                    p_joint = p_card_drawn * p_m_val
                    t_code, _, _ = obs.tactique_code_bugs_app(rank_idx)
                    if is_reve_code(t_code):
                        reve_prob[rank_idx] = 1.0 - (1.0 - reve_prob[rank_idx]) * (1.0 - p_joint)
                    elif is_tactique_code(t_code):
                        spec = TACTIQUES_SPEC[t_code]
                        for c_kind in spec.cibles:
                            if c_kind == "SUR_PLACE":
                                _add_strike(r_u, mt_u, pos_u, spec.mod_seuil, p_joint)
                            elif c_kind == "DEVANT":
                                p_dev = _next_non_razed_obs(obs, p_max, r_u, pos_u)
                                if p_dev is not None:
                                    _add_strike(r_u, mt_u, p_dev, spec.mod_seuil, p_joint)

    expected_seuil: list[float] = []
    for r in range(n):
        for p in range(1, MAX_P + 1):
            idx = r * MAX_P + (p - 1)
            if p <= p_max and seuil_w[idx] > 1e-6:
                expected_seuil.append(seuil_sum[idx] / seuil_w[idx])
            elif p <= p_max:
                expected_seuil.append(float(max(1, cfg.dotation_arbres[p - 1] + cfg.offset_seuil_parade)))
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
      naturel sur tuile G/R/M ou Furtivité), ou urgence vitale immédiate sur son rayon.
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

    # 2. Carte Machine annulée par un Rêve en 3.2 : faible urgence privée -> attend Tick 3 (ou Tick 2 si signal ouvert)
    if bel.own_machine_cancelled_by_reve:
        if bel.coop_lisiere_signals > 0 or bel.coop_furtivite_signals > 0:
            return 2, 0.56
        return 3, 0.28

    # 3. Joueur détenant une carte Machine active
    u_val = 0.35
    if own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players:
        r_m, mt_m = unpack_machine_card(own_hand.card)
        pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
        lec = own_hand.lecture_m
        if st_m == MACHINE_STATUS_NORMAL and pos_m > 0 and lec is not None and 1 <= lec <= 6:
            t_code, _, _ = obs.tactique_code_bugs_app(lec - 1)
            if is_tactique_code(t_code):
                spec = TACTIQUES_SPEC[t_code]
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
                    piege_armed = obs.parcel_piege(r_m, tp) == PIEGE_ACTIF and cur_def >= 1
                    if not piege_armed and cur_def < seuil_est:
                        # Menace directe non parée
                        own_ray_access = (not is_first_defender) or (r_m == own_seat)
                        arbres = obs.parcel_arbres(r_m, tp)
                        danger = 0.62 if own_ray_access else 0.50
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
        return ("FURTIVITE", a, b, c // 2)
    if kind == "LISIERE":
        return ("LISIERE", a)
    if kind == "GARDIEN_PARI":
        return ("GARDIEN_PARI", a)
    if kind == "REVE_ACTIVATION":
        return ("REVE_ACTIVATION", a)
    return None


def resolve_step2_2_from_state(
    state: GameState,
    scorer: TargetScorer,
    *,
    k_max_passes: int | None = None,
    epsilon_base: float = 28.0,
    epsilon_step: float = 12.0,
    counterfactual_open_paravents: bool = False,
    telemetry: Any | None = None,
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
            legal_2 = list_legal_targets(state, s, is_first_defender=False)
            if not legal_2:
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
                apply_step2_def2(
                    state, s, (act_kind, target_2), check_legal=False, telemetry=telemetry
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
            legal_alt = tuple(
                t
                for t in list_legal_targets(
                    state, s, is_first_defender=False, exclude_own_def2=True
                )
                if t != cur_spot
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
                moved = apply_step2_def2(
                    state,
                    s,
                    ("DEPLACER_REFLEXION", best_alt),
                    check_legal=False,
                    telemetry=telemetry,
                )
                if moved:
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
    #     en Mode 2 (Gardiens neutres), si l'équipe n'a pas réuni les N 2es Défenseurs sur la piste
    #     (ou si on est au Tour 8), un pari isolé risque de renvoyer un Gardien en lisière sans gain :
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
            g_tot = obs_s.total_gardien_pari_defenders()
            eveil_valid = obs_s.tour < 8 and g_tot == n
            if cfg.mode == 2 and not eveil_valid:
                # En Mode 2 neutre, parier n'a de sens que pour l'Éveil 100 % Gardiens (Tours 1..7)
                need_gard_retreat = True
            if pari_c == 4:
                res_bets = obs_s.gardien_pari_defenders(4)
                distinct_other_cases = sum(
                    1
                    for ck in (1, 2, 3, 5, 6)
                    if obs_s.gardien_present_at_case(ck)
                    and obs_s.gardien_pari_defenders(ck) >= 1
                )
                col4 = (
                    1
                    if (
                        cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "A"
                        and obs_s.piste_colonie[3] >= 1
                    )
                    else 0
                )
                if cfg.gardien_4_trigger_mode == "DISTINCT_WON_2":
                    max_case4_trigs = max(0, distinct_other_cases - 1) + col4
                else:  # "DISTINCT_OPEN_1"
                    max_case4_trigs = distinct_other_cases + col4
                if max_case4_trigs < res_bets:
                    # Impossible d'allumer 4. Gardien assez de fois pour consommer tous les paris dessus !
                    need_gard_retreat = True
            if need_gard_retreat:
                legal_non_pari = tuple(
                    t
                    for t in list_legal_targets(
                        state, s, is_first_defender=False, exclude_own_def2=True
                    )
                    if t[0] != "GARDIEN_PARI"
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
                    moved = apply_step2_def2(
                        state,
                        s,
                        ("DEPLACER_REFLEXION", fallback_t),
                        check_legal=False,
                        telemetry=telemetry,
                    )
                    if moved:
                        total_rev_moves += 1

    # 3b. Retrait propre en fin de passes « en réflexion » pour l'activation des Rêves :
    #     - en BINOME_ALL_RANK : si un Rêve n'a pas atteint 2 Défenseurs, le Défenseur isolé se replie ;
    #     - en 1_DEF_ALL_RANK : si >= 2 Défenseurs sont empilés sur le même Rêve, le surnuméraire se replie.
    if max_passes > 0 and cfg.mode >= 2 and cfg.reve_activation_mode in (
        "BINOME_ALL_RANK",
        "1_DEF_ALL_RANK",
    ):
        for s in range(n):
            if state.get_player_def_loc_raw(s, 1) == 0 or state.is_player_def2_definitif(s):
                continue
            obs_s = _get_isolated_obs(
                state, s, counterfactual_open_paravents=counterfactual_open_paravents
            )
            rc = obs_s.player_def2_reve_case(s)
            if rc <= 0:
                continue
            cnt_rc = obs_s.reve_activation_defenders(rc)
            need_retreat = (
                (cfg.reve_activation_mode == "BINOME_ALL_RANK" and cnt_rc < 2)
                or (cfg.reve_activation_mode == "1_DEF_ALL_RANK" and cnt_rc >= 2)
            )
            if need_retreat:
                legal_alt = tuple(
                    t
                    for t in list_legal_targets(
                        state, s, is_first_defender=False, exclude_own_def2=True
                    )
                    if t[0] != "REVE_ACTIVATION" and t[0] != "GARDIEN_PARI"
                )
                if legal_alt:
                    bel_s = build_belief_summary(obs_s, cfg)
                    fallback_t, _ = _pick_best_target_isolated(
                        obs_s,
                        cfg,
                        bel_s,
                        legal_alt,
                        scorer,
                        is_first_defender=False,
                        sous_etape_salt=251,
                    )
                    moved = apply_step2_def2(
                        state,
                        s,
                        ("DEPLACER_REFLEXION", fallback_t),
                        check_legal=False,
                        telemetry=telemetry,
                    )
                    if moved:
                        total_rev_moves += 1

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
        cnt = obs.reve_activation_defenders(c_i)
        own_hand = obs.hand_of(obs.observer_seat)
        own_hits = (
            own_hand.card is not None and 1 <= own_hand.card <= 12 and own_hand.lecture_m == c_i
        )
        act_mode = cfg.reve_activation_mode
        if act_mode == "1_DEF_1_MACHINE":
            return base + (180.0 if own_hits else -120.0)
        if act_mode == "1_DEF_ALL_RANK":
            if cnt == 1 and own_hits:
                return base + 260.0
            if cnt >= 2:
                return base - 220.0
            return base - 80.0
        # BINOME_ALL_RANK
        if cnt == 2:
            return base + 380.0
        if cnt > 2:
            return base - 220.0
        return base - 60.0
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
        _, l_idx, p, _ = cur_spot
        nb_d, f_ins = obs.furtivite_defs_and_ins(int(l_idx), int(p))
        if nb_d == 2 or (nb_d == 1 and f_ins >= 1):
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
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and tot_def == 1:
            return base + 380.0
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
    telemetry: Any | None = None,
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
                legal_1 = list_legal_targets(state, s, is_first_defender=True)
                if not legal_1:
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
                    apply_step2_def1(state, s, t_best, check_legal=False, telemetry=telemetry)
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
            telemetry=telemetry,
        )
    return {"passes_executed": 0, "revision_moves": 0}
