"""Tests headless Node vm dédiés à l'Explorateur de Tuiles v6.2 & aux 197 Assises.

Vérifie sans dépendance npm :
1. Encodage UTF-8 sans BOM, fins de lignes LF et syntaxe JS valide via `new vm.Script()`.
2. Énumération exacte des 197 assises uniques (20 à N=3, 45 à N=4, 72 à N=5, 60 à N=6)
   et invariance diédrale (rotation + symétrie miroir).
3. Sélection des 2N tuiles et tableau de bord de santé sur les tables témoins clés
   (`N3-HEI`, `N3-ERI`, `N3-MRO`, `N6-HEMROI`) et 0 alerte sur l'ensemble des 197 assises Canon 0.
4. Ordre canonique v6.2 des 6 icônes Gardiens `[PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE]`
   et normalisation stricte des anciens entiers `declencheurs_amorces` (`5 -> ICONE_REVE`,
   `6 -> ICONE_INSECTE`, jamais `6 -> ICONE_RESONANCE`).
5. Rendu HTML sans erreur (zéro `NaN`/`undefined`) des 3 Modes (`lisieres`, `assises`, `peuples`),
   du tiroir Capot Concepteur, des filtres multi-critères, des puces d'états et du graphe Rayons X.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"
EXPLORER_JS = ROOT / "docs" / "explorer_v6_2.js"
EXPLORER_CSS = ROOT / "docs" / "explorer_v6_2.css"


_NODE_EXPLORER_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, explorerPath] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const explorerJs = fs.readFileSync(explorerPath, 'utf8');

// Vérification syntaxique stricte via new vm.Script()
new vm.Script(explorerJs, { filename: explorerPath });

const inlineScripts = [];
for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
  inlineScripts.push(m[1]);
}
if (inlineScripts.length === 0) {
  throw new Error('Aucun script inline trouvé dans docs/index.html');
}

function makeElement(id) {
  const classes = new Set();
  return {
    id,
    _innerHTML: '',
    _textContent: '',
    value: id === 'changelog-filter-select' ? 'ALL'
         : id === 'diff-version-select' ? 'v6.1'
         : id === 'filter-family' || id === 'filter-peuple' || id === 'filter-scope' ? 'ALL'
         : id === 'filter-profile-letter' ? 'ALL_COMPARE'
         : '',
    className: '',
    options: [],
    style: {},
    classList: {
      add: (...cs) => cs.forEach(c => classes.add(c)),
      remove: (...cs) => cs.forEach(c => classes.delete(c)),
      toggle: (c) => (classes.has(c) ? classes.delete(c) : classes.add(c)),
      contains: (c) => classes.has(c),
    },
    get innerHTML() { return this._innerHTML; },
    set innerHTML(v) { this._innerHTML = String(v); },
    get textContent() { return this._textContent; },
    set textContent(v) { this._textContent = String(v); },
    addEventListener: () => {},
    querySelectorAll: () => [],
    querySelector: () => null,
    focus: () => {},
    setSelectionRange: () => {},
    scrollIntoView: () => {},
    click: () => {},
  };
}

const elements = new Map();
function getEl(id) {
  if (!elements.has(id)) elements.set(id, makeElement(id));
  return elements.get(id);
}

const docListeners = {};
const sandbox = {
  console,
  Math,
  JSON,
  Object,
  Array,
  String,
  Number,
  Boolean,
  Set,
  Map,
  RegExp,
  Date,
  Error,
  TypeError,
  parseInt,
  parseFloat,
  isNaN,
  encodeURIComponent,
  decodeURIComponent,
  setTimeout: () => 0,
  clearTimeout: () => {},
  localStorage: { _m: {}, getItem(k) { return this._m[k] || null; }, setItem(k, v) { this._m[k] = String(v); } },
  navigator: { clipboard: { writeText: async () => {} } },
  location: { protocol: 'file:', href: 'file:///docs/index.html' },
  fetch: async () => ({ ok: false, json: async () => ({}) }),
  tailwind: {},
  document: {
    getElementById: (id) => getEl(id),
    addEventListener: (ev, fn) => { docListeners[ev] = fn; },
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: (tag) => makeElement(tag),
  },
  window: {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

// Charger dans l'ordre exact de docs/index.html
vm.runInContext(dataJs, sandbox, { filename: dataPath });
vm.runInContext(livretJs, sandbox, { filename: livretPath });
vm.runInContext(explorerJs, sandbox, { filename: explorerPath });
for (let i = 0; i < inlineScripts.length; i++) {
  vm.runInContext(inlineScripts[i], sandbox, { filename: `docs/index.html#script${i}` });
}

const exp = sandbox.AmazoniaExplorerV62;
if (!exp) throw new Error('AmazoniaExplorerV62 non exposé sur window');

// 1. Énumération des 197 assises uniques & symétrie diédrale
const all197 = exp.enumerateAll197Assises();
const countsByN = { 3: 0, 4: 0, 5: 0, 6: 0 };
const uniqueKeys = new Set();
let totalAlerts197 = 0;
for (const a of all197) {
  countsByN[a.n]++;
  uniqueKeys.add(a.key);
  const h = exp.computeAssiseHealth(a.peuples);
  totalAlerts197 += h.alerts.length;
}

// Vérifier l'invariance rotation + miroir sur un échantillon N=4 et N=6
const rotCanon1 = exp.canonicalizeAssise(['H', 'E', 'M', 'R']);
const rotCanon2 = exp.canonicalizeAssise(['M', 'R', 'H', 'E']);
const mirCanon3 = exp.canonicalizeAssise(['R', 'M', 'E', 'H']);
const rotTiles1 = exp.getAssiseTilesAndBorders(['H', 'E', 'M', 'R']).tileIds.slice().sort();
const mirTiles3 = exp.getAssiseTilesAndBorders(['R', 'M', 'E', 'H']).tileIds.slice().sort();

// 2. Santé & tuiles des 4 tables témoins clés
const benchmarkResults = {};
for (const [k, circle] of [
  ['N3-HEI', ['H', 'E', 'I']],
  ['N3-ERI', ['E', 'R', 'I']],
  ['N3-MRO', ['M', 'R', 'O']],
  ['N6-HEMROI', ['H', 'E', 'M', 'R', 'O', 'I']],
]) {
  const h = exp.computeAssiseHealth(circle);
  benchmarkResults[k] = {
    canonKey: h.canonKey,
    assiseIndex: h.assiseIndex,
    tileIds: h.tileIds.slice().sort(),
    guardiansCount: h.guardiansCount,
    revesCount: h.revesCount,
    nidsCount: h.nidsCount,
    modules: h.modules,
    twists: h.twists,
    loisPassives: h.loisPassives,
    loisAlert: h.loisAlert,
    catalyseursEveil: h.catalyseursEveil,
    catalyseurAlert: h.catalyseurAlert,
    leviersReve: h.leviersReve,
    levierAlert: h.levierAlert,
    alertsCount: h.alerts.length,
    synergyChainsCount: h.synergyChains.length,
    disjointMajorCount: h.disjointMajorCount,
    iconOrder: h.iconCoverage.map(ic => ic.id),
  };
}

// 3. Garde-fou 6 icônes Gardiens v6.2 & normalisation pré-v6.2
const iconOrderV62 = exp.GUARDIAN_ICONS_V62.map(ic => ic.id);
const normChecks = {
  n1: exp.normalizeDeclencheurToIconId(1),
  n2: exp.normalizeDeclencheurToIconId(2),
  n3: exp.normalizeDeclencheurToIconId(3),
  n4: exp.normalizeDeclencheurToIconId(4),
  n5: exp.normalizeDeclencheurToIconId(5),
  n6: exp.normalizeDeclencheurToIconId(6),
  R1: exp.getNormalizedTileTriggers('R1'),
  G12: exp.getNormalizedTileTriggers('G12'),
  G13: exp.getNormalizedTileTriggers('G13'),
  M4: exp.getNormalizedTileTriggers('M4'),
  M5: exp.getNormalizedTileTriggers('M5'),
};

// 4. Rendu des 3 Modes, Capot, Filtres et Rayons X
sandbox.refreshAllUI();
const badTokenRe = /\b(?:NaN|undefined)\b/;

// Mode 1 : Les 15 Lisières
exp.setMode('lisieres');
const m1Toolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const m1Grid = getEl('catalogue-grid').innerHTML;
const m1Badge = getEl('catalogue-count-badge').textContent;
const m1BordersCount = (m1Grid.match(/data-border="/g) || []).length;
const m1TilesCount = (m1Grid.match(/data-tile-id="/g) || []).length;
const m1FluidCount = (m1Grid.match(/100 % fluide/g) || []).length;
const m1EnracCount = (m1Grid.match(/data-enracine-cartouche="true"/g) || []).length;
const m1HasBad = badTokenRe.test(m1Toolbar + '\n' + m1Grid);

// Vérifier l'ordre exact des 6 icônes dans toutes les 15 rampes Gardiens rendues
const allRamps = Array.from(m1Grid.matchAll(/data-guardian-ramp="v6\.2"[\s\S]*?<div class="exp-faces-stack">/g));
const rampIconsRendered = allRamps.length > 0
  ? Array.from(allRamps[0][0].matchAll(/data-icon-id="([^"]+)"/g)).map(x => x[1])
  : [];
const all15RampsValid = allRamps.length === 15 && allRamps.every(rm => {
  const ids = Array.from(rm[0].matchAll(/data-icon-id="([^"]+)"/g)).map(x => x[1]);
  return JSON.stringify(ids) === JSON.stringify(iconOrderV62) && rm[0].includes('exp-ramp-star');
});
const face2EnracCount = (m1Grid.match(/2 Souches si enraciné/g) || []).length;

// Vérifier le Capot Concepteur (replié par défaut -> déplié à la demande)
const capotHiddenInitially = m1Grid.includes('exp-capot-body is-hidden');
exp.toggleAllCapots();
const m1GridCapotOpen = getEl('catalogue-grid').innerHTML;
const capotExpandedAll = !m1GridCapotOpen.includes('exp-capot-body is-hidden')
  && m1GridCapotOpen.includes('ACTIVE_VERIFIED')
  && m1GridCapotOpen.includes('Phase 5')
  && m1GridCapotOpen.includes('vivier Phase 5');
exp.toggleAllCapots();

// Mode 2 : Table & Roue des 197 Assises
exp.setMode('assises');
exp.selectPresetAssise('N3-HEI');
const m2HeiGrid = getEl('catalogue-grid').innerHTML;
const m2HeiToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const m2HeiHasSvg = m2HeiGrid.includes('class="exp-wheel-svg"') && m2HeiGrid.includes('N3-HEI');
const m2HeiModGardiensInactive = m2HeiGrid.includes('data-module="gardiens" data-active="false"');
const m2HeiHasBad = badTokenRe.test(m2HeiToolbar + '\n' + m2HeiGrid);

// Clic sur la roue (Peuple H) puis effacement
exp.selectWheelFilter('peuple', 'H');
const m2WheelFilteredTiles = (getEl('catalogue-grid').innerHTML.match(/data-tile-id="/g) || []).length;
exp.clearWheelFilter();

// Passer à N3-ERI puis N6-HEMROI
exp.selectPresetAssise('N3-ERI');
const m2EriHasR8 = getEl('catalogue-grid').innerHTML.includes('data-tile-id="R8"');
exp.selectPresetAssise('N6-HEMROI');
const m2N6Tiles = (getEl('catalogue-grid').innerHTML.match(/data-tile-id="/g) || []).length;

// Mode 3 : Grammaires par Peuple (3+3)
exp.setMode('peuples');
const peupleCounts = {};
let m3HasBad = false;
for (const pCode of ['H', 'E', 'M', 'R', 'O', 'I']) {
  exp.setPeupleTab(pCode);
  const gHtml = getEl('catalogue-grid').innerHTML;
  const tHtml = getEl('explorer-v6-2-toolbar').innerHTML;
  if (badTokenRe.test(gHtml + '\n' + tHtml)) m3HasBad = true;
  const outCount = (gHtml.match(new RegExp(`data-origin="${pCode}"`, 'g')) || []).length;
  const inCount = (gHtml.match(new RegExp(`data-neighbor="${pCode}"`, 'g')) || []).length;
  peupleCounts[pCode] = { out: outCount, in: inCount };
}

// 5. Rayons X des Synergies & touche Échap
exp.setMode('lisieres');
exp.toggleXRay('G7');
const xrayG7 = exp.computeXRayGraph('G7');
const xrayToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const xrayGrid = getEl('catalogue-grid').innerHTML;
const xrayHasFocus = xrayGrid.includes('exp-xray-focus') && xrayToolbar.includes('data-xray-focus="G7"');
const xrayHasUpAndDown = xrayGrid.includes('exp-xray-upstream') && xrayGrid.includes('exp-xray-downstream') && xrayGrid.includes('exp-xray-dimmed');
const xrayHasBad = badTokenRe.test(xrayToolbar + '\n' + xrayGrid);

// Simuler touche Échap
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'Escape' });
}
const xrayAfterEscape = exp.getState().xrayFocusId;

// Rayons X scopé sur N3-HEI en Mode 2 (aucun Gardien ne doit fuiter)
exp.setMode('assises');
exp.selectPresetAssise('N3-HEI');
exp.toggleXRay('R10');
const xrayHeiToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const xrayHeiNoGuardianLeak = !xrayHeiToolbar.includes('<strong>G13</strong>') && xrayHeiToolbar.includes('<strong>R2</strong>');
exp.clearXRay();

// 6. Filtres multi-critères & puces d'états cliquables
exp.setMode('lisieres');
exp.setFilter('role', 'TWIST');
const twistFilteredCount = (getEl('catalogue-grid').innerHTML.match(/data-tile-id="/g) || []).length;
exp.resetFilters();

exp.setFilter('role', 'LOI_PASSIVE');
const loiFilteredHtml = getEl('catalogue-grid').innerHTML;
const loiFilteredIds = Array.from(loiFilteredHtml.matchAll(/data-tile-id="([^"]+)"/g)).map(m => m[1]).sort();
exp.resetFilters();

exp.setFilter('icon', 'ICONE_INSECTE');
const insectIconIds = Array.from(getEl('catalogue-grid').innerHTML.matchAll(/data-tile-id="([^"]+)"/g)).map(m => m[1]).sort();
exp.resetFilters();

exp.toggleStateChipFilter('SOUCHE');
const soucheChipIds = Array.from(getEl('catalogue-grid').innerHTML.matchAll(/data-tile-id="([^"]+)"/g)).map(m => m[1]).sort();
exp.resetFilters();
const resetBadge = getEl('catalogue-count-badge').textContent;

// 7. Didacticiel visuel annoté « ? Guide de lecture » & infobulles décodées des vecteurs V1..V5
const guideInitialState = exp.getState().readingGuideOpen;
const guideInitialClosedInDom = !m1Toolbar.includes('id="exp-reading-guide-panel"')
  && m1Toolbar.includes('id="exp-reading-guide-btn"')
  && m1Toolbar.includes('aria-expanded="false"');

exp.toggleReadingGuide();
const guideOpenState = exp.getState().readingGuideOpen;
const guideOpenToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const guideOpenHasBad = badTokenRe.test(guideOpenToolbar);
const guideZones = Array.from(guideOpenToolbar.matchAll(/data-guide-zone="([1-6])"/g)).map(m => m[1]).sort();
const guideVectors = Array.from(guideOpenToolbar.matchAll(/data-guide-vector="(V[1-5])"/g)).map(m => m[1]);
const guideBubblesGardien = Array.from(guideOpenToolbar.matchAll(/class="exp-guide-bubble[^"]*" data-guide-spot="([1-9])"/g)).map(m => m[1]).sort();
const guidePinsGardien = Array.from(guideOpenToolbar.matchAll(/class="exp-guide-pin[^"]*" data-guide-spot="([1-9])"/g)).map(m => m[1]).sort();
const guideHasCloseBtn = guideOpenToolbar.includes('id="exp-reading-guide-close"');
const guideHasExpandedTrue = guideOpenToolbar.includes('aria-expanded="true"');
const guideHasDialogModal = guideOpenToolbar.includes('id="exp-reading-guide-backdrop"')
  && guideOpenToolbar.includes('role="dialog"')
  && guideOpenToolbar.includes('data-guide-specimen="G7"');

// Navigation pas-à-pas & aperçu Capot sur la Planche 1
exp.stepGuideSpot(1);
const guideStep1Spot = exp.getState().guideSpot;
const guideStep1ActiveDom = getEl('explorer-v6-2-toolbar').innerHTML.includes('has-active-spot')
  && getEl('explorer-v6-2-toolbar').innerHTML.includes('Point 1 / 9');
exp.toggleGuideCapotPreview();
const guideCapotPreviewShown = getEl('explorer-v6-2-toolbar').innerHTML.includes('Choix joueur');
exp.setGuideSpot(null);

// Planche 2 : Rêve (R6), Nid / Loi (M2), Twist (G15) & Rayons X
exp.setGuideTab('autres');
const guideTab2Toolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const guideTab2HasBad = badTokenRe.test(guideTab2Toolbar);
const guideTab2Bubbles = Array.from(guideTab2Toolbar.matchAll(/class="exp-guide-bubble[^"]*" data-guide-spot="([1-5])"/g)).map(m => m[1]).sort();
const guideTab2HasSpecimens = guideTab2Toolbar.includes('data-guide-specimen="R6"')
  && guideTab2Toolbar.includes('G15')
  && guideTab2Toolbar.includes('M2')
  && guideTab2Toolbar.includes('Amont (Émeraude)');
exp.setGuideTab('gardien');

// Le changement de mode ou de filtre ne referme pas le guide ouvert
exp.setMode('assises');
const guideStaysOpenOnMode = exp.getState().readingGuideOpen && getEl('explorer-v6-2-toolbar').innerHTML.includes('id="exp-reading-guide-panel"');
exp.setFilter('family', 'GARDIEN');
const guideStaysOpenOnFilter = exp.getState().readingGuideOpen && getEl('explorer-v6-2-toolbar').innerHTML.includes('id="exp-reading-guide-panel"');
exp.resetFilters();
exp.setMode('lisieres');

// Échap avec Rayons X actif ferme d'abord Rayons X sans fermer le guide
exp.toggleXRay('G1');
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'Escape' });
}
const guideOpenAfterXRayEscape = exp.getState().readingGuideOpen && exp.getState().xrayFocusId === null;

// Échap sans Rayons X actif ferme le guide
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'Escape' });
}
const guideClosedAfterEscape = !exp.getState().readingGuideOpen && !getEl('explorer-v6-2-toolbar').innerHTML.includes('id="exp-reading-guide-panel"');

// Réouverture puis fermeture explicite via toggleReadingGuide()
exp.toggleReadingGuide();
const guideReopened = exp.getState().readingGuideOpen;
exp.toggleReadingGuide();
const guideClosedAfterToggle = !exp.getState().readingGuideOpen
  && !getEl('explorer-v6-2-toolbar').innerHTML.includes('id="exp-reading-guide-panel"')
  && getEl('explorer-v6-2-toolbar').innerHTML.includes('aria-expanded="false"');

// Infobulles décodées sur les 30 badges de vecteurs
const vecMatches = Array.from(m1Grid.matchAll(/<span class="exp-vector-chip" data-vector-pair="([^"]+)" title="([^"]+)">/g));
const vectorTooltipsCount = vecMatches.length;
const vectorTooltipsAllDecoded = vecMatches.length === 30 && vecMatches.every(m => {
  const pair = m[1];
  const tip = m[2];
  return (pair.includes('->') || pair.includes('-&gt;')) && tip.includes('(') && tip.includes('→') && !badTokenRe.test(tip);
});
const g1VecTipMatch = m1Grid.match(/data-tile-id="G1"[\s\S]*?<span class="exp-vector-chip" data-vector-pair="([^"]+)" title="([^"]+)">/);
const g1VecTip = g1VecTipMatch ? g1VecTipMatch[2] : '';

console.log(JSON.stringify({
  ok: true,
  total_assises: all197.length,
  unique_keys: uniqueKeys.size,
  counts_by_n: countsByN,
  total_alerts_197: totalAlerts197,
  dihedral_keys: [rotCanon1.key, rotCanon2.key, mirCanon3.key],
  dihedral_tiles_match: JSON.stringify(rotTiles1) === JSON.stringify(mirTiles3),
  benchmarks: benchmarkResults,
  icon_order_v62: iconOrderV62,
  norm_checks: normChecks,
  mode1: {
    badge: m1Badge,
    borders: m1BordersCount,
    tiles: m1TilesCount,
    fluid_badges: m1FluidCount,
    enrac_cartouches: m1EnracCount,
    ramp_icons: rampIconsRendered,
    all_15_ramps_valid: all15RampsValid,
    face2_enrac_count: face2EnracCount,
    capot_hidden_initially: capotHiddenInitially,
    capot_expanded_all: capotExpandedAll,
    has_bad: m1HasBad,
  },
  mode2: {
    hei_svg: m2HeiHasSvg,
    hei_gardiens_inactive: m2HeiModGardiensInactive,
    hei_has_bad: m2HeiHasBad,
    wheel_filtered_tiles_H_on_HEI: m2WheelFilteredTiles,
    eri_has_R8: m2EriHasR8,
    n6_tiles: m2N6Tiles,
  },
  mode3: {
    peuple_counts: peupleCounts,
    has_bad: m3HasBad,
  },
  xray: {
    g7_up_acc: xrayG7.upstreamAccessories.length,
    g7_up_tiles: xrayG7.upstreamTiles.length,
    g7_down_tiles: xrayG7.downstreamTiles.length,
    has_focus: xrayHasFocus,
    has_up_down_dim: xrayHasUpAndDown,
    has_bad: xrayHasBad,
    after_escape: xrayAfterEscape,
    hei_no_guardian_leak: xrayHeiNoGuardianLeak,
  },
  filters: {
    twist_count: twistFilteredCount,
    loi_ids: loiFilteredIds,
    insect_icon_ids: insectIconIds,
    souche_chip_ids: soucheChipIds,
    reset_badge: resetBadge,
  },
  reading_guide: {
    initial_state: guideInitialState,
    initial_closed_in_dom: guideInitialClosedInDom,
    open_state: guideOpenState,
    open_has_bad: guideOpenHasBad,
    has_dialog_modal: guideHasDialogModal,
    zones: guideZones,
    vectors: guideVectors,
    bubbles_gardien: guideBubblesGardien,
    pins_gardien: guidePinsGardien,
    step1_spot: guideStep1Spot,
    step1_active_dom: guideStep1ActiveDom,
    capot_preview_shown: guideCapotPreviewShown,
    tab2_has_bad: guideTab2HasBad,
    tab2_bubbles: guideTab2Bubbles,
    tab2_has_specimens: guideTab2HasSpecimens,
    has_close_btn: guideHasCloseBtn,
    has_expanded_true: guideHasExpandedTrue,
    stays_open_on_mode: guideStaysOpenOnMode,
    stays_open_on_filter: guideStaysOpenOnFilter,
    open_after_xray_escape: guideOpenAfterXRayEscape,
    closed_after_escape: guideClosedAfterEscape,
    reopened: guideReopened,
    closed_after_toggle: guideClosedAfterToggle,
    open_html: guideOpenToolbar,
  },
  vector_tooltips: {
    count: vectorTooltipsCount,
    all_decoded: vectorTooltipsAllDecoded,
    g1_tip: g1VecTip,
  },
}));
"""


