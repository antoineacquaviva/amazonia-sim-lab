"""Tests unitaires du constructeur de bilans auto-portants et du pont Gemini Mobile & PC."""

from __future__ import annotations

import json
from pathlib import Path

from campaigns.digest_builder import (
    DEFAULT_DIGESTS_DIR,
    GEMINI_EDITORIAL_HEADER,
    MAX_DIGEST_BYTES,
    build_active_core_rules,
    build_mobile_one_tap_html,
    build_prompt_gemini_markdown,
    build_self_contained_digest,
    build_tested_tiles_rules,
    decode_chassis_axes,
    write_digest_and_prompt_files,
)
from scripts_cloud.publish_digest import (
    GCLOUD_DRIVE_AUTH_CMD,
    publish_campaign_digest,
    render_ascii_qr,
    upload_prompt_to_google_drive,
)


def test_decode_chassis_axes_and_active_core_rules() -> None:
    c0 = decode_chassis_axes(0)
    assert c0["chassis_id"] == 0
    assert c0["profil_piste"] == "P4_2233"
    assert c0["regle_ouverture_reve_multiple"] == "UNIQUE_PAR_TOUR"
    assert c0["offset_seuil_parade"] == 0
    assert c0["placement_initial_machines"] == "MEME_PARCELLE_P1"

    c383 = decode_chassis_axes(383)
    assert c383["chassis_id"] == 383
    assert c383["profil_piste"] == "P5_12223"
    assert c383["placement_initial_machines"] == "BULLDOZER_P1_ABATTEUSE_P2"
    assert c383["synergie_binome_machines"] == "MUTUALISATION_PUISSANCE_MEME_PARCELLE"

    core = build_active_core_rules((0, 1, 383))
    assert core["version"] == "5.4.0"
    assert "catalog_v5_4.json" in core["studio_sha256"]
    assert "spec_formelle_v5_4.json" in core["studio_sha256"]
    assert len(core["chassis_7_axes"]) == 3
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


def test_build_tested_tiles_rules() -> None:
    tiles = build_tested_tiles_rules([("G1", "A"), "R5:A", ("G9", "C"), "G1:A"])
    assert len(tiles) == 3  # dédupliqué tout en préservant l'ordre
    assert tiles[0]["slot"] == "G1"
    assert tiles[0]["profil"] == "A"
    assert tiles[0]["famille"] == "GARDIEN"
    assert "Surchauffe" in tiles[0]["texte"]
    assert tiles[1]["slot"] == "R5"
    assert tiles[1]["famille"] == "REVE"


def test_palier1_and_palier2_digests_are_self_contained_and_under_35kb() -> None:
    for slug in ("palier1_b0", "palier2_coeur_muet"):
        d_path = DEFAULT_DIGESTS_DIR / f"digest_{slug}.json"
        p_path = DEFAULT_DIGESTS_DIR / f"PROMPT_GEMINI_{slug}.md"
        assert d_path.exists(), f"Digest manquant : {d_path}"
        assert p_path.exists(), f"Prompt Gemini manquant : {p_path}"

        raw_bytes = d_path.read_bytes()
        assert not raw_bytes.startswith(b"\xef\xbb\xbf"), "BOM UTF-8 interdit"
        assert b"\r\n" not in raw_bytes, "CRLF interdit (LF uniquement)"
        assert len(raw_bytes) < MAX_DIGEST_BYTES, (
            f"{d_path.name} dépasse 35 Ko : {len(raw_bytes)} octets"
        )

        payload = json.loads(raw_bytes.decode("utf-8"))
        assert "active_core_rules" in payload
        assert "tested_tiles_rules" in payload
        assert payload["active_core_rules"]["version"] == "5.3.1"

        prompt_bytes = p_path.read_bytes()
        assert not prompt_bytes.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in prompt_bytes
        prompt_txt = prompt_bytes.decode("utf-8")
        assert prompt_txt.startswith(GEMINI_EDITORIAL_HEADER)
        assert "```json\n" in prompt_txt

    p2 = json.loads((DEFAULT_DIGESTS_DIR / "digest_palier2_coeur_muet.json").read_text("utf-8"))
    assert len(p2["tested_tiles_rules"]) == 8


