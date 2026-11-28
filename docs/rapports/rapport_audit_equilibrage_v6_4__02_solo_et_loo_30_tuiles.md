# Rapport d'analyse — `audit_equilibrage_v6_4__02_solo_et_loo_30_tuiles`

- **Campagne** : `audit_equilibrage_v6_4__02_solo_et_loo_30_tuiles` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:16:15Z` | **Mode** : `4` | **Parties simulées** : `84 680`
- **Tables** : `ALL_197_ASSISES` (`[3, 4, 5, 6]`) | **Bots** : `B2`
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4__02_solo_et_loo_30_tuiles.json`

## 1. Alertes automatiques d'équilibrage

- **🟠 VIGILANCE** (`DISPERSION_197_ASSISES`) : Dispersion forte sur les assises (28.9 pts : N3-HMR=48.8% vs N6-HRIMEO=77.8%).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : Ratio manipulation/décision élevé (2.56 > 1.8).
- **🟠 VIGILANCE** (`ANTISYNERGIE_G1`) : Anti-synergie sur G1 : levier synergique L_syn = -4.3 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_G10`) : Tuile G10 très dominante en solo (+9.3 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_G10`) : Anti-synergie sur G10 : levier synergique L_syn = -8.5 pts.
- **🟠 VIGILANCE** (`ANTISYNERGIE_G14`) : Anti-synergie sur G14 : levier synergique L_syn = -4.9 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_R4`) : Tuile R4 très dominante en solo (+9.7 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_R4`) : Anti-synergie sur R4 : levier synergique L_syn = -6.1 pts.
- **🟠 VIGILANCE** (`ANTISYNERGIE_R10`) : Anti-synergie sur R10 : levier synergique L_syn = -6.5 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_M2`) : Tuile M2 très dominante en solo (+16.9 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_M2`) : Anti-synergie sur M2 : levier synergique L_syn = -11.1 pts.
- **🟠 VIGILANCE** (`SOLO_FORT_M5`) : Tuile M5 très dominante en solo (+9.1 pts vs ALL_NEUTRE).
- **🟠 VIGILANCE** (`ANTISYNERGIE_M5`) : Anti-synergie sur M5 : levier synergique L_syn = -9.4 pts.
- **🟠 VIGILANCE** (`FAUX_DILEMME_BOUCLIER_LISIERE_5_3`) : Faux dilemme v6.4 `bouclier_lisiere_5_3` : UTILISER_BOUCLIER choisi 100.0 % (n=13786).
- **🟠 VIGILANCE** (`FAUX_DILEMME_MAMMIFERE_DUEL_2`) : Faux dilemme v6.4 `mammifere_duel_2` : POSER_DUEL_DEFI choisi 91.7 % (n=562539).
- **🟠 VIGILANCE** (`FAUX_DILEMME_SABOTAGE_CIBLE_3_2`) : Faux dilemme v6.4 `sabotage_cible_3_2` : REFROIDIR_ROUGE choisi 97.3 % (n=169130).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G11_HARPIE`) : Faux dilemme d'effet `G11_HARPIE` : FONDRE choisi 100.0 % (n=9485).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G12_F2_SLIDE_REVE`) : Faux dilemme d'effet `G12_F2_SLIDE_REVE` : GLISSER choisi 100.0 % (n=246).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G12_IBIJAU`) : Faux dilemme d'effet `G12_IBIJAU` : CIBLE_PARCELLE_OU_MACHINE choisi 90.1 % (n=8114).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G15_COLIBRI_DST`) : Faux dilemme d'effet `G15_COLIBRI_DST` : FORET choisi 100.0 % (n=228).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G3_ATELE`) : Faux dilemme d'effet `G3_ATELE` : TUPLE_5 choisi 100.0 % (n=5369).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G4_SECOND_CRI`) : Faux dilemme d'effet `G4_SECOND_CRI` : FREE choisi 91.8 % (n=171).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F1_DRINK_BLUE_CROC`) : Faux dilemme d'effet `G5_F1_DRINK_BLUE_CROC` : TUPLE_4 choisi 100.0 % (n=792).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G5_F2_DRINK_BLUE_PIEGE`) : Faux dilemme d'effet `G5_F2_DRINK_BLUE_PIEGE` : TUPLE_4 choisi 100.0 % (n=2345).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_G8_BOTO`) : Faux dilemme d'effet `G8_BOTO` : SLIDE choisi 100.0 % (n=7175).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M1_EMBARQUER`) : Faux dilemme d'effet `M1_EMBARQUER` : TUPLE_3 choisi 100.0 % (n=32646).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_PROD_REPTILE`) : Faux dilemme d'effet `M2_PROD_REPTILE` : SEMER_ECAILLE choisi 99.3 % (n=47821).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M2_SOLDATS_A_GLU`) : Faux dilemme d'effet `M2_SOLDATS_A_GLU` : SOLDATS_A_GLU choisi 100.0 % (n=93).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_BIVOUAC_MARCHE`) : Faux dilemme d'effet `M3_BIVOUAC_MARCHE` : CIBLE_PARCELLE_OU_MACHINE choisi 100.0 % (n=33277).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M3_FRONT_DE_RAID`) : Faux dilemme d'effet `M3_FRONT_DE_RAID` : TUPLE_3 choisi 95.9 % (n=12915).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M4_MELIPONES_RELEVER`) : Faux dilemme d'effet `M4_MELIPONES_RELEVER` : TUPLE_4 choisi 99.3 % (n=39347).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_M5_FILAMENTS_ONIRIQUES`) : Faux dilemme d'effet `M5_FILAMENTS_ONIRIQUES` : ALTERER choisi 99.9 % (n=65907).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R10_SPECTRAL_ALTER`) : Faux dilemme d'effet `R10_SPECTRAL_ALTER` : ALTERER choisi 100.0 % (n=11660).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R1_ECHO_TAMBOUR`) : Faux dilemme d'effet `R1_ECHO_TAMBOUR` : PASSER_TAMBOUR choisi 100.0 % (n=1275).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R2_FLEUVE_CHOICE`) : Faux dilemme d'effet `R2_FLEUVE_CHOICE` : ALTERER choisi 99.7 % (n=34304).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R3_CHAMANE_JAGUAR_BOND`) : Faux dilemme d'effet `R3_CHAMANE_JAGUAR_BOND` : JUMP choisi 96.9 % (n=76948).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_MAUDIRE_OU_SIFFLER`) : Faux dilemme d'effet `R9_MAUDIRE_OU_SIFFLER` : MAUDIRE choisi 99.8 % (n=43685).
- **🟠 VIGILANCE** (`FAUX_DILEMME_EFFET_R9_SIFFLER_SECOND`) : Faux dilemme d'effet `R9_SIFFLER_SECOND` : SIFFLER choisi 100.0 % (n=91).

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 61.0 % |
| Queue basse CVaR20 | 41.9 % |
| Fin Tour 8 | 89.7 % |
| Fin Sommeil (Rêves rang 1) | 7.5 % |
| Fin Éveil (Gardiens A+1) | 2.8 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.77 tours |

## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées

| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B2` | 84680 | 61.0 % | 41.9 % | 89.7 % | 7.5 % | 2.8 % | 0.0 % |

## 4. Équilibrage par nombre de joueurs (3J–6J)

| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3J | 5600 | 57.5 % | 34.6 % | 96.8 % | 0.5 % | 2.7 % | 0.0 % |
| 4J | 16200 | 58.4 % | 38.7 % | 95.3 % | 2.6 % | 2.1 % | 0.0 % |
| 5J | 31680 | 60.8 % | 42.2 % | 89.8 % | 7.1 % | 3.1 % | 0.0 % |
| 6J | 31200 | 63.1 % | 45.1 % | 85.5 % | 11.6 % | 3.0 % | 0.0 % |

### Couverture des assises canoniques (197 assises / 42 compositions)

**Pires assises (survie la plus basse)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N3-HMR` | `N3-HMR` | 20 | 48.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HOMI` | `N4-HMOI` | 20 | 51.9 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-EMI` | `N3-EMI` | 20 | 52.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N5-HORMI` | `N5-HMROI` | 20 | 53.2 % | 0.0 % | 25.0 % | 0.0 % |
| `N3-HMI` | `N3-HMI` | 20 | 53.7 % | 0.0 % | 5.0 % | 0.0 % |
| `N4-ERMI` | `N4-EMRI` | 20 | 54.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HRMI` | `N4-HMRI` | 20 | 55.8 % | 0.0 % | 5.0 % | 0.0 % |
| `N3-EMR` | `N3-EMR` | 20 | 56.0 % | 0.0 % | 5.0 % | 0.0 % |

