"""Tests de rendu headless, garde-fous sémantiques SSOT v6.2 et linter Canon 0 d'Amazonia Doc Studio.

Exécuté automatiquement par `pytest` (porte [9/10] de `verify_lot.py`) sans dépendance npm :
1. Vérifie les schémas SSOT de `amazonia_data_v6_0.js` (`VERSION_CHANGELOG`, `TOPOLOGIES_PISTE_SPEC`,
   `CHASSIS_AXES_SPEC` verrouillé avec `Placement_Initial_Machines.defaultVal = 'BULLDOZER_P1_ABATTEUSE_P2'`,
   30 tuiles du Canon 0 dans `CATALOGUE_TUILES`).
2. Exécute le rendu complet `refreshAllUI()` de `docs/index.html` + `livret_v6_0.js` dans
   Node `vm` sur un mini-DOM mocké :
   - vérifie `0 écart` initial sur le châssis et la neutralisation des axes morts `v6.0` ;
   - teste l'appel à `resetChassisToDefault()` ;
   - vérifie le rendu sans erreur JS des 30 tuiles du Canon 0 ;
   - active automatiquement le contrôleur bloquant `data-inv="INV-01"` .. `data-inv="INV-22"`
     dès que `livret` déclare `LIVRET_SCHEMA_VERSION = "6.2.0"` (Chantier 2).
3. Vérifie le linter automatique `verify_tiles_canon` et le scanner global anti-vestiges.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from verify_lot import (
    lint_tiles_canon_dict,
    verify_global_anti_vestiges,
    verify_tiles_canon,
)

ROOT = Path(__file__).resolve().parent.parent
GUARDS_PATH = ROOT / "contracts" / "studio_rules_guards.json"
INVARIANTS_PATH = ROOT / "contracts" / "physical_and_edge_invariants.json"
TILES_CANON_PATH = ROOT / "contracts" / "tiles_canon_v6_2.json"
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"


def check_rulebook_html_invariants(
    rulebook_html: str,
    invariants_doc: dict[str, Any],
) -> list[str]:
    """Vérifie la présence de chaque `data-inv="INV-XX"` et de ses `assertions_livret` dans le HTML."""
    errors: list[str] = []
    for inv in invariants_doc.get("invariants", []):
        inv_id = str(inv["id"])
        attr_pat = re.compile(rf'data-inv=["\'][^"\']*\b{re.escape(inv_id)}\b[^"\']*["\']')
        if not attr_pat.search(rulebook_html):
            errors.append(f"Attribut HTML manquant dans #rulebook-article : data-inv=\"{inv_id}\"")
        for assertion in inv.get("assertions_livret", []):
            if str(assertion).lower() not in rulebook_html.lower():
                errors.append(
                    f"Assertion livret manquante pour {inv_id} : {assertion!r}"
                )
    return errors


_NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, guardsPath, invariantsPath] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const guards = JSON.parse(fs.readFileSync(guardsPath, 'utf8'));
const invariantsDoc = JSON.parse(fs.readFileSync(invariantsPath, 'utf8'));

// Extract inline <script> blocks from docs/index.html (skipping external <script src=...>)
const inlineScripts = [];
for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
  inlineScripts.push(m[1]);
}
if (inlineScripts.length === 0) {
  throw new Error('Aucun script inline trouvé dans docs/index.html');
}

// Lightweight mock DOM supporting all IDs referenced by docs/index.html & livret_v6_0.js
function makeElement(id) {
  const classes = new Set();
  const el = {
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
    set innerHTML(v) {
      this._innerHTML = String(v);
      const opts = [];
      for (const om of this._innerHTML.matchAll(/<option[^>]*value="([^"]*)"/g)) {
        opts.push({ value: om[1] });
      }
      if (opts.length > 0) this.options = opts;
    },
    get textContent() { return this._textContent; },
    set textContent(v) { this._textContent = String(v); },
    addEventListener: () => {},
    querySelectorAll: () => [],
    querySelector: () => null,
    focus: () => {},
    click: () => {},
  };
  return el;
}

const elements = new Map();
function getEl(id) {
  if (!elements.has(id)) elements.set(id, makeElement(id));
  return elements.get(id);
}

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
  location: { protocol: 'https:', href: 'https://example.invalid/' },
  fetch: async () => ({ ok: false, json: async () => ({}) }),
  tailwind: {},
  document: {
    getElementById: (id) => getEl(id),
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: (tag) => makeElement(tag),
  },
  window: {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

// Load Studio layers in exact browser order
vm.runInContext(dataJs, sandbox, { filename: dataPath });
vm.runInContext(livretJs, sandbox, { filename: livretPath });
for (let i = 0; i < inlineScripts.length; i++) {
  vm.runInContext(inlineScripts[i], sandbox, { filename: `docs/index.html#script${i}` });
}

// 1. Validate VERSION_CHANGELOG, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC & 30 Canon 0 tiles
const schemaReport = vm.runInContext(`(() => {
  const errs = [];
  if (!Array.isArray(VERSION_CHANGELOG) || VERSION_CHANGELOG.length === 0) {
    errs.push('VERSION_CHANGELOG vide ou absent');
  } else {
    if (VERSION_CHANGELOG[0].version !== 'v6.2') {
      errs.push('VERSION_CHANGELOG[0].version attendu v6.2, trouvé ' + VERSION_CHANGELOG[0].version);
    }
    for (const b of VERSION_CHANGELOG) {
      if (!b.version || !b.titre || !b.resume) errs.push('Bloc changelog incomplet: ' + b.version);
      if (!Array.isArray(b.deltas) || b.deltas.length === 0) {
        errs.push('Bloc changelog sans deltas[]: ' + b.version);
      } else {
        for (const d of b.deltas) {
          if (!d.domaine || !d.avant || !d.apres) errs.push('Delta incomplet dans ' + b.version);
        }
      }
    }
  }
  const topoKeys = Object.keys(TOPOLOGIES_PISTE_SPEC || {});
  if (!topoKeys.includes('P4_2233')) errs.push('Topologie canonique P4_2233 absente');
  for (const k of topoKeys) {
    const t = TOPOLOGIES_PISTE_SPEC[k];
    const sumDot = (t.dotation || []).reduce((a, b) => a + b, 0);
    if (t.code !== k) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].code != ' + k);
    if (t.somme !== sumDot) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].somme != sum(dotation)');
    if (t.arbres_par_rayon !== sumDot) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].arbres_par_rayon != sum(dotation)');
  }
  const placementAx = CHASSIS_AXES_SPEC.find(a => a.key === 'Placement_Initial_Machines');
  if (!placementAx || placementAx.defaultVal !== 'BULLDOZER_P1_ABATTEUSE_P2') {
    errs.push('Bug C3-06 : Placement_Initial_Machines.defaultVal doit valoir BULLDOZER_P1_ABATTEUSE_P2');
  }
  const tileKeys = Object.keys(CATALOGUE_TUILES || {});
  if (tileKeys.length !== 30) {
    errs.push('Attendu exactement 30 tuiles Canon 0 dans CATALOGUE_TUILES, trouvé ' + tileKeys.length);
  }
  return {
    errs,
    topoKeys,
    tileKeys,
    catalogueTuilesJson: JSON.stringify(CATALOGUE_TUILES),
    livretSchemaVersion: typeof LIVRET_SCHEMA_VERSION !== 'undefined' ? LIVRET_SCHEMA_VERSION : null,
  };
})()`, sandbox);

if (schemaReport.errs.length > 0) {
  throw new Error('Erreurs schéma Studio:\n' + schemaReport.errs.join('\n'));
}

// 2. Check banned patterns in CATALOGUE_TUILES
for (const pat of guards.banned_in_catalogue_tuiles || []) {
  if (schemaReport.catalogueTuilesJson.includes(pat)) {
    throw new Error(`Motif banni trouvé dans CATALOGUE_TUILES: ${JSON.stringify(pat)}`);
  }
}

// 3. Initial render: verify 0 écart on chassis, locked axes neutralization, resetChassisToDefault(), and 30 Canon 0 tiles
const chassisReport = vm.runInContext(`(() => {
  refreshAllUI();
  const initialModified = getModifiedAxesList().length;
  const initialBadge = document.getElementById('modified-axes-count').textContent;
  const initialPlacement = state.chassis.Placement_Initial_Machines;
  const initialConfigIdx = computeConfigurationIndex();

  // Attempt to mutate a locked dead v6.0 axis via UI handler
  updateChassisAxis('Placement_Initial_Machines', 'MEME_PARCELLE_P1');
  updateChassisAxis('Offset_Seuil_Parade', '1');
  const afterLockedAttemptPlacement = state.chassis.Placement_Initial_Machines;
  const afterLockedAttemptModified = getModifiedAxesList().length;

  // Force corrupt state in memory then call resetChassisToDefault()
  state.chassis.Placement_Initial_Machines = 'MEME_PARCELLE_P1';
  state.chassis.Offset_Seuil_Parade = 1;
  resetChassisToDefault();
  const afterResetPlacement = state.chassis.Placement_Initial_Machines;
  const afterResetOffset = state.chassis.Offset_Seuil_Parade;
  const afterResetModified = getModifiedAxesList().length;
  const afterResetBadge = document.getElementById('modified-axes-count').textContent;

  return {
    initialModified,
    initialBadge,
    initialPlacement,
    initialConfigIdx,
    afterLockedAttemptPlacement,
    afterLockedAttemptModified,
    afterResetPlacement,
    afterResetOffset,
    afterResetModified,
    afterResetBadge,
  };
})()`, sandbox);

if (chassisReport.initialModified !== 0 || chassisReport.initialBadge !== '0 écart') {
  throw new Error('Bug C3-06 : attendu 0 écart initial, obtenu ' + JSON.stringify(chassisReport));
}
if (chassisReport.initialPlacement !== 'BULLDOZER_P1_ABATTEUSE_P2') {
  throw new Error('Placement initial incorrect : ' + chassisReport.initialPlacement);
}
if (chassisReport.afterLockedAttemptPlacement !== 'BULLDOZER_P1_ABATTEUSE_P2' || chassisReport.afterLockedAttemptModified !== 0) {
  throw new Error('Axes morts v6.0 non neutralisés : ' + JSON.stringify(chassisReport));
}
if (
  chassisReport.afterResetPlacement !== 'BULLDOZER_P1_ABATTEUSE_P2' ||
  chassisReport.afterResetOffset !== 0 ||
  chassisReport.afterResetModified !== 0 ||
  chassisReport.afterResetBadge !== '0 écart'
) {
  throw new Error('resetChassisToDefault() ne rétablit pas 0 écart sur standard v6.2 : ' + JSON.stringify(chassisReport));
}

// Verify all 30 Canon 0 tiles render cleanly without JS errors or NaN/undefined
const catalogueHtml = getEl('catalogue-grid').innerHTML;
const catalogueCountBadge = getEl('catalogue-count-badge').textContent;
if (!catalogueCountBadge.includes('30 emplacements') || !catalogueCountBadge.includes('30 profils')) {
  throw new Error('Compteur Explorateur inattendu : ' + catalogueCountBadge);
}
for (const tid of schemaReport.tileKeys) {
  if (!catalogueHtml.includes(`>${tid}<`)) {
    throw new Error(`Tuile Canon 0 non rendue dans #catalogue-grid : ${tid}`);
  }
}

const watchedIds = [
  'header-config-badge',
  'summary-peuples-pill',
  'summary-piege-pill',
  'summary-arbres-pill',
  'rulebook-article',
  'catalogue-grid',
  'changelog-content',
  'json-manifest-output',
];
for (const id of watchedIds) {
  const el = getEl(id);
  const combined = (el.textContent || '') + '\n' + (el.innerHTML || '');
  for (const banned of guards.banned_in_rendered_dom || []) {
    const re = new RegExp(`\\b${banned}\\b`);
    if (re.test(combined)) {
      throw new Error(`Motif interdit "${banned}" dans #${id}`);
    }
  }
}
const changelogHtml = getEl('changelog-content').innerHTML;
if (!changelogHtml || changelogHtml.length < 200 || !changelogHtml.includes('v6.2')) {
  throw new Error('changelog-content vide ou sans entrée v6.2 après refreshAllUI()');
}

// 4. Check positive rulebook assertions per table composition
for (const check of guards.required_livret_assertions || []) {
  vm.runInContext(`(() => {
    state.peuplesCercle = ${JSON.stringify(check.peuples)};
    state.chassis.Profil_Piste = 'P4_2233';
    refreshAllUI();
  })()`, sandbox);
  const livretHtml = getEl('rulebook-article').innerHTML;
  for (const banned of guards.banned_in_livret || []) {
    if (livretHtml.includes(banned)) {
      throw new Error(
        `Motif interdit "${banned}" dans le Livret rendu (#rulebook-article) pour table ${check.peuples.join('-')}`
      );
    }
  }
  for (const expected of check.must_contain) {
    if (!livretHtml.includes(expected)) {
      throw new Error(
        `Assertion Livret échouée pour table ${check.peuples.join('-')} : texte manquant ${JSON.stringify(expected)}`
      );
    }
  }
}

// 5. Blocking LIVRET_SCHEMA_VERSION === '6.2.0' & INV-01..INV-22 data-inv guard (Chantier 2)
if (schemaReport.livretSchemaVersion !== '6.2.0') {
  throw new Error(
    `LIVRET_SCHEMA_VERSION === "6.2.0" exigé (obtenu ${JSON.stringify(schemaReport.livretSchemaVersion)})`
  );
}
const invGuardActivated = true;
vm.runInContext(`(() => {
  resetLivretComplet();
})()`, sandbox);
const fullLivretHtml = getEl('rulebook-article').innerHTML;
const fullLower = fullLivretHtml.toLowerCase();
let invariantsVerified = 0;
for (const inv of invariantsDoc.invariants || []) {
  const invRe = new RegExp(`data-inv=["'][^"']*\\b${inv.id}\\b[^"']*["']`);
  if (!invRe.test(fullLivretHtml)) {
    throw new Error(`Invariant ${inv.id} manquant dans #rulebook-article (attribut data-inv="${inv.id}" requis en 6.2.0)`);
  }
  for (const phrase of inv.assertions_livret || []) {
    if (!fullLower.includes(String(phrase).toLowerCase())) {
      throw new Error(`Assertion livret manquante pour ${inv.id} : ${JSON.stringify(phrase)}`);
    }
  }
  invariantsVerified++;
}

// Verify zero numeric step codes (1.1, 3.2, 4.2, 5.3...) in rendered player prose
const proseOnly = fullLivretHtml
  .replace(/<style[\s\S]*?<\/style>/gi, ' ')
  .replace(/<[^>]+>/g, ' ');
const stepCodeHits = proseOnly.match(/\b[1-6]\.[0-3]\b/g);
if (stepCodeHits && stepCodeHits.length > 0) {
  throw new Error(`Codes numériques d'étape interdits dans la prose du livret : ${JSON.stringify(stepCodeHits)}`);
}

// 5b. Interactive modular table filter tests in Node vm
function inspectRenderedVisibility(htmlStr) {
  const modules = { GARDIENS: [], REVES: [], ESSAIM: [] };
  const peoples = { H: [], E: [], M: [], R: [], O: [], I: [] };

  for (const m of htmlStr.matchAll(/<[^>]+data-module="(GARDIENS|REVES|ESSAIM)"[^>]*>/g)) {
    const tag = m[0];
    const modName = m[1];
    const isHidden = /\bhidden\b/.test(tag) || tag.includes('livret-hidden') || tag.includes('data-module-active="false"');
    modules[modName].push({ visible: !isHidden, tag });
  }
  for (const m of htmlStr.matchAll(/<[^>]+data-peuple="([HEMROI])"[^>]*>/g)) {
    const tag = m[0];
    const pCode = m[1];
    const isHidden = /\bhidden\b/.test(tag) || tag.includes('livret-hidden') || tag.includes('data-peuple-active="false"');
    peoples[pCode].push({ visible: !isHidden, tag });
  }
  return { modules, peoples };
}

const fnCheck = vm.runInContext(`({
  setFn: typeof globalThis.setLivretTablePeoples,
  toggleFn: typeof globalThis.toggleLivretPeuple,
  resetFn: typeof globalThis.resetLivretComplet,
})`, sandbox);
if (fnCheck.setFn !== 'function' || fnCheck.toggleFn !== 'function' || fnCheck.resetFn !== 'function') {
  throw new Error('Fonctions globales interactives manquantes : ' + JSON.stringify(fnCheck));
}

const scenarios = guards.required_livret_filter_scenarios || [];
if (scenarios.length < 4) {
  throw new Error('Attendu au moins 4 scénarios dans required_livret_filter_scenarios');
}
for (const sc of scenarios) {
  let stateAfter;
  if (sc.action === 'setLivretTablePeoples') {
    stateAfter = vm.runInContext(`globalThis.setLivretTablePeoples(${JSON.stringify(sc.peuples)})`, sandbox);
  } else if (sc.action === 'resetLivretComplet') {
    stateAfter = vm.runInContext(`globalThis.resetLivretComplet()`, sandbox);
  } else {
    throw new Error('Action de scénario inconnue : ' + sc.action);
  }
  if (stateAfter.mode !== sc.expected_mode) {
    throw new Error(`Mode filtre inattendu pour ${sc.action}(${sc.peuples}): attendu ${sc.expected_mode}, obtenu ${stateAfter.mode}`);
  }
  const renderedHtml = getEl('rulebook-article').innerHTML;
  const vis = inspectRenderedVisibility(renderedHtml);

  for (const [modName, expectedVis] of Object.entries(sc.expected_modules)) {
    const entries = vis.modules[modName] || [];
    if (entries.length === 0) {
      throw new Error(`Aucun élément data-module="${modName}" trouvé dans #rulebook-article`);
    }
    for (const entry of entries) {
      if (entry.visible !== expectedVis) {
        throw new Error(
          `Visibilité incorrecte sur data-module="${modName}" pour ${sc.action}(${sc.peuples.join('-')}): attendu visible=${expectedVis}, balise=${entry.tag}`
        );
      }
    }
  }
  for (const pCode of sc.expected_peuples_visible || []) {
    const entries = vis.peoples[pCode] || [];
    if (entries.length === 0 || entries.some(e => !e.visible)) {
      throw new Error(`Fiche data-peuple="${pCode}" attendue visible pour ${sc.action}(${sc.peuples.join('-')})`);
    }
  }
  for (const pCode of sc.expected_peuples_hidden || []) {
    const entries = vis.peoples[pCode] || [];
    if (entries.length === 0 || entries.some(e => e.visible)) {
      throw new Error(`Fiche data-peuple="${pCode}" attendue masquée pour ${sc.action}(${sc.peuples.join('-')})`);
    }
  }
}

// Verify toggleLivretPeuple dynamically toggles modules and people cards
vm.runInContext(`globalThis.setLivretTablePeoples(['M', 'R', 'O', 'I'])`, sandbox);
vm.runInContext(`globalThis.toggleLivretPeuple('H')`, sandbox);
const afterAddH = inspectRenderedVisibility(getEl('rulebook-article').innerHTML);
if (afterAddH.modules.REVES.some(e => !e.visible) || afterAddH.peoples.H.some(e => !e.visible)) {
  throw new Error('toggleLivretPeuple("H") doit réafficher REVES et la fiche H');
}
vm.runInContext(`globalThis.toggleLivretPeuple('I')`, sandbox);
const afterRemoveI = inspectRenderedVisibility(getEl('rulebook-article').innerHTML);
if (afterRemoveI.modules.ESSAIM.some(e => e.visible) || afterRemoveI.peoples.I.some(e => e.visible)) {
  throw new Error('toggleLivretPeuple("I") doit masquer ESSAIM et la fiche I');
}
vm.runInContext(`globalThis.resetLivretComplet()`, sandbox);
const afterFinalReset = inspectRenderedVisibility(getEl('rulebook-article').innerHTML);
for (const modName of ['GARDIENS', 'REVES', 'ESSAIM']) {
  if (afterFinalReset.modules[modName].some(e => !e.visible)) {
    throw new Error(`resetLivretComplet() doit réafficher 100 % du module ${modName}`);
  }
}
for (const pCode of ['H', 'E', 'M', 'R', 'O', 'I']) {
  if (afterFinalReset.peoples[pCode].some(e => !e.visible)) {
    throw new Error(`resetLivretComplet() doit réafficher la fiche Peuple ${pCode}`);
  }
}

// Verify no-document safety guard (pure Node context without `document`)
const bareCtx = { console, Math, JSON, Object, Array, String, Number, Boolean, Set, Map, RegExp };
bareCtx.globalThis = bareCtx;
vm.createContext(bareCtx);
vm.runInContext(livretJs, bareCtx, { filename: 'livret_no_dom.js' });
const bareState = vm.runInContext(`(() => {
  globalThis.setLivretTablePeoples(['H', 'M', 'O']);
  globalThis.toggleLivretPeuple('I');
  const st = globalThis.resetLivretComplet();
  const out = renderDidacticRulebook();
  return { mode: st.mode, out };
})()`, bareCtx);
if (bareState.mode !== 'COMPLET' || bareState.out !== '') {
  throw new Error('Protection typeof document !== "undefined" invalide : ' + JSON.stringify(bareState));
}

// 6. Verify quick-access links & dynamic highlight label in docs/index.html
const expectedBriques = [
  'brique-mise-en-place',
  'brique-preparation',
  'brique-pose',
  'brique-ouverture-reves',
  'brique-furtivite',
  'brique-nids-migration',
  'brique-attaques-piegeages',
  'brique-menage',
  'brique-gardiens-eveil',
  'brique-reves-sommeil',
  'brique-peuple-insectes',
  'brique-memento',
];
if (!html.includes('selon vos réglages v6.2') || html.includes('selon vos réglages v6.0')) {
  throw new Error('Libellé dynamique de docs/index.html non aligné sur v6.2');
}
if (html.includes('livret_v5_3.js')) {
  throw new Error('Commentaire obsolète livret_v5_3.js encore présent dans docs/index.html');
}
const lastLivretHtml = getEl('rulebook-article').innerHTML;
for (const bid of expectedBriques) {
  if (!html.includes(`href="#${bid}"`)) {
    throw new Error(`Lien rapide manquant dans docs/index.html : href="#${bid}"`);
  }
  if (!lastLivretHtml.includes(`id="${bid}"`)) {
    throw new Error(`Ancre de brique manquante dans le Livret rendu : id="${bid}"`);
  }
}

vm.runInContext(`(() => {
  toggleDynamicHighlight(false);
  toggleDynamicHighlight(true);
  state.peuplesCercle = ['M', 'H', 'I'];
  refreshAllUI();
})()`, sandbox);
const n3LivretHtml = getEl('rulebook-article').innerHTML;
if (!n3LivretHtml.includes('Table à 3 joueurs')) {
  throw new Error('Interpolation dynamique N=3 absente du Livret rendu');
}

console.log(JSON.stringify({
  ok: true,
  livret_schema_version: schemaReport.livretSchemaVersion,
  topologies_checked: schemaReport.topoKeys.length,
  tiles_rendered: schemaReport.tileKeys.length,
  tables_checked: (guards.required_livret_assertions || []).length,
  briques_checked: expectedBriques.length,
  inv_guard_activated: invGuardActivated,
  invariants_registered: (invariantsDoc.invariants || []).length,
  invariants_verified: invariantsVerified,
  filter_scenarios_checked: scenarios.length,
  toggle_checked: true,
  no_document_guard_ok: true,
}));
"""


