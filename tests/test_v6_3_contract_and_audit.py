"""Tests unitaires du chantier v6.3 — Étapes 1 & 1bis.

Couvre :
- Sanctuarisation SHA-256 v6.2 (`v6_2_socle_locks.sha256` & `kernel_locks.sha256`) ;
- Cadrage `docs/cadrage_tuiles_v6_3.md` (4 murs porteurs `M1..M4`, focalisation, multi-panels) ;
- Audit `197` assises (`scripts/audit_197.py`) sans `C02` (`I07`) ;
- Les 4 Murs Porteurs Physiques (`M1_TEMPS_BATAILLE`, `M2_CONSERVATION_THERMIQUE`,
  `M3_INTEGRITE_PLATEAU_ET_ICONES`, `M4_AUTONOMIE_PLANCHER_SOLO`) + gardes anti-faux-positifs ;
- Schéma bi-composant `v6.3.1` (`entrees_plancher` / `entrees_synergie`, casting animalier) ;
- Staging & comparatif multi-panels (`contracts/panels/` + `audit_panels_directory`) ;
- Rétrocompatibilité transitoire du compilateur Studio (`scripts/build_studio_artifacts.py`).
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from scripts.audit_197 import audit_panels_directory, audit_tiles_catalog_197
from scripts.build_studio_artifacts import (
    INVARIANTS_CONTRACT_PATH,
    RULES_CONTRACT_PATH,
    compile_studio_payloads,
    derive_economie_bot,
)
from scripts.tiles_v6_3_schema import (
    LOCKED_GARDIEN_CASTING_V6_3,
    MURS_PORTEURS_V6_3,
    PANELS_DIR,
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


def _make_complete_v6_3_fixture(*, panel_id: str = "panel_fixture") -> dict[str, Any]:
    """Construit un contrat bi-composant v6.3.1 complet (30 tuiles) conforme à M1..M4 + I01..I07."""
    v62 = json.loads(TILES_V6_2_PATH.read_text(encoding="utf-8"))
    v62_tiles = v62["tuiles_ciblees"]
    doc = build_v6_3_scaffold()
    doc["_meta"]["schema_version"] = "6.3.1"
    doc["_meta"]["statut_global"] = "PANEL_30_AFFINE"
    doc["_meta"]["etape_active"] = "ETAPE_3_AFFINAGE_EDITORIAL"
    doc["_meta"]["panel_id"] = panel_id

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

        raw_in = list(old_prof.get("entrees") or [])
        tile["nature"] = nature
        tile["roles_portes"] = roles
        tile["est_twist"] = est_twist
        tile["vecteurs"] = str(old_prof.get("vecteurs") or "V4 -> V2")
        tile["entrees_plancher"] = list(raw_in)
        tile["entrees_synergie"] = []
        tile["entrees"] = list(raw_in)
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
                "enracine": "+Souches décompte final" if "ENRACINEMENT" in roles else None,
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
                    "Au décompte final, retournez 1 Souche supplémentaire de sa parcelle en Arbre debout."
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
    """Vérifie la sanctuarisation SHA-256 v6.2, les 4 murs porteurs dans cadrage_tuiles_v6_3.md et contracts/panels/."""
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
    for needle in (
        "Dédoublement matériel de chaque Tuile de Synergie",
        "Casting verrouillé des 15 Gardiens",
        "I07",
        *MURS_PORTEURS_V6_3,
        "Focalisation mécanique",
        "contracts/panels/",
    ):
        assert needle in cadrage, f"Mention manquante dans cadrage_tuiles_v6_3.md : {needle!r}"

    assert PANELS_DIR.is_dir()
    assert (PANELS_DIR / "README.md").is_file()


def test_audit_197_on_v6_2_archive_and_no_c02() -> None:
    """Vérifie que scripts/audit_197.py valide l'archive v6.2 sur les 197 assises et les 4 murs M1..M4 sans C02."""
    doc = json.loads(TILES_V6_2_PATH.read_text(encoding="utf-8"))
    report = audit_tiles_catalog_197(doc, allow_draft=False)
    assert report["verdict_global"] == "OK", report["errors"]
    assert report["c02_word_count_purged"] is True
    assert "C02_textes" not in report
    assert report["M1_TEMPS_BATAILLE"]["verdict"] == "OK"
    assert report["M2_CONSERVATION_THERMIQUE"]["verdict"] == "OK"
    assert report["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "OK"
    assert report["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"] == "OK"
    assert report["assises"]["total"] == 197
    assert report["assises"]["compositions"] == 42
    assert report["assises"]["presence_par_emplacement"] == 64
    assert report["I04_couverture_eveil"]["nombre"] == 9
    assert report["I05_couverture_sommeil"]["assises_E_sans_H"] == 30
    assert report["I06_enracinement"]["nombre"] == 4
    assert report["Q01_lois_passives"]["max_par_assise"] <= 2
    assert report["Q02_twists_2K3"]["nombre"] == 6


def test_m1_temps_bataille_rejects_midgame_regen_and_allows_spatial_and_final_scoring() -> None:
    """M1 : bloque Souche -> Arbre en Tours 1–8 ou à la pose d'Enracinement ; zéro faux positif spatial/décompte final."""
    base = _make_complete_v6_3_fixture()

    # Positif 1 : condition spatiale lisant un Arbre debout (pont de canopée) -> 100 % VALIDE
    ok_spatial = copy.deepcopy(base)
    ok_spatial["tuiles_ciblees"]["G3"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Déplacez 1 Défenseur depuis une parcelle portant au moins 1 Arbre debout vers "
        "une parcelle voisine portant aussi un Arbre debout (pont de canopée)."
    )
    rep_sp = audit_tiles_catalog_197(ok_spatial, allow_draft=False)
    assert rep_sp["M1_TEMPS_BATAILLE"]["verdict"] == "OK", rep_sp["M1_TEMPS_BATAILLE"]

    # Positif 2 : Enraciné au décompte final -> 100 % VALIDE
    ok_final = copy.deepcopy(base)
    ok_final["tuiles_ciblees"]["M5"]["carte_joueur"]["texte_regle"]["enracine"] = (
        "Au décompte final, chaque Insecte présent sur sa parcelle retourne 1 Souche de plus en Arbre debout."
    )
    rep_fin = audit_tiles_catalog_197(ok_final, allow_draft=False)
    assert rep_fin["M1_TEMPS_BATAILLE"]["verdict"] == "OK", rep_fin["M1_TEMPS_BATAILLE"]

    # Positif 3 : Enraciné à la pose sans régénération Souche -> Arbre (ex. Altération) -> 100 % VALIDE
    ok_enr_alt = copy.deepcopy(base)
    ok_enr_alt["tuiles_ciblees"]["R2"]["carte_joueur"]["texte_regle"]["enracine"] = (
        "Lors de son enracinement, altérez jusqu’à 2 machines mobiles."
    )
    rep_alt = audit_tiles_catalog_197(ok_enr_alt, allow_draft=False)
    assert rep_alt["M1_TEMPS_BATAILLE"]["verdict"] == "OK", rep_alt["M1_TEMPS_BATAILLE"]

    # Négatif 1 : Souche -> Arbre en Face 1 -> ÉCHEC M1
    bad_f1 = copy.deepcopy(base)
    bad_f1["tuiles_ciblees"]["G7"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Retournez 1 Souche de votre rayon en Arbre debout."
    )
    rep_f1 = audit_tiles_catalog_197(bad_f1, allow_draft=False)
    assert rep_f1["M1_TEMPS_BATAILLE"]["verdict"] == "ECHEC"
    assert any("G7.face_1" in v for v in rep_f1["M1_TEMPS_BATAILLE"]["violations"])

    # Négatif 2 : Souche -> Arbre au moment de la pose d'Enracinement -> ÉCHEC M1
    bad_enr = copy.deepcopy(base)
    bad_enr["tuiles_ciblees"]["R6"]["carte_joueur"]["texte_regle"]["enracine"] = (
        "Lors de son enracinement, retournez immédiatement 1 Souche de sa parcelle en Arbre debout."
    )
    rep_enr = audit_tiles_catalog_197(bad_enr, allow_draft=False)
    assert rep_enr["M1_TEMPS_BATAILLE"]["verdict"] == "ECHEC"
    assert any("R6.enracine" in v for v in rep_enr["M1_TEMPS_BATAILLE"]["violations"])


def test_m2_conservation_thermique_rejects_dry_blue_and_allows_red_flip_or_transfer() -> None:
    """M2 : bloque tout Bleu posé à sec depuis la réserve ; accepte retournement/transfert de Rouge et lecture."""
    base = _make_complete_v6_3_fixture()

    # Positif : retournement, transfert de Rouge en Bleu, déplacement de Bleu existant et loi de lecture
    ok_thermal = copy.deepcopy(base)
    ok_thermal["tuiles_ciblees"]["G6"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Retournez 1 jeton rouge d’une machine en bleu, ou prenez 1 jeton rouge d’une "
        "machine pour le poser sur sa face bleue sur une autre machine."
    )
    ok_thermal["tuiles_ciblees"]["G6"]["carte_joueur"]["texte_regle"]["face_2"] = (
        "Déplacez 1 jeton bleu d’une machine vers une autre ; en Assaut, un jeton rouge "
        "sur la machine visée compte comme un Bleu Surchauffe dans le Seuil."
    )
    rep_ok = audit_tiles_catalog_197(ok_thermal, allow_draft=False)
    assert rep_ok["M2_CONSERVATION_THERMIQUE"]["verdict"] == "OK", rep_ok["M2_CONSERVATION_THERMIQUE"]

    # Négatif 1 : Bleu posé à sec sur une machine
    bad_dry = copy.deepcopy(base)
    bad_dry["tuiles_ciblees"]["G6"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Posez 1 jeton bleu Surchauffe sur la machine ciblée."
    )
    rep_dry = audit_tiles_catalog_197(bad_dry, allow_draft=False)
    assert rep_dry["M2_CONSERVATION_THERMIQUE"]["verdict"] == "ECHEC"
    assert any("G6.face_1" in v for v in rep_dry["M2_CONSERVATION_THERMIQUE"]["violations"])

    # Négatif 2 : Bleu depuis la réserve en clause de repli `; sinon ...`
    bad_res = copy.deepcopy(base)
    bad_res["tuiles_ciblees"]["M4"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Retournez 1 jeton rouge en bleu ; sinon ajoutez 1 jeton bleu depuis la réserve."
    )
    rep_res = audit_tiles_catalog_197(bad_res, allow_draft=False)
    assert rep_res["M2_CONSERVATION_THERMIQUE"]["verdict"] == "ECHEC"
    assert any("M4.face_1" in v for v in rep_res["M2_CONSERVATION_THERMIQUE"]["violations"])


def test_m3_integrite_2233_voluntary_cut_and_icon_fixity() -> None:
    """M3 : immobilité Arbres/Souches, zéro coupe volontaire alliée, fixité d'icône ≤ 1 Twist dédié."""
    base = _make_complete_v6_3_fixture()

    # Positif M3a/M3b/M3c : déplacement Défenseur entre Souches + mention machine qui coupe + 1 seul Twist sautant d'icône
    ok_m3 = copy.deepcopy(base)
    ok_m3["tuiles_ciblees"]["G3"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Déplacez 1 Défenseur d’une parcelle à Souche vers une parcelle voisine à Souche. "
        "Si une Abatteuse coupe un Arbre sur ce rayon, ajoutez 1 Sabotage au sac."
    )
    ok_m3["tuiles_ciblees"]["G15"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Échangez les rangs de deux machines, puis vous pouvez déplacer ce Gardien vers une icône voisine."
    )
    assert ok_m3["tuiles_ciblees"]["G15"]["est_twist"] is True
    rep_ok = audit_tiles_catalog_197(ok_m3, allow_draft=False)
    assert rep_ok["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "OK", rep_ok[
        "M3_INTEGRITE_PLATEAU_ET_ICONES"
    ]
    assert rep_ok["M3_INTEGRITE_PLATEAU_ET_ICONES"]["gardiens_saut_icone"] == ["G15"]

    # Négatif M3a : déplacer une Souche / Arbre entre parcelles
    bad_move = copy.deepcopy(base)
    bad_move["tuiles_ciblees"]["G7"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Déplacez 1 Souche vers une parcelle voisine."
    )
    rep_mv = audit_tiles_catalog_197(bad_move, allow_draft=False)
    assert rep_mv["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "ECHEC"
    assert any("M3a" in v for v in rep_mv["M3_INTEGRITE_PLATEAU_ET_ICONES"]["violations"])

    # Négatif M3b : couper volontairement un Arbre debout allié comme coût
    bad_cut = copy.deepcopy(base)
    bad_cut["tuiles_ciblees"]["R8"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Coupez 1 Arbre debout de votre rayon en Souche pour glisser un Rêve de 2 rangs."
    )
    rep_cut = audit_tiles_catalog_197(bad_cut, allow_draft=False)
    assert rep_cut["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "ECHEC"
    assert any("M3b" in v for v in rep_cut["M3_INTEGRITE_PLATEAU_ET_ICONES"]["violations"])

    # Négatif M3c (non-Twist) : Gardien fluide qui saute d'icône
    bad_jump_fluid = copy.deepcopy(base)
    assert bad_jump_fluid["tuiles_ciblees"]["G1"]["est_twist"] is False
    bad_jump_fluid["tuiles_ciblees"]["G1"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Déplacez ce Gardien sur une autre icône de la Piste des Gardiens."
    )
    rep_jf = audit_tiles_catalog_197(bad_jump_fluid, allow_draft=False)
    assert rep_jf["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "ECHEC"
    assert any("non-Twist" in v for v in rep_jf["M3_INTEGRITE_PLATEAU_ET_ICONES"]["violations"])

    # Négatif M3c (> 1 Twist) : 2 Twists qui sautent d'icône dans le même panel
    bad_two_jumpers = copy.deepcopy(ok_m3)
    assert bad_two_jumpers["tuiles_ciblees"]["G3"]["est_twist"] is True
    bad_two_jumpers["tuiles_ciblees"]["G3"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Ce Gardien change d’icône vers une case libre après sa résolution."
    )
    rep_2j = audit_tiles_catalog_197(bad_two_jumpers, allow_draft=False)
    assert rep_2j["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"] == "ECHEC"
    assert any("> 1 tuiles" in v for v in rep_2j["M3_INTEGRITE_PLATEAU_ET_ICONES"]["violations"])


def test_m4_autonomie_plancher_solo_and_adjusted_i01() -> None:
    """M4 + I01 : interdit les prérequis bloquants inter-tuiles (même via jumelle Y>X), encourage entrees_synergie."""
    base = _make_complete_v6_3_fixture()
    assert audit_tiles_catalog_197(base, allow_draft=False)["verdict_global"] == "OK"

    # 1. M4 NÉGATIF : G2 (R>M) exige BLEU en `entrees_plancher` alors que sa jumelle G1 produit BLEU -> ÉCHEC M4 !
    bad_twin_block = copy.deepcopy(base)
    assert "BLEU" in bad_twin_block["tuiles_ciblees"]["G1"]["sorties"]
    bad_twin_block["tuiles_ciblees"]["G2"]["entrees_plancher"].append("BLEU")
    bad_twin_block["tuiles_ciblees"]["G2"]["entrees"].append("BLEU")
    rep_tb = audit_tiles_catalog_197(bad_twin_block, allow_draft=False)
    assert rep_tb["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"] == "ECHEC"
    assert any("G2" in v and "BLEU" in v for v in rep_tb["M4_AUTONOMIE_PLANCHER_SOLO"]["violations"])

    # 2. M4 POSITIF + I01 : G2 (R>M) garde son plancher solo et place BLEU en `entrees_synergie` (bonus Si… / OU) -> OK !
    ok_synergy = copy.deepcopy(base)
    ok_synergy["tuiles_ciblees"]["G2"]["entrees_synergie"].append("BLEU")
    ok_synergy["tuiles_ciblees"]["G2"]["entrees"].append("BLEU")
    ok_synergy["tuiles_ciblees"]["G2"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Ajoutez 1 jeton Sabotage au sac. Si une machine du rayon Mammifère porte un jeton bleu "
        "Surchauffe, ajoutez un 2e jeton Sabotage au sac."
    )
    rep_syn = audit_tiles_catalog_197(ok_synergy, allow_draft=False)
    assert rep_syn["verdict_global"] == "OK", rep_syn["errors"]
    assert any(
        d["tuile"] == "G2" and d["etat"] == "BLEU" and d["fourni_par_jumelle"] == "G1"
        for d in rep_syn["I01_cloture_elargie_197"]["synergies_jumelle_lisiere"]
    )

    # 3. M4 NÉGATIF : ALTEREE en plancher hors origine E (G8 = M>E) sans prélèvement en réserve -> ÉCHEC
    bad_alt = copy.deepcopy(base)
    bad_alt["tuiles_ciblees"]["G8"]["entrees_plancher"].append("ALTEREE")
    bad_alt["tuiles_ciblees"]["G8"]["entrees"].append("ALTEREE")
    rep_alt_bad = audit_tiles_catalog_197(bad_alt, allow_draft=False)
    assert rep_alt_bad["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"] == "ECHEC"

    # 4. M4 POSITIF : G8 (M>E) prélève explicitement dans la réserve de son voisin E -> VALIDE
    ok_alt_reserve = copy.deepcopy(bad_alt)
    ok_alt_reserve["tuiles_ciblees"]["G8"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Prenez 1 jeton d’Altération dans la réserve des Entités et posez-le sur une machine mobile."
    )
    rep_alt_ok = audit_tiles_catalog_197(ok_alt_reserve, allow_draft=False)
    assert rep_alt_ok["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"] == "OK", rep_alt_ok[
        "M4_AUTONOMIE_PLANCHER_SOLO"
    ]

    # 5. M4 NÉGATIF lexical : Face 1 bloquée uniquement sur un jeton bleu sans plancher ni OU
    bad_lex = copy.deepcopy(base)
    bad_lex["tuiles_ciblees"]["G8"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Si une machine porte un jeton bleu, faites-la reculer de 2 parcelles."
    )
    rep_lex = audit_tiles_catalog_197(bad_lex, allow_draft=False)
    assert rep_lex["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"] == "ECHEC"
    assert any("G8.face_1" in v for v in rep_lex["M4_AUTONOMIE_PLANCHER_SOLO"]["violations"])

    # 6. I01 NÉGATIF : synergie optionnelle orpheline (0/64 assises) ou Insecte hors lisières de I
    bad_orphan = copy.deepcopy(base)
    bad_orphan["tuiles_ciblees"]["G1"]["entrees_synergie"].append("ETAT_INEXISTANT")
    rep_orp = audit_tiles_catalog_197(bad_orphan, allow_draft=False)
    assert rep_orp["I01_cloture_elargie_197"]["verdict"] == "ECHEC"

    bad_ins_syn = copy.deepcopy(base)
    bad_ins_syn["tuiles_ciblees"]["G1"]["entrees_synergie"].append("INSECTE")
    bad_ins_syn["tuiles_ciblees"]["G1"]["entrees"].append("INSECTE")
    rep_ins = audit_tiles_catalog_197(bad_ins_syn, allow_draft=False)
    assert rep_ins["I01_cloture_elargie_197"]["verdict"] == "ECHEC"
    assert any("G1" in e for e in rep_ins["I01_cloture_elargie_197"]["insect_violations"])


def test_audit_197_structural_invariants_i02_i03_c01_q01() -> None:
    """Vérifie I02 (A=0), I03 (divergence), C01 (mem_debt) et Q01 (lois passives ≤ 2/assise)."""
    base = _make_complete_v6_3_fixture()

    # I02 : dépendance Gardien sur tuile A=0 (R2)
    bad_a0 = copy.deepcopy(base)
    bad_a0["tuiles_ciblees"]["R2"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Activez un Gardien voisin à l’ouverture."
    )
    rep_a0 = audit_tiles_catalog_197(bad_a0, allow_draft=False)
    assert rep_a0["verdict_global"] == "ECHEC"
    assert any("R2" in e for e in rep_a0["I02_autonomie_A0"]["violations"])

    # I03 : même sortie principale sur une lisière (G1 / G2)
    bad_div = copy.deepcopy(base)
    bad_div["tuiles_ciblees"]["G2"]["sorties"] = ["DEFENSEUR_REDEPLOYE"]
    rep_div = audit_tiles_catalog_197(bad_div, allow_draft=False)
    assert rep_div["verdict_global"] == "ECHEC"
    assert any("M–R" in e for e in rep_div["I03_divergence_lisiere"]["violations"])

    # C01 : modificateur flottant 'pour ce tour' rejeté
    bad_mem = copy.deepcopy(base)
    bad_mem["tuiles_ciblees"]["G3"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Les machines ont -1 au Seuil de Parade pour ce tour."
    )
    rep_mem = audit_tiles_catalog_197(bad_mem, allow_draft=False)
    assert rep_mem["verdict_global"] == "ECHEC"
    assert any("pour ce tour" in e for e in rep_mem["C01_mem_debt"]["mem_debt_hits"])

    # Q01 : > 2 lois passives sur une même assise
    bad_lois = copy.deepcopy(base)
    for sid in ("M1", "G13", "G14"):
        bad_lois["tuiles_ciblees"][sid]["nature"] = "LOI_PASSIVE"
        if "LOI_PASSIVE" not in bad_lois["tuiles_ciblees"][sid]["roles_portes"]:
            bad_lois["tuiles_ciblees"][sid]["roles_portes"].append("LOI_PASSIVE")
    rep_lois = audit_tiles_catalog_197(bad_lois, allow_draft=False)
    assert rep_lois["verdict_global"] == "ECHEC"
    assert rep_lois["Q01_lois_passives"]["max_par_assise"] > 2


def test_audit_panels_directory_compares_three_parallel_panels(tmp_path: Path) -> None:
    """Vérifie l'audit comparatif parallèle des 3 panels candidats (panel_1, panel_2, panel_3)."""
    p1 = _make_complete_v6_3_fixture(panel_id="panel_1")

    p2 = _make_complete_v6_3_fixture(panel_id="panel_2")
    p2["tuiles_ciblees"]["G7"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Retournez 1 Souche de votre rayon en Arbre debout."
    )
    p2["tuiles_ciblees"]["G6"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Posez 1 jeton bleu Surchauffe sur la machine ciblée."
    )

    p3 = _make_complete_v6_3_fixture(panel_id="panel_3")
    p3["tuiles_ciblees"]["G2"]["entrees_plancher"].append("BLEU")
    p3["tuiles_ciblees"]["G2"]["entrees"].append("BLEU")
    p3["tuiles_ciblees"]["G1"]["carte_joueur"]["texte_regle"]["face_1"] = (
        "Déplacez ce Gardien sur une autre icône de la Piste des Gardiens."
    )

    for name, payload in (("panel_1.json", p1), ("panel_2.json", p2), ("panel_3.json", p3)):
        (tmp_path / name).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

    batch = audit_panels_directory(tmp_path, allow_draft=False)
    assert batch["panels_count"] == 3
    assert batch["all_ok"] is False
    by_file = {row["file"]: row for row in batch["comparison"]}
    assert by_file["panel_1.json"]["verdict"] == "OK"
    assert by_file["panel_1.json"]["total_errors"] == 0
    assert by_file["panel_2.json"]["verdict"] == "ECHEC"
    assert by_file["panel_2.json"]["M1"] >= 1
    assert by_file["panel_2.json"]["M2"] >= 1
    assert by_file["panel_3.json"]["verdict"] == "ECHEC"
    assert by_file["panel_3.json"]["M3"] >= 1
    assert by_file["panel_3.json"]["M4"] >= 1


def test_v6_3_schema_contract_and_casting_guards() -> None:
    """Valide tiles_canon_v6_3.schema.json (6.3.1), le squelette initial et le casting animalier verrouillé."""
    schema = json.loads(V6_3_SCHEMA_PATH.read_text(encoding="utf-8"))
    assert schema["$schema"].startswith("https://json-schema.org/draft/2020-12")
    tile_props = schema["$defs"]["tile_v6_3"]["properties"]
    assert "tuile_plateau" in tile_props
    assert "carte_joueur" in tile_props
    assert "entrees_plancher" in tile_props
    assert "entrees_synergie" in tile_props

    scaffold = json.loads(V6_3_CONTRACT_PATH.read_text(encoding="utf-8"))
    assert is_v6_3_tiles_contract(scaffold) is True
    assert scaffold["_meta"]["schema_version"] == "6.3.1-draft"
    assert scaffold["_meta"]["murs_porteurs_verrouilles"] == list(MURS_PORTEURS_V6_3)
    assert validate_tiles_canon_v6_3(scaffold, strict=False) == []

    complete = _make_complete_v6_3_fixture()
    assert validate_tiles_canon_v6_3(complete, strict=True) == []

    # Rejet d'un chevauchement entrees_plancher / entrees_synergie
    bad_overlap = copy.deepcopy(complete)
    bad_overlap["tuiles_ciblees"]["G1"]["entrees_synergie"] = ["DEFENSEUR_ATTENTE"]
    errs_ov = validate_tiles_canon_v6_3(bad_overlap, strict=True)
    assert any("doivent être disjoints" in e for e in errs_ov)

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
    """Prouve la rétrocompatibilité transitoire du compilateur Studio avec le contrat v6.3.1."""
    rules = json.loads(RULES_CONTRACT_PATH.read_text(encoding="utf-8"))
    invariants = json.loads(INVARIANTS_CONTRACT_PATH.read_text(encoding="utf-8"))
    v63_doc = _make_complete_v6_3_fixture()
    v63_doc["tuiles_ciblees"]["G2"]["entrees_synergie"] = ["BLEU"]

    spec_f, catalog_doc, amazonia_js, adapted = compile_studio_payloads(
        rules, invariants, v63_doc, existing_changelog=[]
    )
    assert spec_f["architecture_reference"]["total_emplacements_synergie"] == 30
    assert catalog_doc["total_emplacements"] == 30
    assert "const CATALOGUE_TUILES =" in amazonia_js
    assert '"tuile_plateau":' in amazonia_js
    assert '"carte_joueur":' in amazonia_js
    assert '"entrees_plancher":' in amazonia_js
    assert '"entrees_synergie":' in amazonia_js
    assert '"Le Jaguar"' in amazonia_js
    assert "BLEU" in adapted["tuiles_ciblees"]["G2"]["profils"]["A"]["entrees"]

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
