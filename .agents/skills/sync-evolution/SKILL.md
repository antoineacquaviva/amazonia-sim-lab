---
name: sync-evolution
description: >-
  Synchronise et met à jour le simulateur et Amazonia Doc Studio après une évolution d'auteur
  sur les contrats SSOT v6.2 : utiliser dès que l'auteur modifie des règles, des invariants ou
  des textes de tuiles, ou demande de resynchroniser Studio et simulateur.
---

# Skill `sync-evolution` — Synchronisation SSOT `v6.2` (Contrats → Studio → Simulateur)

## 1. Protocole Micro-ADR (avant toute modification de règle)
Avant d'éditer un contrat dans `contracts/`, répondre brièvement aux **4 questions du Micro-ADR** définies dans `contracts/CORE_FREEZE_CRITERIA.md` (invariant `INV-XX` touché, impact matériel/cas limite, tuiles Canon 0 / modules impactés, tests & garde-fous).

## 2. Mise à Jour de la Source Unique de Vérité (`contracts/`)
1. Mettre à jour exclusivement la source concernée :
   - Règles & constantes : `contracts/rules_canon_v6_2.json` ;
   - Invariants matériels, cas limites et gouvernance : `contracts/physical_and_edge_invariants.json` (`INV-01..INV-22`) ;
   - Catalogue des 30 tuiles Canon 0 : `contracts/tiles_canon_v6_2.json`.
2. Recompiler **tous** les artefacts dérivés en une seule commande :
   ```bash
   uv run python scripts/build_studio_artifacts.py
   ```
   Cette commande régénère automatiquement `docs/data/amazonia_data_v6_0.js` (validé par Node `new vm.Script()`), `docs/data/catalog_v6_0.json`, `docs/data/spec_formelle_v6_0.json`, `data/catalog_v6_0.json`, `data/spec_formelle_v6_0.json`, `data/studio_lock.json` et `data/spec_bundle_v6_0.json`.

## 3. Diagnostic des Écarts & Respect du Noyau Scellé
1. Examiner `git diff contracts/ data/spec_bundle_v6_0.json` et résumer en français clair les règles ou tuiles modifiées.
2. **Noyau scellé (`contracts/kernel_locks.sha256`)** :
   - **Interdiction absolue** de modifier `engine/state.py`, `engine/rng.py`, `engine/primitives.py` ou `engine/core_engine.py` sans accord explicite de l'auteur (bascule noyau `v6.2` dédiée au Chantier 4).
   - Tant que le moteur reste scellé en attente du Chantier 4/5, conserver `"engine_sync_status": "PENDING_KERNEL_V6_2"` sur les profils du Canon 0 non encore portés en Python.
3. Si le livret joueur (`docs/data/livret_v6_0.js`) est modifié, fournir systématiquement le tableau de conservation des `INV-01..INV-22` et vérifier les attributs `data-inv="INV-XX"`.

## 4. Validation & Journal
1. Exécuter `uv run python verify_lot.py` et obtenir **100 % au vert** (incluant `verify_tiles_canon`, scanner global anti-vestiges, cohérence Studio, `ruff`, `pyright`, `pytest`, fuzzer PyPy).
2. Consigner la synchronisation en une ligne dans `STATUS.md`.
