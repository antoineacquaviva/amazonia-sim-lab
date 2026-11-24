---
trigger: glob
description: Règles des workers Cloud PyPy, plans d'expérience et protocole A/B statistique (v6.2)
globs: "campaigns/**/*.py, scripts_cloud/**/*.py, run_campaign.py, Dockerfile*"
---

# Règles Cloud & Campagnes (`campaigns/`, `scripts_cloud/`)

## 1. Runtime Worker Cloud (`Dockerfile.worker`)
- Base `pypy:3.11-slim`, **zéro `pip install` C++** (stdlib PyPy pure uniquement).
- Upload GCS via `urllib.request` et jeton OAuth2 récupéré depuis le serveur de métadonnées GCP (`http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`).
- Pré-agrégation en RAM par `(variante, table)` écrite en shards `jsonl.gz` sur `gs://amazonia-sim-runs`.

## 2. Échantillonnage Macro, Cercles Équilibrés & Protocole Statistique
- Tirage équilibré des cercles de voisinage miroirs (`balanced_neighbor_mirror_tables`) garantissant une fréquence uniforme de chaque paire de voisins/lisières pour `N=3..6`, sur le **châssis canonique unique `P4_2233` départ décalé**.
- Intervalles de confiance à `95 %` groupés par table (`CR1`), `CVaR_20%` continue uniforme + bootstrap par grappes, dispersion inter-cercles pondérée (`non_estimable_single_circle` si 1 seul cercle), correction de Holm-Bonferroni et panel `CALIBRATION_BOT_PANEL = ("B0", "B1", "B2", "B2_OPEN")`.

## 3. Mode 4 : Évaluation A/B du Canon 0 (`30` emplacements)
- Protocole apparié strict `ACTIVE_VS_NEUTRE` (suivi exact par emplacement `tile_activations`, masquage des tuiles sous `< 1` activation/partie).
- **Interdiction absolue** d'optimiser la moyenne brute sans garde-fou : évaluer simultanément la **`CVaR_20%`** (ratio d'Arbres sauvés sur les 20 % pires tables), la charge cognitive (`mem_debt == 0`, `law_stack <= 2`) et l'équilibre des 3 fins (*Tour 8*, *Sommeil*, *Éveil*).

## 4. Micro-Forks Causaux
- Ablations causales sans biais placebo via `TargetFilter`, séparation stricte entre lot de sélection et lot d'évaluation apparié (`C_prive`, `Delta_V`, corrélation CRN `rho_delta`).

## 5. Verrouillage Zéro Facturation API Gemini / LLM
- **Interdiction absolue** d'installer `google-genai`, `google-generativeai` ou `vertexai`, de lire une variable `GEMINI_API_KEY`, ou d'effectuer le moindre appel HTTP vers une API LLM payante depuis un script Python (`scripts_cloud/`, `campaigns/`, etc.).
- Toute analyse éditoriale passe exclusivement par Antigravity en local et par le dépôt manuel des synthèses `digest_*.json` dans l'interface Gemini web.

## 6. Lancement de campagne en langage naturel & Auto-build Cloud
- Lorsque l'utilisateur décrit une hypothèse de tir en français, traduire son intention en manifeste `campaigns/<nom>.json` conforme au schéma de `campaigns/worker_main.py`, le sauvegarder, puis exécuter `uv run python run_campaign.py campaigns/<nom>.json`.
- `run_campaign.py` compare automatiquement l'empreinte SHA-256 locale des sources embarquées par `Dockerfile.worker` à `gs://amazonia-sim-runs/meta/worker_image_hash.txt` et ne déclenche Cloud Build qu'en cas de changement (sauf `--build` ou `--no-build`).
