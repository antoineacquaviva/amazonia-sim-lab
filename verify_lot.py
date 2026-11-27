"""Garde-fou local de validation de lot pour amazonia-sim-lab (Windows 11 & Ubuntu Linux)."""

from __future__ import annotations

import ast
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import textwrap
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CONTRACTS_DIR = ROOT / "contracts"
LOCKS_FILE = CONTRACTS_DIR / "kernel_locks.sha256"
SOCLE_V6_2_LOCKS_FILE = CONTRACTS_DIR / "v6_2_socle_locks.sha256"
RULES_CANON_FILE = CONTRACTS_DIR / "rules_canon_v6_2.json"
INVARIANTS_FILE = CONTRACTS_DIR / "physical_and_edge_invariants.json"
TILES_CANON_FILE = CONTRACTS_DIR / "tiles_canon_v6_2.json"
TILES_CANON_V6_3_FILE = CONTRACTS_DIR / "tiles_canon_v6_3.json"
TILES_CANON_V6_3_SCHEMA_FILE = CONTRACTS_DIR / "tiles_canon_v6_3.schema.json"
RULES_CANON_V6_4_FILE = CONTRACTS_DIR / "rules_canon_v6_4.json"
INVARIANTS_V6_4_FILE = CONTRACTS_DIR / "physical_and_edge_invariants_v6_4.json"
TILES_CANON_V6_4_FILE = CONTRACTS_DIR / "tiles_canon_v6_4.json"
TILES_CANON_V6_4_SCHEMA_FILE = CONTRACTS_DIR / "tiles_canon_v6_4.schema.json"
PANELS_DIR = CONTRACTS_DIR / "panels"
GUARDS_FILE = CONTRACTS_DIR / "studio_rules_guards.json"
EFFECTS_DIR = ROOT / "engine" / "effects"
PYPROJECT_FILE = ROOT / "pyproject.toml"
DOCS_DATA_DIR = ROOT / "docs" / "data"
STUDIO_CONTEXT_FILE = ROOT / "docs" / "AMAZONIA_STUDIO_CONTEXT.md"
STUDIO_CATALOG_FILE = DOCS_DATA_DIR / "catalog_v6_0.json"
STUDIO_SPEC_FILE = DOCS_DATA_DIR / "spec_formelle_v6_0.json"
STUDIO_JS_FILE = DOCS_DATA_DIR / "amazonia_data_v6_0.js"
STUDIO_LIVRET_JS_FILE = DOCS_DATA_DIR / "livret_v6_0.js"
STUDIO_CATALOG_V6_4_FILE = DOCS_DATA_DIR / "catalog_v6_4.json"
STUDIO_SPEC_V6_4_FILE = DOCS_DATA_DIR / "spec_formelle_v6_4.json"
STUDIO_CANON_V6_4_JS_FILE = DOCS_DATA_DIR / "canon_v6_4_data.js"
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

# Linter structurel des tuiles (I07 : ZÉRO comptage de mots, de phrases ni de conditions)
_FACE_LABEL_RE = re.compile(
    r"^\s*(?:Face\s+[12]|Enraciné|En\s+Parade|En\s+Migration)\s*:\s*",
    re.IGNORECASE,
)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_BR_SPLIT_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_STEP_CODE_RE = re.compile(r"\b[1-6]\.[0-3]\b")
_INSECT_LEXICON_RE = re.compile(r"(?i)\b(?:insectes?|nids?|essaims?|migrations?)\b")
_GARDIEN_LEXICON_RE = re.compile(r"(?i)\b(?:gardiens?|éveil|encoches?|résonance)\b")

