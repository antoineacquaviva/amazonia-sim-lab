"""Génère data/spec_bundle_v5_4.json et engine/effects/mode3_reference.json depuis le Studio."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts_cloud.studio_paths import resolve_studio_dir

DATA_DIR = ROOT / "data"
DOCS_DATA_DIR = ROOT / "docs" / "data"
LOCK_FILE = DATA_DIR / "studio_lock.json"
SPEC_FILE = DOCS_DATA_DIR / "spec_formelle_v5_4.json"
CATALOG_FILE = DOCS_DATA_DIR / "catalog_v5_4.json"
OUT_BUNDLE = DATA_DIR / "spec_bundle_v5_4.json"
OUT_MODE3 = ROOT / "engine" / "effects" / "mode3_reference.json"

RES_VOCAB = frozenset(
    {
        "RES_INSECTE",
        "RES_PIEGE",
        "RES_DEFENSEUR",
        "RES_JETON_BLEU",
        "RES_JETON_ROUGE",
        "RES_APPRENTISSAGE",
        "RES_SEUIL_PARADE",
        "RES_DILUTION_SABOTAGE",
        "RES_SOUCHE",
        "RES_ARBRE",
        "RES_POSITION_MACHINE",
        "RES_POSITION_PISTE",
    }
)
TRIG_VOCAB = frozenset({f"TRIG_{i}" for i in range(1, 7)})


def _load_studio_js_objects() -> dict[str, Any]:
    studio_js_path = resolve_studio_dir(ROOT) / "data" / "amazonia_data_v5_4.js"
    if not studio_js_path.exists():
        raise FileNotFoundError(
            f"Fichier Studio introuvable : {studio_js_path} "
            "(définissez AMAZONIA_STUDIO_DIR ou placez amazonia-doc-studio à côté du dépôt)"
        )
    js_script = (
        "const fs = require('fs');\n"
        "const vm = require('vm');\n"
        "const ctx = { window: {} };\n"
        "vm.createContext(ctx);\n"
        f"const src = fs.readFileSync({json.dumps(studio_js_path.as_posix())}, 'utf8');\n"
        "const res = vm.runInContext("
        "src + '\\n;({ PEUPLES, MATRICE_PAIRES, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC, CATALOGUE_TUILES });', ctx);\n"
        "process.stdout.write(JSON.stringify(res));\n"
    )
    proc = subprocess.run(
        ["node", "-"],
        input=js_script,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return dict(json.loads(proc.stdout))


def _infer_economie_bot(slot: dict[str, Any], prof: dict[str, Any]) -> dict[str, Any]:
    """Dérive l'objet structuré economie_bot depuis primitive, tags, fenetre, cablage et texte."""
    primitive = str(prof.get("primitive", "")).upper()
    tags = {str(t).upper() for t in prof.get("tags", [])}
    fenetre = str(prof.get("fenetre", "")).upper()
    texte = str(prof.get("texte", "")).lower()
    cablage = prof.get("cablage") or []

    inputs: list[str] = []
    outputs: list[str] = []

    # Câblage sur déclencheurs 1..6 (ex: Gardiens)
    if isinstance(cablage, list):
        for trig_num in cablage:
            trig = f"TRIG_{trig_num}"
            if trig in TRIG_VOCAB and trig not in inputs:
                inputs.append(trig)

    # Analyse des coûts / inputs explicites dans le texte ou la primitive
    if "défauss" in texte or "retir" in texte or "coût" in primitive.lower() or "offrande" in primitive.lower():
        if "insecte" in texte and "RES_INSECTE" not in inputs:
            inputs.append("RES_INSECTE")
        if "piège" in texte and ("retir" in texte or "défauss" in texte) and "RES_PIEGE" not in inputs:
            inputs.append("RES_PIEGE")
        if "souche" in texte and ("retir" in texte or "sacrifi" in texte) and "RES_SOUCHE" not in inputs:
            inputs.append("RES_SOUCHE")
        if "arbre" in texte and ("sacrifi" in texte or "coup" in texte) and "RES_ARBRE" not in inputs:
            inputs.append("RES_ARBRE")
    # Précondition jeton rouge pour une conversion rouge -> bleu (Surchauffe)
    is_flip_red_to_blue = (
        "rouge" in texte
        and ("bleu" in texte or "surchauffe" in texte)
        and ("retourn" in texte or "face bleue" in texte)
    )
    if is_flip_red_to_blue and "RES_JETON_ROUGE" not in inputs:
        inputs.append("RES_JETON_ROUGE")

    # Analyse des productions / outputs
    creates_insect = (
        "CREATION_ENTITE (INSECTE)" in primitive
        or "création de jetons insecte" in texte
        or "créez 1 insecte" in texte
        or "créez un insecte" in texte
        or "ajoutez 1 insecte" in texte
        or "placez 1 insecte" in texte
        or "posez 1 insecte" in texte
        or "placez immédiatement 1 insecte" in texte
    )
    if creates_insect:
        outputs.append("RES_INSECTE")
        if "sans allumer la case 6" not in texte:
            outputs.append("TRIG_6")
    elif "allume la case 6" in texte:
        outputs.append("TRIG_6")

    if "PIEGE" in primitive or "piège" in texte:
        if (
            "CREATION_ENTITE (PIEGE)" in primitive
            or ("CREATION_ENTITE" in primitive and "PIEGE" in primitive)
            or "glissez" in texte
            or "posez" in texte
            or "placez" in texte
        ):
            outputs.append("RES_PIEGE")
        if (
            ("ARMEMENT" in tags or "embuscade" in texte or "allume la case 2" in texte)
            and "sans allumer la case 2" not in texte
        ):
            outputs.append("TRIG_2")

    if "SABOTAGE" in primitive or "SABOTAGE" in tags or "sabotage" in texte:
        outputs.append("RES_DILUTION_SABOTAGE")
        if "sans allumer la case 3" not in texte and "sans allumer" not in texte:
            outputs.append("TRIG_3")

    if "BLEU" in primitive or "SURCHAUFFE" in tags or "bleu" in texte:
        outputs.append("RES_JETON_BLEU")

    # RES_JETON_ROUGE en sortie = retrait / blocage / neutralisation directe de jetons rouges
    # (distinct de la simple conversion rouge -> bleu déjà portée par RES_JETON_BLEU + input RES_JETON_ROUGE)
    removes_or_blocks_red = "rouge" in texte and (
        "retire" in texte
        or "retirez" in texte
        or "ignorez" in texte
        or "ne gagne" in texte
        or "ne gagnent" in texte
    )
    if removes_or_blocks_red:
        outputs.append("RES_JETON_ROUGE")

    if "APPRENTISSAGE" in primitive or "APPRENTISSAGE" in tags or "apprentissage" in texte:
        outputs.append("RES_APPRENTISSAGE")
    if "MOD_SEUIL" in primitive or "seuil" in texte or "PARADE" in " ".join(tags):
        outputs.append("RES_SEUIL_PARADE")
        outputs.append("TRIG_1")
    if "DEFENSEUR" in primitive or "FURTIVITE" in tags or "défenseur" in texte:
        outputs.append("RES_DEFENSEUR")
    if "SOUCHE" in primitive or "SOUCHES" in tags or "souche" in texte:
        outputs.append("RES_SOUCHE")
    if "REPOUSSE" in tags or "arbre" in texte:
        outputs.append("RES_ARBRE")
    if "DEPLACEMENT (MACHINE)" in primitive or "RECUL" in tags or "recul" in texte or "avanc" in texte:
        outputs.append("RES_POSITION_MACHINE")
    if "PERMUTATION_PISTE" in primitive or "AVANCEE_REVE" in tags or "MIGRATION" in tags or "rêve" in texte:
        outputs.append("RES_POSITION_PISTE")
    if "RESONANCE" in tags or "REACTIVER_GARDIEN" in primitive or "PARTAGE_INFO" in primitive:
        outputs.append("TRIG_4")
    if "REVE" in str(slot.get("famille", "")) or "AVANCEE_REVE" in tags:
        outputs.append("TRIG_5")

    # Fallback garanti non-vide pour outputs_produits
    if not outputs:
        outputs.append("RES_SEUIL_PARADE")

    # Déduplication préservant l'ordre
    inputs = list(dict.fromkeys(inputs))
    outputs = list(dict.fromkeys(outputs))

    # Rôle sémantique
    if "MOD_LOI_DU_COEUR" in primitive or "LOI" in fenetre:
        role = "MODULATEUR"
    elif "CREATION_ENTITE" in primitive:
        role = "PRODUCTEUR"
    elif "PERMUTATION_PISTE" in primitive or "DEPLACEMENT" in primitive:
        role = "CONTROLE"
    elif "PARTAGE_INFO" in primitive:
        role = "CATALYSEUR"
    else:
        role = "CONSOMMATEUR" if inputs else "MODULATEUR"

    # Portée
    if "global" in texte or "toutes" in texte or "tous les" in texte or "piste" in texte or "MIGRATION" in tags:
        portee = "GLOBAL_PLATEAU"
    elif "PERMUTATION_PISTE" in primitive or "TACTIQUE" in primitive or "REVE" in str(slot.get("famille", "")):
        portee = "PISTE_TACTIQUES"
    elif "lisière" in texte or "adjacent" in texte or "voisin" in texte:
        portee = "LISIERES_ADJACENTES"
    else:
        portee = "LOCAL_RAYON"

    return {
        "role": role,
        "inputs_requis": inputs,
        "outputs_produits": outputs,
        "portee": portee,
    }


