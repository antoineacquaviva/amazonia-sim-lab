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

from campaigns.digest_builder import write_digest_and_prompt_files
from campaigns.stats_tools import (
    assess_sign_stability,
    circle_dispersion_summary,
    cvar_exact_values,
    cvar_with_bootstrap_ci95,
    estimate_required_pairs,
    holm_bonferroni_adjust,
    paired_diff_cluster_ci95,
    sequential_ci_elimination,
)
from campaigns.worker_main import (
    CANONICAL_32_SLOTS,
    _execute_manifest_unit,
    resolve_manifest_plan,
)
from engine.state import ANIMAUX_SAUVAGES, MATRICE_PAIRES
from engine.telemetry import (
    DEFENSE_ATTRIBUTION_FIELDS,
    DILEMMA_CHOICE_FIELDS,
    OCKHAM_COUNT_FIELDS,
    REVEIL_ANATOMY_FIELDS,
)
from scripts_cloud.studio_paths import find_gcloud

REGION: str = "europe-west9"
BUCKET_NAME: str = "amazonia-sim-runs"
IMAGE_URI: str = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
WORKER_IMAGE_HASH_GCS_URI: str = f"gs://{BUCKET_NAME}/meta/worker_image_hash.txt"
# Sources embarquées dans `Dockerfile.worker` (COPY engine/, bots/, campaigns/, data/spec_bundle_v6_0.json)
# ainsi que `Dockerfile.worker` lui-même (image de base PyPy et ENTRYPOINT).
WORKER_IMAGE_SOURCE_PATHS: tuple[str, ...] = (
    "Dockerfile.worker",
    "engine",
    "bots",
    "campaigns",
    "data/spec_bundle_v6_0.json",
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
    téléversés à la volée sur GCS) et `data/spec_bundle_v6_0.json`, en ignorant les caches
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
    """Calcule la CVaR continue uniforme sur une liste de ratios."""
    if not values:
        return 0.0
    return round(cvar_exact_values(values, alpha=alpha), 4)


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


