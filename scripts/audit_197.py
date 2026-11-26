"""Audit structurel et mathématique sur les 197 assises canoniques (v6.2 & v6.3.1).

Vérifie les 4 Murs Porteurs Physiques et les invariants structurels définis dans
`docs/cadrage_tuiles_v6_3.md` (§3.2 & §5.3) :
- `M1_TEMPS_BATAILLE` : zéro régénération Souche → Arbre debout durant les Tours 1–8
  (ni à la pose d'un Enracinement ; uniquement au décompte final via clause `enracine` ;
  conditions spatiales lisant un Arbre debout 100 % valides) ;
- `M2_CONSERVATION_THERMIQUE` : aucun Bleu Surchauffe posé à sec depuis la réserve ;
  tout Bleu provient du retournement/transfert d'un Rouge existant (ou lecture modifiée) ;
- `M3_INTEGRITE_PLATEAU_ET_ICONES` : immobilité absolue des Arbres/Souches (`2–2–3–3`),
  interdiction de couper volontairement un Arbre debout allié comme coût, et fixité
  d'icône des Gardiens en piste (au plus `1` Twist dédié sur 30 dans tout le panel) ;
- `M4_AUTONOMIE_PLANCHER_SOLO` : toute tuile construite seule dispose d'un effet utile
  garanti dès sa `Face 1`, sans prérequis bloquant dépendant d'une autre tuile — pas même
  sa jumelle de lisière `Y>X` (états inter-tuiles encouragés en `entrees_synergie` :
  alternatives `OU`, bonus `Si…` ou `Face 2`) ;
- `C01_mem_debt` : dette mémorielle nulle, zéro code d'étape, zéro vestige de pioche ;
- `I01_cloture_elargie_197` : exclusivité stricte Insectes aux 10 tuiles de `I`, clôture
  solo des `entrees_plancher` et couverture mesurée sur les 64 assises des `entrees_synergie` ;
- `I02_autonomie_A0`, `I03_divergence_lisiere`, `I04_couverture_eveil`, `I05_couverture_sommeil`,
  `I06_enracinement`, `Q01_lois_passives`, `Q02_twists_2K3`, `I07_zero_c02` (zéro C02).

Supporte également l'audit comparatif multi-panels (`--panels-dir contracts/panels`).
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
    MURS_PORTEURS_V6_3,
    SLOTS_BY_ID,
    SLOTS_SPEC_30,
    is_v6_3_tiles_contract,
    validate_tiles_canon_v6_3,
)

# États garantis disponibles par le socle v6.2 sur 100 % des 197 assises (même à 0 tuile construite)
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

# États natifs garantis dès que le Peuple est assis à la table (Accessoires T1 & Modules natifs)
PEUPLE_NATIVE_STATES: dict[str, frozenset[str]] = {
    "H": frozenset({"TAMBOUR", "CHANT", "POSITION_REVE", "RANG_REVE", "ANNULATION"}),
    "E": frozenset({"POSITION_REVE", "RANG_REVE", "ANNULATION"}),
    "M": frozenset({"DUEL", "TERRITOIRE", "GARDIEN"}),
    "R": frozenset({"GARDIEN"}),
    "O": frozenset({"DE_ENVOL", "PERCHOIR", "PLUME", "GARDIEN"}),
    "I": frozenset({"INSECTE", "INSECTE_RANG", "NID", "NID_ACTIVE"}),
}

# M4 : états créés exclusivement par d'autres tuiles (interdits comme prérequis bloquant Face 1)
TILE_ONLY_STATES: frozenset[str] = frozenset(
    {"BLEU", "CALE", "INSECTE_PASSAGER", "RECUL", "PARI_GLISSE"}
)

# M4 : accessoires progressifs stockés dans la réserve d'un Peuple précis
PROGRESSIVE_RESERVE_OWNER: dict[str, str] = {
    "ALTEREE": "E",
    "ALTERATION": "E",
    "ECAILLE": "R",
    "CROC": "R",
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

# Expressions d'hygiène structurelle (ZÉRO regex de comptage de mots, phrases ou conditions — I07)
_HTML_TAG_RE = re.compile(r"<[^>]+>")
_BR_SPLIT_RE = re.compile(r"<br\s*/?>", re.IGNORECASE)
_FACE_PREFIX_RE = re.compile(
    r"^\s*(?:Face\s+[12]|Enraciné|En\s+Parade|En\s+Migration|Loi\s+passive)\s*:\s*",
    re.IGNORECASE,
)
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+")
_CLAUSE_SPLIT_RE = re.compile(r"[.!?;]+")
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

# ---------------------------------------------------------------------------
# Expressions régulières des 4 Murs Porteurs Physiques (M1 à M4)
# ---------------------------------------------------------------------------

# M1 — Unité de temps de la bataille : aucune régénération Souche -> Arbre hors décompte final
_SOUCHE_TO_ARBRE_RE = re.compile(
    r"(?i)(?:"
    r"\b(?:retourn\w*|transform\w*|converti\w*|remet\w*|redress\w*|pass\w*|bascul\w*|chang\w*)"
    r"[^.;:]{0,90}\bsouches?\b[^.;:]{0,70}"
    r"\b(?:en\s+arbres?|sur\s+(?:sa|leur)\s+face\s+arbres?|face\s+arbres?|arbres?\s+debout)\b"
    r"|\bsouches?\b[^.;:]{0,55}\b(?:redevien\w*|devien\w*|repouss\w*|se\s+retourne\w*)"
    r"[^.;:]{0,55}\barbres?\b"
    r"|\b(?:régénér\w*|faites\s+repousser|faire\s+repousser|repousser)\b[^.;:]{0,65}\b(?:souches?|arbres?)\b"
    r"|\bsouches?\s*(?:→|->|⇒)\s*arbres?\b"
    r"|\b(?:posez|ajoutez|placez|remettez|créez)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|des\s+|les?\s+)?arbres?\s+debout\b"
    r")"
)
_FINAL_SCORING_RE = re.compile(
    r"(?i)\b(?:au\s+décompte\s+final|en\s+fin\s+de\s+partie|décompte\s+final)\b"
)
_IMMEDIATE_ENRACINE_RE = re.compile(
    r"(?i)\b(?:lors\s+de\s+son\s+enracinement|à\s+la\s+pose|au\s+moment\s+de\s+l['’]enracinement|"
    r"quand\s+vous\s+enracinez|immédiatement|aussitôt|sur-le-champ)\b"
)
_PLATEAU_REGEN_ACTIVE_RE = re.compile(r"(?i)(?:\bsouches?\s*(?:→|->|⇒)\s*arbres?\b|\brégén\w*)")

# M2 — Conservation thermique : pas de Bleu Surchauffe posé à sec depuis la réserve
_RESERVE_BLEU_RE = re.compile(
    r"(?i)(?:(?:depuis|de)\s+la\s+réserve[^.!?;]{0,75}\b(?:bleus?|surchauffe)\b"
    r"|\b(?:bleus?|surchauffe)\b[^.!?;]{0,75}(?:depuis|de)\s+la\s+réserve)"
)
_SANS_ROUGE_BLEU_RE = re.compile(
    r"(?i)(?:\b(?:sans\s+(?:jeton\s+)?rouge|dépourvue\s+de\s+(?:jeton\s+)?rouge|"
    r"même\s+sans\s+rouge|sans\s+retourner\s+de\s+rouge)\b[^.!?;]{0,75}\b(?:bleus?|surchauffe)\b"
    r"|\b(?:bleus?|surchauffe)\b[^.!?;]{0,75}"
    r"\b(?:sans\s+(?:jeton\s+)?rouge|dépourvue\s+de\s+(?:jeton\s+)?rouge|même\s+sans\s+rouge)\b)"
)
_DRY_ADD_BLEU_RE = re.compile(
    r"(?i)\b(?:posez|placez|ajoutez|donnez|mettez|attribuez|gagnez|appliquez|infligez|créez|créer|poser|placer|ajouter)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|deux\s+|des\s+|le\s+|la\s+|les\s+)?"
    r"(?:jetons?\s+(?:puissance\s+)?(?:bleus?|de\s+surchauffe|surchauffe)|bleus?\s+surchauffe|surchauffe\s+bleue|bleus?\b)"
)
_BLEU_VALID_CONSERVATION_SOURCE_RE = re.compile(
    r"(?i)\b(?:rouges?|depuis\s+une\s+autre\s+machine|d['’]une\s+autre\s+machine|déplac\w*|transfér\w*|retourn\w*)\b"
)

# M3 — Intégrité 2–2–3–3 & fixité d'icône des Gardiens
_MOVE_ARBRE_SOUCHE_RE = re.compile(
    r"(?i)(?:"
    r"\b(?:déplac\w*|transfér\w*|gliss\w*|échang\w*|envoy\w*|transplant\w*|déracin\w*)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|deux\s+|des\s+|les?\s+|la\s+|l['’]|toutes?\s+les\s+|vos\s+|ses\s+|ces?\s+)?"
    r"(?:arbres?(?:\s+debout)?|souches?)\b"
    r"|\b(?:prenez|retirez)\s+(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+)?(?:arbres?(?:\s+debout)?|souches?)\b"
    r"[^.;:]{0,60}\b(?:posez|placez|reposez|déposez|remettez)[-\s](?:le|la|les)\s+(?:sur|vers)\b"
    r"|\b(?:posez|ajoutez|placez)\s+(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|des\s+)?souches?\b"
    r")"
)
_VOLUNTARY_CUT_ARBRE_RE = re.compile(
    r"(?i)(?:"
    r"\b(?:coupez|abattez|sacrifiez|détruisez|défaussez|retirez)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|deux\s+|des\s+|les?\s+|l['’]|vos\s+|ses\s+|votre\s+|son\s+)?arbres?(?:\s+debout)?\b"
    r"|\b(?:pouvez|devez|doit|pour|en)\s+(?:couper|abattre|sacrifier|détruire|défausser|retirer|coupant|abattant|sacrifiant)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|deux\s+|des\s+|les?\s+|l['’]|vos\s+|ses\s+|votre\s+|son\s+)?arbres?(?:\s+debout)?\b"
    r"|\b(?:retourn\w*|transform\w*|converti\w*|pass\w*)\s+"
    r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|deux\s+|des\s+|les?\s+|l['’]|vos\s+|ses\s+|votre\s+|son\s+)?arbres?(?:\s+debout)?\b"
    r"[^.;:]{0,45}\b(?:en\s+souches?|face\s+souche|sur\s+(?:sa|leur)\s+face\s+souche)\b"
    r")"
)
_DIRECT_PLAYER_CUT_IMPERATIVE_RE = re.compile(
    r"(?i)\b(?:coupez|abattez|sacrifiez|détruisez|défaussez|retirez|retournez)\b"
)
_MACHINE_CUT_CONTEXT_RE = re.compile(
    r"(?i)\b(?:machine|abatteuse|bulldozer|ne\s+pas\s+couper|sans\s+couper|empêch\w*|évit\w*|au\s+lieu\s+de\s+couper)\b"
)
_GARDIEN_JUMP_ICON_RE = re.compile(
    r"(?i)(?:"
    r"\b(?:déplac\w*|gliss\w*|chang\w*|échang\w*|permut\w*|saut\w*|bascul\w*|transfér\w*|repositionn\w*|migr\w*)"
    r"[^.;:]{0,60}\b(?:ce\s+gardien|un\s+(?:autre\s+)?gardien|cette\s+tuile(?:\s+gardien)?|le\s+gardien|deux\s+gardiens?)\b"
    r"[^.;:]{0,70}\b(?:icônes?|piste\s+des\s+gardiens|case\s+(?:voisine|libre|adjacente|d['’]icône))\b"
    r"|\b(?:ce\s+gardien|cette\s+tuile|un\s+gardien)\b[^.;:]{0,50}"
    r"\b(?:saute|change\s+d['’]icône|se\s+déplace|glisse|migre|passe)\b"
    r"[^.;:]{0,60}\b(?:icônes?|case\s+(?:voisine|libre|adjacente)|autre\s+icône)\b"
    r"|\b(?:changez|changer|permutez|permuter|échangez|échanger)\b[^.;:]{0,40}\bd['’]icône\b"
    r"|\bd['’]une\s+icône\s+à\s+une\s+autre\b"
    r")"
)
_INSECT_ICON_MIGRATION_RE = re.compile(r"(?i)\b(?:insectes?|essaims?)\b[^.;:]{0,45}\bicônes?\b")

# M4 — Autonomie plancher en solo (prélèvement explicite en réserve voisin & détection Face 1 bloquée)
_RESERVE_DRAW_VERB_RE = re.compile(
    r"(?i)\b(?:réserve|prélev\w*|prenez\s+[^.;:]{0,35}réserve|ajoutez\s+[^.;:]{0,35}réserve|"
    r"posez\s+[^.;:]{0,35}réserve|glissez\s+[^.;:]{0,35}réserve)\b"
)
_ALT_OR_FALLBACK_RE = re.compile(r"(?i)\b(?:ou|sinon|à\s+défaut)\b")

_M4_LEXICAL_BLOCKERS: tuple[tuple[str, re.Pattern[str], re.Pattern[str] | None], ...] = (
    (
        "BLEU",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\b(?:jetons?\s+bleus?|bleus?\s+surchauffe|surchauffe\s+bleue)\b"
            r"|\b(?:défaussez|retirez|consommez|dépensez|déplacez|transférez)\s+"
            r"(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|une\s+|le\s+|les\s+)?(?:jetons?\s+bleus?|bleus?\s+surchauffe)\b)"
        ),
        re.compile(r"(?i)\b(?:retourn\w*[^.;:]{0,45}\brouge\w*)\b"),
    ),
    (
        "CALE",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\b(?:calée?s?|porte\s+une\s+cale|portant\s+une\s+cale|avec\s+une\s+cale)\b"
            r"|\b(?:retirez|défaussez|consommez|dépensez)\s+(?:une\s+|la\s+|1\s+)?cale\b)"
        ),
        re.compile(r"(?i)\b(?:glissez|posez|placez)\s+[^.;:]{0,45}\bcale\b"),
    ),
    (
        "INSECTE_PASSAGER",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\binsectes?\s+passagers?\b"
            r"|\b(?:défaussez|retirez|déplacez)\s+(?:(?:jusqu['’]à\s+)?\d+\s+|un\s+|l['’])?insectes?\s+passagers?\b)"
        ),
        re.compile(r"(?i)\b(?:chargez|embarquez|posez|placez|mont\w*)\s+[^.;:]{0,45}\bpassager\b"),
    ),
    (
        "ALTEREE",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\b(?:machines?\s+altérées?|jetons?\s+d['’]altération)\b"
            r"|\b(?:retirez|défaussez|consommez|transfér\w*)\s+(?:un\s+|1\s+|l['’])?(?:jetons?\s+d['’])?altération\b)"
        ),
        re.compile(r"(?i)\b(?:altérez|altérer)\b"),
    ),
    (
        "ECAILLE",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\b(?:jetons?\s+)?écailles?\b"
            r"|\b(?:retirez|défaussez|consommez)\s+(?:un\s+|1\s+|une\s+)?(?:jetons?\s+)?écailles?\b)"
        ),
        None,
    ),
    (
        "CROC",
        re.compile(
            r"(?i)(?:\b(?:si|quand|lorsqu\w*|sur)\b[^.;:]{0,55}\bcroc\b"
            r"|\b(?:déplacez|retirez|récupérez)\s+le\s+croc\b)"
        ),
        None,
    ),
)


@dataclass(frozen=True, slots=True)
class AuditTileSpec:
    """Vue normalisée d'une tuile (v6.2 ou v6.3.x) pour l'audit sur les 197 assises."""

    slot_id: str
    famille: str
    origine: str
    voisin: str
    alias_oriente: str
    nature: str  # "ACTION" | "LOI_PASSIVE"
    est_twist: bool
    roles_portes: frozenset[str]
    entrees_plancher: tuple[str, ...]
    entrees_synergie: tuple[str, ...]
    entrees: tuple[str, ...]
    has_explicit_floor_split: bool
    sorties: tuple[str, ...]
    cablage: tuple[int, ...] | None
    declencheurs_amorces: tuple[str, ...]
    double_ouverture: str | None
    face_1_text: str
    face_2_text: str | None
    enracine_text: str | None
    rule_texts: tuple[str, ...]
    plateau_active_texts: tuple[str, ...]
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


def _split_v6_2_html_faces(famille: str, raw_html: str) -> tuple[str, str | None, str | None, tuple[str, ...]]:
    parts = [
        _HTML_TAG_RE.sub("", part).strip()
        for part in _BR_SPLIT_RE.split(raw_html)
        if part.strip()
    ]
    f1 = ""
    f2: str | None = None
    enr: str | None = None
    for part in parts:
        low = part.lower()
        clean = _FACE_PREFIX_RE.sub("", part).strip()
        if low.startswith("enraciné"):
            enr = clean
        elif low.startswith("face 2"):
            f2 = clean
        elif not f1:
            f1 = clean
        elif famille == "GARDIEN" and f2 is None:
            f2 = clean
    return f1, f2, enr, tuple(parts)


def normalize_catalog_for_audit(doc: Mapping[str, Any]) -> tuple[str, dict[str, AuditTileSpec]]:
    """Convertit un contrat JSON `v6.2` ou `v6.3.x` en dictionnaire `{slot_id: AuditTileSpec}`."""
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
            f1 = str(tr.get("face_1") or "").strip()
            f2 = str(tr.get("face_2")).strip() if isinstance(tr.get("face_2"), str) and str(tr.get("face_2")).strip() else None
            enr = str(tr.get("enracine")).strip() if isinstance(tr.get("enracine"), str) and str(tr.get("enracine")).strip() else None
            rule_texts = tuple(t for t in (f1, f2, enr) if t)
            plateau_active_texts = tuple(
                s
                for s in (
                    str(mcp.get("face_1") or "").strip(),
                    str(mcp.get("face_2") or "").strip(),
                )
                if s
            )
            plateau_texts = tuple(
                s
                for s in (
                    str(tp.get("nom_court") or "").strip(),
                    str(tp.get("resume_plateau") or "").strip(),
                    *plateau_active_texts,
                    str(mcp.get("enracine") or "").strip(),
                )
                if s
            )
            cablage_raw = entry.get("cablage")
            cablage = tuple(int(x) for x in cablage_raw) if isinstance(cablage_raw, list) else None
            nature = str(entry.get("nature", "ACTION")).upper()

            has_explicit_split = "entrees_plancher" in entry
            raw_entrees = tuple(str(x).upper() for x in (entry.get("entrees") or []))
            if has_explicit_split:
                e_plancher = tuple(str(x).upper() for x in (entry.get("entrees_plancher") or []))
                e_synergie = tuple(str(x).upper() for x in (entry.get("entrees_synergie") or []))
                e_union = tuple(dict.fromkeys((*e_plancher, *e_synergie, *raw_entrees)))
            else:
                e_plancher = raw_entrees
                e_synergie = tuple(str(x).upper() for x in (entry.get("entrees_synergie") or []))
                e_union = tuple(dict.fromkeys((*raw_entrees, *e_synergie)))

            specs[sid] = AuditTileSpec(
                slot_id=sid,
                famille=str(entry.get("famille", exp_fam)),
                origine=str(entry.get("origine", exp_orig)),
                voisin=str(entry.get("voisin", exp_vois)),
                alias_oriente=str(entry.get("alias_oriente", exp_alias)),
                nature="LOI_PASSIVE" if nature == "LOI_PASSIVE" else "ACTION",
                est_twist=bool(entry.get("est_twist", False)),
                roles_portes=frozenset(str(r) for r in (entry.get("roles_portes") or [])),
                entrees_plancher=e_plancher,
                entrees_synergie=e_synergie,
                entrees=e_union,
                has_explicit_floor_split=has_explicit_split,
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
                face_1_text=f1,
                face_2_text=f2,
                enracine_text=enr,
                rule_texts=rule_texts,
                plateau_active_texts=plateau_active_texts,
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
            fam = str(entry.get("famille", exp_fam))
            f1, f2, enr, parts = _split_v6_2_html_faces(fam, str(prof.get("texte", "")).strip())
            cablage_raw = prof.get("cablage")
            cablage = tuple(int(x) for x in cablage_raw) if isinstance(cablage_raw, list) else None
            nature_raw = str(prof.get("nature", "action")).upper()
            raw_entrees = tuple(str(x).upper() for x in (prof.get("entrees") or []))
            specs[sid] = AuditTileSpec(
                slot_id=sid,
                famille=fam,
                origine=str(entry.get("origine", exp_orig)),
                voisin=exp_vois,
                alias_oriente=str(prof.get("alias_oriente", exp_alias)),
                nature="LOI_PASSIVE" if nature_raw == "LOI_PASSIVE" else "ACTION",
                est_twist=bool(prof.get("est_twist_canon0", False)),
                roles_portes=_extract_v6_2_roles(sid, prof),
                entrees_plancher=raw_entrees,
                entrees_synergie=(),
                entrees=raw_entrees,
                has_explicit_floor_split=False,
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
                face_1_text=f1,
                face_2_text=f2,
                enracine_text=enr,
                rule_texts=parts,
                plateau_active_texts=(),
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


def _explicitly_draws_neighbor_reserve(face_1_text: str, req_state: str) -> bool:
    """Vrai si `face_1_text` indique explicitement prélever l'accessoire dans la réserve du voisin."""
    if not face_1_text or not _RESERVE_DRAW_VERB_RE.search(face_1_text):
        return False
    low = face_1_text.lower()
    if req_state in ("ALTEREE", "ALTERATION"):
        return "altér" in low
    if req_state == "ECAILLE":
        return "écaille" in low or "ecaille" in low
    if req_state == "CROC":
        return "croc" in low
    return False


