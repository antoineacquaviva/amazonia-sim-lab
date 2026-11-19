#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scripts/build_v5_3_audit.py
 Consolidation formelle v5.3-audit — Amazonia : Dernier Rempart (Doc Studio)

Actions réalisées :
1. Sauvegarde horodatée de `data/catalog_v5_3.json` et `data/amazonia_data_v5_3.js`.
2. Injection de la spécification formelle consolidée (25 arbitrages + 6 étapes normées)
   dans `data/spec_formelle_v5_3.json`, `data/catalog_v5_3.json` et `data/amazonia_data_v5_3.js`.
3. Purge lexicale et mécanique des concepts supprimés (Insectes engagés, dette de parade,
   verrouillage des parcelles ciblées, exigence de présence locale pour armer un Piège,
   cibles figées à la révélation, recomptage dynamique du seuil de Réveil).
4. Patchs chirurgicaux par tuile (Fourmilière Coupe-Feuilles, Ruches des Mélipones,
   La Piquée de la Harpie, Le Guet du Caïman Noir, Le Cri d'Alarme de l'Ara,
   L'Étreinte de l'Anaconda, L'Affût de la Matamata, L'Écho des Voix Célestes,
   Le Miel des Ancêtres, Guêpes Cazadores) avec autonomisation des Faces 2.
5. Protection stricte par sentinelles de toutes les interpolations JS (`${...}`).
6. Suite d'auto-vérification (intégrité JSON, invariance `${...}`, absence de résidus bannis,
   couverture de `peuple_origine`).