def _run_node_explorer_harness() -> dict[str, Any]:
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_EXPLORER_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(STUDIO_LIVRET),
            str(EXPLORER_JS),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Échec du harnais Node vm Explorateur v6.2 :\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    return dict(json.loads(lines[-1]))


def test_explorer_files_utf8_lf_and_index_wiring() -> None:
    """Vérifie encodage UTF-8 sans BOM, fins LF et branchement minimal dans docs/index.html."""
    for path in (EXPLORER_CSS, EXPLORER_JS, STUDIO_INDEX):
        assert path.is_file(), f"Fichier attendu manquant : {path}"
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {path.name}"
        assert b"\r\n" not in raw, f"Fin de ligne CRLF interdite dans {path.name}"
        raw.decode("utf-8")

    html = STUDIO_INDEX.read_text(encoding="utf-8")
    assert 'href="explorer_v6_2.css"' in html
    assert 'src="explorer_v6_2.js"' in html
    assert 'id="explorer-v6-2-toolbar"' in html
    assert "AmazoniaExplorerV62" in html


def test_explorer_197_assises_benchmarks_icons_modes_and_xray() -> None:
    """Valide l'énumération des 197 assises, les 4 tables témoins, les 6 icônes v6.2, les 3 Modes et Rayons X."""
    payload = _run_node_explorer_harness()
    assert payload["ok"] is True

    # 1. Énumération exacte des 197 assises uniques + invariance diédrale
    assert payload["total_assises"] == 197
    assert payload["unique_keys"] == 197
    assert payload["counts_by_n"] == {"3": 20, "4": 45, "5": 72, "6": 60}
    assert payload["total_alerts_197"] == 0
    assert payload["dihedral_keys"] == ["N4-HEMR", "N4-HEMR", "N4-HEMR"]
    assert payload["dihedral_tiles_match"] is True

    # 2. Tables témoins clés : N3-HEI, N3-ERI, N3-MRO, N6-HEMROI
    bm = payload["benchmarks"]

    hei = bm["N3-HEI"]
    assert hei["canonKey"] == "N3-HEI"
    assert hei["tileIds"] == ["M4", "M5", "R1", "R10", "R2", "R6"]
    assert hei["guardiansCount"] == 0
    assert hei["modules"] == {"gardiens": False, "reves": True, "essaim": True}
    assert hei["alertsCount"] == 0

    eri = bm["N3-ERI"]
    assert eri["canonKey"] == "N3-ERI"
    assert "R8" in eri["leviersReve"]
    assert eri["levierAlert"] is False
    assert eri["modules"] == {"gardiens": True, "reves": True, "essaim": True}

    mro = bm["N3-MRO"]
    assert mro["canonKey"] == "N3-MRO"
    assert mro["tileIds"] == ["G1", "G2", "G3", "G4", "G5", "G6"]
    assert mro["guardiansCount"] == 6
    assert mro["modules"] == {"gardiens": True, "reves": False, "essaim": False}

    n6 = bm["N6-HEMROI"]
    assert n6["canonKey"] == "N6-HEMROI"
    assert len(n6["tileIds"]) == 12
    assert n6["modules"] == {"gardiens": True, "reves": True, "essaim": True}

    # 3. Garde-fou 6 icônes Gardiens v6.2 & normalisation pré-v6.2
    expected_icons = [
        "ICONE_PARADE",
        "ICONE_PIEGEAGE",
        "ICONE_SABOTAGE",
        "ICONE_REVE",
        "ICONE_INSECTE",
        "ICONE_RESONANCE",
    ]
    assert payload["icon_order_v62"] == expected_icons
    assert n6["iconOrder"] == expected_icons

    nc = payload["norm_checks"]
    assert nc["n1"] == "ICONE_PARADE"
    assert nc["n2"] == "ICONE_PIEGEAGE"
    assert nc["n3"] == "ICONE_SABOTAGE"
    assert nc["n4"] == "ICONE_RESONANCE"
    assert nc["n5"] == "ICONE_REVE"
    assert nc["n6"] == "ICONE_INSECTE"
    assert nc["R1"] == ["ICONE_REVE"]
    assert nc["G12"] == ["ICONE_REVE"]
    assert nc["G13"] == ["ICONE_INSECTE"]
    assert nc["M4"] == ["ICONE_INSECTE", "ICONE_PARADE"]
    assert nc["M5"] == ["ICONE_INSECTE"]

    # 4. Mode 1 (15 Lisières face-à-face) + rampe 6 icônes + Capot Concepteur
    m1 = payload["mode1"]
    assert m1["has_bad"] is False
    assert m1["badge"] == "30 / 30 tuiles affichées"
    assert m1["borders"] == 15
    assert m1["tiles"] == 30
    assert m1["fluid_badges"] == 3
    assert m1["enrac_cartouches"] == 3
    assert m1["ramp_icons"] == expected_icons
    assert m1["all_15_ramps_valid"] is True
    assert m1["face2_enrac_count"] == 15
    assert m1["capot_hidden_initially"] is True
    assert m1["capot_expanded_all"] is True

    # 5. Mode 2 (Table & Roue des 197 Assises)
    m2 = payload["mode2"]
    assert m2["hei_has_bad"] is False
    assert m2["hei_svg"] is True
    assert m2["hei_gardiens_inactive"] is True
    assert m2["wheel_filtered_tiles_H_on_HEI"] == 4
    assert m2["eri_has_R8"] is True
    assert m2["n6_tiles"] == 12

    # 6. Mode 3 (Grammaires par Peuple 3+3) : 5 sortantes + 5 entrantes par Peuple
    m3 = payload["mode3"]
    assert m3["has_bad"] is False
    for p_code in ("H", "E", "M", "R", "O", "I"):
        assert m3["peuple_counts"][p_code] == {"out": 5, "in": 5}

    # 7. Mode Rayons X des Synergies & touche Échap
    xr = payload["xray"]
    assert xr["has_bad"] is False
    assert xr["g7_up_acc"] >= 1
    assert xr["g7_up_tiles"] >= 1
    assert xr["g7_down_tiles"] >= 1
    assert xr["has_focus"] is True
    assert xr["has_up_down_dim"] is True
    assert xr["after_escape"] is None
    assert xr["hei_no_guardian_leak"] is True

    # 8. Filtres multi-critères & puces d'états cliquables
    flt = payload["filters"]
    assert flt["twist_count"] == 6
    assert flt["loi_ids"] == ["M2", "M3"]
    assert "G13" in flt["insect_icon_ids"]
    assert "M5" in flt["insect_icon_ids"]
    assert "G1" not in flt["insect_icon_ids"]
    assert {"G3", "G7", "M5", "R8"}.issubset(set(flt["souche_chip_ids"]))
    assert flt["reset_badge"] == "30 / 30 tuiles affichées"


