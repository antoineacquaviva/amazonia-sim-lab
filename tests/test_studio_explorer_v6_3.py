"""Tests headless Node vm & pont Python dédiés à l'Explorateur & Atelier Bi-Composant v6.4.0.

Vérifie sans dépendance npm :
1. Encodage UTF-8 sans BOM, fins LF, compilation `docs/data/canon_v6_4_data.js` et
   `docs/data/panels_v6_3_data.js` (y compris embarquement optionnel de `author_workspace_v6_3.json`
   & filtrage dans `audit_panels_directory`), et validation syntaxique stricte via `new vm.Script()`.
2. Bascule par défaut sur le Canon v6.4 (Affiné — Passe 2) :
   - Entrée par défaut sur `Canon v6.4 (Affiné)` (`mode = 'list'`, `listSource = 'canon_v6_4'`,
     `simSource = 'canon_v6_4'`, `radarTarget = 'canon_v6_4'`), tous tiroirs fermés, 30 Mini-Tuiles
     + 30 Grandes Cartes, pastille Santé consolidée `✅ Équilibre OK` (197 assises, 6 Twists 2K3,
     3 Lois passives max 2/assise, 13 catalyseurs Éveil, 4 Enracinements, 0 orpheline, 0 divergence) ;
   - Repli automatique du bandeau global Studio au clic sur l'onglet Catalogue (`switchTab('catalogue')`)
     et restauration de la préférence utilisateur sur les autres onglets ;
   - Guide des **31 pictogrammes officiels v6.4** (zéro `PIC_PLUME`, `PIC_PERCHOIR` présent),
     focus 1-clic Ressource/Icône (`PERCHOIR`, `BLEU`, `ICONE_PIEGEAGE`), édition live sur
     `canon_v6_4` + export `buildCandidateCanonV64()` validé en strict par
     `validate_tiles_canon_v6_4` et `audit_tiles_catalog_197` ;
   - Archives lecture seule (`Archive v6.3 (Passe 1)` et `Archive v6.2`) et Simulateur de Table
     `3..6` Peuples sur `canon_v6_4`.
3. Préservation complète du Banc de montage Duel `P1 | P2 | P3` (`setMode('arbitrate')`) :
   - 1 emplacement à la fois (`G1`), `<details>` replié par défaut, trio d'annotation,
     navigation clavier `ArrowRight`/`ArrowLeft`/`Escape`, Index 30 emplacements, Radar mixte 2K3,
     Hybrideur, Briefs Markdown Gemini (4 périmètres), persistance `amazonia_atelier_v6_4_workspace_v1`
     (`6.4.0-workspace`) et export strict `buildCandidateCanonV63('panel_1')`.
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts.audit_197 import audit_panels_directory, audit_tiles_catalog_197
from scripts.build_studio_artifacts import compile_panels_v6_3_js
from scripts.tiles_v6_3_schema import (
    PANELS_DIR,
    validate_tiles_canon_v6_3,
    validate_tiles_canon_v6_4,
)

ROOT = Path(__file__).resolve().parent.parent
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
CANON_V6_4_JS = ROOT / "docs" / "data" / "canon_v6_4_data.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"
ILLUSTRATIONS_JS = ROOT / "docs" / "tile_illustrations_v6_2.js"
EXPLORER_V6_2_JS = ROOT / "docs" / "explorer_v6_2.js"
PANELS_V6_3_JS = ROOT / "docs" / "data" / "panels_v6_3_data.js"
EXPLORER_V6_3_JS = ROOT / "docs" / "explorer_v6_3.js"
EXPLORER_V6_3_CSS = ROOT / "docs" / "explorer_v6_3.css"


_NODE_V63_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, canon64Path, livretPath, illPath, exp62Path, panels63Path, exp63Path] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const canon64Js = fs.readFileSync(canon64Path, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const illJs = fs.readFileSync(illPath, 'utf8');
const exp62Js = fs.readFileSync(exp62Path, 'utf8');
const panels63Js = fs.readFileSync(panels63Path, 'utf8');
const exp63Js = fs.readFileSync(exp63Path, 'utf8');

// Validation syntaxique stricte via new vm.Script()
new vm.Script(canon64Js, { filename: canon64Path });
new vm.Script(panels63Js, { filename: panels63Path });
new vm.Script(exp63Js, { filename: exp63Path });

const inlineScripts = [];
for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
  inlineScripts.push(m[1]);
}

function makeElement(id) {
  const classes = new Set();
  return {
    id,
    _innerHTML: '',
    _textContent: '',
    value: id === 'changelog-filter-select' ? 'ALL'
         : id === 'diff-version-select' ? 'v6.2'
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
    select: () => {},
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

const storageMap = {};
const docListeners = {};
const clipboardWrites = [];
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
  setTimeout: () => 1,
  clearTimeout: () => {},
  localStorage: {
    getItem: (k) => (Object.prototype.hasOwnProperty.call(storageMap, k) ? storageMap[k] : null),
    setItem: (k, v) => { storageMap[k] = String(v); },
  },
  navigator: {
    clipboard: {
      writeText: (txt) => {
        clipboardWrites.push(txt);
        return Promise.resolve();
      },
    },
  },
  location: { protocol: 'file:', href: 'file:///docs/index.html' },
  fetch: async () => ({ ok: false, json: async () => ({}) }),
  tailwind: {},
  document: {
    getElementById: (id) => getEl(id),
    addEventListener: (ev, fn) => { docListeners[ev] = fn; },
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: (tag) => makeElement(tag),
    body: { appendChild: () => {}, removeChild: () => {} },
    execCommand: () => true,
  },
  window: {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

// Ordre exact du navigateur dans docs/index.html
vm.runInContext(dataJs, sandbox, { filename: dataPath });
vm.runInContext(canon64Js, sandbox, { filename: canon64Path });
vm.runInContext(livretJs, sandbox, { filename: livretPath });
vm.runInContext(illJs, sandbox, { filename: illPath });
vm.runInContext(exp62Js, sandbox, { filename: exp62Path });
vm.runInContext(panels63Js, sandbox, { filename: panels63Path });
vm.runInContext(exp63Js, sandbox, { filename: exp63Path });
for (let i = 0; i < inlineScripts.length; i++) {
  vm.runInContext(inlineScripts[i], sandbox, { filename: `docs/index.html#script${i}` });
}

const exp = sandbox.AmazoniaExplorerV63;
if (!exp) throw new Error('AmazoniaExplorerV63 non exposé sur window');
if (sandbox.AmazoniaExplorerV64 !== exp) throw new Error('AmazoniaExplorerV64 doit aliaser AmazoniaExplorerV63');

const badTokenRe = /\b(?:NaN|undefined)\b/;
function stripTags(htmlStr) {
  return String(htmlStr || '')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ');
}

sandbox.refreshAllUI();

// 0. État initial v6.4.0 : ouverture par défaut sur Canon v6.4 (Affiné), 30 cartes, tiroirs fermés
const initTb = getEl('explorer-v6-3-toolbar').innerHTML;
const initGd = getEl('catalogue-grid').innerHTML;
const initState = exp.getState();
const initProse = stripTags(initTb + '\n' + initGd);
const v64Radar = exp.computeHealthRadar('canon_v6_4');
const initCheck = {
  version: exp.VERSION,
  mode: initState.mode,
  listSource: initState.listSource,
  simSource: initState.simSource,
  radarTarget: initState.radarTarget,
  activeDrawer: initState.activeDrawer,
  hasSingleHealthPill: initTb.includes('data-health-pill="true"'),
  healthStatusOk: initTb.includes('data-health-status="ok"') || v64Radar.overallStatus === 'ok',
  miniCount: (initGd.match(/data-component="mini-tuile"/g) || []).length,
  grandeCount: (initGd.match(/data-component="grande-carte"/g) || []).length,
  loiCards: (initGd.match(/data-nature="LOI_PASSIVE"/g) || []).length,
  twistCards: (initGd.match(/data-twist="true"/g) || []).length,
  hasBad: badTokenRe.test(initTb + '\n' + initGd),
  hasSnake: (initTb + initGd).includes('\u{1F40D}'),
  hasRawPic: /\bPIC_[A-Z0-9_]+\b/.test(initProse),
  hasRawIcon: /\bICONE_[A-Z_]+\b/.test(initProse),
  hasPlumbing: /\b(?:engine_sync_status|REFINED_V6_4|DESIGNED_V6_3|PASSE_2_AFFINE|PASSE_1_CREATIF|A_CODER|transition_python|mots_par_face)\b/.test(initProse),
};

const canonV64RadarReport = {
  elected: v64Radar.electedCount,
  overallStatus: v64Radar.overallStatus,
  twistsCount: v64Radar.twists.count,
  twists2K3: Boolean(v64Radar.twists.triangles2K3),
  loisCount: v64Radar.lois.count,
  loisMax: v64Radar.lois.maxPerAssise,
  eveilCount: v64Radar.eveil.count,
  sommeilBorders: v64Radar.sommeil.coveredEBorders.length,
  enracCount: v64Radar.enrac.count,
  a0Status: v64Radar.a0.status,
  orphans: v64Radar.synergies.orphans.length,
};

// Repli automatique du bandeau global Studio sur switchTab('catalogue') puis restauration sur 'livret'
sandbox.switchTab('catalogue');
const headerCollapsedOnCatalogue = getEl('header-collapsible-body').classList.contains('hidden');
const headerBtnOnCatalogue = getEl('btn-toggle-header').textContent;
sandbox.switchTab('livret');
const headerRestoredOnLivret = !getEl('header-collapsible-body').classList.contains('hidden');
sandbox.switchTab('catalogue');

// Guide des 31 pictogrammes v6.4 (zéro PIC_PLUME, PIC_PERCHOIR présent) + filtre picto
exp.openPictoGuide();
const guideHtmlV64 = getEl('catalogue-grid').innerHTML;
const guideV64Check = {
  cards_count: (guideHtmlV64.match(/class="x3-picto-guide-card"/g) || []).length,
  has_bad: badTokenRe.test(guideHtmlV64),
  has_plume: guideHtmlV64.includes('PIC_PLUME'),
  has_perchoir: guideHtmlV64.includes('PIC_PERCHOIR'),
};
exp.setPictoFilter('PIC_CROC');
const crocPictoSlots = exp.getFilteredSlotIds();
exp.resetFilters();

const canonV64Global = vm.runInContext('CANON_V6_4', sandbox);
const panelsV63 = vm.runInContext('PANELS_V6_3', sandbox);

// Focus Ressource / Icône 1 clic sur Canon v6.4 (PERCHOIR, BLEU, ICONE_PIEGEAGE)
exp.focusResource('PERCHOIR', 'canon_v6_4');
const perchoirIndex = exp.computeResourceIndex('PERCHOIR', canonV64Global.tuiles_ciblees);
exp.focusResource('BLEU', 'canon_v6_4');
const bleuIndex = exp.computeResourceIndex('BLEU', canonV64Global.tuiles_ciblees);
const bleuHtml = getEl('catalogue-grid').innerHTML;
const bleuHasPanel = bleuHtml.includes('data-resource-focus="BLEU"') && bleuHtml.includes('Producteurs') && bleuHtml.includes('Consommateurs');
exp.focusResource('ICONE_PIEGEAGE', 'canon_v6_4');
const piegIndex = exp.computeResourceIndex('ICONE_PIEGEAGE', canonV64Global.tuiles_ciblees);
exp.clearResourceFocus();

// Édition live sur Canon v6.4 + restauration + export strict buildCandidateCanonV64()
exp.openEditor('G1', 'canon_v6_4');
exp.updateEditorField('carte_joueur.titre_complet', 'Le Jaguar retouché v6.4');
exp.saveEditorToCanon();
const v64EditedHtml = getEl('catalogue-grid').innerHTML;
const v64EditShowsModified = v64EditedHtml.includes('Le Jaguar retouché v6.4') && v64EditedHtml.includes('Modifié');
exp.restoreOriginalSlot('G1', 'canon_v6_4');
const candidateCanonV64Strict = exp.buildCandidateCanonV64();

// Simulateur de Table 3..6 Peuples par défaut sur Canon v6.4
exp.setMode('simulator');
const simResults = {};
for (const preset of ['N3-HEI', 'N3-ERO', 'N3-MRO', 'N6-HEMROI']) {
  exp.setSimPreset(preset);
  const s = exp.analyzeTableSimulation(exp.getState().simPeuples, 'canon_v6_4');
  const sHtml = getEl('catalogue-grid').innerHTML;
  simResults[preset] = {
    canonKey: s.canonKey,
    tilesCount: s.tileEntries.length,
    modules: s.modules,
    accessoriesCount: s.accessories.length,
    chainsCount: s.completeChains.length,
    isolatedCount: s.isolatedAmplifiers.length,
    loisCount: s.metrics.loisCount,
    hasBad: badTokenRe.test(sHtml),
    hasWheelSvg: sHtml.includes('class="x3-wheel-svg"'),
    hasPerchoirVigie: sHtml.includes('Perchoir de Vigie'),
  };
}

// Archives lecture seule : Archive v6.3 (Passe 1) & Archive v6.2
exp.openListView('archive_v6_3');
const archiveV63Html = getEl('catalogue-grid').innerHTML;
const archiveV63Ok = !badTokenRe.test(archiveV63Html) && (archiveV63Html.match(/data-component="grande-carte"/g) || []).length === 30;
exp.openListView('archive_v6_2');
const archiveV62Html = getEl('catalogue-grid').innerHTML;
const archiveV62Ok = archiveV62Html.includes('Archive v6.2') && !badTokenRe.test(archiveV62Html) && (archiveV62Html.match(/data-component="grande-carte"/g) || []).length === 30;

// Bascule vers Banc de montage Duel P1 | P2 | P3 (préservé à 100 %)
exp.setMode('arbitrate');
exp.goToSlot('G1');
const duelTb = getEl('explorer-v6-3-toolbar').innerHTML;
const duelGd = getEl('catalogue-grid').innerHTML;
const duelCheck = {
  mode: exp.getState().mode,
  slot: exp.getState().currentSlotId,
  hasArbitrateSlotG1: duelGd.includes('data-arbitrate-slot="G1"'),
  duelCols: Array.from(duelGd.matchAll(/data-duel-col="([^"]+)"/g)).map(m => m[1]),
  detailsFoldClosed: duelGd.includes('<details class="x3-details-fold"') && !duelGd.includes('<details class="x3-details-fold" open'),
  hasTrioBar: duelGd.includes('data-trio-bar="G1"') && duelGd.includes('data-review-btn="true"'),
  hasBad: badTokenRe.test(duelTb + '\n' + duelGd),
};

// Navigation clavier en mode Duel : ArrowRight -> G2, ArrowLeft -> G1, Escape ferme tiroir
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'ArrowRight', target: { tagName: 'BODY' } });
}
const afterArrowRightSlot = exp.getState().currentSlotId;
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'ArrowLeft', target: { tagName: 'BODY' } });
}
const afterArrowLeftSlot = exp.getState().currentSlotId;

// Tiroir Santé consolidé (dépliable) + 197 assises
exp.toggleDrawer('health');
const healthDrawerHtml = getEl('explorer-v6-3-toolbar').innerHTML;
const healthDrawerCheck = {
  opened: healthDrawerHtml.includes('data-drawer="health"'),
  radarPillsCount: (healthDrawerHtml.match(/data-radar-pill="/g) || []).length,
  hasBad: badTokenRe.test(healthDrawerHtml),
};
if (typeof docListeners.keydown === 'function') {
  docListeners.keydown({ key: 'Escape', target: { tagName: 'BODY' } });
}
const drawerClosedByEscape = exp.getState().activeDrawer === null;

// Modèle 197 assises & Rendu Bi-Composant + Zéro plomberie sur les 3 panels en archive
const all197 = exp.enumerateAll197Assises();
const countsByN = { 3: 0, 4: 0, 5: 0, 6: 0 };
for (const a of all197) countsByN[a.n]++;

const panelRadars = {};
const panelRenders = {};
for (const pid of ['panel_1', 'panel_2', 'panel_3']) {
  const r = exp.computeHealthRadar(pid);
  exp.openListView(pid);
  const tb = getEl('explorer-v6-3-toolbar').innerHTML;
  const gd = getEl('catalogue-grid').innerHTML;
  const visibleProse = stripTags(tb + '\n' + gd);
  panelRadars[pid] = {
    elected: r.electedCount,
    overallStatus: r.overallStatus,
    twistsCount: r.twists.count,
    twists2K3: Boolean(r.twists.triangles2K3),
    twistsStatus: r.twists.status,
    loisCount: r.lois.count,
    loisMax: r.lois.maxPerAssise,
    loisStatus: r.lois.status,
    eveilCount: r.eveil.count,
    eveilStatus: r.eveil.status,
    sommeilBorders: r.sommeil.coveredEBorders.length,
    sommeilStatus: r.sommeil.status,
    enracCount: r.enrac.count,
    enracStatus: r.enrac.status,
    a0Status: r.a0.status,
    orphans: r.synergies.orphans.length,
  };
  panelRenders[pid] = {
    miniCount: (gd.match(/data-component="mini-tuile"/g) || []).length,
    grandeCount: (gd.match(/data-component="grande-carte"/g) || []).length,
    loiCards: (gd.match(/data-nature="LOI_PASSIVE"/g) || []).length,
    twistCards: (gd.match(/data-twist="true"/g) || []).length,
    hasBad: badTokenRe.test(tb + '\n' + gd),
    hasSnake: (tb + gd).includes('\u{1F40D}'),
    proseSampleHasRawPic: /\bPIC_[A-Z0-9_]+\b/.test(visibleProse),
    proseSampleHasRawIcon: /\bICONE_[A-Z_]+\b/.test(visibleProse),
    proseSampleHasPlumbing: /\b(?:engine_sync_status|DESIGNED_V6_3|PASSE_1_CREATIF|A_CODER|transition_python|mots_par_face)\b/.test(visibleProse),
  };
}

// Trio d'annotation, Index 30 emplacements, Radar mixte, Hybridation & Exports
exp.setMode('arbitrate');
exp.goToSlot('G1');
exp.keepSlot('G1', 'panel_1');
const nextPendingAfterG1 = exp.goToNextPending();
exp.goToSlot('G1');

exp.toggleDrawer('index30');
const indexDrawerHtml = getEl('explorer-v6-3-toolbar').innerHTML;
const indexDrawerSlotsCount = (indexDrawerHtml.match(/data-index-slot="/g) || []).length;
exp.fillUnelectedFrom('panel_1');
const canonRadarFullP1 = exp.computeHealthRadar('canon');

exp.keepSlot('G2', 'panel_2');
const canonRadarMixedTwist = exp.computeHealthRadar('canon');
exp.keepSlot('G2', 'panel_1');

exp.toggleSlotReview('G1');
exp.setSlotCommentLive('G1', 'Combiner Face 1 de P1 avec Face 2 de P2');
exp.toggleSlotReview('R4');
exp.setSlotCommentLive('R4', 'Arbitrer le Twist H>R entre P1 et P3');

exp.openEditor('G1', 'panel_1');
exp.importEditorFromPanel('panel_2', 'face_2');
exp.updateEditorField('carte_joueur.titre_complet', 'Le Jaguar hybride des rives');
exp.saveEditorToCanon();

exp.openListView('canon');
const canonListHtml = getEl('catalogue-grid').innerHTML;
const canonShowsModifiedBadge = canonListHtml.includes('Modifié') && canonListHtml.includes('Le Jaguar hybride des rives');

// Exports Gemini Markdown (4 périmètres)
const geminiBriefs = {};
for (const sc of ['to_arbitrate', 'active_context', 'notes_and_edits', 'canon_summary']) {
  const b = exp.buildGeminiMarkdownBrief(sc);
  geminiBriefs[sc] = {
    words: b.words,
    tileCount: b.tileCount,
    comfort: b.comfort,
    hasRawPic: /\bPIC_[A-Z0-9_]+\b/.test(b.markdown),
    hasPlumbing: /\b(?:engine_sync_status|A_CODER|transition_python)\b/.test(b.markdown),
    containsG1Note: b.markdown.includes('Combiner Face 1 de P1'),
  };
}

// Export & ré-import Workspace Antigravity v6.4 + Export candidat strict v6.3
const exportedWorkspace = exp.buildAuthorWorkspaceExport();
const storedRaw = storageMap['amazonia_atelier_v6_4_workspace_v1'] || null;
exp.restoreOriginalSlot('G1');
const candidateCanonStrict = exp.buildCandidateCanonV63('panel_1');

exp.importWorkspaceObject(exportedWorkspace);
const reimportedG1Modified = exp.getWorkspace().slots.G1.is_modified;
const reimportedG1Title = exp.getWorkspace().slots.G1.custom_tile.carte_joueur.titre_complet;

console.log(JSON.stringify({
  ok: true,
  init_check: initCheck,
  canon_v64_radar: canonV64RadarReport,
  v64_edit_shows_modified: v64EditShowsModified,
  duel_check: duelCheck,
  header_auto_collapse: {
    collapsed_on_catalogue: headerCollapsedOnCatalogue,
    btn_on_catalogue: headerBtnOnCatalogue,
    restored_on_livret: headerRestoredOnLivret,
  },
  keyboard: {
    after_arrow_right: afterArrowRightSlot,
    after_arrow_left: afterArrowLeftSlot,
    drawer_closed_by_escape: drawerClosedByEscape,
  },
  health_drawer: healthDrawerCheck,
  index_drawer_slots_count: indexDrawerSlotsCount,
  next_pending_after_g1: nextPendingAfterG1,
  total_assises: all197.length,
  counts_by_n: countsByN,
  panel_radars: panelRadars,
  panel_renders: panelRenders,
  picto_guide_v64: {
    ...guideV64Check,
    croc_slots_count: crocPictoSlots.length,
  },
  resource_focus: {
    perchoir_consumers_or_producers: perchoirIndex.producers.length + perchoirIndex.consumersFloor.length + perchoirIndex.consumersSynergy.length,
    bleu_has_panel: bleuHasPanel,
    bleu_producers: bleuIndex.producers.length,
    piegeage_producers: piegIndex.producers.length,
    piegeage_guardians: piegIndex.consumersIcon.length,
  },
  simulator: simResults,
  archive_v63_ok: archiveV63Ok,
  archive_v62_ok: archiveV62Ok,
  canon_radar_full_p1: {
    elected: canonRadarFullP1.electedCount,
    overallStatus: canonRadarFullP1.overallStatus,
    twists2K3: Boolean(canonRadarFullP1.twists.triangles2K3),
    loisMax: canonRadarFullP1.lois.maxPerAssise,
    eveil: canonRadarFullP1.eveil.status,
    sommeil: canonRadarFullP1.sommeil.status,
    enrac: canonRadarFullP1.enrac.status,
    a0: canonRadarFullP1.a0.status,
  },
  canon_radar_mixed_twist_2k3: Boolean(canonRadarMixedTwist.twists.triangles2K3),
  canon_shows_modified_badge: canonShowsModifiedBadge,
  gemini_briefs: geminiBriefs,
  workspace_saved_in_localstorage: Boolean(storedRaw),
  workspace_schema: exportedWorkspace.schema_version,
  workspace_reimported_g1_modified: reimportedG1Modified,
  workspace_reimported_g1_title: reimportedG1Title,
  candidate_canon_v64_strict: candidateCanonV64Strict,
  candidate_canon_strict: candidateCanonStrict,
}));
"""


