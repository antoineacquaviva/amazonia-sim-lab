---
trigger: glob
description: Règles de maintenance d'Amazonia Doc Studio intégré dans docs/
globs: "docs/**/*"
---

# Règles de Maintenance — Amazonia Doc Studio (`docs/`)

Référentiel complet : `docs/AMAZONIA_STUDIO_CONTEXT.md` (Section 5).

## 1. Synchronisation obligatoire des 4 couches
- Toute évolution de règle ou de profil de tuile dans `docs/` doit mettre à jour **simultanément** les 4 couches :
  1. `docs/data/livret_v5_3.js` (`renderDidacticRulebook` **ET** `REGLES_COEUR_SYNTHESE`) ;
  2. `docs/data/amazonia_data_v5_3.js` (`CATALOGUE_TUILES`, `VERSION_CHANGELOG`, `SPEC_FORMELLE_V5_3`) ;
  3. `docs/data/catalog_v5_3.json` ;
  4. `docs/data/spec_formelle_v5_3.json`.
- Après toute modification dans `docs/data/`, resynchroniser immédiatement le simulateur via :
  `uv run python scripts_cloud/sync_studio.py && uv run python scripts_cloud/build_spec_bundle.py`
  puis valider les **8/8 portes** de `uv run python verify_lot.py` (incluant la porte de cohérence 32 emplacements / 100 profils / 7 axes du châssis).

## 2. Patchs différentiels via Node `vm` + `JSON.stringify`
- Ne **jamais** réécrire tout le catalogue à la main dans une réponse LLM ni injecter des chaînes JS par regex brutes (risque de casse sur les apostrophes `'` vs `’`).
- Toujours charger l'objet dans un contexte Node `vm`, muter uniquement les clés ciblées, resérialiser proprement via `JSON.stringify` et vérifier la syntaxe par `new vm.Script()`.

## 3. Couple `texte` + `temoin` & Faces 2 autonomes
- Ne **jamais** laisser le champ `"temoin"` vide et toujours mettre à jour `"temoin"` dès que `"texte"` change (et réciproquement maintenir aligné le test unitaire correspondant dans `tests/temoins/`).
- Sur un Gardien double-face, le texte de la **Face 2** doit se suffire à lui-même sans jamais renvoyer à la Face 1 cachée.

## 4. Encodage, PowerShell & compatibilité statique (`file://` et HTTPS)
- Écrire tous les fichiers en **UTF-8 sans BOM** avec fins de ligne `\n` (LF).
- Préserver le fonctionnement **SPA statique sans bundler** de `docs/index.html` (chemins relatifs `data/...` uniquement, compatible `file://` et HTTPS).
- Sous Windows PowerShell 5.1, préférer l'exécution d'un fichier script (`node "docs/scripts/xxx.js"`) aux one-liners `node -e "..."` (qui altèrent les guillemets doubles).
