"""Garde-fou local de validation de lot pour amazonia-sim-lab (Windows 11 & Ubuntu Linux)."""

from __future__ import annotations

import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONTRACTS_DIR = ROOT / "contracts"
LOCKS_FILE = CONTRACTS_DIR / "kernel_locks.sha256"
RULES_CANON_FILE = CONTRACTS_DIR / "rules_canon_v6_2.json"
INVARIANTS_FILE = CONTRACTS_DIR / "physical_and_edge_invariants.json"
TILES_CANON_FILE = CONTRACTS_DIR / "tiles_canon_v6_2.json"
GUARDS_FILE = CONTRACTS_DIR / "studio_rules_guards.json"
EFFECTS_DIR = ROOT / "engine" / "effects"
PYPROJECT_FILE = ROOT / "pyproject.toml"
DOCS_DATA_DIR = ROOT / "docs" / "data"
STUDIO_CONTEXT_FILE = ROOT / "docs" / "AMAZONIA_STUDIO_CONTEXT.md"
STUDIO_CATALOG_FILE = DOCS_DATA_DIR / "catalog_v6_0.json"
STUDIO_SPEC_FILE = DOCS_DATA_DIR / "spec_formelle_v6_0.json"
STUDIO_JS_FILE = DOCS_DATA_DIR / "amazonia_data_v6_0.js"
SPEC_BUNDLE_FILE = ROOT / "data" / "spec_bundle_v6_0.json"
UPPER_CASE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

_SKIP_DIRS: frozenset[str] = frozenset(
    {".git", ".venv", ".tmp_runs", "__pycache__", ".pytest_cache", ".ruff_cache", "archive"}
)
_FORBIDDEN_LLM_MODULES: tuple[str, ...] = (
    "google.genai",
    "google.generativeai",
    "google_genai",
    "vertexai",
)
_FORBIDDEN_GOOGLE_SUBMODULES: frozenset[str] = frozenset({"genai", "generativeai"})
_FORBIDDEN_API_KEY_TOKEN: str = "GEMINI_API_KEY"
_FORBIDDEN_PACKAGES: tuple[str, ...] = (
    "google-genai",
    "google-generativeai",
    "google-cloud-aiplatform",
)

# Linter Canon 0 (tuiles)
_FACE_LABEL_RE = re.compile(
    r"^\s*(?:Face\s+[12]|Enraciné|En\s+Parade|En\s+Migration)\s*:\s*",
    re.IGNORECASE,
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_BR_SPLIT_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_WORD_ELISION_RE = re.compile(r"[0-9A-Za-zÀ-ÖØ-öø-ÿ]+")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")
_CONDITION_RE = re.compile(r"(?i)\b(?:si|quand|lorsque|lorsqu)\b")
_STEP_CODE_RE = re.compile(r"\b[1-6]\.[0-3]\b")
_INSECT_LEXICON_RE = re.compile(r"(?i)\b(?:insectes?|nids?|essaims?|migrations?)\b")
_GARDIEN_LEXICON_RE = re.compile(r"(?i)\b(?:gardiens?|éveil|encoches?|résonance)\b")

_I_LISIERE_SLOTS: frozenset[str] = frozenset(
    {"G13", "G14", "G15", "R6", "R10", "M1", "M2", "M3", "M4", "M5"}
)
_A0_AUTONOMOUS_SLOTS: frozenset[str] = frozenset({"R1", "R2", "R6", "R10", "M4", "M5"})
_BANNED_TILE_TERMS: tuple[str, ...] = (
    "carte",
    "cartes",
    "paquet",
    "non rasée",
    "hors Ratissage",
    "sans Piège",
    "sous sa tuile",
    "Embuscade",
    "armer",
    "Apprentissage",
    "Cerveau",
    "Bug",
    "Colonie",
    "case Furtivité",
    "Défenseur d'ajustement",
    "Défenseur d’ajustement",
    "pour ce tour",
    "jusqu'à la fin du tour",
    "jusqu’à la fin du tour",
)


def _is_immutable_expr(node: ast.AST | None) -> bool:
    if node is None:
        return True
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Tuple):
        return all(_is_immutable_expr(elt) for elt in node.elts)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub, ast.Invert)):
        return _is_immutable_expr(node.operand)
    if isinstance(node, ast.BinOp):
        return _is_immutable_expr(node.left) and _is_immutable_expr(node.right)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "frozenset":
        return all(_is_immutable_expr(arg) for arg in node.args)
    return False


