---
trigger: glob
description: Règles des bots coopératifs muets et des 4 capteurs de télémétrie cognitive
globs: "bots/**/*.py, engine/telemetry.py"
---

# Règles des Bots (`bots/`) & Télémétrie (`engine/telemetry.py`)

## 1. Modélisation de l'Étape 2 en Temps Réel Libre
- **Ticks discrets** `t in {1, 2, 3}` pilotés par l'urgence / opportunité privée `U_i in [0, 1]`.
- Résolution par `U_i` décroissant avec bris d'égalité PRNG tournant `hash(seed, tour, sous_etape) % N` (**zéro biais de siège 0**).
- En **2.2**, jusqu'à `K_max = 4` passes de révision par gain marginal `Delta_V_i > epsilon_r` ; dès qu'une passe produit `0` mouvement, retournement simultané en *définitif*.

## 2. Hiérarchie des Bots
- **`B0`** : bot réflexe (`K_max = 0`).
- **`B1`** : bot découverte (`k = 1`, oubli stochastique si `> 2` lois actives).
- **`B2`** : bot cœur de cible (`k = 2`), graphe orienté `economie_bot` sur les 12 jetons `RES_*` et `TRIG_1..6` pondéré par le tour `1..8` + lookahead fin de tour.
- **`B3`** : bot bonus IS-MCTS / Rolling Horizon sur `state.clone()`.

## 3. Formules exactes des 4 capteurs (`engine/telemetry.py`)
1. `mem_debt_score` : nombre de sous-étapes traversées par tout `TransientModifier` non porté par un jeton physique du plateau.
2. `law_stack_mean` & `law_stack_max` : nombre de `MOD_LOI_DU_COEUR` actifs et éligibles sur le rayon à contrôler lors de chaque frappe en Étape 5.
3. `fiddliness_ratio` : `physical_ops_par_tour / decisions_joueurs_par_tour` (`+1` par pion/jeton/carte manipulé ; un Insecte qui bouge sur la roue en `4.3` compte **3 ops physiques** : déplacer + retourner suivi + redresser fin `4.3`).
4. `cascade_sweeps` & `mid_combat_interrupts` : gardiens ouverts par fenêtre d'interruption et nombre de repassages `1 -> 6`.