def test_explorer_reading_guide_and_vector_tooltips() -> None:
    """Vérifie le didacticiel visuel annoté « ? Guide de lecture » et les infobulles décodées V1..V5."""
    payload = _run_node_explorer_harness()
    assert payload["ok"] is True

    rg = payload["reading_guide"]
    assert rg["initial_state"] is False
    assert rg["initial_closed_in_dom"] is True
    assert rg["open_state"] is True
    assert rg["open_has_bad"] is False
    assert rg["has_dialog_modal"] is True
    assert rg["has_close_btn"] is True
    assert rg["has_expanded_true"] is True
    assert rg["zones"] == ["1", "2", "3", "4", "5", "6"]
    assert rg["vectors"] == ["V1", "V2", "V3", "V4", "V5"]
    assert rg["bubbles_gardien"] == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert rg["pins_gardien"] == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    assert rg["step1_spot"] == "1"
    assert rg["step1_active_dom"] is True
    assert rg["capot_preview_shown"] is True
    assert rg["tab2_has_bad"] is False
    assert rg["tab2_bubbles"] == ["1", "2", "3", "4", "5"]
    assert rg["tab2_has_specimens"] is True

    open_html = rg["open_html"]
    for snippet in (
        "Bandeau de lisière",
        "Géométrie 2K3",
        "✓ 0 boucle",
        "En-tête d’identité",
        "Focus Synergies",
        "Forêt, Souches, recul &amp; position des machines",
        "Rangs de la Réglette &amp; jetons Puissance (Rouge / Bleu Surchauffe)",
        "Pièges, Croc, Sabotages, Écailles &amp; Altération",
        "Défenseurs, essaim d’Insectes &amp; jeton Duel",
        "Rêves, Piste des Gardiens &amp; signaux muets (Plume, Perchoir)",
        "2 Souches si enraciné",
        "Chaîne de flux physique cliquable",
        "Capot Concepteur",
        "ACTIVE_VERIFIED",
    ):
        assert snippet in open_html, f"Contenu attendu absent du Didacticiel visuel : {snippet}"

    assert rg["stays_open_on_mode"] is True
    assert rg["stays_open_on_filter"] is True
    assert rg["open_after_xray_escape"] is True
    assert rg["closed_after_escape"] is True
    assert rg["reopened"] is True
    assert rg["closed_after_toggle"] is True

    vt = payload["vector_tooltips"]
    assert vt["count"] == 30
    assert vt["all_decoded"] is True
    assert vt["g1_tip"] == "V4 (Défenseurs, Insectes &amp; Duel) → V2 (Rangs &amp; Puissance Rouge/Bleu)"