class EffectModuleVisitor(ast.NodeVisitor):
    """Visiteur AST vérifiant les contraintes stateless de engine/effects/."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.errors: list[str] = []

    def visit_Attribute(self, node: ast.Attribute) -> None:
        if node.attr == "_buf":
            self.errors.append(f"{self.filename}:{node.lineno}: accès interdit à l'attribut '_buf'")
        self.generic_visit(node)

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            if alias.name == "random" or alias.name.startswith("random."):
                self.errors.append(f"{self.filename}:{node.lineno}: import 'random' interdit")
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module == "random" or (node.module is not None and node.module.startswith("random.")):
            self.errors.append(f"{self.filename}:{node.lineno}: import depuis 'random' interdit")
        self.generic_visit(node)

    def check_module(self, tree: ast.Module) -> None:
        for stmt in tree.body:
            if isinstance(stmt, ast.Assign):
                self._check_global_assign(stmt.targets, stmt.value, stmt.lineno)
            elif isinstance(stmt, ast.AnnAssign):
                self._check_global_assign([stmt.target], stmt.value, stmt.lineno)
            elif isinstance(stmt, ast.AugAssign):
                self.errors.append(
                    f"{self.filename}:{stmt.lineno}: affectation globale mutable interdite"
                )
        self.visit(tree)

    def _check_global_assign(
        self, targets: list[ast.expr], value: ast.expr | None, lineno: int
    ) -> None:
        for target in targets:
            if not isinstance(target, ast.Name):
                self.errors.append(
                    f"{self.filename}:{lineno}: affectation globale non-simple interdite"
                )
                continue
            name = target.id
            if name == "__all__":
                continue
            if not UPPER_CASE_RE.match(name):
                self.errors.append(
                    f"{self.filename}:{lineno}: variable globale '{name}' interdite "
                    "(seules les constantes UPPER_CASE immuables sont autorisées)"
                )
                continue
            if not _is_immutable_expr(value):
                self.errors.append(
                    f"{self.filename}:{lineno}: constante '{name}' doit être immuable"
                )


def check_effect_source(source: str, filename: str = "<string>") -> list[str]:
    """Analyse une source Python d'effet et retourne la liste des violations."""
    tree = ast.parse(source, filename=filename)
    visitor = EffectModuleVisitor(filename)
    visitor.check_module(tree)
    return visitor.errors


def _is_forbidden_llm_module(mod_name: str) -> bool:
    return any(
        mod_name == forbidden or mod_name.startswith(forbidden + ".")
        for forbidden in _FORBIDDEN_LLM_MODULES
    )


def check_zero_llm_api_source(source: str, filename: str = "<string>") -> list[str]:
    """Vérifie qu'une source Python n'importe aucun SDK LLM payant ni ne lit la clé API Gemini."""
    tree = ast.parse(source, filename=filename)
    errors: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if _is_forbidden_llm_module(alias.name):
                    errors.append(
                        f"{filename}:{node.lineno}: import SDK LLM payant interdit ('{alias.name}')"
                    )
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if _is_forbidden_llm_module(mod):
                errors.append(
                    f"{filename}:{node.lineno}: import SDK LLM payant interdit ('{mod}')"
                )
            elif mod == "google":
                for alias in node.names:
                    if alias.name in _FORBIDDEN_GOOGLE_SUBMODULES:
                        errors.append(
                            f"{filename}:{node.lineno}: import 'google.{alias.name}' interdit"
                        )
        elif isinstance(node, ast.Name) and node.id == _FORBIDDEN_API_KEY_TOKEN:
            errors.append(
                f"{filename}:{node.lineno}: référence interdite à '{_FORBIDDEN_API_KEY_TOKEN}'"
            )
        elif isinstance(node, ast.Attribute) and node.attr == _FORBIDDEN_API_KEY_TOKEN:
            errors.append(
                f"{filename}:{node.lineno}: attribut interdit '{_FORBIDDEN_API_KEY_TOKEN}'"
            )
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and _FORBIDDEN_API_KEY_TOKEN in node.value
        ):
            errors.append(
                f"{filename}:{node.lineno}: chaîne interdite contenant '{_FORBIDDEN_API_KEY_TOKEN}'"
            )

    return errors


