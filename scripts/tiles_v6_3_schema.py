"""Validation, gabarit initial et adaptateur Studio du contrat bi-composant v6.3.

Source d'autorité : `docs/cadrage_tuiles_v6_3.md` & `contracts/tiles_canon_v6_3.schema.json`.
Invariant `I07` : aucune vérification ni métrique de comptage de mots, de nombre de phrases
ou de nombre de conditions sur les textes de règles (`carte_joueur.texte_regle`).
"""

from __future__ import annotations

import copy
import html
import json
import re
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CONTRACTS_DIR = ROOT / "contracts"
PANELS_DIR = CONTRACTS_DIR / "panels"
V6_3_SCHEMA_PATH = CONTRACTS_DIR / "tiles_canon_v6_3.schema.json"
V6_3_CONTRACT_PATH = CONTRACTS_DIR / "tiles_canon_v6_3.json"

MURS_PORTEURS_V6_3: tuple[str, ...] = (
    "M1_TEMPS_BATAILLE",
    "M2_CONSERVATION_THERMIQUE",
    "M3_INTEGRITE_PLATEAU_ET_ICONES",
    "M4_AUTONOMIE_PLANCHER_SOLO",
)

SLOTS_SPEC_30: tuple[tuple[str, str, str, str, str], ...] = (
    ("G1", "GARDIEN", "M", "R", "M>R"),
    ("G2", "GARDIEN", "R", "M", "R>M"),
    ("G3", "GARDIEN", "M", "O", "M>O"),
    ("G4", "GARDIEN", "O", "M", "O>M"),
    ("G5", "GARDIEN", "R", "O", "R>O"),
    ("G6", "GARDIEN", "O", "R", "O>R"),
    ("G7", "GARDIEN", "M", "H", "M>H"),
    ("G8", "GARDIEN", "M", "E", "M>E"),
    ("G9", "GARDIEN", "R", "H", "R>H"),
    ("G10", "GARDIEN", "R", "E", "R>E"),
    ("G11", "GARDIEN", "O", "H", "O>H"),
    ("G12", "GARDIEN", "O", "E", "O>E"),
    ("G13", "GARDIEN", "M", "I", "M>I"),
    ("G14", "GARDIEN", "R", "I", "R>I"),
    ("G15", "GARDIEN", "O", "I", "O>I"),
    ("R1", "REVE", "H", "E", "H>E"),
    ("R2", "REVE", "E", "H", "E>H"),
    ("R3", "REVE", "H", "M", "H>M"),
    ("R4", "REVE", "H", "R", "H>R"),
    ("R5", "REVE", "H", "O", "H>O"),
    ("R6", "REVE", "H", "I", "H>I"),
    ("R7", "REVE", "E", "M", "E>M"),
    ("R8", "REVE", "E", "R", "E>R"),
    ("R9", "REVE", "E", "O", "E>O"),
    ("R10", "REVE", "E", "I", "E>I"),
    ("M1", "CROISSANCE", "I", "M", "I>M"),
    ("M2", "CROISSANCE", "I", "R", "I>R"),
    ("M3", "CROISSANCE", "I", "O", "I>O"),
    ("M4", "CROISSANCE", "I", "H", "I>H"),
    ("M5", "CROISSANCE", "I", "E", "I>E"),
)

SLOTS_BY_ID: dict[str, tuple[str, str, str, str]] = {
    sid: (fam, orig, vois, alias) for sid, fam, orig, vois, alias in SLOTS_SPEC_30
}

LOCKED_GARDIEN_CASTING_V6_3: dict[str, str] = {
    "G1": "Le Jaguar",
    "G2": "L’Anaconda vert",
    "G3": "L’Atèle",
    "G4": "L’Ara rouge",
    "G5": "L’Iguane vert",
    "G6": "Le Toucan toco",
    "G7": "Le Tapir",
    "G8": "Le Boto",
    "G9": "Le Caïman noir",
    "G10": "La Matamata",
    "G11": "La Harpie féroce",
    "G12": "L’Ibijau",
    "G13": "Le Tamanoir",
    "G14": "Le Téju",
    "G15": "Le Colibri",
}

I_LISIERE_SLOTS: frozenset[str] = frozenset(
    {"G13", "G14", "G15", "R6", "R10", "M1", "M2", "M3", "M4", "M5"}
)
A0_AUTONOMOUS_SLOTS: frozenset[str] = frozenset({"R1", "R2", "R6", "R10", "M4", "M5"})

VALID_ICONES_GARDIEN: frozenset[str] = frozenset(
    {
        "ICONE_PARADE",
        "ICONE_PIEGEAGE",
        "ICONE_SABOTAGE",
        "ICONE_REVE",
        "ICONE_INSECTE",
        "ICONE_RESONANCE",
    }
)
VALID_ROLES_PORTES: frozenset[str] = frozenset(
    {
        "CATALYSEUR_EVEIL",
        "LEVIER_REVE",
        "ENRACINEMENT",
        "LOI_PASSIVE",
        "AUTONOMIE_A0",
        "TWIST_2K3",
    }
)
VALID_PAIEMENTS: frozenset[str] = frozenset({"P_ARBRE", "P_PARI", "P_RANG", "P_SOUCHE"})
VALID_NATURES: frozenset[str] = frozenset({"ACTION", "LOI_PASSIVE"})
VALID_CYCLES: frozenset[str] = frozenset(
    {"DOUBLE_FACE_UPGRADE", "SIMPLE_CONTINU", "PASSIF_CONTINU"}
)
VALID_ENGINE_SYNC_STATUSES: frozenset[str] = frozenset(
    {"DRAFT_V6_3", "DESIGNED_V6_3", "REFINED_V6_3", "ACTIVE_VERIFIED"}
)
VALID_STATUTS_CONCEPTION: frozenset[str] = frozenset(
    {"A_CONCEVOIR", "PASSE_1_CREATIF", "PASSE_2_AFFINE", "VALIDE_V6_3"}
)

