// =========================================================================
// data/amazonia_data_v6_0.js — Généré automatiquement depuis contracts/ (SSOT v6.2.0 · 30 tuiles Canon 0 · Châssis unique verrouillé)
// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.
// =========================================================================
const PEUPLES = {
  "M": {
    "code": "M",
    "nom": "Mammifères",
    "famille": "Animal Sauvage (Gardien)",
    "categorie": "ANIMAL_SAUVAGE",
    "accessoire_mode": "ACTIF_TOUR_1",
    "badge": "bg-amber-100 text-amber-900 border-amber-300",
    "icon": "🐆"
  },
  "R": {
    "code": "R",
    "nom": "Reptiles",
    "famille": "Animal Sauvage (Gardien)",
    "categorie": "ANIMAL_SAUVAGE",
    "accessoire_mode": "PROGRESSIF_TUILES",
    "badge": "bg-emerald-100 text-emerald-900 border-emerald-300",
    "icon": "🐍"
  },
  "O": {
    "code": "O",
    "nom": "Oiseaux",
    "famille": "Animal Sauvage (Gardien)",
    "categorie": "ANIMAL_SAUVAGE",
    "accessoire_mode": "ACTIF_TOUR_1",
    "badge": "bg-sky-100 text-sky-900 border-sky-300",
    "icon": "🦜"
  },
  "H": {
    "code": "H",
    "nom": "Humains",
    "famille": "Onirique (Rêve)",
    "categorie": "ONIRIQUE",
    "accessoire_mode": "ACTIF_TOUR_1",
    "badge": "bg-rose-100 text-rose-900 border-rose-300",
    "icon": "🏹"
  },
  "E": {
    "code": "E",
    "nom": "Entités Magiques",
    "famille": "Onirique (Rêve)",
    "categorie": "ONIRIQUE",
    "accessoire_mode": "PROGRESSIF_TUILES",
    "badge": "bg-purple-100 text-purple-900 border-purple-300",
    "icon": "✨"
  },
  "I": {
    "code": "I",
    "nom": "Insectes",
    "famille": "Symbiotique (Essaim)",
    "categorie": "ESSAIM",
    "accessoire_mode": "PROGRESSIF_TUILES",
    "badge": "bg-lime-100 text-lime-900 border-lime-300",
    "icon": "🐜"
  }
};

const MATRICE_PAIRES = {
  "M_R": [
    "G1",
    "G2"
  ],
  "R_M": [
    "G2",
    "G1"
  ],
  "M_O": [
    "G3",
    "G4"
  ],
  "O_M": [
    "G4",
    "G3"
  ],
  "R_O": [
    "G5",
    "G6"
  ],
  "O_R": [
    "G6",
    "G5"
  ],
  "M_H": [
    "G7",
    "R3"
  ],
  "H_M": [
    "R3",
    "G7"
  ],
  "M_E": [
    "G8",
    "R7"
  ],
  "E_M": [
    "R7",
    "G8"
  ],
  "R_H": [
    "G9",
    "R4"
  ],
  "H_R": [
    "R4",
    "G9"
  ],
  "R_E": [
    "G10",
    "R8"
  ],
  "E_R": [
    "R8",
    "G10"
  ],
  "O_H": [
    "G11",
    "R5"
  ],
  "H_O": [
    "R5",
    "G11"
  ],
  "O_E": [
    "G12",
    "R9"
  ],
  "E_O": [
    "R9",
    "G12"
  ],
  "M_I": [
    "G13",
    "M1"
  ],
  "I_M": [
    "M1",
    "G13"
  ],
  "R_I": [
    "G14",
    "M2"
  ],
  "I_R": [
    "M2",
    "G14"
  ],
  "O_I": [
    "G15",
    "M3"
  ],
  "I_O": [
    "M3",
    "G15"
  ],
  "H_E": [
    "R1",
    "R2"
  ],
  "E_H": [
    "R2",
    "R1"
  ],
  "H_I": [
    "R6",
    "M4"
  ],
  "I_H": [
    "M4",
    "R6"
  ],
  "E_I": [
    "R10",
    "M5"
  ],
  "I_E": [
    "M5",
    "R10"
  ]
};

const TOPOLOGIES_PISTE_SPEC = {
  "P4_2233": {
    "code": "P4_2233",
    "p_max": 4,
    "dotation": [
      2,
      2,
      3,
      3
    ],
    "somme": 10,
    "arbres_par_rayon": 10,
    "label": "P4_2233 : 4 parcelles [2,2,3,3] (10×N Arbres · Standard unique v6.2)"
  }
};

const CHASSIS_AXES_SPEC = [
  {
    "key": "Profil_Piste",
    "num": 1,
    "label": "1. Profil de Piste & Dotation Seuil Imprimé",
    "defaultVal": "P4_2233",
    "locked": true,
    "options": [
      {
        "val": "P4_2233",
        "text": "P4_2233 : 4 parcelles [2,2,3,3] (10×N Arbres · Standard unique v6.2)"
      }
    ]
  },
  {
    "key": "Regle_Ouverture_Reve_Multiple",
    "num": 2,
    "label": "2. Résolution d'un Rêve défendu à l'ouverture",
    "defaultVal": "UNIQUE_PAR_TOUR",
    "locked": true,
    "options": [
      {
        "val": "UNIQUE_PAR_TOUR",
        "text": "1 résolution par Rêve défendu (Verrouillé · Standard unique v6.2)"
      }
    ]
  },
  {
    "key": "Offset_Seuil_Parade",
    "num": 3,
    "label": "3. Décalage du Seuil de Parade",
    "defaultVal": 0,
    "locked": true,
    "options": [
      {
        "val": 0,
        "text": "Offset 0 — Bleus actifs en tous modes (Verrouillé · Standard unique v6.2)"
      }
    ]
  },
  {
    "key": "Placement_Initial_Machines",
    "num": 5,
    "label": "5. Placement initial des Machines",
    "defaultVal": "BULLDOZER_P1_ABATTEUSE_P2",
    "locked": true,
    "options": [
      {
        "val": "BULLDOZER_P1_ABATTEUSE_P2",
        "text": "Départ décalé : Bulldozer en p=1, Abatteuse en p=2 (Standard unique v6.2)"
      }
    ]
  },
  {
    "key": "Role_Abatteuse_Fin_De_Piste",
    "num": 6,
    "label": "6. Rôle de l'Abatteuse (coupe sans Souches)",
    "defaultVal": "STANDARD_COUPE_ARBRE",
    "locked": true,
    "options": [
      {
        "val": "STANDARD_COUPE_ARBRE",
        "text": "Coupe tous les Arbres debout en Souches, 0 Souche retirée (Verrouillé · v6.2)"
      }
    ]
  },
  {
    "key": "Synergie_Binome_Machines",
    "num": 7,
    "label": "7. Puissance du binôme de machines",
    "defaultVal": "INDIVIDUELLE",
    "locked": true,
    "options": [
      {
        "val": "INDIVIDUELLE",
        "text": "Individuelle propre à chaque machine (Verrouillé · Standard unique v6.2)"
      }
    ]
  }
];

const MODULE_ESSAIM_REGLES_NATIVES = {
  "deviation_reglette": {
    "nom": "Déviation de dé (±1)",
    "fenetre": "OUVERTURE",
    "texte": "À l'ouverture des paravents, défaussez 1 Insecte posé sur un rang de la Réglette pour décaler le dé d'une machine de −1 ou +1 rang (entre 1 et 6), en allumant l'icône Insecte puis balayage."
  },
  "bouclier_de_lisiere": {
    "nom": "Bouclier de lisière (facultatif)",
    "fenetre": "FIN_ATTAQUES",
    "gouverneur": "I",
    "facultatif": true,
    "texte": "En fin d'attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes choisit de défausser ou non 1 Insecte pour maintenir le Gardien en piste sur sa face actuelle (le pari reste perdu)."
  }
};

const PHYSICAL_INVARIANTS_V6_2 = [
  {
    "id": "INV-01",
    "categorie": "MATERIEL",
    "titre": "Dotation finie 10×N pions uniques Arbre / Souche recto-verso",
    "enonce_canonique": "Dotation finie exacte de 10 × N pions uniques recto-verso (Arbre debout / Souche, zéro réserve illimitée). Couper (Abatteuse) = retourner tous les Arbres debout sur place en Souche sans toucher aux Souches ; terrasser (Bulldozer) = retourner 1 Arbre en Souche puis retirer toutes les Souches de la parcelle ; repousse finale = retourner des Souches survivantes en Arbres debout (plafond de dotation initiale 100 % physique).",
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
    "enonce_canonique": "Les jetons Puissance sont des pièces recto-verso portant Rouge (+1) au recto et Bleu Surchauffe (−1) au verso.",
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
    "enonce_canonique": "Chaque joueur dispose de 2 pions Défenseurs recto-verso (Réflexion / Définitif) : le 1er pion est posé directement face Définitif (jamais sur les Gardiens) ; le 2e pion est posé face Réflexion puis retourné irréversiblement sur Définitif, figeant simultanément le jeton Duel ou la Plume de Vigie mobilisés ce tour. Chez les Humains (H), seuls 2 pions Chamanes existent au total (1 Tambour et 1 Chant recto-verso), rendant le binôme imposé auto-vérifiant.",
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
    "titre": "Sac opaque de jetons épais (Machines, Sabotages, Écailles)",
    "enonce_canonique": "La pioche s'effectue dans un sac en tissu opaque contenant les 2N jetons Machine épais, les jetons Sabotage ordinaires et jusqu'à 4 jetons Sabotage Écaille (via tuiles R). Les jetons non piochés restent cachés sans être consultés ; les jetons révélés et celui du Perchoir retournent dans le sac au ménage.",
    "assertions_livret": [
      "sac",
      "opaque",
      "jetons",
      "cachés"
    ],
    "target_test_id": "test_inv05_opaque_bag_tokens_and_remise"
  },
  {
    "id": "INV-06",
    "categorie": "GOUVERNANCE",
    "titre": "Ordre de distribution en pénurie (Coordonnateur horaire, Oiseau en dernier)",
    "enonce_canonique": "En cas de pénurie dans le sac, la distribution s'effectue dans le sens horaire à partir du Coordonnateur, en servant toujours l'Oiseau en dernier (il regarde jusqu'à 2 jetons du sac, en garde 1 si possible et pose l'autre face cachée sur son Perchoir de Vigie).",
    "assertions_livret": [
      "Coordonnateur",
      "Oiseau",
      "en dernier"
    ],
    "target_test_id": "test_inv06_shortage_clockwise_bird_last"
  },
  {
    "id": "INV-07",
    "categorie": "MATERIEL",
    "titre": "Lancer de dés universel sous paravent fermé (zéro fuite sonore)",
    "enonce_canonique": "Sous paravent fermé, tous les joueurs lancent leurs dés (2 dés standards chacun + Dé d'Envol 1–6 chez l'Oiseau sur mini-paravent gradué 1–6), même s'ils ont tiré un Sabotage ou une Écaille (auquel cas leur jet est ignoré), éliminant toute fuite sonore.",
    "assertions_livret": [
      "tous les joueurs lancent",
      "mini-paravent",
      "fuite sonore"
    ],
    "target_test_id": "test_inv07_universal_dice_roll_no_audio_leak"
  },
  {
    "id": "INV-08",
    "categorie": "MATERIEL",
    "titre": "Réglette des Tactiques fixe 1–6 et bandelette d'Acte réversible",
    "enonce_canonique": "La Réglette des Tactiques est fixe sur 6 rangs (cases Rêves au-dessus des actions imprimées 1/4 Sur place, 2/5 Devant, 3/6 En avançant −1) et accompagnée dessous d'une bandelette d'Acte réversible retournée seule au début du Tour 5 sans déplacer ni Rêves ni Insectes.",
    "assertions_livret": [
      "Réglette",
      "bandelette",
      "Tour 5"
    ],
    "target_test_id": "test_inv08_fixed_track_and_reversible_act_strip"
  },
  {
    "id": "INV-09",
    "categorie": "MATERIEL",
    "titre": "Piste des Gardiens à 6 icônes dédiées (Résonance en 6e position)",
    "enonce_canonique": "La Piste des Gardiens comporte 6 icônes dédiées sans numéros dans l'ordre gauche → droite : [Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance]. La Résonance occupe la 6e et dernière position avec compteur individuel des 1res activations d'autres Gardiens du tour sans écrasement de bit, et reprise du balayage gauche → droite si un effet rallume une icône située plus à gauche.",
    "assertions_livret": [
      "Parade",
      "Piégeage",
      "Sabotage",
      "Rêve",
      "Insecte",
      "Résonance"
    ],
    "target_test_id": "test_inv09_six_guardian_icons_resonance_sixth_counter"
  },
  {
    "id": "INV-10",
    "categorie": "MATERIEL",
    "titre": "Deux encoches latérales visibles par Gardien et verdict de pari",
    "enonce_canonique": "Chaque tuile Gardien comporte 2 encoches latérales visibles dans lesquelles glisse 1 Défenseur à chaque activation. En fin d'attaques : ≥ 1 pion encore sur la tuile = pari perdu ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche occupée = aucune mise engagée (le Gardien reste en place sur sa face actuelle sans évoluer).",
    "assertions_livret": [
      "encoches",
      "pari perdu",
      "pari gagné",
      "Face 2"
    ],
    "target_test_id": "test_inv10_guardian_visible_notches_and_zero_bet_no_upgrade"
  },
  {
    "id": "INV-11",
    "categorie": "CAS_LIMITE",
    "titre": "Formule unifiée du Seuil de Parade (Bleus actifs en tous modes)",
    "enonce_canonique": "Seuil de Parade = chiffre gravé + jetons rouges (en Mode Assaut et Ratissage uniquement ; ignorés en Mode Charge) − jetons bleus Surchauffe (actifs dans TOUS les modes : Charge, Assaut et Ratissage) − 1 aux rangs 3 et 6 (minimum 1). En Mode Charge, gain plafonné à +1 jeton rouge par activation dès qu'au moins 1 frappe sur parcelle réelle non-Route n'est ni parée ni piégée.",
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
    "titre": "Ratissage physique (+1 rouge convertible, immobile, parcelle ciblée)",
    "enonce_canonique": "Au ménage, toute machine terminant sur la dernière parcelle de son rayon glisse son jeton Machine sous elle (hors du sac), conserve tous ses jetons Puissance antérieurs et gagne +1 jeton rouge physique (convertible en bleu ; suppression définitive du +1 imprimé). Une machine en Ratissage ne se déplace jamais (ni avancée, ni recul, ni cale, ni Altération, ni changement de rang), mais sa parcelle compte pleinement comme « parcelle ciblée » tant qu'elle n'a pas frappé ce tour.",
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
    "titre": "Parcelles ciblées figées au début de l'activation & Repli de bordure sans double bond",
    "enonce_canonique": "Les parcelles visées par une machine sont figées au début de son activation (toute cible devenue Route Forestière entre-temps est annulée sans report). Si la création d'une Route en bordure pousse déjà une machine d'1 parcelle vers le cœur pendant ses frappes, cette poussée couvre et remplace l'avancée finale d'une action En avançant (jamais de double bond +2 vers le cœur en une activation).",
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
    "titre": "Visibilité des jetons Machine jusqu'à la Furtivité & indépendance de m(r)",
    "enonce_canonique": "Les jetons Machine révélés restent visibles devant leur rayon jusqu'au verdict de Furtivité (inclinés à 90° s'ils sont annulés par un Rêve). La mobilisation m(r) compte uniquement les jetons Machine révélés du rayon r plus ses machines en Ratissage (indépendant d'une déviation ±1, d'une annulation par Rêve ou d'une Altération ; un Sabotage ou une Écaille ne compte pour aucun rayon).",
    "assertions_livret": [
      "90°",
      "Furtivité",
      "Rive Piège",
      "Rive Sabotage"
    ],
    "target_test_id": "test_inv14_machine_tokens_visible_until_furtivite"
  },
  {
    "id": "INV-15",
    "categorie": "CAS_LIMITE",
    "titre": "Séquence stricte d'ouverture, choix du propriétaire du Rêve et Défenseurs solidaires",
    "enonce_canonique": "Ordre strict d'ouverture : chaque Sabotage/Écaille un par un (+ balayage Gardiens) → chaque déviation d'Insecte ±1 une par une (+ balayage) → chaque Rêve défendu de gauche à droite : le propriétaire du Rêve choisit quelle(s) machine(s) présente(s) sur le rang sont annulées (y compris une machine déviée), résout intégralement le pouvoir propre du Rêve (actif dès que le Rêve est défendu même à 0 machine, sauf mention « Quand ce Rêve annule… »), puis si ≥ 1 machine a été annulée (déviée ou non), allume l'icône Rêve + balayage. Les Défenseurs posés sur un Rêve se déplacent toujours avec lui.",
    "assertions_livret": [
      "gauche à droite",
      "propriétaire",
      "déplacent toujours avec lui"
    ],
    "target_test_id": "test_inv15_opening_order_reve_owner_choice_and_moving_defenders"
  },
  {
    "id": "INV-16",
    "categorie": "CAS_LIMITE",
    "titre": "Zéro écrasement au contact hors Route & Vidage sur Route Forestière",
    "enonce_canonique": "Le déplacement d'une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d'une Route Forestière (0 Arbre et 0 Souche après un Bulldozer) vide la case : Nid renvoyé en lisière reconstructible, Défenseurs rendus en main, Piège/Croc/Insectes/Duel remis en réserve. Les Routes Forestières sont sautées radialement et infranchissables latéralement.",
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
    "enonce_canonique": "Une parcelle porte au maximum 1 Piège ordinaire ; tout Piège ordinaire est autonome (pare 1 frappe même avec 0 Défenseur et 0 Insecte, allume l'icône Piégeage et est défaussé aussitôt). Le jeton Croc Reptile peut cohabiter avec un Piège ordinaire sur la même parcelle, pare alors en premier puis revient dans la réserve Reptile.",
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
    "enonce_canonique": "En fin d'attaques, lorsqu'un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes (I) choisit librement de défausser ou non 1 Insecte de cette icône pour maintenir le Gardien en piste sur sa face actuelle (le pari demeurant perdu).",
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
    "titre": "Interdiction de tuile inplaçable, repli de 1re pose, bâtisseurs en attente & bonus 3J",
    "enonce_canonique": "Il est interdit de compléter en lisière une tuile impossible à placer sur le plateau. Si aucun emplacement légal n'existe au 1er temps de pose, le joueur peut placer son 1er Défenseur sur une parcelle d'un allié. Sitôt une tuile construite, ses 2 bâtisseurs sont couchés « en attente » devant leur propriétaire — sauf à 3 joueurs lors de la construction d'un Gardien ou d'un Rêve, où 1 des 2 bâtisseurs rejoint immédiatement une parcelle adjacente.",
    "assertions_livret": [
      "impossible à placer",
      "en attente",
      "3 joueurs"
    ],
    "target_test_id": "test_inv19_unplaceable_tile_ban_builders_waiting_and_3p_bonus"
  },
  {
    "id": "INV-20",
    "categorie": "CAS_LIMITE",
    "titre": "Accessoires 3 + 3 : actifs Tour 1 (H, M, O) et progressifs (E Altération, R Écailles/Croc/Cale)",
    "enonce_canonique": "Trois accessoires actifs dès le Tour 1 (H : Tambour/Chant ; M : Duel Défi↔Territoire tenu ; O : Dé d'Envol/Perchoir/Plume) et trois progressifs via tuiles : E pose un jeton d'Altération directement sur une machine mobile (max 1 ; retiré à sa prochaine révélation, elle compte dans m(r) mais recule d'1 parcelle sans frapper) ; R utilise 4 jetons Écaille (allument Sabotage et posent le Croc réutilisable) et max 1 cale sous machine mobile via G9 ; I gère le Module Essaim.",
    "assertions_livret": [
      "Duel",
      "Plume",
      "Altération",
      "Écaille"
    ],
    "target_test_id": "test_inv20_accessories_3_plus_3_alteration_and_ecaille"
  },
  {
    "id": "INV-21",
    "categorie": "MATERIEL",
    "titre": "Clôture stricte du Module Essaim (I) & descente sur place de l'Insecte passager",
    "enonce_canonique": "Les jetons Insectes sont exclusifs aux 10 tuiles des 5 lisières de I et restent dans la boîte dès que I ne joue pas (Production/Migration ignorées, icône Insecte inactive). Quand I joue, tout Insecte passager (M1) non dépensé descend sur place au ménage.",
    "assertions_livret": [
      "Insectes",
      "boîte",
      "passager"
    ],
    "target_test_id": "test_inv21_swarm_module_closure_and_passenger_dismount"
  },
  {
    "id": "INV-22",
    "categorie": "CAS_LIMITE",
    "titre": "Enracinement volontaire au ménage (1/2 Souches finales & Sommeil bloqué)",
    "enonce_canonique": "Au ménage, avant de remettre les jetons dans le sac, chaque joueur peut enraciner au plus 1 tuile construite de son Peuple au pied de son rayon face à une parcelle : elle perd son pouvoir (hors mention Enraciné), quitte sa piste ou parcelle en y laissant ses Insectes, et un Rêve enraciné rend le Sommeil impossible. Au décompte final (Tour 8, Sommeil ou Éveil), si cette parcelle n'est pas devenue Route Forestière, la tuile y retourne 1 Souche en Arbre debout (F1/unique) ou 2 (F2).",
    "assertions_livret": [
      "enraciner",
      "Sommeil impossible",
      "1 Souche",
      "Face 2"
    ],
    "target_test_id": "test_inv22_voluntary_rooting_regrowth_and_sleep_lock"
  }
];

