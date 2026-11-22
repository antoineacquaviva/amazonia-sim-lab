"""Tests de rendu headless et garde-fous sémantiques d'Amazonia Doc Studio.

Exécuté automatiquement par `pytest` (porte [7/8] de `verify_lot.py`) sans aucune
dépendance npm :
1. Vérifie les schémas critiques de `amazonia_data_v5_5.js` (`VERSION_CHANGELOG[*].deltas`,
   `TOPOLOGIES_PISTE_SPEC[*].{code, p_max, dotation, somme, arbres_par_rayon}`).
2. Exécute le rendu complet `refreshAllUI()` de `docs/index.html` + `livret_v5_5.js` dans
   Node `vm` sur un mini-DOM mocké pour plusieurs tables (`0`, `1`, `2` peuples oniriques)
   et tous les 6 profils de pistes.
3. Vérifie : zéro exception JS, zéro `NaN` / `undefined` dans le DOM rendu, journal
   d'évolution non vide, et respect intégral des garde-fous de
   `contracts/studio_rules_guards.json` (termes bannis hors historique + assertions positives).
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUARDS_PATH = ROOT / "contracts" / "studio_rules_guards.json"
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v5_5.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v5_5.js"


_NODE_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, guardsPath] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const guards = JSON.parse(fs.readFileSync(guardsPath, 'utf8'));

// Extract inline <script> blocks from docs/index.html (skipping external <script src=...>)
const inlineScripts = [];
for (const m of html.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)) {
  inlineScripts.push(m[1]);
}
if (inlineScripts.length === 0) {
  throw new Error('Aucun script inline trouvé dans docs/index.html');
}

// Lightweight mock DOM supporting all IDs referenced by docs/index.html & livret_v5_5.js
function makeElement(id) {
  const classes = new Set();
  const el = {
    id,
    _innerHTML: '',
    _textContent: '',
    value: id === 'changelog-filter-select' ? 'ALL'
         : id === 'diff-version-select' ? 'v5.4.7'
         : id === 'filter-famille' || id === 'filter-peuple' || id === 'filter-tag' || id === 'filter-scope' ? 'ALL'
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
      // Extract <option value="..."> for <select> elements
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

// 1. Validate VERSION_CHANGELOG schema & TOPOLOGIES_PISTE_SPEC schema
const schemaReport = vm.runInContext(`(() => {
  const errs = [];
  if (!Array.isArray(VERSION_CHANGELOG) || VERSION_CHANGELOG.length === 0) {
    errs.push('VERSION_CHANGELOG vide ou absent');
  } else {
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
  if (topoKeys.length !== 6) errs.push('Attendu 6 topologies dans TOPOLOGIES_PISTE_SPEC, trouvé ' + topoKeys.length);
  for (const k of topoKeys) {
    const t = TOPOLOGIES_PISTE_SPEC[k];
    const sumDot = (t.dotation || []).reduce((a, b) => a + b, 0);
    if (t.code !== k) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].code != ' + k);
    if (t.somme !== sumDot) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].somme != sum(dotation)');
    if (t.arbres_par_rayon !== sumDot) errs.push('TOPOLOGIES_PISTE_SPEC[' + k + '].arbres_par_rayon != sum(dotation)');
  }
  return { errs, topoKeys, catalogueTuilesJson: JSON.stringify(CATALOGUE_TUILES) };
})()`, sandbox);

if (schemaReport.errs.length > 0) {
  throw new Error('Erreurs schéma Studio:\n' + schemaReport.errs.join('\n'));
}

// 2. Check banned patterns in CATALOGUE_TUILES (excluding VERSION_CHANGELOG history)
for (const pat of guards.banned_in_catalogue_tuiles || []) {
  if (schemaReport.catalogueTuilesJson.includes(pat)) {
    throw new Error(`Motif banni trouvé dans CATALOGUE_TUILES: ${JSON.stringify(pat)}`);
  }
}

// 3. Render across all 6 track profiles and check 0 exceptions, 0 NaN, 0 undefined
const watchedIds = [
  'header-config-badge',
  'summary-peuples-pill',
  'summary-piege-pill',
  'summary-arbres-pill',
  'rulebook-article',
  'catalogue-grid',
  'changelog-content',
  'json-output',
];

for (const topoCode of schemaReport.topoKeys) {
  vm.runInContext(`(() => {
    state.chassis.Profil_Piste = ${JSON.stringify(topoCode)};
    refreshAllUI();
  })()`, sandbox);
  for (const id of watchedIds) {
    const el = getEl(id);
    const combined = (el.textContent || '') + '\n' + (el.innerHTML || '');
    for (const banned of guards.banned_in_rendered_dom || []) {
      const re = new RegExp(`\\b${banned}\\b`);
      if (re.test(combined)) {
        throw new Error(`Motif interdit "${banned}" dans #${id} pour Profil_Piste=${topoCode}`);
      }
    }
  }
  const changelogHtml = getEl('changelog-content').innerHTML;
  if (!changelogHtml || changelogHtml.length < 200) {
    throw new Error('changelog-content est vide après refreshAllUI()');
  }
}

// 4. Check positive rulebook assertions per table composition (0, 1, 2 oniric peoples)
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

console.log(JSON.stringify({
  ok: true,
  topologies_checked: schemaReport.topoKeys.length,
  tables_checked: (guards.required_livret_assertions || []).length,
}));
"""


def test_studio_banned_terms_in_livret_source() -> None:
    """Interdit tout résidu textuel de règles obsolètes ou jargon interne dans docs/data/livret_v5_5.js."""
    guards = json.loads(GUARDS_PATH.read_text(encoding="utf-8"))
    livret_src = STUDIO_LIVRET.read_text(encoding="utf-8")
    violations = [pat for pat in guards["banned_in_livret"] if pat in livret_src]
    assert not violations, f"Résidus obsolètes détectés dans {STUDIO_LIVRET.name} : {violations}"


def test_studio_headless_render_and_semantic_guards() -> None:
    """Exécute refreshAllUI() en headless Node vm sur les 6 topologies et 3 tables oniriques."""
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(STUDIO_LIVRET),
            str(GUARDS_PATH),
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
    assert payload["topologies_checked"] == 6
    assert payload["tables_checked"] == 4


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
