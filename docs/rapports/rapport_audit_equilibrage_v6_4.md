# Rapport d'analyse — `audit_equilibrage_v6_4`

- **Campagne** : `audit_equilibrage_v6_4` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:42:10Z` | **Mode** : `4` | **Parties simulées** : `273 088`
- **Tables** : `SUITE_MULTI_ETAPES` (`[3, 4, 5, 6]`) | **Bots** : `B0, B1, B2, B2_OPEN, B3`
- **Parties remarquables (`human_trace_1.0`)** : `docs/traces/traces_audit_equilibrage_v6_4__01_assises_197_b0_b3.jsonl` (ouvrable dans `docs/human_logger.html`)
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4.json`

## 1. Alertes automatiques d'équilibrage

- **🟠 VIGILANCE** (`ECART_3J_6J`) : [01_assises_197_b0_b3] Écart inter-tailles modéré (7.3 pts : 3J vs 6J).
- **🟠 VIGILANCE** (`B3_BASCULE_FIN`) : [01_assises_197_b0_b3] B3 MCTS décale fortement la fin `sommeil` (-16.2 pts vs B2) — exploit possible.
- **🟠 VIGILANCE** (`DISPERSION_197_ASSISES`) : [01_assises_197_b0_b3] Dispersion forte sur les assises (31.3 pts : N3-HMI=46.9% vs N6-HMEOIR=78.2%).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : [01_assises_197_b0_b3] Ratio manipulation/décision élevé (2.57 > 1.8).
- **🟠 VIGILANCE** (`FAUX_DILEMME_BOUCLIER_LISIERE_5_3`) : [01_assises_197_b0_b3] Faux dilemme v6.4 `bouclier_lisiere_5_3` : UTILISER_BOUCLIER choisi 99.9 % (n=3968).
- **🟠 VIGILANCE** (`FAUX_DILEMME_SABOTAGE_CIBLE_3_2`) : [01_assises_197_b0_b3] Faux dilemme v6.4 `sabotage_cible_3_2` : REFROIDIR_ROUGE choisi 93.7 % (n=85307).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G11_HARPIE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G11_HARPIE` : FONDRE choisi 99.0 % (n=5948).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G12_F2_SLIDE_REVE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G12_F2_SLIDE_REVE` : GLISSER choisi 100.0 % (n=77).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G15_COLIBRI_DST`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G15_COLIBRI_DST` : FORET choisi 100.0 % (n=249).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G3_ATELE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G3_ATELE` : TUPLE_5 choisi 98.8 % (n=3144).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F1_DRINK_BLUE_CROC`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G5_F1_DRINK_BLUE_CROC` : TUPLE_4 choisi 99.5 % (n=412).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F2_DRINK_BLUE_PIEGE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G5_F2_DRINK_BLUE_PIEGE` : TUPLE_4 choisi 99.0 % (n=776).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G8_BOTO`) : [01_assises_197_b0_b3] Faux dilemme d'effet `G8_BOTO` : SLIDE choisi 99.0 % (n=3828).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M1_EMBARQUER`) : [01_assises_197_b0_b3] Faux dilemme d'effet `M1_EMBARQUER` : TUPLE_3 choisi 99.2 % (n=18012).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_SOLDATS_A_GLU`) : [01_assises_197_b0_b3] Faux dilemme d'effet `M2_SOLDATS_A_GLU` : SOLDATS_A_GLU choisi 92.8 % (n=97).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_BIVOUAC_MARCHE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `M3_BIVOUAC_MARCHE` : CIBLE_PARCELLE_OU_MACHINE choisi 94.3 % (n=38540).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M4_MELIPONES_RELEVER`) : [01_assises_197_b0_b3] Faux dilemme d'effet `M4_MELIPONES_RELEVER` : TUPLE_4 choisi 98.4 % (n=18377).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M5_FILAMENTS_ONIRIQUES`) : [01_assises_197_b0_b3] Faux dilemme d'effet `M5_FILAMENTS_ONIRIQUES` : ALTERER choisi 95.7 % (n=50055).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R10_SPECTRAL_ALTER`) : [01_assises_197_b0_b3] Faux dilemme d'effet `R10_SPECTRAL_ALTER` : ALTERER choisi 98.1 % (n=11042).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R1_ECHO_TAMBOUR`) : [01_assises_197_b0_b3] Faux dilemme d'effet `R1_ECHO_TAMBOUR` : PASSER_TAMBOUR choisi 96.1 % (n=542).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R2_FLEUVE_CHOICE`) : [01_assises_197_b0_b3] Faux dilemme d'effet `R2_FLEUVE_CHOICE` : ALTERER choisi 98.0 % (n=25165).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R3_CHAMANE_JAGUAR_BOND`) : [01_assises_197_b0_b3] Faux dilemme d'effet `R3_CHAMANE_JAGUAR_BOND` : JUMP choisi 94.5 % (n=44534).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_MAUDIRE_OU_SIFFLER`) : [01_assises_197_b0_b3] Faux dilemme d'effet `R9_MAUDIRE_OU_SIFFLER` : MAUDIRE choisi 92.6 % (n=33343).
- **🟠 VIGILANCE** (`ANTISYNERGIE_G1`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur G1 : levier synergique L_syn = -4.3 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_G10`) : [02_solo_et_loo_30_tuiles] Tuile G10 très dominante en solo (+9.3 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_G10`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur G10 : levier synergique L_syn = -8.5 pts.
- **🟠 VIGILANCE** (`ANTISYNERGIE_G14`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur G14 : levier synergique L_syn = -4.9 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_R4`) : [02_solo_et_loo_30_tuiles] Tuile R4 très dominante en solo (+9.7 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_R4`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur R4 : levier synergique L_syn = -6.1 pts.
- **🟠 VIGILANCE** (`ANTISYNERGIE_R10`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur R10 : levier synergique L_syn = -6.5 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_M2`) : [02_solo_et_loo_30_tuiles] Tuile M2 très dominante en solo (+16.9 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_M2`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur M2 : levier synergique L_syn = -11.1 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_M5`) : [02_solo_et_loo_30_tuiles] Tuile M5 très dominante en solo (+9.1 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_M5`) : [02_solo_et_loo_30_tuiles] Anti-synergie sur M5 : levier synergique L_syn = -9.4 pts.
- **🟠 VIGILANCE** (`FAUX_DILEMME_MAMMIFERE_DUEL_2`) : [02_solo_et_loo_30_tuiles] Faux dilemme v6.4 `mammifere_duel_2` : POSER_DUEL_DEFI choisi 91.7 % (n=562539).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G12_IBIJAU`) : [02_solo_et_loo_30_tuiles] Faux dilemme d'effet `G12_IBIJAU` : CIBLE_PARCELLE_OU_MACHINE choisi 90.1 % (n=8114).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G4_SECOND_CRI`) : [02_solo_et_loo_30_tuiles] Faux dilemme d'effet `G4_SECOND_CRI` : FREE choisi 91.8 % (n=171).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_PROD_REPTILE`) : [02_solo_et_loo_30_tuiles] Faux dilemme d'effet `M2_PROD_REPTILE` : SEMER_ECAILLE choisi 99.3 % (n=47821).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_FRONT_DE_RAID`) : [02_solo_et_loo_30_tuiles] Faux dilemme d'effet `M3_FRONT_DE_RAID` : TUPLE_3 choisi 95.9 % (n=12915).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_SIFFLER_SECOND`) : [02_solo_et_loo_30_tuiles] Faux dilemme d'effet `R9_SIFFLER_SECOND` : SIFFLER choisi 100.0 % (n=91).
- **🟠 VIGILANCE** (`EDGE_ANTISYN_R_I`) : [03_carres_2x2_15_lisieres] Lisière 2×2 R_I (G14+M2) : anti-synergie I_2x2 = -4.3 pts.
- **🟠 VIGILANCE** (`EDGE_ANTISYN_E_I`) : [03_carres_2x2_15_lisieres] Lisière 2×2 E_I (R10+M5) : anti-synergie I_2x2 = -4.2 pts.

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 59.5 % |
| Queue basse CVaR20 | 39.6 % |
| Fin Tour 8 | 92.2 % |
| Fin Sommeil (Rêves rang 1) | 5.0 % |
| Fin Éveil (Gardiens A+1) | 2.8 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.82 tours |

## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées

| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B0` | 11820 | 40.9 % | 18.6 % | 97.0 % | 3.0 % | 0.0 % | 0.0 % |
| `B1` | 11820 | 56.0 % | 37.8 % | 96.2 % | 2.7 % | 1.1 % | 0.0 % |
| `B2` | 11820 | 67.5 % | 51.5 % | 79.2 % | 18.1 % | 2.8 % | 0.0 % |
| `B2_OPEN` | 11820 | 69.8 % | 53.9 % | 94.4 % | 5.3 % | 0.3 % | 0.0 % |
| `B3` | 2364 | 69.8 % | 50.3 % | 92.4 % | 1.8 % | 5.8 % | 0.0 % |

### Audit anti-stratégies dégénérées (`B3 MCTS` vs `B2`)

- **Écart moyen `B3 - B2`** : +2.05 pts (sur 197 tables appariées CRN)
- **Décalage des fins (`B3 - B2`)** : tour_8: +13.2 pts, sommeil: -16.2 pts, eveil: +3.0 pts, effondrement: +0.0 pts
- **Assises où B3 exploite le plus l'écart** :
  - `N3-HMI` : B3=65.3 % vs B2=47.2 % (`+18.1 pts`)
  - `N3-HOI` : B3=70.3 % vs B2=55.8 % (`+14.4 pts`)
  - `N4-HMIO` : B3=66.0 % vs B2=53.1 % (`+12.9 pts`)
  - `N4-HMOI` : B3=69.4 % vs B2=57.9 % (`+11.5 pts`)
  - `N3-MOI` : B3=75.0 % vs B2=63.9 % (`+11.1 pts`)

## 4. Équilibrage par nombre de joueurs (3J–6J)

| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3J | 5040 | 55.2 % | 26.5 % | 98.3 % | 0.9 % | 0.8 % | 0.0 % |
| 4J | 11340 | 55.9 % | 28.5 % | 96.3 % | 2.8 % | 0.9 % | 0.0 % |
| 5J | 18144 | 59.3 % | 33.3 % | 92.0 % | 6.9 % | 1.1 % | 0.0 % |
| 6J | 15120 | 62.5 % | 39.0 % | 85.8 % | 12.3 % | 1.9 % | 0.0 % |

### Couverture des assises canoniques (197 assises / 42 compositions)

**Pires assises (survie la plus basse)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N3-HMI` | `N3-HMI` | 60 | 46.9 % | 0.0 % | 8.3 % | 0.0 % |
| `N4-HEMI` | `N4-HEMI` | 60 | 53.2 % | 0.0 % | 10.0 % | 0.0 % |
| `N4-HOMI` | `N4-HMOI` | 60 | 53.5 % | 0.0 % | 1.7 % | 0.0 % |
| `N5-HORMI` | `N5-HMROI` | 60 | 54.6 % | 0.0 % | 10.0 % | 0.0 % |
| `N3-HOI` | `N3-HOI` | 60 | 55.9 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HMR` | `N3-HMR` | 60 | 56.0 % | 1.7 % | 1.7 % | 0.0 % |
| `N4-MROI` | `N4-MROI` | 60 | 56.5 % | 0.0 % | 1.7 % | 0.0 % |
| `N4-HRMI` | `N4-HMRI` | 60 | 56.6 % | 1.7 % | 6.7 % | 0.0 % |

**Meilleures assises (survie la plus haute)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N6-HMEOIR` | `N6-HEMROI` | 60 | 78.2 % | 28.3 % | 5.0 % | 0.0 % |
| `N5-HMEOR` | `N5-HEMRO` | 60 | 75.6 % | 35.0 % | 1.7 % | 0.0 % |
| `N6-HEMORI` | `N6-HEMROI` | 60 | 75.4 % | 3.3 % | 1.7 % | 0.0 % |
| `N6-HEMOIR` | `N6-HEMROI` | 60 | 75.2 % | 33.3 % | 0.0 % | 0.0 % |
| `N6-HRMEOI` | `N6-HEMROI` | 60 | 75.1 % | 18.3 % | 6.7 % | 0.0 % |
| `N6-HEMIOR` | `N6-HEMROI` | 60 | 74.7 % | 43.3 % | 0.0 % | 0.0 % |
| `N3-ROI` | `N3-ROI` | 60 | 74.7 % | 0.0 % | 0.0 % | 0.0 % |
| `N6-HEMRIO` | `N6-HEMROI` | 60 | 74.5 % | 13.3 % | 5.0 % | 0.0 % |