def test_studio_banned_terms_in_livret_source() -> None:
    """Interdit tout résidu textuel de règles obsolètes ou jargon interne et impose UTF-8 sans BOM / LF."""
    guards = json.loads(GUARDS_PATH.read_text(encoding="utf-8"))
    raw_bytes = STUDIO_LIVRET.read_bytes()
    assert not raw_bytes.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {STUDIO_LIVRET.name}"
    assert b"\r\n" not in raw_bytes, f"Fins de ligne CRLF interdites dans {STUDIO_LIVRET.name} (LF requis)"
    livret_src = raw_bytes.decode("utf-8")
    violations = [pat for pat in guards["banned_in_livret"] if pat in livret_src]
    assert not violations, f"Résidus obsolètes détectés dans {STUDIO_LIVRET.name} : {violations}"


def test_studio_headless_render_and_semantic_guards() -> None:
    """Exécute refreshAllUI() en headless Node vm : 0 écart, 30 tuiles, 22 INV et filtre interactif."""
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(STUDIO_LIVRET),
            str(GUARDS_PATH),
            str(INVARIANTS_PATH),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Échec du test de rendu headless Studio :\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    assert payload["ok"] is True
    assert payload["livret_schema_version"] == "6.2.0"
    assert payload["topologies_checked"] == 1
    assert payload["tiles_rendered"] == 30
    assert payload["tables_checked"] == 4
    assert payload["briques_checked"] == 12
    assert payload["inv_guard_activated"] is True
    assert payload["invariants_registered"] == 22
    assert payload["invariants_verified"] == 22
    assert payload["filter_scenarios_checked"] == 4
    assert payload["toggle_checked"] is True
    assert payload["no_document_guard_ok"] is True