def verify_kernel_locks() -> None:
    """Vérifie les empreintes SHA-256 listées dans contracts/kernel_locks.sha256."""
    if not LOCKS_FILE.exists():
        raise FileNotFoundError(f"Fichier de verrouillage manquant : {LOCKS_FILE}")
    lines = [
        line.strip()
        for line in LOCKS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    if not lines:
        print("[1/10] kernel_locks.sha256 vide : OK")
        return

    for line in lines:
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Ligne invalide dans kernel_locks.sha256 : {line}")
        expected_hash, rel_path = parts[0].lower(), parts[1].strip().lstrip("*")
        target = ROOT / rel_path
        if not target.exists():
            raise FileNotFoundError(f"Fichier verrouillé absent : {rel_path}")
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest().lower()
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"VIOLATION kernel_locks.sha256 sur {rel_path}: "
                f"attendu {expected_hash}, obtenu {actual_hash}"
            )
    print(f"[1/10] kernel_locks.sha256 ({len(lines)} fichiers scellés intacts) : OK")


def verify_effects_ast() -> None:
    """Vérifie par AST tous les modules Python dans engine/effects/."""
    py_files = sorted(EFFECTS_DIR.rglob("*.py"))
    all_errors: list[str] = []
    for py_file in py_files:
        source = py_file.read_text(encoding="utf-8")
        rel = py_file.relative_to(ROOT).as_posix()
        all_errors.extend(check_effect_source(source, rel))
    if all_errors:
        raise RuntimeError("Erreurs AST dans engine/effects/ :\n" + "\n".join(all_errors))
    print(f"[2/10] AST engine/effects/ ({len(py_files)} fichiers) : OK")


def verify_zero_llm_api_billing() -> None:
    """Échoue immédiatement si un fichier Python ou pyproject.toml référence une API LLM payante."""
    all_errors: list[str] = []
    scanned_py = 0

    for py_file in sorted(ROOT.rglob("*.py")):
        if any(part in _SKIP_DIRS for part in py_file.parts):
            continue
        if py_file.resolve() == Path(__file__).resolve():
            continue
        scanned_py += 1
        rel = py_file.relative_to(ROOT).as_posix()
        source = py_file.read_text(encoding="utf-8")
        all_errors.extend(check_zero_llm_api_source(source, rel))

    if PYPROJECT_FILE.exists():
        pyproject_txt = PYPROJECT_FILE.read_text(encoding="utf-8").lower()
        for pkg in _FORBIDDEN_PACKAGES:
            if pkg in pyproject_txt:
                all_errors.append(f"pyproject.toml: dépendance LLM payante interdite ('{pkg}')")

    if all_errors:
        raise RuntimeError(
            "VIOLATION Zéro-Facturation API LLM :\n" + "\n".join(all_errors)
        )
    print(f"[3/10] Garde Zéro-API-LLM ({scanned_py} fichiers Python) : OK")


