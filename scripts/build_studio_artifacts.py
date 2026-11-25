"""Compilateur dérivé unique (SSOT v6.2) pour Amazonia Doc Studio & simulateur.

Lit exclusivement les 3 contrats SSOT de `contracts/` :
- `contracts/rules_canon_v6_2.json`
- `contracts/physical_and_edge_invariants.json`
- `contracts/tiles_canon_v6_2.json`

Génère sans aucune constante métier codée en dur :
1. `docs/data/spec_formelle_v6_0.json`
2. `docs/data/catalog_v6_0.json`
3. `docs/data/amazonia_data_v6_0.js` (validé par `new vm.Script()` sous Node)
4. `data/catalog_v6_0.json` et `data/spec_formelle_v6_0.json`
5. `data/studio_lock.json`
6. `data/spec_bundle_v6_0.json` (avec shim de compatibilité minimal jusqu'au Chantier 4)
"""

from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
CONTRACTS_DIR = ROOT / "contracts"
DOCS_DATA_DIR = ROOT / "docs" / "data"
DATA_DIR = ROOT / "data"

RULES_CONTRACT_PATH = CONTRACTS_DIR / "rules_canon_v6_2.json"
INVARIANTS_CONTRACT_PATH = CONTRACTS_DIR / "physical_and_edge_invariants.json"
TILES_CONTRACT_PATH = CONTRACTS_DIR / "tiles_canon_v6_2.json"

OUT_DOCS_SPEC = DOCS_DATA_DIR / "spec_formelle_v6_0.json"
OUT_DOCS_CATALOG = DOCS_DATA_DIR / "catalog_v6_0.json"
OUT_DOCS_JS = DOCS_DATA_DIR / "amazonia_data_v6_0.js"
DOCS_LIVRET_JS = DOCS_DATA_DIR / "livret_v6_0.js"

OUT_DATA_SPEC = DATA_DIR / "spec_formelle_v6_0.json"
OUT_DATA_CATALOG = DATA_DIR / "catalog_v6_0.json"
OUT_STUDIO_LOCK = DATA_DIR / "studio_lock.json"
OUT_SPEC_BUNDLE = DATA_DIR / "spec_bundle_v6_0.json"

RES_VOCAB: frozenset[str] = frozenset(
    {
        "RES_INSECTE",
        "RES_PIEGE",
        "RES_DEFENSEUR",
        "RES_JETON_BLEU",
        "RES_JETON_ROUGE",
        "RES_SEUIL_PARADE",
        "RES_DILUTION_SABOTAGE",
        "RES_SOUCHE",
        "RES_ARBRE",
        "RES_POSITION_MACHINE",
        "RES_POSITION_PISTE",
    }
)
TRIG_VOCAB: frozenset[str] = frozenset({f"TRIG_{i}" for i in range(1, 7)})

_CANON_TOKEN_TO_RES: dict[str, str] = {
    "INSECTE": "RES_INSECTE",
    "INSECTE_PASSAGER": "RES_INSECTE",
    "INSECTE_RANG": "RES_INSECTE",
    "NID": "RES_INSECTE",
    "NID_ACTIVE": "RES_INSECTE",
    "PIEGE": "RES_PIEGE",
    "CROC": "RES_PIEGE",
    "DEFENSEUR_ATTENTE": "RES_DEFENSEUR",
    "DEFENSEUR_REDEPLOYE": "RES_DEFENSEUR",
    "BLEU": "RES_JETON_BLEU",
    "ROUGE": "RES_JETON_ROUGE",
    "DUEL": "RES_SEUIL_PARADE",
    "TERRITOIRE": "RES_SEUIL_PARADE",
    "TAMBOUR": "RES_SEUIL_PARADE",
    "SABOTAGE": "RES_DILUTION_SABOTAGE",
    "ECAILLE": "RES_DILUTION_SABOTAGE",
    "SOUCHE": "RES_SOUCHE",
    "ALTEREE": "RES_POSITION_MACHINE",
    "RECUL": "RES_POSITION_MACHINE",
    "CALE": "RES_POSITION_MACHINE",
    "RANG_MACHINE": "RES_POSITION_MACHINE",
    "POSITION_REVE": "RES_POSITION_PISTE",
    "RANG_REVE": "RES_POSITION_PISTE",
    "ANNULATION": "RES_POSITION_PISTE",
}


