// =========================================================================
// data/amazonia_data_v6_0.js — Données canoniques Amazonia v6.0-alpha (Expérimental · 6 profils · 192 châssis · 32 emplacements)
// =========================================================================
const PEUPLES = {
  "M": {
    "code": "M",
    "nom": "Mammifères",
    "famille": "Animal Sauvage (Gardien)",
    "badge": "bg-amber-100 text-amber-900 border-amber-300",
    "icon": "🐆"
  },
  "R": {
    "code": "R",
    "nom": "Reptiles",
    "famille": "Animal Sauvage (Gardien)",
    "badge": "bg-emerald-100 text-emerald-900 border-emerald-300",
    "icon": "🐍"
  },
  "O": {
    "code": "O",
    "nom": "Oiseaux",
    "famille": "Animal Sauvage (Gardien)",
    "badge": "bg-sky-100 text-sky-900 border-sky-300",
    "icon": "🦜"
  },
  "H": {
    "code": "H",
    "nom": "Humains",
    "famille": "Onirique (Rêve)",
    "badge": "bg-rose-100 text-rose-900 border-rose-300",
    "icon": "🏹"
  },
  "E": {
    "code": "E",
    "nom": "Entités Magiques",
    "famille": "Onirique (Rêve)",
    "badge": "bg-purple-100 text-purple-900 border-purple-300",
    "icon": "✨"
  },
  "I": {
    "code": "I",
    "nom": "Insectes",
    "famille": "Symbiotique (Croissance)",
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
    "p_max": 4,
    "dotation": [
      2,
      2,
      3,
      3
    ],
    "somme": 10,
    "label": "P4_2233 : 4 parcelles [2,2,3,3] (10N Arbres · Standard)",
    "code": "P4_2233",
    "arbres_par_rayon": 10
  },
  "P4_2223": {
    "p_max": 4,
    "dotation": [
      2,
      2,
      2,
      3
    ],
    "somme": 9,
    "label": "P4_2223 : 4 parcelles [2,2,2,3] (9N Arbres)",
    "code": "P4_2223",
    "arbres_par_rayon": 9
  },
  "P4_1223": {
    "p_max": 4,
    "dotation": [
      1,
      2,
      2,
      3
    ],
    "somme": 8,
    "label": "P4_1223 : 4 parcelles [1,2,2,3] (8N Arbres)",
    "code": "P4_1223",
    "arbres_par_rayon": 8
  },
  "P5_22233": {
    "p_max": 5,
    "dotation": [
      2,
      2,
      2,
      3,
      3
    ],
    "somme": 12,
    "label": "P5_22233 : 5 parcelles [2,2,2,3,3] (12N Arbres)",
    "code": "P5_22233",
    "arbres_par_rayon": 12
  },
  "P5_22223": {
    "p_max": 5,
    "dotation": [
      2,
      2,
      2,
      2,
      3
    ],
    "somme": 11,
    "label": "P5_22223 : 5 parcelles [2,2,2,2,3] (11N Arbres)",
    "code": "P5_22223",
    "arbres_par_rayon": 11
  },
  "P5_12223": {
    "p_max": 5,
    "dotation": [
      1,
      2,
      2,
      2,
      3
    ],
    "somme": 10,
    "label": "P5_12223 : 5 parcelles [1,2,2,2,3] (10N Arbres)",
    "code": "P5_12223",
    "arbres_par_rayon": 10
  }
};