def _inter_block_ci95(
    block_means: list[float],
    block_weights: list[int] | None = None,
) -> dict[str, Any]:
    """Calcule la moyenne pondérée et la dispersion inter-cercles (explicitement non estimable si 1 cercle)."""
    res = circle_dispersion_summary(block_means, block_weights)
    # Rétro-compatibilité douce des noms de champs std_inter_blocks / se_inter_blocks
    res["std_inter_blocks"] = res["std_inter_circles"]
    res["se_inter_blocks"] = res["se_inter_circles"]
    return res


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
            "pct_before_t5": round(
                (
                    float(raw.get("rs_t1") or 0)
                    + float(raw.get("rs_t2") or 0)
                    + float(raw.get("rs_t3") or 0)
                    + float(raw.get("rs_t4") or 0)
                )
                * 100.0
                / rs_n,
                2,
            )
            if rs_n > 0
            else 0.0,
            "tour_distribution_pct": {
                "T1": _s_pct("rs_t1"),
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
    req_cols = [c for c in REVEIL_ANATOMY_FIELDS if c != "rs_t1"]
    if not all(col in cell_cols for col in req_cols):
        return None
    bouclier_sql = (
        "CAST(SUM(count_bouclier_lisiere_saves) AS BIGINT) AS count_bouclier_lisiere_saves"
        if "count_bouclier_lisiere_saves" in cell_cols
        else "0 AS count_bouclier_lisiere_saves"
    )
    sum_cols_sql = ",\n            ".join(
        [
            *(
                (
                    f"CAST(SUM({col}) AS BIGINT) AS {col}"
                    if col in cell_cols
                    else f"0 AS {col}"
                )
                for col in REVEIL_ANATOMY_FIELDS
            ),
            bouclier_sql,
        ]
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
    by_var_bot_n_raw = _query_dicts(
        con,
        f"""
        SELECT
            variant_id,
            bot,
            n_players,
            {sum_cols_sql}
        FROM cells
        WHERE bot IN ('B2', 'B3')
        GROUP BY variant_id, bot, n_players
        ORDER BY variant_id, bot, n_players
        """,
    )
    out_blk: dict[str, Any] = {
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
    active_vbn = [
        r
        for r in by_var_bot_n_raw
        if int(r.get("rs_count") or 0) + int(r.get("rf_count") or 0) > 0
    ]
    if active_vbn:
        out_blk["by_variant_x_bot_x_n_players"] = [
            {
                "variant_id": str(r["variant_id"]),
                "bot": str(r["bot"]),
                "n_players": int(r["n_players"]),
                **_format_reveil_anatomy_row(r),
            }
            for r in active_vbn
        ]
    return out_blk


def _build_defense_attribution_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
    total_games: int,
) -> dict[str, Any] | None:
    """Construit la section `defense_attribution` (7 postes + moyennes par partie + ventilation par bot)."""
    if not any(col in cell_cols for col in DEFENSE_ATTRIBUTION_FIELDS):
        return None

    def _sum_sql(col: str) -> str:
        return (
            f"CAST(COALESCE(SUM({col}), 0) AS BIGINT) AS {col}"
            if col in cell_cols
            else f"0 AS {col}"
        )

    select_cols = ",\n            ".join(_sum_sql(c) for c in DEFENSE_ATTRIBUTION_FIELDS)
    g_raw = _query_dicts(con, f"SELECT {select_cols} FROM cells")[0]

    key_map: tuple[tuple[str, str], ...] = (
        ("parade_classique", "da_parade_classique"),
        ("piege", "da_piege"),
        ("parade_avec_insectes", "da_parade_avec_insectes"),
        ("reve_annulation", "da_reve_annulation"),
        ("sabotage_revele", "da_sabotage_revele"),
        ("insecte_bug_deviation", "da_insecte_bug_deviation"),
        ("arbres_repousse_finale", "da_arbres_repousse_finale"),
    )
    denom = max(1, total_games)
    out: dict[str, Any] = {}
    per_game: dict[str, float] = {}
    neutral_keys = (
        "parade_classique",
        "piege",
        "parade_avec_insectes",
        "reve_annulation",
        "sabotage_revele",
        "insecte_bug_deviation",
    )
    total_neutral = 0
    for pub_k, col_k in key_map:
        val = int(g_raw.get(col_k) or 0)
        out[pub_k] = val
        per_game[pub_k] = round(val / denom, 3)
        if pub_k in neutral_keys:
            total_neutral += val
    out["total_neutralisations"] = total_neutral
    out["per_game"] = per_game

    by_bot_raw = _query_dicts(
        con,
        f"""
        SELECT
            bot,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            {select_cols}
        FROM cells
        GROUP BY bot
        ORDER BY bot
        """,
    )
    if len(by_bot_raw) > 1:
        by_bot_out: list[dict[str, Any]] = []
        for brow in by_bot_raw:
            b_ng = max(1, int(brow["n_games"]))
            b_entry: dict[str, Any] = {"bot": str(brow["bot"]), "n_games": int(brow["n_games"])}
            for pub_k, col_k in key_map:
                b_entry[pub_k] = round(int(brow.get(col_k) or 0) / b_ng, 3)
            by_bot_out.append(b_entry)
        out["by_bot"] = by_bot_out
    return out


_OCKHAM_RULES_CATALOG: tuple[tuple[str, str, str, float, str], ...] = (
    ("ok_furt_rive_piege", "FURTIVITE", "4.1 Rive Piège gagnée (m(r) == 2 -> Piège autonome)", 2.0, "UTILE"),
    ("ok_furt_rive_sabotage", "FURTIVITE", "4.1 Rive Sabotage gagnée (m(r) == 0 -> Carte Sabotage 6.3)", 1.0, "UTILE"),
    ("ok_furt_rive_piege_lost", "FURTIVITE", "4.1 Rive Piège perdue (binôme 2/2 avec m(r) != 2)", 2.0, "STERILE_FRICTION"),
    ("ok_furt_rive_sabotage_lost", "FURTIVITE", "4.1 Rive Sabotage perdue (binôme 2/2 avec m(r) != 0)", 2.0, "STERILE_FRICTION"),
    ("ok_furt_orphan_pawns", "FURTIVITE", "4.1 Pion Défenseur orphelin (1/2) perdu à blanc", 1.0, "STERILE_FRICTION"),
    ("ok_furt_failed_binomes", "FURTIVITE", "4.1 Binôme 2/2 perdu ou sans cible valide", 2.0, "STERILE_FRICTION"),
    ("ok_furt_multi_rive_turns", "FURTIVITE", "4.1 Tour avec >= 2 rives Furtivité gagnées", 0.0, "EXCEPTION_RARE"),
    ("ok_pieges_placed", "FURTIVITE", "Jetons Piège autonomes posés en Forêt", 1.0, "UTILE"),
    ("ok_pieges_triggered", "FURTIVITE", "5.x Pièges autonomes déclenchés (1re frappe bloquée)", 1.0, "UTILE"),
    ("ok_pieges_unused_end", "FURTIVITE", "Fin : Pièges actifs jamais déclenchés (reliquat)", 2.0, "STERILE_FRICTION"),
    ("ok_sabotage_acquired", "FURTIVITE", "4.1 Cartes Sabotage acquises (injectées en 6.3)", 1.0, "UTILE"),
    ("ok_sabotage_unrevealed_end", "FURTIVITE", "Fin : Sabotages acquis jamais tirés en 1.2", 1.0, "STERILE_FRICTION"),
    ("ok_routes_created", "PISTE_MACHINES", "5.x Création d'une Route Forestière (0/0)", 2.0, "UTILE"),
    ("ok_pont_routier_jumps", "PISTE_MACHINES", "5.x Saut de Pont routier (ciblage DEVANT, avancée ou repli)", 1.0, "UTILE"),
    ("ok_repli_bordure", "PISTE_MACHINES", "5.x Repli machine standard vers la bordure", 1.0, "UTILE"),
    ("ok_repli_coeur_exception", "PISTE_MACHINES", "5.x Repli machine d'exception vers le cœur (bordure rasée)", 1.0, "EXCEPTION_RARE"),
    ("ok_retrait_definitif_machine", "PISTE_MACHINES", "5.x Retrait définitif d'une machine (rayon 100 % rasé)", 2.0, "EXCEPTION_RARE"),
    ("ok_abatteuse_ratissage_0_arbre", "PISTE_MACHINES", "5.2 Abatteuse en Ratissage frappant une parcelle à 0 Arbre", 1.0, "EXCEPTION_RARE"),
    ("ok_contact_nid_renvois", "PISTE_MACHINES", "Contact Machine/Route-Nid : renvoi du Nid en lisière", 2.0, "EXCEPTION_RARE"),
    ("ok_contact_nid_insectes_perdus", "PISTE_MACHINES", "Contact Machine/Route-Nid : Insectes défaussés", 1.0, "STERILE_FRICTION"),
    ("ok_penurie_cartes_machine", "PISTE_MACHINES", "1.2 Pénurie de cartes Machine à la distribution", 0.0, "EXCEPTION_RARE"),
    ("ok_charge_activations", "CHARGE_ASSAUT", "5.1 Activations de machine en mode CHARGE", 0.0, "DIAGNOSTIC"),
    ("ok_charge_zero_gain", "CHARGE_ASSAUT", "5.1 Activation CHARGE à 0 gain de jeton Puissance", 0.0, "DIAGNOSTIC"),
    ("ok_charge_zero_gain_parried", "CHARGE_ASSAUT", "5.1 Activation CHARGE à 0 gain grâce aux Parades/Pièges", 0.0, "UTILE"),
    ("ok_charge_zero_gain_barren", "CHARGE_ASSAUT", "5.1 Activation CHARGE à 0 gain sur cible stérile / hors-plateau", 0.0, "STERILE_FRICTION"),
    ("ok_ratissage_entries_6_3", "PISTE_MACHINES", "6.3 Passage d'une machine en Ratissage en fin de tour", 1.0, "UTILE"),
    ("ok_ratissage_activations", "PISTE_MACHINES", "5.1/5.2 Frappes exécutées en mode Ratissage permanent", 0.0, "UTILE"),
    ("ok_mig_moves", "INSECTES_GARDIENS", "4.3 Migrations effectives d'Insectes (3 ops par jeton)", 3.0, "UTILE"),
    ("ok_mig_wasted_end", "INSECTES_GARDIENS", "Fin : Migrations d'Insectes restées inutilisées (gaspillage)", 3.0, "STERILE_FRICTION"),
    ("ok_bugs_unused_end", "INSECTES_GARDIENS", "Fin : Jetons Insectes Bug inutilisés sur piste Tactiques", 3.0, "STERILE_FRICTION"),
    ("ok_colonie_unused_end", "INSECTES_GARDIENS", "Fin : Jetons Bouclier de lisière inutilisés sur piste Gardiens", 3.0, "STERILE_FRICTION"),
    ("ok_insectes_foret_unused_end", "INSECTES_GARDIENS", "Fin : Jetons Insectes restant en Forêt", 1.0, "DIAGNOSTIC"),
    ("ok_bouclier_saves", "INSECTES_GARDIENS", "5.3 Gardien sauvé du retour en lisière par Bouclier", 1.0, "UTILE"),
    ("ok_gardien_return_lisiere", "INSECTES_GARDIENS", "5.3 Retour d'un Gardien en lisière sur pari perdu", 2.0, "UTILE"),
    ("ok_gardien_face2_upgrades", "INSECTES_GARDIENS", "5.3 Passage d'un Gardien en Face 2 sur pari gagné (Mode 3+)", 1.0, "UTILE"),
    ("ok_cascade_case4_openings", "INSECTES_GARDIENS", "Balayage : Ouvertures de 4. Gardien (Résonance)", 1.0, "UTILE"),
    ("ok_cascade_second_pass_sweeps", "INSECTES_GARDIENS", "Balayage : Cascades nécessitant un 2e passage 1->6", 0.0, "EXCEPTION_RARE"),
    ("ok_tour8_blocked_sommeil", "FINS_EXCEPTION", "5.3 Tour 8 bloquant un Sommeil réalisé au Tour 8", 0.0, "EXCEPTION_RARE"),
    ("ok_tour8_blocked_eveil", "FINS_EXCEPTION", "5.3 Tour 8 bloquant un Éveil réalisé au Tour 8", 0.0, "EXCEPTION_RARE"),
    ("ok_liberation_batisseur_3j", "FINS_EXCEPTION", "3.1 Libération d'1 bâtisseur à 3 joueurs", 1.0, "UTILE"),
    ("ok_def1_global_fallback", "FINS_EXCEPTION", "2.1 Repli anti-blocage portée globale du 1er Défenseur", 0.0, "EXCEPTION_RARE"),
    ("ok_impasse_totale", "FINS_EXCEPTION", "2.1/2.2 Impasse totale (0 cible légale sur tout le plateau)", 0.0, "EXCEPTION_RARE"),
)

_DILEMMA_BRANCH_SPECS: tuple[tuple[str, str, tuple[tuple[str, str], ...]], ...] = (
    (
        "3.2_bug_deviation",
        "3.2 Déviation Synaptique Bug (PASSER / M-1 / M+1)",
        (
            ("PASSER", "sum_dil_bug_passer"),
            ("M_MOINS_1", "sum_dil_bug_minus"),
            ("M_PLUS_1", "sum_dil_bug_plus"),
        ),
    ),
    (
        "4.1_furtivite_piege_vs_sabotage",
        "4.1 Rives Furtivité gagnées (Piège vs Sabotage)",
        (("PIEGE", "sum_ok_furt_rive_piege"), ("SABOTAGE", "sum_ok_furt_rive_sabotage")),
    ),
    (
        "4.3_migration_insecte",
        "4.3 Migration d'Insecte (>= 2 destinations légales)",
        (
            ("RESTER", "sum_dil_mig_stay"),
            ("FORET", "sum_dil_mig_foret"),
            ("BUG", "sum_dil_mig_bug"),
            ("COLONIE", "sum_dil_mig_colonie"),
        ),
    ),
    (
        "2.1_famille_cible_def1",
        "2.1 Pose du 1er Défenseur par famille de zone (Forêt / Lisière / Furtivité / Rêve)",
        (
            ("FORET", "sum_dil_def1_foret"),
            ("LISIERE", "sum_dil_def1_lisiere"),
            ("FURTIVITE", "sum_dil_def1_furtivite"),
            ("REVE", "sum_dil_def1_reve"),
        ),
    ),
    (
        "2.2_famille_cible_def2_final",
        "2.2 Destination verrouillée du 2e Défenseur",
        (
            ("FORET", "sum_dil_def2_foret"),
            ("LISIERE", "sum_dil_def2_lisiere"),
            ("FURTIVITE", "sum_dil_def2_furtivite"),
            ("REVE", "sum_dil_def2_reve"),
            ("GARDIEN", "sum_dil_def2_gardien"),
        ),
    ),
    (
        "2.2_revision_utile_par_tour",
        "2.2 Tours utilisant effectivement une révision mobile vs 0 mouvement",
        (
            ("AVEC_MOUVEMENT", "sum_dil_step2_turns_with_move"),
            ("ZERO_MOUVEMENT", "sum_dil_step2_turns_zero_move"),
        ),
    ),
    (
        "3.1_case_gardien",
        "3.1 Choix de la case 1..6 à la construction d'un Gardien (>= 2 cases libres)",
        (
            ("C1_PARADE", "sum_dil_gardien_c1"),
            ("C2_PIEGE", "sum_dil_gardien_c2"),
            ("C3_SABOTAGE", "sum_dil_gardien_c3"),
            ("C4_RESONANCE", "sum_dil_gardien_c4"),
            ("C5_REVE", "sum_dil_gardien_c5"),
            ("C6_INSECTE", "sum_dil_gardien_c6"),
        ),
    ),
)


def _build_acceptance_v6_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
    game_cvar20_by_vbn: dict[tuple[str, str, int], float] | None = None,
) -> dict[str, Any] | None:
    """Construit la couverture intégrale des Blocs 1 & 2 du Référentiel d'acceptation v6.x."""
    needed = {"has_insectes", "n_peuples_oniriques", "n_animaux_sauvages"}
    if not needed.issubset(cell_cols):
        return None

    cell_rows = _query_dicts(
        con,
        """
        SELECT
            variant_id,
            bot,
            n_players,
            n_animaux_sauvages,
            has_insectes,
            n_peuples_oniriques,
            n_games,
            sum_ratio_arbres * 1.0 / n_games AS table_mean_ratio
        FROM cells
        WHERE n_games > 0
        """,
    )
    if not cell_rows:
        return None

    # 1. Monotonie de la hiérarchie cognitive B0 < B1 < B2 (<= B3) par variante et par N
    bot_var_rows = _query_dicts(
        con,
        """
        SELECT
            variant_id,
            bot,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
            ROUND(SUM(sum_mem_debt) * 1.0 / SUM(n_games), 4) AS mean_mem_debt,
            ROUND(SUM(sum_fiddliness) / SUM(n_games), 3) AS mean_fiddliness_ops
        FROM cells
        GROUP BY variant_id, bot
        ORDER BY variant_id, bot
        """,
    )
    bot_var_n_rows = _query_dicts(
        con,
        """
        SELECT
            variant_id,
            n_players,
            bot,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres
        FROM cells
        GROUP BY variant_id, n_players, bot
        ORDER BY variant_id, n_players, bot
        """,
    )
    bv_map: dict[str, dict[str, dict[str, Any]]] = {}
    for r in bot_var_rows:
        bv_map.setdefault(str(r["variant_id"]), {})[str(r["bot"])] = r
    bvn_map: dict[tuple[str, int], dict[str, float]] = {}
    for r in bot_var_n_rows:
        bvn_map.setdefault((str(r["variant_id"]), int(r["n_players"])), {})[str(r["bot"])] = float(
            r["mean_ratio_arbres"]
        )

    hierarchy_by_variant: list[dict[str, Any]] = []
    for vid in sorted(bv_map):
        bdict = bv_map[vid]
        m_b0 = bdict.get("B0", {}).get("mean_ratio_arbres")
        m_b1 = bdict.get("B1", {}).get("mean_ratio_arbres")
        m_b2 = bdict.get("B2", {}).get("mean_ratio_arbres")
        m_b3 = bdict.get("B3", {}).get("mean_ratio_arbres")
        strict_global = True
        if m_b0 is not None and m_b1 is not None and not (float(m_b0) < float(m_b1)):
            strict_global = False
        if m_b1 is not None and m_b2 is not None and not (float(m_b1) < float(m_b2)):
            strict_global = False
        if m_b2 is not None and m_b3 is not None and not (float(m_b2) <= float(m_b3) + 0.005):
            strict_global = False

        per_n_checks: dict[str, Any] = {}
        for n_pl in (3, 4, 5, 6):
            nm = bvn_map.get((vid, n_pl))
            if not nm:
                continue
            ok_n = True
            if "B0" in nm and "B1" in nm and not (nm["B0"] < nm["B1"]):
                ok_n = False
            if "B1" in nm and "B2" in nm and not (nm["B1"] < nm["B2"]):
                ok_n = False
            per_n_checks[f"{n_pl}J"] = {**nm, "monotonic_b0_b1_b2": ok_n}

        hierarchy_by_variant.append(
            {
                "variant_id": vid,
                "bots": bdict,
                "strict_b0_lt_b1_lt_b2_global": strict_global,
                "zero_mem_debt_all_bots": all(
                    float(v.get("mean_mem_debt") or 0.0) == 0.0 for v in bdict.values()
                ),
                "by_n_players": per_n_checks,
            }
        )

    # 2. Ventilation d'équité dédiée sur B2 (et B3 si présent) par variante
    present_ref_bots = sorted(
        {str(r["bot"]) for r in cell_rows if str(r["bot"]) in ("B2", "B3")}
    )
    if not present_ref_bots:
        present_ref_bots = sorted({str(r["bot"]) for r in cell_rows})

    t_ratios_n: dict[tuple[str, str, int], list[float]] = {}
    t_ratios_a: dict[tuple[str, str, int], list[float]] = {}
    t_ratios_ins: dict[tuple[str, str, int], list[float]] = {}
    t_ratios_oni: dict[tuple[str, str, int], list[float]] = {}
    for r in cell_rows:
        b_s = str(r["bot"])
        if b_s not in present_ref_bots:
            continue
        v_s = str(r["variant_id"])
        mr = float(r["table_mean_ratio"])
        t_ratios_n.setdefault((b_s, v_s, int(r["n_players"])), []).append(mr)
        t_ratios_a.setdefault((b_s, v_s, int(r["n_animaux_sauvages"])), []).append(mr)
        t_ratios_ins.setdefault((b_s, v_s, int(r["has_insectes"])), []).append(mr)
        t_ratios_oni.setdefault((b_s, v_s, int(r["n_peuples_oniriques"])), []).append(mr)

    def _equity_axis_query(axis_col: str, bot_filter: str, vid_filter: str) -> list[dict[str, Any]]:
        safe_b = bot_filter.replace("'", "''")
        safe_v = vid_filter.replace("'", "''")
        return _query_dicts(
            con,
            f"""
            SELECT
                {axis_col} AS stratum,
                CAST(SUM(n_games) AS INTEGER) AS n_games,
                ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
                ROUND(SUM(cvar20_ratio * n_games) / SUM(n_games), 4) AS cvar20_ratio,
                ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
                ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
                ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
                ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
            FROM cells
            WHERE bot = '{safe_b}' AND variant_id = '{safe_v}'
            GROUP BY {axis_col}
            ORDER BY {axis_col}
            """,
        )

    equity_blocks: list[dict[str, Any]] = []
    distinct_vids = sorted({str(r["variant_id"]) for r in cell_rows})
    for b_ref in present_ref_bots:
        for vid in distinct_vids:
            rows_n = _equity_axis_query("n_players", b_ref, vid)
            if not rows_n:
                continue
            for rn in rows_n:
                n_str = int(rn["stratum"])
                rn["table_cvar20_ratio"] = _cvar_bottom_values(
                    t_ratios_n.get((b_ref, vid, n_str), []), 0.20
                )
                rn["game_cvar20_ratio"] = (
                    game_cvar20_by_vbn[(vid, b_ref, n_str)]
                    if (game_cvar20_by_vbn is not None and (vid, b_ref, n_str) in game_cvar20_by_vbn)
                    else rn["cvar20_ratio"]
                )
            rows_a = _equity_axis_query("n_animaux_sauvages", b_ref, vid)
            for ra in rows_a:
                ra["table_cvar20_ratio"] = _cvar_bottom_values(
                    t_ratios_a.get((b_ref, vid, int(ra["stratum"])), []), 0.20
                )
            rows_ins = _equity_axis_query("has_insectes", b_ref, vid)
            for ri in rows_ins:
                ri["label"] = "AVEC_INSECTES" if int(ri["stratum"]) == 1 else "SANS_INSECTES"
                ri["table_cvar20_ratio"] = _cvar_bottom_values(
                    t_ratios_ins.get((b_ref, vid, int(ri["stratum"])), []), 0.20
                )
            rows_oni = _equity_axis_query("n_peuples_oniriques", b_ref, vid)
            for ro in rows_oni:
                ro["table_cvar20_ratio"] = _cvar_bottom_values(
                    t_ratios_oni.get((b_ref, vid, int(ro["stratum"])), []), 0.20
                )

            n_means = [float(r["mean_ratio_arbres"]) for r in rows_n]
            n_cvars = [float(r["table_cvar20_ratio"]) for r in rows_n]
            a_means = [float(r["mean_ratio_arbres"]) for r in rows_a if int(r["stratum"]) >= 1]
            ins_map = {int(r["stratum"]): float(r["mean_ratio_arbres"]) for r in rows_ins}
            oni_map = {int(r["stratum"]): float(r["mean_ratio_arbres"]) for r in rows_oni}

            equity_blocks.append(
                {
                    "bot": b_ref,
                    "variant_id": vid,
                    "by_n_players": rows_n,
                    "spread_n_players_ratio": round(max(n_means) - min(n_means), 4)
                    if len(n_means) >= 2
                    else 0.0,
                    "spread_n_players_table_cvar20": round(max(n_cvars) - min(n_cvars), 4)
                    if len(n_cvars) >= 2
                    else 0.0,
                    "by_n_animaux_sauvages": rows_a,
                    "spread_animaux_1_to_3_ratio": round(max(a_means) - min(a_means), 4)
                    if len(a_means) >= 2
                    else 0.0,
                    "by_has_insectes": rows_ins,
                    "delta_insectes_with_minus_without": round(ins_map[1] - ins_map[0], 4)
                    if (0 in ins_map and 1 in ins_map)
                    else None,
                    "by_n_peuples_oniriques": rows_oni,
                    "delta_oniriques_2_minus_1": round(oni_map[2] - oni_map[1], 4)
                    if (1 in oni_map and 2 in oni_map)
                    else None,
                }
            )

    return {
        "bot_hierarchy_and_cognition": hierarchy_by_variant,
        "equity_by_bot_x_variant": equity_blocks,
    }


def _build_sommeil_temporality_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
) -> dict[str, Any] | None:
    """Construit la temporalité complète T1..T7 des Sommeils (% avant Tour 5 + ratio exact 6J / 3J)."""
    t_cols = tuple(f"sommeil_t{t}" for t in range(1, 8))
    if not all(c in cell_cols for c in t_cols):
        return None

    sum_sql = """
        CAST(SUM(n_games) AS INTEGER) AS n_games,
        CAST(SUM(count_reve_rang_1) AS INTEGER) AS count_sommeil,
        SUM(sum_sommeil_tours) AS sum_sommeil_tours,
        SUM(sum_sommeil_ratio_arbres) AS sum_sommeil_ratio_arbres,
        CAST(SUM(sommeil_t1) AS INTEGER) AS t1,
        CAST(SUM(sommeil_t2) AS INTEGER) AS t2,
        CAST(SUM(sommeil_t3) AS INTEGER) AS t3,
        CAST(SUM(sommeil_t4) AS INTEGER) AS t4,
        CAST(SUM(sommeil_t5) AS INTEGER) AS t5,
        CAST(SUM(sommeil_t6) AS INTEGER) AS t6,
        CAST(SUM(sommeil_t7) AS INTEGER) AS t7
    """

    def _fmt_sommeil(r: dict[str, Any]) -> dict[str, Any]:
        ng = max(1, int(r["n_games"]))
        cs = int(r["count_sommeil"] or 0)
        counts = {f"T{t}": int(r[f"t{t}"] or 0) for t in range(1, 8)}
        before_t5 = counts["T1"] + counts["T2"] + counts["T3"] + counts["T4"]
        return {
            "n_games": int(r["n_games"]),
            "count_sommeil": cs,
            "pct_sommeil": round(cs * 100.0 / ng, 2),
            "mean_sommeil_tour": round(float(r["sum_sommeil_tours"] or 0) / cs, 3)
            if cs > 0
            else 0.0,
            "mean_sommeil_ratio_arbres": round(
                float(r["sum_sommeil_ratio_arbres"] or 0.0) / cs, 4
            )
            if cs > 0
            else 0.0,
            "pct_before_t5_of_sommeil": round(before_t5 * 100.0 / cs, 2) if cs > 0 else 0.0,
            "pct_before_t5_of_all_games": round(before_t5 * 100.0 / ng, 2),
            "tour_counts": counts,
            "tour_pct_of_sommeil": {
                k: (round(v * 100.0 / cs, 2) if cs > 0 else 0.0) for k, v in counts.items()
            },
        }

    g_raw = _query_dicts(con, f"SELECT {sum_sql} FROM cells")[0]
    by_vbn_raw = _query_dicts(
        con,
        f"""
        SELECT variant_id, bot, n_players, {sum_sql}
        FROM cells
        GROUP BY variant_id, bot, n_players
        ORDER BY variant_id, bot, n_players
        """,
    )
    by_vb_raw = _query_dicts(
        con,
        f"""
        SELECT variant_id, bot, {sum_sql}
        FROM cells
        GROUP BY variant_id, bot
        ORDER BY variant_id, bot
        """,
    )

    pct_map_all: dict[tuple[str, str, int], float] = {}
    formatted_vbn: list[dict[str, Any]] = []
    for r in by_vbn_raw:
        fmt = _fmt_sommeil(r)
        vid = str(r["variant_id"])
        bot_s = str(r["bot"])
        n_pl = int(r["n_players"])
        pct_map_all[(vid, bot_s, n_pl)] = fmt["pct_sommeil"]
        formatted_vbn.append({"variant_id": vid, "bot": bot_s, "n_players": n_pl, **fmt})

    pct_map_oniric: dict[tuple[str, str, int], float] = {}
    if "n_peuples_oniriques" in cell_cols:
        oni_rows = _query_dicts(
            con,
            """
            SELECT
                variant_id,
                bot,
                n_players,
                ROUND(SUM(count_reve_rang_1) * 100.0 / NULLIF(SUM(n_games), 0), 4) AS pct_som
            FROM cells
            WHERE n_peuples_oniriques >= 1
            GROUP BY variant_id, bot, n_players
            """,
        )
        for ro in oni_rows:
            if ro["pct_som"] is not None:
                pct_map_oniric[
                    (str(ro["variant_id"]), str(ro["bot"]), int(ro["n_players"]))
                ] = float(ro["pct_som"])

    summary_vb: list[dict[str, Any]] = []
    for r in by_vb_raw:
        vid = str(r["variant_id"])
        bot_s = str(r["bot"])
        fmt = _fmt_sommeil(r)
        p3 = pct_map_all.get((vid, bot_s, 3))
        p6 = pct_map_all.get((vid, bot_s, 6))
        ratio_6_3 = (
            round(p6 / p3, 3)
            if (p3 is not None and p6 is not None and p3 > 0.0)
            else ("INF" if (p3 == 0.0 and p6 is not None and p6 > 0.0) else None)
        )
        p3_oni = pct_map_oniric.get((vid, bot_s, 3))
        p6_oni = pct_map_oniric.get((vid, bot_s, 6))
        ratio_6_3_oni = (
            round(p6_oni / p3_oni, 3)
            if (p3_oni is not None and p6_oni is not None and p3_oni > 0.0)
            else ("INF" if (p3_oni == 0.0 and p6_oni is not None and p6_oni > 0.0) else None)
        )
        summary_vb.append(
            {
                "variant_id": vid,
                "bot": bot_s,
                **fmt,
                "pct_sommeil_3j": p3,
                "pct_sommeil_6j": p6,
                "ratio_6j_over_3j": ratio_6_3,
                "ratio_6j_over_3j_oniric_tables": ratio_6_3_oni,
            }
        )

    out_som: dict[str, Any] = {
        "global": _fmt_sommeil(g_raw),
        "by_variant_x_bot": summary_vb,
    }
    active_som_vbn = [row for row in formatted_vbn if int(row.get("count_sommeil") or 0) > 0]
    if active_som_vbn:
        out_som["by_variant_x_bot_x_n_players"] = active_som_vbn
    return out_som


