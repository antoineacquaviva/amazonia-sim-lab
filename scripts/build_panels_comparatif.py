"""Générateur du comparatif éditorial côte à côte des 3 panels candidats v6.3.1.

Lit `contracts/panels/panel_{1,2,3}.json` (déjà validés par `scripts/tiles_v6_3_schema.py`
et `scripts/audit_197.py`) et produit `contracts/panels/COMPARATIF_3_PANELS_V6_3.md`,
organisé lisière par lisière (`X ↔ Y`) pour guider l'arbitrage d'auteur de l'Étape 2b.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_197 import audit_tiles_catalog_197
from scripts.tiles_v6_3_schema import (
    DEFAULT_REFERENTIEL_PICTOGRAMMES,
    PANELS_DIR,
    SLOTS_BY_ID,
)

DEFAULT_OUTPUT_PATH = PANELS_DIR / "COMPARATIF_3_PANELS_V6_3.md"

PEUPLE_NAMES: dict[str, str] = {
    "H": "Humains",
    "E": "Entités Magiques",
    "M": "Mammifères",
    "R": "Reptiles",
    "O": "Oiseaux",
    "I": "Insectes",
}

ICON_LABELS: dict[str, str] = {
    "ICONE_PARADE": "Parade",
    "ICONE_PIEGEAGE": "Piégeage",
    "ICONE_SABOTAGE": "Sabotage",
    "ICONE_REVE": "Rêve",
    "ICONE_INSECTE": "Insecte",
    "ICONE_RESONANCE": "Résonance",
}

ROLE_BADGES: dict[str, str] = {
    "TWIST_2K3": "⚡ Twist 2K3",
    "LOI_PASSIVE": "⚖️ Loi passive",
    "CATALYSEUR_EVEIL": "⭐ Éveil",
    "LEVIER_REVE": "🌙 Levier Rêve",
    "ENRACINEMENT": "🌱 Enracinement",
    "AUTONOMIE_A0": "🔓 A=0",
}

# Groupes éditoriaux des 15 lisières (X ↔ Y) et leurs 2 emplacements orientés (X>Y, Y>X)
BORDER_GROUPS: tuple[tuple[str, tuple[tuple[str, str, str, str], ...]], ...] = (
    (
        "A. Lisières Animal ↔ Animal (3 lisières · 6 Gardiens)",
        (
            ("M", "R", "G1", "G2"),
            ("M", "O", "G3", "G4"),
            ("R", "O", "G5", "G6"),
        ),
    ),
    (
        "B. Lisières Animal ↔ Onirique (6 lisières · 6 Gardiens + 6 Rêves)",
        (
            ("M", "H", "G7", "R3"),
            ("M", "E", "G8", "R7"),
            ("R", "H", "G9", "R4"),
            ("R", "E", "G10", "R8"),
            ("O", "H", "G11", "R5"),
            ("O", "E", "G12", "R9"),
        ),
    ),
    (
        "C. Lisières Animal ↔ Essaim (3 lisières · 3 Gardiens + 3 Nids)",
        (
            ("M", "I", "G13", "M1"),
            ("R", "I", "G14", "M2"),
            ("O", "I", "G15", "M3"),
        ),
    ),
    (
        "D. Triangle Autonome A = 0 `{H, E, I}` (3 lisières · 4 Rêves + 2 Nids)",
        (
            ("H", "E", "R1", "R2"),
            ("H", "I", "R6", "M4"),
            ("E", "I", "R10", "M5"),
        ),
    ),
)


def _esc_cell(text: str) -> str:
    """Échappe une chaîne pour cellule Markdown sans saut de ligne brut."""
    cleaned = " ".join(text.replace("|", "\\|").splitlines()).strip()
    return cleaned or "—"


def _format_roles(tile: Mapping[str, Any]) -> str:
    roles = list(tile.get("roles_portes") or [])
    if not roles:
        return "Brique fluide"
    return " · ".join(ROLE_BADGES.get(str(r), str(r)) for r in roles)


def _format_pics(tile: Mapping[str, Any]) -> str:
    pics = list((tile.get("tuile_plateau") or {}).get("pictogrammes") or [])
    out: list[str] = []
    for p in pics:
        entry = DEFAULT_REFERENTIEL_PICTOGRAMMES.get(str(p))
        sym = entry["symbole"] if entry else ""
        out.append(f"{sym} `{p}`".strip())
    return " · ".join(out) if out else "—"


def _format_icon(tile: Mapping[str, Any]) -> str:
    tp = tile.get("tuile_plateau") or {}
    ic = tp.get("icone_conseillee")
    badge = str(tp.get("fenetre_badge") or "—")
    if ic:
        return f"{badge} / **{ICON_LABELS.get(str(ic), str(ic))}**"
    return badge


def _format_tokens(items: list[Any]) -> str:
    if not items:
        return "—"
    return ", ".join(f"`{x}`" for x in items)


def _format_multiline_quote(text: str) -> list[str]:
    lines: list[str] = []
    for raw in text.strip().splitlines():
        s = raw.strip()
        lines.append(f"  > {s}" if s else "  >")
    return lines


def generate_comparatif_markdown(panels_dir: Path = PANELS_DIR) -> str:
    """Génère le texte Markdown complet du comparatif côte à côte des 3 panels."""
    panel_keys = ("panel_1", "panel_2", "panel_3")
    panel_labels = ("Panel 1", "Panel 2", "Panel 3")
    docs: dict[str, dict[str, Any]] = {}
    reports: dict[str, dict[str, Any]] = {}

    for pkey in panel_keys:
        path = panels_dir / f"{pkey}.json"
        if not path.is_file():
            raise FileNotFoundError(f"Panel introuvable : {path}")
        doc = json.loads(path.read_text(encoding="utf-8"))
        docs[pkey] = doc
        reports[pkey] = audit_tiles_catalog_197(doc, allow_draft=False)

    lines: list[str] = [
        "# Comparatif des 3 Panels Candidats (`v6.3.1`) — Arbitrage d’auteur (Étape 2b)",
        "",
        (
            "*Généré automatiquement depuis `contracts/panels/panel_1.json`, `panel_2.json` et `panel_3.json` "
            "(validés à `0 erreur` par `scripts/tiles_v6_3_schema.py --strict` et `scripts/audit_197.py`).*"
        ),
        "",
        "---",
        "",
        "## 1. Tableau de bord comparatif (`audit_197` · 197 assises · 4 Murs Porteurs `M1..M4`)",
        "",
        "| Critère | Panel 1 | Panel 2 | Panel 3 |",
        "|---|---|---|---|",
    ]

    def _row(label: str, fn: Any) -> str:
        vals = [_esc_cell(str(fn(pkey))) for pkey in panel_keys]
        return f"| **{label}** | {vals[0]} | {vals[1]} | {vals[2]} |"

    lines.extend(
        [
            _row("Source / modèle", lambda k: docs[k]["_meta"].get("source_modele", k)),
            _row("Verdict global (`audit_197`)", lambda k: f"**{reports[k]['verdict_global']}** ({len(reports[k]['errors'])} erreur)"),
            _row("Murs `M1 / M2 / M3 / M4`", lambda k: (
                f"{reports[k]['M1_TEMPS_BATAILLE']['verdict']} / "
                f"{reports[k]['M2_CONSERVATION_THERMIQUE']['verdict']} / "
                f"{reports[k]['M3_INTEGRITE_PLATEAU_ET_ICONES']['verdict']} / "
                f"{reports[k]['M4_AUTONOMIE_PLANCHER_SOLO']['verdict']}"
            )),
            _row("Schéma bi-composant `v6.3.1`", lambda k: f"{reports[k]['V63_schema_et_casting']['verdict']} (0 erreur, `C02` purgé)"),
            _row("Twists `2K3` (`Q02`)", lambda k: f"{reports[k]['Q02_twists_2K3']['nombre']} : {', '.join(reports[k]['Q02_twists_2K3']['twists'])}"),
            _row("Lois passives (`Q01` ≤ 5, max/assise ≤ 2)", lambda k: (
                f"{reports[k]['Q01_lois_passives']['nombre']}/5 (max {reports[k]['Q01_lois_passives']['max_par_assise']}/assise) : "
                f"{', '.join(reports[k]['Q01_lois_passives']['lois'])}"
            )),
            _row("Catalyseurs Éveil (`I04` ≥ 9)", lambda k: f"{reports[k]['I04_couverture_eveil']['nombre']} : {', '.join(reports[k]['I04_couverture_eveil']['catalyseurs'])}"),
            _row("Leviers de Rêve (`I05`)", lambda k: f"{len(reports[k]['I05_couverture_sommeil']['leviers'])} ({', '.join(reports[k]['I05_couverture_sommeil']['leviers'])}) · E couverts : {len(reports[k]['I05_couverture_sommeil']['lisieres_E_couvertes'])}/4"),
            _row("Synergies Enracinement (`I06` 3–5)", lambda k: f"{reports[k]['I06_enracinement']['nombre']} : {', '.join(reports[k]['I06_enracinement']['tuiles'])}"),
            _row("Synergies optionnelles couvertes (`/64`)", lambda k: (
                f"{len(reports[k]['I01_cloture_elargie_197']['couverture_synergies_optionnelles'])} déclarées (100 % sur 64/64 assises)"
            )),
            "",
            (
                "> **Note d’assemblage Étape 2a (4 micro-correctifs Red Team appliqués)** : "
                "(1) filet plancher solo ajouté sur `Panel 2 · R2` (*à défaut, sur une mobile sans Altération de E ou H*) ; "
                "(2) physique `v6.2` exacte des encoches rétablie sur `Panel 3 · G1` (*Rugissement d’Éveil* + repli solo) et `Panel 3 · G5` (*Relais d’Éveil* sans retrait de l’encoche, zéro compteur de Résonance `v6.0`) ; "
                "(3) casting verrouillé `Le Caïman noir` (`fenetre_badge: ACTIVATION`) sur `Panel 3 · G9` et renommage `Le Songe de la Carapace de Limon` sur `Panel 3 · R4` ; "
                "(4) mapping complet vers les 32 codes `PIC_*` officiels, suppression de toute référence brute d’étape (`C01`), et séparation `entrees_plancher` / `entrees_synergie` sur les 90 fiches."
            ),
            "",
            "---",
            "",
            "## 2. Sommaire des 15 lisières (`X ↔ Y`)",
            "",
        ]
    )

    for group_title, borders in BORDER_GROUPS:
        lines.append(f"### {group_title}")
        for p1, p2, s1, s2 in borders:
            anchor = f"lisiere-{p1.lower()}-{p2.lower()}-{s1.lower()}-{s2.lower()}"
            lines.append(
                f"- **Lisière `{p1} ↔ {p2}`** ({PEUPLE_NAMES[p1]} ↔ {PEUPLE_NAMES[p2]}) : "
                f"[`{s1}` (`{p1}>{p2}`) & `{s2}` (`{p2}>{p1}`)](#{anchor})"
            )
        lines.append("")

    lines.extend(["---", ""])

    # Sections détaillées lisière par lisière
    for group_title, borders in BORDER_GROUPS:
        lines.extend([f"## {group_title}", ""])
        for p1, p2, s1, s2 in borders:
            anchor = f"lisiere-{p1.lower()}-{p2.lower()}-{s1.lower()}-{s2.lower()}"
            lines.append(f'<a id="{anchor}"></a>')
            lines.append(
                f"### Lisière `{p1} ↔ {p2}` — {PEUPLE_NAMES[p1]} ↔ {PEUPLE_NAMES[p2]} (`{s1}` & `{s2}`)"
            )
            lines.append("")

            # Tableau de vue d'ensemble du duo sur la lisière
            lines.extend(
                [
                    "| Emplacement | Panel 1 | Panel 2 | Panel 3 |",
                    "|---|---|---|---|",
                ]
            )
            for sid in (s1, s2):
                fam, _orig, _vois, alias = SLOTS_BY_ID[sid]
                cells: list[str] = []
                for pkey in panel_keys:
                    t = docs[pkey]["tuiles_ciblees"][sid]
                    titre = str(t["carte_joueur"]["titre_complet"])
                    res = str(t["tuile_plateau"]["resume_plateau"])
                    roles_s = _format_roles(t)
                    out0 = t["sorties"][0] if t["sorties"] else "—"
                    cells.append(
                        _esc_cell(f"**{titre}** — {res} ({roles_s} · sortie `{out0}`)")
                    )
                lines.append(
                    f"| **`{sid}`** (`{alias}`, {fam}) | {cells[0]} | {cells[1]} | {cells[2]} |"
                )
            lines.append("")

            # Détail complet côte à côte pour chaque des 2 emplacements de la lisière
            for sid in (s1, s2):
                fam, _orig, _vois, alias = SLOTS_BY_ID[sid]
                lines.extend(
                    [
                        f"#### Emplacement `{sid}` (`{alias}` · {fam})",
                        "",
                        "| Attribut | Panel 1 | Panel 2 | Panel 3 |",
                        "|---|---|---|---|",
                    ]
                )
                tiles_3 = [docs[pk]["tuiles_ciblees"][sid] for pk in panel_keys]
                lines.append(
                    "| **Titre complet** | "
                    + " | ".join(_esc_cell(f"**{t['carte_joueur']['titre_complet']}**") for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Rôles & Nature** | "
                    + " | ".join(_esc_cell(f"{_format_roles(t)} (`{t['nature']}`)") for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Fenêtre / Icône** | "
                    + " | ".join(_esc_cell(_format_icon(t)) for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Pictogrammes** | "
                    + " | ".join(_esc_cell(_format_pics(t)) for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Résumé Mini-Tuile** | "
                    + " | ".join(_esc_cell(str(t["tuile_plateau"]["resume_plateau"])) for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Mots-clés Face 1** | "
                    + " | ".join(_esc_cell(str(t["tuile_plateau"]["mots_cles_plateau"]["face_1"])) for t in tiles_3)
                    + " |"
                )
                if fam == "GARDIEN":
                    lines.append(
                        "| **Mots-clés Face 2** | "
                        + " | ".join(
                            _esc_cell(str(t["tuile_plateau"]["mots_cles_plateau"]["face_2"] or "—"))
                            for t in tiles_3
                        )
                        + " |"
                    )
                if any(t["tuile_plateau"]["mots_cles_plateau"].get("enracine") for t in tiles_3):
                    lines.append(
                        "| **Mots-clés Enraciné** | "
                        + " | ".join(
                            _esc_cell(str(t["tuile_plateau"]["mots_cles_plateau"].get("enracine") or "—"))
                            for t in tiles_3
                        )
                        + " |"
                    )
                lines.append(
                    "| **Plancher (`M4`)** | "
                    + " | ".join(_esc_cell(_format_tokens(list(t.get("entrees_plancher") or []))) for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Synergies (`I01`)** | "
                    + " | ".join(_esc_cell(_format_tokens(list(t.get("entrees_synergie") or []))) for t in tiles_3)
                    + " |"
                )
                lines.append(
                    "| **Sorties (`I03`)** | "
                    + " | ".join(_esc_cell(_format_tokens(list(t.get("sorties") or []))) for t in tiles_3)
                    + " |"
                )
                lines.append("")

                # Textes de règles complets + dilemmes + témoins (par panel)
                for lbl, t in zip(panel_labels, tiles_3, strict=True):
                    cj = t["carte_joueur"]
                    tr = cj["texte_regle"]
                    dr = cj["decision_et_renoncement"]
                    lines.append(
                        f"- **{lbl} — {cj['titre_complet']}** *({_format_roles(t)} · {_format_icon(t)})*"
                    )
                    lines.append(f"  - *Ambiance* : {cj['pitch_ambiance']}")
                    lines.append("  - **Face 1** :")
                    lines.extend(_format_multiline_quote(str(tr["face_1"])))
                    if tr.get("face_2"):
                        lines.append("  - **Face 2** :")
                        lines.extend(_format_multiline_quote(str(tr["face_2"])))
                    if tr.get("enracine"):
                        lines.append("  - **Enraciné** :")
                        lines.extend(_format_multiline_quote(str(tr["enracine"])))
                    lines.append(
                        f"  - **Dilemme** — *Choix* : {dr['choix']} · *Renoncement* : {dr['renoncement']}"
                    )
                    if t.get("double_ouverture"):
                        lines.append(f"  - **Double activation** : {t['double_ouverture']}")
                    temoins = list(t.get("temoins") or [])
                    if temoins:
                        tm0 = temoins[0]
                        lines.append(f"  - **Témoin `{tm0['id']}`** : {tm0['resume']}")
                    lines.append("")

            lines.extend(["---", ""])

    # Grille finale d'arbitrage Étape 2b
    lines.extend(
        [
            "## 3. Grille d’arbitrage Étape 2b (30 emplacements)",
            "",
            "| Emplacement | Lisière | Panel 1 | Panel 2 | Panel 3 | Arbitrage retenu |",
            "|---|---|---|---|---|---|",
        ]
    )
    for _, borders in BORDER_GROUPS:
        for p1, p2, s1, s2 in borders:
            for sid in (s1, s2):
                _, _orig, _vois, alias = SLOTS_BY_ID[sid]
                t1 = docs["panel_1"]["tuiles_ciblees"][sid]["carte_joueur"]["titre_complet"]
                t2 = docs["panel_2"]["tuiles_ciblees"][sid]["carte_joueur"]["titre_complet"]
                t3 = docs["panel_3"]["tuiles_ciblees"][sid]["carte_joueur"]["titre_complet"]
                lines.append(
                    f"| **`{sid}`** (`{alias}`) | `{p1} ↔ {p2}` | {_esc_cell(t1)} | "
                    f"{_esc_cell(t2)} | {_esc_cell(t3)} | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |"
                )
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Génère contracts/panels/COMPARATIF_3_PANELS_V6_3.md depuis panel_{1,2,3}.json."
    )
    parser.add_argument(
        "--panels-dir",
        type=Path,
        default=PANELS_DIR,
        help="Répertoire contenant panel_1.json, panel_2.json et panel_3.json.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Chemin du fichier Markdown comparatif à écrire.",
    )
    args = parser.parse_args()
    md = generate_comparatif_markdown(args.panels_dir)
    args.output.write_text(md, encoding="utf-8", newline="\n")
    print(
        f"build_panels_comparatif.py : OK -> {args.output.as_posix()} "
        f"({len(md.splitlines())} lignes, {len(md.encode('utf-8'))} octets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
