"""Assemblage officiel du Panel Canonique v6.3.1 (`contracts/tiles_canon_v6_3.json`) et export Passe 1.

Extrait chacun des 30 emplacements depuis sa source arbitrée par l'auteur
(`contracts/panels/panel_{1,2,3}.json`, conservés intacts en archive comparative),
applique l'ajustement explicite sur `G3` (`L’Atèle` reclassé hors-twist),
recalcule proprement `carte_des_roles` et `rapport_audit_197`, valide à 100 %
(`0` erreur) contre `scripts/tiles_v6_3_schema.py` (`strict=True`) et
`scripts/audit_197.py` (`allow_draft=False`), et génère le support lisible
`docs/panel_canon_v6_3_passe1.md` pour l'Étape 3 (Passe 2).
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_197 import audit_tiles_catalog_197
from scripts.build_panels_comparatif import (
    BORDER_GROUPS,
    ICON_LABELS,
    PEUPLE_NAMES,
    ROLE_BADGES,
)
from scripts.tiles_v6_3_schema import (
    DEFAULT_REFERENTIEL_PICTOGRAMMES,
    LOCKED_GARDIEN_CASTING_V6_3,
    MURS_PORTEURS_V6_3,
    PANELS_DIR,
    SLOTS_BY_ID,
    SLOTS_SPEC_30,
    V6_3_CONTRACT_PATH,
    validate_tiles_canon_v6_3,
)

DEFAULT_MARKDOWN_OUTPUT = ROOT / "docs" / "panel_canon_v6_3_passe1.md"

PANEL_1_SLOTS: tuple[str, ...] = (
    "G1",
    "G2",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G12",
    "G13",
    "G14",
    "G15",
    "R1",
    "R3",
    "R4",
    "R6",
    "R7",
    "R9",
    "M1",
    "M2",
    "M3",
    "M4",
)
PANEL_2_SLOTS: tuple[str, ...] = ("G3", "G11", "R2", "R5")
PANEL_3_SLOTS: tuple[str, ...] = ("G10", "R8", "R10", "M5")

SELECTION_BY_PANEL: dict[str, tuple[str, ...]] = {
    "panel_1": PANEL_1_SLOTS,
    "panel_2": PANEL_2_SLOTS,
    "panel_3": PANEL_3_SLOTS,
}

PROVENANCE_BY_SLOT: dict[str, str] = {
    sid: panel_id for panel_id, slots in SELECTION_BY_PANEL.items() for sid in slots
}

EXPECTED_TWISTS_2K3: frozenset[str] = frozenset({"G2", "G7", "R4", "G12", "R10", "M3"})


def _build_casting_verrouille() -> dict[str, dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for sid, fam, orig, vois, alias in SLOTS_SPEC_30:
        if fam == "GARDIEN":
            out[sid] = {
                "alias_oriente": alias,
                "nom_animal": LOCKED_GARDIEN_CASTING_V6_3[sid],
                "origine": orig,
                "voisin": vois,
            }
    return out


def _reclassify_g3_non_twist(tile: dict[str, Any]) -> None:
    """Reclasse `G3` (`L’Atèle`, issu de `panel_2`) en brique classique hors-twist."""
    tile["est_twist"] = False
    tile["roles_portes"] = [r for r in tile.get("roles_portes", []) if r != "TWIST_2K3"]
    if "CATALYSEUR_EVEIL" not in tile["roles_portes"]:
        tile["roles_portes"].insert(0, "CATALYSEUR_EVEIL")
    tile["tags"] = [
        t for t in tile.get("tags", []) if t not in ("PIC_TWIST", "TWIST_2K3", "TWIST")
    ]
    tp = tile["tuile_plateau"]
    tp["pictogrammes"] = [p for p in tp.get("pictogrammes", []) if p != "PIC_TWIST"]


def _compute_carte_des_roles(
    tuiles: Mapping[str, Mapping[str, Any]],
    lois_dist: Mapping[str, int],
) -> dict[str, Any]:
    catalyseurs: list[str] = []
    leviers_reve: list[str] = []
    enracinements: list[str] = []
    lois_passives: list[str] = []
    autonomie_a0: list[str] = []
    twists_2k3: list[str] = []

    for sid, _fam, _orig, _vois, alias in SLOTS_SPEC_30:
        t = tuiles[sid]
        tag = f"{sid}={alias}"
        roles = set(t.get("roles_portes") or [])
        if "CATALYSEUR_EVEIL" in roles:
            catalyseurs.append(tag)
        if "LEVIER_REVE" in roles:
            leviers_reve.append(tag)
        if "ENRACINEMENT" in roles:
            enracinements.append(tag)
        if str(t.get("nature", "")).upper() == "LOI_PASSIVE":
            lois_passives.append(tag)
        if "AUTONOMIE_A0" in roles:
            autonomie_a0.append(tag)
        if bool(t.get("est_twist", False)):
            twists_2k3.append(tag)

    dist_txt = ", ".join(f"{k} sur {v}" for k, v in sorted(lois_dist.items(), key=lambda kv: int(kv[0])))
    lois_list_txt = ", ".join(lois_passives)
    return {
        "statut": "CANON_PASSE_1_ASSEMBLE_V6_3_1",
        "provenance_assemblage": {
            "panel_1": list(PANEL_1_SLOTS),
            "panel_2": list(PANEL_2_SLOTS),
            "panel_3": list(PANEL_3_SLOTS),
            "ajustements": [
                (
                    "G3 (L’Atèle, issu de panel_2) reclassé en brique classique hors-twist "
                    "(est_twist=false, TWIST_2K3 retiré de roles_portes, CATALYSEUR_EVEIL conservé) ; "
                    "les 6 Twists 2K3 du canon sont exactement {G2, G7, R4} + {G12, R10, M3}."
                )
            ],
        },
        "partition_2K3": {
            "triangle_1": "R>M (G2) → M>H (G7) → H>R (R4)",
            "triangle_2": "O>E (G12) → E>I (R10) → I>O (M3)",
        },
        "etoile_lois_passives": (
            f"Les {len(lois_passives)} lois passives ({lois_list_txt}) forment une étoile centrée sur E "
            f"(Entités) : au plus 2 lois sur chacune des 197 assises ({dist_txt})."
        ),
        "roles": {
            "catalyseurs_eveil": catalyseurs,
            "leviers_reve": leviers_reve,
            "synergies_enracinement": enracinements,
            "lois_passives": lois_passives,
            "autonomie_A0": autonomie_a0,
            "twists_2K3": twists_2k3,
        },
    }


def _summarize_audit_report(report: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "verdict_global": report["verdict_global"],
        "c02_word_count_purged": True,
        "assises_verifiees": report["assises"]["total"],
        "compositions_verifiees": report["assises"]["compositions"],
        "M1_TEMPS_BATAILLE": report["M1_TEMPS_BATAILLE"]["verdict"],
        "M2_CONSERVATION_THERMIQUE": report["M2_CONSERVATION_THERMIQUE"]["verdict"],
        "M3_INTEGRITE_PLATEAU_ET_ICONES": report["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"],
        "M4_AUTONOMIE_PLANCHER_SOLO": report["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"],
        "C01_mem_debt": report["C01_mem_debt"]["verdict"],
        "I01_cloture_elargie_197": report["I01_cloture_elargie_197"]["verdict"],
        "I02_autonomie_A0": report["I02_autonomie_A0"]["verdict"],
        "I03_divergence_lisiere": report["I03_divergence_lisiere"]["verdict"],
        "I04_couverture_eveil": {
            "verdict": report["I04_couverture_eveil"]["verdict"],
            "nombre": report["I04_couverture_eveil"]["nombre"],
        },
        "I05_couverture_sommeil": {
            "verdict": report["I05_couverture_sommeil"]["verdict"],
            "nombre_leviers": len(report["I05_couverture_sommeil"]["leviers"]),
            "lisieres_E_couvertes": list(report["I05_couverture_sommeil"]["lisieres_E_couvertes"]),
        },
        "I06_enracinement": {
            "verdict": report["I06_enracinement"]["verdict"],
            "nombre": report["I06_enracinement"]["nombre"],
        },
        "Q01_lois_passives": {
            "verdict": report["Q01_lois_passives"]["verdict"],
            "nombre": report["Q01_lois_passives"]["nombre"],
            "max_par_assise": report["Q01_lois_passives"]["max_par_assise"],
        },
        "Q02_twists_2K3": {
            "verdict": report["Q02_twists_2K3"]["verdict"],
            "nombre": report["Q02_twists_2K3"]["nombre"],
        },
        "V63_schema_et_casting": report["V63_schema_et_casting"]["verdict"],
        "synergies_optionnelles_couvertes": len(
            report["I01_cloture_elargie_197"]["couverture_synergies_optionnelles"]
        ),
    }


def assemble_canon_v6_3(
    panels_dir: Path = PANELS_DIR,
    *,
    genere_le: str = "2026-11-26",
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Assemble et valide en strict le contrat `contracts/tiles_canon_v6_3.json`."""
    expected_ids = set(SLOTS_BY_ID.keys())
    selected_ids = set(PROVENANCE_BY_SLOT.keys())
    if selected_ids != expected_ids or len(PROVENANCE_BY_SLOT) != 30:
        raise ValueError(
            f"Table d'assemblage invalide (manquants={sorted(expected_ids - selected_ids)}, "
            f"en trop={sorted(selected_ids - expected_ids)})"
        )

    panels: dict[str, dict[str, Any]] = {}
    for panel_id in SELECTION_BY_PANEL:
        pfile = panels_dir / f"{panel_id}.json"
        if not pfile.is_file():
            raise FileNotFoundError(f"Panel source introuvable : {pfile}")
        panels[panel_id] = json.loads(pfile.read_text(encoding="utf-8"))

    tuiles_out: dict[str, dict[str, Any]] = {}
    for sid, *_ in SLOTS_SPEC_30:
        src_panel_id = PROVENANCE_BY_SLOT[sid]
        tile = copy.deepcopy(panels[src_panel_id]["tuiles_ciblees"][sid])
        if sid == "G3":
            _reclassify_g3_non_twist(tile)
        tuiles_out[sid] = tile

    actual_twists = {sid for sid, t in tuiles_out.items() if t.get("est_twist")}
    if actual_twists != EXPECTED_TWISTS_2K3:
        raise RuntimeError(
            f"Ensemble des Twists 2K3 inattendu : attendu {sorted(EXPECTED_TWISTS_2K3)}, "
            f"obtenu {sorted(actual_twists)}"
        )

    doc: dict[str, Any] = {
        "_meta": {
            "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
            "schema_version": "6.3.1",
            "socle_verrouille": "6.2.0",
            "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
            "etape_active": "ETAPE_3_AFFINAGE_EDITORIAL",
            "statut_global": "CONCEPTION_EN_COURS",
            "genere_le": genere_le,
            "slots_count": 30,
            "c02_supprime": True,
            "panel_id": "canon_v6_3",
            "source_modele": (
                "Assemblage officiel Étape 2b : 22 tuiles panel_1 + "
                "4 tuiles panel_2 (G3 reclassé hors-twist, G11, R2, R5) + "
                "4 tuiles panel_3 (G10, R8, R10, M5)"
            ),
            "murs_porteurs_verrouilles": list(MURS_PORTEURS_V6_3),
            "note_retrocompatibilite": (
                "Panel canonique v6.3.1 Passe 1 assemblé (30 tuiles rédigées, 0 erreur sur M1..M4 + "
                "I01..I07 + Q01..Q02, prêt pour l'affinage éditorial Étape 3) : le build Doc Studio "
                "actif reste transitoirement sur contracts/tiles_canon_v6_2.json (archive sanctuarisée) "
                "jusqu'aux Étapes 3–4."
            ),
        },
        "referentiel_pictogrammes": copy.deepcopy(DEFAULT_REFERENTIEL_PICTOGRAMMES),
        "casting_gardiens_verrouille": _build_casting_verrouille(),
        "carte_des_roles": {
            "statut": "EN_CALCUL",
            "roles": {
                "catalyseurs_eveil": [],
                "leviers_reve": [],
                "synergies_enracinement": [],
                "lois_passives": [],
                "autonomie_A0": [],
                "twists_2K3": [],
            },
        },
        "rapport_audit_197": {
            "verdict_global": "EN_CALCUL",
            "c02_word_count_purged": True,
        },
        "tuiles_ciblees": tuiles_out,
    }

    # 1er passage d'audit pour calculer carte_des_roles et rapport_audit_197
    first_report = audit_tiles_catalog_197(doc, allow_draft=False)
    doc["carte_des_roles"] = _compute_carte_des_roles(
        tuiles_out, first_report["Q01_lois_passives"]["distribution_par_assise"]
    )
    doc["rapport_audit_197"] = _summarize_audit_report(first_report)

    # Validation finale stricte sur le document complet
    schema_errors = validate_tiles_canon_v6_3(doc, strict=True)
    if schema_errors:
        raise RuntimeError(
            "Échec validation schéma strict v6.3.1 :\n" + "\n".join(f"  - {e}" for e in schema_errors)
        )
    final_report = audit_tiles_catalog_197(doc, allow_draft=False)
    if final_report["verdict_global"] != "OK":
        raise RuntimeError(
            "Échec audit_197 strict :\n" + "\n".join(f"  - {e}" for e in final_report["errors"])
        )

    return doc, final_report


