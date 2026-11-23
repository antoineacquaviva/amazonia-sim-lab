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
    """Vérifie la cohérence du Cœur entre docs/data/ (Studio) et le simulateur Python v6.1.

    Contrôles actifs :
    - docs/data/spec_formelle_v6_0.json == data/spec_bundle_v6_0.json['spec_formelle_v6_0'] ;
    - Topologie canonique P4_2233 dans catalog_v6_0.json == engine.state.CANONICAL_DOTATION (2,2,3,3) ;
    - Cohérence interne Studio (amazonia_data_v6_0.js <-> data/spec_bundle_v6_0.json) ;
    - Réglette des Tactiques T1..T6 == engine.state.TACTIQUES_SPEC ;
    - Empreintes SHA-256 de data/studio_lock.json alignées avec docs/data/.
    """
    studio_lock_file = ROOT / "data" / "studio_lock.json"
    for req_file in (
        STUDIO_CATALOG_FILE,
        STUDIO_SPEC_FILE,
        STUDIO_JS_FILE,
        SPEC_BUNDLE_FILE,
        studio_lock_file,
    ):
        if not req_file.is_file():
            raise FileNotFoundError(f"Fichier Studio/Simulateur manquant : {req_file}")

    catalog: dict[str, Any] = json.loads(STUDIO_CATALOG_FILE.read_text(encoding="utf-8"))
    spec_doc: dict[str, Any] = json.loads(STUDIO_SPEC_FILE.read_text(encoding="utf-8"))
    bundle: dict[str, Any] = json.loads(SPEC_BUNDLE_FILE.read_text(encoding="utf-8"))
    lock_doc: dict[str, Any] = json.loads(studio_lock_file.read_text(encoding="utf-8"))
    studio_js = _load_studio_js_catalog_and_axes(STUDIO_JS_FILE)

    errors: list[str] = []

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

    # 3. Cohérence interne Studio <-> spec_bundle sur les métadonnées Studio
    studio_axes_raw: list[dict[str, Any]] = studio_js["CHASSIS_AXES_SPEC"]
    bundle_axes_raw: list[dict[str, Any]] = bundle["chassis_axes"]

    def _norm_axes(axes_list: list[dict[str, Any]]) -> list[tuple[str, tuple[Any, ...]]]:
        return [
            (str(ax["key"]).lower(), tuple(opt["val"] for opt in ax["options"]))
            for ax in axes_list
        ]

    if _norm_axes(studio_axes_raw) != _norm_axes(bundle_axes_raw):
        errors.append(
            "Désynchronisation entre docs/data/amazonia_data_v6_0.js['CHASSIS_AXES_SPEC'] "
            "et data/spec_bundle_v6_0.json['chassis_axes']"
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

    # 5. Empreintes SHA-256 du Studio verrouillées dans data/studio_lock.json
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

    if errors:
        raise RuntimeError("VIOLATION Cohérence Studio <-> Simulateur :\n" + "\n".join(errors))
    print(
        f"[4/8] Cohérence Socle v6.1 Studio (docs/data/ <-> simulateur : "
        f"spec_formelle, châssis unique {CANONICAL_PROFIL_PISTE}, 6 tactiques, studio_lock) : OK"
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
