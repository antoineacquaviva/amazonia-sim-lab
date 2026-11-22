"""Plans expérimentaux CRN en blocs miroirs, Micro-Forks sans biais et Sequential Halving."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Any

from bots.belief_and_ticks import (
    resolve_step2_2_from_state,
    resolve_step2_full_with_ticks,
)
from bots.heuristic_engine import (
    choose_b1,
    choose_b2,
    score_target_b1,
    score_target_b2,
)
from engine.core_engine import (
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import GameOver
from engine.state import (
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    PEUPLES_ORDER,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    GameConfig,
    GameState,
    is_reve_code,
)

__all__ = (
    "MANDATORY_6_CIRCLES",
    "CausalForksSummary",
    "MicroForkAggregate",
    "MicroForkRecord",
    "MirrorBlock",
    "aggregate_micro_forks",
    "all_canonical_mirror_pairs",
    "inter_block_ci95",
    "micro_fork",
    "mirror_peuples",
    "paired_mirror_blocks",
    "run_micro_fork_on_config",
    "run_v6_1_causal_forks_on_config",
    "sequential_halving_select",
)

# Les 6 cercles obligatoires de couverture complète des 30 tuiles G/R/M (rule-cloud-campaigns.md §2)
MANDATORY_6_CIRCLES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("M-E-I", ("M", "E", "I")),
    ("M-R-O", ("M", "R", "O")),
    ("H-E-I", ("H", "E", "I")),
    ("M-R-H-I", ("M", "R", "H", "I")),
    ("M-O-E-H-I", ("M", "O", "E", "H", "I")),
    ("M-H-O-I-R-E", ("M", "H", "O", "I", "R", "E")),
)


def mirror_peuples(peuples: tuple[str, ...]) -> tuple[str, ...]:
    """Construit le Cercle_Miroir inversant l'orientation horaire tout en gardant le siège 0 fixe."""
    if len(peuples) <= 1:
        return peuples
    return (peuples[0], *reversed(peuples[1:]))


def _canonical_rotation(peuples: tuple[str, ...]) -> tuple[str, ...]:
    """Normalise un cercle par rotation horaire plaçant son premier peuple canonique en siège 0."""
    rank_map = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}
    best_pos = min(range(len(peuples)), key=lambda i: rank_map[peuples[i]])
    return peuples[best_pos:] + peuples[:best_pos]


def all_canonical_mirror_pairs(
    n_players: int,
) -> tuple[tuple[str, tuple[str, ...], str, tuple[str, ...]], ...]:
    """Énumère toutes les paires `(id_A, Cercle_A, id_B, Cercle_Miroir_B)` à `n_players` joueurs."""
    assert 3 <= n_players <= 6
    seen_orientations: set[tuple[str, ...]] = set()
    pairs: list[tuple[str, tuple[str, ...], str, tuple[str, ...]]] = []

    for subset in combinations(PEUPLES_ORDER, n_players):
        first = subset[0]
        for tail in permutations(subset[1:]):
            circle = (first, *tail)
            if circle in seen_orientations:
                continue
            mir = _canonical_rotation(mirror_peuples(circle))
            seen_orientations.add(circle)
            seen_orientations.add(mir)
            id_a = "-".join(circle)
            id_b = "-".join(mir)
            pairs.append((id_a, circle, id_b, mir))
    return tuple(pairs)


@dataclass(frozen=True, slots=True)
class MirrorBlock:
    """Bloc indépendant `(Cercle, Cercle_Miroir)` partageant exactement les mêmes semences CRN."""

    block_id: int
    n_players: int
    circle_id: str
    peuples: tuple[str, ...]
    mirror_id: str
    mirror_peuples: tuple[str, ...]
    exp_seed: int
    rep_ids: tuple[int, ...]
    is_mandatory_cover: bool


