# GEMINI.md — Boussole Globale `amazonia-sim-lab`

## Références principales
- Architecture & cible éditoriale : `docs/PROJECT_CHARTER_V1.md`
- Référentiel Amazonia Doc Studio : `docs/AMAZONIA_STUDIO_CONTEXT.md` (application statique `docs/index.html`)
- Journal d'avancement : `STATUS.md`
- Contrat API du noyau : `contracts/core_state_api.md` (Palier 1)

## Phase active : `CORE_STABILIZATION` (Mode 2 à blanc)
- **Priorité** : stabiliser et équilibrer le **cœur symétrique Mode 2** (tuiles Gardiens, Rêves et Croissance jouables sans effets personnalisés) jusqu'à validation de [`contracts/CORE_FREEZE_CRITERIA.md`](contracts/CORE_FREEZE_CRITERIA.md).
- **Archive des 100 tuiles v5.3** : gelée sur le tag Git `archive/v5.4.3-legacy-100-tiles` et déplacée hors-exécution dans `archive/legacy_tiles_v5_3/`, avec une banque d'idées créative dans `archive/banque_idees_tuiles_v5_3.md`. Ne plus maintenir le stock historique de 100 tuiles tant que le *Core Freeze* n'est pas prononcé.

## Arborescence du dépôt
- `docs/` : Amazonia Doc Studio intégré (`index.html` compatible `file://`/HTTPS, `AMAZONIA_STUDIO_CONTEXT.md`, `data/`, `scripts/`) et `PROJECT_CHARTER_V1.md`
- `engine/` : noyau déterministe (`state.py`, `rng.py`, `primitives.py`, `core_engine.py`, `telemetry.py`)
- `engine/effects/` : registre stateless `@register_tile` prêt pour la future reconception incrémentale post-*Core Freeze* (`LOADED_LOT_MODULES = ()` en phase Cœur)
- `bots/` : agents `B0`, `B1`, `B2`, `B3` (Ticks 1..3, révision 2.2, graphe `economie_bot`)
- `campaigns/` : `worker_main.py` et campagnes Monte-Carlo / Sequential Halving
- `contracts/` : `CORE_FREEZE_CRITERIA.md`, empreintes `kernel_locks.sha256` (dégelées pendant `CORE_STABILIZATION`), `studio_rules_guards.json` et `core_state_api.md`
- `scripts_cloud/` : orchestration locale Cloud Build / Cloud Run Jobs / Cloud Batch / DuckDB
- `archive/` : stock legacy 100 tuiles (`legacy_tiles_v5_3/`) et banque d'idées (`banque_idees_tuiles_v5_3.{md,json}`)

## Architecture duale stricte
- **Runtime Simulation & Cloud (`engine/`, `bots/`, `campaigns/worker_main.py`)** :
  **PyPy 3.11 stdlib pure uniquement** — zéro dépendance tierce C++, zéro `numpy`/`scipy`.
- **Runtime Local & Analyse (`scripts_cloud/`, `verify_lot.py`, `tests/`)** :
  **CPython 3.12 + DuckDB** via `uv run`.

## Loi martiale
1. **Mémoire de session** : Lire `STATUS.md` en début de session et le mettre à jour en fin de session.
2. **Scellement du noyau** : Pendant `CORE_STABILIZATION`, `contracts/kernel_locks.sha256` est volontairement dégelé pour permettre des itérations rapides sur le cœur Mode 2. Dès que `kernel_locks.sha256` contient des empreintes (après *Core Freeze*), interdiction absolue de modifier un fichier listé sans approbation explicite de l'auteur.
3. **Porte de validation** : Exécuter `uv run python verify_lot.py` et obtenir **100 % vert** (SHA-256, AST, garde Zéro-API-LLM, cohérence Cœur Studio `docs/data/` ↔ simulateur, `ruff`, `pyright`, `pytest`, fuzzer PyPy Modes 1 & 2) avant de conclure toute tâche.
4. **Verrouillage Zéro Facturation API Gemini** : Interdiction stricte d'installer `google-genai` / `google-generativeai` / `vertexai`, de lire `GEMINI_API_KEY` ou d'effectuer le moindre appel HTTP vers une API LLM payante depuis un script Python. Toute interprétation passe exclusivement par Antigravity en local et par le dépôt manuel des fichiers `digest_*.json` dans Gemini web.
5. **Maintenance Amazonia Doc Studio (`docs/`)** : En phase `CORE_STABILIZATION`, maintenir la cohérence du **Cœur** (`spec_formelle`, `livret`, `CHASSIS_AXES_SPEC`, topologies, `studio_rules_guards.json`) via Node `vm` + `JSON.stringify` validé par `new vm.Script()`, en **UTF-8 sans BOM** (`\n`) et compatibilité statique `file://` / HTTPS — sans obligation de mettre à jour les 100 profils archivés du catalogue.
6. **Hygiène Git obligatoire** : Toujours démarrer chaque session par `git pull --ff-only origin main` avant toute lecture, édition ou exécution, et toujours terminer par un `git status` propre + `git push origin main` (après passage de `uv run python verify_lot.py` 100 % vert si du code ou le Studio a été modifié).
7. **Lancement de campagne en langage naturel** : Lorsque l'utilisateur décrit une hypothèse de tir en français, traduire son intention en manifeste `campaigns/<nom>.json` conforme au schéma de `campaigns/worker_main.py`, le sauvegarder, puis exécuter `uv run python run_campaign.py campaigns/<nom>.json`.
