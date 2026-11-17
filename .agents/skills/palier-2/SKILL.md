---
name: palier-2
description: >-
  Construit et valide le Palier 2 du simulateur (joueurs virtuels coopératifs muets, capteurs
  de charge mentale et premier lot pilote de tuiles) : utiliser dès que l'auteur demande de
  passer à l'étape suivante du simulateur après le socle, de coder les joueurs virtuels et
  la coopération sous paravent, ou de lancer le Palier 2.
---

# Skill `palier-2` — Exécution Autonome du Palier 2

## Pré-requis & Lecture Initiale
1. Lire `GEMINI.md`, `STATUS.md`, `.agents/rules/rule-bots-telemetry.md`, `.agents/rules/rule-kernel.md` et `contracts/core_state_api.md`.
2. Respecter l'architecture duale stricte : `engine/`, `bots/` et `campaigns/` doivent rester **100 % Python 3.11 stdlib pure** (compatible PyPy 3.11, zéro `numpy`/`scipy`/`duckdb`).

---

## Étape 1 — Capteurs Cognitifs (`engine/telemetry.py`)
Implémenter un collecteur léger optionnel (`TelemetryTracker | None = None`) mesurant exactement les 4 formules de `.agents/rules/rule-bots-telemetry.md` :
1. **`mem_debt_score`** : nombre cumulé de sous-étapes (`step`) traversées par chaque `TransientModifier` actif non porté par un jeton physique du plateau (ex. `TRANS_PARCEL_SEUIL_MOD`, `TRANS_MACHINE_SEUIL_MOD`, `TRANS_GLOBAL_SEUIL_MOD`, `TRANS_PARCEL_FLAGS`, `TRANS_PENDING_APPRENTISSAGE`).
2. **`law_stack_mean` & `law_stack_max`** : nombre d'effets `MOD_LOI_DU_COEUR` actifs et éligibles sur le rayon ciblé à évaluer lors de chaque frappe Machine en Étape 5 (`5.1` et `5.2`).
3. **`fiddliness_ratio`** : `physical_ops_par_tour / max(1, decisions_joueurs_par_tour)` :
   - `+1` par pion, jeton ou carte physiquement posé/déplacé/retourné/retiré ;
   - **Règle spéciale `4.3`** : chaque Insecte déplacé d'un cran sur la roue compte **3 opérations physiques** (déplacer + coucher/suivi + redresser en fin de `4.3`).
4. **`cascade_sweeps` & `mid_combat_interrupts`** : nombre de Gardiens ouverts par fenêtre d'interruption et nombre de repassages ascendants `1 -> 6` dans `sweep_gardiens`.

> **Protocole d'ouverture contrôlée du noyau (si nécessaire)** :
> Si `telemetry.py` requiert 2 ou 3 points d'accroche légers dans `engine/core_engine.py` ou `engine/primitives.py` (`telemetry: TelemetryTracker | None = None`, coût zéro quand `None`), demander ou vérifier l'autorisation explicite de l'auteur, appliquer l'instrumentation minimale sans altérer aucun invariant métier, régénérer `contracts/core_state_api.md` via `uv run python scripts_cloud/export_api_doc.py`, mettre à jour `contracts/kernel_locks.sha256` et re-sceller immédiatement.

---

