---
name: code-lot
description: >-
  Usine en session courte (~15 min) un lot stateless de profils de tuiles (Lot 01 à Lot 11)
  selon contracts/LOTS_PLAN.md : génère engine/effects/lot_XX.py et tests/temoins/test_lot_XX.py,
  étend le fuzzer PyPy, valide verify_lot.py à 100 % vert et met à jour STATUS.md.
  Utiliser dès que l'auteur demande de coder, usiner ou livrer un Lot XX de tuiles.
---

# Skill `code-lot` — Usinage Stateless d'un Lot (`Lot 01` .. `Lot 11`)

## Règle d'Économie de Contexte (Anti-Dérive)
Pour préserver une fenêtre de contexte chirurgicale, **ne lire que** :
1. `STATUS.md` et la section du `Lot XX` demandé dans `contracts/LOTS_PLAN.md`,
2. `.agents/rules/rule-effects.md` et `contracts/core_state_api.md`,
3. Les fiches JSON exactes des seuls profils du `Lot XX` extraites de `data/spec_bundle_v5_3_1.json` via une commande Python ciblée (ne **jamais** charger les 100 profils en texte brut dans le prompt).

Commande type d'extraction ciblée d'un lot :
```powershell
uv run python -c "import json; ct=json.load(open('data/spec_bundle_v5_3_1.json', encoding='utf-8'))['catalogue_tuiles']; pairs=[('G1','B'),('G2','B')]; print(json.dumps({f'{s}:{p}': {'peuple_origine': ct[s]['peuple_origine'], **ct[s]['profils'][p]} for s,p in pairs}, ensure_ascii=False, indent=2))"
```

---

## Protocole d'Exécution en 5 Étapes

### 1. Audit des Hooks & Escalade Noyau Scellé
- Vérifier pour chaque fiche du `Lot XX` (`fenetre`, `primitive`, `requires_options`, `texte`, `temoin`) que les hooks `HOOK_*` et primitives `prim_*` listés dans `contracts/core_state_api.md` suffisent.
- **INTERDICTION ABSOLUE** de modifier un fichier listé dans `contracts/kernel_locks.sha256`.
- Si un point d'accroche moteur manque réellement pour un profil, implémenter le handler en levant explicitement :
  ```python
  raise NotImplementedError("NEEDS_KERNEL_HOOK: <slot_id>:<profile> requiert <détail exact>")
  ```
  Documenter ce besoin précis à l'auteur pour un mini-commit d'ouverture noyau dédié et approuvé séparément.

### 2. Implémentation Stateless (`engine/effects/lot_XX.py`)
Créer `engine/effects/lot_XX.py` (UTF-8 sans BOM, LF, 100 % stdlib PyPy 3.11) en respectant toutes les contraintes vérifiées par AST dans `verify_lot.py` :
- Décorer chaque profil avec `@register_tile(slot_id, profile, hooks=(...))`.
- **Zéro accès à `._buf`**, **zéro `import random`** (utiliser `engine/rng.py` si nécessaire), **zéro variable globale mutable** (uniquement des constantes immuables `UPPER_CASE` composées de littéraux/tuples/`frozenset`).
- **Gouvernance unitaire** : déterminer le siège décideur via `state.cfg.seat_of_peuple(peuple_origine)` (repli `state.coordonnateur` si absent) et inclure systématiquement `"PASSER"` dès que l'effet comporte *« vous pouvez »*.
- **Autonomie des Faces 2** : coder la branche `face == 2` des Gardiens de manière 100 % autonome vis-à-vis de la Face 1.
- **Atomicité & Verrous 1/tour** : exécuter intégralement l'effet atomique avant d'allumer les déclencheurs `1..6` (`light_trigger`) ; utiliser `state.has_slot_used_once_per_turn(slot_id)` / `state.mark_slot_used_once_per_turn(slot_id)` pour tout quota *« 1 fois par tour »*.
- Enregistrer l'import de `lot_XX` dans `engine/effects/__init__.py`.

### 3. Tests Unitaires Témoins (`tests/temoins/test_lot_XX.py`)
Créer `tests/temoins/test_lot_XX.py` (avec `tests/temoins/__init__.py` si absent) contenant **au moins 1 test déterministe dédié par profil** du lot (`test_<slot>_<profile>_temoin`) :
- Reproduire exactement la mise en situation décrite dans le champ `"temoin"` du JSON Studio.
- Vérifier l'état exact avant/après résolution (Arbres, Souches, Insectes, Puissance, Pistes, Déclencheurs `1..6`, option `"PASSER"` le cas échéant, et RAZ `6.2` pour les effets transitoires).

### 4. Extension du Fuzzer PyPy (`scripts_cloud/fuzz_invariants.py`)
- Importer les lots livrés dans `scripts_cloud/fuzz_invariants.py` afin qu'une fraction des `1 000` parties du fuzzer PyPy tourne en **Mode 3/4** en activant aléatoirement (via `rng.py`) les profils déjà enregistrés dans `list_registered_tiles()`, toujours sous garde-fou strict `max_steps = 2000`.
- Pour le **Lot 11**, ajouter `tests/temoins/test_lot_11_audit.py` vérifiant la couverture `100/100` exacte contre `data/spec_bundle_v5_3_1.json` et la validité complète de `engine/effects/mode3_reference.json`.

### 5. Porte de Validation, `STATUS.md` & Commit
1. Exécuter `uv run python verify_lot.py` et obtenir **6/6 PORTES 100% VERT** (`kernel_locks.sha256`, AST `engine/effects/`, `ruff`, `pyright`, `pytest`, `PyPy Invariant Fuzzer`).
2. Cocher `[x] Lot XX` dans `STATUS.md` avec une note concise d'une ligne.
3. Ré-exécuter `uv run python verify_lot.py` puis créer un commit atomique :
   `feat(effects): implement Lot XX (<résumé profils>) with witness tests`.
