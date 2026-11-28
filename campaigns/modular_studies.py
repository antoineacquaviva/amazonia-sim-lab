"""Études modulaires par « Tuiles à blanc » (`NEUTRE`), lisières 2×2 et moteurs v6.4.

100 % stdlib PyPy 3.11 / CPython 3.12 (zéro dépendance tierce).
Dérive dynamiquement les regroupements de moteurs (partition disjointe 30/30 et
moteurs fonctionnels avec tuiles-pivots) directement depuis `contracts/tiles_canon_v6_4.json`
(avec repli embarqué vérifié identique par test pour les workers Docker isolés).
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from engine.state import MATRICE_PAIRES

__all__ = (
    "CANONICAL_15_EDGES",
    "CANONICAL_30_TILES",
    "CANONICAL_30_TILES_SET",
    "DISJOINT_MOTOR_DEFS",
    "PIVOT_MOTOR_PREDICATES",
    "ModularVariantSpec",
    "build_all_neutre_tile_profiles",
    "build_tile_profiles_from_active_subset",
    "build_tile_profiles_from_neutral_subset",
    "get_disjoint_motors",
    "get_motor_catalog",
    "get_pivot_motors",
    "get_pivot_tiles",
    "get_role_motors",
    "load_tile_canon_metadata",
    "resolve_modular_study_variants",
    "resolve_slot_selection",
)

CANONICAL_30_TILES: tuple[str, ...] = (
    "G1",
    "G2",
    "G3",
    "G4",
    "G5",
    "G6",
    "G7",
    "G8",
    "G9",
    "G10",
    "G11",
    "G12",
    "G13",
    "G14",
    "G15",
    "R1",
    "R2",
    "R3",
    "R4",
    "R5",
    "R6",
    "R7",
    "R8",
    "R9",
    "R10",
    "M1",
    "M2",
    "M3",
    "M4",
    "M5",
)
CANONICAL_30_TILES_SET: frozenset[str] = frozenset(CANONICAL_30_TILES)

# 15 lisières canoniques (ordre stable conforme à MATRICE_PAIRES)
_ORDERED_EDGE_KEYS: tuple[str, ...] = (
    "M_R",
    "M_O",
    "R_O",
    "M_H",
    "M_E",
    "R_H",
    "R_E",
    "O_H",
    "O_E",
    "M_I",
    "R_I",
    "O_I",
    "H_E",
    "H_I",
    "E_I",
)
CANONICAL_15_EDGES: dict[str, tuple[str, str]] = {
    edge_key: MATRICE_PAIRES[edge_key] for edge_key in _ORDERED_EDGE_KEYS
}

# Repli canonique minimal (identique aux champs utilisés de contracts/tiles_canon_v6_4.json)
# pour l'exécution dans le conteneur worker-pypy qui n'embarque pas `contracts/`.
# La parité stricte avec `contracts/tiles_canon_v6_4.json` est vérifiée par pytest.
_EMBEDDED_TILES_CANON_FALLBACK: dict[str, Any] = {
    "carte_des_roles": {
        "roles": {
            "catalyseurs_eveil": [
                "G1=M>R", "G3=M>O", "G4=O>M", "G5=R>O", "G6=O>R", "G8=M>E",
                "G9=R>H", "G10=R>E", "G11=O>H", "G12=O>E", "G13=M>I", "G14=R>I", "G15=O>I",
            ],
            "leviers_reve": ["G8=M>E", "R1=H>E", "R4=H>R", "R8=E>R", "R9=E>O", "R10=E>I"],
            "synergies_enracinement": ["G7=M>H", "G15=O>I", "R1=H>E", "R2=E>H"],
            "lois_passives": ["R7=E>M", "R8=E>R", "M5=I>E"],
            "autonomie_A0": ["R1=H>E", "R2=E>H", "R6=H>I", "R10=E>I", "M4=I>H", "M5=I>E"],
            "twists_2K3": ["G2=R>M", "G7=M>H", "G12=O>E", "R4=H>R", "R10=E>I", "M3=I>O"],
        }
    },
    "tuiles_ciblees": {
        "G1": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["DUEL", "CROC", "ROUGE"], "sorties": ["CROC_POSTE", "CROC", "TERRITOIRE", "BLEU"]},
        "G2": {"nature": "ACTION", "est_twist": True, "roles_portes": ["TWIST_2K3"], "tags": ["TWIST_2K3"], "entrees": ["RATISSAGE", "DUEL", "TERRITOIRE"], "sorties": ["RATISSAGE_ROMPU", "RECUL", "ANNULATION"]},
        "G3": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["ARBRE", "ROUTE", "DEFENSEUR_REDEPLOYE", "PERCHOIR"], "sorties": ["DEFENSEUR_REDEPLOYE"]},
        "G4": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["GARDIEN", "TERRITOIRE"], "sorties": ["PARI_GLISSE", "ACTIVATION_RELAIS", "DEFI"]},
        "G5": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["PERCHOIR", "BLEU"], "sorties": ["PIEGE", "CROC"]},
        "G6": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["ROUGE", "PERCHOIR", "BLEU"], "sorties": ["BLEU", "ANNULATION_SURCHAUFFE"]},
        "G7": {"nature": "ACTION", "est_twist": True, "roles_portes": ["TWIST_2K3", "ENRACINEMENT"], "tags": ["ENRACINEMENT", "TWIST_2K3"], "entrees": ["ROUTE", "DUEL", "TAMBOUR", "CHANT", "CHAMANE_EN_FORET", "ROUGE"], "sorties": ["BOURBIER_ROUTE", "TERRITOIRE", "BLEU", "RECUL", "ARBRE"]},
        "G8": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL", "LEVIER_REVE"], "tags": ["CATALYSEUR_EVEIL", "LEVIER_REVE"], "entrees": ["POSITION_REVE", "RANG_REVE"], "sorties": ["POSITION_REVE", "ALTERATION", "ANNULATION"]},
        "G9": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["SABOTAGE", "ECAILLE", "TAMBOUR"], "sorties": ["CALE", "RECUL", "ANNULATION"]},
        "G10": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["ECAILLE", "CROC", "RANG_MACHINE", "ALTERATION"], "sorties": ["ECAILLE", "CROC", "ALTERATION"]},
        "G11": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["CATALYSEUR_EVEIL"], "entrees": ["PERCHOIR", "DEFENSEUR_ATTENTE", "RANG_MACHINE", "CHANT", "TAMBOUR", "POSITION_REVE"], "sorties": ["DEFENSEUR_REDEPLOYE", "ANNULATION"]},
        "G12": {"nature": "ACTION", "est_twist": True, "roles_portes": ["CATALYSEUR_EVEIL", "TWIST_2K3"], "tags": ["CATALYSEUR_EVEIL", "TWIST_2K3"], "entrees": ["DES_SOUS_PARAVENT", "RANG_MACHINE", "POSITION_REVE", "SABOTAGE"], "sorties": ["RANG_RELU", "ANNULATION_INDUITE"]},
        "G13": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["INSECTES", "CATALYSEUR_EVEIL"], "entrees": ["INSECTE", "DUEL", "NID"], "sorties": ["RIPOSTE_ESSAIM", "INSECTE", "TERRITOIRE"]},
        "G14": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL"], "tags": ["INSECTES", "CATALYSEUR_EVEIL"], "entrees": ["ECAILLE", "CROC", "NID"], "sorties": ["PONTE", "CROC", "ECAILLE"]},
        "G15": {"nature": "ACTION", "est_twist": False, "roles_portes": ["CATALYSEUR_EVEIL", "ENRACINEMENT"], "tags": ["INSECTES", "CATALYSEUR_EVEIL", "ENRACINEMENT"], "entrees": ["PERCHOIR", "INSECTE", "NID", "GARDIEN"], "sorties": ["INSECTE_TRANSPORTE", "INSECTE", "INSECTE_RANG", "PARI_GLISSE", "ARBRE"]},
        "R1": {"nature": "ACTION", "est_twist": False, "roles_portes": ["AUTONOMIE_A0", "LEVIER_REVE", "ENRACINEMENT"], "tags": ["A0", "LEVIER_REVE", "ENRACINEMENT"], "entrees": ["POSITION_REVE", "RANG_REVE", "TAMBOUR"], "sorties": ["REVE_COMPACTE", "POSITION_REVE", "ANNULATION"]},
        "R2": {"nature": "ACTION", "est_twist": False, "roles_portes": ["AUTONOMIE_A0", "ENRACINEMENT"], "tags": ["A0", "ENRACINEMENT"], "entrees": ["POSITION_REVE", "RANG_MACHINE", "TAMBOUR", "DEFENSEUR_ATTENTE", "ALTERATION"], "sorties": ["ALTERATION", "DEFENSEUR_REDEPLOYE", "ARBRE"]},
        "R3": {"nature": "ACTION", "est_twist": False, "roles_portes": [], "tags": [], "entrees": ["RANG_REVE", "DUEL", "ANNULATION", "TAMBOUR"], "sorties": ["CHAMANE_EN_FORET", "DEFENSEUR_REDEPLOYE", "TERRITOIRE"]},
        "R4": {"nature": "ACTION", "est_twist": True, "roles_portes": ["TWIST_2K3", "LEVIER_REVE"], "tags": ["LEVIER_REVE", "TWIST_2K3"], "entrees": ["POSITION_REVE", "RANG_REVE"], "sorties": ["PISTON_REVES", "POSITION_REVE", "ECAILLE"]},
        "R5": {"nature": "ACTION", "est_twist": False, "roles_portes": [], "tags": [], "entrees": ["PERCHOIR", "RANG_MACHINE", "TAMBOUR", "CHANT", "ROUGE"], "sorties": ["RANG_MACHINE", "BLEU"]},
        "R6": {"nature": "ACTION", "est_twist": False, "roles_portes": ["AUTONOMIE_A0"], "tags": ["A0", "INSECTES"], "entrees": ["INSECTE", "ANNULATION", "INSECTE_RANG", "TAMBOUR", "CHANT"], "sorties": ["ANNULATION_RENFORCEE", "INSECTE_RANG"]},
        "R7": {"nature": "LOI_PASSIVE", "est_twist": False, "roles_portes": ["LOI_PASSIVE"], "tags": ["LOI_PASSIVE"], "entrees": ["RANG_REVE", "POSITION_REVE", "RANG_MACHINE", "DUEL"], "sorties": ["RECUL", "TERRITOIRE", "ALTERATION"]},
        "R8": {"nature": "LOI_PASSIVE", "est_twist": False, "roles_portes": ["LOI_PASSIVE", "LEVIER_REVE"], "tags": ["LEVIER_REVE", "LOI_PASSIVE"], "entrees": ["POSITION_REVE", "ALTERATION", "RANG_MACHINE", "ECAILLE", "ROUGE"], "sorties": ["RANG_REVE", "ALTERATION", "BLEU"]},
        "R9": {"nature": "ACTION", "est_twist": False, "roles_portes": ["LEVIER_REVE"], "tags": ["LEVIER_REVE"], "entrees": ["PERCHOIR", "RANG_REVE", "ALTERATION", "ROUGE"], "sorties": ["POSITION_REVE", "ALTERATION", "BLEU"]},
        "R10": {"nature": "ACTION", "est_twist": True, "roles_portes": ["AUTONOMIE_A0", "TWIST_2K3", "LEVIER_REVE"], "tags": ["A0", "INSECTES", "LEVIER_REVE", "TWIST_2K3"], "entrees": ["POSITION_REVE", "RANG_MACHINE", "NID", "INSECTE", "ROUGE"], "sorties": ["RANG_REVE", "NID_DEPLACE", "ALTERATION", "INSECTE", "BLEU"]},
        "M1": {"nature": "ACTION", "est_twist": False, "roles_portes": [], "tags": ["INSECTES"], "entrees": ["NID", "INSECTE", "DUEL"], "sorties": ["INSECTE_PASSAGER", "TERRITOIRE"]},
        "M2": {"nature": "ACTION", "est_twist": False, "roles_portes": [], "tags": ["INSECTES"], "entrees": ["NID", "INSECTE"], "sorties": ["PARADE_SOLDATS", "ECAILLE", "CROC"]},
        "M3": {"nature": "ACTION", "est_twist": True, "roles_portes": ["TWIST_2K3"], "tags": ["INSECTES", "TWIST_2K3"], "entrees": ["NID", "INSECTE", "PERCHOIR"], "sorties": ["NID_NOMADE", "INSECTE"]},
        "M4": {"nature": "ACTION", "est_twist": False, "roles_portes": ["AUTONOMIE_A0"], "tags": ["A0", "INSECTES"], "entrees": ["NID", "INSECTE", "DEFENSEUR_ATTENTE", "TAMBOUR"], "sorties": ["DEFENSEUR_REDEPLOYE", "INSECTE"]},
        "M5": {"nature": "LOI_PASSIVE", "est_twist": False, "roles_portes": ["AUTONOMIE_A0", "LOI_PASSIVE"], "tags": ["A0", "INSECTES", "LOI_PASSIVE"], "entrees": ["NID_ACTIVE", "INSECTE", "INSECTE_RANG", "POSITION_REVE"], "sorties": ["ALTERATION", "INSECTE_RANG", "INSECTE"]},
    },
}

# Partition disjointe exacte 30/30 dérivée de l'axe mécanique primaire dans tiles_canon_v6_4.json
DISJOINT_MOTOR_DEFS: dict[str, dict[str, Any]] = {
    "ESSAIM_NIDS": {
        "label": "Essaim & Nids",
        "description": "Gardiens Insectes (G13-G15) et les 5 Nids d'Insectes (M1-M5)",
        "primary_rule": "Tuiles dont le cœur mécanique est NID / INSECTES (hors Rêves purs R6/R10)",
    },
    "DUEL_TERRAIN_THERMIQUE": {
        "label": "Duel, Terrain & Thermique",
        "description": "Combat de parcelle, Duel/Territoire, Croc/Piège, Cale/Ratissage et Bourbier",
        "primary_rule": "Tuiles d'engagement frontal (DUEL/CROC/PIEGE/CALE/RATISSAGE/BOURBIER)",
    },
    "REDEPLOIEMENT_PERCHOIR_RELAIS": {
        "label": "Redéploiement, Perchoir & Relais",
        "description": "Mobilité des Défenseurs, coordination Perchoir/Plume et relais Gardiens",
        "primary_rule": "Tuiles centrées sur PERCHOIR, DEFENSEUR_REDEPLOYE et relais Gardiens",
    },
    "SOMMEIL_REVES": {
        "label": "Sommeil & Réglette des Rêves",
        "description": "Compaction, Piston, rélecture de rang et annulation renforcée de la réglette",
        "primary_rule": "Tuiles pilotant l'avancement ou la lecture de la réglette des Rêves",
    },
    "ALTERATION_LOIS": {
        "label": "Altération & Lois passives",
        "description": "Altération des machines, lois passives (R7, R8) et transposition d'Entités",
        "primary_rule": "Tuiles d'Altération structurelle et lois passives hors Nids",
    },
}

# Prédicats de jetons d'entrées/sorties pour les moteurs fonctionnels avec tuiles-pivots
PIVOT_MOTOR_PREDICATES: dict[str, tuple[str, frozenset[str]]] = {
    "MOTEUR_SOMMEIL_REGLETTE": (
        "Sommeil & Réglette des Rêves",
        frozenset({"POSITION_REVE", "RANG_REVE", "REVE_COMPACTE", "PISTON_REVES", "RANG_RELU"}),
    ),
    "MOTEUR_ALTERATION": (
        "Altération & Entités",
        frozenset({"ALTERATION"}),
    ),
    "MOTEUR_DUEL_TERRAIN": (
        "Duel & Contrôle du Terrain",
        frozenset({"DUEL", "TERRITOIRE", "DEFI", "BOURBIER_ROUTE"}),
    ),
    "MOTEUR_THERMIQUE_PIEGE_CROC": (
        "Thermique, Piège, Croc & Sabotage",
        frozenset({"ROUGE", "BLEU", "CROC", "CROC_POSTE", "PIEGE", "CALE", "ECAILLE", "SABOTAGE", "RATISSAGE", "RATISSAGE_ROMPU", "ANNULATION_SURCHAUFFE"}),
    ),
    "MOTEUR_PERCHOIR_REDEPLOIEMENT": (
        "Perchoir & Redéploiement",
        frozenset({"PERCHOIR", "DEFENSEUR_REDEPLOYE", "DEFENSEUR_ATTENTE", "PARI_GLISSE", "ACTIVATION_RELAIS"}),
    ),
    "MOTEUR_CHAMANES_ANNULATION": (
        "Chamanes & Annulation",
        frozenset({"TAMBOUR", "CHANT", "CHAMANE_EN_FORET", "ANNULATION", "ANNULATION_RENFORCEE", "ANNULATION_INDUITE"}),
    ),
    "MOTEUR_ESSAIM_NIDS": (
        "Essaim & Nids d'Insectes",
        frozenset({"INSECTE", "NID", "NID_ACTIVE", "NID_NOMADE", "NID_DEPLACE", "INSECTE_RANG", "INSECTE_PASSAGER", "INSECTE_TRANSPORTE", "PONTE", "RIPOSTE_ESSAIM", "PARADE_SOLDATS"}),
    ),
}

_CANON_META_CACHE: dict[str, Any] | None = None


def load_tile_canon_metadata(canon_path: Path | None = None) -> dict[str, Any]:
    """Charge `contracts/tiles_canon_v6_4.json` (ou repli embarqué vérifié en conteneur worker)."""
    global _CANON_META_CACHE
    if canon_path is None and _CANON_META_CACHE is not None:
        return _CANON_META_CACHE

    candidate = (
        canon_path
        if canon_path is not None
        else Path(__file__).resolve().parent.parent / "contracts" / "tiles_canon_v6_4.json"
    )
    if candidate.is_file():
        data = json.loads(candidate.read_text(encoding="utf-8"))
        if canon_path is None:
            _CANON_META_CACHE = data
        return data
    if canon_path is not None:
        raise FileNotFoundError(f"Contrat introuvable : {candidate}")
    _CANON_META_CACHE = _EMBEDDED_TILES_CANON_FALLBACK
    return _EMBEDDED_TILES_CANON_FALLBACK


def _sort_slots_canon(slots: set[str] | list[str] | tuple[str, ...]) -> tuple[str, ...]:
    s_set = set(slots)
    unknown = s_set - CANONICAL_30_TILES_SET
    if unknown:
        raise ValueError(f"Emplacements de tuiles inconnus : {sorted(unknown)}")
    return tuple(s for s in CANONICAL_30_TILES if s in s_set)


def _classify_disjoint_motor(slot: str, meta: dict[str, Any]) -> str:
    """Assigne chaque tuile canonique à exactement 1 moteur disjoint à partir de ses métadonnées v6.4."""
    entrees = {str(x) for x in meta.get("entrees", ())}
    sorties = {str(x) for x in meta.get("sorties", ())}
    tags = {str(x) for x in meta.get("tags", ())}
    tokens = entrees | sorties
    nature = str(meta.get("nature", "ACTION"))

    # 1. Essaim & Nids : Nids M1..M5 + Gardiens portant un Nid
    if slot.startswith("M") or ("NID" in tokens and slot.startswith("G")):
        return "ESSAIM_NIDS"
    # 2. Altération & Lois passives : Lois passives (R7, R8) et tuiles centrées sur Altération (G10, R2, R10)
    if nature == "LOI_PASSIVE":
        return "ALTERATION_LOIS"
    if "ALTERATION" in sorties and not ("POSITION_REVE" in sorties):
        return "ALTERATION_LOIS"
    # 3. Sommeil & Réglette des Rêves : tuiles manipulant POSITION_REVE / RANG_RELU / ANNULATION_RENFORCEE
    if (
        "POSITION_REVE" in sorties
        or "RANG_RELU" in sorties
        or "ANNULATION_RENFORCEE" in sorties
        or "LEVIER_REVE" in tags
    ):
        return "SOMMEIL_REVES"
    # 4. Redéploiement, Perchoir & Relais : Perchoir/Relais/Redéploiement (hors Combat pur G5 Piège/Croc et R3 Duel)
    if (
        "PARI_GLISSE" in sorties
        or "ACTIVATION_RELAIS" in sorties
        or "ANNULATION_SURCHAUFFE" in sorties
        or ("PERCHOIR" in entrees and "PIEGE" not in sorties)
    ):
        return "REDEPLOIEMENT_PERCHOIR_RELAIS"
    # 5. Duel, Terrain & Thermique : reste du combat direct (G1, G2, G5, G7, G9, R3)
    return "DUEL_TERRAIN_THERMIQUE"


def get_disjoint_motors(canon_meta: dict[str, Any] | None = None) -> dict[str, tuple[str, ...]]:
    """Retourne la partition disjointe exacte 30/30 des tuiles v6.4 en 5 moteurs."""
    data = canon_meta if canon_meta is not None else load_tile_canon_metadata()
    tuiles = data["tuiles_ciblees"]
    buckets: dict[str, list[str]] = {k: [] for k in DISJOINT_MOTOR_DEFS}
    for slot in CANONICAL_30_TILES:
        motor_id = _classify_disjoint_motor(slot, tuiles[slot])
        buckets[motor_id].append(slot)
    result = {k: _sort_slots_canon(v) for k, v in buckets.items()}
    covered = [s for sl in result.values() for s in sl]
    assert len(covered) == 30 and set(covered) == CANONICAL_30_TILES_SET, (
        "La partition disjointe des moteurs doit couvrir exactement les 30 tuiles."
    )
    return result


def get_pivot_motors(canon_meta: dict[str, Any] | None = None) -> dict[str, tuple[str, ...]]:
    """Retourne les 7 moteurs fonctionnels recouvrants (avec tuiles-pivots) dérivés de `tiles_canon_v6_4.json`."""
    data = canon_meta if canon_meta is not None else load_tile_canon_metadata()
    tuiles = data["tuiles_ciblees"]
    motors: dict[str, list[str]] = {k: [] for k in PIVOT_MOTOR_PREDICATES}
    for slot in CANONICAL_30_TILES:
        meta = tuiles[slot]
        tokens = {str(x) for x in meta.get("entrees", ())} | {
            str(x) for x in meta.get("sorties", ())
        }
        for motor_id, (_, kw_set) in PIVOT_MOTOR_PREDICATES.items():
            if tokens & kw_set:
                motors[motor_id].append(slot)
    return {k: _sort_slots_canon(v) for k, v in motors.items()}


def get_role_motors(canon_meta: dict[str, Any] | None = None) -> dict[str, tuple[str, ...]]:
    """Retourne les 6 regroupements officiels `carte_des_roles` de `contracts/tiles_canon_v6_4.json`."""
    data = canon_meta if canon_meta is not None else load_tile_canon_metadata()
    roles_raw = data.get("carte_des_roles", {}).get("roles", {})
    out: dict[str, tuple[str, ...]] = {}
    for r_key, entries in roles_raw.items():
        slots = [str(item).split("=", 1)[0].strip() for item in entries]
        out[f"ROLE_{str(r_key).upper()}"] = _sort_slots_canon(slots)
    return out


def get_pivot_tiles(
    pivot_motors: dict[str, tuple[str, ...]] | None = None,
) -> dict[str, tuple[str, ...]]:
    """Identifie les tuiles-pivots appartenant à au moins 2 moteurs fonctionnels recouvrants."""
    pm = pivot_motors if pivot_motors is not None else get_pivot_motors()
    membership: dict[str, list[str]] = {s: [] for s in CANONICAL_30_TILES}
    for m_id, slots in pm.items():
        for s in slots:
            membership[s].append(m_id)
    return {s: tuple(ms) for s, ms in membership.items() if len(ms) >= 2}


def get_motor_catalog(
    scope: str = "ALL",
    canon_meta: dict[str, Any] | None = None,
) -> dict[str, tuple[str, ...]]:
    """Retourne le catalogue de moteurs demandé (`DISJOINT`, `PIVOTS`, `ROLES`, ou `ALL`)."""
    sc = str(scope).upper()
    if sc == "DISJOINT":
        return get_disjoint_motors(canon_meta)
    if sc == "PIVOTS":
        return get_pivot_motors(canon_meta)
    if sc == "ROLES":
        return get_role_motors(canon_meta)
    if sc == "ALL":
        merged: dict[str, tuple[str, ...]] = {}
        merged.update(get_disjoint_motors(canon_meta))
        merged.update(get_pivot_motors(canon_meta))
        merged.update(get_role_motors(canon_meta))
        return merged
    raise ValueError(f"Scope de moteurs inconnu : {scope!r} (attendu DISJOINT|PIVOTS|ROLES|ALL)")


def build_all_neutre_tile_profiles() -> tuple[tuple[str, str], ...]:
    """Retourne `tile_profiles` mettant les 30 emplacements canoniques à `NEUTRE`."""
    return tuple((s, "NEUTRE") for s in CANONICAL_30_TILES)


def build_tile_profiles_from_active_subset(
    active_slots: set[str] | list[str] | tuple[str, ...],
    *,
    active_profile: str = "A",
    extra_overrides: tuple[tuple[str, str], ...] = (),
) -> tuple[tuple[str, str], ...]:
    """Construit `tile_profiles` en activant uniquement `active_slots` et mettant les autres à `NEUTRE`."""
    active_canon = set(_sort_slots_canon(active_slots))
    profs: dict[str, str] = {}
    for s in CANONICAL_30_TILES:
        if s in active_canon:
            if active_profile != "A":
                profs[s] = active_profile
        else:
            profs[s] = "NEUTRE"
    for k, v in extra_overrides:
        profs[str(k)] = str(v)
    return tuple(sorted(profs.items()))


def build_tile_profiles_from_neutral_subset(
    neutral_slots: set[str] | list[str] | tuple[str, ...],
    *,
    extra_overrides: tuple[tuple[str, str], ...] = (),
) -> tuple[tuple[str, str], ...]:
    """Construit `tile_profiles` en gardant toutes les tuiles actives sauf `neutral_slots` mis à `NEUTRE`."""
    neutral_canon = set(_sort_slots_canon(neutral_slots))
    active = [s for s in CANONICAL_30_TILES if s not in neutral_canon]
    return build_tile_profiles_from_active_subset(active, extra_overrides=extra_overrides)


def resolve_slot_selection(spec: Any) -> tuple[str, ...]:
    """Résout une sélection flexible d'emplacements : liste, `ALL`, `NONE`, `G`/`R`/`M`, `EDGE:<k>`, `MOTOR:<k>`."""
    if spec is None:
        return ()
    if isinstance(spec, str):
        tok = spec.strip().upper()
        if tok in ("", "NONE", "EMPTY", "ALL_NEUTRE"):
            return ()
        if tok in ("ALL", "ALL_30", "ALL_ACTIVE", "STANDARD_A"):
            return CANONICAL_30_TILES
        if tok in ("GARDIENS", "G"):
            return tuple(s for s in CANONICAL_30_TILES if s.startswith("G"))
        if tok in ("REVES", "R"):
            return tuple(s for s in CANONICAL_30_TILES if s.startswith("R"))
        if tok in ("NIDS", "M", "CROISSANCE"):
            return tuple(s for s in CANONICAL_30_TILES if s.startswith("M"))
        if tok.startswith("EDGE:"):
            ek = tok.split(":", 1)[1]
            if ek not in MATRICE_PAIRES:
                raise ValueError(f"Lisière inconnue : {ek!r}")
            return _sort_slots_canon(MATRICE_PAIRES[ek])
        if tok.startswith("MOTOR:"):
            mk = tok.split(":", 1)[1]
            cat = get_motor_catalog("ALL")
            if mk not in cat:
                raise ValueError(f"Moteur inconnu : {mk!r}. Disponibles : {sorted(cat)}")
            return cat[mk]
        if tok in CANONICAL_30_TILES_SET:
            return (tok,)
        if tok in MATRICE_PAIRES:
            return _sort_slots_canon(MATRICE_PAIRES[tok])
        cat = get_motor_catalog("ALL")
        if tok in cat:
            return cat[tok]
        raise ValueError(f"Sélection d'emplacements inconnue : {spec!r}")
    if isinstance(spec, (list, tuple, set)):
        collected: set[str] = set()
        for item in spec:
            collected.update(resolve_slot_selection(item))
        return _sort_slots_canon(collected)
    raise ValueError(f"Format de sélection d'emplacements invalide : {spec!r}")


