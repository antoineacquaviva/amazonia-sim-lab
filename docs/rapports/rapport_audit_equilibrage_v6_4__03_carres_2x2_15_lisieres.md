# Rapport d'analyse — `audit_equilibrage_v6_4__03_carres_2x2_15_lisieres`

- **Campagne** : `audit_equilibrage_v6_4__03_carres_2x2_15_lisieres` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:21:43Z` | **Mode** : `4` | **Parties simulées** : `61 540`
- **Tables** : `ALL_197_ASSISES` (`[3, 4, 5, 6]`) | **Bots** : `B2`
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4__03_carres_2x2_15_lisieres.json`

## 1. Alertes automatiques d'équilibrage

- **🟢 INFO** (`FIN_T8_EXCLUSIVE`) : Fins anticipées quasi absentes (Sommeil 0.1 %, Éveil 1.9 %).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : Ratio manipulation/décision élevé (2.64 > 1.8).
- **🟠 VIGILANCE** (`SOLO_FORT_G10`) : Tuile G10 très dominante en solo (+9.3 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`SOLO_FORT_R4`) : Tuile R4 très dominante en solo (+9.7 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`SOLO_FORT_M2`) : Tuile M2 très dominante en solo (+16.9 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`SOLO_FORT_M5`) : Tuile M5 très dominante en solo (+9.1 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`EDGE_ANTISYN_R_I`) : Lisière 2×2 R_I (G14+M2) : anti-synergie I_2x2 = -4.3 pts.
- **🟠 VIGILANCE** (`EDGE_ANTISYN_E_I`) : Lisière 2×2 E_I (R10+M5) : anti-synergie I_2x2 = -4.2 pts.

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 55.3 % |
| Queue basse CVaR20 | 38.2 % |
| Fin Tour 8 | 98.0 % |
| Fin Sommeil (Rêves rang 1) | 0.1 % |
| Fin Éveil (Gardiens A+1) | 1.9 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.95 tours |

## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées

| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B2` | 61540 | 55.3 % | 38.2 % | 98.0 % | 0.1 % | 1.9 % | 0.0 % |

## 4. Équilibrage par nombre de joueurs (3J–6J)

| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3J | 4000 | 55.4 % | 32.9 % | 96.4 % | 0.1 % | 3.5 % | 0.0 % |
| 4J | 11700 | 54.1 % | 35.1 % | 98.0 % | 0.1 % | 1.9 % | 0.0 % |
| 5J | 23040 | 55.0 % | 38.4 % | 97.6 % | 0.1 % | 2.3 % | 0.0 % |
| 6J | 22800 | 56.3 % | 41.1 % | 98.6 % | 0.1 % | 1.3 % | 0.0 % |

### Couverture des assises canoniques (197 assises / 42 compositions)

**Pires assises (survie la plus basse)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N4-HERI` | `N4-HERI` | 20 | 40.1 % | 0.0 % | 5.0 % | 0.0 % |
| `N4-ERMI` | `N4-EMRI` | 20 | 41.5 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HMEI` | `N4-HEMI` | 20 | 43.4 % | 0.0 % | 10.0 % | 0.0 % |
| `N3-EMI` | `N3-EMI` | 20 | 44.3 % | 0.0 % | 10.0 % | 0.0 % |
| `N4-HMIR` | `N4-HMRI` | 20 | 44.5 % | 0.0 % | 5.0 % | 0.0 % |
| `N3-HRI` | `N3-HRI` | 20 | 45.2 % | 0.0 % | 5.0 % | 0.0 % |
| `N4-ERIO` | `N4-EROI` | 20 | 45.2 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-EMIR` | `N4-EMRI` | 20 | 45.5 % | 0.0 % | 0.0 % | 0.0 % |

