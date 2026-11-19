"""Agent B3 — Rolling Horizon / IS-MCTS léger par déterminisation sur PlayerObservation.

100 % stdlib PyPy 3.11 / CPython 3.12, zéro dépendance tierce, zéro accès `_buf`.
Opère strictement par déterminisation cohérente avec `PlayerObservation` sur `state.clone()` :
aucune main adverse masquée sous paravent ni l'ordre futur du paquet Machine ne fuit.
"""

from __future__ import annotations

from typing import Any

from bots.belief_and_ticks import (
    BeliefSummary,
    build_belief_summary,
    compute_private_urgency,
    order_seats_by_tick_and_urgency,
    resolve_step2_full_with_ticks,
)
from bots.heuristic_engine import BotB2, choose_b2, score_target_b2
from engine.core_engine import (
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    advance_step2_to_2_2,
    apply_choice,
    apply_step2_def1,
    apply_step2_def2,
    clear_step2_pending_wait,
    finish_step2_to_3_1,
    list_legal_targets,
    step_until_decision,
)
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    DecisionRequest,
    GameOver,
)
from engine.rng import (
    SRC_BOT_TIEBREAK,
    SRC_DICE,
    rand_u64,
    roll_d6,
    shuffle_deterministic,
)
from engine.state import (
    CARD_NONE,
    CARD_SABOTAGE,
    LISIERE_CONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    TRACK_LEN,
    GameConfig,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_code,
    machine_card_code,
)

__all__ = (
    "BotB3",
    "choose_b3",
    "determinize_state_from_obs",
    "evaluate_horizon_state",
    "play_game_b3",
)

_SRC_B3_DETERMINIZE: int = 41


def _reseed_config(cfg: GameConfig, det_seed: int, det_rep: int) -> GameConfig:
    """Construit une copie de `GameConfig` avec un flux PRNG futur indépendant."""
    return GameConfig(
        n_players=cfg.n_players,
        mode=cfg.mode,
        peuples=cfg.peuples,
        exp_seed=det_seed,
        rep_id=det_rep,
        coordonnateur_initial=cfg.coordonnateur_initial,
        max_revision_passes=cfg.max_revision_passes,
        profil_piste=cfg.profil_piste,
        regle_ouverture_reve_multiple=cfg.regle_ouverture_reve_multiple,
        offset_seuil_parade=cfg.offset_seuil_parade,
        placement_initial_machines=cfg.placement_initial_machines,
        role_abatteuse_fin_de_piste=cfg.role_abatteuse_fin_de_piste,
        synergie_binome_machines=cfg.synergie_binome_machines,
        reveil_quota_mode=cfg.reveil_quota_mode,
        reveil_gardien_fate=cfg.reveil_gardien_fate,
        reve_activation_mode=cfg.reve_activation_mode,
        tile_profiles=cfg.tile_profiles,
    )


