---
trigger: glob
description: Règles des bots coopératifs muets et des 4 capteurs de télémétrie cognitive (cible v6.2)
globs: "bots/**/*.py, engine/telemetry.py"
---

# Règles des Bots (`bots/`) & Télémétrie (`engine/telemetry.py`) — Cible `v6.2`

## 1. Modélisation de la Pose des Défenseurs en Temps Réel Libre
- **Ticks discrets** `t in {1, 2, 3}` pilotés par l'urgence / opportunité privée `U_i in [0, 1]`.
- Sous paravent fermé, tous les joueurs lancent leurs dés (éliminant toute fuite sonore). Un joueur ayant tiré un jeton **Sabotage** ou **Écaille** sait en privé qu'il n'active aucune machine et devient un émetteur naturel de signaux coopératifs/altruistes au Tick 1 (construction de lisière ou soutien Furtivité voisin).
- Résolution par `U_i` décroissant avec bris d'égalité PRNG tournant `rand_u64(...)` (**zéro biais de siège 0**).
- Au 2e temps de pose (face `Réflexion` → validation `Définitif`), passes de révision par gain marginal `Delta_V_i > epsilon_r` ; dès qu'une passe produit `0` mouvement (ou clôture à `N−1` joueurs validés), validation sur `Définitif`.

## 2. Hiérarchie des Bots (`CALIBRATION_BOT_PANEL`)
- **`B0`** : bot réflexe (`K_max = 0`), strictement isolé sur `PlayerObservation`.
- **`B1`** : bot découverte (`k = 1`, bruit softmax déterministe calibrable `DEFAULT_TAU_B1 = 60.0` via `rng.py`).
- **`B2`** : bot cœur de cible (`k = 2`), économie unifiée en arbres sauvés (`bots/b2_economy.py`, `< 100` paramètres), graphe orienté `economie_bot` sur les **11 jetons `RES_*` actifs** (incluant `RES_DILUTION_SABOTAGE` pondéré par le tour `1..8`) et `TRIG_1..6` + rollouts CRN (`bots/b2_rollouts.py`).
- **`B2_OPEN`** : plafond d'information ouverte pour mesurer le coût d'asymétrie d'information `C_prive`.
- **`B3`** : bot bonus IS-MCTS / Rolling Horizon par déterminisation sur `state.clone()`.

## 3. Formules exactes des 4 capteurs (`engine/telemetry.py`)
1. `mem_debt_score` : nombre de sous-étapes traversées par tout `TransientModifier` non porté par une pièce physique du plateau (cible `v6.2` : `0.0`).
2. `law_stack_mean` & `law_stack_max` : nombre de lois passives `MOD_LOI_DU_COEUR` actives à surveiller simultanément (plafond Canon 0 : `<= 2`).
3. `fiddliness_ratio` : `physical_ops_par_tour / decisions_joueurs_par_tour` (`+1` par pion ou jeton manipulé ; un Insecte qui migre sur un rayon compte **3 ops physiques** : déplacer + retourner suivi + redresser en fin de Migration).
4. `cascade_sweeps` & `mid_combat_interrupts` : Gardiens activés par fenêtre d'interruption et nombre de balayages gauche → droite sur les 6 icônes.
