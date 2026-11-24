"""Tests de validation du contrat exécutable spec_bundle_v6_0.json compilé depuis le SSOT v6.2."""

from __future__ import annotations

import json
from pathlib import Path

from scripts_cloud.build_spec_bundle import RES_VOCAB, TRIG_VOCAB

ROOT = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT / "data" / "spec_bundle_v6_0.json"

VALID_ROLES = {"PRODUCTEUR", "CONSOMMATEUR", "MODULATEUR", "CONTROLE", "CATALYSEUR"}
VALID_PORTEES = {"LOCAL_RAYON", "LISIERES_ADJACENTES", "GLOBAL_PLATEAU", "PISTE_TACTIQUES"}
ALLOWED_TOKENS = RES_VOCAB | TRIG_VOCAB


def test_spec_bundle_structure_and_counts() -> None:
    assert BUNDLE_PATH.exists(), "data/spec_bundle_v6_0.json manquant"
    bundle = json.loads(BUNDLE_PATH.read_text(encoding="utf-8"))

    assert bundle["meta"]["schema_version"] == "6.2.0"
    assert bundle["meta"]["source_studio_version"] == "v6.2"
    assert len(bundle["chassis_axes"]) == 6
    placement_ax = next(ax for ax in bundle["chassis_axes"] if ax["key"] == "Placement_Initial_Machines")
    assert placement_ax["defaultVal"] == "BULLDOZER_P1_ABATTEUSE_P2"
    assert all(ax.get("locked") is True for ax in bundle["chassis_axes"])

    assert [t["id"] for t in bundle["tactiques"]] == ["T1", "T2", "T3", "T4", "T5", "T6"]
    assert bundle["machine_deck_rules"]["sabotage_dilution_permanente"] is True
    assert bundle["machine_deck_rules"]["lancer_des_universel"] is True
    assert bundle["machine_deck_rules"]["support_physique"] == "SAC_OPAQUE_JETONS_EPAIS"

    # Purge des fausses constantes documentaires
    assert "arbres_coupes_max" not in bundle["machine_damage_rules"]["ABATTEUSE"]
    assert bundle["machine_damage_rules"]["ABATTEUSE"]["coupe_tous_les_arbres"] is True
    assert bundle["machine_damage_rules"]["repousse_finale_base"] == 0
    assert bundle["machine_damage_rules"]["seuil_parade"]["bleus_actifs_tous_modes"] == [
        "CHARGE",
        "ASSAUT",
        "RATISSAGE",
    ]
    rat = bundle["machine_damage_rules"]["ratissage"]
    assert rat["piste_tactiques_fixe"] is True
    assert rat["mode_permanent"] == "ASSAUT"
    assert rat["detache_de_case_1"] is True
    assert rat["bonus_puissance_imprime"] == 0
    assert rat["gain_jeton_rouge_physique"] == 1
    assert "traite_comme_jeton_rouge_a_tous_egards" not in rat

    assert bundle["reglette_tactiques_reversible"]["acte_1_charge_cases"] == [1, 2, 3]
    assert bundle["reglette_tactiques_reversible"]["acte_2_charge_cases"] == [4, 5, 6]
    assert bundle["piste_gardiens"]["ordre_gauche_droite"] == [
        "PARADE",
        "PIEGEAGE",
        "SABOTAGE",
        "REVE",
        "INSECTE",
        "RESONANCE",
    ]

    cat = bundle["catalogue_tuiles"]
    assert len(cat) == 30

    by_family: dict[str, int] = {}
    total_profils = 0
    for slot in cat.values():
        fam = slot["famille"]
        n = len(slot["profils"])
        by_family[fam] = by_family.get(fam, 0) + n
        total_profils += n

    assert total_profils == 30
    assert by_family == {
        "GARDIEN": 15,
        "REVE": 10,
        "CROISSANCE": 5,
    }


def test_all_30_canon0_profiles_have_coherent_economie_bot() -> None:
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
                assert tok != "RES_APPRENTISSAGE"
            for tok in eco["outputs_produits"]:
                assert tok in ALLOWED_TOKENS, f"{slot_id}.{prof_key}: output inconnu {tok}"
                assert tok != "RES_CARTE_SABOTAGE"
                assert tok != "RES_APPRENTISSAGE"

            cablage = prof.get("cablage") or []
            for trig_num in cablage:
                assert f"TRIG_{trig_num}" in eco["inputs_requis"], (
                    f"{slot_id}.{prof_key}: câblage TRIG_{trig_num} absent de inputs_requis"
                )

            tags = {t.upper() for t in prof.get("tags", [])}
            if "SABOTAGE" in tags or "ECAILLE" in tags:
                assert "RES_DILUTION_SABOTAGE" in eco["outputs_produits"], (
                    f"{slot_id}.{prof_key}: tag SABOTAGE/ECAILLE sans RES_DILUTION_SABOTAGE"
                )