_FORBIDDEN_GARDIEN_ORGAN_GESTURE_RE = re.compile(
    r"(?i)^\s*(?:le|la|l['’])\s+(?:bec|coup\s+de|bond|langue|piqu[ée]|chant|étreinte|"
    r"affût|guet|sentier|terrier|voltige|cri|mirage|va-et-vient|griffe|serre|aile|queue|croc)\b"
)
_SENTENCE_PUNCT_RE = re.compile(r"[.!?]")
_PIC_CODE_RE = re.compile(r"^PIC_[A-Z0-9_]+$")
_TEMOIN_ID_RE = re.compile(r"^(G([1-9]|1[0-5])|R([1-9]|10)|M[1-5])_T[1-3]$")

DEFAULT_REFERENTIEL_PICTOGRAMMES: dict[str, dict[str, str]] = {
    "PIC_ARBRE": {
        "code": "PIC_ARBRE",
        "categorie": "FORET",
        "libelle": "Arbre debout",
        "symbole": "🌳",
    },
    "PIC_SOUCHE": {
        "code": "PIC_SOUCHE",
        "categorie": "FORET",
        "libelle": "Souche (retournable en Arbre)",
        "symbole": "🪵",
    },
    "PIC_ROUTE": {
        "code": "PIC_ROUTE",
        "categorie": "FORET",
        "libelle": "Route forestière",
        "symbole": "🛣️",
    },
    "PIC_ENRACINEMENT": {
        "code": "PIC_ENRACINEMENT",
        "categorie": "FORET",
        "libelle": "Enracinement volontaire",
        "symbole": "🌱",
    },
    "PIC_DEFENSEUR": {
        "code": "PIC_DEFENSEUR",
        "categorie": "DEFENSE",
        "libelle": "Défenseur",
        "symbole": "🛡️",
    },
    "PIC_DEFENSEUR_ATTENTE": {
        "code": "PIC_DEFENSEUR_ATTENTE",
        "categorie": "DEFENSE",
        "libelle": "Défenseur en attente (bâtisseur / rive / Rêve)",
        "symbole": "♻️",
    },
    "PIC_PIEGE": {
        "code": "PIC_PIEGE",
        "categorie": "DEFENSE",
        "libelle": "Piège autonome",
        "symbole": "🪤",
    },
    "PIC_CROC": {
        "code": "PIC_CROC",
        "categorie": "ACCESSOIRES",
        "libelle": "Croc Reptile (réutilisable)",
        "symbole": "🦷",
    },
    "PIC_SABOTAGE": {
        "code": "PIC_SABOTAGE",
        "categorie": "SAC",
        "libelle": "Jeton Sabotage (sac opaque)",
        "symbole": "💥",
    },
    "PIC_ECAILLE": {
        "code": "PIC_ECAILLE",
        "categorie": "ACCESSOIRES",
        "libelle": "Jeton Sabotage Écaille (Reptiles)",
        "symbole": "🦎",
    },
    "PIC_DES_PARAVENT": {
        "code": "PIC_DES_PARAVENT",
        "categorie": "SAC",
        "libelle": "Dés lancés sous paravent",
        "symbole": "🎲",
    },
    "PIC_ROUGE": {
        "code": "PIC_ROUGE",
        "categorie": "MACHINES",
        "libelle": "Jeton Puissance Rouge (+1)",
        "symbole": "🔴",
    },
    "PIC_BLEU": {
        "code": "PIC_BLEU",
        "categorie": "MACHINES",
        "libelle": "Jeton Surchauffe Bleu (−1 tous modes)",
        "symbole": "🔵",
    },
    "PIC_RECUL": {
        "code": "PIC_RECUL",
        "categorie": "MACHINES",
        "libelle": "Recul de machine (−1 parcelle)",
        "symbole": "⏪",
    },
    "PIC_CALE": {
        "code": "PIC_CALE",
        "categorie": "ACCESSOIRES",
        "libelle": "Cale sous machine mobile (Reptiles)",
        "symbole": "🧱",
    },
    "PIC_ALTERATION": {
        "code": "PIC_ALTERATION",
        "categorie": "ACCESSOIRES",
        "libelle": "Jeton Altération (Entités)",
        "symbole": "🌀",
    },
    "PIC_RANG_MACHINE": {
        "code": "PIC_RANG_MACHINE",
        "categorie": "PISTE_TACTIQUES",
        "libelle": "Rang de machine sur la Réglette 1–6",
        "symbole": "🔢",
    },
    "PIC_REVE": {
        "code": "PIC_REVE",
        "categorie": "PISTE_TACTIQUES",
        "libelle": "Tuile Rêve sur la Réglette 1–6",
        "symbole": "🌙",
    },
    "PIC_AVANCEE_REVE": {
        "code": "PIC_AVANCEE_REVE",
        "categorie": "PISTE_TACTIQUES",
        "libelle": "Déplacement / avancée de Rêve",
        "symbole": "⬅️",
    },
    "PIC_ANNULATION": {
        "code": "PIC_ANNULATION",
        "categorie": "PISTE_TACTIQUES",
        "libelle": "Machine annulée (jeton incliné 90°)",
        "symbole": "🚫",
    },
    "PIC_PARI_ENCOCHE": {
        "code": "PIC_PARI_ENCOCHE",
        "categorie": "PISTE_GARDIENS",
        "libelle": "Encoche / sécurisation de pari Gardien",
        "symbole": "⭐",
    },
    "PIC_RESONANCE": {
        "code": "PIC_RESONANCE",
        "categorie": "PISTE_GARDIENS",
        "libelle": "Icône Résonance / cascade de Gardiens",
        "symbole": "🔔",
    },
    "PIC_TAMBOUR": {
        "code": "PIC_TAMBOUR",
        "categorie": "ACCESSOIRES",
        "libelle": "Chamane Tambour (Humains)",
        "symbole": "🥁",
    },
    "PIC_CHANT": {
        "code": "PIC_CHANT",
        "categorie": "ACCESSOIRES",
        "libelle": "Chamane Chant (Humains)",
        "symbole": "🎶",
    },
    "PIC_DUEL": {
        "code": "PIC_DUEL",
        "categorie": "ACCESSOIRES",
        "libelle": "Jeton Duel — Défi / Territoire tenu (Mammifères)",
        "symbole": "⚔️",
    },
    "PIC_PLUME": {
        "code": "PIC_PLUME",
        "categorie": "ACCESSOIRES",
        "libelle": "Plume de Vigie — Chaud / Calme (Oiseaux)",
        "symbole": "🪶",
    },
    "PIC_PERCHOIR": {
        "code": "PIC_PERCHOIR",
        "categorie": "ACCESSOIRES",
        "libelle": "Perchoir de Vigie & Dé d’Envol (Oiseaux)",
        "symbole": "🦅",
    },
    "PIC_INSECTE": {
        "code": "PIC_INSECTE",
        "categorie": "ESSAIM",
        "libelle": "Jeton Insecte (exclusif lisières de I)",
        "symbole": "🐜",
    },
    "PIC_NID": {
        "code": "PIC_NID",
        "categorie": "ESSAIM",
        "libelle": "Nid de l’Essaim (exclusif lisières de I)",
        "symbole": "🪹",
    },
    "PIC_MIGRATION": {
        "code": "PIC_MIGRATION",
        "categorie": "ESSAIM",
        "libelle": "Migration / phorésie de l’Essaim",
        "symbole": "➡️",
    },
    "PIC_LOI_PASSIVE": {
        "code": "PIC_LOI_PASSIVE",
        "categorie": "ACTION",
        "libelle": "Loi passive permanente",
        "symbole": "⚖️",
    },
    "PIC_TWIST": {
        "code": "PIC_TWIST",
        "categorie": "ACTION",
        "libelle": "Brique-Twist 2K3",
        "symbole": "⚡",
    },
}


