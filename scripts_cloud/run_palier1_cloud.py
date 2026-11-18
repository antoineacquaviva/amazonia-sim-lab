"""Orchestrateur Cloud Run Jobs & synthèse DuckDB du tir Palier 1 (100 000 parties B0)."""

from __future__ import annotations

import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campaigns.digest_builder import write_digest_and_prompt_files
from campaigns.worker_main import PALIER1_CHASSIS_IDS
from scripts_cloud.publish_digest import publish_campaign_digest
from scripts_cloud.studio_paths import find_gcloud

REGION = "europe-west9"
IMAGE_URI = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
JOB_NAME = "amazonia-palier1"
TASK_COUNT = 10
CPU_PER_TASK = "2"
MEMORY_PER_TASK = "1Gi"
TOTAL_GAMES = 100_000

GCS_PREFIX = "gs://amazonia-sim-runs/palier1_baseline"
LOCAL_RUN_DIR = ROOT / ".tmp_runs" / "palier1_baseline"
LOCAL_SHARDS_DIR = LOCAL_RUN_DIR / "shards"
PARQUET_PATH = LOCAL_RUN_DIR / "palier1_b0_cells.parquet"
DIGEST_PATH = ROOT / "data" / "digests" / "digest_palier1_b0.json"


def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def _query_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    rel = con.sql(sql)
    cols = list(rel.columns)
    return [dict(zip(cols, row, strict=True)) for row in rel.fetchall()]


def synthesize_with_duckdb(job_wall_sec: float) -> dict[str, Any]:
    """Agrège les shards JSONL.gz via DuckDB, archive en Parquet et écrit digest_palier1_b0.json."""
    glob_pattern = (LOCAL_SHARDS_DIR / "shard_*.jsonl.gz").as_posix()
    parquet_posix = PARQUET_PATH.as_posix()

    con = duckdb.connect(":memory:")
    con.execute(
        f"CREATE TABLE cells AS SELECT * FROM read_json_auto('{glob_pattern}')"
    )
    con.execute(f"COPY cells TO '{parquet_posix}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    global_rows = _query_dicts(
        con,
        """
        SELECT
            CAST(SUM(n_games) AS INTEGER) AS total_games,
            COUNT(DISTINCT task_index) AS n_shards,
            COUNT(*) AS n_cells,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 4) AS overall_mean_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 5) AS overall_mean_ratio,
            ROUND(MAX(task_wall_sec), 3) AS max_task_compute_sec,
            ROUND(AVG(task_wall_sec), 3) AS mean_task_compute_sec,
            ROUND(SUM(DISTINCT task_games_per_sec), 1) AS sum_worker_games_per_sec
        FROM cells
        """,
    )
    g_stats = global_rows[0]
    total_games = int(g_stats["total_games"])
    assert total_games == TOTAL_GAMES, f"Total parties inattendu : {total_games} != {TOTAL_GAMES}"

    # Résumé task par task pour sommer proprement les débits des 10 workers
    task_rows = _query_dicts(
        con,
        """
        SELECT
            task_index,
            MAX(task_games) AS games,
            MAX(task_wall_sec) AS compute_sec,
            MAX(task_games_per_sec) AS games_per_sec
        FROM cells
        GROUP BY task_index
        ORDER BY task_index
        """,
    )
    sum_worker_gps = round(sum(float(r["games_per_sec"]) for r in task_rows), 1)
    max_compute_sec = max(float(r["compute_sec"]) for r in task_rows)
    effective_compute_gps = round(total_games / max_compute_sec, 1) if max_compute_sec > 0 else 0.0
    end_to_end_job_gps = round(total_games / job_wall_sec, 1) if job_wall_sec > 0 else 0.0

    by_mode_n = _query_dicts(
        con,
        """
        SELECT
            mode,
            n_players,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(AVG(p20_ratio), 4) AS mean_p20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode, n_players
        ORDER BY mode, n_players
        """,
    )

    by_mode_chassis = _query_dicts(
        con,
        """
        SELECT
            mode,
            chassis_id,
            p_max,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode, chassis_id, p_max
        ORDER BY mode, chassis_id
        """,
    )

    by_mode_summary = _query_dicts(
        con,
        """
        SELECT
            mode,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            CAST(SUM(count_tour_8) AS INTEGER) AS count_tour_8,
            CAST(SUM(count_reve_rang_1) AS INTEGER) AS count_reve_rang_1,
            CAST(SUM(count_reveil_gardiens) AS INTEGER) AS count_reveil_gardiens,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode
        ORDER BY mode
        """,
    )

    mode2_tables = _query_dicts(
        con,
        """
        SELECT
            n_players,
            table_id,
            mirror_pair_id,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        WHERE mode = 2
        GROUP BY n_players, table_id, mirror_pair_id
        ORDER BY n_players, table_id
        """,
    )

    digest: dict[str, Any] = {
        "campaign": "palier1_baseline_b0",
        "generated_at_utc": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cloud_run_job": {
            "job_name": JOB_NAME,
            "region": REGION,
            "image": IMAGE_URI,
            "tasks": TASK_COUNT,
            "cpu_per_task": int(CPU_PER_TASK),
            "memory_per_task": MEMORY_PER_TASK,
            "job_wall_sec_including_scheduling": round(job_wall_sec, 3),
            "max_worker_compute_sec": round(max_compute_sec, 3),
            "mean_worker_compute_sec": g_stats["mean_task_compute_sec"],
            "sum_worker_games_per_sec": sum_worker_gps,
            "effective_cluster_compute_games_per_sec": effective_compute_gps,
            "end_to_end_job_games_per_sec": end_to_end_job_gps,
        },
        "totals": {
            "total_games": total_games,
            "n_shards": g_stats["n_shards"],
            "n_cells": g_stats["n_cells"],
            "parquet_archive": PARQUET_PATH.relative_to(ROOT).as_posix(),
        },
        "by_mode": by_mode_summary,
        "by_mode_and_n_players": by_mode_n,
        "by_mode_and_chassis": by_mode_chassis,
        "mode2_tables": mode2_tables,
        "worker_shards": task_rows,
    }

    digest_path, prompt_path, digest = write_digest_and_prompt_files(
        "palier1_b0",
        digest,
        chassis_ids=PALIER1_CHASSIS_IDS,
        tested_tiles=(),
    )
    encoded = digest_path.read_bytes()

    print("\n=== SYNTHÈSE DUCKDB PALIER 1 (100 000 PARTIES B0) ===")
    con.sql(
        """
        SELECT
            mode,
            n_players AS N,
            CAST(SUM(n_games) AS INTEGER) AS parties,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 2) AS arbres_moy,
            ROUND(SUM(sum_ratio_arbres) * 100.0 / SUM(n_games), 2) AS pct_arbres_sauves,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 2) AS tours_moy,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_r1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_g
        FROM cells
        GROUP BY mode, n_players
        ORDER BY mode, n_players
        """
    ).show()

    print(
        f"Digest écrit : {digest_path.relative_to(ROOT).as_posix()} ({len(encoded)} octets < 35 Ko)"
    )
    print(f"Dossier Gemini : {prompt_path.relative_to(ROOT).as_posix()}")
    print(f"Archive Parquet : {PARQUET_PATH.relative_to(ROOT).as_posix()}")
    con.close()
    return digest