# ---------------------------------------------------------------------------
# Contrôleurs des 4 Murs Porteurs Physiques (M1..M4)
# ---------------------------------------------------------------------------


def _check_m1_temps_bataille(specs: Mapping[str, AuditTileSpec]) -> list[str]:
    """M1 : aucune régénération Souche -> Arbre debout durant les Tours 1–8 ni à la pose d'Enracinement."""
    violations: list[str] = []
    for sid, sp in sorted(specs.items()):
        if sp.is_draft_empty:
            continue

        # 1. Faces actives (Tours 1–8)
        for face_lbl, ftext in (("face_1", sp.face_1_text), ("face_2", sp.face_2_text)):
            if not ftext:
                continue
            for sent in _SENTENCE_SPLIT_RE.split(ftext):
                sent = sent.strip()
                if not sent or not _SOUCHE_TO_ARBRE_RE.search(sent):
                    continue
                if not _FINAL_SCORING_RE.search(sent) or _IMMEDIATE_ENRACINE_RE.search(sent):
                    violations.append(
                        f"M1 [{sid}.{face_lbl}]: régénération Souche → Arbre interdite pendant "
                        f"les Tours 1–8 ({sent!r})"
                    )

        # 2. Clause Enraciné : Souche -> Arbre autorisée EXCLUSIVEMENT au décompte final
        if sp.enracine_text:
            for sent in _SENTENCE_SPLIT_RE.split(sp.enracine_text):
                sent = sent.strip()
                if not sent or not _SOUCHE_TO_ARBRE_RE.search(sent):
                    continue
                if _IMMEDIATE_ENRACINE_RE.search(sent) or not _FINAL_SCORING_RE.search(sent):
                    violations.append(
                        f"M1 [{sid}.enracine]: régénération Souche → Arbre autorisée exclusivement "
                        f"au décompte final, jamais à la pose ({sent!r})"
                    )

        # 3. Mots-clés actifs sur la Mini-Tuile Plateau (hors clause Enraciné)
        for ptxt in sp.plateau_active_texts:
            if _PLATEAU_REGEN_ACTIVE_RE.search(ptxt) and not _FINAL_SCORING_RE.search(ptxt):
                violations.append(
                    f"M1 [{sid}.tuile_plateau]: régénération Souche → Arbre interdite sur face active ({ptxt!r})"
                )

    return violations


