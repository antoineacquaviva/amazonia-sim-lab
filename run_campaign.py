"""Commande unique de bout en bout pour exécuter un manifeste `campaigns/<nom>.json`
sur Cloud Run Jobs / Cloud Batch (`europe-west9`), agréger via DuckDB, publier le bilan
dans Amazonia Doc Studio (`docs/digests/`) et pousser sur `origin main`.

Usage :
    uv run python run_campaign.py campaigns/<nom>.json
    uv run python run_campaign.py campaigns/<nom>.json --build
    uv run python run_campaign.py campaigns/<nom>.json --no-build
    uv run python run_campaign.py campaigns/<nom>.json --backend batch
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

ROOT: Path = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campaigns.digest_builder import (
    chassis_id_to_studio_index_384,
    write_digest_and_prompt_files,
)
from campaigns.worker_main import resolve_manifest_plan
from engine.telemetry import REVEIL_ANATOMY_FIELDS
from scripts_cloud.studio_paths import find_gcloud

REGION: str = "europe-west9"
BUCKET_NAME: str = "amazonia-sim-runs"
IMAGE_URI: str = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
WORKER_IMAGE_HASH_GCS_URI: str = f"gs://{BUCKET_NAME}/meta/worker_image_hash.txt"
# Sources embarquées dans `Dockerfile.worker` (COPY engine/, bots/, campaigns/, data/spec_bundle_v5_4.json)
# ainsi que `Dockerfile.worker` lui-même (image de base PyPy et ENTRYPOINT).
WORKER_IMAGE_SOURCE_PATHS: tuple[str, ...] = (
    "Dockerfile.worker",
    "engine",
    "bots",
    "campaigns",
    "data/spec_bundle_v5_4.json",
)
_IGNORED_DIR_NAMES: frozenset[str] = frozenset({"__pycache__", ".pytest_cache", ".ruff_cache"})
_IGNORED_FILE_SUFFIXES: frozenset[str] = frozenset({".pyc", ".pyo", ".pyd"})
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


def compute_worker_image_hash(root: Path = ROOT) -> str:
    """Calcule une empreinte SHA-256 déterministe des sources embarquées dans `Dockerfile.worker`.

    Couvre `Dockerfile.worker`, `engine/`, `bots/`, `campaigns/` (hors manifestes `*.json`
    téléversés à la volée sur GCS) et `data/spec_bundle_v5_4.json`, en ignorant les caches
    Python (`__pycache__`, `*.pyc`, etc.) conformément à `.dockerignore`.
    """
    collected: list[tuple[str, Path]] = []
    for rel_entry in WORKER_IMAGE_SOURCE_PATHS:
        target = root / rel_entry
        if not target.exists():
            raise FileNotFoundError(f"Source requise par Dockerfile.worker introuvable : {target}")
        if target.is_file():
            collected.append((target.relative_to(root).as_posix(), target))
            continue
        is_campaigns_dir = rel_entry == "campaigns"
        for file_path in target.rglob("*"):
            if not file_path.is_file():
                continue
            rel_path = file_path.relative_to(root)
            if any(part in _IGNORED_DIR_NAMES for part in rel_path.parts):
                continue
            if file_path.suffix in _IGNORED_FILE_SUFFIXES or file_path.name == ".DS_Store":
                continue
            if is_campaigns_dir and file_path.suffix == ".json":
                continue
            collected.append((rel_path.as_posix(), file_path))

    collected.sort(key=lambda item: item[0])
    hasher = hashlib.sha256()
    for rel_posix, file_path in collected:
        data = file_path.read_bytes()
        hasher.update(rel_posix.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(str(len(data)).encode("ascii"))
        hasher.update(b"\0")
        hasher.update(data)
        hasher.update(b"\n")
    return hasher.hexdigest()


def _read_remote_worker_image_hash(
    gcloud: str,
    gcs_uri: str = WORKER_IMAGE_HASH_GCS_URI,
) -> str | None:
    """Lit l'empreinte distante stockée sur GCS (`None` si absente ou illisible)."""
    proc = _run([gcloud, "storage", "cat", gcs_uri], check=False, capture=True)
    if proc.returncode != 0:
        return None
    value = proc.stdout.strip()
    return value or None


