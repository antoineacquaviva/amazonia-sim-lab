// -------------------------------------------------------------------------
    // 1. MÉTADONNÉES DES 6 PEUPLES & MATRICE 6x5 DES 30 TUILES DE LISIÈRE
    // -------------------------------------------------------------------------
    const PEUPLES = {
      M: { code: 'M', nom: 'Mammifères', famille: 'Animal Sauvage (Gardien)', badge: 'bg-amber-100 text-amber-900 border-amber-300', icon: '🐆' },
      R: { code: 'R', nom: 'Reptiles', famille: 'Animal Sauvage (Gardien)', badge: 'bg-emerald-100 text-emerald-900 border-emerald-300', icon: '🐍' },
      O: { code: 'O', nom: 'Oiseaux', famille: 'Animal Sauvage (Gardien)', badge: 'bg-sky-100 text-sky-900 border-sky-300', icon: '🦜' },
      H: { code: 'H', nom: 'Humains', famille: 'Onirique (Rêve)', badge: 'bg-rose-100 text-rose-900 border-rose-300', icon: '🏹' },
      E: { code: 'E', nom: 'Entités Magiques', famille: 'Onirique (Rêve)', badge: 'bg-purple-100 text-purple-900 border-purple-300', icon: '✨' },
      I: { code: 'I', nom: 'Insectes', famille: 'Symbiotique (Croissance)', badge: 'bg-lime-100 text-lime-900 border-lime-300', icon: '🐜' }
    };

    // Matrice exacte § 2.3 : pour toute paire de voisins (X, Y), renvoie les deux tuiles présentes sur leur lisière
    const MATRICE_PAIRES = {
      'M_R': ['G1', 'G2'], 'R_M': ['G2', 'G1'],
      'M_O': ['G3', 'G4'], 'O_M': ['G4', 'G3'],
      'R_O': ['G5', 'G6'], 'O_R': ['G6', 'G5'],
      'M_H': ['G7', 'R3'], 'H_M': ['R3', 'G7'],
      'M_E': ['G8', 'R7'], 'E_M': ['R7', 'G8'],
      'R_H': ['G9', 'R4'], 'H_R': ['R4', 'G9'],
      'R_E': ['G10', 'R8'], 'E_R': ['R8', 'G10'],
      'O_H': ['G11', 'R5'], 'H_O': ['R5', 'G11'],
      'O_E': ['G12', 'R9'], 'E_O': ['R9', 'G12'],
      'M_I': ['G13', 'M1'], 'I_M': ['M1', 'G13'],
      'R_I': ['G14', 'M2'], 'I_R': ['M2', 'G14'],
      'O_I': ['G15', 'M3'], 'I_O': ['M3', 'G15'],
      'H_E': ['R1', 'R2'], 'E_H': ['R2', 'R1'],
      'H_I': ['R6', 'M4'], 'I_H': ['M4', 'R6'],
      'E_I': ['R10', 'M5'], 'I_E': ['M5', 'R10']
    };

    // -------------------------------------------------------------------------
    // 2. LES 10 AXES DU CHÂSSIS (PRODUIT CARTÉSIEN = 128 CONFIGURATIONS)
    // -------------------------------------------------------------------------
    const CHASSIS_AXES_SPEC = [
      {
        key: 'P_Max',
        num: 1,
        label: '1. Topologie & Dotation Seuil Imprimé',
        defaultVal: 4,
        options: [
          { val: 4, text: 'P4_2233 : 4 parcelles [2,2,3,3] (10N Arbres · Standard)' },
          { val: 5, text: 'P5_22233 : 5 parcelles [2,2,2,3,3] (12N Arbres)' }
        ]
      },
      {
        key: 'Regle_Ouverture_Reve_Multiple',
        num: 2,
        label: '2. Ouverture multiple d’un Rêve (3.2)',
        defaultVal: 'UNIQUE_PAR_TOUR',
        options: [
          { val: 'UNIQUE_PAR_TOUR', text: 'Unique par tour (1 ouverture max/tour)' },
          { val: 'PAR_DE_M_DESIGNE', text: 'Cumulatif (1 ouverture par dé M désigné)' }
        ]
      },
      {
        key: 'Offset_Seuil_Parade',
        num: 3,
        label: '3. Décalage du Seuil de Parade',
        defaultVal: 0,
        options: [
          { val: 0, text: 'Offset 0 (Défense ≥ Seuil Imprimé modifié)' },
          { val: 1, text: 'Offset +1 (Exige +1 Défenseur de plus)' }
        ]
      },
      {
        key: 'Mise_En_Place_Tactiques',
        num: 4,
        label: '4. Mise en place Piste des Tactiques',
        defaultVal: 'ORDRE_FIXE_T1_T6',
        options: [
          { val: 'ORDRE_FIXE_T1_T6', text: 'Ordre croissant fixe T1 à T6 (Standard)' },
          { val: 'ALEATOIRE', text: 'Tirage aléatoire au départ' }
        ]
      },
      {
        key: 'Declenchement_Fin_De_Piste',
        num: 5,
        label: '5. Entrée en Siège T4',
        defaultVal: 'ARRIVEE_DERNIERE_PARCELLE',
        options: [
          { val: 'ARRIVEE_DERNIERE_PARCELLE', text: 'Dès présence sur la dernière parcelle intacte' },
          { val: 'DEPASSEMENT_DERNIERE_PARCELLE', text: 'Par dépassement de la dernière parcelle' }
        ]
      },
      {
        key: 'Role_Abatteuse_Fin_De_Piste',
        num: 6,
        label: '6. Rôle de l’Abatteuse en Siège T4',
        defaultVal: 'STANDARD_COUPE_ARBRE',
        options: [
          { val: 'STANDARD_COUPE_ARBRE', text: 'Standard (Coupe uniquement les Arbres)' },
          { val: 'ARRACHE_1_SOUCHE_SI_SANS_ARBRE', text: 'Arrache 1 Souche s’il n’y a plus d’Arbre' }
        ]
      },
      {
        key: 'Synergie_Binome_Machines',
        num: 7,
        label: '7. Puissance du binôme de machines',
        defaultVal: 'INDIVIDUELLE',
        options: [
          { val: 'INDIVIDUELLE', text: 'Individuelle (Propre à chaque machine)' },
          { val: 'MUTUALISATION_PUISSANCE_MEME_PARCELLE', text: 'Mutualisée sur une même parcelle' }
        ]
      }
    ];

    // -------------------------------------------------------------------------
    // 3. CATALOGUE COMPLET DES 32 EMPLACEMENTS ET 116 PROFILS (v5.2)
    // -------------------------------------------------------------------------
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
        "texte": "<strong>Face 1 :</strong> Réduisez de -2 le Seuil de Parade d’une machine portant au moins 1 jeton Puissance (rouge ou bleu) pour le reste du tour.<br><strong>Face 2 (Loi 5) :</strong> Dès qu’une machine porte ≥ 2 jetons bleus (<em>Surchauffe</em>) au moment de frapper, défaussez 2 bleus pour <strong>parer automatiquement toutes ses frappes encore à résoudre</strong> et la faire reculer immédiatement d’1 parcelle non rasée vers la bordure au lieu de son avancée (si elle n’est pas en Siège).",
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
        "texte": "<strong>Face 1 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Siège située sur une parcelle avec au moins 1 Défenseur.<br><strong>Face 2 :</strong> Faites reculer d’1 parcelle non rasée vers la bordure n’importe quelle machine non en Siège.",
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
        "texte": "<strong>Face 1 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas</strong> sur T3/T6.<br><strong>Face 2 (Loi 5) :</strong> Une machine dont toutes les frappes sont parées <strong>n’avance pas ET ne gagne pas de jeton Puissance rouge</strong> sur T3 à T6 (y compris en Siège).",
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
        "texte": "<strong>Face 1 (Ouverture) :</strong> Réduisez de -1 le Seuil de Parade sur une parcelle des rayons O ou M pour le reste du tour.<br><strong>Sacrifice (en 3.2 après révélation) :</strong> Déplacez jusqu’à 2 Défenseurs vers des parcelles ciblées (renvoyez G4 sur sa Face 1 en lisière ; il libère sa case et perd son marqueur « utilisé »).",
        "temoin": "Le sacrifice libère la case Gardien pour une future construction ; le seuil fixe de Réveil calculé à la mise en place ne change pas."
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
        "texte": "Posez 1 Piège sur une parcelle non rasée contenant au moins 1 Souche et aucun Piège, même occupée par une machine ou ciblée (déclenche la case 2).",
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
        "texte": "En 3.2 (ou à l’ouverture avant l’attaque de la machine), décalez d’1 parcelle non rasée dans le même sens le long de son rayon l’ensemble des frappes d’une machine non en Siège pour ce tour, sans déplacer la machine.",
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
        "texte": "<strong>Loi 5 :</strong> Sur 1 rayon au choix par tour, si l’Abatteuse et le Bulldozer sont tous deux actifs, vous pouvez résoudre le <strong>Bulldozer avant l’Abatteuse</strong> (quel que soit leur rang ou en Siège).",
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
        "texte": "<strong>Face 1 :</strong> Ajoutez définitivement 1 carte Sabotage de la réserve au paquet Machine (mise de côté pour le remélange de 6.3 ; allume la case 3).<br><strong>Face 2 :</strong> Ajoutez définitivement 2 cartes Sabotage de la réserve au paquet Machine (allume la case 3).",
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
        "texte": "<strong>Face 1 (Loi 4.1) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong>.<br><strong>Face 2 (Loi 4.1 & 3.2) :</strong> Un binôme en Furtivité peut saboter sa parcelle cible même si une machine y est active ce tour-ci ou en <strong>Siège</strong> ; de plus, en 3.2, chaque carte Sabotage révélée derrière un paravent allume la <strong>case 3. Sabotage</strong> et retire <strong>1 jeton Puissance rouge</strong> d’une machine sur les rayons R ou H.",
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
        "texte": "Échangez une tuile Rêve de la Piste des Tactiques avec sa voisine de gauche (r → r-1, sans ouvrir son Slot ni allumer la case 5).",
        "temoin": "Si le Rêve atteint ainsi le Rang 1, le Sommeil du Contremaître sera validé lors de la vérification de fin d’attaques en 5.3."
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
        "temoin": "Peut consommer le Piège tout juste posé en 4.1 pour amener un Rêve au Rang 1 (victoire vérifiée en fin de 5.3). Un Piège ayant déjà paré ce tour ne peut pas payer ce coût."
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
        "texte": "Posez 1 jeton Insecte sur une parcelle non rasée ou une case Furtivité contenant au moins 1 Défenseur (allume la case 6).",
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
        "texte": "Défaussez 1 Insecte d’une parcelle Forêt pour poser 1 Piège sur cette parcelle ou une parcelle non rasée adjacente du même rayon sans Piège (allume la case 2).",
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
        "temoin": "Accélère l’arrivée au Rang 1 pour déclencher le Sommeil du Contremaître en fin de 5.3."
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
        "temoin": "Coût volontaire : ne déclenche pas un pouvoir de sacrifice et ne modifie pas le seuil fixe de Réveil."
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
        "texte": "Posez 1 Insecte de la réserve sur une parcelle non rasée d’un rayon de cette paire (H ou I, allume la case 6).",
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
        "texte": "Faites reculer d’1 parcelle non rasée vers la bordure une machine non en Siège située sur les rayons E ou M.",
        "temoin": "Retarde l’entrée en Siège et modifie dynamiquement les cibles que cette machine lira à l’Étape 5."
      },
      "B": {
        "nom": "L’Ombre du Maître des Bois",
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "fenetre": "LOI 5",
        "primitive": "MOD_LOI_DU_COEUR (LOI_ENDIGUEMENT_SIEGE_T4)",
        "tags": [
          "SIEGE_T4"
        ],
        "requires_options": {},
        "texte": "<strong>Loi 5 (Endiguement du Siège) :</strong> Les machines en <strong>Siège</strong> sur les rayons E et M et leurs rayons voisins immédiats ne gagnent plus de jeton Puissance rouge après leur attaque et subissent -1 à leur Seuil de Parade.",
        "temoin": "Neutralise l’escalade de Puissance des machines en Siège sans annuler leur statut."
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
        "texte": "Posez 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R, même occupée par une machine ou ciblée (allume la case 2).",
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
        "texte": "<strong>Loi 6.2 :</strong> En cas d’égalité en tête de l’Apprentissage à l’Étape 6.2 (y compris égalité générale à 0), c’est ce Rêve qui avance d’1 rang vers la gauche (r → r−1). S’il atteint ainsi le Rang 1, la fin de partie se déclenche immédiatement à la fin de ce tour (Repousse Finale).",
        "temoin": "Exception unique au test de 5.3 : atteindre le Rang 1 en 6.2 déclenche aussitôt la Repousse Finale. Un blocage par la Cigale (Bug C) d’un vainqueur unique n’est pas une égalité."
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
        "temoin": "Convertit un Insecte de la roue en avancée accélérée vers le Rang 1 (les Insectes déjà migrés sur Bug ou Colonie ne peuvent pas payer ce coût)."
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
        "texte": "Après production en 4.2, vous pouvez défausser 1 Insecte de ce Nid pour ajouter définitivement 1 carte Sabotage de la réserve au paquet Machine (allume la case 3).",
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
        "temoin": "Allume la case 6 en 5.3 juste avant la vérification de fin de partie (pouvant ainsi ouvrir un dernier Gardien pour atteindre le seuil de Réveil !)."
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

    // -------------------------------------------------------------------------
    // 4. JOURNAL STRUCTURÉ DES ÉVOLUTIONS (v4.3 -> v4.9 -> v5.0 -> v5.1 -> v5.2)
    // -------------------------------------------------------------------------
    const VERSION_CHANGELOG = [
  {
    "version": "v5.3",
    "date": "Version consolidée en vigueur (Audit · 25 arbitrages)",
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

    // -------------------------------------------------------------------------

// --- ÉPURATION CONSOLIDÉE v5.3 : 100 PROFILS & CHANGELOG v5.3 ---
Object.keys(CATALOGUE_TUILES).forEach(function(tId) {
  if (CATALOGUE_TUILES[tId].profils && CATALOGUE_TUILES[tId].profils.E) {
    delete CATALOGUE_TUILES[tId].profils.E;
  }
});
if (CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS && CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils.B) {
  delete CATALOGUE_TUILES.SLOT_COLONISATION_GARDIENS.profils.B;
}

// === BEGIN SPEC_FORMELLE_V5_3 (auto-generated by build_v5_3_audit.py) ===
const SPEC_FORMELLE_V5_3 = {
  "schema_version": "5.3.1-audit",
  "date_consolidation": "2026-11-16",
  "architecture_reference": {
    "total_emplacements_synergie": 30,
    "total_pistes_migration": 2,
    "total_profils": 100,
    "topologies_validees": {
      "P3": [
        2,
        3,
        3
      ],
      "P4_2233": [
        2,
        2,
        3,
        3
      ],
      "P5_22233": [
        2,
        2,
        2,
        3,
        3
      ],
      "P6": [
        2,
        2,
        2,
        3,
        3,
        3
      ]
    },
    "reserves_materiel": "illimitees (jetons et cartes Sabotage identiques)",
    "plafond_repousse_parcelle": "dotation_initiale_arbres"
  },
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve, Nid) et chaque piste de Migration est gouvernée exclusivement par le joueur de son Peuple d'origine (champ peuple_origine). Zéro vote de groupe.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés (aucun échange verbal ou gestuel sur les coups, cartes ou dés). Sous Le Cri d'Alarme de l'Ara (ouverture anticipée), visibilité publique des cartes et dés mais pose individuelle sans concertation orale.",
    "pont_routier_routes_forestieres": "Le long d'un rayon de Forêt, toute Route Forestière est systématiquement sautée : viser devant, avancer, reculer, glisser un Piège ou migrer désignent toujours la prochaine parcelle non rasée dans cette direction. Latéralement (Forêt <-> Furtivité), une Route Forestière est infranchissable et inoccupable.",
    "suppression_dette_et_verrouillage": "Zéro Insecte engagé et zéro verrouillage des parcelles ciblées. Les Insectes requis lors d’une parade classique sont défaussés immédiatement à la frappe. Tant qu'un Insecte est sur le plateau, il est libre. Seul un Piège ayant déjà paré au moins une frappe ce tour-ci ne peut plus payer un coût volontaire avant son retrait de fin d'attaques.",
    "cascades_gardiens_a_plat": "On résout toujours intégralement l'action ou la tuile en cours avant d'examiner la Piste des Gardiens (signal binaire allumé/éteint par case 1..6, sans cumul de cardinalité). Dès qu'un Gardien s'ouvre, il reçoit immédiatement son marqueur 'utilisé' avant application de son texte. Balayage à plat dans l'ordre croissant des cases 1 à 6, répété tant qu'une case allumée porte un Gardien non utilisé."
  },
  "etapes_tour": [
    {
      "numero": 1,
      "code": "PREPARATION_POSE_FURTIVITE",
      "nom": "Distribution, Dés secrets et Pose des Défenseurs",
      "regles": [
        "Machines en Siège : toute machine déjà située sur la dernière parcelle non rasée de son rayon est en Siège T4 irréversible (carte posée sur sa parcelle). Son attaque en fin d’Étape 5 est autonome même si la tuile T4 a été éjectée par un Rêve ; en 6.1, elle alimente la tuile T4 en jetons d’Apprentissage si et seulement si T4 est encore présente sur la piste.",
        "Chaque joueur hors pénurie pioche secrètement 1 carte du paquet Machine (incluant toutes les cartes Sabotage intégrées définitivement). Une carte Sabotage tirée n’active aucune machine (action du Contremaître perdue). S’il reste moins de cartes que de joueurs, distribution dans le sens horaire à partir du peuple ayant le plus d’Arbres debout.",
        "Sous paravent fermé (silence complet) : chaque joueur ayant reçu une carte Machine lance ses 2D6 et retient M = min(D1, D2) (modifié par les éventuelles Lois actives), qui désigne le rang sur la Piste des Tactiques. Si ce rang contient une tuile Rêve, l’activation de cette machine sera annulée en 3.2.",
        "Piste de Furtivité à 4 emplacements par case (2 jumeaux rive J1, 2 jumeaux rive J2 ; max 2 Défenseurs par case). Lorsqu'un Défenseur ENTRE sur une case de Furtivité (1er Défenseur, 2e en réflexion ou 2e posé directement en choix définitif), on le pose sur l'un des 4 emplacements valides et l'éventuel autre Défenseur présent glisse aussitôt sur l'emplacement jumeau du même bord (orientant l'unique action du binôme). Retourner sur place un jeton de sa face réflexion à sa face choix définitif se fait strictement sur son emplacement actuel, sans déplacement ni tirage."
      ]
    },
    {
      "numero": 2,
      "code": "REVELATION_DES_REVES_FURTIVITE",
      "nom": "Ouverture des Paravents, Rêves, Dés et Furtivité",
      "regles": [
        "Ouverture simultanée des paravents et fin du silence tactique. Toute carte Sabotage révélée n’a aucun autre effet que d’avoir fait perdre une activation au Contremaître : elle est mise de côté pour être remélangée dans le paquet Machine en fin de tour.",
        "Résolution des Rêves : tout dé M désignant le rang d’un Rêve annule sa machine, ouvre ce Rêve et le fait avancer d’1 cran vers la gauche (max 1 ouverture par Rêve et par tour en châssis standard UNIQUE_PAR_TOUR, résolue de gauche à droite).",
        "Chaque binôme complet sur une case de Furtivité déclenche 1 seule action, gouvernée par le joueur de la rive où se trouvent les 2 emplacements jumeaux occupés."
      ]
    },
    {
      "numero": 3,
      "code": "CONSTRUCTION_SYNERGIES",
      "nom": "Construction obligatoire des Tuiles de Synergie",
      "regles": [
        "Toute tuile réunissant ses 2 constructeurs (ou 1 Défenseur + 1 Insecte avec La Brèche du Tamanoir) est obligatoirement construite.",
        "Nid : posé sur une parcelle non rasée de l'un de ses 2 rayons ne contenant aucune machine ni aucun autre Nid, accompagné de tous ses Défenseurs constructeurs.",
        "Rêve : la Tactique la plus à droite sur la piste est définitivement éjectée ; seules les tuiles situées à droite de ce trou glissent d'un cran vers la gauche ; le nouveau Rêve prend place en case 6 (les Insectes Bug restent sur leur numéro d'emplacement imprimé).",
        "Libération de bâtisseurs (Gardien/Rêve) : si 1 seul Défenseur est libéré parmi 2 (3 joueurs standard, ou 4-6 joueurs avec La Danse des Esprits-Fauves), le joueur du Peuple d'origine de la tuile choisit lequel et sa rive (1re parcelle adjacente non rasée). Si tous les Défenseurs bâtisseurs sont libérés (3 joueurs + Danse), chaque propriétaire choisit sa rive, dans la limite des Défenseurs réellement présents."
      ]
    },
    {
      "numero": 4,
      "code": "NIDS_ET_MIGRATION",
      "nom": "Production des Nids et Migration des Insectes",
      "regles": [
        "Chaque Nid actif est résolu comme un bloc indivisible : (1) création de 1 ou 2 Insectes selon le nombre d'Insectes physiquement présents sur sa parcelle à cet instant précis (y compris pour l'activation autonome des Guêpes Cazadores), puis (2) pouvoir 'après production' du Nid, puis seulement (3) balayage 1..6 des Gardiens. Une production hors phase (Le Miel des Ancêtres) ne crée que les jetons Insecte sans déclencher le pouvoir propre du Nid.",
        "Migration : chaque Insecte sur la roue peut se déplacer de 0 ou 1 cran (jusqu'à 2 avec L'Envol du Batará Suiveur), même s'il a bougé lors de la production d'un Nid. On retourne chaque jeton déplacé sur sa face verso pour suivi, puis on remet tous les jetons à l'endroit en fin de Migration avant d'évaluer la Colonisation.",
        "Depuis la dernière parcelle non rasée d'un rayon, 1 cran permet d'entrer sur n'importe quelle case 1..6 d'une piste globale (Bug du Cerveau ou Colonisation des Gardiens), sans limite de jetons par case. Cet aller simple est définitif."
      ]
    },
    {
      "numero": 5,
      "code": "ATTAQUES_ET_TEST_FIN",
      "nom": "Attaques des Machines et Vérification de Fin de Partie",
      "regles": [
        "Ordre des machines : Piste des Tactiques de 1 à 6, puis machines en Siège. Sur un même rayon au même rang (ou en Siège), l'Abatteuse agit toujours avant le Bulldozer ; entre rayons distincts au même rang, ordre libre entre les joueurs concernés.",
        "Chaque machine est résolue d'un seul tenant : lecture dynamique de ses cibles depuis sa position physique réelle à cet instant (en sautant toute Route Forestière) -> frappes -> avancée éventuelle -> gain éventuel de jeton rouge.",
        "Chaîne stricte des parades à chaque frappe : (1) Bond du Jaguar (Loi auto : 2 jetons bleus défaussés -> toutes frappes restantes de la machine parées + recul) -> (2) Piquée de la Harpie -> (3) Piège (Embuscade auto si Défense totale >= 1, locale ou soutenue à distance ; le Piège est marqué comme ayant servi) -> (4) Parade classique (Défenseurs + défausse immédiate des Insectes manquants).",
        "Contact Machine-Nid : tout mouvement de machine (avancée, recul, repli depuis une Route) entrant sur la parcelle d'un Nid non protégé renvoie ce Nid en lisière (reconstructible) et défausse tous les Insectes de la parcelle (Défenseurs et Piège restent).",
        "Création d'une Route Forestière (0 Arbre et 0 Souche après un Bulldozer) : recul automatique des machines présentes vers la prochaine parcelle non rasée côté bordure, ou vers le cœur uniquement si tout est déjà rasé côté bordure (maintien irréversible du statut de Siège ; retrait définitif de la partie si tout le rayon est rasé).",
        "Fin des attaques : effets 'à la fin des attaques' (ex. Ruches des Mélipones) et retrait de tout Piège ayant paré au moins 1 frappe durant le tour.",
        "Vérification de fin de partie : fin du Tour 8, Rêve en case 1, ou seuil fixe de Réveil atteint sur la Piste des Gardiens (seuil calculé une fois pour toutes à la mise en place : inactif si moins de 3 Gardiens dans la partie, sinon min(nb_joueurs, total_gardiens_partie) avec minimum 3 et plafond 5 à 6 joueurs ; tout Gardien renvoyé en lisière perd son marqueur). Si atteint : saut de l'Apprentissage et passage direct à la Repousse Finale."
      ]
    },
    {
      "numero": 6,
      "code": "APPRENTISSAGE_ET_MENAGE",
      "nom": "Apprentissage du Contremaître et Ménage de fin de tour",
      "regles": [
        "Calcul par machine active ce tour-ci (activée par carte OU en Siège T4) pour sa Tactique (T4 pour un Siège ; sans effet si T4 a été éjectée de la piste) : +1 par parcelle réellement endommagée (>= 1 Arbre coupé ou >= 1 Souche retirée) +1 par jeton Puissance rouge acquis ce tour -1 par jeton bleu Surchauffe présent sur la machine (plancher 0 par machine).",
        "Gain par machine : +1 par parcelle réellement endommagée (au moins 1 Arbre coupé ou 1 Souche retirée par cette machine), +1 par jeton rouge acquis en fin d'attaque, -1 par jeton bleu présent sur la machine.",
        "Réductions : application des retraits volontaires de tuiles (Voile de l'Oubli, Brume de la Dendrobate) AVANT les Insectes Bug du Cerveau (un Bug sur une case déjà à 0 jeton n'est pas défaussé et reste en place).",
        "Avancement : la Tactique strictement seule en tête avec au moins 1 jeton échange sa place avec sa voisine de gauche (y compris un Rêve, qui recule d'un cran à droite ; immobile si déjà en case 1). En cas d'égalité avec L'Écho des Voix Célestes amenant son Rêve en case 1, la fin de partie se déclenche immédiatement à la fin de ce tour (Repousse Finale).",
        "Ménage systématique : remise en réserve de 100 % des jetons d’Apprentissage de toutes les tuiles dans tous les cas, retrait des marqueurs 'utilisé' des Gardiens, retour en main des Défenseurs, et remélange du paquet Machine (hors machines en Siège) avec toutes les cartes Sabotage (révélées/écartées ce tour + nouvellement acquises ce tour)."
      ]
    }
  ],
  "arbitrages_valides": {
    "A01": "Lecture épurée des dés sous paravent : seul un joueur ayant tiré une carte Machine retient M = min(D1, D2) (ou max sous Loi). Si le rang M porte un Rêve en 3.2, la machine est annulée et le Rêve s’ouvre.",
    "A02": "Rêve sur dé Machine : annule l'activation de la machine et peut ouvrir ce Rêve (max 1 ouverture par Rêve et par tour).",
    "A03": "Furtivité à 4 emplacements (2 jumeaux/rive) : entrer sur la case tire l'autre jeton sur le jumeau et oriente l'action unique ; retourner en choix définitif se fait sur place sans déplacement.",
    "A04": "Gouvernance unitaire : chaque tuile de Synergie et piste de Migration est décidée uniquement par son Peuple d'origine.",
    "A05": "Parade classique sans dette : défausse immédiate à la frappe des Insectes requis ; suppression totale des Insectes engagés.",
    "A06": "Armement des Pièges : Embuscade dès que Défense totale >= 1 (locale ou à distance) ; tout Piège ayant paré >= 1 fois dans le tour est retiré en fin d'attaques.",
    "A07": "Zéro verrouillage des parcelles ciblées : Insectes toujours libres tant que présents ; seul un Piège déjà déclenché ce tour-ci ne peut plus payer de coût volontaire.",
    "A08": "Pont routier : Routes Forestières systématiquement sautées le long d'un rayon, mais infranchissables/inoccupables latéralement.",
    "A09": "Repli sur création de Route : recul automatique vers la bordure par défaut, vers le cœur seulement si bord tout rasé, retrait si rayon tout rasé ; Siège irréversible maintenu.",
    "A10": "Autonomie et Apprentissage du Siège : l’attaque d’une machine en Siège reste active même si la tuile T4 est éjectée ; en 6.1, une machine en Siège génère normalement ses jetons d’Apprentissage sur T4 tant que T4 figure sur la Piste des Tactiques (ignorés si T4 est éjectée).",
    "A11": "Insertion d'un Rêve : éjecte la Tactique la plus à droite ; seules les tuiles à droite du trou glissent à gauche ; pose en case 6 ; Bugs fixes sur les cases.",
    "A12": "Cascades de Gardiens : fin complète de l'effet en cours, marquage immédiat à l'ouverture, balayage à plat de 1 à 6 sans pile imbriquée.",
    "A13": "Faces 2 et Lois passives : seule la face visible s'applique (Faces 2 autonomes) ; une Loi passive reçoit automatiquement son marqueur dès que sa case s'allume.",
    "A14": "Seuil de Réveil fixe : calculé à la mise en place (inactif si < 3 Gardiens en jeu) ; retour en lisière efface le marqueur.",
    "A15": "Test de fin de partie : maintenu en fin d'attaques (saut Apprentissage), avec déclenchement en fin d'Apprentissage si L'Écho des Voix Célestes amène son Rêve en case 1.",
    "A16": "Contact Machine-Nid : tout mouvement entrant (avancée, recul, repli) renvoie le Nid reconstructible en lisière et défausse tous les Insectes de la parcelle.",
    "A17": "Migration des Insectes : 0 ou 1 cran facultatif (suivi par retournement des pions) ; aller simple définitif et sans limite vers les pistes globales.",
    "A18": "Production des Nids : bloc indivisible (création selon état réel présent + pouvoir du Nid avant Gardiens) ; Miel des Ancêtres restreint aux jetons Insecte.",
    "A19": "Cibles dynamiques : lues selon la position physique réelle de la machine à l’instant où elle attaque.",
    "A20": "Matamata et chaîne des parades : Matamata vérifie la présence d'une Souche à chaque frappe ; ordre Jaguar -> Harpie -> Piège -> Parade classique.",
    "A21": "Anti-blocage et Nids : pose interdite sur case morte/tuile inconstructible ; 1 seul Nid par parcelle sans machine ; choix du bâtisseur libéré par Peuple d'origine.",
    "A22": "Communication muette : silence tactique sous paravent fermé ; simple visibilité publique sans concertation orale sous l'Ara.",
    "A23": "Apprentissage : dommage réel requis (>= 1 Arbre coupé ou Souche retirée) ; retraits volontaires avant Bugs ; remise à zéro intégrale en fin d'étape.",
    "A24": "Cartes Sabotage (dilution permanente) : toutes identiques et sans effet propre (réserve illimitée). 1 Sabotage acquis ajoute définitivement 1 carte Sabotage au paquet Machine (allume 3. Sabotage) ; 1 carte Sabotage tirée à l’Étape 1 fait perdre 1 activation au Contremaître puis est remélangée en fin de tour.",
    "A25": "Séquence des attaques : Tactiques 1..6 puis Sièges ; Abatteuse avant Bulldozer sur un même rayon, libre entre rayons distincts ; machine résolue d'un seul tenant."
  }
};
if (typeof window !== "undefined") {
  window.SPEC_FORMELLE_V5_3 = SPEC_FORMELLE_V5_3;
}
// === END SPEC_FORMELLE_V5_3 ===