def paired_mirror_blocks(
    *,
    blocks_per_n: int = 3,
    reps_per_side: int = 4,
    exp_seed: int = 20260202,
    n_players_list: tuple[int, ...] = (3, 4, 5, 6),
) -> tuple[MirrorBlock, ...]:
    """Générateur déterministe de blocs miroirs CRN incluant obligatoirement les 6 cercles de couverture."""
    assert blocks_per_n >= 1 and reps_per_side >= 1
    mandatory_by_n: dict[int, list[tuple[str, tuple[str, ...]]]] = {3: [], 4: [], 5: [], 6: []}
    for cid, p_tup in MANDATORY_6_CIRCLES:
        mandatory_by_n[len(p_tup)].append((cid, p_tup))

    blocks: list[MirrorBlock] = []
    block_cursor = 0
    rep_cursor = 0

    for n_pl in n_players_list:
        mand_list = mandatory_by_n.get(n_pl, [])
        all_pairs = list(all_canonical_mirror_pairs(n_pl))
        selected: list[tuple[str, tuple[str, ...], str, tuple[str, ...], bool]] = []
        used_circles: set[tuple[str, ...]] = set()

        # 1. Insérer d'abord tous les cercles obligatoires de ce N
        for cid, p_tup in mand_list:
            canon = _canonical_rotation(p_tup)
            mir = _canonical_rotation(mirror_peuples(canon))
            selected.append(("-".join(canon), canon, "-".join(mir), mir, True))
            used_circles.add(canon)
            used_circles.add(mir)

        # 2. Compléter de manière déterministe jusqu'à max(blocks_per_n, len(mand_list))
        target_cnt = max(blocks_per_n, len(selected))
        stride = max(1, len(all_pairs) // max(1, target_cnt))
        idx_scan = 0
        while len(selected) < target_cnt and idx_scan < len(all_pairs) * 2:
            cand_id_a, cand_a, cand_id_b, cand_b = all_pairs[(idx_scan * stride) % len(all_pairs)]
            idx_scan += 1
            if cand_a in used_circles or cand_b in used_circles:
                continue
            selected.append((cand_id_a, cand_a, cand_id_b, cand_b, False))
            used_circles.add(cand_a)
            used_circles.add(cand_b)

        # Fallback séquentiel si le pas stride a laissé des trous
        if len(selected) < target_cnt:
            for cand_id_a, cand_a, cand_id_b, cand_b in all_pairs:
                if len(selected) >= target_cnt:
                    break
                if cand_a in used_circles or cand_b in used_circles:
                    continue
                selected.append((cand_id_a, cand_a, cand_id_b, cand_b, False))
                used_circles.add(cand_a)
                used_circles.add(cand_b)

        for cid_a, c_a, cid_b, c_b, is_mand in selected:
            shared_reps = tuple(range(rep_cursor, rep_cursor + reps_per_side))
            rep_cursor += reps_per_side
            blocks.append(
                MirrorBlock(
                    block_id=block_cursor,
                    n_players=n_pl,
                    circle_id=cid_a,
                    peuples=c_a,
                    mirror_id=cid_b,
                    mirror_peuples=c_b,
                    exp_seed=exp_seed,
                    rep_ids=shared_reps,
                    is_mandatory_cover=is_mand,
                )
            )
            block_cursor += 1

    return tuple(blocks)


def inter_block_ci95(block_means: list[float] | tuple[float, ...]) -> tuple[float, float, float]:
    """Calcule `(mean, se_inter_bloc, half_width_ci95)` exclusivement inter-blocs."""
    m = len(block_means)
    if m == 0:
        return 0.0, 0.0, 0.0
    mean_v = sum(block_means) / m
    if m == 1:
        return mean_v, 0.0, 0.0
    var_v = sum((x - mean_v) ** 2 for x in block_means) / (m - 1)
    se_v = math.sqrt(var_v / m)
    # Quantile Student t_0.975 approché proprement en stdlib (exact à <0.5% pour df >= 3)
    df = m - 1
    t_crit = 1.96 + 2.4 / df + 2.1 / (df * df)
    return mean_v, se_v, t_crit * se_v


# ---------------------------------------------------------------------------
# Micro-Forks contrôlés en début de 2.2 (sélection et évaluation disjointes)
# ---------------------------------------------------------------------------


def _reseed_future_turns_clone(state: GameState, new_exp_seed: int, new_rep_id: int) -> GameState:
    """Clone `state` en remplaçant `(exp_seed, rep_id)` pour des continuations futures indépendantes."""
    cloned = state.clone()
    old = cloned.cfg
    new_cfg = GameConfig(
        n_players=old.n_players,
        mode=old.mode,
        peuples=old.peuples,
        exp_seed=new_exp_seed,
        rep_id=new_rep_id,
        coordonnateur_initial=old.coordonnateur_initial,
        max_revision_passes=old.max_revision_passes,
        profil_piste=old.profil_piste,
        regle_ouverture_reve_multiple=old.regle_ouverture_reve_multiple,
        offset_seuil_parade=old.offset_seuil_parade,
        placement_initial_machines=old.placement_initial_machines,
        role_abatteuse_fin_de_piste=old.role_abatteuse_fin_de_piste,
        synergie_binome_machines=old.synergie_binome_machines,
        reve_activation_mode=old.reve_activation_mode,
        gardien_bet_cap_policy=old.gardien_bet_cap_policy,
        reve_advance_mode=old.reve_advance_mode,
        gardien_4_trigger_mode=old.gardien_4_trigger_mode,
        reve_5_trigger_mode=old.reve_5_trigger_mode,
        charge_gain_mode=old.charge_gain_mode,
        piege_scope_mode=old.piege_scope_mode,
        tile_profiles=old.tile_profiles,
    )
    cloned.cfg = new_cfg
    return cloned


def _rollout_from_post_2_2(
    state: GameState,
    *,
    is_b2: bool,
    k_max_future: int,
    max_steps: int = 2000,
) -> GameOver:
    scorer = score_target_b2 if is_b2 else score_target_b1
    chooser = choose_b2 if is_b2 else choose_b1
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"max_steps={max_steps} dépassé dans _rollout_from_post_2_2")
        out = step_until_decision(state, max_internal_steps=max_steps)
        if isinstance(out, GameOver):
            return out
        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            resolve_step2_full_with_ticks(
                state,
                scorer,
                k_max_passes=k_max_future,
                epsilon_base=24.0 if is_b2 else 32.0,
                epsilon_step=12.0,
            )
            continue
        apply_choice(state, chooser(state, out))


