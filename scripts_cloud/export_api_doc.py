"""Génère automatiquement contracts/core_state_api.md par inspection AST du noyau public."""

from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DOC = ROOT / "contracts" / "core_state_api.md"

TARGET_MODULES: tuple[tuple[str, str], ...] = (
    ("engine/state.py", "État de jeu (`engine.state`)"),
    ("engine/rng.py", "PRNG adressable par événement (`engine.rng`)"),
    ("engine/primitives.py", "Bus des 7 Primitives & Hooks Mode 4 (`engine.primitives`)"),
    ("engine/effects/registry.py", "Registre stateless des tuiles (`engine.effects.registry`)"),
)


def _first_doc_line(node: ast.AST) -> str:
    doc = ast.get_docstring(node)  # type: ignore[arg-type]
    if not doc:
        return ""
    return " ".join(line.strip() for line in doc.strip().splitlines() if line.strip())


def _format_func_sig(fn: ast.FunctionDef) -> str:
    args_str = ast.unparse(fn.args)
    ret_str = f" -> {ast.unparse(fn.returns)}" if fn.returns is not None else ""
    return f"{fn.name}({args_str}){ret_str}"


def _extract_module_markdown(rel_path: str, title: str) -> list[str]:
    src = (ROOT / rel_path).read_text(encoding="utf-8")
    tree = ast.parse(src, filename=rel_path)
    lines: list[str] = [f"## {title}", "", f"*Source : `{rel_path}`*", ""]

    mod_doc = _first_doc_line(tree)
    if mod_doc:
        lines.extend([f"> {mod_doc}", ""])

    constants: list[str] = []
    functions: list[tuple[str, str]] = []
    classes: list[ast.ClassDef] = []

    for stmt in tree.body:
        if isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
            name = stmt.target.id
            if not name.startswith("_") and name != "__all__":
                ann = ast.unparse(stmt.annotation)
                val = f" = {ast.unparse(stmt.value)}" if stmt.value is not None else ""
                if len(val) > 70:
                    val = " = ..."
                constants.append(f"- `{name}: {ann}{val}`")
        elif isinstance(stmt, ast.Assign):
            for tgt in stmt.targets:
                if isinstance(tgt, ast.Name) and not tgt.id.startswith("_") and tgt.id != "__all__":
                    val = ast.unparse(stmt.value)
                    if len(val) > 70:
                        val = "..."
                    constants.append(f"- `{tgt.id} = {val}`")
        elif isinstance(stmt, ast.FunctionDef) and not stmt.name.startswith("_"):
            functions.append((_format_func_sig(stmt), _first_doc_line(stmt)))
        elif isinstance(stmt, ast.ClassDef) and not stmt.name.startswith("_"):
            classes.append(stmt)

    if constants:
        lines.extend(["### Constantes publiques", "", *constants, ""])

    if functions:
        lines.extend(["### Fonctions publiques", ""])
        for sig, doc in functions:
            suffix = f" — {doc}" if doc else ""
            lines.append(f"- `{sig}`{suffix}")
        lines.append("")

    for cls in classes:
        cls_doc = _first_doc_line(cls)
        lines.append(f"### Classe `{cls.name}`")
        lines.append("")
        if cls_doc:
            lines.extend([cls_doc, ""])

        fields: list[str] = []
        props: list[tuple[str, str]] = []
        methods: list[tuple[str, str]] = []

        for item in cls.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                fname = item.target.id
                if not fname.startswith("_"):
                    fields.append(f"- `{fname}: {ast.unparse(item.annotation)}`")
            elif isinstance(item, ast.FunctionDef) and not item.name.startswith("_"):
                decos = {
                    ast.unparse(d)
                    for d in item.decorator_list
                }
                if "property" in decos:
                    ret = ast.unparse(item.returns) if item.returns is not None else "Any"
                    props.append((f"{item.name}: {ret}", _first_doc_line(item)))
                elif any(d.endswith(".setter") for d in decos):
                    continue
                else:
                    methods.append((_format_func_sig(item), _first_doc_line(item)))

        if fields:
            lines.extend(["**Champs :**", *fields, ""])
        if props:
            lines.append("**Propriétés :**")
            for p_sig, p_doc in props:
                suffix = f" — {p_doc}" if p_doc else ""
                lines.append(f"- `{p_sig}`{suffix}")
            lines.append("")
        if methods:
            lines.append("**Méthodes :**")
            for m_sig, m_doc in methods:
                suffix = f" — {m_doc}" if m_doc else ""
                lines.append(f"- `{m_sig}`{suffix}")
            lines.append("")

    return lines


def export_api_doc() -> Path:
    """Génère contracts/core_state_api.md et retourne son chemin."""
    header = [
        "# Contrat API Publique du Noyau Scellé (`core_state_api.md`)",
        "",
        "Ce document est généré automatiquement par `scripts_cloud/export_api_doc.py` via inspection AST.",
        "Les modules d'effets stateless dans `engine/effects/*.py` doivent utiliser **exclusivement**",
        "les constantes, structures, accesseurs et primitives listés ci-dessous (zéro accès à `_buf`,",
        "zéro `import random`, zéro état global mutable).",
        "",
        "---",
        "",
    ]
    body: list[str] = list(header)
    for rel_path, title in TARGET_MODULES:
        body.extend(_extract_module_markdown(rel_path, title))

    OUT_DOC.parent.mkdir(parents=True, exist_ok=True)
    OUT_DOC.write_text("\n".join(body).rstrip() + "\n", encoding="utf-8", newline="\n")
    return OUT_DOC


def main() -> int:
    out = export_api_doc()
    print(f"Wrote {out.relative_to(ROOT).as_posix()} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