## 5. Étude modulaire « Tuiles à blanc » (`SUITE_MULTI_ETAPES`)

### Plancher Solo, Retrait Écosystème (LOO) & Levier Synergique (`L_syn = Δ_éco - Δ_solo`)

| Tuile | Δ Solo (vs ALL_NEUTRE) | IC95 Solo | Δ Éco (ALL_ACTIVE - LOO) | IC95 Éco | Levier Synergique `L_syn` | p-Holm |
|---|---:|---|---:|---|---:|---:|
| `M2` | +16.94 pts | [+16.3, +17.6] | +5.83 pts | [+4.7, +6.9] | -11.11 pts | 0.0000 |
| `R4` | +9.73 pts | [+8.7, +10.8] | +3.60 pts | [+2.5, +4.7] | -6.13 pts | 0.0000 |
| `R7` | +5.10 pts | [+4.5, +5.7] | +3.53 pts | [+2.9, +4.2] | -1.57 pts | 0.0000 |
| `R9` | +5.38 pts | [+4.8, +5.9] | +2.57 pts | [+1.9, +3.2] | -2.80 pts | 0.0000 |
| `G7` | +1.35 pts | [+0.8, +1.9] | -1.79 pts | [-2.2, -1.3] | -3.14 pts | 0.0000 |
| `R2` | +4.21 pts | [+3.6, +4.9] | +1.42 pts | [+0.7, +2.2] | -2.79 pts | 0.0067 |
| `G15` | +4.74 pts | [+4.3, +5.2] | +1.41 pts | [+1.1, +1.8] | -3.33 pts | 0.0000 |
| `R10` | +7.80 pts | [+7.0, +8.5] | +1.34 pts | [+0.8, +1.9] | -6.46 pts | 0.0005 |
| `R8` | +4.93 pts | [+4.3, +5.5] | +1.29 pts | [+0.4, +2.2] | -3.64 pts | 0.0733 |
| `G14` | +3.90 pts | [+3.3, +4.5] | -0.95 pts | [-1.3, -0.6] | -4.85 pts | 0.0000 |
| `R1` | +2.73 pts | [+2.2, +3.3] | +0.93 pts | [+0.3, +1.5] | -1.80 pts | 0.0363 |
| `M3` | +3.02 pts | [+2.5, +3.6] | +0.82 pts | [+0.5, +1.2] | -2.20 pts | 0.0006 |
| `G10` | +9.32 pts | [+8.6, +10.0] | +0.80 pts | [+0.2, +1.4] | -8.53 pts | 0.0831 |
| `G1` | +3.54 pts | [+2.9, +4.2] | -0.78 pts | [-1.3, -0.3] | -4.32 pts | 0.0284 |
| `M1` | +1.07 pts | [+0.6, +1.6] | -0.77 pts | [-1.1, -0.4] | -1.84 pts | 0.0017 |
| `R3` | +2.74 pts | [+2.2, +3.3] | +0.72 pts | [+0.2, +1.2] | -2.02 pts | 0.0831 |
| `G9` | +0.88 pts | [+0.5, +1.3] | -0.70 pts | [-1.1, -0.4] | -1.58 pts | 0.0034 |
| `M4` | -0.29 pts | [-0.8, +0.2] | -0.68 pts | [-1.0, -0.3] | -0.39 pts | 0.0043 |
| `G13` | +0.82 pts | [+0.5, +1.1] | -0.56 pts | [-0.8, -0.3] | -1.37 pts | 0.0006 |
| `G11` | +0.44 pts | [-0.0, +0.9] | -0.47 pts | [-0.9, -0.1] | -0.91 pts | 0.1395 |
| `G2` | +0.71 pts | [+0.3, +1.1] | -0.46 pts | [-0.8, -0.1] | -1.17 pts | 0.1395 |
| `G6` | +2.22 pts | [+1.7, +2.7] | -0.39 pts | [-0.7, -0.1] | -2.61 pts | 0.1451 |
| `G3` | +0.95 pts | [+0.4, +1.5] | -0.35 pts | [-0.6, -0.1] | -1.30 pts | 0.1107 |
| `G12` | +0.59 pts | [+0.2, +1.0] | -0.33 pts | [-0.6, -0.1] | -0.92 pts | 0.0733 |
| `G4` | +0.78 pts | [+0.4, +1.2] | -0.30 pts | [-0.5, -0.1] | -1.09 pts | 0.1159 |
| `R6` | +0.97 pts | [+0.7, +1.3] | -0.25 pts | [-0.5, +0.0] | -1.21 pts | 0.4483 |
| `M5` | +9.13 pts | [+8.5, +9.7] | -0.24 pts | [-0.8, +0.3] | -9.37 pts | 0.8767 |
| `G5` | +1.34 pts | [+0.9, +1.8] | -0.19 pts | [-0.5, +0.1] | -1.54 pts | 0.8767 |
| `G8` | +0.93 pts | [+0.6, +1.3] | -0.16 pts | [-0.4, +0.1] | -1.08 pts | 0.8767 |
| `R5` | +1.36 pts | [+0.7, +2.0] | -0.02 pts | [-0.7, +0.6] | -1.38 pts | 0.9493 |

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

