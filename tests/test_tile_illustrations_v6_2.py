"""Tests headless Node vm dédiés aux 30 illustrations SVG Canon 0 & à l'icône Reptile v6.2.

Vérifie sans dépendance npm :
1. Encodage UTF-8 sans BOM, fins de lignes LF, ordre des balises `<script>` dans `docs/index.html`
   et syntaxe JS valide via `new vm.Script()`.
2. Présence de 30 médaillons `<svg ... viewBox="0 0 64 64">` distincts, non vides et XML bien formés
   pour `G1..G15`, `R1..R10`, `M1..M5` (aucune ressource externe).
3. Présence de la mini-icône Reptile SVG inline (`14×14`, `viewBox="0 0 24 24"`, et repli SVG dans
   la roue des 197 assises) dans tous les modes de l'Explorateur, avec absence totale de l'ancien
   émoji serpent (`🐍`) sur `R`.
4. Rendu complet sans erreur JS ni `undefined`/`NaN` dans les 3 modes de l'Explorateur, y compris
   en mode dégradé lorsque `tile_illustrations_v6_2.js` n'est pas chargé.
"""

from __future__ import annotations

import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"
ILLUSTRATIONS_JS = ROOT / "docs" / "tile_illustrations_v6_2.js"
EXPLORER_JS = ROOT / "docs" / "explorer_v6_2.js"
EXPLORER_CSS = ROOT / "docs" / "explorer_v6_2.css"

EXPECTED_TILE_IDS: tuple[str, ...] = (
    tuple(f"G{i}" for i in range(1, 16))
    + tuple(f"R{i}" for i in range(1, 11))
    + tuple(f"M{i}" for i in range(1, 6))
)

SNAKE_EMOJI = "\U0001f40d"  # 🐍

_NODE_ILLUSTRATIONS_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, illPath, explorerPath, loadIllustrations] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const illJs = fs.readFileSync(illPath, 'utf8');
const explorerJs = fs.readFileSync(explorerPath, 'utf8');

// Validation syntaxique stricte via new vm.Script()
new vm.Script(illJs, { filename: illPath });
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
    addEventListener: () => {},
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
if (loadIllustrations === '1') {
  vm.runInContext(illJs, sandbox, { filename: illPath });
}
vm.runInContext(explorerJs, sandbox, { filename: explorerPath });
for (let i = 0; i < inlineScripts.length; i++) {
  vm.runInContext(inlineScripts[i], sandbox, { filename: `docs/index.html#script${i}` });
}

const exp = sandbox.AmazoniaExplorerV62;
const ill = sandbox.AmazoniaTileIllustrationsV62 || null;
if (!exp) throw new Error('AmazoniaExplorerV62 non exposé sur window');

const badTokenRe = /\b(?:NaN|undefined)\b/;
sandbox.refreshAllUI();

// Mode 1 : Les 15 Lisières
exp.setMode('lisieres');
const m1Toolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const m1Grid = getEl('catalogue-grid').innerHTML;
const m1Medallions = Array.from(m1Grid.matchAll(/data-tile-illustration="([^"]+)"/g)).map(m => m[1]);
const m1ReptileSvgs = (m1Grid.match(/data-peuple-icon="R"/g) || []).length;

// Mode 2 : Table & Roue des 197 Assises (tables contenant R)
exp.setMode('assises');
exp.selectPresetAssise('N3-MRO');
const m2MroToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const m2MroGrid = getEl('catalogue-grid').innerHTML;
const m2MroWheelHasReptileSvg = /class="exp-wheel-peuple-icon exp-peuple-icon-R"/.test(m2MroGrid);
const m2MroMedallions = Array.from(m2MroGrid.matchAll(/data-tile-illustration="([^"]+)"/g)).map(m => m[1]);

exp.selectPresetAssise('N6-HEMROI');
const m2N6Toolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const m2N6Grid = getEl('catalogue-grid').innerHTML;
const m2N6WheelHasReptileSvg = /class="exp-wheel-peuple-icon exp-peuple-icon-R"/.test(m2N6Grid);
const m2N6Medallions = Array.from(m2N6Grid.matchAll(/data-tile-illustration="([^"]+)"/g)).map(m => m[1]);