def _esc_cell(text: str) -> str:
    return " ".join(text.replace("|", "\\|").splitlines()).strip() or "—"


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
        if entry:
            out.append(f"{entry['symbole']} {entry['libelle']} (`{p}`)")
        else:
            out.append(f"`{p}`")
    return " · ".join(out) if out else "—"


def _format_icon(tile: Mapping[str, Any]) -> str:
    tp = tile.get("tuile_plateau") or {}
    ic = tp.get("icone_conseillee")
    badge = str(tp.get("fenetre_badge") or "—")
    if ic:
        return f"`{badge}` · Icône conseillée : **{ICON_LABELS.get(str(ic), str(ic))}**"
    return f"`{badge}`"


def _format_tokens(items: list[Any]) -> str:
    if not items:
        return "—"
    return ", ".join(f"`{x}`" for x in items)


def _format_quote(text: str) -> list[str]:
    out: list[str] = []
    for raw in text.strip().splitlines():
        s = raw.strip()
        out.append(f"> {s}" if s else ">")
    return out


def render_canon_passe1_markdown(
    doc: Mapping[str, Any],
    report: Mapping[str, Any],
) -> str:
    """Génère le document Markdown lisible `docs/panel_canon_v6_3_passe1.md` pour l'Étape 3."""
    tuiles: Mapping[str, Mapping[str, Any]] = doc["tuiles_ciblees"]
    meta: Mapping[str, Any] = doc["_meta"]
    carte_roles: Mapping[str, Any] = doc["carte_des_roles"]
    roles_map: Mapping[str, list[str]] = carte_roles["roles"]

    div_by_pair: dict[tuple[str, str], Mapping[str, Any]] = {}
    for entry in report["I03_divergence_lisiere"]["lisieres"]:
        t1, t2 = entry["tuiles"]
        div_by_pair[(t1, t2)] = entry
        div_by_pair[(t2, t1)] = entry

    lines: list[str] = [
        "# Panel Canonique `v6.3.1` — Passe 1 Assemblée (Support de travail Étape 3)",
        "",
        (
            f"*Source contractuelle : `contracts/tiles_canon_v6_3.json` (`schema_version = {meta['schema_version']}`, "
            f"`etape_active = {meta['etape_active']}`, généré le `{meta['genere_le']}`). "
            "Validé à **100 % (`0 erreur`)** par `scripts/tiles_v6_3_schema.py` et "
            "`scripts/audit_197.py` sans `--allow-draft`.*"
        ),
        "",
        "---",
        "",
        "## 1. Synthèse de l’assemblage & Santé sur les `197` assises",
        "",
        "### 1.1 Provenance des 30 emplacements retenus",
        "",
        "| Source archivée (`contracts/panels/`) | Effectif | Emplacements extraits | Ajustement appliqué |",
        "|---|---:|---|---|",
        f"| `panel_1.json` | **{len(PANEL_1_SLOTS)}** | {', '.join(f'`{s}`' for s in PANEL_1_SLOTS)} | Extraction verbatim |",
        f"| `panel_2.json` | **{len(PANEL_2_SLOTS)}** | {', '.join(f'`{s}`' for s in PANEL_2_SLOTS)} | `G3` (*L’Atèle*) reclassé hors-twist (`est_twist=false`, `TWIST_2K3` retiré, `CATALYSEUR_EVEIL` conservé) |",
        f"| `panel_3.json` | **{len(PANEL_3_SLOTS)}** | {', '.join(f'`{s}`' for s in PANEL_3_SLOTS)} | Extraction verbatim |",
        "",
        "### 1.2 Tableau de bord `audit_197` (`197` assises · `42` compositions · `64` assises/tuile)",
        "",
        "| Contrôle | Verdict | Détail mesuré |",
        "|---|---|---|",
        f"| **Murs Porteurs `M1..M4`** | **OK** | `M1`={report['M1_TEMPS_BATAILLE']['verdict']} · `M2`={report['M2_CONSERVATION_THERMIQUE']['verdict']} · `M3`={report['M3_INTEGRITE_PLATEAU_ET_ICONES']['verdict']} · `M4`={report['M4_AUTONOMIE_PLANCHER_SOLO']['verdict']} |",
        "| **Dette mémorielle (`C01`) & Zéro `C02` (`I07`)** | **OK** | `0` modificateur flottant, `0` code d’étape, `0` terme obsolète, `c02_word_count_purged=true` |",
        f"| **Clôture `I01` & Synergies optionnelles** | **OK** | `0` violation Insectes / plancher ; **{len(report['I01_cloture_elargie_197']['couverture_synergies_optionnelles'])}** synergies optionnelles couvertes à `64/64` assises |",
        f"| **Autonomie `A=0` (`I02`)** | **OK** | `6/6` tuiles `{', '.join(report['I02_autonomie_A0']['tuiles'])}` sans dépendance Gardien |",
        "| **Divergence des 15 lisières (`I03`)** | **OK** | `15/15` lisières divergentes en sortie principale, `0` boucle fermée à 2 états |",
        f"| **Couverture Éveil (`I04`)** | **OK** | **{report['I04_couverture_eveil']['nombre']}** catalyseurs (`M`: {report['I04_couverture_eveil']['regle_i_par_animal']['M']}, `R`: {report['I04_couverture_eveil']['regle_i_par_animal']['R']}, `O`: {report['I04_couverture_eveil']['regle_i_par_animal']['O']} vers `{{H,E,I}}` ; `3/3` lisières Animal–Animal ; `0` assise `A≥1` découverte) |",
        f"| **Couverture Sommeil (`I05`)** | **OK** | **{len(report['I05_couverture_sommeil']['leviers'])}** leviers (`{', '.join(report['I05_couverture_sommeil']['leviers'])}`) · `4/4` lisières de `E` couvertes (`{', '.join(report['I05_couverture_sommeil']['lisieres_E_couvertes'])}`) · `0/30` assise `(E sans H)` découverte |",
        f"| **Enracinements (`I06`)** | **OK** | **{report['I06_enracinement']['nombre']}** synergies (`{', '.join(report['I06_enracinement']['tuiles'])}`, cible `3–5`) |",
        f"| **Lois passives (`Q01`)** | **OK** | **{report['Q01_lois_passives']['nombre']}/5** (`{', '.join(report['Q01_lois_passives']['lois'])}`) — étoile centrée sur `E`, max **{report['Q01_lois_passives']['max_par_assise']}**/assise (`0` sur {report['Q01_lois_passives']['distribution_par_assise'].get('0', 0)}, `1` sur {report['Q01_lois_passives']['distribution_par_assise'].get('1', 0)}, `2` sur {report['Q01_lois_passives']['distribution_par_assise'].get('2', 0)}) |",
        f"| **Twists `2K3` (`Q02`)** | **OK** | **6** twists exacts : Triangle 1 `{carte_roles['partition_2K3']['triangle_1']}` + Triangle 2 `{carte_roles['partition_2K3']['triangle_2']}` |",
        "| **Schéma bi-composant & Casting (`V63`)** | **OK** | `30/30` emplacements stricts, `15/15` Gardiens verrouillés, `0` phrase sur Mini-Tuile |",
        "",
        "### 1.3 Carte des rôles consolidée",
        "",
        f"- **⚡ Twists `2K3` (6)** : {', '.join(f'`{x}`' for x in roles_map['twists_2K3'])}",
        f"- **⚖️ Lois passives (3)** : {', '.join(f'`{x}`' for x in roles_map['lois_passives'])}",
        f"- **⭐ Catalyseurs d’Éveil (12)** : {', '.join(f'`{x}`' for x in roles_map['catalyseurs_eveil'])}",
        f"- **🌙 Leviers de Rêve (6)** : {', '.join(f'`{x}`' for x in roles_map['leviers_reve'])}",
        f"- **🌱 Synergies d’Enracinement (4)** : {', '.join(f'`{x}`' for x in roles_map['synergies_enracinement'])}",
        f"- **🔓 Autonomie `A=0` (6)** : {', '.join(f'`{x}`' for x in roles_map['autonomie_A0'])}",
        "",
        "### 1.4 Vue synoptique des 15 frontières (`X ↔ Y`) et divergence `I03`",
        "",
        "| Frontière | `X>Y` (Source) | Sortie principale `X>Y` | `Y>X` (Source) | Sortie principale `Y>X` | Divergence `I03` |",
        "|---|---|---|---|---|---|",
    ]

    for _group_title, borders in BORDER_GROUPS:
        for p1, p2, s1, s2 in borders:
            anchor = f"frontiere-{p1.lower()}-{p2.lower()}-{s1.lower()}-{s2.lower()}"
            t1, t2 = tuiles[s1], tuiles[s2]
            src1, src2 = PROVENANCE_BY_SLOT[s1], PROVENANCE_BY_SLOT[s2]
            out1 = t1["sorties"][0] if t1.get("sorties") else "—"
            out2 = t2["sorties"][0] if t2.get("sorties") else "—"
            hybrid_mark = " *(hybride)*" if src1 != src2 else ""
            lines.append(
                f"| [`{p1} ↔ {p2}`](#{anchor}){hybrid_mark} | "
                f"**`{s1}`** {_esc_cell(t1['carte_joueur']['titre_complet'])} (`{src1}`) | `{out1}` | "
                f"**`{s2}`** {_esc_cell(t2['carte_joueur']['titre_complet'])} (`{src2}`) | `{out2}` | "
                "✅ Divergent · 0 boucle |"
            )

    lines.extend(["", "---", "", "## 2. Fiches complètes par frontière (`X ↔ Y`)", ""])

    for group_title, borders in BORDER_GROUPS:
        lines.extend([f"### {group_title}", ""])
        for p1, p2, s1, s2 in borders:
            anchor = f"frontiere-{p1.lower()}-{p2.lower()}-{s1.lower()}-{s2.lower()}"
            src1, src2 = PROVENANCE_BY_SLOT[s1], PROVENANCE_BY_SLOT[s2]
            div_info = div_by_pair.get((s1, s2), {})
            out1 = tuiles[s1]["sorties"][0] if tuiles[s1].get("sorties") else "—"
            out2 = tuiles[s2]["sorties"][0] if tuiles[s2].get("sorties") else "—"
            border_tag = (
                f"Frontière hybride `{src1}` × `{src2}`"
                if src1 != src2
                else f"Paire `{src1}`"
            )
            lines.append(f'<a id="{anchor}"></a>')
            lines.append(
                f"#### Frontière `{p1} ↔ {p2}` — {PEUPLE_NAMES[p1]} ↔ {PEUPLE_NAMES[p2]} "
                f"(`{s1}` & `{s2}`)"
            )
            lines.append("")
            lines.append(
                f"> **{border_tag}** · Divergence `I03` : `{s1}` → **`{out1}`** vs `{s2}` → **`{out2}`** "
                f"({'✅ divergent, 0 boucle' if div_info.get('divergent') and not div_info.get('boucle_a_deux_etats') else '⚠️ à vérifier'})."
            )
            lines.append("")

            for sid in (s1, s2):
                t = tuiles[sid]
                fam, _orig, _vois, alias = SLOTS_BY_ID[sid]
                src_p = PROVENANCE_BY_SLOT[sid]
                tp = t["tuile_plateau"]
                cj = t["carte_joueur"]
                tr = cj["texte_regle"]
                dr = cj["decision_et_renoncement"]
                mcp = tp["mots_cles_plateau"]
                g3_note = " *(reclassé hors-twist depuis `panel_2`)*" if sid == "G3" else ""

                lines.append(
                    f"##### `{sid}` (`{alias}` · {fam}) — {cj['titre_complet']}"
                )
                lines.append("")
                lines.append(
                    f"- **Provenance** : `{src_p}.json`{g3_note} · **Nature** : `{t['nature']}` · "
                    f"**Rôles** : {_format_roles(t)}"
                )
                lines.append("")

                # 1. Mini-Tuile Plateau
                lines.append("**Mini-Tuile Plateau (`tuile_plateau`)**")
                lines.append("")
                lines.append("| Champ | Contenu |")
                lines.append("|---|---|")
                lines.append(f"| **Nom court** | **{_esc_cell(str(tp['nom_court']))}** |")
                lines.append(f"| **Fenêtre / Icône** | {_format_icon(t)} |")
                lines.append(f"| **Pictogrammes** | {_format_pics(t)} |")
                lines.append(f"| **Résumé plateau** | {_esc_cell(str(tp['resume_plateau']))} |")
                lines.append(f"| **Mots-clés Face 1** | {_esc_cell(str(mcp['face_1']))} |")
                if fam == "GARDIEN":
                    lines.append(
                        f"| **Mots-clés Face 2** | {_esc_cell(str(mcp.get('face_2') or '—'))} |"
                    )
                if mcp.get("enracine"):
                    lines.append(
                        f"| **Mots-clés Enraciné** | {_esc_cell(str(mcp['enracine']))} |"
                    )
                lines.append("")

                # 2. Grande Carte Joueur
                lines.append("**Grande Carte Joueur (`carte_joueur`)**")
                lines.append("")
                lines.append(f"- **Entité illustrée** : {cj['entite_illustree']}")
                lines.append(f"- **Pitch d’ambiance** : *{cj['pitch_ambiance']}*")
                lines.append(f"- **Brief illustration** : {cj['brief_illustration']}")
                lines.append("- **Règle — Face 1** :")
                lines.extend(_format_quote(str(tr["face_1"])))
                if tr.get("face_2"):
                    lines.append("- **Règle — Face 2** :")
                    lines.extend(_format_quote(str(tr["face_2"])))
                if tr.get("enracine"):
                    lines.append("- **Règle — Enraciné** :")
                    lines.extend(_format_quote(str(tr["enracine"])))
                lines.append(f"- **Décision (Choix)** : {dr['choix']}")
                lines.append(f"- **Renoncement** : {dr['renoncement']}")
                if t.get("double_ouverture"):
                    lines.append(f"- **Double activation (Gardien)** : {t['double_ouverture']}")
                lines.append("")

                # 3. Flux & Heuristique
                lines.append("**Flux mécaniques & Bot**")
                lines.append("")
                lines.append(
                    f"- **Entrées plancher (`M4`)** : {_format_tokens(list(t.get('entrees_plancher') or []))} · "
                    f"**Entrées synergie (`I01`)** : {_format_tokens(list(t.get('entrees_synergie') or []))}"
                )
                lines.append(
                    f"- **Sorties (`I03`)** : {_format_tokens(list(t.get('sorties') or []))} · "
                    f"**Déclencheurs amorcés** : {_format_tokens(list(t.get('declencheurs_amorces') or []))} · "
                    f"**Paiement** : {_format_tokens(list(t.get('paiement') or []))}"
                )
                lines.append(f"- **Heuristique bot** : {t['heuristique_bot']}")
                lines.append("")

                # 4. Témoins
                temoins = list(t.get("temoins") or [])
                lines.append(f"**Témoins ({len(temoins)})**")
                lines.append("")
                for tm in temoins:
                    lines.append(f"- **`{tm['id']}`** (`{tm['statut']}`) : {tm['resume']}")
                lines.append("")

            lines.extend(["---", ""])

    # Section 3 : Points d'attention repérés pour l'Étape 3 (Passe 2)
    lines.extend(
        [
            "## 3. Points d’harmonisation éditoriale & ergonomique repérés pour l’Étape 3 (Passe 2)",
            "",
            (
                "Les 30 fiches ci-dessus sont extraites fidèlement de leur panel d’origine "
                "(seul `G3` a été reclassé hors-twist). Pour la Passe 2 (harmonisation de voix et "
                "ergonomie finale avant encodage PyPy en Étape 4), les écarts de style inter-panels "
                "suivants mériteront un lissage homogène :"
            ),
            "",
            "1. **Titres complets des Gardiens (`carte_joueur.titre_complet`)** : les 12 Gardiens issus de `panel_1` et `G10` (`panel_3`) portent un épithète évocateur (*« Le Jaguar, seigneur des berges »*, *« La Matamata, Guetteuse des Feuilles Mortes »*), tandis que `G3` (*L’Atèle*) et `G11` (*La Harpie féroce*, issus de `panel_2`) portent uniquement le nom de l’animal ; harmoniser le style des épithètes et la casse (`panel_3` utilise des majuscules de titre).",
            "2. **Zéro code interne dans le texte joueur** : `G11` (`Face 2`, issu de `panel_2`) mentionne explicitement le code interne `« R5 »` (*« après tout échange de R5 »*) ; remplacer en Passe 2 par une formulation joueur (*« après tout échange du Ciel à deux eaux »* ou formulation générique de chronologie d’ouverture).",
            "3. **Homogénéité du champ `mots_cles_plateau.enracine`** : les 22 fiches `panel_1` sans rôle `ENRACINEMENT` laissent ce champ à `null`, alors que `G11` (`panel_2` : `\"Ordinaire\"`) et `G10`, `R8`, `R10`, `M5` (`panel_3` : `\"Standard (...)\"`) y inscrivent une mention standard ; unifier sur `null` hors des 4 synergies d’Enracinement (`G7`, `G15`, `R1`, `R2`).",
            "4. **Homogénéité typographique & structurelle des textes** : unifier les apostrophes typographiques (`’` vs `'` dans `panel_3`), la mise en forme des choix/puces (`panel_1` narratif en paragraphes nommés vs `panel_2` compact vs `panel_3` numéroté `1. / 2. / •`), et la voix des encadrés *Décision / Renoncement*.",
            "5. **Format des champs `vecteurs` et statut des `temoins`** : uniformiser le style de `vecteurs` (phrase fléchée `panel_1` vs formule tokens `panel_2` vs `SCREAMING_SNAKE` `panel_3`) et remettre tous les témoins sur le statut `A_CODER` avant leur implémentation exécutable PyPy en Étape 4 (`G3_T1`, `G3_T2` et `R5_T1` portent actuellement `OK` depuis la maquette Python locale de `panel_2`).",
            "",
        ]
    )

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Assemble contracts/tiles_canon_v6_3.json depuis contracts/panels/panel_{1,2,3}.json "
            "et exporte docs/panel_canon_v6_3_passe1.md."
        )
    )
    parser.add_argument(
        "--panels-dir",
        type=Path,
        default=PANELS_DIR,
        help="Répertoire contenant panel_1.json, panel_2.json et panel_3.json.",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        default=V6_3_CONTRACT_PATH,
        help="Chemin du contrat canonique assemblé (défaut: contracts/tiles_canon_v6_3.json).",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=DEFAULT_MARKDOWN_OUTPUT,
        help="Chemin du document Markdown Passe 1 (défaut: docs/panel_canon_v6_3_passe1.md).",
    )
    parser.add_argument(
        "--date",
        default="2026-11-26",
        help="Date ISO (YYYY-MM-DD) inscrite dans _meta.genere_le.",
    )
    args = parser.parse_args()

    doc, report = assemble_canon_v6_3(args.panels_dir, genere_le=args.date)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    md = render_canon_passe1_markdown(doc, report)
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(md, encoding="utf-8", newline="\n")

    print(
        f"assemble_canon_v6_3.py : OK -> {args.output_json.as_posix()} "
        f"(30 slots : 22 P1 + 4 P2 + 4 P3, audit_197={report['verdict_global']}, "
        f"0 erreur, twists={report['Q02_twists_2K3']['nombre']}, "
        f"lois={report['Q01_lois_passives']['nombre']}/5 max={report['Q01_lois_passives']['max_par_assise']}, "
        f"eveil={report['I04_couverture_eveil']['nombre']}, "
        f"leviers={len(report['I05_couverture_sommeil']['leviers'])}, "
        f"enrac={report['I06_enracinement']['nombre']})"
    )
    print(
        f"Export Markdown Étape 3 : OK -> {args.output_md.as_posix()} "
        f"({len(md.splitlines())} lignes, {len(md.encode('utf-8'))} octets)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