"""

from __future__ import annotations

import argparse
import copy
import datetime as dt
import json
import re
import shutil
import sys
import unicodedata
from pathlib import Path
from typing import Any, Callable


# Force UTF-8 sur la sortie standard (notamment sous Windows PowerShell)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


# ============================================================================
# 1. SPÉCIFICATION FORMELLE CONSOLIDÉE (25 ARBITRAGES + CHÂSSIS V5.3-AUDIT)
# ============================================================================

PEUPLES_CANONIQUES: list[str] = [
    "Humains",
    "Entités",
    "Insectes",
    "Mammifères",
    "Oiseaux",
    "Reptiles/Amphibiens",
]

SPEC_FORMELLE_V5_3: dict[str, Any] = {
    "schema_version": "5.3.1-audit",
    "date_consolidation": "2026-11-16",
    "architecture_reference": {
        "total_emplacements_synergie": 30,
        "total_pistes_migration": 2,
        "total_profils": 100,
        "topologies_validees": {
            "P3": [2, 3, 3],
            "P4_2233": [2, 2, 3, 3],
            "P5_22233": [2, 2, 2, 3, 3],
            "P6": [2, 2, 2, 3, 3, 3],
        },
        "reserves_materiel": "illimitees",
        "plafond_repousse_parcelle": "dotation_initiale_arbres",
    },
    "principes_transverses": {
        "gouvernance_unitaire": (
            "Chaque Tuile de Synergie (Gardien, Rêve, Nid) et chaque piste de Migration "
            "est gouvernée exclusivement par le joueur de son Peuple d'origine (champ "
            "peuple_origine). Zéro vote de groupe."
        ),
        "communication_muette": (
            "Silence tactique complet tant que les paravents sont fermés (aucun échange "
            "verbal ou gestuel sur les coups, cartes ou dés). Sous Le Cri d'Alarme de l'Ara "
            "(ouverture anticipée), visibilité publique des cartes et dés mais pose individuelle "
            "sans concertation orale."
        ),
        "pont_routier_routes_forestieres": (
            "Le long d'un rayon de Forêt, toute Route Forestière est systématiquement sautée : "
            "viser devant, avancer, reculer, glisser un Piège ou migrer désignent toujours la "
            "prochaine parcelle non rasée dans cette direction. Latéralement (Forêt <-> Furtivité), "
            "une Route Forestière est infranchissable et inoccupable."
        ),
        "suppression_dette_et_verrouillage": (
            "Zéro Insecte engagé et zéro verrouillage des parcelles ciblées. Les Insectes "
            "requis lors d’une parade classique sont défaussés immédiatement à la frappe. "
            "Tant qu'un Insecte est sur le plateau, il est libre. Seul un Piège ayant déjà "
            "paré au moins une frappe ce tour-ci ne peut plus payer un coût volontaire avant "
            "son retrait de fin d'attaques."
        ),
        "cascades_gardiens_a_plat": (
            "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner "
            "la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de "
            "cardinalité). Dès qu'un Gardien s'ouvre, il reçoit immédiatement son marqueur "
            "'utilisé' avant application de son texte. Balayage à plat dans l'ordre croissant "
            "des cases 1 à 6, répété tant qu'une case allumée porte un Gardien non utilisé."
        ),
    },
    "etapes_tour": [
        {
            "numero": 1,
            "code": "PREPARATION_POSE_FURTIVITE",
            "nom": "Distribution, Dés secrets et Pose des Défenseurs",
            "regles": [
                "Les machines déjà sur la dernière parcelle non rasée de leur rayon sont en Siège (carte posée face visible sur place, hors paquet).",
                "S'il reste moins de cartes Machine que de joueurs (suite à un rayon entièrement rasé), distribution dans le sens horaire à partir du peuple ayant le plus d'Arbres debout ; les joueurs sans carte lancent quand même leurs 2 dés pour tenter d'ouvrir un Rêve.",
                "Interdiction à la pose : Route Forestière, emplacement de tuile déjà construit ou plein (2 constructeurs), tuile inconstructible (Gardien sans case libre autorisée, Nid sans parcelle légale), ou rive de Furtivité donnant sur une Route Forestière lorsque l'action requiert une parcelle adjacente non rasée.",
                "Piste de Furtivité à 4 emplacements par case (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs par case). Lorsqu'un Défenseur ENTRE sur une case de Furtivité (1er Défenseur, 2e en réflexion ou 2e posé directement en choix définitif), on le pose sur l'un des 4 emplacements valides et l'éventuel autre Défenseur présent glisse aussitôt sur l'emplacement jumeau du même bord (orientant l'unique action du binôme). Retourner sur place un jeton de sa face réflexion à sa face choix définitif se fait strictement sur son emplacement actuel, sans déplacement ni tirage.",
            ],
        },
        {
            "numero": 2,
            "code": "REVELATION_DES_REVES_FURTIVITE",
            "nom": "Ouverture des Paravents, Rêves, Dés et Furtivité",
            "regles": [
                "Ouverture simultanée des paravents. Fin du silence tactique ; ouverture de la fenêtre de jeu des cartes Sabotage visibles (gouvernées par les Humains, ou par leur acquéreur si les Humains sont absents).",
                "Double aux dés : peut ouvrir un Rêve en piste. Hors double, le plus petit dé s'applique à la carte Machine (sauf Loi modifiant le dé retenu).",
                "Si l'emplacement désigné par le dé retenu contient un Rêve, l'activation de cette machine est annulée pour le tour et ce Rêve peut s'ouvrir. Chaque Rêve ne peut s'ouvrir qu'au maximum 1 fois par tour toutes sources confondues.",
                "Chaque binôme complet sur une case de Furtivité déclenche 1 seule action, gouvernée par le joueur de la rive où se trouvent les 2 emplacements jumeaux occupés.",
            ],
        },
        {
            "numero": 3,
            "code": "CONSTRUCTION_SYNERGIES",
            "nom": "Construction obligatoire des Tuiles de Synergie",
            "regles": [
                "Toute tuile réunissant ses 2 constructeurs (ou 1 Défenseur + 1 Insecte avec La Brèche du Tamanoir) est obligatoirement construite.",
                "Nid : posé sur une parcelle non rasée de l'un de ses 2 rayons ne contenant aucune machine ni aucun autre Nid, accompagné de tous ses Défenseurs constructeurs.",
                "Rêve : la Tactique la plus à droite sur la piste est définitivement éjectée ; seules les tuiles situées à droite de ce trou glissent d'un cran vers la gauche ; le nouveau Rêve prend place en case 6 (les Insectes Bug restent sur leur numéro d'emplacement imprimé).",
                "Libération de bâtisseurs (Gardien/Rêve) : si 1 seul Défenseur est libéré parmi 2 (3 joueurs standard, ou 4-6 joueurs avec La Danse des Esprits-Fauves), le joueur du Peuple d'origine de la tuile choisit lequel et sa rive (1re parcelle adjacente non rasée). Si tous les Défenseurs bâtisseurs sont libérés (3 joueurs + Danse), chaque propriétaire choisit sa rive, dans la limite des Défenseurs réellement présents.",
            ],
        },
        {
            "numero": 4,
            "code": "NIDS_ET_MIGRATION",
            "nom": "Production des Nids et Migration des Insectes",
            "regles": [
                "Chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (y compris pour l'activation autonome des Guêpes Cazadores), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens. Une production hors phase (Le Miel des Ancêtres) ne crée que les jetons Insecte sans déclencher le pouvoir propre du Nid.",
                "Migration : chaque Insecte sur la roue peut se déplacer de 0 ou 1 cran (jusqu'à 2 avec L'Envol du Batará Suiveur), même s'il a bougé lors de la production d'un Nid. On retourne chaque jeton déplacé sur sa face verso pour suivi, puis on remet tous les jetons à l'endroit en fin de Migration avant d'évaluer la Colonisation.",
                "Depuis la dernière parcelle non rasée d'un rayon, 1 cran permet d'entrer sur n'importe quelle case 1..6 d'une piste globale (Bug du Cerveau ou Colonisation des Gardiens), sans limite de jetons par case. Cet aller simple est définitif.",
            ],
        },
        {
            "numero": 5,
            "code": "ATTAQUES_ET_TEST_FIN",
            "nom": "Attaques des Machines et Vérification de Fin de Partie",
            "regles": [
                "Fermeture de la fenêtre libre des cartes Sabotage au coup d'envoi de la 1re attaque ; toutefois, toute carte Sabotage fraîchement piochée pendant les attaques peut être jouée immédiatement au moment de sa pioche.",
                "Ordre des machines : Piste des Tactiques de 1 à 6, puis machines en Siège. Sur un même rayon au même rang (ou en Siège), l'Abatteuse agit toujours avant le Bulldozer ; entre rayons distincts au même rang, ordre libre entre les joueurs concernés.",
                "Chaque machine est résolue d'un seul tenant : lecture dynamique de ses cibles depuis sa position physique réelle à cet instant (en sautant toute Route Forestière) -> frappes -> avancée éventuelle -> gain éventuel de jeton rouge.",
                "Chaîne stricte des parades à chaque frappe : (1) Bond du Jaguar (Loi auto : 2 jetons bleus défaussés -> toutes frappes restantes de la machine parées + recul) -> (2) Piquée de la Harpie -> (3) Piège (Embuscade auto si Défense totale >= 1, locale ou soutenue à distance ; le Piège est marqué comme ayant servi) -> (4) Parade classique (Défenseurs + défausse immédiate des Insectes manquants).",
                "Contact Machine-Nid : tout mouvement de machine (avancée, recul, repli depuis une Route) entrant sur la parcelle d'un Nid non protégé renvoie ce Nid en lisière (reconstructible) et défausse tous les Insectes de la parcelle (Défenseurs et Piège restent).",
                "Création d'une Route Forestière (0 Arbre et 0 Souche après un Bulldozer) : recul automatique des machines présentes vers la prochaine parcelle non rasée côté bordure, ou vers le cœur uniquement si tout est déjà rasé côté bordure (maintien irréversible du statut de Siège ; retrait définitif de la partie si tout le rayon est rasé).",
                "Fin des attaques : effets 'à la fin des attaques' (ex. Ruches des Mélipones) et retrait de tout Piège ayant paré au moins 1 frappe durant le tour.",
                "Vérification de fin de partie : fin du Tour 8, Rêve en case 1, ou seuil fixe de Réveil atteint sur la Piste des Gardiens (seuil calculé une fois pour toutes à la mise en place : inactif si moins de 3 Gardiens dans la partie, sinon min(nb_joueurs, total_gardiens_partie) avec minimum 3 et plafond 5 à 6 joueurs ; tout Gardien renvoyé en lisière perd son marqueur). Si atteint : saut de l'Apprentissage et passage direct à la Repousse Finale.",
            ],
        },
        {
            "numero": 6,
            "code": "APPRENTISSAGE_ET_MENAGE",
            "nom": "Apprentissage du Contremaître et Ménage de fin de tour",
            "regles": [
                "Seules les machines activées par une carte révélée ce tour-ci génèrent de l'Apprentissage (les machines en Siège produisent 0 Apprentissage).",
                "Gain par machine : +1 par parcelle réellement endommagée (au moins 1 Arbre coupé ou 1 Souche retirée par cette machine), +1 par jeton rouge acquis en fin d'attaque, -1 par jeton bleu présent sur la machine.",
                "Réductions : application des retraits volontaires de tuiles (Voile de l'Oubli, Brume de la Dendrobate) AVANT les Insectes Bug du Cerveau (un Bug sur une case déjà à 0 jeton n'est pas défaussé et reste en place).",
                "Avancement : la Tactique strictement seule en tête avec au moins 1 jeton échange sa place avec sa voisine de gauche (y compris un Rêve, qui recule d'un cran à droite ; immobile si déjà en case 1). En cas d'égalité avec L'Écho des Voix Célestes amenant son Rêve en case 1, la fin de partie se déclenche immédiatement à la fin de ce tour (Repousse Finale).",
                "Ménage systématique : remise en réserve de 100 % des jetons d'Apprentissage de toutes les tuiles dans tous les cas, retrait des marqueurs 'utilisé' des Gardiens et retour en main des Défenseurs.",
            ],
        },
    ],
    "arbitrages_valides": {
        f"A{i:02d}": desc
        for i, desc in enumerate(
            [
                "Dés et Tactiques : hors double (ouverture Rêve), le plus petit dé s'applique à la carte Machine (modifié par les Lois).",
                "Rêve sur dé Machine : annule l'activation de la machine et peut ouvrir ce Rêve (max 1 ouverture par Rêve et par tour).",
                "Furtivité à 4 emplacements (2 jumeaux/rive) : entrer sur la case tire l'autre jeton sur le jumeau et oriente l'action unique ; retourner en choix définitif se fait sur place sans déplacement.",
                "Gouvernance unitaire : chaque tuile de Synergie et piste de Migration est décidée uniquement par son Peuple d'origine.",
                "Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; suppression totale des Insectes engagés.",
                "Armement des Pièges : Embuscade dès que Défense totale >= 1 (locale ou à distance) ; tout Piège ayant paré >= 1 fois dans le tour est retiré en fin d'attaques.",
                "Zéro verrouillage des parcelles ciblées : Insectes toujours libres tant que présents ; seul un Piège déjà déclenché ce tour-ci ne peut plus payer de coût volontaire.",
                "Pont routier : Routes Forestières systématiquement sautées le long d'un rayon, mais infranchissables/inoccupables latéralement.",
                "Repli sur création de Route : recul automatique vers la bordure par défaut, vers le cœur seulement si bord tout rasé, retrait si rayon tout rasé ; Siège irréversible maintenu.",
                "Autonomie du Siège : actif même si la 4e Tactique est éjectée, et ne génère jamais de jetons d'Apprentissage.",
                "Insertion d'un Rêve : éjecte la Tactique la plus à droite ; seules les tuiles à droite du trou glissent à gauche ; pose en case 6 ; Bugs fixes sur les cases.",
                "Cascades de Gardiens : fin complète de l'effet en cours, marquage immédiat à l'ouverture, balayage à plat de 1 à 6 sans pile imbriquée.",
                "Faces 2 et Lois passives : seule la face visible s'applique (Faces 2 autonomes) ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume.",
                "Seuil de Réveil fixe : calculé à la mise en place (inactif si < 3 Gardiens en jeu) ; retour en lisière efface le marqueur.",
                "Test de fin de partie : maintenu en fin d'attaques (saut Apprentissage), avec déclenchement en fin d'Apprentissage si L'Écho des Voix Célestes amène son Rêve en case 1.",
                "Contact Machine-Nid : tout mouvement entrant (avancée, recul, repli) renvoie le Nid reconstructible en lisière et défausse tous les Insectes de la parcelle.",
                "Migration des Insectes : 0 ou 1 cran facultatif (suivi par retournement des pions) ; aller simple définitif et sans limite vers les pistes globales.",
                "Production des Nids : bloc indivisible (création selon état réel présent + pouvoir du Nid avant Gardiens) ; Miel des Ancêtres restreint aux jetons Insecte.",
                "Cibles dynamiques : lues selon la position physique réelle de la machine à l’instant où elle attaque.",
                "Matamata et chaîne des parades : Matamata vérifie la présence d'une Souche à chaque frappe ; ordre Jaguar -> Harpie -> Piège -> Parade classique.",
                "Anti-blocage et Nids : pose interdite sur case morte/tuile inconstructible ; 1 seul Nid par parcelle sans machine ; choix du bâtisseur libéré par Peuple d'origine.",
                "Communication muette : silence tactique sous paravent fermé ; simple visibilité publique sans concertation orale sous l'Ara.",
                "Apprentissage : dommage réel requis (>= 1 Arbre coupé ou Souche retirée) ; retraits volontaires avant Bugs ; remise à zéro intégrale en fin d'étape.",
                "Cartes Sabotage : visibles, gouvernées par les Humains (ou acquéreur si absents), recyclées, jouables de la Révélation au début des attaques + immédiatement si piochées en attaque.",
                "Séquence des attaques : Tactiques 1..6 puis Sièges ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant.",
            ],
            start=1,
        )
    },
}


# ============================================================================
# 2. OUTILS DE NORMALISATION ET PROTECTION DES INTERPOLATIONS JS (${...})
# ============================================================================

def strip_accents_lower(text: str) -> str:
    """Normalise une chaîne en minuscules sans accents pour la détection robuste des tuiles."""
    nfd = unicodedata.normalize("NFD", text)
    clean = "".join(ch for ch in nfd if unicodedata.category(ch) != "Mn")
    return clean.lower().replace("’", "'").replace("œ", "oe")


def protect_js_interpolations(js_text: str) -> tuple[str, list[str]]:
    """
    Remplace chaque interpolation JavaScript `${...}` (y compris accolades imbriquées)
    par une sentinelle neutre afin de garantir 0 corruption des templates `index.html`.
    """
    tokens: list[str] = []
    out: list[str] = []
    i = 0
    n = len(js_text)
    dollar = chr(36)

    while i < n:
        if js_text[i] == dollar and i + 1 < n and js_text[i + 1] == "{":
            depth = 1
            j = i + 2
            in_quote: str | None = None
            while j < n and depth > 0:
                ch = js_text[j]
                if in_quote:
                    if ch == "\\":
                        j += 2
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
                j += 1
            tokens.append(js_text[i:j])
            out.append(f"__AMAZONIA_JS_INTERP_{len(tokens) - 1:05d}__")
            i = j
        else:
            out.append(js_text[i])
            i += 1

    return "".join(out), tokens


def restore_js_interpolations(protected_text: str, tokens: list[str]) -> str:
    """Restaure à l'octet près toutes les interpolations JavaScript `${...}`."""
    result = protected_text
    for idx, original in enumerate(tokens):
        sentinel = f"__AMAZONIA_JS_INTERP_{idx:05d}__"
        result = result.replace(sentinel, original)
    return result


