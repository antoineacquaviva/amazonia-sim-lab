---
name: palier-4-canon
description: >-
  Implémente et orchestre au Palier 4 la convergence vers le Canon Unique de 32 profils via
  campaigns/map_elites.py sur Google Cloud Batch Spot (Sequential Halving des châssis, archive
  MAP-Elites 2D Complexité x Entropie optimisant la CVaR_20% inter-tables avec mutations guidées
  par régression de Shapley d'ordre 2, puis validation croisée B0 < B1 < B2 et B3 Rolling Horizon).
  Utiliser lorsque les 100 profils sont validés et que l'auteur lance le Palier 4.
---

# Skill `palier-4-canon` — Convergence vers le Canon Unique (32 Profils)

## Pré-requis d'Entrée
1. Vérifier dans `STATUS.md` que le **Palier 2** et les **Lots 01 à 11** du **Palier 3** sont cochés `[x]`.
2. Exécuter `uv run python verify_lot.py` et confirmer que les **100 profils** de `data/spec_bundle_v5_3_1.json` sont enregistrés et 100 % verts.

---

## Étape 1 — Module d'Optimisation `campaigns/map_elites.py` (Stdlib Pure PyPy 3.11)
Implémenter en Python 3.11 stdlib pure (`engine/`, `bots/`, `campaigns/` compatibles PyPy 3.11 ; régression lourde éventuelle côté orchestrateur CPython/DuckDB) :

1. **Phase A — *Sequential Halving* Final des Châssis (`128 -> Top K`)** :
   - Sur le référentiel Mode 3 (`engine/effects/mode3_reference.json`) et un échantillon stratifié de sets Mode 4, éliminer par paliers successifs de budget CRN croissant les châssis hors cible éditoriale (cible : `ratio_arbres` équilibré sans effondrement à `N=3` ni victoire triviale à `N=6`, variance maîtrisée et richesse des 3 fins).
2. **Phase B — Archive `MAP-Elites` 2D des Génomes de 32 Emplacements** :
   - **Génome** : vecteur discret de `32` choix de profils parmi les `100` profils du catalogue (`45 G`, `31 R`, `19 M`, `5 Migration`, soit $\prod_{s=1}^{32} |P_s|$ combinaisons).
   - **Descripteurs comportementaux 2D (grille `MAP-Elites`)** :
     - **Axe X — Complexité cognitive agrégée** : combinaison normalisée issue de `engine/telemetry.py` (`mem_debt_score`, `law_stack_mean`, `fiddliness_ratio`, `cascade_sweeps`).
     - **Axe Y — Entropie de Shannon des 3 causes de fin** : $H = -\sum_{c \in \{\text{T8}, \text{Rêve}, \text{Réveil}\}} p_c \log_3(p_c) \in [0, 1]$ mesurée sur `N = 3..6`.
   - **Fitness intra-cellule (`CVaR_20%` inter-tables)** :
     - Maximiser la robustesse sur les **20 % pires tables circulaires** parmi les **127 tables** (`N in {3, 4, 5, 6}`), pénalisée par l'écart à la bande cible éditoriale de taux de survie des Arbres et par toute asymétrie excessive entre paires miroirs.
   - **Mutations guidées par modèle de substitution (Shapley / interactions d'ordre 2)** :
     - Estimer sur l'historique des génomes évalués (via DuckDB / moindres carrés régularisés côté orchestrateur local) les valeurs marginales de Shapley $\phi_i(s, p)$ et les termes d'interaction de paires $\phi_{ij}((s_1, p_1), (s_2, p_2))$ entre tuiles voisines en lisière (`MATRICE_PAIRES`), afin d'orienter `70 %` des mutations vers les remplacements à fort gain marginal de `CVaR_20%` et `30 %` vers l'exploration uniforme sans biais.

---

## Étape 2 — Validation Croisée de Profondeur Stratégique (`B0 < B1 < B2 <= B3`)
Sur les **meilleurs candidats élites** extraits du front de Pareto de l'archive `MAP-Elites` :
1. Vérifier sur semences CRN appariées la monotonie stricte de compétence :
   $$\mathbb{E}[\text{ratio\_arbres}(B0)] < \mathbb{E}[\text{ratio\_arbres}(B1)] < \mathbb{E}[\text{ratio\_arbres}(B2)]$$
   ainsi que la stricte positivité de `Delta_V_negociation` (`K_max = 3` vs `K_max = 0` en `2.2`).
2. Implémenter en option dans `bots/bot_b3_rh.py` (stdlib pure) un agent **Rolling Horizon / IS-MCTS léger** (`B3`) opérant par déterminisation cohérente avec `PlayerObservation` sur `state.clone()`, et contrôler sur les **3 à 5 finalistes** qu'aucune dégénérescence ou martingale dominante ne casse le jeu à haut niveau.

---

## Étape 3 — Orchestration Cloud Batch Spot & Livrables Finaux
1. Suivre le protocole de devis et de sécurité (`max_steps = 2000`, `--workers=<vcpu>`) de la skill [run-campaign](../run-campaign/SKILL.md) pour soumettre les générations sur **Google Cloud Batch Spot** (`europe-west9`, `c3d-highcpu`, `maxRunDuration <= 7200s`).
2. Rapatrier tous les shards sur `.tmp_runs/palier4_canon/`, consolider l'archive complète en Parquet via DuckDB et générer :
   - `data/canon_unique_32.json` : les 32 profils retenus, le châssis recommandé, les scores par `N=3..6`, la `CVaR_20%` sur les 127 tables et le bilan cognitif des 4 capteurs.
   - `data/digests/digest_palier4_canon.json` (**< 30 Ko**) : synthèse exécutive prête pour arbitrage éditorial dans Gemini Ultra.
3. Cocher `[x] Palier 4` dans `STATUS.md`, passer `uv run python verify_lot.py` à **100 % vert** et commiter.