def _write_remote_worker_image_hash(
    gcloud: str,
    image_hash: str,
    gcs_uri: str = WORKER_IMAGE_HASH_GCS_URI,
) -> None:
    """Écrit la nouvelle empreinte de l'image worker dans GCS après un build réussi."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / "worker_image_hash.txt"
        tmp_file.write_text(f"{image_hash}\n", encoding="utf-8")
        _run([gcloud, "storage", "cp", str(tmp_file), gcs_uri])


def ensure_worker_image_up_to_date(
    gcloud: str,
    *,
    force_build: bool = False,
    no_build: bool = False,
    root: Path = ROOT,
    hash_gcs_uri: str = WORKER_IMAGE_HASH_GCS_URI,
) -> bool:
    """Vérifie si l'image `worker-pypy` doit être reconstruite avant le job Cloud.

    Retourne `True` si Cloud Build a été exécuté, `False` si le build a été sauté.
    """
    if force_build and no_build:
        raise ValueError("Les options --build et --no-build sont mutuellement exclusives.")

    if no_build:
        print("Build image worker sauté : option --no-build active.", flush=True)
        return False

    local_hash = compute_worker_image_hash(root=root)

    if force_build:
        print(
            f"Build image worker déclenché : reconstruction manuelle forcée (--build, empreinte={local_hash[:12]}).",
            flush=True,
        )
        _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])
        _write_remote_worker_image_hash(gcloud, local_hash, gcs_uri=hash_gcs_uri)
        return True

    remote_hash = _read_remote_worker_image_hash(gcloud, gcs_uri=hash_gcs_uri)
    if remote_hash == local_hash:
        print(
            f"Build image worker sauté : empreinte locale identique à GCS ({local_hash[:12]}).",
            flush=True,
        )
        return False

    if remote_hash is None:
        print(
            f"Build image worker déclenché : aucune empreinte distante trouvée sur {hash_gcs_uri} "
            f"(empreinte locale={local_hash[:12]}).",
            flush=True,
        )
    else:
        print(
            f"Build image worker déclenché : sources modifiées "
            f"(GCS={remote_hash[:12]} != local={local_hash[:12]}).",
            flush=True,
        )

    _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])
    _write_remote_worker_image_hash(gcloud, local_hash, gcs_uri=hash_gcs_uri)
    return True


def _query_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    rel = con.sql(sql)
    cols = list(rel.columns)
    return [dict(zip(cols, row, strict=True)) for row in rel.fetchall()]


def _sanitize_gcp_name(raw: str, max_len: int = 40) -> str:
    cleaned = re.sub(r"[^a-z0-9-]+", "-", raw.strip().lower()).strip("-")
    if not cleaned or not cleaned[0].isalpha():
        cleaned = f"c-{cleaned}" if cleaned else "campaign"
    return cleaned[:max_len].rstrip("-")


def _build_run_id(manifest: dict[str, Any]) -> str:
    """Construit un identifiant unique `YYYYMMDDTHHMMSSZ_<sha8>` pour isoler les artefacts GCS/locaux."""
    ts = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    canon = json.dumps(manifest, sort_keys=True, ensure_ascii=False).encode("utf-8")
    digest8 = hashlib.sha256(canon).hexdigest()[:8]
    return f"{ts}_{digest8}"


def _cvar_bottom_values(values: list[float], alpha: float = 0.20) -> float:
    """Calcule la moyenne du pire quintile (CVaR_20% inter-tables) d'une liste de ratios."""
    if not values:
        return 0.0
    ordered = sorted(values)
    k = max(1, int((len(ordered) * alpha) + 0.999999))
    return round(sum(ordered[:k]) / k, 4)


def _quantile_values(values: list[float], q: float) -> float:
    """Calcule un quantile linéaire sur une liste de valeurs numériques."""
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(ordered[0], 4)
    pos = max(0.0, min(1.0, q)) * (len(ordered) - 1)
    lo = math.floor(pos)
    hi = min(len(ordered) - 1, lo + 1)
    frac = pos - lo
    return round(ordered[lo] * (1.0 - frac) + ordered[hi] * frac, 4)


def _inter_block_ci95(block_means: list[float]) -> dict[str, Any]:
    """Calcule la moyenne, l'écart-type, l'erreur standard et l'IC95 % inter-blocs."""
    n = len(block_means)
    if n == 0:
        return {
            "n_blocks": 0,
            "mean_ratio_arbres": 0.0,
            "std_inter_blocks": 0.0,
            "se_inter_blocks": 0.0,
            "ci95_low": 0.0,
            "ci95_high": 0.0,
        }
    mean_v = sum(block_means) / n
    if n == 1:
        m_r = round(mean_v, 4)
        return {
            "n_blocks": 1,
            "mean_ratio_arbres": m_r,
            "std_inter_blocks": 0.0,
            "se_inter_blocks": 0.0,
            "ci95_low": m_r,
            "ci95_high": m_r,
        }
    var = sum((x - mean_v) ** 2 for x in block_means) / (n - 1)
    std = math.sqrt(max(0.0, var))
    se = std / math.sqrt(n)
    half = 1.96 * se
    return {
        "n_blocks": n,
        "mean_ratio_arbres": round(mean_v, 4),
        "std_inter_blocks": round(std, 4),
        "se_inter_blocks": round(se, 4),
        "ci95_low": round(max(0.0, mean_v - half), 4),
        "ci95_high": round(min(1.0, mean_v + half), 4),
    }


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
    image_uri: str = IMAGE_URI,
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
            image_uri,
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
    image_uri: str = IMAGE_URI,
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
                                "imageUri": image_uri,
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


