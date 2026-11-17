"""Worker Cloud PyPy 3.11 stdlib pure pour amazonia-sim-lab (Smoke & Campagne Palier 1)."""

from __future__ import annotations

import argparse
import gzip
import json
import multiprocessing
import os
import platform
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from bots.bot_b0 import play_game_b0
from engine.primitives import CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS, CAUSE_TOUR_8
from engine.state import STATE_BUF_SIZE, GameConfig, GameState

METADATA_TOKEN_URL: str = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/token"
)
BUCKET_NAME: str = "amazonia-sim-runs"
SMOKE_OBJECT_NAME: str = "smoke/shard_00.jsonl.gz"
PALIER1_PREFIX: str = "palier1_baseline"

# Châssis contrastés du Palier 1 :
# 0   : Référence P4_2233 standard
# 1   : P5_22233 standard
# 4   : P4_2233 + Offset_Seuil_Parade = +1
# 5   : P5_22233 + Offset_Seuil_Parade = +1
# 127 : Tous axes alternatifs activés (P5, PAR_DE_M_DESIGNE, Offset +1, ALEATOIRE, DEPASSEMENT, ARRACHE_1_SOUCHE, MUTUALISATION)
PALIER1_CHASSIS_IDS: tuple[int, ...] = (0, 1, 4, 5, 127)

# Blocs en paires miroirs (Cercle, Cercle_Miroir) incluant les 6 cercles de couverture complète
PALIER1_TABLES_BY_N: dict[int, tuple[tuple[str, tuple[str, ...]], ...]] = {
    3: (
        ("M-E-I", ("M", "E", "I")),
        ("I-E-M", ("I", "E", "M")),
        ("M-R-O", ("M", "R", "O")),
        ("O-R-M", ("O", "R", "M")),
        ("H-E-I", ("H", "E", "I")),
        ("I-E-H", ("I", "E", "H")),
    ),
    4: (
        ("M-R-H-I", ("M", "R", "H", "I")),
        ("I-H-R-M", ("I", "H", "R", "M")),
        ("M-O-H-E", ("M", "O", "H", "E")),
        ("E-H-O-M", ("E", "H", "O", "M")),
    ),
    5: (
        ("M-O-E-H-I", ("M", "O", "E", "H", "I")),
        ("I-H-E-O-M", ("I", "H", "E", "O", "M")),
        ("M-R-O-H-I", ("M", "R", "O", "H", "I")),
        ("I-H-O-R-M", ("I", "H", "O", "R", "M")),
    ),
    6: (
        ("M-H-O-I-R-E", ("M", "H", "O", "I", "R", "E")),
        ("E-R-I-O-H-M", ("E", "R", "I", "O", "H", "M")),
        ("M-R-O-H-E-I", ("M", "R", "O", "H", "E", "I")),
        ("I-E-H-O-R-M", ("I", "E", "H", "O", "R", "M")),
    ),
}

CellSpec = tuple[int, int, int, str, tuple[str, ...], int, int, int]