def determinize_state_from_obs(
    template_state: GameState,
    obs: PlayerObservation,
    det_idx: int = 0,
) -> GameState:
    """Construit un clone déterminisé cohérent avec `obs` (zéro fuite mains/paquet/PRNG futur).

    Garantie d'isolation : deux états `s1`, `s2` partageant la même `PlayerObservation`
    produisent exactement les mêmes octets `raw_used_bytes()` après déterminisation.
    """
    cfg = template_state.cfg
    seat = obs.observer_seat
    n = obs.n_players

    salt = ((obs.step & 0xFF) << 16) | ((seat & 0x0F) << 8) | (det_idx & 0xFF)
    det_seed = int(
        rand_u64(cfg.exp_seed, cfg.rep_id, _SRC_B3_DETERMINIZE, obs.tour, seat, salt)
        & 0x7FFFFFFF
    )
    det_rep = int(
        rand_u64(cfg.exp_seed, cfg.rep_id, _SRC_B3_DETERMINIZE, obs.tour, seat + 8, salt)
        & 0x3FFFFFFF
    )

    det = template_state.clone()
    det.cfg = _reseed_config(cfg, det_seed, det_rep)

    # 1. Échantillonner les mains masquées sous paravent uniquement depuis `obs`
    known_machine_cards: set[int] = set()
    known_sabotages = 0
    unknown_seats: list[int] = []

    for s in range(n):
        h = obs.hand_of(s)
        if not h.has_card:
            if not obs.paravents_ouverts and s != seat:
                det.set_player_hand(s, CARD_NONE, 0, 0, 0, 0)
            continue
        if h.card is None:
            unknown_seats.append(s)
        elif h.card == CARD_SABOTAGE:
            known_sabotages += 1
        elif 1 <= h.card <= 2 * n:
            known_machine_cards.add(h.card)

    if not obs.paravents_ouverts and unknown_seats:
        pool: list[int] = []
        for r in range(n):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                _, st = obs.machine_pos_status(r, mt)
                if st == MACHINE_STATUS_NORMAL:
                    code = machine_card_code(r, mt)
                    if code not in known_machine_cards:
                        pool.append(code)
        rem_sab = max(0, obs.sabotage_deck_count - known_sabotages)
        pool.extend([CARD_SABOTAGE] * rem_sab)
        while len(pool) < len(unknown_seats):
            pool.append(CARD_SABOTAGE)

        shuffled_pool = shuffle_deterministic(
            pool, det_seed, det_rep, _SRC_B3_DETERMINIZE, obs.tour, det_idx + 1
        )
        for idx_u, s in enumerate(unknown_seats):
            c_draw = shuffled_pool[idx_u]
            if c_draw == CARD_SABOTAGE:
                det.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
            else:
                d1 = roll_d6(det_seed, det_rep, SRC_DICE, obs.tour, s, det_idx * 2)
                d2 = roll_d6(det_seed, det_rep, SRC_DICE, obs.tour, s, det_idx * 2 + 1)
                lec_m = min(d1, d2)
                t_code, _, _ = obs.tactique_code_bugs_app(lec_m - 1)
                bound_t = t_code if is_tactique_code(t_code) else 0
                det.set_player_hand(s, c_draw, d1, d2, lec_m, bound_t)

    # 2. Réécrire intégralement le paquet Machine restant sans lire l'ordre secret d'origine
    orig_sab_deck = obs.sabotage_deck_count
    orig_sab_pend = obs.sabotage_pending_count
    det.sabotage_deck_count = orig_sab_deck
    det.sabotage_pending_count = 0
    det.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    det.sabotage_pending_count = orig_sab_pend

    # Retirer du paquet futur les cartes Machine actuellement en main (connues + échantillonnées)
    for s in range(n):
        c_held, _, _, _, _ = det.get_player_hand(s)
        if 1 <= c_held <= 2 * n:
            det.remove_machine_card_from_deck_if_present(c_held)

    target_rem = obs.deck_remaining_count
    det.deck_cursor = min(det.deck_len, max(0, det.deck_len - target_rem))
    return det


def _gameover_utility(res: GameOver) -> float:
    """Valeur terminale d'une fin de partie simulée, centrée sur la survie des Arbres."""
    val = res.ratio_arbres
    if res.cause_fin in (CAUSE_REVEIL_GARDIENS, CAUSE_REVE_RANG_1):
        val += 0.03
    elif res.cause_fin == CAUSE_TOUR_8:
        val += 0.01
    return val


def evaluate_horizon_state(state: GameState) -> float:
    """Potentiel heuristique dense d'une feuille Rolling Horizon non terminale."""
    cfg = state.cfg
    n = cfg.n_players
    p_max = cfg.p_max
    init_trees_per_ray = sum(cfg.dotation_arbres)
    total_init = max(1, n * init_trees_per_ray)

    tree_ratio = state.total_arbres_plateau() / total_init

    # Pression des machines actives et jetons Puissance
    danger = 0.0
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            rouges = state.get_machine_effective_rouges(r, mt)
            _, bleus = state.get_machine_tokens(r, mt)
            net_pow = max(0, rouges - bleus)
            depth_w = pos / p_max
            rat_pen = 0.018 if st == MACHINE_STATUS_RATISSAGE else 0.0
            danger += 0.012 * depth_w + 0.008 * net_pow + rat_pen

    # Actifs défensifs et progression coopérative sur le plateau
    assets = 0.0
    for r in range(n):
        for p in range(1, p_max + 1):
            if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                assets += 0.006
            ins = state.get_parcel_insectes(r, p)
            if ins > 0:
                assets += 0.003 * min(3, ins)

    if cfg.mode >= 2:
        for slot_idx in range(2 * n):
            st_l, _ = state.get_lisiere_tile_state(slot_idx)
            if st_l == LISIERE_CONSTRUCTED:
                assets += 0.012
        for rk in range(TRACK_LEN):
            code = state.get_tactique_at_rank(rk)
            if is_reve_code(code):
                # Rêve proche du rang 1 (rk == 0) = victoire anticipée imminente
                assets += 0.010 * (TRACK_LEN - rk) / TRACK_LEN
        if cfg.reveil_quota > 0:
            # Présence d'au moins un Gardien Face 2 éveillé rendant le Réveil possible dès le tour suivant
            has_f2 = any(
                state.get_gardien_at_case(c)[0] > 0 and state.get_gardien_at_case(c)[1] == 2
                for c in range(1, TRACK_LEN + 1)
            )
            if has_f2:
                assets += 0.015

    return tree_ratio + assets - danger


