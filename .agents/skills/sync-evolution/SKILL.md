---
name: sync-evolution
description: >-
  Synchronise et met à jour le simulateur après une retouche d'auteur dans Amazonia Doc Studio :
  utiliser dès que l'auteur dit avoir modifié des règles, des valeurs ou des textes de tuiles
  dans Doc Studio / le Studio, ou demande de mettre le simulateur à jour avec ses derniers changements.
---

# Skill `sync-evolution` — Mise à Jour depuis *Amazonia Doc Studio*

## 1. Synchronisation Portable du Contrat Studio
1. Exécuter `uv run python scripts_cloud/sync_studio.py` (qui détecte automatiquement `../amazonia-doc-studio`, `AMAZONIA_STUDIO_DIR`, `~/dev/amazonia-doc-studio` ou GitHub en secours, et met à jour `data/studio_lock.json`).
2. Régénérer le bundle consolidé via `uv run python scripts_cloud/build_spec_bundle.py` (`data/spec_bundle_v5_3_1.json` et `engine/effects/mode3_reference.json`).

---

## 2. Diagnostic Clair des Écarts Règles & Tuiles
1. Comparer via `git diff data/spec_bundle_v5_3_1.json` les emplacements, profils `A/B/C/D`, témoins ou règles transverses qui ont changé.
2. Résumer à l'auteur en français simple la liste exacte des tuiles ou règles modifiées.

---

## 3. Alignement du Code & Respect du Noyau Scellé
1. **Si seules des tuiles (`G/R/M` ou Migrations hors socle) déjà codées ont changé** :
   - Mettre à jour leurs fonctions stateless dans `engine/effects/lot_XX.py` et leurs tests témoins dans `tests/temoins/test_lot_XX.py`.
2. **Si une règle du cœur du jeu (noyau scellé dans `contracts/kernel_locks.sha256`) est touchée** :
   - Ne **jamais** modifier `engine/state.py`, `engine/rng.py`, `engine/primitives.py` ou `engine/core_engine.py` sans accord explicite : expliquer en 3 phrases simples l'impact à l'auteur, demander son feu vert, appliquer l'ajustement minimal, régénérer `contracts/core_state_api.md` et re-sceller `contracts/kernel_locks.sha256`.

---

## 4. Validation & Journal
1. Exécuter `uv run python verify_lot.py` jusqu'à obtenir **100 % vert (`7/7` portes)**.
2. Consigner la synchronisation en une ligne dans `STATUS.md`.