def _build_tactiques() -> list[dict[str, Any]]:
    return [
        {
            "id": "T1",
            "nom": "Sur place",
            "cibles": ["SUR_PLACE"],
            "avancee": 0,
            "gain_rouge": 0,
            "mod_seuil": 0,
            "est_ratissage_profil": True,
        },
        {
            "id": "T2",
            "nom": "Devant",
            "cibles": ["DEVANT"],
            "avancee": 0,
            "gain_rouge": 0,
            "mod_seuil": 0,
            "est_ratissage_profil": False,
        },
        {
            "id": "T3",
            "nom": "En avançant",
            "cibles": ["SUR_PLACE", "DEVANT"],
            "avancee": 1,
            "gain_rouge": 0,
            "mod_seuil": -1,
            "est_ratissage_profil": False,
        },
        {
            "id": "T4",
            "nom": "Sur place +",
            "cibles": ["SUR_PLACE"],
            "avancee": 0,
            "gain_rouge": 1,
            "mod_seuil": -1,
            "est_ratissage_profil": False,
        },
        {
            "id": "T5",
            "nom": "Devant +",
            "cibles": ["DEVANT"],
            "avancee": 0,
            "gain_rouge": 1,
            "mod_seuil": -1,
            "est_ratissage_profil": False,
        },
        {
            "id": "T6",
            "nom": "En avançant +",
            "cibles": ["SUR_PLACE", "DEVANT"],
            "avancee": 1,
            "gain_rouge": 1,
            "mod_seuil": -2,
            "est_ratissage_profil": False,
        },
    ]