def test_write_and_publish_digest_in_tmp_dir(tmp_path: Path, monkeypatch) -> None:
    sample_stats = {
        "campaign": "unit_test_bridge",
        "generated_at_utc": "2026-11-18T12:00:00Z",
        "totals": {
            "total_games": 400,
            "tested_tiles": ["G3:A", "M1:B"],
        },
        "metrics": {"mean_ratio_arbres": 0.642, "cvar20_ratio": 0.512},
    }
    d_path, p_path, digest = write_digest_and_prompt_files(
        "unit_test_bridge",
        sample_stats,
        chassis_ids=(0, 19),
        digests_dir=tmp_path,
        legacy_data_copy=False,
    )
    assert d_path.exists() and p_path.exists()
    assert len(digest["active_core_rules"]["chassis_7_axes"]) == 2
    assert [t["slot"] for t in digest["tested_tiles_rules"]] == ["G3", "M1"]

    prompt_md = build_prompt_gemini_markdown(digest)
    html_page = build_mobile_one_tap_html("unit_test_bridge", prompt_md, digest)
    assert "📋 Copier tout le dossier pour l'app Gemini" in html_page
    assert "PROMPT_GEMINI_unit_test_bridge.md" in html_page

    qr = render_ascii_qr("https://storage.cloud.google.com/amazonia-sim-runs/mobile/latest.html")
    assert "█" in qr

    # Test du téléversement local Google Drive synchronisé via variable d'environnement
    fake_drive = tmp_path / "fake_gdrive"
    fake_drive.mkdir()
    monkeypatch.setenv("AMAZONIA_GDRIVE_LOCAL_DIR", str(fake_drive))
    drive_res = upload_prompt_to_google_drive(p_path)
    assert drive_res["status"] == "OK_LOCAL_SYNC"
    assert (fake_drive / "Amazonia_Digests" / "PROMPT_GEMINI_unit_test_bridge.md").exists()
    assert (fake_drive / "Amazonia_Digests" / "PROMPT_GEMINI_unit_test_bridge.txt").exists()

    pub_res = publish_campaign_digest(
        "unit_test_bridge",
        sample_stats,
        chassis_ids=(0, 19),
        digests_dir=tmp_path,
        push_gcs=False,
        upload_drive=True,
        copy_clip=False,
    )
    assert pub_res["digest_bytes"] < MAX_DIGEST_BYTES
    assert (tmp_path / "last_digest.html").exists()
    assert "drive.file" in GCLOUD_DRIVE_AUTH_CMD
    assert len(build_self_contained_digest(sample_stats)["active_core_rules"]["tactiques"]) == 6


def test_digest_size_budget_prioritizes_varying_tiles_and_warns_without_crashing(
    tmp_path: Path,
) -> None:
    import pytest

    # 1. Dépassement modéré -> compactage + priorisation des tuiles qui varient dans tested_tiles_rules
    payload_many_tiles = {
        "campaign": "macro_budget_test",
        "generated_at_utc": "2026-11-19T12:00:00Z",
        "totals": {
            "total_games": 5000,
            "tested_tiles": [
                "G1:A",
                "G2:A",
                "G3:A",
                "G4:A",
                "G5:A",
                "G6:A",
                "G7:A",
                "G7:B",
                "R1:A",
                "R2:A",
                "M1:A",
                "M2:A",
            ],
        },
        "tile_metrics": {
            "G7:A": {"slot": "G7", "profile": "A", "n_games": 2500, "mean_ratio_arbres": 0.65},
            "G7:B": {"slot": "G7", "profile": "B", "n_games": 2500, "mean_ratio_arbres": 0.68},
        },
    }
    # On fixe max_bytes juste en dessous de la version 12 tuiles mais suffisant pour 2 tuiles variées
    full_compact_size = len(
        json.dumps(
            build_self_contained_digest(payload_many_tiles, chassis_ids=(0,)),
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
    )
    d_path, _p_path, final_digest = write_digest_and_prompt_files(
        "macro_budget_test",
        payload_many_tiles,
        chassis_ids=(0,),
        varying_tiles=("G7:A", "G7:B"),
        digests_dir=tmp_path,
        legacy_data_copy=False,
        max_bytes=full_compact_size - 10,
    )
    assert d_path.exists()
    kept_pairs = [(t["slot"], t["profil"]) for t in final_digest["tested_tiles_rules"]]
    assert kept_pairs == [("G7", "A"), ("G7", "B")]

    # 2. Dépassement massif -> aucun crash/assert, avertissement clair émis et fichier écrit
    with pytest.warns(UserWarning, match="dépasse le budget cible"):
        d_big, _p_big, big_digest = write_digest_and_prompt_files(
            "macro_huge_test",
            payload_many_tiles,
            chassis_ids=(0,),
            varying_tiles=("G7:A", "G7:B"),
            digests_dir=tmp_path,
            legacy_data_copy=False,
            max_bytes=1_000,
        )
    assert d_big.exists()
    assert big_digest["active_core_rules"]["version"] == "5.4.0"
    assert len(d_big.read_bytes()) >= 1_000
