"""Tests unitaires du chantier v6.3 — Étape 1 (Sanctuarisation v6.2, purge C02, audit 197, schéma bi-composant)."""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.audit_197 import audit_tiles_catalog_197
from scripts.build_studio_artifacts import (
    INVARIANTS_CONTRACT_PATH,
    RULES_CONTRACT_PATH,
    compile_studio_payloads,
    derive_economie_bot,
)
from scripts.tiles_v6_3_schema import (
    LOCKED_GARDIEN_CASTING_V6_3,
    SLOTS_SPEC_30,
    V6_3_CONTRACT_PATH,
    V6_3_SCHEMA_PATH,
    build_v6_3_scaffold,
    is_v6_3_tiles_contract,
    validate_tiles_canon_v6_3,
)
from verify_lot import verify_kernel_locks

ROOT = Path(__file__).resolve().parent.parent
CADRAGE_V6_3_PATH = ROOT / "docs" / "cadrage_tuiles_v6_3.md"
TILES_V6_2_PATH = ROOT / "contracts" / "tiles_canon_v6_2.json"
SOCLE_V6_2_LOCKS_PATH = ROOT / "contracts" / "v6_2_socle_locks.sha256"


def _make_complete_v6_3_fixture() -> dict[str, Any]:
    """Construit un contrat bi-composant v6.3 complet (30 tuiles) à partir des rôles structurels v6.2."""
    v62 = json.loads(TILES_V6_2_PATH.read_text(encoding="utf-8"))
    v62_tiles = v62["tuiles_ciblees"]
    doc = build_v6_3_scaffold()
    doc["_meta"]["statut_global"] = "PANEL_30_AFFINE"
    doc["_meta"]["etape_active"] = "ETAPE_3_AFFINAGE_EDITORIAL"

    for sid, fam, orig, vois, alias in SLOTS_SPEC_30:
        old_prof = v62_tiles[sid]["profils"]["A"]
        tile = doc["tuiles_ciblees"][sid]
        nature = "LOI_PASSIVE" if str(old_prof.get("nature", "")).lower() == "loi_passive" else "ACTION"
        roles: list[str] = []
        tags = {str(t).upper() for t in (old_prof.get("tags") or [])}
        if "CATALYSEUR_EVEIL" in tags:
            roles.append("CATALYSEUR_EVEIL")
        if "LEVIER_REVE" in tags:
            roles.append("LEVIER_REVE")
        if "ENRACINEMENT" in tags:
            roles.append("ENRACINEMENT")
        if nature == "LOI_PASSIVE":
            roles.append("LOI_PASSIVE")
        if sid in {"R1", "R2", "R6", "R10", "M4", "M5"}:
            roles.append("AUTONOMIE_A0")
        est_twist = bool(old_prof.get("est_twist_canon0", False))
        if est_twist:
            roles.append("TWIST_2K3")

        tile["nature"] = nature
        tile["roles_portes"] = roles
        tile["est_twist"] = est_twist
        tile["vecteurs"] = str(old_prof.get("vecteurs") or "V4 -> V2")
        tile["entrees"] = list(old_prof.get("entrees") or [])
        tile["sorties"] = list(old_prof.get("sorties") or [])
        tile["paiement"] = list(old_prof.get("paiement") or ["P_ARBRE"])
        tile["declencheurs_amorces"] = list(old_prof.get("declencheurs_amorces") or [])
        tile["double_ouverture"] = old_prof.get("double_ouverture")
        tile["tags"] = list(old_prof.get("tags") or [])
        tile["heuristique_bot"] = str(old_prof.get("heuristique_bot") or "Arbitrage synergique v6.3")
        tile["engine_sync_status"] = "REFINED_V6_3"
        tile["statut_conception"] = "PASSE_2_AFFINE"

        tp = tile["tuile_plateau"]
        cj = tile["carte_joueur"]
        if fam == "GARDIEN":
            animal = LOCKED_GARDIEN_CASTING_V6_3[sid]
            tp["nom_court"] = animal
            tp["icone_conseillee"] = old_prof.get("cablage_recommande") or "ICONE_PARADE"
            tp["pictogrammes"] = ["PIC_DEFENSEUR", "PIC_PARI_ENCOCHE"]
            tp["mots_cles_plateau"] = {
                "face_1": "Pari → Synergie",
                "face_2": "Pari → Synergie amplifiée",
                "enracine": None,
            }
            tp["resume_plateau"] = "🛡️ ⭐"
            cj["titre_complet"] = animal
            cj["entite_illustree"] = f"{animal} dans son biotope amazonien"
            cj["texte_regle"] = {
                "face_1": (
                    f"Si {animal} s’active sur son icône, le gouverneur choisit une cible "
                    f"compatible avec {alias}. Lorsque l’opportunité se présente, il peut aussi "
                    f"combiner ce mouvement avec l’accessoire de son voisin sans aucune limite "
                    f"artificielle de longueur rédactionnelle ni de nombre de conditions."
                ),
                "face_2": (
                    f"Face éveillée autonome de {animal} : lorsque ce Gardien s’ouvre en Face 2, "
                    f"appliquez l’effet complet sur deux cibles distinctes si possible. Si la "
                    f"seconde cible appartient à la lisière {alias}, déclenchez le bonus associé."
                ),
                "enracine": None,
            }
        else:
            nom = str(old_prof.get("nom") or f"Vision {alias}")
            tp["nom_court"] = nom
            tp["icone_conseillee"] = None
            tp["pictogrammes"] = (
                ["PIC_REVE", "PIC_ANNULATION"] if fam == "REVE" else ["PIC_NID", "PIC_INSECTE"]
            )
            tp["mots_cles_plateau"] = {
                "face_1": "Synergie lisière",
                "face_2": None,
                "enracine": "+Souches" if "ENRACINEMENT" in roles else None,
            }
            tp["resume_plateau"] = "🌙 🚫" if fam == "REVE" else "🪹 🐜"
            cj["titre_complet"] = nom
            cj["entite_illustree"] = str(old_prof.get("animal_ou_theme") or nom)
            cj["texte_regle"] = {
                "face_1": (
                    f"Quand {nom} se résout sur la lisière {alias}, le gouverneur arbitre entre "
                    f"tempo et consolidation. Si une synergie inter-peuples est prête, appliquez "
                    f"intégralement la chaîne d’effets sur le plateau sans modificateur flottant."
                ),
                "face_2": None,
                "enracine": (
                    "Au décompte final, bonifie la régénération des Souches sur sa parcelle."
                    if "ENRACINEMENT" in roles
                    else None
                ),
            }

        cj["brief_illustration"] = f"Scène complète amazonienne centrée sur {cj['entite_illustree']}."
        cj["pitch_ambiance"] = f"Présence vivante de la lisière {alias}."
        cj["decision_et_renoncement"] = {
            "choix": "Choisir la cible prioritaire du moteur inter-peuples.",
            "renoncement": "Renoncer à l’option alternative sur ce tour.",
        }
        tile["temoins"] = [
            {
                "id": f"{sid}_T1",
                "resume": f"Cas témoin exécutable de {sid} ({alias}).",
                "etat_attendu_verifie": {"ok": True},
                "statut": "A_CODER",
            }
        ]

    return doc


