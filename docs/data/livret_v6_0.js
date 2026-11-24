// =========================================================================
// data/livret_v6_0.js — Livret de Règles Modulaire & Synthèse Cœur (Amazonia)
// Architecture modulaire (Tronc commun + 3 Modules + Asymétrie 3+3 + 22 Invariants)
// =========================================================================

const LIVRET_SCHEMA_VERSION = "6.2.0";

const REGLES_COEUR_SYNTHESE = {
  "schema_version": "6.2.0",
  "but_et_format": "Jeu coopératif asymétrique à communication muette (3 à 6 joueurs parmi Humains, Entités Magiques, Mammifères, Reptiles, Oiseaux, Insectes ; 8 tours maximum répartis en 2 Actes). Objectif commun : maximiser le pourcentage et le nombre d'Arbres debout à la fin de la partie (après application des tuiles enracinées) ou remporter une fin anticipée (Sommeil du Contremaître ou Éveil de la Forêt aux Tours 1 à 7). Matériel fini recto-verso : 10 × N pions uniques Arbre debout / Souche (zéro réserve illimitée) et jetons Puissance réversibles Rouge (+1) / Bleu Surchauffe (−1).",
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve ou Nid) est gouvernée exclusivement par le joueur de son Peuple d'origine ; la pose d'un Piège gagné en Furtivité est décidée par le propriétaire du rayon ; le Bouclier de lisière est facultatif et gouverné par le joueur Insectes. Zéro vote collectif.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés. Tous les joueurs lancent leurs dés sous paravent (même sur Sabotage ou Écaille, jet ignoré) pour éliminer toute fuite sonore.",
    "quatre_lois_physiques": "1) Une parcelle désigne uniquement une case non devenue Route Forestière ; les Routes sont sautées radialement comme un pont et infranchissables latéralement (rayon 100 % Route = Furtivité fermée). 2) Maximum 1 Piège ordinaire autonome par parcelle (pare 1 frappe puis est défaussé aussitôt ; le Croc Reptile peut cohabiter et pare en premier). 3) Une machine en Ratissage ne se déplace jamais, mais sa parcelle compte comme parcelle ciblée tant qu'elle n'a pas frappé ce tour. 4) Zéro écrasement au contact hors Route et zéro réservation d'avance : seule la création d'une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve) et replie les machines vers la bordure (ou d'1 parcelle vers le cœur si la bordure est rasée, ce qui couvre l'avancée de En avançant).",
    "cascades_gardiens_6_icones": "Terminez intégralement l'action ou la tuile en cours avant de balayer la Piste des Gardiens de gauche à droite sur les 6 icônes dédiées sans numéros : [Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance]. Partition stricte « 1 événement = au plus 1 icône » ; Résonance occupe la 6e position avec compteur individuel sans écrasement des 1res activations d'autres Gardiens du tour, et le balayage gauche → droite reprend si un effet rallume une icône plus à gauche."
  },
  "architecture_modulaire": {
    "tronc_commun": "Forêt finie 10 × N (4 parcelles gravées 2–2–3–3, départ décalé Bulldozer en parcelle 1 / Abatteuse en parcelle 2), sac opaque de jetons épais (2N Machines + Sabotages + jusqu'à 4 Écailles), Réglette fixe 1–6 à bandelette d'Acte réversible (Face A / Face B retournée seule au début du Tour 5), 2 Défenseurs recto-verso (Réflexion / Définitif), Furtivité Chaud vs Calme par rayon, Pièges autonomes, Seuil unifié avec bleus actifs en tous modes, Ratissage à +1 jeton rouge physique, Enracinement volontaire et score final.",
    "module_gardiens": "Actif dès qu'au moins un Peuple Animal Sauvage (Mammifères, Reptiles ou Oiseaux) joue : Piste des Gardiens à 6 icônes avec Résonance en 6e position, 2 encoches visibles par Gardien, paris 0/1/2 Défenseurs, passage Face 2 sur pari gagné et Éveil de la Forêt.",
    "module_reves": "Actif dès qu'au moins un Peuple Onirique (Humains ou Entités Magiques) joue : pose de Rêves à droite de la Réglette sans déplacer les Insectes, défense dès le premier déploiement, annulation choisie par le propriétaire du Rêve, Défenseurs solidaires lors des glissements et Sommeil du Contremaître (bloqué si un Rêve est enraciné).",
    "module_essaim": "Actif uniquement si les Insectes jouent : jetons Insectes laissés dans la boîte sans ce Peuple ; Nids et Production (+1/+2 sans allumer l'icône Insecte), Migration radiale dans les deux sens et vers les pistes centrales, Déviation ±1 à l'Ouverture, Parade Insecte, Bouclier de lisière facultatif gouverné par les Insectes et descente sur place au Ménage d'un Insecte passager."
  },
  "sequence_tour_6_etapes": {
    "preparation": "Début du Tour 5 uniquement : retournez la seule bandelette d'Acte sur Face B (sans toucher aux Rêves ni aux Insectes). Pioche secrète d'1 jeton dans le sac opaque (pénurie en sens horaire depuis le Coordonnateur, Oiseau toujours servi en dernier avec regard sur 2 jetons et pose du second sur son Perchoir de Vigie). Lancer de dés universel sous mini-paravent gradué 1–6 par tous les joueurs même sur Sabotage ou Écaille.",
    "deploiement": "Premier déploiement simultané directement face Définitif (sa forêt, ses 2 lisières non inplaçables, toute rive ouverte de Furtivité d'un rayon actif ou tout Rêve en jeu ; jamais sur les Gardiens ; repli sur parcelle alliée si aucun emplacement légal). Second déploiement face Réflexion partout (Gardiens inclus, 0/1/2 Défenseurs max par Gardien) puis validation irréversible sur Définitif (figeant Duel ou Plume de Vigie) ; clôture à N−1 joueurs validés (au plus 1 ultime ajustement pour le dernier joueur).",
    "ouverture_et_constructions": "Constructions obligatoires en lisière à 2 bâtisseurs (couchés en attente ; bonus 3 joueurs libérant 1 bâtisseur sur Gardien/Rêve sauf 2 rayons adjacents rasés). Ouverture simultanée des paravents : jetons Machine visibles devant leur rayon jusqu'à la Furtivité (inclinés à 90° si annulés ; retrait d'une éventuelle Altération → recul d'1 parcelle sans frappe). Séquence stricte : Sabotages/Écailles un par un (+ pose Croc + balayage) → déviations Insecte ±1 une par une (+ balayage) → Rêves défendus de gauche à droite (le propriétaire choisit les machines annulées y compris déviées, résout le pouvoir du Rêve, puis allume l'icône Rêve + balayage si ≥ 1 machine annulée).",
    "furtivite_et_essaim": "Furtivité par rayon actif selon m(r) = jetons Machine visibles du rayon (droits ou inclinés) + Ratissages du rayon : Rive Piège gagnée si m(r) = 2 (propriétaire pose 1 Piège), Rive Sabotage gagnée si m(r) = 0 (+1 Sabotage au sac), puis pions couchés en attente. Si les Insectes jouent : Production des Nids défendus (+1/+2, bloc indivisible) puis Migration radiale double sens rayon par rayon (et sortie vers rang 1–6 ou icône Gardien depuis la dernière parcelle).",
    "attaques_et_verdict": "Rangs 1 à 6 puis Ratissage (Abatteuse avant Bulldozer). Parcelles ciblées figées au début de l'activation (cible devenue Route = annulée sans report ; poussée de bordure couvrant l'avancée En avançant). Seuil de Parade = chiffre gravé + rouges (Assaut et Ratissage uniquement ; ignorés en Charge) − bleus Surchauffe (actifs dans tous les modes) − 1 aux rangs 3 et 6, minimum 1. Chaîne à 2 maillons : Croc puis Piège autonome (icône Piégeage) sinon Parade classique (Défenseurs seuls → Parade ; avec Insectes défaussés → Insecte). En Charge : +1 jeton rouge max/activation dès qu'au moins 1 frappe sur parcelle réelle n'est ni parée ni piégée. Verdict des paris Gardiens (2 encoches visibles ; Bouclier de lisière facultatif) puis test de fin de partie (priorité Tour 8, puis Sommeil avant Éveil aux Tours 1–7).",
    "menage_et_enracinement": "Retour des Défenseurs en main, descente sur place d'un Insecte passager non dépensé, Enracinement volontaire (max 1 tuile construite/joueur/tour au pied de son rayon : 1 Souche F1/unique ou 2 Souches F2 au décompte final ; Rêve enraciné rend le Sommeil impossible), passage en Ratissage sur dernière parcelle (jeton Machine glissé dessous hors sac, conservation des jetons antérieurs + gain d'1 jeton rouge physique), remise au sac des jetons révélés et du Perchoir, passage du Coordonnateur et tour suivant."
  },
  "accessoires_3_plus_3": {
    "actifs_tour_1": "Humains (2 Chamanes recto-verso uniques : 1 Tambour et 1 Chant), Mammifères (1 jeton Duel Défi ↔ Territoire tenu), Oiseaux (Dé d'Envol 1–6, Perchoir de Vigie à plat, Plume de Vigie Chaud ↔ Calme).",
    "progressifs_tuiles": "Entités Magiques (jetons d'Altération sur machine mobile, max 1), Reptiles (4 jetons Écaille, 1 Croc réutilisable, max 1 cale sous machine mobile), Insectes (Module Essaim clos sur les 10 tuiles des 5 lisières des Insectes)."
  }
};

const LIVRET_ALL_PEUPLES = ['H', 'E', 'M', 'R', 'O', 'I'];

const LIVRET_PRESETS = [
  {
    id: 'decouverte',
    label: 'Découverte sans Insectes',
    badge: 'H · M · O',
    peuples: ['H', 'M', 'O']
  },
  {
    id: 'sans_animaux',
    label: 'Table sans Animaux',
    badge: 'H · E · I',
    peuples: ['H', 'E', 'I']
  },
  {
    id: 'sans_reves',
    label: 'Table sans Rêves',
    badge: 'M · R · O · I',
    peuples: ['M', 'R', 'O', 'I']
  },
  {
    id: 'complete_6j',
    label: 'Table complète',
    badge: '6J',
    peuples: ['H', 'E', 'M', 'R', 'O', 'I']
  }
];

const _livretFilterState = {
  mode: 'COMPLET', // 'COMPLET' | 'TABLE'
  peuples: LIVRET_ALL_PEUPLES.slice()
};

function _normalizeLivretPeoples(rawList) {
  if (!Array.isArray(rawList)) return [];
  const seen = new Set();
  const out = [];
  for (let i = 0; i < rawList.length; i++) {
    const code = String(rawList[i] || '').toUpperCase().trim();
    if (LIVRET_ALL_PEUPLES.includes(code) && !seen.has(code)) {
      seen.add(code);
      out.push(code);
    }
  }
  return out;
}

function _computeLivretActiveModules(mode, peuplesList) {
  if (mode !== 'TABLE') {
    return { GARDIENS: true, REVES: true, ESSAIM: true };
  }
  const active = _normalizeLivretPeoples(peuplesList);
  return {
    GARDIENS: active.some(p => p === 'M' || p === 'R' || p === 'O'),
    REVES: active.some(p => p === 'H' || p === 'E'),
    ESSAIM: active.includes('I')
  };
}

function _syncLivretDomVisibility() {
  if (typeof document === 'undefined' || !document) return;
  const article = typeof document.getElementById === 'function'
    ? document.getElementById('rulebook-article')
    : null;
  if (!article || typeof article.querySelectorAll !== 'function') return;

  const isTable = _livretFilterState.mode === 'TABLE';
  const activePeoples = isTable ? _livretFilterState.peuples : LIVRET_ALL_PEUPLES;
  const mods = _computeLivretActiveModules(_livretFilterState.mode, activePeoples);

  const modNodes = article.querySelectorAll('[data-module]');
  for (let i = 0; i < modNodes.length; i++) {
    const el = modNodes[i];
    const mName = el && typeof el.getAttribute === 'function' ? el.getAttribute('data-module') : null;
    if (!mName || typeof mods[mName] === 'undefined') continue;
    const visible = Boolean(mods[mName]);
    el.hidden = !visible;
    if (el.classList) {
      if (visible) {
        el.classList.remove('hidden', 'livret-hidden');
      } else {
        el.classList.add('hidden', 'livret-hidden');
      }
    }
    if (typeof el.setAttribute === 'function') {
      el.setAttribute('data-module-active', visible ? 'true' : 'false');
    }
  }

  const peupleNodes = article.querySelectorAll('[data-peuple]');
  for (let i = 0; i < peupleNodes.length; i++) {
    const el = peupleNodes[i];
    const pCode = el && typeof el.getAttribute === 'function' ? el.getAttribute('data-peuple') : null;
    if (!pCode) continue;
    const visible = !isTable || activePeoples.includes(pCode);
    el.hidden = !visible;
    if (el.classList) {
      if (visible) {
        el.classList.remove('hidden', 'livret-hidden');
      } else {
        el.classList.add('hidden', 'livret-hidden');
      }
    }
    if (typeof el.setAttribute === 'function') {
      el.setAttribute('data-peuple-active', visible ? 'true' : 'false');
    }
  }
}

function _rerenderLivretAfterFilterChange() {
  if (typeof document === 'undefined') return;
  if (typeof refreshAllUI === 'function') {
    refreshAllUI();
  } else if (typeof renderDidacticRulebook === 'function') {
    renderDidacticRulebook();
  }
  _syncLivretDomVisibility();
}

function getLivretFilterState() {
  const activePeoples = _livretFilterState.mode === 'TABLE'
    ? _livretFilterState.peuples.slice()
    : LIVRET_ALL_PEUPLES.slice();
  return {
    mode: _livretFilterState.mode,
    peuples: activePeoples,
    activeModules: _computeLivretActiveModules(_livretFilterState.mode, activePeoples)
  };
}

function setLivretTablePeoples(peuplesList) {
  const clean = _normalizeLivretPeoples(peuplesList);
  if (clean.length < 3 || clean.length > 6) {
    if (typeof showToast === 'function' && typeof document !== 'undefined') {
      showToast('Sélection de table invalide', 'Choisissez entre 3 et 6 Peuples autour de la table.');
    }
    return getLivretFilterState();
  }
  _livretFilterState.mode = 'TABLE';
  _livretFilterState.peuples = clean.slice();
  if (typeof state !== 'undefined' && state && Array.isArray(state.peuplesCercle)) {
    state.peuplesCercle = clean.slice();
  }
  _rerenderLivretAfterFilterChange();
  return getLivretFilterState();
}

function toggleLivretPeuple(code) {
  const upper = String(code || '').toUpperCase().trim();
  if (!LIVRET_ALL_PEUPLES.includes(upper)) return getLivretFilterState();

  let current;
  if (_livretFilterState.mode !== 'TABLE') {
    current = LIVRET_ALL_PEUPLES.slice();
  } else {
    current = _livretFilterState.peuples.slice();
  }

  const idx = current.indexOf(upper);
  if (idx >= 0) {
    if (current.length <= 3) {
      if (typeof showToast === 'function' && typeof document !== 'undefined') {
        showToast('Minimum 3 joueurs', 'Une table d’Amazonia compte toujours entre 3 et 6 Peuples.');
      }
      _rerenderLivretAfterFilterChange();
      return getLivretFilterState();
    }
    current.splice(idx, 1);
  } else {
    current.push(upper);
  }

  _livretFilterState.mode = 'TABLE';
  _livretFilterState.peuples = current;
  if (typeof state !== 'undefined' && state && Array.isArray(state.peuplesCercle)) {
    state.peuplesCercle = current.slice();
  }
  _rerenderLivretAfterFilterChange();
  return getLivretFilterState();
}

function resetLivretComplet() {
  _livretFilterState.mode = 'COMPLET';
  _livretFilterState.peuples = LIVRET_ALL_PEUPLES.slice();
  if (typeof state !== 'undefined' && state && Array.isArray(state.peuplesCercle)) {
    state.peuplesCercle = LIVRET_ALL_PEUPLES.slice();
  }
  _rerenderLivretAfterFilterChange();
  return getLivretFilterState();
}