def _load_studio_js_catalog_and_axes(studio_js_path: Path) -> dict[str, Any]:
    """Charge CATALOGUE_TUILES et CHASSIS_AXES_SPEC depuis docs/data/amazonia_data_v6_0.js via Node vm."""
    js_script = (
        "const fs = require('fs');\n"
        "const vm = require('vm');\n"
        "const ctx = { window: {} };\n"
        "vm.createContext(ctx);\n"
        f"const src = fs.readFileSync({json.dumps(studio_js_path.as_posix())}, 'utf8');\n"
        "const res = vm.runInContext("
        "src + '\\n;({ CATALOGUE_TUILES, CHASSIS_AXES_SPEC });', ctx);\n"
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


def lint_tiles_canon_dict(
    tiles_map: Mapping[str, Mapping[str, Any]],
    *,
    source_label: str = "catalogue",
    require_engine_sync_status: bool = False,
) -> list[str]:
    """Linter éditorial et mécanique strict sur un dictionnaire de tuiles Canon 0."""
    errors: list[str] = []
    expected_slots = (
        {f"G{i}" for i in range(1, 16)}
        | {f"R{i}" for i in range(1, 11)}
        | {f"M{i}" for i in range(1, 6)}
    )
    actual_slots = set(tiles_map.keys())
    if actual_slots != expected_slots:
        missing = sorted(expected_slots - actual_slots)
        extra = sorted(actual_slots - expected_slots)
        errors.append(
            f"{source_label}: ensemble d'emplacements invalide (manquants={missing}, en trop={extra})"
        )

    for slot_id, slot in sorted(tiles_map.items()):
        couple = {str(p) for p in (slot.get("couple") or [])}
        has_i = "I" in couple
        if has_i and slot_id not in _I_LISIERE_SLOTS:
            errors.append(f"{source_label}.{slot_id}: couple contient 'I' hors des 10 tuiles I")
        if not has_i and slot_id in _I_LISIERE_SLOTS:
            errors.append(f"{source_label}.{slot_id}: lisière I attendue mais couple={sorted(couple)}")

        profils = slot.get("profils")
        if not isinstance(profils, Mapping) or not profils:
            errors.append(f"{source_label}.{slot_id}: aucun profil défini")
            continue

        for prof_key, prof in profils.items():
            label = f"{source_label}.{slot_id}:{prof_key}"
            if require_engine_sync_status:
                sync_status = prof.get("engine_sync_status")
                if sync_status not in ("PENDING_KERNEL_V6_2", "ACTIVE_VERIFIED"):
                    errors.append(
                        f"{label}: engine_sync_status invalide ({sync_status!r})"
                    )

            raw_text = str(prof.get("texte", "")).strip()
            if not raw_text:
                errors.append(f"{label}: champ 'texte' vide")
                continue

            parts = [p.strip() for p in _BR_SPLIT_RE.split(raw_text) if p.strip()]
            for face_idx, part in enumerate(parts, start=1):
                no_html = _HTML_TAG_RE.sub("", part).strip()
                clean = _FACE_LABEL_RE.sub("", no_html).strip()

                words = _WORD_ELISION_RE.findall(clean)
                if len(words) > 25:
                    errors.append(
                        f"{label} (face {face_idx}): {len(words)} mots > 25 max -> {clean!r}"
                    )

                sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(clean) if s.strip()]
                if len(sentences) != 1:
                    errors.append(
                        f"{label} (face {face_idx}): {len(sentences)} phrases (attendu 1 seule) -> {clean!r}"
                    )

                conds = _CONDITION_RE.findall(clean)
                if len(conds) > 1:
                    errors.append(
                        f"{label} (face {face_idx}): {len(conds)} conditions > 1 max ({conds}) -> {clean!r}"
                    )

                step_hits = _STEP_CODE_RE.findall(no_html)
                if step_hits:
                    errors.append(
                        f"{label} (face {face_idx}): code numérique d'étape interdit {step_hits}"
                    )

                for term in _BANNED_TILE_TERMS:
                    if re.search(rf"(?i)\b{re.escape(term)}\b", no_html):
                        errors.append(
                            f"{label} (face {face_idx}): terme banni {term!r} dans {no_html!r}"
                        )

                if slot_id not in _I_LISIERE_SLOTS:
                    ins_hits = _INSECT_LEXICON_RE.findall(clean)
                    if ins_hits:
                        errors.append(
                            f"{label} (face {face_idx}): mention Insecte/Essaim hors lisières de I ({ins_hits})"
                        )

                if slot_id in _A0_AUTONOMOUS_SLOTS:
                    g_hits = _GARDIEN_LEXICON_RE.findall(clean)
                    if g_hits:
                        errors.append(
                            f"{label} (face {face_idx}): mention Gardien interdite sur tuile A=0 ({g_hits})"
                        )

    return errors


