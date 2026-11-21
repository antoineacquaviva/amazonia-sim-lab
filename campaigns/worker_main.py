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
    chassis_id_to_studio_index_384,
    studio_index_384_to_chassis_id,
)
from engine.primitives import CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS, CAUSE_TOUR_8
from engine.rng import SRC_BOT_TIEBREAK, shuffle_deterministic
from engine.state import (
    ANIMAUX_SAUVAGES,
    CHASSIS_AXES_OPTIONS,
    NUM_CHASSIS,
    PEUPLES_ORDER,
    STATE_BUF_SIZE,
    GameConfig,
    GameState,
    decode_chassis_index,
)
from engine.telemetry import (
    DEFENSE_ATTRIBUTION_FIELDS,
    REVEIL_ANATOMY_FIELDS,
    TelemetryTracker,
)

CANONICAL_32_SLOTS: tuple[str, ...] = (
    *(f"G{i}" for i in range(1, 16)),
    *(f"R{i}" for i in range(1, 11)),
    *(f"M{i}" for i in range(1, 6)),
    "SLOT_BUG_CERVEAU",
    "SLOT_COLONISATION_GARDIENS",
)
LOT_01_PROFILES: tuple[tuple[str, str], ...] = ()

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
        profil_piste=base.profil_piste,
        regle_ouverture_reve_multiple=base.regle_ouverture_reve_multiple,
        offset_seuil_parade=base.offset_seuil_parade,
        placement_initial_machines=base.placement_initial_machines,
        role_abatteuse_fin_de_piste=base.role_abatteuse_fin_de_piste,
        synergie_binome_machines=base.synergie_binome_machines,
        reve_activation_mode=base.reve_activation_mode,
        gardien_bet_cap_policy=base.gardien_bet_cap_policy,
        reve_advance_mode=base.reve_advance_mode,
        tile_profiles=LOT_01_PROFILES,
    )


def _canonical_rot(peuples: tuple[str, ...]) -> tuple[str, ...]:
    rmap = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}
    b = min(range(len(peuples)), key=lambda i: rmap[peuples[i]])
    return peuples[b:] + peuples[:b]