def test_inv_html_guard_enforces_all_22_invariants_when_livret_is_6_2() -> None:
    """Prouve que le contrôleur data-inv='INV-XX' prêt pour Chantier 2 bloque tout invariant manquant."""
    inv_doc = json.loads(INVARIANTS_PATH.read_text(encoding="utf-8"))
    assert len(inv_doc["invariants"]) == 22

    # 1. HTML synthétique couvrant tous les 22 data-inv et leurs assertions -> 0 erreur
    blocks: list[str] = []
    for inv in inv_doc["invariants"]:
        phrases = " ".join(inv["assertions_livret"])
        blocks.append(f'<section data-inv="{inv["id"]}">{phrases}</section>')
    complete_html = "\n".join(blocks)
    assert check_rulebook_html_invariants(complete_html, inv_doc) == []

    # 2. Suppression de INV-11 -> erreur bloquante immédiate
    incomplete_html = "\n".join(b for b in blocks if 'data-inv="INV-11"' not in b)
    errs = check_rulebook_html_invariants(incomplete_html, inv_doc)
    assert any("INV-11" in e for e in errs)


def test_tiles_canon_linter_and_anti_vestiges_guards() -> None:
    """Vérifie le linter structurel (I07 sans C02 : positif + négatifs) et le scanner global anti-vestiges."""
    verify_tiles_canon()
    verify_global_anti_vestiges()

    canon = json.loads(TILES_CANON_PATH.read_text(encoding="utf-8"))["tuiles_ciblees"]

    # Cas positif I07 : C02 purgé — un texte riche (> 25 mots, multi-phrases, multi-conditions) passe sans erreur
    rich_text = copy.deepcopy(canon)
    rich_text["G1"]["profils"]["A"]["texte"] = (
        "<strong>Face 1 :</strong> Si une parcelle ciblée porte un jeton Duel, déplacez un "
        "Défenseur en attente vers cette parcelle puis retournez un jeton rouge en bleu. "
        "Lorsque le Duel bascule ensuite sur Territoire tenu, vous pouvez également "
        "glisser une encoche de pari sur le Jaguar sans dépenser de pion supplémentaire."
    )
    errs_rich = lint_tiles_canon_dict(rich_text)
    assert errs_rich == [], f"I07 violé — C02 ne doit plus bloquer les textes riches : {errs_rich}"

    # Cas négatif 1 : dette mémorielle flottante (`mem_debt = 0`)
    bad_mem = copy.deepcopy(canon)
    bad_mem["G1"]["profils"]["A"]["texte"] = (
        "<strong>Face 1 :</strong> Les machines subissent -1 au Seuil de Parade pour ce tour."
    )
    errs_mem = lint_tiles_canon_dict(bad_mem)
    assert any("terme banni 'pour ce tour'" in e for e in errs_mem)

    # Cas négatif 2 : code d'étape numérique 3.2 et jargon de pioche obsolète ('carte Machine', 'paquet')
    bad_step = copy.deepcopy(canon)
    bad_step["G2"]["profils"]["A"]["texte"] = (
        "<strong>Face 1 :</strong> En 3.2, défaussez une carte Machine du paquet."
    )
    errs_step = lint_tiles_canon_dict(bad_step)
    assert any("code numérique d'étape" in e for e in errs_step)
    assert any("terme banni 'carte Machine'" in e for e in errs_step)
    assert any("terme banni 'paquet'" in e for e in errs_step)

    # Cas négatif 3 : Insecte mentionné hors des 10 tuiles des 5 lisières de I
    bad_insect = copy.deepcopy(canon)
    bad_insect["G1"]["profils"]["A"]["texte"] = (
        "<strong>Face 1 :</strong> Ajoutez 1 Insecte sur une parcelle ciblée."
    )
    errs_insect = lint_tiles_canon_dict(bad_insect)
    assert any("hors lisières de I" in e for e in errs_insect)

    # Cas négatif 4 : Gardien mentionné sur une tuile A=0 (R1)
    bad_a0 = copy.deepcopy(canon)
    bad_a0["R1"]["profils"]["A"]["texte"] = (
        "À l’ouverture, activez un Gardien voisin."
    )
    errs_a0 = lint_tiles_canon_dict(bad_a0)
    assert any("tuile A=0" in e for e in errs_a0)


