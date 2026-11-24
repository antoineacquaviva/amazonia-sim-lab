"""Déroulements courts CRN (1 tour) pour Gardiens/Rêves de B2 et déterminisation exacte (B2/B3).

100 % stdlib PyPy 3.11 / CPython 3.12, zéro dépendance tierce, zéro accès `_buf`.
Fournit :
1. `determinize_state_from_obs` : déterminisation à conservation exacte des cartes
   (Machines normales + Sabotages en main + pioche restante), pondérée par les signaux publics
   du plateau (sans double-comptage des pions de l'observateur) et strictement étanche.
2. `evaluate_gardien_reve_candidates_crn` & `arbitrate_step2_gardien_reve_crn` :
   évaluation par déroulements courts CRN (8 à 16 mondes partagés) en équivalent-arbres
   pour arbitrer les paris Gardiens et activations de Rêves face à la meilleure alternative.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import replace
from typing import Any

from bots.b2_economy import estimate_expected_gardien_triggers
from bots.belief_and_ticks import TargetFilter, build_belief_summary
from engine.core_engine import (
    apply_choice,
    apply_step2_def2,
    finish_step2_to_3_1,
    list_legal_targets,
    step_until_decision,
)
from engine.primitives import DecisionRequest, GameOver
from engine.rng import SRC_DICE, rand_u64, roll_d6
from engine.state import (
    CARD_ECAILLE,
    CARD_NONE,
    CARD_SABOTAGE,
    LISIERE_CONSTRUCTED,
    LISIERE_ROOTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    TRACK_LEN,
    TRIG_RESONANCE,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_code,
    machine_card_code,
    unpack_machine_card,
)

__all__ = (
    "arbitrate_step2_gardien_reve_crn",
    "determinize_state_from_obs",
    "evaluate_gardien_reve_candidates_crn",
    "evaluate_turn_state_trees",
    "rollout_end_of_turn_trees",
)

_SRC_DETERMINIZE: int = 41
_U64_DIVISOR: float = float((1 << 64) + 1)


def _next_non_razed_obs_r(obs: PlayerObservation, p_max: int, ray: int, from_p: int) -> int | None:
    for p_c in range(from_p + 1, p_max + 1):
        if not obs.is_route(ray, p_c):
            return p_c
    return None


def determinize_state_from_obs(
    template_state: GameState,
    obs: PlayerObservation,
    det_idx: int = 0,
) -> GameState:
    """Construit un monde déterminisé cohérent avec `obs` à conservation exacte des cartes.

    Garanties :
    - Isolation stricte : deux états `s1`, `s2` produisant la même `PlayerObservation`
      engendrent des octets `raw_used_bytes()` strictement identiques (y compris Perchoir O & Dé d'Envol).
    - Conservation exacte du multi-ensemble total (Machines normales + Sabotages + Écailles) :
      toutes les mains connues et le Perchoir connu de O sont soustraits, les mains inconnues
      et le Perchoir masqué sont tirés sans remise, et le reliquat exact compose le sac restant.
    """
    cfg = template_state.cfg
    seat = obs.observer_seat
    n = obs.n_players
    p_max = cfg.p_max

    salt = ((obs.step & 0xFF) << 16) | ((seat & 0x0F) << 8) | (det_idx & 0xFF)
    det_seed = int(
        rand_u64(cfg.exp_seed, cfg.rep_id, _SRC_DETERMINIZE, obs.tour, seat, salt) & 0x7FFFFFFF
    )
    det_rep = int(
        rand_u64(cfg.exp_seed, cfg.rep_id, _SRC_DETERMINIZE, obs.tour, seat + 8, salt) & 0x3FFFFFFF
    )

    det = template_state.clone()
    det.cfg = replace(cfg, exp_seed=det_seed, rep_id=det_rep)

    # 1. Multi-ensemble exact de toutes les cartes du cycle courant (Machines normales + Sabotages + Écailles)
    remaining_pool: list[int] = []
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            _, st = obs.machine_pos_status(r, mt)
            if st == MACHINE_STATUS_NORMAL:
                remaining_pool.append(machine_card_code(r, mt))
    remaining_pool.extend([CARD_SABOTAGE] * obs.sabotage_deck_count)
    remaining_pool.extend([CARD_ECAILLE] * obs.ecaille_deck_count)

    # 2. Soustraire toutes les mains connues et le Perchoir visible de O, et lister les sièges masqués
    unknown_seats: list[int] = []
    for s in range(n):
        h = obs.hand_of(s)
        if not h.has_card:
            if not obs.paravents_ouverts and s != seat:
                det.set_player_hand(s, CARD_NONE, 0, 0, 0, 0)
            continue
        if h.card is None:
            unknown_seats.append(s)
            continue
        if h.card in remaining_pool:
            remaining_pool.remove(h.card)

    det_perchoir_card: int = CARD_NONE
    need_sample_perchoir = False
    if obs.oiseau_has_perchoir:
        known_p = obs.oiseau_perchoir_card
        if known_p is not None and known_p != CARD_NONE:
            det_perchoir_card = int(known_p)
            if det_perchoir_card in remaining_pool:
                remaining_pool.remove(det_perchoir_card)
        else:
            need_sample_perchoir = True

    # 3. Échantillonner sans remise les mains inconnues (et le Perchoir masqué) avec pondération alliée
    need_sampling = (not obs.paravents_ouverts and bool(unknown_seats)) or need_sample_perchoir
    if need_sampling and remaining_pool:
        own_f1 = obs.player_def1_furtivite_target(seat)
        own_f2 = obs.player_def2_furtivite_target(seat)
        own_l1 = obs.player_def1_lisiere_slot(seat)
        own_l2 = obs.player_def2_lisiere_slot(seat)

        ally_lis_sig = 0
        if obs.mode >= 2:
            for s_idx in range(2 * n):
                _, st_l, cnt_l = obs.lisiere_tile_info(s_idx)
                own_on_l = (1 if own_l1 == s_idx else 0) + (1 if own_l2 == s_idx else 0)
                if st_l == 1 and cnt_l == 1 and own_on_l == 0:
                    ally_lis_sig += 1

        ally_furt_sab_sig = 0
        for r_i in range(n):
            own_on_s = (1 if own_f1 == (r_i, 1) else 0) + (1 if own_f2 == (r_i, 1) else 0)
            if obs.furtivite_ray_rive_defs(r_i, 1) == 1 and own_on_s == 0:
                ally_furt_sab_sig += 1

        sab_weight = 1.0 + 0.28 * min(3, ally_lis_sig + ally_furt_sab_sig)

        # Clés A-Res (Efraimidis-Spirakis) déterministes pour tirage pondéré sans remise
        keyed_pool: list[tuple[float, int, int]] = []
        for idx_p, c_code in enumerate(remaining_pool):
            if c_code in (CARD_SABOTAGE, CARD_ECAILLE):
                w = sab_weight
            else:
                r_u, mt_u = unpack_machine_card(c_code)
                pos_u, _ = obs.machine_pos_status(r_u, mt_u)
                defs_near = obs.parcel_defenseurs(r_u, pos_u) if pos_u > 0 else 0
                p_dev_u = _next_non_razed_obs_r(obs, p_max, r_u, pos_u) if pos_u > 0 else None
                if p_dev_u is not None:
                    defs_near += obs.parcel_defenseurs(r_u, p_dev_u)
                own_on_p = (1 if own_f1 == (r_u, 0) else 0) + (1 if own_f2 == (r_u, 0) else 0)
                own_on_s = (1 if own_f1 == (r_u, 1) else 0) + (1 if own_f2 == (r_u, 1) else 0)
                ally_p = max(0, obs.furtivite_ray_rive_defs(r_u, 0) - own_on_p)
                ally_s = max(0, obs.furtivite_ray_rive_defs(r_u, 1) - own_on_s)
                w = 1.0 + 0.35 * min(2, defs_near) + 1.15 * min(1, ally_p)
                if ally_s >= 1 and ally_p == 0:
                    w = max(0.35, w - 0.25)
            u_raw = rand_u64(det_seed, det_rep, _SRC_DETERMINIZE, obs.tour, idx_p, det_idx + 1)
            u_01 = (float(u_raw) + 1.0) / _U64_DIVISOR
            exp_key = -math.log(u_01) / max(1e-6, w)
            keyed_pool.append((exp_key, idx_p, c_code))

        keyed_pool.sort()
        cursor_k = 0
        if not obs.paravents_ouverts and unknown_seats:
            for s in unknown_seats:
                if cursor_k >= len(keyed_pool):
                    det.set_player_hand(s, CARD_NONE, 0, 0, 0, 0)
                    continue
                c_draw = keyed_pool[cursor_k][2]
                cursor_k += 1
                d1 = roll_d6(det_seed, det_rep, SRC_DICE, obs.tour, s, det_idx * 2)
                d2 = roll_d6(det_seed, det_rep, SRC_DICE, obs.tour, s, det_idx * 2 + 1)
                if c_draw in (CARD_SABOTAGE, CARD_ECAILLE):
                    det.set_player_hand(s, c_draw, d1, d2, 0, 0)
                else:
                    lec_m = min(d1, d2)
                    t_code, _ = obs.tactique_code_bugs(lec_m - 1)
                    bound_t = t_code if is_tactique_code(t_code) else 0
                    det.set_player_hand(s, c_draw, d1, d2, lec_m, bound_t)
        if need_sample_perchoir and cursor_k < len(keyed_pool):
            det_perchoir_card = int(keyed_pool[cursor_k][2])
            cursor_k += 1

    # Masquage strict du Dé d'Envol de O lorsque paravents fermés et observateur != O
    seat_o = cfg.seat_of_peuple("O")
    if not obs.paravents_ouverts and seat_o is not None and seat != seat_o:
        det.set_oiseau_de_envol(0, False)

    # 4. Reconstruire la pioche restante exacte (Machines + Sabotages + Écailles hors mains et Perchoir)
    orig_sab_deck = obs.sabotage_deck_count
    orig_sab_pend = obs.sabotage_pending_count
    orig_ec_deck = obs.ecaille_deck_count
    orig_ec_pend = obs.ecaille_pending_count
    det.sabotage_deck_count = orig_sab_deck
    det.sabotage_pending_count = 0
    det.ecaille_deck_count = orig_ec_deck
    det.ecaille_pending_count = 0
    det.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    det.sabotage_pending_count = orig_sab_pend
    det.ecaille_pending_count = orig_ec_pend

    # Retirer du sac TOUTES les cartes tenues en main + le jeton posé sur le Perchoir de O
    for s in range(n):
        c_held, _, _, _, _ = det.get_player_hand(s)
        if c_held != CARD_NONE:
            det.remove_machine_card_from_deck_if_present(c_held)
    if det_perchoir_card != CARD_NONE:
        det.remove_machine_card_from_deck_if_present(det_perchoir_card)
    det.oiseau_perchoir_card = det_perchoir_card

    target_rem = obs.deck_remaining_count
    if det.deck_len > target_rem:
        det.deck_cursor = det.deck_len - target_rem
    else:
        det.deck_cursor = 0
    return det


def evaluate_turn_state_trees(state: GameState) -> float:
    """Évalue un état de fin de tour (non terminal) en espérance d'arbres finaux."""
    cfg = state.cfg
    n = cfg.n_players
    p_max = cfg.p_max
    cur_trees = float(state.total_arbres_plateau())
    rem_turns = max(0, 8 - state.tour)

    # Pertes futures attendues sur les tours restants + pression machines courante
    future_loss = 0.34 * float(n) * float(rem_turns)
    machine_pressure = 0.0
    assets = 0.0
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos <= 0:
                continue
            rouges = state.get_machine_effective_rouges(r, mt)
            _, bleus = state.get_machine_tokens(r, mt)
            net_red = max(0, rouges - bleus)
            machine_pressure += 0.25 * (pos / float(p_max)) + 0.30 * float(net_red)
            if st == MACHINE_STATUS_RATISSAGE:
                machine_pressure += 0.55
            if rem_turns > 0:
                if state.has_machine_alteration(r, mt):
                    assets += 0.90
                cale = state.get_machine_cale(r, mt)
                if cale == 2:
                    assets += 0.75
                elif cale == 1:
                    assets += 0.50

    # Actifs durables en équivalent-arbres
    sab_tot = min(
        6,
        state.sabotage_deck_count
        + state.sabotage_pending_count
        + state.ecaille_deck_count
        + state.ecaille_pending_count,
    )
    if sab_tot > 0 and rem_turns > 0:
        assets += 0.28 * float(min(4, rem_turns)) * float(sab_tot)
    if state.get_croc_parcel() is not None and rem_turns > 0:
        assets += 0.65
    if state.get_duel_state()[0] == 2 and rem_turns > 0:
        assets += 0.45

    for r in range(n):
        for p in range(1, p_max + 1):
            if state.is_route_forestiere(r, p):
                continue
            if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                assets += 0.65
            ins = state.get_parcel_insectes(r, p)
            if ins > 0:
                assets += 0.22 * float(min(3, ins))

    if cfg.mode >= 2:
        for slot_idx in range(2 * n):
            st_l, _ = state.get_lisiere_tile_state(slot_idx)
            if st_l == LISIERE_CONSTRUCTED:
                assets += 0.35
            elif st_l == LISIERE_ROOTED:
                rinfo = state.get_slot_rooted_info(slot_idx)
                if rinfo is not None:
                    r_rt, p_rt, f_rt, _ = rinfo
                    if p_rt > 0 and not state.is_route_forestiere(r_rt, p_rt):
                        souches_rt = state.get_parcel_souches(r_rt, p_rt)
                        tid_rt = cfg.lisiere_slots[slot_idx]
                        cap_rt = 2 if f_rt == 2 else 1
                        if tid_rt == "M5":
                            cap_rt += state.get_parcel_insectes(r_rt, p_rt)
                        assets += 0.85 * float(min(souches_rt, cap_rt))
                        if tid_rt == "R6":
                            for pn in (
                                state.next_non_razed_towards_border(r_rt, p_rt),
                                state.next_non_razed_towards_heart(r_rt, p_rt),
                            ):
                                if pn is not None and state.get_parcel_souches(r_rt, pn) >= 1:
                                    assets += 0.85
                                    break
        for rk in range(TRACK_LEN):
            if is_reve_code(state.get_tactique_at_rank(rk)):
                assets += 0.35 * float(TRACK_LEN - rk) / float(TRACK_LEN)
        if cfg.nb_animaux_sauvages >= 1:
            for c_num in range(1, TRACK_LEN + 1):
                g_num, g_face = state.get_gardien_at_case(c_num)
                if g_num > 0:
                    # En Mode 3/4, conserver un Gardien et le passer Face 2 ajoute une vraie valeur future
                    if cfg.mode >= 3:
                        assets += 0.55 if g_face == 2 else 0.25
                    else:
                        assets += 0.18

    return cur_trees + assets - future_loss - machine_pressure


def rollout_end_of_turn_trees(
    sim_state: GameState,
    chooser: Callable[[GameState, DecisionRequest], Any],
    *,
    max_steps: int = 800,
) -> float:
    """Déroule rapidement la fin du tour courant (`3.1 -> 5.3 -> 6.3` ou `GameOver`) en arbres."""
    start_tour = sim_state.tour
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            return evaluate_turn_state_trees(sim_state)
        out = step_until_decision(sim_state, max_internal_steps=max_steps)
        if isinstance(out, GameOver):
            return float(out.score_arbres)
        if sim_state.tour > start_tour and sim_state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2):
            return evaluate_turn_state_trees(sim_state)
        choice = chooser(sim_state, out)
        apply_choice(sim_state, choice)


