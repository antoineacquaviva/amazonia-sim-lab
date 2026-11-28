# Rapport d'analyse — `audit_equilibrage_v6_4__05_micro_forks_causaux_v6_4`

- **Campagne** : `audit_equilibrage_v6_4__05_micro_forks_causaux_v6_4` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:36:42Z` | **Mode** : `4` | **Parties simulées** : `2 364`
- **Tables** : `ALL_197_ASSISES` (`[3, 4, 5, 6]`) | **Bots** : `B2`
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4__05_micro_forks_causaux_v6_4.json`

## 1. Alertes automatiques d'équilibrage

- **🟠 VIGILANCE** (`ECART_3J_6J`) : Écart inter-tailles modéré (7.5 pts : 3J vs 6J).
- **🟠 VIGILANCE** (`DISPERSION_197_ASSISES`) : Dispersion forte sur les assises (40.3 pts : N3-HMI=40.8% vs N6-HRMEOI=81.1%).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : Ratio manipulation/décision élevé (2.47 > 1.8).
- **🟠 VIGILANCE** (`FAUX_DILEMME_BOUCLIER_LISIERE_5_3`) : Faux dilemme v6.4 `bouclier_lisiere_5_3` : UTILISER_BOUCLIER choisi 100.0 % (n=551).
- **🟠 VIGILANCE** (`FAUX_DILEMME_SABOTAGE_CIBLE_3_2`) : Faux dilemme v6.4 `sabotage_cible_3_2` : REFROIDIR_ROUGE choisi 96.4 % (n=4490).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G11_HARPIE`) : Faux dilemme d'effet `G11_HARPIE` : FONDRE choisi 100.0 % (n=511).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G3_ATELE`) : Faux dilemme d'effet `G3_ATELE` : TUPLE_5 choisi 100.0 % (n=234).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F1_DRINK_BLUE_CROC`) : Faux dilemme d'effet `G5_F1_DRINK_BLUE_CROC` : TUPLE_4 choisi 100.0 % (n=41).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F2_DRINK_BLUE_PIEGE`) : Faux dilemme d'effet `G5_F2_DRINK_BLUE_PIEGE` : TUPLE_4 choisi 100.0 % (n=118).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G8_BOTO`) : Faux dilemme d'effet `G8_BOTO` : SLIDE choisi 100.0 % (n=351).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M1_EMBARQUER`) : Faux dilemme d'effet `M1_EMBARQUER` : TUPLE_3 choisi 100.0 % (n=1660).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_PROD_REPTILE`) : Faux dilemme d'effet `M2_PROD_REPTILE` : SEMER_ECAILLE choisi 99.4 % (n=2505).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_BIVOUAC_MARCHE`) : Faux dilemme d'effet `M3_BIVOUAC_MARCHE` : CIBLE_PARCELLE_OU_MACHINE choisi 100.0 % (n=1559).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_FRONT_DE_RAID`) : Faux dilemme d'effet `M3_FRONT_DE_RAID` : TUPLE_3 choisi 94.9 % (n=548).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M4_MELIPONES_RELEVER`) : Faux dilemme d'effet `M4_MELIPONES_RELEVER` : TUPLE_4 choisi 99.3 % (n=1988).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M5_FILAMENTS_ONIRIQUES`) : Faux dilemme d'effet `M5_FILAMENTS_ONIRIQUES` : ALTERER choisi 99.7 % (n=3409).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R10_SPECTRAL_ALTER`) : Faux dilemme d'effet `R10_SPECTRAL_ALTER` : ALTERER choisi 100.0 % (n=633).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R1_ECHO_TAMBOUR`) : Faux dilemme d'effet `R1_ECHO_TAMBOUR` : PASSER_TAMBOUR choisi 100.0 % (n=90).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R2_FLEUVE_CHOICE`) : Faux dilemme d'effet `R2_FLEUVE_CHOICE` : ALTERER choisi 99.9 % (n=1900).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R3_CHAMANE_JAGUAR_BOND`) : Faux dilemme d'effet `R3_CHAMANE_JAGUAR_BOND` : JUMP choisi 96.6 % (n=4073).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_MAUDIRE_OU_SIFFLER`) : Faux dilemme d'effet `R9_MAUDIRE_OU_SIFFLER` : MAUDIRE choisi 99.8 % (n=2508).

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 67.4 % |
| Queue basse CVaR20 | 51.4 % |
| Fin Tour 8 | 79.7 % |
| Fin Sommeil (Rêves rang 1) | 17.8 % |
| Fin Éveil (Gardiens A+1) | 2.6 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.58 tours |

## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées

| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B2` | 2364 | 67.4 % | 51.4 % | 79.7 % | 17.8 % | 2.6 % | 0.0 % |

