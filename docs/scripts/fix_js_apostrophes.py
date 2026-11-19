#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Répare les apostrophes droites dans les chaînes JS de amazonia_data_v5_3.js."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


REPLACEMENTS_AUDIT_PY = [
    ("défausse immédiate d'Insectes", "défausse immédiate d’Insectes"),
    ("lors d'une parade classique", "lors d’une parade classique"),
    ("à l'instant où elle attaque.", "à l’instant où elle attaque."),
    ("jusqu'à deux parcelles non rasées (le bonus s'applique", "jusqu’à deux parcelles non rasées (le bonus s’applique"),
    ("une parcelle non rasée (le bonus s'applique", "une parcelle non rasée (le bonus s’applique"),
    ("S'il atteint ainsi l'emplacement 1 en fin d'Apprentissage", "S’il atteint ainsi l’emplacement 1 en fin d’Apprentissage"),
    ("à l'instant où ce Nid est résolu", "à l’instant où ce Nid est résolu"),
]


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    js_path = root / "data" / "amazonia_data_v5_3.js"
    livret_path = root / "data" / "livret_v5_3.js"
    audit_script = root / "scripts" / "build_v5_3_audit.py"
    backup_dir = root / "data" / ".backups"

    # 1. Restaurer amazonia_data_v5_3.js avant l'injection d'apostrophes droites
    baks = sorted(backup_dir.glob("amazonia_data_v5_3.js.*.bak")) if backup_dir.is_dir() else []
    if baks:
        shutil.copy2(baks[0], js_path)
        print(f"[RESTORE] Restauré depuis la sauvegarde initiale : {baks[0].name}")
    else:
        res = subprocess.run(
            ["git", "show", "HEAD~1:data/amazonia_data_v5_3.js"],
            cwd=root,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        if res.returncode != 0:
            raise RuntimeError("Aucune sauvegarde .bak trouvée et impossible de lire HEAD~1 via git.")
        js_path.write_text(res.stdout, encoding="utf-8", newline="\n")
        print("[RESTORE] Restauré depuis git HEAD~1:data/amazonia_data_v5_3.js")

    # 2. Corriger les apostrophes typographiques dans build_v5_3_audit.py
    src = audit_script.read_text(encoding="utf-8")
    for old, new in REPLACEMENTS_AUDIT_PY:
        src = src.replace(old, new)
    audit_script.write_text(src, encoding="utf-8", newline="\n")
    print("[PATCH]   Apostrophes typographiques (’) appliquées dans scripts/build_v5_3_audit.py")

    # 3. Relancer build_v5_3_audit.py sans écraser la sauvegarde initiale
    run = subprocess.run([sys.executable, str(audit_script), "--no-backup", "--strict"], cwd=root)
    if run.returncode != 0:
        return run.returncode

    # 4. Contrôle syntaxique rapide des apostrophes JS et de livret_v5_3.js
    js_content = js_path.read_text(encoding="utf-8")
    bad_quotes = re.findall(r"[A-Za-zÀ-ÿ]'[A-Za-zÀ-ÿ]", js_content.split("// === BEGIN SPEC_FORMELLE_V5_3")[0])
    if bad_quotes:
        print(f"[ALERTE] Apostrophes droites restantes hors SPEC : {bad_quotes[:5]}")
        return 1

    if livret_path.is_file():
        liv_content = livret_path.read_text(encoding="utf-8")
        decl_count = liv_content.count("const REGLES_COEUR_SYNTHESE")
        if decl_count != 1:
            raise RuntimeError(f"data/livret_v5_3.js contient {decl_count} déclarations de REGLES_COEUR_SYNTHESE (attendu : 1).")
        print("[CHECK]   data/livret_v5_3.js vérifié (1 seule déclaration REGLES_COEUR_SYNTHESE).")

    if shutil.which("node"):
        for target in (js_path, livret_path):
            if target.is_file():
                chk = subprocess.run(["node", "--check", str(target)], capture_output=True, text=True)
                if chk.returncode != 0:
                    print(f"[ERREUR NODE] {target.name} :\n{chk.stderr}")
                    return 1
                print(f"[NODE OK] Syntaxe JavaScript validée par Node : {target.name}")

    print("\n[SUCCÈS] Recharge simplement l'onglet index.html (F5) dans Chrome !")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())