def _format_reveil_anatomy_row(raw: dict[str, Any]) -> dict[str, Any]:
    """Convertit les sommes brutes `rs_*`/`rf_*` d'un groupe DuckDB en métriques lisibles."""
    rs_n = int(raw.get("rs_count") or 0)
    rf_n = int(raw.get("rf_count") or 0)

    def _s_mean(key: str) -> float:
        return round(float(raw.get(key) or 0) / rs_n, 3) if rs_n > 0 else 0.0

    def _s_pct(key: str) -> float:
        return round(float(raw.get(key) or 0) * 100.0 / rs_n, 2) if rs_n > 0 else 0.0

    def _f_mean(key: str) -> float:
        return round(float(raw.get(key) or 0) / rf_n, 3) if rf_n > 0 else 0.0

    def _f_pct(key: str) -> float:
        return round(float(raw.get(key) or 0) * 100.0 / rf_n, 2) if rf_n > 0 else 0.0

    def _a_pct(rs_key: str, rf_key: str) -> float:
        tot_v = float(raw.get(rs_key) or 0) + float(raw.get(rf_key) or 0)
        return round(tot_v * 100.0 / total_att, 2) if total_att > 0 else 0.0

    total_att = rs_n + rf_n
    mean_ratio_arbres_eveil = (
        round(float(raw.get("rs_ratio_arbres_bp") or 0) / (rs_n * 10000.0), 4)
        if rs_n > 0
        else 0.0
    )
    out: dict[str, Any] = {
        "n_reveil_success": rs_n,
        "n_reveil_failures": rf_n,
        "success_rate_pct": round(rs_n * 100.0 / total_att, 2) if total_att > 0 else 0.0,
        "count_bouclier_lisiere_saves": int(raw.get("count_bouclier_lisiere_saves") or 0),
        "pct_trigger_1_parade_lit": _a_pct("rs_trig1_lit", "rf_trig1_lit"),
        "pct_trigger_2_piegeage_lit": _a_pct("rs_trig2_lit", "rf_trig2_lit"),
        "pct_trigger_3_sabotage_lit": _a_pct("rs_trig3_lit", "rf_trig3_lit"),
        "pct_trigger_4_gardien_lit": _a_pct("rs_trig4_lit", "rf_trig4_lit"),
        "pct_trigger_5_reve_lit": _a_pct("rs_trig5_lit", "rf_trig5_lit"),
        "pct_trigger_6_insecte_lit": _a_pct("rs_trig6_lit", "rf_trig6_lit"),
        "success_turn": {
            "mean_tour": _s_mean("rs_tour"),
            "mean_ratio_arbres": mean_ratio_arbres_eveil,
            "tour_distribution_pct": {
                "T2": _s_pct("rs_t2"),
                "T3": _s_pct("rs_t3"),
                "T4": _s_pct("rs_t4"),
                "T5": _s_pct("rs_t5"),
                "T6": _s_pct("rs_t6"),
                "T7": _s_pct("rs_t7"),
            },
            "defenders": {
                "mean_def_on_gardien": _s_mean("rs_def_gardien"),
                "mean_def_on_parade": _s_mean("rs_def_parade"),
                "mean_def_on_resonance": _s_mean("rs_def_resonance"),
                "mean_def_on_other_cases": _s_mean("rs_def_other_cases"),
                "mean_distinct_gardiens_bet": _s_mean("rs_distinct_gardiens_bet"),
                "mean_def_on_reve": _s_mean("rs_def_reve"),
                "mean_def1_on_foret": _s_mean("rs_def1_foret"),
                "mean_def2_on_foret": _s_mean("rs_def2_foret"),
                "mean_total_def_on_foret": round(
                    (float(raw.get("rs_def1_foret") or 0) + float(raw.get("rs_def2_foret") or 0))
                    / rs_n,
                    3,
                )
                if rs_n > 0
                else 0.0,
                "mean_def_on_furtivite": _s_mean("rs_def_furtivite"),
                "mean_def_on_lisiere": _s_mean("rs_def_lisiere"),
            },
            "machine_attrition": {
                "mean_cards_sabotage_dealt": _s_mean("rs_cards_sabotage"),
                "mean_cards_none_dealt": _s_mean("rs_cards_none"),
                "mean_cards_machine_dealt": _s_mean("rs_cards_machine"),
                "mean_machines_cancelled_by_reve": _s_mean("rs_cancelled_reve"),
                "mean_machines_bound_tactique": _s_mean("rs_bound_tactique"),
                "mean_ratissage_active": _s_mean("rs_ratissage_active"),
                "mean_machines_retired": _s_mean("rs_machines_retired"),
                "mean_machines_attacked": _s_mean("rs_machines_attacked"),
                "mean_strikes": _s_mean("rs_strikes"),
                "mean_reves_on_track": _s_mean("rs_reves_on_track"),
                "mean_reves_opened": _s_mean("rs_reves_opened"),
                "pct_trigger_1_parade_lit": _s_pct("rs_trig1_lit"),
                "pct_trigger_2_piegeage_lit": _s_pct("rs_trig2_lit"),
                "pct_trigger_3_sabotage_lit": _s_pct("rs_trig3_lit"),
                "pct_trigger_4_gardien_lit": _s_pct("rs_trig4_lit"),
                "pct_trigger_5_reve_lit": _s_pct("rs_trig5_lit"),
                "pct_trigger_6_insecte_lit": _s_pct("rs_trig6_lit"),
                "mean_sabotage_in_deck": _s_mean("rs_sabotage_in_deck"),
            },
            "zero_damage_mechanisms": {
                "mean_pre_insects_board": _s_mean("rs_pre_insects"),
                "mean_pre_pieges_board": _s_mean("rs_pre_pieges"),
                "mean_insects_spent_step5": _s_mean("rs_insects_spent"),
                "mean_pieges_triggered_step5": _s_mean("rs_pieges_triggered"),
                "pct_zero_strikes": _s_pct("rs_cat_zero_strikes"),
                "pct_with_piege_triggered": _s_pct("rs_cat_piege"),
                "pct_insects_without_piege": _s_pct("rs_cat_insects_no_piege"),
                "pct_pure_def_or_zero_tree": _s_pct("rs_cat_pure_def_or_empty"),
            },
        },
        "failed_attempts_comparison": {
            "mean_tour": _f_mean("rf_tour"),
            "mean_def_on_gardien": _f_mean("rf_def_gardien"),
            "mean_def_on_parade": _f_mean("rf_def_parade"),
            "mean_def_on_resonance": _f_mean("rf_def_resonance"),
            "mean_def_on_other_cases": _f_mean("rf_def_other_cases"),
            "mean_distinct_gardiens_bet": _f_mean("rf_distinct_gardiens_bet"),
            "mean_def_on_reve": _f_mean("rf_def_reve"),
            "mean_def1_on_foret": _f_mean("rf_def1_foret"),
            "mean_def2_on_foret": _f_mean("rf_def2_foret"),
            "mean_cards_sabotage_dealt": _f_mean("rf_cards_sabotage"),
            "mean_machines_cancelled_by_reve": _f_mean("rf_cancelled_reve"),
            "mean_machines_bound_tactique": _f_mean("rf_bound_tactique"),
            "mean_ratissage_active": _f_mean("rf_ratissage_active"),
            "mean_machines_attacked": _f_mean("rf_machines_attacked"),
            "mean_strikes": _f_mean("rf_strikes"),
            "mean_insects_spent_step5": _f_mean("rf_insects_spent"),
            "mean_pieges_triggered_step5": _f_mean("rf_pieges_triggered"),
            "mean_reves_on_track": _f_mean("rf_reves_on_track"),
            "mean_reves_opened": _f_mean("rf_reves_opened"),
            "pct_trigger_1_parade_lit": _f_pct("rf_trig1_lit"),
            "pct_trigger_2_piegeage_lit": _f_pct("rf_trig2_lit"),
            "pct_trigger_3_sabotage_lit": _f_pct("rf_trig3_lit"),
            "pct_trigger_4_gardien_lit": _f_pct("rf_trig4_lit"),
            "pct_trigger_5_reve_lit": _f_pct("rf_trig5_lit"),
            "pct_trigger_6_insecte_lit": _f_pct("rf_trig6_lit"),
            "mean_sabotage_in_deck": _f_mean("rf_sabotage_in_deck"),
        },
    }
    return out