def _build_charge_assaut_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
) -> dict[str, Any] | None:
    """Construit les métriques Charge/Assaut normalisées par machine (2*N) ventilées par bot x n_players."""
    req = {
        "sum_power_tokens_end_act1",
        "count_act1_reached",
        "sum_power_tokens_end_game",
        "count_charge_gains",
        "count_charge_gains_act1",
        "count_charge_gains_act2",
    }
    if not req.issubset(cell_cols):
        return None

    def _fmt_charge_rows(group_cols: str) -> list[dict[str, Any]]:
        rows = _query_dicts(
            con,
            f"""
            SELECT
                {group_cols},
                CAST(SUM(n_games) AS INTEGER) AS n_games,
                CAST(SUM(count_act1_reached) AS INTEGER) AS act1_reached,
                SUM(sum_power_tokens_end_act1) AS sum_tok_act1,
                SUM(sum_power_tokens_end_game) AS sum_tok_end,
                SUM(count_charge_gains) AS gains_total,
                SUM(count_charge_gains_act1) AS gains_act1,
                SUM(count_charge_gains_act2) AS gains_act2
            FROM cells
            GROUP BY {group_cols}
            ORDER BY {group_cols}
            """,
        )
        out_list: list[dict[str, Any]] = []
        for r in rows:
            n_pl = int(r["n_players"])
            n_mach = 2 * n_pl
            ng = max(1, int(r["n_games"]))
            a1_n = int(r["act1_reached"] or 0)
            tok_m_act1 = (
                round(float(r["sum_tok_act1"] or 0) / (a1_n * n_mach), 4) if a1_n > 0 else 0.0
            )
            tok_m_end = round(float(r["sum_tok_end"] or 0) / (ng * n_mach), 4)
            g_tot = int(r["gains_total"] or 0)
            g_a1 = int(r["gains_act1"] or 0)
            g_a2 = int(r["gains_act2"] or 0)
            entry: dict[str, Any] = {}
            if "variant_id" in r:
                entry["variant_id"] = str(r["variant_id"])
            entry.update(
                {
                    "bot": str(r["bot"]),
                    "n_players": n_pl,
                    "n_machines": n_mach,
                    "n_games": int(r["n_games"]),
                    "tokens_per_machine_end_act1": tok_m_act1,
                    "tokens_per_machine_end_game": tok_m_end,
                    "ratio_tokens_act1_over_end_game": round(tok_m_act1 / tok_m_end, 4)
                    if tok_m_end > 0
                    else 0.0,
                    "charge_gains_per_machine_act1": round(g_a1 / (ng * n_mach), 4),
                    "charge_gains_per_machine_act2": round(g_a2 / (ng * n_mach), 4),
                    "charge_gains_per_machine_total": round(g_tot / (ng * n_mach), 4),
                    "share_charge_gains_act1_pct": round(g_a1 * 100.0 / g_tot, 2)
                    if g_tot > 0
                    else 0.0,
                }
            )
            out_list.append(entry)
        return out_list

    by_bn = _fmt_charge_rows("bot, n_players")
    out_ca: dict[str, Any] = {"by_bot_x_n_players": by_bn}
    n_vars_ca = int(
        _query_dicts(con, "SELECT COUNT(DISTINCT variant_id) AS nv FROM cells")[0]["nv"] or 0
    )
    if n_vars_ca > 1:
        out_ca["by_variant_x_bot_x_n_players"] = _fmt_charge_rows("variant_id, bot, n_players")
    return out_ca


def _build_furtivite_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
) -> dict[str, Any] | None:
    """Contrôle la fréquence de Furtivité par partie (binômes Piège vs Sabotage, pions orphelins)."""
    req = {
        "count_furtivite_1_rive_turns",
        "sum_ok_furt_rive_piege",
        "sum_ok_furt_rive_sabotage",
        "sum_ok_furt_orphan_pawns",
        "games_ok_furt_orphan_pawns",
        "sum_ok_furt_failed_binomes",
        "games_ok_furt_failed_binomes",
    }
    if not req.issubset(cell_cols):
        return None

    extra_piege_lost_sql = (
        "SUM(sum_ok_furt_rive_piege_lost)"
        if "sum_ok_furt_rive_piege_lost" in cell_cols
        else "0"
    )
    extra_sab_lost_sql = (
        "SUM(sum_ok_furt_rive_sabotage_lost)"
        if "sum_ok_furt_rive_sabotage_lost" in cell_cols
        else "0"
    )
    extra_p_placed_sql = (
        "SUM(sum_ok_pieges_placed)" if "sum_ok_pieges_placed" in cell_cols else "0"
    )
    extra_p_trig_sql = (
        "SUM(sum_ok_pieges_triggered)" if "sum_ok_pieges_triggered" in cell_cols else "0"
    )

    def _fmt_furt(group_cols: str | None) -> list[dict[str, Any]]:
        grp_sel = f"{group_cols}," if group_cols else ""
        grp_by = f"GROUP BY {group_cols} ORDER BY {group_cols}" if group_cols else ""
        rows = _query_dicts(
            con,
            f"""
            SELECT
                {grp_sel}
                CAST(SUM(n_games) AS INTEGER) AS n_games,
                SUM(count_furtivite_1_rive_turns) AS t_1_rive,
                SUM(sum_ok_furt_rive_piege) AS r_piege,
                SUM(sum_ok_furt_rive_sabotage) AS r_sabotage,
                {extra_piege_lost_sql} AS r_piege_lost,
                {extra_sab_lost_sql} AS r_sab_lost,
                {extra_p_placed_sql} AS p_placed,
                {extra_p_trig_sql} AS p_trig,
                SUM(sum_ok_furt_orphan_pawns) AS orphans,
                SUM(games_ok_furt_orphan_pawns) AS g_orphans,
                SUM(sum_ok_furt_failed_binomes) AS failed_bin,
                SUM(games_ok_furt_failed_binomes) AS g_failed_bin
            FROM cells
            {grp_by}
            """,
        )
        out_l: list[dict[str, Any]] = []
        for r in rows:
            ng = max(1, int(r["n_games"]))
            rp = int(r["r_piege"] or 0)
            rs = int(r["r_sabotage"] or 0)
            rp_l = int(r["r_piege_lost"] or 0)
            rs_l = int(r["r_sab_lost"] or 0)
            rtot = rp + rs
            entry: dict[str, Any] = {}
            if group_cols:
                for col_name in [c.strip() for c in group_cols.split(",")]:
                    entry[col_name] = (
                        int(r[col_name]) if col_name == "n_players" else str(r[col_name])
                    )
            entry.update(
                {
                    "n_games": int(r["n_games"]),
                    "turns_1_rive_per_game": round(int(r["t_1_rive"] or 0) / ng, 4),
                    "rives_piege_per_game": round(rp / ng, 4),
                    "rives_piege_lost_per_game": round(rp_l / ng, 4),
                    "win_rate_rive_piege_pct": round(rp * 100.0 / (rp + rp_l), 2)
                    if (rp + rp_l) > 0
                    else 0.0,
                    "rives_sabotage_per_game": round(rs / ng, 4),
                    "rives_sabotage_lost_per_game": round(rs_l / ng, 4),
                    "win_rate_rive_sabotage_pct": round(rs * 100.0 / (rs + rs_l), 2)
                    if (rs + rs_l) > 0
                    else 0.0,
                    "share_sabotage_of_rives_pct": round(rs * 100.0 / rtot, 2)
                    if rtot > 0
                    else 0.0,
                    "pieges_placed_per_game": round(int(r["p_placed"] or 0) / ng, 4),
                    "pieges_triggered_per_game": round(int(r["p_trig"] or 0) / ng, 4),
                    "orphan_pawns_per_game": round(int(r["orphans"] or 0) / ng, 4),
                    "pct_games_with_orphan_pawn": round(
                        int(r["g_orphans"] or 0) * 100.0 / ng, 2
                    ),
                    "failed_binomes_per_game": round(int(r["failed_bin"] or 0) / ng, 4),
                    "pct_games_with_failed_binome": round(
                        int(r["g_failed_bin"] or 0) * 100.0 / ng, 2
                    ),
                }
            )
            out_l.append(entry)
        return out_l

    by_vb_furt = _fmt_furt("variant_id, bot")
    out_fu: dict[str, Any] = {
        "global": _fmt_furt(None)[0],
        "by_bot_x_n_players": _fmt_furt("bot, n_players"),
    }
    if len(by_vb_furt) > 1:
        out_fu["by_variant_x_bot"] = by_vb_furt
    return out_fu