def _run_v63_harness() -> dict[str, Any]:
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_V63_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(CANON_V6_4_JS),
            str(STUDIO_LIVRET),
            str(ILLUSTRATIONS_JS),
            str(EXPLORER_V6_2_JS),
            str(PANELS_V6_3_JS),
            str(EXPLORER_V6_3_JS),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Échec du harnais Node vm Explorateur v6.4.0 :\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    return dict(json.loads(lines[-1]))


def test_v63_studio_files_utf8_lf_and_index_wiring() -> None:
    """Vérifie UTF-8 sans BOM, fins LF et branchement propre (v6.4 + archives) dans docs/index.html."""
    for path in (CANON_V6_4_JS, PANELS_V6_3_JS, EXPLORER_V6_3_JS, EXPLORER_V6_3_CSS, STUDIO_INDEX):
        assert path.is_file(), f"Fichier attendu manquant : {path}"
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {path.name}"
        assert b"\r\n" not in raw, f"CRLF interdit dans {path.name}"
        raw.decode("utf-8")

    html = STUDIO_INDEX.read_text(encoding="utf-8")
    assert 'href="explorer_v6_3.css"' in html
    assert 'id="explorer-v6-3-toolbar"' in html
    canon64_tag = '<script src="data/canon_v6_4_data.js"></script>'
    livret_tag = '<script src="data/livret_v6_0.js"></script>'
    panels_tag = '<script src="data/panels_v6_3_data.js"></script>'
    exp_tag = '<script src="explorer_v6_3.js"></script>'
    assert canon64_tag in html
    assert livret_tag in html
    assert panels_tag in html
    assert exp_tag in html
    assert html.index(canon64_tag) < html.index(livret_tag)
    assert html.index(panels_tag) < html.index(exp_tag)
    assert "AmazoniaExplorerV63" in html