def test_v6_2_sanctuarization_and_cadrage_document() -> None:
    """Vérifie la sanctuarisation SHA-256 v6.2 et la présence intégrale de docs/cadrage_tuiles_v6_3.md."""
    assert SOCLE_V6_2_LOCKS_PATH.is_file()
    lock_txt = SOCLE_V6_2_LOCKS_PATH.read_text(encoding="utf-8")
    for expected in (
        "contracts/rules_canon_v6_2.json",
        "contracts/physical_and_edge_invariants.json",
        "contracts/tiles_canon_v6_2.json",
    ):
        assert expected in lock_txt
    verify_kernel_locks()

    assert CADRAGE_V6_3_PATH.is_file()
    cadrage = CADRAGE_V6_3_PATH.read_text(encoding="utf-8")
    assert "Dédoublement matériel de chaque Tuile de Synergie" in cadrage
    assert "Casting verrouillé des 15 Gardiens" in cadrage
    assert "I07" in cadrage
    assert "contracts/tiles_canon_v6_3.json" in cadrage


def test_audit_197_on_v6_2_archive_and_no_c02() -> None:
    """Vérifie que scripts/audit_197.py valide l'archive v6.2 sur les 197 assises sans C02."""
    doc = json.loads(TILES_V6_2_PATH.read_text(encoding="utf-8"))
    report = audit_tiles_catalog_197(doc, allow_draft=False)
    assert report["verdict_global"] == "OK", report["errors"]
    assert report["c02_word_count_purged"] is True
    assert "C02_textes" not in report
    assert report["assises"]["total"] == 197
    assert report["assises"]["compositions"] == 42
    assert report["assises"]["presence_par_emplacement"] == 64
    assert report["I04_couverture_eveil"]["nombre"] == 9
    assert report["I05_couverture_sommeil"]["assises_E_sans_H"] == 30
    assert report["I06_enracinement"]["nombre"] == 4
    assert report["Q01_lois_passives"]["max_par_assise"] <= 2
    assert report["Q02_twists_2K3"]["nombre"] == 6


