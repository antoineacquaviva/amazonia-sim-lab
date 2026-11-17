---
trigger: glob
description: Règles d'usinage stateless des effets de tuiles et tests témoins
globs: "engine/effects/**/*.py, tests/temoins/**/*.py"
---

# Règles des Effets (`engine/effects/`) & Témoins (`tests/temoins/`)

## 1. Usinage stateless par lots
- Coder par lots stateless de **8 à 10 profils** enregistrés via `@register_tile(slot_id, profile, hooks=[...])`.
- Utiliser **exclusivement** les méthodes publiques documentées dans `contracts/core_state_api.md`.

## 2. Interdictions strictes (vérifiées par AST dans `verify_lot.py`)
- Interdiction d'accéder à l'attribut `_buf` de `GameState`.
- Interdiction d'importer `random`.
- Interdiction de créer des variables globales mutables (hors constantes `UPPER_CASE` immuables et décorateurs `@register_tile`).

## 3. Contraintes métier des effets
- **Gouvernance unitaire** par `peuple_origine` : toujours inclure l'option `PASSER` dès qu'un effet est facultatif (*« vous pouvez »*).
- **Autonomie intégrale des Faces 2** : aucune dépendance implicite au texte de la Face 1.
- **Atomicité & Déclencheurs** : exécuter complètement les groupes atomiques avant d'émettre les déclencheurs `1..6`.
- **Escalade obligatoire** : si un hook du noyau manque, lever immédiatement :
  `raise NotImplementedError("NEEDS_KERNEL_HOOK: <détail>")`

## 4. Tests unitaires témoins
- Chaque profil livré doit posséder son test unitaire déterministe `pytest` dans `tests/temoins/` traduisant fidèlement son champ `"temoin"` du contrat JSON Studio.