def evaluate_gardien_reve_candidates_crn(
    state: GameState,
    obs: PlayerObservation,
    seat: int,
    baseline_target: tuple[Any, ...],
    candidate_targets: tuple[tuple[Any, ...], ...],
    *,
    chooser: Callable[[GameState, DecisionRequest], Any],
    n_rollouts: int = 8,
    max_steps: int = 800,
) -> dict[tuple[Any, ...], float]:
    """Compare en CRN (`n_rollouts` mondes partagés) chaque candidat Gardien/Rêve à `baseline_target`.

    Retourne un dictionnaire `{target: delta_arbres_moyen_vs_baseline}` (où `baseline` vaut `0.0`).
    """
    n_det = max(1, n_rollouts)
    if not candidate_targets:
        return {baseline_target: 0.0}

    det_worlds = [
        determinize_state_from_obs(state, obs, det_idx=20 + d_i) for d_i in range(n_det)
    ]

    def _eval_target(tgt: tuple[Any, ...]) -> float:
        acc = 0.0
        for dw in det_worlds:
            sim = dw.clone()
            apply_step2_def2(sim, seat, ("DEPLACER_REFLEXION", tgt), check_legal=False)
            finish_step2_to_3_1(sim)
            acc += rollout_end_of_turn_trees(sim, chooser, max_steps=max_steps)
        return acc / float(n_det)

    base_val = _eval_target(baseline_target)
    deltas: dict[tuple[Any, ...], float] = {baseline_target: 0.0}
    for cand in candidate_targets:
        if cand == baseline_target:
            deltas[cand] = 0.0
        else:
            deltas[cand] = _eval_target(cand) - base_val
    return deltas