def test_audit_197_enlarged_twin_closure_and_structural_invariants() -> None:
    """Vérifie I01 élargi à la jumelle Y>X, I02, I03, I04, I05, I06, Q01, mem_debt et I07 sans C02."""
    base_v63 = _make_complete_v6_3_fixture()
    rep_ok = audit_tiles_catalog_197(base_v63, allow_draft=False)
    assert rep_ok["verdict_global"] == "OK", rep_ok["errors"]

    # 1. I01 élargi à la jumelle Y>X : G2 (R>M) exige BLEU produit par sa jumelle G1 (M>R) -> VALIDE !
    twin_ok = copy.deepcopy(base_v63)
    assert "BLEU" in twin_ok["tuiles_ciblees"]["G1"]["sorties"]
    twin_ok["tuiles_ciblees"]["G2"]["entrees"].append("BLEU")
    rep_twin = audit_tiles_catalog_197(twin_ok, allow_draft=False)
    assert rep_twin["verdict_global"] == "OK", rep_twin["errors"]
    assert any(
        d["tuile"] == "G2" and d["etat"] == "BLEU" and d["fourni_par_jumelle"] == "G1"
        for d in rep_twin["I01_cloture_elargie_197"]["dependances_jumelle_lisiere"]
    )

    # 2. I01 négatif : G7 (M>H) exige BLEU alors que ni G7 ni sa jumelle R3 ni le socle ne le produisent -> ÉCHEC
    bad_closure = copy.deepcopy(base_v63)
    bad_closure["tuiles_ciblees"]["G7"]["entrees"].append("BLEU")
    rep_bad_cl = audit_tiles_catalog_197(bad_closure, allow_draft=False)
    assert rep_bad_cl["verdict_global"] == "ECHEC"
    assert any("G7" in e and "BLEU" in e for e in rep_bad_cl["I01_cloture_elargie_197"]["closure_violations"])

    # 3. I01 négatif : exclusivité stricte Insectes hors lisières de I
    bad_ins = copy.deepcopy(base_v63)
    bad_ins["tuiles_ciblees"]["G1"]["entrees"].append("INSECTE")
    rep_ins = audit_tiles_catalog_197(bad_ins, allow_draft=False)
    assert rep_ins["verdict_global"] == "ECHEC"
    assert any("G1" in e for e in rep_ins["I01_cloture_elargie_197"]["insect_violations"])

    # 4. I02 négatif : dépendance Gardien sur tuile A=0 (R2)
    bad_a0 = copy.deepcopy(base_v63)
    bad_a0["tuiles_ciblees"]["R2"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Activez un Gardien voisin à l’ouverture."
    )
    rep_a0 = audit_tiles_catalog_197(bad_a0, allow_draft=False)
    assert rep_a0["verdict_global"] == "ECHEC"
    assert any("R2" in e for e in rep_a0["I02_autonomie_A0"]["violations"])

    # 5. I03 négatif : même sortie principale sur une lisière (G1 / G2)
    bad_div = copy.deepcopy(base_v63)
    bad_div["tuiles_ciblees"]["G2"]["sorties"] = ["DEFENSEUR_REDEPLOYE"]
    rep_div = audit_tiles_catalog_197(bad_div, allow_draft=False)
    assert rep_div["verdict_global"] == "ECHEC"
    assert any("M–R" in e for e in rep_div["I03_divergence_lisiere"]["violations"])

    # 6. C01 mem_debt = 0 : modificateur flottant 'pour ce tour' rejeté
    bad_mem = copy.deepcopy(base_v63)
    bad_mem["tuiles_ciblees"]["G3"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Les machines ont -1 au Seuil de Parade pour ce tour."
    )
    rep_mem = audit_tiles_catalog_197(bad_mem, allow_draft=False)
    assert rep_mem["verdict_global"] == "ECHEC"
    assert any("pour ce tour" in e for e in rep_mem["C01_mem_debt"]["mem_debt_hits"])

    # 7. Q01 négatif : > 2 lois passives sur une même assise (M1 + M2 + M3 sur M-I, R-I, O-I)
    bad_lois = copy.deepcopy(base_v63)
    for sid in ("M1", "G13", "G14"):
        bad_lois["tuiles_ciblees"][sid]["nature"] = "LOI_PASSIVE"
        if "LOI_PASSIVE" not in bad_lois["tuiles_ciblees"][sid]["roles_portes"]:
            bad_lois["tuiles_ciblees"][sid]["roles_portes"].append("LOI_PASSIVE")
    rep_lois = audit_tiles_catalog_197(bad_lois, allow_draft=False)
    assert rep_lois["verdict_global"] == "ECHEC"
    assert rep_lois["Q01_lois_passives"]["max_par_assise"] > 2


