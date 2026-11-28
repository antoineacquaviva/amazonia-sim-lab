# Rapport d'analyse — `audit_equilibrage_v6_4__04_moteurs_disjoints_et_pivots`

- **Campagne** : `audit_equilibrage_v6_4__04_moteurs_disjoints_et_pivots` | **Verdict** : `A_SURVEILLER`
- **Généré (UTC)** : `2026-11-28T11:29:20Z` | **Mode** : `4` | **Parties simulées** : `74 860`
- **Tables** : `ALL_197_ASSISES` (`[3, 4, 5, 6]`) | **Bots** : `B2`
- **Digest complet (données brutes)** : `data/digests/digest_audit_equilibrage_v6_4__04_moteurs_disjoints_et_pivots.json`

## 1. Alertes automatiques d'équilibrage

- **🟠 VIGILANCE** (`DISPERSION_197_ASSISES`) : Dispersion forte sur les assises (30.2 pts : N3-HMI=50.7% vs N6-HMEOIR=80.8%).
- **🟠 VIGILANCE** (`MANIPULATION_ELEVEE`) : Ratio manipulation/décision élevé (2.57 > 1.8).

## 2. Indicateurs globaux

| Métrique | Valeur |
|---|---:|
| Survie moyenne (ratio arbres) | 61.3 % |
| Queue basse CVaR20 | 42.3 % |
| Fin Tour 8 | 91.0 % |
| Fin Sommeil (Rêves rang 1) | 4.4 % |
| Fin Éveil (Gardiens A+1) | 4.7 % |
| Effondrement (0 arbre) | 0.0 % |
| Durée moyenne | 7.78 tours |

## 3. Spectre des bots (`B0` → `B3`) et détection de stratégies dégénérées

| Bot | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| `B2` | 74860 | 61.3 % | 42.3 % | 91.0 % | 4.4 % | 4.7 % | 0.0 % |

## 4. Équilibrage par nombre de joueurs (3J–6J)

| Table | Parties | Survie | CVaR20 | Tour 8 | Sommeil | Éveil | Effondrement |
|---|---:|---:|---:|---:|---:|---:|---:|
| 3J | 7600 | 58.6 % | 36.4 % | 95.9 % | 0.6 % | 3.5 % | 0.0 % |
| 4J | 17100 | 58.3 % | 38.2 % | 94.7 % | 1.9 % | 3.4 % | 0.0 % |
| 5J | 27360 | 61.5 % | 43.7 % | 90.0 % | 5.2 % | 4.8 % | 0.0 % |
| 6J | 22800 | 64.2 % | 47.3 % | 87.6 % | 6.7 % | 5.7 % | 0.0 % |

### Couverture des assises canoniques (197 assises / 42 compositions)

**Pires assises (survie la plus basse)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N3-HMI` | `N3-HMI` | 10 | 50.7 % | 0.0 % | 0.0 % | 0.0 % |
| `N4-HOMI` | `N4-HMOI` | 10 | 52.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N5-HORMI` | `N5-HMROI` | 10 | 53.4 % | 0.0 % | 30.0 % | 0.0 % |
| `N4-HRMI` | `N4-HMRI` | 10 | 53.8 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HEM` | `N3-HEM` | 10 | 54.0 % | 10.0 % | 10.0 % | 0.0 % |
| `N4-HMIO` | `N4-HMOI` | 10 | 55.5 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HMO` | `N3-HMO` | 10 | 55.7 % | 0.0 % | 0.0 % | 0.0 % |
| `N3-HMR` | `N3-HMR` | 10 | 55.7 % | 0.0 % | 0.0 % | 0.0 % |

**Meilleures assises (survie la plus haute)** :

| Assise | Composition | Parties | Survie | Sommeil | Éveil | Effondrement |
|---|---|---:|---:|---:|---:|---:|
| `N6-HMEOIR` | `N6-HEMROI` | 10 | 80.8 % | 40.0 % | 0.0 % | 0.0 % |
| `N3-ROI` | `N3-ROI` | 10 | 77.7 % | 0.0 % | 0.0 % | 0.0 % |
| `N6-HEOMIR` | `N6-HEMROI` | 10 | 77.2 % | 10.0 % | 0.0 % | 0.0 % |
| `N6-HEMOIR` | `N6-HEMROI` | 10 | 77.2 % | 10.0 % | 0.0 % | 0.0 % |
| `N6-HMEROI` | `N6-HEMROI` | 10 | 75.8 % | 10.0 % | 0.0 % | 0.0 % |
| `N5-HEOIR` | `N5-HEROI` | 10 | 75.8 % | 20.0 % | 0.0 % | 0.0 % |
| `N6-HEMIOR` | `N6-HEMROI` | 10 | 75.5 % | 40.0 % | 0.0 % | 0.0 % |
| `N5-HMEOR` | `N5-HEMRO` | 10 | 75.4 % | 40.0 % | 0.0 % | 0.0 % |

## 5. Étude modulaire « Tuiles à blanc » (`MOTORS_BOTH`)

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
