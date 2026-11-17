"""Garde-fou local de validation de lot pour amazonia-sim-lab."""

from __future__ import annotations

import ast
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOCKS_FILE = ROOT / "contracts" / "kernel_locks.sha256"
EFFECTS_DIR = ROOT / "engine" / "effects"
UPPER_CASE_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


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
        print("[1/5] kernel_locks.sha256 vide (Palier 0) : OK")
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
    print(f"[1/5] kernel_locks.sha256 ({len(lines)} fichiers) : OK")


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
    print(f"[2/5] AST engine/effects/ ({len(py_files)} fichiers) : OK")


def run_tool(step_label: str, cmd: list[str]) -> None:
    """Exécute un outil de contrôle et échoue si le code de retour != 0."""
    print(f"{step_label} -> {' '.join(cmd)}")
    subprocess.run(cmd, cwd=ROOT, check=True)


def main() -> int:
    verify_kernel_locks()
    verify_effects_ast()
    run_tool("[3/5] ruff", [sys.executable, "-m", "ruff", "check", "."])
    run_tool("[4/5] pyright", [sys.executable, "-m", "pyright"])
    run_tool("[5/5] pytest", [sys.executable, "-m", "pytest", "-q"])
    print("verify_lot.py : 100% VERT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