def _check_m2_conservation_thermique(specs: Mapping[str, AuditTileSpec]) -> list[str]:
    """M2 : aucun Bleu Surchauffe posé à sec depuis la réserve sur machine sans Rouge."""
    violations: list[str] = []
    for sid, sp in sorted(specs.items()):
        if sp.is_draft_empty:
            continue
        blocks = (
            ("face_1", sp.face_1_text),
            ("face_2", sp.face_2_text),
            ("enracine", sp.enracine_text),
        )
        for b_lbl, text in blocks:
            if not text:
                continue
            for clause in _CLAUSE_SPLIT_RE.split(text):
                clause = clause.strip()
                if not clause:
                    continue
                if _RESERVE_BLEU_RE.search(clause):
                    violations.append(
                        f"M2 [{sid}.{b_lbl}]: Bleu Surchauffe depuis la réserve interdit ({clause!r})"
                    )
                    continue
                if _SANS_ROUGE_BLEU_RE.search(clause):
                    violations.append(
                        f"M2 [{sid}.{b_lbl}]: Bleu Surchauffe sur machine sans Rouge interdit ({clause!r})"
                    )
                    continue
                if _DRY_ADD_BLEU_RE.search(clause) and not _BLEU_VALID_CONSERVATION_SOURCE_RE.search(
                    clause
                ):
                    violations.append(
                        f"M2 [{sid}.{b_lbl}]: pose à sec d'un Bleu Surchauffe sans retournement "
                        f"d'un Rouge existant ({clause!r})"
                    )
    return violations


