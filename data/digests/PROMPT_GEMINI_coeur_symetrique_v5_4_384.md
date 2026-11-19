Dossier de simulation Amazonia : Dernier Rempart — utilise les règles cœur et statistiques ci-dessous comme unique vérité terrain.

```json
{
  "campaign": "coeur_symetrique_v5_4_384",
  "generated_at_utc": "2026-11-19T10:40:45Z",
  "active_core_rules": {
    "version": "5.4.0",
    "source_studio_version": "v5.4",
    "spec_bundle_sha256": "67f5a57f0eacfb3a486cba41581da3eb12e4209f250cf742d2f472a209366599",
    "studio_sha256": {
      "catalog_v5_4.json": "0cad73f652b4769ddcb1618cc7074c61f0b68ce953702cbafd8d5ae85d8bdd62",
      "spec_formelle_v5_4.json": "c9890256b635f6ab481ccdf1b357a04a256ecac91fbf5a59612f150114d332d2",
      "amazonia_data_v5_4.js": "35e3cfecfebe52ba806beeccfb9be491ff9e44e42b3ff6ab41ad2f98241551ef"
    },
    "chassis_7_axes": [
      {
        "chassis_id": 0,
        "studio_config_index_384": 1,
        "profil_piste": "P4_2233",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 1,
        "studio_config_index_384": 65,
        "profil_piste": "P4_2223",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 2,
        "studio_config_index_384": 129,
        "profil_piste": "P4_1223",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 3,
        "studio_config_index_384": 193,
        "profil_piste": "P5_22233",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 4,
        "studio_config_index_384": 257,
        "profil_piste": "P5_22223",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 5,
        "studio_config_index_384": 321,
        "profil_piste": "P5_12223",
        "regle_ouverture_reve_multiple": "UNIQUE_PAR_TOUR",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 6,
        "studio_config_index_384": 33,
        "profil_piste": "P4_2233",
        "regle_ouverture_reve_multiple": "PAR_DE_M_DESIGNE",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
      },
      {
        "chassis_id": 7,
        "studio_config_index_384": 97,
        "profil_piste": "P4_2223",
        "regle_ouverture_reve_multiple": "PAR_DE_M_DESIGNE",
        "offset_seuil_parade": 0,
        "mise_en_place_tactiques": "ORDRE_FIXE_T1_T6",
        "placement_initial_machines": "MEME_PARCELLE_P1",
        "role_abatteuse_fin_de_piste": "STANDARD_COUPE_ARBRE",
        "synergie_binome_machines": "INDIVIDUELLE"
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
        "est_ratissage_profil": true
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
        "est_ratissage_profil": false
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
        "est_ratissage_profil": false
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
        "est_ratissage_profil": false
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
        "est_ratissage_profil": false
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
        "est_ratissage_profil": false
      }
    ],
    "machine_damage_rules": {
      "ABATTEUSE": {
        "arbres_coupes_max": 2,
        "souches_retirees": 0,
        "arrache_1_souche_si_sans_arbre_en_ratissage_option": "ARRACHE_1_SOUCHE_SI_SANS_ARBRE"
      },
      "BULLDOZER": {
        "arbres_coupes_max": 1,
        "retire_toutes_souches_non_protegees": true,
        "test_parade_unique": true
      },
      "ratissage": {
        "pion_double_face": true,
        "bonus_puissance_imprime": 1,
        "traite_comme_jeton_rouge_a_tous_egards": true,
        "conserve_jetons_puissance_anterieurs": true,
        "tactique_imprimee": "T1",
        "autonomie_attaque_si_t1_ejectee": true,
        "apprentissage_sur_t1_si_presente": true,
        "entree_definitive_derniere_parcelle": true
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
      "schema_version": "5.4.0",
      "etapes_1_a_6": {
        "etape_1_PREPARATION_ET_DES_SECRETS": "Ratissage, Distribution et Dés secrets (1.1–1.3) : Lecture épurée des dés sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Si le rang M porte un Rêve en 3.2, la machine est annulée et le Rêve s’ouvre. Communication muette : silence tactique sous paravent fermé ; simple visibilité publique sans concertation orale sous l'Ara.",
        "etape_2_POSE_DES_DEFENSEURS": "Pose des Défenseurs et Piste de Furtivité (2.1–2.2) : Furtivité à 4 emplacements (2 jumeaux/rive) : entrer sur la case tire l'autre jeton sur le jumeau et oriente l'action unique ; retourner en choix définitif se fait sur place sans déplacement.",
        "etape_3_CONSTRUCTION_ET_REVELATION": "Construction obligatoire (3.1), Ouverture des Paravents et Rêves (3.2) : Gouvernance unitaire : chaque tuile de Synergie et piste de Migration est décidée uniquement par son Peuple d'origine. Insertion d'un Rêve : éjecte la Tactique la plus à droite ; seules les tuiles à droite du trou glissent à gauche ; pose en case 6 ; Bugs fixes sur les cases. Anti-blocage et Nids : pose interdite sur case morte/tuile inconstructible ; 1 seul Nid par parcelle sans machine ; choix du bâtisseur libéré par Peuple d'origine. Rêve sur dé Machine : annule l'activation de la machine et peut ouvrir ce Rêve (max 1 ouverture par Rêve et par tour).",
        "etape_4_FURTIVITE_NIDS_ET_MIGRATION": "Furtivité (4.1), Production des Nids (4.2) et Migration des Insectes (4.3) : Cartes Sabotage (dilution permanente) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis ajoute définitivement 1 carte Sabotage au paquet Machine (allume 3. Sabotage) ; 1 carte Sabotage tirée à l’Étape 1 fait perdre 1 activation au Contremaître puis est remélangée en fin de tour. Production des Nids : bloc indivisible (création selon état réel présent + pouvoir du Nid avant Gardiens) ; Miel des Ancêtres restreint aux jetons Insecte. Migration des Insectes : 0 ou 1 cran facultatif (suivi par retournement des pions) ; aller simple définitif et sans limite vers les pistes globales.",
        "etape_5_ATTAQUES_ET_TEST_FIN": "Attaques des Machines et Vérification de Fin de Partie (5.1–5.3) : Séquence des attaques : Tactiques 1..6 puis Ratissages ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant. Cibles dynamiques : lues selon la position physique réelle de la machine à l’instant où elle attaque. Pont routier : Routes Forestières systématiquement sautées le long d'un rayon, mais infranchissables/inoccupables latéralement. Repli sur création de Route : recul automatique vers la bordure par défaut, vers le cœur seulement si bord tout rasé, retrait si rayon tout rasé ; Ratissage irréversible maintenu. Contact Machine-Nid : tout mouvement entrant (avancée, recul, repli) renvoie le Nid reconstructible en lisière et défausse tous les Insectes de la parcelle.",
        "etape_6_APPRENTISSAGE_ET_MENAGE": "Apprentissage du Contremaître et Ménage de fin de tour (6.1–6.3) : Cascades de Gardiens : fin complète de l'effet en cours, marquage immédiat à l'ouverture, balayage à plat de 1 à 6 sans pile imbriquée. Faces 2 et Lois passives : seule la face visible s'applique (Faces 2 autonomes) ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume."
      },
      "furtivite": "Furtivité à 4 emplacements (2 jumeaux/rive) : entrer sur la case tire l'autre jeton sur le jumeau et oriente l'action unique ; retourner en choix définitif se fait sur place sans déplacement.",
      "chaine_parades_et_pieges": "Matamata et chaîne des parades : Matamata vérifie la présence d'une Souche à chaque frappe ; ordre Jaguar -> Harpie -> Piège -> Parade classique. | Armement des Pièges : Embuscade dès que Défense totale >= 1 (locale ou à distance) ; tout Piège ayant paré >= 1 fois dans le tour est retiré en fin d'attaques. | Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; suppression totale des Insectes engagés. | Zéro verrouillage des parcelles ciblées : Insectes toujours libres tant que présents ; seul un Piège déjà déclenché ce tour-ci ne peut plus payer de coût volontaire.",
      "sabotage_par_dilution": "Cartes Sabotage (dilution permanente) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis ajoute définitivement 1 carte Sabotage au paquet Machine (allume 3. Sabotage) ; 1 carte Sabotage tirée à l’Étape 1 fait perdre 1 activation au Contremaître puis est remélangée en fin de tour.",
      "apprentissage": "Apprentissage : dommage réel requis (>= 1 Arbre coupé ou Souche retirée) ; retraits volontaires avant Bugs ; remise à zéro intégrale en fin d'étape. | Autonomie et Apprentissage du Ratissage : pion double face retourné définitivement sur la dernière parcelle non rasée ; +1 puissance imprimée (traité comme +1 rouge à tous égards, jetons rouges antérieurs conservés) et application systématique de T1 Sur place ; attaque autonome même si T1 est éjectée ; en 6.1, alimente T1 en Apprentissage tant que T1 figure sur la Piste des Tactiques.",
      "fins_5_3": "Seuil de Réveil fixe : calculé à la mise en place (inactif si < 3 Gardiens en jeu) ; retour en lisière efface le marqueur. | Test de fin de partie : maintenu en fin d’attaques (saut Apprentissage) sur Tour 8, Réveil Gardiens ou Sommeil (toutes les tuiles Rêves en jeu regroupées en bloc à gauche de la Piste des Tactiques), avec déclenchement en fin d’Apprentissage si L’Écho des Voix Célestes complète ce bloc."
    }
  },
  "tested_tiles_rules": [],
  "description": "Exploration complète du cœur symétrique v5.4 (Mode 2, tuiles neutres, 384 châssis, 3 à 6 joueurs)",
  "selection_manifest": {
    "base_bundle_id": "STANDARD_A",
    "n_resolved_slots": 32,
    "non_default_base_slots": {},
    "resolved_32_slots_sha256": "4050ff38326e49d77d95dfa8d13cbd6611db4766f8c9ed226f13d25e1f1f6fe7",
    "migration_policy": {
      "SLOT_BUG_CERVEAU": "A",
      "SLOT_COLONISATION_GARDIENS": "A",
      "fixed": true,
      "varying_slots": []
    }
  },
  "execution": {
    "backend": "cloudrun",
    "region": "europe-west9",
    "job_name": "amazonia-campaign",
    "image": "europe-west9-docker.pkg.dev/amazonia-sim/sim-workers/worker-pypy:latest",
    "tasks": 20,
    "job_wall_sec": 64.117,
    "max_worker_compute_sec": 45.52,
    "sum_worker_games_per_sec": 1968.1,
    "effective_cluster_games_per_sec": 1619.7,
    "run_id": "20261119T103931Z_d9c9fd6c",
    "gcs_prefix": "campaigns/coeur_symetrique_v5_4_384/20261119T103931Z_d9c9fd6c"
  },
  "totals": {
    "total_games": 73728,
    "n_shards": 20,
    "n_cells": 6912,
    "n_configurations": 1536,
    "mean_score_arbres": 32.452,
    "mean_ratio_arbres": 0.7012,
    "cvar20_ratio": 0.5533,
    "within_table_cvar20_ratio": 0.5533,
    "table_cvar20_ratio": 0.4909,
    "survival_rate": 0.9991,
    "mean_tours": 5.619,
    "pct_tour_8": 34.36,
    "pct_reve_rang_1": 0.43,
    "pct_reveil_gardiens": 65.21,
    "tested_tiles": [],
    "parquet_archive": ".tmp_runs/campaigns/coeur_symetrique_v5_4_384/20261119T103931Z_d9c9fd6c/cells.parquet"
  },
  "telemetry": {
    "mean_mem_debt": 0.0,
    "mean_active_laws": 0.0,
    "max_active_laws": 0,
    "mean_fiddliness_ops": 3.435,
    "mean_cascade_sweeps": 6.207,
    "mean_physical_ops": 416.688,
    "mean_player_decisions": 124.453
  },
  "by_mode": [
    {
      "mode": 2,
      "bot": "B2",
      "n_games": 73728,
      "mean_score_arbres": 32.452,
      "mean_ratio_arbres": 0.7012,
      "cvar20_ratio": 0.5533,
      "mean_tours": 5.619,
      "pct_tour_8": 34.36,
      "pct_reve_rang_1": 0.43,
      "pct_reveil_gardiens": 65.21,
      "table_cvar20_ratio": 0.4909
    }
  ],
  "by_n_players": [
    {
      "n_players": 3,
      "n_games": 18432,
      "mean_score_arbres": 18.751,
      "mean_ratio_arbres": 0.6188,
      "cvar20_ratio": 0.4692,
      "mean_tours": 6.727,
      "pct_tour_8": 66.71,
      "pct_reve_rang_1": 0.0,
      "pct_reveil_gardiens": 33.29,
      "table_cvar20_ratio": 0.3784
    },
    {
      "n_players": 4,
      "n_games": 18432,
      "mean_score_arbres": 27.87,
      "mean_ratio_arbres": 0.6913,
      "cvar20_ratio": 0.5401,
      "mean_tours": 6.48,
      "pct_tour_8": 51.45,
      "pct_reve_rang_1": 0.39,
      "pct_reveil_gardiens": 48.16,
      "table_cvar20_ratio": 0.5748
    },
    {
      "n_players": 5,
      "n_games": 18432,
      "mean_score_arbres": 35.254,
      "mean_ratio_arbres": 0.6999,
      "cvar20_ratio": 0.5395,
      "mean_tours": 5.053,
      "pct_tour_8": 11.59,
      "pct_reve_rang_1": 0.5,
      "pct_reveil_gardiens": 87.91,
      "table_cvar20_ratio": 0.5341
    },
    {
      "n_players": 6,
      "n_games": 18432,
      "mean_score_arbres": 47.932,
      "mean_ratio_arbres": 0.7947,
      "cvar20_ratio": 0.6645,
      "mean_tours": 4.215,
      "pct_tour_8": 7.68,
      "pct_reve_rang_1": 0.84,
      "pct_reveil_gardiens": 91.48,
      "table_cvar20_ratio": 0.6812
    }
  ],
  "by_chassis": [
    {
      "chassis_id": 11,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 37.13,
      "mean_ratio_arbres": 0.8205,
      "cvar20_ratio": 0.7368,
      "mean_tours": 6.714,
      "studio_config_index_384": 353,
      "table_cvar20_ratio": 0.7438
    },
    {
      "chassis_id": 107,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 37.13,
      "mean_ratio_arbres": 0.8205,
      "cvar20_ratio": 0.7368,
      "mean_tours": 6.714,
      "studio_config_index_384": 355,
      "table_cvar20_ratio": 0.7438
    },
    {
      "chassis_id": 5,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 37.031,
      "mean_ratio_arbres": 0.8186,
      "cvar20_ratio": 0.735,
      "mean_tours": 6.724,
      "studio_config_index_384": 321,
      "table_cvar20_ratio": 0.7406
    },
    {
      "chassis_id": 101,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 37.031,
      "mean_ratio_arbres": 0.8186,
      "cvar20_ratio": 0.735,
      "mean_tours": 6.724,
      "studio_config_index_384": 323,
      "table_cvar20_ratio": 0.7406
    },
    {
      "chassis_id": 203,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 36.922,
      "mean_ratio_arbres": 0.8142,
      "cvar20_ratio": 0.7248,
      "mean_tours": 6.333,
      "studio_config_index_384": 354,
      "table_cvar20_ratio": 0.7371
    },
    {
      "chassis_id": 299,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 36.922,
      "mean_ratio_arbres": 0.8142,
      "cvar20_ratio": 0.7248,
      "mean_tours": 6.333,
      "studio_config_index_384": 356,
      "table_cvar20_ratio": 0.7371
    },
    {
      "chassis_id": 197,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 36.896,
      "mean_ratio_arbres": 0.8139,
      "cvar20_ratio": 0.7232,
      "mean_tours": 6.37,
      "studio_config_index_384": 322,
      "table_cvar20_ratio": 0.7396
    },
    {
      "chassis_id": 293,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 36.896,
      "mean_ratio_arbres": 0.8139,
      "cvar20_ratio": 0.7232,
      "mean_tours": 6.37,
      "studio_config_index_384": 324,
      "table_cvar20_ratio": 0.7396
    },
    {
      "chassis_id": 9,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.297,
      "mean_ratio_arbres": 0.812,
      "cvar20_ratio": 0.7447,
      "mean_tours": 5.62,
      "studio_config_index_384": 225,
      "table_cvar20_ratio": 0.7257
    },
    {
      "chassis_id": 105,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.297,
      "mean_ratio_arbres": 0.812,
      "cvar20_ratio": 0.7447,
      "mean_tours": 5.62,
      "studio_config_index_384": 227,
      "table_cvar20_ratio": 0.7257
    },
    {
      "chassis_id": 201,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.24,
      "mean_ratio_arbres": 0.8104,
      "cvar20_ratio": 0.7443,
      "mean_tours": 5.542,
      "studio_config_index_384": 226,
      "table_cvar20_ratio": 0.7144
    },
    {
      "chassis_id": 297,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.24,
      "mean_ratio_arbres": 0.8104,
      "cvar20_ratio": 0.7443,
      "mean_tours": 5.542,
      "studio_config_index_384": 228,
      "table_cvar20_ratio": 0.7144
    },
    {
      "chassis_id": 3,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.063,
      "mean_ratio_arbres": 0.808,
      "cvar20_ratio": 0.74,
      "mean_tours": 5.672,
      "studio_config_index_384": 193,
      "table_cvar20_ratio": 0.7235
    },
    {
      "chassis_id": 99,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.063,
      "mean_ratio_arbres": 0.808,
      "cvar20_ratio": 0.74,
      "mean_tours": 5.672,
      "studio_config_index_384": 195,
      "table_cvar20_ratio": 0.7235
    },
    {
      "chassis_id": 195,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.026,
      "mean_ratio_arbres": 0.8068,
      "cvar20_ratio": 0.7396,
      "mean_tours": 5.589,
      "studio_config_index_384": 194,
      "table_cvar20_ratio": 0.7153
    },
    {
      "chassis_id": 291,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 44.026,
      "mean_ratio_arbres": 0.8068,
      "cvar20_ratio": 0.7396,
      "mean_tours": 5.589,
      "studio_config_index_384": 196,
      "table_cvar20_ratio": 0.7153
    },
    {
      "chassis_id": 10,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.87,
      "mean_ratio_arbres": 0.7965,
      "cvar20_ratio": 0.7232,
      "mean_tours": 5.63,
      "studio_config_index_384": 289,
      "table_cvar20_ratio": 0.7031
    },
    {
      "chassis_id": 106,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.87,
      "mean_ratio_arbres": 0.7965,
      "cvar20_ratio": 0.7232,
      "mean_tours": 5.63,
      "studio_config_index_384": 291,
      "table_cvar20_ratio": 0.7031
    },
    {
      "chassis_id": 202,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.776,
      "mean_ratio_arbres": 0.7936,
      "cvar20_ratio": 0.7196,
      "mean_tours": 5.563,
      "studio_config_index_384": 290,
      "table_cvar20_ratio": 0.6875
    },
    {
      "chassis_id": 298,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.776,
      "mean_ratio_arbres": 0.7936,
      "cvar20_ratio": 0.7196,
      "mean_tours": 5.563,
      "studio_config_index_384": 292,
      "table_cvar20_ratio": 0.6875
    },
    {
      "chassis_id": 4,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.661,
      "mean_ratio_arbres": 0.7927,
      "cvar20_ratio": 0.7187,
      "mean_tours": 5.682,
      "studio_config_index_384": 257,
      "table_cvar20_ratio": 0.6984
    },
    {
      "chassis_id": 100,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.661,
      "mean_ratio_arbres": 0.7927,
      "cvar20_ratio": 0.7187,
      "mean_tours": 5.682,
      "studio_config_index_384": 259,
      "table_cvar20_ratio": 0.6984
    },
    {
      "chassis_id": 196,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.589,
      "mean_ratio_arbres": 0.7903,
      "cvar20_ratio": 0.7143,
      "mean_tours": 5.609,
      "studio_config_index_384": 258,
      "table_cvar20_ratio": 0.6875
    },
    {
      "chassis_id": 292,
      "p_max": 5,
      "n_games": 192,
      "mean_score_arbres": 39.589,
      "mean_ratio_arbres": 0.7903,
      "cvar20_ratio": 0.7143,
      "mean_tours": 5.609,
      "studio_config_index_384": 260,
      "table_cvar20_ratio": 0.6875
    }
  ],
  "by_variant": [
    {
      "variant_id": "BASE",
      "n_games": 73728,
      "mean_score_arbres": 32.452,
      "mean_ratio_arbres": 0.7012,
      "cvar20_ratio": 0.5533,
      "mean_tours": 5.619,
      "pct_tour_8": 34.36,
      "pct_reve_rang_1": 0.43,
      "pct_reveil_gardiens": 65.21,
      "table_cvar20_ratio": 0.4909
    }
  ],
  "tile_metrics": {}
}
```