def verify_tiles_canon() -> None:
    """Linter automatique Canon 0 sur contracts/tiles_canon_v6_2.json et CATALOGUE_TUILES."""
    if not TILES_CANON_FILE.is_file():
        raise FileNotFoundError(f"Contrat tuiles Canon 0 manquant : {TILES_CANON_FILE}")
    if not STUDIO_JS_FILE.is_file():
        raise FileNotFoundError(f"Fichier Studio JS manquant : {STUDIO_JS_FILE}")

    canon_doc: dict[str, Any] = json.loads(TILES_CANON_FILE.read_text(encoding="utf-8"))
    canon_tiles: dict[str, Any] = dict(canon_doc.get("tuiles_ciblees", {}))
    studio_js = _load_studio_js_catalog_and_axes(STUDIO_JS_FILE)
    studio_tiles: dict[str, Any] = dict(studio_js.get("CATALOGUE_TUILES", {}))

    errors: list[str] = []
    errors.extend(
        lint_tiles_canon_dict(
            canon_tiles,
            source_label="contracts/tiles_canon_v6_2.json",
            require_engine_sync_status=True,
        )
    )
    errors.extend(
        lint_tiles_canon_dict(
            studio_tiles,
            source_label="docs/data/amazonia_data_v6_0.js[CATALOGUE_TUILES]",
            require_engine_sync_status=False,
        )
    )

    if canon_tiles != studio_tiles:
        errors.append(
            "Désynchronisation entre contracts/tiles_canon_v6_2.json['tuiles_ciblees'] "
            "et docs/data/amazonia_data_v6_0.js['CATALOGUE_TUILES']"
        )

    if errors:
        raise RuntimeError("VIOLATION Linter Tuiles Canon 0 :\n" + "\n".join(errors))

    faces_total = sum(
        len([p for p in _BR_SPLIT_RE.split(str(prof.get("texte", ""))) if p.strip()])
        for slot in canon_tiles.values()
        for prof in slot["profils"].values()
    )
    print(
        f"[5/10] Linter Tuiles Canon 0 ({len(canon_tiles)} slots, {faces_total} faces ≤ 25 mots, "
        "clôture I & autonomie A=0) : OK"
    )


def verify_global_anti_vestiges() -> None:
    """Scanner global anti-vestiges sur contracts/*.json, docs/data/*.json, STUDIO_CONTEXT et .agents/**/*.md."""
    guards: dict[str, Any] = json.loads(GUARDS_FILE.read_text(encoding="utf-8"))
    banned_patterns: list[str] = [str(p) for p in guards.get("banned_global_vestiges", [])]
    if not banned_patterns:
        raise RuntimeError("Liste 'banned_global_vestiges' vide dans studio_rules_guards.json")

    targets: list[Path] = []
    for f in sorted(CONTRACTS_DIR.glob("*.json")):
        if f.name == GUARDS_FILE.name:
            continue
        targets.append(f)
    targets.extend(sorted(DOCS_DATA_DIR.glob("*.json")))
    if STUDIO_CONTEXT_FILE.is_file():
        targets.append(STUDIO_CONTEXT_FILE)
    agents_dir = ROOT / ".agents"
    if agents_dir.is_dir():
        targets.extend(sorted(agents_dir.rglob("*.md")))

    errors: list[str] = []
    for path in targets:
        rel = path.relative_to(ROOT).as_posix()
        txt = path.read_text(encoding="utf-8")
        for pat in banned_patterns:
            if pat in txt:
                errors.append(f"{rel}: vestige interdit {pat!r} détecté")

    if errors:
        raise RuntimeError("VIOLATION Scanner Global Anti-Vestiges :\n" + "\n".join(errors))
    print(
        f"[6/10] Scanner global anti-vestiges ({len(targets)} fichiers contrats/docs/.agents) : OK"
    )