def _check_m3_integrite_plateau_et_icones(
    specs: Mapping[str, AuditTileSpec],
) -> tuple[list[str], list[str]]:
    """M3 : immobilité Arbres/Souches (2–2–3–3), zéro coupe volontaire alliée, fixité d'icône ≤ 1 Twist."""
    violations: list[str] = []
    icon_jumpers: list[str] = []

    for sid, sp in sorted(specs.items()):
        if sp.is_draft_empty:
            continue
        blocks = (
            ("face_1", sp.face_1_text),
            ("face_2", sp.face_2_text),
            ("enracine", sp.enracine_text),
        )
        tile_jumps_icon = False
        for b_lbl, text in blocks:
            if not text:
                continue
            for clause in _CLAUSE_SPLIT_RE.split(text):
                clause = clause.strip()
                if not clause:
                    continue
                # M3a — Immobilité Arbre / Souche (dotation 2–2–3–3)
                if _MOVE_ARBRE_SOUCHE_RE.search(clause):
                    violations.append(
                        f"M3a [{sid}.{b_lbl}]: déplacement/ajout d'Arbre ou Souche violant 2–2–3–3 ({clause!r})"
                    )
                # M3b — Interdiction de couper volontairement un Arbre debout allié comme coût
                if _VOLUNTARY_CUT_ARBRE_RE.search(clause):
                    is_machine_ctx = bool(_MACHINE_CUT_CONTEXT_RE.search(clause)) and not bool(
                        _DIRECT_PLAYER_CUT_IMPERATIVE_RE.search(clause)
                    )
                    if not is_machine_ctx:
                        violations.append(
                            f"M3b [{sid}.{b_lbl}]: coupe/sacrifice volontaire d'un Arbre debout allié interdit ({clause!r})"
                        )
                # M3c — Saut d'icône d'une Mini-Tuile Gardien en piste
                if _GARDIEN_JUMP_ICON_RE.search(clause) and not _INSECT_ICON_MIGRATION_RE.search(
                    clause
                ):
                    tile_jumps_icon = True

        if tile_jumps_icon:
            icon_jumpers.append(sid)
            if not sp.est_twist:
                violations.append(
                    f"M3c [{sid}]: saut d'icône sur la Piste des Gardiens interdit sur tuile non-Twist"
                )

    if len(icon_jumpers) > 1:
        violations.append(
            f"M3c: {len(icon_jumpers)} > 1 tuiles sautent d'une icône à une autre dans le panel "
            f"({icon_jumpers} — plafond absolu : 1 seul Twist dédié sur 30)"
        )

    return violations, icon_jumpers


