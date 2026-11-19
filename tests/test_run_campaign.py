"""Tests unitaires du pipeline bout-en-bout `run_campaign.py` et du worker manifeste."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

import run_campaign as rc_mod
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from run_campaign import (
    WORKER_IMAGE_HASH_GCS_URI,
    aggregate_campaign_duckdb,
    compute_worker_image_hash,
    ensure_worker_image_up_to_date,
    publish_to_studio_digests,
)


def _sample_manifest() -> dict[str, object]:
    return {
        "schema_version": "5.4",
        "manifest_type": "campaign_plan",
        "campaign_name": "test_micro_unit",
        "description": "Test unitaire manifeste",
        "player_counts": [3, 4],
        "games_per_configuration": 2,
        "bot": "B0",
        "chassis_plan": {
            "varying_axes": [
                {"key": "Profil_Piste", "label": "Profil_Piste", "values": ["P4_2233", "P4_2223"]},
            ],
            "fixed_axes": {
                "Regle_Ouverture_Reve_Multiple": "UNIQUE_PAR_TOUR",
                "Offset_Seuil_Parade": 0,
                "Mise_En_Place_Tactiques": "ORDRE_FIXE_T1_T6",
                "Placement_Initial_Machines": "MEME_PARCELLE_P1",
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


def _create_fake_worker_tree(root: Path) -> None:
    (root / "Dockerfile.worker").write_text("FROM pypy:3.11-slim\n", encoding="utf-8")
    (root / "engine").mkdir(parents=True, exist_ok=True)
    (root / "engine" / "state.py").write_text("STATE_VERSION = 1\n", encoding="utf-8")
    (root / "bots").mkdir(parents=True, exist_ok=True)
    (root / "bots" / "bot_b0.py").write_text("BOT_VERSION = 1\n", encoding="utf-8")
    (root / "campaigns").mkdir(parents=True, exist_ok=True)
    (root / "campaigns" / "worker_main.py").write_text("WORKER_VERSION = 1\n", encoding="utf-8")
    (root / "data").mkdir(parents=True, exist_ok=True)
    (root / "data" / "spec_bundle_v5_4.json").write_text('{"version": "5.4"}\n', encoding="utf-8")


def test_resolve_manifest_plan_cartesian_and_totals() -> None:
    plan = resolve_manifest_plan(_sample_manifest())
    assert plan["campaign_name"] == "test_micro_unit"
    assert plan["chassis_ids"] == (0, 1)
    assert plan["total_configurations"] == 2 * 2 * 2  # 2 N * 2 chassis * 2 profils G7
    assert plan["total_games"] == 16
    assert plan["tested_tiles"] == (("G7", "A"), ("G7", "B"))


def test_local_manifest_worker_duckdb_and_studio_index(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest = _sample_manifest()
    manifest["player_counts"] = [4]
    manifest["chassis_plan"] = {"varying_axes": [], "fixed_axes": {"Profil_Piste": "P4_2233"}}
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

    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "DOCS_DIGESTS_DIR", docs_digests_dir)
    monkeypatch.setattr(rc_mod, "DOCS_DIGESTS_INDEX", docs_index)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

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


def test_compute_worker_image_hash_deterministic_and_sensitive(tmp_path: Path) -> None:
    _create_fake_worker_tree(tmp_path)
    h1 = compute_worker_image_hash(root=tmp_path)
    h2 = compute_worker_image_hash(root=tmp_path)
    assert h1 == h2
    assert len(h1) == 64

    # Les caches Python et les manifestes campaigns/*.json ne doivent pas invalider l'empreinte
    pycache = tmp_path / "engine" / "__pycache__"
    pycache.mkdir(parents=True, exist_ok=True)
    (pycache / "state.cpython-312.pyc").write_bytes(b"\x00\x01\x02")
    (tmp_path / "campaigns" / "nouvelle_campagne.json").write_text('{"campaign_name": "x"}\n', encoding="utf-8")
    assert compute_worker_image_hash(root=tmp_path) == h1

    # Toute modification d'une source embarquée (engine, bots, campaigns/*.py, spec_bundle, Dockerfile) change le hash
    (tmp_path / "engine" / "state.py").write_text("STATE_VERSION = 2\n", encoding="utf-8")
    h3 = compute_worker_image_hash(root=tmp_path)
    assert h3 != h1

    (tmp_path / "data" / "spec_bundle_v5_4.json").write_text('{"version": "5.3.1"}\n', encoding="utf-8")
    h4 = compute_worker_image_hash(root=tmp_path)
    assert h4 != h3

    # Vérification sur le dépôt réel
    repo_hash = compute_worker_image_hash()
    assert len(repo_hash) == 64


def test_ensure_worker_image_auto_builds_when_remote_missing_or_different(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _create_fake_worker_tree(tmp_path)
    expected_hash = compute_worker_image_hash(root=tmp_path)
    gcs_store: dict[str, str] = {}
    commands: list[list[str]] = []

    def fake_run(
        cmd: list[str], *, check: bool = True, capture: bool = False
    ) -> subprocess.CompletedProcess[str]:
        commands.append(cmd)
        if cmd[1:3] == ["storage", "cat"]:
            uri = cmd[3]
            if uri in gcs_store:
                return subprocess.CompletedProcess(cmd, 0, stdout=gcs_store[uri], stderr="")
            return subprocess.CompletedProcess(cmd, 1, stdout="", stderr="NotFound")
        if cmd[1:3] == ["builds", "submit"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="OK\n", stderr="")
        if cmd[1:3] == ["storage", "cp"]:
            src_path = Path(cmd[3])
            dst_uri = cmd[4]
            gcs_store[dst_uri] = src_path.read_text(encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"Commande inattendue : {cmd}")

    monkeypatch.setattr(rc_mod, "_run", fake_run)

    # 1. Fichier distant absent -> build déclenché + écriture empreinte sur GCS
    built = ensure_worker_image_up_to_date("gcloud", root=tmp_path)
    assert built is True
    assert gcs_store[WORKER_IMAGE_HASH_GCS_URI].strip() == expected_hash
    assert any(cmd[1:3] == ["builds", "submit"] for cmd in commands)
    out1 = capsys.readouterr().out
    assert "aucune empreinte distante" in out1

    # 2. Relance sans modification -> build sauté car empreinte identique
    commands.clear()
    built_again = ensure_worker_image_up_to_date("gcloud", root=tmp_path)
    assert built_again is False
    assert not any(cmd[1:3] == ["builds", "submit"] for cmd in commands)
    assert not any(cmd[1:3] == ["storage", "cp"] for cmd in commands)
    out2 = capsys.readouterr().out
    assert "empreinte locale identique à GCS" in out2

    # 3. Modification d'une source -> build déclenché + nouvelle empreinte écrite
    commands.clear()
    (tmp_path / "bots" / "bot_b0.py").write_text("BOT_VERSION = 2\n", encoding="utf-8")
    new_hash = compute_worker_image_hash(root=tmp_path)
    assert new_hash != expected_hash
    built_after_edit = ensure_worker_image_up_to_date("gcloud", root=tmp_path)
    assert built_after_edit is True
    assert gcs_store[WORKER_IMAGE_HASH_GCS_URI].strip() == new_hash
    out3 = capsys.readouterr().out
    assert "sources modifiées" in out3


def test_ensure_worker_image_force_build_and_no_build_flags(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _create_fake_worker_tree(tmp_path)
    local_hash = compute_worker_image_hash(root=tmp_path)
    gcs_store: dict[str, str] = {WORKER_IMAGE_HASH_GCS_URI: f"{local_hash}\n"}
    commands: list[list[str]] = []

    def fake_run(
        cmd: list[str], *, check: bool = True, capture: bool = False
    ) -> subprocess.CompletedProcess[str]:
        commands.append(cmd)
        if cmd[1:3] == ["builds", "submit"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="OK\n", stderr="")
        if cmd[1:3] == ["storage", "cp"]:
            gcs_store[cmd[4]] = Path(cmd[3]).read_text(encoding="utf-8")
            return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")
        raise AssertionError(f"Commande inattendue : {cmd}")

    monkeypatch.setattr(rc_mod, "_run", fake_run)

    # --no-build : saute totalement sans appeler GCS ni Cloud Build
    built_no = ensure_worker_image_up_to_date("gcloud", no_build=True, root=tmp_path)
    assert built_no is False
    assert commands == []
    assert "--no-build" in capsys.readouterr().out

    # --build : force le build même si GCS contient déjà la même empreinte
    built_force = ensure_worker_image_up_to_date("gcloud", force_build=True, root=tmp_path)
    assert built_force is True
    assert any(cmd[1:3] == ["builds", "submit"] for cmd in commands)
    assert gcs_store[WORKER_IMAGE_HASH_GCS_URI].strip() == local_hash
    assert "--build" in capsys.readouterr().out

    # --build et --no-build simultanés : rejetés
    with pytest.raises(ValueError, match="mutuellement exclusives"):
        ensure_worker_image_up_to_date("gcloud", force_build=True, no_build=True, root=tmp_path)

    with pytest.raises(SystemExit):
        rc_mod.main(["campaigns/micro_validation.json", "--build", "--no-build"])


def test_ensure_worker_image_does_not_update_gcs_if_build_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _create_fake_worker_tree(tmp_path)
    gcs_store: dict[str, str] = {WORKER_IMAGE_HASH_GCS_URI: "oldhash\n"}

    def fake_run(
        cmd: list[str], *, check: bool = True, capture: bool = False
    ) -> subprocess.CompletedProcess[str]:
        if cmd[1:3] == ["storage", "cat"]:
            return subprocess.CompletedProcess(cmd, 0, stdout=gcs_store[cmd[3]], stderr="")
        if cmd[1:3] == ["builds", "submit"]:
            raise subprocess.CalledProcessError(1, cmd)
        if cmd[1:3] == ["storage", "cp"]:
            raise AssertionError("Ne doit pas écrire l'empreinte GCS après un build échoué")
        raise AssertionError(f"Commande inattendue : {cmd}")

    monkeypatch.setattr(rc_mod, "_run", fake_run)

    with pytest.raises(subprocess.CalledProcessError):
        ensure_worker_image_up_to_date("gcloud", root=tmp_path)
    assert gcs_store[WORKER_IMAGE_HASH_GCS_URI].strip() == "oldhash"


def test_local_micro_validation_manifest_end_to_end_without_gcs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exécute un micro-run local complet sur campaigns/micro_validation.json sans aucun appel GCS."""
    import campaigns.digest_builder as db_mod

    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "campaigns" / "micro_validation.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(manifest_path),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0
    assert (shards_dir / "shard_00.jsonl.gz").exists()

    digests_dir = tmp_path / "data_digests"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    parquet_path = tmp_path / "cells.parquet"
    digest_path, prompt_path, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        backend="local",
        job_name="local-micro-validation",
        tasks=1,
        job_wall_sec=0.5,
    )
    assert digest_path.exists() and prompt_path.exists() and parquet_path.exists()
    raw_bytes = digest_path.read_bytes()
    assert not raw_bytes.startswith(b"\xef\xbb\xbf")
    assert b"\r\n" not in raw_bytes
    assert len(raw_bytes) < db_mod.MAX_DIGEST_BYTES

    # 1. Règles cœur actives complètes
    core = digest["active_core_rules"]
    assert core["version"] == "5.4.0"
    assert "studio_sha256" in core and len(core["studio_sha256"]) >= 2
    assert len(core["chassis_7_axes"]) == 1
    assert [t["id"] for t in core["tactiques"]] == ["T1", "T2", "T3", "T4", "T5", "T6"]
    assert core["machine_deck_rules"]["sabotage_dilution_permanente"] is True
    sf = core["spec_formelle"]
    assert len(sf["etapes_1_a_6"]) == 6
    for key in (
        "furtivite",
        "chaine_parades_et_pieges",
        "sabotage_par_dilution",
        "apprentissage",
        "fins_5_3",
    ):
        assert isinstance(sf[key], str) and len(sf[key]) > 20

    # 2. Tuiles testées auto-détectées (G7:A et G7:B) + tile_metrics préservé
    assert [(t["slot"], t["profil"]) for t in digest["tested_tiles_rules"]] == [
        ("G7", "A"),
        ("G7", "B"),
    ]
    for entry in digest["tested_tiles_rules"]:
        assert {"slot", "profil", "nom", "famille", "texte"} <= set(entry.keys())
    assert set(digest["tile_metrics"].keys()) == {"G7:A", "G7:B"}

    # 3. Résultats DuckDB complets : quantiles, CVaR_20%, intervalles inter-blocs, telemetry
    assert digest["totals"]["total_games"] == 16
    assert "cvar20_ratio" in digest["totals"]
    assert "table_cvar20_ratio" in digest["totals"]
    q = digest["quantiles"]
    assert {"min_ratio_arbres", "p10_ratio", "p20_ratio", "p50_ratio", "p90_ratio", "max_ratio_arbres"} <= set(q.keys())
    ib = digest["inter_block_intervals"]
    assert ib["global"]["n_blocks"] >= 2
    assert 0.0 <= ib["global"]["ci95_low"] <= ib["global"]["ci95_high"] <= 1.0
    tel = digest["telemetry"]
    assert "mean_mem_debt" in tel and "mean_mid_combat_interrupts" in tel


