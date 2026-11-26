// =========================================================================
// data/panels_v6_3_data.js — Généré automatiquement depuis contracts/panels/ (Atelier v6.3.1 · 3 panels · 32 pictogrammes)
// NE PAS ÉDITER À LA MAIN : exécuter `uv run python scripts/build_studio_artifacts.py`.
// =========================================================================
const REFERENTIEL_PICTOGRAMMES_V6_3 = {
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
    "libelle": "Cale sous machine mobile (Reptiles)",
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
    "libelle": "Déplacement / avancée de Rêve",
    "symbole": "⬅️"
  },
  "PIC_ANNULATION": {
    "code": "PIC_ANNULATION",
    "categorie": "PISTE_TACTIQUES",
    "libelle": "Machine annulée (jeton incliné 90°)",
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
    "libelle": "Icône Résonance / cascade de Gardiens",
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
  "PIC_PLUME": {
    "code": "PIC_PLUME",
    "categorie": "ACCESSOIRES",
    "libelle": "Plume de Vigie — Chaud / Calme (Oiseaux)",
    "symbole": "🪶"
  },
  "PIC_PERCHOIR": {
    "code": "PIC_PERCHOIR",
    "categorie": "ACCESSOIRES",
    "libelle": "Perchoir de Vigie & Dé d’Envol (Oiseaux)",
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
    "libelle": "Migration / phorésie de l’Essaim",
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

const CASTING_GARDIENS_V6_3 = {
  "G1": {
    "alias_oriente": "M>R",
    "nom_animal": "Le Jaguar",
    "origine": "M",
    "voisin": "R"
  },
  "G2": {
    "alias_oriente": "R>M",
    "nom_animal": "L’Anaconda vert",
    "origine": "R",
    "voisin": "M"
  },
  "G3": {
    "alias_oriente": "M>O",
    "nom_animal": "L’Atèle",
    "origine": "M",
    "voisin": "O"
  },
  "G4": {
    "alias_oriente": "O>M",
    "nom_animal": "L’Ara rouge",
    "origine": "O",
    "voisin": "M"
  },
  "G5": {
    "alias_oriente": "R>O",
    "nom_animal": "L’Iguane vert",
    "origine": "R",
    "voisin": "O"
  },
  "G6": {
    "alias_oriente": "O>R",
    "nom_animal": "Le Toucan toco",
    "origine": "O",
    "voisin": "R"
  },
  "G7": {
    "alias_oriente": "M>H",
    "nom_animal": "Le Tapir",
    "origine": "M",
    "voisin": "H"
  },
  "G8": {
    "alias_oriente": "M>E",
    "nom_animal": "Le Boto",
    "origine": "M",
    "voisin": "E"
  },
  "G9": {
    "alias_oriente": "R>H",
    "nom_animal": "Le Caïman noir",
    "origine": "R",
    "voisin": "H"
  },
  "G10": {
    "alias_oriente": "R>E",
    "nom_animal": "La Matamata",
    "origine": "R",
    "voisin": "E"
  },
  "G11": {
    "alias_oriente": "O>H",
    "nom_animal": "La Harpie féroce",
    "origine": "O",
    "voisin": "H"
  },
  "G12": {
    "alias_oriente": "O>E",
    "nom_animal": "L’Ibijau",
    "origine": "O",
    "voisin": "E"
  },
  "G13": {
    "alias_oriente": "M>I",
    "nom_animal": "Le Tamanoir",
    "origine": "M",
    "voisin": "I"
  },
  "G14": {
    "alias_oriente": "R>I",
    "nom_animal": "Le Téju",
    "origine": "R",
    "voisin": "I"
  },
  "G15": {
    "alias_oriente": "O>I",
    "nom_animal": "Le Colibri",
    "origine": "O",
    "voisin": "I"
  }
};

const SLOTS_SPEC_V6_3 = [
  {
    "id": "G1",
    "famille": "GARDIEN",
    "origine": "M",
    "voisin": "R",
    "alias_oriente": "M>R"
  },
  {
    "id": "G2",
    "famille": "GARDIEN",
    "origine": "R",
    "voisin": "M",
    "alias_oriente": "R>M"
  },
  {
    "id": "G3",
    "famille": "GARDIEN",
    "origine": "M",
    "voisin": "O",
    "alias_oriente": "M>O"
  },
  {
    "id": "G4",
    "famille": "GARDIEN",
    "origine": "O",
    "voisin": "M",
    "alias_oriente": "O>M"
  },
  {
    "id": "G5",
    "famille": "GARDIEN",
    "origine": "R",
    "voisin": "O",
    "alias_oriente": "R>O"
  },
  {
    "id": "G6",
    "famille": "GARDIEN",
    "origine": "O",
    "voisin": "R",
    "alias_oriente": "O>R"
  },
  {
    "id": "G7",
    "famille": "GARDIEN",
    "origine": "M",
    "voisin": "H",
    "alias_oriente": "M>H"
  },
  {
    "id": "G8",
    "famille": "GARDIEN",
    "origine": "M",
    "voisin": "E",
    "alias_oriente": "M>E"
  },
  {
    "id": "G9",
    "famille": "GARDIEN",
    "origine": "R",
    "voisin": "H",
    "alias_oriente": "R>H"
  },
  {
    "id": "G10",
    "famille": "GARDIEN",
    "origine": "R",
    "voisin": "E",
    "alias_oriente": "R>E"
  },
  {
    "id": "G11",
    "famille": "GARDIEN",
    "origine": "O",
    "voisin": "H",
    "alias_oriente": "O>H"
  },
  {
    "id": "G12",
    "famille": "GARDIEN",
    "origine": "O",
    "voisin": "E",
    "alias_oriente": "O>E"
  },
  {
    "id": "G13",
    "famille": "GARDIEN",
    "origine": "M",
    "voisin": "I",
    "alias_oriente": "M>I"
  },
  {
    "id": "G14",
    "famille": "GARDIEN",
    "origine": "R",
    "voisin": "I",
    "alias_oriente": "R>I"
  },
  {
    "id": "G15",
    "famille": "GARDIEN",
    "origine": "O",
    "voisin": "I",
    "alias_oriente": "O>I"
  },
  {
    "id": "R1",
    "famille": "REVE",
    "origine": "H",
    "voisin": "E",
    "alias_oriente": "H>E"
  },
  {
    "id": "R2",
    "famille": "REVE",
    "origine": "E",
    "voisin": "H",
    "alias_oriente": "E>H"
  },
  {
    "id": "R3",
    "famille": "REVE",
    "origine": "H",
    "voisin": "M",
    "alias_oriente": "H>M"
  },
  {
    "id": "R4",
    "famille": "REVE",
    "origine": "H",
    "voisin": "R",
    "alias_oriente": "H>R"
  },
  {
    "id": "R5",
    "famille": "REVE",
    "origine": "H",
    "voisin": "O",
    "alias_oriente": "H>O"
  },
  {
    "id": "R6",
    "famille": "REVE",
    "origine": "H",
    "voisin": "I",
    "alias_oriente": "H>I"
  },
  {
    "id": "R7",
    "famille": "REVE",
    "origine": "E",
    "voisin": "M",
    "alias_oriente": "E>M"
  },
  {
    "id": "R8",
    "famille": "REVE",
    "origine": "E",
    "voisin": "R",
    "alias_oriente": "E>R"
  },
  {
    "id": "R9",
    "famille": "REVE",
    "origine": "E",
    "voisin": "O",
    "alias_oriente": "E>O"
  },
  {
    "id": "R10",
    "famille": "REVE",
    "origine": "E",
    "voisin": "I",
    "alias_oriente": "E>I"
  },
  {
    "id": "M1",
    "famille": "CROISSANCE",
    "origine": "I",
    "voisin": "M",
    "alias_oriente": "I>M"
  },
  {
    "id": "M2",
    "famille": "CROISSANCE",
    "origine": "I",
    "voisin": "R",
    "alias_oriente": "I>R"
  },
  {
    "id": "M3",
    "famille": "CROISSANCE",
    "origine": "I",
    "voisin": "O",
    "alias_oriente": "I>O"
  },
  {
    "id": "M4",
    "famille": "CROISSANCE",
    "origine": "I",
    "voisin": "H",
    "alias_oriente": "I>H"
  },
  {
    "id": "M5",
    "famille": "CROISSANCE",
    "origine": "I",
    "voisin": "E",
    "alias_oriente": "I>E"
  }
];

const PANELS_V6_3 = {
  "panel_1": {
    "_meta": {
      "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
      "schema_version": "6.3.1",
      "socle_verrouille": "6.2.0",
      "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
      "etape_active": "ETAPE_2_CONCEPTION_CREATIVE",
      "statut_global": "CONCEPTION_EN_COURS",
      "genere_le": "2026-11-26",
      "slots_count": 30,
      "c02_supprime": true,
      "panel_id": "panel_1",
      "source_modele": "Modèle 1 — Candidat 1 (19 inchangés) + REPONSE_IA1 (11 révisés)",
      "murs_porteurs_verrouilles": [
        "M1_TEMPS_BATAILLE",
        "M2_CONSERVATION_THERMIQUE",
        "M3_INTEGRITE_PLATEAU_ET_ICONES",
        "M4_AUTONOMIE_PLANCHER_SOLO"
      ],
      "note_retrocompatibilite": "Panel candidat panel_1 compilé en v6.3.1 (4 murs porteurs M1..M4, séparation entrees_plancher / entrees_synergie, 32 pictogrammes officiels) pour arbitrage d'auteur de l'Étape 2b."
    },
    "carte_des_roles": {
      "statut": "PASSE_1_CREATIF_V6_3_1",
      "partition_2K3": {
        "triangle_1": "R>M (G2) → M>H (G7) → H>R (R4)",
        "triangle_2": "O>E (G12) → E>I (R10) → I>O (M3)"
      },
      "etoile_lois_passives": "Toutes les lois sont sur une lisière de E (étoile centrée sur les Entités) : au plus 2 lois sur toute assise.",
      "roles": {
        "catalyseurs_eveil": [
          "G1=M>R",
          "G3=M>O",
          "G4=O>M",
          "G5=R>O",
          "G8=M>E",
          "G9=R>H",
          "G11=O>H",
          "G12=O>E",
          "G13=M>I",
          "G14=R>I",
          "G15=O>I"
        ],
        "leviers_reve": [
          "G8=M>E",
          "R1=H>E",
          "R2=E>H",
          "R4=H>R",
          "R8=E>R",
          "R9=E>O",
          "R10=E>I"
        ],
        "synergies_enracinement": [
          "G3=M>O",
          "G7=M>H",
          "G15=O>I",
          "R1=H>E"
        ],
        "lois_passives": [
          "R2=E>H",
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
        "nombre": 11
      },
      "I05_couverture_sommeil": {
        "verdict": "OK",
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
        "nombre": 4,
        "max_par_assise": 2
      },
      "Q02_twists_2K3": {
        "verdict": "OK",
        "nombre": 6
      },
      "synergies_optionnelles_couvertes": 23
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
          "CATALYSEUR_EVEIL",
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "Arbres debout contigus entre rayons voisins → franchissement latéral de Défenseurs (et du Duel) → Parade chez le voisin ; Plume Chaud (O) ouvre une trouée",
        "entrees_plancher": [
          "ARBRE",
          "PLUME"
        ],
        "entrees_synergie": [
          "DUEL"
        ],
        "entrees": [
          "ARBRE",
          "PLUME",
          "DUEL"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "PARADE_CANOPEE",
          "ARBRE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Chaque activation fait traverser un Défenseur différent, ou le même deux fois : la troupe pare au rang 1 sur un rayon, puis passe chez le voisin pour parer au rang 4. Chaque parade ainsi complétée allume Parade, l’icône même de l’Atèle.",
        "tags": [
          "CANOPEE",
          "LATERAL",
          "ENRACINEMENT"
        ],
        "tuile_plateau": {
          "nom_court": "L’Atèle",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_DEFENSEUR",
            "PIC_ARBRE",
            "PIC_PLUME",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "1 Défenseur → même numéro du rayon voisin · Arbre debout des deux côtés",
            "face_2": "Troupe de 2 · traversée en chaîne · Plume Chaud franchit 1 clairière",
            "enracine": "Canopée intacte → 1 repousse de plus chez le voisin"
          },
          "resume_plateau": "Pont de canopée entre rayons voisins"
        },
        "carte_joueur": {
          "titre_complet": "L’Atèle, funambule de la canopée",
          "entite_illustree": "L’Atèle (Ateles chamek) — singe-araignée entier, suspendu par sa queue préhensile entre deux couronnes d’arbres",
          "brief_illustration": "Contre-plongée vertigineuse : un Atèle noir, bras démesurés tendus, la queue enroulée autour d’une branche, franchit le vide entre deux cimes ; sous lui, une trouée de souches coupées interrompt la canopée ; un ara rouge observe depuis une branche. Lumière dorée de fin d’après-midi.",
          "pitch_ambiance": "L’Atèle ne descend presque jamais au sol : sa route, c’est le toit de la forêt. Tant que les cimes se touchent, la troupe passe d’un territoire à l’autre ; qu’une trouée s’ouvre, et le chemin se rompt.",
          "texte_regle": {
            "face_1": "Quand l’Atèle s’active : faites franchir la canopée à 1 Défenseur (de n’importe quel joueur, sur sa face actuelle) : déplacez-le d’une parcelle vers la parcelle de même numéro d’un rayon voisin, à condition que ces deux parcelles portent chacune au moins 1 Arbre debout. Une Route Forestière ou une parcelle réduite à des Souches rompt la canopée : aucun franchissement depuis elle ni vers elle. Si ce Défenseur accompagnait le jeton Duel, le Duel le suit sur sa face actuelle. Arrivé, le Défenseur compte normalement pour toutes les frappes qui n’ont pas encore été résolues.",
            "face_2": "Quand l’Atèle s’active : faites franchir la canopée à une troupe d’au plus 2 Défenseurs partis de la même parcelle (et au jeton Duel s’il les accompagne). Déplacez-les ensemble vers la parcelle de même numéro d’un rayon voisin, puis, si vous le voulez, poursuivez de rayon voisin en rayon voisin tant que la canopée reste continue : chaque parcelle traversée, à ce même numéro, porte au moins 1 Arbre debout. La troupe s’arrête où vous voulez. Une Route Forestière l’arrête toujours ; mais si la Plume de Vigie est posée face Chaud au pied du rayon d’arrivée, la troupe peut traverser ou atteindre une parcelle réduite à des Souches. Arrivés, les Défenseurs comptent pour toutes les frappes non encore résolues.",
            "enracine": "Enraciné : l’Atèle sème par-delà la lisière. Au décompte final, si la parcelle face à laquelle il est enraciné et la parcelle de même numéro d’un rayon voisin portent toutes deux encore au moins 1 Arbre debout (la canopée tient), retournez 1 Souche de cette parcelle voisine en Arbre debout, en plus de sa repousse normale."
          },
          "decision_et_renoncement": {
            "choix": "Quel Défenseur faire traverser, et vers quel voisin : renforcer la frappe imminente d’à côté ou garder la parcelle de départ.",
            "renoncement": "Le Défenseur qui traverse abandonne les frappes à venir sur sa parcelle d’origine ; et laisser une parcelle devenir clairière rompt durablement le pont."
          }
        },
        "temoins": [
          {
            "id": "G3_T1",
            "resume": "Défenseur O sur la parcelle 2 (2 Arbres) du rayon O ; la parcelle 2 du rayon M (1 Arbre) est visée au rang 4 avec 1 Défenseur, seuil 2 ; l’Atèle s’active après une parade au rang 1 : le Défenseur passe sur la parcelle 2 du rayon M, la frappe du rang 4 est parée.",
            "etat_attendu_verifie": {
              "rayon_M_p2_defenseurs": 2,
              "parade_rang_4": true,
              "icone": "PARADE"
            },
            "statut": "A_CODER"
          },
          {
            "id": "G3_T2",
            "resume": "La parcelle 3 du rayon voisin est réduite à des Souches : franchissement refusé en Face 1, accepté en Face 2 si la Plume est face Chaud au pied de ce rayon.",
            "etat_attendu_verifie": {
              "face_1": "FRANCHISSEMENT_INTERDIT",
              "face_2_plume_chaud": "FRANCHISSEMENT_AUTORISE"
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade. Faire traverser le Défenseur dont la parcelle n’est plus visée par aucune frappe non résolue vers la parcelle voisine visée dont le déficit au Seuil est exactement 1.",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "Machine annulée par Rêve (ou proie de passage déjà activée) → avalée hors du sac tant qu’une encoche reste occupée au ménage ; Face 2 : avale sur clairière de Souches",
        "entrees_plancher": [
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "ANNULATION",
          "SOUCHE"
        ],
        "entrees": [
          "RANG_MACHINE",
          "ANNULATION",
          "SOUCHE"
        ],
        "sorties": [
          "JETON_AVALE",
          "ANNULATION"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": "La première activation avale la proie de l’ouverture ; la seconde peut l’échanger contre une machine plus dangereuse annulée plus à droite, ou (Face 2) avaler une machine posée sur une clairière avant qu’elle ne frappe. Seule en piste, la seconde troque la proie de passage contre la machine la plus proche de la dernière parcelle, pour lui interdire le Ratissage. Chaque activation glisse un pari : or c’est une encoche occupée au ménage qui empêche la Matamata de digérer.",
        "tags": [
          "SAC",
          "CAMOUFLAGE",
          "CLAIRIERE"
        ],
        "tuile_plateau": {
          "nom_court": "La Matamata",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_REVE",
          "pictogrammes": [
            "PIC_REVE",
            "PIC_ANNULATION",
            "PIC_SOUCHE",
            "PIC_PARI_ENCOCHE"
          ],
          "mots_cles_plateau": {
            "face_1": "Machine annulée par un Rêve → jeton avalé hors du sac · sans annulation : machine qui a déjà attaqué · encoche vide au ménage = proie rendue",
            "face_2": "Ou machine révélée sur clairière de Souches → annulée et avalée",
            "enracine": null
          },
          "resume_plateau": "Avale un jeton Machine et le garde hors du sac"
        },
        "carte_joueur": {
          "titre_complet": "La Matamata, la souche qui respire",
          "entite_illustree": "La Matamata (Chelus fimbriata), tortue d’eau douce entière au fond d’un ruisseau ambré",
          "brief_illustration": "La Matamata (Chelus fimbriata), tortue d’eau douce entière, carapace d’écorce et tête frangée de feuilles mortes, immobile au fond d’un ruisseau ambré, la gueule entrouverte.",
          "pitch_ambiance": "On la prend pour une souche, pour un tas de feuilles mortes. Puis la gueule s’ouvre en un éclair et l’eau s’engouffre : la proie a disparu avant même d’avoir compris.",
          "texte_regle": {
            "face_1": "La gueule. Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture (son jeton est encore incliné devant son rayon). La Matamata l’avale : posez son jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée (elle n’attaque pas) et ne peut pas entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.\nProie de passage (plancher) : si aucun Rêve n’a annulé de machine à cette ouverture, la Matamata avale à la place, de la même façon, le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).\nDigestion : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.",
            "face_2": "L’affût de la clairière. Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture, ou une machine révélée qui n’a pas encore attaqué et qui se trouve sur une parcelle réduite à des Souches (aucun Arbre debout). La Matamata l’avale : la seconde est annulée (inclinez son jeton) ; posez ce jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée ni entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.\nProie de passage (plancher) : si aucune de ces deux proies n’existe, la Matamata avale à la place le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).\nDigestion : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Garder la même proie tour après tour (en pariant sur la Matamata) ou l’échanger contre une machine plus menaçante.",
            "renoncement": "Pour ne pas digérer, la Matamata exige une encoche occupée à chaque ménage — un Défenseur engagé en pari sur elle plutôt qu’en forêt."
          }
        },
        "temoins": [
          {
            "id": "G10_T1",
            "resume": "Un Rêve au rang 2 annule le Bulldozer du rayon E ; la Matamata (sur Rêve) s’active : jeton avalé ; au tour suivant, le sac contient 2N − 1 jetons Machine.",
            "etat_attendu_verifie": {
              "jeton_avale": true,
              "sac_diminue_de_1": true
            },
            "statut": "A_CODER"
          },
          {
            "id": "G10_T2",
            "resume": "Plancher (Tour 2, aucun Rêve construit) : l’Abatteuse du rayon E a frappé au rang 2 ; au rang 3, une parade allume Parade : la Matamata, construite au Tour 1 et posée sur Parade (icône de repli), avale le jeton de cette Abatteuse. Au ménage, une encoche est occupée : pas de digestion ; au Tour 3, l’Abatteuse reste hors du sac et ne peut pas entrer en Ratissage.",
            "etat_attendu_verifie": {
              "proie_de_passage_avalee": true,
              "digestion_evitee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Rêve (ou Parade en repli sans Rêve). Avaler la machine la plus avancée vers la dernière parcelle ; garder la proie tant qu’un Défenseur peut parier sur la Matamata chaque tour.",
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
        "vecteurs": "Sabotage perché (O) échangé contre une machine révélée → Sabotage rallumé ; Face 2 : proie perchée lâchée sur le rang d’un Rêve Humain (H)",
        "entrees_plancher": [
          "PERCHOIR",
          "SABOTAGE"
        ],
        "entrees_synergie": [
          "POSITION_REVE"
        ],
        "entrees": [
          "PERCHOIR",
          "SABOTAGE",
          "POSITION_REVE"
        ],
        "sorties": [
          "PROIE_ARRACHEE",
          "SABOTAGE",
          "RECUL"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE"
        ],
        "double_ouverture": "Le Perchoir change de nature après un piqué : il porte la machine arrachée. La seconde activation emporte cette proie d’1 parcelle (Face 1) ou la lâche sur le rang d’un Rêve Humain qui l’annule (Face 2) : deux machines neutralisées pour un seul Sabotage perché. Chaque Sabotage révélé rallume la Piste.",
        "tags": [
          "PERCHOIR",
          "SAC",
          "SABOTAGE"
        ],
        "tuile_plateau": {
          "nom_court": "La Harpie féroce",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_PERCHOIR",
            "PIC_SABOTAGE",
            "PIC_ANNULATION",
            "PIC_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Sabotage du Perchoir ↔ machine révélée · Sabotage rallumé · proie perchée recule",
            "face_2": "Tout jeton du Perchoir ↔ machine · machine perchée lâchée au rang d’un Rêve Humain",
            "enracine": null
          },
          "resume_plateau": "Arrache une machine depuis le Perchoir"
        },
        "carte_joueur": {
          "titre_complet": "La Harpie féroce, reine des hautes cimes",
          "entite_illustree": "La Harpie féroce (Harpia harpyja) — aigle géant entier, huppe dressée, perché au sommet d’un fromager émergent",
          "brief_illustration": "Au-dessus d’une mer de canopée, la Harpie féroce entière fond depuis la plus haute branche d’un fromager, ailes ployées, pattes énormes tendues vers une machine en contrebas dont elle arrache un jeton lumineux ; sur une branche voisine, une coiffe de plumes de chamane. Gris ardoise, blanc, ciel d’orage.",
          "pitch_ambiance": "La Harpie peut guetter une journée entière sans bouger une plume. Puis elle plonge à travers les branches et emporte sa proie dans les hauteurs, là où personne ne la reprendra.",
          "texte_regle": {
            "face_1": "Quand la Harpie féroce s’active : si le jeton posé sur le Perchoir de Vigie est un Sabotage ou une Écaille, la Harpie fond sur sa proie : échangez-le avec le jeton d’une machine révélée qui n’est ni annulée ni encore résolue. Cette machine perd son activation : son jeton rejoint le Perchoir, face cachée. Le Sabotage ou l’Écaille, révélé à sa place, allume l’icône Sabotage, puis balayage (une Écaille pose aussi le Croc, comme d’habitude). Si le Perchoir porte déjà un jeton Machine, la Harpie emporte cette proie : faites reculer la machine correspondante d’1 parcelle vers la bordure.",
            "face_2": "Quand la Harpie féroce s’active : échangez le jeton posé sur le Perchoir de Vigie avec le jeton d’une machine révélée qui n’est ni annulée ni encore résolue ; cette machine perd son activation et son jeton rejoint le Perchoir, face cachée. Si le jeton venu du Perchoir est un Sabotage ou une Écaille, il est révélé à sa place : il allume l’icône Sabotage, puis balayage (une Écaille pose aussi le Croc). Si c’est un jeton Machine, la Harpie lâche cette proie dans le rêve des hommes : sa machine est révélée sur le rang d’un Rêve Humain défendu qui n’a pas encore été résolu, où ce Rêve pourra l’annuler ; sans un tel Rêve, cet échange est impossible.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Au tirage, l’Oiseau choisit quel jeton percher : garder la Machine et percher le Sabotage pour la Harpie, ou l’inverse.",
            "renoncement": "Percher le Sabotage oblige l’Oiseau à jouer lui-même la Machine et ses dés ; une Harpie qui ne s’active pas laisse ce Sabotage inutile au Perchoir."
          }
        },
        "temoins": [
          {
            "id": "G11_T1",
            "resume": "Perchoir = Sabotage ; un Bulldozer est révélé au rang 2 ; la Harpie (sur Sabotage) s’active au premier Sabotage : échange ; le Bulldozer est inactif, le Sabotage révélé rallume Sabotage, la mobilisation de son rayon baisse de 1.",
            "etat_attendu_verifie": {
              "bulldozer": "INACTIF",
              "perchoir": "JETON_BULLDOZER",
              "icone": "SABOTAGE",
              "mobilisation_rayon": "-1"
            },
            "statut": "A_CODER"
          },
          {
            "id": "G11_T2",
            "resume": "Face 2 : le Perchoir porte l’Abatteuse du rayon O ; un Rêve Humain défendu au rang 5 n’est pas résolu ; échange avec la machine du rang 1 : l’Abatteuse est révélée au rang 5 puis annulée par le Rêve.",
            "etat_attendu_verifie": {
              "machine_rang_1": "INACTIVE",
              "abatteuse_O": {
                "rang": 5,
                "annulee": true
              }
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Sabotage. Percher un Sabotage dès qu’il est vu et que la Harpie est construite ; arracher la machine révélée en Assaut qui vise la parcelle la plus boisée.",
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
        "cycle": "PASSIF_CONTINU",
        "cablage": null,
        "roles_portes": [
          "AUTONOMIE_A0",
          "LOI_PASSIVE",
          "LEVIER_REVE"
        ],
        "est_twist": false,
        "vecteurs": "Chant (H) assoupli par la loi de la Iara (E) → glissement de Rêve dès la première annulation ; machines laissées au rang envoûtées (Altération)",
        "entrees_plancher": [
          "CHANT",
          "ANNULATION"
        ],
        "entrees_synergie": [],
        "entrees": [
          "CHANT",
          "ANNULATION"
        ],
        "sorties": [
          "GLISSEMENT_CHANT",
          "ALTERATION"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "LOI",
          "CHANT",
          "ALTERATION"
        ],
        "tuile_plateau": {
          "nom_court": "La Iara",
          "fenetre_badge": "PERMANENT",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_LOI_PASSIVE",
            "PIC_CHANT",
            "PIC_AVANCEE_REVE",
            "PIC_ALTERATION"
          ],
          "mots_cles_plateau": {
            "face_1": "Loi · le Chant fait glisser dès 1 machine annulée · restantes du rang = Altération",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Le Chant remonte le fleuve plus facilement"
        },
        "carte_joueur": {
          "titre_complet": "La Iara, mère des eaux",
          "entite_illustree": "La Iara (Mãe-d’água) — entité des rivières, femme aux longs cheveux noirs et à la queue de poisson, chantant sur un rocher au crépuscule",
          "brief_illustration": "Crépuscule sur un rapide : la Iara assise sur un rocher, queue écailleuse dans l’écume, chevelure ruisselante, chante ; ses notes visibles comme des volutes dorées s’enroulent autour d’un Rêve qu’elles entraînent vers l’amont. Bleus profonds, or, écume blanche.",
          "pitch_ambiance": "Les pêcheurs qui entendent la Iara chanter ne rentrent pas au village. Mais pour qui la sert, son chant fait remonter les rêves vers leur source.",
          "texte_regle": {
            "face_1": "Loi passive — Le chant qui remonte le fleuve (tant que la Iara est sur la Réglette, défendue ou non) : un Rêve défendu par le Chant glisse d’1 rang vers la gauche, si ce rang est libre, dès qu’il annule au moins 1 machine, même si une autre machine reste active à son rang. Pouvoir de la Iara (quand elle est défendue, à sa résolution) : l’envoûtement : chaque machine mobile de son rang qui reste non annulée, faute de Défenseurs, reçoit 1 jeton d’Altération si elle n’en porte pas déjà.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Où poser le Chant : sur le Rêve qui annulera au moins une machine, même partiellement couvert, pour le faire remonter.",
            "renoncement": "Un Rêve qui glisse en laissant une machine active la laisse frapper ; et défendre la Iara mobilise un Défenseur qui aurait pu garder la forêt."
          }
        },
        "temoins": [
          {
            "id": "R2_T1",
            "resume": "Chant sur un Rêve H au rang 4 où tombent 2 machines ; il en annule 1 : grâce à la loi, le Rêve glisse au rang 3 bien qu’une machine reste active.",
            "etat_attendu_verifie": {
              "reve_H_rang": 3,
              "machine_active_restante": 1
            },
            "statut": "A_CODER"
          },
          {
            "id": "R2_T2",
            "resume": "La Iara, défendue par 1 Défenseur au rang 5, reçoit 2 machines : 1 annulée, l’autre reçoit 1 Altération (elle reculera sans frapper à sa prochaine révélation).",
            "etat_attendu_verifie": {
              "annulees": 1,
              "alterations_posees": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Défendre un Rêve avec le Chant dès qu’une machine est probable à son rang ; défendre la Iara quand au moins 2 machines peuvent y tomber.",
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
        "vecteurs": "Dé d’Envol (O) → second rang d’annulation pour un Rêve Humain (H)",
        "entrees_plancher": [
          "DE_ENVOL",
          "RANG_REVE"
        ],
        "entrees_synergie": [
          "ANNULATION"
        ],
        "entrees": [
          "DE_ENVOL",
          "RANG_REVE",
          "ANNULATION"
        ],
        "sorties": [
          "ANNULATION_ENVOL"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "DE_ENVOL",
          "DES",
          "ANNULATION"
        ],
        "tuile_plateau": {
          "nom_court": "Le Chamane-Oiseau",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_REVE",
            "PIC_PERCHOIR",
            "PIC_ANNULATION",
            "PIC_DES_PARAVENT"
          ],
          "mots_cles_plateau": {
            "face_1": "Annule aussi au rang du Dé d’Envol · 1 machine par Défenseur au total",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Un Rêve qui veille sur deux rangs"
        },
        "carte_joueur": {
          "titre_complet": "Le Vol du Chamane-Oiseau",
          "entite_illustree": "Vision chamanique du vol de l’âme — un chamane dont l’esprit s’élève en oiseau au-dessus de la canopée",
          "brief_illustration": "Vue aérienne onirique : au-dessus d’une mer d’arbres, une silhouette humaine aux bras devenus ailes de plumes rouges et bleues plane à côté d’un dé lumineux en plein vol ; plus bas, deux rangs de la Réglette s’illuminent à la fois. Rouges, bleus, blanc nacré.",
          "pitch_ambiance": "Quand le chamane chante jusqu’à l’aube, son âme quitte son corps et prend des plumes. De là-haut, elle voit deux chemins à la fois : celui où dort le rêve, et celui où l’oiseau a lancé son dé.",
          "texte_regle": {
            "face_1": "Quand ce Rêve est défendu, à sa résolution : l’âme du chamane s’envole avec le Dé d’Envol. Ce Rêve peut annuler, en plus des machines de son propre rang, les machines révélées sur le rang indiqué par le Dé d’Envol de l’Oiseau, toujours à raison d’1 machine par Défenseur au total. Une machine annulée ainsi ne peut plus l’être par le Rêve qui occupe éventuellement ce rang.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Défendre ce Rêve avec plusieurs Défenseurs pour couvrir deux rangs, ou n’en garder qu’un pour la forêt.",
            "renoncement": "Le Dé d’Envol n’est connu qu’à l’ouverture : un Défenseur posé ici peut n’avoir rien à annuler si aucun des deux rangs ne reçoit de machine."
          }
        },
        "temoins": [
          {
            "id": "R5_T1",
            "resume": "Rêve H au rang 6 défendu par 2 Défenseurs ; Dé d’Envol = 1 ; deux machines révélées au rang 1 : toutes deux annulées.",
            "etat_attendu_verifie": {
              "annulees": 2,
              "rang_envol": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Défendre avec 2 Défenseurs quand le Rêve occupe le rang 5 ou 6 : le Dé d’Envol ramène souvent l’annulation vers un rang fréquent.",
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
        "vecteurs": "Rang du Boitatá (E) → Rouges retournés contre la machine dans le Seuil ; annulations qui nourrissent la gueule de la Matamata (R) ; le serpent ondule vers la gauche",
        "entrees_plancher": [
          "ROUGE",
          "RANG_REVE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "ROUGE",
          "RANG_REVE",
          "RANG_MACHINE"
        ],
        "sorties": [
          "ROUGE_RETOURNE",
          "POSITION_REVE",
          "ANNULATION"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "LOI",
          "SURCHAUFFE",
          "LEVIER"
        ],
        "tuile_plateau": {
          "nom_court": "Le Boitatá",
          "fenetre_badge": "PERMANENT",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_LOI_PASSIVE",
            "PIC_ROUGE",
            "PIC_BLEU",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Loi · à son rang chaque Rouge compte comme un Bleu · annule = glisse d’1 rang",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Le feu des machines se retourne contre elles"
        },
        "carte_joueur": {
          "titre_complet": "Le Boitatá, serpent de feu",
          "entite_illustree": "Le Boitatá — serpent de feu géant aux yeux immenses et lumineux, protecteur des forêts contre les incendiaires",
          "brief_illustration": "Nuit de brûlis : le Boitatá, corps de flammes bleues ondulant entre les troncs, les yeux comme deux lunes ; les braises rouges que crachent les machines se retournent contre elles et virent au bleu froid ; une matamata observe depuis l’eau. Bleus électriques, oranges, noirs.",
          "pitch_ambiance": "Pendant le grand déluge, le Boitatá survécut dans un trou et se nourrit de la lumière des yeux des bêtes mortes ; depuis, son corps brûle. Il poursuit ceux qui incendient la forêt, et leur propre feu se retourne contre eux.",
          "texte_regle": {
            "face_1": "Loi passive — Le feu retourné (tant que le Boitatá est sur la Réglette, défendu ou non) : pour toute machine qui attaque depuis le rang du Boitatá, chaque Rouge compte comme un Bleu dans le Seuil de Parade (−1 au lieu de +1), dans tous les modes. Pouvoir du Boitatá (quand il est défendu) — le serpent ondule : quand ce Rêve annule au moins 1 machine, il glisse ensuite d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent).",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Annuler les machines de son rang pour faire onduler le Boitatá vers la gauche, ou laisser attaquer une machine bourrée de Rouges devenue presque inoffensive.",
            "renoncement": "Une machine laissée active frappe toujours ; et chaque rang gagné vers la gauche emporte la loi du feu vers un autre rang."
          }
        },
        "temoins": [
          {
            "id": "R8_T1",
            "resume": "Machine en Mode Assaut au rang du Boitatá, 3 Rouges, parcelle gravée 3 : Seuil = 3 − 3 = 1 (minimum) au lieu de 6.",
            "etat_attendu_verifie": {
              "seuil_parade": 1
            },
            "statut": "A_CODER"
          },
          {
            "id": "R8_T2",
            "resume": "Boitatá défendu au rang 4 annule 1 machine ; le rang 3 est libre : il glisse au rang 3.",
            "etat_attendu_verifie": {
              "boitata_rang": 3
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Laisser active une machine à 2 Rouges ou plus sur son rang si un seul Défenseur suffit alors à la parer ; sinon annuler pour faire onduler le Boitatá vers le bloc du Sommeil.",
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
        "vecteurs": "Rangs libres de Rêve + Insectes (amorçage 1 luciole en solo) = lanternes d’annulation à distance → glissement du Rêve d’1 rang à gauche",
        "entrees_plancher": [
          "INSECTE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "INSECTE_RANG"
        ],
        "entrees": [
          "INSECTE",
          "RANG_MACHINE",
          "INSECTE_RANG"
        ],
        "sorties": [
          "LANTERNE",
          "ANNULATION",
          "POSITION_REVE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "TWIST",
          "ESSAIM",
          "LEVIER",
          "CASE_LIBRE"
        ],
        "tuile_plateau": {
          "nom_court": "La Mère des Lucioles",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_TWIST",
            "PIC_INSECTE",
            "PIC_ANNULATION",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Rang libre avec Insecte = lanterne · aucun en jeu : 1 luciole de la réserve · 1 Insecte défaussé annule 1 machine · puis glisse d’1 rang",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Les rangs vides deviennent des lanternes"
        },
        "carte_joueur": {
          "titre_complet": "La Mère des Lucioles",
          "entite_illustree": "La Mère des Lucioles, esprit-lanterne nocturne fait de milliers de points lumineux",
          "brief_illustration": "La Mère des Lucioles, esprit-lanterne de la forêt nocturne : une silhouette faite de milliers de points lumineux, penchée sur un chemin de lumière.",
          "pitch_ambiance": "Là où aucun rêve ne veille, la Mère des Lucioles allume ses lanternes. Les égarés suivent ces lumières et rentrent chez eux ; les machines, elles, s’arrêtent, aveuglées, au milieu du chemin.",
          "texte_regle": {
            "face_1": "Quand ce Rêve est défendu, à sa résolution : les lanternes s’allument.\nAmorçage — première luciole (plancher) : s’il n’y a encore aucun Insecte en jeu, posez d’abord 1 Insecte de la réserve de l’Essaim sur un rang de la Réglette libre de tout Rêve.\nChaque rang laissé libre de tout Rêve et portant au moins 1 Insecte devient une lanterne : pour chaque machine révélée et non annulée sur un tel rang, vous pouvez défausser 1 Insecte de ce rang pour l’annuler (inclinez son jeton). Ces annulations comptent comme celles de ce Rêve. Le chemin de lumière : si au moins une lanterne a annulé une machine, ce Rêve glisse ensuite d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent), au risque d’éteindre la lanterne qui s’y trouvait.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Laisser volontairement des rangs libres de tout Rêve pour y allumer des lanternes, ou compacter les Rêves vers le Sommeil.",
            "renoncement": "Chaque rang occupé par un Rêve éteint une lanterne ; chaque Insecte consumé ne déviera plus de dé."
          }
        },
        "temoins": [
          {
            "id": "R10_T1",
            "resume": "Mère des Lucioles défendue au rang 5 ; le rang 1, libre, porte 2 Insectes et reçoit 2 machines : 2 annulations par la lanterne, puis le Rêve glisse au rang 4.",
            "etat_attendu_verifie": {
              "machines_annulees_lanterne": 2,
              "reve_rang": 4
            },
            "statut": "A_CODER"
          },
          {
            "id": "R10_T2",
            "resume": "Plancher (Tour 2, aucun Nid construit, aucun Insecte en jeu) : la Mère des Lucioles, au rang 6, est défendue ; un Bulldozer est révélé au rang 2, libre de tout Rêve. Première luciole : 1 Insecte de la réserve sur le rang 2 ; la lanterne annule le Bulldozer (Insecte défaussé), puis le Rêve glisse au rang 5.",
            "etat_attendu_verifie": {
              "bulldozer_annule": true,
              "reve_rang": 5
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Garder au moins un rang libre de Rêve pour les lanternes (avec première luciole de la réserve si aucun Insecte n’est en jeu) ; ne défausser que pour des machines en Assaut ou En avançant.",
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
        "vecteurs": "Clairière sanctuarisée par l’Essaim (I) : jamais de Route ici ; Insectes envoyés sur les rangs libres de la Réglette, où la Mère des Lucioles (E) en fait des lanternes",
        "entrees_plancher": [
          "NID",
          "INSECTE",
          "SOUCHE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "NID",
          "INSECTE",
          "SOUCHE"
        ],
        "sorties": [
          "SOUCHE_SANCTUARISEE",
          "INSECTE_RANG"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "LOI",
          "CLAIRIERE",
          "ANTI_ROUTE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Jardin du Diable",
          "fenetre_badge": "PERMANENT",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_LOI_PASSIVE",
            "PIC_SOUCHE",
            "PIC_ROUTE",
            "PIC_INSECTE"
          ],
          "mots_cles_plateau": {
            "face_1": "Loi · jamais de Route ici · le Bulldozer n’y retire aucune Souche · 2 Insectes vers un rang libre",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Une clairière que nulle Route n’efface"
        },
        "carte_joueur": {
          "titre_complet": "Le Jardin du Diable",
          "entite_illustree": "Nid vivant — un « jardin du diable » (supay chacra) : clairière où ne poussent que des arbres hôtes, entretenue par de petites fourmis qui empoisonnent toute autre plante",
          "brief_illustration": "Clairière étrange au cœur de la forêt : des arbres d’une seule espèce aux tiges creuses, sol nu ; de petites fourmis en file injectent leur acide dans une pousse étrangère ; à la lisière, une silhouette aux pieds dépareillés observe ; un bulldozer s’arrête net au bord. Verts sourds, sol ocre, brume.",
          "pitch_ambiance": "Les habitants l’appellent le jardin du diable : rien n’y pousse que ce que les fourmis tolèrent, et l’on dit qu’un esprit de la forêt y cultive ses arbres. Ni les hommes ni leurs machines n’osent y arracher les souches.",
          "texte_regle": {
            "face_1": "Loi passive (tant que ce Nid est sur sa parcelle) : la parcelle du Jardin ne peut jamais devenir une Route Forestière : un Bulldozer qui y frappe sans être paré retourne 1 Arbre debout en Souche mais n’y retire aucune Souche ; une Abatteuse y frappe normalement. Les sentinelles du Jardin (à la Production, quand ce Nid est défendu, après avoir produit) : jusqu’à 2 Insectes de ce Nid peuvent migrer directement vers un rang de la Réglette laissé libre de tout Rêve.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Sur quelle parcelle bâtir le Jardin : la plus menacée de devenir Route (elle devient indestructible) ou celle d’où l’Essaim rejoint le plus vite la Réglette.",
            "renoncement": "Le Jardin protège ses Souches, pas ses Arbres : l’Abatteuse y frappe toujours ; et chaque Insecte envoyé sur la Réglette quitte la défense de la forêt."
          }
        },
        "temoins": [
          {
            "id": "M5_T1",
            "resume": "Jardin sur la parcelle 2 (1 Arbre, 0 Souche) ; un Bulldozer non paré frappe : 0 Arbre, 1 Souche ; aucune Route ; le Nid reste en place.",
            "etat_attendu_verifie": {
              "p2": {
                "arbres": 0,
                "souches": 1,
                "route": false
              },
              "nid": "EN_PLACE"
            },
            "statut": "A_CODER"
          },
          {
            "id": "M5_T2",
            "resume": "Production défendue : 2 Insectes migrent vers le rang 1, libre de tout Rêve.",
            "etat_attendu_verifie": {
              "insectes_rang_1": 2
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Bâtir le Jardin sur la parcelle à 1 ou 2 pièces la plus proche d’un Bulldozer ; envoyer les Insectes vers le rang libre le plus fréquent (rang 1 ou 2).",
        "engine_sync_status": "DESIGNED_V6_3",
        "statut_conception": "PASSE_1_CREATIF"
      }
    }
  },
  "panel_2": {
    "_meta": {
      "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
      "schema_version": "6.3.1",
      "socle_verrouille": "6.2.0",
      "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
      "etape_active": "ETAPE_2_CONCEPTION_CREATIVE",
      "statut_global": "CONCEPTION_EN_COURS",
      "genere_le": "2026-11-26",
      "slots_count": 30,
      "c02_supprime": true,
      "panel_id": "panel_2",
      "source_modele": "Modèle 2 — Candidat 2 (19 inchangés) + REPONSE_IA2 (11 révisés + filet R2)",
      "murs_porteurs_verrouilles": [
        "M1_TEMPS_BATAILLE",
        "M2_CONSERVATION_THERMIQUE",
        "M3_INTEGRITE_PLATEAU_ET_ICONES",
        "M4_AUTONOMIE_PLANCHER_SOLO"
      ],
      "note_retrocompatibilite": "Panel candidat panel_2 compilé en v6.3.1 (4 murs porteurs M1..M4, séparation entrees_plancher / entrees_synergie, 32 pictogrammes officiels) pour arbitrage d'auteur de l'Étape 2b."
    },
    "carte_des_roles": {
      "statut": "PASSE_1_CREATIF_V6_3_1",
      "roles": {
        "catalyseurs_eveil": [
          "G1=M>R",
          "G2=R>M",
          "G3=M>O",
          "G4=O>M",
          "G6=O>R",
          "G7=M>H",
          "G8=M>E",
          "G10=R>E",
          "G11=O>H",
          "G12=O>E",
          "G13=M>I",
          "G14=R>I",
          "G15=O>I"
        ],
        "leviers_reve": [
          "R1=H>E",
          "R7=E>M",
          "R8=E>R",
          "R9=E>O",
          "R10=E>I"
        ],
        "synergies_enracinement": [
          "G7=M>H",
          "G12=O>E",
          "R2=E>H",
          "M4=I>H"
        ],
        "lois_passives": [
          "R8=E>R",
          "M1=I>M"
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
          "G3=M>O",
          "G9=R>H",
          "G15=O>I",
          "R1=H>E",
          "R8=E>R",
          "M1=I>M"
        ]
      },
      "triangles_orientes": [
        [
          "I>M",
          "M>O",
          "O>I"
        ],
        [
          "H>E",
          "E>R",
          "R>H"
        ]
      ],
      "lecture_des_cartes": {
        "gouvernance": "« Vous » désigne le peuple d’origine. Chaque option est facultative et exige une cible légale, un coût disponible et la pièce annoncée. Aucun prélèvement dans le sac. Un rang libre de Rêve peut porter des dés ou des Insectes.",
        "chronologie": "Un Rêve défendu annule d’abord une machine active de son rang par Défenseur, au choix de son propriétaire, puis résout son pouvoir, même à zéro annulation, puis émet Rêve si au moins une machine a été annulée. Un Rêve ne résout son pouvoir qu’une fois par ouverture. Si le Chant et un déplacement propre se présentent au même Rêve, constater la condition du Chant au rang de l’annulation, appliquer son pas immédiat si légal, puis le pouvoir propre depuis le rang atteint. Les pions sur un Rêve suivent chacun de ses déplacements.",
        "gardiens": "Chaque Gardien peut occuper l’une des six icônes. Le badge conseille son placement. Une activation fait glisser normalement un parieur disponible en encoche. Les deux faces se lisent indépendamment. Les événements de Gardiens préparés par une carte ne sont émis qu’au moment de leur réalisation. Installer ou déplacer un Piège ne produit pas Piégeage. Une Production seule ne produit pas Insecte.",
        "cibles": "Une parcelle encore ciblée est une cible réelle de frappe restant à résoudre, y compris celle du Ratissage. Pour une machine déjà engagée, employer les cibles figées au début de son activation. Pour les suivantes, lire la situation actuelle. Le Ratissage reste immobile. Un pas radial saute les Routes. Tout mouvement laisse les autres pièces sur place sauf texte explicite.",
        "temoins": "Pour rejouer un témoin dans Python 3, affecter une copie de entree à s, exécuter transition_python, puis comparer r à attendu. Ces projections locales illustrent le choix indiqué, sans simuler une partie complète.",
        "lecture_metadonnees": "Les entrées décrivent les états de jeu mobilisés, y compris les branches optionnelles. Les sorties décrivent les effets propres. Les opérations communes de construction, de pari, de Production, d’annulation native et d’Enracinement ordinaire relèvent du socle. Les déclencheurs amorcés incluent les événements préparés pour une résolution ultérieure."
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
        "nombre": 13
      },
      "I05_couverture_sommeil": {
        "verdict": "OK",
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
        "nombre": 2,
        "max_par_assise": 2
      },
      "Q02_twists_2K3": {
        "verdict": "OK",
        "nombre": 6
      },
      "synergies_optionnelles_couvertes": 32
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
        "vecteurs": "DUEL + CROC + ROUGE + RANG_MACHINE + RATISSAGE → BLEU",
        "entrees_plancher": [
          "DUEL",
          "ROUGE",
          "RANG_MACHINE",
          "RATISSAGE"
        ],
        "entrees_synergie": [
          "CROC"
        ],
        "entrees": [
          "DUEL",
          "ROUGE",
          "RANG_MACHINE",
          "RATISSAGE",
          "CROC"
        ],
        "sorties": [
          "BLEU"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Deux passages peuvent épuiser deux Rouges du même assaillant ou préparer séparément les deux machines du gué.",
        "tags": [
          "GUET",
          "SURCHAUFFE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Jaguar",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PIEGEAGE",
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_CROC",
            "PIC_ROUGE",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "Gué marqué",
            "face_2": "Chaleur à revers",
            "enracine": null
          },
          "resume_plateau": "Gué marqué / Chaleur à revers"
        },
        "carte_joueur": {
          "titre_complet": "Le Jaguar",
          "entite_illustree": "Jaguar au gué",
          "brief_illustration": "Jaguar entier à mi-corps dans l’eau, ses pattes visibles à travers le gué. Deux sillages convergent entre des berges d’argile.",
          "pitch_ambiance": "Au gué, le jaguar laisse passer la première silhouette. La seconde trouve l’eau déjà troublée.",
          "texte_regle": {
            "face_1": "À chaque activation, choisissez une machine qui cible encore la parcelle du Duel ou du Croc. Vous pouvez retourner sur elle un Rouge en Bleu.",
            "face_2": "À chaque activation, choisissez une machine qui cible encore la parcelle du Duel ou du Croc. Vous pouvez retourner un de ses Rouges en Bleu et le laisser sur elle, ou le déposer face Bleue sur l’autre machine de son rayon.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Où laisser la Surchauffe du gué ?",
            "renoncement": "La transmettre au Bulldozer laisse l’Abatteuse plus difficile à parer."
          }
        },
        "temoins": [
          {
            "id": "G1_T1",
            "resume": "Le Croc garde le gué. En Face 2, le Jaguar prend un Rouge à l’Abatteuse qui le vise et le donne en Bleu au Bulldozer. En Charge, son seuil gravé de 2 tombe à 1.",
            "etat_attendu_verifie": {
              "entree": {
                "rouges_A": 1,
                "bleus_B": 0,
                "grave": 2,
                "croc_cible_A": true
              },
              "transition_python": "if s['croc_cible_A'] and s['rouges_A']:\n    s['rouges_A']-=1\n    s['bleus_B']+=1\nr=[s['rouges_A'],s['bleus_B'],max(1,s['grave']-s['bleus_B'])]",
              "attendu": [
                0,
                1,
                1
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G1_T2",
            "resume": "Deux activations F1 avant deux frappes au gué retournent chacune un Rouge. Un seuil d’Assaut gravé 3 avec deux Rouges passe de 5 à 1.",
            "etat_attendu_verifie": {
              "entree": {
                "rouges": 2,
                "bleus": 0,
                "grave": 3,
                "activations": 2
              },
              "transition_python": "seuils=[]\nfor _ in range(s['activations']):\n    if s['rouges']>0:\n        s['rouges']-=1\n        s['bleus']+=1\n    seuils.append(max(1,s['grave']+s['rouges']-s['bleus']))\nr=seuils",
              "attendu": [
                3,
                1
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Transmettre si le premier assaut est déjà couvert par le Croc et si le Bleu permet une Parade sur la seconde machine.",
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
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": false,
        "vecteurs": "RANG_MACHINE + CROC (+ DUEL Face 2) → RECUL / CROC",
        "entrees_plancher": [
          "CROC",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "DUEL"
        ],
        "entrees": [
          "CROC",
          "RANG_MACHINE",
          "DUEL"
        ],
        "sorties": [
          "RECUL",
          "CROC"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Deux replis peuvent ramener deux mobiles d’un pas chacun. En Face 2, le premier passage peut laisser le Croc au gué libéré et le second y attirer une mobile du voisinage.",
        "tags": [
          "RECUL",
          "CROC",
          "GUE"
        ],
        "tuile_plateau": {
          "nom_court": "L’Anaconda vert",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_RECUL",
            "PIC_CROC",
            "PIC_DUEL"
          ],
          "mots_cles_plateau": {
            "face_1": "Repli au gué",
            "face_2": "Rabattre sur la marque",
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Mobile ← un pas · Croc sur la trace / traction vers Croc ou Duel"
        },
        "carte_joueur": {
          "titre_complet": "L’Anaconda vert",
          "entite_illustree": "L’Anaconda vert entier dessinant un double coude entre une souche immergée et une plage de vase",
          "brief_illustration": "L’anaconda entier dessine un double coude entre une souche immergée et une plage de vase. On voit où sa queue ferme le passage.",
          "pitch_ambiance": "L’eau se retire autour des anneaux. Il ne reste qu’un gué.",
          "texte_regle": {
            "face_1": "Repli au gué. Choisissez une mobile de R ou M qui n’est pas en cours d’activation et dispose d’un pas vers la bordure. Faites-la reculer de ce pas, sans frappe. Vous pouvez prendre le Croc en réserve ou en forêt et le poser sur la parcelle qu’elle quitte. Vous pouvez aussi vous limiter à poster le Croc sur une parcelle de R ou M de votre choix (ou sur une parcelle survivante d’un autre rayon si R et M sont entièrement Route), même avant qu’une machine la cible.",
            "face_2": "Rabattre sur la marque. Vous disposez du Repli au gué. Vous pouvez à la place choisir une mobile non engagée à un pas radial du Croc ou du Duel. Tirez-la sur la marque, même vers le cœur. Si vous le souhaitez, placez ensuite le Croc sur la parcelle libérée. Le Duel garde sa place et sa face. Ces deux manœuvres laissent les machines en Ratissage à leur poste.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Laisser le Croc sous la machine pour couvrir Sur place, ou le refermer derrière elle pour couvrir Devant et offrir au Jaguar une autre cible marquée.",
            "renoncement": "Repositionner le Croc libère la parcelle qu’il gardait ; en Face 2, attirer une mobile vers le cœur rapproche son front si elle n’est pas neutralisée dans le tour."
          }
        },
        "temoins": [
          {
            "id": "G2_T1",
            "resume": "Le Duel est en M·2. À l’ouverture, l’Abatteuse de M occupe M·3, porte un Rouge et doit frapper Sur place au rang 4. G2 la ramène en M·2 et laisse le Croc en M·3. Un Piège arrête une frappe de rang 1 et active G1 sur Piégeage : la cible encore à jouer est le Duel en M·2, G1 retourne le Rouge de l’Abatteuse sur place (seuil de rang 4 abaissé de 3 à 1 en Acte 1), le Croc reste en M·3.",
            "etat_attendu_verifie": {
              "abatteuse_parcelle": 2,
              "croc_parcelle": 3
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Reculer une mobile menaçant le cœur et fermer la parcelle quittée avec le Croc ; en Face 2, rabattre une mobile à Rouge sur le Duel ou le Croc pour ouvrir la conversion de G1.",
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
          "CATALYSEUR_EVEIL",
          "TWIST_2K3"
        ],
        "est_twist": true,
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
        "vecteurs": "PLUME + GARDIEN → PARI_REORIENTE / DEFENSEUR_EVACUE",
        "entrees_plancher": [
          "PLUME",
          "GARDIEN"
        ],
        "entrees_synergie": [],
        "entrees": [
          "PLUME",
          "GARDIEN"
        ],
        "sorties": [
          "PARI_REORIENTE",
          "DEFENSEUR_EVACUE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": "Deux cris transfèrent deux parieurs séparément, dans la limite des places réellement libres.",
        "tags": [
          "ALARME",
          "PARI"
        ],
        "tuile_plateau": {
          "nom_court": "L’Ara rouge",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_RESONANCE",
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_PARI_ENCOCHE",
            "PIC_DEFENSEUR"
          ],
          "mots_cles_plateau": {
            "face_1": "Cri · transfert de mise",
            "face_2": "Cri · évacuation",
            "enracine": null
          },
          "resume_plateau": "Cri · transfert de mise / Cri · évacuation"
        },
        "carte_joueur": {
          "titre_complet": "L’Ara rouge",
          "entite_illustree": "Ara au-dessus d’une falaise d’argile",
          "brief_illustration": "Ara rouge entier au premier plan, en plein virage, avec ses congénères en vol devant la falaise d’argile.",
          "pitch_ambiance": "Une bande d’aras décolle du talus. Ceux qui ne voient pas le danger entendent les premiers oiseaux.",
          "texte_regle": {
            "face_1": "À chaque activation, si la Plume indique un rayon, vous pouvez déplacer un Défenseur encore posé sur un Gardien vers un autre Gardien construit. Comptez sur le Gardien d’arrivée les pions dessus et dans ses encoches. Leur total après transfert ne peut dépasser deux. Le pion arrive dessus.",
            "face_2": "À chaque activation, où que soit posée la Plume, vous pouvez transférer un Défenseur encore posé sur un Gardien vers le dessus d’un autre Gardien construit, dans la limite de deux pions dessus et en encoches réunis. Vous pouvez aussi évacuer ce Défenseur sur une parcelle encore ciblée. Un pion en encoche reste en place.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Rallier un pari encore gagnable ou évacuer le parieur ?",
            "renoncement": "Évacuer en forêt sacrifie sa contribution à l’Éveil."
          }
        },
        "temoins": [
          {
            "id": "G4_T1",
            "resume": "Plume sur M. Deux parieurs attendent sur Rêve après le dernier Rêve. L’Ara en transfère un sur Piégeage avant que le Croc pare. Cette activation peut alors faire glisser le parieur normalement.",
            "etat_attendu_verifie": {
              "entree": {
                "source": 2,
                "dessus": 0,
                "encoches": 0,
                "croc_pare": true
              },
              "transition_python": "if s['source'] and s['dessus']+s['encoches']<2:\n    s['source']-=1\n    s['dessus']+=1\nif s['croc_pare'] and s['dessus']:\n    s['dessus']-=1\n    s['encoches']+=1\nr=[s['source'],s['dessus'],s['encoches']]",
              "attendu": [
                1,
                0,
                1
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G4_T2",
            "resume": "Deux alarmes transfèrent les deux parieurs d’un Gardien dont la fenêtre est passée vers deux Gardiens distincts, chacun disposant d’une place.",
            "etat_attendu_verifie": {
              "entree": {
                "source": 2,
                "paris": [
                  [
                    0,
                    1
                  ],
                  [
                    1,
                    0
                  ]
                ]
              },
              "transition_python": "for pari in s['paris']:\n    if s['source'] and sum(pari)<2:\n        s['source']-=1\n        pari[0]+=1\nr=[s['source'],s['paris']]",
              "attendu": [
                0,
                [
                  [
                    1,
                    1
                  ],
                  [
                    2,
                    0
                  ]
                ]
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Transférer vers un événement visible encore à venir, sans retirer la dernière mise utile d’un Gardien qui pourrait passer Face 2.",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "PLUME + ROUGE → BLEU / ECAILLE",
        "entrees_plancher": [
          "PLUME",
          "ROUGE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "PLUME",
          "ROUGE"
        ],
        "sorties": [
          "BLEU",
          "ECAILLE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE",
          "ICONE_PARADE"
        ],
        "double_ouverture": "Deux transferts peuvent faire basculer un seuil élevé. En Face 2, mue et transfert restent deux choix indépendants.",
        "tags": [
          "THERMOREGULATION"
        ],
        "tuile_plateau": {
          "nom_court": "L’Iguane vert",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_ROUGE",
            "PIC_BLEU",
            "PIC_ECAILLE"
          ],
          "mots_cles_plateau": {
            "face_1": "Chaud · Calme",
            "face_2": "Deux versants",
            "enracine": null
          },
          "resume_plateau": "Chaud · Calme / Deux versants"
        },
        "carte_joueur": {
          "titre_complet": "L’Iguane vert",
          "entite_illustree": "Iguane sur une branche au soleil",
          "brief_illustration": "Iguane entier traversant la limite nette entre soleil et ombre sur une branche au-dessus de l’eau.",
          "pitch_ambiance": "Entre soleil et feuillage, l’iguane change de branche et le fleuve change de couleur sous lui.",
          "texte_regle": {
            "face_1": "À chaque activation, si la Plume montre Chaud, choisissez un rayon et prenez un Rouge sur une de ses machines. Posez-le face Bleue sur l’autre machine du même rayon. Si elle montre Calme, vous pouvez glisser une Écaille de la réserve dans le sac.",
            "face_2": "À chaque activation, choisissez entre glisser une Écaille de la réserve dans le sac et transférer un Rouge d’une machine, face Bleue, sur l’autre de son rayon. Si la Plume indique ce rayon, le Bleu peut aussi rester sur la machine d’origine.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Quelle machine doit profiter de l’ombre ?",
            "renoncement": "En transférant le jeton, on laisse la donneuse sans la réduction bleue."
          }
        },
        "temoins": [
          {
            "id": "G5_T1",
            "resume": "Plume Chaud. Un Rouge quitte l’Abatteuse pour devenir le premier Bleu du Bulldozer. Le Toucan peut désormais installer un Piège sur une cible de ce dernier.",
            "etat_attendu_verifie": {
              "entree": {
                "plume": "Chaud",
                "rouges_A": 2,
                "bleus_B": 0,
                "cible_B": "R4"
              },
              "transition_python": "if s['plume']=='Chaud' and s['rouges_A']>0:\n    s['rouges_A']-=1\n    s['bleus_B']+=1\nr=[s['rouges_A'],s['bleus_B'],s['cible_B'] if s['bleus_B'] else None]",
              "attendu": [
                1,
                1,
                "R4"
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G5_T2",
            "resume": "Plume Chaud. Deux Rouge sur la première machine deviennent deux Bleus sur sa jumelle. Un seul Défenseur tient alors son seuil gravé de 3 en Charge.",
            "etat_attendu_verifie": {
              "entree": {
                "rouges": 2,
                "bleus": 0,
                "grave": 3,
                "plume": "Chaud"
              },
              "transition_python": "for _ in range(2):\n    if s['plume']=='Chaud' and s['rouges']:\n        s['rouges']-=1\n        s['bleus']+=1\nr=[s['rouges'],s['bleus'],max(1,s['grave']-s['bleus'])]",
              "attendu": [
                0,
                2,
                1
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Éviter de retirer un Rouge ignoré en Charge si le Bleu obtenu ne change aucune Parade et si une Écaille reste disponible en Face 2.",
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
        "roles_portes": [
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": false,
        "vecteurs": "RANG_MACHINE + SABOTAGE (+ BLEU Face 2) → RANG_MACHINE / SABOTAGE",
        "entrees_plancher": [
          "RANG_MACHINE",
          "SABOTAGE"
        ],
        "entrees_synergie": [
          "BLEU"
        ],
        "entrees": [
          "RANG_MACHINE",
          "SABOTAGE",
          "BLEU"
        ],
        "sorties": [
          "RANG_MACHINE",
          "SABOTAGE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Le premier cri peut envoyer une mobile sur une case piégée. Si cette frappe déclenche le deuxième passage, le Toucan peut encore décaler une attaque ultérieure ou alimenter le sac.",
        "tags": [
          "RANG",
          "SABOTAGE",
          "ECHO_THERMIQUE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Toucan toco",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PIEGEAGE",
          "pictogrammes": [
            "PIC_RANG_MACHINE",
            "PIC_SABOTAGE",
            "PIC_BLEU",
            "PIC_PLUME"
          ],
          "mots_cles_plateau": {
            "face_1": "Appel bref",
            "face_2": "Écho thermique",
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Sur place ↔ Devant / Bleu · échange des dés du rayon"
        },
        "carte_joueur": {
          "titre_complet": "Le Toucan toco",
          "entite_illustree": "Le Toucan toco entier perché sur une fourche de cécropia, le bec tourné vers un second tronc",
          "brief_illustration": "Toucan entier sur une fourche de cécropia, le bec tourné vers un second tronc qui émerge du brouillard.",
          "pitch_ambiance": "Un cri désigne l’arbre. Son écho désigne celui d’à côté.",
          "texte_regle": {
            "face_1": "Appel bref. Choisissez une mobile à jouer. Déplacez son dé entre les rangs 1 et 2, ou entre 4 et 5, dans un sens ou dans l’autre (en cours d’attaques, vers un rang strictement ultérieur au rang en cours). Elle garde son mode et change de cible entre Sur place et Devant. Vous pouvez choisir la fausse alerte à la place et glisser un Sabotage ordinaire de la réserve dans le sac. Il y attend une prochaine pioche.",
            "face_2": "Écho thermique. Vous gardez les deux appels de la Face 1. Une troisième possibilité s’ouvre si les deux mobiles d’un même rayon sont à jouer à des rangs différents et que l’une porte un Bleu. Échangez leurs rangs. Chacune lit toute la tactique et le mode de son nouveau rang. Le Bleu reste sur sa machine. Les jetons Machine restent devant leur rayon.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Décaler une attaque pour la livrer à un Piège ou à des Défenseurs dès ce tour, ou choisir la fausse alerte pour améliorer les pioches futures ; en Face 2, échanger deux rangs via un Bleu.",
            "renoncement": "La fausse alerte ne soulage pas le tour en cours ; l’échange de Face 2 engage à la fois les tactiques et les modes des deux attaques du rayon."
          }
        },
        "temoins": [
          {
            "id": "G6_T1",
            "resume": "En Acte 1, l’Abatteuse R·2 (rang 4, 1 Rouge) et le Bulldozer R·1 (rang 2, nu). G5 (Plume Chaud) dépose le Rouge de l’Abatteuse face Bleue sur le Bulldozer. Un Piège active G6 Face 2 : les dés 2 et 4 s’échangent. L’Abatteuse frappe R·3 en Charge au rang 2 et le Bulldozer frappe R·1 en Assaut au rang 4 au seuil de 1 grâce au Bleu.",
            "etat_attendu_verifie": {
              "abatteuse_rang": 2,
              "bulldozer_rang": 4,
              "seuil_bulldozer": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Décaler 1↔2 ou 4↔5 une mobile pour diriger sa frappe sur un Piège ou des Défenseurs ; sans cible favorable, injecter un Sabotage au sac ; en Face 2, exploiter un Bleu de G5 pour inverser Charge et Assaut sur le rayon.",
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
          "CATALYSEUR_EVEIL",
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "DUEL + DEFENSEUR_ATTENTE + TAMBOUR + CHANT → DEFENSEUR_REDEPLOYE / DUEL / ARBRE",
        "entrees_plancher": [
          "DUEL",
          "DEFENSEUR_ATTENTE",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "SOUCHE"
        ],
        "entrees": [
          "DUEL",
          "DEFENSEUR_ATTENTE",
          "TAMBOUR",
          "CHANT",
          "SOUCHE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "DUEL",
          "ARBRE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Une première percée rassemble deux pions. En Face 2, le second passage peut échanger le Chamane arrivé avec un Mammifère déjà sur un Rêve. Le Duel reste couvert.",
        "tags": [
          "SENTE",
          "DUEL",
          "CHAMANE",
          "ENRACINEMENT"
        ],
        "tuile_plateau": {
          "nom_court": "Le Tapir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_TAMBOUR",
            "PIC_CHANT",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "Ouvrir la sente",
            "face_2": "Croisée du Chant",
            "enracine": "Souche en amont · Final"
          },
          "resume_plateau": "Guide + Duel · pas du Chamane / permutation / repousse en amont"
        },
        "carte_joueur": {
          "titre_complet": "Le Tapir",
          "entite_illustree": "Le Tapir entier écartant les tiges d’un marais avec le poitrail",
          "brief_illustration": "Un tapir entier écarte les tiges d’un marais avec le poitrail. Derrière sa croupe, un sentier assez large pour deux pieds nus se remplit lentement d’eau.",
          "pitch_ambiance": "Le premier passage coûte au tapir. Le second appartient à qui le suit.",
          "texte_regle": {
            "face_1": "Ouvrir la sente. Prenez un de vos Défenseurs hors Gardien et hors encoche, y compris sur une rive, un Rêve, une lisière ou en attente. Placez-le debout sur une parcelle de M ou H (ou sur une parcelle survivante d’un autre rayon si M et H sont entièrement Route) avec le Duel, repris en réserve ou en forêt et tourné sur Défi. Si le Tambour ou le Chant se trouve à un pas radial de l’arrivée, vous pouvez l’y conduire. Le Chamane et le guide compteront tous deux à la Parade. Vous pouvez choisir une parcelle où le Chamane se trouve déjà.",
            "face_2": "Croisée du Chant. Vous pouvez ouvrir la sente. Vous pouvez aussi permuter un Défenseur Mammifère et un Chamane, si l’un se trouve sur le Duel et l’autre sur une autre parcelle ou sur un Rêve. Échangez physiquement leurs postes. Le Duel garde sa face et sa parcelle. Le Chant arrivé sur un Rêve encore à lire y exercera son pouvoir à l’ouverture. Un Rêve déjà lu poursuit son tour.",
            "enracine": "Au décompte final. Si la parcelle désignée a survécu, appliquez-y la repousse ordinaire. Puis vous pouvez retourner une Souche sur la prochaine parcelle non-Route de ce rayon, côté cœur, même si la première parcelle n’avait plus de Souche. À défaut de parcelle ou de Souche en amont, le bonus vaut zéro."
          },
          "decision_et_renoncement": {
            "choix": "Réunir le Tambour et le Duel pour donner à R3 les deux directions de pose de son Piège, ou permuter le Chant sur la Réglette en Face 2.",
            "renoncement": "Envoyer le Chant sur la Réglette peut ouvrir le Sommeil, au prix d’un défenseur de front ; reprendre le Duel le remet sur sa face Défi."
          }
        },
        "temoins": [
          {
            "id": "G7_T1",
            "resume": "Avant la lecture de R3, G7 ouvre la sente en M·2 avec un Mammifère et y amène le Tambour depuis M·1 : R3 défendu peut poser son Piège en M·1 ou M·3. Enraciné Face 2 devant M·2 (2 Souches en M·2, 1 en M·3), les trois Souches survivantes se retournent au décompte final (deux au pied de la tuile et une en amont).",
            "etat_attendu_verifie": {
              "duel_et_tambour_m2": true,
              "souches_finales": 3
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Réunir un Défenseur Mammifère, le Duel et le Tambour avant la résolution de R3 ou une Parade critique ; en Face 2, permuter le Chant vers un Rêve encore à lire ; enraciner Face 2 devant une parcelle avec Souches en amont.",
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
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": false,
        "vecteurs": "DEFENSEUR_ATTENTE + RANG_MACHINE + POSITION_REVE + ALTERATION → DEFENSEUR_REDEPLOYE",
        "entrees_plancher": [
          "DEFENSEUR_ATTENTE",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "entrees_synergie": [
          "ALTERATION"
        ],
        "entrees": [
          "DEFENSEUR_ATTENTE",
          "RANG_MACHINE",
          "POSITION_REVE",
          "ALTERATION"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE",
          "ICONE_PARADE"
        ],
        "double_ouverture": "Deux appels peuvent garnir deux Rêves ou placer deux Défenseurs sur le même front forestier.",
        "tags": [
          "ECHO"
        ],
        "tuile_plateau": {
          "nom_court": "Le Boto",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_ALTERATION",
            "PIC_REVE",
            "PIC_DEFENSEUR_ATTENTE",
            "PIC_DEFENSEUR"
          ],
          "mots_cles_plateau": {
            "face_1": "Écho · veilleur",
            "face_2": "Écho · plongeur",
            "enracine": null
          },
          "resume_plateau": "Écho · veilleur / Écho · plongeur"
        },
        "carte_joueur": {
          "titre_complet": "Le Boto",
          "entite_illustree": "Boto entre les troncs noyés",
          "brief_illustration": "Boto entier en virage sous la surface d’une forêt inondée, avec une seconde silhouette lointaine entre les troncs.",
          "pitch_ambiance": "Dans l’eau trouble, le boto tourne autour d’un tronc. Un second remous lui répond au-delà des branches.",
          "texte_regle": {
            "face_1": "À chaque activation, vous pouvez relever un bâtisseur en attente sur une parcelle encore ciblée de M ou E. Avant la résolution du premier Rêve, vous pouvez plutôt le poser sur un Rêve au rang d’une machine mobile visible et active.",
            "face_2": "À chaque activation, vous pouvez prendre un bâtisseur en attente ou un Défenseur en forêt et le poser sur une autre parcelle encore ciblée. Avant le premier Rêve, vous pouvez plutôt le poser sur un Rêve au rang d’une machine mobile visible et active, ou sur tout Rêve si une machine en forêt porte une Altération.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Faire entendre l’écho en forêt ou sur un Rêve ?",
            "renoncement": "Un veilleur envoyé sur la Réglette ne compte plus au seuil de Parade en forêt."
          }
        },
        "temoins": [
          {
            "id": "G8_T1",
            "resume": "Un Sabotage active le Boto avant les Rêves. Il relève un bâtisseur sur le Rêve du rang 4. Celui-ci annule la machine de rang 4 et allume Rêve.",
            "etat_attendu_verifie": {
              "entree": {
                "attente": 1,
                "rang_reve": 4,
                "actives": [
                  4
                ],
                "defenseurs": 0,
                "avant_reves": true
              },
              "transition_python": "if s['avant_reves'] and s['attente'] and s['rang_reve'] in s['actives']:\n    s['attente']-=1\n    s['defenseurs']+=1\nn=min(s['defenseurs'],s['actives'].count(s['rang_reve']))\nr=[s['attente'],s['defenseurs'],n,'Rêve' if n else None]",
              "attendu": [
                0,
                1,
                1,
                "Rêve"
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G8_T2",
            "resume": "Deux Sabotages successifs donnent deux activations avant les Rêves. Deux bâtisseurs rejoignent le même Rêve en 4 et permettent deux annulations pour un seul événement Rêve.",
            "etat_attendu_verifie": {
              "entree": {
                "attente": 2,
                "pions": 0,
                "machines_au_rang": 2,
                "sabotages": 2
              },
              "transition_python": "for _ in range(s['sabotages']):\n    if s['machines_au_rang'] and s['attente']:\n        s['pions']+=1\n        s['attente']-=1\nannulations=min(s['machines_au_rang'],s['pions'])\nr=[s['attente'],annulations,int(annulations>0)]",
              "attendu": [
                0,
                2,
                1
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Préférer la Réglette si une annulation y évite deux frappes. Après les Rêves, combler un seuil en forêt.",
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
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "CROC + FURTIVITE + RANG_MACHINE (+ CHANT) → CROC / PIEGE",
        "entrees_plancher": [
          "CROC",
          "FURTIVITE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "CHANT"
        ],
        "entrees": [
          "CROC",
          "FURTIVITE",
          "RANG_MACHINE",
          "CHANT"
        ],
        "sorties": [
          "CROC",
          "PIEGE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Un passage arme l’affût. Le second peut inverser sa pointe avant le verdict, le rompre pour une frappe urgente, ou reposter en forêt le Croc libéré après la Furtivité.",
        "tags": [
          "CONFLUENT",
          "CROC",
          "FURTIVITE",
          "TWIST"
        ],
        "tuile_plateau": {
          "nom_court": "Le Caïman noir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_CROC",
            "PIC_DEFENSEUR",
            "PIC_PIEGE",
            "PIC_TWIST"
          ],
          "mots_cles_plateau": {
            "face_1": "Confluent 1 + 1",
            "face_2": "Guetteurs séparés",
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Croc entre R et H → rive bénéficiaire · deux guetteurs groupés / répartis"
        },
        "carte_joueur": {
          "titre_complet": "Le Caïman noir",
          "entite_illustree": "Le Caïman noir entier flottant dans un bras où deux eaux se rejoignent",
          "brief_illustration": "Le caïman entier flotte dans un bras où deux eaux se rejoignent. Sa queue touche encore une berge, son museau pointe vers l’autre.",
          "pitch_ambiance": "Chacun des deux guetteurs n’a vu qu’un sillage. Le caïman les a vus tous les deux.",
          "texte_regle": {
            "face_1": "Confluent. Prenez l’unique Croc en réserve, en forêt ou à l’affût. Soit vous le postez sur une parcelle de R ou H (ou d’un autre rayon si R et H sont entièrement Route), soit vous le couchez entre les deux pieds de rayon R et H, si leurs rives sont ouvertes. Sa pointe désigne le rayon qui pourra gagner. Cette position arme un seul affût pour la prochaine Furtivité. À cette fenêtre, calculez normalement les deux mobilisations. Si m(R) = 1 et m(H) = 1 et que la Rive Piège pointée porte deux Défenseurs, elle gagne un Piège. Le propriétaire du rayon pointé en choisit la parcelle légale. Les autres paris suivent leur règle ordinaire.\nDénouement de l’affût : après cette Furtivité, rendez le Croc en réserve, succès ou échec. Un affût armé après la Furtivité attend celle du tour suivant. Un nouvel emploi du Croc remplace l’ancien. Si G9 quitte la piste, rendez immédiatement un Croc encore à l’affût. La face visible de G9 à la Furtivité fait foi. Jetons inclinés et Ratissages comptent dans leur propre rayon comme d’habitude.",
            "face_2": "Guetteurs séparés. Même choix entre Croc en forêt et affût. Au confluent 1 + 1, vous pouvez aussi former l’équipage avec un Défenseur de chacune des deux Rives Piège. Attribuez un seul Piège au rayon pointé. Un Chamane compte comme le pion de la rive où il se tient.\nDénouement de l’affût : après cette Furtivité, rendez le Croc en réserve, succès ou échec. Un affût armé après la Furtivité attend celle du tour suivant. Un nouvel emploi du Croc remplace l’ancien. Si G9 quitte la piste, rendez immédiatement un Croc encore à l’affût. La face visible de G9 à la Furtivité fait foi. Jetons inclinés et Ratissages comptent dans leur propre rayon comme d’habitude.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Poster le Croc en forêt pour garantir un coup d’arrêt sur une parcelle, ou le risquer au confluent entre R et H pour transformer deux demi-mobilisations en Piège placé au choix du propriétaire du rayon.",
            "renoncement": "Le Croc couché à l’affût ne pare aucune frappe tant que la Furtivité n’est pas passée, et rentre en réserve même si l’affût échoue."
          }
        },
        "temoins": [
          {
            "id": "G9_T1",
            "resume": "G9 Face 2 pointe vers H. Le jeton de l’Abatteuse H est incliné après annulation ; sur R, seul le Bulldozer en Ratissage est mobilisé. Chaque Rive Piège porte 1 pion (dont le Chant sur H). Les compteurs valent 1 et 1 : les deux guetteurs répartis font gagner 1 Piège à H (posé en H·3) et le Croc revient en réserve.",
            "etat_attendu_verifie": {
              "piege_gagne_h": true,
              "croc_en_reserve": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Si m(R)=1 et m(H)=1 s’annoncent avant la Furtivité avec les guetteurs prêts, coucher le Croc au confluent vers le rayon le plus exposé ; sinon poster directement le Croc sur une parcelle menacée de R ou H.",
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
        "vecteurs": "SOUCHE + PIEGE + RANG_MACHINE + RATISSAGE → CROC / PIEGE",
        "entrees_plancher": [
          "SOUCHE",
          "RANG_MACHINE",
          "RATISSAGE"
        ],
        "entrees_synergie": [
          "PIEGE"
        ],
        "entrees": [
          "SOUCHE",
          "RANG_MACHINE",
          "RATISSAGE",
          "PIEGE"
        ],
        "sorties": [
          "CROC",
          "PIEGE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Une aspiration attire le Piège, la suivante peut le remplacer par le Croc et couvrir une autre cible. Deux rayons peuvent aussi fournir deux Pièges.",
        "tags": [
          "MIMETISME"
        ],
        "tuile_plateau": {
          "nom_court": "La Matamata",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_REVE",
          "pictogrammes": [
            "PIC_SOUCHE",
            "PIC_CROC",
            "PIC_PIEGE"
          ],
          "mots_cles_plateau": {
            "face_1": "Litière · aspiration",
            "face_2": "Leurre dédoublé",
            "enracine": null
          },
          "resume_plateau": "Litière · aspiration / Leurre dédoublé"
        },
        "carte_joueur": {
          "titre_complet": "La Matamata",
          "entite_illustree": "Matamata sur un lit de feuilles",
          "brief_illustration": "Matamata entière posée parmi les feuilles mortes d’un bras calme, sa carapace discernable au second regard.",
          "pitch_ambiance": "Feuille entre les feuilles, la matamata attend que l’eau lui amène sa prise.",
          "texte_regle": {
            "face_1": "À chaque activation, choisissez une parcelle encore ciblée portant une Souche. Vous pouvez y poser le Croc de la réserve ou y attirer un Piège ordinaire d’une autre parcelle du même rayon, si la destination est libre de Piège ordinaire.",
            "face_2": "À chaque activation, choisissez une parcelle encore ciblée. Vous pouvez y attirer un Piège ordinaire d’une autre parcelle de son rayon si elle peut le recevoir. Vous pouvez plutôt y poser le Croc de la réserve et, si vous y recouvrez un Piège ordinaire, envoyer ce Piège sur une autre parcelle encore ciblée de ce rayon, libre de Piège ordinaire.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Garder deux intercepteurs ensemble ou faire glisser le leurre ?",
            "renoncement": "Une parcelle dégarnie de son Piège n’arrêtera plus une deuxième frappe après le Croc."
          }
        },
        "temoins": [
          {
            "id": "G10_T1",
            "resume": "Deux machines d’un rayon visent des parcelles différentes. La Matamata F2 couvre la première avec le Croc et en extrait le Piège pour la seconde. Deux frappes, deux événements Piégeage.",
            "etat_attendu_verifie": {
              "entree": {
                "croc_reserve": 1,
                "pieges": [
                  "R2"
                ],
                "cibles": [
                  "R2",
                  "R3"
                ]
              },
              "transition_python": "a,b=s['cibles']\ncroc=None\nif s['croc_reserve']:\n    croc=a\n    if a in s['pieges'] and b not in s['pieges']:\n        s['pieges'].remove(a)\n        s['pieges'].append(b)\nr=[croc,s['pieges'],sum(p==croc or p in s['pieges'] for p in s['cibles'])]",
              "attendu": [
                "R2",
                [
                  "R3"
                ],
                2
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G10_T2",
            "resume": "F2 attire d’abord le Piège de R1 sur R2, puis y pose le Croc et expédie le Piège en R3. Les deux cibles restent couvertes.",
            "etat_attendu_verifie": {
              "entree": {
                "piege": "R1",
                "cibles": [
                  "R2",
                  "R3"
                ],
                "croc": null
              },
              "transition_python": "a,b=s['cibles']\nif s['piege'][0]==a[0] and s['piege']!=a:\n    s['piege']=a\nif s['croc'] is None:\n    s['croc']=a\n    if s['piege']==a and b!=a and b[0]==a[0]:\n        s['piege']=b\nr=[s['croc'],s['piege']]",
              "attendu": [
                "R2",
                "R3"
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Répartir les intercepteurs lorsque deux parcelles différentes seraient perdues, les superposer contre deux frappes destructrices au même endroit.",
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
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "PLUME + RANG_MACHINE + RATISSAGE + SOUCHE + PIEGE → PIEGE / DEFENSEUR_REDEPLOYE",
        "entrees_plancher": [
          "PLUME",
          "RANG_MACHINE",
          "RATISSAGE"
        ],
        "entrees_synergie": [
          "SOUCHE",
          "PIEGE"
        ],
        "entrees": [
          "PLUME",
          "RANG_MACHINE",
          "RATISSAGE",
          "SOUCHE",
          "PIEGE"
        ],
        "sorties": [
          "PIEGE",
          "DEFENSEUR_REDEPLOYE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE",
          "ICONE_PARADE"
        ],
        "double_ouverture": "Deux affûts couvrent deux parcelles désertes. Une première pose peut aussi être renouvelée après le passage d’une machine.",
        "tags": [
          "CAMOUFLAGE"
        ],
        "tuile_plateau": {
          "nom_court": "L’Ibijau",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_PIEGE",
            "PIC_SOUCHE",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "Poste désert",
            "face_2": "Relais de camouflage",
            "enracine": "Dernier affût"
          },
          "resume_plateau": "Poste désert / Relais de camouflage / Dernier affût"
        },
        "carte_joueur": {
          "titre_complet": "L’Ibijau",
          "entite_illustree": "Ibijau sur un chicot",
          "brief_illustration": "Ibijau entier, vertical sur un chicot dans une clairière grise. Sa silhouette se détache à peine de l’écorce.",
          "pitch_ambiance": "Là où l’œil croit compter deux branches, l’ibijau attend que le jour finisse.",
          "texte_regle": {
            "face_1": "À chaque activation, vous pouvez poser un Piège ordinaire de la réserve sur une parcelle encore ciblée, sans Défenseur ni Piège ordinaire, du rayon portant la Plume.",
            "face_2": "À chaque activation, vous pouvez poser un Piège ordinaire de la réserve sur une parcelle encore ciblée, sans Défenseur ni Piège ordinaire. Si elle ne porte que des Souches, vous pouvez aussi déplacer un Défenseur en forêt d’une autre parcelle de son rayon vers la parcelle voisine de la cible, côté cœur, en sautant les Routes.",
            "enracine": "Quand vous enracinez l’Ibijau, vous pouvez transférer un Piège ordinaire de n’importe quelle parcelle vers la parcelle désignée si elle est libre de Piège ordinaire."
          },
          "decision_et_renoncement": {
            "choix": "Couvrir une case vide ou y envoyer un Défenseur ?",
            "renoncement": "Un seul Défenseur déjà sur le poste empêche d’y installer le guet."
          }
        },
        "temoins": [
          {
            "id": "G12_T1",
            "resume": "Plume en E. L’Ibijau piège E3 vide de Défenseurs. Les Entités peuvent y garder ce Piège contre un Bulldozer ou le sacrifier avec le Rêve du Ciel sous l’écorce.",
            "etat_attendu_verifie": {
              "entree": {
                "plume": "E",
                "cible": "E3",
                "defenseurs": [],
                "pieges": [],
                "rang_ciel": 4,
                "rangs_libres": [
                  3
                ]
              },
              "transition_python": "p=s['cible']\nif p[0]==s['plume'] and p not in s['defenseurs'] and p not in s['pieges']:\n    s['pieges'].append(p)\npeut_sacrifier=any(x[0]==s['plume'] for x in s['pieges']) and s['rang_ciel']-1 in s['rangs_libres']\nr=[s['pieges'],peut_sacrifier]",
              "attendu": [
                [
                  "E3"
                ],
                true
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G12_T2",
            "resume": "Deux activations F1 sous la même Plume couvrent deux cibles vides du rayon O. Aucune icône ne s’allume à la pose.",
            "etat_attendu_verifie": {
              "entree": {
                "plume": "O",
                "cibles": [
                  "O1",
                  "O3"
                ],
                "defenseurs": [
                  "O4"
                ],
                "pieges": []
              },
              "transition_python": "for c in s['cibles']:\n    if c[0]==s['plume'] and c not in s['defenseurs'] and c not in s['pieges']:\n        s['pieges'].append(c)\nr=s['pieges']",
              "attendu": [
                "O1",
                "O3"
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Privilégier une cible désertée par nécessité. Conserver le Piège si sa consommation empêcherait une Route.",
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
        "vecteurs": "DUEL (+ INSECTE Face 2) → DEFENSEUR_REDEPLOYE / INSECTE / DUEL",
        "entrees_plancher": [
          "DUEL"
        ],
        "entrees_synergie": [
          "INSECTE"
        ],
        "entrees": [
          "DUEL",
          "INSECTE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "INSECTE",
          "DUEL"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE",
          "ICONE_INSECTE"
        ],
        "double_ouverture": "À chaque passage, garnissez la case que le Mammifère s’apprête à quitter. Deux percées successives laissent une file de deux parcelles occupées et un Défenseur au débouché.",
        "tags": [
          "INSECTES",
          "DUEL",
          "COLONNE",
          "FRONT"
        ],
        "tuile_plateau": {
          "nom_court": "Le Tamanoir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_INSECTE",
            "PIC_DEFENSEUR",
            "PIC_MIGRATION"
          ],
          "mots_cles_plateau": {
            "face_1": "Ouvrir le front",
            "face_2": "Longer la colonne",
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Ouvrière au départ · guide un pas / traversée de la file + Duel"
        },
        "carte_joueur": {
          "titre_complet": "Le Tamanoir",
          "entite_illustree": "Le Tamanoir entier éventrant du bout des griffes un bourrelet de terre",
          "brief_illustration": "Le tamanoir entier éventre du bout des griffes un bourrelet de terre. Sa longue queue protège la file qui sort tandis qu’il avance vers le talus suivant.",
          "pitch_ambiance": "À chaque pas du géant, la terre s’ouvre derrière lui.",
          "texte_regle": {
            "face_1": "Ouvrir le front. Faites sortir un Insecte de la réserve sur une parcelle de M ou I (ou sur une parcelle survivante d’un autre rayon si M et I sont entièrement Route). Si l’un de vos Défenseurs y est debout, vous pouvez le faire avancer d’un pas radial dans le sens choisi. L’ouvrière reste au départ. Si le Défenseur part du Duel, laissez-le en place sur sa face actuelle ou emportez-le à l’arrivée face Défi.",
            "face_2": "Longer la colonne. Faites sortir l’Insecte comme en Face 1. Depuis sa parcelle, vous pouvez conduire un de vos Défenseurs dans un sens le long d’une file continue de parcelles portant chacune au moins un Insecte au sol. Arrêtez-vous sur une autre parcelle de la file ou sur la première parcelle au-delà, même vide. Les Insectes restent en place. Le choix d’emporter le Duel face Défi ou de conserver sa face au départ vous appartient toujours.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Laisser l’ouvrière derrière le combattant pour préparer la galerie de M1 et porter le Défenseur sur la frappe suivante, avec ou sans déplacement du Duel.",
            "renoncement": "Emporter un Territoire tenu ouvre un nouveau Défi mais libère l’ancien passage."
          }
        },
        "temoins": [
          {
            "id": "G13_T1",
            "resume": "Une ouvrière occupe M1 en M·1 ; un Mammifère et son Duel face Défi sont en M·2. G13 fait sortir une ouvrière en M·2 et conduit le Mammifère avec le Duel en M·3. Contre une frappe au seuil de 3, M1 paie 1 ouvrière de M·2 et 1 de M·1 : Parade allumant Insecte et Duel retourné sur Territoire tenu.",
            "etat_attendu_verifie": {
              "ouvriere_m2": 1,
              "mammifere_m3": true,
              "territoire_tenu": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Faire sortir l’ouvrière sous un Mammifère à déplacer vers la frappe suivante afin de prolonger la file de M1 tout en couvrant le front ; en Face 2, longer toute la colonne d’Insectes.",
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
        "vecteurs": "INSECTE (+ PIEGE / INSECTE_RANG / GARDIEN) → INSECTE_RANG / INSECTE_ICONE / INSECTE",
        "entrees_plancher": [
          "INSECTE"
        ],
        "entrees_synergie": [
          "PIEGE",
          "INSECTE_RANG",
          "GARDIEN"
        ],
        "entrees": [
          "INSECTE",
          "PIEGE",
          "INSECTE_RANG",
          "GARDIEN"
        ],
        "sorties": [
          "INSECTE_RANG",
          "INSECTE_ICONE",
          "INSECTE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_INSECTE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Deux Sabotages révélés successivement donnent deux fouilles avant les déviations. La première ouvrière peut gagner le rang d’une machine par une fosse, la seconde rejoindre un Nid au sol, à temps pour sa Production.",
        "tags": [
          "INSECTES",
          "FOUILLE",
          "PIEGE",
          "PISTES"
        ],
        "tuile_plateau": {
          "nom_court": "Le Téju",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_INSECTE",
            "PIC_PIEGE",
            "PIC_RANG_MACHINE",
            "PIC_PARI_ENCOCHE"
          ],
          "mots_cles_plateau": {
            "face_1": "Fouille",
            "face_2": "Rabattre au terrier",
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Sol / fosse ouverte → piste · retour au sol → filet redéployé"
        },
        "carte_joueur": {
          "titre_complet": "Le Téju",
          "entite_illustree": "Le Téju entier raclant de biais un talus chaud pour ouvrir une galerie",
          "brief_illustration": "Le téju entier racle de biais un talus chaud. Un éclat d’argile roule entre ses pattes et découvre l’ouverture d’une galerie.",
          "pitch_ambiance": "Une motte saute. Les ouvrières trouvent une issue là où le filet tenait encore.",
          "texte_regle": {
            "face_1": "Fouille. Faites sortir un Insecte de la réserve au sol sur une parcelle de R ou I (ou sur une parcelle survivante d’un autre rayon si R et I sont entièrement Route). Vous pouvez à la place ouvrir une fosse sur l’un de ces rayons : rendez un Piège ordinaire de ce rayon à la réserve et posez l’Insecte de la réserve directement sur un rang de la Réglette ou sur l’icône d’un Gardien en piste. L’Insecte pourra servir à la prochaine déviation légale ou au Bouclier de lisière, au choix de I.",
            "face_2": "Rabattre au terrier. Vous pouvez effectuer la Fouille. Vous pouvez aussi choisir un Piège ordinaire de R ou I et y rabattre un Insecte depuis un rang ou une icône. Posez-le au sol à la place du Piège, puis déplacez ce Piège sur une autre parcelle encore ciblée du même rayon, libre de Piège ordinaire. Les deux destinations doivent être légales avant le rabattage.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Faire sortir une ouvrière au sol, briser un Piège de M2 pour propulser l’Essaim sur les pistes centrales, ou rappeler en Face 2 une ouvrière pour redéployer le Piège ailleurs.",
            "renoncement": "Ouvrir une fosse consomme le Piège ordinaire ; rappeler un Insecte en Face 2 retire une déviation ou un Bouclier de lisière possible."
          }
        },
        "temoins": [
          {
            "id": "G14_T1",
            "resume": "M2 a façonné un Piège en I·1 ; une mobile est révélée au rang 4 et deux Sabotages s’ouvrent. G14 (2 paris sur Sabotage) ouvre le Piège au 1er balayage et pose une ouvrière sur le rang 4, puis fait sortir une ouvrière sur M2 au 2nd balayage. I dévie la mobile au rang 3 (allume Insecte). Sans Piège, la sortie au sol reste disponible.",
            "etat_attendu_verifie": {
              "insecte_rang_4": 1,
              "deviation_possible": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Si une déviation ±1 ou un Bouclier de lisière est décisif et qu’un Piège non critique existe sur R ou I, ouvrir une fosse vers la Réglette/Piste ; sinon renforcer directement un Nid ou une parcelle de R ou I.",
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
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "DES_SOUS_PARAVENT + INSECTE + INSECTE_RANG + RANG_MACHINE → INSECTE_RANG / INSECTE_RAPATRIE",
        "entrees_plancher": [
          "DES_SOUS_PARAVENT",
          "INSECTE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "INSECTE_RANG"
        ],
        "entrees": [
          "DES_SOUS_PARAVENT",
          "INSECTE",
          "RANG_MACHINE",
          "INSECTE_RANG"
        ],
        "sorties": [
          "INSECTE_RANG",
          "INSECTE_RAPATRIE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_INSECTE"
        ],
        "double_ouverture": "Deux vols peuvent fournir deux déviations distinctes au même rang ou évacuer deux ouvrières vers deux cibles.",
        "tags": [
          "INSECTES",
          "NECTAR",
          "DE_ECARTE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Colibri",
          "fenetre_badge": "OUVERTURE / ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_DES_PARAVENT",
            "PIC_INSECTE",
            "PIC_MIGRATION",
            "PIC_RANG_MACHINE"
          ],
          "mots_cles_plateau": {
            "face_1": "Grand dé · nectar",
            "face_2": "Nectar · vol retour",
            "enracine": null
          },
          "resume_plateau": "Grand dé · nectar / Nectar · vol retour"
        },
        "carte_joueur": {
          "titre_complet": "Le Colibri",
          "entite_illustree": "Colibri à la lisière des fleurs",
          "brief_illustration": "Colibri entier en vol stationnaire entre deux rangées de fleurs, leurs calices dessinant une montée dans la lumière.",
          "pitch_ambiance": "Le colibri revient de corolle en corolle par le même chemin. Une fleur vidée change le sens de sa tournée.",
          "texte_regle": {
            "face_1": "À l’ouverture, laissez visible le plus grand dé standard de l’Oiseau à sa valeur lancée, même sur Sabotage ou Écaille. En cas de double, gardez le dé inutilisé. À chaque activation, vous pouvez envoyer un Insecte au sol de O ou I directement sur le rang indiqué par ce dé. L’envoi ne dépense pas l’Insecte et ne déclenche pas de déviation à lui seul.",
            "face_2": "À l’ouverture, conservez visible le plus grand dé standard de l’Oiseau à sa valeur lancée, même sur Sabotage ou Écaille. En cas de double, gardez le dé inutilisé. À chaque activation, vous pouvez envoyer un Insecte au sol de n’importe quel rayon directement sur ce rang, ou en ramener un de ce rang sur une parcelle encore ciblée. Un transfert seul n’allume aucune icône.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Stocker un vol sur la Réglette ou ramener le dernier renfort vers une frappe ?",
            "renoncement": "Une ouvrière descendue du rang ne pourra plus y dévier une machine."
          }
        },
        "temoins": [
          {
            "id": "G15_T1",
            "resume": "L’Oiseau a tiré Sabotage et lancé 2 et 5. Le Colibri envoie une ouvrière sur 5 lors du balayage du Sabotage. À la fenêtre suivante, elle peut être défaussée pour dévier la machine de 5 à 4 sur un Rêve défendu.",
            "etat_attendu_verifie": {
              "entree": {
                "standard": [
                  2,
                  5
                ],
                "jeton": "Sabotage",
                "insecte_sol": 1,
                "actif": 5,
                "rang_reve": 4
              },
              "transition_python": "nectar=max(s['standard'])\nrang=[nectar] if s['insecte_sol'] else []\nif s['actif'] in rang and abs(s['rang_reve']-s['actif'])==1:\n    rang.remove(s['actif'])\n    s['actif']=s['rang_reve']\nr=[nectar,rang,s['actif']]",
              "attendu": [
                5,
                [],
                4
              ]
            },
            "statut": "OK"
          },
          {
            "id": "G15_T2",
            "resume": "Le grand dé standard indique 5. Deux vols montent deux ouvrières et permettent de dévier deux machines différentes du rang 5 vers le rang 4.",
            "etat_attendu_verifie": {
              "entree": {
                "des": [
                  5,
                  1
                ],
                "sol": 2,
                "machines": [
                  5,
                  5
                ],
                "cible": 4
              },
              "transition_python": "nectar=max(s['des'])\nrang=0\nfor _ in range(2):\n    if s['sol']:\n        s['sol']-=1\n        rang+=1\nfor i,p in enumerate(s['machines']):\n    if rang and p==nectar and abs(p-s['cible'])==1:\n        s['machines'][i]=s['cible']\n        rang-=1\nr=[s['machines'],rang,s['sol']]",
              "attendu": [
                [
                  4,
                  4
                ],
                0,
                0
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Envoyer au rang si la fenêtre de déviation est encore à venir et si une machine y est visible. Sinon préférer une défense immédiate en Face 2.",
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
          "LEVIER_REVE",
          "TWIST_2K3",
          "AUTONOMIE_A0"
        ],
        "est_twist": true,
        "vecteurs": "POSITION_REVE + RANG_REVE → RANG_REVE",
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
          "RANG_REVE"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "A0",
          "PISTON",
          "BLOC"
        ],
        "tuile_plateau": {
          "nom_court": "La Nasse à contre-courant",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_REVE",
            "PIC_AVANCEE_REVE",
            "PIC_CHANT",
            "PIC_TWIST"
          ],
          "mots_cles_plateau": {
            "face_1": "Reflux à droite · bloc à gauche",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Reflux à droite · bloc à gauche"
        },
        "carte_joueur": {
          "titre_complet": "La Nasse à contre-courant",
          "entite_illustree": "Vision d’une nasse de joncs",
          "brief_illustration": "Nasse de joncs à demi-submergée, deux barques de brume glissant contre le fil de l’eau.",
          "pitch_ambiance": "La nasse cède d’une maille. Une brassée de rêves passe dans l’autre sens.",
          "texte_regle": {
            "face_1": "Au pouvoir de ce Rêve défendu, vous pouvez le reculer d’un rang libre vers la droite pour avancer d’un rang vers la gauche un bloc d’un ou deux autres Rêves contigus. Le bloc doit être entièrement à gauche du rang quitté et avoir une case libre à sa gauche. Déplacez d’abord la Nasse puis le bloc, en commençant par son Rêve le plus à gauche. Tous les Défenseurs suivent. Reprenez la lecture des Rêves à droite de la nouvelle case de la Nasse. Aucun Rêve déplacé ne se résout de nouveau.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Accepter un trou derrière le bloc pour gagner deux rangs à gauche ?",
            "renoncement": "La Nasse recule elle-même. Il faudra encore la ramener pour obtenir le Sommeil."
          }
        },
        "temoins": [
          {
            "id": "R1_T1",
            "resume": "Rêves en 3 et 4, Nasse défendue en 5, rangs 2 et 6 libres. La Nasse passe en 6, les deux Rêves passent en 2 et 3, avec leurs pions. Aucun ne se résout deux fois.",
            "etat_attendu_verifie": {
              "entree": {
                "rangs": {
                  "A": 3,
                  "B": 4,
                  "N": 5
                },
                "pions": {
                  "A": 1,
                  "B": 0,
                  "N": 1
                },
                "bloc": [
                  "A",
                  "B"
                ]
              },
              "transition_python": "pos=s['rangs']\nbloc=s['bloc']\nold=pos['N']\nseq=[pos[k] for k in bloc]\nif old<6 and old+1 not in pos.values() and seq==list(range(seq[0],seq[0]+len(seq))) and 1<seq[0]<=seq[-1]<old and seq[0]-1 not in pos.values():\n    pos['N']+=1\n    for k in bloc:\n        pos[k]-=1\nr=[pos,{str(pos[k]):n for k,n in s['pions'].items() if n}]",
              "attendu": [
                {
                  "A": 2,
                  "B": 3,
                  "N": 6
                },
                {
                  "2": 1,
                  "6": 1
                }
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Reculer surtout pour avancer deux Rêves et libérer une trajectoire de Chant. Conserver sa place si le recul briserait un Sommeil déjà acquis.",
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
        "vecteurs": "DUEL + TERRITOIRE + TAMBOUR + ROUTE → PIEGE",
        "entrees_plancher": [
          "DUEL",
          "TERRITOIRE",
          "ROUTE"
        ],
        "entrees_synergie": [
          "TAMBOUR"
        ],
        "entrees": [
          "DUEL",
          "TERRITOIRE",
          "ROUTE",
          "TAMBOUR"
        ],
        "sorties": [
          "PIEGE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE",
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "EMPREINTES"
        ],
        "tuile_plateau": {
          "nom_court": "Les Pas dans l’eau",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_TAMBOUR",
            "PIC_PIEGE"
          ],
          "mots_cles_plateau": {
            "face_1": "Défi devant · Tenu derrière",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Défi devant · Tenu derrière"
        },
        "carte_joueur": {
          "titre_complet": "Les Pas dans l’eau",
          "entite_illustree": "Vision de traces remplies de pluie",
          "brief_illustration": "Des empreintes géantes se remplissent à rebours le long d’une piste entre arbres et eau noire.",
          "pitch_ambiance": "À chaque pas du Tambour, une empreinte se remplit avant que la pluie ne tombe.",
          "texte_regle": {
            "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, si le Duel est en forêt, vous pouvez poser un Piège ordinaire de la réserve un pas radial vers le cœur depuis le Duel face Défi, ou vers la bordure depuis le Territoire tenu. Sautez les Routes. Si le Tambour est sur le Duel, vous choisissez le sens. Il faut une parcelle libre de Piège ordinaire.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Couvrir l’avancée ou garder l’arrière ?",
            "renoncement": "Un Tambour engagé auprès du Duel ne défend pas un Rêve."
          }
        },
        "temoins": [
          {
            "id": "R3_T1",
            "resume": "Le Duel face Défi est en M2, le Tambour aussi. Les Humains choisissent M1 derrière le Duel. Le Piège y intercepte un Bulldozer pendant que la Parade en M2 peut établir le Territoire tenu.",
            "etat_attendu_verifie": {
              "entree": {
                "duel": 2,
                "face": "Défi",
                "tambour": 2,
                "direction_choisie": -1,
                "routes": [],
                "pieges": []
              },
              "transition_python": "sens=s['direction_choisie'] if s['duel']==s['tambour'] else (1 if s['face']=='Défi' else -1)\np=s['duel']+sens\nwhile p in s['routes']:\n    p+=sens\nif 1<=p<=4 and p not in s['pieges']:\n    s['pieges'].append(p)\nr=[s['pieges'],s['duel'] in s['pieges']]",
              "attendu": [
                [
                  1
                ],
                false
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Viser la frappe qui détruirait le plus de Souches sans interposer un Piège sur la parcelle même du Duel.",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "POSITION_REVE + TAMBOUR (+ ANNULATION / PIEGE / CROC) → PIEGE / DEFENSEUR_REDEPLOYE",
        "entrees_plancher": [
          "POSITION_REVE",
          "TAMBOUR"
        ],
        "entrees_synergie": [
          "ANNULATION",
          "PIEGE",
          "CROC"
        ],
        "entrees": [
          "POSITION_REVE",
          "TAMBOUR",
          "ANNULATION",
          "PIEGE",
          "CROC"
        ],
        "sorties": [
          "PIEGE",
          "DEFENSEUR_REDEPLOYE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE",
          "ICONE_PIEGEAGE",
          "ICONE_PARADE"
        ],
        "double_ouverture": null,
        "tags": [
          "TRAVERSEE",
          "PIEGE",
          "FURTIVITE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Tambour des deux berges",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_TAMBOUR",
            "PIC_PIEGE",
            "PIC_CROC",
            "PIC_DEFENSEUR"
          ],
          "mots_cles_plateau": {
            "face_1": "Traversée · Débarquement",
            "face_2": null,
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Rayon annulé / pointe du Croc / foyer H · filet vers cible ou veilleur à terre"
        },
        "carte_joueur": {
          "titre_complet": "Le Tambour des deux berges",
          "entite_illustree": "Tambour tendu au-dessus d’un bras mort reliant une clairière abandonnée à une rive vivante",
          "brief_illustration": "Un tambour tendu au-dessus d’un bras mort, ses cordes reliant une clairière abandonnée à une rive vivante.",
          "pitch_ambiance": "Un coup résonne du côté où la machine s’est tue. Sur l’autre berge, quelqu’un ramasse le filet.",
          "texte_regle": {
            "face_1": "Appeler la berge. Après les annulations de ce Rêve défendu, choisissez le rayon d’une machine qu’il vient d’annuler, le rayon que pointe le Croc à l’affût du Caïman, ou votre propre rayon H. Si le rayon choisi est entièrement Route, prenez un autre rayon ouvert.\nTransporter : prenez un Piège ordinaire sur le rayon choisi et portez-le sur une parcelle encore ciblée d’un autre rayon, libre de Piège ordinaire. Si le Tambour occupait la parcelle de départ, vous pouvez l’emporter avec le Piège.\nDébarquer : vous pouvez aussi prendre un Défenseur de ce Rêve et le poser sur une parcelle du rayon choisi ou sur une place libre de l’une de ses deux rives de Furtivité. Cette option reste ouverte à zéro annulation et même si aucun Piège n’est en jeu. Les annulations déjà résolues sont acquises. Une rive ainsi rejointe sera évaluée à la Furtivité.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Exporter un Piège (et éventuellement le Tambour) vers une cible urgente ailleurs, ou débarquer un Défenseur du Rêve sur le terrain ou sur une rive de Furtivité.",
            "renoncement": "Débarquer un veilleur complète un équipage avant la Furtivité mais dégarnit la Réglette ; exporter un filet découvre la parcelle de départ."
          }
        },
        "temoins": [
          {
            "id": "R4_T1",
            "resume": "R4 défendu par le Chant se résout à rang vide (rayon R libre de Piège ordinaire). Le Croc de G9 Face 2 pointe vers R et un Défenseur attend sur la Rive Piège de H. R4 débarque le Chant sur celle de R : à la Furtivité avec m(R)=1 et m(H)=1, G9 réunit l’équipage partagé et R gagne 1 Piège. Seul, R4 débarque le Chant sur H·2.",
            "etat_attendu_verifie": {
              "chant_debarque_rive_r": true,
              "piege_confluent": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Exporter un Piège non menacé (avec le Tambour si présent) vers une parcelle ciblée prioritaire, ou débarquer le Défenseur de R4 pour fermer une rive de Furtivité (confluent G9) ou renforcer une Parade.",
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
        "vecteurs": "TAMBOUR + INSECTE + RANG_MACHINE + POSITION_REVE → INSECTE_RANG",
        "entrees_plancher": [
          "TAMBOUR",
          "INSECTE",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "TAMBOUR",
          "INSECTE",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "sorties": [
          "INSECTE_RANG"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "RAPPEL"
        ],
        "tuile_plateau": {
          "nom_court": "Le Chant des chambres creuses",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_TAMBOUR",
            "PIC_INSECTE",
            "PIC_RANG_MACHINE",
            "PIC_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Tambour en forêt · montée au rang",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Tambour en forêt · montée au rang"
        },
        "carte_joueur": {
          "titre_complet": "Le Chant des chambres creuses",
          "entite_illustree": "Vision d’une calebasse habitée",
          "brief_illustration": "Une calebasse ouverte comme une caisse de résonance, une piste d’ouvrières courant jusqu’à son bord.",
          "pitch_ambiance": "Le Chamane approche l’oreille de la calebasse. Des pas minuscules y battent déjà le rappel.",
          "texte_regle": {
            "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, si le Tambour est en forêt, vous pouvez prendre un Insecte au sol sur sa parcelle et le poser sur le rang de ce Rêve ou sur celui d’une machine visible encore active. Si cette machine menace la parcelle du Tambour, vous pouvez aussi transporter un second Insecte de cette parcelle sur le même rang. La fenêtre de déviation de cette ouverture est déjà passée.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Parier sur le prochain tirage ou garder autour du Tambour de quoi parer aujourd’hui ?",
            "renoncement": "Les ouvrières montées au rang manquent aux frappes imminentes."
          }
        },
        "temoins": [
          {
            "id": "R6_T1",
            "resume": "Le Nid des calebasses a rassemblé trois ouvrières auprès du Tambour. Au tour suivant, le Chant en envoie deux sur 3, rang d’une machine qui vise le Tambour. Elles y attendent la prochaine ouverture.",
            "etat_attendu_verifie": {
              "entree": {
                "tambour": "H4",
                "stock": 3,
                "rang": 3,
                "cibles": [
                  "H4"
                ],
                "rang_reve": 5
              },
              "transition_python": "n=min(s['stock'],1+int(s['tambour'] in s['cibles']))\nr=[s['stock']-n,{str(s['rang']):n}]",
              "attendu": [
                1,
                {
                  "3": 2
                }
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Prélever les ouvrières surnuméraires après calcul du seuil autour du Tambour. Choisir un rang utile à un futur Rêve.",
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "roles_portes": [
          "LEVIER_REVE"
        ],
        "est_twist": false,
        "vecteurs": "DUEL + RANG_MACHINE + POSITION_REVE → ALTERATION / RANG_REVE",
        "entrees_plancher": [
          "DUEL",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "DUEL",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "sorties": [
          "ALTERATION",
          "RANG_REVE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "AMARRAGE"
        ],
        "tuile_plateau": {
          "nom_court": "La Pirogue sans rameur",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_ALTERATION",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Remous · amarrage",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Remous · amarrage"
        },
        "carte_joueur": {
          "titre_complet": "La Pirogue sans rameur",
          "entite_illustree": "Vision d’une pirogue menée par son reflet",
          "brief_illustration": "Pirogue vide à la jonction de deux eaux, sa ligne de flottaison se prolongeant en sillage autour d’un gué.",
          "pitch_ambiance": "La pirogue remonte le courant. Sous sa coque, le reflet descend vers le gué.",
          "texte_regle": {
            "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez poser une Altération de la réserve sur une machine mobile de M ou E qui n’en porte pas. Si elle se trouve sur la parcelle du Duel, vous pouvez aussi avancer ce Rêve d’un rang vers la gauche si la case est libre. Les Défenseurs embarqués suivent.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Marquer la machine la plus dangereuse ou amarrer la pirogue au Duel ?",
            "renoncement": "Une meilleure position sur la Réglette peut coûter le recul d’une autre machine."
          }
        },
        "temoins": [
          {
            "id": "R7_T1",
            "resume": "Duel et Bulldozer mobile occupent M2. La Pirogue le marque et passe de 5 à 4. À sa prochaine révélation, le Bulldozer recule sans frapper mais compte pour la Furtivité.",
            "etat_attendu_verifie": {
              "entree": {
                "duel": "M2",
                "machine": "M2",
                "mobile": true,
                "rang": 5,
                "occupes": [
                  5
                ],
                "alteree": false
              },
              "transition_python": "if s['mobile'] and not s['alteree']:\n    s['alteree']=True\n    if s['duel']==s['machine'] and s['rang']>1 and s['rang']-1 not in s['occupes']:\n        s['rang']-=1\nr=[s['rang'],s['alteree']]",
              "attendu": [
                4,
                true
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Donner la priorité au glissement qui ferme un trou vers le Sommeil si le Bulldozer du Duel menace aussi des Souches.",
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
          "LEVIER_REVE",
          "LOI_PASSIVE",
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "ALTERATION + RANG_MACHINE + CROC + POSITION_REVE → RANG_REVE / ALTERATION",
        "entrees_plancher": [
          "ALTERATION",
          "RANG_MACHINE",
          "POSITION_REVE"
        ],
        "entrees_synergie": [
          "CROC"
        ],
        "entrees": [
          "ALTERATION",
          "RANG_MACHINE",
          "POSITION_REVE",
          "CROC"
        ],
        "sorties": [
          "RANG_REVE",
          "ALTERATION"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "MUE",
          "ANTICIPATION"
        ],
        "tuile_plateau": {
          "nom_court": "La Peau du fleuve",
          "fenetre_badge": "RETRAIT ALTÉRATION / OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_ALTERATION",
            "PIC_AVANCEE_REVE",
            "PIC_CROC",
            "PIC_LOI_PASSIVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Mue · rang révélé",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Mue · rang révélé"
        },
        "carte_joueur": {
          "titre_complet": "La Peau du fleuve",
          "entite_illustree": "Vision d’un fleuve qui sort de sa peau",
          "brief_illustration": "Deux méandres superposés, l’un d’eau et l’autre de vase craquelée, avec une ligne d’écailles à leur jonction.",
          "pitch_ambiance": "Le fleuve abandonne son ancienne courbe. Le lit vide garde un instant la forme de ce qui va arriver.",
          "texte_regle": {
            "face_1": "Sur la Réglette, même sans Défenseur, ce Rêve peut prendre le rang révélé d’une mobile dont on retire l’Altération, s’il est libre et à sa gauche. Déplacez-le avec ses Défenseurs avant les Sabotages. La machine recule et reste privée de frappe comme prévu. Pour plusieurs retraits simultanés, les Entités choisissent leur ordre. Au pouvoir de ce Rêve défendu, vous pouvez altérer une mobile sans Altération de E ou R, ou de tout rayon portant le Croc. Posez le jeton de la réserve.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Sauter vers le Sommeil ou conserver le rang d’une annulation certaine ?",
            "renoncement": "À son arrivée, la machine qui a payé le passage est déjà neutralisée. Il faut une autre machine pour y réussir une annulation."
          }
        },
        "temoins": [
          {
            "id": "R8_T1",
            "resume": "Une mobile altérée révèle 2. La Peau, défendue en 5, rejoint le 2 libre. La première machine recule. Une seconde machine de rang 2 peut alors être annulée par le Rêve.",
            "etat_attendu_verifie": {
              "entree": {
                "reve": 5,
                "occupes": [
                  5
                ],
                "rang_alteree": 2,
                "autres_actives": [
                  2
                ],
                "pions": 1
              },
              "transition_python": "cible=s['rang_alteree']\nif cible<s['reve'] and cible not in s['occupes']:\n    s['reve']=cible\nannulations=min(s['pions'],s['autres_actives'].count(s['reve']))\nr=[s['reve'],annulations,annulations>0]",
              "attendu": [
                2,
                1,
                true
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Sauter si le rang d’arrivée ferme le bloc de gauche ou contient une seconde machine plus menaçante que celle du rang quitté.",
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
        "vecteurs": "PLUME + PIEGE + DE_ENVOL + POSITION_REVE → RANG_REVE / ALTERATION",
        "entrees_plancher": [
          "PLUME",
          "PIEGE",
          "POSITION_REVE"
        ],
        "entrees_synergie": [
          "DE_ENVOL"
        ],
        "entrees": [
          "PLUME",
          "PIEGE",
          "POSITION_REVE",
          "DE_ENVOL"
        ],
        "sorties": [
          "RANG_REVE",
          "ALTERATION"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "CONSTELLATION"
        ],
        "tuile_plateau": {
          "nom_court": "Le Ciel sous l’écorce",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_PIEGE",
            "PIC_PERCHOIR",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "Poste sacrifié · étoile basse",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Poste sacrifié · étoile basse"
        },
        "carte_joueur": {
          "titre_complet": "Le Ciel sous l’écorce",
          "entite_illustree": "Vision d’une constellation d’écorce",
          "brief_illustration": "Arbre creux ouvert sur un firmament inversé, une plume claire au pied du tronc.",
          "pitch_ambiance": "On détache une écaille de bois. Derrière elle, une étoile attendait à hauteur de main.",
          "texte_regle": {
            "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, si la Plume indique un rayon, vous pouvez y défausser un Piège ordinaire pour avancer ce Rêve d’un rang libre vers la gauche. Si le Dé d’Envol montre le rang d’arrivée, vous pouvez ensuite poser une Altération de la réserve sur une mobile de ce rayon qui n’en porte pas. Les Défenseurs suivent le Rêve.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Brûler un guet de l’Ibijau pour gagner un rang ?",
            "renoncement": "Si le Dé d’Envol ne coïncide pas, la machine de ce rayon conserve son prochain passage."
          }
        },
        "temoins": [
          {
            "id": "R9_T1",
            "resume": "Plume en E, Dé d’Envol sur 3. Le Ciel en 4 sacrifie le Piège de l’Ibijau, rejoint le 3 libre et altère le Bulldozer mobile d’E.",
            "etat_attendu_verifie": {
              "entree": {
                "rank": 4,
                "envol": 3,
                "occupes": [
                  4
                ],
                "pieges": [
                  "E3"
                ],
                "plume": "E",
                "mobile_sans_marque": true
              },
              "transition_python": "g=s['rank']-1\neligible=[x for x in s['pieges'] if x[0]==s['plume']]\nmarque=False\nif eligible and g>=1 and g not in s['occupes']:\n    s['pieges'].remove(eligible[0])\n    s['rank']=g\n    marque=s['envol']==g and s['mobile_sans_marque']\nr=[s['rank'],s['pieges'],marque]",
              "attendu": [
                3,
                [],
                true
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Dépenser en priorité un Piège éloigné des cibles, surtout si le dé offre aussi une Altération.",
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
          "LEVIER_REVE",
          "AUTONOMIE_A0"
        ],
        "est_twist": false,
        "vecteurs": "INSECTE_RANG + INSECTE + POSITION_REVE + RANG_MACHINE → RANG_REVE / ALTERATION / INSECTE_IMMERGE",
        "entrees_plancher": [
          "INSECTE_RANG",
          "INSECTE",
          "POSITION_REVE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "INSECTE_RANG",
          "INSECTE",
          "POSITION_REVE",
          "RANG_MACHINE"
        ],
        "sorties": [
          "RANG_REVE",
          "ALTERATION",
          "INSECTE_IMMERGE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "PLONGEE"
        ],
        "tuile_plateau": {
          "nom_court": "Les Lanternes englouties",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_INSECTE",
            "PIC_AVANCEE_REVE",
            "PIC_ALTERATION"
          ],
          "mots_cles_plateau": {
            "face_1": "Lanterne du rang · plongée",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Lanterne du rang · plongée"
        },
        "carte_joueur": {
          "titre_complet": "Les Lanternes englouties",
          "entite_illustree": "Vision de lumières sous les racines",
          "brief_illustration": "Traînée de petites lumières au ras de l’eau, puis sous des racines immergées comme des arches.",
          "pitch_ambiance": "Une lumière s’éteint à la surface. Sous les racines, le cortège gagne une longueur de pirogue.",
          "texte_regle": {
            "face_1": "À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez retirer un Insecte du rang de ce Rêve pour avancer celui-ci d’un rang libre vers la gauche avec ses Défenseurs. Posez cet Insecte au sol sur une parcelle de E ou I portant une machine mobile. S’il y rejoint un autre Insecte au sol, vous pouvez poser une Altération de la réserve sur une mobile de cette parcelle qui n’en porte pas. Le mouvement exige les deux destinations légales.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Garder l’Insecte pour dévier ou le faire plonger à l’endroit d’une future frappe ?",
            "renoncement": "La Réglette perd son aiguilleur pour gagner un rang de Sommeil."
          }
        },
        "temoins": [
          {
            "id": "R10_T1",
            "resume": "Le Nid des reflets a garni le rang 4. Les Lanternes en 4 passent en 3 libre. L’ouvrière rejoint une autre en E2 et les Entités y altèrent l’Abatteuse mobile.",
            "etat_attendu_verifie": {
              "entree": {
                "rang": 4,
                "occupes": [
                  4
                ],
                "stock_rang": 1,
                "sol": 1,
                "mobile": true,
                "marque": false
              },
              "transition_python": "if s['stock_rang'] and s['rang']>1 and s['rang']-1 not in s['occupes'] and s['mobile']:\n    s['stock_rang']-=1\n    s['rang']-=1\n    s['marque']=s['marque'] or s['sol']>0\n    s['sol']+=1\nr=[s['rang'],s['stock_rang'],s['sol'],s['marque']]",
              "attendu": [
                3,
                0,
                2,
                true
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Privilégier une arrivée qui réalise à la fois l’Altération et un pas vers le bloc de Sommeil.",
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
        "cycle": "PASSIF_CONTINU",
        "cablage": null,
        "roles_portes": [
          "TWIST_2K3",
          "LOI_PASSIVE"
        ],
        "est_twist": true,
        "vecteurs": "NID_ACTIVE + INSECTE (+ DUEL) → PARADE_GALERIE / TERRITOIRE",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE"
        ],
        "entrees_synergie": [
          "DUEL"
        ],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "DUEL"
        ],
        "sorties": [
          "PARADE_GALERIE",
          "TERRITOIRE"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [
          "ICONE_INSECTE"
        ],
        "double_ouverture": null,
        "tags": [
          "INSECTES",
          "LOI_PASSIVE",
          "TWIST",
          "CONTRE_SAPE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Nid de la contre-sape",
          "fenetre_badge": "PRODUCTION / FRAPPE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_INSECTE",
            "PIC_DUEL",
            "PIC_TWIST"
          ],
          "mots_cles_plateau": {
            "face_1": "Galerie continue",
            "face_2": null,
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Nid → file au sol → Défenseur · un paiement par case"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid de la contre-sape",
          "entite_illustree": "Coupe de berge montrant des chambres souterraines alignées sous des racines",
          "brief_illustration": "Une coupe de la berge montre des chambres alignées sous des racines. À la sortie, la patte d’un mammifère comprime la voûte sans l’effondrer.",
          "pitch_ambiance": "Le guetteur tient seul au jour. Sous ses pieds, toute la berge répond.",
          "texte_regle": {
            "face_1": "Ouvrir la galerie. Après la Production ordinaire de ce Nid défendu, vous pouvez faire avancer un Insecte de sa parcelle d’un pas radial. La Migration vient ensuite. Vous pouvez aussi le garder au Nid, déjà en mesure de soutenir la parcelle voisine.\nPayer depuis la galerie (Loi passive). Tant que M1 est en forêt, à une frappe sur une autre parcelle de son rayon portant au moins un Défenseur, vous pouvez choisir une Parade de galerie après le Croc et le Piège. Il faut une file ininterrompue d’Insectes au sol du Nid jusqu’à la parcelle voisine de la cible, Nid compris. Comptez les points qui manquent aux Défenseurs pour atteindre le seuil réel. En partant de la case de la file la plus proche de la cible, défaussez un Insecte par parcelle successive, à hauteur de ce manque. Il faut pouvoir payer tout le manque ainsi. Ce paiement remplace la dépense locale d’Insectes pour cette frappe. Avec au moins un Insecte dépensé, allumez seulement Insecte. Un Défenseur participant sur le Défi peut le retourner sur Territoire tenu.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Empiler les ouvrières au Nid pour entretenir la Production à deux, ou les étirer une par case pour allonger la portée de la galerie.",
            "renoncement": "Payer depuis l’extrémité de la galerie peut rompre la continuité avant une seconde frappe sur le rayon."
          }
        },
        "temoins": [
          {
            "id": "M1_T1",
            "resume": "M1, défendu en I·1, commence sa 1re Production à zéro et garde son unique ouvrière au Nid. Un Défenseur en I·2 subit une frappe au seuil de 2 (parcelle libre de Piège ordinaire) : I dépense l’ouvrière d’I·1 (1 Défenseur + 1 Insecte = 2). Au seuil de 3, même deux ouvrières empilées en I·1 n’auraient fourni qu’un seul point par la galerie.",
            "etat_attendu_verifie": {
              "parade_galerie_reussie": true,
              "max_1_par_case": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Maintenir une chaîne continue d’au moins 1 ouvrière par parcelle entre M1 et les Défenseurs avancés pour couvrir à distance les déficits de Seuil tout en préservant les 2 ouvrières au Nid quand c’est possible.",
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
        "vecteurs": "NID_ACTIVE + INSECTE (+ PIEGE) → PIEGE / INSECTES_TRANSPORTES",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE"
        ],
        "entrees_synergie": [
          "PIEGE"
        ],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "PIEGE"
        ],
        "sorties": [
          "PIEGE",
          "INSECTES_TRANSPORTES"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": null,
        "tags": [
          "INSECTES",
          "PIEGE",
          "ARGILE",
          "POTIERES"
        ],
        "tuile_plateau": {
          "nom_court": "Le Nid des fours d’argile",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_INSECTE",
            "PIC_PIEGE",
            "PIC_MIGRATION"
          ],
          "mots_cles_plateau": {
            "face_1": "Cuire ou déterrer",
            "face_2": null,
            "enracine": "Ordinaire"
          },
          "resume_plateau": "Ouvrière → Piège proche / Piège lointain ↔ ouvrière du Nid"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid des fours d’argile",
          "entite_illustree": "Nid d’argile au soleil bas montrant ses chambres ouvertes et ses minces couvercles d’ocre",
          "brief_illustration": "Au soleil bas, un nid d’argile montre ses chambres ouvertes et ses minces couvercles d’ocre. Le bord d’un couvercle affleure plus loin sous les feuilles.",
          "pitch_ambiance": "Les potières savent quelle croûte portera une patte et laquelle cédera sous une roue.",
          "texte_regle": {
            "face_1": "Cuire ou déterrer. Après la Production ordinaire de ce Nid défendu, vous pouvez cuire un couvercle : rendez un Insecte du Nid à la réserve et posez un Piège ordinaire de la réserve sur le Nid ou à un pas radial, sur une parcelle libre de Piège ordinaire. Vous pouvez plutôt déterrer un Piège situé sur une autre parcelle du rayon : échangez-le contre un Insecte du Nid. Le Piège arrive sur le Nid, qui doit être libre de Piège ordinaire, et l’Insecte arrive au sol sur la parcelle libérée. Il pourra migrer normalement. Dans les deux cas, vérifiez la place et les pièces disponibles avant le paiement.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Cuire une ouvrière en Piège autonome, la garder au Nid pour approcher la Production à deux, ou déterrer un filet lointain pour protéger le Nid tout en avançant l’ouvrière.",
            "renoncement": "Dépenser la première ouvrière ramène le Nid à zéro et ralentit la montée en régime de l’Essaim."
          }
        },
        "temoins": [
          {
            "id": "M2_T1",
            "resume": "Le Nid défendu en R·3 produit sa 1re ouvrière (aucun Piège ni Croc sur R). I dépense cette ouvrière et pose un Piège ordinaire en R·4 ; le Nid revient à zéro. Si le Bulldozer en Ratissage y frappe, le Piège pare sans Défenseur et allume Piégeage.",
            "etat_attendu_verifie": {
              "piege_r4": true,
              "insectes_nid": 0
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Cuire un Piège devant une menace proche (ou pour alimenter une fosse de G14), ou déterrer un Piège lointain pour projeter une ouvrière vers la sortie du rayon tout en couvrant le Nid.",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "NID_ACTIVE + PLUME + INSECTE_RANG + GARDIEN + INSECTE → INSECTE_ICONE / INSECTE_RAPPELE",
        "entrees_plancher": [
          "NID_ACTIVE",
          "PLUME",
          "INSECTE"
        ],
        "entrees_synergie": [
          "INSECTE_RANG",
          "GARDIEN"
        ],
        "entrees": [
          "NID_ACTIVE",
          "PLUME",
          "INSECTE",
          "INSECTE_RANG",
          "GARDIEN"
        ],
        "sorties": [
          "INSECTE_ICONE",
          "INSECTE_RAPPELE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "INSECTES",
          "TISSAGE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Nid des feuilles cousues",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_PLUME",
            "PIC_INSECTE",
            "PIC_PARI_ENCOCHE"
          ],
          "mots_cles_plateau": {
            "face_1": "Chaud · sentinelle / Calme · rappel",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Chaud · sentinelle / Calme · rappel"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid des feuilles cousues",
          "entite_illustree": "Nid suspendu entre deux feuilles",
          "brief_illustration": "Deux feuilles vivantes rapprochées par des fils, des ouvrières suspendues en chaîne sous la voûte.",
          "pitch_ambiance": "À la couture de deux feuilles, une chaîne d’ouvrières tend ou relâche le fil.",
          "texte_regle": {
            "face_1": "Après la production de ce Nid défendu, si la Plume montre Chaud, vous pouvez déplacer un Insecte d’un rang de la Réglette vers l’icône d’un Gardien en piste. Si elle montre Calme, vous pouvez rappeler un Insecte d’une icône sur la parcelle du Nid. Le Bouclier de lisière reste au choix des Insectes au verdict et un pari perdu le reste même si le Bouclier maintient le Gardien.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Coudre une assurance à un Gardien ou refaire la masse du Nid ?",
            "renoncement": "L’Insecte retiré du rang ne servira pas à une déviation."
          }
        },
        "temoins": [
          {
            "id": "M3_T1",
            "resume": "Le Colibri a laissé une ouvrière sur 5. Avec Plume Chaud, le Nid la place sur l’icône d’un Gardien menacé. Au verdict, I peut la dépenser pour maintenir sa Face 2 malgré le pari perdu.",
            "etat_attendu_verifie": {
              "entree": {
                "plume": "Chaud",
                "ouvrieres_rang": 1,
                "ouvrieres_icone": 0,
                "verdict": "perdu",
                "face": 2
              },
              "transition_python": "if s['plume']=='Chaud' and s['ouvrieres_rang']:\n    s['ouvrieres_rang']-=1\n    s['ouvrieres_icone']+=1\nmaintien=s['verdict']=='perdu' and s['ouvrieres_icone']>0\nif maintien:\n    s['ouvrieres_icone']-=1\nr=[s['verdict'],s['face'] if maintien else 1,s['ouvrieres_rang'],s['ouvrieres_icone']]",
              "attendu": [
                "perdu",
                2,
                0,
                0
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Utiliser Chaud pour protéger une Face 2 précieuse quand la déviation est passée. Rappeler sur Calme si le stock du Nid est sous deux.",
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
          "ENRACINEMENT",
          "AUTONOMIE_A0"
        ],
        "est_twist": false,
        "vecteurs": "NID_ACTIVE + INSECTE + TAMBOUR + ROUTE → INSECTES_EN_CONVOI / INSECTE_RANG",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE",
          "TAMBOUR",
          "ROUTE"
        ],
        "entrees_synergie": [],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "TAMBOUR",
          "ROUTE"
        ],
        "sorties": [
          "INSECTES_EN_CONVOI",
          "INSECTE_RANG"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "CONVOI"
        ],
        "tuile_plateau": {
          "nom_court": "Le Nid des calebasses",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_TAMBOUR",
            "PIC_INSECTE",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "Convoi vers le Tambour",
            "face_2": null,
            "enracine": "Essaimage"
          },
          "resume_plateau": "Convoi vers le Tambour / Essaimage"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid des calebasses",
          "entite_illustree": "Nid dans une courge sèche",
          "brief_illustration": "Une calebasse sèche entre les contreforts d’un grand arbre, parcourue par une colonne jusqu’à une peau de tambour.",
          "pitch_ambiance": "Quand le Tambour résonne, la courge vide vibre jusque dans les chambres où repose le couvain.",
          "texte_regle": {
            "face_1": "Après la production de ce Nid défendu, si le Tambour occupe une autre parcelle du même rayon, vous pouvez y conduire autant d’Insectes du Nid que vous le souhaitez. Le convoi suit le rayon, en sautant les Routes, avant la Migration.",
            "face_2": null,
            "enracine": "Quand vous enracinez ce Nid, laissez ses Insectes sur leur parcelle. Vous pouvez ensuite donner à un de ces Insectes au sol un pas radial vers le cœur, Routes sautées, ou le poser sur un rang librement choisi s’il est déjà sur la dernière parcelle."
          },
          "decision_et_renoncement": {
            "choix": "Combien d’ouvrières confier au Tambour ?",
            "renoncement": "Au-dessous de deux ouvrières restantes, la prochaine Production tombe à une."
          }
        },
        "temoins": [
          {
            "id": "M4_T1",
            "resume": "Quatre ouvrières après Production en H2. Deux gagnent le Tambour en H4 en sautant la Route H3. Deux restent au Nid et permettront une nouvelle ponte de deux.",
            "etat_attendu_verifie": {
              "entree": {
                "stock_apres_ponte": 4,
                "nid": 2,
                "tambour": 4,
                "routes": [
                  3
                ],
                "convoi": 2
              },
              "transition_python": "parcours=[p for p in range(s['nid']+1,s['tambour']+1) if p not in s['routes']]\nn=min(s['stock_apres_ponte'],s['convoi'])\nreste=s['stock_apres_ponte']-n\nr=[parcours,reste,n,2 if reste>=2 else 1]",
              "attendu": [
                [
                  4
                ],
                2,
                2,
                2
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Conserver deux ouvrières si la prochaine Production est plausible. Allonger le convoi si le Tambour protège la dernière parcelle.",
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "roles_portes": [
          "AUTONOMIE_A0"
        ],
        "est_twist": false,
        "vecteurs": "NID_ACTIVE + INSECTE + RANG_MACHINE + ANNULATION → INSECTE_RANG",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "ANNULATION"
        ],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "RANG_MACHINE",
          "ANNULATION"
        ],
        "sorties": [
          "INSECTE_RANG"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "REFLET"
        ],
        "tuile_plateau": {
          "nom_court": "Le Nid des reflets",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_RANG_MACHINE",
            "PIC_INSECTE",
            "PIC_ANNULATION"
          ],
          "mots_cles_plateau": {
            "face_1": "Reflet droit · reflet incliné",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Reflet droit · reflet incliné"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid des reflets",
          "entite_illustree": "Nid de papier au-dessus de l’eau noire",
          "brief_illustration": "Nid de papier fixé sous une branche au ras d’un bras mort. Deux colonnes se séparent à la surface réfléchissante.",
          "pitch_ambiance": "Sous le nid de papier, chaque remous porte deux images. Les ouvrières suivent celle qui tremble encore.",
          "texte_regle": {
            "face_1": "Après la production de ce Nid défendu, choisissez un jeton Machine révélé du rayon du Nid. Posez un Insecte du Nid sur le rang de son dé. Si le jeton est incliné par une annulation, vous pouvez choisir à la place un rang voisin de ce dé, entre 1 et 6. Gardez les jetons visibles avec leur orientation et leurs dés de machine jusqu’à cette lecture. Utilisez le rang après toute déviation. Un jeton de Ratissage sous sa machine ne donne pas de départ.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Lire la menace visible ou exploiter le reflet d’une machine annulée ?",
            "renoncement": "La cohorte investie dans la Réglette ne pare plus sur la parcelle du Nid."
          }
        },
        "temoins": [
          {
            "id": "M5_T1",
            "resume": "Le Rêve a incliné le jeton d’une machine déviée en 5. Après Production, le Nid choisit le rang 4 voisin. Cette ouvrière pourra payer la plongée des Lanternes en 4 à une prochaine ouverture.",
            "etat_attendu_verifie": {
              "entree": {
                "rang_apres_deviation": 5,
                "incline": true,
                "choix": 4,
                "stock_nid": 3
              },
              "transition_python": "d=s['rang_apres_deviation']\naccessibles={d}\nif s['incline']:\n    accessibles.update(p for p in (d-1,d+1) if 1<=p<=6)\ntransfert=s['choix'] in accessibles and s['stock_nid']>0\nr=[s['stock_nid']-int(transfert),s['choix'] if transfert else None]",
              "attendu": [
                2,
                4
              ]
            },
            "statut": "OK"
          }
        ],
        "heuristique_bot": "Chercher un rang qui prépare les Lanternes ou une déviation du prochain tour, tout en gardant si possible deux Insectes au Nid.",
        "engine_sync_status": "DESIGNED_V6_3",
        "statut_conception": "PASSE_1_CREATIF"
      }
    }
  },
  "panel_3": {
    "_meta": {
      "projet": "Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)",
      "schema_version": "6.3.1",
      "socle_verrouille": "6.2.0",
      "cadrage_source": "docs/cadrage_tuiles_v6_3.md",
      "etape_active": "ETAPE_2_CONCEPTION_CREATIVE",
      "statut_global": "CONCEPTION_EN_COURS",
      "genere_le": "2026-11-26",
      "slots_count": 30,
      "c02_supprime": true,
      "panel_id": "panel_3",
      "source_modele": "Modèle 3 — Candidat 3 (4 inchangés) + REPONSE_IA3 Lots A1/A2/A3/B (26 révisés + correctifs Red Team)",
      "murs_porteurs_verrouilles": [
        "M1_TEMPS_BATAILLE",
        "M2_CONSERVATION_THERMIQUE",
        "M3_INTEGRITE_PLATEAU_ET_ICONES",
        "M4_AUTONOMIE_PLANCHER_SOLO"
      ],
      "note_retrocompatibilite": "Panel candidat panel_3 compilé en v6.3.1 (4 murs porteurs M1..M4, séparation entrees_plancher / entrees_synergie, 32 pictogrammes officiels) pour arbitrage d'auteur de l'Étape 2b."
    },
    "carte_des_roles": {
      "statut": "PASSE_1_CREATIF_V6_3_1",
      "roles": {
        "catalyseurs_eveil": [
          "G1=M>R",
          "G4=O>M",
          "G5=R>O",
          "G7=M>H",
          "G9=R>H",
          "G10=R>E",
          "G11=O>H",
          "G12=O>E",
          "G13=M>I",
          "G14=R>I",
          "G15=O>I"
        ],
        "leviers_reve": [
          "R4=H>R",
          "R5=H>O",
          "R7=E>M",
          "R8=E>R",
          "R9=E>O",
          "R10=E>I"
        ],
        "synergies_enracinement": [
          "G3=M>O",
          "G15=O>I",
          "R3=H>M",
          "M4=I>H"
        ],
        "lois_passives": [
          "R2=E>H",
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
          "G6=O>R",
          "G8=M>E",
          "G9=R>H",
          "R5=H>O",
          "R10=E>I",
          "M1=I>M"
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
        "nombre": 11
      },
      "I05_couverture_sommeil": {
        "verdict": "OK",
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
      "synergies_optionnelles_couvertes": 68
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
        "vecteurs": "DUEL_TERRITOIRE_SURCHAUFFE_CROC_GLISSEMENT_PARI_EVEIL",
        "entrees_plancher": [
          "DUEL",
          "ROUGE",
          "GARDIEN"
        ],
        "entrees_synergie": [
          "DEFENSEUR_ATTENTE"
        ],
        "entrees": [
          "DUEL",
          "ROUGE",
          "GARDIEN",
          "DEFENSEUR_ATTENTE"
        ],
        "sorties": [
          "PARI_GLISSE",
          "BLEU",
          "CROC",
          "TERRITOIRE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Engager 2 Défenseurs sur G1 exige 2 Parades aux attaques (puisque G1 ne peut jamais faire glisser son propre second pari). La 1re Parade permet d'affaiblir la machine située sur la parcelle du Duel (1 Rouge → Bleu, abaissant son Seuil de Parade de 2 points en Assaut ou Ratissage), ce qui facilite la réussite de la 2nde Parade sur ce Duel : celui-ci bascule alors en Territoire tenu, fait glisser le 2nd pari de G1 dans sa seconde encoche et déclenche en Face 2 le double effet complet.",
        "tags": [
          "CATALYSEUR_EVEIL",
          "DUEL",
          "SURCHAUFFE_BLEUE",
          "CROC",
          "PARI_GLISSE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Jaguar",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_DUEL",
            "PIC_BLEU",
            "PIC_CROC",
            "PIC_PARI_ENCOCHE"
          ],
          "mots_cles_plateau": {
            "face_1": "1 🔴→🔵 (si 0 🔴 : 🦷) OU glisse 1 pari allié → ⭐ (repli : ♻️ → ⚔️/M)",
            "face_2": "1 🔴→🔵 (ou 🦷) · si Territoire tenu : ET glisse 1 pari allié → ⭐",
            "enracine": null
          },
          "resume_plateau": "Surchauffe féline ou pari sauvé"
        },
        "carte_joueur": {
          "titre_complet": "Le Jaguar, Souverain des Berges",
          "entite_illustree": "Le Jaguar entier bondissant sur la berge à l'orée de la forêt amazonienne",
          "brief_illustration": "Un grand jaguar amazonien entier bondissant hors de l'ombre d'un massif de racines vers un engin surchauffé, son rugissement faisant vibrer les totems des autres Gardiens.",
          "pitch_ambiance": "« Là où la forêt refuse de céder un pas, l'ombre tachetée bondit et réveille les anciens esprits. »",
          "texte_regle": {
            "face_1": "Lors d'une Parade sur la parcelle du Duel avec au moins 1 Défenseur, retournez d'abord le Duel sur Territoire tenu avant de résoudre Le Jaguar. À l'activation, choisissez l'un des deux effets :\n1. Bond Thermique : ciblez 1 machine du plateau et retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe ; si cette machine ne porte aucun Rouge, posez ou déplacez le pion Croc (depuis la réserve Reptile ou le plateau) sur sa parcelle.\n2. Rugissement d'Éveil : faites glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir) ; si aucun autre Gardien construit ne porte de Défenseur en pari, relevez à la place 1 Défenseur couché en attente (ou déplacez 1 Défenseur d'une parcelle non ciblée) sur la parcelle du Duel ou sur une parcelle ciblée du rayon Mammifère.",
            "face_2": "Résolvez Bond Thermique ou Rugissement d'Éveil (comme en Face 1). Si le jeton Duel est sur sa face Territoire tenu au moment de cette activation, résolvez les deux effets successivement (Bond Thermique puis Rugissement d'Éveil).",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Trancher en Face 1 (et en Face 2 tant que le Duel reste en Défi) entre neutraliser une menace physique immédiate (Rouge → Bleu ou Croc avant une attaque) et sécuriser le pari compromis d'un autre Gardien pour préserver l'Éveil de la Forêt.",
            "renoncement": "Sauver un pari allié par Rugissement d'Éveil renonce à l'appui de terrain immédiat tant que Territoire tenu n'est pas verrouillé en Face 2."
          }
        },
        "temoins": [
          {
            "id": "G1_T1",
            "resume": "Tour 4 (Acte 1, 4 joueurs), 4 Défenseurs engagés sur la Piste des Gardiens (2 sur G1 Face 2 Parade, 1 sur Piégeage, 1 sur Sabotage non déclenché à l'ouverture). Aux attaques, une Parade au rang 2 active G1 (Bond Thermique : Rouge → Bleu sur l'Abatteuse du rang 5, seuil 4 → 2). Au rang 5, la Parade sur la parcelle du Duel le bascule en Territoire tenu et déclenche la 2nde activation de G1 : pose du Croc + Rugissement d'Éveil qui fait glisser le pari du Gardien Sabotage dans son encoche libre → 0 pari perdu, Éveil.",
            "etat_attendu_verifie": {
              "abatteuse_seuil_reduit": 2,
              "pari_sabotage_glisse": true,
              "eveil_foret": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade. Utiliser Bond Thermique pour faire chuter le Seuil d'une attaque sur le Duel avant de déclencher Territoire tenu ; en Face 2, cumuler Bond Thermique et glissement de pari allié pour sécuriser l'Éveil.",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "CONSTRICTION_THERMIQUE_BLEU_RECUL_ECAILLE_CROC_DUEL",
        "entrees_plancher": [
          "ROUGE",
          "ECAILLE",
          "CROC"
        ],
        "entrees_synergie": [
          "DUEL",
          "TERRITOIRE"
        ],
        "entrees": [
          "ROUGE",
          "ECAILLE",
          "CROC",
          "DUEL",
          "TERRITOIRE"
        ],
        "sorties": [
          "BLEU",
          "ECAILLE",
          "CROC",
          "RECUL"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE",
          "ICONE_SABOTAGE"
        ],
        "double_ouverture": "Avec 2 Défenseurs engagés sur Piégeage et 2 Pièges déclenchés aux attaques, la 1re activation peut refroidir la machine postée sur le Duel (Rouge → Bleu) afin d'assurer sa Parade par M sur un rang intermédiaire ; une fois le Duel retourné sur Territoire tenu, la 2nde activation de G2 sur un Piège ultérieur déploie simultanément la double Constriction et Sillage d'Écaille (replaçant aussitôt le Croc sur une parcelle dont le Piège vient de céder).",
        "tags": [
          "SURCHAUFFE_BLEUE",
          "ECAILLE",
          "CROC",
          "DUEL"
        ],
        "tuile_plateau": {
          "nom_court": "L’Anaconda vert",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PIEGEAGE",
          "pictogrammes": [
            "PIC_ROUGE",
            "PIC_BLEU",
            "PIC_ECAILLE",
            "PIC_DUEL"
          ],
          "mots_cles_plateau": {
            "face_1": "1 🔴→🔵 (si 0 🔴 : ⏪ 1) OU +1 🦎 au sac + 🦷 hors ⚔️",
            "face_2": "Rayon ⚔️ = jusqu’à 2 🔴→🔵 · si Territoire tenu = Constriction ET 🦎/🦷",
            "enracine": null
          },
          "resume_plateau": "Constriction thermique et mue Reptile"
        },
        "carte_joueur": {
          "titre_complet": "L’Anaconda vert, Souffle Glacé de l’Igapó",
          "entite_illustree": "L’Anaconda vert entier enroulé dans l'eau noire d'un méandre amazonien",
          "brief_illustration": "Un immense anaconda vert entier émergeant d'un méandre d'eau noire, ses anneaux glacés enserrant une chenille d'acier fumante tandis qu'une mue d'écailles dérive dans le courant.",
          "pitch_ambiance": "« Sous l'eau noire du méandre, ses anneaux glacés étouffent la ferraille avant même qu'elle ne gronde. »",
          "texte_regle": {
            "face_1": "À l'activation, choisissez l'un des deux effets :\n1. Constriction : ciblez 1 machine du plateau et retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe ; si cette machine ne porte aucun Rouge et est mobile, faites-la reculer d'1 parcelle vers la bordure (en sautant toute Route Forestière).\n2. Sillage d'Écaille : versez 1 jeton Écaille de la réserve Reptile dans le sac opaque (s'il en reste en réserve) et posez ou déplacez le pion Croc sur toute parcelle autre que celle portant le Duel.",
            "face_2": "Résolvez Constriction ou Sillage d'Écaille (comme en Face 1), avec deux amplifications liées au Duel :\n• Si Constriction cible une machine située sur le rayon portant le Duel, retournez sur elle jusqu'à 2 jetons Rouge existants en Bleu Surchauffe (ou 1 Rouge → Bleu suivi d'un recul d'1 parcelle si elle n'avait qu'1 seul Rouge et est mobile).\n• Si le Duel est sur sa face Territoire tenu, résolvez Constriction ET Sillage d'Écaille lors de cette même activation.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Arbitrer entre le soulagement thermique immédiat d'une machine menaçante (Constriction) et l'enrichissement structurel du sac en Écailles assorti d'un Croc hors Duel (Sillage d'Écaille).",
            "renoncement": "Laisser la parcelle du Duel libre d'être parée par les Mammifères pour débloquer Territoire tenu plutôt que d'y poser le Croc."
          }
        },
        "temoins": [
          {
            "id": "G2_T1",
            "resume": "Tour 5 (Acte 2), G2 Face 2 sur Piégeage (1 pari). Sur M, le Bulldozer est paré au rang 1 (Duel → Territoire tenu) et l'Abatteuse (rang 3, 2 Rouges, seuil 4) attend. Au rang 2, un Piège sur R active G2 Face 2 : grâce à Territoire tenu, Constriction retourne les 2 Rouges de l'Abatteuse en 2 Bleus (seuil ramené au minimum 1) ET Sillage d'Écaille ajoute 1 Écaille au sac et pose le Croc en parcelle 2 de R.",
            "etat_attendu_verifie": {
              "rouges_retournes": 2,
              "seuil_abatteuse": 1,
              "ecaille_au_sac": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Piégeage. Refroidir les machines chargées en Rouges sur le rayon du Duel (jusqu'à 2 Rouges → Bleus en Face 2) et cumuler avec Sillage d'Écaille dès que Territoire tenu est actif.",
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
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "PERMUTATION_BINOME_MACHINES_RECUL_DUEL_ENRACINEMENT_CANOPEE",
        "entrees_plancher": [
          "ARBRE",
          "RANG_MACHINE",
          "PLUME"
        ],
        "entrees_synergie": [
          "DUEL",
          "ROUGE",
          "SOUCHE"
        ],
        "entrees": [
          "ARBRE",
          "RANG_MACHINE",
          "PLUME",
          "DUEL",
          "ROUGE",
          "SOUCHE"
        ],
        "sorties": [
          "RECUL",
          "DUEL",
          "BLEU",
          "ARBRE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Deux activations permettent soit de désorganiser successivement deux rayons menacés avant leurs frappes, soit sur un même rayon de faire reculer une machine mobile puis d'échanger le binôme pour renvoyer l'Abatteuse tout au bord de la forêt.",
        "tags": [
          "ENRACINEMENT",
          "PERMUTATION",
          "DUEL",
          "CANOPEE"
        ],
        "tuile_plateau": {
          "nom_court": "L’Atèle",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_ARBRE",
            "PIC_RECUL",
            "PIC_DUEL",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "Rayon M / O / 🪶 : permute les 2 machines mobiles OU ⏪ -1 (+ déplace ⚔️ sous 🌳)",
            "face_2": "Tout rayon : permute les 2 mobiles OU ⏪ -1 · Puis 🔴→🔵 (ou ⚔️ sur Territoire tenu)",
            "enracine": "Décompte final : +1 🪵→🌳 sur une autre parcelle (M ou O) si ≥ 2 parcelles gardent 🌳"
          },
          "resume_plateau": "Croise les machines sous les cimes"
        },
        "carte_joueur": {
          "titre_complet": "L’Atèle, Acrobate des Hautes Voûtes",
          "entite_illustree": "L’Atèle (Ateles paniscus) entier en plein balancier au sommet de la canopée",
          "brief_illustration": "L’Atèle (Ateles paniscus) entier en plein balancier au sommet de la canopée, suspendu par sa queue préhensile entre deux hautes couronnes tandis qu'en contrebas deux engins désorientés se croisent à contre-sens.",
          "pitch_ambiance": "« D'un bond de trente mètres dans les houppiers, il agite les branches à contre-courant : en bas, l'abatteuse retourne vers les souches et le bulldozer perd sa trace. »",
          "texte_regle": {
            "face_1": "Lorsque L’Atèle s’active, ciblez le rayon Mammifères, le rayon Oiseaux ou le rayon désigné par la Plume de Vigie (si la Plume désigne un rang 1–6, ciblez le rayon d’une machine présente sur ce rang). Choisissez l’une des deux feintes : échangez les parcelles des 2 machines mobiles de ce rayon si aucune des deux n’a encore résolu son activation à ce tour, ou faites reculer d’1 parcelle vers la bordure 1 machine mobile de ce rayon (en sautant toute Route Forestière). Ensuite, si le jeton Duel est sur ce rayon ou dans la réserve Mammifères, vous pouvez le poser ou le déplacer (en conservant sa face actuelle) sur une parcelle de ce rayon portant au moins 1 Arbre debout et au moins 1 Défenseur.",
            "face_2": "Lorsque L’Atèle s’active, ciblez n’importe quel rayon du plateau : échangez les parcelles de ses 2 machines mobiles non encore résolues à ce tour, ou faites reculer d’1 parcelle vers la bordure 1 machine mobile de ce rayon. De plus, appliquez un effet au choix sur ce rayon : retournez 1 jeton Rouge existant en Bleu Surchauffe sur l’une de ses machines, ou posez ou déplacez le jeton Duel directement sur sa face Territoire tenu auprès d’un Défenseur présent sur une parcelle de ce rayon portant au moins 1 Arbre debout.",
            "enracine": "Au décompte final, en plus de sa régénération normale d’Enracinement sur sa parcelle (1 Souche en Face 1, ou 2 Souches en Face 2), retournez 1 Souche supplémentaire en Arbre debout sur une autre parcelle non-Route de votre rayon ou du rayon Oiseaux voisin si au moins 2 parcelles de votre rayon portent encore chacune au moins 1 Arbre debout."
          },
          "decision_et_renoncement": {
            "choix": "Désynchroniser le binôme adverse en renvoyant l'Abatteuse frapper à blanc sur une clairière de Souches pendant que le Bulldozer est déporté sur une parcelle boisée, ou conserver L'Atèle jusqu'en fin de partie avant de l'enraciner pour jusqu'à 3 Arbres au décompte final.",
            "renoncement": "Échanger les deux machines sauve une clairière de Souches contre le Bulldozer, mais rapproche ce Bulldozer du cœur du rayon pour les tours suivants s'il n'est pas contenu par le Duel."
          }
        },
        "temoins": [
          {
            "id": "G3_T1",
            "resume": "Sur le rayon Oiseaux marqué par la Plume, parcelle 2 ne porte que 2 Souches sous le Bulldozer (rang 4) tandis que l'Abatteuse est en parcelle 3 (3 Arbres, rang 2). À l'ouverture sur un Sabotage, L'Atèle (Face 1) échange leurs positions : l'Abatteuse frappe parcelle 2 à blanc (0 Arbre coupé) et le Bulldozer frappe parcelle 3 boisée sans pouvoir créer de Route.",
            "etat_attendu_verifie": {
              "machines_permutees": true,
              "route_evitee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Permuter Abatteuse et Bulldozer dès qu'un Bulldozer menace une clairière de Souches ; sinon reculer la machine la plus avancée ; enraciner Face 2 en fin de partie si ≥ 2 parcelles M gardent des Arbres debout.",
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
        "vecteurs": "RALLIEMENT_DEFENSEURS_PLUME_CHAUD_CALME_DUEL_TENU",
        "entrees_plancher": [
          "PLUME",
          "DEFENSEUR_ATTENTE"
        ],
        "entrees_synergie": [
          "DUEL",
          "ROUGE"
        ],
        "entrees": [
          "PLUME",
          "DEFENSEUR_ATTENTE",
          "DUEL",
          "ROUGE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "TERRITOIRE",
          "BLEU"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Placé sur Parade, L'Ara rouge transforme une première Parade aux rangs bas en réaction en chaîne : il relève un bâtisseur couché pour atteindre le Seuil de Parade d'un rang suivant, ce qui rallume Parade et déclenche sa seconde activation (jusqu'à 4 Défenseurs mobilisés en Face 2 sur un seul tour).",
        "tags": [
          "CATALYSEUR_EVEIL",
          "REDEPLOIEMENT",
          "PLUME",
          "DUEL"
        ],
        "tuile_plateau": {
          "nom_court": "L’Ara rouge",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_DEFENSEUR_ATTENTE",
            "PIC_DEFENSEUR",
            "PIC_DUEL"
          ],
          "mots_cles_plateau": {
            "face_1": "🪶 Chaud : 1 ♻️ (ou 🛡️ non ciblé) → parcelle ciblée · 🪶 Calme : 1 🛡️ → parcelle ciblée + ⚔️ Tenu (si ≥ 2 🛡️)",
            "face_2": "Jusqu’à 2 (♻️ ou 🛡️ non ciblés) → parcelles ciblées · Sur ⚔️/🪶 : ⚔️ Tenu OU 🔴→🔵",
            "enracine": null
          },
          "resume_plateau": "Rallie la garde au cri d’alerte"
        },
        "carte_joueur": {
          "titre_complet": "L’Ara rouge, Vigie Écarlate de la Collpa",
          "entite_illustree": "Un couple d’Aras rouges (Ara macao) entiers prenant leur envol devant une falaise d’argile",
          "brief_illustration": "Un couple d’Aras rouges (Ara macao) entiers prenant leur envol toutes ailes déployées devant une falaise d’argile ocre (collpa), donnant l’alerte aux mammifères rassemblés en lisière.",
          "pitch_ambiance": "« Quand le couple écarlate décolle de la falaise d’argile, son cri porte si loin que la forêt entière a déjà refermé ses rangs avant l’arrivée des chenilles. »",
          "texte_regle": {
            "face_1": "Lorsque L’Ara rouge s’active, observez la face de la Plume de Vigie et ciblez le rayon qu’elle désigne, le rayon d’une machine située sur son rang, ou le rayon portant le jeton Duel (à défaut, le rayon Oiseaux ou Mammifères) :\n• Si la Plume affiche Chaud (ou n’est pas posée) : prenez 1 Défenseur couché en attente (bâtisseur en lisière ou pion couché en Furtivité, de n’importe quel joueur) — ou, s’il n’en existe aucun, 1 Défenseur debout sur une parcelle non ciblée — et placez-le debout (face Définitif) sur une parcelle ciblée de ce rayon.\n• Si la Plume affiche Calme : déplacez 1 Défenseur debout d’une parcelle non ciblée (ou relevez 1 Défenseur couché en attente) vers une parcelle ciblée de ce rayon ; si cette parcelle d’arrivée porte le jeton Duel face Défi et réunit désormais au moins 2 Défenseurs, retournez immédiatement le Duel sur Territoire tenu.",
            "face_2": "Lorsque L’Ara rouge s’active, mobilisez en couple jusqu’à 2 Défenseurs (chacun relevé parmi les Défenseurs couchés en attente ou déplacé depuis une parcelle non ciblée) et placez-les debout sur une ou deux parcelles ciblées de n’importe quels rayons. De plus, si au moins l’un d’eux rejoint la parcelle du jeton Duel ou le rayon désigné par la Plume de Vigie, choisissez 1 bonus : retournez immédiatement le jeton Duel (s’il est accompagné d’au moins 1 Défenseur) sur Territoire tenu, ou retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine visant cette parcelle.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Orienter sous paravent la Plume sur Chaud pour recycler un bâtisseur couché lors d'un tour de construction, ou sur Calme pour verrouiller immédiatement Territoire tenu avant l'avancée des rangs 3 ou 6.",
            "renoncement": "Engager ses Défenseurs du second déploiement en pari sur les Gardiens pour viser l'Éveil dégarnit la forêt au départ et rend la table tributaire du ralliement de L'Ara."
          }
        },
        "temoins": [
          {
            "id": "G4_T1",
            "resume": "Deux alliés ont construit un Gardien à l'ouverture (2 bâtisseurs couchés) et la Plume est Chaud au pied du rayon M où parcelle 3 (Seuil 3) porte le Duel et 2 Défenseurs. Une Parade au rang 1 active L'Ara rouge Face 1 : il relève 1 bâtisseur en parcelle 3 (garde à 3). Au rang 3, la frappe est parée, le Duel passe Territoire tenu et Parade rallume la 2nde activation de L'Ara.",
            "etat_attendu_verifie": {
              "defenseur_releve_m3": true,
              "territoire_tenu": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade. Relever prioritairement les bâtisseurs couchés vers la parcelle du Duel ou la parcelle au déficit de Seuil exactement égal à 1 (ou 2 en Face 2) pour chaîner les Parades.",
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
        "vecteurs": "RELAIS_DEFENSEUR_PLUME_PARI_GLISSE_BAIN_SOLAIRE_ECAILLE_PERCHOIR",
        "entrees_plancher": [
          "ROUGE",
          "ECAILLE",
          "PLUME"
        ],
        "entrees_synergie": [
          "DEFENSEUR_ATTENTE",
          "PERCHOIR",
          "GARDIEN"
        ],
        "entrees": [
          "ROUGE",
          "ECAILLE",
          "PLUME",
          "DEFENSEUR_ATTENTE",
          "PERCHOIR",
          "GARDIEN"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "PARI_GLISSE",
          "ECAILLE",
          "BLEU",
          "CROC"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE",
          "ICONE_SABOTAGE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Engager 2 Défenseurs sur G5 conserve intacts les engagements visuels de ses encoches tout en projetant des renforts : la 1re activation relève un Défenseur couché en attente (ou déplace un Défenseur d'une parcelle non ciblée) sur une parcelle menacée d'un rang ultérieur, aidant à réussir la 2nde Parade qui fait glisser le 2nd pari de G5 dans sa seconde encoche et double la production d'Écailles et de conversions Rouge → Bleu.",
        "tags": [
          "CATALYSEUR_EVEIL",
          "PLUME",
          "PERCHOIR",
          "ECAILLE",
          "SURCHAUFFE_BLEUE"
        ],
        "tuile_plateau": {
          "nom_court": "L’Iguane vert",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_DEFENSEUR",
            "PIC_PLUME",
            "PIC_ECAILLE",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "1 ♻️/🛡️ non ciblé → forêt (sur 🪶 : +1 pari allié → ⭐) + [🔴→🔵/⏪/🦷 OU +1 🦎 & révéler 🦅]",
            "face_2": "Idem + 🪶 Chaud/Machine 🦅 = les 2 · 🪶 Calme/💥🦎 🦅 = +1 pari allié → ⭐",
            "enracine": null
          },
          "resume_plateau": "Défenseur redéployé et canopée refroidie"
        },
        "carte_joueur": {
          "titre_complet": "L’Iguane vert, Guetteur Solaire des Cimes",
          "entite_illustree": "L’Iguane vert entier immobile à la cime baignée de soleil face au perchoir de vigie",
          "brief_illustration": "Un grand iguane vert entier à la crête dorée, posté sur la plus haute branche baignée de lumière, reflétant la chaleur du métal vers un perchoir d'oiseau de vigie.",
          "pitch_ambiance": "« Immobile à la cime baignée de soleil, il boit la fièvre de l'acier et guide le vol des sentinelles. »",
          "texte_regle": {
            "face_1": "À l'activation (son Défenseur en pari glissant normalement dans son encoche), résolvez successivement :\n1. Relais d'Éveil : relevez 1 Défenseur couché en attente (bâtisseur en lisière ou pion de rive couché) — ou déplacez 1 Défenseur debout depuis une parcelle non ciblée — vers une parcelle de forêt de votre choix (où il participe aux Parades restantes). S'il rejoint le rayon ou une parcelle visée par le rang marqué par la Plume de Vigie (ou si aucun Défenseur n'est disponible à redéployer), faites en outre glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir).\n2. Bain Solaire — choisissez l'une des deux actions :\n• Insolation : retournez 1 jeton Rouge existant en Bleu Surchauffe sur 1 machine du plateau ; si cette machine n'a aucun Rouge, reculez-la d'1 parcelle vers la bordure (si mobile) ou posez/déplacez le Croc sur sa parcelle.\n• Mue de Vigie : versez 1 jeton Écaille de la réserve Reptile dans le sac opaque (s'il n'en reste plus, posez ou déplacez le Croc sur toute parcelle) ; si le Perchoir de Vigie porte un jeton face cachée, vous pouvez le révéler sur le Perchoir (et poser/déplacer le Croc si c'est une Écaille).",
            "face_2": "Résolvez Relais d'Éveil puis Bain Solaire (comme en Face 1), enrichis par l'état public de la Vigie d'Oiseau :\n• Si la Plume de Vigie affiche Chaud ou si une Machine est visible sur le Perchoir, résolvez les deux actions de Bain Solaire (Insolation ET Mue de Vigie).\n• Si la Plume de Vigie affiche Calme ou si un Sabotage ou une Écaille est visible sur le Perchoir, faites en outre glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir).",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Orienter au déploiement la Plume sur Chaud pour cumuler Insolation et Mue de Vigie, ou sur Calme pour sécuriser un pari Gardien allié ; choisir à l'activation où projeter le Défenseur relevé (colmater une parcelle critique ou suivre la Plume).",
            "renoncement": "Sans Machine visible sur le Perchoir, la Plume ne peut pas offrir à la fois le double Bain Solaire (Chaud) et le glissement de pari bonus (Calme)."
          }
        },
        "temoins": [
          {
            "id": "G5_T1",
            "resume": "Tour 3 (Acte 1), G5 Face 2 sur Parade (1 pari), Plume Calme au pied du rayon R, Machine visible sur le Perchoir (via G6), 1 bâtisseur couché en attente et 1 pari en attente sur un Gardien Rêve. Aux attaques, une Parade au rang 1 active G5 (son parieur glisse dans son encoche) : Relais d'Éveil relève le bâtisseur en parcelle 3 de R (rayon Plume), la Machine sur le Perchoir cumule Insolation (Rouge → Bleu sur l'Abatteuse de R, seuil 4 → 2) + Mue de Vigie (+1 Écaille au sac), et Plume Calme fait glisser le pari du Gardien Rêve dans son encoche libre.",
            "etat_attendu_verifie": {
              "defenseur_releve_r3": true,
              "ecaille_au_sac": 1,
              "pari_reve_glisse": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade. Relever les bâtisseurs couchés vers le rayon de la Plume pour sécuriser les Parades et glisser les paris alliés ; coordonner avec G6 pour garder une Machine sur le Perchoir tout en gardant la Plume Calme en Face 2.",
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
        "roles_portes": [
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "CONTREBANDE_PERCHOIR_ECHANGE_MACHINE_PIQUE_THERMIQUE",
        "entrees_plancher": [
          "PERCHOIR",
          "ROUGE",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "SABOTAGE",
          "ECAILLE"
        ],
        "entrees": [
          "PERCHOIR",
          "ROUGE",
          "RANG_MACHINE",
          "SABOTAGE",
          "ECAILLE"
        ],
        "sorties": [
          "ANNULATION",
          "BLEU",
          "PIEGE",
          "RECUL"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Les deux activations en Face 2 s'enchaînent naturellement l'une dans l'autre : lors de la 1re activation, Échange de Vigie extrait un Sabotage ou une Écaille du Perchoir et y enferme une Machine active ; lors de la 2nde activation dans le même tour, puisque cette Machine occupe désormais le Perchoir, Piqué Thermique est automatiquement survolté et refroidit (Rouge → Bleu), recule ou piège 2 autres machines distinctes sur le plateau.",
        "tags": [
          "TWIST_2K3",
          "PERCHOIR",
          "ECHANGE_VIGIE",
          "SURCHAUFFE_BLEUE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Toucan toco",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_PERCHOIR",
            "PIC_TWIST",
            "PIC_BLEU",
            "PIC_CROC"
          ],
          "mots_cles_plateau": {
            "face_1": "Révéler 🦅 + 1 🔴→🔵 (si 0 🔴 : ⏪ 1 ou 🪤) · + 🪤 si 💥 · + 🦷 si 🦎",
            "face_2": "Révéler 🦅 : échanger 💥/🦎 contre 1 Machine active (+ 🦷 si 🦎) OU Piqué (x2 si Machine sur 🦅)",
            "enracine": null
          },
          "resume_plateau": "Échange de machine via Perchoir"
        },
        "carte_joueur": {
          "titre_complet": "Le Toucan toco, Contrebandier du Kapokier",
          "entite_illustree": "Le Toucan toco entier au sommet d'un kapokier face au Perchoir de Vigie",
          "brief_illustration": "Un toucan toco entier au grand bec orangé perché à la cime d'un kapokier géant, escamotant un jeton d'acier dans le feuillage tandis qu'une écaille tombe vers la forêt.",
          "pitch_ambiance": "« D'un claquement de bec au sommet du kapokier, il escamote la menace dans les feuillages avant que la piste ne s'ouvre. »",
          "texte_regle": {
            "face_1": "S'il y a un jeton face cachée sur le Perchoir de Vigie, révélez-le (il y reste face visible). Ciblez ensuite 1 machine du plateau : retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe — ou, si cette machine ne porte aucun Rouge, au choix reculez-la d'1 parcelle vers la bordure (si mobile) ou posez 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire de son rayon.\nBonus de Perchoir : si le jeton visible sur le Perchoir est un Sabotage, posez en plus 1 Piège ordinaire sur toute parcelle dépourvue de Piège ordinaire ; s'il s'agit d'une Écaille, posez ou déplacez en plus le pion Croc sur toute parcelle. (Si le Perchoir est vide ou montre une Machine, seul l'effet de base s'applique.)",
            "face_2": "S'il y a un jeton face cachée sur le Perchoir de Vigie, révélez-le, puis choisissez l'un des deux modes :\n1. Échange de Vigie (uniquement si le Perchoir porte un Sabotage ou une Écaille) : échangez ce jeton avec 1 jeton Machine actif non annulé (n'ayant pas encore agi ce tour) situé devant n'importe quel rayon. Cette Machine est placée face visible sur le Perchoir : elle libère son dé de rang, n'agit pas ce tour et, si l'échange a lieu avant la Furtivité, ne compte plus dans m(r) lors de la Furtivité. Le Sabotage ou l'Écaille prend sa place devant ce rayon sans relancer de balayage Gardiens ; si c'est une Écaille, posez ou déplacez en plus le Croc sur toute parcelle.\n2. Piqué Thermique (toujours disponible, quel que soit l'état du Perchoir) : appliquez l'effet de base de la Face 1 (1 Rouge → Bleu, ou à défaut de Rouge sur la machine : Recul d'1 parcelle si mobile ou 1 Piège ordinaire sur son rayon) ; si une Machine est visible sur le Perchoir, appliquez cet effet de base sur jusqu'à 2 machines distinctes.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Inverser dès la pioche le choix habituel d'Oiseau : garder la Machine sous son paravent et cacher un Sabotage ou une Écaille sur le Perchoir pour capturer en Face 2 la pire Machine révélée sur toute la table.",
            "renoncement": "Cacher un Sabotage ou une Écaille sur le Perchoir renonce à son déclenchement immédiat à l'ouverture au profit de l'échange ciblé."
          }
        },
        "temoins": [
          {
            "id": "G6_T1",
            "resume": "Tour 3 (Acte 1), O garde sa Machine et cache 1 Écaille sur le Perchoir ; G6 Face 2 sur Sabotage (2 paris), 2 Défenseurs sur la Rive Sabotage de R. À l'ouverture, 1er Sabotage → Échange de Vigie capture la Machine de R sur le Perchoir et pose le Croc en parcelle 2 d'O ; 2nd Sabotage → Piqué Thermique survolté (x2) recule l'Abatteuse d'O et refroidit un Bulldozer. À la Furtivité, m(R)=0 gagne la Rive Sabotage.",
            "etat_attendu_verifie": {
              "machine_perchee": true,
              "pique_x2": true,
              "furtivite_r_zero": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Sabotage. En Face 2, stocker un Sabotage ou une Écaille sur le Perchoir pour escamoter la Machine la plus menaçante avant la Furtivité, puis exploiter la Machine perchée pour doubler Piqué Thermique et alimenter G5.",
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
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": false,
        "vecteurs": "RELAIS_DUEL_TERRITOIRE_SURCHAUFFE_RECUL_ACCORD_TAMBOUR_REVE",
        "entrees_plancher": [
          "ROUGE",
          "DUEL",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "POSITION_REVE"
        ],
        "entrees": [
          "ROUGE",
          "DUEL",
          "TAMBOUR",
          "CHANT",
          "POSITION_REVE"
        ],
        "sorties": [
          "BLEU",
          "RECUL",
          "TERRITOIRE",
          "RANG_REVE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE"
        ],
        "double_ouverture": "Engager 2 Défenseurs sur G7 crée un effet domino naturel sur l'icône Parade : une première Parade facile en début d'attaques déclenche la 1re activation de G7, qui abaisse le Seuil d'une machine d'un rang ultérieur (Rouge → Bleu et/ou Recul) tout en relayant le Duel sur sa parcelle pour bloquer l'avancée +1 ; cette seconde parcelle réussit alors sa Parade et rallume Parade pour le 2nd pari de G7.",
        "tags": [
          "CATALYSEUR_EVEIL",
          "DUEL",
          "SURCHAUFFE_BLEUE",
          "RECUL",
          "TAMBOUR"
        ],
        "tuile_plateau": {
          "nom_court": "Le Tapir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_BLEU",
            "PIC_RECUL",
            "PIC_DUEL",
            "PIC_TAMBOUR"
          ],
          "mots_cles_plateau": {
            "face_1": "1x [🔴→🔵 ou ⏪ 1] + relayer ⚔️ (🥁/🎶 : 🌙 ←1)",
            "face_2": "2x [🔴→🔵 et/ou ⏪ 1] + relayer ⚔️ (🥁/🎶 : 2 🌙 ←1)",
            "enracine": null
          },
          "resume_plateau": "Refroidir ou reculer, déplacer Duel"
        },
        "carte_joueur": {
          "titre_complet": "Le Tapir, Ouvreur des Sentiers Profonds",
          "entite_illustree": "Le Tapir terrestre entier fendant les broussailles vers la lisière",
          "brief_illustration": "Un grand tapir amazonien entier fendant les fourrés humides d'un pas massif, traçant un passage vers une clairière où résonne un tambour chamanique.",
          "pitch_ambiance": "« Lourd comme le tonnerre sourd du tambour, il fend les broussailles pour porter le défi là où la lisière vacille. »",
          "texte_regle": {
            "face_1": "À l'activation de ce Gardien, sur 1 machine au choix, retournez 1 jeton Rouge existant en Bleu Surchauffe OU reculez-la d'1 parcelle vers la bordure si elle est mobile (en sautant radialement toute Route Forestière). Vous pouvez ensuite déplacer le jeton Duel (face Territoire tenu) vers une autre parcelle ayant au moins 1 Défenseur.\nAccord M>H : si le Duel se trouve alors sur le rayon du Tambour, ou si la machine ciblée est sur le rang du Chant, glissez 1 Rêve d'1 rang libre à gauche.",
            "face_2": "À l'activation de ce Gardien, appliquez deux fois l'effet physique sur 1 ou 2 machines (retourner 1 jeton Rouge existant en Bleu Surchauffe et/ou reculer d'1 parcelle une machine mobile). Vous pouvez ensuite déplacer le jeton Duel (face Territoire tenu) vers une autre parcelle ayant au moins 1 Défenseur.\nAccord M>H : si le Duel occupe le rayon du Tambour ou si au moins une machine ciblée est sur le rang du Chant, glissez jusqu'à 2 Rêves d'1 rang libre à gauche (ou un même Rêve de 2 rangs libres à gauche).",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Refroidir (Rouge → Bleu) une machine chaude pour abaisser durablement son Seuil dans tous les modes, ou reculer une machine mobile loin d'une parcelle gravée 3 / du Ratissage ; relayer le Duel sur le rayon du Tambour pour faire glisser un Rêve.",
            "renoncement": "Déraciner le Duel de sa parcelle initiale expose celle-ci à une seconde machine plus tardive."
          }
        },
        "temoins": [
          {
            "id": "G7_T1",
            "resume": "Tour 3 (Acte 1, 4 joueurs), G7 Face 1 sur Parade (2 paris). Au rang 3, Parade sur M (Duel bloque l'avancée) → 1re activation de G7 : retourne le Rouge du Bulldozer de H (rang 6) en Bleu, relaie le Duel (Territoire tenu) en parcelle 3 de H (rayon du Tambour) et glisse un Rêve du rang 4 au rang 3. Au rang 6, seuil du Bulldozer réduit de 3 à 1 → Parade réussie, 2nde activation de G7 qui le recule en parcelle 2 et passage Face 2.",
            "etat_attendu_verifie": {
              "bulldozer_seuil": 1,
              "reve_rang": 3,
              "face_2": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade avec 2 paris. Enchaîner le refroidissement ou recul d'une cible tardive avec le relais du Duel vers le rayon du Tambour pour verrouiller la 2nde Parade et avancer un Rêve.",
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
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "CHENAL_SOUCHES_GLISSIERE_RECUL_ALTERATION_SURCHAUFFE_DUEL",
        "entrees_plancher": [
          "SOUCHE",
          "RANG_MACHINE",
          "DUEL"
        ],
        "entrees_synergie": [
          "ALTERATION",
          "ROUGE"
        ],
        "entrees": [
          "SOUCHE",
          "RANG_MACHINE",
          "DUEL",
          "ALTERATION",
          "ROUGE"
        ],
        "sorties": [
          "RECUL",
          "ALTERATION",
          "BLEU",
          "TERRITOIRE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PARADE",
          "ICONE_REVE"
        ],
        "double_ouverture": "Lors d'une double mise gagnante (ex. 2 parades dans le tour sur Parade), Le Boto refoule et altère deux machines distinctes — ou s'acharne deux fois sur la même machine mobile : la 1re activation la renvoie en bordure et l'altère, la 2nde convertit l'un de ses jetons Rouges en Bleu Surchauffe et y verrouille le Territoire tenu.",
        "tags": [
          "TWIST_2K3",
          "CHENAL_SOUCHES",
          "RECUL",
          "ALTERATION"
        ],
        "tuile_plateau": {
          "nom_court": "Le Boto",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_RECUL",
            "PIC_ALTERATION",
            "PIC_BLEU",
            "PIC_DUEL"
          ],
          "mots_cles_plateau": {
            "face_1": "Recul 1 + Chenal Souches + 🌀 / 🔴→🔵",
            "face_2": "Toute mobile + 🌀 / 🔴→🔵 + Chenal + ⚔️ Tenu",
            "enracine": "Standard (1 ou 2 Souches finales)"
          },
          "resume_plateau": "Refoule par les souches et altère"
        },
        "carte_joueur": {
          "titre_complet": "Le Boto, Enchanteur des Eaux Roses",
          "entite_illustree": "Grand dauphin rose d'Amazonie entier émergeant d'un bras d'eau noire noyant une clairière de souches",
          "brief_illustration": "Un grand dauphin rose d'Amazonie entier émerge à mi-corps d'un bras d'eau noire noyant une clairière de souches moussues, soulevant dans son sillage des tourbillons irisés qui repoussent une abatteuse vers la lisière.",
          "pitch_ambiance": "« Dans le brouillard du fleuve en crue, chaque souche coupée devient un tourbillon qui ramène le fer à son point de départ. »",
          "texte_regle": {
            "face_1": "Lorsque Le Boto s'active, choisissez 1 machine mobile située sur le rayon Mammifère, sur le rayon Entités, sur le rayon portant le jeton Duel, ou portant déjà un jeton d'Altération :\n1. Chenal des Souches : faites reculer cette machine d'1 parcelle vers la bordure de son rayon ; puis, tant que la parcelle où elle se trouve ou la parcelle suivante vers la bordure contient au moins 1 Souche, continuez de la faire glisser vers la bordure à travers toutes ces parcelles consécutives à Souches (en sautant les Routes Forestières, sans dépasser la 1re parcelle du rayon). Tout jeton d'Altération déjà présent sur elle y demeure attaché.\n2. Brume Rose : si cette machine ne porte pas encore de jeton d'Altération — et qu'elle a traversé ou rejoint au moins 1 Souche (ou le jeton Duel), ou qu'elle était déjà sur la 1re parcelle — posez sur elle 1 jeton d'Altération de la réserve Entités. Si elle portait déjà un jeton d'Altération au début de cette activation et possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.",
            "face_2": "Lorsque Le Boto s'active, choisissez n'importe quelle machine mobile du plateau :\n1. Si elle ne porte pas encore de jeton d'Altération, posez d'abord sur elle 1 jeton d'Altération de la réserve Entités ; si elle en portait déjà un et possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe. Faites-la ensuite reculer le long du Chenal des Souches comme en Face 1.\n2. Mirage du Détroit : vous pouvez déplacer immédiatement le jeton Duel (depuis la réserve Mammifère ou depuis sa parcelle actuelle) sur la parcelle d'arrivée de cette machine, directement tourné sur sa face Territoire tenu. Si le jeton Duel s'y trouvait déjà sur Territoire tenu, retournez 1 jeton Rouge d'une machine de ce rayon (mobile ou en Ratissage) sur sa face Bleue Surchauffe.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Exploiter une chaîne de Souches derrière le front comme toboggan de refoulement jusqu'à la bordure tout en altérant la machine ; en Face 2, verrouiller Territoire tenu sur la bordure rejointe.",
            "renoncement": "Laisser des Souches intactes expose ces parcelles à un Bulldozer non neutralisé ; déplacer le Duel en Face 2 dégarnit le barrage précédemment tenu."
          }
        },
        "temoins": [
          {
            "id": "G8_T1",
            "resume": "Tour 4, sur le rayon Entités, les parcelles 1, 2 et 3 portent chacune 1 Souche et l'Abatteuse est en parcelle 4 (1 Rouge, 0 Altération). Sur Parade, Le Boto Face 1 la recule en 3 (Souche) puis la fait glisser d'un trait à travers 2 jusqu'en parcelle 1 et pose sur elle 1 jeton d'Altération.",
            "etat_attendu_verifie": {
              "abatteuse_parcelle": 1,
              "alteration_posee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade (ou Rêve). Refouler en priorité une Abatteuse ou un Bulldozer mobile engagé loin derrière des Souches consécutives pour le ramener en parcelle 1 avec une Altération.",
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
          "TWIST_2K3",
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": true,
        "vecteurs": "LA_HAPPE_PIOCHE_SAC_FURTIVITE_ECAILLE_CROC_ACCORD_CHAMANE",
        "entrees_plancher": [
          "ECAILLE",
          "CROC",
          "SABOTAGE",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "ROUGE",
          "POSITION_REVE"
        ],
        "entrees": [
          "ECAILLE",
          "CROC",
          "SABOTAGE",
          "TAMBOUR",
          "CHANT",
          "ROUGE",
          "POSITION_REVE"
        ],
        "sorties": [
          "ECAILLE",
          "CROC",
          "MOBILISATION",
          "BLEU",
          "RANG_REVE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Sur l'icône Sabotage, engager 2 Défenseurs sur G9 catalyse directement l'Éveil de la Forêt même lorsqu'un seul joueur détient un Sabotage ou une Écaille sous son paravent : la 1re activation injecte d'abord une Écaille au sac puis déclenche La Happe ; tout Sabotage ou Écaille pêché dans le sac rallume aussitôt Sabotage, faisant glisser en chaîne le 2nd pari de G9 tout en posant deux fois le Croc et en sculptant m(r) avant la Furtivité.",
        "tags": [
          "TWIST_2K3",
          "CATALYSEUR_EVEIL",
          "ECAILLE",
          "CROC",
          "LA_HAPPE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Caïman noir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_TWIST",
            "PIC_ECAILLE",
            "PIC_CROC",
            "PIC_SABOTAGE"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🦎 au sac + 🦷 + Happe 1 jeton du sac (💥/🦎=résoudre · Machine=sac ou inclinée m(r)+1)",
            "face_2": "+1 🦎 au sac + 🦷 + Happe 2 jetons du sac + Accord 🥁/🎶 (🔴→🔵 + 🌙 ←1)",
            "enracine": null
          },
          "resume_plateau": "Piocher au sac, tordre Furtivité"
        },
        "carte_joueur": {
          "titre_complet": "Le Caïman noir, Maître des Eaux Noires",
          "entite_illustree": "Le Caïman noir entier jaillissant sous le miroir d'encre du fleuve",
          "brief_illustration": "Un immense caïman noir entier à fleur d'eau dans un bras sombre du fleuve, ses mâchoires émergeant d'un éclat d'écailles pour happer un jeton métallique avant l'assaut.",
          "pitch_ambiance": "« Sous le miroir d'encre du fleuve, seul l'éclair d'une écaille trahit la mâchoire qui happe l'intrus avant l'assaut. »",
          "texte_regle": {
            "face_1": "À l'activation de ce Gardien, ajoutez 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu) et posez ou déplacez le pion Croc sur une parcelle alliée.\nTwist 2K3 — La Happe : piochez ensuite 1 jeton au hasard dans le Sac opaque :\n• Sabotage ou Écaille : résolvez-le immédiatement comme un jeton révélé à l'ouverture (effet du Sabotage ou pose/repositionnement du Croc, allumage de l'icône Sabotage et nouveau balayage des Gardiens ; il suit ensuite le ménage normal).\n• Machine (du rayon r) : au choix, remettez-la dans le Sac opaque, OU échouez-la inclinée à 90° sans dé au pied de son rayon r (neutralisée sans rang, elle n'agit pas aux attaques, mais compte comme visible et inclinée pour +1 dans m(r) à la Furtivité avant de rentrer au sac au ménage).\nAccord R>H : si le Croc occupe le rayon du Tambour OU si le Chant occupe un rang ayant au moins 1 machine annulée ou aucune machine active, retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine (ou glissez 1 Rêve d'1 rang libre à gauche si aucun Rouge n'est présent).",
            "face_2": "À l'activation de ce Gardien, ajoutez 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu) et posez ou déplacez le pion Croc sur une parcelle alliée.\nDouble Happe : piochez jusqu'à 2 jetons dans le Sac opaque et appliquez à chacun d'eux (dans l'ordre de votre choix) les règles de La Happe (Sabotage ou Écaille résolu immédiatement avec allumage de Sabotage et balayage Gardiens ; Machine remise au sac ou posée inclinée à 90° sans dé au pied de son rayon pour +1 à m(r) sans action).\nAccord R>H : avec le Croc sur le rayon du Tambour ou le Chant sur un rang sans machine active restante, retournez jusqu'à 1 jeton Rouge existant en Bleu Surchauffe ET glissez 1 Rêve d'1 rang libre à gauche.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Lorsqu'une Machine surgit de La Happe, l'échouer inclinée pour monter m(r) de 1 à 2 et remporter la Rive Piège gratuitement, ou la rejeter dans le Sac opaque ; placer le Croc sur le rayon du Tambour pour déclencher l'accord chamanique.",
            "renoncement": "Échouer une Machine compromet une éventuelle Rive Sabotage (m(r) = 0) sur ce rayon ; aligner le Croc sur le Tambour peut le détourner d'une parcelle plus critique ailleurs."
          }
        },
        "temoins": [
          {
            "id": "G9_T1",
            "resume": "Tour 5 (Acte 2), G9 Face 1 sur Sabotage (2 paris), 2 Défenseurs sur Rive Piège de R, Tambour en parcelle 2 de R. Un seul Sabotage est révélé et m(R)=1 : la 1re activation de G9 ajoute 1 Écaille, pose le Croc en parcelle 2 de R (accord R>H : Rouge → Bleu) et happe une Écaille qui rallume Sabotage ! La 2nde activation happe la 2nde Machine de R et l'échoue inclinée sans dé → m(R)=2 à la Furtivité (Rive Piège gagnée) et passage Face 2.",
            "etat_attendu_verifie": {
              "double_happe_chainee": true,
              "m_r_furtivite": 2,
              "face_2": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Sabotage (en double pari dès que le sac est riche en Écailles/Sabotages). Échouer les Machines happées qui complètent une Rive Piège m(r)=2 et rejeter au sac celles qui casseraient une Rive Sabotage.",
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
        "vecteurs": "PIEGE_SERRE_ZENITHALE_MACHINE_ISOLEE_RECUL_SURCHAUFFE",
        "entrees_plancher": [
          "PLUME",
          "TAMBOUR",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "CHANT",
          "ROUGE"
        ],
        "entrees": [
          "PLUME",
          "TAMBOUR",
          "RANG_MACHINE",
          "CHANT",
          "ROUGE"
        ],
        "sorties": [
          "PIEGE",
          "RECUL",
          "BLEU"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": "Placée sur Piégeage, La Harpie s'auto-alimente tout en restant sur son icône : un premier Piège déclenché aux rangs bas (ou le Croc) active La Harpie, qui recule et piège une machine d'un rang supérieur ; lorsque cette seconde machine percute ce nouveau Piège plus tard aux attaques, Piégeage se rallume et déclenche la seconde activation de La Harpie.",
        "tags": [
          "CATALYSEUR_EVEIL",
          "PIEGE",
          "RECUL",
          "CIBLE_ISOLEE"
        ],
        "tuile_plateau": {
          "nom_court": "La Harpie féroce",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PIEGEAGE",
          "pictogrammes": [
            "PIC_PIEGE",
            "PIC_RANG_MACHINE",
            "PIC_RECUL",
            "PIC_TAMBOUR"
          ],
          "mots_cles_plateau": {
            "face_1": "Rayon 🪶 / 🥁 / machine seule sur son rang : +1 🪤 · Si seule sur son rang (ou rang 🎶) : ⏪ -1",
            "face_2": "Tout rayon : +1 🪤 · Puis sur 1 machine du rayon : ⏪ -1 (si mobile) ET 🔴→🔵 (si ≥ 1 🔴)",
            "enracine": null
          },
          "resume_plateau": "Cloue au sol la cible isolée"
        },
        "carte_joueur": {
          "titre_complet": "La Harpie féroce, Souveraine des Grands Fromagers",
          "entite_illustree": "La Harpie féroce (Harpia harpyja) entière plongeant depuis la cime d’un fromager géant",
          "brief_illustration": "La Harpie féroce (Harpia harpyja) entière, double huppe dressée et serres puissantes ouvertes, plongeant depuis la cime d’un fromager géant vers un engin isolé sur une piste forestière au son lointain d’un tambour.",
          "pitch_ambiance": "« Tant que les engins roulent en meute, l’ombre plane en silence ; dès que l’un d’eux s’isole à l’écart du convoi, les serres s’abattent du haut du fromager. »",
          "texte_regle": {
            "face_1": "Lorsque La Harpie féroce s’active, ciblez un rayon désigné par la Plume de Vigie, portant le Tambour, ou contenant une machine qui est la seule machine non annulée présente sur son rang 1–6 (à défaut, ciblez le rayon Oiseaux) :\n• Posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire de ce rayon.\n• Serre Zénithale : si une machine mobile de ce rayon est la seule machine non annulée sur son rang 1–6 (ou si son dé occupe le rang d’un Rêve portant le Chant), faites-la reculer d’1 parcelle vers la bordure (en sautant toute Route Forestière).",
            "face_2": "Lorsque La Harpie féroce s’active, ciblez n’importe quel rayon du plateau :\n• Posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire de ce rayon (ou de tout autre rayon si toutes ses parcelles sont déjà piégées).\n• Choisissez 1 machine de ce rayon : si elle est mobile, faites-la reculer d’1 parcelle vers la bordure ; et si elle porte au moins 1 jeton Rouge (y compris une machine en Ratissage), retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Coordonner le Dé d'Envol ou R5 pour expédier une machine dangereuse seule sur un rang élevé afin que La Harpie la recule ET pose un Piège devant sa nouvelle cible, ou piquer directement sur le rayon du Tambour.",
            "renoncement": "Isoler une machine sur un rang tardif (5 ou 6) pour déclencher la Serre Zénithale peut la faire passer en Assaut (Acte 1) ou en En avançant (rang 6) si le Piège est consommé avant son tour."
          }
        },
        "temoins": [
          {
            "id": "G11_T1",
            "resume": "À l'ouverture, R5 utilise un dé écarté 5 pour projeter le Bulldozer de H seul sur le rang 5 (Devant, parcelle 3) et allume Rêve. La Harpie Face 1 (sur Rêve) recule ce Bulldozer en parcelle 2 et pose 1 Piège ordinaire en parcelle 3 : au rang 5, le Bulldozer frappe Devant en parcelle 3, percute le Piège et allume Piégeage.",
            "etat_attendu_verifie": {
              "bulldozer_recul_p2": true,
              "piege_p3": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Piégeage (ou Rêve avec R5). Capter une machine isolée sur son rang pour cumuler recul + Piège sur sa future cible et chaîner les déclenchements Piégeage.",
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
          "CATALYSEUR_EVEIL"
        ],
        "est_twist": false,
        "vecteurs": "MIMETISME_SOUCHE_ALTERATION_ENDORMISSEMENT_ANNULATION",
        "entrees_plancher": [
          "SOUCHE",
          "PLUME",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "ALTERATION",
          "ROUGE"
        ],
        "entrees": [
          "SOUCHE",
          "PLUME",
          "RANG_MACHINE",
          "ALTERATION",
          "ROUGE"
        ],
        "sorties": [
          "ALTERATION",
          "ANNULATION",
          "BLEU",
          "RECUL",
          "PIEGE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE",
          "ICONE_REVE"
        ],
        "double_ouverture": "Même seul sans R9, deux activations dans le même tour (par exemple sur deux Sabotages ou via Résonance) réalisent le combo complet sur une même cible : la première pose l'Altération (+ Rouge → Bleu), la seconde endort immédiatement la machine à 90° (+ Piège en Face 2, allumant Piégeage en cascade). Avec R9 en jeu, deux activations endorment coup sur coup les deux machines altérées par l'Éclipse.",
        "tags": [
          "CATALYSEUR_EVEIL",
          "ALTERATION",
          "ANNULATION",
          "SOUCHE"
        ],
        "tuile_plateau": {
          "nom_court": "L’Ibijau",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_REVE",
          "pictogrammes": [
            "PIC_ALTERATION",
            "PIC_SOUCHE",
            "PIC_ANNULATION",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "Mobile sur 🪵 ou 🪶 : si sans 🌀 → pose 1 🌀 (+🔴→🔵) · Si déjà 🌀 → 🚫 à ce tour (ou ⏪ -1)",
            "face_2": "Toute mobile : +🌀 + (🔴→🔵 ou ⏪ -1), si déjà 🌀 → 🚫 + 🪤 · Ratissage : 🔴→🔵 + 🪤",
            "enracine": null
          },
          "resume_plateau": "Endort les machines altérées"
        },
        "carte_joueur": {
          "titre_complet": "L’Ibijau, Veilleur Fantôme des Souches Grises",
          "entite_illustree": "Le Grand Ibijau (Nyctibius grandis) entier figé à la verticale au sommet d’une souche grise",
          "brief_illustration": "Le Grand Ibijau (Nyctibius grandis) entier figé à la verticale au sommet d’une souche grise sous le clair de lune, son plumage d’écorce indiscernable du bois mort tandis qu’une brume violette enveloppe une machine arrêtée en contrebas.",
          "pitch_ambiance": "« Immobile sur sa souche comme un éclat d’écorce morte, il pousse à la nuit tombée une plainte si lente que l’engin déjà égaré s’endort sur place. »",
          "texte_regle": {
            "face_1": "Lorsque L’Ibijau s’active, ciblez 1 machine mobile occupant une parcelle qui porte au moins 1 Souche, ou appartenant au rayon ou au rang désigné par la Plume de Vigie (à défaut, une machine mobile du rayon Oiseaux ou Entités) :\n• Si elle ne porte pas de jeton d’Altération : prenez 1 jeton d’Altération de la réserve Entités et posez-le sur elle ; de plus, si elle porte au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges en Bleu Surchauffe.\n• Si elle porte déjà un jeton d’Altération : laissez ce jeton d’Altération sur elle (pour sa prochaine révélation) et, si son jeton Machine est révélé, non annulé et n’a pas encore résolu son activation à ce tour, inclinez-le à 90° (cette machine est annulée à ce tour) ; sinon, faites-la reculer d’1 parcelle vers la bordure.",
            "face_2": "Lorsque L’Ibijau s’active, ciblez n’importe quelle machine du plateau :\n• Si elle est mobile et sans Altération : posez 1 jeton d’Altération de la réserve Entités sur elle, puis au choix retournez 1 de ses jetons Rouges existants en Bleu Surchauffe ou faites-la reculer d’1 parcelle vers la bordure.\n• Si elle est mobile et porte déjà une Altération : laissez son Altération sur elle, inclinez son jeton Machine à 90° (annulée à ce tour si elle n’a pas encore agi ; sinon recul d’1 parcelle) et posez 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire de son rayon.\n• Si elle est en Ratissage : retournez 1 de ses jetons Rouges existants en Bleu Surchauffe et posez 1 Piège ordinaire sur sa parcelle si elle en est dépourvue.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Semer une nouvelle Altération sur une machine intacte pour préparer le tour suivant, ou frapper une machine déjà altérée (par R9 ou une première activation) pour cumuler deux tours complets de neutralisation.",
            "renoncement": "Concentrer deux activations sur la même machine la verrouille pour deux tours, mais laisse une seconde machine active frapper librement à ce tour."
          }
        },
        "temoins": [
          {
            "id": "G12_T1",
            "resume": "À l'ouverture, R9 (Éclipse de Plumes) pose 2 Altérations (dont une Abatteuse en parcelle 2 à 1 Souche) et allume Rêve. L'Ibijau Face 1 (sur Rêve) incline le jeton de l'Abatteuse à 90° : elle est annulée à ce tour ET conserve son Altération pour reculer sans frapper à sa prochaine pioche.",
            "etat_attendu_verifie": {
              "abatteuse_annulee": true,
              "alteration_conservee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Rêve (ou Sabotage). Endormir en priorité toute machine révélée déjà altérée (notamment après R9), sinon altérer et refroidir la machine mobile la plus menaçante sur Souche ou Plume.",
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
        "vecteurs": "ASPIRATION_LATERALE_ESSAIM_DUEL_TERRITOIRE_TENU_BLEU",
        "entrees_plancher": [
          "DUEL"
        ],
        "entrees_synergie": [
          "INSECTE",
          "ROUGE",
          "GARDIEN"
        ],
        "entrees": [
          "DUEL",
          "INSECTE",
          "ROUGE",
          "GARDIEN"
        ],
        "sorties": [
          "TERRITOIRE",
          "INSECTE",
          "INSECTE_RANG",
          "BLEU"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_INSECTE",
          "ICONE_PARADE"
        ],
        "double_ouverture": "Sur une double activation (ex. posé sur Parade ou Insecte), la 1re activation arme le Duel (ou le passe de Défi à Territoire tenu), refroidit une première machine et concentre l'Essaim ; la 2nde activation renforce un second front ou empile de nouveaux Insectes sur la Réglette et les icônes de la Piste des Gardiens pour sécuriser les paris d'Éveil.",
        "tags": [
          "INSECTES",
          "CATALYSEUR_EVEIL",
          "ASPIRATION",
          "DUEL"
        ],
        "tuile_plateau": {
          "nom_court": "Le Tamanoir",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_PARADE",
          "pictogrammes": [
            "PIC_INSECTE",
            "PIC_DUEL",
            "PIC_MIGRATION",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🐜 (+Aspire 2 voisins & +1 Réglette/Icône) + ⚔️ Tenu & 🔴→🔵",
            "face_2": "Toute parcelle + Déplace ⚔️ Tenu + 2 voisins & +1 Réglette/Icône",
            "enracine": "Standard (1 ou 2 Souches finales)"
          },
          "resume_plateau": "Aspire l'essaim, dresse le Duel"
        },
        "carte_joueur": {
          "titre_complet": "Le Tamanoir, Sentinelle à Crinière des Fourmilières",
          "entite_illustree": "Tamanoir géant entier dressé sur ses pattes arrière au milieu d'une clairière",
          "brief_illustration": "Dressé sur ses pattes arrière au milieu d'une clairière, queue en panache ancrée dans l'humus et griffes courbes grandes ouvertes devant un engin fumant, un tamanoir géant entier rassemble autour de lui les colonnes noires de fourmis surgies des fourrés voisins.",
          "pitch_ambiance": "« Quand le grand fourmilier se dresse debout, la forêt entière converge vers ses griffes : pas un essaim, pas un fauve ne recule d'un pouce. »",
          "texte_regle": {
            "face_1": "Lorsque Le Tamanoir s'active, choisissez 1 parcelle portant le jeton Duel ou au moins 1 Défenseur Mammifère (ou, à défaut, n'importe quelle parcelle du rayon Mammifère ou du rayon Insectes) :\n1. Langue Fouettante : posez 1 jeton Insecte de la réserve sur cette parcelle. En outre, s'il existe au moins 1 Insecte sur une parcelle de même numéro (1..4) d'un rayon immédiatement voisin (sans franchir de case devenue Route Forestière), vous pouvez aspirer latéralement jusqu'à 2 de ces Insectes sur la parcelle choisie ET poser 1 Insecte supplémentaire de la réserve directement sur un rang 1–6 de la Réglette ou sur une icône de la Piste des Gardiens.\n2. Posture Debout : si le jeton Duel est dans la réserve Mammifère, vous pouvez le poser sur sa face Défi sur cette parcelle ; s'il s'y trouve déjà sur Défi, retournez-le sur Territoire tenu. Enfin, sur 1 machine présente sur cette parcelle (ou ciblant cette parcelle), retournez 1 jeton Rouge existant sur sa face Bleue Surchauffe.",
            "face_2": "Lorsque Le Tamanoir s'active, choisissez n'importe quelle parcelle de la forêt :\n1. Posez 1 Insecte de la réserve sur cette parcelle, ET posez 1 Insecte de la réserve directement sur un rang 1–6 de la Réglette ou sur une icône de la Piste des Gardiens ; vous pouvez en outre aspirer latéralement jusqu'à 2 Insectes situés sur les parcelles de même numéro (1..4) des deux rayons immédiatement voisins (sans franchir de Route Forestière).\n2. Vous pouvez déplacer le jeton Duel (depuis la réserve Mammifère ou sa parcelle actuelle) sur cette parcelle, directement tourné sur Territoire tenu, puis retourner 1 jeton Rouge existant sur sa face Bleue Surchauffe sur une machine présente sur (ou ciblant) cette parcelle.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Aspirer latéralement les Insectes des rayons voisins pour concentrer un bastion imprenable autour du Duel et projeter un Insecte supplémentaire sur la Réglette ou en Bouclier de lisière.",
            "renoncement": "L'aspiration dégarnit les parcelles adjacentes où un allié comptait peut-être sur ces ouvrières pour une Parade."
          }
        },
        "temoins": [
          {
            "id": "G13_T1",
            "resume": "Tour 3, M1 a déployé des Insectes en parcelle 2 des rayons voisins. Une Parade au rang 1 active Le Tamanoir Face 1 sur la parcelle 2 de M (1 Défenseur, Duel Défi, Bulldozer 2 Rouges seuil 4) : il pose 1 Insecte, aspire 2 Insectes voisins (1 Déf + 3 Ins = 4), pose 1 Insecte sur une icône Gardien, passe Duel sur Territoire tenu et retourne 1 Rouge en Bleu (seuil 4 → 2). Parade Insecte aisée au rang 4.",
            "etat_attendu_verifie": {
              "insectes_m2": 3,
              "territoire_tenu": true,
              "seuil_reduit": 2
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Parade (ou Insecte). Cibler la parcelle du Duel menacée par une machine à Rouge pour cumuler renfort Essaim, Territoire tenu, refroidissement et Insecte sur Réglette/icône.",
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
        "vecteurs": "TERRIER_SOLAIRE_ECAILLE_INSECTE_MORSURE_THERMIQUE_CROC",
        "entrees_plancher": [
          "ECAILLE",
          "CROC",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "INSECTE",
          "INSECTE_RANG",
          "ROUGE"
        ],
        "entrees": [
          "ECAILLE",
          "CROC",
          "RANG_MACHINE",
          "INSECTE",
          "INSECTE_RANG",
          "ROUGE"
        ],
        "sorties": [
          "CROC",
          "BLEU",
          "ECAILLE",
          "INSECTE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_PIEGEAGE",
          "ICONE_SABOTAGE",
          "ICONE_INSECTE"
        ],
        "double_ouverture": "Posé sur Piégeage ou Sabotage, Le Téju enchaîne deux injections d'Écailles, refroidit deux machines Rouges marquées par M2 et recycle le Croc entre deux attaques pour catalyser les paris de toute la Piste des Gardiens.",
        "tags": [
          "INSECTES",
          "CATALYSEUR_EVEIL",
          "ECAILLE",
          "CROC",
          "SURCHAUFFE_BLEUE"
        ],
        "tuile_plateau": {
          "nom_court": "Le Téju",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_SABOTAGE",
          "pictogrammes": [
            "PIC_ECAILLE",
            "PIC_INSECTE",
            "PIC_BLEU",
            "PIC_CROC"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🦎 sac & +1 🐜 (machine/rang) + Machine avec 🐜 : 🔴→🔵 & (-1 🐜 → 🦷)",
            "face_2": "+2 🐜, 2 machines 🔴→🔵 & 🦷 gratuit",
            "enracine": "Standard (1 ou 2 Souches finales)"
          },
          "resume_plateau": "Traque machines marquées, déploie Croc"
        },
        "carte_joueur": {
          "titre_complet": "Le Téju, Maraudeur Doré des Termitières",
          "entite_illustree": "Grand lézard téju entier aux écailles noir et or jaillissant au pied d'une termitière",
          "brief_illustration": "Baigné d'un rayon de soleil brûlant au pied d'une haute termitière d'argile rouge, un grand lézard téju entier aux écailles noir et or jaillit hors de son terrier, dardant sa langue fourchue vers une machine surchauffée envahie de termites soldats.",
          "pitch_ambiance": "« Réveillé par la fièvre du métal et le crépitement des soldats d'argile, le téju fond droit sur la source de chaleur. »",
          "texte_regle": {
            "face_1": "Lorsque Le Téju s'active :\n1. Terrier Solaire : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; ET posez 1 jeton Insecte de la réserve soit sur la parcelle d'une machine de votre choix, soit sur un rang 1–6 de la Réglette occupé par le dé d'une machine.\n2. Morsure Thermique : choisissez ensuite 1 machine du plateau dont la parcelle ou le rang 1–6 sur la Réglette contient au moins 1 Insecte :\n• Si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ;\n• En outre, si le jeton Croc est dans la réserve Reptile, vous pouvez défausser 1 Insecte présent sur la parcelle ou sur le rang 1–6 de cette machine pour poser immédiatement le Croc sur n'importe quelle parcelle ciblée (par une machine non encore activée à ce tour, mobile ou en Ratissage).",
            "face_2": "Lorsque Le Téju s'active :\n1. S'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; ET posez 2 jetons Insectes de la réserve, répartis librement sur des parcelles occupées par des machines et/ou sur des rangs 1–6 occupés par des dés de machines.\n2. Appliquez Morsure Thermique sur jusqu'à 2 machines distinctes dont la parcelle ou le rang contient au moins 1 Insecte (retournant 1 jeton Rouge existant → Bleu Surchauffe sur chacune d'elles) ; de plus, si au moins l'une d'elles est ainsi ciblée et que le Croc est dans la réserve Reptile, posez immédiatement le Croc sur une parcelle ciblée sans avoir à défausser d'Insecte.",
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "En Face 1, consommer un Insecte posé sur la parcelle ou le rang d'une machine Rouge (notamment celui parachuté par M2) pour déployer aussitôt le Croc et allumer Piégeage.",
            "renoncement": "Défausser cet Insecte le retire d'une Parade Insecte ou d'une déviation ±1 au tour suivant."
          }
        },
        "temoins": [
          {
            "id": "G14_T1",
            "resume": "Tour 4, à la Production, M2 a parachuté 1 Insecte sur le rang 5 d'un Bulldozer (2 Rouges). Aux attaques (rang 1), le Croc pare une Abatteuse (Piégeage) et active Le Téju Face 1 : +1 Écaille au sac, +1 Insecte sur une autre machine Rouge, puis Morsure Thermique sur le Bulldozer du rang 5 (1 Rouge → Bleu, défausse l'Insecte du rang 5 pour reposer le Croc devant ce Bulldozer).",
            "etat_attendu_verifie": {
              "rouge_retourne": 1,
              "croc_repose": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Sabotage ou Piégeage. Marquer une machine chargée en Rouges puis défausser un Insecte déjà passé d'ouverture pour reposer le Croc sur une parcelle ciblée ultérieure.",
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
        "vecteurs": "POLLEN_DES_CIMES_NECTAR_EVEIL_PIQUE_POLLINISATION_FINALE",
        "entrees_plancher": [
          "DE_ENVOL",
          "PLUME",
          "GARDIEN"
        ],
        "entrees_synergie": [
          "INSECTE",
          "INSECTE_RANG",
          "ROUGE",
          "SOUCHE"
        ],
        "entrees": [
          "DE_ENVOL",
          "PLUME",
          "GARDIEN",
          "INSECTE",
          "INSECTE_RANG",
          "ROUGE",
          "SOUCHE"
        ],
        "sorties": [
          "PARI_GLISSE",
          "INSECTE_RANG",
          "BLEU",
          "RECUL",
          "ARBRE"
        ],
        "paiement": [
          "P_PARI"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_INSECTE",
          "ICONE_RESONANCE"
        ],
        "double_ouverture": "Sur Insecte (allumé une 1re fois à l'ouverture par déviation ±1, puis une 2nde fois aux attaques par Parade Insecte), Le Colibri pose 2 Insectes aériens, refroidit ou refoule une machine et fait glisser un pari allié bloqué pour boucler l'Éveil de la Forêt.",
        "tags": [
          "INSECTES",
          "CATALYSEUR_EVEIL",
          "ENRACINEMENT",
          "NECTAR_EVEIL"
        ],
        "tuile_plateau": {
          "nom_court": "Le Colibri",
          "fenetre_badge": "ACTIVATION",
          "icone_conseillee": "ICONE_INSECTE",
          "pictogrammes": [
            "PIC_INSECTE",
            "PIC_PARI_ENCOCHE",
            "PIC_BLEU",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🐜 (Dé Envol/🪶, ou Icône si Calme) + [Piqué 🔴→🔵/⏪ 1 OU -1 🐜 Icône → ⭐]",
            "face_2": "+1 🐜 libre (dont Icône) + Les 2 effets",
            "enracine": "Fin : +1 🪵 sur ≤ 2 parcelles avec 🐜/🪹"
          },
          "resume_plateau": "Pollinise pistes, valide paris, régénère"
        },
        "carte_joueur": {
          "titre_complet": "Le Colibri, Joyau Émeraude des Cimes",
          "entite_illustree": "Colibri à gorge d'émeraude entier en vol stationnaire au-dessus d'orchidées géantes",
          "brief_illustration": "Suspendu en vol stationnaire dans un poudroiement d'or au-dessus d'orchidées géantes de la canopée, un colibri à gorge d'émeraude entier guide dans le sillage vibrant de ses ailes une nuée d'ouvrières ailées vers les cimes blessées.",
          "pitch_ambiance": "« Cent battements d'ailes par seconde : là où le joyau vert effleure la corolle, l'essaim trouve sa route et la forêt garde mémoire de sa floraison. »",
          "texte_regle": {
            "face_1": "Lorsque Le Colibri s'active :\n1. Pollen des Cimes : posez 1 jeton Insecte de la réserve soit sur le rang 1–6 de la Réglette indiqué par le Dé d'Envol de l'Oiseau, soit sur l'emplacement marqué par la Plume de Vigie (sur ce rang 1–6, ou sur la 1re parcelle du rayon au pied duquel repose la Plume) — OU, si la Plume de Vigie affiche sa face Calme, directement sur l'icône de votre choix de la Piste des Gardiens.\n2. L'Appel du Colibri : choisissez 1 seul des deux effets suivants :\n• Piqué Vertigineux : sur 1 machine dont le dé occupe un rang portant au moins 1 Insecte (ou située sur le rayon marqué par la Plume de Vigie), retournez 1 jeton Rouge existant sur sa face Bleue Surchauffe ; si elle ne porte aucun jeton Rouge et est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).\n• Nectar d'Éveil : défaussez 1 Insecte présent sur l'icône d'un Gardien de la Piste des Gardiens portant encore au moins 1 Défenseur en pari : glissez immédiatement 1 de ces Défenseurs dans une encoche latérale libre de ce Gardien (sécurisant cette mise pour la Face 2 ou l'Éveil de la Forêt, sans déclencher le pouvoir de ce Gardien).",
            "face_2": "Lorsque Le Colibri s'active :\n1. Posez 1 jeton Insecte de la réserve sur le rang du Dé d'Envol, sur l'emplacement marqué par la Plume de Vigie, OU directement sur n'importe quelle icône de la Piste des Gardiens (quelle que soit la face de la Plume).\n2. Résolvez les deux effets de L'Appel du Colibri (Piqué Vertigineux ET Nectar d'Éveil).",
            "enracine": "Pollinisation Suprême (Décompte final uniquement). Au décompte final (Tour 8, Sommeil ou Éveil), tant que la parcelle d'ancrage du Colibri n'est pas devenue une Route Forestière, en plus de sa régénération standard sur cette parcelle (1 Souche retournée en Arbre debout en Face 1, ou 2 en Face 2), retournez 1 Souche survivante supplémentaire en Arbre debout sur chacune d'au plus 2 autres parcelles de la forêt contenant au moins 1 Insecte ou 1 Nid (à défaut, sur d'autres parcelles du rayon Oiseau)."
          },
          "decision_et_renoncement": {
            "choix": "Consommer un Insecte d'icône (via M3 ou Plume Calme) par Nectar d'Éveil pour convertir un Bouclier de lisière en vrai pari gagné, ou enraciner Le Colibri en Face 2 pour sauver jusqu'à 4 Souches au décompte final.",
            "renoncement": "Défausser l'Insecte d'icône retire le Bouclier de lisière en cas de seconde mise non validée ; enraciner Le Colibri sacrifie son catalyseur d'Éveil actif."
          }
        },
        "temoins": [
          {
            "id": "G15_T1",
            "resume": "Tour 6, M3 a projeté 1 Insecte sur Sabotage où un Gardien allié porte encore 1 pari. Aux attaques, une Parade Insecte active Le Colibri Face 2 : il pose 1 Insecte sur le rang 4 du Dé d'Envol, retourne 1 Rouge en Bleu par Piqué Vertigineux, puis défausse l'Insecte de Sabotage par Nectar d'Éveil pour glisser le dernier pari d'Éveil. Enraciné Face 2, il retourne jusqu'à 4 Souches au décompte final.",
            "etat_attendu_verifie": {
              "pari_allie_glisse": true,
              "souches_finales_max": 4
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Siéger sur Insecte (ou Parade). Combiner M3 ou Plume Calme avec Nectar d'Éveil pour sécuriser les paris bloqués ; enraciner Face 2 en fin de partie lorsque l'Essaim couvre ≥ 2 parcelles à Souches.",
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
          "AUTONOMIE_A0"
        ],
        "est_twist": false,
        "vecteurs": "VOILE_ALTERATION_TRANSE_TAMBOUR_TELEPORTATION_TRANSE_CHANT_A0",
        "entrees_plancher": [
          "POSITION_REVE",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "ALTERATION",
          "ROUGE"
        ],
        "entrees": [
          "POSITION_REVE",
          "TAMBOUR",
          "CHANT",
          "ALTERATION",
          "ROUGE"
        ],
        "sorties": [
          "DEFENSEUR_REDEPLOYE",
          "RANG_REVE",
          "ALTERATION",
          "ANNULATION",
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
          "TAMBOUR",
          "CHANT",
          "ALTERATION"
        ],
        "tuile_plateau": {
          "nom_court": "Voyage Astral",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_ALTERATION",
            "PIC_TAMBOUR",
            "PIC_CHANT",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "🌀/🔴→🔵 + [Téléporte 🥁 & 🔴→🔵/🌀 OU 🎶 : annule +1 machine sinon Glisse 1G]",
            "face_2": null,
            "enracine": "Standard (1 Souche finale, bloque Sommeil)"
          },
          "resume_plateau": "Guide Tambour ou purifie Chant"
        },
        "carte_joueur": {
          "titre_complet": "Le Chant du Voyage Astral",
          "entite_illustree": "Chamane humain frappant son tambour tandis que son double lumineux traverse la canopée",
          "brief_illustration": "Assis les yeux clos devant un feu de résine bleue, un chamane humain frappe son tambour tandis que son double lumineux traverse la canopée pour se matérialiser bras levés devant l'engin qui menace un rayon lointain.",
          "pitch_ambiance": "« Le corps demeure près des braises, mais le battement du tambour franchit trois vallées avant que la scie n'ait touché l'écorce. »",
          "texte_regle": {
            "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :\n1. Voile d'Altération : posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore (ou, sur une machine mobile portant déjà une Altération et au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe).\n2. Danse du Tambour et du Chant : choisissez 1 seule des deux transes suivantes :\n• Transe du Tambour : si le pion Tambour se trouve actuellement sur une parcelle de forêt ou sur un Rêve de la Réglette, déplacez-le immédiatement vers n'importe quelle parcelle de n'importe quel rayon du plateau ; sur 1 machine présente sur (ou ciblant) cette parcelle d'arrivée, retournez 1 jeton Rouge existant en Bleu Surchauffe (ou, si elle n'a aucun Rouge, est mobile et sans Altération, posez sur elle 1 jeton d'Altération).\n• Transe du Chant : désignez le Rêve portant le pion Chant (ou ce Rêve R1 lui-même si le Chant n'occupe aucun Rêve). S'il reste au moins 1 machine active sur son rang, annulez 1 machine supplémentaire sur ce rang (inclinez son jeton à 90° ; si le pion Chant est sur ce Rêve et qu'aucune machine active n'y reste, le Chant déclenche aussitôt son glissement d'1 rang vers la gauche) ; sinon (si aucune machine active n'occupe ce rang et que ce Rêve n'a pas encore glissé à cette ouverture), faites glisser ce Rêve (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Choisir Transe du Tambour pour corriger à livres ouverts la position du Tambour (et déclencher R2), ou Transe du Chant pour annuler une seconde machine ou faire glisser un Rêve même sur un rang vide.",
            "renoncement": "Redéployer le Tambour renonce à l'annulation supplémentaire ou au glissement gratuit du Chant, et inversement."
          }
        },
        "temoins": [
          {
            "id": "R1_T1",
            "resume": "Tour 4 (table {H, E, I}), Tambour posé au 1er déploiement en parcelle 2 de I (où la machine recule par Altération) et Chant au 2nd déploiement sur R1 au rang 5 (rang vide). R1 pose 1 Altération (Voile d'Altération) puis tranche : Transe du Tambour téléporte le Tambour en parcelle 3 de E et retourne le Rouge du Bulldozer en Bleu, OU Transe du Chant glisse R1 du rang 5 au rang 3 libre.",
            "etat_attendu_verifie": {
              "voile_alteration": true,
              "transe_au_choix": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Choisir Transe du Tambour dès qu'une parcelle critique manque d'un Défenseur (surtout avec R2 en jeu), sinon choisir Transe du Chant pour nettoyer une double machine ou avancer vers le Sommeil.",
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
        "cycle": "PASSIF_CONTINU",
        "cablage": null,
        "roles_portes": [
          "AUTONOMIE_A0",
          "LOI_PASSIVE"
        ],
        "est_twist": false,
        "vecteurs": "LOI_PASSIVE_TAMBOUR_DOUBLE_VEILLE_ALTERATION_DOUBLE_FRAPPE_BLEU_A0",
        "entrees_plancher": [
          "POSITION_REVE",
          "TAMBOUR",
          "RANG_MACHINE"
        ],
        "entrees_synergie": [
          "ANNULATION",
          "ROUGE"
        ],
        "entrees": [
          "POSITION_REVE",
          "TAMBOUR",
          "RANG_MACHINE",
          "ANNULATION",
          "ROUGE"
        ],
        "sorties": [
          "ALTERATION",
          "BLEU"
        ],
        "paiement": [],
        "nature": "LOI_PASSIVE",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "LOI_PASSIVE",
          "TAMBOUR",
          "ALTERATION",
          "SURCHAUFFE_BLEUE"
        ],
        "tuile_plateau": {
          "nom_court": "Doubles Chamaniques",
          "fenetre_badge": "PERMANENT",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_LOI_PASSIVE",
            "PIC_TAMBOUR",
            "PIC_ALTERATION",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "Passif : Défendu ou 🌙 annule (rayon 🥁/🔴) → 🌀 · Parade 🥁 → 🔴→🔵 (sinon 🌀)",
            "face_2": null,
            "enracine": "Standard (1 Souche finale, bloque Sommeil)"
          },
          "resume_plateau": "Le Tambour reflète l'altération mystique"
        },
        "carte_joueur": {
          "titre_complet": "Le Pacte des Doubles Chamaniques",
          "entite_illustree": "Guerrier porteur de tambour et entité spectrale frappant dos à dos la même membrane",
          "brief_illustration": "Debout dos à dos au centre d'une clairière nocturne, un guerrier porteur de tambour et une entité spectrale couronnée de lucioles frappent d'un même geste la membrane tendue dont l'onde bleue fige une abatteuse en pleine charge.",
          "pitch_ambiance": "« Chaque battement de peau tendue résonne des deux côtés du voile : là où l'homme tient bon, l'esprit retourne la fièvre du fer contre lui. »",
          "texte_regle": {
            "face_1": "Tant que ce Rêve occupe un rang de la Réglette (même sans Défenseur posé sur lui) :\n• Double de Veille (À l'ouverture) : lorsque ce Rêve est défendu à sa résolution d'ouverture, OU chaque fois qu'un autre Rêve défendu annule au moins 1 machine qui appartient au rayon portant le Tambour Humain ou qui possède au moins 1 jeton Rouge, posez 1 jeton d'Altération de la réserve Entités sur une machine mobile de votre choix qui n'en porte pas encore.\n• Double de Frappe (Aux attaques) : chaque fois qu'une frappe de machine est parée par des Défenseurs sur la parcelle portant le Tambour Humain : si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge), si elle est mobile et ne porte pas encore d'Altération, posez sur elle 1 jeton d'Altération de la réserve Entités.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Envoyer le Tambour dès le 1er déploiement sur le rayon le plus exposé pour maximiser à la fois Double de Veille à l'ouverture et Double de Frappe aux attaques.",
            "renoncement": "Engager le Tambour au 1er déploiement avant l'ouverture des paravents le fige sur ce rayon si R1 n'est pas défendu pour le déplacer."
          }
        },
        "temoins": [
          {
            "id": "R2_T1",
            "resume": "Tour 3 (table {H, E, I}), R2 non défendu au rang 6, autre Rêve défendu au rang 2, Tambour en parcelle 2 de H. Le Rêve du rang 2 annule l'Abatteuse de H (rayon du Tambour) → Double de Veille pose 1 Altération sur l'Abatteuse de I. Aux attaques, le Bulldozer de H (1 Rouge) est paré sur la parcelle du Tambour → Double de Frappe retourne son Rouge en Bleu.",
            "etat_attendu_verifie": {
              "alteration_i": true,
              "rouge_retourne_h": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Construire R2 rapidement pour profiter de ses deux déclencheurs passifs ; placer le Tambour sur une parcelle défendue face à des machines à Rouge pour multiplier les Altérations et les Bleus.",
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
        "roles_portes": [
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "PIEGE_TAMBOUR_DUEL_ECHO_THERMIQUE_REVE_ENRACINEMENT_TRIPLE",
        "entrees_plancher": [
          "POSITION_REVE",
          "TAMBOUR",
          "DUEL"
        ],
        "entrees_synergie": [
          "CHANT",
          "ROUGE",
          "SOUCHE"
        ],
        "entrees": [
          "POSITION_REVE",
          "TAMBOUR",
          "DUEL",
          "CHANT",
          "ROUGE",
          "SOUCHE"
        ],
        "sorties": [
          "PIEGE",
          "BLEU",
          "RANG_REVE",
          "ARBRE"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": null,
        "tags": [
          "ENRACINEMENT",
          "PIEGE",
          "TAMBOUR",
          "DUEL"
        ],
        "tuile_plateau": {
          "nom_court": "L’Appel du Singe Hurleur",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_PIEGE",
            "PIC_TAMBOUR",
            "PIC_DUEL",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🪤 (🥁/⚔️) · avec 🎶 et/ou ⚔️ : 🔴→🔵 et/ou 🌙 ←1",
            "face_2": null,
            "enracine": "Décompte final : régénère 2 🪵 sur H + 1 🪵 sur rayon allié 0-Route (priorité M)"
          },
          "resume_plateau": "Piéger les sentes, enracinement bonifié"
        },
        "carte_joueur": {
          "titre_complet": "L’Appel du Singe Hurleur",
          "entite_illustree": "Vision chamanique d'un singe hurleur dominant la canopée à l'aube",
          "brief_illustration": "Au sommet d'un grand arbre baigné de brume dorée, la silhouette visionnaire d'un singe hurleur pousse son cri d'aube tandis que des lianes-pièges se tendent entre les rayons des chamanes et des grands fauves.",
          "pitch_ambiance": "« Son cri d'aube court de cime en cime, scellant les frontières des grands fauves pour que la graine dorme jusqu'au renouveau. »",
          "texte_regle": {
            "face_1": "À l'ouverture, lorsque ce Rêve est défendu (après le choix éventuel des machines annulées), posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire du rayon portant le Tambour ou le jeton Duel (ou du rayon de H si aucune n'est éligible).\nÉcho territorial (H>M) : vérifiez combien des conditions suivantes sont réunies (0, 1 ou 2) : (1) le Chant occupe le rang de ce Rêve ou ce Rêve vient d'annuler au moins 1 machine ; (2) le jeton Duel est en jeu en forêt alliée.\n• 1 condition : retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine de l'un de ces rayons, OU glissez 1 Rêve d'1 rang libre à gauche.\n• 2 conditions : appliquez les deux effets ci-dessus (si aucune machine de ces rayons n'a de Rouge, posez à la place 1 second Piège ordinaire sur une autre parcelle dépourvue de Piège ordinaire des rayons du Tambour ou du Duel).",
            "face_2": null,
            "enracine": "Si H enracine volontairement cette tuile au ménage au pied de son rayon devant une parcelle non-Route, elle perd son pouvoir actif et rend impossible le Sommeil du Contremaître ; aucune Souche n'est retournée lors de la pose ni pendant les Tours 1 à 8. Uniquement lors du décompte final (quelle que soit la fin de partie), au lieu de régénérer 1 seule Souche, retournez jusqu'à 2 Souches existantes en Arbres debout sur leurs parcelles du rayon de H (en commençant par sa parcelle d'attache), plus 1 Souche existante en Arbre debout sur un autre rayon allié sans aucune Route Forestière (en priorité celui de M s'il est sans Route, sinon un rayon portant une autre tuile Enracinée)."
          },
          "decision_et_renoncement": {
            "choix": "Conserver R3 actif sur la Réglette pour tisser des Pièges protecteurs et garder ouverte la voie du Sommeil, ou l'enraciner au ménage avant qu'une Route ne condamne le rayon pour verrouiller jusqu'à 3 régénérations au décompte final.",
            "renoncement": "Enraciner R3 ferme définitivement la victoire par Sommeil du Contremaître et éteint sa production de Pièges."
          }
        },
        "temoins": [
          {
            "id": "R3_T1",
            "resume": "Tour 4, Tambour en parcelle 2 de H, Chant sur R3 au rang 3, Duel en parcelle 2 de M. À l'ouverture, R3 annule 1 machine au rang 3, pose 1 Piège en parcelle 2 de H, puis (2 conditions réunies) retourne 1 Rouge en Bleu sur M ET glisse un Rêve du rang 5 au rang 4. Enraciné au Tour 6 devant une parcelle non-Route (0 repousse immédiate), il retourne 2 Souches sur H + 1 Souche sur M sans Route au décompte final.",
            "etat_attendu_verifie": {
              "piege_h2": true,
              "souches_finales": 3
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Défendre R3 avec le Chant tant que le Duel est en forêt pour cumuler Piège + Bleu + glissement de Rêve ; enraciner aux Tours 6–8 si le Sommeil est écarté et que H/M conservent des Souches sans Route.",
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
          "LEVIER_REVE"
        ],
        "est_twist": false,
        "vecteurs": "ENGLOUTISSEMENT_MACHINE_INCLINEE_SAC_FURTIVITE_ECAILLE_CROC_REVE",
        "entrees_plancher": [
          "POSITION_REVE",
          "ANNULATION",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "ECAILLE",
          "ROUGE"
        ],
        "entrees": [
          "POSITION_REVE",
          "ANNULATION",
          "TAMBOUR",
          "CHANT",
          "ECAILLE",
          "ROUGE"
        ],
        "sorties": [
          "RANG_REVE",
          "ECAILLE",
          "CROC",
          "BLEU"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE",
          "ICONE_PIEGEAGE"
        ],
        "double_ouverture": null,
        "tags": [
          "LEVIER_REVE",
          "FURTIVITE",
          "ECAILLE",
          "CROC",
          "CARAPACE_LIMON"
        ],
        "tuile_plateau": {
          "nom_court": "Carapace de Limon",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_ANNULATION",
            "PIC_ECAILLE",
            "PIC_CROC",
            "PIC_CHANT"
          ],
          "mots_cles_plateau": {
            "face_1": "Machine inclinée → au Sac opaque (m(r) - 1) + 1 🦎 au sac · 🥁/🎶 : 🦷 + 🌙 ←1",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "Engloutir machine annulée au sac"
        },
        "carte_joueur": {
          "titre_complet": "Le Songe de la Carapace de Limon",
          "entite_illustree": "Vision fluviale d'une carapace de limon et de feuilles noyées engloutissant le fer",
          "brief_illustration": "Sous les eaux ambrées d'un bras mort, une immense carapace couverte de limon et de feuilles noyées s'entrouvre dans un songe silencieux pour engloutir une machine annulée loin des rives.",
          "pitch_ambiance": "« Feuille morte parmi les feuilles noyées, sa carapace engloutit le vacarme du fer dans le silence du limon. »",
          "texte_regle": {
            "face_1": "À l'ouverture, lorsque ce Rêve est défendu (après le choix éventuel des machines annulées ici), choisissez 1 jeton Machine incliné à 90° (annulé par ce Rêve ou par un Rêve précédent) et plongez-le immédiatement dans le Sac opaque en retirant son dé de la Réglette : disparu sous l'eau avant la Furtivité, ce jeton ne compte plus dans m(r) pour la Furtivité (soit m(r) − 1, tout en restant comptabilisé comme machine annulée à ce tour pour le Chant et pour allumer l'icône Rêve). (Plancher : si aucune machine n'est inclinée, retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine mobile ou glissez 1 Rêve d'1 rang libre à gauche.)\nAjoutez ensuite 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu).\nSillage H>R : si la machine engloutie provenait du rayon du Tambour ou du rang du Chant (ou si au moins 1 Écaille est déjà sortie du sac à ce tour), posez ou déplacez le pion Croc sur une parcelle alliée et glissez 1 Rêve d'1 rang libre à gauche.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Engloutir une machine annulée d'un rayon à m(r)=1 pour le ramener à m(r)=0 et remporter la Rive Sabotage (+1 Sabotage au sac), tout en injectant 1 Écaille et en posant le Croc.",
            "renoncement": "Engloutir cette machine renonce à m(r)=2 sur une Rive Piège et remet dès maintenant ce jeton Machine en circulation dans le Sac opaque avant une éventuelle Happe de G9."
          }
        },
        "temoins": [
          {
            "id": "R4_T1",
            "resume": "Tour 4, 2 Défenseurs sur Rive Sabotage de H (vise m(H)=0), Tambour en parcelle 1 de H, Chant et 1 Défenseur sur R4 au rang 2 où tombe l'unique Machine de H. R4 annule cette machine, l'engloutit aussitôt dans le Sac opaque (m(H) retombe à 0), ajoute 1 Écaille au sac, pose le Croc et glisse un autre Rêve à gauche (Sillage H>R), puis le Chant avance R4 au rang 1. À la Furtivité, m(H)=0 gagne la Rive Sabotage.",
            "etat_attendu_verifie": {
              "m_h_furtivite": 0,
              "ecaille_au_sac": 1,
              "rive_sabotage_gagnee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Engloutir toute machine annulée d'un rayon engagé en Rive Sabotage (ramenant m(r) de 1 à 0) tout en alimentant le sac en Écailles et en déclenchant le Sillage Croc + glissement de Rêve.",
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
        "roles_portes": [
          "TWIST_2K3",
          "LEVIER_REVE"
        ],
        "est_twist": true,
        "vecteurs": "LECTURE_DE_ECARTE_TELEPORTATION_RANG_MACHINE_OU_REVE",
        "entrees_plancher": [
          "DES_SOUS_PARAVENT",
          "DE_ENVOL",
          "POSITION_REVE"
        ],
        "entrees_synergie": [
          "CHANT",
          "PLUME"
        ],
        "entrees": [
          "DES_SOUS_PARAVENT",
          "DE_ENVOL",
          "POSITION_REVE",
          "CHANT",
          "PLUME"
        ],
        "sorties": [
          "RANG_MACHINE",
          "RANG_REVE"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "TWIST_2K3",
          "LEVIER_REVE",
          "DES_ECARTES",
          "TELEPORTATION_RANG"
        ],
        "tuile_plateau": {
          "nom_court": "Condor des Brumes",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_TWIST",
            "PIC_DES_PARAVENT",
            "PIC_RANG_MACHINE",
            "PIC_AVANCEE_REVE"
          ],
          "mots_cles_plateau": {
            "face_1": "⚡ Lit 1 🎲 écarté (V) : machine → rang V OU ce 🌙 → V / ⬅️ (les 2 si 🎶 ou 🪶 rang)",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "⚡ Dé écarté 🎲 → Rang V / ⬅️"
        },
        "carte_joueur": {
          "titre_complet": "La Vision du Condor des Brumes",
          "entite_illustree": "Silhouette astrale d'un grand condor planant au-dessus d'une mer de nuages étoilés reliés au souffle d'un chamane",
          "brief_illustration": "Silhouette astrale d'un grand condor andin-amazonien planant au-dessus d'une mer de nuages nocturnes où brillent des constellations géométriques reliées au souffle d'un chamane.",
          "pitch_ambiance": "« Rien de ce qui roule dans l'ombre des mains humaines n'échappe à l'œil qui plane au-dessus des nuages : même le destin écarté trace encore une route. »",
          "texte_regle": {
            "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu, choisissez 1 dé non retenu visible devant le paravent ouvert de l'Oiseau, des Humains, ou de tout joueur ayant révélé un Sabotage ou une Écaille (c'est-à-dire le Dé d'Envol non choisi, le dé standard supérieur non retenu d'un porteur de Machine, ou l'un des dés lancés à blanc sur un Sabotage/Écaille). Soit V sa valeur (de 1 à 6). Appliquez 1 présage au choix — ou les deux si ce Rêve porte le Chant ou si la Plume de Vigie est posée près d'un rang 1–6 :\n• Courant Ascendant : déplacez le dé actif d'1 machine mobile non annulée de votre choix directement sur le rang V de la Réglette (si un Rêve défendu situé strictement à droite de ce Rêve ne s'est pas encore résolu et occupe le rang V, il pourra annuler cette machine lors de son tour de résolution !).\n• Aile du Songe : si le rang V ne porte aucun autre Rêve et est situé à gauche de ce Rêve, déplacez ce Rêve (avec ses Défenseurs solidaires) directement sur le rang V ; sinon, faites glisser ce Rêve vers le premier rang libre à sa gauche (vers le rang 1).",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Sous paravent fermé, l'Oiseau fait face à un vrai casse-tête d'initié : s'il obtient min(D1,D2) = 3 et Dé d'Envol = 1, garde-t-il 1 pour adoucir sa propre machine, ou retient-il 3 afin de laisser le 1 disponible comme dé écarté pour catapulter Le Condor des Brumes directement de la case 6 à la case 1 !",
            "renoncement": "Téléporter une machine ennemie vers un Rêve situé plus à droite neutralise cette machine mais consomme l'annulation de ce second Rêve."
          }
        },
        "temoins": [
          {
            "id": "R5_T1",
            "resume": "R5 construit au rang 6 est défendu avec le Chant, tandis que l'Oiseau a révélé un Sabotage dont les dés lancés sous paravent affichent 1 et 5 : R5 lit le dé écarté 1, saute directement du rang 6 au rang 1 par Aile du Songe ET projette par Courant Ascendant un Bulldozer d'Assaut du rang 5 vers le Mode Charge au rang 1 !",
            "etat_attendu_verifie": {
              "nouveau_rang_r5": 1,
              "nouveau_rang_bulldozer": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Chercher parmi les dés écartés un rang occupé par un Rêve défendu situé plus à droite pour annuler gratuitement un Bulldozer actif, ou la valeur libre la plus basse (1 ou 2) pour projeter ce Rêve vers le Sommeil.",
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
        "vecteurs": "MIEL_DE_VEILLE_INSECTES_X2_DANSE_FRETILLANTE_DEVIATION_CHANT_A0",
        "entrees_plancher": [
          "POSITION_REVE",
          "RANG_MACHINE",
          "TAMBOUR",
          "CHANT"
        ],
        "entrees_synergie": [
          "NID",
          "INSECTE_RANG",
          "ROUGE"
        ],
        "entrees": [
          "POSITION_REVE",
          "RANG_MACHINE",
          "TAMBOUR",
          "CHANT",
          "NID",
          "INSECTE_RANG",
          "ROUGE"
        ],
        "sorties": [
          "INSECTE_RANG",
          "RANG_MACHINE",
          "BLEU",
          "RANG_REVE"
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
          "DEVIATION",
          "CHANT"
        ],
        "tuile_plateau": {
          "nom_court": "Mélipones d’Or",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_INSECTE",
            "PIC_RANG_MACHINE",
            "PIC_BLEU",
            "PIC_CHANT"
          ],
          "mots_cles_plateau": {
            "face_1": "+2 🐜 (Réglette/🥁/🪹) + Décale 1 dé ±1 (🔴→🔵 si 🐜/🌙) + 🎶 libre → Glisse 1G",
            "face_2": null,
            "enracine": "Standard (1 Souche finale, bloque Sommeil)"
          },
          "resume_plateau": "Essaime le miel, danse déviante"
        },
        "carte_joueur": {
          "titre_complet": "Le Rêve des Mélipones d’Or",
          "entite_illustree": "Chamane entourée d'un essaim doré d'abeilles mélipones autour d'un tronc creux",
          "brief_illustration": "Autour d'un tronc creux baigné de brume dorée où chantent une chamane et son essaim d'abeilles mélipones sans dard, des spirales de pollen lumineux infléchissent la course d'un convoi de machines à travers la brume.",
          "pitch_ambiance": "« La danse des abeilles sacrées ne se trompe jamais d'angle : un bourdonnement suffit à égarer le fer hors du sentier. »",
          "texte_regle": {
            "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :\n1. Miel de Veille : prenez 2 jetons Insectes de la réserve et répartissez-les librement entre les rangs 1–6 de la Réglette, la parcelle portant le Tambour, et/ou une parcelle portant un Nid (si ni le Tambour ni aucun Nid ne sont en forêt, vous pouvez aussi les placer sur une parcelle du rayon Humain).\n2. Danse Frétillante : vous pouvez décaler le dé révélé d'1 machine encore active de −1 ou +1 rang sur la Réglette (entre 1 et 6) ; si ce dé rejoint un rang portant au moins 1 Insecte ou un Rêve défendu situé plus à droite (non encore résolu), et que cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe. Enfin, si un Rêve portant le pion Chant n'a pas encore glissé à cette ouverture et que son rang ne contient désormais plus aucune machine active, faites-le glisser immédiatement (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Répartir les 2 Insectes entre un Nid (pour franchir le seuil ≥ 2 avant la Production), le Tambour ou la Réglette ; puis choisir entre dégager le rang du Chant ou faire basculer une machine Rouge d'Assaut vers Charge.",
            "renoncement": "Alimenter un Nid ou le Tambour renonce à garnir la Réglette pour les déviations futures et le refroidissement de Danse Frétillante."
          }
        },
        "temoins": [
          {
            "id": "R6_T1",
            "resume": "Tour 3 (Acte 1), R6 défendu par le Chant au rang 4 face à 2 machines (Abatteuse + Bulldozer 2 Rouges). R6 annule l'Abatteuse, pose 1 Insecte sur M4 (passe à 2 avant Production) et 1 sur le rang 3, puis décale le Bulldozer de 4 → 3 (Charge, seuil −1, 1 Rouge → Bleu) ; le rang 4 étant vidé, le Chant fait glisser R6 à gauche.",
            "etat_attendu_verifie": {
              "bulldozer_rang": 3,
              "rouge_retourne": 1,
              "r6_glisse_gauche": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Alimenter un Nid à 1 Insecte et la Réglette par Miel de Veille, puis décaler une machine Rouge d'Assaut vers un rang Insecte ou Rêve à droite tout en libérant le rang du Chant.",
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
        "cycle": "SIMPLE_CONTINU",
        "cablage": null,
        "roles_portes": [
          "LEVIER_REVE"
        ],
        "est_twist": false,
        "vecteurs": "FOULEE_ONIRIQUE_DUEL_TERRITOIRE_ALTERATION_HANTISE_SOUCHES",
        "entrees_plancher": [
          "POSITION_REVE",
          "DUEL",
          "SOUCHE"
        ],
        "entrees_synergie": [
          "ALTERATION",
          "ROUGE"
        ],
        "entrees": [
          "POSITION_REVE",
          "DUEL",
          "SOUCHE",
          "ALTERATION",
          "ROUGE"
        ],
        "sorties": [
          "RANG_REVE",
          "TERRITOIRE",
          "ALTERATION",
          "BLEU"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "LEVIER_REVE",
          "DUEL",
          "ALTERATION",
          "SOUCHE"
        ],
        "tuile_plateau": {
          "nom_court": "Brame des Brumes",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_AVANCEE_REVE",
            "PIC_DUEL",
            "PIC_ALTERATION",
            "PIC_SOUCHE"
          ],
          "mots_cles_plateau": {
            "face_1": "Glisse 1G + [⚔️ Tenu & 🌀/🔴→🔵 OU 2e Glisse si 🪵/⚔️]",
            "face_2": null,
            "enracine": "Standard (1 Souche finale, bloque Sommeil)"
          },
          "resume_plateau": "Glisse un rêve, arme le Duel"
        },
        "carte_joueur": {
          "titre_complet": "Le Songe du Brame des Brumes",
          "entite_illustree": "Silhouette translucide d'un grand cerf des marais aux bois de brume violette",
          "brief_illustration": "Au milieu d'une futaie déchirée où fument des souches noires, la silhouette translucide d'un grand cerf des marais fait face à un bulldozer figé, ses bois de brume violette traçant au sol un cercle infranchissable.",
          "pitch_ambiance": "« Quand le brame des esprits répond au défi du fauve, la clairière blessée se referme comme un rempart invisible devant les chenilles. »",
          "texte_regle": {
            "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :\n1. Foulée Onirique : faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).\n2. Appel du Territoire Spectral : choisissez 1 seul des deux effets suivants :\n• Ancrer la Harde : si le jeton Duel est déjà en forêt sur sa face Défi, retournez-le immédiatement sur sa face Territoire tenu ; s'il est dans la réserve Mammifère, posez-le sur sa face Défi sur n'importe quelle parcelle contenant au moins 1 Défenseur ou 1 Souche. Ensuite, sur le rayon portant désormais le Duel, posez 1 jeton d'Altération sur une machine mobile sans Altération (ou retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine de ce rayon).\n• Hantise des Souches : si au moins 1 machine annulée par ce Rêve — ou au moins 1 machine mobile portant déjà un jeton d'Altération — appartient à un rayon comptant au moins 1 Souche (ou portant le Duel), faites glisser une seconde fois un Rêve en jeu (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Choisir Ancrer la Harde pour verrouiller Territoire tenu dès l'ouverture et poser une Altération, ou Hantise des Souches pour convertir les Souches en double bond vers le Sommeil.",
            "renoncement": "Verrouiller le Duel renonce au double glissement de Rêve ; accélérer le Sommeil renonce au verrouillage préventif du Duel."
          }
        },
        "temoins": [
          {
            "id": "R7_T1",
            "resume": "Tour 3, R7 défendu au rang 5 ; Duel (face Défi) en parcelle 2 de M face à l'Abatteuse (rang 3 En avançant, 0 Altération). À l'ouverture, R7 glisse au rang 4 libre puis choisit Ancrer la Harde : le Duel passe sur Territoire tenu (bloquant l'avancée du rang 3) et l'Abatteuse reçoit 1 Altération.",
            "etat_attendu_verifie": {
              "reve_rang": 4,
              "territoire_tenu": true,
              "alteration_posee": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Défendre R7 pour garantir 1 glissement de Rêve par tour ; choisir Ancrer la Harde dès qu'un rang 3/6 menace le Duel, sinon choisir Hantise des Souches pour accélérer le Sommeil.",
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
        "vecteurs": "LECTURE_PERCHOIR_PLUME_DOUBLE_GLISSEMENT_OU_ALTERATION",
        "entrees_plancher": [
          "PLUME",
          "PERCHOIR",
          "POSITION_REVE"
        ],
        "entrees_synergie": [
          "ANNULATION"
        ],
        "entrees": [
          "PLUME",
          "PERCHOIR",
          "POSITION_REVE",
          "ANNULATION"
        ],
        "sorties": [
          "RANG_REVE",
          "ALTERATION"
        ],
        "paiement": [
          "P_RANG"
        ],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_REVE"
        ],
        "double_ouverture": null,
        "tags": [
          "LEVIER_REVE",
          "PERCHOIR",
          "PLUME",
          "ECLIPSE"
        ],
        "tuile_plateau": {
          "nom_court": "Éclipse de Plumes",
          "fenetre_badge": "OUVERTURE",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_PLUME",
            "PIC_PERCHOIR",
            "PIC_AVANCEE_REVE",
            "PIC_ALTERATION"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🌀 + 1 🌙 ⬅️ + regarde 🦅 (Chaud/Machine : +2e 🌀 · Calme/🚫 : +2e ⬅️)",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "+🌀 + 🌙 ⬅️ + bonus 🪶/🦅"
        },
        "carte_joueur": {
          "titre_complet": "Le Rêve de l’Éclipse de Plumes",
          "entite_illustree": "Couronne d'ailes nocturnes éclipsant la pleine lune au-dessus de la canopée dans une pluie de plumes violettes",
          "brief_illustration": "Immense couronne d'ailes sombres tourbillonnant devant le disque lunaire au-dessus de la canopée, faisant pleuvoir des plumes luminescentes qui voilent les projecteurs des engins forestiers.",
          "pitch_ambiance": "« Là où tombe la plume de vigie, la lune s'éteint pour les hommes de fer : leurs phares éclairent une forêt qui a déjà bougé. »",
          "texte_regle": {
            "face_1": "À l'ouverture des paravents, lorsque ce Rêve est défendu :\n1. Posez 1 jeton d'Altération sur 1 machine mobile qui n'en porte pas encore, ET faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).\n2. Consultez secrètement le jeton posé sur le Perchoir de Vigie de l'Oiseau (s'il est face cachée, reposez-le face cachée sans le révéler au reste de la table), puis appliquez 1 bonus d'Éclipse au choix parmi ceux déverrouillés :\n• Éclipse Chaude (déverrouillée si la Plume de Vigie est face Chaud OU si le Perchoir porte un jeton Machine) : posez 1 second jeton d'Altération sur une machine mobile qui n'en porte pas encore, choisie sur le rayon ou le rang marqué par la Plume — ou directement sur la machine correspondant au jeton du Perchoir.\n• Éclipse Calme (déverrouillée si la Plume de Vigie est face Calme OU si ce Rêve a annulé au moins 1 machine à cette ouverture) : faites glisser d'1 rang libre vers la gauche un Rêve en jeu de votre choix (le même Rêve pour un double glissement, ou un second Rêve).",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Sous paravents fermés, l'Oiseau oriente silencieusement l'Éclipse par la face (Chaud vs Calme) de sa Plume et le jeton caché sur son Perchoir ; à l'ouverture, les Entités choisissent entre doubler le ralentissement physique (2 Altérations) ou doubler la compression de la Réglette vers le Sommeil (2 glissements de Rêve).",
            "renoncement": "Pousser deux fois les Rêves vers la gauche rapproche la victoire par Sommeil mais renonce à neutraliser la prochaine ouverture d'une seconde machine mobile."
          }
        },
        "temoins": [
          {
            "id": "R9_T1",
            "resume": "Dans une partie E–O–M (sans H), l'Oiseau a caché 1 Bulldozer sur son Perchoir de Vigie et posé sa Plume face Calme au pied du rayon Mammifère. R9, construit au rang 4 et défendu, consulte le Perchoir (déverrouillant Éclipse Chaude via la Machine cachée ET Éclipse Calme via la Plume Calme) : E choisit Éclipse Calme, pose 1 Altération et fait glisser deux fois R9 (de 4 en 3, puis de 3 en 2, sautant le rang 1 déjà occupé) pour assembler instantanément le bloc contigu 1..2 !",
            "etat_attendu_verifie": {
              "alterations_posees": 1,
              "glissements_reve": 2,
              "nouveau_rang_r9": 2,
              "bloc_sommeil_1_2_forme": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Choisir Éclipse Calme dès qu'un Rêve se trouve à droite du bloc contigu 1..k afin d'accélérer le Sommeil ; choisir Éclipse Chaude si tous les Rêves sont déjà groupés à gauche pour altérer la machine cachée sur le Perchoir.",
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
        "roles_portes": [
          "TWIST_2K3"
        ],
        "est_twist": true,
        "vecteurs": "COLONNE_RAID_LATERAL_TOPOLOGIQUE_DUEL_TENU_BLEU_RECUL",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE",
          "ROUTE"
        ],
        "entrees_synergie": [
          "DUEL",
          "ROUGE"
        ],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "ROUTE",
          "DUEL",
          "ROUGE"
        ],
        "sorties": [
          "RAID_LATERAL",
          "TERRITOIRE",
          "BLEU",
          "RECUL",
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
          "TWIST_2K3",
          "RAID_LATERAL",
          "DUEL"
        ],
        "tuile_plateau": {
          "nom_court": "Bivouac Légionnaire",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_TWIST",
            "PIC_MIGRATION",
            "PIC_DUEL",
            "PIC_BLEU"
          ],
          "mots_cles_plateau": {
            "face_1": "Raid latéral 1–3 🐜 même profondeur (stop 🛣️) + ⚔️ Tenu/+1 🐜 + 🔴→🔵/⏪ 1",
            "face_2": null,
            "enracine": "Standard (1 Souche finale)"
          },
          "resume_plateau": "Raid latéral d'essaim entre rayons"
        },
        "carte_joueur": {
          "titre_complet": "Le Bivouac des Légionnaires, Marée Noire des Sous-Bois",
          "entite_illustree": "Sphère vivante de fourmis légionnaires lançant un pont grouillant d'une rive à l'autre",
          "brief_illustration": "Accrochée entre les contreforts de deux kapokiers, une sphère vivante de millions de fourmis légionnaires lance un pont grouillant d'une rive forestière à l'autre tandis qu'un félin aux aguets accompagne l'avancée de la colonne vers les machines.",
          "pitch_ambiance": "« Là où la forêt tient encore debout d'un seul tenant, la légion ignore les frontières : ses ponts vivants submergent trois vallées en une heure. »",
          "texte_regle": {
            "face_1": "À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :\n1. Colonne de Raid Latérale (Twist topologique) : choisissez une profondeur de forêt (parcelle 1, 2, 3 ou 4) contenant au moins 1 Insecte sur le rayon de ce Nid (ou sur le rayon portant le jeton Duel). Vous pouvez déplacer latéralement de 1 à 3 Insectes présents sur cette parcelle de départ en les répartissant sur des parcelles de même numéro (1..4) le long de rayons voisins consécutifs (vers la gauche et/ou vers la droite autour du plateau), sans jamais franchir une case devenue Route Forestière. (Ces Insectes pourront ensuite migrer normalement le long de leur nouveau rayon à la Migration.)\n2. Morsure d'Avant-Garde : choisissez 1 parcelle ayant reçu au moins 1 Insecte de cette Colonne (ou la parcelle de ce Nid si aucun Insecte n'a changé de rayon) :\n• Si le jeton Duel s'y trouve sur sa face Défi, retournez-le immédiatement sur Territoire tenu et ajoutez +1 Insecte de la réserve sur cette parcelle ;\n• De plus, sur 1 machine occupant cette parcelle : si elle possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge) et qu'elle est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Projeter 1 à 3 Insectes latéralement chez les voisins pour irriguer toute la table avant la Migration et activer Morsure d'Avant-Garde sur le Duel ou une machine.",
            "renoncement": "Vider le Nid sous le seuil de 2 Insectes fait retomber sa prochaine Production à +1 ; une Route Forestière sur la profondeur choisie coupe définitivement le pont latéral."
          }
        },
        "temoins": [
          {
            "id": "M1_T1",
            "resume": "Tour 4 (I, M, H, O ; parcelle 2 d'O est Route). M1 en parcelle 2 de I (2 Insectes) produit +2 (total 4), garde 2 Insectes et envoie 1 en parcelle 2 de M (Duel Défi + Abatteuse sans Rouge) et 1 en parcelle 2 de H (bloqué avant O par la Route). Morsure d'Avant-Garde sur M·2 passe le Duel sur Territoire tenu (+1 Insecte) et recule l'Abatteuse en M·1.",
            "etat_attendu_verifie": {
              "raid_m2_h2": true,
              "territoire_tenu": true,
              "abatteuse_recul_m1": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Garder au moins 2 Insectes au Nid pour la production +2 et projeter le surplus latéralement vers la parcelle du Duel ou les fronts menacés avant la Migration radiale.",
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
        "vecteurs": "MINERALISATION_ECAILLE_SAC_PROJECTION_INSECTE_SUR_ROUGE",
        "entrees_plancher": [
          "NID_ACTIVE",
          "ROUGE"
        ],
        "entrees_synergie": [
          "SABOTAGE",
          "ECAILLE"
        ],
        "entrees": [
          "NID_ACTIVE",
          "ROUGE",
          "SABOTAGE",
          "ECAILLE"
        ],
        "sorties": [
          "ECAILLE",
          "INSECTE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [
          "ICONE_SABOTAGE",
          "ICONE_INSECTE"
        ],
        "double_ouverture": null,
        "tags": [
          "INSECTES",
          "ECAILLE",
          "ANTI_ROUGE",
          "TERMITIERE_CUIRASSEE"
        ],
        "tuile_plateau": {
          "nom_court": "Termitière Cuirassée",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_ECAILLE",
            "PIC_INSECTE",
            "PIC_ROUGE"
          ],
          "mots_cles_plateau": {
            "face_1": "+1 🦎 Sac (ou +1 🐜 si 0 🦎 réserve) · Si 💥/🦎 ou 🔴 : +1 🐜 sur machine 🔴 ou rang 1–6",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "+🦎 Sac + 🐜 sur machine 🔴 / rang"
        },
        "carte_joueur": {
          "titre_complet": "La Termitière Cuirassée, Bastion d’Argile et d’Écailles",
          "entite_illustree": "Dôme d'argile ferrugineuse vitrifié aux crêtes d'écailles d'où jaillissent des soldats mandibulés",
          "brief_illustration": "Dôme d'argile ferrugineuse vitrifié par le soleil équatorial, hérissé de crêtes minérales aussi dures que l'écaille d'un caïman, d'où jaillissent des soldats mandibulés vers les engins fumants.",
          "pitch_ambiance": "« Cuite par la chaleur même des moteurs, sa muraille secrète des plaques de pierre vive qui grippent les engrenages de toute la forêt. »",
          "texte_regle": {
            "face_1": "À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :\n1. Carapace Minérale : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; sinon (si les 4 Écailles sont déjà hors de la réserve Reptile), ajoutez +1 Insecte de la réserve sur la parcelle de ce Nid.\n2. Réplique Thermique : si au moins 1 Sabotage ou Écaille a été révélé à cette ouverture OU si au moins 1 machine du plateau porte un jeton Rouge (y compris en Ratissage), prenez 1 Insecte supplémentaire de la réserve et posez-le directement soit sur la parcelle d'une machine portant au moins 1 jeton Rouge, soit sur un rang 1–6 de la Réglette occupé par le dé d'une telle machine.",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Parachuter l'Insecte bonus directement sur la parcelle d'une machine en Ratissage (d'où il pourra parer sur place ou migrer immédiatement depuis la dernière parcelle vers une icône Gardien !) ou l'installer tout de suite sur un rang 1–6 pour préparer une déviation ±1 dès la prochaine ouverture.",
            "renoncement": "Défendre M2 chaque tour vide rapidement la réserve d'Écailles Reptiles vers le sac (maximisant la dilution, mais privant temporairement un effet comme G9 d'Écaille fraîche en réserve tant qu'aucune n'a été consommée)."
          }
        },
        "temoins": [
          {
            "id": "M2_T1",
            "resume": "Au Tour 3, M2 est défendu alors qu'un Bulldozer allié en parcelle 4 est déjà passé en Ratissage (+1 jeton Rouge physique). Après sa production standard, M2 glisse 1 Écaille dans le sac opaque et pose +1 Insecte de la réserve directement en parcelle 4 sur le Bulldozer en Ratissage : à la Migration qui suit immédiatement, cet Insecte peut soit rester en parcelle 4 pour préparer une Parade Insecte + la cible du Téju, soit sauter directement de la parcelle 4 vers la Piste des Gardiens !",
            "etat_attendu_verifie": {
              "ecailles_ajoutees_sac": 1,
              "insecte_parachute_parcelle_4": true
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Défendre régulièrement pour injecter les 4 Écailles dans le sac et parachuter l'Insecte thermique sur une parcelle en Ratissage (pour parer avec Le Téju ou migrer vers les pistes centrales).",
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
        "roles_portes": [],
        "est_twist": false,
        "vecteurs": "PONT_DE_SOIE_AERIEN_PROJECTION_DIRECTE_REGLETTE_PISTE",
        "entrees_plancher": [
          "NID_ACTIVE",
          "DE_ENVOL",
          "PLUME"
        ],
        "entrees_synergie": [
          "GARDIEN"
        ],
        "entrees": [
          "NID_ACTIVE",
          "DE_ENVOL",
          "PLUME",
          "GARDIEN"
        ],
        "sorties": [
          "INSECTE_RANG",
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
          "PONT_AERIEN",
          "REGLETTE",
          "TISSERANDS"
        ],
        "tuile_plateau": {
          "nom_court": "Nid Tisserand",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_NID",
            "PIC_PERCHOIR",
            "PIC_PLUME",
            "PIC_INSECTE"
          ],
          "mots_cles_plateau": {
            "face_1": "1 🐜 du 🪹 → rang Dé d’Envol ou 🪶 · Si 🪶 rayon/Calme : +1 🐜 réserve ou icône",
            "face_2": null,
            "enracine": null
          },
          "resume_plateau": "🦅/🪶 → projection directe 🐜 sur rang 1–6"
        },
        "carte_joueur": {
          "titre_complet": "Le Nid Tisserand des Cimes, Hamac de Soie des Hauts Vents",
          "entite_illustree": "Sphère aérienne de feuilles cousues de soie blanche dans la canopée d'où planent des fourmis tisserandes",
          "brief_illustration": "Sphère aérienne de feuilles vertes cousues de soie blanche tout en haut d'une branche maîtresse, sous l'œil d'un oiseau de vigie, d'où des fourmis tisserandes se laissent planer au bout de longs fils argentés.",
          "pitch_ambiance": "« Pourquoi ramper à travers les souches quand un seul fil tendu sous l'aile de l'oiseau suffit à traverser toute la canopée ? »",
          "texte_regle": {
            "face_1": "À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :\n1. Fil d'Envol : prenez 1 Insecte présent sur la parcelle de ce Nid (ou sur une parcelle du rayon Oiseau) et placez-le directement sur le rang 1–6 de la Réglette indiqué par le Dé d'Envol de l'Oiseau — OU, si la Plume de Vigie est posée près d'un rang 1–6, sur ce rang (sans passer par la dernière parcelle).\n2. Brise de Vigie : si la Plume de Vigie est posée au pied du rayon de ce Nid ou du rayon Oiseau, OU si elle est sur sa face Calme, choisissez 1 bonus : ajoutez +1 Insecte de la réserve sur la parcelle de ce Nid, OU projetez 1 Insecte présent sur la parcelle de ce Nid directement sur l'icône de votre choix de la Piste des Gardiens (pour préparer un Bouclier de lisière ou l'appel du Colibri).",
            "face_2": null,
            "enracine": null
          },
          "decision_et_renoncement": {
            "choix": "Même construit dès le Tour 1 en parcelle 1, M3 contourne les 3 tours de marche vers la parcelle 4 : l'Oiseau choisit sous paravent s'il utilise sa Plume pour désigner un rang libre précis à l'Essaim ou s'il la pose face Calme au pied d'un rayon pour générer +1 Insecte ou un Bouclier de lisière instantané.",
            "renoncement": "Projeter 2 Insectes hors du Nid en un seul tour dégarnit la parcelle du Nid et risque de ramener sa production suivante de +2 à +1 si moins de 2 Insectes y restent."
          }
        },
        "temoins": [
          {
            "id": "M3_T1",
            "resume": "Dès le Tour 1, M3 est construit en parcelle 3 du rayon Insectes (sans machine au départ décalé !) et défendu au Tour 2. L'Oiseau a obtenu 4 sur son Dé d'Envol et posé sa Plume face Calme près du rang 2. Après production, M3 catapulte directement 1 Insecte sur le rang 2 (Plume) et gagne +1 Insecte bonus sur le Nid (face Calme) sans avoir jamais eu besoin d'atteindre la parcelle 4 !",
            "etat_attendu_verifie": {
              "insecte_projete_rang": 2,
              "insecte_bonus_nid": 1
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Construire tôt même loin de la parcelle 4 pour alimenter dès le Tour 2 la Réglette 1–6 en déviations ±1 et déclencher la double repousse du Colibri (G15).",
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
          "AUTONOMIE_A0",
          "ENRACINEMENT"
        ],
        "est_twist": false,
        "vecteurs": "LIANES_FORMIQUES_PIEGE_SABOTAGE_HARMONIE_CHANT_TERRA_PRETA_A0",
        "entrees_plancher": [
          "NID_ACTIVE",
          "INSECTE"
        ],
        "entrees_synergie": [
          "TAMBOUR",
          "CHANT",
          "ROUGE",
          "SOUCHE"
        ],
        "entrees": [
          "NID_ACTIVE",
          "INSECTE",
          "TAMBOUR",
          "CHANT",
          "ROUGE",
          "SOUCHE"
        ],
        "sorties": [
          "PIEGE",
          "SABOTAGE",
          "BLEU",
          "INSECTE_RANG",
          "ARBRE"
        ],
        "paiement": [],
        "nature": "ACTION",
        "declencheurs_amorces": [],
        "double_ouverture": null,
        "tags": [
          "A0",
          "INSECTES",
          "ENRACINEMENT",
          "PIEGE",
          "TERRA_PRETA"
        ],
        "tuile_plateau": {
          "nom_court": "Fourmis Sacrées",
          "fenetre_badge": "PRODUCTION",
          "icone_conseillee": null,
          "pictogrammes": [
            "PIC_PIEGE",
            "PIC_SABOTAGE",
            "PIC_BLEU",
            "PIC_ENRACINEMENT"
          ],
          "mots_cles_plateau": {
            "face_1": "[-1 🐜 → +1 🪤 (🪹/H/🥁) OU +1 💥 sac & 🔴→🔵] + Si 🥁/🎶 : +1 🐜 (Réglette/🪹)",
            "face_2": null,
            "enracine": "Fin : +1 🪵 sur ≤ 2 parcelles (rayon H ou 🪤 / ≥ 2 🐜)"
          },
          "resume_plateau": "Tresse pièges, fertilise la fin"
        },
        "carte_joueur": {
          "titre_complet": "Le Jardin des Fourmis Sacrées, Clairière du Pacte Ancien",
          "entite_illustree": "Clairière d'arbres Duroia entretenue par des fourmis rousses et bordée de totems humains",
          "brief_illustration": "Au cœur d'une clairière d'arbres Duroia entretenue par des millions de petites fourmis rousses et bordée de totems humains tressés de lianes-pièges, une terre noire fertile couve les jeunes pousses sous les souches calcinées.",
          "pitch_ambiance": "« Autour du jardin sacré, les lianes mordent d'acide ; dessous, la terre noire des ancêtres attend l'heure de relever la futaie. »",
          "texte_regle": {
            "face_1": "À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :\n1. Lianes Formiques : choisissez 1 seule des deux options suivantes :\n• Fosse de Lianes : défaussez 1 Insecte présent sur la parcelle de ce Nid (ou sur la parcelle portant le Tambour) pour poser immédiatement 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire appartenant au rayon de ce Nid, au rayon Humain, ou au rayon portant le Tambour.\n• Cendre de Bivouac : glissez 1 jeton Sabotage ordinaire dans le sac opaque, ET sur 1 machine située sur le rayon de ce Nid ou sur le rayon portant le Tambour qui possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.\n2. Harmonie du Chant : si le pion Tambour occupe la parcelle de ce Nid — OU si le pion Chant occupe actuellement un Rêve sur la Réglette — posez +1 jeton Insecte de la réserve directement sur un rang 1–6 de la Réglette ou sur la parcelle de ce Nid.",
            "face_2": null,
            "enracine": "Terre Noire des Ancêtres (Décompte final uniquement). Au décompte final (quelle que soit l'issue qui met fin à la partie), tant que la parcelle d'ancrage de cette tuile n'est pas devenue une Route Forestière, en plus de la 1 Souche retournée en Arbre debout sur sa parcelle d'ancrage, retournez jusqu'à 2 Souches survivantes supplémentaires en Arbres debout, choisies sur des parcelles distinctes appartenant au rayon Humain et/ou contenant au moins 1 Piège ordinaire ou au moins 2 Insectes (max 1 Souche supplémentaire par parcelle ainsi choisie)."
          },
          "decision_et_renoncement": {
            "choix": "Sacrifier 1 Insecte pour poser un Piège autonome par Fosse de Lianes, ou diluer le sac et refroidir une machine par Cendre de Bivouac ; enraciner M4 sans bloquer le Sommeil pour régénérer jusqu'à 3 Souches au décompte final.",
            "renoncement": "Enraciner M4 renonce définitivement à sa fabrique de Pièges et de Sabotages ; Fosse de Lianes consomme 1 Insecte qui peut faire redescendre le Nid sous 2 Insectes."
          }
        },
        "temoins": [
          {
            "id": "M4_T1",
            "resume": "Tour 6 (table {H, E, I} visant le Sommeil), M4 en parcelle 1 de I (2 Insectes, défendu), Chant sur un Rêve : produit +2 (4), dépense 1 Insecte pour 1 Piège en H·3 (Fosse de Lianes) et regagne +1 Insecte (Harmonie du Chant). Enraciné au ménage du Tour 6 sans bloquer le Sommeil, il retourne 3 Souches en Arbres debout au décompte final du Tour 7.",
            "etat_attendu_verifie": {
              "piege_h3": true,
              "souches_finales": 3
            },
            "statut": "A_CODER"
          }
        ],
        "heuristique_bot": "Produire des Pièges sur H/I via Fosse de Lianes quand le Chant compense l'Insecte dépensé, ou diluer le sac par Cendre de Bivouac ; enraciner M4 en fin de partie (compatible Sommeil) pour +3 Arbres finaux.",
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
  }
};

const AUTHOR_WORKSPACE_INITIAL_V6_3 = null;
