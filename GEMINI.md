# GEMINI.md — Boussole Globale `amazonia-sim-lab`

## Références principales
- Architecture & cible éditoriale : `docs/PROJECT_CHARTER_V1.md`
- Référentiel Amazonia Doc Studio : `docs/AMAZONIA_STUDIO_CONTEXT.md` (application statique `docs/index.html`)
- Journal d'avancement : `STATUS.md`
- Contrat API du noyau : `contracts/core_state_api.md` (Palier 1)

## Phase active : `SOCLE_V5_5_FIGE` (Mode 4 — Catalogue actif 32 slots)
- **Socle figé `v5.5` (`schema_version = 5.5.0`)** : cœur validé et scellé dans `contracts/kernel_locks.sha256` (Piste des Tactiques fixe `T1..T6`, Rêves en coût d'activation `1_DEF_1_MACHINE` + `CLEAR_RANK_ONLY`, Piste des Gardiens pari uniforme 0/1/2 Défenseurs + passage Face 2 en `5.3` sur pari gagné, partition stricte des 6 déclencheurs sans `4.2 Nids`, Éveil 100 % Gardiens, Insectes `SLOT_BUG_CERVEAU=B` et Bouclier de lisière `SLOT_COLONISATION_GARDIENS=B`).
- **Catalogue actif Mode 4 (`engine/effects/{gardiens,reves,croissance}_v5_5.py`)** : 30 tuiles actives `STANDARD_A` (`G1..G15`, `R1..R10`, `M1..M5`) + 2 slots de migration intégrés = 32 slots exécutables et compatibles double activation Gardiens / Face 2 en `5.3`.
- **Archive des 100 tuiles v5.3** : gelée sur le tag Git `archive/v5.4.3-legacy-100-tiles` et conservée hors-exécution dans `archive/legacy_tiles_v5_3/`, avec banque d'idées dans `archive/banque_idees_tuiles_v5_3.md`.

## Arborescence du dépôt
- `docs/` : Amazonia Doc Studio intégré (`index.html` compatible `file://`/HTTPS, `AMAZONIA_STUDIO_CONTEXT.md`, `data/*_v5_5.*`, `scripts/`) et `PROJECT_CHARTER_V1.md`
- `engine/` : noyau déterministe scellé (`state.py`, `rng.py`, `primitives.py`, `core_engine.py`, `telemetry.py`)
- `engine/effects/` : catalogue stateless `@register_tile` actif v5.5 (`gardiens_v5_5.py`, `reves_v5_5.py`, `croissance_v5_5.py`)
- `bots/` : agents `B0`, `B1`, `B2`, `B3` (Ticks 1..3, révision 2.2, graphe `economie_bot`)
- `campaigns/` : `worker_main.py`, `digest_builder.py` et manifestes `campaigns/manifests/` (dont `baseline_mode4_v5_5.json`)
- `contracts/` : `CORE_FREEZE_CRITERIA.md`, empreintes scellées `kernel_locks.sha256` (v5.5), `studio_rules_guards.json` et `core_state_api.md`
- `scripts_cloud/` : orchestration locale Cloud Build / Cloud Run Jobs / Cloud Batch / DuckDB
- `archive/` : stock legacy 100 tuiles (`legacy_tiles_v5_3/`) et banque d'idées (`banque_idees_tuiles_v5_3.{md,json}`)

## Architecture duale stricte
- **Runtime Simulation & Cloud (`engine/`, `bots/`, `campaigns/worker_main.py`)** :
  **PyPy 3.11 stdlib pure uniquement** — zéro dépendance tierce C++, zéro `numpy`/`scipy`.
- **Runtime Local & Analyse (`scripts_cloud/`, `verify_lot.py`, `tests/`)** :
  **CPython 3.12 + DuckDB** via `uv run`.

## Loi martiale
1. **Mémoire de session** : Lire `STATUS.md` en début de session et le mettre à jour en fin de session.
2. **Scellement du noyau** : Le socle `v5.5` est officiellement scellé dans `contracts/kernel_locks.sha256`. Interdiction absolue de modifier un fichier listé dans `kernel_locks.sha256` sans approbation explicite de l'auteur.
3. **Porte de validation** : Exécuter `uv run python verify_lot.py` et obtenir **100 % vert** (SHA-256, AST, garde Zéro-API-LLM, cohérence Cœur Studio `docs/data/` ↔ simulateur, `ruff`, `pyright`, `pytest`, fuzzer PyPy Modes 1, 2 & 4) avant de conclure toute tâche.
4. **Verrouillage Zéro Facturation API Gemini** : Interdiction stricte d'installer `google-genai` / `google-generativeai` / `vertexai`, de lire `GEMINI_API_KEY` ou d'effectuer le moindre appel HTTP vers une API LLM payante depuis un script Python. Toute interprétation passe exclusivement par Antigravity en local et par le dépôt manuel des fichiers `digest_*.json` dans Gemini web.
5. **Maintenance Amazonia Doc Studio (`docs/`)** : Maintenir la synchronisation stricte des 4 couches `v5.5` (`livret_v5_5.js`, `amazonia_data_v5_5.js`, `catalog_v5_5.json`, `spec_formelle_v5_5.json` + `studio_rules_guards.json`) via Node `vm` + `JSON.stringify` validé par `new vm.Script()`, en **UTF-8 sans BOM** (`\n`) et compatibilité statique `file://` / HTTPS, zéro jargon interne dans le livret joueur.
6. **Hygiène Git obligatoire** : Toujours démarrer chaque session par `git pull --ff-only origin main` avant toute lecture, édition ou exécution, et toujours terminer par un `git status` propre + `git push origin main` (après passage de `uv run python verify_lot.py` 100 % vert si du code ou le Studio a été modifié).
7. **Lancement de campagne en langage naturel** : Lorsque l'utilisateur décrit une hypothèse de tir en français, traduire son intention en manifeste `campaigns/<nom>.json` conforme au schéma de `campaigns/worker_main.py`, le sauvegarder, puis exécuter `uv run python run_campaign.py campaigns/<nom>.json`.