def _current_def2_target_local(state: GameState, seat: int) -> tuple[Any, ...] | None:
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


def arbitrate_step2_gardien_reve_crn(
    state: GameState,
    *,
    chooser: Callable[[GameState, DecisionRequest], Any],
    target_filter: TargetFilter | None = None,
    counterfactual_open_paravents: bool = False,
    n_rollouts: int = 8,
    min_gain_trees: float = 0.10,
    max_candidates_per_seat: int = 1,
    telemetry: Any | None = None,
) -> int:
    """Passe d'arbitrage CRN en fin d'Étape 2.2 pour Gardiens (Mode >= 3) et Rêves.

    Évalue sur `n_rollouts` (8..16) déroulements CRN d'un tour si déplacer le 2e Défenseur
    sur un Gardien ou un Rêve améliore l'espérance d'arbres par rapport au poste courant.
    Respecte strictement `PlayerObservation` et `target_filter`.
    """
    cfg = state.cfg
    if n_rollouts <= 0 or cfg.mode < 3 or state.step != STEP_2_2_DEF2:
        return 0

    from bots.b2_economy import score_forest_marginal_trees

    n = cfg.n_players
    moves = 0

    for s in range(n):
        if state.get_player_def_loc_raw(s, 1) == 0 or state.is_player_def2_definitif(s):
            continue
        cur_spot = _current_def2_target_local(state, s)
        if cur_spot is None:
            continue

        if counterfactual_open_paravents and not state.paravents_ouverts:
            saved_p = state.paravents_ouverts
            state.paravents_ouverts = True
            try:
                obs_s = state.get_observation(s)
            finally:
                state.paravents_ouverts = saved_p
        else:
            obs_s = state.get_observation(s)

        bel_s = build_belief_summary(obs_s, cfg)

        # Éviter de défaire une parade Forêt critique (> 2.4 arbres directs) ou un binôme 2/2 complet
        if cur_spot[0] == "FORET":
            cur_f_trees = score_forest_marginal_trees(
                obs_s, cfg, bel_s, int(cur_spot[1]), int(cur_spot[2]), is_held=True
            )
            if cur_f_trees >= 2.45:
                continue
        elif cur_spot[0] == "LISIERE":
            _, st_l, cnt_l = obs_s.lisiere_tile_info(int(cur_spot[1]))
            if st_l == 0 and cnt_l == 2:
                continue
        elif cur_spot[0] == "FURTIVITE" and obs_s.furtivite_ray_rive_defs(int(cur_spot[1]), int(cur_spot[2])) == 2:
            continue

        legal_alts = list_legal_targets(state, s, is_first_defender=False, exclude_own_def2=True)
        if target_filter is not None:
            legal_alts = tuple(t for t in legal_alts if target_filter(t, False))

        # Sélectionner les candidats Gardiens / Rêves plausibles (trigger attendu >= 0.45)
        exp_trigs = estimate_expected_gardien_triggers(obs_s, cfg, bel_s, for_eveil=False)
        scored_gr: list[tuple[float, tuple[Any, ...]]] = []

        for tgt in legal_alts:
            if tgt == cur_spot:
                continue
            tk = tgt[0]
            if tk == "GARDIEN_PARI":
                c_num = int(tgt[1])
                own_c = obs_s.player_def2_gardien_pari_case(s)
                allies_c = max(0, obs_s.gardien_pari_defenders(c_num) - (1 if own_c == c_num else 0))
                if c_num == TRIG_RESONANCE:
                    exp_t = sum(
                        min(1.0, exp_trigs[k - 1])
                        for k in (1, 2, 3, 4, 5)
                        if obs_s.gardien_present_at_case(k)
                    )
                else:
                    exp_t = exp_trigs[c_num - 1]
                if exp_t >= float(allies_c) + 0.45:
                    g_face = obs_s.gardien_face_at_case(c_num)
                    prio = exp_t - float(allies_c) + (0.25 if g_face == 1 else 0.0)
                    scored_gr.append((prio, tgt))
            elif tk == "REVE_ACTIVATION":
                c_num = int(tgt[1])
                if bel_s.reve_open_prob_by_rank[c_num - 1] >= 0.40:
                    scored_gr.append((bel_s.reve_open_prob_by_rank[c_num - 1], tgt))

        scored_gr.sort(key=lambda x: (-x[0], x[1]))
        eval_list: list[tuple[Any, ...]] = [t for _, t in scored_gr[:max_candidates_per_seat]]

        # Si le poste courant est déjà un Gardien/Rêve, comparer symétriquement à la meilleure parcelle Forêt
        if cur_spot[0] in ("GARDIEN_PARI", "REVE_ACTIVATION"):
            best_f: tuple[Any, ...] | None = None
            best_f_sc = -1e9
            for tgt in legal_alts:
                if tgt[0] == "FORET":
                    sc_f = score_forest_marginal_trees(
                        obs_s, cfg, bel_s, int(tgt[1]), int(tgt[2]), is_held=False
                    )
                    if sc_f > best_f_sc:
                        best_f_sc = sc_f
                        best_f = tgt
            if best_f is not None and best_f not in eval_list:
                eval_list.append(best_f)

        if not eval_list:
            continue

        eval_cands = tuple(eval_list)
        deltas = evaluate_gardien_reve_candidates_crn(
            state,
            obs_s,
            s,
            cur_spot,
            eval_cands,
            chooser=chooser,
            n_rollouts=n_rollouts,
        )

        best_cand = cur_spot
        best_delta = 0.0
        for cand in eval_cands:
            d_val = deltas.get(cand, 0.0)
            if d_val > best_delta:
                best_delta = d_val
                best_cand = cand

        if (
            best_cand != cur_spot
            and best_delta >= min_gain_trees
            and apply_step2_def2(
                state, s, ("DEPLACER_REFLEXION", best_cand), check_legal=False, telemetry=telemetry
            )
        ):
            moves += 1

    return moves