def _rollout_horizon_b2(
    sim_state: GameState,
    *,
    stop_tour: int,
    k_max_passes: int = 3,
    max_steps: int = 2000,
) -> float:
    """Déroule `sim_state` avec B2 jusqu'à `stop_tour` (ou fin de partie) et retourne sa valeur."""
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"Garde-fou max_steps={max_steps} dépassé dans rollout B3")
        out = step_until_decision(sim_state, max_internal_steps=max_steps)
        if isinstance(out, GameOver):
            return _gameover_utility(out)
        if sim_state.tour >= stop_tour and sim_state.step == STEP_2_1_DEF1:
            return evaluate_horizon_state(sim_state)
        if sim_state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            resolve_step2_full_with_ticks(
                sim_state,
                score_target_b2,
                k_max_passes=k_max_passes,
                epsilon_base=24.0,
                epsilon_step=12.0,
            )
            if sim_state.tour >= stop_tour:
                return evaluate_horizon_state(sim_state)
            continue

        choice = choose_b2(sim_state, out)
        apply_choice(sim_state, choice)


def _rank_candidates_for_b3(
    obs: PlayerObservation,
    decision: DecisionRequest,
    cfg: GameConfig,
    max_candidates: int,
) -> tuple[Any, ...]:
    """Pré-trie les options légales avec l'heuristique B2 pour borner le facteur de branchement."""
    opts = decision.options
    if len(opts) <= max_candidates:
        return opts

    b2_fav = BotB2.choose(obs, decision, cfg)
    if decision.decision_type in (DEC_POSE_DEFENSEUR_1, DEC_POSE_DEFENSEUR_2):
        belief: BeliefSummary = build_belief_summary(obs, cfg)
        is_def2 = decision.decision_type == DEC_POSE_DEFENSEUR_2
        scored = sorted(
            enumerate(opts),
            key=lambda iv: (
                -score_target_b2(obs, cfg, belief, iv[1], is_def2),
                int(
                    rand_u64(
                        cfg.exp_seed,
                        cfg.rep_id,
                        SRC_BOT_TIEBREAK,
                        obs.tour,
                        obs.observer_seat,
                        iv[0],
                    )
                    & 0xFFFF
                ),
            ),
        )
        picked = [opt for _, opt in scored[:max_candidates]]
        if b2_fav not in picked:
            picked[-1] = b2_fav
        return tuple(picked)

    # Pour les autres décisions à large éventail : inclure le favori B2 + sous-ensemble déterministe
    picked_other: list[Any] = [b2_fav]
    remaining = [o for o in opts if o != b2_fav]
    if remaining:
        stride = max(1, len(remaining) // max(1, max_candidates - 1))
        idx = 0
        while len(picked_other) < max_candidates and idx < len(remaining):
            cand = remaining[idx]
            if cand not in picked_other:
                picked_other.append(cand)
            idx += stride
        for cand in remaining:
            if len(picked_other) >= max_candidates:
                break
            if cand not in picked_other:
                picked_other.append(cand)
    return tuple(picked_other)


class BotB3:
    """Agent Rolling Horizon / IS-MCTS léger opérant par déterminisation cohérente sur clone."""

    @staticmethod
    def choose_from_determinized(
        state: GameState,
        obs: PlayerObservation,
        decision: DecisionRequest,
        *,
        n_determinizations: int = 2,
        horizon_turns: int = 1,
        max_candidates: int = 3,
        max_steps: int = 2000,
    ) -> Any:
        opts = decision.options
        assert len(opts) >= 1
        if len(opts) == 1:
            return opts[0]

        candidates = _rank_candidates_for_b3(obs, decision, state.cfg, max_candidates)
        if len(candidates) == 1:
            return candidates[0]

        b2_choice = BotB2.choose(obs, decision, state.cfg)
        stop_tour = min(9, obs.tour + max(1, horizon_turns))
        n_det = max(1, n_determinizations)

        # Pré-générer les `n_det` mondes déterminisés CRN partagés entre tous les candidats
        det_worlds = [
            determinize_state_from_obs(state, obs, det_idx=d_i) for d_i in range(n_det)
        ]

        best_opt = candidates[0]
        best_val = -1e9
        best_tb = -1

        for c_idx, cand in enumerate(candidates):
            acc_val = 0.0
            for det_w in det_worlds:
                sim = det_w.clone()
                apply_choice(sim, cand)
                acc_val += _rollout_horizon_b2(
                    sim,
                    stop_tour=stop_tour,
                    k_max_passes=3,
                    max_steps=max_steps,
                )
            mean_val = acc_val / n_det
            # Léger prior domaine B2 pour stabiliser les ex-aequo Monte-Carlo
            if cand == b2_choice:
                mean_val += 0.0025
            tb = int(
                rand_u64(
                    state.cfg.exp_seed,
                    state.cfg.rep_id,
                    SRC_BOT_TIEBREAK,
                    obs.tour,
                    obs.observer_seat,
                    c_idx + 500,
                )
                & 0xFFFFFFFF
            )
            if mean_val > best_val or (mean_val == best_val and tb > best_tb):
                best_val = mean_val
                best_tb = tb
                best_opt = cand

        return best_opt


def choose_b3(
    state: GameState,
    decision: DecisionRequest,
    *,
    n_determinizations: int = 2,
    horizon_turns: int = 1,
    max_candidates: int = 3,
    max_steps: int = 2000,
) -> Any:
    """Point d'entrée isolé B3 : extrait d'abord `obs` puis déterminise sans fuite d'information."""
    obs = state.get_observation(decision.decideur)
    return BotB3.choose_from_determinized(
        state,
        obs,
        decision,
        n_determinizations=n_determinizations,
        horizon_turns=horizon_turns,
        max_candidates=max_candidates,
        max_steps=max_steps,
    )


def _current_def2_target(state: GameState, seat: int) -> tuple[Any, ...] | None:
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
    if kind == "GARDIEN_REVEIL":
        return ("GARDIEN_REVEIL", a)
    if kind == "REVE_ACTIVATION":
        return ("REVE_ACTIVATION", a)
    return None


def _pick_best_b2_target(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    legal_targets: tuple[Any, ...],
    *,
    is_first: bool,
    salt_base: int,
) -> tuple[Any, float]:
    best_t = legal_targets[0]
    best_v = -1e12
    best_tb = -1
    for idx_t, t in enumerate(legal_targets):
        v = score_target_b2(obs, cfg, belief, t, is_first)
        tb = int(
            rand_u64(
                cfg.exp_seed,
                cfg.rep_id,
                SRC_BOT_TIEBREAK,
                obs.tour,
                obs.observer_seat,
                salt_base * 64 + idx_t,
            )
            & 0xFFFFFFFF
        )
        if v > best_v or (v == best_v and tb > best_tb):
            best_v = v
            best_tb = tb
            best_t = t
    return best_t, best_v


def _score_held_spot_b3(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    cur_spot: tuple[Any, ...],
) -> float:
    """Évalue la valeur marginale du poste déjà occupé par le 2e Défenseur du joueur."""
    kind = cur_spot[0]
    base = score_target_b2(obs, cfg, belief, cur_spot, False)
    if kind == "GARDIEN_REVEIL":
        _, case_c = cur_spot
        q = cfg.reveil_quota
        cnt = obs.gardien_reveil_defenders(int(case_c))
        if q > 0 and cnt >= q:
            return base + 480.0
        return base - 260.0
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
        if cnt == 2:
            return base + 380.0
        if cnt > 2:
            return base - 220.0
        return base - 60.0
    if kind == "LISIERE":
        _, slot_idx = cur_spot
        _, st_l, nb_c = obs.lisiere_tile_info(int(slot_idx))
        if st_l == 1 and nb_c == 2:
            return base + 420.0
        if st_l == 1 and nb_c == 1:
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
        idx = r_i * 5 + (p_i - 1)
        seuil_e = belief.parcel_expected_seuil[idx]
        s_prob = belief.parcel_strike_prob[idx]
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and tot_def == 1:
            return base + 380.0
        if obs.mode >= 2 and obs.parcel_has_nid(r_i, p_i) and defs == 1:
            return base + 350.0
        if s_prob > 0.15 and (tot_def - 1) < seuil_e <= tot_def:
            return base + 360.0 * min(1.5, s_prob)
        if tot_def - 1 >= seuil_e:
            return base - 190.0
    return base


def _resolve_step2_b3(
    state: GameState,
    *,
    k_max_passes: int = 4,
    n_determinizations: int = 2,
    horizon_turns: int = 1,
    max_steps: int = 2000,
    telemetry: Any | None = None,
) -> None:
    """Résout 2.1 + 2.2 avec passes B2 suivies d'une passe finale IS-MCTS déterminisée."""
    if k_max_passes <= 0:
        resolve_step2_full_with_ticks(
            state,
            score_target_b2,
            k_max_passes=0,
            epsilon_base=24.0,
            epsilon_step=12.0,
            telemetry=telemetry,
        )
        return

    cfg = state.cfg
    n = cfg.n_players
    clear_step2_pending_wait(state)

    # 1. Étape 2.1 en Ticks discrets 1..3
    if state.step == STEP_2_1_DEF1:
        rem_1 = [s for s in range(n) if state.get_player_def_loc_raw(s, 0) == 0]
        for current_tick in (1, 2, 3):
            if not rem_1:
                break
            tick_items: list[tuple[int, int, float]] = []
            for s in rem_1:
                obs_s = state.get_observation(s)
                bel_s = build_belief_summary(obs_s, cfg)
                t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=True)
                if t_s <= current_tick or current_tick == 3:
                    tick_items.append((s, current_tick, u_s))
            ordered_1 = order_seats_by_tick_and_urgency(
                tick_items, cfg, state.tour, 210 + current_tick
            )
            for s in ordered_1:
                obs_s = state.get_observation(s)
                bel_s = build_belief_summary(obs_s, cfg)
                legal_1 = list_legal_targets(state, s, is_first_defender=True)
                if not legal_1:
                    apply_step2_def1(
                        state, s, ("PASSER_IMPASSE",), check_legal=False, telemetry=telemetry
                    )
                else:
                    t_best, _ = _pick_best_b2_target(
                        obs_s, cfg, bel_s, legal_1, is_first=True, salt_base=210 + current_tick
                    )
                    apply_step2_def1(state, s, t_best, check_legal=False, telemetry=telemetry)
                rem_1.remove(s)
        advance_step2_to_2_2(state, telemetry=telemetry)

    if state.step != STEP_2_2_DEF2:
        return

    # 2. Pose initiale du 2e Défenseur en face réflexion (Ticks 1..3)
    clear_step2_pending_wait(state)
    rem_2 = [s for s in range(n) if state.get_player_def_loc_raw(s, 1) == 0]
    for current_tick in (1, 2, 3):
        if not rem_2:
            break
        tick_cands: list[tuple[int, int, float]] = []
        for s in rem_2:
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=False)
            if t_s <= current_tick or current_tick == 3:
                tick_cands.append((s, current_tick, u_s))
        ordered_2 = order_seats_by_tick_and_urgency(
            tick_cands, cfg, state.tour, 220 + current_tick
        )
        for s in ordered_2:
            obs_s = state.get_observation(s)
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
                t_2, _ = _pick_best_b2_target(
                    obs_s, cfg, bel_s, legal_2, is_first=False, salt_base=220 + current_tick
                )
                apply_step2_def2(
                    state, s, ("POSER_REFLEXION", t_2), check_legal=False, telemetry=telemetry
                )
            rem_2.remove(s)

    # 3. Passes rapides heuristiques B2 (convergence coopérative sur signaux de table)
    heur_passes = max(0, min(3, k_max_passes - 1))
    for pass_idx in range(1, heur_passes + 1):
        refl = [
            s
            for s in range(n)
            if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s)
        ]
        if not refl:
            break
        eps_r = 24.0 + (pass_idx - 1) * 12.0
        p_items: list[tuple[int, int, float]] = []
        for s in refl:
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=False)
            p_items.append((s, t_s, u_s))
        ordered_r = order_seats_by_tick_and_urgency(p_items, cfg, state.tour, 230 + pass_idx)
        moved_cnt = 0
        for s in ordered_r:
            cur_spot = _current_def2_target(state, s)
            if cur_spot is None:
                continue
            alts = tuple(
                t
                for t in list_legal_targets(
                    state, s, is_first_defender=False, exclude_own_def2=True
                )
                if t != cur_spot
            )
            if not alts:
                apply_step2_def2(
                    state, s, ("GARDER_REFLEXION", None), check_legal=False, telemetry=telemetry
                )
                continue
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            cur_sc = _score_held_spot_b3(obs_s, cfg, bel_s, cur_spot)
            best_alt, alt_sc = _pick_best_b2_target(
                obs_s, cfg, bel_s, alts, is_first=False, salt_base=230 + pass_idx
            )
            if alt_sc - cur_sc > eps_r:
                if apply_step2_def2(
                    state,
                    s,
                    ("DEPLACER_REFLEXION", best_alt),
                    check_legal=False,
                    telemetry=telemetry,
                ):
                    moved_cnt += 1
            else:
                apply_step2_def2(
                    state, s, ("GARDER_REFLEXION", None), check_legal=False, telemetry=telemetry
                )
        if moved_cnt == 0:
            break

    # 4. Passe finale Rolling Horizon déterminisée par siège (strictement depuis PlayerObservation)
    refl_final = [
        s
        for s in range(n)
        if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s)
    ]
    if refl_final:
        f_items: list[tuple[int, int, float]] = []
        for s in refl_final:
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            t_s, u_s = compute_private_urgency(obs_s, cfg, bel_s, is_first_defender=False)
            f_items.append((s, t_s, u_s))
        ordered_f = order_seats_by_tick_and_urgency(f_items, cfg, state.tour, 249)
        stop_t = min(9, state.tour + max(1, horizon_turns))
        n_det = max(1, n_determinizations)

        for s in ordered_f:
            cur_spot = _current_def2_target(state, s)
            if cur_spot is None:
                continue
            alts = tuple(
                t
                for t in list_legal_targets(
                    state, s, is_first_defender=False, exclude_own_def2=True
                )
                if t != cur_spot
            )
            if not alts:
                continue
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            best_alt, alt_sc = _pick_best_b2_target(
                obs_s, cfg, bel_s, alts, is_first=False, salt_base=249
            )
            cur_sc = _score_held_spot_b3(obs_s, cfg, bel_s, cur_spot)
            # N'arbitrer par rollout déterminisé que si l'alternative heuristique est sérieuse
            if alt_sc < cur_sc - 80.0:
                continue

            det_worlds = [
                determinize_state_from_obs(state, obs_s, det_idx=d_i + 10)
                for d_i in range(n_det)
            ]
            keep_sum = 0.0
            move_sum = 0.0
            for dw in det_worlds:
                sim_keep = dw.clone()
                finish_step2_to_3_1(sim_keep)
                keep_sum += _rollout_horizon_b2(
                    sim_keep, stop_tour=stop_t, k_max_passes=3, max_steps=max_steps
                )

                sim_move = dw.clone()
                apply_step2_def2(
                    sim_move, s, ("DEPLACER_REFLEXION", best_alt), check_legal=False
                )
                finish_step2_to_3_1(sim_move)
                move_sum += _rollout_horizon_b2(
                    sim_move, stop_tour=stop_t, k_max_passes=3, max_steps=max_steps
                )

            if (move_sum - keep_sum) / n_det > 0.012:
                apply_step2_def2(
                    state,
                    s,
                    ("DEPLACER_REFLEXION", best_alt),
                    check_legal=False,
                    telemetry=telemetry,
                )

    finish_step2_to_3_1(state, telemetry=telemetry)


