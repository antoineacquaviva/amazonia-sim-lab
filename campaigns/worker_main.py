"""Worker Cloud PyPy 3.11 stdlib pure pour amazonia-sim-lab (Socle v6.1 & Mode 4)."""

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
from bots.bot_b3_rh import play_game_b3
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.designs import (
    balanced_neighbor_mirror_tables,
    mirror_peuples,
    run_v6_1_causal_forks_on_config,
)
from campaigns.digest_builder import (
    build_mobile_one_tap_html,
    build_prompt_gemini_markdown,
    build_self_contained_digest,
)
from engine.core_engine import ensure_builtin_migration_registered
from engine.effects.registry import list_registered_tiles
from engine.primitives import CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS, CAUSE_TOUR_8
from engine.state import (
    ANIMAUX_SAUVAGES,
    CANONICAL_P_MAX,
    CANONICAL_PROFIL_PISTE,
    PEUPLES_ONIRIQUES,
    PEUPLES_ORDER,
    STATE_BUF_SIZE,
    GameConfig,
    GameState,
)
from engine.telemetry import (
    DEFENSE_ATTRIBUTION_FIELDS,
    DILEMMA_CHOICE_FIELDS,
    OCKHAM_COUNT_FIELDS,
    REVEIL_ANATOMY_FIELDS,
    TelemetryTracker,
)

# Catalogue actif Mode 4 : 30 tuiles asymétriques (G1..G15, R1..R10, M1..M5) + 2 slots de migration
CANONICAL_32_SLOTS: tuple[str, ...] = (
    *(f"G{i}" for i in range(1, 16)),
    *(f"R{i}" for i in range(1, 11)),
    *(f"M{i}" for i in range(1, 6)),
    "SLOT_BUG_CERVEAU",
    "SLOT_COLONISATION_GARDIENS",
)
CANONICAL_32_SLOTS_SET: frozenset[str] = frozenset(CANONICAL_32_SLOTS)
NATIVE_MIGRATION_SLOTS: frozenset[str] = frozenset(
    {"SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"}
)
NEUTRAL_TILE_PROFILE: str = "NEUTRE"

ALLOWED_MANIFEST_KEYS: frozenset[str] = frozenset(
    {
        "schema_version",
        "manifest_type",
        "campaign_name",
        "target_path",
        "description",
        "campaign_kind",
        "micro_forks",
        "fork_selection_rollouts",
        "fork_eval_rollouts",
        "mode",
        "bot",
        "bots",
        "k_max",
        "seed",
        "player_counts",
        "table_selection",
        "min_animaux_sauvages",
        "games_per_configuration",
        "include_full_tile_metrics",
        "include_v6_audit_blocks",
        "base_instance",
        "slot_profile_comparisons",
    }
)
ALLOWED_BASE_INSTANCE_KEYS: frozenset[str] = frozenset(
    {"bundle_id", "peuples_cercle", "profile_overrides"}
)
ALLOWED_TABLE_SELECTIONS: frozenset[str] = frozenset(
    {"DEFAULT", "ALL_PEUPLE_COMBOS", "BALANCED_CIRCLES"}
)
ALLOWED_CAMPAIGN_KINDS: frozenset[str] = frozenset({"MACRO", "MICRO_FORKS"})
ALLOWED_BUNDLE_IDS: frozenset[str] = frozenset({"STANDARD_A"})

METADATA_TOKEN_URL: str = (
    "http://metadata.google.internal/computeMetadata/v1/"
    "instance/service-accounts/default/token"
)
BUCKET_NAME: str = "amazonia-sim-runs"
SMOKE_OBJECT_NAME: str = "smoke/shard_00.jsonl.gz"
MOBILE_LATEST_OBJECT: str = "mobile/latest.html"