def build_shuffled_halving_cohorts(
    n_chassis: int = NUM_CHASSIS,
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

    # Volet C : CHASSIS_HALVING (384 châssis mélangés de façon déterministe sans biais modulo)
    cohorts = build_shuffled_halving_cohorts(NUM_CHASSIS, halving_cohorts, seed=exp_seed + 300_000)
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
    """Phase A du Palier 4 (archivée en Phase CORE_STABILIZATION)."""
    del (
        halving_cohorts,
        base_reps,
        chassis_ids_csv,
        round_offset,
        shard_tag,
        task_index,
        task_count,
        workers,
        local_out_dir,
    )
    raise RuntimeError(
        "Palier 4 Phase A archivé en Phase CORE_STABILIZATION "
        "(voir archive/legacy_tiles_v5_3/ et le tag archive/v5.4.3-legacy-100-tiles)."
    )


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
    """Phase B du Palier 4 (archivée en Phase CORE_STABILIZATION)."""
    del (
        chassis_id,
        chassis_ids_csv,
        islands,
        n_init,
        n_generations,
        batch_per_gen,
        reps_127,
        top_finalists_k,
        depth_reps,
        fast_smoke,
        task_index,
        task_count,
        workers,
        local_out_dir,
    )
    raise RuntimeError(
        "Palier 4 Phase B archivé en Phase CORE_STABILIZATION "
        "(voir archive/legacy_tiles_v5_3/ et le tag archive/v5.4.3-legacy-100-tiles)."
    )


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
    return cleaned or "campagne_v5_5"


def _match_axis_bit(axis_name: str, val: Any, opts_tuple: tuple[Any, ...]) -> int:
    for opt_idx, opt in enumerate(opts_tuple):
        if val == opt:
            return opt_idx
        if (
            isinstance(opt, int)
            and isinstance(val, str)
            and val.strip().lstrip("-").isdigit()
            and int(val) == opt
        ):
            return opt_idx
        if isinstance(opt, str) and isinstance(val, str) and val.strip().upper() == opt.upper():
            return opt_idx
    raise ValueError(f"Valeur invalide pour l'axe {axis_name!r} : {val!r} (attendu {opts_tuple})")


def resolve_manifest_plan(manifest: dict[str, Any]) -> dict[str, Any]:
    """Résout un manifeste JSON `campaigns/<nom>.json` en plan exécutable déterministe."""
    campaign_name = _sanitize_slug(str(manifest.get("campaign_name", "campagne_v5_5")))
    raw_players = manifest.get("player_counts", [4])
    player_counts = sorted({int(n) for n in raw_players})
    if not player_counts or any(n not in (3, 4, 5, 6) for n in player_counts):
        raise ValueError(f"player_counts invalide (attendu 3..6) : {player_counts}")

    games_per_cfg = max(1, int(manifest.get("games_per_configuration", 1)))
    raw_bots = manifest.get("bots")
    if raw_bots is not None:
        if isinstance(raw_bots, str):
            bot_list = [raw_bots.strip().upper()]
        else:
            bot_list = [str(b).strip().upper() for b in raw_bots]
    else:
        bot_list = [str(manifest.get("bot", "B2")).strip().upper()]
    bot_list = list(dict.fromkeys(bot_list))
    if not bot_list or any(b not in ("B0", "B1", "B2") for b in bot_list):
        raise ValueError(
            f"Bot(s) non supporté(s) dans le manifeste : {bot_list!r} (attendu B0/B1/B2)"
        )
    bot_name = bot_list[0]
    k_max_default = int(manifest.get("k_max", 0 if bot_name == "B0" else 3))
    mode = int(manifest.get("mode", 3))
    exp_seed = int(manifest.get("seed", 20261119))
    include_full_tile_metrics = bool(manifest.get("include_full_tile_metrics", False))

    # 1. Résolution des châssis (produit cartésien des axes variables + axes figés,
    #    avec repli éventuel sur base_instance.config_index_192 au format Studio 1..192)
    base_inst = manifest.get("base_instance", {})
    raw_studio_idx = base_inst.get("config_index_192")
    if raw_studio_idx is None:
        raw_studio_idx = base_inst.get("config_index_384")
    if raw_studio_idx is None:
        raw_studio_idx = base_inst.get("config_index_128")
    base_chassis_default: int = (
        studio_index_384_to_chassis_id(int(raw_studio_idx))
        if raw_studio_idx is not None
        else 0
    )
    base_decoded = decode_chassis_index(base_chassis_default)

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

    axis_opt_choices: list[list[int]] = []
    for axis_name, opts_tuple in CHASSIS_AXES_OPTIONS:
        ax_low = axis_name.lower()
        if ax_low in varying_norm:
            raw_vals = varying_norm[ax_low]
            if not raw_vals:
                axis_opt_choices.append(list(range(len(opts_tuple))))
            else:
                idxs = sorted(
                    {_match_axis_bit(axis_name, v, opts_tuple) for v in raw_vals}
                )
                axis_opt_choices.append(idxs)
        elif ax_low in fixed_norm:
            opt_idx = _match_axis_bit(axis_name, fixed_norm[ax_low], opts_tuple)
            axis_opt_choices.append([opt_idx])
        else:
            axis_opt_choices.append([opts_tuple.index(base_decoded[axis_name])])

    chassis_ids: list[int] = []
    for combo in itertools.product(*axis_opt_choices):
        cid = 0
        mult = 1
        for ax_idx, opt_idx in enumerate(combo):
            cid += opt_idx * mult
            mult *= len(CHASSIS_AXES_OPTIONS[ax_idx][1])
        chassis_ids.append(cid)
    chassis_ids = sorted(set(chassis_ids))
    chassis_studio_indices_192 = tuple(chassis_id_to_studio_index_384(c) for c in chassis_ids)

    # 2. Résolution explicite du génome de base (32 slots)
    bundle_id = str(base_inst.get("bundle_id", "STANDARD_A")).strip().upper()
    base_map: dict[str, str] = {slot_id: "A" for slot_id in CANONICAL_32_SLOTS}
    # Défauts officiels v5.5 : Déviation Synaptique (Bug=B) & Bouclier de lisière (Colonie=B)
    base_map["SLOT_BUG_CERVEAU"] = "B"
    base_map["SLOT_COLONISATION_GARDIENS"] = "B"
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
    varying_tiles_set: list[tuple[str, str]] = []
    if ordered_comp_slots:
        for s, letters in zip(ordered_comp_slots, comp_lists, strict=True):
            for letter in letters:
                pair = (s, letter)
                if pair not in varying_tiles_set:
                    varying_tiles_set.append(pair)
                if pair not in tested_tiles_set:
                    tested_tiles_set.append(pair)
        if mode >= 3:
            for s in CANONICAL_32_SLOTS:
                if s not in ordered_comp_slots and base_map[s] != "A":
                    pair = (s, base_map[s])
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
        # Inclut les éventuels profils non-A actifs en Mode >= 3 (Mode 2 = tuiles neutres)
        if mode >= 3:
            for s in CANONICAL_32_SLOTS:
                if base_map[s] != "A":
                    tested_tiles_set.append((s, base_map[s]))

    # 3b. Paramètres hors-châssis consolidés v5.5
    raw_act_modes = manifest.get("reve_activation_modes", manifest.get("reve_activation_mode"))
    if raw_act_modes is None:
        r_act_modes: list[str] = ["1_DEF_1_MACHINE"]
        explicit_reve_act_sweep = False
    elif isinstance(raw_act_modes, str):
        r_act_modes = [raw_act_modes.strip().upper()]
        explicit_reve_act_sweep = "reve_activation_modes" in manifest
    else:
        r_act_modes = [str(x).strip().upper() for x in raw_act_modes]
        explicit_reve_act_sweep = True
    for ram in r_act_modes:
        if ram not in ("1_DEF_1_MACHINE", "1_DEF_ALL_RANK", "BINOME_ALL_RANK"):
            raise ValueError(f"reve_activation_mode invalide : {ram!r}")

    raw_cap_pols = manifest.get("gardien_bet_cap_policies", manifest.get("gardien_bet_cap_policy"))
    if raw_cap_pols is None:
        cap_pols: list[str] = ["UNIFORM_MAX_2"]
        explicit_cap_pol_sweep = False
    elif isinstance(raw_cap_pols, str):
        cap_pols = [raw_cap_pols.strip().upper()]
        explicit_cap_pol_sweep = "gardien_bet_cap_policies" in manifest
    else:
        cap_pols = [str(x).strip().upper() for x in raw_cap_pols]
        explicit_cap_pol_sweep = True
    for gcp in cap_pols:
        if gcp not in ("UNIFORM_MAX_2", "MAX_2_RES_MAX_1"):
            raise ValueError(f"gardien_bet_cap_policy invalide : {gcp!r}")

    raw_adv_modes = manifest.get("reve_advance_modes", manifest.get("reve_advance_mode"))
    if raw_adv_modes is None:
        adv_modes: list[str] = ["EXCLUSIVE_CHOICE"]
        explicit_adv_mode_sweep = False
    elif isinstance(raw_adv_modes, str):
        adv_modes = [raw_adv_modes.strip().upper()]
        explicit_adv_mode_sweep = "reve_advance_modes" in manifest
    else:
        adv_modes = [str(x).strip().upper() for x in raw_adv_modes]
        explicit_adv_mode_sweep = True
    for radv in adv_modes:
        if radv != "EXCLUSIVE_CHOICE":
            raise ValueError(
                f"reve_advance_mode invalide (v6.0 : EXCLUSIVE_CHOICE uniquement, CLEAR_RANK_ONLY supprimé) : {radv!r}"
            )

    raw_g4_modes = manifest.get("gardien_4_trigger_modes", manifest.get("gardien_4_trigger_mode"))
    if raw_g4_modes is None:
        g4_modes: list[str] = ["DISTINCT_OPEN_1"]
        explicit_g4_mode_sweep = False
    elif isinstance(raw_g4_modes, str):
        g4_modes = [raw_g4_modes.strip().upper()]
        explicit_g4_mode_sweep = "gardien_4_trigger_modes" in manifest
    else:
        g4_modes = [str(x).strip().upper() for x in raw_g4_modes]
        explicit_g4_mode_sweep = True
    for g4m in g4_modes:
        if g4m != "DISTINCT_OPEN_1":
            raise ValueError(
                f"gardien_4_trigger_mode invalide (verrouillé sur DISTINCT_OPEN_1) : {g4m!r}"
            )

    if len(r_act_modes) > 1:
        explicit_reve_act_sweep = True
    if len(cap_pols) > 1:
        explicit_cap_pol_sweep = True
    if len(adv_modes) > 1:
        explicit_adv_mode_sweep = True
    if len(g4_modes) > 1:
        explicit_g4_mode_sweep = True

    expanded_variants: list[dict[str, Any]] = []
    ev_idx = 0
    for var in profile_variants:
        for ram, gcp, radv, g4m in itertools.product(r_act_modes, cap_pols, adv_modes, g4_modes):
            tag_parts: list[str] = []
            if explicit_reve_act_sweep:
                tag_parts.append(f"REVE={ram}")
            if explicit_cap_pol_sweep:
                tag_parts.append(f"CAP={gcp}")
            if explicit_adv_mode_sweep:
                tag_parts.append(f"ADV={radv}")
            if explicit_g4_mode_sweep:
                tag_parts.append(f"G4={g4m}")
            if tag_parts:
                ext_tag = "|".join(tag_parts)
                v_id = ext_tag if var["variant_id"] == "BASE" else f"{var['variant_id']}|{ext_tag}"
            else:
                v_id = str(var["variant_id"])
            expanded_variants.append(
                {
                    "variant_idx": ev_idx,
                    "variant_id": v_id,
                    "compared_slots": dict(var["compared_slots"]),
                    "tile_profiles": var["tile_profiles"],
                    "reve_activation_mode": ram,
                    "gardien_bet_cap_policy": gcp,
                    "reve_advance_mode": radv,
                    "gardien_4_trigger_mode": g4m,
                }
            )
            ev_idx += 1
    profile_variants = expanded_variants

    # 4. Construction des unités de calcul (chaque configuration = games_per_cfg parties,
    #    avec appariement CRN strict sur chaque paire de tables miroirs et par bot)
    base_peuples_raw = base_inst.get("peuples_cercle", [])
    base_peuples: tuple[str, ...] = tuple(str(p).strip().upper() for p in base_peuples_raw)
    table_selection = str(manifest.get("table_selection", "PALIER1_DEFAULT")).strip().upper()
    min_animaux = max(0, int(manifest.get("min_animaux_sauvages", 0)))

    units: list[dict[str, Any]] = []
    config_idx = 0
    for b_name in bot_list:
        b_k_max = 0 if b_name == "B0" else int(manifest.get("k_max", 3))
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
            elif table_selection == "ALL_PEUPLE_COMBOS":
                all_combs = tuple(
                    ("-".join(comb), comb)
                    for comb in itertools.combinations(PEUPLES_ORDER, n_pl)
                    if sum(1 for p in comb if p in ANIMAUX_SAUVAGES) >= min_animaux
                )
                candidate_tables = all_combs[: min(games_per_cfg, len(all_combs))]
            else:
                all_t = tuple(
                    (tid, pl)
                    for tid, pl in PALIER1_TABLES_BY_N[n_pl]
                    if sum(1 for p in pl if p in ANIMAUX_SAUVAGES) >= min_animaux
                )
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
                                    "reve_activation_mode": var["reve_activation_mode"],
                                    "gardien_bet_cap_policy": var["gardien_bet_cap_policy"],
                                    "reve_advance_mode": var["reve_advance_mode"],
                                    "gardien_4_trigger_mode": var["gardien_4_trigger_mode"],
                                    "table_id": t_id,
                                    "peuples": peuples,
                                    "n_animaux_sauvages": sum(
                                        1 for p in peuples if p in ANIMAUX_SAUVAGES
                                    ),
                                    "is_mirror_pair": is_mirror_pair,
                                    "bot": b_name,
                                    "k_max": b_k_max,
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
        "chassis_studio_indices_192": chassis_studio_indices_192,
        "base_studio_config_index_192": (
            int(raw_studio_idx) if raw_studio_idx is not None else None
        ),
        "base_bundle_id": bundle_id,
        "base_tile_profiles": dict(base_map),
        "resolved_32_slots_sha256": resolved_32_slots_sha256,
        "migration_policy": migration_policy,
        "profile_variants": profile_variants,
        "tested_tiles": tuple(tested_tiles_set),
        "varying_tiles": tuple(varying_tiles_set),
        "include_full_tile_metrics": include_full_tile_metrics,
        "games_per_configuration": games_per_cfg,
        "total_configurations": config_idx,
        "total_games": sum(int(u["n_games"]) for u in units),
        "bot": bot_name,
        "bots": tuple(bot_list),
        "k_max": k_max_default,
        "mode": mode,
        "exp_seed": exp_seed,
        "units": units,
    }