_NATURE_SHORT: dict[str, str] = {
    "UTILE": "UTILE",
    "STERILE_FRICTION": "STERILE",
    "EXCEPTION_RARE": "RARE",
    "DIAGNOSTIC": "DIAG",
}


def _build_ockham_razor_block(
    con: duckdb.DuckDBPyConnection,
    cell_cols: set[str],
) -> dict[str, Any] | None:
    """Cartographie Rasoir d'Ockham compacte : 37 micro-règles vivantes + 7 embranchements."""
    sum_ok_cols = [f"sum_{k}" for k in OCKHAM_COUNT_FIELDS]
    games_ok_cols = [f"games_{k}" for k in OCKHAM_COUNT_FIELDS]
    sum_dil_cols = [f"sum_{k}" for k in DILEMMA_CHOICE_FIELDS]
    if not all(c in cell_cols for c in sum_ok_cols[:4]):
        return None

    all_acc_cols = [
        c for c in [*sum_ok_cols, *games_ok_cols, *sum_dil_cols] if c in cell_cols
    ]
    sel_sql = ",\n            ".join(
        f"CAST(COALESCE(SUM({c}), 0) AS BIGINT) AS {c}" for c in all_acc_cols
    )

    def _compile_ockham_profile(where_clause: str) -> dict[str, Any] | None:
        rows = _query_dicts(
            con,
            f"""
            SELECT
                CAST(COALESCE(SUM(n_games), 0) AS INTEGER) AS n_games,
                {sel_sql}
            FROM cells
            {where_clause}
            """,
        )
        if not rows or int(rows[0]["n_games"] or 0) <= 0:
            return None
        r = rows[0]
        ng = int(r["n_games"])

        # Dictionnaire compact sans perte : ok_key -> [mean_per_game, pct_games_concerned, mean_ops, nature, candidate]
        micro_rules: dict[str, list[Any]] = {}
        simplifiable_candidates: list[str] = []
        for ok_key, _cat, _label, ops_unit, nature in _OCKHAM_RULES_CATALOG:
            s_col = f"sum_{ok_key}"
            g_col = f"games_{ok_key}"
            if s_col not in r:
                continue
            tot_cnt = int(r.get(s_col) or 0)
            g_cnt = int(r.get(g_col) or 0)
            mean_pg = round(tot_cnt / ng, 4)
            pct_g = round(g_cnt * 100.0 / ng, 2)
            mean_ops = round(mean_pg * ops_unit, 4)
            is_cand = (nature == "EXCEPTION_RARE" and pct_g < 5.0) or (
                nature == "STERILE_FRICTION" and (pct_g >= 10.0 or mean_pg >= 0.25)
            )
            if is_cand:
                simplifiable_candidates.append(ok_key)
            micro_rules[ok_key] = [
                mean_pg,
                pct_g,
                mean_ops,
                _NATURE_SHORT.get(nature, nature),
                is_cand,
            ]

        dilemmas: dict[str, dict[str, Any]] = {}
        flagged_false_dilemmas: list[str] = []
        for branch_id, _branch_label, opt_specs in _DILEMMA_BRANCH_SPECS:
            counts_map: dict[str, int] = {}
            tot_branch = 0
            for opt_name, col_name in opt_specs:
                val = int(r.get(col_name) or 0)
                counts_map[opt_name] = val
                tot_branch += val
            shares_pct = {
                opt_n: (round(cnt_v * 100.0 / tot_branch, 2) if tot_branch > 0 else 0.0)
                for opt_n, cnt_v in counts_map.items()
            }
            if tot_branch > 0:
                dom_opt, dom_pct = max(shares_pct.items(), key=lambda kv: kv[1])
            else:
                dom_opt, dom_pct = ("NONE", 0.0)
            is_false = tot_branch >= 20 and dom_pct > 90.0
            if is_false:
                flagged_false_dilemmas.append(f"{branch_id}:{dom_opt}={dom_pct}%")
            dilemmas[branch_id] = {
                "n": tot_branch,
                "per_game": round(tot_branch / ng, 3),
                "shares_pct": shares_pct,
                "dominant": dom_opt,
                "dominant_pct": dom_pct,
                "false_dilemma_gt90": is_false,
            }

        order_prompts = {
            "constr_3_1": round(int(r.get("sum_dil_ordre_constr_3_1") or 0) / ng, 4),
            "nids_4_2": round(int(r.get("sum_dil_ordre_nid_4_2") or 0) / ng, 4),
            "attaque_5_1": round(int(r.get("sum_dil_ordre_att_5_1") or 0) / ng, 4),
            "ratissage_5_2": round(int(r.get("sum_dil_ordre_rat_5_2") or 0) / ng, 4),
        }

        return {
            "n_games": ng,
            "simplifiable_candidates": simplifiable_candidates,
            "flagged_false_dilemmas_gt90": flagged_false_dilemmas,
            "order_tiebreak_prompts": order_prompts,
            "micro_rules": micro_rules,
            "decision_branches": dilemmas,
        }

    b2_prof = _compile_ockham_profile("WHERE bot = 'B2'")
    global_prof = _compile_ockham_profile("")
    by_bot_names = [
        str(x["bot"])
        for x in _query_dicts(con, "SELECT DISTINCT bot FROM cells ORDER BY bot")
    ]
    out_ok: dict[str, Any] = {
        "reference_policy": "B2" if b2_prof is not None else "GLOBAL",
        "micro_rule_tuple_schema": [
            "mean_per_game",
            "pct_games_concerned",
            "mean_ops_per_game",
            "nature",
            "ockham_candidate",
        ],
        "primary": b2_prof if b2_prof is not None else global_prof,
    }
    if len(by_bot_names) > 1:
        by_bot_summary: dict[str, Any] = {}
        for b_nm in by_bot_names:
            safe_b = b_nm.replace("'", "''")
            prof_b = _compile_ockham_profile(f"WHERE bot = '{safe_b}'")
            if prof_b is not None:
                by_bot_summary[b_nm] = {
                    "n_games": prof_b["n_games"],
                    "simplifiable_candidates": prof_b["simplifiable_candidates"],
                    "flagged_false_dilemmas_gt90": prof_b["flagged_false_dilemmas_gt90"],
                    "order_tiebreak_prompts": prof_b["order_tiebreak_prompts"],
                }
        out_ok["by_bot_overview"] = by_bot_summary
    return out_ok


def _active_slots_for_peuples_circle(peuples_str: str) -> set[str]:
    """Retourne l'ensemble des emplacements (parmi les 32) effectivement actifs sur ce cercle."""
    peuples = tuple(p.strip().upper() for p in peuples_str.split("-") if p.strip())
    n = len(peuples)
    active: set[str] = set()
    if n >= 3:
        for i in range(n):
            pair_key = f"{peuples[i]}_{peuples[(i + 1) % n]}"
            pair_tiles = MATRICE_PAIRES.get(pair_key)
            if pair_tiles:
                active.add(pair_tiles[0])
                active.add(pair_tiles[1])
    if "I" in peuples:
        active.add("SLOT_BUG_CERVEAU")
        if any(p in ANIMAUX_SAUVAGES for p in peuples):
            active.add("SLOT_COLONISATION_GARDIENS")
    return active


def _parse_json_dict(raw: Any) -> dict[str, Any]:
    if not raw:
        return {}
    if isinstance(raw, dict):
        return raw
    try:
        parsed = json.loads(str(raw))
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError):
        return {}


def _parse_bp_list(raw: Any) -> list[int] | None:
    if not raw:
        return None
    if isinstance(raw, list):
        return [int(x) for x in raw]
    try:
        parsed = json.loads(str(raw))
        if isinstance(parsed, list) and parsed:
            return [int(x) for x in parsed]
    except (TypeError, ValueError):
        return None
    return None


def _extract_cell_diffs_pair(row_var: dict[str, Any], row_ref: dict[str, Any]) -> list[float]:
    """Extrait les différences appariées jeu-à-jeu (CRN) entre deux cellules sur la même table."""
    bp_v = _parse_bp_list(row_var.get("rep_ratios_bp_json"))
    bp_r = _parse_bp_list(row_ref.get("rep_ratios_bp_json"))
    if bp_v is not None and bp_r is not None and len(bp_v) == len(bp_r) and bp_v:
        return [(a - b) / 10000.0 for a, b in zip(bp_v, bp_r, strict=True)]
    nv = max(1, int(row_var.get("n_games") or 1))
    nr = max(1, int(row_ref.get("n_games") or 1))
    mv = float(row_var.get("sum_ratio_arbres") or 0.0) / nv
    mr = float(row_ref.get("sum_ratio_arbres") or 0.0) / nr
    return [mv - mr] * min(nv, nr)


def _build_weighted_circle_dispersion(
    cell_rows: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, dict[str, Any]]]:
    """Calcule la moyenne pondérée et la dispersion inter-cercles (explicite non estimable si 1 cercle)."""
    # Agrégation exacte par cercle orienté `peuples` (poids = n_games) -> moyenne globale unifiée avec totals
    by_circle_global: dict[str, list[float]] = {}
    by_n_circle: dict[int, dict[str, list[float]]] = {}
    by_bn_circle: dict[tuple[str, int], dict[str, list[float]]] = {}
    by_var_circle: dict[str, dict[str, list[float]]] = {}

    for r in cell_rows:
        ng = int(r.get("n_games") or 0)
        if ng <= 0:
            continue
        sr = float(r.get("sum_ratio_arbres") or 0.0)
        circle_key = str(r.get("peuples") or r.get("table_id") or "")
        n_pl = int(r["n_players"])
        bot_s = str(r["bot"])
        vid = str(r["variant_id"])

        for bucket, k in (
            (by_circle_global, circle_key),
            (by_n_circle.setdefault(n_pl, {}), circle_key),
            (by_bn_circle.setdefault((bot_s, n_pl), {}), circle_key),
            (by_var_circle.setdefault(vid, {}), circle_key),
        ):
            acc = bucket.get(k)
            if acc is None:
                bucket[k] = [sr, float(ng)]
            else:
                acc[0] += sr
                acc[1] += float(ng)

    def _summarize_circle_map(cmap: dict[str, list[float]]) -> dict[str, Any]:
        means: list[float] = []
        weights: list[int] = []
        for c_key in sorted(cmap):
            sr_c, ng_c = cmap[c_key]
            w_i = round(ng_c)
            if w_i > 0:
                means.append(sr_c / w_i)
                weights.append(w_i)
        return _inter_block_ci95(means, weights)

    global_disp = _summarize_circle_map(by_circle_global)
    by_n_disp = {str(n_pl): _summarize_circle_map(by_n_circle[n_pl]) for n_pl in sorted(by_n_circle)}
    by_bn_disp = [
        {"bot": bot_s, "n_players": n_pl, **_summarize_circle_map(by_bn_circle[(bot_s, n_pl)])}
        for (bot_s, n_pl) in sorted(by_bn_circle)
    ]
    by_var_disp = {vid: _summarize_circle_map(by_var_circle[vid]) for vid in sorted(by_var_circle)}

    inter_block_intervals: dict[str, Any] = {
        "global": global_disp,
        "by_n_players": by_n_disp,
    }
    circle_dispersion: dict[str, Any] = {
        "global": global_disp,
        "by_n_players": by_n_disp,
        "by_bot_x_n_players": by_bn_disp,
    }
    return inter_block_intervals, circle_dispersion, by_var_disp