def _check_m4_autonomie_plancher_solo(specs: Mapping[str, AuditTileSpec]) -> list[str]:
    """M4 : toute tuile construite seule doit avoir un effet utile garanti dès sa Face 1."""
    violations: list[str] = []

    for sid, sp in sorted(specs.items()):
        if sp.is_draft_empty:
            continue

        solo_native = (
            set(SOCLE_STATES)
            | set(PEUPLE_NATIVE_STATES[sp.origine])
            | set(PEUPLE_NATIVE_STATES[sp.voisin])
        )

        # 1. Contrôle typé sur `entrees_plancher` (ou `entrees` si non séparé)
        for req in sp.entrees_plancher:
            if req in TILE_ONLY_STATES:
                violations.append(
                    f"M4 [{sid} ({sp.alias_oriente})]: prérequis bloquant Face 1 {req!r} produit "
                    f"exclusivement par d'autres tuiles (déplacer dans entrees_synergie en OU / Si… / Face 2)"
                )
            elif req in PROGRESSIVE_RESERVE_OWNER:
                owner = PROGRESSIVE_RESERVE_OWNER[req]
                if sp.origine == owner:
                    continue
                if sp.voisin == owner and _explicitly_draws_neighbor_reserve(sp.face_1_text, req):
                    continue
                violations.append(
                    f"M4 [{sid} ({sp.alias_oriente})]: prérequis bloquant Face 1 {req!r} hors "
                    f"origine {owner} sans prélèvement explicite en réserve du voisin "
                    f"(déplacer dans entrees_synergie ou prélever depuis la réserve)"
                )
            elif req not in solo_native:
                violations.append(
                    f"M4 [{sid} ({sp.alias_oriente})]: prérequis bloquant Face 1 {req!r} non "
                    f"garanti en solo par socle + {sp.origine} + {sp.voisin}"
                )

        # 2. Contrôle lexical Face 1 : détecte une Face 1 entièrement bloquée sur un état inter-tuile
        if sp.face_1_text:
            sentences = [s.strip() for s in _SENTENCE_SPLIT_RE.split(sp.face_1_text) if s.strip()]
            if sentences:
                for state_tok, blocker_re, self_prod_re in _M4_LEXICAL_BLOCKERS:
                    # Autoriser l'accessoire progressif si la tuile est d'origine propriétaire ou prélève en réserve voisin
                    owner = PROGRESSIVE_RESERVE_OWNER.get(state_tok)
                    if owner is not None:
                        if sp.origine == owner:
                            continue
                        if sp.voisin == owner and _explicitly_draws_neighbor_reserve(
                            sp.face_1_text, state_tok
                        ):
                            continue
                    # Si au moins une phrase offre un effet plancher autonome sans ce verrou (ou une alternative OU/sinon)
                    all_sentences_blocked = True
                    for sent in sentences:
                        has_blocker = bool(blocker_re.search(sent))
                        is_self_produced = bool(self_prod_re and self_prod_re.search(sent))
                        has_fallback = bool(_ALT_OR_FALLBACK_RE.search(sent))
                        if not has_blocker or is_self_produced or has_fallback:
                            all_sentences_blocked = False
                            break
                    if all_sentences_blocked:
                        violations.append(
                            f"M4 [{sid}.face_1]: la Face 1 dépend de manière bloquante de "
                            f"{state_tok!r} sans effet plancher solo ni alternative OU/sinon ({sp.face_1_text!r})"
                        )

    return violations


