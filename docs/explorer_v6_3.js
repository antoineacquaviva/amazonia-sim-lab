/* ============================================================================
 * Amazonia Doc Studio — Atelier d'Arbitrage Bi-Composant (v6.3.2)
 * Recentré : Duel P1|P2|P3 par défaut, trio Garder/À revoir/Note, tiroirs à la demande.
 * 100 % vanilla JS (compatible file://, GitHub Pages & Node vm).
 * ============================================================================ */
(function (global) {
  'use strict';

  const VERSION = '6.3.2';
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
    custom: 'Hyb'
  };

  const A0_SLOTS = new Set(['R1', 'R2', 'R6', 'R10', 'M4', 'M5']);
  const ANIMAL_ANIMAL_BORDERS = [['M', 'R'], ['M', 'O'], ['R', 'O']];
  const E_NON_H_BORDERS = [['E', 'M'], ['E', 'R'], ['E', 'O'], ['E', 'I']];
  const ALL_15_BORDERS = [
    ['M', 'R'], ['M', 'O'], ['R', 'O'],
    ['M', 'H'], ['M', 'E'], ['M', 'I'],
    ['R', 'H'], ['R', 'E'], ['R', 'I'],
    ['O', 'H'], ['O', 'E'], ['O', 'I'],
    ['H', 'E'], ['H', 'I'], ['E', 'I']
  ];

  const GUARDIAN_ICONS = [
    { id: 'ICONE_PARADE', label: 'Parade', icon: '🛡️', desc: 'Parade classique par Défenseurs seuls' },
    { id: 'ICONE_PIEGEAGE', label: 'Piégeage', icon: '🪤', desc: 'Frappe arrêtée par un Piège autonome ou le Croc' },
    { id: 'ICONE_SABOTAGE', label: 'Sabotage', icon: '💥', desc: 'Jeton Sabotage ou Écaille révélé à l’ouverture' },
    { id: 'ICONE_REVE', label: 'Rêve', icon: '🌙', desc: 'Rêve défendu annulant au moins une machine' },
    { id: 'ICONE_INSECTE', label: 'Insecte', icon: '🐜', desc: 'Déviation ±1 ou Parade avec Insectes (si I joue)' },
    { id: 'ICONE_RESONANCE', label: 'Résonance', icon: '🔔', desc: '6e icône : 1res activations des autres Gardiens' }
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

  const ACCESSORIES_3_3 = {
    H: {
      code: 'H', tierLabel: 'Actif dès le Tour 1', title: 'Tambour & Chant', icon: '🥁',
      summary: 'Tambour posable sur tout rayon dès le 1er temps ; Chant glisse un Rêve d’1 rang à gauche s’il vide son rang.',
      states: ['TAMBOUR', 'CHANT', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION'],
      icons: ['ICONE_PARADE', 'ICONE_REVE']
    },
    M: {
      code: 'M', tierLabel: 'Actif dès le Tour 1', title: 'Jeton Duel (Défi ↔ Territoire tenu)', icon: '⚔️',
      summary: 'Posé avec un Défenseur M ; parer sur sa parcelle le retourne sur Territoire tenu (bloque l’avancée +1).',
      states: ['DUEL', 'TERRITOIRE', 'GARDIEN'],
      icons: ['ICONE_PARADE']
    },
    O: {
      code: 'O', tierLabel: 'Actif dès le Tour 1', title: 'Dé d’Envol · Perchoir · Plume de Vigie', icon: '🪶',
      summary: 'Servi dernier au sac (garde 1, pose 1 au Perchoir) ; choix min(D1,D2) ou Dé d’Envol ; Plume Chaud/Calme.',
      states: ['DE_ENVOL', 'PERCHOIR', 'PLUME', 'RANG_MACHINE', 'GARDIEN'],
      icons: []
    },
    E: {
      code: 'E', tierLabel: 'Progressif via tuiles', title: 'Jetons d’Altération', icon: '🌀',
      summary: 'Posés sur machine mobile (max 1) : compte dans m(r) puis recule d’1 parcelle sans frapper.',
      states: ['ALTERATION', 'ALTEREE', 'POSITION_REVE', 'RANG_REVE', 'ANNULATION'],
      icons: ['ICONE_REVE']
    },
    R: {
      code: 'R', tierLabel: 'Progressif via tuiles', title: '4 Écailles · Croc · Cales', icon: '🦷',
      summary: 'Écaille allume Sabotage et pose le Croc réutilisable (pare en premier) ; max 1 cale/machine mobile.',
      states: ['ECAILLE', 'CROC', 'CALE', 'SABOTAGE', 'GARDIEN'],
      icons: ['ICONE_SABOTAGE', 'ICONE_PIEGEAGE']
    },
    I: {
      code: 'I', tierLabel: 'Progressif via tuiles', title: 'Essaim · Nids · Déviation ±1 · Bouclier', icon: '🐜',
      summary: 'Production des Nids (+1/+2), Migration, Déviation ±1, Parade Insecte et Bouclier de lisière.',
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

  const PRESET_TABLES = [
    { key: 'N3-HEI', peuples: ['H', 'E', 'I'], label: '{H, E, I}', tag: 'A=0' },
    { key: 'N3-ERO', peuples: ['E', 'R', 'O'], label: '{E, R, O}', tag: 'E sans H' },
    { key: 'N3-ERI', peuples: ['E', 'R', 'I'], label: '{E, R, I}', tag: 'E sans H + I' },
    { key: 'N3-MRO', peuples: ['M', 'R', 'O'], label: '{M, R, O}', tag: '100 % Gardiens' },
    { key: 'N3-MIR', peuples: ['M', 'I', 'R'], label: '{M, I, R}', tag: 'Triade M–I–R' },
    { key: 'N4-HEMR', peuples: ['H', 'E', 'M', 'R'], label: '{H, E, M, R}', tag: '4J mixte' },
    { key: 'N6-HEMROI', peuples: ['H', 'E', 'M', 'R', 'O', 'I'], label: 'Table à 6', tag: '12 tuiles' }
  ];

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
    ICONE_PARADE: { icon: '🛡️', label: 'Icône Parade', kind: 'icon' },
    ICONE_PIEGEAGE: { icon: '🪤', label: 'Icône Piégeage', kind: 'icon' },
    ICONE_SABOTAGE: { icon: '💥', label: 'Icône Sabotage', kind: 'icon' },
    ICONE_REVE: { icon: '🌙', label: 'Icône Rêve', kind: 'icon' },
    ICONE_INSECTE: { icon: '🐜', label: 'Icône Insecte', kind: 'icon' },
    ICONE_RESONANCE: { icon: '🔔', label: 'Icône Résonance', kind: 'icon' }
  };

  const QUICK_RESOURCES = [
    'BLEU', 'ALTERATION', 'CROC', 'DUEL', 'PLUME', 'INSECTE',
    'PIEGE', 'SABOTAGE', 'SOUCHE', 'ICONE_PIEGEAGE', 'ICONE_SABOTAGE', 'ICONE_RESONANCE'
  ];

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
  // Utilitaires & Accès aux données compilées
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

  function getPanelsData() {
    if (typeof PANELS_V6_3 !== 'undefined' && PANELS_V6_3) return PANELS_V6_3;
    return global.PANELS_V6_3 || {};
  }

  function getPictosRef() {
    if (typeof REFERENTIEL_PICTOGRAMMES_V6_3 !== 'undefined' && REFERENTIEL_PICTOGRAMMES_V6_3) {
      return REFERENTIEL_PICTOGRAMMES_V6_3;
    }
    return global.REFERENTIEL_PICTOGRAMMES_V6_3 || {};
  }

  function getCastingRef() {
    if (typeof CASTING_GARDIENS_V6_3 !== 'undefined' && CASTING_GARDIENS_V6_3) {
      return CASTING_GARDIENS_V6_3;
    }
    return global.CASTING_GARDIENS_V6_3 || {};
  }

  function getSlotsSpec() {
    if (typeof SLOTS_SPEC_V6_3 !== 'undefined' && Array.isArray(SLOTS_SPEC_V6_3)) {
      return SLOTS_SPEC_V6_3;
    }
    return Array.isArray(global.SLOTS_SPEC_V6_3) ? global.SLOTS_SPEC_V6_3 : [];
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
    return global.AUTHOR_WORKSPACE_INITIAL_V6_3 || null;
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
    return PEUPLE_ORDER.indexOf(a) <= PEUPLE_ORDER.indexOf(b) ? `${a}-${b}` : `${b}-${a}`;
  }

  function borderLabel(a, b) {
    return PEUPLE_ORDER.indexOf(a) <= PEUPLE_ORDER.indexOf(b) ? `${a} ↔ ${b}` : `${b} ↔ ${a}`;
  }

  const BORDER_TO_SLOTS = {};
  const TWIN_BY_SLOT = {};
  function ensureBorderMaps() {
    if (Object.keys(TWIN_BY_SLOT).length > 0) return;
    getSlotsSpec().forEach(s => {
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
  // Modèle exact des 197 Assises Canoniques
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
        candidates.push(seq.slice(shift).concat(seq.slice(0, shift)));
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
        if (idx === rest.length) { out.push([first].concat(rest)); return; }
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
            seen.set(c.key, { n: c.n, peuples: c.peuples, key: c.key, tileIds });
          }
        });
      });
    });

    _CACHED_197_ASSISES = Array.from(seen.values());
    return _CACHED_197_ASSISES;
  }

  // --------------------------------------------------------------------------
  // Archive v6.2 (lecture seule)
  // --------------------------------------------------------------------------
  let _ARCHIVE_V62_CACHE = null;
  function getArchiveV62Map() {
    if (_ARCHIVE_V62_CACHE) return _ARCHIVE_V62_CACHE;
    const out = {};
    const cat = typeof CATALOGUE_TUILES !== 'undefined' ? CATALOGUE_TUILES : global.CATALOGUE_TUILES;
    if (!cat) { _ARCHIVE_V62_CACHE = out; return out; }
    const specMap = getSlotSpecMap();
    Object.keys(specMap).forEach(sid => {
      const slot = cat[sid];
      const sp = specMap[sid];
      if (!slot || !slot.profils || !slot.profils.A) return;
      const p = slot.profils.A;
      const parts = String(p.texte || '').split(/<br\s*\/?>/i).map(x => x.replace(/<[^>]+>/g, '').trim()).filter(Boolean);
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
      const tags = (p.tags || []).map(t => String(t).toUpperCase());
      const roles = [];
      if (tags.includes('CATALYSEUR_EVEIL')) roles.push('CATALYSEUR_EVEIL');
      if (tags.includes('LEVIER_REVE')) roles.push('LEVIER_REVE');
      if (tags.includes('ENRACINEMENT') || enr) roles.push('ENRACINEMENT');
      const isLoi = String(p.nature || '').toLowerCase() === 'loi_passive';
      if (isLoi) roles.push('LOI_PASSIVE');
      const isTwist = Boolean(p.est_twist_canon0);
      if (isTwist) roles.push('TWIST_2K3');
      if (A0_SLOTS.has(sid)) roles.push('AUTONOMIE_A0');

      const dr = p.decision_joueur || {};
      out[sid] = {
        id: sid,
        alias_oriente: sp.alias_oriente,
        famille: sp.famille,
        origine: sp.origine,
        voisin: sp.voisin,
        couple: [sp.origine, sp.voisin],
        roles_portes: roles,
        est_twist: isTwist,
        entrees_plancher: (p.entrees || []).map(x => String(x).toUpperCase()),
        entrees_synergie: [],
        entrees: (p.entrees || []).map(x => String(x).toUpperCase()),
        sorties: (p.sorties || []).map(x => String(x).toUpperCase()),
        nature: isLoi ? 'LOI_PASSIVE' : 'ACTION',
        declencheurs_amorces: (p.declencheurs_amorces || []).map(x => String(x).toUpperCase()).filter(x => GUARDIAN_ICON_BY_ID[x]),
        double_ouverture: p.double_ouverture || null,
        tuile_plateau: {
          nom_court: slot.nomBase || p.nom || sid,
          fenetre_badge: p.fenetre || 'ACTIVATION',
          icone_conseillee: p.cablage_recommande || null,
          pictogrammes: [],
          mots_cles_plateau: { face_1: 'Archive v6.2 (lecture seule)', face_2: null, enracine: enr ? 'Clause Enraciné dédiée' : null },
          resume_plateau: p.animal_ou_theme || ''
        },
        carte_joueur: {
          titre_complet: p.nom || slot.nomBase || sid,
          entite_illustree: p.animal_ou_theme || slot.nomBase || sid,
          brief_illustration: '',
          pitch_ambiance: '',
          texte_regle: { face_1: f1, face_2: f2, enracine: enr },
          decision_et_renoncement: { choix: dr.choix || '', renoncement: dr.renoncement || '' }
        },
        temoins: p.temoin ? [{ id: `${sid}_T1`, resume: p.temoin }] : [],
        _isArchiveV62: true
      };
    });
    _ARCHIVE_V62_CACHE = out;
    return out;
  }

  // --------------------------------------------------------------------------
  // Workspace persistant (localStorage + import/export author_workspace_v6_3.json)
  // --------------------------------------------------------------------------
  function isSlotFlaggedReview(wsSlot) {
    return Boolean(wsSlot && (wsSlot.status === 'HESITATION' || wsSlot.status === 'A_HYBRIDER'));
  }

  function createEmptyWorkspace() {
    const slots = {};
    getSlotsSpec().forEach(sp => {
      slots[sp.id] = {
        slot_id: sp.id,
        alias_oriente: sp.alias_oriente,
        selected_source: null,
        base_source: 'panel_1',
        is_modified: false,
        status: '',
        comment: '',
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
      dst.comment = typeof src.comment === 'string' ? src.comment : '';
      dst.updated_at = typeof src.updated_at === 'string' ? src.updated_at : null;
      if (src.custom_tile && typeof src.custom_tile === 'object') {
        dst.custom_tile = deepClone(src.custom_tile);
      }
    });
    return base;
  }

  function loadInitialWorkspace() {
    try {
      if (typeof localStorage !== 'undefined' && localStorage && typeof localStorage.getItem === 'function') {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (stored) return normalizeWorkspace(JSON.parse(stored));
      }
    } catch (_err) {
      // ignore
    }
    const seed = getInitialWorkspaceSeed();
    if (seed && typeof seed === 'object') return normalizeWorkspace(seed);
    return createEmptyWorkspace();
  }

  function saveWorkspaceToStorage() {
    uiState.workspace.updated_at = new Date().toISOString();
    try {
      if (typeof localStorage !== 'undefined' && localStorage && typeof localStorage.setItem === 'function') {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(uiState.workspace));
      }
    } catch (_err) {
      // ignore
    }
  }

  // --------------------------------------------------------------------------
  // État réactif (centré sur le Duel P1|P2|P3 par défaut)
  // --------------------------------------------------------------------------
  const uiState = {
    initialized: false,
    mode: 'arbitrate', // 'arbitrate' | 'list' | 'simulator'
    currentSlotId: 'G1',
    listSource: 'canon', // 'canon' | 'panel_1' | 'panel_2' | 'panel_3' | 'archive_v6_2'
    simSource: 'canon', // 'canon' | 'panel_1' | 'panel_2' | 'panel_3'
    activeDrawer: null, // null | 'health' | 'index30' | 'browse'
    indexFilter: 'ALL', // 'ALL' | 'UNELECTED' | 'REVIEW' | 'MODIFIED'
    radarDetailKey: null,
    radarTarget: 'canon', // 'canon' | 'panel_1' | 'panel_2' | 'panel_3'
    filters: {
      search: '',
      peuple: 'ALL',
      family: 'ALL',
      role: 'ALL',
      reviewOnly: false,
      picto: null
    },
    resourceFocus: null,
    resourceFocusSource: null,
    simPeuples: ['M', 'R', 'O', 'H'],
    simHighlightPeuple: null,
    pictoGuideOpen: false,
    editor: null,
    exportModal: null,
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
        if (uiState.editor) { uiState.editor = null; render(); return; }
        if (uiState.exportModal) { uiState.exportModal = null; render(); return; }
        if (uiState.pictoGuideOpen) { uiState.pictoGuideOpen = false; render(); return; }
        if (uiState.resourceFocus) { uiState.resourceFocus = null; render(); return; }
        if (uiState.activeDrawer) { uiState.activeDrawer = null; render(); return; }
      }
      if (isTyping || uiState.editor || uiState.exportModal || uiState.pictoGuideOpen) return;
      if (uiState.mode === 'arbitrate') {
        if (ev.key === 'ArrowRight') api.stepSlot(1);
        else if (ev.key === 'ArrowLeft') api.stepSlot(-1);
      }
    });
  }

  // --------------------------------------------------------------------------
  // Résolution des Tuiles
  // --------------------------------------------------------------------------
  function getPanelTile(panelId, slotId) {
    const p = getPanelsData()[panelId];
    return p && p.tuiles_ciblees ? p.tuiles_ciblees[slotId] || null : null;
  }

  function getCanonSlotResolved(slotId, fallbackPanelId) {
    ensureInitialized();
    const w = uiState.workspace.slots[slotId];
    if (w) {
      if (w.selected_source === 'custom' && w.custom_tile) {
        return { tile: w.custom_tile, sourceKey: 'custom', baseSource: w.base_source || 'panel_1', elected: true, modified: true };
      }
      if (w.selected_source && PANEL_IDS.includes(w.selected_source)) {
        const t = getPanelTile(w.selected_source, slotId);
        if (t) return { tile: t, sourceKey: w.selected_source, baseSource: w.selected_source, elected: true, modified: false };
      }
    }
    if (fallbackPanelId) {
      return { tile: getPanelTile(fallbackPanelId, slotId), sourceKey: fallbackPanelId, baseSource: fallbackPanelId, elected: false, modified: false };
    }
    return { tile: null, sourceKey: null, baseSource: null, elected: false, modified: false };
  }

  function getTilesMapForSource(src) {
    ensureInitialized();
    if (src === 'archive_v6_2') return getArchiveV62Map();
    if (src === 'canon') {
      const out = {};
      getSlotsSpec().forEach(sp => {
        const res = getCanonSlotResolved(sp.id, null);
        if (res.tile) out[sp.id] = res.tile;
      });
      return out;
    }
    const p = getPanelsData()[src];
    return (p && p.tuiles_ciblees) ? p.tuiles_ciblees : {};
  }

  function getEffectiveTile(slotId, src) {
    if (src === 'canon') return getCanonSlotResolved(slotId, null);
    if (src === 'archive_v6_2') {
      return { tile: getArchiveV62Map()[slotId] || null, sourceKey: 'archive_v6_2', elected: false, modified: false };
    }
    const w = uiState.workspace.slots[slotId];
    return {
      tile: getPanelTile(src, slotId),
      sourceKey: src,
      elected: Boolean(w && w.selected_source === src),
      modified: false
    };
  }

  // --------------------------------------------------------------------------
  // Moteur Synergique & Radar 197 Assises
  // --------------------------------------------------------------------------
  function normalizeStateList(arr) {
    return Array.from(new Set((arr || []).map(x => String(x || '').trim().toUpperCase()).filter(Boolean)));
  }

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

  function computeSynergyCoverage64(slotId, stateToken, tilesMap) {
    const tok = String(stateToken || '').toUpperCase();
    const assises = enumerateAll197Assises();
    let covered = 0;
    let total = 0;
    assises.forEach(a => {
      if (!a.tileIds.includes(slotId)) return;
      total++;
      const avail = new Set(SOCLE_STATES);
      a.peuples.forEach(p => (PEUPLE_NATIVE_STATES[p] || []).forEach(st => avail.add(st)));
      a.tileIds.forEach(otherId => {
        const ot = tilesMap[otherId];
        if (ot) expandOutputStates(ot.sorties).forEach(st => avail.add(st));
      });
      if (avail.has(tok) || (tok === 'ALTEREE' && avail.has('ALTERATION')) || (tok === 'ALTERATION' && avail.has('ALTEREE'))) {
        covered++;
      }
    });
    return { covered, total: total || 64 };
  }

  function computeTileLinks(slotId, tilesMap) {
    const tile = tilesMap[slotId];
    if (!tile) return { upstreamTiles: [], downstreamTiles: [], synergyCoverage: {} };
    const floorIn = normalizeStateList(tile.entrees_plancher);
    const synIn = normalizeStateList(tile.entrees_synergie);
    const allIn = Array.from(new Set(floorIn.concat(synIn)));
    const myOut = expandOutputStates(tile.sorties);
    const myLit = new Set(normalizeStateList(tile.declencheurs_amorces));
    const myRecIcon = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee
      ? String(tile.tuile_plateau.icone_conseillee).toUpperCase()
      : null;

    const upMap = new Map();
    const downMap = new Map();

    Object.entries(tilesMap).forEach(([otherId, other]) => {
      if (otherId === slotId || !other) return;
      const otherOut = expandOutputStates(other.sorties);
      const otherIn = new Set(normalizeStateList(other.entrees_plancher).concat(normalizeStateList(other.entrees_synergie)));
      const otherLit = new Set(normalizeStateList(other.declencheurs_amorces));
      const otherRecIcon = other.tuile_plateau && other.tuile_plateau.icone_conseillee
        ? String(other.tuile_plateau.icone_conseillee).toUpperCase()
        : null;

      const upReasons = allIn.filter(st => otherOut.has(st));
      if (myRecIcon && otherLit.has(myRecIcon)) upReasons.push(myRecIcon);
      if (upReasons.length > 0) {
        upMap.set(otherId, {
          id: otherId,
          nom: (other.tuile_plateau && other.tuile_plateau.nom_court) || otherId,
          isTwin: TWIN_BY_SLOT[slotId] === otherId,
          reasons: Array.from(new Set(upReasons))
        });
      }

      const downReasons = Array.from(otherIn).filter(st => myOut.has(st));
      if (otherRecIcon && myLit.has(otherRecIcon)) downReasons.push(otherRecIcon);
      if (downReasons.length > 0) {
        downMap.set(otherId, {
          id: otherId,
          nom: (other.tuile_plateau && other.tuile_plateau.nom_court) || otherId,
          isTwin: TWIN_BY_SLOT[slotId] === otherId,
          reasons: Array.from(new Set(downReasons))
        });
      }
    });

    const synergyCoverage = {};
    synIn.forEach(st => { synergyCoverage[st] = computeSynergyCoverage64(slotId, st, tilesMap); });
    const sortLinks = arr => arr.sort((a, b) => (b.isTwin ? 1 : 0) - (a.isTwin ? 1 : 0) || a.id.localeCompare(b.id));
    return {
      upstreamTiles: sortLinks(Array.from(upMap.values())),
      downstreamTiles: sortLinks(Array.from(downMap.values())),
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
      nativeProducers.push({ code: 'SOCLE', label: 'Socle commun v6.2', icon: '🌿' });
    }
    Object.values(ACCESSORIES_3_3).forEach(acc => {
      const hit = isIcon ? acc.icons.includes(key) : acc.states.some(s => matchSet.has(s));
      if (hit) nativeProducers.push({ code: acc.code, label: `${PEUPLE_META[acc.code].short} — ${acc.title}`, icon: acc.icon });
    });

    const producers = [];
    const consumersFloor = [];
    const consumersSynergy = [];
    const consumersIcon = [];

    Object.entries(tilesMap).forEach(([sid, tile]) => {
      if (!tile) return;
      const item = { id: sid, nom: (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid, alias: tile.alias_oriente };
      if (isIcon) {
        if (normalizeStateList(tile.declencheurs_amorces).includes(key)) producers.push(item);
        const rec = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee ? String(tile.tuile_plateau.icone_conseillee).toUpperCase() : '';
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

    const allInvolvedIds = new Set(producers.concat(consumersFloor, consumersSynergy, consumersIcon).map(x => x.id));
    return { key, isIcon, meta, nativeProducers, producers, consumersFloor, consumersSynergy, consumersIcon, allInvolvedIds };
  }

  function find2K3Triangles(twistTiles) {
    const edgeByDir = {};
    twistTiles.forEach(t => { edgeByDir[`${t.origine}>${t.voisin}`] = t; });
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
          if (edgeByDir[`${b}>${c}`] && edgeByDir[`${c}>${a}`] && i === Math.min(i, j, k)) {
            triangles.push({ nodes: [a, b, c], arcs: [edgeByDir[`${a}>${b}`], edgeByDir[`${b}>${c}`], edgeByDir[`${c}>${a}`]] });
          }
        }
      }
    }
    for (let x = 0; x < triangles.length; x++) {
      for (let y = x + 1; y < triangles.length; y++) {
        if (new Set(triangles[x].nodes.concat(triangles[y].nodes)).size === 6) {
          return [triangles[x], triangles[y]];
        }
      }
    }
    return null;
  }

  function computeHealthRadar(targetSource) {
    ensureInitialized();
    const src = targetSource || uiState.radarTarget || 'canon';
    const tilesMap = getTilesMapForSource(src);
    const specs = getSlotsSpec();
    const assises = enumerateAll197Assises();

    const presentIds = specs.map(s => s.id).filter(id => Boolean(tilesMap[id]));
    const unelectedIds = specs.map(s => s.id).filter(id => !tilesMap[id]);
    const electedCount = presentIds.length;
    const isComplete = electedCount === 30;

    // Twists 2K3
    const twistTiles = presentIds.map(id => tilesMap[id]).filter(t => Boolean(t.est_twist));
    const twistByOrig = Object.fromEntries(PEUPLE_ORDER.map(p => [p, []]));
    const twistByEdge = {};
    twistTiles.forEach(t => {
      if (twistByOrig[t.origine]) twistByOrig[t.origine].push(t.id);
      const bk = borderKey(t.origine, t.voisin);
      if (!twistByEdge[bk]) twistByEdge[bk] = [];
      twistByEdge[bk].push(t.id);
    });
    const missingOrigins = PEUPLE_ORDER.filter(p => twistByOrig[p].length === 0);
    const doubleBorders = Object.entries(twistByEdge).filter(([, ids]) => ids.length > 1);
    const triangles2K3 = find2K3Triangles(twistTiles);
    let twistsStatus = 'ok';
    if (doubleBorders.length > 0) twistsStatus = 'err';
    else if (twistTiles.length < 6 || missingOrigins.length > 0) twistsStatus = isComplete ? 'err' : 'warn';
    else if (!triangles2K3) twistsStatus = 'warn';

    // Lois passives
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

    // Éveil (i) + (ii)
    const catalyseurIds = presentIds.filter(id => tilesMap[id].famille === 'GARDIEN' && (tilesMap[id].roles_portes || []).includes('CATALYSEUR_EVEIL'));
    const catSet = new Set(catalyseurIds);
    const regleI = {};
    const missingAnimalsI = [];
    ['M', 'R', 'O'].forEach(an => {
      const cnt = catalyseurIds.filter(id => tilesMap[id].origine === an && NON_ANIMAL_PEUPLES.has(tilesMap[id].voisin)).length;
      regleI[an] = cnt;
      if (cnt < 2) missingAnimalsI.push(`${an} (${cnt}/2)`);
    });
    const regleII = {};
    const missingBordersII = [];
    ANIMAL_ANIMAL_BORDERS.forEach(([a1, a2]) => {
      const pair = BORDER_TO_SLOTS[borderKey(a1, a2)] || [];
      const ok = pair.some(id => catSet.has(id));
      regleII[`${a1}–${a2}`] = ok;
      if (!ok) missingBordersII.push(`${a1}–${a2}`);
    });
    const uncoveredEveil = assises.filter(a => a.peuples.some(p => ANIMAL_PEUPLES.has(p)) && !a.tileIds.some(id => catSet.has(id))).map(a => a.key);
    let eveilStatus = 'ok';
    if (catalyseurIds.length < 9 || missingAnimalsI.length > 0 || missingBordersII.length > 0 || uncoveredEveil.length > 0) {
      eveilStatus = isComplete ? 'err' : 'warn';
    }

    // Sommeil E sans H
    const levierIds = presentIds.filter(id => (tilesMap[id].roles_portes || []).includes('LEVIER_REVE'));
    const levSet = new Set(levierIds);
    const coveredEBorders = [];
    const missingEBorders = [];
    E_NON_H_BORDERS.forEach(([p1, p2]) => {
      const pair = BORDER_TO_SLOTS[borderKey(p1, p2)] || [];
      if (pair.some(id => levSet.has(id))) coveredEBorders.push(`${p1}–${p2}`);
      else missingEBorders.push(`${p1}–${p2}`);
    });
    const uncoveredSommeil = assises.filter(a => a.peuples.includes('E') && !a.peuples.includes('H') && !a.tileIds.some(id => levSet.has(id))).map(a => a.key);
    let sommeilStatus = 'ok';
    if (coveredEBorders.length < 3 || uncoveredSommeil.length > 0) sommeilStatus = isComplete ? 'err' : 'warn';

    // Enracinements
    const enracIds = presentIds.filter(id => (tilesMap[id].roles_portes || []).includes('ENRACINEMENT'));
    let enracStatus = 'ok';
    if (enracIds.length > 5) enracStatus = 'err';
    else if (enracIds.length < 3) enracStatus = isComplete ? 'err' : 'warn';

    // Autonomie A=0
    const gardienLexRe = /\b(?:gardiens?|éveil|encoches?|résonance)\b/i;
    const a0Violations = [];
    Array.from(A0_SLOTS).sort().forEach(sid => {
      const t = tilesMap[sid];
      if (!t) return;
      const texts = [
        t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.face_1,
        t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.enracine
      ].filter(Boolean);
      const hitTxt = texts.some(txt => gardienLexRe.test(txt));
      const hitTok = normalizeStateList((t.entrees || []).concat(t.sorties || [])).some(tok => tok === 'GARDIEN' || tok === 'PARI_GLISSE');
      const hitRes = normalizeStateList(t.declencheurs_amorces).includes('ICONE_RESONANCE');
      if (hitTxt || hitTok || hitRes) a0Violations.push(sid);
    });
    const a0Present = Array.from(A0_SLOTS).filter(sid => Boolean(tilesMap[sid])).length;
    const a0Status = a0Violations.length > 0 ? 'err' : (a0Present < 6 ? 'warn' : 'ok');

    // Synergies orphelines & Divergence
    const orphans = [];
    presentIds.forEach(sid => {
      normalizeStateList(tilesMap[sid].entrees_synergie).forEach(st => {
        if (computeSynergyCoverage64(sid, st, tilesMap).covered === 0) orphans.push({ slotId: sid, state: st });
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
      if (o1 && o2 && o1 === o2) divergenceIssues.push(`${borderLabel(p1, p2)} : même sortie (${humanizeToken(o1).label})`);
    });
    const synStatus = (orphans.length > 0 || divergenceIssues.length > 0) ? (isComplete ? 'err' : 'warn') : 'ok';

    const statuses = [twistsStatus, loisStatus, eveilStatus, sommeilStatus, enracStatus, a0Status, synStatus];
    const errorCount = statuses.filter(s => s === 'err').length;
    const warnCount = statuses.filter(s => s === 'warn').length;
    const overallStatus = errorCount > 0 ? 'err' : (warnCount > 0 ? 'warn' : 'ok');

    return {
      source: src,
      scopeLabel: PANEL_LABELS[src] || src,
      electedCount,
      unelectedIds,
      isComplete,
      overallStatus,
      issuesCount: errorCount + warnCount,
      twists: { status: twistsStatus, ids: twistTiles.map(t => t.id), count: twistTiles.length, missingOrigins, doubleBorders, triangles2K3 },
      lois: { status: loisStatus, ids: loiIds, count: loiIds.length, maxPerAssise: maxLoisPerAssise, offendingAssises: offendingLoiAssises },
      eveil: { status: eveilStatus, ids: catalyseurIds, count: catalyseurIds.length, regleI, missingAnimalsI, regleII, missingBordersII, uncoveredAssises: uncoveredEveil },
      sommeil: { status: sommeilStatus, ids: levierIds, count: levierIds.length, coveredEBorders, missingEBorders, uncoveredAssises: uncoveredSommeil },
      enrac: { status: enracStatus, ids: enracIds, count: enracIds.length },
      a0: { status: a0Status, presentCount: a0Present, violations: a0Violations },
      synergies: { status: synStatus, orphans, divergenceIssues }
    };
  }

  // --------------------------------------------------------------------------
  // Simulateur de Table 3 à 6 Peuples
  // --------------------------------------------------------------------------
  function analyzeTableSimulation(peuples, sourceOverride) {
    ensureInitialized();
    const circle = Array.from(peuples || []);
    const n = circle.length;
    const src = sourceOverride || uiState.simSource || 'canon';
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
        const res = getEffectiveTile(sid, src);
        tileEntries.push({
          slotId: sid,
          borderKey: bk,
          tile: res.tile,
          sourceKey: res.sourceKey,
          elected: res.elected,
          modified: res.modified
        });
      });
    }

    const activeTilesMap = {};
    tileEntries.forEach(e => { if (e.tile) activeTilesMap[e.slotId] = e.tile; });

    const prodByState = {};
    const lightersByIcon = {};
    function pushProd(map, k, item) {
      if (!map[k]) map[k] = [];
      if (!map[k].some(x => x.id === item.id)) map[k].push(item);
    }

    SOCLE_STATES.forEach(st => pushProd(prodByState, st, { type: 'native', id: 'SOCLE', label: 'Socle commun' }));
    circle.forEach(p => {
      const acc = ACCESSORIES_3_3[p];
      if (!acc) return;
      (PEUPLE_NATIVE_STATES[p] || []).forEach(st => pushProd(prodByState, st, { type: 'native', id: `ACC_${p}`, label: `${PEUPLE_META[p].short}` }));
      acc.icons.forEach(ic => pushProd(lightersByIcon, ic, { type: 'native', id: `ACC_${p}`, label: `${PEUPLE_META[p].short}` }));
    });
    Object.entries(activeTilesMap).forEach(([sid, tile]) => {
      const lbl = `${sid} · ${(tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid}`;
      expandOutputStates(tile.sorties).forEach(st => pushProd(prodByState, st, { type: 'tile', id: sid, label: lbl }));
      normalizeStateList(tile.declencheurs_amorces).forEach(ic => pushProd(lightersByIcon, ic, { type: 'tile', id: sid, label: lbl }));
    });

    const completeChains = [];
    const isolatedAmplifiers = [];
    Object.entries(activeTilesMap).forEach(([sid, tile]) => {
      const consumerLbl = `${sid} · ${(tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid}`;
      normalizeStateList(tile.entrees_synergie).forEach(st => {
        const prods = (prodByState[st] || []).filter(p => p.id !== sid);
        if (prods.length === 0) {
          isolatedAmplifiers.push({ slotId: sid, tileName: (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid, state: st, stateMeta: humanizeToken(st) });
        } else {
          const shown = prods.filter(p => p.type === 'tile');
          (shown.length > 0 ? shown : prods).slice(0, 2).forEach(pr => {
            completeChains.push({ fromId: pr.id, fromLabel: pr.label, via: st, viaMeta: humanizeToken(st), toId: sid, toLabel: consumerLbl, kind: 'synergy' });
          });
        }
      });
      const recIcon = tile.tuile_plateau && tile.tuile_plateau.icone_conseillee ? String(tile.tuile_plateau.icone_conseillee).toUpperCase() : null;
      if (recIcon) {
        (lightersByIcon[recIcon] || []).filter(p => p.type === 'tile' && p.id !== sid).slice(0, 2).forEach(pr => {
          completeChains.push({ fromId: pr.id, fromLabel: pr.label, via: recIcon, viaMeta: humanizeToken(recIcon), toId: sid, toLabel: consumerLbl, kind: 'icon' });
        });
      }
    });

    const seen = new Set();
    const uniqueChains = completeChains.filter(ch => {
      const k = `${ch.fromId}->${ch.via}->${ch.toId}`;
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });

    const present = Object.values(activeTilesMap);
    const loisCount = present.filter(t => String(t.nature || '').toUpperCase() === 'LOI_PASSIVE').length;
    const twistsCount = present.filter(t => Boolean(t.est_twist)).length;
    const eveilCount = present.filter(t => t.famille === 'GARDIEN' && (t.roles_portes || []).includes('CATALYSEUR_EVEIL')).length;
    const sommeilCount = present.filter(t => (t.roles_portes || []).includes('LEVIER_REVE')).length;
    const enracCount = present.filter(t => (t.roles_portes || []).includes('ENRACINEMENT')).length;
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
  // Exports : Gemini Markdown ciblé & Antigravity JSON déterministe
  // --------------------------------------------------------------------------
  function countWords(text) {
    const clean = String(text || '').trim();
    return clean ? clean.split(/\s+/).filter(Boolean).length : 0;
  }

  function buildGeminiMarkdownBrief(scope) {
    ensureInitialized();
    const specs = getSlotsSpec();
    const ws = uiState.workspace;
    const radar = computeHealthRadar('canon');
    const lines = [];
    let tileCount = 0;

    function formatTileBrief(sid, tile, srcLabel) {
      const w = ws.slots[sid];
      const cj = tile.carte_joueur || {};
      const tr = cj.texte_regle || {};
      const dr = cj.decision_et_renoncement || {};
      const out = [`### ${sid} (${tile.alias_oriente}) — ${cj.titre_complet || (tile.tuile_plateau && tile.tuile_plateau.nom_court) || sid} [${srcLabel}]`];
      if (w && isSlotFlaggedReview(w)) out.push('- **Marqueur** : À revoir');
      if (w && w.comment) out.push(`- **Note d’auteur** : ${w.comment}`);
      if (tr.face_1) out.push(`- **Face 1** : ${tr.face_1}`);
      if (tr.face_2) out.push(`- **Face 2** : ${tr.face_2}`);
      if (tr.enracine) out.push(`- **Enraciné** : ${tr.enracine}`);
      if (dr.choix || dr.renoncement) out.push(`- **Dilemme** : Choix — ${dr.choix || '—'} | Renoncement — ${dr.renoncement || '—'}`);
      return out.join('\n');
    }

    if (scope === 'to_arbitrate') {
      lines.push('# Brief Atelier Amazonia v6.3 — Emplacements marqués « À revoir »');
      lines.push('');
      const targets = specs.filter(sp => isSlotFlaggedReview(ws.slots[sp.id]));
      if (targets.length === 0) {
        lines.push('_Aucun emplacement n’est actuellement marqué « À revoir »._');
      } else {
        targets.forEach(sp => {
          tileCount++;
          const w = ws.slots[sp.id];
          lines.push(`## ${sp.id} (${sp.alias_oriente})`);
          if (w.comment) lines.push(`> **Note d’auteur** : ${w.comment}`);
          lines.push('');
          if (w.is_modified && w.custom_tile) {
            lines.push(formatTileBrief(sp.id, w.custom_tile, 'Version hybride/éditée'));
            lines.push('');
          }
          PANEL_IDS.forEach(pid => {
            const pt = getPanelTile(pid, sp.id);
            if (!pt) return;
            const tr = (pt.carte_joueur && pt.carte_joueur.texte_regle) || {};
            const mark = w.selected_source === pid ? ' ★ Gardée' : '';
            lines.push(`- **${PANEL_LABELS[pid]}${mark} — ${(pt.carte_joueur && pt.carte_joueur.titre_complet) || pt.tuile_plateau.nom_court}** : ${tr.face_1 || ''}${tr.face_2 ? ' // Face 2 : ' + tr.face_2 : ''}${tr.enracine ? ' // Enraciné : ' + tr.enracine : ''}`);
          });
          lines.push('');
        });
      }
    } else if (scope === 'active_context') {
      if (uiState.mode === 'simulator') {
        const sim = analyzeTableSimulation(uiState.simPeuples, uiState.simSource);
        lines.push(`# Brief Table ${sim.canonKey} (${sim.peuples.join(' – ')}) — ${PANEL_LABELS[uiState.simSource]}`);
        lines.push('');
        sim.tileEntries.forEach(e => {
          if (!e.tile) return;
          tileCount++;
          lines.push(formatTileBrief(e.slotId, e.tile, PANEL_LABELS[e.sourceKey] || 'Mon Canon'));
          lines.push('');
        });
      } else if (uiState.mode === 'arbitrate') {
        const sid = uiState.currentSlotId;
        const w = ws.slots[sid];
        lines.push(`# Brief Duel ${sid} (${getSlotSpecMap()[sid].alias_oriente})`);
        if (w && w.comment) lines.push(`> **Note d’auteur** : ${w.comment}`);
        lines.push('');
        PANEL_IDS.forEach(pid => {
          const pt = getPanelTile(pid, sid);
          if (!pt) return;
          tileCount++;
          lines.push(formatTileBrief(sid, pt, PANEL_LABELS[pid] + (w && w.selected_source === pid ? ' ★ Gardée' : '')));
          lines.push('');
        });
      } else {
        const visibleIds = getFilteredSlotIds();
        lines.push(`# Brief Liste ${PANEL_LABELS[uiState.listSource]} (${visibleIds.length} tuile(s))`);
        lines.push('');
        visibleIds.forEach(sid => {
          const res = getEffectiveTile(sid, uiState.listSource);
          if (!res.tile) return;
          tileCount++;
          lines.push(formatTileBrief(sid, res.tile, res.modified ? 'Hybride' : (PANEL_LABELS[res.sourceKey] || uiState.listSource)));
          lines.push('');
        });
      }
    } else if (scope === 'notes_and_edits') {
      lines.push('# Brief Atelier Amazonia v6.3 — Notes d’auteur & Tuiles modifiées');
      lines.push('');
      const touched = specs.filter(sp => {
        const w = ws.slots[sp.id];
        return w && (w.is_modified || (w.comment && w.comment.trim()) || isSlotFlaggedReview(w));
      });
      if (touched.length === 0) {
        lines.push('_Aucune note ni modification enregistrée pour le moment._');
      } else {
        touched.forEach(sp => {
          const w = ws.slots[sp.id];
          const res = getCanonSlotResolved(sp.id, w.base_source || 'panel_1');
          if (!res.tile) return;
          tileCount++;
          lines.push(formatTileBrief(sp.id, res.tile, w.is_modified ? 'Hybride / Édité' : (w.selected_source ? PANEL_LABELS[w.selected_source] : 'À trancher')));
          lines.push('');
        });
      }
    } else {
      lines.push(`# Synthèse Mon Canon v6.3 (${radar.electedCount}/30 emplacements gardés)`);
      lines.push('');
      lines.push(`- **Twists 2K3** : ${radar.twists.count} (${radar.twists.triangles2K3 ? '2 triangles valides' : 'géométrie en cours'})`);
      lines.push(`- **Lois passives** : ${radar.lois.count}/5 (max ${radar.lois.maxPerAssise}/assise sur 197 assises)`);
      lines.push(`- **Éveil** : ${radar.eveil.count} catalyseurs · **Sommeil E sans H** : ${radar.sommeil.coveredEBorders.length}/4 lisières · **Enracinements** : ${radar.enrac.count}`);
      lines.push('');
      lines.push('| Slot | Lisière | Choix | Titre | À revoir | Note |');
      lines.push('| --- | --- | --- | --- | --- | --- |');
      specs.forEach(sp => {
        const w = ws.slots[sp.id];
        const res = getCanonSlotResolved(sp.id, null);
        if (res.tile) tileCount++;
        const srcTxt = w.selected_source ? (PANEL_SHORT[w.selected_source] || w.selected_source) : '—';
        const title = res.tile ? ((res.tile.carte_joueur && res.tile.carte_joueur.titre_complet) || res.tile.tuile_plateau.nom_court) : '—';
        const safeCom = (w.comment || '').replace(/\|/g, '/').replace(/\n/g, ' ');
        lines.push(`| ${sp.id} | ${sp.alias_oriente} | ${srcTxt} | ${title} | ${isSlotFlaggedReview(w) ? '🤔' : '—'} | ${safeCom || '—'} |`);
      });
    }

    const markdown = lines.join('\n').trim() + '\n';
    const words = countWords(markdown);
    return {
      markdown,
      words,
      chars: markdown.length,
      tileCount,
      comfort: words <= 2500 ? 'green' : (words <= 6000 ? 'amber' : 'red')
    };
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
        comment: w.comment || '',
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
    t.cycle = spec.famille === 'GARDIEN' ? 'DOUBLE_FACE_UPGRADE' : (t.nature === 'LOI_PASSIVE' ? 'PASSIF_CONTINU' : 'SIMPLE_CONTINU');
    t.cablage = spec.famille === 'GARDIEN' ? [1, 2, 3, 4, 5, 6] : null;
    t.nature = t.nature === 'LOI_PASSIVE' ? 'LOI_PASSIVE' : 'ACTION';
    t.est_twist = Boolean(t.est_twist);

    const roles = new Set(Array.isArray(t.roles_portes) ? t.roles_portes : []);
    if (A0_SLOTS.has(spec.id)) roles.add('AUTONOMIE_A0');
    if (t.nature === 'LOI_PASSIVE') roles.add('LOI_PASSIVE'); else roles.delete('LOI_PASSIVE');
    if (t.est_twist) roles.add('TWIST_2K3'); else roles.delete('TWIST_2K3');
    if (t.carte_joueur && t.carte_joueur.texte_regle && t.carte_joueur.texte_regle.enracine && String(t.carte_joueur.texte_regle.enracine).trim()) {
      roles.add('ENRACINEMENT');
    }
    t.roles_portes = Array.from(roles);

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
    if (spec.famille === 'GARDIEN' && casting[spec.id]) t.tuile_plateau.nom_court = casting[spec.id].nom_animal;
    if (spec.famille !== 'GARDIEN') {
      t.tuile_plateau.icone_conseillee = null;
      if (t.carte_joueur && t.carte_joueur.texte_regle) t.carte_joueur.texte_regle.face_2 = null;
      if (t.tuile_plateau.mots_cles_plateau) t.tuile_plateau.mots_cles_plateau.face_2 = null;
      t.double_ouverture = null;
    }
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
      tuilesOut[sp.id] = sanitizeTileForCanonExport(res.tile, sp);
      provenance[sp.id] = res.elected ? res.sourceKey : `${fallback}_fallback`;
    });

    const rolesSummary = {
      catalyseurs_eveil: [], leviers_reve: [], synergies_enracinement: [],
      lois_passives: [], autonomie_A0: [], twists_2K3: []
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

    const tris = find2K3Triangles(specs.map(sp => tuilesOut[sp.id]).filter(t => t.est_twist));
    const carteDesRoles = { statut: 'CANDIDAT_ATELIER_V6_3_1', roles: rolesSummary };
    if (tris) {
      carteDesRoles.partition_2K3 = {
        triangle_1: tris[0].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → '),
        triangle_2: tris[1].arcs.map(a => `${a.alias_oriente} (${a.id})`).join(' → ')
      };
    }

    return {
      _meta: {
        projet: 'Amazonia : Dernier Rempart — Catalogue Canonique v6.3 (Bi-Composant Mini-Tuile + Grande Carte)',
        schema_version: '6.3.1',
        socle_verrouille: '6.2.0',
        cadrage_source: 'docs/cadrage_tuiles_v6_3.md',
        etape_active: 'ETAPE_3_SELECTION_ET_AFFINAGE',
        statut_global: 'CANDIDAT_AUTEUR_V6_3',
        genere_le: new Date().toISOString().slice(0, 10),
        slots_count: 30,
        c02_supprime: true,
        panel_id: 'canon_v6_3_candidat',
        murs_porteurs_verrouilles: [
          'M1_TEMPS_BATAILLE', 'M2_CONSERVATION_THERMIQUE',
          'M3_INTEGRITE_PLATEAU_ET_ICONES', 'M4_AUTONOMIE_PLANCHER_SOLO'
        ],
        provenance_par_emplacement: provenance
      },
      referentiel_pictogrammes: deepClone(getPictosRef()),
      casting_gardiens_verrouille: deepClone(getCastingRef()),
      carte_des_roles: carteDesRoles,
      rapport_audit_197: { verdict_global: 'A_VALIDER_PAR_AUDIT_197', c02_word_count_purged: true, assises_verifiees: 197 },
      tuiles_ciblees: tuilesOut
    };
  }

  // --------------------------------------------------------------------------
  // Filtrage (Mode Liste)
  // --------------------------------------------------------------------------
  function getFilteredSlotIds() {
    ensureInitialized();
    const specs = getSlotsSpec();
    const tilesMap = getTilesMapForSource(uiState.listSource);
    const f = uiState.filters;
    const search = String(f.search || '').toLowerCase().trim();
    const rfIdx = uiState.resourceFocus ? computeResourceIndex(uiState.resourceFocus, tilesMap) : null;

    return specs.filter(sp => {
      const sid = sp.id;
      const w = uiState.workspace.slots[sid];
      const tile = tilesMap[sid];
      if (f.peuple !== 'ALL' && sp.origine !== f.peuple && sp.voisin !== f.peuple) return false;
      if (f.family !== 'ALL' && sp.famille !== f.family) return false;
      if (f.reviewOnly && !isSlotFlaggedReview(w)) return false;
      if (rfIdx && !rfIdx.allInvolvedIds.has(sid)) return false;

      if (f.role !== 'ALL') {
        if (!tile) return false;
        if (f.role === 'TWIST_2K3' && !tile.est_twist) return false;
        else if (f.role === 'LOI_PASSIVE' && tile.nature !== 'LOI_PASSIVE') return false;
        else if (f.role !== 'TWIST_2K3' && f.role !== 'LOI_PASSIVE' && !(tile.roles_portes || []).includes(f.role)) return false;
      }

      if (f.picto) {
        if (!tile || !tile.tuile_plateau || !(tile.tuile_plateau.pictogrammes || []).includes(f.picto)) return false;
      }

      if (search) {
        const parts = [sid, sp.alias_oriente, w && w.comment];
        if (tile) {
          const tp = tile.tuile_plateau || {};
          const cj = tile.carte_joueur || {};
          const tr = cj.texte_regle || {};
          parts.push(tp.nom_court, cj.titre_complet, cj.pitch_ambiance, tr.face_1, tr.face_2, tr.enracine);
        }
        if (!parts.filter(Boolean).join(' ').toLowerCase().includes(search)) return false;
      }
      return true;
    }).map(sp => sp.id);
  }

  // --------------------------------------------------------------------------
  // Rendu — Composants partagés (Badges, Pictos, Détails repliables)
  // --------------------------------------------------------------------------
  function renderPeuplePill(code, withName) {
    const meta = PEUPLE_META[code] || { code, short: code };
    return `<span class="x3-peuple-badge x3-peuple-${esc(code)}">${getPeupleIconHtml(code, 13)}<span>${esc(withName ? meta.short : code)}</span></span>`;
  }

  function renderOrientedEdgeBadge(orig, vois) {
    return (
      `<span class="x3-edge-badge" title="${esc(PEUPLE_META[orig].nom)} vers ${esc(PEUPLE_META[vois].nom)}">` +
      `${renderPeuplePill(orig, false)}<span class="text-slate-400">›</span>${renderPeuplePill(vois, false)}</span>`
    );
  }

  function renderPictoToken(picCode) {
    const entry = getPictosRef()[picCode];
    if (!entry) return '';
    return `<span class="x3-picto-token" data-picto-symbol="true" title="${esc(entry.libelle)}" aria-label="${esc(entry.libelle)}">${esc(entry.symbole)}</span>`;
  }

  function renderRoleBadges(tile, isModified) {
    const roles = Array.isArray(tile.roles_portes) ? tile.roles_portes : [];
    const pills = [];
    if (tile.nature === 'LOI_PASSIVE') pills.push('<span class="x3-role-pill x3-role-loi" title="Modifie le cœur en continu">⚖️ Loi passive</span>');
    if (tile.est_twist) pills.push('<span class="x3-role-pill x3-role-twist" title="Tord une règle familière (géométrie 2K3)">⚡ Twist 2K3</span>');
    if (roles.includes('CATALYSEUR_EVEIL')) pills.push('<span class="x3-role-pill x3-role-eveil">☀️ Éveil</span>');
    if (roles.includes('LEVIER_REVE')) pills.push('<span class="x3-role-pill x3-role-reve">🌙 Levier Rêve</span>');
    if (roles.includes('ENRACINEMENT')) pills.push('<span class="x3-role-pill x3-role-enrac">🌱 Enracinement</span>');
    if (roles.includes('AUTONOMIE_A0')) pills.push('<span class="x3-role-pill x3-role-a0" title="Autonome sur table {H, E, I} sans Gardiens">🔓 A=0</span>');
    if (isModified) pills.push('<span class="x3-role-pill x3-role-mod">✏️ Modifié</span>');
    return pills.join('');
  }

  function renderCollapsibleDetails(tile, tilesMap, sourceHint) {
    const cj = tile.carte_joueur || {};
    const dr = cj.decision_et_renoncement || {};
    const temoins = Array.isArray(tile.temoins) ? tile.temoins : [];
    const links = computeTileLinks(tile.id, tilesMap);
    const floorIn = normalizeStateList(tile.entrees_plancher);
    const synIn = normalizeStateList(tile.entrees_synergie);
    const outs = normalizeStateList(tile.sorties);
    const litIcons = normalizeStateList(tile.declencheurs_amorces);
    const twinId = TWIN_BY_SLOT[tile.id];
    const twinTile = twinId ? tilesMap[twinId] : null;
    const srcArg = sourceHint ? `, '${esc(sourceHint)}'` : '';

    const floorChips = floorIn.map(st => `<button type="button" class="x3-res-pill is-floor" onclick="AmazoniaExplorerV63.focusResource('${esc(st)}'${srcArg})">${humanizeToken(st).icon} ${esc(humanizeToken(st).label)}</button>`).join('');
    const synChips = synIn.map(st => {
      const cov = links.synergyCoverage[st];
      return `<button type="button" class="x3-res-pill is-synergy" onclick="AmazoniaExplorerV63.focusResource('${esc(st)}'${srcArg})">${humanizeToken(st).icon} ${esc(humanizeToken(st).label)}${cov ? ` <span class="font-mono text-[10px]">${cov.covered}/${cov.total}</span>` : ''}</button>`;
    }).join('');
    const outChips = outs.map(st => `<button type="button" class="x3-res-pill is-output" onclick="AmazoniaExplorerV63.focusResource('${esc(st)}'${srcArg})">${humanizeToken(st).icon} ${esc(humanizeToken(st).label)}</button>`).concat(
      litIcons.map(ic => `<button type="button" class="x3-res-pill is-icon" onclick="AmazoniaExplorerV63.focusResource('${esc(ic)}'${srcArg})">${humanizeToken(ic).icon} ${esc(humanizeToken(ic).label)}</button>`)
    ).join('');

    const upChips = links.upstreamTiles.slice(0, 6).map(lk => `<button type="button" class="x3-tile-link-chip is-up" onclick="AmazoniaExplorerV63.goToSlot('${esc(lk.id)}')">${lk.isTwin ? '🔗 ' : ''}${esc(lk.id)} ${esc(lk.nom)}</button>`).join('');
    const downChips = links.downstreamTiles.slice(0, 6).map(lk => `<button type="button" class="x3-tile-link-chip is-down" onclick="AmazoniaExplorerV63.goToSlot('${esc(lk.id)}')">${lk.isTwin ? '🔗 ' : ''}${esc(lk.id)} ${esc(lk.nom)}</button>`).join('');

    return (
      `<details class="x3-details-fold" data-details-fold="${esc(tile.id)}">` +
      `<summary><span>▾ Dilemme, Scènes &amp; Synergies</span><span class="text-[11px] font-normal text-slate-500">${temoins.length} scène(s) · ${links.upstreamTiles.length + links.downstreamTiles.length} lien(s)</span></summary>` +
      `<div class="x3-details-body">` +
      (dr.choix || dr.renoncement
        ? `<div class="space-y-1">` +
          `<div><strong>🎯 Pourquoi la jouer :</strong> ${esc(dr.choix || '—')}</div>` +
          `<div><strong>⚖️ Ce qu’elle coûte :</strong> ${esc(dr.renoncement || '—')}</div>` +
          `</div>`
        : '') +
      (tile.famille === 'GARDIEN' && tile.double_ouverture
        ? `<div class="p-2 rounded bg-amber-50 border border-amber-200 text-amber-950 text-xs"><strong>⚡ Double activation :</strong> ${esc(tile.double_ouverture)}</div>`
        : '') +
      (temoins.length > 0
        ? `<div class="space-y-1.5"><div class="x3-section-label">🎬 Scènes témoins</div>` +
          temoins.map((tm, i) => `<div class="p-2 rounded bg-slate-50 border-l-2 border-slate-400 text-xs"><strong>Scène ${i + 1} :</strong> ${esc(tm.resume || '')}</div>`).join('') +
          `</div>`
        : '') +
      `<div class="space-y-1.5 pt-1 border-t border-slate-100">` +
      `<div class="x3-section-label">🔄 Synergies (clic sur une ressource = Producteurs ⇄ Consommateurs)</div>` +
      `<div class="flex flex-wrap gap-1 items-center"><span class="text-[11px] font-semibold text-slate-500">Plancher solo :</span>${floorChips || '<span class="text-xs text-slate-400">Autonome</span>'}</div>` +
      (synChips ? `<div class="flex flex-wrap gap-1 items-center"><span class="text-[11px] font-semibold text-slate-500">Amplificateurs :</span>${synChips}</div>` : '') +
      (outChips ? `<div class="flex flex-wrap gap-1 items-center"><span class="text-[11px] font-semibold text-slate-500">Produit :</span>${outChips}</div>` : '') +
      (upChips ? `<div class="flex flex-wrap gap-1 items-center"><span class="text-[11px] font-semibold text-emerald-700">⬅️ Alimentée par :</span>${upChips}</div>` : '') +
      (downChips ? `<div class="flex flex-wrap gap-1 items-center"><span class="text-[11px] font-semibold text-amber-800">➡️ Alimente :</span>${downChips}</div>` : '') +
      (twinId ? `<div class="text-xs text-slate-600">🔗 <strong>Jumelle (${esc(twinId)}) :</strong> ${twinTile ? esc((twinTile.tuile_plateau && twinTile.tuile_plateau.nom_court) || twinId) : 'non encore gardée'} <button type="button" class="underline font-semibold ml-1" onclick="AmazoniaExplorerV63.goToSlot('${esc(twinId)}')">Voir →</button></div>` : '') +
      `</div>` +
      (cj.brief_illustration ? `<div class="text-xs text-slate-500 pt-1 border-t border-slate-100"><strong>🎨 Brief illustration :</strong> ${esc(cj.brief_illustration)}</div>` : '') +
      `</div>` +
      `</details>`
    );
  }

  // --------------------------------------------------------------------------
  // 1. Bandeau Supérieur Unique + Tiroirs à la demande
  // --------------------------------------------------------------------------
  function renderTopBar() {
    const canonRadar = computeHealthRadar('canon');
    const healthRadar = uiState.radarTarget === 'canon' ? canonRadar : computeHealthRadar(uiState.radarTarget);
    const reviewCount = getSlotsSpec().filter(sp => isSlotFlaggedReview(uiState.workspace.slots[sp.id])).length;

    const healthLabel = canonRadar.overallStatus === 'ok'
      ? '✅ Équilibre OK'
      : (canonRadar.electedCount < 30
        ? `🩺 Santé (${canonRadar.issuesCount} point${canonRadar.issuesCount > 1 ? 's' : ''})`
        : `⚠️ ${canonRadar.issuesCount} point${canonRadar.issuesCount > 1 ? 's' : ''} à vérifier`);

    let drawerHtml = '';
    if (uiState.activeDrawer === 'health') {
      drawerHtml = renderHealthDrawer(healthRadar);
    } else if (uiState.activeDrawer === 'index30') {
      drawerHtml = renderIndex30Drawer(canonRadar, reviewCount);
    } else if (uiState.activeDrawer === 'browse') {
      drawerHtml = renderBrowseDrawer();
    }

    return (
      `<div class="x3-topbar" data-explorer-version="${VERSION}">` +
      `<div class="x3-topbar-row">` +
      `<div class="x3-mode-group" role="tablist" aria-label="Modes de l’Atelier">` +
      `<button type="button" class="x3-mode-btn ${uiState.mode === 'arbitrate' || uiState.mode === 'list' ? 'is-active' : ''}" data-mode-btn="arbitrate" onclick="AmazoniaExplorerV63.setMode('arbitrate')">⚔️ Arbitrer (30)</button>` +
      `<button type="button" class="x3-mode-btn ${uiState.mode === 'simulator' ? 'is-active' : ''}" data-mode-btn="simulator" onclick="AmazoniaExplorerV63.setMode('simulator')">🎡 Tester une Table</button>` +
      `</div>` +
      `<div class="x3-status-group">` +
      `<button type="button" class="x3-progress-pill ${uiState.activeDrawer === 'index30' ? 'is-open' : ''}" data-progress-pill="true" onclick="AmazoniaExplorerV63.toggleDrawer('index30')" title="Ouvrir l’index des 30 emplacements">` +
      `<span>★ Mon Canon : ${canonRadar.electedCount}/30</span>` +
      (reviewCount > 0 ? `<span>· 🤔 ${reviewCount}</span>` : '') +
      `</button>` +
      `<button type="button" class="x3-health-pill is-${canonRadar.overallStatus} ${uiState.activeDrawer === 'health' ? 'is-open' : ''}" data-health-pill="true" data-health-status="${canonRadar.overallStatus}" onclick="AmazoniaExplorerV63.toggleDrawer('health')" title="Déplier le bilan des invariants sur les 197 assises">${esc(healthLabel)}</button>` +
      `</div>` +
      `<div class="x3-tools-group">` +
      `<button type="button" class="x3-tool-btn ${uiState.activeDrawer === 'browse' || uiState.mode === 'list' ? 'is-active' : ''}" data-browse-btn="true" onclick="AmazoniaExplorerV63.toggleDrawer('browse')">🔍 Parcourir / Filtrer</button>` +
      `<button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.openPictoGuide()">📖 Pictos</button>` +
      `<button type="button" class="x3-tool-btn x3-tool-btn-accent" onclick="AmazoniaExplorerV63.openExportModal('gemini')">📤 Exporter</button>` +
      `</div>` +
      `</div>` +
      `${drawerHtml}` +
      `</div>`
    );
  }

  function renderHealthDrawer(radar) {
    const pills = [
      { key: 'twists', status: radar.twists.status, text: `⚡ Twists 2K3 : ${radar.twists.count}${radar.twists.triangles2K3 ? ' · 2△ OK' : ''}` },
      { key: 'lois', status: radar.lois.status, text: `⚖️ Lois : ${radar.lois.count}/5 (max ${radar.lois.maxPerAssise}/assise)` },
      { key: 'eveil', status: radar.eveil.status, text: `☀️ Éveil (i)+(ii) : ${radar.eveil.count}` },
      { key: 'sommeil', status: radar.sommeil.status, text: `🌙 Sommeil E sans H : ${radar.sommeil.coveredEBorders.length}/4` },
      { key: 'enrac', status: radar.enrac.status, text: `🌱 Enracinements : ${radar.enrac.count} (3–5)` },
      { key: 'a0', status: radar.a0.status, text: `🔓 A=0 : ${radar.a0.violations.length === 0 ? radar.a0.presentCount + '/6' : radar.a0.violations.length + ' alerte(s)'}` },
      { key: 'synergies', status: radar.synergies.status, text: `🔄 Clôture : ${radar.synergies.orphans.length + radar.synergies.divergenceIssues.length === 0 ? 'OK' : (radar.synergies.orphans.length + radar.synergies.divergenceIssues.length) + ' point(s)'}` }
    ].map(p => (
      `<button type="button" class="x3-radar-pill is-${p.status} ${uiState.radarDetailKey === p.key ? 'is-selected' : ''}" ` +
      `data-radar-pill="${p.key}" data-radar-status="${p.status}" onclick="AmazoniaExplorerV63.toggleRadarDetail('${p.key}')">${esc(p.text)}</button>`
    )).join('');

    const k = uiState.radarDetailKey || 'twists';
    let detailHtml = '';
    if (k === 'twists') {
      detailHtml = radar.twists.triangles2K3
        ? `✅ <strong>2 triangles orientés 2K3 valides :</strong> ${esc(radar.twists.triangles2K3[0].arcs.map(a => `${a.alias_oriente}(${a.id})`).join(' → '))} · ${esc(radar.twists.triangles2K3[1].arcs.map(a => `${a.alias_oriente}(${a.id})`).join(' → '))}`
        : `⚠️ Géométrie 2K3 en cours (${radar.twists.count} twists : ${esc(radar.twists.ids.join(', ') || 'aucun')}).${radar.twists.missingOrigins.length > 0 ? ' Manquent en origine : <strong>' + esc(radar.twists.missingOrigins.join(', ')) + '</strong>.' : ''}${radar.twists.doubleBorders.length > 0 ? ' ❌ Doublon sur lisière : ' + esc(radar.twists.doubleBorders.map(([b]) => b).join(', ')) + '.' : ''}`;
    } else if (k === 'lois') {
      detailHtml = `Lois passives (${radar.lois.count}/5) : ${esc(radar.lois.ids.join(', ') || 'aucune')}. ${radar.lois.offendingAssises.length > 0 ? '❌ > 2 lois sur ' + radar.lois.offendingAssises.length + ' assise(s).' : '✅ Max ' + radar.lois.maxPerAssise + ' loi(s)/assise sur les 197 assises.'}`;
    } else if (k === 'eveil') {
      detailHtml = `Catalyseurs : ${radar.eveil.count} (cible ≥ 9) · Règle (i) M=${radar.eveil.regleI.M}/2, R=${radar.eveil.regleI.R}/2, O=${radar.eveil.regleI.O}/2 · Règle (ii) ${Object.entries(radar.eveil.regleII).map(([b, ok]) => `${b} ${ok ? '✓' : '✗'}`).join(', ')}.`;
    } else if (k === 'sommeil') {
      detailHtml = `Lisières E–{M,R,O,I} couvertes : ${esc(radar.sommeil.coveredEBorders.join(', ') || 'aucune')} (${radar.sommeil.coveredEBorders.length}/4). ${radar.sommeil.uncoveredAssises.length > 0 ? '⚠️ ' + radar.sommeil.uncoveredAssises.length + '/30 assises (E sans H) sans levier.' : '✅ 30/30 assises couvertes.'}`;
    } else if (k === 'enrac') {
      detailHtml = `Synergies d’Enracinement (${radar.enrac.count}, cible 3–5) : ${esc(radar.enrac.ids.join(', ') || 'aucune')}.`;
    } else if (k === 'a0') {
      detailHtml = radar.a0.violations.length === 0 ? `✅ Autonomie A=0 intacte (${radar.a0.presentCount}/6 tuiles présentes).` : `❌ Mention Gardien sur : ${esc(radar.a0.violations.join(', '))}.`;
    } else {
      detailHtml = radar.synergies.orphans.length === 0 && radar.synergies.divergenceIssues.length === 0
        ? '✅ 0 synergie orpheline et 100 % des lisières divergent sur leur sortie principale.'
        : `${radar.synergies.orphans.map(o => `⚠️ ${esc(o.slotId)} (${esc(humanizeToken(o.state).label)}) 0/64`).join(' · ')} ${radar.synergies.divergenceIssues.map(esc).join(' · ')}`;
    }

    return (
      `<div class="x3-drawer" data-drawer="health">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<div class="flex items-center gap-2 flex-wrap">` +
      `<span class="x3-section-label">🩺 Radar sur les 197 assises — ${esc(radar.scopeLabel)} (${radar.electedCount}/30)</span>` +
      `<select class="x3-select text-xs" aria-label="Cible du Radar" onchange="AmazoniaExplorerV63.setRadarTarget(this.value)">` +
      `<option value="canon" ${uiState.radarTarget === 'canon' ? 'selected' : ''}>Mon Canon v6.3</option>` +
      `<option value="panel_1" ${uiState.radarTarget === 'panel_1' ? 'selected' : ''}>Panel 1</option>` +
      `<option value="panel_2" ${uiState.radarTarget === 'panel_2' ? 'selected' : ''}>Panel 2</option>` +
      `<option value="panel_3" ${uiState.radarTarget === 'panel_3' ? 'selected' : ''}>Panel 3</option>` +
      `</select>` +
      `</div>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.toggleDrawer(null)">✕ Fermer</button>` +
      `</div>` +
      `<div class="x3-radar-pills-row">${pills}</div>` +
      `<div class="x3-radar-detail-box"><div>${detailHtml}</div></div>` +
      `</div>`
    );
  }

  function renderIndex30Drawer(radar, reviewCount) {
    const specs = getSlotsSpec();
    const ws = uiState.workspace;
    const filtered = specs.filter(sp => {
      const w = ws.slots[sp.id];
      if (uiState.indexFilter === 'UNELECTED') return !w.selected_source;
      if (uiState.indexFilter === 'REVIEW') return isSlotFlaggedReview(w);
      if (uiState.indexFilter === 'MODIFIED') return Boolean(w.is_modified);
      return true;
    });

    const cells = filtered.map(sp => {
      const w = ws.slots[sp.id];
      const res = getCanonSlotResolved(sp.id, null);
      const nom = res.tile ? ((res.tile.tuile_plateau && res.tile.tuile_plateau.nom_court) || sp.id) : (getCastingRef()[sp.id] ? getCastingRef()[sp.id].nom_animal : sp.alias_oriente);
      const isRev = isSlotFlaggedReview(w);
      const cls = ['x3-index-cell'];
      if (uiState.currentSlotId === sp.id) cls.push('is-current');
      if (isRev) cls.push('is-review');
      else if (w.selected_source) cls.push('is-elected');
      const srcCls = w.selected_source === 'custom' ? 'is-custom' : (w.selected_source ? 'is-set' : '');
      const srcTxt = w.selected_source ? PANEL_SHORT[w.selected_source] : '—';

      return (
        `<button type="button" class="${cls.join(' ')}" data-index-slot="${esc(sp.id)}" onclick="AmazoniaExplorerV63.goToSlot('${esc(sp.id)}')">` +
        `<span class="truncate"><strong class="font-mono">${esc(sp.id)}</strong> <span class="text-slate-500">${esc(sp.alias_oriente)}</span> · ${esc(nom)}</span>` +
        `<span class="flex items-center gap-1">${isRev ? '<span title="À revoir">🤔</span>' : ''}${w.comment ? '<span title="Note">💬</span>' : ''}<span class="x3-index-src ${srcCls}">${esc(srcTxt)}</span></span>` +
        `</button>`
      );
    }).join('');

    return (
      `<div class="x3-drawer" data-drawer="index30">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<div class="flex flex-wrap items-center gap-1.5">` +
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.indexFilter === 'ALL' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setIndexFilter('ALL')">Tous (30)</button>` +
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.indexFilter === 'UNELECTED' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setIndexFilter('UNELECTED')">À trancher (${radar.unelectedIds.length})</button>` +
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.indexFilter === 'REVIEW' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setIndexFilter('REVIEW')">🤔 À revoir (${reviewCount})</button>` +
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.indexFilter === 'MODIFIED' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setIndexFilter('MODIFIED')">✏️ Hybrides</button>` +
      `</div>` +
      `<div class="flex flex-wrap items-center gap-1.5">` +
      `<span class="text-xs text-slate-500">Pré-remplir les non tranchés :</span>` +
      PANEL_IDS.map(pid => `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.fillUnelectedFrom('${pid}')">${PANEL_SHORT[pid]}</button>`).join('') +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.toggleDrawer(null)">✕</button>` +
      `</div>` +
      `</div>` +
      `<div class="x3-index-grid">${cells || '<div class="text-xs text-slate-500">Aucun emplacement dans ce filtre.</div>'}</div>` +
      `</div>`
    );
  }

  function renderBrowseDrawer() {
    const f = uiState.filters;
    const sources = [
      { id: 'canon', label: '★ Mon Canon' },
      { id: 'panel_1', label: 'Panel 1' },
      { id: 'panel_2', label: 'Panel 2' },
      { id: 'panel_3', label: 'Panel 3' },
      { id: 'archive_v6_2', label: '📦 Archive v6.2' }
    ].map(s => (
      `<button type="button" class="x3-btn x3-btn-sm ${uiState.mode === 'list' && uiState.listSource === s.id ? 'x3-btn-primary' : ''}" ` +
      `data-list-source="${s.id}" onclick="AmazoniaExplorerV63.openListView('${s.id}')">${esc(s.label)}</button>`
    )).join('');

    const quickRes = QUICK_RESOURCES.map(tok => {
      const m = humanizeToken(tok);
      const cls = tok.startsWith('ICONE_') ? 'is-icon' : '';
      return `<button type="button" class="x3-res-pill ${cls} ${uiState.resourceFocus === tok ? 'is-active' : ''}" onclick="AmazoniaExplorerV63.focusResource('${esc(tok)}')">${m.icon} ${esc(m.label)}</button>`;
    }).join('');

    return (
      `<div class="x3-drawer" data-drawer="browse">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<div class="flex flex-wrap items-center gap-1.5"><span class="text-xs font-bold text-slate-600">Vue Liste complète :</span>${sources}</div>` +
      `<div class="flex items-center gap-1.5">` +
      (uiState.mode === 'list' ? `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.setMode('arbitrate')">↩ Retour au Duel P1·P2·P3</button>` : '') +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.toggleDrawer(null)">✕ Fermer</button>` +
      `</div>` +
      `</div>` +
      `<div class="flex flex-wrap items-center gap-2">` +
      `<input type="text" id="x3-search-input" class="x3-input flex-1" style="min-width:12rem" value="${esc(f.search)}" placeholder="Rechercher un animal, une règle, une note…" oninput="AmazoniaExplorerV63.setFilter('search', this.value)" />` +
      `<select class="x3-select" onchange="AmazoniaExplorerV63.setFilter('peuple', this.value)">` +
      `<option value="ALL" ${f.peuple === 'ALL' ? 'selected' : ''}>Tous Peuples</option>` +
      PEUPLE_ORDER.map(p => `<option value="${p}" ${f.peuple === p ? 'selected' : ''}>${p} · ${esc(PEUPLE_META[p].nom)}</option>`).join('') +
      `</select>` +
      `<select class="x3-select" onchange="AmazoniaExplorerV63.setFilter('family', this.value)">` +
      `<option value="ALL" ${f.family === 'ALL' ? 'selected' : ''}>Toutes Familles</option>` +
      `<option value="GARDIEN" ${f.family === 'GARDIEN' ? 'selected' : ''}>Gardiens</option>` +
      `<option value="REVE" ${f.family === 'REVE' ? 'selected' : ''}>Rêves</option>` +
      `<option value="CROISSANCE" ${f.family === 'CROISSANCE' ? 'selected' : ''}>Nids</option>` +
      `</select>` +
      `<select class="x3-select" onchange="AmazoniaExplorerV63.setFilter('role', this.value)">` +
      `<option value="ALL" ${f.role === 'ALL' ? 'selected' : ''}>Tous Rôles</option>` +
      `<option value="TWIST_2K3" ${f.role === 'TWIST_2K3' ? 'selected' : ''}>⚡ Twists 2K3</option>` +
      `<option value="LOI_PASSIVE" ${f.role === 'LOI_PASSIVE' ? 'selected' : ''}>⚖️ Lois passives</option>` +
      `<option value="CATALYSEUR_EVEIL" ${f.role === 'CATALYSEUR_EVEIL' ? 'selected' : ''}>☀️ Catalyseurs Éveil</option>` +
      `<option value="LEVIER_REVE" ${f.role === 'LEVIER_REVE' ? 'selected' : ''}>🌙 Leviers Rêve</option>` +
      `<option value="ENRACINEMENT" ${f.role === 'ENRACINEMENT' ? 'selected' : ''}>🌱 Enracinements</option>` +
      `<option value="AUTONOMIE_A0" ${f.role === 'AUTONOMIE_A0' ? 'selected' : ''}>🔓 A=0</option>` +
      `</select>` +
      `<button type="button" class="x3-btn x3-btn-sm x3-btn-review ${f.reviewOnly ? 'is-on' : ''}" onclick="AmazoniaExplorerV63.toggleFilterReviewOnly()">🤔 À revoir</button>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.resetFilters()">↺</button>` +
      `</div>` +
      `<div class="flex flex-wrap items-center gap-1.5"><span class="text-[11px] font-bold text-slate-500">Producteurs ⇄ Consommateurs :</span>${quickRes}</div>` +
      `</div>`
    );
  }

  function renderResourceFocusPanel(tilesMap) {
    if (!uiState.resourceFocus) return '';
    const idx = computeResourceIndex(uiState.resourceFocus, tilesMap);
    const natHtml = idx.nativeProducers.map(n => `<span class="x3-res-pill is-floor">${n.icon} ${esc(n.label)}</span>`).join('');
    const prodHtml = idx.producers.map(p => `<button type="button" class="x3-tile-link-chip is-up" onclick="AmazoniaExplorerV63.goToSlot('${esc(p.id)}')"><strong>${esc(p.id)}</strong> ${esc(p.nom)}</button>`).join('');
    const consList = idx.isIcon
      ? idx.consumersIcon.map(c => `<button type="button" class="x3-tile-link-chip is-down" onclick="AmazoniaExplorerV63.goToSlot('${esc(c.id)}')">🗿 <strong>${esc(c.id)}</strong> ${esc(c.nom)}</button>`).join('')
      : idx.consumersFloor.map(c => `<button type="button" class="x3-tile-link-chip" onclick="AmazoniaExplorerV63.goToSlot('${esc(c.id)}')">✅ <strong>${esc(c.id)}</strong> ${esc(c.nom)}</button>`).concat(
          idx.consumersSynergy.map(c => `<button type="button" class="x3-tile-link-chip is-down" onclick="AmazoniaExplorerV63.goToSlot('${esc(c.id)}')">✨ <strong>${esc(c.id)}</strong> ${esc(c.nom)} (${c.coverage.covered}/${c.coverage.total})</button>`)
        ).join('');

    return (
      `<div class="x3-resource-focus" data-resource-focus="${esc(idx.key)}">` +
      `<div class="flex items-center justify-between gap-2 flex-wrap">` +
      `<div class="font-bold text-sm">${idx.meta.icon} ${esc(idx.meta.label)} — Producteurs ⇄ Consommateurs</div>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.clearResourceFocus()">✕ Fermer</button>` +
      `</div>` +
      `<div class="x3-two-cols">` +
      `<div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5"><div class="x3-section-label">⬅️ Producteurs &amp; Déclencheurs</div><div class="flex flex-wrap gap-1">${natHtml}${prodHtml || '<span class="text-xs text-slate-400">Aucune tuile</span>'}</div></div>` +
      `<div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 space-y-1.5"><div class="x3-section-label">➡️ Consommateurs &amp; Bénéficiaires</div><div class="flex flex-wrap gap-1">${consList || '<span class="text-xs text-slate-400">Aucune tuile</span>'}</div></div>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // 2. ÉCRAN PRINCIPAL — Duel Arbitrage P1 | P2 | P3 (1 emplacement à la fois)
  // --------------------------------------------------------------------------
  function renderArbitrateDuelView() {
    const specs = getSlotsSpec();
    const specMap = getSlotSpecMap();
    const slotId = specMap[uiState.currentSlotId] ? uiState.currentSlotId : 'G1';
    const sp = specMap[slotId];
    const curIdx = specs.findIndex(s => s.id === slotId);
    const twinId = TWIN_BY_SLOT[slotId];
    const w = uiState.workspace.slots[slotId];
    const isRev = isSlotFlaggedReview(w);

    const animalTitle = sp.famille === 'GARDIEN' && getCastingRef()[slotId]
      ? getCastingRef()[slotId].nom_animal
      : (sp.famille === 'REVE' ? `Rêve ${sp.alias_oriente}` : `Nid ${sp.alias_oriente}`);

    const colsHtml = PANEL_IDS.map(pid => {
      const tile = getPanelTile(pid, slotId);
      if (!tile) return '';
      const tp = tile.tuile_plateau || {};
      const mcp = tp.mots_cles_plateau || {};
      const cj = tile.carte_joueur || {};
      const tr = cj.texte_regle || {};
      const isKept = w.selected_source === pid;
      const isLoi = tile.nature === 'LOI_PASSIVE';
      const isTwist = Boolean(tile.est_twist);
      const colCls = ['x3-duel-col'];
      if (isKept) colCls.push('is-kept');
      if (isLoi) colCls.push('is-loi');
      if (isTwist) colCls.push('is-twist');

      const recIcon = tp.icone_conseillee ? GUARDIAN_ICON_BY_ID[String(tp.icone_conseillee).toUpperCase()] : null;
      const pictos = (tp.pictogrammes || []).map(renderPictoToken).join('');
      const kwHtml = [
        mcp.face_1 ? `<div class="x3-mini-kw-line"><strong>F1 :</strong> ${esc(mcp.face_1)}</div>` : '',
        mcp.face_2 ? `<div class="x3-mini-kw-line"><strong>F2 :</strong> ${esc(mcp.face_2)}</div>` : '',
        mcp.enracine ? `<div class="x3-mini-kw-line text-emerald-800"><strong>🌱 :</strong> ${esc(mcp.enracine)}</div>` : ''
      ].filter(Boolean).join('');

      const panelMap = getTilesMapForSource(pid);

      return (
        `<article class="${colCls.join(' ')}" data-duel-col="${pid}" data-nature="${esc(tile.nature)}" data-twist="${isTwist ? 'true' : 'false'}">` +
        `<div class="x3-duel-col-head">` +
        `<div class="flex items-center justify-between gap-2">` +
        `<span class="text-xs font-bold uppercase tracking-wider text-slate-500">${esc(PANEL_LABELS[pid])}</span>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-keep ${isKept ? 'is-kept' : ''}" data-keep-btn="${pid}" onclick="AmazoniaExplorerV63.keepSlot('${esc(slotId)}', '${pid}')">${isKept ? '✓ Gardée' : '★ Garder'}</button>` +
        `</div>` +
        `<h3 class="x3-duel-title">${esc(cj.titre_complet || tp.nom_court || slotId)}</h3>` +
        `<div class="flex flex-wrap gap-1">${renderRoleBadges(tile, false)}</div>` +
        `<div class="x3-duel-mini-strip" data-component="mini-tuile">` +
        `<div class="flex items-center justify-between gap-2 flex-wrap">` +
        `<span class="x3-mini-window">${recIcon ? recIcon.icon + ' ' + esc(recIcon.label) : '⏱ ' + esc(formatFenetreLabel(tp.fenetre_badge))}</span>` +
        `<div class="flex gap-1">${pictos}</div>` +
        `</div>` +
        `${kwHtml}` +
        `</div>` +
        `</div>` +
        `<div class="x3-duel-col-body" data-component="grande-carte">` +
        (cj.pitch_ambiance ? `<p class="x3-pitch">${esc(cj.pitch_ambiance)}</p>` : '') +
        `<div class="x3-rule-block ${isLoi ? 'is-loi-rule' : ''}"><div class="x3-rule-label">${isLoi ? '⚖️ Loi passive permanente' : (sp.famille === 'GARDIEN' ? 'Face 1' : 'Effet')}</div><div>${esc(tr.face_1 || '—')}</div></div>` +
        (tr.face_2 ? `<div class="x3-rule-block is-face2"><div class="x3-rule-label">✨ Face 2 — Éveillée</div><div>${esc(tr.face_2)}</div></div>` : '') +
        (tr.enracine ? `<div class="x3-rule-block is-enracine"><div class="x3-rule-label">🌱 Enraciné</div><div>${esc(tr.enracine)}</div></div>` : '') +
        `${renderCollapsibleDetails(tile, panelMap, pid)}` +
        `</div>` +
        `<div class="x3-duel-col-foot">` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${esc(slotId)}', '${pid}')">✏️ Hybrider depuis ${PANEL_SHORT[pid]}</button>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-keep ${isKept ? 'is-kept' : ''}" onclick="AmazoniaExplorerV63.keepSlot('${esc(slotId)}', '${pid}')">${isKept ? '✓ Gardée' : '★ Garder'}</button>` +
        `</div>` +
        `</article>`
      );
    }).join('');

    const customBanner = w.is_modified && w.custom_tile
      ? `<div class="rounded-xl bg-amber-50 border border-amber-300 px-4 py-2.5 text-xs flex flex-wrap items-center justify-between gap-2" data-custom-banner="true">` +
        `<div><strong>✏️ Version hybride / modifiée :</strong> ${esc((w.custom_tile.carte_joueur && w.custom_tile.carte_joueur.titre_complet) || slotId)}</div>` +
        `<div class="flex flex-wrap gap-1.5">` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-keep ${w.selected_source === 'custom' ? 'is-kept' : ''}" onclick="AmazoniaExplorerV63.keepSlot('${esc(slotId)}', 'custom')">${w.selected_source === 'custom' ? '✓ Gardée' : '★ Garder ma version'}</button>` +
        `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${esc(slotId)}', 'custom')">✏️ Modifier</button>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-danger" onclick="AmazoniaExplorerV63.restoreOriginalSlot('${esc(slotId)}')">↺ Restaurer</button>` +
        `</div></div>`
      : '';

    const rfSrc = uiState.resourceFocusSource || 'panel_1';
    const rfPanel = uiState.resourceFocus ? renderResourceFocusPanel(getTilesMapForSource(rfSrc)) : '';
    const medallion = getTileMedallionHtml(slotId, sp.famille);

    return (
      `<div class="space-y-3" data-arbitrate-slot="${esc(slotId)}">` +
      `<div class="x3-stepper-bar">` +
      `<div class="flex items-center gap-2.5 flex-wrap">` +
      `${medallion}` +
      `<span class="x3-slot-id-pill">${esc(slotId)}</span>` +
      `${renderOrientedEdgeBadge(sp.origine, sp.voisin)}` +
      `<h2 class="x3-slot-heading">${esc(animalTitle)}</h2>` +
      (twinId ? `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.goToSlot('${esc(twinId)}')">🔗 Jumelle ${esc(twinId)}</button>` : '') +
      `</div>` +
      `<div class="flex items-center gap-1.5 flex-wrap">` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.stepSlot(-1)" title="Flèche gauche">◀ Précédent</button>` +
      `<button type="button" class="x3-btn x3-btn-sm font-mono" onclick="AmazoniaExplorerV63.toggleDrawer('index30')" title="Voir les 30 emplacements">${curIdx + 1} / ${specs.length}</button>` +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.stepSlot(1)" title="Flèche droite">Suivant ▶</button>` +
      `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.goToNextPending()">⏭ Prochain à trancher</button>` +
      `</div>` +
      `</div>` +
      `${rfPanel}` +
      `${customBanner}` +
      `<div class="x3-duel-grid">${colsHtml}</div>` +
      `<div class="x3-trio-bar" data-trio-bar="${esc(slotId)}">` +
      `<button type="button" class="x3-btn x3-btn-sm x3-btn-review ${isRev ? 'is-on' : ''}" data-review-btn="true" onclick="AmazoniaExplorerV63.toggleSlotReview('${esc(slotId)}')">${isRev ? '🤔 Marqué À revoir' : '🤔 À revoir'}</button>` +
      `<input type="text" class="x3-note-input" data-note-slot="${esc(slotId)}" value="${esc(w.comment || '')}" placeholder="Note personnelle sur ${esc(slotId)} (sauvegarde instantanée)…" oninput="AmazoniaExplorerV63.setSlotCommentLive('${esc(slotId)}', this.value)" />` +
      `<span class="x3-saved-hint" id="x3-saved-${esc(slotId)}">✓ Enregistré</span>` +
      `</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // 3. Vue Liste Bi-Composant (Mon Canon / Panel 1..3 / Archive v6.2)
  // --------------------------------------------------------------------------
  function renderBiComponentCard(slotId, tile, sourceInfo, tilesMap, allowEdit) {
    if (!tile) {
      const sp = getSlotSpecMap()[slotId];
      return (
        `<article class="x3-tile-card" data-slot-id="${esc(slotId)}">` +
        `<div class="x3-card-top">` +
        `<div class="flex items-center gap-2"><strong>${esc(slotId)}</strong> ${renderOrientedEdgeBadge(sp.origine, sp.voisin)} <span class="text-xs text-slate-500">À trancher</span></div>` +
        `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.goToSlot('${esc(slotId)}')">⚔️ Arbitrer P1·P2·P3</button>` +
        `</div></article>`
      );
    }

    const tp = tile.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const cj = tile.carte_joueur || {};
    const tr = cj.texte_regle || {};
    const w = uiState.workspace.slots[slotId];
    const isRev = isSlotFlaggedReview(w);
    const isLoi = tile.nature === 'LOI_PASSIVE';
    const isTwist = Boolean(tile.est_twist);
    const cls = ['x3-tile-card'];
    if (isLoi) cls.push('is-loi');
    if (isTwist) cls.push('is-twist');
    if (sourceInfo && sourceInfo.elected) cls.push('is-kept');

    const recIcon = tp.icone_conseillee ? GUARDIAN_ICON_BY_ID[String(tp.icone_conseillee).toUpperCase()] : null;
    const pictos = (tp.pictogrammes || []).map(renderPictoToken).join('');
    const medallion = getTileMedallionHtml(tile.id, tile.famille);

    const kwLines = [
      mcp.face_1 ? `<div class="x3-mini-kw-line"><strong>F1 :</strong> ${esc(mcp.face_1)}</div>` : '',
      mcp.face_2 ? `<div class="x3-mini-kw-line"><strong>F2 :</strong> ${esc(mcp.face_2)}</div>` : '',
      mcp.enracine ? `<div class="x3-mini-kw-line text-emerald-800"><strong>🌱 :</strong> ${esc(mcp.enracine)}</div>` : ''
    ].filter(Boolean).join('');

    const digestFooter = (sourceInfo && sourceInfo.sourceKey === 'archive_v6_2' && typeof global.renderSlotDigestFooter === 'function')
      ? `<div class="px-4 pb-3">${global.renderSlotDigestFooter(tile.id, ['A'])}</div>`
      : '';

    const keepTarget = (sourceInfo && PANEL_IDS.includes(sourceInfo.sourceKey)) ? sourceInfo.sourceKey : (w && w.selected_source) || 'panel_1';
    const isKept = Boolean(w && (sourceInfo.sourceKey === 'canon' ? w.selected_source : w.selected_source === sourceInfo.sourceKey));

    return (
      `<article class="${cls.join(' ')}" data-slot-id="${esc(tile.id)}" data-nature="${esc(tile.nature)}" data-twist="${isTwist ? 'true' : 'false'}">` +
      `<div class="x3-card-top">` +
      `<div class="flex items-center gap-1.5 flex-wrap">` +
      `<span class="x3-slot-id-pill">${esc(tile.id)}</span>` +
      `${renderOrientedEdgeBadge(tile.origine, tile.voisin)}` +
      `${renderRoleBadges(tile, sourceInfo && sourceInfo.modified)}` +
      `</div>` +
      `<div class="flex items-center gap-1.5">` +
      (allowEdit ? `<button type="button" class="x3-btn x3-btn-sm x3-btn-keep ${isKept ? 'is-kept' : ''}" onclick="AmazoniaExplorerV63.keepSlot('${esc(tile.id)}', '${esc(keepTarget)}')">${isKept ? '✓ Gardée' : '★ Garder'}</button>` : '') +
      (allowEdit ? `<button type="button" class="x3-btn x3-btn-sm x3-btn-review ${isRev ? 'is-on' : ''}" onclick="AmazoniaExplorerV63.toggleSlotReview('${esc(tile.id)}')">🤔</button>` : '') +
      (allowEdit ? `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.openEditor('${esc(tile.id)}', '${esc(sourceInfo.sourceKey === 'canon' ? (w.selected_source || 'panel_1') : sourceInfo.sourceKey)}')">✏️</button>` : '') +
      `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.goToSlot('${esc(tile.id)}')">⚔️ Duel</button>` +
      `</div>` +
      `</div>` +
      `<div class="x3-duo-grid">` +
      `<div class="x3-mini-tuile fam-${esc(tile.famille)}" data-component="mini-tuile">` +
      `<div class="flex items-center gap-2">${medallion}<div class="x3-mini-name">${esc(tp.nom_court || tile.id)}</div></div>` +
      `<span class="x3-mini-window">${recIcon ? recIcon.icon + ' ' + esc(recIcon.label) : '⏱ ' + esc(formatFenetreLabel(tp.fenetre_badge))}</span>` +
      (pictos ? `<div class="flex flex-wrap gap-1">${pictos}</div>` : '') +
      `${kwLines}` +
      `</div>` +
      `<div class="x3-grande-carte" data-component="grande-carte">` +
      `<h3 class="x3-duel-title">${esc(cj.titre_complet || tp.nom_court || tile.id)}</h3>` +
      (cj.pitch_ambiance ? `<p class="x3-pitch">${esc(cj.pitch_ambiance)}</p>` : '') +
      `<div class="x3-rule-block ${isLoi ? 'is-loi-rule' : ''}"><div class="x3-rule-label">${isLoi ? '⚖️ Loi passive permanente' : (tile.famille === 'GARDIEN' ? 'Face 1' : 'Effet')}</div><div>${esc(tr.face_1 || '—')}</div></div>` +
      (tr.face_2 ? `<div class="x3-rule-block is-face2"><div class="x3-rule-label">✨ Face 2 — Éveillée</div><div>${esc(tr.face_2)}</div></div>` : '') +
      (tr.enracine ? `<div class="x3-rule-block is-enracine"><div class="x3-rule-label">🌱 Enraciné</div><div>${esc(tr.enracine)}</div></div>` : '') +
      `${renderCollapsibleDetails(tile, tilesMap)}` +
      `</div>` +
      `</div>` +
      `${digestFooter}` +
      `</article>`
    );
  }

  function renderListView() {
    const visibleIds = getFilteredSlotIds();
    const tilesMap = getTilesMapForSource(uiState.listSource);
    const isArchive = uiState.listSource === 'archive_v6_2';
    const headerBanner =
      `<div class="x3-stepper-bar">` +
      `<div class="text-sm font-bold">${esc(PANEL_LABELS[uiState.listSource] || uiState.listSource)} · ${visibleIds.length} / 30 emplacements${isArchive ? ' (lecture seule)' : ''}</div>` +
      `<div class="flex items-center gap-1.5">` +
      `<button type="button" class="x3-btn x3-btn-sm x3-btn-primary" onclick="AmazoniaExplorerV63.setMode('arbitrate')">↩ Retour au Duel P1·P2·P3</button>` +
      `</div></div>`;

    const cards = visibleIds.map(sid => {
      const res = getEffectiveTile(sid, uiState.listSource);
      return renderBiComponentCard(sid, res.tile, res, tilesMap, !isArchive);
    }).join('');

    return (
      `<div class="space-y-3" data-list-view="${esc(uiState.listSource)}">` +
      `${headerBanner}` +
      (uiState.resourceFocus ? renderResourceFocusPanel(tilesMap) : '') +
      `${cards || '<div class="p-8 text-center bg-white rounded-xl border border-dashed border-slate-300 text-sm text-slate-500">Aucun emplacement ne correspond aux filtres.</div>'}` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // 4. ÉCRAN SECONDAIRE — Simulateur de Table 3 à 6 Peuples
  // --------------------------------------------------------------------------
  function renderTableWheelSvg(sim) {
    const cx = 125; const cy = 115; const r = 76; const n = sim.n;
    const coords = sim.peuples.map((p, i) => {
      const ang = -Math.PI / 2 + (2 * Math.PI * i) / n;
      return { p, x: cx + r * Math.cos(ang), y: cy + r * Math.sin(ang) };
    });
    const edges = coords.map((c, i) => {
      const nxt = coords[(i + 1) % n];
      const mx = (c.x + nxt.x) / 2; const my = (c.y + nxt.y) / 2;
      return (
        `<line x1="${c.x.toFixed(1)}" y1="${c.y.toFixed(1)}" x2="${nxt.x.toFixed(1)}" y2="${nxt.y.toFixed(1)}" stroke="#357054" stroke-width="2.2" stroke-opacity="0.65" />` +
        `<rect x="${(mx - 20).toFixed(1)}" y="${(my - 8).toFixed(1)}" width="40" height="16" rx="8" fill="#ffffff" stroke="#b8d5c4" />` +
        `<text x="${mx.toFixed(1)}" y="${(my + 3).toFixed(1)}" text-anchor="middle" font-size="8.5" font-weight="700" fill="#1a3529">${esc(sim.borders[i].slots.join('·'))}</text>`
      );
    }).join('');
    const nodes = coords.map(c => {
      const col = PEUPLE_SVG_COLORS[c.p] || { fill: '#f1f5f9', stroke: '#64748b', text: '#0f172a' };
      const hl = uiState.simHighlightPeuple === c.p;
      return (
        `<g style="cursor:pointer" onclick="AmazoniaExplorerV63.toggleSimHighlight('${c.p}')">` +
        `<circle cx="${c.x.toFixed(1)}" cy="${c.y.toFixed(1)}" r="${hl ? 22 : 19}" fill="${col.fill}" stroke="${col.stroke}" stroke-width="${hl ? 3 : 2}" />` +
        `<text x="${c.x.toFixed(1)}" y="${(c.y + 4).toFixed(1)}" text-anchor="middle" font-size="12" font-weight="800" fill="${col.text}">${esc(c.p)}</text>` +
        `</g>`
      );
    }).join('');
    return (
      `<svg class="x3-wheel-svg" viewBox="0 0 250 230" width="230" height="212" role="img" aria-label="Roue ${esc(sim.canonKey)}">` +
      `<circle cx="${cx}" cy="${cy}" r="${r}" fill="none" stroke="#dbe7df" stroke-dasharray="4 4" />` +
      `${edges}${nodes}` +
      `<text x="${cx}" y="${cy - 3}" text-anchor="middle" font-size="10.5" font-weight="800" fill="#1a3529">${esc(sim.canonKey)}</text>` +
      `<text x="${cx}" y="${cy + 11}" text-anchor="middle" font-size="9" font-weight="600" fill="#475569">${sim.n}J · ${sim.n * 2} tuiles</text>` +
      `</svg>`
    );
  }

  function renderSimulatorView() {
    const sim = analyzeTableSimulation(uiState.simPeuples, uiState.simSource);
    const activeMap = {};
    sim.tileEntries.forEach(e => { if (e.tile) activeMap[e.slotId] = e.tile; });

    const presets = PRESET_TABLES.map(pr => {
      const act = canonicalizeAssise(pr.peuples).key === sim.canonKey;
      return `<button type="button" class="x3-btn x3-btn-sm ${act ? 'x3-btn-primary' : ''}" data-sim-preset="${esc(pr.key)}" onclick="AmazoniaExplorerV63.setSimPreset('${esc(pr.key)}')">${esc(pr.label)} <span class="opacity-70 font-normal">${esc(pr.tag)}</span></button>`;
    }).join('');

    const seats = sim.peuples.map((p, i) => (
      `<span class="x3-seat-pill x3-peuple-${p}">#${i + 1} ${getPeupleIconHtml(p, 13)} ${esc(PEUPLE_META[p].short)}` +
      (i > 0 ? `<button type="button" class="x3-seat-move" onclick="AmazoniaExplorerV63.moveSimPeuple('${p}', -1)">◀</button>` : '') +
      (i < sim.n - 1 ? `<button type="button" class="x3-seat-move" onclick="AmazoniaExplorerV63.moveSimPeuple('${p}', 1)">▶</button>` : '') +
      `<button type="button" class="x3-seat-move" onclick="AmazoniaExplorerV63.toggleSimPeuple('${p}')">✕</button></span>`
    )).join('') + PEUPLE_ORDER.filter(p => !sim.peuples.includes(p)).map(p => (
      `<button type="button" class="x3-seat-pill is-inactive" onclick="AmazoniaExplorerV63.toggleSimPeuple('${p}')">+ ${getPeupleIconHtml(p, 13)} ${esc(PEUPLE_META[p].short)}</button>`
    )).join('');

    const chainsHtml = sim.completeChains.length > 0
      ? sim.completeChains.slice(0, 12).map(ch => `<div class="text-xs p-2 rounded bg-slate-50 border border-slate-200"><strong class="text-emerald-800">${esc(ch.fromLabel)}</strong> → <span class="font-semibold">${ch.viaMeta.icon} ${esc(ch.viaMeta.label)}</span> → <strong class="text-amber-900">${esc(ch.toLabel)}</strong></div>`).join('')
      : '<div class="text-xs text-slate-500">Toutes les tuiles tournent sur leurs planchers solo et accessoires.</div>';

    const isolatedHtml = sim.isolatedAmplifiers.length > 0
      ? sim.isolatedAmplifiers.map(iso => `<div class="text-xs p-2 rounded bg-amber-50 border border-amber-200 text-amber-950">⚠️ <strong>${esc(iso.slotId)} · ${esc(iso.tileName)}</strong> : amplificateur ${iso.stateMeta.icon} ${esc(iso.stateMeta.label)} sans producteur sur cette table.</div>`).join('')
      : '<div class="text-xs p-2 rounded bg-emerald-50 border border-emerald-200 text-emerald-900">✅ Aucun amplificateur isolé sur cette table.</div>';

    const accHtml = sim.accessories.map(acc => `<div class="text-xs p-2 rounded bg-slate-50 border border-slate-200"><strong>${renderPeuplePill(acc.code, true)}</strong> · ${acc.icon} <strong>${esc(acc.title)}</strong> — ${esc(acc.summary)}</div>`).join('');

    const visibleEntries = uiState.simHighlightPeuple
      ? sim.tileEntries.filter(e => {
          const sp = getSlotSpecMap()[e.slotId];
          return sp && (sp.origine === uiState.simHighlightPeuple || sp.voisin === uiState.simHighlightPeuple);
        })
      : sim.tileEntries;

    const cards = visibleEntries.map(e => renderBiComponentCard(e.slotId, e.tile, e, activeMap, true)).join('');

    return (
      `<div class="space-y-3" data-simulator-assise="${esc(sim.canonKey)}">` +
      `<div class="x3-sim-panel">` +
      `<div class="flex flex-wrap items-center justify-between gap-2">` +
      `<h2 class="font-serif text-xl font-bold text-slate-900">🎡 Tester une Table — ${esc(sim.canonKey)} (${sim.n} joueurs · ${sim.n * 2} tuiles)</h2>` +
      `<div class="flex items-center gap-1.5 text-xs"><span class="font-semibold text-slate-500">Source :</span>` +
      `<select class="x3-select" onchange="AmazoniaExplorerV63.setSimSource(this.value)">` +
      `<option value="canon" ${uiState.simSource === 'canon' ? 'selected' : ''}>★ Mon Canon v6.3</option>` +
      `<option value="panel_1" ${uiState.simSource === 'panel_1' ? 'selected' : ''}>Panel 1</option>` +
      `<option value="panel_2" ${uiState.simSource === 'panel_2' ? 'selected' : ''}>Panel 2</option>` +
      `<option value="panel_3" ${uiState.simSource === 'panel_3' ? 'selected' : ''}>Panel 3</option>` +
      `</select></div>` +
      `</div>` +
      `<div class="flex flex-wrap gap-1.5">${presets}</div>` +
      (uiState.simSource === 'canon' && sim.metrics.missingCanonCount > 0
        ? `<div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-950 flex flex-wrap items-center justify-between gap-2">` +
          `<span>💡 <strong>${sim.metrics.missingCanonCount}</strong> tuile(s) de cette table ne sont pas encore gardées dans <strong>Mon Canon</strong>.</span>` +
          `<span class="flex gap-1.5"><button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setSimSource('panel_1')">Tester Panel 1</button>` +
          `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setSimSource('panel_2')">Panel 2</button>` +
          `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.setSimSource('panel_3')">Panel 3</button></span></div>`
        : '') +
      `<div class="x3-sim-grid">` +
      `<div class="x3-sim-wheel-box">${renderTableWheelSvg(sim)}<div class="text-[11px] text-slate-500">Clic Peuple = isoler ses lisières</div></div>` +
      `<div class="space-y-3">` +
      `<div class="flex flex-wrap gap-1.5">${seats}</div>` +
      `<div class="x3-sim-metrics">` +
      `<div class="x3-metric-card ${sim.metrics.loisAlert ? 'is-err' : 'is-ok'}"><div class="x3-metric-val">${sim.metrics.loisCount} / 2</div><div class="x3-metric-lbl">⚖️ Lois passives</div></div>` +
      `<div class="x3-metric-card"><div class="x3-metric-val">${sim.metrics.twistsCount}</div><div class="x3-metric-lbl">⚡ Twists 2K3</div></div>` +
      `<div class="x3-metric-card ${sim.metrics.eveilAlert ? 'is-err' : (sim.modules.gardiens ? 'is-ok' : '')}"><div class="x3-metric-val">${sim.modules.gardiens ? sim.metrics.eveilCount : '—'}</div><div class="x3-metric-lbl">☀️ Éveil</div></div>` +
      `<div class="x3-metric-card ${sim.metrics.sommeilAlert ? 'is-err' : (sim.modules.reves ? 'is-ok' : '')}"><div class="x3-metric-val">${sim.modules.reves ? sim.metrics.sommeilCount : '—'}</div><div class="x3-metric-lbl">🌙 Sommeil</div></div>` +
      `<div class="x3-metric-card"><div class="x3-metric-val">${sim.metrics.enracCount}</div><div class="x3-metric-lbl">🌱 Enracinements</div></div>` +
      `</div>` +
      `<details class="x3-details-fold"><summary><span>▾ Accessoires 3+3 présents (${sim.accessories.length}) &amp; Chaînes de moteurs (${sim.completeChains.length})</span><span class="text-[11px] text-slate-500">${sim.isolatedAmplifiers.length} isolé(s)</span></summary>` +
      `<div class="x3-details-body"><div class="space-y-1">${accHtml}</div><div class="x3-two-cols"><div class="space-y-1"><div class="x3-section-label">🔗 Chaînes bouclées</div>${chainsHtml}</div><div class="space-y-1"><div class="x3-section-label">🔍 Amplificateurs isolés</div>${isolatedHtml}</div></div></div></details>` +
      `</div>` +
      `</div>` +
      `</div>` +
      `<div class="space-y-3">${cards}</div>` +
      `</div>`
    );
  }

  // --------------------------------------------------------------------------
  // 5. Modales : Guide 32 Pictos, Éditeur/Hybrideur, Exports
  // --------------------------------------------------------------------------
  function renderPictoGuideModal() {
    if (!uiState.pictoGuideOpen) return '';
    const ref = getPictosRef();
    const byCat = {};
    Object.values(ref).forEach(it => {
      const c = it.categorie || 'ACTION';
      if (!byCat[c]) byCat[c] = [];
      byCat[c].push(it);
    });
    const cats = PICTO_CATEGORIES.map(cat => {
      const items = byCat[cat.id] || [];
      if (!items.length) return '';
      return (
        `<div class="space-y-1.5"><div class="x3-section-label">${esc(cat.label)} (${items.length})</div>` +
        `<div class="x3-picto-cat-grid">` +
        items.map(it => `<button type="button" class="x3-picto-guide-card" onclick="AmazoniaExplorerV63.setPictoFilter('${esc(it.code)}')"><span class="x3-picto-guide-sym">${esc(it.symbole)}</span><span class="text-xs font-semibold text-slate-800">${esc(it.libelle)}</span></button>`).join('') +
        `</div></div>`
      );
    }).join('');
    return (
      `<div class="x3-modal-backdrop" id="x3-picto-guide-modal" role="dialog" aria-modal="true" onclick="if(event.target===this) AmazoniaExplorerV63.closePictoGuide()">` +
      `<div class="x3-modal-panel">` +
      `<div class="x3-modal-head"><h3 class="x3-modal-title">📖 Guide des ${Object.keys(ref).length} pictogrammes officiels</h3><button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closePictoGuide()">✕ Fermer</button></div>` +
      `<div class="x3-modal-body">${cats}</div>` +
      `</div></div>`
    );
  }

  function renderEditorMiniTuileHint(tile) {
    const tp = tile.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const hasPunct = [mcp.face_1, mcp.face_2, mcp.enracine, tp.resume_plateau].some(s => typeof s === 'string' && /[.!?]/.test(s));
    return hasPunct ? '<div class="p-2 rounded bg-amber-50 border border-amber-200 text-[11px] text-amber-900">💡 Astuce Mini-Tuile : évitez <code>. ! ?</code> sur les mots-clés plateau.</div>' : '';
  }

  function renderEditorPreviewHtml(tile) {
    const tp = tile.tuile_plateau || {};
    const mcp = tp.mots_cles_plateau || {};
    const cj = tile.carte_joueur || {};
    const tr = cj.texte_regle || {};
    const pictos = (tp.pictogrammes || []).map(renderPictoToken).join('');
    return (
      `<div class="x3-section-label">👁️ Prévisualisation en direct</div>` +
      `${renderEditorMiniTuileHint(tile)}` +
      `<div class="x3-mini-tuile fam-${esc(tile.famille)}">` +
      `<div class="x3-mini-name">${esc(tp.nom_court || tile.id)}</div>` +
      `<div class="flex flex-wrap gap-1">${pictos}</div>` +
      (mcp.face_1 ? `<div class="x3-mini-kw-line"><strong>F1 :</strong> ${esc(mcp.face_1)}</div>` : '') +
      (mcp.face_2 ? `<div class="x3-mini-kw-line"><strong>F2 :</strong> ${esc(mcp.face_2)}</div>` : '') +
      (mcp.enracine ? `<div class="x3-mini-kw-line text-emerald-800"><strong>🌱 :</strong> ${esc(mcp.enracine)}</div>` : '') +
      `</div>` +
      `<div class="p-3 rounded-xl border border-slate-200 bg-white space-y-2">` +
      `<div class="x3-duel-title">${esc(cj.titre_complet || tp.nom_court || tile.id)}</div>` +
      `<div class="flex flex-wrap gap-1">${renderRoleBadges(tile, true)}</div>` +
      (cj.pitch_ambiance ? `<p class="x3-pitch">${esc(cj.pitch_ambiance)}</p>` : '') +
      `<div class="x3-rule-block"><div class="x3-rule-label">Face 1</div><div>${esc(tr.face_1 || '—')}</div></div>` +
      (tr.face_2 ? `<div class="x3-rule-block is-face2"><div class="x3-rule-label">Face 2</div><div>${esc(tr.face_2)}</div></div>` : '') +
      (tr.enracine ? `<div class="x3-rule-block is-enracine"><div class="x3-rule-label">🌱 Enraciné</div><div>${esc(tr.enracine)}</div></div>` : '') +
      `</div>`
    );
  }

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
    const w = uiState.workspace.slots[ed.slotId];
    const selPictos = Array.isArray(tp.pictogrammes) ? tp.pictogrammes : [];
    const roles = Array.isArray(t.roles_portes) ? t.roles_portes : [];

    const hybridRow = (lbl, sec) => (
      `<span class="inline-flex items-center gap-1 text-xs"><strong>${esc(lbl)} :</strong>` +
      PANEL_IDS.map(pid => `<button type="button" class="x3-btn x3-btn-sm" onclick="AmazoniaExplorerV63.importEditorFromPanel('${pid}', '${sec}')">${PANEL_SHORT[pid]}</button>`).join('') +
      `</span>`
    );

    const pictoPicker = Object.values(getPictosRef()).map(it => (
      `<button type="button" class="x3-picto-pick-btn ${selPictos.includes(it.code) ? 'is-selected' : ''}" title="${esc(it.libelle)}" onclick="AmazoniaExplorerV63.toggleEditorPicto('${esc(it.code)}')">${esc(it.symbole)}</button>`
    )).join('');

    return (
      `<div class="x3-modal-backdrop" id="x3-editor-modal" role="dialog" aria-modal="true" onclick="if(event.target===this) AmazoniaExplorerV63.closeEditor()">` +
      `<div class="x3-modal-panel" style="width:min(1180px,100%)">` +
      `<div class="x3-modal-head"><h3 class="x3-modal-title">✏️ Modifier / Hybrider — ${esc(ed.slotId)} (${esc(t.alias_oriente)})</h3><button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closeEditor()">✕ Fermer</button></div>` +
      `<div class="x3-modal-body">` +
      `<div class="p-2.5 rounded-lg bg-amber-50 border border-amber-200 flex flex-wrap items-center gap-3">` +
      `<span class="text-xs font-bold text-amber-900">🧬 Importer depuis un panel :</span>` +
      `${hybridRow('Tout', 'all')}${hybridRow('Face 1', 'face_1')}${isGardien ? hybridRow('Face 2', 'face_2') : ''}${hybridRow('Enraciné', 'enracine')}${hybridRow('Pitch', 'pitch')}${hybridRow('Dilemme', 'dilemma')}` +
      `</div>` +
      `<div class="x3-editor-layout">` +
      `<div class="space-y-3">` +
      `<div class="x3-form-section">` +
      `<div class="x3-two-cols">` +
      `<div class="x3-field"><label>Nom court ${isGardien ? '🔒' : ''}</label><input type="text" value="${esc(tp.nom_court || '')}" ${isGardien ? 'disabled' : ''} oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.nom_court', this.value)" /></div>` +
      `<div class="x3-field"><label>Titre complet</label><input type="text" value="${esc(cj.titre_complet || '')}" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.titre_complet', this.value)" /></div>` +
      `</div>` +
      `<div class="flex flex-wrap gap-3 items-center text-xs">` +
      `<select class="x3-select" onchange="AmazoniaExplorerV63.updateEditorField('nature', this.value)"><option value="ACTION" ${t.nature !== 'LOI_PASSIVE' ? 'selected' : ''}>✦ Action</option><option value="LOI_PASSIVE" ${t.nature === 'LOI_PASSIVE' ? 'selected' : ''}>⚖️ Loi passive</option></select>` +
      (isGardien ? `<select class="x3-select" onchange="AmazoniaExplorerV63.updateEditorField('tuile_plateau.icone_conseillee', this.value)">${GUARDIAN_ICONS.map(ic => `<option value="${ic.id}" ${tp.icone_conseillee === ic.id ? 'selected' : ''}>${ic.icon} ${esc(ic.label)}</option>`).join('')}</select>` : '') +
      `<label class="inline-flex items-center gap-1 font-semibold"><input type="checkbox" ${t.est_twist ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('TWIST_2K3', this.checked)" /> ⚡ Twist 2K3</label>` +
      (isGardien ? `<label class="inline-flex items-center gap-1 font-semibold"><input type="checkbox" ${roles.includes('CATALYSEUR_EVEIL') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('CATALYSEUR_EVEIL', this.checked)" /> ☀️ Éveil</label>` : '') +
      `<label class="inline-flex items-center gap-1 font-semibold"><input type="checkbox" ${roles.includes('LEVIER_REVE') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('LEVIER_REVE', this.checked)" /> 🌙 Rêve</label>` +
      `<label class="inline-flex items-center gap-1 font-semibold"><input type="checkbox" ${roles.includes('ENRACINEMENT') ? 'checked' : ''} onchange="AmazoniaExplorerV63.toggleEditorRole('ENRACINEMENT', this.checked)" /> 🌱 Enrac.</label>` +
      `</div>` +
      `<div class="x3-field"><label>Pictogrammes Mini-Tuile (${selPictos.length}/4)</label><div class="x3-picto-picker">${pictoPicker}</div></div>` +
      `<div class="x3-two-cols">` +
      `<div class="x3-field"><label>Mots-clés Face 1</label><input type="text" value="${esc(mcp.face_1 || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.face_1', this.value)" /></div>` +
      (isGardien ? `<div class="x3-field"><label>Mots-clés Face 2</label><input type="text" value="${esc(mcp.face_2 || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.face_2', this.value)" /></div>` : `<div class="x3-field"><label>Mots-clés Enraciné</label><input type="text" value="${esc(mcp.enracine || '')}" oninput="AmazoniaExplorerV63.updateEditorField('tuile_plateau.mots_cles_plateau.enracine', this.value)" /></div>`) +
      `</div>` +
      `</div>` +
      `<div class="x3-form-section">` +
      `<div class="x3-field"><label>Pitch d’ambiance</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.pitch_ambiance', this.value)">${esc(cj.pitch_ambiance || '')}</textarea></div>` +
      `<div class="x3-field"><label>Texte Face 1</label><textarea rows="4" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.face_1', this.value)">${esc(tr.face_1 || '')}</textarea></div>` +
      (isGardien ? `<div class="x3-field"><label>Texte Face 2 (autonome)</label><textarea rows="4" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.face_2', this.value)">${esc(tr.face_2 || '')}</textarea></div>` : '') +
      `<div class="x3-field"><label>Clause Enraciné (optionnelle)</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.texte_regle.enracine', this.value)">${esc(tr.enracine || '')}</textarea></div>` +
      `<div class="x3-two-cols">` +
      `<div class="x3-field"><label>🎯 Choix</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.decision_et_renoncement.choix', this.value)">${esc(dr.choix || '')}</textarea></div>` +
      `<div class="x3-field"><label>⚖️ Renoncement</label><textarea rows="2" oninput="AmazoniaExplorerV63.updateEditorField('carte_joueur.decision_et_renoncement.renoncement', this.value)">${esc(dr.renoncement || '')}</textarea></div>` +
      `</div>` +
      `</div>` +
      `</div>` +
      `<div class="space-y-3" id="x3-editor-live-preview">${renderEditorPreviewHtml(t)}</div>` +
      `</div>` +
      `</div>` +
      `<div class="x3-modal-foot">` +
      `<div>${w && w.is_modified ? `<button type="button" class="x3-btn x3-btn-danger" onclick="AmazoniaExplorerV63.restoreOriginalSlot('${esc(ed.slotId)}')">↺ Restaurer l’original</button>` : ''}</div>` +
      `<div class="flex gap-2"><button type="button" class="x3-btn" onclick="AmazoniaExplorerV63.closeEditor()">Annuler</button><button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.saveEditorToCanon()">💾 Enregistrer &amp; Garder</button></div>` +
      `</div></div></div>`
    );
  }

  function renderExportModal() {
    if (!uiState.exportModal) return '';
    const em = uiState.exportModal;
    const radar = computeHealthRadar('canon');
    const brief = buildGeminiMarkdownBrief(em.geminiScope || 'to_arbitrate');
    const comfortCls = brief.comfort === 'green' ? 'is-ok' : (brief.comfort === 'amber' ? 'is-warn' : 'is-err');

    const scopes = [
      { id: 'to_arbitrate', label: '🤔 À revoir' },
      { id: 'active_context', label: uiState.mode === 'simulator' ? '🎡 Table active' : '⚔️ Emplacement actif' },
      { id: 'notes_and_edits', label: '✏️ Notes & Hybrides' },
      { id: 'canon_summary', label: '📋 Synthèse Mon Canon' }
    ].map(sc => `<button type="button" class="x3-btn x3-btn-sm ${em.geminiScope === sc.id ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setExportGeminiScope('${sc.id}')">${esc(sc.label)}</button>`).join('');

    return (
      `<div class="x3-modal-backdrop" id="x3-export-modal" role="dialog" aria-modal="true" onclick="if(event.target===this) AmazoniaExplorerV63.closeExportModal()">` +
      `<div class="x3-modal-panel">` +
      `<div class="x3-modal-head"><h3 class="x3-modal-title">📤 Passerelles Gemini &amp; Antigravity</h3><button type="button" class="x3-tool-btn" onclick="AmazoniaExplorerV63.closeExportModal()">✕ Fermer</button></div>` +
      `<div class="x3-modal-body">` +
      `<div class="flex gap-2">` +
      `<button type="button" class="x3-btn x3-btn-sm ${em.tab === 'gemini' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setExportTab('gemini')">✨ Vers Gemini (Markdown)</button>` +
      `<button type="button" class="x3-btn x3-btn-sm ${em.tab === 'antigravity' ? 'x3-btn-primary' : ''}" onclick="AmazoniaExplorerV63.setExportTab('antigravity')">🚀 Vers Antigravity &amp; Sauvegarde JSON</button>` +
      `</div>` +
      (em.tab === 'gemini'
        ? `<div class="space-y-2.5">` +
          `<div class="flex flex-wrap items-center justify-between gap-2"><div class="flex flex-wrap gap-1.5">${scopes}</div><span class="x3-radar-pill ${comfortCls}" data-gemini-word-count="${brief.words}">~${brief.words} mots · ${brief.tileCount} tuile(s)</span></div>` +
          `<pre class="x3-export-preview">${esc(brief.markdown)}</pre>` +
          `<div class="flex justify-end"><button type="button" id="x3-btn-copy-md" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.copyGeminiBrief()">📋 Copier le Brief Markdown (~${brief.words} mots)</button></div>` +
          `</div>`
        : `<div class="space-y-3">` +
          `<div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2">` +
          `<div class="x3-section-label">1. Sauvegarde complète (contracts/panels/author_workspace_v6_3.json)</div>` +
          `<div class="flex flex-wrap gap-2">` +
          `<button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.downloadWorkspaceJson()">💾 Télécharger author_workspace_v6_3.json</button>` +
          `<input type="file" id="x3-workspace-import-input" accept=".json,application/json" class="hidden" onchange="AmazoniaExplorerV63.handleWorkspaceImport(event)" />` +
          `<button type="button" class="x3-btn" onclick="document.getElementById('x3-workspace-import-input').click()">📂 Importer author_workspace_v6_3.json</button>` +
          `</div></div>` +
          `<div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 space-y-2">` +
          `<div class="x3-section-label">2. Exporter tiles_canon_v6_3.json candidat (${radar.electedCount}/30 gardées)</div>` +
          (radar.electedCount < 30
            ? `<div class="flex items-center gap-2 text-xs"><span>Compléter les ${30 - radar.electedCount} non tranchées depuis :</span><select class="x3-select" onchange="AmazoniaExplorerV63.setExportFallbackPanel(this.value)">${PANEL_IDS.map(p => `<option value="${p}" ${em.fallbackPanel === p ? 'selected' : ''}>${PANEL_LABELS[p]}</option>`).join('')}</select></div>`
            : `<div class="text-xs text-emerald-800 font-semibold">✅ 30/30 emplacements gardés dans Mon Canon.</div>`) +
          `<button type="button" class="x3-btn x3-btn-primary" onclick="AmazoniaExplorerV63.downloadCandidateCanonJson()">🏆 Exporter tiles_canon_v6_3.json candidat</button>` +
          `</div></div>`) +
      `</div></div></div>`
    );
  }

  // --------------------------------------------------------------------------
  // Rendu Principal & Helpers IO
  // --------------------------------------------------------------------------
  function render() {
    ensureInitialized();
    const toolbarEl = document.getElementById('explorer-v6-3-toolbar') || document.getElementById('explorer-v6-2-toolbar');
    const gridEl = document.getElementById('catalogue-grid');
    if (!toolbarEl || !gridEl) return;

    const legacyFilters = document.getElementById('legacy-catalogue-filters');
    if (legacyFilters && legacyFilters.classList) legacyFilters.classList.add('hidden');
    const v62Banner = document.getElementById('v62-catalogue-banner');
    if (v62Banner && v62Banner.classList) v62Banner.classList.add('hidden');
    const oldToolbar = document.getElementById('explorer-v6-2-toolbar');
    if (oldToolbar && oldToolbar !== toolbarEl && oldToolbar.classList) oldToolbar.classList.add('hidden');

    let bodyHtml = '';
    if (uiState.mode === 'simulator') bodyHtml = renderSimulatorView();
    else if (uiState.mode === 'list') bodyHtml = renderListView();
    else bodyHtml = renderArbitrateDuelView();

    const modalsHtml = renderPictoGuideModal() + renderEditorModal() + renderExportModal();
    toolbarEl.innerHTML = `<div class="x3-shell">${renderTopBar()}</div>`;
    gridEl.innerHTML = `<div class="x3-shell">${bodyHtml}</div>${modalsHtml}`;
  }

  function copyTextRobust(text) {
    if (typeof navigator !== 'undefined' && navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        const p = navigator.clipboard.writeText(text);
        if (p && typeof p.catch === 'function') p.catch(() => fallbackCopySync(text));
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
    try { if (typeof document.execCommand === 'function') ok = document.execCommand('copy'); } catch (_err) { ok = false; }
    if (document.body && document.body.removeChild) document.body.removeChild(ta);
    return ok;
  }

  function downloadJsonFile(filename, payloadObj) {
    const jsonText = JSON.stringify(payloadObj, null, 2) + '\n';
    if (typeof Blob === 'undefined' || typeof URL === 'undefined' || typeof URL.createObjectURL !== 'function') return jsonText;
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

  // --------------------------------------------------------------------------
  // API Publique
  // --------------------------------------------------------------------------
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

    setMode(m) {
      ensureInitialized();
      uiState.mode = m;
      if (m !== 'list') uiState.activeDrawer = null;
      render();
    },

    openListView(src) {
      ensureInitialized();
      uiState.mode = 'list';
      uiState.listSource = src || 'canon';
      render();
    },

    toggleDrawer(name) {
      ensureInitialized();
      uiState.activeDrawer = (uiState.activeDrawer === name || !name) ? null : name;
      render();
    },

    setRadarTarget(src) {
      ensureInitialized();
      uiState.radarTarget = src;
      render();
    },

    toggleRadarDetail(k) {
      ensureInitialized();
      uiState.radarDetailKey = uiState.radarDetailKey === k ? null : k;
      render();
    },

    setIndexFilter(f) {
      ensureInitialized();
      uiState.indexFilter = f;
      render();
    },

    goToSlot(slotId) {
      ensureInitialized();
      if (!getSlotSpecMap()[slotId]) return;
      uiState.currentSlotId = slotId;
      uiState.mode = 'arbitrate';
      uiState.activeDrawer = null;
      render();
    },

    stepSlot(delta) {
      ensureInitialized();
      const specs = getSlotsSpec();
      const idx = specs.findIndex(s => s.id === uiState.currentSlotId);
      const next = (idx + delta + specs.length) % specs.length;
      uiState.currentSlotId = specs[next].id;
      render();
    },

    goToNextPending() {
      ensureInitialized();
      const specs = getSlotsSpec();
      const curIdx = specs.findIndex(s => s.id === uiState.currentSlotId);
      for (let off = 1; off <= specs.length; off++) {
        const cand = specs[(curIdx + off) % specs.length];
        const w = uiState.workspace.slots[cand.id];
        if (!w.selected_source || isSlotFlaggedReview(w)) {
          uiState.currentSlotId = cand.id;
          uiState.mode = 'arbitrate';
          render();
          return cand.id;
        }
      }
      return uiState.currentSlotId;
    },

    // Trio d'annotation : Garder · À revoir · Note
    keepSlot(slotId, sourceKey) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      if (sourceKey === 'custom' && !w.custom_tile) return;
      w.selected_source = w.selected_source === sourceKey ? null : sourceKey;
      if (PANEL_IDS.includes(sourceKey)) w.base_source = sourceKey;
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

    toggleSlotReview(slotId) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      if (!w) return;
      w.status = isSlotFlaggedReview(w) ? '' : 'HESITATION';
      w.updated_at = new Date().toISOString();
      saveWorkspaceToStorage();
      render();
    },

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
        hint._timer = setTimeout(() => hint.classList.remove('is-visible'), 1300);
      }
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

    // Filtres & Ressources
    setFilter(key, val) {
      ensureInitialized();
      uiState.filters[key] = val;
      if (uiState.mode !== 'list') uiState.mode = 'list';
      if (uiState.listSource === 'canon' && computeHealthRadar('canon').electedCount === 0) {
        uiState.listSource = 'panel_1';
      }
      render();
      if (key === 'search') {
        const inp = document.getElementById('x3-search-input');
        if (inp && typeof inp.focus === 'function') {
          inp.focus();
          if (typeof inp.setSelectionRange === 'function') {
            const len = String(val || '').length;
            inp.setSelectionRange(len, len);
          }
        }
      }
    },

    toggleFilterReviewOnly() {
      ensureInitialized();
      uiState.filters.reviewOnly = !uiState.filters.reviewOnly;
      uiState.mode = 'list';
      render();
    },

    setPictoFilter(picCode) {
      ensureInitialized();
      uiState.filters.picto = picCode || null;
      uiState.pictoGuideOpen = false;
      uiState.mode = 'list';
      if (uiState.listSource === 'canon' && computeHealthRadar('canon').electedCount === 0) {
        uiState.listSource = 'panel_1';
      }
      render();
    },

    resetFilters() {
      ensureInitialized();
      uiState.filters = { search: '', peuple: 'ALL', family: 'ALL', role: 'ALL', reviewOnly: false, picto: null };
      uiState.resourceFocus = null;
      uiState.resourceFocusSource = null;
      render();
    },

    focusResource(tok, sourceHint) {
      ensureInitialized();
      if (uiState.resourceFocus === tok && (!sourceHint || uiState.resourceFocusSource === sourceHint)) {
        uiState.resourceFocus = null;
        uiState.resourceFocusSource = null;
      } else {
        uiState.resourceFocus = tok;
        uiState.resourceFocusSource = sourceHint || (uiState.mode === 'list' ? uiState.listSource : 'panel_1');
      }
      render();
    },

    clearResourceFocus() {
      ensureInitialized();
      uiState.resourceFocus = null;
      uiState.resourceFocusSource = null;
      render();
    },

    // Simulateur de Table
    setSimSource(src) { ensureInitialized(); uiState.simSource = src; render(); },
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
      if (idx >= 0) { if (uiState.simPeuples.length <= 3) return; uiState.simPeuples.splice(idx, 1); }
      else uiState.simPeuples.push(code);
      uiState.simHighlightPeuple = null;
      render();
    },
    moveSimPeuple(code, delta) {
      ensureInitialized();
      const idx = uiState.simPeuples.indexOf(code);
      const nxt = idx + delta;
      if (idx < 0 || nxt < 0 || nxt >= uiState.simPeuples.length) return;
      const tmp = uiState.simPeuples[nxt]; uiState.simPeuples[nxt] = code; uiState.simPeuples[idx] = tmp;
      render();
    },
    toggleSimHighlight(code) {
      ensureInitialized();
      uiState.simHighlightPeuple = uiState.simHighlightPeuple === code ? null : code;
      render();
    },

    // Guide Pictos
    openPictoGuide() { ensureInitialized(); uiState.pictoGuideOpen = true; render(); },
    closePictoGuide() { ensureInitialized(); uiState.pictoGuideOpen = false; render(); },

    // Éditeur / Hybrideur
    openEditor(slotId, sourceHint) {
      ensureInitialized();
      const w = uiState.workspace.slots[slotId];
      const baseSource = PANEL_IDS.includes(sourceHint) ? sourceHint : (w.base_source || 'panel_1');
      const baseTile = (sourceHint === 'custom' && w.custom_tile)
        ? deepClone(w.custom_tile)
        : deepClone(getPanelTile(baseSource, slotId));
      if (!baseTile) return;
      uiState.editor = { slotId, baseSource, tile: baseTile };
      render();
    },
    closeEditor() { ensureInitialized(); uiState.editor = null; render(); },
    importEditorFromPanel(panelId, section) {
      ensureInitialized();
      if (!uiState.editor) return;
      const src = getPanelTile(panelId, uiState.editor.slotId);
      if (!src) return;
      const t = uiState.editor.tile;
      if (section === 'all') { uiState.editor.tile = deepClone(src); uiState.editor.baseSource = panelId; }
      else if (section === 'face_1') { t.carte_joueur.texte_regle.face_1 = src.carte_joueur.texte_regle.face_1; t.tuile_plateau.mots_cles_plateau.face_1 = src.tuile_plateau.mots_cles_plateau.face_1; }
      else if (section === 'face_2') { t.carte_joueur.texte_regle.face_2 = src.carte_joueur.texte_regle.face_2; t.tuile_plateau.mots_cles_plateau.face_2 = src.tuile_plateau.mots_cles_plateau.face_2; }
      else if (section === 'enracine') { t.carte_joueur.texte_regle.enracine = src.carte_joueur.texte_regle.enracine; t.tuile_plateau.mots_cles_plateau.enracine = src.tuile_plateau.mots_cles_plateau.enracine; }
      else if (section === 'pitch') { t.carte_joueur.titre_complet = src.carte_joueur.titre_complet; t.carte_joueur.pitch_ambiance = src.carte_joueur.pitch_ambiance; }
      else if (section === 'dilemma') { t.carte_joueur.decision_et_renoncement = deepClone(src.carte_joueur.decision_et_renoncement); }
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
      cur[last] = last === 'enracine' ? (String(val || '').trim() ? val : null) : val;
      if (path === 'nature') {
        const r = new Set(uiState.editor.tile.roles_portes || []);
        if (val === 'LOI_PASSIVE') r.add('LOI_PASSIVE'); else r.delete('LOI_PASSIVE');
        uiState.editor.tile.roles_portes = Array.from(r);
      }
      const prev = document.getElementById('x3-editor-live-preview');
      if (prev) prev.innerHTML = renderEditorPreviewHtml(uiState.editor.tile);
    },
    toggleEditorRole(roleCode, checked) {
      ensureInitialized();
      if (!uiState.editor) return;
      const t = uiState.editor.tile;
      const r = new Set(t.roles_portes || []);
      if (checked) r.add(roleCode); else r.delete(roleCode);
      if (roleCode === 'TWIST_2K3') t.est_twist = Boolean(checked);
      t.roles_portes = Array.from(r);
      const prev = document.getElementById('x3-editor-live-preview');
      if (prev) prev.innerHTML = renderEditorPreviewHtml(t);
    },
    toggleEditorPicto(picCode) {
      ensureInitialized();
      if (!uiState.editor) return;
      const list = (uiState.editor.tile.tuile_plateau.pictogrammes || []).slice();
      const idx = list.indexOf(picCode);
      if (idx >= 0) list.splice(idx, 1);
      else { if (list.length >= 4) list.shift(); list.push(picCode); }
      uiState.editor.tile.tuile_plateau.pictogrammes = list;
      render();
    },
    saveEditorToCanon() {
      ensureInitialized();
      if (!uiState.editor) return;
      const { slotId, baseSource, tile } = uiState.editor;
      const w = uiState.workspace.slots[slotId];
      w.custom_tile = sanitizeTileForCanonExport(tile, getSlotSpecMap()[slotId]);
      w.is_modified = true;
      w.selected_source = 'custom';
      w.base_source = baseSource;
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
      if (w.selected_source === 'custom') w.selected_source = w.base_source || 'panel_1';
      w.updated_at = new Date().toISOString();
      uiState.editor = null;
      saveWorkspaceToStorage();
      render();
    },

    // Exports & Imports
    openExportModal(tab) {
      ensureInitialized();
      uiState.exportModal = { tab: tab === 'antigravity' ? 'antigravity' : 'gemini', geminiScope: 'to_arbitrate', fallbackPanel: 'panel_1' };
      render();
    },
    closeExportModal() { ensureInitialized(); uiState.exportModal = null; render(); },
    setExportTab(t) { if (uiState.exportModal) { uiState.exportModal.tab = t; render(); } },
    setExportGeminiScope(sc) { if (uiState.exportModal) { uiState.exportModal.geminiScope = sc; render(); } },
    setExportFallbackPanel(p) { if (uiState.exportModal) { uiState.exportModal.fallbackPanel = p; render(); } },
    copyGeminiBrief() {
      ensureInitialized();
      const scope = (uiState.exportModal && uiState.exportModal.geminiScope) || 'to_arbitrate';
      const b = buildGeminiMarkdownBrief(scope);
      copyTextRobust(b.markdown);
      const btn = document.getElementById('x3-btn-copy-md');
      if (btn) {
        btn.textContent = `✅ Brief copié (~${b.words} mots)`;
        setTimeout(() => { btn.textContent = `📋 Copier le Brief Markdown (~${b.words} mots)`; }, 2000);
      }
      return b;
    },
    downloadWorkspaceJson() { return downloadJsonFile('author_workspace_v6_3.json', buildAuthorWorkspaceExport()); },
    downloadCandidateCanonJson() { return downloadJsonFile('tiles_canon_v6_3.json', buildCandidateCanonV63((uiState.exportModal && uiState.exportModal.fallbackPanel) || 'panel_1')); },
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
          api.importWorkspaceObject(JSON.parse(String(e.target.result || '')));
          if (typeof global.showToast === 'function') global.showToast('Atelier importé', `${file.name} chargé dans Mon Canon v6.3.`);
        } catch (err) {
          if (typeof global.showToast === 'function') global.showToast('Import invalide', err.message);
        } finally { event.target.value = ''; }
      };
      reader.readAsText(file, 'utf-8');
    },

    getFilteredSelection() {
      ensureInitialized();
      const sid = uiState.currentSlotId;
      const selected = {};
      if (uiState.mode === 'list') {
        const tm = getTilesMapForSource(uiState.listSource);
        getFilteredSlotIds().forEach(id => { if (tm[id]) selected[id] = tm[id]; });
      } else {
        PANEL_IDS.forEach(pid => {
          const t = getPanelTile(pid, sid);
          if (t) selected[`${sid}_${pid}`] = t;
        });
      }
      return { isUnfiltered: false, profileCount: Object.keys(selected).length, selected };
    }
  };

  global.AmazoniaExplorerV63 = api;
})(typeof window !== 'undefined' ? window : globalThis);