def _build_stratified_cvar_bootstrap(
    cell_rows: list[dict[str, Any]],
    *,
    alpha: float = 0.20,
    n_boot: int = 300,
    seed: int = 20261201,
) -> dict[str, Any]:
    """Calcule la CVaR directe (alpha uniforme) et son IC 95 % bootstrap sur chaque strate."""
    global_clusters: dict[str, dict[int, int]] = {}
    by_mode: dict[tuple[int, str], dict[str, dict[int, int]]] = {}
    by_n: dict[int, dict[str, dict[int, int]]] = {}
    by_anim: dict[int, dict[str, dict[int, int]]] = {}
    by_var: dict[str, dict[str, dict[int, int]]] = {}
    by_var_n: dict[tuple[str, int], dict[str, dict[int, int]]] = {}
    by_vbn: dict[tuple[str, str, int], dict[str, dict[int, int]]] = {}
    by_var_anim: dict[tuple[str, int], dict[str, dict[int, int]]] = {}

    has_any_hist = False
    for r in cell_rows:
        raw_h = r.get("ratio_bp_counts_json")
        if not raw_h:
            continue
        parsed_h = _parse_json_dict(raw_h)
        if not parsed_h:
            continue
        has_any_hist = True
        hist = {int(k): int(v) for k, v in parsed_h.items() if int(v) > 0}
        if not hist:
            continue

        circle_k = str(r.get("peuples") or r.get("table_id") or "")
        mode_i = int(r["mode"])
        bot_s = str(r["bot"])
        n_pl = int(r["n_players"])
        vid = str(r["variant_id"])

        def _merge(target: dict[str, dict[int, int]], c_key: str, h_add: dict[int, int]) -> None:
            dst = target.setdefault(c_key, {})
            for bp_v, cnt_v in h_add.items():
                dst[bp_v] = dst.get(bp_v, 0) + cnt_v

        _merge(global_clusters, circle_k, hist)
        _merge(by_mode.setdefault((mode_i, bot_s), {}), circle_k, hist)
        _merge(by_n.setdefault(n_pl, {}), circle_k, hist)
        _merge(by_var.setdefault(vid, {}), circle_k, hist)
        _merge(by_var_n.setdefault((vid, n_pl), {}), circle_k, hist)
        _merge(by_vbn.setdefault((vid, bot_s, n_pl), {}), circle_k, hist)
        if r.get("n_animaux_sauvages") is not None:
            na = int(r["n_animaux_sauvages"])
            _merge(by_anim.setdefault(na, {}), circle_k, hist)
            _merge(by_var_anim.setdefault((vid, na), {}), circle_k, hist)

    if not has_any_hist:
        return {"has_hist": False}

    def _run_boot(cmap: dict[str, dict[int, int]], salt: int) -> dict[str, Any]:
        ordered = [cmap[k] for k in sorted(cmap)]
        return cvar_with_bootstrap_ci95(
            ordered, alpha=alpha, n_boot=n_boot, seed=(seed ^ salt) & 0x7FFFFFFF
        )

    return {
        "has_hist": True,
        "global": _run_boot(global_clusters, 101),
        "by_mode": {k: _run_boot(v, 200 + i) for i, (k, v) in enumerate(sorted(by_mode.items()))},
        "by_n": {k: _run_boot(v, 300 + i) for i, (k, v) in enumerate(sorted(by_n.items()))},
        "by_anim": {k: _run_boot(v, 400 + i) for i, (k, v) in enumerate(sorted(by_anim.items()))},
        "by_variant": {k: _run_boot(v, 500 + i) for i, (k, v) in enumerate(sorted(by_var.items()))},
        "by_variant_n": {
            k: _run_boot(v, 600 + i) for i, (k, v) in enumerate(sorted(by_var_n.items()))
        },
        "by_vbn": {k: _run_boot(v, 700 + i) for i, (k, v) in enumerate(sorted(by_vbn.items()))},
        "by_variant_anim": {
            k: _run_boot(v, 800 + i) for i, (k, v) in enumerate(sorted(by_var_anim.items()))
        },
    }


