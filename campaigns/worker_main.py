"""Worker Cloud PyPy 3.11 stdlib pure pour amazonia-sim-lab (Smoke, Paliers 1, 2 & 4)."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
import multiprocessing
import os
import platform
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import engine.effects  # noqa: F401
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.designs import (
    MANDATORY_6_CIRCLES,
    MirrorBlock,
    mirror_peuples,
    paired_mirror_blocks,
    run_micro_fork_on_config,
    sequential_halving_select,
)
from campaigns.digest_builder import (
    build_mobile_one_tap_html,
    build_prompt_gemini_markdown,
    build_self_contained_digest,
    chassis_id_to_studio_index_128,
    studio_index_128_to_chassis_id,
)
from campaigns.map_elites import (
    CANONICAL_32_SLOTS,
    GenomeEvaluation,
    StrategicDepthReport,
    build_127_circular_tables,
    encode_genome_key,
    evaluate_genome_on_tables,
    genome_to_tile_profiles,
    load_mode3_reference_genome,
    run_map_elites_island,
    run_phase_a_chassis_halving,
    validate_strategic_depth,
)
from engine.effects.lot_01 import LOT_01_PROFILES
from engine.primitives import CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS, CAUSE_TOUR_8
from engine.rng import SRC_BOT_TIEBREAK, shuffle_deterministic
from engine.state import (
    CHASSIS_AXES_OPTIONS,
    PEUPLES_ORDER,
    STATE_BUF_SIZE,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker

METADATA_TOKEN_URL: str = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/token"
)
BUCKET_NAME: str = "amazonia-sim-runs"
SMOKE_OBJECT_NAME: str = "smoke/shard_00.jsonl.gz"
MOBILE_LATEST_OBJECT: str = "mobile/latest.html"
PALIER1_PREFIX: str = "palier1_baseline"
PALIER2_PREFIX: str = "palier2_coeur_muet"
PALIER4_PREFIX: str = "palier4_canon"

PALIER1_CHASSIS_IDS: tuple[int, ...] = (0, 1, 4, 5, 127)

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

PALIER2_POLICIES: tuple[tuple[str, str, int], ...] = (
    ("B0_K0", "B0", 0),
    ("B1_K0", "B1", 0),
    ("B1_K3", "B1", 3),
    ("B2_K0", "B2", 0),
    ("B2_K3", "B2", 3),
)


def _fetch_gcp_access_token() -> str:
    req = urllib.request.Request(
        METADATA_TOKEN_URL,
        headers={"Metadata-Flavor": "Google"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return str(payload["access_token"])


def _upload_gcs_bytes(
    bucket: str,
    object_name: str,
    data: bytes,
    token: str,
    *,
    content_type: str = "application/gzip",
) -> dict[str, Any]:
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
            "Content-Type": content_type,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return dict(json.loads(resp.read().decode("utf-8")))


def _download_gcs_bytes(bucket: str, object_name: str, token: str) -> bytes:
    encoded_name = urllib.parse.quote(object_name, safe="")
    url = f"https://storage.googleapis.com/storage/v1/b/{bucket}/o/{encoded_name}?alt=media"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}"},
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return bytes(resp.read())


def _upload_worker_mobile_latest_html(
    campaign_slug: str,
    records: list[dict[str, Any]],
    *,
    chassis_ids: tuple[int, ...],
    tested_tiles: tuple[tuple[str, str], ...],
    token: str,
) -> None:
    """Génère et pousse `gs://amazonia-sim-runs/mobile/latest.html` directement depuis le worker Cloud."""
    total_games = sum(int(r.get("n_games", 0)) for r in records)
    stats_payload: dict[str, Any] = {
        "campaign": campaign_slug,
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "worker_direct_preview": {
            "task_index": 0,
            "shard_records": len(records),
            "shard_games": total_games,
        },
        "shard_00_summary": records[:24],
    }
    digest = build_self_contained_digest(
        stats_payload,
        chassis_ids=chassis_ids,
        tested_tiles=tested_tiles,
    )
    prompt_md = build_prompt_gemini_markdown(digest)
    html_bytes = build_mobile_one_tap_html(campaign_slug, prompt_md, digest).encode("utf-8")
    _upload_gcs_bytes(
        BUCKET_NAME,
        MOBILE_LATEST_OBJECT,
        html_bytes,
        token,
        content_type="text/html; charset=utf-8",
    )


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


def _cvar_bottom_sorted(sorted_vals: list[float], alpha: float = 0.20) -> float:
    if not sorted_vals:
        return 0.0
    k = max(1, round(len(sorted_vals) * alpha))
    return sum(sorted_vals[:k]) / k


# ---------------------------------------------------------------------------
# Campagne Palier 1 (conservée intacte)
# ---------------------------------------------------------------------------


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
        if task_index == 0:
            _upload_worker_mobile_latest_html(
                "palier1_b0",
                records,
                chassis_ids=PALIER1_CHASSIS_IDS,
                tested_tiles=(),
                token=token,
            )
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


# ---------------------------------------------------------------------------
# Campagne Palier 2 : Cœur Coopératif Muet, Micro-Forks, Lot 01 & 128 Châssis
# ---------------------------------------------------------------------------


def _make_cfg_with_mode(
    chassis_id: int,
    *,
    n_players: int,
    mode: int,
    peuples: tuple[str, ...],
    exp_seed: int,
    rep_id: int,
    coordonnateur_initial: int,
    max_revision_passes: int,
) -> GameConfig:
    base = GameConfig.from_chassis_index(
        chassis_id,
        n_players=n_players,
        mode=mode,
        peuples=peuples,
        exp_seed=exp_seed,
        rep_id=rep_id,
        coordonnateur_initial=coordonnateur_initial,
        max_revision_passes=max_revision_passes,
    )
    if mode < 3:
        return base
    return GameConfig(
        n_players=base.n_players,
        mode=mode,
        peuples=base.peuples,
        exp_seed=base.exp_seed,
        rep_id=base.rep_id,
        coordonnateur_initial=base.coordonnateur_initial,
        max_revision_passes=base.max_revision_passes,
        p_max=base.p_max,
        regle_ouverture_reve_multiple=base.regle_ouverture_reve_multiple,
        offset_seuil_parade=base.offset_seuil_parade,
        mise_en_place_tactiques=base.mise_en_place_tactiques,
        declenchement_fin_de_piste=base.declenchement_fin_de_piste,
        role_abatteuse_fin_de_piste=base.role_abatteuse_fin_de_piste,
        synergie_binome_machines=base.synergie_binome_machines,
        tile_profiles=LOT_01_PROFILES,
    )


def _canonical_rot(peuples: tuple[str, ...]) -> tuple[str, ...]:
    rmap = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}
    b = min(range(len(peuples)), key=lambda i: rmap[peuples[i]])
    return peuples[b:] + peuples[:b]


def build_shuffled_halving_cohorts(
    n_chassis: int = 128,
    n_cohorts: int = 16,
    *,
    seed: int = 20264010,
) -> tuple[tuple[int, ...], ...]:
    """Partitionne `0..n_chassis-1` en `n_cohorts` cohortes sans biais modulo sur les bits bas.

    - `n_cohorts == 1` : pool global unique (Sequential Halving non partitionné sans quotas d'axes).
    - `n_cohorts > 1` : permutation Fisher-Yates déterministe avant découpage en tranches égales,
      éliminant le biais `cid % 16` qui imposait des quotas rigides sur les 4 premiers axes binaires.
    """
    assert n_cohorts >= 1 and n_chassis % n_cohorts == 0
    if n_cohorts == 1:
        return (tuple(range(n_chassis)),)
    shuffled = shuffle_deterministic(
        tuple(range(n_chassis)),
        exp_seed=seed,
        rep_id=0,
        source_type=SRC_BOT_TIEBREAK,
        tour=0,
        entity_id=n_cohorts,
    )
    chunk = n_chassis // n_cohorts
    return tuple(
        tuple(shuffled[i * chunk : (i + 1) * chunk])
        for i in range(n_cohorts)
    )


def build_palier2_work_units(
    *,
    reps_per_table_coop: int = 12,
    forks_per_table: int = 2,
    halving_cohorts: int = 16,
    exp_seed: int = 20262201,
) -> list[dict[str, Any]]:
    """Construit les unités de travail parallélisables des 3 volets du Palier 2."""
    blocks: tuple[MirrorBlock, ...] = paired_mirror_blocks(
        blocks_per_n=2, reps_per_side=reps_per_table_coop, exp_seed=exp_seed
    )
    units: list[dict[str, Any]] = []

    # Volet A : COOP_MATRIX (Modes 1, 2, 3 x B0_K0, B1_K0, B1_K3, B2_K0, B2_K3 sur blocs miroirs CRN)
    for mode in (1, 2, 3):
        for pol_id, bot_name, k_max in PALIER2_POLICIES:
            for blk in blocks:
                for is_mirror, (tid, peuples) in enumerate(
                    ((blk.circle_id, blk.peuples), (blk.mirror_id, blk.mirror_peuples))
                ):
                    units.append(
                        {
                            "unit_kind": "COOP_MATRIX",
                            "mode": mode,
                            "policy_id": pol_id,
                            "bot_name": bot_name,
                            "k_max": k_max,
                            "block_id": blk.block_id,
                            "n_players": blk.n_players,
                            "table_id": tid,
                            "mirror_pair_id": f"{blk.circle_id}__{blk.mirror_id}",
                            "is_mirror": bool(is_mirror),
                            "peuples": peuples,
                            "exp_seed": exp_seed,
                            "rep_ids": blk.rep_ids,
                        }
                    )

    # Volet B : MICRO_FORK (Modes 1, 2, 3 x B1, B2 sur ancres Tour 2 & Tour 3, sélection != évaluation)
    for mode in (1, 2, 3):
        for bot_name in ("B1", "B2"):
            for blk in blocks:
                for tid, peuples in ((blk.circle_id, blk.peuples), (blk.mirror_id, blk.mirror_peuples)):
                    units.append(
                        {
                            "unit_kind": "MICRO_FORK",
                            "mode": mode,
                            "bot_name": bot_name,
                            "block_id": blk.block_id,
                            "n_players": blk.n_players,
                            "table_id": tid,
                            "mirror_pair_id": f"{blk.circle_id}__{blk.mirror_id}",
                            "peuples": peuples,
                            "exp_seed": exp_seed + 100_000,
                            "rep_ids": blk.rep_ids[:forks_per_table],
                        }
                    )

    # Volet C : CHASSIS_HALVING (128 châssis mélangés de façon déterministe sans biais modulo)
    cohorts = build_shuffled_halving_cohorts(128, halving_cohorts, seed=exp_seed + 300_000)
    for cohort_idx, cohort_chassis in enumerate(cohorts):
        units.append(
            {
                "unit_kind": "CHASSIS_HALVING",
                "cohort_id": cohort_idx,
                "chassis_ids": cohort_chassis,
                "exp_seed": exp_seed + 300_000,
            }
        )

    return units


def _execute_coop_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    t0 = time.perf_counter()
    mode = int(unit["mode"])
    pol_id = str(unit["policy_id"])
    bot_name = str(unit["bot_name"])
    k_max = int(unit["k_max"])
    n_pl = int(unit["n_players"])
    peuples = tuple(unit["peuples"])
    exp_seed = int(unit["exp_seed"])
    rep_ids: tuple[int, ...] = tuple(unit["rep_ids"])
    n_reps = len(rep_ids)

    ratios: list[float] = []
    sum_arbres = 0
    sum_ratio = 0.0
    sum_sq_ratio = 0.0
    sum_tours = 0
    cnt_t8 = 0
    cnt_reve = 0
    cnt_reveil = 0

    sum_mem_debt = 0
    sum_law_mean = 0.0
    max_law_max = 0
    sum_fiddliness = 0.0
    sum_cascade_sweeps = 0
    sum_mid_combat = 0

    for idx_r, rep_id in enumerate(rep_ids):
        cfg = _make_cfg_with_mode(
            0,
            n_players=n_pl,
            mode=mode,
            peuples=peuples,
            exp_seed=exp_seed,
            rep_id=rep_id,
            coordonnateur_initial=idx_r % n_pl,
            max_revision_passes=k_max,
        )
        trk = TelemetryTracker()
        st = GameState(cfg)
        if bot_name == "B0":
            res = play_game_b0(st, max_steps=2000, chassis_id=0, telemetry=trk)
        elif bot_name == "B1":
            res = play_game_b1(
                st, k_max_passes=k_max, max_steps=2000, chassis_id=0, telemetry=trk
            )
        else:
            res = play_game_b2(
                st, k_max_passes=k_max, max_steps=2000, chassis_id=0, telemetry=trk
            )

        rt = res.ratio_arbres
        ratios.append(rt)
        sum_arbres += res.score_arbres
        sum_ratio += rt
        sum_sq_ratio += rt * rt
        sum_tours += res.tour_fin
        if res.cause_fin == CAUSE_TOUR_8:
            cnt_t8 += 1
        elif res.cause_fin == CAUSE_REVE_RANG_1:
            cnt_reve += 1
        elif res.cause_fin == CAUSE_REVEIL_GARDIENS:
            cnt_reveil += 1

        ts = trk.summary()
        sum_mem_debt += ts.mem_debt_score
        sum_law_mean += ts.law_stack_mean
        max_law_max = max(max_law_max, ts.law_stack_max)
        sum_fiddliness += ts.fiddliness_ratio
        sum_cascade_sweeps += ts.cascade_sweeps
        sum_mid_combat += ts.mid_combat_interrupts

    ratios.sort()
    cpu_sec = time.perf_counter() - t0
    return [
        {
            "record_type": "COOP_MATRIX",
            "mode": mode,
            "policy_id": pol_id,
            "bot_name": bot_name,
            "k_max": k_max,
            "chassis_id": 0,
            "halving_round": 0,
            "selected_next": True,
            "block_id": int(unit["block_id"]),
            "n_players": n_pl,
            "p_max": 4,
            "table_id": str(unit["table_id"]),
            "mirror_pair_id": str(unit["mirror_pair_id"]),
            "n_games": n_reps,
            "sum_arbres": sum_arbres,
            "sum_ratio_arbres": round(sum_ratio, 6),
            "sum_sq_ratio_arbres": round(sum_sq_ratio, 6),
            "mean_ratio_arbres": round(sum_ratio / n_reps, 6),
            "cvar20_ratio": round(_cvar_bottom_sorted(ratios, 0.20), 6),
            "p50_ratio": round(_quantile_sorted(ratios, 0.50), 6),
            "sum_tours": sum_tours,
            "mean_tours": round(sum_tours / n_reps, 6),
            "count_tour_8": cnt_t8,
            "count_reve_rang_1": cnt_reve,
            "count_reveil_gardiens": cnt_reveil,
            "mean_mem_debt": round(sum_mem_debt / n_reps, 4),
            "mean_law_stack": round(sum_law_mean / n_reps, 5),
            "max_law_stack": max_law_max,
            "mean_fiddliness": round(sum_fiddliness / n_reps, 4),
            "mean_cascade_sweeps": round(sum_cascade_sweeps / n_reps, 4),
            "mean_mid_combat_interrupts": round(sum_mid_combat / n_reps, 4),
            "fork_anchors": 0,
            "fork_diverged": 0,
            "sum_delta_v_neg": 0.0,
            "sum_c_prive": 0.0,
            "sum_g_naive": 0.0,
            "sum_g_unbiased": 0.0,
            "sum_rho_delta": 0.0,
            "cell_cpu_sec": round(cpu_sec, 4),
        }
    ]


def _execute_micro_fork_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    t0 = time.perf_counter()
    mode = int(unit["mode"])
    bot_name = str(unit["bot_name"])
    is_b2 = bot_name == "B2"
    n_pl = int(unit["n_players"])
    peuples = tuple(unit["peuples"])
    exp_seed = int(unit["exp_seed"])
    rep_ids: tuple[int, ...] = tuple(unit["rep_ids"])

    n_sel = 3
    n_eval = 4
    rollouts_per_anchor = n_sel * 2 + n_eval * 3  # 18 rollouts par ancre

    anchors_done = 0
    anchors_missed = 0
    diverged_cnt = 0
    sum_dv = 0.0
    sum_cp = 0.0
    sum_gn = 0.0
    sum_gu = 0.0
    sum_rho = 0.0
    sum_v_k3 = 0.0

    for idx_r, rep_id in enumerate(rep_ids):
        anchor_tour = 2 if (idx_r % 2 == 0) else 3
        cfg = _make_cfg_with_mode(
            0,
            n_players=n_pl,
            mode=mode,
            peuples=peuples,
            exp_seed=exp_seed,
            rep_id=rep_id,
            coordonnateur_initial=idx_r % n_pl,
            max_revision_passes=3,
        )
        rec = run_micro_fork_on_config(
            cfg,
            target_tour=anchor_tour,
            is_b2=is_b2,
            n_selection_rollouts=n_sel,
            n_eval_rollouts=n_eval,
        )
        if rec is None:
            anchors_missed += 1
        else:
            anchors_done += 1
            if rec.diverged_in_2_2:
                diverged_cnt += 1
            sum_dv += rec.delta_v_negociation
            sum_cp += rec.c_prive
            sum_gn += rec.g_naive_selection
            sum_gu += rec.g_unbiased_eval
            sum_rho += rec.rho_delta
            sum_v_k3 += rec.v_k3_priv_eval

    cpu_sec = time.perf_counter() - t0
    total_rollouts = anchors_done * rollouts_per_anchor
    denom = max(1, anchors_done)
    return [
        {
            "record_type": "MICRO_FORK",
            "mode": mode,
            "policy_id": f"{bot_name}_FORK",
            "bot_name": bot_name,
            "k_max": 3,
            "chassis_id": 0,
            "halving_round": 0,
            "selected_next": True,
            "block_id": int(unit["block_id"]),
            "n_players": n_pl,
            "p_max": 4,
            "table_id": str(unit["table_id"]),
            "mirror_pair_id": str(unit["mirror_pair_id"]),
            "n_games": total_rollouts,
            "sum_arbres": 0,
            "sum_ratio_arbres": round(sum_v_k3, 6),
            "sum_sq_ratio_arbres": 0.0,
            "mean_ratio_arbres": round(sum_v_k3 / denom, 6),
            "cvar20_ratio": 0.0,
            "p50_ratio": 0.0,
            "sum_tours": 0,
            "mean_tours": 0.0,
            "count_tour_8": 0,
            "count_reve_rang_1": 0,
            "count_reveil_gardiens": 0,
            "mean_mem_debt": 0.0,
            "mean_law_stack": 0.0,
            "max_law_stack": 0,
            "mean_fiddliness": 0.0,
            "mean_cascade_sweeps": 0.0,
            "mean_mid_combat_interrupts": 0.0,
            "fork_anchors": anchors_done,
            "fork_anchors_missed": anchors_missed,
            "fork_diverged": diverged_cnt,
            "sum_delta_v_neg": round(sum_dv, 6),
            "sum_c_prive": round(sum_cp, 6),
            "sum_g_naive": round(sum_gn, 6),
            "sum_g_unbiased": round(sum_gu, 6),
            "sum_rho_delta": round(sum_rho, 6),
            "cell_cpu_sec": round(cpu_sec, 4),
        }
    ]


def _execute_halving_cohort_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    """Exécute le Sequential Halving en Modes 1 & 2 sur les 6 paires de cercles miroirs CRN."""
    cohort_id = int(unit["cohort_id"])
    active_chassis: tuple[int, ...] = tuple(int(c) for c in unit["chassis_ids"])
    base_seed = int(unit["exp_seed"])

    # 6 paires = les 6 cercles obligatoires de couverture complète appariés à leurs miroirs exacts
    mirror_pairs: list[tuple[int, tuple[str, ...], tuple[str, ...]]] = []
    for _, p_tup in MANDATORY_6_CIRCLES:
        c_a = _canonical_rot(p_tup)
        c_b = _canonical_rot(mirror_peuples(c_a))
        mirror_pairs.append((len(c_a), c_a, c_b))

    # Budgets doublants par round jusqu'à 1 survivant (pour 8 châssis : 1, 2, 4 reps/table)
    round_specs_list: list[tuple[int, int, int]] = []
    rem = len(active_chassis)
    r_idx = 1
    while rem > 1:
        next_keep = max(1, rem // 2)
        round_specs_list.append((r_idx, 1 << (r_idx - 1), next_keep))
        rem = next_keep
        r_idx += 1
    if not round_specs_list:
        round_specs_list.append((1, 1, 1))
    round_specs: tuple[tuple[int, int, int], ...] = tuple(round_specs_list)

    out_records: list[dict[str, Any]] = []
    for r_num, reps_per_tbl, keep_k in round_specs:
        round_seed = base_seed + r_num * 50_000
        composite_scores: dict[int, float] = {}
        staged_rows: list[tuple[int, dict[str, Any]]] = []

        for ch_id in active_chassis:
            mode_scores: list[float] = []
            for mode in (1, 2):
                t_c = time.perf_counter()
                ratios: list[float] = []
                sum_arbres = 0
                sum_ratio = 0.0
                sum_sq_ratio = 0.0
                sum_tours = 0
                cnt_t8 = 0
                cnt_reve = 0
                cnt_reveil = 0
                sum_fidd = 0.0
                p_max_val = 4

                # CRN strict : les deux orientations d'une paire miroir partagent le même rep_id
                for pair_idx, (n_pl, c_a, c_b) in enumerate(mirror_pairs):
                    for rep_off in range(reps_per_tbl):
                        rep_id = pair_idx * reps_per_tbl + rep_off
                        for peuples in (c_a, c_b):
                            cfg = _make_cfg_with_mode(
                                ch_id,
                                n_players=n_pl,
                                mode=mode,
                                peuples=peuples,
                                exp_seed=round_seed,
                                rep_id=rep_id,
                                coordonnateur_initial=rep_off % n_pl,
                                max_revision_passes=3,
                            )
                            p_max_val = cfg.p_max
                            trk = TelemetryTracker()
                            res = play_game_b2(
                                GameState(cfg),
                                k_max_passes=3,
                                max_steps=2000,
                                chassis_id=ch_id,
                                telemetry=trk,
                            )
                            rt = res.ratio_arbres
                            ratios.append(rt)
                            sum_arbres += res.score_arbres
                            sum_ratio += rt
                            sum_sq_ratio += rt * rt
                            sum_tours += res.tour_fin
                            if res.cause_fin == CAUSE_TOUR_8:
                                cnt_t8 += 1
                            elif res.cause_fin == CAUSE_REVE_RANG_1:
                                cnt_reve += 1
                            elif res.cause_fin == CAUSE_REVEIL_GARDIENS:
                                cnt_reveil += 1
                            sum_fidd += trk.summary().fiddliness_ratio

                ratios.sort()
                n_g = len(ratios)
                mean_rt = sum_ratio / n_g
                cvar20_rt = _cvar_bottom_sorted(ratios, 0.20)
                # Critère éditorial d'équilibre de châssis : proximité d'un taux d'Arbres sauvés sain (~0.62)
                # pénalisant l'écrasement (trop dur < 0.35) comme la trivialité (> 0.88) + bonus CVaR_20%
                balance_fitness = 1.0 - abs(mean_rt - 0.62) + 0.35 * cvar20_rt
                if mode == 2:
                    # Bonus de diversité des 3 fins en Mode 2 (ni 100 % Tour 8 ni 100 % Rêve précoce)
                    p_t8 = cnt_t8 / n_g
                    p_rv = cnt_reve / n_g
                    p_gd = cnt_reveil / n_g
                    active_ends = sum(1 for px in (p_t8, p_rv, p_gd) if px >= 0.05)
                    balance_fitness += 0.08 * active_ends
                mode_scores.append(balance_fitness)

                rec_row: dict[str, Any] = {
                    "record_type": "CHASSIS_HALVING",
                    "mode": mode,
                    "policy_id": "B2_K3",
                    "bot_name": "B2",
                    "k_max": 3,
                    "chassis_id": ch_id,
                    "halving_round": r_num,
                    "selected_next": False,
                    "block_id": cohort_id,
                    "n_players": 0,
                    "p_max": p_max_val,
                    "table_id": "MANDATORY_6_MIRRORS",
                    "mirror_pair_id": f"COHORT_{cohort_id:02d}",
                    "n_games": n_g,
                    "sum_arbres": sum_arbres,
                    "sum_ratio_arbres": round(sum_ratio, 6),
                    "sum_sq_ratio_arbres": round(sum_sq_ratio, 6),
                    "mean_ratio_arbres": round(mean_rt, 6),
                    "cvar20_ratio": round(cvar20_rt, 6),
                    "p50_ratio": round(_quantile_sorted(ratios, 0.50), 6),
                    "sum_tours": sum_tours,
                    "mean_tours": round(sum_tours / n_g, 6),
                    "count_tour_8": cnt_t8,
                    "count_reve_rang_1": cnt_reve,
                    "count_reveil_gardiens": cnt_reveil,
                    "mean_mem_debt": 0.0,
                    "mean_law_stack": 0.0,
                    "max_law_stack": 0,
                    "mean_fiddliness": round(sum_fidd / n_g, 4),
                    "mean_cascade_sweeps": 0.0,
                    "mean_mid_combat_interrupts": 0.0,
                    "fork_anchors": 0,
                    "fork_diverged": 0,
                    "sum_delta_v_neg": 0.0,
                    "sum_c_prive": 0.0,
                    "sum_g_naive": 0.0,
                    "sum_g_unbiased": 0.0,
                    "sum_rho_delta": 0.0,
                    "cell_cpu_sec": round(time.perf_counter() - t_c, 4),
                }
                staged_rows.append((ch_id, rec_row))

            composite_scores[ch_id] = sum(mode_scores) / len(mode_scores)

        kept_set = set(sequential_halving_select(composite_scores, keep_count=keep_k))
        for ch_id, rec_row in staged_rows:
            rec_row["selected_next"] = ch_id in kept_set
            out_records.append(rec_row)
        active_chassis = tuple(sorted(kept_set))

    return out_records


def _execute_palier2_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    kind = str(unit["unit_kind"])
    if kind == "COOP_MATRIX":
        return _execute_coop_unit(unit)
    if kind == "MICRO_FORK":
        return _execute_micro_fork_unit(unit)
    if kind == "CHASSIS_HALVING":
        return _execute_halving_cohort_unit(unit)
    raise ValueError(f"Unité Palier 2 inconnue : {kind}")


def run_campaign_palier2(
    *,
    reps_per_table_coop: int = 12,
    forks_per_table: int = 2,
    halving_cohorts: int = 16,
    task_index: int | None = None,
    task_count: int | None = None,
    workers: int | None = None,
    local_out_dir: str | None = None,
) -> int:
    """Exécute la tranche `task_index / task_count` de la campagne scientifique Palier 2."""
    if task_index is None:
        task_index = int(
            os.environ.get("CLOUD_RUN_TASK_INDEX", os.environ.get("TASK_INDEX", "0"))
        )
    if task_count is None:
        task_count = int(
            os.environ.get("CLOUD_RUN_TASK_COUNT", os.environ.get("TASK_COUNT", "1"))
        )
    assert 0 <= task_index < task_count

    all_units = build_palier2_work_units(
        reps_per_table_coop=reps_per_table_coop,
        forks_per_table=forks_per_table,
        halving_cohorts=halving_cohorts,
    )
    my_units = [u for idx, u in enumerate(all_units) if idx % task_count == task_index]
    n_procs = workers if workers is not None else max(1, os.cpu_count() or 1)

    t0 = time.perf_counter()
    nested: list[list[dict[str, Any]]]
    if n_procs > 1 and len(my_units) > 1:
        with multiprocessing.Pool(processes=min(n_procs, len(my_units))) as pool:
            nested = pool.map(_execute_palier2_unit, my_units)
    else:
        nested = [_execute_palier2_unit(u) for u in my_units]

    records = [row for sub in nested for row in sub]
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
        object_name = f"{PALIER2_PREFIX}/{shard_filename}"
        token = _fetch_gcp_access_token()
        _upload_gcs_bytes(BUCKET_NAME, object_name, compressed, token)
        if task_index == 0:
            _upload_worker_mobile_latest_html(
                "palier2_coeur_muet",
                records,
                chassis_ids=(0,),
                tested_tiles=LOT_01_PROFILES,
                token=token,
            )
        dest_uri = f"gs://{BUCKET_NAME}/{object_name}"

    print(
        json.dumps(
            {
                "status": "PALIER2_SHARD_OK",
                "task_index": task_index,
                "task_count": task_count,
                "workers": n_procs,
                "units": len(my_units),
                "rows": len(records),
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


# ---------------------------------------------------------------------------
# Campagne Palier 4 : Canon Unique 32 Tuiles (Cloud Batch Spot / Cloud Run / Local)
# ---------------------------------------------------------------------------


def _resolve_task_coords(
    task_index: int | None, task_count: int | None
) -> tuple[int, int]:
    """Résout `(task_index, task_count)` depuis Cloud Batch, Cloud Run ou CLI."""
    if task_index is None:
        raw_idx = (
            os.environ.get("BATCH_TASK_INDEX")
            or os.environ.get("CLOUD_RUN_TASK_INDEX")
            or os.environ.get("TASK_INDEX")
            or "0"
        )
        task_index = int(raw_idx)
    if task_count is None:
        raw_cnt = (
            os.environ.get("BATCH_TASK_COUNT")
            or os.environ.get("CLOUD_RUN_TASK_COUNT")
            or os.environ.get("TASK_COUNT")
            or "1"
        )
        task_count = int(raw_cnt)
    assert 0 <= task_index < task_count
    return task_index, task_count


def _normalize_p4_row(base: dict[str, Any]) -> dict[str, Any]:
    """Garantit un schéma tabulaire uniforme pour l'ingestion DuckDB Parquet ZSTD."""
    template: dict[str, Any] = {
        "record_type": str(base.get("record_type", "UNKNOWN")),
        "island_id": int(base.get("island_id", -1)),
        "halving_round": int(base.get("halving_round", 0)),
        "selected_next": bool(base.get("selected_next", False)),
        "chassis_id": int(base.get("chassis_id", 0)),
        "genome_key": str(base.get("genome_key", "")),
        "n_tables": int(base.get("n_tables", 0)),
        "n_games": int(base.get("n_games", 0)),
        "mean_ratio_arbres": float(base.get("mean_ratio_arbres", 0.0)),
        "median_table_ratio": float(base.get("median_table_ratio", 0.0)),
        "cvar20_tables": float(base.get("cvar20_tables", 0.0)),
        "ratio_n3": float(base.get("ratio_n3", 0.0)),
        "ratio_n4": float(base.get("ratio_n4", 0.0)),
        "ratio_n5": float(base.get("ratio_n5", 0.0)),
        "ratio_n6": float(base.get("ratio_n6", 0.0)),
        "cvar20_n3": float(base.get("cvar20_n3", 0.0)),
        "cvar20_n4": float(base.get("cvar20_n4", 0.0)),
        "cvar20_n5": float(base.get("cvar20_n5", 0.0)),
        "cvar20_n6": float(base.get("cvar20_n6", 0.0)),
        "mirror_asymmetry_mean": float(base.get("mirror_asymmetry_mean", 0.0)),
        "mean_tours": float(base.get("mean_tours", 0.0)),
        "pct_tour_8": float(base.get("pct_tour_8", 0.0)),
        "pct_reve_rang_1": float(base.get("pct_reve_rang_1", 0.0)),
        "pct_reveil_gardiens": float(base.get("pct_reveil_gardiens", 0.0)),
        "shannon_entropy": float(base.get("shannon_entropy", 0.0)),
        "mem_debt_mean": float(base.get("mem_debt_mean", 0.0)),
        "law_stack_mean": float(base.get("law_stack_mean", 0.0)),
        "law_stack_max": int(base.get("law_stack_max", 0)),
        "fiddliness_mean": float(base.get("fiddliness_mean", 0.0)),
        "cascade_sweeps_mean": float(base.get("cascade_sweeps_mean", 0.0)),
        "mid_combat_interrupts_mean": float(base.get("mid_combat_interrupts_mean", 0.0)),
        "x_cognitive": float(base.get("x_cognitive", 0.0)),
        "cell_fitness": float(base.get("cell_fitness", base.get("chassis_fitness", 0.0))),
        "editorial_score": float(base.get("editorial_score", base.get("chassis_fitness", 0.0))),
        "mean_b0": float(base.get("mean_b0", 0.0)),
        "mean_b1": float(base.get("mean_b1", 0.0)),
        "mean_b2_k0": float(base.get("mean_b2_k0", 0.0)),
        "mean_b2_k3": float(base.get("mean_b2_k3", 0.0)),
        "mean_b3": float(base.get("mean_b3", 0.0)),
        "delta_v_negociation_crn": float(base.get("delta_v_negociation_crn", 0.0)),
        "micro_fork_delta_v_unbiased": float(base.get("micro_fork_delta_v_unbiased", 0.0)),
        "monotone_b0_b1_b2": bool(base.get("monotone_b0_b1_b2", False)),
        "positive_negotiation": bool(base.get("positive_negotiation", False)),
        "b3_non_degenerate": bool(base.get("b3_non_degenerate", False)),
        "passed_all_checks": bool(base.get("passed_all_checks", False)),
        "guided_mutations": int(base.get("guided_mutations", 0)),
        "uniform_mutations": int(base.get("uniform_mutations", 0)),
        "cell_cpu_sec": float(base.get("cell_cpu_sec", 0.0)),
    }
    return template


def _parse_chassis_csv(chassis_ids_csv: str | None) -> tuple[int, ...]:
    if not chassis_ids_csv:
        return ()
    return tuple(int(tok.strip()) for tok in chassis_ids_csv.split(",") if tok.strip())


def _execute_p4_phase_a_cohort(unit: dict[str, Any]) -> list[dict[str, Any]]:
    cohort_id = int(unit["cohort_id"])
    chassis_ids: tuple[int, ...] = tuple(int(c) for c in unit["chassis_ids"])
    base_reps = int(unit["base_reps"])
    round_offset = int(unit.get("round_offset", 0))
    exp_seed = int(unit["exp_seed"])
    ref_key = encode_genome_key(load_mode3_reference_genome())

    _, rows = run_phase_a_chassis_halving(
        chassis_ids,
        keep_final=1,
        base_reps_per_table=base_reps,
        round_offset=round_offset,
        exp_seed=exp_seed,
    )
    out: list[dict[str, Any]] = []
    for r in rows:
        r["island_id"] = cohort_id
        r["genome_key"] = ref_key
        r["n_tables"] = 12
        out.append(_normalize_p4_row(r))
    return out


def run_campaign_palier4_phase_a(
    *,
    halving_cohorts: int = 16,
    base_reps: int = 1,
    chassis_ids_csv: str | None = None,
    round_offset: int = 0,
    shard_tag: str = "phaseA",
    task_index: int | None = None,
    task_count: int | None = None,
    workers: int | None = None,
    local_out_dir: str | None = None,
) -> int:
    """Phase A du Palier 4 : Sequential Halving des 128 châssis sur Mode 3 réf + Mode 4."""
    t_idx, t_cnt = _resolve_task_coords(task_index, task_count)
    explicit_chassis = _parse_chassis_csv(chassis_ids_csv)
    if explicit_chassis:
        all_units = [
            {
                "cohort_id": 99,
                "chassis_ids": explicit_chassis,
                "base_reps": base_reps,
                "round_offset": round_offset,
                "exp_seed": 20264050,
            }
        ]
    else:
        cohorts = build_shuffled_halving_cohorts(128, halving_cohorts, seed=20264010)
        all_units = [
            {
                "cohort_id": c_idx,
                "chassis_ids": cohort_chassis,
                "base_reps": base_reps,
                "round_offset": round_offset,
                "exp_seed": 20264010,
            }
            for c_idx, cohort_chassis in enumerate(cohorts)
        ]
    my_units = [u for i, u in enumerate(all_units) if i % t_cnt == t_idx]
    n_procs = workers if workers is not None else max(1, os.cpu_count() or 1)

    t0 = time.perf_counter()
    if n_procs > 1 and len(my_units) > 1:
        with multiprocessing.Pool(processes=min(n_procs, len(my_units))) as pool:
            nested = pool.map(_execute_p4_phase_a_cohort, my_units)
    else:
        nested = [_execute_p4_phase_a_cohort(u) for u in my_units]

    records = [row for sub in nested for row in sub]
    wall_sec = time.perf_counter() - t0
    task_games = sum(int(r["n_games"]) for r in records)
    task_gps = task_games / wall_sec if wall_sec > 0 else 0.0

    for rec in records:
        rec["task_index"] = t_idx
        rec["task_count"] = t_cnt
        rec["task_workers"] = n_procs
        rec["task_games"] = task_games
        rec["task_wall_sec"] = round(wall_sec, 4)
        rec["task_games_per_sec"] = round(task_gps, 2)
        rec["python_impl"] = platform.python_implementation()

    raw_jsonl = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    compressed = gzip.compress(raw_jsonl)
    shard_filename = f"shard_{shard_tag}_{t_idx:02d}.jsonl.gz"

    if local_out_dir is not None:
        out_path = Path(local_out_dir) / shard_filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(compressed)
        dest_uri = str(out_path)
    else:
        object_name = f"{PALIER4_PREFIX}/{shard_filename}"
        token = _fetch_gcp_access_token()
        _upload_gcs_bytes(BUCKET_NAME, object_name, compressed, token)
        dest_uri = f"gs://{BUCKET_NAME}/{object_name}"

    print(
        json.dumps(
            {
                "status": "PALIER4_PHASE_A_SHARD_OK",
                "shard_tag": shard_tag,
                "task_index": t_idx,
                "task_count": t_cnt,
                "workers": n_procs,
                "rows": len(records),
                "games": task_games,
                "wall_sec": round(wall_sec, 3),
                "games_per_sec": round(task_gps, 1),
                "dest": dest_uri,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


def _execute_p4_island_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    island_id = int(unit["island_id"])
    chassis_id = int(unit["chassis_id"])
    n_init = int(unit["n_init"])
    n_generations = int(unit["n_generations"])
    batch_per_gen = int(unit["batch_per_gen"])
    reps_127 = int(unit["reps_127"])
    top_finalists_k = int(unit["top_finalists_k"])
    depth_finalists_k = int(unit.get("depth_finalists_k", 2))
    depth_reps = int(unit["depth_reps"])
    exp_seed = int(unit["exp_seed"])

    archive, _, all_evals, stats = run_map_elites_island(
        chassis_id,
        island_id=island_id,
        n_init=n_init,
        n_generations=n_generations,
        batch_per_gen=batch_per_gen,
        screening_blocks_per_n=2,
        reps_screening=1,
        exp_seed=exp_seed,
    )

    out_rows: list[dict[str, Any]] = []
    for idx_e, ev in enumerate(all_evals):
        d = ev.to_record_dict(record_type="PHASE_B_SCREENING")
        d["island_id"] = island_id
        if idx_e == 0:
            d["guided_mutations"] = stats["guided_mutations"]
            d["uniform_mutations"] = stats["uniform_mutations"]
        out_rows.append(_normalize_p4_row(d))

    # Promotion sur les 127 tables circulaires des meilleurs finalistes Pareto de l'île
    # (+ référence Mode 3 évaluée sur l'île 0 comme témoin de contrôle)
    fast_smoke = bool(unit.get("fast_smoke", False))
    tables_promo = (
        build_127_circular_tables()[:12] if fast_smoke else build_127_circular_tables()
    )
    finalists: list[GenomeEvaluation] = archive.select_top_finalists(top_k=top_finalists_k)
    cand_genomes = [f.genome for f in finalists]
    if island_id == 0:
        ref_g = load_mode3_reference_genome()
        if ref_g not in cand_genomes:
            cand_genomes.append(ref_g)

    promoted_evals: list[GenomeEvaluation] = []
    for cand_g in cand_genomes:
        ev_127 = evaluate_genome_on_tables(
            chassis_id,
            cand_g,
            tables_promo,
            reps_per_table=max(1, reps_127),
            exp_seed=exp_seed + 500_000,
        )
        promoted_evals.append(ev_127)
        d_127 = ev_127.to_record_dict(record_type="PHASE_B_ELITE_127")
        d_127["island_id"] = island_id
        d_127["selected_next"] = True
        out_rows.append(_normalize_p4_row(d_127))

    # Étape 2 : Validation croisée B0 < B1 < B2 <= B3 et Delta_V_neg sur les finalistes 127 tables
    promoted_evals.sort(key=lambda e: (-e.editorial_score, -e.cvar20_tables))
    for top_ev in promoted_evals[: max(1, min(depth_finalists_k, len(promoted_evals)))]:
        depth_rep: StrategicDepthReport = validate_strategic_depth(
            chassis_id,
            top_ev.genome,
            reps_per_table=depth_reps,
            b3_reps_per_table=0 if fast_smoke else 1,
            exp_seed=exp_seed + 800_000,
        )
        d_dep = depth_rep.to_record_dict()
        d_dep["island_id"] = island_id
        out_rows.append(_normalize_p4_row(d_dep))

    return out_rows


def run_campaign_palier4_phase_b(
    *,
    chassis_id: int = 19,
    chassis_ids_csv: str | None = None,
    islands: int = 8,
    n_init: int = 8,
    n_generations: int = 8,
    batch_per_gen: int = 4,
    reps_127: int = 1,
    top_finalists_k: int = 3,
    depth_reps: int = 2,
    fast_smoke: bool = False,
    task_index: int | None = None,
    task_count: int | None = None,
    workers: int | None = None,
    local_out_dir: str | None = None,
) -> int:
    """Phase B & Étape 2 du Palier 4 : îles MAP-Elites + Shapley + 127 tables + B0..B3."""
    t_idx, t_cnt = _resolve_task_coords(task_index, task_count)
    chassis_pool = _parse_chassis_csv(chassis_ids_csv) or (chassis_id,)
    depth_per_island = 1 if fast_smoke else (3 if islands == 1 else 2)

    all_units = [
        {
            "island_id": isl,
            "chassis_id": chassis_pool[isl % len(chassis_pool)],
            "n_init": n_init,
            "n_generations": n_generations,
            "batch_per_gen": batch_per_gen,
            "reps_127": reps_127,
            "top_finalists_k": top_finalists_k,
            "depth_finalists_k": depth_per_island,
            "depth_reps": depth_reps,
            "fast_smoke": fast_smoke,
            "exp_seed": 20264100,
        }
        for isl in range(islands)
    ]
    my_units = [u for i, u in enumerate(all_units) if i % t_cnt == t_idx]
    n_procs = workers if workers is not None else max(1, os.cpu_count() or 1)

    t0 = time.perf_counter()
    if n_procs > 1 and len(my_units) > 1:
        with multiprocessing.Pool(processes=min(n_procs, len(my_units))) as pool:
            nested = pool.map(_execute_p4_island_unit, my_units)
    else:
        nested = [_execute_p4_island_unit(u) for u in my_units]

    records = [row for sub in nested for row in sub]
    wall_sec = time.perf_counter() - t0
    task_games = sum(int(r["n_games"]) for r in records)
    task_gps = task_games / wall_sec if wall_sec > 0 else 0.0

    for rec in records:
        rec["task_index"] = t_idx
        rec["task_count"] = t_cnt
        rec["task_workers"] = n_procs
        rec["task_games"] = task_games
        rec["task_wall_sec"] = round(wall_sec, 4)
        rec["task_games_per_sec"] = round(task_gps, 2)
        rec["python_impl"] = platform.python_implementation()

    raw_jsonl = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    compressed = gzip.compress(raw_jsonl)
    shard_filename = f"shard_phaseB_{t_idx:02d}.jsonl.gz"

    if local_out_dir is not None:
        out_path = Path(local_out_dir) / shard_filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(compressed)
        dest_uri = str(out_path)
    else:
        object_name = f"{PALIER4_PREFIX}/{shard_filename}"
        token = _fetch_gcp_access_token()
        _upload_gcs_bytes(BUCKET_NAME, object_name, compressed, token)
        if t_idx == 0:
            ref_tiles = genome_to_tile_profiles(load_mode3_reference_genome())
            _upload_worker_mobile_latest_html(
                "palier4_canon",
                records,
                chassis_ids=chassis_pool,
                tested_tiles=ref_tiles,
                token=token,
            )
        dest_uri = f"gs://{BUCKET_NAME}/{object_name}"

    print(
        json.dumps(
            {
                "status": "PALIER4_PHASE_B_SHARD_OK",
                "task_index": t_idx,
                "task_count": t_cnt,
                "workers": n_procs,
                "islands": len(my_units),
                "rows": len(records),
                "games": task_games,
                "wall_sec": round(wall_sec, 3),
                "games_per_sec": round(task_gps, 1),
                "dest": dest_uri,
            },
            ensure_ascii=False,
        ),
        flush=True,
    )
    return 0


_MANIFEST_D_SLOTS: tuple[str, ...] = (
    "G3",
    "G7",
    "G10",
    "G11",
    "G14",
    "R4",
    "R5",
    "R6",
    "R8",
    "R10",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
)


def _sanitize_slug(raw: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", raw.strip().lower()).strip("_")
    return cleaned or "campagne_v5_3"


def _match_axis_bit(axis_name: str, val: Any, opts_pair: tuple[Any, Any]) -> int:
    for bit_idx, opt in enumerate(opts_pair):
        if val == opt:
            return bit_idx
        if (
            isinstance(opt, int)
            and isinstance(val, str)
            and val.strip().lstrip("-").isdigit()
            and int(val) == opt
        ):
            return bit_idx
        if isinstance(opt, str) and isinstance(val, str) and val.strip().upper() == opt.upper():
            return bit_idx
    raise ValueError(f"Valeur invalide pour l'axe {axis_name!r} : {val!r} (attendu {opts_pair})")


def resolve_manifest_plan(manifest: dict[str, Any]) -> dict[str, Any]:
    """Résout un manifeste JSON `campaigns/<nom>.json` en plan exécutable déterministe."""
    campaign_name = _sanitize_slug(str(manifest.get("campaign_name", "campagne_v5_3")))
    raw_players = manifest.get("player_counts", [4])
    player_counts = sorted({int(n) for n in raw_players})
    if not player_counts or any(n not in (3, 4, 5, 6) for n in player_counts):
        raise ValueError(f"player_counts invalide (attendu 3..6) : {player_counts}")

    games_per_cfg = max(1, int(manifest.get("games_per_configuration", 1)))
    bot_name = str(manifest.get("bot", "B2")).strip().upper()
    if bot_name not in ("B0", "B1", "B2"):
        raise ValueError(f"Bot non supporté dans le manifeste : {bot_name!r} (attendu B0/B1/B2)")
    k_max = int(manifest.get("k_max", 0 if bot_name == "B0" else 3))
    mode = int(manifest.get("mode", 3))
    exp_seed = int(manifest.get("seed", 20261119))

    # 1. Résolution des châssis (produit cartésien des axes variables + axes figés,
    #    avec repli éventuel sur base_instance.config_index_128 au format Studio 1..128)
    base_inst = manifest.get("base_instance", {})
    raw_studio_idx = base_inst.get("config_index_128")
    base_chassis_default: int = (
        studio_index_128_to_chassis_id(int(raw_studio_idx))
        if raw_studio_idx is not None
        else 0
    )

    chassis_plan = manifest.get("chassis_plan", {})
    fixed_raw = chassis_plan.get("fixed_axes", {})
    fixed_norm: dict[str, Any] = {str(k).lower(): v for k, v in fixed_raw.items()}
    varying_raw = chassis_plan.get("varying_axes", [])
    varying_norm: dict[str, list[Any]] = {}
    for item in varying_raw:
        if isinstance(item, str):
            ax_key = item.lower()
            varying_norm[ax_key] = []
        elif isinstance(item, dict) and "key" in item:
            ax_key = str(item["key"]).lower()
            vals = list(item.get("values", []))
            varying_norm[ax_key] = vals

    axis_bit_choices: list[list[int]] = []
    for bit_pos, (axis_name, opts_pair) in enumerate(CHASSIS_AXES_OPTIONS):
        ax_low = axis_name.lower()
        if ax_low in varying_norm:
            raw_vals = varying_norm[ax_low]
            if not raw_vals:
                axis_bit_choices.append([0, 1])
            else:
                bits = sorted(
                    {_match_axis_bit(axis_name, v, opts_pair) for v in raw_vals}
                )
                axis_bit_choices.append(bits)
        elif ax_low in fixed_norm:
            bit_val = _match_axis_bit(axis_name, fixed_norm[ax_low], opts_pair)
            axis_bit_choices.append([bit_val])
        else:
            axis_bit_choices.append([(base_chassis_default >> bit_pos) & 1])

    chassis_ids: list[int] = []
    for combo in itertools.product(*axis_bit_choices):
        cid = 0
        for bit_pos, b in enumerate(combo):
            cid |= b << bit_pos
        chassis_ids.append(cid)
    chassis_ids = sorted(set(chassis_ids))
    chassis_studio_indices_128 = tuple(chassis_id_to_studio_index_128(c) for c in chassis_ids)

    # 2. Résolution explicite du génome de base (32 slots)
    bundle_id = str(base_inst.get("bundle_id", "STANDARD_A")).strip().upper()
    if bundle_id == "MODE3_REF":
        ref_genome = load_mode3_reference_genome()
        base_map: dict[str, str] = dict(zip(CANONICAL_32_SLOTS, ref_genome, strict=True))
    else:
        base_map = {slot_id: "A" for slot_id in CANONICAL_32_SLOTS}
        if bundle_id == "LOT_01_PILOT":
            for s, p in LOT_01_PROFILES:
                if s in base_map:
                    base_map[s] = p
        elif bundle_id == "ESSAI_52_EMBUSCADE":
            for s in _MANIFEST_D_SLOTS:
                base_map[s] = "D"

    for slot_id, prof in dict(base_inst.get("profile_overrides", {})).items():
        if slot_id in base_map:
            base_map[str(slot_id)] = str(prof).strip().upper()
    for slot_id, prof in dict(base_inst.get("slots_insectes", {})).items():
        if slot_id in base_map:
            base_map[str(slot_id)] = str(prof).strip().upper()

    # 3. Variantes de profils comparés (produit cartésien sur slot_profile_comparisons)
    raw_comps = manifest.get("slot_profile_comparisons", {})
    ordered_comp_slots = [s for s in CANONICAL_32_SLOTS if raw_comps.get(s)]
    comp_lists = [[str(p).strip().upper() for p in raw_comps[s]] for s in ordered_comp_slots]

    migration_slots = ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS")
    migration_varying = [s for s in migration_slots if s in ordered_comp_slots]
    migration_policy: dict[str, Any] = {
        "SLOT_BUG_CERVEAU": base_map["SLOT_BUG_CERVEAU"],
        "SLOT_COLONISATION_GARDIENS": base_map["SLOT_COLONISATION_GARDIENS"],
        "fixed": len(migration_varying) == 0,
        "varying_slots": migration_varying,
    }
    base_slots_canonical = ",".join(f"{s}:{base_map[s]}" for s in CANONICAL_32_SLOTS)
    resolved_32_slots_sha256 = hashlib.sha256(base_slots_canonical.encode("utf-8")).hexdigest()

    profile_variants: list[dict[str, Any]] = []
    tested_tiles_set: list[tuple[str, str]] = []
    if ordered_comp_slots:
        for s, letters in zip(ordered_comp_slots, comp_lists, strict=True):
            for letter in letters:
                pair = (s, letter)
                if pair not in tested_tiles_set:
                    tested_tiles_set.append(pair)
        for v_idx, combo in enumerate(itertools.product(*comp_lists)):
            overrides = dict(zip(ordered_comp_slots, combo, strict=True))
            gmap = dict(base_map)
            gmap.update(overrides)
            v_label = ",".join(f"{s}:{p}" for s, p in overrides.items())
            profile_variants.append(
                {
                    "variant_idx": v_idx,
                    "variant_id": v_label,
                    "compared_slots": overrides,
                    "tile_profiles": tuple((s, gmap[s]) for s in CANONICAL_32_SLOTS),
                }
            )
    else:
        profile_variants.append(
            {
                "variant_idx": 0,
                "variant_id": "BASE",
                "compared_slots": {},
                "tile_profiles": tuple((s, base_map[s]) for s in CANONICAL_32_SLOTS),
            }
        )
        # Inclut les éventuels profils non-A de base pour un digest informatif
        for s in CANONICAL_32_SLOTS:
            if base_map[s] != "A":
                tested_tiles_set.append((s, base_map[s]))

    # 4. Construction des unités de calcul (chaque configuration = games_per_cfg parties,
    #    avec appariement CRN strict sur chaque paire de tables miroirs)
    base_peuples_raw = base_inst.get("peuples_cercle", [])
    base_peuples: tuple[str, ...] = tuple(str(p).strip().upper() for p in base_peuples_raw)

    units: list[dict[str, Any]] = []
    config_idx = 0
    for n_pl in player_counts:
        if (
            len(base_peuples) == n_pl
            and len(set(base_peuples)) == n_pl
            and all(p in PEUPLES_ORDER for p in base_peuples)
        ):
            mir = mirror_peuples(base_peuples)
            t1_id = "-".join(base_peuples)
            t2_id = "-".join(mir)
            if games_per_cfg >= 2 and mir != base_peuples:
                candidate_tables: tuple[tuple[str, tuple[str, ...]], ...] = (
                    (t1_id, base_peuples),
                    (t2_id, mir),
                )
            else:
                candidate_tables = ((t1_id, base_peuples),)
        else:
            all_t = PALIER1_TABLES_BY_N[n_pl]
            candidate_tables = all_t[: min(games_per_cfg, len(all_t))]

        n_tables = len(candidate_tables)
        base_per_tbl = games_per_cfg // n_tables
        rem_tbl = games_per_cfg % n_tables

        # Regroupe les paires miroirs consécutives pour leur affecter le même rep_start (CRN)
        table_groups: list[tuple[bool, tuple[tuple[int, str, tuple[str, ...]], ...]]] = []
        idx_t = 0
        while idx_t < n_tables:
            t_id_a, p_a = candidate_tables[idx_t]
            if (
                idx_t + 1 < n_tables
                and mirror_peuples(p_a) == candidate_tables[idx_t + 1][1]
            ):
                t_id_b, p_b = candidate_tables[idx_t + 1]
                table_groups.append((True, ((idx_t, t_id_a, p_a), (idx_t + 1, t_id_b, p_b))))
                idx_t += 2
            else:
                table_groups.append((False, ((idx_t, t_id_a, p_a),)))
                idx_t += 1

        for ch_id in chassis_ids:
            for var in profile_variants:
                rep_offset = 0
                for is_mirror_pair, grp in table_groups:
                    max_g_in_grp = 0
                    for t_i, t_id, peuples in grp:
                        g_cnt = base_per_tbl + (1 if t_i < rem_tbl else 0)
                        if g_cnt <= 0:
                            continue
                        max_g_in_grp = max(max_g_in_grp, g_cnt)
                        units.append(
                            {
                                "campaign": campaign_name,
                                "config_id": config_idx,
                                "n_players": n_pl,
                                "chassis_id": ch_id,
                                "variant_idx": var["variant_idx"],
                                "variant_id": var["variant_id"],
                                "compared_slots": var["compared_slots"],
                                "tile_profiles": var["tile_profiles"],
                                "table_id": t_id,
                                "peuples": peuples,
                                "is_mirror_pair": is_mirror_pair,
                                "bot": bot_name,
                                "k_max": k_max,
                                "mode": mode,
                                "exp_seed": exp_seed,
                                "rep_start": rep_offset,
                                "n_games": g_cnt,
                            }
                        )
                    rep_offset += max_g_in_grp
                config_idx += 1

    return {
        "campaign_name": campaign_name,
        "player_counts": player_counts,
        "chassis_ids": tuple(chassis_ids),
        "chassis_studio_indices_128": chassis_studio_indices_128,
        "base_studio_config_index_128": (
            int(raw_studio_idx) if raw_studio_idx is not None else None
        ),
        "base_bundle_id": bundle_id,
        "base_tile_profiles": dict(base_map),
        "resolved_32_slots_sha256": resolved_32_slots_sha256,
        "migration_policy": migration_policy,
        "profile_variants": profile_variants,
        "tested_tiles": tuple(tested_tiles_set),
        "games_per_configuration": games_per_cfg,
        "total_configurations": config_idx,
        "total_games": sum(int(u["n_games"]) for u in units),
        "bot": bot_name,
        "k_max": k_max,
        "mode": mode,
        "units": units,
    }


def _execute_manifest_unit(unit: dict[str, Any]) -> dict[str, Any]:
    t0 = time.perf_counter()
    n_pl = int(unit["n_players"])
    ch_id = int(unit["chassis_id"])
    mode = int(unit["mode"])
    peuples = tuple(unit["peuples"])
    tile_profiles = tuple((str(s), str(p)) for s, p in unit["tile_profiles"])
    bot_name = str(unit["bot"])
    k_max = int(unit["k_max"])
    exp_seed = int(unit["exp_seed"])
    rep_start = int(unit["rep_start"])
    n_games = int(unit["n_games"])

    ratios: list[float] = []
    sum_arbres = 0
    sum_ratio = 0.0
    sum_sq_ratio = 0.0
    sum_tours = 0
    cnt_t8 = 0
    cnt_reve = 0
    cnt_reveil = 0
    cnt_arbres_pos = 0
    p_max_val = 4

    sum_mem_debt = 0
    sum_law_mean = 0.0
    max_law_max = 0
    sum_fiddliness = 0.0
    sum_physical_ops = 0
    sum_player_decisions = 0
    sum_cascade_sweeps = 0
    sum_mid_combat = 0

    for i in range(n_games):
        rep_id = rep_start + i
        base_cfg = GameConfig.from_chassis_index(
            ch_id,
            n_players=n_pl,
            mode=mode,
            peuples=peuples,
            exp_seed=exp_seed,
            rep_id=rep_id,
            coordonnateur_initial=rep_id % n_pl,
            max_revision_passes=k_max,
        )
        p_max_val = base_cfg.p_max
        cfg = GameConfig(
            n_players=base_cfg.n_players,
            mode=mode,
            peuples=base_cfg.peuples,
            exp_seed=base_cfg.exp_seed,
            rep_id=base_cfg.rep_id,
            coordonnateur_initial=base_cfg.coordonnateur_initial,
            max_revision_passes=base_cfg.max_revision_passes,
            p_max=base_cfg.p_max,
            regle_ouverture_reve_multiple=base_cfg.regle_ouverture_reve_multiple,
            offset_seuil_parade=base_cfg.offset_seuil_parade,
            mise_en_place_tactiques=base_cfg.mise_en_place_tactiques,
            declenchement_fin_de_piste=base_cfg.declenchement_fin_de_piste,
            role_abatteuse_fin_de_piste=base_cfg.role_abatteuse_fin_de_piste,
            synergie_binome_machines=base_cfg.synergie_binome_machines,
            tile_profiles=tile_profiles if mode >= 3 else (),
        )
        trk = TelemetryTracker()
        st = GameState(cfg)
        if bot_name == "B0":
            res = play_game_b0(st, max_steps=2000, chassis_id=ch_id, telemetry=trk)
        elif bot_name == "B1":
            res = play_game_b1(
                st, k_max_passes=k_max, max_steps=2000, chassis_id=ch_id, telemetry=trk
            )
        else:
            res = play_game_b2(
                st, k_max_passes=k_max, max_steps=2000, chassis_id=ch_id, telemetry=trk
            )

        rt = float(res.ratio_arbres)
        ratios.append(rt)
        sum_arbres += int(res.score_arbres)
        sum_ratio += rt
        sum_sq_ratio += rt * rt
        sum_tours += int(res.tour_fin)
        if res.score_arbres > 0:
            cnt_arbres_pos += 1
        if res.cause_fin == CAUSE_TOUR_8:
            cnt_t8 += 1
        elif res.cause_fin == CAUSE_REVE_RANG_1:
            cnt_reve += 1
        elif res.cause_fin == CAUSE_REVEIL_GARDIENS:
            cnt_reveil += 1

        ts = trk.summary()
        sum_mem_debt += int(ts.mem_debt_score)
        sum_law_mean += float(ts.law_stack_mean)
        max_law_max = max(max_law_max, int(ts.law_stack_max))
        sum_fiddliness += float(ts.fiddliness_ratio)
        sum_physical_ops += int(ts.total_physical_ops)
        sum_player_decisions += int(ts.total_player_decisions)
        sum_cascade_sweeps += int(ts.cascade_sweeps)
        sum_mid_combat += int(ts.mid_combat_interrupts)

    ratios.sort()
    k20 = max(1, (len(ratios) + 4) // 5)
    p20_idx = min(len(ratios) - 1, max(0, int(0.2 * (len(ratios) - 1))))
    cvar20 = sum(ratios[:k20]) / k20
    wall_sec = time.perf_counter() - t0

    return {
        "campaign": str(unit["campaign"]),
        "config_id": int(unit["config_id"]),
        "n_players": n_pl,
        "chassis_id": ch_id,
        "p_max": p_max_val,
        "variant_idx": int(unit["variant_idx"]),
        "variant_id": str(unit["variant_id"]),
        "compared_slots_json": json.dumps(unit["compared_slots"], sort_keys=True, ensure_ascii=False),
        "table_id": str(unit["table_id"]),
        "peuples": "-".join(peuples),
        "bot": bot_name,
        "k_max": k_max,
        "mode": mode,
        "n_games": n_games,
        "sum_arbres": sum_arbres,
        "sum_ratio_arbres": round(sum_ratio, 6),
        "sum_sq_ratio_arbres": round(sum_sq_ratio, 6),
        "min_ratio_arbres": round(ratios[0], 6),
        "max_ratio_arbres": round(ratios[-1], 6),
        "p20_ratio": round(ratios[p20_idx], 6),
        "cvar20_ratio": round(cvar20, 6),
        "count_arbres_pos": cnt_arbres_pos,
        "sum_tours": sum_tours,
        "count_tour_8": cnt_t8,
        "count_reve_rang_1": cnt_reve,
        "count_reveil_gardiens": cnt_reveil,
        "sum_mem_debt": sum_mem_debt,
        "sum_law_mean": round(sum_law_mean, 4),
        "max_law_max": max_law_max,
        "sum_fiddliness": round(sum_fiddliness, 4),
        "sum_physical_ops": sum_physical_ops,
        "sum_player_decisions": sum_player_decisions,
        "sum_cascade_sweeps": sum_cascade_sweeps,
        "sum_mid_combat": sum_mid_combat,
        "cell_wall_sec": round(wall_sec, 4),
    }


def _load_manifest_from_source(source: str) -> dict[str, Any]:
    if source.startswith("gs://"):
        without_scheme = source[5:]
        bucket, _, obj_name = without_scheme.partition("/")
        if not bucket or not obj_name:
            raise ValueError(f"URI GCS invalide : {source}")
        token = _fetch_gcp_access_token()
        raw = _download_gcs_bytes(bucket, obj_name, token)
        return dict(json.loads(raw.decode("utf-8")))
    return dict(json.loads(Path(source).read_text(encoding="utf-8")))


def run_campaign_manifest(
    *,
    manifest_source: str,
    gcs_prefix: str | None = None,
    task_index: int | None = None,
    task_count: int | None = None,
    workers: int | None = None,
    local_out_dir: str | None = None,
) -> int:
    """Exécute un manifeste JSON `campaigns/<nom>.json` sur Cloud Run Jobs / Cloud Batch ou en local."""
    t_idx = (
        task_index
        if task_index is not None
        else int(os.environ.get("CLOUD_RUN_TASK_INDEX", os.environ.get("BATCH_TASK_INDEX", "0")))
    )
    t_cnt = (
        task_count
        if task_count is not None
        else int(os.environ.get("CLOUD_RUN_TASK_COUNT", os.environ.get("BATCH_TASK_COUNT", "1")))
    )
    manifest = _load_manifest_from_source(manifest_source)
    plan = resolve_manifest_plan(manifest)
    campaign_name = str(plan["campaign_name"])
    prefix = gcs_prefix if gcs_prefix else f"campaigns/{campaign_name}"

    all_units: list[dict[str, Any]] = list(plan["units"])
    my_units = [u for i, u in enumerate(all_units) if i % t_cnt == t_idx]
    n_procs = workers if workers is not None else max(1, os.cpu_count() or 1)

    t0 = time.perf_counter()
    if n_procs > 1 and len(my_units) > 1:
        with multiprocessing.Pool(processes=min(n_procs, len(my_units))) as pool:
            records = pool.map(_execute_manifest_unit, my_units)
    else:
        records = [_execute_manifest_unit(u) for u in my_units]

    wall_sec = time.perf_counter() - t0
    task_games = sum(int(r["n_games"]) for r in records)
    task_gps = task_games / wall_sec if wall_sec > 0 else 0.0

    for rec in records:
        rec["task_index"] = t_idx
        rec["task_count"] = t_cnt
        rec["task_workers"] = n_procs
        rec["task_games"] = task_games
        rec["task_wall_sec"] = round(wall_sec, 4)
        rec["task_games_per_sec"] = round(task_gps, 2)
        rec["python_impl"] = platform.python_implementation()

    shard_filename = f"shard_{t_idx:02d}.jsonl.gz"
    if not records:
        print(
            json.dumps(
                {
                    "status": "CAMPAIGN_MANIFEST_SHARD_EMPTY",
                    "campaign": campaign_name,
                    "task_index": t_idx,
                    "task_count": t_cnt,
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        return 0

    raw_jsonl = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records).encode("utf-8")
    compressed = gzip.compress(raw_jsonl)

    if local_out_dir is not None:
        out_path = Path(local_out_dir) / shard_filename
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_bytes(compressed)
        dest_uri = str(out_path)
    else:
        object_name = f"{prefix.rstrip('/')}/{shard_filename}"
        token = _fetch_gcp_access_token()
        _upload_gcs_bytes(BUCKET_NAME, object_name, compressed, token)
        dest_uri = f"gs://{BUCKET_NAME}/{object_name}"

    print(
        json.dumps(
            {
                "status": "CAMPAIGN_MANIFEST_SHARD_OK",
                "campaign": campaign_name,
                "task_index": t_idx,
                "task_count": t_cnt,
                "workers": n_procs,
                "units": len(my_units),
                "games": task_games,
                "wall_sec": round(wall_sec, 3),
                "games_per_sec": round(task_gps, 1),
                "dest": dest_uri,
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
    parser.add_argument(
        "--campaign-palier2",
        action="store_true",
        help="Exécute la campagne Palier 2 (B0/B1/B2 K=0 vs K=3, Micro-Forks, Lot 01 & 128 châssis).",
    )
    parser.add_argument(
        "--campaign-palier4-phase-a",
        action="store_true",
        help="Exécute la Phase A du Palier 4 (Sequential Halving des 128 châssis).",
    )
    parser.add_argument(
        "--campaign-palier4-phase-b",
        action="store_true",
        help="Exécute la Phase B & Étape 2 du Palier 4 (MAP-Elites + Shapley + 127 tables + B0..B3).",
    )
    parser.add_argument(
        "--campaign-manifest",
        type=str,
        default=None,
        help="Chemin local ou URI gs:// vers un manifeste JSON campaigns/<nom>.json.",
    )
    parser.add_argument(
        "--gcs-prefix",
        type=str,
        default=None,
        help="Préfixe GCS dans gs://amazonia-sim-runs pour écrire les shards.",
    )
    parser.add_argument("--total-games", type=int, default=100_000)
    parser.add_argument("--reps-coop", type=int, default=12)
    parser.add_argument("--forks-per-table", type=int, default=2)
    parser.add_argument("--halving-cohorts", type=int, default=16)
    parser.add_argument("--base-reps", type=int, default=1)
    parser.add_argument("--chassis-id", type=int, default=19)
    parser.add_argument("--chassis-ids", type=str, default=None)
    parser.add_argument("--round-offset", type=int, default=0)
    parser.add_argument("--shard-tag", type=str, default="phaseA")
    parser.add_argument("--islands", type=int, default=8)
    parser.add_argument("--n-init", type=int, default=8)
    parser.add_argument("--n-generations", type=int, default=8)
    parser.add_argument("--batch-per-gen", type=int, default=4)
    parser.add_argument("--reps-127", type=int, default=1)
    parser.add_argument("--top-finalists-k", type=int, default=3)
    parser.add_argument("--depth-reps", type=int, default=2)
    parser.add_argument("--task-index", type=int, default=None)
    parser.add_argument("--task-count", type=int, default=None)
    parser.add_argument("--workers", type=int, default=None)
    parser.add_argument("--local-out-dir", type=str, default=None)

    args = parser.parse_args(argv)
    if args.smoke_test:
        return run_smoke_test()
    if args.campaign_manifest:
        return run_campaign_manifest(
            manifest_source=args.campaign_manifest,
            gcs_prefix=args.gcs_prefix,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    if args.campaign_palier1:
        return run_campaign_palier1(
            total_games=args.total_games,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    if args.campaign_palier2:
        return run_campaign_palier2(
            reps_per_table_coop=args.reps_coop,
            forks_per_table=args.forks_per_table,
            halving_cohorts=args.halving_cohorts,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    if args.campaign_palier4_phase_a:
        return run_campaign_palier4_phase_a(
            halving_cohorts=args.halving_cohorts,
            base_reps=args.base_reps,
            chassis_ids_csv=args.chassis_ids,
            round_offset=args.round_offset,
            shard_tag=args.shard_tag,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    if args.campaign_palier4_phase_b:
        return run_campaign_palier4_phase_b(
            chassis_id=args.chassis_id,
            chassis_ids_csv=args.chassis_ids,
            islands=args.islands,
            n_init=args.n_init,
            n_generations=args.n_generations,
            batch_per_gen=args.batch_per_gen,
            reps_127=args.reps_127,
            top_finalists_k=args.top_finalists_k,
            depth_reps=args.depth_reps,
            task_index=args.task_index,
            task_count=args.task_count,
            workers=args.workers,
            local_out_dir=args.local_out_dir,
        )
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
