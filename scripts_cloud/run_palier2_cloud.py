"""Orchestrateur Cloud Run Jobs & synthèse DuckDB du tir Palier 2 (Cœur Coopératif Muet)."""

from __future__ import annotations

import json
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

import engine.effects  # noqa: F401
from campaigns.designs import inter_block_ci95, paired_mirror_blocks
from campaigns.worker_main import build_palier2_work_units
from engine.effects.lot_01 import LOT_01_PROFILES
from engine.effects.registry import list_registered_tiles
from engine.state import CHASSIS_AXES_OPTIONS, MATRICE_PAIRES
from scripts_cloud.studio_paths import find_gcloud, find_uv

REGION = "europe-west9"
IMAGE_URI = "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest"
JOB_NAME = "amazonia-palier2"
TASK_COUNT = 16
CPU_PER_TASK = "2"
MEMORY_PER_TASK = "1Gi"

REPS_COOP = 12
FORKS_PER_TABLE = 2
HALVING_COHORTS = 16

GCS_PREFIX = "gs://amazonia-sim-runs/palier2_coeur_muet"
LOCAL_RUN_DIR = ROOT / ".tmp_runs" / "palier2_coeur_muet"
LOCAL_SHARDS_DIR = LOCAL_RUN_DIR / "shards"
PARQUET_PATH = LOCAL_RUN_DIR / "cells.parquet"
DIGEST_PATH = ROOT / "data" / "digest_palier2_coeur_muet.json"
DIGESTS_COPY_PATH = ROOT / "data" / "digests" / "digest_palier2_coeur_muet.json"