## Étape 2 — Bots Coopératifs Muets `B1` & `B2` (`bots/`)
1. **`bots/belief_and_ticks.py`** :
   - Croyance bayésienne légère sur les mains adverses sous paravent (`PlayerObservation` uniquement — zéro accès à `state._buf` ni à `DECK_CARDS`).
   - **Ticks discrets `t in {1, 2, 3}`** en `2.1` et `2.2` : calcul de l'urgence/opportunité privée `U_i in [0, 1]`, résolution par `U_i` décroissant avec bris d'égalité PRNG tournant `rand_u64(exp_seed, rep_id, SRC_BOT_TIEBREAK, tour, sous_etape, seat)` (**zéro biais de siège 0**).
   - **Émetteur altruiste Sabotage** : un joueur ayant tiré une carte `CARD_SABOTAGE` (pas de dés, aucune machine activée par sa main) émet prioritairement un signal coopératif au **Tick 1** (pose sur tuile `G/R/M` en `3.1` ou ouverture d'un binôme Furtivité voisin).
   - **Révision `2.2`** : jusqu'à `K_max = 4` passes ; un siège ne déplace son 2e Défenseur que si le gain marginal estimé dépasse `Delta_V_i > epsilon_r` ; arrêt immédiat dès qu'une passe produit `0` mouvement.
2. **`bots/heuristic_engine.py`** :
   - **`B1` (Découverte, `k = 1`)** : évaluation tactique à 1 coup + oubli stochastique contrôlé via `rng.py` dès que `> 2` lois `MOD_LOI_DU_COEUR` sont actives simultanément.
   - **`B2` (Cœur de cible, `k = 2`)** : lecture dynamique du graphe orienté `economie_bot` extrait de `data/spec_bundle_v5_3_1.json` sur les 12 ressources `RES_*` (incluant `RES_DILUTION_SABOTAGE` fortement pondérée aux Tours `1..5` et faiblement aux Tours `7..8`) et les signaux `TRIG_1..6`, avec lookahead de fin de tour (`5.1 -> 6.2`).
   - Ajouter un test strict d'isolation dans `tests/` prouvant que `B1` et `B2` produisent un choix identique lorsque seule la main cachée d'un voisin change sous paravent fermé (`paravents_ouverts == False`).

---

## Étape 3 — Plans Expérimentaux & Micro-Forks (`campaigns/designs.py`)
1. **`paired_mirror_blocks`** : générateur déterministe des blocs en paires miroirs `(Cercle, Cercle_Miroir)` intégrant les **6 cercles de couverture complète** sur `N in {3, 4, 5, 6}` avec semences CRN partagées (`exp_seed`, `rep_id`).
2. **`micro_fork`** : sur un état `state.clone()` en début d'Étape `2.2`, bifurcations contrôlées (`K_max = 0` vs `K_max = 3` passes de révision, et comparaison information privée vs paravents révélés en contrefactuel) séparant strictement l'échantillon de sélection et l'échantillon d'évaluation pour estimer sans biais :
   - `Delta_V_negociation` (gain net en ratio d'Arbres de la révision `2.2` muette),
   - `C_prive` (coût d'asymétrie d'information sous paravent),
   - `g` et `rho_delta` (corrélation inter-réplications CRN).

---

## Étape 4 — Lot Pilote des 8 Primitives (`Lot 01`)
Activer et suivre intégralement la skill [code-lot](../code-lot/SKILL.md) pour usiner **Lot 01** (`G1:A`, `G2:A`, `G4:A`, `G6:A`, `G7:A`, `G10:A`, `R5:A`, `G9:C`) dans `engine/effects/lot_01.py` et ses 8 tests témoins dans `tests/temoins/test_lot_01.py`.

---

## Étape 5 — Tir Scientifique Cloud Run Jobs & Clôture
1. Passer `uv run python verify_lot.py` à **100 % vert** (`6/6` portes, incluant le fuzzer PyPy avec `B0/B1/B2` et `Lot 01`, toujours sous garde-fou `max_steps = 2000`).
2. Exécuter sur **Cloud Run Jobs** (`europe-west9`, image `worker-pypy:latest`) la campagne Palier 2 :
   - Validation `K_max = 3` vs `K_max = 0` avec `B1/B2` (`micro_fork` + `telemetry.py`),
   - Premier tri *Sequential Halving* des **128 châssis** en Modes 1 et 2 sur blocs miroirs.
3. Agréger les shards `.jsonl.gz` en Parquet via **DuckDB** et écrire `data/digest_palier2_coeur_muet.json` (**< 30 Ko**).
4. Cocher `[x] Palier 2` et `[x] Lot 01` dans `STATUS.md`, revérifier `uv run python verify_lot.py` et créer un commit propre.
