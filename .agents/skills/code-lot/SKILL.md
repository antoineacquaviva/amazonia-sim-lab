---
name: code-lot
description: >-
  Code et valide un lot de tuiles du Canon 0 (30 emplacements v6.2) avec ses tests témoins :
  utiliser dès que l'auteur demande de coder le prochain lot de tuiles ou d'avancer sur
  l'implémentation des tuiles (Gardiens, Rêves, Nids).
---

# Skill `code-lot` — Usinage Stateless des Tuiles Canon 0 (`v6.2`)

## Règle d'Économie de Contexte (Anti-Dérive)
Pour préserver une fenêtre de contexte chirurgicale, **ne lire que** :
1. `STATUS.md`, `.agents/rules/rule-effects.md` et `contracts/core_state_api.md`,
2. Les fiches JSON exactes des seuls emplacements du lot ciblé extraites de `contracts/tiles_canon_v6_2.json` via une commande Python ciblée.

Commande type d'extraction ciblée :
```bash
uv run python -c "import json; ct=json.load(open('contracts/tiles_canon_v6_2.json', encoding='utf-8'))['tuiles_ciblees']; slots=['G1','G2']; print(json.dumps({s: ct[s] for s in slots}, ensure_ascii=False, indent=2))"
```

---

## Protocole d'Exécution en 5 Étapes

### 1. Audit des Hooks & Respect du Noyau Scellé
- Vérifier pour chaque fiche (`fenetre`, `primitive`, `texte`, `temoins`) que les hooks `HOOK_*` et primitives `prim_*` documentés dans `contracts/core_state_api.md` suffisent.
- **INTERDICTION ABSOLUE** de modifier un fichier listé dans `contracts/kernel_locks.sha256` sans accord explicite et Micro-ADR validé.
- Si un point d'accroche moteur manque réellement, lever explicitement :
  ```python
  raise NotImplementedError("NEEDS_KERNEL_HOOK: <slot_id>:<profile> requiert <détail exact>")
  ```

### 2. Implémentation Stateless (`engine/effects/`)
- Décorer chaque profil avec `@register_tile(slot_id, profile, hooks=(...))` (100 % stdlib PyPy 3.11, UTF-8 sans BOM, LF).
- **Zéro accès à `._buf`**, **zéro `import random`**, **zéro variable globale mutable** (vérifié par AST dans `verify_lot.py`).
- **Gouvernance unitaire** par `peuple_origine` (`state.cfg.seat_of_peuple(peuple_origine)`), avec option `"PASSER"` dès que l'effet est facultatif.
- **Autonomie des Faces 2** : coder `face == 2` sans aucune dépendance à la Face 1.
- **Zéro dette mémorielle (`mem_debt == 0`)** et **atomicité** : terminer l'effet avant de déclencher le balayage des 6 icônes Gardiens.

### 3. Tests Unitaires Témoins (`tests/`)
- Reproduire fidèlement chaque entrée de `temoins` de `contracts/tiles_canon_v6_2.json` (35 témoins au total sur les 30 tuiles) en vérifiant l'état avant/après et le statut `"engine_sync_status": "ACTIVE_VERIFIED"` une fois validé (Chantier 5).

### 4. Fuzzer PyPy & Linter Canon 0
- Vérifier l'exécution sans erreur dans `scripts_cloud/fuzz_invariants.py` (garde-fou `max_steps = 2000`) et le passage de `verify_tiles_canon` dans `verify_lot.py`.

### 5. Porte de Validation, `STATUS.md` & Commit
1. Exécuter `uv run python verify_lot.py` et obtenir **100 % VERT**.
2. Consigner l'avancement dans `STATUS.md` puis créer un commit atomique.
