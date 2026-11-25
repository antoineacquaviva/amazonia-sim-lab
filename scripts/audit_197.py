"""Audit structurel et mathématique sur les 197 assises canoniques (v6.2 & v6.3).

Vérifie les invariants structurels définis dans `docs/cadrage_tuiles_v6_3.md` (§5.3) :
- `C01_mem_debt` : dette mémorielle nulle (aucun modificateur flottant de tour), zéro code d'étape,
  zéro vestige obsolète de pioche/paquet ;
- `I01_cloture_elargie_197` : clôture de disponibilité sur 100 % des 64 assises de chaque tuile
  (en incluant socle, accessoires natifs des Peuples présents, la tuile elle-même et sa tuile jumelle
  de lisière `Y>X` co-présente à 100 %) + exclusivité stricte des Insectes aux 10 tuiles de `I` ;
- `I02_autonomie_A0` : autonomie stricte sur `{H, E, I}` pour `R1, R2, R6, R10, M4, M5` ;
- `I03_divergence_lisiere` : sorties principales distinctes sur `X>Y` vs `Y>X` et zéro boucle fermée à 2 ;
- `I04_couverture_eveil` : quotas `(i) + (ii)` (≥ 9 Gardiens catalyseurs, 0/196 assises découvertes,
  15/15 Gardiens rentables en double ouverture) ;
- `I05_couverture_sommeil` : ≥ 3 des 4 lisières `E–{M,R,O,I}` avec levier de Rêve (0/30 assises `E` sans `H`) ;
- `I06_enracinement` : 3 à 5 tuiles à synergie d'Enracinement volontaire ;
- `Q01_lois_passives` : ≤ 5 lois passives dans le panel et ≤ 2 sur chacune des 197 assises ;
- `Q02_twists_2K3` : ≥ 6 twists, ≥ 1 par Peuple d'origine et ≤ 1 par lisière ;
- `I07_zero_c02` : AUCUNE vérification ni métrique de comptage de mots, de phrases ou de conditions.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from campaigns.designs import CanonicalAssise, enumerate_197_canonical_assises
from scripts.tiles_v6_3_schema import (
    A0_AUTONOMOUS_SLOTS,
    I_LISIERE_SLOTS,
    LOCKED_GARDIEN_CASTING_V6_3,
    SLOTS_BY_ID,
    SLOTS_SPEC_30,
    is_v6_3_tiles_contract,
    validate_tiles_canon_v6_3,
)

# États garantis disponibles par le socle v6.2 sur 100 % des 197 assises
SOCLE_STATES: frozenset[str] = frozenset(
    {
        "ARBRE",
        "SOUCHE",
        "ROUTE",
        "ROUGE",
        "DEFENSEUR_ATTENTE",
        "DEFENSEUR_REDEPLOYE",
        "PIEGE",
        "SABOTAGE",
        "MOBILISATION",
        "RANG_MACHINE",
        "DES_SOUS_PARAVENT",
        "FURTIVITE",
        "RATISSAGE",
    }
)

# États natifs garantis dès que le Peuple est assis à la table (Accessoires T1 & Modules)
PEUPLE_NATIVE_STATES: dict[str, frozenset[str]] = {
    "H": frozenset({"TAMBOUR", "CHANT", "POSITION_REVE", "RANG_REVE", "ANNULATION"}),
    "E": frozenset({"POSITION_REVE", "RANG_REVE", "ANNULATION"}),
    "M": frozenset({"DUEL", "TERRITOIRE", "GARDIEN"}),
    "R": frozenset({"GARDIEN"}),
    "O": frozenset({"DE_ENVOL", "PERCHOIR", "PLUME", "GARDIEN"}),
    "I": frozenset({"INSECTE", "INSECTE_RANG", "NID", "NID_ACTIVE"}),
}

INSECT_STATE_TOKENS: frozenset[str] = frozenset(
    {"INSECTE", "INSECTE_PASSAGER", "INSECTE_RANG", "NID", "NID_ACTIVE"}
)
GARDIEN_DEPENDENCY_TOKENS: frozenset[str] = frozenset({"GARDIEN", "PARI_GLISSE"})

ANIMAL_PEUPLES: tuple[str, ...] = ("M", "R", "O")
NON_ANIMAL_PEUPLES: frozenset[str] = frozenset({"H", "E", "I"})
ALL_PEUPLES: tuple[str, ...] = ("H", "E", "M", "R", "O", "I")

ANIMAL_ANIMAL_BORDERS: tuple[tuple[str, str], ...] = (
    ("M", "R"),
    ("M", "O"),
    ("R", "O"),
)
E_NON_H_BORDERS: tuple[tuple[str, str], ...] = (
    ("E", "M"),
    ("E", "R"),
    ("E", "O"),
    ("E", "I"),
)

# Expressions d'hygiène purement structurelle (ZÉRO regex de mots, phrases ou conditions — I07)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_BR_SPLIT_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_STEP_CODE_RE = re.compile(r"\b[1-6]\.[0-3]\b")
_INSECT_LEXICON_RE = re.compile(r"(?i)\b(?:insectes?|nids?|essaims?|migrations?)\b")
_GARDIEN_LEXICON_RE = re.compile(r"(?i)\b(?:gardiens?|éveil|encoches?|résonance)\b")

_MEM_DEBT_PATTERNS: tuple[str, ...] = (
    "pour ce tour",
    "jusqu'à la fin du tour",
    "jusqu’à la fin du tour",
)

BANNED_OBSOLETE_TILE_TERMS: tuple[str, ...] = (
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
)


@dataclass(frozen=True, slots=True)
class AuditTileSpec:
    """Vue normalisée d'une tuile (v6.2 ou v6.3) pour l'audit sur les 197 assises."""

    slot_id: str
    famille: str
    origine: str
    voisin: str
    alias_oriente: str
    nature: str  # "ACTION" | "LOI_PASSIVE"
    est_twist: bool
    roles_portes: frozenset[str]
    entrees: tuple[str, ...]
    sorties: tuple[str, ...]
    cablage: tuple[int, ...] | None
    declencheurs_amorces: tuple[str, ...]
    double_ouverture: str | None
    rule_texts: tuple[str, ...]
    plateau_texts: tuple[str, ...]
    nom_court: str
    titre_complet: str
    is_draft_empty: bool


def _undirected_edge(a: str, b: str) -> tuple[str, str]:
    return (a, b) if a < b else (b, a)


def _border_label(edge: tuple[str, str]) -> str:
    order = {p: i for i, p in enumerate(ALL_PEUPLES)}
    p1, p2 = sorted(edge, key=lambda p: order.get(p, 99))
    return f"{p1}–{p2}"


def _extract_v6_2_roles(slot_id: str, prof: Mapping[str, Any]) -> frozenset[str]:
    roles: set[str] = set()
    tags = {str(t).upper() for t in (prof.get("tags") or [])}
    role_lines = " ".join(str(x) for x in (prof.get("role_porte") or [])).lower()

    if "CATALYSEUR_EVEIL" in tags or "catalyseur" in role_lines:
        roles.add("CATALYSEUR_EVEIL")
    if "LEVIER_REVE" in tags or "levier" in role_lines:
        roles.add("LEVIER_REVE")
    if "ENRACINEMENT" in tags or "enracinement" in role_lines:
        roles.add("ENRACINEMENT")
    if str(prof.get("nature", "")).lower() == "loi_passive" or "LOI_PASSIVE" in tags:
        roles.add("LOI_PASSIVE")
    if slot_id in A0_AUTONOMOUS_SLOTS or "A0" in tags:
        roles.add("AUTONOMIE_A0")
    if bool(prof.get("est_twist_canon0", False)) or "TWIST" in tags:
        roles.add("TWIST_2K3")
    return frozenset(roles)


def normalize_catalog_for_audit(doc: Mapping[str, Any]) -> tuple[str, dict[str, AuditTileSpec]]:
    """Convertit un contrat JSON `v6.2` ou `v6.3` en dictionnaire `{slot_id: AuditTileSpec}`."""
    is_v63 = is_v6_3_tiles_contract(doc)
    version_tag = "v6.3" if is_v63 else "v6.2"
    raw_tiles = doc.get("tuiles_ciblees")
    if not isinstance(raw_tiles, Mapping):
        raise TypeError("Champ 'tuiles_ciblees' absent ou invalide")

    specs: dict[str, AuditTileSpec] = {}
    for sid, (exp_fam, exp_orig, exp_vois, exp_alias) in SLOTS_BY_ID.items():
        entry = raw_tiles.get(sid)
        if not isinstance(entry, Mapping):
            continue

        if is_v63:
            tp = entry.get("tuile_plateau") or {}
            cj = entry.get("carte_joueur") or {}
            tr = cj.get("texte_regle") or {}
            mcp = tp.get("mots_cles_plateau") or {}
            rule_texts = tuple(
                str(tr.get(k)).strip()
                for k in ("face_1", "face_2", "enracine")
                if isinstance(tr.get(k), str) and str(tr.get(k)).strip()
            )
            plateau_texts = tuple(
                s
                for s in (
                    str(tp.get("nom_court") or "").strip(),
                    str(tp.get("resume_plateau") or "").strip(),
                    str(mcp.get("face_1") or "").strip(),
                    str(mcp.get("face_2") or "").strip(),
                    str(mcp.get("enracine") or "").strip(),
                )
                if s
            )
            cablage_raw = entry.get("cablage")
            cablage = tuple(int(x) for x in cablage_raw) if isinstance(cablage_raw, list) else None
            nature = str(entry.get("nature", "ACTION")).upper()
            specs[sid] = AuditTileSpec(
                slot_id=sid,
                famille=str(entry.get("famille", exp_fam)),
                origine=str(entry.get("origine", exp_orig)),
                voisin=str(entry.get("voisin", exp_vois)),
                alias_oriente=str(entry.get("alias_oriente", exp_alias)),
                nature="LOI_PASSIVE" if nature == "LOI_PASSIVE" else "ACTION",
                est_twist=bool(entry.get("est_twist", False)),
                roles_portes=frozenset(str(r) for r in (entry.get("roles_portes") or [])),
                entrees=tuple(str(x).upper() for x in (entry.get("entrees") or [])),
                sorties=tuple(str(x).upper() for x in (entry.get("sorties") or [])),
                cablage=cablage,
                declencheurs_amorces=tuple(
                    str(x).upper() for x in (entry.get("declencheurs_amorces") or [])
                ),
                double_ouverture=(
                    str(entry["double_ouverture"]).strip()
                    if isinstance(entry.get("double_ouverture"), str)
                    else None
                ),
                rule_texts=rule_texts,
                plateau_texts=plateau_texts,
                nom_court=str(tp.get("nom_court") or ""),
                titre_complet=str(cj.get("titre_complet") or ""),
                is_draft_empty=str(entry.get("statut_conception", "")) == "A_CONCEVOIR",
            )
        else:
            profils = entry.get("profils") or {}
            prof = profils.get("A") if isinstance(profils, Mapping) else None
            if not isinstance(prof, Mapping):
                continue
            raw_html = str(prof.get("texte", "")).strip()
            parts = [
                _HTML_TAG_RE.sub("", part).strip()
                for part in _BR_SPLIT_RE.split(raw_html)
                if part.strip()
            ]
            cablage_raw = prof.get("cablage")
            cablage = tuple(int(x) for x in cablage_raw) if isinstance(cablage_raw, list) else None
            nature_raw = str(prof.get("nature", "action")).upper()
            specs[sid] = AuditTileSpec(
                slot_id=sid,
                famille=str(entry.get("famille", exp_fam)),
                origine=str(entry.get("origine", exp_orig)),
                voisin=exp_vois,
                alias_oriente=str(prof.get("alias_oriente", exp_alias)),
                nature="LOI_PASSIVE" if nature_raw == "LOI_PASSIVE" else "ACTION",
                est_twist=bool(prof.get("est_twist_canon0", False)),
                roles_portes=_extract_v6_2_roles(sid, prof),
                entrees=tuple(str(x).upper() for x in (prof.get("entrees") or [])),
                sorties=tuple(str(x).upper() for x in (prof.get("sorties") or [])),
                cablage=cablage,
                declencheurs_amorces=tuple(
                    str(x).upper() for x in (prof.get("declencheurs_amorces") or [])
                ),
                double_ouverture=(
                    str(prof["double_ouverture"]).strip()
                    if isinstance(prof.get("double_ouverture"), str)
                    else None
                ),
                rule_texts=tuple(parts),
                plateau_texts=(),
                nom_court=str(entry.get("nomBase") or prof.get("nom") or ""),
                titre_complet=str(prof.get("nom") or ""),
                is_draft_empty=False,
            )

    return version_tag, specs


def _build_border_to_tiles_map() -> dict[tuple[str, str], tuple[str, str]]:
    """Associe chaque lisière non orientée `{X, Y}` à sa paire exacte de tuiles `(X>Y, Y>X)`."""
    by_edge: dict[tuple[str, str], list[str]] = {}
    for sid, _, orig, vois, _ in SLOTS_SPEC_30:
        edge = _undirected_edge(orig, vois)
        by_edge.setdefault(edge, []).append(sid)
    out: dict[tuple[str, str], tuple[str, str]] = {}
    for edge, tids in by_edge.items():
        assert len(tids) == 2, f"Lisière {edge} invalide : {tids}"
        out[edge] = (tids[0], tids[1])
    return out


_BORDER_TO_TILES: dict[tuple[str, str], tuple[str, str]] = _build_border_to_tiles_map()


def _seated_tile_ids_for_assise(assise: CanonicalAssise) -> tuple[str, ...]:
    peuples = assise.peuples
    n = assise.n_players
    seated: list[str] = []
    for i in range(n):
        edge = _undirected_edge(peuples[i], peuples[(i + 1) % n])
        t1, t2 = _BORDER_TO_TILES[edge]
        seated.append(t1)
        seated.append(t2)
    return tuple(seated)


def _twin_slot_id(slot_id: str) -> str:
    _, orig, vois, _ = SLOTS_BY_ID[slot_id]
    t1, t2 = _BORDER_TO_TILES[_undirected_edge(orig, vois)]
    return t2 if t1 == slot_id else t1


def audit_tiles_catalog_197(
    doc: Mapping[str, Any],
    *,
    allow_draft: bool = False,
) -> dict[str, Any]:
    """Exécute l'audit structurel complet sur les 197 assises canoniques (zéro C02)."""
    version_tag, specs = normalize_catalog_for_audit(doc)
    assises = enumerate_197_canonical_assises()
    errors: list[str] = []

    expected_slots = set(SLOTS_BY_ID.keys())
    if set(specs.keys()) != expected_slots:
        errors.append(
            f"Emplacements incomplets : manquants={sorted(expected_slots - set(specs.keys()))}"
        )

    draft_slots = sorted(sid for sid, sp in specs.items() if sp.is_draft_empty)
    if draft_slots and not allow_draft:
        errors.append(
            f"{len(draft_slots)} emplacements encore en statut A_CONCEVOIR "
            f"(passer --allow-draft pour un audit partiel) : {draft_slots[:6]}"
        )

    # Pré-calcul des 197 assises et présence par tuile (64 assises exactes par tuile)
    assises_tiles: list[tuple[CanonicalAssise, tuple[str, ...]]] = [
        (a, _seated_tile_ids_for_assise(a)) for a in assises
    ]
    presence_counts: dict[str, int] = {sid: 0 for sid in expected_slots}
    for _, seated in assises_tiles:
        for sid in seated:
            presence_counts[sid] += 1
    bad_presence = {sid: cnt for sid, cnt in presence_counts.items() if cnt != 64}
    if bad_presence:
        errors.append(f"Présence par tuile != 64 assises : {bad_presence}")

    # 1. C01 — Dette mémorielle nulle, zéro code d'étape, zéro vestige obsolète (ZÉRO C02)
    mem_debt_hits: list[str] = []
    step_code_hits: list[str] = []
    obsolete_term_hits: list[str] = []
    for sid, sp in sorted(specs.items()):
        for idx_txt, txt in enumerate(sp.rule_texts, start=1):
            low = txt.lower()
            for pat in _MEM_DEBT_PATTERNS:
                if pat in low:
                    mem_debt_hits.append(f"{sid} (bloc {idx_txt}): modificateur flottant {pat!r}")
            steps = _STEP_CODE_RE.findall(txt)
            if steps:
                step_code_hits.append(f"{sid} (bloc {idx_txt}): code d'étape {steps}")
            for term in BANNED_OBSOLETE_TILE_TERMS:
                if re.search(rf"(?i)\b{re.escape(term)}\b", txt):
                    obsolete_term_hits.append(f"{sid} (bloc {idx_txt}): terme obsolète {term!r}")

    c01_issues = mem_debt_hits + step_code_hits + obsolete_term_hits
    errors.extend(c01_issues)

    # 2. I01 — Clôture de disponibilité élargie à la lisière (Y>X) + Exclusivité stricte Insectes
    insect_violations: list[str] = []
    closure_violations: list[str] = []
    twin_dependencies: list[dict[str, str]] = []

    for sid, sp in sorted(specs.items()):
        if sid not in I_LISIERE_SLOTS:
            bad_toks = [
                tok
                for tok in (*sp.entrees, *sp.sorties)
                if tok in INSECT_STATE_TOKENS
            ]
            if bad_toks:
                insect_violations.append(f"{sid}: jetons Insectes hors lisières de I ({bad_toks})")
            if "ICONE_INSECTE" in sp.declencheurs_amorces:
                insect_violations.append(f"{sid}: ICONE_INSECTE hors lisières de I")
            for txt in (*sp.rule_texts, *sp.plateau_texts):
                hits = _INSECT_LEXICON_RE.findall(txt)
                if hits:
                    insect_violations.append(f"{sid}: lexique Insecte/Essaim hors lisières de I ({hits})")

        if sp.is_draft_empty:
            continue

        twin_id = _twin_slot_id(sid)
        twin_spec = specs.get(twin_id)
        local_without_twin = (
            set(SOCLE_STATES)
            | set(PEUPLE_NATIVE_STATES[sp.origine])
            | set(PEUPLE_NATIVE_STATES[sp.voisin])
            | set(sp.sorties)
        )
        twin_outputs = set(twin_spec.sorties) if twin_spec is not None else set()

        for req_state in sp.entrees:
            missing_assises: list[str] = []
            for assise, seated in assises_tiles:
                if sid not in seated:
                    continue
                avail: set[str] = set(SOCLE_STATES)
                for p in assise.peuples:
                    avail.update(PEUPLE_NATIVE_STATES[p])
                for other_sid in seated:
                    other_sp = specs.get(other_sid)
                    if other_sp is not None:
                        avail.update(other_sp.sorties)
                if req_state not in avail:
                    missing_assises.append(assise.key)
            if missing_assises:
                closure_violations.append(
                    f"{sid} ({sp.alias_oriente}): entrée {req_state!r} absente sur "
                    f"{len(missing_assises)}/64 assises (ex. {missing_assises[:3]})"
                )
            elif req_state not in local_without_twin and req_state in twin_outputs:
                twin_dependencies.append(
                    {
                        "tuile": sid,
                        "alias": sp.alias_oriente,
                        "etat": req_state,
                        "fourni_par_jumelle": twin_id,
                    }
                )

    errors.extend(insect_violations)
    errors.extend(closure_violations)

    # 3. I02 — Autonomie A = 0 sur {H, E, I} (`R1, R2, R6, R10, M4, M5`)
    a0_violations: list[str] = []
    for sid in sorted(A0_AUTONOMOUS_SLOTS):
        sp = specs.get(sid)
        if sp is None:
            continue
        bad_g_toks = [
            tok for tok in (*sp.entrees, *sp.sorties) if tok in GARDIEN_DEPENDENCY_TOKENS
        ]
        if bad_g_toks:
            a0_violations.append(f"{sid}: dépendance Gardien interdite en A=0 ({bad_g_toks})")
        if sp.cablage is not None:
            a0_violations.append(f"{sid}: cablage Gardien interdit sur tuile A=0")
        if "ICONE_RESONANCE" in sp.declencheurs_amorces:
            a0_violations.append(f"{sid}: ICONE_RESONANCE interdite sur tuile A=0")
        for txt in (*sp.rule_texts, *sp.plateau_texts):
            g_hits = _GARDIEN_LEXICON_RE.findall(txt)
            if g_hits:
                a0_violations.append(f"{sid}: mention Gardien interdite en A=0 ({g_hits})")
    errors.extend(a0_violations)

    # 4. I03 — Divergence de lisière (`X>Y` vs `Y>X`) et zéro boucle fermée à 2
    divergence_details: list[dict[str, Any]] = []
    divergence_violations: list[str] = []
    for edge, (t1, t2) in sorted(_BORDER_TO_TILES.items()):
        s1 = specs.get(t1)
        s2 = specs.get(t2)
        if s1 is None or s2 is None:
            continue
        b_lbl = _border_label(edge)
        if s1.is_draft_empty or s2.is_draft_empty:
            divergence_details.append({"lisiere": b_lbl, "tuiles": [t1, t2], "statut": "DRAFT"})
            continue
        p1 = s1.sorties[0] if s1.sorties else "AUCUNE"
        p2 = s2.sorties[0] if s2.sorties else "AUCUNE"
        divergent = (p1 != p2) and p1 != "AUCUNE" and p2 != "AUCUNE"
        # Boucle d'états physique bidirectionnelle stricte entre les 2 tuiles de la lisière
        out1_to_in2 = sorted(set(s1.sorties) & set(s2.entrees))
        out2_to_in1 = sorted(set(s2.sorties) & set(s1.entrees))
        boucle_deux = bool(out1_to_in2) and bool(out2_to_in1)
        divergence_details.append(
            {
                "lisiere": b_lbl,
                "tuiles": [t1, t2],
                "sortie_principale": [p1, p2],
                "divergent": divergent,
                "boucle_a_deux_etats": boucle_deux,
            }
        )
        if not divergent:
            divergence_violations.append(
                f"Lisière {b_lbl} ({t1}/{t2}): sorties principales non divergentes ({p1!r} vs {p2!r})"
            )
        if boucle_deux:
            divergence_violations.append(
                f"Lisière {b_lbl} ({t1}/{t2}): boucle d'états fermée à deux "
                f"({t1}->{t2}: {out1_to_in2}, {t2}->{t1}: {out2_to_in1})"
            )
    errors.extend(divergence_violations)

    # 5. I04 — Couverture Éveil (i) + (ii) & rentabilité double activation
    eveil_violations: list[str] = []
    catalyseurs = sorted(
        sid
        for sid, sp in specs.items()
        if sp.famille == "GARDIEN" and "CATALYSEUR_EVEIL" in sp.roles_portes
    )
    regle_i: dict[str, int] = {}
    for animal in ANIMAL_PEUPLES:
        cnt = sum(
            1
            for sid in catalyseurs
            if specs[sid].origine == animal and specs[sid].voisin in NON_ANIMAL_PEUPLES
        )
        regle_i[animal] = cnt
        if not draft_slots and cnt < 2:
            eveil_violations.append(
                f"I04 (i): animal {animal} n'a que {cnt}/2 catalyseurs tournés vers {{H,E,I}}"
            )

    regle_ii: dict[str, bool] = {}
    for a1, a2 in ANIMAL_ANIMAL_BORDERS:
        t1, t2 = _BORDER_TO_TILES[_undirected_edge(a1, a2)]
        ok_pair = (t1 in catalyseurs) or (t2 in catalyseurs)
        regle_ii[f"{a1}–{a2}"] = ok_pair
        if not draft_slots and not ok_pair:
            eveil_violations.append(
                f"I04 (ii): lisière Animal–Animal {a1}–{a2} ({t1}/{t2}) sans catalyseur d'Éveil"
            )

    if not draft_slots and len(catalyseurs) < 9:
        eveil_violations.append(f"I04: seulement {len(catalyseurs)} < 9 Gardiens catalyseurs d'Éveil")

    assises_a_ge_1_uncovered: list[str] = []
    for assise, seated in assises_tiles:
        if any(p in ANIMAL_PEUPLES for p in assise.peuples) and not any(
            sid in catalyseurs for sid in seated
        ):
            assises_a_ge_1_uncovered.append(assise.key)
    if not draft_slots and assises_a_ge_1_uncovered:
        eveil_violations.append(
            f"I04: {len(assises_a_ge_1_uncovered)} assises avec A>=1 sans catalyseur d'Éveil "
            f"(ex. {assises_a_ge_1_uncovered[:3]})"
        )

    gardiens_sans_double_ouverture = sorted(
        sid
        for sid, sp in specs.items()
        if sp.famille == "GARDIEN"
        and not sp.is_draft_empty
        and not (sp.double_ouverture and sp.double_ouverture.strip())
    )
    if gardiens_sans_double_ouverture:
        eveil_violations.append(
            f"I04: Gardiens sans justification de double ouverture : {gardiens_sans_double_ouverture}"
        )
    errors.extend(eveil_violations)

    # 6. I05 — Couverture Sommeil (`E` sans `H`)
    sommeil_violations: list[str] = []
    leviers_reve = sorted(
        sid for sid, sp in specs.items() if "LEVIER_REVE" in sp.roles_portes
    )
    covered_e_borders: list[str] = []
    for p1, p2 in E_NON_H_BORDERS:
        t1, t2 = _BORDER_TO_TILES[_undirected_edge(p1, p2)]
        if t1 in leviers_reve or t2 in leviers_reve:
            covered_e_borders.append(f"{p1}–{p2}")
    if not draft_slots and len(covered_e_borders) < 3:
        sommeil_violations.append(
            f"I05: seulement {len(covered_e_borders)}/3 lisières E–{{M,R,O,I}} couvertes ({covered_e_borders})"
        )

    assises_e_sans_h_uncovered: list[str] = []
    assises_e_sans_h_total = 0
    for assise, seated in assises_tiles:
        if "E" in assise.peuples and "H" not in assise.peuples:
            assises_e_sans_h_total += 1
            if not any(sid in leviers_reve for sid in seated):
                assises_e_sans_h_uncovered.append(assise.key)
    if not draft_slots and assises_e_sans_h_uncovered:
        sommeil_violations.append(
            f"I05: {len(assises_e_sans_h_uncovered)}/{assises_e_sans_h_total} assises (E sans H) "
            f"sans levier de Rêve (ex. {assises_e_sans_h_uncovered[:3]})"
        )
    errors.extend(sommeil_violations)

    # 7. I06 — Synergies d'Enracinement (3 à 5 tuiles)
    enrac_violations: list[str] = []
    enracinements = sorted(
        sid for sid, sp in specs.items() if "ENRACINEMENT" in sp.roles_portes
    )
    if not draft_slots and not (3 <= len(enracinements) <= 5):
        enrac_violations.append(
            f"I06: nombre de synergies d'Enracinement hors [3, 5] (obtenu {len(enracinements)}: {enracinements})"
        )
    errors.extend(enrac_violations)

    # 8. Q01 — Lois passives (<= 5 global et <= 2 sur chacune des 197 assises)
    lois_violations: list[str] = []
    lois_passives = sorted(
        sid for sid, sp in specs.items() if sp.nature == "LOI_PASSIVE"
    )
    if len(lois_passives) > 5:
        lois_violations.append(
            f"Q01: {len(lois_passives)} > 5 lois passives dans le panel ({lois_passives})"
        )
    lois_dist: dict[int, int] = {}
    assises_trop_de_lois: list[str] = []
    for assise, seated in assises_tiles:
        c_lois = sum(1 for sid in seated if sid in lois_passives)
        lois_dist[c_lois] = lois_dist.get(c_lois, 0) + 1
        if c_lois > 2:
            assises_trop_de_lois.append(f"{assise.key}({c_lois})")
    if assises_trop_de_lois:
        lois_violations.append(
            f"Q01: {len(assises_trop_de_lois)} assises dépassent 2 lois passives "
            f"(ex. {assises_trop_de_lois[:5]})"
        )
    errors.extend(lois_violations)

    # 9. Q02 — Twists 2K3 (>= 6 twists, >= 1 par Peuple d'origine, <= 1 par lisière)
    twists_violations: list[str] = []
    twists = sorted(sid for sid, sp in specs.items() if sp.est_twist)
    if not draft_slots:
        if len(twists) < 6:
            twists_violations.append(f"Q02: seulement {len(twists)} < 6 Briques-Twists ({twists})")
        by_orig: dict[str, int] = {p: 0 for p in ALL_PEUPLES}
        by_edge: dict[tuple[str, str], list[str]] = {}
        for sid in twists:
            sp = specs[sid]
            by_orig[sp.origine] += 1
            e = _undirected_edge(sp.origine, sp.voisin)
            by_edge.setdefault(e, []).append(sid)
        missing_orig = [p for p, cnt in by_orig.items() if cnt < 1]
        if missing_orig:
            twists_violations.append(f"Q02: Peuples sans Twist : {missing_orig}")
        double_edges = {
            _border_label(e): tids for e, tids in by_edge.items() if len(tids) > 1
        }
        if double_edges:
            twists_violations.append(f"Q02: lisières portant > 1 Twist : {double_edges}")
    errors.extend(twists_violations)

    # 10. Validation schéma bi-composant & casting animalier pour v6.3
    v63_schema_errors: list[str] = []
    if version_tag == "v6.3":
        v63_schema_errors = validate_tiles_canon_v6_3(doc, strict=not allow_draft)
        errors.extend(v63_schema_errors)

    verdict = "OK" if not errors else "ECHEC"
    return {
        "schema_source": version_tag,
        "verdict_global": verdict,
        "c02_word_count_purged": True,
        "allow_draft": allow_draft,
        "draft_slots_count": len(draft_slots),
        "assises": {
            "total": len(assises),
            "par_N": {
                "N3": sum(1 for a in assises if a.n_players == 3),
                "N4": sum(1 for a in assises if a.n_players == 4),
                "N5": sum(1 for a in assises if a.n_players == 5),
                "N6": sum(1 for a in assises if a.n_players == 6),
            },
            "compositions": len({a.composition_key for a in assises}),
            "presence_par_emplacement": 64 if not bad_presence else bad_presence,
        },
        "C01_mem_debt": {
            "verdict": "OK" if not c01_issues else "ECHEC",
            "mem_debt_hits": mem_debt_hits,
            "step_code_hits": step_code_hits,
            "obsolete_term_hits": obsolete_term_hits,
        },
        "I01_cloture_elargie_197": {
            "verdict": "OK" if not (insect_violations or closure_violations) else "ECHEC",
            "insect_violations": insect_violations,
            "closure_violations": closure_violations,
            "dependances_jumelle_lisiere": twin_dependencies,
        },
        "I02_autonomie_A0": {
            "verdict": "OK" if not a0_violations else "ECHEC",
            "tuiles": sorted(A0_AUTONOMOUS_SLOTS),
            "violations": a0_violations,
        },
        "I03_divergence_lisiere": {
            "verdict": "OK" if not divergence_violations else "ECHEC",
            "lisieres": divergence_details,
            "violations": divergence_violations,
        },
        "I04_couverture_eveil": {
            "verdict": "OK" if not eveil_violations else "ECHEC",
            "catalyseurs": catalyseurs,
            "nombre": len(catalyseurs),
            "regle_i_par_animal": regle_i,
            "regle_ii_lisieres_animal_animal": regle_ii,
            "assises_A_ge_1_sans_catalyseur": assises_a_ge_1_uncovered,
            "gardiens_sans_double_ouverture": gardiens_sans_double_ouverture,
        },
        "I05_couverture_sommeil": {
            "verdict": "OK" if not sommeil_violations else "ECHEC",
            "leviers": leviers_reve,
            "lisieres_E_couvertes": covered_e_borders,
            "assises_E_sans_H": assises_e_sans_h_total,
            "assises_E_sans_H_sans_levier": assises_e_sans_h_uncovered,
        },
        "I06_enracinement": {
            "verdict": "OK" if not enrac_violations else "ECHEC",
            "tuiles": enracinements,
            "nombre": len(enracinements),
        },
        "Q01_lois_passives": {
            "verdict": "OK" if not lois_violations else "ECHEC",
            "lois": lois_passives,
            "nombre": len(lois_passives),
            "distribution_par_assise": {str(k): v for k, v in sorted(lois_dist.items())},
            "max_par_assise": max(lois_dist.keys()) if lois_dist else 0,
        },
        "Q02_twists_2K3": {
            "verdict": "OK" if not twists_violations else "ECHEC",
            "twists": twists,
            "nombre": len(twists),
            "violations": twists_violations,
        },
        "V63_schema_et_casting": {
            "verdict": "OK" if not v63_schema_errors else "ECHEC",
            "casting_attendu": LOCKED_GARDIEN_CASTING_V6_3 if version_tag == "v6.3" else None,
            "errors": v63_schema_errors,
        },
        "I07_zero_c02": {
            "verdict": "OK",
            "c02_word_count_purged": True,
            "note": "Aucune vérification de nombre de mots, de phrases ni de conditions.",
        },
        "errors": errors,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit structurel sur les 197 assises (v6.2 / v6.3 — zéro biais C02)."
    )
    parser.add_argument(
        "contract_path",
        nargs="?",
        default=str(ROOT / "contracts" / "tiles_canon_v6_2.json"),
        help="Chemin du contrat JSON de tuiles à auditer.",
    )
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help="Autorise les emplacements v6.3 encore en statut A_CONCEVOIR.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Affiche le rapport d'audit complet au format JSON.",
    )
    args = parser.parse_args()
    path = Path(args.contract_path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    report = audit_tiles_catalog_197(doc, allow_draft=args.allow_draft)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            f"audit_197.py [{report['schema_source']}] -> {report['verdict_global']} "
            f"(197 assises, C02 purgé={report['c02_word_count_purged']}, "
            f"lois={report['Q01_lois_passives']['nombre']}/5 max/assise={report['Q01_lois_passives']['max_par_assise']}, "
            f"eveil={report['I04_couverture_eveil']['nombre']}, "
            f"leviers_reve={len(report['I05_couverture_sommeil']['leviers'])}, "
            f"enrac={report['I06_enracinement']['nombre']}, "
            f"twists={report['Q02_twists_2K3']['nombre']})"
        )
        if report["errors"]:
            for err in report["errors"]:
                print(f"  - {err}")
    return 0 if report["verdict_global"] == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