### Moteurs du jeu (testés seuls vs par ablation)

| Moteur | Tuiles | Δ Solo (vs ALL_NEUTRE) | Δ Ablation (ALL_ACTIVE - sans moteur) | Synergie inter-moteurs |
|---|---|---:|---:|---:|
| `ALTERATION_LOIS` | `G10,R2,R7,R8,R10` | +9.17 pts | +3.97 pts | -5.20 pts |
| `DUEL_TERRAIN_THERMIQUE` | `G1,G2,G5,G7,G9,R3` | +2.25 pts | -0.69 pts | -2.95 pts |
| `ESSAIM_NIDS` | `G13,G14,G15,M1,M2,M3,M4,M5` | +8.83 pts | +2.31 pts | -6.52 pts |
| `MOTEUR_ALTERATION` | `G8,G10,R2,R7,R8,R9,R10,M5` | +11.59 pts | +6.40 pts | -5.19 pts |
| `MOTEUR_CHAMANES_ANNULATION` | `G2,G7,G8,G9,G11,G12,R1,R2,R3,R5,R6,M4` | +2.81 pts | -0.33 pts | -3.14 pts |
| `MOTEUR_DUEL_TERRAIN` | `G1,G2,G4,G7,G13,R3,R7,M1` | +3.22 pts | +0.42 pts | -2.80 pts |
| `MOTEUR_ESSAIM_NIDS` | `G13,G14,G15,R6,R10,M1,M2,M3,M4,M5` | +9.93 pts | +3.93 pts | -6.00 pts |
| `MOTEUR_PERCHOIR_REDEPLOIEMENT` | `G3,G4,G5,G6,G11,G15,R2,R3,R5,R9,M3,M4` | +5.73 pts | +2.06 pts | -3.67 pts |
| `MOTEUR_SOMMEIL_REGLETTE` | `G8,G11,G12,R1,R2,R3,R4,R7,R8,R9,R10,M5` | +14.40 pts | +7.36 pts | -7.04 pts |
| `MOTEUR_THERMIQUE_PIEGE_CROC` | `G1,G2,G5,G6,G7,G9,G10,G12,G14,R4,R5,R8,R9,R10,M2` | +13.14 pts | +8.52 pts | -4.62 pts |
| `REDEPLOIEMENT_PERCHOIR_RELAIS` | `G3,G4,G6,G11,R5` | +1.10 pts | -0.66 pts | -1.76 pts |
| `ROLE_AUTONOMIE_A0` | `R1,R2,R6,R10,M4,M5` | +5.52 pts | +2.46 pts | -3.06 pts |
| `ROLE_CATALYSEURS_EVEIL` | `G1,G3,G4,G5,G6,G8,G9,G10,G11,G12,G13,G14,G15` | +5.19 pts | -0.61 pts | -5.80 pts |
| `ROLE_LEVIERS_REVE` | `G8,R1,R4,R8,R9,R10` | +10.06 pts | +4.66 pts | -5.40 pts |
| `ROLE_LOIS_PASSIVES` | `R7,R8,M5` | +5.65 pts | +1.83 pts | -3.82 pts |
| `ROLE_SYNERGIES_ENRACINEMENT` | `G7,G15,R1,R2` | +3.45 pts | +1.19 pts | -2.26 pts |
| `ROLE_TWISTS_2K3` | `G2,G7,G12,R4,R10,M3` | +6.76 pts | +1.63 pts | -5.13 pts |
| `SOMMEIL_REVES` | `G8,G12,R1,R4,R6,R9` | +6.04 pts | +2.44 pts | -3.60 pts |