**Meilleures assises (survie la plus haute)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N3-ERO` | `N3-ERO` | 20 | 61.0 % | 0.0 % | 30.0 % | 0.0 % |
| `N3-EMO` | `N3-EMO` | 20 | 58.2 % | 0.0 % | 20.0 % | 0.0 % |
| `N4-HMRO` | `N4-HMRO` | 20 | 58.0 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HEOM` | `N4-HEMO` | 20 | 57.5 % | 0.0 % | 20.0 % | 0.0 % |
| `N4-HRIO` | `N4-HROI` | 20 | 57.1 % | 0.0 % | 10.0 % | 0.0 % |
| `N5-HERMO` | `N5-HEMRO` | 20 | 57.0 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HRO` | `N3-HRO` | 20 | 57.0 % | 0.0 % | 20.0 % | 0.0 % |
| `N6-HMIERO` | `N6-HEMROI` | 20 | 56.8 % | 0.0 % | 0.0 % | 0.0 % |

## 5. Étude modulaire « Tuiles à blanc » (`EDGE_2X2`)

### Plancher Solo, Retrait Écosystème (LOO) & Levier Synergique (`L_syn = Δ_éco - Δ_solo`)

| Tuile | Δ Solo (vs ALL_NEUTRE) | IC95 Solo | Δ Éco (ALL_ACTIVE - LOO) | IC95 Éco | Levier Synergique `L_syn` | p-Holm |
|---|---:|---|---:|---|---:|---:|
| `M2` | +16.94 pts | [+16.3, +17.6] | — | — | — | 0.0000 |
| `R4` | +9.73 pts | [+8.7, +10.8] | — | — | — | 0.0000 |
| `G10` | +9.32 pts | [+8.6, +10.0] | — | — | — | 0.0000 |
| `M5` | +9.13 pts | [+8.5, +9.7] | — | — | — | 0.0000 |
| `R10` | +7.80 pts | [+7.0, +8.5] | — | — | — | 0.0000 |
| `R9` | +5.38 pts | [+4.8, +5.9] | — | — | — | 0.0000 |
| `R7` | +5.10 pts | [+4.5, +5.7] | — | — | — | 0.0000 |
| `R8` | +4.93 pts | [+4.3, +5.5] | — | — | — | 0.0000 |
| `G15` | +4.74 pts | [+4.3, +5.2] | — | — | — | 0.0000 |
| `R2` | +4.21 pts | [+3.6, +4.9] | — | — | — | 0.0000 |
| `G14` | +3.90 pts | [+3.3, +4.5] | — | — | — | 0.0000 |
| `G1` | +3.54 pts | [+2.9, +4.2] | — | — | — | 0.0000 |
| `M3` | +3.02 pts | [+2.5, +3.6] | — | — | — | 0.0000 |
| `R3` | +2.74 pts | [+2.2, +3.3] | — | — | — | 0.0000 |
| `R1` | +2.73 pts | [+2.2, +3.3] | — | — | — | 0.0000 |
| `G6` | +2.22 pts | [+1.7, +2.7] | — | — | — | 0.0000 |
| `R5` | +1.36 pts | [+0.7, +2.0] | — | — | — | 0.0004 |
| `G7` | +1.35 pts | [+0.8, +1.9] | — | — | — | 0.0001 |
| `G5` | +1.34 pts | [+0.9, +1.8] | — | — | — | 0.0000 |
| `M1` | +1.07 pts | [+0.6, +1.6] | — | — | — | 0.0003 |
| `R6` | +0.97 pts | [+0.7, +1.3] | — | — | — | 0.0000 |
| `G3` | +0.95 pts | [+0.4, +1.5] | — | — | — | 0.0021 |
| `G8` | +0.93 pts | [+0.6, +1.3] | — | — | — | 0.0000 |
| `G9` | +0.88 pts | [+0.5, +1.3] | — | — | — | 0.0008 |
| `G13` | +0.82 pts | [+0.5, +1.1] | — | — | — | 0.0000 |
| `G4` | +0.78 pts | [+0.4, +1.2] | — | — | — | 0.0021 |
| `G2` | +0.71 pts | [+0.3, +1.1] | — | — | — | 0.0030 |
| `G12` | +0.59 pts | [+0.2, +1.0] | — | — | — | 0.0088 |
| `G11` | +0.44 pts | [-0.0, +0.9] | — | — | — | 0.1203 |
| `M4` | -0.29 pts | [-0.8, +0.2] | — | — | — | 0.2465 |

### Carrés factoriels `2×2` des lisières (`I_2x2 = Y11 - Y10 - Y01 + Y00`)

| Lisière | Paire | Fond | Y00 | Y10 (A) | Y01 (B) | Y11 (A+B) | Interaction `I_2x2` | IC95 `I_2x2` |
|---|---|---|---:|---:|---:|---:|---:|---|
| `R_I` | `G14`+`M2` | `ALL_NEUTRE` | 50.3 % | 54.2 % | 67.3 % | 66.9 % | -4.29 pts | [-5.0, -3.5] |
| `E_I` | `R10`+`M5` | `ALL_NEUTRE` | 50.6 % | 58.4 % | 59.7 % | 63.2 % | -4.25 pts | [-4.9, -3.6] |
| `R_E` | `G10`+`R8` | `ALL_NEUTRE` | 51.1 % | 60.4 % | 56.0 % | 62.5 % | -2.80 pts | [-3.6, -2.0] |
| `M_H` | `G7`+`R3` | `ALL_NEUTRE` | 52.3 % | 53.6 % | 55.0 % | 54.3 % | -2.05 pts | [-2.7, -1.4] |
| `O_I` | `G15`+`M3` | `ALL_NEUTRE` | 51.6 % | 56.3 % | 54.6 % | 57.6 % | -1.70 pts | [-2.2, -1.2] |
| `O_E` | `G12`+`R9` | `ALL_NEUTRE` | 52.2 % | 52.8 % | 57.6 % | 56.9 % | -1.30 pts | [-1.7, -0.9] |
| `M_R` | `G1`+`G2` | `ALL_NEUTRE` | 51.0 % | 54.6 % | 51.7 % | 54.0 % | -1.29 pts | [-2.0, -0.6] |
| `H_E` | `R1`+`R2` | `ALL_NEUTRE` | 51.3 % | 54.0 % | 55.5 % | 57.1 % | -1.15 pts | [-1.9, -0.4] |
| `H_I` | `R6`+`M4` | `ALL_NEUTRE` | 50.9 % | 51.9 % | 50.7 % | 50.5 % | -1.12 pts | [-1.5, -0.8] |
| `M_O` | `G3`+`G4` | `ALL_NEUTRE` | 52.0 % | 53.0 % | 52.8 % | 52.8 % | -0.98 pts | [-1.5, -0.5] |
| `O_H` | `G11`+`R5` | `ALL_NEUTRE` | 52.6 % | 53.0 % | 53.9 % | 53.5 % | -0.89 pts | [-1.5, -0.2] |
| `R_H` | `G9`+`R4` | `ALL_NEUTRE` | 51.2 % | 52.0 % | 60.9 % | 61.0 % | -0.77 pts | [-1.4, -0.2] |
| `M_E` | `G8`+`R7` | `ALL_NEUTRE` | 50.8 % | 51.7 % | 55.9 % | 56.2 % | -0.61 pts | [-1.2, -0.1] |
| `R_O` | `G5`+`G6` | `ALL_NEUTRE` | 52.1 % | 53.4 % | 54.3 % | 55.1 % | -0.52 pts | [-1.1, +0.1] |
| `M_I` | `G13`+`M1` | `ALL_NEUTRE` | 50.7 % | 51.5 % | 51.8 % | 52.2 % | -0.41 pts | [-0.9, +0.1] |