def play_game_b3(
    state: GameState,
    *,
    k_max_passes: int = 4,
    n_determinizations: int = 2,
    horizon_turns: int = 1,
    max_candidates: int = 3,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
) -> GameOver:
    """Exécute une partie complète pilotée par B3 (Ticks 1..3 + révision IS-MCTS + Rolling Horizon)."""
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            cfg = state.cfg
            raise RuntimeError(
                f"Garde-fou max_steps={max_steps} dépassé (B3) : "
                f"mode={cfg.mode}, chassis_id={chassis_id}, n_players={cfg.n_players}, "
                f"exp_seed={cfg.exp_seed}, rep_id={cfg.rep_id}, tour={state.tour}, "
                f"step={state.step}"
            )
        out = step_until_decision(
            state, max_internal_steps=max(2000, max_steps), telemetry=telemetry
        )
        if isinstance(out, GameOver):
            return out

        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            _resolve_step2_b3(
                state,
                k_max_passes=k_max_passes,
                n_determinizations=n_determinizations,
                horizon_turns=horizon_turns,
                max_steps=max_steps,
                telemetry=telemetry,
            )
            continue

        choice = choose_b3(
            state,
            out,
            n_determinizations=n_determinizations,
            horizon_turns=horizon_turns,
            max_candidates=max_candidates,
            max_steps=max_steps,
        )
        apply_choice(state, choice, telemetry=telemetry)