const CATALOGUE_TUILES = {
  "G1": {
    "id": "G1",
    "famille": "GARDIEN",
    "couple": [
      "M",
      "R"
    ],
    "origine": "M",
    "nomBase": "Le Bond du Jaguar",
    "profils": {
      "A": {
        "nom": "Le Bond du Jaguar",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "DEPLACEMENT (DEFENSEUR EN ATTENTE) + MOD_PUISSANCE",
        "tags": [
          "CATALYSEUR_EVEIL",
          "PARADE_CLASSIQUE",
          "SURCHAUFFE",
          "RECYCLAGE_DEFENSEUR"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Déplacez 1 Défenseur en attente vers une parcelle ciblée des Mammifères ou des Reptiles.<br><strong>Face 2 :</strong> Déplacez 1 Défenseur en attente vers une parcelle ciblée, puis retournez 1 jeton rouge en bleu sur une machine qui la vise.",
        "temoin": "Sur l’icône Parade : une parade au rang 1 active le Jaguar, qui fait bondir un bâtisseur en attente sur la parcelle du Duel visée au rang 2 ; nouvelle parade, 2e activation, pari gagné.",
        "alias_oriente": "M>R",
        "id_profil": "M>R·A",
        "alias_profil": "G1-A",
        "animal_ou_theme": "Jaguar",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (ii) : lisière Animal–Animal M–R"
        ],
        "decision_joueur": {
          "choix": "Quel Défenseur en attente (bâtisseur, Défenseur d’un Rêve ou d’une rive de Furtivité) faire bondir, et sur quelle parcelle ciblée : celle du jeton Duel (bascule en Territoire tenu) ou la plus boisée.",
          "renoncement": "La parcelle non choisie reste découverte ; câblé sur 1 il opère en 5.1, câblé sur 3 il anticipe dès 3.2 mais sans les Défenseurs de Furtivité."
        },
        "entrees": [
          "DEFENSEUR_ATTENTE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "BLEU"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V4 -> V2",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.0,
            "Face 2": 1.5
          },
          "composantes": {
            "Face 1": [
              "DEFENSEUR_REDEPLOYE"
            ],
            "Face 2": [
              "DEFENSEUR_REDEPLOYE",
              "BLEU"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [
          1
        ],
        "double_ouverture": "Chaque ouverture recycle un nouveau Défenseur en attente : deux parades possibles dans le même balayage.",
        "cablage_recommande": "ICONE_PARADE",
        "heuristique_bot": "Câbler sur 1 ; viser en priorité la parcelle du jeton Duel si elle est ciblée, sinon la parcelle ciblée au plus grand nombre d’Arbres ; en Face 2, retourner le rouge de la machine en Assaut.",
        "temoins": [
          {
            "id": "G1_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                1,
                1
              ],
              "p3-M": [
                3,
                "territoire"
              ],
              "paris_restants": 0
            },
            "journal": [
              "B_M -> p1-M : parade par 2 Défenseur(s), Seuil 2 (1)",
              "A_M -> p3-M : parade par 3 Défenseur(s), Seuil 3 (1)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 14,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 22,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "M"
  },
  "G2": {
    "id": "G2",
    "famille": "GARDIEN",
    "couple": [
      "R",
      "M"
    ],
    "origine": "R",
    "nomBase": "L’Étreinte de l’Anaconda",
    "profils": {
      "A": {
        "nom": "L’Étreinte de l’Anaconda",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (SABOTAGE, BONUS DE TERRITOIRE)",
        "tags": [
          "SABOTAGE",
          "ENTROPIE",
          "TERRITOIRE",
          "DEBLOCAGE_PAR_ANCRAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Ajoutez 1 jeton Sabotage au sac, ou 2 si le jeton Duel est sur <em>Territoire tenu</em>.<br><strong>Face 2 :</strong> Ajoutez 2 jetons Sabotage au sac, ou 3 si le jeton Duel est sur <em>Territoire tenu</em>.",
        "temoin": "Jeton Duel sur Territoire tenu : l’Anaconda en Face 1 glisse immédiatement 2 jetons Sabotage de la réserve dans le sac.",
        "alias_oriente": "R>M",
        "id_profil": "R>M·A",
        "alias_profil": "G2-A",
        "animal_ou_theme": "Anaconda vert",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Les Reptiles misent sur le Territoire tenu des Mammifères pour doubler l’injection ; les Mammifères choisissent de risquer le Défi sur une parcelle vraiment frappée.",
          "renoncement": "Un Défi posé loin des frappes ne bascule jamais : l’Anaconda reste au plancher ; une rupture du Duel coupe le bonus pour les tours suivants."
        },
        "entrees": [
          "SABOTAGE"
        ],
        "sorties": [
          "SABOTAGE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V3",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.4,
            "Face 2": 2.1
          },
          "composantes": {
            "Face 1": [
              "SABOTAGE",
              "TERRITOIRE_BONUS"
            ],
            "Face 2": [
              "SABOTAGE",
              "SABOTAGE",
              "TERRITOIRE_BONUS"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Chaque ouverture ajoute un ou deux jetons : la dilution est cumulative.",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Câbler sur 3 (les Sabotages révélés nourrissent la cascade) ; parier dès que le Duel est sur Territoire tenu.",
        "temoins": [
          {
            "id": "G2_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "cartes_sabotage_mises_de_cote": 2
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 16,
            "phrases": 1,
            "conditions": 1
          },
          "Face 2": {
            "mots": 16,
            "phrases": 1,
            "conditions": 1
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "R"
  },
  "G3": {
    "id": "G3",
    "famille": "GARDIEN",
    "couple": [
      "M",
      "O"
    ],
    "origine": "M",
    "nomBase": "La Voltige de l’Atèle",
    "profils": {
      "A": {
        "nom": "La Voltige de l’Atèle",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "DEPLACEMENT (DEFENSEUR, ARCHIPEL DE SOUCHES)",
        "tags": [
          "TWIST",
          "ARCHIPEL_DE_SOUCHES",
          "MOBILITE",
          "DESTRUCTION_VALORISEE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Déplacez 1 Défenseur d’une parcelle à Souche vers la parcelle de même profondeur d’un rayon voisin portant aussi une Souche.<br><strong>Face 2 :</strong> Déplacez jusqu’à 2 Défenseurs entre des parcelles à Souche de même profondeur, d’un rayon à l’autre sur toute la roue.",
        "temoin": "Parcelles p2 des Mammifères et des Oiseaux toutes deux à Souche : le Défenseur de p2-M voltige sur p2-O ciblée au rang 1 et complète la parade.",
        "alias_oriente": "M>O",
        "id_profil": "M>O·A",
        "alias_profil": "G3-A",
        "animal_ou_theme": "Atèle (Singe-araignée)",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A #7 — L’archipel de Souches",
        "role_porte": [],
        "decision_joueur": {
          "choix": "Laisser des Souches debout comme ponts de canopée pour faire voltiger un Défenseur vers le rayon voisin menacé.",
          "renoncement": "La parcelle quittée perd sa défense ; un Bulldozer qui efface les Souches efface aussi le pont."
        },
        "entrees": [
          "SOUCHE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V1 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.0,
            "Face 2": 2.0
          },
          "composantes": {
            "Face 1": [
              "DEFENSEUR_REDEPLOYE"
            ],
            "Face 2": [
              "DEFENSEUR_REDEPLOYE",
              "DEFENSEUR_REDEPLOYE"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Chaque ouverture fait voltiger un nouveau Défenseur.",
        "cablage_recommande": "ICONE_PARADE",
        "heuristique_bot": "Garder au moins une parcelle à Souche par profondeur ; déplacer un Défenseur dont la parcelle n’est plus ciblée.",
        "temoins": [
          {
            "id": "G3_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "voltige_legale": true,
              "vers_p2R_sans_souche_interdite": true,
              "resultat": [
                "pare"
              ]
            },
            "journal": [
              "A_O -> p2-O : parade par 2 Défenseur(s), Seuil 2 (1)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 22,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 23,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "M"
  },
  "G4": {
    "id": "G4",
    "famille": "GARDIEN",
    "couple": [
      "O",
      "M"
    ],
    "origine": "O",
    "nomBase": "Le Cri d’Alarme de l’Ara",
    "profils": {
      "A": {
        "nom": "Le Cri d’Alarme de l’Ara",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (SECURISER_PARI_VOISIN)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "SECURISATION_DE_PARI",
          "COUPLE_INSEPARABLE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Un Gardien voisin de l’Ara glisse 1 de ses Défenseurs de pari dans une encoche.<br><strong>Face 2 :</strong> Chacun des deux Gardiens voisins de l’Ara glisse 1 de ses Défenseurs de pari dans une encoche.",
        "temoin": "Ara placé entre deux Gardiens pariés : un Piège déclenché active l’Ara (son pion glisse dans son encoche) et son cri fait aussi glisser dans son encoche le pion d’un Gardien voisin, sans activer son effet.",
        "alias_oriente": "O>M",
        "id_profil": "O>M·A",
        "alias_profil": "G4-A",
        "animal_ou_theme": "Ara rouge",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (ii) : lisière Animal–Animal M–O"
        ],
        "decision_joueur": {
          "choix": "Où construire l’Ara sur la Piste (entre quels Gardiens pariés) et sur quel déclencheur le câbler pour que son cri sécurise aussi les paris voisins.",
          "renoncement": "Une case voisine vide ou sans pari ne rapporte rien ; coller l’Ara à deux Gardiens pariés concentre le risque du tour sur ce trio."
        },
        "entrees": [
          "GARDIEN"
        ],
        "sorties": [
          "PARI_GLISSE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "vecteurs": "V5 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.0,
            "Face 2": 2.0
          },
          "composantes": {
            "Face 1": [
              "GARDIEN_OUVERT"
            ],
            "Face 2": [
              "GARDIEN_OUVERT",
              "GARDIEN_OUVERT"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Chaque ouverture de l’Ara glisse un nouveau Défenseur de pari chez un voisin : deux ouvertures sécurisent deux paris voisins.",
        "cablage_recommande": "ICONE_PIEGEAGE",
        "heuristique_bot": "Construire entre deux Gardiens déjà pariés ; câbler sur le déclencheur le plus fréquent de la table (1 ou 2) ; parier 2 Défenseurs sur l’Ara.",
        "temoins": [
          {
            "id": "G4_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "paris": {
                "2": 0,
                "1": 0
              },
              "declencheurs": [
                2
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 16,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 18,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "O"
  },
  "G5": {
    "id": "G5",
    "famille": "GARDIEN",
    "couple": [
      "R",
      "O"
    ],
    "origine": "R",
    "nomBase": "Le Coup de Queue de l’Iguane",
    "profils": {
      "A": {
        "nom": "Le Coup de Queue de l’Iguane",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (PIEGE SPECIAL) + DEPLACEMENT (PIEGE)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "PIEGE_SPECIAL",
          "VIGIE",
          "MENACE_AFFICHEE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Posez le <em>Croc</em> sur une parcelle ciblée du rayon Reptile ou du rayon marqué par la Plume de Vigie.<br><strong>Face 2 :</strong> Posez le <em>Croc</em> sur une parcelle ciblée, puis déplacez 1 Piège vers une autre parcelle ciblée.",
        "temoin": "Sur l’icône Piégeage : le Croc pare le Bulldozer au rang 1 et revient en réserve ; l’icône Piégeage réactive l’Iguane, qui repose le Croc devant l’Abatteuse (y compris en Ratissage) ; 2e parade, pari gagné.",
        "alias_oriente": "R>O",
        "id_profil": "R>O·A",
        "alias_profil": "G5-A",
        "animal_ou_theme": "Iguane vert",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (ii) : lisière Animal–Animal R–O"
        ],
        "decision_joueur": {
          "choix": "Quelle parcelle ciblée reçoit l’unique Croc : le rayon Reptile ou celui que l’Oiseau a signalé avec la Plume.",
          "renoncement": "Un seul Croc : le poser ici le retire d’ailleurs ; la Plume engagée pour l’Iguane ne guide plus un autre pari."
        },
        "entrees": [
          "CROC",
          "PLUME"
        ],
        "sorties": [
          "CROC",
          "PIEGE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V3 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.6,
            "Face 2": 2.3
          },
          "composantes": {
            "Face 1": [
              "CROC"
            ],
            "Face 2": [
              "CROC",
              "PIEGE_DEPLACE"
            ]
          },
          "activations_pour_amortir": 1.2
        },
        "declencheurs_amorces": [
          2
        ],
        "double_ouverture": "Câblé sur 2, le Croc revenu en réserve après une parade est reposé à la 2e ouverture.",
        "cablage_recommande": "ICONE_PIEGEAGE",
        "heuristique_bot": "Câbler sur 2 ; poser le Croc devant l’Abatteuse la plus chargée ; Oiseaux : poser la Plume sur le rayon le plus menacé.",
        "temoins": [
          {
            "id": "G5_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                2,
                2
              ],
              "paris_restants": 0
            },
            "journal": [
              "B_R -> p1-R : Croc pare et revient en réserve (2)",
              "A_R -> p3-R : Croc pare et revient en réserve (2)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 19,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 16,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "R"
  },
  "G6": {
    "id": "G6",
    "famille": "GARDIEN",
    "couple": [
      "O",
      "R"
    ],
    "origine": "O",
    "nomBase": "Le Bec du Toucan",
    "profils": {
      "A": {
        "nom": "Le Bec du Toucan",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "MOD_PUISSANCE (SURCHAUFFE GUIDEE PAR LA PLUME)",
        "tags": [
          "SURCHAUFFE",
          "VIGIE",
          "RADIATEUR_THERMIQUE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Sur le rayon marqué par la Plume de Vigie, retournez 1 jeton rouge d’une machine en bleu.<br><strong>Face 2 :</strong> Retournez sur leur face bleue jusqu’à 2 jetons rouges répartis sur une ou deux machines.",
        "temoin": "Plume au pied des Reptiles : le Toucan retourne 1 jeton rouge en bleu sur l’Abatteuse, réduisant son Seuil dès ce tour (−1 en Charge, −2 net en Assaut ou Ratissage).",
        "alias_oriente": "O>R",
        "id_profil": "O>R·A",
        "alias_profil": "G6-A",
        "animal_ou_theme": "Toucan toco",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Poser la Plume sur le rayon d’une machine chargée en rouges pour retourner sa puissance contre elle avant l’Assaut ou le Ratissage.",
          "renoncement": "Sans jeton rouge sur le rayon marqué en Face 1, le Toucan n’a rien à refroidir ; la Plume posée ici ne guide plus un autre allié."
        },
        "entrees": [
          "PLUME",
          "ROUGE"
        ],
        "sorties": [
          "BLEU"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V2",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.2,
            "Face 2": 2.2
          },
          "composantes": {
            "Face 1": [
              "BLEU"
            ],
            "Face 2": [
              "BLEU",
              "BLEU"
            ]
          },
          "activations_pour_amortir": 1.7
        },
        "declencheurs_amorces": [
          1
        ],
        "double_ouverture": "Chaque ouverture retourne 1 nouveau jeton rouge en bleu (jusqu’à 2 par ouverture en Face 2).",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Câbler sur 3 ou 1 ; viser en priorité une machine en Assaut ou en Ratissage portant au moins 1 jeton rouge.",
        "temoins": [
          {
            "id": "G6_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "seuil_avant": 4,
              "seuil_apres": 2,
              "bleus": 1,
              "resultat": [
                "pare"
              ]
            },
            "journal": [
              "Toucan F1 : 1 rouge -> 1 bleu sur A_R ; parade à 2 Défenseurs (1)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 18,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 16,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Consolidation Canon 0 (Greffe 1) : refonte en spécialiste Surchauffe dès Face 1 via la Plume (l’ancien effet Dé d’Envol rejoint le vivier de variantes)."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "O"
  },
  "G7": {
    "id": "G7",
    "famille": "GARDIEN",
    "couple": [
      "M",
      "H"
    ],
    "origine": "M",
    "nomBase": "Le Sentier du Tapir",
    "profils": {
      "A": {
        "nom": "Le Sentier du Tapir",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (PIEGE SUR SOUCHES / PARCELLES ENRACINEES)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "SOUCHES",
          "ENRACINEMENT",
          "JARDINIER"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Posez 1 Piège sur une parcelle ciblée portant au moins 1 Souche.<br><strong>Face 2 :</strong> Posez 1 Piège sur une parcelle ciblée à Souche, et 1 sur chaque parcelle ciblée bordée par une tuile enracinée.",
        "temoin": "p3 des Humains porte 1 Arbre et 2 Souches face au Bulldozer : le Piège du Tapir pare la frappe et sauve les 2 Souches pour la repousse finale.",
        "alias_oriente": "M>H",
        "id_profil": "M>H·A",
        "alias_profil": "G7-A",
        "animal_ou_theme": "Tapir",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien M>H tourné vers {H, E, I}",
          "Synergie d’Enracinement volontaire"
        ],
        "decision_joueur": {
          "choix": "Protéger une parcelle à Souches ciblée (repousse future) plutôt qu’une parcelle encore boisée ; en Face 2, enraciner d’autres tuiles pour multiplier ses Pièges.",
          "renoncement": "Chaque tuile enracinée pour le Tapir perd son pouvoir ; un Piège ne couvre qu’une frappe."
        },
        "entrees": [
          "SOUCHE"
        ],
        "sorties": [
          "PIEGE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_SOUCHE",
          "P_PARI"
        ],
        "vecteurs": "V1 -> V3",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.4,
            "Face 2": 2.8
          },
          "composantes": {
            "Face 1": [
              "PIEGE"
            ],
            "Face 2": [
              "PIEGE",
              "PIEGE"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [
          2
        ],
        "double_ouverture": "Chaque ouverture pose un nouveau Piège sur une autre parcelle ciblée à Souche.",
        "cablage_recommande": "ICONE_PIEGEAGE",
        "heuristique_bot": "Câbler sur 2 ; protéger d’abord la parcelle ciblée par un Bulldozer qui porte des Souches ; enraciner à Face 2 en fin de partie.",
        "temoins": [
          {
            "id": "G7_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "avec_piege": [
                1,
                2,
                false
              ],
              "sans_piege_route": true
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 12,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "M"
  },
  "G8": {
    "id": "G8",
    "famille": "GARDIEN",
    "couple": [
      "M",
      "E"
    ],
    "origine": "M",
    "nomBase": "Le Mirage du Boto",
    "profils": {
      "A": {
        "nom": "Le Mirage du Boto",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "DEPLACEMENT (MACHINE, RECUL)",
        "tags": [
          "RECUL",
          "TERRITOIRE",
          "DEBLOCAGE_PAR_ANCRAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Faites reculer d’1 parcelle une machine mobile qui vise la parcelle du jeton Duel.<br><strong>Face 2 :</strong> Faites reculer d’1 parcelle une machine mobile, ou deux si le jeton Duel est sur <em>Territoire tenu</em>.",
        "temoin": "Abatteuse en p3 visant Devant la parcelle p4 du Défi : le Boto la fait reculer en p2, où elle frappe à blanc une clairière de Souches.",
        "alias_oriente": "M>E",
        "id_profil": "M>E·A",
        "alias_profil": "G8-A",
        "animal_ou_theme": "Boto (Dauphin rose)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Reculer la machine qui menace le Défi (le front tient) ou, en Face 2, la machine la plus proche du Ratissage.",
          "renoncement": "Le recul peut ramener une machine sur une parcelle encore boisée et l’éloigner du Territoire tenu qui la bloquait."
        },
        "entrees": [
          "DUEL"
        ],
        "sorties": [
          "RECUL"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 0.8,
            "Face 2": 1.6
          },
          "composantes": {
            "Face 1": [
              "RECUL"
            ],
            "Face 2": [
              "RECUL",
              "RECUL"
            ]
          },
          "activations_pour_amortir": 2.5
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Chaque ouverture fait reculer une autre machine (ou la même d’un cran de plus).",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Reculer en priorité une Abatteuse à 1 avancée du Ratissage ou une machine dont le recul l’envoie sur une clairière.",
        "temoins": [
          {
            "id": "G8_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "cible_avant": "p4",
              "p4-M": 3,
              "p3-M": [
                0,
                3
              ]
            },
            "journal": [
              "A_M -> p3-M : non parée, Seuil 3 -> 0 Arbre(s), 3 Souche(s)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 15,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 18,
            "phrases": 1,
            "conditions": 1
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "M"
  },
  "G9": {
    "id": "G9",
    "famille": "GARDIEN",
    "couple": [
      "R",
      "H"
    ],
    "origine": "R",
    "nomBase": "Le Guet du Caïman noir",
    "profils": {
      "A": {
        "nom": "Le Guet du Caïman noir",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (SABOTAGE EN CALE)",
        "tags": [
          "TWIST",
          "SABOTAGE_CALE",
          "VERROU_D_AVANCEE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Glissez sous une machine mobile 1 jeton Sabotage de la réserve, qui annule sa prochaine avancée puis rejoint le sac.<br><strong>Face 2 :</strong> Glissez sous une machine mobile 1 jeton <em>Écaille</em> de la réserve, qui annule sa prochaine avancée puis rejoint le sac.",
        "temoin": "Abatteuse en p3 calée, révélée au rang 3 (En avançant) : elle frappe mais n’avance pas, et le jeton Sabotage glissé dessous rejoint immédiatement le sac.",
        "alias_oriente": "R>H",
        "id_profil": "R>H·A",
        "alias_profil": "G9-A",
        "animal_ou_theme": "Caïman noir",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A #10 — Le Sabotage sert de cale",
        "role_porte": [],
        "decision_joueur": {
          "choix": "Caler une machine (verrou local de sa prochaine avancée) ou laisser le jeton diluer le sac tout de suite.",
          "renoncement": "Tant qu’il cale, le jeton échappe au retour au sac et ne le dilue pas."
        },
        "entrees": [
          "SABOTAGE"
        ],
        "sorties": [
          "CALE",
          "SABOTAGE",
          "ECAILLE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V3 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.6,
            "Face 2": 2.0
          },
          "composantes": {
            "Face 1": [
              "CALE",
              "SABOTAGE"
            ],
            "Face 2": [
              "CALE",
              "ECAILLE"
            ]
          },
          "activations_pour_amortir": 1.2
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Deux ouvertures calent deux machines (ou deux avancées de la même).",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Caler l’Abatteuse à 1 avancée du Ratissage ; en Face 2 préférer l’Écaille (elle reposera le Croc).",
        "temoins": [
          {
            "id": "G9_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "position": "p3",
              "cale_restante": 0,
              "sabotages_pour_6.3": 1
            },
            "journal": [
              "A_R -> p3-R : non parée, Seuil 2 -> 0 Arbre(s), 3 Souche(s)",
              "A_R -> p4-R : non parée, Seuil 2 -> 0 Arbre(s), 3 Souche(s)",
              "A_R : avancée absorbée par la cale (sabotage)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "R"
  },
  "G10": {
    "id": "G10",
    "famille": "GARDIEN",
    "couple": [
      "R",
      "E"
    ],
    "origine": "R",
    "nomBase": "L’Affût de la Matamata",
    "profils": {
      "A": {
        "nom": "L’Affût de la Matamata",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (ECAILLE) + ALTERATION_MACHINE",
        "tags": [
          "CATALYSEUR_EVEIL",
          "ECAILLE",
          "ENTROPIE",
          "ALTERATION"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Ajoutez 1 jeton <em>Écaille</em> de la réserve Reptile au sac.<br><strong>Face 2 :</strong> Ajoutez 1 jeton <em>Écaille</em> au sac, puis altérez une machine mobile révélée.",
        "temoin": "Au tour suivant, l’Écaille tirée du sac allume l’icône Sabotage à l’ouverture et pose le Croc sur une parcelle ciblée.",
        "alias_oriente": "R>E",
        "id_profil": "R>E·A",
        "alias_profil": "G10-A",
        "animal_ou_theme": "Matamata",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien R>E tourné vers {H, E, I}"
        ],
        "decision_joueur": {
          "choix": "Encrasser le sac d’Écailles camouflées (chaque révélation future allume 3. Sabotage et pose le Croc) tant que la réserve en contient.",
          "renoncement": "Réserve de 4 Écailles : une injection précoce épuise la réserve ; l’altération de Face 2 détourne une machine choisie par les Reptiles, pas par les Entités."
        },
        "entrees": [
          "ECAILLE"
        ],
        "sorties": [
          "ECAILLE",
          "ALTEREE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V3 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.1,
            "Face 2": 2.4
          },
          "composantes": {
            "Face 1": [
              "ECAILLE"
            ],
            "Face 2": [
              "ECAILLE",
              "ALTEREE"
            ]
          },
          "activations_pour_amortir": 1.8
        },
        "declencheurs_amorces": [
          3
        ],
        "double_ouverture": "Chaque ouverture ajoute une Écaille tant que la réserve en contient.",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Câbler sur 3 ; injecter tôt (Acte 1) ; en Face 2, altérer une Abatteuse proche du Ratissage.",
        "temoins": [
          {
            "id": "G10_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                3,
                2
              ],
              "p2-E": 2,
              "croc_revenu": true
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 10,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 12,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "R"
  },
  "G11": {
    "id": "G11",
    "famille": "GARDIEN",
    "couple": [
      "O",
      "H"
    ],
    "origine": "O",
    "nomBase": "Le Piqué de la Harpie",
    "profils": {
      "A": {
        "nom": "Le Piqué de la Harpie",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (PIEGE GUIDE PAR LA PLUME)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "VIGIE",
          "PIEGE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Posez 1 Piège sur une parcelle ciblée du rayon marqué par la Plume de Vigie.<br><strong>Face 2 :</strong> Posez 1 Piège sur une parcelle ciblée de n’importe quel rayon, puis déplacez la Plume de Vigie.",
        "temoin": "Plume au pied des Humains : la Harpie pose 1 Piège sur p2-H ciblée, qui pare seul la frappe et allume l’icône Piégeage.",
        "alias_oriente": "O>H",
        "id_profil": "O>H·A",
        "alias_profil": "G11-A",
        "animal_ou_theme": "Harpie féroce",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien O>H tourné vers {H, E, I}"
        ],
        "decision_joueur": {
          "choix": "Où poser la Plume en 2.1/2.2, sous paravents fermés, en sachant que la Harpie y piquera après la révélation.",
          "renoncement": "La Plume engagée pour la Harpie ne signale plus le pari Chaud ou Calme d’un autre rayon."
        },
        "entrees": [
          "PLUME"
        ],
        "sorties": [
          "PIEGE",
          "PLUME"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V3 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.4,
            "Face 2": 1.7
          },
          "composantes": {
            "Face 1": [
              "PIEGE"
            ],
            "Face 2": [
              "PIEGE",
              "PLUME_DEPLACEE"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [
          2
        ],
        "double_ouverture": "Deux ouvertures posent deux Pièges sur le rayon guetté.",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Câbler sur 3 (ouverture en 3.2, avant les frappes) ; Plume sur le rayon le plus boisé.",
        "temoins": [
          {
            "id": "G11_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                2
              ],
              "p2-H": 2
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 15,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 18,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "O"
  },
  "G12": {
    "id": "G12",
    "famille": "GARDIEN",
    "couple": [
      "O",
      "E"
    ],
    "origine": "O",
    "nomBase": "Le Chant de l’Ibijau",
    "profils": {
      "A": {
        "nom": "Le Chant de l’Ibijau",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "PERMUTATION_PISTE (REVE)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "LEVIER_REVE",
          "SOMMEIL",
          "HYPNOSE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Faites glisser un Rêve d’1 rang vers la gauche.<br><strong>Face 2 :</strong> Faites glisser un Rêve de 2 rangs vers la gauche.",
        "temoin": "Sur l’icône Sabotage : un Sabotage révélé active l’Ibijau avant les Rêves ; le Rêve défendu du rang 4 glisse avec son Défenseur au rang 3, annule la machine et allume l’icône Rêve.",
        "alias_oriente": "O>E",
        "id_profil": "O>E·A",
        "alias_profil": "G12-A",
        "animal_ou_theme": "Ibijau (Oiseau fantôme)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien O>E tourné vers {H, E, I}",
          "Levier de mouvement de Rêve — lisière E–O (C07)"
        ],
        "decision_joueur": {
          "choix": "Quel Rêve hypnotiser : celui qui passera sous une machine révélée (annulation, 5. Rêve) ou celui qui comble le bloc du Sommeil.",
          "renoncement": "Le glissement pousse les Rêves contigus et peut retirer un Rêve de la case où il bloquait."
        },
        "entrees": [
          "POSITION_REVE"
        ],
        "sorties": [
          "RANG_REVE",
          "ANNULATION"
        ],
        "paiement": [
          "P_RANG",
          "P_PARI"
        ],
        "vecteurs": "V5 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.8,
            "Face 2": 2.4
          },
          "composantes": {
            "Face 1": [
              "RANG_REVE",
              "ANNULATION"
            ],
            "Face 2": [
              "RANG_REVE",
              "RANG_REVE",
              "ANNULATION"
            ]
          },
          "activations_pour_amortir": 1.1
        },
        "declencheurs_amorces": [
          5
        ],
        "double_ouverture": "Chaque ouverture fait glisser un Rêve de plus.",
        "cablage_recommande": "ICONE_SABOTAGE",
        "heuristique_bot": "Câbler sur 3 ; glisser le Rêve défendu sous la machine révélée la plus dangereuse, sinon vers le bloc 1..2D.",
        "temoins": [
          {
            "id": "G12_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "reglette": {
                "6": "R2",
                "3": "R7"
              },
              "annulee": true,
              "declencheurs": [
                3,
                5
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 10,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 10,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "O"
  },
  "G13": {
    "id": "G13",
    "famille": "GARDIEN",
    "couple": [
      "M",
      "I"
    ],
    "origine": "M",
    "nomBase": "La Langue du Tamanoir",
    "profils": {
      "A": {
        "nom": "La Langue du Tamanoir",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "DEPLACEMENT (INSECTES -> PARCELLE CIBLEE)",
        "tags": [
          "CATALYSEUR_EVEIL",
          "INSECTES",
          "PARADE_INSECTE",
          "TERRITOIRE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Déplacez jusqu’à 2 Insectes d’un même rayon vers une parcelle ciblée de ce rayon.<br><strong>Face 2 :</strong> Déplacez jusqu’à 2 Insectes vers une parcelle ciblée, puis posez-y le jeton Duel face <em>Défi</em>.",
        "temoin": "2 Insectes en p1-I rejoignent 1 Défenseur en p3-I (Seuil 3) : parade réussie avec dépense des 2 Insectes, allumant l’icône Insecte.",
        "alias_oriente": "M>I",
        "id_profil": "M>I·A",
        "alias_profil": "G13-A",
        "animal_ou_theme": "Tamanoir",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien M>I tourné vers {H, E, I}"
        ],
        "decision_joueur": {
          "choix": "Prélever des Insectes sur un Nid (au risque de casser sa masse critique) ou sur une parcelle calme pour les jeter sur la parcelle ciblée.",
          "renoncement": "Un Insecte défaussé en Parade ne migrera plus vers la Réglette ni la Piste des Gardiens."
        },
        "entrees": [
          "INSECTE"
        ],
        "sorties": [
          "INSECTE",
          "DUEL"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V4 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.0,
            "Face 2": 1.7
          },
          "composantes": {
            "Face 1": [
              "INSECTE",
              "INSECTE"
            ],
            "Face 2": [
              "INSECTE",
              "INSECTE",
              "TERRITOIRE_BONUS"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [
          6
        ],
        "double_ouverture": "Chaque ouverture amène jusqu’à 2 nouveaux Insectes.",
        "cablage_recommande": "ICONE_INSECTE",
        "heuristique_bot": "Câbler sur 6 ou 1 ; prendre les Insectes hors Nid sauf si le Nid en porte au moins 4.",
        "temoins": [
          {
            "id": "G13_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                6
              ],
              "p3-I": [
                3,
                0
              ]
            },
            "journal": [
              "A_I -> p3-I : parade 1 Déf. + 2 Insecte(s), Seuil 3 (6)"
            ]
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 16,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 17,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "M"
  },
  "G14": {
    "id": "G14",
    "famille": "GARDIEN",
    "couple": [
      "R",
      "I"
    ],
    "origine": "R",
    "nomBase": "Le Terrier du Téju",
    "profils": {
      "A": {
        "nom": "Le Terrier du Téju",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "CREATION_ENTITE (PIEGE) avec coût Insecte",
        "tags": [
          "CATALYSEUR_EVEIL",
          "CONVERSION",
          "INSECTES",
          "PIEGE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Défaussez 1 Insecte d’une parcelle pour poser 1 Piège sur cette parcelle ou une parcelle voisine de son rayon.<br><strong>Face 2 :</strong> Défaussez 1 Insecte pour poser 1 Piège, ou le <em>Croc</em>, sur n’importe quelle parcelle ciblée.",
        "temoin": "À l’ouverture, le Téju prélève 1 des 2 Insectes d’un Nid pour piéger la parcelle voisine menacée : le Piège pare seul (icône Piégeage), mais le Nid ne produit plus que +1.",
        "alias_oriente": "R>I",
        "id_profil": "R>I·A",
        "alias_profil": "G14-A",
        "animal_ou_theme": "Téju",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Catalyseur d’Éveil — règle (i) : Gardien R>I tourné vers {H, E, I}"
        ],
        "decision_joueur": {
          "choix": "Dépenser un Insecte maintenant pour couvrir une parcelle menacée avant l’attaque, même s’il faut le prélever sur un Nid avant sa production.",
          "renoncement": "Prélevé sur un Nid à 2 Insectes, l’Insecte fait passer sa production de +2 à +1 ; attendre préserve le rendement mais laisse passer la frappe."
        },
        "entrees": [
          "INSECTE"
        ],
        "sorties": [
          "PIEGE",
          "CROC"
        ],
        "paiement": [
          "P_ARBRE",
          "P_PARI"
        ],
        "vecteurs": "V4 -> V3",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 1.4,
            "Face 2": 1.6
          },
          "composantes": {
            "Face 1": [
              "PIEGE"
            ],
            "Face 2": [
              "CROC"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [
          2
        ],
        "double_ouverture": "Chaque ouverture convertit un nouvel Insecte en Piège.",
        "cablage_recommande": "ICONE_PIEGEAGE",
        "heuristique_bot": "Câbler sur 2 ; prélever hors Nid si possible, sinon sur un Nid à 3 Insectes ou plus ; viser la parcelle ciblée la plus boisée.",
        "temoins": [
          {
            "id": "G14_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "production_4.2": 1,
              "declencheurs": [
                2
              ],
              "p3-R": 3,
              "insectes_nid": 2
            },
            "journal": []
          },
          {
            "id": "G14_T2",
            "statut": "OK",
            "etat_attendu_verifie": {
              "production_4.2_si_attente": 2,
              "p3-R_sans_piege": [
                0,
                3
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 16,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "R"
  },
  "G15": {
    "id": "G15",
    "famille": "GARDIEN",
    "couple": [
      "O",
      "I"
    ],
    "origine": "O",
    "nomBase": "Le Va-et-vient du Colibri",
    "profils": {
      "A": {
        "nom": "Le Va-et-vient du Colibri",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "ACTIVATION",
        "primitive": "PERMUTATION_PISTE (ECHANGE DE RANGS — TORSION DE FILE)",
        "tags": [
          "TWIST",
          "TORSION_DE_FILE",
          "FRONTIERE_DES_ACTES"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Échangez les rangs de deux machines révélées qui n’ont pas encore frappé.<br><strong>Face 2 :</strong> Échangez deux fois les rangs de deux machines révélées qui n’ont pas encore frappé.",
        "temoin": "Acte 2 : l’Abatteuse au rang 3 (Assaut, En avançant) et le Bulldozer au rang 5 (Charge, Devant) échangent leurs rangs avant de frapper.",
        "alias_oriente": "O>I",
        "id_profil": "O>I·A",
        "alias_profil": "G15-A",
        "animal_ou_theme": "Colibri",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A / §5.3 #3 — Torsion d’une file engagée",
        "role_porte": [],
        "decision_joueur": {
          "choix": "Quelles deux machines intervertir : un Assaut contre une Charge, une avancée contre un Sur place, ou jeter une machine sur un Rêve défendu.",
          "renoncement": "L’échange déplace aussi l’autre machine : chaque permutation est un pari à double tranchant."
        },
        "entrees": [],
        "sorties": [
          "RANG_MACHINE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V2 -> V2",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face 1": 0.9,
            "Face 2": 1.8
          },
          "composantes": {
            "Face 1": [
              "RANG_MACHINE"
            ],
            "Face 2": [
              "RANG_MACHINE",
              "RANG_MACHINE"
            ]
          },
          "activations_pour_amortir": 2.2
        },
        "declencheurs_amorces": [],
        "double_ouverture": "Chaque ouverture permet un nouvel échange avant les frappes restantes.",
        "cablage_recommande": "ICONE_PARADE",
        "heuristique_bot": "Câbler sur 1 (ouverture en 5.1) ; échanger la machine en Assaut la plus chargée contre une machine en Charge peu dangereuse.",
        "temoins": [
          {
            "id": "G15_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "Abatteuse_avant": [
                "Assaut",
                "En avançant"
              ],
              "Abatteuse_apres": [
                "Charge",
                "Devant"
              ],
              "a_avance": false
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face 1": {
            "mots": 13,
            "phrases": 1,
            "conditions": 0
          },
          "Face 2": {
            "mots": 15,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "O"
  },
  "R1": {
    "id": "R1",
    "famille": "REVE",
    "couple": [
      "H",
      "E"
    ],
    "origine": "H",
    "nomBase": "Le Seuil des Deux Mondes",
    "profils": {
      "A": {
        "nom": "Le Seuil des Deux Mondes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "MOD_REVE (ANNULATION SUR CASE VIDE VOISINE)",
        "tags": [
          "TWIST",
          "PLACE_LIBRE",
          "REVE",
          "A0"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, chaque Défenseur de ce Rêve peut annuler une machine visant un rang voisin sans Rêve plutôt qu’une machine de son rang.",
        "temoin": "R1 défendu au rang 4, rang 3 sans Rêve visé par une Abatteuse : le Défenseur l’annule à distance et allume l’icône Rêve.",
        "alias_oriente": "H>E",
        "id_profil": "H>E·A",
        "alias_profil": "R1-A",
        "animal_ou_theme": "Rêve des Humains",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A #12 — La place libre a un pouvoir",
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste"
        ],
        "decision_joueur": {
          "choix": "Laisser une case vide à côté de ce Rêve pour étendre sa protection aux machines qui y tombent.",
          "renoncement": "Une case vide est un trou dans le bloc : tant qu’elle reste ouverte, le Sommeil est impossible."
        },
        "entrees": [
          "POSITION_REVE"
        ],
        "sorties": [
          "ANNULATION"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.2
          },
          "composantes": {
            "Face unique": [
              "ANNULATION"
            ]
          },
          "activations_pour_amortir": 1.7
        },
        "declencheurs_amorces": [
          5
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre quand une case vide voisine est probable (1–3) ; refermer le trou au plus tard 2 tours avant un Sommeil visé.",
        "temoins": [
          {
            "id": "R1_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "case_3_vide": true,
              "annulee": true,
              "declencheurs": [
                5
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 25,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "H"
  },
  "R2": {
    "id": "R2",
    "famille": "REVE",
    "couple": [
      "E",
      "H"
    ],
    "origine": "E",
    "nomBase": "Le Voile de l’Oubli",
    "profils": {
      "A": {
        "nom": "Le Voile de l’Oubli",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE / ENRACINEMENT",
        "primitive": "ALTERATION_MACHINE (SUR ANNULATION)",
        "tags": [
          "ALTERATION",
          "ENRACINEMENT",
          "COUP_D_ECLAT",
          "A0"
        ],
        "requires_options": {},
        "texte": "Quand ce Rêve annule une machine, altérez-la.<br><strong>Enraciné :</strong> Lors de son enracinement, altérez jusqu’à 2 machines mobiles.",
        "temoin": "R2 annule le Bulldozer des Humains et pose 1 jeton d’Altération dessus : à sa prochaine révélation, ce Bulldozer reculera d’1 parcelle sans frapper.",
        "alias_oriente": "E>H",
        "id_profil": "E>H·A",
        "alias_profil": "R2-A",
        "animal_ou_theme": "Rêve des Entités",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste",
          "Synergie d’Enracinement volontaire"
        ],
        "decision_joueur": {
          "choix": "Défendre ce Rêve pour muter la machine qu’il annule ; ou l’enraciner (coup d’éclat : 2 altérations) en renonçant au Sommeil.",
          "renoncement": "Enraciner un Rêve rend le Sommeil impossible ; défendu sur une case peu visée, il n’annule rien."
        },
        "entrees": [
          "ANNULATION",
          "ALTEREE"
        ],
        "sorties": [
          "ALTEREE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_SOUCHE"
        ],
        "vecteurs": "V3 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.3,
            "Enraciné": 3.8
          },
          "composantes": {
            "Face unique": [
              "ALTEREE"
            ],
            "Enraciné": [
              "ALTEREE",
              "ALTEREE",
              "SOUCHE_REGEN"
            ]
          },
          "activations_pour_amortir": 1.5
        },
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre quand il recouvre une case 1–3 ; l’enraciner au Tour 6 ou 7 si le Sommeil est hors d’atteinte.",
        "temoins": [
          {
            "id": "R2_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "alteree_dans_paquet": [
                "B_H"
              ],
              "revelation": [
                "alteree"
              ],
              "recul_vers": "p1"
            },
            "journal": []
          },
          {
            "id": "R2_T2",
            "statut": "OK",
            "etat_attendu_verifie": {
              "alterations": [
                "A_H",
                "B_E"
              ],
              "p3-E_final": [
                2,
                1
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 8,
            "phrases": 1,
            "conditions": 1
          },
          "Enraciné": {
            "mots": 10,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "E"
  },
  "R3": {
    "id": "R3",
    "famille": "REVE",
    "couple": [
      "H",
      "M"
    ],
    "origine": "H",
    "nomBase": "La Danse des Esprits-Fauves",
    "profils": {
      "A": {
        "nom": "La Danse des Esprits-Fauves",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (DEFENSEUR DU REVE -> JETON DUEL)",
        "tags": [
          "MULTIFONCTION",
          "TERRITOIRE",
          "SOUTIEN_ALLIE"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, après ses annulations, 1 Défenseur de ce Rêve rejoint la parcelle du jeton Duel.",
        "temoin": "Le Chant annule la machine du rang 5 (R3 glisse au rang 4), puis rejoint la parcelle du Défi pour réussir la parade et passer en Territoire tenu.",
        "alias_oriente": "H>M",
        "id_profil": "H>M·A",
        "alias_profil": "R3-A",
        "animal_ou_theme": "Rêve des Humains",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Poser un Défenseur sur ce Rêve plutôt qu’en forêt : il bloque d’abord une machine de son rang, puis renforce le Défi des Mammifères.",
          "renoncement": "Il ne peut rejoindre que la parcelle du jeton Duel, même si une autre parcelle est plus menacée."
        },
        "entrees": [
          "DUEL",
          "POSITION_REVE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "TERRITOIRE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.7
          },
          "composantes": {
            "Face unique": [
              "DEFENSEUR_REDEPLOYE",
              "TERRITOIRE_BONUS"
            ]
          },
          "activations_pour_amortir": 1.2
        },
        "declencheurs_amorces": [
          1
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre avec le Chant si une machine vise son rang ; sinon avec le Défenseur fixe d’un allié qui vise le Duel.",
        "temoins": [
          {
            "id": "R3_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "reglette": {
                "4": "R3"
              },
              "duel": "territoire",
              "declencheurs": [
                5,
                1
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 17,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "H"
  },
  "R4": {
    "id": "R4",
    "famille": "REVE",
    "couple": [
      "H",
      "R"
    ],
    "origine": "H",
    "nomBase": "Le Sommeil de la Pierre-Serpent",
    "profils": {
      "A": {
        "nom": "Le Sommeil de la Pierre-Serpent",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (DEFENSEUR DU REVE -> RIVE PIEGE)",
        "tags": [
          "MULTIFONCTION",
          "FURTIVITE_CHAUD",
          "PIEGE"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, 1 Défenseur de ce Rêve peut compléter la Rive Piège d’un rayon comptant 2 machines mobilisées.",
        "temoin": "2 machines mobilisées chez les Reptiles (lues sur les jetons visibles devant le rayon) et 1 allié déjà en Rive Piège : le pion de R4 complète le binôme avant l’évaluation de Furtivité.",
        "alias_oriente": "H>R",
        "id_profil": "H>R·A",
        "alias_profil": "R4-A",
        "animal_ou_theme": "Rêve des Humains",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Défendre ce Rêve en gardant l’option de compléter, une fois m(r) connu, une Rive Piège qu’un allié a amorcée à l’aveugle.",
          "renoncement": "Sans premier Défenseur déjà posé sur cette rive, l’option est perdue et le Défenseur reste sur le Rêve."
        },
        "entrees": [
          "MOBILISATION",
          "POSITION_REVE"
        ],
        "sorties": [
          "PIEGE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V3",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.4
          },
          "composantes": {
            "Face unique": [
              "PIEGE"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre si une rive Piège est amorcée ; compléter la rive du rayon à m(r)=2 le plus boisé.",
        "temoins": [
          {
            "id": "R4_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "m(r)": 2,
              "binome": [
                "allié",
                "Défenseur du Rêve"
              ],
              "piege_pose": true
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "H"
  },
  "R5": {
    "id": "R5",
    "famille": "REVE",
    "couple": [
      "H",
      "O"
    ],
    "origine": "H",
    "nomBase": "La Vision des Plumes Claires",
    "profils": {
      "A": {
        "nom": "La Vision des Plumes Claires",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (DEFENSEUR DU REVE -> RAYON DE LA PLUME)",
        "tags": [
          "MULTIFONCTION",
          "VIGIE",
          "SIGNAL_MUET"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, 1 Défenseur de ce Rêve, ou 2 avec le Tambour, rejoint une parcelle ciblée du rayon de la Plume de Vigie.",
        "temoin": "Plume au pied des Oiseaux : après l’ouverture, le Défenseur de R5 descend défendre p3-O ciblée.",
        "alias_oriente": "H>O",
        "id_profil": "H>O·A",
        "alias_profil": "R5-A",
        "animal_ou_theme": "Rêve des Humains",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "Défendre ce Rêve en se fiant au signal muet de l’Oiseau : après la révélation, le Défenseur suit la Plume ; avec le Tambour, deux Défenseurs suivent.",
          "renoncement": "Seul le rayon de la Plume est accessible ; un signal mal placé rend ce Défenseur inutile en forêt."
        },
        "entrees": [
          "PLUME",
          "POSITION_REVE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.5
          },
          "composantes": {
            "Face unique": [
              "DEFENSEUR_REDEPLOYE",
              "TAMBOUR_BONUS"
            ]
          },
          "activations_pour_amortir": 1.3
        },
        "declencheurs_amorces": [
          1
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Oiseaux : poser la Plume sur le rayon le plus menacé ; Humains : défendre ce Rêve avec le Défenseur fixe.",
        "temoins": [
          {
            "id": "R5_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "resultat": [
                "pare"
              ],
              "p3-O": 3
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 24,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "H"
  },
  "R6": {
    "id": "R6",
    "famille": "REVE",
    "couple": [
      "H",
      "I"
    ],
    "origine": "H",
    "nomBase": "Le Miel des Ancêtres",
    "profils": {
      "A": {
        "nom": "Le Miel des Ancêtres",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE / DÉCOMPTE FINAL",
        "primitive": "DEPLACEMENT (DEFENSEUR DU REVE -> NID) + REPOUSSE ETENDUE",
        "tags": [
          "MULTIFONCTION",
          "NID",
          "ENRACINEMENT",
          "REPOUSSE_FINALE",
          "A0"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, 1 Défenseur de ce Rêve rejoint la parcelle d’un Nid pour activer sa production.<br><strong>Enraciné :</strong> Au décompte final, retournez aussi 1 Souche d’une parcelle voisine en Arbre debout.",
        "temoin": "Enraciné face à p3-H (2 Souches) voisine de p2-H (1 Souche) : au décompte final, il retourne 1 Souche sur p3-H et 1 Souche sur p2-H.",
        "alias_oriente": "H>I",
        "id_profil": "H>I·A",
        "alias_profil": "R6-A",
        "animal_ou_theme": "Rêve des Humains",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste",
          "Synergie d’Enracinement volontaire"
        ],
        "decision_joueur": {
          "choix": "Défendre ce Rêve pour activer un Nid à distance après la révélation ; ou l’enraciner pour une repousse sur deux parcelles.",
          "renoncement": "Enraciné, il n’active plus les Nids et le Sommeil devient impossible."
        },
        "entrees": [
          "NID",
          "POSITION_REVE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "NID_ACTIVE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_SOUCHE"
        ],
        "vecteurs": "V5 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.5,
            "Enraciné": 2.4
          },
          "composantes": {
            "Face unique": [
              "DEFENSEUR_REDEPLOYE",
              "INSECTE"
            ],
            "Enraciné": [
              "SOUCHE_REGEN",
              "SOUCHE_REGEN"
            ]
          },
          "activations_pour_amortir": 1.3
        },
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre si un Nid sans Défenseur est sur une parcelle non ciblée ; enraciner face à la parcelle la plus riche en Souches au Tour 7.",
        "temoins": [
          {
            "id": "R6_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "p3-H": [
                2,
                1
              ],
              "p2-H": [
                2,
                0
              ]
            },
            "journal": []
          },
          {
            "id": "R6_T2",
            "statut": "OK",
            "etat_attendu_verifie": {
              "production_4.2": 1
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 18,
            "phrases": 1,
            "conditions": 0
          },
          "Enraciné": {
            "mots": 14,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "H"
  },
  "R7": {
    "id": "R7",
    "famille": "REVE",
    "couple": [
      "E",
      "M"
    ],
    "origine": "E",
    "nomBase": "L’Ombre du Maître des Bois",
    "profils": {
      "A": {
        "nom": "L’Ombre du Maître des Bois",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "PERMUTATION_PISTE (REVE, AVANCEE AU CALME)",
        "tags": [
          "LEVIER_REVE",
          "SOMMEIL",
          "SCULPTURE_REGLETTE"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, si ce Rêve défendu n’annule aucune machine, faites-le glisser d’1 rang vers la gauche.",
        "temoin": "R7 défendu au rang 6 sans machine sur 6 : il glisse au rang 5 avec son Défenseur en poussant un Rêve contigu du rang 5 au rang 4.",
        "alias_oriente": "E>M",
        "id_profil": "E>M·A",
        "alias_profil": "R7-A",
        "animal_ou_theme": "Rêve des Entités",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Levier de mouvement de Rêve — lisière E–M (C07)"
        ],
        "decision_joueur": {
          "choix": "Défendre ce Rêve sur une case peu visée pour qu’il avance, ou le laisser bloquer une machine de son rang.",
          "renoncement": "S’il annule une machine, il n’avance pas ce tour ; un Défenseur posé là ne protège pas la forêt."
        },
        "entrees": [
          "POSITION_REVE"
        ],
        "sorties": [
          "RANG_REVE"
        ],
        "paiement": [
          "P_RANG"
        ],
        "vecteurs": "V5 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 0.6
          },
          "composantes": {
            "Face unique": [
              "RANG_REVE"
            ]
          },
          "activations_pour_amortir": 3.3
        },
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Défendre au tour où son rang est peu probable (5–6) ; arrêter dès que le bloc 1..2D est atteint.",
        "temoins": [
          {
            "id": "R7_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "reglette": {
                "4": "R1",
                "5": "R7"
              }
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 20,
            "phrases": 1,
            "conditions": 1
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "E"
  },
  "R8": {
    "id": "R8",
    "famille": "REVE",
    "couple": [
      "E",
      "R"
    ],
    "origine": "E",
    "nomBase": "Le Mirage du Fleuve-Miroir",
    "profils": {
      "A": {
        "nom": "Le Mirage du Fleuve-Miroir",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "PERMUTATION_PISTE (REVE CONTRE SOUCHE)",
        "tags": [
          "TWIST",
          "MONNAIE_SOUCHE",
          "LEVIER_REVE",
          "SOMMEIL"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, ce Rêve défendu peut retirer 1 Souche sans vider sa parcelle pour glisser un Rêve d’1 ou 2 rangs à gauche.",
        "temoin": "Sur {E, R, I}, R8 défendu au rang 5 retire définitivement 1 des 2 Souches de p2-R et glisse lui-même au rang 3 vers le Sommeil.",
        "alias_oriente": "E>R",
        "id_profil": "E>R·A",
        "alias_profil": "R8-A",
        "animal_ou_theme": "Rêve des Entités",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A #11 — La dernière Souche comme monnaie",
        "role_porte": [
          "Levier de mouvement de Rêve — lisière E–R (C07)"
        ],
        "decision_joueur": {
          "choix": "Sacrifier 1 Souche en forêt pour propulser n’importe quel Rêve (y compris celui-ci) de 1 ou 2 cases vers le bloc du Sommeil.",
          "renoncement": "La Souche retirée ne pourra plus être régénérée à l’Enracinement et éteint les synergies de Souches si c’était la seule d’une parcelle boisée."
        },
        "entrees": [
          "SOUCHE",
          "POSITION_REVE"
        ],
        "sorties": [
          "RANG_REVE"
        ],
        "paiement": [
          "P_RANG"
        ],
        "vecteurs": "V1 -> V5",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.5
          },
          "composantes": {
            "Face unique": [
              "RANG_REVE",
              "RANG_REVE"
            ]
          },
          "activations_pour_amortir": 1.3
        },
        "declencheurs_amorces": [
          5
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Prélever 1 Souche sur une parcelle qui en compte au moins 2 (hors parcelle enracinée) pour regrouper tous les Rêves sur 1..2D.",
        "temoins": [
          {
            "id": "R8_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "souches_p2R_avant": 2,
              "souches_p2R_apres": 1,
              "reglette": {
                "3": "R8"
              }
            },
            "journal": [
              "R8 3.2 : -1 Souche sur p2-R (reste 1) -> R8 glisse de 5 en 3"
            ]
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 25,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Consolidation Canon 0 (Greffe 3) : remplacement du piston bloquant sur N3-ERI par le Twist #11 (Souche sacrifiée), débloquant le Sommeil sur 100 % des tables E sans H ; le piston rejoint le vivier Humains."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "E"
  },
  "R9": {
    "id": "R9",
    "famille": "REVE",
    "couple": [
      "E",
      "O"
    ],
    "origine": "E",
    "nomBase": "L’Écho des Voix Célestes",
    "profils": {
      "A": {
        "nom": "L’Écho des Voix Célestes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "ALTERATION_MACHINE (JETON DU PERCHOIR) + CREATION_ENTITE (PIEGE)",
        "tags": [
          "ALTERATION",
          "PERCHOIR",
          "PIEGE",
          "SIGNAL_SECRET"
        ],
        "requires_options": {},
        "texte": "À l’ouverture, si le Perchoir de Vigie cache un jeton Machine, altérez sa machine et posez 1 Piège sur son rayon.",
        "temoin": "L’Oiseau a posé le jeton de l’Abatteuse Reptile face cachée sur son Perchoir : R9 pose 1 jeton d’Altération sur cette Abatteuse et 1 Piège sur le rayon Reptile.",
        "alias_oriente": "E>O",
        "id_profil": "E>O·A",
        "alias_profil": "R9-A",
        "animal_ou_theme": "Rêve des Entités",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [],
        "decision_joueur": {
          "choix": "L’Oiseau choisit en 1.1 quel jeton Machine poser sur son Perchoir pour désigner son rayon ; les Entités défendent R9 pour altérer ce jeton Machine et piéger ce rayon.",
          "renoncement": "Révèle à la table l’identité du jeton posé sur le Perchoir ; sans effet si l’Oiseau y a posé un jeton Sabotage."
        },
        "entrees": [
          "PERCHOIR",
          "ALTEREE",
          "POSITION_REVE"
        ],
        "sorties": [
          "ALTEREE",
          "PIEGE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V5 -> V3",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.9
          },
          "composantes": {
            "Face unique": [
              "ALTEREE",
              "PIEGE"
            ]
          },
          "activations_pour_amortir": 1.1
        },
        "declencheurs_amorces": [
          2
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Oiseaux : poser sur le Perchoir un jeton Machine d’un rayon menacé ; Entités : défendre R9 pour altérer la machine et poser le Piège.",
        "temoins": [
          {
            "id": "R9_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "alterees_pour_6.3": [
                "A_O"
              ],
              "piege_pose": "p2-O",
              "declencheurs_potentiels": [
                2
              ]
            },
            "journal": [
              "R9 3.2 : A_O sous Perchoir -> altérée + 1 Piège posé sur rayon O"
            ]
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 22,
            "phrases": 1,
            "conditions": 1
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Consolidation Canon 0 (Greffe 2) : couplage de l’altération sous Perchoir avec 1 Piège sur ce rayon, ramenant l’isolement de R9 de 48 % à 0 %."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "E"
  },
  "R10": {
    "id": "R10",
    "famille": "REVE",
    "couple": [
      "E",
      "I"
    ],
    "origine": "E",
    "nomBase": "La Nuée des Songes",
    "profils": {
      "A": {
        "nom": "La Nuée des Songes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "OUVERTURE",
        "primitive": "ALTERATION_MACHINE + CREATION_ENTITE (INSECTE SUR NID OU REGLETTE)",
        "tags": [
          "ALTERATION",
          "INSECTES",
          "DEVIATION",
          "MASSE_CRITIQUE",
          "A0"
        ],
        "requires_options": {},
        "texte": "Quand ce Rêve annule une machine, altérez-la et posez 1 Insecte sur un Nid ou sur ce rang.",
        "temoin": "R10 annule une machine (même déviée vers lui par un Insecte), pose 1 jeton d’Altération dessus, pose 1 Insecte sur un Nid avant sa production, puis allume l’icône Rêve.",
        "alias_oriente": "E>I",
        "id_profil": "E>I·A",
        "alias_profil": "R10-A",
        "animal_ou_theme": "Rêve des Entités",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste"
        ],
        "decision_joueur": {
          "choix": "Nourrir un Nid avant l’étape 4.2 pour franchir le palier de +2 Insectes, ou poser l’Insecte sur ce rang de Réglette afin de préparer une déviation ±1.",
          "renoncement": "Exige d’annuler effectivement une machine sur ce rang ; l’Insecte posé en Réglette n’ira jamais défendre en forêt."
        },
        "entrees": [
          "ANNULATION",
          "ALTEREE"
        ],
        "sorties": [
          "ALTEREE",
          "INSECTE",
          "INSECTE_RANG",
          "NID_ACTIVE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V3 -> V4",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.9
          },
          "composantes": {
            "Face unique": [
              "ALTEREE",
              "INSECTE"
            ]
          },
          "activations_pour_amortir": 1.1
        },
        "declencheurs_amorces": [
          6
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Poser l’Insecte sur un Nid à 1 Insecte si ce Nid va produire en 4.2 ; sinon le poser sur ce rang de Réglette pour préparer une déviation ±1 vers un Rêve.",
        "temoins": [
          {
            "id": "R10_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "annulee": true,
              "nid_insectes_avant_4.2": 2,
              "production_4.2": 2
            },
            "journal": [
              "R10 3.2 : annule machine -> altérée + 1 Insecte sur Nid (1->2) -> +2 en 4.2"
            ]
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 19,
            "phrases": 1,
            "conditions": 1
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Consolidation Canon 0 (Greffe 2) : choix entre Nid construit et rang de Réglette, ouvrant un 2e moteur majeur disjoint sur la table {H, E, I}."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "E"
  },
  "M1": {
    "id": "M1",
    "famille": "CROISSANCE",
    "couple": [
      "I",
      "M"
    ],
    "origine": "I",
    "nomBase": "La Fourmilière Coupe-Feuilles",
    "profils": {
      "A": {
        "nom": "La Fourmilière Coupe-Feuilles",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "PRODUCTION",
        "primitive": "DEPLACEMENT (INSECTE PASSAGER — PHORESIE)",
        "tags": [
          "TWIST",
          "PHORESIE",
          "INSECTES",
          "PARADE_MOBILE"
        ],
        "requires_options": {},
        "texte": "Après production, 1 Insecte de ce Nid monte sur une machine de son rayon et défend chaque parcelle qu’elle frappe.",
        "temoin": "L’Insecte passager accompagne l’Abatteuse et complète une parade (allumant l’icône Insecte) ; non dépensé, il descend sur la parcelle de la machine au ménage.",
        "alias_oriente": "I>M",
        "id_profil": "I>M·A",
        "alias_profil": "M1-A",
        "animal_ou_theme": "Nid des Insectes (fourmis coupe-feuilles)",
        "est_twist_canon0": true,
        "piste_twist": "Annexe A #5 — L’Insecte passager (phorésie)",
        "role_porte": [],
        "decision_joueur": {
          "choix": "Embarquer un Insecte sur une machine (défense mobile qui la suit partout) ou le garder au Nid pour la masse critique.",
          "renoncement": "L’Insecte quitte le Nid : la production suivante peut tomber de +2 à +1."
        },
        "entrees": [
          "INSECTE"
        ],
        "sorties": [
          "INSECTE_PASSAGER"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 0.8
          },
          "composantes": {
            "Face unique": [
              "INSECTE_PASSAGER"
            ]
          },
          "activations_pour_amortir": 2.5
        },
        "declencheurs_amorces": [
          6
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Embarquer sur l’Abatteuse en Assaut la plus dangereuse si le Nid garde au moins 2 Insectes.",
        "temoins": [
          {
            "id": "M1_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                6
              ],
              "p3-M": 3,
              "passager_restant": 0
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 21,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "I"
  },
  "M2": {
    "id": "M2",
    "famille": "CROISSANCE",
    "couple": [
      "I",
      "R"
    ],
    "origine": "I",
    "nomBase": "La Termitière à Glu",
    "profils": {
      "A": {
        "nom": "La Termitière à Glu",
        "cycle": "PASSIF_CONTINU",
        "cablage": null,
        "fenetre": "LOI PARADE",
        "primitive": "MOD_LOI_DU_COEUR (PARADE INSECTE -> SABOTAGE)",
        "tags": [
          "LOI_PASSIVE",
          "INSECTES",
          "SABOTAGE",
          "FLUX_EN_AVAL"
        ],
        "requires_options": {},
        "texte": "<strong>En Parade :</strong> Pour chaque Insecte défaussé en Parade sur la parcelle de ce Nid, ajoutez 1 jeton Sabotage au sac.",
        "temoin": "Le Nid cohabite sans dommage avec les machines ; une parade sur sa parcelle dépensant 2 Insectes ajoute aussitôt 2 jetons Sabotage dans le sac.",
        "alias_oriente": "I>R",
        "id_profil": "I>R·A",
        "alias_profil": "M2-A",
        "animal_ou_theme": "Nid des Insectes (termites)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Loi passive (1 des 2 emplacements-lois ; plafond C08 = 5, ≤ 2 par assise)"
        ],
        "decision_joueur": {
          "choix": "Défendre la parcelle du Nid avec ses Insectes : chaque Insecte sacrifié encrasse le sac des Reptiles.",
          "renoncement": "Chaque Insecte dépensé quitte le Nid et réduit la masse critique du tour suivant."
        },
        "entrees": [
          "INSECTE"
        ],
        "sorties": [
          "SABOTAGE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V3",
        "acte": "les_deux",
        "nature": "loi_passive",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Loi 5.1": 1.4
          },
          "composantes": {
            "Loi 5.1": [
              "SABOTAGE",
              "SABOTAGE"
            ]
          },
          "activations_pour_amortir": 1.4
        },
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Garder le Nid sur une parcelle ciblée par une machine du rang 1 (fréquente) et y engager les Insectes.",
        "temoins": [
          {
            "id": "M2_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "sabotages_pour_6.3": 2,
              "declencheurs": [
                6
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "En Parade": {
            "mots": 18,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "I"
  },
  "M3": {
    "id": "M3",
    "famille": "CROISSANCE",
    "couple": [
      "I",
      "O"
    ],
    "origine": "I",
    "nomBase": "La Branche des Guêpes Cazadores",
    "profils": {
      "A": {
        "nom": "La Branche des Guêpes Cazadores",
        "cycle": "PASSIF_CONTINU",
        "cablage": null,
        "fenetre": "LOI MIGRATION",
        "primitive": "MOD_LOI_DU_COEUR (MIGRATION LATERALE VERS LA PLUME)",
        "tags": [
          "LOI_PASSIVE",
          "INSECTES",
          "PONT_LATERAL",
          "VIGIE"
        ],
        "requires_options": {},
        "texte": "<strong>En Migration :</strong> Les Insectes de ce Nid peuvent migrer vers la parcelle de même profondeur du rayon de la Plume de Vigie.",
        "temoin": "Nid en p3-I avec 3 Insectes et Plume au pied des Humains : en Migration, l’essaim vole latéralement en p3-H avant les attaques.",
        "alias_oriente": "I>O",
        "id_profil": "I>O·A",
        "alias_profil": "M3-A",
        "animal_ou_theme": "Nid des Insectes (guêpes)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Loi passive (1 des 2 emplacements-lois ; plafond C08 = 5, ≤ 2 par assise)"
        ],
        "decision_joueur": {
          "choix": "Les Oiseaux posent la Plume sur le rayon à renforcer ; l’essaim de la Branche y vole en 4.3, juste avant les frappes.",
          "renoncement": "Les Insectes qui quittent le Nid réduisent sa masse critique ; la Plume posée pour l’essaim ne signale plus un autre pari."
        },
        "entrees": [
          "INSECTE",
          "PLUME"
        ],
        "sorties": [
          "INSECTE"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V3",
        "acte": "les_deux",
        "nature": "loi_passive",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Loi 4.3": 1.0
          },
          "composantes": {
            "Loi 4.3": [
              "INSECTE",
              "INSECTE"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [
          6
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Oiseaux : Plume sur le rayon le plus menacé de même profondeur que le Nid ; Insectes : garder 2 Insectes au Nid pour la masse critique.",
        "temoins": [
          {
            "id": "M3_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "declencheurs": [
                6
              ],
              "p3-H": [
                3,
                1
              ]
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "En Migration": {
            "mots": 20,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "I"
  },
  "M4": {
    "id": "M4",
    "famille": "CROISSANCE",
    "couple": [
      "I",
      "H"
    ],
    "origine": "I",
    "nomBase": "La Ruche des Mélipones",
    "profils": {
      "A": {
        "nom": "La Ruche des Mélipones",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "PRODUCTION",
        "primitive": "DEPLACEMENT (INSECTE -> TAMBOUR) OU MOD_PUISSANCE (SURCHAUFFE)",
        "tags": [
          "INSECTES",
          "TAMBOUR",
          "SURCHAUFFE",
          "PONT_LATERAL",
          "A0"
        ],
        "requires_options": {},
        "texte": "Après production, envoyez 1 Insecte de ce Nid rejoindre le Tambour ou défaussez-le pour retourner 1 jeton rouge en bleu.",
        "temoin": "Après production, la Ruche défausse 1 Insecte pour retourner 1 rouge en bleu (actif dès la Charge à −1 et en Assaut/Ratissage à −2 net) ou renforce la parcelle du Tambour.",
        "alias_oriente": "I>H",
        "id_profil": "I>H·A",
        "alias_profil": "M4-A",
        "animal_ou_theme": "Nid des Insectes (abeilles mélipones)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste"
        ],
        "decision_joueur": {
          "choix": "Projeter 1 Insecte vers la parcelle alliée du Tambour pour parer, ou sacrifier cet Insecte afin de retourner 1 jeton rouge en Surchauffe bleue.",
          "renoncement": "L’Insecte projeté ou défaussé quitte la Ruche (au risque de repasser sous le palier de 2 Insectes au tour suivant)."
        },
        "entrees": [
          "INSECTE",
          "TAMBOUR",
          "ROUGE"
        ],
        "sorties": [
          "INSECTE",
          "BLEU"
        ],
        "paiement": [
          "P_ARBRE"
        ],
        "vecteurs": "V4 -> V2",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.3
          },
          "composantes": {
            "Face unique": [
              "INSECTE_OU_BLEU"
            ]
          },
          "activations_pour_amortir": 1.5
        },
        "declencheurs_amorces": [
          6,
          1
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Si une machine en Assaut/Ratissage porte un rouge décisif, défausser 1 Insecte pour le retourner en bleu ; sinon envoyer 1 Insecte rejoindre le Tambour en forêt.",
        "temoins": [
          {
            "id": "M4_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "p4-E": 3,
              "declencheurs": [
                6
              ]
            },
            "journal": [
              "A_E -> p3-E : non parée, Seuil 2 -> 0 Arbre(s), 3 Souche(s)",
              "A_E -> p4-E : parade 1 Déf. + 1 Insecte(s), Seuil 2 (6)"
            ]
          },
          {
            "id": "M4_T2",
            "statut": "OK",
            "etat_attendu_verifie": {
              "rouges": 0,
              "bleus": 1,
              "insectes_nid_apres": 0
            },
            "journal": [
              "M4 4.2 : production +1 -> défausse 1 Insecte -> 1 rouge retourné en bleu"
            ]
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 21,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Consolidation Canon 0 (Greffe 1) : ajout de l’option Surchauffe par dépense d’1 Insecte, couvrant les tables sans Oiseaux (dont {H,E,I} et {H,E,M,I})."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "I"
  },
  "M5": {
    "id": "M5",
    "famille": "CROISSANCE",
    "couple": [
      "I",
      "E"
    ],
    "origine": "I",
    "nomBase": "Le Jardin du Diable",
    "profils": {
      "A": {
        "nom": "Le Jardin du Diable",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "PRODUCTION / DÉCOMPTE FINAL",
        "primitive": "DEPLACEMENT (INSECTE -> SOUCHES) + REPOUSSE PAR L’ESSAIM",
        "tags": [
          "INSECTES",
          "SOUCHES",
          "ENRACINEMENT",
          "REPOUSSE_FINALE",
          "A0"
        ],
        "requires_options": {},
        "texte": "Après production, déplacez 1 Insecte de ce Nid vers une parcelle à Souche de son rayon ou du rayon des Entités.<br><strong>Enraciné :</strong> Au décompte final, chaque Insecte de sa parcelle y retourne 1 Souche de plus en Arbre debout.",
        "temoin": "Enraciné face à p3-I (3 Souches, 2 Insectes) : au décompte final, les 3 Souches survivantes sont retournées sur leur face Arbre debout (1 de base + 2 par les Insectes).",
        "alias_oriente": "I>E",
        "id_profil": "I>E·A",
        "alias_profil": "M5-A",
        "animal_ou_theme": "Nid des Insectes (fourmis du jardin du diable)",
        "est_twist_canon0": false,
        "piste_twist": null,
        "role_porte": [
          "Autonomie A = 0 (table {H, E, I}) — aucune dépendance aux Gardiens ni à la Piste",
          "Synergie d’Enracinement volontaire"
        ],
        "decision_joueur": {
          "choix": "Accumuler l’essaim sur une parcelle à Souches, puis enraciner le Nid face à elle pour convertir les Insectes en repousse.",
          "renoncement": "Enraciné, le Nid ne produit plus ; chaque Insecte gardé pour la repousse ne pare aucune frappe."
        },
        "entrees": [
          "INSECTE",
          "SOUCHE"
        ],
        "sorties": [
          "INSECTE"
        ],
        "paiement": [
          "P_ARBRE",
          "P_SOUCHE"
        ],
        "vecteurs": "V4 -> V1",
        "acte": "les_deux",
        "nature": "action",
        "prix_estime": {
          "unite": "Défenseur-tour (DT)",
          "bareme": "H0 a priori — à remplacer par le barème mesuré du Lot 0",
          "cout_construction_DT": 2,
          "par_face": {
            "Face unique": 1.0,
            "Enraciné": 3.6
          },
          "composantes": {
            "Face unique": [
              "INSECTE",
              "INSECTE"
            ],
            "Enraciné": [
              "SOUCHE_REGEN",
              "SOUCHE_REGEN",
              "SOUCHE_REGEN"
            ]
          },
          "activations_pour_amortir": 2.0
        },
        "declencheurs_amorces": [
          6
        ],
        "double_ouverture": null,
        "cablage_recommande": null,
        "heuristique_bot": "Envoyer les Insectes sur la parcelle à Souches la moins menacée ; enraciner au Tour 6–7 face à elle.",
        "temoins": [
          {
            "id": "M5_T1",
            "statut": "OK",
            "etat_attendu_verifie": {
              "p3-I_final": [
                3,
                0
              ]
            },
            "journal": []
          },
          {
            "id": "M5_T2",
            "statut": "OK",
            "etat_attendu_verifie": {
              "avec_insecte": [
                2,
                false
              ],
              "sans_insecte_route": true
            },
            "journal": []
          }
        ],
        "mots_par_face": {
          "Face unique": {
            "mots": 21,
            "phrases": 1,
            "conditions": 0
          },
          "Enraciné": {
            "mots": 17,
            "phrases": 1,
            "conditions": 0
          }
        },
        "statut": "canon0_audite_statique",
        "journal": [
          "2026-11-24 — Canon 0 : profil de référence rédigé ; audit 197 assises conforme ; témoins exécutés."
        ],
        "engine_sync_status": "PENDING_KERNEL_V6_2"
      }
    },
    "peuple_origine": "I"
  }
};

const VERSION_CHANGELOG = [
  {
    "version": "v6.2",
    "date": "2026-11-24",
    "titre": "Fondation SSOT v6.2 : Socle épuré, Asymétrie Hybride 3 + 3, Enracinement volontaire & Canon 0 (30 tuiles)",
    "resume": "Passage à la source unique de vérité (contracts/rules_canon_v6_2.json, physical_and_edge_invariants.json, tiles_canon_v6_2.json) : matériel fini recto-verso (10×N Arbres/Souches, jetons Puissance Rouge/Bleu, 2 Défenseurs Réflexion/Définitif), sac opaque, lancer de dés universel, bandelette d'Acte réversible, Piste des Gardiens à 6 icônes (Résonance en 6e, 2 encoches visibles), Bleus actifs en tous modes, Ratissage à +1 rouge physique, zéro écrasement hors Route, accessoires 3+3, Enracinement volontaire et 30 tuiles Canon 0 auditées sur 197 assises.",
    "deltas": [
      {
        "domaine": "Matériel fini & Sac opaque (INV-01 à INV-07)",
        "avant": "Réserves illimitées, pioche par paquet de cartes, seuls les porteurs de Machine lançaient les dés.",
        "apres": "10×N pions uniques recto-verso Arbre/Souche, jetons Puissance Rouge/Bleu, sac opaque de jetons épais (2N Machines + Sabotages + max 4 Écailles), pénurie horaire depuis le Coordonnateur (Oiseau dernier), lancer de dés universel sous paravent fermé."
      },
      {
        "domaine": "Supports fixes, 6 icônes Gardiens & Encoches (INV-08 à INV-10)",
        "avant": "Retournement de toute la Réglette au Tour 5 ; Piste des Gardiens numérotée 1..6 avec Résonance en 4e position et sans encoches latérales visibles.",
        "apres": "Réglette fixe 1–6 à bandelette d'Acte réversible dessous ; Piste des Gardiens à 6 icônes sans numéros [Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance] (compteur individuel sans écrasement) ; 2 encoches latérales visibles par Gardien (≥ 1 encoche requise pour passer Face 2)."
      },
      {
        "domaine": "Seuil, Ratissage, Repli & Contacts (INV-11 à INV-17)",
        "avant": "Bleus ignorés en Mode Charge ; +1 imprimé en Ratissage ; écrasement du Nid au contact machine ; double bond possible en Repli de bordure.",
        "apres": "Bleus Surchauffe (−1) actifs dans tous les modes (Charge, Assaut, Ratissage) ; Ratissage donne +1 jeton rouge physique (0 imprimé) et rend sa parcelle ciblée ; zéro écrasement au contact hors Route (seule la Route vide la case) ; poussée de bordure couvre l'avancée En avançant."
      },
      {
        "domaine": "Asymétrie 3 + 3, Enracinement & Canon 0 (30 tuiles)",
        "avant": "Ancien catalogue de 32 emplacements (incluant 2 slots de migration) et châssis à axes multiples v6.0.",
        "apres": "Châssis unique verrouillé (P4_2233, départ décalé Bulldozer p=1 / Abatteuse p=2, 0 écart), 3 modules (Gardiens/Éveil, Rêves/Sommeil, Essaim absorbant Déviation ±1 et Bouclier facultatif), accessoires 3+3, Enracinement volontaire (1/2 Souches au décompte final) et Canon 0 de 30 tuiles (48 faces ≤ 25 mots, 34 témoins)."
      }
    ]
  },
  {
    "version": "v6.1",
    "date": "Branche expérimentale exp/socle-v6 (2026-11-22)",
    "titre": "Socle gelé v6.1 : départ décalé, Abatteuse coupe-tout, Pièges autonomes 1 frappe, Charge sur frappe non parée & Furtivité « Chaud vs Calme »",
    "resume": "Incrément canonique gelé pro-simplicité (schema_version 6.1.0-alpha, P4_2233 + départ décalé Bulldozer p=1 / Abatteuse p=2, chassis_id = 24) : l'Abatteuse coupe tous les Arbres debout de la parcelle ciblée et ne touche jamais aux Souches ; Pièges autonomes sans Embuscade parant exactement 1 frappe puis défaussés aussitôt (SINGLE_STRIKE) ; gain Charge gelé sur FRAPPE_NON_PAREE (+1 jeton Puissance max/activation dès qu'au moins 1 frappe sur parcelle réelle non-Route n'est ni parée ni piégée, hors Devant dans le vide) ; Rêves ouverts en 2.1 et recentrés sur le blocage pur (CLEAR_RANK_ONLY, REVE_TRIG=ACTIF figé) ; Furtivité « Chaud vs Calme » par rayon (Rive Piège m(r)==2 gouvernée par le propriétaire du rayon, Rive Sabotage m(r)==0) ; élagage du test Ratissage en 1.1 et du passage d'Insectes en Furtivité.",
    "deltas": [
      {
        "domaine": "Départ décalé canonique & Abatteuse coupe-tout (sans micro-règle souche)",
        "avant": "v6.0 : Départ groupé en parcelle 1 ; Abatteuse coupait au maximum 2 Arbres debout avec option de souche en Ratissage.",
        "apres": "v6.1 : Mise en place décalée canonique (Bulldozer en parcelle 1, Abatteuse en parcelle 2 sur chaque rayon, chassis_id = 24) ; l’Abatteuse coupe tous les Arbres debout de la parcelle ciblée en Souches et ne touche jamais aux Souches (suppression définitive de la micro-règle souche) ; maintien strict de T3/T6 mod_seuil = -1 et Bulldozer = 1 Arbre + toutes Souches."
      },
      {
        "domaine": "Rêves épurés en socle, ouverture de 2.1 aux Rêves & déclencheur 5. Rêve actif",
        "avant": "v6.0 : Seul le 2e Défenseur (2.2) pouvait cibler un Rêve ; choix exclusif Bloquer OU Avancer en 3.2 ; 5. Rêve allumé même sur un Rêve inerte sans Défenseur.",
        "apres": "v6.1 : Le 1er Défenseur (2.1, simultané et fixe) peut désormais cibler tout Rêve déjà en piste (seule la Piste des Gardiens reste réservée à 2.2), débloquant l’Éveil à 5J–6J sur un Gardien case 5. Dans le socle, tout Rêve défendu applique uniquement le blocage (1 Défenseur annule 1 machine prioritaire, le Rêve ne bouge pas ; avancée transférée au Mode 4). REVE_TRIG=ACTIF figé : 5. Rêve s’allume uniquement si un Rêve défendu annule réellement >= 1 machine non déviée."
      },
      {
        "domaine": "Furtivité « Chaud vs Calme » par piste de forêt (Rive Piège vs Rive Sabotage)",
        "avant": "v6.0 : Furtivité sur lisières par parcelle en face (condition statique présence/activité de machine).",
        "apres": "v6.1 : Au pied de chaque rayon r (1..N), 2 rives de 2 emplacements (Rive Piège et Rive Sabotage) ouvertes à toute la table en 2.1 et 2.2 (fermées dès que le rayon est 100 % en Routes). En 4.1, seule une rive à 2 Défenseurs est évaluée selon m(r) = cartes Machine de r révélées en 3.2 + Ratissages de r (indépendant de déviation Insecte ±1 et d’annulation Rêve). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège sur une parcelle non-Route de r) ; Rive Sabotage gagnée si m(r) == 0 (+1 Sabotage pour 6.3)."
      },
      {
        "domaine": "Pièges autonomes 1 frappe (SINGLE_STRIKE) & Charge sur frappe non parée (FRAPPE_NON_PAREE)",
        "avant": "v6.0 : Un Piège exigeait Défense totale >= 1 (Embuscade) sur la parcelle pour se déclencher ; gain en Charge uniquement sur dégât effectif.",
        "apres": "v6.1 : Dès qu’un jeton Piège est présent sur une parcelle attaquée en 5.1/5.2, il se déclenche de lui-même (même avec 0 Défenseur et 0 Insecte), pare exactement 1 frappe puis est défaussé aussitôt sans consommer les Défenseurs ou Insectes présents, en allumant uniquement 2. Piégeage. Gain Charge gelé sur FRAPPE_NON_PAREE (+1 jeton Puissance max/activation dès qu’au moins 1 frappe sur parcelle réelle non-Route n’est ni parée ni piégée, hors Devant dans le vide)."
      }
    ]
  },
  {
    "version": "v6.0",
    "date": "Incrément précédent exp/socle-v6 (2026-11-21)",
    "titre": "Refonte du socle cœur v6.0 : Réglette réversible Charge/Assaut, Rêves Bloquer/Avancer, Furtivité libre & 0 Repousse Finale",
    "resume": "Évolution majeure du cœur de jeu en branche expérimentale (schema_version 6.0.0-alpha, calibrée d'abord en Mode 2 à tuiles neutres sans toucher au socle figé v5.5 sur main) : Réglette des Tactiques réversible en 2 Actes (Face A Tours 1–4 : 1–3 Charge / 4–6 Assaut ; Face B Tours 5–8 : permutation 1–3 Assaut / 4–6 Charge ; Ratissage détaché en Assaut permanent), Rêves en choix exclusif Bloquer OU Avancer avec saut vers la 1re case libre à gauche, Furtivité libre à 2 rives indépendantes (1 ou 2 binômes complets par case, zéro glissement forcé) et suppression de la Repousse Finale automatique de base (score = Arbres debout).",
    "deltas": [
      {
        "domaine": "Réglette des Tactiques réversible par blocs (Charge / Assaut) & Ratissage",
        "avant": "v5.5 : Piste fixe T1..T6 asymétrique (T4/T5/T6 donnaient +1 jeton rouge systématiquement) et Ratissage rattaché à T1 Sur place.",
        "apres": "v6.0 : Lecture unique du Dé MIN (Tours 1–8). Actions fixes 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (+1 parcelle, -1 seuil). Face A (Acte 1, Tours 1–4) : 1–3 CHARGE / 4–6 ASSAUT ; Face B (Acte 2, Tours 5–8, retournée début Tour 5) : 1–3 ASSAUT / 4–6 CHARGE. CHARGE ignore les jetons Puissance existants au seuil et donne +1 jeton uniquement si >= 1 dégât effectif (plafonné à +1/activation). ASSAUT active tous les jetons Puissance sans gain. Ratissage détaché de la case 1 en ASSAUT permanent (+1 imprimé)."
      },
      {
        "domaine": "Rêves en choix exclusif « Bloquer OU Avancer »",
        "avant": "v5.5 : Un Rêve annulait 1 machine par Défenseur et avançait automatiquement uniquement si toutes les machines du rang étaient annulées.",
        "apres": "v6.0 : Pour chaque Rêve muni d’au moins 1 Défenseur et visé en 3.2, le Peuple Onirique tranche : BLOQUER (1 Défenseur annule 1 machine prioritaire, le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit, 0 machine annulée, toutes jouent la Tactique dessous, et le Rêve saute vers la 1re case libre à sa gauche). Déclencheur 5. Rêve inchangé."
      },
      {
        "domaine": "Furtivité libre (2 rives indépendantes)",
        "avant": "v5.5 : Entrer sur une case de Furtivité attirait de force le partenaire sur la case jumelle (max 2 Défenseurs et 1 seule action par case).",
        "apres": "v6.0 : Zéro glissement forcé. Les 4 emplacements (2 rives de 2 cases) sont libres. En 4.1, chaque rive déclenche son action uniquement si elle forme un binôme complet (2 Défenseurs ; un pion seul ne déclenche rien). Si les 4 emplacements sont occupés, les 2 rives s’exécutent toutes les deux."
      },
      {
        "domaine": "Suppression de la Repousse Finale de base",
        "avant": "v5.5 : En fin de partie, 1 Souche par parcelle non rasée repoussait automatiquement en Arbre avant le score.",
        "apres": "v6.0 : 0 Repousse Finale automatique de base — le score compte uniquement les Arbres debout. La règle de l’Abatteuse en Ratissage (arrache 1 Souche s’il n’y a plus d’Arbre sous l’option correspondante) est conservée intacte pour préserver les Routes Forestières et le Repli."
      }
    ]
  },
  {
    "version": "v5.5",
    "date": "Socle figé précédent (2026-11-20)",
    "titre": "Gel officiel du socle v5.5, refonte éditoriale complète du Livret et état des lieux Mode 4",
    "resume": "Gel officiel du socle symétrique v5.5 (schema_version 5.5.0) consolidant toutes les règles validées en 5.4.7 : Piste des Tactiques fixe T1..T6, Rêves en coût d'activation (avancée uniquement si toutes les machines du rang sont annulées), Piste des Gardiens à pari uniforme (0/1/2 Défenseurs glissés, Face 2 en 5.3 uniquement sur pari gagné), partition stricte des 6 déclencheurs, Réveil de la Forêt 100 % Gardiens, Insectes Déviation + Bouclier de lisière. Réécriture intégrale du livret de règles joueur en 7 sections didactiques, vérification des 30 tuiles actives STANDARD_A en Mode 4, et enrichissement du digest (defense_attribution + tile_metrics complet).",
    "deltas": [
      {
        "domaine": "Gel du socle v5.5 (moteur & 4 couches Studio)",
        "avant": "v5.4.7 : Phase de stabilisation Mode 2 à blanc (verrous kernel dégelés, défauts hérités JUMP_PUSH et Colonie A).",
        "apres": "v5.5 (5.5.0) : Socle officiellement gelé et verrouillé (kernel_locks.sha256 rescellé), défauts officiels CLEAR_RANK_ONLY + SLOT_BUG_CERVEAU=B + SLOT_COLONISATION_GARDIENS=B, compatibilité vérifiée des 30 tuiles actives STANDARD_A avec la double activation Gardien et le passage Face 2 en 5.3 uniquement."
      },
      {
        "domaine": "Refonte complète du Livret de Règles joueur",
        "avant": "v5.4.7 : Livret accumulant des correctifs successifs, des codes techniques et des formulations rétrospectives.",
        "apres": "v5.5 : Livret réécrit intégralement de zéro en 7 sections éditoriales modernes (Présentation, Matériel, Vue d’ensemble, Déroulé étape par étape, Les Peuples, Fin & Repousse, Mémento de table), vocabulaire unifié, encadrés Règle d’or & Exemple concret, zéro jargon technique."
      },
      {
        "domaine": "Digest enrichi & Manifeste Mode 4 baseline_mode4_v5_5",
        "avant": "v5.4.7 : Campagnes mono-bot sans ventilation defense_attribution ni tile_metrics complet sur les 32 emplacements.",
        "apres": "v5.5 : Section defense_attribution (7 postes), support multi-bots B0/B1/B2, tile_metrics complet sur les 32 slots, et manifeste baseline_mode4_v5_5.json prêt pour le premier état des lieux Mode 4."
      }
    ]
  },
  {
    "version": "v5.4.7",
    "date": "Validation pré-gel (2026-11-20)",
    "titre": "Finalisation du socle : 6. Insecte strict (sans 4.2 Nids) & 4. Gardien verrouillé sur DISTINCT_OPEN_1",
    "resume": "Correction des deux biais détectés sur calibration_declencheurs_v5_4 : la production d’un Nid en 4.2 n’allume plus jamais 6. Insecte (partition stricte exclusivement en 3.2 déviation Bug ou 5.1 Parade classique avec dépense >= 1 Insecte), verrouillage définitif de 4. Gardien sur DISTINCT_OPEN_1 (suppression de DISTINCT_WON_2), et recalibrage de B2 (valorisation réaliste du Sabotage en 4.1 et arbitrage Migration 4.3 forêt / Bug / Bouclier de lisière).",
    "deltas": [
      {
        "domaine": "Déclencheur 6. Insecte (partition stricte sans 4.2 Nids)",
        "avant": "v5.4.6 : La production de jetons Insecte par un Nid en 4.2 allumait aussi 6. Insecte (~92–100 % des tours).",
        "apres": "v5.4.7 : La production d’un Nid en 4.2 n’allume jamais 6. Insecte. 6. Insecte s’allume exclusivement en 3.2 (déviation Bug prioritaire sur 5. Rêve) ou en 5.1 (Parade classique défaussant >= 1 Insecte, prioritaire sur 1. Parade)."
      },
      {
        "domaine": "Case 4. Gardien verrouillée sur DISTINCT_OPEN_1",
        "avant": "v5.4.6 : Duel expérimental DISTINCT_OPEN_1 vs DISTINCT_WON_2.",
        "apres": "v5.4.7 : Verrouillage sur DISTINCT_OPEN_1 (1re ouverture du tour de chaque autre Gardien distinct, anti-boucle conservé) et suppression de DISTINCT_WON_2."
      }
    ]
  },
  {
    "version": "v5.4.6",
    "date": "Version en vigueur (2026-11-20)",
    "titre": "Partition stricte des 6 déclencheurs Gardiens & Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B)",
    "resume": "Recalibrage complet des 6 déclencheurs de la Piste des Gardiens selon la partition stricte « 1 événement = au plus 1 déclencheur » (3.2 : Sabotage > Insecte Bug > Rêve ; 5.1 : Piégeage > Insecte Parade > Parade Défenseurs seuls ; 4.1 Furtivité sans déclencheur 2/3), duel sur 4. Gardien (DISTINCT_OPEN_1 vs DISTINCT_WON_2), et ajout du profil B « Bouclier de lisière » sur SLOT_COLONISATION_GARDIENS.",
    "deltas": [
      {
        "domaine": "Partition stricte 3.2 (Ouverture des paravents)",
        "avant": "v5.4.5 : 3. Sabotage s’allumait en 4.1 Furtivité ; 5. Rêve ne s’allumait qu’à l’annulation d’une machine par un Défenseur sur un Rêve.",
        "apres": "v5.4.6 : Au plus 1 déclencheur par carte révélée : 3. Sabotage (carte Sabotage révélée) > 6. Insecte (déviation Bug) > 5. Rêve (dé retenu M sur un rang occupé par un Rêve, annulée ou non)."
      },
      {
        "domaine": "Partition stricte 5.1 (Attaques des machines)",
        "avant": "v5.4.5 : 2. Piégeage s’allumait à la pose en 4.1 ; toute parade (Piège, Insecte ou Défenseurs) allumait 1. Parade.",
        "apres": "v5.4.6 : Au plus 1 déclencheur par frappe bloquée : 2. Piégeage (Piège armé) > 6. Insecte (Parade classique défaussant >= 1 Insecte) > 1. Parade (Défenseurs seuls sans Piège ni Insecte)."
      },
      {
        "domaine": "Case 4. Gardien & Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B)",
        "avant": "v5.4.5 : Chaque ouverture d’un autre Gardien allumait 4. Gardien ; tout pari perdu renvoyait le Gardien en lisière.",
        "apres": "v5.4.6 : Duel DISTINCT_OPEN_1 (1re ouverture du tour de chaque autre Gardien distinct) vs DISTINCT_WON_2 (2e puis 3e autre Gardien distinct achevant son pari). Nouveau profil B Bouclier de lisière : en 5.3 sur pari perdu, défausser 1 Insecte de la case empêche le retour en lisière (le pari reste PERDU)."
      }
    ]
  },
  {
    "version": "v5.4.5",
    "date": "Version en vigueur (2026-11-20)",
    "titre": "Éveil 100 % Gardiens, Plafond Pari Gardiens max 2 & Avancée Rêves CLEAR_RANK_ONLY",
    "resume": "Sortie complète des Rêves de l’Éveil de la Forêt (100 % Piste des Gardiens, Tours 1..7, A >= 1), plafond de pari sur les Gardiens à 2 Défenseurs max (gardien_bet_cap_policy : UNIFORM_MAX_2 vs MAX_2_RES_MAX_1 sur 4. Gardien), et avancée des Rêves paramétrable (JUMP_PUSH vs CLEAR_RANK_ONLY : un Rêve qui annule >= 1 machine s’ouvre toujours mais n’avance que si toutes les machines du rang M sont annulées).",
    "deltas": [
      {
        "domaine": "Éveil de la Forêt 100 % Piste des Gardiens (Étape 5.3)",
        "avant": "v5.4.4 : Mobilisation croisée Gardiens + Rêves avec politiques PARITY / PARITY_CAP_ONIRIQUE.",
        "apres": "v5.4.5 : Sortie complète des Rêves de l’Éveil. Aux Tours 1..7 (si A >= 1, priorité Tour 8), la Forêt s’éveille uniquement si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu’aucun pari n’est perdu (0 Défenseur restant)."
      },
      {
        "domaine": "Plafond de pari sur les Gardiens (Étape 2.2)",
        "avant": "v5.4.4 : Plafond uniforme d’1 seul Défenseur par Gardien sur les cases 1..6.",
        "apres": "v5.4.5 : Plafond à 2 Défenseurs max par Gardien construit (0 = inactif, 1 = 1 déclenchement attendu, 2 = 2 déclenchements attendus), avec duel UNIFORM_MAX_2 (max 2 sur 1..6) vs MAX_2_RES_MAX_1 (max 1 sur 4. Gardien). Anti-boucle 4. Gardien maintenue."
      },
      {
        "domaine": "Activation & Avancée des Rêves (Étape 3.2)",
        "avant": "v5.4.4 : Avancée JUMP_PUSH vs FREE_SLOT_ONLY.",
        "apres": "v5.4.5 : Rêves en coût d’activation indépendant de l’Éveil. Ajout de CLEAR_RANK_ONLY (face au témoin JUMP_PUSH) : un Rêve qui annule >= 1 machine s’ouvre toujours (allume 5. Rêve), mais n’avance vers la gauche (saut/poussée vers la 1re case libre à gauche) que si toutes les machines de ce rang M sont annulées ce tour-ci."
      }
    ]
  },
  {
    "version": "v5.4.4",
    "date": "Version en vigueur (2026-11-20)",
    "titre": "Pari unique sur les Gardiens, Consommation symétrique des Rêves & Éveil par mobilisation croisée",
    "resume": "Uniformisation du pari Gardien à 1 seul Défenseur max par Gardien construit (cases 1..6), consommation symétrique des Défenseurs sur les Rêves qui annulent effectivement 1 machine en 3.2, Éveil de la Forêt par mobilisation croisée (Gardiens + Rêves, politiques PARITY et PARITY_CAP_ONIRIQUE), et mode d’avancée des Rêves reve_advance_mode (JUMP_PUSH vs FREE_SLOT_ONLY). Purge du reliquat v5.4.1 dans spec_formelle.fins_5_3.",
    "deltas": [
      {
        "domaine": "Pari unique sur les Gardiens (Étape 2.2)",
        "avant": "v5.4.3 : Cumul libre de Défenseurs sur un même Gardien (exception gardien_resonance_cap sur 4. Résonance).",
        "apres": "v5.4.4 : Limite uniforme d’1 seul Défenseur par Gardien construit sur l’ensemble des 6 cases (anti-boucle 4. Gardien conservée)."
      },
      {
        "domaine": "Consommation symétrique & Avancée des Rêves (Étape 3.2)",
        "avant": "v5.4.3 : Défenseurs sur Rêves non suivis comme paris consommés ; avancée uniquement par saut/poussée (JUMP_PUSH).",
        "apres": "v5.4.4 : Chaque Défenseur sur un Rêve annulant effectivement 1 machine (Option A : 1_DEF_1_MACHINE) est consommé (pari gagné), sinon reste non consommé jusqu’au ménage. Deux modes d’avancée : JUMP_PUSH et FREE_SLOT_ONLY."
      },
      {
        "domaine": "Éveil de la Forêt par mobilisation croisée (Étape 5.3)",
        "avant": "v5.4.3 : Éveil exigeant les N Défenseurs uniquement sur la Piste des Gardiens.",
        "apres": "v5.4.4 : Aux Tours 1..7 (si A >= 1, priorité Tour 8), la Forêt s’éveille si les N Défenseurs ont été engagés en 2.2 sur Gardiens + Rêves, 0 pari perdu (0 Défenseur restant), et contrainte reveil_reves_policy respectée (PARITY : gardiens_won >= reves_won ; PARITY_CAP_ONIRIQUE : + reves_won <= nb_peuples_oniriques)."
      }
    ]
  },
  {
    "version": "v5.4.3",
    "date": "Version en vigueur (2026-11-20)",
    "titre": "Pari d’activation des Gardiens & Éveil de la Forêt (symétrique de l’activation des Rêves)",
    "resume": "Purge de l’ancien Réveil par unanimité/Face 2 et des marqueurs « utilisé » sur la Piste des Gardiens : les 2es Défenseurs posés en 2.2 sur un Gardien deviennent eux-mêmes son compteur d’activations restantes. Anti-boucle sur 4. Résonance (plafond hors-châssis UNLIMITED vs MAX_1_DEF). En 5.3 : pari gagné (reste en piste + passage Face 2 en Mode 4 si double-face), pari perdu (retour en lisière Face 1), priorité absolue à Tour 8, et Éveil de la Forêt aux Tours 1..7 si les N seconds Défenseurs étaient sur la Piste des Gardiens et que tous les paris sont gagnés.",
    "deltas": [
      {
        "domaine": "Pari d’activation des Gardiens (Étape 2.2)",
        "avant": "v5.4.2 : Marqueurs « utilisé » 1/tour sur cases 1..6, retournement Face 1 -> Face 2 universel à l’ouverture, engagement collectif sur 1 Gardien Face 2 avec retrait de la piste et condition 0 dommage réel.",
        "apres": "v5.4.3 : Zéro marqueur « utilisé ». Un Gardien sans 2e Défenseur est inactif. En 2.2 (si >= 1 Animal Sauvage M/R/O), pose cumulable de 2es Défenseurs sur tout Gardien construit (paramètre hors-châssis gardien_resonance_cap = UNLIMITED ou MAX_1_DEF sur 4. Résonance). Chaque déclencheur retire 1 Défenseur et ouvre le Gardien ; l’ouverture sur 4. Résonance ne ré-allume jamais 4. Résonance."
      },
      {
        "domaine": "Issue des paris & Éveil de la Forêt (Étape 5.3)",
        "avant": "v5.4.2 : Test 0 dommage réel en 5.3 et résolution de l’échec en 6.3.",
        "apres": "v5.4.3 : En 5.3, pari gagné (>=1 posé en 2.2 et 0 restant) -> le Gardien reste en piste (passage Face 2 en Mode 4 si double-face) ; pari perdu (>=1 Défenseur restant) -> retour immédiat en lisière d’origine Face 1. Priorité absolue à Tour 8 ; aux Tours 1..7, Éveil de la Forêt si les N seconds Défenseurs étaient sur la Piste des Gardiens et tous les paris sont gagnés."
      }
    ]
  },
  {
    "version": "v5.4.2",
    "date": "Version en vigueur (2026-11-19)",
    "titre": "Piste des Tactiques fixe (T1..T6), purge de l’Étape 6.1 et activation des Rêves en 2.2 (192 châssis)",
    "resume": "Piste des Tactiques T1..T6 imprimée en dur (zéro éjection, 6 axes = 192 châssis), suppression complète de l’Étape 6.1 et bascule de SLOT_BUG_CERVEAU sur le profil B par défaut, et activation des Rêves par pose de 2e Défenseur en 2.2 (Option A par défaut : 1 Déf = 1 Machine annulée, Options B/C paramétrables) avec avancée par saut/poussée vers la première case libre à gauche.",
    "deltas": [
      {
        "domaine": "Piste des Tactiques fixe (T1..T6) & Châssis 192",
        "avant": "v5.4.1 : 6 tuiles Tactique mobiles, axe Mise_En_Place_Tactiques (384 châssis), éjection de Tactique à la construction d’un Rêve.",
        "apres": "v5.4.2 : Cases 1..6 imprimées en dur T1..T6. Suppression de Mise_En_Place_Tactiques (6 axes = 192 châssis). Un Rêve construit se pose par-dessus la case libre la plus à droite (6, puis 5, etc.) sans aucune éjection."
      },
      {
        "domaine": "Suppression de l’Étape 6.1 & SLOT_BUG_CERVEAU",
        "avant": "v5.4.1 : Collecte de jetons en 6.1, avancée de la Tactique en tête en 6.2, SLOT_BUG_CERVEAU profil A par défaut.",
        "apres": "v5.4.2 : Étape 6 réduite au seul ménage de fin de tour (6.2–6.3). SLOT_BUG_CERVEAU bascule par défaut sur le profil B (déviation ±1 rang en 3.2 par défausse d’1 Bug)."
      },
      {
        "domaine": "Activation des Rêves en 2.2 & Avancée par saut/poussée",
        "avant": "v5.4.1 : Tout dé M tombant sur un Rêve annulait automatiquement la machine et ouvrait le Rêve (avancée simple d’1 cran).",
        "apres": "v5.4.2 : Pose légale du 2e Défenseur en 2.2 sur un Rêve de la piste. En 3.2, 1 Défenseur annule 1 machine sur ce rang (Option A par défaut ; Options B/C paramétrables) ; toute machine non annulée exécute la Tactique imprimée sous le Rêve. Dès >=1 machine annulée, le Rêve s’ouvre et avance vers la première case libre à sa gauche (saut/poussée du bloc contigu)."
      }
    ]
  },
  {
    "version": "v5.4.1",
    "date": "Version en vigueur (2026-11-19)",
    "titre": "Réveil de la Forêt par engagement collectif sur Gardien Face 2 (purge du Seuil fixe)",
    "resume": "Remplacement définitif du Seuil de Réveil fixe par le Réveil de la Forêt : actif si >= 1 Peuple Animal Sauvage (M/R/O), éveil universel Face 1 -> Face 2 à l’ouverture d’un Gardien, engagement collectif en 2.2 au quota Q sur 1 Gardien Face 2 (case libérée dès 3.1) et déclenchement en 5.3 si 0 dommage réel subi ce tour.",
    "deltas": [
      {
        "domaine": "Réveil de la Forêt (Condition de victoire Gardiens)",
        "avant": "v5.4 : Seuil de Réveil fixe calculé à la mise en place sur le nombre de marqueurs « utilisé » en fin de 5.3.",
        "apres": "v5.4.1 : Actif uniquement si >= 1 Peuple Animal Sauvage (M/R/O) à la table. Éveil universel Face 1 -> Face 2 à l’ouverture d’un Gardien (G14:C éligible sur Face 2 Rassasié). En 2.2, engagement collectif au quota Q de 2es Défenseurs sur 1 Gardien Face 2 (retiré de la piste, case libre dès 3.1) ; déclenchement immédiat en 5.3 si 0 dommage réel ce tour, sinon sort du Gardien résolu en 6.3."
      }
    ]
  },
  {
    "version": "v5.4",
    "date": "Version en vigueur (2026-11-19)",
    "titre": "6 Profils de Pistes, Placement Échelonné, Sommeil en Bloc & Mode Ratissage (384 configs)",
    "resume": "Évolution majeure du cœur de jeu : 4 nouveaux profils de pistes homogènes (2223, 1223, 22223, 12223), option de placement initial échelonné (Bulldozer p=1, Abatteuse p=2) remplaçant DEPASSEMENT_DERNIERE_PARCELLE, victoire par Sommeil exigeant le bloc contigu en tête de tous les Rêves en jeu, et remplacement définitif du Siège T4 par le mode Ratissage (pion double face, +1 puissance rouge imprimée, T1 Sur place).",
    "deltas": [
      {
        "domaine": "1. Profils de pistes homogènes (Axe 1 · 6 profils)",
        "avant": "v5.3 : 2 profils de pistes uniquement — P4_2233 [2,2,3,3] (10N Arbres) et P5_22233 [2,2,2,3,3] (12N Arbres).",
        "apres": "v5.4 : 6 profils homogènes sur tous les rayons — P4_2233 [2,2,3,3], P4_2223 [2,2,2,3], P4_1223 [1,2,2,3], P5_22233 [2,2,2,3,3], P5_22223 [2,2,2,2,3] et P5_12223 [1,2,2,2,3]."
      },
      {
        "domaine": "2. Placement initial des machines (Axe 5 · 384 configs)",
        "avant": "v5.3 : Option Declenchement_Fin_De_Piste (ARRIVEE_DERNIERE_PARCELLE vs DEPASSEMENT_DERNIERE_PARCELLE) ; 128 configurations.",
        "apres": "v5.4 : Suppression définitive de DEPASSEMENT_DERNIERE_PARCELLE. Nouvel Axe 5 Placement_Initial_Machines : MEME_PARCELLE_P1 (Bulldozer & Abatteuse en p=1) vs BULLDOZER_P1_ABATTEUSE_P2 (Bulldozer en p=1, Abatteuse en p=2). Espace combinatoire porté à 6 × 2^6 = 384 configurations."
      },
      {
        "domaine": "3. Victoire par Sommeil du Contremaître (Bloc de Rêves)",
        "avant": "v5.3 : Victoire dès qu’une seule tuile Rêve atteint le Rang 1 (case 1) de la Piste des Tactiques.",
        "apres": "v5.4 : Toutes les tuiles Rêves en jeu (2 par peuple onirique présent à la table, soit 2 ou 4 ; victoire impossible à 0 peuple onirique) doivent occuper en bloc contigu toutes les premières positions à gauche de la Piste des Tactiques (rangs 1..k)."
      },
      {
        "domaine": "4. Abandon du « Siège » → Mode « Ratissage » (Pion double face)",
        "avant": "v5.3 : État Siège appliquant la tactique T4 (+1 rouge ajouté à chaque tour, -1 Seuil) et alimentant T4 en Apprentissage.",
        "apres": "v5.4 : Pions machine double face (face normale -> retournement permanent sur face Ratissage dès la dernière parcelle non rasée). Mode Ratissage : +1 puissance imprimé directement applicable (traité comme +1 rouge à tous égards, conservant les jetons rouges acquis) et application systématique de T1 Sur place (mod Seuil 0, gain rouge 0, alimente T1 en 6.1 Apprentissage). R7:B simplifiée en -1 Seuil sur les machines en Ratissage (E/M et voisins)."
      }
    ]
  },
  {
    "version": "v5.3",
    "date": "Version précédente (Audit · 25 arbitrages)",
    "titre": "Seuil Imprimé Fixe, Embuscade unique (100 profils), Furtivité à 4 emplacements jumeaux & Zéro Verrouillage",
    "resume": "Alignement intégral Livret Humain / Catalogue (100 profils) / Simulateur / BGA : Seuil Imprimé fixe (P4_2233 / P5_22233), Furtivité orientée à 4 emplacements jumeaux, gouvernance unitaire par Peuple d’origine, défausse immédiate des Insectes à la parade (zéro dette et zéro verrouillage des parcelles), cascades de Gardiens à plat (1→6) et résolution complète machine par machine.",
    "deltas": [
      {
        "domaine": "1. Topologie, Seuil Imprimé & Chaîne des Parades (100 profils)",
        "avant": "v5.2 : Seuil comptant Arbres + Souches ; 2 options de Pièges avec Amortisseur (116 profils D/E).",
        "apres": "v5.3 : P4_2233 [2,2,3,3] (10N Arbres) ou P5_22233 [2,2,2,3,3] (12N Arbres). Seuil = max(1, Seuil_Imprimé(p) + Offset + Rouges - Bleus + Mod_Tactique + Mod_Tuiles). Suppression de l’Amortisseur (100 profils). Chaîne stricte à chaque frappe : 1° Jaguar (2 bleus) -> 2° Harpie -> 3° Piège Embuscade (si Défense totale >= 1, locale ou à distance) -> 4° Parade classique."
      },
      {
        "domaine": "2. Furtivité à 4 emplacements jumeaux, Silence & Gouvernance",
        "avant": "Action bilatérale sur les 2 rives ou mémoire de l’ordre d’arrivée ; décisions collectives sur les tuiles.",
        "apres": "v5.3 : 4 emplacements par case Furtivité (2 jumeaux/rive, max 2 Défenseurs). Entrer sur la case (toute face) tire l’autre pion sur le jumeau de son bord et oriente l’unique action du binôme ; retourner de réflexion à définitif se fait strictement sur place. Silence tactique sous paravent fermé ; chaque Tuile et piste de Migration est gouvernée par son seul Peuple d’origine. Sabotage pur : +1 carte Sabotage identique ajoutée définitivement au paquet Machine (1 carte Sabotage tirée en Étape 1 = 1 activation machine perdue)."
      },
      {
        "domaine": "3. Combat d’un seul tenant, Zéro Verrouillage, Routes & Contact Nid",
        "avant": "Dette d’Insectes engagés ou verrouillage des parcelles ciblées durant l’Étape 5 ; cibles figées à la révélation.",
        "apres": "v5.3 : Défausse immédiate des Insectes requis à la frappe et zéro verrouillage des parcelles (seul un Piège déjà déclenché ne paie plus de coût volontaire). Ordre Tactiques 1..6 puis Sièges (Abatteuse avant Bulldozer sur un même rayon), chaque machine résolue d’un seul tenant depuis sa position réelle. Routes sautées le long du rayon ; tout mouvement machine entrant sur un Nid le renvoie reconstructible en lisière et défausse les Insectes de la case."
      },
      {
        "domaine": "4. Dés, Rêves, Nids, Cascades à plat (1→6), Siège & Fin de partie",
        "avant": "Cascades imbriquées, seuil de Réveil recalculé après sacrifice, Siège dépendant de T4.",
        "apres": "v5.3 : Lecture pure M = min(D1,D2) sur carte Machine (annulée si rang M = Rêve). Rêve inséré en case 6 (éjecte la Tactique la plus à droite, glissement partiel). Nid indivisible avant Gardiens ; Migration 0 ou 1 cran (aller simple vers pistes globales). Cascades à plat de 1 à 6 (marquage immédiat, Faces 2 autonomes). Siège T4 autonome (alimente T4 en 6.1 tant que T4 est en piste). Seuil de Réveil fixe vérifié en fin de 5.3 (+ Écho en 6.2) ; raz totale des jetons Apprentissage en 6.2."
      }
    ]
  },
  {
    "version": "v5.2",
    "date": "Étape intermédiaire (116 profils)",
    "titre": "Deux options exclusives de Pièges (Embuscade Assistée vs Amortisseur), 30 nouveaux profils D/E & Système de Tags",
    "resume": "Suppression définitive de l’auto-parade inconditionnelle des Pièges au profit de l’Axe 10 du châssis (portant l’espace de test à 128 configurations) et ajout de 30 profils dédiés (15 D + 15 E), portant le catalogue à 116 profils.",
    "deltas": [
      {
        "domaine": "Mécanique des Pièges (Étape 5 · Axe 10)",
        "avant": "v4.3 à v5.1 : Un jeton Piège sur une parcelle parait automatiquement et inconditionnellement toutes les frappes ciblant cette parcelle, même sans aucun Défenseur ni Insecte.",
        "apres": "v5.2 : Deux options exclusives sur l’Axe 10 :\n• Option par défaut exige Défense totale >= 1 (locale ou soutenue à distance) (Embuscade Assistée) : le Piège pare automatiquement si et seulement si la parcelle dispose d’au moins 1 point de Défense à l’instant de la frappe (pion local ou soutien autorisé).\n• Option AMORTISSEUR_SANS_PARADE (Amortisseur de Dégâts) : aucune Parade, mais réduit la coupe effective de l’Abatteuse de -1 et ramène le terrassement du Bulldozer à 0 Souche (sans besoin de présence)."
      },
      {
        "domaine": "Engagement & Persistance des Pièges (5.3)",
        "avant": "v5.1 : Tout Piège sur une parcelle ciblée se déclenchait.",
        "apres": "v5.2 : Un Piège ne devient engagé (PIEGE_ENGAGE = true) et n’est retiré/glissé en 5.3 que s’il a effectivement agi (Parade sous Embuscade, ou réduction réelle de dégâts sous Amortisseur). Un Piège non armé ou redondant avec M5 C / R8 B reste non engagé sur sa parcelle."
      },
      {
        "domaine": "Extension de la Bibliothèque : +30 Profils (D & E)",
        "avant": "v5.1 : 86 profils au total (64 A/B + 22 C).",
        "apres": "v5.2 : 116 profils au total sur les 32 mêmes emplacements : ajout de 15 profils D (G3, G7, G10, G11, G14, R4, R5, R6, R8, R10, M1 à M5) liés à l’Embuscade et 15 profils E liés à l’Amortisseur, avec validation stricte requires_options et 5 modules N=3 clés en main."
      }
    ]
  },
  {
    "version": "v5.1",
    "date": "Consolidation offensive & simplifications",
    "titre": "Puissance de frappe des Machines renforcée & 11 arbitrages de simplification",
    "resume": "Augmentation de la létalité des machines non parées pour créer des états intermédiaires de Souches et suppression des conditions superflues sur 11 tuiles.",
    "deltas": [
      {
        "domaine": "Frappe de l’Abatteuse & du Bulldozer (5.1 & 5.2)",
        "avant": "v4.3 à v5.0 : L’Abatteuse coupait 1 seul Arbre en Souche ; le Bulldozer retirait uniquement les Souches déjà présentes (frappait à vide sur 3 Arbres debout).",
        "apres": "v5.1+ : L’Abatteuse coupe jusqu’à 2 Arbres debout par parcelle frappée. Le Bulldozer coupe jusqu’à 1 Arbre debout en Souche PUIS terrasse toutes les Souches non protégées (y compris celle qu’il vient de créer), avec une seule vérification de Parade avant la coupe."
      },
      {
        "domaine": "Cible rasée avant résolution (5.1 / 5.2)",
        "avant": "Question ouverte en cas d’inversion G8 B ou de frappes multiples.",
        "apres": "v5.1+ : Toute frappe dont la parcelle cible a été rasée (Route Forestière) avant sa résolution est annulée sans report."
      },
      {
        "domaine": "Simplification de 11 profils (G5 A, G7 A, G8 A/B, R8 B, M5 A/C, G3 C, R4 C)",
        "avant": "Seuils mémorisés ou restrictions d’arbres debout.",
        "apres": "Lecture dynamique des Souches pour G5 A (valent 0), pose sous machine autorisée pour G7 A, R8 B laisse toujours 1 Souche sans condition de quantité initiale, M5 C coupe 1 Arbre mais terrasse 0 Souche."
      }
    ]
  },
  {
    "version": "v5.0",
    "date": "Enrichissement asymétrique",
    "titre": "Ajout de la Bibliothèque complémentaire des 22 Profils C & Conventions de résolution",
    "resume": "Création d’un 3e profil expérimental (Profil C) sur 20 tuiles de lisière et les 2 slots de migration (La Cigale et Les Lucioles), avec câblages dédiés (G10 C sur case 6, G12 C sur case 2) et cycle nourri (G14 C).",
    "deltas": [
      {
        "domaine": "Bibliothèque C (22 nouveaux profils)",
        "avant": "v4.9 : Uniquement Profil A (Flux) et Profil B (Loi) par emplacement (64 profils).",
        "apres": "v5.0+ : Ajout de 22 profils C explorant les traversées directes (G3 C, R7 C), les soutiens depuis les machines (G5 C), la Terra Preta en repousse finale (R6 C), le cycle À jeun/Rassasié (G14 C), la Cigale (Bug C) et les Lucioles (Colonie C)."
      }
    ]
  },
  {
    "version": "v4.9",
    "date": "Architecture formelle consolidée (depuis v4.3)",
    "titre": "Du Socle Didactique v4.3 à l’Architecture Siège T4, Surchauffe Rouge/Bleu & Routes Forestières",
    "resume": "Structuration complète du matériel (mini-paravents, jetons Puissance double-face Rouge/Bleu, Routes Forestières, Siège T4 irréversible et grammaire à 8 primitives).",
    "deltas": [
      {
        "domaine": "Secret & Matériel individuel (Étape 1 & 2)",
        "avant": "v4.3 : Gobelet opaque + carte Tactique « leurre » posée face cachée en cas de Sabotage ou Rêve.",
        "apres": "v4.9+ : Plateau personnel à Mini-Paravent reproduisant les 6 rangs (le dé M y est posé en secret ; l’emplacement Tactique reste simplement vide sur Sabotage ou Rêve). Jetons 1er Défenseur (1 face) et 2e Défenseur (2 faces réflexion/définitif) différenciés."
      },
      {
        "domaine": "Jetons Puissance Double-Face : Rouge (+1) / Bleu Surchauffe (-1)",
        "avant": "v4.3 : Jetons Puissance simples (+1 au seuil).",
        "apres": "v4.9+ : Jetons double-face : Rouge (+1 Seuil) au recto, Bleu Surchauffe (-1 Seuil en Étape 5 ET -1 Apprentissage en 6.1) au verso. Retourner un rouge en bleu abaisse de 2 le seuil brut."
      },
      {
        "domaine": "Routes Forestières & Siège Irréversible en T4 (1.1, 5.2, 5.3)",
        "avant": "v4.3 : Pas de règle de saut de parcelle rasée ni de verrouillage en bout de piste.",
        "apres": "v4.9+ : Une parcelle sans arbre ni souche reçoit une tuile Route Forestière (sautée par machines et insectes). Toute machine sur la dernière parcelle non rasée de son rayon entre irréversiblement en Siège (T4 automatique hors pioche à chaque tour)."
      },
      {
        "domaine": "Deux Slots de Migration Centrale (4.3)",
        "avant": "v4.3 : Migration uniquement vers la Piste des Tactiques (Bug du Cerveau).",
        "apres": "v4.9+ : Choix en fin de rayon entre SLOT_BUG_CERVEAU (Piste des Tactiques) et SLOT_COLONISATION_GARDIENS (Piste des Gardiens)."
      }
    ]
  }
];

const SPEC_FORMELLE_V6_0 = {
  "schema_version": "6.2.0",
  "date_consolidation": "2026-11-24",
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
      "perimetre": "Forêt finie 10×N, sac opaque de jetons, Réglette fixe à bandelette d'Acte, Défenseurs recto-verso, Furtivité Chaud/Calme, Pièges autonomes, attaques, Ratissage, Enracinement volontaire et score final."
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
        "resume": "Lu uniquement si au moins un Peuple Animal Sauvage (M, R ou O) joue : Piste des Gardiens à 6 icônes avec Résonance en 6e position, 2 encoches visibles par Gardien, paris 0/1/2 Défenseurs, passage Face 2 et fin anticipée par Éveil de la Forêt."
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
        "resume": "Lu uniquement si au moins un Peuple Onirique (H ou E) joue : pose de Rêves sur la Réglette depuis la droite, défense en 1re et 2e pose, annulation choisie par le propriétaire du Rêve, glissements avec Défenseurs solidaires et fin anticipée par Sommeil du Contremaître (impossible si un Rêve est enraciné)."
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
          "deviation_reglette": {
            "nom": "Déviation de dé (±1)",
            "fenetre": "OUVERTURE",
            "texte": "À l'ouverture des paravents, défaussez 1 Insecte posé sur un rang de la Réglette pour décaler le dé d'une machine de −1 ou +1 rang (entre 1 et 6), en allumant l'icône Insecte puis balayage."
          },
          "bouclier_de_lisiere": {
            "nom": "Bouclier de lisière (facultatif)",
            "fenetre": "FIN_ATTAQUES",
            "gouverneur": "I",
            "facultatif": true,
            "texte": "En fin d'attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur Insectes choisit de défausser ou non 1 Insecte pour maintenir le Gardien en piste sur sa face actuelle (le pari reste perdu)."
          }
        },
        "resume": "Lu uniquement si les Insectes (I) jouent : jetons Insectes exclusifs aux 10 tuiles des 5 lisières de I (laissés dans la boîte sans I, Production/Migration ignorées et icône Insecte inactive), Production des Nids (+1/+2), Migration radiale et vers les pistes centrales, déviation ±1, Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage de tout Insecte passager non dépensé."
      }
    }
  },
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve, Nid) est gouvernée exclusivement par le joueur de son Peuple d'origine ; la pose d'un Piège gagné en Furtivité est choisie par le propriétaire du rayon ; le Bouclier de lisière est facultatif et gouverné par le joueur Insectes (I). Zéro vote de groupe.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés. Tous les joueurs lancent leurs dés (même sur Sabotage ou Écaille, jet ignoré) afin d'éliminer toute fuite sonore.",
    "pont_routier_routes_forestieres": "Une parcelle désigne toujours une case de forêt non devenue Route Forestière. Le long d'un rayon, les Routes Forestières sont sautées radialement et infranchissables latéralement. Dès qu'un rayon est 100 % Routes Forestières, sa zone de Furtivité est fermée.",
    "zero_ecrasement_et_zero_dette": "Zéro écrasement au contact hors Route : déplacer une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d'une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve). Zéro dette mémorielle : tout état est porté par une pièce physique ; tout Piège ordinaire est autonome (SINGLE_STRIKE, max 1 par parcelle ; le Croc peut cohabiter et pare en premier).",
    "cascades_gardiens_6_icones": "On résout intégralement l'action ou la tuile en cours avant de balayer la Piste des Gardiens de gauche à droite sur les 6 icônes dédiées : [PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE]. Partition stricte « 1 événement = au plus 1 icône » ; Résonance en 6e position compte individuellement chaque 1re activation d'un autre Gardien du tour sans écrasement de bit, et le balayage gauche → droite reprend si un effet rallume une icône située plus à gauche."
  },
  "etapes_tour": [
    {
      "numero": 1,
      "code": "PREPARATION_ET_DES_SECRETS",
      "nom": "Bandelette d'Acte, Pioche au sac opaque et Dés secrets universels",
      "regles": [
        "Réglette fixe 1–6 à bandelette d'Acte réversible : Acte 1 (Tours 1–4, Face A) place les rangs 1–3 en Mode Charge et 4–6 en Mode Assaut. Au début du Tour 5, retournez uniquement la bandelette d'Acte sur Face B (Acte 2, Tours 5–8) : 1–3 en Mode Assaut et 4–6 en Mode Charge, sans déplacer ni Rêves ni Insectes. Actions fixes : 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (Sur place + Devant, avancée +1, Seuil −1).",
        "Départ décalé canonique (P4_2233, dotation finie 10×N pions Arbre/Souche recto-verso) : Bulldozer en parcelle 1, Abatteuse en parcelle 2 sur chaque rayon.",
        "Pioche au sac opaque : chaque joueur pioche secrètement 1 jeton (2N jetons Machine épais + Sabotages ordinaires + jusqu'à 4 Écailles). Les jetons non piochés restent cachés sans être consultés. En cas de pénurie, distribution horaire depuis le Coordonnateur, Oiseau toujours servi en dernier (regarde jusqu'à 2 jetons, garde 1 et pose l'autre face cachée sur son Perchoir à plat).",
        "Lancer de dés universel sous paravent fermé : tous les joueurs lancent leurs dés (2 dés standards + Dé d'Envol 1–6 chez O sur mini-paravent gradué 1–6), même sur Sabotage ou Écaille (jet ignoré), éliminant toute fuite sonore."
      ]
    },
    {
      "numero": 2,
      "code": "POSE_DES_DEFENSEURS",
      "nom": "Pose des 2 Défenseurs recto-verso, Rêves, Furtivité et Paris Gardiens",
      "regles": [
        "1er temps de pose simultané (directement face Définitif, jamais sur les Gardiens) : parcelle de sa propre Forêt (ou parcelle alliée en repli si aucun emplacement légal ; Tambour H autorisé sur tout rayon), tuile non construite de ses 2 lisières (interdit si impossible à placer), Rêve présent sur la Réglette, ou rive ouverte de Furtivité d'un rayon non 100 % Route.",
        "Furtivité « Chaud vs Calme » par rayon : 2 rives indépendantes de 2 places (Rive Piège et Rive Sabotage) au pied de chaque rayon actif, ouvertes à toute la table en 1er comme en 2e temps.",
        "2e temps de pose global (face Réflexion -> validation irréversible face Définitif) : partout sur le plateau, y compris en pari sur un Gardien construit (0, 1 ou 2 Défenseurs max par Gardien si au moins 1 Animal Sauvage joue). Retourner son 2e pion sur Définitif fige simultanément son jeton Duel ou sa Plume de Vigie ; dès que N−1 joueurs ont validé, le dernier joueur effectue au plus 1 ultime ajustement. Chez H : 2 pions Chamanes (1 Tambour, 1 Chant) rendant le binôme auto-vérifiant."
      ]
    },
    {
      "numero": 3,
      "code": "CONSTRUCTION_ET_REVELATION",
      "nom": "Construction obligatoire, Ouverture des paravents et Rêves",
      "regles": [
        "Construction obligatoire avant l'ouverture des paravents de toute tuile réunissant ses 2 bâtisseurs (interdit si l'emplacement cible est indisponible). Sitôt construite, les 2 bâtisseurs sont couchés « en attente » devant leur propriétaire — sauf à 3 joueurs sur un Gardien ou un Rêve, où 1 bâtisseur rejoint immédiatement une parcelle adjacente.",
        "Nid : posé sur une parcelle libre sans machine ni autre Nid de l'un de ses 2 rayons. Rêve : posé par-dessus le rang libre le plus à droite (6, 5…) de la Réglette fixe sans déplacer les Insectes.",
        "Ouverture des paravents : les jetons Machine révélés restent visibles devant leur rayon jusqu'au verdict de Furtivité (inclinés à 90° s'ils sont annulés). Tout jeton d'Altération sur une machine révélée est retiré : elle compte dans m(r) mais recule d'1 parcelle sans frapper.",
        "Ordre strict d'ouverture : (1) chaque jeton Sabotage/Écaille un par un (allume SABOTAGE + pose Croc sur Écaille + balayage Gardiens) ; (2) chaque déviation d'Insecte ±1 une par une (allume INSECTE + balayage) ; (3) chaque Rêve défendu de gauche à droite : son propriétaire choisit quelle(s) machine(s) du rang sont annulées (y compris déviée), résout intégralement le pouvoir propre du Rêve (actif dès que défendu même à 0 machine, sauf mention « Quand ce Rêve annule… »), puis si ≥ 1 machine a été annulée (déviée ou non), allume REVE + balayage. Les Défenseurs posés sur un Rêve se déplacent toujours avec lui."
      ]
    },
    {
      "numero": 4,
      "code": "FURTIVITE_NIDS_ET_MIGRATION",
      "nom": "Furtivité par rayon, Production des Nids et Migration de l'Essaim",
      "regles": [
        "Furtivité « Chaud vs Calme » : seule une rive portant 2 Défenseurs est évaluée selon m(r) = jetons Machine révélés de r + machines de r en Ratissage (indépendant de déviation ±1, annulation Rêve ou Altération ; Sabotage/Écaille = 0 rayon). Rive Piège gagnée si m(r) == 2 (le propriétaire du rayon r pose 1 Piège sur une parcelle sans Piège ordinaire de r) ; Rive Sabotage gagnée si m(r) == 0 (+1 jeton Sabotage glissé dans le sac sans allumer SABOTAGE).",
        "Module Essaim (uniquement si I joue) — Production des Nids : chaque Nid défendu crée +1 Insecte (0–1 présent) ou +2 Insectes (≥ 2 présents) sans allumer INSECTE, puis applique son pouvoir après production, puis balayage Gardiens.",
        "Module Essaim (uniquement si I joue) — Migration : résolue rayon par rayon, chaque Insecte se déplace de 0 ou 1 cran dans les deux sens le long de son rayon (en sautant les Routes) ou depuis la dernière parcelle vers un rang 1–6 de la Réglette ou une icône de la Piste des Gardiens (suivi par retournement puis redressement)."
      ]
    },
    {
      "numero": 5,
      "code": "ATTAQUES_ET_TEST_FIN",
      "nom": "Attaques des Machines, Encoches Gardiens et Verdict de fin",
      "regles": [
        "Ordre de passage : rangs 1 à 6 de la Réglette puis machines en Ratissage (Assaut permanent, immobiles, mais leur parcelle compte comme parcelle ciblée tant qu'elles n'ont pas frappé). Abatteuse avant Bulldozer sur un même rayon.",
        "Parcelles ciblées figées au début de l'activation (toute cible devenue Route entre-temps est annulée sans report). Seuil de Parade = chiffre gravé + rouges (en Assaut et Ratissage uniquement ; ignorés en Charge) − bleus Surchauffe (actifs dans TOUS les modes : Charge, Assaut et Ratissage) − 1 aux rangs 3 et 6, minimum 1.",
        "Chaîne des parades : Croc Reptile (s'il cohabite, pare en premier, allume PIEGEAGE et retourne en réserve R) -> Piège ordinaire autonome SINGLE_STRIKE (pare 1 frappe même à 0 Défenseur/Insecte, allume PIEGEAGE et est défaussé) -> Parade classique (Défenseurs seuls -> PARADE ; avec défausse immédiate d'Insectes -> INSECTE).",
        "Frappe non parée : Abatteuse retourne tous les Arbres debout en Souches sans toucher aux Souches ; Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches. En Mode Charge : +1 jeton rouge max/activation dès qu'au moins 1 frappe réelle non-Route n'est ni parée ni piégée. En création de Route (0 Arbre, 0 Souche) : la case est vidée (Nid en lisière, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve) ; si la poussée de bordure déplace déjà la machine d'1 parcelle vers le cœur, elle couvre et remplace l'avancée finale de En avançant (jamais de double bond +2).",
        "Verdict des Gardiens (2 encoches visibles) : ≥ 1 pion encore sur la tuile = pari perdu (retour lisière Face 1, sauf choix facultatif de I de défausser 1 Insecte en Bouclier de lisière pour la maintenir sur sa face actuelle) ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche occupée = aucune mise (reste en place sans évoluer).",
        "Vérification de fin : priorité absolue au Tour 8 ; aux Tours 1–7, Sommeil du Contremaître (tous les Rêves en bloc contigu 1..k, impossible si un Rêve est enraciné) ou Éveil de la Forêt (tous les N 2es pions engagés sur les Gardiens et tous les paris gagnés). Au décompte final : application des tuiles enracinées (1 Souche en F1/unique, 2 en F2 retournées en Arbres debout) puis décompte des Arbres debout."
      ]
    },
    {
      "numero": 6,
      "code": "MENAGE_FIN_DE_TOUR",
      "nom": "Enracinement volontaire, Ratissage physique et Ménage",
      "regles": [
        "Retour en main des Défenseurs (y compris depuis les encoches et en attente), descente sur place de tout Insecte passager non dépensé, et remise à zéro des états transitoires.",
        "Enracinement volontaire (avant remise au sac) : chaque joueur peut enraciner au plus 1 tuile construite de son Peuple au pied de son rayon face à une parcelle (1 Souche en F1/unique ou 2 en F2 au décompte final ; un Rêve enraciné rend le Sommeil impossible).",
        "Passage en Ratissage : toute machine terminant sur la dernière parcelle de son rayon glisse son jeton Machine sous elle (hors sac), conserve tous ses jetons Puissance antérieurs et gagne +1 jeton rouge physique (convertible en bleu ; 0 bonus imprimé).",
        "Remise au sac opaque de tous les jetons révélés et du jeton du Perchoir, passage du pion Coordonnateur au siège suivant et avancée du marqueur de Tour."
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
    "A01": "Lancer de dés universel sous paravent fermé : tous les joueurs lancent leurs dés (2 dés standards + Dé d'Envol 1–6 chez O sur mini-paravent gradué 1–6), même sur Sabotage ou Écaille (jet ignoré), éliminant toute fuite sonore.",
    "A02": "Défenseurs recto-verso (Réflexion/Définitif) et clôture à N−1 : 1er pion posé directement face Définitif (jamais sur les Gardiens ; ouvert aux Rêves et à la Furtivité) ; 2e pion posé face Réflexion puis validé irréversiblement sur Définitif (figeant Duel/Plume ; à N−1 validés, au plus 1 ultime ajustement pour le dernier joueur) ; chez H, 2 Chamanes uniques (Tambour, Chant).",
    "A03": "Furtivité « Chaud vs Calme » par rayon : 2 rives indépendantes de 2 places (Rive Piège et Rive Sabotage) par rayon actif. Les jetons Machine révélés restent visibles devant leur rayon jusqu'au verdict (inclinés à 90° si annulés). m(r) = jetons Machine révélés de r + Ratissages de r (inclut Altération ; indépendant de déviation ±1 et annulation Rêve ; Sabotage/Écaille = 0).",
    "A04": "Gouvernance unitaire : chaque Tuile de Synergie est décidée par son Peuple d'origine ; la pose de Piège en Furtivité par le propriétaire du rayon ; le Bouclier de lisière facultatif par le joueur Insectes (I).",
    "A05": "Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; zéro Insecte réservé d'avance.",
    "A06": "Pièges autonomes SINGLE_STRIKE & Croc : max 1 Piège ordinaire par parcelle (pare 1 frappe même à 0 Défenseur/Insecte, allume PIEGEAGE, défaussé aussitôt) ; le Croc Reptile peut cohabiter, pare en premier puis retourne dans la réserve Reptile.",
    "A07": "Zéro verrouillage d'avance : tant qu'un Insecte ou un Piège est sur le plateau, il reste librement utilisable.",
    "A08": "Pont routier : une parcelle est une case non-Route ; les Routes Forestières sont sautées radialement et infranchissables latéralement.",
    "A09": "Repli sur création de Route et plafond En avançant : recul vers la bordure par défaut, ou d'1 parcelle vers le cœur si la bordure est rasée ; cette poussée vers le cœur couvre et remplace l'avancée finale d'une action En avançant (jamais de double bond +2).",
    "A10": "Dotation finie 10×N recto-verso, départ décalé & Ratissage physique : 10×N pions Arbre/Souche sans réserve illimitée ; Bulldozer p=1 / Abatteuse p=2 ; Abatteuse retourne tous les Arbres sans toucher aux Souches ; au ménage, toute machine sur la dernière parcelle glisse son jeton Machine sous elle (hors sac), conserve ses jetons Puissance et gagne +1 jeton rouge physique (convertible en bleu ; 0 bonus imprimé ; immobile mais parcelle ciblée).",
    "A11": "Réglette fixe 1–6 et bandelette d'Acte réversible : bandelette retournée seule au début du Tour 5 sans déplacer ni Rêves ni Insectes ; un Rêve construit se pose au-dessus du rang libre le plus à droite (6, 5…).",
    "A12": "Piste des Gardiens à 6 icônes (Résonance en 6e position) : [PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE], sans numéros visibles ; compteur individuel sans écrasement sur Résonance et reprise du balayage gauche → droite si une icône plus à gauche se rallume.",
    "A13": "Deux encoches visibles par Gardien et Faces 2 autonomes : ≥ 1 pion encore sur la tuile = pari perdu ; 0 pion dessus et ≥ 1 encoche occupée = pari gagné (passage Face 2) ; 0 pion dessus et 0 encoche = aucune mise (reste en place sans évoluer).",
    "A14": "Éveil de la Forêt 100 % Piste des Gardiens (Module Gardiens) : actif si ≥ 1 Animal Sauvage (M/R/O) joue, aux Tours 1–7 (priorité Tour 8), si tous les N 2es pions ont été engagés sur les Gardiens et tous les paris sont gagnés (un Gardien maintenu par Bouclier de lisière reste pari PERDU).",
    "A15": "Fins de partie & Enracinement volontaire : priorité absolue Tour 8 ; Tours 1–7 Sommeil (tous les Rêves en bloc contigu 1..k, impossible si un Rêve est enraciné) ou Éveil ; au décompte final, chaque tuile enracinée face à une parcelle non-Route y retourne 1 Souche (F1/unique) ou 2 Souches (F2) en Arbres debout.",
    "A16": "Zéro écrasement au contact hors Route : le déplacement d'une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d'une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve).",
    "A17": "Module Essaim clos sur I : jetons Insectes exclusifs aux 10 tuiles des 5 lisières de I (laissés dans la boîte sans I). Quand I joue : Migration radiale dans les deux sens et vers les pistes centrales, déviation ±1, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d'un Insecte passager non dépensé.",
    "A18": "Production des Nids (Module Essaim) : bloc indivisible (+1/+2 Insectes sans allumer INSECTE, puis pouvoir après production, puis balayage Gardiens).",
    "A19": "Parcelles ciblées figées au début de l'activation d'une machine : toute cible devenue Route entre-temps est annulée sans report ; une machine en Ratissage rend sa parcelle ciblée tant qu'elle n'a pas frappé ce tour.",
    "A20": "Accessoires 3 + 3 : actifs Tour 1 (H Tambour/Chant, M Duel Défi↔Territoire tenu, O Dé d'Envol/Perchoir/Plume) et progressifs via tuiles (E jeton d'Altération sur machine mobile max 1, R 4 Écailles + Croc réutilisable + max 1 cale G9, I Module Essaim).",
    "A21": "Ouverture stricte & Rêves défendus : Sabotages/Écailles un par un (+ balayage) → déviations ±1 une par une (+ balayage) → Rêves défendus de gauche à droite : le propriétaire choisit quelle(s) machine(s) du rang sont annulées (y compris déviée), résout le pouvoir propre du Rêve (actif dès que défendu même à 0 machine, sauf mention « Quand ce Rêve annule… »), puis allume REVE + balayage si ≥ 1 machine annulée (déviée ou non). Les Défenseurs suivent tout déplacement du Rêve.",
    "A22": "Légalité des poses & Bâtisseurs : interdit de compléter une tuile impossible à placer ; repli 1re pose sur parcelle alliée si aucun emplacement légal ; sitôt construite, les 2 bâtisseurs sont couchés en attente devant leur propriétaire (maintien du bonus 3 joueurs libérant 1 bâtisseur vers une parcelle adjacente sur Gardien/Rêve).",
    "A23": "Seuil de Parade unifié & Gain Charge : en Mode Charge, seuls les jetons rouges sont ignorés ; les jetons bleus Surchauffe (−1) s'appliquent dans TOUS les modes (Charge, Assaut, Ratissage), −1 aux rangs 3 et 6, minimum 1. Gain Charge = +1 rouge max/activation dès qu'au moins 1 frappe réelle non-Route n'est ni parée ni piégée (FRAPPE_NON_PAREE).",
    "A24": "Sac opaque & pénurie : 2N jetons Machine + Sabotages + max 4 Écailles dans un sac en tissu opaque ; non piochés cachés ; pénurie distribuée en sens horaire depuis le Coordonnateur avec Oiseau toujours servi en dernier.",
    "A25": "Séquence des attaques : rangs 1..6 de la Réglette puis machines en Ratissage (Assaut permanent) ; Abatteuse avant Bulldozer sur un même rayon ; chaque machine résolue d'un seul tenant."
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
  ]
};
