"""Orchestrateur Palier 4 (Cloud Batch Spot / Cloud Run / Local PyPy) & synthèse DuckDB du Canon Unique 32 Tuiles."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import duckdb

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import engine.effects  # noqa: F401
from campaigns.designs import inter_block_ci95
from campaigns.digest_builder import (
    build_tested_tiles_rules,
    decode_chassis_axes,
    load_spec_bundle,
    write_digest_and_prompt_files,
)
from campaigns.map_elites import (
    CANONICAL_32_SLOTS,
    GenomeEvaluation,
    MapElitesArchive2D,
    ShapleySurrogateOrder2,
    build_127_circular_tables,
    decode_genome_key,
    encode_genome_key,
    genome_to_tile_profiles,
    load_catalog_slot_profiles,
    load_mode3_reference_genome,
)
from engine.effects.registry import list_registered_tiles
from engine.state import CHASSIS_AXES_OPTIONS, MATRICE_PAIRES, decode_chassis_index
from scripts_cloud.publish_digest import publish_campaign_digest
from scripts_cloud.studio_paths import find_gcloud, find_uv

REGION = "europe-west9"
IMAGE_URI = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
BATCH_MACHINE_TYPE = "c3d-highcpu-4"
BATCH_MAX_RUN_DURATION = "7200s"
CLOUDRUN_JOB_PHASE_A = "amazonia-palier4-phase-a"
CLOUDRUN_JOB_PHASE_B = "amazonia-palier4-phase-b"

GCS_PREFIX = "gs://amazonia-sim-runs/palier4_canon"
LOCAL_RUN_DIR = ROOT / ".tmp_runs" / "palier4_canon"
LOCAL_SHARDS_DIR = LOCAL_RUN_DIR / "shards"
PARQUET_PATH = LOCAL_RUN_DIR / "cells.parquet"
CANON_JSON_PATH = ROOT / "data" / "canon_unique_32.json"
MAX_PALIER4_DIGEST_BYTES = 30_000


def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def estimate_palier4_games(
    *,
    halving_cohorts: int,
    base_reps_a: int,
    islands: int,
    n_init: int,
    n_generations: int,
    batch_per_gen: int,
    reps_127: int,
    top_finalists_k: int,
    depth_reps: int,
) -> dict[str, int]:
    """Calcule le volume prévisionnel de parties des Phases A, B et Étape 2."""
    # Phase A Stage 1 : 16 cohortes x (8->4->2->1) sur 12 tables x 2 génomes sondes
    per_cohort_a = (8 * base_reps_a + 4 * min(4, base_reps_a * 2) + 2 * min(4, base_reps_a * 4)) * 24
    phase_a_stage1 = halving_cohorts * per_cohort_a
    # Phase A Stage 2 (Finale inter-cohortes 16 -> 8 -> 4 -> 2 -> 1)
    champ_reps = max(1, base_reps_a * 2)
    phase_a_final = (
        16 * champ_reps
        + 8 * min(4, champ_reps * 2)
        + 4 * 4
        + 2 * 4
    ) * 24

    # Phase B : criblage MAP-Elites (16 tables miroirs) + promotion sur 127 tables + validation B0..B3
    evals_per_island = n_init + n_generations * batch_per_gen
    phase_b_screening = islands * evals_per_island * 16
    promoted_total = islands * top_finalists_k + 1
    phase_b_127 = promoted_total * 127 * reps_127

    depth_per_island = 3 if islands == 1 else 2
    depth_candidates = islands * min(depth_per_island, top_finalists_k)
    games_per_depth = 12 * (4 * depth_reps + 1) + 6 * 13
    phase_c_depth = depth_candidates * games_per_depth

    total = phase_a_stage1 + phase_a_final + phase_b_screening + phase_b_127 + phase_c_depth
    return {
        "phase_a_games": phase_a_stage1 + phase_a_final,
        "phase_b_screening_games": phase_b_screening,
        "phase_b_127_games": phase_b_127,
        "phase_c_depth_games": phase_c_depth,
        "total_games": total,
    }


def preflight_check_and_quote(
    *,
    mode: str = "batch",
    halving_cohorts: int = 16,
    base_reps_a: int = 1,
    islands: int = 8,
    n_init: int = 8,
    n_generations: int = 8,
    batch_per_gen: int = 4,
    reps_127: int = 1,
    top_finalists_k: int = 3,
    depth_reps: int = 2,
    local_workers: int | None = None,
) -> tuple[dict[str, int], float]:
    """Pré-vérification métier silencieuse (100/100 profils, 127 tables, micro-tir PyPy < 1,5s) + Devis 5 lignes."""
    catalog = load_catalog_slot_profiles()
    registered = set(list_registered_tiles())
    expected_pairs = {(s, p) for s, profs in catalog.items() for p in profs}
    missing = expected_pairs - registered
    assert not missing and len(expected_pairs) == 100, f"Profils manquants : {sorted(missing)}"

    # Vérification de présence géométrique des 30 emplacements G/R/M sur les 127 tables circulaires
    tables_127 = build_127_circular_tables()
    assert len(tables_127) == 127
    present_slots: set[str] = {"SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"}
    for tbl in tables_127:
        n = tbl.n_players
        for i in range(n):
            t0, t1 = MATRICE_PAIRES[f"{tbl.peuples[i]}_{tbl.peuples[(i + 1) % n]}"]
            present_slots.add(t0)
            present_slots.add(t1)
    for slot_id in CANONICAL_32_SLOTS:
        assert slot_id in present_slots, f"Emplacement {slot_id} absent des 127 tables !"

    # Micro-essai local obligatoire de 20 parties Mode 4 sous PyPy 3.11 en < 1,5 s (max_steps = 2000)
    uv_bin = find_uv()
    micro_code = (
        "import time; import engine.effects; "
        "from bots import play_game_b2; "
        "from campaigns.map_elites import genome_to_tile_profiles, load_mode3_reference_genome; "
        "from engine.state import GameConfig, GameState; "
        "tp = genome_to_tile_profiles(load_mode3_reference_genome()); "
        "[play_game_b2(GameState(GameConfig(n_players=4, mode=4, peuples=('M','R','O','H'), tile_profiles=tp, exp_seed=11, rep_id=k)), max_steps=2000) for k in range(12)]; "
        "t0 = time.perf_counter(); "
        "[play_game_b2(GameState(GameConfig(n_players=4, mode=4, peuples=('M','R','O','H'), tile_profiles=tp, exp_seed=99, rep_id=i)), max_steps=2000) for i in range(20)]; "
        "dt = time.perf_counter() - t0; "
        "print(round(dt, 4)); "
        "assert dt < 1.5, f'Micro-tir Mode 4 trop lent : {dt:.3f}s'"
    )
    proc = subprocess.run(
        [uv_bin, "run", "--no-project", "--python", "pypy@3.11", "python", "-c", micro_code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    micro_sec = float(proc.stdout.strip().splitlines()[-1])
    gps_per_core = 20.0 / max(0.05, micro_sec)

    vol = estimate_palier4_games(
        halving_cohorts=halving_cohorts,
        base_reps_a=base_reps_a,
        islands=islands,
        n_init=n_init,
        n_generations=n_generations,
        batch_per_gen=batch_per_gen,
        reps_127=reps_127,
        top_finalists_k=top_finalists_k,
        depth_reps=depth_reps,
    )
    total_games = vol["total_games"]

    if mode == "local":
        eff_cores = max(1, local_workers or (os.cpu_count() or 2))
        # Légère marge pour les parties d'analyse approfondie de fin de parcours
        est_sec = total_games / (eff_cores * gps_per_core * 0.72) + 25.0
        cost_label = "0 € (calcul direct sans frais)."
    elif mode == "cloudrun":
        eff_cores = max(2, min(16, islands) * 2)
        est_sec = total_games / (eff_cores * gps_per_core * 0.75) + 45.0
        cost_label = "0 € (inclus dans le palier gratuit)."
    else:
        eff_cores = max(4, min(16, islands) * 4)
        est_sec = total_games / (eff_cores * gps_per_core * 0.80) + 90.0
        cost_eur = max(0.05, round((est_sec / 3600.0) * eff_cores * 0.012, 2))
        cost_label = f"~{cost_eur:.2f} € sur les crédits disponibles (tarif réduit)."

    wait_str = (
        f"~{max(1, round(est_sec / 60.0))} minutes"
        if est_sec >= 90.0
        else f"~{est_sec:.0f} secondes"
    )

    print("\n=== DEVIS DE VALIDATION (5 LIGNES) ===")
    print(
        "1. Question testée                   : Quelle sélection unique de 32 tuiles (parmi les 100 créées) et quel "
        "réglage de règles offrent les parties les plus riches, fluides et équilibrées de 3 à 6 joueurs, même sur les tables les plus dures ?"
    )
    print(
        "2. Ce qu'on compare                  : Tri complet des 128 réglages de règles de base, exploration guidée d'assemblages "
        "de 32 tuiles (variantes A/B/C/D des Gardiens, Rêves, Croissances et Migrations), et contrôle sur 4 niveaux de joueurs virtuels."
    )
    print(
        "3. Tables & nombre de joueurs couverts: Les 127 tables circulaires de peuples (avec leurs miroirs inversés) "
        "couvrant toutes les configurations à 3, 4, 5 et 6 joueurs."
    )
    print(
        f"4. Volume & durée estimée            : ~{total_games:,} parties simulées — attente estimée {wait_str}.".replace(
            ",", " "
        )
    )
    print(f"5. Coût estimé                       : {cost_label}\n", flush=True)
    return vol, micro_sec


def build_cloud_batch_job_spec(
    worker_args: list[str],
    *,
    task_count: int,
    parallelism: int,
    vcpus_per_task: int = 4,
    memory_mib: int = 4096,
) -> dict[str, Any]:
    """Construit la spécification JSON Google Cloud Batch Spot (`europe-west9`, `c3d-highcpu`, <= 7200s)."""
    return {
        "taskGroups": [
            {
                "taskCount": str(task_count),
                "parallelism": str(parallelism),
                "taskSpec": {
                    "runnables": [
                        {
                            "container": {
                                "imageUri": IMAGE_URI,
                                "commands": worker_args,
                            }
                        }
                    ],
                    "computeResource": {
                        "cpuMilli": str(vcpus_per_task * 1000),
                        "memoryMib": str(memory_mib),
                    },
                    "maxRetryCount": 2,
                    "maxRunDuration": BATCH_MAX_RUN_DURATION,
                },
            }
        ],
        "allocationPolicy": {
            "instances": [
                {
                    "policy": {
                        "machineType": BATCH_MACHINE_TYPE,
                        "provisioningModel": "SPOT",
                    }
                }
            ]
        },
        "logsPolicy": {
            "destination": "CLOUD_LOGGING",
        },
    }


def _submit_and_wait_batch_job(
    gcloud: str,
    job_prefix: str,
    spec: dict[str, Any],
    *,
    poll_interval_sec: float = 10.0,
) -> None:
    stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    job_id = f"{job_prefix}-{stamp}"
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", encoding="utf-8", delete=False
    ) as tmp:
        json.dump(spec, tmp, indent=2)
        cfg_path = Path(tmp.name)

    try:
        _run(
            [
                gcloud,
                "batch",
                "jobs",
                "submit",
                job_id,
                f"--location={REGION}",
                f"--config={cfg_path.as_posix()}",
            ]
        )
    finally:
        cfg_path.unlink(missing_ok=True)

    while True:
        proc = subprocess.run(
            [
                gcloud,
                "batch",
                "jobs",
                "describe",
                job_id,
                f"--location={REGION}",
                "--format=json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        info = json.loads(proc.stdout)
        state = str(info.get("status", {}).get("state", "STATE_UNSPECIFIED"))
        print(f"[Cloud Batch {job_id}] état = {state}", flush=True)
        if state == "SUCCEEDED":
            return
        if state in ("FAILED", "DELETION_IN_PROGRESS", "CANCELLED"):
            raise RuntimeError(f"Échec du job Cloud Batch {job_id} (état={state})")
        time.sleep(poll_interval_sec)


def _extract_stage1_cohort_winners(shards_dir: Path) -> list[int]:
    """Extrait via DuckDB les châssis vainqueurs des cohortes initiales de Phase A."""
    glob_a = (shards_dir / "shard_phaseA_*.jsonl.gz").as_posix()
    con = duckdb.connect(":memory:")
    rows = con.sql(
        f"""
        WITH max_r AS (
            SELECT island_id, MAX(halving_round) AS mr
            FROM read_json_auto('{glob_a}')
            WHERE record_type = 'PHASE_A_HALVING'
            GROUP BY island_id
        )
        SELECT DISTINCT c.chassis_id, c.cell_fitness
        FROM read_json_auto('{glob_a}') c
        JOIN max_r m ON c.island_id = m.island_id AND c.halving_round = m.mr
        WHERE c.record_type = 'PHASE_A_HALVING' AND c.selected_next = TRUE
        ORDER BY c.cell_fitness DESC, c.chassis_id ASC
        """
    ).fetchall()
    con.close()
    winners = [int(r[0]) for r in rows]
    assert len(winners) >= 1, "Aucun châssis qualifié à l'issue de la Phase A Stage 1 !"
    return winners


def _extract_top_k_final_chassis(shards_dir: Path, top_k: int = 2) -> tuple[int, ...]:
    """Retourne les `top_k` meilleurs châssis à l'issue de la finale Phase A."""
    glob_all_a = (shards_dir / "shard_phaseA*.jsonl.gz").as_posix()
    con = duckdb.connect(":memory:")
    rows = con.sql(
        f"""
        SELECT
            chassis_id,
            MAX(halving_round) AS max_round,
            BOOL_OR(CASE WHEN halving_round = (
                SELECT MAX(halving_round) FROM read_json_auto('{glob_all_a}')
                WHERE record_type = 'PHASE_A_HALVING'
            ) THEN selected_next ELSE FALSE END) AS won_final,
            AVG(cell_fitness) AS mean_fit
        FROM read_json_auto('{glob_all_a}')
        WHERE record_type = 'PHASE_A_HALVING'
        GROUP BY chassis_id
        ORDER BY won_final DESC, max_round DESC, mean_fit DESC, chassis_id ASC
        LIMIT {int(top_k)}
        """
    ).fetchall()
    con.close()
    return tuple(int(r[0]) for r in rows)