def _advance_to_target_2_2_anchor(
    cfg: GameConfig,
    *,
    target_tour: int,
    is_b2: bool,
    max_steps: int = 2000,
) -> GameState | None:
    """Avance une partie jusqu'au début exact de l'Étape 2.2 du `target_tour` (après 2.1)."""
    scorer = score_target_b2 if is_b2 else score_target_b1
    chooser = choose_b2 if is_b2 else choose_b1
    state = GameState(cfg)
    steps = 0

    while True:
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"max_steps={max_steps} dépassé avant ancre 2.2")
        out = step_until_decision(state, max_internal_steps=max_steps)
        if isinstance(out, GameOver):
            return None

        if state.tour == target_tour and state.step == STEP_2_1_DEF1:
            # Exécuter uniquement 2.1 en Ticks 1..3 puis s'arrêter net au début de 2.2 !
            # Pour ce faire, on résout 2.1 puis on clone immédiatement avant 2.2 :
            _resolve_only_2_1_ticks(state, scorer)
            return state.clone()

        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            resolve_step2_full_with_ticks(
                state,
                scorer,
                k_max_passes=3,
                epsilon_base=24.0 if is_b2 else 32.0,
                epsilon_step=12.0,
            )
            continue
        apply_choice(state, chooser(state, out))


def _resolve_only_2_1_ticks(state: GameState, scorer: Any) -> None:
    from bots.belief_and_ticks import (
        _pick_best_target_isolated,
        build_belief_summary,
        compute_private_urgency,
        order_seats_by_tick_and_urgency,
    )
    from engine.core_engine import (
        advance_step2_to_2_2,
        apply_step2_def1,
        clear_step2_pending_wait,
        list_legal_targets,
    )

    cfg = state.cfg
    n = cfg.n_players
    clear_step2_pending_wait(state)
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
        ordered_1 = order_seats_by_tick_and_urgency(tick_items, cfg, state.tour, 210 + current_tick)
        for s in ordered_1:
            obs_s = state.get_observation(s)
            bel_s = build_belief_summary(obs_s, cfg)
            legal_1 = list_legal_targets(state, s, is_first_defender=True)
            if not legal_1:
                apply_step2_def1(state, s, ("PASSER_IMPASSE",), check_legal=False)
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
                apply_step2_def1(state, s, t_best, check_legal=False)
            rem_1.remove(s)
    advance_step2_to_2_2(state)


@dataclass(frozen=True, slots=True)
class MicroForkRecord:
    """Résultat sans biais d'un micro-fork ancré au début de l'Étape 2.2."""

    tour_anchor: int
    diverged_in_2_2: bool
    revision_moves_k3: int
    v_k0_priv_eval: float
    v_k3_priv_eval: float
    v_k3_open_eval: float
    delta_v_negociation: float
    c_prive: float
    g_naive_selection: float
    g_unbiased_eval: float
    rho_delta: float


@dataclass(frozen=True, slots=True)
class MicroForkAggregate:
    """Agrégation statistique d'une batterie de micro-forks."""

    n_anchors: int
    pct_diverged_in_2_2: float
    mean_revision_moves_k3: float
    mean_delta_v_negociation: float
    mean_c_prive: float
    mean_g_naive_selection: float
    mean_g_unbiased_eval: float
    mean_rho_delta: float


def _pearson_corr(xs: list[float], ys: list[float]) -> float:
    m = len(xs)
    if m < 2:
        return 1.0
    mx = sum(xs) / m
    my = sum(ys) / m
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx <= 1e-12 or vy <= 1e-12:
        return 1.0 if abs(mx - my) <= 1e-9 else 0.0
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True))
    return max(-1.0, min(1.0, cov / math.sqrt(vx * vy)))