function activateLivretTableMode() {
  const fallback = (typeof state !== 'undefined' && state && Array.isArray(state.peuplesCercle) && state.peuplesCercle.length >= 3)
    ? state.peuplesCercle.slice()
    : ['H', 'M', 'O'];
  return setLivretTablePeoples(fallback);
}

if (typeof globalThis !== 'undefined') {
  globalThis.LIVRET_SCHEMA_VERSION = LIVRET_SCHEMA_VERSION;
  globalThis.setLivretTablePeoples = setLivretTablePeoples;
  globalThis.toggleLivretPeuple = toggleLivretPeuple;
  globalThis.resetLivretComplet = resetLivretComplet;
  globalThis.activateLivretTableMode = activateLivretTableMode;
  globalThis.getLivretFilterState = getLivretFilterState;
}
if (typeof window !== 'undefined') {
  window.LIVRET_SCHEMA_VERSION = LIVRET_SCHEMA_VERSION;
  window.setLivretTablePeoples = setLivretTablePeoples;
  window.toggleLivretPeuple = toggleLivretPeuple;
  window.resetLivretComplet = resetLivretComplet;
  window.activateLivretTableMode = activateLivretTableMode;
  window.getLivretFilterState = getLivretFilterState;
}

function _livretModAttrs(moduleName, isVisible, extraClasses) {
  const cls = `${extraClasses || ''}${isVisible ? '' : ' hidden livret-hidden'}`.trim();
  const hid = isVisible ? '' : ' hidden';
  return `data-module="${moduleName}" data-module-active="${isVisible ? 'true' : 'false'}"${hid}${cls ? ` class="${cls}"` : ''}`;
}

function _livretPeupleAttrs(code, isVisible, extraClasses) {
  const cls = `${extraClasses || ''}${isVisible ? '' : ' hidden livret-hidden'}`.trim();
  const hid = isVisible ? '' : ' hidden';
  return `data-peuple="${code}" data-peuple-active="${isVisible ? 'true' : 'false'}"${hid}${cls ? ` class="${cls}"` : ''}`;
}

function _buildFallbackPeuplesMap() {
  return {
    H: { code: 'H', nom: 'Humains', icon: '🏹', famille: 'Onirique (Rêve)' },
    E: { code: 'E', nom: 'Entités Magiques', icon: '✨', famille: 'Onirique (Rêve)' },
    M: { code: 'M', nom: 'Mammifères', icon: '🐆', famille: 'Animal Sauvage (Gardien)' },
    R: { code: 'R', nom: 'Reptiles', icon: '🐍', famille: 'Animal Sauvage (Gardien)' },
    O: { code: 'O', nom: 'Oiseaux', icon: '🦜', famille: 'Animal Sauvage (Gardien)' },
    I: { code: 'I', nom: 'Insectes', icon: '🐜', famille: 'Symbiotique (Essaim)' }
  };
}