def _run_pypy_worker_local(extra_args: list[str]) -> None:
    uv_bin = find_uv()
    cmd = [
        uv_bin,
        "run",
        "--no-project",
        "--python",
        "pypy@3.11",
        "python",
        "-m",
        "campaigns.worker_main",
        *extra_args,
    ]
    _run(cmd)


def _query_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    rel = con.sql(sql)
    cols = list(rel.columns)
    return [dict(zip(cols, row, strict=True)) for row in rel.fetchall()]


def _row_to_genome_eval(row: dict[str, Any]) -> GenomeEvaluation:
    gk = str(row["genome_key"])
    return GenomeEvaluation(
        genome_key=gk,
        genome=decode_genome_key(gk),
        chassis_id=int(row["chassis_id"]),
        n_tables=int(row["n_tables"]),
        n_games=int(row["n_games"]),
        mean_ratio_arbres=float(row["mean_ratio_arbres"]),
        median_table_ratio=float(row["median_table_ratio"]),
        cvar20_tables=float(row["cvar20_tables"]),
        by_n_mean_ratio={
            3: float(row["ratio_n3"]),
            4: float(row["ratio_n4"]),
            5: float(row["ratio_n5"]),
            6: float(row["ratio_n6"]),
        },
        by_n_cvar20={
            3: float(row["cvar20_n3"]),
            4: float(row["cvar20_n4"]),
            5: float(row["cvar20_n5"]),
            6: float(row["cvar20_n6"]),
        },
        mirror_asymmetry_mean=float(row["mirror_asymmetry_mean"]),
        mean_tours=float(row["mean_tours"]),
        pct_tour_8=float(row["pct_tour_8"]),
        pct_reve_rang_1=float(row["pct_reve_rang_1"]),
        pct_reveil_gardiens=float(row["pct_reveil_gardiens"]),
        shannon_entropy=float(row["shannon_entropy"]),
        mem_debt_mean=float(row["mem_debt_mean"]),
        law_stack_mean=float(row["law_stack_mean"]),
        law_stack_max=int(row["law_stack_max"]),
        fiddliness_mean=float(row["fiddliness_mean"]),
        cascade_sweeps_mean=float(row["cascade_sweeps_mean"]),
        mid_combat_interrupts_mean=float(row["mid_combat_interrupts_mean"]),
        x_cognitive=float(row["x_cognitive"]),
        cell_fitness=float(row["cell_fitness"]),
        editorial_score=float(row["editorial_score"]),
        cpu_sec=float(row["cell_cpu_sec"]),
    )


