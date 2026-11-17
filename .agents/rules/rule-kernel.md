---
trigger: glob
description: Règles d'architecture et invariants v5.3 du noyau déterministe scellé
globs: "engine/state.py, engine/rng.py, engine/primitives.py, engine/core_engine.py"
---

# Règles du Noyau (`engine/`)

## 1. Représentation de l'état (`engine/state.py`)
- `GameState` est scellé avec `__slots__ = ("_buf", "_continuation", "cfg")` sur un `bytearray(384)` (`STATE_BUF_SIZE = 384`, 6 cache lines) alloué séquentiellement via `_Layout.alloc()` — **zéro magic number**.
- `clone()` s'effectue par copie brute `bytearray(self._buf)` et copie légère de `_continuation`.
- Une plage dédiée d'octets transitoires de tour est remise à zéro systématiquement en sous-étape **6.2**.
- **Isolation État Public / Privé** : `get_observation(seat_id)` masque strictement les informations privées tant que les paravents sont fermés (avant **3.2**, hors cas explicite du sacrifice `G4 B`).

## 2. Déterminisme & PRNG (`engine/rng.py`)
- PRNG déterministe adressable par compteur : `rand_event(exp_seed, rep_id, source_type, tour, entity_id, draw_idx)`.
- **Aucun `branch_id`** sur les événements comparables :
  - Jets de dés indexés par `(DICE, tour, peuple_id)` (uniquement pour les joueurs ayant tiré une carte Machine).
  - Mélange du paquet Machine (incluant les cartes Sabotage intégrées définitivement) indexé par `(MACHINE_DECK_SHUFFLE, tour)`.

## 3. Machine à états suspendable BGA-ready (`engine/core_engine.py`)
- Interface `step_until_decision() -> DecisionRequest | GameOver` et `apply_choice(choice)`.
- Le **Coordonnateur du tour** tourne en sens horaire pour trancher les ordres globaux non attribués :
  - Ordre des constructions en **3.1**.
  - Ordre d'activation des machines en Siège en **5**, sous contrainte stricte : **Abatteuse avant Bulldozer sur un même rayon**.

## 4. Invariants métier v5.3
- **Dés épurés (sans double aux dés)** : seul un joueur ayant pioché une carte Machine lance 2D6 et retient `M = min(D1, D2)` (ou `max` sous Loi). Un joueur tirant une carte Sabotage ou sans carte en pénurie ne lance pas de dés.
- **Sabotage par dilution permanente** : toutes les cartes Sabotage sont identiques et sans effet propre (réserve illimitée). Acquérir un Sabotage (`4.1`, `4.2`, tuiles) ajoute définitivement `+1` carte Sabotage au paquet Machine (remélangée en **6.3**, allume `3. Sabotage`). Tirer une carte Sabotage en Étape 1 fait perdre l'activation du Contremaître pour le tour.
- **Siège `T4` & Apprentissage (`A10`)** : une machine en Siège `T4` attaque de manière autonome en **5** même si `T4` est éjectée ; en **6.1**, elle génère normalement de l'Apprentissage sur `T4` si et seulement si `T4` figure encore sur la piste.
- **Seuil Imprimé fixe** : `P4_2233` `[2, 2, 3, 3]` ou `P5_22233` `[2, 2, 2, 3, 3]`, indépendant du nombre d'Arbres ou de Souches.
- **Furtivité à 4 emplacements jumeaux** : entrer sur un emplacement tire l'autre pion sur le jumeau de la rive choisie ; retourner `réflexion -> définitif` s'effectue sur place.
- **Chaîne des 4 parades** (zéro dette, zéro verrouillage) :
  1. `Jaguar` (2 bleus)
  2. `Harpie`
  3. `Piège Embuscade` (si `Déf >= 1`)
  4. `Parade classique` (défausse immédiate des Insectes)
- **Routes** : sautées le long d'un rayon, infranchissables latéralement.
- **Nids** : un Nid est indivisible en **4.2** avant balayage.
- **Cascades Gardiens** : balayage à plat `1 -> 6` avec marquage utilisé immédiat.
- **Conditions de fin en 5.3** : Tour 8 atteint, Rêve au rang 1, ou Réveil des Gardiens fixe `min(N, G0, 5)` si `G0 >= 3` (+ exception `R9 B` en **6.2**).

## 5. Définition exacte des Modes 1 & 2
- **Mode 1 (Cœur symétrique)** : 0 tuile `G/R/M`, 0 piste `Bug/Colonie`, Sabotage par dilution permanente du paquet Machine actif (via `4.1`), fin au Tour 8.
- **Mode 2 (Asymétrie à vide)** : tuiles `G/R/M` présentes sans texte ni pouvoir propre, mais fonctions structurelles actives (Nids `+1/+2`, Rêves insérés/avancés/annulant une machine sur dé `M`, Gardiens marqués utilisés, fins anticipées `5.3` actives) et Migrations fixées à `A/A`.