def _write_text_lf(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    _write_text_lf(path, json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


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


def _extract_existing_changelog(js_path: Path) -> list[dict[str, Any]]:
    """Extrait VERSION_CHANGELOG existant depuis docs/data/amazonia_data_v6_0.js via Node vm."""
    if not js_path.is_file():
        return []
    js_script = (
        "const fs = require('fs');\n"
        "const vm = require('vm');\n"
        "const ctx = { window: {} };\n"
        "vm.createContext(ctx);\n"
        f"const src = fs.readFileSync({json.dumps(js_path.as_posix())}, 'utf8');\n"
        "const res = vm.runInContext(src + '\\n;(typeof VERSION_CHANGELOG !== \"undefined\" ? VERSION_CHANGELOG : []);', ctx);\n"
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
    loaded = json.loads(proc.stdout)
    return list(loaded) if isinstance(loaded, list) else []


def _validate_js_syntax(js_source: str, label: str) -> None:
    """Valide une source JS via `new vm.Script()` dans Node."""
    js_script = (
        "const vm = require('vm');\n"
        "let src = '';\n"
        "process.stdin.setEncoding('utf8');\n"
        "process.stdin.on('data', chunk => { src += chunk; });\n"
        "process.stdin.on('end', () => {\n"
        f"  new vm.Script(src, {{ filename: {json.dumps(label)} }});\n"
        "  const ctx = { window: {} };\n"
        "  vm.createContext(ctx);\n"
        "  vm.runInContext(src, ctx);\n"
        "});\n"
    )
    proc = subprocess.run(
        ["node", "-e", js_script],
        input=js_source,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Validation Node vm.Script échouée pour {label} :\n{proc.stderr}")


def derive_economie_bot(
    slot: dict[str, Any],
    prof: dict[str, Any],
    trigger_codes: dict[str, int] | None = None,
) -> dict[str, Any]:
    """Dérive le graphe orienté `economie_bot` depuis les champs typés du Canon 0."""
    famille = str(slot.get("famille", "")).upper()
    primitive = str(prof.get("primitive", "")).upper()
    fenetre = str(prof.get("fenetre", "")).upper()
    nature = str(prof.get("nature", "")).lower()
    tags = {str(t).upper() for t in prof.get("tags", [])}
    entrees = [str(x).upper() for x in (prof.get("entrees") or [])]
    sorties = [str(x).upper() for x in (prof.get("sorties") or [])]
    cablage = prof.get("cablage") or []
    declencheurs_amorces = prof.get("declencheurs_amorces") or []
    texte_lower = str(prof.get("texte", "")).lower()
    codes = trigger_codes or {"REVE": 4, "RESONANCE": 6}
    trig_reve = f"TRIG_{int(codes.get('REVE', 4))}"
    trig_resonance = f"TRIG_{int(codes.get('RESONANCE', 6))}"

    inputs: list[str] = []
    outputs: list[str] = []

    if isinstance(cablage, list):
        for trig_num in cablage:
            tok = f"TRIG_{int(trig_num)}"
            if tok in TRIG_VOCAB:
                inputs.append(tok)

    for raw_in in entrees:
        mapped = _CANON_TOKEN_TO_RES.get(raw_in)
        if mapped in RES_VOCAB:
            inputs.append(mapped)

    for raw_out in sorties:
        mapped = _CANON_TOKEN_TO_RES.get(raw_out)
        if mapped in RES_VOCAB:
            outputs.append(mapped)
        elif raw_out == "PARI_GLISSE" and trig_resonance in TRIG_VOCAB:
            outputs.append(trig_resonance)

    if "REPOUSSE_FINALE" in tags or "enraciné" in texte_lower and "arbre debout" in texte_lower:
        outputs.append("RES_ARBRE")

    if "SABOTAGE" in tags or "ECAILLE" in tags:
        outputs.append("RES_DILUTION_SABOTAGE")

    _icon_to_trig = {
        "ICONE_PARADE": "TRIG_1",
        "ICONE_PIEGEAGE": "TRIG_2",
        "ICONE_SABOTAGE": "TRIG_3",
        "ICONE_REVE": trig_reve,
        "ICONE_INSECTE": f"TRIG_{int(codes.get('INSECTE', 5))}",
        "ICONE_RESONANCE": trig_resonance,
    }
    if isinstance(declencheurs_amorces, list):
        for raw_trig in declencheurs_amorces:
            if isinstance(raw_trig, str):
                tok = _icon_to_trig.get(raw_trig.strip().upper(), "")
            else:
                tok = f"TRIG_{int(raw_trig)}"
            if tok in TRIG_VOCAB:
                outputs.append(tok)

    if famille == "REVE" and trig_reve in TRIG_VOCAB:
        outputs.append(trig_reve)

    if not outputs:
        outputs.append("RES_SEUIL_PARADE")

    inputs = list(dict.fromkeys(inputs))
    outputs = list(dict.fromkeys(outputs))

    # Rôle sémantique dérivé de nature / primitive / tags
    if nature == "loi_passive" or "MOD_LOI_DU_COEUR" in primitive or "LOI" in fenetre:
        role = "MODULATEUR"
    elif "CATALYSEUR_EVEIL" in tags and "PARI_GLISSE" in sorties:
        role = "CATALYSEUR"
    elif "CREATION_ENTITE" in primitive or "AJOUT_SABOTAGE" in primitive or "ECAILLE" in sorties:
        role = "PRODUCTEUR"
    elif (
        "DEPLACEMENT" in primitive
        or "GLISSEMENT" in primitive
        or "PERMUTATION" in primitive
        or "RECUL" in sorties
        or "RANG_REVE" in sorties
        or "RANG_MACHINE" in sorties
    ):
        role = "CONTROLE"
    else:
        role = "CONSOMMATEUR" if any(t.startswith("RES_") for t in inputs) else "MODULATEUR"

    # Portée
    if "toute la roue" in texte_lower or "n’importe quel" in texte_lower or "n'importe quel" in texte_lower:
        portee = "GLOBAL_PLATEAU"
    elif famille == "REVE" or "RANG_REVE" in sorties or "RANG_MACHINE" in sorties:
        portee = "PISTE_TACTIQUES"
    elif "voisin" in texte_lower or "lisière" in texte_lower or "des mammifères ou des reptiles" in texte_lower:
        portee = "LISIERES_ADJACENTES"
    else:
        portee = "LOCAL_RAYON"

    return {
        "role": role,
        "inputs_requis": inputs,
        "outputs_produits": outputs,
        "portee": portee,
    }


def _build_spec_formelle(
    rules: dict[str, Any],
    invariants: dict[str, Any],
    tiles: dict[str, Any],
) -> dict[str, Any]:
    meta = rules["meta"]
    chassis = rules["chassis_canonique"]
    topos_studio = rules["topologies_studio"]
    sf_src = rules["spec_formelle_v6_2"]
    tuiles = tiles["tuiles_ciblees"]

    total_slots = len(tuiles)
    total_profiles = sum(len(slot["profils"]) for slot in tuiles.values())
    mat_arbres = rules["materiel_fini_reversible"]["arbres_et_souches"]

    return {
        "schema_version": str(meta["schema_version"]),
        "date_consolidation": str(meta["date_consolidation"]),
        "architecture_reference": {
            "total_emplacements_synergie": total_slots,
            "total_profils": total_profiles,
            "topologies_validees": {
                code: list(spec["dotation"]) for code, spec in topos_studio.items()
            },
            "reserves_materiel": (
                f"finie ({mat_arbres['dotation_formule']} pions uniques recto-verso "
                f"{mat_arbres['recto']}/{mat_arbres['verso']} ; sac opaque de jetons)"
            ),
            "plafond_repousse_parcelle": "dotation_initiale_arbres_physique",
            "repousse_finale_base": int(chassis["repousse_finale_base"]),
            "enracinement_volontaire": dict(rules["enracinement_volontaire"]["calibrage"]),
            "score_final": "arbres_debout_apres_enracinement_volontaire",
        },
        "architecture_modulaire": copy.deepcopy(rules["architecture_modulaire"]),
        "principes_transverses": copy.deepcopy(sf_src["principes_transverses"]),
        "etapes_tour": copy.deepcopy(sf_src["etapes_tour"]),
        "step_arbitrages_map": copy.deepcopy(sf_src["step_arbitrages_map"]),
        "arbitrages_valides": copy.deepcopy(sf_src["arbitrages_valides"]),
        "invariants_physiques_ids": [str(inv["id"]) for inv in invariants["invariants"]],
    }


def _build_catalog_json(
    rules: dict[str, Any],
    spec_formelle: dict[str, Any],
    tiles: dict[str, Any],
) -> dict[str, Any]:
    meta = rules["meta"]
    chassis = rules["chassis_canonique"]
    arb = spec_formelle["arbitrages_valides"]
    tuiles = tiles["tuiles_ciblees"]

    topos_out: dict[str, Any] = {}
    for code, spec in rules["topologies_studio"].items():
        topos_out[code] = {
            "P_Max": int(spec["p_max"]),
            "seuil_imprime_et_dotation": list(spec["dotation"]),
            "arbres_par_joueur": int(spec["arbres_par_rayon"]),
        }

    return {
        "schema_version": str(meta["schema_version"]),
        "date_consolidation": str(meta["date_consolidation"]),
        "total_emplacements": len(tuiles),
        "total_profils": sum(len(s["profils"]) for s in tuiles.values()),
        "topologies": topos_out,
        "formule_seuil_parade": str(arb["A23"]),
        "verification_fin_de_partie": str(arb["A15"]),
        "regle_piege": str(arb["A06"]),
        "bonus_constructeur_n3": int(chassis["bonus_constructeur_n3"]),
        "regle_furtivite": str(arb["A03"]),
        "gouvernance_autorite": str(arb["A04"]),
        "spec_formelle": copy.deepcopy(spec_formelle),
    }


def _build_amazonia_js(
    rules: dict[str, Any],
    invariants: dict[str, Any],
    tiles: dict[str, Any],
    spec_formelle: dict[str, Any],
    existing_changelog: list[dict[str, Any]],
) -> str:
    meta = rules["meta"]
    changelog_v6_2 = copy.deepcopy(rules["changelog_v6_2"])
    v62_ver = str(changelog_v6_2["version"])
    merged_changelog = [changelog_v6_2] + [
        block for block in existing_changelog if str(block.get("version", "")) != v62_ver
    ]

    catalogue_js = copy.deepcopy(tiles["tuiles_ciblees"])
    essaim_natives = copy.deepcopy(
        rules["architecture_modulaire"]["modules"]["module_essaim"]["regles_natives"]
    )
    invariants_list = copy.deepcopy(invariants["invariants"])

    sections = [
        "// =========================================================================",
        (
            f"// data/amazonia_data_v6_0.js — Généré automatiquement depuis contracts/ "
            f"(SSOT v{meta['schema_version']} · {len(catalogue_js)} tuiles Canon 0 · Châssis unique verrouillé)"
        ),
        "// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.",
        "// =========================================================================",
        f"const PEUPLES = {json.dumps(rules['peuples'], indent=2, ensure_ascii=False)};",
        "",
        f"const MATRICE_PAIRES = {json.dumps(rules['matrice_paires'], indent=2, ensure_ascii=False)};",
        "",
        f"const TOPOLOGIES_PISTE_SPEC = {json.dumps(rules['topologies_studio'], indent=2, ensure_ascii=False)};",
        "",
        f"const CHASSIS_AXES_SPEC = {json.dumps(rules['chassis_axes_studio'], indent=2, ensure_ascii=False)};",
        "",
        f"const MODULE_ESSAIM_REGLES_NATIVES = {json.dumps(essaim_natives, indent=2, ensure_ascii=False)};",
        "",
        f"const PHYSICAL_INVARIANTS_V6_2 = {json.dumps(invariants_list, indent=2, ensure_ascii=False)};",
        "",
        f"const CATALOGUE_TUILES = {json.dumps(catalogue_js, indent=2, ensure_ascii=False)};",
        "",
        f"const VERSION_CHANGELOG = {json.dumps(merged_changelog, indent=2, ensure_ascii=False)};",
        "",
        f"const SPEC_FORMELLE_V6_0 = {json.dumps(spec_formelle, indent=2, ensure_ascii=False)};",
        "",
    ]
    return "\n".join(sections)


def compile_studio_payloads(
    rules: dict[str, Any],
    invariants: dict[str, Any],
    tiles: dict[str, Any],
    existing_changelog: list[dict[str, Any]],
) -> tuple[dict[str, Any], dict[str, Any], str, dict[str, Any]]:
    """Compile en mémoire `(spec_formelle, catalog_doc, amazonia_js, adapted_tiles)` pour v6.2 ou v6.3."""
    from scripts.tiles_v6_3_schema import adapt_tiles_contract_for_studio

    adapted_tiles = adapt_tiles_contract_for_studio(tiles)
    spec_formelle = _build_spec_formelle(rules, invariants, adapted_tiles)
    catalog_doc = _build_catalog_json(rules, spec_formelle, adapted_tiles)
    amazonia_js = _build_amazonia_js(
        rules, invariants, adapted_tiles, spec_formelle, existing_changelog
    )
    _validate_js_syntax(amazonia_js, "docs/data/amazonia_data_v6_0.js")
    return spec_formelle, catalog_doc, amazonia_js, adapted_tiles


def build_all_artifacts(tiles_contract_path: Path | None = None) -> dict[str, Any]:
    """Compile l'ensemble des artefacts dérivés depuis les 3 contrats SSOT de `contracts/`.

    Accepte un `tiles_contract_path` optionnel (par défaut `contracts/tiles_canon_v6_2.json`,
    compatible de manière transparente avec le schéma bi-composant `tiles_canon_v6_3.json`).
    """
    active_tiles_path = tiles_contract_path or TILES_CONTRACT_PATH
    for req in (RULES_CONTRACT_PATH, INVARIANTS_CONTRACT_PATH, active_tiles_path):
        if not req.is_file():
            raise FileNotFoundError(f"Contrat SSOT manquant : {req}")

    rules: dict[str, Any] = json.loads(RULES_CONTRACT_PATH.read_text(encoding="utf-8"))
    invariants: dict[str, Any] = json.loads(INVARIANTS_CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_tiles: dict[str, Any] = json.loads(active_tiles_path.read_text(encoding="utf-8"))

    existing_changelog = _extract_existing_changelog(OUT_DOCS_JS)
    spec_formelle, catalog_doc, amazonia_js, tiles = compile_studio_payloads(
        rules, invariants, raw_tiles, existing_changelog
    )

    # 1. Écriture des artefacts Studio (docs/data/)
    _write_json(OUT_DOCS_SPEC, spec_formelle)
    _write_json(OUT_DOCS_CATALOG, catalog_doc)
    _write_text_lf(OUT_DOCS_JS, amazonia_js)

    # 2. Miroirs data/ et verrou SHA-256 data/studio_lock.json
    _write_json(OUT_DATA_SPEC, spec_formelle)
    _write_json(OUT_DATA_CATALOG, catalog_doc)

    studio_sha256: dict[str, dict[str, object]] = {
        "catalog_v6_0.json": _file_lock_entry(OUT_DOCS_CATALOG),
        "spec_formelle_v6_0.json": _file_lock_entry(OUT_DOCS_SPEC),
        "amazonia_data_v6_0.js": _file_lock_entry(OUT_DOCS_JS),
        "livret_v6_0.js": _file_lock_entry(DOCS_LIVRET_JS),
    }
    contracts_sha256: dict[str, dict[str, object]] = {
        "rules_canon_v6_2.json": _file_lock_entry(RULES_CONTRACT_PATH),
        "physical_and_edge_invariants.json": _file_lock_entry(INVARIANTS_CONTRACT_PATH),
        active_tiles_path.name: _file_lock_entry(active_tiles_path),
    }

    lock_payload: dict[str, Any] = {
        "studio_version": "v6.2",
        "schema_version": str(rules["meta"]["schema_version"]),
        "files": studio_sha256,
        "contracts": contracts_sha256,
    }
    _write_json(OUT_STUDIO_LOCK, lock_payload)

    # 3. Construction de data/spec_bundle_v6_0.json (dérivé SSOT + shim de compatibilité Chantier 1)
    trigger_codes = rules["supports_fixes"]["piste_gardiens"]["codes_internes"]
    catalogue_bundle = copy.deepcopy(tiles["tuiles_ciblees"])
    for slot in catalogue_bundle.values():
        for prof in slot["profils"].values():
            prof["economie_bot"] = derive_economie_bot(slot, prof, trigger_codes=trigger_codes)

    reglette = rules["supports_fixes"]["reglette_tactiques"]
    ratissage = rules["seuil_ratissage_cibles_et_contacts"]["ratissage"]
    sac = rules["materiel_fini_reversible"]["sac_opaque_et_jetons"]
    chassis = rules["chassis_canonique"]

    bundle: dict[str, Any] = {
        "meta": {
            "schema_version": str(rules["meta"]["schema_version"]),
            "source_studio_version": "v6.2",
            "kernel_runtime_status": str(rules["meta"]["kernel_sync_status"]),
            "studio_sha256": studio_sha256,
            "contracts_sha256": contracts_sha256,
            "total_emplacements": len(catalogue_bundle),
            "total_profils": sum(len(s["profils"]) for s in catalogue_bundle.values()),
        },
        "peuples": copy.deepcopy(rules["peuples"]),
        "matrice_paires": copy.deepcopy(rules["matrice_paires"]),
        "chassis_canonique": copy.deepcopy(chassis),
        "chassis_axes": copy.deepcopy(rules["chassis_axes_studio"]),
        "topologies": {
            "validees": copy.deepcopy(spec_formelle["architecture_reference"]["topologies_validees"]),
            "details_seuil_et_dotation": copy.deepcopy(catalog_doc["topologies"]),
            "reserves_materiel": spec_formelle["architecture_reference"]["reserves_materiel"],
            "plafond_repousse_parcelle": spec_formelle["architecture_reference"][
                "plafond_repousse_parcelle"
            ],
            "repousse_finale_base": int(chassis["repousse_finale_base"]),
        },
        "tactiques": copy.deepcopy(reglette["tactiques"]),
        "reglette_tactiques_reversible": {
            k: copy.deepcopy(v) for k, v in reglette.items() if k != "tactiques"
        },
        "piste_gardiens": copy.deepcopy(rules["supports_fixes"]["piste_gardiens"]),
        "machine_damage_rules": {
            "placement_initial_canonique": str(chassis["placement_initial_machines"]),
            "piege_autonome_portee": str(chassis["piege_autonome_portee"]),
            "seuil_parade": copy.deepcopy(
                rules["seuil_ratissage_cibles_et_contacts"]["seuil_parade"]
            ),
            "ABATTEUSE": {
                "coupe_tous_les_arbres": True,
                "souches_retirees": 0,
            },
            "BULLDOZER": {
                "arbres_retournes_en_souche": 1,
                "retire_toutes_souches": True,
                "test_parade_unique": True,
            },
            "repousse_finale_base": int(chassis["repousse_finale_base"]),
            "enracinement_volontaire": copy.deepcopy(
                rules["enracinement_volontaire"]["calibrage"]
            ),
            "ratissage": copy.deepcopy(ratissage),
        },
        # Shim de clé `machine_deck_rules` conservé pour compatibilité tests/digest jusqu'au Chantier 4
        "machine_deck_rules": {
            "support_physique": str(sac["support"]),
            "jetons_machine_par_rayon": int(sac["jetons_machine_par_rayon"]),
            "types_par_rayon": list(sac["types_par_rayon"]),
            "total_initial_formula": str(sac["total_initial_formula"]),
            "sabotage_dilution_permanente": bool(sac["sabotage_ordinaires_dilution_permanente"]),
            "sabotage_ecailles_max": int(sac["sabotage_ecailles_max"]),
            "sabotage_effet_propre": sac["sabotage_effet_propre"],
            "lancer_des_universel": bool(
                rules["materiel_fini_reversible"]["lancer_de_des_universel"][
                    "tous_les_joueurs_lancent"
                ]
            ),
            "remise_sac_etape": "MENAGE",
            "penurie_ordre": str(sac["penurie_ordre"]),
        },
        "accessoires_3_plus_3": copy.deepcopy(rules["accessoires_3_plus_3"]),
        "enracinement_volontaire": copy.deepcopy(rules["enracinement_volontaire"]),
        "step_arbitrages_map": copy.deepcopy(spec_formelle["step_arbitrages_map"]),
        "spec_formelle_v6_0": spec_formelle,
        "catalogue_tuiles": catalogue_bundle,
    }
    _write_json(OUT_SPEC_BUNDLE, bundle)

    return {
        "schema_version": bundle["meta"]["schema_version"],
        "slots": bundle["meta"]["total_emplacements"],
        "profiles": bundle["meta"]["total_profils"],
        "invariants": len(invariants["invariants"]),
    }


def main() -> int:
    summary = build_all_artifacts()
    print(
        f"build_studio_artifacts.py : OK (v{summary['schema_version']}, "
        f"{summary['slots']} slots, {summary['profiles']} profils, "
        f"{summary['invariants']} invariants)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