def _score_mode3_profile(prof_key: str, prof: dict[str, Any]) -> tuple[int, list[str]]:
    """Plus le score est bas, plus le profil est épuré pour Mode 3."""
    score = 0
    reasons: list[str] = []
    tags = {str(t).upper() for t in prof.get("tags", [])}
    fenetre = str(prof.get("fenetre", "")).upper()
    primitive = str(prof.get("primitive", "")).upper()
    texte = str(prof.get("texte", "")).lower()

    # Critère 1 : zéro modification de l'ordre d'attaque ou du secret des paravents
    if "ORDRE_MACHINES" in tags or "INVERSION_ETAPE_5_1_ET_5_2" in primitive:
        score += 1000
        reasons.append("modifie l'ordre d'attaque")
    if "INFORMATION" in tags or "paravent" in texte or "LOI 2.1" in fenetre or "PARTAGE_INFO" in primitive:
        score += 900
        reasons.append("modifie le secret des paravents / information")

    # Critère 2 : minimum de dette mémorielle
    if "->" in fenetre or "TEMP" in fenetre:
        score += 200
        reasons.append("modificateur transitoire multi-sous-étapes")
    elif "LOI" in fenetre or "MOD_LOI_DU_COEUR" in primitive:
        score += 100
        reasons.append("loi persistante à surveiller")

    # Critère 3 : effet local borné
    if "global" in texte or "toutes" in texte or "tous les" in texte:
        score += 30
        reasons.append("portée globale")

    # Préférence légère pour A à qualité égale
    order_tiebreak = {"A": 0, "B": 1, "C": 2, "D": 3}.get(prof_key, 9)
    return score * 10 + order_tiebreak, reasons