## 4. Équilibrage par nombre de joueurs (3J–6J)

| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3J | 240 | 63.0 % | 41.5 % | 96.2 % | 2.1 % | 1.7 % | 0.0 % |
| 4J | 540 | 64.1 % | 47.1 % | 91.8 % | 6.5 % | 1.7 % | 0.0 % |
| 5J | 864 | 68.1 % | 53.8 % | 79.0 % | 18.1 % | 2.9 % | 0.0 % |
| 6J | 720 | 70.6 % | 59.0 % | 65.7 % | 31.1 % | 3.2 % | 0.0 % |

### Couverture des assises canoniques (197 assises / 42 compositions)

**Pires assises (survie la plus basse)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N3-HMI` | `N3-HMI` | 12 | 40.8 % | 0.0 % | 8.3 % | 0.0 % |
| `N4-HEMI` | `N4-HEMI` | 12 | 49.4 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HRMI` | `N4-HMRI` | 12 | 51.9 % | 0.0 % | 16.7 % | 0.0 % |
| `N5-HORMI` | `N5-HMROI` | 12 | 54.2 % | 0.0 % | 16.7 % | 0.0 % |
| `N4-HOMI` | `N4-HMOI` | 12 | 54.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-EMI` | `N3-EMI` | 12 | 55.0 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HEI` | `N3-HEI` | 12 | 55.0 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HEM` | `N3-HEM` | 12 | 56.1 % | 8.3 % | 8.3 % | 0.0 % |

**Meilleures assises (survie la plus haute)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N6-HRMEOI` | `N6-HEMROI` | 12 | 81.1 % | 8.3 % | 0.0 % | 0.0 % |
| `N6-HMEORI` | `N6-HEMROI` | 12 | 79.4 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-ROI` | `N3-ROI` | 12 | 79.2 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HEOR` | `N4-HERO` | 12 | 77.1 % | 25.0 % | 0.0 % | 0.0 % |
| `N5-EMOIR` | `N5-EMROI` | 12 | 76.2 % | 66.7 % | 0.0 % | 0.0 % |
| `N5-HEOIR` | `N5-HEROI` | 12 | 75.8 % | 8.3 % | 0.0 % | 0.0 % |
| `N6-HERIMO` | `N6-HEMROI` | 12 | 75.4 % | 66.7 % | 0.0 % | 0.0 % |
| `N6-HMEOIR` | `N6-HEMROI` | 12 | 75.3 % | 41.7 % | 0.0 % | 0.0 % |

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
| `bouclier_lisiere_5_3` | 551 | `UTILISER_BOUCLIER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `chaman_2_1` | 14425 | `TAMBOUR` | 76.6 % | 0.78 | OK |
| `choix_case_gardien_3_1` | 11135 | `CASE_3` | 22.3 % | 0.96 | OK |
| `deploiement_nid_4_2` | 13419 | `FORET` | 53.9 % | 0.85 | OK |
| `enracinement_6_1` | 61317 | `PASSER` | 79.9 % | 0.72 | OK |
| `mammifere_duel_2` | 11947 | `POSER_DUEL_DEFI` | 85.2 % | 0.61 | OK |
| `oiseau_de_1_3` | 9268 | `D1_PREMIER` | 51.0 % | 1.00 | OK |
| `oiseau_plume_2` | 32637 | `CHAUD` | 78.6 % | 0.75 | OK |
| `sabotage_cible_3_2` | 4490 | `REFROIDIR_ROUGE` | 96.4 % | 0.22 | ⚠️ FAUX DILEMME |
| `effet:BUG_DEVIATION_SYNAPTIQUE_3_2` | 3208 | `M_MOINS_1` | 47.8 % | 0.96 | OK |
| `effet:G10_F1_MATAMATA` | 431 | `ENVOUTER` | 73.8 % | 0.83 | OK |
| `effet:G11_HARPIE` | 511 | `FONDRE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G12_F2_SLIDE_REVE` | 12 | `GLISSER` | 100.0 % | 0.00 | OK |
| `effet:G12_IBIJAU` | 337 | `CIBLE_PARCELLE_OU_MACHINE` | 89.9 % | 0.47 | OK |
| `effet:G14_POSE_PONTE` | 184 | `VAL_2` | 52.2 % | 0.84 | OK |
| `effet:G15_COLIBRI_DST` | 13 | `FORET` | 100.0 % | 0.00 | OK |
| `effet:G15_COLIBRI_SRC` | 264 | `PARCEL` | 60.2 % | 0.61 | OK |
| `effet:G1_F2_CROC_DUEL` | 78 | `CROC_AND_DUEL` | 61.5 % | 0.96 | OK |
| `effet:G2_ANACONDA` | 1 | `ETOUFFER_RECULER` | 100.0 % | 0.00 | OK |
| `effet:G3_ATELE` | 234 | `TUPLE_5` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G4_FIRST_CRI` | 13 | `VAL_5` | 53.9 % | 0.81 | OK |
| `effet:G4_SECOND_CRI` | 8 | `FREE` | 100.0 % | 0.00 | OK |
| `effet:G5_F1_DRINK_BLUE_CROC` | 41 | `TUPLE_4` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G5_F2_DRINK_BLUE_PIEGE` | 118 | `TUPLE_4` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G6_CRI_DE_VAPEUR` | 254 | `VAL_5` | 40.2 % | 0.89 | OK |
| `effet:G7_TAPIR` | 110 | `FOULER_DUEL` | 50.9 % | 0.75 | OK |
| `effet:G8_BOTO` | 351 | `SLIDE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M1_EMBARQUER` | 1660 | `TUPLE_3` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M2_PROD_REPTILE` | 2505 | `SEMER_ECAILLE` | 99.4 % | 0.05 | ⚠️ FAUX DILEMME |
| `effet:M2_SOLDATS_A_GLU` | 6 | `SOLDATS_A_GLU` | 100.0 % | 0.00 | OK |
| `effet:M3_BIVOUAC_MARCHE` | 1559 | `CIBLE_PARCELLE_OU_MACHINE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M3_FRONT_DE_RAID` | 548 | `TUPLE_3` | 94.9 % | 0.29 | ⚠️ FAUX DILEMME |
| `effet:M4_MELIPONES_RELEVER` | 1988 | `TUPLE_4` | 99.3 % | 0.06 | ⚠️ FAUX DILEMME |
| `effet:M5_FILAMENTS_ONIRIQUES` | 3409 | `ALTERER` | 99.7 % | 0.03 | ⚠️ FAUX DILEMME |
| `effet:R10_BRANCH` | 2101 | `ENVOL` | 69.8 % | 0.88 | OK |
| `effet:R10_ENVOL_BONUS` | 1433 | `ALTERER` | 77.1 % | 0.78 | OK |
| `effet:R10_SLIDE_REVE` | 1025 | `VAL_5` | 39.2 % | 0.97 | OK |
| `effet:R10_SPECTRAL_ALTER` | 633 | `ALTERER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:R1_ECHO_TAMBOUR` | 90 | `PASSER_TAMBOUR` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:R1_PULL_ENTITY` | 1038 | `VAL_9` | 36.6 % | 0.93 | OK |
| `effet:R2_FLEUVE_CHOICE` | 1900 | `ALTERER` | 99.9 % | 0.01 | ⚠️ FAUX DILEMME |
| `effet:R3_CHAMANE_JAGUAR_BOND` | 4073 | `JUMP` | 96.6 % | 0.21 | ⚠️ FAUX DILEMME |
| `effet:R4_PIROGUE` | 1329 | `POUSSEE` | 60.6 % | 0.97 | OK |
| `effet:R5_CIEL_EAUX` | 1482 | `SWAP` | 64.7 % | 0.94 | OK |
| `effet:R6_CUEILLIR` | 179 | `PARCEL` | 82.1 % | 0.68 | OK |
| `effet:R6_PIQURES` | 45 | `VAL_3` | 26.7 % | 0.94 | OK |
| `effet:R8_ALTER_OR_COOL` | 3997 | `REFROIDIR` | 68.3 % | 0.90 | OK |
| `effet:R8_SLIDE_REVE` | 1516 | `VAL_5` | 38.4 % | 0.98 | OK |
| `effet:R9_MAUDIRE_OU_SIFFLER` | 2508 | `MAUDIRE` | 99.8 % | 0.02 | ⚠️ FAUX DILEMME |
| `effet:R9_SIFFLER_SECOND` | 5 | `SIFFLER` | 100.0 % | 0.00 | OK |
