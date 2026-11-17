---
trigger: glob
description: Règles d'architecture et invariants v5.3 du noyau déterministe scellé
globs: "engine/state.py, engine/rng.py, engine/primitives.py, engine/core_engine.py"
---

# Règles du Noyau (`engine/`)

## 1. Représentation de l'état (`engine/state.py`)
- `GameState` est scellé avec `__slots__ = ("_buf", "cfg", "_rng_state")` sur un `bytearray(256)` alloué séquentiellement via `_Layout.alloc()` — **zéro magic number**.
- `clone()` s'effectue par copie brute `bytearray(self._buf)`.
- Une plage dédiée d'octets transitoires de tour est remise à zéro systématiquement en sous-étape **6.2**.
- **Isolation État Public / Privé** : `get_observation(seat_id)` masque strictement les informations privées tant que les paravents sont fermés (avant **3.2**, hors cas explicite du sacrifice `G4 B`).

## 2. Déterminisme & PRNG (`engine/rng.py`)
- PRNG déterministe adressable par compteur : `rand_event(exp_seed, rep_id, source_type, tour, entity_id, draw_idx)`.
- **Aucun `branch_id`** sur les événements comparables :
  - Jets de dés indexés par `(DICE, tour, peuple_id)`.
  - Recyclage Sabotage indexé par `(SABOTAGE_RESHUFFLE, count)` sur le multi-ensemble disponible.

## 3. Machine à états suspendable BGA-ready (`engine/core_engine.py`)
- Interface `step_until_decision() -> DecisionRequest | GameOver` et `apply_choice(choice)`.
- Le **Coordonnateur du tour** tourne en sens horaire pour trancher les ordres globaux non attribués :
  - Ordre des constructions en **3.1**.
  - Ordre d'activation des machines en Siège en **5**, sous contrainte stricte : **Abatteuse avant Bulldozer sur un même rayon**.
  - Passe circulaire `PASSER` sur les Sabotages.

## 4. Invariants métier v5.3
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
- Un **Double `(X, X)`** sans aucun Rêve en piste au début de **3.2** active normalement la carte Machine au rang `M = X`.
- **Mode 1 (Cœur symétrique)** : 0 tuile `G/R/M`, 0 piste `Bug/Colonie`, Sabotages gouvernés par l'acquéreur, fin au Tour 8.
- **Mode 2 (Asymétrie à vide)** : tuiles `G/R/M` présentes sans texte ni pouvoir propre, mais fonctions structurelles actives (Nids `+1/+2`, Rêves insérés/avancés/annulant une machine, Gardiens marqués utilisés, fins anticipées `5.3` actives) et Migrations fixées à `A/A`.
