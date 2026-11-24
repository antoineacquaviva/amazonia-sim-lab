"""Étalonnage local PyPy 3.11 sur les 197 assises canoniques (B1 Lot 0 vs B2 Canon 0 + barème Arbres)."""

from __future__ import annotations

import argparse
import json
import math
import multiprocessing
import os
import platform
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import engine.effects  # noqa: F401
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.designs import (
    BENCHMARK_ASSISE_KEYS,
    build_paired_197_calibration_configs,
)
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
)
from engine.state import (
    LISIERE_CONSTRUCTED,
    LISIERE_ROOTED,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker

_END_LABELS: dict[str, str] = {
    CAUSE_TOUR_8: "TOUR_8",
    CAUSE_REVE_RANG_1: "SOMMEIL",
    CAUSE_REVEIL_GARDIENS: "EVEIL",
}


def _run_one_game(
    cfg: GameConfig,
    *,
    bot: str,
    gardien_reve_rollouts: int,
) -> dict[str, Any]:
    state = GameState(cfg)
    trk = TelemetryTracker()
    if bot == "B1":
        over = play_game_b1(state, max_steps=2000, telemetry=trk)
    else:
        over = play_game_b2(
            state,
            max_steps=2000,
            telemetry=trk,
            gardien_reve_rollouts=gardien_reve_rollouts,
        )
    ts = trk.summary()
    acts_dict = dict(ts.tile_activations)
    rooted_tiles: list[str] = [tid_r for _, tid_r, _, _, _ in state.list_rooted_tiles()]
    rooted_set = set(rooted_tiles)
    built_tiles: list[str] = []
    for sl_idx, tid in enumerate(cfg.lisiere_slots):
        st_l, _ = state.get_lisiere_tile_state(sl_idx)
        if (
            st_l in (LISIERE_CONSTRUCTED, LISIERE_ROOTED)
            or tid in rooted_set
            or int(acts_dict.get(tid, 0)) > 0
        ):
            built_tiles.append(tid)

    return {
        "ratio_arbres": float(over.ratio_arbres),
        "score_arbres": int(over.score_arbres),
        "max_arbres": 10 * cfg.n_players,
        "cause_fin": _END_LABELS.get(over.cause_fin, "AUTRE"),
        "tour_fin": int(over.tour_fin),
        "mem_debt_score": int(ts.mem_debt_score),
        "law_stack_max": int(ts.law_stack_max),
        "gardiens_opened_total": int(ts.gardiens_opened_total),
        "gardien_bets_won": int(ts.gardien_bets_won),
        "reves_activated": int(ts.reves_activated),
        "da_parade_classique": int(ts.da_parade_classique),
        "da_piege": int(ts.da_piege),
        "da_parade_avec_insectes": int(ts.da_parade_avec_insectes),
        "da_reve_annulation": int(ts.da_reve_annulation),
        "da_sabotage_revele": int(ts.da_sabotage_revele),
        "da_insecte_bug_deviation": int(ts.da_insecte_bug_deviation),
        "da_arbres_repousse_finale": int(ts.da_arbres_repousse_finale),
        "built_tiles": built_tiles,
        "rooted_tiles": rooted_tiles,
        "tile_activations": acts_dict,
    }


def _worker_chunk(task: tuple[list[tuple[Any, GameConfig, GameConfig, int]], int, int]) -> list[dict[str, Any]]:
    items, gardien_reve_rollouts, b2_lot0_reps = task
    rows: list[dict[str, Any]] = []
    for assise, cfg_l0, cfg_c0, rep_idx in items:
        r_b1 = _run_one_game(cfg_l0, bot="B1", gardien_reve_rollouts=0)
        r_b2 = _run_one_game(cfg_c0, bot="B2", gardien_reve_rollouts=gardien_reve_rollouts)
        r_b2_l0 = (
            _run_one_game(cfg_l0, bot="B2", gardien_reve_rollouts=gardien_reve_rollouts)
            if rep_idx < b2_lot0_reps
            else None
        )
        rows.append(
            {
                "assise_index": int(assise.index),
                "assise_key": str(assise.key),
                "composition_key": str(assise.composition_key),
                "n_players": int(assise.n_players),
                "peuples": list(assise.peuples),
                "lisiere_slots": list(cfg_c0.lisiere_slots),
                "rep": int(rep_idx),
                "b1_lot0": r_b1,
                "b2_canon0": r_b2,
                "b2_lot0": r_b2_l0,
            }
        )
    return rows


def _solve_linear_system(a_mat: list[list[float]], b_vec: list[float]) -> list[float]:
    """Résout A x = b par élimination de Gauss avec pivot partiel (stdlib pure)."""
    n = len(b_vec)
    m = [row[:] + [b_vec[i]] for i, row in enumerate(a_mat)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(m[r][col]))
        if abs(m[piv][col]) < 1e-12:
            return [0.0] * n
        m[col], m[piv] = m[piv], m[col]
        diag = m[col][col]
        for j in range(col, n + 1):
            m[col][j] /= diag
        for r in range(n):
            if r == col:
                continue
            factor = m[r][col]
            if factor == 0.0:
                continue
            for j in range(col, n + 1):
                m[r][j] -= factor * m[col][j]
    return [m[i][n] for i in range(n)]


def _invert_matrix(a_mat: list[list[float]]) -> list[list[float]]:
    """Inverse une petite matrice symétrique définie positive (stdlib pure)."""
    n = len(a_mat)
    aug = [a_mat[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[piv][col]) < 1e-12:
            return [[0.0] * n for _ in range(n)]
        aug[col], aug[piv] = aug[piv], aug[col]
        diag = aug[col][col]
        for j in range(2 * n):
            aug[col][j] /= diag
        for r in range(n):
            if r == col:
                continue
            factor = aug[r][col]
            if factor == 0.0:
                continue
            for j in range(2 * n):
                aug[r][j] -= factor * aug[col][j]
    return [row[n:] for row in aug]


def _estimate_empirical_tree_bareme(
    rows: list[dict[str, Any]],
    *,
    arm_key: str,
    tour8_only: bool = False,
) -> dict[str, Any]:
    """Estime la valeur marginale en Arbres (OLS intra-assise à effets fixes + contrôle durée `tour_fin`)."""
    base_features: list[tuple[str, str]] = [
        ("parade_classique", "da_parade_classique"),
        ("piege_declenche", "da_piege"),
        ("parade_avec_insectes", "da_parade_avec_insectes"),
        ("reve_annulation", "da_reve_annulation"),
        ("sabotage_revele", "da_sabotage_revele"),
        ("insecte_deviation_de", "da_insecte_bug_deviation"),
        ("gardien_ouverture", "gardiens_opened_total"),
        ("tuile_construite", "_built_count"),
        ("enracinement_tuile", "_rooted_count"),
    ]
    if not tour8_only:
        base_features.append(("controle_tour_fin", "tour_fin"))
    features = tuple(base_features)
    k = len(features)

    filtered = [
        r for r in rows if (not tour8_only) or r[arm_key]["cause_fin"] == "TOUR_8"
    ]

    def _feat_vec(rec: dict[str, Any]) -> list[float]:
        out: list[float] = []
        for _, field_k in features:
            if field_k == "_built_count":
                out.append(float(len(rec["built_tiles"])))
            elif field_k == "_rooted_count":
                out.append(float(len(rec["rooted_tiles"])))
            else:
                out.append(float(rec[field_k]))
        return out

    # Centrage intra-assise (effets fixes par assise : élimine tout biais de N ou de composition)
    by_assise: dict[str, list[tuple[float, list[float]]]] = {}
    for row in filtered:
        rec = row[arm_key]
        by_assise.setdefault(row["assise_key"], []).append(
            (float(rec["score_arbres"]), _feat_vec(rec))
        )

    y_centered: list[float] = []
    x_centered: list[list[float]] = []
    raw_means = [0.0] * k
    total_obs = 0
    for grp in by_assise.values():
        m = len(grp)
        if m == 0:
            continue
        mean_y = sum(y for y, _ in grp) / m
        mean_x = [sum(fv[j] for _, fv in grp) / m for j in range(k)]
        for y_v, fv in grp:
            total_obs += 1
            for j in range(k):
                raw_means[j] += fv[j]
            y_centered.append(y_v - mean_y)
            x_centered.append([fv[j] - mean_x[j] for j in range(k)])

    raw_means = [v / max(1, total_obs) for v in raw_means]

    # X'X + lambda*I (légère régularisation 1e-4 pour stabilité numérique)
    xtx = [[0.0] * k for _ in range(k)]
    xty = [0.0] * k
    for y_c, xc in zip(y_centered, x_centered, strict=True):
        for i in range(k):
            xi = xc[i]
            xty[i] += xi * y_c
            for j in range(k):
                xtx[i][j] += xi * xc[j]
    for i in range(k):
        xtx[i][i] += 1e-4

    beta = _solve_linear_system(xtx, xty)
    xtx_inv = _invert_matrix(xtx)

    sse = 0.0
    sst = 0.0
    for y_c, xc in zip(y_centered, x_centered, strict=True):
        pred = sum(beta[j] * xc[j] for j in range(k))
        err = y_c - pred
        sse += err * err
        sst += y_c * y_c

    df = max(1, total_obs - len(by_assise) - k)
    sigma2 = sse / df
    r2_within = 1.0 - (sse / sst) if sst > 1e-12 else 0.0

    # Repousse finale directe (exacte en Arbres)
    mean_repousse = sum(float(r[arm_key]["da_arbres_repousse_finale"]) for r in filtered) / max(1, len(filtered))
    mean_rooted = sum(float(len(r[arm_key]["rooted_tiles"])) for r in filtered) / max(1, len(filtered))
    direct_trees_per_root = (mean_repousse / mean_rooted) if mean_rooted > 1e-9 else 0.0

    items: dict[str, dict[str, float]] = {}
    for idx, (label, _) in enumerate(features):
        se_i = math.sqrt(max(0.0, sigma2 * xtx_inv[idx][idx]))
        items[label] = {
            "marginal_trees_ols": round(beta[idx], 3),
            "se_trees": round(se_i, 3),
            "ci95_low": round(beta[idx] - 1.96 * se_i, 3),
            "ci95_high": round(beta[idx] + 1.96 * se_i, 3),
            "mean_count_per_game": round(raw_means[idx], 3),
        }
    items["repousse_finale_directe_par_enracinement"] = {
        "direct_trees_per_rooted_tile": round(direct_trees_per_root, 3),
        "mean_repousse_arbres_per_game": round(mean_repousse, 3),
        "mean_rooted_tiles_per_game": round(mean_rooted, 3),
    }

    return {
        "arm": arm_key,
        "tour8_only": tour8_only,
        "observations": total_obs,
        "r2_within_assise": round(r2_within, 4),
        "items": items,
    }


def _summarize_arm(recs: list[dict[str, Any]]) -> dict[str, Any]:
    n = max(1, len(recs))
    end_counts = {"TOUR_8": 0, "SOMMEIL": 0, "EVEIL": 0, "AUTRE": 0}
    for r in recs:
        end_counts[r["cause_fin"]] = end_counts.get(r["cause_fin"], 0) + 1
    return {
        "games": len(recs),
        "mean_ratio_arbres": round(sum(r["ratio_arbres"] for r in recs) / n, 4),
        "mean_score_arbres": round(sum(r["score_arbres"] for r in recs) / n, 2),
        "mean_tour_fin": round(sum(r["tour_fin"] for r in recs) / n, 2),
        "endings_pct": {
            k: round(100.0 * v / n, 2) for k, v in end_counts.items() if k != "AUTRE" or v > 0
        },
        "mem_debt_max": max(r["mem_debt_score"] for r in recs) if recs else 0,
        "mem_debt_sum": sum(r["mem_debt_score"] for r in recs),
        "law_stack_max": max(r["law_stack_max"] for r in recs) if recs else 0,
        "mean_built_tiles": round(sum(len(r["built_tiles"]) for r in recs) / n, 2),
        "mean_rooted_tiles": round(sum(len(r["rooted_tiles"]) for r in recs) / n, 2),
    }


def _summarize_slice(rows: list[dict[str, Any]]) -> dict[str, Any]:
    b1_recs = [r["b1_lot0"] for r in rows]
    b2_recs = [r["b2_canon0"] for r in rows]

    # Par assise (pour SE inter-assise) et par composition (pour décompte sur 42 compositions)
    assise_deltas: dict[str, list[float]] = {}
    comp_b1: dict[str, list[float]] = {}
    comp_b2: dict[str, list[float]] = {}
    for r in rows:
        ak = r["assise_key"]
        ck = r["composition_key"]
        r1 = r["b1_lot0"]["ratio_arbres"]
        r2 = r["b2_canon0"]["ratio_arbres"]
        assise_deltas.setdefault(ak, []).append(r2 - r1)
        comp_b1.setdefault(ck, []).append(r1)
        comp_b2.setdefault(ck, []).append(r2)

    assise_means = [sum(v) / len(v) for v in assise_deltas.values()]
    m_a = len(assise_means)
    mean_delta = sum(assise_means) / max(1, m_a)
    if m_a > 1:
        var_a = sum((x - mean_delta) ** 2 for x in assise_means) / (m_a - 1)
        se_a = math.sqrt(var_a / m_a)
    else:
        se_a = 0.0

    comp_wins = sum(
        1
        for ck in comp_b1
        if (sum(comp_b2[ck]) / len(comp_b2[ck])) > (sum(comp_b1[ck]) / len(comp_b1[ck]))
    )
    assise_wins = sum(1 for x in assise_means if x > 0.0)
    mean_delta_trees = sum(
        r["b2_canon0"]["score_arbres"] - r["b1_lot0"]["score_arbres"] for r in rows
    ) / max(1, len(rows))

    # Contrôle B2 Lot 0 (isolation du lift pur des 30 tuiles Canon 0 à bot B2 constant)
    ctrl_rows = [r for r in rows if r["b2_lot0"] is not None]
    ctrl_summary: dict[str, Any] = {}
    if ctrl_rows:
        m_b2_l0 = sum(r["b2_lot0"]["ratio_arbres"] for r in ctrl_rows) / len(ctrl_rows)
        m_b2_c0_sub = sum(r["b2_canon0"]["ratio_arbres"] for r in ctrl_rows) / len(ctrl_rows)
        ctrl_summary = {
            "paired_games": len(ctrl_rows),
            "b2_lot0_mean_ratio": round(m_b2_l0, 4),
            "b2_canon0_matched_mean_ratio": round(m_b2_c0_sub, 4),
            "pure_canon0_lift_at_b2": round(m_b2_c0_sub - m_b2_l0, 4),
        }

    return {
        "assises_count": m_a,
        "compositions_count": len(comp_b1),
        "b1_lot0": _summarize_arm(b1_recs),
        "b2_canon0": _summarize_arm(b2_recs),
        "delta_b2_canon0_minus_b1_lot0": {
            "mean_ratio": round(mean_delta, 4),
            "se_inter_assise": round(se_a, 4),
            "ci95_half": round(1.96 * se_a, 4),
            "mean_trees": round(mean_delta_trees, 2),
            "compositions_b2_gt_b1": comp_wins,
            "compositions_total": len(comp_b1),
            "assises_b2_gt_b1": assise_wins,
            "assises_total": m_a,
        },
        "b2_lot0_control": ctrl_summary,
    }


def _summarize_tiles(rows: list[dict[str, Any]]) -> dict[str, Any]:
    all_30 = (
        [f"G{i}" for i in range(1, 16)]
        + [f"R{i}" for i in range(1, 11)]
        + [f"M{i}" for i in range(1, 6)]
    )
    stats: dict[str, dict[str, Any]] = {
        tid: {
            "eligible_games": 0,
            "built_games": 0,
            "rooted_games": 0,
            "activations_total": 0,
            "deltas_present": [],
            "deltas_built": [],
            "deltas_not_built": [],
            "ctrl_canon0_minus_lot0_present": [],
        }
        for tid in all_30
    }

    for r in rows:
        b1_r = r["b1_lot0"]["ratio_arbres"]
        b2_r = r["b2_canon0"]["ratio_arbres"]
        delta = b2_r - b1_r
        built_set = set(r["b2_canon0"]["built_tiles"])
        rooted_set = set(r["b2_canon0"]["rooted_tiles"])
        acts = r["b2_canon0"]["tile_activations"]
        ctrl_lift = (
            (b2_r - r["b2_lot0"]["ratio_arbres"]) if r["b2_lot0"] is not None else None
        )
        for tid in r["lisiere_slots"]:
            if tid not in stats:
                continue
            st = stats[tid]
            st["eligible_games"] += 1
            st["deltas_present"].append(delta)
            if ctrl_lift is not None:
                st["ctrl_canon0_minus_lot0_present"].append(ctrl_lift)
            if tid in built_set:
                st["built_games"] += 1
                st["deltas_built"].append(delta)
            else:
                st["deltas_not_built"].append(delta)
            if tid in rooted_set:
                st["rooted_games"] += 1
            st["activations_total"] += int(acts.get(tid, 0))

    per_tile: list[dict[str, Any]] = []
    for tid in all_30:
        st = stats[tid]
        elig = max(1, st["eligible_games"])
        built = st["built_games"]
        d_pres = sum(st["deltas_present"]) / elig
        d_built = (
            sum(st["deltas_built"]) / len(st["deltas_built"]) if st["deltas_built"] else 0.0
        )
        d_not = (
            sum(st["deltas_not_built"]) / len(st["deltas_not_built"])
            if st["deltas_not_built"]
            else 0.0
        )
        ctrl_d = (
            sum(st["ctrl_canon0_minus_lot0_present"]) / len(st["ctrl_canon0_minus_lot0_present"])
            if st["ctrl_canon0_minus_lot0_present"]
            else 0.0
        )
        build_rate = built / elig
        act_per_elig = st["activations_total"] / elig
        # Score composite rentabilité : taux de construction * lift net + activations
        profitability_index = round(build_rate * max(0.0, d_built) * 100.0 + act_per_elig * 2.0, 2)
        per_tile.append(
            {
                "tile_id": tid,
                "eligible_games": st["eligible_games"],
                "built_games": built,
                "build_rate": round(build_rate, 4),
                "rooted_games": st["rooted_games"],
                "root_rate": round(st["rooted_games"] / elig, 4),
                "activations_total": st["activations_total"],
                "activations_per_eligible": round(act_per_elig, 3),
                "mean_delta_b2_minus_b1_present": round(d_pres, 4),
                "mean_delta_when_built": round(d_built, 4),
                "mean_delta_when_not_built": round(d_not, 4),
                "build_lift_ratio": round(d_built - d_not, 4),
                "pure_canon0_lift_at_b2_present": round(ctrl_d, 4),
                "profitability_index": profitability_index,
            }
        )

    top_5 = sorted(
        per_tile,
        key=lambda x: (x["build_rate"], x["mean_delta_when_built"], x["activations_per_eligible"]),
        reverse=True,
    )[:5]
    flop_5 = sorted(
        per_tile,
        key=lambda x: (x["build_rate"], x["activations_per_eligible"], x["mean_delta_b2_minus_b1_present"]),
    )[:5]
    return {
        "all_30_tiles": sorted(per_tile, key=lambda x: x["build_rate"], reverse=True),
        "top_5_most_built_profitable": top_5,
        "flop_5_underplayed": flop_5,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Calibration 197 assises Canon 0 vs Lot 0 (PyPy 3.11)")
    parser.add_argument("--reps", type=int, default=8, help="Réplicats CRN appariés par assise (défaut: 8 -> 1576 paires)")
    parser.add_argument("--b2-lot0-reps", type=int, default=2, help="Réplicats contrôle B2 Lot 0 par assise (défaut: 2 -> 394)")
    parser.add_argument("--gardien-reve-rollouts", type=int, default=8, help="Rollouts CRN B2 Gardien/Rêve")
    parser.add_argument("--workers", type=int, default=max(1, os.cpu_count() or 1))
    parser.add_argument("--exp-seed", type=int, default=20260620)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "digests" / "calibration_canon0_v6_2_197.json",
    )
    args = parser.parse_args(argv)

    t0 = time.perf_counter()
    paired = build_paired_197_calibration_configs(
        reps_per_assise=args.reps,
        exp_seed=args.exp_seed,
        max_revision_passes=3,
    )
    items: list[tuple[Any, GameConfig, GameConfig, int]] = []
    for idx, (assise, cfg_l0, cfg_c0) in enumerate(paired):
        rep_idx = idx % args.reps
        items.append((assise, cfg_l0, cfg_c0, rep_idx))

    n_workers = max(1, min(args.workers, len(items)))
    chunk_size = max(1, math.ceil(len(items) / (n_workers * 8)))
    chunks = [
        (items[i : i + chunk_size], args.gardien_reve_rollouts, args.b2_lot0_reps)
        for i in range(0, len(items), chunk_size)
    ]

    all_rows: list[dict[str, Any]] = []
    if n_workers == 1:
        for ch in chunks:
            all_rows.extend(_worker_chunk(ch))
    else:
        with multiprocessing.Pool(processes=n_workers) as pool:
            for done_idx, part in enumerate(pool.imap_unordered(_worker_chunk, chunks), start=1):
                all_rows.extend(part)
                if done_idx % 4 == 0 or done_idx == len(chunks):
                    dt = time.perf_counter() - t0
                    print(
                        f"  [{done_idx}/{len(chunks)} blocs] {len(all_rows)}/{len(items)} paires CRN en {dt:.1f}s",
                        flush=True,
                    )

    elapsed = time.perf_counter() - t0
    by_n: dict[str, Any] = {}
    for n_pl in (3, 4, 5, 6):
        sub = [r for r in all_rows if r["n_players"] == n_pl]
        by_n[f"{n_pl}J"] = _summarize_slice(sub)
    by_n["GLOBAL_197"] = _summarize_slice(all_rows)

    benchmarks: dict[str, Any] = {}
    for bk in BENCHMARK_ASSISE_KEYS:
        sub_b = [r for r in all_rows if r["assise_key"] == bk]
        benchmarks[bk] = _summarize_slice(sub_b)

    digest = {
        "meta": {
            "schema_version": "6.2.0",
            "campaign": "calibration_canon0_v6_2_197",
            "runtime": f"{platform.python_implementation()} {platform.python_version()}",
            "exp_seed": int(args.exp_seed),
            "reps_per_assise": int(args.reps),
            "b2_lot0_control_reps_per_assise": int(args.b2_lot0_reps),
            "gardien_reve_rollouts": int(args.gardien_reve_rollouts),
            "total_assises": 197,
            "total_compositions": 42,
            "games_b1_lot0": len(all_rows),
            "games_b2_canon0": len(all_rows),
            "games_b2_lot0_control": sum(1 for r in all_rows if r["b2_lot0"] is not None),
            "elapsed_seconds": round(elapsed, 2),
        },
        "by_n_players": by_n,
        "benchmarks": benchmarks,
        "empirical_tree_bareme": {
            "b2_canon0": _estimate_empirical_tree_bareme(all_rows, arm_key="b2_canon0"),
            "b2_canon0_tour8_only": _estimate_empirical_tree_bareme(
                all_rows, arm_key="b2_canon0", tour8_only=True
            ),
            "b1_lot0": _estimate_empirical_tree_bareme(all_rows, arm_key="b1_lot0"),
        },
        "tile_leaderboard": _summarize_tiles(all_rows),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(digest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Étalonnage 197 assises terminé en {elapsed:.1f}s -> {args.out}")
    g = digest["by_n_players"]["GLOBAL_197"]
    print(
        f"GLOBAL_197: B1(Lot0)={g['b1_lot0']['mean_ratio_arbres']:.4f} | "
        f"B2(Canon0)={g['b2_canon0']['mean_ratio_arbres']:.4f} | "
        f"Delta={g['delta_b2_canon0_minus_b1_lot0']['mean_ratio']:+.4f} "
        f"({g['delta_b2_canon0_minus_b1_lot0']['compositions_b2_gt_b1']}/42 comp) | "
        f"mem_debt={g['b1_lot0']['mem_debt_max']}/{g['b2_canon0']['mem_debt_max']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