def test_compile_panels_embeds_initial_workspace_and_audit_ignores_it(tmp_path: Path) -> None:
    """Vérifie l'embarquement optionnel de author_workspace_v6_3.json et son exclusion de audit_panels_directory."""
    for pid in ("panel_1", "panel_2", "panel_3"):
        src = PANELS_DIR / f"{pid}.json"
        (tmp_path / f"{pid}.json").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

    ws_payload = {
        "schema_version": "6.3.1-workspace",
        "updated_at": "2026-11-26T12:00:00Z",
        "slots": {"G1": {"selected_source": "panel_2", "comment": "Test seed"}},
    }
    ws_path = tmp_path / "author_workspace_v6_3.json"
    ws_path.write_text(json.dumps(ws_payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    js_src, meta = compile_panels_v6_3_js(panels_dir=tmp_path)
    assert meta["panels_count"] == 3
    assert meta["pictograms_count"] == 32
    assert meta["workspace_file"] == ws_path
    assert '"Test seed"' in js_src
    assert re.search(r"const AUTHOR_WORKSPACE_INITIAL_V6_3\s*=\s*\{", js_src)

    # audit_panels_directory doit ignorer author_workspace_v6_3.json et valider les 3 panels
    batch = audit_panels_directory(tmp_path, allow_draft=False)
    assert batch["panels_count"] == 3
    assert batch["all_ok"] is True


def test_explorer_v63_streamlined_atelier_radar_simulator_and_strict_export() -> None:
    """Valide l'Explorateur v6.4.0 (Canon v6.4 par défaut, 31 pictos, Simulateur, Archives, Duel & exports stricts)."""
    payload = _run_v63_harness()
    assert payload["ok"] is True

    # 0. Entrée par défaut = Canon v6.4 (Affiné), 30 cartes, tiroirs fermés, zéro plomberie
    ic = payload["init_check"]
    assert ic["version"] == "6.4.0"
    assert ic["mode"] == "list"
    assert ic["listSource"] == "canon_v6_4"
    assert ic["simSource"] == "canon_v6_4"
    assert ic["radarTarget"] == "canon_v6_4"
    assert ic["activeDrawer"] is None
    assert ic["hasSingleHealthPill"] is True
    assert ic["healthStatusOk"] is True
    assert ic["miniCount"] == 30
    assert ic["grandeCount"] == 30
    assert ic["loiCards"] == 3
    assert ic["twistCards"] == 6
    assert ic["hasBad"] is False
    assert ic["hasSnake"] is False
    assert ic["hasRawPic"] is False
    assert ic["hasRawIcon"] is False
    assert ic["hasPlumbing"] is False

    r64 = payload["canon_v64_radar"]
    assert r64["elected"] == 30
    assert r64["overallStatus"] == "ok"
    assert r64["twistsCount"] == 6
    assert r64["twists2K3"] is True
    assert r64["loisCount"] == 3
    assert r64["loisMax"] <= 2
    assert r64["eveilCount"] == 13
    assert r64["sommeilBorders"] == 4
    assert r64["enracCount"] == 4
    assert r64["a0Status"] == "ok"
    assert r64["orphans"] == 0
    assert payload["v64_edit_shows_modified"] is True

    # Repli bandeau auto
    hac = payload["header_auto_collapse"]
    assert hac["collapsed_on_catalogue"] is True
    assert "Afficher le bandeau" in hac["btn_on_catalogue"]
    assert hac["restored_on_livret"] is True

    # Guide des 31 pictogrammes v6.4 (sans PIC_PLUME)
    pg = payload["picto_guide_v64"]
    assert pg["cards_count"] == 31
    assert pg["has_bad"] is False
    assert pg["has_plume"] is False
    assert pg["has_perchoir"] is True
    assert pg["croc_slots_count"] >= 1

    # Focus Ressource / Icône sur Canon v6.4
    rf = payload["resource_focus"]
    assert rf["perchoir_consumers_or_producers"] >= 1
    assert rf["bleu_has_panel"] is True
    assert rf["bleu_producers"] >= 1
    assert rf["piegeage_producers"] >= 1
    assert rf["piegeage_guardians"] >= 1

    # Simulateur de Table 3..6 Peuples sur Canon v6.4
    sim = payload["simulator"]
    assert sim["N3-HEI"]["tilesCount"] == 6
    assert sim["N3-HEI"]["modules"] == {"gardiens": False, "reves": True, "essaim": True}
    assert sim["N3-HEI"]["accessoriesCount"] == 3
    assert sim["N3-HEI"]["hasWheelSvg"] is True
    assert sim["N3-HEI"]["hasBad"] is False

    assert sim["N3-ERO"]["tilesCount"] == 6
    assert sim["N3-ERO"]["hasPerchoirVigie"] is True
    assert sim["N3-ERO"]["hasBad"] is False

    assert sim["N3-MRO"]["tilesCount"] == 6
    assert sim["N3-MRO"]["modules"] == {"gardiens": True, "reves": False, "essaim": False}

    assert sim["N6-HEMROI"]["tilesCount"] == 12
    assert sim["N6-HEMROI"]["accessoriesCount"] == 6
    assert sim["N6-HEMROI"]["chainsCount"] >= 1
    assert sim["N6-HEMROI"]["hasPerchoirVigie"] is True
    assert sim["N6-HEMROI"]["hasBad"] is False

    # Archives lecture seule (v6.3 Passe 1 + v6.2)
    assert payload["archive_v63_ok"] is True
    assert payload["archive_v62_ok"] is True

    # Mode Duel P1 | P2 | P3 préservé + clavier + tiroirs
    dc = payload["duel_check"]
    assert dc["mode"] == "arbitrate"
    assert dc["slot"] == "G1"
    assert dc["hasArbitrateSlotG1"] is True
    assert dc["duelCols"] == ["panel_1", "panel_2", "panel_3"]
    assert dc["detailsFoldClosed"] is True
    assert dc["hasTrioBar"] is True
    assert dc["hasBad"] is False

    kb = payload["keyboard"]
    assert kb["after_arrow_right"] == "G2"
    assert kb["after_arrow_left"] == "G1"
    assert kb["drawer_closed_by_escape"] is True

    hd = payload["health_drawer"]
    assert hd["opened"] is True
    assert hd["radarPillsCount"] == 7
    assert hd["hasBad"] is False
    assert payload["index_drawer_slots_count"] == 30
    assert payload["next_pending_after_g1"] == "G2"

    # Modèle exact des 197 assises
    assert payload["total_assises"] == 197
    assert payload["counts_by_n"] == {"3": 20, "4": 45, "5": 72, "6": 60}

    # Rendu Bi-Composant + Zéro plomberie + Radar 100 % OK sur les 3 panels archivés
    for pid in ("panel_1", "panel_2", "panel_3"):
        rad = payload["panel_radars"][pid]
        assert rad["elected"] == 30
        assert rad["overallStatus"] == "ok"
        assert rad["twistsCount"] == 6
        assert rad["twists2K3"] is True, f"{pid} doit valider 2 triangles orientés 2K3"
        assert rad["twistsStatus"] == "ok"
        assert rad["loisCount"] <= 5
        assert rad["loisMax"] <= 2
        assert rad["loisStatus"] == "ok"
        assert rad["eveilStatus"] == "ok"
        assert rad["sommeilStatus"] == "ok"
        assert rad["enracStatus"] == "ok"
        assert rad["a0Status"] == "ok"
        assert rad["orphans"] == 0

        rnd = payload["panel_renders"][pid]
        assert rnd["miniCount"] == 30
        assert rnd["grandeCount"] == 30
        assert rnd["loiCards"] == rad["loisCount"]
        assert rnd["twistCards"] == 6
        assert rnd["hasBad"] is False
        assert rnd["hasSnake"] is False
        assert rnd["proseSampleHasRawPic"] is False, f"Code brut PIC_* visible sur {pid}"
        assert rnd["proseSampleHasRawIcon"] is False, f"Code brut ICONE_* visible sur {pid}"
        assert rnd["proseSampleHasPlumbing"] is False, f"Plomberie technique visible sur {pid}"

    # Radar Mon Canon (y compris détection 2K3 cassée en mixant)
    assert payload["canon_radar_full_p1"]["elected"] == 30
    assert payload["canon_radar_full_p1"]["overallStatus"] == "ok"
    assert payload["canon_radar_full_p1"]["twists2K3"] is True
    assert payload["canon_radar_mixed_twist_2k3"] is False
    assert payload["canon_shows_modified_badge"] is True

    # Briefs Gemini (4 périmètres, zéro code brut) & Persistance Workspace v6.4
    gb = payload["gemini_briefs"]
    for sc in ("to_arbitrate", "active_context", "notes_and_edits", "canon_summary"):
        assert gb[sc]["words"] > 20
        assert gb[sc]["hasRawPic"] is False
        assert gb[sc]["hasPlumbing"] is False
    assert gb["to_arbitrate"]["tileCount"] == 2
    assert gb["to_arbitrate"]["containsG1Note"] is True
    assert gb["notes_and_edits"]["containsG1Note"] is True

    assert payload["workspace_saved_in_localstorage"] is True
    assert payload["workspace_schema"] == "6.4.0-workspace"
    assert payload["workspace_reimported_g1_modified"] is True
    assert payload["workspace_reimported_g1_title"] == "Le Jaguar hybride des rives"

    # Pont Antigravity v6.4 : export navigateur tiles_canon_v6_4.json passe strict Python + audit_197 !
    cand64 = payload["candidate_canon_v64_strict"]
    schema64_errs = validate_tiles_canon_v6_4(cand64, strict=True)
    assert schema64_errs == [], f"Export tiles_canon_v6_4.json invalide : {schema64_errs}"
    audit64_rep = audit_tiles_catalog_197(cand64, allow_draft=False)
    assert audit64_rep["verdict_global"] == "OK", f"Audit 197 v6.4 échoué : {audit64_rep['errors']}"

    # Pont Antigravity v6.3 archive : export navigateur tiles_canon_v6_3.json toujours strictement valide
    cand = payload["candidate_canon_strict"]
    schema_errs = validate_tiles_canon_v6_3(cand, strict=True)
    assert schema_errs == [], f"Export tiles_canon_v6_3.json invalide : {schema_errs}"
    audit_rep = audit_tiles_catalog_197(cand, allow_draft=False)
    assert audit_rep["verdict_global"] == "OK", f"Audit 197 échoué sur export candidat : {audit_rep['errors']}"