def _build_reveil_anatomy_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
) -> dict[str, Any] | None:
    if not all(col in cell_cols for col in REVEIL_ANATOMY_FIELDS):
        return None
    bouclier_sql = (
        "CAST(SUM(count_bouclier_lisiere_saves) AS BIGINT) AS count_bouclier_lisiere_saves"
        if "count_bouclier_lisiere_saves" in cell_cols
        else "0 AS count_bouclier_lisiere_saves"
    )
    sum_cols_sql = ",\n            ".join(
        [*(f"CAST(SUM({col}) AS BIGINT) AS {col}" for col in REVEIL_ANATOMY_FIELDS), bouclier_sql]
    )
    g_raw = _query_dicts(con, f"SELECT {sum_cols_sql} FROM cells")[0]
    if int(g_raw.get("rs_count") or 0) == 0 and int(g_raw.get("rf_count") or 0) == 0:
        return None

    by_variant_raw = _query_dicts(
        con,
        f"""
        SELECT
            variant_id,
            {sum_cols_sql}
        FROM cells
        GROUP BY variant_id
        ORDER BY variant_id
        """,
    )
    by_n_raw = _query_dicts(
        con,
        f"""
        SELECT
            n_players,
            {sum_cols_sql}
        FROM cells
        GROUP BY n_players
        ORDER BY n_players
        """,
    )
    return {
        "global": _format_reveil_anatomy_row(g_raw),
        "by_variant": [
            {"variant_id": str(r["variant_id"]), **_format_reveil_anatomy_row(r)}
            for r in by_variant_raw
        ],
        "by_n_players": [
            {"n_players": int(r["n_players"]), **_format_reveil_anatomy_row(r)}
            for r in by_n_raw
        ],
    }


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
    run_id: str | None = None,
    gcs_prefix: str | None = None,
    image_uri: str = IMAGE_URI,
) -> tuple[Path, Path, dict[str, Any]]:
    """Agrège les shards JSONL.gz via DuckDB, archive Parquet et écrit le digest auto-portant."""
    campaign_name = str(plan["campaign_name"])
    glob_pattern = (shards_dir / "shard_*.jsonl.gz").as_posix()
    parquet_posix = parquet_path.as_posix()

    con = duckdb.connect(":memory:")
    con.execute(f"CREATE TABLE cells AS SELECT * FROM read_json_auto('{glob_pattern}')")
    con.execute(f"COPY cells TO '{parquet_posix}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    cell_cols = {str(r[0]) for r in con.sql("DESCRIBE cells").fetchall()}
    has_ops_cols = "sum_physical_ops" in cell_cols and "sum_player_decisions" in cell_cols
    ops_select_sql = (
        """
            ROUND(SUM(sum_physical_ops) * 1.0 / SUM(n_games), 3) AS mean_physical_ops,
            ROUND(SUM(sum_player_decisions) * 1.0 / SUM(n_games), 3) AS mean_player_decisions,
        """
        if has_ops_cols
        else """
            NULL AS mean_physical_ops,
            NULL AS mean_player_decisions,
        """
    )
    mid_combat_sql = (
        "ROUND(SUM(sum_mid_combat) * 1.0 / SUM(n_games), 3) AS mean_mid_combat_interrupts,"
        if "sum_mid_combat" in cell_cols
        else "NULL AS mean_mid_combat_interrupts,"
    )
    extra_q_sql_parts: list[str] = []
    if "min_ratio_arbres" in cell_cols:
        extra_q_sql_parts.append("ROUND(MIN(min_ratio_arbres), 4) AS cell_min_ratio,")
    else:
        extra_q_sql_parts.append("NULL AS cell_min_ratio,")
    if "max_ratio_arbres" in cell_cols:
        extra_q_sql_parts.append("ROUND(MAX(max_ratio_arbres), 4) AS cell_max_ratio,")
    else:
        extra_q_sql_parts.append("NULL AS cell_max_ratio,")
    for q_col in ("p10_ratio", "p20_ratio", "p50_ratio", "p90_ratio"):
        if q_col in cell_cols:
            extra_q_sql_parts.append(
                f"ROUND(SUM({q_col} * n_games) / SUM(n_games), 4) AS weighted_{q_col},"
            )
        else:
            extra_q_sql_parts.append(f"NULL AS weighted_{q_col},")
    extra_q_sql = "\n            ".join(extra_q_sql_parts)

    has_reveil_diag_cols = (
        "count_reveil_attempts" in cell_cols and "count_reveil_failures" in cell_cols
    )
    has_gardien_bets_cols = (
        "count_gardien_bets_won" in cell_cols and "count_gardien_bets_lost" in cell_cols
    )
    has_bouclier_col = "count_bouclier_lisiere_saves" in cell_cols
    reveil_diag_sql = (
        (
            """
            CAST(SUM(count_reveil_attempts) AS INTEGER) AS count_reveil_attempts,
            CAST(SUM(count_reveil_failures) AS INTEGER) AS count_reveil_failures,
        """
            if has_reveil_diag_cols
            else """
            0 AS count_reveil_attempts,
            0 AS count_reveil_failures,
        """
        )
        + (
            """
            CAST(SUM(count_gardien_bets_won) AS INTEGER) AS count_gardien_bets_won,
            CAST(SUM(count_gardien_bets_lost) AS INTEGER) AS count_gardien_bets_lost,
        """
            if has_gardien_bets_cols
            else """
            0 AS count_gardien_bets_won,
            0 AS count_gardien_bets_lost,
        """
        )
        + (
            """
            CAST(SUM(count_bouclier_lisiere_saves) AS INTEGER) AS count_bouclier_lisiere_saves,
        """
            if has_bouclier_col
            else """
            0 AS count_bouclier_lisiere_saves,
        """
        )
    )
    has_reve_act_cols = (
        "count_reves_activated" in cell_cols
        and "count_machines_cancelled_by_reve" in cell_cols
        and "count_machines_bypassed_inactive_reve" in cell_cols
    )
    reve_act_sql = (
        """
            CAST(SUM(count_reves_activated) AS INTEGER) AS count_reves_activated,
            CAST(SUM(count_machines_cancelled_by_reve) AS INTEGER) AS count_machines_cancelled_by_reve,
            CAST(SUM(count_machines_bypassed_inactive_reve) AS INTEGER) AS count_machines_bypassed_inactive_reve,
        """
        if has_reve_act_cols
        else """
            0 AS count_reves_activated,
            0 AS count_machines_cancelled_by_reve,
            0 AS count_machines_bypassed_inactive_reve,
        """
    )
    has_n_animaux_col = "n_animaux_sauvages" in cell_cols

    g_stats = _query_dicts(
        con,
        f"""
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
            {reveil_diag_sql}
            {reve_act_sql}
            ROUND(SUM(sum_mem_debt) * 1.0 / SUM(n_games), 3) AS mean_mem_debt,
            ROUND(SUM(sum_law_mean) / SUM(n_games), 3) AS mean_active_laws,
            CAST(MAX(max_law_max) AS INTEGER) AS max_active_laws,
            ROUND(SUM(sum_fiddliness) / SUM(n_games), 3) AS mean_fiddliness_ops,
            {ops_select_sql}
            {mid_combat_sql}
            {extra_q_sql}
            ROUND(SUM(sum_cascade_sweeps) * 1.0 / SUM(n_games), 3) AS mean_cascade_sweeps
        FROM cells
        """,
    )[0]

    # CVaR_20% inter-tables véritable (pire quintile des ratios moyens par table/cellule),
    # distinct de `cvar20_ratio` (moyenne pondérée des CVaR intra-cellule).
    n_anim_col_sql = "n_animaux_sauvages," if has_n_animaux_col else "NULL AS n_animaux_sauvages,"
    cell_table_rows = _query_dicts(
        con,
        f"""
        SELECT
            mode,
            bot,
            n_players,
            chassis_id,
            variant_id,
            {n_anim_col_sql}
            sum_ratio_arbres * 1.0 / n_games AS table_mean_ratio
        FROM cells
        WHERE n_games > 0
        """,
    )
    all_table_ratios: list[float] = []
    ratios_by_mode: dict[tuple[int, str], list[float]] = {}
    ratios_by_n: dict[int, list[float]] = {}
    ratios_by_chassis: dict[int, list[float]] = {}
    ratios_by_variant: dict[str, list[float]] = {}
    ratios_by_n_animaux: dict[int, list[float]] = {}
    ratios_by_variant_n: dict[tuple[str, int], list[float]] = {}
    ratios_by_variant_animaux: dict[tuple[str, int], list[float]] = {}
    for tr in cell_table_rows:
        mr_t = float(tr["table_mean_ratio"])
        v_id_t = str(tr["variant_id"])
        n_pl_t = int(tr["n_players"])
        all_table_ratios.append(mr_t)
        ratios_by_mode.setdefault((int(tr["mode"]), str(tr["bot"])), []).append(mr_t)
        ratios_by_n.setdefault(n_pl_t, []).append(mr_t)
        ratios_by_chassis.setdefault(int(tr["chassis_id"]), []).append(mr_t)
        ratios_by_variant.setdefault(v_id_t, []).append(mr_t)
        ratios_by_variant_n.setdefault((v_id_t, n_pl_t), []).append(mr_t)
        if tr.get("n_animaux_sauvages") is not None:
            na_t = int(tr["n_animaux_sauvages"])
            ratios_by_n_animaux.setdefault(na_t, []).append(mr_t)
            ratios_by_variant_animaux.setdefault((v_id_t, na_t), []).append(mr_t)

    global_table_cvar20 = _cvar_bottom_values(all_table_ratios, 0.20)

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
        f"""
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
            {reveil_diag_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode, bot
        ORDER BY mode, bot
        """,
    )
    for row in by_mode:
        row["table_cvar20_ratio"] = _cvar_bottom_values(
            ratios_by_mode.get((int(row["mode"]), str(row["bot"])), []), 0.20
        )

    by_n_players = _query_dicts(
        con,
        f"""
        SELECT
            n_players,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            {reveil_diag_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY n_players
        ORDER BY n_players
        """,
    )
    for row in by_n_players:
        row["table_cvar20_ratio"] = _cvar_bottom_values(
            ratios_by_n.get(int(row["n_players"]), []), 0.20
        )

    by_n_animaux_sauvages: list[dict[str, Any]] = []
    if has_n_animaux_col:
        by_n_animaux_sauvages = _query_dicts(
            con,
            f"""
            SELECT
                n_animaux_sauvages,
                CAST(SUM(n_games) AS INTEGER) AS n_games,
                ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
                ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
                ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
                ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
                ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
                ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
                {reveil_diag_sql}
                ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
            FROM cells
            GROUP BY n_animaux_sauvages
            ORDER BY n_animaux_sauvages
            """,
        )
        for row in by_n_animaux_sauvages:
            row["table_cvar20_ratio"] = _cvar_bottom_values(
                ratios_by_n_animaux.get(int(row["n_animaux_sauvages"]), []), 0.20
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
    for row in by_chassis:
        cid = int(row["chassis_id"])
        row["studio_config_index_192"] = chassis_id_to_studio_index_384(cid)
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_chassis.get(cid, []), 0.20)

    by_variant = _query_dicts(
        con,
        f"""
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
            {reveil_diag_sql}
            {reve_act_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY variant_id, compared_slots_json
        ORDER BY mean_ratio_arbres DESC, variant_id ASC
        """,
    )
    for row in by_variant:
        row["table_cvar20_ratio"] = _cvar_bottom_values(
            ratios_by_variant.get(str(row["variant_id"]), []), 0.20
        )

    by_variant_x_n_players = _query_dicts(
        con,
        f"""
        SELECT
            variant_id,
            n_players,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            {reveil_diag_sql}
            {reve_act_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY variant_id, n_players
        ORDER BY variant_id ASC, n_players ASC
        """,
    )
    for row in by_variant_x_n_players:
        row["table_cvar20_ratio"] = _cvar_bottom_values(
            ratios_by_variant_n.get((str(row["variant_id"]), int(row["n_players"])), []), 0.20
        )

    by_variant_x_n_animaux_sauvages: list[dict[str, Any]] = []
    if has_n_animaux_col:
        by_variant_x_n_animaux_sauvages = _query_dicts(
            con,
            f"""
            SELECT
                variant_id,
                n_animaux_sauvages,
                CAST(SUM(n_games) AS INTEGER) AS n_games,
                ROUND(SUM(sum_arbres) * 1.0 / SUM(n_games), 3) AS mean_score_arbres,
                ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
                ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
                ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
                ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
                ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
                {reveil_diag_sql}
                {reve_act_sql}
                ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
            FROM cells
            GROUP BY variant_id, n_animaux_sauvages
            ORDER BY variant_id ASC, n_animaux_sauvages ASC
            """,
        )
        for row in by_variant_x_n_animaux_sauvages:
            row["table_cvar20_ratio"] = _cvar_bottom_values(
                ratios_by_variant_animaux.get(
                    (str(row["variant_id"]), int(row["n_animaux_sauvages"])), []
                ),
                0.20,
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
    varying_tiles: tuple[tuple[str, str], ...] = tuple(plan.get("varying_tiles", ()))
    chassis_ids: tuple[int, ...] = tuple(plan["chassis_ids"])
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    campaign_seed = int(manifest.get("seed", plan.get("exp_seed", 20261119)))

    # Quantiles inter-tables + quantiles intra-cellules disponibles dans DuckDB
    quantiles_block: dict[str, Any] = {
        "min_ratio_arbres": _quantile_values(all_table_ratios, 0.0),
        "p10_ratio": _quantile_values(all_table_ratios, 0.10),
        "p20_ratio": _quantile_values(all_table_ratios, 0.20),
        "p50_ratio": _quantile_values(all_table_ratios, 0.50),
        "p90_ratio": _quantile_values(all_table_ratios, 0.90),
        "max_ratio_arbres": _quantile_values(all_table_ratios, 1.0),
    }
    for q_key in (
        "cell_min_ratio",
        "cell_max_ratio",
        "weighted_p10_ratio",
        "weighted_p20_ratio",
        "weighted_p50_ratio",
        "weighted_p90_ratio",
    ):
        if g_stats.get(q_key) is not None:
            quantiles_block[q_key] = float(g_stats[q_key])

    # Intervalles de confiance 95 % calculés inter-blocs (uniquement sur les moyennes de blocs/tables)
    inter_block_intervals: dict[str, Any] = {
        "global": _inter_block_ci95(all_table_ratios),
        "by_n_players": {
            str(n_pl): _inter_block_ci95(ratios_by_n[n_pl])
            for n_pl in sorted(ratios_by_n)
        },
    }

    # Forks et seeds (inclus automatiquement si la campagne produit des colonnes de micro-forks)
    forks_block: dict[str, Any] | None = None
    if "fork_anchors" in cell_cols:
        fork_missed_sql = (
            "CAST(SUM(fork_anchors_missed) AS INTEGER) AS fork_anchors_missed,"
            if "fork_anchors_missed" in cell_cols
            else "0 AS fork_anchors_missed,"
        )
        fork_div_sql = (
            "CAST(SUM(fork_diverged) AS INTEGER) AS fork_diverged,"
            if "fork_diverged" in cell_cols
            else "0 AS fork_diverged,"
        )
        fork_row = _query_dicts(
            con,
            f"""
            SELECT
                CAST(SUM(fork_anchors) AS INTEGER) AS fork_anchors,
                {fork_missed_sql}
                {fork_div_sql}
                COUNT(*) AS n_fork_rows
            FROM cells
            WHERE fork_anchors > 0
            """,
        )[0]
        if int(fork_row.get("fork_anchors") or 0) > 0:
            seed_col = "exp_seed" if "exp_seed" in cell_cols else ("seed" if "seed" in cell_cols else None)
            if seed_col is not None:
                seed_rows = _query_dicts(
                    con,
                    f"SELECT DISTINCT {seed_col} AS seed FROM cells WHERE fork_anchors > 0 ORDER BY seed LIMIT 64",
                )
                fork_seeds = [int(r["seed"]) for r in seed_rows if r.get("seed") is not None]
            else:
                fork_seeds = [campaign_seed]
            forks_block = {
                "fork_anchors": int(fork_row["fork_anchors"]),
                "fork_anchors_missed": int(fork_row["fork_anchors_missed"] or 0),
                "fork_diverged": int(fork_row["fork_diverged"] or 0),
                "n_fork_rows": int(fork_row["n_fork_rows"]),
                "seeds": fork_seeds,
            }

    base_tile_profiles: dict[str, str] = dict(plan.get("base_tile_profiles", {}))
    non_default_base_slots = {s: p for s, p in base_tile_profiles.items() if p != "A"}
    selection_manifest: dict[str, Any] = {
        "base_bundle_id": str(plan.get("base_bundle_id", "STANDARD_A")),
        "n_resolved_slots": len(base_tile_profiles) if base_tile_profiles else 32,
        "non_default_base_slots": non_default_base_slots,
        "resolved_32_slots_sha256": str(plan.get("resolved_32_slots_sha256", "")),
        "migration_policy": dict(plan.get("migration_policy", {})),
    }

    execution_meta: dict[str, Any] = {
        "backend": backend,
        "region": REGION,
        "job_name": job_name,
        "image": image_uri,
        "tasks": tasks,
        "seed": campaign_seed,
        "job_wall_sec": round(job_wall_sec, 3),
        "max_worker_compute_sec": round(max_compute_sec, 3),
        "sum_worker_games_per_sec": sum_worker_gps,
        "effective_cluster_games_per_sec": eff_gps,
    }
    if run_id is not None:
        execution_meta["run_id"] = run_id
    if gcs_prefix is not None:
        execution_meta["gcs_prefix"] = gcs_prefix

    telemetry_block: dict[str, Any] = {
        "mean_mem_debt": g_stats["mean_mem_debt"],
        "mean_active_laws": g_stats["mean_active_laws"],
        "max_active_laws": g_stats["max_active_laws"],
        "mean_fiddliness_ops": g_stats["mean_fiddliness_ops"],
        "mean_cascade_sweeps": g_stats["mean_cascade_sweeps"],
    }
    if g_stats["mean_physical_ops"] is not None:
        telemetry_block["mean_physical_ops"] = g_stats["mean_physical_ops"]
    if g_stats["mean_player_decisions"] is not None:
        telemetry_block["mean_player_decisions"] = g_stats["mean_player_decisions"]
    if g_stats.get("mean_mid_combat_interrupts") is not None:
        telemetry_block["mean_mid_combat_interrupts"] = g_stats["mean_mid_combat_interrupts"]

    digest_payload: dict[str, Any] = {
        "campaign": campaign_name,
        "description": str(manifest.get("description", "")).strip(),
        "generated_at_utc": generated_at,
        "selection_manifest": selection_manifest,
        "execution": execution_meta,
        "totals": {
            "total_games": total_games,
            "n_shards": int(g_stats["n_shards"]),
            "n_cells": int(g_stats["n_cells"]),
            "n_configurations": int(g_stats["n_configurations"]),
            "mean_score_arbres": g_stats["mean_score_arbres"],
            "mean_ratio_arbres": g_stats["mean_ratio_arbres"],
            "cvar20_ratio": g_stats["cvar20_ratio"],
            "within_table_cvar20_ratio": g_stats["cvar20_ratio"],
            "table_cvar20_ratio": global_table_cvar20,
            "survival_rate": g_stats["survival_rate"],
            "mean_tours": g_stats["mean_tours"],
            "pct_tour_8": g_stats["pct_tour_8"],
            "pct_reve_rang_1": g_stats["pct_reve_rang_1"],
            "pct_reveil_gardiens": g_stats["pct_reveil_gardiens"],
            "count_reveil_attempts": int(g_stats["count_reveil_attempts"]),
            "count_reveil_failures": int(g_stats["count_reveil_failures"]),
            "count_gardien_bets_won": int(g_stats["count_gardien_bets_won"]),
            "count_gardien_bets_lost": int(g_stats["count_gardien_bets_lost"]),
            "count_bouclier_lisiere_saves": int(g_stats["count_bouclier_lisiere_saves"]),
            "count_reves_activated": int(g_stats["count_reves_activated"]),
            "count_machines_cancelled_by_reve": int(g_stats["count_machines_cancelled_by_reve"]),
            "count_machines_bypassed_inactive_reve": int(
                g_stats["count_machines_bypassed_inactive_reve"]
            ),
            "tested_tiles": [f"{s}:{p}" for s, p in tested_tiles],
            "parquet_archive": parquet_path.relative_to(ROOT).as_posix(),
        },
        "quantiles": quantiles_block,
        "inter_block_intervals": inter_block_intervals,
        "telemetry": telemetry_block,
        "by_mode": by_mode,
        "by_n_players": by_n_players,
        "by_chassis": by_chassis,
        "by_variant": by_variant_clean,
        "by_variant_x_n_players": by_variant_x_n_players,
        "tile_metrics": tile_metrics,
    }
    if by_n_animaux_sauvages:
        digest_payload["by_n_animaux_sauvages"] = by_n_animaux_sauvages
    if by_variant_x_n_animaux_sauvages:
        digest_payload["by_variant_x_n_animaux_sauvages"] = by_variant_x_n_animaux_sauvages
    if forks_block is not None:
        digest_payload["forks"] = forks_block
    reveil_anatomy_block = _build_reveil_anatomy_block(con, cell_cols)
    if reveil_anatomy_block is not None:
        digest_payload["reveil_anatomy"] = reveil_anatomy_block

    digest_path, prompt_path, final_digest = write_digest_and_prompt_files(
        campaign_name,
        digest_payload,
        chassis_ids=chassis_ids[:8],
        tested_tiles=tested_tiles,
        varying_tiles=varying_tiles if varying_tiles else None,
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
        "--image-uri",
        type=str,
        default=IMAGE_URI,
        help="URI d'image Docker worker PyPy (recommandé : digest immuable @sha256:... pour reproductibilité).",
    )
    build_group = parser.add_mutually_exclusive_group()
    build_group.add_argument(
        "--build",
        action="store_true",
        help="Force la reconstruction et le push de l'image worker PyPy via Cloud Build avant exécution.",
    )
    build_group.add_argument(
        "--no-build",
        action="store_true",
        help="Force le saut du build Cloud même si les sources locales diffèrent de GCS.",
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
    image_uri = str(args.image_uri).strip() or IMAGE_URI
    run_id = _build_run_id(manifest)

    print(
        f"=== Campagne '{campaign_name}' [run_id={run_id}] : {total_games_planned} parties "
        f"({plan['total_configurations']} configs, {n_units} unités) | "
        f"backend={backend} ({REGION}, {tasks} tâche(s)) ===",
        flush=True,
    )

    gcloud = find_gcloud()
    gcs_prefix = f"campaigns/{campaign_name}/{run_id}"
    manifest_gcs_uri = f"gs://{BUCKET_NAME}/{gcs_prefix}/manifest.json"
    shards_gcs_glob = f"gs://{BUCKET_NAME}/{gcs_prefix}/shard_*.jsonl.gz"

    # 1. Auto-détection (ou forçage --build / saut --no-build) du build de l'image worker PyPy
    ensure_worker_image_up_to_date(
        gcloud,
        force_build=bool(args.build),
        no_build=bool(args.no_build),
    )

    # 2. Upload du manifeste sous préfixe GCS isolé par run_id (aucun `rm` destructif sur un préfixe partagé)
    _run([gcloud, "storage", "cp", str(manifest_path), manifest_gcs_uri])

    # 3. Exécution Cloud Run Jobs ou Cloud Batch (europe-west9) et attente synchrone
    run_dir = ROOT / ".tmp_runs" / "campaigns" / campaign_name / run_id
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
            image_uri=image_uri,
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
            image_uri=image_uri,
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
        run_id=run_id,
        gcs_prefix=gcs_prefix,
        image_uri=image_uri,
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
