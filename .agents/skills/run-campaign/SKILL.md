---
name: run-campaign
description: >-
  Lance des simulations de parties et répond aux questions d'équilibrage en français courant :
  utiliser dès que l'auteur demande de tester une idée, simuler des parties, mesurer l'effet
  d'une règle, comparer des profils de tuiles, observer comment une partie tourne, vérifier la
  difficulté de 3 à 6 joueurs ou chercher de bonnes configurations.
---

# Skill `run-campaign` — Simulations à la Demande & Synthèse Auteur (`v6.2`)

## 1. Pré-Vérification Métier en Coulisses (Silencieuse pour l'Auteur)
Avant de lancer une simulation, l'agent vérifie seul en arrière-plan :
1. **Disponibilité des tuiles** : tous les profils concernés sont enregistrés dans `list_registered_tiles()` (sans `NEEDS_KERNEL_HOOK`).
2. **Présence réelle autour de la table (`MATRICE_PAIRES`)** : si l'auteur teste une ou plusieurs tuiles `G/R/M`, filtrer automatiquement les cercles équilibrés (`balanced_neighbor_mirror_tables`) où ces tuiles sont en jeu, sur les mêmes tirages aléatoires CRN.
3. **Sécurité & rapidité** : garde-fou `max_steps = 2000` actif et micro-essai local de **20 parties** sous PyPy en `< 1,5 s`.
4. **Choix automatique du moteur d'exécution en coulisses (sans exposer le jargon à l'auteur)** :
   - Question ciblée sur la révision ou l'asymétrie d'information -> **analyse par bifurcations causales** (`campaigns/designs.py`).
   - Tir rapide **<= 5 min** -> exécution parallèle gratuite Cloud Run Jobs (`europe-west9`, `--workers=2`).
   - Recherche longue **5 min à 2 h** -> Cloud Batch Spot (`europe-west9`, `c3d-highcpu`, `maxRunDuration: "7200s"`).
   - **Zéro appel API LLM payant** : interdiction absolue d'appeler une API Gemini/Vertex depuis Python.

---

## 2. Devis de Validation en 5 Lignes (Français Clair d'Auteur, Zéro Jargon Cloud)
Toujours présenter ce devis simple de **5 lignes** en français naturel avant de lancer le calcul :
1. **Question testée** : reformulation limpide de l'hypothèse de jeu étudiée.
2. **Ce qu'on compare** : règles, tuiles ou comportements de joueurs virtuels mis face à face.
3. **Tables & nombre de joueurs couverts** : configurations de peuples et tailles de table (`3`, `4`, `5` et/ou `6` joueurs, avec miroirs).
4. **Volume & durée estimée** : nombre total de parties simulées et temps d'attente estimé (en secondes ou minutes).
5. **Coût estimé** : **`0 €`** (palier gratuit) ou montant estimé en euros sur les crédits.

---

## 3. Exécution & Rapatriement Automatique
1. Exécuter `uv run python run_campaign.py campaigns/<nom>.json` (auto-détection du build Docker `worker-pypy` via empreinte SHA-256).
2. Exécuter le tir sur `europe-west9` avec `--workers=<vcpu_par_tache>` et rapatrier les shards dans `.tmp_runs/<nom_campagne>/shards/`.

---

## 4. Synthèse Analytique DuckDB & Dossier Auto-Portant (`< 35 Ko`)
Avec **CPython 3.12 + DuckDB** et `campaigns/digest_builder.py` :
1. Archiver les données détaillées en `.tmp_runs/<nom_campagne>/cells.parquet` (compression ZSTD).
2. Calculer les indicateurs utiles à l'auteur :
   - Taux moyen d'Arbres sauvés, médiane et **pire quintile des tables (`CVaR_20%`, bootstrap par grappes)** ;
   - Durée moyenne en tours et répartition des 3 fins (*Fin du Tour 8*, *Sommeil du Contremaître*, *Éveil de la Forêt*) ;
   - Charge mentale mesurée par les 4 capteurs (`mem_debt`, `law_stack`, manipulations par décision, cascades) ;
   - Marges d'incertitude à `95 %` groupées par table (`CR1`) et dispersion inter-cercles pondérée.
3. Appeler `write_digest_and_prompt_files("<nom_campagne>", ...)` pour générer (UTF-8 sans BOM, LF) :
   - `data/digests/digest_<nom_campagne>.json` embarquant `"active_core_rules"` (dérivé de `contracts/rules_canon_v6_2.json` via `data/spec_bundle_v6_0.json`) et `"tested_tiles_rules"` ;
   - `data/digests/PROMPT_GEMINI_<nom_campagne>.md` avec les consignes de restitution éditoriale auteur.

---

## 5. Pont Zéro-Friction Mobile Android & PC (`scripts_cloud/publish_digest.py`)
En fin de campagne, publier dans `docs/digests/` (+ mise à jour `docs/digests/index.json`) pour copie en 1 tap depuis Amazonia Doc Studio, et optionnellement synchroniser via `scripts_cloud/publish_digest.py` sans aucune API LLM payante.