function renderDidacticRulebook() {
  if (typeof document === 'undefined') return '';

  const peuplesMap = (typeof PEUPLES !== 'undefined' && PEUPLES) ? PEUPLES : _buildFallbackPeuplesMap();
  const hasStudioState = typeof state !== 'undefined' && state && Array.isArray(state.peuplesCercle);

  // Synchroniser le filtre Table avec le cercle Studio lorsqu'on est en mode TABLE
  if (_livretFilterState.mode === 'TABLE' && hasStudioState && state.peuplesCercle.length >= 3) {
    _livretFilterState.peuples = _normalizeLivretPeoples(state.peuplesCercle);
  }

  const isTableMode = _livretFilterState.mode === 'TABLE';
  const tablePeoples = isTableMode
    ? _livretFilterState.peuples.slice()
    : (hasStudioState && state.peuplesCercle.length >= 3
      ? _normalizeLivretPeoples(state.peuplesCercle)
      : LIVRET_ALL_PEUPLES.slice());

  // En mode COMPLET (par défaut), les 3 modules et les 6 Peuples sont tous affichés.
  // En mode TABLE, seuls les modules et Peuples actifs autour de la table choisie sont affichés.
  const filterPeoples = isTableMode ? tablePeoples : LIVRET_ALL_PEUPLES;
  const visibleModules = _computeLivretActiveModules(_livretFilterState.mode, filterPeoples);
  const showGardiens = visibleModules.GARDIENS;
  const showReves = visibleModules.REVES;
  const showEssaim = visibleModules.ESSAIM;

  const isPeupleVisible = (code) => !isTableMode || filterPeoples.includes(code);
  const showGroupTour1 = isPeupleVisible('H') || isPeupleVisible('M') || isPeupleVisible('O');
  const showGroupProgressif = isPeupleVisible('E') || isPeupleVisible('R') || isPeupleVisible('I');

  // Données de la table active pour les éléments dynamiques (N joueurs, Arbres, Lisières)
  const n = tablePeoples.length;
  const topoSpec = (typeof TOPOLOGIES_PISTE_SPEC !== 'undefined' && TOPOLOGIES_PISTE_SPEC.P4_2233)
    ? TOPOLOGIES_PISTE_SPEC.P4_2233
    : { code: 'P4_2233', p_max: 4, dotation: [2, 2, 3, 3], somme: 10, arbres_par_rayon: 10 };
  const pMax = topoSpec.p_max || 4;
  const arbresParRayon = topoSpec.arbres_par_rayon || topoSpec.somme || 10;
  const totalArbres = n * arbresParRayon;
  const dotationStr = (topoSpec.dotation || [2, 2, 3, 3]).join(' – ');

  const tableNbAnimaux = tablePeoples.filter(p => p === 'M' || p === 'R' || p === 'O').length;
  const tableGardiensActif = tableNbAnimaux >= 1;
  const tableNbOniriques = tablePeoples.filter(p => p === 'H' || p === 'E').length;
  const tableNbReves = 2 * tableNbOniriques;
  const tableEssaimActif = tablePeoples.includes('I');

  const configNum = typeof computeConfigurationIndex === 'function' ? computeConfigurationIndex() : 1;
  const totalConfigs = (typeof CHASSIS_AXES_SPEC !== 'undefined' && Array.isArray(CHASSIS_AXES_SPEC))
    ? CHASSIS_AXES_SPEC.reduce((acc, ax) => acc * (ax.options ? ax.options.length : 1), 1)
    : 1;

  // Lisières actives pour la table courante
  let lisieres = [];
  if (typeof getActiveLisieresAndTiles === 'function' && hasStudioState) {
    lisieres = getActiveLisieresAndTiles().lisieres || [];
  } else if (typeof MATRICE_PAIRES !== 'undefined') {
    for (let i = 0; i < tablePeoples.length; i++) {
      const p1 = tablePeoples[i];
      const p2 = tablePeoples[(i + 1) % tablePeoples.length];
      lisieres.push({ index: i + 1, p1, p2, tuiles: MATRICE_PAIRES[`${p1}_${p2}`] || [] });
    }
  }

  const tableSummary = tablePeoples
    .map(code => `${peuplesMap[code].icon} ${peuplesMap[code].nom}`)
    .join(' · ');

  const presetKeyNow = tablePeoples.slice().sort().join(',');

  const presetsHtml = LIVRET_PRESETS.map(pr => {
    const prKey = pr.peuples.slice().sort().join(',');
    const isActivePreset = isTableMode && presetKeyNow === prKey;
    const argsJs = JSON.stringify(pr.peuples).replace(/"/g, "'");
    return `
      <button type="button" onclick="setLivretTablePeoples(${argsJs})" class="livret-preset-btn ${isActivePreset ? 'livret-preset-btn-active' : ''}">
        <span class="font-semibold">${pr.label}</span>
        <span class="livret-preset-tag">${pr.badge}</span>
      </button>
    `;
  }).join('');

  const checkboxesHtml = LIVRET_ALL_PEUPLES.map(code => {
    const p = peuplesMap[code];
    const checked = isTableMode ? tablePeoples.includes(code) : true;
    const checkedAttr = checked ? ' checked' : '';
    return `
      <label class="livret-peuple-chip ${checked ? 'livret-peuple-chip-on' : 'livret-peuple-chip-off'}">
        <input type="checkbox" value="${code}"${checkedAttr} onclick="toggleLivretPeuple('${code}')" class="rounded text-emerald-700 focus:ring-emerald-600" />
        <span>${p.icon} <strong>${p.nom}</strong> <span class="text-[10px] opacity-75">(${code})</span></span>
      </label>
    `;
  }).join('');

  const lisieresRowsHtml = lisieres.map(l => (l.tuiles || []).map((tId, idx) => {
    const t = (typeof CATALOGUE_TUILES !== 'undefined' && CATALOGUE_TUILES[tId]) ? CATALOGUE_TUILES[tId] : null;
    if (!t) return '';
    const pLetter = (hasStudioState && state.profileOverrides && state.profileOverrides[tId]) || 'A';
    const prof = (t.profils && (t.profils[pLetter] || t.profils.A)) || { nom: tId, texte: '' };
    const famLabel = t.famille === 'GARDIEN'
      ? '<span class="px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 font-semibold">Gardien</span>'
      : t.famille === 'REVE'
        ? '<span class="px-1.5 py-0.5 rounded bg-purple-100 text-purple-900 font-semibold">Rêve</span>'
        : '<span class="px-1.5 py-0.5 rounded bg-lime-100 text-lime-900 font-semibold">Nid</span>';
    const origObj = peuplesMap[t.origine];
    const origName = origObj ? `${origObj.icon} ${origObj.nom}` : t.origine;
    return `
      <tr class="hover:bg-slate-50">
        ${idx === 0 ? `<td rowspan="2" class="p-2.5 font-bold bg-slate-50 border-r border-slate-200 align-middle whitespace-nowrap">Lisière ${l.index}<br><span class="text-forest-700">${peuplesMap[l.p1].icon} ${peuplesMap[l.p1].nom} ↔ ${peuplesMap[l.p2].icon} ${peuplesMap[l.p2].nom}</span></td>` : ''}
        <td class="p-2.5 align-top whitespace-nowrap">
          <div class="font-bold text-slate-900">${prof.nom}</div>
          <div class="mt-1">${famLabel}</div>
        </td>
        <td class="p-2.5 align-top whitespace-nowrap font-medium text-forest-800">${origName}</td>
        <td class="p-2.5 align-top text-slate-700 leading-relaxed">${prof.texte}</td>
      </tr>
    `;
  }).join('')).join('');

  const html = `
    <style id="livret-v62-styles">
      .livret-hidden,
      [data-module][hidden],
      [data-peuple][hidden] {
        display: none !important;
      }
      .livret-config-banner {
        background: linear-gradient(135deg, #f0fdf4 0%, #f8fafc 60%, #fffbeb 100%);
        border: 2px solid #86efac;
        border-radius: 1rem;
        padding: 1rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.05);
      }
      .livret-mode-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.45rem 0.9rem;
        border-radius: 0.65rem;
        font-size: 0.78rem;
        font-weight: 700;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: #334155;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .livret-mode-btn:hover {
        border-color: #16a34a;
        color: #14532d;
      }
      .livret-mode-btn-active {
        background: #14532d;
        border-color: #14532d;
        color: #ffffff;
        box-shadow: 0 1px 4px rgba(20, 83, 45, 0.25);
      }
      .livret-mode-btn-active:hover {
        color: #ffffff;
      }
      .livret-preset-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.7rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        border: 1px solid #cbd5e1;
        background: #ffffff;
        color: #1e293b;
        cursor: pointer;
        transition: all 0.15s ease;
      }
      .livret-preset-btn:hover {
        border-color: #059669;
        background: #ecfdf5;
      }
      .livret-preset-btn-active {
        border-color: #047857;
        background: #d1fae5;
        color: #064e3b;
      }
      .livret-preset-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.65rem;
        padding: 0.05rem 0.35rem;
        border-radius: 9999px;
        background: #f1f5f9;
        color: #475569;
      }
      .livret-peuple-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        padding: 0.35rem 0.65rem;
        border-radius: 0.6rem;
        font-size: 0.76rem;
        border: 1px solid #cbd5e1;
        cursor: pointer;
        user-select: none;
        transition: all 0.15s ease;
      }
      .livret-peuple-chip-on {
        background: #ecfdf5;
        border-color: #34d399;
        color: #064e3b;
      }
      .livret-peuple-chip-off {
        background: #f8fafc;
        border-color: #e2e8f0;
        color: #64748b;
        opacity: 0.75;
      }
      .livret-module-summary {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 0.6rem;
        margin-top: 0.85rem;
        padding-top: 0.85rem;
        border-top: 1px dashed #bbf7d0;
      }
      .livret-mod-pill {
        border-radius: 0.7rem;
        padding: 0.55rem 0.75rem;
        font-size: 0.74rem;
        border: 1px solid #e2e8f0;
        background: #ffffff;
      }
      .livret-mod-pill-on {
        border-color: #86efac;
        background: #f0fdf4;
        color: #14532d;
      }
      .livret-mod-pill-off {
        border-color: #cbd5e1;
        background: #f1f5f9;
        color: #475569;
      }
      .livret-law-card {
        background: #ffffff;
        border: 1px solid #cbd5e1;
        border-left: 4px solid #1e3b2e;
        border-radius: 0.75rem;
        padding: 0.85rem 1rem;
      }
      .livret-peuple-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 0.9rem;
        padding: 1rem 1.15rem;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
        break-inside: avoid;
        page-break-inside: avoid;
      }
      @media print {
        .livret-config-controls {
          display: none !important;
        }
        .livret-config-banner {
          background: #ffffff !important;
          border: 1px solid #94a3b8 !important;
          padding: 0.6rem 0.8rem !important;
        }
      }
    </style>

    <!-- =================================================================== -->
    <!-- BANDEAU INTERACTIF AUTO-EMBARQUÉ : CONFIGURER LE LIVRET             -->
    <!-- =================================================================== -->
    <div id="livret-table-configurator" class="livret-config-banner">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <div>
          <div class="text-xs font-bold uppercase tracking-wider text-forest-800">
            🧭 Configurer le livret pour ma table
          </div>
          <p class="text-xs text-slate-600 mt-0.5">
            Lisez le livret complet à 6 Peuples ou adaptez-le instantanément aux Peuples présents autour de votre table (3 à 6 joueurs) pour replier les modules inutiles ce soir.
          </p>
        </div>
        <div class="livret-config-controls flex flex-wrap items-center gap-2 no-print">
          <button type="button" id="btn-livret-mode-complet" onclick="resetLivretComplet()" class="livret-mode-btn ${!isTableMode ? 'livret-mode-btn-active' : ''}">
            📚 Livret complet (6 Peuples)
          </button>
          <button type="button" id="btn-livret-mode-table" onclick="activateLivretTableMode()" class="livret-mode-btn ${isTableMode ? 'livret-mode-btn-active' : ''}">
            🎯 Sur-mesure pour ma table (3 à 6 joueurs)
          </button>
        </div>
      </div>

      <div class="livret-config-controls mt-3 space-y-2.5 no-print">
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-600">Pré-réglages rapides :</span>
          ${presetsHtml}
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-slate-600">Peuples sélectionnés :</span>
          ${checkboxesHtml}
        </div>
      </div>

      <div id="livret-modules-recap" class="livret-module-summary">
        <div class="livret-mod-pill livret-mod-pill-on">
          <div class="font-bold">🌳 Tronc commun · Toujours actif</div>
          <div class="text-[11px] mt-0.5">${isTableMode ? `Table sur-mesure (${n} joueurs : ${tablePeoples.join('–')})` : `Mode Livret complet · 6 Peuples &amp; 22 règles d’arbitrage affichés`}</div>
        </div>
        <div class="livret-mod-pill ${showGardiens ? 'livret-mod-pill-on' : 'livret-mod-pill-off'}">
          <div class="font-bold">🐾 Module Gardiens &amp; Éveil · ${showGardiens ? 'Actif' : 'Masqué (sans Animaux)'}</div>
          <div class="text-[11px] mt-0.5">${showGardiens ? 'Piste des Gardiens (6 icônes), encoches visibles, paris et Éveil affichés.' : 'Aucun Animal Sauvage (M, R, O) autour de la table : la Piste des Gardiens reste dans la boîte.'}</div>
        </div>
        <div class="livret-mod-pill ${showReves ? 'livret-mod-pill-on' : 'livret-mod-pill-off'}">
          <div class="font-bold">🌙 Module Rêves &amp; Sommeil · ${showReves ? 'Actif' : 'Masqué (sans Rêves)'}</div>
          <div class="text-[11px] mt-0.5">${showReves ? 'Tuiles Rêve sur la Réglette, annulations et Sommeil du Contremaître affichés.' : 'Aucun Peuple Onirique (H, E) autour de la table : aucune tuile Rêve ni Sommeil dans cette partie.'}</div>
        </div>
        <div class="livret-mod-pill ${showEssaim ? 'livret-mod-pill-on' : 'livret-mod-pill-off'}">
          <div class="font-bold">🐜 Module Essaim · ${showEssaim ? 'Actif' : 'Masqué (sans Insectes)'}</div>
          <div class="text-[11px] mt-0.5">${showEssaim ? 'Nids, Production, Migration, Déviation ±1, Parade Insecte et Bouclier de lisière affichés.' : 'Jetons Insectes laissés dans la boîte : Production, Migration, Déviation ±1, icône Insecte et Bouclier repliés.'}</div>
        </div>
      </div>
    </div>

    <!-- EN-TÊTE ÉDITORIAL -->
    <header class="border-b-4 border-forest-800 pb-6 mb-8">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div class="text-xs font-semibold uppercase tracking-[0.18em] text-forest-700 mb-1">
            Livret de Règles Officiel · Édition Modulaire
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-forest-950 tracking-tight">
            AMAZONIA : DERNIER REMPART
          </h1>
          <p class="text-sm text-slate-600 mt-1.5 font-medium">
            Jeu coopératif asymétrique à communication silencieuse · <strong>3 à 6 joueurs</strong> · <strong>8 tours en 2 Actes</strong>
          </p>
        </div>
        <div class="bg-forest-50 border border-forest-200 rounded-xl px-4 py-3 text-xs text-forest-900 space-y-1">
          <div><strong class="text-forest-800">Table configurée :</strong> <span class="dyn-span">Table à ${n} joueurs</span></div>
          <div><strong class="text-forest-800">Forêt initiale :</strong> <span class="dyn-span">${totalArbres} Arbres (${pMax} parcelles : ${dotationStr})</span></div>
          <div><strong class="text-forest-800">Standard officiel :</strong> #${configNum} / ${totalConfigs} · Départ décalé</div>
        </div>
      </div>

      <div class="mt-4 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-xs text-slate-700 flex flex-wrap items-center justify-between gap-2">
        <div><strong>Peuples autour de la table :</strong> <span class="dyn-span">${tableSummary}</span></div>
        <div class="flex flex-wrap gap-2">
          <span class="px-2 py-0.5 rounded-full ${tableGardiensActif ? 'bg-amber-100 text-amber-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${tableGardiensActif ? `🐾 Gardiens &amp; Éveil actifs (${tableNbAnimaux} Peuple${tableNbAnimaux > 1 ? 's' : ''})` : '🐾 Sans Animaux Sauvages'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${tableNbReves > 0 ? 'bg-purple-100 text-purple-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${tableNbReves > 0 ? `🌙 ${tableNbReves} Rêves en jeu` : '🌙 Sans Peuples Oniriques'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${tableEssaimActif ? 'bg-lime-100 text-lime-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${tableEssaimActif ? '🐜 Essaim présent' : '🐜 Sans Insectes'}
          </span>
        </div>
      </div>
    </header>

    <!-- =================================================================== -->
    <!-- SECTION 1 : PRÉSENTATION, BUT DU JEU & MATÉRIEL INTELLIGENT         -->
    <!-- =================================================================== -->
    <section id="sec-presentation" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        1. Présentation, But du jeu &amp; Matériel intelligent
      </h2>

      <p class="text-sm text-slate-700 leading-relaxed">
        Les machines du Contremaître encerclent la grande forêt amazonienne. Depuis la bordure de chaque rayon, Abatteuses et Bulldozers s’enfoncent vers le cœur sacré, transformant les arbres centenaires en souches puis en routes de terre battue. Face à cette avancée implacable, les <strong>Peuples de la forêt</strong> — Humains, Entités Magiques, Mammifères, Reptiles, Oiseaux et Insectes — unissent leurs forces dans un silence tendu.
      </p>

      <p class="text-sm text-slate-700 leading-relaxed">
        <strong>Amazonia : Dernier Rempart</strong> est un jeu <strong>100 % coopératif</strong> : vous gagnez et scorez ensemble. Votre <strong>score collectif</strong> est égal au nombre — et au <strong>pourcentage (%)</strong> — d’<strong>Arbres encore debout</strong> à l’issue de la partie (après application éventuelle de vos tuiles enracinées) sur votre capital initial de <span class="dyn-span"><strong>${totalArbres} Arbres</strong></span>. La partie dure <strong>8 tours maximum</strong>, découpés en <strong>deux Actes</strong> inversant la cadence des engins au début du 5<sup>e</sup> tour.
      </p>

      <div>
        <h3 class="text-base font-bold text-forest-900 mb-2">Les trois issues de fin de partie</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
          <div class="bg-forest-50 border border-forest-200 rounded-xl p-3.5">
            <div class="font-bold text-forest-900 mb-1">⏳ 1. Tenir 8 tours (priorité absolue)</div>
            <p class="text-slate-600">Résistez jusqu’au terme des attaques du 8<sup>e</sup> tour. Cette fin l’emporte toujours au Tour 8, quelles que soient la position des Rêves ou des Gardiens.</p>
          </div>
          <div ${_livretModAttrs('REVES', showReves, 'bg-purple-50 border border-purple-200 rounded-xl p-3.5')}>
            <div class="font-bold text-purple-900 mb-1">🌙 2. Sommeil du Contremaître (Tours 1 à 7)</div>
            <p class="text-slate-600">
              ${tableNbReves > 0
                ? `<span class="dyn-span">Réunissez les <strong>${tableNbReves} tuiles Rêve</strong> de la partie en un bloc continu à gauche de la Réglette (rangs 1 à ${tableNbReves}). Prioritaire sur l’Éveil en cas de réalisation simultanée, mais impossible si un Rêve a été enraciné.</span>`
                : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Onirique autour de la table).</span>'}
            </p>
          </div>
          <div ${_livretModAttrs('GARDIENS', showGardiens, 'bg-amber-50 border border-amber-200 rounded-xl p-3.5')}>
            <div class="font-bold text-amber-900 mb-1">🌿 3. Éveil de la Forêt (Tours 1 à 7)</div>
            <p class="text-slate-600">
              ${tableGardiensActif
                ? `<span class="dyn-span">Engagez tous les <strong>${n} deuxièmes pions</strong> de la table sur la Piste des Gardiens et remportez <strong>tous les paris du tour</strong>.</span>`
                : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Animal Sauvage autour de la table).</span>'}
            </p>
          </div>
        </div>
      </div>

      <!-- ANCRE MATÉRIEL & MISE EN PLACE -->
      <div id="sec-materiel" class="scroll-mt-24">
        <div id="brique-mise-en-place" class="brique-card scroll-mt-24 space-y-5">
          <div class="brique-header">
            <div class="flex items-center gap-2.5 flex-wrap">
              <span class="brique-badge">Matériel &amp; Mise en place</span>
              <h3 class="text-lg font-bold text-forest-950">Un matériel auto-vérifiant pensé pour la table</h3>
            </div>
            <span class="text-xs font-mono text-forest-700"><span class="dyn-span">${n} rayons · ${totalArbres} Arbres · ${2 * n} tuiles</span></span>
          </div>

          <p class="text-sm text-slate-700">
            Dans <strong>Amazonia</strong>, chaque pièce porte sa propre règle dans sa forme ou sur ses deux faces : aucune feuille de suivi, aucune mémoire cachée, aucun oubli possible.
          </p>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 text-xs text-slate-700">
            <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2.5">
              <h4 class="font-bold text-sm text-forest-900">🌳 Forêt, Puissance &amp; Pioche secrète</h4>
              <ul class="space-y-2 list-disc pl-4">
                <li data-inv="INV-01">
                  <strong>Dotation finie de 10 × N pions uniques recto-verso (Arbre debout / Souche) :</strong> il n’existe jamais de réserve illimitée d’arbres ou de souches. Les <span class="dyn-span"><strong>${totalArbres} pions</strong></span> posés au départ constituent l’intégralité de votre forêt : l’Abatteuse retourne tous les <strong>Arbre debout</strong> d’une parcelle sur leur face <strong>Souche</strong> sans toucher aux Souches ; le Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches ; la repousse finale par Enracinement retourne des Souches survivantes en Arbres debout, plafonnant naturellement chaque parcelle à sa dotation d’origine.
                </li>
                <li data-inv="INV-02">
                  <strong>Jetons Puissance recto-verso Rouge (+1) / Bleu Surchauffe (−1) :</strong> chaque jeton Puissance porte une face <strong>Rouge (+1)</strong> et une face <strong>Bleu Surchauffe (−1)</strong>. Retourner un jeton rouge en bleu matérialise immédiatement la surchauffe d’une machine.
                </li>
                <li data-inv="INV-05">
                  <strong>Sac en tissu opaque de jetons épais :</strong> la pioche s’effectue dans un <strong>sac opaque</strong> garni des <span class="dyn-span"><strong>${2 * n} jetons Machine</strong></span> (1 Abatteuse et 1 Bulldozer par rayon), des jetons <strong>Sabotage</strong> ordinaires gagnés en jeu et, avec les Reptiles, jusqu’à <strong>4 jetons Sabotage « Écaille »</strong> de même gabarit. Les jetons non piochés restent toujours <strong>cachés</strong> dans le sac sans jamais être consultés ; les jetons révélés (et celui du Perchoir) retournent au sac au Ménage.
                </li>
                <li>
                  <strong>Mini-Paravent gradué 1–6 &amp; Dés :</strong> chaque joueur dispose d’un <strong>mini-paravent gradué de 1 à 6</strong> et de <strong>2 dés standards</strong> à 6 faces (plus 1 <em>Dé d’Envol</em> 1–6 chez les Oiseaux), ainsi que de tuiles <strong>Route Forestière</strong>, de jetons <strong>Piège</strong>, du jeton <strong>Coordonnateur</strong> et du <strong>marqueur de Tour (1 à 8)</strong>.
                </li>
              </ul>
            </div>

            <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2.5">
              <h4 class="font-bold text-sm text-forest-900">🛡️ Défenseurs &amp; Supports centraux fixes</h4>
              <ul class="space-y-2 list-disc pl-4">
                <li data-inv="INV-03">
                  <strong>2 pions Défenseurs recto-verso (Réflexion / Définitif) par joueur :</strong> un seul modèle de pion recto-verso pour tous. Votre premier pion se pose directement face <strong>Définitif</strong> (jamais sur les Gardiens) ; votre deuxième pion se pose face <strong>Réflexion</strong> puis se retourne irréversiblement sur <strong>Définitif</strong> (figeant au même instant votre jeton Duel ou votre Plume de Vigie). Chez les Humains, il n’existe que 2 pions Chamanes au total — <strong>1 Tambour</strong> et <strong>1 Chant</strong> recto-verso : poser l’un au premier temps laisse automatiquement l’autre en main pour le second temps !
                </li>
                <li data-inv="INV-08">
                  <strong>Réglette des Tactiques fixe 1–6 &amp; bandelette d’Acte réversible :</strong> la <strong>Réglette</strong> reste immobile toute la partie sur ses 6 rangs (cases Rêves au-dessus des actions imprimées : <em>1 &amp; 4 Sur place</em>, <em>2 &amp; 5 Devant</em>, <em>3 &amp; 6 En avançant −1</em>). Glissée dessous, une <strong>bandelette</strong> d’Acte réversible se retourne seule au début du <strong>Tour 5</strong> (Face A → Face B), sans jamais déplacer ni les Rêves ni les Insectes.
                </li>
                <li ${_livretModAttrs('GARDIENS', showGardiens, '')} data-inv="INV-09">
                  <strong>Piste des Gardiens à 6 icônes dédiées (sans numéros) :</strong> de gauche à droite, les 6 icônes fixes sont <strong>Parade</strong>, <strong>Piégeage</strong>, <strong>Sabotage</strong>, <strong>Rêve</strong>, <strong>Insecte</strong> et <strong>Résonance</strong> en 6<sup>e</sup> et dernière position. L’icône <strong>Résonance</strong> compte individuellement chaque première activation du tour d’un autre Gardien (aucun déclenchement perdu) et le balayage gauche → droite reprend dès qu’un effet rallume une icône située plus à gauche.
                </li>
                <li ${_livretModAttrs('GARDIENS', showGardiens, '')} data-inv="INV-10">
                  <strong>2 encoches latérales visibles par tuile Gardien :</strong> chaque Gardien comporte <strong>2 encoches</strong> sur le côté. À chaque activation du Gardien, faites glisser 1 Défenseur posé dessus dans une encoche. En fin d’attaques : ≥ 1 pion encore sur la tuile = <strong>pari perdu</strong> ; 0 pion dessus et ≥ 1 encoche occupée = <strong>pari gagné</strong> (le Gardien passe sur sa <strong>Face 2</strong>) ; 0 pion dessus et 0 encoche occupée = aucune mise engagée (le Gardien reste en place sur sa face actuelle sans évoluer).
                </li>
                <li ${_livretModAttrs('ESSAIM', showEssaim, '')}>
                  <strong>Essaim &amp; 30 Tuiles de Synergie :</strong> les 30 Tuiles de Synergie couvrent tous les couples de Peuples (15 Gardiens, 10 Rêves, 5 Nids). Les jetons Insectes ne sortent de la boîte que lorsque les Insectes participent à la partie.
                </li>
              </ul>
            </div>
          </div>

          <div>
            <h4 class="text-sm font-bold text-forest-900 uppercase tracking-wider mb-2">Mise en place en 5 gestes</h4>
            <ol class="space-y-1.5 text-sm text-slate-700 list-decimal pl-5">
              <li><strong>Assemblez la roue de la forêt :</strong> chaque joueur choisit un Peuple et s’installe face à son rayon de <strong>${pMax} parcelles</strong> gravées <span class="dyn-span"><strong>${dotationStr}</strong></span>. Garnissez chaque parcelle d’autant de pions <strong>Arbre debout</strong> que son chiffre gravé (<span class="dyn-span"><strong>${arbresParRayon} Arbres par rayon</strong>, soit <strong>${totalArbres} Arbres</strong></span> en tout).</li>
              <li><strong>Installez les supports centraux :</strong> posez la <strong>Réglette des Tactiques</strong> fixe avec la <strong>bandelette d’Acte sur sa Face A (Acte 1)</strong><span ${_livretModAttrs('GARDIENS', showGardiens, '')}> ainsi que la <strong>Piste des Gardiens</strong> à 6 icônes</span>.</li>
              <li><strong>Garnissez les lisières :</strong> entre deux rayons voisins, placez face visible (Face 1) les <span class="dyn-span"><strong>${2 * n} Tuiles de Synergie</strong></span> correspondant aux paires de Peuples autour de votre table (tableau ci-dessous).</li>
              <li><strong>Départ décalé des Machines &amp; Sac opaque :</strong> sur chaque rayon, placez le <strong>Bulldozer sur la parcelle 1 (bordure)</strong> et l’<strong>Abatteuse sur la parcelle 2</strong>, sans aucun jeton Puissance. Glissez leurs <span class="dyn-span"><strong>${2 * n} jetons Machine</strong></span> dans le <strong>sac opaque</strong> (les Sabotages, les Écailles et les jetons Puissance restent en réserve à portée de main).</li>
              <li><strong>Accessoires &amp; Premier tour :</strong> chaque joueur prend son mini-paravent gradué 1–6, ses 2 dés, ses 2 pions Défenseurs et l’accessoire propre à son Peuple (Section 5). Désignez le premier <strong>Coordonnateur</strong> et posez le marqueur de Tour sur <strong>1</strong>.</li>
            </ol>
          </div>

          <div>
            <h4 class="text-sm font-bold text-forest-900 uppercase tracking-wider mb-2">Vos <span class="dyn-span">${2 * n} Tuiles de Synergie</span> en lisière pour cette table</h4>
            <div class="overflow-x-auto border border-slate-200 rounded-xl">
              <table class="w-full text-xs text-left border-collapse">
                <thead class="bg-forest-900 text-white">
                  <tr>
                    <th class="p-2.5">Lisière</th>
                    <th class="p-2.5">Tuile &amp; Famille</th>
                    <th class="p-2.5">Peuple d’origine</th>
                    <th class="p-2.5">Effet officiel</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-200">
                  ${lisieresRowsHtml}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- SECTION 2 : VUE D'ENSEMBLE & LES 4 LOIS PHYSIQUES PERMANENTES       -->
    <!-- =================================================================== -->
    <section id="sec-vue-tour" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        2. Vue d’ensemble &amp; Les 4 Lois Physiques permanentes
      </h2>

      <p class="text-sm text-slate-700 leading-relaxed">
        Autour du centre de la table rayonnent <span class="dyn-span"><strong>${n} rayons de forêt</strong></span>, chacun composé de <strong>4 parcelles</strong> numérotées de la <strong>bordure (parcelle 1)</strong> jusqu’au <strong>cœur (parcelle 4)</strong> avec les chiffres gravés <strong>2 – 2 – 3 – 3</strong>. Chaque chiffre gravé indique à la fois les Arbres plantés au départ et le <strong>Seuil de Parade imprimé</strong> de la parcelle. Au départ, chaque rayon démarre en <strong>départ décalé</strong> : le <strong>Bulldozer sur la parcelle 1</strong> et l’<strong>Abatteuse sur la parcelle 2</strong>. Au pied de chaque rayon figure sa zone de <strong>Furtivité</strong> (<em>Rive Piège</em> et <em>Rive Sabotage</em>), et chaque <strong>lisière partagée</strong> entre deux joueurs voisins porte 2 Tuiles de Synergie.
      </p>

      <!-- APERÇU DU TOUR EN 6 TEMPS -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
        <a href="#brique-preparation" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">1. Préparation sous paravent</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Pioche secrète au sac opaque (Oiseau dernier) et lancer de dés universel par toute la table.</p>
        </a>

        <a href="#brique-pose" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">2. Déploiement muet</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Premier déploiement définitif, puis second déploiement en Réflexion jusqu’à clôture à N−1.</p>
        </a>

        <a href="#brique-ouverture-reves" class="block border border-emerald-200 hover:border-emerald-400 rounded-xl p-3.5 bg-emerald-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">3. Ouverture &amp; Constructions</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🗣️ Parole libre</span>
          </div>
          <p class="text-slate-600">Constructions en lisière, ouverture des paravents, Sabotages, déviations et Rêves défendus.</p>
        </a>

        <a href="#brique-furtivite" class="block border border-emerald-200 hover:border-emerald-400 rounded-xl p-3.5 bg-emerald-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">4. Furtivité &amp; Vie de l’Essaim</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🌿 Forêt vive</span>
          </div>
          <p class="text-slate-600">Verdict Chaud vs Calme par rayon, puis Production des Nids et Migration de l’Essaim.</p>
        </a>

        <a href="#brique-attaques-piegeages" class="block border border-rose-200 hover:border-rose-400 rounded-xl p-3.5 bg-rose-50/50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-rose-900 text-sm">5. Attaques &amp; Verdict</span>
            <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-semibold">⚔️ Résolution</span>
          </div>
          <p class="text-slate-600">Rangs 1 à 6 puis Ratissage, Seuil unifié, Pièges, verdict des paris Gardiens et test de fin.</p>
        </a>

        <a href="#brique-menage" class="block border border-slate-200 hover:border-forest-400 rounded-xl p-3.5 bg-slate-50 transition">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">6. Ménage &amp; Enracinement</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🌱 Transition</span>
          </div>
          <p class="text-slate-600">Enracinement volontaire, passage en Ratissage, remise au sac et rotation du Coordonnateur.</p>
        </a>
      </div>

      <!-- BASCULEMENT ACTE 1 -> ACTE 2 -->
      <div class="rounded-2xl border-2 border-forest-300 bg-gradient-to-r from-amber-50/70 via-white to-rose-50/70 p-4 text-xs">
        <div class="font-bold uppercase tracking-wider text-forest-900 mb-2">
          🎭 Le basculement en 2 Actes — Retourner uniquement la bandelette d’Acte au début du Tour 5
        </div>
        <div class="grid grid-cols-1 md:grid-cols-11 gap-2 items-center">
          <div class="md:col-span-5 bg-white/90 border border-amber-200 rounded-xl p-3">
            <div class="font-bold text-amber-950 text-sm mb-1">Acte 1 · Tours 1 à 4 (Face A)</div>
            <p class="text-slate-700"><strong>Rangs 1–3 : ⚡ Mode Charge</strong> · <strong>Rangs 4–6 : 🔥 Mode Assaut</strong></p>
            <p class="text-slate-500 mt-1">Comme vous retenez le plus petit de 2 dés, les rangs 1–3 tombent souvent : les engins accumulent des jetons rouges chaque fois qu’une frappe passe.</p>
          </div>
          <div class="md:col-span-1 text-center font-bold text-forest-800 text-base py-1">
            ↻<br><span class="text-[10px] uppercase tracking-wider">Tour 5</span>
          </div>
          <div class="md:col-span-5 bg-white/90 border border-rose-200 rounded-xl p-3">
            <div class="font-bold text-rose-950 text-sm mb-1">Acte 2 · Tours 5 à 8 (Face B)</div>
            <p class="text-slate-700"><strong>Rangs 1–3 : 🔥 Mode Assaut</strong> · <strong>Rangs 4–6 : ⚡ Mode Charge</strong></p>
            <p class="text-slate-500 mt-1">La Réglette ne bouge pas : seule la bandelette dessous se retourne sur Face B. Les rangs 1–3 libèrent alors toute la puissance rouge accumulée !</p>
          </div>
        </div>
      </div>

      <!-- LES 4 LOIS PHYSIQUES PERMANENTES -->
      <div class="rounded-2xl border-2 border-forest-800/20 bg-forest-50/60 p-5 space-y-3.5">
        <div>
          <span class="brique-badge">Règles d’or du plateau</span>
          <h3 class="text-xl font-bold text-forest-950 mt-1.5">Les 4 Lois Physiques permanentes</h3>
          <p class="text-xs text-slate-600 mt-0.5">Ces quatre lois s’appliquent à chaque instant de la partie et tranchent instantanément tous les cas particuliers sur la roue.</p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs text-slate-700">
          <div class="livret-law-card space-y-1.5">
            <div class="font-bold text-sm text-forest-950">Loi 1 · Parcelle &amp; Pont routier</div>
            <p>
              Le mot <strong>parcelle</strong> désigne exclusivement une case de forêt contenant encore au moins 1 Arbre ou 1 Souche : une <strong>Route Forestière</strong> n’est plus une parcelle. Le long d’un rayon, toute Route Forestière est <strong>sautée comme un pont</strong> dans le sens radial (pour viser <em>Devant</em>, avancer, reculer ou migrer), mais reste <strong>infranchissable latéralement</strong>. Dès qu’un rayon est 100 % transformé en Routes Forestières, sa zone de Furtivité est définitivement fermée.
            </p>
          </div>

          <div class="livret-law-card space-y-1.5" data-inv="INV-17">
            <div class="font-bold text-sm text-forest-950">Loi 2 · Pièges autonomes &amp; priorité du Croc</div>
            <p>
              Une parcelle accueille au maximum <strong>1 Piège ordinaire</strong>. Tout <strong>Piège</strong> ordinaire est <strong>Piège autonome</strong> : il bloque automatiquement une unique frappe (même avec 0 Défenseur et 0 Insecte, sans consommer les pions présents), allume l’icône <em>Piégeage</em>, puis est <strong>défaussé aussitôt</strong>. Le jeton spécial <strong>Croc</strong> des Reptiles peut cohabiter avec un Piège ordinaire sur la même parcelle : il pare alors <strong>en premier</strong>, allume <em>Piégeage</em> et revient dans la réserve Reptile.
            </p>
          </div>

          <div class="livret-law-card space-y-1.5" data-inv="INV-12">
            <div class="font-bold text-sm text-forest-950">Loi 3 · Inamovibilité du Ratissage</div>
            <p>
              Une machine entrée en <strong>Ratissage</strong> ne quitte plus sa case et ne se déplace jamais (ni avancée, ni recul, ni cale, ni Altération, ni changement de rang). Elle agit hors Réglette en <strong>Assaut permanent</strong> <em>Sur place</em> avec tous ses jetons Puissance antérieurs et son <strong>+1 jeton rouge</strong> physique reçu au passage en Ratissage (convertible en bleu). Malgré son immobilité, sa case compte pleinement comme <strong>parcelle ciblée</strong> tant que cette machine n’a pas encore frappé ce tour.
            </p>
          </div>

          <div class="livret-law-card space-y-1.5" data-inv="INV-16">
            <div class="font-bold text-sm text-forest-950">Loi 4 · Zéro écrasement hors Route, Zéro réservation &amp; Tri sur Route</div>
            <p>
              Déplacer une machine sur une parcelle laisse Nids, Insectes, Pièges et jeton Duel <strong>intacts</strong> (aucun écrasement au contact hors Route), et aucun pion n’est jamais réservé d’avance. Seule la création d’une <strong>Route Forestière</strong> (0 Arbre et 0 Souche après un Bulldozer) vide intégralement la case : tout Nid repart en lisière (<strong>reconstructible</strong>), les Défenseurs reviennent en main à leur propriétaire, et Piège, Croc, Insectes et Duel retournent en réserve. Toute machine sur la case rasée se replie vers la <strong>bordure</strong> (1<sup>re</sup> parcelle côté bordure), ou d’<strong>1 parcelle vers le cœur</strong> si toute la bordure est déjà en Routes (et quitte définitivement le plateau si tout le rayon est rasé).
            </p>
          </div>
        </div>
      </div>

      <!-- BIJECTION LEXICALE & GOUVERNANCE UNITAIRE -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5 text-xs">
        <div class="callout-principe">
          <div class="callout-title">📖 Un mot = un seul sens (Bijection lexicale)</div>
          <ul class="list-disc pl-4 space-y-1 mt-1">
            <li><strong>Ouvrir</strong> = toujours les <em>paravents</em> (jamais une tuile).</li>
            <li><strong>S’activer</strong> = toujours un <em>Gardien</em> qui déclenche son effet.</li>
            <li><strong>Rayon</strong> = la piste de forêt d’un joueur (4 parcelles).</li>
            <li><strong>Rang (1 à 6)</strong> = un emplacement de la <em>Réglette des Tactiques</em>.</li>
            <li><strong>Icône</strong> = un des 6 emplacements dédiés (sans numéros) de la <em>Piste des Gardiens</em>.</li>
            <li><strong>Parcelle</strong> = une case de forêt non devenue <em>Route Forestière</em>.</li>
          </ul>
        </div>
        <div class="callout-principe">
          <div class="callout-title">✨ Règle d’or — Gouvernance unitaire fluide</div>
          <p class="mt-1">
            Zéro vote collectif ni débat interminable autour de la table : chaque <strong>Tuile de Synergie</strong> (Gardien, Rêve ou Nid) est décidée exclusivement par le joueur de son <strong>Peuple d’origine</strong> ; la pose d’un Piège gagné en Furtivité appartient au <strong>propriétaire du rayon</strong> ; le <strong>Bouclier de lisière</strong> est un choix facultatif réservé au joueur <strong>Insectes</strong>. Chacun tranche son domaine avec netteté !
          </p>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- SECTION 3 : DÉROULÉ D'UN TOUR EN 6 ÉTAPES FLUIDES                   -->
    <!-- =================================================================== -->
    <section id="sec-deroule" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        3. Déroulé d’un Tour en 6 étapes fluides
      </h2>

      <!-- ÉTAPE 1 : PRÉPARATION SECRÈTE SOUS PARAVENT -->
      <div id="brique-preparation" class="brique-card scroll-mt-24 space-y-3">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 1</span>
            <h3 class="text-lg font-bold text-forest-950">Préparation secrète sous paravent</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🤫 Paravents fermés</span>
        </div>

        <ol class="space-y-2.5 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Passage à l’Acte 2 (début du Tour 5 uniquement) :</strong> retournez uniquement la <strong>bandelette d’Acte</strong> sous la Réglette sur sa <strong>Face B</strong> (rangs 1–3 en <em>Assaut</em>, rangs 4–6 en <em>Charge</em>). Les Rêves et les Insectes posés sur la Réglette ne bougent pas.
          </li>
          <li data-inv="INV-06">
            <strong>Pioche secrète dans le sac opaque :</strong> chaque joueur pioche secrètement <strong>1 jeton</strong> dans le sac opaque et le cache derrière son mini-paravent (les jetons restés dans le sac demeurent cachés sans jamais être consultés). En cas de <strong>pénurie</strong> (moins de jetons dans le sac que de joueurs), la distribution s’effectue dans le <strong>sens horaire à partir du Coordonnateur</strong>, en servant toujours l’<strong>Oiseau en dernier</strong> : grâce à son pouvoir d’<em>Éclaireur du ciel</em>, l’Oiseau regarde jusqu’à 2 jetons du sac, en garde 1 si possible et pose l’autre face cachée à plat sur son <em>Perchoir de Vigie</em>. Un joueur qui ne reçoit aucun jeton joue normalement tout le reste du tour.
          </li>
          <li data-inv="INV-07">
            <strong>Lancer de dés universel obligatoire :</strong> derrière leur <strong>mini-paravent</strong> gradué de 1 à 6, <strong>tous les joueurs lancent</strong> simultanément leurs dés (2 dés standards chacun, plus le <em>Dé d’Envol</em> 1–6 chez l’Oiseau), <strong>même s’ils ont pioché un Sabotage ou une Écaille</strong> (auquel cas leur résultat est simplement ignoré). Chacun place son dé retenu (le <strong>plus petit</strong> des 2 dés standards, ou le <em>Dé d’Envol</em> si l’Oiseau choisit son <em>Double horizon</em>) devant le rang 1 à 6 correspondant sur la graduation de son paravent. Ce geste commun supprime totalement toute <strong>fuite sonore</strong> !
          </li>
        </ol>

        <div class="callout-principe">
          <div class="callout-title">✨ Règle d’or — Zéro indice acoustique</div>
          <p>En lançant tous les dés en même temps — Sabotage, Écaille ou Machine — personne ne peut deviner à l’oreille qui a neutralisé une machine du Contremaître.</p>
        </div>
      </div>

      <!-- ÉTAPE 2 : DÉPLOIEMENT MUET EN DEUX TEMPS -->
      <div id="brique-pose" class="brique-card scroll-mt-24 space-y-3">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 2</span>
            <h3 class="text-lg font-bold text-forest-950">Déploiement muet en deux temps</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🤫 Silence tactique absolu</span>
        </div>

        <p class="text-sm text-slate-700">
          Paravents toujours fermés et sans un mot ni geste d’allusion, chaque joueur déploie ses <strong>2 pions Défenseurs</strong> en deux temps très clairs :
        </p>

        <ol class="space-y-3 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Premier déploiement (simultané, directement face <em>Définitif</em>) :</strong> tous les joueurs posent en même temps leur premier pion face <strong>Définitif</strong> sur l’une des destinations suivantes (<strong>jamais sur la Piste des Gardiens</strong>) :
            <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600 text-xs sm:text-sm">
              <li>une parcelle de <strong>sa propre forêt</strong> (ou de n’importe quel rayon pour le <em>Tambour</em> des Humains) ;</li>
              <li>une Tuile de Synergie non construite de <strong>ses deux lisières</strong> (max 2 bâtisseurs par tuile) ;</li>
              <li>une <strong>rive ouverte de Furtivité</strong> (<em>Rive Piège</em> ou <em>Rive Sabotage</em>, max 2 pions par rive) au pied de n’importe quel rayon qui n’est pas 100 % rasé ;</li>
              <li ${_livretModAttrs('REVES', showReves, '')}>une tuile <strong>Rêve déjà en jeu</strong> sur la Réglette des Tactiques.</li>
            </ul>
            Ce premier pion ne peut plus être déplacé jusqu’à l’Ouverture des paravents.
          </li>
          <li>
            <strong>Second déploiement (face <em>Réflexion</em> → validation irréversible face <em>Définitif</em>) :</strong> chaque joueur place ensuite son deuxième pion face <strong>Réflexion</strong> sur l’une des destinations suivantes, <strong>n’importe où sur le plateau</strong> :
            <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600 text-xs sm:text-sm">
              <li>toute parcelle de <strong>n’importe quel rayon</strong> de la forêt ;</li>
              <li>toute Tuile de Synergie non construite de <strong>n’importe quelle lisière</strong> ;</li>
              <li>toute <strong>rive ouverte de Furtivité</strong> d’un rayon non 100 % rasé ;</li>
              <li ${_livretModAttrs('REVES', showReves, '')}>tout <strong>Rêve déjà en jeu</strong> sur la Réglette des Tactiques ;</li>
              <li ${_livretModAttrs('GARDIENS', showGardiens, '')}>en <strong>pari sur un Gardien déjà construit</strong> sur la Piste des Gardiens (0, 1 ou <strong>maximum 2 Défenseurs par Gardien</strong>).</li>
            </ul>
            Tant que votre pion est face <em>Réflexion</em>, vous pouvez le déplacer librement en observant les poses visibles de vos alliés. Dès que votre choix est arrêté, retournez-le sur sa face <strong>Définitif</strong> : ce geste est <strong>irréversible</strong> et fige au même instant le jeton <em>Duel</em> (Mammifères) ou la <em>Plume de Vigie</em> (Oiseaux) que vous auriez mobilisé ce tour.
          </li>
        </ol>

        <div class="callout-gardefou space-y-2">
          <div class="callout-title">🛡️ Garde-fous du déploiement muet</div>
          <p data-inv="INV-04">
            <strong>Clôture à N−1 joueurs validés :</strong> dès que <strong>N − 1 joueurs</strong> ont retourné leur deuxième pion sur face <em>Définitif</em>, le dernier joueur encore en <em>Réflexion</em> a droit à au plus un <strong>ultime ajustement</strong> avant de valider irréversiblement son pion.
          </p>
          <p data-inv="INV-19">
            <strong>Zéro coup stérile, Repli de première pose &amp; Bâtisseurs :</strong> il est strictement interdit de poser le deuxième bâtisseur sur une tuile de lisière actuellement <strong>impossible à placer</strong> sur le plateau (par exemple, un Nid alors que les deux rayons adjacents n’ont aucune parcelle libre sans machine ni Nid). Si un joueur ne dispose d’aucun emplacement légal au Premier déploiement (sa forêt est entièrement rasée et ses lisières sont complètes ou inplaçables), il peut poser son premier pion en repli sur une parcelle d’un allié. Une fois construite à l’étape suivante, toute tuile couche ses bâtisseurs <strong>en attente</strong> devant leur propriétaire — sauf sur une table à <strong>3 joueurs</strong> lors de la construction d’un Gardien ou d’un Rêve (voir Étape 3).
          </p>
        </div>

        <div class="callout-exemple">
          <div class="callout-title">💡 Exemple concret — Dialogue silencieux autour de la table</div>
          <p>
            Vous détenez l’Abatteuse des Mammifères derrière votre paravent et voyez que le Bulldozer des Mammifères est déjà en Ratissage. Au Premier déploiement, vous placez votre pion sur la <em>Rive Piège</em> des Mammifères : vos alliés comprennent sans un mot que ce rayon va subir 2 machines ce tour-ci, et l’un d’eux peut compléter la rive au Second déploiement pendant que les Mammifères préparent leur parade !
          </p>
        </div>
      </div>

      <!-- ÉTAPE 3 : OUVERTURE DES PARAVENTS & CONSTRUCTIONS -->
      <div id="brique-ouverture-reves" class="brique-card scroll-mt-24 space-y-3.5">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 3</span>
            <h3 class="text-lg font-bold text-forest-950">Ouverture des paravents &amp; Constructions</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">🗣️ Paravents ouverts · Parole libre</span>
        </div>

        <ol class="space-y-3 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Constructions obligatoires en lisière (juste avant d’ouvrir les paravents) :</strong> chaque tuile de lisière réunissant <strong>2 Défenseurs</strong> est construite immédiatement (si plusieurs tuiles sont prêtes, le <strong>Coordonnateur</strong> choisit l’ordre de construction) :
            <ul class="list-disc pl-5 mt-1 space-y-1 text-slate-600 text-xs sm:text-sm">
              <li ${_livretModAttrs('GARDIENS', showGardiens, '')}><strong>Gardien :</strong> posé Face 1 sur une icône libre de la Piste des Gardiens choisie par son Peuple d’origine.</li>
              <li ${_livretModAttrs('REVES', showReves, '')}><strong>Rêve :</strong> posé par-dessus le <strong>rang libre le plus à droite</strong> de la Réglette (<code>6</code>, puis <code>5</code>…), sans jamais déplacer les Insectes présents ni masquer l’action imprimée dessous.</li>
              <li ${_livretModAttrs('ESSAIM', showEssaim, '')}><strong>Nid :</strong> posé sur une parcelle libre (sans machine ni autre Nid) de l’un de ses deux rayons voisins.</li>
            </ul>
            <div class="mt-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-slate-700">
              <strong>Sort des bâtisseurs :</strong> sitôt la tuile posée, ses 2 Défenseurs bâtisseurs sont couchés <strong>en attente</strong> devant leur propriétaire jusqu’au Ménage (ils pourront notamment être rappelés en jeu par un pouvoir comme <em>Le Bond du Jaguar</em>).
              <span class="dyn-span"><strong>Bonus à 3 joueurs :</strong> ${n === 3 ? 'sur votre table à 3 joueurs, ' : 'dans une partie à 3 joueurs, '}lors de la construction d’un <strong>Gardien</strong> ou d’un <strong>Rêve</strong>, le Peuple d’origine libère immédiatement <strong>1 des 2 bâtisseurs</strong> vers une parcelle de l’un des deux rayons adjacents (sauf si ces deux rayons sont déjà 100 % rasés en Routes Forestières).</span>
            </div>
          </li>

          <li>
            <strong>Ouverture simultanée des paravents :</strong> tous les joueurs lèvent ensemble leur paravent et la parole redevient libre ! Posez chaque <strong>jeton Machine</strong> révélé bien en vue <strong>devant son rayon d’origine</strong> (il y reste visible jusqu’au verdict de Furtivité ; s’il est annulé par un Rêve, <strong>inclinez-le à 90°</strong> sans le retirer). Si une machine mobile révélée portait un jeton d’<strong>Altération</strong> (Entités Magiques), retirez ce jeton : la machine compte normalement dans la mobilisation de son rayon, mais elle <strong>recule d’1 parcelle</strong> (si possible) et <strong>ne frappe pas</strong> ce tour-ci.
          </li>

          <li data-inv="INV-15">
            <strong>Séquence réactive stricte de l’Ouverture :</strong> résolvez toujours ces trois temps dans cet ordre exact, en effectuant un <strong>balayage gauche → droite de la Piste des Gardiens</strong> après chaque événement :
            <ol class="list-[lower-alpha] pl-5 mt-1.5 space-y-1.5 text-xs sm:text-sm text-slate-700">
              <li>
                <strong>Sabotages &amp; Écailles (un par un) :</strong> chaque jeton <em>Sabotage</em> ordinaire ou <em>Écaille</em> révélé fait perdre son activation au Contremaître et allume l’icône <strong>Sabotage</strong>. S’il s’agit d’une <strong>Écaille</strong>, le joueur Reptile pose en plus le <em>Croc</em> sur une parcelle ciblée → balayage Gardiens.
              </li>
              <li ${_livretModAttrs('ESSAIM', showEssaim, '')}>
                <strong>Déviations d’Insectes ±1 (une par une) :</strong> le joueur Insectes peut défausser 1 Insecte posé sur un rang de la Réglette pour décaler le dé d’une machine révélée de <strong>−1 ou +1 rang</strong> (entre 1 et 6), ce qui allume l’icône <strong>Insecte</strong> → balayage Gardiens.
              </li>
              <li ${_livretModAttrs('REVES', showReves, '')}>
                <strong>Rêves défendus (de gauche à droite) :</strong> parcourez chaque Rêve portant au moins 1 Défenseur de <strong>gauche à droite</strong> sur la Réglette. Pour chacun :
                <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600">
                  <li><strong>Annulation choisie :</strong> chaque Défenseur posé sur ce Rêve <strong>annule 1 machine</strong> présente sur ce rang (inclinez son jeton à 90°). S’il y a plus de machines que de Défenseurs, <strong>le propriétaire du Rêve choisit librement</strong> quelle(s) machine(s) sont annulées, <strong>y compris une machine déviée</strong> sur ce rang ; les machines non annulées exécuteront normalement la Tactique imprimée dessous pendant les Attaques.</li>
                  <li><strong>Pouvoir propre du Rêve :</strong> appliquez intégralement le texte du Rêve (il est actif dès que le Rêve est défendu, <strong>même s’il y a 0 machine sur ce rang</strong>, sauf s’il commence explicitement par <em>« Quand ce Rêve annule… »</em>).</li>
                  <li><strong>Icône Rêve &amp; Défenseurs solidaires :</strong> si au moins 1 machine a été annulée par ce Rêve (<strong>déviée ou non</strong>), allumez l’icône <strong>Rêve</strong> puis balayez la Piste des Gardiens. Un Rêve sans aucun Défenseur reste totalement inerte. Enfin, chaque fois qu’un Rêve glisse sur la Réglette, <strong>les Défenseurs posés sur un Rêve se déplacent toujours avec lui</strong> !</li>
                </ul>
              </li>
            </ol>
          </li>
        </ol>
      </div>

      <!-- ÉTAPE 4 : FURTIVITÉ & VIE DE L'ESSAIM -->
      <div id="brique-furtivite" class="brique-card scroll-mt-24 space-y-3" data-inv="INV-14">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 4 · Furtivité</span>
            <h3 class="text-lg font-bold text-forest-950">Furtivité « Chaud vs Calme » par rayon</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">🎯 Rive Piège vs 🔧 Rive Sabotage</span>
        </div>

        <p class="text-sm text-slate-700">
          Au pied de chaque rayon actif se trouvent <strong>2 rives indépendantes</strong> de 2 places : la <strong>🎯 Rive Piège</strong> et la <strong>🔧 Rive Sabotage</strong>. Seule une rive portant un <strong>binôme complet de 2 Défenseurs</strong> est évaluée (1 pion seul est sans effet et ne bascule jamais vers l’autre rive).
        </p>
        <p class="text-sm text-slate-700">
          Pour lire la mobilisation <strong>m(r)</strong> d’un rayon en un coup d’œil, comptez simplement les <strong>jetons Machine visibles devant ce rayon (droits ou inclinés à 90°)</strong> plus ses <strong>machines déjà en Ratissage</strong>. Une déviation d’Insecte ±1, une annulation par Rêve ou une Altération ne changent jamais <em>m(r)</em> ; un Sabotage ou une Écaille ne compte pour aucun rayon.
        </p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs sm:text-sm">
          <div class="rounded-xl border border-amber-200 bg-amber-50/60 p-3.5">
            <div class="font-bold text-amber-950 mb-1">🎯 Rive Piège (« rayon chaud » : m(r) = 2)</div>
            <p class="text-slate-700">Réussit si les <strong>2 machines</strong> de ce rayon sont mobilisées ce tour-ci → le <strong>propriétaire du rayon</strong> pose <strong>1 Piège ordinaire</strong> sur une parcelle de son rayon qui ne porte pas encore de Piège ordinaire. <em>(Échoue sans compensation si toutes les parcelles de ce rayon sont déjà piégées, ou si m(r) vaut 0 ou 1.)</em></p>
          </div>
          <div class="rounded-xl border border-sky-200 bg-sky-50/60 p-3.5">
            <div class="font-bold text-sky-950 mb-1">🔧 Rive Sabotage (« rayon calme » : m(r) = 0)</div>
            <p class="text-slate-700">Réussit si <strong>0 machine</strong> de ce rayon n’est mobilisée ce tour-ci → ajoutez <strong>1 jeton Sabotage</strong> de la réserve directement dans le sac opaque (sans allumer l’icône <em>Sabotage</em>). <em>(Échoue si m(r) vaut 1 ou 2.)</em></p>
          </div>
        </div>

        <p class="text-xs text-slate-600">
          Une fois les rives tranchées, couchez tous les Défenseurs de Furtivité <strong>en attente</strong> devant leur propriétaire jusqu’au Ménage. La Furtivité n’allume jamais aucune icône de la Piste des Gardiens.
        </p>

        <div class="callout-exemple">
          <div class="callout-title">💡 Exemple concret — Lecture instantanée devant chaque rayon</div>
          <ul class="list-disc pl-4 space-y-0.5">
            <li><strong>Rayon chaud (2) :</strong> le Bulldozer des Reptiles est en Ratissage et leur Abatteuse a été révélée puis annulée par un Rêve (jeton incliné à 90° devant le rayon) → <code>1 + 1 = 2</code> : la <em>Rive Piège</em> est gagnée !</li>
            <li><strong>Rayon calme (0) :</strong> aucun jeton Machine des Oiseaux n’a été tiré et aucune de leurs machines n’est en Ratissage → <code>0</code> : la <em>Rive Sabotage</em> ajoute 1 Sabotage au sac.</li>
            <li><strong>Cas mixte (1) :</strong> avec 1 seule machine mobilisée, les deux rives échouent.</li>
          </ul>
        </div>
      </div>

      <!-- ÉTAPE 4 SUITE : VIE DE L'ESSAIM (MODULE ESSAIM) -->
      <div id="brique-nids-migration" ${_livretModAttrs('ESSAIM', showEssaim, 'brique-card brique-card-lime scroll-mt-24 space-y-3')}>
        <div class="brique-header border-lime-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-lime-100 text-lime-950 border-lime-300">Étape 4 · Module Essaim</span>
            <h3 class="text-lg font-bold text-lime-950">Vie de l’Essaim : Production des Nids &amp; Migration</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold ${tableEssaimActif ? 'bg-lime-200 text-lime-950' : 'bg-slate-200 text-slate-600'}">
            ${tableEssaimActif ? '🐜 Actif sur votre table' : '🐜 Actif uniquement avec les Insectes'}
          </span>
        </div>

        <ol class="space-y-2.5 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Production des Nids défendus :</strong> dans l’ordre choisi par le joueur Insectes, chaque Nid en forêt portant <strong>au moins 1 Défenseur</strong> se résout comme un bloc indivisible : créez <strong>+1 Insecte</strong> sur sa parcelle s’il y a 0 ou 1 Insecte à cet instant, ou <strong>+2 Insectes</strong> s’il y en a déjà 2 ou plus (cette création n’allume pas l’icône <em>Insecte</em>), puis appliquez son pouvoir <em>« Après production »</em>, puis balayez la Piste des Gardiens.
          </li>
          <li>
            <strong>Migration de l’Essaim (dans les deux sens) :</strong> résolue <strong>rayon par rayon</strong> dans l’ordre choisi par le joueur Insectes. Chaque Insecte en forêt reste sur place ou se déplace d’<strong>1 cran dans les deux sens</strong> le long de son rayon (vers le cœur ou vers la bordure, en sautant les Routes Forestières comme un pont). Depuis la <strong>dernière parcelle</strong> d’un rayon (la plus proche du cœur), 1 cran permet une sortie en aller simple vers n’importe quel <strong>rang 1–6 de la Réglette</strong> ou n’importe quelle <strong>icône de la Piste des Gardiens</strong> (sans limite par emplacement). Retournez chaque jeton déplacé pour suivre vos mouvements, puis remettez-les à l’endroit une fois terminé. Les Insectes ne migrent jamais dans les zones de Furtivité.
          </li>
        </ol>
      </div>

      <!-- ÉTAPE 5 : ATTAQUES DES MACHINES & VERDICT DES PARIS -->
      <div id="brique-attaques-piegeages" class="brique-card scroll-mt-24 space-y-4">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 5</span>
            <h3 class="text-lg font-bold text-forest-950">Attaques des Machines &amp; Verdict des Paris</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-rose-100 text-rose-800">⚔️ Rangs 1 → 6 puis Ratissage</span>
        </div>

        <p class="text-sm text-slate-700">
          Résolvez d’abord les machines encore actives des <strong>rangs 1 à 6 de la Réglette</strong> (y compris sous un Rêve si elles n’ont pas été annulées), puis toutes les machines en <strong>Ratissage</strong> (<em>Assaut permanent Sur place</em>). Sur un même rayon (au même rang ou en Ratissage), l’<strong>Abatteuse agit toujours avant le Bulldozer</strong> ; entre rayons distincts, les joueurs choisissent l’ordre. Chaque machine est résolue d’un seul tenant (cibles → frappes → avancée éventuelle → gain éventuel en Charge → balayage Gardiens).
        </p>

        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2 text-xs sm:text-sm text-slate-700" data-inv="INV-13">
          <div class="font-bold text-forest-900">1. Parcelles ciblées figées &amp; Plafond d’avancée sans double bond</div>
          <p>
            Dès qu’une machine s’active, les parcelles qu’elle vise sont <strong>figées</strong> (ex. sur <em>En avançant</em> : sa parcelle actuelle puis la parcelle <em>Devant</em>). Si la seconde parcelle ciblée devient entre-temps une <strong>Route</strong>, cette frappe est simplement <strong>annulée sans aucun report</strong> sur la parcelle suivante. De même, sur une action <strong>En avançant</strong> (rangs 3 et 6), si la création d’une Route en bordure pendant ses frappes a déjà poussé la machine d’1 parcelle vers le cœur, cette poussée couvre et remplace l’avancée finale : <strong>jamais de double bond de +2 parcelles</strong> en une activation !
          </p>
        </div>

        <div class="bg-amber-50/70 border border-amber-300 rounded-xl p-3.5 space-y-1.5 text-xs sm:text-sm text-slate-800" data-inv="INV-11">
          <div class="font-bold text-amber-950">2. Formule unique du Seuil de Parade</div>
          <p class="font-medium">
            <strong>Seuil de Parade</strong> = <strong>chiffre gravé de la parcelle</strong> (<span class="dyn-span">${dotationStr}</span>)
            <strong>+ jetons rouges</strong> <em>(en Mode Assaut et Ratissage uniquement ; ignorés en Mode Charge)</em>
            <strong>− jetons bleus Surchauffe</strong> <em>(actifs dans TOUS les modes : Charge, Assaut et Ratissage)</em>
            <strong>− 1</strong> aux rangs <code>3</code> et <code>6</code> <em>(En avançant)</em>, avec un <strong>minimum 1</strong>.
          </p>
          <p class="text-xs text-amber-900">
            Chaque machine combat avec sa propre puissance, indépendamment de l’autre machine de son rayon.
          </p>
        </div>

        <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-2 text-xs sm:text-sm text-slate-700">
          <div class="font-bold text-forest-900">3. Chaîne à 2 maillons des parades (pour chaque frappe)</div>
          <ol class="list-decimal pl-5 space-y-1.5">
            <li>
              <strong>Maillon 1 — Piège (Croc prioritaire, puis Piège ordinaire) :</strong> si le <strong>Croc</strong> Reptile se trouve sur la parcelle, il pare <strong>en premier</strong> (même s’il cohabite avec un Piège ordinaire), allume l’icône <em>Piégeage</em> et revient dans la réserve Reptile. Sinon, un <strong>Piège autonome</strong> sur la parcelle pare automatiquement cette frappe (même à 0 Défenseur et 0 Insecte, sans dépenser les pions présents), allume l’icône <em>Piégeage</em> et est <strong>défaussé aussitôt</strong>.
            </li>
            <li>
              <strong>Maillon 2 — Parade classique :</strong> si aucun piège n’a intercepté la frappe et que <code>Défenseurs présents${showEssaim ? ' + Insectes présents' : ''} ≥ Seuil de Parade</code>, la frappe est parée. Si des Défenseurs seuls suffisent à couvrir le Seuil, allumez l’icône <strong>Parade</strong>. <span ${_livretModAttrs('ESSAIM', showEssaim, '')}>Si au moins 1 Insecte est défaussé à la volée pour compléter le Seuil, allumez plutôt l’icône <strong>Insecte</strong>.</span> <em>(Les Défenseurs restent en place sur la parcelle.)</em>
            </li>
          </ol>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div class="bg-white border border-slate-200 rounded-xl p-3.5 space-y-1">
            <div class="font-bold text-slate-900">🪓 Si la frappe n’est pas parée</div>
            <ul class="list-disc pl-4 space-y-1 text-slate-700">
              <li><strong>Abatteuse :</strong> retourne <strong>tous les Arbres debout</strong> de la parcelle sur leur face <em>Souche</em> et <strong>ne touche jamais aux Souches</strong>.</li>
              <li><strong>Bulldozer :</strong> retourne <strong>1 Arbre debout</strong> en <em>Souche</em> puis retire <strong>toutes les Souches</strong> de la parcelle. S’il ne reste ni Arbre ni Souche, posez une tuile <strong>Route Forestière</strong> (vidage exact de la Loi 4 + repli).</li>
            </ul>
          </div>
          <div class="bg-white border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <div>
              <span class="font-bold text-amber-900">⚡ Gain en Mode Charge</span> <span class="text-slate-500">(Acte 1 : rangs 1–3 · Acte 2 : rangs 4–6)</span> :
              dès qu’au moins une frappe ciblant une parcelle réelle non-Route n’est ni parée ni piégée, ajoutez <strong>+1 jeton rouge</strong> sur cette machine (<strong>1 jeton maximum par activation</strong>, même sur <em>En avançant</em> ; une attaque <em>Devant</em> dans le vide depuis la dernière parcelle ne rapporte jamais de jeton).
            </div>
            <div>
              <span class="font-bold text-rose-900">🔥 Mode Assaut &amp; Ratissage</span> <span class="text-slate-500">(Acte 1 : 4–6 · Acte 2 : 1–3 · Ratissage)</span> :
              tous les jetons rouges et bleus comptent au Seuil ; aucun jeton rouge n’est gagné.
            </div>
          </div>
        </div>

        <div ${_livretModAttrs('GARDIENS', showGardiens, 'bg-amber-50/50 border border-amber-200 rounded-xl p-3.5 text-xs sm:text-sm text-slate-700 space-y-1.5')}>
          <div class="font-bold text-amber-950">4. Verdict des Paris sur les Gardiens (en fin d’attaques)</div>
          <ul class="list-disc pl-5 space-y-1">
            <li><strong>Pari perdu (≥ 1 Défenseur encore posé sur la tuile) :</strong> le Gardien retourne immédiatement en lisière sur sa Face 1 (reconstructible plus tard)<span ${_livretModAttrs('ESSAIM', showEssaim, '')}>, sauf si le joueur Insectes choisit d’activer le <strong>Bouclier de lisière</strong> (défausser 1 Insecte posé sur cette icône pour garder le Gardien en piste sur sa face actuelle ; le pari reste néanmoins perdu)</span>.</li>
            <li><strong>Pari gagné (0 pion sur la tuile et ≥ 1 encoche latérale occupée) :</strong> le Gardien reste en piste et passe sur sa <strong>Face 2</strong> pour la suite de la partie.</li>
            <li><strong>Aucune mise engagée (0 pion sur la tuile et 0 encoche occupée) :</strong> le Gardien reste paisiblement en place sur sa face actuelle sans évoluer.</li>
          </ul>
        </div>

        <div class="bg-forest-50 border border-forest-200 rounded-xl p-3 text-xs sm:text-sm text-forest-950">
          <strong>5. Test immédiat des fins de partie :</strong> juste après le verdict des paris, vérifiez si la partie s’achève. Au <strong>Tour 8</strong>, fin temporelle prioritaire absolue. Aux <strong>Tours 1 à 7</strong>, vérifiez les victoires anticipées (en cas de réalisation simultanée, <strong>priorité au Sommeil du Contremaître sur l’Éveil de la Forêt</strong>). Si la partie se termine, ignorez le Ménage et passez au décompte final !
        </div>

        <div class="callout-exemple">
          <div class="callout-title">💡 Exemple concret — Surchauffe bleue en Mode Charge &amp; Croc prioritaire</div>
          <p>
            Au Tour 3 (Acte 1, Face A), un Bulldozer portant 2 jetons rouges et 1 jeton bleu <em>Surchauffe</em> révèle le rang <code>1</code> (<strong>Charge · Sur place</strong>) sur une parcelle gravée <code>2</code> : ses 2 rouges sont ignorés, mais son bleu <em>Surchauffe</em> s’applique bel et bien, abaissant le Seuil de Parade à <code>2 − 1 = 1</code> ! Si la parcelle portait à la fois le <em>Croc</em> Reptile et un Piège ordinaire, le <em>Croc</em> intercepte la frappe en premier et retourne en réserve Reptile, laissant le Piège ordinaire intact pour la frappe suivante.
          </p>
        </div>
      </div>

      <!-- ÉTAPE 6 : MÉNAGE, ENRACINEMENT & FIN DE TOUR -->
      <div id="brique-menage" class="brique-card scroll-mt-24 space-y-3">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Étape 6</span>
            <h3 class="text-lg font-bold text-forest-950">Ménage, Enracinement &amp; Fin de Tour</h3>
          </div>
          <span class="px-2 py-0.5 rounded-full text-xs font-semibold bg-slate-100 text-slate-700">🌱 Préparation du tour suivant</span>
        </div>

        <ol class="space-y-2.5 text-sm text-slate-700 list-decimal pl-5">
          <li>
            <strong>Retour des Défenseurs &amp; Fin des effets temporaires :</strong> chaque joueur reprend en main ses <strong>2 pions Défenseurs</strong> (depuis les parcelles, les Rêves, les encoches des Gardiens et la zone <em>en attente</em>). <span ${_livretModAttrs('ESSAIM', showEssaim, '')}>Tout <strong>Insecte passager</strong> (monté sur une machine via <em>La Fourmilière Coupe-Feuilles</em>) qui n’a pas été dépensé descend sur place sur la parcelle actuelle de la machine.</span> Les effets temporaires du tour prennent fin.
          </li>
          <li data-inv="INV-22">
            <strong>Enracinement volontaire (avant remise au sac) :</strong> chaque joueur peut <strong>enraciner</strong> au plus <strong>1 tuile construite de son Peuple</strong> par tour en la glissant au pied de son rayon face à une parcelle de son choix. La tuile perd son pouvoir actif (hors clause <em>« Enraciné : »</em>), quitte la Piste des Gardiens, la Réglette ou sa parcelle (en y laissant sur place ses éventuels Insectes). <strong>Attention :</strong> enraciner un Rêve rend le <strong>Sommeil impossible</strong> pour le reste de la partie ! Au décompte final (Tour 8, Sommeil ou Éveil), si cette parcelle n’est pas devenue Route Forestière, la tuile y retourne <strong>1 Souche</strong> survivante en Arbre debout — ou <strong>2 Souches</strong> si elle a été enracinée depuis sa <strong>Face 2</strong>.
          </li>
          <li>
            <strong>Passage en Ratissage :</strong> toute machine encore mobile qui termine le tour sur la <strong>dernière parcelle</strong> de son rayon glisse définitivement son <strong>jeton Machine sous elle</strong> (hors du sac pour le reste de la partie), conserve tous ses jetons Puissance antérieurs (rouges et bleus) et reçoit immédiatement <strong>+1 jeton rouge</strong> physique de la réserve.
          </li>
          <li>
            <strong>Remise au sac, Coordonnateur &amp; Tour suivant :</strong> remettez dans le <strong>sac opaque</strong> tous les jetons révélés ce tour (Machines mobiles, Sabotages, Écailles) ainsi que le jeton face cachée du <em>Perchoir de Vigie</em>. Passez le jeton <strong>Coordonnateur</strong> au joueur suivant dans le sens horaire et avancez le marqueur de Tour. <em>(Au début du Tour 5, retournez la seule bandelette d’Acte sur sa Face B !)</em>
          </li>
        </ol>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- SECTION 4 : LES 3 MODULES DE FAMILLES & FIN DE PARTIE               -->
    <!-- =================================================================== -->
    <section id="sec-modules" class="mb-10 scroll-mt-24 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        4. Les 3 Modules de Familles &amp; Fin de Partie
      </h2>

      <!-- MODULE GARDIENS & ÉVEIL -->
      <div id="brique-gardiens-eveil" ${_livretModAttrs('GARDIENS', showGardiens, 'brique-card brique-card-amber scroll-mt-24 space-y-3.5')}>
        <div class="brique-header border-amber-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-amber-100 text-amber-950 border-amber-300">Module Gardiens</span>
            <h3 class="text-lg font-bold text-amber-950">Gardiens &amp; Éveil de la Forêt (🐆 Mammifères, 🐍 Reptiles, 🦜 Oiseaux)</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${tableGardiensActif ? 'bg-amber-200 text-amber-950' : 'bg-slate-200 text-slate-600'}">
            ${tableGardiensActif ? `Actif sur votre table (${tableNbAnimaux} Peuple${tableNbAnimaux > 1 ? 's' : ''})` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${tableGardiensActif
            ? '<span class="dyn-span">Au moins un Peuple Animal Sauvage siège autour de votre table : la <strong>Piste des Gardiens</strong> et l’<strong>Éveil de la Forêt</strong> sont pleinement actifs.</span>'
            : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Animal Sauvage autour de la table).</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Câblage sur 6 icônes dédiées (sans numéros) :</strong> lors de sa construction, un Gardien se pose sur une icône libre choisie par son Peuple d’origine. On termine toujours l’action en cours avant de balayer la piste de <strong>gauche à droite</strong> : <em>Parade → Piégeage → Sabotage → Rêve → Insecte → Résonance</em>. Si l’activation d’un Gardien rallume une icône située plus à gauche, le balayage reprend depuis la gauche.</li>
          <li><strong>Résonance en 6<sup>e</sup> position (compteur sans écrasement) :</strong> l’icône <strong>Résonance</strong> enregistre individuellement chaque première activation du tour de tout autre Gardien distinct (un même Gardien activé deux fois ne l’incrémente qu’une fois, et Résonance ne s’auto-alimente jamais). Aucun déclenchement n’est jamais écrasé : si deux autres Gardiens s’activent pendant un même enchaînement, Résonance s’active deux fois si elle porte 2 Défenseurs !</li>
          <li><strong>Paris uniformes (0, 1 ou 2 Défenseurs) &amp; 2 encoches visibles :</strong> au Second déploiement, les joueurs peuvent miser 0, 1 ou <strong>maximum 2 Défenseurs par Gardien</strong>. Chaque activation fait glisser 1 Défenseur dans une encoche latérale et déclenche son pouvoir. Sans mise (0 pion, 0 encoche), le Gardien demeure en piste sur sa face actuelle sans risque ni promotion.</li>
          <li><strong>Condition comptable de l’Éveil de la Forêt (Tours 1 à 7) :</strong> tous les <span class="dyn-span"><strong>${n} deuxièmes pions</strong></span> de la table ont été engagés sur la Piste des Gardiens et <strong>tous les paris du tour sont gagnés</strong> (0 pion restant sur aucune tuile ; un Gardien sauvé par Bouclier de lisière reste un pari perdu).</li>
        </ul>

        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-amber-900 mb-2">Partition stricte des 6 icônes (1 événement = au plus 1 icône)</h4>
          <div class="overflow-x-auto border border-amber-200 rounded-xl bg-white">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-amber-900 text-white">
                <tr>
                  <th class="p-2 w-32">Icône (gauche → droite)</th>
                  <th class="p-2 w-36">Moment</th>
                  <th class="p-2">Condition exacte d’allumage</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-amber-100 text-slate-700">
                <tr>
                  <td class="p-2 font-bold text-amber-950">🛡️ Parade</td>
                  <td class="p-2">Attaques</td>
                  <td class="p-2">Frappe bloquée par <strong>Défenseurs seuls</strong> (sans piège ni dépense d’Insecte).</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">🪤 Piégeage</td>
                  <td class="p-2">Attaques</td>
                  <td class="p-2">Frappe arrêtée par le <strong>Croc</strong> Reptile ou un <strong>Piège autonome</strong> (prioritaire sur Parade et Insecte).</td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">🔧 Sabotage</td>
                  <td class="p-2">Ouverture</td>
                  <td class="p-2">Un jeton <strong>Sabotage</strong> ou une <strong>Écaille</strong> est révélé à l’Ouverture des paravents.</td>
                </tr>
                <tr ${_livretModAttrs('REVES', showReves, '')}>
                  <td class="p-2 font-bold text-amber-950">🌙 Rêve</td>
                  <td class="p-2">Ouverture</td>
                  <td class="p-2">Un <strong>Rêve défendu</strong> annule au moins 1 machine de son rang (<strong>déviée ou non</strong>).</td>
                </tr>
                <tr ${_livretModAttrs('ESSAIM', showEssaim, '')}>
                  <td class="p-2 font-bold text-amber-950">🐜 Insecte</td>
                  <td class="p-2">Ouverture ou Attaques</td>
                  <td class="p-2">Un Insecte de la Réglette effectue une <strong>déviation ±1</strong> à l’Ouverture <strong>OU</strong> une Parade en forêt défausse au moins 1 Insecte. <em>(Icône inactive si les Insectes ne jouent pas.)</em></td>
                </tr>
                <tr>
                  <td class="p-2 font-bold text-amber-950">✨ Résonance</td>
                  <td class="p-2">Tout le tour</td>
                  <td class="p-2"><strong>6<sup>e</sup> et dernière icône :</strong> 1<sup>re</sup> activation du tour de chaque autre Gardien distinct (compteur individuel sans écrasement, aucune auto-alimentation).</td>
                </tr>
              </tbody>
            </table>
          </div>
          <p class="text-[11px] text-amber-950 mt-1.5">
            <strong>Hors déclencheurs :</strong> la Furtivité et la Production des Nids n’allument jamais aucune icône de la Piste des Gardiens.
          </p>
        </div>
      </div>

      <!-- MODULE RÊVES & SOMMEIL -->
      <div id="brique-reves-sommeil" ${_livretModAttrs('REVES', showReves, 'brique-card brique-card-purple scroll-mt-24 space-y-3')}>
        <div class="brique-header border-purple-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-purple-100 text-purple-950 border-purple-300">Module Rêves</span>
            <h3 class="text-lg font-bold text-purple-950">Rêves &amp; Sommeil du Contremaître (🏹 Humains, ✨ Entités Magiques)</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${tableNbReves > 0 ? 'bg-purple-200 text-purple-950' : 'bg-slate-200 text-slate-600'}">
            ${tableNbReves > 0 ? `${tableNbReves} tuiles Rêve sur votre table` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${tableNbReves > 0
            ? `<span class="dyn-span">Votre table comporte <strong>${tableNbReves} tuiles Rêve</strong> en jeu. Pour déclencher le <strong>Sommeil du Contremaître</strong> aux Tours 1 à 7, réunissez ces ${tableNbReves} tuiles en un bloc contigu sur les <strong>rangs 1 à ${tableNbReves}</strong> de la Réglette.</span>`
            : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Onirique autour de la table).</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Pose à droite sans éjection :</strong> tout Rêve construit se pose au-dessus du rang libre le plus à droite (<code>6</code>, puis <code>5</code>…) sans retirer l’action imprimée ni déplacer les Insectes présents.</li>
          <li><strong>Blocage &amp; choix du propriétaire :</strong> n’importe quel joueur peut défendre un Rêve dès le Premier déploiement ou au Second déploiement. À l’Ouverture (de gauche à droite), chaque Défenseur présent <strong>annule 1 machine</strong> choisie par le <strong>propriétaire du Rêve</strong> (y compris une machine déviée), résout le pouvoir propre du Rêve (actif dès que défendu même à 0 machine, sauf mention <em>« Quand ce Rêve annule… »</em>) puis allume l’icône <em>Rêve</em> si ≥ 1 machine a été annulée.</li>
          <li><strong>Glissements solidaires :</strong> lorsqu’un effet (comme le <em>Chant</em> Humain ou <em>Le Chant de l’Ibijau</em>) fait glisser un Rêve vers la gauche, il pousse avec lui tout bloc contigu de Rêves placé devant lui, et les Défenseurs posés sur ces Rêves se déplacent toujours avec eux.</li>
          <li><strong>Sommeil du Contremaître &amp; Enracinement :</strong> la victoire anticipée par Sommeil exige la totalité des <strong>2 × D</strong> tuiles Rêve (2 avec 1 Peuple Onirique, 4 avec 2 Peuples Oniriques) alignées sur les rangs <code>1</code> à <code>2D</code>. Dès qu’un seul Rêve est enraciné au Ménage, le Sommeil devient définitivement impossible pour le reste de la partie.</li>
        </ul>
      </div>

      <!-- MODULE ESSAIM -->
      <div id="brique-peuple-insectes" ${_livretModAttrs('ESSAIM', showEssaim, 'brique-card brique-card-lime scroll-mt-24 space-y-3.5')}>
        <div class="brique-header border-lime-200">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge bg-lime-100 text-lime-950 border-lime-300">Module Essaim</span>
            <h3 class="text-lg font-bold text-lime-950">Module Essaim (🐜 Insectes — Exclusif à ce Peuple)</h3>
          </div>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${tableEssaimActif ? 'bg-lime-200 text-lime-950' : 'bg-slate-200 text-slate-600'}">
            ${tableEssaimActif ? 'Actif sur votre table' : 'Inactif sans les Insectes'}
          </span>
        </div>

        <p class="text-sm text-slate-700" data-inv="INV-21">
          <strong>Clôture stricte du Module Essaim :</strong> les jetons <strong>Insectes</strong> sont exclusivement liés aux 10 tuiles des 5 lisières des Insectes. Dès que les Insectes ne participent pas à la partie, tous les jetons Insectes restent dans la <strong>boîte</strong>, la Production et la Migration sont ignorées et l’icône <em>Insecte</em> reste inactive. Lorsque les Insectes jouent, tout Insecte <strong>passager</strong> monté sur une machine (<em>La Fourmilière Coupe-Feuilles</em>) et non dépensé pendant les attaques descend sur place au Ménage.
        </p>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">1. 🍯 Nids &amp; Production</div>
            <p class="text-slate-700">Nid défendu = <code>+1</code> Insecte (0–1 présent) ou <code>+2</code> (≥ 2 présents), sans allumer <em>Insecte</em>, puis pouvoir <em>« Après production »</em>.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">2. 🔄 Migration double sens</div>
            <p class="text-slate-700">Rayon par rayon : 0 ou 1 cran vers le cœur ou la bordure (saute les Routes), ou sortie depuis la dernière parcelle vers un rang 1–6 ou une icône Gardien.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">3. 🎲 Déviation de dé (±1)</div>
            <p class="text-slate-700">À l’Ouverture, défaussez 1 Insecte d’un rang de la Réglette pour décaler le dé d’une machine de <strong>−1 ou +1 rang</strong> (entre 1 et 6) → allume <em>Insecte</em>.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">4. 🛡️ Parade Insecte</div>
            <p class="text-slate-700">Défaussés à la volée pendant une attaque pour compléter le Seuil de Parade d’une parcelle → allume <em>Insecte</em>.</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3" data-inv="INV-18">
            <div class="font-bold text-lime-950 mb-1">5. 🌿 Bouclier de lisière (facultatif)</div>
            <p class="text-slate-700">En fin d’attaques, si un Gardien perd son pari et porte au moins 1 Insecte sur son icône, le joueur <strong>Insectes choisit</strong> librement de défausser ou non 1 Insecte pour le garder en piste sur sa face actuelle (le pari reste perdu).</p>
          </div>
          <div class="bg-white border border-lime-200 rounded-xl p-3">
            <div class="font-bold text-lime-950 mb-1">6. 🐞 Insecte passager</div>
            <p class="text-slate-700">Un Insecte embarqué sur une machine défend chaque parcelle qu’elle frappe ; s’il n’est pas dépensé, il descend sur place au Ménage.</p>
          </div>
        </div>
      </div>

      <!-- FIN DE PARTIE & REPOUSSE PAR ENRACINEMENT -->
      <div id="sec-fin" class="brique-card scroll-mt-24 space-y-3.5">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Fin de partie</span>
            <h3 class="text-lg font-bold text-forest-950">Fin de partie &amp; Repousse par Enracinement</h3>
          </div>
          <span class="text-xs font-mono text-forest-700">Score collectif en % d’Arbres debout</span>
        </div>

        <p class="text-sm text-slate-700">
          La fin de partie se teste uniquement <strong>en fin d’attaques</strong> (après le verdict des paris Gardiens). Dès qu’une issue est atteinte, ignorez le Ménage et procédez au décompte final :
        </p>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-2.5 text-xs">
          <div class="p-3 rounded-xl bg-slate-50 border border-slate-200">
            <div class="font-bold text-slate-900">1. Fin du 8<sup>e</sup> tour</div>
            <p class="text-slate-600 mt-0.5">Priorité absolue au terme des attaques du Tour 8.</p>
          </div>
          <div ${_livretModAttrs('REVES', showReves, 'p-3 rounded-xl bg-purple-50/70 border border-purple-200')}>
            <div class="font-bold text-purple-950">2. Sommeil du Contremaître</div>
            <p class="text-slate-700 mt-0.5">
              ${tableNbReves > 0
                ? `<span class="dyn-span">Tours 1 à 7 (prioritaire sur l’Éveil) : les <strong>${tableNbReves} tuiles Rêve</strong> réunies en bloc contigu sur les <strong>rangs 1 à ${tableNbReves}</strong> (aucun Rêve enraciné).</span>`
                : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Onirique autour de la table).</span>'}
            </p>
          </div>
          <div ${_livretModAttrs('GARDIENS', showGardiens, 'p-3 rounded-xl bg-amber-50/70 border border-amber-200')}>
            <div class="font-bold text-amber-950">3. Éveil de la Forêt</div>
            <p class="text-slate-700 mt-0.5">
              ${tableGardiensActif
                ? `<span class="dyn-span">Tours 1 à 7 : les <strong>${n} joueurs</strong> ont tous misé leur deuxième pion sur les Gardiens et <strong>tous les paris du tour sont gagnés</strong>.</span>`
                : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Animal Sauvage autour de la table).</span>'}
            </p>
          </div>
        </div>

        <div class="bg-emerald-50 border-2 border-emerald-300 rounded-xl p-4 text-sm text-emerald-950 space-y-1.5">
          <div class="font-bold text-emerald-900">🌱 Décompte final &amp; repousse par Enracinement</div>
          <p class="text-xs sm:text-sm leading-relaxed">
            Il n’existe <strong>aucune repousse automatique de base</strong> : une Souche seule ne vaut aucun point. Avant de compter vos arbres, appliquez vos <strong>tuiles enracinées</strong> : chaque tuile glissée au pied d’un rayon face à une parcelle qui n’est pas devenue Route Forestière y retourne <strong>1 Souche</strong> survivante sur sa face <em>Arbre debout</em> (ou <strong>2 Souches</strong> si elle a été enracinée depuis sa <strong>Face 2</strong>), ainsi que son éventuelle clause <em>« Enraciné : »</em>. Additionnez enfin tous les <strong>Arbres encore debout</strong> sur le plateau : votre score collectif est le nombre et le <strong>pourcentage d’Arbres sauvés</strong> sur <span class="dyn-span"><strong>${totalArbres} Arbres</strong></span> initiaux !
          </p>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- SECTION 5 : LES 6 PEUPLES — ASYMÉTRIE HYBRIDE 3 + 3                 -->
    <!-- =================================================================== -->
    <section id="sec-peuples" class="mb-10 scroll-mt-24 space-y-5" data-inv="INV-20">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        5. Les 6 Peuples : Asymétrie Hybride 3 + 3
      </h2>

      <p class="text-sm text-slate-700 leading-relaxed">
        Chaque Peuple possède une identité matérielle unique selon un équilibre <strong>3 + 3</strong> : <strong>trois Peuples</strong> entrent en jeu dès le Tour 1 avec un accessoire actif sur la table (<strong>Humains</strong>, <strong>Mammifères</strong>, <strong>Oiseaux</strong>), tandis que <strong>trois Peuples</strong> montent en puissance via une réserve dédiée mobilisée par leurs Tuiles de Synergie (<strong>Entités Magiques</strong>, <strong>Reptiles</strong>, <strong>Insectes</strong>).
      </p>

      <!-- GROUPE A : ACTIFS TOUR 1 -->
      <div class="${showGroupTour1 ? 'space-y-3' : 'hidden livret-hidden'}">
        <h3 class="text-base font-bold text-forest-900 flex items-center gap-2">
          <span class="px-2 py-0.5 rounded-full text-xs bg-emerald-100 text-emerald-900">Groupe 1</span>
          <span>3 Peuples à accessoire actif dès le Tour 1</span>
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs text-slate-700">
          <div ${_livretPeupleAttrs('H', isPeupleVisible('H'), 'livret-peuple-card border-t-4 border-t-rose-500 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-rose-950">🏹 Humains</div>
              <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-900 font-semibold">Onirique · Rêves</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> 2 pions Chamanes recto-verso uniques (<strong>1 Tambour</strong> et <strong>1 Chant</strong>) + leurs 2 fiches d’archétype. Poser l’un au Premier déploiement laisse automatiquement l’autre en main pour le Second déploiement.</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Tambour :</strong> au Premier déploiement, le Tambour peut aussi être posé sur une parcelle de <strong>n’importe quel autre Peuple</strong>.</li>
              <li><strong>Chant :</strong> à l’Ouverture, si un Rêve portant le Chant annule au moins 1 machine et qu’aucune machine n’y reste active, ce Rêve <strong>glisse immédiatement d’1 rang vers la gauche</strong> (poussant tout bloc contigu, Défenseurs solidaires).</li>
            </ul>
          </div>

          <div ${_livretPeupleAttrs('M', isPeupleVisible('M'), 'livret-peuple-card border-t-4 border-t-amber-500 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-amber-950">🐆 Mammifères</div>
              <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-900 font-semibold">Animal · Gardiens</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> 1 jeton <strong>Duel</strong> recto-verso (<em>Défi</em> ↔ <em>Territoire tenu</em>).</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Pose &amp; ajustement :</strong> posé ou déplacé face <em>Défi</em> avec un Défenseur Mammifère en forêt (ajustable tant que le deuxième pion est en <em>Réflexion</em>, figé irréversiblement sur <em>Définitif</em>).</li>
              <li><strong>Territoire tenu :</strong> dès qu’une frappe sur sa parcelle est parée par au moins 1 Défenseur, retournez le Duel sur <strong>Territoire tenu</strong> : il bloque l’avancée de toute machine présente sur cette parcelle aux rangs 3 et 6. Une frappe non parée et non piégée (ou la création d’une Route) le renvoie en réserve.</li>
            </ul>
          </div>

          <div ${_livretPeupleAttrs('O', isPeupleVisible('O'), 'livret-peuple-card border-t-4 border-t-sky-500 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-sky-950">🦜 Oiseaux</div>
              <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-900 font-semibold">Animal · Gardiens</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> 1 <strong>Dé d’Envol</strong> (1–6), 1 <strong>Perchoir de Vigie</strong> à plat devant le paravent, 1 jeton <strong>Plume de Vigie</strong> recto-verso (<em>Chaud</em> ↔ <em>Calme</em>).</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Éclaireur du ciel :</strong> toujours servi en dernier à la pioche, l’Oiseau regarde jusqu’à 2 jetons du sac, en garde 1 si possible et pose l’autre face cachée sur son Perchoir jusqu’au Ménage.</li>
              <li><strong>Double horizon :</strong> sous paravent, s’il détient un jeton Machine, il choisit secrètement entre le plus petit de ses 2 dés standards ou la valeur exacte de son <em>Dé d’Envol</em>.</li>
              <li><strong>Signal de Vigie :</strong> sous paravents fermés, il pose ou ajuste la <strong>Plume</strong> (<em>Chaud</em> ou <em>Calme</em>) au pied d’un rayon ou près d’un rang 1–6 (figée avec son deuxième pion).</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- GROUPE B : PROGRESSIFS VIA TUILES -->
      <div class="${showGroupProgressif ? 'space-y-3' : 'hidden livret-hidden'}">
        <h3 class="text-base font-bold text-forest-900 flex items-center gap-2">
          <span class="px-2 py-0.5 rounded-full text-xs bg-purple-100 text-purple-900">Groupe 2</span>
          <span>3 Peuples à réserve progressive via Tuiles de Synergie</span>
        </h3>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 text-xs text-slate-700">
          <div ${_livretPeupleAttrs('E', isPeupleVisible('E'), 'livret-peuple-card border-t-4 border-t-purple-500 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-purple-950">✨ Entités Magiques</div>
              <span class="px-2 py-0.5 rounded bg-purple-100 text-purple-900 font-semibold">Onirique · Rêves</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> jetons d’<strong>Altération</strong> en réserve.</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Altérer une machine :</strong> posez 1 jeton d’<strong>Altération</strong> directement sur une machine mobile qui n’en porte pas encore (<strong>maximum 1 par machine</strong> ; jamais en Ratissage).</li>
              <li><strong>Déclenchement à l’Ouverture :</strong> à la prochaine Ouverture où le jeton de cette machine est révélé, retirez son jeton d’Altération : elle compte normalement dans la mobilisation <em>m(r)</em> de son rayon, mais <strong>recule d’1 parcelle sans frapper</strong> ce tour-ci. Si la machine passe en Ratissage ou si son rayon est 100 % rasé, le jeton d’Altération retourne en réserve.</li>
            </ul>
          </div>

          <div ${_livretPeupleAttrs('R', isPeupleVisible('R'), 'livret-peuple-card border-t-4 border-t-emerald-600 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-emerald-950">🐍 Reptiles</div>
              <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 font-semibold">Animal · Gardiens</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> <strong>4 jetons Sabotage « Écaille »</strong> (même gabarit que les jetons du sac) et <strong>1 jeton Piège spécial « Croc »</strong>.</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Écaille :</strong> ajoutée au sac par vos tuiles, une <strong>Écaille</strong> révélée à l’Ouverture allume l’icône <em>Sabotage</em> puis le joueur Reptile pose le <em>Croc</em> sur une parcelle ciblée (l’Écaille retourne au sac au Ménage).</li>
              <li><strong>Croc réutilisable &amp; Cale :</strong> le <em>Croc</em> peut cohabiter avec un Piège ordinaire, pare <strong>en premier</strong> 1 frappe (allume <em>Piégeage</em>) puis revient en réserve Reptile. Via <em>Le Guet du Caïman noir</em>, vous pouvez aussi glisser au plus <strong>1 cale</strong> (Sabotage ou Écaille) sous une machine mobile pour annuler sa prochaine avancée avant qu’elle rejoigne le sac.</li>
            </ul>
          </div>

          <div ${_livretPeupleAttrs('I', isPeupleVisible('I'), 'livret-peuple-card border-t-4 border-t-lime-600 space-y-2')}>
            <div class="flex items-center justify-between">
              <div class="font-bold text-sm text-lime-950">🐜 Insectes</div>
              <span class="px-2 py-0.5 rounded bg-lime-100 text-lime-900 font-semibold">Symbiotique · Essaim</span>
            </div>
            <p class="text-slate-600"><strong>Matériel :</strong> jetons <strong>Insectes</strong> double face et 5 Nids sur les 10 tuiles des 5 lisières des Insectes.</p>
            <ul class="list-disc pl-4 space-y-1">
              <li><strong>Essaim exclusif :</strong> gouverne la Production des Nids (+1/+2), la Migration radiale dans les deux sens et vers les pistes centrales, la Déviation ±1 à l’Ouverture et la Parade Insecte en forêt.</li>
              <li><strong>Bouclier &amp; Passager :</strong> choisit librement d’activer ou non le <em>Bouclier de lisière</em> sur un Gardien ayant perdu son pari, et gère la descente sur place au Ménage de tout <em>Insecte passager</em> non dépensé.</li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- SECTION 6 : MÉMENTO DE TABLE & ARBITRAGES DE RÉFÉRENCE              -->
    <!-- =================================================================== -->
    <section id="sec-memento" class="page-break mb-4 scroll-mt-24 space-y-4">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        6. Mémento de table &amp; Arbitrages de référence
      </h2>

      <div id="brique-memento" class="brique-card scroll-mt-24 space-y-4">
        <div class="brique-header">
          <div class="flex items-center gap-2.5 flex-wrap">
            <span class="brique-badge">Aide de jeu</span>
            <h3 class="text-lg font-bold text-forest-950">Mémento de table imprimable</h3>
          </div>
          <span class="text-xs font-mono text-forest-700">Fiche synthèse · Table à ${n} joueurs</span>
        </div>

        <!-- SYNTHÈSE ULTRA-RAPIDE D'UN TOUR -->
        <div class="bg-forest-50/70 border border-forest-200 rounded-xl p-3 text-xs">
          <div class="font-bold uppercase tracking-wider text-forest-900 mb-1.5">⏱️ Rythme d’un tour en 6 temps</div>
          <ol class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-1.5 list-decimal pl-4 text-slate-700">
            <li><strong>Préparation :</strong> bandelette Face B au Tour 5 · pioche au sac (Oiseau dernier) · tous lancent les dés.</li>
            <li><strong>Déploiement muet :</strong> 1<sup>er</sup> pion face <em>Définitif</em><span ${_livretModAttrs('GARDIENS', showGardiens, '')}> (jamais Gardiens)</span> · 2<sup>e</sup> pion <em>Réflexion → Définitif</em> (clôture N−1).</li>
            <li><strong>Ouverture :</strong> constructions (bâtisseurs en attente) · Sabotages/Écailles<span ${_livretModAttrs('ESSAIM', showEssaim, '')}> → Déviations ±1</span><span ${_livretModAttrs('REVES', showReves, '')}> → Rêves gauche → droite</span>.</li>
            <li><strong>Furtivité<span ${_livretModAttrs('ESSAIM', showEssaim, '')}> &amp; Essaim</span> :</strong> Rive Piège (<code>m=2</code>) / Rive Sabotage (<code>m=0</code>)<span ${_livretModAttrs('ESSAIM', showEssaim, '')}> · Production Nids → Migration double sens</span>.</li>
            <li><strong>Attaques &amp; Verdict :</strong> rangs 1–6 puis Ratissage (Abatteuse avant Bulldozer)<span ${_livretModAttrs('GARDIENS', showGardiens, '')}> · verdict paris</span> · test de fin.</li>
            <li><strong>Ménage :</strong> retour pions · Enracinement volontaire · passage en Ratissage (+1 rouge) · remise au sac.</li>
          </ol>
        </div>

        <!-- RÉGLETTE DES TACTIQUES + BANDELETTE + RATISSAGE -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-forest-800 mb-1.5">Réglette fixe 1–6, bandelette d’Acte (Face A / Face B) &amp; Ratissage</h4>
          <div class="overflow-x-auto border border-slate-200 rounded-xl">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-forest-900 text-white">
                <tr>
                  <th class="p-2">Rang</th>
                  <th class="p-2">Action fixe</th>
                  <th class="p-2">Parcelles ciblées</th>
                  <th class="p-2">Modif. Seuil</th>
                  <th class="p-2">Avancée</th>
                  <th class="p-2">Acte 1 (Tours 1–4 · Face A)</th>
                  <th class="p-2">Acte 2 (Tours 5–8 · Face B)</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 text-slate-700">
                <tr>
                  <td class="p-1.5 font-bold">1</td>
                  <td class="p-1.5 font-semibold">Sur place</td>
                  <td class="p-1.5">Parcelle actuelle</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">2</td>
                  <td class="p-1.5 font-semibold">Devant</td>
                  <td class="p-1.5">Prochaine parcelle vers le cœur</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">3</td>
                  <td class="p-1.5 font-semibold">En avançant</td>
                  <td class="p-1.5">Sur place, puis Devant</td>
                  <td class="p-1.5 font-semibold">−1</td>
                  <td class="p-1.5">+1 parcelle (sauf repli cœur)</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">4</td>
                  <td class="p-1.5 font-semibold">Sur place</td>
                  <td class="p-1.5">Parcelle actuelle</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">5</td>
                  <td class="p-1.5 font-semibold">Devant</td>
                  <td class="p-1.5">Prochaine parcelle vers le cœur</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr>
                  <td class="p-1.5 font-bold">6</td>
                  <td class="p-1.5 font-semibold">En avançant</td>
                  <td class="p-1.5">Sur place, puis Devant</td>
                  <td class="p-1.5 font-semibold">−1</td>
                  <td class="p-1.5">+1 parcelle (sauf repli cœur)</td>
                  <td class="p-1.5 font-semibold text-rose-800 bg-rose-50/70">🔥 Assaut</td>
                  <td class="p-1.5 font-semibold text-amber-800 bg-amber-50/70">⚡ Charge</td>
                </tr>
                <tr class="bg-slate-100/90 border-t-2 border-slate-300">
                  <td class="p-1.5 font-bold text-slate-900">★</td>
                  <td class="p-1.5 font-bold text-slate-900">Ratissage <em>(hors sac)</em></td>
                  <td class="p-1.5">Sur place (immobile · parcelle ciblée)</td>
                  <td class="p-1.5">0</td>
                  <td class="p-1.5">—</td>
                  <td class="p-1.5 font-bold text-rose-900 bg-rose-100/70" colspan="2">🔥 Assaut permanent (+1 jeton rouge physique à l’entrée, tous jetons actifs, 0 gain)</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- FORMULE DU SEUIL & CHAÎNE DE FRAPPE -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <h4 class="font-bold uppercase tracking-wider text-forest-800">⚔️ Formule du Seuil &amp; Chaîne de frappe</h4>
            <p class="font-semibold text-slate-900">
              Seuil = Chiffre gravé + Rouges (Assaut/Ratissage seuls) − Bleus Surchauffe (TOUS modes) − 1 aux rangs 3 &amp; 6 (min 1).
            </p>
            <ol class="list-decimal pl-4 space-y-1 text-slate-700">
              <li><strong>Piège :</strong> <em>Croc</em> en premier (retourne en réserve Reptile), sinon <em>Piège autonome</em> (défaussé aussitôt) → icône <em>Piégeage</em>.</li>
              <li><strong>Parade classique :</strong> Défenseurs seuls → icône <em>Parade</em><span ${_livretModAttrs('ESSAIM', showEssaim, '')}> ; avec défausse d’Insectes → icône <em>Insecte</em></span>.</li>
              <li><strong>Non parée :</strong> Abatteuse retourne <strong>tous les Arbres</strong> en Souches (0 Souche retirée) ; Bulldozer = 1 Arbre + toutes Souches (0/0 = Route). En <em>Charge</em> : +1 rouge max/activation.</li>
            </ol>
          </div>

          <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-1.5">
            <h4 class="font-bold uppercase tracking-wider text-forest-800">🎯 Furtivité<span ${_livretModAttrs('GARDIENS', showGardiens, '')}> &amp; 6 Icônes Gardiens</span></h4>
            <ul class="list-disc pl-4 space-y-1 text-slate-700">
              <li><strong>Rive Piège (Chaud, m = 2) :</strong> le propriétaire du rayon pose 1 Piège ordinaire sur son rayon (sinon perdu sans compensation).</li>
              <li><strong>Rive Sabotage (Calme, m = 0) :</strong> +1 jeton Sabotage au sac opaque.</li>
              <li ${_livretModAttrs('GARDIENS', showGardiens, '')}><strong>6 icônes (gauche → droite) :</strong> <em>Parade · Piégeage · Sabotage · Rêve · Insecte · Résonance</em> (compteur individuel, reprise à gauche).</li>
              <li ${_livretModAttrs('GARDIENS', showGardiens, '')}><strong>Jamais d’icône :</strong> Furtivité<span ${_livretModAttrs('ESSAIM', showEssaim, '')}> et Production des Nids</span> n’allument jamais la Piste des Gardiens.</li>
            </ul>
          </div>
        </div>

        <!-- TABLEAU DES ARBITRAGES & CAS LIMITES DE RÉFÉRENCE -->
        <div>
          <h4 class="text-xs font-bold uppercase tracking-wider text-forest-800 mb-1.5">⚖️ Tableau des arbitrages &amp; cas limites de référence</h4>
          <div class="overflow-x-auto border border-slate-200 rounded-xl">
            <table class="w-full text-xs text-left border-collapse">
              <thead class="bg-slate-800 text-white">
                <tr>
                  <th class="p-2 w-48">Situation à la table</th>
                  <th class="p-2">Arbitrage officiel</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-slate-200 text-slate-700">
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Pénurie dans le sac opaque</td>
                  <td class="p-2">Distribution horaire à partir du Coordonnateur, <strong>Oiseau toujours servi en dernier</strong> (regarde jusqu’à 2 jetons, garde 1, pose l’autre sur son Perchoir).</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Jeton Sabotage / Écaille tiré</td>
                  <td class="p-2">Le joueur lance quand même ses dés sous mini-paravent (jet ignoré, zéro fuite sonore) ; à l’Ouverture, allume <em>Sabotage</em> (+ pose du <em>Croc</em> sur Écaille).</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Tuile de lisière impossible à placer</td>
                  <td class="p-2">Interdit de poser le 2<sup>e</sup> bâtisseur. Si aucun coup légal au Premier déploiement, repli autorisé sur une parcelle d’un allié.</td>
                </tr>
                <tr ${_livretModAttrs('REVES', showReves, '')}>
                  <td class="p-2 font-semibold text-slate-900">Plusieurs machines sur un Rêve défendu</td>
                  <td class="p-2">Le <strong>propriétaire du Rêve</strong> choisit quelle(s) machine(s) annuler (y compris déviées). Pouvoir propre actif même à 0 machine sauf <em>« Quand ce Rêve annule… »</em>.</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Jeton Machine annulé / altéré &amp; Furtivité</td>
                  <td class="p-2">Reste visible devant son rayon (incliné à <strong>90°</strong> si annulé) jusqu’à la Furtivité et compte toujours dans <em>m(r)</em>.</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Cible devenue Route &amp; En avançant</td>
                  <td class="p-2">Cibles figées au début de l’activation : cible devenue Route = annulée sans report. Si un repli de bordure pousse déjà la machine d’1 parcelle vers le cœur, il couvre l’avancée (0 double bond).</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Contact machine vs Création de Route</td>
                  <td class="p-2">Hors Route, Nids, Insectes, Pièges et Duel restent intacts. Sur création de Route : Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve.</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Enracinement &amp; Sommeil</td>
                  <td class="p-2">Max 1 tuile construite/joueur/tour au Ménage (1 Souche en Face 1/unique ou 2 en Face 2 au décompte final) ; enraciner un Rêve rend le Sommeil impossible.</td>
                </tr>
                <tr>
                  <td class="p-2 font-semibold text-slate-900">Sommeil et Éveil au même tour</td>
                  <td class="p-2">Aux Tours 1 à 7, le <strong>Sommeil du Contremaître</strong> l’emporte sur l’Éveil de la Forêt. Au Tour 8, la fin temporelle a toujours la priorité absolue.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  `;

  const container = typeof document.getElementById === 'function'
    ? document.getElementById('rulebook-article')
    : null;
  if (container) {
    container.innerHTML = html;
  }
  return html;
}
