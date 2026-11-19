"""Commande unique de bout en bout pour exécuter un manifeste `campaigns/<nom>.json`
sur Cloud Run Jobs / Cloud Batch (`europe-west9`), agréger via DuckDB, publier le bilan
dans Amazonia Doc Studio (`docs/digests/`) et pousser sur `origin main`.

Usage :
    uv run python run_campaign.py campaigns/<nom>.json
    uv run python run_campaign.py campaigns/<nom>.json --build
    uv run python run_campaign.py campaigns/<nom>.json --backend batch
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

ROOT: Path = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campaigns.digest_builder import write_digest_and_prompt_files
from campaigns.worker_main import resolve_manifest_plan
from scripts_cloud.studio_paths import find_gcloud

REGION: str = "europe-west9"
BUCKET_NAME: str = "amazonia-sim-runs"
IMAGE_URI: str = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
CLOUD_RUN_JOB_NAME: str = "amazonia-campaign"
BATCH_THRESHOLD_GAMES: int = 50_000
DOCS_DIGESTS_DIR: Path = ROOT / "docs" / "digests"
DOCS_DIGESTS_INDEX: Path = DOCS_DIGESTS_DIR / "index.json"


def _run(cmd: list[str], *, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print(f"$ {' '.join(cmd)}", flush=True)
    return subprocess.run(
        cmd,
        cwd=ROOT,
        check=check,
        text=True,
        capture_output=capture,
    )


def _query_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    rel = con.sql(sql)
    cols = list(rel.columns)
    return [dict(zip(cols, row, strict=True)) for row in rel.fetchall()]


def _sanitize_gcp_name(raw: str, max_len: int = 40) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", raw.strip().lower()).strip("-")
    if not cleaned or not cleaned[0].isalpha():
        cleaned = f"c-{cleaned}" if cleaned else "campaign"
    return cleaned[:max_len].rstrip("-")


def _auto_task_count(n_units: int, total_games: int, backend: str) -> int:
    if n_units <= 1 or total_games <= 32:
        return 1
    if backend == "batch":
        return min(n_units, max(2, min(16, (total_games + 1999) // 2000)))
    return min(n_units, max(1, min(10, (total_games + 499) // 500)))


def _run_cloud_run_job(
    gcloud: str,
    *,
    manifest_gcs_uri: str,
    gcs_prefix: str,
    tasks: int,
    cpu: str,
    memory: str,
    timeout_sec: int,
) -> tuple[str, float]:
    args_value = (
        f"--campaign-manifest={manifest_gcs_uri},"
        f"--gcs-prefix={gcs_prefix},"
        f"--workers={cpu}"
    )
    _run(
        [
            gcloud,
            "run",
            "jobs",
            "deploy",
            CLOUD_RUN_JOB_NAME,
            "--image",
            IMAGE_URI,
            "--region",
            REGION,
            "--tasks",
            str(tasks),
            "--parallelism",
            str(tasks),
            "--cpu",
            cpu,
            "--memory",
            memory,
            "--max-retries",
            "1",
            "--task-timeout",
            f"{timeout_sec}s",
            f"--args={args_value}",
        ]
    )
    t0 = time.perf_counter()
    _run(
        [
            gcloud,
            "run",
            "jobs",
            "execute",
            CLOUD_RUN_JOB_NAME,
            "--region",
            REGION,
            "--wait",
        ]
    )
    wall_sec = time.perf_counter() - t0
    return CLOUD_RUN_JOB_NAME, wall_sec


def _run_cloud_batch_job(
    gcloud: str,
    *,
    campaign_name: str,
    manifest_gcs_uri: str,
    gcs_prefix: str,
    tasks: int,
    timeout_sec: int,
    run_dir: Path,
) -> tuple[str, float]:
    ts = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    job_name = f"amazonia-{_sanitize_gcp_name(campaign_name, max_len=28)}-{ts}"
    batch_spec: dict[str, Any] = {
        "taskGroups": [
            {
                "taskSpec": {
                    "runnables": [
                        {
                            "container": {
                                "imageUri": IMAGE_URI,
                                "commands": [
                                    f"--campaign-manifest={manifest_gcs_uri}",
                                    f"--gcs-prefix={gcs_prefix}",
                                    "--workers=4",
                                ],
                            }
                        }
                    ],
                    "computeResource": {"cpuMilli": 4000, "memoryMib": 4096},
                    "maxRetryCount": 2,
                    "maxRunDuration": f"{timeout_sec}s",
                },
                "taskCount": tasks,
                "parallelism": tasks,
            }
        ],
        "allocationPolicy": {
            "instances": [
                {
                    "policy": {
                        "machineType": "c3d-highcpu-4",
                        "provisioningModel": "SPOT",
                    }
                }
            ]
        },
        "logsPolicy": {"destination": "CLOUD_LOGGING"},
    }
    spec_path = run_dir / "batch_job.json"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text(json.dumps(batch_spec, indent=2) + "\n", encoding="utf-8")

    t0 = time.perf_counter()
    _run(
        [
            gcloud,
            "batch",
            "jobs",
            "submit",
            job_name,
            "--location",
            REGION,
            "--config",
            str(spec_path),
        ]
    )

    while True:
        proc = _run(
            [
                gcloud,
                "batch",
                "jobs",
                "describe",
                job_name,
                "--location",
                REGION,
                "--format=value(status.state)",
            ],
            capture=True,
        )
        state = proc.stdout.strip().upper()
        print(f"Cloud Batch [{job_name}] état : {state}", flush=True)
        if state == "SUCCEEDED":
            break
        if state in ("FAILED", "DELETION_IN_PROGRESS"):
            raise RuntimeError(f"Le job Cloud Batch {job_name} a échoué (état={state}).")
        time.sleep(10)

    wall_sec = time.perf_counter() - t0
    return job_name, wall_sec


def aggregate_campaign_duckdb(
    *,
    manifest: dict[str, Any],
    plan: dict[str, Any],
    shards_dir: Path,
    parquet_path: Path,
    backend: str,
    job_name: str,
    tasks: int,
    job_wall_sec: float,
) -> tuple[Path, Path, dict[str, Any]]:
    """Agrège les shards JSONL.gz via DuckDB, archive Parquet et écrit le digest auto-portant."""
    campaign_name = str(plan["campaign_name"])
    glob_pattern = (shards_dir / "shard_*.jsonl.gz").as_posix()
    parquet_posix = parquet_path.as_posix()

    con = duckdb.connect(":memory:")
    con.execute(f"CREATE TABLE cells AS SELECT * FROM read_json_auto('{glob_pattern}')")
    con.execute(f"COPY cells TO '{parquet_posix}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    g_stats = _query_dicts(
        con,
        """
        SELECT
            CAST(SUM(n_games) AS INTEGER) AS total_games,
            COUNT(DISTINCT task_index) AS n_shards,
            COUNT(*) AS n_cells,
            COUNT(DISTINCT config_id) AS n_configurations,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(count_arbres_pos) * 1.0 / SUM(n_games), 4) AS survival_rate,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens,
            ROUND(SUM(sum_mem_debt) * 1.0 / SUM(n_games), 3) AS mean_mem_debt,
            ROUND(SUM(sum_law_mean) / SUM(n_games), 3) AS mean_active_laws,
            CAST(MAX(max_law_max) AS INTEGER) AS max_active_laws,
            ROUND(SUM(sum_fiddliness) / SUM(n_games), 3) AS mean_fiddliness_ops,
            ROUND(SUM(sum_cascade_sweeps) * 1.0 / SUM(n_games), 3) AS mean_cascade_sweeps
        FROM cells
        """,
    )[0]

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
    total_games = int(g_stats["total_games"])
    max_compute_sec = max((float(r["compute_sec"]) for r in task_rows), default=0.0)
    sum_worker_gps = round(sum(float(r["games_per_sec"]) for r in task_rows), 1)
    eff_gps = round(total_games / max_compute_sec, 1) if max_compute_sec > 0 else 0.0

    by_mode = _query_dicts(
        con,
        """
        SELECT
            mode,
            bot,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode, bot
        ORDER BY mode, bot
        """,
    )

    by_n_players = _query_dicts(
        con,
        """
        SELECT
            n_players,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY n_players
        ORDER BY n_players
        """,
    )

    by_chassis = _query_dicts(
        con,
        """
        SELECT
            chassis_id,
            p_max,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours
        FROM cells
        GROUP BY chassis_id, p_max
        ORDER BY mean_ratio_arbres DESC, chassis_id ASC
        LIMIT 24
        """,
    )

    by_variant = _query_dicts(
        con,
        """
        SELECT
            variant_id,
            compared_slots_json,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY variant_id, compared_slots_json
        ORDER BY mean_ratio_arbres DESC, variant_id ASC
        """,
    )

    # Agrégation directe par (slot, profil) pour affichage dans Amazonia Doc Studio (tile_metrics)
    tile_acc: dict[str, dict[str, Any]] = {}
    for row in by_variant:
        comp_map: dict[str, str] = json.loads(str(row["compared_slots_json"]))
        ng = int(row["n_games"])
        mr = float(row["mean_ratio_arbres"])
        cv = float(row["cvar20_ratio"])
        for slot_id, prof in comp_map.items():
            tok = f"{slot_id}:{prof}"
            if tok not in tile_acc:
                tile_acc[tok] = {
                    "slot": slot_id,
                    "profile": prof,
                    "n_games": 0,
                    "weighted_ratio": 0.0,
                    "weighted_cvar20": 0.0,
                }
            tile_acc[tok]["n_games"] += ng
            tile_acc[tok]["weighted_ratio"] += mr * ng
            tile_acc[tok]["weighted_cvar20"] += cv * ng

    tile_metrics: dict[str, dict[str, Any]] = {}
    for tok, acc in sorted(tile_acc.items()):
        ng = int(acc["n_games"])
        tile_metrics[tok] = {
            "slot": acc["slot"],
            "profile": acc["profile"],
            "n_games": ng,
            "mean_ratio_arbres": round(acc["weighted_ratio"] / ng, 4) if ng > 0 else 0.0,
            "cvar20": round(acc["weighted_cvar20"] / ng, 4) if ng > 0 else 0.0,
        }

    by_variant_clean = [
        {k: v for k, v in row.items() if k != "compared_slots_json"}
        for row in by_variant[:24]
    ]

    tested_tiles: tuple[tuple[str, str], ...] = tuple(plan["tested_tiles"])
    chassis_ids: tuple[int, ...] = tuple(plan["chassis_ids"])
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    digest_payload: dict[str, Any] = {
        "campaign": campaign_name,
        "description": str(manifest.get("description", "")).strip(),
        "generated_at_utc": generated_at,
        "execution": {
            "backend": backend,
            "region": REGION,
            "job_name": job_name,
            "image": IMAGE_URI,
            "tasks": tasks,
            "job_wall_sec": round(job_wall_sec, 3),
            "max_worker_compute_sec": round(max_compute_sec, 3),
            "sum_worker_games_per_sec": sum_worker_gps,
            "effective_cluster_games_per_sec": eff_gps,
        },
        "totals": {
            "total_games": total_games,
            "n_shards": int(g_stats["n_shards"]),
            "n_cells": int(g_stats["n_cells"]),
            "n_configurations": int(g_stats["n_configurations"]),
            "mean_score_arbres": g_stats["mean_score_arbres"],
            "mean_ratio_arbres": g_stats["mean_ratio_arbres"],
            "cvar20_ratio": g_stats["cvar20_ratio"],
            "survival_rate": g_stats["survival_rate"],
            "mean_tours": g_stats["mean_tours"],
            "pct_tour_8": g_stats["pct_tour_8"],
            "pct_reve_rang_1": g_stats["pct_reve_rang_1"],
            "pct_reveil_gardiens": g_stats["pct_reveil_gardiens"],
            "tested_tiles": [f"{s}:{p}" for s, p in tested_tiles],
            "parquet_archive": parquet_path.relative_to(ROOT).as_posix(),
        },
        "telemetry": {
            "mean_mem_debt": g_stats["mean_mem_debt"],
            "mean_active_laws": g_stats["mean_active_laws"],
            "max_active_laws": g_stats["max_active_laws"],
            "mean_fiddliness_ops": g_stats["mean_fiddliness_ops"],
            "mean_cascade_sweeps": g_stats["mean_cascade_sweeps"],
        },
        "by_mode": by_mode,
        "by_n_players": by_n_players,
        "by_chassis": by_chassis,
        "by_variant": by_variant_clean,
        "tile_metrics": tile_metrics,
    }

    digest_path, prompt_path, final_digest = write_digest_and_prompt_files(
        campaign_name,
        digest_payload,
        chassis_ids=chassis_ids[:8],
        tested_tiles=tested_tiles,
    )

    print(f"\n=== SYNTHÈSE DUCKDB — {campaign_name} ({total_games} parties) ===")
    con.sql(
        """
        SELECT
            n_players AS N,
            chassis_id AS chassis,
            variant_id AS variante,
            CAST(SUM(n_games) AS INTEGER) AS parties,
            ROUND(SUM(sum_ratio_arbres) * 100.0 / SUM(n_games), 2) AS pct_arbres,
            ROUND(SUM(cvar20_ratio * n_games) * 100.0 / SUM(n_games), 2) AS pct_cvar20,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 2) AS tours_moy
        FROM cells
        GROUP BY n_players, chassis_id, variant_id
        ORDER BY n_players, chassis_id, variant_id
        """
    ).show()
    con.close()
    return digest_path, prompt_path, final_digest


def publish_to_studio_digests(
    *,
    campaign_name: str,
    digest_path: Path,
    digest: dict[str, Any],
    manifest: dict[str, Any],
) -> tuple[Path, Path]:
    """Copie `digest_<nom>.json` dans `docs/digests/` et met à jour `docs/digests/index.json`."""
    DOCS_DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    target_digest_path = DOCS_DIGESTS_DIR / digest_path.name
    shutil.copyfile(digest_path, target_digest_path)

    if DOCS_DIGESTS_INDEX.exists():
        index_data = json.loads(DOCS_DIGESTS_INDEX.read_text(encoding="utf-8"))
        existing = list(index_data.get("digests", []))
    else:
        index_data = {"schema_version": "1.0", "digests": []}
        existing = []

    total_games = int(digest.get("totals", {}).get("total_games", 0))
    desc = str(manifest.get("description", "")).strip()
    base_label = desc if desc else campaign_name
    label = f"{base_label} ({total_games} parties)"

    new_entry: dict[str, Any] = {
        "id": campaign_name,
        "label": label,
        "file": target_digest_path.name,
        "campaign": campaign_name,
        "generated_at_utc": str(digest.get("generated_at_utc", "")),
        "total_games": total_games,
    }

    filtered = [
        item
        for item in existing
        if item.get("id") != campaign_name and item.get("file") != target_digest_path.name
    ]
    index_data["schema_version"] = str(index_data.get("schema_version", "1.0"))
    index_data["digests"] = [new_entry, *filtered]

    DOCS_DIGESTS_INDEX.write_text(
        json.dumps(index_data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return target_digest_path, DOCS_DIGESTS_INDEX


def git_commit_and_push(
    *,
    campaign_name: str,
    total_games: int,
    paths_to_stage: list[Path],
) -> None:
    """Exécute `git add`, `git commit` et `git push origin main` sur les livrables de campagne."""
    rel_paths: list[str] = []
    for p in paths_to_stage:
        resolved = p.resolve()
        try:
            rel = resolved.relative_to(ROOT.resolve()).as_posix()
            if rel not in rel_paths:
                rel_paths.append(rel)
        except ValueError:
            continue

    _run(["git", "add", *rel_paths])
    diff_check = _run(["git", "diff", "--cached", "--quiet"], check=False)
    if diff_check.returncode == 0:
        print("Aucun changement à committer dans Git.")
        return

    commit_msg = f"chore(campaign): publier bilan {campaign_name} ({total_games} parties)"
    _run(["git", "commit", "-m", commit_msg])
    _run(["git", "push", "origin", "main"])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Exécute un manifeste campaigns/<nom>.json sur GCP -> DuckDB -> Studio -> GitHub Pages."
    )
    parser.add_argument(
        "manifest",
        type=str,
        help="Chemin vers le manifeste JSON de campagne (ex: campaigns/micro_validation.json).",
    )
    parser.add_argument(
        "--backend",
        choices=("auto", "cloudrun", "batch"),
        default="auto",
        help="Moteur GCP europe-west9 : auto (<=50k cloudrun, >50k batch), cloudrun ou batch.",
    )
    parser.add_argument(
        "--tasks",
        type=int,
        default=None,
        help="Nombre de tâches parallèles Cloud (calculé automatiquement si omis).",
    )
    parser.add_argument("--cpu", type=str, default="2", help="vCPU par tâche Cloud Run (défaut: 2).")
    parser.add_argument("--memory", type=str, default="1Gi", help="Mémoire par tâche Cloud Run (défaut: 1Gi).")
    parser.add_argument(
        "--timeout",
        type=int,
        default=600,
        help="Timeout max par tâche en secondes (défaut: 600).",
    )
    parser.add_argument(
        "--build",
        action="store_true",
        help="Reconstruit et pousse l'image worker PyPy via Cloud Build avant exécution.",
    )
    parser.add_argument(
        "--skip-git-push",
        action="store_true",
        help="N'exécute pas git add/commit/push (utile pour test à blanc).",
    )
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = (ROOT / manifest_path).resolve()
    if not manifest_path.exists():
        raise FileNotFoundError(f"Manifeste introuvable : {manifest_path}")

    manifest: dict[str, Any] = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not manifest.get("campaign_name"):
        manifest["campaign_name"] = manifest_path.stem
    plan = resolve_manifest_plan(manifest)
    campaign_name = str(plan["campaign_name"])
    total_games_planned = int(plan["total_games"])
    n_units = len(plan["units"])

    backend = (
        ("batch" if total_games_planned > BATCH_THRESHOLD_GAMES else "cloudrun")
        if args.backend == "auto"
        else str(args.backend)
    )
    tasks = (
        max(1, min(int(args.tasks), n_units))
        if args.tasks is not None
        else _auto_task_count(n_units, total_games_planned, backend)
    )

    print(
        f"=== Campagne '{campaign_name}' : {total_games_planned} parties "
        f"({plan['total_configurations']} configs, {n_units} unités) | "
        f"backend={backend} ({REGION}, {tasks} tâche(s)) ===",
        flush=True,
    )

    gcloud = find_gcloud()
    gcs_prefix = f"campaigns/{campaign_name}"
    manifest_gcs_uri = f"gs://{BUCKET_NAME}/{gcs_prefix}/manifest.json"
    shards_gcs_glob = f"gs://{BUCKET_NAME}/{gcs_prefix}/shard_*.jsonl.gz"

    # 1. Optionnel : build & push de l'image PyPy via Cloud Build
    if args.build:
        _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])

    # 2. Nettoyage d'éventuels anciens shards du même nom + upload du manifeste sur GCS
    _run([gcloud, "storage", "rm", shards_gcs_glob], check=False)
    _run([gcloud, "storage", "cp", str(manifest_path), manifest_gcs_uri])

    # 3. Exécution Cloud Run Jobs ou Cloud Batch (europe-west9) et attente synchrone
    run_dir = ROOT / ".tmp_runs" / "campaigns" / campaign_name
    shards_dir = run_dir / "shards"
    parquet_path = run_dir / "cells.parquet"

    if backend == "batch":
        job_name, job_wall_sec = _run_cloud_batch_job(
            gcloud,
            campaign_name=campaign_name,
            manifest_gcs_uri=manifest_gcs_uri,
            gcs_prefix=gcs_prefix,
            tasks=tasks,
            timeout_sec=int(args.timeout),
            run_dir=run_dir,
        )
    else:
        job_name, job_wall_sec = _run_cloud_run_job(
            gcloud,
            manifest_gcs_uri=manifest_gcs_uri,
            gcs_prefix=gcs_prefix,
            tasks=tasks,
            cpu=str(args.cpu),
            memory=str(args.memory),
            timeout_sec=int(args.timeout),
        )
    print(f"Calcul Cloud ({backend}/{job_name}) terminé en {job_wall_sec:.2f}s murale.", flush=True)

    # 4. Rapatriement local des shards depuis gs://amazonia-sim-runs
    if shards_dir.exists():
        shutil.rmtree(shards_dir)
    shards_dir.mkdir(parents=True, exist_ok=True)
    _run([gcloud, "storage", "cp", shards_gcs_glob, str(shards_dir)])

    # 5. Agrégation DuckDB + génération digest_<nom>.json auto-portant
    digest_path, prompt_path, final_digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        backend=backend,
        job_name=job_name,
        tasks=tasks,
        job_wall_sec=job_wall_sec,
    )
    print(f"Digest généré : {digest_path.relative_to(ROOT).as_posix()} ({digest_path.stat().st_size} octets)")

    # 6. Publication dans docs/digests/ et mise à jour de docs/digests/index.json
    studio_digest_path, studio_index_path = publish_to_studio_digests(
        campaign_name=campaign_name,
        digest_path=digest_path,
        digest=final_digest,
        manifest=manifest,
    )
    print(f"Publié dans le Studio : {studio_digest_path.relative_to(ROOT).as_posix()}")
    print(f"Index Studio mis à jour : {studio_index_path.relative_to(ROOT).as_posix()}")

    # 7. Git add / commit / push origin main
    if not args.skip_git_push:
        git_commit_and_push(
            campaign_name=campaign_name,
            total_games=int(final_digest["totals"]["total_games"]),
            paths_to_stage=[
                manifest_path,
                digest_path,
                prompt_path,
                studio_digest_path,
                studio_index_path,
            ],
        )
        print("Publication GitHub Pages poussée sur origin main.")
    else:
        print("Option --skip-git-push active : commit/push ignorés.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