const CHASSIS_AXES_SPEC = [
  {
    "key": "Profil_Piste",
    "num": 1,
    "label": "1. Profil de Piste & Dotation Seuil Imprimé",
    "defaultVal": "P4_2233",
    "options": [
      {
        "val": "P4_2233",
        "text": "P4_2233 : 4 parcelles [2,2,3,3] (10N Arbres · Standard)"
      },
      {
        "val": "P4_2223",
        "text": "P4_2223 : 4 parcelles [2,2,2,3] (9N Arbres)"
      },
      {
        "val": "P4_1223",
        "text": "P4_1223 : 4 parcelles [1,2,2,3] (8N Arbres)"
      },
      {
        "val": "P5_22233",
        "text": "P5_22233 : 5 parcelles [2,2,2,3,3] (12N Arbres)"
      },
      {
        "val": "P5_22223",
        "text": "P5_22223 : 5 parcelles [2,2,2,2,3] (11N Arbres)"
      },
      {
        "val": "P5_12223",
        "text": "P5_12223 : 5 parcelles [1,2,2,2,3] (10N Arbres)"
      }
    ]
  },
  {
    "key": "Regle_Ouverture_Reve_Multiple",
    "num": 2,
    "label": "2. Ouverture multiple d’un Rêve (3.2)",
    "defaultVal": "UNIQUE_PAR_TOUR",
    "options": [
      {
        "val": "UNIQUE_PAR_TOUR",
        "text": "Unique par tour (1 ouverture max/tour)"
      },
      {
        "val": "PAR_DE_M_DESIGNE",
        "text": "Cumulatif (1 ouverture par dé M désigné)"
      }
    ]
  },
  {
    "key": "Offset_Seuil_Parade",
    "num": 3,
    "label": "3. Décalage du Seuil de Parade",
    "defaultVal": 0,
    "options": [
      {
        "val": 0,
        "text": "Offset 0 (Défense ≥ Seuil Imprimé modifié)"
      },
      {
        "val": 1,
        "text": "Offset +1 (Exige +1 Défenseur de plus)"
      }
    ]
  },
  {
    "key": "Placement_Initial_Machines",
    "num": 5,
    "label": "5. Placement initial des Machines",
    "defaultVal": "MEME_PARCELLE_P1",
    "options": [
      {
        "val": "MEME_PARCELLE_P1",
        "text": "Standard : Abatteuse et Bulldozer en p=1"
      },
      {
        "val": "BULLDOZER_P1_ABATTEUSE_P2",
        "text": "Échelonné : Bulldozer en p=1, Abatteuse en p=2"
      }
    ]
  },
  {
    "key": "Role_Abatteuse_Fin_De_Piste",
    "num": 6,
    "label": "6. Rôle de l’Abatteuse en Ratissage",
    "defaultVal": "STANDARD_COUPE_ARBRE",
    "options": [
      {
        "val": "STANDARD_COUPE_ARBRE",
        "text": "Standard (Coupe uniquement les Arbres)"
      },
      {
        "val": "ARRACHE_1_SOUCHE_SI_SANS_ARBRE",
        "text": "Arrache 1 Souche s’il n’y a plus d’Arbre"
      }
    ]
  },
  {
    "key": "Synergie_Binome_Machines",
    "num": 7,
    "label": "7. Puissance du binôme de machines",
    "defaultVal": "INDIVIDUELLE",
    "options": [
      {
        "val": "INDIVIDUELLE",
        "text": "Individuelle (Propre à chaque machine)"
      },
      {
        "val": "MUTUALISATION_PUISSANCE_MEME_PARCELLE",
        "text": "Mutualisée sur une même parcelle"
      }
    ]
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
        "fenetre": "OUVERTURE",
        "primitive": "MOD_PUISSANCE",
        "tags": [
          "SURCHAUFFE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Retournez 1 jeton Puissance rouge d’une machine sur sa face bleue <em>Surchauffe</em>.<br><strong>Face 2 :</strong> Retournez jusqu’à 2 jetons rouges en bleus <em>Surchauffe</em> (répartis librement entre des machines).",
        "temoin": "En Face 2, permet de retourner au plus 2 jetons rouges au total, répartis librement entre une ou deux machines."
      },
      "B": {
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
        "fenetre": "OUVERTURE / LOI 5",
        "primitive": "MOD_SEUIL + MOD_PUISSANCE",
        "tags": [
          "SURCHAUFFE",
          "PARADE_AUTO"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Réduisez de -2 le Seuil de Parade d’une machine portant au moins 1 jeton Puissance (rouge ou bleu) pour le reste du tour.<br><strong>Face 2 (Loi 5) :</strong> Dès qu’une machine porte ≥ 2 jetons bleus (<em>Surchauffe</em>) au moment de frapper, défaussez 2 bleus pour <strong>parer automatiquement toutes ses frappes encore à résoudre</strong> et la faire reculer immédiatement d’1 parcelle non rasée vers la bordure au lieu de son avancée (si elle n’est pas en Ratissage).",
        "temoin": "1er maillon de la chaîne des parades (avant Harpie et Piège) : consomme automatiquement 2 bleus, allume 1. Parade et laisse un éventuel Piège intact (non déclenché)."
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
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (MACHINE)",
        "tags": [
          "RECUL"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Ratissage située sur une parcelle avec au moins 1 Défenseur.<br><strong>Face 2 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure n’importe quelle machine non en Ratissage.",
        "temoin": "Saute les Routes Forestières (et détruit par contact un éventuel Nid non protégé à l’arrivée). Les cibles de la machine se liront depuis sa nouvelle position réelle à l’instant où elle attaque."
      },
      "B": {
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
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_MACHINE_PAREE_SANS_ELAN)",
        "tags": [
          "PARADE_TOTALE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas</strong> sur T3/T6.<br><strong>Face 2 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas ET ne gagne pas de jeton Puissance rouge</strong> sur T3 à T6 (y compris en Ratissage).",
        "temoin": "Une frappe annulée sur une parcelle déjà rasée en Route Forestière ne compte pas comme parée pour cette loi."
      },
      "C": {
        "nom": "La fuite sous les feuilles",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (INSECTE TOUS)",
        "tags": [
          "INSECTES",
          "MOBILITE"
        ],
        "requires_options": {},
        "texte": "Vous pouvez déplacer <strong>tous les Insectes</strong> d’une parcelle vers la prochaine parcelle non rasée du même rayon, côté bordure ou côté cœur.",
        "temoin": "3 Insectes en p=1, Route en p=2, Nid en p=3 : les 3 arrivent ensemble en p=3 sans allumer la case 6 (tous les Insectes présents sur la roue sont libres)."
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (DEFENSEUR)",
        "tags": [
          "MOBILITE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Déplacez 1 Défenseur (y compris un constructeur resté en bordure de lisière en 3.1) vers une parcelle Forêt non rasée adjacente.",
        "temoin": "Un constructeur en bordure peut rejoindre p=1 d’un rayon bordant sa lisière."
      },
      "B": {
        "nom": "La Voltige de l’Atèle",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 4.1 -> 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_FURTIVITE_GLISSE_EN_FORET_ETAPE_5)",
        "tags": [
          "FURTIVITE",
          "ARMEMENT",
          "MOBILITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.1 :</strong> Une fois par tour, après l’action d’un binôme sur l’une des lisières de M ou O, 1 de ses Défenseurs glisse gratuitement sur une parcelle Forêt non rasée adjacente en face pour l’Étape 5.",
        "temoin": "Idéal pour agir en Furtivité en 4.1 puis armer un Piège Embuscade en Forêt à l’Étape 5."
      },
      "C": {
        "nom": "Le passage des singes-lianes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (TRAVERSEE M<->O)",
        "tags": [
          "MOBILITE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Vous pouvez faire passer un Défenseur du rayon des Mammifères à celui des Oiseaux, ou inversement, à la même profondeur. Les deux parcelles doivent être non rasées.",
        "temoin": "Une Parade chez M ouvre G3 C : un Défenseur ayant paré traverse chez O à même profondeur. La première Parade reste acquise."
      },
      "D": {
        "nom": "Les sentinelles des lianes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (FURTIVITE -> PARCELLE_PIEGEE)",
        "tags": [
          "ARMEMENT",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "Vous pouvez déplacer un Défenseur d’une case Furtivité vers une parcelle piégée des Mammifères ou des Oiseaux qui lui fait face.",
        "temoin": "Un binôme a agi en Furtivité face à M p=2 piégée : à l’ouverture, 1 Défenseur rejoint M p=2 pour armer l’Embuscade."
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
        "cycle": "SACRIFICE_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE / SACRIFICE 3.2",
        "primitive": "MOD_SEUIL / DEPLACEMENT",
        "tags": [
          "REDEPLOIEMENT"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Ouverture) :</strong> Réduisez de −1 le Seuil de Parade sur une parcelle des rayons O ou M pour le reste du tour.<br><strong>Sacrifice (en 3.2 après révélation) :</strong> Déplacez jusqu’à 2 Défenseurs vers des parcelles ciblées et renvoyez ce Gardien sur sa Face 1 en lisière (sa case est immédiatement libérée).",
        "temoin": "Le renvoi en lisière libère la case Gardien pour une future construction ; le Gardien repasse Face 1 et perd son marqueur « utilisé »."
      },
      "B": {
        "nom": "Le Cri d’Alarme de l’Ara",
        "cycle": "SACRIFICE_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 2.1 / SACRIFICE DÉBUT 2",
        "primitive": "MOD_LOI_DU_COEUR + PARTAGE_INFO",
        "tags": [
          "INFORMATION",
          "PORTÉE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Loi 2.1) :</strong> Le peuple d’origine (O) et son voisin (M) posent leur 1er Défenseur à portée globale.<br><strong>Sacrifice (Début Étape 2) :</strong> Ouvrez tous les mini-paravents <strong>avant</strong> de placer les Défenseurs ce tour-ci (renvoyez G4 en lisière ; il perd son marqueur « utilisé »).",
        "temoin": "Offre une visibilité publique complète des cartes et dés, mais la pose reste individuelle et sans concertation orale."
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
        "fenetre": "OUVERTURE (LOI TEMP 5)",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SOUCHES_REDUISENT_SEUIL)",
        "tags": [
          "SOUCHES"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Désignez 1 parcelle non rasée : pour ce tour, réduisez de <strong>−1</strong> son Seuil de Parade à chaque frappe trouvant au moins 1 Souche sur place à cet instant.<br><strong>Face 2 :</strong> Désignez jusqu’à 2 parcelles non rasées : pour ce tour, réduisez de <strong>−1</strong> leur Seuil de Parade à chaque frappe trouvant au moins 1 Souche sur place à cet instant.",
        "temoin": "Vérification dynamique à chaque frappe : si une Abatteuse crée une Souche sur la parcelle désignée, le Bulldozer suivant subit immédiatement le −1 au Seuil."
      },
      "B": {
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
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SOUCHES_REDUISENT_SEUIL)",
        "tags": [
          "SOUCHES"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Loi 5) :</strong> Sur les rayons R et O, toute parcelle contenant au moins 1 Souche voit son Seuil de Parade réduit de <strong>−1</strong>.<br><strong>Face 2 (Loi 5) :</strong> Sur tout le plateau, toute parcelle contenant au moins 1 Souche voit son Seuil de Parade réduit de <strong>−1</strong>.",
        "temoin": "Vérifié dynamiquement à chaque frappe sur le Seuil Imprimé : dès qu’au moins 1 Souche est présente sur la parcelle à cet instant, le Seuil diminue de −1."
      },
      "C": {
        "nom": "Le Perchoir du caïman",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SOUTIEN_MACHINE_VERS_DEVANT)",
        "tags": [
          "SOUTIEN",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Sur les rayons des Reptiles et des Oiseaux, quand une machine frappe devant elle, chaque Défenseur situé sur la parcelle de la machine apporte aussi +1 point de Défense à la parcelle frappée.",
        "temoin": "Ce point de soutien à distance suffit à armer un Piège Embuscade sur la parcelle devant la machine, même si celle-ci est vide de pion."
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
    "nomBase": "L’Œil Double du Toucan",
    "profils": {
      "A": {
        "nom": "L’Œil Double du Toucan",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE (3.2)",
        "primitive": "PERMUTATION_PISTE (LECTURE_DE_M)",
        "tags": [
          "LECTURE_DE"
        ],
        "requires_options": {},
        "texte": "En 3.2, décalez de -1 ou +1 rang la lecture du dé M d’un joueur sur la Piste des Tactiques.",
        "temoin": "Si ouvert avant 3.2, prépare le décalage pour la révélation du tour courant."
      },
      "B": {
        "nom": "L’Œil Double du Toucan",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 1.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_DE_M_CHOIX_MIN_MAX)",
        "tags": [
          "LECTURE_DE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 1.3 :</strong> Le peuple d’origine (O) et son voisin (R) peuvent retenir le plus grand de leurs deux dés (M = max(D1, D2)) derrière leur paravent.",
        "temoin": "Permet d’aller chercher volontairement les Rêves insérés aux rangs 5 et 6."
      },
      "C": {
        "nom": "Le Vol en ciseaux",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (ECHANGE_ATOMIQUE)",
        "tags": [
          "FURTIVITE",
          "INSECTES",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Vous pouvez échanger simultanément 1 Défenseur d’une parcelle des Oiseaux ou des Reptiles avec 1 Insecte de la case Furtivité qui lui fait face sur leur lisière commune (posez ce Défenseur sur un emplacement valide de la case en tirant l’éventuel autre Défenseur sur son jumeau).",
        "temoin": "Avant 4.1, permet de former et d’orienter un binôme de 2 Défenseurs en Furtivité tout en envoyant l’Insecte défendre la forêt."
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
    "nomBase": "Le Barrage du Capybara",
    "profils": {
      "A": {
        "nom": "Le Barrage du Capybara",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE",
          "SOUCHES"
        ],
        "requires_options": {},
        "texte": "Posez 1 Piège sur une parcelle non rasée contenant au moins 1 Souche et aucun Piège, même occupée par une machine ou ciblée.",
        "temoin": "Fonctionne sur toute la roue dès qu’une Souche est présente."
      },
      "B": {
        "nom": "Le Barrage du Capybara",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 4.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_PIEGE_SOUS_MACHINE_OU_CIBLE)",
        "tags": [
          "POSE",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.1 :</strong> Les binômes en Furtivité peuvent poser un Piège <strong>même sur une parcelle occupée par une machine</strong> (et ce Piège s’arme immédiatement si au moins 1 Défenseur du binôme glisse dessus ou soutient la parcelle).",
        "temoin": "Fait sauter le verrou majeur du minage en Furtivité."
      },
      "C": {
        "nom": "La Loutre géante",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_DEFENSEURS_APRES_PREMIER_DOUBLES)",
        "tags": [
          "PARADE_CLASSIQUE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Sur les rayons des Mammifères et des Humains, chaque Défenseur physiquement présent après le premier apporte <strong>2 points de Défense</strong> (D + max(0, D−1)).",
        "temoin": "2 Défenseurs valent 3 points de Défense, épargnant les Insectes locaux."
      },
      "D": {
        "nom": "Le barrage habité du Capybara",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Vous pouvez poser 1 Piège sur une parcelle non rasée sans Piège des Mammifères ou des Humains contenant au moins 1 Défenseur ou 1 Insecte, même occupée par une machine ou ciblée (allume la case 2).",
        "temoin": "Pose un Piège immédiatement armé par la présence locale (un soutien distant seul ne suffit pas pour la pose)."
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
    "nomBase": "Le Sillage du Boto",
    "profils": {
      "A": {
        "nom": "Le Sillage du Boto",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE (3.2)",
        "primitive": "DEPLACEMENT (CIBLAGE)",
        "tags": [
          "CIBLAGE"
        ],
        "requires_options": {},
        "texte": "En 3.2 (ou à l’ouverture avant l’attaque de la machine), décalez d’1 parcelle non rasée dans le même sens le long de son rayon l’ensemble des frappes d’une machine non en Ratissage pour ce tour, sans déplacer la machine.",
        "temoin": "Saute les Routes Forestières ; le décalage s’applique aux cibles lues depuis la position réelle de la machine à l’instant où elle attaque."
      },
      "B": {
        "nom": "Le Sillage du Boto",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_INVERSION_ETAPE_5_1_ET_5_2)",
        "tags": [
          "ORDRE_MACHINES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Sur 1 rayon au choix par tour, si l’Abatteuse et le Bulldozer sont tous deux actifs, vous pouvez résoudre le <strong>Bulldozer avant l’Abatteuse</strong> (quel que soit leur rang ou en Ratissage).",
        "temoin": "Sur 3 Arbres sans Souche : le Bulldozer coupe 1 Arbre (0 Souche à terrasser), puis l’Abatteuse coupe les 2 Arbres restants en 2 Souches (évite la Route Forestière !)."
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
    "nomBase": "Le Guet du Caïman Noir",
    "profils": {
      "A": {
        "nom": "Le Guet du Caïman Noir",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (SABOTAGE)",
        "tags": [
          "SABOTAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Ajoutez définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de fin de tour).<br><strong>Face 2 :</strong> Ajoutez définitivement 2 cartes Sabotage de la réserve au paquet Machine (mises de côté pour le remélange de fin de tour).",
        "temoin": "Dilue durablement le paquet Machine en réaction à n’importe quel Déclencheur (réserve de cartes Sabotage illimitée)."
      },
      "B": {
        "nom": "Le Guet du Caïman Noir",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 4.1 / LOI 3.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SABOTAGE_ACTIF_ET_REVELATION)",
        "tags": [
          "SABOTAGE",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Loi 4.1) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Ratissage</strong>.<br><strong>Face 2 (Loi 4.1 & 3.2) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Ratissage</strong> ; de plus, en 3.2, chaque carte Sabotage révélée derrière un paravent allume la <strong>case 3. Sabotage</strong> et retire <strong>1 jeton Puissance rouge</strong> d’une machine sur les rayons R ou H.",
        "temoin": "En Face 2, chaque panne tirée en 3.2 déclenche une cascade sur la case 3 (une seule activation max du Gardien câblé en 3) et affaiblit les machines sur R/H avant que la carte Sabotage ne soit remélangée en 6.3."
      },
      "C": {
        "nom": "La Peau de boue",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_ROUGES_IGNORES_DEVANT)",
        "tags": [
          "PARADE_CLASSIQUE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Sur les rayons des Reptiles et des Humains, ignorez tous les jetons Puissance rouges d’une machine quand elle frappe la parcelle située devant elle.",
        "temoin": "Une machine T6 avec 2 rouges et 1 bleu frappant devant elle sur base 3 a un seuil de 3 + 0 - 1 - 2 = 1."
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
    "nomBase": "La Brume de la Dendrobate",
    "profils": {
      "A": {
        "nom": "La Brume de la Dendrobate",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE (6.1)",
        "primitive": "MOD_APPRENTISSAGE",
        "tags": [
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "En 6.1 ce tour-ci, retirez 1 jeton Apprentissage à la tuile Tactique de votre choix.",
        "temoin": "Mémorisé jusqu’en 6.1 et appliqué avant les Insectes Bug (permettant d’épargner un Bug si la Tactique tombe à 0 jeton)."
      },
      "B": {
        "nom": "La Brume de la Dendrobate",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5.3",
        "primitive": "MOD_LOI_DU_COEUR + MOD_PUISSANCE",
        "tags": [
          "DECLENCHEMENT_EFFECTIF",
          "SURCHAUFFE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5.3 :</strong> À la fin des attaques, chaque Piège déclenché ce tour-ci retire 1 jeton Puissance rouge (ou retourne 1 rouge en bleu) sur chaque machine dont il a paré au moins une frappe.",
        "temoin": "S’applique en 5.3 avant le retrait des Pièges déclenchés, une fois par couple Piège–machine parée."
      },
      "C": {
        "nom": "La Rainette géante",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          6
        ],
        "fenetre": "OUVERTURE (CASE 6)",
        "primitive": "CREATION_ENTITE (SABOTAGE) avec coût",
        "tags": [
          "CONVERSION",
          "SABOTAGE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<em>(Câblage obligatoire sur 6. Insecte)</em> À l’ouverture, vous pouvez défausser 1 Insecte d’une parcelle Forêt pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (allume la case 3).",
        "temoin": "En 4.2, l’Insecte produit par un Nid peut payer ce coût après le bloc indivisible du Nid pour diluer durablement le paquet Machine."
      },
      "D": {
        "nom": "Les éclaireurs de la Dendrobate",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI APRÈS PARADE PIÈGE",
        "primitive": "MOD_LOI_DU_COEUR (LOI_EMBUSCADE_CREE_SENTINELLE)",
        "tags": [
          "ARMEMENT",
          "REACTION",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi :</strong> Une fois par tour, après une Parade par un Piège sur les rayons des Reptiles ou des Entités, vous pouvez créer 1 Insecte sur une <strong>autre</strong> parcelle piégée de ces deux rayons (allume la case 6).",
        "temoin": "Une première Embuscade réussie crée la sentinelle qui arme immédiatement une seconde Embuscade."
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
    "nomBase": "La Piquée de la Harpie",
    "profils": {
      "A": {
        "nom": "La Piquée de la Harpie",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "MOD_SEUIL",
        "tags": [
          "PARADE_CLASSIQUE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 :</strong> Réduisez de -1 le Seuil de Parade sur une parcelle (-2 s’il s’y trouve ≥ 2 Défenseurs).<br><strong>Face 2 :</strong> Parez automatiquement 1 attaque sur une parcelle contenant ≥ 2 Défenseurs.",
        "temoin": "2e maillon de la chaîne des parades (après Jaguar, avant Piège) : pare la frappe sans déclencher un éventuel Piège présent."
      },
      "B": {
        "nom": "La Piquée de la Harpie",
        "cycle": "DOUBLE_FACE_UPGRADE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SOUTIEN_LISIERE_DEFENSE)",
        "tags": [
          "SOUTIEN",
          "ARMEMENT",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (Loi 5) :</strong> Tout Défenseur isolé sur une case Furtivité ajoute +1 en Défense aux deux parcelles Forêt non rasées en face (même profondeur p).<br><strong>Face 2 (Loi 5) :</strong> Tout Défenseur isolé sur une case Furtivité ajoute +1 en Défense aux deux parcelles Forêt non rasées en face (même profondeur p), et chaque Défenseur constructeur resté en bordure de lisière ajoute +1 en Défense aux parcelles p=1 non rasées adjacentes.",
        "temoin": "Fournit un soutien à distance capable d’armer les Pièges Embuscade en face."
      },
      "C": {
        "nom": "L’Oiseau indicateur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 2.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_DEFENSEUR_1_CASE_INSECTE)",
        "tags": [
          "FURTIVITE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 2.1 :</strong> Tout Peuple autour de la table peut poser son Premier Défenseur sur une case Furtivité de la lisière Oiseaux–Humains qui contient déjà au moins 1 Insecte.",
        "temoin": "Offre un point d’ancrage global dès 2.1 (le Défenseur se pose sur l’un des 4 emplacements valides de la case)."
      },
      "D": {
        "nom": "La veille de la Harpie",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_FURTIVITE_ARME_PIEGES)",
        "tags": [
          "SOUTIEN",
          "ARMEMENT",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Chaque case Furtivité contenant au moins 1 Défenseur (isolé ou en binôme) fournit au total 1 point de Défense aux parcelles <strong>piégées</strong> des Oiseaux ou des Humains qui lui font face.",
        "temoin": "Permet à un binôme de travailler en Furtivité en 4.1 tout en armant à distance les Pièges en face à l’Étape 5."
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "PERMUTATION_PISTE (REVE)",
        "tags": [
          "AVANCEE_REVE"
        ],
        "requires_options": {},
        "texte": "Faites avancer d’1 rang vers la gauche une tuile Rêve de la Piste des Tactiques (en poussant d’un cran tout bloc contigu de Rêves, sans activer son effet).",
        "temoin": "Si l’échange regroupe ainsi en bloc à gauche toutes les tuiles Rêves en jeu (rangs 1..k), le Sommeil du Contremaître sera validé lors de la vérification de fin de partie en 5.3."
      },
      "B": {
        "nom": "Le Chant de l’Ibijau",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN",
        "tags": [
          "RESONANCE"
        ],
        "requires_options": {},
        "texte": "Retournez gratuitement un autre Gardien évolutif en jeu sur sa Face 2 (ou ouvrez immédiatement le Slot d’un autre Gardien encore disponible ce tour-ci).",
        "temoin": "Ne peut pas retourner gratuitement le cycle nourri de G14 C, mais peut ouvrir son Slot."
      },
      "C": {
        "nom": "Le Vautour-Roi",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          2
        ],
        "fenetre": "OUVERTURE (CASE 2)",
        "primitive": "PERMUTATION_PISTE (REVE) avec coût",
        "tags": [
          "CONVERSION",
          "AVANCEE_REVE"
        ],
        "requires_options": {},
        "texte": "<em>(Câblage obligatoire sur 2. Piégeage)</em> À l’ouverture, vous pouvez retirer de la forêt 1 Piège non déclenché ce tour-ci pour faire avancer d’1 rang vers la gauche le Rêve le plus à gauche.",
        "temoin": "Peut consommer le Piège tout juste posé en 4.1 pour avancer le Rêve le plus à gauche (vers le bloc de Rêves en tête ; victoire vérifiée en fin de 5.3). Un Piège ayant déjà paré ce tour ne peut pas payer ce coût."
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
    "nomBase": "La Brèche du Tamanoir",
    "profils": {
      "A": {
        "nom": "La Brèche du Tamanoir",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (INSECTE)",
        "tags": [
          "INSECTES",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Posez 1 jeton Insecte sur une parcelle non rasée ou une case Furtivité contenant au moins 1 Défenseur.",
        "temoin": "Peut compléter un binôme furtif avant 4.1 ou renforcer une Parade en 5."
      },
      "B": {
        "nom": "La Brèche du Tamanoir",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 3.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_CONSTRUCTION_HYBRIDE_INSECTE)",
        "tags": [
          "INSECTES",
          "CONSTRUCTION"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 3.1 :</strong> Vous pouvez construire une tuile en lisière avec <code>1 Défenseur + 1 Insecte</code> (pris sur une case Furtivité de cette même lisière et défaussé) au lieu de 2 Défenseurs.",
        "temoin": "Accélère considérablement la mise en jeu des Tuiles de Synergie."
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
    "nomBase": "L’Écaille du Téju",
    "profils": {
      "A": {
        "nom": "L’Écaille du Téju",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (PIEGE) avec coût",
        "tags": [
          "CONVERSION",
          "POSE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Défaussez 1 Insecte d’une parcelle Forêt pour poser 1 Piège sur cette parcelle ou une parcelle non rasée adjacente du même rayon sans Piège.",
        "temoin": "Attention : ne défaussez pas le dernier pion qui devait fournir le point de Défense armant ce Piège !"
      },
      "B": {
        "nom": "L’Écaille du Téju",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI DE CONTACT",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NID_INDESTRUCTIBLE_AU_CONTACT)",
        "tags": [
          "CONTACT",
          "NID"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de contact :</strong> Les Nids de Croissance (M) de toute la roue et leurs Insectes sont préservés lorsqu’une machine entre ou recule sur leur parcelle.",
        "temoin": "Protège les Nids et leurs Insectes contre tout mouvement de machine (avancée, recul, repli), mais pas contre la transformation de la parcelle en Route Forestière."
      },
      "C": {
        "nom": "Le ventre plein",
        "cycle": "DOUBLE_FACE_CYCLE",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "CREATION_ENTITE (CYCLE NOURRI)",
        "tags": [
          "POSE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Face 1 (À jeun) :</strong> Défaussez 1 Insecte d’une parcelle du rayon des Reptiles pour retourner ce Gardien sur <em>Rassasié</em>.<br><strong>Face 2 (Rassasié) :</strong> Posez 1 Piège sur une parcelle non rasée des Reptiles sans machine ni Piège, puis retournez ce Gardien sur <em>À jeun</em> (allume la case 2).",
        "temoin": "Cycle fermé à 2 temps : le retournement sur À jeun est acquis avant la cascade de la case 2."
      },
      "D": {
        "nom": "Les porteurs du Téju",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (INSECTE)",
        "tags": [
          "ARMEMENT",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Vous pouvez déplacer 1 Insecte d’une parcelle des Reptiles ou des Insectes vers une autre parcelle piégée du <strong>même rayon</strong>, à toute distance.",
        "temoin": "Envoie une sentinelle armer un Piège en bout de rayon sans consommer le jeton."
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
    "nomBase": "L’Envol du Batará Suiveur",
    "profils": {
      "A": {
        "nom": "L’Envol du Batará Suiveur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "OUVERTURE",
        "primitive": "DEPLACEMENT (MIGRATION DIRECTE)",
        "tags": [
          "INSECTES",
          "MIGRATION"
        ],
        "requires_options": {},
        "texte": "Faites migrer immédiatement 1 Insecte depuis n’importe quelle parcelle ou case Furtivité de la roue vers une case 1..6 d’une piste globale (<code>Bug</code> ou <code>Colonie</code>, aller simple définitif).",
        "temoin": "Permet de coloniser le Cerveau ou les Gardiens sans attendre d’atteindre la dernière parcelle non rasée."
      },
      "B": {
        "nom": "L’Envol du Batará Suiveur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 4.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_AILES_ESSAIM_2_CRANS)",
        "tags": [
          "INSECTES",
          "MOBILITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.3 :</strong> En 4.3, chaque Insecte sur la roue peut se déplacer de <strong>0, 1 ou 2 crans</strong> (au lieu de 0 ou 1).",
        "temoin": "Un Insecte peut traverser une lisière puis entrer sur la forêt voisine dans le même mouvement."
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
    "nomBase": "Le Tambour des Deux Mondes",
    "profils": {
      "A": {
        "nom": "Le Tambour des Deux Mondes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "PERMUTATION_PISTE (TACTIQUE)",
        "tags": [
          "CERVEAU"
        ],
        "requires_options": {},
        "texte": "À l’ouverture en 3.2, avant l’avancée de ce Rêve, échangez deux tuiles Tactique adjacentes sur la piste centrale.",
        "temoin": "Permet de repousser T6 vers la droite pour qu’elle soit éjectée par le prochain Rêve."
      },
      "B": {
        "nom": "Le Tambour des Deux Mondes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 3.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_REVE_DOUBLE_AVANCEE)",
        "tags": [
          "AVANCEE_REVE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 3.2 :</strong> Lorsqu’il s’ouvre en 3.2, ce Rêve avance de <strong>jusqu’à 2 rangs</strong> vers la gauche (plafonné au Rang 1) au lieu d’1.",
        "temoin": "Accélère le regroupement des tuiles Rêves en tête de piste (rangs 1..k) pour déclencher le Sommeil du Contremaître."
      },
      "C": {
        "nom": "La Part rendue à la forêt",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "PERMUTATION_PISTE avec offrande",
        "tags": [
          "CONVERSION",
          "AVANCEE_REVE"
        ],
        "requires_options": {},
        "texte": "À chaque ouverture en 3.2, vous pouvez renvoyer 1 Gardien de la piste vers sa lisière (sur sa Face 1, en retirant son marqueur « utilisé ») pour faire avancer ce Rêve de <strong>jusqu’à 2 rangs</strong> au lieu d’1.",
        "temoin": "Coût volontaire : ne déclenche pas un pouvoir de sacrifice et renvoie le Gardien en lisière Face 1 sans marqueur « utilisé »."
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
        "fenetre": "3.2 -> 6.1",
        "primitive": "MOD_APPRENTISSAGE (-2)",
        "tags": [
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "En 6.1 ce tour-ci, retirez jusqu’à 2 jetons Apprentissage sur la Piste des Tactiques.",
        "temoin": "Appliqué en 6.1 avant les Insectes Bug : permet de provoquer une égalité en tête ou d’épargner un Bug sur une case ramenée à 0."
      },
      "B": {
        "nom": "Le Voile de l’Oubli",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 6.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_PARADE_ANNULE_APPRENTISSAGE)",
        "tags": [
          "PARADE_TOTALE",
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 6.1 :</strong> Une machine dont toutes les frappes sont parées ce tour-ci ne rapporte <strong>aucun jeton Apprentissage</strong> (même via son gain de Puissance T4/T5/T6).",
        "temoin": "Une frappe annulée sur une parcelle déjà rasée en Route Forestière ne compte pas comme parée."
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
        "fenetre": "3.2",
        "primitive": "DEPLACEMENT (2 DEFENSEURS)",
        "tags": [
          "REDEPLOIEMENT",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "À l’ouverture en 3.2, déplacez jusqu’à 2 Défenseurs (y compris des constructeurs restés en lisière en 3.1) vers des parcelles Forêt non rasées.",
        "temoin": "Recycle immédiatement les bâtisseurs après la révélation des cibles."
      },
      "B": {
        "nom": "La Danse des Esprits-Fauves",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 3.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_CONSTRUCTEURS_REJOIGNENT_FORET)",
        "tags": [
          "CONSTRUCTION",
          "MOBILITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 3.1 :</strong> Lors d’une construction (G ou R), le Peuple d’origine de la tuile construite libère <strong>1 des 2 Défenseurs bâtisseurs</strong> vers la 1re parcelle adjacente non rasée de son choix (ou <strong>tous les Défenseurs bâtisseurs à N=3 joueurs</strong>, chacun choisissant sa rive).",
        "temoin": "Prend effet dès la construction de R3 B pour ses propres bâtisseurs (dans la limite des Défenseurs réellement présents)."
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
        "fenetre": "3.2",
        "primitive": "MOD_PUISSANCE (SURCHAUFFE)",
        "tags": [
          "SURCHAUFFE"
        ],
        "requires_options": {},
        "texte": "À l’ouverture en 3.2, retournez 1 jeton Puissance rouge d’une machine sur sa face bleue <em>Surchauffe</em>.",
        "temoin": "Réduit de 2 le seuil brut de la machine dès ce tour."
      },
      "B": {
        "nom": "Le Sommeil de la Pierre-Serpent",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 3.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SABOTAGE_REVELE_PROLIFERE)",
        "tags": [
          "SABOTAGE",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 3.2 :</strong> En 3.2, si au moins 1 Défenseur occupe une case Furtivité et qu’au moins 1 carte Sabotage est révélée à l’ouverture des paravents, ajoutez définitivement <strong>+1 nouvelle carte Sabotage</strong> de la réserve au paquet Machine (sans allumer la case 3).",
        "temoin": "Amplifie boule de neige la dilution du paquet Machine (1 carte bonus max par tour) tant qu’une présence furtive accompagne la révélation d’une panne."
      },
      "C": {
        "nom": "Le Rêve de la seconde rive",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE"
        ],
        "requires_options": {},
        "texte": "Face à une Route Forestière de l’autre rayon sur la lisière Humains–Reptiles, vous pouvez poser 1 Piège sur la parcelle non rasée sans Piège en face, même ne portant que des Souches, ciblée ou occupée par une machine (allume la case 2).",
        "temoin": "Transforme une Route subie sur une rive en protection pour l’autre rive."
      },
      "D": {
        "nom": "Le guetteur de pierre",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "DEPLACEMENT + CREATION_ENTITE (GROUPE)",
        "tags": [
          "POSE",
          "ARMEMENT",
          "FURTIVITE"
        ],
        "requires_options": {},
        "texte": "Vous pouvez déplacer 1 Défenseur d’une case Furtivité vers une parcelle non rasée sans Piège des Humains ou des Reptiles qui lui fait face, et y poser 1 Piège (groupe atomique, allume la case 2).",
        "temoin": "Fournit simultanément le Piège et son Défenseur d’armement avant les cascades de la case 2."
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
        "fenetre": "3.2",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (REACTIVER_GARDIEN)",
        "tags": [
          "RESONANCE"
        ],
        "requires_options": {},
        "texte": "À l’ouverture en 3.2, ouvrez immédiatement un Gardien disponible sur la Piste des Gardiens.",
        "temoin": "Allume aussi le Déclencheur 4 en résonance après l’effet du Gardien."
      },
      "B": {
        "nom": "La Vision des Plumes Claires",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 1.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_DE_M_CHOIX_MIN_MAX)",
        "tags": [
          "LECTURE_DE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 1.3 :</strong> Le peuple d’origine de ce Rêve (H) peut retenir le plus grand de ses deux dés (M = max(D1, D2)) derrière son paravent.",
        "temoin": "Permet aux Humains de cibler délibérément les Rêves en fin de piste."
      },
      "C": {
        "nom": "Le Rêve du nid vide",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE",
          "PARCELLE_VIDE"
        ],
        "requires_options": {},
        "texte": "Vous pouvez poser 1 Piège sur une parcelle ciblée des Humains ou des Oiseaux qui ne contient ni Défenseur, ni Insecte, ni Piège (allume la case 2).",
        "temoin": "Pose un Piège d’urgence sur cible vide : il suffira d’y amener 1 point de Défense (local ou soutenu à distance) avant la frappe pour déclencher l’Embuscade."
      },
      "D": {
        "nom": "Le rêve du veilleur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE (INSECTE)",
        "tags": [
          "ARMEMENT",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Vous pouvez créer 1 Insecte sur une parcelle piégée des Humains ou des Oiseaux (allume la case 6).",
        "temoin": "Arme un Piège déjà en place (attention à ne pas faire partir cet Insecte en 4.3 sans relève)."
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
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE (INSECTE)",
        "tags": [
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Posez 1 Insecte de la réserve sur une parcelle non rasée d’un rayon de cette paire (H ou I).",
        "temoin": "Fournit un Insecte dès l’Étape 3.2 avant l’action des binômes en 4.1."
      },
      "B": {
        "nom": "Le Miel des Ancêtres",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (ACTIVER_NID)",
        "tags": [
          "INSECTES",
          "NID"
        ],
        "requires_options": {},
        "texte": "Déclenchez immédiatement la création de jetons Insecte d’1 Nid en jeu (+1 ou +2 selon les Insectes présents sur sa parcelle à cet instant, même sans Défenseur dessus ; allume la case 6 sans déclencher le pouvoir propre du Nid).",
        "temoin": "Production hors phase restreinte aux seuls jetons Insecte ; l’activation complète du Nid en 4.2 reste disponible."
      },
      "C": {
        "nom": "La Terra Preta",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI REPOUSSE FINALE",
        "primitive": "MOD_LOI_DU_COEUR (LOI_REPOUSSE_DEUX_SOUCHES)",
        "tags": [
          "SOUCHES",
          "REPOUSSE_FINALE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de Repousse finale :</strong> À la fin de la partie, sur chaque parcelle non rasée des Humains ou des Insectes ayant conservé au moins 1 Souche, retournez jusqu’à <strong>2 Souches</strong> en Arbres debout (dans la limite de la dotation initiale de la parcelle).",
        "temoin": "Une parcelle H avec 3 Souches rend 2 Arbres debout au décompte final."
      },
      "D": {
        "nom": "Les chemins du veilleur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 4.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NIDS_DESSERVENT_PIEGES)",
        "tags": [
          "ARMEMENT",
          "RESEAU",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.3 :</strong> En 4.3, chaque Insecte quittant un Nid situé chez les Humains ou les Insectes peut utiliser 1 cran pour rejoindre directement une parcelle piégée du même rayon, à toute distance.",
        "temoin": "Transforme tout Nid H/I en répartiteur direct de sentinelles vers les Pièges."
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
        "fenetre": "3.2",
        "primitive": "DEPLACEMENT (MACHINE)",
        "tags": [
          "RECUL"
        ],
        "requires_options": {},
        "texte": "Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Ratissage située sur les rayons E ou M.",
        "temoin": "Retarde l’entrée en Ratissage et modifie dynamiquement les cibles que cette machine lira à l’Étape 5."
      },
      "B": {
        "nom": "L’Ombre du Maître des Bois",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_ENDIGUEMENT_RATISSAGE)",
        "tags": [
          "LOI_5",
          "RATISSAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 (Endiguement du Ratissage) :</strong> Les machines en <strong>Ratissage</strong> sur les rayons E et M et leurs rayons voisins immédiats subissent -1 à leur Seuil de Parade (annulant le +1 imprimé de la face Ratissage).",
        "temoin": "En mode Ratissage sur E, M ou leurs voisins immédiats, le Seuil de Parade est réduit de -1 (compensant le +1 de puissance imprimé sur la face Ratissage)."
      },
      "C": {
        "nom": "Le bras mort du fleuve",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 4.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_PASSAGE_DIRECT_INSECTES)",
        "tags": [
          "INSECTES",
          "MOBILITE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.3 :</strong> En 4.3, un Insecte peut utiliser son déplacement (1 cran) pour traverser directement entre les rayons des Entités et des Mammifères à la même profondeur.",
        "temoin": "Court-circuite la case Furtivité intermédiaire entre E et M."
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
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE"
        ],
        "requires_options": {},
        "texte": "Posez 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R, même occupée par une machine ou ciblée.",
        "temoin": "Pose un Piège directement sur une cible révélée en 3.2."
      },
      "B": {
        "nom": "Le Mirage du Fleuve-Miroir",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI TERRASSEMENT",
        "primitive": "MOD_LOI_DU_COEUR (LOI_DERNIERE_SOUCHE_INDESTRUCTIBLE)",
        "tags": [
          "SOUCHES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de terrassement (Sanctuarisation) :</strong> Sur les rayons E et R, les Bulldozers laissent <strong>1 Souche</strong> lors du terrassement <strong>uniquement si au moins 1 Défenseur ou 1 Insecte est présent sur la parcelle</strong>.",
        "temoin": "Tant qu’au moins 1 Défenseur ou 1 Insecte tient la parcelle lors de la frappe, un Bulldozer non paré ne peut pas créer de Route Forestière sur E et R."
      },
      "C": {
        "nom": "Le Mapinguari",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 3.2 ANNULATION",
        "primitive": "MOD_LOI_DU_COEUR (LOI_REVE_ANNULE_MACHINE_RECULE)",
        "tags": [
          "RECUL"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 3.2 :</strong> Chaque machine dont ce Rêve annule l’attaque en 3.2 recule immédiatement d’1 parcelle vers la bordure, si elle le peut.",
        "temoin": "S’applique à chaque machine annulée par R8 C, quel que soit le mode d’ouverture des Rêves."
      },
      "D": {
        "nom": "L’appel des berges gardées",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "DEPLACEMENT + MOD_PUISSANCE",
        "tags": [
          "ARMEMENT",
          "SURCHAUFFE"
        ],
        "requires_options": {},
        "texte": "Vous pouvez transférer 1 Défenseur d’une parcelle des Entités ou des Reptiles vers une autre parcelle piégée de ces deux rayons ; puis retourner 1 jeton rouge en bleu sur une machine qui cible la destination.",
        "temoin": "Arme une Embuscade tout en infligeant Surchauffe à la machine menaçante."
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
        "fenetre": "3.2",
        "primitive": "MOD_SEUIL (-2 RAYON)",
        "tags": [
          "PARADE_CLASSIQUE"
        ],
        "requires_options": {},
        "texte": "Réduisez de -2 le Seuil de Parade sur toutes les parcelles d’un rayon au choix pour ce tour.",
        "temoin": "Sécurise tout un rayon soumis à une double frappe."
      },
      "B": {
        "nom": "L’Écho des Voix Célestes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 6.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_EGALITE_FAIT_AVANCER_REVE)",
        "tags": [
          "AVANCEE_REVE",
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 6.2 :</strong> En cas d’égalité en tête de l’Apprentissage à l’Étape 6.2 (y compris égalité générale à 0), c’est ce Rêve qui avance d’1 rang vers la gauche (r → r−1). S’il complète ainsi le bloc de toutes les tuiles Rêves en jeu en tête de piste (rangs 1..k), la fin de partie par Sommeil se déclenche immédiatement (Repousse Finale).",
        "temoin": "Si l’avancée de R9 sur égalité en 6.2 place en bloc toutes les tuiles Rêves en jeu aux premiers rangs à gauche, la fin de partie par Sommeil se déclenche immédiatement avant le ménage."
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
        "fenetre": "3.2",
        "primitive": "MOD_SEUIL (SCALING INSECTES)",
        "tags": [
          "INSECTES",
          "PARADE_CLASSIQUE"
        ],
        "requires_options": {},
        "texte": "Réduisez le Seuil de Parade d’une machine de -1 par Insecte présent sur son rayon (<code>NB_INSECTES_RAYON</code>).",
        "temoin": "Calculé au moment de la résolution de l’ouverture."
      },
      "B": {
        "nom": "La Nuée des Songes",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "PERMUTATION_PISTE avec coût",
        "tags": [
          "CONVERSION",
          "INSECTES",
          "AVANCEE_REVE"
        ],
        "requires_options": {},
        "texte": "<strong>Conversion 3.2 :</strong> À l’ouverture de ce Rêve, vous pouvez défausser 1 Insecte présent sur la roue pour le faire avancer d’1 rang supplémentaire vers la gauche (plafonné au Rang 1).",
        "temoin": "Convertit un Insecte de la roue en 1 rang d’avancée supplémentaire pour R10 vers le bloc de tête (rangs 1..k)."
      },
      "D": {
        "nom": "La relève des lucioles",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "3.2",
        "primitive": "CREATION_ENTITE + DEPLACEMENT (GROUPE)",
        "tags": [
          "POSE",
          "REDEPLOIEMENT",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Vous pouvez poser 1 Piège sur une parcelle sans Piège des Entités ou des Insectes contenant au moins 1 Défenseur et 1 Insecte, puis déplacer 1 Insecte de cette parcelle vers une autre parcelle non rasée du même rayon, à toute distance (groupe atomique, allume la case 2).",
        "temoin": "Le Défenseur reste pour armer le nouveau Piège tandis que l’Insecte est redéployé ailleurs."
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
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "DEPLACEMENT (DEFENSEUR)",
        "tags": [
          "MOBILITE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, déplacez 1 Défenseur présent sur ce Nid vers n’importe quelle autre parcelle Forêt non rasée du plateau.",
        "temoin": "Résolu au sein du bloc indivisible du Nid avant le balayage de la case 6 ; le Défenseur rejoint n’importe quel front pour l’Étape 5."
      },
      "B": {
        "nom": "La Fourmilière Coupe-Feuilles",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_CARAPACES_EPARGNE_INSECTE)",
        "tags": [
          "PARADE_CLASSIQUE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 (Carapaces) :</strong> Une fois par tour, lors d’une Parade classique sur la parcelle de ce Nid à laquelle contribue au moins 1 Défenseur, épargnez 1 des Insectes qui devaient être défaussés immédiatement.",
        "temoin": "Économise immédiatement 1 Insecte au moment de la frappe parée et maintient la masse critique sur le Nid."
      },
      "C": {
        "nom": "La piste des fourmis légionnaires",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "DEPLACEMENT (INSECTE RAYON)",
        "tags": [
          "INSECTES",
          "MOBILITE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Après sa production en 4.2, vous pouvez déplacer 1 Insecte de ce Nid vers toute autre parcelle non rasée de son rayon.",
        "temoin": "Un Insecte envoyé sur la dernière parcelle non rasée en 4.2 peut ensuite migrer vers une piste globale dès 4.3 du même tour !"
      },
      "D": {
        "nom": "Les fourmis sentinelles",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "DEPLACEMENT (2 INSECTES -> PIEGES)",
        "tags": [
          "ARMEMENT",
          "DISPERSION",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, vous pouvez envoyer jusqu’à <strong>2 Insectes</strong> de ce Nid vers des parcelles piégées de son rayon, à toute distance (1 Insecte max par destination).",
        "temoin": "Arme deux Embuscades distinctes sur le rayon tout en laissant le mouvement 4.3 disponible."
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "MOD_PUISSANCE (SURCHAUFFE)",
        "tags": [
          "SURCHAUFFE"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, retournez 1 jeton Puissance rouge d’une machine de ce rayon (ou d’un rayon voisin) sur sa face bleue <em>Surchauffe</em>.",
        "temoin": "Source récurrente de Surchauffe à chaque tour."
      },
      "B": {
        "nom": "La Termitière à Glu",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 4.1",
        "primitive": "MOD_LOI_DU_COEUR (LOI_INSECTE_FURTIF_PERMANENT)",
        "tags": [
          "FURTIVITE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.1 :</strong> Sur les deux lisières qui bordent ce rayon, lorsqu’un binôme est formé par <code>1 Défenseur + 1 Insecte</code>, l’Insecte n’est pas défaussé.",
        "temoin": "L’action du binôme s’oriente sur la rive occupée par le Défenseur, et l’Insecte reste disponible sur la case Furtivité."
      },
      "C": {
        "nom": "La souche creuse",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI CONTACT MACHINE",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NID_CONTACT_SOUCHE)",
        "tags": [
          "CONTACT",
          "SOUCHES",
          "NID"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de contact :</strong> Quand une machine entre sur cette parcelle, ce Nid et ses Insectes survivent au contact si la parcelle porte au moins <strong>1 Souche</strong> à cet instant.",
        "temoin": "Une Abatteuse T3 qui crée 2 Souches devant elle permet au Nid de survivre lors de son avancée immédiate après ses frappes."
      },
      "D": {
        "nom": "La termitière gardée",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI CONTACT MACHINE",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NID_CONTACT_PIEGE_GARDE)",
        "tags": [
          "CONTACT",
          "PRESENCE",
          "NID"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de contact :</strong> Quand une machine entre sur ce Nid, le Nid et ses Insectes survivent au contact si sa parcelle contient 1 Piège ET au moins 1 Défenseur ou 1 Insecte.",
        "temoin": "Comme un Piège déclenché reste en place jusqu’en 5.3, il protège encore le Nid lors de l’avancée immédiate d’une machine T3/T6 parée ! En revanche, si plus aucun Défenseur ni Insecte n’est présent à l’entrée de la machine, le Nid retourne en lisière."
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "DEPLACEMENT (2 INSECTES)",
        "tags": [
          "INSECTES",
          "MOBILITE"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, déplacez immédiatement d’1 cran jusqu’à 2 Insectes présents sur ce Nid (avant l’Étape 4.3).",
        "temoin": "Donne une portée effective de 2 crans aux Insectes produits."
      },
      "B": {
        "nom": "La Branche des Guêpes Cazadores",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 4.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NID_AUTONOME)",
        "tags": [
          "NID",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.2 (Pouponnière) :</strong> Ce Nid s’active aussi sans Défenseur en 4.2 s’il contient déjà au moins 2 Insectes à l’instant où ce Nid est résolu (1 activation max/tour).",
        "temoin": "Génère +2 Insectes chaque tour en autonomie complète."
      },
      "C": {
        "nom": "Le Scarabée Hercule",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_INSECTES_DEFENSE_DOUBLE)",
        "tags": [
          "PARADE_CLASSIQUE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 :</strong> Sur la parcelle de ce Nid, chaque Insecte physiquement présent apporte <strong>2 points de Défense</strong> (lors d’une Parade classique, défaussez immédiatement le nombre d’Insectes arrondi au supérieur du manque).",
        "temoin": "1 Défenseur + 2 Insectes (5 en Défense) parent un Seuil de 5 en ne défaussant immédiatement que 2 Insectes au lieu de 4."
      },
      "D": {
        "nom": "Les guêpes aux aguets",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "CREATION_ENTITE (PIEGE)",
        "tags": [
          "POSE",
          "ARMEMENT"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, si ce Nid contient au moins 1 Insecte et aucun Piège, vous pouvez poser 1 Piège sur sa parcelle (allume la case 2).",
        "temoin": "Auto-piège le Nid qui est immédiatement armé par sa propre production d’Insectes."
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
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "CREATION_ENTITE (SABOTAGE) avec coût",
        "tags": [
          "CONVERSION",
          "SABOTAGE",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de fin de tour).",
        "temoin": "Résolu dans le bloc indivisible du Nid : enrichit définitivement le paquet Machine, puis au balayage suivant les cases 3 et 6 sont examinées dans l’ordre 1 → 6."
      },
      "B": {
        "nom": "La Ruche des Mélipones",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_PIEGE_GLISSE_VERS_CENTRE)",
        "tags": [
          "DECLENCHEMENT_EFFECTIF",
          "PERSISTANCE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5.3 :</strong> À la fin des attaques, sur ce rayon, chaque Piège ayant paré au moins une frappe ce tour-ci glisse sur la prochaine parcelle non rasée vers le cœur (si elle est sans Piège, sans allumer la case 2) au lieu d’être retiré.",
        "temoin": "Résolu du cœur vers la bordure ; un Piège non déclenché reste sur place."
      },
      "D": {
        "nom": "Les mélipones convoyeurs",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5.3 RÉCUPÉRATION",
        "primitive": "MOD_LOI_DU_COEUR (LOI_CONVOI_PIEGE_INSECTE)",
        "tags": [
          "PERSISTANCE",
          "ARMEMENT",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5.3 :</strong> À la fin des attaques, une fois par tour, vous pouvez faire glisser ensemble 1 Piège déclenché ce tour-ci de ce rayon ET 1 Insecte présent sur sa parcelle vers la prochaine parcelle non rasée côté cœur, si elle est sans Piège.",
        "temoin": "Convoie à la fois le Piège et sa sentinelle d’armement pour le tour suivant."
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
    "nomBase": "La Clairière du Jardin du Diable",
    "profils": {
      "A": {
        "nom": "La Clairière du Jardin du Diable",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "4.2 APRÈS PRODUCTION",
        "primitive": "CREATION_ENTITE (SANCTUAIRE_SOUCHE) avec coût",
        "tags": [
          "SOUCHES",
          "CONVERSION"
        ],
        "requires_options": {},
        "texte": "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid : jusqu’à la fin du tour, les Bulldozers laissent toujours 1 Souche sur cette parcelle lors du terrassement, s’il y en a (<code>SANCTUAIRE_SOUCHE</code>).",
        "temoin": "Peut être payé même à 0 Souche actuelle ; persiste jusqu’à la fin du tour même si le Nid est détruit."
      },
      "B": {
        "nom": "La Clairière du Jardin du Diable",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 4.3",
        "primitive": "MOD_LOI_DU_COEUR (LOI_TUNNEL_MIGRATION_DIRECTE)",
        "tags": [
          "INSECTES",
          "MIGRATION"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 4.3 (Tunnel du cœur) :</strong> Une fois par tour, défaussez 1 Insecte de ce Nid pour en faire migrer un autre directement du Nid vers une piste globale.",
        "temoin": "Permet un aller simple définitif vers une case 1..6 de Bug ou Colonie dès p=1, sans traverser tout le rayon."
      },
      "C": {
        "nom": "Le Figuier étrangleur",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI TERRASSEMENT BULLDOZER",
        "primitive": "MOD_LOI_DU_COEUR (LOI_SOUCHES_PROTEGEES_PAR_NID)",
        "tags": [
          "SOUCHES",
          "NID"
        ],
        "requires_options": {},
        "texte": "<strong>Loi de terrassement :</strong> Sur la parcelle de ce Nid, les Bulldozers coupent normalement jusqu’à 1 Arbre mais <strong>ne terrassent aucune Souche</strong>.",
        "temoin": "Même non paré, un Bulldozer ne peut jamais raser cette parcelle en Route Forestière tant que le Nid est en place et qu’il reste au moins 1 Arbre ou 1 Souche."
      },
      "D": {
        "nom": "Le jardin des relèveuses",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5.3 PRÉ-RETRAIT",
        "primitive": "MOD_LOI_DU_COEUR (LOI_NID_RELEVE_APRES_EMBUSCADE)",
        "tags": [
          "RENOUVELLEMENT",
          "INSECTES"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5.3 :</strong> Si un Piège a paré au moins une frappe sur la parcelle de ce Nid pendant qu’il était actif ce tour-ci, créez-y 1 Insecte avant le retrait des Pièges (allume la case 6).",
        "temoin": "Allume la case 6 en 5.3 juste avant la vérification de fin de partie (pouvant ainsi ouvrir un dernier Gardien et l'éveiller en Face 2 pour le tour suivant !)."
      }
    },
    "peuple_origine": "I"
  },
  "SLOT_BUG_CERVEAU": {
    "id": "SLOT_BUG_CERVEAU",
    "famille": "MIGRATION",
    "couple": [
      "I",
      "*"
    ],
    "origine": "I",
    "nomBase": "Slot Migration : Bug du Cerveau",
    "profils": {
      "A": {
        "nom": "Court-circuit d’Apprentissage (Standard)",
        "cycle": "CONSOMME_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "HOOK 6.1",
        "primitive": "MOD_APPRENTISSAGE (-1)",
        "tags": [
          "MIGRATION",
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "En 6.1, après les gains et déductions de Surchauffe, défaussez automatiquement l’Insecte pour retirer -1 jeton Apprentissage à la Tactique qui occupe ce rang (s’il y en a).",
        "temoin": "Appliqué en 6.1 après les retraits volontaires de tuiles : si la case est déjà à 0 jeton, l’Insecte Bug n’est pas défaussé et reste sur son numéro d’emplacement."
      },
      "B": {
        "nom": "Déviation Synaptique (Contrôle 3.2)",
        "cycle": "CONSOMME_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "HOOK 3.2",
        "primitive": "PERMUTATION_PISTE (LECTURE_DE_M)",
        "tags": [
          "MIGRATION",
          "LECTURE_DE"
        ],
        "requires_options": {},
        "texte": "Lorsqu’un joueur obtient ce rang avec son dé M en 3.2, le gouverneur de la piste (Insectes, ou ce joueur si I est absent) peut défausser l’Insecte pour décaler la lecture de ce dé M d’1 rang (M−1 ou M+1, borné de 1 à 6).",
        "temoin": "Permet de dévier une lecture vers un Rêve voisin."
      },
      "C": {
        "nom": "La Cigale dans l’engrenage",
        "cycle": "PASSIF_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "LOI 6.2",
        "primitive": "MOD_LOI_DU_COEUR (LOI_BUG_BLOQUE_AVANCEE_APPRENTISSAGE)",
        "tags": [
          "MIGRATION",
          "APPRENTISSAGE"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 6.2 :</strong> Une Tactique qui occupe un rang portant au moins 1 Insecte ne peut pas avancer par Apprentissage en 6.2. L’Insecte reste sur son numéro de rang.",
        "temoin": "Même lorsque la Cigale bloque l’avancée du vainqueur en 6.2, 100 % des jetons d’Apprentissage de toutes les tuiles sont remis à zéro."
      }
    },
    "peuple_origine": "I"
  },
  "SLOT_COLONISATION_GARDIENS": {
    "id": "SLOT_COLONISATION_GARDIENS",
    "famille": "MIGRATION",
    "couple": [
      "I",
      "*"
    ],
    "origine": "I",
    "nomBase": "Slot Migration : Colonisation des Gardiens",
    "profils": {
      "A": {
        "nom": "Carburant Symbiotique (Standard)",
        "cycle": "CONSOMME_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "HOOK 4.3 FIN",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (REACTIVER_GARDIEN)",
        "tags": [
          "MIGRATION",
          "RESONANCE"
        ],
        "requires_options": {},
        "texte": "À la fin de chaque Étape 4.3, vous pouvez défausser l’Insecte pour ouvrir immédiatement le Gardien disponible de cette case (marquez son ouverture normalement).",
        "temoin": "Examiné des cases 1 à 6 à chaque tour, même sans nouvelle migration."
      },
      "B": {
        "nom": "Bouclier de lisière",
        "cycle": "CONSOMME_ONESHOT",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "5.3 ISSUE PARIS GARDIENS",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (PROTEGER_LISIERE)",
        "tags": [
          "MIGRATION",
          "PROTECTION"
        ],
        "requires_options": {},
        "texte": "En 5.3, lorsqu'un Gardien perd son pari (≥ 1 Défenseur restant sur sa tuile), s'il y a au moins 1 jeton Insecte sur sa case de la Piste des Gardiens, défaussez 1 jeton Insecte de cette case pour empêcher le retour en lisière (le Gardien reste sur la piste sur sa face actuelle). Le pari reste toutefois considéré comme PERDU (ne compte pas pour l'Éveil de la Forêt et ne fait pas passer en Face 2).",
        "temoin": "Protège la présence du Gardien sur la piste en cas de pari perdu, sans valider le pari pour l’Éveil ni déclencher Face 2."
      },
      "C": {
        "nom": "Les Lucioles",
        "cycle": "PASSIF_CONTINU",
        "cablage": [
          1,
          2,
          3,
          4,
          5,
          6
        ],
        "fenetre": "HOOK 4.3 FIN",
        "primitive": "PARTAGE_INFO_ETAT_GARDIEN (AUTO)",
        "tags": [
          "MIGRATION",
          "RESONANCE"
        ],
        "requires_options": {},
        "texte": "À la fin de chaque Étape 4.3, chaque case occupée par au moins 1 Insecte ouvre automatiquement son Gardien disponible. <strong>L’Insecte reste sur sa case.</strong>",
        "temoin": "Assure une ouverture automatique récurrente chaque tour tant que le Gardien n’a pas encore été utilisé."
      }
    },
    "peuple_origine": "I"
  }
};

const VERSION_CHANGELOG = [
  {
    "version": "v6.0",
    "date": "Branche expérimentale exp/socle-v6 (2026-11-21)",
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
  "schema_version": "6.0.0-alpha",
  "date_consolidation": "2026-11-21",
  "architecture_reference": {
    "total_emplacements_synergie": 30,
    "total_pistes_migration": 2,
    "total_profils": 100,
    "topologies_validees": {
      "P4_2233": [
        2,
        2,
        3,
        3
      ],
      "P4_2223": [
        2,
        2,
        2,
        3
      ],
      "P4_1223": [
        1,
        2,
        2,
        3
      ],
      "P5_22233": [
        2,
        2,
        2,
        3,
        3
      ],
      "P5_22223": [
        2,
        2,
        2,
        2,
        3
      ],
      "P5_12223": [
        1,
        2,
        2,
        2,
        3
      ]
    },
    "reserves_materiel": "illimitees (jetons et cartes Sabotage identiques)",
    "plafond_repousse_parcelle": "dotation_initiale_arbres",
    "repousse_finale_base": 0,
    "score_final": "arbres_debout_uniquement (0 Repousse Finale automatique de base)"
  },
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve, Nid) et chaque piste de Migration est gouvernée exclusivement par le joueur de son Peuple d'origine (champ peuple_origine). Zéro vote de groupe.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés (aucun échange verbal ou gestuel sur les coups, cartes ou dés). Sous Le Cri d'Alarme de l'Ara (ouverture anticipée), visibilité publique des cartes et dés mais pose individuelle sans concertation orale.",
    "pont_routier_routes_forestieres": "Le long d'un rayon de Forêt, toute Route Forestière est systématiquement sautée : viser devant, avancer, reculer, glisser un Piège ou migrer désignent toujours la prochaine parcelle non rasée dans cette direction. Latéralement (Forêt <-> Furtivité), une Route Forestière est infranchissable et inoccupable.",
    "suppression_dette_et_verrouillage": "Zéro Insecte engagé et zéro verrouillage des parcelles ciblées. Les Insectes requis lors d’une parade classique sont défaussés immédiatement à la frappe. Tant qu'un Insecte est sur le plateau, il est libre. Seul un Piège ayant déjà paré au moins une frappe ce tour-ci ne peut plus payer un coût volontaire avant son retrait de fin d'attaques.",
    "cascades_gardiens_a_plat": "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur ») : en 3.2 (par carte révélée) 3. Sabotage > 6. Insecte (déviation sur la Réglette des Tactiques) > 5. Rêve (dé M sur rang occupé par un Rêve, quel que soit le choix Bloquer/Avancer) ; en 4.1 Furtivité et en 4.2 production de Nid aucun déclencheur n'est allumé ; en 5.1/5.2 (par frappe bloquée) 2. Piégeage (Piège armé) > 6. Insecte (Parade classique avec dépense >= 1 Insecte) > 1. Parade (Défenseurs seuls). Case 4. Gardien : 1re ouverture du tour de chaque autre Gardien distinct (anti-boucle conservé). Pari uniforme de 0, 1 ou 2 Défenseurs maximum par Gardien construit en 2.2 (glissés sous la tuile à chaque déclenchement). Balayage à plat de 1 à 6."
  },
  "etapes_tour": [
    {
      "numero": 1,
      "code": "PREPARATION_ET_DES_SECRETS",
      "nom": "Acte / Réglette, Ratissage, Distribution et Dés secrets (1.1–1.3)",
      "regles": [
        "1.0 Réglette des Tactiques réversible par blocs : Acte 1 (Tours 1–4, Face A) place les cases 1, 2, 3 en mode CHARGE et les cases 4, 5, 6 en mode ASSAUT. Au début du Tour 5, retournez la Réglette sur sa Face B (Acte 2, Tours 5–8) : permutation des deux blocs — cases 1, 2, 3 en mode ASSAUT et cases 4, 5, 6 en mode CHARGE. Actions fixes sur les deux faces : 1/4 = Sur place (mod_seuil = 0), 2/5 = Devant (mod_seuil = 0), 3/6 = En avançant (SUR_PLACE + DEVANT, avancée +1, mod_seuil = -1).",
        "1.1 Machines en Ratissage : dès qu'une machine se trouve sur la dernière parcelle non rasée de son rayon, elle est retournée définitivement sur sa face Ratissage (carte retirée du paquet Machine). Le Ratissage est détaché de la case 1 et opère en mode ASSAUT permanent : attaque Sur place (mod_seuil = 0), tous ses jetons Puissance actifs dont son +1 imprimé (traité comme +1 jeton Puissance rouge, jetons antérieurs conservés), aucun gain de jeton Puissance. Sous l'option Abatteuse en Ratissage, si sa parcelle cible n'a plus d'Arbre debout, elle arrache 1 Souche (préservant la création de Route Forestière et le cycle de Repli).",
        "1.2 Distribution : chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n'active aucune machine (action du Contremaître perdue). S'il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d'Arbres debout.",
        "1.3 Dés secrets sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient la plus petite valeur (Dé MIN unique du Tour 1 au Tour 8, modifié par les éventuelles Lois actives), qui désigne le rang 1..6 sur la Réglette des Tactiques."
      ]
    },
    {
      "numero": 2,
      "code": "POSE_DES_DEFENSEURS",
      "nom": "Pose des Défenseurs et Piste de Furtivité (2.1–2.2)",
      "regles": [
        "2.1 / 2.2 Pose sous paravent fermé : 1er Défenseur irrévocable sur sa Forêt ou ses 2 lisières ; puis Défenseur de portée globale (réflexion -> choix définitif). Anti-blocage : pose interdite sur Route Forestière, tuile construite/pleine/inconstructible ou rive Furtivité bordant une Route.",
        "Furtivité libre (A1) : 4 emplacements indépendants par case de Furtivité (2 rives de 2 cases, maximum 2 Défenseurs par rive, jusqu'à 4 Défenseurs par case). Aucun déplacement forcé ni glissement sur case jumelle : chaque joueur pose librement son Défenseur sur l'une des 2 cases de la rive qu'il choisit.",
        "2.2 Portée globale, Rêves & Pari sur les Gardiens : pose en réflexion puis définitive partout sur le plateau, y compris sur un Rêve de la Réglette des Tactiques (pour ouvrir le choix exclusif Bloquer OU Avancer en 3.2) ou en pari d'activation sur tout Gardien déjà construit (si >= 1 Animal Sauvage M/R/O ; 0, 1 ou 2 Défenseurs maximum par Gardien, glissés sous la tuile à chaque déclenchement). Un Gardien sans Défenseur reste inactif ce tour-ci."
      ]
    },
    {
      "numero": 3,
      "code": "CONSTRUCTION_ET_REVELATION",
      "nom": "Construction obligatoire (3.1), Ouverture des Paravents et Rêves (3.2)",
      "regles": [
        "3.1 Construction obligatoire : toute tuile réunissant ses 2 constructeurs (ou 1 Défenseur + 1 Insecte avec La Brèche du Tamanoir) est obligatoirement construite AVANT l’ouverture des paravents.",
        "3.1 Nid : posé sur une parcelle non rasée de l'un de ses 2 rayons ne contenant aucune machine ni aucun autre Nid, accompagné de tous ses Défenseurs constructeurs.",
        "3.1 Rêve : un Rêve construit se pose par-dessus la case libre la plus à droite de la Réglette des Tactiques fixe 1..6 (case 6, puis case 5 si 6 est déjà occupée par un Rêve, etc.). Aucune Tactique n'est éjectée (les Insectes restent sur leur numéro de case imprimé). Ce Rêve est immédiatement présent sur la piste pour l'étape 3.2.",
        "3.1 Libération de bâtisseurs (Gardien/Rêve) : si 1 seul Défenseur est libéré parmi 2 (3 joueurs standard, ou 4-6 joueurs avec La Danse des Esprits-Fauves), le joueur du Peuple d'origine de la tuile choisit lequel et sa rive (1re parcelle adjacente non rasée). Si tous les Défenseurs bâtisseurs sont libérés (3 joueurs + Danse), chaque propriétaire choisit sa rive, dans la limite des Défenseurs réellement présents.",
        "3.2 Révélation simultanée (paravents ouverts) — partition stricte « 1 carte révélée = au plus 1 déclencheur » : (a) 3. Sabotage si la carte révélée est un Sabotage ; (b) sinon 6. Insecte si un pion Insecte de la Réglette des Tactiques (SLOT_BUG_CERVEAU=B) dévie le dé M de ±1 rang ; (c) sinon 5. Rêve si le dé retenu M d'une carte Machine pointe sur un rang occupé par une tuile Rêve (quel que soit le choix Bloquer ou Avancer). Résolution des Rêves (choix exclusif Bloquer OU Avancer) : pour chaque Rêve portant >= 1 Défenseur et visé par >= 1 machine non déviée, le Peuple Onirique choisit une seule issue — BLOQUER (chaque Défenseur posé annule 1 machine de ce rang en priorisant la plus menaçante ; les machines restantes exécutent la Tactique imprimée dessous ; le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit quel que soit le nombre de machines ; aucune machine n'est annulée et toutes exécutent la Tactique imprimée dessous ; le Rêve saute vers la 1re case libre à sa gauche). Par défaut, le pouvoir propre du Rêve s'active sur les deux choix."
      ]
    },
    {
      "numero": 4,
      "code": "FURTIVITE_NIDS_ET_MIGRATION",
      "nom": "Furtivité (4.1), Production des Nids (4.2) et Migration des Insectes (4.3)",
      "regles": [
        "4.1 Furtivité libre (A1) : sur chaque case de Furtivité, chacune des 2 rives est évaluée indépendamment et déclenche son action uniquement si elle porte un binôme complet (2 Défenseurs sur ses 2 cases ; un pion seul ne déclenche rien). Si les 4 cases sont occupées (2 binômes complets), les 2 rives s'exécutent toutes les deux. Chaque rive déclenchée est gouvernée par le joueur de son bord : Piège si aucune machine sur la parcelle en face, OU Sabotage si au moins 1 machine y stationne et aucune n'est active ce tour (Ratissage = active ; une machine annulée par Bloquer en 3.2 est inactive et sabotable). Aucun déclencheur Gardien n'est allumé en 4.1.",
        "4.2 Production des Nids : chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (sans allumer le déclencheur 6. Insecte), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens.",
        "4.3 Migration : chaque Insecte sur la roue peut se déplacer de 0 ou 1 cran (jusqu'à 2 avec L'Envol du Batará Suiveur), même s'il a bougé lors de la production d'un Nid. On retourne chaque jeton déplacé sur sa face verso pour suivi, puis on remet tous les jetons à l'endroit en fin de Migration avant d'évaluer la Colonisation.",
        "4.3 Pistes globales : depuis la dernière parcelle non rasée d'un rayon, 1 cran permet d'entrer sur n'importe quelle case 1..6 d'une piste globale (Bug du Cerveau ou Colonisation des Gardiens), sans limite de jetons par case. Cet aller simple est définitif."
      ]
    },
    {
      "numero": 5,
      "code": "ATTAQUES_ET_TEST_FIN",
      "nom": "Attaques des Machines et Vérification de Fin de Partie (5.1–5.3)",
      "regles": [
        "Ordre des machines : Réglette des Tactiques de la case 1 à la case 6, puis machines en Ratissage (mode ASSAUT permanent, détaché de la case 1). Sur un même rayon au même rang (ou en Ratissage), l'Abatteuse agit toujours avant le Bulldozer ; entre rayons distincts au même rang, ordre libre entre les joueurs concernés.",
        "Modes CHARGE et ASSAUT (Réglette réversible) : chaque machine est résolue d'un seul tenant (lecture dynamique des cibles -> frappes -> avancée éventuelle sur 3/6 -> gain éventuel de jeton Puissance). En mode CHARGE (Acte 1 cases 1–3 ; Acte 2 cases 4–6) : les jetons Puissance déjà sur la machine sont ignorés dans le calcul du seuil de parade ; si l'activation inflige au moins 1 dégât effectif (>= 1 Arbre coupé ou >= 1 Souche arrachée), la machine gagne +1 jeton Puissance (plafonné à +1 par activation même sur double cible 3/6). En mode ASSAUT (Acte 1 cases 4–6 ; Acte 2 cases 1–3 ; et Ratissage permanent) : tous les jetons Puissance comptent dans le seuil de parade ; aucun jeton Puissance n'est gagné.",
        "Chaîne stricte des parades à chaque frappe : (1) Bond du Jaguar (Loi auto : 2 jetons bleus défaussés -> toutes frappes restantes de la machine parées + recul) -> (2) Piquée de la Harpie -> (3) Piège (Embuscade auto si Défense totale >= 1, locale ou soutenue à distance ; le Piège est marqué comme ayant servi) -> (4) Parade classique (Défenseurs + défausse immédiate des Insectes manquants).",
        "Contact Machine-Nid : tout mouvement de machine (avancée, recul, repli depuis une Route) entrant sur la parcelle d'un Nid non protégé renvoie ce Nid en lisière (reconstructible) et défausse tous les Insectes de la parcelle (Défenseurs et Piège restent).",
        "Création d'une Route Forestière (0 Arbre et 0 Souche après un Bulldozer, ou après une Abatteuse en Ratissage arrachant la dernière Souche sous l'option correspondante) : recul automatique des machines présentes vers la prochaine parcelle non rasée côté bordure, ou vers le cœur uniquement si tout est déjà rasé côté bordure (maintien irréversible du mode Ratissage ; retrait définitif de la partie si tout le rayon est rasé).",
        "Fin des attaques : effets 'à la fin des attaques' (ex. Ruches des Mélipones) et retrait de tout Piège ayant paré au moins 1 frappe durant le tour.",
        "Issue des paris Gardiens, Bouclier de lisière & Vérification de fin de partie (5.3) : retrait des Pièges déclenchés, puis résolution des paris Gardiens (0 Défenseur restant -> pari gagné : le Gardien reste en piste et passe Face 2 s'il est double-face ; >= 1 Défenseur restant -> pari perdu : si Bouclier de lisière SLOT_COLONISATION_GARDIENS=B et >= 1 Insecte sur sa case, défausser 1 Insecte pour garder le Gardien en piste sur sa face actuelle tout en laissant le pari PERDU, sinon retour immédiat en lisière Face 1). Test de fin de partie : priorité absolue au Tour 8 ; aux Tours 1..7, Sommeil du Contremaître (toutes les tuiles Rêves en jeu en bloc continu 1..k) ou Réveil de la Forêt 100 % Piste des Gardiens (les N Défenseurs de la table engagés en 2.2 sur les Gardiens et aucun pari perdu). Si atteint : fin immédiate de la partie et décompte des Arbres debout (0 Repousse Finale automatique de base)."
      ]
    },
    {
      "numero": 6,
      "code": "APPRENTISSAGE_ET_MENAGE",
      "nom": "Ménage de fin de tour (6.2–6.3)",
      "regles": [
        "Ménage systématique (6.2) : Réglette des Tactiques 1..6 fixe (retournée sur Face B au début du Tour 5 pour l'Acte 2), retour en main de tous les Défenseurs (y compris ceux posés sur des Rêves ou Gardiens et ceux glissés sous une tuile) et remise à zéro des modificateurs transitoires.",
        "Clôture du tour (6.3) : passage du pion Coordonnateur au siège suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
      ]
    }
  ],
  "arbitrages_valides": {
    "A01": "Lecture unique du Dé MIN (Tours 1 à 8) sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Ce rang 1..6 désigne la case visée sur la Réglette des Tactiques.",
    "A02": "Rêve sur dé Machine (v6.0) : un Rêve muni d'au moins 1 Défenseur et visé par >= 1 machine non déviée en 3.2 propose au Peuple Onirique le choix exclusif BLOQUER ou AVANCER (max 1 ouverture par Rêve et par tour par défaut).",
    "A03": "Furtivité libre A1 (v6.0) : 4 emplacements indépendants par case (2 rives de 2 cases, max 2 Défenseurs par rive, zéro glissement sur case jumelle). En 4.1, une rive déclenche son action uniquement si elle porte un binôme complet (2 Défenseurs sur ses 2 cases ; un pion seul ne déclenche rien). Si les 4 cases sont occupées (2 binômes complets), les 2 rives s'exécutent toutes les deux.",
    "A04": "Gouvernance unitaire : chaque tuile de Synergie et piste de Migration est décidée uniquement par son Peuple d'origine.",
    "A05": "Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; suppression totale des Insectes engagés.",
    "A06": "Armement des Pièges : Embuscade dès que Défense totale >= 1 (locale ou à distance) ; tout Piège ayant paré >= 1 fois dans le tour est retiré en fin d'attaques.",
    "A07": "Zéro verrouillage des parcelles ciblées : Insectes toujours libres tant que présents ; seul un Piège déjà déclenché ce tour-ci ne peut plus payer de coût volontaire.",
    "A08": "Pont routier : Routes Forestières systématiquement sautées le long d'un rayon, mais infranchissables/inoccupables latéralement.",
    "A09": "Repli sur création de Route : recul automatique vers la bordure par défaut, vers le cœur seulement si bord tout rasé, retrait si rayon tout rasé ; Ratissage irréversible maintenu.",
    "A10": "Autonomie du Ratissage en Assaut permanent (v6.0) : pion double face retourné définitivement sur la dernière parcelle non rasée ; détaché de la case 1, il attaque Sur place (mod_seuil = 0) en mode ASSAUT permanent (tous les jetons Puissance actifs dont son +1 imprimé, aucun gain de jeton Puissance). Sous l'option Abatteuse en Ratissage, si la parcelle n'a plus d'Arbre debout, elle arrache 1 Souche (préservant Route Forestière et Repli).",
    "A11": "Réglette des Tactiques réversible par blocs & placement des Rêves (v6.0) : actions fixes 1/4 Sur place (0), 2/5 Devant (0), 3/6 En avançant (+1 parcelle, -1 seuil). Acte 1 (Tours 1–4, Face A) : 1–3 CHARGE / 4–6 ASSAUT. Acte 2 (Tours 5–8, Face B retournée début Tour 5) : 1–3 ASSAUT / 4–6 CHARGE. Un Rêve construit en 3.1 se pose par-dessus la case libre la plus à droite (6, puis 5, etc.) sans éjecter les Tactiques ni déplacer les Insectes.",
    "A12": "Cascades de Gardiens : fin complète de l'effet en cours, marquage immédiat à l'ouverture, balayage à plat de 1 à 6 sans pile imbriquée.",
    "A13": "Faces 2 et Lois passives : seule la face visible s'applique (Faces 2 autonomes) ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume.",
    "A14": "Éveil / Réveil de la Forêt 100 % Piste des Gardiens (v6.0) : actif uniquement si >= 1 Peuple Animal Sauvage (M, R ou O) est autour de la table, aux Tours 1..7 (priorité absolue au Tour 8). En 5.3, la Forêt s'éveille si les N Défenseurs de la table ont tous été engagés en 2.2 sur la Piste des Gardiens et qu'aucun pari n'est perdu (0 Défenseur restant). Un Gardien sauvé par Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) reste en piste sur sa face actuelle mais son pari reste PERDU.",
    "A15": "Test de fin de partie & Suppression de la Repousse Finale de base (5.3, v6.0) : priorité absolue au Tour 8 (fin TOUR_8) ; aux Tours 1..7, vérification directe après issue des paris Gardiens de Sommeil du Contremaître (tous les Rêves en jeu en bloc continu cases 1..k) ou de Réveil de la Forêt 100 % Gardiens. En fin de partie, 0 Souche ne repousse automatiquement dans le cœur : le score compte uniquement les Arbres debout.",
    "A16": "Contact Machine-Nid : tout mouvement entrant (avancée, recul, repli) renvoie le Nid reconstructible en lisière et défausse tous les Insectes de la parcelle.",
    "A17": "Migration des Insectes : 0 ou 1 cran facultatif (suivi par retournement des pions) ; aller simple définitif et sans limite vers les pistes globales.",
    "A18": "Production des Nids : bloc indivisible (création selon état réel présent + pouvoir du Nid avant Gardiens) ; Miel des Ancêtres restreint aux jetons Insecte.",
    "A19": "Cibles dynamiques : lues selon la position physique réelle de la machine à l’instant où elle attaque.",
    "A20": "Matamata et chaîne des parades : Matamata vérifie la présence d'une Souche à chaque frappe ; ordre Jaguar -> Harpie -> Piège -> Parade classique.",
    "A21": "Rêves en choix exclusif « Bloquer OU Avancer » (v6.0) : en 3.2, pour chaque Rêve portant >= 1 Défenseur et visé par >= 1 machine non déviée, le Peuple Onirique choisit une seule issue : BLOQUER (chaque Défenseur annule 1 machine du rang en priorisant la plus menaçante ; les machines restantes jouent la Tactique dessous ; le Rêve ne bouge pas) OU AVANCER (1 seul Défenseur suffit ; 0 machine annulée, toutes jouent la Tactique dessous ; le Rêve saute vers la 1re case libre à sa gauche). Déclencheur 5. Rêve inchangé (allumé dès qu'une machine non déviée pointe sur un rang Rêve, quel que soit le choix). Pouvoir propre du Rêve actif par défaut sur les deux choix.",
    "A22": "Pari uniforme sur les Gardiens & Partition stricte des 6 déclencheurs (v6.0) : actif si >= 1 Animal Sauvage (M/R/O) est à la table. Pari uniforme UNIFORM_MAX_2 (0, 1 ou 2 Défenseurs maximum par Gardien construit cases 1..6, glissés sous la tuile à chaque déclenchement). Partition stricte (« 1 événement = au plus 1 déclencheur ») : en 3.2 Sabotage > Insecte sur Tactiques > Rêve ; en 4.1 et 4.2 Nids aucun déclencheur ; en 5.1/5.2 Piégeage > Insecte en Parade >= 1 Insecte > Parade par Défenseurs seuls ; 4. Gardien sur 1re ouverture du tour de chaque autre Gardien distinct (DISTINCT_OPEN_1, anti-boucle conservé). En 5.3 : pari gagné -> reste en piste et passe Face 2 si double-face ; pari perdu -> retour en lisière Face 1, sauf Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B) qui défausse 1 Insecte de la case pour garder le Gardien en piste sur sa face actuelle, le pari restant PERDU.",
    "A23": "Réglette des Tactiques réversible Face A/B, Charge/Assaut & Déviation par Insectes (v6.0) : en mode CHARGE les jetons Puissance existants sont ignorés au seuil et +1 jeton Puissance est gagné uniquement sur >= 1 dégât effectif (plafonné à +1/activation) ; en mode ASSAUT tous les jetons Puissance comptent au seuil et 0 jeton n'est gagné. SLOT_BUG_CERVEAU=B (Déviation ±1 en 3.2) et SLOT_COLONISATION_GARDIENS=B (Bouclier de lisière en 5.3) sont actifs par défaut.",
    "A24": "Cartes Sabotage (dilution permanente, v5.5) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis en Furtivité 4.1 est mis de côté pour rejoindre définitivement le paquet Machine en 6.3 (sans allumer 3. Sabotage) ; 1 carte Sabotage révélée à l'ouverture des paravents en 3.2 fait perdre 1 activation au Contremaître, allume 3. Sabotage (partition stricte 3.2), puis est remélangée en fin de tour.",
    "A25": "Séquence des attaques (v6.0) : Réglette 1..6 (mode CHARGE ou ASSAUT selon l'Acte) puis Ratissages (ASSAUT permanent détaché de la case 1) ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant."
  }
};
