// =========================================================================
// data/canon_v6_4_data.js — Généré automatiquement depuis contracts/*_v6_4.json (SSOT v6.4.0 · 30 tuiles Passe 2 affinées · 31 pictogrammes · Archive Passe 1 v6.3 incluse)
// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.
// =========================================================================
const SIX_VERBES_COEUR_V6_4 = {
  "REFROIDIR": {
    "verbe": "Refroidir",
    "definition": "Retourner 1 jeton Rouge existant d’une machine (mobile ou en Ratissage) sur sa face Bleu Surchauffe (−1 dans tous les modes ; jamais de Bleu posé à sec depuis la réserve)."
  },
  "ALTERER": {
    "verbe": "Altérer",
    "definition": "Poser 1 jeton d’Altération de la réserve Entités sur une machine mobile qui n’en porte pas encore (max 1 par machine ; jamais sur une machine en Ratissage)."
  },
  "RECULER": {
    "verbe": "Reculer",
    "definition": "Déplacer une machine mobile d’1 parcelle vers la bordure de son rayon en sautant les Routes Forestières (sans sortir du plateau ; sans effet sur une machine en Ratissage)."
  },
  "ETOUFFER": {
    "verbe": "Étouffer",
    "definition": "Neutraliser toute l’activation restante d’une machine à ce tour : incliner son jeton Machine mobile à 90° devant son rayon et retirer immédiatement son dé de la Réglette, ou tourner une machine en Ratissage à 90° sur place jusqu’au ménage. Annuler une machine via un Rêve revient à l’Étouffer. Le mot « cale » est 100 % exclusif au jeton glissé sous une machine mobile par Le Caïman noir."
  },
  "SEMER_AU_SAC": {
    "verbe": "Semer au sac",
    "definition": "Glisser 1 jeton disponible (Sabotage ordinaire ou Écaille) dans le sac opaque sans allumer d’icône."
  },
  "GLISSER_UN_REVE": {
    "verbe": "Glisser un Rêve",
    "definition": "Déplacer une tuile Rêve sur la Réglette 1–6 en emportant ses Défenseurs dans leur état actuel (debout si encore à résoudre, couchés si déjà résolu)."
  }
};

const RULES_CANON_V6_4 = {
  "meta": {
    "projet": "Amazonia : Dernier Rempart",
    "schema_version": "6.4.0",
    "date_consolidation": "2026-11-27",
    "statut": "SSOT_V6_4_ACTIVE",
    "kernel_sync_status": "SEALED_V6_4_ACTIVE_VERIFIED",
    "cadrage_source": "docs/cadrage_v6_4.md",
    "description": "Contrat formel typé unique (SSOT) de la cible consolidée v6.4 : 9 évolutions Cœur zéro-mémoire, 6 Verbes du Cœur, Asymétrie Hybride 3+3 épurée, Enracinement sur Rive Sabotage (Effet Sentinelle) et Canon de 30 tuiles affinées Passe 2."
  },
  "six_verbes_du_coeur": {
    "REFROIDIR": {
      "verbe": "Refroidir",
      "definition": "Retourner 1 jeton Rouge existant d’une machine (mobile ou en Ratissage) sur sa face Bleu Surchauffe (−1 dans tous les modes ; jamais de Bleu posé à sec depuis la réserve)."
    },
    "ALTERER": {
      "verbe": "Altérer",
      "definition": "Poser 1 jeton d’Altération de la réserve Entités sur une machine mobile qui n’en porte pas encore (max 1 par machine ; jamais sur une machine en Ratissage)."
    },
    "RECULER": {
      "verbe": "Reculer",
      "definition": "Déplacer une machine mobile d’1 parcelle vers la bordure de son rayon en sautant les Routes Forestières (sans sortir du plateau ; sans effet sur une machine en Ratissage)."
    },
    "ETOUFFER": {
      "verbe": "Étouffer",
      "definition": "Neutraliser toute l’activation restante d’une machine à ce tour : incliner son jeton Machine mobile à 90° devant son rayon et retirer immédiatement son dé de la Réglette, ou tourner une machine en Ratissage à 90° sur place jusqu’au ménage. Annuler une machine via un Rêve revient à l’Étouffer. Le mot « cale » est 100 % exclusif au jeton glissé sous une machine mobile par Le Caïman noir."
    },
    "SEMER_AU_SAC": {
      "verbe": "Semer au sac",
      "definition": "Glisser 1 jeton disponible (Sabotage ordinaire ou Écaille) dans le sac opaque sans allumer d’icône."
    },
    "GLISSER_UN_REVE": {
      "verbe": "Glisser un Rêve",
      "definition": "Déplacer une tuile Rêve sur la Réglette 1–6 en emportant ses Défenseurs dans leur état actuel (debout si encore à résoudre, couchés si déjà résolu)."
    }
  },
  "architecture_modulaire": {
    "principe": "1 Tronc commun court suivi de 3 modules activés uniquement si au moins un Peuple de la famille participe à la partie.",
    "tronc_commun": {
      "id": "tronc_commun",
      "titre": "Tronc commun (toujours actif)",
      "perimetre": "Forêt finie 10×N, sac opaque de jetons (avec Sabotage différé Refroidir/Reculer), 2 dés standards universels, Réglette fixe à bandelette d’Acte et fil d’ouverture imprimé, 2 Défenseurs recto-verso, Furtivité Chaud/Calme à Rive Sabotage unifiée avec Enracinement volontaire (Effet Sentinelle permanent), Pièges autonomes, attaques avec dé retiré, Ratissage physique, 6 Verbes du Cœur et score final."
    },
    "modules": {
      "module_gardiens_et_eveil": {
        "titre": "Module Gardiens & Éveil",
        "peuples_requis": [
          "M",
          "R",
          "O"
        ],
        "assises_actives": 196,
        "assises_total": 197,
        "assises_inactives": [
          [
            "H",
            "E",
            "I"
          ]
        ],
        "resume": "Lu uniquement si au moins un Peuple Animal Sauvage (M, R ou O) joue : Piste des Gardiens à 6 icônes directes (sans balayage), Résonance en 6e position déclenchée au dernier pari glissé lors d’une vraie activation, 2 encoches visibles par Gardien, paris 0/1/2 Défenseurs, passage Face 2 sur pari gagné et fin anticipée par Éveil cumulatif (≥ A + 1 Gardiens en piste en Face 2 et 0 pari perdu ce tour)."
      },
      "module_reves_et_sommeil": {
        "titre": "Module Rêves & Sommeil",
        "peuples_requis": [
          "H",
          "E"
        ],
        "famille_inactive": [
          "M",
          "R",
          "O",
          "I"
        ],
        "resume": "Lu uniquement si au moins un Peuple Onirique (H ou E) joue : pose de Rêves sur la Réglette depuis la droite, défense en 1er et 2e temps, annulation (Étouffement) choisie par le propriétaire du Rêve, Défenseurs couchés dès résolution, glissements avec Défenseurs solidaires et fin anticipée par Sommeil du Contremaître (impossible si un Rêve est enraciné, hors exception explicite)."
      },
      "module_essaim": {
        "titre": "Module Essaim",
        "peuples_requis": [
          "I"
        ],
        "assises_actives": 160,
        "assises_total": 197,
        "assises_inactives_count": 37,
        "regles_natives": {
          "deploiement_direct_production": {
            "nom": "Déploiement direct à la Production",
            "fenetre": "PRODUCTION",
            "texte": "Chaque Nid défendu produit +1 Insecte (0–1 présent) ou +2 Insectes (≥ 2 présents) sans allumer d’icône ; chaque Insecte ainsi créé est immédiatement posé au choix sur ce Nid, sur une parcelle adjacente de son rayon (en sautant les Routes), ou — si ce Nid occupe la dernière parcelle de son rayon — sur un rang 1–6 de la Réglette ou une icône de la Piste des Gardiens ; puis le pouvoir du Nid s’applique."
          },
          "amorcage_natif": {
            "nom": "Amorçage natif de l’Essaim",
            "fenetre": "PERMANENT",
            "texte": "Si un effet de tuile déplace ou prélève un Insecte en jeu alors qu’aucun Insecte n’est sur le plateau, prenez 1 Insecte dans la réserve de l’Essaim."
          },
          "demenagement_unifie_nid": {
            "nom": "Déménagement unifié d’un Nid",
            "fenetre": "PERMANENT",
            "texte": "Tout Nid déplacé par une tuile emporte simultanément tous ses Insectes, tous les Défenseurs de sa parcelle et toute éventuelle ponte glissée sous lui."
          },
          "deviation_reglette": {
            "nom": "Déviation de dé (±1)",
            "fenetre": "OUVERTURE",
            "texte": "À l’ouverture des paravents, défaussez 1 Insecte posé sur un rang de la Réglette pour décaler le dé d’une machine mobile de −1 ou +1 rang (entre 1 et 6), en allumant l’icône Insecte."
          },
          "bouclier_de_lisiere": {
            "nom": "Bouclier de lisière (facultatif)",
            "fenetre": "FIN_ATTAQUES",
            "gouverneur": "I",
            "facultatif": true,
            "texte": "En fin d’attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes choisit de défausser ou non 1 Insecte pour maintenir le Gardien en piste sur sa face actuelle (sa Face 2 est sauvée pour la suite, mais son pari reste perdu à ce tour)."
          }
        },
        "resume": "Lu uniquement si les Insectes (I) jouent : jetons Insectes exclusifs aux 10 tuiles des 5 lisières de I (laissés dans la boîte sans I, Production ignorée et icône Insecte inactive), Déploiement direct à la Production (+1/+2 vers le Nid, une parcelle adjacente ou les pistes centrales depuis la dernière parcelle), Amorçage natif en réserve, Déménagement unifié des Nids, Déviation ±1, Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d’un Insecte passager non dépensé."
      }
    }
  },
  "accessoires_3_plus_3": {
    "actifs_des_le_tour_1": {
      "H": {
        "materiel": "2 pions Chamanes recto-verso uniquement (1 Tambour et 1 Chant) + 2 Fiches d’archétype.",
        "binome": "Le choix du pion posé au 1er temps laisse automatiquement l’autre archétype en main pour le 2e temps (auto-vérifiant).",
        "fiche_tambour": "Au 1er temps de pose, le Tambour peut aussi être placé sur une parcelle de n’importe quel autre Peuple.",
        "fiche_chant": "À l’ouverture, si un Rêve portant le Chant Étouffe au moins une machine et qu’aucune machine n’y reste active, Glissez ce Rêve d’1 rang vers la gauche."
      },
      "M": {
        "materiel": "1 jeton Duel recto-verso (Défi ↔ Territoire tenu).",
        "regle": "Posé ou déplacé face Défi avec un Défenseur Mammifère en forêt (ajustable tant que le 2e pion est en Réflexion). Duel unifié : toute frappe sur sa parcelle qui est parée ou piégée par n’importe quel moyen (Défenseur de tout Peuple, Insectes, Piège ordinaire ou Croc) retourne aussitôt le Duel sur Territoire tenu (bloque l’avancée des machines de cette parcelle aux rangs 3 et 6). Seule une frappe ni parée ni piégée (ou la création d’une Route) le renvoie en réserve."
      },
      "O": {
        "materiel": "1 Perchoir de Vigie mobile orientable (Chaud à un bout, Calme à l’autre) et ses 2 dés standards 1–6.",
        "eclaireur_du_ciel": "Toujours servi en dernier à la pioche, l’Oiseau regarde jusqu’à 2 jetons du sac, en garde 1 si possible et pose l’autre face cachée sur son Perchoir de Vigie jusqu’au ménage.",
        "regard_libre": "Sous paravent fermé, s’il détient un jeton Machine, il choisit librement lequel de ses 2 dés standards il retient comme dé de machine (l’autre dé est son dé écarté).",
        "signal_du_perchoir": "Sous paravents fermés, il place ou ajuste ce Perchoir (même vide en cas de pénurie) au pied d’un rayon ou pointé vers un rang 1–6, le bout Chaud ou Calme orienté vers sa cible (figé avec son 2e Défenseur ; jeton caché remis au sac au ménage)."
      }
    },
    "progressifs_via_tuiles": {
      "E": {
        "materiel": "Jetons d’Altération en réserve des Entités.",
        "regle": "Altérer une machine : posez 1 jeton d’Altération sur une machine mobile qui n’en porte pas encore (max 1 par machine). À la prochaine ouverture où le jeton de cette machine est révélé (temps 1 du fil d’ouverture), retirez son jeton d’Altération : elle compte dans m(r), mais Recule d’1 parcelle et est Étouffée (dé retiré, ne frappe pas). Si la machine passe en Ratissage ou si son rayon est 100 % rasé, le jeton d’Altération retourne en réserve."
      },
      "R": {
        "materiel": "4 jetons Sabotage « Écaille » (même gabarit que les jetons du sac) et 1 jeton Piège spécial « Croc ».",
        "regle": "Révélée à l’ouverture, une Écaille allume l’icône Sabotage puis le joueur Reptile pose le Croc sur une parcelle ciblée (l’Écaille rejoint le sac au ménage). En attaque, le Croc pare 1 frappe (allume l’icône Piégeage) puis revient dans la réserve Reptile. Le mot « cale » est 100 % exclusif au jeton glissé sous une machine mobile par Le Caïman noir."
      },
      "I": {
        "materiel": "Jetons Insectes et 5 Nids sur les 10 tuiles des 5 lisières des Insectes (exclusifs aux parties avec I).",
        "regle": "Déploiement direct à la Production (+1 si 0–1 présent, +2 si ≥ 2 présents, sans icône : chaque Insecte créé est posé sur ce Nid, sur une parcelle adjacente de son rayon en sautant les Routes, ou — depuis la dernière parcelle — sur un rang 1–6 ou une icône Gardien), Amorçage natif en réserve si 0 Insecte en jeu, Déménagement unifié des Nids (emporte Insectes, Défenseurs et ponte), Déviation ±1 à l’ouverture, Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d’un Insecte passager non dépensé."
      }
    }
  },
  "enracinement_volontaire": {
    "fenetre": "MENAGE_AVANT_RETOUR_SAC",
    "max_tuiles_par_joueur_par_tour": 1,
    "emplacement": "sur une place libre de la Rive Sabotage du rayon du joueur (interdit si le rayon est 100 % Routes)",
    "effet_sentinelle_permanent": "Chaque tuile enracinée occupe en permanence 1 des 2 places de la Rive Sabotage de son rayon (1 tuile = 1 seul Défenseur actif requis ; 2 tuiles = 2/2 permanent à 0 Défenseur chaque tour où m(r) == 0). La Rive Piège exige toujours 2 Défenseurs.",
    "perte_pouvoir_hors_mention_enracine": true,
    "laisse_insectes_sur_place": true,
    "reve_enracine_rend_sommeil_impossible": true,
    "exception_sommeil_ouvert": [
      "R1"
    ],
    "fins_eligibles": [
      "TOUR_8",
      "SOMMEIL",
      "EVEIL"
    ],
    "choix_souches_final": "librement choisies parmi les parcelles survivantes de son rayon",
    "calibrage": {
      "face_unique_ou_face_1": 1,
      "face_2": 2
    },
    "texte": "Au ménage, avant de remettre les jetons dans le sac, chaque joueur peut enraciner au plus 1 tuile construite de son Peuple sur une place libre de la Rive Sabotage de son rayon (interdit si son rayon est 100 % Routes). La tuile quitte sa piste ou parcelle (en y laissant ses Insectes), perd son pouvoir actif (hors clause « Enraciné »), et un Rêve enraciné ferme le Sommeil (sauf mention contraire). Effet Sentinelle permanent : chaque tuile enracinée occupe en permanence 1 place de la Rive Sabotage (1 tuile = 1 seul Défenseur actif requis ; 2 tuiles = 2/2 permanent à 0 Défenseur quand m(r) = 0). Au décompte final (Tour 8, Sommeil ou Éveil), elle retourne 1 Souche survivante (Face 1 / unique) ou 2 Souches (Face 2) en Arbres debout, librement choisies parmi les parcelles survivantes de son rayon."
  },
  "supports_fixes": {
    "reglette_tactiques": {
      "rangs": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "fixe": true,
      "fil_ouverture_imprime": "1. Altérations → 2. Sabotages & Écailles → 3. Déviations (±1) → 4. Rêves défendus (gauche → droite)",
      "cases_reves_au_dessus": true,
      "bandelette_acte_reversible_dessous": true,
      "retournement_bandelette_debut_tour": 5,
      "lecture_des_tours_1_8": "MIN_SAUF_OISEAU_CHOIX_LIBRE",
      "acte_1_tours": [
        1,
        2,
        3,
        4
      ],
      "acte_1_face": "FACE_A",
      "acte_1_charge_cases": [
        1,
        2,
        3
      ],
      "acte_1_assaut_cases": [
        4,
        5,
        6
      ],
      "acte_2_tours": [
        5,
        6,
        7,
        8
      ],
      "acte_2_face": "FACE_B",
      "acte_2_assaut_cases": [
        1,
        2,
        3
      ],
      "acte_2_charge_cases": [
        4,
        5,
        6
      ],
      "charge_gain_mode": "FRAPPE_NON_PAREE",
      "mode_charge": "Seuls les jetons rouges sont ignorés au seuil ; les jetons bleus Surchauffe (−1) s’appliquent ; +1 jeton rouge max/activation dès qu’au moins 1 frappe sur parcelle réelle non-Route n’est ni parée ni piégée (hors attaque Devant dans le vide depuis la dernière parcelle).",
      "mode_assaut": "Tous les jetons Puissance (rouges +1 et bleus −1) comptent au seuil ; 0 jeton Puissance gagné.",
      "tactiques": [
        {
          "id": "T1",
          "nom": "Sur place (Rang 1)",
          "cibles": [
            "SUR_PLACE"
          ],
          "avancee": 0,
          "gain_rouge": 0,
          "mod_seuil": 0,
          "est_ratissage_profil": false,
          "mode_acte_1": "CHARGE",
          "mode_acte_2": "ASSAUT"
        },
        {
          "id": "T2",
          "nom": "Devant (Rang 2)",
          "cibles": [
            "DEVANT"
          ],
          "avancee": 0,
          "gain_rouge": 0,
          "mod_seuil": 0,
          "est_ratissage_profil": false,
          "mode_acte_1": "CHARGE",
          "mode_acte_2": "ASSAUT"
        },
        {
          "id": "T3",
          "nom": "En avançant (Rang 3)",
          "cibles": [
            "SUR_PLACE",
            "DEVANT"
          ],
          "avancee": 1,
          "gain_rouge": 0,
          "mod_seuil": -1,
          "est_ratissage_profil": false,
          "mode_acte_1": "CHARGE",
          "mode_acte_2": "ASSAUT"
        },
        {
          "id": "T4",
          "nom": "Sur place (Rang 4)",
          "cibles": [
            "SUR_PLACE"
          ],
          "avancee": 0,
          "gain_rouge": 0,
          "mod_seuil": 0,
          "est_ratissage_profil": false,
          "mode_acte_1": "ASSAUT",
          "mode_acte_2": "CHARGE"
        },
        {
          "id": "T5",
          "nom": "Devant (Rang 5)",
          "cibles": [
            "DEVANT"
          ],
          "avancee": 0,
          "gain_rouge": 0,
          "mod_seuil": 0,
          "est_ratissage_profil": false,
          "mode_acte_1": "ASSAUT",
          "mode_acte_2": "CHARGE"
        },
        {
          "id": "T6",
          "nom": "En avançant (Rang 6)",
          "cibles": [
            "SUR_PLACE",
            "DEVANT"
          ],
          "avancee": 1,
          "gain_rouge": 0,
          "mod_seuil": -1,
          "est_ratissage_profil": false,
          "mode_acte_1": "ASSAUT",
          "mode_acte_2": "CHARGE"
        }
      ]
    },
    "piste_gardiens": {
      "sans_numeros_visibles": true,
      "ordre_gauche_droite": [
        "PARADE",
        "PIEGEAGE",
        "SABOTAGE",
        "REVE",
        "INSECTE",
        "RESONANCE"
      ],
      "codes_internes": {
        "PARADE": 1,
        "PIEGEAGE": 2,
        "SABOTAGE": 3,
        "REVE": 4,
        "INSECTE": 5,
        "RESONANCE": 6
      },
      "resonance_position": 6,
      "balayage_supprime": true,
      "resonance_declencheur": "DERNIER_PARI_GLISSE_SUR_ACTIVATION_REELLE",
      "resonance_une_fois_par_vague_sans_boucle": true,
      "encoches_laterales_visibles": 2,
      "pari_max_defenseurs": 2,
      "eveil_cumulatif": {
        "tours_eligibles": [
          1,
          2,
          3,
          4,
          5,
          6,
          7
        ],
        "seuil_face_2_en_piste": "A + 1",
        "exemples_par_A": {
          "A=1": "2 Gardiens Face 2 en piste (sur 2)",
          "A=2": "3 Gardiens Face 2 en piste (sur 4)",
          "A=3": "4 Gardiens Face 2 en piste (sur 6)"
        },
        "zero_pari_perdu_ce_tour": true,
        "bouclier_lisiere_conserve_face2_mais_pari_reste_perdu": true
      },
      "verdict_fin_attaques": {
        "pari_perdu": "au moins 1 pion encore sur la tuile (retour en lisière Face 1, sauf Bouclier de lisière facultatif gouverné par I qui préserve la face pour la suite mais laisse le pari perdu à ce tour)",
        "pari_gagne": "0 pion sur la tuile et au moins 1 encoche occupée (reste en piste et passe Face 2)",
        "aucune_mise": "0 pion sur la tuile et 0 encoche occupée (reste en place sur sa face actuelle sans évoluer)"
      }
    }
  },
  "changelog_v6_4": {
    "version": "v6.4",
    "date": "2026-11-27",
    "titre": "Consolidation Cœur v6.4 (9 évolutions zéro-mémoire + 6 Verbes) & Passe 2 des 30 Tuiles",
    "resume": "Épuration matérielle et cognitive du Cœur sans altérer la profondeur tactique (Oiseau à 2 dés et Perchoir orientable unique, Duel unifié, Essaim à déploiement direct sans sous-étape radiale, Enracinement sur la Rive Sabotage avec Effet Sentinelle permanent, Sabotage différé Refroidir/Reculer, Piste des Gardiens directe avec Résonance au dernier pari, Éveil cumulatif A + 1 Face 2, fil d’ouverture imprimé et 6 Verbes du Cœur), accompagnée de la Passe 2 complète des 30 tuiles bi-composant.",
    "deltas": [
      {
        "domaine": "Oiseau épuré & Duel unifié (INV-07, INV-20)",
        "avant": "L’Oiseau manipulait un 3e dé dédié et deux pièces distinctes de vigie ; le Duel exigeait des clauses d’exception sur plusieurs tuiles pour basculer sur Territoire tenu.",
        "apres": "Tous les joueurs lancent uniquement 2 dés standards 1–6 (l’Oiseau choisit librement lequel retenir) ; pièce unique orientable Perchoir de Vigie (Chaud/Calme) ; Duel unifié retourné sur Territoire tenu par toute parade ou piège de n’importe quel moyen."
      },
      {
        "domaine": "Module Essaim fluide & Bonus 3J unifié (INV-19, INV-21)",
        "avant": "Sous-étape radiale dédiée avec retournement/redressement d’Insectes, amorçages répétés carte par carte et bonus 3 joueurs réservé aux Gardiens et Rêves.",
        "apres": "Déploiement direct à la Production (+1/+2 posés sur le Nid, une parcelle adjacente ou les pistes centrales depuis la dernière parcelle), Amorçage natif en réserve, Déménagement unifié des Nids et bonus 3 joueurs étendu aux Nids."
      },
      {
        "domaine": "Pied du rayon unifié & Sabotage différé (INV-05, INV-14, INV-22)",
        "avant": "Enracinements alignés face à une parcelle précise ; jeton Sabotage ordinaire sans effet immédiat sur le plateau.",
        "apres": "100 % des Enracinements posés sur la Rive Sabotage du rayon avec Effet Sentinelle permanent (1 ou 2 places occupées) et choix libre des Souches au décompte final ; Sabotage ordinaire révélé permet de Refroidir ou Reculer 1 machine de son rayon ou d’un voisin."
      },
      {
        "domaine": "Piste directe, Éveil cumulatif & Zéro-mémoire (INV-08, INV-09, INV-10)",
        "avant": "Défilement gauche → droite avec retours en arrière, compteur individuel sur Résonance et Éveil exigeant les N deuxièmes pions engagés au même tour.",
        "apres": "Activation directe sur l’unique icône allumée, Résonance déclenchée une fois par vague lorsqu’une vraie activation vide un dernier pari, Éveil cumulatif dès ≥ A + 1 Gardiens en piste en Face 2 avec 0 pari perdu ce tour, fil d’ouverture imprimé, dé retiré et Défenseurs couchés sur Rêve résolu."
      },
      {
        "domaine": "6 Verbes du Cœur & Passe 2 des 30 Tuiles",
        "avant": "Canon Passe 1 assemblé depuis 3 panels aux styles hétérogènes et à quelques clauses redondantes ou lourdes.",
        "apres": "Lexique unifié des 6 Verbes (Refroidir, Altérer, Reculer, Étouffer, Semer au sac, Glisser un Rêve), grammaire télégraphique zéro-émoji des 30 Mini-Tuiles, 13 tuiles alignées + 17 tuiles consolidées (13 catalyseurs d’Éveil, 6 Twists 2K3, 3 Lois passives, 0 erreur sur 197 assises)."
      }
    ]
  }
};

const MODULE_ESSAIM_REGLES_NATIVES_V6_4 = {
  "deploiement_direct_production": {
    "nom": "Déploiement direct à la Production",
    "fenetre": "PRODUCTION",
    "texte": "Chaque Nid défendu produit +1 Insecte (0–1 présent) ou +2 Insectes (≥ 2 présents) sans allumer d’icône ; chaque Insecte ainsi créé est immédiatement posé au choix sur ce Nid, sur une parcelle adjacente de son rayon (en sautant les Routes), ou — si ce Nid occupe la dernière parcelle de son rayon — sur un rang 1–6 de la Réglette ou une icône de la Piste des Gardiens ; puis le pouvoir du Nid s’applique."
  },
  "amorcage_natif": {
    "nom": "Amorçage natif de l’Essaim",
    "fenetre": "PERMANENT",
    "texte": "Si un effet de tuile déplace ou prélève un Insecte en jeu alors qu’aucun Insecte n’est sur le plateau, prenez 1 Insecte dans la réserve de l’Essaim."
  },
  "demenagement_unifie_nid": {
    "nom": "Déménagement unifié d’un Nid",
    "fenetre": "PERMANENT",
    "texte": "Tout Nid déplacé par une tuile emporte simultanément tous ses Insectes, tous les Défenseurs de sa parcelle et toute éventuelle ponte glissée sous lui."
  },
  "deviation_reglette": {
    "nom": "Déviation de dé (±1)",
    "fenetre": "OUVERTURE",
    "texte": "À l’ouverture des paravents, défaussez 1 Insecte posé sur un rang de la Réglette pour décaler le dé d’une machine mobile de −1 ou +1 rang (entre 1 et 6), en allumant l’icône Insecte."
  },
  "bouclier_de_lisiere": {
    "nom": "Bouclier de lisière (facultatif)",
    "fenetre": "FIN_ATTAQUES",
    "gouverneur": "I",
    "facultatif": true,
    "texte": "En fin d’attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes choisit de défausser ou non 1 Insecte pour maintenir le Gardien en piste sur sa face actuelle (sa Face 2 est sauvée pour la suite, mais son pari reste perdu à ce tour)."
  }
};

const PHYSICAL_INVARIANTS_V6_4 = [
  {
    "id": "INV-01",
    "categorie": "MATERIEL",
    "titre": "Dotation finie 10×N pions uniques Arbre / Souche recto-verso",
    "enonce_canonique": "Dotation finie exacte de 10 × N pions uniques recto-verso (Arbre debout / Souche, zéro réserve illimitée). Couper (Abatteuse) = retourner tous les Arbres debout sur place en Souche sans toucher aux Souches ; terrasser (Bulldozer) = retourner 1 Arbre en Souche puis retirer toutes les Souches de la parcelle ; repousse finale = retourner des Souches survivantes en Arbres debout au décompte final uniquement (plafond de dotation initiale 100 % physique).",
    "assertions_livret": [
      "10 × N",
      "recto-verso",
      "Arbre debout",
      "Souche"
    ],
    "target_test_id": "test_inv01_finite_reversible_trees_stumps"
  },
  {
    "id": "INV-02",
    "categorie": "MATERIEL",
    "titre": "Jetons Puissance recto-verso Rouge (+1) / Bleu Surchauffe (−1)",
    "enonce_canonique": "Les jetons Puissance sont des pièces recto-verso portant Rouge (+1) au recto et Bleu Surchauffe (−1) au verso. Refroidir une machine consiste toujours à retourner 1 Rouge existant en Bleu (aucun Bleu posé à sec depuis la réserve).",
    "assertions_livret": [
      "recto-verso",
      "Rouge",
      "Bleu",
      "Surchauffe"
    ],
    "target_test_id": "test_inv02_reversible_power_tokens"
  },
  {
    "id": "INV-03",
    "categorie": "MATERIEL",
    "titre": "Modèle unique de 2 Défenseurs recto-verso & Chamanes Humains auto-vérifiants",
    "enonce_canonique": "Chaque joueur dispose de 2 pions Défenseurs recto-verso (Réflexion / Définitif) : le 1er pion est posé directement face Définitif (jamais sur les Gardiens) ; le 2e pion est posé face Réflexion puis retourné irréversiblement sur Définitif, figeant simultanément le jeton Duel ou le Perchoir de Vigie mobilisés ce tour. Chez les Humains (H), seuls 2 pions Chamanes existent au total (1 Tambour et 1 Chant recto-verso), rendant le binôme imposé auto-vérifiant.",
    "assertions_livret": [
      "Réflexion",
      "Définitif",
      "Tambour",
      "Chant"
    ],
    "target_test_id": "test_inv03_two_reversible_defenders_and_human_chamans"
  },
  {
    "id": "INV-04",
    "categorie": "GOUVERNANCE",
    "titre": "Clôture du temps de réflexion à N−1 joueurs validés",
    "enonce_canonique": "Dès que N−1 joueurs ont retourné leur 2e pion sur sa face Définitif, le dernier joueur effectue au plus 1 ultime ajustement avant de valider irréversiblement son pion.",
    "assertions_livret": [
      "ultime ajustement"
    ],
    "target_test_id": "test_inv04_reflection_closure_n_minus_1"
  },
  {
    "id": "INV-05",
    "categorie": "MATERIEL",
    "titre": "Sac opaque de jetons épais & Sabotage différé au tirage",
    "enonce_canonique": "La pioche s’effectue dans un sac en tissu opaque contenant les 2N jetons Machine épais, les jetons Sabotage ordinaires et jusqu’à 4 jetons Sabotage Écaille (via tuiles R). Les jetons non piochés restent cachés sans être consultés ; les jetons révélés et celui du Perchoir de Vigie retournent dans le sac au ménage. Lorsqu’un jeton Sabotage ordinaire est révélé à l’ouverture (hors Écaille), il ne mobilise aucune machine, allume Sabotage, et le joueur qui l’a tiré vise 1 machine de son rayon ou d’un rayon voisin : si elle porte au moins 1 Rouge (mobile ou Ratissage), il la Refroidit ; sinon, si elle est mobile, il la fait Reculer d’1 parcelle vers la bordure.",
    "assertions_livret": [
      "sac",
      "opaque",
      "cachés",
      "Refroidit"
    ],
    "target_test_id": "test_inv05_opaque_bag_and_compound_sabotage"
  },
  {
    "id": "INV-06",
    "categorie": "GOUVERNANCE",
    "titre": "Ordre de distribution en pénurie (Coordonnateur horaire, Oiseau en dernier)",
    "enonce_canonique": "En cas de pénurie dans le sac, la distribution s’effectue dans le sens horaire à partir du Coordonnateur, en servant toujours l’Oiseau en dernier (il regarde jusqu’à 2 jetons du sac, en garde 1 si possible et pose l’autre face cachée sur son Perchoir de Vigie).",
    "assertions_livret": [
      "Coordonnateur",
      "Oiseau",
      "en dernier",
      "Perchoir de Vigie"
    ],
    "target_test_id": "test_inv06_shortage_clockwise_bird_last"
  },
  {
    "id": "INV-07",
    "categorie": "MATERIEL",
    "titre": "Lancer universel des 2 dés standards sous paravent fermé & choix libre Oiseau",
    "enonce_canonique": "Sous paravent fermé, tous les joueurs lancent uniquement leurs 2 dés standards 1–6 (même sur Sabotage ou Écaille, jet ignoré), éliminant toute fuite sonore. S’il détient un jeton Machine, l’Oiseau (O) choisit librement lequel de ses 2 dés il retient (au lieu du plus petit pour les autres Peuples) ; l’autre dé est son dé écarté.",
    "assertions_livret": [
      "tous les joueurs lancent",
      "2 dés standards",
      "fuite sonore",
      "dé écarté"
    ],
    "target_test_id": "test_inv07_universal_two_dice_and_bird_free_choice"
  },
  {
    "id": "INV-08",
    "categorie": "MATERIEL",
    "titre": "Réglette fixe 1–6, bandelette d’Acte, fil d’ouverture imprimé & dé retiré",
    "enonce_canonique": "La Réglette des Tactiques est fixe sur 6 rangs (cases Rêves au-dessus des actions imprimées 1/4 Sur place, 2/5 Devant, 3/6 En avançant −1), porte imprimé le fil d’ouverture (1. Altérations → 2. Sabotages & Écailles → 3. Déviations ±1 → 4. Rêves défendus) et est accompagnée dessous d’une bandelette d’Acte réversible retournée seule au début du Tour 5 sans déplacer ni Rêves ni Insectes. Dès qu’une machine mobile est Étouffée ou a terminé son attaque, son dé est immédiatement retiré de la Réglette.",
    "assertions_livret": [
      "Réglette",
      "bandelette",
      "Tour 5",
      "fil d’ouverture"
    ],
    "target_test_id": "test_inv08_fixed_track_act_strip_and_removed_die"
  },
  {
    "id": "INV-09",
    "categorie": "MATERIEL",
    "titre": "Piste des Gardiens directe à 6 icônes (sans balayage) & Résonance au dernier pari",
    "enonce_canonique": "La Piste des Gardiens comporte 6 icônes dédiées sans numéros : [Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance]. Lorsqu’un événement allume son unique icône parmi les 5 premières, seuls les Gardiens posés sur cette icône portant ≥ 1 pari s’activent directement (zéro balayage séquentiel, zéro reprise en arrière). Si cette activation vide le dessus d’au moins un Gardien (dernier pari glissé en encoche lors d’une vraie activation ; exclu sur glissement passif sans activation), l’icône Résonance s’allume juste après, une seule fois pour cette vague sans boucler sur elle-même.",
    "assertions_livret": [
      "Parade",
      "Piégeage",
      "Sabotage",
      "Rêve",
      "Insecte",
      "Résonance",
      "dernier pari"
    ],
    "target_test_id": "test_inv09_direct_guardian_icons_and_last_bet_resonance"
  },
  {
    "id": "INV-10",
    "categorie": "MATERIEL",
    "titre": "Deux encoches visibles, verdict de pari & Éveil cumulatif en piste (A + 1 Face 2)",
    "enonce_canonique": "Chaque tuile Gardien comporte 2 encoches latérales visibles dans lesquelles glisse 1 Défenseur à chaque activation. En fin d’attaques : ≥ 1 pion encore sur la tuile = pari perdu ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche = aucune mise (reste en place sans évoluer). Aux Tours 1 à 7 (A ≥ 1), l’Éveil de la Forêt est remporté dès qu’au moins A + 1 Gardiens en piste sont sur leur Face 2 ET qu’aucun pari de Gardien n’a été perdu à ce tour.",
    "assertions_livret": [
      "encoches",
      "pari perdu",
      "pari gagné",
      "Face 2",
      "A + 1"
    ],
    "target_test_id": "test_inv10_guardian_notches_and_cumulative_awakening"
  },
  {
    "id": "INV-11",
    "categorie": "CAS_LIMITE",
    "titre": "Formule unifiée du Seuil de Parade (Bleus actifs en tous modes)",
    "enonce_canonique": "Seuil de Parade = chiffre gravé + jetons rouges (en Mode Assaut et Ratissage uniquement ; ignorés en Mode Charge) − jetons bleus Surchauffe (actifs dans TOUS les modes : Charge, Assaut et Ratissage) − 1 aux rangs 3 et 6 (minimum 1). En Mode Charge, gain plafonné à +1 jeton rouge par activation dès qu’au moins 1 frappe sur parcelle réelle non-Route n’est ni parée ni piégée.",
    "assertions_livret": [
      "Seuil de Parade",
      "bleus",
      "Charge",
      "minimum 1"
    ],
    "target_test_id": "test_inv11_parade_threshold_blue_in_all_modes"
  },
  {
    "id": "INV-12",
    "categorie": "CAS_LIMITE",
    "titre": "Ratissage physique (+1 rouge convertible, immobile, parcelle ciblée, Étouffement 90°)",
    "enonce_canonique": "Au ménage, toute machine terminant sur la dernière parcelle de son rayon glisse son jeton Machine sous elle (hors du sac), conserve tous ses jetons Puissance antérieurs et gagne +1 jeton rouge physique (convertible en bleu ; 0 bonus imprimé). Une machine en Ratissage ne se déplace jamais (ni avancée, ni recul, ni cale, ni Altération, ni changement de rang), mais sa parcelle compte pleinement comme « parcelle ciblée » tant qu’elle n’a pas frappé ce tour ; si elle est Étouffée, tournez la machine à 90° sur place jusqu’au ménage.",
    "assertions_livret": [
      "Ratissage",
      "jeton rouge",
      "parcelle ciblée"
    ],
    "target_test_id": "test_inv12_ratissage_physical_red_immobile_targeted"
  },
  {
    "id": "INV-13",
    "categorie": "CAS_LIMITE",
    "titre": "Parcelles ciblées figées au début de l’activation & Repli de bordure sans double bond",
    "enonce_canonique": "Les parcelles visées par une machine sont figées au début de son activation (toute cible devenue Route Forestière entre-temps est annulée sans report). Si la création d’une Route en bordure pousse déjà une machine d’1 parcelle vers le cœur pendant ses frappes, cette poussée couvre et remplace l’avancée finale d’une action En avançant (jamais de double bond +2 vers le cœur en une activation).",
    "assertions_livret": [
      "figées",
      "Route",
      "En avançant"
    ],
    "target_test_id": "test_inv13_frozen_targets_and_border_retreat_no_double_jump"
  },
  {
    "id": "INV-14",
    "categorie": "CAS_LIMITE",
    "titre": "Visibilité des jetons Machine, Furtivité m(r) & Effet Sentinelle sur Rive Sabotage",
    "enonce_canonique": "Les jetons Machine révélés restent visibles devant leur rayon jusqu’au verdict de Furtivité (inclinés à 90° et dé retiré s’ils sont Étouffés). La mobilisation m(r) compte les jetons Machine visibles devant r plus ses machines en Ratissage (indépendant d’une déviation ±1, d’un Étouffement ou d’une Altération ; Sabotage/Écaille = 0). Effet Sentinelle permanent : chaque tuile enracinée occupe en permanence 1 place de la Rive Sabotage de son rayon (1 tuile = 1 seul Défenseur actif requis ; 2 tuiles = 2/2 permanent à 0 Défenseur quand m(r) = 0). La Rive Piège exige toujours 2 Défenseurs.",
    "assertions_livret": [
      "90°",
      "Furtivité",
      "Rive Piège",
      "Rive Sabotage",
      "Sentinelle"
    ],
    "target_test_id": "test_inv14_machine_tokens_furtivite_and_sentinel_bank"
  },
  {
    "id": "INV-15",
    "categorie": "CAS_LIMITE",
    "titre": "Fil d’ouverture imprimé (1→4), choix du propriétaire, Défenseurs couchés & solidaires",
    "enonce_canonique": "Ordre strict imprimé sur la Réglette : (1) Altérations → (2) Sabotages (Refroidir sinon Reculer) & Écailles (Croc) un par un → (3) Déviations d’Insecte ±1 une par une → (4) Rêves défendus de gauche à droite : le propriétaire du Rêve choisit quelle(s) machine(s) du rang sont Étouffées (y compris déviée : jeton incliné 90° et dé retiré), résout intégralement le pouvoir propre du Rêve (actif dès que défendu même à 0 machine, sauf mention « Quand ce Rêve annule… »), couche ses Défenseurs à plat pour marquer le Rêve résolu, puis si ≥ 1 machine a été Étouffée, allume directement l’icône Rêve. Lors de tout glissement, les Défenseurs posés sur un Rêve se déplacent toujours avec lui (debout ou couchés).",
    "assertions_livret": [
      "gauche à droite",
      "propriétaire",
      "couchés",
      "déplacent toujours avec lui"
    ],
    "target_test_id": "test_inv15_opening_track_owner_choice_and_lying_defenders"
  },
  {
    "id": "INV-16",
    "categorie": "CAS_LIMITE",
    "titre": "Zéro écrasement au contact hors Route & Vidage sur Route Forestière",
    "enonce_canonique": "Le déplacement d’une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d’une Route Forestière (0 Arbre et 0 Souche après un Bulldozer) vide la case : Nid renvoyé en lisière reconstructible, Défenseurs rendus en main, Piège/Croc/Insectes/Duel/ponte remis en réserve. Les Routes Forestières sont sautées radialement et infranchissables latéralement.",
    "assertions_livret": [
      "intacts",
      "Route Forestière",
      "reconstructible"
    ],
    "target_test_id": "test_inv16_zero_crush_on_contact_route_clears_cell"
  },
  {
    "id": "INV-17",
    "categorie": "CAS_LIMITE",
    "titre": "Plafond de 1 Piège ordinaire par parcelle, autonomie et priorité du Croc",
    "enonce_canonique": "Une parcelle porte au maximum 1 Piège ordinaire ; tout Piège ordinaire est autonome (pare 1 frappe même avec 0 Défenseur et 0 Insecte, allume l’icône Piégeage et est défaussé aussitôt). Le jeton Croc Reptile peut cohabiter avec un Piège ordinaire sur la même parcelle, pare alors en premier puis revient dans la réserve Reptile.",
    "assertions_livret": [
      "Piège",
      "Croc",
      "en premier"
    ],
    "target_test_id": "test_inv17_max_one_trap_and_croc_cohabitation_priority"
  },
  {
    "id": "INV-18",
    "categorie": "GOUVERNANCE",
    "titre": "Bouclier de lisière facultatif gouverné par les Insectes (I)",
    "enonce_canonique": "En fin d’attaques, lorsqu’un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes (I) choisit librement de défausser ou non 1 Insecte de cette icône pour maintenir le Gardien en piste sur sa face actuelle (il conserve sa Face 2 pour la suite de la partie, mais son pari reste perdu à ce tour).",
    "assertions_livret": [
      "Bouclier de lisière",
      "Insectes",
      "choisit"
    ],
    "target_test_id": "test_inv18_optional_bouclier_lisiere_governed_by_insects"
  },
  {
    "id": "INV-19",
    "categorie": "GOUVERNANCE",
    "titre": "Interdiction de tuile inplaçable, repli de 1re pose, bâtisseurs en attente & bonus 3J unifié",
    "enonce_canonique": "Il est interdit de compléter en lisière une tuile impossible à placer sur le plateau. Si aucun emplacement légal n’existe au 1er temps de pose, le joueur peut placer son 1er Défenseur sur une parcelle d’un allié. Sitôt une tuile construite, ses 2 bâtisseurs sont couchés « en attente » devant leur propriétaire — sauf à 3 joueurs où construire un Gardien, un Rêve ou un Nid libère immédiatement 1 des 2 bâtisseurs vers une parcelle adjacente.",
    "assertions_livret": [
      "impossible à placer",
      "en attente",
      "3 joueurs",
      "ou un Nid"
    ],
    "target_test_id": "test_inv19_unplaceable_tile_ban_and_unified_3p_bonus"
  },
  {
    "id": "INV-20",
    "categorie": "CAS_LIMITE",
    "titre": "Accessoires 3 + 3 épurés : Duel unifié, Perchoir orientable, Altération, Écailles/Croc/Cale",
    "enonce_canonique": "Trois accessoires actifs dès le Tour 1 : H (Tambour/Chant) ; M (Duel unifié : toute frappe parée ou piégée par n’importe quel moyen sur sa parcelle le retourne sur Territoire tenu ; seule une frappe ni parée ni piégée le renvoie en réserve) ; O (Perchoir de Vigie mobile orientable Chaud/Calme, placé au pied d’un rayon ou pointé vers un rang 1–6, figé avec le 2e Défenseur). Trois progressifs via tuiles : E (Altération max 1/mobile) ; R (4 Écailles, Croc réutilisable, mot cale exclusif au Caïman noir) ; I (Module Essaim).",
    "assertions_livret": [
      "Duel",
      "Perchoir de Vigie",
      "Altération",
      "Écaille"
    ],
    "target_test_id": "test_inv20_accessories_v6_4_unified_duel_and_perchoir"
  },
  {
    "id": "INV-21",
    "categorie": "MATERIEL",
    "titre": "Module Essaim clos sur I : Déploiement direct à la Production, Amorçage & Déménagement natifs",
    "enonce_canonique": "Les jetons Insectes sont exclusifs aux 10 tuiles des 5 lisières de I et restent dans la boîte dès que I ne joue pas (Production ignorée, icône Insecte inactive). Quand I joue : chaque Nid défendu produit +1 (0–1 présent) ou +2 (≥ 2 présents) sans allumer d’icône, chaque Insecte créé étant immédiatement posé au choix sur ce Nid, sur une parcelle adjacente de son rayon (en sautant les Routes) ou — depuis la dernière parcelle — sur un rang 1–6 ou une icône Gardien ; Amorçage natif (1 Insecte pris en réserve si un effet de tuile déplace/prélève un Insecte alors qu’il y en a 0 en jeu) ; Déménagement unifié d’un Nid (emporte Insectes, Défenseurs et ponte) ; descente sur place au ménage d’un Insecte passager.",
    "assertions_livret": [
      "Insectes",
      "boîte",
      "Déploiement direct",
      "Amorçage natif",
      "passager"
    ],
    "target_test_id": "test_inv21_swarm_direct_deployment_native_priming_and_move"
  },
  {
    "id": "INV-22",
    "categorie": "CAS_LIMITE",
    "titre": "Enracinement volontaire sur la Rive Sabotage (Sentinelle & Souches libres au décompte final)",
    "enonce_canonique": "Au ménage, avant de remettre les jetons dans le sac, chaque joueur peut enraciner au plus 1 tuile construite de son Peuple sur une place libre de la Rive Sabotage de son rayon (interdit si rayon 100 % Routes) : elle quitte sa piste ou parcelle en y laissant ses Insectes, perd son pouvoir actif (hors clause Enraciné), occupe en permanence cette place (Effet Sentinelle) et un Rêve enraciné ferme le Sommeil (sauf mention contraire). Au décompte final uniquement (Tour 8, Sommeil ou Éveil), elle retourne 1 Souche survivante (F1/unique) ou 2 Souches (F2) en Arbres debout, librement choisies parmi les parcelles survivantes de son rayon.",
    "assertions_livret": [
      "enraciner",
      "Rive Sabotage",
      "Sommeil impossible",
      "1 Souche",
      "Face 2"
    ],
    "target_test_id": "test_inv22_voluntary_rooting_on_sabotage_bank"
  }
];

const SPEC_FORMELLE_V6_4 = {
  "schema_version": "6.4.0",
  "date_consolidation": "2026-11-27",
  "architecture_reference": {
    "total_emplacements_synergie": 30,
    "total_profils": 30,
    "topologies_validees": {
      "P4_2233": [
        2,
        2,
        3,
        3
      ]
    },
    "reserves_materiel": "finie (10 * N pions uniques recto-verso Arbre debout/Souche ; sac opaque de jetons)",
    "plafond_repousse_parcelle": "dotation_initiale_arbres_physique",
    "repousse_finale_base": 0,
    "enracinement_volontaire": {
      "face_unique_ou_face_1": 1,
      "face_2": 2
    },
    "score_final": "arbres_debout_apres_enracinement_volontaire"
  },
  "architecture_modulaire": {
    "principe": "1 Tronc commun court suivi de 3 modules activés uniquement si au moins un Peuple de la famille participe à la partie.",
    "tronc_commun": {
      "id": "tronc_commun",
      "titre": "Tronc commun (toujours actif)",
      "perimetre": "Forêt finie 10×N, sac opaque de jetons (avec Sabotage différé Refroidir/Reculer), 2 dés standards universels, Réglette fixe à bandelette d’Acte et fil d’ouverture imprimé, 2 Défenseurs recto-verso, Furtivité Chaud/Calme à Rive Sabotage unifiée avec Enracinement volontaire (Effet Sentinelle permanent), Pièges autonomes, attaques avec dé retiré, Ratissage physique, 6 Verbes du Cœur et score final."
    },
    "modules": {
      "module_gardiens_et_eveil": {
        "titre": "Module Gardiens & Éveil",
        "peuples_requis": [
          "M",
          "R",
          "O"
        ],
        "assises_actives": 196,
        "assises_total": 197,
        "assises_inactives": [
          [
            "H",
            "E",
            "I"
          ]
        ],
        "resume": "Lu uniquement si au moins un Peuple Animal Sauvage (M, R ou O) joue : Piste des Gardiens à 6 icônes directes (sans balayage), Résonance en 6e position déclenchée au dernier pari glissé lors d’une vraie activation, 2 encoches visibles par Gardien, paris 0/1/2 Défenseurs, passage Face 2 sur pari gagné et fin anticipée par Éveil cumulatif (≥ A + 1 Gardiens en piste en Face 2 et 0 pari perdu ce tour)."
      },
      "module_reves_et_sommeil": {
        "titre": "Module Rêves & Sommeil",
        "peuples_requis": [
          "H",
          "E"
        ],
        "famille_inactive": [
          "M",
          "R",
          "O",
          "I"
        ],
        "resume": "Lu uniquement si au moins un Peuple Onirique (H ou E) joue : pose de Rêves sur la Réglette depuis la droite, défense en 1er et 2e temps, annulation (Étouffement) choisie par le propriétaire du Rêve, Défenseurs couchés dès résolution, glissements avec Défenseurs solidaires et fin anticipée par Sommeil du Contremaître (impossible si un Rêve est enraciné, hors exception explicite)."
      },
      "module_essaim": {
        "titre": "Module Essaim",
        "peuples_requis": [
          "I"
        ],
        "assises_actives": 160,
        "assises_total": 197,
        "assises_inactives_count": 37,
        "regles_natives": {
          "deploiement_direct_production": {
            "nom": "Déploiement direct à la Production",
            "fenetre": "PRODUCTION",
            "texte": "Chaque Nid défendu produit +1 Insecte (0–1 présent) ou +2 Insectes (≥ 2 présents) sans allumer d’icône ; chaque Insecte ainsi créé est immédiatement posé au choix sur ce Nid, sur une parcelle adjacente de son rayon (en sautant les Routes), ou — si ce Nid occupe la dernière parcelle de son rayon — sur un rang 1–6 de la Réglette ou une icône de la Piste des Gardiens ; puis le pouvoir du Nid s’applique."
          },
          "amorcage_natif": {
            "nom": "Amorçage natif de l’Essaim",
            "fenetre": "PERMANENT",
            "texte": "Si un effet de tuile déplace ou prélève un Insecte en jeu alors qu’aucun Insecte n’est sur le plateau, prenez 1 Insecte dans la réserve de l’Essaim."
          },
          "demenagement_unifie_nid": {
            "nom": "Déménagement unifié d’un Nid",
            "fenetre": "PERMANENT",
            "texte": "Tout Nid déplacé par une tuile emporte simultanément tous ses Insectes, tous les Défenseurs de sa parcelle et toute éventuelle ponte glissée sous lui."
          },
          "deviation_reglette": {
            "nom": "Déviation de dé (±1)",
            "fenetre": "OUVERTURE",
            "texte": "À l’ouverture des paravents, défaussez 1 Insecte posé sur un rang de la Réglette pour décaler le dé d’une machine mobile de −1 ou +1 rang (entre 1 et 6), en allumant l’icône Insecte."
          },
          "bouclier_de_lisiere": {
            "nom": "Bouclier de lisière (facultatif)",
            "fenetre": "FIN_ATTAQUES",
            "gouverneur": "I",
            "facultatif": true,
            "texte": "En fin d’attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes choisit de défausser ou non 1 Insecte pour maintenir le Gardien en piste sur sa face actuelle (sa Face 2 est sauvée pour la suite, mais son pari reste perdu à ce tour)."
          }
        },
        "resume": "Lu uniquement si les Insectes (I) jouent : jetons Insectes exclusifs aux 10 tuiles des 5 lisières de I (laissés dans la boîte sans I, Production ignorée et icône Insecte inactive), Déploiement direct à la Production (+1/+2 vers le Nid, une parcelle adjacente ou les pistes centrales depuis la dernière parcelle), Amorçage natif en réserve, Déménagement unifié des Nids, Déviation ±1, Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d’un Insecte passager non dépensé."
      }
    }
  },
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve, Nid) est gouvernée exclusivement par le joueur de son Peuple d’origine ; la pose d’un Piège gagné en Furtivité est choisie par le propriétaire du rayon ; le Bouclier de lisière est facultatif et gouverné par le joueur Insectes (I). Zéro vote de groupe.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés. Tous les joueurs lancent uniquement leurs 2 dés standards 1–6 (même sur Sabotage ou Écaille, jet ignoré) afin d’éliminer toute fuite sonore.",
    "pont_routier_routes_forestieres": "Une parcelle désigne toujours une case de forêt non devenue Route Forestière. Le long d’un rayon, les Routes Forestières sont sautées radialement et infranchissables latéralement. Dès qu’un rayon est 100 % Routes Forestières, sa zone de Furtivité est fermée et l’Enracinement y est interdit.",
    "zero_ecrasement_et_zero_dette": "Zéro écrasement au contact hors Route : déplacer une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d’une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel/ponte en réserve). Zéro dette mémorielle : fil d’ouverture imprimé sur la Réglette, dé retiré dès qu’une mobile est Étouffée ou a attaqué, Défenseurs couchés sur Rêve résolu ; Pièges autonomes SINGLE_STRIKE (max 1 par parcelle ; Croc cohabite et pare en premier).",
    "piste_gardiens_directe_6_icones": "On résout intégralement l’action ou la tuile en cours avant d’activer directement la seule icône allumée parmi [PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE] (zéro balayage séquentiel, zéro reprise en arrière). Partition stricte « 1 événement = au plus 1 icône » ; si cette vague vide le dessus d’au moins un Gardien (dernier pari glissé en encoche lors d’une vraie activation, exclu sur glissement passif), l’icône RESONANCE (6e position) s’allume aussitôt une seule fois pour cette vague sans boucler sur elle-même."
  },
  "etapes_tour": [
    {
      "numero": 1,
      "code": "PREPARATION_ET_DES_SECRETS",
      "nom": "Bandelette d’Acte, Pioche au sac opaque et 2 Dés universels",
      "regles": [
        "Réglette fixe 1–6 à bandelette d’Acte réversible et fil d’ouverture imprimé : Acte 1 (Tours 1–4, Face A) place les rangs 1–3 en Mode Charge et 4–6 en Mode Assaut. Au début du Tour 5, retournez uniquement la bandelette d’Acte sur Face B (Acte 2, Tours 5–8) : 1–3 en Mode Assaut et 4–6 en Mode Charge, sans déplacer ni Rêves ni Insectes. Actions fixes : 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (Sur place + Devant, avancée +1, Seuil −1).",
        "Départ décalé canonique (P4_2233, dotation finie 10×N pions Arbre/Souche recto-verso) : Bulldozer en parcelle 1, Abatteuse en parcelle 2 sur chaque rayon.",
        "Pioche au sac opaque : chaque joueur pioche secrètement 1 jeton (2N jetons Machine épais + Sabotages ordinaires + jusqu’à 4 Écailles). Les jetons non piochés restent cachés sans être consultés. En cas de pénurie, distribution horaire depuis le Coordonnateur, Oiseau toujours servi en dernier (regarde jusqu’à 2 jetons, garde 1 et pose l’autre face cachée sur son Perchoir de Vigie).",
        "Lancer universel de 2 dés standards 1–6 sous paravent fermé : tous les joueurs lancent leurs 2 dés standards, même sur Sabotage ou Écaille (jet ignoré), éliminant toute fuite sonore. S’il détient un jeton Machine, l’Oiseau choisit librement lequel de ses 2 dés il retient (l’autre est son dé écarté) ; les autres Peuples retiennent le plus petit (min) et écartent l’autre."
      ]
    },
    {
      "numero": 2,
      "code": "POSE_DES_DEFENSEURS",
      "nom": "Pose des 2 Défenseurs recto-verso, Rêves, Furtivité et Paris Gardiens",
      "regles": [
        "1er temps de pose simultané (directement face Définitif, jamais sur les Gardiens) : parcelle de sa propre Forêt (ou parcelle alliée en repli si aucun emplacement légal ; Tambour H autorisé sur tout rayon), tuile non construite de ses 2 lisières (interdit si impossible à placer), Rêve présent sur la Réglette, ou rive ouverte de Furtivité d’un rayon non 100 % Route.",
        "Furtivité « Chaud vs Calme » par rayon : 2 rives indépendantes de 2 places (Rive Piège et Rive Sabotage) au pied de chaque rayon actif. Effet Sentinelle : chaque tuile enracinée occupe en permanence 1 place de la Rive Sabotage (1 tuile = 1 Défenseur requis ; 2 tuiles = 2/2 permanent à 0 Défenseur). La Rive Piège exige toujours 2 Défenseurs.",
        "2e temps de pose global (face Réflexion -> validation irréversible face Définitif) : partout sur le plateau, y compris en pari sur un Gardien construit (0, 1 ou 2 Défenseurs max par Gardien si au moins 1 Animal Sauvage joue). Retourner son 2e pion sur Définitif fige simultanément son jeton Duel ou la position/orientation Chaud–Calme de son Perchoir de Vigie ; dès que N−1 joueurs ont validé, le dernier joueur effectue au plus 1 ultime ajustement. Chez H : 2 pions Chamanes (1 Tambour, 1 Chant) rendant le binôme auto-vérifiant."
      ]
    },
    {
      "numero": 3,
      "code": "CONSTRUCTION_ET_REVELATION",
      "nom": "Constructions obligatoires et Fil d’ouverture imprimé (1 → 4)",
      "regles": [
        "Constructions obligatoires avant l’ouverture des paravents de toute tuile réunissant ses 2 bâtisseurs (interdit si l’emplacement cible est indisponible). Sitôt construite, les 2 bâtisseurs sont couchés « en attente » devant leur propriétaire — sauf à 3 joueurs où construire un Gardien, un Rêve ou un Nid libère immédiatement 1 des 2 bâtisseurs vers une parcelle adjacente.",
        "Nid : posé sur une parcelle libre sans machine ni autre Nid de l’un de ses 2 rayons. Rêve : posé par-dessus le rang libre le plus à droite (6, 5…) de la Réglette fixe sans déplacer les Insectes.",
        "Ouverture des paravents : les jetons Machine révélés restent visibles devant leur rayon jusqu’à la Furtivité ; les dés retenus des machines mobiles sont posés sur leur rang 1–6 (dès qu’une mobile est Étouffée ou a terminé son attaque, son dé est retiré de la Réglette et son jeton est incliné à 90° si Étouffée).",
        "Fil d’ouverture imprimé sur la Réglette : (1) Altérations (retirez chaque Altération sur machine révélée : elle compte dans m(r), Recule d’1 parcelle et est Étouffée) → (2) Sabotages & Écailles un par un (tous allument SABOTAGE ; un Sabotage ordinaire vise 1 machine de son rayon ou d’un rayon voisin pour la Refroidir si ≥ 1 Rouge, sinon la faire Reculer d’1 parcelle si mobile ; une Écaille pose le Croc sur une parcelle ciblée) → (3) Déviations d’Insectes ±1 une par une (allume INSECTE) → (4) Rêves défendus de gauche à droite (le propriétaire choisit quelle(s) machine(s) du rang sont Étouffées y compris déviées, résout intégralement le pouvoir du Rêve actif même à 0 machine hors mention contraire, couche ses Défenseurs à plat pour le marquer résolu, puis allume REVE si ≥ 1 machine a été Étouffée). Les Défenseurs posés sur un Rêve se déplacent toujours avec lui."
      ]
    },
    {
      "numero": 4,
      "code": "FURTIVITE_ET_PRODUCTION_ESSAIM",
      "nom": "Furtivité par rayon et Déploiement direct des Nids de l’Essaim",
      "regles": [
        "Furtivité « Chaud vs Calme » : évaluée sur toute rive complétée à 2/2 (2 Défenseurs sur Rive Piège ; 2 places occupées sur Rive Sabotage en comptant les tuiles enracinées en Sentinelle permanente) selon m(r) = jetons Machine visibles devant r (droits ou inclinés) + machines de r en Ratissage (indépendant de déviation ±1, Étouffement Rêve ou Altération ; Sabotage/Écaille = 0 rayon). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège ordinaire) ; Rive Sabotage gagnée si m(r) == 0 (Semer 1 Sabotage au sac sans allumer SABOTAGE).",
        "Module Essaim (uniquement si I joue) — Production à Déploiement direct : dans l’ordre choisi par I, chaque Nid défendu produit +1 Insecte (0–1 présent) ou +2 Insectes (≥ 2 présents) sans allumer INSECTE ; chaque Insecte ainsi créé est immédiatement posé au choix sur ce Nid, sur une parcelle adjacente de son rayon (en sautant les Routes), ou — si ce Nid occupe la dernière parcelle de son rayon — sur un rang 1–6 de la Réglette ou une icône de la Piste des Gardiens ; puis le pouvoir propre du Nid s’applique. Aucune phase supplémentaire ensuite."
      ]
    },
    {
      "numero": 5,
      "code": "ATTAQUES_ET_TEST_FIN",
      "nom": "Attaques des Machines, Encoches Gardiens et Verdict de fin",
      "regles": [
        "Ordre de passage : dés encore présents sur les rangs 1 à 6 de la Réglette (chaque dé est retiré sitôt son attaque terminée), puis machines en Ratissage non Étouffées (Assaut permanent, immobiles, mais leur parcelle compte comme ciblée tant qu’elles n’ont pas frappé). Abatteuse avant Bulldozer sur un même rayon.",
        "Parcelles ciblées figées au début de l’activation (toute cible devenue Route entre-temps est annulée sans report). Seuil de Parade = chiffre gravé + rouges (en Assaut et Ratissage uniquement ; ignorés en Charge) − bleus Surchauffe (actifs dans TOUS les modes : Charge, Assaut et Ratissage) − 1 aux rangs 3 et 6, minimum 1.",
        "Chaîne des parades : Croc Reptile (pare en premier, allume PIEGEAGE, revient en réserve R) -> Piège ordinaire autonome SINGLE_STRIKE (pare 1 frappe même à 0 pion, allume PIEGEAGE, défaussé aussitôt) -> Parade classique (Défenseurs seuls -> PARADE ; avec défausse immédiate d’Insectes -> INSECTE). Duel unifié : toute frappe sur la parcelle du Duel parée ou piégée par n’importe quel moyen retourne aussitôt le Duel sur Territoire tenu.",
        "Frappe non parée : Abatteuse retourne tous les Arbres debout en Souches sans toucher aux Souches ; Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches. En Mode Charge : +1 jeton rouge max/activation dès qu’au moins 1 frappe réelle non-Route n’est ni parée ni piégée. En création de Route (0 Arbre, 0 Souche) : la case est vidée (Nid en lisière, Défenseurs en main, Piège/Croc/Insectes/Duel/ponte en réserve) ; si la poussée de bordure déplace déjà la machine d’1 parcelle vers le cœur, elle couvre et remplace l’avancée finale de En avançant (jamais de double bond +2).",
        "Verdict des Gardiens (2 encoches visibles) : ≥ 1 pion encore sur la tuile = pari perdu (retour lisière Face 1, sauf choix facultatif de I de défausser 1 Insecte en Bouclier de lisière pour préserver sa face pour la suite, le pari restant perdu à ce tour) ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche occupée = aucune mise (reste en place sans évoluer).",
        "Vérification de fin : priorité absolue au Tour 8 ; aux Tours 1–7, priorité au Sommeil du Contremaître (tous les Rêves en bloc contigu 1..k, impossible si un Rêve est enraciné hors R1) sur l’Éveil de la Forêt cumulatif (≥ A + 1 Gardiens en piste en Face 2 ET 0 pari perdu ce tour). Au décompte final : application des tuiles enracinées (1 Souche en F1/unique ou 2 en F2 librement choisies parmi les parcelles survivantes de son rayon) puis décompte des Arbres debout."
      ]
    },
    {
      "numero": 6,
      "code": "MENAGE_FIN_DE_TOUR",
      "nom": "Enracinement sur Rive Sabotage, Ratissage physique et Ménage",
      "regles": [
        "Retour en main des Défenseurs (y compris depuis les encoches, les Rêves couchés et la zone en attente), redressement des machines en Ratissage Étouffées à 90°, descente sur place de tout Insecte passager non dépensé et remise à zéro des états transitoires.",
        "Enracinement volontaire (avant remise au sac) : chaque joueur peut enraciner au plus 1 tuile construite de son Peuple sur une place libre de la Rive Sabotage de son rayon (interdit si rayon 100 % Routes). Elle occupe en permanence cette place (Effet Sentinelle) et retournera 1 Souche (F1/unique) ou 2 (F2) au décompte final parmi les parcelles survivantes de son rayon ; un Rêve enraciné ferme le Sommeil (sauf R1).",
        "Passage en Ratissage : toute machine terminant sur la dernière parcelle de son rayon glisse son jeton Machine sous elle (hors sac), conserve tous ses jetons Puissance antérieurs et gagne +1 jeton rouge physique (convertible en bleu ; 0 bonus imprimé).",
        "Remise au sac opaque de tous les jetons révélés et du jeton caché du Perchoir de Vigie, passage du pion Coordonnateur au siège suivant et avancée du marqueur de Tour."
      ]
    }
  ],
  "step_arbitrages_map": {
    "1": [
      "A01",
      "A10",
      "A24"
    ],
    "2": [
      "A02",
      "A03",
      "A22"
    ],
    "3": [
      "A04",
      "A11",
      "A21"
    ],
    "4": [
      "A03",
      "A17",
      "A18"
    ],
    "5": [
      "A05",
      "A06",
      "A08",
      "A09",
      "A14",
      "A15",
      "A16",
      "A19",
      "A23",
      "A25"
    ],
    "6": [
      "A10",
      "A12",
      "A13",
      "A20"
    ]
  },
  "arbitrages_valides": {
    "A01": "Lancer universel de 2 dés standards 1–6 sous paravent fermé : tous les joueurs lancent leurs 2 dés standards, même sur Sabotage ou Écaille (jet ignoré), éliminant toute fuite sonore. L’Oiseau choisit librement lequel de ses 2 dés il retient (l’autre est son dé écarté) ; les autres Peuples retiennent le plus petit.",
    "A02": "Défenseurs recto-verso (Réflexion/Définitif) et clôture à N−1 : 1er pion posé directement face Définitif (jamais sur les Gardiens ; ouvert aux Rêves et à la Furtivité) ; 2e pion posé face Réflexion puis validé irréversiblement sur Définitif (figeant le Duel ou le Perchoir de Vigie ; à N−1 validés, au plus 1 ultime ajustement pour le dernier joueur) ; chez H, 2 Chamanes uniques (Tambour, Chant).",
    "A03": "Furtivité « Chaud vs Calme » & Effet Sentinelle : 2 rives indépendantes de 2 places par rayon actif. Chaque tuile enracinée occupe en permanence 1 place de la Rive Sabotage de son rayon (1 tuile = 1 Défenseur requis ; 2 tuiles = 2/2 permanent à 0 Défenseur quand m(r)=0 ; Rive Piège exige toujours 2 Défenseurs). Les jetons Machine révélés restent visibles devant leur rayon jusqu’à la Furtivité (inclinés à 90° si Étouffés). m(r) = jetons Machine visibles devant r + Ratissages de r.",
    "A04": "Gouvernance unitaire : chaque Tuile de Synergie est décidée par son Peuple d’origine ; la pose de Piège en Furtivité par le propriétaire du rayon ; le Bouclier de lisière facultatif par le joueur Insectes (I).",
    "A05": "Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; zéro Insecte réservé d’avance.",
    "A06": "Pièges autonomes SINGLE_STRIKE & Croc : max 1 Piège ordinaire par parcelle (pare 1 frappe même à 0 Défenseur/Insecte, allume PIEGEAGE, défaussé aussitôt) ; le Croc Reptile peut cohabiter, pare en premier puis retourne dans la réserve Reptile.",
    "A07": "Zéro verrouillage d’avance & Zéro mémoire cachée : dé retiré sitôt la mobile Étouffée ou son attaque terminée ; Défenseurs couchés sur Rêve résolu ; tant qu’un Insecte ou un Piège est sur le plateau, il reste librement utilisable.",
    "A08": "Pont routier : une parcelle est une case non-Route ; les Routes Forestières sont sautées radialement et infranchissables latéralement.",
    "A09": "Repli sur création de Route et plafond En avançant : recul vers la bordure par défaut, ou d’1 parcelle vers le cœur si la bordure est rasée ; cette poussée vers le cœur couvre et remplace l’avancée finale d’une action En avançant (jamais de double bond +2).",
    "A10": "Dotation finie 10×N recto-verso, départ décalé & Ratissage physique : 10×N pions Arbre/Souche sans réserve illimitée ; Bulldozer p=1 / Abatteuse p=2 ; Abatteuse retourne tous les Arbres sans toucher aux Souches ; au ménage, toute machine sur la dernière parcelle glisse son jeton Machine sous elle (hors sac), conserve ses jetons Puissance et gagne +1 jeton rouge physique (convertible en bleu ; 0 bonus imprimé ; immobile mais parcelle ciblée ; Étouffée = tournée à 90° jusqu’au ménage).",
    "A11": "Réglette fixe 1–6, bandelette d’Acte réversible et fil d’ouverture imprimé : bandelette retournée seule au début du Tour 5 sans déplacer ni Rêves ni Insectes ; fil d’ouverture imprimé 1→4 ; un Rêve construit se pose au-dessus du rang libre le plus à droite (6, 5…).",
    "A12": "Piste des Gardiens directe à 6 icônes (zéro balayage) : [PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE], sans numéros visibles. Seule l’icône allumée par l’événement s’active immédiatement ; si cette vague vide le dessus d’au moins un Gardien (dernier pari glissé en encoche lors d’une vraie activation, exclu sur glissement passif), Résonance s’allume une seule fois pour cette vague sans boucler sur elle-même.",
    "A13": "Deux encoches visibles par Gardien et Faces 2 autonomes : ≥ 1 pion encore sur la tuile = pari perdu ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche = aucune mise (reste en place sans évoluer).",
    "A14": "Éveil de la Forêt cumulatif en piste (Module Gardiens) : actif si A ≥ 1 Animal Sauvage joue, aux Tours 1–7 (priorité Tour 8, puis Sommeil), remporté dès qu’au moins A + 1 Gardiens en piste sont sur leur Face 2 (2/2 à A=1, 3/4 à A=2, 4/6 à A=3) ET qu’aucun pari de Gardien n’a été perdu à ce tour (Bouclier de lisière préserve la Face 2 pour la suite mais laisse le pari perdu à ce tour).",
    "A15": "Fins de partie & Enracinement sur Rive Sabotage : priorité absolue Tour 8 ; Tours 1–7 Sommeil (tous les Rêves en bloc contigu 1..k, impossible si un Rêve est enraciné hors R1) avant Éveil cumulatif ; au décompte final, chaque tuile enracinée sur la Rive Sabotage de son rayon y retourne 1 Souche survivante (F1/unique) ou 2 Souches (F2) en Arbres debout, librement choisies parmi les parcelles survivantes de son rayon.",
    "A16": "Zéro écrasement au contact hors Route : le déplacement d’une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d’une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel/ponte en réserve).",
    "A17": "Module Essaim clos sur I : jetons Insectes exclusifs aux 10 tuiles des 5 lisières de I (laissés dans la boîte sans I). Quand I joue : Déploiement direct à la Production, Amorçage natif en réserve si 0 Insecte en jeu, Déménagement unifié des Nids (Insectes + Défenseurs + ponte), Déviation ±1, Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d’un Insecte passager.",
    "A18": "Production des Nids à Déploiement direct (Module Essaim) : bloc indivisible (+1 si 0–1 présent / +2 si ≥ 2 présents sans allumer INSECTE ; chaque Insecte créé est posé au choix sur ce Nid, sur une parcelle adjacente de son rayon en sautant les Routes, ou depuis la dernière parcelle sur un rang 1–6 ou une icône Gardien ; puis pouvoir propre du Nid).",
    "A19": "Parcelles ciblées figées au début de l’activation d’une machine : toute cible devenue Route entre-temps est annulée sans report ; une machine en Ratissage non Étouffée rend sa parcelle ciblée tant qu’elle n’a pas frappé ce tour.",
    "A20": "Accessoires 3 + 3 épurés : actifs Tour 1 (H Tambour/Chant, M Duel unifié retourné sur Territoire tenu par toute parade ou piège de tout moyen, O Perchoir de Vigie orientable Chaud/Calme + choix libre parmi ses 2 dés) et progressifs via tuiles (E Altération max 1/mobile, R 4 Écailles + Croc + cale exclusive du Caïman noir, I Module Essaim).",
    "A21": "Fil d’ouverture imprimé (1→4) & Sabotage différé : (1) Altérations → (2) Sabotages ordinaires (allume SABOTAGE + Refroidir sinon Reculer 1 machine de son rayon ou d’un voisin) & Écailles (allume SABOTAGE + pose Croc) → (3) Déviations ±1 (allume INSECTE) → (4) Rêves défendus de gauche à droite (le propriétaire Étouffe 1 machine/Défenseur, résout le pouvoir du Rêve actif même à 0 machine hors mention contraire, couche ses Défenseurs à plat, puis allume REVE si ≥ 1 machine Étouffée). Défenseurs solidaires lors de tout glissement.",
    "A22": "Légalité des poses & Bâtisseurs (Bonus 3J unifié) : interdit de compléter une tuile impossible à placer ; repli 1re pose sur parcelle alliée si aucun emplacement légal ; sitôt construite, les 2 bâtisseurs sont couchés en attente devant leur propriétaire — sauf à 3 joueurs où construire un Gardien, un Rêve ou un Nid libère immédiatement 1 bâtisseur vers une parcelle adjacente.",
    "A23": "Seuil de Parade unifié & Gain Charge : en Mode Charge, seuls les jetons rouges sont ignorés ; les jetons bleus Surchauffe (−1) s’appliquent dans TOUS les modes (Charge, Assaut, Ratissage), −1 aux rangs 3 et 6, minimum 1. Gain Charge = +1 rouge max/activation dès qu’au moins 1 frappe réelle non-Route n’est ni parée ni piégée.",
    "A24": "Sac opaque & pénurie : 2N jetons Machine + Sabotages + max 4 Écailles dans un sac en tissu opaque ; non piochés cachés ; pénurie distribuée en sens horaire depuis le Coordonnateur avec Oiseau toujours servi en dernier (regarde jusqu’à 2 jetons, garde 1 et pose l’autre sur son Perchoir de Vigie).",
    "A25": "Séquence des attaques : dés restants sur les rangs 1..6 de la Réglette (retirés sitôt l’attaque achevée) puis machines en Ratissage non Étouffées ; Abatteuse avant Bulldozer sur un même rayon ; chaque machine résolue d’un seul tenant."
  },
  "invariants_physiques_ids": [
    "INV-01",
    "INV-02",
    "INV-03",
    "INV-04",
    "INV-05",
    "INV-06",
    "INV-07",
    "INV-08",
    "INV-09",
    "INV-10",
    "INV-11",
    "INV-12",
    "INV-13",
    "INV-14",
    "INV-15",
    "INV-16",
    "INV-17",
    "INV-18",
    "INV-19",
    "INV-20",
    "INV-21",
    "INV-22"
  ],
  "six_verbes_du_coeur": {
    "REFROIDIR": {
      "verbe": "Refroidir",
      "definition": "Retourner 1 jeton Rouge existant d’une machine (mobile ou en Ratissage) sur sa face Bleu Surchauffe (−1 dans tous les modes ; jamais de Bleu posé à sec depuis la réserve)."
    },
    "ALTERER": {
      "verbe": "Altérer",
      "definition": "Poser 1 jeton d’Altération de la réserve Entités sur une machine mobile qui n’en porte pas encore (max 1 par machine ; jamais sur une machine en Ratissage)."
    },
    "RECULER": {
      "verbe": "Reculer",
      "definition": "Déplacer une machine mobile d’1 parcelle vers la bordure de son rayon en sautant les Routes Forestières (sans sortir du plateau ; sans effet sur une machine en Ratissage)."
    },
    "ETOUFFER": {
      "verbe": "Étouffer",
      "definition": "Neutraliser toute l’activation restante d’une machine à ce tour : incliner son jeton Machine mobile à 90° devant son rayon et retirer immédiatement son dé de la Réglette, ou tourner une machine en Ratissage à 90° sur place jusqu’au ménage. Annuler une machine via un Rêve revient à l’Étouffer. Le mot « cale » est 100 % exclusif au jeton glissé sous une machine mobile par Le Caïman noir."
    },
    "SEMER_AU_SAC": {
      "verbe": "Semer au sac",
      "definition": "Glisser 1 jeton disponible (Sabotage ordinaire ou Écaille) dans le sac opaque sans allumer d’icône."
    },
    "GLISSER_UN_REVE": {
      "verbe": "Glisser un Rêve",
      "definition": "Déplacer une tuile Rêve sur la Réglette 1–6 en emportant ses Défenseurs dans leur état actuel (debout si encore à résoudre, couchés si déjà résolu)."
    }
  }
};

const REFERENTIEL_PICTOGRAMMES_V6_4 = {
  "PIC_ARBRE": {
    "code": "PIC_ARBRE",
    "categorie": "FORET",
    "libelle": "Arbre debout",
    "symbole": "🌳"
  },
  "PIC_SOUCHE": {
    "code": "PIC_SOUCHE",
    "categorie": "FORET",
    "libelle": "Souche (retournable en Arbre)",
    "symbole": "🪵"
  },
  "PIC_ROUTE": {
    "code": "PIC_ROUTE",
    "categorie": "FORET",
    "libelle": "Route forestière",
    "symbole": "🛣️"
  },
  "PIC_ENRACINEMENT": {
    "code": "PIC_ENRACINEMENT",
    "categorie": "FORET",
    "libelle": "Enracinement volontaire",
    "symbole": "🌱"
  },
  "PIC_DEFENSEUR": {
    "code": "PIC_DEFENSEUR",
    "categorie": "DEFENSE",
    "libelle": "Défenseur",
    "symbole": "🛡️"
  },
  "PIC_DEFENSEUR_ATTENTE": {
    "code": "PIC_DEFENSEUR_ATTENTE",
    "categorie": "DEFENSE",
    "libelle": "Défenseur en attente (bâtisseur / rive / Rêve)",
    "symbole": "♻️"
  },
  "PIC_PIEGE": {
    "code": "PIC_PIEGE",
    "categorie": "DEFENSE",
    "libelle": "Piège autonome",
    "symbole": "🪤"
  },
  "PIC_CROC": {
    "code": "PIC_CROC",
    "categorie": "ACCESSOIRES",
    "libelle": "Croc Reptile (réutilisable)",
    "symbole": "🦷"
  },
  "PIC_SABOTAGE": {
    "code": "PIC_SABOTAGE",
    "categorie": "SAC",
    "libelle": "Jeton Sabotage (sac opaque)",
    "symbole": "💥"
  },
  "PIC_ECAILLE": {
    "code": "PIC_ECAILLE",
    "categorie": "ACCESSOIRES",
    "libelle": "Jeton Sabotage Écaille (Reptiles)",
    "symbole": "🦎"
  },
  "PIC_DES_PARAVENT": {
    "code": "PIC_DES_PARAVENT",
    "categorie": "SAC",
    "libelle": "Dés lancés sous paravent",
    "symbole": "🎲"
  },
  "PIC_ROUGE": {
    "code": "PIC_ROUGE",
    "categorie": "MACHINES",
    "libelle": "Jeton Puissance Rouge (+1)",
    "symbole": "🔴"
  },
  "PIC_BLEU": {
    "code": "PIC_BLEU",
    "categorie": "MACHINES",
    "libelle": "Jeton Surchauffe Bleu (−1 tous modes)",
    "symbole": "🔵"
  },
  "PIC_RECUL": {
    "code": "PIC_RECUL",
    "categorie": "MACHINES",
    "libelle": "Recul de machine (−1 parcelle)",
    "symbole": "⏪"
  },
  "PIC_CALE": {
    "code": "PIC_CALE",
    "categorie": "ACCESSOIRES",
    "libelle": "Cale sous machine mobile (exclusif Caïman noir)",
    "symbole": "🧱"
  },
  "PIC_ALTERATION": {
    "code": "PIC_ALTERATION",
    "categorie": "ACCESSOIRES",
    "libelle": "Jeton Altération (Entités)",
    "symbole": "🌀"
  },
  "PIC_RANG_MACHINE": {
    "code": "PIC_RANG_MACHINE",
    "categorie": "PISTE_TACTIQUES",
    "libelle": "Rang de machine sur la Réglette 1–6",
    "symbole": "🔢"
  },
  "PIC_REVE": {
    "code": "PIC_REVE",
    "categorie": "PISTE_TACTIQUES",
    "libelle": "Tuile Rêve sur la Réglette 1–6",
    "symbole": "🌙"
  },
  "PIC_AVANCEE_REVE": {
    "code": "PIC_AVANCEE_REVE",
    "categorie": "PISTE_TACTIQUES",
    "libelle": "Glisser un Rêve sur la Réglette 1–6",
    "symbole": "⬅️"
  },
  "PIC_ANNULATION": {
    "code": "PIC_ANNULATION",
    "categorie": "PISTE_TACTIQUES",
    "libelle": "Étouffer une machine (jeton incliné 90°, dé retiré)",
    "symbole": "🚫"
  },
  "PIC_PARI_ENCOCHE": {
    "code": "PIC_PARI_ENCOCHE",
    "categorie": "PISTE_GARDIENS",
    "libelle": "Encoche / sécurisation de pari Gardien",
    "symbole": "⭐"
  },
  "PIC_RESONANCE": {
    "code": "PIC_RESONANCE",
    "categorie": "PISTE_GARDIENS",
    "libelle": "Icône Résonance (dernier pari glissé en encoche)",
    "symbole": "🔔"
  },
  "PIC_TAMBOUR": {
    "code": "PIC_TAMBOUR",
    "categorie": "ACCESSOIRES",
    "libelle": "Chamane Tambour (Humains)",
    "symbole": "🥁"
  },
  "PIC_CHANT": {
    "code": "PIC_CHANT",
    "categorie": "ACCESSOIRES",
    "libelle": "Chamane Chant (Humains)",
    "symbole": "🎶"
  },
  "PIC_DUEL": {
    "code": "PIC_DUEL",
    "categorie": "ACCESSOIRES",
    "libelle": "Jeton Duel — Défi / Territoire tenu (Mammifères)",
    "symbole": "⚔️"
  },
  "PIC_PERCHOIR": {
    "code": "PIC_PERCHOIR",
    "categorie": "ACCESSOIRES",
    "libelle": "Perchoir de Vigie — Chaud / Calme & jeton caché (Oiseaux)",
    "symbole": "🦅"
  },
  "PIC_INSECTE": {
    "code": "PIC_INSECTE",
    "categorie": "ESSAIM",
    "libelle": "Jeton Insecte (exclusif lisières de I)",
    "symbole": "🐜"
  },
  "PIC_NID": {
    "code": "PIC_NID",
    "categorie": "ESSAIM",
    "libelle": "Nid de l’Essaim (exclusif lisières de I)",
    "symbole": "🪹"
  },
  "PIC_MIGRATION": {
    "code": "PIC_MIGRATION",
    "categorie": "ESSAIM",
    "libelle": "Déplacement / phorésie de l’Essaim",
    "symbole": "➡️"
  },
  "PIC_LOI_PASSIVE": {
    "code": "PIC_LOI_PASSIVE",
    "categorie": "ACTION",
    "libelle": "Loi passive permanente",
    "symbole": "⚖️"
  },
  "PIC_TWIST": {
    "code": "PIC_TWIST",
    "categorie": "ACTION",
    "libelle": "Brique-Twist 2K3",
    "symbole": "⚡"
  }
};

const CANON_V6_4 = {
  "_meta": {
    "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.4 (Passe 2 Affinée, 30 Tuiles Bi-Composant)",
    "schema_version": "6.4.0",
    "socle_verrouille": "6.4.0",
    "cadrage_source": "docs/cadrage_v6_4.md",
    "etape_active": "JALON_5_ENCODAGE_30_TUILES_V6_4",
    "statut_global": "ACTIVE_VERIFIED",
    "genere_le": "2026-11-27",
    "slots_count": 30,
    "c02_supprime": true,
    "panel_id": "canon_v6_4",
    "murs_porteurs_verrouilles": [
      "M1_TEMPS_BATAILLE",
      "M2_CONSERVATION_THERMIQUE",
      "M3_INTEGRITE_PLATEAU_ET_ICONES",
      "M4_AUTONOMIE_PLANCHER_SOLO"
    ],
    "note_phase_a": "Catalogue Passe 2 v6.4.0 consolidé sur les 9 évolutions du Cœur v6.4 et les 6 Verbes du Cœur. Archive Passe 1 conservée sur le tag archive/v6.3.2-panel-passe1 et dans contracts/tiles_canon_v6_3.json ; noyau PyPy v6.2 sanctuarisé jusqu'au Jalon 4."
  },
  "carte_des_roles": {
    "statut": "CONSOLIDE_PASSE_2_V6_4",
    "roles": {
      "catalyseurs_eveil": [
        "G1=M>R",
        "G3=M>O",
        "G4=O>M",
        "G5=R>O",
        "G6=O>R",
        "G8=M>E",
        "G9=R>H",
        "G10=R>E",
        "G11=O>H",
        "G12=O>E",
        "G13=M>I",
        "G14=R>I",
        "G15=O>I"
      ],
      "leviers_reve": [
        "G8=M>E",
        "R1=H>E",
        "R4=H>R",
        "R8=E>R",
        "R9=E>O",
        "R10=E>I"
      ],
      "synergies_enracinement": [
        "G7=M>H",
        "G15=O>I",
        "R1=H>E",
        "R2=E>H"
      ],
      "lois_passives": [
        "R7=E>M",
        "R8=E>R",
        "M5=I>E"
      ],
      "autonomie_A0": [
        "R1=H>E",
        "R2=E>H",
        "R6=H>I",
        "R10=E>I",
        "M4=I>H",
        "M5=I>E"
      ],
      "twists_2K3": [
        "G2=R>M",
        "G7=M>H",
        "G12=O>E",
        "R4=H>R",
        "R10=E>I",
        "M3=I>O"
      ]
    }
  },
  "rapport_audit_197": {
    "verdict_global": "OK",
    "schema_source": "v6.4",
    "c02_word_count_purged": true,
    "assises_verifiees": 197,
    "compositions_verifiees": 42,
    "murs_porteurs": {
      "M1_TEMPS_BATAILLE": "OK",
      "M2_CONSERVATION_THERMIQUE": "OK",
      "M3_INTEGRITE_PLATEAU_ET_ICONES": "OK",
      "M4_AUTONOMIE_PLANCHER_SOLO": "OK"
    },
    "compteurs": {
      "catalyseurs_eveil": 13,
      "leviers_reve": 6,
      "synergies_enracinement": 4,
      "lois_passives": 3,
      "max_lois_par_assise": 2,
      "twists_2K3": 6,
      "autonomie_A0": 6
    },
    "erreurs": 0
  },
  "tuiles_ciblees": {
    "G1": {
      "id": "G1",
      "alias_oriente": "M>R",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "R",
      "couple": [
        "M",
        "R"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Duel (M) + Croc (R) → embuscade sur la parcelle du Duel → Piégeage en cascade · Face 2 : Refroidit la machine parée",
      "entrees_plancher": [
        "DUEL",
        "CROC"
      ],
      "entrees_synergie": [
        "ROUGE"
      ],
      "entrees": [
        "DUEL",
        "CROC",
        "ROUGE"
      ],
      "sorties": [
        "CROC_POSTE",
        "CROC",
        "TERRITOIRE",
        "BLEU"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume Piégeage (l’icône du Jaguar) et retourne le Duel sur Territoire tenu (règle native), ouvrant une seconde activation qui reposte aussitôt le Croc pour la frappe suivante.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Jaguar",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_CROC",
          "PIC_DUEL",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Croc → parcelle du Duel · sinon Duel sur parcelle ciblée puis Croc dessus",
          "face_2": "Croc (+ Duel) → toute parcelle ciblée · parade du Croc = Refroidir 1 Rouge",
          "enracine": null
        },
        "resume_plateau": "Poste le Croc aux côtés du Duel"
      },
      "carte_joueur": {
        "titre_complet": "Le Jaguar, seigneur des berges",
        "entite_illustree": "Le Jaguar (Panthera onca) — grand félin tacheté, animal entier sur une plage de sable noir du rio, surgissant des herbes vers un caïman qui se chauffe",
        "brief_illustration": "Plan large crépusculaire sur une berge de várzea : le Jaguar entier, musculature tendue, rosettes nettes, avance à demi immergé dans l’eau noire ; au premier plan, une gueule de caïman entrouverte (évocation du Croc) ; au fond, des troncs coupés et la lueur orangée d’une machine. Palette ocre, vert profond, reflets d’or sur l’eau.",
        "pitch_ambiance": "Le Jaguar ne craint ni l’eau ni les écailles : il chasse le caïman sur sa propre berge et le tue d’une seule morsure au crâne. Là où il rôde, la rive appartient de nouveau à la forêt.",
        "texte_regle": {
          "face_1": "Prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et posez-le sur la parcelle du jeton Duel. Si le Duel est en réserve, posez d’abord le Duel face Défi sur une parcelle ciblée de votre choix, puis posez le Croc dessus.",
          "face_2": "Même effet, mais vous pouvez poser le Croc — et, au choix, déplacer le Duel avec lui en conservant sa face — sur n’importe quelle parcelle ciblée du plateau. Chaque fois que le Croc pare une attaque à ce tour, Refroidissez cette machine si elle porte au moins 1 jeton Rouge.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Poste le Croc sur la parcelle du Duel (ou sur toute cible en Face 2) et Refroidit l’attaquante.",
          "renoncement": "Mobilise l’unique Croc sur une seule parcelle ; le Croc n’est plus libre pour les pontes ou une autre embuscade tant qu’il n’a pas paré."
        }
      },
      "temoins": [
        {
          "id": "G1_T1",
          "statut": "OK",
          "resume": "Duel face Défi sur M·2 ; Jaguar F1 pose le Croc (pris en réserve Reptile) sur M·2 ; la frappe parée par le Croc allume Piégeage et retourne nativement le Duel sur Territoire tenu."
        },
        {
          "id": "G1_T2",
          "statut": "OK",
          "resume": "Jaguar F2 déplace Duel + Croc sur une parcelle ciblée d’un rayon voisin ; la machine parée par le Croc est immédiatement Refroidie (1 Rouge → Bleu)."
        }
      ],
      "heuristique_bot": "Prioritaire dès qu’une parcelle ciblée porte le Duel ou une attaque à fort Seuil ; en Face 2, combine Piégeage en boucle et Refroidissement sur machine chargée.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G2": {
      "id": "G2",
      "alias_oriente": "R>M",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "M",
      "couple": [
        "R",
        "M"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Territoire tenu ou 2 Défenseurs → machine arrachée au Ratissage (jeton au sac + Reculer) · Face 2 : Étouffer et Reculer une mobile",
      "entrees_plancher": [
        "RATISSAGE",
        "DUEL"
      ],
      "entrees_synergie": [
        "TERRITOIRE"
      ],
      "entrees": [
        "RATISSAGE",
        "DUEL",
        "TERRITOIRE"
      ],
      "sorties": [
        "RATISSAGE_ROMPU",
        "RECUL",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": "Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la dernière parcelle : deux activations arrachent successivement l’Abatteuse puis le Bulldozer, ou combinent arrachage et Étouffement d’une mobile en Face 2.",
      "tags": [
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "L’Anaconda vert",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_DUEL",
          "PIC_RECUL",
          "PIC_ANNULATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Ratissage sur Territoire tenu OU 2 Défenseurs → jeton au sac · Reculer 1",
          "face_2": "Duel OU 2 Défenseurs → rompt Ratissage OU Étouffe et Recule 1 mobile",
          "enracine": null
        },
        "resume_plateau": "Arrache une machine à son Ratissage"
      },
      "carte_joueur": {
        "titre_complet": "L’Anaconda vert, l’étau des eaux dormantes",
        "entite_illustree": "L’Anaconda vert (Eunectes murinus) — serpent géant entier, anneaux olive tachetés de noir, enroulé dans les eaux d’un igapó",
        "brief_illustration": "Vue semi-immergée : l’Anaconda vert entier, anneaux déroulés sous la surface, enserre les chenilles d’une machine de déboisement à demi engloutie ; sur la berge, les empreintes fraîches d’un jaguar. Lumière verte filtrée, eau sombre et miroitante.",
        "pitch_ambiance": "L’Anaconda attend des heures, invisible sous la lentille d’eau. Quand la proie s’aventure au bord, chaque expiration resserre ses anneaux, et il l’entraîne là où plus rien ne pousse : au fond.",
        "texte_regle": {
          "face_1": "Choisissez une machine en Ratissage dont la parcelle porte le Duel sur sa face Territoire tenu ou au moins 2 Défenseurs : elle quitte immédiatement son Ratissage, son jeton Machine retourne dans le sac opaque (elle perd son éventuel jeton Rouge de Ratissage s’il peut être retiré, en conservant ses autres jetons), et vous la faites Reculer d’1 parcelle vers la bordure. S’il n’y a aucune machine en Ratissage éligible, choisissez une machine mobile visant la parcelle du Duel ou une parcelle portant au moins 2 Défenseurs et faites-la Reculer d’1 parcelle.",
          "face_2": "Même effet dès que la parcelle porte le Duel (quelle que soit sa face) ou au moins 2 Défenseurs ; de plus, vous pouvez choisir à la place une machine mobile active visant cette parcelle pour l’Étouffer et la faire Reculer d’1 parcelle vers la bordure.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Rompt un Ratissage (ou fait Reculer / Étouffe une machine mobile sur parcelle verrouillée).",
          "renoncement": "Remet le jeton Machine dans le sac opaque et exige de concentrer 2 Défenseurs ou le Duel sur la parcelle menacée."
        }
      },
      "temoins": [
        {
          "id": "G2_T1",
          "statut": "OK",
          "resume": "Abatteuse en Ratissage sur la dernière parcelle portant Territoire tenu : Anaconda F1 la sort du Ratissage, remet son jeton au sac et la fait Reculer d’1 parcelle."
        },
        {
          "id": "G2_T2",
          "statut": "OK",
          "resume": "Anaconda F2 sur une mobile active visant la parcelle du Duel : la machine est Étouffée (jeton à 90°, dé retiré) et Recule d’1 parcelle."
        }
      ],
      "heuristique_bot": "Prioritaire dès qu’une machine entre en Ratissage sur une parcelle défendue ou tenue par le Duel ; en Face 2, neutralise directement la mobile la plus dangereuse.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G3": {
      "id": "G3",
      "alias_oriente": "M>O",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "O",
      "couple": [
        "M",
        "O"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Arbres debout + Routes + Perchoir (O) → traversée haute et Saut de lisière (Rive ↔ Arbre) → redéploiement instantané de Parade",
      "entrees_plancher": [
        "ARBRE",
        "ROUTE",
        "DEFENSEUR_REDEPLOYE"
      ],
      "entrees_synergie": [
        "PERCHOIR"
      ],
      "entrees": [
        "ARBRE",
        "ROUTE",
        "DEFENSEUR_REDEPLOYE",
        "PERCHOIR"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Deux traversées amènent les deux Défenseurs nécessaires à une Parade décisive, ou basculent un pion d’une Rive de Furtivité vers le cœur puis un autre vers une Rive.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "L’Atèle",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_ARBRE",
          "PIC_ROUTE",
          "PIC_DEFENSEUR",
          "PIC_PERCHOIR"
        ],
        "mots_cles_plateau": {
          "face_1": "2 cimes même profondeur (M ↔ O) OU Rive ↔ cime · 1 pas avant",
          "face_2": "Rayon du Perchoir ↔ voisins · Rive ↔ cime · 1 pas avant et après",
          "enracine": null
        },
        "resume_plateau": "Fait traverser un Défenseur par la cime"
      },
      "carte_joueur": {
        "titre_complet": "L’Atèle, acrobate des hautes cimes",
        "entite_illustree": "Atèle dans la canopée",
        "brief_illustration": "Atèle entier suspendu par la queue entre deux couronnes. En contrebas, une trouée coupe le chemin radial.",
        "pitch_ambiance": "L’atèle essaie le poids d’une branche avant de lâcher la précédente. Au-dessous de lui, le chemin a disparu.",
        "texte_regle": {
          "face_1": "Déplacez 1 Défenseur entre deux parcelles de même profondeur portant un Arbre debout, situées sur le rayon Mammifères et le rayon Oiseaux (en sautant les Routes intermédiaires). Avant la traversée, ce Défenseur peut faire 1 pas sur son rayon de départ. Saut de lisière : l’une des deux extrémités (départ ou arrivée) peut être une Rive de Furtivité de ces deux rayons, l’autre devant rester une parcelle portant un Arbre debout.",
          "face_2": "Même effet entre le rayon désigné par le Perchoir de Vigie (ou le rayon Oiseaux si le Perchoir pointe un rang) et l’un de ses rayons voisins, avec jusqu’à 1 pas avant la traversée et 1 pas après (y compris en Saut de lisière depuis ou vers une Rive de Furtivité de ces rayons).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Redéploie un Défenseur entre rayons ou entre une Rive de Furtivité et la canopée pour compléter une Parade ou une Rive.",
          "renoncement": "Quitter une Rive ou un rayon fragilise la défense ou le contrôle de Furtivité laissé derrière soi."
        }
      },
      "temoins": [
        {
          "id": "G3_T1",
          "statut": "OK",
          "resume": "Saut de lisière F1 : un Défenseur sur la Rive Sabotage de O traverse directement sur une parcelle à Arbre debout de M pour compléter une Parade."
        },
        {
          "id": "G3_T2",
          "statut": "OK",
          "resume": "Atèle F2 avec Perchoir au pied d’un rayon voisin : 1 pas avant, traversée entre cimes, puis 1 pas après pour atteindre exactement la parcelle menacée."
        }
      ],
      "heuristique_bot": "Évalue chaque Défenseur excédentaire ou sur Rive déjà gagnée/perdue pour compléter une Parade à manque de 1 ou sécuriser une Rive 2/2.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G4": {
      "id": "G4",
      "alias_oriente": "O>M",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "M",
      "couple": [
        "O",
        "M"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Pari Gardien → glissement en encoche (F1) ou activation en relais (F2) · Second cri gratuit sur icône voisine OU Territoire tenu → Défi",
      "entrees_plancher": [
        "GARDIEN"
      ],
      "entrees_synergie": [
        "TERRITOIRE"
      ],
      "entrees": [
        "GARDIEN",
        "TERRITOIRE"
      ],
      "sorties": [
        "PARI_GLISSE",
        "ACTIVATION_RELAIS",
        "DEFI"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_RESONANCE"
      ],
      "double_ouverture": "Deux activations font boucler un Gardien à 2 paris sur une icône silencieuse ou déclenchent un relais en chaîne en Face 2 ; dès qu’une activation vide le dernier pari d’un Gardien en Face 2, la Résonance se déclenche.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "L’Ara rouge",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_RESONANCE",
        "pictogrammes": [
          "PIC_PARI_ENCOCHE",
          "PIC_RESONANCE",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "1 pari tiers → encoche · Second cri si icône voisine OU Territoire → Défi",
          "face_2": "Active 1 Gardien tiers avec pari · Second cri si icône voisine OU Territoire → Défi",
          "enracine": null
        },
        "resume_plateau": "Fait avancer ou réveille d’autres Gardiens"
      },
      "carte_joueur": {
        "titre_complet": "L’Ara rouge, sentinelle de la collpa",
        "entite_illustree": "L’Ara rouge (Ara macao), animal entier agrippé à une falaise d’argile",
        "brief_illustration": "L’Ara rouge (Ara macao), animal entier : perroquet écarlate, jaune et bleu, agrippé à une falaise d’argile (collpa) au milieu de sa volée, le bec ouvert sur le cri d’alarme.",
        "pitch_ambiance": "À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.",
        "texte_regle": {
          "face_1": "Glissez 1 pari d’un autre Gardien en piste dans son encoche libre (sans déclencher son pouvoir ni allumer la Résonance). Second cri : si ce premier Gardien siège sur une icône directement voisine de celle de l’Ara rouge sur la Piste — ou si vous retournez le jeton Duel de sa face Territoire tenu sur sa face Défi —, répétez cet effet sur un second Gardien (ou une seconde fois sur le même). Sentinelle seule : s’il n’y a aucun autre Gardien avec pari en piste, glissez aussitôt un second pari de l’Ara rouge lui-même dans son encoche.",
          "face_2": "Activez immédiatement en relais 1 autre Gardien en piste portant au moins 1 pari (il glisse 1 pari en encoche et résout son pouvoir, pouvant allumer la Résonance s’il glisse ainsi son dernier pari). Le Second cri (gratuit sur une icône directement voisine de l’Ara rouge, ou en retournant Territoire tenu sur Défi) et le repli Sentinelle seule s’appliquent à l’identique.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Sécurise (F1) ou réveille en relais (F2) jusqu’à deux Gardiens ; récompense le placement sur des icônes voisines ou la dépense de Territoire tenu.",
          "renoncement": "En Face 1, sécuriser un pari renonce au pouvoir actif de ce Gardien et ne déclenche pas la Résonance."
        }
      },
      "temoins": [
        {
          "id": "G4_T1",
          "statut": "OK",
          "resume": "Ara F1 sur Résonance (position 6) choisit un Gardien sur Insecte (position 5, directement voisine) : 1 pari glisse sans pouvoir ni Résonance, et Second cri est gratuit pour un second Gardien."
        },
        {
          "id": "G4_T2",
          "statut": "OK",
          "resume": "Ara F2 active en relais un Gardien sur son dernier pari : ce Gardien résout son pouvoir, vide son dessus et allume Résonance."
        }
      ],
      "heuristique_bot": "Maximise le taux de passage Face 2 des Gardiens en piste ; privilégie un premier choix sur une icône adjacente à l’Ara pour obtenir le Second cri gratuitement.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G5": {
      "id": "G5",
      "alias_oriente": "R>O",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "O",
      "couple": [
        "R",
        "O"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Perchoir de Vigie (O) → Piège sur la zone guettée (sinon R ou O) · Bleu bu → Croc (F1) ou second plongeon (F2) → Piégeage en boucle",
      "entrees_plancher": [
        "PERCHOIR"
      ],
      "entrees_synergie": [
        "BLEU"
      ],
      "entrees": [
        "PERCHOIR",
        "BLEU"
      ],
      "sorties": [
        "PIEGE",
        "CROC"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Chaque Piège ou Croc qui pare allume Piégeage (l’icône de l’Iguane) : deux chutes couvrent les deux parcelles d’un En avançant, ou boivent un Bleu pour déclencher Croc ou double plongeon.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "L’Iguane vert",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_PIEGE",
          "PIC_PERCHOIR",
          "PIC_CROC",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Piège sur cible du Perchoir (sinon R OU O) · Bleu bu = Croc aussi",
          "face_2": "Piège + Croc partout · Bleu bu = second plongeon",
          "enracine": null
        },
        "resume_plateau": "Tombe en Piège sous le Perchoir"
      },
      "carte_joueur": {
        "titre_complet": "L’Iguane vert, dormeur des hautes branches",
        "entite_illustree": "L’Iguane vert (Iguana iguana), animal entier allongé sur une branche au-dessus de l’eau",
        "brief_illustration": "L’Iguane vert (Iguana iguana), animal entier : grand lézard à la crête dorsale dressée, allongé au soleil sur une branche au-dessus de l’eau, l’œil tourné vers un oiseau qui donne l’alerte.",
        "pitch_ambiance": "L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.",
        "texte_regle": {
          "face_1": "Posez 1 Piège ordinaire disponible sur une parcelle ciblée libre de Piège désignée par le Perchoir de Vigie (sur son rayon s’il est au pied d’un rayon, ou sur une parcelle visée par une machine du rang qu’il pointe ; à défaut, sur le rayon Reptiles ou le rayon Oiseaux). Si cette machine porte au moins 1 jeton Bleu Surchauffe, vous pouvez en défausser 1 (l’Iguane boit la fraîcheur) pour poser aussi le Croc disponible depuis la réserve Reptile sur une autre parcelle ciblée de votre choix.",
          "face_2": "Même effet sur n’importe quelle parcelle ciblée du plateau, et vous posez aussi le Croc disponible sur une seconde parcelle ciblée. Si vous buvez 1 jeton Bleu d’une machine visée, résolvez un second plongeon (1 Piège supplémentaire sur une autre parcelle ciblée libre).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Pose un Piège chirurgical guidé par le Perchoir et peut convertir un Bleu ennemi en Croc (F1) ou en double plongeon (F2).",
          "renoncement": "Boire un Bleu rend sa pleine puissance à la machine qui le portait si elle survit au piégeage."
        }
      },
      "temoins": [
        {
          "id": "G5_T1",
          "statut": "OK",
          "resume": "Perchoir pointant le rang 4 : Iguane F1 pose 1 Piège sur la parcelle ciblée par la machine du rang 4 ; si elle porte un Bleu, boire ce Bleu pose aussi le Croc de la réserve."
        },
        {
          "id": "G5_T2",
          "statut": "OK",
          "resume": "Iguane F2 pose Piège + Croc sur deux parcelles ciblées de son choix, puis boit 1 Bleu pour effectuer un second plongeon."
        }
      ],
      "heuristique_bot": "Cible les parcelles à plus fort Seuil sans Défenseur ; boit un Bleu uniquement sur une machine déjà piégée ou facile à parer afin de multiplier les déclenchements de Piégeage.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G6": {
      "id": "G6",
      "alias_oriente": "O>R",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "R",
      "couple": [
        "O",
        "R"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Perchoir (O) + Rouge → Refroidir · Cri de vapeur (0 Rouge restant OU 0 Rouge éligible) → allume 1 icône à droite sur la Piste · Face 2 : Étouffer à 0 Rouge et ≥ 2 Bleus",
      "entrees_plancher": [
        "ROUGE",
        "PERCHOIR"
      ],
      "entrees_synergie": [
        "BLEU"
      ],
      "entrees": [
        "ROUGE",
        "PERCHOIR",
        "BLEU"
      ],
      "sorties": [
        "BLEU",
        "ANNULATION_SURCHAUFFE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE",
        "ICONE_SABOTAGE",
        "ICONE_REVE"
      ],
      "double_ouverture": "Assis sur Parade, la première activation Refroidit une machine et, si elle tombe à 0 Rouge (ou sans cible Rouge), le Cri de vapeur allume une icône située à droite du Toucan sur la Piste (hors Résonance) pour relancer d’autres Gardiens ; en Face 2, la seconde activation pousse une machine à 0 Rouge et ≥ 2 Bleus pour l’Étouffer.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Toucan toco",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_ROUGE",
          "PIC_BLEU",
          "PIC_PERCHOIR",
          "PIC_ANNULATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Refroidir sous le Perchoir (sinon O OU voisin) · 0 Rouge = allume 1 icône à droite",
          "face_2": "Refroidir partout · 0 Rouge et 2 Bleus = Étouffer · Cri de vapeur actif",
          "enracine": null
        },
        "resume_plateau": "Refroidit les machines et relance la Piste"
      },
      "carte_joueur": {
        "titre_complet": "Le Toucan toco, le bec-radiateur",
        "entite_illustree": "Le Toucan toco (Ramphastos toco) — oiseau entier au bec orange démesuré, perché au sommet d’un arbre émergent",
        "brief_illustration": "Contre-jour brûlant : le Toucan toco entier, bec orange incandescent, se découpe sur un ciel blanc de chaleur ; des volutes de chaleur partent de son bec vers une machine en contrebas dont les jauges virent au bleu ; un iguane se chauffe sur une branche voisine. Orange, noir, bleu électrique.",
        "pitch_ambiance": "Le bec du toucan toco est un radiateur vivant : il y dirige son sang pour relâcher la chaleur du jour. Au-dessus des machines brûlantes, il rend la fournaise au monde, et le métal s’essouffle.",
        "texte_regle": {
          "face_1": "Refroidissez 1 machine désignée par le Perchoir de Vigie (sur son rayon s’il est au pied d’un rayon, ou une machine du rang qu’il pointe ; à défaut, une machine du rayon Oiseaux ou d’un rayon voisin). Cri de vapeur : si cette machine n’a plus aucun jeton Rouge après ce Refroidissement — ou s’il n’y avait aucune machine éligible portant un jeton Rouge —, allumez immédiatement 1 icône de votre choix située strictement à droite de celle du Toucan toco sur la Piste des Gardiens (hors Résonance).",
          "face_2": "Même effet, mais vous pouvez Refroidir n’importe quelle machine du plateau (mobile ou en Ratissage). De plus, si la machine refroidie atteint 0 jeton Rouge et au moins 2 jetons Bleus Surchauffe, vous l’Étouffez immédiatement (le Cri de vapeur s’applique aussi).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Refroidit une machine ciblée pour réduire son Seuil (ou l’Étouffer en Face 2) et allume une icône à droite sur la Piste via le Cri de vapeur.",
          "renoncement": "Cibler une machine à 1 seul Rouge maximise le Cri de vapeur en piste, mais laisse intacte une machine à 2 ou 3 Rouges ailleurs."
        }
      },
      "temoins": [
        {
          "id": "G6_T1",
          "statut": "OK",
          "resume": "Toucan F1 assis sur Parade Refroidit la machine à 1 Rouge sous le Perchoir : elle passe à 0 Rouge et Cri de vapeur allume Piégeage (à droite de Parade, hors Résonance)."
        },
        {
          "id": "G6_T2",
          "statut": "OK",
          "resume": "Toucan F2 Refroidit partout une machine portant 1 Rouge et 1 Bleu : elle passe à 0 Rouge et 2 Bleus, est immédiatement Étouffée et déclenche Cri de vapeur."
        }
      ],
      "heuristique_bot": "Siège idéal sur Parade pour maximiser les icônes à droite ; priorise les machines à 1 Rouge (Cri de vapeur immédiat) ou à 1 Rouge + 1 Bleu en Face 2 (Étouffement).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G7": {
      "id": "G7",
      "alias_oriente": "M>H",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "H",
      "couple": [
        "M",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "TWIST_2K3",
        "ENRACINEMENT"
      ],
      "est_twist": true,
      "vecteurs": "Duel ou Chamane sur Route → Bourbier bloquant la 1re traversée/frappe · Frayer → Duel + Territoire tenu · Face 2 : Refroidir ou Reculer · Enraciné : +1 Souche finale",
      "entrees_plancher": [
        "ROUTE",
        "DUEL",
        "TAMBOUR",
        "CHANT"
      ],
      "entrees_synergie": [
        "CHAMANE_EN_FORET",
        "ROUGE"
      ],
      "entrees": [
        "ROUTE",
        "DUEL",
        "TAMBOUR",
        "CHANT",
        "CHAMANE_EN_FORET",
        "ROUGE"
      ],
      "sorties": [
        "BOURBIER_ROUTE",
        "TERRITOIRE",
        "BLEU",
        "RECUL",
        "ARBRE"
      ],
      "paiement": [
        "P_SOUCHE"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Deux activations installent un Bourbier sur une Route clé puis posent le Duel sur une parcelle ciblée (ou créent deux Bourbiers distincts avec Duel et Chamane) ; en Face 2, un Bourbier en Territoire tenu résiste à une première machine.",
      "tags": [
        "ENRACINEMENT",
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "Le Tapir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_ROUTE",
          "PIC_DUEL",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "Duel OU Chamane sur Route = Bourbier bloque 1re traversée OU Frayer Duel",
          "face_2": "Bourbier Refroidit (sinon Reculer 1) · Territoire tenu bascule sur Défi",
          "enracine": "Décompte final · Duel + Chamane = +1 Souche"
        },
        "resume_plateau": "Transforme les Routes en Bourbiers"
      },
      "carte_joueur": {
        "titre_complet": "Le Tapir, jardinier des sentiers",
        "entite_illustree": "Le Tapir terrestre (Tapirus terrestris), animal entier avançant dans un sentier de boue",
        "brief_illustration": "Le Tapir terrestre (Tapirus terrestris), animal entier : grand herbivore à la trompe mobile, robe brun sombre et courte crinière, qui avance au crépuscule dans un sentier de boue tracé en travers d’une trouée de bulldozer. Empreintes à quatre doigts dans la glaise ; à l’orée, un chamane suit la piste, tambour à la main.",
        "pitch_ambiance": "Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.",
        "texte_regle": {
          "face_1": "Choisissez : Fouler une Route — posez le jeton Duel (pris où qu’il se trouve, face actuelle) sur une Route Forestière, ou glissez le Tambour ou le Chant depuis une parcelle adjacente sur une Route de son rayon. Tant que Le Tapir est en piste, cette Route devient un Bourbier : la première machine qui devrait la franchir en avançant ou en frappant Devant voit cette avancée ou cette frappe annulée, puis le Duel retourne en réserve (ou le Chamane est couché en attente). Ou Frayer — posez le Duel (pris partout) sur une parcelle ciblée ; s’il y rejoint un Chamane, retournez le Duel sur Territoire tenu.",
          "face_2": "Même effet, et la machine enlisée dans un Bourbier est en outre Refroidie si elle porte au moins 1 jeton Rouge (sinon, si elle est mobile, faites-la Reculer d’1 parcelle). De plus, un Bourbier tenu par le Duel sur sa face Territoire tenu bascule sur sa face Défi au lieu de rentrer en réserve.",
          "enracine": "Au décompte final, si le jeton Duel et au moins un Chamane occupent la même parcelle survivante, retournez 1 Souche supplémentaire en Arbre debout sur ce rayon."
        },
        "decision_et_renoncement": {
          "choix": "Bloque une avancée ou une frappe Devant par-dessus une Route via un Bourbier, ou scelle le Duel auprès d’un Chamane.",
          "renoncement": "Engager le Duel ou un Chamane dans un Bourbier le prive de sa présence sur une parcelle forestière active ; enraciner Le Tapir dissipe aussitôt ses Bourbiers."
        }
      },
      "temoins": [
        {
          "id": "G7_T1",
          "statut": "OK",
          "resume": "Route en M·2 portant le Duel (Bourbier F1) : une machine en M·1 qui doit frapper Devant (M·3) ou avancer par-dessus M·2 voit cette frappe/avancée annulée et le Duel rentre en réserve."
        },
        {
          "id": "G7_T2",
          "statut": "OK",
          "resume": "Tapir F2 avec Duel face Territoire tenu en Bourbier : la machine enlisée est Refroidie (ou Recule d’1) et le Duel bascule sur Défi au lieu de rentrer en réserve."
        }
      ],
      "heuristique_bot": "Prioritaire dès qu’une Route sépare une machine d’une parcelle riche en Arbres ; en absence de Route utile, Frayer sécurise Territoire tenu sur un Chamane.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G8": {
      "id": "G8",
      "alias_oriente": "M>E",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "E",
      "couple": [
        "M",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "Rêve glissé d’1 rang à gauche ou échangé (Face 2 : 2 rangs / plongée sous voisin) · plancher sans Rêve : Altérer 1 mobile",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "sorties": [
        "POSITION_REVE",
        "ALTERATION",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": "Deux activations font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2) ou compactent deux Rêves séparés vers le Sommeil ; sans Rêve en jeu, elles Altèrent deux machines différentes.",
      "tags": [
        "CATALYSEUR_EVEIL",
        "LEVIER_REVE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Boto",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_REVE",
        "pictogrammes": [
          "PIC_AVANCEE_REVE",
          "PIC_REVE",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Glisser 1 Rêve 1 rang à gauche OU échanger voisins · aucun = Altérer",
          "face_2": "Glisser 1 Rêve 2 rangs OU plonger sous voisin · aucun = Altérer",
          "enracine": null
        },
        "resume_plateau": "Fait glisser les Rêves vers le rang 1"
      },
      "carte_joueur": {
        "titre_complet": "Le Boto, l’encantado du fleuve",
        "entite_illustree": "Le Boto (Inia geoffrensis), dauphin rose de l’Amazone glissant entre les troncs inondés",
        "brief_illustration": "Le Boto (Inia geoffrensis), dauphin rose de l’Amazone, animal entier, glissant entre les troncs d’une forêt inondée ; sur l’eau sombre se reflète la silhouette d’un homme en blanc.",
        "pitch_ambiance": "Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.",
        "texte_regle": {
          "face_1": "Choisissez un Rêve sur la Réglette et Glissez-le d’1 rang libre vers la gauche, ou échangez deux Rêves occupant deux rangs voisins (en conservant l’état debout ou couché de leurs Défenseurs). Si aucun Rêve ne peut bouger (ou s’il n’y a aucun Rêve sur la Réglette), Altérez 1 machine mobile de votre choix.",
          "face_2": "Même effet, mais le Rêve choisi peut Glisser jusqu’à 2 rangs libres vers la gauche — ou plonger par-dessus un Rêve voisin jusqu’au premier rang libre immédiatement à sa gauche. S’il n’y a toujours aucun mouvement possible, Altérez 1 machine mobile.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Accélère la convergence des Rêves vers les rangs 1–2–3 pour le Sommeil, ou Altère une mobile en plancher solo.",
          "renoncement": "Déplacer un Rêve vers la gauche peut lui faire manquer une machine qui allait attaquer sur un rang élevé."
        }
      },
      "temoins": [
        {
          "id": "G8_T1",
          "statut": "OK",
          "resume": "Boto F1 Glisse un Rêve du rang 5 au rang 4 libre (emportant ses Défenseurs) ; sans Rêve déplaçable, il Altère 1 machine mobile depuis la réserve Entités."
        },
        {
          "id": "G8_T2",
          "statut": "OK",
          "resume": "Boto F2 fait plonger un Rêve du rang 4 par-dessus un Rêve au rang 3 pour atterrir au rang 2 libre."
        }
      ],
      "heuristique_bot": "Levier majeur du Sommeil quand E joue sans H ; fait converger les Rêves à gauche dès l’Acte 1, sinon pose des Altérations.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G9": {
      "id": "G9",
      "alias_oriente": "R>H",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "H",
      "couple": [
        "R",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Sabotage ou Écaille révélé → cale sous machine mobile (R, H ou Tambour) → Ratissage bloqué · Face 2 : cale partout et machine calée révélée Étouffée",
      "entrees_plancher": [
        "SABOTAGE",
        "ECAILLE"
      ],
      "entrees_synergie": [
        "TAMBOUR"
      ],
      "entrees": [
        "SABOTAGE",
        "ECAILLE",
        "TAMBOUR"
      ],
      "sorties": [
        "CALE",
        "RECUL",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_SABOTAGE"
      ],
      "double_ouverture": "La première activation pose la cale (sur le Sabotage qui vient d’allumer l’icône), la seconde fait Reculer la machine calée d’1 parcelle ou déplace la cale ; chaque révélation de la machine calée rallume Sabotage sur la Piste.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Caïman noir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_CALE",
          "PIC_SABOTAGE",
          "PIC_TAMBOUR",
          "PIC_RECUL"
        ],
        "mots_cles_plateau": {
          "face_1": "Jeton Sabotage révélé → cale sous mobile (R · H · Tambour) · bloque Ratissage",
          "face_2": "Cale partout · mobile calée révélée = Étouffée · Sabotage rallumé",
          "enracine": null
        },
        "resume_plateau": "Pose la cale exclusive sous une machine"
      },
      "carte_joueur": {
        "titre_complet": "Le Caïman noir, l’ombre sous la pirogue",
        "entite_illustree": "Le Caïman noir (Melanosuchus niger) — grand crocodilien entier, dos cuirassé à fleur d’eau dans un lac d’eaux noires",
        "brief_illustration": "Nuit sans lune sur un lac d’eaux noires : le Caïman noir entier, seuls ses yeux rouges et sa crête dorsale affleurent ; sa gueule agrippe la roue d’une machine embourbée sur la berge ; en arrière-plan, la proue sculptée d’une pirogue et la lueur d’un tambour. Noirs profonds, reflets rubis.",
        "pitch_ambiance": "Le Caïman noir saisit et ne lâche plus : il tient sa proie contre le fond jusqu’à ce qu’elle cesse de lutter. Les pêcheurs le savent : dans les eaux noires, ce qu’il a pris ne remonte pas.",
        "texte_regle": {
          "face_1": "Glissez le jeton cale (pris en réserve ou déjà sous une autre machine) sous une machine mobile du rayon Reptiles, du rayon Humains ou du rayon portant le Tambour (sinon, faites Reculer d’1 parcelle la machine actuellement calée). Tant qu’elle porte la cale, cette machine ne peut pas entrer en Ratissage, et chaque fois que son jeton Machine est révélé à l’ouverture, allumez aussitôt l’icône Sabotage (la cale reste sous elle jusqu’à ce qu’elle soit déplacée ou que le Caïman noir quitte la piste).",
          "face_2": "Même effet sur n’importe quelle machine mobile du plateau ; de plus, chaque fois que la machine calée est révélée à l’ouverture, allumez Sabotage et Étouffez-la immédiatement (elle ne frappe pas).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Verrouille la machine la plus menaçante sous la cale (bloque Ratissage, rallume Sabotage et l’Étouffe en Face 2).",
          "renoncement": "Une seule cale existe en jeu ; la déplacer libère la machine précédemment retenue."
        }
      },
      "temoins": [
        {
          "id": "G9_T1",
          "statut": "OK",
          "resume": "Caïman F1 pose la cale sous l’Abatteuse du rayon du Tambour : elle ne peut pas entrer en Ratissage et sa révélation au tour suivant rallume Sabotage."
        },
        {
          "id": "G9_T2",
          "statut": "OK",
          "resume": "Caïman F2 : lorsque la machine calée est révélée à l’ouverture, Sabotage s’allume et la machine est Étouffée (jeton à 90°, dé retiré)."
        }
      ],
      "heuristique_bot": "Pose la cale en priorité sur une machine proche de la dernière parcelle (anti-Ratissage) ou sur la plus chargée en Rouges en Face 2.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G10": {
      "id": "G10",
      "alias_oriente": "R>E",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "E",
      "couple": [
        "R",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Semer 1 Écaille au sac → Happer (Croc sur parcelle ciblée) OU Envoûter (Altérer 1 mobile) · Face 2 : Happer ET Envoûter",
      "entrees_plancher": [
        "ECAILLE",
        "CROC",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "ALTERATION"
      ],
      "entrees": [
        "ECAILLE",
        "CROC",
        "RANG_MACHINE",
        "ALTERATION"
      ],
      "sorties": [
        "ECAILLE",
        "CROC",
        "ALTERATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE",
        "ICONE_SABOTAGE"
      ],
      "double_ouverture": "Assise sur Piégeage, la première activation Sème 1 Écaille et poste le Croc ; dès que ce Croc pare une attaque (regagnant la réserve Reptile), il rallume Piégeage et déclenche la seconde activation de La Matamata.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "La Matamata",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_ECAILLE",
          "PIC_CROC",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Semer 1 Écaille · Happer (Croc réserve → cible) OU Envoûter (Altérer 1 mobile)",
          "face_2": "Semer 1 Écaille · Happer (Croc partout → cible) · Envoûter (Altérer 1 mobile)",
          "enracine": null
        },
        "resume_plateau": "Sème une Écaille, embusque le Croc ou Altère"
      },
      "carte_joueur": {
        "titre_complet": "La Matamata, guetteuse des feuilles mortes",
        "entite_illustree": "Tortue matamata entière camouflée au fond d’un igarapé ouvrant sa large gueule",
        "brief_illustration": "Indiscernable d’un amas d’écorces sombres et de feuilles mortes au fond d’un igarapé peu profond, une tortue matamata entière ouvre brusquement sa large gueule triangulaire dans un remous spectral qui fige les rouages d’un engin.",
        "pitch_ambiance": "On croit marcher sur un lit de feuilles mortes ; déjà le vide s’est ouvert sous l’acier et la vase glacée l’aspire.",
        "texte_regle": {
          "face_1": "Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), puis choisissez : Happer — prenez le Croc dans la réserve Reptile et posez-le sur une parcelle ciblée de votre choix ; ou Envoûter — Altérez 1 machine mobile de votre choix et, si le Croc se trouve déjà sur une parcelle non ciblée, vous pouvez le déplacer sur une parcelle ciblée du rayon de cette machine.",
          "face_2": "Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), puis résolvez à la fois Happer (en pouvant prendre le Croc soit dans la réserve Reptile, soit sur une parcelle non ciblée) et Envoûter.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Enrichit le sac en Écailles puis arbitre en Face 1 entre embuscade immédiate du Croc (Happer) et pression onirique (Envoûter) ; cumule les deux en Face 2.",
          "renoncement": "En Face 1, choisir Happer renonce à l’Altération ; choisir Envoûter laisse le Croc en réserve s’il n’est pas déjà en jeu."
        }
      },
      "temoins": [
        {
          "id": "G10_T1",
          "statut": "OK",
          "resume": "Matamata F1 Sème 1 Écaille au sac et choisit Happer : le Croc de la réserve Reptile se poste sur une parcelle ciblée, prêt à rallumer Piégeage."
        },
        {
          "id": "G10_T2",
          "statut": "OK",
          "resume": "Matamata F2 Sème 1 Écaille, repositionne le Croc depuis une parcelle non ciblée vers une cible (Happer) et Altère 1 machine mobile (Envoûter)."
        }
      ],
      "heuristique_bot": "Sème des Écailles tôt pour gonfler le sac ; en Face 1, choisit Happer dès qu’une cible menacée peut rallumer Piégeage, sinon Envoûter.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G11": {
      "id": "G11",
      "alias_oriente": "O>H",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "H",
      "couple": [
        "O",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Défenseur Oiseau recyclé + Perchoir (O) → Fondre en forêt OU Saisir pour Étouffer sur le rang pointé · Face 2 : rang miroir + Chamane porté sur un Rêve",
      "entrees_plancher": [
        "PERCHOIR",
        "DEFENSEUR_ATTENTE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "CHANT",
        "TAMBOUR",
        "POSITION_REVE"
      ],
      "entrees": [
        "PERCHOIR",
        "DEFENSEUR_ATTENTE",
        "RANG_MACHINE",
        "CHANT",
        "TAMBOUR",
        "POSITION_REVE"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Un premier piqué pose un Oiseau au sol pour compléter une Parade (qui rallume son icône) ; le second piqué saisit une machine sous le Perchoir pour l’Étouffer.",
      "tags": [
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "La Harpie féroce",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_PERCHOIR",
          "PIC_RANG_MACHINE",
          "PIC_DEFENSEUR",
          "PIC_ANNULATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Recycle 1 Oiseau → Fondre devant machine OU Saisir sur rang du Perchoir (Étouffer)",
          "face_2": "Saisir sur rang du Perchoir OU miroir · porte 1 Chamane vers Rêve opposé",
          "enracine": null
        },
        "resume_plateau": "Fond au sol ou saisit une machine sous le Perchoir"
      },
      "carte_joueur": {
        "titre_complet": "La Harpie féroce, l’ombre sous la voûte",
        "entite_illustree": "La Harpie féroce entière plongeant sous la voûte, ailes repliées entre deux troncs",
        "brief_illustration": "La harpie entière plonge sous la voûte, ailes repliées juste assez pour passer entre deux troncs. Son ombre se referme sur un toit de tôle.",
        "pitch_ambiance": "Au cri du guetteur, on regarde le ciel. L’ombre est déjà passée.",
        "texte_regle": {
          "face_1": "Prenez 1 Défenseur Oiseau (en forêt, sur une Rive de Furtivité, sur un Rêve, en lisière ou en attente) et choisissez : Fondre — posez-le sur la parcelle d’une machine ou 1 pas devant elle (en sautant les Routes) ; ou Saisir — si le Perchoir de Vigie pointe un rang 1–6, posez cet Oiseau directement sur le jeton d’une machine mobile active de ce rang pour l’Étouffer jusqu’au ménage.",
          "face_2": "Même effet, mais Saisir vise aussi bien le rang pointé par le Perchoir de Vigie que son rang miroir (1↔4, 2↔5, 3↔6). De plus, après avoir saisi une machine, vous pouvez emporter 1 Chamane depuis une parcelle visée par cette machine et le poser debout sur un Rêve occupant le rang opposé (son miroir).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Recycle un Défenseur Oiseau pour renforcer une Parade (Fondre) ou Étouffer net une machine sur le rang guetté (Saisir).",
          "renoncement": "L’Oiseau posé en saisie reste immobilisé sur le jeton Machine jusqu’au ménage et ne défend plus la forêt ni les Rives."
        }
      },
      "temoins": [
        {
          "id": "G11_T1",
          "statut": "OK",
          "resume": "Harpie F1 recycle 1 Oiseau couché en attente et choisit Saisir sur le rang 5 pointé par le Perchoir : la mobile du rang 5 est Étouffée jusqu’au ménage."
        },
        {
          "id": "G11_T2",
          "statut": "OK",
          "resume": "Harpie F2 saisit une mobile au rang 2 (miroir du Perchoir au rang 5), puis porte le Chant depuis sa parcelle visée debout sur un Rêve au rang 5."
        }
      ],
      "heuristique_bot": "Privilégie le recyclage d’un Oiseau couché en attente ou libéré ; choisit Saisir sur la mobile la plus létale du rang du Perchoir (et miroir en F2), sinon Fondre pour boucler une Parade.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G12": {
      "id": "G12",
      "alias_oriente": "O>E",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "E",
      "couple": [
        "O",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Dé écarté sous paravent (et 2 dés ignorés des porteurs de Sabotage/Écaille en F2) → nouveau rang → Étouffement sur Rêve et glissement du Rêve",
      "entrees_plancher": [
        "DES_SOUS_PARAVENT",
        "RANG_MACHINE",
        "POSITION_REVE"
      ],
      "entrees_synergie": [
        "SABOTAGE"
      ],
      "entrees": [
        "DES_SOUS_PARAVENT",
        "RANG_MACHINE",
        "POSITION_REVE",
        "SABOTAGE"
      ],
      "sorties": [
        "RANG_RELU",
        "ANNULATION_INDUITE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": "Chaque Sabotage révélé allume l’icône de L’Ibijau : deux activations déplacent deux mobiles vers les Rêves encore à résoudre, et en Face 2 puisent aussi dans les dés ignorés des porteurs de Sabotage ou d’Écaille.",
      "tags": [
        "CATALYSEUR_EVEIL",
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "L’Ibijau",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_DES_PARAVENT",
          "PIC_RANG_MACHINE",
          "PIC_REVE"
        ],
        "mots_cles_plateau": {
          "face_1": "Dé d’une mobile révélée → rang de son dé écarté sous paravent",
          "face_2": "OU dé ignoré d’un Sabotage · Rêve qui l’Étouffe Glisse 1 rang à gauche",
          "enracine": null
        },
        "resume_plateau": "Relit le dé écarté vers un Rêve"
      },
      "carte_joueur": {
        "titre_complet": "L’Ibijau, les yeux fendus de la nuit",
        "entite_illustree": "L’Ibijau (Nyctibius griseus) — oiseau nocturne entier, figé à la verticale au bout d’une branche cassée, confondu avec elle",
        "brief_illustration": "Clair de lune : l’Ibijau entier, plumage d’écorce grise, se tient droit au sommet d’un chicot ; ses paupières sont closes mais deux fentes laissent filtrer un regard d’or ; sous lui, les paravents des joueurs laissent deviner des dés ; un Rêve violet flotte à l’horizon. Gris, or, violet.",
        "pitch_ambiance": "Le jour, l’Ibijau n’est qu’un bout de branche morte. Pourtant il voit : deux fentes dans ses paupières closes guettent tout. La nuit, sa plainte descendante raconte, dit-on, l’histoire d’une jeune femme changée en oiseau, qui pleure encore celui qu’elle a perdu.",
        "texte_regle": {
          "face_1": "Choisissez une machine mobile révélée dont le dé est encore sur la Réglette : déplacez son dé sur le rang indiqué par le dé écarté sous le paravent de son porteur (fonctionne à l’identique pour l’Oiseau, dont le second dé est son dé écarté). Si la machine change ainsi de rang, elle est résolue sur son nouveau rang (et peut y être Étouffée par un Rêve encore debout ou subir une Loi passive de ce rang).",
          "face_2": "Même effet, et vous pouvez aussi choisir à la place l’un des 2 dés ignorés d’un joueur ayant révélé un Sabotage ou une Écaille ce tour-ci. De plus, si la machine ainsi déplacée est Étouffée par un Rêve, vous pouvez aussitôt Glisser ce Rêve d’1 rang libre vers la gauche.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Pousse une machine mobile hors d’un rang létal ou directement sous un Rêve défendu en relisant les dés écartés sous paravent.",
          "renoncement": "Le dé écarté est souvent plus élevé que le dé retenu : l’utiliser hors Rêve peut faire passer une machine en Assaut ou en En avançant."
        }
      },
      "temoins": [
        {
          "id": "G12_T1",
          "statut": "OK",
          "resume": "Porteur d’Abatteuse (dés 2 et 5, retenu 2, écarté 5) alors qu’un Rêve défendu siège au rang 5 : Ibijau F1 déplace son dé du rang 2 au rang 5 où le Rêve l’Étouffe."
        },
        {
          "id": "G12_T2",
          "statut": "OK",
          "resume": "Ibijau F2 relit un dé ignoré (4) d’un porteur de Sabotage pour amener une mobile sur le Rêve du rang 4 ; Étouffée, elle permet de Glisser ce Rêve au rang 3 libre."
        }
      ],
      "heuristique_bot": "Priorise tout déplacement amenant une mobile sur un Rêve défendu encore debout (ou hors d’un rang 3/6 En avançant) ; en F2, exploite les dés ignorés des Sabotages.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G13": {
      "id": "G13",
      "alias_oriente": "M>I",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "I",
      "couple": [
        "M",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Nid à ≥ 2 Insectes éventré (−1 → +2) ou repli réserve (+1) · Face 2 : riposte projetée sur parcelle ciblée adjacente",
      "entrees_plancher": [
        "INSECTE",
        "DUEL"
      ],
      "entrees_synergie": [
        "NID"
      ],
      "entrees": [
        "INSECTE",
        "DUEL",
        "NID"
      ],
      "sorties": [
        "RIPOSTE_ESSAIM",
        "INSECTE",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": "Deux éventrements font gonfler deux Nids (ou deux fois le même) juste avant les attaques ; en Face 2, chaque riposte jaillit directement sur une parcelle ciblée adjacente pour allumer Insecte à la parade.",
      "tags": [
        "INSECTES",
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Tamanoir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_INSECTE",
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "Nid à 2 Insectes OU plus · −1 → +2 · sans Nid éligible = +1 réserve",
          "face_2": "Riposte projetée sur parcelle ciblée adjacente · sans Nid = +1 réserve",
          "enracine": null
        },
        "resume_plateau": "Éventre un Nid pour déclencher une riposte"
      },
      "carte_joueur": {
        "titre_complet": "Le Tamanoir, le grand mangeur qui épargne",
        "entite_illustree": "Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier éventrant une termitière",
        "brief_illustration": "Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier, longue tête tubulaire et queue en panache, éventrant une termitière de sa griffe ; des soldats jaillissent déjà des galeries.",
        "pitch_ambiance": "Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.",
        "texte_regle": {
          "face_1": "Choisissez un Nid portant au moins 2 Insectes : défaussez 1 de ses Insectes pour en ajouter aussitôt 2 de la réserve sur ce Nid (gain net de +1 Insecte). S’il n’y a aucun Nid portant au moins 2 Insectes sur le plateau, prenez 1 Insecte de la réserve de l’Essaim et posez-le sur la parcelle d’un Nid (ou, à défaut, sur la parcelle du jeton Duel ou sur une parcelle du rayon Mammifères ou Insectes).",
          "face_2": "Même effet, mais les 2 Insectes de la riposte peuvent être posés directement sur une parcelle ciblée adjacente au Nid (en sautant les Routes) — y compris sur la parcelle du Duel pour y parer et le retourner nativement sur Territoire tenu.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Multiplie le stock d’Insectes d’un Nid mûr (ou amorce un Nid vide) et projette la riposte sur les parcelles ciblées en Face 2.",
          "renoncement": "Exige de maintenir au moins 2 Insectes sur un Nid au lieu de les dépenser tous en parade."
        }
      },
      "temoins": [
        {
          "id": "G13_T1",
          "statut": "OK",
          "resume": "Nid à 2 Insectes : Tamanoir F1 en défausse 1 et ajoute 2 Insectes de la réserve (le Nid passe à 3 Insectes) ; sans Nid à ≥ 2, pose 1 Insecte de la réserve."
        },
        {
          "id": "G13_T2",
          "statut": "OK",
          "resume": "Tamanoir F2 éventre un Nid à 2 Insectes et projette les 2 Insectes de la riposte sur une parcelle ciblée adjacente portant le Duel face Défi."
        }
      ],
      "heuristique_bot": "Eventre en priorité un Nid à ≥ 2 Insectes adjacent à une parcelle ciblée (en F2) ou sur le point de produire ; sinon utilise le repli réserve pour porter un Nid à 2 Insectes.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G14": {
      "id": "G14",
      "alias_oriente": "R>I",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "I",
      "couple": [
        "R",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Écaille en ponte sous un Nid (sinon Semer 1 Écaille + Croc sur cible R/I) → éclosion du Croc sur frappe → Piégeage + Écaille semée au sac",
      "entrees_plancher": [
        "ECAILLE",
        "CROC"
      ],
      "entrees_synergie": [
        "NID"
      ],
      "entrees": [
        "ECAILLE",
        "CROC",
        "NID"
      ],
      "sorties": [
        "PONTE",
        "CROC",
        "ECAILLE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Deux activations installent deux pontes sous deux Nids (en Face 2) ou combinent une ponte sous un Nid et un Croc directement posté ; chaque éclosion allume Piégeage et Sème l’Écaille au sac.",
      "tags": [
        "INSECTES",
        "CATALYSEUR_EVEIL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Téju",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_INSECTE",
        "pictogrammes": [
          "PIC_ECAILLE",
          "PIC_NID",
          "PIC_CROC",
          "PIC_PIEGE"
        ],
        "mots_cles_plateau": {
          "face_1": "Écaille sous 1 Nid → Croc éclot sur frappe et Sème Écaille · sans Nid = Semer + Croc",
          "face_2": "Jusqu’à 2 pontes (OU 1 ponte + Croc) · le Croc éclot d’où qu’il soit",
          "enracine": null
        },
        "resume_plateau": "Pond une Écaille protectrice sous un Nid"
      },
      "carte_joueur": {
        "titre_complet": "Le Téju, la ponte au cœur de la termitière",
        "entite_illustree": "Le Téju (Tupinambis teguixin), grand lézard entier noir et doré griffant une termitière",
        "brief_illustration": "Le Téju (Tupinambis teguixin), grand lézard entier à la robe noire et dorée, griffant la paroi d’une termitière pour y pondre ; à ses pieds, la litière de feuilles où s’enfouissent les pontes sans abri.",
        "pitch_ambiance": "La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.",
        "texte_regle": {
          "face_1": "Glissez 1 Écaille (prise dans la réserve Reptile ou parmi les Écailles révélées à ce tour) sous un Nid sans ponte (max 1 ponte en jeu). À la première frappe contre la parcelle de ce Nid, si le Croc est en réserve Reptile, il éclot aussitôt sur place : il pare cette frappe (allumant Piégeage), retourne en réserve Reptile et l’Écaille est Semée au sac. S’il n’y a aucun Nid sans ponte (ou déjà 1 ponte en jeu), Semez au sac 1 Écaille disponible et posez le Croc disponible depuis la réserve sur une parcelle ciblée du rayon Reptiles ou du rayon Insectes.",
          "face_2": "Même effet, mais vous pouvez maintenir jusqu’à 2 pontes simultanées sous des Nids différents (ou 1 ponte + le Croc posté ailleurs), et lors d’une éclosion le Croc peut accourir d’où qu’il se trouve (réserve Reptile ou plateau), puis rentre normalement en réserve Reptile après sa parade.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Protège un Nid vital contre sa prochaine frappe tout en préparant une Écaille à Semer au sac (et couvre deux Nids en Face 2).",
          "renoncement": "Immobilise une Écaille hors du sac tant que la ponte n’éclot pas, et exige en Face 1 de garder le Croc en réserve pour l’éclosion."
        }
      },
      "temoins": [
        {
          "id": "G14_T1",
          "statut": "OK",
          "resume": "Téju F1 glisse 1 Écaille sous un Nid ; une frappe sur ce Nid fait éclore le Croc de la réserve (parade + Piégeage + Croc revient en réserve + Écaille Semée au sac)."
        },
        {
          "id": "G14_T2",
          "statut": "OK",
          "resume": "Téju F2 entretient 2 pontes simultanées et fait éclore le Croc même s’il était posté sur une autre parcelle, avant qu’il regagne normalement la réserve."
        }
      ],
      "heuristique_bot": "Pose une ponte dès qu’un Nid est à portée de frappe ; sans Nid libre, Sème une Écaille et poste le Croc directement sur la parcelle la plus menacée de R ou I.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "G15": {
      "id": "G15",
      "alias_oriente": "O>I",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "I",
      "couple": [
        "O",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "Insecte transporté à vol d’oiseau (amorçage natif) → prélèvement sur icône de Gardien = 1 pari en encoche · Face 2 : 2 Insectes + pollinisation + dépôt Perchoir · Enraciné : +1 Souche par tuile voisine",
      "entrees_plancher": [
        "PERCHOIR"
      ],
      "entrees_synergie": [
        "INSECTE",
        "NID",
        "GARDIEN"
      ],
      "entrees": [
        "PERCHOIR",
        "INSECTE",
        "NID",
        "GARDIEN"
      ],
      "sorties": [
        "INSECTE_TRANSPORTE",
        "INSECTE",
        "INSECTE_RANG",
        "PARI_GLISSE",
        "ARBRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": "Deux vols complètent une parade urgente puis pollinisent un Nid (Face 2) ou prélèvent un Insecte sur la Piste des Gardiens pour glisser un pari en encoche.",
      "tags": [
        "INSECTES",
        "CATALYSEUR_EVEIL",
        "ENRACINEMENT"
      ],
      "tuile_plateau": {
        "nom_court": "Le Colibri",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_INSECTE",
          "PIC_PERCHOIR",
          "PIC_PARI_ENCOCHE",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Insecte → toute parcelle · pris sur icône d’un Gardien = 1 pari en encoche",
          "face_2": "2 Insectes · arrivée Nid = +1 Insecte · dépôt possible sur rang du Perchoir",
          "enracine": "Décompte final · +1 Souche par autre tuile enracinée sur O OU voisins"
        },
        "resume_plateau": "Transporte l’Essaim et accélère les paris"
      },
      "carte_joueur": {
        "titre_complet": "Le Colibri, porteur de gouttes et de pollen",
        "entite_illustree": "Le Colibri (Phaethornis), minuscule oiseau entier en vol stationnaire devant une fleur d’héliconia",
        "brief_illustration": "Le Colibri (Phaethornis, ermite des sous-bois), animal entier : minuscule oiseau en vol stationnaire devant une fleur d’héliconia ; dans la lumière rasante, on devine les acariens des fleurs qui voyagent dans ses narines, de corolle en corolle.",
        "pitch_ambiance": "Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.",
        "texte_regle": {
          "face_1": "Déplacez 1 Insecte depuis n’importe où sur le plateau vers n’importe quelle parcelle forestière (l’amorçage natif de l’Essaim s’applique si aucun Insecte n’est en jeu). Si cet Insecte est prélevé sur l’icône d’un Gardien en piste portant au moins 1 pari, glissez aussitôt 1 pari de ce Gardien dans son encoche (sans déclencher son pouvoir ni allumer la Résonance).",
          "face_2": "Même effet avec jusqu’à 2 Insectes. De plus, chaque fois qu’un Insecte transporté arrive sur la parcelle d’un Nid, produisez aussitôt 1 Insecte supplémentaire de la réserve sur ce Nid ; et si le Perchoir de Vigie pointe un rang 1–6, vous pouvez déposer l’un des Insectes directement sur ce rang de la Réglette.",
          "enracine": "Au décompte final, retournez 1 Souche supplémentaire en Arbre debout sur le rayon de chaque autre tuile enracinée située sur le rayon Oiseaux ou sur l’un de ses deux rayons voisins."
        },
        "decision_et_renoncement": {
          "choix": "Ravitaille n’importe quelle parcelle ou déviation, ou prélève un Insecte sur la Piste des Gardiens pour sécuriser un pari.",
          "renoncement": "Prélever un Insecte sur une icône de Gardien le prive de son rôle de déclencheur sur la Piste ; enraciner Le Colibri sacrifie sa logistique aérienne."
        }
      },
      "temoins": [
        {
          "id": "G15_T1",
          "statut": "OK",
          "resume": "Colibri F1 prélève 1 Insecte posé sur l’icône d’un Gardien en piste et le dépose sur une parcelle menacée : 1 pari de ce Gardien glisse en encoche sans pouvoir ni Résonance."
        },
        {
          "id": "G15_T2",
          "statut": "OK",
          "resume": "Colibri F2 transporte 2 Insectes : le premier arrive sur un Nid (+1 Insecte produit), le second est déposé sur le rang pointé par le Perchoir de Vigie."
        }
      ],
      "heuristique_bot": "Priorise le prélèvement sur une icône de Gardien ayant un pari bloqué ; en Face 2, pollinise les Nids à 1 Insecte et alimente le rang pointé par le Perchoir.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R1": {
      "id": "R1",
      "alias_oriente": "H>E",
      "famille": "REVE",
      "origine": "H",
      "voisin": "E",
      "couple": [
        "H",
        "E"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "LEVIER_REVE",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "Rêve Humain défendu → tire un Rêve des Entités contre lui (bloc contigu) · Écho chamane : le Tambour passe debout sur le Rêve tiré · Enraciné sans fermer le Sommeil",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [
        "TAMBOUR"
      ],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE",
        "TAMBOUR"
      ],
      "sorties": [
        "REVE_COMPACTE",
        "POSITION_REVE",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "LEVIER_REVE",
        "ENRACINEMENT"
      ],
      "tuile_plateau": {
        "nom_court": "La Liane des Esprits",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_AVANCEE_REVE",
          "PIC_TAMBOUR",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "Tire 1 Rêve des Entités · collé = paire Glisse à gauche · Écho Tambour debout dessus",
          "face_2": null,
          "enracine": "Enracinée sur Rive Sabotage de H sans fermer le Sommeil"
        },
        "resume_plateau": "Tire un Rêve des Entités et relaie le Tambour"
      },
      "carte_joueur": {
        "titre_complet": "La Liane des Esprits",
        "entite_illustree": "Vision chamanique de l’ayahuasca : une liane torsadée reliant le monde des hommes à celui des esprits",
        "brief_illustration": "Vision chamanique de l’ayahuasca : une liane torsadée qui relie le monde des hommes à celui des esprits ; ses vrilles s’enroulent autour d’un rêve lumineux et l’attirent vers le chamane.",
        "pitch_ambiance": "On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.",
        "texte_regle": {
          "face_1": "Défendu : après avoir résolu ses annulations habituelles, choisissez un Rêve des Entités situé à droite de La Liane des Esprits et Glissez-le jusqu’au rang libre immédiatement à droite de la Liane (s’il est déjà collé contre elle, Glissez la paire ensemble d’1 rang libre vers la gauche). S’il n’y a aucun Rêve des Entités à droite, Glissez la Liane d’1 rang libre vers la gauche (ou, si le rang à sa gauche est occupé, Étouffez 1 machine mobile supplémentaire sur son rang). Écho chamane : si le Tambour défendait La Liane des Esprits, il peut aussitôt après ces annulations passer debout sur le Rêve des Entités ainsi tiré — s’il n’était pas défendu — afin que ce Rêve se résolve à son tour à l’ouverture.",
          "face_2": null,
          "enracine": "Enracinée sur la Rive Sabotage du rayon Humains, La Liane des Esprits ne ferme pas la victoire par Sommeil Profond (les autres Rêves peuvent encore former un bloc contigu suffisant)."
        },
        "decision_et_renoncement": {
          "choix": "Compacte les Rêves vers le Sommeil et permet au Tambour de déclencher en relais un Rêve des Entités non défendu, tout en restant enracinable sans briser le Sommeil.",
          "renoncement": "Passer le Tambour debout sur le Rêve des Entités le prive d’une descente en forêt et expose ce second Rêve à son propre rang."
        }
      },
      "temoins": [
        {
          "id": "R1_T1",
          "statut": "OK",
          "resume": "Liane défendue au rang 2 par le Tambour, Rêve Entités non défendu au rang 5 : la Liane tire ce Rêve au rang 3 puis Écho chamane passe le Tambour debout au rang 3 pour le résoudre aussitôt."
        },
        {
          "id": "R1_T2",
          "statut": "OK",
          "resume": "Liane enracinée sur la Rive Sabotage de H : elle apporte l’Effet Sentinelle permanent sans fermer la victoire par Sommeil Profond."
        }
      ],
      "heuristique_bot": "Défendue en priorité avec le Tambour dès qu’un Rêve Entités non défendu siège à sa droite ; candidate sûre à l’Enracinement en fin de partie sans bloquer le Sommeil.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R2": {
      "id": "R2",
      "alias_oriente": "E>H",
      "famille": "REVE",
      "origine": "E",
      "voisin": "H",
      "couple": [
        "E",
        "H"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "Linceul de cendre (altérée/Étouffée → face cachée = 0 en Furtivité) + Altérer OU relever Tambour sur Rêve à droite · Enraciné : Gué de cendre + Gué marqué 90° → 2 Souches finales",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "TAMBOUR",
        "DEFENSEUR_ATTENTE",
        "ALTERATION"
      ],
      "entrees": [
        "POSITION_REVE",
        "RANG_MACHINE",
        "TAMBOUR",
        "DEFENSEUR_ATTENTE",
        "ALTERATION"
      ],
      "sorties": [
        "ALTERATION",
        "DEFENSEUR_REDEPLOYE",
        "ARBRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "ENRACINEMENT"
      ],
      "tuile_plateau": {
        "nom_court": "Le Fleuve sous la cendre",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_ALTERATION",
          "PIC_TAMBOUR",
          "PIC_SOUCHE",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "Linceul = jeton face cachée (0) · Altérer 1 mobile OU relever Tambour sur Rêve à droite",
          "face_2": null,
          "enracine": "Gué de cendre sur E · machine altérée = 90° · 2 Souches finales"
        },
        "resume_plateau": "Masque la Furtivité, Altère et marque le Gué"
      },
      "carte_joueur": {
        "titre_complet": "Le Fleuve sous la cendre",
        "entite_illustree": "Filet d’eau lumineuse rejoignant une souche sous un banc de cendre dans un méandre asséché",
        "brief_illustration": "Un filet d’eau lumineuse rejoint une souche sous un banc de cendre, dans un méandre asséché.",
        "pitch_ambiance": "Sous la cendre, l’eau se souvient du lit qu’elle occupait. Le premier arbre à boire lui rend son chemin.",
        "texte_regle": {
          "face_1": "Linceul de cendre : tant que Le Fleuve sous la cendre est défendu à ce tour, chaque machine qui perd son Altération à l’ouverture ou qui est Étouffée par ce Rêve retourne son jeton Machine face cachée devant son rayon (il compte pour 0 dans le compte de Furtivité de ce rayon). De plus, à sa résolution, choisissez : Altérez 1 machine mobile (de n’importe quel rayon si le Tambour est en forêt, sinon du rayon Entités ou du rayon Humains) ; ou relevez le Tambour en attente pour le poser debout sur un Rêve non défendu situé à droite de ce Rêve.",
          "face_2": null,
          "enracine": "Gué de cendre (Rive Sabotage du rayon Entités ; ferme le Sommeil) : toute machine du rayon Entités qui perd son Altération à l’ouverture retourne son jeton face cachée devant le rayon Entités (il compte pour 0 dans son compte de Furtivité). Si au moins 1 machine du rayon Entités porte une Altération au moment de l’enracinement, tournez cette Grande Carte à 90° (Gué marqué). Au décompte final, une carte en Gué marqué retourne 2 Souches survivantes au lieu d’1 en Arbres debout sur le rayon Entités."
        },
        "decision_et_renoncement": {
          "choix": "Assure la Rive Sabotage en masquant les jetons en Furtivité, Altère ou relève le Tambour, puis double son rapport de Souches en s’enracinant sur un Gué marqué.",
          "renoncement": "Enraciner Le Fleuve sous la cendre ferme la victoire par Sommeil Profond ; manquer le marquage d’une machine altérée sur E limite son enracinement à 1 Souche."
        }
      },
      "temoins": [
        {
          "id": "R2_T1",
          "statut": "OK",
          "resume": "Fleuve défendu : une mobile perd son Altération à l’ouverture et retourne son jeton face cachée (compte 0 en Furtivité), permettant de gagner la Rive Sabotage à 0 machine visible."
        },
        {
          "id": "R2_T2",
          "statut": "OK",
          "resume": "Enraciné sur la Rive Sabotage de E alors qu’une machine de E est altérée : carte tournée à 90° (Gué marqué), retournant 2 Souches en Arbres au décompte final + Effet Sentinelle permanent."
        }
      ],
      "heuristique_bot": "Défendu dès que E vise la Rive Sabotage ou veut relever un Tambour en attente ; s’enracine au Tour 5–7 dès qu’une machine de E porte une Altération (Gué marqué).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R3": {
      "id": "R3",
      "alias_oriente": "H>M",
      "famille": "REVE",
      "origine": "H",
      "voisin": "M",
      "couple": [
        "H",
        "M"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Défenseurs du Rêve après résolution → bond vers Duel ou parcelle ciblée · Écho chamane : le Tambour emporte le Duel sur sa parcelle d’arrivée",
      "entrees_plancher": [
        "RANG_REVE",
        "DUEL"
      ],
      "entrees_synergie": [
        "ANNULATION",
        "TAMBOUR"
      ],
      "entrees": [
        "RANG_REVE",
        "DUEL",
        "ANNULATION",
        "TAMBOUR"
      ],
      "sorties": [
        "CHAMANE_EN_FORET",
        "DEFENSEUR_REDEPLOYE",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": null,
      "tags": [],
      "tuile_plateau": {
        "nom_court": "Le Chamane-Jaguar",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_DEFENSEUR",
          "PIC_TAMBOUR",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "Après résolution · Défenseurs bondissent en forêt · Écho Tambour emporte le Duel",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Étouffe puis fait bondir ses Défenseurs"
      },
      "carte_joueur": {
        "titre_complet": "La Vision du Chamane-Jaguar",
        "entite_illustree": "Vision chamanique de la métamorphose — un chamane dont l’ombre devient celle d’un jaguar en plein bond",
        "brief_illustration": "Nuit de cérémonie : un chamane danse autour d’un feu, coiffe de plumes, corps peint ; son ombre projetée sur la canopée est celle d’un jaguar bondissant, qui atterrit sur une parcelle menacée à côté du jeton Duel. Rouges braise, noirs, taches dorées.",
        "pitch_ambiance": "Chez les peuples du Haut Rio Negro, un même mot désigne le chamane et le jaguar. Quand la vision le prend, le chamane quitte le rêve sur quatre pattes et bondit là où la forêt saigne.",
        "texte_regle": {
          "face_1": "Défendu : après avoir résolu ses annulations habituelles, chacun des Défenseurs qui défendaient ce Rêve peut bondir directement sur la parcelle du jeton Duel ou sur une parcelle ciblée du rayon d’une machine tout juste Étouffée par ce Rêve (au lieu de rester couché sur le Rêve ; s’il n’a Étouffé aucune machine, ils peuvent bondir sur le rayon Humains ou le rayon Mammifères). Écho chamane : si le Tambour bondit ainsi, il peut emporter le jeton Duel (pris où qu’il se trouve, en conservant sa face actuelle) et le poser sur sa parcelle d’arrivée.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Transforme chaque Défenseur du Rêve en renfort de Parade immédiat et permet au Tambour de repositionner le Duel où la bataille se joue.",
          "renoncement": "Quitter le Rêve ne retire pas son blocage déjà résolu, mais oblige à choisir quelle parcelle sauver avec le Duel."
        }
      },
      "temoins": [
        {
          "id": "R3_T1",
          "statut": "OK",
          "resume": "Vision défendue par le Tambour : après avoir Étouffé la machine du rang, le Tambour bondit sur une parcelle ciblée en emportant le jeton Duel (Écho chamane)."
        }
      ],
      "heuristique_bot": "Défendue en priorité par le Tambour pour obtenir un double service (Étouffement à l’ouverture + Parade avec Duel repositionné aux attaques).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R4": {
      "id": "R4",
      "alias_oriente": "H>R",
      "famille": "REVE",
      "origine": "H",
      "voisin": "R",
      "couple": [
        "H",
        "R"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "TWIST_2K3",
        "LEVIER_REVE"
      ],
      "est_twist": true,
      "vecteurs": "Rêve-piston : Poussée en queue (tout le convoi Glisse d’1) OU Retour (échange à droite) · chaque mue Sème 1 Écaille au sac",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "sorties": [
        "PISTON_REVES",
        "POSITION_REVE",
        "ECAILLE"
      ],
      "paiement": [
        "P_RANG"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "LEVIER_REVE",
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "La Pirogue-Anaconda",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_AVANCEE_REVE",
          "PIC_REVE",
          "PIC_ECAILLE"
        ],
        "mots_cles_plateau": {
          "face_1": "En queue = convoi Glisse 1G · OU échange à droite · chaque mue = Semer 1 Écaille",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Pousse tout le convoi et Sème des Écailles"
      },
      "carte_joueur": {
        "titre_complet": "La Pirogue-Anaconda des ancêtres",
        "entite_illustree": "Vision mythique de la pirogue-serpent — l’anaconda géant dont le ventre porta les ancêtres en remontant le fleuve",
        "brief_illustration": "Fleuve cosmique au crépuscule : une immense pirogue dont la coque est le corps d’un anaconda, tête dressée à la proue, remonte le courant ; à son bord, d’autres Rêves lumineux comme des passagers ; dans son sillage, des écailles scintillantes tombent à l’eau. Bleus nuit, verts olive, éclats d’argent.",
        "pitch_ambiance": "Au commencement, racontent les peuples du Rio Negro, les ancêtres remontèrent le fleuve dans le ventre d’un anaconda-pirogue, de halte en halte, jusqu’à devenir des hommes. La pirogue pousse encore les rêves vers l’amont.",
        "texte_regle": {
          "face_1": "Défendu : après ses annulations habituelles, choisissez : Poussée — si La Pirogue-Anaconda est le Rêve le plus à droite de la Réglette (ou le seul), Glissez ensemble tous les Rêves de la Réglette d’1 rang libre vers la gauche (en commençant par le plus à gauche) ; ou Retour — échangez La Pirogue-Anaconda avec le premier Rêve situé à sa droite (en conservant l’état debout ou couché de leurs Défenseurs). Chaque fois qu’un mouvement est effectué ainsi, Semez au sac 1 Écaille disponible depuis la réserve Reptile.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Pousse tout le convoi des Rêves d’un bloc vers les rangs 1–2–3 ou recule pour relancer un cycle de poussée tout en Semant des Écailles au sac.",
          "renoncement": "Choisir Retour éloigne temporairement la Pirogue du bloc gauche en échange d’un repositionnement en queue et d’une Écaille."
        }
      },
      "temoins": [
        {
          "id": "R4_T1",
          "statut": "OK",
          "resume": "Pirogue-Anaconda en queue au rang 5 avec deux Rêves aux rangs 2 et 4 : Poussée Glisse les trois Rêves aux rangs 1, 3 et 4 et Sème 1 Écaille au sac."
        }
      ],
      "heuristique_bot": "Défendue en queue de convoi pour compacter vers le Sommeil tout en enrichissant le sac en Écailles.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R5": {
      "id": "R5",
      "alias_oriente": "H>O",
      "famille": "REVE",
      "origine": "H",
      "voisin": "O",
      "couple": [
        "H",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Perchoir de Vigie (O) → échange de 2 mobiles actives à ±3 rangs (1↔4, 2↔5, 3↔6) · Écho chamane : Chant bascule 1 mobile seule · Tambour Refroidit 1 déplacée",
      "entrees_plancher": [
        "PERCHOIR",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "TAMBOUR",
        "CHANT",
        "ROUGE"
      ],
      "entrees": [
        "PERCHOIR",
        "RANG_MACHINE",
        "TAMBOUR",
        "CHANT",
        "ROUGE"
      ],
      "sorties": [
        "RANG_MACHINE",
        "BLEU"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [],
      "tuile_plateau": {
        "nom_court": "Le Ciel à deux eaux",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_PERCHOIR",
          "PIC_RANG_MACHINE",
          "PIC_TAMBOUR",
          "PIC_CHANT"
        ],
        "mots_cles_plateau": {
          "face_1": "Échange 2 mobiles à ±3 rangs sous le Perchoir · Écho Chant seul · Tambour Refroidit",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Inverse les rangs miroirs sous le Perchoir"
      },
      "carte_joueur": {
        "titre_complet": "Le Ciel à deux eaux",
        "entite_illustree": "Vision d’un ciel reflété dans le fleuve",
        "brief_illustration": "Un bras de fleuve reflète deux horizons décalés sous une même ligne de pluie.",
        "pitch_ambiance": "Les deux rives montrent le même ciel. Une seule voit l’orage arriver.",
        "texte_regle": {
          "face_1": "Défendu : avant ses annulations habituelles, si le Perchoir de Vigie pointe un rang 1–6 (ou est au pied d’un rayon en portant un jeton caché), vous pouvez échanger les dés de 2 machines mobiles actives séparées d’exactement 3 rangs (1↔4, 2↔5 ou 3↔6) dont l’une au moins est désignée par le Perchoir (sinon, échangez deux mobiles actives de votre choix séparées de 3 rangs). Écho chamane : si le Chant défend ce Rêve, vous pouvez aussi basculer 1 machine mobile seule vers son rang miroir même sans machine active en face ; si le Tambour défend ce Rêve, Refroidissez l’une des machines ainsi déplacées si elle porte au moins 1 jeton Rouge.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Bascule une machine d’Assaut vers Charge (ou vers le rang d’un Rêve), avec souplesse de bascule solo via le Chant ou Refroidissement via le Tambour.",
          "renoncement": "Échanger deux mobiles expose le rang miroir à la seconde machine si aucun Rêve ne l’y attend."
        }
      },
      "temoins": [
        {
          "id": "R5_T1",
          "statut": "OK",
          "resume": "Ciel défendu par le Chant au rang 2 avec Perchoir au rang 5 : la mobile du rang 5 bascule seule sur son miroir au rang 2 où le Rêve l’Étouffe aussitôt."
        },
        {
          "id": "R5_T2",
          "statut": "OK",
          "resume": "Ciel défendu par le Tambour échange deux mobiles entre les rangs 3 et 6 et Refroidit celle qui porte 1 Rouge."
        }
      ],
      "heuristique_bot": "Défendu avec Chant (bascule solo vers ce Rêve ou un Rêve à droite) ou Tambour (échange + Refroidissement d’une machine à Rouge).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R6": {
      "id": "R6",
      "alias_oriente": "H>I",
      "famille": "REVE",
      "origine": "H",
      "voisin": "I",
      "couple": [
        "H",
        "I"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0"
      ],
      "est_twist": false,
      "vecteurs": "Cueillette d’1 Insecte de H sur ce rang (amorçage natif) → chaque Insecte défaussé Étouffe +1 machine · Écho chamane : Tambour cueille jusqu’à 2 (H/I) · Chant Étouffe aussi à ±1",
      "entrees_plancher": [
        "INSECTE",
        "ANNULATION"
      ],
      "entrees_synergie": [
        "INSECTE_RANG",
        "TAMBOUR",
        "CHANT"
      ],
      "entrees": [
        "INSECTE",
        "ANNULATION",
        "INSECTE_RANG",
        "TAMBOUR",
        "CHANT"
      ],
      "sorties": [
        "ANNULATION_RENFORCEE",
        "INSECTE_RANG"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES"
      ],
      "tuile_plateau": {
        "nom_court": "La Tucandeira",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_INSECTE",
          "PIC_ANNULATION",
          "PIC_TAMBOUR"
        ],
        "mots_cles_plateau": {
          "face_1": "Cueille 1 Insecte de H → chaque défaussé Étouffe +1 · Écho Tambour 2 (H/I) · Chant ±1",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "L’Essaim multiplie les Étouffements du Rêve"
      },
      "carte_joueur": {
        "titre_complet": "Le Rite de la Tucandeira",
        "entite_illustree": "Gants tressés de fourmis tucandeiras portés lors d’une danse rituelle",
        "brief_illustration": "Vision rituelle : les gants tressés de fourmis tucandeiras du rite de passage, portés par un jeune initié qui danse ; à ses pieds, les fourmis fraîchement cueillies en forêt.",
        "pitch_ambiance": "Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.",
        "texte_regle": {
          "face_1": "Défendu : avant de résoudre ses annulations, vous pouvez cueillir 1 Insecte depuis le rayon Humains pour le poser sur le rang de ce Rêve (l’amorçage natif de l’Essaim s’applique si aucun Insecte n’est sur le plateau). Puis, lors de sa résolution, chaque Insecte que vous défaussez depuis ce rang Étouffe 1 machine mobile supplémentaire de ce rang (en plus du quota habituel de ses Défenseurs). Écho chamane : si le Tambour défend ce Rêve, vous pouvez cueillir jusqu’à 2 Insectes depuis le rayon Humains ou le rayon Insectes ; si le Chant défend ce Rêve, chaque Insecte défaussé peut Étouffer une machine mobile soit sur ce rang, soit sur un rang directement adjacent (±1).",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Transforme des Insectes en Étouffements multiples dès l’ouverture, élargis à ±1 rang avec le Chant ou à 2 cueillettes avec le Tambour.",
          "renoncement": "Défausser des Insectes sur la Réglette les retire de la défense forestière et de la croissance des Nids."
        }
      },
      "temoins": [
        {
          "id": "R6_T1",
          "statut": "OK",
          "resume": "Tucandeira défendue par le Chant au rang 4 : cueille 1 Insecte de H et le défausse pour Étouffer une machine mobile au rang 5 adjacent (Écho chamane)."
        },
        {
          "id": "R6_T2",
          "statut": "OK",
          "resume": "Tucandeira défendue par le Tambour avec 0 Insecte en jeu : amorçage natif en réserve, puis chaque Insecte défaussé Étouffe +1 machine du rang."
        }
      ],
      "heuristique_bot": "Défendue par le Chant pour couvrir 3 rangs (rang ±1) avec un seul Défenseur + Insectes, ou par le Tambour pour nettoyer un encombrement de 2–3 machines sur le même rang.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R7": {
      "id": "R7",
      "alias_oriente": "E>M",
      "famille": "REVE",
      "origine": "E",
      "voisin": "M",
      "couple": [
        "E",
        "M"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LOI_PASSIVE"
      ],
      "est_twist": false,
      "vecteurs": "Loi passive : machines sur son rang marchent à reculons + tout Recul hors du Duel (toute cause) retourne Territoire tenu · Défendu : mobiles Étouffées aussi Altérées",
      "entrees_plancher": [
        "RANG_REVE",
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "DUEL"
      ],
      "entrees": [
        "RANG_REVE",
        "POSITION_REVE",
        "RANG_MACHINE",
        "DUEL"
      ],
      "sorties": [
        "RECUL",
        "TERRITOIRE",
        "ALTERATION"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "LOI_PASSIVE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Curupira",
        "fenetre_badge": "LOI_PASSIVE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_RECUL",
          "PIC_DUEL",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Loi · son rang marche à reculons · tout Recul hors Duel = Territoire · Défendu = Altérer",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Inverse la marche et Altère les Étouffées"
      },
      "carte_joueur": {
        "titre_complet": "Le Curupira, protecteur aux pieds retournés",
        "entite_illustree": "Le Curupira — esprit protecteur de la forêt, petit être à la chevelure de flammes rouges et aux pieds tournés vers l’arrière",
        "brief_illustration": "Sentier boueux au crépuscule : le Curupira, chevelure flamboyante, court en sens inverse de ses propres empreintes ; des chenilles de machine suivent ces traces et reculent vers la lisière ; derrière lui, un jaguar et un tapir l’observent, à l’abri. Rouges flamme, verts sombres, boue ocre.",
        "pitch_ambiance": "Le Curupira protège les bêtes et punit qui abat trop d’arbres. Ses pieds tournés à l’envers laissent des traces qui égarent les chasseurs : qui croit le suivre s’éloigne de lui, et retourne d’où il vient.",
        "texte_regle": {
          "face_1": "Loi passive : toute machine mobile qui attaque depuis le rang du Curupira marche à reculons — sa frappe Devant vise la parcelle derrière elle vers la bordure (en sautant les Routes), son avancée la fait Reculer d’1 parcelle vers la bordure, et sa frappe Sur place ne gagne jamais de jeton Rouge. De plus, partout sur le plateau, toute machine qui Recule hors de la parcelle du jeton Duel face Défi — quelle qu’en soit la cause — retourne aussitôt le Duel sur sa face Territoire tenu. Défendu : chaque machine mobile Étouffée sur son rang est en outre Altérée.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Laisse Le Curupira sans Défenseur pour faire reculer les machines de son rang et sceller Territoire tenu, ou le défend pour Étouffer et Altérer simultanément.",
          "renoncement": "Défendre Le Curupira Étouffe la machine au lieu de la laisser reculer d’elle-même, mais pose une Altération pour le tour suivant."
        }
      },
      "temoins": [
        {
          "id": "R7_T1",
          "statut": "OK",
          "resume": "Curupira non défendu au rang 3 : une machine au rang 3 frappe derrière et Recule hors de la parcelle du Duel face Défi, le retournant sur Territoire tenu."
        },
        {
          "id": "R7_T2",
          "statut": "OK",
          "resume": "Curupira défendu au rang 4 : la mobile Étouffée par ce Rêve reçoit en outre 1 jeton d’Altération de la réserve Entités."
        }
      ],
      "heuristique_bot": "Positionné sur un rang En avançant (3 ou 6) pour casser l’avancée sans Défenseur ; défendu lorsqu’une mobile critique doit être à la fois Étouffée et Altérée.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R8": {
      "id": "R8",
      "alias_oriente": "E>R",
      "famille": "REVE",
      "origine": "E",
      "voisin": "R",
      "couple": [
        "E",
        "R"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LOI_PASSIVE",
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "Loi passive 100 % Ouverture : chaque Écaille révélée (ou ce Rêve défendu) → Glisser 1 Rêve d’1 rang libre à gauche + Altérer 1 mobile OU Refroidir 1 machine",
      "entrees_plancher": [
        "POSITION_REVE",
        "ALTERATION",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "ECAILLE",
        "ROUGE"
      ],
      "entrees": [
        "POSITION_REVE",
        "ALTERATION",
        "RANG_MACHINE",
        "ECAILLE",
        "ROUGE"
      ],
      "sorties": [
        "RANG_REVE",
        "ALTERATION",
        "BLEU"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [
        "LEVIER_REVE",
        "LOI_PASSIVE"
      ],
      "tuile_plateau": {
        "nom_court": "La Mue d’obsidienne",
        "fenetre_badge": "LOI_PASSIVE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_ECAILLE",
          "PIC_AVANCEE_REVE",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Loi · chaque Écaille révélée OU Défendu → Glisser 1 Rêve 1G + Altérer OU Refroidir",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Écailles et Rêve glissent, Altèrent ou Refroidissent"
      },
      "carte_joueur": {
        "titre_complet": "La Mue d’obsidienne",
        "entite_illustree": "Mue translucide d’obsidienne d’un grand serpent enroulée autour d’une lame givrée",
        "brief_illustration": "Suspendue entre deux troncs noirs baignés de lueurs violettes, la mue translucide et tranchante comme du verre volcanique d’un grand serpent s’enroule autour d’une lame de scie couverte de givre bleu.",
        "pitch_ambiance": "Le reptile abandonne son ancienne peau aux esprits de la nuit ; chaque écaille qui tombe ouvre un sillon d’ombre vers le cœur du sommeil.",
        "texte_regle": {
          "face_1": "Loi passive (Ouverture) : chaque fois qu’une Écaille Reptile est révélée à l’ouverture — ainsi que lorsque La Mue d’obsidienne est défendue et résolue —, Glissez 1 Rêve de votre choix d’1 rang libre vers la gauche, puis choisissez : Altérez 1 machine mobile ou Refroidissez 1 machine portant au moins 1 jeton Rouge.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Convertit chaque Écaille révélée (et chaque défense propre) en avancée vers le Sommeil couplée à une Altération ou un Refroidissement.",
          "renoncement": "Arbitrer entre Altérer une mobile pour le tour suivant ou Refroidir immédiatement une menace chargée de ce tour."
        }
      },
      "temoins": [
        {
          "id": "R8_T1",
          "statut": "OK",
          "resume": "Une Écaille est révélée à l’ouverture : La Mue d’obsidienne (même non défendue) Glisse 1 Rêve d’1 rang libre à gauche et Refroidit 1 machine à Rouge."
        },
        {
          "id": "R8_T2",
          "statut": "OK",
          "resume": "La Mue d’obsidienne défendue à l’ouverture : après ses annulations, elle Glisse 1 Rêve d’1 rang libre à gauche et Altère 1 machine mobile."
        }
      ],
      "heuristique_bot": "Levier passif très rentable avec les Écailles semées par R ; privilégie Refroidir sur menace immédiate à fort Seuil, sinon Altérer pour préparer le tour suivant.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R9": {
      "id": "R9",
      "alias_oriente": "E>O",
      "famille": "REVE",
      "origine": "E",
      "voisin": "O",
      "couple": [
        "E",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "Perchoir de Vigie (O) → vol de 2 rangs avant annulation · puis Maudire (Altérer) OU Siffler dans la brume (retire 1–2 Altérations → Glisse 1–2 Rêves à gauche + Refroidit)",
      "entrees_plancher": [
        "PERCHOIR",
        "RANG_REVE"
      ],
      "entrees_synergie": [
        "ALTERATION",
        "ROUGE"
      ],
      "entrees": [
        "PERCHOIR",
        "RANG_REVE",
        "ALTERATION",
        "ROUGE"
      ],
      "sorties": [
        "POSITION_REVE",
        "ALTERATION",
        "BLEU"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [
        "LEVIER_REVE"
      ],
      "tuile_plateau": {
        "nom_court": "La Matinta Pereira",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_PERCHOIR",
          "PIC_AVANCEE_REVE",
          "PIC_ALTERATION",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Vole ≤ 2 rangs vers Perchoir · Maudire (Altérer) OU retirer 1–2 Altérations → Glisser + Refroidir",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Vole vers le Perchoir, maudit ou siffle"
      },
      "carte_joueur": {
        "titre_complet": "La Matinta Pereira, siffleuse de minuit",
        "entite_illustree": "La Matinta Pereira — vieille sorcière de la forêt qui prend la forme d’un oiseau noir au sifflement strident",
        "brief_illustration": "Minuit sur un village sur pilotis : une vieille femme drapée de noir se dissout en un oiseau sombre qui s’élève en sifflant ; son vol trace une ligne lumineuse vers un perchoir de vigie pointé vers un rang de la Réglette ; sur un seuil, une offrande de tabac. Noirs, violets, argent lunaire.",
        "pitch_ambiance": "Le sifflement de la Matinta semble venir de partout à la fois. Promettez-lui du tabac et elle s’en va ; refusez, et votre nuit sera maudite.",
        "texte_regle": {
          "face_1": "Défendu : avant de résoudre ses annulations, si le Perchoir de Vigie pointe un rang 1–6, Glissez La Matinta Pereira jusqu’à 2 rangs libres en direction de ce rang (elle peut s’y poser s’il est libre). Après ses annulations habituelles, choisissez : Maudire — Altérez 1 machine mobile de ce rang (même tout juste Étouffée) ou du rayon ou du rang désigné par le Perchoir (à défaut, du rayon Entités) ; ou Siffler dans la brume — retirez 1 ou 2 jetons d’Altération en jeu (rendus à la réserve Entités) : pour chaque Altération ainsi retirée, Glissez 1 Rêve d’1 rang libre vers la gauche et, si la machine réveillée porte au moins 1 jeton Rouge, Refroidissez-la.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Intercepte une machine en volant vers le Perchoir, puis accumule des Altérations (Maudire) ou les encaisse en tempo Sommeil + Refroidissement (Siffler dans la brume).",
          "renoncement": "Retirer des Altérations par Siffler dans la brume renonce à leur effacement au tour suivant mais accélère nettement la convergence des Rêves."
        }
      },
      "temoins": [
        {
          "id": "R9_T1",
          "statut": "OK",
          "resume": "Matinta défendue au rang 4 avec Perchoir pointant le rang 2 libre : elle vole au rang 2, Étouffe la mobile présente et choisit Maudire pour l’Altérer."
        },
        {
          "id": "R9_T2",
          "statut": "OK",
          "resume": "Matinta choisit Siffler dans la brume en retirant 2 Altérations en jeu : elle Glisse 2 Rêves d’1 rang libre à gauche et Refroidit chaque machine réveillée portant un Rouge."
        }
      ],
      "heuristique_bot": "Vole vers le rang du Perchoir pour Étouffer la cible ; choisit Siffler dans la brume dès que 1–2 Altérations sont mûres pour fermer le Sommeil ou Refroidir.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "R10": {
      "id": "R10",
      "alias_oriente": "E>I",
      "famille": "REVE",
      "origine": "E",
      "voisin": "I",
      "couple": [
        "E",
        "I"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "TWIST_2K3",
        "LEVIER_REVE"
      ],
      "est_twist": true,
      "vecteurs": "Glisser 1 Rêve d’1 rang à gauche + Envol de la Ruche (déménage 1 Nid avec garnison + Altérer ou Refroidir) OU Essaim spectral (+1 Insecte réserve + Altérer)",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "NID",
        "INSECTE",
        "ROUGE"
      ],
      "entrees": [
        "POSITION_REVE",
        "RANG_MACHINE",
        "NID",
        "INSECTE",
        "ROUGE"
      ],
      "sorties": [
        "RANG_REVE",
        "NID_DEPLACE",
        "ALTERATION",
        "INSECTE",
        "BLEU"
      ],
      "paiement": [
        "P_RANG"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES",
        "LEVIER_REVE",
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "La Ruche vagabonde",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_AVANCEE_REVE",
          "PIC_NID",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Glisser 1 Rêve 1G · déménage 1 Nid + Altérer OU Refroidir · OU +1 Insecte + Altérer",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Glisse un Rêve et déménage une ruche"
      },
      "carte_joueur": {
        "titre_complet": "La Transe de la Ruche vagabonde",
        "entite_illustree": "Immense ruche d’écorce vivante flottant dans la nuit portée par des filaments de brume",
        "brief_illustration": "Portée par des filaments de brume violette à travers la nuit amazonienne, une immense ruche d’écorce vivante flotte entre les troncs avec toute sa nuée lumineuse pour venir se greffer juste devant la lame d’un engin surpris.",
        "pitch_ambiance": "Guidé par le songe, le nid décroche ses racines d’écorce et traverse la nuit : quand l’acier frappe la clairière, la ruche est déjà derrière lui.",
        "texte_regle": {
          "face_1": "Défendu : après ses annulations habituelles, Glissez 1 Rêve de votre choix d’1 rang libre vers la gauche, puis choisissez : Envol de la Ruche — déménagez 1 Nid en jeu vers n’importe quelle parcelle forestière sans autre Nid (en emportant tous ses Insectes, tous ses Défenseurs et son éventuelle ponte selon la règle commune), puis Altérez 1 machine mobile du rayon rejoint ou Refroidissez 1 machine présente sur la parcelle rejointe ; ou Essaim spectral — prenez 1 Insecte dans la réserve de l’Essaim pour le poser sur le rayon Entités, le rayon Insectes ou un rang 1–6 de la Réglette, puis Altérez 1 machine mobile de votre choix.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Avance vers le Sommeil tout en téléportant un Nid complet avec sa garnison (ou en injectant un Insecte + une Altération en plancher solo).",
          "renoncement": "Déménager un Nid avec ses Défenseurs dégarnit instantanément la parcelle de départ."
        }
      },
      "temoins": [
        {
          "id": "R10_T1",
          "statut": "OK",
          "resume": "Table {H, E, I} : La Transe de la Ruche vagabonde Glisse un Rêve à gauche puis téléporte un Nid avec son Défenseur et ses 2 Insectes sur la parcelle menacée d’un autre rayon et Refroidit le Bulldozer sur place."
        }
      ],
      "heuristique_bot": "Exploite Envol de la Ruche pour projeter un Nid défendu sur une parcelle critique (ou la dernière parcelle d’un rayon pour débloquer le déploiement sur la Réglette).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "M1": {
      "id": "M1",
      "alias_oriente": "I>M",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "M",
      "couple": [
        "I",
        "M"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Insectes (I) embarqués en phorésie sur une machine → sautent en parade là où elle frappe → descente au ménage",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [
        "DUEL"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "DUEL"
      ],
      "sorties": [
        "INSECTE_PASSAGER",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": null,
      "tags": [
        "INSECTES"
      ],
      "tuile_plateau": {
        "nom_court": "Le Pelage du Paresseux",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_MIGRATION",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "1–2 Insectes embarquent sur 1 machine voisine · sautent à la frappe · descente ménage",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Des passagers qui voyagent sur les machines"
      },
      "carte_joueur": {
        "titre_complet": "Le Pelage du Paresseux",
        "entite_illustree": "Nid vivant — le pelage d’un paresseux à trois doigts, verdi d’algues, où vivent des papillons et de minuscules passagers",
        "brief_illustration": "Gros plan sur un paresseux suspendu à une branche, sa fourrure verte d’algues grouillant de petits papillons et d’insectes ; certains s’envolent vers la chenille d’une machine qui passe sous l’arbre et s’y agrippent ; sur la parcelle voisine, le jeton Duel. Verts mousse, gris, ambre.",
        "pitch_ambiance": "La fourrure du paresseux est un monde : des algues, des champignons, des papillons qui n’existent nulle part ailleurs. Ces passagers voyagent sans bouger leurs ailes, et savent descendre au bon endroit.",
        "texte_regle": {
          "face_1": "Production (défendu) : après la production de ce Nid, vous pouvez embarquer 1 ou 2 Insectes présents sur la parcelle de ce Nid sur une machine située sur son rayon ou sur un rayon voisin (ils deviennent des passagers et se déplacent avec elle). Chaque fois que cette machine frappe une parcelle, avant la résolution de la parade, vous pouvez faire sauter tout ou partie de ses passagers sur la parcelle frappée pour aider la parade (une parade sur la parcelle du Duel le retourne nativement sur Territoire tenu). Au ménage, les passagers encore à bord descendent sur la parcelle où la machine s’est arrêtée.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Embarque 1–2 Insectes en réserve mobile directement sur la machine ennemie pour parer sa frappe la plus dangereuse.",
          "renoncement": "Quitter le Nid réduit sa garnison sous le seuil de 2 Insectes pour la Production suivante."
        }
      },
      "temoins": [
        {
          "id": "M1_T1",
          "statut": "OK",
          "resume": "2 passagers embarqués sur le Bulldozer : quand il frappe la parcelle du Duel face Défi (1 Défenseur, Seuil 3), les 2 passagers sautent, parent la frappe (icône Insecte) et retournent nativement le Duel sur Territoire tenu."
        },
        {
          "id": "M1_T2",
          "statut": "OK",
          "resume": "Un passager non dépensé descend au ménage sur la dernière parcelle atteinte par sa machine."
        }
      ],
      "heuristique_bot": "Embarque 1–2 Insectes sur la machine la plus menaçante du rayon I ou voisin dès que le Nid conserve 2 Insectes (ou qu’une parade critique manque de 1–2).",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "M2": {
      "id": "M2",
      "alias_oriente": "I>R",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "R",
      "couple": [
        "I",
        "R"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Soldats (2 Insectes parent tout Seuil sur ce Nid) · Production défendue → Semer 1 Écaille au sac OU poster le Croc sur machine présente",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "NID",
        "INSECTE"
      ],
      "sorties": [
        "PARADE_SOLDATS",
        "ECAILLE",
        "CROC"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE",
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": null,
      "tags": [
        "INSECTES"
      ],
      "tuile_plateau": {
        "nom_court": "La Termitière-Forteresse",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_ECAILLE",
          "PIC_CROC"
        ],
        "mots_cles_plateau": {
          "face_1": "2 Insectes du Nid parent tout Seuil · Production = Semer 1 Écaille OU Croc sur place",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Forteresse d’argile et soldats à glu"
      },
      "carte_joueur": {
        "titre_complet": "La Termitière-Forteresse",
        "entite_illustree": "Nid vivant — une termitière de terre cuite au soleil, hérissée de cheminées, défendue par des soldats à tête-seringue",
        "brief_illustration": "Une termitière haute comme un homme, parois ocres striées, cheminées fumantes ; à sa base, des soldats à tête en pointe projettent une glu luisante sur la chenille d’une machine ; un lézard se chauffe au sommet ; quelques écailles d’argile brillent sur la paroi. Ocres, rouilles, éclats dorés.",
        "pitch_ambiance": "Le mur de la termitière est plus dur que la brique. Ses soldats, la tête en forme de seringue, projettent une glu qui colle tout ce qui ose y toucher. Les reptiles le savent : il n’est pas d’abri plus sûr.",
        "texte_regle": {
          "face_1": "Soldats à glu : lorsqu’une machine frappe la parcelle de ce Nid, vous pouvez défausser 2 Insectes présents sur ce Nid pour parer seuls cette frappe quel que soit son Seuil (sans aucun Défenseur requis ; allume l’icône Insecte). Production (défendu) : après la production de ce Nid, choisissez — Semez au sac 1 Écaille disponible depuis la réserve Reptile ; ou, si une machine mobile se trouve sur la parcelle de ce Nid, posez le Croc disponible depuis la réserve Reptile sur cette parcelle.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Défend sa propre parcelle contre n’importe quel Seuil avec 2 Insectes et alimente le sac en Écailles (ou pose le Croc).",
          "renoncement": "Dépenser 2 Insectes en Soldats à glu vide rapidement la termitière avant sa prochaine Production."
        }
      },
      "temoins": [
        {
          "id": "M2_T1",
          "statut": "OK",
          "resume": "Abatteuse en Assaut à Seuil 4 sur le Nid sans Défenseur : 2 Insectes défaussés parent seuls la frappe et allument l’icône Insecte."
        },
        {
          "id": "M2_T2",
          "statut": "OK",
          "resume": "Production défendue sans machine présente : 1 Écaille de la réserve Reptile est Semée au sac."
        }
      ],
      "heuristique_bot": "Défendue tôt pour Semer des Écailles au sac et maintenir ≥ 2 Insectes capables de parer seuls un Assaut à haut Seuil.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "M3": {
      "id": "M3",
      "alias_oriente": "I>O",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "O",
      "couple": [
        "I",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Production (Nid défendu) → déménagement avant production (1 pas, ou 2 vers/sur le rayon du Perchoir, garnison emportée) → production → Front de raid (1–2 Insectes)",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [
        "PERCHOIR"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "PERCHOIR"
      ],
      "sorties": [
        "NID_NOMADE",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": null,
      "tags": [
        "INSECTES",
        "TWIST_2K3"
      ],
      "tuile_plateau": {
        "nom_court": "Le Bivouac des Légionnaires",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_NID",
          "PIC_MIGRATION",
          "PIC_PERCHOIR"
        ],
        "mots_cles_plateau": {
          "face_1": "Défendu avant prod → avance 1 pas (2 vers Perchoir) · prod · raid 1–2 Insectes",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Nid nomade guidé par le Perchoir"
      },
      "carte_joueur": {
        "titre_complet": "Le Bivouac des Légionnaires",
        "entite_illustree": "Nid vivant nomade — le bivouac des fourmis légionnaires, boule de centaines de milliers de corps entrelacés suspendue sous un tronc",
        "brief_illustration": "Aube : sous un tronc couché, une masse vivante de fourmis légionnaires forme des chambres et des couloirs de leurs propres corps ; une colonne s’étire déjà vers la parcelle voisine ; au-dessus, des oiseaux fourmiliers suivent le front de raid, et un perchoir de vigie est planté au bout du chemin. Bruns rouges, noirs, lumière rasante.",
        "pitch_ambiance": "Le bivouac n’a pas de murs : ce sont les fourmis elles-mêmes, accrochées les unes aux autres. Chaque nuit, la colonne repart ; et derrière son front de raid, les oiseaux fourmiliers suivent, guettant ce qui s’enfuit.",
        "texte_regle": {
          "face_1": "Production (défendu) : avant de produire, si ce Nid est défendu, vous pouvez le déplacer d’1 parcelle libre adjacente (sans autre Nid ; en sautant les Routes, y compris latéralement entre parcelles de même profondeur) — ou jusqu’à 2 parcelles libres adjacentes en vous rapprochant ou en restant sur le rayon désigné par le Perchoir de Vigie — en emportant simultanément tous ses Insectes, tous ses Défenseurs et son éventuelle ponte selon la règle commune. Puis ce Nid produit normalement et lance son Front de raid : déplacez 1 ou 2 Insectes de ce Nid vers une parcelle ciblée adjacente.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Déplace un bastion entier (Nid + Défenseurs + Insectes) vers le point chaud du tour puis projette un Front de raid de 1–2 Insectes.",
          "renoncement": "Exige un Défenseur sur le Nid pour lever le camp ; projeter 2 Insectes en raid expose le Nid lui-même à sa prochaine frappe."
        }
      },
      "temoins": [
        {
          "id": "M3_T1",
          "statut": "OK",
          "resume": "Bivouac défendu en I·1 avec Perchoir au pied du rayon O voisin : il avance de 2 parcelles vers O avec son Défenseur et ses Insectes, produit, puis envoie 2 Insectes en Front de raid."
        }
      ],
      "heuristique_bot": "Suit le Perchoir de Vigie ou la plus forte pression machine pour repositionner un Défenseur + Nid + Front de raid en une seule Production.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "M4": {
      "id": "M4",
      "alias_oriente": "I>H",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "H",
      "couple": [
        "I",
        "H"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0"
      ],
      "est_twist": false,
      "vecteurs": "Insecte consommé à la Production → relève 1 bâtisseur en attente vers le Nid ou le Tambour (H), jusqu’à 2 fois",
      "entrees_plancher": [
        "NID",
        "INSECTE",
        "DEFENSEUR_ATTENTE"
      ],
      "entrees_synergie": [
        "TAMBOUR"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "DEFENSEUR_ATTENTE",
        "TAMBOUR"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES"
      ],
      "tuile_plateau": {
        "nom_court": "Le Rucher des Mélipones",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_DEFENSEUR_ATTENTE",
          "PIC_TAMBOUR",
          "PIC_INSECTE"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Insecte → relève 1 bâtisseur en attente sur le Nid OU le Tambour (max 2)",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Le miel relève les bâtisseurs couchés"
      },
      "carte_joueur": {
        "titre_complet": "Le Rucher des Mélipones",
        "entite_illustree": "Nid vivant — une ruche d’abeilles sans dard (mélipones) logée dans un tronc creux, avec son tube d’entrée de cire",
        "brief_illustration": "Tronc creux au bord d’un jardin villageois : un tube de cire brune où entrent et sortent de petites abeilles sans dard ; un chamane y recueille une calebasse de miel ; à côté, deux bâtisseurs couchés se relèvent, revigorés. Miels ambrés, bruns, verts tendres.",
        "pitch_ambiance": "Les mélipones n’ont pas de dard ; elles offrent leur miel aux peuples qui les protègent depuis des siècles. Une gorgée, et ceux qui ont bâti jusqu’à l’épuisement se relèvent pour défendre la forêt.",
        "texte_regle": {
          "face_1": "Production (défendu) : après la production de ce Nid, vous pouvez défausser 1 ou 2 Insectes présents sur ce Nid. Pour chaque Insecte ainsi défaussé, relevez 1 Défenseur couché en attente (bâtisseur ou pion couché) et posez-le actif sur la parcelle de ce Nid ou sur la parcelle du Tambour.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Convertit des Insectes en Défenseurs actifs au tour même où un joueur a construit, effaçant le coût de construction.",
          "renoncement": "Consomme les Insectes du Nid au lieu de les accumuler pour les parades ou les déviations."
        }
      },
      "temoins": [
        {
          "id": "M4_T1",
          "statut": "OK",
          "resume": "Après construction d’un Rêve (2 bâtisseurs couchés), Le Rucher des Mélipones défendu défausse 1 Insecte pour relever 1 bâtisseur actif sur la parcelle du Tambour."
        }
      ],
      "heuristique_bot": "Prioritaire les tours de construction ; relève en priorité un bâtisseur vers la parcelle menacée du Tambour ou du Nid.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    },
    "M5": {
      "id": "M5",
      "alias_oriente": "I>E",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "E",
      "couple": [
        "I",
        "E"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "LOI_PASSIVE"
      ],
      "est_twist": false,
      "vecteurs": "Loi passive : Déviation ±1 vers Rêve → Altérer + recycle l’Insecte sur ce Nid (si < 2) · Production défendue → 1 Insecte vers Réglette OU Altérer",
      "entrees_plancher": [
        "NID_ACTIVE",
        "INSECTE"
      ],
      "entrees_synergie": [
        "INSECTE_RANG",
        "POSITION_REVE"
      ],
      "entrees": [
        "NID_ACTIVE",
        "INSECTE",
        "INSECTE_RANG",
        "POSITION_REVE"
      ],
      "sorties": [
        "ALTERATION",
        "INSECTE_RANG",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES",
        "LOI_PASSIVE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Mycélium luminescent",
        "fenetre_badge": "LOI_PASSIVE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_REVE",
          "PIC_ALTERATION",
          "PIC_INSECTE"
        ],
        "mots_cles_plateau": {
          "face_1": "Loi · Déviation vers Rêve → Altérer + recycle si < 2 · Prod = 1 Insecte Réglette OU Altérer",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Déviations vers Rêves Altèrent et recyclent"
      },
      "carte_joueur": {
        "titre_complet": "Le Mycélium luminescent, réseau spectral des racines noires",
        "entite_illustree": "Entrelacs de champignons bioluminescents bleu-vert sous un grand arbre creux",
        "brief_illustration": "Sous l’humus sombre d’un grand arbre creux colonisé par les insectes, un entrelacs de champignons bioluminescents bleu-vert relie les galeries souterraines jusqu’aux chenilles d’un bulldozer égaré dans une brume de spores.",
        "pitch_ambiance": "Ce que l’insecte touche là-haut résonne aussitôt sous l’humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé.",
        "texte_regle": {
          "face_1": "Spores de déviation (Loi passive) : chaque fois qu’un Insecte défaussé sur la Réglette dévie une machine mobile (±1) sur le rang d’un Rêve, Altérez cette machine ; de plus, si ce Nid porte strictement moins de 2 Insectes, replacez l’Insecte défaussé sur ce Nid au lieu de le rendre à la réserve. Filaments oniriques (Production défendue) : après la production de ce Nid, choisissez — déplacez 1 Insecte de ce Nid directement sur un rang 1–6 de la Réglette ; ou Altérez 1 machine mobile de votre choix.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Nourrit la Réglette en Insectes de déviation depuis n’importe quelle parcelle (Filaments oniriques) et recycle les déviations vers les Rêves en Altérations.",
          "renoncement": "Envoyer un Insecte sur la Réglette laisse ce Nid sous le seuil de 2 Insectes jusqu’au prochain recyclage par déviation."
        }
      },
      "temoins": [
        {
          "id": "M5_T1",
          "statut": "OK",
          "resume": "Le Mycélium luminescent défendu envoie 1 Insecte sur le rang 4 (Filaments oniriques) ; au tour suivant, la déviation ±1 vers un Rêve au rang 3 Altère la machine et recycle l’Insecte sur ce Nid (< 2)."
        }
      ],
      "heuristique_bot": "Défendu dès que possible pour alimenter les rangs adjacents aux Rêves en Insectes ; déclenche le recyclage automatique sur toute déviation vers un Rêve.",
      "engine_sync_status": "ACTIVE_VERIFIED",
      "statut_conception": "VALIDE_V6_4"
    }
  }
};

const CANON_V6_3_PASSE1 = {
  "_meta": {
    "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
    "schema_version": "6.3.1",
    "socle_verrouille": "6.2.0",
    "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
    "etape_active": "ETAPE_3_AFFINAGE_EDITORIAL",
    "statut_global": "CONCEPTION_EN_COURS",
    "genere_le": "2026-11-26",
    "slots_count": 30,
    "c02_supprime": true,
    "panel_id": "canon_v6_3",
    "source_modele": "Assemblage officiel Étape 2b : 22 tuiles panel_1 + 4 tuiles panel_2 (G3 reclassé hors-twist, G11, R2, R5) + 4 tuiles panel_3 (G10, R8, R10, M5)",
    "murs_porteurs_verrouilles": [
      "M1_TEMPS_BATAILLE",
      "M2_CONSERVATION_THERMIQUE",
      "M3_INTEGRITE_PLATEAU_ET_ICONES",
      "M4_AUTONOMIE_PLANCHER_SOLO"
    ],
    "note_retrocompatibilite": "Panel canonique v6.3.1 Passe 1 assemblé (30 tuiles rédigées, 0 erreur sur M1..M4 + I01..I07 + Q01..Q02, prêt pour l'affinage éditorial Étape 3) : le build Doc Studio actif reste transitoirement sur contracts/tiles_canon_v6_2.json (archive sanctuarisée) jusqu'aux Étapes 3–4."
  },
  "carte_des_roles": {
    "statut": "CANON_PASSE_1_ASSEMBLE_V6_3_1",
    "provenance_assemblage": {
      "panel_1": [
        "G1",
        "G2",
        "G4",
        "G5",
        "G6",
        "G7",
        "G8",
        "G9",
        "G12",
        "G13",
        "G14",
        "G15",
        "R1",
        "R3",
        "R4",
        "R6",
        "R7",
        "R9",
        "M1",
        "M2",
        "M3",
        "M4"
      ],
      "panel_2": [
        "G3",
        "G11",
        "R2",
        "R5"
      ],
      "panel_3": [
        "G10",
        "R8",
        "R10",
        "M5"
      ],
      "ajustements": [
        "G3 (L’Atèle, issu de panel_2) reclassé en brique classique hors-twist (est_twist=false, TWIST_2K3 retiré de roles_portes, CATALYSEUR_EVEIL conservé) ; les 6 Twists 2K3 du canon sont exactement {G2, G7, R4} + {G12, R10, M3}."
      ]
    },
    "partition_2K3": {
      "triangle_1": "R>M (G2) → M>H (G7) → H>R (R4)",
      "triangle_2": "O>E (G12) → E>I (R10) → I>O (M3)"
    },
    "etoile_lois_passives": "Les 3 lois passives (R7=E>M, R8=E>R, M5=I>E) forment une étoile centrée sur E (Entités) : au plus 2 lois sur chacune des 197 assises (0 sur 53, 1 sur 96, 2 sur 48).",
    "roles": {
      "catalyseurs_eveil": [
        "G1=M>R",
        "G3=M>O",
        "G4=O>M",
        "G5=R>O",
        "G8=M>E",
        "G9=R>H",
        "G10=R>E",
        "G11=O>H",
        "G12=O>E",
        "G13=M>I",
        "G14=R>I",
        "G15=O>I"
      ],
      "leviers_reve": [
        "G8=M>E",
        "R1=H>E",
        "R4=H>R",
        "R8=E>R",
        "R9=E>O",
        "R10=E>I"
      ],
      "synergies_enracinement": [
        "G7=M>H",
        "G15=O>I",
        "R1=H>E",
        "R2=E>H"
      ],
      "lois_passives": [
        "R7=E>M",
        "R8=E>R",
        "M5=I>E"
      ],
      "autonomie_A0": [
        "R1=H>E",
        "R2=E>H",
        "R6=H>I",
        "R10=E>I",
        "M4=I>H",
        "M5=I>E"
      ],
      "twists_2K3": [
        "G2=R>M",
        "G7=M>H",
        "G12=O>E",
        "R4=H>R",
        "R10=E>I",
        "M3=I>O"
      ]
    }
  },
  "rapport_audit_197": {
    "verdict_global": "OK",
    "c02_word_count_purged": true,
    "assises_verifiees": 197,
    "compositions_verifiees": 42,
    "M1_TEMPS_BATAILLE": "OK",
    "M2_CONSERVATION_THERMIQUE": "OK",
    "M3_INTEGRITE_PLATEAU_ET_ICONES": "OK",
    "M4_AUTONOMIE_PLANCHER_SOLO": "OK",
    "C01_mem_debt": "OK",
    "I01_cloture_elargie_197": "OK",
    "I02_autonomie_A0": "OK",
    "I03_divergence_lisiere": "OK",
    "I04_couverture_eveil": {
      "verdict": "OK",
      "nombre": 12
    },
    "I05_couverture_sommeil": {
      "verdict": "OK",
      "nombre_leviers": 6,
      "lisieres_E_couvertes": [
        "E–M",
        "E–R",
        "E–O",
        "E–I"
      ]
    },
    "I06_enracinement": {
      "verdict": "OK",
      "nombre": 4
    },
    "Q01_lois_passives": {
      "verdict": "OK",
      "nombre": 3,
      "max_par_assise": 2
    },
    "Q02_twists_2K3": {
      "verdict": "OK",
      "nombre": 6
    },
    "V63_schema_et_casting": "OK",
    "synergies_optionnelles_couvertes": 34
  },
  "tuiles_ciblees": {
    "G1": {
      "id": "G1",
      "alias_oriente": "M>R",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "R",
      "couple": [
        "M",
        "R"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Croc Reptile (R) posté sur la parcelle du Duel (M) → parade du Croc qui scelle le Territoire tenu → Piégeage en cascade",
      "entrees_plancher": [
        "DUEL",
        "CROC"
      ],
      "entrees_synergie": [],
      "entrees": [
        "DUEL",
        "CROC"
      ],
      "sorties": [
        "CROC_POSTE",
        "CROC",
        "TERRITOIRE",
        "BLEU"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume Piégeage, l’icône même où siège le Jaguar, d’où une seconde activation qui le reposte aussitôt pour la frappe suivante. Deux activations = deux parades du Croc et un Duel scellé sur Territoire tenu dès la première.",
      "tags": [
        "CROC",
        "DUEL",
        "BERGE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Jaguar",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_CROC",
          "PIC_DUEL",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Croc → parcelle du Duel · parade du Croc = Territoire tenu",
          "face_2": "Croc et Duel → toute parcelle ciblée · machine parée = 1 Rouge en Bleu",
          "enracine": null
        },
        "resume_plateau": "Le Croc chasse aux côtés du Duel"
      },
      "carte_joueur": {
        "titre_complet": "Le Jaguar, seigneur des berges",
        "entite_illustree": "Le Jaguar (Panthera onca) — grand félin tacheté, animal entier sur une plage de sable noir du rio, surgissant des herbes vers un caïman qui se chauffe",
        "brief_illustration": "Plan large crépusculaire sur une berge de várzea : le Jaguar entier, musculature tendue, rosettes nettes, avance à demi immergé dans l’eau noire ; au premier plan, une gueule de caïman entrouverte (évocation du Croc) ; au fond, des troncs coupés et la lueur orangée d’une machine. Palette ocre, vert profond, reflets d’or sur l’eau.",
        "pitch_ambiance": "Le Jaguar ne craint ni l’eau ni les écailles : il chasse le caïman sur sa propre berge et le tue d’une seule morsure au crâne. Là où il rôde, la rive appartient de nouveau à la forêt.",
        "texte_regle": {
          "face_1": "Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur la parcelle qui porte le jeton Duel, quelle que soit sa face. Le Croc y pare en premier, comme toujours, puis regagne la réserve Reptile. Pacte de la berge : tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne aussi le Duel sur Territoire tenu, comme si un Défenseur l’avait parée. Si le Duel n’est pas en forêt, le Jaguar ne fait rien.",
          "face_2": "Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur n’importe quelle parcelle ciblée, de n’importe quel rayon. Le jeton Duel peut traverser le fleuve avec lui : déplacez-le sur cette parcelle, sur sa face actuelle, même sans Défenseur Mammifère. Le Croc y pare en premier puis regagne la réserve Reptile ; tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne le Duel sur Territoire tenu. Morsure au crâne : la machine dont le Croc vient de parer la frappe retourne aussi 1 de ses Rouges en Bleu.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Où poster le Croc : sur le Duel pour sceller un Territoire tenu, ou (Face 2) sur la parcelle ciblée la plus menacée d’un autre rayon, Duel compris.",
          "renoncement": "Déplacer le Croc dégarnit la parcelle où une Écaille l’avait posé ; et l’icône Piégeage ne s’allume que si une frappe tombe réellement sur lui."
        }
      },
      "temoins": [
        {
          "id": "G1_T1",
          "resume": "Croc en réserve, Duel face Défi sur la parcelle 3 du rayon M ; le Jaguar s’active : le Croc y est posté ; le Bulldozer frappe la parcelle 3 : le Croc pare (Piégeage) et regagne la réserve ; le Duel passe sur Territoire tenu.",
          "etat_attendu_verifie": {
            "croc": "RESERVE_R",
            "duel": "TERRITOIRE_TENU",
            "icone_allumee": "PIEGEAGE",
            "arbres_p3": "inchanges"
          },
          "statut": "A_CODER"
        },
        {
          "id": "G1_T2",
          "resume": "Face 2 : Croc et Duel postés sur la parcelle 2 ciblée du rayon H ; une Abatteuse portant 2 Rouges frappe, le Croc pare : Duel sur Territoire tenu, Abatteuse à 1 Rouge et 1 Bleu.",
          "etat_attendu_verifie": {
            "duel_parcelle": "H_p2",
            "duel_face": "TERRITOIRE_TENU",
            "abatteuse": {
              "rouges": 1,
              "bleus": 1
            }
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Piégeage. Poster le Croc sur le Duel si une machine révélée vise sa parcelle ; sinon (Face 2) sur la parcelle ciblée la plus boisée. Ne jamais retirer le Croc d’une parcelle dont la frappe n’est pas résolue sans cible plus menacée.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G2": {
      "id": "G2",
      "alias_oriente": "R>M",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "M",
      "couple": [
        "R",
        "M"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Territoire tenu (M) ou 2 Défenseurs sur la dernière parcelle → machine arrachée à son Ratissage (jeton remis au sac) → recul",
      "entrees_plancher": [
        "RATISSAGE",
        "DUEL"
      ],
      "entrees_synergie": [
        "TERRITOIRE"
      ],
      "entrees": [
        "RATISSAGE",
        "DUEL",
        "TERRITOIRE"
      ],
      "sorties": [
        "RATISSAGE_ROMPU",
        "RECUL",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": "Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la même dernière parcelle : la première activation arrache l’Abatteuse, la seconde le Bulldozer, tant que le Duel tient la parcelle. En Face 2, la seconde activation peut aussi noyer la machine mobile qui s’apprête à frapper le Duel.",
      "tags": [
        "RATISSAGE",
        "DUEL",
        "RECUL",
        "TWIST"
      ],
      "tuile_plateau": {
        "nom_court": "L’Anaconda vert",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_DUEL",
          "PIC_RECUL"
        ],
        "mots_cles_plateau": {
          "face_1": "Ratissage sur Territoire tenu ou 2 Défenseurs → jeton au sac · recul 1",
          "face_2": "Duel ou 2 Défenseurs · Ratissage arraché · machine mobile noyée et reculée",
          "enracine": null
        },
        "resume_plateau": "Arrache une machine à son Ratissage"
      },
      "carte_joueur": {
        "titre_complet": "L’Anaconda vert, l’étau des eaux dormantes",
        "entite_illustree": "L’Anaconda vert (Eunectes murinus) — serpent géant entier, anneaux olive tachetés de noir, enroulé dans les eaux d’un igapó",
        "brief_illustration": "Vue semi-immergée : l’Anaconda vert entier, anneaux déroulés sous la surface, enserre les chenilles d’une machine de déboisement à demi engloutie ; sur la berge, les empreintes fraîches d’un jaguar. Lumière verte filtrée, eau sombre et miroitante.",
        "pitch_ambiance": "L’Anaconda attend des heures, invisible sous la lentille d’eau. Quand la proie s’aventure au bord, chaque expiration resserre ses anneaux, et il l’entraîne là où plus rien ne pousse : au fond.",
        "texte_regle": {
          "face_1": "Quand l’Anaconda vert s’active : choisissez une machine en Ratissage dont la parcelle porte le jeton Duel face Territoire tenu, ou au moins 2 Défenseurs. L’étau l’arrache à son Ratissage : reprenez le jeton Machine glissé sous elle et remettez-le dans le sac ; la machine redevient mobile et recule d’1 parcelle vers la bordure (en sautant les Routes Forestières), en conservant tous ses jetons Puissance. Faute de jeton tiré, elle n’attaque plus avant le ménage ; au ménage, n’étant plus sur la dernière parcelle, elle ne rentre pas en Ratissage.",
          "face_2": "Quand l’Anaconda vert s’active : choisissez une machine dont la parcelle porte le jeton Duel (sur l’une ou l’autre face) ou au moins 2 Défenseurs. Si elle est en Ratissage, l’étau l’en arrache : reprenez son jeton Machine et remettez-le dans le sac ; elle redevient mobile, recule d’1 parcelle vers la bordure (en sautant les Routes Forestières) en conservant ses jetons Puissance, et n’attaque plus avant le ménage. Si elle est mobile et n’a pas encore attaqué, l’Anaconda la noie : inclinez son jeton Machine (elle est annulée) et faites-la reculer d’1 parcelle vers la bordure.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Arracher maintenant la machine en Ratissage, ou la laisser au fond tant que son jeton n’alourdit pas le sac.",
          "renoncement": "Le jeton Machine rendu au sac rend chaque pioche future plus dangereuse ; et le Duel engagé sur la dernière parcelle ne couvre plus la lisière."
        }
      },
      "temoins": [
        {
          "id": "G2_T1",
          "resume": "Bulldozer en Ratissage (2 Rouges) sur la dernière parcelle du rayon R, Duel face Territoire tenu sur cette parcelle ; l’Anaconda s’active au rang 2 : jeton remis au sac, Bulldozer mobile en parcelle 3, aucune frappe de Ratissage.",
          "etat_attendu_verifie": {
            "bulldozer": {
              "position": "p3",
              "ratissage": false,
              "rouges": 2
            },
            "sac_jetons_machine": "+1",
            "frappes_ratissage": 0
          },
          "statut": "A_CODER"
        },
        {
          "id": "G2_T2",
          "resume": "Face 2 : une Abatteuse mobile du rang 5 vise la parcelle du Duel (face Défi) ; l’Anaconda s’active au rang 2 : Abatteuse annulée (jeton incliné) et reculée d’1 parcelle.",
          "etat_attendu_verifie": {
            "abatteuse": {
              "annulee": true,
              "recul": 1
            }
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Parade. Arracher en priorité la machine en Ratissage la plus chargée en Rouges ; refuser si le sac ne contient plus qu’1 Sabotage et qu’il reste au moins 4 tours.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G3": {
      "id": "G3",
      "alias_oriente": "M>O",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "O",
      "couple": [
        "M",
        "O"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "ARBRE + ROUTE + DEFENSEUR_REDEPLOYE + PLUME → DEFENSEUR_REDEPLOYE",
      "entrees_plancher": [
        "ARBRE",
        "ROUTE",
        "DEFENSEUR_REDEPLOYE"
      ],
      "entrees_synergie": [
        "PLUME"
      ],
      "entrees": [
        "ARBRE",
        "ROUTE",
        "DEFENSEUR_REDEPLOYE",
        "PLUME"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Deux traversées amènent les deux pions nécessaires à une Parade ou desservent deux rayons différents.",
      "tags": [
        "CANOPEE",
        "TRAVERSEE"
      ],
      "tuile_plateau": {
        "nom_court": "L’Atèle",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_ARBRE",
          "PIC_ROUTE",
          "PIC_DEFENSEUR",
          "PIC_PLUME"
        ],
        "mots_cles_plateau": {
          "face_1": "Deux cimes · traverse",
          "face_2": "Plume · trajet en L",
          "enracine": null
        },
        "resume_plateau": "Deux cimes · traverse / Plume · trajet en L"
      },
      "carte_joueur": {
        "titre_complet": "L’Atèle",
        "entite_illustree": "Atèle dans la canopée",
        "brief_illustration": "Atèle entier suspendu par la queue entre deux couronnes. En contrebas, une trouée coupe le chemin radial.",
        "pitch_ambiance": "L’atèle essaie le poids d’une branche avant de lâcher la précédente. Au-dessous de lui, le chemin a disparu.",
        "texte_regle": {
          "face_1": "À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux. Il traverse leur frontière entre deux parcelles de même profondeur portant chacune un Arbre debout. Avant de traverser, il peut faire un pas radial sur son rayon, en sautant les Routes. Le Duel reste en place.",
          "face_2": "À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux, ou entre le rayon portant la Plume et un de ses voisins. Traversez entre deux parcelles de même profondeur portant chacune un Arbre. Vous pouvez ajouter un pas radial avant et un après la traversée, en sautant les Routes. Le Duel reste en place.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quelle cime peut-on dégarnir pour tenir l’autre rive ?",
          "renoncement": "Le pion quitte réellement sa première ligne de défense."
        }
      },
      "temoins": [
        {
          "id": "G3_T1",
          "resume": "En Face 2, un Défenseur quitte M1, saute la Route M2 jusqu’à M3, traverse entre les arbres M3 et O3, puis descend en O4. Il rejoint le Défenseur qui attend un Ratissage de seuil 2.",
          "etat_attendu_verifie": {
            "entree": {
              "M": [
                2,
                null,
                1,
                2
              ],
              "O": [
                2,
                2,
                1,
                1
              ],
              "depart": 1,
              "garde_O4": 1,
              "seuil": 2
            },
            "transition_python": "i=s['depart']-1\nsuivant=lambda rayon,x: next(j for j in range(x+1,len(rayon)) if rayon[j] is not None)\npassage=suivant(s['M'],i)\nassert min(s['M'][passage],s['O'][passage])>0\narrivee=suivant(s['O'],passage)\nr=[passage+1,arrivee+1,s['garde_O4']+1>=s['seuil']]",
            "attendu": [
              3,
              4,
              true
            ]
          },
          "statut": "OK"
        },
        {
          "id": "G3_T2",
          "resume": "Deux traversées F1 entre deux cimes de même profondeur portent deux Défenseurs de M vers une cible d’O de seuil 2.",
          "etat_attendu_verifie": {
            "entree": {
              "pions": [
                2,
                0
              ],
              "arbres": [
                1,
                2
              ],
              "seuil": 2
            },
            "transition_python": "for _ in range(2):\n    if min(s['arbres'])>0 and s['pions'][0]:\n        s['pions'][0]-=1\n        s['pions'][1]+=1\nr=[s['pions'],s['pions'][1]>=s['seuil']]",
            "attendu": [
              [
                0,
                2
              ],
              true
            ]
          },
          "statut": "OK"
        }
      ],
      "heuristique_bot": "Chercher une destination qui fait atteindre le seuil exact. Écarter les trajets qui feraient perdre une Parade plus coûteuse au départ.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G4": {
      "id": "G4",
      "alias_oriente": "O>M",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "M",
      "couple": [
        "O",
        "M"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Pari Gardien → encoche libre (ou 2e pari solo en repli) ; Territoire tenu → Défi = 2e cri ; Face 2 : réveil d’un autre Gardien",
      "entrees_plancher": [
        "GARDIEN"
      ],
      "entrees_synergie": [
        "TERRITOIRE"
      ],
      "entrees": [
        "GARDIEN",
        "TERRITOIRE"
      ],
      "sorties": [
        "PARI_GLISSE",
        "ACTIVATION_RELAIS",
        "DEFI"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_RESONANCE"
      ],
      "double_ouverture": "Chaque cri fait progresser un pari différent : deux activations bouclent le pari d’un Gardien qui ne s’allume jamais (deux glissements sur la même tuile) ou en sécurisent deux. En Face 2, chaque cri déclenche en plus le pouvoir du Gardien réveillé, et chaque 1re activation ainsi provoquée relance la Résonance. Seul en piste, une seule activation boucle son propre pari de deux Défenseurs.",
      "tags": [
        "PARI",
        "ENCOCHE",
        "CRI_ALARME"
      ],
      "tuile_plateau": {
        "nom_court": "L’Ara rouge",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_RESONANCE",
        "pictogrammes": [
          "PIC_PARI_ENCOCHE",
          "PIC_RESONANCE",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "1 pari d’un autre Gardien → encoche · Territoire tenu → Défi = 2e cri · seul en piste : son 2e pari glisse aussi",
          "face_2": "Un autre Gardien avec pari s’active · Territoire tenu → Défi = 2e réveil · seul en piste : son 2e pari glisse aussi",
          "enracine": null
        },
        "resume_plateau": "Cri d’alarme qui fait avancer les paris"
      },
      "carte_joueur": {
        "titre_complet": "L’Ara rouge, sentinelle de la collpa",
        "entite_illustree": "L’Ara rouge (Ara macao), animal entier agrippé à une falaise d’argile",
        "brief_illustration": "L’Ara rouge (Ara macao), animal entier : perroquet écarlate, jaune et bleu, agrippé à une falaise d’argile (collpa) au milieu de sa volée, le bec ouvert sur le cri d’alarme.",
        "pitch_ambiance": "À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.",
        "texte_regle": {
          "face_1": "Le cri d’alarme. Quand l’Ara rouge s’active : faites glisser 1 Défenseur posé en pari sur un autre Gardien construit vers une encoche libre de ce même Gardien. Cela ne résout pas le pouvoir de ce Gardien et n’allume aucune icône. Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour faire glisser de la même façon un 2e Défenseur, posé en pari sur un Gardien différent du premier.\nSentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, l’Ara crie pour sa propre volée : faites aussi glisser son second pari, s’il en porte un, dans son encoche encore libre.",
          "face_2": "La volée se lève. Quand l’Ara rouge s’active : choisissez un autre Gardien construit qui porte au moins 1 Défenseur en pari ; il s’active aussitôt (son Défenseur glisse dans une encoche et vous résolvez son pouvoir comme si son icône venait de s’allumer ; s’il s’agit de sa 1re activation du tour, la Résonance la compte). Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour réveiller de la même façon un 2e Gardien, différent du premier. L’Ara ne se réveille jamais lui-même.\nSentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, faites aussi glisser le second pari de l’Ara, s’il en porte un, dans son encoche encore libre, sans résoudre son pouvoir une seconde fois.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quel pari faire progresser — celui du Gardien le plus en retard, ou celui dont le pouvoir doit frapper maintenant (Face 2).",
          "renoncement": "Retourner le Duel sur Défi pour un 2e cri libère l’avancée des machines de sa parcelle aux rangs 3 et 6 ; construit en premier, l’Ara posé sur Parade s’active seul, mais renonce à la cascade de la Résonance tant qu’il reste en piste."
        }
      },
      "temoins": [
        {
          "id": "G4_T1",
          "resume": "La Matamata porte 1 pari et 0 encoche occupée ; l’Ara s’active : le pari glisse dans l’encoche ; en fin d’attaques, 0 pion sur la Matamata et 1 encoche : pari gagné.",
          "etat_attendu_verifie": {
            "matamata_encoches": 1,
            "pari_gagne": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "G4_T2",
          "resume": "Plancher (Tour 2) : l’Ara, construit au Tour 1 et posé sur Parade (icône de repli), est le seul Gardien en piste ; il porte 2 paris. Après une parade au rang 1, il s’active : son 1er pari glisse dans une encoche ; sentinelle seule, le 2nd aussi. En fin d’attaques, 0 pion sur la tuile et 2 encoches occupées : pari gagné, l’Ara passe en Face 2.",
          "etat_attendu_verifie": {
            "ara_encoches": 2,
            "face_2": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Résonance (ou Parade en repli si premier Gardien construit). Glisser d’abord le pari du Gardien dont l’icône a le moins de chances de s’allumer ; n’utiliser l’Écho (Territoire tenu → Défi) que si l’Éveil est atteignable au tour même.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G5": {
      "id": "G5",
      "alias_oriente": "R>O",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "O",
      "couple": [
        "R",
        "O"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Plume de Vigie (O) → Piège garanti là où elle signale (repli R ou O) ; Bleu bu (amplificateur) → Croc en Face 1 ou second plongeon en Face 2",
      "entrees_plancher": [
        "PLUME"
      ],
      "entrees_synergie": [
        "BLEU"
      ],
      "entrees": [
        "PLUME",
        "BLEU"
      ],
      "sorties": [
        "PIEGE",
        "CROC"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Chaque Piège qui pare allume Piégeage, l’icône de l’Iguane : la chute appelle la chute, une fois par pari. Deux chutes couvrent les deux parcelles d’un « En avançant » (Sur place et Devant), ou deux fois la même parcelle visée par l’Abatteuse puis le Bulldozer. Avec le Toucan à ses côtés, chaque chute boit son Bleu : le Croc tombe à chaque fois s’il a regagné la réserve (Face 1), et quatre Pièges couvrent la forêt (Face 2).",
      "tags": [
        "SURCHAUFFE",
        "PIEGE",
        "PLUME"
      ],
      "tuile_plateau": {
        "nom_court": "L’Iguane vert",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_PIEGE",
          "PIC_PLUME",
          "PIC_CROC",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Piège là où signale la Plume (sinon rayon R ou O) · Bleu bu = le Croc tombe aussi",
          "face_2": "Piège + Croc sur toute parcelle ciblée · Bleu bu = second plongeon",
          "enracine": null
        },
        "resume_plateau": "Tombe en Piège au cri des oiseaux"
      },
      "carte_joueur": {
        "titre_complet": "L’Iguane vert, dormeur des hautes branches",
        "entite_illustree": "L’Iguane vert (Iguana iguana), animal entier allongé sur une branche au-dessus de l’eau",
        "brief_illustration": "L’Iguane vert (Iguana iguana), animal entier : grand lézard à la crête dorsale dressée, allongé au soleil sur une branche au-dessus de l’eau, l’œil tourné vers un oiseau qui donne l’alerte.",
        "pitch_ambiance": "L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.",
        "texte_regle": {
          "face_1": "La chute au cri des oiseaux. Quand l’Iguane vert s’active, il se laisse tomber : posez 1 Piège sur une parcelle ciblée qui n’en porte pas encore, sur le rayon désigné par la Plume de Vigie, ou visée par une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu ou ne signale aucune parcelle ciblée, il tombe au plus près : sur une parcelle ciblée du rayon Reptile ou du rayon de l’Oiseau. S’il n’y en a aucune, il guette : posez le Piège sur n’importe quelle parcelle libre de Piège ordinaire du rayon Reptile, où il attendra la prochaine frappe.\nBoire la chaleur (amplificateur) : avant de tomber, vous pouvez boire 1 Bleu : retirez-le d’une machine de n’importe quel rayon et remettez-le dans la réserve (la machine perd la Surchauffe correspondante). Gorgé de chaleur, l’Iguane tombe avec ses mâchoires : si le Croc est dans la réserve Reptile, postez-le sur la parcelle du Piège. Il y pare en premier, le Piège ensuite.",
          "face_2": "Le plongeon. Quand l’Iguane vert s’active, il plonge où il veut : posez 1 Piège sur n’importe quelle parcelle ciblée qui n’en porte pas encore, de n’importe quel rayon, et postez-y le Croc s’il est dans la réserve Reptile (si la Plume de Vigie est face Chaud, prenez le Croc où qu’il se trouve sur le plateau). Le Croc pare en premier, le Piège ensuite.\nBoire la chaleur (amplificateur) : avant de plonger, vous pouvez boire 1 Bleu (retiré d’une machine de n’importe quel rayon, rendu à la réserve) : l’Iguane plonge une seconde fois et pose 1 second Piège sur une autre parcelle ciblée libre de Piège ordinaire. Chacune de ces parades allume Piégeage.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Tomber seul là où la Plume l’indique, ou boire un Bleu pour emporter le Croc (Face 1) ou plonger deux fois (Face 2) ; de préférence le Bleu d’une machine déjà annulée, ou dont le Seuil est déjà tombé à 1.",
          "renoncement": "La machine qui perd son Bleu redevient plus difficile à parer, et ce Bleu manquera au Toucan pour la faire caler ; le Croc emporté ne garde plus la parcelle où une Écaille l’avait posté."
        }
      },
      "temoins": [
        {
          "id": "G5_T1",
          "resume": "Plancher sans Toucan (Tour 2, Acte 1) : aucun Bleu en jeu. La Plume est posée face Chaud au pied du rayon O, dont la parcelle 2 est visée au rang 4 par l’Abatteuse (Sur place) puis au rang 5 par le Bulldozer (Devant). Un Piège pare au rang 1 (Piégeage) : l’Iguane (2 paris) tombe sur la parcelle 2 ; au rang 4 son Piège pare l’Abatteuse (Piégeage), seconde activation, nouveau Piège sur la même parcelle qui pare le Bulldozer au rang 5.",
          "etat_attendu_verifie": {
            "pieges_poses": 2,
            "arbres_sauves": 2
          },
          "statut": "A_CODER"
        },
        {
          "id": "G5_T2",
          "resume": "Amplifié par le Toucan (Face 1) : le Toucan a retourné 1 Rouge en Bleu sur l’Abatteuse du rayon M, annulée à l’ouverture par un Rêve. La Plume désigne le rayon R, dont la parcelle 3 est visée aux rangs 4 et 5. Après une parade de Piège au rang 2, l’Iguane boit le Bleu de la machine annulée et tombe avec le Croc sur la parcelle 3 : le Croc pare l’Abatteuse, le Piège pare le Bulldozer (deux fois Piégeage).",
          "etat_attendu_verifie": {
            "bleu_bu": 1,
            "croc_et_piege_poses": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Piégeage. En autonomie, poser le Piège sur la parcelle ciblée signalée par la Plume qui porte le plus d’Arbres debout ; avec un Bleu disponible, boire celui d’une machine annulée ou à Seuil 1 pour ajouter le Croc (Face 1) ou doubler la pose de Pièges (Face 2).",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G6": {
      "id": "G6",
      "alias_oriente": "O>R",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "R",
      "couple": [
        "O",
        "R"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Rouge → Bleu (Surchauffe) sur la cible désignée par la Plume (O) ; Face 2 : 0 Rouge et 2 Bleus = machine calée ; ces Bleus nourrissent l’Iguane (R)",
      "entrees_plancher": [
        "ROUGE",
        "PLUME"
      ],
      "entrees_synergie": [
        "BLEU"
      ],
      "entrees": [
        "ROUGE",
        "PLUME",
        "BLEU"
      ],
      "sorties": [
        "BLEU",
        "ANNULATION_SURCHAUFFE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": "La surchauffe se construit en deux temps : la première activation convertit un Rouge, la seconde le dernier Rouge de la même machine ; en Face 2, celle-ci cale aussitôt (0 Rouge, 2 Bleus) avant même d’attaquer. Sur Résonance, le Toucan s’active de nouveau à chaque 1re activation d’un autre Gardien.",
      "tags": [
        "SURCHAUFFE",
        "PLUME"
      ],
      "tuile_plateau": {
        "nom_court": "Le Toucan toco",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_RESONANCE",
        "pictogrammes": [
          "PIC_ROUGE",
          "PIC_BLEU",
          "PIC_PLUME",
          "PIC_ANNULATION"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Rouge → Bleu sur la cible désignée par la Plume",
          "face_2": "1 Rouge → Bleu partout · 0 Rouge et 2 Bleus = machine calée",
          "enracine": null
        },
        "resume_plateau": "Rend la chaleur aux machines"
      },
      "carte_joueur": {
        "titre_complet": "Le Toucan toco, le bec-radiateur",
        "entite_illustree": "Le Toucan toco (Ramphastos toco) — oiseau entier au bec orange démesuré, perché au sommet d’un arbre émergent",
        "brief_illustration": "Contre-jour brûlant : le Toucan toco entier, bec orange incandescent, se découpe sur un ciel blanc de chaleur ; des volutes de chaleur partent de son bec vers une machine en contrebas dont les jauges virent au bleu ; un iguane se chauffe sur une branche voisine. Orange, noir, bleu électrique.",
        "pitch_ambiance": "Le bec du toucan toco est un radiateur vivant : il y dirige son sang pour relâcher la chaleur du jour. Au-dessus des machines brûlantes, il rend la fournaise au monde, et le métal s’essouffle.",
        "texte_regle": {
          "face_1": "Quand le Toucan toco s’active : il rayonne : retournez 1 Rouge en Bleu sur une machine, mobile ou en Ratissage, du rayon désigné par la Plume de Vigie, ou sur une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu, visez une machine du rayon de l’Oiseau ou d’un rayon voisin.",
          "face_2": "Quand le Toucan toco s’active : il rayonne sur toute la forêt : retournez 1 Rouge en Bleu sur une machine de n’importe quel rayon, mobile ou en Ratissage. Coup de chaleur : si cette machine ne porte alors plus aucun Rouge mais au moins 2 Bleus, et qu’elle n’a pas encore attaqué, elle cale : inclinez son jeton Machine à 90° (pour une machine en Ratissage, tournez la machine elle-même d’un quart de tour) ; elle est annulée jusqu’au ménage, où elle reprend sa position.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Disperser la Surchauffe pour abaisser plusieurs Seuils, ou la concentrer sur une seule machine pour la faire caler (Face 2).",
          "renoncement": "Chaque Bleu concentré sur la machine à caler n’aide pas les autres parades ; et l’Iguane voisin voudra boire ces mêmes Bleus."
        }
      },
      "temoins": [
        {
          "id": "G6_T1",
          "resume": "Abatteuse en Mode Assaut, 2 Rouges, parcelle gravée 3 (Seuil 5) ; le Toucan s’active : 1 Rouge et 1 Bleu, Seuil 3.",
          "etat_attendu_verifie": {
            "abatteuse": {
              "rouges": 1,
              "bleus": 1
            },
            "seuil_parade": 3
          },
          "statut": "A_CODER"
        },
        {
          "id": "G6_T2",
          "resume": "Face 2 : Bulldozer à 1 Rouge et 1 Bleu au rang 6, pas encore résolu ; le Toucan s’active : 0 Rouge, 2 Bleus, le Bulldozer cale et n’attaque pas.",
          "etat_attendu_verifie": {
            "bulldozer": {
              "rouges": 0,
              "bleus": 2,
              "annule": true
            }
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Résonance. Convertir d’abord le Rouge d’une machine en Assaut qui n’a pas encore attaqué ; en Face 2, finir la machine à 1 seul Rouge qui porte déjà au moins 1 Bleu.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G7": {
      "id": "G7",
      "alias_oriente": "M>H",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "H",
      "couple": [
        "M",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "TWIST_2K3",
        "ENRACINEMENT"
      ],
      "est_twist": true,
      "vecteurs": "Duel (M) ou Chamane (H) posé sur une Route → sentier : parcelle vide plus sautée ; sinon Duel → Chamane = Territoire tenu ; Enraciné au décompte final",
      "entrees_plancher": [
        "ROUTE",
        "DUEL",
        "TAMBOUR",
        "CHANT"
      ],
      "entrees_synergie": [
        "CHAMANE_EN_FORET"
      ],
      "entrees": [
        "ROUTE",
        "DUEL",
        "TAMBOUR",
        "CHANT",
        "CHAMANE_EN_FORET"
      ],
      "sorties": [
        "SENTIER_ROUTE",
        "TERRITOIRE",
        "ARBRE"
      ],
      "paiement": [
        "P_SOUCHE"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Deux pas, deux sentiers : la première activation pose le Duel sur une Route, la seconde y fait descendre un Chamane sur une autre, ou sur la même pour que le sentier survive au départ du Duel. Chaque frappe parée sur un sentier allume Parade, l’icône du Tapir. En Face 2, chaque sentier attire en plus les frappes de ses deux voisines.",
      "tags": [
        "ROUTE",
        "SENTIER",
        "ENRACINEMENT",
        "TWIST"
      ],
      "tuile_plateau": {
        "nom_court": "Le Tapir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_ROUTE",
          "PIC_DUEL",
          "PIC_TAMBOUR"
        ],
        "mots_cles_plateau": {
          "face_1": "Duel ou Chamane sur Route = sentier (parcelle vide, plus sautée) · sinon Duel → Chamane = Territoire tenu",
          "face_2": "+ frappes des parcelles voisines détournées sur le sentier · l’Abatteuse n’en déloge plus le Duel",
          "enracine": "Fin de partie : Duel + Chamane sur une parcelle = 1 repousse de plus"
        },
        "resume_plateau": "Change les Routes en sentiers où les machines s’enlisent"
      },
      "carte_joueur": {
        "titre_complet": "Le Tapir, jardinier des sentiers",
        "entite_illustree": "Le Tapir terrestre (Tapirus terrestris), animal entier avançant dans un sentier de boue",
        "brief_illustration": "Le Tapir terrestre (Tapirus terrestris), animal entier : grand herbivore à la trompe mobile, robe brun sombre et courte crinière, qui avance au crépuscule dans un sentier de boue tracé en travers d’une trouée de bulldozer. Empreintes à quatre doigts dans la glaise ; à l’orée, un chamane suit la piste, tambour à la main.",
        "pitch_ambiance": "Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.",
        "texte_regle": {
          "face_1": "Le sentier battu. Quand le Tapir s’active, choisissez l’un de ses deux pas :\n• Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon — pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère —, ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon. Cette Route devient un sentier.\n• Frayer (toujours possible, même sans aucune Route en jeu) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère. S’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu : les hommes tiennent déjà ce terrain.\nLe sentier : (1) tant qu’il porte le Duel ou un Chamane, le sentier compte comme une parcelle, avec le chiffre gravé de sa case, bien qu’il ne porte ni Arbre ni Souche ; (2) les machines ne le sautent plus : une frappe Devant le vise, une avancée s’y arrête, et une frappe sur le sentier ne fait jamais gagner de Rouge ; (3) il accueille Défenseurs, Piège et autres pièces de défense comme toute parcelle, et le Duel y suit ses règles habituelles (parade → Territoire tenu ; frappe non parée et non piégée → retour en réserve) ; (4) une frappe de Bulldozer non parée le refait Route, et dès qu’il ne porte plus ni Duel ni Chamane (frappe, déplacement, retour des Défenseurs au ménage), il redevient Route : la case est vidée et toute machine qui s’y trouve se replie comme sur une Route qui vient de se créer ; (5) jamais de sentier sur la dernière case d’un rayon, tout sentier redevient aussitôt Route si le Tapir quitte la Piste des Gardiens, et aucun pion Arbre ou Souche n’est jamais déplacé.",
          "face_2": "Le sentier qui égare. Quand le Tapir s’active, choisissez l’un de ses deux pas :\n• Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon (pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère), ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon : elle devient un sentier.\n• Frayer (toujours possible) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère ; s’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu.\nEn Face 2, le sentier obéit aux règles du sentier avec deux pas de plus :\n• Les machines s’égarent : quand une machine attaque, avant de figer ses cibles, si l’une d’elles est la parcelle juste avant ou juste après un sentier sur ce rayon, vous pouvez détourner cette frappe sur le sentier.\n• La boue tient : une frappe d’Abatteuse non parée sur un sentier ne déloge plus le Duel : seul un Bulldozer non paré refait la Route.",
          "enracine": "Les graines du sentier. Au décompte final, en plus de sa repousse habituelle (1 Souche, ou 2 s’il était en Face 2, sur la parcelle qu’il regarde), le Tapir fait repousser 1 Souche de la parcelle qui porte le jeton Duel, si le Tambour ou le Chant s’y tient aussi. Cette clause ne se lit qu’au décompte final."
        },
        "decision_et_renoncement": {
          "choix": "Fouler une Route — avec le Duel, qui tient d’un tour à l’autre, ou avec un Chamane, jusqu’au ménage — ou frayer pour poster le Duel en Territoire tenu auprès d’un Chamane.",
          "renoncement": "Le Duel posé sur un sentier ne garde plus aucune parcelle boisée ; le Chamane qui descend abandonne la parcelle qu’il gardait ; un Bulldozer non paré refait la Route en vidant la case."
        }
      },
      "temoins": [
        {
          "id": "G7_T1",
          "resume": "Le sentier tenu par le Tambour (Tour 3, Acte 1) : sur le rayon H, parcelle 1 (2 Arbres) porte Bulldozer (rang 3), Abatteuse (rang 5) et Tambour ; parcelle 2 est une Route ; parcelle 3 porte 3 Arbres. Après une parade au rang 1, le Tapir (sur Parade) fait descendre le Tambour sur la Route (sentier gravé 2). Au rang 3 le Bulldozer frappe la parcelle 1 puis le sentier (paré par le Tambour, Parade) et s’arrête sur le sentier ; au rang 5 l’Abatteuse frappe le sentier à vide ; au ménage le sentier redevient Route et le Bulldozer se replie en parcelle 1. Parcelle 3 intacte.",
          "etat_attendu_verifie": {
            "parcelle_3_intacte": true,
            "bulldozer_replie_p1": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "G7_T2",
          "resume": "Plancher Frayer (Tour 2, Acte 1, aucune Route en jeu) : le Tapir, construit au Tour 1, porte 1 pari. Sur le rayon M, le Bulldozer en parcelle 1 (2 Arbres) est révélé au rang 6 face à 1 Défenseur Mammifère et le Tambour. Après une parade au rang 2, le Tapir fraye : le Duel quitte la réserve, rejoint le Tambour et arrive face Territoire tenu. Au rang 6, la frappe Sur place est parée et Territoire tenu bloque l’avancée en parcelle 1.",
          "etat_attendu_verifie": {
            "duel_territoire_tenu": true,
            "avancee_bloquee": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Parade. S’il existe une Route devant une parcelle boisée menacée, y poser le Duel ou y faire descendre un Chamane pour absorber les frappes Devant et bloquer l’avancée ; sans Route, Frayer auprès du Tambour/Chant pour verrouiller Territoire tenu. Enraciner en fin de partie si Duel et Chamane peuvent se réunir sur une parcelle à Souches.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G8": {
      "id": "G8",
      "alias_oriente": "M>E",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "E",
      "couple": [
        "M",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "Rêve nagé d’1 rang à gauche ou échangé (Face 2 : 2 rangs / plongée sous son voisin) ; plancher sans Rêve : 1 Altération de la réserve Entités",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "sorties": [
        "POSITION_REVE",
        "ALTERATION",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": "Deux nages font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2), ou compactent deux Rêves séparés : le plus court chemin vers le Sommeil quand les Humains ne sont pas à la table. Posé sur Rêve, le Boto nage dès la première annulation ; posé sur Sabotage, il déplace les Rêves avant même leur résolution. Sans Rêve, deux envoûtements sur deux machines différentes.",
      "tags": [
        "REVE",
        "SOMMEIL",
        "LEVIER",
        "ALTERATION"
      ],
      "tuile_plateau": {
        "nom_court": "Le Boto",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_REVE",
        "pictogrammes": [
          "PIC_AVANCEE_REVE",
          "PIC_REVE",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Rêve glisse d’1 rang à gauche ou échange avec son voisin · aucun Rêve ne nage = 1 Altération",
          "face_2": "1 Rêve glisse de 2 rangs ou plonge sous son voisin · ou échange · aucun Rêve ne nage = 1 Altération",
          "enracine": null
        },
        "resume_plateau": "Fait nager les Rêves vers le rang 1"
      },
      "carte_joueur": {
        "titre_complet": "Le Boto, l’encantado du fleuve",
        "entite_illustree": "Le Boto (Inia geoffrensis), dauphin rose de l’Amazone glissant entre les troncs inondés",
        "brief_illustration": "Le Boto (Inia geoffrensis), dauphin rose de l’Amazone, animal entier, glissant entre les troncs d’une forêt inondée ; sur l’eau sombre se reflète la silhouette d’un homme en blanc.",
        "pitch_ambiance": "Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.",
        "texte_regle": {
          "face_1": "La nage. Quand le Boto s’active : faites nager un Rêve : glissez-le d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent). Si ce rang est occupé, vous pouvez à la place échanger ce Rêve avec le Rêve qui l’occupe (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.\nL’encantado (plancher) : si aucun Rêve ne peut nager (Réglette sans Rêve, ou seul Rêve déjà au rang 1), le Boto envoûte à la place une machine : posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.",
          "face_2": "La plongée vers l’Encante. Quand le Boto s’active : faites glisser un Rêve d’1 ou 2 rangs libres vers la gauche (ses Défenseurs le suivent), ou faites-le plonger sous le Rêve qui le précède : il ressort sur le premier rang libre situé à gauche de celui-ci. Vous pouvez aussi, à la place, échanger deux Rêves voisins (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.\nL’encantado (plancher) : si aucun Rêve ne peut nager ni plonger, posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Faire nager le Rêve vers le rang où des machines viennent d’être révélées (annulation immédiate) ou vers le bloc du Sommeil ; sans Rêve, envoûter la machine qui menacera la parcelle la plus boisée à sa prochaine sortie.",
          "renoncement": "Un Rêve déplacé quitte le rang qu’il couvrait : les machines qui y arriveraient ensuite (déviées ou relues) ne seront plus annulées."
        }
      },
      "temoins": [
        {
          "id": "G8_T1",
          "resume": "Rêve E au rang 5 non résolu, machine révélée au rang 4 ; un Rêve au rang 2 annule et allume Rêve ; le Boto s’active : le Rêve E passe au rang 4 et annule la machine.",
          "etat_attendu_verifie": {
            "reve_e_rang": 4,
            "machine_annulee": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "G8_T2",
          "resume": "Plancher (Tour 2, aucun Rêve construit) : le Boto, construit au Tour 1 et posé sur Sabotage (icône de repli), s’active au premier Sabotage révélé : l’encantado pose 1 Altération sur l’Abatteuse du rayon M en parcelle 2. À sa prochaine révélation, elle compte dans m(r) mais recule en parcelle 1 sans frapper.",
          "etat_attendu_verifie": {
            "alteration_posee": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Rêve (ou Sabotage en repli avant le premier Rêve). Si une machine révélée occupe un rang libre juste à gauche d’un Rêve non résolu, nager vers elle ; sinon compacter vers le rang 1 pour viser le Sommeil ; sans Rêve en jeu, altérer la machine mobile la plus avancée.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G9": {
      "id": "G9",
      "alias_oriente": "R>H",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "H",
      "couple": [
        "R",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Sabotage ou Écaille révélé (Écailles semées par la Pirogue) → cale sous une machine du rayon du Tambour (H) → machine tenue, Ratissage bloqué, Sabotage rallumé à chaque révélation",
      "entrees_plancher": [
        "SABOTAGE",
        "ECAILLE"
      ],
      "entrees_synergie": [
        "TAMBOUR"
      ],
      "entrees": [
        "SABOTAGE",
        "ECAILLE",
        "TAMBOUR"
      ],
      "sorties": [
        "CALE",
        "RECUL",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_SABOTAGE"
      ],
      "double_ouverture": "La première activation pose la cale (souvent sur le Sabotage qui vient d’allumer l’icône), la seconde traîne la machine calée d’1 parcelle vers la bordure ou déplace la cale vers une machine plus menaçante. Et chaque fois que la machine calée est révélée, la cale rallume Sabotage pour toute la Piste.",
      "tags": [
        "CALE",
        "SABOTAGE",
        "TAMBOUR"
      ],
      "tuile_plateau": {
        "nom_court": "Le Caïman noir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_CALE",
          "PIC_SABOTAGE",
          "PIC_TAMBOUR",
          "PIC_RECUL"
        ],
        "mots_cles_plateau": {
          "face_1": "Sabotage révélé → cale · machine tenue sans Ratissage · rayon Reptile, Humain ou du Tambour",
          "face_2": "Cale partout · machine calée révélée = annulée · Sabotage rallumé",
          "enracine": null
        },
        "resume_plateau": "Tient une machine au fond des eaux noires"
      },
      "carte_joueur": {
        "titre_complet": "Le Caïman noir, l’ombre sous la pirogue",
        "entite_illustree": "Le Caïman noir (Melanosuchus niger) — grand crocodilien entier, dos cuirassé à fleur d’eau dans un lac d’eaux noires",
        "brief_illustration": "Nuit sans lune sur un lac d’eaux noires : le Caïman noir entier, seuls ses yeux rouges et sa crête dorsale affleurent ; sa gueule agrippe la roue d’une machine embourbée sur la berge ; en arrière-plan, la proue sculptée d’une pirogue et la lueur d’un tambour. Noirs profonds, reflets rubis.",
        "pitch_ambiance": "Le Caïman noir saisit et ne lâche plus : il tient sa proie contre le fond jusqu’à ce qu’elle cesse de lutter. Les pêcheurs le savent : dans les eaux noires, ce qu’il a pris ne remonte pas.",
        "texte_regle": {
          "face_1": "Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous une machine mobile du rayon Reptile, du rayon Humain ou du rayon où se trouve le Tambour (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile de ces rayons, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée est tenue : elle ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage (si elle termine le ménage sur la dernière parcelle, son jeton ne glisse pas sous elle). Quand son jeton Machine est révélé, la cale s’agite dans la séquence des Sabotages : allumez l’icône Sabotage, puis balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.",
          "face_2": "Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous n’importe quelle machine mobile (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage. La noyade : quand son jeton Machine est révélé, inclinez-le aussitôt (elle est annulée) ; puis, dans la séquence des Sabotages, la cale allume l’icône Sabotage et balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quelle machine tenir : celle qui approche de la dernière parcelle (bloquer le Ratissage) ou celle qui menace la parcelle du Tambour.",
          "renoncement": "Le jeton pris en cale ne dilue plus le sac : chaque pioche suivante a plus de chances de réveiller une machine."
        }
      },
      "temoins": [
        {
          "id": "G9_T1",
          "resume": "Un Sabotage est révélé ; le Caïman (sur Sabotage) s’active : cale sous l’Abatteuse du rayon H en parcelle 3 ; elle finit le ménage en parcelle 4 mais n’entre pas en Ratissage.",
          "etat_attendu_verifie": {
            "abatteuse_H": {
              "cale": true,
              "ratissage": false
            },
            "sac_sabotages": "-1"
          },
          "statut": "A_CODER"
        },
        {
          "id": "G9_T2",
          "resume": "Tour suivant : le jeton de la machine calée est révélé : l’icône Sabotage s’allume ; en Face 2, la machine est en outre annulée.",
          "etat_attendu_verifie": {
            "icone": "SABOTAGE",
            "annulee_en_face_2": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Sabotage. Caler la machine mobile la plus proche de la dernière parcelle ; garder une Écaille plutôt qu’un Sabotage ordinaire pour la cale seulement si le Croc est déjà sur le plateau.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G10": {
      "id": "G10",
      "alias_oriente": "R>E",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "E",
      "couple": [
        "R",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "MUE_VASE_ECAILLE_CROC_PARCELLE_CIBLEE_ALTERATION_BLEU",
      "entrees_plancher": [
        "ECAILLE",
        "CROC",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "ALTERATION",
        "ROUGE"
      ],
      "entrees": [
        "ECAILLE",
        "CROC",
        "RANG_MACHINE",
        "ALTERATION",
        "ROUGE"
      ],
      "sorties": [
        "ECAILLE",
        "CROC",
        "ALTERATION",
        "BLEU"
      ],
      "paiement": [
        "P_PARI"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE",
        "ICONE_SABOTAGE"
      ],
      "double_ouverture": "Posée sur Piégeage, La Matamata excelle en double mise : dès qu'un premier Piège ou le Croc pare une attaque (le Croc regagnant aussitôt la réserve Reptile avant le balayage), sa 1re activation redéploie immédiatement le Croc sur une seconde parcelle ciblée plus tard dans l'ordre des rangs ; lorsque ce Croc pare à son tour, il rallume Piégeage et déclenche tout seul la 2nde activation de La Matamata.",
      "tags": [
        "CATALYSEUR_EVEIL",
        "ECAILLE",
        "CROC",
        "ALTERATION"
      ],
      "tuile_plateau": {
        "nom_court": "La Matamata",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PIEGEAGE",
        "pictogrammes": [
          "PIC_ECAILLE",
          "PIC_CROC",
          "PIC_ALTERATION",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "+1 🦎 sac + [🦷 ciblé & 🔴→🔵 OU 🌀]",
          "face_2": "+1 🦎/🔴→🔵 + 🦷 ciblé ET 🌀",
          "enracine": "Standard (1 ou 2 Souches finales)"
        },
        "resume_plateau": "Injecte Écaille, embusque Croc, altère"
      },
      "carte_joueur": {
        "titre_complet": "La Matamata, Guetteuse des Feuilles Mortes",
        "entite_illustree": "Tortue matamata entière camouflée au fond d'un igarapé ouvrant sa large gueule",
        "brief_illustration": "Indiscernable d'un amas d'écorces sombres et de feuilles mortes au fond d'un igarapé peu profond, une tortue matamata entière ouvre brusquement sa large gueule triangulaire dans un remous spectral qui fige les rouages d'un engin.",
        "pitch_ambiance": "« On croit marcher sur un lit de feuilles mortes ; déjà le vide s'est ouvert sous l'acier et la vase glacée l'aspire. »",
        "texte_regle": {
          "face_1": "Lorsque La Matamata s'active :\n1. Mue de Vase : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque.\n2. Gueule Aspirante : choisissez 1 seule des deux manœuvres suivantes :\n• Happer la Proie : si le jeton Croc est dans la réserve Reptile, posez-le sur n'importe quelle parcelle ciblée (par une machine qui n'a pas encore frappé à ce tour, mobile ou en Ratissage) ; en outre, si une machine ciblant cette parcelle porte déjà un jeton d'Altération ou possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.\n• Vase Hallucinogène : posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération ; si le jeton Croc se trouve déjà sur le plateau sur une parcelle non ciblée, vous pouvez le déplacer sur une parcelle ciblée de ce rayon.",
          "face_2": "Lorsque La Matamata s'active :\n1. S'il reste au moins 1 jeton Écaille chez les Reptiles, glissez-le dans le sac opaque ; si les 4 Écailles sont déjà sorties, retournez 1 jeton Rouge existant d'une machine du plateau sur sa face Bleue Surchauffe.\n2. Résolvez les deux effets de Gueule Aspirante dans l'ordre de votre choix : déployez (ou repositionnez depuis une parcelle non ciblée) le Croc sur une parcelle ciblée avec son retournement Rouge → Bleu, ET posez 1 jeton d'Altération sur une machine mobile sans Altération (si toutes les machines mobiles sont déjà altérées, retournez 1 jeton Rouge existant → Bleu Surchauffe sur une machine altérée).",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "En Face 1, choisir Happer la Proie pour recycler aussitôt le Croc et allumer Piégeage (en synergie avec R8), ou Vase Hallucinogène pour neutraliser le tour suivant par Altération.",
          "renoncement": "En Face 1, les deux manœuvres s'excluent mutuellement : sécuriser le tour courant via le Croc renonce à l'Altération préventive du tour suivant."
        }
      },
      "temoins": [
        {
          "id": "G10_T1",
          "resume": "Tour 3, La Matamata Face 1 sur Piégeage (2 paris). Au rang 2, le Croc pare une Abatteuse (rentre en réserve, allume Piégeage) : 1re activation → +1 Écaille au sac + Happer la Proie repose le Croc devant le Bulldozer du rang 5 (Rouge → Bleu). Au rang 5, le Croc pare et rallume Piégeage : 2nde activation (Face 2) → +1 Écaille + Vase Hallucinogène altère le Bulldozer.",
          "etat_attendu_verifie": {
            "double_activation_auto": true,
            "ecailles_ajoutees": 2,
            "face_2": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Piégeage avec 2 paris. Dès que le Croc revient en réserve, choisir Happer la Proie pour le reposer sur la prochaine parcelle ciblée afin d'auto-chaîner la 2nde activation.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G11": {
      "id": "G11",
      "alias_oriente": "O>H",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "H",
      "couple": [
        "O",
        "H"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "DE_ENVOL + PLUME + DEFENSEUR_ATTENTE + RANG_MACHINE → DEFENSEUR_REDEPLOYE / ANNULATION",
      "entrees_plancher": [
        "DE_ENVOL",
        "PLUME",
        "DEFENSEUR_ATTENTE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "CHANT",
        "POSITION_REVE"
      ],
      "entrees": [
        "DE_ENVOL",
        "PLUME",
        "DEFENSEUR_ATTENTE",
        "RANG_MACHINE",
        "CHANT",
        "POSITION_REVE"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": "Un premier piqué met un Oiseau au sol pour une Parade. Au second, ce même pion peut saisir une autre menace. Deux saisies demandent deux Oiseaux disponibles.",
      "tags": [
        "PIQUE",
        "SAISIE",
        "DE_ENVOL",
        "MIROIR"
      ],
      "tuile_plateau": {
        "nom_court": "La Harpie féroce",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_PLUME",
          "PIC_RANG_MACHINE",
          "PIC_DEFENSEUR",
          "PIC_CHANT"
        ],
        "mots_cles_plateau": {
          "face_1": "Fondre ou saisir",
          "face_2": "Piqué miroir",
          "enracine": "Ordinaire"
        },
        "resume_plateau": "Oiseau au sol / Oiseau sur jeton Machine · miroir → Chamane au Rêve"
      },
      "carte_joueur": {
        "titre_complet": "La Harpie féroce",
        "entite_illustree": "La Harpie féroce entière plongeant sous la voûte, ailes repliées entre deux troncs",
        "brief_illustration": "La harpie entière plonge sous la voûte, ailes repliées juste assez pour passer entre deux troncs. Son ombre se referme sur un toit de tôle.",
        "pitch_ambiance": "Au cri du guetteur, on regarde le ciel. L’ombre est déjà passée.",
        "texte_regle": {
          "face_1": "Fondre ou saisir (après ouverture des paravents). Prenez un Défenseur Oiseau disponible en forêt, sur une rive, un Rêve, une lisière ou en attente. Pour fondre, posez-le sur la parcelle d’une machine ou un pas radial devant elle, même si elle ne doit pas frapper ce tour. Pour saisir, choisissez une mobile à jouer au rang qu’indique votre Dé d’Envol. Laissez-le visible à l’ouverture, même sur un Sabotage. S’il sert de dé de machine, lisez sa face actuelle. Posez le Défenseur sur son jeton Machine révélé. La machine cesse aussitôt d’être active et perd toute son activation. Son jeton reste droit et visible pour la Furtivité, son dé lisible à son rang. Le pion engagé dans la saisie revient en main au ménage.",
          "face_2": "Piqué miroir. Vous pouvez fondre ou saisir comme en Face 1. Si la Plume indique le rang du Dé d’Envol ou son miroir (1↔4, 2↔5, 3↔6), les deux rangs s’ouvrent à la saisie. Après une saisie sur l’un des deux, vous pouvez porter un Chamane en forêt, depuis une parcelle que cette machine menaçait, sur un Rêve au rang miroir de la prise. Il y défendra le Rêve si sa lecture est encore à venir. Le rang lu est celui du dé au moment du piqué, après tout échange de R5.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Fondre au sol pour participer à plusieurs Parades, ou saisir un jeton Machine pour retirer toute son activation du tour ; en Face 2, monter le Chant sur le Rêve miroir.",
          "renoncement": "L’Oiseau posé sur un jeton Machine ne défendra aucune autre frappe du tour ; monter le Chant peut vider la parcelle menacée par une seconde machine."
        }
      },
      "temoins": [
        {
          "id": "G11_T1",
          "resume": "Dé d’Envol 3 visible, Plume sur 6. R5 échange les rangs 3 et 6 (le Bulldozer H·1 passe au rang 6 ; le Chant est en H·2). L’icône Rêve active G11 Face 2 : un Oiseau saisit le Bulldozer au rang 6 et porte le Chant sur un Rêve encore à lire au rang 3, qui annule l’autre mobile et glisse au rang 2 libre.",
          "etat_attendu_verifie": {
            "bulldozer_saisi": true,
            "chant_porte_rang_3": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Saisir en priorité une mobile coûteuse au rang du Dé d’Envol (ou son miroir en Face 2 avec la Plume) ; à défaut, fondre avec un bâtisseur couché sur une parcelle menacée.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G12": {
      "id": "G12",
      "alias_oriente": "O>E",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "E",
      "couple": [
        "O",
        "E"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Dé écarté sous paravent (et dés ignorés des porteurs de Sabotage) → nouveau rang de machine → annulation par un Rêve (E) qui l’attendait à droite",
      "entrees_plancher": [
        "DES_SOUS_PARAVENT",
        "RANG_MACHINE",
        "POSITION_REVE"
      ],
      "entrees_synergie": [
        "SABOTAGE"
      ],
      "entrees": [
        "DES_SOUS_PARAVENT",
        "RANG_MACHINE",
        "POSITION_REVE",
        "SABOTAGE"
      ],
      "sorties": [
        "RANG_RELU",
        "ANNULATION_INDUITE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": "Chaque Sabotage révélé rallume l’icône de l’Ibijau : deux activations poussent deux machines vers les Rêves de droite avant leur résolution. En Face 2, il puise aussi dans les dés « morts » des porteurs de Sabotage, ce qui lui offre presque toujours un rang utile.",
      "tags": [
        "DES",
        "PARAVENT",
        "REVE",
        "TWIST"
      ],
      "tuile_plateau": {
        "nom_court": "L’Ibijau",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_SABOTAGE",
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_DES_PARAVENT",
          "PIC_RANG_MACHINE",
          "PIC_REVE"
        ],
        "mots_cles_plateau": {
          "face_1": "Machine révélée → rang de son dé écarté",
          "face_2": "Ou dé ignoré d’un porteur de Sabotage · le Rêve qui l’annule glisse d’1 rang",
          "enracine": null
        },
        "resume_plateau": "Relit le dé écarté et pousse la machine vers un Rêve"
      },
      "carte_joueur": {
        "titre_complet": "L’Ibijau, les yeux fendus de la nuit",
        "entite_illustree": "L’Ibijau (Nyctibius griseus) — oiseau nocturne entier, figé à la verticale au bout d’une branche cassée, confondu avec elle",
        "brief_illustration": "Clair de lune : l’Ibijau entier, plumage d’écorce grise, se tient droit au sommet d’un chicot ; ses paupières sont closes mais deux fentes laissent filtrer un regard d’or ; sous lui, les paravents des joueurs laissent deviner des dés ; un Rêve violet flotte à l’horizon. Gris, or, violet.",
        "pitch_ambiance": "Le jour, l’Ibijau n’est qu’un bout de branche morte. Pourtant il voit : deux fentes dans ses paupières closes guettent tout. La nuit, sa plainte descendante raconte, dit-on, l’histoire d’une jeune femme changée en oiseau, qui pleure encore celui qu’elle a perdu.",
        "texte_regle": {
          "face_1": "Quand l’Ibijau s’active : ses paupières closes voient le dé écarté. Choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez le plus haut des deux dés standards du joueur qui a tiré son jeton : la machine quitte son rang et prend celui de ce dé (si les deux dés étaient égaux, rien ne change). Une machine ne peut jamais être déplacée vers un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement.",
          "face_2": "Quand l’Ibijau s’active : choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez l’un de ces dés : le plus haut des deux dés standards du joueur qui a tiré son jeton, ou n’importe lequel des deux dés d’un joueur qui a tiré un Sabotage ou une Écaille (des dés d’ordinaire ignorés). La machine quitte son rang et prend celui du dé lu, jamais un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement ; la complainte de l’urutau guide alors ce Rêve : s’il l’annule, il glisse ensuite d’1 rang vers la gauche si ce rang est libre.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quelle machine relire : celle dont le dé écarté tombe pile sur un Rêve défendu, ou celle qu’il faut chasser d’un rang « Sur place » vers un rang moins nuisible.",
          "renoncement": "Le dé écarté est presque toujours plus haut : la machine relue peut atterrir sur un rang d’Assaut ou d’En avançant et frapper plus fort si aucun Rêve ne l’y attend."
        }
      },
      "temoins": [
        {
          "id": "G12_T1",
          "resume": "Bulldozer révélé au rang 1 (dés 1 et 5) ; Rêve E défendu au rang 5 ; l’Ibijau s’active au premier Sabotage : le Bulldozer passe au rang 5 puis est annulé par le Rêve (icône Rêve).",
          "etat_attendu_verifie": {
            "bulldozer": {
              "rang": 5,
              "annule": true
            },
            "icone": "REVE"
          },
          "statut": "A_CODER"
        },
        {
          "id": "G12_T2",
          "resume": "Dés égaux (3 et 3) : la machine reste au rang 3 ; en Face 2, l’Ibijau peut à la place lire le 6 d’un porteur de Sabotage.",
          "etat_attendu_verifie": {
            "face_1_rang": 3,
            "face_2_rang_possible": 6
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Sabotage. Relire la machine dont le dé écarté correspond à un Rêve défendu non résolu ; à défaut, ne pas relire vers un rang d’Assaut En avançant.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G13": {
      "id": "G13",
      "alias_oriente": "M>I",
      "famille": "GARDIEN",
      "origine": "M",
      "voisin": "I",
      "couple": [
        "M",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Nid à ≥ 2 Insectes éventré (-1 → +2) ou termitière sauvage (+1 de la réserve) ; Face 2 : riposte projetée sur parcelle adjacente + garde dressée du Duel",
      "entrees_plancher": [
        "INSECTE",
        "DUEL"
      ],
      "entrees_synergie": [
        "NID"
      ],
      "entrees": [
        "INSECTE",
        "DUEL",
        "NID"
      ],
      "sorties": [
        "RIPOSTE_ESSAIM",
        "INSECTE",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": "Deux éventrements, deux ripostes : soit deux Nids différents gonflent à la veille des frappes, soit le même Nid riposte deux fois. En Face 2, chaque riposte jaillit sur la parcelle menacée et fait allumer Insecte à la parade, l’icône du Tamanoir. Sans Nid à éventrer, la seconde termitière sauvage peut porter un Nid tout juste construit jusqu’à ses 2 Insectes.",
      "tags": [
        "INSECTES",
        "ESSAIM",
        "PRODUCTION",
        "DUEL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Tamanoir",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_INSECTE",
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "Nid à 2 Insectes ou plus · 1 Insecte mangé → riposte de 2 · sans Nid à éventrer : 1 Insecte de la réserve",
          "face_2": "Riposte posée sur parcelle ciblée adjacente · parade aidée = Territoire tenu · sans Nid : idem",
          "enracine": null
        },
        "resume_plateau": "Mange un peu, fait riposter beaucoup"
      },
      "carte_joueur": {
        "titre_complet": "Le Tamanoir, le grand mangeur qui épargne",
        "entite_illustree": "Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier éventrant une termitière",
        "brief_illustration": "Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier, longue tête tubulaire et queue en panache, éventrant une termitière de sa griffe ; des soldats jaillissent déjà des galeries.",
        "pitch_ambiance": "Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.",
        "texte_regle": {
          "face_1": "La récolte. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1 (le Tamanoir ne vide jamais un Nid). L’Essaim riposte aussitôt : ce Nid produit 2 Insectes, sans allumer d’icône ni appliquer son pouvoir de Nid. Ces Insectes restent sur le Nid et participent normalement aux parades sur sa parcelle.\nTermitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, le Tamanoir fouille une termitière sauvage : prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée, où il participe aux parades.",
          "face_2": "La garde dressée. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1. L’Essaim riposte : ce Nid produit 2 Insectes, sans allumer d’icône, que vous pouvez faire jaillir : posez-les sur la parcelle du Nid ou sur une parcelle ciblée adjacente (même rayon, ou même numéro d’un rayon voisin), où ils participeront aux parades. La garde dressée : si le jeton Duel se trouve sur l’une de ces parcelles, une parade aidée par ces Insectes y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère.\nTermitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée ; la garde dressée s’y applique.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quel Nid éventrer — celui qui riposte le plus près de la frappe à venir, ou celui qu’il faut regonfler avant la Production.",
          "renoncement": "L’Insecte mangé manque à une déviation ou à un Bouclier de lisière ; un Nid réduit à 1 Insecte ne peut plus être éventré."
        }
      },
      "temoins": [
        {
          "id": "G13_T1",
          "resume": "Nid à 3 Insectes ; le Tamanoir s’active : 3 − 1 + 2 = 4 Insectes sur le Nid.",
          "etat_attendu_verifie": {
            "insectes_nid": 4
          },
          "statut": "A_CODER"
        },
        {
          "id": "G13_T2",
          "resume": "Plancher (Tour 2, aucun Nid construit) : la parcelle 2 du rayon M est visée au rang 4 (Assaut, Seuil 2) et gardée par 1 Défenseur. Après une parade au rang 1, le Tamanoir (sur Parade, icône de repli) fouille une termitière sauvage et pose 1 Insecte de la réserve sur cette parcelle ; au rang 4, parade réussie avec cet Insecte (icône Insecte).",
          "etat_attendu_verifie": {
            "insecte_reserve_pose": 1,
            "icone_insecte_allumee": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Insecte (ou Parade en repli sans Nid). Éventrer le Nid le plus proche d’une parcelle visée ; en Face 2, faire jaillir la riposte sur la parcelle visée dont le déficit au Seuil est au plus 2.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G14": {
      "id": "G14",
      "alias_oriente": "R>I",
      "famille": "GARDIEN",
      "origine": "R",
      "voisin": "I",
      "couple": [
        "R",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL"
      ],
      "est_twist": false,
      "vecteurs": "Écaille couvée sous un Nid (ou ponte au sol rayon R/I) → éclosion du Croc sur frappe → Piégeage + Écaille au sac ; Face 2 : nichée tenant jusqu’au ménage",
      "entrees_plancher": [
        "ECAILLE",
        "CROC"
      ],
      "entrees_synergie": [
        "NID"
      ],
      "entrees": [
        "ECAILLE",
        "CROC",
        "NID"
      ],
      "sorties": [
        "PONTE",
        "CROC",
        "ECAILLE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": "Chaque activation installe une ponte sous un Nid différent : deux Nids protégés, deux éclosions possibles, deux icônes Piégeage. En Face 2, une seule ponte suffit à tenir une parcelle pendant toute la phase d’attaques. Sans Nid, la seconde activation déplace la ponte au sol vers la parcelle la plus menacée.",
      "tags": [
        "INSECTES",
        "PONTE",
        "CROC",
        "ECAILLE",
        "ESSAIM"
      ],
      "tuile_plateau": {
        "nom_court": "Le Téju",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_INSECTE",
        "pictogrammes": [
          "PIC_ECAILLE",
          "PIC_NID",
          "PIC_CROC",
          "PIC_PIEGE"
        ],
        "mots_cles_plateau": {
          "face_1": "Écaille sous un Nid (sans Nid libre : au sol, rayon R ou I) · frappe → le Croc éclot et pare",
          "face_2": "Le Croc éclot d’où qu’il soit et pare chaque frappe jusqu’au ménage",
          "enracine": null
        },
        "resume_plateau": "Pond une Écaille au cœur d’un Nid"
      },
      "carte_joueur": {
        "titre_complet": "Le Téju, la ponte au cœur de la termitière",
        "entite_illustree": "Le Téju (Tupinambis teguixin), grand lézard entier noir et doré griffant une termitière",
        "brief_illustration": "Le Téju (Tupinambis teguixin), grand lézard entier à la robe noire et dorée, griffant la paroi d’une termitière pour y pondre ; à ses pieds, la litière de feuilles où s’enfouissent les pontes sans abri.",
        "pitch_ambiance": "La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.",
        "texte_regle": {
          "face_1": "La ponte. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. Éclosion : quand une machine frappe la parcelle de ce Nid et que le Croc est dans la réserve Reptile, la ponte éclot avant toute parade : postez le Croc sur cette parcelle ; il pare cette frappe en premier (allumez Piégeage) puis regagne la réserve, et l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.\nPonte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, le Téju pond dans la litière : posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte. Elle éclot de la même façon quand une machine frappe cette parcelle, et regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois : pondre de nouveau au sol la déplace.",
          "face_2": "La nichée. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. La nichée : quand une machine frappe la parcelle de ce Nid, la ponte éclot avant toute parade : postez le Croc sur cette parcelle, où qu’il se trouve (réserve Reptile ou autre parcelle) ; il pare cette frappe en premier (allumez Piégeage) et, au lieu de regagner la réserve, reste sur place pour parer de même chaque frappe suivante sur cette parcelle jusqu’au ménage, où il regagne la réserve tandis que l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.\nPonte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte : la nichée y éclot de la même façon, et l’Écaille regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois.",
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Sous quel Nid pondre — celui dont la parcelle est visée ce tour, ou un Nid exposé à long terme près du cœur ; sans Nid, quelle parcelle couver.",
          "renoncement": "L’Écaille couvée n’est plus dans le sac tant qu’elle n’a pas éclos (moins de Sabotages tirés) ; un Croc parti éclore ne protège plus la parcelle où une Écaille l’avait posté."
        }
      },
      "temoins": [
        {
          "id": "G14_T1",
          "resume": "Ponte sous le Nid de la parcelle 2 du rayon I ; le Bulldozer frappe cette parcelle ; le Croc est en réserve : éclosion, parade du Croc (Piégeage), Écaille au sac.",
          "etat_attendu_verifie": {
            "croc_pare": true,
            "ecaille_au_sac": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "G14_T2",
          "resume": "Plancher (Tour 2, aucun Nid construit) : après une parade au rang 1, le Téju (sur Parade, icône de repli) pond au sol 1 Écaille face cachée au bord de la parcelle 2 du rayon R. Au rang 4, l’Abatteuse frappe cette parcelle : éclosion du Croc (Piégeage) puis retour en réserve et Écaille au sac.",
          "etat_attendu_verifie": {
            "ponte_au_sol_eclot": true,
            "ecaille_au_sac": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Insecte (ou Parade en repli sans Nid). Pondre sous le Nid dont la parcelle est visée par une machine révélée ; sinon sous le Nid le plus proche du cœur, ou en ponte au sol sur une parcelle menacée de R ou I.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "G15": {
      "id": "G15",
      "alias_oriente": "O>I",
      "famille": "GARDIEN",
      "origine": "O",
      "voisin": "I",
      "couple": [
        "O",
        "I"
      ],
      "cycle": "DOUBLE_FACE_UPGRADE",
      "cablage": [
        1,
        2,
        3,
        4,
        5,
        6
      ],
      "roles_portes": [
        "CATALYSEUR_EVEIL",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "Insecte transporté à vol d’oiseau (amorçage réserve en solo) → parade Insecte ; Face 2 : pollinisation de Nid (+1 Insecte) et dépôt Réglette via Plume ; Enraciné final",
      "entrees_plancher": [
        "PLUME"
      ],
      "entrees_synergie": [
        "INSECTE",
        "NID"
      ],
      "entrees": [
        "PLUME",
        "INSECTE",
        "NID"
      ],
      "sorties": [
        "INSECTE_TRANSPORTE",
        "INSECTE",
        "INSECTE_RANG",
        "ARBRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": "Une goutte par activation : la première complète la parade d’une frappe imminente, la seconde ravitaille une autre parcelle ou, en Face 2, pollinise un Nid qui produira +2 à sa prochaine Production. Chaque parade aidée allume Insecte et relance la Piste.",
      "tags": [
        "INSECTES",
        "ESSAIM",
        "TRANSPORT",
        "POLLINISATION",
        "ENRACINEMENT"
      ],
      "tuile_plateau": {
        "nom_court": "Le Colibri",
        "fenetre_badge": "ACTIVATION",
        "icone_conseillee": "ICONE_PARADE",
        "pictogrammes": [
          "PIC_INSECTE",
          "PIC_MIGRATION",
          "PIC_NID",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Insecte pris n’importe où → n’importe quelle parcelle · aucun Insecte en jeu = 1 de la réserve",
          "face_2": "2 Insectes · arrivée sur un Nid = +1 Insecte · Plume près d’un rang = dépôt sur la Réglette",
          "enracine": "Fin de partie : tuiles enracinées voisines, 1 repousse de plus"
        },
        "resume_plateau": "Transporte l’Essaim à vol d’oiseau"
      },
      "carte_joueur": {
        "titre_complet": "Le Colibri, porteur de gouttes et de pollen",
        "entite_illustree": "Le Colibri (Phaethornis), minuscule oiseau entier en vol stationnaire devant une fleur d’héliconia",
        "brief_illustration": "Le Colibri (Phaethornis, ermite des sous-bois), animal entier : minuscule oiseau en vol stationnaire devant une fleur d’héliconia ; dans la lumière rasante, on devine les acariens des fleurs qui voyagent dans ses narines, de corolle en corolle.",
        "pitch_ambiance": "Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.",
        "texte_regle": {
          "face_1": "Le porteur de gouttes. Quand le Colibri s’active, il emporte un passager : déplacez 1 Insecte depuis n’importe quel Nid, parcelle, rang de la Réglette ou icône de la Piste des Gardiens vers n’importe quelle parcelle de n’importe quel rayon. Il y participe normalement aux parades (une parade aidée par un Insecte allume l’icône Insecte).\nAmorçage — narines fleuries (plancher) : s’il n’y a encore aucun Insecte en jeu, le Colibri en rapporte un des fleurs : prenez-le dans la réserve de l’Essaim.",
          "face_2": "La tournée. Quand le Colibri s’active, il fait sa tournée : déplacez jusqu’à 2 Insectes, pris n’importe où (Nid, parcelle, rang de la Réglette, icône de la Piste des Gardiens), vers une ou deux parcelles de n’importe quels rayons, où ils participent aux parades. S’il n’y a encore aucun Insecte en jeu, le premier vient de la réserve de l’Essaim.\nPollinisation : si l’un d’eux arrive sur un Nid, ce Nid produit aussitôt 1 Insecte, sans allumer d’icône ni appliquer son pouvoir de Nid.\nFleur signalée : si la Plume de Vigie est posée près d’un rang de la Réglette, vous pouvez déposer l’un de ces passagers sur ce rang plutôt que sur une parcelle : il y servira à une déviation, une lanterne ou un rite.",
          "enracine": "La part du colibri. Au décompte final, chaque autre tuile enracinée au pied de son rayon ou d’un rayon voisin fait repousser 1 Souche de plus."
        },
        "decision_et_renoncement": {
          "choix": "Quel Insecte déplacer, et d’où — vider un rang, un Nid ou une icône pour compléter une parade imminente ; en Face 2, faire escale sur un Nid pour le polliniser, ou déposer un passager là où siffle la Plume.",
          "renoncement": "Chaque Insecte emporté laisse un trou ailleurs (une déviation, une Production plus faible, un Bouclier de lisière en moins) ; un passager posé sur la Réglette ne pare rien ce tour-ci."
        }
      },
      "temoins": [
        {
          "id": "G15_T1",
          "resume": "Amorçage (Tour 2, aucun Nid construit, aucun Insecte en jeu) : la parcelle 3 du rayon M est visée au rang 4 (Seuil 3) et gardée par 2 Défenseurs. Après une parade au rang 1, le Colibri (sur Parade) apporte 1 Insecte de la réserve sur cette parcelle ; au rang 4, parade réussie avec cet Insecte défaussé (icône Insecte).",
          "etat_attendu_verifie": {
            "insecte_reserve_transporte": 1,
            "icone_insecte_allumee": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "G15_T2",
          "resume": "Pollinisation (Face 2) : un Nid porte 1 Insecte en parcelle 2 du rayon I et 1 Insecte attend sur le rang 4. Le Colibri porte ce dernier sur le Nid (2 Insectes → pollinisation +1 = 3 Insectes), puis porte un second passager depuis l’icône Insecte vers la parcelle 3 du rayon O visée au rang 5.",
          "etat_attendu_verifie": {
            "insectes_nid_apres_pollinisation": 3
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Siéger sur Parade. Transporter l’Insecte (ou amorcer depuis la réserve) vers la parcelle visée non résolue dont le déficit au Seuil est exactement 1 ; en Face 2, polliniser un Nid à 1 Insecte ou alimenter la Réglette via la Plume ; enraciner en fin de partie si deux tuiles voisines sont déjà enracinées.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R1": {
      "id": "R1",
      "alias_oriente": "H>E",
      "famille": "REVE",
      "origine": "H",
      "voisin": "E",
      "couple": [
        "H",
        "E"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "LEVIER_REVE",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "Rêve Humain défendu → Rêve des Entités tiré contre lui → bloc contigu vers le Sommeil ; plancher solo : grimpe d’1 rang ou serre +1 machine ; Enracinement sans fermer le Sommeil",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "sorties": [
        "REVE_COMPACTE",
        "POSITION_REVE",
        "ANNULATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "SOMMEIL",
        "LEVIER",
        "ENRACINEMENT"
      ],
      "tuile_plateau": {
        "nom_court": "La Liane des Esprits",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_AVANCEE_REVE",
          "PIC_ANNULATION",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "Rêve des Entités tiré contre la Liane · collé = la paire glisse à gauche · aucun à droite = la Liane grimpe d’1 rang, sinon serre 1 machine de plus",
          "face_2": null,
          "enracine": "Enracinée sans fermer le Sommeil"
        },
        "resume_plateau": "Tire un Rêve des Entités contre elle"
      },
      "carte_joueur": {
        "titre_complet": "La Liane des Esprits",
        "entite_illustree": "Vision chamanique de l’ayahuasca : une liane torsadée reliant le monde des hommes à celui des esprits",
        "brief_illustration": "Vision chamanique de l’ayahuasca : une liane torsadée qui relie le monde des hommes à celui des esprits ; ses vrilles s’enroulent autour d’un rêve lumineux et l’attirent vers le chamane.",
        "pitch_ambiance": "On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.",
        "texte_regle": {
          "face_1": "Quand ce Rêve est défendu, à sa résolution, après ses annulations : la liane s’enroule. Choisissez un Rêve des Entités situé plus à droite sur la Réglette. S’il reste au moins un rang libre entre eux, faites glisser ce Rêve jusqu’au rang libre qui touche la Liane (ses Défenseurs le suivent). S’il touche déjà la Liane, elle l’entraîne : la Liane glisse d’1 rang vers la gauche si ce rang est libre, et ce Rêve glisse d’1 rang à sa suite. Un Rêve déplacé qui n’a pas encore été résolu se résout ensuite depuis sa nouvelle place.\nLa liane grimpe (plancher) : s’il n’y a aucun Rêve des Entités à sa droite, la Liane s’enroule sur elle-même : elle glisse d’1 rang vers la gauche si ce rang est libre (ses Défenseurs la suivent ; elle ne se résout pas une seconde fois). Si elle ne peut pas glisser (rang occupé, ou Liane déjà au rang 1), elle serre : elle annule 1 machine de plus sur son rang.",
          "face_2": null,
          "enracine": "La Liane nourrit encore les rêves : contrairement aux autres Rêves enracinés, elle ne rend pas le Sommeil impossible. Au décompte final, elle fait repousser 1 Souche comme toute tuile enracinée."
        },
        "decision_et_renoncement": {
          "choix": "Tirer le Rêve des Entités pour combler un trou du bloc, ou faire glisser la paire vers le rang 1 ; seule, grimper vers le bloc ou serrer une machine de plus.",
          "renoncement": "Le Rêve tiré abandonne le rang qu’il couvrait ; une Liane qui grimpe quitte un rang où des machines pourraient encore tomber ; enraciner la Liane lui retire ce pouvoir mais garde le Sommeil possible."
        }
      },
      "temoins": [
        {
          "id": "R1_T1",
          "resume": "L’enroulement : Liane au rang 3 défendue, Rêve des Entités au rang 6, rangs 4 et 5 libres : le Rêve des Entités glisse au rang 4.",
          "etat_attendu_verifie": {
            "reve_e_rang": 4
          },
          "statut": "A_CODER"
        },
        {
          "id": "R1_T2",
          "resume": "Plancher (Tour 2, aucun Rêve des Entités construit) : la Liane, au rang 6 avec 1 Défenseur, annule la machine de son rang puis grimpe au rang 5 ; plus tard, collée au rang 2 contre un Rêve Humain au rang 1 avec 2 machines et 1 Défenseur, elle en annule une puis serre la seconde.",
          "etat_attendu_verifie": {
            "liane_grimpe_ou_serre": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Tirer le Rêve E le plus à droite ; s’il est collé et que le rang de gauche est libre, faire glisser la paire ; seule, grimper vers le rang 1 ou serrer une 2e machine sur son rang. Enraciner la Liane en fin de partie sans craindre de fermer le Sommeil.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R2": {
      "id": "R2",
      "alias_oriente": "E>H",
      "famille": "REVE",
      "origine": "E",
      "voisin": "H",
      "couple": [
        "E",
        "H"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "ENRACINEMENT"
      ],
      "est_twist": false,
      "vecteurs": "POSITION_REVE + RANG_MACHINE (+ TAMBOUR / SOUCHE / DEFENSEUR_ATTENTE) → ALTERATION / DEFENSEUR_REDEPLOYE / ARBRE",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "TAMBOUR",
        "SOUCHE",
        "DEFENSEUR_ATTENTE"
      ],
      "entrees": [
        "POSITION_REVE",
        "RANG_MACHINE",
        "TAMBOUR",
        "SOUCHE",
        "DEFENSEUR_ATTENTE"
      ],
      "sorties": [
        "ALTERATION",
        "DEFENSEUR_REDEPLOYE",
        "ARBRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "ALTERATION",
        "ENRACINEMENT",
        "GUE_MARQUE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Fleuve sous la cendre",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_SOUCHE",
          "PIC_ALTERATION",
          "PIC_TAMBOUR",
          "PIC_ENRACINEMENT"
        ],
        "mots_cles_plateau": {
          "face_1": "Lit sec · Marque",
          "face_2": null,
          "enracine": "Gué marqué · Final"
        },
        "resume_plateau": "Tambour / Souches → Altération · ancrage marqué → Souche finale supplémentaire"
      },
      "carte_joueur": {
        "titre_complet": "Le Fleuve sous la cendre",
        "entite_illustree": "Filet d’eau lumineuse rejoignant une souche sous un banc de cendre dans un méandre asséché",
        "brief_illustration": "Un filet d’eau lumineuse rejoint une souche sous un banc de cendre, dans un méandre asséché.",
        "pitch_ambiance": "Sous la cendre, l’eau se souvient du lit qu’elle occupait. Le premier arbre à boire lui rend son chemin.",
        "texte_regle": {
          "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez poser une Altération de la réserve sur une mobile sans Altération dans le rayon du Tambour en forêt, ou sur une mobile d’un rayon dont une parcelle ne porte que des Souches (à défaut, sur une mobile sans Altération de E ou H). Vous pouvez à la place relever le Tambour en attente sur un Rêve non défendu à droite de celui-ci. Il y participera à la résolution ordinaire.",
          "face_2": null,
          "enracine": "Gué marqué. À l’enracinement, si une machine mobile porte une Altération sur la parcelle désignée, vous pouvez tourner la Grande Carte d’un quart de tour, côté « Gué marqué » vers le haut. Ce repère conserve le droit au bonus, même après le départ de la machine. Le Sommeil se ferme dès l’ancrage. Au décompte final seulement, si la parcelle a survécu, retournez-y une Souche au titre de l’ancrage ordinaire, puis une autre si le gué est marqué. Chaque retournement exige une Souche encore présente."
        },
        "decision_et_renoncement": {
          "choix": "Altérer une mobile grâce au Tambour ou aux Souches (ou sur E/H à défaut), relever le Tambour en attente sur un Rêve plus à droite, ou enraciner le Fleuve sur une parcelle altérée pour marquer le gué.",
          "renoncement": "Enraciner le Fleuve sur le gué abandonne ses deux usages actifs et ferme définitivement la voie du Sommeil."
        }
      },
      "temoins": [
        {
          "id": "R2_T1",
          "resume": "À l’ouverture, le Tambour est en E·1 ; R2 défendu altère une mobile en E·3. Au ménage du Tour 5, elle s’y trouve encore avec son Altération et deux Souches. E enracine R2 devant E·3 et tourne sa Grande Carte (les Souches restent face Souche pendant la bataille). Au décompte final, si les deux Souches survivent, les deux deviennent Arbres en E·3.",
          "etat_attendu_verifie": {
            "gue_marque": true,
            "souches_retournees_fin": 2
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Altérer une mobile avancée via le Tambour, une clairière de Souches ou le repli E/H ; relever le Tambour en attente sur un Rêve menacé à droite si disponible ; enraciner sur une parcelle altérée à ≥ 2 Souches lorsque le Sommeil est hors de portée.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R3": {
      "id": "R3",
      "alias_oriente": "H>M",
      "famille": "REVE",
      "origine": "H",
      "voisin": "M",
      "couple": [
        "H",
        "M"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Défenseur d’un Rêve (H) → bond vers la parcelle du Duel (M) ou du rayon annulé → double emploi annulation + parade ; dépose un Chamane en forêt pour le Tapir",
      "entrees_plancher": [
        "RANG_REVE",
        "DUEL"
      ],
      "entrees_synergie": [
        "ANNULATION"
      ],
      "entrees": [
        "RANG_REVE",
        "DUEL",
        "ANNULATION"
      ],
      "sorties": [
        "CHAMANE_EN_FORET",
        "DEFENSEUR_REDEPLOYE",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_PARADE"
      ],
      "double_ouverture": null,
      "tags": [
        "BOND",
        "DUEL",
        "DOUBLE_EMPLOI"
      ],
      "tuile_plateau": {
        "nom_court": "Le Chamane-Jaguar",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_DEFENSEUR",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "Après annulation · ses Défenseurs bondissent vers le Duel ou une parcelle visée",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Annule puis bondit défendre la forêt"
      },
      "carte_joueur": {
        "titre_complet": "La Vision du Chamane-Jaguar",
        "entite_illustree": "Vision chamanique de la métamorphose — un chamane dont l’ombre devient celle d’un jaguar en plein bond",
        "brief_illustration": "Nuit de cérémonie : un chamane danse autour d’un feu, coiffe de plumes, corps peint ; son ombre projetée sur la canopée est celle d’un jaguar bondissant, qui atterrit sur une parcelle menacée à côté du jeton Duel. Rouges braise, noirs, taches dorées.",
        "pitch_ambiance": "Chez les peuples du Haut Rio Negro, un même mot désigne le chamane et le jaguar. Quand la vision le prend, le chamane quitte le rêve sur quatre pattes et bondit là où la forêt saigne.",
        "texte_regle": {
          "face_1": "Quand ce Rêve est défendu, à sa résolution : une fois ses annulations faites, chaque Défenseur posé sur ce Rêve peut bondir hors de lui, sur sa face Définitif, vers la parcelle qui porte le jeton Duel, ou vers une parcelle ciblée du rayon d’une machine que ce Rêve vient d’annuler. Il y compte pour toutes les parades à venir. Sur la parcelle du Duel, un Défenseur Humain arrivé ainsi compte comme un Défenseur Mammifère pour retourner le Duel sur Territoire tenu.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Où bondir : sur le Duel pour sceller un Territoire tenu, ou sur la parcelle visée du rayon dont une machine vient d’être annulée.",
          "renoncement": "Engager un Défenseur sur ce Rêve, c’est parier qu’une machine tombera sur son rang : s’il n’annule rien, il ne peut bondir que vers le Duel."
        }
      },
      "temoins": [
        {
          "id": "R3_T1",
          "resume": "Rêve H au rang 2 défendu par le Chant ; il annule l’Abatteuse du rayon M ; le Chant bondit sur la parcelle 3 du rayon M (Duel face Défi, 1 Défenseur M) ; la frappe du Bulldozer y est parée (Seuil 2) ; le Duel passe sur Territoire tenu.",
          "etat_attendu_verifie": {
            "duel": "TERRITOIRE_TENU",
            "parade": true,
            "chant_parcelle": "M_p3"
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Défendre ce Rêve quand le Duel est posé sur une parcelle à Seuil 2 ou plus ; bondir vers la parcelle visée dont le déficit est exactement 1.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R4": {
      "id": "R4",
      "alias_oriente": "H>R",
      "famille": "REVE",
      "origine": "H",
      "voisin": "R",
      "couple": [
        "H",
        "R"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "TWIST_2K3",
        "LEVIER_REVE"
      ],
      "est_twist": true,
      "vecteurs": "Rêve-piston : la Pirogue recule pour faire remonter un Rêve, ou pousse tout le convoi depuis la queue ; mue → Écailles (R) dans le sac, qui serviront de cales au Caïman",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "POSITION_REVE",
        "RANG_REVE"
      ],
      "sorties": [
        "PISTON_REVES",
        "POSITION_REVE",
        "ECAILLE"
      ],
      "paiement": [
        "P_RANG"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "TWIST",
        "SOMMEIL",
        "PISTON",
        "ECAILLE"
      ],
      "tuile_plateau": {
        "nom_court": "La Pirogue-Anaconda",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_AVANCEE_REVE",
          "PIC_REVE",
          "PIC_ECAILLE"
        ],
        "mots_cles_plateau": {
          "face_1": "En queue · tout le convoi glisse d’1 ‖ Retour · échange avec le Rêve de droite ‖ mue = 1 Écaille au sac",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Piston de Rêves qui pousse le convoi"
      },
      "carte_joueur": {
        "titre_complet": "La Pirogue-Anaconda des Ancêtres",
        "entite_illustree": "Vision mythique de la pirogue-serpent — l’anaconda géant dont le ventre porta les ancêtres en remontant le fleuve",
        "brief_illustration": "Fleuve cosmique au crépuscule : une immense pirogue dont la coque est le corps d’un anaconda, tête dressée à la proue, remonte le courant ; à son bord, d’autres Rêves lumineux comme des passagers ; dans son sillage, des écailles scintillantes tombent à l’eau. Bleus nuit, verts olive, éclats d’argent.",
        "pitch_ambiance": "Au commencement, racontent les peuples du Rio Negro, les ancêtres remontèrent le fleuve dans le ventre d’un anaconda-pirogue, de halte en halte, jusqu’à devenir des hommes. La pirogue pousse encore les rêves vers l’amont.",
        "texte_regle": {
          "face_1": "Quand ce Rêve est défendu, à sa résolution (après ses annulations), choisissez une manœuvre. Poussée : si la Pirogue est le Rêve le plus à droite de la Réglette, elle pousse tout le convoi : chaque Rêve, du plus à gauche au plus à droite (la Pirogue en dernier), glisse d’1 rang vers la gauche si ce rang est libre. Retour : la Pirogue échange sa place avec le premier Rêve situé à sa droite, même séparé d’elle par des rangs libres ; chacun garde ses Défenseurs, et ce Rêve, s’il n’a pas encore été résolu, se résout aussitôt depuis sa nouvelle place. Mue de l’anaconda : après chaque manœuvre, le joueur Reptile peut glisser 1 Écaille de sa réserve dans le sac.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Pousser le convoi entier (si la Pirogue est en queue) ou reculer en échangeant avec le Rêve de droite pour le faire remonter d’un coup.",
          "renoncement": "Le Retour éloigne la Pirogue vers les rangs rares et la détache du bloc du Sommeil ; tant qu’elle n’est pas en queue, elle ne peut pas pousser."
        }
      },
      "temoins": [
        {
          "id": "R4_T1",
          "resume": "Rêves aux rangs 3 et 4, Pirogue au rang 6 (rangs 1, 2 et 5 libres) : Poussée : Rêves aux rangs 2, 3 et Pirogue au rang 5 ; mue : 1 Écaille au sac.",
          "etat_attendu_verifie": {
            "reves_rangs": [
              2,
              3,
              5
            ],
            "sac_ecailles": "+1"
          },
          "statut": "A_CODER"
        },
        {
          "id": "R4_T2",
          "resume": "Pirogue au rang 2, Rêve E au rang 5 non résolu : Retour : le Rêve E passe au rang 2 et se résout aussitôt, la Pirogue passe au rang 5.",
          "etat_attendu_verifie": {
            "pirogue_rang": 5,
            "reve_E_rang": 2
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Si la Pirogue est en queue, Poussée ; sinon Retour quand le Rêve de droite est défendu et qu’une machine révélée occupe le rang de la Pirogue.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R5": {
      "id": "R5",
      "alias_oriente": "H>O",
      "famille": "REVE",
      "origine": "H",
      "voisin": "O",
      "couple": [
        "H",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "PLUME + PERCHOIR + RANG_MACHINE → RANG_MACHINE",
      "entrees_plancher": [
        "PLUME",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "PERCHOIR"
      ],
      "entrees": [
        "PLUME",
        "RANG_MACHINE",
        "PERCHOIR"
      ],
      "sorties": [
        "RANG_MACHINE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [
        "MIROIR",
        "TACTIQUE"
      ],
      "tuile_plateau": {
        "nom_court": "Le Ciel à deux eaux",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_PLUME",
          "PIC_RANG_MACHINE",
          "PIC_PERCHOIR"
        ],
        "mots_cles_plateau": {
          "face_1": "Rangs miroirs · échange",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Rangs miroirs · échange"
      },
      "carte_joueur": {
        "titre_complet": "Le Ciel à deux eaux",
        "entite_illustree": "Vision d’un ciel reflété dans le fleuve",
        "brief_illustration": "Un bras de fleuve reflète deux horizons décalés sous une même ligne de pluie.",
        "pitch_ambiance": "Les deux rives montrent le même ciel. Une seule voit l’orage arriver.",
        "texte_regle": {
          "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez échanger les rangs de deux machines visibles encore actives, distants exactement de trois. La Plume doit indiquer l’un de ces rangs. Si le Perchoir porte un jeton face cachée, une Plume au pied du rayon d’une des deux machines convient aussi. Laissez le jeton caché sur son Perchoir. Placez leurs dés de machine aux rangs échangés, sans déplacer leurs jetons de rayon. Chacune garde sa tactique imprimée mais change de mode. Les Rêves encore à résoudre lisent les nouveaux rangs.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Quelle machine doit passer en Charge et laquelle attaquera plus tôt ?",
          "renoncement": "Le changement de mode vaut pour les deux. Il peut renforcer la machine qu’on laisse en Assaut."
        }
      },
      "temoins": [
        {
          "id": "R5_T1",
          "resume": "Acte I, Plume en 1, une Abatteuse en 1 échange avec un Bulldozer chargé de Rouges en 4. Le Bulldozer passe en Charge sur place. L’Abatteuse passe en Assaut en 4 devant un Rêve encore à résoudre.",
          "etat_attendu_verifie": {
            "entree": {
              "plume": 1,
              "A": 1,
              "B": 4,
              "reve_a_venir": 4
            },
            "transition_python": "if abs(s['A']-s['B'])==3 and s['plume'] in (s['A'],s['B']):\n    s['A'],s['B']=s['B'],s['A']\nr=[s['A'],s['B'],'Charge' if s['B']<=3 else 'Assaut',s['A']==s['reve_a_venir']]",
            "attendu": [
              4,
              1,
              "Charge",
              true
            ]
          },
          "statut": "OK"
        }
      ],
      "heuristique_bot": "Échanger si la perte de force ou l’annulation de la machine la plus dangereuse dépasse le risque créé au rang opposé.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R6": {
      "id": "R6",
      "alias_oriente": "H>I",
      "famille": "REVE",
      "origine": "H",
      "voisin": "I",
      "couple": [
        "H",
        "I"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0"
      ],
      "est_twist": false,
      "vecteurs": "Insecte du rayon Humain cueilli sur son rang (ou amorçage réserve en solo) → chaque Insecte défaussé annule +1 machine du rang",
      "entrees_plancher": [
        "INSECTE",
        "ANNULATION"
      ],
      "entrees_synergie": [
        "INSECTE_RANG"
      ],
      "entrees": [
        "INSECTE",
        "ANNULATION",
        "INSECTE_RANG"
      ],
      "sorties": [
        "ANNULATION_RENFORCEE",
        "INSECTE_RANG"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES",
        "ESSAIM",
        "ANNULATION"
      ],
      "tuile_plateau": {
        "nom_court": "La Tucandeira",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_REVE",
          "PIC_INSECTE",
          "PIC_ANNULATION"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Insecte du rayon Humain → son rang (aucun en jeu : de la réserve) · chaque Insecte défaussé = 1 annulation de plus",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "L’Essaim multiplie les annulations du Rêve"
      },
      "carte_joueur": {
        "titre_complet": "Le Rite de la Tucandeira",
        "entite_illustree": "Gants tressés de fourmis tucandeiras portés lors d’une danse rituelle",
        "brief_illustration": "Vision rituelle : les gants tressés de fourmis tucandeiras du rite de passage, portés par un jeune initié qui danse ; à ses pieds, les fourmis fraîchement cueillies en forêt.",
        "pitch_ambiance": "Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.",
        "texte_regle": {
          "face_1": "Quand ce Rêve est défendu, à sa résolution : la cueillette : vous pouvez d’abord déplacer 1 Insecte d’une parcelle du rayon Humain vers le rang de ce Rêve.\nAmorçage — cueillette sauvage (plancher) : s’il n’y a encore aucun Insecte en jeu, prenez-le dans la réserve de l’Essaim.\nPuis le gant de tucandeiras : en plus d’1 machine par Défenseur, ce Rêve annule 1 machine supplémentaire de son rang pour chaque Insecte que vous défaussez de ce rang.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Combien d’Insectes offrir au gant — un par machine qui resterait sinon active sur le rang.",
          "renoncement": "Les Insectes consumés au rite ne dévieront plus de dés et ne pareront plus de frappes."
        }
      },
      "temoins": [
        {
          "id": "R6_T1",
          "resume": "Rêve au rang 1 défendu par 1 Défenseur ; 3 machines au rang 1 et 2 Insectes sur ce rang : 3 machines annulées (1 + 2), 2 Insectes défaussés.",
          "etat_attendu_verifie": {
            "machines_annulees": 3,
            "insectes_defausses": 2
          },
          "statut": "A_CODER"
        },
        {
          "id": "R6_T2",
          "resume": "Plancher (Tour 2, aucun Nid construit, aucun Insecte en jeu) : le Rite, au rang 3, est défendu par 1 Défenseur face à 2 machines. Cueillette sauvage : 1 Insecte de la réserve sur le rang 3 ; le gant annule les 2 machines (1 + 1) et l’Insecte est défaussé.",
          "etat_attendu_verifie": {
            "machines_annulees": 2,
            "insecte_reserve_utilise": 1
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Défausser autant d’Insectes que de machines non couvertes au rang du Rêve (avec amorçage depuis la réserve si aucun Insecte n’est en jeu), en gardant 1 Insecte sur la Réglette si une déviation utile reste possible.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R7": {
      "id": "R7",
      "alias_oriente": "E>M",
      "famille": "REVE",
      "origine": "E",
      "voisin": "M",
      "couple": [
        "E",
        "M"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LOI_PASSIVE"
      ],
      "est_twist": false,
      "vecteurs": "Rang du Curupira (E) → les machines y marchent à reculons (frappe derrière, recul) ; Duel (M) reconquis quand elles reculent",
      "entrees_plancher": [
        "RANG_REVE",
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "DUEL"
      ],
      "entrees": [
        "RANG_REVE",
        "POSITION_REVE",
        "RANG_MACHINE",
        "DUEL"
      ],
      "sorties": [
        "RECUL",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "LOI",
        "RECUL",
        "DUEL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Curupira",
        "fenetre_badge": "PERMANENT",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_RECUL",
          "PIC_RANG_MACHINE",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "Loi · à son rang Devant = derrière · avancée = recul · Sur place sans gain de Rouge",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Les machines de son rang marchent à reculons"
      },
      "carte_joueur": {
        "titre_complet": "Le Curupira, protecteur aux pieds retournés",
        "entite_illustree": "Le Curupira — esprit protecteur de la forêt, petit être à la chevelure de flammes rouges et aux pieds tournés vers l’arrière",
        "brief_illustration": "Sentier boueux au crépuscule : le Curupira, chevelure flamboyante, court en sens inverse de ses propres empreintes ; des chenilles de machine suivent ces traces et reculent vers la lisière ; derrière lui, un jaguar et un tapir l’observent, à l’abri. Rouges flamme, verts sombres, boue ocre.",
        "pitch_ambiance": "Le Curupira protège les bêtes et punit qui abat trop d’arbres. Ses pieds tournés à l’envers laissent des traces qui égarent les chasseurs : qui croit le suivre s’éloigne de lui, et retourne d’où il vient.",
        "texte_regle": {
          "face_1": "Loi passive — Pieds à l’envers (tant que le Curupira est sur la Réglette, défendu ou non) : toute machine non annulée qui attaque depuis le rang du Curupira marche à reculons. Sa frappe « Devant » vise la parcelle située derrière elle, côté bordure (en sautant les Routes Forestières ; s’il n’y en a aucune, la frappe se perd). L’avancée d’« En avançant » devient un recul d’1 parcelle. Une frappe « Sur place » depuis ce rang ne fait gagner aucun Rouge en Mode Charge. Protecteur des bêtes : quand une machine recule ainsi hors de la parcelle qui porte le jeton Duel face Défi, retournez le Duel sur Territoire tenu. Comme tout Rêve défendu, le Curupira annule à son rang 1 machine par Défenseur : à vous de choisir celles que vous laissez marcher à reculons.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Annuler une machine de son rang, ou la laisser marcher à reculons : frappe derrière elle, puis recul d’1 parcelle.",
          "renoncement": "Une machine laissée active frappe quand même : derrière elle, une parcelle de bordure encore boisée peut y perdre ses Arbres."
        }
      },
      "temoins": [
        {
          "id": "R7_T1",
          "resume": "Curupira au rang 3 (Acte 1, Charge) ; un Bulldozer en parcelle 2, non annulé, frappe la parcelle 2 puis la parcelle 1 (derrière), et recule en parcelle 1.",
          "etat_attendu_verifie": {
            "bulldozer": {
              "position": "p1"
            },
            "frappes": [
              "p2",
              "p1"
            ]
          },
          "statut": "A_CODER"
        },
        {
          "id": "R7_T2",
          "resume": "Abatteuse au rang 2 du Curupira, en parcelle 1 (aucune parcelle derrière elle) : sa frappe se perd.",
          "etat_attendu_verifie": {
            "frappe_perdue": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Laisser marcher à reculons la machine dont la parcelle de derrière est une Route ou une clairière ; annuler en priorité celle dont la parcelle de derrière est la plus boisée.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R8": {
      "id": "R8",
      "alias_oriente": "E>R",
      "famille": "REVE",
      "origine": "E",
      "voisin": "R",
      "couple": [
        "E",
        "R"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LOI_PASSIVE",
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "LOI_PASSIVE_PISTON_ECAILLE_ALTERATION_VENIN_CROC_BLEU_RECUL",
      "entrees_plancher": [
        "POSITION_REVE",
        "ALTERATION",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "ECAILLE",
        "CROC",
        "ROUGE"
      ],
      "entrees": [
        "POSITION_REVE",
        "ALTERATION",
        "RANG_MACHINE",
        "ECAILLE",
        "CROC",
        "ROUGE"
      ],
      "sorties": [
        "RANG_REVE",
        "ALTERATION",
        "BLEU",
        "RECUL"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [
        "LOI_PASSIVE",
        "LEVIER_REVE",
        "ECAILLE",
        "CROC"
      ],
      "tuile_plateau": {
        "nom_court": "Mue d’Obsidienne",
        "fenetre_badge": "PERMANENT",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_ECAILLE",
          "PIC_ALTERATION",
          "PIC_CROC"
        ],
        "mots_cles_plateau": {
          "face_1": "Passif : 🦎/Défendu → Glisse 1G & 🌀 · 🦷 pare → 🔴→🔵 (sinon ⏪ 1)",
          "face_2": null,
          "enracine": "Standard (1 Souche finale, bloque Sommeil)"
        },
        "resume_plateau": "Écailles glissent rêves · Croc refroidit"
      },
      "carte_joueur": {
        "titre_complet": "Le Rêve de la Mue d’Obsidienne",
        "entite_illustree": "Mue translucide d'obsidienne d'un grand serpent enroulée autour d'une lame givrée",
        "brief_illustration": "Suspendue entre deux troncs noirs baignés de lueurs violettes, la mue translucide et tranchante comme du verre volcanique d'un grand serpent s'enroule autour d'une lame de scie couverte de givre bleu.",
        "pitch_ambiance": "« Le reptile abandonne son ancienne peau aux esprits de la nuit ; quiconque y mord sent le gel remonter jusqu'au cœur du moteur. »",
        "texte_regle": {
          "face_1": "Tant que ce Rêve occupe un rang de la Réglette (même sans Défenseur posé sur lui) :\n• Piston d'Écaille (À l'ouverture) : chaque fois qu'un jeton Écaille est révélé à l'ouverture des paravents — ainsi que lorsque ce Rêve lui-même est défendu à sa résolution d'ouverture — faites glisser 1 Rêve en jeu de votre choix (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.\n• Venin d'Obsidienne (Aux attaques) : chaque fois que le jeton Croc Reptile pare la frappe d'une machine (juste avant que le Croc ne regagne la réserve Reptile) : si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge) et qu'elle est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Laisser R8 sans Défenseur pour profiter passivement des Écailles et du Croc tout en économisant des poses, ou le défendre activement pour garantir un glissement et une Altération même sans Écaille tirée.",
          "renoncement": "Défendre R8 immobilise un Défenseur sur la Réglette ; le laisser vide renonce à l'annulation sur son rang et au déclenchement garanti lors des tours sans Écaille."
        }
      },
      "temoins": [
        {
          "id": "R8_T1",
          "resume": "Tour 5, R8 non défendu au rang 4, un autre Rêve au rang 3. Une Écaille révélée pose le Croc en parcelle 3 de R et déclenche Piston d'Écaille (Rêve 3 → 2 + Altération sur une Abatteuse). Aux attaques, un Bulldozer sans Rouge est paré par le Croc : Venin d'Obsidienne le recule en parcelle 2 avant le retour du Croc en réserve.",
          "etat_attendu_verifie": {
            "reve_glisse_rang_2": true,
            "bulldozer_recul_p2": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Construire R8 tôt avec des Écailles au sac (via G10/M2) pour générer glissements de Rêves et Altérations sans consommer de Défenseur ; le défendre si son rang porte une menace.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R9": {
      "id": "R9",
      "alias_oriente": "E>O",
      "famille": "REVE",
      "origine": "E",
      "voisin": "O",
      "couple": [
        "E",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "LEVIER_REVE"
      ],
      "est_twist": false,
      "vecteurs": "Plume de Vigie (O) posée près d’un rang → le Rêve (E) s’y envole et annule ; échec = Altération",
      "entrees_plancher": [
        "PLUME",
        "RANG_REVE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "PLUME",
        "RANG_REVE"
      ],
      "sorties": [
        "POSITION_REVE",
        "ALTERATION"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_REVE"
      ],
      "double_ouverture": null,
      "tags": [
        "LEVIER",
        "PLUME",
        "ALTERATION"
      ],
      "tuile_plateau": {
        "nom_court": "La Matinta Pereira",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_PLUME",
          "PIC_AVANCEE_REVE",
          "PIC_ALTERATION"
        ],
        "mots_cles_plateau": {
          "face_1": "Vole de 2 rangs au plus vers la Plume · 0 annulation = 1 Altération",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Le Rêve vole là où siffle la Plume"
      },
      "carte_joueur": {
        "titre_complet": "La Matinta Pereira, siffleuse de minuit",
        "entite_illustree": "La Matinta Pereira — vieille sorcière de la forêt qui prend la forme d’un oiseau noir au sifflement strident",
        "brief_illustration": "Minuit sur un village sur pilotis : une vieille femme drapée de noir se dissout en un oiseau sombre qui s’élève en sifflant ; son vol trace une ligne lumineuse vers une plume posée près d’un rang de la Réglette ; sur un seuil, une offrande de tabac. Noirs, violets, argent lunaire.",
        "pitch_ambiance": "Le sifflement de la Matinta semble venir de partout à la fois. Promettez-lui du tabac et elle s’en va ; refusez, et votre nuit sera maudite.",
        "texte_regle": {
          "face_1": "Quand ce Rêve est défendu, à sa résolution, avant d’annuler : la Matinta vole vers le sifflement : si la Plume de Vigie est posée près d’un rang de la Réglette, déplacez ce Rêve, avec ses Défenseurs, d’au plus 2 rangs en direction de ce rang (sans le dépasser ni traverser un rang occupé), puis annulez-y normalement ; un Rêve ne se résout qu’une fois par ouverture. Malédiction : si ce Rêve n’annule finalement aucune machine, posez 1 jeton d’Altération sur une machine mobile de votre choix qui n’en porte pas.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Pour l’Oiseau : poser la Plume près du rang où il sait qu’une machine tombera (la sienne ou celle vue au Perchoir), ou près d’un rang qui compacte le bloc du Sommeil.",
          "renoncement": "Poser la Plume près d’un rang, c’est renoncer à l’utiliser au pied d’un rayon pour signaler Chaud ou Calme aux rives de Furtivité."
        }
      },
      "temoins": [
        {
          "id": "R9_T1",
          "resume": "Matinta défendue au rang 4 ; la Plume est posée près du rang 2, libre, où l’Oiseau a révélé sa machine : le Rêve vole de 2 rangs jusqu’au rang 2 et l’annule.",
          "etat_attendu_verifie": {
            "matinta_rang": 2,
            "machine_annulee": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "R9_T2",
          "resume": "Plume au pied d’un rayon (pas près d’un rang) et aucune machine au rang 6 : la Matinta n’annule rien et pose 1 Altération.",
          "etat_attendu_verifie": {
            "alterations_posees": 1
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Côté Oiseau : poser la Plume près du rang de sa propre machine s’il est libre. Côté Entités : défendre la Matinta dès que la Plume est posée près d’un rang.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "R10": {
      "id": "R10",
      "alias_oriente": "E>I",
      "famille": "REVE",
      "origine": "E",
      "voisin": "I",
      "couple": [
        "E",
        "I"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "TWIST_2K3",
        "LEVIER_REVE"
      ],
      "est_twist": true,
      "vecteurs": "SILLAGE_ONIRIQUE_TRANSHUMANCE_NID_GARNISON_ALTERATION_BLEU_A0",
      "entrees_plancher": [
        "POSITION_REVE",
        "RANG_MACHINE"
      ],
      "entrees_synergie": [
        "NID",
        "INSECTE",
        "ROUGE"
      ],
      "entrees": [
        "POSITION_REVE",
        "RANG_MACHINE",
        "NID",
        "INSECTE",
        "ROUGE"
      ],
      "sorties": [
        "RANG_REVE",
        "NID_DEPLACE",
        "ALTERATION",
        "INSECTE",
        "BLEU"
      ],
      "paiement": [
        "P_RANG"
      ],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES",
        "TWIST_2K3",
        "LEVIER_REVE",
        "TRANSHUMANCE_NID"
      ],
      "tuile_plateau": {
        "nom_court": "Ruche Vagabonde",
        "fenetre_badge": "OUVERTURE",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_AVANCEE_REVE",
          "PIC_NID",
          "PIC_ALTERATION",
          "PIC_BLEU"
        ],
        "mots_cles_plateau": {
          "face_1": "Glisse 1G + [Déplace 1 🪹 (+🐜 & 🛡️) partout & 🌀/🔴→🔵 OU +1 🐜 & +1 🌀]",
          "face_2": null,
          "enracine": "Standard (1 Souche finale, bloque Sommeil)"
        },
        "resume_plateau": "Glisse rêve, déménage une ruche"
      },
      "carte_joueur": {
        "titre_complet": "La Transe de la Ruche Vagabonde",
        "entite_illustree": "Immense ruche d'écorce vivante flottant dans la nuit portée par des filaments de brume",
        "brief_illustration": "Portée par des filaments de brume violette à travers la nuit amazonienne, une immense ruche d'écorce vivante flotte entre les troncs avec toute sa nuée lumineuse pour venir se greffer juste devant la lame d'un engin surpris.",
        "pitch_ambiance": "« Guidé par le songe, le nid décroche ses racines d'écorce et traverse la nuit : quand l'acier frappe la clairière, la ruche est déjà derrière lui. »",
        "texte_regle": {
          "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :\n1. Sillage Onirique : faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).\n2. Transhumance de la Ruche (Twist spatial) : choisissez 1 seul des deux effets suivants :\n• Envol de la Ruche (si au moins 1 Nid est en forêt) : déplacez 1 Nid construit — en emportant simultanément avec lui tous les Insectes et tous les Défenseurs présents sur sa parcelle — vers n'importe quelle autre parcelle dépourvue d'autre Nid sur n'importe quel rayon du plateau (y compris hors des rayons voisins des Insectes, et y compris sur une parcelle occupée par une machine). Ensuite, posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération du rayon rejoint — ou, sur une machine occupant la parcelle rejointe et possédant au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.\n• Essaim Spectral (toujours disponible, y compris si aucun Nid n'est en forêt) : posez 1 jeton Insecte de la réserve sur une parcelle du rayon Entités ou du rayon Insectes (ou sur un rang 1–6 de la Réglette), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Téléporter un Nid défendu et toute sa garnison directement devant une machine lointaine pour produire sur place à la Production puis parer aux attaques, ou choisir Essaim Spectral en solo.",
          "renoncement": "Déménager le Nid abandonne son ancien secteur et expose le Nid au renvoi en lisière si un Bulldozer transforme la parcelle rejointe en Route Forestière."
        }
      },
      "temoins": [
        {
          "id": "R10_T1",
          "resume": "Tour 4 (table {H, E, I}), M5 en parcelle 1 de I (1 Défenseur, 2 Insectes) tandis qu'un Bulldozer (1 Rouge, seuil 4) menace la parcelle 4 de H. R10 glisse du rang 3 au rang 2 libre puis choisit Envol de la Ruche : M5 atterrit en H·4 avec son Défenseur et ses 2 Insectes, retourne le Rouge en Bleu (seuil 4 → 2), produit +2 Insectes à la Production et pare aisément aux attaques.",
          "etat_attendu_verifie": {
            "nid_deplace_h4": true,
            "seuil_bulldozer": 2
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Glisser un Rêve chaque tour et téléporter un Nid garni directement sur la parcelle la plus menacée du plateau (en retournant un Rouge en Bleu) ; sans Nid en forêt, jouer Essaim Spectral.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "M1": {
      "id": "M1",
      "alias_oriente": "I>M",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "M",
      "couple": [
        "I",
        "M"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Insectes (I) en phorésie sur une machine → parade là où elle frappe, descente au cœur au ménage ; Duel (M) retourné par une parade aidée",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [
        "DUEL"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "DUEL"
      ],
      "sorties": [
        "INSECTE_PASSAGER",
        "TERRITOIRE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": null,
      "tags": [
        "PASSAGER",
        "PHORESIE",
        "DUEL"
      ],
      "tuile_plateau": {
        "nom_court": "Le Pelage du Paresseux",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_MIGRATION",
          "PIC_DUEL"
        ],
        "mots_cles_plateau": {
          "face_1": "2 Insectes montent sur une machine voisine · sautent sur la parcelle frappée · descente au ménage",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Des passagers qui voyagent sur les machines"
      },
      "carte_joueur": {
        "titre_complet": "Le Pelage du Paresseux",
        "entite_illustree": "Nid vivant — le pelage d’un paresseux à trois doigts, verdi d’algues, où vivent des papillons et de minuscules passagers",
        "brief_illustration": "Gros plan sur un paresseux suspendu à une branche, sa fourrure verte d’algues grouillant de petits papillons et d’insectes ; certains s’envolent vers la chenille d’une machine qui passe sous l’arbre et s’y agrippent ; sur la parcelle voisine, le jeton Duel. Verts mousse, gris, ambre.",
        "pitch_ambiance": "La fourrure du paresseux est un monde : des algues, des champignons, des papillons qui n’existent nulle part ailleurs. Ces passagers voyagent sans bouger leurs ailes, et savent descendre au bon endroit.",
        "texte_regle": {
          "face_1": "Production (quand ce Nid est défendu, après avoir produit) : les passagers embarquent : jusqu’à 2 Insectes de ce Nid montent, comme passagers, sur une machine mobile de sa parcelle ou d’une parcelle adjacente du même rayon, et voyagent avec elle. Quand cette machine frappe une parcelle, ses passagers peuvent sauter sur la parcelle frappée et y compter comme Insectes présents pour la parade. Si cette parcelle porte le jeton Duel, une parade aidée par un passager y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère. Au ménage, tout passager non dépensé descend sur place, sur la parcelle de sa machine.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Sur quelle machine embarquer : celle qui va frapper une parcelle à défendre, ou celle qui avance vers le cœur pour y déposer l’Essaim au ménage.",
          "renoncement": "Les passagers quittent le Nid : sa prochaine Production sera plus faible et sa parcelle perd ces renforts."
        }
      },
      "temoins": [
        {
          "id": "M1_T1",
          "resume": "2 passagers sur le Bulldozer du rayon M ; il frappe la parcelle 3 (1 Défenseur, Seuil 3) : les 2 passagers sautent, parade avec Insectes (icône Insecte).",
          "etat_attendu_verifie": {
            "parade": "INSECTE",
            "passagers_defausses": 2
          },
          "statut": "A_CODER"
        },
        {
          "id": "M1_T2",
          "resume": "Un passager non dépensé ; sa machine termine en dernière parcelle : au ménage, il descend sur cette parcelle.",
          "etat_attendu_verifie": {
            "insectes_derniere_parcelle": 1
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Embarquer sur la machine révélée au rang le plus élevé (elle frappe tard, quand les autres parades sont connues) ; sinon sur celle qui avance vers le cœur.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "M2": {
      "id": "M2",
      "alias_oriente": "I>R",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "R",
      "couple": [
        "I",
        "R"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [],
      "est_twist": false,
      "vecteurs": "Soldats de la termitière (I) → parade autonome à 2 Insectes ; argile → Écaille (R) au sac (matière des pontes du Téju) ou Croc posté",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [],
      "entrees": [
        "NID",
        "INSECTE"
      ],
      "sorties": [
        "PARADE_SOLDATS",
        "ECAILLE",
        "CROC"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE",
        "ICONE_PIEGEAGE"
      ],
      "double_ouverture": null,
      "tags": [
        "FORTERESSE",
        "ECAILLE",
        "CROC",
        "ESSAIM"
      ],
      "tuile_plateau": {
        "nom_court": "La Termitière-Forteresse",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_INSECTE",
          "PIC_ECAILLE",
          "PIC_CROC"
        ],
        "mots_cles_plateau": {
          "face_1": "2 Insectes du Nid parent seuls toute frappe · Production = 1 Écaille au sac ou Croc posté",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Forteresse d’argile et soldats à glu"
      },
      "carte_joueur": {
        "titre_complet": "La Termitière-Forteresse",
        "entite_illustree": "Nid vivant — une termitière de terre cuite au soleil, hérissée de cheminées, défendue par des soldats à tête-seringue",
        "brief_illustration": "Une termitière haute comme un homme, parois ocres striées, cheminées fumantes ; à sa base, des soldats à tête en pointe projettent une glu luisante sur la chenille d’une machine ; un lézard se chauffe au sommet ; quelques écailles d’argile brillent sur la paroi. Ocres, rouilles, éclats dorés.",
        "pitch_ambiance": "Le mur de la termitière est plus dur que la brique. Ses soldats, la tête en forme de seringue, projettent une glu qui colle tout ce qui ose y toucher. Les reptiles le savent : il n’est pas d’abri plus sûr.",
        "texte_regle": {
          "face_1": "Les soldats (quand une machine frappe la parcelle de ce Nid) : avant la parade classique, vous pouvez défausser 2 Insectes de ce Nid ; ils parent cette frappe à eux seuls, quel que soit le Seuil de Parade (allumez l’icône Insecte). Argile d’écailles (à la Production, quand ce Nid est défendu, après avoir produit), choisissez : le joueur Reptile glisse 1 Écaille de sa réserve dans le sac ; ou, si le Croc est dans la réserve Reptile et qu’une machine mobile se trouve sur la parcelle de ce Nid, postez le Croc sur cette parcelle.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Faire tenir la termitière par ses soldats (2 Insectes par frappe) ou garder ces Insectes pour produire et migrer.",
          "renoncement": "Chaque défense des soldats vide le Nid de 2 Insectes et affaiblit sa prochaine Production ; une Écaille glissée au sac ne servira plus aux pontes du Téju."
        }
      },
      "temoins": [
        {
          "id": "M2_T1",
          "resume": "Nid à 3 Insectes en parcelle 2 ; une Abatteuse en Mode Assaut à 2 Rouges y frappe (Seuil 4) sans aucun Défenseur : 2 Insectes défaussés, frappe parée, icône Insecte.",
          "etat_attendu_verifie": {
            "parade": "SOLDATS",
            "nid_insectes": 1,
            "icone": "INSECTE"
          },
          "statut": "A_CODER"
        },
        {
          "id": "M2_T2",
          "resume": "Production défendue, aucune machine sur la parcelle : le joueur Reptile glisse 1 Écaille au sac.",
          "etat_attendu_verifie": {
            "sac_ecailles": "+1"
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Faire parer les soldats quand le Seuil de la frappe dépasse Défenseurs + Insectes disponibles ; à la Production, poster le Croc si une machine mobile partage la parcelle.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "M3": {
      "id": "M3",
      "alias_oriente": "I>O",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "O",
      "couple": [
        "I",
        "O"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "TWIST_2K3"
      ],
      "est_twist": true,
      "vecteurs": "Nid (I) qui lève le camp à chaque Production, guidé par la Plume de Vigie (O) ; front de raid vers la parcelle visée ; Insectes offerts au Colibri",
      "entrees_plancher": [
        "NID",
        "INSECTE"
      ],
      "entrees_synergie": [
        "PLUME"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "PLUME"
      ],
      "sorties": [
        "NID_NOMADE",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [
        "ICONE_INSECTE"
      ],
      "double_ouverture": null,
      "tags": [
        "TWIST",
        "NOMADE",
        "PLUME",
        "RAID"
      ],
      "tuile_plateau": {
        "nom_court": "Le Bivouac des Légionnaires",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_TWIST",
          "PIC_NID",
          "PIC_MIGRATION",
          "PIC_PLUME"
        ],
        "mots_cles_plateau": {
          "face_1": "Chaque Production · le Nid se déplace d’1 parcelle (2 vers la Plume) · raid de 2 Insectes",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Un Nid nomade qui suit la Plume"
      },
      "carte_joueur": {
        "titre_complet": "Le Bivouac des Légionnaires",
        "entite_illustree": "Nid vivant nomade — le bivouac des fourmis légionnaires, boule de centaines de milliers de corps entrelacés suspendue sous un tronc",
        "brief_illustration": "Aube : sous un tronc couché, une masse vivante de fourmis légionnaires forme des chambres et des couloirs de leurs propres corps ; une colonne s’étire déjà vers la parcelle voisine ; au-dessus, des oiseaux fourmiliers suivent le front de raid, et une plume de vigie est plantée au bout du chemin. Bruns rouges, noirs, lumière rasante.",
        "pitch_ambiance": "Le bivouac n’a pas de murs : ce sont les fourmis elles-mêmes, accrochées les unes aux autres. Chaque nuit, la colonne repart ; et derrière son front de raid, les oiseaux fourmiliers suivent, guettant ce qui s’enfuit.",
        "texte_regle": {
          "face_1": "Nid nomade (à chaque Production, avant de produire, que ce Nid soit défendu ou non) : le bivouac lève le camp : déplacez ce Nid, avec ses Insectes, vers une parcelle libre (sans machine ni autre Nid) adjacente : sur le même rayon, ou à la parcelle de même numéro d’un rayon voisin. Si ce déplacement le rapproche du rayon désigné par la Plume de Vigie, ou le garde sur ce rayon, il peut enchaîner 2 parcelles adjacentes libres au lieu d’1 : les oiseaux fourmiliers guident la colonne. Puis, s’il est défendu à sa nouvelle place, il produit normalement. Front de raid (après la production) : jusqu’à 2 Insectes du bivouac peuvent se poster sur une parcelle adjacente visée par une machine révélée, où ils participeront aux parades.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Où lever le camp : vers la parcelle menacée pour y lancer le raid, ou loin d’un Bulldozer qui menace d’en faire une Route.",
          "renoncement": "Le bivouac qui quitte la parcelle de son Défenseur ne produit pas ; et un Nid qui s’approche des machines risque d’être renvoyé en lisière."
        }
      },
      "temoins": [
        {
          "id": "M3_T1",
          "resume": "Bivouac en parcelle 1 du rayon I ; la Plume est au pied du rayon O voisin : le Nid passe en parcelle 1 du rayon O puis en parcelle 2 (2 pas vers la Plume) ; défendu là, il produit.",
          "etat_attendu_verifie": {
            "nid_position": "O_p2",
            "production": true
          },
          "statut": "A_CODER"
        },
        {
          "id": "M3_T2",
          "resume": "Front de raid : 2 Insectes du bivouac se postent sur la parcelle 3 visée du rayon O.",
          "etat_attendu_verifie": {
            "insectes_O_p3": 2
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Lever le camp vers une parcelle visée adjacente qui porte un Défenseur (pour produire) ; fuir toute parcelle réduite à 1 pièce visée par un Bulldozer.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "M4": {
      "id": "M4",
      "alias_oriente": "I>H",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "H",
      "couple": [
        "I",
        "H"
      ],
      "cycle": "SIMPLE_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0"
      ],
      "est_twist": false,
      "vecteurs": "Insecte (I) consommé → bâtisseur en attente relevé sur la parcelle du Nid ou du Tambour (H)",
      "entrees_plancher": [
        "NID",
        "INSECTE",
        "DEFENSEUR_ATTENTE"
      ],
      "entrees_synergie": [
        "TAMBOUR"
      ],
      "entrees": [
        "NID",
        "INSECTE",
        "DEFENSEUR_ATTENTE",
        "TAMBOUR"
      ],
      "sorties": [
        "DEFENSEUR_REDEPLOYE",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "ACTION",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "BATISSEURS",
        "TAMBOUR"
      ],
      "tuile_plateau": {
        "nom_court": "Le Rucher des Mélipones",
        "fenetre_badge": "PRODUCTION",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_NID",
          "PIC_DEFENSEUR_ATTENTE",
          "PIC_TAMBOUR",
          "PIC_INSECTE"
        ],
        "mots_cles_plateau": {
          "face_1": "1 Insecte → 1 bâtisseur relevé sur le Nid ou le Tambour · deux fois au plus",
          "face_2": null,
          "enracine": null
        },
        "resume_plateau": "Le miel relève les bâtisseurs"
      },
      "carte_joueur": {
        "titre_complet": "Le Rucher des Mélipones",
        "entite_illustree": "Nid vivant — une ruche d’abeilles sans dard (mélipones) logée dans un tronc creux, avec son tube d’entrée de cire",
        "brief_illustration": "Tronc creux au bord d’un jardin villageois : un tube de cire brune où entrent et sortent de petites abeilles sans dard ; un chamane y recueille une calebasse de miel ; à côté, deux bâtisseurs couchés se relèvent, revigorés. Miels ambrés, bruns, verts tendres.",
        "pitch_ambiance": "Les mélipones n’ont pas de dard ; elles offrent leur miel aux peuples qui les protègent depuis des siècles. Une gorgée, et ceux qui ont bâti jusqu’à l’épuisement se relèvent pour défendre la forêt.",
        "texte_regle": {
          "face_1": "Production (quand ce Nid est défendu, après avoir produit) : le miel des mélipones : défaussez 1 Insecte de ce Nid pour relever 1 Défenseur couché en attente (bâtisseur d’une tuile construite à ce tour) : son propriétaire le pose aussitôt, face Définitif, sur la parcelle de ce Nid ou sur la parcelle qui porte le Tambour, où il compte pour les parades. Vous pouvez recommencer une seconde fois en défaussant 1 autre Insecte.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Relever un bâtisseur (souvent celui qui vient d’achever une tuile) pour défendre le Nid ou la parcelle du Tambour.",
          "renoncement": "Chaque gorgée coûte un Insecte qui ne déviera ni ne parera ; et il faut avoir construit à ce tour pour avoir un bâtisseur à relever."
        }
      },
      "temoins": [
        {
          "id": "M4_T1",
          "resume": "Un Rêve vient d’être construit par 2 bâtisseurs couchés ; Production du Rucher défendu : 1 Insecte défaussé, 1 bâtisseur posé sur la parcelle du Tambour.",
          "etat_attendu_verifie": {
            "defenseurs_en_attente": 1,
            "defenseurs_parcelle_tambour": "+1"
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Relever un bâtisseur dès que la parcelle du Nid ou du Tambour est visée avec un déficit de 1 au Seuil.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    },
    "M5": {
      "id": "M5",
      "alias_oriente": "I>E",
      "famille": "CROISSANCE",
      "origine": "I",
      "voisin": "E",
      "couple": [
        "I",
        "E"
      ],
      "cycle": "PASSIF_CONTINU",
      "cablage": null,
      "roles_portes": [
        "AUTONOMIE_A0",
        "LOI_PASSIVE"
      ],
      "est_twist": false,
      "vecteurs": "LOI_PASSIVE_SPORES_DEVIATION_REVE_ALTERATION_RECYCLAGE_FILAMENTS_A0",
      "entrees_plancher": [
        "NID_ACTIVE",
        "INSECTE"
      ],
      "entrees_synergie": [
        "INSECTE_RANG",
        "POSITION_REVE"
      ],
      "entrees": [
        "NID_ACTIVE",
        "INSECTE",
        "INSECTE_RANG",
        "POSITION_REVE"
      ],
      "sorties": [
        "ALTERATION",
        "INSECTE_RANG",
        "INSECTE"
      ],
      "paiement": [],
      "nature": "LOI_PASSIVE",
      "declencheurs_amorces": [],
      "double_ouverture": null,
      "tags": [
        "A0",
        "INSECTES",
        "LOI_PASSIVE",
        "DEVIATION",
        "ALTERATION"
      ],
      "tuile_plateau": {
        "nom_court": "Mycélium Luminescent",
        "fenetre_badge": "PERMANENT",
        "icone_conseillee": null,
        "pictogrammes": [
          "PIC_LOI_PASSIVE",
          "PIC_REVE",
          "PIC_ALTERATION",
          "PIC_INSECTE"
        ],
        "mots_cles_plateau": {
          "face_1": "Passif : Déviation ±1 vers 🌙 → +1 🌀 & recycle 🐜 sur M5 (si <2) · Production → 1 🐜 vers Réglette OU +1 🌀",
          "face_2": null,
          "enracine": "Standard (1 Souche finale)"
        },
        "resume_plateau": "Déviations vers rêves altèrent, recyclent"
      },
      "carte_joueur": {
        "titre_complet": "Le Mycélium Luminescent, Réseau Spectral des Racines Noires",
        "entite_illustree": "Entrelacs de champignons bioluminescents bleu-vert sous un grand arbre creux",
        "brief_illustration": "Sous l'humus sombre d'un grand arbre creux colonisé par les insectes, un entrelacs de champignons bioluminescents bleu-vert relie les galeries souterraines jusqu'aux chenilles d'un bulldozer égaré dans une brume de spores.",
        "pitch_ambiance": "« Ce que l'insecte touche là-haut résonne aussitôt sous l'humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé. »",
        "texte_regle": {
          "face_1": "Tant que ce Nid est en forêt (même sans Défenseur posé sur lui — et en plus de sa production standard +1 ou +2 lorsqu'il est défendu) :\n• Spores de Déviation (À l'ouverture) : chaque fois qu'un Insecte posé sur la Réglette est défaussé à l'ouverture pour décaler le dé d'une machine (±1) vers un rang portant un Rêve (défendu ou non), posez immédiatement 1 jeton d'Altération de la réserve Entités sur cette machine mobile si elle n'en porte pas encore (elle peut ensuite être annulée normalement si ce Rêve est défendu) ; de plus, si la parcelle de ce Nid contient alors strictement moins de 2 Insectes, replacez cet Insecte sur la parcelle de ce Nid au lieu de le remettre en réserve.\n• Filaments Oniriques (À la Production des Nids) : lorsque ce Nid est défendu à l'étape de Production, après sa production standard (+1 ou +2, avant la Migration), choisissez 1 effet : transférez directement 1 Insecte présent sur sa parcelle vers le rang 1–6 de votre choix de la Réglette, OU posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.",
          "face_2": null,
          "enracine": null
        },
        "decision_et_renoncement": {
          "choix": "Expédier 1 Insecte sur la Réglette à la Production pour amorcer la boucle Spores de Déviation (en restant sous 2 Insectes pour recycler gratuitement l'ouvrière), ou poser immédiatement 1 Altération directe.",
          "renoncement": "Rester sous 2 Insectes sur M5 maintient sa production à +1 au lieu de +2 ; dévier une machine vers un Rêve non défendu lui inflige une Altération mais ne l'annule pas à ce tour."
        }
      },
      "temoins": [
        {
          "id": "M5_T1",
          "resume": "Tour 3, M5 défendu (0 Insecte) produit +1 et envoie cet Insecte sur le rang 4 via Filaments Oniriques (M5 revient à 0). À l'ouverture du Tour 4, I dévie une Abatteuse du rang 4 vers le Rêve du rang 3 : Spores de Déviation pose 1 Altération sur l'Abatteuse et replace l'Insecte sur M5 (< 2 Insectes), puis le Rêve défendu annule l'Abatteuse à ce tour.",
          "etat_attendu_verifie": {
            "alteration_posee": true,
            "insecte_recycle_m5": true
          },
          "statut": "A_CODER"
        }
      ],
      "heuristique_bot": "Maintenir un flux d'Insectes sur les rangs adjacents aux Rêves via Filaments Oniriques pour transformer chaque déviation ±1 en double neutralisation (annulation + Altération) avec recyclage gratuit sur M5.",
      "engine_sync_status": "DESIGNED_V6_3",
      "statut_conception": "PASSE_1_CREATIF"
    }
  }
};

const AUTHOR_WORKSPACE_INITIAL_V6_4 = null;