- **Synergie holistique (5 moteurs disjoints)** : gain total `ALL_ACTIVE - ALL_NEUTRE` = +16.25 pts | somme des 5 solos = +27.39 pts | interaction holistique = **-11.14 pts**

## 6. Micro-forks causaux `v6.4` (appariés CRN)

| Mécanique / Décision | Ancres | ΔV moyen (survie) | Écart-type |
|---|---:|---:|---:|
| `2_1_b2_vs_b0` | 2363 | -0.32 pts | 3.9 % |
| `2_1_reve` | 2199 | +0.22 pts | 3.1 % |
| `2_2_negociation` | 2363 | +0.24 pts | 2.3 % |
| `furt_rive_piege` | 1059 | +0.62 pts | 3.7 % |
| `furt_rive_sabotage` | 2363 | -0.89 pts | 4.6 % |
| `furt_sentinelle` | 527 | -0.10 pts | 1.5 % |
| `4_1_pose_piege` | 994 | +1.09 pts | 2.9 % |
| `6_1_enracinement` | 1476 | +2.38 pts | 2.8 % |
| `eveil_a_plus_1` | 978 | -2.65 pts | 4.7 % |
| `2_2_gardien_pari` | 2298 | -0.02 pts | 4.0 % |
| `2_1_chaman_chosen_vs_alt` | 1857 | +0.09 pts | 2.1 % |
| `2_1_chaman_tambour_minus_chant` | 1857 | +0.09 pts | 2.1 % |
| `alteration` | 1891 | +1.07 pts | 1.7 % |
| `3_1_gardien_icone` | 2352 | +0.31 pts | 3.0 % |