# ---------------------------------------------------------------------------
# Audit complet sur les 197 Assises Canoniques
# ---------------------------------------------------------------------------


def audit_tiles_catalog_197(
    doc: Mapping[str, Any],
    *,
    allow_draft: bool = False,
) -> dict[str, Any]:
    """Exécute l'audit structurel complet (M1..M4 + I01..I07 + Q01..Q02) sur les 197 assises."""
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

    # 0. Les 4 Murs Porteurs Physiques (M1 à M4)
    m1_violations = _check_m1_temps_bataille(specs)
    m2_violations = _check_m2_conservation_thermique(specs)
    m3_violations, m3_icon_jumpers = _check_m3_integrite_plateau_et_icones(specs)
    m4_violations = _check_m4_autonomie_plancher_solo(specs)
    errors.extend(m1_violations)
    errors.extend(m2_violations)
    errors.extend(m3_violations)
    errors.extend(m4_violations)

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

    # 2. I01 — Exclusivité stricte Insectes + clôture plancher / synergies sur les 197 assises
    insect_violations: list[str] = []
    closure_violations: list[str] = []
    synergy_coverage: list[dict[str, Any]] = []
    twin_synergies: list[dict[str, str]] = []

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

        # 2a. Plancher bloquant (`entrees_plancher`) : disponible sur 64/64 assises (renforcé par M4 en solo)
        for req_state in sp.entrees_plancher:
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
                    f"{sid} ({sp.alias_oriente}): entrée plancher {req_state!r} absente sur "
                    f"{len(missing_assises)}/64 assises (ex. {missing_assises[:3]})"
                )

        # 2b. Synergies optionnelles (`entrees_synergie`, OU / Si… / Face 2) :
        #     doivent être atteignables sur ≥ 1 assise (0 synergie orpheline) + suivi couverture /64
        for syn_state in sp.entrees_synergie:
            covered_count = 0
            for assise, seated in assises_tiles:
                if sid not in seated:
                    continue
                avail_s: set[str] = set(SOCLE_STATES)
                for p in assise.peuples:
                    avail_s.update(PEUPLE_NATIVE_STATES[p])
                for other_sid in seated:
                    other_sp = specs.get(other_sid)
                    if other_sp is not None:
                        avail_s.update(other_sp.sorties)
                if syn_state in avail_s:
                    covered_count += 1
            synergy_coverage.append(
                {
                    "tuile": sid,
                    "alias": sp.alias_oriente,
                    "etat": syn_state,
                    "assises_couvertes": covered_count,
                    "assises_totales": 64,
                    "via_jumelle": syn_state not in local_without_twin and syn_state in twin_outputs,
                }
            )
            if covered_count == 0:
                closure_violations.append(
                    f"{sid} ({sp.alias_oriente}): synergie optionnelle {syn_state!r} "
                    f"inatteignable (0/64 assises — aucun producteur dans le panel)"
                )
            elif syn_state not in local_without_twin and syn_state in twin_outputs:
                twin_synergies.append(
                    {
                        "tuile": sid,
                        "alias": sp.alias_oriente,
                        "etat": syn_state,
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
        out1_to_in2 = sorted(set(s1.sorties) & set(s2.entrees_plancher))
        out2_to_in1 = sorted(set(s2.sorties) & set(s1.entrees_plancher))
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

    meta_raw = doc.get("_meta")
    panel_id = str(meta_raw.get("panel_id", "")) if isinstance(meta_raw, Mapping) else ""
    verdict = "OK" if not errors else "ECHEC"

    return {
        "schema_source": version_tag,
        "panel_id": panel_id or None,
        "verdict_global": verdict,
        "c02_word_count_purged": True,
        "murs_porteurs_actifs": list(MURS_PORTEURS_V6_3),
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
        "M1_TEMPS_BATAILLE": {
            "verdict": "OK" if not m1_violations else "ECHEC",
            "violations": m1_violations,
        },
        "M2_CONSERVATION_THERMIQUE": {
            "verdict": "OK" if not m2_violations else "ECHEC",
            "violations": m2_violations,
        },
        "M3_INTEGRITE_PLATEAU_ET_ICONES": {
            "verdict": "OK" if not m3_violations else "ECHEC",
            "gardiens_saut_icone": m3_icon_jumpers,
            "violations": m3_violations,
        },
        "M4_AUTONOMIE_PLANCHER_SOLO": {
            "verdict": "OK" if not m4_violations else "ECHEC",
            "violations": m4_violations,
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
            "couverture_synergies_optionnelles": synergy_coverage,
            "synergies_jumelle_lisiere": twin_synergies,
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


def audit_panels_directory(
    panels_dir: Path,
    *,
    allow_draft: bool = False,
) -> dict[str, Any]:
    """Audite et compare en parallèle tous les fichiers `*.json` présents dans `panels_dir`."""
    if not panels_dir.is_dir():
        raise FileNotFoundError(f"Répertoire de panels introuvable : {panels_dir}")

    panel_files = sorted(
        p
        for p in panels_dir.glob("*.json")
        if p.is_file() and not p.name.startswith("author_workspace")
    )
    summaries: list[dict[str, Any]] = []
    reports: dict[str, dict[str, Any]] = {}

    for pfile in panel_files:
        doc = json.loads(pfile.read_text(encoding="utf-8"))
        rep = audit_tiles_catalog_197(doc, allow_draft=allow_draft)
        label = rep.get("panel_id") or pfile.stem
        reports[pfile.name] = rep
        summaries.append(
            {
                "file": pfile.name,
                "panel_id": label,
                "verdict": rep["verdict_global"],
                "total_errors": len(rep["errors"]),
                "M1": len(rep["M1_TEMPS_BATAILLE"]["violations"]),
                "M2": len(rep["M2_CONSERVATION_THERMIQUE"]["violations"]),
                "M3": len(rep["M3_INTEGRITE_PLATEAU_ET_ICONES"]["violations"]),
                "M4": len(rep["M4_AUTONOMIE_PLANCHER_SOLO"]["violations"]),
                "I01_I06": (
                    len(rep["I01_cloture_elargie_197"]["insect_violations"])
                    + len(rep["I01_cloture_elargie_197"]["closure_violations"])
                    + len(rep["I02_autonomie_A0"]["violations"])
                    + len(rep["I03_divergence_lisiere"]["violations"])
                    + (0 if rep["I04_couverture_eveil"]["verdict"] == "OK" else 1)
                    + (0 if rep["I05_couverture_sommeil"]["verdict"] == "OK" else 1)
                    + (0 if rep["I06_enracinement"]["verdict"] == "OK" else 1)
                ),
                "schema_v63": len(rep["V63_schema_et_casting"]["errors"]),
                "lois": rep["Q01_lois_passives"]["nombre"],
                "twists": rep["Q02_twists_2K3"]["nombre"],
                "eveil": rep["I04_couverture_eveil"]["nombre"],
                "enrac": rep["I06_enracinement"]["nombre"],
                "synergies_optionnelles": len(
                    rep["I01_cloture_elargie_197"]["couverture_synergies_optionnelles"]
                ),
            }
        )

    all_ok = all(s["verdict"] == "OK" for s in summaries) if summaries else True
    return {
        "panels_dir": panels_dir.as_posix(),
        "panels_count": len(panel_files),
        "all_ok": all_ok,
        "c02_word_count_purged": True,
        "comparison": summaries,
        "reports": reports,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit structurel sur les 197 assises + 4 murs porteurs M1..M4 (v6.2 / v6.3 — zéro C02)."
    )
    parser.add_argument(
        "contract_path",
        nargs="?",
        default=str(ROOT / "contracts" / "tiles_canon_v6_2.json"),
        help="Chemin du contrat JSON de tuiles à auditer.",
    )
    parser.add_argument(
        "--panels-dir",
        type=Path,
        default=None,
        help="Audite et compare en parallèle tous les fichiers *.json du répertoire (ex. contracts/panels).",
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

    if args.panels_dir is not None:
        batch = audit_panels_directory(args.panels_dir, allow_draft=args.allow_draft)
        if args.json:
            print(json.dumps(batch, indent=2, ensure_ascii=False))
        else:
            if not batch["comparison"]:
                print(f"audit_197.py --panels-dir {args.panels_dir} : aucun fichier *.json présent.")
                return 0
            print(
                f"Comparatif multi-panels ({batch['panels_count']} fichiers dans {args.panels_dir}, C02 purgé=True) :"
            )
            header = f"{'Fichier':<20} {'Verdict':<7} {'Err':>4} {'M1':>3} {'M2':>3} {'M3':>3} {'M4':>3} {'Sch':>4} {'Lois':>4} {'Tw':>3} {'Ev':>3} {'Enr':>3}"
            print(header)
            print("-" * len(header))
            for row in batch["comparison"]:
                print(
                    f"{row['file']:<20} {row['verdict']:<7} {row['total_errors']:>4} "
                    f"{row['M1']:>3} {row['M2']:>3} {row['M3']:>3} {row['M4']:>3} "
                    f"{row['schema_v63']:>4} {row['lois']:>4} {row['twists']:>3} "
                    f"{row['eveil']:>3} {row['enrac']:>3}"
                )
        return 0 if batch["all_ok"] else 1

    path = Path(args.contract_path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    report = audit_tiles_catalog_197(doc, allow_draft=args.allow_draft)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            f"audit_197.py [{report['schema_source']}] -> {report['verdict_global']} "
            f"(197 assises, C02 purgé={report['c02_word_count_purged']}, "
            f"M1={report['M1_TEMPS_BATAILLE']['verdict']} "
            f"M2={report['M2_CONSERVATION_THERMIQUE']['verdict']} "
            f"M3={report['M3_INTEGRITE_PLATEAU_ET_ICONES']['verdict']} "
            f"M4={report['M4_AUTONOMIE_PLANCHER_SOLO']['verdict']}, "
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
