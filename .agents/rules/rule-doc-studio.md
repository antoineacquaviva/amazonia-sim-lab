---
trigger: glob
description: Règles de maintenance d'Amazonia Doc Studio intégré dans docs/ (SSOT v6.2)
globs: "docs/**/*"
---

# Règles de Maintenance — Amazonia Doc Studio (`docs/`, SSOT `v6.2`)

Référentiel complet : `docs/AMAZONIA_STUDIO_CONTEXT.md`.

## 1. Source Unique de Vérité (`contracts/`) & Compilateur Dérivé Unique
- Toute constante de règle, tout invariant et toute fiche de tuile du Canon 0 vivent **exclusivement** dans les 3 contrats SSOT de `contracts/` :
  1. `contracts/rules_canon_v6_2.json` (châssis unique `P4_2233` départ décalé, matériel fini, supports fixes, 6 icônes Gardiens, 3 modules, accessoires `3 + 3`, Enracinement) ;
  2. `contracts/physical_and_edge_invariants.json` (registre permanent `INV-01` à `INV-22`) ;
  3. `contracts/tiles_canon_v6_2.json` (30 emplacements du Canon 0, `48` faces, témoins, `carte_des_roles`, `rapport_audit_197`, vivier `B/C`).
- **Interdiction absolue** d'éditer à la main les fichiers dérivés (`docs/data/amazonia_data_v6_0.js`, `docs/data/catalog_v6_0.json`, `docs/data/spec_formelle_v6_0.json`, `data/spec_bundle_v6_0.json`, `data/studio_lock.json`).
- Après toute modification dans `contracts/` ou `docs/data/livret_v6_0.js`, exécuter impérativement :
  `uv run python scripts/build_studio_artifacts.py`
  puis valider **100 % au vert** `uv run python verify_lot.py`.

## 2. Sécurité JS & Encodage (`file://` et HTTPS)
- Le compilateur valide systématiquement tout fichier JS généré via Node `new vm.Script()` + exécution dans un contexte `vm` isolé.
- Écrire tous les fichiers en **UTF-8 sans BOM** avec fins de ligne `\n` (LF).
- Préserver le fonctionnement **SPA statique sans bundler** de `docs/index.html` (chemins relatifs `data/...`, compatible `file://` et HTTPS).
- Ne **jamais** laisser d'axe mort de châssis ou d'écart par défaut à l'ouverture (`0 écart` à l'ouverture et après `resetChassisToDefault()`, `Placement_Initial_Machines.defaultVal = "BULLDOZER_P1_ABATTEUSE_P2"`).

## 3. Contraintes éditoriales du Livret Modulaire & Conservation des `INV-01..INV-22`
- **Interdiction absolue** de condenser ou réécrire le livret joueur (`docs/data/livret_v6_0.js`) sans produire le tableau de conservation intégral des 22 invariants `INV-01..INV-22` de `contracts/physical_and_edge_invariants.json`.
- Dès que `livret_v6_0.js` déclare `LIVRET_SCHEMA_VERSION = "6.2.0"` (Chantier 2), `tests/test_studio_render_and_guards.py` exige en mode bloquant la présence de chaque attribut HTML `data-inv="INV-XX"` et de ses `assertions_livret` dans `#rulebook-article`.
- Zéro jargon technique, zéro code numérique d'étape et zéro formulation rétrospective négative dans le livret joueur.

## 4. Linter Automatique des Tuiles & Anti-Vestiges (`verify_lot.py`)
- Chaque face/ligne de texte de tuile dans `contracts/tiles_canon_v6_2.json` et `CATALOGUE_TUILES` doit respecter :
  - `≤ 25` mots stricts (élisions séparées, hors étiquette `Face 1 :` / `Face 2 :` / `Enraciné :` / `En Parade :` / `En Migration :`), `1` seule phrase, `≤ 1` condition ;
  - `0` code numérique d'étape (`1.1` à `6.3`), `0` terme banni (pas de jargon de pioche obsolète, pas de redondance, pas de vestige antérieur) ;
  - Clôture stricte des Insectes aux 10 tuiles des 5 lisières de `I` et zéro mention des Gardiens sur les 6 tuiles `A=0` (`R1, R2, R6, R10, M4, M5`) ;
  - Faces 2 autonomes (ne jamais renvoyer à la Face 1 cachée) et champ `"temoin"` toujours renseigné.
- Le scanner global anti-vestiges de `verify_lot.py` audite automatiquement `contracts/*.json`, `docs/data/*.json`, `docs/AMAZONIA_STUDIO_CONTEXT.md` et `.agents/**/*.md` (hors `VERSION_CHANGELOG` et `archive/`).
