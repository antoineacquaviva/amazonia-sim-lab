# Rapport d'analyse — `audit_equilibrage_v6_4__01_assises_197_b0_b3`

- **Campagne** : `audit_equilibrage_v6_4__01_assises_197_b0_b3` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:38:06Z` | **Mode** : `4` | **Parties simulées** : `49 644`
- **Tables** : `ALL_197_ASSISES` (`[3, 4, 5, 6]`) | **Bots** : `B0, B1, B2, B2_OPEN, B3`
- **Parties remarquables (`human_trace_1.0`)** : `docs/traces/traces_audit_equilibrage_v6_4__01_assises_197_b0_b3.jsonl` (ouvrable dans `docs/human_logger.html`)
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4__01_assises_197_b0_b3.json`

## 1. Alertes automatiques d'équilibrage

- **🟠 VIGILANCE** (`ECART_3J_6J`) : Écart inter-tailles modéré (7.3 pts : 3J vs 6J).
- **🟠 VIGILANCE** (`B3_BASCULE_FIN`) : B3 MCTS décale fortement la fin `sommeil` (-16.2 pts vs B2) — exploit possible.
- **🟠 VIGILANCE** (`DISPERSION_197_ASSISES`) : Dispersion forte sur les assises (31.3 pts : N3-HMI=46.9% vs N6-HMEOIR=78.2%).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : Ratio manipulation/décision élevé (2.57 > 1.8).
- **🟠 VIGILANCE** (`FAUX_DILEMME_BOUCLIER_LISIERE_5_3`) : Faux dilemme v6.4 `bouclier_lisiere_5_3` : UTILISER_BOUCLIER choisi 99.9 % (n=3968).
- **🟠 VIGILANCE** (`FAUX_DILEMME_SABOTAGE_CIBLE_3_2`) : Faux dilemme v6.4 `sabotage_cible_3_2` : REFROIDIR_ROUGE choisi 93.7 % (n=85307).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G11_HARPIE`) : Faux dilemme d'effet `G11_HARPIE` : FONDRE choisi 99.0 % (n=5948).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G12_F2_SLIDE_REVE`) : Faux dilemme d'effet `G12_F2_SLIDE_REVE` : GLISSER choisi 100.0 % (n=77).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G15_COLIBRI_DST`) : Faux dilemme d'effet `G15_COLIBRI_DST` : FORET choisi 100.0 % (n=249).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G3_ATELE`) : Faux dilemme d'effet `G3_ATELE` : TUPLE_5 choisi 98.8 % (n=3144).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F1_DRINK_BLUE_CROC`) : Faux dilemme d'effet `G5_F1_DRINK_BLUE_CROC` : TUPLE_4 choisi 99.5 % (n=412).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F2_DRINK_BLUE_PIEGE`) : Faux dilemme d'effet `G5_F2_DRINK_BLUE_PIEGE` : TUPLE_4 choisi 99.0 % (n=776).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G8_BOTO`) : Faux dilemme d'effet `G8_BOTO` : SLIDE choisi 99.0 % (n=3828).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M1_EMBARQUER`) : Faux dilemme d'effet `M1_EMBARQUER` : TUPLE_3 choisi 99.2 % (n=18012).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_SOLDATS_A_GLU`) : Faux dilemme d'effet `M2_SOLDATS_A_GLU` : SOLDATS_A_GLU choisi 92.8 % (n=97).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_BIVOUAC_MARCHE`) : Faux dilemme d'effet `M3_BIVOUAC_MARCHE` : CIBLE_PARCELLE_OU_MACHINE choisi 94.3 % (n=38540).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M4_MELIPONES_RELEVER`) : Faux dilemme d'effet `M4_MELIPONES_RELEVER` : TUPLE_4 choisi 98.4 % (n=18377).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M5_FILAMENTS_ONIRIQUES`) : Faux dilemme d'effet `M5_FILAMENTS_ONIRIQUES` : ALTERER choisi 95.7 % (n=50055).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R10_SPECTRAL_ALTER`) : Faux dilemme d'effet `R10_SPECTRAL_ALTER` : ALTERER choisi 98.1 % (n=11042).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R1_ECHO_TAMBOUR`) : Faux dilemme d'effet `R1_ECHO_TAMBOUR` : PASSER_TAMBOUR choisi 96.1 % (n=542).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R2_FLEUVE_CHOICE`) : Faux dilemme d'effet `R2_FLEUVE_CHOICE` : ALTERER choisi 98.0 % (n=25165).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R3_CHAMANE_JAGUAR_BOND`) : Faux dilemme d'effet `R3_CHAMANE_JAGUAR_BOND` : JUMP choisi 94.5 % (n=44534).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_MAUDIRE_OU_SIFFLER`) : Faux dilemme d'effet `R9_MAUDIRE_OU_SIFFLER` : MAUDIRE choisi 92.6 % (n=33343).

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 59.1 % |
| Queue basse CVaR20 | 32.7 % |
| Fin Tour 8 | 91.7 % |
| Fin Sommeil (Rêves rang 1) | 7.0 % |
| Fin Éveil (Gardiens A+1) | 1.3 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.84 tours |

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