def verify_studio_coherence() -> None:
    """Vérifie la cohérence SSOT v6.2 entre contracts/, docs/data/ et le simulateur Python.

    Contrôles actifs :
    - Existence & empreintes SHA-256 des 3 contrats SSOT (`rules_canon_v6_2`, `invariants` 22, `tiles_canon_v6_2`) ;
    - `docs/data/spec_formelle_v6_0.json == data/spec_bundle_v6_0.json['spec_formelle_v6_0']` ;
    - Topologie canonique `P4_2233` dans `catalog_v6_0.json` == `engine.state.CANONICAL_DOTATION (2,2,3,3)` ;
    - Châssis verrouillé (`Placement_Initial_Machines.defaultVal == 'BULLDOZER_P1_ABATTEUSE_P2'`) ;
    - Réglette des Tactiques `T1..T6` == `engine.state.TACTIQUES_SPEC` ;
    - Empreintes SHA-256 de `data/studio_lock.json` alignées avec `docs/data/` et `contracts/`.
    """
    studio_lock_file = ROOT / "data" / "studio_lock.json"
    for req_file in (
        RULES_CANON_FILE,
        INVARIANTS_FILE,
        TILES_CANON_FILE,
        STUDIO_CATALOG_FILE,
        STUDIO_SPEC_FILE,
        STUDIO_JS_FILE,
        SPEC_BUNDLE_FILE,
        studio_lock_file,
    ):
        if not req_file.is_file():
            raise FileNotFoundError(f"Fichier SSOT/Studio manquant : {req_file}")

    invariants_doc: dict[str, Any] = json.loads(INVARIANTS_FILE.read_text(encoding="utf-8"))
    catalog: dict[str, Any] = json.loads(STUDIO_CATALOG_FILE.read_text(encoding="utf-8"))
    spec_doc: dict[str, Any] = json.loads(STUDIO_SPEC_FILE.read_text(encoding="utf-8"))
    bundle: dict[str, Any] = json.loads(SPEC_BUNDLE_FILE.read_text(encoding="utf-8"))
    lock_doc: dict[str, Any] = json.loads(studio_lock_file.read_text(encoding="utf-8"))
    studio_js = _load_studio_js_catalog_and_axes(STUDIO_JS_FILE)

    errors: list[str] = []

    # 0. Registre permanent des 22 invariants INV-01..INV-22
    inv_ids = [str(item.get("id", "")) for item in invariants_doc.get("invariants", [])]
    expected_inv_ids = [f"INV-{i:02d}" for i in range(1, 23)]
    if inv_ids != expected_inv_ids:
        errors.append(
            f"Registre invariants invalide : attendu {expected_inv_ids[0]}..{expected_inv_ids[-1]}, "
            f"obtenu {inv_ids}"
        )

    # 1. Cohérence spec_formelle_v6_0.json <-> bundle
    if bundle.get("spec_formelle_v6_0") != spec_doc:
        errors.append(
            "Désynchronisation entre docs/data/spec_formelle_v6_0.json et "
            "data/spec_bundle_v6_0.json['spec_formelle_v6_0']"
        )

    from engine.state import CANONICAL_DOTATION, CANONICAL_PROFIL_PISTE, TACTIQUES_SPEC

    # 2. Châssis canonique unique P4_2233 : docs/data/catalog_v6_0.json <-> engine.state
    topos_cat = catalog.get("topologies", {})
    if CANONICAL_PROFIL_PISTE not in topos_cat:
        errors.append(
            f"Topologie canonique {CANONICAL_PROFIL_PISTE!r} absente de docs/data/catalog_v6_0.json"
        )
    else:
        cat_dot = tuple(
            int(x) for x in topos_cat[CANONICAL_PROFIL_PISTE]["seuil_imprime_et_dotation"]
        )
        if cat_dot != CANONICAL_DOTATION:
            errors.append(
                f"Dotation {CANONICAL_PROFIL_PISTE} dans catalog_v6_0.json ({cat_dot}) != "
                f"engine.state.CANONICAL_DOTATION ({CANONICAL_DOTATION})"
            )

    # 3. Cohérence Studio <-> spec_bundle & verrouillage C3-06
    studio_axes_raw: list[dict[str, Any]] = studio_js["CHASSIS_AXES_SPEC"]
    bundle_axes_raw: list[dict[str, Any]] = bundle["chassis_axes"]

    def _norm_axes(axes_list: list[dict[str, Any]]) -> list[tuple[str, Any, tuple[Any, ...]]]:
        return [
            (str(ax["key"]).lower(), ax.get("defaultVal"), tuple(opt["val"] for opt in ax["options"]))
            for ax in axes_list
        ]

    if _norm_axes(studio_axes_raw) != _norm_axes(bundle_axes_raw):
        errors.append(
            "Désynchronisation entre docs/data/amazonia_data_v6_0.js['CHASSIS_AXES_SPEC'] "
            "et data/spec_bundle_v6_0.json['chassis_axes']"
        )

    placement_ax = next(
        (ax for ax in studio_axes_raw if ax.get("key") == "Placement_Initial_Machines"),
        None,
    )
    if placement_ax is None or placement_ax.get("defaultVal") != "BULLDOZER_P1_ABATTEUSE_P2":
        errors.append(
            "Bug C3-06 actif : Placement_Initial_Machines.defaultVal doit valoir 'BULLDOZER_P1_ABATTEUSE_P2'"
        )

    # 4. Réglette des Tactiques T1..T6 : spec_bundle <-> engine.state.TACTIQUES_SPEC
    bundle_tactiques = bundle.get("tactiques", [])
    if len(bundle_tactiques) != 6:
        errors.append(f"tactiques bundle invalides (attendu 6, obtenu {len(bundle_tactiques)})")
    else:
        for idx, b_tac in enumerate(bundle_tactiques, start=1):
            e_tac = TACTIQUES_SPEC[idx]
            if (
                tuple(b_tac.get("cibles", ())) != e_tac.cibles
                or int(b_tac.get("avancee", -99)) != e_tac.avancee
                or int(b_tac.get("mod_seuil", -99)) != e_tac.mod_seuil
                or int(b_tac.get("gain_rouge", -99)) != e_tac.gain_rouge
            ):
                errors.append(
                    f"Écart Tactique T{idx} entre spec_bundle ({b_tac}) et TACTIQUES_SPEC ({e_tac})"
                )

    # 5. Empreintes SHA-256 du Studio et des contrats verrouillées dans data/studio_lock.json
    for fname, info in lock_doc.get("files", {}).items():
        expected_sha = str(info.get("sha256", "")).lower()
        target_f = DOCS_DATA_DIR / str(fname)
        if not target_f.is_file():
            errors.append(f"Fichier Studio listé dans studio_lock.json introuvable : {fname}")
        else:
            actual_sha = hashlib.sha256(target_f.read_bytes()).hexdigest().lower()
            if actual_sha != expected_sha:
                errors.append(
                    f"Empreinte SHA-256 Studio divergente sur {fname} : "
                    f"attendu {expected_sha[:12]}, obtenu {actual_sha[:12]}"
                )

    for cname, info in lock_doc.get("contracts", {}).items():
        expected_sha = str(info.get("sha256", "")).lower()
        target_c = CONTRACTS_DIR / str(cname)
        if not target_c.is_file():
            errors.append(f"Contrat SSOT listé dans studio_lock.json introuvable : {cname}")
        else:
            actual_sha = hashlib.sha256(target_c.read_bytes()).hexdigest().lower()
            if actual_sha != expected_sha:
                errors.append(
                    f"Empreinte SHA-256 Contrat SSOT divergente sur {cname} : "
                    f"attendu {expected_sha[:12]}, obtenu {actual_sha[:12]} "
                    "(exécuter scripts/build_studio_artifacts.py)"
                )

    if errors:
        raise RuntimeError("VIOLATION Cohérence SSOT Studio <-> Simulateur :\n" + "\n".join(errors))
    print(
        f"[4/10] Cohérence SSOT v6.2 (contracts/ <-> docs/data/ <-> simulateur : "
        f"22 invariants, châssis unique {CANONICAL_PROFIL_PISTE}, 6 tactiques, studio_lock) : OK"
    )


