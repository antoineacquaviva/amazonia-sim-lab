# GEMINI.md — Boussole Globale `amazonia-sim-lab`

## Références principales
- Architecture & cible éditoriale : `docs/PROJECT_CHARTER_V1.md`
- Référentiel Amazonia Doc Studio : `docs/AMAZONIA_STUDIO_CONTEXT.md` (application statique `docs/index.html`)
- Journal d'avancement : `STATUS.md`
- Contrat API du noyau : `contracts/core_state_api.md` (Palier 1)

## Arborescence du dépôt
- `docs/` : Amazonia Doc Studio intégré (`index.html` compatible `file://`/HTTPS, `AMAZONIA_STUDIO_CONTEXT.md`, `data/`, `scripts/`) et `PROJECT_CHARTER_V1.md`
- `engine/` : noyau déterministe (`state.py`, `rng.py`, `primitives.py`, `core_engine.py`, `telemetry.py`)
- `engine/effects/` : implémentations stateless des 100 profils de tuiles (`@register_tile`)
- `bots/` : agents `B0`, `B1`, `B2`, `B3` (Ticks 1..3, révision 2.2, graphe `economie_bot`)
- `campaigns/` : `worker_main.py` et campagnes Monte-Carlo / Sequential Halving / MAP-Elites
- `contracts/` : schémas, empreintes `kernel_locks.sha256` et API publique du noyau
- `scripts_cloud/` : orchestration locale Cloud Build / Cloud Run Jobs / Cloud Batch / DuckDB
- `tests/temoins/` : tests unitaires déterministes traduisant le champ `"temoin"` de chaque profil

## Architecture duale stricte
- **Runtime Simulation & Cloud (`engine/`, `bots/`, `campaigns/worker_main.py`)** :
  **PyPy 3.11 stdlib pure uniquement** — zéro dépendance tierce C++, zéro `numpy`/`scipy`.
- **Runtime Local & Analyse (`scripts_cloud/`, `verify_lot.py`, `tests/`)** :
  **CPython 3.12 + DuckDB** via `uv run`.

## Loi martiale
1. **Mémoire de session** : Lire `STATUS.md` en début de session et le mettre à jour en fin de session.
2. **Scellement du noyau** : Interdiction absolue de modifier un fichier listé dans `contracts/kernel_locks.sha256` sans approbation explicite de l'auteur.
3. **Porte de validation** : Exécuter `uv run python verify_lot.py` et obtenir **100 % vert** (SHA-256, AST, garde Zéro-API-LLM, cohérence Studio `docs/data/` ↔ simulateur, `ruff`, `pyright`, `pytest`, fuzzer PyPy) avant de conclure toute tâche.
4. **Verrouillage Zéro Facturation API Gemini** : Interdiction stricte d'installer `google-genai` / `google-generativeai` / `vertexai`, de lire `GEMINI_API_KEY` ou d'effectuer le moindre appel HTTP vers une API LLM payante depuis un script Python. Toute interprétation passe exclusivement par Antigravity en local et par le dépôt manuel des fichiers `digest_*.json` dans Gemini web.
5. **Maintenance Amazonia Doc Studio (`docs/`)** : Respecter impérativement `.agents/rules/rule-doc-studio.md` et `docs/AMAZONIA_STUDIO_CONTEXT.md` (Section 5) : synchronisation obligatoire des 4 couches (`docs/data/livret_v5_3.js`, `docs/data/amazonia_data_v5_3.js`, `docs/data/catalog_v5_3.json`, `docs/data/spec_formelle_v5_3.json`), patchs différentiels via Node `vm` + `JSON.stringify` validés par `new vm.Script()`, mise à jour conjointe du couple `texte`/`temoin` (Faces 2 autonomes), écriture en **UTF-8 sans BOM** (`\n`) et compatibilité statique `file://` / HTTPS.