def _norm_apostrophe(text: str) -> str:
    return text.strip().replace("'", "’")


def is_v6_3_tiles_contract(doc: Mapping[str, Any]) -> bool:
    """Retourne True si `doc` suit le schéma bi-composant v6.3."""
    meta = doc.get("_meta")
    if isinstance(meta, Mapping) and str(meta.get("schema_version", "")).startswith("6.3."):
        return True
    tuiles = doc.get("tuiles_ciblees")
    if isinstance(tuiles, Mapping) and tuiles:
        first = next(iter(tuiles.values()))
        if isinstance(first, Mapping) and "tuile_plateau" in first and "carte_joueur" in first:
            return True
    return False


def validate_tiles_canon_v6_3(
    doc: Mapping[str, Any],
    *,
    strict: bool = False,
) -> list[str]:
    """Valide un contrat `tiles_canon_v6_3.json` contre les règles du cadrage `v6.3`.

    - `strict=False` : valide la structure complète bi-composant, les 30 emplacements,
      le casting verrouillé des 15 Gardiens, la purge C02 (zéro `mots_par_face`/`C02_textes`),
      la validité des pictogrammes et l'hygiène Mini-Tuile, tout en autorisant les champs
      textuels vides pour les tuiles en `statut_conception == "A_CONCEVOIR"`.
    - `strict=True` : exige en outre que les 30 tuiles soient rédigées (2..4 pictogrammes,
      mots-clés plateau, titre/entité/brief/pitch/texte_regle/décision, 1..3 témoins,
      heuristique bot, Face 2 autonome sur les 15 Gardiens). Aucun plafond de mots,
      de phrases ou de conditions n'est jamais appliqué (`I07`).
    """
    errors: list[str] = []

    required_root = (
        "_meta",
        "referentiel_pictogrammes",
        "casting_gardiens_verrouille",
        "carte_des_roles",
        "rapport_audit_197",
        "tuiles_ciblees",
    )
    for key in required_root:
        if key not in doc:
            errors.append(f"Racine v6.3 : clé obligatoire manquante {key!r}")

    meta = doc.get("_meta")
    if isinstance(meta, Mapping):
        if not str(meta.get("schema_version", "")).startswith("6.3."):
            errors.append(f"_meta.schema_version doit commencer par '6.3.' (obtenu {meta.get('schema_version')!r})")
        if meta.get("socle_verrouille") != "6.2.0":
            errors.append(f"_meta.socle_verrouille doit valoir '6.2.0' (obtenu {meta.get('socle_verrouille')!r})")
        if meta.get("cadrage_source") != "docs/cadrage_tuiles_v6_3.md":
            errors.append("_meta.cadrage_source doit référencer 'docs/cadrage_tuiles_v6_3.md'")
        if meta.get("slots_count") != 30:
            errors.append(f"_meta.slots_count doit valoir 30 (obtenu {meta.get('slots_count')!r})")
        if meta.get("c02_supprime") is not True:
            errors.append("_meta.c02_supprime doit valoir true (invariant I07)")
    else:
        errors.append("_meta doit être un objet JSON")

    audit_rep = doc.get("rapport_audit_197")
    if isinstance(audit_rep, Mapping):
        if "C02_textes" in audit_rep:
            errors.append("rapport_audit_197 ne doit jamais contenir 'C02_textes' (I07)")
        if audit_rep.get("c02_word_count_purged") is not True:
            errors.append("rapport_audit_197.c02_word_count_purged doit valoir true")

    ref_pics_raw = doc.get("referentiel_pictogrammes")
    valid_pics: set[str] = set()
    if isinstance(ref_pics_raw, Mapping) and ref_pics_raw:
        for pcode, pentry in ref_pics_raw.items():
            if not _PIC_CODE_RE.match(str(pcode)):
                errors.append(f"referentiel_pictogrammes: code invalide {pcode!r}")
                continue
            if not isinstance(pentry, Mapping) or pentry.get("code") != pcode:
                errors.append(f"referentiel_pictogrammes.{pcode}: entrée invalide ou code discordant")
                continue
            valid_pics.add(str(pcode))
    else:
        errors.append("referentiel_pictogrammes doit être un objet non vide")

    casting = doc.get("casting_gardiens_verrouille")
    if isinstance(casting, Mapping):
        for gid, expected_animal in LOCKED_GARDIEN_CASTING_V6_3.items():
            c_entry = casting.get(gid)
            if not isinstance(c_entry, Mapping):
                errors.append(f"casting_gardiens_verrouille.{gid}: manquant")
                continue
            if _norm_apostrophe(str(c_entry.get("nom_animal", ""))) != _norm_apostrophe(expected_animal):
                errors.append(
                    f"casting_gardiens_verrouille.{gid}: attendu {expected_animal!r}, "
                    f"obtenu {c_entry.get('nom_animal')!r}"
                )
    else:
        errors.append("casting_gardiens_verrouille doit être un objet JSON")

    tuiles = doc.get("tuiles_ciblees")
    if not isinstance(tuiles, Mapping):
        errors.append("tuiles_ciblees doit être un objet JSON")
        return errors

    expected_ids = set(SLOTS_BY_ID.keys())
    actual_ids = set(tuiles.keys())
    if actual_ids != expected_ids:
        errors.append(
            f"tuiles_ciblees : emplacements invalides "
            f"(manquants={sorted(expected_ids - actual_ids)}, en trop={sorted(actual_ids - expected_ids)})"
        )

    for sid, (exp_fam, exp_orig, exp_vois, exp_alias) in SLOTS_BY_ID.items():
        tile = tuiles.get(sid)
        if not isinstance(tile, Mapping):
            continue
        lbl = f"tuiles_ciblees.{sid}"

        # Interdiction stricte de tout vestige C02
        if "mots_par_face" in tile:
            errors.append(f"{lbl}: champ C02 interdit 'mots_par_face'")

        # 1. Identité & Rôle
        if tile.get("id") != sid:
            errors.append(f"{lbl}: id discordant ({tile.get('id')!r} != {sid!r})")
        if tile.get("famille") != exp_fam:
            errors.append(f"{lbl}: famille attendue {exp_fam!r}, obtenue {tile.get('famille')!r}")
        if tile.get("origine") != exp_orig:
            errors.append(f"{lbl}: origine attendue {exp_orig!r}, obtenue {tile.get('origine')!r}")
        if tile.get("voisin") != exp_vois:
            errors.append(f"{lbl}: voisin attendu {exp_vois!r}, obtenu {tile.get('voisin')!r}")
        if tile.get("alias_oriente") != exp_alias:
            errors.append(
                f"{lbl}: alias_oriente attendu {exp_alias!r}, obtenu {tile.get('alias_oriente')!r}"
            )
        if list(tile.get("couple") or []) != [exp_orig, exp_vois]:
            errors.append(f"{lbl}: couple attendu {[exp_orig, exp_vois]!r}, obtenu {tile.get('couple')!r}")

        cycle = tile.get("cycle")
        if cycle not in VALID_CYCLES:
            errors.append(f"{lbl}: cycle invalide {cycle!r}")
        elif exp_fam == "GARDIEN" and cycle != "DOUBLE_FACE_UPGRADE":
            errors.append(f"{lbl}: un Gardien doit avoir cycle='DOUBLE_FACE_UPGRADE'")

        cablage = tile.get("cablage")
        if exp_fam == "GARDIEN":
            if not isinstance(cablage, list) or sorted(cablage) != [1, 2, 3, 4, 5, 6]:
                errors.append(f"{lbl}: un Gardien doit déclarer cablage=[1,2,3,4,5,6]")
        elif cablage is not None:
            errors.append(f"{lbl}: cablage doit être null hors famille GARDIEN")

        nature = tile.get("nature")
        if nature not in VALID_NATURES:
            errors.append(f"{lbl}: nature invalide {nature!r} (attendu ACTION ou LOI_PASSIVE)")

        roles = tile.get("roles_portes")
        if not isinstance(roles, list):
            errors.append(f"{lbl}: roles_portes doit être une liste")
            roles = []
        else:
            for r in roles:
                if r not in VALID_ROLES_PORTES:
                    errors.append(f"{lbl}: rôle inconnu {r!r}")
            if sid in A0_AUTONOMOUS_SLOTS and "AUTONOMIE_A0" not in roles:
                errors.append(f"{lbl}: tuile A=0 doit porter le rôle 'AUTONOMIE_A0'")
            if nature == "LOI_PASSIVE" and "LOI_PASSIVE" not in roles:
                errors.append(f"{lbl}: nature='LOI_PASSIVE' requiert 'LOI_PASSIVE' dans roles_portes")
            if tile.get("est_twist") is True and "TWIST_2K3" not in roles:
                errors.append(f"{lbl}: est_twist=true requiert 'TWIST_2K3' dans roles_portes")
            if tile.get("est_twist") is False and "TWIST_2K3" in roles:
                errors.append(f"{lbl}: 'TWIST_2K3' dans roles_portes incohérent avec est_twist=false")

        if not isinstance(tile.get("est_twist"), bool):
            errors.append(f"{lbl}: est_twist doit être un booléen")

        for list_field in ("entrees", "sorties", "paiement", "declencheurs_amorces", "tags"):
            if not isinstance(tile.get(list_field), list):
                errors.append(f"{lbl}: {list_field} doit être une liste")

        for opt_list in ("entrees_plancher", "entrees_synergie"):
            if opt_list in tile and not isinstance(tile.get(opt_list), list):
                errors.append(f"{lbl}: {opt_list} doit être une liste")
        if isinstance(tile.get("entrees_plancher"), list) and isinstance(
            tile.get("entrees_synergie"), list
        ):
            overlap = sorted(
                {str(x).upper() for x in tile["entrees_plancher"]}
                & {str(x).upper() for x in tile["entrees_synergie"]}
            )
            if overlap:
                errors.append(
                    f"{lbl}: entrees_plancher et entrees_synergie doivent être disjoints "
                    f"(doublons={overlap})"
                )

        for pay in tile.get("paiement") or []:
            if pay not in VALID_PAIEMENTS:
                errors.append(f"{lbl}: paiement invalide {pay!r}")

        for trig in tile.get("declencheurs_amorces") or []:
            if trig not in VALID_ICONES_GARDIEN:
                errors.append(f"{lbl}: declencheur inconnu {trig!r}")

        sync_st = tile.get("engine_sync_status")
        if sync_st not in VALID_ENGINE_SYNC_STATUSES:
            errors.append(f"{lbl}: engine_sync_status invalide {sync_st!r}")

        conception_st = tile.get("statut_conception")
        if conception_st not in VALID_STATUTS_CONCEPTION:
            errors.append(f"{lbl}: statut_conception invalide {conception_st!r}")

        is_authored = strict or conception_st != "A_CONCEVOIR"

        # 2. Mini-Tuile Plateau (`tuile_plateau`)
        tp = tile.get("tuile_plateau")
        if not isinstance(tp, Mapping):
            errors.append(f"{lbl}: bloc 'tuile_plateau' manquant ou invalide")
        else:
            nom_court = str(tp.get("nom_court", "")).strip()
            if exp_fam == "GARDIEN":
                exp_animal = LOCKED_GARDIEN_CASTING_V6_3[sid]
                if _norm_apostrophe(nom_court) != _norm_apostrophe(exp_animal):
                    errors.append(
                        f"{lbl}.tuile_plateau.nom_court: casting Gardien verrouillé "
                        f"attendu {exp_animal!r}, obtenu {nom_court!r}"
                    )
                if _FORBIDDEN_GARDIEN_ORGAN_GESTURE_RE.match(nom_court):
                    errors.append(
                        f"{lbl}.tuile_plateau.nom_court: titre organe/geste interdit ({nom_court!r})"
                    )
            elif is_authored and not nom_court:
                errors.append(f"{lbl}.tuile_plateau.nom_court requis")

            ic_cons = tp.get("icone_conseillee")
            if ic_cons is not None and ic_cons not in VALID_ICONES_GARDIEN:
                errors.append(f"{lbl}.tuile_plateau.icone_conseillee invalide {ic_cons!r}")
            if exp_fam != "GARDIEN" and ic_cons is not None:
                errors.append(f"{lbl}.tuile_plateau.icone_conseillee doit être null hors GARDIEN")
            if exp_fam == "GARDIEN" and is_authored and ic_cons is None:
                errors.append(f"{lbl}.tuile_plateau.icone_conseillee requis sur Gardien rédigé")

            pics = tp.get("pictogrammes")
            if not isinstance(pics, list):
                errors.append(f"{lbl}.tuile_plateau.pictogrammes doit être une liste")
            else:
                if len(pics) > 4:
                    errors.append(f"{lbl}.tuile_plateau.pictogrammes: max 4 pictogrammes (obtenu {len(pics)})")
                if is_authored and len(pics) < 2:
                    errors.append(
                        f"{lbl}.tuile_plateau.pictogrammes: 2 à 4 pictogrammes requis (obtenu {len(pics)})"
                    )
                for p in pics:
                    if str(p) not in valid_pics:
                        errors.append(f"{lbl}.tuile_plateau.pictogrammes: code non déclaré {p!r}")

            mcp = tp.get("mots_cles_plateau")
            if not isinstance(mcp, Mapping):
                errors.append(f"{lbl}.tuile_plateau.mots_cles_plateau manquant")
            else:
                for mkey in ("face_1", "face_2", "enracine"):
                    if mkey not in mcp:
                        errors.append(f"{lbl}.tuile_plateau.mots_cles_plateau.{mkey} manquant")
                        continue
                    mval = mcp.get(mkey)
                    # Mini-Tuile : zéro phrase rédigée (pas de ponctuation terminale de phrase)
                    if isinstance(mval, str) and mval.strip() and _SENTENCE_PUNCT_RE.search(mval):
                        errors.append(
                            f"{lbl}.tuile_plateau.mots_cles_plateau.{mkey}: "
                            f"zéro phrase rédigée sur la Mini-Tuile ({mval!r})"
                        )
                if is_authored:
                    if not str(mcp.get("face_1") or "").strip():
                        errors.append(f"{lbl}.tuile_plateau.mots_cles_plateau.face_1 requis")
                    if exp_fam == "GARDIEN" and not str(mcp.get("face_2") or "").strip():
                        errors.append(f"{lbl}.tuile_plateau.mots_cles_plateau.face_2 requis sur Gardien")

            resume_p = tp.get("resume_plateau")
            if isinstance(resume_p, str) and resume_p.strip() and _SENTENCE_PUNCT_RE.search(resume_p):
                errors.append(
                    f"{lbl}.tuile_plateau.resume_plateau: zéro phrase rédigée sur la Mini-Tuile ({resume_p!r})"
                )

        # 3. Grande Carte Joueur (`carte_joueur`) — ZÉRO limite de mots / phrases / conditions (I07)
        cj = tile.get("carte_joueur")
        if not isinstance(cj, Mapping):
            errors.append(f"{lbl}: bloc 'carte_joueur' manquant ou invalide")
        else:
            if "mots_par_face" in cj:
                errors.append(f"{lbl}.carte_joueur: champ C02 interdit 'mots_par_face'")
            titre = str(cj.get("titre_complet", "")).strip()
            if exp_fam == "GARDIEN":
                exp_animal = LOCKED_GARDIEN_CASTING_V6_3[sid]
                if _FORBIDDEN_GARDIEN_ORGAN_GESTURE_RE.match(titre):
                    errors.append(
                        f"{lbl}.carte_joueur.titre_complet: titre organe/geste interdit ({titre!r})"
                    )
                if _norm_apostrophe(exp_animal).lower() not in _norm_apostrophe(titre).lower():
                    errors.append(
                        f"{lbl}.carte_joueur.titre_complet doit célébrer l'animal {exp_animal!r} "
                        f"(obtenu {titre!r})"
                    )

            tr = cj.get("texte_regle")
            if not isinstance(tr, Mapping):
                errors.append(f"{lbl}.carte_joueur.texte_regle manquant")
            else:
                for tkey in ("face_1", "face_2", "enracine"):
                    if tkey not in tr:
                        errors.append(f"{lbl}.carte_joueur.texte_regle.{tkey} manquant")
                if is_authored:
                    if not str(tr.get("face_1") or "").strip():
                        errors.append(f"{lbl}.carte_joueur.texte_regle.face_1 requis")
                    if exp_fam == "GARDIEN" and not str(tr.get("face_2") or "").strip():
                        errors.append(
                            f"{lbl}.carte_joueur.texte_regle.face_2 requis (Face 2 autonome sur Gardien)"
                        )
                    if exp_fam != "GARDIEN" and tr.get("face_2") is not None:
                        errors.append(
                            f"{lbl}.carte_joueur.texte_regle.face_2 doit être null hors GARDIEN"
                        )

            dr = cj.get("decision_et_renoncement")
            if not isinstance(dr, Mapping) or "choix" not in dr or "renoncement" not in dr:
                errors.append(f"{lbl}.carte_joueur.decision_et_renoncement invalide")
            elif is_authored:
                if not str(dr.get("choix") or "").strip():
                    errors.append(f"{lbl}.carte_joueur.decision_et_renoncement.choix requis")
                if not str(dr.get("renoncement") or "").strip():
                    errors.append(f"{lbl}.carte_joueur.decision_et_renoncement.renoncement requis")

            if is_authored:
                for req_cj in ("titre_complet", "entite_illustree", "brief_illustration", "pitch_ambiance"):
                    if not str(cj.get(req_cj) or "").strip():
                        errors.append(f"{lbl}.carte_joueur.{req_cj} requis")

        # 4. Exécution & Preuve
        temoins = tile.get("temoins")
        if not isinstance(temoins, list):
            errors.append(f"{lbl}.temoins doit être une liste")
        else:
            if len(temoins) > 3:
                errors.append(f"{lbl}.temoins: max 3 témoins (obtenu {len(temoins)})")
            if is_authored and len(temoins) < 1:
                errors.append(f"{lbl}.temoins: 1 à 3 témoins requis")
            for idx_t, t_obj in enumerate(temoins):
                if not isinstance(t_obj, Mapping):
                    errors.append(f"{lbl}.temoins[{idx_t}] doit être un objet")
                    continue
                tid_str = str(t_obj.get("id", ""))
                if not _TEMOIN_ID_RE.match(tid_str) or not tid_str.startswith(f"{sid}_T"):
                    errors.append(f"{lbl}.temoins[{idx_t}].id invalide ({tid_str!r})")
                if not str(t_obj.get("resume", "")).strip():
                    errors.append(f"{lbl}.temoins[{idx_t}].resume vide")
        if is_authored and not str(tile.get("heuristique_bot") or "").strip():
            errors.append(f"{lbl}.heuristique_bot requis")

    return errors