_I_LISIERE_SLOTS: frozenset[str] = frozenset(
    {"G13", "G14", "G15", "R6", "R10", "M1", "M2", "M3", "M4", "M5"}
)
_A0_AUTONOMOUS_SLOTS: frozenset[str] = frozenset({"R1", "R2", "R6", "R10", "M4", "M5"})
_BANNED_TILE_TERMS: tuple[str, ...] = (
    "paquet",
    "carte Machine",
    "cartes Machine",
    "carte Sabotage",
    "cartes Sabotage",
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


def _verify_sha256_lock_file(lock_file: Path) -> int:
    """Vérifie toutes les empreintes SHA-256 déclarées dans un fichier de verrouillage."""
    if not lock_file.exists():
        raise FileNotFoundError(f"Fichier de verrouillage manquant : {lock_file}")
    lines = [
        line.strip()
        for line in lock_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    for line in lines:
        parts = line.split(maxsplit=1)
        if len(parts) != 2:
            raise ValueError(f"Ligne invalide dans {lock_file.name} : {line}")
        expected_hash, rel_path = parts[0].lower(), parts[1].strip().lstrip("*")
        target = ROOT / rel_path
        if not target.exists():
            raise FileNotFoundError(f"Fichier verrouillé absent : {rel_path}")
        actual_hash = hashlib.sha256(target.read_bytes()).hexdigest().lower()
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"VIOLATION {lock_file.name} sur {rel_path}: "
                f"attendu {expected_hash}, obtenu {actual_hash}"
            )
    return len(lines)


def verify_kernel_locks() -> None:
    """Vérifie les empreintes SHA-256 du noyau (`kernel_locks.sha256`) et du socle v6.2 (`v6_2_socle_locks.sha256`)."""
    n_kernel = _verify_sha256_lock_file(LOCKS_FILE)
    n_socle = _verify_sha256_lock_file(SOCLE_V6_2_LOCKS_FILE)
    print(
        f"[1/10] kernel_locks.sha256 ({n_kernel} fichiers noyau) + "
        f"v6_2_socle_locks.sha256 ({n_socle} contrats v6.2 sanctuarisés intacts) : OK"
    )


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
                if sync_status != "ACTIVE_VERIFIED":
                    errors.append(
                        f"{label}: engine_sync_status doit valoir 'ACTIVE_VERIFIED' "
                        f"(obtenu {sync_status!r} — 0 tuile PENDING tolérée)"
                    )

            raw_text = str(prof.get("texte", "")).strip()
            if not raw_text:
                errors.append(f"{label}: champ 'texte' vide")
                continue

            parts = [p.strip() for p in _BR_SPLIT_RE.split(raw_text) if p.strip()]
            for face_idx, part in enumerate(parts, start=1):
                no_html = _HTML_TAG_RE.sub("", part).strip()
                clean = _FACE_LABEL_RE.sub("", no_html).strip()

                # Invariant I07 : aucune vérification de nombre de mots, de phrases ou de conditions (C02 purgé).
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


def _is_trivial_noop_stmt(stmt: ast.stmt) -> bool:
    """Vrai si l'instruction AST ne produit aucun effet (docstring, pass, return None, `_ = ...`)."""
    if isinstance(stmt, ast.Pass):
        return True
    if isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
        return True
    if isinstance(stmt, ast.Return) and (
        stmt.value is None
        or (isinstance(stmt.value, ast.Constant) and stmt.value.value is None)
    ):
        return True
    return (
        isinstance(stmt, ast.Assign)
        and all(isinstance(t, ast.Name) and t.id == "_" for t in stmt.targets)
        and isinstance(stmt.value, (ast.Name, ast.Tuple, ast.Constant))
    )


def check_active_tile_handlers_non_noop(
    tiles_map: Mapping[str, Mapping[str, Any]],
) -> tuple[int, list[str]]:
    """Vérifie par AST que chaque profil `ACTIVE_VERIFIED` possède un handler enregistré non-no-op."""
    import engine.effects  # noqa: F401
    from engine.effects.registry import get_tile_registration

    checked = 0
    errors: list[str] = []
    for slot_id, slot in sorted(tiles_map.items()):
        profils = slot.get("profils")
        if not isinstance(profils, Mapping):
            continue
        for prof_key, prof in sorted(profils.items()):
            if prof.get("engine_sync_status") != "ACTIVE_VERIFIED":
                continue
            checked += 1
            reg = get_tile_registration(str(slot_id), str(prof_key))
            if reg is None:
                errors.append(
                    f"{slot_id}:{prof_key} marqué ACTIVE_VERIFIED mais absent du registre @register_tile"
                )
                continue
            if not reg.hooks:
                errors.append(
                    f"{slot_id}:{prof_key} enregistré sans aucun hook ({reg.handler.__name__})"
                )
                continue
            try:
                src = textwrap.dedent(inspect.getsource(reg.handler))
                tree = ast.parse(src)
            except (OSError, TypeError, SyntaxError) as exc:
                errors.append(
                    f"{slot_id}:{prof_key}: impossible d'analyser l'AST du handler {reg.handler!r} ({exc})"
                )
                continue
            fn_node = next(
                (n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))),
                None,
            )
            if fn_node is None or not any(
                not _is_trivial_noop_stmt(st) for st in fn_node.body
            ):
                errors.append(
                    f"{slot_id}:{prof_key}: handler no-op détecté ({reg.handler.__name__})"
                )
    return checked, errors


