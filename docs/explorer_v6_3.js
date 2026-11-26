/* ============================================================================
 * Amazonia Doc Studio — Explorateur Bi-Composant & Atelier Draft (v6.3.1)
 * Module vanilla JS pur sans bundler (100 % file://, GitHub Pages & Node vm).
 * ============================================================================ */
(function (global) {
  'use strict';

  const VERSION = '6.3.1';
  const STORAGE_KEY = 'amazonia_atelier_v6_3_workspace_v1';
  const PEUPLE_ORDER = ['H', 'E', 'M', 'R', 'O', 'I'];
  const ANIMAL_PEUPLES = new Set(['M', 'R', 'O']);
  const NON_ANIMAL_PEUPLES = new Set(['H', 'E', 'I']);
  const ONIRIQUE_PEUPLES = new Set(['H', 'E']);
  const PANEL_IDS = ['panel_1', 'panel_2', 'panel_3'];
  const PANEL_LABELS = {
    panel_1: 'Panel 1',
    panel_2: 'Panel 2',
    panel_3: 'Panel 3',
    canon: 'Mon Canon v6.3',
    archive_v6_2: 'Archive v6.2'
  };
  const PANEL_SHORT = {
    panel_1: 'P1',
    panel_2: 'P2',
    panel_3: 'P3',
    custom: 'Hybride'
  };

  const A0_SLOTS = new Set(['R1', 'R2', 'R6', 'R10', 'M4', 'M5']);
  const I_SLOTS = new Set(['G13', 'G14', 'G15', 'R6', 'R10', 'M1', 'M2', 'M3', 'M4', 'M5']);
  const ANIMAL_ANIMAL_BORDERS = [['M', 'R'], ['M', 'O'], ['R', 'O']];
  const E_NON_H_BORDERS = [['E', 'M'], ['E', 'R'], ['E', 'O'], ['E', 'I']];

  const BORDER_GROUPS = [
    {
      id: 'animal-animal',
      title: 'Lisières Animal ↔ Animal',
      subtitle: '6 Gardiens purs — couverture Éveil entre Animaux sauvages',
      pairs: [['M', 'R'], ['M', 'O'], ['R', 'O']]
    },
    {
      id: 'animal-autre',
      title: 'Ponts Animal ↔ Autre Peuple',
      subtitle: '9 Gardiens face à 6 Rêves & 3 Nids — ponts entre Éveil, Sommeil et Essaim',
      pairs: [
        ['M', 'H'], ['M', 'E'], ['M', 'I'],
        ['R', 'H'], ['R', 'E'], ['R', 'I'],
        ['O', 'H'], ['O', 'E'], ['O', 'I']
      ]
    },
    {
      id: 'sans-animal',
      title: 'Lisières sans Animal (Autonomie A=0)',
      subtitle: '4 Rêves & 2 Nids autonomes — 100 % jouables sans Piste des Gardiens',
      pairs: [['H', 'E'], ['H', 'I'], ['E', 'I']]
    }
  ];

  const ALL_15_BORDERS = BORDER_GROUPS.reduce((acc, g) => acc.concat(g.pairs), []);

  const GUARDIAN_ICONS = [
    { id: 'ICONE_PARADE', key: 'PARADE', label: 'Parade', icon: '🛡️', desc: 'Parade classique par Défenseurs seuls' },
    { id: 'ICONE_PIEGEAGE', key: 'PIEGEAGE', label: 'Piégeage', icon: '🪤', desc: 'Frappe arrêtée par un Piège autonome ou le Croc' },
    { id: 'ICONE_SABOTAGE', key: 'SABOTAGE', label: 'Sabotage', icon: '💥', desc: 'Jeton Sabotage ou Écaille révélé à l’ouverture' },
    { id: 'ICONE_REVE', key: 'REVE', label: 'Rêve', icon: '🌙', desc: 'Rêve défendu annulant au moins une machine' },
    { id: 'ICONE_INSECTE', key: 'INSECTE', label: 'Insecte', icon: '🐜', desc: 'Déviation ±1 ou Parade avec Insectes (actif si I joue)' },
    { id: 'ICONE_RESONANCE', key: 'RESONANCE', label: 'Résonance', icon: '🔔', desc: '6e icône : compteur des 1res activations des autres Gardiens' }
  ];
  const GUARDIAN_ICON_BY_ID = Object.fromEntries(GUARDIAN_ICONS.map(ic => [ic.id, ic]));

  const PEUPLE_META = {
    M: { code: 'M', nom: 'Mammifères', short: 'Mammifères', icon: '🐆' },
    R: { code: 'R', nom: 'Reptiles', short: 'Reptiles', icon: 'R_SVG' },
    O: { code: 'O', nom: 'Oiseaux', short: 'Oiseaux', icon: '🦜' },
    H: { code: 'H', nom: 'Humains', short: 'Humains', icon: '🥁' },
    E: { code: 'E', nom: 'Entités Magiques', short: 'Entités', icon: '✨' },
    I: { code: 'I', nom: 'Insectes', short: 'Insectes', icon: '🐜' }
  };

  const PEUPLE_SVG_COLORS = {
    M: { fill: '#fef3c7', stroke: '#d97706', text: '#92400e' },
    R: { fill: '#d1fae5', stroke: '#059669', text: '#065f46' },
    O: { fill: '#e0f2fe', stroke: '#0284c7', text: '#075985' },
    H: { fill: '#ffe4e6', stroke: '#e11d48', text: '#9f1239' },
    E: { fill: '#ede9fe', stroke: '#7c3aed', text: '#5b21b6' },
    I: { fill: '#ecfccb', stroke: '#65a30d', text: '#3f6212' }
  };

  // Accessoires 3+3 (v6.2 verrouillé)
  const ACCESSORIES_3_3 = {
    H: {
      code: 'H',
      tier: 'T1',
      tierLabel: 'Actif dès le Tour 1',
      title: 'Tambour & Chant',
      icon: '🥁',
      summary: 'Tambour posable sur tout rayon dès le 1er temps ; Chant glisse un Rêve d’1 rang à gauche s’il vide son rang.',
      states: ['TAMBOUR', 'CHANT', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION'],
      icons: ['ICONE_PARADE', 'ICONE_REVE']
    },
    M: {
      code: 'M',
      tier: 'T1',
      tierLabel: 'Actif dès le Tour 1',
      title: 'Jeton Duel (Défi ↔ Territoire tenu)',
      icon: '⚔️',
      summary: 'Posé avec un Défenseur M ; parer sur sa parcelle le retourne sur Territoire tenu (bloque l’avancée +1).',
      states: ['DUEL', 'TERRITOIRE', 'GARDIEN'],
      icons: ['ICONE_PARADE']
    },
    O: {
      code: 'O',
      tier: 'T1',
      tierLabel: 'Actif dès le Tour 1',
      title: 'Dé d’Envol · Perchoir · Plume de Vigie',
      icon: '🪶',
      summary: 'Servi dernier au sac (garde 1, pose 1 caché au Perchoir) ; choix min(D1,D2) ou Dé d’Envol ; Plume Chaud/Calme.',
      states: ['DE_ENVOL', 'PERCHOIR', 'PLUME', 'RANG_MACHINE', 'GARDIEN'],
      icons: []
    },
    E: {
      code: 'E',
      tier: 'PROG',
      tierLabel: 'Progressif via tuiles',
      title: 'Jetons d’Altération',
      icon: '🌀',
      summary: 'Posés sur machine mobile (max 1) : à sa révélation, compte dans m(r) mais recule d’1 parcelle sans frapper.',
      states: ['ALTERATION', 'ALTEREE', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION'],
      icons: ['ICONE_REVE']
    },
    R: {
      code: 'R',
      tier: 'PROG',
      tierLabel: 'Progressif via tuiles',
      title: '4 Écailles · Croc · Cales',
      icon: '🦷',
      summary: 'Écaille allume Sabotage et pose le Croc réutilisable (cohabite avec Piège, pare en premier) ; max 1 cale/machine.',
      states: ['ECAILLE', 'CROC', 'CALE', 'SABOTAGE', 'GARDIEN'],
      icons: ['ICONE_SABOTAGE', 'ICONE_PIEGEAGE']
    },
    I: {
      code: 'I',
      tier: 'PROG',
      tierLabel: 'Progressif via tuiles',
      title: 'Essaim · Nids · Déviation ±1 · Bouclier',
      icon: '🐜',
      summary: 'Production des Nids (+1/+2), Migration, Déviation de dé ±1, Parade Insecte et Bouclier de lisière.',
      states: ['INSECTE', 'INSECTE_RANG', 'NID', 'NID_ACTIVE'],
      icons: ['ICONE_INSECTE']
    }
  };

  const SOCLE_STATES = new Set([
    'ARBRE', 'SOUCHE', 'ROUTE', 'ROUGE', 'DEFENSEUR_ATTENTE', 'DEFENSEUR_REDEPLOYE',
    'PIEGE', 'SABOTAGE', 'MOBILISATION', 'RANG_MACHINE', 'DES_SOUS_PARAVENT',
    'FURTIVITE', 'RATISSAGE'
  ]);

  const PEUPLE_NATIVE_STATES = {
    H: new Set(['TAMBOUR', 'CHANT', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION']),
    E: new Set(['POSITION_REVE', 'RANG_REVE', 'ANNULATION']),
    M: new Set(['DUEL', 'TERRITOIRE', 'GARDIEN']),
    R: new Set(['GARDIEN']),
    O: new Set(['DE_ENVOL', 'PERCHOIR', 'PLUME', 'GARDIEN']),
    I: new Set(['INSECTE', 'INSECTE_RANG', 'NID', 'NID_ACTIVE'])
  };

  const PROGRESSIVE_RESERVE_OWNER = {
    ALTEREE: 'E',
    ALTERATION: 'E',
    ECAILLE: 'R',
    CROC: 'R'
  };

  const PRESET_TABLES = [
    { key: 'N3-HEI', peuples: ['H', 'E', 'I'], label: '{H, E, I}', tag: 'A=0 · Sans Gardiens' },
    { key: 'N3-ERO', peuples: ['E', 'R', 'O'], label: '{E, R, O}', tag: 'E sans H' },
    { key: 'N3-ERI', peuples: ['E', 'R', 'I'], label: '{E, R, I}', tag: 'E sans H + Essaim' },
    { key: 'N3-MRO', peuples: ['M', 'R', 'O'], label: '{M, R, O}', tag: '100 % Gardiens' },
    { key: 'N3-MIR', peuples: ['M', 'I', 'R'], label: '{M, I, R}', tag: 'Triade M–I–R' },
    { key: 'N4-HEMR', peuples: ['H', 'E', 'M', 'R'], label: '{H, E, M, R}', tag: 'Table 4J mixte' },
    { key: 'N6-HEMROI', peuples: ['H', 'E', 'M', 'R', 'O', 'I'], label: 'Table à 6', tag: '6 Peuples · 12 tuiles' }
  ];

  // Dictionnaire humain exhaustif des ressources / états (zéro code brut exposé)
  const RESOURCE_META = {
    BLEU: { icon: '🔵', label: 'Bleu Surchauffe', kind: 'state' },
    ROUGE: { icon: '🔴', label: 'Rouge (+1)', kind: 'state' },
    ROUGE_RETOURNE: { icon: '🔵', label: 'Rouge → Bleu', kind: 'state', canon: 'BLEU' },
    ALTERATION: { icon: '🌀', label: 'Altération', kind: 'state' },
    ALTEREE: { icon: '🌀', label: 'Altération', kind: 'state', canon: 'ALTERATION' },
    CROC: { icon: '🦷', label: 'Croc Reptile', kind: 'state' },
    CROC_POSTE: { icon: '🦷', label: 'Croc posté', kind: 'state', canon: 'CROC' },
    DUEL: { icon: '⚔️', label: 'Jeton Duel', kind: 'state' },
    DEFI: { icon: '⚔️', label: 'Duel (Défi)', kind: 'state', canon: 'DUEL' },
    TERRITOIRE: { icon: '🏰', label: 'Territoire tenu', kind: 'state' },
    PLUME: { icon: '🪶', label: 'Plume de Vigie', kind: 'state' },
    PERCHOIR: { icon: '🦅', label: 'Perchoir', kind: 'state' },
    DE_ENVOL: { icon: '🎲', label: 'Dé d’Envol', kind: 'state' },
    DES_SOUS_PARAVENT: { icon: '🎲', label: 'Dés sous paravent', kind: 'state' },
    TAMBOUR: { icon: '🥁', label: 'Tambour', kind: 'state' },
    CHANT: { icon: '🎶', label: 'Chant', kind: 'state' },
    CHAMANE_EN_FORET: { icon: '🥁', label: 'Chamane en forêt', kind: 'state' },
    INSECTE: { icon: '🐜', label: 'Insecte', kind: 'state' },
    INSECTE_PASSAGER: { icon: '🐞', label: 'Insecte passager', kind: 'state' },
    INSECTE_RANG: { icon: '🐜', label: 'Insecte (Réglette)', kind: 'state' },
    INSECTE_TRANSPORTE: { icon: '🐞', label: 'Insecte transporté', kind: 'state', canon: 'INSECTE' },
    INSECTES_TRANSPORTES: { icon: '🐞', label: 'Insectes transportés', kind: 'state', canon: 'INSECTE' },
    INSECTES_EN_CONVOI: { icon: '🐞', label: 'Convoi d’Insectes', kind: 'state', canon: 'INSECTE' },
    INSECTE_ICONE: { icon: '🐜', label: 'Insecte sur icône', kind: 'state', canon: 'INSECTE' },
    INSECTE_IMMERGE: { icon: '🐜', label: 'Insecte déployé', kind: 'state', canon: 'INSECTE' },
    INSECTE_RAPATRIE: { icon: '🐜', label: 'Insecte rapatrié', kind: 'state', canon: 'INSECTE' },
    INSECTE_RAPPELE: { icon: '🐜', label: 'Insecte rappelé', kind: 'state', canon: 'INSECTE' },
    PONTE: { icon: '🐜', label: 'Ponte d’Insectes', kind: 'state', canon: 'INSECTE' },
    RIPOSTE_ESSAIM: { icon: '🐜', label: 'Riposte Essaim', kind: 'state', canon: 'INSECTE' },
    PARADE_SOLDATS: { icon: '🐜', label: 'Parade Essaim', kind: 'state', canon: 'INSECTE' },
    PARADE_GALERIE: { icon: '🐜', label: 'Parade souterraine', kind: 'state', canon: 'INSECTE' },
    NID: { icon: '🪹', label: 'Nid', kind: 'state' },
    NID_ACTIVE: { icon: '🪹', label: 'Production de Nid', kind: 'state', canon: 'NID' },
    NID_NOMADE: { icon: '🪹', label: 'Nid nomade', kind: 'state', canon: 'NID' },
    NID_DEPLACE: { icon: '🪹', label: 'Nid déplacé', kind: 'state', canon: 'NID' },
    PIEGE: { icon: '🪤', label: 'Piège autonome', kind: 'state' },
    SABOTAGE: { icon: '💥', label: 'Sabotage (sac)', kind: 'state' },
    ECAILLE: { icon: '🦎', label: 'Écaille (Reptiles)', kind: 'state' },
    CALE: { icon: '🧱', label: 'Cale (Reptiles)', kind: 'state' },
    ARBRE: { icon: '🌳', label: 'Arbre debout', kind: 'state' },
    SOUCHE: { icon: '🪵', label: 'Souche', kind: 'state' },
    SOUCHE_SANCTUARISEE: { icon: '🪵', label: 'Souche protégée', kind: 'state', canon: 'SOUCHE' },
    ROUTE: { icon: '🛣️', label: 'Route forestière', kind: 'state' },
    SENTIER_ROUTE: { icon: '🛣️', label: 'Sentier / Route', kind: 'state', canon: 'ROUTE' },
    RATISSAGE: { icon: '⚙️', label: 'Ratissage', kind: 'state' },
    RATISSAGE_ROMPU: { icon: '⏪', label: 'Ratissage rompu', kind: 'state', canon: 'RECUL' },
    PROIE_ARRACHEE: { icon: '⏪', label: 'Machine arrachée', kind: 'state', canon: 'RECUL' },
    RECUL: { icon: '⏪', label: 'Recul de machine', kind: 'state' },
    RANG_MACHINE: { icon: '🔢', label: 'Rang de machine', kind: 'state' },
    RANG_RELU: { icon: '🔢', label: 'Rang réinterprété', kind: 'state', canon: 'RANG_MACHINE' },
    POSITION_REVE: { icon: '🌙', label: 'Rêve sur Réglette', kind: 'state' },
    RANG_REVE: { icon: '⬅️', label: 'Avancée de Rêve', kind: 'state' },
    PISTON_REVES: { icon: '⬅️', label: 'Piston de Rêves', kind: 'state', canon: 'RANG_REVE' },
    REVE_COMPACTE: { icon: '⬅️', label: 'Rêves compactés', kind: 'state', canon: 'RANG_REVE' },
    GLISSEMENT_CHANT: { icon: '🎶', label: 'Glissement Chant', kind: 'state', canon: 'RANG_REVE' },
    ANNULATION: { icon: '🚫', label: 'Annulation machine', kind: 'state' },
    ANNULATION_ENVOL: { icon: '🚫', label: 'Annulation Envol', kind: 'state', canon: 'ANNULATION' },
    ANNULATION_INDUITE: { icon: '🚫', label: 'Annulation induite', kind: 'state', canon: 'ANNULATION' },
    ANNULATION_RENFORCEE: { icon: '🚫', label: 'Annulation renforcée', kind: 'state', canon: 'ANNULATION' },
    ANNULATION_SURCHAUFFE: { icon: '🚫', label: 'Annulation Surchauffe', kind: 'state', canon: 'ANNULATION' },
    DEFENSEUR_ATTENTE: { icon: '♻️', label: 'Défenseur en attente', kind: 'state' },
    DEFENSEUR_REDEPLOYE: { icon: '🛡️', label: 'Défenseur redéployé', kind: 'state' },
    DEFENSEUR_EVACUE: { icon: '🛡️', label: 'Défenseur évacué', kind: 'state', canon: 'DEFENSEUR_REDEPLOYE' },
    PARADE_CANOPEE: { icon: '🛡️', label: 'Parade canopée', kind: 'state', canon: 'DEFENSEUR_REDEPLOYE' },
    RAID_LATERAL: { icon: '🛡️', label: 'Redéploiement latéral', kind: 'state', canon: 'DEFENSEUR_REDEPLOYE' },
    GARDIEN: { icon: '🗿', label: 'Gardien en piste', kind: 'state' },
    PARI_GLISSE: { icon: '⭐', label: 'Pari en encoche', kind: 'state' },
    PARI_REORIENTE: { icon: '⭐', label: 'Pari réorienté', kind: 'state', canon: 'PARI_GLISSE' },
    ACTIVATION_RELAIS: { icon: '🔔', label: 'Relais de Gardien', kind: 'state', canon: 'GARDIEN' },
    FURTIVITE: { icon: '🌫️', label: 'Furtivité', kind: 'state' },
    MOBILISATION: { icon: '🔥', label: 'Mobilisation m(r)', kind: 'state' },
    JETON_AVALE: { icon: '💥', label: 'Jeton absorbé', kind: 'state', canon: 'SABOTAGE' },
    LANTERNE: { icon: '✨', label: 'Signal lumineux', kind: 'state', canon: 'PLUME' },
    // Icônes Gardiens comme filtres 1-clic
    ICONE_PARADE: { icon: '🛡️', label: 'Icône Parade', kind: 'icon' },
    ICONE_PIEGEAGE: { icon: '🪤', label: 'Icône Piégeage', kind: 'icon' },
    ICONE_SABOTAGE: { icon: '💥', label: 'Icône Sabotage', kind: 'icon' },
    ICONE_REVE: { icon: '🌙', label: 'Icône Rêve', kind: 'icon' },
    ICONE_INSECTE: { icon: '🐜', label: 'Icône Insecte', kind: 'icon' },
    ICONE_RESONANCE: { icon: '🔔', label: 'Icône Résonance', kind: 'icon' }
  };

  // Ressources / Icônes mises en avant dans la barre rapide 1-clic
  const QUICK_RESOURCES = [
    'BLEU', 'ALTERATION', 'CROC', 'DUEL', 'TERRITOIRE', 'PLUME', 'PERCHOIR',
    'INSECTE', 'PIEGE', 'SABOTAGE', 'ECAILLE', 'SOUCHE', 'POSITION_REVE',
    'ICONE_PIEGEAGE', 'ICONE_SABOTAGE', 'ICONE_REVE', 'ICONE_INSECTE', 'ICONE_RESONANCE'
  ];

  // Ponts sémantiques Sortie -> États d'entrée alimentés
  const OUTPUT_FEEDS_STATES = {
    ROUGE_RETOURNE: ['BLEU'],
    ALTEREE: ['ALTERATION', 'ALTEREE'],
    ALTERATION: ['ALTERATION', 'ALTEREE'],
    CROC_POSTE: ['CROC'],
    CROC: ['CROC', 'PIEGE'],
    ECAILLE: ['ECAILLE', 'SABOTAGE', 'CROC'],
    DEFI: ['DUEL'],
    TERRITOIRE: ['TERRITOIRE', 'DUEL'],
    INSECTE_PASSAGER: ['INSECTE_PASSAGER', 'INSECTE'],
    INSECTE_RANG: ['INSECTE_RANG', 'INSECTE'],
    INSECTE_TRANSPORTE: ['INSECTE'],
    INSECTES_TRANSPORTES: ['INSECTE'],
    INSECTES_EN_CONVOI: ['INSECTE'],
    INSECTE_ICONE: ['INSECTE'],
    INSECTE_IMMERGE: ['INSECTE'],
    INSECTE_RAPATRIE: ['INSECTE'],
    INSECTE_RAPPELE: ['INSECTE'],
    PONTE: ['INSECTE'],
    RIPOSTE_ESSAIM: ['INSECTE'],
    PARADE_SOLDATS: ['INSECTE'],
    PARADE_GALERIE: ['INSECTE'],
    NID_ACTIVE: ['NID_ACTIVE', 'NID', 'INSECTE'],
    NID_NOMADE: ['NID', 'INSECTE'],
    NID_DEPLACE: ['NID', 'INSECTE'],
    ANNULATION_ENVOL: ['ANNULATION'],
    ANNULATION_INDUITE: ['ANNULATION'],
    ANNULATION_RENFORCEE: ['ANNULATION'],
    ANNULATION_SURCHAUFFE: ['ANNULATION'],
    PISTON_REVES: ['POSITION_REVE', 'RANG_REVE'],
    REVE_COMPACTE: ['POSITION_REVE', 'RANG_REVE'],
    GLISSEMENT_CHANT: ['POSITION_REVE', 'RANG_REVE', 'CHANT'],
    RANG_REVE: ['RANG_REVE', 'POSITION_REVE'],
    RANG_RELU: ['RANG_MACHINE'],
    DEFENSEUR_EVACUE: ['DEFENSEUR_REDEPLOYE', 'DEFENSEUR_ATTENTE'],
    DEFENSEUR_REDEPLOYE: ['DEFENSEUR_REDEPLOYE', 'DEFENSEUR_ATTENTE'],
    PARADE_CANOPEE: ['DEFENSEUR_REDEPLOYE'],
    RAID_LATERAL: ['DEFENSEUR_REDEPLOYE'],
    CHAMANE_EN_FORET: ['CHAMANE_EN_FORET', 'TAMBOUR', 'CHANT'],
    PARI_GLISSE: ['PARI_GLISSE', 'GARDIEN'],
    PARI_REORIENTE: ['PARI_GLISSE', 'GARDIEN'],
    ACTIVATION_RELAIS: ['GARDIEN'],
    SOUCHE_SANCTUARISEE: ['SOUCHE'],
    SENTIER_ROUTE: ['ROUTE'],
    RATISSAGE_ROMPU: ['RECUL', 'RATISSAGE'],
    PROIE_ARRACHEE: ['RECUL'],
    JETON_AVALE: ['SABOTAGE'],
    LANTERNE: ['PLUME']
  };

  const DRAFT_STATUSES = [
    { value: '', label: 'Statut : —' },
    { value: 'RETENUE', label: '✅ Retenue' },
    { value: 'A_HYBRIDER', label: '🧬 À hybrider' },
    { value: 'HESITATION', label: '🤔 Hésitation' },
    { value: 'ALTERNATIVE', label: '🔄 Alternative' },
    { value: 'ECARTEE', label: '🚫 Écartée' }
  ];

  const PICTO_CATEGORIES = [
    { id: 'FORET', label: '🌿 Forêt & Terrain' },
    { id: 'DEFENSE', label: '🛡️ Défense & Pièges' },
    { id: 'MACHINES', label: '⚙️ Machines & Puissance' },
    { id: 'SAC', label: '🎒 Sac opaque & Paravent' },
    { id: 'PISTE_TACTIQUES', label: '🌙 Réglette & Rêves' },
    { id: 'PISTE_GARDIENS', label: '🗿 Piste des Gardiens' },
    { id: 'ACCESSOIRES', label: '✨ Accessoires 3 + 3' },
    { id: 'ESSAIM', label: '🐜 Module Essaim (Lisières de I)' },
    { id: 'ACTION', label: '⚡ Statuts spéciaux' }
  ];

  const FENETRE_LABELS = {
    ACTIVATION: 'À l’activation',
    OUVERTURE: 'À l’ouverture',
    PRODUCTION: 'À la production',
    PERMANENT: 'Loi permanente',
    'OUVERTURE / ACTIVATION': 'Ouverture / Activation',
    'PRODUCTION / FRAPPE': 'Production / Frappe',
    'RETRAIT ALTÉRATION / OUVERTURE': 'Retrait Altération / Ouverture'
  };

  // --------------------------------------------------------------------------
  // Utilitaires de base & Accès aux données compilées
  // --------------------------------------------------------------------------
  function esc(str) {
    return String(str == null ? '' : str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function deepClone(obj) {
    return obj == null ? obj : JSON.parse(JSON.stringify(obj));
  }

  function normApos(s) {
    return String(s || '').trim().replace(/'/g, '’');
  }

  function getPanelsData() {
    if (typeof PANELS_V6_3 !== 'undefined' && PANELS_V6_3) return PANELS_V6_3;
    if (global.PANELS_V6_3) return global.PANELS_V6_3;
    return {};
  }

  function getPictosRef() {
    if (typeof REFERENTIEL_PICTOGRAMMES_V6_3 !== 'undefined' && REFERENTIEL_PICTOGRAMMES_V6_3) {
      return REFERENTIEL_PICTOGRAMMES_V6_3;
    }
    if (global.REFERENTIEL_PICTOGRAMMES_V6_3) return global.REFERENTIEL_PICTOGRAMMES_V6_3;
    return {};
  }

  function getCastingRef() {
    if (typeof CASTING_GARDIENS_V6_3 !== 'undefined' && CASTING_GARDIENS_V6_3) {
      return CASTING_GARDIENS_V6_3;
    }
    if (global.CASTING_GARDIENS_V6_3) return global.CASTING_GARDIENS_V6_3;
    return {};
  }

  function getSlotsSpec() {
    if (typeof SLOTS_SPEC_V6_3 !== 'undefined' && Array.isArray(SLOTS_SPEC_V6_3)) {
      return SLOTS_SPEC_V6_3;
    }
    if (Array.isArray(global.SLOTS_SPEC_V6_3)) return global.SLOTS_SPEC_V6_3;
    return [];
  }

  function getSlotSpecMap() {
    const map = {};
    getSlotsSpec().forEach(s => { map[s.id] = s; });
    return map;
  }

  function getInitialWorkspaceSeed() {
    if (typeof AUTHOR_WORKSPACE_INITIAL_V6_3 !== 'undefined' && AUTHOR_WORKSPACE_INITIAL_V6_3) {
      return AUTHOR_WORKSPACE_INITIAL_V6_3;
    }
    if (global.AUTHOR_WORKSPACE_INITIAL_V6_3) return global.AUTHOR_WORKSPACE_INITIAL_V6_3;
    return null;
  }

  function getReptileIconHtml(size) {
    const px = Number(size) > 0 ? Number(size) : 14;
    if (
      global.AmazoniaTileIllustrationsV62 &&
      typeof global.AmazoniaTileIllustrationsV62.getReptileIconSvg === 'function'
    ) {
      return global.AmazoniaTileIllustrationsV62.getReptileIconSvg(px);
    }
    return (
      '<svg xmlns="http://www.w3.org/2000/svg" class="exp-peuple-icon-svg exp-peuple-icon-R" ' +
      'data-peuple-icon="R" width="' + px + '" height="' + px + '" viewBox="0 0 24 24" role="img" aria-label="Reptiles">' +
      '<path d="M2 14L5 9L9 7L13 8L21 10C22 10.5 22 12 21 12.5L13 13L20 15.5C19 17.5 13 19 2 17.5Z" fill="#10b981" stroke="#064e3b" stroke-width="1.5"/>' +
      '<circle cx="9.5" cy="10" r="2" fill="#fbbf24" stroke="#064e3b" stroke-width="1"/>' +
      '</svg>'
    );
  }

  function getPeupleIconHtml(code, size) {
    if (code === 'R') return getReptileIconHtml(size || 14);
    const meta = PEUPLE_META[code];
    return meta ? meta.icon : esc(code);
  }

  function getTileMedallionHtml(slotId, famille) {
    if (
      famille === 'GARDIEN' &&
      global.AmazoniaTileIllustrationsV62 &&
      typeof global.AmazoniaTileIllustrationsV62.getTileIllustrationSvg === 'function'
    ) {
      const svg = global.AmazoniaTileIllustrationsV62.getTileIllustrationSvg(slotId);
      if (svg) return '<div class="x3-mini-medallion">' + svg + '</div>';
    }
    return '';
  }

  function humanizeToken(tok) {
    const key = String(tok || '').trim().toUpperCase();
    if (!key) return { icon: '•', label: '', kind: 'state', canon: '' };
    if (RESOURCE_META[key]) {
      return {
        icon: RESOURCE_META[key].icon,
        label: RESOURCE_META[key].label,
        kind: RESOURCE_META[key].kind || 'state',
        canon: RESOURCE_META[key].canon || key
      };
    }
    const clean = key
      .replace(/^ICONE_/, 'Icône ')
      .replace(/^PIC_/, '')
      .toLowerCase()
      .replace(/_/g, ' ')
      .replace(/^\w/, c => c.toUpperCase());
    return { icon: '◆', label: clean, kind: key.startsWith('ICONE_') ? 'icon' : 'state', canon: key };
  }

  function formatFenetreLabel(raw) {
    const s = String(raw || '').trim();
    if (!s) return 'Activation';
    return FENETRE_LABELS[s.toUpperCase()] || s;
  }

  function borderKey(a, b) {
    const idxA = PEUPLE_ORDER.indexOf(a);
    const idxB = PEUPLE_ORDER.indexOf(b);
    return idxA <= idxB ? `${a}-${b}` : `${b}-${a}`;
  }

  function borderLabel(a, b) {
    const idxA = PEUPLE_ORDER.indexOf(a);
    const idxB = PEUPLE_ORDER.indexOf(b);
    return idxA <= idxB ? `${a} ↔ ${b}` : `${b} ↔ ${a}`;
  }

  // Index lisière non orientée -> [slot1, slot2] et jumelle de lisière
  const BORDER_TO_SLOTS = {};
  const TWIN_BY_SLOT = {};
  function ensureBorderMaps() {
    if (Object.keys(TWIN_BY_SLOT).length > 0) return;
    const specs = getSlotsSpec();
    specs.forEach(s => {
      const bk = borderKey(s.origine, s.voisin);
      if (!BORDER_TO_SLOTS[bk]) BORDER_TO_SLOTS[bk] = [];
      BORDER_TO_SLOTS[bk].push(s.id);
    });
    Object.values(BORDER_TO_SLOTS).forEach(pair => {
      if (pair.length === 2) {
        TWIN_BY_SLOT[pair[0]] = pair[1];
        TWIN_BY_SLOT[pair[1]] = pair[0];
      }
    });
  }

  // --------------------------------------------------------------------------
  // Modèle exact des 197 Assises Canoniques (invariance diédrale)
  // --------------------------------------------------------------------------
  let _CACHED_197_ASSISES = null;

  function canonicalizeAssise(peuples) {
    const arr = Array.from(peuples || []);
    const n = arr.length;
    if (n < 3) return { n, peuples: arr, key: `N${n}-${arr.join('')}` };
    const candidates = [];
    for (let dir = 0; dir < 2; dir++) {
      const seq = dir === 0 ? arr : arr.slice().reverse();
      for (let shift = 0; shift < n; shift++) {
        const rot = seq.slice(shift).concat(seq.slice(0, shift));
        candidates.push(rot);
      }
    }
    const rankStr = seq => seq.map(p => PEUPLE_ORDER.indexOf(p)).join(',');
    candidates.sort((a, b) => rankStr(a).localeCompare(rankStr(b)));
    const best = candidates[0];
    return { n, peuples: best, key: `N${n}-${best.join('')}` };
  }

  function enumerateAll197Assises() {
    if (_CACHED_197_ASSISES) return _CACHED_197_ASSISES;
    ensureBorderMaps();
    const seen = new Map();

    function combinations(items, k) {
      const out = [];
      function rec(start, cur) {
        if (cur.length === k) { out.push(cur.slice()); return; }
        for (let i = start; i < items.length; i++) {
          cur.push(items[i]);
          rec(i + 1, cur);
          cur.pop();
        }
      }
      rec(0, []);
      return out;
    }

    function permuteFixedFirst(arr) {
      const first = arr[0];
      const rest = arr.slice(1);
      const out = [];
      function rec(idx) {
        if (idx === rest.length) {
          out.push([first].concat(rest));
          return;
        }
        for (let i = idx; i < rest.length; i++) {
          const tmp = rest[idx]; rest[idx] = rest[i]; rest[i] = tmp;
          rec(idx + 1);
          rest[i] = rest[idx]; rest[idx] = tmp;
        }
      }
      rec(0);
      return out;
    }

    [3, 4, 5, 6].forEach(n => {
      combinations(PEUPLE_ORDER, n).forEach(combo => {
        permuteFixedFirst(combo).forEach(perm => {
          const c = canonicalizeAssise(perm);
          if (!seen.has(c.key)) {
            const tileIds = [];
            for (let i = 0; i < c.peuples.length; i++) {
              const bk = borderKey(c.peuples[i], c.peuples[(i + 1) % c.peuples.length]);
              (BORDER_TO_SLOTS[bk] || []).forEach(tid => tileIds.push(tid));
            }
            seen.set(c.key, {
              n: c.n,
              peuples: c.peuples,
              key: c.key,
              tileIds
            });
          }
        });
      });
    });

    _CACHED_197_ASSISES = Array.from(seen.values());
    return _CACHED_197_ASSISES;
  }

  // --------------------------------------------------------------------------
  // Adaptation Lecture Seule de l'Archive v6.2 (CATALOGUE_TUILES)
  // --------------------------------------------------------------------------
  function buildArchiveV62Tiles() {
    const out = {};
    const cat = typeof CATALOGUE_TUILES !== 'undefined' ? CATALOGUE_TUILES : global.CATALOGUE_TUILES;
    if (!cat) return out;
    const specMap = getSlotSpecMap();

    Object.keys(specMap).forEach(sid => {
      const slot = cat[sid];
      const sp = specMap[sid];
      if (!slot || !slot.profils || !slot.profils.A) return;
      const p = slot.profils.A;
      const rawHtml = String(p.texte || '');
      const parts = rawHtml.split(/<br\s*\/?>/i).map(x => x.replace(/<[^>]+>/g, '').trim()).filter(Boolean);
      let f1 = '';
      let f2 = null;
      let enr = null;
      parts.forEach(pt => {
        const low = pt.toLowerCase();
        const clean = pt.replace(/^\s*(?:Face\s+[12]|Enraciné|Loi\s+passive)\s*:\s*/i, '').trim();
        if (low.startsWith('enraciné')) enr = clean;
        else if (low.startsWith('face 2')) f2 = clean;
        else if (!f1) f1 = clean;
        else if (sp.famille === 'GARDIEN' && f2 === null) f2 = clean;
      });
      const roles = [];
      const tags = (p.tags || []).map(t => String(t).toUpperCase());
      if (tags.includes('CATALYSEUR_EVEIL')) roles.push('CATALYSEUR_EVEIL');
      if (tags.includes('LEVIER_REVE')) roles.push('LEVIER_REVE');
      if (tags.includes('ENRACINEMENT') || enr) roles.push('ENRACINEMENT');
      const isLoi = String(p.nature || '').toLowerCase() === 'loi_passive';
      if (isLoi) roles.push('LOI_PASSIVE');
      const isTwist = Boolean(p.est_twist_canon0);
      if (isTwist) roles.push('TWIST_2K3');
      if (A0_SLOTS.has(sid)) roles.push('AUTONOMIE_A0');

      const dr = p.decision_joueur || {};
      const decls = (p.declencheurs_amorces || []).map(x => String(x).toUpperCase()).filter(x => GUARDIAN_ICON_BY_ID[x]);

      out[sid] = {
        id: sid,
        alias_oriente: sp.alias_oriente,
        famille: sp.famille,
        origine: sp.origine,
        voisin: sp.voisin,
        couple: [sp.origine, sp.voisin],
        cycle: sp.famille === 'GARDIEN' ? 'DOUBLE_FACE_UPGRADE' : (isLoi ? 'PASSIF_CONTINU' : 'SIMPLE_CONTINU'),
        cablage: sp.famille === 'GARDIEN' ? [1, 2, 3, 4, 5, 6] : null,
        roles_portes: roles,
        est_twist: isTwist,
        vecteurs: p.vecteurs || '',
        entrees_plancher: (p.entrees || []).map(x => String(x).toUpperCase()),
        entrees_synergie: [],
        entrees: (p.entrees || []).map(x => String(x).toUpperCase()),
        sorties: (p.sorties || []).map(x => String(x).toUpperCase()),
        paiement: (p.paiement || []).map(x => String(x).toUpperCase()),
        nature: isLoi ? 'LOI_PASSIVE' : 'ACTION',
        declencheurs_amorces: decls,
        double_ouverture: p.double_ouverture || null,
        tags: tags,
        tuile_plateau: {
          nom_court: slot.nomBase || p.nom || sid,
          fenetre_badge: p.fenetre || (sp.famille === 'GARDIEN' ? 'ACTIVATION' : 'OUVERTURE'),
          icone_conseillee: p.cablage_recommande || null,
          pictogrammes: [],
          mots_cles_plateau: {
            face_1: 'Archive v6.2 (lecture seule)',
            face_2: sp.famille === 'GARDIEN' ? 'Face 2 archive v6.2' : null,
            enracine: enr ? 'Clause Enraciné dédiée' : null
          },
          resume_plateau: p.animal_ou_theme || ''
        },
        carte_joueur: {
          titre_complet: p.nom || slot.nomBase || sid,
          entite_illustree: p.animal_ou_theme || slot.nomBase || sid,
          brief_illustration: '',
          pitch_ambiance: '',
          texte_regle: {
            face_1: f1,
            face_2: f2,
            enracine: enr
          },
          decision_et_renoncement: {
            choix: dr.choix || '',
            renoncement: dr.renoncement || ''
          }
        },
        temoins: p.temoin ? [{ id: `${sid}_T1`, resume: p.temoin }] : [],
        heuristique_bot: p.heuristique_bot || '',
        _isArchiveV62: true
      };
    });
    return out;
  }

  // --------------------------------------------------------------------------
  // Gestion de l'Atelier Draft (Workspace + localStorage + Import/Export)
  // --------------------------------------------------------------------------
  function createEmptyWorkspace() {
    const slots = {};
    getSlotsSpec().forEach(sp => {
      slots[sp.id] = {
        slot_id: sp.id,
        alias_oriente: sp.alias_oriente,
        selected_source: null, // 'panel_1' | 'panel_2' | 'panel_3' | 'custom' | null
        base_source: 'panel_1',
        is_modified: false,
        status: '',
        rating: 0,
        favorite: false,
        comment: '',
        panel_notes: {
          panel_1: { rating: 0, comment: '' },
          panel_2: { rating: 0, comment: '' },
          panel_3: { rating: 0, comment: '' }
        },
        custom_tile: null,
        updated_at: null
      };
    });
    return {
      schema_version: '6.3.1-workspace',
      projet: 'Amazonia : Dernier Rempart — Atelier Draft v6.3.1',
      updated_at: null,
      slots
    };
  }

  function normalizeWorkspace(raw) {
    const base = createEmptyWorkspace();
    if (!raw || typeof raw !== 'object') return base;
    if (typeof raw.updated_at === 'string') base.updated_at = raw.updated_at;
    const rawSlots = raw.slots && typeof raw.slots === 'object' ? raw.slots : {};
    Object.keys(base.slots).forEach(sid => {
      const src = rawSlots[sid];
      if (!src || typeof src !== 'object') return;
      const dst = base.slots[sid];
      if (['panel_1', 'panel_2', 'panel_3', 'custom', null].includes(src.selected_source)) {
        dst.selected_source = src.selected_source;
      }
      if (['panel_1', 'panel_2', 'panel_3'].includes(src.base_source)) {
        dst.base_source = src.base_source;
      }
      dst.is_modified = Boolean(src.is_modified && src.custom_tile);
      dst.status = typeof src.status === 'string' ? src.status : '';
      dst.rating = Math.max(0, Math.min(5, Number(src.rating) || 0));
      dst.favorite = Boolean(src.favorite);
      dst.comment = typeof src.comment === 'string' ? src.comment : '';
      dst.updated_at = typeof src.updated_at === 'string' ? src.updated_at : null;
      if (src.custom_tile && typeof src.custom_tile === 'object') {
        dst.custom_tile = deepClone(src.custom_tile);
      }
      if (src.panel_notes && typeof src.panel_notes === 'object') {
        PANEL_IDS.forEach(pid => {
          if (src.panel_notes[pid] && typeof src.panel_notes[pid] === 'object') {
            dst.panel_notes[pid] = {
              rating: Math.max(0, Math.min(5, Number(src.panel_notes[pid].rating) || 0)),
              comment: typeof src.panel_notes[pid].comment === 'string' ? src.panel_notes[pid].comment : ''
            };
          }
        });
      }
    });
    return base;
  }

  function loadInitialWorkspace() {
    try {
      if (typeof localStorage !== 'undefined' && localStorage && typeof localStorage.getItem === 'function') {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) {
          return normalizeWorkspace(JSON.parse(stored));
        }
      }
    } catch (_err) {
      // ignore storage errors
    }
    const seed = getInitialWorkspaceSeed();
    if (seed && typeof seed === 'object') {
      return normalizeWorkspace(seed);
    }
    return createEmptyWorkspace();
  }

  function saveWorkspaceToStorage() {
    uiState.workspace.updated_at = new Date().toISOString();
    try {
      if (typeof localStorage !== 'undefined' && localStorage && typeof localStorage.setItem === 'function') {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(uiState.workspace));
      }
    } catch (_err) {
      // ignore storage errors
    }
  }

  // --------------------------------------------------------------------------
  // État réactif de l'Explorateur v6.3.1
  // --------------------------------------------------------------------------
  const uiState = {
    initialized: false,
    source: 'panel_1', // 'panel_1' | 'panel_2' | 'panel_3' | 'canon' | 'archive_v6_2'
    radarTarget: 'canon', // 'canon' | 'active_source'
    radarDetailKey: null, // 'elected' | 'twists' | 'lois' | 'eveil' | 'sommeil' | 'enrac' | 'a0' | 'synergies' | null
    view: 'explorer', // 'explorer' | 'simulator' | 'dashboard'
    explorerSubView: 'cards', // 'cards' | 'duel'
    selectedBorder: 'ALL', // 'ALL' | 'M-R' | ...
    duelSlotId: 'G1',
    filters: {
      search: '',
      peuple: 'ALL',
      family: 'ALL',
      role: 'ALL',
      draft: 'ALL',
      picto: null
    },
    resourceFocus: null, // state token or ICONE_*
    resourceFilterOnly: false,
    // Simulateur de table
    simPeuples: ['M', 'R', 'O', 'H'],
    simHighlightPeuple: null,
    // Tableau de bord
    dashFilter: 'ALL',
    // Modales / Tiroirs
    pictoGuideOpen: false,
    editor: null, // { slotId, baseSource, tile }
    exportModal: null, // { tab: 'gemini' | 'antigravity', geminiScope: 'to_arbitrate', fallbackPanel: 'panel_1' }
    // Workspace persistant
    workspace: null
  };

  function ensureInitialized() {
    ensureBorderMaps();
    if (!uiState.initialized) {
      uiState.workspace = loadInitialWorkspace();
      uiState.initialized = true;
      bindGlobalKeys();
    }
  }

  let _keysBound = false;
  function bindGlobalKeys() {
    if (_keysBound) return;
    if (typeof document === 'undefined' || typeof document.addEventListener !== 'function') return;
    _keysBound = true;
    document.addEventListener('keydown', function (ev) {
      if (!ev) return;
      const tag = ev.target && ev.target.tagName ? String(ev.target.tagName).toUpperCase() : '';
      const isTyping = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT';
      if (ev.key === 'Escape') {
        if (uiState.editor) {
          uiState.editor = null;
          render();
          return;
        }
        if (uiState.exportModal) {
          uiState.exportModal = null;
          render();
          return;
        }
        if (uiState.pictoGuideOpen) {
          uiState.pictoGuideOpen = false;
          render();
          return;
        }
        if (uiState.resourceFocus) {
          uiState.resourceFocus = null;
          uiState.resourceFilterOnly = false;
          render();
          return;
        }
        if (uiState.radarDetailKey) {
          uiState.radarDetailKey = null;
          render();
          return;
        }
      }
      if (isTyping) return;
      if (uiState.view === 'explorer' && uiState.explorerSubView === 'duel') {
        const specs = getSlotsSpec();
        const curIdx = specs.findIndex(s => s.id === uiState.duelSlotId);
        if (ev.key === 'ArrowRight' && curIdx >= 0) {
          uiState.duelSlotId = specs[(curIdx + 1) % specs.length].id;
          render();
        } else if (ev.key === 'ArrowLeft' && curIdx >= 0) {
          uiState.duelSlotId = specs[(curIdx - 1 + specs.length) % specs.length].id;
          render();
        }
      }
    });
  }

  // --------------------------------------------------------------------------
  // Résolution des Tuiles par Source (Panel 1/2/3, Mon Canon, Archive v6.2)
  // --------------------------------------------------------------------------
  function getPanelTile(panelId, slotId) {
    const panels = getPanelsData();
    const p = panels[panelId];
    return p && p.tuiles_ciblees ? p.tuiles_ciblees[slotId] || null : null;
  }

  function getCanonSlotResolved(slotId, fallbackPanelId) {
    ensureInitialized();
    const wsSlot = uiState.workspace.slots[slotId];
    if (wsSlot) {
      if (wsSlot.selected_source === 'custom' && wsSlot.custom_tile) {
        return {
          tile: wsSlot.custom_tile,
          sourceKey: 'custom',
          baseSource: wsSlot.base_source || 'panel_1',
          elected: true,
          modified: true
        };
      }
      if (wsSlot.selected_source && PANEL_IDS.includes(wsSlot.selected_source)) {
        const t = getPanelTile(wsSlot.selected_source, slotId);
        if (t) {
          return {
            tile: t,
            sourceKey: wsSlot.selected_source,
            baseSource: wsSlot.selected_source,
            elected: true,
            modified: false
          };
        }
      }
    }
    if (fallbackPanelId) {
      return {
        tile: getPanelTile(fallbackPanelId, slotId),
        sourceKey: fallbackPanelId,
        baseSource: fallbackPanelId,
        elected: false,
        modified: false
      };
    }
    return { tile: null, sourceKey: null, baseSource: null, elected: false, modified: false };
  }

  let _ARCHIVE_V62_CACHE = null;
  function getArchiveV62Map() {
    if (!_ARCHIVE_V62_CACHE) _ARCHIVE_V62_CACHE = buildArchiveV62Tiles();
    return _ARCHIVE_V62_CACHE;
  }

  function getActiveTilesMap(sourceOverride) {
    ensureInitialized();
    const src = sourceOverride || uiState.source;
    const out = {};
    if (src === 'archive_v6_2') {
      return getArchiveV62Map();
    }
    if (src === 'canon') {
      getSlotsSpec().forEach(sp => {
        const res = getCanonSlotResolved(sp.id, null);
        if (res.tile) out[sp.id] = res.tile;
      });
      return out;
    }
    const panels = getPanelsData();
    const p = panels[src];
    return (p && p.tuiles_ciblees) ? p.tuiles_ciblees : {};
  }

  function getEffectiveTileForSlot(slotId, sourceOverride) {
    const src = sourceOverride || uiState.source;
    if (src === 'canon') {
      return getCanonSlotResolved(slotId, null);
    }
    if (src === 'archive_v6_2') {
      return {
        tile: getArchiveV62Map()[slotId] || null,
        sourceKey: 'archive_v6_2',
        elected: false,
        modified: false
      };
    }
    const wsSlot = uiState.workspace.slots[slotId];
    const tile = getPanelTile(src, slotId);
    return {
      tile,
      sourceKey: src,
      elected: Boolean(wsSlot && wsSlot.selected_source === src),
      modified: false
    };
  }

  // --------------------------------------------------------------------------
  // Moteur Synergique (Producteurs <-> Consommateurs & Couverture /64 assises)
  // --------------------------------------------------------------------------
  function expandOutputStates(rawOutputs) {
    const set = new Set();
    (rawOutputs || []).forEach(raw => {
      const tok = String(raw || '').trim().toUpperCase();
      if (!tok) return;
      set.add(tok);
      const mapped = OUTPUT_FEEDS_STATES[tok];
      if (mapped) mapped.forEach(m => set.add(m));
      const meta = RESOURCE_META[tok];
      if (meta && meta.canon) set.add(meta.canon);
    });
    return set;
  }

  function normalizeStateList(arr) {
    return Array.from(new Set((arr || []).map(x => String(x || '').trim().toUpperCase()).filter(Boolean)));
  }

  function computeSynergyCoverage64(slotId, stateToken, tilesMap) {
    const tok = String(stateToken || '').toUpperCase();
    const assises = enumerateAll197Assises();
    let covered = 0;
    let total = 0;
    assises.forEach(a => {
      if (!a.tileIds.includes(slotId)) return;
      total++;
      const avail = new Set(SOCLE_STATES);
      a.peuples.forEach(p => {
        (PEUPLE_NATIVE_STATES[p] || []).forEach(st => avail.add(st));
      });
      a.tileIds.forEach(otherId => {
        const ot = tilesMap[otherId];
        if (!ot) return;
        expandOutputStates(ot.sorties).forEach(st => avail.add(st));
      });
      if (avail.has(tok) || (tok === 'ALTEREE' && avail.has('ALTERATION')) || (tok === 'ALTERATION' && avail.has('ALTEREE'))) {
        covered++;
      }
    });
    return { covered, total: total || 64 };
  }

  function computeTileLinks(slotId, tilesMap) {
    const tile = tilesMap[slotId];
    if (!tile) {
      return {
        upstreamTiles: [],
        downstreamTiles: [],
        nativeSources: [],
        synergyCoverage: {}
      };
    }
    const floorIn = normalizeStateList(tile.entrees_plancher);
    const synIn = normalizeStateList(tile.entrees_synergie);
    const allIn = Array.from(new Set(floorIn.concat(synIn)));
    const myOut = expandOutputStates(tile.sorties);
    const myIconsLit = new Set(normalizeStateList(tile.declencheurs_amorces));
    const myRecIcon = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee
      ? String(tile.tuile_plateau.icone_conseillee).toUpperCase()
      : null;

    const upstreamMap = new Map();
    const downstreamMap = new Map();

    Object.entries(tilesMap).forEach(([otherId, other]) => {
      if (otherId === slotId || !other) return;
      const otherOut = expandOutputStates(other.sorties);
      const otherFloor = normalizeStateList(other.entrees_plancher);
      const otherSyn = normalizeStateList(other.entrees_synergie);
      const otherAllIn = new Set(otherFloor.concat(otherSyn));
      const otherLit = new Set(normalizeStateList(other.declencheurs_amorces));
      const otherRecIcon = other.tuile_plateau && other.tuile_plateau.icone_conseillee
        ? String(other.tuile_plateau.icone_conseillee).toUpperCase()
        : null;

      // Qui m'alimente ?
      const upReasons = [];
      allIn.forEach(st => {
        if (otherOut.has(st)) upReasons.push(st);
      });
      if (myRecIcon && otherLit.has(myRecIcon)) {
        upReasons.push(myRecIcon);
      }
      if (upReasons.length > 0) {
        upstreamMap.set(otherId, {
          id: otherId,
          nom: (other.tuile_plateau && other.tuile_plateau.nom_court) || otherId,
          alias: other.alias_oriente,
          isTwin: TWIN_BY_SLOT[slotId] === otherId,
          reasons: Array.from(new Set(upReasons))
        });
      }

      // Qui j'alimente ?
      const downReasons = [];
      otherAllIn.forEach(st => {
        if (myOut.has(st)) downReasons.push(st);
      });
      if (otherRecIcon && myIconsLit.has(otherRecIcon)) {
        downReasons.push(otherRecIcon);
      }
      if (downReasons.length > 0) {
        downstreamMap.set(otherId, {
          id: otherId,
          nom: (other.tuile_plateau && other.tuile_plateau.nom_court) || otherId,
          alias: other.alias_oriente,
          isTwin: TWIN_BY_SLOT[slotId] === otherId,
          reasons: Array.from(new Set(downReasons))
        });
      }
    });

    // Sources natives (Socle ou Peuples de la lisière)
    const nativeSources = [];
    const seenNat = new Set();
    [tile.origine, tile.voisin].forEach(pCode => {
      const acc = ACCESSORIES_3_3[pCode];
      if (!acc) return;
      const matches = allIn.filter(st => acc.states.includes(st));
      if (matches.length > 0 && !seenNat.has(pCode)) {
        seenNat.add(pCode);
        nativeSources.push({ code: pCode, label: acc.title, icon: acc.icon });
      }
    });

    const synergyCoverage = {};
    synIn.forEach(st => {
      synergyCoverage[st] = computeSynergyCoverage64(slotId, st, tilesMap);
    });

    const sortLinks = list => list.sort((a, b) => (b.isTwin ? 1 : 0) - (a.isTwin ? 1 : 0) || a.id.localeCompare(b.id));
    return {
      upstreamTiles: sortLinks(Array.from(upstreamMap.values())),
      downstreamTiles: sortLinks(Array.from(downstreamMap.values())),
      nativeSources,
      synergyCoverage
    };
  }

  function computeResourceIndex(token, tilesMap) {
    const key = String(token || '').toUpperCase();
    const isIcon = key.startsWith('ICONE_');
    const meta = humanizeToken(key);
    const canon = meta.canon || key;
    const matchSet = new Set([key, canon]);
    if (key === 'ALTERATION' || key === 'ALTEREE') { matchSet.add('ALTERATION'); matchSet.add('ALTEREE'); }

    const nativeProducers = [];
    if (!isIcon && SOCLE_STATES.has(canon)) {
      nativeProducers.push({ code: 'SOCLE', label: 'Socle commun v6.2 (Forêt / Furtivité / Sac)', icon: '🌿' });
    }
    Object.values(ACCESSORIES_3_3).forEach(acc => {
      const hit = isIcon
        ? acc.icons.includes(key)
        : acc.states.some(s => matchSet.has(s));
      if (hit) {
        nativeProducers.push({ code: acc.code, label: `${PEUPLE_META[acc.code].nom} — ${acc.title}`, icon: acc.icon });
      }
    });

    const producers = [];
    const consumersFloor = [];
    const consumersSynergy = [];
    const consumersIcon = [];

    Object.entries(tilesMap).forEach(([sid, tile]) => {
      if (!tile) return;
      const nom = (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid;
      const item = { id: sid, nom, alias: tile.alias_oriente, origine: tile.origine, voisin: tile.voisin };

      if (isIcon) {
        const lit = normalizeStateList(tile.declencheurs_amorces);
        if (lit.includes(key)) producers.push(item);
        const rec = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee
          ? String(tile.tuile_plateau.icone_conseillee).toUpperCase()
          : '';
        if (rec === key) consumersIcon.push(item);
      } else {
        const outs = expandOutputStates(tile.sorties);
        if (Array.from(matchSet).some(m => outs.has(m))) producers.push(item);

        const fl = normalizeStateList(tile.entrees_plancher);
        if (Array.from(matchSet).some(m => fl.includes(m))) consumersFloor.push(item);

        const syn = normalizeStateList(tile.entrees_synergie);
        if (Array.from(matchSet).some(m => syn.includes(m))) {
          const cov = computeSynergyCoverage64(sid, syn.find(s => matchSet.has(s)) || key, tilesMap);
          consumersSynergy.push(Object.assign({}, item, { coverage: cov }));
        }
      }
    });

    const allInvolvedIds = new Set(
      producers.concat(consumersFloor, consumersSynergy, consumersIcon).map(x => x.id)
    );

    return {
      key,
      isIcon,
      meta,
      nativeProducers,
      producers,
      consumersFloor,
      consumersSynergy,
      consumersIcon,
      allInvolvedIds
    };
  }

  // --------------------------------------------------------------------------
  // Radar de Santé en Temps Réel (197 assises, 2K3 géométrique, Lois, Éveil, Sommeil, Enrac, A=0)
  // --------------------------------------------------------------------------
  function find2K3Triangles(twistTiles) {
    // Cherche 2 cycles dirigés de longueur 3 disjoints en sommets couvrant les 6 Peuples
    const edgeByDir = {};
    twistTiles.forEach(t => {
      const k = `${t.origine}>${t.voisin}`;
      edgeByDir[k] = t;
    });

    const triangles = [];
    for (let i = 0; i < PEUPLE_ORDER.length; i++) {
      const a = PEUPLE_ORDER[i];
      for (let j = 0; j < PEUPLE_ORDER.length; j++) {
        if (j === i) continue;
        const b = PEUPLE_ORDER[j];
        if (!edgeByDir[`${a}>${b}`]) continue;
        for (let k = 0; k < PEUPLE_ORDER.length; k++) {
          if (k === i || k === j) continue;
          const c = PEUPLE_ORDER[k];
          if (edgeByDir[`${b}>${c}`] && edgeByDir[`${c}>${a}`]) {
            const minIdx = Math.min(i, j, k);
            if (i === minIdx) {
              triangles.push({
                nodes: [a, b, c],
                arcs: [edgeByDir[`${a}>${b}`], edgeByDir[`${b}>${c}`], edgeByDir[`${c}>${a}`]]
              });
            }
          }
        }
      }
    }

    for (let x = 0; x < triangles.length; x++) {
      for (let y = x + 1; y < triangles.length; y++) {
        const union = new Set(triangles[x].nodes.concat(triangles[y].nodes));
        if (union.size === 6) {
          return [triangles[x], triangles[y]];
        }
      }
    }
    return null;
  }

  function computeHealthRadar(targetMode) {
    ensureInitialized();
    const mode = targetMode || uiState.radarTarget || 'canon';
    const isCanon = mode === 'canon';
    const tilesMap = isCanon ? getActiveTilesMap('canon') : getActiveTilesMap(uiState.source);
    const specs = getSlotsSpec();
    const assises = enumerateAll197Assises();

    const presentIds = specs.map(s => s.id).filter(id => Boolean(tilesMap[id]));
    const unelectedIds = specs.map(s => s.id).filter(id => !tilesMap[id]);
    const electedCount = presentIds.length;
    const isComplete = electedCount === 30;

    // 1. Twists 2K3
    const twistTiles = presentIds.map(id => tilesMap[id]).filter(t => Boolean(t.est_twist));
    const twistByOrig = Object.fromEntries(PEUPLE_ORDER.map(p => [p, []]));
    const twistByEdge = {};
    twistTiles.forEach(t => {
      if (twistByOrig[t.origine]) twistByOrig[t.origine].push(t.id);
      const bk = borderKey(t.origine, t.voisin);
      if (!twistByEdge[bk]) twistByEdge[bk] = [];
      twistByEdge[bk].push(t.id);
    });
    const missingOrigTwists = PEUPLE_ORDER.filter(p => twistByOrig[p].length === 0);
    const doubleTwistBorders = Object.entries(twistByEdge).filter(([, ids]) => ids.length > 1);
    const triangles2K3 = find2K3Triangles(twistTiles);
    let twistsStatus = 'ok';
    if (doubleTwistBorders.length > 0) {
      twistsStatus = 'err';
    } else if (twistTiles.length < 6 || missingOrigTwists.length > 0) {
      twistsStatus = isComplete ? 'err' : 'warn';
    } else if (!triangles2K3) {
      twistsStatus = 'warn';
    }

    // 2. Lois passives (<= 5 global et max <= 2 / assise sur 197 assises)
    const loiIds = presentIds.filter(id => String(tilesMap[id].nature || '').toUpperCase() === 'LOI_PASSIVE');
    const loiSet = new Set(loiIds);
    let maxLoisPerAssise = 0;
    const offendingLoiAssises = [];
    assises.forEach(a => {
      const cnt = a.tileIds.reduce((acc, tid) => acc + (loiSet.has(tid) ? 1 : 0), 0);
      if (cnt > maxLoisPerAssise) maxLoisPerAssise = cnt;
      if (cnt > 2) offendingLoiAssises.push({ key: a.key, count: cnt });
    });
    const loisStatus = (loiIds.length > 5 || maxLoisPerAssise > 2) ? 'err' : 'ok';

    // 3. Couverture Éveil (i) + (ii)
    const catalyseurIds = presentIds.filter(id => {
      const t = tilesMap[id];
      return t.famille === 'GARDIEN' && Array.isArray(t.roles_portes) && t.roles_portes.includes('CATALYSEUR_EVEIL');
    });
    const catSet = new Set(catalyseurIds);
    const eveilRegleI = {};
    const missingAnimalsI = [];
    ['M', 'R', 'O'].forEach(an => {
      const cnt = catalyseurIds.filter(id => tilesMap[id].origine === an && NON_ANIMAL_PEUPLES.has(tilesMap[id].voisin)).length;
      eveilRegleI[an] = cnt;
      if (cnt < 2) missingAnimalsI.push(`${an} (${cnt}/2)`);
    });
    const eveilRegleII = {};
    const missingBordersII = [];
    ANIMAL_ANIMAL_BORDERS.forEach(([a1, a2]) => {
      const pair = BORDER_TO_SLOTS[borderKey(a1, a2)] || [];
      const ok = pair.some(id => catSet.has(id));
      eveilRegleII[`${a1}–${a2}`] = ok;
      if (!ok) missingBordersII.push(`${a1}–${a2}`);
    });
    const uncoveredEveilAssises = [];
    assises.forEach(a => {
      if (a.peuples.some(p => ANIMAL_PEUPLES.has(p)) && !a.tileIds.some(id => catSet.has(id))) {
        uncoveredEveilAssises.push(a.key);
      }
    });
    let eveilStatus = 'ok';
    if (catalyseurIds.length < 9 || missingAnimalsI.length > 0 || missingBordersII.length > 0 || uncoveredEveilAssises.length > 0) {
      eveilStatus = isComplete ? 'err' : 'warn';
    }

    // 4. Couverture Sommeil (E sans H : >= 3/4 lisières E-{M,R,O,I} et 30/30 assises)
    const levierIds = presentIds.filter(id => Array.isArray(tilesMap[id].roles_portes) && tilesMap[id].roles_portes.includes('LEVIER_REVE'));
    const levSet = new Set(levierIds);
    const coveredEBorders = [];
    const missingEBorders = [];
    E_NON_H_BORDERS.forEach(([p1, p2]) => {
      const pair = BORDER_TO_SLOTS[borderKey(p1, p2)] || [];
      if (pair.some(id => levSet.has(id))) coveredEBorders.push(`${p1}–${p2}`);
      else missingEBorders.push(`${p1}–${p2}`);
    });
    const uncoveredESansH = [];
    assises.forEach(a => {
      if (a.peuples.includes('E') && !a.peuples.includes('H') && !a.tileIds.some(id => levSet.has(id))) {
        uncoveredESansH.push(a.key);
      }
    });
    let sommeilStatus = 'ok';
    if (coveredEBorders.length < 3 || uncoveredESansH.length > 0) {
      sommeilStatus = isComplete ? 'err' : 'warn';
    }

    // 5. Enracinements (3 à 5)
    const enracIds = presentIds.filter(id => Array.isArray(tilesMap[id].roles_portes) && tilesMap[id].roles_portes.includes('ENRACINEMENT'));
    let enracStatus = 'ok';
    if (enracIds.length > 5) enracStatus = 'err';
    else if (enracIds.length < 3) enracStatus = isComplete ? 'err' : 'warn';

    // 6. Autonomie A=0 ({R1, R2, R6, R10, M4, M5})
    const gardienLexRe = /\b(?:gardiens?|éveil|encoches?|résonance)\b/i;
    const a0Violations = [];
    Array.from(A0_SLOTS).sort().forEach(sid => {
      const t = tilesMap[sid];
      if (!t) return;
      const texts = [
        t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.face_1,
        t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.enracine,
        t.tuile_plateau && t.tuile_plateau.mots_cles_plateau && t.tuile_plateau.mots_cles_plateau.face_1
      ].filter(Boolean);
      const hitTxt = texts.some(txt => gardienLexRe.test(txt));
      const hitTok = normalizeStateList((t.entrees || []).concat(t.sorties || [])).some(tok => tok === 'GARDIEN' || tok === 'PARI_GLISSE');
      const hitRes = normalizeStateList(t.declencheurs_amorces).includes('ICONE_RESONANCE');
      if (hitTxt || hitTok || hitRes) a0Violations.push(sid);
    });
    const a0Present = Array.from(A0_SLOTS).filter(sid => Boolean(tilesMap[sid])).length;
    let a0Status = 'ok';
    if (a0Violations.length > 0) a0Status = 'err';
    else if (a0Present < 6) a0Status = 'warn';

    // 7. Synergies orphelines (0/64) & Divergence de lisière (I03)
    const orphanSynergies = [];
    presentIds.forEach(sid => {
      const t = tilesMap[sid];
      normalizeStateList(t.entrees_synergie).forEach(st => {
        const cov = computeSynergyCoverage64(sid, st, tilesMap);
        if (cov.covered === 0) orphanSynergies.push({ slotId: sid, state: st });
      });
    });
    const divergenceIssues = [];
    ALL_15_BORDERS.forEach(([p1, p2]) => {
      const pair = BORDER_TO_SLOTS[borderKey(p1, p2)] || [];
      const t1 = tilesMap[pair[0]];
      const t2 = tilesMap[pair[1]];
      if (!t1 || !t2) return;
      const o1 = (t1.sorties && t1.sorties[0]) ? String(t1.sorties[0]).toUpperCase() : '';
      const o2 = (t2.sorties && t2.sorties[0]) ? String(t2.sorties[0]).toUpperCase() : '';
      if (o1 && o2 && o1 === o2) {
        divergenceIssues.push(`${borderLabel(p1, p2)} : même sortie principale (${humanizeToken(o1).label})`);
      }
    });
    const synStatus = (orphanSynergies.length > 0 || divergenceIssues.length > 0) ? (isComplete ? 'err' : 'warn') : 'ok';

    return {
      scopeLabel: isCanon ? 'Mon Canon v6.3' : (PANEL_LABELS[uiState.source] || uiState.source),
      electedCount,
      unelectedIds,
      isComplete,
      twists: {
        status: twistsStatus,
        ids: twistTiles.map(t => t.id),
        count: twistTiles.length,
        missingOrigins: missingOrigTwists,
        doubleBorders: doubleTwistBorders,
        triangles2K3
      },
      lois: {
        status: loisStatus,
        ids: loiIds,
        count: loiIds.length,
        maxPerAssise: maxLoisPerAssise,
        offendingAssises: offendingLoiAssises
      },
      eveil: {
        status: eveilStatus,
        ids: catalyseurIds,
        count: catalyseurIds.length,
        regleI: eveilRegleI,
        missingAnimalsI,
        regleII: eveilRegleII,
        missingBordersII,
        uncoveredAssises: uncoveredEveilAssises
      },
      sommeil: {
        status: sommeilStatus,
        ids: levierIds,
        count: levierIds.length,
        coveredEBorders,
        missingEBorders,
        uncoveredAssises: uncoveredESansH
      },
      enrac: {
        status: enracStatus,
        ids: enracIds,
        count: enracIds.length
      },
      a0: {
        status: a0Status,
        presentCount: a0Present,
        violations: a0Violations
      },
      synergies: {
        status: synStatus,
        orphans: orphanSynergies,
        divergenceIssues
      }
    };
  }

  // --------------------------------------------------------------------------
  // Simulateur de Table 3 à 6 Peuples (Vue 2)
  // --------------------------------------------------------------------------
  function analyzeTableSimulation(peuples, sourceOverride) {
    ensureInitialized();
    const circle = Array.from(peuples || []);
    const n = circle.length;
    const src = sourceOverride || uiState.source;
    const canon = canonicalizeAssise(circle);
    const borders = [];
    const tileEntries = [];

    for (let i = 0; i < n; i++) {
      const p1 = circle[i];
      const p2 = circle[(i + 1) % n];
      const bk = borderKey(p1, p2);
      const pair = BORDER_TO_SLOTS[bk] || [];
      borders.push({ p1, p2, key: bk, label: borderLabel(p1, p2), slots: pair });
      pair.forEach(sid => {
        const res = getEffectiveTileForSlot(sid, src);
        tileEntries.push({
          slotId: sid,
          borderKey: bk,
          borderLabel: borderLabel(p1, p2),
          tile: res.tile,
          sourceKey: res.sourceKey,
          elected: res.elected,
          modified: res.modified
        });
      });
    }

    const activeTilesMap = {};
    tileEntries.forEach(e => {
      if (e.tile) activeTilesMap[e.slotId] = e.tile;
    });

    // États et icônes disponibles à cette table
    const tableProducersByState = {}; // state -> [{type:'native'|'tile', id, label}]
    const tableIconLighters = {}; // ICONE_* -> [{type:'native'|'tile', id, label}]

    function addProducer(map, key, entry) {
      if (!map[key]) map[key] = [];
      if (!map[key].some(x => x.id === entry.id)) map[key].push(entry);
    }

    SOCLE_STATES.forEach(st => {
      addProducer(tableProducersByState, st, { type: 'native', id: 'SOCLE', label: 'Socle commun' });
    });
    circle.forEach(p => {
      const acc = ACCESSORIES_3_3[p];
      if (!acc) return;
      (PEUPLE_NATIVE_STATES[p] || []).forEach(st => {
        addProducer(tableProducersByState, st, { type: 'native', id: `ACC_${p}`, label: `${PEUPLE_META[p].short} (${acc.title})` });
      });
      acc.icons.forEach(ic => {
        addProducer(tableIconLighters, ic, { type: 'native', id: `ACC_${p}`, label: `${PEUPLE_META[p].short} (${acc.title})` });
      });
    });

    Object.entries(activeTilesMap).forEach(([sid, tile]) => {
      const lbl = `${sid} · ${(tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid}`;
      expandOutputStates(tile.sorties).forEach(st => {
        addProducer(tableProducersByState, st, { type: 'tile', id: sid, label: lbl });
      });
      normalizeStateList(tile.declencheurs_amorces).forEach(ic => {
        addProducer(tableIconLighters, ic, { type: 'tile', id: sid, label: lbl });
      });
    });

    // Chaînes de moteurs complètes qui se bouclent à cette table + amplificateurs isolés
    const completeChains = [];
    const isolatedAmplifiers = [];

    Object.entries(activeTilesMap).forEach(([sid, tile]) => {
      const consumerLbl = `${sid} · ${(tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid}`;
      const synIn = normalizeStateList(tile.entrees_synergie);
      const floorIn = normalizeStateList(tile.entrees_plancher);
      const recIcon = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee
        ? String(tile.tuile_plateau.icone_conseillee).toUpperCase()
        : null;

      // Synergies amplificatrices
      synIn.forEach(st => {
        const prods = (tableProducersByState[st] || []).filter(p => p.id !== sid);
        const tileProds = prods.filter(p => p.type === 'tile');
        if (prods.length === 0) {
          isolatedAmplifiers.push({
            slotId: sid,
            tileName: (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid,
            state: st,
            stateMeta: humanizeToken(st)
          });
        } else {
          const shownProds = tileProds.length > 0 ? tileProds : prods.slice(0, 2);
          shownProds.slice(0, 3).forEach(pr => {
            completeChains.push({
              fromId: pr.id,
              fromLabel: pr.label,
              fromType: pr.type,
              via: st,
              viaMeta: humanizeToken(st),
              toId: sid,
              toLabel: consumerLbl,
              kind: 'synergy'
            });
          });
        }
      });

      // Plancher alimenté par une autre tuile de la table (pont inter-tuiles concret)
      floorIn.forEach(st => {
        const tileProds = (tableProducersByState[st] || []).filter(p => p.type === 'tile' && p.id !== sid);
        tileProds.slice(0, 2).forEach(pr => {
          completeChains.push({
            fromId: pr.id,
            fromLabel: pr.label,
            fromType: 'tile',
            via: st,
            viaMeta: humanizeToken(st),
            toId: sid,
            toLabel: consumerLbl,
            kind: 'floor_boost'
          });
        });
      });

      // Cascades vers icône Gardien conseillée
      if (recIcon) {
        const tileLighters = (tableIconLighters[recIcon] || []).filter(p => p.type === 'tile' && p.id !== sid);
        tileLighters.slice(0, 2).forEach(pr => {
          completeChains.push({
            fromId: pr.id,
            fromLabel: pr.label,
            fromType: 'tile',
            via: recIcon,
            viaMeta: humanizeToken(recIcon),
            toId: sid,
            toLabel: consumerLbl,
            kind: 'guardian_icon'
          });
        });
      }
    });

    // Dédupliquer les chaînes
    const seenChains = new Set();
    const uniqueChains = completeChains.filter(ch => {
      const k = `${ch.fromId}->${ch.via}->${ch.toId}`;
      if (seenChains.has(k)) return false;
      seenChains.add(k);
      return true;
    });

    const presentTiles = Object.values(activeTilesMap);
    const loisCount = presentTiles.filter(t => String(t.nature || '').toUpperCase() === 'LOI_PASSIVE').length;
    const twistsCount = presentTiles.filter(t => Boolean(t.est_twist)).length;
    const eveilCount = presentTiles.filter(t => t.famille === 'GARDIEN' && (t.roles_portes || []).includes('CATALYSEUR_EVEIL')).length;
    const sommeilCount = presentTiles.filter(t => (t.roles_portes || []).includes('LEVIER_REVE')).length;
    const enracCount = presentTiles.filter(t => (t.roles_portes || []).includes('ENRACINEMENT')).length;
    const missingCanonCount = tileEntries.filter(e => !e.tile).length;

    const hasAnimaux = circle.some(p => ANIMAL_PEUPLES.has(p));
    const hasReves = circle.some(p => ONIRIQUE_PEUPLES.has(p));
    const hasEssaim = circle.includes('I');
    const isESansH = circle.includes('E') && !circle.includes('H');

    return {
      peuples: circle,
      n,
      canonKey: canon.key,
      borders,
      tileEntries,
      modules: { gardiens: hasAnimaux, reves: hasReves, essaim: hasEssaim },
      accessories: circle.map(p => ACCESSORIES_3_3[p]).filter(Boolean),
      metrics: {
        loisCount,
        loisAlert: loisCount > 2,
        twistsCount,
        eveilCount,
        eveilAlert: hasAnimaux && missingCanonCount === 0 && eveilCount === 0,
        sommeilCount,
        sommeilAlert: isESansH && missingCanonCount === 0 && sommeilCount === 0,
        enracCount,
        missingCanonCount
      },
      completeChains: uniqueChains,
      isolatedAmplifiers
    };
  }

  // --------------------------------------------------------------------------
  // Passerelles d'Export : Gemini Markdown ciblé & Antigravity JSON déterministe
  // --------------------------------------------------------------------------
  function countWords(text) {
    const clean = String(text || '').trim();
    if (!clean) return 0;
    return clean.split(/\s+/).filter(Boolean).length;
  }

  function buildGeminiMarkdownBrief(scope) {
    ensureInitialized();
    const specs = getSlotsSpec();
    const ws = uiState.workspace;
    const radar = computeHealthRadar('canon');
    const lines = [];
    let tileCount = 0;

    function formatTileBrief(sid, tile, srcLabel) {
      const wsSlot = ws.slots[sid];
      const tp = tile.tuile_plateau || {};
      const cj = tile.carte_joueur || {};
      const tr = cj.texte_regle || {};
      const dr = cj.decision_et_renoncement || {};
      const rolesHuman = [];
      if (tile.nature === 'LOI_PASSIVE') rolesHuman.push('Loi passive permanente');
      if (tile.est_twist) rolesHuman.push('Twist 2K3');
      if ((tile.roles_portes || []).includes('CATALYSEUR_EVEIL')) rolesHuman.push('Catalyseur d’Éveil');
      if ((tile.roles_portes || []).includes('LEVIER_REVE')) rolesHuman.push('Levier de Rêve');
      if ((tile.roles_portes || []).includes('ENRACINEMENT')) rolesHuman.push('Synergie d’Enracinement');

      const out = [];
      out.push(`### ${sid} (${tile.alias_oriente}) — ${cj.titre_complet || tp.nom_court || sid} [${srcLabel}]`);
      if (rolesHuman.length > 0) out.push(`- **Nature & rôles** : ${rolesHuman.join(' · ')}`);
      if (wsSlot && (wsSlot.status || wsSlot.rating || wsSlot.favorite)) {
        const meta = [];
        if (wsSlot.status) meta.push(`Statut : ${wsSlot.status}`);
        if (wsSlot.rating) meta.push(`Note : ${wsSlot.rating}/5`);
        if (wsSlot.favorite) meta.push('Coup de cœur');
        out.push(`- **Repère atelier** : ${meta.join(' · ')}`);
      }
      if (wsSlot && wsSlot.comment) out.push(`- **Note d’auteur** : ${wsSlot.comment}`);
      if (tr.face_1) out.push(`- **Face 1** : ${tr.face_1}`);
      if (tr.face_2) out.push(`- **Face 2** : ${tr.face_2}`);
      if (tr.enracine) out.push(`- **Enraciné** : ${tr.enracine}`);
      if (dr.choix || dr.renoncement) {
        out.push(`- **Dilemme** : Choix — ${dr.choix || '—'} | Renoncement — ${dr.renoncement || '—'}`);
      }
      return out.join('\n');
    }

    if (scope === 'to_arbitrate') {
      lines.push('# Brief Atelier Amazonia v6.3 — Emplacements en hésitation ou à hybrider');
      lines.push('');
      const targets = specs.filter(sp => {
        const st = ws.slots[sp.id] && ws.slots[sp.id].status;
        return st === 'HESITATION' || st === 'A_HYBRIDER';
      });
      if (targets.length === 0) {
        lines.push('_Aucun emplacement n’est actuellement marqué « Hésitation » ou « À hybrider »._');
      } else {
        targets.forEach(sp => {
          tileCount++;
          const wsSlot = ws.slots[sp.id];
          lines.push(`## ${sp.id} (${sp.alias_oriente}) — ${wsSlot.status === 'A_HYBRIDER' ? 'À hybrider' : 'Hésitation'}`);
          if (wsSlot.comment) lines.push(`> **Intention d’auteur** : ${wsSlot.comment}`);
          lines.push('');
          if (wsSlot.is_modified && wsSlot.custom_tile) {
            lines.push(formatTileBrief(sp.id, wsSlot.custom_tile, 'Version hybride/éditée'));
            lines.push('');
          }
          PANEL_IDS.forEach(pid => {
            const pt = getPanelTile(pid, sp.id);
            if (!pt) return;
            const tr = (pt.carte_joueur && pt.carte_joueur.texte_regle) || {};
            const mark = wsSlot.selected_source === pid ? ' ★ Élu' : '';
            lines.push(`- **${PANEL_LABELS[pid]}${mark} — ${(pt.carte_joueur && pt.carte_joueur.titre_complet) || pt.tuile_plateau.nom_court}** : ${tr.face_1 || ''}${tr.face_2 ? ' // Face 2 : ' + tr.face_2 : ''}${tr.enracine ? ' // Enraciné : ' + tr.enracine : ''}`);
          });
          lines.push('');
        });
      }
    } else if (scope === 'active_context') {
      if (uiState.view === 'simulator') {
        const sim = analyzeTableSimulation(uiState.simPeuples, uiState.source);
        lines.push(`# Brief Table simulée ${sim.canonKey} (${sim.peuples.join(' – ')}) — ${PANEL_LABELS[uiState.source] || uiState.source}`);
        lines.push('');
        lines.push(`- **Bilan local** : ${sim.metrics.loisCount} loi(s) passive(s), ${sim.metrics.twistsCount} twist(s), ${sim.metrics.eveilCount} catalyseur(s) d’Éveil, ${sim.metrics.sommeilCount} levier(s) de Rêve, ${sim.metrics.enracCount} Enracinement(s).`);
        if (sim.isolatedAmplifiers.length > 0) {
          lines.push(`- **Amplificateurs sans producteur à cette table** : ${sim.isolatedAmplifiers.map(x => `${x.slotId} (${x.stateMeta.label})`).join(', ')}.`);
        }
        lines.push('');
        sim.tileEntries.forEach(entry => {
          if (!entry.tile) return;
          tileCount++;
          lines.push(formatTileBrief(entry.slotId, entry.tile, PANEL_LABELS[entry.sourceKey] || 'Mon Canon'));
          lines.push('');
        });
      } else {
        const visibleIds = getFilteredSlotIds();
        lines.push(`# Brief Explorateur Amazonia v6.3 — ${PANEL_LABELS[uiState.source] || uiState.source} (${visibleIds.length} tuile(s))`);
        lines.push('');
        visibleIds.forEach(sid => {
          const res = getEffectiveTileForSlot(sid, uiState.source);
          if (!res.tile) return;
          tileCount++;
          lines.push(formatTileBrief(sid, res.tile, res.modified ? 'Modifié par l’auteur' : (PANEL_LABELS[res.sourceKey] || uiState.source)));
          lines.push('');
        });
      }
    } else if (scope === 'notes_and_edits') {
      lines.push('# Brief Atelier Amazonia v6.3 — Notes d’auteur & Tuiles modifiées');
      lines.push('');
      const touched = specs.filter(sp => {
        const w = ws.slots[sp.id];
        return w && (w.is_modified || (w.comment && w.comment.trim()) || w.status || w.favorite);
      });
      if (touched.length === 0) {
        lines.push('_Aucune note ni modification enregistrée pour le moment._');
      } else {
        touched.forEach(sp => {
          const w = ws.slots[sp.id];
          const res = getCanonSlotResolved(sp.id, w.base_source || 'panel_1');
          if (!res.tile) return;
          tileCount++;
          const label = w.is_modified ? 'Modifié / Hybride' : (w.selected_source ? PANEL_LABELS[w.selected_source] : 'Non élu');
          lines.push(formatTileBrief(sp.id, res.tile, label));
          lines.push('');
        });
      }
    } else {
      // canon_summary
      lines.push(`# Synthèse Mon Canon v6.3 (${radar.electedCount}/30 emplacements élus)`);
      lines.push('');
      lines.push(`- **Twists 2K3** : ${radar.twists.count} (${radar.twists.triangles2K3 ? '2 triangles valides' : 'géométrie en cours'})`);
      lines.push(`- **Lois passives** : ${radar.lois.count}/5 (max ${radar.lois.maxPerAssise}/assise sur 197 assises)`);
      lines.push(`- **Couverture Éveil** : ${radar.eveil.count} catalyseurs`);
      lines.push(`- **Sommeil E sans H** : ${radar.sommeil.coveredEBorders.length}/4 lisières de E couvertes`);
      lines.push(`- **Enracinements** : ${radar.enrac.count} (cible 3–5)`);
      lines.push('');
      lines.push('| Slot | Lisière | Source | Titre | Rôles | Statut | Note | Commentaire |');
      lines.push('| --- | --- | --- | --- | --- | --- | --- | --- |');
      specs.forEach(sp => {
        const w = ws.slots[sp.id];
        const res = getCanonSlotResolved(sp.id, null);
        if (res.tile) tileCount++;
        const srcTxt = w.selected_source ? (PANEL_SHORT[w.selected_source] || w.selected_source) : 'À trancher';
        const title = res.tile ? ((res.tile.carte_joueur && res.tile.carte_joueur.titre_complet) || res.tile.tuile_plateau.nom_court) : '—';
        const tags = [];
        if (res.tile) {
          if (res.tile.est_twist) tags.push('⚡Twist');
          if (res.tile.nature === 'LOI_PASSIVE') tags.push('⚖️Loi');
          if ((res.tile.roles_portes || []).includes('CATALYSEUR_EVEIL')) tags.push('☀️Éveil');
          if ((res.tile.roles_portes || []).includes('LEVIER_REVE')) tags.push('🌙Rêve');
          if ((res.tile.roles_portes || []).includes('ENRACINEMENT')) tags.push('🌱Enrac');
        }
        const safeCom = (w.comment || '').replace(/\|/g, '/').replace(/\n/g, ' ');
        lines.push(`| ${sp.id} | ${sp.alias_oriente} | ${srcTxt} | ${title} | ${tags.join(' ')} | ${w.status || '—'} | ${w.rating ? w.rating + '★' : '—'}${w.favorite ? ' ♥' : ''} | ${safeCom || '—'} |`);
      });
    }

    const markdown = lines.join('\n').trim() + '\n';
    const words = countWords(markdown);
    const chars = markdown.length;
    const comfort = words <= 2500 ? 'green' : (words <= 6000 ? 'amber' : 'red');
    return { markdown, words, chars, tileCount, comfort };
  }

  function buildAuthorWorkspaceExport() {
    ensureInitialized();
    const radar = computeHealthRadar('canon');
    const orderedSlots = {};
    getSlotsSpec().forEach(sp => {
      const w = uiState.workspace.slots[sp.id];
      orderedSlots[sp.id] = {
        slot_id: sp.id,
        alias_oriente: sp.alias_oriente,
        selected_source: w.selected_source,
        base_source: w.base_source,
        is_modified: Boolean(w.is_modified && w.custom_tile),
        status: w.status || '',
        rating: Number(w.rating) || 0,
        favorite: Boolean(w.favorite),
        comment: w.comment || '',
        panel_notes: {
          panel_1: deepClone(w.panel_notes.panel_1 || { rating: 0, comment: '' }),
          panel_2: deepClone(w.panel_notes.panel_2 || { rating: 0, comment: '' }),
          panel_3: deepClone(w.panel_notes.panel_3 || { rating: 0, comment: '' })
        },
        custom_tile: (w.is_modified && w.custom_tile) ? deepClone(w.custom_tile) : null,
        updated_at: w.updated_at || null
      };
    });

    return {
      schema_version: '6.3.1-workspace',
      projet: 'Amazonia : Dernier Rempart — Atelier Draft v6.3.1',
      updated_at: uiState.workspace.updated_at || new Date().toISOString(),
      radar_summary: {
        elected_count: radar.electedCount,
        twists_count: radar.twists.count,
        twists_2k3_valid: Boolean(radar.twists.triangles2K3),
        lois_passives_count: radar.lois.count,
        lois_max_per_assise: radar.lois.maxPerAssise,
        catalyseurs_eveil_count: radar.eveil.count,
        sommeil_e_borders_covered: radar.sommeil.coveredEBorders.length,
        enracinements_count: radar.enrac.count,
        a0_violations: radar.a0.violations.slice()
      },
      slots: orderedSlots
    };
  }

  function sanitizeTileForCanonExport(rawTile, spec) {
    const t = deepClone(rawTile);
    const casting = getCastingRef();
    t.id = spec.id;
    t.alias_oriente = spec.alias_oriente;
    t.famille = spec.famille;
    t.origine = spec.origine;
    t.voisin = spec.voisin;
    t.couple = [spec.origine, spec.voisin];
    t.cycle = spec.famille === 'GARDIEN'
      ? 'DOUBLE_FACE_UPGRADE'
      : (t.nature === 'LOI_PASSIVE' ? 'PASSIF_CONTINU' : 'SIMPLE_CONTINU');
    t.cablage = spec.famille === 'GARDIEN' ? [1, 2, 3, 4, 5, 6] : null;
    t.nature = t.nature === 'LOI_PASSIVE' ? 'LOI_PASSIVE' : 'ACTION';
    t.est_twist = Boolean(t.est_twist);

    const rolesSet = new Set(Array.isArray(t.roles_portes) ? t.roles_portes : []);
    if (A0_SLOTS.has(spec.id)) rolesSet.add('AUTONOMIE_A0');
    if (t.nature === 'LOI_PASSIVE') rolesSet.add('LOI_PASSIVE');
    else rolesSet.delete('LOI_PASSIVE');
    if (t.est_twist) rolesSet.add('TWIST_2K3');
    else rolesSet.delete('TWIST_2K3');
    if (t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.enracine && String(t.carte_joueur.texte_regle.enracine).trim()) {
      rolesSet.add('ENRACINEMENT');
    }
    t.roles_portes = Array.from(rolesSet);

    const floorList = normalizeStateList(t.entrees_plancher);
    const floorSet = new Set(floorList);
    const synList = normalizeStateList(t.entrees_synergie).filter(x => !floorSet.has(x));
    t.entrees_plancher = floorList;
    t.entrees_synergie = synList;
    t.entrees = Array.from(new Set(floorList.concat(synList)));
    t.sorties = normalizeStateList(t.sorties);
    t.declencheurs_amorces = normalizeStateList(t.declencheurs_amorces).filter(ic => Boolean(GUARDIAN_ICON_BY_ID[ic]));
    if (!Array.isArray(t.paiement)) t.paiement = [];
    if (!Array.isArray(t.tags)) t.tags = [];

    if (!t.tuile_plateau) t.tuile_plateau = {};
    if (spec.famille === 'GARDIEN' && casting[spec.id]) {
      t.tuile_plateau.nom_court = casting[spec.id].nom_animal;
    }
    if (spec.famille !== 'GARDIEN') {
      t.tuile_plateau.icone_conseillee = null;
      if (t.carte_joueur && t.carte_joueur.texte_regle) {
        t.carte_joueur.texte_regle.face_2 = null;
      }
      if (t.tuile_plateau.mots_cles_plateau) {
        t.tuile_plateau.mots_cles_plateau.face_2 = null;
      }
      t.double_ouverture = null;
    }

    // Supprimer toute propriété privée / vestige C02
    delete t.mots_par_face;
    delete t._isArchiveV62;
    if (t.carte_joueur) delete t.carte_joueur.mots_par_face;
    return t;
  }

  function buildCandidateCanonV63(fallbackPanelId) {
    ensureInitialized();
    const specs = getSlotsSpec();
    const fallback = PANEL_IDS.includes(fallbackPanelId) ? fallbackPanelId : 'panel_1';
    const tuilesOut = {};
    const provenance = {};

    specs.forEach(sp => {
      const res = getCanonSlotResolved(sp.id, fallback);
      const tile = sanitizeTileForCanonExport(res.tile, sp);
      tuilesOut[sp.id] = tile;
      provenance[sp.id] = res.elected ? res.sourceKey : `${fallback}_fallback`;
    });

    const rolesSummary = {
      catalyseurs_eveil: [],
      leviers_reve: [],
      synergies_enracinement: [],
      lois_passives: [],
      autonomie_A0: [],
      twists_2K3: []
    };
    specs.forEach(sp => {
      const t = tuilesOut[sp.id];
      const tag = `${sp.id}=${sp.alias_oriente}`;
      if (t.roles_portes.includes('CATALYSEUR_EVEIL')) rolesSummary.catalyseurs_eveil.push(tag);
      if (t.roles_portes.includes('LEVIER_REVE')) rolesSummary.leviers_reve.push(tag);
      if (t.roles_portes.includes('ENRACINEMENT')) rolesSummary.synergies_enracinement.push(tag);
      if (t.nature === 'LOI_PASSIVE') rolesSummary.lois_passives.push(tag);
      if (t.roles_portes.includes('AUTONOMIE_A0')) rolesSummary.autonomie_A0.push(tag);
      if (t.est_twist) rolesSummary.twists_2K3.push(tag);
    });

    const twistTiles = specs.map(sp => tuilesOut[sp.id]).filter(t => t.est_twist);
    const tris = find2K3Triangles(twistTiles);
    const carteDesRoles = {
      statut: 'CANDIDAT_ATELIER_V6_3_1',
      roles: rolesSummary
    };
    if (tris) {
      carteDesRoles.partition_2K3 = {
        triangle_1: tris[0].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → '),
        triangle_2: tris[1].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → ')
      };
    }

    const today = new Date().toISOString().slice(0, 10);
    return {
      _meta: {
        projet: 'Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)',
        schema_version: '6.3.1',
        socle_verrouille: '6.2.0',
        cadrage_source: 'docs/cadrage_tuiles_v6_3.md',
        etape_active: 'ETAPE_3_SELECTION_ET_AFFINAGE',
        statut_global: 'CANDIDAT_AUTEUR_V6_3',
        genere_le: today,
        slots_count: 30,
        c02_supprime: true,
        panel_id: 'canon_v6_3_candidat',
        murs_porteurs_verrouilles: [
          'M1_TEMPS_BATAILLE',
          'M2_CONSERVATION_THERMIQUE',
          'M3_INTEGRITE_PLATEAU_ET_ICONES',
          'M4_AUTONOMIE_PLANCHER_SOLO'
        ],
        provenance_par_emplacement: provenance
      },
      referentiel_pictogrammes: deepClone(getPictosRef()),
      casting_gardiens_verrouille: deepClone(getCastingRef()),
      carte_des_roles: carteDesRoles,
      rapport_audit_197: {
        verdict_global: 'A_VALIDER_PAR_AUDIT_197',
        c02_word_count_purged: true,
        assises_verifiees: 197
      },
      tuiles_ciblees: tuilesOut
    };
  }

  // --------------------------------------------------------------------------
  // Filtrage des emplacements (Vue 1)
  // --------------------------------------------------------------------------
  function getFilteredSlotIds() {
    ensureInitialized();
    const specs = getSlotsSpec();
    const tilesMap = getActiveTilesMap(uiState.source);
    const f = uiState.filters;
    const search = String(f.search || '').toLowerCase().trim();
    const rfIndex = (uiState.resourceFocus && uiState.resourceFilterOnly)
      ? computeResourceIndex(uiState.resourceFocus, tilesMap)
      : null;

    return specs.filter(sp => {
      const sid = sp.id;
      const wsSlot = uiState.workspace.slots[sid];
      const tile = tilesMap[sid];

      if (uiState.selectedBorder !== 'ALL' && borderKey(sp.origine, sp.voisin) !== uiState.selectedBorder) {
        return false;
      }
      if (f.peuple !== 'ALL' && sp.origine !== f.peuple && sp.voisin !== f.peuple) return false;
      if (f.family !== 'ALL' && sp.famille !== f.family) return false;

      if (rfIndex && !rfIndex.allInvolvedIds.has(sid)) return false;

      if (f.draft !== 'ALL' && wsSlot) {
        if (f.draft === 'ELECTED' && !wsSlot.selected_source) return false;
        if (f.draft === 'UNELECTED' && wsSlot.selected_source) return false;
        if (f.draft === 'MODIFIED' && !wsSlot.is_modified) return false;
        if (f.draft === 'COMMENTED' && !(wsSlot.comment && wsSlot.comment.trim())) return false;
        if (f.draft === 'FAVORITE' && !wsSlot.favorite) return false;
        if (['RETENUE', 'A_HYBRIDER', 'HESITATION', 'ALTERNATIVE', 'ECARTEE'].includes(f.draft) && wsSlot.status !== f.draft) {
          return false;
        }
      }

      if (f.role !== 'ALL') {
        if (!tile) return false;
        if (f.role === 'TWIST_2K3' && !tile.est_twist) return false;
        else if (f.role === 'LOI_PASSIVE' && tile.nature !== 'LOI_PASSIVE') return false;
        else if (f.role !== 'TWIST_2K3' && f.role !== 'LOI_PASSIVE') {
          if (!Array.isArray(tile.roles_portes) || !tile.roles_portes.includes(f.role)) return false;
        }
      }

      if (f.picto) {
        if (!tile || !tile.tuile_plateau || !Array.isArray(tile.tuile_plateau.pictogrammes)) return false;
        if (!tile.tuile_plateau.pictogrammes.includes(f.picto)) return false;
      }

      if (search) {
        const hayParts = [sid, sp.alias_oriente, sp.famille];
        if (tile) {
          const tp = tile.tuile_plateau || {};
          const cj = tile.carte_joueur || {};
          const tr = cj.texte_regle || {};
          const dr = cj.decision_et_renoncement || {};
          hayParts.push(
            tp.nom_court, tp.resume_plateau,
            tp.mots_cles_plateau && tp.mots_cles_plateau.face_1,
            tp.mots_cles_plateau && tp.mots_cles_plateau.face_2,
            cj.titre_complet, cj.entite_illustree, cj.pitch_ambiance,
            tr.face_1, tr.face_2, tr.enracine,
            dr.choix, dr.renoncement
          );
          (tile.entrees_plancher || []).concat(tile.entrees_synergie || [], tile.sorties || []).forEach(st => {
            hayParts.push(humanizeToken(st).label);
          });
        }
        if (wsSlot && wsSlot.comment) hayParts.push(wsSlot.comment);
        if (!hayParts.filter(Boolean).join(' ').toLowerCase().includes(search)) return false;
      }

      return true;
    }).map(sp => sp.id);
  }

  // --------------------------------------------------------------------------
  // Rendus UI — Pilier A (Mini-Tuile + Grande Carte + 15s), B (Flux), C, D
  // --------------------------------------------------------------------------
  function renderPeuplePill(code, withName) {
    const meta = PEUPLE_META[code] || { code, short: code };
    return (
      `<span class="x3-peuple-badge x3-peuple-${esc(code)}">` +
      `${getPeupleIconHtml(code, 13)}` +
      `<span>${esc(withName ? meta.short : code)}</span>` +
      `</span>`
    );
  }

  function renderOrientedEdgeBadge(orig, vois) {
    return (
      `<span class="x3-edge-badge" title="${esc(PEUPLE_META[orig].nom)} vers ${esc(PEUPLE_META[vois].nom)}">` +
      `${renderPeuplePill(orig, false)}` +
      `<span class="x3-edge-arrow">›</span>` +
      `${renderPeuplePill(vois, false)}` +
      `</span>`
    );
  }

  function renderPictoToken(picCode) {
    const ref = getPictosRef();
    const entry = ref[picCode];
    if (!entry) return '';
    return (
      `<span class="x3-picto-token" data-picto-symbol="true" title="${esc(entry.libelle)}" aria-label="${esc(entry.libelle)}">` +
      `${esc(entry.symbole)}` +
      `</span>`
    );
  }

  function renderMiniTuile(tile, compact) {
    const tp = tile.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const recIcon = tp.icone_conseillee ? GUARDIAN_ICON_BY_ID[String(tp.icone_conseillee).toUpperCase()] : null;
    const windowHtml = recIcon
      ? `<span class="x3-mini-window" title="Icône Gardien conseillée : ${esc(recIcon.desc)}">${recIcon.icon} ${esc(recIcon.label)}</span>`
      : `<span class="x3-mini-window">⏱ ${esc(formatFenetreLabel(tp.fenetre_badge))}</span>`;

    const pictos = Array.isArray(tp.pictogrammes) ? tp.pictogrammes : [];
    const pictosHtml = pictos.length > 0
      ? `<div class="x3-mini-pictos" aria-label="Pictogrammes plateau">${pictos.map(renderPictoToken).join('')}</div>`
      : '';

    const kwLines = [];
    if (mcp.face_1) {
      kwLines.push(
        `<div class="x3-mini-kw-line"><span class="x3-mini-kw-tag">${tile.nature === 'LOI_PASSIVE' ? 'Loi' : 'Face 1'}</span>${esc(mcp.face_1)}</div>`
      );
    }
    if (mcp.face_2) {
      kwLines.push(
        `<div class="x3-mini-kw-line is-f2"><span class="x3-mini-kw-tag">Face 2</span>${esc(mcp.face_2)}</div>`
      );
    }
    if (mcp.enracine) {
      kwLines.push(
        `<div class="x3-mini-kw-line is-enrac"><span class="x3-mini-kw-tag">🌱 Enraciné</span>${esc(mcp.enracine)}</div>`
      );
    }

    const medallion = getTileMedallionHtml(tile.id, tile.famille);

    return (
      `<div class="x3-mini-tuile-wrap">` +
      `<div class="x3-component-kicker"><span>Mini-Tuile Plateau · 360°</span><span>${tile.famille === 'GARDIEN' ? '2 encoches pari' : (tile.famille === 'REVE' ? 'Réglette 1–6' : 'Parcelle Forêt')}</span></div>` +
      `<div class="x3-mini-tuile fam-${esc(tile.famille)}" data-component="mini-tuile" data-slot-id="${esc(tile.id)}">` +
      `<div class="x3-mini-top">` +
      `<span class="x3-mini-id">${esc(tile.id)}</span>` +
      `${renderOrientedEdgeBadge(tile.origine, tile.voisin)}` +
      `</div>` +
      `<div class="x3-mini-identity">` +
      `${medallion}` +
      `<div class="x3-mini-name">${esc(tp.nom_court || tile.id)}</div>` +
      `</div>` +
      `${windowHtml}` +
      `${pictosHtml}` +
      (kwLines.length > 0 ? `<div class="x3-mini-keywords">${kwLines.join('')}</div>` : '') +
      (tp.resume_plateau ? `<div class="x3-mini-resume">${esc(tp.resume_plateau)}</div>` : '') +
      `</div>` +
      (!compact
        ? `<button type="button" class="x3-picto-guide-link" onclick="AmazoniaExplorerV63.openPictoGuide()">📖 Guide des 32 pictogrammes</button>`
        : '') +
      `</div>`
    );
  }

  function renderGrandeCarte(tile) {
    const cj = tile.carte_joueur || {};
    const tr = cj.texte_regle || {};
    const isLoi = tile.nature === 'LOI_PASSIVE';
    const isGardien = tile.famille === 'GARDIEN';

    const enracHtml = tr.enracine
      ? `<div class="x3-rule-block is-enracine" data-enracine-clause="true"><div class="x3-rule-label">🌱 Clause Enraciné dédiée</div><div>${esc(tr.enracine)}</div></div>`
      : `<div class="x3-enrac-standard-note">🌱 <strong>Enracinement standard :</strong> au décompte final, retourne ${isGardien ? '1 Souche (Face 1) ou 2 Souches (Face 2)' : '1 Souche'} en Arbre debout${tile.famille === 'REVE' ? ' · un Rêve enraciné rend le Sommeil impossible' : ''}.</div>`;

    return (
      `<div class="x3-grande-carte" data-component="grande-carte" data-slot-id="${esc(tile.id)}">` +
      `<div class="x3-gc-immersive">` +
      `<div class="x3-component-kicker"><span>Grande Carte Joueur</span><span>Gouvernance : ${esc(PEUPLE_META[tile.origine].nom)}</span></div>` +
      `<h3 class="x3-gc-title">${esc(cj.titre_complet || (tile.tuile_plateau && tile.tuile_plateau.nom_court) || tile.id)}</h3>` +
      (cj.entite_illustree ? `<div class="x3-gc-entity">${esc(cj.entite_illustree)}</div>` : '') +
      (cj.pitch_ambiance ? `<blockquote class="x3-gc-pitch">${esc(cj.pitch_ambiance)}</blockquote>` : '') +
      (cj.brief_illustration
        ? `<details class="x3-gc-brief"><summary>🎨 Brief d’illustration</summary><p>${esc(cj.brief_illustration)}</p></details>`
        : '') +
      `</div>` +
      `<div class="x3-gc-rules">` +
      `<div class="x3-rule-block ${isLoi ? 'is-loi-rule' : ''}">` +
      `<div class="x3-rule-label">${isLoi ? '⚖️ Loi passive permanente' : (isGardien ? 'Face 1' : 'Effet de la tuile')}</div>` +
      `<div>${esc(tr.face_1 || '—')}</div>` +
      `</div>` +
      (tr.face_2
        ? `<div class="x3-rule-block is-face2"><div class="x3-rule-label">✨ Face 2 — Éveillée (autonome)</div><div>${esc(tr.face_2)}</div></div>`
        : '') +
      `${enracHtml}` +
      `</div>` +
      `</div>`
    );
  }

  function renderSilhouetteStrip(tile, sourceInfo) {
    const isLoi = tile.nature === 'LOI_PASSIVE';
    const isTwist = Boolean(tile.est_twist);
    const roles = Array.isArray(tile.roles_portes) ? tile.roles_portes : [];
    const pills = [];

    if (isLoi) {
      pills.push('<span class="x3-nature-pill x3-nature-loi" title="Modifie le cœur du jeu en continu tant que la tuile est active">⚖️ Loi passive permanente</span>');
    } else {
      pills.push('<span class="x3-nature-pill x3-nature-action">✦ Action</span>');
    }
    if (isTwist) {
      pills.push('<span class="x3-nature-pill x3-nature-twist" title="Tord une règle familière du socle dans la géométrie 2K3">⚡ Twist 2K3</span>');
    }
    if (roles.includes('CATALYSEUR_EVEIL')) {
      pills.push('<span class="x3-role-pill x3-role-eveil">☀️ Catalyseur d’Éveil</span>');
    }
    if (roles.includes('LEVIER_REVE')) {
      pills.push('<span class="x3-role-pill x3-role-reve">🌙 Levier de Rêve</span>');
    }
    if (roles.includes('ENRACINEMENT')) {
      pills.push('<span class="x3-role-pill x3-role-enrac">🌱 Synergie d’Enracinement</span>');
    }
    if (roles.includes('AUTONOMIE_A0')) {
      pills.push('<span class="x3-role-pill x3-role-a0" title="Fonctionne 100 % sans Piste des Gardiens sur la table {H, E, I}">🔓 Autonomie A=0</span>');
    }
    if (sourceInfo && sourceInfo.modified) {
      pills.push('<span class="x3-modified-badge">✏️ Modifié par l’auteur</span>');
    }

    const srcBadge = sourceInfo && sourceInfo.sourceKey
      ? `<span class="x3-source-tag">${esc(sourceInfo.sourceKey === 'custom' ? 'Hybride / Édité' : (PANEL_LABELS[sourceInfo.sourceKey] || sourceInfo.sourceKey))}</span>`
      : '';

    return (
      `<div class="x3-silhouette-strip">` +
      `<div class="x3-silhouette-left">${pills.join('')}</div>` +
      `<div class="flex items-center gap-2">${srcBadge}</div>` +
      `</div>`
    );
  }

  function renderDepthSection(tile) {
    const cj = tile.carte_joueur || {};
    const dr = cj.decision_et_renoncement || {};
    const temoins = Array.isArray(tile.temoins) ? tile.temoins : [];
    const hasDilemma = Boolean(dr.choix || dr.renoncement);
    const hasDouble = Boolean(tile.famille === 'GARDIEN' && tile.double_ouverture);

    if (!hasDilemma && !hasDouble && temoins.length === 0) return '';

    const scenesHtml = temoins.length > 0
      ? `<div class="x3-section-label">🎬 Scènes témoins</div>` +
        `<div class="x3-scenes-list">` +
        temoins.map((tm, idx) => (
          `<div class="x3-scene-card">` +
          `<div class="x3-scene-head">Scène ${idx + 1}</div>` +
          `<div>${esc(tm.resume || '')}</div>` +
          `</div>`
        )).join('') +
        `</div>`
      : '';

    return (
      `<div class="x3-depth-zone">` +
      `<div class="x3-dilemma-box">` +
      `<div class="x3-section-label">🧭 Intention &amp; Dilemme</div>` +
      (hasDilemma
        ? `<div class="x3-dilemma-cols">` +
          `<div class="x3-dilemma-col is-choice"><div class="x3-dilemma-col-head">🎯 Pourquoi la jouer</div><div>${esc(dr.choix || '—')}</div></div>` +
          `<div class="x3-dilemma-col is-cost"><div class="x3-dilemma-col-head">⚖️ Ce qu’elle coûte vraiment</div><div>${esc(dr.renoncement || '—')}</div></div>` +
          `</div>`
        : '') +
      (hasDouble
        ? `<div class="x3-double-open"><strong>⚡ Montée en puissance / Double activation :</strong> ${esc(tile.double_ouverture)}</div>`
        : '') +
      `${scenesHtml}` +
      `</div>` +
      `</div>`
    );
  }

  function renderResourceChipBtn(tok, extraClass, coverage) {
    const m = humanizeToken(tok);
    const activeCls = uiState.resourceFocus === tok ? ' is-active' : '';
    const covHtml = coverage
      ? `<span class="x3-cov-tag ${coverage.covered === 0 ? 'is-zero' : ''}" title="Présent sur ${coverage.covered} des ${coverage.total} assises de cette tuile">${coverage.covered}/${coverage.total}</span>`
      : '';
    return (
      `<button type="button" class="x3-res-pill ${extraClass || ''}${activeCls}" ` +
      `data-resource-chip="${esc(tok)}" ` +
      `onclick="AmazoniaExplorerV63.focusResource('${esc(tok)}')" ` +
      `title="Cliquer pour voir Producteurs et Consommateurs de ${esc(m.label)}">` +
      `<span>${m.icon}</span><span>${esc(m.label)}</span>${covHtml}` +
      `</button>`
    );
  }

  function renderSynergyStrip(tile, tilesMap) {
    const links = computeTileLinks(tile.id, tilesMap);
    const floorIn = normalizeStateList(tile.entrees_plancher);
    const synIn = normalizeStateList(tile.entrees_synergie);
    const outs = normalizeStateList(tile.sorties);
    const litIcons = normalizeStateList(tile.declencheurs_amorces);
    const twinId = TWIN_BY_SLOT[tile.id];
    const twinTile = twinId ? tilesMap[twinId] : null;

    const floorHtml = floorIn.length > 0
      ? floorIn.map(st => renderResourceChipBtn(st, 'is-floor')).join('')
      : '<span class="text-xs text-slate-400">Autonome sans prérequis</span>';

    const synHtml = synIn.length > 0
      ? synIn.map(st => renderResourceChipBtn(st, 'is-synergy', links.synergyCoverage[st])).join('')
      : '<span class="text-xs text-slate-400">Aucun amplificateur conditionnel déclaré</span>';

    const outChips = outs.map(st => renderResourceChipBtn(st, 'is-output')).concat(
      litIcons.map(ic => renderResourceChipBtn(ic, 'is-icon'))
    );

    const upHtml = links.upstreamTiles.length > 0
      ? links.upstreamTiles.slice(0, 8).map(lk => (
          `<button type="button" class="x3-tile-link-chip is-upstream" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(lk.id)}')" title="Alimente via ${esc(lk.reasons.map(r => humanizeToken(r).label).join(', '))}">` +
          `${lk.isTwin ? '🔗 ' : ''}<strong>${esc(lk.id)}</strong> ${esc(lk.nom)}</button>`
        )).join('') + (links.upstreamTiles.length > 8 ? `<span class="text-[11px] text-slate-500">+${links.upstreamTiles.length - 8}</span>` : '')
      : '<span class="text-xs text-slate-400">Tourne déjà sur socle &amp; accessoires natifs</span>';

    const downHtml = links.downstreamTiles.length > 0
      ? links.downstreamTiles.slice(0, 8).map(lk => (
          `<button type="button" class="x3-tile-link-chip is-downstream" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(lk.id)}')" title="Alimenté via ${esc(lk.reasons.map(r => humanizeToken(r).label).join(', '))}">` +
          `${lk.isTwin ? '🔗 ' : ''}<strong>${esc(lk.id)}</strong> ${esc(lk.nom)}</button>`
        )).join('') + (links.downstreamTiles.length > 8 ? `<span class="text-[11px] text-slate-500">+${links.downstreamTiles.length - 8}</span>` : '')
      : '<span class="text-xs text-slate-400">Effet terminal direct sur le plateau</span>';

    const twinBar = twinId
      ? `<div class="x3-twin-bar">` +
        `<div>🔗 <strong>Jumelle de lisière (100 % co-présente) :</strong> ` +
        (twinTile
          ? `<strong>${esc(twinId)} · ${esc((twinTile.tuile_plateau && twinTile.tuile_plateau.nom_court) || twinId)}</strong> (${esc(twinTile.alias_oriente)}) — ${esc((twinTile.tuile_plateau && twinTile.tuile_plateau.resume_plateau) || (twinTile.carte_joueur && twinTile.carte_joueur.titre_complet) || '')}`
          : `<strong>${esc(twinId)}</strong> (non encore élue dans Mon Canon)`) +
        `</div>` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(twinId)}')">Voir ${esc(twinId)} →</button>` +
        `</div>`
      : '';

    return (
      `<div class="x3-synergy-strip" data-synergy-strip="${esc(tile.id)}">` +
      `<div class="x3-section-label">🔄 Flux Synergique (En amont → ${esc(tile.id)} → En aval)</div>` +
      `<div class="x3-synergy-flow">` +
      `<div class="x3-syn-box">` +
      `<div class="x3-syn-sub">✅ Tourne seule dès le Tour 1 (Plancher)</div>` +
      `<div class="x3-syn-chips">${floorHtml}</div>` +
      `<div class="x3-syn-sub" style="margin-top:0.25rem">✨ Amplifiée avec les alliés (Synergies · /64 assises)</div>` +
      `<div class="x3-syn-chips">${synHtml}</div>` +
      `<div class="x3-syn-sub" style="margin-top:0.25rem">⬅️ Qui m’alimente ?</div>` +
      `<div class="x3-syn-chips">${upHtml}</div>` +
      `</div>` +
      `<div class="x3-synergy-center-arrow"><span>→</span><span style="font-size:0.7rem">${esc(tile.id)}</span><span>→</span></div>` +
      `<div class="x3-syn-box">` +
      `<div class="x3-syn-sub">🎯 États produits &amp; Icônes allumées</div>` +
      `<div class="x3-syn-chips">${outChips.length > 0 ? outChips.join('') : '<span class="text-xs text-slate-400">Effet de contrôle direct</span>'}</div>` +
      `<div class="x3-syn-sub" style="margin-top:0.25rem">➡️ Qui j’alimente ?</div>` +
      `<div class="x3-syn-chips">${downHtml}</div>` +
      `</div>` +
      `</div>` +
      `${twinBar}` +
      `</div>`
    );
  }

  function renderDraftAnnotationBar(slotId, activeSourceKey) {
    if (activeSourceKey === 'archive_v6_2') {
      return (
        `<div class="x3-draft-bar">` +
        `<span class="text-slate-500 font-medium">📦 Archive v6.2 en lecture seule — basculez sur Panel 1 / 2 / 3 ou Mon Canon pour éditer et élire.</span>` +
        `</div>`
      );
    }
    const w = uiState.workspace.slots[slotId];
    const isThisElected = activeSourceKey === 'canon'
      ? Boolean(w.selected_source)
      : (w.selected_source === activeSourceKey);
    const electTarget = activeSourceKey === 'canon' ? (w.selected_source || 'panel_1') : activeSourceKey;
    const electLabel = isThisElected
      ? `✓ Élue dans Mon Canon (${w.selected_source === 'custom' ? 'Hybride' : PANEL_SHORT[w.selected_source]})`
      : `★ Élire ${PANEL_SHORT[electTarget] || ''} dans Mon Canon`;

    const starsHtml = [1, 2, 3, 4, 5].map(n => (
      `<button type="button" class="x3-star-btn ${w.rating >= n ? 'is-on' : ''}" ` +
      `onclick="AmazoniaExplorerV63.setSlotRating('${esc(slotId)}', ${n})" ` +
      `title="Noter ${n}/5" aria-label="Noter ${n} sur 5">★</button>`
    )).join('');

    const statusOptions = DRAFT_STATUSES.map(st => (
      `<option value="${esc(st.value)}" ${w.status === st.value ? 'selected' : ''}>${esc(st.label)}</option>`
    )).join('');

    return (
      `<div class="x3-draft-bar" data-draft-bar="${esc(slotId)}">` +
      `<button type="button" class="x3-btn x3-btn-elect ${isThisElected ? 'is-elected' : ''}" ` +
      `onclick="AmazoniaExplorerV63.electSlot('${esc(slotId)}', '${esc(electTarget)}')">${esc(electLabel)}</button>` +
      `<select class="x3-select" aria-label="Statut Draft ${esc(slotId)}" onchange="AmazoniaExplorerV63.setSlotStatus('${esc(slotId)}', this.value)">${statusOptions}</select>` +
      `<div class="x3-stars" role="group" aria-label="Appréciation ${esc(slotId)}">${starsHtml}</div>` +
      `<button type="button" class="x3-fav-btn ${w.favorite ? 'is-on' : ''}" onclick="AmazoniaExplorerV63.toggleSlotFavorite('${esc(slotId)}')" title="Coup de cœur">${w.favorite ? '♥' : '♡'}</button>` +
      `<input type="text" class="x3-comment-input" data-comment-slot="${esc(slotId)}" ` +
      `value="${esc(w.comment || '')}" placeholder="Note / intention d’auteur (sauvegarde instantanée)…" ` +
      `oninput="AmazoniaExplorerV63.setSlotCommentLive('${esc(slotId)}', this.value)" />` +
      `<span class="x3-saved-hint" id="x3-saved-${esc(slotId)}">✓ Enregistré</span>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${esc(slotId)}', '${esc(activeSourceKey === 'canon' ? (w.selected_source === 'custom' ? 'custom' : (w.selected_source || 'panel_1')) : activeSourceKey)}')">✏️ Modifier / Hybrider</button>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openDuelForSlot('${esc(slotId)}')">⚔️ Duel P1·P2·P3</button>` +
      `</div>`
    );
  }

  function renderBiComponentCard(slotId, tile, sourceInfo, tilesMap) {
    if (!tile) {
      const sp = getSlotSpecMap()[slotId];
      return (
        `<article class="x3-tile-card" data-slot-id="${esc(slotId)}" data-unelected="true">` +
        `<div class="x3-silhouette-strip">` +
        `<div class="x3-silhouette-left"><strong>${esc(slotId)}</strong> ${renderOrientedEdgeBadge(sp.origine, sp.voisin)} <span class="x3-role-pill">À trancher dans Mon Canon</span></div>` +
        `<div class="flex items-center gap-1.5">` +
        PANEL_IDS.map(pid => `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.electSlot('${esc(slotId)}', '${pid}')">Élire ${PANEL_SHORT[pid]}</button>`).join('') +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.openDuelForSlot('${esc(slotId)}')">⚔️ Comparer P1·P2·P3</button>` +
        `</div>` +
        `</div>` +
        `<div class="p-5 text-sm text-slate-500">Aucune proposition n’est encore élue sur <strong>${esc(slotId)} (${esc(sp.alias_oriente)})</strong>. Ouvrez le Duel comparatif ou cliquez sur P1 / P2 / P3 ci-dessus pour l’élire.</div>` +
        `</article>`
      );
    }

    const classes = ['x3-tile-card'];
    if (tile.nature === 'LOI_PASSIVE') classes.push('is-loi');
    if (tile.est_twist) classes.push('is-twist');
    if (sourceInfo && sourceInfo.elected && uiState.source !== 'canon') classes.push('is-elected-card');

    const digestFooter = (uiState.source === 'archive_v6_2' && typeof global.renderSlotDigestFooter === 'function')
      ? `<div class="px-5 pb-4">${global.renderSlotDigestFooter(tile.id, ['A'])}</div>`
      : '';

    return (
      `<article class="${classes.join(' ')}" data-slot-id="${esc(tile.id)}" data-nature="${esc(tile.nature)}" data-twist="${tile.est_twist ? 'true' : 'false'}">` +
      `${renderSilhouetteStrip(tile, sourceInfo)}` +
      `<div class="x3-duo-grid">` +
      `${renderMiniTuile(tile, false)}` +
      `${renderGrandeCarte(tile)}` +
      `</div>` +
      `${renderDepthSection(tile)}` +
      `${renderSynergyStrip(tile, tilesMap)}` +
      `${digestFooter}` +
      `${renderDraftAnnotationBar(tile.id, uiState.source)}` +
      `</article>`
    );
  }

  // --------------------------------------------------------------------------
  // Rendu du Bandeau Supérieur Permanent + Radar de Santé
  // --------------------------------------------------------------------------
  function renderTopBarAndRadar() {
    const canonRadar = computeHealthRadar('canon');
    const activeRadar = uiState.radarTarget === 'canon' ? canonRadar : computeHealthRadar('active_source');

    const sourceButtons = [
      { id: 'panel_1', label: 'Panel 1', cls: '' },
      { id: 'panel_2', label: 'Panel 2', cls: '' },
      { id: 'panel_3', label: 'Panel 3', cls: '' },
      { id: 'canon', label: `★ Mon Canon v6.3`, count: `${canonRadar.electedCount}/30`, cls: 'is-canon' },
      { id: 'archive_v6_2', label: '📦 Archive v6.2', cls: 'is-archive' }
    ].map(btn => (
      `<button type="button" class="x3-source-btn ${btn.cls} ${uiState.source === btn.id ? 'is-active' : ''}" ` +
      `data-source-btn="${btn.id}" onclick="AmazoniaExplorerV63.setSource('${btn.id}')">` +
      `<span>${esc(btn.label)}</span>` +
      (btn.count ? `<span class="x3-count-pill">${esc(btn.count)}</span>` : '') +
      `</button>`
    )).join('');

    const radarPills = [
      {
        key: 'elected',
        status: activeRadar.electedCount === 30 ? 'ok' : 'warn',
        text: `Élues ${activeRadar.electedCount}/30`
      },
      {
        key: 'twists',
        status: activeRadar.twists.status,
        text: `⚡ Twists 2K3 : ${activeRadar.twists.count}${activeRadar.twists.triangles2K3 ? ' · 2△ OK' : ''}`
      },
      {
        key: 'lois',
        status: activeRadar.lois.status,
        text: `⚖️ Lois : ${activeRadar.lois.count}/5 (max ${activeRadar.lois.maxPerAssise}/assise)`
      },
      {
        key: 'eveil',
        status: activeRadar.eveil.status,
        text: `☀️ Éveil (i)+(ii) : ${activeRadar.eveil.count}`
      },
      {
        key: 'sommeil',
        status: activeRadar.sommeil.status,
        text: `🌙 Sommeil E sans H : ${activeRadar.sommeil.coveredEBorders.length}/4`
      },
      {
        key: 'enrac',
        status: activeRadar.enrac.status,
        text: `🌱 Enracinements : ${activeRadar.enrac.count} (3–5)`
      },
      {
        key: 'a0',
        status: activeRadar.a0.status,
        text: `🔓 Autonomie A=0 : ${activeRadar.a0.violations.length === 0 ? activeRadar.a0.presentCount + '/6' : activeRadar.a0.violations.length + ' alerte(s)'}`
      },
      {
        key: 'synergies',
        status: activeRadar.synergies.status,
        text: `🔄 Clôture : ${activeRadar.synergies.orphans.length === 0 && activeRadar.synergies.divergenceIssues.length === 0 ? 'OK' : (activeRadar.synergies.orphans.length + activeRadar.synergies.divergenceIssues.length) + ' point(s)'}`
      }
    ].map(p => (
      `<button type="button" class="x3-radar-pill is-${p.status} ${uiState.radarDetailKey === p.key ? 'is-selected' : ''}" ` +
      `data-radar-pill="${p.key}" data-radar-status="${p.status}" onclick="AmazoniaExplorerV63.toggleRadarDetail('${p.key}')">${esc(p.text)}</button>`
    )).join('');

    const radarDetailHtml = uiState.radarDetailKey ? renderRadarDetail(activeRadar, uiState.radarDetailKey) : '';

    const viewTabs = [
      { id: 'explorer', icon: '🧩', label: '1. Explorateur & Duel P1·P2·P3', sub: 'Étudier & Choisir' },
      { id: 'simulator', icon: '🎡', label: '2. Simulateur de Table 3–6J', sub: 'Éprouver les synergies' },
      { id: 'dashboard', icon: '📋', label: '3. Tableau de bord Mon Canon', sub: `${canonRadar.electedCount}/30 · Piloter` }
    ].map(v => (
      `<button type="button" class="x3-view-tab ${uiState.view === v.id ? 'is-active' : ''}" ` +
      `data-view-tab="${v.id}" onclick="AmazoniaExplorerV63.setView('${v.id}')">` +
      `<span>${v.icon} ${esc(v.label)}</span><span class="x3-view-sub">${esc(v.sub)}</span>` +
      `</button>`
    )).join('');

    const subViewSwitch = uiState.view === 'explorer'
      ? `<div class="x3-subview-switch">` +
        `<button type="button" class="x3-subview-btn ${uiState.explorerSubView === 'cards' ? 'is-active' : ''}" data-subview="cards" onclick="AmazoniaExplorerV63.setExplorerSubView('cards')">📄 Fiches &amp; Duos de Lisière</button>` +
        `<button type="button" class="x3-subview-btn ${uiState.explorerSubView === 'duel' ? 'is-active' : ''}" data-subview="duel" onclick="AmazoniaExplorerV63.setExplorerSubView('duel')">⚔️ Duel Panel 1 | 2 | 3</button>` +
        `</div>`
      : '';

    const radarToggleBtn = uiState.source !== 'canon' && uiState.source !== 'archive_v6_2'
      ? `<button type="button" class="x3-radar-scope-toggle" onclick="AmazoniaExplorerV63.toggleRadarTarget()" title="Basculer le radar entre Mon Canon v6.3 et le panel affiché">Cible : ${esc(activeRadar.scopeLabel)} ⇄</button>`
      : '';

    return (
      `<div class="x3-topbar" data-explorer-version="${VERSION}">` +
      `<div class="x3-topbar-primary">` +
      `<div class="x3-source-group" role="tablist" aria-label="Source du catalogue">${sourceButtons}</div>` +
      `<div class="x3-topbar-tools">` +
      `<button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.openPictoGuide()">📖 Guide 32 pictos</button>` +
      `<button type="button" class="x3-tool-btn x3-tool-btn-accent" onclick="AmazoniaExplorerV63.openExportModal('gemini')">📤 Passerelles Gemini &amp; Antigravity</button>` +
      `</div>` +
      `</div>` +
      `<div class="x3-radar-strip" data-radar-scope="${esc(uiState.radarTarget)}">` +
      `<span class="x3-radar-title">🩺 Radar ${esc(activeRadar.scopeLabel)} :</span>` +
      `${radarToggleBtn}` +
      `${radarPills}` +
      `</div>` +
      `${radarDetailHtml}` +
      `<div class="x3-views-bar">` +
      `<div class="x3-view-tabs">${viewTabs}</div>` +
      `${subViewSwitch}` +
      `</div>` +
      `</div>`
    );
  }

  function renderRadarDetail(radar, key) {
    let title = '';
    let body = '';
    const actions = [];

    if (key === 'elected') {
      title = `Progression de ${radar.scopeLabel} : ${radar.electedCount} / 30 emplacements élus`;
      body = radar.unelectedIds.length === 0
        ? 'Tous les 30 emplacements sont pourvus !'
        : `Emplacements restant à élire (${radar.unelectedIds.length}) : ${radar.unelectedIds.join(', ')}.`;
      if (radar.unelectedIds.length > 0) {
        actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'draft\', \'UNELECTED\')">Filtrer les slots à trancher</button>');
        actions.push('<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setView(\'dashboard\')">Ouvrir Tableau de bord</button>');
      }
    } else if (key === 'twists') {
      title = `Twists 2K3 : ${radar.twists.count} tuile(s)`;
      const parts = [];
      if (radar.twists.triangles2K3) {
        const t1 = radar.twists.triangles2K3[0].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → ');
        const t2 = radar.twists.triangles2K3[1].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → ');
        parts.push(`✅ Géométrie 2K3 valide — <strong>Triangle 1 :</strong> ${esc(t1)} · <strong>Triangle 2 :</strong> ${esc(t2)}.`);
      } else {
        parts.push(`⚠️ Les twists actuels (${esc(radar.twists.ids.join(', ') || 'aucun')}) ne bouclent pas encore 2 triangles orientés disjoints sur les 6 Peuples.`);
      }
      if (radar.twists.missingOrigins.length > 0) {
        parts.push(`Peuples d’origine sans Twist : <strong>${esc(radar.twists.missingOrigins.join(', '))}</strong>.`);
      }
      if (radar.twists.doubleBorders.length > 0) {
        parts.push(`❌ Lisières portant > 1 Twist : ${radar.twists.doubleBorders.map(([bk, ids]) => `${esc(bk)} (${esc(ids.join(', '))})`).join(', ')}.`);
      }
      body = parts.join('<br>');
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'TWIST_2K3\')">Filtrer les Twists</button>');
    } else if (key === 'lois') {
      title = `Lois passives permanentes : ${radar.lois.count} / 5 (max ${radar.lois.maxPerAssise} / assise sur 197 assises)`;
      const parts = [`Lois présentes : ${radar.lois.ids.length > 0 ? esc(radar.lois.ids.join(', ')) : 'aucune'}.`];
      if (radar.lois.offendingAssises.length > 0) {
        parts.push(`❌ ${radar.lois.offendingAssises.length} assise(s) dépassent 2 lois : ${radar.lois.offendingAssises.slice(0, 6).map(x => `${esc(x.key)} (${x.count})`).join(', ')}.`);
      } else {
        parts.push('✅ Aucune des 197 assises ne dépasse 2 lois passives simultanées.');
      }
      body = parts.join('<br>');
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'LOI_PASSIVE\')">Filtrer les Lois passives</button>');
    } else if (key === 'eveil') {
      title = `Couverture Éveil (i)+(ii) : ${radar.eveil.count} catalyseurs (seuil ≥ 9)`;
      const parts = [
        `Règle (i) vers {H, E, I} : M=${radar.eveil.regleI.M}/2 · R=${radar.eveil.regleI.R}/2 · O=${radar.eveil.regleI.O}/2.`,
        `Règle (ii) lisières Animal–Animal : ${Object.entries(radar.eveil.regleII).map(([b, ok]) => `${b} ${ok ? '✓' : '✗'}`).join(' · ')}.`
      ];
      if (radar.eveil.uncoveredAssises.length > 0) {
        parts.push(`⚠️ ${radar.eveil.uncoveredAssises.length} assise(s) A≥1 sans catalyseur (ex. ${esc(radar.eveil.uncoveredAssises.slice(0, 5).join(', '))}).`);
      } else {
        parts.push('✅ 100 % des 196 assises avec Animaux sauvages disposent d’au moins un catalyseur d’Éveil.');
      }
      body = parts.join('<br>');
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'CATALYSEUR_EVEIL\')">Filtrer les Catalyseurs</button>');
    } else if (key === 'sommeil') {
      title = `Couverture Sommeil (E sans H) : ${radar.sommeil.coveredEBorders.length}/4 lisières E–{M,R,O,I}`;
      body =
        `Lisières couvertes : ${esc(radar.sommeil.coveredEBorders.join(', ') || 'aucune')}. ` +
        (radar.sommeil.missingEBorders.length > 0 ? `Non couvertes : ${esc(radar.sommeil.missingEBorders.join(', '))}. ` : '') +
        (radar.sommeil.uncoveredAssises.length > 0
          ? `<br>⚠️ ${radar.sommeil.uncoveredAssises.length}/30 assises (E sans H) sans levier de Rêve (ex. ${esc(radar.sommeil.uncoveredAssises.slice(0, 5).join(', '))}).`
          : '<br>✅ 30/30 assises (E sans H) disposent d’un levier de Rêve.');
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'LEVIER_REVE\')">Filtrer les Leviers de Rêve</button>');
    } else if (key === 'enrac') {
      title = `Synergies d’Enracinement : ${radar.enrac.count} (plage cible 3 à 5)`;
      body = `Tuiles dédiées : ${esc(radar.enrac.ids.join(', ') || 'aucune')}.`;
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'ENRACINEMENT\')">Filtrer les Enracinements</button>');
    } else if (key === 'a0') {
      title = `Autonomie A=0 ({H, E, I} : R1, R2, R6, R10, M4, M5)`;
      body = radar.a0.violations.length === 0
        ? `✅ Aucune dépendance Gardien détectée (${radar.a0.presentCount}/6 tuiles A=0 présentes).`
        : `❌ Dépendance Gardien détectée sur : ${esc(radar.a0.violations.join(', '))}.`;
      actions.push('<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.applyRadarFilter(\'role\', \'AUTONOMIE_A0\')">Filtrer les 6 tuiles A=0</button>');
    } else if (key === 'synergies') {
      title = 'Clôture des synergies & Divergence de lisière';
      const parts = [];
      if (radar.synergies.orphans.length > 0) {
        parts.push(`⚠️ Synergies optionnelles à 0/64 assises (aucun producteur) : ${radar.synergies.orphans.map(o => `${esc(o.slotId)} (${esc(humanizeToken(o.state).label)})`).join(', ')}.`);
      } else {
        parts.push('✅ 0 synergie orpheline : chaque amplificateur a un producteur sur les 197 assises.');
      }
      if (radar.synergies.divergenceIssues.length > 0) {
        parts.push(`⚠️ Divergence de lisière : ${radar.synergies.divergenceIssues.map(esc).join(' · ')}.`);
      } else {
        parts.push('✅ Toutes les lisières complètes divergent sur leur sortie principale.');
      }
      body = parts.join('<br>');
    }

    actions.push('<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.toggleRadarDetail(null)">✕ Fermer</button>');

    return (
      `<div class="x3-radar-detail" data-radar-detail="${esc(key)}">` +
      `<div class="x3-radar-detail-body"><strong>${esc(title)}</strong><div>${body}</div></div>` +
      `<div class="x3-radar-detail-actions">${actions.join('')}</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // Panneau Focus Ressource / Icône (Producteurs <-> Consommateurs)
  // --------------------------------------------------------------------------
  function renderResourceFocusPanel(tilesMap) {
    if (!uiState.resourceFocus) return '';
    const idx = computeResourceIndex(uiState.resourceFocus, tilesMap);

    const natHtml = idx.nativeProducers.map(n => (
      `<span class="x3-res-pill is-floor">${n.icon} ${esc(n.label)}</span>`
    )).join('');

    const prodTilesHtml = idx.producers.length > 0
      ? idx.producers.map(p => (
          `<button type="button" class="x3-tile-link-chip is-upstream" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(p.id)}')">` +
          `<strong>${esc(p.id)}</strong> ${esc(p.nom)} <span class="opacity-70">(${esc(p.alias)})</span></button>`
        )).join('')
      : '<span class="text-xs text-slate-400">Aucune tuile productrice dans cette source</span>';

    const consFloorHtml = idx.consumersFloor.map(c => (
      `<button type="button" class="x3-tile-link-chip" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(c.id)}')">` +
      `✅ <strong>${esc(c.id)}</strong> ${esc(c.nom)}</button>`
    )).join('');

    const consSynHtml = idx.consumersSynergy.map(c => (
      `<button type="button" class="x3-tile-link-chip is-downstream" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(c.id)}')">` +
      `✨ <strong>${esc(c.id)}</strong> ${esc(c.nom)} <span class="x3-cov-tag">${c.coverage.covered}/${c.coverage.total}</span></button>`
    )).join('');

    const consIconHtml = idx.consumersIcon.map(c => (
      `<button type="button" class="x3-tile-link-chip is-downstream" onclick="AmazoniaExplorerV63.jumpToSlot('${esc(c.id)}')">` +
      `🗿 <strong>${esc(c.id)}</strong> ${esc(c.nom)}</button>`
    )).join('');

    const anyConsumer = idx.consumersFloor.length + idx.consumersSynergy.length + idx.consumersIcon.length > 0;

    return (
      `<div class="x3-resource-focus" data-resource-focus="${esc(idx.key)}">` +
      `<div class="x3-rf-header">` +
      `<div class="flex items-center gap-2 flex-wrap">` +
      `<span class="text-lg">${idx.meta.icon}</span>` +
      `<strong class="text-base">${esc(idx.meta.label)}</strong>` +
      `<span class="text-xs text-slate-500">(${idx.allInvolvedIds.size} tuile(s) impliquée(s) dans ${esc(PANEL_LABELS[uiState.source] || uiState.source)})</span>` +
      `</div>` +
      `<div class="flex items-center gap-2">` +
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.resourceFilterOnly ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.toggleResourceFilterOnly()">${uiState.resourceFilterOnly ? '✓ Liste filtrée sur cette ressource' : 'Filtrer la liste sur ces tuiles'}</button>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.clearResourceFocus()">✕ Fermer</button>` +
      `</div>` +
      `</div>` +
      `<div class="x3-rf-cols">` +
      `<div class="x3-rf-col">` +
      `<div class="x3-rf-col-title">⬅️ Producteurs &amp; Déclencheurs (${idx.producers.length} tuile(s))</div>` +
      (natHtml ? `<div class="x3-syn-chips">${natHtml}</div>` : '') +
      `<div class="x3-syn-chips">${prodTilesHtml}</div>` +
      `</div>` +
      `<div class="x3-rf-col">` +
      `<div class="x3-rf-col-title">➡️ Consommateurs &amp; Bénéficiaires (${idx.consumersFloor.length + idx.consumersSynergy.length + idx.consumersIcon.length} tuile(s))</div>` +
      (idx.isIcon
        ? `<div class="x3-syn-chips">${consIconHtml || '<span class="text-xs text-slate-400">Aucun Gardien conseillé sur cette icône</span>'}</div>`
        : (anyConsumer
          ? (consFloorHtml ? `<div class="x3-syn-sub">Plancher solo</div><div class="x3-syn-chips">${consFloorHtml}</div>` : '') +
            (consSynHtml ? `<div class="x3-syn-sub">Amplificateurs Synergie</div><div class="x3-syn-chips">${consSynHtml}</div>` : '')
          : '<span class="text-xs text-slate-400">Aucune tuile consommatrice dans cette source</span>')) +
      `</div>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // VUE 1 — Explorateur & Duel P1 | P2 | P3
  // --------------------------------------------------------------------------
  function renderExplorerControls(visibleCount) {
    const f = uiState.filters;
    const ws = uiState.workspace;
    const borderChips = [
      `<button type="button" class="x3-border-chip ${uiState.selectedBorder === 'ALL' ? 'is-active' : ''}" onclick="AmazoniaExplorerV63.selectBorder('ALL')">Toutes les 15 lisières</button>`
    ].concat(ALL_15_BORDERS.map(([p1, p2]) => {
      const bk = borderKey(p1, p2);
      const pair = BORDER_TO_SLOTS[bk] || [];
      const dots = pair.map(sid => {
        const w = ws.slots[sid];
        const cls = w && w.is_modified ? 'is-modified' : (w && w.selected_source ? 'is-elected' : (w && (w.status === 'HESITATION' || w.status === 'A_HYBRIDER') ? 'is-warn' : ''));
        return `<span class="x3-slot-dot ${cls}" title="${esc(sid)}"></span>`;
      }).join('');
      return (
        `<button type="button" class="x3-border-chip ${uiState.selectedBorder === bk ? 'is-active' : ''}" ` +
        `data-border-chip="${esc(bk)}" onclick="AmazoniaExplorerV63.selectBorder('${esc(bk)}')">` +
        `<span>${esc(p1)}↔${esc(p2)}</span>${dots}</button>`
      );
    })).join('');

    const pictoTag = f.picto && getPictosRef()[f.picto]
      ? `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.setPictoFilter(null)">Pictogramme : ${esc(getPictosRef()[f.picto].symbole)} ${esc(getPictosRef()[f.picto].libelle)} ✕</button>`
      : '';

    const hasActiveFilter = Boolean(
      f.search || f.peuple !== 'ALL' || f.family !== 'ALL' || f.role !== 'ALL' ||
      f.draft !== 'ALL' || f.picto || uiState.selectedBorder !== 'ALL' || uiState.resourceFilterOnly
    );

    const quickResHtml = QUICK_RESOURCES.map(tok => {
      const cls = tok.startsWith('ICONE_') ? 'is-icon' : '';
      return renderResourceChipBtn(tok, cls);
    }).join('');

    return (
      `<div class="x3-controls-card">` +
      `<div class="x3-filter-row">` +
      `<input type="text" id="x3-search-input" class="x3-search-input" value="${esc(f.search)}" ` +
      `placeholder="Rechercher un animal, une règle, un dilemme, une note…" ` +
      `oninput="AmazoniaExplorerV63.setFilter('search', this.value)" />` +
      `<select class="x3-select" aria-label="Filtrer par Peuple" onchange="AmazoniaExplorerV63.setFilter('peuple', this.value)">` +
      `<option value="ALL" ${f.peuple === 'ALL' ? 'selected' : ''}>Tous Peuples</option>` +
      PEUPLE_ORDER.map(p => `<option value="${p}" ${f.peuple === p ? 'selected' : ''}>${p} · ${esc(PEUPLE_META[p].nom)}</option>`).join('') +
      `</select>` +
      `<select class="x3-select" aria-label="Filtrer par Famille" onchange="AmazoniaExplorerV63.setFilter('family', this.value)">` +
      `<option value="ALL" ${f.family === 'ALL' ? 'selected' : ''}>Toutes Familles</option>` +
      `<option value="GARDIEN" ${f.family === 'GARDIEN' ? 'selected' : ''}>Gardiens (G1–G15)</option>` +
      `<option value="REVE" ${f.family === 'REVE' ? 'selected' : ''}>Rêves (R1–R10)</option>` +
      `<option value="CROISSANCE" ${f.family === 'CROISSANCE' ? 'selected' : ''}>Nids (M1–M5)</option>` +
      `</select>` +
      `<select class="x3-select" aria-label="Filtrer par Rôle" onchange="AmazoniaExplorerV63.setFilter('role', this.value)">` +
      `<option value="ALL" ${f.role === 'ALL' ? 'selected' : ''}>Tous Rôles &amp; Natures</option>` +
      `<option value="TWIST_2K3" ${f.role === 'TWIST_2K3' ? 'selected' : ''}>⚡ Twists 2K3</option>` +
      `<option value="LOI_PASSIVE" ${f.role === 'LOI_PASSIVE' ? 'selected' : ''}>⚖️ Lois passives</option>` +
      `<option value="CATALYSEUR_EVEIL" ${f.role === 'CATALYSEUR_EVEIL' ? 'selected' : ''}>☀️ Catalyseurs d’Éveil</option>` +
      `<option value="LEVIER_REVE" ${f.role === 'LEVIER_REVE' ? 'selected' : ''}>🌙 Leviers de Rêve</option>` +
      `<option value="ENRACINEMENT" ${f.role === 'ENRACINEMENT' ? 'selected' : ''}>🌱 Synergies d’Enracinement</option>` +
      `<option value="AUTONOMIE_A0" ${f.role === 'AUTONOMIE_A0' ? 'selected' : ''}>🔓 Autonomie A=0</option>` +
      `</select>` +
      `<select class="x3-select" aria-label="Filtrer par Statut Draft" onchange="AmazoniaExplorerV63.setFilter('draft', this.value)">` +
      `<option value="ALL" ${f.draft === 'ALL' ? 'selected' : ''}>Tous Statuts Draft</option>` +
      `<option value="ELECTED" ${f.draft === 'ELECTED' ? 'selected' : ''}>★ Élues dans Mon Canon</option>` +
      `<option value="UNELECTED" ${f.draft === 'UNELECTED' ? 'selected' : ''}>○ À trancher</option>` +
      `<option value="HESITATION" ${f.draft === 'HESITATION' ? 'selected' : ''}>🤔 Hésitation</option>` +
      `<option value="A_HYBRIDER" ${f.draft === 'A_HYBRIDER' ? 'selected' : ''}>🧬 À hybrider</option>` +
      `<option value="RETENUE" ${f.draft === 'RETENUE' ? 'selected' : ''}>✅ Retenue</option>` +
      `<option value="ALTERNATIVE" ${f.draft === 'ALTERNATIVE' ? 'selected' : ''}>🔄 Alternative</option>` +
      `<option value="ECARTEE" ${f.draft === 'ECARTEE' ? 'selected' : ''}>🚫 Écartée</option>` +
      `<option value="MODIFIED" ${f.draft === 'MODIFIED' ? 'selected' : ''}>✏️ Modifiées / Hybrides</option>` +
      `<option value="COMMENTED" ${f.draft === 'COMMENTED' ? 'selected' : ''}>💬 Avec commentaire</option>` +
      `<option value="FAVORITE" ${f.draft === 'FAVORITE' ? 'selected' : ''}>♥ Coups de cœur</option>` +
      `</select>` +
      `${pictoTag}` +
      (hasActiveFilter ? `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.resetFilters()">↺ Réinitialiser</button>` : '') +
      `<span class="text-xs font-mono font-semibold text-slate-600 ml-auto">${visibleCount} / 30 emplacements</span>` +
      `</div>` +
      `<div class="x3-borders-rail" aria-label="Navigation par lisières">${borderChips}</div>` +
      `<div class="x3-quick-resources" aria-label="Filtre Ressource ou Icône en 1 clic">` +
      `<span class="text-[11px] font-bold uppercase tracking-wider text-slate-500 mr-1">Ressource / Icône :</span>` +
      `${quickResHtml}` +
      `</div>` +
      `</div>`
    );
  }

  function renderExplorerCardsView() {
    const visibleIds = getFilteredSlotIds();
    const visibleSet = new Set(visibleIds);
    const tilesMap = getActiveTilesMap(uiState.source);
    const sections = [];

    if (uiState.source === 'archive_v6_2') {
      sections.push(
        `<div class="x3-archive-banner">` +
        `<div><strong>📦 Archive v6.2 (Canon 0 sanctuarisé · lecture seule)</strong> — Référence historique conservée pour comparaison.</div>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.setSource('panel_1')">Revenir aux Panels v6.3.1</button>` +
        `</div>`
      );
    }

    sections.push(renderExplorerControls(visibleIds.length));
    if (uiState.resourceFocus) sections.push(renderResourceFocusPanel(tilesMap));

    if (visibleIds.length === 0) {
      sections.push('<div class="x3-empty-state">Aucun emplacement ne correspond aux filtres actifs. <button type="button" class="x3-btn x3-btn-sm ml-2" onclick="AmazoniaExplorerV63.resetFilters()">Réinitialiser les filtres</button></div>');
      return sections.join('');
    }

    ALL_15_BORDERS.forEach(([p1, p2]) => {
      const bk = borderKey(p1, p2);
      const pair = (BORDER_TO_SLOTS[bk] || []).filter(sid => visibleSet.has(sid));
      if (pair.length === 0) return;

      const cardsHtml = pair.map(sid => {
        const res = getEffectiveTileForSlot(sid, uiState.source);
        return renderBiComponentCard(sid, res.tile, res, tilesMap);
      }).join('');

      sections.push(
        `<section class="x3-border-section" data-border-section="${esc(bk)}">` +
        `<div class="x3-border-banner">` +
        `<div class="x3-border-banner-left">` +
        `${renderPeuplePill(p1, true)} <span>↔</span> ${renderPeuplePill(p2, true)}` +
        `<span class="x3-border-banner-title">Lisière ${esc(p1)} ↔ ${esc(p2)}</span>` +
        `<span class="x3-border-meta-pill">Jumelles co-présentes à 100 % : ${(BORDER_TO_SLOTS[bk] || []).join(' & ')}</span>` +
        `</div>` +
        `<div class="flex items-center gap-1.5">` +
        (BORDER_TO_SLOTS[bk] || []).map(sid => (
          `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openDuelForSlot('${esc(sid)}')">⚔️ Duel ${esc(sid)}</button>`
        )).join('') +
        `</div>` +
        `</div>` +
        `${cardsHtml}` +
        `</section>`
      );
    });

    return sections.join('');
  }

  function renderDuelView() {
    const specs = getSlotsSpec();
    const specMap = getSlotSpecMap();
    const slotId = specMap[uiState.duelSlotId] ? uiState.duelSlotId : 'G1';
    const sp = specMap[slotId];
    const curIdx = specs.findIndex(s => s.id === slotId);
    const prevId = specs[(curIdx - 1 + specs.length) % specs.length].id;
    const nextId = specs[(curIdx + 1) % specs.length].id;
    const twinId = TWIN_BY_SLOT[slotId];
    const wsSlot = uiState.workspace.slots[slotId];

    const slotBtns = specs.map(s => {
      const w = uiState.workspace.slots[s.id];
      const dotCls = w && w.is_modified ? 'is-modified' : (w && w.selected_source ? 'is-elected' : (w && (w.status === 'HESITATION' || w.status === 'A_HYBRIDER') ? 'is-warn' : ''));
      return (
        `<button type="button" class="x3-duel-slot-btn ${s.id === slotId ? 'is-active' : ''}" ` +
        `data-duel-slot-btn="${esc(s.id)}" onclick="AmazoniaExplorerV63.setDuelSlot('${esc(s.id)}')">` +
        `<span class="x3-slot-dot ${dotCls}"></span>${esc(s.id)}</button>`
      );
    }).join('');

    const colsHtml = PANEL_IDS.map(pid => {
      const tile = getPanelTile(pid, slotId);
      if (!tile) return '';
      const tp = tile.tuile_plateau || {};
      const cj = tile.carte_joueur || {};
      const tr = cj.texte_regle || {};
      const dr = cj.decision_et_renoncement || {};
      const isElected = wsSlot.selected_source === pid;
      const isLoi = tile.nature === 'LOI_PASSIVE';
      const isTwist = Boolean(tile.est_twist);
      const colClasses = ['x3-duel-col'];
      if (isElected) colClasses.push('is-elected');
      if (isLoi) colClasses.push('is-loi');
      if (isTwist) colClasses.push('is-twist');

      const badges = [];
      if (isLoi) badges.push('<span class="x3-role-pill" style="background:#1e293b;color:#fff">⚖️ Loi passive</span>');
      if (isTwist) badges.push('<span class="x3-role-pill" style="background:#ea580c;color:#fff">⚡ Twist 2K3</span>');
      if ((tile.roles_portes || []).includes('CATALYSEUR_EVEIL')) badges.push('<span class="x3-role-pill x3-role-eveil">☀️ Éveil</span>');
      if ((tile.roles_portes || []).includes('LEVIER_REVE')) badges.push('<span class="x3-role-pill x3-role-reve">🌙 Levier Rêve</span>');
      if ((tile.roles_portes || []).includes('ENRACINEMENT')) badges.push('<span class="x3-role-pill x3-role-enrac">🌱 Enracinement</span>');

      const recIcon = tp.icone_conseillee ? GUARDIAN_ICON_BY_ID[String(tp.icone_conseillee).toUpperCase()] : null;
      const pictos = (tp.pictogrammes || []).map(renderPictoToken).join('');
      const mcp = tp.mots_cles_plateau || {};
      const miniKwBits = [];
      if (mcp.face_1) miniKwBits.push(`<div><strong>F1 :</strong> ${esc(mcp.face_1)}</div>`);
      if (mcp.face_2) miniKwBits.push(`<div><strong>F2 :</strong> ${esc(mcp.face_2)}</div>`);
      if (mcp.enracine) miniKwBits.push(`<div class="text-emerald-800"><strong>🌱 :</strong> ${esc(mcp.enracine)}</div>`);
      const floorChips = normalizeStateList(tile.entrees_plancher).map(st => `<span class="x3-res-pill is-floor">${humanizeToken(st).icon} ${esc(humanizeToken(st).label)}</span>`).join('');
      const synChips = normalizeStateList(tile.entrees_synergie).map(st => `<span class="x3-res-pill is-synergy">${humanizeToken(st).icon} ${esc(humanizeToken(st).label)}</span>`).join('');

      return (
        `<div class="${colClasses.join(' ')}" data-duel-col="${pid}">` +
        `<div class="x3-duel-col-head">` +
        `<div class="flex items-center justify-between gap-2">` +
        `<strong class="text-sm">${esc(PANEL_LABELS[pid])}</strong>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-elect ${isElected ? 'is-elected' : ''}" ` +
        `data-elect-btn="${pid}" onclick="AmazoniaExplorerV63.electSlot('${esc(slotId)}', '${pid}')">` +
        `${isElected ? '✓ Élue dans Mon Canon' : '★ Élire dans Mon Canon'}</button>` +
        `</div>` +
        `<div class="font-serif font-bold text-base text-slate-900">${esc(cj.titre_complet || tp.nom_court || slotId)}</div>` +
        `<div class="flex flex-wrap gap-1">${badges.join('')}</div>` +
        `<div class="flex items-center justify-between gap-2 flex-wrap">` +
        `<span class="x3-mini-window">${recIcon ? recIcon.icon + ' ' + esc(recIcon.label) : '⏱ ' + esc(formatFenetreLabel(tp.fenetre_badge))}</span>` +
        `<div class="flex gap-1">${pictos}</div>` +
        `</div>` +
        (miniKwBits.length > 0 ? `<div class="text-[11px] bg-white/90 rounded-lg px-2 py-1.5 border border-slate-200 space-y-0.5 text-slate-700">${miniKwBits.join('')}</div>` : '') +
        `</div>` +
        `<div class="x3-duel-col-body">` +
        (cj.pitch_ambiance ? `<div class="italic text-xs text-slate-600 border-l-2 border-emerald-400 pl-2">${esc(cj.pitch_ambiance)}</div>` : '') +
        `<div class="x3-rule-block ${isLoi ? 'is-loi-rule' : ''}"><div class="x3-rule-label">${isLoi ? '⚖️ Loi permanente' : 'Face 1'}</div><div>${esc(tr.face_1 || '—')}</div></div>` +
        (tr.face_2 ? `<div class="x3-rule-block is-face2"><div class="x3-rule-label">✨ Face 2</div><div>${esc(tr.face_2)}</div></div>` : '') +
        (tr.enracine ? `<div class="x3-rule-block is-enracine"><div class="x3-rule-label">🌱 Enraciné</div><div>${esc(tr.enracine)}</div></div>` : '') +
        `<div class="text-xs bg-slate-50 rounded-lg p-2.5 border border-slate-200 space-y-1">` +
        `<div><strong>🎯 Choix :</strong> ${esc(dr.choix || '—')}</div>` +
        `<div><strong>⚖️ Renoncement :</strong> ${esc(dr.renoncement || '—')}</div>` +
        `</div>` +
        `<div class="space-y-1">` +
        `<div class="x3-syn-sub">Plancher solo :</div><div class="x3-syn-chips">${floorChips || '<span class="text-xs text-slate-400">Autonome</span>'}</div>` +
        `<div class="x3-syn-sub">Synergies :</div><div class="x3-syn-chips">${synChips || '<span class="text-xs text-slate-400">—</span>'}</div>` +
        `</div>` +
        `</div>` +
        `<div class="x3-duel-col-foot">` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${esc(slotId)}', '${pid}')">✏️ Hybrider depuis ${PANEL_SHORT[pid]}</button>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-elect ${isElected ? 'is-elected' : ''}" onclick="AmazoniaExplorerV63.electSlot('${esc(slotId)}', '${pid}')">${isElected ? '✓ Élue' : '★ Élire ' + PANEL_SHORT[pid]}</button>` +
        `</div>` +
        `</div>`
      );
    }).join('');

    const customBanner = wsSlot.is_modified && wsSlot.custom_tile
      ? `<div class="rounded-xl bg-amber-50 border border-amber-300 px-4 py-2.5 text-xs flex flex-wrap items-center justify-between gap-2">` +
        `<div><strong>✏️ Version hybride / modifiée enregistrée dans Mon Canon :</strong> ${esc((wsSlot.custom_tile.carte_joueur && wsSlot.custom_tile.carte_joueur.titre_complet) || slotId)}</div>` +
        `<div class="flex gap-2">` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.openEditor('${esc(slotId)}', 'custom')">✏️ Rouvrir l’éditeur</button>` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.electSlot('${esc(slotId)}', 'custom')">${wsSlot.selected_source === 'custom' ? '✓ Élue' : '★ Élire ma version'}</button>` +
        `</div></div>`
      : '';

    return (
      `<div class="x3-duel-shell" data-duel-slot="${esc(slotId)}">` +
      `<div class="x3-duel-slot-nav">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<div class="flex items-center gap-2 flex-wrap">` +
      `<span class="x3-mini-id">${esc(slotId)}</span>` +
      `${renderOrientedEdgeBadge(sp.origine, sp.voisin)}` +
      `<strong class="text-sm">${esc(sp.famille === 'GARDIEN' ? (getCastingRef()[slotId] ? getCastingRef()[slotId].nom_animal : slotId) : `${sp.famille} ${sp.alias_oriente}`)}</strong>` +
      (twinId ? `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setDuelSlot('${esc(twinId)}')">🔗 Voir jumelle ${esc(twinId)}</button>` : '') +
      `</div>` +
      `<div class="flex items-center gap-1.5">` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setDuelSlot('${esc(prevId)}')">← ${esc(prevId)}</button>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setDuelSlot('${esc(nextId)}')">${esc(nextId)} →</button>` +
      `</div>` +
      `</div>` +
      `<div class="x3-duel-slots-grid">${slotBtns}</div>` +
      `</div>` +
      `${customBanner}` +
      `<div class="x3-duel-grid">${colsHtml}</div>` +
      `<div class="x3-tile-card">${renderDraftAnnotationBar(slotId, 'canon')}</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // VUE 2 — Simulateur de Table 3 à 6 Peuples
  // --------------------------------------------------------------------------
  function renderTableWheelSvg(sim) {
    const cx = 130;
    const cy = 122;
    const r = 82;
    const n = sim.n;
    const coords = sim.peuples.map((p, i) => {
      const ang = -Math.PI / 2 + (2 * Math.PI * i) / n;
      return { p, x: cx + r * Math.cos(ang), y: cy + r * Math.sin(ang) };
    });

    const edgesSvg = coords.map((c, i) => {
      const next = coords[(i + 1) % n];
      const mx = (c.x + next.x) / 2;
      const my = (c.y + next.y) / 2;
      const b = sim.borders[i];
      return (
        `<line x1="${c.x.toFixed(1)}" y1="${c.y.toFixed(1)}" x2="${next.x.toFixed(1)}" y2="${next.y.toFixed(1)}" stroke="#357054" stroke-width="2.5" stroke-opacity="0.65" />` +
        `<rect x="${(mx - 22).toFixed(1)}" y="${(my - 9).toFixed(1)}" width="44" height="18" rx="9" fill="#ffffff" stroke="#b8d5c4" stroke-width="1" />` +
        `<text x="${mx.toFixed(1)}" y="${(my + 3.5).toFixed(1)}" text-anchor="middle" font-size="9" font-weight="700" fill="#1a3529">${esc(b.slots.join('·'))}</text>`
      );
    }).join('');

    const nodesSvg = coords.map(c => {
      const col = PEUPLE_SVG_COLORS[c.p] || { fill: '#f1f5f9', stroke: '#64748b', text: '#0f172a' };
      const isHl = uiState.simHighlightPeuple === c.p;
      return (
        `<g style="cursor:pointer" onclick="AmazoniaExplorerV63.toggleSimHighlight('${c.p}')">` +
        `<circle cx="${c.x.toFixed(1)}" cy="${c.y.toFixed(1)}" r="${isHl ? 24 : 21}" fill="${col.fill}" stroke="${col.stroke}" stroke-width="${isHl ? 3.5 : 2}" />` +
        `<text x="${c.x.toFixed(1)}" y="${(c.y + 4).toFixed(1)}" text-anchor="middle" font-size="13" font-weight="800" fill="${col.text}">${esc(c.p)}</text>` +
        `</g>`
      );
    }).join('');

    return (
      `<svg class="x3-wheel-svg" viewBox="0 0 260 244" width="244" height="230" role="img" aria-label="Roue de la table ${esc(sim.canonKey)}">` +
      `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#dbe7df" stroke-dasharray="4 4" stroke-width="1.2" />` +
      `${edgesSvg}` +
      `${nodesSvg}` +
      `<text x="${cx}" y="${cy - 4}" text-anchor="middle" font-size="11" font-weight="800" fill="#1a3529">${esc(sim.canonKey)}</text>` +
      `<text x="${cx}" y="${cy + 12}" text-anchor="middle" font-size="9.5" font-weight="600" fill="#475569">${sim.n} Peuples · ${sim.n * 2} tuiles</text>` +
      `</svg>`
    );
  }

  function renderSimulatorView() {
    const sim = analyzeTableSimulation(uiState.simPeuples, uiState.source);
    const activeTilesMap = {};
    sim.tileEntries.forEach(e => { if (e.tile) activeTilesMap[e.slotId] = e.tile; });

    const presetsHtml = PRESET_TABLES.map(pr => {
      const isAct = canonicalizeAssise(pr.peuples).key === sim.canonKey;
      return (
        `<button type="button" class="x3-btn x3-btn-sm ${isAct ? 'x3-btn-primary' : ''}" ` +
        `data-sim-preset="${esc(pr.key)}" onclick="AmazoniaExplorerV63.setSimPreset('${esc(pr.key)}')" ` +
        `title="${esc(pr.tag)}">${esc(pr.label)} <span class="opacity-75 font-normal">· ${esc(pr.tag)}</span></button>`
      );
    }).join('');

    const activeSeatsHtml = sim.peuples.map((p, idx) => (
      `<span class="x3-seat-pill x3-peuple-${p}">` +
      `<span>#${idx + 1}</span>${getPeupleIconHtml(p, 13)}<span>${esc(PEUPLE_META[p].short)}</span>` +
      (idx > 0 ? `<button type="button" class="x3-seat-move" title="Décaler à gauche" onclick="AmazoniaExplorerV63.moveSimPeuple('${p}', -1)">◀</button>` : '') +
      (idx < sim.n - 1 ? `<button type="button" class="x3-seat-move" title="Décaler à droite" onclick="AmazoniaExplorerV63.moveSimPeuple('${p}', 1)">▶</button>` : '') +
      `<button type="button" class="x3-seat-move" title="Retirer de la table" onclick="AmazoniaExplorerV63.toggleSimPeuple('${p}')">✕</button>` +
      `</span>`
    )).join('');

    const absentPeuples = PEUPLE_ORDER.filter(p => !sim.peuples.includes(p));
    const absentHtml = absentPeuples.map(p => (
      `<button type="button" class="x3-seat-pill is-inactive" onclick="AmazoniaExplorerV63.toggleSimPeuple('${p}')">` +
      `+ ${getPeupleIconHtml(p, 13)} ${esc(PEUPLE_META[p].short)}</button>`
    )).join('');

    const accHtml = sim.accessories.map(acc => (
      `<div class="p-2.5 rounded-lg border border-slate-200 bg-slate-50/80 text-xs">` +
      `<div class="flex items-center justify-between gap-1 mb-1">` +
      `<span class="font-bold">${renderPeuplePill(acc.code, true)}</span>` +
      `<span class="text-[10px] font-semibold px-1.5 py-0.5 rounded bg-white border border-slate-200">${esc(acc.tierLabel)}</span>` +
      `</div>` +
      `<div class="font-semibold text-slate-800">${acc.icon} ${esc(acc.title)}</div>` +
      `<div class="text-[11px] text-slate-600 mt-0.5">${esc(acc.summary)}</div>` +
      `</div>`
    )).join('');

    const modulesHtml = [
      { key: 'gardiens', label: '🗿 Gardiens & Éveil', on: sim.modules.gardiens },
      { key: 'reves', label: '🌙 Rêves & Sommeil', on: sim.modules.reves },
      { key: 'essaim', label: '🐜 Module Essaim', on: sim.modules.essaim }
    ].map(m => (
      `<span class="x3-radar-pill ${m.on ? 'is-ok' : ''}" data-sim-module="${m.key}" data-active="${m.on ? 'true' : 'false'}">${m.label} : ${m.on ? 'Actif' : 'Inactif'}</span>`
    )).join('');

    const chainsHtml = sim.completeChains.length > 0
      ? sim.completeChains.slice(0, 14).map(ch => (
          `<div class="x3-chain-item">` +
          `<span class="font-semibold text-emerald-800">${esc(ch.fromLabel)}</span>` +
          `<span>→</span>` +
          `<span class="x3-res-pill ${ch.kind === 'guardian_icon' ? 'is-icon' : 'is-synergy'}" onclick="AmazoniaExplorerV63.focusResource('${esc(ch.via)}')">${ch.viaMeta.icon} ${esc(ch.viaMeta.label)}</span>` +
          `<span>→</span>` +
          `<span class="font-semibold text-amber-900">${esc(ch.toLabel)}</span>` +
          `</div>`
        )).join('')
      : '<div class="text-xs text-slate-500">Aucune chaîne inter-tuiles détectée (les tuiles tournent sur leurs planchers solo et accessoires).</div>';

    const isolatedHtml = sim.isolatedAmplifiers.length > 0
      ? sim.isolatedAmplifiers.map(iso => (
          `<div class="x3-isolated-item" data-isolated-amplifier="${esc(iso.slotId)}">` +
          `⚠️ <strong>${esc(iso.slotId)} · ${esc(iso.tileName)}</strong> : son amplificateur <strong>${iso.stateMeta.icon} ${esc(iso.stateMeta.label)}</strong> n’a aucun producteur autour de cette table <span class="opacity-80">(plancher solo actif)</span>.` +
          `</div>`
        )).join('')
      : '<div class="p-2.5 rounded-lg bg-emerald-50 border border-emerald-200 text-xs text-emerald-900">✅ Tous les amplificateurs synergiques présents autour de cette table ont un producteur actif !</div>';

    const visibleEntries = uiState.simHighlightPeuple
      ? sim.tileEntries.filter(e => {
          const sp = getSlotSpecMap()[e.slotId];
          return sp && (sp.origine === uiState.simHighlightPeuple || sp.voisin === uiState.simHighlightPeuple);
        })
      : sim.tileEntries;

    const cardsHtml = visibleEntries.map(e => renderBiComponentCard(e.slotId, e.tile, e, activeTilesMap)).join('');

    const missingBanner = sim.metrics.missingCanonCount > 0
      ? `<div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-950 flex flex-wrap items-center justify-between gap-2">` +
        `<span>ℹ️ <strong>${sim.metrics.missingCanonCount}</strong> emplacement(s) de cette table ne sont pas encore élu(s) dans <strong>Mon Canon v6.3</strong> — vous pouvez les élire directement ci-dessous ou basculer sur un panel candidat.</span>` +
        `<div class="flex gap-1.5">${PANEL_IDS.map(pid => `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setSource('${pid}')">${PANEL_LABELS[pid]}</button>`).join('')}</div>` +
        `</div>`
      : '';

    return (
      `<div class="space-y-4" data-simulator-assise="${esc(sim.canonKey)}">` +
      `<div class="x3-sim-panel">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<div><h2 class="font-serif text-xl font-bold text-slate-900">🎡 Simulateur de Table — ${esc(sim.canonKey)} (${sim.n} joueurs · ${sim.n * 2} tuiles actives)</h2>` +
      `<p class="text-xs text-slate-500">Source active : <strong>${esc(PANEL_LABELS[uiState.source] || uiState.source)}</strong> · Composez l’ordre exact autour de la roue pour éprouver les synergies réelles.</p></div>` +
      `<div class="flex flex-wrap gap-1.5">${modulesHtml}</div>` +
      `</div>` +
      `${missingBanner}` +
      `<div class="flex flex-wrap gap-1.5 items-center"><span class="text-xs font-bold text-slate-600 mr-1">Tables témoins :</span>${presetsHtml}</div>` +
      `<div class="x3-sim-grid">` +
      `<div class="x3-sim-wheel-box">` +
      `${renderTableWheelSvg(sim)}` +
      `<div class="text-[11px] text-slate-500 text-center">Cliquez un Peuple sur la roue pour isoler ses lisières${uiState.simHighlightPeuple ? ` · <button type="button" class="underline font-semibold" onclick="AmazoniaExplorerV63.toggleSimHighlight(null)">Tout afficher</button>` : ''}</div>` +
      `</div>` +
      `<div class="space-y-3">` +
      `<div><div class="x3-section-label mb-1.5">Ordre autour de la table (3 à 6 Peuples)</div>` +
      `<div class="x3-sim-seats-row">${activeSeatsHtml}${absentHtml}</div></div>` +
      `<div class="x3-sim-metrics">` +
      `<div class="x3-metric-card ${sim.metrics.loisAlert ? 'is-err' : 'is-ok'}"><div class="x3-metric-val">${sim.metrics.loisCount} / 2</div><div class="x3-metric-lbl">⚖️ Lois passives</div></div>` +
      `<div class="x3-metric-card"><div class="x3-metric-val">${sim.metrics.twistsCount}</div><div class="x3-metric-lbl">⚡ Twists 2K3</div></div>` +
      `<div class="x3-metric-card ${sim.metrics.eveilAlert ? 'is-err' : (sim.modules.gardiens ? 'is-ok' : '')}"><div class="x3-metric-val">${sim.modules.gardiens ? sim.metrics.eveilCount : '—'}</div><div class="x3-metric-lbl">☀️ Catalyseurs Éveil</div></div>` +
      `<div class="x3-metric-card ${sim.metrics.sommeilAlert ? 'is-err' : (sim.modules.reves ? 'is-ok' : '')}"><div class="x3-metric-val">${sim.modules.reves ? sim.metrics.sommeilCount : '—'}</div><div class="x3-metric-lbl">🌙 Leviers Sommeil</div></div>` +
      `<div class="x3-metric-card"><div class="x3-metric-val">${sim.metrics.enracCount}</div><div class="x3-metric-lbl">🌱 Enracinements</div></div>` +
      `</div>` +
      `<div><div class="x3-section-label mb-1.5">✨ Accessoires 3+3 présents à cette table (${sim.accessories.length})</div>` +
      `<div class="grid grid-cols-1 md:grid-cols-2 gap-2">${accHtml}</div></div>` +
      `</div>` +
      `</div>` +
      `<div class="x3-chains-box">` +
      `<div class="space-y-1.5"><div class="x3-section-label">🔗 Chaînes de moteurs bouclées à cette table (${sim.completeChains.length})</div><div class="space-y-1.5">${chainsHtml}</div></div>` +
      `<div class="space-y-1.5"><div class="x3-section-label">🔍 Contrôle des amplificateurs isolés (${sim.isolatedAmplifiers.length})</div><div class="space-y-1.5">${isolatedHtml}</div></div>` +
      `</div>` +
      `</div>` +
      (uiState.resourceFocus ? renderResourceFocusPanel(activeTilesMap) : '') +
      `<div class="space-y-4">${cardsHtml}</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // VUE 3 — Tableau de bord Atelier Mon Canon (30 slots)
  // --------------------------------------------------------------------------
  function renderDashboardView() {
    const specs = getSlotsSpec();
    const ws = uiState.workspace;
    const radar = computeHealthRadar('canon');

    let modifiedCount = 0;
    let toArbitrateCount = 0;
    let commentedCount = 0;
    specs.forEach(sp => {
      const w = ws.slots[sp.id];
      if (w.is_modified) modifiedCount++;
      if (!w.selected_source || w.status === 'HESITATION' || w.status === 'A_HYBRIDER') toArbitrateCount++;
      if (w.comment && w.comment.trim()) commentedCount++;
    });

    const dashFilters = [
      { id: 'ALL', label: `Tous (30)` },
      { id: 'TO_ARBITRATE', label: `Points à arbitrer (${toArbitrateCount})` },
      { id: 'UNELECTED', label: `À trancher (${radar.unelectedIds.length})` },
      { id: 'HESITATION_HYBRID', label: `Hésitation / À hybrider` },
      { id: 'MODIFIED', label: `Hybride / Édité (${modifiedCount})` },
      { id: 'COMMENTED', label: `Avec notes (${commentedCount})` },
      { id: 'FAVORITE', label: `♥ Coups de cœur` }
    ].map(df => (
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.dashFilter === df.id ? 'x3-btn-primary' : ''}" ` +
      `onclick="AmazoniaExplorerV63.setDashFilter('${df.id}')">${esc(df.label)}</button>`
    )).join('');

    const rowsHtml = specs.filter(sp => {
      const w = ws.slots[sp.id];
      if (uiState.dashFilter === 'TO_ARBITRATE') return !w.selected_source || w.status === 'HESITATION' || w.status === 'A_HYBRIDER';
      if (uiState.dashFilter === 'UNELECTED') return !w.selected_source;
      if (uiState.dashFilter === 'HESITATION_HYBRID') return w.status === 'HESITATION' || w.status === 'A_HYBRIDER';
      if (uiState.dashFilter === 'MODIFIED') return Boolean(w.is_modified);
      if (uiState.dashFilter === 'COMMENTED') return Boolean(w.comment && w.comment.trim());
      if (uiState.dashFilter === 'FAVORITE') return Boolean(w.favorite);
      return true;
    }).map(sp => {
      const sid = sp.id;
      const w = ws.slots[sid];
      const res = getCanonSlotResolved(sid, null);
      const tile = res.tile;
      const title = tile ? ((tile.carte_joueur && tile.carte_joueur.titre_complet) || (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid) : '— À trancher —';
      const roleTags = [];
      if (tile) {
        if (tile.est_twist) roleTags.push('<span class="x3-role-pill" style="background:#ea580c;color:#fff">⚡</span>');
        if (tile.nature === 'LOI_PASSIVE') roleTags.push('<span class="x3-role-pill" style="background:#334155;color:#fff">⚖️</span>');
        if ((tile.roles_portes || []).includes('CATALYSEUR_EVEIL')) roleTags.push('<span class="x3-role-pill x3-role-eveil">☀️</span>');
        if ((tile.roles_portes || []).includes('LEVIER_REVE')) roleTags.push('<span class="x3-role-pill x3-role-reve">🌙</span>');
        if ((tile.roles_portes || []).includes('ENRACINEMENT')) roleTags.push('<span class="x3-role-pill x3-role-enrac">🌱</span>');
      }

      const srcPills = PANEL_IDS.map(pid => (
        `<button type="button" class="x3-src-mini ${w.selected_source === pid ? 'is-active' : ''}" ` +
        `onclick="AmazoniaExplorerV63.electSlot('${sid}', '${pid}')">${PANEL_SHORT[pid]}</button>`
      )).join('') +
        (w.is_modified ? `<button type="button" class="x3-src-mini is-custom ${w.selected_source === 'custom' ? 'is-active' : ''}" onclick="AmazoniaExplorerV63.electSlot('${sid}', 'custom')">Hyb</button>` : '') +
        (w.selected_source ? `<button type="button" class="x3-src-mini" title="Remettre À trancher" onclick="AmazoniaExplorerV63.clearSlotElection('${sid}')">○</button>` : '');

      const statusOptions = DRAFT_STATUSES.map(st => (
        `<option value="${esc(st.value)}" ${w.status === st.value ? 'selected' : ''}>${esc(st.label)}</option>`
      )).join('');

      const stars = [1, 2, 3, 4, 5].map(n => (
        `<button type="button" class="x3-star-btn ${w.rating >= n ? 'is-on' : ''}" onclick="AmazoniaExplorerV63.setSlotRating('${sid}', ${n})">★</button>`
      )).join('');

      return (
        `<tr data-dash-slot="${esc(sid)}">` +
        `<td><div class="flex items-center gap-1.5"><strong class="font-mono">${esc(sid)}</strong>${renderOrientedEdgeBadge(sp.origine, sp.voisin)}</div></td>` +
        `<td><div class="x3-dash-src-pills">${srcPills}</div></td>` +
        `<td><div class="font-semibold text-slate-900">${esc(title)}</div><div class="flex gap-1 mt-0.5">${roleTags.join('')}</div></td>` +
        `<td><select class="x3-select text-xs" onchange="AmazoniaExplorerV63.setSlotStatus('${sid}', this.value)">${statusOptions}</select></td>` +
        `<td><div class="flex items-center gap-1"><div class="x3-stars">${stars}</div><button type="button" class="x3-fav-btn ${w.favorite ? 'is-on' : ''}" onclick="AmazoniaExplorerV63.toggleSlotFavorite('${sid}')">${w.favorite ? '♥' : '♡'}</button></div></td>` +
        `<td><input type="text" class="x3-comment-input" style="min-width:10rem" value="${esc(w.comment || '')}" placeholder="Note…" oninput="AmazoniaExplorerV63.setSlotCommentLive('${sid}', this.value)" /></td>` +
        `<td><div class="flex items-center gap-1">` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openDuelForSlot('${sid}')" title="Duel P1/P2/P3">⚔️</button>` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.jumpToSlot('${sid}')" title="Ouvrir la fiche">👁️</button>` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${sid}', '${w.selected_source || 'panel_1'}')" title="Modifier / Hybrider">✏️</button>` +
        `</div></td>` +
        `</tr>`
      );
    }).join('');

    const pendingArbitrage = specs.filter(sp => {
      const w = ws.slots[sp.id];
      return !w.selected_source || w.status === 'HESITATION' || w.status === 'A_HYBRIDER';
    });
    const arbitrageStrip = pendingArbitrage.length > 0
      ? `<div class="p-3 rounded-xl bg-amber-50/90 border border-amber-200 space-y-2" data-arbitrage-list="true">` +
        `<div class="text-xs font-bold text-amber-950">🎯 Points restant à arbitrer (${pendingArbitrage.length}) — cliquez pour ouvrir le Duel :</div>` +
        `<div class="flex flex-wrap gap-1.5">` +
        pendingArbitrage.map(sp => {
          const w = ws.slots[sp.id];
          const badge = !w.selected_source ? 'À trancher' : (w.status === 'A_HYBRIDER' ? 'À hybrider' : 'Hésitation');
          return `<button type="button" class="x3-tile-link-chip is-downstream" onclick="AmazoniaExplorerV63.openDuelForSlot('${esc(sp.id)}')"><strong>${esc(sp.id)}</strong> (${esc(sp.alias_oriente)}) · ${esc(badge)}</button>`;
        }).join('') +
        `</div></div>`
      : `<div class="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs font-semibold text-emerald-900">✅ Tous les 30 emplacements sont arbitrés ! Vous pouvez exporter votre Canon candidat vers Antigravity.</div>`;

    return (
      `<div class="x3-dash-card" data-view="dashboard">` +
      `<div class="flex flex-wrap items-center justify-between gap-3">` +
      `<div><h2 class="font-serif text-xl font-bold text-slate-900">📋 Tableau de bord Atelier — Mon Canon v6.3 (${radar.electedCount}/30 élues)</h2>` +
      `<p class="text-xs text-slate-500">Pilotez vos 30 emplacements, vos hybridations et vos arbitrages restants. Tout est sauvegardé automatiquement dans votre navigateur.</p></div>` +
      `<div class="flex flex-wrap items-center gap-1.5">` +
      `<span class="text-xs text-slate-500">Pré-remplir les non tranchés :</span>` +
      PANEL_IDS.map(pid => `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.fillUnelectedFrom('${pid}')">Depuis ${PANEL_SHORT[pid]}</button>`).join('') +
      `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.openExportModal('antigravity')">💾 Exporter / Importer</button>` +
      `</div>` +
      `</div>` +
      `${arbitrageStrip}` +
      `<div class="flex flex-wrap items-center gap-1.5">${dashFilters}</div>` +
      `<div class="x3-dash-table-wrap">` +
      `<table class="x3-dash-table">` +
      `<thead><tr><th>Emplacement</th><th>Source élue</th><th>Tuile &amp; Rôles</th><th>Statut</th><th>Note</th><th>Commentaire d’auteur</th><th>Actions</th></tr></thead>` +
      `<tbody>${rowsHtml || '<tr><td colspan="7" class="text-center py-6 text-slate-400">Aucun emplacement dans ce filtre.</td></tr>'}</tbody>` +
      `</table>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // MODALE 1 — Guide des 32 Pictogrammes
  // --------------------------------------------------------------------------
  function renderPictoGuideModal() {
    if (!uiState.pictoGuideOpen) return '';
    const ref = getPictosRef();
    const byCat = {};
    Object.values(ref).forEach(entry => {
      const cat = entry.categorie || 'ACTION';
      if (!byCat[cat]) byCat[cat] = [];
      byCat[cat].push(entry);
    });

    const catsHtml = PICTO_CATEGORIES.map(cat => {
      const items = byCat[cat.id] || [];
      if (items.length === 0) return '';
      return (
        `<div class="space-y-2">` +
        `<div class="x3-section-label">${esc(cat.label)} (${items.length})</div>` +
        `<div class="x3-picto-cat-grid">` +
        items.map(it => (
          `<button type="button" class="x3-picto-guide-card" onclick="AmazoniaExplorerV63.setPictoFilter('${esc(it.code)}')">` +
          `<span class="x3-picto-guide-sym">${esc(it.symbole)}</span>` +
          `<span class="text-xs font-semibold text-slate-800">${esc(it.libelle)}</span>` +
          `</button>`
        )).join('') +
        `</div>` +
        `</div>`
      );
    }).join('');

    return (
      `<div class="x3-modal-backdrop" id="x3-picto-guide-modal" role="dialog" aria-modal="true" aria-label="Guide des 32 pictogrammes" onclick="if(event.target===this) AmazoniaExplorerV63.closePictoGuide()">` +
      `<div class="x3-modal-panel">` +
      `<div class="x3-modal-head">` +
      `<h3 class="x3-modal-title">📖 Guide visuel des ${Object.keys(ref).length} pictogrammes officiels (Mini-Tuiles Plateau)</h3>` +
      `<button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closePictoGuide()">✕ Fermer</button>` +
      `</div>` +
      `<div class="x3-modal-body">` +
      `<p class="text-xs text-slate-600">Cliquez sur n’importe quel pictogramme pour filtrer l’Explorateur sur les tuiles qui l’affichent sur leur Mini-Tuile Plateau.</p>` +
      `${catsHtml}` +
      `</div>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // MODALE 2 — Tiroir d'Édition & d'Hybridation à la demande
  // --------------------------------------------------------------------------
  function renderEditorModal() {
    if (!uiState.editor) return '';
    const ed = uiState.editor;
    const t = ed.tile;
    const tp = t.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const cj = t.carte_joueur || {};
    const tr = cj.texte_regle || {};
    const dr = cj.decision_et_renoncement || {};
    const isGardien = t.famille === 'GARDIEN';
    const isA0 = A0_SLOTS.has(ed.slotId);
    const wsSlot = uiState.workspace.slots[ed.slotId];
    const refPictos = getPictosRef();
    const selPictos = Array.isArray(tp.pictogrammes) ? tp.pictogrammes : [];
    const roles = Array.isArray(t.roles_portes) ? t.roles_portes : [];

    const pictoPicker = Object.values(refPictos).map(it => {
      const on = selPictos.includes(it.code);
      return (
        `<button type="button" class="x3-picto-pick-btn ${on ? 'is-selected' : ''}" ` +
        `title="${esc(it.libelle)}" onclick="AmazoniaExplorerV63.toggleEditorPicto('${esc(it.code)}')">` +
        `${esc(it.symbole)} <span class="text-[11px]">${esc(it.libelle.split('(')[0].trim())}</span></button>`
      );
    }).join('');

    const iconSelect = isGardien
      ? `<div class="x3-field"><label>Icône Gardien conseillée</label>` +
        `<select onchange="AmazoniaExplorerV63.updateEditorField('tuile_plateau.icone_conseillee', this.value)">` +
        GUARDIAN_ICONS.map(ic => `<option value="${ic.id}" ${tp.icone_conseillee === ic.id ? 'selected' : ''}>${ic.icon} ${esc(ic.label)}</option>`).join('') +
        `</select></div>`
      : '';

    const hybridRow = (label, section) => (
      `<div class="flex flex-wrap items-center gap-1 text-xs">` +
      `<span class="font-semibold text-slate-600">${esc(label)} :</span>` +
      PANEL_IDS.map(pid => (
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.importEditorFromPanel('${pid}', '${section}')">${PANEL_SHORT[pid]}</button>`
      )).join('') +
      `</div>`
    );

    return (
      `<div class="x3-modal-backdrop" id="x3-editor-modal" role="dialog" aria-modal="true" aria-label="Éditer et hybrider ${esc(ed.slotId)}" onclick="if(event.target===this) AmazoniaExplorerV63.closeEditor()">` +
      `<div class="x3-modal-panel" style="width:min(1220px, 100%)">` +
      `<div class="x3-modal-head">` +
      `<h3 class="x3-modal-title">✏️ Atelier d’Édition &amp; Hybridation — ${esc(ed.slotId)} (${esc(t.alias_oriente)})</h3>` +
      `<button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closeEditor()">✕ Fermer</button>` +
      `</div>` +
      `<div class="x3-modal-body">` +
      `<div class="p-3 rounded-xl bg-amber-50 border border-amber-200 flex flex-wrap items-center gap-3">` +
      `<span class="text-xs font-bold text-amber-900">🧬 Raccourcis d’hybridation 1-clic :</span>` +
      `${hybridRow('Tout charger', 'all')}` +
      `${hybridRow('Face 1', 'face_1')}` +
      (isGardien ? hybridRow('Face 2', 'face_2') : '') +
      `${hybridRow('Enraciné', 'enracine')}` +
      `${hybridRow('Pitch', 'pitch')}` +
      `${hybridRow('Dilemme', 'dilemma')}` +
      `</div>` +
      `<div class="x3-editor-layout">` +
      `<div class="space-y-3">` +
      `<div class="x3-form-section">` +
      `<div class="x3-section-label">1. Identité, Nature &amp; Rôles</div>` +
      `<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">` +
      `<div class="x3-field"><label>Nom court Mini-Tuile ${isGardien ? '🔒 (Animal verrouillé)' : ''}</label>` +
      `<input type="text" value="${esc(tp.nom_court || '')}" ${isGardien ? 'disabled' : ''} oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.nom_court', this.value)" /></div>` +
      `<div class="x3-field"><label>Titre complet Grande Carte</label>` +
      `<input type="text" value="${esc(cj.titre_complet || '')}" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.titre_complet', this.value)" /></div>` +
      `</div>` +
      `<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">` +
      `<div class="x3-field"><label>Nature</label>` +
      `<select onchange="AmazoniaExplorerV63.updateEditorField('nature', this.value)">` +
      `<option value="ACTION" ${t.nature !== 'LOI_PASSIVE' ? 'selected' : ''}>✦ Action</option>` +
      `<option value="LOI_PASSIVE" ${t.nature === 'LOI_PASSIVE' ? 'selected' : ''}>⚖️ Loi passive permanente</option>` +
      `</select></div>` +
      `${iconSelect}` +
      `</div>` +
      `<div class="flex flex-wrap gap-3 text-xs pt-1">` +
      `<label class="inline-flex items-center gap-1.5 font-semibold"><input type="checkbox" ${t.est_twist ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('TWIST_2K3', this.checked)" /> ⚡ Twist 2K3</label>` +
      (isGardien ? `<label class="inline-flex items-center gap-1.5 font-semibold"><input type="checkbox" ${roles.includes('CATALYSEUR_EVEIL') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('CATALYSEUR_EVEIL', this.checked)" /> ☀️ Catalyseur d’Éveil</label>` : '') +
      `<label class="inline-flex items-center gap-1.5 font-semibold"><input type="checkbox" ${roles.includes('LEVIER_REVE') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('LEVIER_REVE', this.checked)" /> 🌙 Levier de Rêve</label>` +
      `<label class="inline-flex items-center gap-1.5 font-semibold"><input type="checkbox" ${roles.includes('ENRACINEMENT') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('ENRACINEMENT', this.checked)" /> 🌱 Synergie d’Enracinement</label>` +
      (isA0 ? `<span class="text-sky-800 font-semibold">🔓 Autonomie A=0 (verrouillée)</span>` : '') +
      `</div>` +
      `</div>` +
      `<div class="x3-form-section">` +
      `<div class="x3-section-label">2. Mini-Tuile Plateau (2 à 4 pictos · zéro phrase)</div>` +
      `<div class="text-[11px] text-slate-600">Pictogrammes sélectionnés (${selPictos.length}/4) :</div>` +
      `<div class="x3-picto-picker">${pictoPicker}</div>` +
      `<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">` +
      `<div class="x3-field"><label>Mots-clés Face 1</label><input type="text" value="${esc(mcp.face_1 || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.face_1', this.value)" /></div>` +
      (isGardien ? `<div class="x3-field"><label>Mots-clés Face 2</label><input type="text" value="${esc(mcp.face_2 || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.face_2', this.value)" /></div>` : '') +
      `<div class="x3-field"><label>Mots-clés Enraciné (optionnel)</label><input type="text" value="${esc(mcp.enracine || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.enracine', this.value)" /></div>` +
      `<div class="x3-field"><label>Résumé plateau</label><input type="text" value="${esc(tp.resume_plateau || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.resume_plateau', this.value)" /></div>` +
      `</div>` +
      `</div>` +
      `<div class="x3-form-section">` +
      `<div class="x3-section-label">3. Grande Carte Joueur &amp; Dilemme</div>` +
      `<div class="x3-field"><label>Pitch d’ambiance</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.pitch_ambiance', this.value)">${esc(cj.pitch_ambiance || '')}</textarea></div>` +
      `<div class="x3-field"><label>Texte Face 1</label><textarea rows="4" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.face_1', this.value)">${esc(tr.face_1 || '')}</textarea></div>` +
      (isGardien ? `<div class="x3-field"><label>Texte Face 2 (autonome)</label><textarea rows="4" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.face_2', this.value)">${esc(tr.face_2 || '')}</textarea></div>` : '') +
      `<div class="x3-field"><label>Clause Enraciné dédiée (laisser vide = ancrage standard)</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.enracine', this.value)">${esc(tr.enracine || '')}</textarea></div>` +
      `<div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">` +
      `<div class="x3-field"><label>🎯 Pourquoi la jouer (Choix)</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.decision_et_renoncement.choix', this.value)">${esc(dr.choix || '')}</textarea></div>` +
      `<div class="x3-field"><label>⚖️ Ce qu’elle coûte (Renoncement)</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.decision_et_renoncement.renoncement', this.value)">${esc(dr.renoncement || '')}</textarea></div>` +
      `</div>` +
      `</div>` +
      `</div>` +
      `<div class="space-y-3" id="x3-editor-live-preview">` +
      `<div class="x3-section-label">👁️ Prévisualisation en direct</div>` +
      `${renderMiniTuile(t, true)}` +
      `${renderGrandeCarte(t)}` +
      `</div>` +
      `</div>` +
      `</div>` +
      `<div class="x3-modal-foot">` +
      `<div class="flex items-center gap-2">` +
      (wsSlot && wsSlot.is_modified ? `<button type="button" class="x3-btn x3-btn-danger" onclick="AmazoniaExplorerV63.restoreOriginalSlot('${esc(ed.slotId)}')">↺ Restaurer l’original</button>` : '') +
      `</div>` +
      `<div class="flex items-center gap-2">` +
      `<button type="button" class="x3-btn" onclick="AmazoniaExplorerV63.closeEditor()">Annuler</button>` +
      `<button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.saveEditorToCanon()">💾 Enregistrer &amp; Élire dans Mon Canon</button>` +
      `</div>` +
      `</div>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // MODALE 3 — Passerelles d'Export Gemini & Antigravity + Import Workspace
  // --------------------------------------------------------------------------
  function renderExportModal() {
    if (!uiState.exportModal) return '';
    const em = uiState.exportModal;
    const radar = computeHealthRadar('canon');
    const geminiBrief = buildGeminiMarkdownBrief(em.geminiScope || 'to_arbitrate');
    const comfortBadge = geminiBrief.comfort === 'green'
      ? 'is-ok'
      : (geminiBrief.comfort === 'amber' ? 'is-warn' : 'is-err');

    const scopes = [
      { id: 'to_arbitrate', label: '🤔 Hésitation & À hybrider' },
      { id: 'active_context', label: uiState.view === 'simulator' ? '🎡 Table active' : '🔍 Lisière / Filtre actif' },
      { id: 'notes_and_edits', label: '✏️ Mes notes & textes modifiés' },
      { id: 'canon_summary', label: '📋 Synthèse légère Mon Canon' }
    ].map(sc => (
      `<button type="button" class="x3-btn x3-btn-sm ${em.geminiScope === sc.id ? 'x3-btn-primary' : ''}" ` +
      `onclick="AmazoniaExplorerV63.setExportGeminiScope('${sc.id}')">${esc(sc.label)}</button>`
    )).join('');

    const hasSeed = Boolean(getInitialWorkspaceSeed());

    return (
      `<div class="x3-modal-backdrop" id="x3-export-modal" role="dialog" aria-modal="true" aria-label="Passerelles Gemini et Antigravity" onclick="if(event.target===this) AmazoniaExplorerV63.closeExportModal()">` +
      `<div class="x3-modal-panel">` +
      `<div class="x3-modal-head">` +
      `<h3 class="x3-modal-title">📤 Passerelles d’Export « Zéro Saturation » &amp; Sauvegarde Atelier</h3>` +
      `<button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closeExportModal()">✕ Fermer</button>` +
      `</div>` +
      `<div class="x3-modal-body">` +
      `<div class="x3-subview-switch" style="width:fit-content">` +
      `<button type="button" class="x3-subview-btn ${em.tab === 'gemini' ? 'is-active' : ''}" onclick="AmazoniaExplorerV63.setExportTab('gemini')">✨ Vers Gemini (Brief Markdown ciblé)</button>` +
      `<button type="button" class="x3-subview-btn ${em.tab === 'antigravity' ? 'is-active' : ''}" onclick="AmazoniaExplorerV63.setExportTab('antigravity')">🚀 Vers Antigravity &amp; Sauvegarde JSON</button>` +
      `</div>` +
      (em.tab === 'gemini'
        ? `<div class="space-y-3">` +
          `<div class="flex flex-wrap items-center justify-between gap-2">` +
          `<div class="flex flex-wrap gap-1.5">${scopes}</div>` +
          `<span class="x3-radar-pill ${comfortBadge}" data-gemini-word-count="${geminiBrief.words}">~${geminiBrief.words} mots · ${geminiBrief.tileCount} tuile(s)</span>` +
          `</div>` +
          `<pre class="x3-export-preview" id="x3-gemini-md-preview">${esc(geminiBrief.markdown)}</pre>` +
          `<div class="flex items-center justify-between gap-2 flex-wrap">` +
          `<span class="text-xs text-slate-500">Markdown propre sans bruit technique, calibré pour un échange fluide dans Gemini web.</span>` +
          `<button type="button" id="x3-btn-copy-md" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.copyGeminiBrief()">📋 Copier le Brief Markdown (~${geminiBrief.words} mots)</button>` +
          `</div>` +
          `</div>`
        : `<div class="space-y-4">` +
          `<div class="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">` +
          `<div class="x3-section-label">1. Sauvegarde complète de l’Atelier (prête pour contracts/panels/author_workspace_v6_3.json)</div>` +
          `<p class="text-xs text-slate-600">Contient votre sélection par emplacement (${radar.electedCount}/30), toutes vos surcharges hybrides au format v6.3.1, vos statuts, notes et commentaires d’auteur.</p>` +
          `<div class="flex flex-wrap gap-2">` +
          `<button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.downloadWorkspaceJson()">💾 Télécharger author_workspace_v6_3.json</button>` +
          `<input type="file" id="x3-workspace-import-input" accept=".json,application/json" class="hidden" onchange="AmazoniaExplorerV63.handleWorkspaceImport(event)" />` +
          `<button type="button" class="x3-btn" onclick="document.getElementById('x3-workspace-import-input').click()">📂 Importer author_workspace_v6_3.json</button>` +
          (hasSeed ? `<button type="button" class="x3-btn" onclick="AmazoniaExplorerV63.reloadSeedWorkspace()">↺ Recharger l’état du dépôt</button>` : '') +
          `</div>` +
          `</div>` +
          `<div class="p-4 rounded-xl bg-emerald-50 border border-emerald-200 space-y-2.5">` +
          `<div class="x3-section-label">2. Exporter un contrat candidat tiles_canon_v6_3.json (Étape 3)</div>` +
          `<p class="text-xs text-emerald-950">Génère un catalogue 30 tuiles conforme au schéma v6.3.1 (avec <code>referentiel_pictogrammes</code>, <code>casting_gardiens_verrouille</code> et <code>carte_des_roles</code> recalculée).</p>` +
          (radar.electedCount < 30
            ? `<div class="flex flex-wrap items-center gap-2 text-xs text-amber-900 bg-amber-50 border border-amber-200 rounded-lg px-3 py-2">` +
              `<span>⚠️ ${30 - radar.electedCount} emplacement(s) non encore élu(s) — compléter les manquants depuis :</span>` +
              `<select class="x3-select" onchange="AmazoniaExplorerV63.setExportFallbackPanel(this.value)">` +
              PANEL_IDS.map(pid => `<option value="${pid}" ${em.fallbackPanel === pid ? 'selected' : ''}>${PANEL_LABELS[pid]}</option>`).join('') +
              `</select></div>`
            : `<div class="text-xs text-emerald-800 font-semibold">✅ 30/30 emplacements élus — export 100 % issu de Mon Canon v6.3.</div>`) +
          `<button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.downloadCandidateCanonJson()">🏆 Exporter tiles_canon_v6_3.json candidat</button>` +
          `</div>` +
          `</div>`) +
      `</div>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // Rendu Principal & Gestion de l'Intégration dans docs/index.html
  // --------------------------------------------------------------------------
  function render() {
    ensureInitialized();
    const toolbarEl = document.getElementById('explorer-v6-3-toolbar') || document.getElementById('explorer-v6-2-toolbar');
    const gridEl = document.getElementById('catalogue-grid');
    if (!toolbarEl || !gridEl) return;

    // Masquer les éléments hérités v6.2 pour un espace de travail épuré
    const legacyFilters = document.getElementById('legacy-catalogue-filters');
    if (legacyFilters && legacyFilters.classList) legacyFilters.classList.add('hidden');
    const v62Banner = document.getElementById('v62-catalogue-banner');
    if (v62Banner && v62Banner.classList) v62Banner.classList.add('hidden');
    const oldToolbar = document.getElementById('explorer-v6-2-toolbar');
    if (oldToolbar && oldToolbar !== toolbarEl && oldToolbar.classList) oldToolbar.classList.add('hidden');

    let bodyHtml = '';
    if (uiState.view === 'simulator') {
      bodyHtml = renderSimulatorView();
    } else if (uiState.view === 'dashboard') {
      bodyHtml = renderDashboardView();
    } else {
      bodyHtml = uiState.explorerSubView === 'duel' ? renderDuelView() : renderExplorerCardsView();
    }

    const modalsHtml = renderPictoGuideModal() + renderEditorModal() + renderExportModal();

    toolbarEl.innerHTML = `<div class="x3-shell">${renderTopBarAndRadar()}</div>`;
    gridEl.innerHTML = `<div class="x3-shell">${bodyHtml}</div>${modalsHtml}`;
  }

  // --------------------------------------------------------------------------
  // Actions Interactives (API publique window.AmazoniaExplorerV63)
  // --------------------------------------------------------------------------
  function copyTextRobust(text) {
    if (typeof navigator !== 'undefined' && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        const p = navigator.clipboard.writeText(text);
        if (p && typeof p.catch === 'function') {
          p.catch(() => fallbackCopySync(text));
        }
        return true;
      } catch (_err) {
        return fallbackCopySync(text);
      }
    }
    return fallbackCopySync(text);
  }

  function fallbackCopySync(text) {
    if (typeof document === 'undefined' || typeof document.createElement !== 'function') return false;
    const ta = document.createElement('textarea');
    ta.value = text;
    if (ta.style) { ta.style.position = 'fixed'; ta.style.top = '-9999px'; }
    if (document.body && document.body.appendChild) document.body.appendChild(ta);
    if (ta.select) ta.select();
    let ok = false;
    try {
      if (typeof document.execCommand === 'function') ok = document.execCommand('copy');
    } catch (_err) {
      ok = false;
    }
    if (document.body && document.body.removeChild) document.body.removeChild(ta);
    return ok;
  }

  function downloadJsonFile(filename, payloadObj) {
    const jsonText = JSON.stringify(payloadObj, null, 2) + '\n';
    if (typeof Blob === 'undefined' || typeof URL === 'undefined' || typeof URL.createObjectURL !== 'function') {
      return jsonText;
    }
    const blob = new Blob([jsonText], { type: 'application/json;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    if (document.body && document.body.appendChild) document.body.appendChild(a);
    a.click();
    if (document.body && document.body.removeChild) document.body.removeChild(a);
    if (typeof URL.revokeObjectURL === 'function') URL.revokeObjectURL(url);
    return jsonText;
  }

  function renderEditorMiniTuileHint(tile) {
    const tp = tile.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const hasPunct = [mcp.face_1, mcp.face_2, mcp.enracine, tp.resume_plateau].some(
      s => typeof s === 'string' && /[.!?]/.test(s)
    );
    if (!hasPunct) return '';
    return '<div class="p-2 rounded-lg bg-amber-50 border border-amber-200 text-[11px] text-amber-900">💡 <strong>Astuce Mini-Tuile :</strong> évitez la ponctuation de phrase (<code>. ! ?</code>) sur les mots-clés plateau (utilisez <code>·</code> ou <code>→</code>).</div>';
  }

  function updateEditorPreviewOnly() {
    if (!uiState.editor) return;
    const prev = document.getElementById('x3-editor-live-preview');
    if (prev) {
      prev.innerHTML =
        `<div class="x3-section-label">👁️ Prévisualisation en direct</div>` +
        `${renderEditorMiniTuileHint(uiState.editor.tile)}` +
        `${renderMiniTuile(uiState.editor.tile, true)}` +
        `${renderGrandeCarte(uiState.editor.tile)}`;
    }
  }

  const api = {
    VERSION,
    render,
    getState: () => uiState,
    getWorkspace: () => { ensureInitialized(); return uiState.workspace; },
    enumerateAll197Assises,
    canonicalizeAssise,
    computeHealthRadar,
    analyzeTableSimulation,
    computeResourceIndex,
    computeTileLinks,
    buildGeminiMarkdownBrief,
    buildAuthorWorkspaceExport,
    buildCandidateCanonV63,
    getFilteredSlotIds,

    setSource(src) {
      ensureInitialized();
      uiState.source = src;
      if (src === 'canon') uiState.radarTarget = 'canon';
      render();
    },

    toggleRadarTarget() {
      ensureInitialized();
      uiState.radarTarget = uiState.radarTarget === 'canon' ? 'active_source' : 'canon';
      render();
    },

    toggleRadarDetail(key) {
      ensureInitialized();
      uiState.radarDetailKey = (uiState.radarDetailKey === key || !key) ? null : key;
      render();
    },

    applyRadarFilter(filterKind, value) {
      ensureInitialized();
      uiState.view = 'explorer';
      uiState.explorerSubView = 'cards';
      uiState.selectedBorder = 'ALL';
      uiState.filters = { search: '', peuple: 'ALL', family: 'ALL', role: 'ALL', draft: 'ALL', picto: null };
      uiState.filters[filterKind] = value;
      uiState.radarDetailKey = null;
      render();
    },

    setView(v) {
      ensureInitialized();
      uiState.view = v;
      render();
    },

    setExplorerSubView(sv) {
      ensureInitialized();
      uiState.view = 'explorer';
      uiState.explorerSubView = sv;
      render();
    },

    selectBorder(bk) {
      ensureInitialized();
      uiState.selectedBorder = bk;
      render();
    },

    setFilter(key, value) {
      ensureInitialized();
      uiState.filters[key] = value;
      render();
      if (key === 'search') {
        const inp = document.getElementById('x3-search-input');
        if (inp && typeof inp.focus === 'function') {
          inp.focus();
          if (typeof inp.setSelectionRange === 'function') {
            const len = String(value || '').length;
            inp.setSelectionRange(len, len);
          }
        }
      }
    },

    setPictoFilter(picCode) {
      ensureInitialized();
      uiState.filters.picto = picCode || null;
      uiState.pictoGuideOpen = false;
      uiState.view = 'explorer';
      uiState.explorerSubView = 'cards';
      render();
    },

    resetFilters() {
      ensureInitialized();
      uiState.selectedBorder = 'ALL';
      uiState.filters = { search: '', peuple: 'ALL', family: 'ALL', role: 'ALL', draft: 'ALL', picto: null };
      uiState.resourceFilterOnly = false;
      render();
    },

    focusResource(tok) {
      ensureInitialized();
      if (uiState.resourceFocus === tok) {
        uiState.resourceFocus = null;
        uiState.resourceFilterOnly = false;
      } else {
        uiState.resourceFocus = tok;
      }
      render();
    },

    toggleResourceFilterOnly() {
      ensureInitialized();
      uiState.resourceFilterOnly = !uiState.resourceFilterOnly;
      render();
    },

    clearResourceFocus() {
      ensureInitialized();
      uiState.resourceFocus = null;
      uiState.resourceFilterOnly = false;
      render();
    },

    jumpToSlot(slotId) {
      ensureInitialized();
      const sp = getSlotSpecMap()[slotId];
      if (!sp) return;
      uiState.view = 'explorer';
      uiState.explorerSubView = 'cards';
      uiState.selectedBorder = borderKey(sp.origine, sp.voisin);
      uiState.filters = { search: '', peuple: 'ALL', family: 'ALL', role: 'ALL', draft: 'ALL', picto: null };
      uiState.resourceFilterOnly = false;
      render();
      if (typeof document !== 'undefined' && typeof document.querySelector === 'function') {
        const el = document.querySelector(`[data-slot-id="${slotId}"]`);
        if (el && typeof el.scrollIntoView === 'function') {
          el.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    },

    openDuelForSlot(slotId) {
      ensureInitialized();
      uiState.view = 'explorer';
      uiState.explorerSubView = 'duel';
      uiState.duelSlotId = slotId;
      render();
    },

    setDuelSlot(slotId) {
      ensureInitialized();
      uiState.duelSlotId = slotId;
      render();
    },

    // Simulateur de table
    setSimPreset(presetKey) {
      ensureInitialized();
      const pr = PRESET_TABLES.find(p => p.key === presetKey);
      if (!pr) return;
      uiState.simPeuples = pr.peuples.slice();
      uiState.simHighlightPeuple = null;
      render();
    },

    toggleSimPeuple(code) {
      ensureInitialized();
      const idx = uiState.simPeuples.indexOf(code);
      if (idx >= 0) {
        if (uiState.simPeuples.length <= 3) return;
        uiState.simPeuples.splice(idx, 1);
      } else {
        uiState.simPeuples.push(code);
      }
      uiState.simHighlightPeuple = null;
      render();
    },

    moveSimPeuple(code, delta) {
      ensureInitialized();
      const idx = uiState.simPeuples.indexOf(code);
      const next = idx + delta;
      if (idx < 0 || next < 0 || next >= uiState.simPeuples.length) return;
      const tmp = uiState.simPeuples[next];
      uiState.simPeuples[next] = code;
      uiState.simPeuples[idx] = tmp;
      render();
    },

    toggleSimHighlight(code) {
      ensureInitialized();
      uiState.simHighlightPeuple = uiState.simHighlightPeuple === code ? null : code;
      render();
    },

    // Tableau de bord
    setDashFilter(df) {
      ensureInitialized();
      uiState.dashFilter = df;
      render();
    },

    fillUnelectedFrom(panelId) {
      ensureInitialized();
      if (!PANEL_IDS.includes(panelId)) return;
      getSlotsSpec().forEach(sp => {
        const w = uiState.workspace.slots[sp.id];
        if (!w.selected_source) {
          w.selected_source = panelId;
          w.base_source = panelId;
          w.updated_at = new Date().toISOString();
        }
      });
      saveWorkspaceToStorage();
      render();
    },

    // Annotations Draft
    electSlot(slotId, sourceKey) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      if (sourceKey === 'custom' && !w.custom_tile) return;
      w.selected_source = (w.selected_source === sourceKey && uiState.view !== 'dashboard') ? null : sourceKey;
      if (PANEL_IDS.includes(sourceKey)) w.base_source = sourceKey;
      if (w.selected_source && !w.status) w.status = 'RETENUE';
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    clearSlotElection(slotId) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.selected_source = null;
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    setSlotStatus(slotId, statusVal) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.status = statusVal;
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    setSlotRating(slotId, stars) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.rating = w.rating === stars ? 0 : stars;
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    toggleSlotFavorite(slotId) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.favorite = !w.favorite;
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    // Sauvegarde instantanée au fil de la frappe SANS détruire le focus du champ
    setSlotCommentLive(slotId, text) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.comment = String(text || '');
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      const hint = document.getElementById(`x3-saved-${slotId}`);
      if (hint && hint.classList) {
        hint.classList.add('is-visible');
        clearTimeout(hint._timer);
        hint._timer = setTimeout(() => hint.classList.remove('is-visible'), 1400);
      }
    },

    // Guide 32 Pictogrammes
    openPictoGuide() {
      ensureInitialized();
      uiState.pictoGuideOpen = true;
      render();
    },

    closePictoGuide() {
      ensureInitialized();
      uiState.pictoGuideOpen = false;
      render();
    },

    // Éditeur & Hybrideur
    openEditor(slotId, sourceHint) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      let baseTile = null;
      let baseSource = PANEL_IDS.includes(sourceHint) ? sourceHint : (w.base_source || 'panel_1');
      if (sourceHint === 'custom' && w.custom_tile) {
        baseTile = deepClone(w.custom_tile);
      } else if (PANEL_IDS.includes(sourceHint)) {
        baseTile = deepClone(getPanelTile(sourceHint, slotId));
      } else if (w.is_modified && w.custom_tile) {
        baseTile = deepClone(w.custom_tile);
      } else {
        baseTile = deepClone(getPanelTile(baseSource, slotId));
      }
      if (!baseTile) return;
      uiState.editor = { slotId, baseSource, tile: baseTile };
      render();
    },

    closeEditor() {
      ensureInitialized();
      uiState.editor = null;
      render();
    },

    importEditorFromPanel(panelId, section) {
      ensureInitialized();
      if (!uiState.editor) return;
      const srcTile = getPanelTile(panelId, uiState.editor.slotId);
      if (!srcTile) return;
      const t = uiState.editor.tile;
      if (section === 'all') {
        uiState.editor.tile = deepClone(srcTile);
        uiState.editor.baseSource = panelId;
      } else if (section === 'face_1') {
        t.carte_joueur.texte_regle.face_1 = srcTile.carte_joueur.texte_regle.face_1;
        t.tuile_plateau.mots_cles_plateau.face_1 = srcTile.tuile_plateau.mots_cles_plateau.face_1;
      } else if (section === 'face_2') {
        t.carte_joueur.texte_regle.face_2 = srcTile.carte_joueur.texte_regle.face_2;
        t.tuile_plateau.mots_cles_plateau.face_2 = srcTile.tuile_plateau.mots_cles_plateau.face_2;
      } else if (section === 'enracine') {
        t.carte_joueur.texte_regle.enracine = srcTile.carte_joueur.texte_regle.enracine;
        t.tuile_plateau.mots_cles_plateau.enracine = srcTile.tuile_plateau.mots_cles_plateau.enracine;
        const hasEnr = Boolean(t.carte_joueur.texte_regle.enracine && String(t.carte_joueur.texte_regle.enracine).trim());
        const r = new Set(t.roles_portes || []);
        if (hasEnr) r.add('ENRACINEMENT');
        t.roles_portes = Array.from(r);
      } else if (section === 'pitch') {
        t.carte_joueur.titre_complet = srcTile.carte_joueur.titre_complet;
        t.carte_joueur.entite_illustree = srcTile.carte_joueur.entite_illustree;
        t.carte_joueur.pitch_ambiance = srcTile.carte_joueur.pitch_ambiance;
        t.carte_joueur.brief_illustration = srcTile.carte_joueur.brief_illustration;
      } else if (section === 'dilemma') {
        t.carte_joueur.decision_et_renoncement = deepClone(srcTile.carte_joueur.decision_et_renoncement);
      }
      render();
    },

    updateEditorField(path, val) {
      ensureInitialized();
      if (!uiState.editor) return;
      const parts = String(path).split('.');
      let cur = uiState.editor.tile;
      for (let i = 0; i < parts.length - 1; i++) {
        if (!cur[parts[i]] || typeof cur[parts[i]] !== 'object') cur[parts[i]] = {};
        cur = cur[parts[i]];
      }
      const last = parts[parts.length - 1];
      if (last === 'enracine') {
        cur[last] = String(val || '').trim() ? val : null;
      } else {
        cur[last] = val;
      }
      if (path === 'nature') {
        const roles = new Set(uiState.editor.tile.roles_portes || []);
        if (val === 'LOI_PASSIVE') roles.add('LOI_PASSIVE');
        else roles.delete('LOI_PASSIVE');
        uiState.editor.tile.roles_portes = Array.from(roles);
      }
      updateEditorPreviewOnly();
    },

    toggleEditorRole(roleCode, checked) {
      ensureInitialized();
      if (!uiState.editor) return;
      const t = uiState.editor.tile;
      const roles = new Set(t.roles_portes || []);
      if (checked) roles.add(roleCode);
      else roles.delete(roleCode);
      if (roleCode === 'TWIST_2K3') t.est_twist = Boolean(checked);
      t.roles_portes = Array.from(roles);
      updateEditorPreviewOnly();
    },

    toggleEditorPicto(picCode) {
      ensureInitialized();
      if (!uiState.editor) return;
      const tp = uiState.editor.tile.tuile_plateau;
      const list = Array.isArray(tp.pictogrammes) ? tp.pictogrammes.slice() : [];
      const idx = list.indexOf(picCode);
      if (idx >= 0) {
        list.splice(idx, 1);
      } else {
        if (list.length >= 4) list.shift();
        list.push(picCode);
      }
      tp.pictogrammes = list;
      render();
    },

    saveEditorToCanon() {
      ensureInitialized();
      if (!uiState.editor) return;
      const { slotId, baseSource, tile } = uiState.editor;
      const sp = getSlotSpecMap()[slotId];
      const cleaned = sanitizeTileForCanonExport(tile, sp);
      const w = uiState.workspace.slots[slotId];
      w.custom_tile = cleaned;
      w.is_modified = true;
      w.selected_source = 'custom';
      w.base_source = baseSource;
      if (!w.status) w.status = 'RETENUE';
      w.updated_at = new Date().toISOString();
      uiState.editor = null;
      saveWorkspaceToStorage();
      render();
    },

    restoreOriginalSlot(slotId) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.custom_tile = null;
      w.is_modified = false;
      if (w.selected_source === 'custom') {
        w.selected_source = w.base_source || 'panel_1';
      }
      w.updated_at = new Date().toISOString();
      uiState.editor = null;
      saveWorkspaceToStorage();
      render();
    },

    // Exports & Imports
    openExportModal(tab) {
      ensureInitialized();
      uiState.exportModal = {
        tab: tab === 'antigravity' ? 'antigravity' : 'gemini',
        geminiScope: 'to_arbitrate',
        fallbackPanel: 'panel_1'
      };
      render();
    },

    closeExportModal() {
      ensureInitialized();
      uiState.exportModal = null;
      render();
    },

    setExportTab(tab) {
      ensureInitialized();
      if (!uiState.exportModal) return;
      uiState.exportModal.tab = tab;
      render();
    },

    setExportGeminiScope(scope) {
      ensureInitialized();
      if (!uiState.exportModal) return;
      uiState.exportModal.geminiScope = scope;
      render();
    },

    setExportFallbackPanel(pid) {
      ensureInitialized();
      if (!uiState.exportModal) return;
      uiState.exportModal.fallbackPanel = pid;
      render();
    },

    copyGeminiBrief() {
      ensureInitialized();
      const scope = (uiState.exportModal && uiState.exportModal.geminiScope) || 'to_arbitrate';
      const brief = buildGeminiMarkdownBrief(scope);
      copyTextRobust(brief.markdown);
      const btn = document.getElementById('x3-btn-copy-md');
      if (btn) {
        btn.textContent = `✅ Brief copié (~${brief.words} mots)`;
        setTimeout(() => {
          btn.textContent = `📋 Copier le Brief Markdown (~${brief.words} mots)`;
        }, 2000);
      }
      return brief;
    },

    downloadWorkspaceJson() {
      const obj = buildAuthorWorkspaceExport();
      return downloadJsonFile('author_workspace_v6_3.json', obj);
    },

    downloadCandidateCanonJson() {
      const fb = (uiState.exportModal && uiState.exportModal.fallbackPanel) || 'panel_1';
      const obj = buildCandidateCanonV63(fb);
      return downloadJsonFile('tiles_canon_v6_3.json', obj);
    },

    importWorkspaceObject(rawObj) {
      ensureInitialized();
      uiState.workspace = normalizeWorkspace(rawObj);
      saveWorkspaceToStorage();
      render();
      return uiState.workspace;
    },

    handleWorkspaceImport(event) {
      const file = event && event.target && event.target.files ? event.target.files[0] : null;
      if (!file) return;
      const reader = new FileReader();
      reader.onload = function (e) {
        try {
          const parsed = JSON.parse(String(e.target.result || ''));
          api.importWorkspaceObject(parsed);
          if (typeof global.showToast === 'function') {
            global.showToast('Atelier importé', `Le fichier ${file.name} a bien été chargé dans Mon Canon v6.3.`);
          }
        } catch (err) {
          if (typeof global.showToast === 'function') {
            global.showToast('Import invalide', `Impossible de lire ${file.name} : ${err.message}`);
          }
        } finally {
          event.target.value = '';
        }
      };
      reader.readAsText(file, 'utf-8');
    },

    reloadSeedWorkspace() {
      const seed = getInitialWorkspaceSeed();
      if (!seed) return;
      api.importWorkspaceObject(seed);
    },

    // Compatibilité douce avec le bouton global "Copier contexte Gemini" de docs/index.html
    getFilteredSelection() {
      ensureInitialized();
      const visibleIds = getFilteredSlotIds();
      const tilesMap = getActiveTilesMap(uiState.source);
      const selected = {};
      visibleIds.forEach(sid => {
        if (tilesMap[sid]) selected[sid] = tilesMap[sid];
      });
      return {
        isUnfiltered: visibleIds.length === 30 && uiState.source === 'archive_v6_2',
        profileCount: Object.keys(selected).length,
        selected
      };
    }
  };

  global.AmazoniaExplorerV63 = api;
})(typeof window !== 'undefined' ? window : globalThis);
