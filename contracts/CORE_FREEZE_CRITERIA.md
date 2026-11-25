# CORE_FREEZE_CRITERIA.md — Gouvernance SSOT `v6.2` (Sanctuarisée), Chantier `v6.3` & Micro-ADR

> **Socle règles cœur sanctuarisé** : **`v6.2.0`** (`contracts/rules_canon_v6_2.json`, `contracts/physical_and_edge_invariants.json` `INV-01..INV-22`, noyau PyPy dans `contracts/kernel_locks.sha256` et archive de comparaison `contracts/tiles_canon_v6_2.json` verrouillée dans `contracts/v6_2_socle_locks.sha256` + tag Git `archive/v6.2.0-socle-canon0`).
> **Jalon `v6.2` (Chantiers 1–5) : ARCHIVÉ & TERMINÉ.**
> **Chantier actif : `v6.3` — Refonte bi-composant des 30 Tuiles (Mini-Tuile Plateau + Grande Carte Joueur, zéro contrainte `C02`)**
> *Source d'autorité* : `docs/cadrage_tuiles_v6_3.md` & `contracts/tiles_canon_v6_3.schema.json`.
> 1. **Étape 1** : Cadrage `v6.3`, sanctuarisation `v6.2`, purge `C02`, `scripts/audit_197.py` et contrat JSON bi-composant `contracts/tiles_canon_v6_3.json`.
> 2. **Étape 2** : Conception créative et audit structurel (`197` assises) du nouveau panel de `30` tuiles (priorité synergies & twists).
> 3. **Étape 3** : Affinage ergonomique et double rédaction éditoriale (Grande Carte + Mini-Tuile).
> 4. **Étape 4** : Ré-encodage PyPy, nouveaux témoins exécutables, heuristiques bots synergiques et calibration Monte-Carlo `v6.3` face au `Lot 0`.
> 5. **Étape 5 (secondaire)** : Refonte UX/UI de l'explorateur de tuiles dans Doc Studio (vue dédoublée Mini-Tuile / Grande Carte, retrait des compteurs de mots, guide des pictogrammes).

---

## 1. Protocole Obligatoire « Micro-ADR en 4 Questions »

Avant toute modification d'une règle du cœur dans `contracts/rules_canon_v6_2.json`, d'un invariant dans `contracts/physical_and_edge_invariants.json` ou d'une mécanique transverse, l'auteur et l'agent doivent renseigner explicitement ce **Micro-ADR en 4 questions** :

1. **Invariant & Motivation** : quel invariant (`INV-01..INV-22`) ou clause de `rules_canon_v6_2.json` change, et quel signal factuel (playtest physique ou télémétrie avec IC 95 %) justifie la retouche ?
2. **Impact Matériel & Cas Limites** : quelles pièces physiques (dotation finie `10 × N`, sac opaque, 2 Défenseurs recto-verso, bandelette d'Acte, 6 icônes Gardiens, 2 encoches visibles, accessoires `3 + 3`) sont affectées ? Vérification stricte de `mem_debt == 0`.
3. **Propagation Modules & Panel 30 Tuiles** : quels modules (*Gardiens & Éveil*, *Rêves & Sommeil*, *Essaim*) et quelles tuiles parmi les 30 emplacements (`contracts/tiles_canon_v6_3.json` / archive `v6.2`) sont impactés (clôture `I01` élargie à la jumelle `Y>X`, autonomie `I02` `A=0`, quotas `I03..I06` ; **zéro plafond de mots `I07`**) ?
4. **Preuves & Synchronisation Dérivée** : quels tests (`target_test_id`, témoins, `scripts/audit_197.py`, `verify_tiles_canon`, scanner anti-vestiges) prouvent la non-régression après régénération par `uv run python scripts/build_studio_artifacts.py` ?

---

## 2. Règle Anti-Perte sur le Livret Joueur (Conservation des `INV-01..INV-22`)

- **Interdiction absolue de condenser, réorganiser ou réécrire le livret joueur (`docs/data/livret_v6_0.js`) sans établir préalablement un tableau de conservation intégral couvrant 100 % des 22 invariants `INV-01` à `INV-22`** de `contracts/physical_and_edge_invariants.json`.
- Chaque ligne du tableau doit indiquer : `INV-XX` | section / module cible | attribut HTML `data-inv="INV-XX"` présent dans le DOM `#rulebook-article` | vérification de chaque chaîne de `assertions_livret`.
- Tout retrait ou fusion d'un invariant exige au préalable un **Micro-ADR en 4 questions** validé par l'auteur et une mise à jour versionnée de `contracts/physical_and_edge_invariants.json`.

---

## 3. Grille Cible de Validation & Gel du Noyau `v6.2` (Chantiers 4–5)

| Axe | Métrique | Cible *Core Freeze* `v6.2` (`B2`, `N=3..6`, cercles équilibrés) |
| :--- | :--- | :--- |
| **Invariance `N=3..6`** | Écart max `mean_ratio_arbres` entre `N=3` et `N=6` | **≤ 4,0 pts** (avec IC 95 % inter-tables) |
| **Robustesse pire quintile** | `table_cvar20_ratio` (bootstrap par grappes) | **≥ 35 %** et écart inter-`N` **≤ 6,0 pts** |
| **Équité Peuples & Modules** | Écart `3 + 3`, tables sans `I` / sans `H,E` / `{H,E,I}` | **≤ 5,0 pts** sur les 197 assises |
| **Difficulté cible** | `mean_ratio_arbres` global (Canon 0 actif) | Bande éditoriale **45 % – 60 %** (tension sans blocage) |
| **Équilibre des 3 fins** | `% Tour 8` / `% Sommeil` / `% Éveil` | 3 fins réellement atteignables et équilibrées selon `N` |
| **Profondeur & Silence** | Hiérarchie `B0 < B1 < B2 <= B3` & `B2_OPEN` | Monotonie stricte sur toutes strates + `Delta_V_neg > 0` |
| **Budget cognitif** | `mem_debt_score`, `law_stack_max`, `fiddliness_ratio` | `mem_debt == 0`, `law_stack <= 2`, `fiddliness <= 3,5` |
| **Intégrité SSOT** | `verify_lot.py` (SHA-256, AST, Zéro-LLM, Linter 30 tuiles, Anti-vestiges, Node `vm`, `ruff`, `pyright`, `pytest`, PyPy fuzzer) | **100 % VERT** |

---

## 4. Protocole de Scellement du Noyau (`contracts/kernel_locks.sha256`)

1. Toute ouverture du noyau requiert l'accord explicite de l'auteur et un Micro-ADR complété.
2. Après modification approuvée de `engine/{rng,state,primitives,core_engine}.py`, régénérer `contracts/core_state_api.md` via `uv run python scripts_cloud/export_api_doc.py` et re-sceller immédiatement les empreintes SHA-256 dans `contracts/kernel_locks.sha256`.
3. Passer `uv run python verify_lot.py` à **100 % vert** avant tout commit ou campagne Cloud.
