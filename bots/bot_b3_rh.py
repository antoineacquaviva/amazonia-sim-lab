"""Agent B3 — Rolling Horizon / IS-MCTS léger par déterminisation sur PlayerObservation.

100 % stdlib PyPy 3.11 / CPython 3.12, zéro dépendance tierce, zéro accès `_buf`.
Opère strictement par déterminisation cohérente avec `PlayerObservation` sur `state.clone()` :
aucune main adverse masquée sous paravent ni l'ordre futur du paquet Machine ne fuit.
"""

from __future__ import annotations

import math
from typing import Any

from bots.b2_rollouts import determinize_state_from_obs
from bots.belief_and_ticks import (
    BeliefSummary,
    _apply_step2_tick_accessories,
    build_belief_summary,
    compute_private_urgency,
    order_seats_by_tick_and_urgency,
    resolve_step2_full_with_ticks,
)
from bots.heuristic_engine import BotB2, choose_b2, score_target_b2
from engine.core_engine import (
    DEC_HUMAIN_CHAMAN_2_1,
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
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
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
)

__all__ = (
    "BotB3",
    "choose_b3",
    "determinize_state_from_obs",
    "evaluate_horizon_state",
    "play_game_b3",
)


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

    # Actifs défensifs, dilution Sabotage/Écaille et progression coopérative sur le plateau
    assets = 0.0
    rem_turns = max(0, 8 - state.tour)
    sab_tot = min(
        6,
        state.sabotage_deck_count
        + state.sabotage_pending_count
        + state.ecaille_deck_count
        + state.ecaille_pending_count,
    )
    if sab_tot > 0 and rem_turns > 0:
        assets += 0.0055 * rem_turns * sab_tot
    if state.get_croc_parcel() is not None and rem_turns > 0:
        assets += 0.008
    if state.get_duel_state()[0] == 2 and rem_turns > 0:
        assets += 0.006
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            if rem_turns > 0:
                if state.has_machine_alteration(r, mt):
                    assets += 0.012
                if state.get_machine_cale(r, mt) != 0:
                    assets += 0.007

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
            elif state.is_slot_rooted(slot_idx):
                rinfo = state.get_slot_rooted_info(slot_idx)
                if rinfo is not None:
                    r_rt, _, tier_rt, _ = rinfo
                    sch_ray = sum(
                        state.get_parcel_souches(r_rt, p_s)
                        for p_s in range(1, p_max + 1)
                        if not state.is_route_forestiere(r_rt, p_s)
                    )
                    assets += 0.014 * min(sch_ray, tier_rt) + 0.008
        for rk in range(TRACK_LEN):
            code = state.get_tactique_at_rank(rk)
            if is_reve_code(code):
                # Rêve proche du rang 1 (rk == 0) = victoire anticipée imminente
                assets += 0.010 * (TRACK_LEN - rk) / TRACK_LEN
        if cfg.nb_animaux_sauvages >= 1:
            # Présence de Gardiens sur la piste rendant les paris d'activation / Éveil possibles
            g_cnt = sum(1 for c in range(1, TRACK_LEN + 1) if state.get_gardien_at_case(c)[0] > 0)
            if g_cnt >= 1:
                assets += min(0.025, 0.010 * g_cnt)

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
            DEC_HUMAIN_CHAMAN_2_1,
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


def _paired_margin_separated(diffs: list[float], threshold: float) -> bool:
    """Vrai si la marge CRN appariée entre top-2 dépasse à la fois le seuil et 1,96 * SE."""
    m = len(diffs)
    if m == 0:
        return False
    mean_d = sum(diffs) / float(m)
    if m == 1:
        return abs(mean_d) >= threshold
    var_d = sum((d - mean_d) ** 2 for d in diffs) / float(m - 1)
    se_d = math.sqrt(var_d / float(m))
    return abs(mean_d) > max(threshold, 1.96 * se_d)