// Mode 3 : Grammaires par Peuple (3+3) sur les 6 onglets
exp.setMode('peuples');
const m3ByPeuple = {};
let m3AllHtml = '';
for (const pCode of ['H', 'E', 'M', 'R', 'O', 'I']) {
  exp.setPeupleTab(pCode);
  const tHtml = getEl('explorer-v6-2-toolbar').innerHTML;
  const gHtml = getEl('catalogue-grid').innerHTML;
  m3AllHtml += tHtml + '\n' + gHtml + '\n';
  m3ByPeuple[pCode] = {
    medallions: (gHtml.match(/data-tile-illustration="/g) || []).length,
    reptile_svgs: (gHtml.match(/data-peuple-icon="R"/g) || []).length,
    has_bad: badTokenRe.test(tHtml + '\n' + gHtml),
  };
}

// Focus Rayons X sur une tuile Reptile (G5 : Coup de Queue de l'Iguane, consomme/amorce R)
exp.setMode('lisieres');
exp.toggleXRay('G2');
const xrayToolbar = getEl('explorer-v6-2-toolbar').innerHTML;
const xrayGrid = getEl('catalogue-grid').innerHTML;
const xrayReptileAccSvg = /data-peuple-icon="R"/.test(xrayToolbar);
exp.clearXRay();

const combinedAllHtml = [
  m1Toolbar,
  m1Grid,
  m2MroToolbar,
  m2MroGrid,
  m2N6Toolbar,
  m2N6Grid,
  m3AllHtml,
  xrayToolbar,
  xrayGrid,
].join('\n');

const catalogSvgs = {};
if (ill) {
  for (const tid of Object.keys(ill.TILE_ILLUSTRATIONS_V62)) {
    catalogSvgs[tid] = {
      map_val: ill.TILE_ILLUSTRATIONS_V62[tid],
      fn_val: ill.getTileIllustrationSvg(tid),
    };
  }
}

console.log(JSON.stringify({
  ok: true,
  has_illustrations_module: Boolean(ill),
  reptile_icon_svg: ill ? ill.REPTILE_ICON_SVG : null,
  reptile_icon_14: ill ? ill.getReptileIconSvg(14) : null,
  reptile_wheel_svg: ill ? ill.getReptileWheelIconSvg(200, 150, 20) : null,
  unknown_tile_svg: ill ? ill.getTileIllustrationSvg('UNKNOWN_ID') : null,
  catalog_svgs: catalogSvgs,
  mode1: {
    medallions: m1Medallions,
    reptile_svgs: m1ReptileSvgs,
    has_bad: badTokenRe.test(m1Toolbar + '\n' + m1Grid),
  },
  mode2: {
    mro_wheel_reptile_svg: m2MroWheelHasReptileSvg,
    mro_medallions: m2MroMedallions,
    mro_has_bad: badTokenRe.test(m2MroToolbar + '\n' + m2MroGrid),
    n6_wheel_reptile_svg: m2N6WheelHasReptileSvg,
    n6_medallions: m2N6Medallions,
    n6_has_bad: badTokenRe.test(m2N6Toolbar + '\n' + m2N6Grid),
  },
  mode3: m3ByPeuple,
  xray: {
    has_bad: badTokenRe.test(xrayToolbar + '\n' + xrayGrid),
    reptile_acc_svg: xrayReptileAccSvg,
  },
  has_snake_emoji_anywhere: combinedAllHtml.includes('\u{1F40D}'),
  has_bad_anywhere: badTokenRe.test(combinedAllHtml),
}));
"""


def _run_harness(load_illustrations: bool = True) -> dict[str, Any]:
    proc = subprocess.run(
        [
            "node",
            "-e",
            _NODE_ILLUSTRATIONS_HARNESS,
            str(STUDIO_INDEX),
            str(STUDIO_DATA),
            str(STUDIO_LIVRET),
            str(ILLUSTRATIONS_JS),
            str(EXPLORER_JS),
            "1" if load_illustrations else "0",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Échec du harnais Node vm Illustrations v6.2 :\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    return dict(json.loads(lines[-1]))


def test_illustrations_files_utf8_lf_and_script_order() -> None:
    """Vérifie encodage UTF-8 sans BOM, LF uniquement et balise <script> avant explorer_v6_2.js."""
    for path in (ILLUSTRATIONS_JS, EXPLORER_JS, EXPLORER_CSS, STUDIO_INDEX):
        assert path.is_file(), f"Fichier attendu manquant : {path}"
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {path.name}"
        assert b"\r\n" not in raw, f"Fin de ligne CRLF interdite dans {path.name}"
        raw.decode("utf-8")

    html = STUDIO_INDEX.read_text(encoding="utf-8")
    ill_tag = '<script src="tile_illustrations_v6_2.js"></script>'
    exp_tag = '<script src="explorer_v6_2.js"></script>'
    assert ill_tag in html, "Balise tile_illustrations_v6_2.js absente de docs/index.html"
    assert exp_tag in html, "Balise explorer_v6_2.js absente de docs/index.html"
    assert html.index(ill_tag) < html.index(exp_tag), (
        "tile_illustrations_v6_2.js doit être chargé avant explorer_v6_2.js"
    )


def test_30_tile_svg_medallions_distinct_and_well_formed() -> None:
    """Vérifie 30 médaillons <svg viewBox='0 0 64 64'> distincts, XML valides et sans ressource externe."""
    payload = _run_harness(load_illustrations=True)
    assert payload["ok"] is True
    assert payload["has_illustrations_module"] is True
    assert payload["unknown_tile_svg"] == ""

    catalog_svgs: dict[str, dict[str, str]] = payload["catalog_svgs"]
    assert set(catalog_svgs.keys()) == set(EXPECTED_TILE_IDS)
    assert len(catalog_svgs) == 30

    raw_svgs: set[str] = set()
    inner_artworks: set[str] = set()
    for tile_id in EXPECTED_TILE_IDS:
        entry = catalog_svgs[tile_id]
        svg = entry["fn_val"]
        assert svg == entry["map_val"], f"Divergence map vs getter sur {tile_id}"
        assert svg.startswith("<svg") and svg.endswith("</svg>"), f"SVG mal borné sur {tile_id}"
        assert 'viewBox="0 0 64 64"' in svg, f"viewBox 0 0 64 64 manquant sur {tile_id}"
        assert "NaN" not in svg and "undefined" not in svg
        assert "<script" not in svg.lower() and "<image" not in svg.lower()
        assert "xlink:href" not in svg.lower() and "url(http" not in svg.lower()

        # Validation XML stricte
        root = ET.fromstring(svg)
        assert root.attrib.get("viewBox") == "0 0 64 64"
        assert len(list(root)) >= 4, f"Illustration trop pauvre sur {tile_id}"

        raw_svgs.add(svg)
        # Normaliser la balise d'ouverture pour garantir 30 dessins géométriques distincts
        inner = re.sub(r"^<svg[^>]*>", "", svg)
        inner_artworks.add(inner)

    assert len(raw_svgs) == 30, "Les 30 médaillons SVG doivent être tous différents"
    assert len(inner_artworks) == 30, "Les 30 dessins internes SVG doivent être tous distincts"

    # Validation de la mini-icône Reptile SVG
    reptile_svg: str = payload["reptile_icon_svg"]
    assert reptile_svg == payload["reptile_icon_14"]
    assert 'viewBox="0 0 24 24"' in reptile_svg
    assert 'width="14"' in reptile_svg and 'height="14"' in reptile_svg
    assert 'data-peuple-icon="R"' in reptile_svg
    assert SNAKE_EMOJI not in reptile_svg
    rep_root = ET.fromstring(reptile_svg)
    assert rep_root.attrib.get("viewBox") == "0 0 24 24"

    # Validation du repli SVG dans la roue des 197 assises
    wheel_svg: str = payload["reptile_wheel_svg"]
    assert 'viewBox="0 0 24 24"' in wheel_svg
    assert 'data-peuple-icon="R"' in wheel_svg
    ET.fromstring(wheel_svg)


def test_explorer_renders_medallions_and_reptile_svg_in_all_3_modes() -> None:
    """Vérifie les 30 médaillons, la mini-icône Reptile SVG et l'absence de 🐍/NaN/undefined."""
    payload = _run_harness(load_illustrations=True)
    assert payload["ok"] is True
    assert payload["has_bad_anywhere"] is False
    assert payload["has_snake_emoji_anywhere"] is False, (
        "L'ancien émoji serpent ne doit plus apparaître dans l'Explorateur sur le Peuple R"
    )

    # Mode 1 : 15 lisières (30 tuiles)
    m1 = payload["mode1"]
    assert m1["has_bad"] is False
    assert len(m1["medallions"]) == 30
    assert set(m1["medallions"]) == set(EXPECTED_TILE_IDS)
    assert m1["reptile_svgs"] >= 15

    # Mode 2 : Table & Roue des 197 Assises
    m2 = payload["mode2"]
    assert m2["mro_has_bad"] is False
    assert m2["mro_wheel_reptile_svg"] is True
    assert len(m2["mro_medallions"]) == 6
    assert m2["n6_has_bad"] is False
    assert m2["n6_wheel_reptile_svg"] is True
    assert len(m2["n6_medallions"]) == 12

    # Mode 3 : Grammaires par Peuple (3+3) sur les 6 onglets
    m3: dict[str, dict[str, Any]] = payload["mode3"]
    for p_code in ("H", "E", "M", "R", "O", "I"):
        assert m3[p_code]["has_bad"] is False
        assert m3[p_code]["medallions"] == 10
        assert m3[p_code]["reptile_svgs"] >= 1
    # Sur l'onglet R : bouton d'onglet + bannière + 10 pilules de cartes = au moins 12 icônes R
    assert m3["R"]["reptile_svgs"] >= 12

    # Rayons X
    assert payload["xray"]["has_bad"] is False
    assert payload["xray"]["reptile_acc_svg"] is True


def test_explorer_graceful_fallback_without_illustrations_module() -> None:
    """Garantit la rétrocompatibilité si AmazoniaTileIllustrationsV62 n'est pas chargé."""
    payload = _run_harness(load_illustrations=False)
    assert payload["ok"] is True
    assert payload["has_illustrations_module"] is False
    assert payload["has_bad_anywhere"] is False
    assert payload["has_snake_emoji_anywhere"] is False
    assert payload["mode1"]["medallions"] == []
    assert payload["mode1"]["reptile_svgs"] >= 15
    assert payload["mode2"]["mro_wheel_reptile_svg"] is True
    assert payload["mode2"]["n6_wheel_reptile_svg"] is True