_NODE_COPY_DIGEST_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, digestPath] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const digestRaw = fs.readFileSync(digestPath, 'utf8');
const digestObj = JSON.parse(digestRaw);

if (!html.includes('id="btn-copy-digest-gemini"') || !html.includes('📋 Copier Bilan Gemini')) {
  throw new Error('Bouton #btn-copy-digest-gemini absent de docs/index.html');
}

const inlineScripts = [];
for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
  inlineScripts.push(m[1]);
}

function makeElement(id) {
  const classes = new Set(id === 'btn-copy-digest-gemini' ? ['hidden'] : []);
  return {
    id,
    _innerHTML: id === 'btn-copy-digest-gemini' ? '<span>📋 Copier Bilan Gemini</span>' : '',
    _textContent: '',
    disabled: id === 'btn-copy-digest-gemini',
    value: '',
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
    setAttribute: () => {},
    addEventListener: () => {},
    querySelectorAll: () => [],
    querySelector: () => null,
    focus: () => {},
    select: () => {},
    setSelectionRange: () => {},
    click: () => {},
  };
}

const elements = new Map();
function getEl(id) {
  if (!elements.has(id)) elements.set(id, makeElement(id));
  return elements.get(id);
}

let fetchCallsDuringCopy = 0;
let trackingCopyFetch = false;
let clipboardWrites = [];
let fallbackTextareas = [];
let execCopyCount = 0;

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
  TextEncoder,
  parseInt,
  parseFloat,
  isNaN,
  encodeURIComponent,
  decodeURIComponent,
  setTimeout: () => 1,
  clearTimeout: () => {},
  localStorage: { _m: {}, getItem(k) { return this._m[k] || null; }, setItem(k, v) { this._m[k] = String(v); } },
  navigator: {
    clipboard: {
      writeText: (txt) => {
        clipboardWrites.push(txt);
        return Promise.resolve();
      },
    },
  },
  location: { protocol: 'https:', href: 'https://example.invalid/' },
  fetch: async () => {
    if (trackingCopyFetch) fetchCallsDuringCopy++;
    return { ok: false, json: async () => ({}) };
  },
  tailwind: {},
  document: {
    getElementById: (id) => getEl(id),
    querySelector: () => null,
    querySelectorAll: () => [],
    createElement: (tag) => {
      const el = makeElement(tag);
      if (tag === 'textarea') fallbackTextareas.push(el);
      return el;
    },
    body: {
      appendChild: () => {},
      removeChild: () => {},
    },
    execCommand: (cmd) => {
      if (cmd === 'copy') execCopyCount++;
      return true;
    },
  },
  window: {},
};
sandbox.window = sandbox;
sandbox.globalThis = sandbox;
vm.createContext(sandbox);

