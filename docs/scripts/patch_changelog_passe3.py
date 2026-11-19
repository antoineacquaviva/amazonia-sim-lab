#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Passe 3 : Mise à jour de VERSION_CHANGELOG (v5.3 consolidée) dans data/amazonia_data_v5_3.js."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


V5_3_CHANGELOG_ENTRY = {
    "version": "v5.3",
    "date": "Version consolidée en vigueur (Audit · 25 arbitrages)",
    "titre": "Seuil Imprimé Fixe, Embuscade unique (100 profils), Furtivité à 4 emplacements jumeaux & Zéro Verrouillage",
    "resume": (
        "Alignement intégral Livret Humain / Catalogue (100 profils) / Simulateur / BGA : Seuil Imprimé fixe "
        "(P4_2233 / P5_22233), Furtivité orientée à 4 emplacements jumeaux, gouvernance unitaire par Peuple "
        "d’origine, défausse immédiate des Insectes à la parade (zéro dette et zéro verrouillage des parcelles), "
        "cascades de Gardiens à plat (1→6) et résolution complète machine par machine."
    ),
    "deltas": [
        {
            "domaine": "1. Topologie, Seuil Imprimé & Chaîne des Parades (100 profils)",
            "avant": "v5.2 : Seuil comptant Arbres + Souches ; 2 options de Pièges avec Amortisseur (116 profils D/E).",
            "apres": (
                "v5.3 : P4_2233 [2,2,3,3] (10N Arbres) ou P5_22233 [2,2,2,3,3] (12N Arbres). "
                "Seuil = max(1, Seuil_Imprimé(p) + Offset + Rouges - Bleus + Mod_Tactique + Mod_Tuiles). "
                "Suppression de l’Amortisseur (100 profils). Chaîne stricte à chaque frappe : "
                "1° Jaguar (2 bleus) -> 2° Harpie -> 3° Piège Embuscade (si Défense totale >= 1, locale ou à distance) -> 4° Parade classique."
            ),
        },
        {
            "domaine": "2. Furtivité à 4 emplacements jumeaux, Silence & Gouvernance",
            "avant": "Action bilatérale sur les 2 rives ou mémoire de l’ordre d’arrivée ; décisions collectives sur les tuiles.",
            "apres": (
                "v5.3 : 4 emplacements par case Furtivité (2 jumeaux/rive, max 2 Défenseurs). Entrer sur la case "
                "(toute face) tire l’autre pion sur le jumeau de son bord et oriente l’unique action du binôme ; "
                "retourner de réflexion à définitif se fait strictement sur place. Silence tactique sous paravent fermé ; "
                "chaque Tuile et piste de Migration est gouvernée par son seul Peuple d’origine (Sabotages visibles par H)."
            ),
        },
        {
            "domaine": "3. Combat d’un seul tenant, Zéro Verrouillage, Routes & Contact Nid",
            "avant": "Dette d’Insectes engagés ou verrouillage des parcelles ciblées durant l’Étape 5 ; cibles figées à la révélation.",
            "apres": (
                "v5.3 : Défausse immédiate des Insectes requis à la frappe et zéro verrouillage des parcelles "
                "(seul un Piège déjà déclenché ne paie plus de coût volontaire). Ordre Tactiques 1..6 puis Sièges "
                "(Abatteuse avant Bulldozer sur un même rayon), chaque machine résolue d’un seul tenant depuis sa position réelle. "
                "Routes sautées le long du rayon ; tout mouvement machine entrant sur un Nid le renvoie reconstructible en lisière et défausse les Insectes de la case."
            ),
        },
        {
            "domaine": "4. Dés, Rêves, Nids, Cascades à plat (1→6), Siège & Fin de partie",
            "avant": "Cascades imbriquées, seuil de Réveil recalculé après sacrifice, Siège dépendant de T4.",
            "apres": (
                "v5.3 : Double = Rêve ; hors double, min(D1,D2) sur la machine (annulée si Rêve). Rêve inséré en case 6 "
                "(éjecte la Tactique la plus à droite, glissement partiel). Nid indivisible avant Gardiens ; Migration 0 ou 1 cran "
                "(aller simple vers pistes globales). Cascades à plat de 1 à 6 (marquage immédiat, Faces 2 autonomes). "
                "Siège autonome (0 Apprentissage). Seuil de Réveil fixe vérifié en fin de 5.3 (+ Écho en 6.2) ; raz totale des jetons Apprentissage en 6.2."
            ),
        },
    ],
}


def find_first_object_span(text: str, start_idx: int) -> tuple[int, int]:
    i = text.find("{", start_idx)
    if i == -1:
        raise RuntimeError("Objet initial introuvable dans VERSION_CHANGELOG.")
    depth = 0
    in_quote: str | None = None
    obj_start = i
    while i < len(text):
        ch = text[i]
        if in_quote:
            if ch == "\\":
                i += 2
                continue
            if ch == in_quote:
                in_quote = None
        else:
            if ch in ("'", '"', "`"):
                in_quote = ch
            elif ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return obj_start, i + 1
        i += 1
    raise RuntimeError("Accolade fermante introuvable dans VERSION_CHANGELOG.")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    js_path = root / "data" / "amazonia_data_v5_3.js"
    src = js_path.read_text(encoding="utf-8")

    m = re.search(r"\bconst\s+VERSION_CHANGELOG\s*=\s*\[", src)
    if not m:
        raise RuntimeError("VERSION_CHANGELOG introuvable dans amazonia_data_v5_3.js")

    obj_start, obj_end = find_first_object_span(src, m.end())
    first_block = src[obj_start:obj_end]
    entry_js = json.dumps(V5_3_CHANGELOG_ENTRY, ensure_ascii=False, indent=6)

    if re.search(r"""['"]?version['"]?\s*:\s*['"]v5\.3['"]""", first_block):
        updated = src[:obj_start] + entry_js + src[obj_end:]
        action = "Entrée v5.3 existante remplacée"
    else:
        rest = src[obj_start:].replace("date: 'Version en vigueur'", "date: 'Étape intermédiaire (116 profils)'", 1)
        updated = src[:obj_start] + entry_js + ",\n      " + rest
        action = "Entrée v5.3 insérée en tête devant v5.2"

    js_path.write_text(updated, encoding="utf-8", newline="\n")
    print(f"[WRITE] {action} dans data/amazonia_data_v5_3.js")

    if shutil.which("node"):
        chk = subprocess.run(["node", "--check", str(js_path)], capture_output=True, text=True)
        if chk.returncode != 0:
            raise RuntimeError(f"Erreur syntaxe JS :\n{chk.stderr}")
        print("[NODE OK] Syntaxe JavaScript validée.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())