DEFAULT_TABLES_BY_N: dict[int, tuple[tuple[str, tuple[str, ...]], ...]] = {
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


def _sanitize_slug(raw: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9_-]+", "_", raw.strip().lower()).strip("_")
    return cleaned or "campagne_v6_1"


def _validate_tile_profile_executable(
    slot_id: str,
    profile: str,
    *,
    mode: int,
    registered_tiles: frozenset[tuple[str, str]],
) -> tuple[str, str]:
    """Vérifie qu'un couple `(slot_id, profile)` est exécutable dans le moteur (registre ou migration native)."""
    s_norm = str(slot_id).strip()
    p_norm = str(profile).strip().upper()
    if s_norm not in CANONICAL_32_SLOTS_SET:
        raise ValueError(
            f"Emplacement de tuile inconnu dans le manifeste : {slot_id!r} "
            "(attendu G1..G15, R1..R10, M1..M5, SLOT_BUG_CERVEAU ou SLOT_COLONISATION_GARDIENS)"
        )
    if not p_norm:
        raise ValueError(f"Profil vide interdit pour l'emplacement {s_norm!r}")
    if p_norm == NEUTRAL_TILE_PROFILE:
        return s_norm, p_norm
    if s_norm in NATIVE_MIGRATION_SLOTS:
        if (s_norm, p_norm) not in registered_tiles:
            raise ValueError(
                f"Profil de migration non implémenté dans le moteur : {s_norm}:{p_norm} "
                "(seuls 'B' et 'NEUTRE' sont exécutables en v6.1)"
            )
        return s_norm, p_norm
    if mode < 3:
        raise ValueError(
            f"Profil de tuile {s_norm}:{p_norm} demandé en mode={mode} : "
            "les effets de tuiles G/R/M ne s'exécutent qu'en Mode 3 ou 4."
        )
    if (s_norm, p_norm) not in registered_tiles:
        raise ValueError(
            f"Profil de tuile non enregistré dans le moteur : {s_norm}:{p_norm} "
            "(aucun gestionnaire @register_tile actif)"
        )
    return s_norm, p_norm


def resolve_manifest_plan(manifest: dict[str, Any]) -> dict[str, Any]:
    """Valide strictement et résout un manifeste JSON `campaigns/<nom>.json` en plan déterministe v6.1."""
    if not isinstance(manifest, dict):
        raise TypeError("Le manifeste de campagne doit être un objet JSON.")

    unknown_keys = sorted(str(k) for k in manifest if str(k) not in ALLOWED_MANIFEST_KEYS)
    if unknown_keys:
        raise ValueError(
            f"Clé(s) ou axe(s) inconnu(s)/obsolète(s) dans le manifeste : {unknown_keys}"
        )

    if "mode" not in manifest:
        raise ValueError(
            "Champ obligatoire 'mode' absent du manifeste (attendu 1, 2, 3 ou 4, aligné sur GameConfig)."
        )
    mode = int(manifest["mode"])
    if mode not in (1, 2, 3, 4):
        raise ValueError(f"mode invalide (attendu 1..4) : {mode}")

    default_cfg = GameConfig(mode=mode)

    campaign_name = _sanitize_slug(str(manifest.get("campaign_name", "campagne_v6_1")))
    raw_players = manifest.get("player_counts", [default_cfg.n_players])
    if not isinstance(raw_players, (list, tuple)) or not raw_players:
        raise ValueError(f"player_counts invalide (attendu liste non vide dans 3..6) : {raw_players!r}")
    player_counts = sorted({int(n) for n in raw_players})
    if any(n not in (3, 4, 5, 6) for n in player_counts):
        raise ValueError(f"player_counts invalide (attendu 3..6) : {player_counts}")

    games_per_cfg = int(manifest.get("games_per_configuration", 1))
    if games_per_cfg < 1:
        raise ValueError(f"games_per_configuration doit être >= 1 (reçu {games_per_cfg})")

    if "bot" in manifest and "bots" in manifest:
        raise ValueError("Spécifier soit 'bot', soit 'bots', mais pas les deux simultanément.")
    raw_bots = manifest.get("bots")
    if raw_bots is not None:
        if isinstance(raw_bots, str):
            bot_list = [raw_bots.strip().upper()]
        elif isinstance(raw_bots, (list, tuple)):
            bot_list = [str(b).strip().upper() for b in raw_bots]
        else:
            raise ValueError(f"Format invalide pour 'bots' : {raw_bots!r}")
    else:
        bot_list = [str(manifest.get("bot", "B2")).strip().upper()]
    bot_list = list(dict.fromkeys(bot_list))
    if not bot_list or any(b not in ("B0", "B1", "B2", "B3") for b in bot_list):
        raise ValueError(
            f"Bot(s) non supporté(s) dans le manifeste : {bot_list!r} (attendu B0/B1/B2/B3)"
        )
    bot_name = bot_list[0]

    has_explicit_k_max = "k_max" in manifest
    if has_explicit_k_max:
        explicit_k_max = int(manifest["k_max"])
        if not (0 <= explicit_k_max <= 4):
            raise ValueError(f"k_max invalide (attendu 0..4) : {explicit_k_max}")
    else:
        explicit_k_max = default_cfg.max_revision_passes
    k_max_default = 0 if bot_name == "B0" else explicit_k_max

    exp_seed = int(manifest.get("seed", 20261201))
    include_full_tile_metrics = bool(manifest.get("include_full_tile_metrics", False))

    campaign_kind = str(manifest.get("campaign_kind", "MACRO")).strip().upper()
    if campaign_kind not in ALLOWED_CAMPAIGN_KINDS:
        raise ValueError(
            f"campaign_kind invalide : {campaign_kind!r} (attendu {sorted(ALLOWED_CAMPAIGN_KINDS)})"
        )
    is_micro_forks = bool(manifest.get("micro_forks", False)) or (campaign_kind == "MICRO_FORKS")
    fork_n_sel = int(manifest.get("fork_selection_rollouts", 3))
    fork_n_eval = int(manifest.get("fork_eval_rollouts", 4))
    if fork_n_sel < 1 or fork_n_eval < 2:
        raise ValueError(
            f"Rollouts de micro-forks invalides : selection={fork_n_sel} (>=1), eval={fork_n_eval} (>=2)"
        )

    # Registre réel des effets exécutables (30 tuiles Mode 4 + 2 migrations natives)
    ensure_builtin_migration_registered()
    registered_tiles: frozenset[tuple[str, str]] = frozenset(list_registered_tiles())

    # 1. Validation & résolution du génome de base Mode 4
    base_inst_raw = manifest.get("base_instance", {})
    if not isinstance(base_inst_raw, dict):
        raise TypeError("base_instance doit être un objet JSON.")
    unknown_base_keys = sorted(
        str(k) for k in base_inst_raw if str(k) not in ALLOWED_BASE_INSTANCE_KEYS
    )
    if unknown_base_keys:
        raise ValueError(f"Clé(s) inconnue(s) dans base_instance : {unknown_base_keys}")

    bundle_id = str(base_inst_raw.get("bundle_id", "STANDARD_A")).strip().upper()
    if bundle_id not in ALLOWED_BUNDLE_IDS:
        raise ValueError(
            f"base_instance.bundle_id invalide : {bundle_id!r} (attendu {sorted(ALLOWED_BUNDLE_IDS)})"
        )
    base_map: dict[str, str] = {slot_id: "A" for slot_id in CANONICAL_32_SLOTS}
    base_map["SLOT_BUG_CERVEAU"] = "B"
    base_map["SLOT_COLONISATION_GARDIENS"] = "B"

    raw_overrides = base_inst_raw.get("profile_overrides", {})
    if not isinstance(raw_overrides, dict):
        raise TypeError("base_instance.profile_overrides doit être un objet JSON.")
    for slot_id, prof in raw_overrides.items():
        s_ok, p_ok = _validate_tile_profile_executable(
            str(slot_id), str(prof), mode=mode, registered_tiles=registered_tiles
        )
        base_map[s_ok] = p_ok

    # 2. Validation & résolution des variantes de profils comparés (slot_profile_comparisons)
    raw_comps = manifest.get("slot_profile_comparisons", {})
    if not isinstance(raw_comps, dict):
        raise TypeError("slot_profile_comparisons doit être un objet JSON.")
    validated_comps: dict[str, list[str]] = {}
    for raw_slot, raw_profs in raw_comps.items():
        slot_s = str(raw_slot).strip()
        if slot_s not in CANONICAL_32_SLOTS_SET:
            raise ValueError(
                f"Emplacement inconnu dans slot_profile_comparisons : {raw_slot!r}"
            )
        if not isinstance(raw_profs, (list, tuple)) or not raw_profs:
            raise ValueError(
                f"Liste de profils vide ou invalide pour {slot_s!r} dans slot_profile_comparisons."
            )
        prof_list: list[str] = []
        for p_item in raw_profs:
            _, p_ok = _validate_tile_profile_executable(
                slot_s, str(p_item), mode=mode, registered_tiles=registered_tiles
            )
            if p_ok not in prof_list:
                prof_list.append(p_ok)
        validated_comps[slot_s] = prof_list

    ordered_comp_slots = [s for s in CANONICAL_32_SLOTS if s in validated_comps]
    comp_lists = [validated_comps[s] for s in ordered_comp_slots]

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
            for s in CANONICAL_32_SLOTS[:30]:
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
        if mode >= 3:
            for s in CANONICAL_32_SLOTS[:30]:
                if base_map[s] != "A":
                    tested_tiles_set.append((s, base_map[s]))

    # 3. Construction des unités de calcul (cercles de voisinage équilibrés en paires miroirs CRN)
    base_peuples_raw = base_inst_raw.get("peuples_cercle", [])
    if not isinstance(base_peuples_raw, (list, tuple)):
        raise TypeError("base_instance.peuples_cercle doit être une liste de codes Peuples.")
    base_peuples: tuple[str, ...] = tuple(str(p).strip().upper() for p in base_peuples_raw)
    if base_peuples:
        if len(base_peuples) not in (3, 4, 5, 6) or len(set(base_peuples)) != len(base_peuples):
            raise ValueError(f"base_instance.peuples_cercle invalide : {base_peuples!r}")
        if any(p not in PEUPLES_ORDER for p in base_peuples):
            raise ValueError(f"Peuple inconnu dans base_instance.peuples_cercle : {base_peuples!r}")

    table_selection = str(manifest.get("table_selection", "BALANCED_CIRCLES")).strip().upper()
    if table_selection not in ALLOWED_TABLE_SELECTIONS:
        raise ValueError(
            f"table_selection invalide : {table_selection!r} "
            f"(attendu {sorted(ALLOWED_TABLE_SELECTIONS)})"
        )
    min_animaux = int(manifest.get("min_animaux_sauvages", 0))
    if not (0 <= min_animaux <= 3):
        raise ValueError(f"min_animaux_sauvages invalide (attendu 0..3) : {min_animaux}")

    units: list[dict[str, Any]] = []
    config_idx = 0
    for b_name in bot_list:
        b_k_max = 0 if b_name == "B0" else explicit_k_max
        for n_pl in player_counts:
            if len(base_peuples) == n_pl:
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
            elif table_selection in ("ALL_PEUPLE_COMBOS", "BALANCED_CIRCLES"):
                candidate_tables = balanced_neighbor_mirror_tables(
                    n_pl,
                    min_animaux_sauvages=min_animaux,
                    max_tables=games_per_cfg,
                    exp_seed=exp_seed,
                )
            else:
                # DEFAULT : sous-ensemble compact de paires miroirs équilibrées (sans biais M/R ni ordre fixe)
                candidate_tables = balanced_neighbor_mirror_tables(
                    n_pl,
                    min_animaux_sauvages=min_animaux,
                    max_tables=min(games_per_cfg, 10),
                    exp_seed=exp_seed,
                )

            if not candidate_tables:
                raise ValueError(
                    f"Aucune table légale pour n_players={n_pl} et min_animaux_sauvages={min_animaux}"
                )

            n_tables = len(candidate_tables)
            base_per_tbl = games_per_cfg // n_tables
            rem_tbl = games_per_cfg % n_tables

            table_groups: list[tuple[bool, tuple[tuple[int, str, tuple[str, ...]], ...]]] = []
            idx_t = 0
            while idx_t < n_tables:
                t_id_a, p_a = candidate_tables[idx_t]
                if (
                    idx_t + 1 < n_tables
                    and mirror_peuples(p_a) == candidate_tables[idx_t + 1][1]
                ):
                    t_id_b, p_b = candidate_tables[idx_t + 1]
                    table_groups.append(
                        (True, ((idx_t, t_id_a, p_a), (idx_t + 1, t_id_b, p_b)))
                    )
                    idx_t += 2
                else:
                    table_groups.append((False, ((idx_t, t_id_a, p_a),)))
                    idx_t += 1

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
                                "n_machines_initial": 2 * n_pl,
                                "profil_piste": CANONICAL_PROFIL_PISTE,
                                "variant_idx": var["variant_idx"],
                                "variant_id": var["variant_id"],
                                "compared_slots": var["compared_slots"],
                                "tile_profiles": var["tile_profiles"],
                                "micro_forks": is_micro_forks,
                                "fork_selection_rollouts": fork_n_sel,
                                "fork_eval_rollouts": fork_n_eval,
                                "table_id": t_id,
                                "peuples": peuples,
                                "n_animaux_sauvages": sum(
                                    1 for p in peuples if p in ANIMAUX_SAUVAGES
                                ),
                                "has_insectes": 1 if "I" in peuples else 0,
                                "n_peuples_oniriques": sum(
                                    1 for p in peuples if p in PEUPLES_ONIRIQUES
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
        "profil_piste": CANONICAL_PROFIL_PISTE,
        "base_bundle_id": bundle_id,
        "base_tile_profiles": dict(base_map),
        "resolved_32_slots_sha256": resolved_32_slots_sha256,
        "profile_variants": profile_variants,
        "tested_tiles": tuple(tested_tiles_set),
        "varying_tiles": tuple(varying_tiles_set),
        "include_full_tile_metrics": include_full_tile_metrics,
        "micro_forks": is_micro_forks,
        "table_selection": table_selection,
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
    mode = int(unit["mode"])
    peuples = tuple(unit["peuples"])
    tile_profiles = tuple((str(s), str(p)) for s, p in unit["tile_profiles"])
    is_micro_forks = bool(unit.get("micro_forks", False))
    fork_n_sel = int(unit.get("fork_selection_rollouts", 3))
    fork_n_eval = int(unit.get("fork_eval_rollouts", 4))
    n_animaux = int(
        unit.get("n_animaux_sauvages", sum(1 for p in peuples if p in ANIMAUX_SAUVAGES))
    )
    has_insectes = int(unit.get("has_insectes", 1 if "I" in peuples else 0))
    n_oniriques = int(
        unit.get("n_peuples_oniriques", sum(1 for p in peuples if p in PEUPLES_ONIRIQUES))
    )
    bot_name = str(unit["bot"])
    k_max = int(unit["k_max"])
    exp_seed = int(unit["exp_seed"])
    rep_start = int(unit["rep_start"])
    n_games = int(unit["n_games"])

    ratios: list[float] = []
    ratio_bp_counts: dict[str, int] = {}
    sum_arbres = 0
    sum_ratio = 0.0
    sum_sq_ratio = 0.0
    sum_tours = 0
    cnt_t8 = 0
    cnt_reve = 0
    cnt_reveil = 0
    sommeil_by_t = [0] * 9
    sum_sommeil_tours = 0
    sum_sommeil_ratio = 0.0
    cnt_reveil_attempts = 0
    cnt_reveil_failures = 0
    cnt_gardien_bets_won = 0
    cnt_gardien_bets_lost = 0
    cnt_bouclier_lisiere_saves = 0
    cnt_reves_activated = 0
    cnt_machines_cancelled_by_reve = 0
    cnt_machines_bypassed_inactive_reve = 0
    sum_power_tokens_end_act1 = 0
    cnt_act1_reached = 0
    sum_power_tokens_end_game = 0
    cnt_charge_gains = 0
    cnt_charge_gains_act1 = 0
    cnt_charge_gains_act2 = 0
    cnt_furtivite_1_rive_turns = 0
    cnt_arbres_pos = 0

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
    ok_sum_acc: dict[str, int] = {f"sum_{k}": 0 for k in OCKHAM_COUNT_FIELDS}
    ok_games_acc: dict[str, int] = {f"games_{k}": 0 for k in OCKHAM_COUNT_FIELDS}
    dil_sum_acc: dict[str, int] = {f"sum_{k}": 0 for k in DILEMMA_CHOICE_FIELDS}

    fork_anchors = 0
    fork_anchors_missed = 0
    fork_diverged = 0
    sum_delta_v_neg = 0.0
    sum_sq_delta_v_neg = 0.0
    sum_c_prive = 0.0
    sum_sq_c_prive = 0.0
    sum_g_naive = 0.0
    sum_g_unbiased = 0.0
    sum_rho_delta = 0.0
    fork_2_1_anchors = 0
    sum_delta_v_2_1_b2_vs_b0 = 0.0
    sum_sq_delta_v_2_1_b2_vs_b0 = 0.0
    fork_2_1_reve_anchors = 0
    sum_delta_v_2_1_reve = 0.0
    sum_sq_delta_v_2_1_reve = 0.0
    fork_furt_rp_anchors = 0
    sum_delta_v_furt_rp = 0.0
    sum_sq_delta_v_furt_rp = 0.0
    fork_furt_rs_anchors = 0
    sum_delta_v_furt_rs = 0.0
    sum_sq_delta_v_furt_rs = 0.0
    fork_4_1_piege_anchors = 0
    sum_delta_v_4_1_piege = 0.0
    sum_sq_delta_v_4_1_piege = 0.0
    fork_eveil_anchors = 0
    sum_delta_v_eveil_vs_survival = 0.0
    sum_sq_delta_v_eveil_vs_survival = 0.0

    for i in range(n_games):
        rep_id = rep_start + i
        cfg = GameConfig(
            n_players=n_pl,
            mode=mode,
            peuples=peuples,
            exp_seed=exp_seed,
            rep_id=rep_id,
            coordonnateur_initial=rep_id % n_pl,
            max_revision_passes=k_max,
            tile_profiles=tile_profiles if mode >= 3 else (),
        )

        if is_micro_forks:
            anchor_tour = 2 if (i % 2 == 0) else 3
            cf = run_v6_1_causal_forks_on_config(
                cfg,
                target_tour=anchor_tour,
                is_b2=(bot_name != "B1"),
                n_selection_rollouts=fork_n_sel,
                n_eval_rollouts=fork_n_eval,
                k_max_future=max(1, k_max),
            )
            if cf.mf_2_2 is None:
                fork_anchors_missed += 1
            else:
                fork_anchors += 1
                if cf.mf_2_2.diverged_in_2_2:
                    fork_diverged += 1
                sum_delta_v_neg += cf.mf_2_2.delta_v_negociation
                sum_sq_delta_v_neg += cf.mf_2_2.delta_v_negociation ** 2
                sum_c_prive += cf.mf_2_2.c_prive
                sum_sq_c_prive += cf.mf_2_2.c_prive ** 2
                sum_g_naive += cf.mf_2_2.g_naive_selection
                sum_g_unbiased += cf.mf_2_2.g_unbiased_eval
                sum_rho_delta += cf.mf_2_2.rho_delta
            if cf.has_2_1_anchor:
                fork_2_1_anchors += 1
                sum_delta_v_2_1_b2_vs_b0 += cf.delta_v_2_1_b2_vs_b0
                sum_sq_delta_v_2_1_b2_vs_b0 += cf.delta_v_2_1_b2_vs_b0 ** 2
            if cf.has_2_1_reve_fork:
                fork_2_1_reve_anchors += 1
                sum_delta_v_2_1_reve += cf.delta_v_2_1_reve
                sum_sq_delta_v_2_1_reve += cf.delta_v_2_1_reve ** 2
            if cf.has_furt_rive_piege_fork:
                fork_furt_rp_anchors += 1
                sum_delta_v_furt_rp += cf.delta_v_furt_rive_piege
                sum_sq_delta_v_furt_rp += cf.delta_v_furt_rive_piege ** 2
            if cf.has_furt_rive_sabotage_fork:
                fork_furt_rs_anchors += 1
                sum_delta_v_furt_rs += cf.delta_v_furt_rive_sabotage
                sum_sq_delta_v_furt_rs += cf.delta_v_furt_rive_sabotage ** 2
            if cf.has_4_1_piege_fork:
                fork_4_1_piege_anchors += 1
                sum_delta_v_4_1_piege += cf.delta_v_4_1_pose_piege
                sum_sq_delta_v_4_1_piege += cf.delta_v_4_1_pose_piege ** 2
            if cf.has_eveil_fork:
                fork_eveil_anchors += 1
                sum_delta_v_eveil_vs_survival += cf.delta_v_eveil_vs_survival
                sum_sq_delta_v_eveil_vs_survival += cf.delta_v_eveil_vs_survival ** 2

        trk = TelemetryTracker()
        st = GameState(cfg)
        if bot_name == "B0":
            res = play_game_b0(st, max_steps=2000, telemetry=trk)
        elif bot_name == "B1":
            res = play_game_b1(st, k_max_passes=k_max, max_steps=2000, telemetry=trk)
        elif bot_name == "B3":
            res = play_game_b3(st, k_max_passes=max(1, k_max), max_steps=2000, telemetry=trk)
        else:
            res = play_game_b2(st, k_max_passes=k_max, max_steps=2000, telemetry=trk)

        rt = float(res.ratio_arbres)
        tf = int(res.tour_fin)
        ratios.append(rt)
        bp_key = str(round(rt * 10000))
        ratio_bp_counts[bp_key] = ratio_bp_counts.get(bp_key, 0) + 1
        sum_arbres += int(res.score_arbres)
        sum_ratio += rt
        sum_sq_ratio += rt * rt
        sum_tours += tf
        if res.score_arbres > 0:
            cnt_arbres_pos += 1
        if res.cause_fin == CAUSE_TOUR_8:
            cnt_t8 += 1
        elif res.cause_fin == CAUSE_REVE_RANG_1:
            cnt_reve += 1
            sum_sommeil_tours += tf
            sum_sommeil_ratio += rt
            if 1 <= tf <= 8:
                sommeil_by_t[tf] += 1
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
        sum_power_tokens_end_act1 += int(ts.power_tokens_end_act1)
        cnt_act1_reached += int(ts.act1_reached)
        sum_power_tokens_end_game += int(ts.power_tokens_end_game)
        cnt_charge_gains += int(ts.charge_gains)
        cnt_charge_gains_act1 += int(ts.charge_gains_act1)
        cnt_charge_gains_act2 += int(ts.charge_gains_act2)
        cnt_furtivite_1_rive_turns += int(ts.furtivite_1_rive_turns)
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
        for k in OCKHAM_COUNT_FIELDS:
            v_ok = int(getattr(ts, k))
            if v_ok > 0:
                ok_sum_acc[f"sum_{k}"] += v_ok
                ok_games_acc[f"games_{k}"] += 1
        for k in DILEMMA_CHOICE_FIELDS:
            v_dl = int(getattr(ts, k))
            if v_dl > 0:
                dil_sum_acc[f"sum_{k}"] += v_dl
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
        "n_machines_initial": 2 * n_pl,
        "profil_piste": CANONICAL_PROFIL_PISTE,
        "p_max": CANONICAL_P_MAX,
        "variant_idx": int(unit["variant_idx"]),
        "variant_id": str(unit["variant_id"]),
        "compared_slots_json": json.dumps(unit["compared_slots"], sort_keys=True, ensure_ascii=False),
        "ratio_bp_counts_json": json.dumps(ratio_bp_counts, sort_keys=True),
        "table_id": str(unit["table_id"]),
        "peuples": "-".join(peuples),
        "n_animaux_sauvages": n_animaux,
        "has_insectes": has_insectes,
        "n_peuples_oniriques": n_oniriques,
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
        "sum_sommeil_tours": sum_sommeil_tours,
        "sum_sommeil_ratio_arbres": round(sum_sommeil_ratio, 6),
        "sommeil_t1": sommeil_by_t[1],
        "sommeil_t2": sommeil_by_t[2],
        "sommeil_t3": sommeil_by_t[3],
        "sommeil_t4": sommeil_by_t[4],
        "sommeil_t5": sommeil_by_t[5],
        "sommeil_t6": sommeil_by_t[6],
        "sommeil_t7": sommeil_by_t[7],
        "count_reveil_attempts": cnt_reveil_attempts,
        "count_reveil_failures": cnt_reveil_failures,
        "count_gardien_bets_won": cnt_gardien_bets_won,
        "count_gardien_bets_lost": cnt_gardien_bets_lost,
        "count_bouclier_lisiere_saves": cnt_bouclier_lisiere_saves,
        "count_reves_activated": cnt_reves_activated,
        "count_machines_cancelled_by_reve": cnt_machines_cancelled_by_reve,
        "count_machines_bypassed_inactive_reve": cnt_machines_bypassed_inactive_reve,
        "sum_power_tokens_end_act1": sum_power_tokens_end_act1,
        "count_act1_reached": cnt_act1_reached,
        "sum_power_tokens_end_game": sum_power_tokens_end_game,
        "count_charge_gains": cnt_charge_gains,
        "count_charge_gains_act1": cnt_charge_gains_act1,
        "count_charge_gains_act2": cnt_charge_gains_act2,
        "count_furtivite_1_rive_turns": cnt_furtivite_1_rive_turns,
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
    if is_micro_forks:
        out_row.update(
            {
                "fork_anchors": fork_anchors,
                "fork_anchors_missed": fork_anchors_missed,
                "fork_diverged": fork_diverged,
                "sum_delta_v_neg": round(sum_delta_v_neg, 6),
                "sum_sq_delta_v_neg": round(sum_sq_delta_v_neg, 6),
                "sum_c_prive": round(sum_c_prive, 6),
                "sum_sq_c_prive": round(sum_sq_c_prive, 6),
                "sum_g_naive": round(sum_g_naive, 6),
                "sum_g_unbiased": round(sum_g_unbiased, 6),
                "sum_rho_delta": round(sum_rho_delta, 6),
                "fork_2_1_anchors": fork_2_1_anchors,
                "sum_delta_v_2_1_b2_vs_b0": round(sum_delta_v_2_1_b2_vs_b0, 6),
                "sum_sq_delta_v_2_1_b2_vs_b0": round(sum_sq_delta_v_2_1_b2_vs_b0, 6),
                "fork_2_1_reve_anchors": fork_2_1_reve_anchors,
                "sum_delta_v_2_1_reve": round(sum_delta_v_2_1_reve, 6),
                "sum_sq_delta_v_2_1_reve": round(sum_sq_delta_v_2_1_reve, 6),
                "fork_furt_rp_anchors": fork_furt_rp_anchors,
                "sum_delta_v_furt_rp": round(sum_delta_v_furt_rp, 6),
                "sum_sq_delta_v_furt_rp": round(sum_sq_delta_v_furt_rp, 6),
                "fork_furt_rs_anchors": fork_furt_rs_anchors,
                "sum_delta_v_furt_rs": round(sum_delta_v_furt_rs, 6),
                "sum_sq_delta_v_furt_rs": round(sum_sq_delta_v_furt_rs, 6),
                "fork_4_1_piege_anchors": fork_4_1_piege_anchors,
                "sum_delta_v_4_1_piege": round(sum_delta_v_4_1_piege, 6),
                "sum_sq_delta_v_4_1_piege": round(sum_sq_delta_v_4_1_piege, 6),
                "fork_eveil_anchors": fork_eveil_anchors,
                "sum_delta_v_eveil_vs_survival": round(sum_delta_v_eveil_vs_survival, 6),
                "sum_sq_delta_v_eveil_vs_survival": round(sum_sq_delta_v_eveil_vs_survival, 6),
            }
        )
    out_row.update(def_attr_acc)
    out_row.update(ok_sum_acc)
    out_row.update(ok_games_acc)
    out_row.update(dil_sum_acc)
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
        if t_idx == 0:
            _upload_worker_mobile_latest_html(
                campaign_name,
                records,
                tested_tiles=tuple(plan["tested_tiles"]),
                token=token,
            )
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
    parser = argparse.ArgumentParser(description="Amazonia Sim Lab PyPy Worker (Socle v6.1 & Mode 4)")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Exécute le smoke-test JIT PyPy -> GCS.",
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
    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
