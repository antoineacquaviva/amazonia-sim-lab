---
trigger: glob
description: Règles des workers Cloud PyPy, plans d'expérience et optimisation MAP-Elites
globs: "campaigns/**/*.py, scripts_cloud/**/*.py, run_campaign.py, Dockerfile*"
---

# Règles Cloud & Campagnes (`campaigns/`, `scripts_cloud/`)

## 1. Runtime Worker Cloud (`Dockerfile.worker`)
- Base `pypy:3.11-slim`, **zéro `pip install` C++** (stdlib PyPy pure uniquement).
- Upload GCS via `urllib.request` et jeton OAuth2 récupéré depuis le serveur de métadonnées GCP (`http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`).
- Pré-agrégation en RAM par `(chassis, set_tuiles, table)` écrite en shards `jsonl.gz` sur `gs://amazonia-sim-runs`.

## 2. Échantillonnage Macro & Sequential Halving
- Blocs indépendants en paires `(Cercle, Cercle_Miroir)` (`paired_mirror_blocks`), incluant obligatoirement les 6 cercles de couverture complète :
  `M-E-I`, `M-R-O`, `H-E-I`, `M-R-H-I`, `M-O-E-H-I`, `M-H-O-I-R-E`.
- Intervalles de confiance calculés **uniquement inter-blocs**.
- Tri des **128 châssis** par *Sequential Halving*.

## 3. Mode 4 : Recherche du Canon Unique (32 tuiles)
- **Interdiction absolue** d'un algorithme génétique optimisant la moyenne brute.
- Implémenter **`MAP-Elites` 2D** :
  - **Axe X** : charge cognitive (`mem_debt + law_stack`).
  - **Axe Y** : entropie de Shannon des 3 fins.
  - **Objectif** : maximiser la **`CVaR_20%`** (ratio d'Arbres sauvés sur les 20 % pires tables circulaires).
  - **Mutation** : opérateur guidé par régression de **Shapley d'ordre 2**.

## 4. Micro-Forks
- Séparation stricte entre le lot de sélection des coups candidats et le lot d'évaluation apparié (`C_prive`, écart `g`, courbe d'inversion `rho_delta`).

## 5. Verrouillage Zéro Facturation API Gemini / LLM
- **Interdiction absolue** d'installer `google-genai`, `google-generativeai` ou `vertexai`, de lire une variable `GEMINI_API_KEY`, ou d'effectuer le moindre appel HTTP vers une API LLM payante depuis un script Python (`scripts_cloud/`, `campaigns/`, etc.).
- Toute analyse éditoriale passe exclusivement par Antigravity en local et par le glisser-déposer manuel des synthèses `digest_*.json` (`< 30 Ko`) dans l'interface Gemini web.

## 6. Lancement de campagne en langage naturel & Auto-build Cloud
- Lorsque l'utilisateur décrit une hypothèse de tir en français, traduire son intention en manifeste `campaigns/<nom>.json` conforme au schéma de `campaigns/worker_main.py`, le sauvegarder, puis exécuter `uv run python run_campaign.py campaigns/<nom>.json`.
- `run_campaign.py` compare automatiquement l'empreinte SHA-256 locale des sources embarquées par `Dockerfile.worker` à `gs://amazonia-sim-runs/meta/worker_image_hash.txt` et ne déclenche Cloud Build qu'en cas de changement (sauf `--build` pour forcer ou `--no-build` pour sauter).