**Meilleures assises (survie la plus haute)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N6-HRIMEO` | `N6-HEMROI` | 20 | 77.8 % | 45.0 % | 5.0 % | 0.0 % |
| `N6-HMEOIR` | `N6-HEMROI` | 20 | 77.5 % | 45.0 % | 0.0 % | 0.0 % |
| `N3-ROI` | `N3-ROI` | 20 | 76.3 % | 0.0 % | 0.0 % | 0.0 % |
| `N6-HEMIRO` | `N6-HEMROI` | 20 | 75.9 % | 5.0 % | 5.0 % | 0.0 % |
| `N6-HEMRIO` | `N6-HEMROI` | 20 | 75.6 % | 10.0 % | 5.0 % | 0.0 % |
| `N6-HROEMI` | `N6-HEMROI` | 20 | 75.1 % | 5.0 % | 5.0 % | 0.0 % |
| `N6-HEMOIR` | `N6-HEMROI` | 20 | 74.6 % | 45.0 % | 0.0 % | 0.0 % |
| `N6-HEMIOR` | `N6-HEMROI` | 20 | 74.6 % | 30.0 % | 0.0 % | 0.0 % |

## 5. Étude modulaire « Tuiles à blanc » (`SOLO_AND_ECOSYSTEM`)

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

## 7. Audit Ockham — Choix internes `v6.4` et faux dilemmes (> 90 %)

| Dilemme | Décisions | Choix dominant | Part dominante | Entropie norm. | Verdict |
|---|---:|---|---:|---:|---|
| `bouclier_lisiere_5_3` | 13786 | `UTILISER_BOUCLIER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `chaman_2_1` | 550931 | `TAMBOUR` | 85.7 % | 0.59 | OK |
| `choix_case_gardien_3_1` | 421522 | `CASE_1` | 26.7 % | 0.97 | OK |
| `deploiement_nid_4_2` | 487641 | `FORET` | 54.4 % | 0.82 | OK |
| `enracinement_6_1` | 2026676 | `PASSER` | 73.3 % | 0.84 | OK |
| `mammifere_duel_2` | 562539 | `POSER_DUEL_DEFI` | 91.7 % | 0.41 | ⚠️ FAUX DILEMME |
| `oiseau_de_1_3` | 380861 | `D1_PREMIER` | 50.5 % | 1.00 | OK |
| `oiseau_plume_2` | 1209372 | `CHAUD` | 83.4 % | 0.65 | OK |
| `sabotage_cible_3_2` | 169130 | `REFROIDIR_ROUGE` | 97.3 % | 0.18 | ⚠️ FAUX DILEMME |
| `effet:BUG_DEVIATION_SYNAPTIQUE_3_2` | 141576 | `M_MOINS_1` | 50.5 % | 0.94 | OK |
| `effet:G10_F1_MATAMATA` | 8585 | `ENVOUTER` | 68.9 % | 0.89 | OK |
| `effet:G11_HARPIE` | 9485 | `FONDRE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G12_F2_SLIDE_REVE` | 246 | `GLISSER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G12_IBIJAU` | 8114 | `CIBLE_PARCELLE_OU_MACHINE` | 90.1 % | 0.46 | ⚠️ FAUX DILEMME |
| `effet:G14_POSE_PONTE` | 3492 | `VAL_2` | 50.5 % | 0.85 | OK |
| `effet:G15_COLIBRI_DST` | 228 | `FORET` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G15_COLIBRI_SRC` | 4606 | `PARCEL` | 61.1 % | 0.58 | OK |
| `effet:G1_F2_CROC_DUEL` | 3093 | `CROC_AND_DUEL` | 51.1 % | 1.00 | OK |
| `effet:G2_ANACONDA` | 23 | `EXIT_RATISSAGE` | 78.3 % | 0.76 | OK |
| `effet:G3_ATELE` | 5369 | `TUPLE_5` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G4_FIRST_CRI` | 201 | `VAL_5` | 37.8 % | 0.89 | OK |
| `effet:G4_SECOND_CRI` | 171 | `FREE` | 91.8 % | 0.41 | ⚠️ FAUX DILEMME |
| `effet:G5_F1_DRINK_BLUE_CROC` | 792 | `TUPLE_4` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G5_F2_DRINK_BLUE_PIEGE` | 2345 | `TUPLE_4` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:G6_CRI_DE_VAPEUR` | 6306 | `VAL_4` | 38.4 % | 0.92 | OK |
| `effet:G7_TAPIR` | 2367 | `FOULER_DUEL` | 48.8 % | 0.76 | OK |
| `effet:G8_BOTO` | 7175 | `SLIDE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M1_EMBARQUER` | 32646 | `TUPLE_3` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M2_PROD_REPTILE` | 47821 | `SEMER_ECAILLE` | 99.3 % | 0.06 | ⚠️ FAUX DILEMME |
| `effet:M2_SOLDATS_A_GLU` | 93 | `SOLDATS_A_GLU` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M3_BIVOUAC_MARCHE` | 33277 | `CIBLE_PARCELLE_OU_MACHINE` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:M3_FRONT_DE_RAID` | 12915 | `TUPLE_3` | 95.9 % | 0.25 | ⚠️ FAUX DILEMME |
| `effet:M4_MELIPONES_RELEVER` | 39347 | `TUPLE_4` | 99.3 % | 0.06 | ⚠️ FAUX DILEMME |
| `effet:M5_FILAMENTS_ONIRIQUES` | 65907 | `ALTERER` | 99.9 % | 0.01 | ⚠️ FAUX DILEMME |
| `effet:R10_BRANCH` | 41354 | `ENVOL` | 71.8 % | 0.54 | OK |
| `effet:R10_ENVOL_BONUS` | 29106 | `ALTERER` | 78.3 % | 0.75 | OK |
| `effet:R10_SLIDE_REVE` | 18605 | `VAL_5` | 40.1 % | 0.97 | OK |
| `effet:R10_SPECTRAL_ALTER` | 11660 | `ALTERER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:R1_ECHO_TAMBOUR` | 1275 | `PASSER_TAMBOUR` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:R1_EXTRA_ETOUFFER` | 16 | `VAL_3` | 25.0 % | 0.96 | OK |
| `effet:R1_PULL_ENTITY` | 16166 | `VAL_9` | 32.5 % | 0.97 | OK |
| `effet:R2_FLEUVE_CHOICE` | 34304 | `ALTERER` | 99.7 % | 0.03 | ⚠️ FAUX DILEMME |
| `effet:R3_CHAMANE_JAGUAR_BOND` | 76948 | `JUMP` | 96.9 % | 0.13 | ⚠️ FAUX DILEMME |
| `effet:R4_PIROGUE` | 25899 | `POUSSEE` | 64.2 % | 0.94 | OK |
| `effet:R5_CIEL_EAUX` | 27393 | `SWAP` | 68.1 % | 0.90 | OK |
| `effet:R6_CUEILLIR` | 4741 | `PARCEL` | 73.7 % | 0.83 | OK |
| `effet:R6_PIQURES` | 972 | `VAL_1` | 19.9 % | 0.98 | OK |
| `effet:R8_ALTER_OR_COOL` | 69928 | `REFROIDIR` | 68.2 % | 0.90 | OK |
| `effet:R8_SLIDE_REVE` | 26354 | `VAL_5` | 40.1 % | 0.97 | OK |
| `effet:R9_MAUDIRE_OU_SIFFLER` | 43685 | `MAUDIRE` | 99.8 % | 0.02 | ⚠️ FAUX DILEMME |
| `effet:R9_SIFFLER_SECOND` | 91 | `SIFFLER` | 100.0 % | 0.00 | ⚠️ FAUX DILEMME |
| `effet:R9_SIFFLER_SLIDE` | 28 | `VAL_5` | 60.7 % | 0.78 | OK |