def verify_tiles_canon() -> None:
    """Linter structurel, audit 197 assises (I01..I07, C02 purgé) et contrats bi-composants v6.3 & v6.4."""
    for req_file, label in (
        (TILES_CANON_FILE, "Contrat tuiles Canon 0 v6.2"),
        (STUDIO_JS_FILE, "Fichier Studio JS"),
        (TILES_CANON_V6_3_SCHEMA_FILE, "Schéma JSON v6.3"),
        (TILES_CANON_V6_3_FILE, "Contrat bi-composant v6.3"),
        (TILES_CANON_V6_4_SCHEMA_FILE, "Schéma JSON v6.4"),
        (TILES_CANON_V6_4_FILE, "Contrat bi-composant v6.4"),
    ):
        if not req_file.is_file():
            raise FileNotFoundError(f"{label} manquant : {req_file}")

    from scripts.audit_197 import audit_panels_directory, audit_tiles_catalog_197
    from scripts.tiles_v6_3_schema import (
        validate_tiles_canon_v6_3,
        validate_tiles_canon_v6_4,
    )

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

    verified_handlers, noop_errors = check_active_tile_handlers_non_noop(canon_tiles)
    errors.extend(noop_errors)
    if verified_handlers != 30:
        errors.append(
            f"Nombre de profils ACTIVE_VERIFIED invalide : attendu 30, obtenu {verified_handlers}"
        )

    # Audit structurel sur les 197 assises + 4 murs porteurs M1..M4 (zéro C02) sur l'archive v6.2
    audit_v62 = audit_tiles_catalog_197(canon_doc, allow_draft=False)
    if audit_v62["verdict_global"] != "OK":
        errors.extend(f"audit_197[v6.2]: {e}" for e in audit_v62["errors"])

    # Validation du schéma JSON v6.3 et du contrat bi-composant tiles_canon_v6_3.json (Archive Passe 1)
    schema_v63 = json.loads(TILES_CANON_V6_3_SCHEMA_FILE.read_text(encoding="utf-8"))
    if not isinstance(schema_v63, dict) or "$defs" not in schema_v63:
        errors.append("contracts/tiles_canon_v6_3.schema.json invalide")
    v63_doc: dict[str, Any] = json.loads(TILES_CANON_V6_3_FILE.read_text(encoding="utf-8"))
    v63_is_draft = any(
        isinstance(t, Mapping) and t.get("statut_conception") == "A_CONCEVOIR"
        for t in (v63_doc.get("tuiles_ciblees") or {}).values()
    )
    errors.extend(
        f"tiles_canon_v6_3.json: {e}"
        for e in validate_tiles_canon_v6_3(v63_doc, strict=not v63_is_draft)
    )
    audit_v63 = audit_tiles_catalog_197(v63_doc, allow_draft=v63_is_draft)
    if audit_v63["verdict_global"] != "OK":
        errors.extend(f"audit_197[v6.3]: {e}" for e in audit_v63["errors"])

    # Validation stricte du schéma JSON v6.4 et du Canon Passe 2 tiles_canon_v6_4.json (0 erreur tolérée)
    schema_v64 = json.loads(TILES_CANON_V6_4_SCHEMA_FILE.read_text(encoding="utf-8"))
    if not isinstance(schema_v64, dict) or "$defs" not in schema_v64:
        errors.append("contracts/tiles_canon_v6_4.schema.json invalide")
    v64_doc: dict[str, Any] = json.loads(TILES_CANON_V6_4_FILE.read_text(encoding="utf-8"))
    errors.extend(
        f"tiles_canon_v6_4.json: {e}"
        for e in validate_tiles_canon_v6_4(v64_doc, strict=True)
    )
    audit_v64 = audit_tiles_catalog_197(v64_doc, allow_draft=False)
    if audit_v64["verdict_global"] != "OK":
        errors.extend(f"audit_197[v6.4]: {e}" for e in audit_v64["errors"])

    # Répertoire multi-panels (`contracts/panels/`) : JSON bien formé requis, audit diagnostic non bloquant
    panels_summary = "0 panel"
    if not PANELS_DIR.is_dir():
        errors.append(f"Répertoire multi-panels manquant : {PANELS_DIR}")
    else:
        panel_jsons = sorted(
            p
            for p in PANELS_DIR.glob("*.json")
            if p.is_file() and not p.name.startswith("author_workspace")
        )
        if panel_jsons:
            try:
                batch = audit_panels_directory(PANELS_DIR, allow_draft=False)
                ok_cnt = sum(1 for r in batch["comparison"] if r["verdict"] == "OK")
                panels_summary = f"{len(panel_jsons)} panels ({ok_cnt} OK)"
            except (json.JSONDecodeError, TypeError, KeyError) as exc:
                errors.append(f"contracts/panels/: JSON mal formé ({exc})")

    if errors:
        raise RuntimeError(
            "VIOLATION Linter Tuiles / Audit 197 / Schémas v6.3 & v6.4 :\n" + "\n".join(errors)
        )

    v63_mode = "DRAFT_V6_3" if v63_is_draft else "STRICT_V6_3"
    print(
        f"[5/10] Linter Tuiles + Audit 197 (M1..M4 + I01..I07) + Schémas v6.3 & v6.4 "
        f"({len(canon_tiles)} slots, C02 purgé, {verified_handlers}/30 ACTIVE_VERIFIED, "
        f"0 no-op, {v63_mode}, STRICT_V6_4, {panels_summary}) : OK"
    )