def _find_uv() -> str:
    found = shutil.which("uv")
    if found:
        return found
    bin_names = ("uv.exe", "uv") if os.name == "nt" else ("uv",)
    home = Path.home()
    for folder in (home / ".local" / "bin", home / ".cargo" / "bin"):
        for bname in bin_names:
            cand = folder / bname
            if cand.exists():
                return str(cand)
    raise FileNotFoundError("Impossible de trouver l'exécutable 'uv'.")


def run_tool(step_label: str, cmd: list[str]) -> None:
    """Exécute un outil de contrôle et échoue si le code de retour != 0."""
    print(f"{step_label} -> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    verify_kernel_locks()
    verify_effects_ast()
    verify_zero_llm_api_billing()
    verify_studio_coherence()
    verify_tiles_canon()
    verify_global_anti_vestiges()
    run_tool("[7/10] ruff", [sys.executable, "-m", "ruff", "check", "."])
    run_tool("[8/10] pyright", [sys.executable, "-m", "pyright"])
    run_tool("[9/10] pytest", [sys.executable, "-m", "pytest", "-q"])
    uv_bin = _find_uv()
    run_tool(
        "[10/10] PyPy Invariant Fuzzer",
        [
            uv_bin,
            "run",
            "--no-project",
            "--python",
            "pypy@3.11",
            "python",
            "scripts_cloud/fuzz_invariants.py",
            "--games",
            "1000",
        ],
    )
    print("verify_lot.py : 10/10 PORTES 100% VERT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
