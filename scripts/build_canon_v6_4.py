"""Générateur déterministe du Catalogue Canonique v6.4 (Passe 2 — 30 Tuiles affinées).

Lit `contracts/tiles_canon_v6_3.json` en lecture seule (archive Passe 1 sanctuarisée),
applique la consolidation mécanique et la charte éditoriale Passe 2 définies dans
`docs/cadrage_v6_4.md`, valide à 0 erreur stricte via `validate_tiles_canon_v6_4` et
`audit_tiles_catalog_197`, puis écrit :
- `contracts/tiles_canon_v6_4.json`
- `docs/panel_canon_v6_4.md`
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_197 import audit_tiles_catalog_197
from scripts.tiles_v6_3_schema import (
    DEFAULT_REFERENTIEL_PICTOGRAMMES_V6_4,
    LOCKED_GARDIEN_CASTING_V6_3,
    MURS_PORTEURS_V6_3,
    SLOTS_SPEC_30,
    V6_3_CONTRACT_PATH,
    V6_4_CONTRACT_PATH,
    validate_tiles_canon_v6_4,
)

PANEL_MD_V6_4_PATH = ROOT / "docs" / "panel_canon_v6_4.md"

PEUPLE_NAMES: dict[str, str] = {
    "H": "Humains",
    "E": "Entités",
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


def _typo(text: str | None) -> str | None:
    if text is None:
        return None
    out = text.replace("'", "’").strip()
    if out.startswith("«") and out.endswith("»"):
        out = out[1:-1].strip()
    return out


def _build_v6_4_overrides() -> dict[str, dict[str, Any]]:
    """Spécification complète Passe 2 v6.4 des 30 tuiles (13 alignées + 17 greffées/allégées)."""
    return {
        # ------------------------------------------------------------------
        # GARDIENS (G1 .. G15)
        # ------------------------------------------------------------------
        "G1": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["DUEL", "CROC"],
            "entrees_synergie": ["ROUGE"],
            "sorties": ["CROC_POSTE", "CROC", "TERRITOIRE", "BLEU"],
            "declencheurs_amorces": ["ICONE_PIEGEAGE"],
            "vecteurs": "Duel (M) + Croc (R) → embuscade sur la parcelle du Duel → Piégeage en cascade · Face 2 : Refroidit la machine parée",
            "double_ouverture": (
                "Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume "
                "Piégeage (l’icône du Jaguar) et retourne le Duel sur Territoire tenu (règle native), "
                "ouvrant une seconde activation qui reposte aussitôt le Croc pour la frappe suivante."
            ),
            "tuile_plateau": {
                "nom_court": "Le Jaguar",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PIEGEAGE",
                "pictogrammes": ["PIC_CROC", "PIC_DUEL", "PIC_BLEU"],
                "mots_cles_plateau": {
                    "face_1": "Croc → parcelle du Duel · sinon Duel sur parcelle ciblée puis Croc dessus",
                    "face_2": "Croc (+ Duel) → toute parcelle ciblée · parade du Croc = Refroidir 1 Rouge",
                    "enracine": None,
                },
                "resume_plateau": "Poste le Croc aux côtés du Duel",
            },
            "carte_joueur": {
                "titre_complet": "Le Jaguar, seigneur des berges",
                "texte_regle": {
                    "face_1": (
                        "Prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et posez-le sur "
                        "la parcelle du jeton Duel. Si le Duel est en réserve, posez d’abord le Duel "
                        "face Défi sur une parcelle ciblée de votre choix, puis posez le Croc dessus."
                    ),
                    "face_2": (
                        "Même effet, mais vous pouvez poser le Croc — et, au choix, déplacer le Duel "
                        "avec lui en conservant sa face — sur n’importe quelle parcelle ciblée du "
                        "plateau. Chaque fois que le Croc pare une attaque à ce tour, Refroidissez "
                        "cette machine si elle porte au moins 1 jeton Rouge."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Poste le Croc sur la parcelle du Duel (ou sur toute cible en Face 2) et Refroidit l’attaquante.",
                    "renoncement": "Mobilise l’unique Croc sur une seule parcelle ; le Croc n’est plus libre pour les pontes ou une autre embuscade tant qu’il n’a pas paré.",
                },
            },
            "temoins": [
                {
                    "id": "G1_T1",
                    "statut": "A_CODER",
                    "resume": "Duel face Défi sur M·2 ; Jaguar F1 pose le Croc (pris en réserve Reptile) sur M·2 ; la frappe parée par le Croc allume Piégeage et retourne nativement le Duel sur Territoire tenu.",
                },
                {
                    "id": "G1_T2",
                    "statut": "A_CODER",
                    "resume": "Jaguar F2 déplace Duel + Croc sur une parcelle ciblée d’un rayon voisin ; la machine parée par le Croc est immédiatement Refroidie (1 Rouge → Bleu).",
                },
            ],
            "heuristique_bot": "Prioritaire dès qu’une parcelle ciblée porte le Duel ou une attaque à fort Seuil ; en Face 2, combine Piégeage en boucle et Refroidissement sur machine chargée.",
        },
        "G2": {
            "roles_portes": ["TWIST_2K3"],
            "est_twist": True,
            "paiement": [],
            "entrees_plancher": ["RATISSAGE", "DUEL"],
            "entrees_synergie": ["TERRITOIRE"],
            "sorties": ["RATISSAGE_ROMPU", "RECUL", "ANNULATION"],
            "declencheurs_amorces": [],
            "vecteurs": "Territoire tenu ou 2 Défenseurs → machine arrachée au Ratissage (jeton au sac + Reculer) · Face 2 : Étouffer et Reculer une mobile",
            "double_ouverture": (
                "Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la dernière "
                "parcelle : deux activations arrachent successivement l’Abatteuse puis le Bulldozer, "
                "ou combinent arrachage et Étouffement d’une mobile en Face 2."
            ),
            "tuile_plateau": {
                "nom_court": "L’Anaconda vert",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PARADE",
                "pictogrammes": ["PIC_TWIST", "PIC_DUEL", "PIC_RECUL", "PIC_ANNULATION"],
                "mots_cles_plateau": {
                    "face_1": "Ratissage sur Territoire tenu OU 2 Défenseurs → jeton au sac · Reculer 1",
                    "face_2": "Duel OU 2 Défenseurs → rompt Ratissage OU Étouffe et Recule 1 mobile",
                    "enracine": None,
                },
                "resume_plateau": "Arrache une machine à son Ratissage",
            },
            "carte_joueur": {
                "titre_complet": "L’Anaconda vert, l’étau des eaux dormantes",
                "texte_regle": {
                    "face_1": (
                        "Choisissez une machine en Ratissage dont la parcelle porte le Duel sur sa face "
                        "Territoire tenu ou au moins 2 Défenseurs : elle quitte immédiatement son "
                        "Ratissage, son jeton Machine retourne dans le sac opaque (elle perd son "
                        "éventuel jeton Rouge de Ratissage s’il peut être retiré, en conservant ses "
                        "autres jetons), et vous la faites Reculer d’1 parcelle vers la bordure. "
                        "S’il n’y a aucune machine en Ratissage éligible, choisissez une machine mobile "
                        "visant la parcelle du Duel ou une parcelle portant au moins 2 Défenseurs et "
                        "faites-la Reculer d’1 parcelle."
                    ),
                    "face_2": (
                        "Même effet dès que la parcelle porte le Duel (quelle que soit sa face) ou au "
                        "moins 2 Défenseurs ; de plus, vous pouvez choisir à la place une machine mobile "
                        "active visant cette parcelle pour l’Étouffer et la faire Reculer d’1 parcelle "
                        "vers la bordure."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Rompt un Ratissage (ou fait Reculer / Étouffe une machine mobile sur parcelle verrouillée).",
                    "renoncement": "Remet le jeton Machine dans le sac opaque et exige de concentrer 2 Défenseurs ou le Duel sur la parcelle menacée.",
                },
            },
            "temoins": [
                {
                    "id": "G2_T1",
                    "statut": "A_CODER",
                    "resume": "Abatteuse en Ratissage sur la dernière parcelle portant Territoire tenu : Anaconda F1 la sort du Ratissage, remet son jeton au sac et la fait Reculer d’1 parcelle.",
                },
                {
                    "id": "G2_T2",
                    "statut": "A_CODER",
                    "resume": "Anaconda F2 sur une mobile active visant la parcelle du Duel : la machine est Étouffée (jeton à 90°, dé retiré) et Recule d’1 parcelle.",
                },
            ],
            "heuristique_bot": "Prioritaire dès qu’une machine entre en Ratissage sur une parcelle défendue ou tenue par le Duel ; en Face 2, neutralise directement la mobile la plus dangereuse.",
        },
        "G3": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["ARBRE", "ROUTE", "DEFENSEUR_REDEPLOYE"],
            "entrees_synergie": ["PERCHOIR"],
            "sorties": ["DEFENSEUR_REDEPLOYE"],
            "declencheurs_amorces": ["ICONE_PARADE"],
            "vecteurs": "Arbres debout + Routes + Perchoir (O) → traversée haute et Saut de lisière (Rive ↔ Arbre) → redéploiement instantané de Parade",
            "double_ouverture": (
                "Deux traversées amènent les deux Défenseurs nécessaires à une Parade décisive, ou "
                "basculent un pion d’une Rive de Furtivité vers le cœur puis un autre vers une Rive."
            ),
            "tuile_plateau": {
                "nom_court": "L’Atèle",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_SABOTAGE",
                "pictogrammes": ["PIC_ARBRE", "PIC_ROUTE", "PIC_DEFENSEUR", "PIC_PERCHOIR"],
                "mots_cles_plateau": {
                    "face_1": "2 cimes même profondeur (M ↔ O) OU Rive ↔ cime · 1 pas avant",
                    "face_2": "Rayon du Perchoir ↔ voisins · Rive ↔ cime · 1 pas avant et après",
                    "enracine": None,
                },
                "resume_plateau": "Fait traverser un Défenseur par la cime",
            },
            "carte_joueur": {
                "titre_complet": "L’Atèle, acrobate des hautes cimes",
                "texte_regle": {
                    "face_1": (
                        "Déplacez 1 Défenseur entre deux parcelles de même profondeur portant un Arbre "
                        "debout, situées sur le rayon Mammifères et le rayon Oiseaux (en sautant les "
                        "Routes intermédiaires). Avant la traversée, ce Défenseur peut faire 1 pas sur "
                        "son rayon de départ. Saut de lisière : l’une des deux extrémités (départ ou "
                        "arrivée) peut être une Rive de Furtivité de ces deux rayons, l’autre devant "
                        "rester une parcelle portant un Arbre debout."
                    ),
                    "face_2": (
                        "Même effet entre le rayon désigné par le Perchoir de Vigie (ou le rayon "
                        "Oiseaux si le Perchoir pointe un rang) et l’un de ses rayons voisins, avec "
                        "jusqu’à 1 pas avant la traversée et 1 pas après (y compris en Saut de lisière "
                        "depuis ou vers une Rive de Furtivité de ces rayons)."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Redéploie un Défenseur entre rayons ou entre une Rive de Furtivité et la canopée pour compléter une Parade ou une Rive.",
                    "renoncement": "Quitter une Rive ou un rayon fragilise la défense ou le contrôle de Furtivité laissé derrière soi.",
                },
            },
            "temoins": [
                {
                    "id": "G3_T1",
                    "statut": "A_CODER",
                    "resume": "Saut de lisière F1 : un Défenseur sur la Rive Sabotage de O traverse directement sur une parcelle à Arbre debout de M pour compléter une Parade.",
                },
                {
                    "id": "G3_T2",
                    "statut": "A_CODER",
                    "resume": "Atèle F2 avec Perchoir au pied d’un rayon voisin : 1 pas avant, traversée entre cimes, puis 1 pas après pour atteindre exactement la parcelle menacée.",
                },
            ],
            "heuristique_bot": "Évalue chaque Défenseur excédentaire ou sur Rive déjà gagnée/perdue pour compléter une Parade à manque de 1 ou sécuriser une Rive 2/2.",
        },
        "G4": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["GARDIEN"],
            "entrees_synergie": ["TERRITOIRE"],
            "sorties": ["PARI_GLISSE", "ACTIVATION_RELAIS", "DEFI"],
            "declencheurs_amorces": ["ICONE_RESONANCE"],
            "vecteurs": "Pari Gardien → glissement en encoche (F1) ou activation en relais (F2) · Second cri gratuit sur icône voisine OU Territoire tenu → Défi",
            "double_ouverture": (
                "Deux activations font boucler un Gardien à 2 paris sur une icône silencieuse ou "
                "déclenchent un relais en chaîne en Face 2 ; dès qu’une activation vide le dernier "
                "pari d’un Gardien en Face 2, la Résonance se déclenche."
            ),
            "tuile_plateau": {
                "nom_court": "L’Ara rouge",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_RESONANCE",
                "pictogrammes": ["PIC_PARI_ENCOCHE", "PIC_RESONANCE", "PIC_DUEL"],
                "mots_cles_plateau": {
                    "face_1": "1 pari tiers → encoche · Second cri si icône voisine OU Territoire → Défi",
                    "face_2": "Active 1 Gardien tiers avec pari · Second cri si icône voisine OU Territoire → Défi",
                    "enracine": None,
                },
                "resume_plateau": "Fait avancer ou réveille d’autres Gardiens",
            },
            "carte_joueur": {
                "titre_complet": "L’Ara rouge, sentinelle de la collpa",
                "texte_regle": {
                    "face_1": (
                        "Glissez 1 pari d’un autre Gardien en piste dans son encoche libre (sans "
                        "déclencher son pouvoir ni allumer la Résonance). Second cri : si ce premier "
                        "Gardien siège sur une icône directement voisine de celle de l’Ara rouge sur "
                        "la Piste — ou si vous retournez le jeton Duel de sa face Territoire tenu sur "
                        "sa face Défi —, répétez cet effet sur un second Gardien (ou une seconde fois "
                        "sur le même). Sentinelle seule : s’il n’y a aucun autre Gardien avec pari en "
                        "piste, glissez aussitôt un second pari de l’Ara rouge lui-même dans son "
                        "encoche."
                    ),
                    "face_2": (
                        "Activez immédiatement en relais 1 autre Gardien en piste portant au moins "
                        "1 pari (il glisse 1 pari en encoche et résout son pouvoir, pouvant allumer "
                        "la Résonance s’il glisse ainsi son dernier pari). Le Second cri (gratuit sur "
                        "une icône directement voisine de l’Ara rouge, ou en retournant Territoire tenu "
                        "sur Défi) et le repli Sentinelle seule s’appliquent à l’identique."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Sécurise (F1) ou réveille en relais (F2) jusqu’à deux Gardiens ; récompense le placement sur des icônes voisines ou la dépense de Territoire tenu.",
                    "renoncement": "En Face 1, sécuriser un pari renonce au pouvoir actif de ce Gardien et ne déclenche pas la Résonance.",
                },
            },
            "temoins": [
                {
                    "id": "G4_T1",
                    "statut": "A_CODER",
                    "resume": "Ara F1 sur Résonance (position 6) choisit un Gardien sur Insecte (position 5, directement voisine) : 1 pari glisse sans pouvoir ni Résonance, et Second cri est gratuit pour un second Gardien.",
                },
                {
                    "id": "G4_T2",
                    "statut": "A_CODER",
                    "resume": "Ara F2 active en relais un Gardien sur son dernier pari : ce Gardien résout son pouvoir, vide son dessus et allume Résonance.",
                },
            ],
            "heuristique_bot": "Maximise le taux de passage Face 2 des Gardiens en piste ; privilégie un premier choix sur une icône adjacente à l’Ara pour obtenir le Second cri gratuitement.",
        },
        "G5": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["PERCHOIR"],
            "entrees_synergie": ["BLEU"],
            "sorties": ["PIEGE", "CROC"],
            "declencheurs_amorces": ["ICONE_PIEGEAGE"],
            "vecteurs": "Perchoir de Vigie (O) → Piège sur la zone guettée (sinon R ou O) · Bleu bu → Croc (F1) ou second plongeon (F2) → Piégeage en boucle",
            "double_ouverture": (
                "Chaque Piège ou Croc qui pare allume Piégeage (l’icône de l’Iguane) : deux chutes "
                "couvrent les deux parcelles d’un En avançant, ou boivent un Bleu pour déclencher "
                "Croc ou double plongeon."
            ),
            "tuile_plateau": {
                "nom_court": "L’Iguane vert",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PIEGEAGE",
                "pictogrammes": ["PIC_PIEGE", "PIC_PERCHOIR", "PIC_CROC", "PIC_BLEU"],
                "mots_cles_plateau": {
                    "face_1": "Piège sur cible du Perchoir (sinon R OU O) · Bleu bu = Croc aussi",
                    "face_2": "Piège + Croc partout · Bleu bu = second plongeon",
                    "enracine": None,
                },
                "resume_plateau": "Tombe en Piège sous le Perchoir",
            },
            "carte_joueur": {
                "titre_complet": "L’Iguane vert, dormeur des hautes branches",
                "texte_regle": {
                    "face_1": (
                        "Posez 1 Piège ordinaire disponible sur une parcelle ciblée libre de Piège "
                        "désignée par le Perchoir de Vigie (sur son rayon s’il est au pied d’un rayon, "
                        "ou sur une parcelle visée par une machine du rang qu’il pointe ; à défaut, sur "
                        "le rayon Reptiles ou le rayon Oiseaux). Si cette machine porte au moins 1 jeton "
                        "Bleu Surchauffe, vous pouvez en défausser 1 (l’Iguane boit la fraîcheur) pour "
                        "poser aussi le Croc disponible depuis la réserve Reptile sur une autre "
                        "parcelle ciblée de votre choix."
                    ),
                    "face_2": (
                        "Même effet sur n’importe quelle parcelle ciblée du plateau, et vous posez "
                        "aussi le Croc disponible sur une seconde parcelle ciblée. Si vous buvez "
                        "1 jeton Bleu d’une machine visée, résolvez un second plongeon (1 Piège "
                        "supplémentaire sur une autre parcelle ciblée libre)."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Pose un Piège chirurgical guidé par le Perchoir et peut convertir un Bleu ennemi en Croc (F1) ou en double plongeon (F2).",
                    "renoncement": "Boire un Bleu rend sa pleine puissance à la machine qui le portait si elle survit au piégeage.",
                },
            },
            "temoins": [
                {
                    "id": "G5_T1",
                    "statut": "A_CODER",
                    "resume": "Perchoir pointant le rang 4 : Iguane F1 pose 1 Piège sur la parcelle ciblée par la machine du rang 4 ; si elle porte un Bleu, boire ce Bleu pose aussi le Croc de la réserve.",
                },
                {
                    "id": "G5_T2",
                    "statut": "A_CODER",
                    "resume": "Iguane F2 pose Piège + Croc sur deux parcelles ciblées de son choix, puis boit 1 Bleu pour effectuer un second plongeon.",
                },
            ],
            "heuristique_bot": "Cible les parcelles à plus fort Seuil sans Défenseur ; boit un Bleu uniquement sur une machine déjà piégée ou facile à parer afin de multiplier les déclenchements de Piégeage.",
        },
        "G6": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["ROUGE", "PERCHOIR"],
            "entrees_synergie": ["BLEU"],
            "sorties": ["BLEU", "ANNULATION_SURCHAUFFE"],
            "declencheurs_amorces": ["ICONE_PIEGEAGE", "ICONE_SABOTAGE", "ICONE_REVE"],
            "vecteurs": "Perchoir (O) + Rouge → Refroidir · Cri de vapeur (0 Rouge restant OU 0 Rouge éligible) → allume 1 icône à droite sur la Piste · Face 2 : Étouffer à 0 Rouge et ≥ 2 Bleus",
            "double_ouverture": (
                "Assis sur Parade, la première activation Refroidit une machine et, si elle tombe à "
                "0 Rouge (ou sans cible Rouge), le Cri de vapeur allume une icône située à droite du "
                "Toucan sur la Piste (hors Résonance) pour relancer d’autres Gardiens ; en Face 2, "
                "la seconde activation pousse une machine à 0 Rouge et ≥ 2 Bleus pour l’Étouffer."
            ),
            "tuile_plateau": {
                "nom_court": "Le Toucan toco",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PARADE",
                "pictogrammes": ["PIC_ROUGE", "PIC_BLEU", "PIC_PERCHOIR", "PIC_ANNULATION"],
                "mots_cles_plateau": {
                    "face_1": "Refroidir sous le Perchoir (sinon O OU voisin) · 0 Rouge = allume 1 icône à droite",
                    "face_2": "Refroidir partout · 0 Rouge et 2 Bleus = Étouffer · Cri de vapeur actif",
                    "enracine": None,
                },
                "resume_plateau": "Refroidit les machines et relance la Piste",
            },
            "carte_joueur": {
                "titre_complet": "Le Toucan toco, le bec-radiateur",
                "texte_regle": {
                    "face_1": (
                        "Refroidissez 1 machine désignée par le Perchoir de Vigie (sur son rayon s’il "
                        "est au pied d’un rayon, ou une machine du rang qu’il pointe ; à défaut, une "
                        "machine du rayon Oiseaux ou d’un rayon voisin). Cri de vapeur : si cette "
                        "machine n’a plus aucun jeton Rouge après ce Refroidissement — ou s’il n’y "
                        "avait aucune machine éligible portant un jeton Rouge —, allumez immédiatement "
                        "1 icône de votre choix située strictement à droite de celle du Toucan toco sur "
                        "la Piste des Gardiens (hors Résonance)."
                    ),
                    "face_2": (
                        "Même effet, mais vous pouvez Refroidir n’importe quelle machine du plateau "
                        "(mobile ou en Ratissage). De plus, si la machine refroidie atteint 0 jeton "
                        "Rouge et au moins 2 jetons Bleus Surchauffe, vous l’Étouffez immédiatement "
                        "(le Cri de vapeur s’applique aussi)."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Refroidit une machine ciblée pour réduire son Seuil (ou l’Étouffer en Face 2) et allume une icône à droite sur la Piste via le Cri de vapeur.",
                    "renoncement": "Cibler une machine à 1 seul Rouge maximise le Cri de vapeur en piste, mais laisse intacte une machine à 2 ou 3 Rouges ailleurs.",
                },
            },
            "temoins": [
                {
                    "id": "G6_T1",
                    "statut": "A_CODER",
                    "resume": "Toucan F1 assis sur Parade Refroidit la machine à 1 Rouge sous le Perchoir : elle passe à 0 Rouge et Cri de vapeur allume Piégeage (à droite de Parade, hors Résonance).",
                },
                {
                    "id": "G6_T2",
                    "statut": "A_CODER",
                    "resume": "Toucan F2 Refroidit partout une machine portant 1 Rouge et 1 Bleu : elle passe à 0 Rouge et 2 Bleus, est immédiatement Étouffée et déclenche Cri de vapeur.",
                },
            ],
            "heuristique_bot": "Siège idéal sur Parade pour maximiser les icônes à droite ; priorise les machines à 1 Rouge (Cri de vapeur immédiat) ou à 1 Rouge + 1 Bleu en Face 2 (Étouffement).",
        },
        "G7": {
            "roles_portes": ["TWIST_2K3", "ENRACINEMENT"],
            "est_twist": True,
            "paiement": ["P_SOUCHE"],
            "entrees_plancher": ["ROUTE", "DUEL", "TAMBOUR", "CHANT"],
            "entrees_synergie": ["CHAMANE_EN_FORET", "ROUGE"],
            "sorties": ["BOURBIER_ROUTE", "TERRITOIRE", "BLEU", "RECUL", "ARBRE"],
            "declencheurs_amorces": ["ICONE_PARADE"],
            "vecteurs": "Duel ou Chamane sur Route → Bourbier bloquant la 1re traversée/frappe · Frayer → Duel + Territoire tenu · Face 2 : Refroidir ou Reculer · Enraciné : +1 Souche finale",
            "double_ouverture": (
                "Deux activations installent un Bourbier sur une Route clé puis posent le Duel sur une "
                "parcelle ciblée (ou créent deux Bourbiers distincts avec Duel et Chamane) ; en Face 2, "
                "un Bourbier en Territoire tenu résiste à une première machine."
            ),
            "tuile_plateau": {
                "nom_court": "Le Tapir",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PARADE",
                "pictogrammes": ["PIC_TWIST", "PIC_ROUTE", "PIC_DUEL", "PIC_ENRACINEMENT"],
                "mots_cles_plateau": {
                    "face_1": "Duel OU Chamane sur Route = Bourbier bloque 1re traversée OU Frayer Duel",
                    "face_2": "Bourbier Refroidit (sinon Reculer 1) · Territoire tenu bascule sur Défi",
                    "enracine": "Décompte final · Duel + Chamane = +1 Souche",
                },
                "resume_plateau": "Transforme les Routes en Bourbiers",
            },
            "carte_joueur": {
                "titre_complet": "Le Tapir, jardinier des sentiers",
                "texte_regle": {
                    "face_1": (
                        "Choisissez : Fouler une Route — posez le jeton Duel (pris où qu’il se trouve, "
                        "face actuelle) sur une Route Forestière, ou glissez le Tambour ou le Chant "
                        "depuis une parcelle adjacente sur une Route de son rayon. Tant que Le Tapir "
                        "est en piste, cette Route devient un Bourbier : la première machine qui "
                        "devrait la franchir en avançant ou en frappant Devant voit cette avancée ou "
                        "cette frappe annulée, puis le Duel retourne en réserve (ou le Chamane est "
                        "couché en attente). Ou Frayer — posez le Duel (pris partout) sur une parcelle "
                        "ciblée ; s’il y rejoint un Chamane, retournez le Duel sur Territoire tenu."
                    ),
                    "face_2": (
                        "Même effet, et la machine enlisée dans un Bourbier est en outre Refroidie si "
                        "elle porte au moins 1 jeton Rouge (sinon, si elle est mobile, faites-la "
                        "Reculer d’1 parcelle). De plus, un Bourbier tenu par le Duel sur sa face "
                        "Territoire tenu bascule sur sa face Défi au lieu de rentrer en réserve."
                    ),
                    "enracine": (
                        "Au décompte final, si le jeton Duel et au moins un Chamane occupent la même "
                        "parcelle survivante, retournez 1 Souche supplémentaire en Arbre debout sur "
                        "ce rayon."
                    ),
                },
                "decision_et_renoncement": {
                    "choix": "Bloque une avancée ou une frappe Devant par-dessus une Route via un Bourbier, ou scelle le Duel auprès d’un Chamane.",
                    "renoncement": "Engager le Duel ou un Chamane dans un Bourbier le prive de sa présence sur une parcelle forestière active ; enraciner Le Tapir dissipe aussitôt ses Bourbiers.",
                },
            },
            "temoins": [
                {
                    "id": "G7_T1",
                    "statut": "A_CODER",
                    "resume": "Route en M·2 portant le Duel (Bourbier F1) : une machine en M·1 qui doit frapper Devant (M·3) ou avancer par-dessus M·2 voit cette frappe/avancée annulée et le Duel rentre en réserve.",
                },
                {
                    "id": "G7_T2",
                    "statut": "A_CODER",
                    "resume": "Tapir F2 avec Duel face Territoire tenu en Bourbier : la machine enlisée est Refroidie (ou Recule d’1) et le Duel bascule sur Défi au lieu de rentrer en réserve.",
                },
            ],
            "heuristique_bot": "Prioritaire dès qu’une Route sépare une machine d’une parcelle riche en Arbres ; en absence de Route utile, Frayer sécurise Territoire tenu sur un Chamane.",
        },
        "G8": {
            "roles_portes": ["CATALYSEUR_EVEIL", "LEVIER_REVE"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["POSITION_REVE", "RANG_REVE"],
            "entrees_synergie": [],
            "sorties": ["POSITION_REVE", "ALTERATION", "ANNULATION"],
            "declencheurs_amorces": ["ICONE_REVE"],
            "vecteurs": "Rêve glissé d’1 rang à gauche ou échangé (Face 2 : 2 rangs / plongée sous voisin) · plancher sans Rêve : Altérer 1 mobile",
            "double_ouverture": (
                "Deux activations font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2) ou "
                "compactent deux Rêves séparés vers le Sommeil ; sans Rêve en jeu, elles Altèrent "
                "deux machines différentes."
            ),
            "tuile_plateau": {
                "nom_court": "Le Boto",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_REVE",
                "pictogrammes": ["PIC_AVANCEE_REVE", "PIC_REVE", "PIC_ALTERATION"],
                "mots_cles_plateau": {
                    "face_1": "Glisser 1 Rêve 1 rang à gauche OU échanger voisins · aucun = Altérer",
                    "face_2": "Glisser 1 Rêve 2 rangs OU plonger sous voisin · aucun = Altérer",
                    "enracine": None,
                },
                "resume_plateau": "Fait glisser les Rêves vers le rang 1",
            },
            "carte_joueur": {
                "titre_complet": "Le Boto, l’encantado du fleuve",
                "texte_regle": {
                    "face_1": (
                        "Choisissez un Rêve sur la Réglette et Glissez-le d’1 rang libre vers la "
                        "gauche, ou échangez deux Rêves occupant deux rangs voisins (en conservant "
                        "l’état debout ou couché de leurs Défenseurs). Si aucun Rêve ne peut bouger "
                        "(ou s’il n’y a aucun Rêve sur la Réglette), Altérez 1 machine mobile de "
                        "votre choix."
                    ),
                    "face_2": (
                        "Même effet, mais le Rêve choisi peut Glisser jusqu’à 2 rangs libres vers la "
                        "gauche — ou plonger par-dessus un Rêve voisin jusqu’au premier rang libre "
                        "immédiatement à sa gauche. S’il n’y a toujours aucun mouvement possible, "
                        "Altérez 1 machine mobile."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Accélère la convergence des Rêves vers les rangs 1–2–3 pour le Sommeil, ou Altère une mobile en plancher solo.",
                    "renoncement": "Déplacer un Rêve vers la gauche peut lui faire manquer une machine qui allait attaquer sur un rang élevé.",
                },
            },
            "temoins": [
                {
                    "id": "G8_T1",
                    "statut": "A_CODER",
                    "resume": "Boto F1 Glisse un Rêve du rang 5 au rang 4 libre (emportant ses Défenseurs) ; sans Rêve déplaçable, il Altère 1 machine mobile depuis la réserve Entités.",
                },
                {
                    "id": "G8_T2",
                    "statut": "A_CODER",
                    "resume": "Boto F2 fait plonger un Rêve du rang 4 par-dessus un Rêve au rang 3 pour atterrir au rang 2 libre.",
                },
            ],
            "heuristique_bot": "Levier majeur du Sommeil quand E joue sans H ; fait converger les Rêves à gauche dès l’Acte 1, sinon pose des Altérations.",
        },
        "G9": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["SABOTAGE", "ECAILLE"],
            "entrees_synergie": ["TAMBOUR"],
            "sorties": ["CALE", "RECUL", "ANNULATION"],
            "declencheurs_amorces": ["ICONE_SABOTAGE"],
            "vecteurs": "Sabotage ou Écaille révélé → cale sous machine mobile (R, H ou Tambour) → Ratissage bloqué · Face 2 : cale partout et machine calée révélée Étouffée",
            "double_ouverture": (
                "La première activation pose la cale (sur le Sabotage qui vient d’allumer l’icône), "
                "la seconde fait Reculer la machine calée d’1 parcelle ou déplace la cale ; chaque "
                "révélation de la machine calée rallume Sabotage sur la Piste."
            ),
            "tuile_plateau": {
                "nom_court": "Le Caïman noir",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_SABOTAGE",
                "pictogrammes": ["PIC_CALE", "PIC_SABOTAGE", "PIC_TAMBOUR", "PIC_RECUL"],
                "mots_cles_plateau": {
                    "face_1": "Jeton Sabotage révélé → cale sous mobile (R · H · Tambour) · bloque Ratissage",
                    "face_2": "Cale partout · mobile calée révélée = Étouffée · Sabotage rallumé",
                    "enracine": None,
                },
                "resume_plateau": "Pose la cale exclusive sous une machine",
            },
            "carte_joueur": {
                "titre_complet": "Le Caïman noir, l’ombre sous la pirogue",
                "texte_regle": {
                    "face_1": (
                        "Glissez le jeton cale (pris en réserve ou déjà sous une autre machine) sous "
                        "une machine mobile du rayon Reptiles, du rayon Humains ou du rayon portant "
                        "le Tambour (sinon, faites Reculer d’1 parcelle la machine actuellement calée). "
                        "Tant qu’elle porte la cale, cette machine ne peut pas entrer en Ratissage, et "
                        "chaque fois que son jeton Machine est révélé à l’ouverture, allumez aussitôt "
                        "l’icône Sabotage (la cale reste sous elle jusqu’à ce qu’elle soit déplacée "
                        "ou que le Caïman noir quitte la piste)."
                    ),
                    "face_2": (
                        "Même effet sur n’importe quelle machine mobile du plateau ; de plus, chaque "
                        "fois que la machine calée est révélée à l’ouverture, allumez Sabotage et "
                        "Étouffez-la immédiatement (elle ne frappe pas)."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Verrouille la machine la plus menaçante sous la cale (bloque Ratissage, rallume Sabotage et l’Étouffe en Face 2).",
                    "renoncement": "Une seule cale existe en jeu ; la déplacer libère la machine précédemment retenue.",
                },
            },
            "temoins": [
                {
                    "id": "G9_T1",
                    "statut": "A_CODER",
                    "resume": "Caïman F1 pose la cale sous l’Abatteuse du rayon du Tambour : elle ne peut pas entrer en Ratissage et sa révélation au tour suivant rallume Sabotage.",
                },
                {
                    "id": "G9_T2",
                    "statut": "A_CODER",
                    "resume": "Caïman F2 : lorsque la machine calée est révélée à l’ouverture, Sabotage s’allume et la machine est Étouffée (jeton à 90°, dé retiré).",
                },
            ],
            "heuristique_bot": "Pose la cale en priorité sur une machine proche de la dernière parcelle (anti-Ratissage) ou sur la plus chargée en Rouges en Face 2.",
        },
        "G10": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["ECAILLE", "CROC", "RANG_MACHINE"],
            "entrees_synergie": ["ALTERATION"],
            "sorties": ["ECAILLE", "CROC", "ALTERATION"],
            "declencheurs_amorces": ["ICONE_PIEGEAGE", "ICONE_SABOTAGE"],
            "vecteurs": "Semer 1 Écaille au sac → Happer (Croc sur parcelle ciblée) OU Envoûter (Altérer 1 mobile) · Face 2 : Happer ET Envoûter",
            "double_ouverture": (
                "Assise sur Piégeage, la première activation Sème 1 Écaille et poste le Croc ; dès que "
                "ce Croc pare une attaque (regagnant la réserve Reptile), il rallume Piégeage et "
                "déclenche la seconde activation de La Matamata."
            ),
            "tuile_plateau": {
                "nom_court": "La Matamata",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PIEGEAGE",
                "pictogrammes": ["PIC_ECAILLE", "PIC_CROC", "PIC_ALTERATION"],
                "mots_cles_plateau": {
                    "face_1": "Semer 1 Écaille · Happer (Croc réserve → cible) OU Envoûter (Altérer 1 mobile)",
                    "face_2": "Semer 1 Écaille · Happer (Croc partout → cible) · Envoûter (Altérer 1 mobile)",
                    "enracine": None,
                },
                "resume_plateau": "Sème une Écaille, embusque le Croc ou Altère",
            },
            "carte_joueur": {
                "titre_complet": "La Matamata, guetteuse des feuilles mortes",
                "pitch_ambiance": "On croit marcher sur un lit de feuilles mortes ; déjà le vide s’est ouvert sous l’acier et la vase glacée l’aspire.",
                "texte_regle": {
                    "face_1": (
                        "Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), "
                        "puis choisissez : Happer — prenez le Croc dans la réserve Reptile et "
                        "posez-le sur une parcelle ciblée de votre choix ; ou Envoûter — Altérez 1 "
                        "machine mobile de votre choix et, si le Croc se trouve déjà sur une parcelle "
                        "non ciblée, vous pouvez le déplacer sur une parcelle ciblée du rayon de "
                        "cette machine."
                    ),
                    "face_2": (
                        "Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), "
                        "puis résolvez à la fois Happer (en pouvant prendre le Croc soit dans la "
                        "réserve Reptile, soit sur une parcelle non ciblée) et Envoûter."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Enrichit le sac en Écailles puis arbitre en Face 1 entre embuscade immédiate du Croc (Happer) et pression onirique (Envoûter) ; cumule les deux en Face 2.",
                    "renoncement": "En Face 1, choisir Happer renonce à l’Altération ; choisir Envoûter laisse le Croc en réserve s’il n’est pas déjà en jeu.",
                },
            },
            "temoins": [
                {
                    "id": "G10_T1",
                    "statut": "A_CODER",
                    "resume": "Matamata F1 Sème 1 Écaille au sac et choisit Happer : le Croc de la réserve Reptile se poste sur une parcelle ciblée, prêt à rallumer Piégeage.",
                },
                {
                    "id": "G10_T2",
                    "statut": "A_CODER",
                    "resume": "Matamata F2 Sème 1 Écaille, repositionne le Croc depuis une parcelle non ciblée vers une cible (Happer) et Altère 1 machine mobile (Envoûter).",
                },
            ],
            "heuristique_bot": "Sème des Écailles tôt pour gonfler le sac ; en Face 1, choisit Happer dès qu’une cible menacée peut rallumer Piégeage, sinon Envoûter.",
        },
        "G11": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["PERCHOIR", "DEFENSEUR_ATTENTE", "RANG_MACHINE"],
            "entrees_synergie": ["CHANT", "TAMBOUR", "POSITION_REVE"],
            "sorties": ["DEFENSEUR_REDEPLOYE", "ANNULATION"],
            "declencheurs_amorces": ["ICONE_PARADE"],
            "vecteurs": "Défenseur Oiseau recyclé + Perchoir (O) → Fondre en forêt OU Saisir pour Étouffer sur le rang pointé · Face 2 : rang miroir + Chamane porté sur un Rêve",
            "double_ouverture": (
                "Un premier piqué pose un Oiseau au sol pour compléter une Parade (qui rallume son "
                "icône) ; le second piqué saisit une machine sous le Perchoir pour l’Étouffer."
            ),
            "tuile_plateau": {
                "nom_court": "La Harpie féroce",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PARADE",
                "pictogrammes": ["PIC_PERCHOIR", "PIC_RANG_MACHINE", "PIC_DEFENSEUR", "PIC_ANNULATION"],
                "mots_cles_plateau": {
                    "face_1": "Recycle 1 Oiseau → Fondre devant machine OU Saisir sur rang du Perchoir (Étouffer)",
                    "face_2": "Saisir sur rang du Perchoir OU miroir · porte 1 Chamane vers Rêve opposé",
                    "enracine": None,
                },
                "resume_plateau": "Fond au sol ou saisit une machine sous le Perchoir",
            },
            "carte_joueur": {
                "titre_complet": "La Harpie féroce, l’ombre sous la voûte",
                "texte_regle": {
                    "face_1": (
                        "Prenez 1 Défenseur Oiseau (en forêt, sur une Rive de Furtivité, sur un Rêve, "
                        "en lisière ou en attente) et choisissez : Fondre — posez-le sur la parcelle "
                        "d’une machine ou 1 pas devant elle (en sautant les Routes) ; ou Saisir — si "
                        "le Perchoir de Vigie pointe un rang 1–6, posez cet Oiseau directement sur le "
                        "jeton d’une machine mobile active de ce rang pour l’Étouffer jusqu’au ménage."
                    ),
                    "face_2": (
                        "Même effet, mais Saisir vise aussi bien le rang pointé par le Perchoir de "
                        "Vigie que son rang miroir (1↔4, 2↔5, 3↔6). De plus, après avoir saisi une "
                        "machine, vous pouvez emporter 1 Chamane depuis une parcelle visée par cette "
                        "machine et le poser debout sur un Rêve occupant le rang opposé (son miroir)."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Recycle un Défenseur Oiseau pour renforcer une Parade (Fondre) ou Étouffer net une machine sur le rang guetté (Saisir).",
                    "renoncement": "L’Oiseau posé en saisie reste immobilisé sur le jeton Machine jusqu’au ménage et ne défend plus la forêt ni les Rives.",
                },
            },
            "temoins": [
                {
                    "id": "G11_T1",
                    "statut": "A_CODER",
                    "resume": "Harpie F1 recycle 1 Oiseau couché en attente et choisit Saisir sur le rang 5 pointé par le Perchoir : la mobile du rang 5 est Étouffée jusqu’au ménage.",
                },
                {
                    "id": "G11_T2",
                    "statut": "A_CODER",
                    "resume": "Harpie F2 saisit une mobile au rang 2 (miroir du Perchoir au rang 5), puis porte le Chant depuis sa parcelle visée debout sur un Rêve au rang 5.",
                },
            ],
            "heuristique_bot": "Privilégie le recyclage d’un Oiseau couché en attente ou libéré ; choisit Saisir sur la mobile la plus létale du rang du Perchoir (et miroir en F2), sinon Fondre pour boucler une Parade.",
        },
        "G12": {
            "roles_portes": ["CATALYSEUR_EVEIL", "TWIST_2K3"],
            "est_twist": True,
            "paiement": [],
            "entrees_plancher": ["DES_SOUS_PARAVENT", "RANG_MACHINE", "POSITION_REVE"],
            "entrees_synergie": ["SABOTAGE"],
            "sorties": ["RANG_RELU", "ANNULATION_INDUITE"],
            "declencheurs_amorces": ["ICONE_REVE"],
            "vecteurs": "Dé écarté sous paravent (et 2 dés ignorés des porteurs de Sabotage/Écaille en F2) → nouveau rang → Étouffement sur Rêve et glissement du Rêve",
            "double_ouverture": (
                "Chaque Sabotage révélé allume l’icône de L’Ibijau : deux activations déplacent "
                "deux mobiles vers les Rêves encore à résoudre, et en Face 2 puisent aussi dans les "
                "dés ignorés des porteurs de Sabotage ou d’Écaille."
            ),
            "tuile_plateau": {
                "nom_court": "L’Ibijau",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_SABOTAGE",
                "pictogrammes": ["PIC_TWIST", "PIC_DES_PARAVENT", "PIC_RANG_MACHINE", "PIC_REVE"],
                "mots_cles_plateau": {
                    "face_1": "Dé d’une mobile révélée → rang de son dé écarté sous paravent",
                    "face_2": "OU dé ignoré d’un Sabotage · Rêve qui l’Étouffe Glisse 1 rang à gauche",
                    "enracine": None,
                },
                "resume_plateau": "Relit le dé écarté vers un Rêve",
            },
            "carte_joueur": {
                "titre_complet": "L’Ibijau, les yeux fendus de la nuit",
                "texte_regle": {
                    "face_1": (
                        "Choisissez une machine mobile révélée dont le dé est encore sur la Réglette : "
                        "déplacez son dé sur le rang indiqué par le dé écarté sous le paravent de son "
                        "porteur (fonctionne à l’identique pour l’Oiseau, dont le second dé est son "
                        "dé écarté). Si la machine change ainsi de rang, elle est résolue sur son "
                        "nouveau rang (et peut y être Étouffée par un Rêve encore debout ou subir une "
                        "Loi passive de ce rang)."
                    ),
                    "face_2": (
                        "Même effet, et vous pouvez aussi choisir à la place l’un des 2 dés ignorés "
                        "d’un joueur ayant révélé un Sabotage ou une Écaille ce tour-ci. De plus, si "
                        "la machine ainsi déplacée est Étouffée par un Rêve, vous pouvez aussitôt "
                        "Glisser ce Rêve d’1 rang libre vers la gauche."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Pousse une machine mobile hors d’un rang létal ou directement sous un Rêve défendu en relisant les dés écartés sous paravent.",
                    "renoncement": "Le dé écarté est souvent plus élevé que le dé retenu : l’utiliser hors Rêve peut faire passer une machine en Assaut ou en En avançant.",
                },
            },
            "temoins": [
                {
                    "id": "G12_T1",
                    "statut": "A_CODER",
                    "resume": "Porteur d’Abatteuse (dés 2 et 5, retenu 2, écarté 5) alors qu’un Rêve défendu siège au rang 5 : Ibijau F1 déplace son dé du rang 2 au rang 5 où le Rêve l’Étouffe.",
                },
                {
                    "id": "G12_T2",
                    "statut": "A_CODER",
                    "resume": "Ibijau F2 relit un dé ignoré (4) d’un porteur de Sabotage pour amener une mobile sur le Rêve du rang 4 ; Étouffée, elle permet de Glisser ce Rêve au rang 3 libre.",
                },
            ],
            "heuristique_bot": "Priorise tout déplacement amenant une mobile sur un Rêve défendu encore debout (ou hors d’un rang 3/6 En avançant) ; en F2, exploite les dés ignorés des Sabotages.",
        },
        "G13": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["INSECTE", "DUEL"],
            "entrees_synergie": ["NID"],
            "sorties": ["RIPOSTE_ESSAIM", "INSECTE", "TERRITOIRE"],
            "declencheurs_amorces": ["ICONE_INSECTE"],
            "vecteurs": "Nid à ≥ 2 Insectes éventré (−1 → +2) ou repli réserve (+1) · Face 2 : riposte projetée sur parcelle ciblée adjacente",
            "double_ouverture": (
                "Deux éventrements font gonfler deux Nids (ou deux fois le même) juste avant les "
                "attaques ; en Face 2, chaque riposte jaillit directement sur une parcelle ciblée "
                "adjacente pour allumer Insecte à la parade."
            ),
            "tuile_plateau": {
                "nom_court": "Le Tamanoir",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_INSECTE",
                "pictogrammes": ["PIC_NID", "PIC_INSECTE", "PIC_DUEL"],
                "mots_cles_plateau": {
                    "face_1": "Nid à 2 Insectes OU plus · −1 → +2 · sans Nid éligible = +1 réserve",
                    "face_2": "Riposte projetée sur parcelle ciblée adjacente · sans Nid = +1 réserve",
                    "enracine": None,
                },
                "resume_plateau": "Éventre un Nid pour déclencher une riposte",
            },
            "carte_joueur": {
                "titre_complet": "Le Tamanoir, le grand mangeur qui épargne",
                "texte_regle": {
                    "face_1": (
                        "Choisissez un Nid portant au moins 2 Insectes : défaussez 1 de ses Insectes "
                        "pour en ajouter aussitôt 2 de la réserve sur ce Nid (gain net de +1 Insecte). "
                        "S’il n’y a aucun Nid portant au moins 2 Insectes sur le plateau, prenez 1 "
                        "Insecte de la réserve de l’Essaim et posez-le sur la parcelle d’un Nid (ou, "
                        "à défaut, sur la parcelle du jeton Duel ou sur une parcelle du rayon "
                        "Mammifères ou Insectes)."
                    ),
                    "face_2": (
                        "Même effet, mais les 2 Insectes de la riposte peuvent être posés directement "
                        "sur une parcelle ciblée adjacente au Nid (en sautant les Routes) — y compris "
                        "sur la parcelle du Duel pour y parer et le retourner nativement sur "
                        "Territoire tenu."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Multiplie le stock d’Insectes d’un Nid mûr (ou amorce un Nid vide) et projette la riposte sur les parcelles ciblées en Face 2.",
                    "renoncement": "Exige de maintenir au moins 2 Insectes sur un Nid au lieu de les dépenser tous en parade.",
                },
            },
            "temoins": [
                {
                    "id": "G13_T1",
                    "statut": "A_CODER",
                    "resume": "Nid à 2 Insectes : Tamanoir F1 en défausse 1 et ajoute 2 Insectes de la réserve (le Nid passe à 3 Insectes) ; sans Nid à ≥ 2, pose 1 Insecte de la réserve.",
                },
                {
                    "id": "G13_T2",
                    "statut": "A_CODER",
                    "resume": "Tamanoir F2 éventre un Nid à 2 Insectes et projette les 2 Insectes de la riposte sur une parcelle ciblée adjacente portant le Duel face Défi.",
                },
            ],
            "heuristique_bot": "Eventre en priorité un Nid à ≥ 2 Insectes adjacent à une parcelle ciblée (en F2) ou sur le point de produire ; sinon utilise le repli réserve pour porter un Nid à 2 Insectes.",
        },
        "G14": {
            "roles_portes": ["CATALYSEUR_EVEIL"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["ECAILLE", "CROC"],
            "entrees_synergie": ["NID"],
            "sorties": ["PONTE", "CROC", "ECAILLE"],
            "declencheurs_amorces": ["ICONE_PIEGEAGE"],
            "vecteurs": "Écaille en ponte sous un Nid (sinon Semer 1 Écaille + Croc sur cible R/I) → éclosion du Croc sur frappe → Piégeage + Écaille semée au sac",
            "double_ouverture": (
                "Deux activations installent deux pontes sous deux Nids (en Face 2) ou combinent "
                "une ponte sous un Nid et un Croc directement posté ; chaque éclosion allume Piégeage "
                "et Sème l’Écaille au sac."
            ),
            "tuile_plateau": {
                "nom_court": "Le Téju",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_INSECTE",
                "pictogrammes": ["PIC_ECAILLE", "PIC_NID", "PIC_CROC", "PIC_PIEGE"],
                "mots_cles_plateau": {
                    "face_1": "Écaille sous 1 Nid → Croc éclot sur frappe et Sème Écaille · sans Nid = Semer + Croc",
                    "face_2": "Jusqu’à 2 pontes (OU 1 ponte + Croc) · le Croc éclot d’où qu’il soit",
                    "enracine": None,
                },
                "resume_plateau": "Pond une Écaille protectrice sous un Nid",
            },
            "carte_joueur": {
                "titre_complet": "Le Téju, la ponte au cœur de la termitière",
                "texte_regle": {
                    "face_1": (
                        "Glissez 1 Écaille (prise dans la réserve Reptile ou parmi les Écailles "
                        "révélées à ce tour) sous un Nid sans ponte (max 1 ponte en jeu). À la "
                        "première frappe contre la parcelle de ce Nid, si le Croc est en réserve "
                        "Reptile, il éclot aussitôt sur place : il pare cette frappe (allumant "
                        "Piégeage), retourne en réserve Reptile et l’Écaille est Semée au sac. S’il "
                        "n’y a aucun Nid sans ponte (ou déjà 1 ponte en jeu), Semez au sac 1 Écaille "
                        "disponible et posez le Croc disponible depuis la réserve sur une parcelle "
                        "ciblée du rayon Reptiles ou du rayon Insectes."
                    ),
                    "face_2": (
                        "Même effet, mais vous pouvez maintenir jusqu’à 2 pontes simultanées sous "
                        "des Nids différents (ou 1 ponte + le Croc posté ailleurs), et lors d’une "
                        "éclosion le Croc peut accourir d’où qu’il se trouve (réserve Reptile ou "
                        "plateau), puis rentre normalement en réserve Reptile après sa parade."
                    ),
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Protège un Nid vital contre sa prochaine frappe tout en préparant une Écaille à Semer au sac (et couvre deux Nids en Face 2).",
                    "renoncement": "Immobilise une Écaille hors du sac tant que la ponte n’éclot pas, et exige en Face 1 de garder le Croc en réserve pour l’éclosion.",
                },
            },
            "temoins": [
                {
                    "id": "G14_T1",
                    "statut": "A_CODER",
                    "resume": "Téju F1 glisse 1 Écaille sous un Nid ; une frappe sur ce Nid fait éclore le Croc de la réserve (parade + Piégeage + Croc revient en réserve + Écaille Semée au sac).",
                },
                {
                    "id": "G14_T2",
                    "statut": "A_CODER",
                    "resume": "Téju F2 entretient 2 pontes simultanées et fait éclore le Croc même s’il était posté sur une autre parcelle, avant qu’il regagne normalement la réserve.",
                },
            ],
            "heuristique_bot": "Pose une ponte dès qu’un Nid est à portée de frappe ; sans Nid libre, Sème une Écaille et poste le Croc directement sur la parcelle la plus menacée de R ou I.",
        },
        "G15": {
            "roles_portes": ["CATALYSEUR_EVEIL", "ENRACINEMENT"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["PERCHOIR"],
            "entrees_synergie": ["INSECTE", "NID", "GARDIEN"],
            "sorties": ["INSECTE_TRANSPORTE", "INSECTE", "INSECTE_RANG", "PARI_GLISSE", "ARBRE"],
            "declencheurs_amorces": ["ICONE_INSECTE"],
            "vecteurs": "Insecte transporté à vol d’oiseau (amorçage natif) → prélèvement sur icône de Gardien = 1 pari en encoche · Face 2 : 2 Insectes + pollinisation + dépôt Perchoir · Enraciné : +1 Souche par tuile voisine",
            "double_ouverture": (
                "Deux vols complètent une parade urgente puis pollinisent un Nid (Face 2) ou "
                "prélèvent un Insecte sur la Piste des Gardiens pour glisser un pari en encoche."
            ),
            "tuile_plateau": {
                "nom_court": "Le Colibri",
                "fenetre_badge": "ACTIVATION",
                "icone_conseillee": "ICONE_PARADE",
                "pictogrammes": ["PIC_INSECTE", "PIC_PERCHOIR", "PIC_PARI_ENCOCHE", "PIC_ENRACINEMENT"],
                "mots_cles_plateau": {
                    "face_1": "1 Insecte → toute parcelle · pris sur icône d’un Gardien = 1 pari en encoche",
                    "face_2": "2 Insectes · arrivée Nid = +1 Insecte · dépôt possible sur rang du Perchoir",
                    "enracine": "Décompte final · +1 Souche par autre tuile enracinée sur O OU voisins",
                },
                "resume_plateau": "Transporte l’Essaim et accélère les paris",
            },
            "carte_joueur": {
                "titre_complet": "Le Colibri, porteur de gouttes et de pollen",
                "texte_regle": {
                    "face_1": (
                        "Déplacez 1 Insecte depuis n’importe où sur le plateau vers n’importe quelle "
                        "parcelle forestière (l’amorçage natif de l’Essaim s’applique si aucun Insecte "
                        "n’est en jeu). Si cet Insecte est prélevé sur l’icône d’un Gardien en piste "
                        "portant au moins 1 pari, glissez aussitôt 1 pari de ce Gardien dans son "
                        "encoche (sans déclencher son pouvoir ni allumer la Résonance)."
                    ),
                    "face_2": (
                        "Même effet avec jusqu’à 2 Insectes. De plus, chaque fois qu’un Insecte "
                        "transporté arrive sur la parcelle d’un Nid, produisez aussitôt 1 Insecte "
                        "supplémentaire de la réserve sur ce Nid ; et si le Perchoir de Vigie pointe "
                        "un rang 1–6, vous pouvez déposer l’un des Insectes directement sur ce rang "
                        "de la Réglette."
                    ),
                    "enracine": (
                        "Au décompte final, retournez 1 Souche supplémentaire en Arbre debout sur le "
                        "rayon de chaque autre tuile enracinée située sur le rayon Oiseaux ou sur l’un "
                        "de ses deux rayons voisins."
                    ),
                },
                "decision_et_renoncement": {
                    "choix": "Ravitaille n’importe quelle parcelle ou déviation, ou prélève un Insecte sur la Piste des Gardiens pour sécuriser un pari.",
                    "renoncement": "Prélever un Insecte sur une icône de Gardien le prive de son rôle de déclencheur sur la Piste ; enraciner Le Colibri sacrifie sa logistique aérienne.",
                },
            },
            "temoins": [
                {
                    "id": "G15_T1",
                    "statut": "A_CODER",
                    "resume": "Colibri F1 prélève 1 Insecte posé sur l’icône d’un Gardien en piste et le dépose sur une parcelle menacée : 1 pari de ce Gardien glisse en encoche sans pouvoir ni Résonance.",
                },
                {
                    "id": "G15_T2",
                    "statut": "A_CODER",
                    "resume": "Colibri F2 transporte 2 Insectes : le premier arrive sur un Nid (+1 Insecte produit), le second est déposé sur le rang pointé par le Perchoir de Vigie.",
                },
            ],
            "heuristique_bot": "Priorise le prélèvement sur une icône de Gardien ayant un pari bloqué ; en Face 2, pollinise les Nids à 1 Insecte et alimente le rang pointé par le Perchoir.",
        },
        # ------------------------------------------------------------------
        # RÊVES (R1 .. R10)
        # ------------------------------------------------------------------
        "R1": {
            "roles_portes": ["AUTONOMIE_A0", "LEVIER_REVE", "ENRACINEMENT"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["POSITION_REVE", "RANG_REVE"],
            "entrees_synergie": ["TAMBOUR"],
            "sorties": ["REVE_COMPACTE", "POSITION_REVE", "ANNULATION"],
            "declencheurs_amorces": [],
            "vecteurs": "Rêve Humain défendu → tire un Rêve des Entités contre lui (bloc contigu) · Écho chamane : le Tambour passe debout sur le Rêve tiré · Enraciné sans fermer le Sommeil",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Liane des Esprits",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_REVE", "PIC_AVANCEE_REVE", "PIC_TAMBOUR", "PIC_ENRACINEMENT"],
                "mots_cles_plateau": {
                    "face_1": "Tire 1 Rêve des Entités · collé = paire Glisse à gauche · Écho Tambour debout dessus",
                    "face_2": None,
                    "enracine": "Enracinée sur Rive Sabotage de H sans fermer le Sommeil",
                },
                "resume_plateau": "Tire un Rêve des Entités et relaie le Tambour",
            },
            "carte_joueur": {
                "titre_complet": "La Liane des Esprits",
                "texte_regle": {
                    "face_1": (
                        "Défendu : après avoir résolu ses annulations habituelles, choisissez un Rêve "
                        "des Entités situé à droite de La Liane des Esprits et Glissez-le jusqu’au "
                        "rang libre immédiatement à droite de la Liane (s’il est déjà collé contre "
                        "elle, Glissez la paire ensemble d’1 rang libre vers la gauche). S’il n’y a "
                        "aucun Rêve des Entités à droite, Glissez la Liane d’1 rang libre vers la "
                        "gauche (ou, si le rang à sa gauche est occupé, Étouffez 1 machine mobile "
                        "supplémentaire sur son rang). Écho chamane : si le Tambour défendait La "
                        "Liane des Esprits, il peut aussitôt après ces annulations passer debout sur "
                        "le Rêve des Entités ainsi tiré — s’il n’était pas défendu — afin que ce Rêve "
                        "se résolve à son tour à l’ouverture."
                    ),
                    "face_2": None,
                    "enracine": (
                        "Enracinée sur la Rive Sabotage du rayon Humains, La Liane des Esprits ne "
                        "ferme pas la victoire par Sommeil Profond (les autres Rêves peuvent encore "
                        "former un bloc contigu suffisant)."
                    ),
                },
                "decision_et_renoncement": {
                    "choix": "Compacte les Rêves vers le Sommeil et permet au Tambour de déclencher en relais un Rêve des Entités non défendu, tout en restant enracinable sans briser le Sommeil.",
                    "renoncement": "Passer le Tambour debout sur le Rêve des Entités le prive d’une descente en forêt et expose ce second Rêve à son propre rang.",
                },
            },
            "temoins": [
                {
                    "id": "R1_T1",
                    "statut": "A_CODER",
                    "resume": "Liane défendue au rang 2 par le Tambour, Rêve Entités non défendu au rang 5 : la Liane tire ce Rêve au rang 3 puis Écho chamane passe le Tambour debout au rang 3 pour le résoudre aussitôt.",
                },
                {
                    "id": "R1_T2",
                    "statut": "A_CODER",
                    "resume": "Liane enracinée sur la Rive Sabotage de H : elle apporte l’Effet Sentinelle permanent sans fermer la victoire par Sommeil Profond.",
                },
            ],
            "heuristique_bot": "Défendue en priorité avec le Tambour dès qu’un Rêve Entités non défendu siège à sa droite ; candidate sûre à l’Enracinement en fin de partie sans bloquer le Sommeil.",
        },
        "R2": {
            "roles_portes": ["AUTONOMIE_A0", "ENRACINEMENT"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["POSITION_REVE", "RANG_MACHINE"],
            "entrees_synergie": ["TAMBOUR", "DEFENSEUR_ATTENTE", "ALTERATION"],
            "sorties": ["ALTERATION", "DEFENSEUR_REDEPLOYE", "ARBRE"],
            "declencheurs_amorces": [],
            "vecteurs": "Linceul de cendre (altérée/Étouffée → face cachée = 0 en Furtivité) + Altérer OU relever Tambour sur Rêve à droite · Enraciné : Gué de cendre + Gué marqué 90° → 2 Souches finales",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Fleuve sous la cendre",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_ALTERATION", "PIC_TAMBOUR", "PIC_SOUCHE", "PIC_ENRACINEMENT"],
                "mots_cles_plateau": {
                    "face_1": "Linceul = jeton face cachée (0) · Altérer 1 mobile OU relever Tambour sur Rêve à droite",
                    "face_2": None,
                    "enracine": "Gué de cendre sur E · machine altérée = 90° · 2 Souches finales",
                },
                "resume_plateau": "Masque la Furtivité, Altère et marque le Gué",
            },
            "carte_joueur": {
                "titre_complet": "Le Fleuve sous la cendre",
                "texte_regle": {
                    "face_1": (
                        "Linceul de cendre : tant que Le Fleuve sous la cendre est défendu à ce tour, "
                        "chaque machine qui perd son Altération à l’ouverture ou qui est Étouffée par "
                        "ce Rêve retourne son jeton Machine face cachée devant son rayon (il compte "
                        "pour 0 dans le compte de Furtivité de ce rayon). De plus, à sa résolution, "
                        "choisissez : Altérez 1 machine mobile (de n’importe quel rayon si le Tambour "
                        "est en forêt, sinon du rayon Entités ou du rayon Humains) ; ou relevez le "
                        "Tambour en attente pour le poser debout sur un Rêve non défendu situé à "
                        "droite de ce Rêve."
                    ),
                    "face_2": None,
                    "enracine": (
                        "Gué de cendre (Rive Sabotage du rayon Entités ; ferme le Sommeil) : toute "
                        "machine du rayon Entités qui perd son Altération à l’ouverture retourne son "
                        "jeton face cachée devant le rayon Entités (il compte pour 0 dans son compte "
                        "de Furtivité). Si au moins 1 machine du rayon Entités porte une Altération "
                        "au moment de l’enracinement, tournez cette Grande Carte à 90° (Gué marqué). "
                        "Au décompte final, une carte en Gué marqué retourne 2 Souches survivantes "
                        "au lieu d’1 en Arbres debout sur le rayon Entités."
                    ),
                },
                "decision_et_renoncement": {
                    "choix": "Assure la Rive Sabotage en masquant les jetons en Furtivité, Altère ou relève le Tambour, puis double son rapport de Souches en s’enracinant sur un Gué marqué.",
                    "renoncement": "Enraciner Le Fleuve sous la cendre ferme la victoire par Sommeil Profond ; manquer le marquage d’une machine altérée sur E limite son enracinement à 1 Souche.",
                },
            },
            "temoins": [
                {
                    "id": "R2_T1",
                    "statut": "A_CODER",
                    "resume": "Fleuve défendu : une mobile perd son Altération à l’ouverture et retourne son jeton face cachée (compte 0 en Furtivité), permettant de gagner la Rive Sabotage à 0 machine visible.",
                },
                {
                    "id": "R2_T2",
                    "statut": "A_CODER",
                    "resume": "Enraciné sur la Rive Sabotage de E alors qu’une machine de E est altérée : carte tournée à 90° (Gué marqué), retournant 2 Souches en Arbres au décompte final + Effet Sentinelle permanent.",
                },
            ],
            "heuristique_bot": "Défendu dès que E vise la Rive Sabotage ou veut relever un Tambour en attente ; s’enracine au Tour 5–7 dès qu’une machine de E porte une Altération (Gué marqué).",
        },
        "R3": {
            "roles_portes": [],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["RANG_REVE", "DUEL"],
            "entrees_synergie": ["ANNULATION", "TAMBOUR"],
            "sorties": ["CHAMANE_EN_FORET", "DEFENSEUR_REDEPLOYE", "TERRITOIRE"],
            "declencheurs_amorces": ["ICONE_PARADE"],
            "vecteurs": "Défenseurs du Rêve après résolution → bond vers Duel ou parcelle ciblée · Écho chamane : le Tambour emporte le Duel sur sa parcelle d’arrivée",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Chamane-Jaguar",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_REVE", "PIC_DEFENSEUR", "PIC_TAMBOUR", "PIC_DUEL"],
                "mots_cles_plateau": {
                    "face_1": "Après résolution · Défenseurs bondissent en forêt · Écho Tambour emporte le Duel",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Étouffe puis fait bondir ses Défenseurs",
            },
            "carte_joueur": {
                "titre_complet": "La Vision du Chamane-Jaguar",
                "texte_regle": {
                    "face_1": (
                        "Défendu : après avoir résolu ses annulations habituelles, chacun des "
                        "Défenseurs qui défendaient ce Rêve peut bondir directement sur la parcelle "
                        "du jeton Duel ou sur une parcelle ciblée du rayon d’une machine tout juste "
                        "Étouffée par ce Rêve (au lieu de rester couché sur le Rêve ; s’il n’a "
                        "Étouffé aucune machine, ils peuvent bondir sur le rayon Humains ou le rayon "
                        "Mammifères). Écho chamane : si le Tambour bondit ainsi, il peut emporter le "
                        "jeton Duel (pris où qu’il se trouve, en conservant sa face actuelle) et le "
                        "poser sur sa parcelle d’arrivée."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Transforme chaque Défenseur du Rêve en renfort de Parade immédiat et permet au Tambour de repositionner le Duel où la bataille se joue.",
                    "renoncement": "Quitter le Rêve ne retire pas son blocage déjà résolu, mais oblige à choisir quelle parcelle sauver avec le Duel.",
                },
            },
            "temoins": [
                {
                    "id": "R3_T1",
                    "statut": "A_CODER",
                    "resume": "Vision défendue par le Tambour : après avoir Étouffé la machine du rang, le Tambour bondit sur une parcelle ciblée en emportant le jeton Duel (Écho chamane).",
                },
            ],
            "heuristique_bot": "Défendue en priorité par le Tambour pour obtenir un double service (Étouffement à l’ouverture + Parade avec Duel repositionné aux attaques).",
        },
        "R4": {
            "roles_portes": ["TWIST_2K3", "LEVIER_REVE"],
            "est_twist": True,
            "paiement": ["P_RANG"],
            "entrees_plancher": ["POSITION_REVE", "RANG_REVE"],
            "entrees_synergie": [],
            "sorties": ["PISTON_REVES", "POSITION_REVE", "ECAILLE"],
            "declencheurs_amorces": [],
            "vecteurs": "Rêve-piston : Poussée en queue (tout le convoi Glisse d’1) OU Retour (échange à droite) · chaque mue Sème 1 Écaille au sac",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Pirogue-Anaconda",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_TWIST", "PIC_AVANCEE_REVE", "PIC_REVE", "PIC_ECAILLE"],
                "mots_cles_plateau": {
                    "face_1": "En queue = convoi Glisse 1G · OU échange à droite · chaque mue = Semer 1 Écaille",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Pousse tout le convoi et Sème des Écailles",
            },
            "carte_joueur": {
                "titre_complet": "La Pirogue-Anaconda des ancêtres",
                "texte_regle": {
                    "face_1": (
                        "Défendu : après ses annulations habituelles, choisissez : Poussée — si La "
                        "Pirogue-Anaconda est le Rêve le plus à droite de la Réglette (ou le seul), "
                        "Glissez ensemble tous les Rêves de la Réglette d’1 rang libre vers la gauche "
                        "(en commençant par le plus à gauche) ; ou Retour — échangez La "
                        "Pirogue-Anaconda avec le premier Rêve situé à sa droite (en conservant "
                        "l’état debout ou couché de leurs Défenseurs). Chaque fois qu’un mouvement "
                        "est effectué ainsi, Semez au sac 1 Écaille disponible depuis la réserve "
                        "Reptile."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Pousse tout le convoi des Rêves d’un bloc vers les rangs 1–2–3 ou recule pour relancer un cycle de poussée tout en Semant des Écailles au sac.",
                    "renoncement": "Choisir Retour éloigne temporairement la Pirogue du bloc gauche en échange d’un repositionnement en queue et d’une Écaille.",
                },
            },
            "temoins": [
                {
                    "id": "R4_T1",
                    "statut": "A_CODER",
                    "resume": "Pirogue-Anaconda en queue au rang 5 avec deux Rêves aux rangs 2 et 4 : Poussée Glisse les trois Rêves aux rangs 1, 3 et 4 et Sème 1 Écaille au sac.",
                },
            ],
            "heuristique_bot": "Défendue en queue de convoi pour compacter vers le Sommeil tout en enrichissant le sac en Écailles.",
        },
        "R5": {
            "roles_portes": [],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["PERCHOIR", "RANG_MACHINE"],
            "entrees_synergie": ["TAMBOUR", "CHANT", "ROUGE"],
            "sorties": ["RANG_MACHINE", "BLEU"],
            "declencheurs_amorces": ["ICONE_REVE"],
            "vecteurs": "Perchoir de Vigie (O) → échange de 2 mobiles actives à ±3 rangs (1↔4, 2↔5, 3↔6) · Écho chamane : Chant bascule 1 mobile seule · Tambour Refroidit 1 déplacée",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Ciel à deux eaux",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_PERCHOIR", "PIC_RANG_MACHINE", "PIC_TAMBOUR", "PIC_CHANT"],
                "mots_cles_plateau": {
                    "face_1": "Échange 2 mobiles à ±3 rangs sous le Perchoir · Écho Chant seul · Tambour Refroidit",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Inverse les rangs miroirs sous le Perchoir",
            },
            "carte_joueur": {
                "titre_complet": "Le Ciel à deux eaux",
                "texte_regle": {
                    "face_1": (
                        "Défendu : avant ses annulations habituelles, si le Perchoir de Vigie pointe "
                        "un rang 1–6 (ou est au pied d’un rayon en portant un jeton caché), vous "
                        "pouvez échanger les dés de 2 machines mobiles actives séparées d’exactement "
                        "3 rangs (1↔4, 2↔5 ou 3↔6) dont l’une au moins est désignée par le Perchoir "
                        "(sinon, échangez deux mobiles actives de votre choix séparées de 3 rangs). "
                        "Écho chamane : si le Chant défend ce Rêve, vous pouvez aussi basculer 1 "
                        "machine mobile seule vers son rang miroir même sans machine active en face ; "
                        "si le Tambour défend ce Rêve, Refroidissez l’une des machines ainsi "
                        "déplacées si elle porte au moins 1 jeton Rouge."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Bascule une machine d’Assaut vers Charge (ou vers le rang d’un Rêve), avec souplesse de bascule solo via le Chant ou Refroidissement via le Tambour.",
                    "renoncement": "Échanger deux mobiles expose le rang miroir à la seconde machine si aucun Rêve ne l’y attend.",
                },
            },
            "temoins": [
                {
                    "id": "R5_T1",
                    "statut": "A_CODER",
                    "resume": "Ciel défendu par le Chant au rang 2 avec Perchoir au rang 5 : la mobile du rang 5 bascule seule sur son miroir au rang 2 où le Rêve l’Étouffe aussitôt.",
                },
                {
                    "id": "R5_T2",
                    "statut": "A_CODER",
                    "resume": "Ciel défendu par le Tambour échange deux mobiles entre les rangs 3 et 6 et Refroidit celle qui porte 1 Rouge.",
                },
            ],
            "heuristique_bot": "Défendu avec Chant (bascule solo vers ce Rêve ou un Rêve à droite) ou Tambour (échange + Refroidissement d’une machine à Rouge).",
        },
        "R6": {
            "roles_portes": ["AUTONOMIE_A0"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["INSECTE", "ANNULATION"],
            "entrees_synergie": ["INSECTE_RANG", "TAMBOUR", "CHANT"],
            "sorties": ["ANNULATION_RENFORCEE", "INSECTE_RANG"],
            "declencheurs_amorces": [],
            "vecteurs": "Cueillette d’1 Insecte de H sur ce rang (amorçage natif) → chaque Insecte défaussé Étouffe +1 machine · Écho chamane : Tambour cueille jusqu’à 2 (H/I) · Chant Étouffe aussi à ±1",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Tucandeira",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_REVE", "PIC_INSECTE", "PIC_ANNULATION", "PIC_TAMBOUR"],
                "mots_cles_plateau": {
                    "face_1": "Cueille 1 Insecte de H → chaque défaussé Étouffe +1 · Écho Tambour 2 (H/I) · Chant ±1",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "L’Essaim multiplie les Étouffements du Rêve",
            },
            "carte_joueur": {
                "titre_complet": "Le Rite de la Tucandeira",
                "texte_regle": {
                    "face_1": (
                        "Défendu : avant de résoudre ses annulations, vous pouvez cueillir 1 Insecte "
                        "depuis le rayon Humains pour le poser sur le rang de ce Rêve (l’amorçage "
                        "natif de l’Essaim s’applique si aucun Insecte n’est sur le plateau). Puis, "
                        "lors de sa résolution, chaque Insecte que vous défaussez depuis ce rang "
                        "Étouffe 1 machine mobile supplémentaire de ce rang (en plus du quota "
                        "habituel de ses Défenseurs). Écho chamane : si le Tambour défend ce Rêve, "
                        "vous pouvez cueillir jusqu’à 2 Insectes depuis le rayon Humains ou le rayon "
                        "Insectes ; si le Chant défend ce Rêve, chaque Insecte défaussé peut Étouffer "
                        "une machine mobile soit sur ce rang, soit sur un rang directement adjacent "
                        "(±1)."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Transforme des Insectes en Étouffements multiples dès l’ouverture, élargis à ±1 rang avec le Chant ou à 2 cueillettes avec le Tambour.",
                    "renoncement": "Défausser des Insectes sur la Réglette les retire de la défense forestière et de la croissance des Nids.",
                },
            },
            "temoins": [
                {
                    "id": "R6_T1",
                    "statut": "A_CODER",
                    "resume": "Tucandeira défendue par le Chant au rang 4 : cueille 1 Insecte de H et le défausse pour Étouffer une machine mobile au rang 5 adjacent (Écho chamane).",
                },
                {
                    "id": "R6_T2",
                    "statut": "A_CODER",
                    "resume": "Tucandeira défendue par le Tambour avec 0 Insecte en jeu : amorçage natif en réserve, puis chaque Insecte défaussé Étouffe +1 machine du rang.",
                },
            ],
            "heuristique_bot": "Défendue par le Chant pour couvrir 3 rangs (rang ±1) avec un seul Défenseur + Insectes, ou par le Tambour pour nettoyer un encombrement de 2–3 machines sur le même rang.",
        },
        "R7": {
            "roles_portes": ["LOI_PASSIVE"],
            "est_twist": False,
            "nature": "LOI_PASSIVE",
            "cycle": "PASSIF_CONTINU",
            "paiement": [],
            "entrees_plancher": ["RANG_REVE", "POSITION_REVE", "RANG_MACHINE"],
            "entrees_synergie": ["DUEL"],
            "sorties": ["RECUL", "TERRITOIRE", "ALTERATION"],
            "declencheurs_amorces": [],
            "vecteurs": "Loi passive : machines sur son rang marchent à reculons + tout Recul hors du Duel (toute cause) retourne Territoire tenu · Défendu : mobiles Étouffées aussi Altérées",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Curupira",
                "fenetre_badge": "LOI_PASSIVE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_LOI_PASSIVE", "PIC_RECUL", "PIC_DUEL", "PIC_ALTERATION"],
                "mots_cles_plateau": {
                    "face_1": "Loi · son rang marche à reculons · tout Recul hors Duel = Territoire · Défendu = Altérer",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Inverse la marche et Altère les Étouffées",
            },
            "carte_joueur": {
                "titre_complet": "Le Curupira, protecteur aux pieds retournés",
                "texte_regle": {
                    "face_1": (
                        "Loi passive : toute machine mobile qui attaque depuis le rang du Curupira "
                        "marche à reculons — sa frappe Devant vise la parcelle derrière elle vers la "
                        "bordure (en sautant les Routes), son avancée la fait Reculer d’1 parcelle "
                        "vers la bordure, et sa frappe Sur place ne gagne jamais de jeton Rouge. De "
                        "plus, partout sur le plateau, toute machine qui Recule hors de la parcelle "
                        "du jeton Duel face Défi — quelle qu’en soit la cause — retourne aussitôt le "
                        "Duel sur sa face Territoire tenu. Défendu : chaque machine mobile Étouffée "
                        "sur son rang est en outre Altérée."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Laisse Le Curupira sans Défenseur pour faire reculer les machines de son rang et sceller Territoire tenu, ou le défend pour Étouffer et Altérer simultanément.",
                    "renoncement": "Défendre Le Curupira Étouffe la machine au lieu de la laisser reculer d’elle-même, mais pose une Altération pour le tour suivant.",
                },
            },
            "temoins": [
                {
                    "id": "R7_T1",
                    "statut": "A_CODER",
                    "resume": "Curupira non défendu au rang 3 : une machine au rang 3 frappe derrière et Recule hors de la parcelle du Duel face Défi, le retournant sur Territoire tenu.",
                },
                {
                    "id": "R7_T2",
                    "statut": "A_CODER",
                    "resume": "Curupira défendu au rang 4 : la mobile Étouffée par ce Rêve reçoit en outre 1 jeton d’Altération de la réserve Entités.",
                },
            ],
            "heuristique_bot": "Positionné sur un rang En avançant (3 ou 6) pour casser l’avancée sans Défenseur ; défendu lorsqu’une mobile critique doit être à la fois Étouffée et Altérée.",
        },
        "R8": {
            "roles_portes": ["LOI_PASSIVE", "LEVIER_REVE"],
            "est_twist": False,
            "nature": "LOI_PASSIVE",
            "cycle": "PASSIF_CONTINU",
            "paiement": [],
            "entrees_plancher": ["POSITION_REVE", "ALTERATION", "RANG_MACHINE"],
            "entrees_synergie": ["ECAILLE", "ROUGE"],
            "sorties": ["RANG_REVE", "ALTERATION", "BLEU"],
            "declencheurs_amorces": ["ICONE_REVE"],
            "vecteurs": "Loi passive 100 % Ouverture : chaque Écaille révélée (ou ce Rêve défendu) → Glisser 1 Rêve d’1 rang libre à gauche + Altérer 1 mobile OU Refroidir 1 machine",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Mue d’obsidienne",
                "fenetre_badge": "LOI_PASSIVE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_LOI_PASSIVE", "PIC_ECAILLE", "PIC_AVANCEE_REVE", "PIC_ALTERATION"],
                "mots_cles_plateau": {
                    "face_1": "Loi · chaque Écaille révélée OU Défendu → Glisser 1 Rêve 1G + Altérer OU Refroidir",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Écailles et Rêve glissent, Altèrent ou Refroidissent",
            },
            "carte_joueur": {
                "titre_complet": "La Mue d’obsidienne",
                "pitch_ambiance": "Le reptile abandonne son ancienne peau aux esprits de la nuit ; chaque écaille qui tombe ouvre un sillon d’ombre vers le cœur du sommeil.",
                "texte_regle": {
                    "face_1": (
                        "Loi passive (Ouverture) : chaque fois qu’une Écaille Reptile est révélée à "
                        "l’ouverture — ainsi que lorsque La Mue d’obsidienne est défendue et résolue "
                        "—, Glissez 1 Rêve de votre choix d’1 rang libre vers la gauche, puis "
                        "choisissez : Altérez 1 machine mobile ou Refroidissez 1 machine portant au "
                        "moins 1 jeton Rouge."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Convertit chaque Écaille révélée (et chaque défense propre) en avancée vers le Sommeil couplée à une Altération ou un Refroidissement.",
                    "renoncement": "Arbitrer entre Altérer une mobile pour le tour suivant ou Refroidir immédiatement une menace chargée de ce tour.",
                },
            },
            "temoins": [
                {
                    "id": "R8_T1",
                    "statut": "A_CODER",
                    "resume": "Une Écaille est révélée à l’ouverture : La Mue d’obsidienne (même non défendue) Glisse 1 Rêve d’1 rang libre à gauche et Refroidit 1 machine à Rouge.",
                },
                {
                    "id": "R8_T2",
                    "statut": "A_CODER",
                    "resume": "La Mue d’obsidienne défendue à l’ouverture : après ses annulations, elle Glisse 1 Rêve d’1 rang libre à gauche et Altère 1 machine mobile.",
                },
            ],
            "heuristique_bot": "Levier passif très rentable avec les Écailles semées par R ; privilégie Refroidir sur menace immédiate à fort Seuil, sinon Altérer pour préparer le tour suivant.",
        },
        "R9": {
            "roles_portes": ["LEVIER_REVE"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["PERCHOIR", "RANG_REVE"],
            "entrees_synergie": ["ALTERATION", "ROUGE"],
            "sorties": ["POSITION_REVE", "ALTERATION", "BLEU"],
            "declencheurs_amorces": ["ICONE_REVE"],
            "vecteurs": "Perchoir de Vigie (O) → vol de 2 rangs avant annulation · puis Maudire (Altérer) OU Siffler dans la brume (retire 1–2 Altérations → Glisse 1–2 Rêves à gauche + Refroidit)",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Matinta Pereira",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_PERCHOIR", "PIC_AVANCEE_REVE", "PIC_ALTERATION", "PIC_BLEU"],
                "mots_cles_plateau": {
                    "face_1": "Vole ≤ 2 rangs vers Perchoir · Maudire (Altérer) OU retirer 1–2 Altérations → Glisser + Refroidir",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Vole vers le Perchoir, maudit ou siffle",
            },
            "carte_joueur": {
                "titre_complet": "La Matinta Pereira, siffleuse de minuit",
                "brief_illustration": (
                    "Minuit sur un village sur pilotis : une vieille femme drapée de noir se "
                    "dissout en un oiseau sombre qui s’élève en sifflant ; son vol trace une "
                    "ligne lumineuse vers un perchoir de vigie pointé vers un rang de la "
                    "Réglette ; sur un seuil, une offrande de tabac. Noirs, violets, argent "
                    "lunaire."
                ),
                "texte_regle": {
                    "face_1": (
                        "Défendu : avant de résoudre ses annulations, si le Perchoir de Vigie pointe "
                        "un rang 1–6, Glissez La Matinta Pereira jusqu’à 2 rangs libres en direction "
                        "de ce rang (elle peut s’y poser s’il est libre). Après ses annulations "
                        "habituelles, choisissez : Maudire — Altérez 1 machine mobile de ce rang "
                        "(même tout juste Étouffée) ou du rayon ou du rang désigné par le Perchoir "
                        "(à défaut, du rayon Entités) ; ou Siffler dans la brume — retirez 1 ou 2 "
                        "jetons d’Altération en jeu (rendus à la réserve Entités) : pour chaque "
                        "Altération ainsi retirée, Glissez 1 Rêve d’1 rang libre vers la gauche et, "
                        "si la machine réveillée porte au moins 1 jeton Rouge, Refroidissez-la."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Intercepte une machine en volant vers le Perchoir, puis accumule des Altérations (Maudire) ou les encaisse en tempo Sommeil + Refroidissement (Siffler dans la brume).",
                    "renoncement": "Retirer des Altérations par Siffler dans la brume renonce à leur effacement au tour suivant mais accélère nettement la convergence des Rêves.",
                },
            },
            "temoins": [
                {
                    "id": "R9_T1",
                    "statut": "A_CODER",
                    "resume": "Matinta défendue au rang 4 avec Perchoir pointant le rang 2 libre : elle vole au rang 2, Étouffe la mobile présente et choisit Maudire pour l’Altérer.",
                },
                {
                    "id": "R9_T2",
                    "statut": "A_CODER",
                    "resume": "Matinta choisit Siffler dans la brume en retirant 2 Altérations en jeu : elle Glisse 2 Rêves d’1 rang libre à gauche et Refroidit chaque machine réveillée portant un Rouge.",
                },
            ],
            "heuristique_bot": "Vole vers le rang du Perchoir pour Étouffer la cible ; choisit Siffler dans la brume dès que 1–2 Altérations sont mûres pour fermer le Sommeil ou Refroidir.",
        },
        "R10": {
            "roles_portes": ["AUTONOMIE_A0", "TWIST_2K3", "LEVIER_REVE"],
            "est_twist": True,
            "paiement": ["P_RANG"],
            "entrees_plancher": ["POSITION_REVE", "RANG_MACHINE"],
            "entrees_synergie": ["NID", "INSECTE", "ROUGE"],
            "sorties": ["RANG_REVE", "NID_DEPLACE", "ALTERATION", "INSECTE", "BLEU"],
            "declencheurs_amorces": [],
            "vecteurs": "Glisser 1 Rêve d’1 rang à gauche + Envol de la Ruche (déménage 1 Nid avec garnison + Altérer ou Refroidir) OU Essaim spectral (+1 Insecte réserve + Altérer)",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Ruche vagabonde",
                "fenetre_badge": "OUVERTURE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_TWIST", "PIC_AVANCEE_REVE", "PIC_NID", "PIC_ALTERATION"],
                "mots_cles_plateau": {
                    "face_1": "Glisser 1 Rêve 1G · déménage 1 Nid + Altérer OU Refroidir · OU +1 Insecte + Altérer",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Glisse un Rêve et déménage une ruche",
            },
            "carte_joueur": {
                "titre_complet": "La Transe de la Ruche vagabonde",
                "pitch_ambiance": "Guidé par le songe, le nid décroche ses racines d’écorce et traverse la nuit : quand l’acier frappe la clairière, la ruche est déjà derrière lui.",
                "texte_regle": {
                    "face_1": (
                        "Défendu : après ses annulations habituelles, Glissez 1 Rêve de votre choix "
                        "d’1 rang libre vers la gauche, puis choisissez : Envol de la Ruche — "
                        "déménagez 1 Nid en jeu vers n’importe quelle parcelle forestière sans autre "
                        "Nid (en emportant tous ses Insectes, tous ses Défenseurs et son éventuelle "
                        "ponte selon la règle commune), puis Altérez 1 machine mobile du rayon rejoint "
                        "ou Refroidissez 1 machine présente sur la parcelle rejointe ; ou Essaim "
                        "spectral — prenez 1 Insecte dans la réserve de l’Essaim pour le poser sur le "
                        "rayon Entités, le rayon Insectes ou un rang 1–6 de la Réglette, puis Altérez "
                        "1 machine mobile de votre choix."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Avance vers le Sommeil tout en téléportant un Nid complet avec sa garnison (ou en injectant un Insecte + une Altération en plancher solo).",
                    "renoncement": "Déménager un Nid avec ses Défenseurs dégarnit instantanément la parcelle de départ.",
                },
            },
            "temoins": [
                {
                    "id": "R10_T1",
                    "statut": "A_CODER",
                    "resume": "Table {H, E, I} : La Transe de la Ruche vagabonde Glisse un Rêve à gauche puis téléporte un Nid avec son Défenseur et ses 2 Insectes sur la parcelle menacée d’un autre rayon et Refroidit le Bulldozer sur place.",
                },
            ],
            "heuristique_bot": "Exploite Envol de la Ruche pour projeter un Nid défendu sur une parcelle critique (ou la dernière parcelle d’un rayon pour débloquer le déploiement sur la Réglette).",
        },
        # ------------------------------------------------------------------
        # NIDS / CROISSANCE (M1 .. M5)
        # ------------------------------------------------------------------
        "M1": {
            "roles_portes": [],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["NID", "INSECTE"],
            "entrees_synergie": ["DUEL"],
            "sorties": ["INSECTE_PASSAGER", "TERRITOIRE"],
            "declencheurs_amorces": ["ICONE_INSECTE"],
            "vecteurs": "Insectes (I) embarqués en phorésie sur une machine → sautent en parade là où elle frappe → descente au ménage",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Pelage du Paresseux",
                "fenetre_badge": "PRODUCTION",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_NID", "PIC_INSECTE", "PIC_MIGRATION", "PIC_DUEL"],
                "mots_cles_plateau": {
                    "face_1": "1–2 Insectes embarquent sur 1 machine voisine · sautent à la frappe · descente ménage",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Des passagers qui voyagent sur les machines",
            },
            "carte_joueur": {
                "titre_complet": "Le Pelage du Paresseux",
                "texte_regle": {
                    "face_1": (
                        "Production (défendu) : après la production de ce Nid, vous pouvez embarquer "
                        "1 ou 2 Insectes présents sur la parcelle de ce Nid sur une machine située "
                        "sur son rayon ou sur un rayon voisin (ils deviennent des passagers et se "
                        "déplacent avec elle). Chaque fois que cette machine frappe une parcelle, "
                        "avant la résolution de la parade, vous pouvez faire sauter tout ou partie "
                        "de ses passagers sur la parcelle frappée pour aider la parade (une parade "
                        "sur la parcelle du Duel le retourne nativement sur Territoire tenu). Au "
                        "ménage, les passagers encore à bord descendent sur la parcelle où la machine "
                        "s’est arrêtée."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Embarque 1–2 Insectes en réserve mobile directement sur la machine ennemie pour parer sa frappe la plus dangereuse.",
                    "renoncement": "Quitter le Nid réduit sa garnison sous le seuil de 2 Insectes pour la Production suivante.",
                },
            },
            "temoins": [
                {
                    "id": "M1_T1",
                    "statut": "A_CODER",
                    "resume": "2 passagers embarqués sur le Bulldozer : quand il frappe la parcelle du Duel face Défi (1 Défenseur, Seuil 3), les 2 passagers sautent, parent la frappe (icône Insecte) et retournent nativement le Duel sur Territoire tenu.",
                },
                {
                    "id": "M1_T2",
                    "statut": "A_CODER",
                    "resume": "Un passager non dépensé descend au ménage sur la dernière parcelle atteinte par sa machine.",
                },
            ],
            "heuristique_bot": "Embarque 1–2 Insectes sur la machine la plus menaçante du rayon I ou voisin dès que le Nid conserve 2 Insectes (ou qu’une parade critique manque de 1–2).",
        },
        "M2": {
            "roles_portes": [],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["NID", "INSECTE"],
            "entrees_synergie": [],
            "sorties": ["PARADE_SOLDATS", "ECAILLE", "CROC"],
            "declencheurs_amorces": ["ICONE_INSECTE", "ICONE_PIEGEAGE"],
            "vecteurs": "Soldats (2 Insectes parent tout Seuil sur ce Nid) · Production défendue → Semer 1 Écaille au sac OU poster le Croc sur machine présente",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "La Termitière-Forteresse",
                "fenetre_badge": "PRODUCTION",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_NID", "PIC_INSECTE", "PIC_ECAILLE", "PIC_CROC"],
                "mots_cles_plateau": {
                    "face_1": "2 Insectes du Nid parent tout Seuil · Production = Semer 1 Écaille OU Croc sur place",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Forteresse d’argile et soldats à glu",
            },
            "carte_joueur": {
                "titre_complet": "La Termitière-Forteresse",
                "texte_regle": {
                    "face_1": (
                        "Soldats à glu : lorsqu’une machine frappe la parcelle de ce Nid, vous pouvez "
                        "défausser 2 Insectes présents sur ce Nid pour parer seuls cette frappe quel "
                        "que soit son Seuil (sans aucun Défenseur requis ; allume l’icône Insecte). "
                        "Production (défendu) : après la production de ce Nid, choisissez — Semez au "
                        "sac 1 Écaille disponible depuis la réserve Reptile ; ou, si une machine "
                        "mobile se trouve sur la parcelle de ce Nid, posez le Croc disponible depuis "
                        "la réserve Reptile sur cette parcelle."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Défend sa propre parcelle contre n’importe quel Seuil avec 2 Insectes et alimente le sac en Écailles (ou pose le Croc).",
                    "renoncement": "Dépenser 2 Insectes en Soldats à glu vide rapidement la termitière avant sa prochaine Production.",
                },
            },
            "temoins": [
                {
                    "id": "M2_T1",
                    "statut": "A_CODER",
                    "resume": "Abatteuse en Assaut à Seuil 4 sur le Nid sans Défenseur : 2 Insectes défaussés parent seuls la frappe et allument l’icône Insecte.",
                },
                {
                    "id": "M2_T2",
                    "statut": "A_CODER",
                    "resume": "Production défendue sans machine présente : 1 Écaille de la réserve Reptile est Semée au sac.",
                },
            ],
            "heuristique_bot": "Défendue tôt pour Semer des Écailles au sac et maintenir ≥ 2 Insectes capables de parer seuls un Assaut à haut Seuil.",
        },
        "M3": {
            "roles_portes": ["TWIST_2K3"],
            "est_twist": True,
            "paiement": [],
            "entrees_plancher": ["NID", "INSECTE"],
            "entrees_synergie": ["PERCHOIR"],
            "sorties": ["NID_NOMADE", "INSECTE"],
            "declencheurs_amorces": ["ICONE_INSECTE"],
            "vecteurs": "Production (Nid défendu) → déménagement avant production (1 pas, ou 2 vers/sur le rayon du Perchoir, garnison emportée) → production → Front de raid (1–2 Insectes)",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Bivouac des Légionnaires",
                "fenetre_badge": "PRODUCTION",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_TWIST", "PIC_NID", "PIC_MIGRATION", "PIC_PERCHOIR"],
                "mots_cles_plateau": {
                    "face_1": "Défendu avant prod → avance 1 pas (2 vers Perchoir) · prod · raid 1–2 Insectes",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Nid nomade guidé par le Perchoir",
            },
            "carte_joueur": {
                "titre_complet": "Le Bivouac des Légionnaires",
                "brief_illustration": (
                    "Aube : sous un tronc couché, une masse vivante de fourmis légionnaires "
                    "forme des chambres et des couloirs de leurs propres corps ; une colonne "
                    "s’étire déjà vers la parcelle voisine ; au-dessus, des oiseaux fourmiliers "
                    "suivent le front de raid, et un perchoir de vigie est planté au bout du "
                    "chemin. Bruns rouges, noirs, lumière rasante."
                ),
                "texte_regle": {
                    "face_1": (
                        "Production (défendu) : avant de produire, si ce Nid est défendu, vous pouvez "
                        "le déplacer d’1 parcelle libre adjacente (sans autre Nid ; en sautant les "
                        "Routes, y compris latéralement entre parcelles de même profondeur) — ou "
                        "jusqu’à 2 parcelles libres adjacentes en vous rapprochant ou en restant sur "
                        "le rayon désigné par le Perchoir de Vigie — en emportant simultanément tous "
                        "ses Insectes, tous ses Défenseurs et son éventuelle ponte selon la règle "
                        "commune. Puis ce Nid produit normalement et lance son Front de raid : "
                        "déplacez 1 ou 2 Insectes de ce Nid vers une parcelle ciblée adjacente."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Déplace un bastion entier (Nid + Défenseurs + Insectes) vers le point chaud du tour puis projette un Front de raid de 1–2 Insectes.",
                    "renoncement": "Exige un Défenseur sur le Nid pour lever le camp ; projeter 2 Insectes en raid expose le Nid lui-même à sa prochaine frappe.",
                },
            },
            "temoins": [
                {
                    "id": "M3_T1",
                    "statut": "A_CODER",
                    "resume": "Bivouac défendu en I·1 avec Perchoir au pied du rayon O voisin : il avance de 2 parcelles vers O avec son Défenseur et ses Insectes, produit, puis envoie 2 Insectes en Front de raid.",
                },
            ],
            "heuristique_bot": "Suit le Perchoir de Vigie ou la plus forte pression machine pour repositionner un Défenseur + Nid + Front de raid en une seule Production.",
        },
        "M4": {
            "roles_portes": ["AUTONOMIE_A0"],
            "est_twist": False,
            "paiement": [],
            "entrees_plancher": ["NID", "INSECTE", "DEFENSEUR_ATTENTE"],
            "entrees_synergie": ["TAMBOUR"],
            "sorties": ["DEFENSEUR_REDEPLOYE", "INSECTE"],
            "declencheurs_amorces": [],
            "vecteurs": "Insecte consommé à la Production → relève 1 bâtisseur en attente vers le Nid ou le Tambour (H), jusqu’à 2 fois",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Rucher des Mélipones",
                "fenetre_badge": "PRODUCTION",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_NID", "PIC_DEFENSEUR_ATTENTE", "PIC_TAMBOUR", "PIC_INSECTE"],
                "mots_cles_plateau": {
                    "face_1": "1 Insecte → relève 1 bâtisseur en attente sur le Nid OU le Tambour (max 2)",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Le miel relève les bâtisseurs couchés",
            },
            "carte_joueur": {
                "titre_complet": "Le Rucher des Mélipones",
                "texte_regle": {
                    "face_1": (
                        "Production (défendu) : après la production de ce Nid, vous pouvez défausser "
                        "1 ou 2 Insectes présents sur ce Nid. Pour chaque Insecte ainsi défaussé, "
                        "relevez 1 Défenseur couché en attente (bâtisseur ou pion couché) et posez-le "
                        "actif sur la parcelle de ce Nid ou sur la parcelle du Tambour."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Convertit des Insectes en Défenseurs actifs au tour même où un joueur a construit, effaçant le coût de construction.",
                    "renoncement": "Consomme les Insectes du Nid au lieu de les accumuler pour les parades ou les déviations.",
                },
            },
            "temoins": [
                {
                    "id": "M4_T1",
                    "statut": "A_CODER",
                    "resume": "Après construction d’un Rêve (2 bâtisseurs couchés), Le Rucher des Mélipones défendu défausse 1 Insecte pour relever 1 bâtisseur actif sur la parcelle du Tambour.",
                },
            ],
            "heuristique_bot": "Prioritaire les tours de construction ; relève en priorité un bâtisseur vers la parcelle menacée du Tambour ou du Nid.",
        },
        "M5": {
            "roles_portes": ["AUTONOMIE_A0", "LOI_PASSIVE"],
            "est_twist": False,
            "nature": "LOI_PASSIVE",
            "cycle": "PASSIF_CONTINU",
            "paiement": [],
            "entrees_plancher": ["NID_ACTIVE", "INSECTE"],
            "entrees_synergie": ["INSECTE_RANG", "POSITION_REVE"],
            "sorties": ["ALTERATION", "INSECTE_RANG", "INSECTE"],
            "declencheurs_amorces": [],
            "vecteurs": "Loi passive : Déviation ±1 vers Rêve → Altérer + recycle l’Insecte sur ce Nid (si < 2) · Production défendue → 1 Insecte vers Réglette OU Altérer",
            "double_ouverture": None,
            "tuile_plateau": {
                "nom_court": "Le Mycélium luminescent",
                "fenetre_badge": "LOI_PASSIVE",
                "icone_conseillee": None,
                "pictogrammes": ["PIC_LOI_PASSIVE", "PIC_REVE", "PIC_ALTERATION", "PIC_INSECTE"],
                "mots_cles_plateau": {
                    "face_1": "Loi · Déviation vers Rêve → Altérer + recycle si < 2 · Prod = 1 Insecte Réglette OU Altérer",
                    "face_2": None,
                    "enracine": None,
                },
                "resume_plateau": "Déviations vers Rêves Altèrent et recyclent",
            },
            "carte_joueur": {
                "titre_complet": "Le Mycélium luminescent, réseau spectral des racines noires",
                "pitch_ambiance": "Ce que l’insecte touche là-haut résonne aussitôt sous l’humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé.",
                "texte_regle": {
                    "face_1": (
                        "Spores de déviation (Loi passive) : chaque fois qu’un Insecte défaussé sur "
                        "la Réglette dévie une machine mobile (±1) sur le rang d’un Rêve, Altérez "
                        "cette machine ; de plus, si ce Nid porte strictement moins de 2 Insectes, "
                        "replacez l’Insecte défaussé sur ce Nid au lieu de le rendre à la réserve. "
                        "Filaments oniriques (Production défendue) : après la production de ce Nid, "
                        "choisissez — déplacez 1 Insecte de ce Nid directement sur un rang 1–6 de la "
                        "Réglette ; ou Altérez 1 machine mobile de votre choix."
                    ),
                    "face_2": None,
                    "enracine": None,
                },
                "decision_et_renoncement": {
                    "choix": "Nourrit la Réglette en Insectes de déviation depuis n’importe quelle parcelle (Filaments oniriques) et recycle les déviations vers les Rêves en Altérations.",
                    "renoncement": "Envoyer un Insecte sur la Réglette laisse ce Nid sous le seuil de 2 Insectes jusqu’au prochain recyclage par déviation.",
                },
            },
            "temoins": [
                {
                    "id": "M5_T1",
                    "statut": "A_CODER",
                    "resume": "Le Mycélium luminescent défendu envoie 1 Insecte sur le rang 4 (Filaments oniriques) ; au tour suivant, la déviation ±1 vers un Rêve au rang 3 Altère la machine et recycle l’Insecte sur ce Nid (< 2).",
                },
            ],
            "heuristique_bot": "Défendu dès que possible pour alimenter les rangs adjacents aux Rêves en Insectes ; déclenche le recyclage automatique sur toute déviation vers un Rêve.",
        },
    }


def build_canon_v6_4_document() -> dict[str, Any]:
    base = json.loads(V6_3_CONTRACT_PATH.read_text(encoding="utf-8"))
    overrides = _build_v6_4_overrides()

    tuiles_out: dict[str, dict[str, Any]] = {}
    casting_out: dict[str, dict[str, str]] = {}

    for sid, fam, orig, vois, alias in SLOTS_SPEC_30:
        src = copy.deepcopy(base["tuiles_ciblees"][sid])
        ov = overrides[sid]

        if fam == "GARDIEN":
            casting_out[sid] = {
                "alias_oriente": alias,
                "nom_animal": LOCKED_GARDIEN_CASTING_V6_3[sid],
                "origine": orig,
                "voisin": vois,
            }

        # Apply top-level overrides
        for k in (
            "roles_portes",
            "est_twist",
            "nature",
            "cycle",
            "paiement",
            "entrees_plancher",
            "entrees_synergie",
            "sorties",
            "declencheurs_amorces",
            "vecteurs",
            "double_ouverture",
            "temoins",
            "heuristique_bot",
        ):
            if k in ov:
                src[k] = copy.deepcopy(ov[k])

        # Synchronise union entrees = entrees_plancher + entrees_synergie
        src["entrees"] = list(
            dict.fromkeys([*src["entrees_plancher"], *src["entrees_synergie"]])
        )

        # Tags cohérents
        tags: list[str] = []
        if "AUTONOMIE_A0" in src["roles_portes"]:
            tags.append("A0")
        if orig == "I" or vois == "I":
            tags.append("INSECTES")
        for role_tag in (
            "CATALYSEUR_EVEIL",
            "LEVIER_REVE",
            "ENRACINEMENT",
            "LOI_PASSIVE",
            "TWIST_2K3",
        ):
            if role_tag in src["roles_portes"]:
                tags.append(role_tag)
        src["tags"] = tags

        # Mini-Tuile Plateau
        tp_ov = ov["tuile_plateau"]
        src["tuile_plateau"] = copy.deepcopy(tp_ov)

        # Grande Carte Joueur (conserve entite_illustree, brief_illustration, pitch_ambiance sauf surcharge, normalise apostrophes)
        cj_ov = ov["carte_joueur"]
        cj = src["carte_joueur"]
        cj["titre_complet"] = _typo(cj_ov["titre_complet"])
        cj["entite_illustree"] = _typo(cj_ov.get("entite_illustree", cj["entite_illustree"]))
        cj["brief_illustration"] = _typo(cj_ov.get("brief_illustration", cj["brief_illustration"]))
        cj["pitch_ambiance"] = _typo(cj_ov.get("pitch_ambiance", cj["pitch_ambiance"]))
        cj["texte_regle"] = {
            "face_1": _typo(cj_ov["texte_regle"]["face_1"]),
            "face_2": _typo(cj_ov["texte_regle"]["face_2"]),
            "enracine": _typo(cj_ov["texte_regle"]["enracine"]),
        }
        cj["decision_et_renoncement"] = {
            "choix": _typo(cj_ov["decision_et_renoncement"]["choix"]),
            "renoncement": _typo(cj_ov["decision_et_renoncement"]["renoncement"]),
        }

        # Normalize witness texts & bot heuristic typography
        for tm in src["temoins"]:
            tm["resume"] = _typo(tm["resume"])
        src["heuristique_bot"] = _typo(src["heuristique_bot"])
        if src["double_ouverture"] is not None:
            src["double_ouverture"] = _typo(src["double_ouverture"])

        src["statut_conception"] = "PASSE_2_AFFINE"
        src["engine_sync_status"] = "REFINED_V6_4"
        tuiles_out[sid] = src

    def _role_list(role_name: str) -> list[str]:
        return [
            f"{sid}={tuiles_out[sid]['alias_oriente']}"
            for sid, *_ in SLOTS_SPEC_30
            if role_name in tuiles_out[sid]["roles_portes"]
        ]

    doc: dict[str, Any] = {
        "_meta": {
            "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.4 (Passe 2 Affinée, 30 Tuiles Bi-Composant)",
            "schema_version": "6.4.0",
            "socle_verrouille": "6.4.0",
            "cadrage_source": "docs/cadrage_v6_4.md",
            "etape_active": "JALON_2_PASSE_2_AFFINEE",
            "statut_global": "PANEL_30_AFFINE",
            "genere_le": "2026-11-27",
            "slots_count": 30,
            "c02_supprime": True,
            "panel_id": "canon_v6_4",
            "murs_porteurs_verrouilles": list(MURS_PORTEURS_V6_3),
            "note_phase_a": (
                "Catalogue Passe 2 v6.4.0 consolidé sur les 9 évolutions du Cœur v6.4 et les 6 Verbes "
                "du Cœur. Archive Passe 1 conservée sur le tag archive/v6.3.2-panel-passe1 et dans "
                "contracts/tiles_canon_v6_3.json ; noyau PyPy v6.2 sanctuarisé jusqu'au Jalon 4."
            ),
        },
        "referentiel_pictogrammes": copy.deepcopy(DEFAULT_REFERENTIEL_PICTOGRAMMES_V6_4),
        "casting_gardiens_verrouille": casting_out,
        "carte_des_roles": {
            "statut": "CONSOLIDE_PASSE_2_V6_4",
            "roles": {
                "catalyseurs_eveil": _role_list("CATALYSEUR_EVEIL"),
                "leviers_reve": _role_list("LEVIER_REVE"),
                "synergies_enracinement": _role_list("ENRACINEMENT"),
                "lois_passives": _role_list("LOI_PASSIVE"),
                "autonomie_A0": _role_list("AUTONOMIE_A0"),
                "twists_2K3": _role_list("TWIST_2K3"),
            },
        },
        "rapport_audit_197": {
            "verdict_global": "PENDING",
            "c02_word_count_purged": True,
        },
        "tuiles_ciblees": tuiles_out,
    }

    # Audit & embed exact audit summary
    audit_rep = audit_tiles_catalog_197(doc, allow_draft=False)
    schema_errs = validate_tiles_canon_v6_4(doc, strict=True)
    if schema_errs:
        raise RuntimeError("Erreurs schéma v6.4 :\n" + "\n".join(f"  - {e}" for e in schema_errs))
    if audit_rep["verdict_global"] != "OK":
        raise RuntimeError(
            "Erreurs audit_197 v6.4 :\n" + "\n".join(f"  - {e}" for e in audit_rep["errors"])
        )

    doc["rapport_audit_197"] = {
        "verdict_global": "OK",
        "schema_source": "v6.4",
        "c02_word_count_purged": True,
        "assises_verifiees": audit_rep["assises"]["total"],
        "compositions_verifiees": audit_rep["assises"]["compositions"],
        "murs_porteurs": {
            "M1_TEMPS_BATAILLE": audit_rep["M1_TEMPS_BATAILLE"]["verdict"],
            "M2_CONSERVATION_THERMIQUE": audit_rep["M2_CONSERVATION_THERMIQUE"]["verdict"],
            "M3_INTEGRITE_PLATEAU_ET_ICONES": audit_rep["M3_INTEGRITE_PLATEAU_ET_ICONES"]["verdict"],
            "M4_AUTONOMIE_PLANCHER_SOLO": audit_rep["M4_AUTONOMIE_PLANCHER_SOLO"]["verdict"],
        },
        "compteurs": {
            "catalyseurs_eveil": audit_rep["I04_couverture_eveil"]["nombre"],
            "leviers_reve": len(audit_rep["I05_couverture_sommeil"]["leviers"]),
            "synergies_enracinement": audit_rep["I06_enracinement"]["nombre"],
            "lois_passives": audit_rep["Q01_lois_passives"]["nombre"],
            "max_lois_par_assise": audit_rep["Q01_lois_passives"]["max_par_assise"],
            "twists_2K3": audit_rep["Q02_twists_2K3"]["nombre"],
            "autonomie_A0": len(audit_rep["I02_autonomie_A0"]["tuiles"]),
        },
        "erreurs": 0,
    }

    # Re-validate after embedding rapport_audit_197
    final_errs = validate_tiles_canon_v6_4(doc, strict=True)
    if final_errs:
        raise RuntimeError("Erreurs après injection rapport_audit_197 :\n" + "\n".join(final_errs))
    return doc


def render_panel_markdown_v6_4(doc: dict[str, Any]) -> str:
    rep = doc["rapport_audit_197"]
    roles = doc["carte_des_roles"]["roles"]
    ref_pics = doc["referentiel_pictogrammes"]
    lines: list[str] = [
        "# Catalogue Canonique `v6.4` — Passe 2 Affinée (30 Tuiles Bi-Composant)",
        "",
        "**Projet :** *Amazonia : Dernier Rempart*  ",
        "**Contrat SSOT :** `contracts/tiles_canon_v6_4.json` (`schema_version = 6.4.0`, `statut_global = PANEL_30_AFFINE`)  ",
        "**Cœur associé :** `contracts/rules_canon_v6_4.json` & `contracts/physical_and_edge_invariants_v6_4.json`  ",
        f"**Audit 197 assises :** **`{rep['verdict_global']}`** (`0` erreur — `M1..M4 = OK`, `I01..I07 = OK`, `Q01..Q02 = OK`, zéro contrainte `C02`)  ",
        "",
        "## Synthèse de la Carte des Rôles (`v6.4`)",
        "",
        f"- **Catalyseurs d’Éveil (`{len(roles['catalyseurs_eveil'])}`) :** {', '.join(roles['catalyseurs_eveil'])}",
        f"- **Leviers de Rêve (`{len(roles['leviers_reve'])}`) :** {', '.join(roles['leviers_reve'])}",
        f"- **Synergies d’Enracinement (`{len(roles['synergies_enracinement'])}`) :** {', '.join(roles['synergies_enracinement'])}",
        f"- **Lois passives (`{len(roles['lois_passives'])}`, max `2`/assise) :** {', '.join(roles['lois_passives'])}",
        f"- **Autonomes `A = 0` (`{len(roles['autonomie_A0'])}`) :** {', '.join(roles['autonomie_A0'])}",
        f"- **Briques-Twists `2K3` (`{len(roles['twists_2K3'])}`) :** {', '.join(roles['twists_2K3'])}",
        "",
        "## Rappel des 6 Verbes du Cœur (`v6.4`)",
        "",
        "1. **Refroidir** : `1 Rouge existant → Bleu Surchauffe` (`M2` : zéro Bleu à sec).",
        "2. **Altérer** : `+1 Altération` (réserve `E`) sur une machine mobile sans Altération.",
        "3. **Reculer** : `−1` parcelle vers la bordure sur une machine mobile (saute les Routes).",
        "4. **Étouffer** : neutralise toute l’activation restante (jeton à `90°` + dé retiré, ou Ratissage tourné à `90°`). Le mot **cale** est exclusif au *Caïman noir*.",
        "5. **Semer au sac** : glisse `1` jeton disponible (Sabotage ou Écaille) dans le sac opaque sans allumer d’icône.",
        "6. **Glisser un Rêve** : déplace un Rêve sur la Réglette `1–6` avec ses Défenseurs dans leur état actuel (debout/couchés).",
        "",
        "---",
        "",
    ]

    sections = [
        ("Gardiens — 15 Tuiles (Casting animalier verrouillé)", "GARDIEN"),
        ("Rêves — 10 Tuiles (Humains & Entités)", "REVE"),
        ("Nids de l’Essaim — 5 Tuiles (Insectes)", "CROISSANCE"),
    ]

    for sec_title, fam_code in sections:
        lines.append(f"## {sec_title}")
        lines.append("")
        for sid, fam, orig, vois, alias in SLOTS_SPEC_30:
            if fam != fam_code:
                continue
            t = doc["tuiles_ciblees"][sid]
            tp = t["tuile_plateau"]
            cj = t["carte_joueur"]
            tr = cj["texte_regle"]
            mcp = tp["mots_cles_plateau"]
            dr = cj["decision_et_renoncement"]

            pic_badges = " · ".join(
                f"{ref_pics[p]['symbole']} `{p}`" for p in tp["pictogrammes"] if p in ref_pics
            )
            ic_str = ICON_LABELS.get(tp["icone_conseillee"], "—") if tp["icone_conseillee"] else "—"
            roles_str = ", ".join(t["roles_portes"]) if t["roles_portes"] else "Standard"

            lines.append(
                f"### {sid} (`{alias}`) — {cj['titre_complet']}"
            )
            lines.append("")
            lines.append(
                f"- **Lisière :** {PEUPLE_NAMES[orig]} → {PEUPLE_NAMES[vois]} | "
                f"**Nature :** `{t['nature']}` | **Rôles :** {roles_str} | "
                f"**Icône conseillée :** {ic_str}"
            )
            lines.append(
                f"- **Mini-Tuile (`{tp['nom_court']}`) :** *{tp['resume_plateau']}* | {pic_badges}"
            )
            lines.append(f"  - **Mots-clés Face 1 :** `{mcp['face_1']}`")
            if mcp["face_2"]:
                lines.append(f"  - **Mots-clés Face 2 :** `{mcp['face_2']}`")
            if mcp["enracine"]:
                lines.append(f"  - **Mots-clés Enraciné :** `{mcp['enracine']}`")
            lines.append(f"- **Vecteurs :** {t['vecteurs']}")
            lines.append(f"- **Ambiance :** *{cj['pitch_ambiance']}*")
            if fam == "GARDIEN":
                lines.append(f"- **Face 1 :** {tr['face_1']}")
                lines.append(f"- **Face 2 :** {tr['face_2']}")
            else:
                lines.append(f"- **Règle :** {tr['face_1']}")
            if tr["enracine"]:
                lines.append(f"- **Enraciné :** {tr['enracine']}")
            lines.append(f"- **Décision :** {dr['choix']} *(Renoncement : {dr['renoncement']})*")
            if t["double_ouverture"]:
                lines.append(f"- **Double ouverture :** {t['double_ouverture']}")
            lines.append(
                f"- **Entrées plancher :** `{', '.join(t['entrees_plancher'])}` | "
                f"**Synergies :** `{', '.join(t['entrees_synergie']) or '—'}` | "
                f"**Sorties :** `{', '.join(t['sorties'])}`"
            )
            lines.append(f"- **Heuristique bot :** {t['heuristique_bot']}")
            for tm in t["temoins"]:
                lines.append(f"  - **Témoin `{tm['id']}` (`{tm['statut']}`) :** {tm['resume']}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    doc = build_canon_v6_4_document()
    V6_4_CONTRACT_PATH.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    md = render_panel_markdown_v6_4(doc)
    PANEL_MD_V6_4_PATH.write_text(md, encoding="utf-8", newline="\n")

    rep = doc["rapport_audit_197"]
    print(
        f"build_canon_v6_4.py : OK -> {V6_4_CONTRACT_PATH.relative_to(ROOT)} & "
        f"{PANEL_MD_V6_4_PATH.relative_to(ROOT)} "
        f"(audit_197={rep['verdict_global']}, eveil={rep['compteurs']['catalyseurs_eveil']}, "
        f"leviers_reve={rep['compteurs']['leviers_reve']}, lois={rep['compteurs']['lois_passives']}, "
        f"enrac={rep['compteurs']['synergies_enracinement']}, twists={rep['compteurs']['twists_2K3']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