@dataclass(frozen=True, slots=True)
class ModularVariantSpec:
    """Spécification exécutable d'une variante dans une étude modulaire à « Tuiles à blanc »."""

    variant_id: str
    study_role: str
    active_slots: tuple[str, ...]
    tile_profiles: tuple[tuple[str, str], ...]
    target_slots: tuple[str, ...] = ()
    group_id: str = ""
    required_any_slots: tuple[str, ...] = ()
    extra_meta: dict[str, Any] = field(default_factory=dict)


def _resolve_motor_dict(motors_spec: Any) -> dict[str, tuple[str, ...]]:
    if motors_spec is None:
        return get_disjoint_motors()
    if isinstance(motors_spec, str):
        su = motors_spec.strip().upper()
        if su in ("DISJOINT", "PIVOTS", "ROLES", "ALL"):
            return get_motor_catalog(su)
        all_m = get_motor_catalog("ALL")
        if su in all_m:
            return {su: all_m[su]}
        raise ValueError(f"Spécification de moteurs inconnue : {motors_spec!r}")
    if isinstance(motors_spec, list):
        all_m = get_motor_catalog("ALL")
        out: dict[str, tuple[str, ...]] = {}
        for item in motors_spec:
            key = str(item).strip().upper()
            if key in ("DISJOINT", "PIVOTS", "ROLES"):
                out.update(get_motor_catalog(key))
            elif key in all_m:
                out[key] = all_m[key]
            else:
                raise ValueError(f"Moteur inconnu dans la liste : {item!r}")
        return out
    if isinstance(motors_spec, dict):
        return {str(k).strip().upper(): resolve_slot_selection(v) for k, v in motors_spec.items()}
    raise ValueError(f"Format de `motors` invalide : {motors_spec!r}")