def test_aggregate_campaign_duckdb_includes_forks_with_seeds(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Vérifie l'inclusion automatique de `forks` avec leurs `seeds` si produits par la campagne."""
    import gzip

    import campaigns.digest_builder as db_mod

    shards_dir = tmp_path / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    row = {
        "campaign": "fork_unit",
        "task_index": 0,
        "task_games": 4,
        "task_wall_sec": 0.2,
        "task_games_per_sec": 20.0,
        "config_id": 0,
        "n_players": 4,
        "chassis_id": 0,
        "p_max": 4,
        "variant_idx": 0,
        "variant_id": "G7:A",
        "compared_slots_json": '{"G7":"A"}',
        "table_id": "M-R-O-H",
        "peuples": "M-R-O-H",
        "bot": "B2",
        "k_max": 3,
        "mode": 3,
        "exp_seed": 20269901,
        "n_games": 4,
        "sum_arbres": 100,
        "sum_ratio_arbres": 2.5,
        "sum_sq_ratio_arbres": 1.6,
        "min_ratio_arbres": 0.5,
        "max_ratio_arbres": 0.75,
        "p10_ratio": 0.5,
        "p20_ratio": 0.55,
        "p50_ratio": 0.625,
        "p90_ratio": 0.75,
        "cvar20_ratio": 0.5,
        "count_arbres_pos": 4,
        "sum_tours": 24,
        "count_tour_8": 2,
        "count_reve_rang_1": 0,
        "count_reveil_gardiens": 2,
        "sum_mem_debt": 200,
        "sum_law_mean": 1.0,
        "max_law_max": 2,
        "sum_fiddliness": 10.0,
        "sum_physical_ops": 120,
        "sum_player_decisions": 40,
        "sum_cascade_sweeps": 12,
        "sum_mid_combat": 4,
        "fork_anchors": 6,
        "fork_anchors_missed": 1,
        "fork_diverged": 4,
    }
    with gzip.open(shards_dir / "shard_00.jsonl.gz", "wt", encoding="utf-8") as fh:
        fh.write(json.dumps(row) + "\n")

    manifest = _sample_manifest()
    manifest["campaign_name"] = "fork_unit"
    plan = resolve_manifest_plan(manifest)

    digests_dir = tmp_path / "data_digests"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    _, _, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="local",
        job_name="local-fork-unit",
        tasks=1,
        job_wall_sec=0.2,
    )
    assert "forks" in digest
    assert digest["forks"]["fork_anchors"] == 6
    assert digest["forks"]["fork_anchors_missed"] == 1
    assert digest["forks"]["fork_diverged"] == 4
    assert digest["forks"]["seeds"] == [20269901]