def verify_global_anti_vestiges() -> None:
    """Scanner global anti-vestiges + garde termes retirés v6.4 sur les artefacts actifs."""
    guards: dict[str, Any] = json.loads(GUARDS_FILE.read_text(encoding="utf-8"))
    banned_patterns: list[str] = [str(p) for p in guards.get("banned_global_vestiges", [])]
    if not banned_patterns:
        raise RuntimeError("Liste 'banned_global_vestiges' vide dans studio_rules_guards.json")
    banned_v64_retired: list[str] = [str(p) for p in guards.get("banned_v6_4_retired_terms", [])]

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

    # Garde stricte des termes retirés v6.4 uniquement sur les fichiers actifs v6.4 (archives v6.2/v6.3 isolées)
    v64_active_targets: list[Path] = [
        p
        for p in (
            RULES_CANON_V6_4_FILE,
            INVARIANTS_V6_4_FILE,
            TILES_CANON_V6_4_FILE,
            STUDIO_CATALOG_V6_4_FILE,
            STUDIO_SPEC_V6_4_FILE,
            STUDIO_LIVRET_JS_FILE,
            STUDIO_CONTEXT_FILE,
        )
        if p.is_file()
    ]
    for path in v64_active_targets:
        rel = path.relative_to(ROOT).as_posix()
        txt = path.read_text(encoding="utf-8")
        for pat in banned_v64_retired:
            if pat in txt:
                errors.append(f"{rel}: terme retiré v6.4 interdit {pat!r} détecté")

    if errors:
        raise RuntimeError("VIOLATION Scanner Global Anti-Vestiges :\n" + "\n".join(errors))
    print(
        f"[6/10] Scanner global anti-vestiges ({len(targets)} fichiers + "
        f"{len(v64_active_targets)} cibles actives v6.4) : OK"
    )