def _resolve_edge_list(edges_spec: Any) -> tuple[str, ...]:
    if edges_spec is None or str(edges_spec).upper() == "ALL":
        return _ORDERED_EDGE_KEYS
    if isinstance(edges_spec, str):
        ek = edges_spec.strip().upper()
        if ek not in MATRICE_PAIRES:
            raise ValueError(f"Lisière inconnue : {ek!r}")
        # Normaliser sur la clé canonique si l'utilisateur a écrit R_M au lieu de M_R
        pair_set = frozenset(MATRICE_PAIRES[ek])
        for canon_k, canon_pair in CANONICAL_15_EDGES.items():
            if frozenset(canon_pair) == pair_set:
                return (canon_k,)
        return (ek,)
    if isinstance(edges_spec, list):
        out: list[str] = []
        for item in edges_spec:
            for k in _resolve_edge_list(item):
                if k not in out:
                    out.append(k)
        return tuple(out)
    raise ValueError(f"Format de `edges` invalide : {edges_spec!r}")


def resolve_modular_study_variants(tile_study: dict[str, Any]) -> tuple[ModularVariantSpec, ...]:
    """Résout un bloc manifeste `tile_study` en variantes CRN dédupliquées.

    Types supportés :
    - `SUBSET` : sous-ensemble arbitraire (`active_slots` ou `neutral_slots` ou `motor` ou `edge`)
    - `SOLO_ISOLATED` : plancher solo (`ALL_NEUTRE` vs `SOLO:<slot>`)
    - `LEAVE_ONE_OUT` : ablation écosystème (`ALL_ACTIVE` vs `LOO:<slot>`)
    - `SOLO_AND_ECOSYSTEM` : plancher solo + ablation écosystème + levier synergique L_syn
    - `EDGE_2X2` : carrés factoriels 2×2 sur les 15 lisières (`ALL_NEUTRE` ou `STANDARD_A` en fond)
    - `MOTORS_SOLO` / `MOTORS_ABLATION` / `MOTORS_BOTH` : moteurs disjoints, pivots ou personnalisés
    - `CUSTOM_VARIANTS` : liste libre de variantes nommées
    """
    study_type = str(tile_study.get("study_type", "SUBSET")).strip().upper()
    filter_by_presence = bool(tile_study.get("filter_tables_by_presence", False))

    variants_by_active: dict[tuple[str, ...], ModularVariantSpec] = {}
    ordered_keys: list[tuple[str, ...]] = []
    aliases: dict[str, str] = {}

    def _register(
        variant_id: str,
        study_role: str,
        active_slots: tuple[str, ...],
        *,
        target_slots: tuple[str, ...] = (),
        group_id: str = "",
        extra_meta: dict[str, Any] | None = None,
    ) -> str:
        canon_active = _sort_slots_canon(active_slots)
        if canon_active in variants_by_active:
            existing = variants_by_active[canon_active]
            aliases[variant_id] = existing.variant_id
            # Enrichir les métadonnées d'alias si plusieurs rôles partagent la même config (ex: EDGE_2X2 + SOLO)
            existing.extra_meta.setdefault("shared_aliases", []).append(
                {
                    "variant_id": variant_id,
                    "study_role": study_role,
                    "group_id": group_id,
                    "target_slots": list(target_slots),
                    **(extra_meta or {}),
                }
            )
            return existing.variant_id
        req_slots = target_slots if (filter_by_presence and target_slots) else ()
        spec = ModularVariantSpec(
            variant_id=variant_id,
            study_role=study_role,
            active_slots=canon_active,
            tile_profiles=build_tile_profiles_from_active_subset(canon_active),
            target_slots=target_slots,
            group_id=group_id,
            required_any_slots=req_slots,
            extra_meta=dict(extra_meta or {}),
        )
        variants_by_active[canon_active] = spec
        ordered_keys.append(canon_active)
        return variant_id

    if study_type == "SUBSET":
        if "active_slots" in tile_study:
            active_sub = resolve_slot_selection(tile_study["active_slots"])
        elif "slots" in tile_study:
            active_sub = resolve_slot_selection(tile_study["slots"])
        elif "neutral_slots" in tile_study:
            neut_sub = set(resolve_slot_selection(tile_study["neutral_slots"]))
            active_sub = tuple(s for s in CANONICAL_30_TILES if s not in neut_sub)
        elif "motor" in tile_study:
            active_sub = resolve_slot_selection(f"MOTOR:{tile_study['motor']}")
        elif "edge" in tile_study:
            active_sub = resolve_slot_selection(f"EDGE:{tile_study['edge']}")
        else:
            active_sub = ()
        baselines = tile_study.get("include_baselines", ["ALL_NEUTRE"])
        if isinstance(baselines, str):
            baselines = [baselines]
        for b_name in baselines:
            bu = str(b_name).upper()
            if bu == "ALL_NEUTRE":
                _register("ALL_NEUTRE", "baseline_neutre", (), group_id="BASELINE")
            elif bu in ("ALL_ACTIVE", "STANDARD_A"):
                _register("ALL_ACTIVE", "baseline_active", CANONICAL_30_TILES, group_id="BASELINE")
        sub_name = str(tile_study.get("subset_name", "SUBSET_CUSTOM"))
        _register(sub_name, "subset", active_sub, target_slots=active_sub, group_id=sub_name)

    elif study_type == "SOLO_ISOLATED":
        slots = resolve_slot_selection(tile_study.get("slots", "ALL"))
        _register("ALL_NEUTRE", "baseline_neutre", (), group_id="BASELINE")
        for s in slots:
            _register(f"SOLO:{s}", "solo", (s,), target_slots=(s,), group_id=s)

    elif study_type == "LEAVE_ONE_OUT":
        slots = resolve_slot_selection(tile_study.get("slots", "ALL"))
        _register("ALL_ACTIVE", "baseline_active", CANONICAL_30_TILES, group_id="BASELINE")
        for s in slots:
            rem = tuple(x for x in CANONICAL_30_TILES if x != s)
            _register(f"LOO:{s}", "loo", rem, target_slots=(s,), group_id=s)

    elif study_type == "SOLO_AND_ECOSYSTEM":
        slots = resolve_slot_selection(tile_study.get("slots", "ALL"))
        _register("ALL_NEUTRE", "baseline_neutre", (), group_id="BASELINE")
        _register("ALL_ACTIVE", "baseline_active", CANONICAL_30_TILES, group_id="BASELINE")
        for s in slots:
            _register(f"SOLO:{s}", "solo", (s,), target_slots=(s,), group_id=s)
        for s in slots:
            rem = tuple(x for x in CANONICAL_30_TILES if x != s)
            _register(f"LOO:{s}", "loo", rem, target_slots=(s,), group_id=s)

    elif study_type == "EDGE_2X2":
        edges = _resolve_edge_list(tile_study.get("edges", "ALL"))
        bg = str(tile_study.get("background", "ALL_NEUTRE")).strip().upper()
        if bg not in ("ALL_NEUTRE", "STANDARD_A", "ALL_ACTIVE"):
            raise ValueError(f"background EDGE_2X2 invalide : {bg!r} (ALL_NEUTRE ou STANDARD_A)")
        is_blank_bg = bg == "ALL_NEUTRE"
        if is_blank_bg:
            _register("ALL_NEUTRE", "baseline_neutre", (), group_id="BASELINE")
        else:
            _register("ALL_ACTIVE", "baseline_active", CANONICAL_30_TILES, group_id="BASELINE")
        for ek in edges:
            sa, sb = CANONICAL_15_EDGES[ek]
            if is_blank_bg:
                c00: tuple[str, ...] = ()
                c10: tuple[str, ...] = (sa,)
                c01: tuple[str, ...] = (sb,)
                c11: tuple[str, ...] = _sort_slots_canon((sa, sb))
            else:
                c00 = tuple(x for x in CANONICAL_30_TILES if x not in (sa, sb))
                c10 = tuple(x for x in CANONICAL_30_TILES if x != sb)
                c01 = tuple(x for x in CANONICAL_30_TILES if x != sa)
                c11 = CANONICAL_30_TILES
            edge_meta = {"edge": ek, "slot_a": sa, "slot_b": sb, "background": bg}
            _register(f"EDGE:{ek}:00", "edge_2x2", c00, target_slots=(sa, sb), group_id=ek, extra_meta={**edge_meta, "cell": "00"})
            _register(f"EDGE:{ek}:10", "edge_2x2", c10, target_slots=(sa, sb), group_id=ek, extra_meta={**edge_meta, "cell": "10"})
            _register(f"EDGE:{ek}:01", "edge_2x2", c01, target_slots=(sa, sb), group_id=ek, extra_meta={**edge_meta, "cell": "01"})
            _register(f"EDGE:{ek}:11", "edge_2x2", c11, target_slots=(sa, sb), group_id=ek, extra_meta={**edge_meta, "cell": "11"})

    elif study_type in ("MOTORS_SOLO", "MOTORS_ABLATION", "MOTORS_BOTH"):
        raw_mot = tile_study.get("motors", tile_study.get("motor_family", "DISJOINT"))
        motors_map = _resolve_motor_dict(raw_mot)
        want_solo = study_type in ("MOTORS_SOLO", "MOTORS_BOTH")
        want_ablation = study_type in ("MOTORS_ABLATION", "MOTORS_BOTH")
        if want_solo:
            _register("ALL_NEUTRE", "baseline_neutre", (), group_id="BASELINE")
        if want_ablation or bool(tile_study.get("include_all_active", want_solo and study_type == "MOTORS_SOLO")):
            _register("ALL_ACTIVE", "baseline_active", CANONICAL_30_TILES, group_id="BASELINE")
        for m_id, m_slots in motors_map.items():
            if want_solo:
                _register(
                    f"MOTOR_SOLO:{m_id}",
                    "motor_solo",
                    m_slots,
                    target_slots=m_slots,
                    group_id=m_id,
                    extra_meta={"motor_id": m_id, "motor_slots": list(m_slots)},
                )
            if want_ablation:
                rem = tuple(x for x in CANONICAL_30_TILES if x not in m_slots)
                _register(
                    f"MOTOR_ABLATION:{m_id}",
                    "motor_ablation",
                    rem,
                    target_slots=m_slots,
                    group_id=m_id,
                    extra_meta={"motor_id": m_id, "motor_slots": list(m_slots)},
                )

    elif study_type == "CUSTOM_VARIANTS":
        raw_variants = tile_study.get("variants")
        if not isinstance(raw_variants, list) or not raw_variants:
            raise ValueError("CUSTOM_VARIANTS exige une liste non vide `variants`.")
        for idx, v_raw in enumerate(raw_variants):
            if not isinstance(v_raw, dict):
                raise TypeError(f"Variante {idx} invalide : {v_raw!r}")
            vid = str(v_raw.get("id", f"CUSTOM_{idx}"))
            if "active_slots" in v_raw:
                act = resolve_slot_selection(v_raw["active_slots"])
            elif "neutral_slots" in v_raw:
                neut = set(resolve_slot_selection(v_raw["neutral_slots"]))
                act = tuple(s for s in CANONICAL_30_TILES if s not in neut)
            elif "motor" in v_raw:
                act = resolve_slot_selection(f"MOTOR:{v_raw['motor']}")
            elif "edge" in v_raw:
                act = resolve_slot_selection(f"EDGE:{v_raw['edge']}")
            else:
                raise ValueError(f"Variante {vid} sans `active_slots`/`neutral_slots`/`motor`/`edge`.")
            role = str(v_raw.get("study_role", "custom"))
            grp = str(v_raw.get("group_id", vid))
            _register(vid, role, act, target_slots=act, group_id=grp)
    else:
        raise ValueError(
            f"study_type inconnu : {study_type!r}. "
            "Valeurs supportées : SUBSET, SOLO_ISOLATED, LEAVE_ONE_OUT, "
            "SOLO_AND_ECOSYSTEM, EDGE_2X2, MOTORS_SOLO, MOTORS_ABLATION, MOTORS_BOTH, CUSTOM_VARIANTS."
        )

    return tuple(variants_by_active[k] for k in ordered_keys)