def _fetch_gcp_access_token() -> str:
    req = urllib.request.Request(
        METADATA_TOKEN_URL,
        headers={"Metadata-Flavor": "Google"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return str(payload["access_token"])


def _upload_gcs_bytes(bucket: str, object_name: str, data: bytes, token: str) -> dict[str, Any]:
    encoded_name = urllib.parse.quote(object_name, safe="")
    url = (
        f"https://storage.googleapis.com/upload/storage/v1/b/{bucket}/o"
        f"?uploadType=media&name={encoded_name}"
    )
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/gzip",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return dict(json.loads(resp.read().decode("utf-8")))


def _run_jit_microloop(iterations: int = 1_000_000) -> tuple[float, int]:
    buf = bytearray(STATE_BUF_SIZE)
    t0 = time.perf_counter()
    acc = 0
    for i in range(iterations):
        idx = i % STATE_BUF_SIZE
        val = (buf[idx] + i) & 255
        buf[idx] = val
        acc = (acc + val) & 0xFFFFFFFF
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    return elapsed_ms, acc


def run_smoke_test() -> int:
    elapsed_ms, checksum = _run_jit_microloop(1_000_000)
    record = {
        "status": "SMOKE_OK",
        "python_implementation": platform.python_implementation(),
        "pypy_version": sys.version.replace("\n", " "),
        "iterations": 1_000_000,
        "cpu_ms": round(elapsed_ms, 3),
        "checksum": checksum,
    }
    raw_jsonl = (json.dumps(record, ensure_ascii=False) + "\n").encode("utf-8")
    compressed = gzip.compress(raw_jsonl)

    token = _fetch_gcp_access_token()
    gcs_resp = _upload_gcs_bytes(BUCKET_NAME, SMOKE_OBJECT_NAME, compressed, token)
    print(
        json.dumps(
            {
                "uploaded_to": f"gs://{BUCKET_NAME}/{SMOKE_OBJECT_NAME}",
                "size": gcs_resp.get("size"),
                "record": record,
            },
            ensure_ascii=False,
        )
    )
    return 0


def _quantile_sorted(sorted_vals: list[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    pos = q * (len(sorted_vals) - 1)
    lo = int(pos)
    hi = min(len(sorted_vals) - 1, lo + 1)
    frac = pos - lo
    return sorted_vals[lo] * (1.0 - frac) + sorted_vals[hi] * frac


def build_palier1_cells(total_games: int = 100_000, exp_seed: int = 20261117) -> list[CellSpec]:
    """Construit la grille déterministe exacte de `total_games` parties (50% Mode 1, 50% Mode 2)."""
    assert total_games >= 40 and total_games % 40 == 0, "total_games doit être multiple de 40"
    per_mode_n_chassis = total_games // (2 * 4 * len(PALIER1_CHASSIS_IDS))

    cells: list[CellSpec] = []
    rep_cursor = 0
    for mode in (1, 2):
        for n_players in (3, 4, 5, 6):
            tables = PALIER1_TABLES_BY_N[n_players]
            base_reps = per_mode_n_chassis // len(tables)
            rem_reps = per_mode_n_chassis % len(tables)
            for chassis_id in PALIER1_CHASSIS_IDS:
                for t_idx, (table_id, peuples) in enumerate(tables):
                    n_reps = base_reps + (1 if t_idx < rem_reps else 0)
                    if n_reps <= 0:
                        continue
                    cells.append(
                        (
                            mode,
                            n_players,
                            chassis_id,
                            table_id,
                            peuples,
                            exp_seed,
                            rep_cursor,
                            n_reps,
                        )
                    )
                    rep_cursor += n_reps

    assert rep_cursor == total_games
    return cells


def _simulate_cell(cell: CellSpec) -> dict[str, Any]:
    """Exécute et pré-agrège en RAM une cellule `(mode, n_players, chassis_id, table_id)`."""
    mode, n_players, chassis_id, table_id, peuples, exp_seed, rep_start, n_reps = cell
    t0 = time.perf_counter()

    scores: list[float] = []
    ratios: list[float] = []
    sum_arbres = 0
    sum_sq_arbres = 0.0
    sum_ratio = 0.0
    sum_sq_ratio = 0.0
    sum_tours = 0
    cnt_tour_8 = 0
    cnt_reve = 0
    cnt_reveil = 0
    p_max_val = 4

    for offset in range(n_reps):
        rep_id = rep_start + offset
        cfg = GameConfig.from_chassis_index(
            chassis_id,
            n_players=n_players,
            mode=mode,
            peuples=peuples,
            exp_seed=exp_seed,
            rep_id=rep_id,
            coordonnateur_initial=offset % n_players,
            max_revision_passes=0,
        )
        p_max_val = cfg.p_max
        res = play_game_b0(GameState(cfg), max_steps=2000, chassis_id=chassis_id)

        sc = res.score_arbres
        rt = res.ratio_arbres
        scores.append(float(sc))
        ratios.append(rt)
        sum_arbres += sc
        sum_sq_arbres += float(sc * sc)
        sum_ratio += rt
        sum_sq_ratio += rt * rt
        sum_tours += res.tour_fin

        if res.cause_fin == CAUSE_TOUR_8:
            cnt_tour_8 += 1
        elif res.cause_fin == CAUSE_REVE_RANG_1:
            cnt_reve += 1
        elif res.cause_fin == CAUSE_REVEIL_GARDIENS:
            cnt_reveil += 1

    cpu_sec = time.perf_counter() - t0
    scores.sort()
    ratios.sort()

    return {
        "mode": mode,
        "n_players": n_players,
        "p_max": p_max_val,
        "chassis_id": chassis_id,
        "table_id": table_id,
        "mirror_pair_id": "-".join(sorted([table_id, "-".join(reversed(table_id.split("-")))])),
        "n_games": n_reps,
        "sum_arbres": sum_arbres,
        "sum_sq_arbres": round(sum_sq_arbres, 4),
        "mean_arbres": round(sum_arbres / n_reps, 6),
        "p10_arbres": round(_quantile_sorted(scores, 0.10), 4),
        "p20_arbres": round(_quantile_sorted(scores, 0.20), 4),
        "p50_arbres": round(_quantile_sorted(scores, 0.50), 4),
        "p90_arbres": round(_quantile_sorted(scores, 0.90), 4),
        "sum_ratio_arbres": round(sum_ratio, 6),
        "sum_sq_ratio_arbres": round(sum_sq_ratio, 6),
        "mean_ratio_arbres": round(sum_ratio / n_reps, 6),
        "p10_ratio": round(_quantile_sorted(ratios, 0.10), 6),
        "p20_ratio": round(_quantile_sorted(ratios, 0.20), 6),
        "p50_ratio": round(_quantile_sorted(ratios, 0.50), 6),
        "p90_ratio": round(_quantile_sorted(ratios, 0.90), 6),
        "sum_tours": sum_tours,
        "mean_tours": round(sum_tours / n_reps, 6),
        "count_tour_8": cnt_tour_8,
        "count_reve_rang_1": cnt_reve,
        "count_reveil_gardiens": cnt_reveil,
        "cell_cpu_sec": round(cpu_sec, 4),
    }


def run_campaign_palier1(
    *,
    total_games: int = 100_000,
    task_index: int | None = None,
    task_count: int | None = None,
    workers: int | None = None,
    local_out_dir: str | None = None,
) -> int:
    """Exécute la tranche `task_index / task_count` des 100 000 parties Palier 1 avec multiprocessing."""
    if task_index is None:
        task_index = int(
            os.environ.get("CLOUD_RUN_TASK_INDEX", os.environ.get("TASK_INDEX", "0"))
        )
    if task_count is None:
        task_count = int(
            os.environ.get("CLOUD_RUN_TASK_COUNT", os.environ.get("TASK_COUNT", "1"))
        )
    assert 0 <= task_index < task_count

    all_cells = build_palier1_cells(total_games=total_games)
    my_cells = [cell for idx, cell in enumerate(all_cells) if idx % task_count == task_index]
    n_procs = workers if workers is not None else max(1, os.cpu_count() or 1)

    t0 = time.perf_counter()
    if n_procs > 1 and len(my_cells) > 1:
        with multiprocessing.Pool(processes=min(n_procs, len(my_cells))) as pool:
            records = pool.map(_simulate_cell, my_cells)
    else:
        records = [_simulate_cell(c) for c in my_cells]

    wall_sec = time.perf_counter() - t0
    task_games = sum(int(r["n_games"]) for r in records)
    task_gps = task_games / wall_sec if wall_sec > 0 else 0.0

    for rec in records:
        rec["task_index"] = task_index
        rec["task_count"] = task_count
        rec["task_workers"] = n_procs
        rec["task_games"] = task_games
        rec["task_wall_sec"] = round(wall_sec, 4)
        rec["task_games_per_sec"] = round(task_gps, 2)
        rec["python_impl"] = platform.python_implementation()

    raw_jsonl = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    compressed = gzip.compress(raw_jsonl)
    shard_filename = f"shard_{task_index:02d}.jsonl.gz"

    if local_out_dir is not None:
        out_path = Path(local_out_dir) / shard_filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(compressed)
        dest_uri = str(out_path)
    else:
        object_name = f"{PALIER1_PREFIX}/{shard_filename}"
        token = _fetch_gcp_access_token()
        _upload_gcs_bytes(BUCKET_NAME, object_name, compressed, token)
        dest_uri = f"gs://{BUCKET_NAME}/{object_name}"

    print(
        json.dumps(
            {
                "status": "PALIER1_SHARD_OK",
                "task_index": task_index,
                "task_count": task_count,
                "workers": n_procs,
                "cells": len(records),
                "games": task_games,
                "wall_sec": round(wall_sec, 3),
                "games_per_sec": round(task_gps, 1),
                "dest": dest_uri,
                "compressed_bytes": len(compressed),
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Amazonia Sim Lab PyPy Worker")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Exécute le smoke-test JIT PyPy -> GCS.",
    )
    parser.add_argument(
        "--campaign-palier1",
        action="store_true",
        help="Exécute la campagne baseline Palier 1 (100k parties B0 Modes 1 & 2).",
    )
    parser.add_argument("--total-games", type=int, default=100_000)
    parser.add_argument("--task-index", type=int, default=None)
    parser.add_argument("--task-count", type=int, default=None)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--local-out-dir", type=str, default=None)

    args = parser.parse_args(argv)
    if args.smoke_test:
        return run_smoke_test()
    if args.campaign_palier1:
        return run_campaign_palier1(
            total_games=args.total_games,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
