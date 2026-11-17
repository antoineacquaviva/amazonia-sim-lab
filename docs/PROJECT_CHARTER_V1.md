# Amazonia Sim Lab — Project Charter v1 ("Solo 30 Jours")

## 1. Cible métier
Simulateur Monte-Carlo Macro/Micro pour **Amazonia : Dernier Rempart** (règles **v5.3 consolidée**), aligné sur le dépôt éditorial `https://github.com/antoineacquaviva/amazonia-doc-studio` :
- **Périmètre** : 3 à 6 joueurs ($N \in \{3, 4, 5, 6\}$), 8 tours maximum par partie.
- **Matériel modélisé** : 32 emplacements de tuiles / 100 profils distincts :
  - **45 Gardiens** (`G`)
  - **31 Rêves** (`R`)
  - **19 Croissance** (`C`)
  - **5 Migration** (`M`)

## 2. Objectif éditorial
1. **Valider le cœur coopératif muet** : modéliser la révision en temps réel libre du 2e Défenseur en Étape 2.2 sans communication verbale, et mesurer l'impact des contraintes de complexité cognitive.
2. **Trier les 128 châssis ($2^7$)** par *Sequential Halving* sur blocs appariés miroirs.
3. **Converger vers un unique set canonique fixe de 32 profils** robuste sur les **127 tables circulaires** ($N = 3..6$) sans taxe de complexité cognitive (`mem_debt_score`, `law_stack`, `fiddliness_ratio`).

## 3. Architecture "Solo 30 Jours"
- **Poste local (Windows 11)** : CLI pilotée via `uv` + **CPython 3.12** + **DuckDB** pour l'orchestration, les tests `pytest`, le contrôle statique (`ruff`, `pyright`), l'agrégation analytique locale et la génération de `digest_for_llm.json` (< 30 Ko).
- **Calcul 100 % Cloud** :
  - **Cloud Run Jobs** (smoke-tests et lots rapides < 5 min, niveau gratuit) et **Cloud Batch Spot** (campagnes massives < 2 h).
  - **Image unique** `pypy:3.11-slim` (`europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest`), **zéro dépendance C++**, 100 % stdlib PyPy.
  - **Stockage intermédiaire** : écriture directe de shards pré-agrégés `jsonl.gz` sur `gs://amazonia-sim-runs` via l'API HTTP GCS + jeton OAuth2 du serveur de métadonnées GCP.
  - **Rapatriement & Synthèse** : téléchargement local des shards et requête directe via `DuckDB`.

## 4. Garde-fous d'ingénierie
- **Noyau scellé** (`contracts/kernel_locks.sha256`) : `state.py`, `rng.py`, `primitives.py`, `core_engine.py` verrouillés par empreinte SHA-256 après le Palier 1.
- **Effets stateless** : chaque profil dans `engine/effects/` passe uniquement par l'API publique `contracts/core_state_api.md` (vérification AST dans `verify_lot.py`).
- **Validation systématique** : `uv run python verify_lot.py` doit être 100 % vert avant toute clôture de lot.
