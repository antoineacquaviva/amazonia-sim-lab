"""Tests de validation du contrat exécutable spec_bundle_v5_5.json et mode3_reference.json."""

from __future__ import annotations

import json
from pathlib import Path

from scripts_cloud.build_spec_bundle import RES_VOCAB, TRIG_VOCAB

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "data" / "spec_bundle_v5_5.json"

VALID_ROLES = {"PRODUCTEUR", "CONSOMMATEUR", "MODULATEUR", "CONTROLE", "CATALYSEUR"}
VALID_PORTEES = {"LOCAL_RAYON", "LISIERES_ADJACENTES", "GLOBAL_PLATEAU", "PISTE_TACTIQUES"}
ALLOWED_TOKENS = RES_VOCAB | TRIG_VOCAB


def test_spec_bundle_structure_and_counts() -> None:
    assert BUNDLE_PATH.exists(), "data/spec_bundle_v5_5.json manquant"
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))

    assert bundle["meta"]["schema_version"] == "5.5.0"
    assert len(bundle["chassis_axes"]) == 6
    assert [t["id"] for t in bundle["tactiques"]] == ["T1", "T2", "T3", "T4", "T5", "T6"]
    assert bundle["machine_deck_rules"]["sabotage_dilution_permanente"] is True
    assert bundle["machine_damage_rules"]["ratissage"]["piste_tactiques_fixe"] is True
    assert bundle["machine_damage_rules"]["ratissage"]["bonus_puissance_imprime"] == 1

    cat = bundle["catalogue_tuiles"]
    assert len(cat) == 32

    by_family: dict[str, int] = {}
    total_profils = 0
    for slot in cat.values():
        fam = slot["famille"]
        n = len(slot["profils"])
        by_family[fam] = by_family.get(fam, 0) + n
        total_profils += n

    assert total_profils == 101
    assert by_family == {
        "GARDIEN": 45,
        "REVE": 31,
        "CROISSANCE": 19,
        "MIGRATION": 6,
    }


def test_all_100_profiles_have_coherent_economie_bot() -> None:
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))
    for slot_id, slot in bundle["catalogue_tuiles"].items():
        for prof_key, prof in slot["profils"].items():
            eco = prof.get("economie_bot")
            assert isinstance(eco, dict), f"{slot_id}.{prof_key}: economie_bot manquant"
            assert eco["role"] in VALID_ROLES
            assert eco["portee"] in VALID_PORTEES
            assert len(eco["outputs_produits"]) >= 1

            for tok in eco["inputs_requis"]:
                assert tok in ALLOWED_TOKENS, f"{slot_id}.{prof_key}: input inconnu {tok}"
                assert tok != "RES_CARTE_SABOTAGE"
            for tok in eco["outputs_produits"]:
                assert tok in ALLOWED_TOKENS, f"{slot_id}.{prof_key}: output inconnu {tok}"
                assert tok != "RES_CARTE_SABOTAGE"

            cablage = prof.get("cablage") or []
            for trig_num in cablage:
                assert f"TRIG_{trig_num}" in eco["inputs_requis"], (
                    f"{slot_id}.{prof_key}: câblage TRIG_{trig_num} absent de inputs_requis"
                )

            tags = {t.upper() for t in prof.get("tags", [])}
            if "SABOTAGE" in tags:
                assert "RES_DILUTION_SABOTAGE" in eco["outputs_produits"], (
                    f"{slot_id}.{prof_key}: tag SABOTAGE sans RES_DILUTION_SABOTAGE"
                )