def main() -> int:
    gcloud = find_gcloud()

    # 1. Build & Push de l'image PyPy 3.11 via Cloud Build
    _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])

    # 2. Déploiement du Cloud Run Job (10 tâches parallèles x 2 vCPU, 1Gi, europe-west9)
    _run(
        [
            gcloud,
            "run",
            "jobs",
            "deploy",
            JOB_NAME,
            "--image",
            IMAGE_URI,
            "--region",
            REGION,
            "--tasks",
            str(TASK_COUNT),
            "--parallelism",
            str(TASK_COUNT),
            "--cpu",
            CPU_PER_TASK,
            "--memory",
            MEMORY_PER_TASK,
            "--max-retries",
            "1",
            "--task-timeout",
            "300s",
            f"--args=--campaign-palier1,--total-games={TOTAL_GAMES},--workers={CPU_PER_TASK}",
        ]
    )

    # 3. Exécution synchrone du tir de 100 000 parties sur Cloud Run Jobs
    t_job_start = time.perf_counter()
    _run([gcloud, "run", "jobs", "execute", JOB_NAME, "--region", REGION, "--wait"])
    job_wall_sec = time.perf_counter() - t_job_start
    print(f"Tir Cloud Run terminé en {job_wall_sec:.2f}s murale.")

    # 4. Rapatriement local des shards depuis GCS
    if LOCAL_SHARDS_DIR.exists():
        shutil.rmtree(LOCAL_SHARDS_DIR)
    LOCAL_SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])

    # 5. Agrégation DuckDB, export Parquet & publication auto-portante (Drive + Mobile + Presse-papiers)
    digest = synthesize_with_duckdb(job_wall_sec=job_wall_sec)
    publish_campaign_digest(
        "palier1_b0",
        digest,
        chassis_ids=PALIER1_CHASSIS_IDS,
        tested_tiles=(),
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