def micro_fork(
    anchor_2_2: GameState,
    *,
    is_b2: bool = True,
    n_selection_rollouts: int = 4,
    n_eval_rollouts: int = 6,
    selection_seed_offset: int = 500_000,
    eval_seed_offset: int = 900_000,
    k_max_future: int = 3,
) -> MicroForkRecord:
    """Exécute un micro-fork contrôlé sur `anchor_2_2.clone()` en séparant sélection et évaluation.

    Compare 3 branches au point exact d'entrée en 2.2 :
    - `B_k0_priv` : `K_max = 0` passes de révision **sur ce tour 2.2 uniquement**, paravents fermés ;
    - `B_k3_priv` : `K_max = 3` passes de révision **sur ce tour 2.2**, paravents fermés ;
    - `B_k3_open` : `K_max = 3` passes de révision **sur ce tour 2.2**, paravents révélés (`C_prive`).

    Pour isoler strictement la valeur de la révision de ce tour (sans confondre avec le droit de
    réviser aux tours ultérieurs), toutes les branches poursuivent les tours suivants avec la même
    politique future `k_max_future` et les mêmes tirages aléatoires CRN. Deux états identiques en
    sortie de 2.2 produisent ainsi un écart strictement nul (`0.0`) sur chaque graine.
    """
    assert anchor_2_2.step == STEP_2_2_DEF2, "micro_fork requiert un état en début d'Étape 2.2"
    assert n_selection_rollouts >= 1 and n_eval_rollouts >= 2
    assert selection_seed_offset != eval_seed_offset, (
        "Les semences de sélection et d'évaluation doivent être strictement disjointes"
    )

    scorer = score_target_b2 if is_b2 else score_target_b1
    eps_b = 24.0 if is_b2 else 32.0

    s_k0 = anchor_2_2.clone()
    s_k3 = anchor_2_2.clone()
    s_open = anchor_2_2.clone()

    resolve_step2_2_from_state(s_k0, scorer, k_max_passes=0, epsilon_base=eps_b)
    stats_k3 = resolve_step2_2_from_state(s_k3, scorer, k_max_passes=3, epsilon_base=eps_b)
    resolve_step2_2_from_state(
        s_open,
        scorer,
        k_max_passes=3,
        epsilon_base=eps_b,
        counterfactual_open_paravents=True,
    )

    diverged = s_k0.raw_used_bytes() != s_k3.raw_used_bytes()
    base_seed = anchor_2_2.cfg.exp_seed
    base_rep = anchor_2_2.cfg.rep_id

    # 1. Lot de SÉLECTION (identifie l'action candidate gagnante entre K=3 et K=0)
    sel_k0_vals: list[float] = []
    sel_k3_vals: list[float] = []
    for i in range(n_selection_rollouts):
        sel_seed = base_seed + selection_seed_offset + i * 17
        sel_rep = base_rep * 31 + i
        r0 = _rollout_from_post_2_2(
            _reseed_future_turns_clone(s_k0, sel_seed, sel_rep),
            is_b2=is_b2,
            k_max_future=k_max_future,
        )
        r3 = _rollout_from_post_2_2(
            _reseed_future_turns_clone(s_k3, sel_seed, sel_rep),
            is_b2=is_b2,
            k_max_future=k_max_future,
        )
        sel_k0_vals.append(r0.ratio_arbres)
        sel_k3_vals.append(r3.ratio_arbres)

    mean_sel_k0 = sum(sel_k0_vals) / n_selection_rollouts
    mean_sel_k3 = sum(sel_k3_vals) / n_selection_rollouts
    selected_is_k3 = mean_sel_k3 >= mean_sel_k0
    g_naive = abs(mean_sel_k3 - mean_sel_k0)

    # 2. Lot d'ÉVALUATION STRICTEMENT DISJOINT (estime sans biais Delta_V, C_prive, g et rho_delta)
    eval_k0_vals: list[float] = []
    eval_k3_vals: list[float] = []
    eval_open_vals: list[float] = []
    for j in range(n_eval_rollouts):
        ev_seed = base_seed + eval_seed_offset + j * 29
        ev_rep = base_rep * 37 + j
        e0 = _rollout_from_post_2_2(
            _reseed_future_turns_clone(s_k0, ev_seed, ev_rep),
            is_b2=is_b2,
            k_max_future=k_max_future,
        )
        e3 = _rollout_from_post_2_2(
            _reseed_future_turns_clone(s_k3, ev_seed, ev_rep),
            is_b2=is_b2,
            k_max_future=k_max_future,
        )
        eo = _rollout_from_post_2_2(
            _reseed_future_turns_clone(s_open, ev_seed, ev_rep),
            is_b2=is_b2,
            k_max_future=k_max_future,
        )
        eval_k0_vals.append(e0.ratio_arbres)
        eval_k3_vals.append(e3.ratio_arbres)
        eval_open_vals.append(eo.ratio_arbres)

    v_k0 = sum(eval_k0_vals) / n_eval_rollouts
    v_k3 = sum(eval_k3_vals) / n_eval_rollouts
    v_open = sum(eval_open_vals) / n_eval_rollouts

    delta_v_neg = v_k3 - v_k0
    c_prive = v_open - v_k3
    g_unbiased = (v_k3 - v_k0) if selected_is_k3 else (v_k0 - v_k3)
    rho_d = _pearson_corr(eval_k3_vals, eval_k0_vals)

    return MicroForkRecord(
        tour_anchor=anchor_2_2.tour,
        diverged_in_2_2=diverged,
        revision_moves_k3=stats_k3["revision_moves"],
        v_k0_priv_eval=v_k0,
        v_k3_priv_eval=v_k3,
        v_k3_open_eval=v_open,
        delta_v_negociation=delta_v_neg,
        c_prive=c_prive,
        g_naive_selection=g_naive,
        g_unbiased_eval=g_unbiased,
        rho_delta=rho_d,
    )


