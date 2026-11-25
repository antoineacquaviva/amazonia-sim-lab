---
trigger: glob
description: Règles de maintenance d'Amazonia Doc Studio intégré dans docs/ (SSOT v6.2)
globs: "docs/**/*"
---

# Règles de Maintenance — Amazonia Doc Studio (`docs/`, SSOT `v6.2`)

Référentiel complet : `docs/AMAZONIA_STUDIO_CONTEXT.md`.

## 1. Source Unique de Vérité (`contracts/`) & Compilateur Dérivé Unique
- Le socle `v6.2` (`rules_canon_v6_2.json`, `physical_and_edge_invariants.json` `INV-01..INV-22`, `tiles_canon_v6_2.json` archive de référence) est **sanctuarisé par empreinte SHA-256** dans `contracts/v6_2_socle_locks.sha256`.
- Le chantier actif **`v6.3`** (référentiel : `docs/cadrage_tuiles_v6_3.md`) introduit le contrat bi-composant `contracts/tiles_canon_v6_3.json` (`tuile_plateau` + `carte_joueur`, validé par `contracts/tiles_canon_v6_3.schema.json` et `scripts/audit_197.py`).
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
- `tests/test_studio_render_and_guards.py` exige en mode bloquant la présence de chaque attribut HTML `data-inv="INV-XX"` et de ses `assertions_livret` dans `#rulebook-article`.
- Zéro jargon technique, zéro code numérique d'étape et zéro formulation rétrospective négative dans le livret joueur.

## 4. Linter Structurel des Tuiles, 4 Murs Porteurs (`M1..M4`), Audit 197 Assises & Anti-Vestiges (`verify_lot.py` + `scripts/audit_197.py`)
- **Invariant `I07` (Purge définitive de `C02`)** : **aucune limite** de nombre de mots, de nombre de phrases ni de nombre de conditions sur les textes de règles (`carte_joueur.texte_regle`).
- Chaque tuile des 30 emplacements doit respecter les **4 Murs Porteurs Physiques** et les invariants structurels vérifiés par `verify_lot.py` et `scripts/audit_197.py` :
  - `M1_TEMPS_BATAILLE` : aucune régénération `Souche → Arbre debout` durant les Tours 1–8 ni à la pose d'un Enracinement (exclusivement au décompte final via `enracine` ; conditions spatiales sur Arbre debout valides) ;
  - `M2_CONSERVATION_THERMIQUE` : aucun Bleu Surchauffe posé à sec depuis la réserve (toujours issu du retournement/transfert d'un Rouge existant ou d'une lecture modifiée) ;
  - `M3_INTEGRITE_PLATEAU_ET_ICONES` : immobilité absolue des Arbres/Souches (`2–2–3–3`), zéro coupe volontaire d'un Arbre debout allié comme coût, et fixité d'icône des Gardiens en piste (`≤ 1` Twist dédié sur 30) ;
  - `M4_AUTONOMIE_PLANCHER_SOLO` : toute tuile construite seule a un effet plancher utile garanti dès sa `Face 1` (`entrees_plancher` sans prérequis bloquant issu d'une autre tuile ni même de la jumelle `Y>X` ; synergies inter-tuiles encouragées dans `entrees_synergie` en `OU` / `Si…` / `Face 2`) ;
  - `mem_debt = 0` (aucun modificateur flottant de tour), `0` code numérique d'étape (`1.1` à `6.3`), `0` jargon de pioche/paquet obsolète ;
  - `I01` Clôture solo `entrees_plancher`, atteignabilité des `entrees_synergie` sur les 64 assises et exclusivité stricte des Insectes aux 10 tuiles des 5 lisières de `I` ;
  - `I02` Autonomie stricte `A = 0` sur `{H, E, I}` (`R1, R2, R6, R10, M4, M5`) ;
  - `I03..I06` Divergence de lisière, quotas Éveil `(i)+(ii)`, Sommeil (`E` sans `H`), Enracinement (`3–5`), Lois passives (`≤ 5` global, `≤ 2` par assise), Twists `2K3` (`≥ 6`) ;
  - Casting animalier verrouillé sur les 15 Gardiens (`tuile_plateau` sans phrase rédigée, `carte_joueur` autonome en Face 2) et staging parallèle des candidats dans `contracts/panels/` (`panel_1..3.json`).
- Le scanner global anti-vestiges de `verify_lot.py` audite automatiquement `contracts/*.json`, `docs/data/*.json`, `docs/AMAZONIA_STUDIO_CONTEXT.md` et `.agents/**/*.md` (hors `VERSION_CHANGELOG` et `archive/`).