def _run(cmd: list[str]) -> None:
    print(f"$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def preflight_check_and_quote() -> tuple[int, float]:
    """Pré-vérification métier obligatoire (skill run-campaign) + micro-tir local PyPy 20 parties."""
    registered = set(list_registered_tiles())
    for slot_id, prof in LOT_01_PROFILES:
        assert (slot_id, prof) in registered, f"Profil Lot 01 non enregistré : {slot_id}:{prof}"

    # Vérification d'activabilité géométrique sur les blocs miroirs de la campagne
    blocks = paired_mirror_blocks(blocks_per_n=2, reps_per_side=REPS_COOP, exp_seed=20262201)
    present_slots: set[str] = set()
    for blk in blocks:
        for p_tup in (blk.peuples, blk.mirror_peuples):
            n = len(p_tup)
            for i in range(n):
                t0, t1 = MATRICE_PAIRES[f"{p_tup[i]}_{p_tup[(i + 1) % n]}"]
                present_slots.add(t0)
                present_slots.add(t1)
    for slot_id, _ in LOT_01_PROFILES:
        assert slot_id in present_slots, f"Tuile {slot_id} absente des tables miroirs !"

    # Micro-tir local de 20 parties sous PyPy 3.11 avec garde-fou max_steps=2000 (< 1,5 s après JIT)
    uv_bin = find_uv()
    micro_code = (
        "import time; import engine.effects; "
        "from bots import play_game_b2; "
        "from engine.effects.lot_01 import LOT_01_PROFILES; "
        "from engine.state import GameConfig, GameState; "
        "[play_game_b2(GameState(GameConfig(n_players=4, mode=2, exp_seed=9, rep_id=k)), max_steps=2000) for k in range(15)]; "
        "t0=time.perf_counter(); "
        "[play_game_b2(GameState(GameConfig(n_players=4, mode=3, peuples=('M','R','O','H'), tile_profiles=LOT_01_PROFILES, exp_seed=77, rep_id=i)), max_steps=2000) for i in range(20)]; "
        "dt=time.perf_counter()-t0; "
        "print(round(dt, 4)); "
        "assert dt < 1.5, f'Micro-tir trop lent : {dt:.3f}s'"
    )
    proc = subprocess.run(
        [uv_bin, "run", "--no-project", "--python", "pypy@3.11", "python", "-c", micro_code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    micro_sec = float(proc.stdout.strip().splitlines()[-1])

    units = build_palier2_work_units(
        reps_per_table_coop=REPS_COOP,
        forks_per_table=FORKS_PER_TABLE,
        halving_cohorts=HALVING_COHORTS,
    )
    coop_games = sum(len(u["rep_ids"]) for u in units if u["unit_kind"] == "COOP_MATRIX")
    fork_games = sum(len(u["rep_ids"]) * 18 for u in units if u["unit_kind"] == "MICRO_FORK")
    halving_games = HALVING_COHORTS * (8 * 24 + 4 * 48 + 2 * 96)
    total_games = coop_games + fork_games + halving_games

    gps_per_vcpu = 20.0 / max(0.05, micro_sec)
    est_compute_sec = total_games / (TASK_COUNT * int(CPU_PER_TASK) * gps_per_vcpu)

    print("\n=== DEVIS DE VALIDATION (5 LIGNES) ===")
    print(
        "1. Question testée                   : La révision muette du 2e Défenseur sous paravent aide-t-elle vraiment "
        "l'équipe à sauver la forêt, et quelles variantes de règles de base sont les plus équilibrées ?"
    )
    print(
        "2. Ce qu'on compare                  : Joueurs sans révision vs avec révision (réflexe, découverte, expérimenté), "
        "jeu sans tuiles / tuiles muettes / 8 premières tuiles actives, et tri des 128 réglages de règles."
    )
    print(
        f"3. Tables & nombre de joueurs couverts: {len(blocks) * 2} tables circulaires (avec leurs miroirs inversés) "
        "couvrant 3, 4, 5 et 6 joueurs."
    )
    print(
        f"4. Volume & durée estimée            : {total_games} parties simulées — attente estimée ~{est_compute_sec + 20:.0f} secondes."
    )
    print("5. Coût estimé                       : 0 € (inclus dans le palier gratuit).\n", flush=True)
    return total_games, micro_sec


def _query_dicts(con: duckdb.DuckDBPyConnection, sql: str) -> list[dict[str, Any]]:
    rel = con.sql(sql)
    cols = list(rel.columns)
    return [dict(zip(cols, row, strict=True)) for row in rel.fetchall()]


def synthesize_with_duckdb(job_wall_sec: float, expected_total_games: int) -> dict[str, Any]:
    """Agrège les shards JSONL.gz via DuckDB, archive en Parquet ZSTD et génère digest < 30 Ko."""
    glob_pattern = (LOCAL_SHARDS_DIR / "shard_*.jsonl.gz").as_posix()
    parquet_posix = PARQUET_PATH.as_posix()
    PARQUET_PATH.parent.mkdir(parents=True, exist_ok=True)

    con = duckdb.connect(":memory:")
    con.execute(f"CREATE TABLE cells AS SELECT * FROM read_json_auto('{glob_pattern}')")
    con.execute(f"COPY cells TO '{parquet_posix}' (FORMAT PARQUET, COMPRESSION ZSTD)")

    task_rows = _query_dicts(
        con,
        """
        SELECT
            task_index,
            MAX(task_games) AS games,
            ROUND(MAX(task_wall_sec), 3) AS compute_sec,
            ROUND(MAX(task_games_per_sec), 1) AS games_per_sec
        FROM cells
        GROUP BY task_index
        ORDER BY task_index
        """,
    )
    total_games = int(con.sql("SELECT CAST(SUM(n_games) AS INTEGER) FROM cells").fetchall()[0][0])
    assert total_games == expected_total_games, (
        f"Total parties inattendu : {total_games} != {expected_total_games}"
    )
    max_compute_sec = max(float(r["compute_sec"]) for r in task_rows)
    mean_compute_sec = round(
        sum(float(r["compute_sec"]) for r in task_rows) / max(1, len(task_rows)), 3
    )
    sum_worker_gps = round(sum(float(r["games_per_sec"]) for r in task_rows), 1)
    effective_gps = round(total_games / max_compute_sec, 1) if max_compute_sec > 0 else 0.0

    # 1. Synthèse Volet A : Hiérarchie B0 / B1 / B2, gain K=3 vs K=0 & 4 capteurs cognitifs
    coop_by_mode_policy = _query_dicts(
        con,
        """
        SELECT
            mode,
            policy_id,
            bot_name,
            k_max,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(sum_ratio_arbres) / SUM(n_games), 4) AS mean_ratio_arbres,
            ROUND(AVG(cvar20_ratio), 4) AS cvar20_inter_tables,
            ROUND(AVG(p50_ratio), 4) AS median_ratio_inter_tables,
            ROUND(SUM(sum_tours) * 1.0 / SUM(n_games), 3) AS mean_tours,
            ROUND(SUM(count_tour_8) * 100.0 / SUM(n_games), 2) AS pct_tour_8,
            ROUND(SUM(count_reve_rang_1) * 100.0 / SUM(n_games), 2) AS pct_reve_rang_1,
            ROUND(SUM(count_reveil_gardiens) * 100.0 / SUM(n_games), 2) AS pct_reveil_gardiens,
            ROUND(AVG(mean_mem_debt), 3) AS mem_debt_score,
            ROUND(AVG(mean_law_stack), 4) AS law_stack_mean,
            CAST(MAX(max_law_stack) AS INTEGER) AS law_stack_max,
            ROUND(AVG(mean_fiddliness), 3) AS fiddliness_ratio,
            ROUND(AVG(mean_cascade_sweeps), 3) AS cascade_sweeps,
            ROUND(AVG(mean_mid_combat_interrupts), 3) AS mid_combat_interrupts
        FROM cells
        WHERE record_type = 'COOP_MATRIX'
        GROUP BY mode, policy_id, bot_name, k_max
        ORDER BY mode, policy_id
        """,
    )

    # Intervalles de confiance à 95 % STRICTEMENT INTER-BLOCS sur les différences appariées CRN
    paired_deltas: list[dict[str, Any]] = []
    comparisons = (
        ("B1_K3", "B1_K0", "Gain révision 2.2 muette (B1 K=3 - K=0)"),
        ("B2_K3", "B2_K0", "Gain révision 2.2 muette (B2 K=3 - K=0)"),
        ("B1_K3", "B0_K0", "Progression B1_K3 vs Baseline B0"),
        ("B2_K3", "B1_K3", "Progression B2_K3 (economie_bot) vs B1_K3"),
        ("B2_K3", "B0_K0", "Gain total cœur coopératif B2_K3 vs B0"),
    )
    for mode in (1, 2, 3):
        for pol_hi, pol_lo, label in comparisons:
            blk_rows = _query_dicts(
                con,
                f"""
                WITH block_pol AS (
                    SELECT
                        block_id,
                        policy_id,
                        SUM(sum_ratio_arbres) / SUM(n_games) AS blk_ratio
                    FROM cells
                    WHERE record_type = 'COOP_MATRIX' AND mode = {mode}
                      AND policy_id IN ('{pol_hi}', '{pol_lo}')
                    GROUP BY block_id, policy_id
                )
                SELECT
                    a.block_id,
                    (a.blk_ratio - b.blk_ratio) AS delta_ratio
                FROM block_pol a
                JOIN block_pol b
                  ON a.block_id = b.block_id
                WHERE a.policy_id = '{pol_hi}' AND b.policy_id = '{pol_lo}'
                ORDER BY a.block_id
                """,
            )
            diffs = [float(r["delta_ratio"]) for r in blk_rows]
            m_diff, se_diff, hw95 = inter_block_ci95(diffs)
            paired_deltas.append(
                {
                    "mode": mode,
                    "comparison": f"{pol_hi} - {pol_lo}",
                    "label": label,
                    "n_mirror_blocks": len(diffs),
                    "mean_delta_ratio": round(m_diff, 5),
                    "se_inter_block": round(se_diff, 5),
                    "ci95_low": round(m_diff - hw95, 5),
                    "ci95_high": round(m_diff + hw95, 5),
                }
            )

    # Impact Mode 3 (Lot 01) vs Mode 2 à vide pour B2_K3 (inter-blocs CRN)
    m3_vs_m2_rows = _query_dicts(
        con,
        """
        WITH bp AS (
            SELECT block_id, mode, SUM(sum_ratio_arbres) / SUM(n_games) AS blk_ratio
            FROM cells
            WHERE record_type = 'COOP_MATRIX' AND policy_id = 'B2_K3' AND mode IN (2, 3)
            GROUP BY block_id, mode
        )
        SELECT a.block_id, (a.blk_ratio - b.blk_ratio) AS d
        FROM bp a JOIN bp b ON a.block_id = b.block_id
        WHERE a.mode = 3 AND b.mode = 2
        ORDER BY a.block_id
        """,
    )
    m32, se32, hw32 = inter_block_ci95([float(r["d"]) for r in m3_vs_m2_rows])
    lot01_impact = {
        "comparison": "Mode 3 (Lot 01) - Mode 2 (Asymétrie à vide) sous B2_K3",
        "n_mirror_blocks": len(m3_vs_m2_rows),
        "mean_delta_ratio": round(m32, 5),
        "se_inter_block": round(se32, 5),
        "ci95_low": round(m32 - hw32, 5),
        "ci95_high": round(m32 + hw32, 5),
    }

    # 2. Synthèse Volet B : Micro-Forks sans biais (sélection != évaluation)
    micro_forks_summary = _query_dicts(
        con,
        """
        SELECT
            mode,
            bot_name,
            CAST(SUM(fork_anchors) AS INTEGER) AS n_anchors,
            CAST(SUM(n_games) AS INTEGER) AS total_rollouts,
            ROUND(SUM(fork_diverged) * 100.0 / NULLIF(SUM(fork_anchors), 0), 2) AS pct_diverged_in_2_2,
            ROUND(SUM(sum_delta_v_neg) / NULLIF(SUM(fork_anchors), 0), 5) AS mean_delta_v_negociation,
            ROUND(SUM(sum_c_prive) / NULLIF(SUM(fork_anchors), 0), 5) AS mean_c_prive,
            ROUND(SUM(sum_g_naive) / NULLIF(SUM(fork_anchors), 0), 5) AS mean_g_naive_selection,
            ROUND(SUM(sum_g_unbiased) / NULLIF(SUM(fork_anchors), 0), 5) AS mean_g_unbiased_eval,
            ROUND(SUM(sum_rho_delta) / NULLIF(SUM(fork_anchors), 0), 4) AS mean_rho_delta
        FROM cells
        WHERE record_type = 'MICRO_FORK'
        GROUP BY mode, bot_name
        ORDER BY mode, bot_name
        """,
    )

    # 3. Synthèse Volet C : Entonnoir Sequential Halving des 128 châssis (128 -> 64 -> 32 -> 16)
    halving_rounds_overview = _query_dicts(
        con,
        """
        SELECT
            halving_round,
            COUNT(DISTINCT chassis_id) AS n_chassis_evaluated,
            COUNT(DISTINCT CASE WHEN selected_next THEN chassis_id END) AS n_chassis_kept,
            CAST(SUM(n_games) AS INTEGER) AS n_games,
            ROUND(SUM(CASE WHEN mode = 1 THEN sum_ratio_arbres ELSE 0 END) /
                  NULLIF(SUM(CASE WHEN mode = 1 THEN n_games ELSE 0 END), 0), 4) AS mean_ratio_mode1,
            ROUND(SUM(CASE WHEN mode = 2 THEN sum_ratio_arbres ELSE 0 END) /
                  NULLIF(SUM(CASE WHEN mode = 2 THEN n_games ELSE 0 END), 0), 4) AS mean_ratio_mode2
        FROM cells
        WHERE record_type = 'CHASSIS_HALVING'
        GROUP BY halving_round
        ORDER BY halving_round
        """,
    )

    top16_finalists = _query_dicts(
        con,
        """
        WITH winners AS (
            SELECT DISTINCT chassis_id
            FROM cells
            WHERE record_type = 'CHASSIS_HALVING' AND halving_round = 3 AND selected_next = TRUE
        )
        SELECT
            c.chassis_id,
            MAX(c.p_max) AS p_max,
            CAST(SUM(c.n_games) AS INTEGER) AS total_games_cumul,
            ROUND(SUM(CASE WHEN c.mode = 1 THEN c.sum_ratio_arbres ELSE 0 END) /
                  SUM(CASE WHEN c.mode = 1 THEN c.n_games ELSE 0 END), 4) AS ratio_mode1,
            ROUND(SUM(CASE WHEN c.mode = 2 THEN c.sum_ratio_arbres ELSE 0 END) /
                  SUM(CASE WHEN c.mode = 2 THEN c.n_games ELSE 0 END), 4) AS ratio_mode2,
            ROUND(AVG(CASE WHEN c.mode = 2 THEN c.cvar20_ratio END), 4) AS cvar20_mode2,
            ROUND(SUM(CASE WHEN c.mode = 2 THEN c.count_tour_8 ELSE 0 END) * 100.0 /
                  SUM(CASE WHEN c.mode = 2 THEN c.n_games ELSE 0 END), 1) AS m2_pct_t8,
            ROUND(SUM(CASE WHEN c.mode = 2 THEN c.count_reve_rang_1 ELSE 0 END) * 100.0 /
                  SUM(CASE WHEN c.mode = 2 THEN c.n_games ELSE 0 END), 1) AS m2_pct_reve,
            ROUND(SUM(CASE WHEN c.mode = 2 THEN c.count_reveil_gardiens ELSE 0 END) * 100.0 /
                  SUM(CASE WHEN c.mode = 2 THEN c.n_games ELSE 0 END), 1) AS m2_pct_reveil
        FROM cells c
        JOIN winners w ON c.chassis_id = w.chassis_id
        WHERE c.record_type = 'CHASSIS_HALVING'
        GROUP BY c.chassis_id
        ORDER BY (ratio_mode1 + ratio_mode2) DESC, c.chassis_id
        """,
    )

    # Fréquence des 7 axes binaires parmi les 16 châssis finalistes
    winner_ids = [int(r["chassis_id"]) for r in top16_finalists]
    axis_trends: list[dict[str, Any]] = []
    for bit_pos, (axis_name, opts_pair) in enumerate(CHASSIS_AXES_OPTIONS):
        cnt_opt1 = sum(1 for cid in winner_ids if ((cid >> bit_pos) & 1) == 1)
        cnt_opt0 = len(winner_ids) - cnt_opt1
        axis_trends.append(
            {
                "axis": axis_name,
                "option_0": str(opts_pair[0]),
                "count_0_in_top16": cnt_opt0,
                "option_1": str(opts_pair[1]),
                "count_1_in_top16": cnt_opt1,
            }
        )

    digest: dict[str, Any] = {
        "campaign": "palier2_coeur_muet",
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
            "mean_worker_compute_sec": mean_compute_sec,
            "sum_worker_games_per_sec": sum_worker_gps,
            "effective_cluster_compute_games_per_sec": effective_gps,
        },
        "totals": {
            "total_games_and_rollouts": total_games,
            "n_shards": len(task_rows),
            "lot_01_profiles": [f"{s}:{p}" for s, p in LOT_01_PROFILES],
            "parquet_archive": PARQUET_PATH.relative_to(ROOT).as_posix(),
        },
        "coop_matrix_and_telemetry": coop_by_mode_policy,
        "paired_inter_block_ci95": paired_deltas,
        "lot_01_mode3_vs_mode2_b2": lot01_impact,
        "micro_forks_step_2_2": micro_forks_summary,
        "chassis_sequential_halving": {
            "funnel_rounds": halving_rounds_overview,
            "top_16_finalists": top16_finalists,
            "top_16_axis_frequencies": axis_trends,
        },
        "worker_shards": task_rows,
    }

    DIGEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    DIGESTS_COPY_PATH.parent.mkdir(parents=True, exist_ok=True)
    raw_json = json.dumps(digest, indent=2, ensure_ascii=False) + "\n"
    encoded = raw_json.encode("utf-8")
    assert len(encoded) < 30_000, f"Digest trop volumineux : {len(encoded)} >= 30000 octets"
    DIGEST_PATH.write_text(raw_json, encoding="utf-8", newline="\n")
    DIGESTS_COPY_PATH.write_text(raw_json, encoding="utf-8", newline="\n")

    print("\n=== SYNTHÈSE DUCKDB PALIER 2 — MATRICE COOPÉRATIVE & TÉLÉMÉTRIE ===")
    con.sql(
        """
        SELECT
            mode,
            policy_id,
            CAST(SUM(n_games) AS INTEGER) AS games,
            ROUND(SUM(sum_ratio_arbres) * 100.0 / SUM(n_games), 2) AS pct_arbres,
            ROUND(AVG(cvar20_ratio) * 100.0, 2) AS pct_cvar20,
            ROUND(AVG(mean_mem_debt), 2) AS mem_debt,
            ROUND(AVG(mean_law_stack), 3) AS law_mean,
            ROUND(AVG(mean_fiddliness), 2) AS fiddliness,
            ROUND(AVG(mean_cascade_sweeps), 2) AS sweeps
        FROM cells
        WHERE record_type = 'COOP_MATRIX'
        GROUP BY mode, policy_id
        ORDER BY mode, policy_id
        """
    ).show()

    print(
        f"Digest écrit : {DIGEST_PATH.relative_to(ROOT).as_posix()} ({len(encoded)} octets < 30 Ko)"
    )
    con.close()
    return digest


def main() -> int:
    expected_games, _ = preflight_check_and_quote()
    gcloud = find_gcloud()

    # 1. Build & Push de l'image PyPy 3.11 mise à jour (engine + bots + campaigns + Lot 01)
    _run([gcloud, "builds", "submit", "--config", "cloudbuild.yaml", "."])

    # 2. Nettoyage préventif des anciens shards GCS sous le préfixe palier2_coeur_muet
    subprocess.run(
        [gcloud, "storage", "rm", f"{GCS_PREFIX}/shard_*.jsonl.gz"],
        cwd=ROOT,
        check=False,
        capture_output=True,
    )

    # 3. Déploiement du Cloud Run Job (16 tâches parallèles x 2 vCPU, 1Gi, europe-west9)
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
            (
                f"--args=--campaign-palier2,--reps-coop={REPS_COOP},"
                f"--forks-per-table={FORKS_PER_TABLE},--halving-cohorts={HALVING_COHORTS},"
                f"--workers={CPU_PER_TASK}"
            ),
        ]
    )

    # 4. Exécution synchrone du tir scientifique Palier 2 sur Cloud Run Jobs
    t_job_start = time.perf_counter()
    _run([gcloud, "run", "jobs", "execute", JOB_NAME, "--region", REGION, "--wait"])
    job_wall_sec = time.perf_counter() - t_job_start
    print(f"Tir Cloud Run Palier 2 terminé en {job_wall_sec:.2f}s murale.", flush=True)

    # 5. Rapatriement local des 16 shards depuis GCS
    if LOCAL_SHARDS_DIR.exists():
        shutil.rmtree(LOCAL_SHARDS_DIR)
    LOCAL_SHARDS_DIR.mkdir(parents=True, exist_ok=True)
    _run([gcloud, "storage", "cp", f"{GCS_PREFIX}/shard_*.jsonl.gz", str(LOCAL_SHARDS_DIR)])

    # 6. Agrégation DuckDB, archive Parquet ZSTD & génération de data/digest_palier2_coeur_muet.json
    synthesize_with_duckdb(job_wall_sec=job_wall_sec, expected_total_games=expected_games)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