def safe_sub(pattern: str, replacement: str, text: str, flags: int = re.IGNORECASE) -> tuple[str, int]:
    """
    Substitution regex sécurisée par fonction lambda : n'interprète jamais les `$` ou `\\`
    dans la chaîne de remplacement.
    """
    count = 0

    def _repl(_match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        return replacement

    new_text = re.sub(pattern, _repl, text, flags=flags)
    return new_text, count


# ============================================================================
# 3. RÈGLES DE PURGE GLOBALE ET PATCHS CHIRURGICAUX PAR TUILE
# ============================================================================

# Remplacements lexicaux globaux (appliqués à tous les textes de règles et de tuiles)
GLOBAL_LEXICAL_RULES: list[tuple[str, str, str]] = [
    (
        r"insectes?\s+engag[ée]s?\s*(?:pour\s+parer|lors\s+d['’]une\s+parade|en\s+parade)?",
        "Insectes défaussés immédiatement lors de la parade",
        "Purge concept 'Insectes engagés'",
    ),
    (
        r"dette\s+d['’]insectes?",
        "défausse immédiate d’Insectes",
        "Purge concept 'dette d'Insectes'",
    ),
    (
        r"(?:avant|apr[èe]s|malgr[ée])\s+la\s+lev[ée]e\s+du\s+verrouillage(?:\s+des\s+parcelles)?",
        "à la fin des attaques",
        "Purge 'levée du verrouillage'",
    ),
    (
        r"parcelles?\s+verrouill[ée]es?(?:\s+pendant\s+les\s+attaques)?",
        "parcelles visées",
        "Purge 'parcelles verrouillées'",
    ),
    (
        r"verrouillage\s+des\s+parcelles\s+cibl[ée]es",
        "suivi direct des pions présents sur le plateau (sans verrouillage des parcelles)",
        "Purge 'verrouillage des parcelles ciblées'",
    ),
    (
        r"exige[_\s]+pr[ée]sence[_\s]+locale",
        "exige Défense totale >= 1 (locale ou soutenue à distance)",
        "Correction label trompeur d'armement de Piège",
    ),
    (
        r"Chaque\s+Insecte\s+bouge\s+d['’]un\s+cran(?!\s+ou\s+reste)",
        "Chaque Insecte sur la roue peut se déplacer de 0 ou 1 cran (retournez le jeton déplacé pour suivi)",
        "Migration facultative (Arb 17)",
    ),
]


def patch_tile_text_by_identity(tile_norm_header: str, text: str, field_name: str = "") -> tuple[str, list[str]]:
    """
    Applique les corrections chirurgicales propres à une tuile identifiée par son en-tête normalisé.
    Retourne `(nouveau_texte, liste_des_modifications)`.
    """
    changes: list[str] = []
    updated = text
    field_lower = field_name.lower()

    # 1. Fourmilière Coupe-Feuilles : épargne immédiate d'un Insecte à la parade
    if "coupe-feuilles" in tile_norm_header or "coupe feuilles" in tile_norm_header:
        new_txt, n = safe_sub(
            r"(?:retirez|d[ée]faussez)\s+1\s+insecte\s+engag[ée]\s+de\s+moins[^.;]*",
            "épargnez immédiatement 1 Insecte qui aurait dû être défaussé lors d’une parade classique",
            updated,
        )
        if n:
            updated = new_txt
            changes.append("Fourmilière Coupe-Feuilles : épargne immédiate à la parade")

    # 2. Ruches des Mélipones : retrait de toute référence au verrouillage en fin d'attaques
    if "melipones" in tile_norm_header:
        new_txt, n = safe_sub(
            r"\s*\(?[^()]*verrouillage[^()]*\)?",
            "",
            updated,
        )
        if n:
            updated = new_txt
            changes.append("Ruches des Mélipones : suppression mention verrouillage")

    # 3. Le Cri d'Alarme de l'Ara : suppression du témoin de recomptage dynamique + silence sous Ara
    if "alarme de l'ara" in tile_norm_header or "cri d'alarme" in tile_norm_header:
        new_txt, n = safe_sub(
            r"[^.!?]*(?:recompt|recalcul|ajuste\s+le\s+seuil|modifie\s+le\s+seuil)[^.!?]*[.!?]?",
            " Le seuil de Réveil reste fixe (calculé à la mise en place) et un Gardien renvoyé en lisière perd son marqueur « utilisé ».",
            updated,
        )
        if n:
            updated = new_txt.strip()
            changes.append("Cri d'Alarme de l'Ara : suppression du témoin de recomptage dynamique")
        if "paravents" in strip_accents_lower(updated) and "sans discussion" not in strip_accents_lower(updated):
            if any(k in field_lower for k in ("comment", "temoin", "note", "exemp", "desc", "regle", "effet", "texte", "")):
                if "ouvrir tous les paravents" in strip_accents_lower(updated) or "ouvrez tous les paravents" in strip_accents_lower(updated):
                    updated = (
                        updated.rstrip()
                        + " (Visibilité publique des cartes et dés, sans discussion tactique orale.)"
                    )
                    changes.append("Cri d'Alarme de l'Ara : précision visibilité publique sans concertation orale")

    # 4. L'Étreinte de l'Anaconda : suppression de la note "ne modifie pas les cibles programmées"
    if "anaconda" in tile_norm_header:
        new_txt, n = safe_sub(
            r"[^.!?]*ne\s+modifie\s+pas\s+les\s+cibles[^.!?]*[.!?]?",
            " Les cibles de la machine se liront depuis sa nouvelle position réelle à l’instant où elle attaque.",
            updated,
        )
        if n:
            updated = new_txt.strip()
            changes.append("Étreinte de l'Anaconda : lecture dynamique des cibles après recul")

    # 5. L'Affût de la Matamata : désignation libre d'une parcelle non rasée, Souche vérifiée à la frappe
    if "matamata" in tile_norm_header:
        new_txt, n1 = safe_sub(
            r"deux\s+parcelles\s+cibl[ée]es\s+contenant\s+au\s+moins\s+une\s+souche",
            "jusqu’à deux parcelles non rasées (le bonus s’applique à chaque frappe trouvant au moins une Souche sur place à cet instant)",
            updated,
        )
        new_txt, n2 = safe_sub(
            r"une\s+parcelle\s+cibl[ée]e\s+contenant\s+au\s+moins\s+une\s+souche",
            "une parcelle non rasée (le bonus s’applique à chaque frappe trouvant au moins une Souche sur place à cet instant)",
            new_txt,
        )
        if n1 or n2:
            updated = new_txt
            changes.append("Affût de la Matamata : condition de Souche vérifiée dynamiquement à chaque frappe")

    # 6. L'Écho des Voix Célestes : déclenchement de fin de partie si rang 1 atteint en fin d'Apprentissage
    if "voix celestes" in tile_norm_header or "echo des voix" in tile_norm_header:
        norm_u = strip_accents_lower(updated)
        if ("apprentissage" in norm_u or "egalite" in norm_u) and "repousse finale" not in norm_u and "fin de ce tour" not in norm_u:
            if any(w in norm_u for w in ("avance", "gauche", "cran")):
                updated = (
                    updated.rstrip()
                    + " S’il atteint ainsi l’emplacement 1 en fin d’Apprentissage, la fin de partie se déclenche à la fin de ce tour (Repousse Finale directe)."
                )
                changes.append("Écho des Voix Célestes : déclenchement fin de partie au rang 1 en fin d'Apprentissage")

    # 7. Le Miel des Ancêtres : production hors phase restreinte aux seuls jetons Insecte
    if "miel des ancetres" in tile_norm_header:
        norm_u = strip_accents_lower(updated)
        if "produc" in norm_u and "pouvoir" not in norm_u and "uniquement les jetons" not in norm_u:
            updated = (
                updated.rstrip()
                + " (Génère uniquement le ou les jetons Insecte et allume la case Gardien associée, sans déclencher le pouvoir post-production du Nid.)"
            )
            changes.append("Miel des Ancêtres : restriction aux seuls jetons Insecte hors phase des Nids")

    # 8. Guêpes Cazadores (Pouponnière autonome) : lecture de l'état présent à l'activation du Nid
    if "cazadores" in tile_norm_header or "pouponniere" in tile_norm_header:
        new_txt, n = safe_sub(
            r"au\s+d[ée]but\s+de\s+l['’][ée]tape(?:\s+des\s+nids)?",
            "à l’instant où ce Nid est résolu",
            updated,
        )
        if n:
            updated = new_txt
            changes.append("Guêpes Cazadores : décompte des Insectes à l'instant de la résolution du Nid")

    return updated, changes


def make_face2_autonomous(face1_text: str, face2_text: str, tile_norm_header: str) -> tuple[str, bool]:
    """
    Détecte toute Face 2 non autonome faisant référence au verso caché ('S'applique aussi...',
    'En plus de la face 1...', 'Conserve l'effet...') et la réécrit de manière 100 % autonome.
    """
    if not face1_text or not face2_text:
        return face2_text, False

    norm_f2 = strip_accents_lower(face2_text).strip()
    non_autonomous_markers = (
        "s'applique aussi",
        "s'appliquent aussi",
        "en plus de la face 1",
        "comme en face 1",
        "comme sur la face 1",
        "conserve l'effet de la face 1",
        "garde l'effet de la face 1",
        "meme effet qu'en face 1",
    )

    if not any(marker in norm_f2 for marker in non_autonomous_markers):
        return face2_text, False

    f1_clean = face1_text.strip().rstrip(".")
    f2_clean = face2_text.strip()

    # Cas dédiés de La Piquée de la Harpie et du Guet du Caïman Noir (et tout autre Gardien évolutif)
    f2_complement = re.sub(
        r"^(?:En\s+plus\s+de\s+la\s+face\s*1\s*,?\s*|Comme\s+(?:en|sur\s+la)\s+face\s*1\s*,?\s*)",
        "",
        f2_clean,
        flags=re.IGNORECASE,
    )
    if norm_f2.startswith("s'applique aussi"):
        autonomous = f"{f1_clean}. De plus, cet effet {f2_complement[0].lower() + f2_complement[1:]}"
    else:
        autonomous = f"{f1_clean}. {f2_complement}"

    return autonomous, True


# ============================================================================
# 4. PATCHEUR RÉCURSIF AST POUR `data/catalog_v5_3.json`
# ============================================================================

def infer_peuple_origine(node: dict[str, Any]) -> str | None:
    """Infère ou normalise le `peuple_origine` d'une tuile ou piste si un indice explicite existe."""
    for key in ("peuple_origine", "origine", "peuple", "owner_peuple", "gouverneur"):
        val = node.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()

    # Si une paire est renseignée sous forme "Insectes + Mammifères" ou liste ["Insectes", "Mammifères"],
    # le premier peuple cité dans la nomenclature du studio est par convention l'origine si identifié.
    paire = node.get("paire") or node.get("peuples")
    if isinstance(paire, list) and len(paire) >= 1 and isinstance(paire[0], str):
        return paire[0].strip()

    # Inférence par préfixe d'identifiant de piste de Migration (Insectes)
    raw_id = str(node.get("id") or node.get("code") or "")
    norm_title = strip_accents_lower(str(node.get("nom") or node.get("titre") or node.get("title") or ""))
    if raw_id.upper().startswith("M") or "bug du cerveau" in norm_title or "colonisation" in norm_title:
        return "Insectes"

    return None


def extract_node_header(node: dict[str, Any], inherited_header: str = "") -> str:
    """Construit une signature normalisée du nœud courant (titre/nom/id) pour identifier la tuile."""
    parts: list[str] = [inherited_header] if inherited_header else []
    for k in ("id", "code", "slot_id", "nom", "titre", "title", "name", "label"):
        v = node.get(k)
        if isinstance(v, str) and v.strip():
            parts.append(strip_accents_lower(v))
    return " | ".join(parts)


def patch_json_tree(
    node: Any,
    stats: dict[str, Any],
    inherited_header: str = "",
) -> Any:
    """Parcourt récursivement l'arbre JSON du catalogue pour appliquer tous les patchs."""
    if isinstance(node, list):
        return [patch_json_tree(item, stats, inherited_header) for item in node]

    if isinstance(node, dict):
        current_header = extract_node_header(node, inherited_header)
        out: dict[str, Any] = {}

        # Vérification / enrichissement de `peuple_origine` sur les emplacements de tuiles / migrations
        is_tile_or_track = any(
            k in node for k in ("profils", "profiles", "famille", "categorie", "slot_id", "paire")
        )
        if is_tile_or_track and "peuple_origine" not in node:
            inferred = infer_peuple_origine(node)
            if inferred:
                node = dict(node)
                node["peuple_origine"] = inferred
                stats["peuple_origine_ajoutes"] += 1

        # Autonomisation éventuelle des Faces 2 si Face 1 + Face 2 coexistent dans le même dictionnaire
        f1_keys = [k for k in ("face_1", "face1", "recto", "texte_f1", "effet_f1") if isinstance(node.get(k), str)]
        f2_keys = [k for k in ("face_2", "face2", "verso", "texte_f2", "effet_f2") if isinstance(node.get(k), str)]
        node_work = dict(node)
        if f1_keys and f2_keys:
            k1, k2 = f1_keys[0], f2_keys[0]
            new_f2, changed_f2 = make_face2_autonomous(node_work[k1], node_work[k2], current_header)
            if changed_f2:
                node_work[k2] = new_f2
                stats["faces2_autonomisees"].append(current_header or k2)

        for key, val in node_work.items():
            if isinstance(val, str):
                new_val = val
                # 1. Règles lexicales globales
                for pattern, repl, label in GLOBAL_LEXICAL_RULES:
                    new_val, cnt = safe_sub(pattern, repl, new_val)
                    if cnt:
                        stats["remplacements_globaux_json"] += cnt
                        stats["details_actions"].add(label)

                # 2. Règles chirurgicales liées à la tuile courante
                new_val, tile_changes = patch_tile_text_by_identity(current_header, new_val, field_name=key)
                if tile_changes:
                    stats["tuiles_patchees_json"].update(tile_changes)

                out[key] = new_val
            else:
                out[key] = patch_json_tree(val, stats, current_header)

        if "peuple_origine" in out and isinstance(out["peuple_origine"], str) and out["peuple_origine"].strip():
            stats["peuple_origine_total"] += 1

        return out

    return node


def patch_catalog_json_root(catalog_data: dict[str, Any], stats: dict[str, Any]) -> dict[str, Any]:
    """Met à jour les métadonnées racine et l'arbre complet de `data/catalog_v5_3.json`."""
    patched = patch_json_tree(copy.deepcopy(catalog_data), stats)

    # Consolidation des paramètres châssis v5.3-audit à la racine
    patched["schema_version"] = "5.3.1-audit"
    patched.setdefault("total_emplacements", 30)
    patched.setdefault("total_profils", 100)

    topos = patched.get("topologies")
    if not isinstance(topos, dict):
        topos = {}
    topos.setdefault("P4_2233", [2, 2, 3, 3])
    topos.setdefault("P5_22233", [2, 2, 2, 3, 3])
    patched["topologies"] = topos

    patched["formule_seuil_parade"] = (
        "Seuil imprimé fixe ; parade classique par Défenseurs + défausse immédiate des Insectes "
        "manquants (zéro Insecte engagé, zéro verrouillage des parcelles ciblées). "
        "Chaîne stricte : Bond du Jaguar -> Piquée de la Harpie -> Piège -> Parade classique."
    )
    patched["regle_piege"] = (
        "Embuscade automatique dès que la Défense totale de la parcelle vaut au moins 1 à l'instant "
        "de la frappe (présence locale ou soutien à distance). Tout Piège ayant paré au moins une "
        "frappe durant le tour est retiré à la fin des attaques (et ne peut plus payer de coût "
        "volontaire entre-temps)."
    )
    patched["verification_fin_de_partie"] = (
        "Vérification unique à la fin des attaques (saut de l'Apprentissage et passage direct à la "
        "Repousse Finale), complétée par le déclenchement en fin d'Apprentissage si L'Écho des Voix "
        "Célestes amène son Rêve en case 1. Seuil de Réveil fixe calculé à la mise en place."
    )
    patched["regle_furtivite"] = (
        "4 emplacements par case de Furtivité (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs). "
        "Entrer sur la case (quelle que soit la face) tire l'éventuel autre Défenseur sur l'emplacement "
        "jumeau et oriente l'action unique du binôme ; retourner de réflexion à choix définitif se fait "
        "strictement sur place sans déplacement."
    )
    patched["gouvernance_autorite"] = (
        "Autorité unitaire par Peuple d'origine (tuiles de Synergie et pistes de Migration) ; "
        "cartes Sabotage visibles gouvernées par les Humains (ou l'acquéreur en leur absence)."
    )
    patched["spec_formelle_v5_3"] = SPEC_FORMELLE_V5_3

    return patched


# ============================================================================
# 5. DÉCOUPEUR D'OBJETS JS ÉQUILIBRÉS ET PATCHEUR `data/amazonia_data_v5_3.js`
# ============================================================================

def iter_top_level_js_objects(js_slice: str) -> list[tuple[int, int]]:
    """
    Repère les bornes `(start, end)` des blocs `{ ... }` de premier niveau dans un tableau
    ou objet JavaScript (en ignorant chaînes `'...'`, `"..."`, templates `` `...` `` et commentaires).
    """
    spans: list[tuple[int, int]] = []
    i = 0
    n = len(js_slice)
    depth = 0
    block_start = -1
    in_quote: str | None = None

    while i < n:
        ch = js_slice[i]

        # Commentaires ligne / bloc hors chaîne
        if in_quote is None:
            if ch == "/" and i + 1 < n and js_slice[i + 1] == "/":
                nl = js_slice.find("\n", i + 2)
                i = n if nl == -1 else nl + 1
                continue
            if ch == "/" and i + 1 < n and js_slice[i + 1] == "*":
                end_c = js_slice.find("*/", i + 2)
                i = n if end_c == -1 else end_c + 2
                continue

        if in_quote is not None:
            if ch == "\\":
                i += 2
                continue
            if ch == in_quote:
                in_quote = None
            i += 1
            continue

        if ch in ("'", '"', "`"):
            in_quote = ch
        elif ch == "{":
            if depth == 0:
                block_start = i
            depth += 1
        elif ch == "}":
            if depth > 0:
                depth -= 1
                if depth == 0 and block_start != -1:
                    spans.append((block_start, i + 1))
                    block_start = -1
        i += 1

    return spans


def find_js_variable_span(js_text: str, var_name: str) -> tuple[int, int] | None:
    """
    Trouve l'intervalle `[start, end)` de la valeur assignée à `var_name` (ex. `CATALOGUE_TUILES = [...]`).
    """
    m = re.search(rf"\b(?:const|let|var|window\.)\s*{re.escape(var_name)}\s*=\s*([\[{{])", js_text)
    if not m:
        return None

    open_pos = m.start(1)
    open_ch = m.group(1)
    close_ch = "]" if open_ch == "[" else "}"
    i = open_pos
    n = len(js_text)
    depth = 0
    in_quote: str | None = None

    while i < n:
        ch = js_text[i]
        if in_quote is None:
            if ch == "/" and i + 1 < n and js_text[i + 1] == "/":
                nl = js_text.find("\n", i + 2)
                i = n if nl == -1 else nl + 1
                continue
            if ch == "/" and i + 1 < n and js_text[i + 1] == "*":
                end_c = js_text.find("*/", i + 2)
                i = n if end_c == -1 else end_c + 2
                continue
            if ch in ("'", '"', "`"):
                in_quote = ch
            elif ch == open_ch:
                depth += 1
            elif ch == close_ch:
                depth -= 1
                if depth == 0:
                    return (open_pos, i + 1)
        else:
            if ch == "\\":
                i += 2
                continue
            if ch == in_quote:
                in_quote = None
        i += 1

    return None


def patch_js_Autonomous_face2_in_block(block_text: str, norm_block: str, stats: dict[str, Any]) -> str:
    """
    Rend autonomes les Faces 2 dans un bloc d'objet JS (ex. La Piquée de la Harpie, Le Guet du Caïman Noir)
    lorsque `face_1`/`face1` et `face_2`/`face2` figurent côte à côte sous forme de chaînes.
    """
    pair_pattern = re.compile(
        r'(?P<k1>["\']?(?:face_1|face1|recto|effet_f1)["\']?\s*:\s*)(?P<q1>["\'])(?P<v1>(?:\\.|(?!(?P=q1)).)*)(?P=q1)'
        r'(?P<mid>[\s\S]{0,400}?)'
        r'(?P<k2>["\']?(?:face_2|face2|verso|effet_f2)["\']?\s*:\s*)(?P<q2>["\'])(?P<v2>(?:\\.|(?!(?P=q2)).)*)(?P=q2)'
    )

    def _repl(m: re.Match[str]) -> str:
        v1 = m.group("v1")
        v2 = m.group("v2")
        new_v2, changed = make_face2_autonomous(v1, v2, norm_block[:80])
        if not changed:
            return m.group(0)
        q2 = m.group("q2")
        if q2 == "'":
            new_v2 = new_v2.replace("\\'", "'").replace("'", "\\'")
        elif q2 == '"':
            new_v2 = new_v2.replace('\\"', '"').replace('"', '\\"')
        stats["faces2_autonomisees_js"] += 1
        return f"{m.group('k1')}{m.group('q1')}{v1}{m.group('q1')}{m.group('mid')}{m.group('k2')}{q2}{new_v2}{q2}"

    return pair_pattern.sub(_repl, block_text)


def patch_amazonia_js(js_source: str, stats: dict[str, Any]) -> str:
    """
    Applique l'ensemble des patchs v5.3-audit sur `data/amazonia_data_v5_3.js`
    en garantissant l'intégrité absolue des interpolations `${...}`.
    """
    protected, interp_tokens = protect_js_interpolations(js_source)
    stats["js_interpolations_protegees"] = len(interp_tokens)

    # 1. Patch chirurgical bloc par bloc dans CATALOGUE_TUILES s'il est présent
    cat_span = find_js_variable_span(protected, "CATALOGUE_TUILES")
    if cat_span is not None:
        c_start, c_end = cat_span
        cat_body = protected[c_start:c_end]
        obj_spans = iter_top_level_js_objects(cat_body)
        if obj_spans:
            rebuilt_parts: list[str] = []
            cursor = 0
            for b_start, b_end in obj_spans:
                rebuilt_parts.append(cat_body[cursor:b_start])
                block = cat_body[b_start:b_end]
                norm_block = strip_accents_lower(block)

                # Autonomisation Face 2 -> Face 1 si nécessaire
                block = patch_js_Autonomous_face2_in_block(block, norm_block, stats)

                # Patchs ciblés par identité de tuile
                block, t_changes = patch_tile_text_by_identity(norm_block, block, field_name="js_tile_block")
                if t_changes:
                    stats["tuiles_patchees_js"].update(t_changes)

                rebuilt_parts.append(block)
                cursor = b_end
            rebuilt_parts.append(cat_body[cursor:])
            protected = protected[:c_start] + "".join(rebuilt_parts) + protected[c_end:]

    # 2. Règles lexicales globales sur tout le fichier JS (livret didactique + axes + tuiles)
    for pattern, repl, label in GLOBAL_LEXICAL_RULES:
        protected, cnt = safe_sub(pattern, repl, protected)
        if cnt:
            stats["remplacements_globaux_js"] += cnt
            stats["details_actions"].add(label)

    # 3. Export / mise à jour idempotente de SPEC_FORMELLE_V5_3 en fin de fichier JS
    spec_json_str = json.dumps(SPEC_FORMELLE_V5_3, ensure_ascii=False, indent=2)
    spec_js_banner = (
        "// === BEGIN SPEC_FORMELLE_V5_3 (auto-generated by build_v5_3_audit.py) ===\n"
        f"const SPEC_FORMELLE_V5_3 = {spec_json_str};\n"
        'if (typeof window !== "undefined") {\n'
        "  window.SPEC_FORMELLE_V5_3 = SPEC_FORMELLE_V5_3;\n"
        "}\n"
        "// === END SPEC_FORMELLE_V5_3 ===\n"
    )

    marker_re = re.compile(
        r"// === BEGIN SPEC_FORMELLE_V5_3.*?// === END SPEC_FORMELLE_V5_3 ===\n?",
        flags=re.DOTALL,
    )
    if marker_re.search(protected):
        protected, _ = safe_sub(
            r"// === BEGIN SPEC_FORMELLE_V5_3.*?// === END SPEC_FORMELLE_V5_3 ===\n?",
            spec_js_banner,
            protected,
            flags=re.DOTALL,
        )
    else:
        protected = protected.rstrip() + "\n\n" + spec_js_banner

    # 4. Restauration intégrale des interpolations `${...}` et vérification de cardinalité
    restored = restore_js_interpolations(protected, interp_tokens)
    _, post_tokens = protect_js_interpolations(restored)
    if post_tokens != interp_tokens:
        raise RuntimeError(
            f"Alerte sécurité : divergence sur les interpolations JS "
            f"(avant={len(interp_tokens)}, après={len(post_tokens)}). Écriture annulée."
        )

    return restored


# ============================================================================
# 6. SUITE D'AUTO-VÉRIFICATION POST-BUILD
# ============================================================================

FORBIDDEN_RESIDUES: list[tuple[str, str]] = [
    (r"insectes?\s+engag[ée]s?", "Concept obsolète 'Insecte engagé'"),
    (r"dette\s+d['’]insectes?", "Concept obsolète 'dette d'Insectes'"),
    (r"parcelles?\s+verrouill[ée]es?", "Concept obsolète 'parcelle verrouillée'"),
    (r"lev[ée]e\s+du\s+verrouillage", "Concept obsolète 'levée du verrouillage'"),
    (r"verrouillage\s+des\s+parcelles", "Concept obsolète 'verrouillage des parcelles'"),
    (r"exige[_\s]+pr[ée]sence[_\s]+locale", "Label obsolète 'exige présence locale'"),
    (r"ne\s+modifie\s+pas\s+les\s+cibles", "Note obsolète de cibles figées (Anaconda)"),
]


def run_verification_suite(
    catalog_text: str | None,
    js_text: str | None,
    spec_text: str,
) -> list[str]:
    """Vérifie les invariants formels sur les artefacts générés. Retourne la liste d'anomalies."""
    issues: list[str] = []

    # 1. Validité JSON de spec_formelle_v5_3.json
    try:
        spec_obj = json.loads(spec_text)
        if len(spec_obj.get("arbitrages_valides", {})) != 25:
            issues.append("spec_formelle_v5_3.json ne contient pas exactement 25 arbitrages.")
        if len(spec_obj.get("etapes_tour", [])) != 6:
            issues.append("spec_formelle_v5_3.json ne contient pas exactement 6 étapes de tour.")
    except Exception as exc:
        issues.append(f"JSON invalide dans spec_formelle_v5_3.json : {exc}")

    # 2. Validité JSON et résidus dans catalog_v5_3.json
    if catalog_text is not None:
        try:
            cat_obj = json.loads(catalog_text)
            topos = cat_obj.get("topologies", {})
            if "P4_2233" not in topos or "P5_22233" not in topos:
                issues.append("Topologies P4_2233 / P5_22233 absentes de catalog_v5_3.json.")
        except Exception as exc:
            issues.append(f"JSON invalide dans catalog_v5_3.json : {exc}")

        # Scan hors bloc spec_formelle_v5_3 (qui mentionne "zéro Insecte engagé" en négatif)
        cat_without_spec = json.dumps(
            {k: v for k, v in json.loads(catalog_text).items() if k != "spec_formelle_v5_3"},
            ensure_ascii=False,
        )
        cat_without_negations = re.sub(
            r"z[ée]ro\s+(?:insecte\s+engag[ée]|verrouillage\s+des\s+parcelles(?:\s+cibl[ée]es)?)",
            "",
            cat_without_spec,
            flags=re.IGNORECASE,
        )
        for pattern, desc in FORBIDDEN_RESIDUES:
            m = re.search(pattern, cat_without_negations, flags=re.IGNORECASE)
            if m:
                issues.append(f"[catalog_v5_3.json] Résidu détecté ({desc}) : « {m.group(0)} »")

    # 3. Scan des résidus dans amazonia_data_v5_3.js (hors bannière SPEC_FORMELLE_V5_3 et négations explicites)
    if js_text is not None:
        js_core = re.sub(
            r"// === BEGIN SPEC_FORMELLE_V5_3.*?// === END SPEC_FORMELLE_V5_3 ===",
            "",
            js_text,
            flags=re.DOTALL,
        )
        js_core = re.sub(
            r"(?:z[ée]ro|sans|aucun)\s+(?:insectes?\s+engag[ée]s?|verrouillage\s+des\s+parcelles(?:\s+cibl[ée]es)?)",
            "",
            js_core,
            flags=re.IGNORECASE,
        )
        for pattern, desc in FORBIDDEN_RESIDUES:
            m = re.search(pattern, js_core, flags=re.IGNORECASE)
            if m:
                issues.append(f"[amazonia_data_v5_3.js] Résidu détecté ({desc}) : « {m.group(0)} »")

        if "__AMAZONIA_JS_INTERP_" in js_text:
            issues.append("[amazonia_data_v5_3.js] Sentinelle d'interpolation non restaurée !")

    return issues


# ============================================================================
# 7. POINT D'ENTRÉE CLI ET SAUVEGARDE SÉCURISÉE
# ============================================================================

def detect_repo_root(explicit_root: str | None) -> Path:
    """Détecte automatiquement la racine du dépôt `amazonia-doc-studio`."""
    if explicit_root:
        return Path(explicit_root).resolve()
    script_dir = Path(__file__).resolve().parent
    if (script_dir.parent / "data").is_dir() or (script_dir.parent / "index.html").is_file():
        return script_dir.parent
    return Path.cwd().resolve()


def backup_file(path: Path, backup_dir: Path, timestamp: str) -> Path:
    """Crée une copie de sauvegarde horodatée avant écriture."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    target = backup_dir / f"{path.name}.{timestamp}.bak"
    shutil.copy2(path, target)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Applique la consolidation d'audit v5.3 (25 arbitrages + correctifs) sur Amazonia Doc Studio."
    )
    parser.add_argument("--root", type=str, default=None, help="Chemin racine du dépôt (auto-détecté par défaut).")
    parser.add_argument("--dry-run", action="store_true", help="Exécute l'audit et affiche le bilan sans écrire sur le disque.")
    parser.add_argument("--no-backup", action="store_true", help="Désactive la création de sauvegardes dans data/.backups/.")
    parser.add_argument("--strict", action="store_true", help="Retourne un code de sortie 1 si un résidu subsiste.")
    args = parser.parse_args(argv)

    root = detect_repo_root(args.root)
    data_dir = root / "data"
    catalog_path = data_dir / "catalog_v5_3.json"
    js_path = data_dir / "amazonia_data_v5_3.js"
    spec_out_path = data_dir / "spec_formelle_v5_3.json"

    stats: dict[str, Any] = {
        "remplacements_globaux_json": 0,
        "remplacements_globaux_js": 0,
        "tuiles_patchees_json": set(),
        "tuiles_patchees_js": set(),
        "faces2_autonomisees": [],
        "faces2_autonomisees_js": 0,
        "peuple_origine_ajoutes": 0,
        "peuple_origine_total": 0,
        "js_interpolations_protegees": 0,
        "details_actions": set(),
    }

    print(f"=== Consolidation Amazonia Doc Studio v5.3-audit ===")
    print(f"Racine détectée : {root}")
    print(f"Mode            : {'DRY-RUN (aucune écriture)' if args.dry_run else 'APPLY (écriture sur disque)'}\n")

    patched_catalog_str: str | None = None
    patched_js_str: str | None = None
    spec_str = json.dumps(SPEC_FORMELLE_V5_3, ensure_ascii=False, indent=2) + "\n"

    # Traitement de data/catalog_v5_3.json
    if catalog_path.is_file():
        raw_catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
        patched_catalog = patch_catalog_json_root(raw_catalog, stats)
        patched_catalog_str = json.dumps(patched_catalog, ensure_ascii=False, indent=2) + "\n"
        print(f"[OK] Lu et patché en mémoire : {catalog_path.relative_to(root)}")
    else:
        print(f"[INFO] Fichier absent (ignoré) : {catalog_path}")

    # Traitement de data/amazonia_data_v5_3.js
    if js_path.is_file():
        raw_js = js_path.read_text(encoding="utf-8")
        patched_js_str = patch_amazonia_js(raw_js, stats)
        print(f"[OK] Lu et patché en mémoire : {js_path.relative_to(root)}")
    else:
        print(f"[INFO] Fichier absent (ignoré) : {js_path}")

    # Vérification automatique avant écriture
    issues = run_verification_suite(patched_catalog_str, patched_js_str, spec_str)

    # Écriture sur disque (sauf --dry-run)
    if not args.dry_run:
        data_dir.mkdir(parents=True, exist_ok=True)
        ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = data_dir / ".backups"

        if patched_catalog_str is not None:
            if not args.no_backup and catalog_path.is_file():
                b_cat = backup_file(catalog_path, backup_dir, ts)
                print(f"[BACKUP] {b_cat.relative_to(root)}")
            catalog_path.write_text(patched_catalog_str, encoding="utf-8", newline="\n")
            print(f"[WRITE]  {catalog_path.relative_to(root)}")

        if patched_js_str is not None:
            if not args.no_backup and js_path.is_file():
                b_js = backup_file(js_path, backup_dir, ts)
                print(f"[BACKUP] {b_js.relative_to(root)}")
            js_path.write_text(patched_js_str, encoding="utf-8", newline="\n")
            print(f"[WRITE]  {js_path.relative_to(root)}")

        spec_out_path.write_text(spec_str, encoding="utf-8", newline="\n")
        print(f"[WRITE]  {spec_out_path.relative_to(root)}")

    # Rapport synthétique
    print("\n--- Bilan des transformations ---")
    print(f"• Interpolations JS protégées/vérifiées : {stats['js_interpolations_protegees']}")
    print(f"• Remplacements lexicaux (JSON / JS)    : {stats['remplacements_globaux_json']} / {stats['remplacements_globaux_js']}")
    print(f"• Faces 2 rendues autonomes (JSON / JS) : {len(stats['faces2_autonomisees'])} / {stats['faces2_autonomisees_js']}")
    print(f"• Champs peuple_origine (ajoutés/total) : {stats['peuple_origine_ajoutes']} / {stats['peuple_origine_total']}")

    all_tile_patches = sorted(stats["tuiles_patchees_json"] | stats["tuiles_patchees_js"])
    if all_tile_patches:
        print("• Ajustements chirurgicaux appliqués sur les tuiles :")
        for item in all_tile_patches:
            print(f"    - {item}")

    if issues:
        print("\n--- Alertes d'auto-vérification ---")
        for issue in issues:
            print(f"  [!] {issue}")
        if args.strict:
            return 1
    else:
        print("\n[SUCCÈS] Tous les contrôles d'intégrité (JSON, interpolations JS, zéro résidu banni) sont verts.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())