def _execute_manifest_unit(unit: dict[str, Any]) -> dict[str, Any]:
    t0 = time.perf_counter()
    n_pl = int(unit["n_players"])
    ch_id = int(unit["chassis_id"])
    mode = int(unit["mode"])
    peuples = tuple(unit["peuples"])
    tile_profiles = tuple((str(s), str(p)) for s, p in unit["tile_profiles"])
    reve_activation_mode = str(unit.get("reve_activation_mode", "1_DEF_1_MACHINE"))
    gardien_bet_cap_policy = str(unit.get("gardien_bet_cap_policy", "UNIFORM_MAX_2"))
    reve_advance_mode = str(unit.get("reve_advance_mode", "EXCLUSIVE_CHOICE"))
    gardien_4_trigger_mode = str(unit.get("gardien_4_trigger_mode", "DISTINCT_OPEN_1"))
    n_animaux = int(
        unit.get("n_animaux_sauvages", sum(1 for p in peuples if p in ANIMAUX_SAUVAGES))
    )
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
    cnt_reveil_attempts = 0
    cnt_reveil_failures = 0
    cnt_gardien_bets_won = 0
    cnt_gardien_bets_lost = 0
    cnt_bouclier_lisiere_saves = 0
    cnt_reves_activated = 0
    cnt_machines_cancelled_by_reve = 0
    cnt_machines_bypassed_inactive_reve = 0
    cnt_reves_choice_block = 0
    cnt_reves_choice_advance = 0
    sum_power_tokens_end_act1 = 0
    cnt_act1_reached = 0
    sum_power_tokens_end_game = 0
    cnt_charge_gains = 0
    cnt_furtivite_1_rive_turns = 0
    cnt_furtivite_2_rives_turns = 0
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
    reveil_anat_acc: dict[str, int] = {k: 0 for k in REVEIL_ANATOMY_FIELDS}
    def_attr_acc: dict[str, int] = {k: 0 for k in DEFENSE_ATTRIBUTION_FIELDS}

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
            reve_activation_mode=reve_activation_mode,
            gardien_bet_cap_policy=gardien_bet_cap_policy,
            reve_advance_mode=reve_advance_mode,
            gardien_4_trigger_mode=gardien_4_trigger_mode,
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
            profil_piste=base_cfg.profil_piste,
            regle_ouverture_reve_multiple=base_cfg.regle_ouverture_reve_multiple,
            offset_seuil_parade=base_cfg.offset_seuil_parade,
            placement_initial_machines=base_cfg.placement_initial_machines,
            role_abatteuse_fin_de_piste=base_cfg.role_abatteuse_fin_de_piste,
            synergie_binome_machines=base_cfg.synergie_binome_machines,
            reve_activation_mode=reve_activation_mode,
            gardien_bet_cap_policy=gardien_bet_cap_policy,
            reve_advance_mode=reve_advance_mode,
            gardien_4_trigger_mode=gardien_4_trigger_mode,
            tile_profiles=tile_profiles if mode >= 2 else (),
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
        cnt_reveil_attempts += int(ts.reveil_attempts)
        cnt_reveil_failures += int(ts.reveil_failures)
        cnt_gardien_bets_won += int(ts.gardien_bets_won)
        cnt_gardien_bets_lost += int(ts.gardien_bets_lost)
        cnt_bouclier_lisiere_saves += int(ts.bouclier_lisiere_saves)
        cnt_reves_activated += int(ts.reves_activated)
        cnt_machines_cancelled_by_reve += int(ts.machines_cancelled_by_reve)
        cnt_machines_bypassed_inactive_reve += int(ts.machines_bypassed_inactive_reve)
        cnt_reves_choice_block += int(ts.reves_choice_block)
        cnt_reves_choice_advance += int(ts.reves_choice_advance)
        sum_power_tokens_end_act1 += int(ts.power_tokens_end_act1)
        cnt_act1_reached += int(ts.act1_reached)
        sum_power_tokens_end_game += int(ts.power_tokens_end_game)
        cnt_charge_gains += int(ts.charge_gains)
        cnt_furtivite_1_rive_turns += int(ts.furtivite_1_rive_turns)
        cnt_furtivite_2_rives_turns += int(ts.furtivite_2_rives_turns)
        sum_mem_debt += int(ts.mem_debt_score)
        sum_law_mean += float(ts.law_stack_mean)
        max_law_max = max(max_law_max, int(ts.law_stack_max))
        sum_fiddliness += float(ts.fiddliness_ratio)
        sum_physical_ops += int(ts.total_physical_ops)
        sum_player_decisions += int(ts.total_player_decisions)
        sum_cascade_sweeps += int(ts.cascade_sweeps)
        sum_mid_combat += int(ts.mid_combat_interrupts)
        for k in DEFENSE_ATTRIBUTION_FIELDS:
            def_attr_acc[k] += int(getattr(ts, k))
        if ts.rs_count or ts.rf_count:
            for k in REVEIL_ANATOMY_FIELDS:
                reveil_anat_acc[k] += int(getattr(ts, k))

    ratios.sort()
    k20 = max(1, (len(ratios) + 4) // 5)
    p20_idx = min(len(ratios) - 1, max(0, int(0.2 * (len(ratios) - 1))))
    cvar20 = sum(ratios[:k20]) / k20
    wall_sec = time.perf_counter() - t0

    out_row: dict[str, Any] = {
        "campaign": str(unit["campaign"]),
        "config_id": int(unit["config_id"]),
        "n_players": n_pl,
        "chassis_id": ch_id,
        "p_max": p_max_val,
        "variant_idx": int(unit["variant_idx"]),
        "variant_id": str(unit["variant_id"]),
        "reve_activation_mode": reve_activation_mode,
        "gardien_bet_cap_policy": gardien_bet_cap_policy,
        "reve_advance_mode": reve_advance_mode,
        "gardien_4_trigger_mode": gardien_4_trigger_mode,
        "compared_slots_json": json.dumps(unit["compared_slots"], sort_keys=True, ensure_ascii=False),
        "table_id": str(unit["table_id"]),
        "peuples": "-".join(peuples),
        "n_animaux_sauvages": n_animaux,
        "bot": bot_name,
        "k_max": k_max,
        "mode": mode,
        "exp_seed": exp_seed,
        "n_games": n_games,
        "sum_arbres": sum_arbres,
        "sum_ratio_arbres": round(sum_ratio, 6),
        "sum_sq_ratio_arbres": round(sum_sq_ratio, 6),
        "min_ratio_arbres": round(ratios[0], 6),
        "max_ratio_arbres": round(ratios[-1], 6),
        "p10_ratio": round(_quantile_sorted(ratios, 0.10), 6),
        "p20_ratio": round(ratios[p20_idx], 6),
        "p50_ratio": round(_quantile_sorted(ratios, 0.50), 6),
        "p90_ratio": round(_quantile_sorted(ratios, 0.90), 6),
        "cvar20_ratio": round(cvar20, 6),
        "count_arbres_pos": cnt_arbres_pos,
        "sum_tours": sum_tours,
        "count_tour_8": cnt_t8,
        "count_reve_rang_1": cnt_reve,
        "count_reveil_gardiens": cnt_reveil,
        "count_reveil_attempts": cnt_reveil_attempts,
        "count_reveil_failures": cnt_reveil_failures,
        "count_gardien_bets_won": cnt_gardien_bets_won,
        "count_gardien_bets_lost": cnt_gardien_bets_lost,
        "count_bouclier_lisiere_saves": cnt_bouclier_lisiere_saves,
        "count_reves_activated": cnt_reves_activated,
        "count_machines_cancelled_by_reve": cnt_machines_cancelled_by_reve,
        "count_machines_bypassed_inactive_reve": cnt_machines_bypassed_inactive_reve,
        "count_reves_choice_block": cnt_reves_choice_block,
        "count_reves_choice_advance": cnt_reves_choice_advance,
        "sum_power_tokens_end_act1": sum_power_tokens_end_act1,
        "count_act1_reached": cnt_act1_reached,
        "sum_power_tokens_end_game": sum_power_tokens_end_game,
        "count_charge_gains": cnt_charge_gains,
        "count_furtivite_1_rive_turns": cnt_furtivite_1_rive_turns,
        "count_furtivite_2_rives_turns": cnt_furtivite_2_rives_turns,
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
    out_row.update(def_attr_acc)
    out_row.update(reveil_anat_acc)
    return out_row


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