def synthesize_palier4_with_duckdb(
    *,
    job_wall_sec: float,
    execution_mode: str = "batch",
    shards_dir: Path | None = None,
    parquet_path: Path | None = None,
    canon_json_path: Path | None = None,
    digests_dir: Path | None = None,
    bundle_path: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Consolide tous les shards en Parquet ZSTD via DuckDB et génère `canon_unique_32.json` + `digest_palier4_canon.json` (< 30 Ko)."""
    s_dir = shards_dir if shards_dir is not None else LOCAL_SHARDS_DIR
    p_path = parquet_path if parquet_path is not None else PARQUET_PATH
    c_path = canon_json_path if canon_json_path is not None else CANON_JSON_PATH

    glob_pattern = (s_dir / "shard_*.jsonl.gz").as_posix()
    p_path.parent.mkdir(parents=True, exist_ok=True)
    c_path.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(":memory:")
    con.execute(f"CREATE TABLE cells AS SELECT * FROM read_json_auto('{glob_pattern}')")
    con.execute(f"COPY cells TO '{p_path.as_posix()}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    total_games = int(con.sql("SELECT CAST(SUM(n_games) AS INTEGER) FROM cells").fetchall()[0][0])

    # 1. Synthèse Phase A : entonnoir Sequential Halving des 128 châssis
    halving_funnel = _query_dicts(
        con,
        """
        SELECT
            halving_round,
            COUNT(DISTINCT chassis_id) AS n_chassis_in,
            COUNT(DISTINCT CASE WHEN selected_next THEN chassis_id END) AS n_chassis_kept,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(AVG(mean_ratio_arbres), 4) AS mean_ratio_arbres,
            ROUND(AVG(cvar20_tables), 4) AS mean_cvar20,
            ROUND(AVG(shannon_entropy), 4) AS mean_entropy
        FROM cells
        WHERE record_type = 'PHASE_A_HALVING'
        GROUP BY halving_round
        ORDER BY halving_round
        """,
    )

    top_chassis_rows = _query_dicts(
        con,
        """
        SELECT
            chassis_id,
            MAX(halving_round) AS max_round,
            CAST(SUM(n_games) AS INTEGER) AS total_games,
            ROUND(AVG(mean_ratio_arbres), 4) AS mean_ratio_arbres,
            ROUND(AVG(cvar20_tables), 4) AS mean_cvar20,
            ROUND(AVG(ratio_n3), 4) AS ratio_n3,
            ROUND(AVG(ratio_n6), 4) AS ratio_n6,
            ROUND(AVG(shannon_entropy), 4) AS shannon_entropy,
            ROUND(MAX(cell_fitness), 4) AS best_fitness
        FROM cells
        WHERE record_type = 'PHASE_A_HALVING'
        GROUP BY chassis_id
        ORDER BY max_round DESC, best_fitness DESC, chassis_id ASC
        LIMIT 6
        """,
    )

    top16_rows = _query_dicts(
        con,
        """
        SELECT DISTINCT chassis_id
        FROM cells
        WHERE record_type = 'PHASE_A_HALVING' AND halving_round >= 3 AND selected_next = TRUE
        """,
    )
    top_ids_for_axes = [int(r["chassis_id"]) for r in (top16_rows or top_chassis_rows)]
    axis_trends: list[dict[str, Any]] = []
    for axis_name, opts in CHASSIS_AXES_OPTIONS:
        counts = {str(opt): 0 for opt in opts}
        for cid in top_ids_for_axes:
            counts[str(decode_chassis_index(cid)[axis_name])] += 1
        axis_trends.append({"axis": axis_name, "counts_in_top": counts})

    # 2. Reconstruction de l'archive globale MAP-Elites 2D & Régression de Shapley d'ordre 2
    screening_rows = _query_dicts(
        con,
        """
        SELECT *
        FROM cells
        WHERE record_type IN ('PHASE_B_SCREENING', 'PHASE_B_ELITE_127')
        """,
    )
    global_archive = MapElitesArchive2D(n_bins_x=8, n_bins_y=8)
    surrogate = ShapleySurrogateOrder2(ridge_lambda=2.5)
    fit_genomes = []
    fit_targets: list[float] = []
    seen_fit: dict[str, float] = {}

    for r in screening_rows:
        ev = _row_to_genome_eval(r)
        global_archive.add(ev)
        # En cas de double évaluation (16 tables puis 127 tables), privilégier la mesure 127 tables
        if r["record_type"] == "PHASE_B_ELITE_127" or ev.genome_key not in seen_fit:
            seen_fit[ev.genome_key] = ev.cell_fitness

    for gk, target_val in seen_fit.items():
        fit_genomes.append(decode_genome_key(gk))
        fit_targets.append(target_val)
    surrogate.fit(fit_genomes, fit_targets)

    mut_totals = _query_dicts(
        con,
        """
        SELECT
            CAST(COALESCE(SUM(guided_mutations), 0) AS INTEGER) AS guided,
            CAST(COALESCE(SUM(uniform_mutations), 0) AS INTEGER) AS uniform_m
        FROM cells
        WHERE record_type = 'PHASE_B_SCREENING'
        """,
    )[0]
    n_guided = int(mut_totals["guided"])
    n_uniform = int(mut_totals["uniform_m"])

    # 3. Candidats évalués sur les 127 tables circulaires & Validation B0 < B1 < B2 <= B3
    elite_127_rows = _query_dicts(
        con,
        """
        SELECT *
        FROM cells
        WHERE record_type = 'PHASE_B_ELITE_127'
        ORDER BY editorial_score DESC, cvar20_tables DESC, genome_key ASC
        """,
    )
    if not elite_127_rows:
        elite_127_rows = _query_dicts(
            con,
            """
            SELECT *
            FROM cells
            WHERE record_type = 'PHASE_B_SCREENING'
            ORDER BY editorial_score DESC, cvar20_tables DESC, genome_key ASC
            LIMIT 5
            """,
        )

    depth_rows = _query_dicts(
        con,
        """
        SELECT
            genome_key,
            chassis_id,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(AVG(mean_b0), 4) AS mean_b0,
            ROUND(AVG(mean_b1), 4) AS mean_b1,
            ROUND(AVG(mean_b2_k0), 4) AS mean_b2_k0,
            ROUND(AVG(mean_b2_k3), 4) AS mean_b2_k3,
            ROUND(AVG(mean_b3), 4) AS mean_b3,
            ROUND(AVG(delta_v_negociation_crn), 4) AS delta_v_negociation_crn,
            ROUND(AVG(micro_fork_delta_v_unbiased), 4) AS micro_fork_delta_v_unbiased,
            BOOL_AND(monotone_b0_b1_b2) AS monotone_b0_b1_b2,
            BOOL_AND(positive_negotiation) AS positive_negotiation,
            BOOL_AND(b3_non_degenerate) AS b3_non_degenerate,
            BOOL_AND(passed_all_checks) AS passed_all_checks
        FROM cells
        WHERE record_type = 'PHASE_C_DEPTH_VALIDATION'
        GROUP BY genome_key, chassis_id
        ORDER BY passed_all_checks DESC, mean_b2_k3 DESC
        """,
    )
    depth_by_key: dict[tuple[str, int], dict[str, Any]] = {
        (str(d["genome_key"]), int(d["chassis_id"])): d for d in depth_rows
    }

    # Dédupliquer les finalistes 127 tables par (genome_key, chassis_id)
    dedup_127: list[dict[str, Any]] = []
    seen_127_keys: set[tuple[str, int]] = set()
    for r in elite_127_rows:
        pair_k = (str(r["genome_key"]), int(r["chassis_id"]))
        if pair_k not in seen_127_keys:
            seen_127_keys.add(pair_k)
            dedup_127.append(r)

    # Sélection du Canon Unique : priorité absolue aux génomes validés `passed_all_checks`
    ref_key = encode_genome_key(load_mode3_reference_genome())

    def _canon_rank_key(r: dict[str, Any]) -> tuple[int, int, float, float]:
        dep = depth_by_key.get((str(r["genome_key"]), int(r["chassis_id"])))
        passed = 1 if (dep and dep.get("passed_all_checks")) else 0
        has_dep = 1 if dep is not None else 0
        return (
            passed,
            has_dep,
            float(r["editorial_score"]),
            float(r["cvar20_tables"]),
        )

    ranked_127 = sorted(dedup_127, key=_canon_rank_key, reverse=True)
    winner_row = ranked_127[0]
    winner_ev = _row_to_genome_eval(winner_row)
    winner_chassis_id = winner_ev.chassis_id
    winner_tiles = genome_to_tile_profiles(winner_ev.genome)
    winner_depth = depth_by_key.get(
        (winner_ev.genome_key, winner_chassis_id),
        depth_rows[0] if depth_rows else {},
    )

    ref_row = next((r for r in dedup_127 if str(r["genome_key"]) == ref_key), None)

    # Marge d'incertitude inter-îles sur les élites évaluées
    island_cvar_rows = _query_dicts(
        con,
        """
        SELECT island_id, MAX(cvar20_tables) AS best_cvar
        FROM cells
        WHERE record_type IN ('PHASE_B_ELITE_127', 'PHASE_B_SCREENING')
        GROUP BY island_id
        ORDER BY island_id
        """,
    )
    m_isl, se_isl, hw_isl = inter_block_ci95([float(x["best_cvar"]) for x in island_cvar_rows])

    # 4. Écriture de `data/canon_unique_32.json`
    spec_bundle = load_spec_bundle(bundle_path)
    tiles_meta = build_tested_tiles_rules(winner_tiles, bundle=spec_bundle)
    meta_by_slot = {t["slot"]: t for t in tiles_meta}

    selections_map: dict[str, dict[str, Any]] = {}
    changed_vs_mode3: list[str] = []
    ref_genome = load_mode3_reference_genome()
    for idx_s, (slot_id, prof) in enumerate(winner_tiles):
        t_info = meta_by_slot[slot_id]
        if prof != ref_genome[idx_s]:
            changed_vs_mode3.append(f"{slot_id}:{ref_genome[idx_s]}->{prof}")
        selections_map[slot_id] = {
            "profile": prof,
            "nom": t_info["nom"],
            "famille": t_info["famille"],
            "shapley_phi": round(surrogate.phi_main.get((slot_id, prof), 0.0), 5),
            "texte": t_info["texte"],
        }

    top_finalists_summary: list[dict[str, Any]] = []
    for rk_idx, r in enumerate(ranked_127[:5], start=1):
        gk = str(r["genome_key"])
        cid = int(r["chassis_id"])
        dep = depth_by_key.get((gk, cid), {})
        g_tup = decode_genome_key(gk)
        diffs_ref = [
            f"{s}:{ p }"
            for s, p, pr in zip(CANONICAL_32_SLOTS, g_tup, ref_genome, strict=True)
            if p != pr
        ]
        top_finalists_summary.append(
            {
                "rank": rk_idx,
                "chassis_id": cid,
                "is_mode3_ref": gk == ref_key,
                "n_diffs_vs_mode3_ref": len(diffs_ref),
                "diffs_vs_mode3_ref": diffs_ref[:12],
                "mean_ratio_arbres": round(float(r["mean_ratio_arbres"]), 4),
                "median_table_ratio": round(float(r["median_table_ratio"]), 4),
                "cvar20_127_tables": round(float(r["cvar20_tables"]), 4),
                "by_n": {
                    "3": round(float(r["ratio_n3"]), 4),
                    "4": round(float(r["ratio_n4"]), 4),
                    "5": round(float(r["ratio_n5"]), 4),
                    "6": round(float(r["ratio_n6"]), 4),
                },
                "mirror_asymmetry": round(float(r["mirror_asymmetry_mean"]), 4),
                "shannon_entropy": round(float(r["shannon_entropy"]), 4),
                "x_cognitive": round(float(r["x_cognitive"]), 4),
                "editorial_score": round(float(r["editorial_score"]), 4),
                "depth_passed": bool(dep.get("passed_all_checks", False)),
                "b0_b1_b2_b3": [
                    round(float(dep.get("mean_b0", 0.0)), 4),
                    round(float(dep.get("mean_b1", 0.0)), 4),
                    round(float(dep.get("mean_b2_k3", 0.0)), 4),
                    round(float(dep.get("mean_b3", 0.0)), 4),
                ]
                if dep
                else [],
            }
        )

    generated_utc = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    canon_doc: dict[str, Any] = {
        "schema_version": str(spec_bundle.get("meta", {}).get("schema_version", "5.3.1")),
        "campaign": "palier4_canon",
        "generated_at_utc": generated_utc,
        "recommended_chassis": decode_chassis_axes(winner_chassis_id),
        "canon_32_list": [f"{s}:{p}" for s, p in winner_tiles],
        "changes_vs_mode3_reference": changed_vs_mode3,
        "selections": selections_map,
        "scores_127_tables": {
            "n_circular_tables": winner_ev.n_tables,
            "n_games": winner_ev.n_games,
            "mean_ratio_arbres": round(winner_ev.mean_ratio_arbres, 4),
            "median_table_ratio": round(winner_ev.median_table_ratio, 4),
            "cvar20_127_tables": round(winner_ev.cvar20_tables, 4),
            "mirror_asymmetry_mean": round(winner_ev.mirror_asymmetry_mean, 4),
            "by_n_players": {
                str(n_p): {
                    "mean_ratio_arbres": round(winner_ev.by_n_mean_ratio.get(n_p, 0.0), 4),
                    "cvar20_tables": round(winner_ev.by_n_cvar20.get(n_p, 0.0), 4),
                }
                for n_p in (3, 4, 5, 6)
            },
            "mean_tours": round(winner_ev.mean_tours, 3),
            "end_causes_pct": {
                "TOUR_8": round(winner_ev.pct_tour_8, 2),
                "REVE_RANG_1": round(winner_ev.pct_reve_rang_1, 2),
                "REVEIL_GARDIENS": round(winner_ev.pct_reveil_gardiens, 2),
            },
            "shannon_entropy_3_ends": round(winner_ev.shannon_entropy, 4),
            "editorial_score": round(winner_ev.editorial_score, 4),
        },
        "cognitive_sensors": {
            "mem_debt_score": round(winner_ev.mem_debt_mean, 3),
            "law_stack_mean": round(winner_ev.law_stack_mean, 4),
            "law_stack_max": winner_ev.law_stack_max,
            "fiddliness_ratio": round(winner_ev.fiddliness_mean, 3),
            "cascade_sweeps": round(winner_ev.cascade_sweeps_mean, 3),
            "mid_combat_interrupts": round(winner_ev.mid_combat_interrupts_mean, 3),
            "x_cognitive_normalized": round(winner_ev.x_cognitive, 4),
        },
        "strategic_depth_validation": winner_depth,
        "vs_mode3_reference_127_tables": {
            "mode3_mean_ratio": round(float(ref_row["mean_ratio_arbres"]), 4)
            if ref_row
            else None,
            "mode3_cvar20": round(float(ref_row["cvar20_tables"]), 4) if ref_row else None,
            "mode3_entropy": round(float(ref_row["shannon_entropy"]), 4) if ref_row else None,
            "delta_cvar20_canon_minus_mode3": round(
                winner_ev.cvar20_tables - float(ref_row["cvar20_tables"]), 4
            )
            if ref_row
            else None,
            "delta_editorial_score": round(
                winner_ev.editorial_score - float(ref_row["editorial_score"]), 4
            )
            if ref_row
            else None,
        },
        "pareto_top5_finalists": top_finalists_summary,
        "shapley_order2_highlights": {
            "n_unique_genomes_fitted": surrogate.n_samples,
            "guided_mutations": n_guided,
            "uniform_mutations": n_uniform,
            "guided_ratio_actual": round(n_guided / max(1, n_guided + n_uniform), 3),
            "top_positive_profiles": surrogate.top_main_effects(limit=12),
            "top_border_pair_synergies": surrogate.top_pair_interactions(limit=10),
        },
    }
    c_path.write_text(
        json.dumps(canon_doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    # 5. Synthèse exécutive compacte (< 30 Ko avec active_core_rules + 32 tested_tiles_rules)
    pareto_cells = [
        {
            "bin_xy": list(global_archive.coords_for(e)),
            "cvar20": round(e.cvar20_tables, 4),
            "mean_arbres": round(e.mean_ratio_arbres, 4),
            "entropy_h": round(e.shannon_entropy, 4),
            "x_cog": round(e.x_cognitive, 4),
            "ed_score": round(e.editorial_score, 4),
        }
        for e in global_archive.pareto_front()[:8]
    ]

    digest_payload: dict[str, Any] = {
        "campaign": "palier4_canon",
        "generated_at_utc": generated_utc,
        "execution": {
            "mode": execution_mode,
            "region": REGION,
            "wall_sec": round(job_wall_sec, 2),
            "total_games_and_rollouts": total_games,
            "parquet_archive": p_path.relative_to(ROOT).as_posix()
            if p_path.is_relative_to(ROOT)
            else p_path.as_posix(),
            "canon_file": c_path.relative_to(ROOT).as_posix()
            if c_path.is_relative_to(ROOT)
            else c_path.as_posix(),
        },
        "totals": {
            "total_games_and_rollouts": total_games,
            "unique_genomes_evaluated": surrogate.n_samples,
            "map_elites_filled_cells_8x8": len(global_archive.cells),
            "mutations_guided_70_vs_uniform_30": {
                "guided": n_guided,
                "uniform": n_uniform,
                "guided_share": round(n_guided / max(1, n_guided + n_uniform), 3),
            },
            "tested_tiles": [f"{s}:{p}" for s, p in winner_tiles],
        },
        "phase_a_chassis_halving": {
            "funnel_rounds": halving_funnel,
            "top_6_chassis": top_chassis_rows,
            "axis_frequencies_in_qualifiers": axis_trends,
        },
        "canon_unique_32_summary": {
            "recommended_chassis_id": winner_chassis_id,
            "canon_32_profiles": [f"{s}:{p}" for s, p in winner_tiles],
            "changes_vs_mode3_ref": changed_vs_mode3,
            "scores_127_tables": canon_doc["scores_127_tables"],
            "cognitive_sensors": canon_doc["cognitive_sensors"],
            "vs_mode3_reference": canon_doc["vs_mode3_reference_127_tables"],
            "inter_island_best_cvar20_ci95": {
                "n_islands": len(island_cvar_rows),
                "mean": round(m_isl, 4),
                "se": round(se_isl, 4),
                "ci95": [round(m_isl - hw_isl, 4), round(m_isl + hw_isl, 4)],
            },
        },
        "map_elites_pareto_front": pareto_cells,
        "top_5_finalists_127_tables": top_finalists_summary,
        "strategic_depth_b0_b1_b2_b3": depth_rows[:5],
        "shapley_order2_top_effects": {
            "top_main_profiles": surrogate.top_main_effects(limit=10),
            "top_pair_interactions": surrogate.top_pair_interactions(limit=8),
        },
    }

    digest_path, prompt_path, full_digest = write_digest_and_prompt_files(
        "palier4_canon",
        digest_payload,
        chassis_ids=(winner_chassis_id,),
        tested_tiles=winner_tiles,
        digests_dir=digests_dir,
        max_bytes=MAX_PALIER4_DIGEST_BYTES,
        bundle_path=bundle_path,
    )
    encoded_size = len(digest_path.read_bytes())
    assert encoded_size < MAX_PALIER4_DIGEST_BYTES, (
        f"digest_palier4_canon.json dépasse 30 Ko : {encoded_size} octets"
    )

    print("\n=== SYNTHÈSE DUCKDB PALIER 4 — CANON UNIQUE 32 PROFILS ===")
    print(f"• Châssis recommandé : #{winner_chassis_id} -> {decode_chassis_axes(winner_chassis_id)}")
    print(
        f"• 127 tables (Mode 4): moyenne={winner_ev.mean_ratio_arbres * 100:.2f}% | "
        f"médiane={winner_ev.median_table_ratio * 100:.2f}% | "
        f"CVaR_20%={winner_ev.cvar20_tables * 100:.2f}% | "
        f"entropie H={winner_ev.shannon_entropy:.3f}"
    )
    print(
        f"• Par taille de table: N=3:{winner_ev.by_n_mean_ratio.get(3, 0.0) * 100:.1f}% | "
        f"N=4:{winner_ev.by_n_mean_ratio.get(4, 0.0) * 100:.1f}% | "
        f"N=5:{winner_ev.by_n_mean_ratio.get(5, 0.0) * 100:.1f}% | "
        f"N=6:{winner_ev.by_n_mean_ratio.get(6, 0.0) * 100:.1f}%"
    )
    print(
        f"• Canon écrit        : {c_path.relative_to(ROOT).as_posix() if c_path.is_relative_to(ROOT) else c_path.as_posix()}"
    )
    print(
        f"• Digest écrit       : {digest_path.relative_to(ROOT).as_posix() if digest_path.is_relative_to(ROOT) else digest_path.as_posix()} "
        f"({encoded_size} octets < 30 Ko)"
    )
    print(
        f"• Dossier Gemini     : {prompt_path.relative_to(ROOT).as_posix() if prompt_path.is_relative_to(ROOT) else prompt_path.as_posix()}"
    )
    con.close()
    return canon_doc, full_digest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Orchestrateur Palier 4 : Canon Unique 32 Tuiles (Cloud Batch Spot / Cloud Run / Local PyPy)"
    )
    parser.add_argument(
        "--mode",
        choices=("batch", "cloudrun", "local"),
        default="batch",
        help="Moteur d'exécution : Cloud Batch Spot ('batch'), Cloud Run Jobs ('cloudrun') ou PyPy local ('local').",
    )
    parser.add_argument("--quote-only", action="store_true", help="Affiche uniquement la pré-vérification et le devis 5 lignes.")
    parser.add_argument("--synthesize-only", action="store_true", help="Relance uniquement la synthèse DuckDB sur les shards existants.")
    parser.add_argument("--skip-build", action="store_true", help="Réutilise l'image worker-pypy existante sans Cloud Build.")
    parser.add_argument("--halving-cohorts", type=int, default=16)
    parser.add_argument("--base-reps-a", type=int, default=1)
    parser.add_argument("--islands", type=int, default=8)
    parser.add_argument("--n-init", type=int, default=8)
    parser.add_argument("--n-generations", type=int, default=8)
    parser.add_argument("--batch-per-gen", type=int, default=4)
    parser.add_argument("--reps-127", type=int, default=1)
    parser.add_argument("--top-finalists-k", type=int, default=3)
    parser.add_argument("--depth-reps", type=int, default=2)
    parser.add_argument("--workers", type=int, default=None)

    args = parser.parse_args(argv)

    if args.synthesize_only:
        canon_doc, full_digest = synthesize_palier4_with_duckdb(
            job_wall_sec=0.0,
            execution_mode=args.mode,
        )
        winner_cid = int(canon_doc["recommended_chassis"]["chassis_id"])
        winner_tiles = tuple(
            (s, str(canon_doc["selections"][s]["profile"])) for s in CANONICAL_32_SLOTS
        )
        publish_campaign_digest(
            "palier4_canon",
            full_digest,
            chassis_ids=[winner_cid],
            tested_tiles=winner_tiles,
            push_gcs=(args.mode != "local"),
        )
        # Ré-appliquer le plafond strict < 30 Ko après publication
        write_digest_and_prompt_files(
            "palier4_canon",
            full_digest,
            chassis_ids=(winner_cid,),
            tested_tiles=winner_tiles,
            max_bytes=MAX_PALIER4_DIGEST_BYTES,
        )
        return 0

    preflight_check_and_quote(
        mode=args.mode,
        halving_cohorts=args.halving_cohorts,
        base_reps_a=args.base_reps_a,
        islands=args.islands,
        n_init=args.n_init,
        n_generations=args.n_generations,
        batch_per_gen=args.batch_per_gen,
        reps_127=args.reps_127,
        top_finalists_k=args.top_finalists_k,
        depth_reps=args.depth_reps,
        local_workers=args.workers,
    )
    if args.quote_only:
        return 0

    if LOCAL_SHARDS_DIR.exists():
        shutil.rmtree(LOCAL_SHARDS_DIR)
    LOCAL_SHARDS_DIR.mkdir(parents=True, exist_ok=True)

    t_start = time.perf_counter()

    if args.mode == "local":
        n_workers = args.workers or max(1, os.cpu_count() or 2)
        # 1. Phase A Stage 1 : 128 -> 16 en local multi-cœurs sous PyPy 3.11
        _run_pypy_worker_local(
            [
                "--campaign-palier4-phase-a",
                f"--halving-cohorts={args.halving_cohorts}",
                f"--base-reps={args.base_reps_a}",
                "--task-index=0",
                "--task-count=1",
                f"--workers={n_workers}",
                f"--local-out-dir={LOCAL_SHARDS_DIR.as_posix()}",
            ]
        )
        stage1_winners = _extract_stage1_cohort_winners(LOCAL_SHARDS_DIR)
        if len(stage1_winners) > 1:
            winners_csv = ",".join(str(c) for c in stage1_winners)
            _run_pypy_worker_local(
                [
                    "--campaign-palier4-phase-a",
                    f"--chassis-ids={winners_csv}",
                    f"--base-reps={max(1, args.base_reps_a * 2)}",
                    "--round-offset=3",
                    "--shard-tag=phaseA_final",
                    "--task-index=0",
                    "--task-count=1",
                    "--workers=1",
                    f"--local-out-dir={LOCAL_SHARDS_DIR.as_posix()}",
                ]
            )
        top_chassis = _extract_top_k_final_chassis(LOCAL_SHARDS_DIR, top_k=2)
        top_csv = ",".join(str(c) for c in top_chassis)

        # 2. Phase B & Étape 2 : îles MAP-Elites + 127 tables + B0..B3
        _run_pypy_worker_local(
            [
                "--campaign-palier4-phase-b",
                f"--chassis-id={top_chassis[0]}",
                f"--chassis-ids={top_csv}",
                f"--islands={args.islands}",
                f"--n-init={args.n_init}",
                f"--n-generations={args.n_generations}",
                f"--batch-per-gen={args.batch_per_gen}",
                f"--reps-127={args.reps_127}",
                f"--top-finalists-k={args.top_finalists_k}",
                f"--depth-reps={args.depth_reps}",
                "--task-index=0",
                "--task-count=1",
                f"--workers={n_workers}",
                f"--local-out-dir={LOCAL_SHARDS_DIR.as_posix()}",
            ]
        )
    elif args.mode == "batch":
        gcloud = find_gcloud()
        if not args.skip_build:
            _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])

        subprocess.run(
            [gcloud, "storage", "rm", f"{GCS_PREFIX}/shard_*.jsonl.gz"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )

        # Phase A sur Cloud Batch Spot (4 tâches x 4 vCPU c3d-highcpu-4 = 16 cohortes)
        tasks_a = min(args.halving_cohorts, 4)
        spec_a = build_cloud_batch_job_spec(
            [
                "--campaign-palier4-phase-a",
                f"--halving-cohorts={args.halving_cohorts}",
                f"--base-reps={args.base_reps_a}",
                "--workers=4",
            ],
            task_count=tasks_a,
            parallelism=tasks_a,
            vcpus_per_task=4,
        )
        _submit_and_wait_batch_job(gcloud, "amazonia-p4-phase-a", spec_a)
        _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_phaseA_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])

        stage1_winners = _extract_stage1_cohort_winners(LOCAL_SHARDS_DIR)
        if len(stage1_winners) > 1:
            winners_csv = ",".join(str(c) for c in stage1_winners)
            _run_pypy_worker_local(
                [
                    "--campaign-palier4-phase-a",
                    f"--chassis-ids={winners_csv}",
                    f"--base-reps={max(1, args.base_reps_a * 2)}",
                    "--round-offset=3",
                    "--shard-tag=phaseA_final",
                    "--task-index=0",
                    "--task-count=1",
                    "--workers=1",
                    f"--local-out-dir={LOCAL_SHARDS_DIR.as_posix()}",
                ]
            )
        top_chassis = _extract_top_k_final_chassis(LOCAL_SHARDS_DIR, top_k=2)
        top_csv = ",".join(str(c) for c in top_chassis)

        # Phase B sur Cloud Batch Spot (c3d-highcpu-4 Spot, maxRunDuration=7200s)
        tasks_b = max(1, min(args.islands, 8))
        spec_b = build_cloud_batch_job_spec(
            [
                "--campaign-palier4-phase-b",
                f"--chassis-id={top_chassis[0]}",
                f"--chassis-ids={top_csv}",
                f"--islands={args.islands}",
                f"--n-init={args.n_init}",
                f"--n-generations={args.n_generations}",
                f"--batch-per-gen={args.batch_per_gen}",
                f"--reps-127={args.reps_127}",
                f"--top-finalists-k={args.top_finalists_k}",
                f"--depth-reps={args.depth_reps}",
                "--workers=4",
            ],
            task_count=tasks_b,
            parallelism=tasks_b,
            vcpus_per_task=4,
        )
        _submit_and_wait_batch_job(gcloud, "amazonia-p4-phase-b", spec_b)
        _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_phaseB_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])
    else:
        gcloud = find_gcloud()
        if not args.skip_build:
            _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])

        subprocess.run(
            [gcloud, "storage", "rm", f"{GCS_PREFIX}/shard_*.jsonl.gz"],
            cwd=ROOT,
            check=False,
            capture_output=True,
        )

        tasks_a = min(args.halving_cohorts, 8)
        _run(
            [
                gcloud,
                "run",
                "jobs",
                "deploy",
                CLOUDRUN_JOB_PHASE_A,
                "--image",
                IMAGE_URI,
                "--region",
                REGION,
                "--tasks",
                str(tasks_a),
                "--parallelism",
                str(tasks_a),
                "--cpu=2",
                "--memory=1Gi",
                "--max-retries=1",
                "--task-timeout=900s",
                f"--args=--campaign-palier4-phase-a,--halving-cohorts={args.halving_cohorts},--base-reps={args.base_reps_a},--workers=2",
            ]
        )
        _run([gcloud, "run", "jobs", "execute", CLOUDRUN_JOB_PHASE_A, "--region", REGION, "--wait"])
        _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_phaseA_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])

        stage1_winners = _extract_stage1_cohort_winners(LOCAL_SHARDS_DIR)
        if len(stage1_winners) > 1:
            winners_csv = ",".join(str(c) for c in stage1_winners)
            _run_pypy_worker_local(
                [
                    "--campaign-palier4-phase-a",
                    f"--chassis-ids={winners_csv}",
                    f"--base-reps={max(1, args.base_reps_a * 2)}",
                    "--round-offset=3",
                    "--shard-tag=phaseA_final",
                    "--task-index=0",
                    "--task-count=1",
                    "--workers=1",
                    f"--local-out-dir={LOCAL_SHARDS_DIR.as_posix()}",
                ]
            )
        top_chassis = _extract_top_k_final_chassis(LOCAL_SHARDS_DIR, top_k=2)
        top_csv = ",".join(str(c) for c in top_chassis)

        tasks_b = max(1, min(args.islands, 16))
        _run(
            [
                gcloud,
                "run",
                "jobs",
                "deploy",
                CLOUDRUN_JOB_PHASE_B,
                "--image",
                IMAGE_URI,
                "--region",
                REGION,
                "--tasks",
                str(tasks_b),
                "--parallelism",
                str(tasks_b),
                "--cpu=2",
                "--memory=2Gi",
                "--max-retries=1",
                "--task-timeout=1800s",
                (
                    f"--args=--campaign-palier4-phase-b,--chassis-id={top_chassis[0]},"
                    f"--islands={args.islands},--n-init={args.n_init},"
                    f"--n-generations={args.n_generations},--batch-per-gen={args.batch_per_gen},"
                    f"--reps-127={args.reps_127},--top-finalists-k={args.top_finalists_k},"
                    f"--depth-reps={args.depth_reps},--workers=2"
                ),
            ]
        )
        _run([gcloud, "run", "jobs", "execute", CLOUDRUN_JOB_PHASE_B, "--region", REGION, "--wait"])
        _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_phaseB_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])

    wall_sec = time.perf_counter() - t_start
    canon_doc, full_digest = synthesize_palier4_with_duckdb(
        job_wall_sec=wall_sec,
        execution_mode=args.mode,
    )
    winner_cid = int(canon_doc["recommended_chassis"]["chassis_id"])
    winner_tiles = tuple(
        (s, str(canon_doc["selections"][s]["profile"])) for s in CANONICAL_32_SLOTS
    )
    publish_campaign_digest(
        "palier4_canon",
        full_digest,
        chassis_ids=[winner_cid],
        tested_tiles=winner_tiles,
        push_gcs=(args.mode != "local"),
    )
    write_digest_and_prompt_files(
        "palier4_canon",
        full_digest,
        chassis_ids=(winner_cid,),
        tested_tiles=winner_tiles,
        max_bytes=MAX_PALIER4_DIGEST_BYTES,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
