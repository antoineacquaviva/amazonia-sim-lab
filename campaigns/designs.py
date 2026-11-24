"""Plans expérimentaux CRN en blocs miroirs, Micro-Forks sans biais et Sequential Halving."""

from __future__ import annotations

import math
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Any

from bots.belief_and_ticks import (
    TargetFilter,
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
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    ANIMAUX_SAUVAGES,
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
    "BENCHMARK_ASSISE_KEYS",
    "CANON0_ACTIVE_PROFILES",
    "CANONICAL_PEUPLES_ORDER_197",
    "LOT0_NEUTRE_PROFILES",
    "MANDATORY_6_CIRCLES",
    "CanonicalAssise",
    "CausalForksSummary",
    "MicroForkAggregate",
    "MicroForkRecord",
    "MirrorBlock",
    "aggregate_micro_forks",
    "all_canonical_mirror_pairs",
    "balanced_neighbor_mirror_pairs",
    "balanced_neighbor_mirror_tables",
    "build_paired_197_calibration_configs",
    "build_plan_canon0_197",
    "build_plan_lot0_197",
    "canonicalize_dihedral_assise",
    "enumerate_197_canonical_assises",
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


# Système de triplets 2-fold exact (hémi-icosaèdre sur 6 peuples, n'inclut pas H-E-I) :
# chacune des 15 paires de voisins apparaît exactement 2 fois et chaque peuple exactement 5 fois.
_HEMI_ICOSAHEDRON_10: frozenset[frozenset[str]] = frozenset(
    frozenset((PEUPLES_ORDER[a], PEUPLES_ORDER[b], PEUPLES_ORDER[c]))
    for a, b, c in (
        (0, 1, 2),
        (0, 2, 3),
        (0, 3, 4),
        (0, 4, 5),
        (0, 5, 1),
        (1, 2, 4),
        (2, 3, 5),
        (3, 4, 1),
        (4, 5, 2),
        (5, 1, 3),
    )
)

_ALL_15_NEIGHBOR_EDGES: tuple[tuple[str, str], ...] = tuple(
    (PEUPLES_ORDER[i], PEUPLES_ORDER[j])
    if PEUPLES_ORDER[i] < PEUPLES_ORDER[j]
    else (PEUPLES_ORDER[j], PEUPLES_ORDER[i])
    for i in range(len(PEUPLES_ORDER))
    for j in range(i + 1, len(PEUPLES_ORDER))
)


def _circle_neighbor_edges(circle: tuple[str, ...]) -> tuple[tuple[str, str], ...]:
    n = len(circle)
    out: list[tuple[str, str]] = []
    for i in range(n):
        a = circle[i]
        b = circle[(i + 1) % n]
        out.append((a, b) if a < b else (b, a))
    return tuple(out)


def _greedy_balance_mirror_pairs(
    pairs: list[tuple[str, tuple[str, ...], str, tuple[str, ...]]],
    *,
    exp_seed: int,
    n_players: int,
) -> list[tuple[str, tuple[str, ...], str, tuple[str, ...]]]:
    """Ordonne des paires miroirs pour équilibrer les 15 arêtes de voisinage et les 6 peuples sur tout préfixe."""
    edge_cnt: dict[tuple[str, str], int] = {e: 0 for e in _ALL_15_NEIGHBOR_EDGES}
    peuple_cnt: dict[str, int] = {p: 0 for p in PEUPLES_ORDER}
    subset_cnt: dict[tuple[str, ...], int] = {}

    rem = [
        (
            item,
            _circle_neighbor_edges(item[1]),
            tuple(sorted(item[1])),
            rand_u64(exp_seed, n_players, SRC_BOT_TIEBREAK, 91, idx, 0),
        )
        for idx, item in enumerate(pairs)
    ]
    ordered: list[tuple[str, tuple[str, ...], str, tuple[str, ...]]] = []

    while rem:
        best_pos = 0
        best_key: tuple[int, int, int, int, int, str] | None = None
        for pos, (item, edges, sub_k, tie_u64) in enumerate(rem):
            e_max = 0
            e_sq_delta = 0
            for e in edges:
                c_e = edge_cnt[e]
                e_max = max(e_max, c_e + 1)
                e_sq_delta += 2 * c_e + 1
            p_sq_delta = 0
            for p_code in item[1]:
                p_sq_delta += 2 * peuple_cnt[p_code] + 1
            s_cur = subset_cnt.get(sub_k, 0)
            cand_key = (e_max, e_sq_delta, s_cur, p_sq_delta, tie_u64, item[0])
            if best_key is None or cand_key < best_key:
                best_key = cand_key
                best_pos = pos
        chosen_item, chosen_edges, chosen_sub, _ = rem.pop(best_pos)
        ordered.append(chosen_item)
        for e in chosen_edges:
            edge_cnt[e] += 1
        for p_code in chosen_item[1]:
            peuple_cnt[p_code] += 1
        subset_cnt[chosen_sub] = subset_cnt.get(chosen_sub, 0) + 1
    return ordered


def balanced_neighbor_mirror_pairs(
    n_players: int,
    *,
    min_animaux_sauvages: int = 0,
    exp_seed: int = 20261201,
) -> tuple[tuple[str, tuple[str, ...], str, tuple[str, ...]], ...]:
    """Ordonne les paires de cercles miroirs à `n_players` joueurs en équilibrant les 15 paires de voisins.

    Propriétés garanties (indépendantes de `PYTHONHASHSEED`) :
    - Chaque entrée `(id_a, circle_a, id_b, circle_b)` est une paire miroir exacte (`mirror_peuples(circle_a) == circle_b`).
    - À `N=3` : les 10 premières paires forment le système 2-fold exact (chaque arête apparaît 2 fois,
      chaque peuple 5 fois, y compris sous `min_animaux_sauvages=1`).
    - À `N=4`, `N=5`, `N=6` : les préfixes équilibrés couvrent équitablement toutes les 15 paires de voisins
      (et donc les 30 lisières) sans biais de troncature sur `M`/`R` ni blocage sur un cercle unique à 6J.
    """
    assert 3 <= n_players <= 6
    valid = [
        item
        for item in all_canonical_mirror_pairs(n_players)
        if sum(1 for p in item[1] if p in ANIMAUX_SAUVAGES) >= min_animaux_sauvages
    ]
    if n_players == 3:
        block_1 = [item for item in valid if frozenset(item[1]) in _HEMI_ICOSAHEDRON_10]
        block_2 = [item for item in valid if frozenset(item[1]) not in _HEMI_ICOSAHEDRON_10]
        return tuple(
            _greedy_balance_mirror_pairs(block_1, exp_seed=exp_seed, n_players=n_players)
            + _greedy_balance_mirror_pairs(block_2, exp_seed=exp_seed + 1, n_players=n_players)
        )
    return tuple(_greedy_balance_mirror_pairs(valid, exp_seed=exp_seed, n_players=n_players))


def balanced_neighbor_mirror_tables(
    n_players: int,
    *,
    min_animaux_sauvages: int = 0,
    max_tables: int | None = None,
    exp_seed: int = 20261201,
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Retourne une séquence de tables `(table_id, peuples)` groupées par paires miroirs équilibrées."""
    pairs = balanced_neighbor_mirror_pairs(
        n_players,
        min_animaux_sauvages=min_animaux_sauvages,
        exp_seed=exp_seed,
    )
    if not pairs:
        return ()
    if max_tables is not None:
        if max_tables <= 0:
            return ()
        if max_tables == 1:
            return ((pairs[0][0], pairs[0][1]),)
        n_pairs = min(len(pairs), max_tables // 2)
        pairs = pairs[:n_pairs]
    out: list[tuple[str, tuple[str, ...]]] = []
    for id_a, c_a, id_b, c_b in pairs:
        out.append((id_a, c_a))
        out.append((id_b, c_b))
    return tuple(out)


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


def _resolve_only_2_1_ticks(
    state: GameState,
    scorer: Any,
    *,
    target_filter: TargetFilter | None = None,
) -> None:
    from bots.belief_and_ticks import (
        _filter_legal_targets,
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
            legal_1 = _filter_legal_targets(
                list_legal_targets(state, s, is_first_defender=True),
                target_filter,
                is_first_defender=True,
                fallback_if_empty=True,
            )
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
# Sequential Halving générique (sélection multi-candidats Mode 4)
# ---------------------------------------------------------------------------


def sequential_halving_select(
    scores_by_candidate: dict[int, float],
    *,
    keep_count: int | None = None,
) -> tuple[int, ...]:
    """Retient la moitié supérieure (ou `keep_count`) des candidats triés par score décroissant."""
    assert len(scores_by_candidate) >= 1
    k = keep_count if keep_count is not None else max(1, len(scores_by_candidate) // 2)
    ranked = sorted(scores_by_candidate.items(), key=lambda kv: (-kv[1], kv[0]))
    return tuple(cand_id for cand_id, _ in ranked[:k])


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

    def _allow_no_reve_2_1(t: tuple[Any, ...], is_f: bool) -> bool:
        return not (is_f and t[0] == "REVE_ACTIVATION")

    def _allow_no_furt_piege(t: tuple[Any, ...], _is_f: bool) -> bool:
        return not (t[0] == "FURTIVITE" and len(t) >= 3 and int(t[2]) == FURT_RIVE_PIEGE)

    def _allow_no_furt_sabotage(t: tuple[Any, ...], _is_f: bool) -> bool:
        return not (t[0] == "FURTIVITE" and len(t) >= 3 and int(t[2]) == FURT_RIVE_SABOTAGE)

    def _allow_no_gardien_2_2(t: tuple[Any, ...], _is_f: bool) -> bool:
        return t[0] != "GARDIEN_PARI"

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
                    scorer,
                    k_max_passes=k_max_future,
                    epsilon_base=eps_b,
                    epsilon_step=12.0,
                    target_filter=_allow_no_furt_piege,
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
                    scorer,
                    k_max_passes=k_max_future,
                    epsilon_base=eps_b,
                    epsilon_step=12.0,
                    target_filter=_allow_no_furt_sabotage,
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
                scorer,
                k_max_passes=k_max_future,
                epsilon_base=eps_b,
                target_filter=_allow_no_gardien_2_2,
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
            _resolve_only_2_1_ticks(s_noreve_21, scorer, target_filter=_allow_no_reve_2_1)

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
                        _resolve_only_2_1_ticks(
                            s_noreve_other, scorer, target_filter=_allow_no_reve_2_1
                        )
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
    )


# ---------------------------------------------------------------------------
# Plans exhaustifs v6.2 sur les 197 Assises Canoniques Diédrales (Lot 0 & Canon 0)
# ---------------------------------------------------------------------------

CANONICAL_PEUPLES_ORDER_197: tuple[str, ...] = ("H", "E", "M", "R", "O", "I")
_CANON_RANK_197: dict[str, int] = {p: idx for idx, p in enumerate(CANONICAL_PEUPLES_ORDER_197)}

LOT0_NEUTRE_PROFILES: tuple[tuple[str, str], ...] = tuple(
    [(f"G{i}", "NEUTRE") for i in range(1, 16)]
    + [(f"R{i}", "NEUTRE") for i in range(1, 11)]
    + [(f"M{i}", "NEUTRE") for i in range(1, 6)]
)

CANON0_ACTIVE_PROFILES: tuple[tuple[str, str], ...] = tuple(
    [(f"G{i}", "A") for i in range(1, 16)]
    + [(f"R{i}", "A") for i in range(1, 11)]
    + [(f"M{i}", "A") for i in range(1, 6)]
)

BENCHMARK_ASSISE_KEYS: tuple[str, ...] = (
    "N3-HEI",
    "N3-ERI",
    "N3-HER",
    "N3-MOI",
    "N3-MRO",
    "N6-HEMROI",
)


@dataclass(frozen=True, slots=True)
class CanonicalAssise:
    """Assise diédrale canonique v6.2 (isomorphe à `docs/explorer_v6_2.js`)."""

    index: int  # 1..197
    n_players: int  # 3..6
    key: str  # ex. "N3-HEI", "N6-HEMROI"
    composition_key: str  # sous-ensemble non ordonné canonique (42 compositions)
    peuples: tuple[str, ...]


def canonicalize_dihedral_assise(peuples: tuple[str, ...]) -> tuple[str, tuple[str, ...]]:
    """Retourne `(canon_key, canon_seq)` invariant par rotation et symétrie miroir (ordre H,E,M,R,O,I)."""
    n = len(peuples)
    assert 3 <= n <= 6
    best: tuple[str, ...] | None = None
    best_rank: tuple[int, ...] | None = None
    for seq in (peuples, tuple(reversed(peuples))):
        for shift in range(n):
            rot = seq[shift:] + seq[:shift]
            rk = tuple(_CANON_RANK_197[p] for p in rot)
            if best_rank is None or rk < best_rank:
                best_rank = rk
                best = rot
    assert best is not None
    return (f"N{n}-{''.join(best)}", best)


def enumerate_197_canonical_assises() -> tuple[CanonicalAssise, ...]:
    """Énumère exactement les 197 assises diédrales canoniques (20 à 3J, 45 à 4J, 72 à 5J, 60 à 6J)."""
    out: list[CanonicalAssise] = []
    global_idx = 1
    for n in (3, 4, 5, 6):
        seen_n: set[str] = set()
        for subset in combinations(CANONICAL_PEUPLES_ORDER_197, n):
            comp_key = f"N{n}-{''.join(subset)}"
            first = subset[0]
            for tail in permutations(subset[1:]):
                key, canon_seq = canonicalize_dihedral_assise((first, *tail))
                if key in seen_n:
                    continue
                seen_n.add(key)
                out.append(
                    CanonicalAssise(
                        index=global_idx,
                        n_players=n,
                        key=key,
                        composition_key=comp_key,
                        peuples=canon_seq,
                    )
                )
                global_idx += 1
    assert len(out) == 197
    return tuple(out)


def build_plan_lot0_197(
    reps_per_assise: int = 8,
    *,
    exp_seed: int = 20260620,
    max_revision_passes: int = 3,
) -> tuple[tuple[CanonicalAssise, GameConfig], ...]:
    """Plan exhaustif `Lot 0` (Mode 3, 30 tuiles `NEUTRE`) sur les 197 assises canoniques."""
    assert reps_per_assise >= 1
    assises = enumerate_197_canonical_assises()
    plan: list[tuple[CanonicalAssise, GameConfig]] = []
    for assise in assises:
        for rep in range(reps_per_assise):
            rep_id = assise.index * 1000 + rep
            cfg = GameConfig(
                n_players=assise.n_players,
                mode=3,
                peuples=assise.peuples,
                exp_seed=exp_seed,
                rep_id=rep_id,
                max_revision_passes=max_revision_passes,
                tile_profiles=LOT0_NEUTRE_PROFILES,
            )
            plan.append((assise, cfg))
    return tuple(plan)


def build_plan_canon0_197(
    reps_per_assise: int = 8,
    *,
    exp_seed: int = 20260620,
    max_revision_passes: int = 3,
) -> tuple[tuple[CanonicalAssise, GameConfig], ...]:
    """Plan exhaustif `Canon 0` (Mode 4, 30 profils `A`) apparié CRN sur les 197 assises canoniques."""
    assert reps_per_assise >= 1
    assises = enumerate_197_canonical_assises()
    plan: list[tuple[CanonicalAssise, GameConfig]] = []
    for assise in assises:
        for rep in range(reps_per_assise):
            rep_id = assise.index * 1000 + rep
            cfg = GameConfig(
                n_players=assise.n_players,
                mode=4,
                peuples=assise.peuples,
                exp_seed=exp_seed,
                rep_id=rep_id,
                max_revision_passes=max_revision_passes,
                tile_profiles=CANON0_ACTIVE_PROFILES,
            )
            plan.append((assise, cfg))
    return tuple(plan)


def build_paired_197_calibration_configs(
    reps_per_assise: int = 8,
    *,
    exp_seed: int = 20260620,
    max_revision_passes: int = 3,
) -> tuple[tuple[CanonicalAssise, GameConfig, GameConfig], ...]:
    """Retourne les paires CRN exactes `(assise, cfg_lot0, cfg_canon0)` sur les 197 assises."""
    plan_l0 = build_plan_lot0_197(
        reps_per_assise=reps_per_assise,
        exp_seed=exp_seed,
        max_revision_passes=max_revision_passes,
    )
    plan_c0 = build_plan_canon0_197(
        reps_per_assise=reps_per_assise,
        exp_seed=exp_seed,
        max_revision_passes=max_revision_passes,
    )
    return tuple((a, cfg_l0, cfg_c0) for (a, cfg_l0), (_, cfg_c0) in zip(plan_l0, plan_c0, strict=True))

