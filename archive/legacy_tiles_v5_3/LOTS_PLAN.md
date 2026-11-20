# Plan Officiel d'Usinage des 11 Lots — Catalogue 100/100 (`spec_bundle_v5_3_1.json`)

Ce document fixe le découpage canonique et sans recouvrement des **100 profils** de `data/spec_bundle_v5_3_1.json` (`45` Gardiens `G`, `31` Rêves `R`, `19` Croissance `M`, `5` Migrations) en **11 sessions stateless** réparties sur les **Paliers 2 et 3**.

- **Socle Palier 1 déjà intégré dans `engine/core_engine.py` (2 profils)** :
  - `SLOT_BUG_CERVEAU:A` (*Court-circuit d’Apprentissage — Standard*)
  - `SLOT_COLONISATION_GARDIENS:A` (*Carburant Symbiotique — Standard*)
- **Usinage modulaire `engine/effects/lot_XX.py` + `tests/temoins/test_lot_XX.py` (98 profils)** :
  - **Palier 2** : `Lot 01` (`8` profils pilotes validant les 8 primitives formelles).
  - **Palier 3** : `Lots 02..10` (`90` profils restants) + `Lot 11` (consolidation intégrale `100/100` & tir Cloud Mode 3).

---

## Récapitulatif Comptable Exact

| Lot | Palier | Périmètre métier | Module cible | Tests témoins | Nb profils | Cumul (avec socle) |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Socle** | 1 | Migrations standard `Bug A` & `Colonie A` | `engine/core_engine.py` | `tests/test_kernel_invariants.py` | `2` | `2 / 100` |
| **Lot 01** | 2 | Lot Pilote des 8 Primitives | `engine/effects/lot_01.py` | `tests/temoins/test_lot_01.py` | `8` | `10 / 100` |
| **Lot 02** | 3 | Gardiens `G1..G5` (hors pilote) | `engine/effects/lot_02.py` | `tests/temoins/test_lot_02.py` | `10` | `20 / 100` |
| **Lot 03** | 3 | Gardiens `G5..G9` (hors `G9_C`) | `engine/effects/lot_03.py` | `tests/temoins/test_lot_03.py` | `10` | `30 / 100` |
| **Lot 04** | 3 | Gardiens `G10..G12` (hors `G10_A`) | `engine/effects/lot_04.py` | `tests/temoins/test_lot_04.py` | `10` | `40 / 100` |
| **Lot 05** | 3 | Gardiens `G13..G15` + Migrations `B/C` | `engine/effects/lot_05.py` | `tests/temoins/test_lot_05.py` | `11` | `51 / 100` |
| **Lot 06** | 3 | Rêves `R1..R4` | `engine/effects/lot_06.py` | `tests/temoins/test_lot_06.py` | `11` | `62 / 100` |
| **Lot 07** | 3 | Rêves `R5..R7` (hors `R5_A`) | `engine/effects/lot_07.py` | `tests/temoins/test_lot_07.py` | `10` | `72 / 100` |
| **Lot 08** | 3 | Rêves `R8..R10` (`R10` : `A, B, D`) | `engine/effects/lot_08.py` | `tests/temoins/test_lot_08.py` | `9` | `81 / 100` |
| **Lot 09** | 3 | Croissance `M1..M3` | `engine/effects/lot_09.py` | `tests/temoins/test_lot_09.py` | `12` | `93 / 100` |
| **Lot 10** | 3 | Croissance `M4..M5` (`M4` : `A, B, D`) | `engine/effects/lot_10.py` | `tests/temoins/test_lot_10.py` | `7` | `100 / 100` |
| **Lot 11** | 3 | Consolidation Catalogue `100/100` & Mode 3 | `engine/effects/__init__.py` | `tests/temoins/test_lot_11_audit.py` | `0` (audit) | `100 / 100` |

---

## Détail Canonique par Lot (Format `SLOT:PROFIL` vérifié par `tests/test_lots_plan.py`)

### Socle (Palier 1 — 2 profils)
- Profils : `SLOT_BUG_CERVEAU:A`, `SLOT_COLONISATION_GARDIENS:A`

