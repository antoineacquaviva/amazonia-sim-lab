"""Accordeur automatique et reproductible des poids `B2Weights` sur graines & cercles disjoints.

100 % stdlib (CPython 3.12 / PyPy 3.11), déterministe via `engine.rng.rand_u64` (zéro `random`).
Optimise `B2Weights` sur un jeu d'entraînement `(cercles_train, graines_train)`, valide sur un
jeu strictement disjoint `(cercles_val, graines_val)` et suit de version en version :
- le score moyen (`mean_ratio`) ;
- le pire quintile (`cvar20` calculée directement via `campaigns.stats_tools.cvar_exact_values`) ;
- le regret décisionnel (`c_prive`, `delta_v_negociation`, `g_unbiased_eval`) via `micro_fork`.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, fields, replace
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import engine.effects  # noqa: F401
from bots.b2_economy import DEFAULT_B2_WEIGHTS, B2Weights
from bots.heuristic_engine import make_b2_scorer, play_game_b2
from campaigns.designs import (
    aggregate_micro_forks,
    balanced_neighbor_mirror_pairs,
    run_micro_fork_on_config,
)
from campaigns.stats_tools import cvar_exact_values
from engine.rng import rand_u64
from engine.state import GameConfig, GameState

__all__ = (
    "build_disjoint_train_val_configs",
    "evaluate_weights_on_configs",
    "perturb_b2_weights",
    "tune_b2_weights",
)

_SRC_TUNER: int = 83
_U64_DIV: float = float(1 << 64)

# Sous-ensemble de poids prioritaires (arbres, route, charge, staging, lisière, furtivité, rêves, gardiens)
_DEFAULT_TUNABLE_FIELDS: tuple[str, ...] = (
    "route_penalty_trees",
    "charge_penalty_early",
    "charge_penalty_mid",
    "charge_penalty_late",
    "insect_saved_trees",
    "nid_base_trees",
    "coop_gap2_share",
    "coop_gap2_held_share",
    "lisiere_complete_base",
    "lisiere_open_covered_base",
    "furt_piege_complete_base",
    "furt_sab_complete_base",
    "furt_sab_waste_penalty",
    "reve_base_trees",
    "eveil_finish_trees",
    "eveil_progress_trees",
    "gardien_mode4_probable_trees",
    "gardien_mode4_face1_bonus",
)


def build_disjoint_train_val_configs(
    *,
    mode: int = 2,
    n_players_list: tuple[int, ...] = (4,),
    pairs_per_split: int = 2,
    reps_per_table: int = 2,
    exp_seed: int = 20261123,
) -> tuple[list[GameConfig], list[GameConfig]]:
    """Construit deux ensembles strictement disjoints de cercles ET de graines (train vs val)."""
    train_cfgs: list[GameConfig] = []
    val_cfgs: list[GameConfig] = []
    min_anim = 1 if mode >= 2 else 0

    for n_pl in n_players_list:
        all_pairs = balanced_neighbor_mirror_pairs(
            n_pl, min_animaux_sauvages=min_anim, exp_seed=exp_seed
        )
        n_avail = len(all_pairs)
        k_train = min(pairs_per_split, max(1, n_avail // 2))
        k_val = min(pairs_per_split, max(1, n_avail - k_train))

        train_pairs = all_pairs[:k_train]
        val_pairs = all_pairs[k_train : k_train + k_val]

        t_idx = 0
        for _id_a, c_a, _id_b, c_b in train_pairs:
            for circle in (c_a, c_b):
                for rep in range(reps_per_table):
                    train_cfgs.append(
                        GameConfig(
                            n_players=n_pl,
                            mode=mode,
                            peuples=circle,
                            exp_seed=exp_seed + n_pl * 1000 + t_idx,
                            rep_id=rep,
                        )
                    )
                t_idx += 1

        v_idx = 0
        for _id_a, c_a, _id_b, c_b in val_pairs:
            for circle in (c_a, c_b):
                for rep in range(reps_per_table):
                    val_cfgs.append(
                        GameConfig(
                            n_players=n_pl,
                            mode=mode,
                            peuples=circle,
                            exp_seed=exp_seed + 100_000 + n_pl * 1000 + v_idx,
                            rep_id=1000 + rep,
                        )
                    )
                v_idx += 1

    return train_cfgs, val_cfgs


def evaluate_weights_on_configs(
    weights: B2Weights,
    configs: list[GameConfig],
    *,
    cvar_weight: float = 0.25,
    gardien_reve_rollouts: int = 0,
    with_regret_forks: int = 0,
) -> dict[str, Any]:
    """Évalue un jeu `B2Weights` sur `configs` : moyenne, CVaR_20%, objectif et regret micro-fork."""
    ratios: list[float] = []
    for cfg in configs:
        over = play_game_b2(
            GameState(cfg),
            weights=weights,
            gardien_reve_rollouts=gardien_reve_rollouts,
        )
        ratios.append(over.ratio_arbres)

    n_games = len(ratios)
    mean_r = sum(ratios) / float(n_games) if n_games > 0 else 0.0
    cvar20 = cvar_exact_values(ratios, alpha=0.20) if n_games > 0 else 0.0
    objective = (1.0 - cvar_weight) * mean_r + cvar_weight * cvar20

    regret_summary: dict[str, float | int] | None = None
    if with_regret_forks > 0 and configs:
        # Utiliser micro_fork (v6.1) pour suivre le regret décisionnel (c_prive, delta_v, g_unbiased)
        from bots import heuristic_engine as he_mod

        prev_scorer = he_mod.score_target_b2
        try:
            he_mod.score_target_b2 = make_b2_scorer(weights)
            records = []
            for cfg_mf in configs[:with_regret_forks]:
                rec = run_micro_fork_on_config(
                    cfg_mf,
                    target_tour=2,
                    is_b2=True,
                    n_selection_rollouts=2,
                    n_eval_rollouts=3,
                )
                if rec is not None:
                    records.append(rec)
            agg = aggregate_micro_forks(records)
            regret_summary = {
                "n_anchors": agg.n_anchors,
                "mean_c_prive": agg.mean_c_prive,
                "mean_delta_v_negociation": agg.mean_delta_v_negociation,
                "mean_g_unbiased_eval": agg.mean_g_unbiased_eval,
                "mean_rho_delta": agg.mean_rho_delta,
            }
        finally:
            he_mod.score_target_b2 = prev_scorer

    return {
        "n_games": n_games,
        "mean_ratio": mean_r,
        "cvar20": cvar20,
        "objective": objective,
        "regret": regret_summary,
    }


def perturb_b2_weights(
    base: B2Weights,
    *,
    step_idx: int,
    seed: int,
    scale: float = 0.12,
    tunable_fields: tuple[str, ...] = _DEFAULT_TUNABLE_FIELDS,
    n_coords: int = 3,
) -> B2Weights:
    """Génère une perturbation multiplicative déterministe de `n_coords` poids dans `B2Weights`."""
    valid_names = {f.name for f in fields(B2Weights)}
    pool = [name for name in tunable_fields if name in valid_names]
    if not pool:
        return base

    updates: dict[str, float] = {}
    k_pick = min(max(1, n_coords), len(pool))
    for j in range(k_pick):
        u_idx = int(rand_u64(seed, step_idx, _SRC_TUNER, 1, j, 0) % len(pool))
        fname = pool[u_idx]
        u_val = float(rand_u64(seed, step_idx, _SRC_TUNER, 2, j, 0)) / _U64_DIV
        # Facteur multiplicatif symétrique dans [1 - scale, 1 + scale]
        mult = 1.0 + scale * (2.0 * u_val - 1.0)
        cur_val = float(getattr(base, fname))
        new_val = max(0.02, round(cur_val * mult, 4))
        updates[fname] = new_val

    return replace(base, **updates)


def tune_b2_weights(
    *,
    mode: int = 2,
    n_players_list: tuple[int, ...] = (4,),
    pairs_per_split: int = 2,
    reps_per_table: int = 2,
    iterations: int = 6,
    exp_seed: int = 20261123,
    init_scale: float = 0.12,
    cvar_weight: float = 0.25,
    gardien_reve_rollouts: int = 0,
    regret_forks: int = 2,
    initial_weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> dict[str, Any]:
    """Recherche adaptative reproductible (1+1)-ES sur split disjoint (train/val) avec suivi de regret."""
    train_cfgs, val_cfgs = build_disjoint_train_val_configs(
        mode=mode,
        n_players_list=n_players_list,
        pairs_per_split=pairs_per_split,
        reps_per_table=reps_per_table,
        exp_seed=exp_seed,
    )

    train_circles = sorted({"-".join(c.peuples) for c in train_cfgs})
    val_circles = sorted({"-".join(c.peuples) for c in val_cfgs})
    assert not (set(train_circles) & set(val_circles)), "Fuite train/val sur les cercles !"
    assert not ({c.exp_seed for c in train_cfgs} & {c.exp_seed for c in val_cfgs}), (
        "Fuite train/val sur les graines !"
    )

    base_train = evaluate_weights_on_configs(
        initial_weights,
        train_cfgs,
        cvar_weight=cvar_weight,
        gardien_reve_rollouts=gardien_reve_rollouts,
    )
    base_val = evaluate_weights_on_configs(
        initial_weights,
        val_cfgs,
        cvar_weight=cvar_weight,
        gardien_reve_rollouts=gardien_reve_rollouts,
        with_regret_forks=regret_forks,
    )

    best_weights = initial_weights
    best_train = base_train
    scale = init_scale
    history: list[dict[str, Any]] = []

    for it in range(1, iterations + 1):
        cand_weights = perturb_b2_weights(
            best_weights, step_idx=it, seed=exp_seed, scale=scale
        )
        cand_train = evaluate_weights_on_configs(
            cand_weights,
            train_cfgs,
            cvar_weight=cvar_weight,
            gardien_reve_rollouts=gardien_reve_rollouts,
        )
        accepted = cand_train["objective"] > best_train["objective"] + 1e-6
        if accepted:
            best_weights = cand_weights
            best_train = cand_train
            scale = min(0.25, scale * 1.15)
        else:
            scale = max(0.03, scale * 0.85)
        history.append(
            {
                "iteration": it,
                "accepted": accepted,
                "scale": round(scale, 4),
                "cand_train_objective": round(cand_train["objective"], 6),
                "best_train_objective": round(best_train["objective"], 6),
            }
        )

    best_val = evaluate_weights_on_configs(
        best_weights,
        val_cfgs,
        cvar_weight=cvar_weight,
        gardien_reve_rollouts=gardien_reve_rollouts,
        with_regret_forks=regret_forks,
    )

    return {
        "schema_version": "b2_tuner_1.0",
        "mode": mode,
        "n_players_list": list(n_players_list),
        "exp_seed": exp_seed,
        "param_count": B2Weights.param_count(),
        "train_circles": train_circles,
        "val_circles": val_circles,
        "baseline_train": base_train,
        "baseline_val": base_val,
        "best_train": best_train,
        "best_val": best_val,
        "val_delta_mean_ratio": best_val["mean_ratio"] - base_val["mean_ratio"],
        "val_delta_cvar20": best_val["cvar20"] - base_val["cvar20"],
        "history": history,
        "best_weights": asdict(best_weights),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Accordeur automatique déterministe de B2Weights (split train/val disjoint + regret micro-fork)."
    )
    parser.add_argument("--mode", type=int, default=2, choices=(2, 4))
    parser.add_argument("--n-players", type=int, nargs="+", default=[4])
    parser.add_argument("--pairs-per-split", type=int, default=2)
    parser.add_argument("--reps-per-table", type=int, default=2)
    parser.add_argument("--iterations", type=int, default=8)
    parser.add_argument("--seed", type=int, default=20261123)
    parser.add_argument("--regret-forks", type=int, default=2)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)

    report = tune_b2_weights(
        mode=args.mode,
        n_players_list=tuple(args.n_players),
        pairs_per_split=args.pairs_per_split,
        reps_per_table=args.reps_per_table,
        iterations=args.iterations,
        exp_seed=args.seed,
        regret_forks=args.regret_forks,
    )
    text = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output is not None:
        args.output.write_text(text + "\n", encoding="utf-8")
        print(f"Rapport d'accordage écrit : {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
