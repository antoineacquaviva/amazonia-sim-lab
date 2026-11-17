---
name: run-campaign
description: >-
  Traduit une demande d'expérience Monte-Carlo en langage naturel en tir Cloud reproductible
  sur europe-west9 (Cloud Run Jobs gratuit <= 5 min ou Cloud Batch Spot c3d-highcpu <= 2 h),
  affiche un devis de 5 lignes après pré-vérification métier, rapatrie les shards .jsonl.gz,
  archive en Parquet via DuckDB et produit data/digests/digest_<nom_campagne>.json (< 30 Ko).
  Utiliser dès que l'auteur demande un tir, un duel de variantes ou une campagne Cloud.
---

# Skill `run-campaign` — Orchestration Cloud & Digest DuckDB

## 1. Pré-Vérification Métier Obligatoire (Avant tout tir)
Avant de construire ou lancer quoi que ce soit sur GCP, vérifier localement en Python :
1. **Disponibilité des profils** : tous les couples `(slot_id, profile)` demandés sont enregistrés dans `list_registered_tiles()` (sans `NEEDS_KERNEL_HOOK`).
2. **Activabilité géométrique sur table (`MATRICE_PAIRES`)** : si l'auteur teste une ou plusieurs tuiles `G/R/M` précises, filtrer ou stratifier automatiquement les tables `peuples` afin que les paires adjacentes génératrices de ces tuiles soient réellement présentes en lisière (toujours en paires miroirs `(Cercle, Cercle_Miroir)` avec semences CRN identiques).
3. **Garde-fou anti-boucle** : vérifier que la boucle worker invoque le moteur avec **`max_steps = 2000`** et qu'un micro-tir local de **20 parties** sous PyPy passe en `< 1 s` avant tout envoi Cloud.
4. **Choix de l'exécuteur GCP (`europe-west9`, projet `amazonia-sim`)** :
   - Durée estimée **<= 5 min** (jusqu'à ~`500 000` parties `B0` ou ~`150 000` parties `B2`) -> **Cloud Run Jobs** (`10` à `50` tâches × `2` vCPU, `1Gi`, `--workers=2`, niveau gratuit).
   - Campagne lourde **5 min à 2 h** -> **Google Cloud Batch Spot** (`provisioningModel: SPOT`, famille `c3d-highcpu-8` ou `c3d-highcpu-16`, `maxRunDuration: "7200s"`).

---

## 2. Affichage du Devis Lisible en 5 Lignes
Présenter systématiquement ce devis synthétique de **5 lignes** avant l'exécution Cloud :
1. **Objectif & Plan CRN** : variantes comparées, bots (`B0/B1/B2/B3`), `N`, châssis et nombre de tables miroirs.
2. **Volume exact** : nombre total de parties (`N_games`) et répartition par cellule/shard.
3. **Cible Cloud** : `Cloud Run Jobs` ou `Cloud Batch Spot` (`europe-west9`, nb tâches × vCPU, `--workers`).
4. **Temps & Coût estimés** : durée murale estimée (calibrée sur le micro-tir local) et coût estimé (`0,00 €` Cloud Run gratuit ou estimation Spot).
5. **Sorties** : préfixe GCS `gs://amazonia-sim-runs/<nom_campagne>/`, archive `.tmp_runs/<nom_campagne>/cells.parquet` et `data/digests/digest_<nom_campagne>.json`.

---

## 3. Exécution Cloud & Rapatriement
1. Rebuild l'image `europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest` via `gcloud builds submit --config cloudbuild.yaml .` si `engine/`, `bots/` ou `campaigns/` a été modifié depuis le dernier build.
2. Déployer et exécuter le job sur `europe-west9` en passant explicitement `--workers=<vcpu_par_tache>` (ne jamais laisser `os.cpu_count()` sur-allouer les processus sur un conteneur cgroup).
3. Rapatrier les shards `shard_*.jsonl.gz` depuis `gs://amazonia-sim-runs/<nom_campagne>/` vers `.tmp_runs/<nom_campagne>/shards/`.

---

## 4. Synthèse Analytique DuckDB & Digest `< 30 Ko`
Avec **CPython 3.12 + DuckDB** (`uv run python ...`) :
1. Convertir les shards en archive locale compressée ZSTD : `.tmp_runs/<nom_campagne>/cells.parquet`.
2. Calculer les métriques éditoriales :
   - Moyenne, écart-type CRN sur différences appariées, médiane et **`CVaR_20%`** (moyenne des 20 % pires tables/parties) sur `ratio_arbres`,
   - Durée moyenne en tours et distribution des 3 causes de fin (`TOUR_8_ATTEINT`, `REVE_RANG_1`, `REVEIL_GARDIENS`),
   - Moyennes des 4 capteurs cognitifs (`mem_debt_score`, `law_stack_mean/max`, `fiddliness_ratio`, `cascade_sweeps`) si activés,
   - Intervalles de confiance à `95 %` sur les deltas appariés CRN.
3. Écrire `data/digests/digest_<nom_campagne>.json` (UTF-8 sans BOM, LF) et vérifier `assert len(raw_bytes) < 30_000` (**strictement < 30 Ko**, prêt à glisser dans Gemini Ultra).
