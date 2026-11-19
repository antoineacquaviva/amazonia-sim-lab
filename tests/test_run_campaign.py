"""Tests unitaires du pipeline bout-en-bout `run_campaign.py` et du worker manifeste."""

from __future__ import annotations

import json
from pathlib import Path

from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from run_campaign import aggregate_campaign_duckdb, publish_to_studio_digests


def _sample_manifest() -> dict[str, object]:
    return {
        "schema_version": "5.3",
        "manifest_type": "campaign_plan",
        "campaign_name": "test_micro_unit",
        "description": "Test unitaire manifeste",
        "player_counts": [3, 4],
        "games_per_configuration": 2,
        "bot": "B0",
        "chassis_plan": {
            "varying_axes": [
                {"key": "P_Max", "label": "P_Max", "values": [4, 5]},
            ],
            "fixed_axes": {
                "Regle_Ouverture_Reve_Multiple": "UNIQUE_PAR_TOUR",
                "Offset_Seuil_Parade": 0,
                "Mise_En_Place_Tactiques": "ORDRE_FIXE_T1_T6",
                "Declenchement_Fin_De_Piste": "ARRIVEE_DERNIERE_PARCELLE",
                "Role_Abatteuse_Fin_De_Piste": "STANDARD_COUPE_ARBRE",
                "Synergie_Binome_Machines": "INDIVIDUELLE",
            },
        },
        "slot_profile_comparisons": {
            "G7": ["A", "B"],
        },
        "base_instance": {
            "bundle_id": "STANDARD_A",
            "peuples_cercle": ["M", "R", "O", "H"],
            "slots_insectes": {
                "SLOT_BUG_CERVEAU": "A",
                "SLOT_COLONISATION_GARDIENS": "A",
            },
        },
    }


def test_resolve_manifest_plan_cartesian_and_totals() -> None:
    plan = resolve_manifest_plan(_sample_manifest())
    assert plan["campaign_name"] == "test_micro_unit"
    assert plan["chassis_ids"] == (0, 1)
    assert plan["total_configurations"] == 2 * 2 * 2  # 2 N * 2 chassis * 2 profils G7
    assert plan["total_games"] == 16
    assert plan["tested_tiles"] == (("G7", "A"), ("G7", "B"))


def test_local_manifest_worker_duckdb_and_studio_index(tmp_path: Path, monkeypatch: object) -> None:
    manifest = _sample_manifest()
    manifest["player_counts"] = [4]
    manifest["chassis_plan"] = {"varying_axes": [], "fixed_axes": {"P_Max": 4}}
    manifest["games_per_configuration"] = 2

    manifest_file = tmp_path / "test_micro_unit.json"
    manifest_file.write_text(json.dumps(manifest), encoding="utf-8")

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(manifest_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0
    assert (shards_dir / "shard_00.jsonl.gz").exists()

    import campaigns.digest_builder as db_mod
    import run_campaign as rc_mod

    digests_dir = tmp_path / "data_digests"
    docs_digests_dir = tmp_path / "docs_digests"
    docs_digests_dir.mkdir(parents=True, exist_ok=True)
    docs_index = docs_digests_dir / "index.json"
    docs_index.write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "digests": [
                    {
                        "id": "palier4_canon",
                        "label": "Palier 4",
                        "file": "digest_palier4_canon.json",
                        "campaign": "palier4_canon",
                        "generated_at_utc": "2026-11-19T05:30:59Z",
                        "total_games": 16195,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    mp = monkeypatch
    assert hasattr(mp, "setattr")
    mp.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)  # type: ignore[attr-defined]
    mp.setattr(rc_mod, "DOCS_DIGESTS_DIR", docs_digests_dir)  # type: ignore[attr-defined]
    mp.setattr(rc_mod, "DOCS_DIGESTS_INDEX", docs_index)  # type: ignore[attr-defined]
    mp.setattr(rc_mod, "ROOT", tmp_path)  # type: ignore[attr-defined]

    plan = resolve_manifest_plan(manifest)
    parquet_path = tmp_path / "cells.parquet"
    digest_path, prompt_path, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        backend="cloudrun",
        job_name="amazonia-campaign",
        tasks=1,
        job_wall_sec=1.5,
    )
    assert digest_path.exists()
    assert prompt_path.exists()
    assert parquet_path.exists()
    assert digest["totals"]["total_games"] == 4
    assert "G7:A" in digest["tile_metrics"]
    assert "G7:B" in digest["tile_metrics"]

    studio_digest, studio_idx = publish_to_studio_digests(
        campaign_name="test_micro_unit",
        digest_path=digest_path,
        digest=digest,
        manifest=manifest,
    )
    assert studio_digest.exists()
    idx_data = json.loads(studio_idx.read_text(encoding="utf-8"))
    assert len(idx_data["digests"]) == 2
    assert idx_data["digests"][0]["id"] == "test_micro_unit"
    assert idx_data["digests"][1]["id"] == "palier4_canon"