def build_v6_3_scaffold(*, genere_le: str = "2026-11-25") -> dict[str, Any]:
    """Construit le squelette propre et valide `contracts/tiles_canon_v6_3.json` pour l'Étape 2."""
    casting_out: dict[str, dict[str, str]] = {}
    tuiles_out: dict[str, dict[str, Any]] = {}

    for sid, fam, orig, vois, alias in SLOTS_SPEC_30:
        is_gardien = fam == "GARDIEN"
        is_a0 = sid in A0_AUTONOMOUS_SLOTS

        if is_gardien:
            animal = LOCKED_GARDIEN_CASTING_V6_3[sid]
            casting_out[sid] = {
                "alias_oriente": alias,
                "nom_animal": animal,
                "origine": orig,
                "voisin": vois,
            }
            nom_court = animal
            titre_complet = animal
            entite_illustree = f"{animal} — animal sauvage entier dans son biotope amazonien"
            fenetre_badge = "ACTIVATION"
            cycle = "DOUBLE_FACE_UPGRADE"
            cablage: list[int] | None = [1, 2, 3, 4, 5, 6]
            face_2_placeholder: str | None = ""
        elif fam == "REVE":
            nom_court = ""
            titre_complet = ""
            entite_illustree = ""
            fenetre_badge = "OUVERTURE"
            cycle = "SIMPLE_CONTINU"
            cablage = None
            face_2_placeholder = None
        else:
            nom_court = ""
            titre_complet = ""
            entite_illustree = ""
            fenetre_badge = "PRODUCTION"
            cycle = "SIMPLE_CONTINU"
            cablage = None
            face_2_placeholder = None

        roles_portes = ["AUTONOMIE_A0"] if is_a0 else []
        tags = ["A0"] if is_a0 else []
        if sid in I_LISIERE_SLOTS:
            tags.append("INSECTES")

        tuiles_out[sid] = {
            "id": sid,
            "alias_oriente": alias,
            "famille": fam,
            "origine": orig,
            "voisin": vois,
            "couple": [orig, vois],
            "cycle": cycle,
            "cablage": cablage,
            "roles_portes": roles_portes,
            "est_twist": False,
            "vecteurs": "",
            "entrees_plancher": [],
            "entrees_synergie": [],
            "entrees": [],
            "sorties": [],
            "paiement": [],
            "nature": "ACTION",
            "declencheurs_amorces": [],
            "double_ouverture": "" if is_gardien else None,
            "tags": tags,
            "tuile_plateau": {
                "nom_court": nom_court,
                "fenetre_badge": fenetre_badge,
                "icone_conseillee": None,
                "pictogrammes": [],
                "mots_cles_plateau": {
                    "face_1": "",
                    "face_2": face_2_placeholder,
                    "enracine": None,
                },
                "resume_plateau": "",
            },
            "carte_joueur": {
                "titre_complet": titre_complet,
                "entite_illustree": entite_illustree,
                "brief_illustration": "",
                "pitch_ambiance": "",
                "texte_regle": {
                    "face_1": "",
                    "face_2": face_2_placeholder,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "",
                    "renoncement": "",
                },
            },
            "temoins": [],
            "heuristique_bot": "",
            "engine_sync_status": "DRAFT_V6_3",
            "statut_conception": "A_CONCEVOIR",
        }

    return {
        "_meta": {
            "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
            "schema_version": "6.3.1-draft",
            "socle_verrouille": "6.2.0",
            "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
            "etape_active": "ETAPE_1_CADRAGE_ET_SCHEMA",
            "statut_global": "SCAFFOLD_PRET_ETAPE_2",
            "genere_le": genere_le,
            "slots_count": 30,
            "c02_supprime": True,
            "panel_id": "canon_v6_3",
            "murs_porteurs_verrouilles": list(MURS_PORTEURS_V6_3),
            "note_retrocompatibilite": (
                "Squelette v6.3.1 (4 murs porteurs M1..M4 + séparation entrees_plancher / "
                "entrees_synergie) : le build Doc Studio actif reste transitoirement sur "
                "contracts/tiles_canon_v6_2.json (archive sanctuarisée) jusqu'aux Étapes 3–5, "
                "tout en disposant déjà de l'adaptateur bi-composant v6.3."
            ),
        },
        "referentiel_pictogrammes": copy.deepcopy(DEFAULT_REFERENTIEL_PICTOGRAMMES),
        "casting_gardiens_verrouille": casting_out,
        "carte_des_roles": {
            "statut": "A_CONCEVOIR_ETAPE_2",
            "roles": {
                "catalyseurs_eveil": [],
                "leviers_reve": [],
                "synergies_enracinement": [],
                "lois_passives": [],
                "autonomie_A0": [
                    f"{sid}={SLOTS_BY_ID[sid][3]}" for sid in ("R1", "R2", "R6", "R10", "M4", "M5")
                ],
                "twists_2K3": [],
            },
        },
        "rapport_audit_197": {
            "verdict_global": "EN_ATTENTE_ETAPE_2 — Squelette v6.3 initialisé ; zéro contrainte C02.",
            "c02_word_count_purged": True,
        },
        "tuiles_ciblees": tuiles_out,
    }