def run_micro_fork_on_config(
    cfg: GameConfig,
    *,
    target_tour: int = 2,
    is_b2: bool = True,
    n_selection_rollouts: int = 4,
    n_eval_rollouts: int = 6,
    k_max_future: int = 3,
) -> MicroForkRecord | None:
    """Construit l'ancre 2.2 au tour `target_tour` puis exécute `micro_fork`."""
    anchor = _advance_to_target_2_2_anchor(cfg, target_tour=target_tour, is_b2=is_b2)
    if anchor is None:
        return None
    return micro_fork(
        anchor,
        is_b2=is_b2,
        n_selection_rollouts=n_selection_rollouts,
        n_eval_rollouts=n_eval_rollouts,
        k_max_future=k_max_future,
    )


def aggregate_micro_forks(records: list[MicroForkRecord]) -> MicroForkAggregate:
    m = len(records)
    if m == 0:
        return MicroForkAggregate(0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    return MicroForkAggregate(
        n_anchors=m,
        pct_diverged_in_2_2=round(sum(1 for r in records if r.diverged_in_2_2) * 100.0 / m, 2),
        mean_revision_moves_k3=round(sum(r.revision_moves_k3 for r in records) / m, 4),
        mean_delta_v_negociation=round(sum(r.delta_v_negociation for r in records) / m, 6),
        mean_c_prive=round(sum(r.c_prive for r in records) / m, 6),
        mean_g_naive_selection=round(sum(r.g_naive_selection for r in records) / m, 6),
        mean_g_unbiased_eval=round(sum(r.g_unbiased_eval for r in records) / m, 6),
        mean_rho_delta=round(sum(r.rho_delta for r in records) / m, 4),
    )


# ---------------------------------------------------------------------------
# Sequential Halving des 128 châssis (Palier 2 & Palier 4)
# ---------------------------------------------------------------------------


def sequential_halving_select(
    scores_by_chassis: dict[int, float],
    *,
    keep_count: int | None = None,
) -> tuple[int, ...]:
    """Retient la moitié supérieure (ou `keep_count`) des châssis triés par score décroissant."""
    assert len(scores_by_chassis) >= 1
    k = keep_count if keep_count is not None else max(1, len(scores_by_chassis) // 2)
    ranked = sorted(scores_by_chassis.items(), key=lambda kv: (-kv[1], kv[0]))
    return tuple(ch_id for ch_id, _ in ranked[:k])


# ---------------------------------------------------------------------------
# Batterie contrefactuelle multi-étapes v6.1
# (2.1 / 2.2 / Rive Piège / Rive Sabotage / 4.1 Pose Piège / 5.3 Éveil)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CausalForksSummary:
    """Bilan contrefactuel multi-ancres v6.1 sur une trajectoire CRN."""

    mf_2_2: MicroForkRecord | None
    has_2_1_anchor: bool
    delta_v_2_1_b2_vs_b0: float
    has_2_1_reve_fork: bool
    delta_v_2_1_reve: float
    has_4_1_piege_fork: bool
    delta_v_4_1_pose_piege: float
    has_eveil_fork: bool
    delta_v_eveil_vs_survival: float
    total_rollouts: int
    has_furt_rive_piege_fork: bool = False
    delta_v_furt_rive_piege: float = 0.0
    has_furt_rive_sabotage_fork: bool = False
    delta_v_furt_rive_sabotage: float = 0.0
    has_charge_gain_fork: bool = False
    delta_v_charge_frappe_minus_degat: float = 0.0
    delta_tokens_act1_frappe_minus_degat: float = 0.0


def run_v6_1_causal_forks_on_config(
    cfg: GameConfig,
    *,
    target_tour: int = 2,
    is_b2: bool = True,
    n_selection_rollouts: int = 3,
    n_eval_rollouts: int = 4,
    k_max_future: int = 3,
    max_steps: int = 2000,
) -> CausalForksSummary:
    """Exécute la batterie complète des forks contrefactuels v6.1 (CRN apparié)."""
    from bots.bot_b0 import choose_b0
    from engine.core_engine import (
        DEC_POSE_PIEGE_FURTIVITE_4_1,
        advance_step2_to_2_2,
        apply_step2_def1,
        clear_step2_pending_wait,
        list_legal_targets,
    )
    from engine.primitives import DecisionRequest

    scorer = score_target_b2 if is_b2 else score_target_b1
    chooser = choose_b2 if is_b2 else choose_b1
    eps_b = 24.0 if is_b2 else 32.0
    state = GameState(cfg)
    steps = 0

    mf_rec: MicroForkRecord | None = None
    has_2_1 = False
    dv_2_1_b0 = 0.0
    has_2_1_reve = False
    dv_2_1_reve = 0.0
    has_furt_rp = False
    dv_furt_rp = 0.0
    has_furt_rs = False
    dv_furt_rs = 0.0
    has_4_1_piege = False
    dv_4_1_piege = 0.0
    has_eveil = False
    dv_eveil = 0.0
    rollouts = 0

    def _no_reve_2_1_scorer(o: Any, c: GameConfig, b: Any, t: tuple[Any, ...], is_f: bool) -> float:
        if is_f and t[0] == "REVE_ACTIVATION":
            return -1_000_000.0
        return scorer(o, c, b, t, is_f)

    def _no_furt_piege_scorer(
        o: Any, c: GameConfig, b: Any, t: tuple[Any, ...], is_f: bool
    ) -> float:
        if t[0] == "FURTIVITE" and len(t) >= 3 and int(t[2]) == FURT_RIVE_PIEGE:
            return -1_000_000.0
        return scorer(o, c, b, t, is_f)

    def _no_furt_sabotage_scorer(
        o: Any, c: GameConfig, b: Any, t: tuple[Any, ...], is_f: bool
    ) -> float:
        if t[0] == "FURTIVITE" and len(t) >= 3 and int(t[2]) == FURT_RIVE_SABOTAGE:
            return -1_000_000.0
        return scorer(o, c, b, t, is_f)

    def _no_gardien_2_2_scorer(
        o: Any, c: GameConfig, b: Any, t: tuple[Any, ...], is_f: bool
    ) -> float:
        if t[0] == "GARDIEN_PARI":
            return -1_000_000.0
        return scorer(o, c, b, t, is_f)

    def _paired_post_2_2_eval(
        s_a: GameState, s_b: GameState, seed_offset: int, mult_s: int, mult_r: int
    ) -> float:
        nonlocal rollouts
        acc_a = 0.0
        acc_b = 0.0
        for j in range(n_eval_rollouts):
            ev_s = cfg.exp_seed + seed_offset + j * mult_s
            ev_r = cfg.rep_id * mult_r + j
            acc_a += _rollout_from_post_2_2(
                _reseed_future_turns_clone(s_a, ev_s, ev_r),
                is_b2=is_b2,
                k_max_future=k_max_future,
            ).ratio_arbres
            acc_b += _rollout_from_post_2_2(
                _reseed_future_turns_clone(s_b, ev_s, ev_r),
                is_b2=is_b2,
                k_max_future=k_max_future,
            ).ratio_arbres
            rollouts += 2
        return (acc_a - acc_b) / n_eval_rollouts

    def _check_post_2_2_forks(
        cur_state: GameState, pre_2_1_snap: GameState | None, pre_2_2_snap: GameState
    ) -> None:
        nonlocal has_furt_rp, dv_furt_rp, has_furt_rs, dv_furt_rs, has_eveil, dv_eveil
        if cur_state.tour <= 7 and pre_2_1_snap is not None:
            if not has_furt_rp and any(
                cur_state.get_furtivite_nb_def_rive(r_i, 1, FURT_RIVE_PIEGE) == 2
                for r_i in range(cfg.n_players)
            ):
                s_no_rp = pre_2_1_snap.clone()
                resolve_step2_full_with_ticks(
                    s_no_rp,
                    _no_furt_piege_scorer,
                    k_max_passes=k_max_future,
                    epsilon_base=eps_b,
                    epsilon_step=12.0,
                )
                if cur_state.raw_used_bytes() != s_no_rp.raw_used_bytes():
                    has_furt_rp = True
                    dv_furt_rp = _paired_post_2_2_eval(cur_state, s_no_rp, 850_000, 41, 53)

            if not has_furt_rs and any(
                cur_state.get_furtivite_nb_def_rive(r_i, 1, FURT_RIVE_SABOTAGE) == 2
                for r_i in range(cfg.n_players)
            ):
                s_no_rs = pre_2_1_snap.clone()
                resolve_step2_full_with_ticks(
                    s_no_rs,
                    _no_furt_sabotage_scorer,
                    k_max_passes=k_max_future,
                    epsilon_base=eps_b,
                    epsilon_step=12.0,
                )
                if cur_state.raw_used_bytes() != s_no_rs.raw_used_bytes():
                    has_furt_rs = True
                    dv_furt_rs = _paired_post_2_2_eval(cur_state, s_no_rs, 870_000, 43, 59)

        if (
            not has_eveil
            and cur_state.tour <= 7
            and cfg.nb_animaux_sauvages >= 1
            and cur_state.total_gardien_pari_engaged() == cfg.n_players
        ):
            has_eveil = True
            s_surv = pre_2_2_snap.clone()
            resolve_step2_2_from_state(
                s_surv,
                _no_gardien_2_2_scorer,
                k_max_passes=k_max_future,
                epsilon_base=eps_b,
            )
            dv_eveil = _paired_post_2_2_eval(cur_state, s_surv, 830_000, 37, 43)

    while True:
        steps += 1
        if steps > max_steps:
            raise RuntimeError(f"max_steps={max_steps} dépassé dans run_v6_1_causal_forks_on_config")
        out = step_until_decision(state, max_internal_steps=max_steps)
        if isinstance(out, GameOver):
            break

        # 1 & 2. Ancres 2.1 et 2.2 au target_tour
        if state.tour == target_tour and state.step == STEP_2_1_DEF1 and not has_2_1:
            has_2_1 = True
            pre_2_1_clone = state.clone()
            s_b0_21 = state.clone()
            clear_step2_pending_wait(s_b0_21)
            for seat_i in range(cfg.n_players):
                leg_1 = list_legal_targets(s_b0_21, seat_i, is_first_defender=True)
                if not leg_1:
                    apply_step2_def1(s_b0_21, seat_i, ("PASSER_IMPASSE",), check_legal=False)
                else:
                    req_1 = DecisionRequest(
                        decideur=seat_i,
                        decision_type=DEC_POSE_DEFENSEUR_1,
                        options=leg_1,
                        context={},
                    )
                    apply_step2_def1(s_b0_21, seat_i, choose_b0(s_b0_21, req_1), check_legal=False)
            advance_step2_to_2_2(s_b0_21)

            s_noreve_21 = state.clone()
            _resolve_only_2_1_ticks(s_noreve_21, _no_reve_2_1_scorer)

            # Avancer l'état réel sur 2.1 -> début 2.2
            _resolve_only_2_1_ticks(state, scorer)
            reve_diverged = (not has_2_1_reve) and (
                state.raw_used_bytes() != s_noreve_21.raw_used_bytes()
            )

            # Fork 2.1 : B2 vs B0 (et vs sans Rêve 2.1 si pertinent)
            acc_b2_21 = 0.0
            acc_b0_21 = 0.0
            acc_nr_21 = 0.0
            for j in range(n_eval_rollouts):
                ev_s = cfg.exp_seed + 710_000 + j * 31
                ev_r = cfg.rep_id * 41 + j
                c_b2 = _reseed_future_turns_clone(state, ev_s, ev_r)
                resolve_step2_2_from_state(c_b2, scorer, k_max_passes=k_max_future, epsilon_base=eps_b)
                acc_b2_21 += _rollout_from_post_2_2(
                    c_b2, is_b2=is_b2, k_max_future=k_max_future
                ).ratio_arbres

                c_b0 = _reseed_future_turns_clone(s_b0_21, ev_s, ev_r)
                resolve_step2_2_from_state(c_b0, scorer, k_max_passes=k_max_future, epsilon_base=eps_b)
                acc_b0_21 += _rollout_from_post_2_2(
                    c_b0, is_b2=is_b2, k_max_future=k_max_future
                ).ratio_arbres
                rollouts += 2

                if reve_diverged:
                    c_nr = _reseed_future_turns_clone(s_noreve_21, ev_s, ev_r)
                    resolve_step2_2_from_state(
                        c_nr, scorer, k_max_passes=k_max_future, epsilon_base=eps_b
                    )
                    acc_nr_21 += _rollout_from_post_2_2(
                        c_nr, is_b2=is_b2, k_max_future=k_max_future
                    ).ratio_arbres
                    rollouts += 1

            dv_2_1_b0 = (acc_b2_21 - acc_b0_21) / n_eval_rollouts
            if reve_diverged:
                has_2_1_reve = True
                dv_2_1_reve = (acc_b2_21 - acc_nr_21) / n_eval_rollouts

            # Fork 2.2 (K=3 vs K=0 vs Open Paravents) sur l'ancre exacte d'entrée en 2.2
            mf_rec = micro_fork(
                state,
                is_b2=is_b2,
                n_selection_rollouts=n_selection_rollouts,
                n_eval_rollouts=n_eval_rollouts,
                k_max_future=k_max_future,
            )
            rollouts += n_selection_rollouts * 2 + n_eval_rollouts * 3

            # Résoudre 2.2 sur l'état réel puis évaluer Rive Piège / Rive Sabotage / Éveil
            pre_2_2_clone = state.clone()
            resolve_step2_2_from_state(state, scorer, k_max_passes=k_max_future, epsilon_base=eps_b)
            _check_post_2_2_forks(state, pre_2_1_clone, pre_2_2_clone)
            continue

        # Résolution normale Étape 2 sur les autres tours
        # (+ balayage 2.1 Rêve, Rive Piège, Rive Sabotage et 5.3 Éveil)
        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            need_scan = (
                (not has_2_1_reve and state.tour <= 7 and cfg.total_reves_partie > 0)
                or (not has_furt_rp and state.tour <= 7)
                or (not has_furt_rs and state.tour <= 7)
                or (not has_eveil and state.tour <= 7 and cfg.nb_animaux_sauvages >= 1)
            )
            if need_scan:
                pre_2_1_snap: GameState | None = (
                    state.clone() if state.step == STEP_2_1_DEF1 else None
                )
                if state.step == STEP_2_1_DEF1:
                    check_reve_here = (
                        (not has_2_1_reve)
                        and state.tour <= 7
                        and any(is_reve_code(state.get_tactique_at_rank(rk)) for rk in range(6))
                    )
                    s_noreve_other = state.clone() if check_reve_here else None
                    _resolve_only_2_1_ticks(state, scorer)
                    if s_noreve_other is not None:
                        _resolve_only_2_1_ticks(s_noreve_other, _no_reve_2_1_scorer)
                        if state.raw_used_bytes() != s_noreve_other.raw_used_bytes():
                            has_2_1_reve = True
                            acc_rv = 0.0
                            acc_nr = 0.0
                            for j in range(n_eval_rollouts):
                                ev_s = cfg.exp_seed + 730_000 + j * 31
                                ev_r = cfg.rep_id * 41 + j
                                c_rv = _reseed_future_turns_clone(state, ev_s, ev_r)
                                resolve_step2_2_from_state(
                                    c_rv, scorer, k_max_passes=k_max_future, epsilon_base=eps_b
                                )
                                acc_rv += _rollout_from_post_2_2(
                                    c_rv, is_b2=is_b2, k_max_future=k_max_future
                                ).ratio_arbres
                                c_nr = _reseed_future_turns_clone(s_noreve_other, ev_s, ev_r)
                                resolve_step2_2_from_state(
                                    c_nr, scorer, k_max_passes=k_max_future, epsilon_base=eps_b
                                )
                                acc_nr += _rollout_from_post_2_2(
                                    c_nr, is_b2=is_b2, k_max_future=k_max_future
                                ).ratio_arbres
                                rollouts += 2
                            dv_2_1_reve = (acc_rv - acc_nr) / n_eval_rollouts

                pre_2_2_snap = state.clone()
                resolve_step2_2_from_state(
                    state, scorer, k_max_passes=k_max_future, epsilon_base=eps_b
                )
                _check_post_2_2_forks(state, pre_2_1_snap, pre_2_2_snap)
                continue

            resolve_step2_full_with_ticks(
                state,
                scorer,
                k_max_passes=k_max_future,
                epsilon_base=eps_b,
                epsilon_step=12.0,
            )
            continue

        # 3. Fork 4.1 : pose du Piège autonome par le propriétaire du rayon (>= 2 parcelles candidates)
        if (
            not has_4_1_piege
            and out.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1
            and len(out.options) >= 2
        ):
            has_4_1_piege = True
            chosen_p = chooser(state, out)
            alt_cands = [opt_p for opt_p in out.options if opt_p != chosen_p]
            alt_p = alt_cands[0]
            s_chosen = state.clone()
            apply_choice(s_chosen, chosen_p)
            s_alt = state.clone()
            apply_choice(s_alt, alt_p)
            dv_4_1_piege = _paired_post_2_2_eval(s_chosen, s_alt, 790_000, 29, 47)
            apply_choice(state, chosen_p)
            continue

        apply_choice(state, chooser(state, out))

    return CausalForksSummary(
        mf_2_2=mf_rec,
        has_2_1_anchor=has_2_1,
        delta_v_2_1_b2_vs_b0=dv_2_1_b0,
        has_2_1_reve_fork=has_2_1_reve,
        delta_v_2_1_reve=dv_2_1_reve,
        has_4_1_piege_fork=has_4_1_piege,
        delta_v_4_1_pose_piege=dv_4_1_piege,
        has_eveil_fork=has_eveil,
        delta_v_eveil_vs_survival=dv_eveil,
        total_rollouts=max(1, rollouts),
        has_furt_rive_piege_fork=has_furt_rp,
        delta_v_furt_rive_piege=dv_furt_rp,
        has_furt_rive_sabotage_fork=has_furt_rs,
        delta_v_furt_rive_sabotage=dv_furt_rs,
        has_charge_gain_fork=False,
        delta_v_charge_frappe_minus_degat=0.0,
        delta_tokens_act1_frappe_minus_degat=0.0,
    )