def _build_mode3_reference(catalogue: dict[str, Any]) -> dict[str, Any]:
    selections: dict[str, Any] = {}
    kept_a_count = 0
    replaced_a: list[dict[str, str]] = []

    for slot_id, slot in catalogue.items():
        famille = slot.get("famille", "")
        profils: dict[str, dict[str, Any]] = slot.get("profils", {})

        if famille == "MIGRATION":
            if slot_id == "SLOT_BUG_CERVEAU":
                chosen_key = "B"
                rationale = (
                    "Profil B actif par défaut depuis v5.4.2 "
                    "(Déviation Synaptique en 3.2, Apprentissage supprimé)."
                )
                replaced_a.append({"slot": slot_id, "chosen": chosen_key, "reason": rationale})
            else:
                chosen_key = "A"
                rationale = "Migration fixée à A selon la référence Mode 3."
                kept_a_count += 1
        else:
            scored = []
            for pk, p in profils.items():
                sc, rs = _score_mode3_profile(pk, p)
                scored.append((sc, pk, rs))
            scored.sort()
            _, chosen_key, chosen_reasons = scored[0]
            _, a_reasons = _score_mode3_profile("A", profils["A"]) if "A" in profils else (0, [])
            if chosen_key == "A":
                kept_a_count += 1
                rationale = "Profil A retenu (conforme sans dette ni atteinte au secret/ordre)."
            else:
                reason_str = ", ".join(a_reasons) if a_reasons else "dette supérieure"
                rationale = f"Profil A écarté ({reason_str}) ; {chosen_key} retenu ({', '.join(chosen_reasons) or 'effet local borné'})."
                replaced_a.append({"slot": slot_id, "chosen": chosen_key, "reason": rationale})

        selections[slot_id] = {
            "famille": famille,
            "peuple_origine": slot.get("peuple_origine"),
            "profile": chosen_key,
            "nom": profils[chosen_key]["nom"],
            "kept_A": chosen_key == "A",
            "rationale": rationale,
        }

    return {
        "schema_version": "5.4.0",
        "description": "Sélection de référence Mode 3 (1 profil épuré par emplacement, Migrations A/A).",
        "criteres_priorite": [
            "1. Zéro modification de l'ordre d'attaque ou du secret des paravents",
            "2. Minimum de dette mémorielle (zéro TransientModifier multi-sous-étapes si évitable)",
            "3. Effet local borné (préférence A à égalité)",
        ],
        "stats": {
            "total_emplacements": len(selections),
            "kept_A": kept_a_count,
            "replaced_A": len(replaced_a),
        },
        "ecarts_A": replaced_a,
        "selections": selections,
    }


def _file_lock_entry(path: Path) -> dict[str, object]:
    raw_bytes = path.read_bytes()
    resolved = path.resolve()
    try:
        src_label = resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        src_label = resolved.as_posix()
    return {
        "sha256": hashlib.sha256(raw_bytes).hexdigest(),
        "bytes": len(raw_bytes),
        "source": src_label,
    }