def _render_texte_regle_html(famille: str, nature: str, texte_regle: Mapping[str, Any]) -> str:
    """Projette `carte_joueur.texte_regle` en HTML rétro-compatible pour Doc Studio avant Étape 5."""
    f1 = html.escape(str(texte_regle.get("face_1") or "").strip())
    f2_raw = texte_regle.get("face_2")
    f2 = html.escape(str(f2_raw).strip()) if isinstance(f2_raw, str) and f2_raw.strip() else ""
    enr_raw = texte_regle.get("enracine")
    enr = html.escape(str(enr_raw).strip()) if isinstance(enr_raw, str) and enr_raw.strip() else ""

    parts: list[str] = []
    if famille == "GARDIEN":
        if f1:
            parts.append(f"<strong>Face 1 :</strong> {f1}")
        if f2:
            parts.append(f"<strong>Face 2 :</strong> {f2}")
    else:
        if f1:
            if nature == "LOI_PASSIVE":
                parts.append(f"<strong>Loi passive :</strong> {f1}")
            else:
                parts.append(f1)
    if enr:
        parts.append(f"<strong>Enraciné :</strong> {enr}")
    return "<br>".join(parts)


def project_v6_3_tile_to_studio_compat(tile: Mapping[str, Any]) -> dict[str, Any]:
    """Convertit une entrée bi-composant `v6.3` vers le format slot Studio transitoire (pré-Étape 5).

    Préserve intégralement `tuile_plateau` et `carte_joueur` dans le profil projeté afin que
    la future refonte UX/UI (Étape 5) puisse consommer directement les deux composants sans perte.
    """
    sid = str(tile["id"])
    famille = str(tile["famille"])
    origine = str(tile["origine"])
    voisin = str(tile["voisin"])
    alias = str(tile["alias_oriente"])
    nature = str(tile.get("nature", "ACTION")).upper()
    tp = dict(tile["tuile_plateau"])
    cj = dict(tile["carte_joueur"])
    dr = dict(cj.get("decision_et_renoncement") or {})
    tr = dict(cj.get("texte_regle") or {})
    temoins_list = list(tile.get("temoins") or [])
    first_temoin_txt = (
        str(temoins_list[0].get("resume", ""))
        if temoins_list and isinstance(temoins_list[0], Mapping)
        else ""
    )

    nom_base = str(tp.get("nom_court") or cj.get("titre_complet") or sid)
    titre_complet = str(cj.get("titre_complet") or nom_base)

    profile_a: dict[str, Any] = {
        "nom": titre_complet,
        "cycle": str(tile.get("cycle", "DOUBLE_FACE_UPGRADE" if famille == "GARDIEN" else "SIMPLE_CONTINU")),
        "cablage": copy.deepcopy(tile.get("cablage")),
        "fenetre": str(tp.get("fenetre_badge") or ""),
        "primitive": "BI_COMPOSANT_V6_3",
        "tags": list(tile.get("tags") or []),
        "requires_options": {},
        "texte": _render_texte_regle_html(famille, nature, tr),
        "temoin": first_temoin_txt,
        "alias_oriente": alias,
        "id_profil": f"{alias}·A",
        "alias_profil": f"{sid}-A",
        "animal_ou_theme": str(cj.get("entite_illustree") or nom_base),
        "est_twist_canon0": bool(tile.get("est_twist", False)),
        "est_twist": bool(tile.get("est_twist", False)),
        "role_porte": list(tile.get("roles_portes") or []),
        "roles_portes": list(tile.get("roles_portes") or []),
        "decision_joueur": {
            "choix": str(dr.get("choix", "")),
            "renoncement": str(dr.get("renoncement", "")),
        },
        "entrees_plancher": list(tile.get("entrees_plancher") or []),
        "entrees_synergie": list(tile.get("entrees_synergie") or []),
        "entrees": list(
            dict.fromkeys(
                [
                    *(tile.get("entrees_plancher") or []),
                    *(tile.get("entrees_synergie") or []),
                    *(tile.get("entrees") or []),
                ]
            )
        ),
        "sorties": list(tile.get("sorties") or []),
        "paiement": list(tile.get("paiement") or []),
        "vecteurs": str(tile.get("vecteurs") or ""),
        "nature": "loi_passive" if nature == "LOI_PASSIVE" else "action",
        "declencheurs_amorces": list(tile.get("declencheurs_amorces") or []),
        "double_ouverture": tile.get("double_ouverture"),
        "cablage_recommande": tp.get("icone_conseillee"),
        "heuristique_bot": str(tile.get("heuristique_bot") or ""),
        "temoins": copy.deepcopy(temoins_list),
        "tuile_plateau": copy.deepcopy(tp),
        "carte_joueur": copy.deepcopy(cj),
        "statut_conception": str(tile.get("statut_conception", "A_CONCEVOIR")),
        "engine_sync_status": str(tile.get("engine_sync_status", "DRAFT_V6_3")),
    }

    return {
        "id": sid,
        "famille": famille,
        "couple": [origine, voisin],
        "origine": origine,
        "peuple_origine": origine,
        "nomBase": nom_base,
        "tuile_plateau": copy.deepcopy(tp),
        "carte_joueur": copy.deepcopy(cj),
        "profils": {"A": profile_a},
    }