def _build_paired_comparisons_block(
    cell_rows: list[dict[str, Any]],
    *,
    reference_variant_id: str,
    by_variant_rows: list[dict[str, Any]],
    circle_ci_by_variant: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    """Construit les différences appariées + IC 95 % groupés par table, correction Holm et stabilité panel."""
    if not cell_rows:
        return None

    distinct_variants = sorted({str(r["variant_id"]) for r in cell_rows})
    distinct_bots = sorted({str(r["bot"]) for r in cell_rows})
    ref_vid = (
        reference_variant_id
        if reference_variant_id in distinct_variants
        else ("BASE" if "BASE" in distinct_variants else distinct_variants[0])
    )

    # Indexation CRN : (variant_id, bot, n_players, table_id, exp_seed, rep_start) -> row
    indexed: dict[tuple[str, str, int, str, int, int], dict[str, Any]] = {}
    for r in cell_rows:
        key = (
            str(r["variant_id"]),
            str(r["bot"]),
            int(r["n_players"]),
            str(r.get("table_id") or r.get("peuples") or ""),
            int(r.get("exp_seed") or 0),
            int(r.get("rep_start") or 0),
        )
        indexed[key] = r

    vs_ref_entries: list[dict[str, Any]] = []
    p_items_global: list[tuple[str, float | None]] = []

    if len(distinct_variants) >= 2:
        for vid in distinct_variants:
            if vid == ref_vid:
                continue
            diffs_all_by_tbl: dict[tuple[int, str], list[float]] = {}
            diffs_by_bot: dict[str, dict[tuple[int, str], list[float]]] = {}
            diffs_by_bn: dict[tuple[str, int], dict[str, list[float]]] = {}

            for (v_k, b_k, n_k, t_k, s_k, rs_k), row_v in indexed.items():
                if v_k != vid:
                    continue
                row_ref = indexed.get((ref_vid, b_k, n_k, t_k, s_k, rs_k))
                if row_ref is None:
                    continue
                d_list = _extract_cell_diffs_pair(row_v, row_ref)
                diffs_all_by_tbl.setdefault((n_k, t_k), []).extend(d_list)
                diffs_by_bot.setdefault(b_k, {}).setdefault((n_k, t_k), []).extend(d_list)
                diffs_by_bn.setdefault((b_k, n_k), {}).setdefault(t_k, []).extend(d_list)

            glob_stat = paired_diff_cluster_ci95(diffs_all_by_tbl)
            bot_stats = {
                b_s: paired_diff_cluster_ci95(diffs_by_bot[b_s]) for b_s in sorted(diffs_by_bot)
            }
            bn_list = [
                {"bot": b_s, "n_players": n_pl, **paired_diff_cluster_ci95(diffs_by_bn[(b_s, n_pl)])}
                for (b_s, n_pl) in sorted(diffs_by_bn)
            ]
            sign_stab = assess_sign_stability(bot_stats)
            p_items_global.append((vid, glob_stat.get("p_value")))
            vs_ref_entries.append(
                {
                    "variant_id": vid,
                    "reference_variant_id": ref_vid,
                    "global": glob_stat,
                    "by_bot": bot_stats,
                    "by_bot_x_n_players": bn_list,
                    "sign_stability_b1_b2_open": sign_stab,
                }
            )

        holm_map = holm_bonferroni_adjust(p_items_global, alpha=0.05)
        for entry in vs_ref_entries:
            h_res = holm_map.get(str(entry["variant_id"]), {})
            entry["holm_adjusted_p"] = h_res.get("holm_adjusted_p")
            entry["holm_significant"] = bool(h_res.get("reject_h0", False))

    # Élimination séquentielle par IC 95 % entre variantes si >= 2 variantes
    seq_elim: dict[str, Any] | None = None
    if len(by_variant_rows) >= 2:
        cand_list = []
        for vr in by_variant_rows:
            vid = str(vr["variant_id"])
            ci_v = circle_ci_by_variant.get(vid, {})
            cand_list.append(
                {
                    "id": vid,
                    "mean": float(vr["mean_ratio_arbres"]),
                    "ci95_low": ci_v.get("ci95_low"),
                    "ci95_high": ci_v.get("ci95_high"),
                }
            )
        seq_elim = sequential_ci_elimination(cand_list, maximize=True)

    # Comparaisons appariées du panel de bots (B1/B2/B2_OPEN vs B0 et B2_OPEN vs B2)
    bot_panel_comps: list[dict[str, Any]] = []
    if len(distinct_bots) >= 2:
        bot_pairs: list[tuple[str, str]] = []
        if "B0" in distinct_bots:
            for b_other in ("B1", "B2", "B2_OPEN", "B3"):
                if b_other in distinct_bots:
                    bot_pairs.append((b_other, "B0"))
        if "B1" in distinct_bots and "B2" in distinct_bots:
            bot_pairs.append(("B2", "B1"))
        if "B2" in distinct_bots and "B2_OPEN" in distinct_bots:
            bot_pairs.append(("B2_OPEN", "B2"))
        for b_hi, b_lo in bot_pairs:
            d_tbl: dict[tuple[int, str], list[float]] = {}
            d_by_n: dict[int, dict[str, list[float]]] = {}
            for (v_k, b_k, n_k, t_k, s_k, rs_k), row_hi in indexed.items():
                if b_k != b_hi:
                    continue
                row_lo = indexed.get((v_k, b_lo, n_k, t_k, s_k, rs_k))
                if row_lo is None:
                    continue
                dl = _extract_cell_diffs_pair(row_hi, row_lo)
                d_tbl.setdefault((n_k, t_k), []).extend(dl)
                d_by_n.setdefault(n_k, {}).setdefault(t_k, []).extend(dl)
            if d_tbl:
                bot_panel_comps.append(
                    {
                        "comparison": f"{b_hi}_minus_{b_lo}",
                        "bot_high": b_hi,
                        "bot_low": b_lo,
                        "global": paired_diff_cluster_ci95(d_tbl),
                        "by_n_players": {
                            str(n_pl): paired_diff_cluster_ci95(d_by_n[n_pl])
                            for n_pl in sorted(d_by_n)
                        },
                    }
                )

    if not vs_ref_entries and not bot_panel_comps:
        return None

    out_block: dict[str, Any] = {
        "reference_variant_id": ref_vid,
        "multiple_comparison_method": "holm_bonferroni",
        "bots_present": distinct_bots,
        "has_full_calibration_panel": all(
            b in distinct_bots for b in ("B0", "B1", "B2", "B2_OPEN")
        ),
    }
    if vs_ref_entries:
        out_block["variants_vs_reference"] = vs_ref_entries
    if seq_elim is not None:
        out_block["sequential_ci_elimination"] = seq_elim
    if bot_panel_comps:
        out_block["bot_panel_diffs"] = bot_panel_comps
    return out_block


def _build_paired_ab_tile_metrics(
    cell_rows: list[dict[str, Any]],
    *,
    plan: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Construit `tile_metrics` par protocole A/B apparié (ou audit d'activations sans biais N/lisière)."""
    base_tile_profiles: dict[str, str] = dict(plan.get("base_tile_profiles", {}))
    ab_protocol = plan.get("ab_tile_protocol")

    # Pré-parsing de compared_slots, active_slots et tile_activations par cellule
    parsed_rows: list[dict[str, Any]] = []
    slot_act_by_var: dict[tuple[str, str], list[int]] = {}
    slot_act_by_vbn: dict[tuple[str, str, str, int], list[int]] = {}
    slot_act_global: dict[str, list[int]] = {}

    for r in cell_rows:
        ng = int(r.get("n_games") or 0)
        if ng <= 0:
            continue
        vid = str(r["variant_id"])
        bot_s = str(r["bot"])
        n_pl = int(r["n_players"])
        peuples_s = str(r.get("peuples") or r.get("table_id") or "")
        act_slots = _active_slots_for_peuples_circle(peuples_s)
        comp_map = {str(k): str(v) for k, v in _parse_json_dict(r.get("compared_slots_json")).items()}
        acts_map = {str(k): int(v) for k, v in _parse_json_dict(r.get("tile_activations_json")).items()}

        for s_id in act_slots:
            a_cnt = acts_map.get(s_id, 0)
            cur_g = slot_act_global.get(s_id)
            if cur_g is None:
                slot_act_global[s_id] = [ng, a_cnt]
            else:
                cur_g[0] += ng
                cur_g[1] += a_cnt

            k_var = (vid, s_id)
            cur_v = slot_act_by_var.get(k_var)
            if cur_v is None:
                slot_act_by_var[k_var] = [ng, a_cnt]
            else:
                cur_v[0] += ng
                cur_v[1] += a_cnt

            k_vbn = (vid, bot_s, s_id, n_pl)
            cur_b = slot_act_by_vbn.get(k_vbn)
            if cur_b is None:
                slot_act_by_vbn[k_vbn] = [ng, a_cnt]
            else:
                cur_b[0] += ng
                cur_b[1] += a_cnt

        parsed_rows.append(
            {
                **r,
                "_active_slots": act_slots,
                "_comp_map": comp_map,
                "_acts_map": acts_map,
            }
        )

    def _act_rate(pair_counts: list[int] | None) -> tuple[int, int, float]:
        if not pair_counts or pair_counts[0] <= 0:
            return 0, 0, 0.0
        ng_v, act_v = pair_counts[0], pair_counts[1]
        return ng_v, act_v, round(act_v / ng_v, 4)

    # Indexation CRN : (variant_id, bot, n_players, table_id, exp_seed, rep_start) -> parsed_row
    indexed_by_vid: dict[tuple[str, str, int, str, int, int], dict[str, Any]] = {
        (
            str(r["variant_id"]),
            str(r["bot"]),
            int(r["n_players"]),
            str(r.get("table_id") or r.get("peuples") or ""),
            int(r.get("exp_seed") or 0),
            int(r.get("rep_start") or 0),
        ): r
        for r in parsed_rows
    }

    # --- Cas 1 : Protocole A/B explicite ACTIVE_VS_NEUTRE (BASE vs "{slot}:NEUTRE") ---
    if ab_protocol == "ACTIVE_VS_NEUTRE":
        ab_slots: tuple[str, ...] = tuple(plan.get("ab_slots", ()))
        out_ab: dict[str, dict[str, Any]] = {}
        p_items_ab: list[tuple[str, float | None]] = []

        for s_id in ab_slots:
            active_prof = str(base_tile_profiles.get(s_id, "B" if s_id.startswith("SLOT_") else "A"))
            neutre_vid = f"{s_id}:NEUTRE"
            diffs_all: dict[tuple[int, str], list[float]] = {}
            diffs_bot: dict[str, dict[tuple[int, str], list[float]]] = {}
            diffs_bn: dict[tuple[str, int], dict[str, list[float]]] = {}

            for (v_k, b_k, n_k, t_k, seed_k, rs_k), row_neu in indexed_by_vid.items():
                if v_k != neutre_vid:
                    continue
                if s_id not in row_neu["_active_slots"]:
                    continue
                row_base = indexed_by_vid.get(("BASE", b_k, n_k, t_k, seed_k, rs_k))
                if row_base is None:
                    continue
                # Effet positif = la tuile active améliore le score par rapport à la tuile neutralisée
                d_list = _extract_cell_diffs_pair(row_base, row_neu)
                diffs_all.setdefault((n_k, t_k), []).extend(d_list)
                diffs_bot.setdefault(b_k, {}).setdefault((n_k, t_k), []).extend(d_list)
                diffs_bn.setdefault((b_k, n_k), {}).setdefault(t_k, []).extend(d_list)

            ng_in_play, act_tot, act_pg = _act_rate(slot_act_by_var.get(("BASE", s_id)))
            glob_s = paired_diff_cluster_ci95(diffs_all)
            bot_s_map = {b_k: paired_diff_cluster_ci95(diffs_bot[b_k]) for b_k in sorted(diffs_bot)}
            bn_rows: list[dict[str, Any]] = []
            for b_k, n_pl in sorted(diffs_bn):
                _, _, act_bn = _act_rate(slot_act_by_vbn.get(("BASE", b_k, s_id, n_pl)))
                bn_st = paired_diff_cluster_ci95(diffs_bn[(b_k, n_pl)])
                bn_rows.append(
                    {
                        "bot": b_k,
                        "n_players": n_pl,
                        "n_tables": bn_st["n_tables"],
                        "n_pairs": bn_st["n_pairs"],
                        "mean_delta_ratio": bn_st["mean_delta"],
                        "ci95_low": bn_st["ci95_low"],
                        "ci95_high": bn_st["ci95_high"],
                        "activations_per_game": act_bn,
                        "low_activation_lt1": bool(act_bn < 1.0),
                    }
                )

            tok = f"{s_id}:{active_prof}"
            p_items_ab.append((tok, glob_s.get("p_value")))
            out_ab[tok] = {
                "slot": s_id,
                "profile": active_prof,
                "ref_profile": "NEUTRE",
                "protocol": "PAIRED_AB_ACTIVE_VS_NEUTRE",
                "ab_effect_estimable": bool(glob_s["estimable"]),
                "n_games": ng_in_play,
                "n_games_in_play": ng_in_play,
                "n_tables": glob_s["n_tables"],
                "n_pairs": glob_s["n_pairs"],
                "mean_delta_ratio": glob_s["mean_delta"],
                "se_clustered": glob_s["se_clustered"],
                "ci95_low": glob_s["ci95_low"],
                "ci95_high": glob_s["ci95_high"],
                "p_value": glob_s["p_value"],
                "activations_total": act_tot,
                "activations_per_game": act_pg,
                "low_activation_lt1": bool(act_pg < 1.0),
                "sign_stability_b1_b2_open": assess_sign_stability(bot_s_map),
                "by_bot_x_n_players": bn_rows,
            }

        holm_ab = holm_bonferroni_adjust(p_items_ab, alpha=0.05)
        for tok, entry in out_ab.items():
            h_res = holm_ab.get(tok, {})
            entry["holm_adjusted_p"] = h_res.get("holm_adjusted_p")
            raw_sig = bool(h_res.get("reject_h0", False))
            entry["raw_significant"] = raw_sig
            entry["significant"] = bool(raw_sig and not entry["low_activation_lt1"])
        return out_ab

    # --- Cas 2 : Comparaisons de profils (`slot_profile_comparisons`, ex. G7:A vs G7:NEUTRE) ---
    slot_to_profs: dict[str, list[str]] = {}
    for r in parsed_rows:
        for s_id, prof in r["_comp_map"].items():
            plist = slot_to_profs.setdefault(s_id, [])
            if prof not in plist:
                plist.append(prof)

    if slot_to_profs:
        out_comp: dict[str, dict[str, Any]] = {}
        p_items_comp: list[tuple[str, float | None]] = []

        # Indexation générique par (bot, n_players, table_id, exp_seed, rep_start, frozen_comp_map)
        indexed_comp: dict[
            tuple[str, int, str, int, int, tuple[tuple[str, str], ...]], dict[str, Any]
        ] = {}
        for r in parsed_rows:
            comp_key = tuple(sorted(r["_comp_map"].items()))
            indexed_comp[
                (
                    str(r["bot"]),
                    int(r["n_players"]),
                    str(r.get("table_id") or r.get("peuples") or ""),
                    int(r.get("exp_seed") or 0),
                    int(r.get("rep_start") or 0),
                    comp_key,
                )
            ] = r

        for s_id in [s for s in CANONICAL_32_SLOTS if s in slot_to_profs]:
            profs = slot_to_profs[s_id]
            ref_prof = "NEUTRE" if "NEUTRE" in profs else profs[0]

            # Statistiques d'activation & moyenne sur tables actives pour chaque profil de s_id
            prof_ng_act: dict[str, list[int]] = {}
            prof_ratio_acc: dict[str, list[float]] = {}
            prof_bn_act: dict[tuple[str, str, int], list[int]] = {}
            for r in parsed_rows:
                p_cur = r["_comp_map"].get(s_id)
                if p_cur is None or s_id not in r["_active_slots"]:
                    continue
                ng = int(r["n_games"])
                a_cnt = r["_acts_map"].get(s_id, 0)
                sr = float(r.get("sum_ratio_arbres") or 0.0)
                cur_a = prof_ng_act.setdefault(p_cur, [0, 0])
                cur_a[0] += ng
                cur_a[1] += a_cnt
                cur_r = prof_ratio_acc.setdefault(p_cur, [0.0, 0.0])
                cur_r[0] += sr
                cur_r[1] += float(ng)
                b_key = (p_cur, str(r["bot"]), int(r["n_players"]))
                cur_bn = prof_bn_act.setdefault(b_key, [0, 0])
                cur_bn[0] += ng
                cur_bn[1] += a_cnt

            # Entrée de référence explicite
            ref_ng, ref_act, ref_act_pg = _act_rate(prof_ng_act.get(ref_prof))
            ref_mean = (
                round(prof_ratio_acc[ref_prof][0] / prof_ratio_acc[ref_prof][1], 4)
                if (ref_prof in prof_ratio_acc and prof_ratio_acc[ref_prof][1] > 0)
                else None
            )
            out_comp[f"{s_id}:{ref_prof}"] = {
                "slot": s_id,
                "profile": ref_prof,
                "ref_profile": ref_prof,
                "is_reference": True,
                "protocol": "PAIRED_AB_REFERENCE",
                "ab_effect_estimable": True,
                "n_games": ref_ng,
                "n_games_in_play": ref_ng,
                "mean_ratio_arbres_in_play": ref_mean,
                "mean_delta_ratio": 0.0,
                "ci95_low": 0.0,
                "ci95_high": 0.0,
                "activations_total": ref_act,
                "activations_per_game": ref_act_pg,
                "low_activation_lt1": bool(ref_act_pg < 1.0),
                "significant": False,
            }

            for p_cand in profs:
                if p_cand == ref_prof:
                    continue
                diffs_all: dict[tuple[int, str], list[float]] = {}
                diffs_bot: dict[str, dict[tuple[int, str], list[float]]] = {}
                diffs_bn: dict[tuple[str, int], dict[str, list[float]]] = {}

                for (b_k, n_k, t_k, seed_k, rs_k, comp_t), row_c in indexed_comp.items():
                    if dict(comp_t).get(s_id) != p_cand:
                        continue
                    if s_id not in row_c["_active_slots"]:
                        continue
                    ref_comp_dict = dict(comp_t)
                    ref_comp_dict[s_id] = ref_prof
                    row_r = indexed_comp.get(
                        (b_k, n_k, t_k, seed_k, rs_k, tuple(sorted(ref_comp_dict.items())))
                    )
                    if row_r is None:
                        continue
                    dl = _extract_cell_diffs_pair(row_c, row_r)
                    diffs_all.setdefault((n_k, t_k), []).extend(dl)
                    diffs_bot.setdefault(b_k, {}).setdefault((n_k, t_k), []).extend(dl)
                    diffs_bn.setdefault((b_k, n_k), {}).setdefault(t_k, []).extend(dl)

                ng_c, act_c, act_pg_c = _act_rate(prof_ng_act.get(p_cand))
                cand_mean = (
                    round(prof_ratio_acc[p_cand][0] / prof_ratio_acc[p_cand][1], 4)
                    if (p_cand in prof_ratio_acc and prof_ratio_acc[p_cand][1] > 0)
                    else None
                )
                glob_s = paired_diff_cluster_ci95(diffs_all)
                bot_s_map = {
                    b_k: paired_diff_cluster_ci95(diffs_bot[b_k]) for b_k in sorted(diffs_bot)
                }
                bn_rows: list[dict[str, Any]] = []
                for b_k, n_pl in sorted(diffs_bn):
                    _, _, act_bn = _act_rate(prof_bn_act.get((p_cand, b_k, n_pl)))
                    bn_st = paired_diff_cluster_ci95(diffs_bn[(b_k, n_pl)])
                    bn_rows.append(
                        {
                            "bot": b_k,
                            "n_players": n_pl,
                            "n_tables": bn_st["n_tables"],
                            "n_pairs": bn_st["n_pairs"],
                            "mean_delta_ratio": bn_st["mean_delta"],
                            "ci95_low": bn_st["ci95_low"],
                            "ci95_high": bn_st["ci95_high"],
                            "activations_per_game": act_bn,
                            "low_activation_lt1": bool(act_bn < 1.0),
                        }
                    )

                tok = f"{s_id}:{p_cand}"
                p_items_comp.append((tok, glob_s.get("p_value")))
                out_comp[tok] = {
                    "slot": s_id,
                    "profile": p_cand,
                    "ref_profile": ref_prof,
                    "is_reference": False,
                    "protocol": "PAIRED_AB_PROFILE_COMPARE",
                    "ab_effect_estimable": bool(glob_s["estimable"]),
                    "n_games": ng_c,
                    "n_games_in_play": ng_c,
                    "mean_ratio_arbres_in_play": cand_mean,
                    "n_tables": glob_s["n_tables"],
                    "n_pairs": glob_s["n_pairs"],
                    "mean_delta_ratio": glob_s["mean_delta"],
                    "se_clustered": glob_s["se_clustered"],
                    "ci95_low": glob_s["ci95_low"],
                    "ci95_high": glob_s["ci95_high"],
                    "p_value": glob_s["p_value"],
                    "activations_total": act_c,
                    "activations_per_game": act_pg_c,
                    "low_activation_lt1": bool(act_pg_c < 1.0),
                    "sign_stability_b1_b2_open": assess_sign_stability(bot_s_map),
                    "by_bot_x_n_players": bn_rows,
                }

        holm_c = holm_bonferroni_adjust(p_items_comp, alpha=0.05)
        for tok, h_res in holm_c.items():
            entry = out_comp[tok]
            entry["holm_adjusted_p"] = h_res.get("holm_adjusted_p")
            raw_sig = bool(h_res.get("reject_h0", False))
            entry["raw_significant"] = raw_sig
            entry["significant"] = bool(raw_sig and not entry["low_activation_lt1"])
        return out_comp

    # --- Cas 3 : Campagne mono-variante (sans protocole A/B) -> audit d'activations pur ---
    if not (bool(plan.get("include_full_tile_metrics", False)) or int(plan.get("mode", 0)) >= 4):
        return {}

    out_audit: dict[str, dict[str, Any]] = {}
    for s_id in CANONICAL_32_SLOTS:
        ng_s, act_s, act_pg_s = _act_rate(slot_act_global.get(s_id))
        if ng_s <= 0:
            continue
        prof = str(base_tile_profiles.get(s_id, "B" if s_id.startswith("SLOT_") else "A"))
        out_audit[f"{s_id}:{prof}"] = {
            "slot": s_id,
            "profile": prof,
            "protocol": "ACTIVATION_AUDIT_ONLY",
            "ab_effect_estimable": False,
            "n_games": ng_s,
            "n_games_in_play": ng_s,
            "activations_total": act_s,
            "activations_per_game": act_pg_s,
            "low_activation_lt1": bool(act_pg_s < 1.0),
            "significant": False,
            "note": "Effet causal non estimable sans protocole A/B apparié (ab_tile_protocol: ACTIVE_VS_NEUTRE).",
        }
    return out_audit


def run_pilot_sample_size_estimation(
    manifest: dict[str, Any],
    *,
    pilot_pairs: int = 100,
    target_delta: float = 0.02,
) -> dict[str, Any]:
    """Exécute un pilote local (~100 paires CRN) et estime la taille d'échantillon n = (1,96*sigma/delta)^2."""
    if pilot_pairs < 4:
        raise ValueError(f"pilot_pairs doit être >= 4 (reçu {pilot_pairs})")
    if target_delta <= 0.0:
        raise ValueError(f"target_delta doit être > 0 (reçu {target_delta})")

    pilot_manifest = dict(manifest)
    pilot_manifest["games_per_configuration"] = int(pilot_pairs)
    pilot_manifest["micro_forks"] = False
    plan = resolve_manifest_plan(pilot_manifest)
    ref_vid = str(plan["reference_variant_id"])
    variants = [str(v["variant_id"]) for v in plan["profile_variants"]]
    if len(variants) < 2:
        raise ValueError(
            "Le dimensionnement apparié requiert au moins 2 variantes (ex. slot_profile_comparisons ou ab_tile_protocol)."
        )

    records = [_execute_manifest_unit(u) for u in plan["units"]]
    indexed: dict[tuple[str, str, int, str, int, int], dict[str, Any]] = {
        (
            str(r["variant_id"]),
            str(r["bot"]),
            int(r["n_players"]),
            str(r["table_id"]),
            int(r["exp_seed"]),
            int(r["rep_start"]),
        ): r
        for r in records
    }

    estimates: list[dict[str, Any]] = []
    for vid in variants:
        if vid == ref_vid:
            continue
        diffs_by_bn: dict[tuple[str, int], list[float]] = {}
        diffs_all: list[float] = []
        for (v_k, b_k, n_k, t_k, s_k, rs_k), row_v in indexed.items():
            if v_k != vid:
                continue
            row_r = indexed.get((ref_vid, b_k, n_k, t_k, s_k, rs_k))
            if row_r is None:
                continue
            dl = _extract_cell_diffs_pair(row_v, row_r)
            diffs_all.extend(dl)
            diffs_by_bn.setdefault((b_k, n_k), []).extend(dl)

        if len(diffs_all) >= 2:
            entry: dict[str, Any] = {
                "variant_id": vid,
                "reference_variant_id": ref_vid,
                "global": estimate_required_pairs(diffs_all, target_delta=target_delta),
                "by_bot_x_n_players": [
                    {
                        "bot": b_k,
                        "n_players": n_pl,
                        **estimate_required_pairs(
                            diffs_by_bn[(b_k, n_pl)], target_delta=target_delta
                        ),
                    }
                    for (b_k, n_pl) in sorted(diffs_by_bn)
                    if len(diffs_by_bn[(b_k, n_pl)]) >= 2
                ],
            }
            estimates.append(entry)

    return {
        "campaign": str(plan["campaign_name"]),
        "pilot_pairs_requested": int(pilot_pairs),
        "target_delta": float(target_delta),
        "reference_variant_id": ref_vid,
        "estimates": estimates,
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

    con = duckdb.connect(":memory:", config={"threads": 1})
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
    has_v6_metrics_cols = (
        "sum_power_tokens_end_act1" in cell_cols
        and "count_act1_reached" in cell_cols
        and "sum_power_tokens_end_game" in cell_cols
        and "count_charge_gains" in cell_cols
        and "count_furtivite_1_rive_turns" in cell_cols
    )
    v6_metrics_sql = (
        """
            CAST(ROUND(COALESCE(SUM(sum_power_tokens_end_act1) * 1.0 / NULLIF(SUM(count_act1_reached), 0), 0.0), 3) AS DOUBLE) AS mean_power_tokens_end_act1,
            CAST(ROUND(SUM(sum_power_tokens_end_game) * 1.0 / SUM(n_games), 3) AS DOUBLE) AS mean_power_tokens_end_game,
            CAST(SUM(count_charge_gains) AS INTEGER) AS count_charge_gains,
            CAST(SUM(count_furtivite_1_rive_turns) AS INTEGER) AS count_furtivite_1_rive_turns,
        """
        if has_v6_metrics_cols
        else """
            CAST(0.0 AS DOUBLE) AS mean_power_tokens_end_act1,
            CAST(0.0 AS DOUBLE) AS mean_power_tokens_end_game,
            0 AS count_charge_gains,
            0 AS count_furtivite_1_rive_turns,
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
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens,
            {reveil_diag_sql}
            {reve_act_sql}
            {v6_metrics_sql}
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

    # Chargement unifié des cellules pour CVaR directe (alpha=0.20 uniforme + bootstrap IC95),
    # dispersion inter-cercles pondérée, différences appariées groupées par table et A/B tuiles.
    opt_cell_cols = (
        ("n_animaux_sauvages", "NULL AS n_animaux_sauvages"),
        ("table_id", "peuples AS table_id"),
        ("peuples", "table_id AS peuples"),
        ("compared_slots_json", "'{}' AS compared_slots_json"),
        ("exp_seed", "0 AS exp_seed"),
        ("rep_start", "0 AS rep_start"),
        ("ratio_bp_counts_json", "NULL AS ratio_bp_counts_json"),
        ("rep_ratios_bp_json", "NULL AS rep_ratios_bp_json"),
        ("tile_activations_json", "NULL AS tile_activations_json"),
    )
    opt_select_sql = ",\n            ".join(
        col if col in cell_cols else fallback for col, fallback in opt_cell_cols
    )
    cell_table_rows = _query_dicts(
        con,
        f"""
        SELECT
            mode,
            bot,
            n_players,
            variant_id,
            n_games,
            sum_ratio_arbres,
            {opt_select_sql},
            sum_ratio_arbres * 1.0 / n_games AS table_mean_ratio
        FROM cells
        WHERE n_games > 0
        """,
    )
    all_table_ratios: list[float] = []
    ratios_by_mode: dict[tuple[int, str], list[float]] = {}
    ratios_by_n: dict[int, list[float]] = {}
    ratios_by_variant: dict[str, list[float]] = {}
    ratios_by_n_animaux: dict[int, list[float]] = {}
    ratios_by_variant_n: dict[tuple[str, int], list[float]] = {}
    ratios_by_variant_bot_n: dict[tuple[str, str, int], list[float]] = {}
    ratios_by_variant_animaux: dict[tuple[str, int], list[float]] = {}
    for tr in cell_table_rows:
        mr_t = float(tr["table_mean_ratio"])
        v_id_t = str(tr["variant_id"])
        bot_t = str(tr["bot"])
        n_pl_t = int(tr["n_players"])
        all_table_ratios.append(mr_t)
        ratios_by_mode.setdefault((int(tr["mode"]), bot_t), []).append(mr_t)
        ratios_by_n.setdefault(n_pl_t, []).append(mr_t)
        ratios_by_variant.setdefault(v_id_t, []).append(mr_t)
        ratios_by_variant_n.setdefault((v_id_t, n_pl_t), []).append(mr_t)
        ratios_by_variant_bot_n.setdefault((v_id_t, bot_t, n_pl_t), []).append(mr_t)
        if tr.get("n_animaux_sauvages") is not None:
            na_t = int(tr["n_animaux_sauvages"])
            ratios_by_n_animaux.setdefault(na_t, []).append(mr_t)
            ratios_by_variant_animaux.setdefault((v_id_t, na_t), []).append(mr_t)

    global_table_cvar20 = _cvar_bottom_values(all_table_ratios, 0.20)
    campaign_seed = int(manifest.get("seed", plan.get("exp_seed", 20261201)))
    cvar_boot = _build_stratified_cvar_bootstrap(
        cell_table_rows, alpha=0.20, n_boot=300, seed=campaign_seed
    )

    def _apply_direct_cvar(row: dict[str, Any], boot_info: dict[str, Any] | None) -> None:
        if boot_info is not None:
            row["cvar20_ratio"] = boot_info["cvar"]
            row["game_cvar20_ratio"] = boot_info["cvar"]
            row["cvar20_ci95_low"] = boot_info["ci95_low"]
            row["cvar20_ci95_high"] = boot_info["ci95_high"]

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
            {v6_metrics_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY mode, bot
        ORDER BY mode, bot
        """,
    )
    for row in by_mode:
        m_key = (int(row["mode"]), str(row["bot"]))
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_mode.get(m_key, []), 0.20)
        if cvar_boot.get("has_hist"):
            _apply_direct_cvar(row, cvar_boot["by_mode"].get(m_key))

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
            {v6_metrics_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY n_players
        ORDER BY n_players
        """,
    )
    for row in by_n_players:
        n_key = int(row["n_players"])
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_n.get(n_key, []), 0.20)
        if cvar_boot.get("has_hist"):
            _apply_direct_cvar(row, cvar_boot["by_n"].get(n_key))

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
            a_key = int(row["n_animaux_sauvages"])
            row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_n_animaux.get(a_key, []), 0.20)
            if cvar_boot.get("has_hist"):
                _apply_direct_cvar(row, cvar_boot["by_anim"].get(a_key))

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
        v_key = str(row["variant_id"])
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_variant.get(v_key, []), 0.20)
        if cvar_boot.get("has_hist"):
            _apply_direct_cvar(row, cvar_boot["by_variant"].get(v_key))

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
        vn_key = (str(row["variant_id"]), int(row["n_players"]))
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_variant_n.get(vn_key, []), 0.20)
        if cvar_boot.get("has_hist"):
            _apply_direct_cvar(row, cvar_boot["by_variant_n"].get(vn_key))

    by_variant_x_bot_x_n_players = _query_dicts(
        con,
        f"""
        SELECT
            variant_id,
            bot,
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
            {v6_metrics_sql}
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens
        FROM cells
        GROUP BY variant_id, bot, n_players
        ORDER BY variant_id ASC, bot ASC, n_players ASC
        """,
    )
    for row in by_variant_x_bot_x_n_players:
        vbn_key = (str(row["variant_id"]), str(row["bot"]), int(row["n_players"]))
        row["table_cvar20_ratio"] = _cvar_bottom_values(ratios_by_variant_bot_n.get(vbn_key, []), 0.20)
        if cvar_boot.get("has_hist"):
            _apply_direct_cvar(row, cvar_boot["by_vbn"].get(vbn_key))

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
            va_key = (str(row["variant_id"]), int(row["n_animaux_sauvages"]))
            row["table_cvar20_ratio"] = _cvar_bottom_values(
                ratios_by_variant_animaux.get(va_key, []), 0.20
            )
            if cvar_boot.get("has_hist"):
                _apply_direct_cvar(row, cvar_boot["by_variant_anim"].get(va_key))

    # Protocole A/B apparié par tuile (remplace l'ancien tile_metrics confondu avec N et co-lisières)
    base_tile_profiles_plan: dict[str, str] = dict(plan.get("base_tile_profiles", {}))
    tile_metrics = _build_paired_ab_tile_metrics(cell_table_rows, plan=plan)

    by_variant_clean = [
        {k: v for k, v in row.items() if k != "compared_slots_json"}
        for row in by_variant[:24]
    ]

    tested_tiles: tuple[tuple[str, str], ...] = tuple(plan["tested_tiles"])
    varying_tiles: tuple[tuple[str, str], ...] = tuple(plan.get("varying_tiles", ()))
    generated_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

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

    # Dispersion inter-cercles pondérée par n_games (unifiée avec totals.mean_ratio_arbres,
    # et explicitement marquée non estimable lorsqu'un seul cercle a été exécuté)
    inter_block_intervals, circle_dispersion, circle_ci_by_variant = (
        _build_weighted_circle_dispersion(cell_table_rows)
    )

    # Différences appariées + IC 95 % groupés par table, correction Holm et stabilité panel B1/B2/B2_OPEN
    ref_vid_plan = str(plan.get("reference_variant_id") or "BASE")
    paired_comparisons = _build_paired_comparisons_block(
        cell_table_rows,
        reference_variant_id=ref_vid_plan,
        by_variant_rows=by_variant,
        circle_ci_by_variant=circle_ci_by_variant,
    )

    # CVaR_20% exact sur les parties individuelles (alpha=0.20 uniforme) + IC 95 % bootstrap
    global_cvar_boot: dict[str, Any] | None = (
        cvar_boot["global"] if cvar_boot.get("has_hist") else None
    )
    exact_game_cvar20: float | None = (
        float(global_cvar_boot["cvar"]) if global_cvar_boot is not None else None
    )
    game_cvar20_by_vbn: dict[tuple[str, str, int], float] = (
        {kv: float(bv["cvar"]) for kv, bv in cvar_boot["by_vbn"].items()}
        if cvar_boot.get("has_hist")
        else {}
    )

    # Forks et seeds (inclus automatiquement si la campagne produit des colonnes de micro-forks)
    forks_block: dict[str, Any] | None = None
    if "fork_anchors" in cell_cols:
        def _opt_sum_sql(col_n: str, cast_t: str = "DOUBLE") -> str:
            return (
                f"CAST(COALESCE(SUM({col_n}), 0) AS {cast_t}) AS {col_n}"
                if col_n in cell_cols
                else f"CAST(0 AS {cast_t}) AS {col_n}"
            )

        fork_cols_sql = ",\n                ".join(
            [
                _opt_sum_sql("fork_anchors", "INTEGER"),
                _opt_sum_sql("fork_anchors_missed", "INTEGER"),
                _opt_sum_sql("fork_diverged", "INTEGER"),
                _opt_sum_sql("sum_delta_v_neg"),
                _opt_sum_sql("sum_sq_delta_v_neg"),
                _opt_sum_sql("sum_c_prive"),
                _opt_sum_sql("sum_sq_c_prive"),
                _opt_sum_sql("sum_g_naive"),
                _opt_sum_sql("sum_g_unbiased"),
                _opt_sum_sql("sum_rho_delta"),
                _opt_sum_sql("fork_2_1_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_2_1_b2_vs_b0"),
                _opt_sum_sql("sum_sq_delta_v_2_1_b2_vs_b0"),
                _opt_sum_sql("fork_2_1_reve_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_2_1_reve"),
                _opt_sum_sql("sum_sq_delta_v_2_1_reve"),
                _opt_sum_sql("fork_furt_rp_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_furt_rp"),
                _opt_sum_sql("sum_sq_delta_v_furt_rp"),
                _opt_sum_sql("fork_furt_rs_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_furt_rs"),
                _opt_sum_sql("sum_sq_delta_v_furt_rs"),
                _opt_sum_sql("fork_4_1_piege_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_4_1_piege"),
                _opt_sum_sql("sum_sq_delta_v_4_1_piege"),
                _opt_sum_sql("fork_eveil_anchors", "INTEGER"),
                _opt_sum_sql("sum_delta_v_eveil_vs_survival"),
                _opt_sum_sql("sum_sq_delta_v_eveil_vs_survival"),
            ]
        )

        def _ci95_half(n_a: int, sx: float, sx2: float) -> float | None:
            if n_a < 2:
                return None
            var = max(0.0, (sx2 - (sx * sx) / n_a) / (n_a - 1))
            return round(1.96 * math.sqrt(var / n_a), 5)

        def _fmt_fork_summary(fr: dict[str, Any]) -> dict[str, Any]:
            fa = int(fr.get("fork_anchors") or 0)
            f21 = int(fr.get("fork_2_1_anchors") or 0)
            f21r = int(fr.get("fork_2_1_reve_anchors") or 0)
            ffrp = int(fr.get("fork_furt_rp_anchors") or 0)
            ffrs = int(fr.get("fork_furt_rs_anchors") or 0)
            f41 = int(fr.get("fork_4_1_piege_anchors") or 0)
            fev = int(fr.get("fork_eveil_anchors") or 0)

            s_neg = float(fr.get("sum_delta_v_neg") or 0.0)
            s_cpr = float(fr.get("sum_c_prive") or 0.0)
            d: dict[str, Any] = {
                "fork_anchors": fa,
                "fork_anchors_missed": int(fr.get("fork_anchors_missed") or 0),
                "fork_diverged": int(fr.get("fork_diverged") or 0),
                "pct_diverged_2_2": round(int(fr.get("fork_diverged") or 0) * 100.0 / fa, 2)
                if fa > 0
                else 0.0,
                "mean_delta_v_negociation_2_2": round(s_neg / fa, 5) if fa > 0 else 0.0,
                "ci95_delta_v_negociation_2_2": _ci95_half(
                    fa, s_neg, float(fr.get("sum_sq_delta_v_neg") or 0.0)
                ),
                "mean_c_prive_2_2": round(s_cpr / fa, 5) if fa > 0 else 0.0,
                "ci95_c_prive_2_2": _ci95_half(
                    fa, s_cpr, float(fr.get("sum_sq_c_prive") or 0.0)
                ),
                "mean_g_naive_2_2": round(float(fr.get("sum_g_naive") or 0.0) / fa, 5)
                if fa > 0
                else 0.0,
                "mean_g_unbiased_2_2": round(float(fr.get("sum_g_unbiased") or 0.0) / fa, 5)
                if fa > 0
                else 0.0,
                "mean_rho_delta_2_2": round(float(fr.get("sum_rho_delta") or 0.0) / fa, 4)
                if fa > 0
                else 0.0,
            }
            if f21 > 0 or f41 > 0 or fev > 0 or ffrp > 0 or ffrs > 0:
                s21 = float(fr.get("sum_delta_v_2_1_b2_vs_b0") or 0.0)
                s21r = float(fr.get("sum_delta_v_2_1_reve") or 0.0)
                sfrp = float(fr.get("sum_delta_v_furt_rp") or 0.0)
                sfrs = float(fr.get("sum_delta_v_furt_rs") or 0.0)
                s41 = float(fr.get("sum_delta_v_4_1_piege") or 0.0)
                sev = float(fr.get("sum_delta_v_eveil_vs_survival") or 0.0)
                d["causal_v6_1"] = {
                    "anchors_2_1": f21,
                    "mean_delta_v_2_1_b2_vs_b0": round(s21 / f21, 5) if f21 > 0 else 0.0,
                    "ci95_delta_v_2_1_b2_vs_b0": _ci95_half(
                        f21, s21, float(fr.get("sum_sq_delta_v_2_1_b2_vs_b0") or 0.0)
                    ),
                    "anchors_2_1_reve": f21r,
                    "mean_delta_v_2_1_reve": round(s21r / f21r, 5) if f21r > 0 else None,
                    "ci95_delta_v_2_1_reve": _ci95_half(
                        f21r, s21r, float(fr.get("sum_sq_delta_v_2_1_reve") or 0.0)
                    ),
                    "anchors_furt_rive_piege": ffrp,
                    "mean_delta_v_furt_rive_piege": round(sfrp / ffrp, 5) if ffrp > 0 else None,
                    "ci95_delta_v_furt_rive_piege": _ci95_half(
                        ffrp, sfrp, float(fr.get("sum_sq_delta_v_furt_rp") or 0.0)
                    ),
                    "anchors_furt_rive_sabotage": ffrs,
                    "mean_delta_v_furt_rive_sabotage": round(sfrs / ffrs, 5) if ffrs > 0 else None,
                    "ci95_delta_v_furt_rive_sabotage": _ci95_half(
                        ffrs, sfrs, float(fr.get("sum_sq_delta_v_furt_rs") or 0.0)
                    ),
                    "anchors_4_1_pose_piege": f41,
                    "mean_delta_v_4_1_pose_piege": round(s41 / f41, 5) if f41 > 0 else None,
                    "ci95_delta_v_4_1_pose_piege": _ci95_half(
                        f41, s41, float(fr.get("sum_sq_delta_v_4_1_piege") or 0.0)
                    ),
                    "anchors_5_3_eveil": fev,
                    "mean_delta_v_eveil_vs_survival": round(sev / fev, 5) if fev > 0 else None,
                    "ci95_delta_v_eveil_vs_survival": _ci95_half(
                        fev, sev, float(fr.get("sum_sq_delta_v_eveil_vs_survival") or 0.0)
                    ),
                }
            return d

        fork_row = _query_dicts(
            con,
            f"""
            SELECT
                {fork_cols_sql},
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
            fork_by_n_rows = _query_dicts(
                con,
                f"""
                SELECT
                    n_players,
                    {fork_cols_sql}
                FROM cells
                WHERE fork_anchors > 0
                GROUP BY n_players
                ORDER BY n_players
                """,
            )
            forks_block = {
                **_fmt_fork_summary(fork_row),
                "n_fork_rows": int(fork_row["n_fork_rows"]),
                "seeds": fork_seeds,
                "by_n_players": [
                    {"n_players": int(rn["n_players"]), **_fmt_fork_summary(rn)}
                    for rn in fork_by_n_rows
                ],
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
        "execution": execution_meta,
        "totals": {
            "total_games": total_games,
            "n_shards": int(g_stats["n_shards"]),
            "n_cells": int(g_stats["n_cells"]),
            "n_configurations": int(g_stats["n_configurations"]),
            "mean_score_arbres": g_stats["mean_score_arbres"],
            "mean_ratio_arbres": g_stats["mean_ratio_arbres"],
            "cvar20_ratio": exact_game_cvar20 if exact_game_cvar20 is not None else g_stats["cvar20_ratio"],
            "game_cvar20_ratio": exact_game_cvar20 if exact_game_cvar20 is not None else g_stats["cvar20_ratio"],
            "cvar20_ci95_low": global_cvar_boot["ci95_low"] if global_cvar_boot is not None else None,
            "cvar20_ci95_high": global_cvar_boot["ci95_high"] if global_cvar_boot is not None else None,
            "cvar20_bootstrap_level": (
                global_cvar_boot["bootstrap_level"] if global_cvar_boot is not None else "unavailable"
            ),
            "table_cvar20_ratio": global_table_cvar20,
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
            "mean_power_tokens_end_act1": float(g_stats["mean_power_tokens_end_act1"] or 0.0),
            "mean_power_tokens_end_game": float(g_stats["mean_power_tokens_end_game"] or 0.0),
            "count_charge_gains": int(g_stats["count_charge_gains"]),
            "count_furtivite_1_rive_turns": int(g_stats["count_furtivite_1_rive_turns"]),
            "tested_tiles": [f"{s}:{p}" for s, p in tested_tiles],
            "parquet_archive": parquet_path.relative_to(ROOT).as_posix(),
        },
        "quantiles": quantiles_block,
        "inter_block_intervals": inter_block_intervals,
        "circle_dispersion": circle_dispersion,
        "telemetry": telemetry_block,
        "by_mode": by_mode,
        "by_n_players": by_n_players,
        "by_variant": by_variant_clean,
        "by_variant_x_n_players": by_variant_x_n_players,
        "tile_metrics": tile_metrics,
    }
    if paired_comparisons is not None:
        digest_payload["paired_comparisons"] = paired_comparisons
    if int(plan.get("mode", 0)) >= 3 or varying_tiles:
        digest_payload["mode4_catalog"] = {
            "base_bundle_id": str(plan.get("base_bundle_id", "STANDARD_A")),
            "n_resolved_slots": len(base_tile_profiles_plan) if base_tile_profiles_plan else 32,
            "resolved_32_slots_sha256": str(plan.get("resolved_32_slots_sha256", "")),
        }
    if len(by_mode) > 1 or int(plan.get("mode", 0)) == 2:
        digest_payload["by_variant_x_bot_x_n_players"] = by_variant_x_bot_x_n_players
    if by_n_animaux_sauvages:
        digest_payload["by_n_animaux_sauvages"] = by_n_animaux_sauvages
    if by_variant_x_n_animaux_sauvages:
        digest_payload["by_variant_x_n_animaux_sauvages"] = by_variant_x_n_animaux_sauvages
    if forks_block is not None:
        digest_payload["forks"] = forks_block
    defense_attr_block = _build_defense_attribution_block(con, cell_cols, total_games)
    if defense_attr_block is not None:
        digest_payload["defense_attribution"] = defense_attr_block
    reveil_anatomy_block = _build_reveil_anatomy_block(con, cell_cols)
    if reveil_anatomy_block is not None:
        digest_payload["reveil_anatomy"] = reveil_anatomy_block
    # Les 5 blocs analytiques détaillés d'audit du socle v6.1 (acceptance_v6, sommeil_temporality,
    # charge_assaut_metrics, furtivite_metrics, ockham_razor) sont émis pour toute campagne Mode 2
    # ou multi-bots (ou si explicitement demandé via `include_v6_audit_blocks: true`).
    emit_v6_audit = (
        int(plan.get("mode", 0)) == 2
        or len(by_mode) > 1
        or bool(manifest.get("include_v6_audit_blocks", False))
    )
    if emit_v6_audit:
        acceptance_v6_block = _build_acceptance_v6_block(con, cell_cols, game_cvar20_by_vbn)
        if acceptance_v6_block is not None:
            digest_payload["acceptance_v6"] = acceptance_v6_block
        sommeil_temp_block = _build_sommeil_temporality_block(con, cell_cols)
        if sommeil_temp_block is not None:
            digest_payload["sommeil_temporality"] = sommeil_temp_block
        charge_assaut_block = _build_charge_assaut_block(con, cell_cols)
        if charge_assaut_block is not None:
            digest_payload["charge_assaut_metrics"] = charge_assaut_block
        furtivite_block = _build_furtivite_block(con, cell_cols)
        if furtivite_block is not None:
            digest_payload["furtivite_metrics"] = furtivite_block
        ockham_block = _build_ockham_razor_block(con, cell_cols)
        if ockham_block is not None:
            digest_payload["ockham_razor"] = ockham_block

    digest_path, prompt_path, final_digest = write_digest_and_prompt_files(
        campaign_name,
        digest_payload,
        tested_tiles=tested_tiles,
        varying_tiles=varying_tiles if varying_tiles else None,
    )

    print(f"\n=== SYNTHÈSE DUCKDB — {campaign_name} ({total_games} parties) ===")
    con.sql(
        """
        SELECT
            n_players AS N,
            bot,
            variant_id AS variante,
            CAST(SUM(n_games) AS INTEGER) AS parties,
            ROUND(SUM(sum_ratio_arbres) * 100.0 / SUM(n_games), 2) AS pct_arbres,
            ROUND(SUM(cvar20_ratio * n_games) * 100.0 / SUM(n_games), 2) AS pct_cvar20,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 2) AS tours_moy
        FROM cells
        GROUP BY n_players, bot, variant_id
        ORDER BY n_players, bot, variant_id
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
    branch_res = _run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture=True)
    target_branch = (branch_res.stdout or "").strip() or "main"
    _run(["git", "push", "origin", target_branch])


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
    parser.add_argument(
        "--estimate-sample-size",
        action="store_true",
        help="Mode pré-campagne local : exécute un pilote apparié et estime n = (1,96*sigma/delta)^2.",
    )
    parser.add_argument(
        "--pilot-pairs",
        type=int,
        default=100,
        help="Nombre de paires pilote pour --estimate-sample-size (défaut: 100).",
    )
    parser.add_argument(
        "--target-delta",
        type=float,
        default=0.02,
        help="Précision cible delta (ratio d'arbres) pour --estimate-sample-size (défaut: 0.02).",
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

    if args.estimate_sample_size:
        sizing = run_pilot_sample_size_estimation(
            manifest,
            pilot_pairs=int(args.pilot_pairs),
            target_delta=float(args.target_delta),
        )
        print(json.dumps(sizing, indent=2, ensure_ascii=False))
        return 0

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