class BotB3:
    """Agent Rolling Horizon / IS-MCTS léger à conservation exacte et budget CRN adaptatif."""

    @staticmethod
    def choose_from_determinized(
        state: GameState,
        obs: PlayerObservation,
        decision: DecisionRequest,
        *,
        n_determinizations: int = 2,
        max_determinizations: int | None = None,
        uncertainty_threshold: float = 0.035,
        horizon_turns: int = 1,
        max_candidates: int = 3,
        max_steps: int = 2000,
        budget_stats: dict[str, int] | None = None,
    ) -> Any:
        opts = decision.options
        assert len(opts) >= 1
        if len(opts) == 1:
            if budget_stats is not None:
                budget_stats["determinizations_used"] = 0
                budget_stats["rollouts_executed"] = 0
            return opts[0]

        candidates = _rank_candidates_for_b3(obs, decision, state.cfg, max_candidates)
        if len(candidates) == 1:
            if budget_stats is not None:
                budget_stats["determinizations_used"] = 0
                budget_stats["rollouts_executed"] = 0
            return candidates[0]

        b2_choice = BotB2.choose(obs, decision, state.cfg)
        stop_tour = min(9, obs.tour + max(1, horizon_turns))
        min_det = max(1, n_determinizations)
        max_det = max(min_det, max_determinizations if max_determinizations is not None else max(min_det, 6))

        # Phase 1 : évaluer tous les candidats sur les `min_det` premiers mondes CRN partagés
        det_worlds = [
            determinize_state_from_obs(state, obs, det_idx=d_i) for d_i in range(min_det)
        ]
        scores_by_cand: list[list[float]] = [[] for _ in candidates]
        rollouts_run = 0

        for c_idx, cand in enumerate(candidates):
            for det_w in det_worlds:
                sim = det_w.clone()
                apply_choice(sim, cand)
                scores_by_cand[c_idx].append(
                    _rollout_horizon_b2(
                        sim,
                        stop_tour=stop_tour,
                        k_max_passes=3,
                        max_steps=max_steps,
                    )
                )
                rollouts_run += 1

        def _cand_mean(c_idx: int) -> float:
            vals = scores_by_cand[c_idx]
            mean_v = sum(vals) / float(len(vals))
            if candidates[c_idx] == b2_choice:
                mean_v += 0.0025
            return mean_v

        def _cand_tb(c_idx: int) -> int:
            return int(
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

        ranked_idx = sorted(
            range(len(candidates)),
            key=lambda i: (_cand_mean(i), _cand_tb(i)),
            reverse=True,
        )
        top1, top2 = ranked_idx[0], ranked_idx[1]

        # Phase 2 : allocation dynamique du budget sur le duel top-2 uniquement si l'écart est incertain
        n_det_used = min_det
        while n_det_used < max_det:
            diffs_12 = [
                scores_by_cand[top1][k] - scores_by_cand[top2][k] for k in range(n_det_used)
            ]
            if _paired_margin_separated(diffs_12, uncertainty_threshold):
                break
            extra_world = determinize_state_from_obs(state, obs, det_idx=n_det_used)
            for c_idx in (top1, top2):
                sim = extra_world.clone()
                apply_choice(sim, candidates[c_idx])
                scores_by_cand[c_idx].append(
                    _rollout_horizon_b2(
                        sim,
                        stop_tour=stop_tour,
                        k_max_passes=3,
                        max_steps=max_steps,
                    )
                )
                rollouts_run += 1
            n_det_used += 1

        if budget_stats is not None:
            budget_stats["determinizations_used"] = n_det_used
            budget_stats["rollouts_executed"] = rollouts_run

        best_idx = max((top1, top2), key=lambda i: (_cand_mean(i), _cand_tb(i)))
        return candidates[best_idx]


def choose_b3(
    state: GameState,
    decision: DecisionRequest,
    *,
    n_determinizations: int = 2,
    max_determinizations: int | None = None,
    uncertainty_threshold: float = 0.035,
    horizon_turns: int = 1,
    max_candidates: int = 3,
    max_steps: int = 2000,
    budget_stats: dict[str, int] | None = None,
) -> Any:
    """Point d'entrée isolé B3 : extrait d'abord `obs` puis déterminise sans fuite d'information."""
    obs = state.get_observation(decision.decideur)
    return BotB3.choose_from_determinized(
        state,
        obs,
        decision,
        n_determinizations=n_determinizations,
        max_determinizations=max_determinizations,
        uncertainty_threshold=uncertainty_threshold,
        horizon_turns=horizon_turns,
        max_candidates=max_candidates,
        max_steps=max_steps,
        budget_stats=budget_stats,
    )


def _current_def2_target(state: GameState, seat: int) -> tuple[Any, ...] | None:
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
    return score_target_b2.held_score(obs, cfg, belief, cur_spot)


def _resolve_step2_b3(
    state: GameState,
    *,
    k_max_passes: int = 4,
    n_determinizations: int = 2,
    max_determinizations: int | None = None,
    uncertainty_threshold: float = 0.035,
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
                    _apply_step2_tick_accessories(state, s, t_best, obs_s, bel_s)
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
                _apply_step2_tick_accessories(state, s, t_2, obs_s, bel_s)
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
                    _apply_step2_tick_accessories(state, s, best_alt, obs_s, bel_s)
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
        min_det = max(1, n_determinizations)
        max_det = max(min_det, max_determinizations if max_determinizations is not None else max(min_det, 6))

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

            diffs_km: list[float] = []
            d_i = 0
            while d_i < max_det:
                dw = determinize_state_from_obs(state, obs_s, det_idx=d_i + 10)
                sim_keep = dw.clone()
                finish_step2_to_3_1(sim_keep)
                v_keep = _rollout_horizon_b2(
                    sim_keep, stop_tour=stop_t, k_max_passes=3, max_steps=max_steps
                )

                sim_move = dw.clone()
                apply_step2_def2(
                    sim_move, s, ("DEPLACER_REFLEXION", best_alt), check_legal=False
                )
                finish_step2_to_3_1(sim_move)
                v_move = _rollout_horizon_b2(
                    sim_move, stop_tour=stop_t, k_max_passes=3, max_steps=max_steps
                )
                diffs_km.append(v_move - v_keep)
                d_i += 1
                if d_i >= min_det and _paired_margin_separated(diffs_km, uncertainty_threshold):
                    break

            if (sum(diffs_km) / float(len(diffs_km))) > 0.012:
                apply_step2_def2(
                    state,
                    s,
                    ("DEPLACER_REFLEXION", best_alt),
                    check_legal=False,
                    telemetry=telemetry,
                )
                _apply_step2_tick_accessories(state, s, best_alt, obs_s, bel_s)

    # 5. Repli propre des pions restés orphelins (1/2 Furtivité/Lisière ou pari Gardien Mode 2 incomplet)
    for s in range(n):
        if state.get_player_def_loc_raw(s, 1) == 0 or state.is_player_def2_definitif(s):
            continue
        cur_sp = _current_def2_target(state, s)
        if cur_sp is None:
            continue
        obs_s = state.get_observation(s)
        need_retreat = False
        if cur_sp[0] == "FURTIVITE":
            _, ray_o, rv_o = cur_sp
            need_retreat = obs_s.furtivite_ray_rive_defs(int(ray_o), int(rv_o)) == 1
        elif cur_sp[0] == "LISIERE" and obs_s.mode >= 2:
            _, sl_o = cur_sp
            _, st_lo, nb_co = obs_s.lisiere_tile_info(int(sl_o))
            need_retreat = st_lo == LISIERE_UNCONSTRUCTED and nb_co == 1
        elif cur_sp[0] == "GARDIEN_PARI" and cfg.mode == 2:
            need_retreat = not (obs_s.tour < 8 and obs_s.total_gardien_pari_defenders() == n)
        if not need_retreat:
            continue
        viable = tuple(
            t
            for t in list_legal_targets(state, s, is_first_defender=False, exclude_own_def2=True)
            if t[0] == "FORET"
            or (
                t[0] == "FURTIVITE"
                and obs_s.furtivite_ray_rive_defs(int(t[1]), int(t[2])) == 1
            )
            or (
                t[0] == "LISIERE"
                and obs_s.mode >= 2
                and obs_s.lisiere_tile_info(int(t[1]))[1] == LISIERE_UNCONSTRUCTED
                and obs_s.lisiere_tile_info(int(t[1]))[2] == 1
            )
        )
        if viable:
            bel_s = build_belief_summary(obs_s, cfg)
            fb_t, _ = _pick_best_b2_target(
                obs_s, cfg, bel_s, viable, is_first=False, salt_base=253
            )
            apply_step2_def2(
                state, s, ("DEPLACER_REFLEXION", fb_t), check_legal=False, telemetry=telemetry
            )
            _apply_step2_tick_accessories(state, s, fb_t, obs_s, bel_s)

    finish_step2_to_3_1(state, telemetry=telemetry)


def play_game_b3(
    state: GameState,
    *,
    k_max_passes: int = 4,
    n_determinizations: int = 2,
    max_determinizations: int | None = None,
    uncertainty_threshold: float = 0.035,
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
            DEC_HUMAIN_CHAMAN_2_1,
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            _resolve_step2_b3(
                state,
                k_max_passes=k_max_passes,
                n_determinizations=n_determinizations,
                max_determinizations=max_determinizations,
                uncertainty_threshold=uncertainty_threshold,
                horizon_turns=horizon_turns,
                max_steps=max_steps,
                telemetry=telemetry,
            )
            continue

        choice = choose_b3(
            state,
            out,
            n_determinizations=n_determinizations,
            max_determinizations=max_determinizations,
            uncertainty_threshold=uncertainty_threshold,
            horizon_turns=horizon_turns,
            max_candidates=max_candidates,
            max_steps=max_steps,
        )
        apply_choice(state, choice, telemetry=telemetry)