### Lot 01 (Palier 2 — Lot Pilote des 8 Primitives, 8 profils)
Valide les 8 primitives formelles, le bus de hooks et les 4 capteurs `engine/telemetry.py` avant l'usinage industriel du Palier 3 :
- `G1:A` — `MOD_PUISSANCE` (*Le Bond du Jaguar*)
- `G2:A` — `DEPLACEMENT` (*L’Étreinte de l’Anaconda*)
- `G4:A` — `MOD_SEUIL` + sacrifice (*Le Cri d’Alarme de l’Ara*)
- `G6:A` — `PERMUTATION_PISTE` (*L’Œil Double du Toucan*)
- `G7:A` — `CREATION_ENTITE` (*Le Barrage du Capybara*)
- `G10:A` — `MOD_APPRENTISSAGE` (*La Brume de la Dendrobate*)
- `R5:A` — `PARTAGE_INFO_ETAT_GARDIEN` (*Le Rêve du nid vide*)
- `G9:C` — `MOD_LOI_DU_COEUR` (*Le Guet du Caïman Noir — Profil C*)
- Profils : `G1:A`, `G2:A`, `G4:A`, `G6:A`, `G7:A`, `G10:A`, `R5:A`, `G9:C`

### Lot 02 (Palier 3 — Gardiens G1..G5, 10 profils)
- Profils : `G1:B`, `G2:B`, `G2:C`, `G3:A`, `G3:B`, `G3:C`, `G3:D`, `G4:B`, `G5:A`, `G5:B`

### Lot 03 (Palier 3 — Gardiens G5..G9, 10 profils)
- Profils : `G5:C`, `G6:B`, `G6:C`, `G7:B`, `G7:C`, `G7:D`, `G8:A`, `G8:B`, `G9:A`, `G9:B`

### Lot 04 (Palier 3 — Gardiens G10..G12, 10 profils)
- Profils : `G10:B`, `G10:C`, `G10:D`, `G11:A`, `G11:B`, `G11:C`, `G11:D`, `G12:A`, `G12:B`, `G12:C`

### Lot 05 (Palier 3 — Gardiens G13..G15 & Migrations restantes, 11 profils)
Clôture intégralement `100 %` des familles `GARDIEN` (`45/45`) et `MIGRATION` (`5/5`) :
- Profils : `G13:A`, `G13:B`, `G14:A`, `G14:B`, `G14:C`, `G14:D`, `G15:A`, `G15:B`, `SLOT_BUG_CERVEAU:B`, `SLOT_BUG_CERVEAU:C`, `SLOT_COLONISATION_GARDIENS:C`

### Lot 06 (Palier 3 — Rêves R1..R4, 11 profils)
- Profils : `R1:A`, `R1:B`, `R1:C`, `R2:A`, `R2:B`, `R3:A`, `R3:B`, `R4:A`, `R4:B`, `R4:C`, `R4:D`

### Lot 07 (Palier 3 — Rêves R5..R7 hors R5_A, 10 profils)
- Profils : `R5:B`, `R5:C`, `R5:D`, `R6:A`, `R6:B`, `R6:C`, `R6:D`, `R7:A`, `R7:B`, `R7:C`

### Lot 08 (Palier 3 — Rêves R8..R10, 9 profils)
Clôture intégralement `100 %` de la famille `REVE` (`31/31`, sachant que `R10` possède les profils `A, B, D`) :
- Profils : `R8:A`, `R8:B`, `R8:C`, `R8:D`, `R9:A`, `R9:B`, `R10:A`, `R10:B`, `R10:D`

### Lot 09 (Palier 3 — Croissance M1..M3, 12 profils)
- Profils : `M1:A`, `M1:B`, `M1:C`, `M1:D`, `M2:A`, `M2:B`, `M2:C`, `M2:D`, `M3:A`, `M3:B`, `M3:C`, `M3:D`

### Lot 10 (Palier 3 — Croissance M4..M5, 7 profils)
Clôture intégralement `100 %` de la famille `CROISSANCE` (`19/19`, sachant que `M4` possède les profils `A, B, D`) :
- Profils : `M4:A`, `M4:B`, `M4:D`, `M5:A`, `M5:B`, `M5:C`, `M5:D`

### Lot 11 (Palier 3 — Consolidation Catalogue 100/100 & Validation Mode 3)
1. Importer `lot_01` à `lot_10` dans `engine/effects/__init__.py` via une fonction idempotente `load_all_effects()`.
2. Écrire `tests/temoins/test_lot_11_audit.py` vérifiant automatiquement :
   - que chacun des **100 `(slot_id, profile)`** de `data/spec_bundle_v5_3_1.json` est enregistré dans `list_registered_tiles()`,
   - qu'au moins **1 fonction de test dédiée** par profil existe dans `tests/temoins/`,
   - que les 32 sélections de `engine/effects/mode3_reference.json` tournent sans erreur sur `N=3..6` sous le fuzzer PyPy.
3. Lancer une campagne Cloud Run Jobs (`run-campaign`) comparant Mode 2 vs Mode 3 (`mode3_reference.json`) avec `B1/B2` et les 4 capteurs cognitifs (`data/digests/digest_palier3_mode3_ref.json` < 30 Ko).
