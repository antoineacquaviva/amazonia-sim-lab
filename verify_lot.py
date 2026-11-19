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
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
LOCKS_FILE = ROOT / "contracts" / "kernel_locks.sha256"
EFFECTS_DIR = ROOT / "engine" / "effects"
PYPROJECT_FILE = ROOT / "pyproject.toml"
DOCS_DATA_DIR = ROOT / "docs" / "data"
STUDIO_CATALOG_FILE = DOCS_DATA_DIR / "catalog_v5_4.json"
STUDIO_SPEC_FILE = DOCS_DATA_DIR / "spec_formelle_v5_4.json"
STUDIO_JS_FILE = DOCS_DATA_DIR / "amazonia_data_v5_4.js"
SPEC_BUNDLE_FILE = ROOT / "data" / "spec_bundle_v5_4.json"
UPPER_CASE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")

_SKIP_DIRS: frozenset[str] = frozenset(
    {".git", ".venv", ".tmp_runs", "__pycache__", ".pytest_cache", ".ruff_cache"}
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
        print("[1/8] kernel_locks.sha256 vide (Palier 0) : OK")
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
    print(f"[1/8] kernel_locks.sha256 ({len(lines)} fichiers) : OK")


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
    print(f"[2/8] AST engine/effects/ ({len(py_files)} fichiers) : OK")


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
    print(f"[3/8] Garde Zéro-API-LLM ({scanned_py} fichiers Python) : OK")


def _load_studio_js_catalog_and_axes(studio_js_path: Path) -> dict[str, Any]:
    """Charge CATALOGUE_TUILES et CHASSIS_AXES_SPEC depuis docs/data/amazonia_data_v5_3.js via Node vm."""
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


def verify_studio_coherence() -> None:
    """Vérifie la cohérence exacte entre docs/data/ (Studio) et le simulateur Python.

    Contrôle :
    - 32 emplacements et 100 profils déclarés dans docs/data/catalog_v5_3.json & amazonia_data_v5_3.js
      == data/spec_bundle_v5_3_1.json == registre @register_tile du simulateur ;
    - 7 axes du châssis (clés + couples de valeurs) == engine.state.CHASSIS_AXES_OPTIONS ;
    - Topologies (P4_2233, P5_22233) == engine.state.TOPOLOGIES_DOTATION ;
    - docs/data/spec_formelle_v5_3.json == spec_bundle_v5_3_1.json['spec_formelle_v5_3'].
    """
    for req_file in (STUDIO_CATALOG_FILE, STUDIO_SPEC_FILE, STUDIO_JS_FILE, SPEC_BUNDLE_FILE):
        if not req_file.is_file():
            raise FileNotFoundError(f"Fichier Studio/Simulateur manquant : {req_file}")

    catalog: dict[str, Any] = json.loads(STUDIO_CATALOG_FILE.read_text(encoding="utf-8"))
    spec_doc: dict[str, Any] = json.loads(STUDIO_SPEC_FILE.read_text(encoding="utf-8"))
    bundle: dict[str, Any] = json.loads(SPEC_BUNDLE_FILE.read_text(encoding="utf-8"))
    studio_js = _load_studio_js_catalog_and_axes(STUDIO_JS_FILE)

    errors: list[str] = []

    # 1. Compteurs déclarés dans docs/data/catalog_v5_4.json
    decl_slots = catalog.get("total_emplacements")
    decl_profiles = catalog.get("total_profils")
    if decl_slots != 32:
        errors.append(f"docs/data/catalog_v5_4.json: total_emplacements={decl_slots} (attendu 32)")
    if decl_profiles != 100:
        errors.append(f"docs/data/catalog_v5_4.json: total_profils={decl_profiles} (attendu 100)")

    arch_ref = catalog.get("spec_formelle_v5_4", {}).get("architecture_reference", {})
    arch_slots = int(arch_ref.get("total_emplacements_synergie", 0)) + int(
        arch_ref.get("total_pistes_migration", 0)
    )
    if arch_slots != 32 or arch_ref.get("total_profils") != 100:
        errors.append(
            f"docs/data/catalog_v5_4.json architecture_reference incohérente "
            f"(slots={arch_slots}, profils={arch_ref.get('total_profils')})"
        )

    # 2. Cohérence spec_formelle_v5_4.json <-> bundle
    if bundle.get("spec_formelle_v5_4") != spec_doc:
        errors.append(
            "Désynchronisation entre docs/data/spec_formelle_v5_4.json et "
            "data/spec_bundle_v5_4.json['spec_formelle_v5_4']"
        )

    # 3. 32 emplacements & 100 profils : Studio JS/JSON <-> spec_bundle <-> registre Python
    from engine.core_engine import ensure_builtin_migration_registered
    from engine.effects import load_all_effects
    from engine.effects.registry import clear_tile_registry, list_registered_tiles
    from engine.state import CHASSIS_AXES_OPTIONS, TOPOLOGIES_DOTATION

    clear_tile_registry()
    ensure_builtin_migration_registered()
    load_all_effects()
    registered_pairs: set[tuple[str, str]] = set(list_registered_tiles())
    registered_slots: set[str] = {slot for slot, _ in registered_pairs}

    studio_cat: dict[str, Any] = studio_js["CATALOGUE_TUILES"]
    studio_slots: set[str] = set(studio_cat.keys())
    studio_pairs: set[tuple[str, str]] = {
        (slot_id, prof_key)
        for slot_id, slot_meta in studio_cat.items()
        for prof_key in slot_meta["profils"]
    }

    bundle_cat: dict[str, Any] = bundle["catalogue_tuiles"]
    bundle_slots: set[str] = set(bundle_cat.keys())
    bundle_pairs: set[tuple[str, str]] = {
        (slot_id, prof_key)
        for slot_id, slot_meta in bundle_cat.items()
        for prof_key in slot_meta["profils"]
    }

    if len(studio_slots) != decl_slots or len(studio_pairs) != decl_profiles:
        errors.append(
            f"Studio JS ({len(studio_slots)} slots, {len(studio_pairs)} profils) != "
            f"catalog_v5_4.json ({decl_slots} slots, {decl_profiles} profils)"
        )
    if studio_slots != bundle_slots or studio_slots != registered_slots:
        errors.append(
            f"Écart sur les 32 emplacements : "
            f"studio-sim={sorted(studio_slots - registered_slots)}, "
            f"sim-studio={sorted(registered_slots - studio_slots)}, "
            f"studio-bundle={sorted(studio_slots - bundle_slots)}"
        )
    if studio_pairs != bundle_pairs or studio_pairs != registered_pairs:
        errors.append(
            f"Écart sur les 100 profils : "
            f"studio-sim={sorted(studio_pairs - registered_pairs)}, "
            f"sim-studio={sorted(registered_pairs - studio_pairs)}, "
            f"studio-bundle={sorted(studio_pairs - bundle_pairs)}"
        )

    # Si catalog_v5_4.json expose directement catalogue_tuiles, on le vérifie aussi
    if isinstance(catalog.get("catalogue_tuiles"), dict):
        cat_json_pairs = {
            (slot_id, prof_key)
            for slot_id, slot_meta in catalog["catalogue_tuiles"].items()
            for prof_key in slot_meta["profils"]
        }
        if cat_json_pairs != registered_pairs:
            errors.append("Écart entre catalog_v5_4.json['catalogue_tuiles'] et le simulateur")

    # 4. Topologies déclarées dans docs/data/catalog_v5_4.json <-> engine.state.TOPOLOGIES_DOTATION
    cat_topos: dict[str, tuple[int, ...]] = {
        str(code): tuple(int(x) for x in meta["seuil_imprime_et_dotation"])
        for code, meta in catalog.get("topologies", {}).items()
    }
    if cat_topos != TOPOLOGIES_DOTATION:
        errors.append(
            f"Topologies docs/data/catalog_v5_4.json ({cat_topos}) != "
            f"engine.state.TOPOLOGIES_DOTATION ({TOPOLOGIES_DOTATION})"
        )

    # 5. 7 axes du châssis : Studio <-> spec_bundle <-> engine.state.CHASSIS_AXES_OPTIONS
    studio_axes_raw: list[dict[str, Any]] = studio_js["CHASSIS_AXES_SPEC"]
    bundle_axes_raw: list[dict[str, Any]] = bundle["chassis_axes"]

    def _norm_axes(axes_list: list[dict[str, Any]]) -> list[tuple[str, tuple[Any, ...]]]:
        return [
            (str(ax["key"]).lower(), tuple(opt["val"] for opt in ax["options"]))
            for ax in axes_list
        ]

    studio_axes = _norm_axes(studio_axes_raw)
    bundle_axes = _norm_axes(bundle_axes_raw)
    engine_axes = [(name.lower(), tuple(opts)) for name, opts in CHASSIS_AXES_OPTIONS]

    if len(studio_axes) != 7 or studio_axes != bundle_axes or studio_axes != engine_axes:
        errors.append(
            f"Écart sur les 7 axes du châssis :\n"
            f"  Studio : {studio_axes}\n"
            f"  Bundle : {bundle_axes}\n"
            f"  Engine : {engine_axes}"
        )

    if errors:
        raise RuntimeError("VIOLATION Cohérence Studio <-> Simulateur :\n" + "\n".join(errors))
    print(
        f"[4/8] Cohérence Studio (docs/data/ <-> simulateur : "
        f"{len(registered_slots)} emplacements, {len(registered_pairs)} profils, "
        f"{len(engine_axes)} axes châssis) : OK"
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
    run_tool("[5/8] ruff", [sys.executable, "-m", "ruff", "check", "."])
    run_tool("[6/8] pyright", [sys.executable, "-m", "pyright"])
    run_tool("[7/8] pytest", [sys.executable, "-m", "pytest", "-q"])
    uv_bin = _find_uv()
    run_tool(
        "[8/8] PyPy Invariant Fuzzer",
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
    print("verify_lot.py : 8/8 PORTES 100% VERT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