def test_v6_3_schema_contract_and_casting_guards() -> None:
    """Valide tiles_canon_v6_3.schema.json, le squelette initial et le casting animalier verrouillé."""
    schema = json.loads(V6_3_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$schema"].startswith("https://json-schema.org/draft/2020-12")
    assert "tile_v6_3" in schema["$defs"]
    assert "tuile_plateau" in schema["$defs"]["tile_v6_3"]["properties"]
    assert "carte_joueur" in schema["$defs"]["tile_v6_3"]["properties"]

    scaffold = json.loads(V6_3_CONTRACT_PATH.read_text(encoding="utf-8"))
    assert is_v6_3_tiles_contract(scaffold) is True
    assert validate_tiles_canon_v6_3(scaffold, strict=False) == []

    complete = _make_complete_v6_3_fixture()
    assert validate_tiles_canon_v6_3(complete, strict=True) == []

    # Rejet d'un titre organe/geste sur Gardien ("Le Bec du Toucan")
    bad_title = copy.deepcopy(complete)
    bad_title["tuiles_ciblees"]["G6"]["tuile_plateau"]["nom_court"] = "Le Bec du Toucan"
    errs_title = validate_tiles_canon_v6_3(bad_title, strict=True)
    assert any("casting Gardien verrouillé" in e for e in errs_title)
    assert any("organe/geste interdit" in e for e in errs_title)

    # Rejet d'une phrase rédigée sur la Mini-Tuile Plateau
    bad_mini = copy.deepcopy(complete)
    bad_mini["tuiles_ciblees"]["G1"]["tuile_plateau"]["mots_cles_plateau"]["face_1"] = (
        "Déplacez un Défenseur sur une parcelle ciblée."
    )
    errs_mini = validate_tiles_canon_v6_3(bad_mini, strict=True)
    assert any("zéro phrase rédigée sur la Mini-Tuile" in e for e in errs_mini)

    # Rejet de toute réintroduction de champ C02 'mots_par_face'
    bad_c02 = copy.deepcopy(complete)
    bad_c02["tuiles_ciblees"]["G1"]["mots_par_face"] = {"Face 1": {"mots": 42}}
    errs_c02 = validate_tiles_canon_v6_3(bad_c02, strict=True)
    assert any("mots_par_face" in e for e in errs_c02)


def test_build_studio_artifacts_accepts_v6_3_bicomponent_catalog_without_breaking() -> None:
    """Prouve la rétrocompatibilité transitoire du compilateur Studio avec le contrat v6.3."""
    rules = json.loads(RULES_CONTRACT_PATH.read_text(encoding="utf-8"))
    invariants = json.loads(INVARIANTS_CONTRACT_PATH.read_text(encoding="utf-8"))
    v63_doc = _make_complete_v6_3_fixture()

    spec_f, catalog_doc, amazonia_js, adapted = compile_studio_payloads(
        rules, invariants, v63_doc, existing_changelog=[]
    )
    assert spec_f["architecture_reference"]["total_emplacements_synergie"] == 30
    assert catalog_doc["total_emplacements"] == 30
    assert "const CATALOGUE_TUILES =" in amazonia_js
    assert '"tuile_plateau":' in amazonia_js
    assert '"carte_joueur":' in amazonia_js
    assert '"Le Jaguar"' in amazonia_js

    # derive_economie_bot fonctionne sans erreur sur les 30 tuiles v6.3 projetées
    trigger_codes = rules["supports_fixes"]["piste_gardiens"]["codes_internes"]
    for sid, slot in adapted["tuiles_ciblees"].items():
        prof = slot["profils"]["A"]
        eco = derive_economie_bot(slot, prof, trigger_codes=trigger_codes)
        assert eco["outputs_produits"], f"{sid}: economie_bot vide"


@pytest.mark.parametrize("slot_id,expected_animal", sorted(LOCKED_GARDIEN_CASTING_V6_3.items()))
def test_v6_3_scaffold_locks_all_15_gardien_animals(slot_id: str, expected_animal: str) -> None:
    scaffold = json.loads(V6_3_CONTRACT_PATH.read_text(encoding="utf-8"))
    tile = scaffold["tuiles_ciblees"][slot_id]
    assert tile["tuile_plateau"]["nom_court"] == expected_animal
    assert tile["carte_joueur"]["titre_complet"] == expected_animal