def build_bundle() -> None:
    studio_js_path = resolve_studio_dir(ROOT) / "data" / "amazonia_data_v5_4.js"
    studio_js = _load_studio_js_objects()
    spec_data = json.loads(SPEC_FILE.read_text(encoding="utf-8"))
    catalog_meta = json.loads(CATALOG_FILE.read_text(encoding="utf-8"))
    studio_sha256 = {
        "catalog_v5_4.json": _file_lock_entry(CATALOG_FILE),
        "spec_formelle_v5_4.json": _file_lock_entry(SPEC_FILE),
        "amazonia_data_v5_4.js": _file_lock_entry(studio_js_path),
    }

    catalogue = studio_js["CATALOGUE_TUILES"]
    for slot in catalogue.values():
        for prof in slot["profils"].values():
            prof["economie_bot"] = _infer_economie_bot(slot, prof)

    bundle = {
        "meta": {
            "schema_version": "5.4.0",
            "source_studio_version": "v5.4",
            "studio_sha256": studio_sha256,
            "total_emplacements": len(catalogue),
            "total_profils": sum(len(s["profils"]) for s in catalogue.values()),
        },
        "peuples": studio_js["PEUPLES"],
        "matrice_paires": studio_js["MATRICE_PAIRES"],
        "chassis_axes": studio_js["CHASSIS_AXES_SPEC"],
        "topologies": {
            "validees": spec_data["architecture_reference"]["topologies_validees"],
            "details_seuil_et_dotation": catalog_meta["topologies"],
            "reserves_materiel": spec_data["architecture_reference"]["reserves_materiel"],
            "plafond_repousse_parcelle": spec_data["architecture_reference"]["plafond_repousse_parcelle"],
        },
        "tactiques": _build_tactiques(),
        "machine_damage_rules": {
            "ABATTEUSE": {
                "arbres_coupes_max": 2,
                "souches_retirees": 0,
                "arrache_1_souche_si_sans_arbre_en_ratissage_option": "ARRACHE_1_SOUCHE_SI_SANS_ARBRE",
            },
            "BULLDOZER": {
                "arbres_coupes_max": 1,
                "retire_toutes_souches_non_protegees": True,
                "test_parade_unique": True,
            },
            "ratissage": {
                "pion_double_face": True,
                "bonus_puissance_imprime": 1,
                "traite_comme_jeton_rouge_a_tous_egards": True,
                "conserve_jetons_puissance_anterieurs": True,
                "tactique_imprimee": "T1",
                "piste_tactiques_fixe": True,
                "entree_definitive_derniere_parcelle": True,
            },
        },
        "machine_deck_rules": {
            "cartes_machine_par_rayon": 2,
            "types_par_rayon": ["ABATTEUSE", "BULLDOZER"],
            "total_initial_formula": "2 * N",
            "sabotage_dilution_permanente": True,
            "sabotage_effet_propre": None,
            "sabotage_perd_activation_et_pas_de_des": True,
            "remelange_etape": "6.3",
            "penurie_ordre": "sens_horaire_depuis_plus_arbres_debout",
        },
        "spec_formelle_v5_4": spec_data,
        "catalogue_tuiles": catalogue,
    }

    OUT_BUNDLE.write_text(
        json.dumps(bundle, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(f"Wrote {OUT_BUNDLE.relative_to(ROOT).as_posix()} ({bundle['meta']['total_emplacements']} slots, {bundle['meta']['total_profils']} profils)")

    if OUT_MODE3.exists():
        mode3 = _build_mode3_reference(catalogue)
        OUT_MODE3.write_text(
            json.dumps(mode3, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        print(
            f"Wrote {OUT_MODE3.relative_to(ROOT).as_posix()} "
            f"(kept_A={mode3['stats']['kept_A']}, replaced_A={mode3['stats']['replaced_A']})"
        )
    else:
        print("Skipped mode3_reference.json (Phase CORE_STABILIZATION : stock 100 tuiles archivé)")


if __name__ == "__main__":
    build_bundle()