## 7. Audit Ockham — Choix internes `v6.4` et faux dilemmes (> 90 %)

| Dilemme | Décisions | Choix dominant | Part dominante | Entropie norm. | Verdict |
|---|---:|---|---:|---:|---|
| `bouclier_lisiere_5_3` | 3968 | `UTILISER_BOUCLIER` | 99.9 % | 0.01 | ⚠️ FAUX DILEMME |
| `chaman_2_1` | 314788 | `TAMBOUR` | 85.3 % | 0.60 | OK |
| `choix_case_gardien_3_1` | 203168 | `CASE_1` | 25.1 % | 0.96 | OK |
| `deploiement_nid_4_2` | 207398 | `BUG` | 54.0 % | 0.81 | OK |
| `enracinement_6_1` | 1160630 | `PASSER` | 78.8 % | 0.75 | OK |
| `mammifere_duel_2` | 377415 | `POSER_DUEL_DEFI` | 79.4 % | 0.73 | OK |
| `oiseau_de_1_3` | 216737 | `D1_PREMIER` | 55.1 % | 0.99 | OK |
| `oiseau_plume_2` | 681093 | `CHAUD` | 83.0 % | 0.66 | OK |
| `sabotage_cible_3_2` | 85307 | `REFROIDIR_ROUGE` | 93.7 % | 0.34 | ⚠️ FAUX DILEMME |
| `effet:BUG_DEVIATION_SYNAPTIQUE_3_2` | 109844 | `PASSER` | 39.8 % | 0.99 | OK |
| `effet:G10_F1_MATAMATA` | 5614 | `ENVOUTER` | 67.7 % | 0.91 | OK |
| `effet:G11_HARPIE` | 5948 | `FONDRE` | 99.0 % | 0.08 | ⚠️ FAUX DILEMME |
| `effet:G12_F2_SLIDE_REVE` | 77 | `GLISSER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G12_IBIJAU` | 3008 | `CIBLE_PARCELLE_OU_MACHINE` | 85.3 % | 0.60 | OK |
| `effet:G14_POSE_PONTE` | 1825 | `VAL_2` | 50.4 % | 0.85 | OK |
| `effet:G15_COLIBRI_DST` | 249 | `FORET` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G15_COLIBRI_SRC` | 2658 | `PARCEL` | 59.2 % | 0.64 | OK |
| `effet:G1_F2_CROC_DUEL` | 2019 | `CROC_AND_DUEL` | 51.2 % | 1.00 | OK |
| `effet:G2_ANACONDA` | 12 | `ETOUFFER_RECULER` | 58.3 % | 0.98 | OK |
| `effet:G3_ATELE` | 3144 | `TUPLE_5` | 98.8 % | 0.09 | ⚠️ FAUX DILEMME |
| `effet:G4_FIRST_CRI` | 73 | `VAL_5` | 28.8 % | 0.88 | OK |
| `effet:G4_SECOND_CRI` | 49 | `FREE` | 87.8 % | 0.39 | OK |
| `effet:G5_F1_DRINK_BLUE_CROC` | 412 | `TUPLE_4` | 99.5 % | 0.04 | ⚠️ FAUX DILEMME |
| `effet:G5_F2_DRINK_BLUE_PIEGE` | 776 | `TUPLE_4` | 99.0 % | 0.08 | ⚠️ FAUX DILEMME |
| `effet:G6_CRI_DE_VAPEUR` | 3705 | `VAL_4` | 36.8 % | 0.93 | OK |
| `effet:G7_TAPIR` | 1185 | `FOULER_DUEL` | 50.5 % | 0.79 | OK |
| `effet:G8_BOTO` | 3828 | `SLIDE` | 99.0 % | 0.08 | ⚠️ FAUX DILEMME |
| `effet:M1_EMBARQUER` | 18012 | `TUPLE_3` | 99.2 % | 0.07 | ⚠️ FAUX DILEMME |
| `effet:M2_PROD_REPTILE` | 49436 | `SEMER_ECAILLE` | 85.2 % | 0.41 | OK |
| `effet:M2_SOLDATS_A_GLU` | 97 | `SOLDATS_A_GLU` | 92.8 % | 0.37 | ⚠️ FAUX DILEMME |
| `effet:M3_BIVOUAC_MARCHE` | 38540 | `CIBLE_PARCELLE_OU_MACHINE` | 94.3 % | 0.31 | ⚠️ FAUX DILEMME |
| `effet:M3_FRONT_DE_RAID` | 13270 | `TUPLE_3` | 86.2 % | 0.58 | OK |
| `effet:M4_MELIPONES_RELEVER` | 18377 | `TUPLE_4` | 98.4 % | 0.12 | ⚠️ FAUX DILEMME |
| `effet:M5_FILAMENTS_ONIRIQUES` | 50055 | `ALTERER` | 95.7 % | 0.18 | ⚠️ FAUX DILEMME |
| `effet:R10_BRANCH` | 28235 | `ENVOL` | 59.9 % | 0.63 | OK |
| `effet:R10_ENVOL_BONUS` | 16615 | `ALTERER` | 77.1 % | 0.60 | OK |
| `effet:R10_SLIDE_REVE` | 12782 | `VAL_6` | 33.8 % | 0.87 | OK |
| `effet:R10_SPECTRAL_ALTER` | 11042 | `ALTERER` | 98.1 % | 0.14 | ⚠️ FAUX DILEMME |
| `effet:R1_ECHO_TAMBOUR` | 542 | `PASSER_TAMBOUR` | 96.1 % | 0.24 | ⚠️ FAUX DILEMME |
| `effet:R1_EXTRA_ETOUFFER` | 20 | `VAL_1` | 30.0 % | 0.94 | OK |
| `effet:R1_PULL_ENTITY` | 9710 | `VAL_9` | 29.8 % | 0.95 | OK |
| `effet:R2_FLEUVE_CHOICE` | 25165 | `ALTERER` | 98.0 % | 0.10 | ⚠️ FAUX DILEMME |
| `effet:R3_CHAMANE_JAGUAR_BOND` | 44534 | `JUMP` | 94.5 % | 0.23 | ⚠️ FAUX DILEMME |
| `effet:R4_PIROGUE` | 21444 | `RETOUR` | 45.5 % | 0.87 | OK |
| `effet:R5_CIEL_EAUX` | 18829 | `SWAP` | 65.3 % | 0.76 | OK |
| `effet:R6_CUEILLIR` | 5265 | `RESERVE` | 45.4 % | 0.96 | OK |
| `effet:R6_PIQURES` | 1014 | `VAL_2` | 19.4 % | 0.95 | OK |
| `effet:R8_ALTER_OR_COOL` | 55617 | `REFROIDIR` | 58.1 % | 0.66 | OK |
| `effet:R8_SLIDE_REVE` | 23412 | `VAL_5` | 32.9 % | 0.86 | OK |
| `effet:R9_MAUDIRE_OU_SIFFLER` | 33343 | `MAUDIRE` | 92.6 % | 0.28 | ⚠️ FAUX DILEMME |
| `effet:R9_SIFFLER_SECOND` | 423 | `SIFFLER` | 67.4 % | 0.91 | OK |
| `effet:R9_SIFFLER_SLIDE` | 519 | `VAL_6` | 27.2 % | 0.97 | OK |

## 8. Parties remarquables extraites (`human_trace_1.0`)

Fichier exporté : `docs/traces/traces_audit_equilibrage_v6_4__01_assises_197_b0_b3.jsonl` (14 parties, 764 décisions).

| Catégorie | Bot | Variante | Assise | Fin | Tour | Survie | Décisions |
|---|---|---|---|---|---:|---:|---:|
| `collapse_worst` | `B0` | `BASE` | `N4-HEMR` | `TOUR_8_ATTEINT` | 8 | 0.0 % | 64 |
| `best_score` | `B2_OPEN` | `BASE` | `N3-HRI` | `TOUR_8_ATTEINT` | 8 | 96.7 % | 51 |
| `early_sommeil` | `B2` | `BASE` | `N5-HMEOR` | `REVE_RANG_1` | 2 | 84.0 % | 21 |
| `eveil_success` | `B3` | `BASE` | `N3-HOI` | `REVEIL_GARDIENS` | 5 | 86.7 % | 33 |
| `tour8_clutch` | `B1` | `BASE` | `N4-HEMR` | `TOUR_8_ATTEINT` | 8 | 50.0 % | 91 |
| `b3_vs_b2_outlier` | `B3` | `BASE` | `N3-HMI` | `TOUR_8_ATTEINT` | 8 | 63.3 % | 57 |
| `collapse_worst` | `B0` | `BASE` | `N3-HER` | `TOUR_8_ATTEINT` | 8 | 0.0 % | 48 |
| `best_score` | `B2` | `BASE` | `N3-ERO` | `TOUR_8_ATTEINT` | 8 | 96.7 % | 53 |
| `early_sommeil` | `B2` | `BASE` | `N6-HRIMEO` | `REVE_RANG_1` | 2 | 83.3 % | 39 |
| `eveil_success` | `B3` | `BASE` | `N6-HMEROI` | `REVEIL_GARDIENS` | 6 | 88.3 % | 80 |
| `tour8_clutch` | `B1` | `BASE` | `N3-HEM` | `TOUR_8_ATTEINT` | 8 | 50.0 % | 68 |
| `collapse_worst` | `B0` | `BASE` | `N4-HERM` | `TOUR_8_ATTEINT` | 8 | 0.0 % | 64 |
| `best_score` | `B1` | `BASE` | `N3-ROI` | `TOUR_8_ATTEINT` | 8 | 96.7 % | 66 |
| `early_sommeil` | `B2_OPEN` | `BASE` | `N6-HRIMEO` | `REVE_RANG_1` | 2 | 76.7 % | 29 |

## 9. Récapitulatif de la suite orchestrée

| Étape | Parties | Survie | Alertes critiques | Alertes vigilance | Rapport |
|---|---:|---:|---:|---:|---|
| `01_assises_197_b0_b3` | 49644 | 59.1 % | 0 | 23 | `docs/rapports/rapport_audit_equilibrage_v6_4__01_assises_197_b0_b3.md` |
| `02_solo_et_loo_30_tuiles` | 84680 | 61.0 % | 0 | 38 | `docs/rapports/rapport_audit_equilibrage_v6_4__02_solo_et_loo_30_tuiles.md` |
| `03_carres_2x2_15_lisieres` | 61540 | 55.3 % | 0 | 7 | `docs/rapports/rapport_audit_equilibrage_v6_4__03_carres_2x2_15_lisieres.md` |
| `04_moteurs_disjoints_et_pivots` | 74860 | 61.3 % | 0 | 2 | `docs/rapports/rapport_audit_equilibrage_v6_4__04_moteurs_disjoints_et_pivots.md` |
| `05_micro_forks_causaux_v6_4` | 2364 | 67.4 % | 0 | 21 | `docs/rapports/rapport_audit_equilibrage_v6_4__05_micro_forks_causaux_v6_4.md` |
