---
trigger: always_on
description: Hygiène Git obligatoire de session et lancement de campagnes en langage naturel
---

# Règles Permanentes — Hygiène Git & Campagnes en Langage Naturel

## 1. Hygiène Git obligatoire
- **Début de session** : toujours exécuter `git pull --ff-only origin main` avant toute lecture, édition ou exécution.
- **Fin de session** :
  1. Si du code ou Amazonia Doc Studio (`docs/`) a été modifié, exécuter `uv run python verify_lot.py` et obtenir **100 % vert**.
  2. Vérifier que `git status` est propre après commit des livrables attendus.
  3. Terminer par `git push origin main`.

## 2. Lancement de campagne en langage naturel
- Lorsque l'utilisateur décrit une hypothèse de tir en français (tables `3..6` joueurs, axes de châssis à varier, profils `A/B/C/D` à comparer, volume de parties, bot `B0..B3`) :
  1. Traduire son intention en un manifeste JSON `campaigns/<nom>.json` strictement conforme au schéma attendu par `campaigns/worker_main.py` (`resolve_manifest_plan`).
  2. Sauvegarder ce manifeste dans `campaigns/<nom>.json`.
  3. Exécuter `uv run python run_campaign.py campaigns/<nom>.json` (l'auto-détection du build Cloud s'occupe de reconstruire l'image `worker-pypy` uniquement si les sources embarquées ont changé).
