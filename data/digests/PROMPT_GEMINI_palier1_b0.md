Dossier de simulation Amazonia : Dernier Rempart — utilise les règles cœur et statistiques ci-dessous comme unique vérité terrain.

```json
{
  "campaign": "palier1_baseline_b0",
  "generated_at_utc": "2026-11-17T16:31:26Z",
  "active_core_rules": {
    "version": "5.3.1",
    "source_studio_version": "v5.3",
    "studio_sha256": {
      "catalog_v5_3.json": "8f9ef62b478ccef35ca3b850d647d9e125b60834f1b8e1bbdcd92cc197d76c09",
      "spec_formelle_v5_3.json": "cd264fcf967df6f9bf61a4a8ef39b64be5576be2111d73a811afd5e1753602b6"
    },
    "chassis_7_axes": [
      {
        "chassis_id": 0,
        "p_max": 4,
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "declenchement_fin_de_piste": "ARRIVEE_DERNIERE_PARCELLE",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 1,
        "p_max": 5,
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "declenchement_fin_de_piste": "ARRIVEE_DERNIERE_PARCELLE",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 4,
        "p_max": 4,
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 1,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "declenchement_fin_de_piste": "ARRIVEE_DERNIERE_PARCELLE",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 5,
        "p_max": 5,
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 1,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "declenchement_fin_de_piste": "ARRIVEE_DERNIERE_PARCELLE",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 127,
        "p_max": 5,
        "regle_ouverture_reve_multiple": "PAR_DE_M_DESIGNE",
        "offset_seuil_parade": 1,
        "mise_en_place_tactiques": "ALEATOIRE",
        "declenchement_fin_de_piste": "DEPASSEMENT_DERNIERE_PARCELLE",
        "role_abatteuse_fin_de_piste": "ARRACHE_1_SOUCHE_SI_SANS_ARBRE",
        "synergie_binome_machines": "MUTUALISATION_PUISSANCE_MEME_PARCELLE"
      }
    ],
    "tactiques": [
      {
        "id": "T1",
        "nom": "Sur place",
        "cibles": [
          "SUR_PLACE"
        ],
        "avancee": 0,
        "gain_rouge": 0,
        "mod_seuil": 0,
        "est_siege_profil": false
      },
      {
        "id": "T2",
        "nom": "Devant",
        "cibles": [
          "DEVANT"
        ],
        "avancee": 0,
        "gain_rouge": 0,
        "mod_seuil": 0,
        "est_siege_profil": false
      },
      {
        "id": "T3",
        "nom": "En avançant",
        "cibles": [
          "SUR_PLACE",
          "DEVANT"
        ],
        "avancee": 1,
        "gain_rouge": 0,
        "mod_seuil": -1,
        "est_siege_profil": false
      },
      {
        "id": "T4",
        "nom": "Sur place +",
        "cibles": [
          "SUR_PLACE"
        ],
        "avancee": 0,
        "gain_rouge": 1,
        "mod_seuil": -1,
        "est_siege_profil": true
      },
      {
        "id": "T5",
        "nom": "Devant +",
        "cibles": [
          "DEVANT"
        ],
        "avancee": 0,
        "gain_rouge": 1,
        "mod_seuil": -1,
        "est_siege_profil": false
      },
      {
        "id": "T6",
        "nom": "En avançant +",
        "cibles": [
          "SUR_PLACE",
          "DEVANT"
        ],
        "avancee": 1,
        "gain_rouge": 1,
        "mod_seuil": -2,
        "est_siege_profil": false
      }
    ],
    "machine_damage_rules": {
      "ABATTEUSE": {
        "arbres_coupes_max": 2,
        "souches_retirees": 0,
        "arrache_1_souche_si_sans_arbre_en_siege_option": "ARRACHE_1_SOUCHE_SI_SANS_ARBRE"
      },
      "BULLDOZER": {
        "arbres_coupes_max": 1,
        "retire_toutes_souches_non_protegees": true,
        "test_parade_unique": true
      },
      "siege_t4": {
        "autonomie_attaque_si_t4_ejectee": true,
        "apprentissage_sur_t4_si_presente": true
      }
    },
    "machine_deck_rules": {
      "cartes_machine_par_rayon": 2,
      "types_par_rayon": [
        "ABATTEUSE",
        "BULLDOZER"
      ],
      "total_initial_formula": "2 * N",
      "sabotage_dilution_permanente": true,
      "sabotage_effet_propre": null,
      "sabotage_perd_activation_et_pas_de_des": true,
      "remelange_etape": "6.3",
      "penurie_ordre": "sens_horaire_depuis_plus_arbres_debout"
    },
    "spec_formelle": {
      "schema_version": "5.3.1-audit",
      "etapes_1_a_6": {
        "etape_1_PREPARATION_POSE_FURTIVITE": "Distribution, Dés secrets et Pose des Défenseurs : Lecture épurée des dés sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Si le rang M porte un Rêve en 3.2, la machine est annulée et le Rêve s’ouvre. Communication muette : silence tactique sous paravent fermé ; simple visibilité publique sans concertation orale sous l'Ara.",
        "etape_2_REVELATION_DES_REVES_FURTIVITE": "Ouverture des Paravents, Rêves, Dés et Furtivité : Rêve sur dé Machine : annule l'activation de la machine et peut ouvrir ce Rêve (max 1 ouverture par Rêve et par tour).",
        "etape_3_CONSTRUCTION_SYNERGIES": "Construction obligatoire des Tuiles de Synergie : Gouvernance unitaire : chaque tuile de Synergie et piste de Migration est décidée uniquement par son Peuple d'origine. Insertion d'un Rêve : éjecte la Tactique la plus à droite ; seules les tuiles à droite du trou glissent à gauche ; pose en case 6 ; Bugs fixes sur les cases. Anti-blocage et Nids : pose interdite sur case morte/tuile inconstructible ; 1 seul Nid par parcelle sans machine ; choix du bâtisseur libéré par Peuple d'origine.",
        "etape_4_NIDS_ET_MIGRATION": "Production des Nids et Migration des Insectes : Production des Nids : bloc indivisible (création selon état réel présent + pouvoir du Nid avant Gardiens) ; Miel des Ancêtres restreint aux jetons Insecte. Migration des Insectes : 0 ou 1 cran facultatif (suivi par retournement des pions) ; aller simple définitif et sans limite vers les pistes globales.",
        "etape_5_ATTAQUES_ET_TEST_FIN": "Attaques des Machines et Vérification de Fin de Partie : Séquence des attaques : Tactiques 1..6 puis Sièges ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant. Cibles dynamiques : lues selon la position physique réelle de la machine à l’instant où elle attaque. Pont routier : Routes Forestières systématiquement sautées le long d'un rayon, mais infranchissables/inoccupables latéralement. Repli sur création de Route : recul automatique vers la bordure par défaut, vers le cœur seulement si bord tout rasé, retrait si rayon tout rasé ; Siège irréversible maintenu. Contact Machine-Nid : tout mouvement entrant (avancée, recul, repli) renvoie le Nid reconstructible en lisière et défausse tous les Insectes de la parcelle.",
        "etape_6_APPRENTISSAGE_ET_MENAGE": "Apprentissage du Contremaître et Ménage de fin de tour : Cascades de Gardiens : fin complète de l'effet en cours, marquage immédiat à l'ouverture, balayage à plat de 1 à 6 sans pile imbriquée. Faces 2 et Lois passives : seule la face visible s'applique (Faces 2 autonomes) ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume."
      },
      "furtivite": "Furtivité à 4 emplacements (2 jumeaux/rive) : entrer sur la case tire l'autre jeton sur le jumeau et oriente l'action unique ; retourner en choix définitif se fait sur place sans déplacement.",
      "chaine_parades_et_pieges": "Matamata et chaîne des parades : Matamata vérifie la présence d'une Souche à chaque frappe ; ordre Jaguar -> Harpie -> Piège -> Parade classique. | Armement des Pièges : Embuscade dès que Défense totale >= 1 (locale ou à distance) ; tout Piège ayant paré >= 1 fois dans le tour est retiré en fin d'attaques. | Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; suppression totale des Insectes engagés. | Zéro verrouillage des parcelles ciblées : Insectes toujours libres tant que présents ; seul un Piège déjà déclenché ce tour-ci ne peut plus payer de coût volontaire.",
      "sabotage_par_dilution": "Cartes Sabotage (dilution permanente) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis ajoute définitivement 1 carte Sabotage au paquet Machine (allume 3. Sabotage) ; 1 carte Sabotage tirée à l’Étape 1 fait perdre 1 activation au Contremaître puis est remélangée en fin de tour.",
      "apprentissage": "Apprentissage : dommage réel requis (>= 1 Arbre coupé ou Souche retirée) ; retraits volontaires avant Bugs ; remise à zéro intégrale en fin d'étape. | Autonomie et Apprentissage du Siège : l’attaque d’une machine en Siège reste active même si la tuile T4 est éjectée ; en 6.1, une machine en Siège génère normalement ses jetons d’Apprentissage sur T4 tant que T4 figure sur la Piste des Tactiques (ignorés si T4 est éjectée).",
      "fins_5_3": "Seuil de Réveil fixe : calculé à la mise en place (inactif si < 3 Gardiens en jeu) ; retour en lisière efface le marqueur. | Test de fin de partie : maintenu en fin d'attaques (saut Apprentissage), avec déclenchement en fin d'Apprentissage si L'Écho des Voix Célestes amène son Rêve en case 1."
    }
  },
  "tested_tiles_rules": [],
  "cloud_run_job": {
    "job_name": "amazonia-palier1",
    "region": "europe-west9",
    "image": "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest",
    "tasks": 10,
    "cpu_per_task": 2,
    "memory_per_task": "1Gi",
    "job_wall_sec_including_scheduling": 36.239,
    "max_worker_compute_sec": 18.567,
    "mean_worker_compute_sec": 17.179,
    "sum_worker_games_per_sec": 5866.3,
    "effective_cluster_compute_games_per_sec": 5385.8,
    "end_to_end_job_games_per_sec": 2759.5
  },
  "totals": {
    "total_games": 100000,
    "n_shards": 10,
    "n_cells": 180,
    "parquet_archive": ".tmp_runs/palier1_baseline/palier1_b0_cells.parquet"
  },
  "by_mode": [
    {
      "mode": 1,
      "n_games": 50000,
      "mean_score_arbres": 24.764,
      "mean_ratio_arbres": 0.4866,
      "mean_tours": 8.0,
      "count_tour_8": 50000,
      "count_reve_rang_1": 0,
      "count_reveil_gardiens": 0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 2,
      "n_games": 50000,
      "mean_score_arbres": 34.398,
      "mean_ratio_arbres": 0.6583,
      "mean_tours": 6.219,
      "count_tour_8": 17885,
      "count_reve_rang_1": 28845,
      "count_reveil_gardiens": 3270,
      "pct_tour_8": 35.77,
      "pct_reve_rang_1": 57.69,
      "pct_reveil_gardiens": 6.54
    }
  ],
  "by_mode_and_n_players": [
    {
      "mode": 1,
      "n_players": 3,
      "n_games": 12500,
      "mean_score_arbres": 16.723,
      "mean_ratio_arbres": 0.4924,
      "mean_p20_ratio": 0.3945,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "n_players": 4,
      "n_games": 12500,
      "mean_score_arbres": 21.99,
      "mean_ratio_arbres": 0.4852,
      "mean_p20_ratio": 0.3973,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "n_players": 5,
      "n_games": 12500,
      "mean_score_arbres": 27.487,
      "mean_ratio_arbres": 0.4852,
      "mean_p20_ratio": 0.406,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "n_players": 6,
      "n_games": 12500,
      "mean_score_arbres": 32.858,
      "mean_ratio_arbres": 0.4836,
      "mean_p20_ratio": 0.411,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 2,
      "n_players": 3,
      "n_games": 12500,
      "mean_score_arbres": 18.651,
      "mean_ratio_arbres": 0.5504,
      "mean_p20_ratio": 0.4352,
      "mean_tours": 7.576,
      "pct_tour_8": 75.98,
      "pct_reve_rang_1": 23.98,
      "pct_reveil_gardiens": 0.04
    },
    {
      "mode": 2,
      "n_players": 4,
      "n_games": 12500,
      "mean_score_arbres": 28.589,
      "mean_ratio_arbres": 0.6342,
      "mean_p20_ratio": 0.5172,
      "mean_tours": 6.664,
      "pct_tour_8": 39.14,
      "pct_reve_rang_1": 53.95,
      "pct_reveil_gardiens": 6.9
    },
    {
      "mode": 2,
      "n_players": 5,
      "n_games": 12500,
      "mean_score_arbres": 37.059,
      "mean_ratio_arbres": 0.6578,
      "mean_p20_ratio": 0.5533,
      "mean_tours": 6.15,
      "pct_tour_8": 25.08,
      "pct_reve_rang_1": 61.24,
      "pct_reveil_gardiens": 13.68
    },
    {
      "mode": 2,
      "n_players": 6,
      "n_games": 12500,
      "mean_score_arbres": 53.294,
      "mean_ratio_arbres": 0.7909,
      "mean_p20_ratio": 0.7326,
      "mean_tours": 4.488,
      "pct_tour_8": 2.88,
      "pct_reve_rang_1": 91.58,
      "pct_reveil_gardiens": 5.54
    }
  ],
  "by_mode_and_chassis": [
    {
      "mode": 1,
      "chassis_id": 0,
      "p_max": 4,
      "n_games": 10000,
      "mean_score_arbres": 23.922,
      "mean_ratio_arbres": 0.5324,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "chassis_id": 1,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 36.639,
      "mean_ratio_arbres": 0.6792,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "chassis_id": 4,
      "p_max": 4,
      "n_games": 10000,
      "mean_score_arbres": 12.883,
      "mean_ratio_arbres": 0.2872,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "chassis_id": 5,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 26.908,
      "mean_ratio_arbres": 0.4989,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 1,
      "chassis_id": 127,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 23.47,
      "mean_ratio_arbres": 0.4352,
      "mean_tours": 8.0,
      "pct_tour_8": 100.0,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.0
    },
    {
      "mode": 2,
      "chassis_id": 0,
      "p_max": 4,
      "n_games": 10000,
      "mean_score_arbres": 32.162,
      "mean_ratio_arbres": 0.6959,
      "mean_tours": 6.211,
      "pct_tour_8": 34.62,
      "pct_reve_rang_1": 57.28,
      "pct_reveil_gardiens": 8.1
    },
    {
      "mode": 2,
      "chassis_id": 1,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 42.552,
      "mean_ratio_arbres": 0.7759,
      "mean_tours": 6.212,
      "pct_tour_8": 33.97,
      "pct_reve_rang_1": 56.85,
      "pct_reveil_gardiens": 9.18
    },
    {
      "mode": 2,
      "chassis_id": 4,
      "p_max": 4,
      "n_games": 10000,
      "mean_score_arbres": 24.581,
      "mean_ratio_arbres": 0.5178,
      "mean_tours": 6.479,
      "pct_tour_8": 41.37,
      "pct_reve_rang_1": 53.78,
      "pct_reveil_gardiens": 4.85
    },
    {
      "mode": 2,
      "chassis_id": 5,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 36.304,
      "mean_ratio_arbres": 0.6531,
      "mean_tours": 6.408,
      "pct_tour_8": 37.72,
      "pct_reve_rang_1": 55.64,
      "pct_reveil_gardiens": 6.64
    },
    {
      "mode": 2,
      "chassis_id": 127,
      "p_max": 5,
      "n_games": 10000,
      "mean_score_arbres": 36.393,
      "mean_ratio_arbres": 0.649,
      "mean_tours": 5.787,
      "pct_tour_8": 31.17,
      "pct_reve_rang_1": 64.9,
      "pct_reveil_gardiens": 3.93
    }
  ],
  "mode2_tables": [
    {
      "n_players": 3,
      "table_id": "H-E-I",
      "mirror_pair_id": "H-E-I-I-E-H",
      "n_games": 2080,
      "mean_ratio_arbres": 0.6617,
      "pct_reve_rang_1": 56.92,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 3,
      "table_id": "I-E-H",
      "mirror_pair_id": "H-E-I-I-E-H",
      "n_games": 2080,
      "mean_ratio_arbres": 0.6693,
      "pct_reve_rang_1": 58.27,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 3,
      "table_id": "I-E-M",
      "mirror_pair_id": "I-E-M-M-E-I",
      "n_games": 2085,
      "mean_ratio_arbres": 0.5312,
      "pct_reve_rang_1": 14.05,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 3,
      "table_id": "M-E-I",
      "mirror_pair_id": "I-E-M-M-E-I",
      "n_games": 2085,
      "mean_ratio_arbres": 0.5355,
      "pct_reve_rang_1": 14.82,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 3,
      "table_id": "M-R-O",
      "mirror_pair_id": "M-R-O-O-R-M",
      "n_games": 2085,
      "mean_ratio_arbres": 0.4511,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.14
    },
    {
      "n_players": 3,
      "table_id": "O-R-M",
      "mirror_pair_id": "M-R-O-O-R-M",
      "n_games": 2085,
      "mean_ratio_arbres": 0.4541,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 0.1
    },
    {
      "n_players": 4,
      "table_id": "E-H-O-M",
      "mirror_pair_id": "E-H-O-M-M-O-H-E",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7227,
      "pct_reve_rang_1": 81.98,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 4,
      "table_id": "I-H-R-M",
      "mirror_pair_id": "I-H-R-M-M-R-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.5424,
      "pct_reve_rang_1": 24.77,
      "pct_reveil_gardiens": 14.08
    },
    {
      "n_players": 4,
      "table_id": "M-O-H-E",
      "mirror_pair_id": "E-H-O-M-M-O-H-E",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7203,
      "pct_reve_rang_1": 81.15,
      "pct_reveil_gardiens": 0.0
    },
    {
      "n_players": 4,
      "table_id": "M-R-H-I",
      "mirror_pair_id": "I-H-R-M-M-R-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.5515,
      "pct_reve_rang_1": 27.9,
      "pct_reveil_gardiens": 13.54
    },
    {
      "n_players": 5,
      "table_id": "I-H-E-O-M",
      "mirror_pair_id": "I-H-E-O-M-M-O-E-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7395,
      "pct_reve_rang_1": 82.85,
      "pct_reveil_gardiens": 8.74
    },
    {
      "n_players": 5,
      "table_id": "I-H-O-R-M",
      "mirror_pair_id": "I-H-O-R-M-M-R-O-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.5676,
      "pct_reve_rang_1": 37.02,
      "pct_reveil_gardiens": 19.55
    },
    {
      "n_players": 5,
      "table_id": "M-O-E-H-I",
      "mirror_pair_id": "I-H-E-O-M-M-O-E-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7528,
      "pct_reve_rang_1": 85.57,
      "pct_reveil_gardiens": 7.52
    },
    {
      "n_players": 5,
      "table_id": "M-R-O-H-I",
      "mirror_pair_id": "I-H-O-R-M-M-R-O-H-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.5713,
      "pct_reve_rang_1": 39.52,
      "pct_reveil_gardiens": 18.91
    },
    {
      "n_players": 6,
      "table_id": "E-R-I-O-H-M",
      "mirror_pair_id": "E-R-I-O-H-M-M-H-O-I-R-E",
      "n_games": 3125,
      "mean_ratio_arbres": 0.8115,
      "pct_reve_rang_1": 94.56,
      "pct_reveil_gardiens": 3.01
    },
    {
      "n_players": 6,
      "table_id": "I-E-H-O-R-M",
      "mirror_pair_id": "I-E-H-O-R-M-M-R-O-H-E-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7688,
      "pct_reve_rang_1": 88.06,
      "pct_reveil_gardiens": 7.94
    },
    {
      "n_players": 6,
      "table_id": "M-H-O-I-R-E",
      "mirror_pair_id": "E-R-I-O-H-M-M-H-O-I-R-E",
      "n_games": 3125,
      "mean_ratio_arbres": 0.8124,
      "pct_reve_rang_1": 95.01,
      "pct_reveil_gardiens": 3.23
    },
    {
      "n_players": 6,
      "table_id": "M-R-O-H-E-I",
      "mirror_pair_id": "I-E-H-O-R-M-M-R-O-H-E-I",
      "n_games": 3125,
      "mean_ratio_arbres": 0.7709,
      "pct_reve_rang_1": 88.7,
      "pct_reveil_gardiens": 7.97
    }
  ],
  "worker_shards": [
    {
      "task_index": 0,
      "games": 10000,
      "compute_sec": 18.4792,
      "games_per_sec": 541.15
    },
    {
      "task_index": 1,
      "games": 10000,
      "compute_sec": 18.294,
      "games_per_sec": 546.63
    },
    {
      "task_index": 2,
      "games": 10000,
      "compute_sec": 15.27,
      "games_per_sec": 654.88
    },
    {
      "task_index": 3,
      "games": 10000,
      "compute_sec": 17.0608,
      "games_per_sec": 586.14
    },
    {
      "task_index": 4,
      "games": 10000,
      "compute_sec": 17.9435,
      "games_per_sec": 557.31
    },
    {
      "task_index": 5,
      "games": 10000,
      "compute_sec": 17.6396,
      "games_per_sec": 566.91
    },
    {
      "task_index": 6,
      "games": 10000,
      "compute_sec": 18.5675,
      "games_per_sec": 538.57
    },
    {
      "task_index": 7,
      "games": 10000,
      "compute_sec": 17.5187,
      "games_per_sec": 570.82
    },
    {
      "task_index": 8,
      "games": 10000,
      "compute_sec": 17.1275,
      "games_per_sec": 583.86
    },
    {
      "task_index": 9,
      "games": 10000,
      "compute_sec": 13.8887,
      "games_per_sec": 720.01
    }
  ]
}
```