def adapt_tiles_contract_for_studio(tiles_doc: Mapping[str, Any]) -> dict[str, Any]:
    """Adapte un contrat `v6.2` ou `v6.3` vers le dictionnaire `tuiles_ciblees` attendu par Studio."""
    if not is_v6_3_tiles_contract(tiles_doc):
        return copy.deepcopy(dict(tiles_doc))
    adapted = copy.deepcopy(dict(tiles_doc))
    raw_tiles = tiles_doc.get("tuiles_ciblees") or {}
    adapted["tuiles_ciblees"] = {
        str(sid): project_v6_3_tile_to_studio_compat(tile)
        for sid, tile in raw_tiles.items()
    }
    return adapted


def write_v6_3_scaffold(target_path: Path = V6_3_CONTRACT_PATH) -> dict[str, Any]:
    """Écrit le squelette initialisé `contracts/tiles_canon_v6_3.json` en UTF-8 LF et le valide."""
    scaffold = build_v6_3_scaffold()
    errs = validate_tiles_canon_v6_3(scaffold, strict=False)
    if errs:
        raise RuntimeError("Squelette v6.3 invalide :\n" + "\n".join(errs))
    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(
        json.dumps(scaffold, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return scaffold


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Validation ou génération du contrat bi-composant tiles_canon_v6_3.json."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=str(V6_3_CONTRACT_PATH),
        help="Chemin vers le contrat JSON v6.3 à valider (défaut: contracts/tiles_canon_v6_3.json).",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Active la validation complète (toutes les 30 tuiles rédigées ; zéro plafond C02).",
    )
    parser.add_argument(
        "--init-scaffold",
        action="store_true",
        help="Génère le squelette initialisé v6.3 à l'emplacement cible.",
    )
    args = parser.parse_args()
    target = Path(args.path)

    if args.init_scaffold:
        write_v6_3_scaffold(target)
        print(f"tiles_v6_3_schema.py : squelette généré dans {target.as_posix()} (30 slots, C02 purgé)")
        return 0

    doc = json.loads(target.read_text(encoding="utf-8"))
    errs = validate_tiles_canon_v6_3(doc, strict=args.strict)
    if errs:
        print("ERREURS schéma v6.3 :")
        for e in errs:
            print(f"  - {e}")
        return 1
    mode_lbl = "STRICT" if args.strict else "DRAFT-AWARE"
    print(f"tiles_v6_3_schema.py : OK ({target.as_posix()}, mode={mode_lbl}, 30 slots, I07 sans C02)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