vm.runInContext(dataJs, sandbox, { filename: dataPath });
vm.runInContext(livretJs, sandbox, { filename: livretPath });
for (let i = 0; i < inlineScripts.length; i++) {
  vm.runInContext(inlineScripts[i], sandbox, { filename: `docs/index.html#script${i}` });
}

// 1. Avant chargement : bouton masqué et désactivé
vm.runInContext('clearActiveDigest();', sandbox);
const btn = getEl('btn-copy-digest-gemini');
if (!btn.classList.contains('hidden') || btn.disabled !== true) {
  throw new Error('Le bouton Copier Bilan Gemini doit être masqué et désactivé sans bilan');
}

// 2. Après chargement en mémoire : bouton visible et actif
sandbox.__TEST_DIGEST = digestObj;
sandbox.__TEST_DIGEST_RAW = digestRaw;
vm.runInContext('applyLoadedDigest(__TEST_DIGEST, "digests/digest_micro_validation.json", __TEST_DIGEST_RAW);', sandbox);
if (btn.classList.contains('hidden') || btn.disabled !== false) {
  throw new Error('Le bouton Copier Bilan Gemini doit être visible et actif avec un bilan chargé');
}

// 3. Clic synchrone via navigator.clipboard (zéro fetch)
trackingCopyFetch = true;
vm.runInContext('copyActiveDigestForGemini();', sandbox);
trackingCopyFetch = false;

