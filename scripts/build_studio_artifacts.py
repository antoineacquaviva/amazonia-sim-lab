"""Compilateur dérivé unique (SSOT v6.4 actif + archive/runtime v6.2 sanctuarisée) pour Amazonia Doc Studio.

Lit exclusivement les contrats SSOT de `contracts/` :
- Socle actif Studio `v6.4` : `rules_canon_v6_4.json`, `physical_and_edge_invariants_v6_4.json`,
  `tiles_canon_v6_4.json` (+ archive Passe 1 `tiles_canon_v6_3.json`)
- Socle archive/runtime PyPy `v6.2` : `rules_canon_v6_2.json`,
  `physical_and_edge_invariants.json`, `tiles_canon_v6_2.json`

Génère sans aucune constante métier codée en dur :
1. `docs/data/spec_formelle_v6_4.json`, `docs/data/catalog_v6_4.json`, `docs/data/canon_v6_4_data.js`
2. `docs/data/spec_formelle_v6_0.json`, `docs/data/catalog_v6_0.json`, `docs/data/amazonia_data_v6_0.js`
3. `docs/data/panels_v6_3_data.js` (archives duel P1/P2/P3)
4. `data/catalog_v6_0.json`, `data/spec_formelle_v6_0.json`, `data/studio_lock.json`, `data/spec_bundle_v6_0.json`
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

RULES_V6_4_CONTRACT_PATH = CONTRACTS_DIR / "rules_canon_v6_4.json"
INVARIANTS_V6_4_CONTRACT_PATH = CONTRACTS_DIR / "physical_and_edge_invariants_v6_4.json"
TILES_V6_4_CONTRACT_PATH = CONTRACTS_DIR / "tiles_canon_v6_4.json"
TILES_V6_3_CONTRACT_PATH = CONTRACTS_DIR / "tiles_canon_v6_3.json"

PANELS_DIR = CONTRACTS_DIR / "panels"
AUTHOR_WORKSPACE_PATH = PANELS_DIR / "author_workspace_v6_3.json"
AUTHOR_WORKSPACE_V6_4_PATH = PANELS_DIR / "author_workspace_v6_4.json"
PANEL_IDS_V6_3: tuple[str, ...] = ("panel_1", "panel_2", "panel_3")

OUT_DOCS_SPEC = DOCS_DATA_DIR / "spec_formelle_v6_0.json"
OUT_DOCS_CATALOG = DOCS_DATA_DIR / "catalog_v6_0.json"
OUT_DOCS_JS = DOCS_DATA_DIR / "amazonia_data_v6_0.js"
OUT_DOCS_PANELS_V6_3_JS = DOCS_DATA_DIR / "panels_v6_3_data.js"
OUT_DOCS_SPEC_V6_4 = DOCS_DATA_DIR / "spec_formelle_v6_4.json"
OUT_DOCS_CATALOG_V6_4 = DOCS_DATA_DIR / "catalog_v6_4.json"
OUT_DOCS_CANON_V6_4_JS = DOCS_DATA_DIR / "canon_v6_4_data.js"
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
    "ARBRE": "RES_ARBRE",
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

    if "ENRACINEMENT" in tags and "souche" in texte_lower:
        inputs.append("RES_SOUCHE")
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
    sf_src = rules.get("spec_formelle_v6_4") or rules["spec_formelle_v6_2"]
    tuiles = tiles["tuiles_ciblees"]

    total_slots = len(tuiles)
    total_profiles = sum(
        len(slot["profils"]) if isinstance(slot, dict) and "profils" in slot else 1
        for slot in tuiles.values()
    )
    mat_arbres = rules["materiel_fini_reversible"]["arbres_et_souches"]

    out: dict[str, Any] = {
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
    if "six_verbes_du_coeur" in rules:
        out["six_verbes_du_coeur"] = copy.deepcopy(rules["six_verbes_du_coeur"])
    return out


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
        "total_profils": sum(
            len(s["profils"]) if isinstance(s, dict) and "profils" in s else 1
            for s in tuiles.values()
        ),
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
    *,
    extra_top_changelog: dict[str, Any] | None = None,
) -> str:
    meta = rules["meta"]
    changelog_v6_2 = copy.deepcopy(rules["changelog_v6_2"])
    v62_ver = str(changelog_v6_2["version"])
    head_blocks: list[dict[str, Any]] = []
    skip_versions: set[str] = {v62_ver}
    if extra_top_changelog is not None:
        top_block = copy.deepcopy(extra_top_changelog)
        head_blocks.append(top_block)
        skip_versions.add(str(top_block["version"]))
    head_blocks.append(changelog_v6_2)
    merged_changelog = head_blocks + [
        block for block in existing_changelog if str(block.get("version", "")) not in skip_versions
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
            f"(Archive/Runtime v{meta['schema_version']} · {len(catalogue_js)} tuiles Canon 0 · "
            "Châssis unique verrouillé · Changelog aligné v6.4)"
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


def compile_panels_v6_3_js(
    panels_dir: Path = PANELS_DIR,
    workspace_path: Path | None = None,
) -> tuple[str, dict[str, Any]]:
    """Compile `docs/data/panels_v6_3_data.js` (3 panels v6.3.1, 32 pictos, workspace initial)."""
    from scripts.tiles_v6_3_schema import (
        DEFAULT_REFERENTIEL_PICTOGRAMMES,
        LOCKED_GARDIEN_CASTING_V6_3,
        SLOTS_SPEC_30,
    )

    panels_payload: dict[str, Any] = {}
    panel_files_used: list[Path] = []
    referentiel_pictos: dict[str, Any] = copy.deepcopy(DEFAULT_REFERENTIEL_PICTOGRAMMES)

    for pid in PANEL_IDS_V6_3:
        pfile = panels_dir / f"{pid}.json"
        if not pfile.is_file():
            continue
        raw_doc: dict[str, Any] = json.loads(pfile.read_text(encoding="utf-8"))
        if isinstance(raw_doc.get("referentiel_pictogrammes"), dict):
            for pcode, pentry in raw_doc["referentiel_pictogrammes"].items():
                if pcode in referentiel_pictos and isinstance(pentry, dict):
                    referentiel_pictos[pcode] = copy.deepcopy(pentry)
        panels_payload[pid] = {
            "_meta": copy.deepcopy(raw_doc.get("_meta") or {}),
            "carte_des_roles": copy.deepcopy(raw_doc.get("carte_des_roles") or {}),
            "rapport_audit_197": copy.deepcopy(raw_doc.get("rapport_audit_197") or {}),
            "tuiles_ciblees": copy.deepcopy(raw_doc.get("tuiles_ciblees") or {}),
        }
        panel_files_used.append(pfile)

    ws_file = workspace_path if workspace_path is not None else (panels_dir / "author_workspace_v6_3.json")
    initial_workspace: dict[str, Any] | None = None
    ws_used: Path | None = None
    if ws_file.is_file():
        loaded_ws = json.loads(ws_file.read_text(encoding="utf-8"))
        if isinstance(loaded_ws, dict):
            initial_workspace = loaded_ws
            ws_used = ws_file

    slots_spec = [
        {
            "id": sid,
            "famille": fam,
            "origine": orig,
            "voisin": vois,
            "alias_oriente": alias,
        }
        for sid, fam, orig, vois, alias in SLOTS_SPEC_30
    ]

    casting_out = {
        sid: {
            "alias_oriente": next(a for s, _f, _o, _v, a in SLOTS_SPEC_30 if s == sid),
            "nom_animal": animal,
            "origine": next(o for s, _f, o, _v, _a in SLOTS_SPEC_30 if s == sid),
            "voisin": next(v for s, _f, _o, v, _a in SLOTS_SPEC_30 if s == sid),
        }
        for sid, animal in LOCKED_GARDIEN_CASTING_V6_3.items()
    }

    sections = [
        "// =========================================================================",
        (
            "// data/panels_v6_3_data.js — Généré automatiquement depuis contracts/panels/ "
            f"(Atelier v6.3.1 · {len(panels_payload)} panels · {len(referentiel_pictos)} pictogrammes)"
        ),
        "// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.",
        "// =========================================================================",
        f"const REFERENTIEL_PICTOGRAMMES_V6_3 = {json.dumps(referentiel_pictos, indent=2, ensure_ascii=False)};",
        "",
        f"const CASTING_GARDIENS_V6_3 = {json.dumps(casting_out, indent=2, ensure_ascii=False)};",
        "",
        f"const SLOTS_SPEC_V6_3 = {json.dumps(slots_spec, indent=2, ensure_ascii=False)};",
        "",
        f"const PANELS_V6_3 = {json.dumps(panels_payload, indent=2, ensure_ascii=False)};",
        "",
        f"const AUTHOR_WORKSPACE_INITIAL_V6_3 = {json.dumps(initial_workspace, indent=2, ensure_ascii=False)};",
        "",
    ]
    js_src = "\n".join(sections)
    _validate_js_syntax(js_src, "docs/data/panels_v6_3_data.js")
    return js_src, {
        "panels_count": len(panels_payload),
        "pictograms_count": len(referentiel_pictos),
        "panel_files": panel_files_used,
        "workspace_file": ws_used,
    }


def compile_canon_v6_4_js(
    rules_v64: dict[str, Any],
    invariants_v64: dict[str, Any],
    tiles_v64: dict[str, Any],
    tiles_v63: dict[str, Any],
    spec_formelle_v64: dict[str, Any],
    workspace_v64_path: Path | None = None,
) -> tuple[str, dict[str, Any]]:
    """Compile `docs/data/canon_v6_4_data.js` (Cœur v6.4, 22 INV, 6 Verbes, Canon 30 affiné + Archive Passe 1)."""
    ws_file = workspace_v64_path if workspace_v64_path is not None else AUTHOR_WORKSPACE_V6_4_PATH
    initial_ws_v64: dict[str, Any] | None = None
    ws_used: Path | None = None
    if ws_file.is_file():
        loaded_ws = json.loads(ws_file.read_text(encoding="utf-8"))
        if isinstance(loaded_ws, dict):
            initial_ws_v64 = loaded_ws
            ws_used = ws_file

    canon_v64_payload = {
        "_meta": copy.deepcopy(tiles_v64.get("_meta") or {}),
        "carte_des_roles": copy.deepcopy(tiles_v64.get("carte_des_roles") or {}),
        "rapport_audit_197": copy.deepcopy(tiles_v64.get("rapport_audit_197") or {}),
        "tuiles_ciblees": copy.deepcopy(tiles_v64.get("tuiles_ciblees") or {}),
    }
    canon_v63_payload = {
        "_meta": copy.deepcopy(tiles_v63.get("_meta") or {}),
        "carte_des_roles": copy.deepcopy(tiles_v63.get("carte_des_roles") or {}),
        "rapport_audit_197": copy.deepcopy(tiles_v63.get("rapport_audit_197") or {}),
        "tuiles_ciblees": copy.deepcopy(tiles_v63.get("tuiles_ciblees") or {}),
    }
    ref_pictos_v64 = copy.deepcopy(tiles_v64.get("referentiel_pictogrammes") or {})
    essaim_natives_v64 = copy.deepcopy(
        rules_v64["architecture_modulaire"]["modules"]["module_essaim"]["regles_natives"]
    )
    rules_summary_v64 = {
        "meta": copy.deepcopy(rules_v64["meta"]),
        "six_verbes_du_coeur": copy.deepcopy(rules_v64["six_verbes_du_coeur"]),
        "architecture_modulaire": copy.deepcopy(rules_v64["architecture_modulaire"]),
        "accessoires_3_plus_3": copy.deepcopy(rules_v64["accessoires_3_plus_3"]),
        "enracinement_volontaire": copy.deepcopy(rules_v64["enracinement_volontaire"]),
        "supports_fixes": copy.deepcopy(rules_v64["supports_fixes"]),
        "changelog_v6_4": copy.deepcopy(rules_v64["changelog_v6_4"]),
    }

    sections = [
        "// =========================================================================",
        (
            "// data/canon_v6_4_data.js — Généré automatiquement depuis contracts/*_v6_4.json "
            f"(SSOT v{rules_v64['meta']['schema_version']} · 30 tuiles Passe 2 affinées · "
            f"{len(ref_pictos_v64)} pictogrammes · Archive Passe 1 v6.3 incluse)"
        ),
        "// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.",
        "// =========================================================================",
        f"const SIX_VERBES_COEUR_V6_4 = {json.dumps(rules_v64['six_verbes_du_coeur'], indent=2, ensure_ascii=False)};",
        "",
        f"const RULES_CANON_V6_4 = {json.dumps(rules_summary_v64, indent=2, ensure_ascii=False)};",
        "",
        f"const MODULE_ESSAIM_REGLES_NATIVES_V6_4 = {json.dumps(essaim_natives_v64, indent=2, ensure_ascii=False)};",
        "",
        f"const PHYSICAL_INVARIANTS_V6_4 = {json.dumps(invariants_v64['invariants'], indent=2, ensure_ascii=False)};",
        "",
        f"const SPEC_FORMELLE_V6_4 = {json.dumps(spec_formelle_v64, indent=2, ensure_ascii=False)};",
        "",
        f"const REFERENTIEL_PICTOGRAMMES_V6_4 = {json.dumps(ref_pictos_v64, indent=2, ensure_ascii=False)};",
        "",
        f"const CANON_V6_4 = {json.dumps(canon_v64_payload, indent=2, ensure_ascii=False)};",
        "",
        f"const CANON_V6_3_PASSE1 = {json.dumps(canon_v63_payload, indent=2, ensure_ascii=False)};",
        "",
        f"const AUTHOR_WORKSPACE_INITIAL_V6_4 = {json.dumps(initial_ws_v64, indent=2, ensure_ascii=False)};",
        "",
    ]
    js_src = "\n".join(sections)
    _validate_js_syntax(js_src, "docs/data/canon_v6_4_data.js")
    return js_src, {
        "pictograms_v6_4": len(ref_pictos_v64),
        "invariants_v6_4": len(invariants_v64["invariants"]),
        "workspace_v6_4_file": ws_used,
    }


def compile_studio_payloads(
    rules: dict[str, Any],
    invariants: dict[str, Any],
    tiles: dict[str, Any],
    existing_changelog: list[dict[str, Any]],
    *,
    extra_top_changelog: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], str, dict[str, Any]]:
    """Compile en mémoire `(spec_formelle, catalog_doc, amazonia_js, adapted_tiles)` pour v6.2/v6.3/v6.4."""
    from scripts.tiles_v6_3_schema import adapt_tiles_contract_for_studio

    adapted_tiles = adapt_tiles_contract_for_studio(tiles)
    spec_formelle = _build_spec_formelle(rules, invariants, adapted_tiles)
    catalog_doc = _build_catalog_json(rules, spec_formelle, adapted_tiles)
    amazonia_js = _build_amazonia_js(
        rules,
        invariants,
        adapted_tiles,
        spec_formelle,
        existing_changelog,
        extra_top_changelog=extra_top_changelog,
    )
    _validate_js_syntax(amazonia_js, "docs/data/amazonia_data_v6_0.js")
    return spec_formelle, catalog_doc, amazonia_js, adapted_tiles


def build_all_artifacts(tiles_contract_path: Path | None = None) -> dict[str, Any]:
    """Compile l'ensemble des artefacts dérivés Studio v6.4 + archive/runtime PyPy v6.2.

    - Couche Studio active `v6.4` : `docs/data/spec_formelle_v6_4.json`, `docs/data/catalog_v6_4.json`,
      `docs/data/canon_v6_4_data.js` (+ `VERSION_CHANGELOG[0] = v6.4` dans `amazonia_data_v6_0.js`).
    - Couche archive/runtime PyPy `v6.2` (sanctuarisée jusqu'au Jalon 4) : `docs/data/*_v6_0.*`,
      `data/spec_bundle_v6_0.json`, `docs/data/panels_v6_3_data.js`.
    """
    active_tiles_path = tiles_contract_path or TILES_CONTRACT_PATH
    for req in (
        RULES_CONTRACT_PATH,
        INVARIANTS_CONTRACT_PATH,
        active_tiles_path,
        RULES_V6_4_CONTRACT_PATH,
        INVARIANTS_V6_4_CONTRACT_PATH,
        TILES_V6_4_CONTRACT_PATH,
        TILES_V6_3_CONTRACT_PATH,
    ):
        if not req.is_file():
            raise FileNotFoundError(f"Contrat SSOT manquant : {req}")

    rules: dict[str, Any] = json.loads(RULES_CONTRACT_PATH.read_text(encoding="utf-8"))
    invariants: dict[str, Any] = json.loads(INVARIANTS_CONTRACT_PATH.read_text(encoding="utf-8"))
    raw_tiles: dict[str, Any] = json.loads(active_tiles_path.read_text(encoding="utf-8"))

    rules_v64: dict[str, Any] = json.loads(RULES_V6_4_CONTRACT_PATH.read_text(encoding="utf-8"))
    invariants_v64: dict[str, Any] = json.loads(INVARIANTS_V6_4_CONTRACT_PATH.read_text(encoding="utf-8"))
    tiles_v64: dict[str, Any] = json.loads(TILES_V6_4_CONTRACT_PATH.read_text(encoding="utf-8"))
    tiles_v63: dict[str, Any] = json.loads(TILES_V6_3_CONTRACT_PATH.read_text(encoding="utf-8"))

    existing_changelog = _extract_existing_changelog(OUT_DOCS_JS)
    spec_formelle, catalog_doc, amazonia_js, _tiles = compile_studio_payloads(
        rules,
        invariants,
        raw_tiles,
        existing_changelog,
        extra_top_changelog=rules_v64.get("changelog_v6_4"),
    )
    panels_v6_3_js, panels_meta = compile_panels_v6_3_js(PANELS_DIR, AUTHOR_WORKSPACE_PATH)

    # Couche Studio v6.4 (Cœur v6.4 + 30 Tuiles Passe 2 + Archive Passe 1)
    spec_formelle_v64 = _build_spec_formelle(rules_v64, invariants_v64, tiles_v64)
    catalog_v64 = _build_catalog_json(rules_v64, spec_formelle_v64, tiles_v64)
    canon_v6_4_js, v64_meta = compile_canon_v6_4_js(
        rules_v64,
        invariants_v64,
        tiles_v64,
        tiles_v63,
        spec_formelle_v64,
        AUTHOR_WORKSPACE_V6_4_PATH,
    )

    # 1. Écriture des artefacts Studio (docs/data/)
    _write_json(OUT_DOCS_SPEC, spec_formelle)
    _write_json(OUT_DOCS_CATALOG, catalog_doc)
    _write_text_lf(OUT_DOCS_JS, amazonia_js)
    _write_text_lf(OUT_DOCS_PANELS_V6_3_JS, panels_v6_3_js)
    _write_json(OUT_DOCS_SPEC_V6_4, spec_formelle_v64)
    _write_json(OUT_DOCS_CATALOG_V6_4, catalog_v64)
    _write_text_lf(OUT_DOCS_CANON_V6_4_JS, canon_v6_4_js)

    # 2. Miroirs data/ et verrou SHA-256 data/studio_lock.json
    _write_json(OUT_DATA_SPEC, spec_formelle)
    _write_json(OUT_DATA_CATALOG, catalog_doc)

    studio_sha256: dict[str, dict[str, object]] = {
        "catalog_v6_0.json": _file_lock_entry(OUT_DOCS_CATALOG),
        "spec_formelle_v6_0.json": _file_lock_entry(OUT_DOCS_SPEC),
        "amazonia_data_v6_0.js": _file_lock_entry(OUT_DOCS_JS),
        "livret_v6_0.js": _file_lock_entry(DOCS_LIVRET_JS),
        "panels_v6_3_data.js": _file_lock_entry(OUT_DOCS_PANELS_V6_3_JS),
        "catalog_v6_4.json": _file_lock_entry(OUT_DOCS_CATALOG_V6_4),
        "spec_formelle_v6_4.json": _file_lock_entry(OUT_DOCS_SPEC_V6_4),
        "canon_v6_4_data.js": _file_lock_entry(OUT_DOCS_CANON_V6_4_JS),
    }
    contracts_sha256: dict[str, dict[str, object]] = {
        "rules_canon_v6_2.json": _file_lock_entry(RULES_CONTRACT_PATH),
        "physical_and_edge_invariants.json": _file_lock_entry(INVARIANTS_CONTRACT_PATH),
        active_tiles_path.name: _file_lock_entry(active_tiles_path),
        "rules_canon_v6_4.json": _file_lock_entry(RULES_V6_4_CONTRACT_PATH),
        "physical_and_edge_invariants_v6_4.json": _file_lock_entry(INVARIANTS_V6_4_CONTRACT_PATH),
        "tiles_canon_v6_4.json": _file_lock_entry(TILES_V6_4_CONTRACT_PATH),
        "tiles_canon_v6_3.json": _file_lock_entry(TILES_V6_3_CONTRACT_PATH),
    }
    for pfile in panels_meta["panel_files"]:
        rel_panel = pfile.relative_to(CONTRACTS_DIR).as_posix()
        contracts_sha256[rel_panel] = _file_lock_entry(pfile)
    if panels_meta["workspace_file"] is not None:
        ws_rel = panels_meta["workspace_file"].relative_to(CONTRACTS_DIR).as_posix()
        contracts_sha256[ws_rel] = _file_lock_entry(panels_meta["workspace_file"])
    if v64_meta["workspace_v6_4_file"] is not None:
        ws64_rel = v64_meta["workspace_v6_4_file"].relative_to(CONTRACTS_DIR).as_posix()
        contracts_sha256[ws64_rel] = _file_lock_entry(v64_meta["workspace_v6_4_file"])

    lock_payload: dict[str, Any] = {
        "studio_version": "v6.4",
        "schema_version": str(rules_v64["meta"]["schema_version"]),
        "runtime_bundle_version": str(rules_v64["meta"]["schema_version"]),
        "files": studio_sha256,
        "contracts": contracts_sha256,
    }
    _write_json(OUT_STUDIO_LOCK, lock_payload)

    # 3. Construction de data/spec_bundle_v6_0.json (runtime PyPy v6.4 actif & graphe economie_bot 30 tuiles v6.4)
    from scripts.tiles_v6_3_schema import adapt_tiles_contract_for_studio

    adapted_v64_tiles = adapt_tiles_contract_for_studio(tiles_v64)
    trigger_codes = rules_v64["supports_fixes"]["piste_gardiens"]["codes_internes"]
    catalogue_bundle = copy.deepcopy(adapted_v64_tiles["tuiles_ciblees"])
    for slot in catalogue_bundle.values():
        for prof in slot["profils"].values():
            prof["economie_bot"] = derive_economie_bot(slot, prof, trigger_codes=trigger_codes)

    reglette = rules_v64["supports_fixes"]["reglette_tactiques"]
    ratissage = rules_v64["seuil_ratissage_cibles_et_contacts"]["ratissage"]
    sac = rules_v64["materiel_fini_reversible"]["sac_opaque_et_jetons"]
    chassis = rules_v64["chassis_canonique"]

    bundle: dict[str, Any] = {
        "meta": {
            "schema_version": str(rules_v64["meta"]["schema_version"]),
            "source_studio_version": "v6.4",
            "kernel_runtime_status": str(rules_v64["meta"]["kernel_sync_status"]),
            "studio_sha256": studio_sha256,
            "contracts_sha256": contracts_sha256,
            "total_emplacements": len(catalogue_bundle),
            "total_profils": sum(len(s["profils"]) for s in catalogue_bundle.values()),
        },
        "peuples": copy.deepcopy(rules_v64["peuples"]),
        "matrice_paires": copy.deepcopy(rules_v64["matrice_paires"]),
        "chassis_canonique": copy.deepcopy(chassis),
        "chassis_axes": copy.deepcopy(rules_v64["chassis_axes_studio"]),
        "topologies": {
            "validees": copy.deepcopy(spec_formelle_v64["architecture_reference"]["topologies_validees"]),
            "details_seuil_et_dotation": copy.deepcopy(catalog_v64["topologies"]),
            "reserves_materiel": spec_formelle_v64["architecture_reference"]["reserves_materiel"],
            "plafond_repousse_parcelle": spec_formelle_v64["architecture_reference"][
                "plafond_repousse_parcelle"
            ],
            "repousse_finale_base": int(chassis["repousse_finale_base"]),
        },
        "tactiques": copy.deepcopy(reglette["tactiques"]),
        "reglette_tactiques_reversible": {
            k: copy.deepcopy(v) for k, v in reglette.items() if k != "tactiques"
        },
        "piste_gardiens": copy.deepcopy(rules_v64["supports_fixes"]["piste_gardiens"]),
        "machine_damage_rules": {
            "placement_initial_canonique": str(chassis["placement_initial_machines"]),
            "piege_autonome_portee": str(chassis["piege_autonome_portee"]),
            "seuil_parade": copy.deepcopy(
                rules_v64["seuil_ratissage_cibles_et_contacts"]["seuil_parade"]
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
                rules_v64["enracinement_volontaire"]["calibrage"]
            ),
            "ratissage": copy.deepcopy(ratissage),
        },
        "machine_deck_rules": {
            "support_physique": str(sac["support"]),
            "jetons_machine_par_rayon": int(sac["jetons_machine_par_rayon"]),
            "types_par_rayon": list(sac["types_par_rayon"]),
            "total_initial_formula": str(sac["total_initial_formula"]),
            "sabotage_dilution_permanente": bool(sac["sabotage_ordinaires_dilution_permanente"]),
            "sabotage_ecailles_max": int(sac["sabotage_ecailles_max"]),
            "sabotage_effet_propre": sac["sabotage_effet_propre"],
            "lancer_des_universel": bool(
                rules_v64["materiel_fini_reversible"]["lancer_de_des_universel"][
                    "tous_les_joueurs_lancent"
                ]
            ),
            "remise_sac_etape": "MENAGE",
            "penurie_ordre": str(sac["penurie_ordre"]),
        },
        "accessoires_3_plus_3": copy.deepcopy(rules_v64["accessoires_3_plus_3"]),
        "enracinement_volontaire": copy.deepcopy(rules_v64["enracinement_volontaire"]),
        "step_arbitrages_map": copy.deepcopy(spec_formelle_v64["step_arbitrages_map"]),
        "spec_formelle_v6_0": spec_formelle_v64,
        "catalogue_tuiles": catalogue_bundle,
    }
    _write_json(OUT_SPEC_BUNDLE, bundle)

    return {
        "schema_version": bundle["meta"]["schema_version"],
        "studio_schema_version": str(rules_v64["meta"]["schema_version"]),
        "slots": bundle["meta"]["total_emplacements"],
        "profiles": bundle["meta"]["total_profils"],
        "invariants": len(invariants_v64["invariants"]),
        "panels_v6_3": panels_meta["panels_count"],
        "pictograms_v6_3": panels_meta["pictograms_count"],
        "pictograms_v6_4": v64_meta["pictograms_v6_4"],
    }


def main() -> int:
    summary = build_all_artifacts()
    print(
        f"build_studio_artifacts.py : OK (Studio v{summary['studio_schema_version']} · "
        f"Runtime PyPy v{summary['schema_version']}, {summary['slots']} slots, "
        f"{summary['invariants']} invariants, {summary['pictograms_v6_4']} pictos v6.4, "
        f"{summary['panels_v6_3']} panels archive)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
