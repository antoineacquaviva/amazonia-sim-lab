/* ============================================================================
 * Amazonia Doc Studio — Explorateur de Tuiles & Modèle des 197 Assises (v6.2)
 * Module vanilla JS pur sans bundler (compatible file://, HTTPS & Node vm).
 * ============================================================================ */
(function (global) {
  'use strict';

  const VERSION = '6.2.0';
  const PEUPLE_CANON_ORDER = ['H', 'E', 'M', 'R', 'O', 'I'];
  const ANIMAL_PEUPLES = new Set(['M', 'R', 'O']);
  const ONIRIQUE_PEUPLES = new Set(['H', 'E']);

  // Ordre canonique v6.2 gauche -> droite des 6 icônes de la Piste des Gardiens
  const GUARDIAN_ICONS_V62 = [
    {
      id: 'ICONE_PARADE',
      pos: 1,
      key: 'PARADE',
      label: 'Parade',
      short: 'Parade',
      icon: '🛡️',
      desc: 'Parade classique par Défenseurs seuls'
    },
    {
      id: 'ICONE_PIEGEAGE',
      pos: 2,
      key: 'PIEGEAGE',
      label: 'Piégeage',
      short: 'Piégeage',
      icon: '🪤',
      desc: 'Frappe arrêtée par un Piège autonome ou le Croc'
    },
    {
      id: 'ICONE_SABOTAGE',
      pos: 3,
      key: 'SABOTAGE',
      label: 'Sabotage',
      short: 'Sabotage',
      icon: '💥',
      desc: 'Jeton Sabotage ou Écaille révélé à l’ouverture'
    },
    {
      id: 'ICONE_REVE',
      pos: 4,
      key: 'REVE',
      label: 'Rêve',
      short: 'Rêve',
      icon: '🌙',
      desc: 'Rêve défendu annulant au moins une machine'
    },
    {
      id: 'ICONE_INSECTE',
      pos: 5,
      key: 'INSECTE',
      label: 'Insecte',
      short: 'Insecte',
      icon: '🪲',
      desc: 'Déviation ±1 ou Parade impliquant des Insectes (actif si I joue)'
    },
    {
      id: 'ICONE_RESONANCE',
      pos: 6,
      key: 'RESONANCE',
      label: 'Résonance',
      short: 'Résonance',
      icon: '✨',
      desc: '6e icône : compteur individuel des 1res activations des autres Gardiens'
    }
  ];

  const GUARDIAN_ICON_BY_ID = Object.fromEntries(GUARDIAN_ICONS_V62.map(ic => [ic.id, ic]));

  // Garde-fou critique : normalisation stricte des anciens entiers pré-v6.2 de declencheurs_amorces
  // En pré-v6.2 : 4 = Résonance, 5 = Rêve, 6 = Insecte (NE JAMAIS confondre 6 avec ICONE_RESONANCE).
  const LEGACY_DECLENCHEUR_TO_V62_ICON = {
    1: 'ICONE_PARADE',
    2: 'ICONE_PIEGEAGE',
    3: 'ICONE_SABOTAGE',
    4: 'ICONE_RESONANCE',
    5: 'ICONE_REVE',
    6: 'ICONE_INSECTE'
  };

  function normalizeDeclencheurToIconId(raw) {
    if (raw === null || raw === undefined || raw === '') return null;
    if (typeof raw === 'number') {
      return LEGACY_DECLENCHEUR_TO_V62_ICON[raw] || null;
    }
    const str = String(raw).trim().toUpperCase();
    if (GUARDIAN_ICON_BY_ID[str]) return str;
    if (GUARDIAN_ICON_BY_ID['ICONE_' + str]) return 'ICONE_' + str;
    if (/^[1-6]$/.test(str)) {
      return LEGACY_DECLENCHEUR_TO_V62_ICON[Number(str)] || null;
    }
    return null;
  }

  // Libellés humains iconifiés des états, ressources et paiements
  const STATE_META = {
    SOUCHE: { icon: '🪵', label: 'Souche', group: 'Forêt' },
    PIEGE: { icon: '🪤', label: 'Piège', group: 'Défense' },
    CROC: { icon: '🦷', label: 'Croc', group: 'Reptiles' },
    SABOTAGE: { icon: '💥', label: 'Sabotage', group: 'Sac' },
    ECAILLE: { icon: '🦎', label: 'Écaille', group: 'Reptiles' },
    CALE: { icon: '🧱', label: 'Cale Sabotage', group: 'Contrôle' },
    ROUGE: { icon: '🔴', label: 'Rouge (+1)', group: 'Puissance' },
    BLEU: { icon: '🔵', label: 'Bleu (−1)', group: 'Puissance' },
    DUEL: { icon: '⚔️', label: 'Duel', group: 'Mammifères' },
    TERRITOIRE: { icon: '🏰', label: 'Territoire tenu', group: 'Mammifères' },
    PLUME: { icon: '🪶', label: 'Plume', group: 'Oiseaux' },
    PERCHOIR: { icon: '🦅', label: 'Perchoir', group: 'Oiseaux' },
    ALTEREE: { icon: '✨', label: 'Altération', group: 'Entités' },
    INSECTE: { icon: '🪲', label: 'Insecte', group: 'Essaim' },
    INSECTE_PASSAGER: { icon: '🐞', label: 'Insecte passager', group: 'Essaim' },
    INSECTE_RANG: { icon: '🪲', label: 'Insecte (Réglette)', group: 'Essaim' },
    TAMBOUR: { icon: '🥁', label: 'Tambour', group: 'Humains' },
    NID: { icon: '🪹', label: 'Nid', group: 'Essaim' },
    NID_ACTIVE: { icon: '🪹', label: 'Production Nid', group: 'Essaim' },
    GARDIEN: { icon: '🗿', label: 'Gardien en piste', group: 'Gardiens' },
    PARI_GLISSE: { icon: '🎯', label: 'Pari en encoche', group: 'Gardiens' },
    DEFENSEUR_ATTENTE: { icon: '🧍', label: 'Défenseur en attente', group: 'Placement' },
    DEFENSEUR_REDEPLOYE: { icon: '🏃', label: 'Défenseur redéployé', group: 'Placement' },
    ANNULATION: { icon: '🚫', label: 'Annulation machine', group: 'Rêves' },
    POSITION_REVE: { icon: '🌙', label: 'Position Rêve', group: 'Rêves' },
    RANG_REVE: { icon: '🌙', label: 'Glissement Rêve', group: 'Rêves' },
    RANG_MACHINE: { icon: '🎲', label: 'Rang machine', group: 'Tempo' },
    RECUL: { icon: '⏪', label: 'Recul machine', group: 'Contrôle' },
    MOBILISATION: { icon: '🔥', label: 'Mobilisation m(r)', group: 'Furtivité' },
    // Paiements terminaux
    P_ARBRE: { icon: '🌳', label: 'Arbres sauvés', group: 'Paiement' },
    P_SOUCHE: { icon: '🌱', label: 'Repousse Souches', group: 'Paiement' },
    P_PARI: { icon: '☀️', label: 'Éveil / Paris', group: 'Paiement' },
    P_RANG: { icon: '💤', label: 'Sommeil / Rangs', group: 'Paiement' }
  };

  const VECTOR_DEFS_V62 = {
    V1: {
      code: 'V1',
      short: 'Forêt, Souches, recul & position des machines',
      full: 'Forêt, Souches, recul & position des machines'
    },
    V2: {
      code: 'V2',
      short: 'Rangs & Puissance Rouge/Bleu',
      full: 'Rangs de la Réglette & jetons Puissance (Rouge / Bleu Surchauffe)'
    },
    V3: {
      code: 'V3',
      short: 'Pièges, Croc, Sabotages, Écailles & Altération',
      full: 'Pièges, Croc, Sabotages, Écailles & Altération'
    },
    V4: {
      code: 'V4',
      short: 'Défenseurs, Insectes & Duel',
      full: 'Défenseurs, essaim d’Insectes & jeton Duel'
    },
    V5: {
      code: 'V5',
      short: 'Rêves, Piste des Gardiens & signaux muets',
      full: 'Rêves, Piste des Gardiens & signaux muets (Plume, Perchoir)'
    }
  };

  const VECTOR_TOOLTIPS = Object.fromEntries(
    Object.entries(VECTOR_DEFS_V62).map(([k, v]) => [k, `${v.code} (${v.short})`])
  );

  function formatVectorTooltip(vecRaw) {
    const raw = String(vecRaw || '').trim();
    if (!raw) return '';
    const parts = raw.split(/\s*(?:->|→|➔)\s*/);
    const decode = (code) => {
      const key = String(code || '').trim().toUpperCase();
      return VECTOR_TOOLTIPS[key] || key;
    };
    if (parts.length === 2) {
      return `${decode(parts[0])} → ${decode(parts[1])}`;
    }
    return decode(raw);
  }

  // Asymétrie Hybride 3 + 3 (alignée SSOT v6.2 / A20)
  const PEUPLE_ACCESSORIES_V62 = {
    H: {
      code: 'H',
      tier: 'ACTIF_TOUR_1',
      tierLabel: 'Actif dès le Tour 1',
      shortTag: '🥁 Tambour & Chant',
      materiel: '2 pions Chamanes recto-verso uniquement (1 Tambour et 1 Chant) + 2 Fiches d’archétype.',
      regle: 'Binôme auto-vérifiant : le Tambour peut se poser dès le 1er temps sur n’importe quel rayon ; à l’ouverture, si un Rêve portant le Chant annule au moins 1 machine sans autre machine active sur son rang, il glisse aussitôt d’1 rang vers la gauche.',
      producesStates: ['TAMBOUR', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION'],
      lightsIcons: ['ICONE_PARADE', 'ICONE_REVE']
    },
    M: {
      code: 'M',
      tier: 'ACTIF_TOUR_1',
      tierLabel: 'Actif dès le Tour 1',
      shortTag: '⚔️ Jeton Duel',
      materiel: '1 jeton Duel recto-verso (Défi ↔ Territoire tenu).',
      regle: 'Posé ou déplacé face Défi avec un Défenseur Mammifère (figé avec le 2e pion). Parer sur sa parcelle le retourne sur Territoire tenu (bloque l’avancée aux rangs 3 et 6) ; une frappe non parée et non piégée le renvoie en réserve.',
      producesStates: ['DUEL', 'TERRITOIRE'],
      lightsIcons: ['ICONE_PARADE']
    },
    O: {
      code: 'O',
      tier: 'ACTIF_TOUR_1',
      tierLabel: 'Actif dès le Tour 1',
      shortTag: '🪶 Envol · Perchoir · Plume',
      materiel: '1 Dé d’Envol (1–6), 1 zone Perchoir de Vigie à plat devant le paravent, 1 jeton Plume de Vigie (Chaud ↔ Calme).',
      regle: 'Servi en dernier au sac, regarde jusqu’à 2 jetons, garde 1 et pose l’autre caché sur le Perchoir. Choisit secrètement min(D1, D2) ou son Dé d’Envol. Pose la Plume (Chaud/Calme) sous paravent fermé pour guider la table.',
      producesStates: ['PLUME', 'PERCHOIR', 'RANG_MACHINE'],
      lightsIcons: []
    },
    E: {
      code: 'E',
      tier: 'PROGRESSIF_TUILES',
      tierLabel: 'Progressif via tuiles',
      shortTag: '✨ Jetons d’Altération',
      materiel: 'Jetons d’Altération en réserve des Entités (max 1 par machine mobile).',
      regle: 'Posé sur une machine mobile via les tuiles Entités. À la prochaine ouverture où son jeton est révélé, retirez l’Altération : la machine compte dans m(r) mais recule d’1 parcelle sans frapper ce tour-ci.',
      producesStates: ['ALTEREE', 'POSITION_REVE', 'ANNULATION'],
      lightsIcons: ['ICONE_REVE']
    },
    R: {
      code: 'R',
      tier: 'PROGRESSIF_TUILES',
      tierLabel: 'Progressif via tuiles',
      shortTag: '🦷 4 Écailles & Croc',
      materiel: '4 jetons Sabotage « Écaille » (même gabarit que le sac) et 1 jeton Piège spécial « Croc » réutilisable.',
      regle: 'Révélée à l’ouverture, une Écaille allume l’icône Sabotage puis pose le Croc sur une parcelle ciblée. En attaque, le Croc cohabite avec un Piège ordinaire, pare en premier (allume Piégeage) puis revient en réserve Reptile.',
      producesStates: ['ECAILLE', 'CROC', 'SABOTAGE'],
      lightsIcons: ['ICONE_SABOTAGE', 'ICONE_PIEGEAGE']
    },
    I: {
      code: 'I',
      tier: 'PROGRESSIF_TUILES',
      tierLabel: 'Progressif via tuiles',
      shortTag: '🪲 Essaim · Nids · ±1',
      materiel: 'Jetons Insectes double-face et Nids M1–M5 (exclusifs aux parties avec les Insectes).',
      regle: 'Production des Nids (+1/+2), Migration radiale et vers les pistes centrales, Déviation de dé ±1 (allume Insecte), Parade Insecte, Bouclier de lisière facultatif gouverné par I et descente sur place au ménage d’un Insecte passager.',
      producesStates: ['INSECTE', 'NID', 'INSECTE_RANG'],
      lightsIcons: ['ICONE_INSECTE']
    }
  };

  // Tronc commun v6.2 (sources natives du socle)
  const CORE_SOCLE_ACCESSORY = {
    code: 'SOCLE',
    name: 'Tronc commun v6.2',
    icon: '🌿',
    shortTag: 'Forêt 10×N · Furtivité · Sac opaque',
    producesStates: ['SOUCHE', 'ROUGE', 'MOBILISATION', 'PIEGE', 'SABOTAGE', 'DEFENSEUR_ATTENTE', 'GARDIEN'],
    lightsIcons: ['ICONE_PARADE', 'ICONE_PIEGEAGE', 'ICONE_SABOTAGE']
  };

  // Les 3 lisières 100 % fluides issues de la géométrie 2K3 (EHR / IMO)
  const LISIERES_100PC_FLUIDES = new Set(['E-O', 'O-E', 'H-M', 'M-H', 'R-I', 'I-R']);

  // Groupes de lisières pour le Mode 1 (15 duos face-à-face)
  const BORDER_GROUPS_V62 = [
    {
      id: 'animal-animal',
      title: '3 lisières Animal – Animal',
      subtitle: '6 Gardiens purs — chaque paire porte 1 Catalyseur d’Éveil (règle ii)',
      pairs: [
        ['M', 'R'],
        ['M', 'O'],
        ['R', 'O']
      ]
    },
    {
      id: 'animal-autre',
      title: '9 ponts Animal – Autre',
      subtitle: '9 Gardiens face à 6 Rêves & 3 Nids — ponts entre Éveil, Sommeil et Essaim',
      pairs: [
        ['M', 'H'],
        ['M', 'E'],
        ['M', 'I'],
        ['R', 'H'],
        ['R', 'E'],
        ['R', 'I'],
        ['O', 'H'],
        ['O', 'E'],
        ['O', 'I']
      ]
    },
    {
      id: 'sans-animal',
      title: '3 lisières sans Animal (A = 0)',
      subtitle: '4 Rêves & 2 Nids autonomes — 100 % jouables sans Piste des Gardiens (table N3-HEI)',
      pairs: [
        ['H', 'E'],
        ['H', 'I'],
        ['E', 'I']
      ]
    }
  ];

  // Tables témoins clés pour le Mode 2
  const PRESET_ASSISES = [
    { key: 'N3-HEI', peuples: ['H', 'E', 'I'], label: 'N3-HEI', tag: 'A=0 · Sans Animaux' },
    { key: 'N3-ERI', peuples: ['E', 'R', 'I'], label: 'N3-ERI', tag: 'Entités sans H' },
    { key: 'N3-HER', peuples: ['H', 'E', 'R'], label: 'N3-HER', tag: 'Triangle EHR · 3 Twists' },
    { key: 'N3-MRO', peuples: ['M', 'R', 'O'], label: 'N3-MRO', tag: '100 % Animaux' },
    { key: 'N3-MOI', peuples: ['M', 'O', 'I'], label: 'N3-MOI', tag: 'Triangle IMO · 3 Twists' },
    { key: 'N4-MROI', peuples: ['M', 'R', 'O', 'I'], label: 'N4-MROI', tag: 'Sans Rêves' },
    { key: 'N4-HEMR', peuples: ['H', 'E', 'M', 'R'], label: 'N4-HEMR', tag: 'Mixte 4J' },
    { key: 'N6-HEMROI', peuples: ['H', 'E', 'M', 'R', 'O', 'I'], label: 'N6-HEMROI', tag: 'Table complète 6J' }
  ];

  // Vivier candidats Phase 5 (Profils B / C pré-câblés — miroir de tiles_canon_v6_2.json)
  const DEFAULT_VIVIER_PHASE_5 = [
    {
      slots: ['R5', 'R1'],
      cible: 'R5 (H>O) ou R1 (H>E) · Profil C (Twist)',
      origine: 'P2 R8 / P1 R1',
      concept: 'Le piston du Rêve qui cède du terrain : reculer ce Rêve d’1 case à droite pour faire glisser un autre Rêve de 2 cases à gauche (100 % sûr chez H grâce au Chamane Chant).'
    },
    {
      slots: ['G6'],
      cible: 'G6 (O>R) · Profil C (Twist)',
      origine: 'P2 G6',
      concept: 'Réaffecter le rang d’une machine révélée n’ayant pas encore frappé à la valeur exacte du Dé d’Envol (franchissement Assaut → Charge en Acte 2).'
    },
    {
      slots: ['M2', 'M4'],
      cible: 'M2 (I>R) ou M4 (I>H) · Profil C (Twist)',
      origine: 'P1 M2',
      concept: 'La Termitière itinérante (tuile nomade) : après production, déplacer ce Nid avec 1 de ses Insectes vers une autre parcelle libre, en laissant le Défenseur garder le départ.'
    },
    {
      slots: ['G8', 'G13'],
      cible: 'G8 (M>E) ou G13 (M>I) · Profil B/C',
      origine: 'P1 G13',
      concept: 'Échange atomique de position entre le jeton Duel (en conservant sa face Territoire tenu) et un groupe de pions/Insectes sur une autre parcelle.'
    },
    {
      slots: ['G11'],
      cible: 'G11 (O>H) · Profil B',
      origine: 'P1 G11',
      concept: 'Déplacer 1 Piège vers le rayon de la Plume ou défausser ce Piège pour glisser un Défenseur encore en pari dans une encoche de son Gardien.'
    },
    {
      slots: ['G3'],
      cible: 'G3 (M>O) · Profil B',
      origine: 'P0 G3',
      concept: 'La clairière sans machine : projeter un Défenseur depuis une lisière ou rive de Furtivité en franchissant toute suite continue de parcelles sans machine.'
    },
    {
      slots: ['R9'],
      cible: 'R9 (E>O) · Profil B',
      origine: 'P1 R9',
      concept: 'La mesure du ciel : rapprocher un Rêve d’1 ou 2 cases vers la valeur indiquée par le Dé d’Envol.'
    },
    {
      slots: ['R3'],
      cible: 'R3 (H>M) · Profil B',
      origine: 'P1 R3',
      concept: 'La peau du Tambour : sur la parcelle du jeton Duel, le Chamane Tambour pare à lui seul une frappe d’Abatteuse (faisant basculer le Défi en Territoire tenu).'
    }
  ];

  // Couleurs hexadécimales SVG par Peuple
  const PEUPLE_SVG_COLORS = {
    M: { fill: '#fef3c7', stroke: '#d97706', text: '#92400e', accent: '#b45309' },
    R: { fill: '#d1fae5', stroke: '#059669', text: '#065f46', accent: '#047857' },
    O: { fill: '#e0f2fe', stroke: '#0284c7', text: '#075985', accent: '#0369a1' },
    H: { fill: '#ffe4e6', stroke: '#e11d48', text: '#9f1239', accent: '#be123c' },
    E: { fill: '#ede9fe', stroke: '#7c3aed', text: '#5b21b6', accent: '#6d28d9' },
    I: { fill: '#ecfccb', stroke: '#65a30d', text: '#3f6212', accent: '#4d7c0f' }
  };

  // Ponts sémantiques d'états physiques (Sortie -> Entrées compatibles)
  const STATE_OUTPUT_TO_INPUTS = {
    TERRITOIRE: ['DUEL'],
    INSECTE_PASSAGER: ['INSECTE'],
    INSECTE_RANG: ['INSECTE'],
    NID_ACTIVE: ['INSECTE', 'NID'],
    RANG_REVE: ['POSITION_REVE']
  };

  // Ponts sorties physiques -> icônes Gardiens v6.2 amorçables en partie
  const STATE_OUTPUT_TO_GUARDIAN_ICONS = {
    SABOTAGE: ['ICONE_SABOTAGE'],
    ECAILLE: ['ICONE_SABOTAGE'],
    PIEGE: ['ICONE_PIEGEAGE'],
    CROC: ['ICONE_PIEGEAGE'],
    ANNULATION: ['ICONE_REVE'],
    RANG_REVE: ['ICONE_REVE'],
    INSECTE: ['ICONE_INSECTE'],
    INSECTE_PASSAGER: ['ICONE_INSECTE'],
    INSECTE_RANG: ['ICONE_INSECTE'],
    NID_ACTIVE: ['ICONE_INSECTE'],
    DEFENSEUR_REDEPLOYE: ['ICONE_PARADE'],
    BLEU: ['ICONE_PARADE']
  };

  // --------------------------------------------------------------------------
  // État interne de l'Explorateur
  // --------------------------------------------------------------------------
  const explorerState = {
    mode: 'lisieres',          // 'lisieres' | 'assises' | 'peuples'
    activePeupleTab: 'H',      // 'H' | 'E' | 'M' | 'R' | 'O' | 'I'
    xrayFocusId: null,         // tileId | null
    capotOpenIds: new Set(),   // Set<tileId>
    allCapotsOpen: false,
    readingGuideOpen: false,   // Panneau Guide de lecture fermé par défaut
    wheelSelection: null,      // null | { kind: 'peuple', code } | { kind: 'border', p1, p2 }
    filters: {
      search: '',
      family: 'ALL',
      peuple: 'ALL',
      role: 'ALL',
      icon: 'ALL',
      stateToken: 'ALL',
      inCircleOnly: false
    },
    escapeBound: false
  };

  // Cache combinatoire des 197 assises
  let _cached197 = null;
  let _cached197ByKey = null;

  // --------------------------------------------------------------------------
  // Accès sécurisé aux données globales
  // --------------------------------------------------------------------------
  function getCatalogue() {
    if (typeof global.CATALOGUE_TUILES !== 'undefined' && global.CATALOGUE_TUILES) {
      return global.CATALOGUE_TUILES;
    }
    if (typeof CATALOGUE_TUILES !== 'undefined') return CATALOGUE_TUILES;
    return {};
  }

  function getPeuplesMap() {
    if (typeof global.PEUPLES !== 'undefined' && global.PEUPLES) return global.PEUPLES;
    if (typeof PEUPLES !== 'undefined') return PEUPLES;
    return {};
  }

  function getMatricePaires() {
    if (typeof global.MATRICE_PAIRES !== 'undefined' && global.MATRICE_PAIRES) return global.MATRICE_PAIRES;
    if (typeof MATRICE_PAIRES !== 'undefined') return MATRICE_PAIRES;
    return {};
  }

  function getStudioState() {
    if (typeof global.state !== 'undefined' && global.state) return global.state;
    if (typeof state !== 'undefined') return state;
    return { peuplesCercle: ['M', 'R', 'O', 'H'], profileOverrides: {} };
  }

  function getCurrentCircle() {
    const st = getStudioState();
    if (st && Array.isArray(st.peuplesCercle) && st.peuplesCercle.length >= 3) {
      return st.peuplesCercle.slice();
    }
    return ['M', 'R', 'O', 'H'];
  }

  function escapeHtml(str) {
    return String(str === null || str === undefined ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  const FALLBACK_REPTILE_ICON_INNER_SVG =
    '<path d="M1.8 14.4L4.2 9.4L6.8 6.4L9.2 7.5L11.3 5.5L13.5 8.1L21.5 9.6C22.4 9.8 22.6 11.7 21.6 12.2L13.2 13L20.8 15.2C21.2 16.2 20.1 17.6 18.2 18.1C12.8 19.3 6.8 19.3 1.8 17.6Z" fill="#10b981" stroke="#064e3b" stroke-width="1.5" stroke-linejoin="round"/>' +
    '<path d="M12.8 12.9L21 12.3L20.2 15.1L12.8 12.9Z" fill="#064e3b"/>' +
    '<path d="M14.2 12.7L15.4 14.8L16.6 12.5M17.5 12.4L18.7 14.5L19.9 12.2" fill="#ffffff" stroke="#064e3b" stroke-width="0.7" stroke-linejoin="round"/>' +
    '<path d="M3.8 16.5C8.2 17.6 13.4 17.6 18 16.5" fill="none" stroke="#a7f3d0" stroke-width="1.2" stroke-linecap="round"/>' +
    '<circle cx="9.6" cy="9.9" r="2.3" fill="#fbbf24" stroke="#064e3b" stroke-width="1.1"/>' +
    '<ellipse cx="9.8" cy="9.9" rx="0.65" ry="1.5" fill="#064e3b"/>' +
    '<circle cx="19.6" cy="10.4" r="0.9" fill="#064e3b"/>';

  function getTileIllustrationsModule() {
    if (typeof global.AmazoniaTileIllustrationsV62 !== 'undefined' && global.AmazoniaTileIllustrationsV62) {
      return global.AmazoniaTileIllustrationsV62;
    }
    return null;
  }

  function renderPeupleIconHtml(code, fallbackIcon, size) {
    if (code === 'R') {
      const mod = getTileIllustrationsModule();
      const px = Number(size) > 0 ? Number(size) : 14;
      if (mod && typeof mod.getReptileIconSvg === 'function') {
        return mod.getReptileIconSvg(px);
      }
      return (
        `<svg xmlns="http://www.w3.org/2000/svg" class="exp-peuple-icon-svg exp-peuple-icon-R" ` +
        `data-peuple-icon="R" width="${px}" height="${px}" viewBox="0 0 24 24" ` +
        `role="img" aria-label="Reptiles" focusable="false">${FALLBACK_REPTILE_ICON_INNER_SVG}</svg>`
      );
    }
    return fallbackIcon || '';
  }

  function renderPeupleWheelIconSvg(code, fallbackIcon, cx, cy) {
    if (code === 'R') {
      const mod = getTileIllustrationsModule();
      if (mod && typeof mod.getReptileWheelIconSvg === 'function') {
        return mod.getReptileWheelIconSvg(cx, cy, 20);
      }
      return (
        `<svg class="exp-wheel-peuple-icon exp-peuple-icon-R" data-peuple-icon="R" ` +
        `x="${(cx - 10).toFixed(1)}" y="${(cy - 26).toFixed(1)}" width="20" height="20" ` +
        `viewBox="0 0 24 24" aria-hidden="true">${FALLBACK_REPTILE_ICON_INNER_SVG}</svg>`
      );
    }
    return `<text x="${cx.toFixed(1)}" y="${(cy - 9).toFixed(1)}" text-anchor="middle" font-size="17">${fallbackIcon}</text>`;
  }

  function getPeupleSelectOptionIcon(code, fallbackIcon) {
    if (code === 'R') return '🦎';
    return fallbackIcon || '';
  }

  function renderTileMedallionHtml(tileId) {
    const mod = getTileIllustrationsModule();
    if (!mod || typeof mod.getTileIllustrationSvg !== 'function') return '';
    const svg = mod.getTileIllustrationSvg(tileId);
    if (!svg) return '';
    return `<div class="exp-tile-medallion" data-tile-illustration="${escapeHtml(tileId)}" aria-hidden="true">${svg}</div>`;
  }

  function stripHtml(str) {
    return String(str || '').replace(/<[^>]+>/g, '').trim();
  }

  function countWordsStrict(text) {
    const clean = stripHtml(text)
      .replace(/^\s*(?:Face\s+[12]|Enraciné|En\s+Parade|En\s+Migration)\s*:\s*/i, '')
      .trim();
    const matches = clean.match(/[0-9A-Za-zÀ-ÖØ-öø-ÿ]+/g);
    return matches ? matches.length : 0;
  }

  function getTileProfile(tileId) {
    const cat = getCatalogue();
    const tile = cat[tileId];
    if (!tile || !tile.profils) return null;
    const st = getStudioState();
    const pref = (st && st.profileOverrides && st.profileOverrides[tileId]) || 'A';
    return tile.profils[pref] || tile.profils.A || Object.values(tile.profils)[0] || null;
  }

  function getTileNeighbor(tile) {
    if (!tile || !Array.isArray(tile.couple)) return '';
    return tile.couple.find(c => c !== tile.origine) || tile.couple[1] || '';
  }

  function getStateMeta(token) {
    const key = String(token || '').toUpperCase();
    return STATE_META[key] || { icon: '🔹', label: key, group: 'Autre' };
  }

  function getNormalizedTileTriggers(tileId) {
    const prof = getTileProfile(tileId);
    if (!prof || !Array.isArray(prof.declencheurs_amorces)) return [];
    const seen = new Set();
    const result = [];
    for (const raw of prof.declencheurs_amorces) {
      const norm = normalizeDeclencheurToIconId(raw);
      if (norm && !seen.has(norm)) {
        seen.add(norm);
        result.push(norm);
      }
    }
    return result;
  }

  function getTileRoleFlags(tileId) {
    const tile = getCatalogue()[tileId];
    const prof = getTileProfile(tileId);
    if (!tile || !prof) {
      return {
        isTwist: false,
        isLoi: false,
        isCatalyseur: false,
        isLevier: false,
        isEnracinement: false,
        isAutonomeA0: false,
        isFluide: true
      };
    }
    const tags = Array.isArray(prof.tags) ? prof.tags : [];
    const rolesTxt = (Array.isArray(prof.role_porte) ? prof.role_porte : []).join(' ').toLowerCase();
    const isTwist = Boolean(prof.est_twist_canon0);
    const isLoi = prof.nature === 'loi_passive' || tags.includes('LOI_PASSIVE');
    const isCatalyseur = tags.includes('CATALYSEUR_EVEIL') || rolesTxt.includes('catalyseur');
    const isLevier = tags.includes('LEVIER_REVE') || rolesTxt.includes('levier');
    const isEnracinement = tags.includes('ENRACINEMENT') || rolesTxt.includes('enracinement');
    const isAutonomeA0 = tags.includes('A0') || rolesTxt.includes('a = 0') || rolesTxt.includes('a=0');
    const isFluide = !isTwist && !isLoi;
    return {
      isTwist,
      isLoi,
      isCatalyseur,
      isLevier,
      isEnracinement,
      isAutonomeA0,
      isFluide
    };
  }

  function getVivierPistesForSlot(tileId) {
    if (
      typeof global.VIVIER_CANDIDATS_B_C_PHASE_5 !== 'undefined' &&
      global.VIVIER_CANDIDATS_B_C_PHASE_5 &&
      Array.isArray(global.VIVIER_CANDIDATS_B_C_PHASE_5.pistes_retenues)
    ) {
      const re = new RegExp('\\b' + tileId + '\\b');
      return global.VIVIER_CANDIDATS_B_C_PHASE_5.pistes_retenues
        .filter(p => re.test(String(p.emplacement_cible || '')))
        .map(p => ({
          cible: p.emplacement_cible,
          origine: p.origine || 'Vivier',
          concept: p.concept || ''
        }));
    }
    return DEFAULT_VIVIER_PHASE_5.filter(item => item.slots.includes(tileId));
  }

  // --------------------------------------------------------------------------
  // Moteur géométrique des 197 Assises uniques (groupe diédral D_N)
  // --------------------------------------------------------------------------
  function compareSeqByCanonOrder(a, b) {
    const len = Math.min(a.length, b.length);
    for (let i = 0; i < len; i++) {
      const ra = PEUPLE_CANON_ORDER.indexOf(a[i]);
      const rb = PEUPLE_CANON_ORDER.indexOf(b[i]);
      if (ra !== rb) return ra - rb;
    }
    return a.length - b.length;
  }

  function getCanonicalSequence(circle) {
    const arr = (circle || []).filter(p => PEUPLE_CANON_ORDER.includes(p));
    const n = arr.length;
    if (n === 0) return [];
    let best = null;
    const candidates = [arr, arr.slice().reverse()];
    for (const seq of candidates) {
      for (let shift = 0; shift < n; shift++) {
        const rot = seq.slice(shift).concat(seq.slice(0, shift));
        if (!best || compareSeqByCanonOrder(rot, best) < 0) {
          best = rot;
        }
      }
    }
    return best || arr;
  }

  function enumerateAll197Assises() {
    if (_cached197) return _cached197;
    const all = [];

    function combinations(arr, k, start, current, out) {
      if (current.length === k) {
        out.push(current.slice());
        return;
      }
      for (let i = start; i <= arr.length - (k - current.length); i++) {
        current.push(arr[i]);
        combinations(arr, k, i + 1, current, out);
        current.pop();
      }
    }

    function permutations(arr, used, current, out) {
      if (current.length === arr.length) {
        out.push(current.slice());
        return;
      }
      for (let i = 0; i < arr.length; i++) {
        if (used[i]) continue;
        used[i] = true;
        current.push(arr[i]);
        permutations(arr, used, current, out);
        current.pop();
        used[i] = false;
      }
    }

    let globalIdx = 1;
    for (let n = 3; n <= 6; n++) {
      const subsets = [];
      combinations(PEUPLE_CANON_ORDER, n, 0, [], subsets);
      for (const sub of subsets) {
        // Fixer le 1er élément (plus petit dans PEUPLE_CANON_ORDER) supprime les rotations
        const first = sub[0];
        const rest = sub.slice(1);
        const perms = [];
        permutations(rest, new Array(rest.length).fill(false), [], perms);
        for (const perm of perms) {
          // Briser la symétrie miroir : voisin droit < voisin gauche
          if (PEUPLE_CANON_ORDER.indexOf(perm[0]) < PEUPLE_CANON_ORDER.indexOf(perm[perm.length - 1])) {
            const seq = [first].concat(perm);
            const key = 'N' + n + '-' + seq.join('');
            all.push({
              index: globalIdx++,
              n,
              key,
              peuples: seq
            });
          }
        }
      }
    }

    _cached197 = all;
    _cached197ByKey = Object.fromEntries(all.map(item => [item.key, item]));
    return _cached197;
  }

  function canonicalizeAssise(peuples) {
    const all = enumerateAll197Assises();
    const canon = getCanonicalSequence(peuples);
    const n = canon.length;
    const key = 'N' + n + '-' + canon.join('');
    const found = _cached197ByKey ? _cached197ByKey[key] : all.find(a => a.key === key);
    return {
      key,
      canon,
      n,
      index: found ? found.index : null,
      total: all.length
    };
  }

  function getAssiseTilesAndBorders(peuples) {
    const circle = Array.isArray(peuples) && peuples.length >= 3 ? peuples.slice() : getCurrentCircle();
    const n = circle.length;
    const matrice = getMatricePaires();
    const borders = [];
    const tileIds = [];
    for (let i = 0; i < n; i++) {
      const p1 = circle[i];
      const p2 = circle[(i + 1) % n];
      const pair = matrice[p1 + '_' + p2] || [];
      borders.push({
        index: i + 1,
        p1,
        p2,
        key: p1 + '-' + p2,
        tuiles: pair.slice(),
        is100pcFluide: LISIERES_100PC_FLUIDES.has(p1 + '-' + p2)
      });
      for (const tid of pair) {
        if (!tileIds.includes(tid)) tileIds.push(tid);
      }
    }
    const canonInfo = canonicalizeAssise(circle);
    return {
      circle,
      n,
      canonKey: canonInfo.key,
      assiseIndex: canonInfo.index,
      borders,
      tileIds
    };
  }

  // --------------------------------------------------------------------------
  // Moteur de Synergies & Rayons X (états physiques + bus des 6 icônes v6.2)
  // --------------------------------------------------------------------------
  function getTileEffectiveIconTriggers(tileId) {
    const tile = getCatalogue()[tileId];
    const prof = getTileProfile(tileId);
    if (!tile || !prof) return [];
    const icons = new Set(getNormalizedTileTriggers(tileId));
    for (const out of (prof.sorties || [])) {
      const mapped = STATE_OUTPUT_TO_GUARDIAN_ICONS[out];
      if (mapped) {
        for (const ic of mapped) icons.add(ic);
      }
    }
    // Tout Rêve défendu peut annuler une machine (ICONE_REVE)
    if (tile.famille === 'REVE') {
      icons.add('ICONE_REVE');
    }
    return Array.from(icons);
  }

  function computeDirectedLink(srcId, dstId) {
    if (srcId === dstId) return null;
    const cat = getCatalogue();
    const srcTile = cat[srcId];
    const dstTile = cat[dstId];
    const srcProf = getTileProfile(srcId);
    const dstProf = getTileProfile(dstId);
    if (!srcTile || !dstTile || !srcProf || !dstProf) return null;

    const srcOuts = Array.isArray(srcProf.sorties) ? srcProf.sorties : [];
    const dstIns = Array.isArray(dstProf.entrees) ? dstProf.entrees : [];
    const dstInSet = new Set(dstIns);

    const stateBridges = [];
    for (const out of srcOuts) {
      if (dstInSet.has(out)) {
        stateBridges.push(out);
      }
      const mapped = STATE_OUTPUT_TO_INPUTS[out] || [];
      for (const targetIn of mapped) {
        if (dstInSet.has(targetIn) && !stateBridges.includes(out + '→' + targetIn)) {
          stateBridges.push(targetIn);
        }
      }
    }
    // Un Gardien en piste nourrit l'entrée GARDIEN (G4 Ara)
    if (srcTile.famille === 'GARDIEN' && dstInSet.has('GARDIEN') && !stateBridges.includes('GARDIEN')) {
      stateBridges.push('GARDIEN');
    }

    const iconBridges = [];
    if (dstTile.famille === 'GARDIEN' && dstProf.cablage_recommande) {
      const targetIcon = normalizeDeclencheurToIconId(dstProf.cablage_recommande);
      if (targetIcon) {
        const srcIcons = getTileEffectiveIconTriggers(srcId);
        if (srcIcons.includes(targetIcon)) {
          iconBridges.push(targetIcon);
        }
      }
    }

    const uniqueStates = Array.from(new Set(stateBridges));
    const uniqueIcons = Array.from(new Set(iconBridges));
    if (uniqueStates.length === 0 && uniqueIcons.length === 0) return null;

    return {
      source: srcId,
      target: dstId,
      states: uniqueStates,
      icons: uniqueIcons,
      kind: uniqueStates.length > 0 ? (uniqueIcons.length > 0 ? 'HYBRID' : 'STATE') : 'BUS'
    };
  }

  function computeXRayGraph(focusId, scopeTileIds, scopeOptions) {
    const cat = getCatalogue();
    const focusTile = cat[focusId];
    const focusProf = getTileProfile(focusId);
    const opts = scopeOptions || {};
    if (!focusTile || !focusProf) {
      return {
        focusId: null,
        scopeLabel: opts.scopeLabel || null,
        upstreamAccessories: [],
        upstreamTiles: [],
        downstreamTiles: [],
        byTileId: {}
      };
    }

    const allIds = Array.isArray(scopeTileIds) && scopeTileIds.length > 0
      ? scopeTileIds
      : Object.keys(cat);
    const allowedPeuples = Array.isArray(opts.activePeuples) && opts.activePeuples.length > 0
      ? new Set(opts.activePeuples)
      : null;
    const activeModules = opts.activeModules || null;

    const focusInputs = new Set(focusProf.entrees || []);
    const focusCab = focusTile.famille === 'GARDIEN'
      ? normalizeDeclencheurToIconId(focusProf.cablage_recommande)
      : null;

    // 1) Accessoires 3+3 et Socle en Amont
    const upstreamAccessories = [];
    const peuplesMap = getPeuplesMap();
    for (const pCode of PEUPLE_CANON_ORDER) {
      if (allowedPeuples && !allowedPeuples.has(pCode)) continue;
      const acc = PEUPLE_ACCESSORIES_V62[pCode];
      const matchedStates = acc.producesStates.filter(s => focusInputs.has(s));
      const matchedIcons = focusCab && acc.lightsIcons.includes(focusCab) ? [focusCab] : [];
      if (matchedStates.length > 0 || matchedIcons.length > 0) {
        const pInfo = peuplesMap[pCode] || { icon: '', nom: pCode };
        upstreamAccessories.push({
          code: pCode,
          name: pInfo.nom || pCode,
          icon: pInfo.icon || '',
          shortTag: acc.shortTag,
          states: matchedStates,
          icons: matchedIcons
        });
      }
    }
    const coreStates = CORE_SOCLE_ACCESSORY.producesStates.filter(s => focusInputs.has(s));
    const coreIcons = focusCab && CORE_SOCLE_ACCESSORY.lightsIcons.includes(focusCab) ? [focusCab] : [];
    if (coreStates.length > 0 || coreIcons.length > 0) {
      upstreamAccessories.push({
        code: 'SOCLE',
        name: CORE_SOCLE_ACCESSORY.name,
        icon: CORE_SOCLE_ACCESSORY.icon,
        shortTag: CORE_SOCLE_ACCESSORY.shortTag,
        states: coreStates,
        icons: coreIcons
      });
    }

    function filterLinkForModules(link) {
      if (!link) return null;
      if (!activeModules) return link;
      const validIcons = activeModules.essaim
        ? link.icons
        : link.icons.filter(ic => ic !== 'ICONE_INSECTE');
      const finalIcons = activeModules.gardiens ? validIcons : [];
      if (link.states.length === 0 && finalIcons.length === 0) return null;
      return {
        source: link.source,
        target: link.target,
        states: link.states,
        icons: finalIcons,
        kind: link.states.length > 0 ? (finalIcons.length > 0 ? 'HYBRID' : 'STATE') : 'BUS'
      };
    }

    // 2) Tuiles Amont et Tuiles Aval
    const upstreamTiles = [];
    const downstreamTiles = [];
    const byTileId = {};
    byTileId[focusId] = { role: 'focus', upReasons: [], downReasons: [] };

    for (const otherId of allIds) {
      if (otherId === focusId) continue;
      const upLink = filterLinkForModules(computeDirectedLink(otherId, focusId));
      const downLink = filterLinkForModules(computeDirectedLink(focusId, otherId));

      if (upLink) upstreamTiles.push(upLink);
      if (downLink) downstreamTiles.push(downLink);

      if (upLink || downLink) {
        byTileId[otherId] = {
          role: upLink && downLink ? 'both' : (upLink ? 'upstream' : 'downstream'),
          upLink: upLink || null,
          downLink: downLink || null
        };
      }
    }

    return {
      focusId,
      scopeLabel: opts.scopeLabel || null,
      upstreamAccessories,
      upstreamTiles,
      downstreamTiles,
      byTileId
    };
  }

  function computeMaximumMatchingCount(tileIds, edges) {
    // Couplage maximal par recherche augmentante sur graphe non orienté des paires liées
    const adj = new Map();
    for (const id of tileIds) adj.set(id, new Set());
    for (const e of edges) {
      if (adj.has(e.source) && adj.has(e.target) && e.source !== e.target) {
        adj.get(e.source).add(e.target);
        adj.get(e.target).add(e.source);
      }
    }
    // Pour N <= 6 (au plus 12 tuiles), heuristique degré min + amélioration exhaustive sûre
    const used = new Set();
    let count = 0;
    const sorted = tileIds.slice().sort((a, b) => adj.get(a).size - adj.get(b).size);
    for (const u of sorted) {
      if (used.has(u)) continue;
      const neighbors = Array.from(adj.get(u)).filter(v => !used.has(v));
      if (neighbors.length === 0) continue;
      neighbors.sort((a, b) => adj.get(a).size - adj.get(b).size);
      used.add(u);
      used.add(neighbors[0]);
      count++;
    }
    return count;
  }

  function computeAssiseHealth(peuples) {
    const info = getAssiseTilesAndBorders(peuples);
    const circleSet = new Set(info.circle);
    const cat = getCatalogue();

    const animalCount = info.circle.filter(p => ANIMAL_PEUPLES.has(p)).length;
    const hasH = circleSet.has('H');
    const hasE = circleSet.has('E');
    const hasI = circleSet.has('I');

    const modules = {
      gardiens: animalCount >= 1,
      reves: hasH || hasE,
      essaim: hasI
    };

    const twists = [];
    const loisPassives = [];
    const catalyseursEveil = [];
    const leviersReve = [];
    const enracinements = [];
    const autonomesA0 = [];
    let guardiansCount = 0;
    let revesCount = 0;
    let nidsCount = 0;

    for (const tid of info.tileIds) {
      const tile = cat[tid];
      if (!tile) continue;
      if (tile.famille === 'GARDIEN') guardiansCount++;
      else if (tile.famille === 'REVE') revesCount++;
      else if (tile.famille === 'CROISSANCE') nidsCount++;

      const flags = getTileRoleFlags(tid);
      if (flags.isTwist) twists.push(tid);
      if (flags.isLoi) loisPassives.push(tid);
      if (flags.isCatalyseur) catalyseursEveil.push(tid);
      if (flags.isLevier) leviersReve.push(tid);
      if (flags.isEnracinement) enracinements.push(tid);
      if (flags.isAutonomeA0) autonomesA0.push(tid);
    }

    // Couverture des 6 icônes Gardiens dans l'ordre v6.2
    const iconCoverage = GUARDIAN_ICONS_V62.map(ic => {
      const active = modules.gardiens && (ic.id !== 'ICONE_INSECTE' || modules.essaim);
      const recommendedGuardians = [];
      const triggerSources = [];
      for (const tid of info.tileIds) {
        const tile = cat[tid];
        const prof = getTileProfile(tid);
        if (!tile || !prof) continue;
        if (tile.famille === 'GARDIEN' && normalizeDeclencheurToIconId(prof.cablage_recommande) === ic.id) {
          recommendedGuardians.push(tid);
        }
        const trigs = getTileEffectiveIconTriggers(tid);
        if (trigs.includes(ic.id)) {
          triggerSources.push(tid);
        }
        if (ic.id === 'ICONE_RESONANCE' && tile.famille === 'GARDIEN' && !triggerSources.includes(tid)) {
          triggerSources.push(tid);
        }
      }
      return {
        id: ic.id,
        pos: ic.pos,
        label: ic.label,
        icon: ic.icon,
        active,
        recommendedGuardians,
        triggerSources
      };
    });

    // Chaînes de synergie majeures constructibles sur cette table
    const synergyChains = [];
    for (const srcId of info.tileIds) {
      for (const dstId of info.tileIds) {
        if (srcId === dstId) continue;
        const link = computeDirectedLink(srcId, dstId);
        if (!link) continue;
        // Sur une table sans I, filtrer d'éventuels liens ICONE_INSECTE
        const validIcons = modules.essaim
          ? link.icons
          : link.icons.filter(ic => ic !== 'ICONE_INSECTE');
        if (link.states.length === 0 && validIcons.length === 0) continue;
        // Sur une table sans Gardiens, pas de liens vers Gardiens
        if (!modules.gardiens && cat[dstId] && cat[dstId].famille === 'GARDIEN') continue;
        const bridgeLabels = link.states
          .map(s => getStateMeta(s).icon + ' ' + getStateMeta(s).label)
          .concat(
            validIcons.map(icId => {
              const ic = GUARDIAN_ICON_BY_ID[icId];
              return ic ? '★' + ic.icon + ' ' + ic.label : icId;
            })
          );
        synergyChains.push({
          source: srcId,
          target: dstId,
          kind: link.states.length > 0 ? (validIcons.length > 0 ? 'HYBRID' : 'STATE') : 'BUS',
          states: link.states,
          icons: validIcons,
          bridges: bridgeLabels,
          label: srcId + ' ➔ ' + bridgeLabels.join(' · ') + ' ➔ ' + dstId
        });
      }
    }

    // Trier : liens d'états physiques d'abord, puis bus Gardiens
    synergyChains.sort((a, b) => {
      const rank = k => (k === 'HYBRID' ? 0 : (k === 'STATE' ? 1 : 2));
      if (rank(a.kind) !== rank(b.kind)) return rank(a.kind) - rank(b.kind);
      return a.source.localeCompare(b.source) || a.target.localeCompare(b.target);
    });

    const loisAlert = loisPassives.length > 2;
    const catalyseurAlert = animalCount >= 1 && catalyseursEveil.length === 0;
    const levierAlert = hasE && !hasH && leviersReve.length === 0;

    const alerts = [];
    if (loisAlert) {
      alerts.push({ level: 'alert', text: `Trop de lois passives (${loisPassives.length} > 2)` });
    }
    if (catalyseurAlert) {
      alerts.push({ level: 'alert', text: 'Aucun Catalyseur d’Éveil alors qu’au moins 1 Peuple Animal joue' });
    }
    if (levierAlert) {
      alerts.push({ level: 'alert', text: 'Aucun Levier de Rêve alors que E joue sans H' });
    }

    return {
      circle: info.circle,
      n: info.n,
      canonKey: info.canonKey,
      assiseIndex: info.assiseIndex,
      borders: info.borders,
      tileIds: info.tileIds,
      animalCount,
      hasH,
      hasE,
      hasI,
      guardiansCount,
      revesCount,
      nidsCount,
      modules,
      twists,
      loisPassives,
      loisAlert,
      catalyseursEveil,
      catalyseurAlert,
      leviersReve,
      levierAlert,
      enracinements,
      autonomesA0,
      iconCoverage,
      synergyChains,
      disjointMajorCount: computeMaximumMatchingCount(info.tileIds, synergyChains),
      alerts
    };
  }

  // --------------------------------------------------------------------------
  // Preuve de divergence pour Mode 1 (15 Lisières face-à-face)
  // --------------------------------------------------------------------------
  function computeBorderDivergence(tileIdA, tileIdB) {
    const profA = getTileProfile(tileIdA);
    const profB = getTileProfile(tileIdB);
    const outsA = (profA && Array.isArray(profA.sorties)) ? profA.sorties : [];
    const outsB = (profB && Array.isArray(profB.sorties)) ? profB.sorties : [];
    const primaryOutA = outsA[0] || 'AUCUNE';
    const primaryOutB = outsB[0] || 'AUCUNE';
    const linkAB = computeDirectedLink(tileIdA, tileIdB);
    const linkBA = computeDirectedLink(tileIdB, tileIdA);
    const stateAB = linkAB && linkAB.states.length > 0;
    const stateBA = linkBA && linkBA.states.length > 0;
    let stateChain = null;
    if (stateAB && !stateBA) stateChain = `${tileIdA} ➔ ${tileIdB}`;
    else if (stateBA && !stateAB) stateChain = `${tileIdB} ➔ ${tileIdA}`;
    else if (stateAB && stateBA) stateChain = `${tileIdA} ↔ ${tileIdB}`;

    return {
      primaryOutA,
      primaryOutB,
      divergent: primaryOutA !== primaryOutB,
      stateChain,
      noStateLoop: !(stateAB && stateBA)
    };
  }

  // --------------------------------------------------------------------------
  // Parseur des faces joueur & compteurs de mots
  // --------------------------------------------------------------------------
  function parseTileFaces(tile, prof) {
    const raw = String((prof && prof.texte) || '');
    const parts = raw
      .split(/<br\s*\/?>/i)
      .map(s => s.trim())
      .filter(Boolean);
    const motsMap = (prof && prof.mots_par_face) || {};

    if (tile.famille === 'GARDIEN') {
      const f1Raw = parts[0] || raw;
      const f2Raw = parts[1] || '';
      const f1Body = f1Raw.replace(/^<strong>\s*Face\s*1\s*:\s*<\/strong>\s*/i, '');
      const f2Body = f2Raw.replace(/^<strong>\s*Face\s*2\s*:\s*<\/strong>\s*/i, '');
      const f1Words = (motsMap['Face 1'] && motsMap['Face 1'].mots) || countWordsStrict(f1Raw);
      const f2Words = (motsMap['Face 2'] && motsMap['Face 2'].mots) || countWordsStrict(f2Raw);
      return {
        kind: 'GARDIEN',
        faces: [
          { key: 'Face 1', label: 'Face 1', html: f1Body, words: f1Words, isFace2: false },
          { key: 'Face 2', label: 'Face 2 · Éveillé', html: f2Body, words: f2Words, isFace2: true }
        ],
        enracine: null
      };
    }

    let mainPart = parts[0] || raw;
    let enracPart = null;
    for (const p of parts) {
      if (/Enraciné\s*:/i.test(stripHtml(p))) {
        enracPart = p;
      } else if (p !== mainPart && !mainPart) {
        mainPart = p;
      }
    }

    let mainKey = 'Face unique';
    let mainLabel = tile.famille === 'REVE' ? 'Effet du Rêve' : 'Effet du Nid';
    if (/^<strong>\s*En\s+Parade\s*:/i.test(mainPart)) {
      mainKey = 'En Parade';
      mainLabel = 'Loi passive · En Parade';
      mainPart = mainPart.replace(/^<strong>\s*En\s+Parade\s*:\s*<\/strong>\s*/i, '');
    } else if (/^<strong>\s*En\s+Migration\s*:/i.test(mainPart)) {
      mainKey = 'En Migration';
      mainLabel = 'Loi passive · En Migration';
      mainPart = mainPart.replace(/^<strong>\s*En\s+Migration\s*:\s*<\/strong>\s*/i, '');
    }

    const mainWords = (motsMap[mainKey] && motsMap[mainKey].mots) || countWordsStrict(mainPart);
    let enracine = null;
    if (enracPart) {
      const enracBody = enracPart.replace(/^<strong>\s*Enraciné\s*:\s*<\/strong>\s*/i, '');
      const enracWords = (motsMap['Enraciné'] && motsMap['Enraciné'].mots) || countWordsStrict(enracPart);
      enracine = { label: '🌱 Enraciné', html: enracBody, words: enracWords };
    }

    return {
      kind: tile.famille,
      faces: [{ key: mainKey, label: mainLabel, html: mainPart, words: mainWords, isFace2: false }],
      enracine
    };
  }

  function getNaturalWindowBadges(tile, prof) {
    const fen = String((prof && prof.fenetre) || '').toUpperCase();
    const badges = [];
    if (fen.includes('OUVERTURE')) badges.push({ icon: '🌅', label: 'À l’ouverture' });
    if (fen.includes('PRODUCTION')) badges.push({ icon: '🪹', label: 'Après production' });
    if (fen.includes('LOI PARADE')) badges.push({ icon: '🛡️', label: 'En Parade' });
    if (fen.includes('LOI MIGRATION')) badges.push({ icon: '🪲', label: 'En Migration' });
    if (fen.includes('ENRACINEMENT')) badges.push({ icon: '🌱', label: 'Enracinement' });
    if (fen.includes('DÉCOMPTE FINAL') || fen.includes('DECOMPTE FINAL')) {
      badges.push({ icon: '🌳', label: 'Décompte final' });
    }
    if (badges.length === 0 && tile.famille === 'REVE') {
      badges.push({ icon: '🌅', label: 'À l’ouverture' });
    }
    return badges;
  }

  // --------------------------------------------------------------------------
  // Filtrage multi-critères (Pilier C)
  // --------------------------------------------------------------------------
  function tileMatchesFilters(tileId, activeCircleSet) {
    const cat = getCatalogue();
    const tile = cat[tileId];
    const prof = getTileProfile(tileId);
    if (!tile || !prof) return false;

    const f = explorerState.filters;
    if (f.inCircleOnly && activeCircleSet && !activeCircleSet.has(tileId)) return false;
    if (f.family !== 'ALL' && tile.famille !== f.family) return false;
    if (f.peuple !== 'ALL' && !tile.couple.includes(f.peuple)) return false;

    if (f.role !== 'ALL') {
      const flags = getTileRoleFlags(tileId);
      if (f.role === 'TWIST' && !flags.isTwist) return false;
      if (f.role === 'LOI_PASSIVE' && !flags.isLoi) return false;
      if (f.role === 'CATALYSEUR_EVEIL' && !flags.isCatalyseur) return false;
      if (f.role === 'LEVIER_REVE' && !flags.isLevier) return false;
      if (f.role === 'ENRACINEMENT' && !flags.isEnracinement) return false;
      if (f.role === 'AUTONOME_A0' && !flags.isAutonomeA0) return false;
      if (f.role === 'BRIQUE_FLUIDE' && !flags.isFluide) return false;
    }

    if (f.icon !== 'ALL') {
      const cab = normalizeDeclencheurToIconId(prof.cablage_recommande);
      const trigs = getNormalizedTileTriggers(tileId);
      const isResonance = f.icon === 'ICONE_RESONANCE' && tile.famille === 'GARDIEN';
      if (cab !== f.icon && !trigs.includes(f.icon) && !isResonance) return false;
    }

    if (f.stateToken !== 'ALL') {
      const allTokens = []
        .concat(prof.entrees || [])
        .concat(prof.sorties || [])
        .concat(prof.paiement || []);
      if (!allTokens.includes(f.stateToken)) return false;
    }

    if (f.search && f.search.trim()) {
      const q = f.search.trim().toLowerCase();
      const hay = [
        tile.id,
        tile.nomBase,
        prof.nom,
        prof.alias_oriente,
        prof.animal_ou_theme,
        stripHtml(prof.texte),
        prof.primitive,
        prof.temoin,
        prof.piste_twist,
        prof.heuristique_bot,
        prof.decision_joueur && prof.decision_joueur.choix,
        prof.decision_joueur && prof.decision_joueur.renoncement,
        (prof.tags || []).join(' '),
        (prof.role_porte || []).join(' ')
      ]
        .filter(Boolean)
        .join(' ')
        .toLowerCase();
      if (!hay.includes(q)) return false;
    }

    return true;
  }

  function hasAnyActiveFilter() {
    const f = explorerState.filters;
    return Boolean(
      (f.search && f.search.trim()) ||
      f.family !== 'ALL' ||
      f.peuple !== 'ALL' ||
      f.role !== 'ALL' ||
      f.icon !== 'ALL' ||
      f.stateToken !== 'ALL' ||
      f.inCircleOnly
    );
  }

  function getFilteredTileIdSet() {
    const cat = getCatalogue();
    const { tileIds } = getAssiseTilesAndBorders(getCurrentCircle());
    const activeCircleSet = new Set(tileIds);
    const matched = new Set();
    for (const tid of Object.keys(cat)) {
      if (tileMatchesFilters(tid, activeCircleSet)) matched.add(tid);
    }
    return { matched, activeCircleSet };
  }

  // --------------------------------------------------------------------------
  // Rendu Pilier A — Carte-Tuile à double lecture
  // --------------------------------------------------------------------------
  function renderGuardianRamp(tile, prof) {
    const recIconId = normalizeDeclencheurToIconId(prof.cablage_recommande);
    return `
      <div class="exp-guardian-ramp" data-guardian-ramp="v6.2" role="list" aria-label="Piste des 6 icônes Gardiens v6.2">
        ${GUARDIAN_ICONS_V62.map(ic => {
          const isRec = recIconId === ic.id;
          return `
            <div class="exp-ramp-slot ${isRec ? 'is-recommended' : ''}" data-icon-id="${ic.id}" data-icon-pos="${ic.pos}" title="${escapeHtml(ic.label + ' — ' + ic.desc + (isRec ? ' (Câblage recommandé ★)' : ''))}">
              ${isRec ? '<span class="exp-ramp-star" aria-label="Câblage recommandé">★</span>' : ''}
              <span class="exp-ramp-emoji">${ic.icon}</span>
              <span>${escapeHtml(ic.short)}</span>
            </div>
          `;
        }).join('')}
      </div>
    `;
  }

  function formatReasonsCompact(link) {
    if (!link) return '';
    const parts = [];
    for (const s of (link.states || [])) {
      const m = getStateMeta(s);
      parts.push(m.icon + ' ' + m.label);
    }
    for (const icId of (link.icons || [])) {
      const ic = GUARDIAN_ICON_BY_ID[icId];
      parts.push(ic ? '★' + ic.icon + ' ' + ic.label : icId);
    }
    return parts.join(' · ');
  }

  function renderTileCard(tileId, context) {
    const cat = getCatalogue();
    const peuplesMap = getPeuplesMap();
    const tile = cat[tileId];
    const prof = getTileProfile(tileId);
    if (!tile || !prof) return '';

    const ctx = context || {};
    const activeCircleSet = ctx.activeCircleSet || new Set();
    const xray = ctx.xray || null;
    const isInCircle = activeCircleSet.has(tileId);

    const originCode = tile.origine;
    const neighborCode = getTileNeighbor(tile);
    const originP = peuplesMap[originCode] || { icon: '', nom: originCode };
    const neighborP = peuplesMap[neighborCode] || { icon: '', nom: neighborCode };

    const famMeta = tile.famille === 'GARDIEN'
      ? { icon: '🛡️', label: 'Gardien' }
      : (tile.famille === 'REVE'
          ? { icon: '🌙', label: 'Rêve' }
          : { icon: '🪹', label: 'Nid' });

    const flags = getTileRoleFlags(tileId);
    let statusBadgeHtml = '';
    if (flags.isTwist) {
      const twistTip = prof.piste_twist || 'Twist structurel 2K3 du Canon 0';
      statusBadgeHtml = `<span class="exp-status-badge exp-status-twist" data-status="TWIST" data-twist-piste="${escapeHtml(twistTip)}" title="${escapeHtml(twistTip)}">⚡ Twist 2K3</span>`;
    } else if (flags.isLoi) {
      statusBadgeHtml = `<span class="exp-status-badge exp-status-loi" data-status="LOI_PASSIVE" title="Loi passive continue (plafond ≤ 2 par assise)">⚖️ Loi passive</span>`;
    } else {
      statusBadgeHtml = `<span class="exp-status-badge exp-status-fluide" data-status="BRIQUE_FLUIDE" title="Brique fluide sans surcharge de loi ni twist">🌊 Brique fluide</span>`;
    }

    // Ruban de rôle modèle + vecteurs
    const rolePills = [];
    if (flags.isCatalyseur) rolePills.push('<span class="exp-role-badge exp-role-eveil">☀️ Catalyseur d’Éveil</span>');
    if (flags.isLevier) rolePills.push('<span class="exp-role-badge exp-role-reve">🌙 Levier de Rêve</span>');
    if (flags.isEnracinement) rolePills.push('<span class="exp-role-badge exp-role-enrac">🌱 Synergie Enracinement</span>');
    if (flags.isAutonomeA0) rolePills.push('<span class="exp-role-badge exp-role-a0">🔓 Autonome A=0</span>');

    const vecRaw = String(prof.vecteurs || '').trim();
    const vecTip = formatVectorTooltip(vecRaw);
    const vecDisplay = vecRaw ? vecRaw.replace('->', '➔') : '';

    // Corps joueur
    const parsedFaces = parseTileFaces(tile, prof);
    let playerBodyHtml = '';
    if (tile.famille === 'GARDIEN') {
      playerBodyHtml = `
        ${renderGuardianRamp(tile, prof)}
        <div class="exp-faces-stack">
          ${parsedFaces.faces.map(f => `
            <div class="exp-face-box ${f.isFace2 ? 'is-face2' : ''}">
              <div class="exp-face-head">
                <span class="exp-face-label">
                  <span>${escapeHtml(f.label)}</span>
                  ${f.isFace2 ? '<span class="exp-face2-enrac-pill">🌱 2 Souches si enraciné</span>' : ''}
                </span>
                <span class="exp-word-count">${f.words} mots</span>
              </div>
              <div class="exp-face-text">${f.html}</div>
            </div>
          `).join('')}
        </div>
      `;
    } else {
      const winBadges = getNaturalWindowBadges(tile, prof);
      playerBodyHtml = `
        <div class="exp-window-row">
          ${winBadges.map(b => `<span class="exp-window-badge">${b.icon} ${escapeHtml(b.label)}</span>`).join('')}
        </div>
        <div class="exp-faces-stack">
          ${parsedFaces.faces.map(f => `
            <div class="exp-face-box">
              <div class="exp-face-head">
                <span class="exp-face-label">${escapeHtml(f.label)}</span>
                <span class="exp-word-count">${f.words} mots</span>
              </div>
              <div class="exp-face-text">${f.html}</div>
            </div>
          `).join('')}
          ${parsedFaces.enracine ? `
            <div class="exp-face-box is-enracine" data-enracine-cartouche="true">
              <div class="exp-face-head">
                <span class="exp-face-label">${parsedFaces.enracine.label} :</span>
                <span class="exp-word-count">${parsedFaces.enracine.words} mots</span>
              </div>
              <div class="exp-face-text">${parsedFaces.enracine.html}</div>
            </div>
          ` : ''}
        </div>
      `;
    }

    // Pied de carte — Puces de flux cliquables [Entrées] -> [Sorties] -> 🎯 [Paiements]
    const selectedState = explorerState.filters.stateToken;
    const renderChip = (tok, kindCls) => {
      const m = getStateMeta(tok);
      const selCls = selectedState === tok ? 'is-selected' : '';
      return `<button type="button" class="exp-state-chip ${kindCls} ${selCls}" data-state-token="${escapeHtml(tok)}" onclick="AmazoniaExplorerV62.toggleStateChipFilter('${escapeHtml(tok)}')" title="Filtrer les tuiles liées à : ${escapeHtml(m.label)}">${m.icon} ${escapeHtml(m.label)}</button>`;
    };

    const inputs = Array.isArray(prof.entrees) ? prof.entrees : [];
    const outputs = Array.isArray(prof.sorties) ? prof.sorties : [];
    const payments = Array.isArray(prof.paiement) ? prof.paiement : [];

    const flowFooterHtml = `
      <div class="exp-flow-footer" aria-label="Flux d’états de la tuile">
        <span class="exp-flow-group">
          ${inputs.length > 0 ? inputs.map(t => renderChip(t, 'is-input')).join('') : '<span class="exp-state-empty">Libre</span>'}
        </span>
        <span class="exp-flow-sep" aria-hidden="true">➔</span>
        <span class="exp-flow-group">
          ${outputs.length > 0 ? outputs.map(t => renderChip(t, 'is-output')).join('') : '<span class="exp-state-empty">—</span>'}
        </span>
        <span class="exp-flow-sep" aria-hidden="true">➔ 🎯</span>
        <span class="exp-flow-group">
          ${payments.length > 0 ? payments.map(t => renderChip(t, 'is-pay')).join('') : '<span class="exp-state-empty">—</span>'}
        </span>
      </div>
    `;

    // Tiroir « Capot Concepteur »
    const capotOpen = explorerState.allCapotsOpen || explorerState.capotOpenIds.has(tileId);
    const dec = prof.decision_joueur || {};
    const prix = prof.prix_estime || {};
    const parFaceEntries = prix.par_face ? Object.entries(prix.par_face) : [];
    const temoinsArr = Array.isArray(prof.temoins) ? prof.temoins : [];
    const normTriggers = getNormalizedTileTriggers(tileId);
    const syncStatus = String(prof.engine_sync_status || 'PENDING_KERNEL_V6_2');
    const syncIsVerified = syncStatus === 'ACTIVE_VERIFIED';
    const vivierPistes = getVivierPistesForSlot(tileId);

    const capotHtml = `
      <div class="exp-capot-wrap">
        <button type="button" class="exp-capot-toggle" aria-expanded="${capotOpen ? 'true' : 'false'}" onclick="AmazoniaExplorerV62.toggleCapot('${tileId}')">
          <span>${capotOpen ? '▾' : '▸'} Capot Concepteur (Choix/Renoncement · Bot · Prix DT · Témoins · Profils B/C)</span>
          <span class="exp-sync-badge ${syncIsVerified ? 'is-verified' : 'is-pending'}">${escapeHtml(syncStatus)}</span>
        </button>
        <div class="exp-capot-body ${capotOpen ? '' : 'is-hidden'}" data-capot-tile="${tileId}">
          <div class="exp-diptych">
            <div class="exp-diptych-box is-choice">
              <div class="exp-capot-label">✦ Choix joueur</div>
              <div>${escapeHtml(dec.choix || '—')}</div>
            </div>
            <div class="exp-diptych-box is-tradeoff">
              <div class="exp-capot-label">⚖️ Renoncement</div>
              <div>${escapeHtml(dec.renoncement || '—')}</div>
            </div>
          </div>

          <div class="exp-capot-metrics">
            <div class="exp-capot-block">
              <div class="exp-capot-label">🤖 Heuristique Bot</div>
              <div>${escapeHtml(prof.heuristique_bot || '—')}</div>
              ${prof.double_ouverture ? `<div style="margin-top:0.4rem;color:#0f766e;"><strong>Double ouverture :</strong> ${escapeHtml(prof.double_ouverture)}</div>` : ''}
            </div>
            <div class="exp-capot-block">
              <div class="exp-capot-label">💎 Prix estimé (${escapeHtml(prix.unite || 'Défenseur-tour (DT)')})</div>
              <div class="exp-dt-pills">
                <span class="exp-dt-pill">Coût : ${prix.cout_construction_DT !== undefined ? escapeHtml(prix.cout_construction_DT) : '2'} DT</span>
                ${parFaceEntries.map(([k, v]) => `<span class="exp-dt-pill">${escapeHtml(k)} : ${escapeHtml(v)} DT</span>`).join('')}
                ${prix.activations_pour_amortir !== undefined ? `<span class="exp-dt-pill">Amorti en ${escapeHtml(prix.activations_pour_amortir)} act.</span>` : ''}
              </div>
              ${prix.bareme ? `<div style="margin-top:0.3rem;font-size:0.68rem;color:#64748b;">${escapeHtml(prix.bareme)}</div>` : ''}
            </div>
          </div>

          <div class="exp-capot-block">
            <div class="exp-capot-label">🧪 Scénarios témoins vérifiés (${temoinsArr.length})</div>
            <div style="font-style:italic;color:#334155;">${escapeHtml(prof.temoin || '—')}</div>
            ${temoinsArr.length > 0 ? `
              <div class="exp-witness-list">
                ${temoinsArr.map(w => `
                  <div class="exp-witness-item">
                    <strong>✓ ${escapeHtml(w.id)} · ${escapeHtml(w.statut || 'OK')}</strong>
                    ${Array.isArray(w.journal) && w.journal.length > 0 ? ` — ${escapeHtml(w.journal.join(' ; '))}` : ''}
                  </div>
                `).join('')}
              </div>
            ` : ''}
          </div>

          <div class="exp-capot-meta-row">
            <div style="display:flex;flex-wrap:wrap;gap:0.35rem;align-items:center;">
              <span class="exp-dt-pill">Primitive : ${escapeHtml(prof.primitive || '—')}</span>
              ${normTriggers.length > 0 ? `
                <span class="exp-dt-pill">Icônes amorcées (v6.2) : ${normTriggers.map(icId => {
                  const ic = GUARDIAN_ICON_BY_ID[icId];
                  return ic ? ic.icon + ' ' + ic.label : icId;
                }).join(', ')}</span>
              ` : ''}
            </div>
            <div class="exp-profile-tabs" aria-label="Sélecteur de profil">
              <span style="font-size:0.68rem;color:#64748b;margin-right:0.2rem;">Profil :</span>
              <span class="exp-profile-tab is-active" title="Profil A · Canon 0 actif">[A] Canon 0</span>
              <span class="exp-profile-tab is-future" title="Profil B prévu en Phase 5">[B] Phase 5</span>
              <span class="exp-profile-tab is-future" title="Profil C prévu en Phase 5">[C] Phase 5</span>
            </div>
          </div>

          ${vivierPistes.length > 0 ? `
            <div class="exp-vivier-preview">
              <div class="exp-capot-label">🔮 Piste(s) candidate(s) du vivier Phase 5 (aperçu [B] / [C])</div>
              ${vivierPistes.map(vp => `
                <div style="margin-top:0.25rem;">
                  <strong>${escapeHtml(vp.cible)}</strong> <span style="opacity:0.75;">(${escapeHtml(vp.origine)})</span> — ${escapeHtml(vp.concept)}
                </div>
              `).join('')}
            </div>
          ` : ''}
        </div>
      </div>
    `;

    // Classes & ruban Rayons X
    let xrayClass = '';
    let xrayRibbonHtml = '';
    if (xray && xray.focusId) {
      const entry = xray.byTileId[tileId];
      if (!entry) {
        xrayClass = 'exp-xray-dimmed';
      } else if (entry.role === 'focus') {
        xrayClass = 'exp-xray-focus';
        xrayRibbonHtml = `<div class="exp-xray-card-ribbon is-focus">🔬 Tuile au centre du Focus Synergies</div>`;
      } else if (entry.role === 'upstream') {
        xrayClass = 'exp-xray-upstream';
        xrayRibbonHtml = `<div class="exp-xray-card-ribbon is-up">▲ Amont (nourrit ${escapeHtml(xray.focusId)}) · ${escapeHtml(formatReasonsCompact(entry.upLink))}</div>`;
      } else if (entry.role === 'downstream') {
        xrayClass = 'exp-xray-downstream';
        xrayRibbonHtml = `<div class="exp-xray-card-ribbon is-down">▼ Aval (consomme ${escapeHtml(xray.focusId)}) · ${escapeHtml(formatReasonsCompact(entry.downLink))}</div>`;
      } else if (entry.role === 'both') {
        xrayClass = 'exp-xray-both';
        xrayRibbonHtml = `<div class="exp-xray-card-ribbon is-both">▲▼ Amont & Aval de ${escapeHtml(xray.focusId)} · ▲ ${escapeHtml(formatReasonsCompact(entry.upLink))} | ▼ ${escapeHtml(formatReasonsCompact(entry.downLink))}</div>`;
      }
    }

    const isFocused = explorerState.xrayFocusId === tileId;
    const medallionHtml = renderTileMedallionHtml(tile.id);
    const digestFooter = typeof global.renderSlotDigestFooter === 'function'
      ? global.renderSlotDigestFooter(tileId, ['A'])
      : '';

    return `
      <article class="exp-tile-card fam-${tile.famille} ${xrayClass}" data-tile-id="${tile.id}" data-origin="${originCode}" data-neighbor="${neighborCode}" data-family="${tile.famille}">
        ${xrayRibbonHtml}
        <div class="exp-card-head">
          <div class="exp-card-head-left">
            <span class="exp-orient-pill" title="${escapeHtml(originP.nom + ' vers ' + neighborP.nom + ' · Emplacement ' + tile.id)}">
              <span class="exp-orient-half exp-p-${originCode}">${renderPeupleIconHtml(originCode, originP.icon)} ${originCode}</span>
              <span class="exp-orient-arrow">➔</span>
              <span class="exp-orient-half exp-p-${neighborCode}">${renderPeupleIconHtml(neighborCode, neighborP.icon)} ${neighborCode}</span>
              <span class="exp-orient-id">${tile.id}</span>
            </span>
            <span class="exp-family-pill fam-${tile.famille}">${famMeta.icon} ${famMeta.label}</span>
          </div>
          <div class="exp-card-head-right">
            ${statusBadgeHtml}
            <button type="button" class="exp-xray-btn ${isFocused ? 'is-active' : ''}" onclick="AmazoniaExplorerV62.toggleXRay('${tile.id}')" title="Activer le mode Rayons X des synergies autour de ${tile.id}">
              🔬 ${isFocused ? 'Focus actif' : 'Focus Synergies'}
            </button>
          </div>
        </div>

        <div class="exp-card-title-row ${medallionHtml ? 'has-medallion' : ''}">
          <div class="exp-card-identity">
            ${medallionHtml}
            <div class="exp-card-title-block">
              <h4 class="exp-card-title">${escapeHtml(prof.nom || tile.nomBase)}</h4>
              ${prof.animal_ou_theme ? `<div class="exp-card-theme">${escapeHtml(prof.animal_ou_theme)}</div>` : ''}
            </div>
          </div>
          ${isInCircle ? '<span class="exp-inplay-tag">✓ En jeu</span>' : ''}
        </div>

        ${rolePills.length > 0 || vecDisplay ? `
          <div class="exp-role-ribbon">
            ${rolePills.join('')}
            ${vecDisplay ? `<span class="exp-vector-chip" data-vector-pair="${escapeHtml(vecRaw)}" title="${escapeHtml(vecTip)}">${escapeHtml(vecDisplay)}</span>` : ''}
          </div>
        ` : ''}

        ${playerBodyHtml}
        ${flowFooterHtml}
        ${capotHtml}
        ${digestFooter}
      </article>
    `;
  }

  // --------------------------------------------------------------------------
  // Rendu Mode 1 — Les 15 Lisières face-à-face
  // --------------------------------------------------------------------------
  function renderMode1Lisieres(matchedSet, activeCircleSet, xray) {
    const matrice = getMatricePaires();
    const peuplesMap = getPeuplesMap();
    const activeBordersSet = new Set();
    const { borders } = getAssiseTilesAndBorders(getCurrentCircle());
    for (const b of borders) {
      activeBordersSet.add(b.p1 + '-' + b.p2);
      activeBordersSet.add(b.p2 + '-' + b.p1);
    }

    let totalRendered = 0;
    const sectionsHtml = BORDER_GROUPS_V62.map(group => {
      const duosHtml = group.pairs.map(([pA, pB]) => {
        const pair = matrice[pA + '_' + pB] || [];
        const tidA = pair[0];
        const tidB = pair[1];
        if (!tidA || !tidB) return '';

        const showA = matchedSet.has(tidA);
        const showB = matchedSet.has(tidB);
        if (!showA && !showB) return '';

        if (showA) totalRendered++;
        if (showB) totalRendered++;

        const is100Fluid = LISIERES_100PC_FLUIDES.has(pA + '-' + pB);
        const isInTable = activeBordersSet.has(pA + '-' + pB);
        const div = computeBorderDivergence(tidA, tidB);
        const mA = getStateMeta(div.primaryOutA);
        const mB = getStateMeta(div.primaryOutB);
        const pInfoA = peuplesMap[pA] || { icon: '', nom: pA };
        const pInfoB = peuplesMap[pB] || { icon: '', nom: pB };

        const renderSlot = (tid, isShown, dirLabel) => {
          if (isShown) return renderTileCard(tid, { activeCircleSet, xray });
          const tObj = getCatalogue()[tid];
          return `
            <div class="exp-filtered-placeholder">
              <strong>${escapeHtml(dirLabel)} · ${escapeHtml(tid)} (${escapeHtml(tObj ? tObj.nomBase : '')})</strong>
              <span>Masquée par les filtres actifs</span>
              <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.resetFilters()">Afficher la lisière complète</button>
            </div>
          `;
        };

        return `
          <div class="exp-border-duo ${isInTable ? 'is-in-table' : ''}" data-border="${pA}-${pB}">
            <div class="exp-border-banner">
              <div class="exp-border-title">
                <span class="exp-orient-half exp-p-${pA}" style="border-radius:0.45rem;border:1px solid;">${renderPeupleIconHtml(pA, pInfoA.icon)} ${pA}</span>
                <span>↔</span>
                <span class="exp-orient-half exp-p-${pB}" style="border-radius:0.45rem;border:1px solid;">${renderPeupleIconHtml(pB, pInfoB.icon)} ${pB}</span>
                <span style="color:#64748b;font-weight:600;font-size:0.72rem;">${escapeHtml(pInfoA.nom)} – ${escapeHtml(pInfoB.nom)}</span>
                ${isInTable ? '<span class="exp-inplay-tag">✓ Lisière active sur la table</span>' : ''}
              </div>
              <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.4rem;">
                <span class="exp-geo-badge ${is100Fluid ? 'is-fluid' : 'is-mixed'}">
                  ${is100Fluid ? '🌿 100 % fluide' : '🔀 Mixte (géométrie 2K3)'}
                </span>
                <span class="exp-divergence-proof" title="Preuve de divergence C05 entre les sorties principales des deux tuiles de la lisière">
                  <strong>Divergence :</strong>
                  <span>${escapeHtml(tidA)} (${mA.icon} ${escapeHtml(mA.label)})</span>
                  <span style="font-weight:800;color:${div.divergent ? '#059669' : '#dc2626'};">${div.divergent ? '≠' : '='}</span>
                  <span>${escapeHtml(tidB)} (${mB.icon} ${escapeHtml(mB.label)})</span>
                  ${div.stateChain ? `<span style="color:#475569;">· Flux : ${escapeHtml(div.stateChain)}</span>` : ''}
                  <span style="color:#059669;font-weight:700;">✓ 0 boucle</span>
                </span>
              </div>
            </div>
            <div class="exp-border-cards">
              ${renderSlot(tidA, showA, pA + ' ➔ ' + pB)}
              ${renderSlot(tidB, showB, pB + ' ➔ ' + pA)}
            </div>
          </div>
        `;
      }).filter(Boolean);

      if (duosHtml.length === 0) return '';
      return `
        <section class="exp-group-section" data-border-group="${group.id}">
          <div class="exp-group-header">
            <h3>${escapeHtml(group.title)}</h3>
            <span class="exp-group-sub">${escapeHtml(group.subtitle)}</span>
          </div>
          ${duosHtml.join('')}
        </section>
      `;
    }).filter(Boolean);

    if (sectionsHtml.length === 0) {
      return {
        displayedCount: 0,
        html: `<div class="exp-empty-state">Aucune tuile ne correspond aux critères sélectionnés. <button type="button" class="exp-btn" style="margin-left:0.5rem;" onclick="AmazoniaExplorerV62.resetFilters()">↺ Réinitialiser les filtres</button></div>`
      };
    }

    return { displayedCount: totalRendered, html: sectionsHtml.join('') };
  }

  // --------------------------------------------------------------------------
  // Rendu Mode 2 — Table & Roue des 197 Assises (SVG + Tableau de santé)
  // --------------------------------------------------------------------------
  function renderAssiseWheelSvg(health) {
    const cx = 230;
    const cy = 230;
    const rNode = 152;
    const rEdge = 112;
    const n = health.n;
    const peuplesMap = getPeuplesMap();
    const cat = getCatalogue();

    const coords = health.circle.map((code, i) => {
      const angle = -Math.PI / 2 + (2 * Math.PI * i) / n;
      return {
        code,
        angle,
        x: cx + rNode * Math.cos(angle),
        y: cy + rNode * Math.sin(angle)
      };
    });

    const linesSvg = [];
    const edgesSvg = [];
    for (let i = 0; i < n; i++) {
      const a = coords[i];
      const b = coords[(i + 1) % n];
      const border = health.borders[i];
      const midAngle = -Math.PI / 2 + (2 * Math.PI * (i + 0.5)) / n;
      const mx = cx + rEdge * Math.cos(midAngle);
      const my = cy + rEdge * Math.sin(midAngle);

      // Rayon vers le centre
      linesSvg.push(`<line x1="${cx}" y1="${cy}" x2="${a.x.toFixed(1)}" y2="${a.y.toFixed(1)}" stroke="#cbd5e1" stroke-width="1.5" stroke-dasharray="4 4" />`);
      // Lisière entre a et b
      const strokeCol = border.is100pcFluide ? '#10b981' : '#94a3b8';
      linesSvg.push(`<line x1="${a.x.toFixed(1)}" y1="${a.y.toFixed(1)}" x2="${b.x.toFixed(1)}" y2="${b.y.toFixed(1)}" stroke="${strokeCol}" stroke-width="3" />`);

      const sel = explorerState.wheelSelection;
      const isEdgeSelected = sel && sel.kind === 'border' && sel.p1 === border.p1 && sel.p2 === border.p2;
      const tLabels = border.tuiles.map(tid => {
        const flags = getTileRoleFlags(tid);
        return tid + (flags.isTwist ? '⚡' : (flags.isLoi ? '⚖' : ''));
      }).join(' · ');

      edgesSvg.push(`
        <g class="exp-wheel-edge" data-wheel-border="${border.p1}-${border.p2}" onclick="AmazoniaExplorerV62.selectWheelFilter('border','${border.p1}','${border.p2}')">
          <rect x="${(mx - 44).toFixed(1)}" y="${(my - 14).toFixed(1)}" width="88" height="28" rx="9" fill="${isEdgeSelected ? '#1e3b2e' : '#ffffff'}" stroke="${isEdgeSelected ? '#0f2119' : strokeCol}" stroke-width="${isEdgeSelected ? '2.2' : '1.5'}" />
          <text x="${mx.toFixed(1)}" y="${(my + 4).toFixed(1)}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10.5" font-weight="700" fill="${isEdgeSelected ? '#ffffff' : '#0f172a'}">${escapeHtml(tLabels)}</text>
        </g>
      `);
    }

    const nodesSvg = coords.map((pt, idx) => {
      const pInfo = peuplesMap[pt.code] || { icon: '', nom: pt.code };
      const acc = PEUPLE_ACCESSORIES_V62[pt.code] || { shortTag: '' };
      const col = PEUPLE_SVG_COLORS[pt.code] || { fill: '#f1f5f9', stroke: '#64748b', text: '#0f172a' };
      const sel = explorerState.wheelSelection;
      const isNodeSelected = sel && sel.kind === 'peuple' && sel.code === pt.code;

      return `
        <g class="exp-wheel-node" data-wheel-peuple="${pt.code}" onclick="AmazoniaExplorerV62.selectWheelFilter('peuple','${pt.code}')">
          <circle cx="${pt.x.toFixed(1)}" cy="${pt.y.toFixed(1)}" r="38" fill="${col.fill}" stroke="${isNodeSelected ? '#0f2119' : col.stroke}" stroke-width="${isNodeSelected ? '3.5' : '2.2'}" />
          ${renderPeupleWheelIconSvg(pt.code, pInfo.icon, pt.x, pt.y)}
          <text x="${pt.x.toFixed(1)}" y="${(pt.y + 8).toFixed(1)}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="800" fill="${col.text}">${pt.code} · #${idx + 1}</text>
          <text x="${pt.x.toFixed(1)}" y="${(pt.y + 21).toFixed(1)}" text-anchor="middle" font-family="Inter, sans-serif" font-size="8.2" font-weight="600" fill="${col.text}">${escapeHtml(acc.tier === 'ACTIF_TOUR_1' ? 'Actif T1' : 'Progressif')}</text>
        </g>
      `;
    });

    // Vérifier qu'aucun cat lookup n'a produit d'undefined
    const totalArbres = n * 10;
    const activeCount = health.tileIds.filter(tid => Boolean(cat[tid])).length;

    return `
      <svg class="exp-wheel-svg" viewBox="0 0 460 460" role="img" aria-label="Roue interactive de l’assise ${escapeHtml(health.canonKey)}">
        <circle cx="${cx}" cy="${cy}" r="${rNode}" fill="none" stroke="#e2e8f0" stroke-width="1.5" />
        ${linesSvg.join('')}
        <circle cx="${cx}" cy="${cy}" r="50" fill="#1e3b2e" stroke="#468a68" stroke-width="2.5" />
        <text x="${cx}" y="${cy - 12}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="12" font-weight="800" fill="#a7f3d0">${escapeHtml(health.canonKey)}</text>
        <text x="${cx}" y="${cy + 5}" text-anchor="middle" font-family="Inter, sans-serif" font-size="10.5" font-weight="700" fill="#ffffff">${n} J · ${activeCount} tuiles</text>
        <text x="${cx}" y="${cy + 20}" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="9.5" fill="#c5dfd0">${totalArbres} Arbres · #${health.assiseIndex || 1}/197</text>
        ${edgesSvg.join('')}
        ${nodesSvg.join('')}
      </svg>
    `;
  }

  function renderMode2Assises(matchedSet, activeCircleSet, xray) {
    const circle = getCurrentCircle();
    const health = computeAssiseHealth(circle);
    const all197 = enumerateAll197Assises();
    const peuplesMap = getPeuplesMap();

    // Regrouper les 197 assises par N dans le <select>
    const byN = { 3: [], 4: [], 5: [], 6: [] };
    for (const a of all197) byN[a.n].push(a);

    // Filtrer les 2N tuiles selon la sélection sur la roue ET les filtres globaux
    let wheelTileIds = health.tileIds.slice();
    const ws = explorerState.wheelSelection;
    if (ws && ws.kind === 'peuple') {
      wheelTileIds = wheelTileIds.filter(tid => {
        const t = getCatalogue()[tid];
        return t && t.couple.includes(ws.code);
      });
    } else if (ws && ws.kind === 'border') {
      const b = health.borders.find(x => x.p1 === ws.p1 && x.p2 === ws.p2);
      if (b) wheelTileIds = b.tuiles.slice();
    }
    const visibleTileIds = wheelTileIds.filter(tid => matchedSet.has(tid));

    const composerHtml = `
      <div class="exp-assises-composer" data-assise-key="${escapeHtml(health.canonKey)}" data-assise-index="${health.assiseIndex || 0}">
        <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.75rem;">
          <div>
            <h3 style="margin:0;font-family:'Crimson Pro',serif;font-size:1.25rem;font-weight:700;color:#0f172a;">
              Simulateur des 197 Assises Uniques — <span style="font-family:'JetBrains Mono',monospace;color:#1e3b2e;">${escapeHtml(health.canonKey)}</span>
              <span style="font-size:0.78rem;font-family:'JetBrains Mono',monospace;color:#475569;">(Assise #${health.assiseIndex || 1} / 197)</span>
            </h3>
            <div style="font-size:0.74rem;color:#64748b;">
              Espace exact canonisé modulo rotation &amp; symétrie : 20 (N=3) + 45 (N=4) + 72 (N=5) + 60 (N=6) = 197 assises.
            </div>
          </div>
          <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.45rem;">
            <label for="exp-assise-197-select" style="font-size:0.72rem;font-weight:700;color:#475569;">Explorer les 197 :</label>
            <select id="exp-assise-197-select" class="exp-select" style="width:auto;min-width:190px;" onchange="AmazoniaExplorerV62.selectAssiseByKey(this.value)">
              ${[3, 4, 5, 6].map(n => `
                <optgroup label="N=${n} joueurs (${byN[n].length} assises)">
                  ${byN[n].map(a => `<option value="${a.key}" ${a.key === health.canonKey ? 'selected' : ''}>#${a.index} · ${a.key} (${a.peuples.join('–')})</option>`).join('')}
                </optgroup>
              `).join('')}
            </select>
          </div>
        </div>

        <div>
          <div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#64748b;margin-bottom:0.35rem;">Tables témoins clés :</div>
          <div class="exp-presets-bar">
            ${PRESET_ASSISES.map(pr => `
              <button type="button" class="exp-preset-btn ${pr.key === health.canonKey ? 'is-active' : ''}" data-preset-key="${pr.key}" onclick="AmazoniaExplorerV62.selectPresetAssise('${pr.key}')">
                <span style="font-family:'JetBrains Mono',monospace;">${pr.label}</span>
                <span class="exp-preset-tag">· ${escapeHtml(pr.tag)}</span>
              </button>
            `).join('')}
          </div>
        </div>

        <div style="display:flex;flex-direction:column;gap:0.45rem;">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.5rem;">
            <span style="font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#64748b;">
              Ordre circulaire autour de la roue (cliquez pour ajouter/retirer ou permuter les sièges) :
            </span>
            <div style="display:flex;gap:0.35rem;">
              <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.rotateTable(-1)" title="Rotation anti-horaire">↺ Tourner</button>
              <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.reverseTable()" title="Symétrie miroir">⇄ Miroir</button>
            </div>
          </div>

          <div class="exp-seats-strip">
            ${health.circle.map((code, idx) => {
              const pInfo = peuplesMap[code] || { icon: '', nom: code };
              const nextIdx = (idx + 1) % health.n;
              return `
                <span class="exp-seat-pill exp-p-${code}">
                  <span class="exp-seat-label">#${idx + 1} ${renderPeupleIconHtml(code, pInfo.icon)} ${code}</span>
                  ${idx > 0 ? `<button type="button" class="exp-seat-move-btn" onclick="AmazoniaExplorerV62.swapTableSeats(${idx - 1}, ${idx})" title="Déplacer à gauche">←</button>` : ''}
                  ${idx < health.n - 1 ? `<button type="button" class="exp-seat-move-btn" onclick="AmazoniaExplorerV62.swapTableSeats(${idx}, ${nextIdx})" title="Déplacer à droite">→</button>` : ''}
                  ${health.n > 3 ? `<button type="button" class="exp-seat-move-btn" onclick="AmazoniaExplorerV62.toggleTablePeuple('${code}')" title="Retirer ${code} de la table">✕</button>` : ''}
                </span>
              `;
            }).join('')}
            ${PEUPLE_CANON_ORDER.filter(c => !health.circle.includes(c)).map(code => {
              const pInfo = peuplesMap[code] || { icon: '', nom: code };
              return `<button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.toggleTablePeuple('${code}')" title="Ajouter ${escapeHtml(pInfo.nom)} à la table">+ ${renderPeupleIconHtml(code, pInfo.icon)} ${code}</button>`;
            }).join('')}
          </div>
        </div>
      </div>
    `;

    // Tableau de bord de santé
    const loisStatus = health.loisAlert ? 'is-alert' : 'is-ok';
    const catStatus = health.catalyseurAlert ? 'is-alert' : (health.animalCount === 0 ? '' : 'is-ok');
    const levStatus = health.levierAlert ? 'is-alert' : (health.hasE && !health.hasH ? 'is-ok' : '');

    const healthHtml = `
      <div class="exp-health-panel" data-assise-health="${escapeHtml(health.canonKey)}">
        <div style="display:flex;align-items:center;justify-content:space-between;gap:0.5rem;flex-wrap:wrap;">
          <h4 style="margin:0;font-family:'Crimson Pro',serif;font-size:1.15rem;font-weight:700;">Tableau de bord de santé de l’assise</h4>
          <span style="font-size:0.72rem;font-weight:700;color:${health.alerts.length === 0 ? '#059669' : '#dc2626'};">
            ${health.alerts.length === 0 ? '✓ Assise saine (0 alerte)' : '⚠️ ' + health.alerts.length + ' alerte(s)'}
          </span>
        </div>

        <div class="exp-modules-row" aria-label="Modules du livret">
          <span class="exp-module-pill ${health.modules.gardiens ? 'is-active' : 'is-inactive'}" data-module="gardiens" data-active="${health.modules.gardiens}">
            🛡️ Module Gardiens &amp; Éveil (${health.modules.gardiens ? 'Actif' : 'Inactif'})
          </span>
          <span class="exp-module-pill ${health.modules.reves ? 'is-active' : 'is-inactive'}" data-module="reves" data-active="${health.modules.reves}">
            🌙 Module Rêves &amp; Sommeil (${health.modules.reves ? 'Actif' : 'Inactif'})
          </span>
          <span class="exp-module-pill ${health.modules.essaim ? 'is-active' : 'is-inactive'}" data-module="essaim" data-active="${health.modules.essaim}">
            🪲 Module Essaim (${health.modules.essaim ? 'Actif' : 'Inactif'})
          </span>
        </div>

        <div class="exp-health-grid">
          <div class="exp-kpi-card">
            <span class="exp-kpi-label">⚡ Twists 2K3</span>
            <span class="exp-kpi-value">${health.twists.length} <span style="font-size:0.72rem;font-weight:600;color:#64748b;">(0..4)</span></span>
            <span class="exp-kpi-detail">${health.twists.length > 0 ? health.twists.join(', ') : 'Aucun Twist'}</span>
          </div>
          <div class="exp-kpi-card ${loisStatus}">
            <span class="exp-kpi-label">⚖️ Lois passives</span>
            <span class="exp-kpi-value">${health.loisPassives.length} / 2 max</span>
            <span class="exp-kpi-detail">${health.loisAlert ? '🚨 Alerte > 2 lois !' : (health.loisPassives.length > 0 ? health.loisPassives.join(', ') : '0 loi (léger)')}</span>
          </div>
          <div class="exp-kpi-card ${catStatus}">
            <span class="exp-kpi-label">☀️ Catalyseurs d’Éveil</span>
            <span class="exp-kpi-value">${health.animalCount === 0 ? 'N/A (A=0)' : health.catalyseursEveil.length}</span>
            <span class="exp-kpi-detail">${health.catalyseurAlert ? '🚨 Alerte : 0 catalyseur !' : (health.catalyseursEveil.length > 0 ? health.catalyseursEveil.join(', ') : 'Module Gardiens inactif')}</span>
          </div>
          <div class="exp-kpi-card ${levStatus}">
            <span class="exp-kpi-label">🌙 Leviers de Rêve</span>
            <span class="exp-kpi-value">${health.leviersReve.length}</span>
            <span class="exp-kpi-detail">${health.levierAlert ? '🚨 Alerte : E sans H et 0 levier !' : (health.leviersReve.length > 0 ? health.leviersReve.join(', ') : (health.hasH ? 'Chant H natif' : 'Sans Entités'))}</span>
          </div>
          <div class="exp-kpi-card">
            <span class="exp-kpi-label">🌱 Enracinement</span>
            <span class="exp-kpi-value">${health.enracinements.length}</span>
            <span class="exp-kpi-detail">${health.enracinements.length > 0 ? health.enracinements.join(', ') : 'Enracinement socle'}</span>
          </div>
          <div class="exp-kpi-card is-ok">
            <span class="exp-kpi-label">🔗 Moteurs majeurs</span>
            <span class="exp-kpi-value">${health.disjointMajorCount} disjoints</span>
            <span class="exp-kpi-detail">${health.synergyChains.length} arcs inter-tuiles</span>
          </div>
        </div>

        <div style="margin-top:0.8rem;">
          <div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#475569;margin-bottom:0.35rem;">
            Couverture des 6 icônes Gardiens (ordre v6.2 gauche ➔ droite) :
          </div>
          <div class="exp-guardian-ramp" data-health-icons-ramp="v6.2">
            ${health.iconCoverage.map(ic => `
              <div class="exp-ramp-slot ${ic.recommendedGuardians.length > 0 && ic.active ? 'is-recommended' : ''}" style="${ic.active ? '' : 'opacity:0.4;text-decoration:line-through;'}" data-icon-id="${ic.id}" data-icon-pos="${ic.pos}" title="${escapeHtml(ic.label + ' — Câblés : ' + (ic.recommendedGuardians.join(', ') || 'aucun') + ' | Amorces : ' + (ic.triggerSources.join(', ') || 'socle'))}">
                <span class="exp-ramp-emoji">${ic.icon}</span>
                <span>${escapeHtml(ic.label)}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.6rem;color:#334155;">★${ic.recommendedGuardians.length} · ⚡${ic.triggerSources.length}</span>
              </div>
            `).join('')}
          </div>
        </div>

        <div style="margin-top:0.8rem;">
          <div style="font-size:0.68rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;color:#475569;">
            Chaînes de synergie majeures sur ${escapeHtml(health.canonKey)} (${health.synergyChains.length} — cliquez pour focaliser en Rayons X) :
          </div>
          <div class="exp-chains-list">
            ${health.synergyChains.length > 0
              ? health.synergyChains.slice(0, 28).map(ch => `
                  <button type="button" class="exp-chain-pill ${ch.kind === 'BUS' ? 'is-bus' : ''}" onclick="AmazoniaExplorerV62.toggleXRay('${ch.source}')" title="Activer Rayons X sur ${ch.source}">
                    <strong>${escapeHtml(ch.source)}</strong>
                    <span>➔</span>
                    <span>${escapeHtml(ch.bridges.join(' · '))}</span>
                    <span>➔</span>
                    <strong>${escapeHtml(ch.target)}</strong>
                  </button>
                `).join('')
              : '<span style="font-size:0.75rem;color:#64748b;">Aucune chaîne inter-tuiles détectée.</span>'}
          </div>
        </div>
      </div>
    `;

    const wheelFilterBanner = ws
      ? `<div style="display:flex;align-items:center;justify-content:space-between;gap:0.5rem;padding:0.55rem 0.85rem;border-radius:0.75rem;background:#eef2ff;border:1px solid #c7d2fe;font-size:0.76rem;color:#312e81;">
           <span>🎯 Filtré depuis la Roue : <strong>${ws.kind === 'peuple' ? 'Peuple ' + ws.code : 'Lisière ' + ws.p1 + '–' + ws.p2}</strong> (${visibleTileIds.length} tuiles)</span>
           <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.clearWheelFilter()">✕ Afficher les ${health.tileIds.length} tuiles de la table</button>
         </div>`
      : '';

    const stageHtml = `
      <div style="display:flex;flex-direction:column;gap:1rem;">
        ${composerHtml}
        <div class="exp-assises-stage">
          <div class="exp-wheel-panel">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:0.4rem;">
              <h4 style="margin:0;font-family:'Crimson Pro',serif;font-size:1.1rem;font-weight:700;">Roue de table (${health.n} rayons · ${health.tileIds.length} tuiles actives)</h4>
              <span style="font-size:0.7rem;color:#64748b;">Cliquez un Peuple ou une lisière</span>
            </div>
            ${renderAssiseWheelSvg(health)}
            <div style="display:flex;flex-wrap:wrap;gap:0.35rem;justify-content:center;margin-top:0.5rem;font-size:0.69rem;color:#475569;">
              ${health.circle.map(c => `<span class="exp-p-${c}" style="padding:0.15rem 0.45rem;border-radius:0.45rem;border:1px solid;font-weight:600;">${c} : ${escapeHtml(PEUPLE_ACCESSORIES_V62[c].shortTag)}</span>`).join('')}
            </div>
          </div>
          ${healthHtml}
        </div>
        ${wheelFilterBanner}
        <div id="exp-assises-cards-anchor" class="exp-active-cards-grid">
          ${visibleTileIds.length > 0
            ? visibleTileIds.map(tid => renderTileCard(tid, { activeCircleSet, xray })).join('')
            : `<div class="exp-empty-state" style="grid-column:1/-1;">Aucune tuile de cette table ne correspond aux filtres actifs.</div>`}
        </div>
      </div>
    `;

    return { displayedCount: visibleTileIds.length, html: stageHtml };
  }

  // --------------------------------------------------------------------------
  // Rendu Mode 3 — Grammaires par Peuple (3 + 3)
  // --------------------------------------------------------------------------
  function renderMode3Peuples(matchedSet, activeCircleSet, xray) {
    const selectedCode = PEUPLE_CANON_ORDER.includes(explorerState.activePeupleTab)
      ? explorerState.activePeupleTab
      : 'H';
    const peuplesMap = getPeuplesMap();
    const matrice = getMatricePaires();
    const pInfo = peuplesMap[selectedCode] || { icon: '', nom: selectedCode, famille: '' };
    const acc = PEUPLE_ACCESSORIES_V62[selectedCode];

    const tier1 = ['H', 'M', 'O'];
    const tier2 = ['E', 'R', 'I'];

    const renderTabBtn = code => {
      const pi = peuplesMap[code] || { icon: '', nom: code };
      const active = code === selectedCode;
      return `
        <button type="button" class="exp-peuple-tab-btn exp-p-${code} ${active ? 'is-active' : ''}" data-peuple-tab="${code}" onclick="AmazoniaExplorerV62.setPeupleTab('${code}')">
          <span class="exp-peuple-tab-icon">${renderPeupleIconHtml(code, pi.icon)}</span>
          <span>${code} · ${escapeHtml(pi.nom)}</span>
        </button>
      `;
    };

    // Paires avec les 5 autres Peuples : sortante (P>Q) à gauche vs entrante (Q>P) à droite
    const neighbors = PEUPLE_CANON_ORDER.filter(c => c !== selectedCode);
    let displayedCount = 0;
    const rowsHtml = neighbors.map(qCode => {
      const pair = matrice[selectedCode + '_' + qCode] || [];
      const outTid = pair[0]; // gouvernée par selectedCode (P>Q)
      const inTid = pair[1];  // gouvernée par qCode (Q>P)
      const showOut = outTid && matchedSet.has(outTid);
      const showIn = inTid && matchedSet.has(inTid);
      if (!showOut && !showIn) return '';
      if (showOut) displayedCount++;
      if (showIn) displayedCount++;

      const renderCol = (tid, show, fallbackLabel) => {
        if (show) return renderTileCard(tid, { activeCircleSet, xray });
        return `<div class="exp-filtered-placeholder"><strong>${escapeHtml(fallbackLabel)} (${escapeHtml(tid || '—')})</strong><span>Masquée par les filtres actifs</span></div>`;
      };

      return `
        <div class="exp-peuple-pair-row" data-peuple-row="${selectedCode}-${qCode}">
          ${renderCol(outTid, showOut, selectedCode + ' ➔ ' + qCode)}
          ${renderCol(inTid, showIn, qCode + ' ➔ ' + selectedCode)}
        </div>
      `;
    }).filter(Boolean);

    const html = `
      <div style="display:flex;flex-direction:column;gap:0.95rem;" data-peuple-grammar="${selectedCode}">
        <div class="exp-topbar" style="padding:0.85rem 1rem;">
          <div class="exp-peuple-tabs-wrap">
            <div class="exp-peuple-tier-row">
              <span class="exp-tier-label">⚡ 3 Actifs dès le Tour 1 :</span>
              ${tier1.map(renderTabBtn).join('')}
            </div>
            <div class="exp-peuple-tier-row">
              <span class="exp-tier-label">🌱 3 Progressifs via tuiles :</span>
              ${tier2.map(renderTabBtn).join('')}
            </div>
          </div>
        </div>

        <div class="exp-peuple-banner exp-p-${selectedCode}">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.5rem;">
            <div style="display:flex;align-items:center;gap:0.55rem;">
              <span class="exp-peuple-banner-icon" style="font-size:1.6rem;">${renderPeupleIconHtml(selectedCode, pInfo.icon, 28)}</span>
              <div>
                <h3 style="margin:0;font-family:'Crimson Pro',serif;font-size:1.35rem;font-weight:700;">${selectedCode} · ${escapeHtml(pInfo.nom)} — ${escapeHtml(acc.shortTag)}</h3>
                <div style="font-size:0.75rem;opacity:0.9;">${escapeHtml(pInfo.famille || '')} · <strong>${escapeHtml(acc.tierLabel)}</strong></div>
              </div>
            </div>
            <span class="exp-counter-pill" style="background:rgba(255,255,255,0.85);">5 sortantes (${selectedCode}&gt;*) · 5 entrantes (*&gt;${selectedCode})</span>
          </div>
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:0.65rem;font-size:0.78rem;">
            <div style="background:rgba(255,255,255,0.72);padding:0.6rem 0.75rem;border-radius:0.65rem;border:1px solid rgba(15,23,42,0.1);">
              <div style="font-size:0.66rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.2rem;">Matériel d’accessoire (3 + 3)</div>
              <div>${escapeHtml(acc.materiel)}</div>
            </div>
            <div style="background:rgba(255,255,255,0.72);padding:0.6rem 0.75rem;border-radius:0.65rem;border:1px solid rgba(15,23,42,0.1);">
              <div style="font-size:0.66rem;font-weight:800;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.2rem;">Règle asymétrique v6.2</div>
              <div>${escapeHtml(acc.regle)}</div>
            </div>
          </div>
        </div>

        <div class="exp-peuple-columns-header">
          <div class="exp-col-banner is-out">
            <span>➔ 5 tuiles gouvernées sortantes (${selectedCode} &gt; *)</span>
            <span style="font-size:0.7rem;opacity:0.85;">Décidées par ${escapeHtml(pInfo.nom)}</span>
          </div>
          <div class="exp-col-banner is-in">
            <span>⬅ 5 tuiles entrantes des voisins (* &gt; ${selectedCode})</span>
            <span style="font-size:0.7rem;opacity:0.85;">Couplées aux voisins de ${selectedCode}</span>
          </div>
        </div>

        <div>
          ${rowsHtml.length > 0 ? rowsHtml.join('') : '<div class="exp-empty-state">Aucune tuile de ce Peuple ne correspond aux filtres actifs.</div>'}
        </div>
      </div>
    `;

    return { displayedCount, html };
  }

  // --------------------------------------------------------------------------
  // Rendu du Panneau Rayons X & de la Barre d'outils globale
  // --------------------------------------------------------------------------
  function renderXRayBanner(xray) {
    if (!xray || !xray.focusId) return '';
    const cat = getCatalogue();
    const focusTile = cat[xray.focusId];
    const focusProf = getTileProfile(xray.focusId);
    if (!focusTile || !focusProf) return '';

    const focusCab = focusTile.famille === 'GARDIEN'
      ? normalizeDeclencheurToIconId(focusProf.cablage_recommande)
      : null;
    const focusCabIcon = focusCab ? GUARDIAN_ICON_BY_ID[focusCab] : null;

    return `
      <div class="exp-xray-banner" data-xray-focus="${escapeHtml(xray.focusId)}">
        <div class="exp-xray-header">
          <div class="exp-xray-title">
            <span>🔬 Rayons X des Synergies :</span>
            <span class="exp-orient-id" style="border-radius:0.45rem;">${escapeHtml(focusTile.id)}</span>
            <span>${escapeHtml(focusProf.nom || focusTile.nomBase)}</span>
            ${focusCabIcon ? `<span class="exp-xray-dot is-focus">★ ${focusCabIcon.icon} ${escapeHtml(focusCabIcon.label)}</span>` : ''}
            ${xray.scopeLabel ? `<span class="exp-xray-dot is-focus">${escapeHtml(xray.scopeLabel)}</span>` : ''}
          </div>
          <div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem;">
            <div class="exp-xray-legend">
              <span class="exp-xray-dot is-up">▲ Amont (${xray.upstreamTiles.length} tuiles + ${xray.upstreamAccessories.length} acc.)</span>
              <span class="exp-xray-dot is-focus">● Focus</span>
              <span class="exp-xray-dot is-down">▼ Aval (${xray.downstreamTiles.length} tuiles)</span>
            </div>
            <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.clearXRay()">✕ Quitter le focus (Échap)</button>
          </div>
        </div>

        <div class="exp-xray-columns">
          <div class="exp-xray-col is-up">
            <div class="exp-xray-col-title">
              <span>▲ Amont — Sources &amp; Accessoires (Émeraude)</span>
              <span>${xray.upstreamAccessories.length} acc. · ${xray.upstreamTiles.length} tuiles</span>
            </div>
            ${xray.upstreamAccessories.length > 0 ? `
              <div class="exp-xray-node-list">
                ${xray.upstreamAccessories.map(a => `
                  <span class="exp-xray-acc-pill" title="${escapeHtml(a.shortTag)}">
                    ${renderPeupleIconHtml(a.code, a.icon)} ${escapeHtml(a.name)} · ${escapeHtml(a.states.map(s => getStateMeta(s).icon + getStateMeta(s).label).concat(a.icons.map(i => GUARDIAN_ICON_BY_ID[i] ? '★' + GUARDIAN_ICON_BY_ID[i].label : i)).join(', '))}
                  </span>
                `).join('')}
              </div>
            ` : ''}
            <div class="exp-xray-node-list">
              ${xray.upstreamTiles.length > 0
                ? xray.upstreamTiles.map(u => `
                    <button type="button" class="exp-xray-node-btn" onclick="AmazoniaExplorerV62.toggleXRay('${u.source}')">
                      <strong>${escapeHtml(u.source)}</strong>
                      <span class="exp-xray-reason">${escapeHtml(formatReasonsCompact(u))}</span>
                    </button>
                  `).join('')
                : '<span style="font-size:0.72rem;color:#94a3b8;">Autonome (nourrie directement par les accessoires / le socle).</span>'}
            </div>
          </div>

          <div class="exp-xray-col is-center">
            <div class="exp-xray-col-title">
              <span>● Cœur observé</span>
              <span>${escapeHtml(focusProf.vecteurs || '')}</span>
            </div>
            <div style="font-size:0.78rem;font-weight:700;">${escapeHtml(focusTile.id)} · ${escapeHtml(focusProf.nom)}</div>
            <div style="font-size:0.71rem;color:#e2e8f0;">
              <div><strong>Entrées :</strong> ${(focusProf.entrees || []).map(s => getStateMeta(s).icon + ' ' + getStateMeta(s).label).join(', ') || 'Libre'}</div>
              <div style="margin-top:0.2rem;"><strong>Sorties :</strong> ${(focusProf.sorties || []).map(s => getStateMeta(s).icon + ' ' + getStateMeta(s).label).join(', ') || '—'}</div>
            </div>
          </div>

          <div class="exp-xray-col is-down">
            <div class="exp-xray-col-title">
              <span>▼ Aval — Tuiles consommatrices (Ambre)</span>
              <span>${xray.downstreamTiles.length} tuiles</span>
            </div>
            <div class="exp-xray-node-list">
              ${xray.downstreamTiles.length > 0
                ? xray.downstreamTiles.map(d => `
                    <button type="button" class="exp-xray-node-btn" onclick="AmazoniaExplorerV62.toggleXRay('${d.target}')">
                      <strong>${escapeHtml(d.target)}</strong>
                      <span class="exp-xray-reason">${escapeHtml(formatReasonsCompact(d))}</span>
                    </button>
                  `).join('')
                : '<span style="font-size:0.72rem;color:#94a3b8;">Paiement direct (Arbres, Souches, Éveil ou Sommeil).</span>'}
            </div>
          </div>
        </div>
      </div>
    `;
  }

  function renderReadingGuide() {
    if (!explorerState.readingGuideOpen) return '';
    const vecKeys = ['V1', 'V2', 'V3', 'V4', 'V5'];
    return `
      <section id="exp-reading-guide-panel" class="exp-reading-guide" data-reading-guide="open" aria-label="Guide de lecture de l’Explorateur v6.2">
        <div class="exp-guide-header">
          <div class="exp-guide-title-wrap">
            <span class="exp-guide-kicker">? Guide de lecture</span>
            <h3 class="exp-guide-title">Anatomie d’une lisière &amp; d’une carte-tuile Canon 0 (v6.2)</h3>
          </div>
          <button type="button" id="exp-reading-guide-close" class="exp-btn exp-guide-close-btn" onclick="AmazoniaExplorerV62.toggleReadingGuide(false)" title="Fermer le guide de lecture (Échap)">
            ✕ Fermer
          </button>
        </div>

        <div class="exp-guide-grid">
          <article class="exp-guide-card" data-guide-zone="1">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">1</span>
              <h4 class="exp-guide-card-title">Bandeau de lisière &amp; Géométrie 2K3</h4>
            </div>
            <div class="exp-guide-samples">
              <span class="exp-orient-half exp-p-M exp-guide-mini-chip">M</span>
              <span class="exp-guide-sep">↔</span>
              <span class="exp-orient-half exp-p-R exp-guide-mini-chip">R</span>
              <span class="exp-geo-badge is-fluid">🌿 100 % fluide</span>
              <span class="exp-geo-badge is-mixed">🔀 Mixte (2K3)</span>
              <span class="exp-guide-div-pill">✓ 0 boucle</span>
            </div>
            <p class="exp-guide-text">
              Frontière partagée entre deux Peuples voisins (<code>M ↔ R</code>). Distingue les <strong>3 lisières 100 % fluides</strong> (<code>E–O</code>, <code>H–M</code>, <code>R–I</code>) des <strong>12 lisières Mixtes (2K3)</strong> pouvant porter un Twist. La preuve de <strong>Divergence (<code>✓ 0 boucle</code>)</strong> garantit deux sorties différentes sans boucle d’état fermée à deux.
            </p>
          </article>

          <article class="exp-guide-card" data-guide-zone="2">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">2</span>
              <h4 class="exp-guide-card-title">En-tête d’identité &amp; Gouvernance</h4>
            </div>
            <div class="exp-guide-samples">
              <span class="exp-orient-pill">
                <span class="exp-orient-half exp-p-M">Origine</span>
                <span class="exp-orient-arrow">→</span>
                <span class="exp-orient-half exp-p-R">Voisin</span>
                <span class="exp-orient-id">ID</span>
              </span>
              <span class="exp-family-pill fam-GARDIEN">🛡️ Gardien</span>
              <span class="exp-family-pill fam-REVE">🌙 Rêve</span>
              <span class="exp-family-pill fam-CROISSANCE">🪹 Nid</span>
              <span class="exp-status-badge exp-status-fluide">🌊 Brique fluide</span>
              <span class="exp-status-badge exp-status-twist">⚡ Twist 2K3</span>
              <span class="exp-status-badge exp-status-loi">⚖️ Loi passive</span>
              <span class="exp-guide-xray-pill">🔬 Focus Synergies</span>
            </div>
            <p class="exp-guide-text">
              Dans <strong>[Origine → Voisin · ID]</strong>, le Peuple de gauche gouverne la tuile et fixe sa famille (<code>🛡️ Gardien</code> recto-verso, <code>🌙 Rêve</code>, <code>Nid</code>). À droite : <strong>Brique fluide</strong>, <strong>⚡ Twist 2K3</strong> (détourne une règle ou pièce du cœur — survoler pour lire la piste) ou <strong>⚖️ Loi passive</strong> (<code>M2</code> et <code>M3</code> uniquement), et <strong>Focus Synergies</strong> (<em>Rayons X</em> : <span class="exp-guide-inline-up">vert émeraude = fournisseurs amont</span>, <span class="exp-guide-inline-down">ambre = débouchés aval</span>).
            </p>
          </article>

          <article class="exp-guide-card" data-guide-zone="3">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">3</span>
              <h4 class="exp-guide-card-title">Obligations du modèle &amp; Les 5 Vecteurs (V1..V5)</h4>
            </div>
            <div class="exp-guide-samples">
              <span class="exp-role-badge exp-role-eveil">☀️ Catalyseur d’Éveil</span>
              <span class="exp-role-badge exp-role-reve">🌙 Levier de Rêve</span>
              <span class="exp-role-badge exp-role-enrac">🌱 Synergie Enracinement</span>
              <span class="exp-role-badge exp-role-a0">🔓 Autonome A=0</span>
              <span class="exp-vector-chip" title="${escapeHtml(formatVectorTooltip('V4 -> V2'))}">V_entrée → V_sortie</span>
            </div>
            <p class="exp-guide-text">
              Garanties structurelles du modèle (aucun badge = emplacement libre de toute obligation dure). La flèche de bivalence <strong><code>V_entrée → V_sortie</code></strong> (décodée au survol sur chaque carte) code les 5 familles de leviers :
            </p>
            <ul class="exp-guide-vector-list">
              ${vecKeys.map(vk => {
                const vd = VECTOR_DEFS_V62[vk];
                return `<li data-guide-vector="${vk}"><span class="exp-vector-chip exp-guide-vec-code">${vk}</span><span>${escapeHtml(vd.full)}</span></li>`;
              }).join('')}
            </ul>
          </article>

          <article class="exp-guide-card" data-guide-zone="4">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">4</span>
              <h4 class="exp-guide-card-title">Zone Joueur (Icônes, Fenêtres &amp; Enracinement)</h4>
            </div>
            <div class="exp-guide-samples">
              <span class="exp-guide-ramp-preview">🛡️ Parade · 🪤 Piégeage · 💥 Sabotage · 🌙 Rêve · 🪲 Insecte · ✨ Résonance (★)</span>
              <span class="exp-face2-enrac-pill">🌱 2 Souches si enraciné</span>
              <span class="exp-window-badge">🌅 À l’ouverture</span>
              <span class="exp-window-badge">🪹 Après production</span>
              <span class="exp-window-badge">🛡️ En Parade</span>
              <span class="exp-window-badge">🪲 En Migration</span>
              <span class="exp-guide-enrac-pill">🌱 Enraciné</span>
            </div>
            <p class="exp-guide-text">
              <strong>Gardiens</strong> : rampe des <strong>6 icônes</strong> dans l’ordre <code>v6.2</code> gauche → droite (<code>Parade</code>, <code>Piégeage</code>, <code>Sabotage</code>, <code>Rêve</code>, <code>Insecte</code>, <code>Résonance</code>) avec <strong>★</strong> sur l’icône de câblage recommandée ; <code>Face 2 · Éveillé</code> rappelle le bonus <strong>🌱 2 Souches si enraciné</strong> (contre <code>1 Souche</code> en Face 1 ou face unique). <strong>Rêves &amp; Nids</strong> : badge de fenêtre naturelle et cartouche vert forêt <strong>🌱 Enraciné</strong> pour les bonus dédiés (<code>R2</code>, <code>R6</code>, <code>M5</code>).
            </p>
          </article>

          <article class="exp-guide-card" data-guide-zone="5">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">5</span>
              <h4 class="exp-guide-card-title">Chaîne de flux physique cliquable (Pied de carte)</h4>
            </div>
            <div class="exp-guide-samples exp-guide-flow-sample">
              <span class="exp-state-chip is-input">Entrées requises (vert)</span>
              <span class="exp-flow-sep" aria-hidden="true">→</span>
              <span class="exp-state-chip is-output">Sorties produites (ambre)</span>
              <span class="exp-flow-sep" aria-hidden="true">→ 🎯</span>
              <span class="exp-state-chip is-pay">Paiement de victoire (bleu-violet)</span>
            </div>
            <p class="exp-guide-text">
              Se lit comme une équation <strong>[Entrées requises (vert)] → [Sorties produites (ambre)] → 🎯 [Paiement de victoire (bleu-violet)]</strong>. Cliquer sur n’importe quelle puce en pied de carte filtre aussitôt les tuiles liées à cet élément.
            </p>
          </article>

          <article class="exp-guide-card" data-guide-zone="6">
            <div class="exp-guide-card-head">
              <span class="exp-guide-num">6</span>
              <h4 class="exp-guide-card-title">Capot Concepteur &amp; Statut Moteur</h4>
            </div>
            <div class="exp-guide-samples">
              <span class="exp-dt-pill">✦ Choix / ⚖️ Renoncement</span>
              <span class="exp-dt-pill">🤖 Bot · 💎 Prix DT · 🧪 Témoins</span>
              <span class="exp-profile-tab is-future">[B] / [C] Phase 5</span>
              <span class="exp-sync-badge is-verified">ACTIVE_VERIFIED</span>
            </div>
            <p class="exp-guide-text">
              Tiroir dépliable rassemblant le dilemme <em>Choix / Renoncement</em>, l’heuristique bot, le prix estimé en Défenseurs-tours (<code>DT</code>), les scénarios témoins et l’aperçu des variantes Phase 5 (<code>B</code>/<code>C</code>). Le badge vert <strong>ACTIVE_VERIFIED</strong> certifie que la tuile est codée dans le simulateur Python et couverte par ses tests témoins.
            </p>
          </article>
        </div>
      </section>
    `;
  }

  function renderToolbar(matchedCount, totalCatalog, xray) {
    const f = explorerState.filters;
    const peuplesMap = getPeuplesMap();

    // Construire la liste des ressources/états présents dans le catalogue
    const stateTokens = Object.keys(STATE_META);

    const activeChips = [];
    if (f.search) activeChips.push({ key: 'search', label: `Texte: "${f.search}"` });
    if (f.family !== 'ALL') activeChips.push({ key: 'family', label: `Famille: ${f.family}` });
    if (f.peuple !== 'ALL') activeChips.push({ key: 'peuple', label: `Peuple: ${f.peuple}` });
    if (f.role !== 'ALL') activeChips.push({ key: 'role', label: `Rôle: ${f.role}` });
    if (f.icon !== 'ALL') {
      const ic = GUARDIAN_ICON_BY_ID[f.icon];
      activeChips.push({ key: 'icon', label: `Icône: ${ic ? ic.icon + ' ' + ic.label : f.icon}` });
    }
    if (f.stateToken !== 'ALL') {
      const sm = getStateMeta(f.stateToken);
      activeChips.push({ key: 'stateToken', label: `État: ${sm.icon} ${sm.label}` });
    }
    if (f.inCircleOnly) activeChips.push({ key: 'inCircleOnly', label: 'En jeu (2N)' });

    return `
      <div class="exp-shell" data-explorer-mode="${explorerState.mode}">
        <div class="exp-topbar">
          <div class="exp-topbar-row">
            <div class="exp-mode-switcher" role="tablist" aria-label="Modes de l’Explorateur">
              <button type="button" role="tab" aria-selected="${explorerState.mode === 'lisieres'}" class="exp-mode-btn ${explorerState.mode === 'lisieres' ? 'is-active' : ''}" data-mode-btn="lisieres" onclick="AmazoniaExplorerV62.setMode('lisieres')">
                <span>⚖️ 1. Les 15 Lisières</span>
                <span class="exp-mode-sub">Face-à-face</span>
              </button>
              <button type="button" role="tab" aria-selected="${explorerState.mode === 'assises'}" class="exp-mode-btn ${explorerState.mode === 'assises' ? 'is-active' : ''}" data-mode-btn="assises" onclick="AmazoniaExplorerV62.setMode('assises')">
                <span>🎡 2. Table &amp; 197 Assises</span>
                <span class="exp-mode-sub">Roue &amp; Santé</span>
              </button>
              <button type="button" role="tab" aria-selected="${explorerState.mode === 'peuples'}" class="exp-mode-btn ${explorerState.mode === 'peuples' ? 'is-active' : ''}" data-mode-btn="peuples" onclick="AmazoniaExplorerV62.setMode('peuples')">
                <span>🧬 3. Grammaires (3+3)</span>
                <span class="exp-mode-sub">Par Peuple</span>
              </button>
            </div>

            <div class="exp-topbar-actions">
              <span id="exp-dynamic-counter" class="exp-counter-pill">${matchedCount} / ${totalCatalog} tuiles affichées</span>
              <button type="button" class="exp-btn" onclick="AmazoniaExplorerV62.toggleAllCapots()">
                ${explorerState.allCapotsOpen ? '▾ Tout replier (Capot)' : '▸ Tout déplier (Capot)'}
              </button>
              <button type="button" id="exp-reading-guide-btn" class="exp-btn exp-guide-toggle-btn ${explorerState.readingGuideOpen ? 'is-active' : ''}" aria-expanded="${explorerState.readingGuideOpen ? 'true' : 'false'}" aria-controls="exp-reading-guide-panel" onclick="AmazoniaExplorerV62.toggleReadingGuide()">
                ? Guide de lecture
              </button>
              <button type="button" class="exp-btn ${hasAnyActiveFilter() || explorerState.xrayFocusId ? 'exp-btn-primary' : ''}" onclick="AmazoniaExplorerV62.resetFilters()">
                ↺ Réinitialiser
              </button>
            </div>
          </div>

          <div class="exp-filters-grid">
            <div class="exp-field">
              <label for="exp-filter-search">Recherche texte</label>
              <input id="exp-filter-search" type="text" class="exp-input" value="${escapeHtml(f.search)}" placeholder="ID, nom, effet, twist, témoin…" oninput="AmazoniaExplorerV62.setFilter('search', this.value)" />
            </div>

            <div class="exp-field">
              <label for="exp-filter-family">Famille</label>
              <select id="exp-filter-family" class="exp-select" onchange="AmazoniaExplorerV62.setFilter('family', this.value)">
                <option value="ALL" ${f.family === 'ALL' ? 'selected' : ''}>Toutes (30)</option>
                <option value="GARDIEN" ${f.family === 'GARDIEN' ? 'selected' : ''}>🛡️ Gardiens (15)</option>
                <option value="REVE" ${f.family === 'REVE' ? 'selected' : ''}>🌙 Rêves (10)</option>
                <option value="CROISSANCE" ${f.family === 'CROISSANCE' ? 'selected' : ''}>🪹 Nids (5)</option>
              </select>
            </div>

            <div class="exp-field">
              <label for="exp-filter-peuple">Peuple</label>
              <select id="exp-filter-peuple" class="exp-select" onchange="AmazoniaExplorerV62.setFilter('peuple', this.value)">
                <option value="ALL" ${f.peuple === 'ALL' ? 'selected' : ''}>Tous (6)</option>
                ${PEUPLE_CANON_ORDER.map(c => {
                  const p = peuplesMap[c] || { icon: '', nom: c };
                  return `<option value="${c}" ${f.peuple === c ? 'selected' : ''}>${getPeupleSelectOptionIcon(c, p.icon)} ${c} · ${escapeHtml(p.nom)}</option>`;
                }).join('')}
              </select>
            </div>

            <div class="exp-field">
              <label for="exp-filter-role">Rôle modèle</label>
              <select id="exp-filter-role" class="exp-select" onchange="AmazoniaExplorerV62.setFilter('role', this.value)">
                <option value="ALL" ${f.role === 'ALL' ? 'selected' : ''}>Tous les rôles</option>
                <option value="TWIST" ${f.role === 'TWIST' ? 'selected' : ''}>⚡ Twist 2K3 (6)</option>
                <option value="LOI_PASSIVE" ${f.role === 'LOI_PASSIVE' ? 'selected' : ''}>⚖️ Loi passive (2)</option>
                <option value="CATALYSEUR_EVEIL" ${f.role === 'CATALYSEUR_EVEIL' ? 'selected' : ''}>☀️ Catalyseur d’Éveil (9)</option>
                <option value="LEVIER_REVE" ${f.role === 'LEVIER_REVE' ? 'selected' : ''}>🌙 Levier de Rêve (3)</option>
                <option value="ENRACINEMENT" ${f.role === 'ENRACINEMENT' ? 'selected' : ''}>🌱 Enracinement (4)</option>
                <option value="AUTONOME_A0" ${f.role === 'AUTONOME_A0' ? 'selected' : ''}>🔓 Autonome A=0 (6)</option>
                <option value="BRIQUE_FLUIDE" ${f.role === 'BRIQUE_FLUIDE' ? 'selected' : ''}>🌊 Brique fluide (22)</option>
              </select>
            </div>

            <div class="exp-field">
              <label for="exp-filter-icon">Icône Gardien (v6.2)</label>
              <select id="exp-filter-icon" class="exp-select" onchange="AmazoniaExplorerV62.setFilter('icon', this.value)">
                <option value="ALL" ${f.icon === 'ALL' ? 'selected' : ''}>Toutes les 6 icônes</option>
                ${GUARDIAN_ICONS_V62.map(ic => `<option value="${ic.id}" ${f.icon === ic.id ? 'selected' : ''}>${ic.icon} ${escapeHtml(ic.label)}</option>`).join('')}
              </select>
            </div>

            <div class="exp-field">
              <label for="exp-filter-state">Ressource / État</label>
              <select id="exp-filter-state" class="exp-select" onchange="AmazoniaExplorerV62.setFilter('stateToken', this.value)">
                <option value="ALL" ${f.stateToken === 'ALL' ? 'selected' : ''}>Tous les états</option>
                ${stateTokens.map(tok => {
                  const m = STATE_META[tok];
                  return `<option value="${tok}" ${f.stateToken === tok ? 'selected' : ''}>${m.icon} ${escapeHtml(m.label)}</option>`;
                }).join('')}
              </select>
            </div>
          </div>

          <div class="exp-filters-footer">
            <div class="exp-active-filters">
              <label class="exp-checkbox-pill ${f.inCircleOnly ? 'is-checked' : ''}">
                <input type="checkbox" ${f.inCircleOnly ? 'checked' : ''} onchange="AmazoniaExplorerV62.setFilter('inCircleOnly', this.checked)" />
                <span>✓ Uniquement les 2N tuiles en jeu (${getCurrentCircle().join('–')})</span>
              </label>
              ${activeChips.map(ch => `
                <span class="exp-filter-chip">
                  ${escapeHtml(ch.label)}
                  <button type="button" onclick="AmazoniaExplorerV62.clearSingleFilter('${ch.key}')" aria-label="Retirer ce filtre">✕</button>
                </span>
              `).join('')}
            </div>
            <span style="color:#64748b;font-size:0.71rem;">Astuce : cliquez sur n’importe quelle puce d’état en pied de carte pour filtrer instantanément.</span>
          </div>
        </div>

        ${renderReadingGuide()}
        ${renderXRayBanner(xray)}
      </div>
    `;
  }

  // --------------------------------------------------------------------------
  // Rendu complet & API d'interaction
  // --------------------------------------------------------------------------
  function bindEscapeKeyOnce() {
    if (explorerState.escapeBound) return;
    if (typeof global.document !== 'undefined' && typeof global.document.addEventListener === 'function') {
      global.document.addEventListener('keydown', function (ev) {
        if (ev && ev.key === 'Escape') {
          if (explorerState.xrayFocusId) {
            clearXRay();
          } else if (explorerState.readingGuideOpen) {
            toggleReadingGuide(false);
          }
        }
      });
      explorerState.escapeBound = true;
    }
  }

  function renderModeHtml(targetMode) {
    const mode = targetMode || explorerState.mode;
    const cat = getCatalogue();
    const totalCatalog = Object.keys(cat).length;
    const { matched, activeCircleSet } = getFilteredTileIdSet();
    let xray = null;
    if (explorerState.xrayFocusId) {
      if (mode === 'assises') {
        const health = computeAssiseHealth(getCurrentCircle());
        xray = computeXRayGraph(explorerState.xrayFocusId, health.tileIds, {
          activeModules: health.modules,
          activePeuples: health.circle,
          scopeLabel: `Table ${health.canonKey} (${health.tileIds.length} tuiles)`
        });
      } else {
        xray = computeXRayGraph(explorerState.xrayFocusId, null, {
          scopeLabel: `Catalogue complet (${totalCatalog} tuiles)`
        });
      }
    }

    let stage = { displayedCount: 0, html: '' };
    if (mode === 'assises') {
      stage = renderMode2Assises(matched, activeCircleSet, xray);
    } else if (mode === 'peuples') {
      stage = renderMode3Peuples(matched, activeCircleSet, xray);
    } else {
      stage = renderMode1Lisieres(matched, activeCircleSet, xray);
    }

    return {
      mode,
      matchedCount: matched.size,
      displayedCount: stage.displayedCount,
      totalCatalog,
      toolbarHtml: renderToolbar(matched.size, totalCatalog, xray),
      stageHtml: stage.html
    };
  }

  function render() {
    bindEscapeKeyOnce();
    if (typeof global.document === 'undefined') return null;

    const legacyFilters = global.document.getElementById('legacy-catalogue-filters');
    if (legacyFilters && legacyFilters.classList) {
      legacyFilters.classList.add('hidden');
    }

    const res = renderModeHtml(explorerState.mode);
    const toolbarEl = global.document.getElementById('explorer-v6-2-toolbar');
    const gridEl = global.document.getElementById('catalogue-grid');
    const badgeEl = global.document.getElementById('catalogue-count-badge');

    if (toolbarEl) {
      toolbarEl.innerHTML = res.toolbarHtml;
    }
    if (gridEl) {
      gridEl.className = 'exp-stage';
      gridEl.innerHTML = res.stageHtml;
    }
    if (badgeEl) {
      badgeEl.textContent = `${res.matchedCount} / ${res.totalCatalog} tuiles affichées`;
    }
    return res;
  }

  function syncStudioAfterCircleChange() {
    const st = getStudioState();
    if (st) st.bundleId = 'CUSTOM';
    if (typeof global.document !== 'undefined') {
      const sel = global.document.getElementById('preset-bundle-select');
      if (sel) sel.value = 'CUSTOM';
    }
    if (typeof global.refreshAllUI === 'function') {
      global.refreshAllUI();
    } else {
      render();
    }
  }

  function setMode(mode) {
    if (!['lisieres', 'assises', 'peuples'].includes(mode)) return;
    explorerState.mode = mode;
    explorerState.wheelSelection = null;
    render();
  }

  function setPeupleTab(code) {
    if (!PEUPLE_CANON_ORDER.includes(code)) return;
    explorerState.activePeupleTab = code;
    render();
  }

  function setFilter(key, value) {
    if (!(key in explorerState.filters)) return;
    explorerState.filters[key] = value;
    render();
    // Conserver le focus sur la barre de recherche en saisie interactive
    if (key === 'search' && typeof global.document !== 'undefined') {
      const inp = global.document.getElementById('exp-filter-search');
      if (inp && typeof inp.focus === 'function') {
        inp.focus();
        if (typeof inp.setSelectionRange === 'function') {
          const len = String(value || '').length;
          inp.setSelectionRange(len, len);
        }
      }
    }
  }

  function clearSingleFilter(key) {
    if (key === 'search') explorerState.filters.search = '';
    else if (key === 'inCircleOnly') explorerState.filters.inCircleOnly = false;
    else if (key in explorerState.filters) explorerState.filters[key] = 'ALL';
    render();
  }

  function resetFilters() {
    explorerState.filters = {
      search: '',
      family: 'ALL',
      peuple: 'ALL',
      role: 'ALL',
      icon: 'ALL',
      stateToken: 'ALL',
      inCircleOnly: false
    };
    explorerState.xrayFocusId = null;
    explorerState.wheelSelection = null;
    render();
  }

  function toggleStateChipFilter(token) {
    explorerState.filters.stateToken = explorerState.filters.stateToken === token ? 'ALL' : token;
    render();
  }

  function toggleXRay(tileId) {
    explorerState.xrayFocusId = explorerState.xrayFocusId === tileId ? null : tileId;
    render();
  }

  function clearXRay() {
    explorerState.xrayFocusId = null;
    render();
  }

  function toggleCapot(tileId) {
    if (explorerState.allCapotsOpen) {
      // Passer en contrôle individuel avec tous ouverts sauf celui-ci
      const allIds = Object.keys(getCatalogue());
      explorerState.allCapotsOpen = false;
      explorerState.capotOpenIds = new Set(allIds.filter(id => id !== tileId));
    } else if (explorerState.capotOpenIds.has(tileId)) {
      explorerState.capotOpenIds.delete(tileId);
    } else {
      explorerState.capotOpenIds.add(tileId);
    }
    render();
  }

  function toggleAllCapots() {
    explorerState.allCapotsOpen = !explorerState.allCapotsOpen;
    if (!explorerState.allCapotsOpen) {
      explorerState.capotOpenIds.clear();
    }
    render();
  }

  function toggleReadingGuide(forceState) {
    if (typeof forceState === 'boolean') {
      explorerState.readingGuideOpen = forceState;
    } else {
      explorerState.readingGuideOpen = !explorerState.readingGuideOpen;
    }
    render();
  }

  function selectPresetAssise(presetKey) {
    const preset = PRESET_ASSISES.find(p => p.key === presetKey);
    if (!preset) return;
    const st = getStudioState();
    st.peuplesCercle = preset.peuples.slice();
    explorerState.wheelSelection = null;
    syncStudioAfterCircleChange();
  }

  function selectAssiseByKey(canonKey) {
    enumerateAll197Assises();
    const found = _cached197ByKey && _cached197ByKey[canonKey];
    if (!found) return;
    const st = getStudioState();
    st.peuplesCercle = found.peuples.slice();
    explorerState.wheelSelection = null;
    syncStudioAfterCircleChange();
  }

  function toggleTablePeuple(code) {
    if (!PEUPLE_CANON_ORDER.includes(code)) return;
    const st = getStudioState();
    const circle = getCurrentCircle();
    const idx = circle.indexOf(code);
    if (idx >= 0) {
      if (circle.length <= 3) return;
      circle.splice(idx, 1);
    } else {
      circle.push(code);
    }
    st.peuplesCercle = circle;
    explorerState.wheelSelection = null;
    syncStudioAfterCircleChange();
  }

  function swapTableSeats(idxA, idxB) {
    const st = getStudioState();
    const circle = getCurrentCircle();
    if (idxA < 0 || idxB < 0 || idxA >= circle.length || idxB >= circle.length) return;
    const tmp = circle[idxA];
    circle[idxA] = circle[idxB];
    circle[idxB] = tmp;
    st.peuplesCercle = circle;
    explorerState.wheelSelection = null;
    syncStudioAfterCircleChange();
  }

  function rotateTable(dir) {
    const st = getStudioState();
    const circle = getCurrentCircle();
    if (circle.length < 2) return;
    if (dir < 0) {
      circle.push(circle.shift());
    } else {
      circle.unshift(circle.pop());
    }
    st.peuplesCercle = circle;
    syncStudioAfterCircleChange();
  }

  function reverseTable() {
    const st = getStudioState();
    const circle = getCurrentCircle();
    st.peuplesCercle = circle.reverse();
    syncStudioAfterCircleChange();
  }

  function selectWheelFilter(kind, arg1, arg2) {
    const cur = explorerState.wheelSelection;
    if (kind === 'peuple') {
      if (cur && cur.kind === 'peuple' && cur.code === arg1) {
        explorerState.wheelSelection = null;
      } else {
        explorerState.wheelSelection = { kind: 'peuple', code: arg1 };
      }
    } else if (kind === 'border') {
      if (cur && cur.kind === 'border' && cur.p1 === arg1 && cur.p2 === arg2) {
        explorerState.wheelSelection = null;
      } else {
        explorerState.wheelSelection = { kind: 'border', p1: arg1, p2: arg2 };
      }
    }
    render();
    if (explorerState.wheelSelection && typeof global.document !== 'undefined') {
      const anchor = global.document.getElementById('exp-assises-cards-anchor');
      if (anchor && typeof anchor.scrollIntoView === 'function') {
        anchor.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }
    }
  }

  function clearWheelFilter() {
    explorerState.wheelSelection = null;
    render();
  }

  function getFilteredSelection() {
    const cat = getCatalogue();
    const { matched } = getFilteredTileIdSet();
    const isUnfiltered = !hasAnyActiveFilter();
    const selected = {};
    let profileCount = 0;
    const st = getStudioState();

    for (const tileId of matched) {
      const t = cat[tileId];
      if (!t) continue;
      const letter = (st && st.profileOverrides && st.profileOverrides[tileId]) || 'A';
      const prof = t.profils[letter] || t.profils.A;
      if (!prof) continue;
      profileCount++;
      selected[tileId] = {
        id: t.id,
        famille: t.famille,
        couple: t.couple,
        origine: t.origine,
        nomBase: t.nomBase,
        profil_actif_instance: letter,
        profils: { [letter]: prof }
      };
    }

    return { isUnfiltered, profileCount, selected };
  }

  function getState() {
    return {
      mode: explorerState.mode,
      activePeupleTab: explorerState.activePeupleTab,
      xrayFocusId: explorerState.xrayFocusId,
      allCapotsOpen: explorerState.allCapotsOpen,
      capotOpenIds: Array.from(explorerState.capotOpenIds),
      readingGuideOpen: explorerState.readingGuideOpen,
      wheelSelection: explorerState.wheelSelection,
      filters: Object.assign({}, explorerState.filters)
    };
  }

  const api = {
    VERSION,
    PEUPLE_CANON_ORDER,
    GUARDIAN_ICONS_V62,
    STATE_META,
    VECTOR_DEFS_V62,
    PEUPLE_ACCESSORIES_V62,
    PRESET_ASSISES,
    LISIERES_100PC_FLUIDES: ['E-O', 'H-M', 'R-I'],
    normalizeDeclencheurToIconId,
    getNormalizedTileTriggers,
    formatVectorTooltip,
    canonicalizeAssise,
    enumerateAll197Assises,
    getAssiseTilesAndBorders,
    computeAssiseHealth,
    computeXRayGraph,
    computeBorderDivergence,
    parseTileFaces,
    getState,
    setMode,
    setPeupleTab,
    setFilter,
    clearSingleFilter,
    resetFilters,
    toggleStateChipFilter,
    toggleXRay,
    clearXRay,
    toggleCapot,
    toggleAllCapots,
    toggleReadingGuide,
    selectPresetAssise,
    selectAssiseByKey,
    toggleTablePeuple,
    swapTableSeats,
    rotateTable,
    reverseTable,
    selectWheelFilter,
    clearWheelFilter,
    getFilteredSelection,
    renderModeHtml,
    render
  };

  global.AmazoniaExplorerV62 = api;
  if (typeof global.window !== 'undefined') {
    global.window.AmazoniaExplorerV62 = api;
  }
})(typeof window !== 'undefined' ? window : globalThis);