def _check_canon_v6_4_js_vm(canon_js_path: Path) -> dict[str, Any]:
    """Valide `docs/data/canon_v6_4_data.js` via Node `new vm.Script()` et renvoie ses métriques clés."""
    js_script = (
        "const fs = require('fs');\n"
        "const vm = require('vm');\n"
        "const ctx = { window: {} };\n"
        "vm.createContext(ctx);\n"
        f"const src = fs.readFileSync({json.dumps(canon_js_path.as_posix())}, 'utf8');\n"
        "new vm.Script(src, { filename: 'docs/data/canon_v6_4_data.js' }).runInContext(ctx);\n"
        "const out = vm.runInContext(\n"
        "  '({ verbes: Object.keys(SIX_VERBES_COEUR_V6_4 || {}), '\n"
        "  + 'invariants: (PHYSICAL_INVARIANTS_V6_4 || []).map(x => x.id), '\n"
        "  + 'pictos: Object.keys(REFERENTIEL_PICTOGRAMMES_V6_4 || {}), '\n"
        "  + 'slots_v64: Object.keys((CANON_V6_4 && CANON_V6_4.tuiles_ciblees) || {}), '\n"
        "  + 'slots_v63: Object.keys((CANON_V6_3_PASSE1 && CANON_V6_3_PASSE1.tuiles_ciblees) || {}) })', ctx);\n"
        "process.stdout.write(JSON.stringify(out));\n"
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


def verify_studio_coherence() -> None:
    """Vérifie la cohérence SSOT v6.4 (Studio actif) & v6.2 (runtime PyPy) entre contracts/, docs/data/ et engine/."""
    studio_lock_file = ROOT / "data" / "studio_lock.json"
    for req_file in (
        RULES_CANON_FILE,
        INVARIANTS_FILE,
        TILES_CANON_FILE,
        RULES_CANON_V6_4_FILE,
        INVARIANTS_V6_4_FILE,
        TILES_CANON_V6_4_FILE,
        STUDIO_CATALOG_FILE,
        STUDIO_SPEC_FILE,
        STUDIO_JS_FILE,
        STUDIO_LIVRET_JS_FILE,
        STUDIO_CATALOG_V6_4_FILE,
        STUDIO_SPEC_V6_4_FILE,
        STUDIO_CANON_V6_4_JS_FILE,
        SPEC_BUNDLE_FILE,
        studio_lock_file,
    ):
        if not req_file.is_file():
            raise FileNotFoundError(f"Fichier SSOT/Studio manquant : {req_file}")

    invariants_doc: dict[str, Any] = json.loads(INVARIANTS_FILE.read_text(encoding="utf-8"))
    invariants_v64_doc: dict[str, Any] = json.loads(INVARIANTS_V6_4_FILE.read_text(encoding="utf-8"))
    catalog: dict[str, Any] = json.loads(STUDIO_CATALOG_FILE.read_text(encoding="utf-8"))
    spec_doc: dict[str, Any] = json.loads(STUDIO_SPEC_FILE.read_text(encoding="utf-8"))
    spec_v64_doc: dict[str, Any] = json.loads(STUDIO_SPEC_V6_4_FILE.read_text(encoding="utf-8"))
    catalog_v64: dict[str, Any] = json.loads(STUDIO_CATALOG_V6_4_FILE.read_text(encoding="utf-8"))
    bundle: dict[str, Any] = json.loads(SPEC_BUNDLE_FILE.read_text(encoding="utf-8"))
    lock_doc: dict[str, Any] = json.loads(studio_lock_file.read_text(encoding="utf-8"))
    studio_js = _load_studio_js_catalog_and_axes(STUDIO_JS_FILE)
    v64_js_meta = _check_canon_v6_4_js_vm(STUDIO_CANON_V6_4_JS_FILE)

    errors: list[str] = []

    # 0. Registres permanents des 22 invariants INV-01..INV-22 (v6.2 & v6.4)
    expected_inv_ids = [f"INV-{i:02d}" for i in range(1, 23)]
    for lbl, doc in (
        ("physical_and_edge_invariants.json", invariants_doc),
        ("physical_and_edge_invariants_v6_4.json", invariants_v64_doc),
    ):
        inv_ids = [str(item.get("id", "")) for item in doc.get("invariants", [])]
        if inv_ids != expected_inv_ids:
            errors.append(
                f"Registre invariants invalide ({lbl}) : attendu {expected_inv_ids[0]}..{expected_inv_ids[-1]}, "
                f"obtenu {inv_ids}"
            )

    # 0b. Cohérence Studio v6.4 compilé (canon_v6_4_data.js, spec_formelle_v6_4.json, catalog_v6_4.json, studio_lock)
    if str(spec_v64_doc.get("schema_version")) != "6.4.0":
        errors.append(
            f"docs/data/spec_formelle_v6_4.json schema_version attendu '6.4.0', obtenu {spec_v64_doc.get('schema_version')!r}"
        )
    if str(catalog_v64.get("schema_version")) != "6.4.0":
        errors.append(
            f"docs/data/catalog_v6_4.json schema_version attendu '6.4.0', obtenu {catalog_v64.get('schema_version')!r}"
        )
    if str(lock_doc.get("studio_version")) != "v6.4" or str(lock_doc.get("schema_version")) != "6.4.0":
        errors.append(
            f"data/studio_lock.json doit déclarer studio_version='v6.4' & schema_version='6.4.0' "
            f"(obtenu {lock_doc.get('studio_version')!r} / {lock_doc.get('schema_version')!r})"
        )
    if len(v64_js_meta.get("verbes", [])) != 6:
        errors.append(f"SIX_VERBES_COEUR_V6_4 doit contenir 6 verbes, obtenu {v64_js_meta.get('verbes')}")
    if v64_js_meta.get("invariants") != expected_inv_ids:
        errors.append("PHYSICAL_INVARIANTS_V6_4 dans canon_v6_4_data.js != INV-01..INV-22")
    pictos_v64 = list(v64_js_meta.get("pictos", []))
    if len(pictos_v64) != 31 or "PIC_PLUME" in pictos_v64:
        errors.append(f"REFERENTIEL_PICTOGRAMMES_V6_4 invalide (len={len(pictos_v64)}, PIC_PLUME={'PIC_PLUME' in pictos_v64})")
    if len(v64_js_meta.get("slots_v64", [])) != 30 or len(v64_js_meta.get("slots_v63", [])) != 30:
        errors.append(
            f"CANON_V6_4 / CANON_V6_3_PASSE1 doivent contenir 30 tuiles chacun "
            f"(obtenu {len(v64_js_meta.get('slots_v64', []))}/{len(v64_js_meta.get('slots_v63', []))})"
        )

    # 1. Cohérence spec_formelle_v6_0.json <-> bundle (runtime PyPy v6.2 sanctuarisé Phase A)
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
        f"[4/10] Cohérence SSOT v6.4 Studio + v6.2 Runtime (contracts/ <-> docs/data/ <-> simulateur : "
        f"22 invariants, 6 Verbes, 31 pictos, châssis unique {CANONICAL_PROFIL_PISTE}, studio_lock) : OK"
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