setImmediate(() => {
  try {
    if (fetchCallsDuringCopy !== 0) {
      throw new Error('copyActiveDigestForGemini ne doit jamais relancer de fetch');
    }
    if (clipboardWrites.length !== 1) {
      throw new Error('Attendu 1 écriture presse-papiers, obtenu ' + clipboardWrites.length);
    }
    const copied = clipboardWrites[0];
    const expectedPrefix = "Voici le bilan de campagne Amazonia : Dernier Rempart (règles cœur actives, tuiles testées et statistiques comme référence factuelle) :";
    if (!copied.startsWith(expectedPrefix)) {
      throw new Error('Amorce attendue absente au début du texte copié');
    }
    if (!copied.includes("Consignes de restitution pour l'auteur :") || !copied.includes("Continuité de la discussion avant tout")) {
      throw new Error('Consignes de restitution auteur absentes du texte copié');
    }
    if (!copied.includes('"active_core_rules"') || !copied.includes('"tested_tiles_rules"') || !copied.includes('"tile_metrics"')) {
      throw new Error('Le texte copié ne contient pas le digest complet');
    }
    if (!/✅ Bilan copié \(\d+ Ko\)/.test(btn.innerHTML)) {
      throw new Error('Retour visuel attendu sur le bouton absent: ' + btn.innerHTML);
    }

    // 4. Vérification du fallback synchrone <textarea> quand navigator.clipboard est absent (Android / file://)
    sandbox.navigator = {};
    vm.runInContext('copyActiveDigestForGemini();', sandbox);
    if (execCopyCount !== 1 || fallbackTextareas.length !== 1) {
      throw new Error('Fallback textarea + execCommand(copy) non déclenché');
    }
    if (!fallbackTextareas[0].value.startsWith(expectedPrefix)) {
      throw new Error('Contenu du fallback textarea invalide');
    }

    console.log(JSON.stringify({
      ok: true,
      copied_len: copied.length,
      button_feedback: btn.innerHTML,
      fallback_exec_copy: execCopyCount,
    }));
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
});
"""


def test_studio_copy_active_digest_for_gemini_mobile_one_tap() -> None:
    """Vérifie le bouton 1-tap `📋 Copier Bilan Gemini` et son fallback textarea dans docs/index.html."""
    digest_path = ROOT / "docs" / "digests" / "digest_micro_validation.json"
    assert digest_path.exists()
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_COPY_DIGEST_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(STUDIO_LIVRET),
            str(digest_path),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Échec du test Copier Bilan Gemini :\nSTDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    payload = json.loads(proc.stdout.strip().splitlines()[-1])
    assert payload["ok"] is True
    assert payload["copied_len"] > 5000
    assert payload["fallback_exec_copy"] == 1
    assert "✅ Bilan copié (" in payload["button_feedback"]
