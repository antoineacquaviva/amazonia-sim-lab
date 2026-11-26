"""Tests headless Node vm & pont Python dédiés à l'Explorateur Bi-Composant & Atelier Draft v6.3.1.

Vérifie sans dépendance npm :
1. Encodage UTF-8 sans BOM, fins LF, compilation `docs/data/panels_v6_3_data.js` (y compris
   embarquement optionnel de `author_workspace_v6_3.json` & filtrage dans `audit_panels_directory`),
   et validation syntaxique stricte via `new vm.Script()`.
2. Pilier A : rendu Bi-Composant (Mini-Tuile + Grande Carte), silhouettes Action / Loi passive / Twist 2K3,
   Guide des 32 pictogrammes, absence totale de plomberie technique (`PIC_*`, `ICONE_*`,
   `engine_sync_status`, `A_CODER`, `transition_python`) et zéro compteur C02 en lecture primaire.
3. Pilier B : Flux Synergique (Plancher solo vs Amplificateurs /64, Jumelle Y>X, Qui m'alimente /
   Qui j'alimente) et filtre 1-clic Ressource / Icône (Producteurs <-> Consommateurs).
4. Pilier C : Bandeau permanent (`Panel 1|2|3`, `Mon Canon`, `Archive v6.2`), Radar de santé
   temps réel sur les 197 assises (géométrie 2 triangles orientés `2K3`, Lois ≤ 5 & ≤ 2/assise,
   Éveil (i)+(ii), Sommeil E sans H, Enracinements 3–5, Autonomie A=0), Vue 1 Duel `P1|P2|P3`,
   Vue 2 Simulateur de Table `3..6` Peuples et Vue 3 Tableau de bord Atelier.
5. Pilier D : Annotations Draft (`localStorage` + réimport), tiroir Édition/Hybridation (raccourcis
   inter-panels + restauration), Brief Markdown Gemini ciblé (4 périmètres + compteur de mots)
   et exports Antigravity (`author_workspace_v6_3.json` + `tiles_canon_v6_3.json` candidat validé
   en strict par `validate_tiles_canon_v6_3` et `audit_tiles_catalog_197`).
"""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any

from scripts.audit_197 import audit_panels_directory, audit_tiles_catalog_197
from scripts.build_studio_artifacts import compile_panels_v6_3_js
from scripts.tiles_v6_3_schema import PANELS_DIR, validate_tiles_canon_v6_3

ROOT = Path(__file__).resolve().parent.parent
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"
ILLUSTRATIONS_JS = ROOT / "docs" / "tile_illustrations_v6_2.js"
EXPLORER_V6_2_JS = ROOT / "docs" / "explorer_v6_2.js"
PANELS_V6_3_JS = ROOT / "docs" / "data" / "panels_v6_3_data.js"
EXPLORER_V6_3_JS = ROOT / "docs" / "explorer_v6_3.js"
EXPLORER_V6_3_CSS = ROOT / "docs" / "explorer_v6_3.css"


_NODE_V63_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath, illPath, exp62Path, panels63Path, exp63Path] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');
const illJs = fs.readFileSync(illPath, 'utf8');
const exp62Js = fs.readFileSync(exp62Path, 'utf8');
const panels63Js = fs.readFileSync(panels63Path, 'utf8');
const exp63Js = fs.readFileSync(exp63Path, 'utf8');

// Validation syntaxique stricte via new vm.Script()
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

const badTokenRe = /\b(?:NaN|undefined)\b/;
function stripTags(htmlStr) {
  return String(htmlStr || '')
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<[^>]+>/g, ' ');
}

sandbox.refreshAllUI();

// 1. Vérification 197 assises & Radar sur les 3 panels
const all197 = exp.enumerateAll197Assises();
const countsByN = { 3: 0, 4: 0, 5: 0, 6: 0 };
for (const a of all197) countsByN[a.n]++;

const panelRadars = {};
const panelRenders = {};
for (const pid of ['panel_1', 'panel_2', 'panel_3']) {
  exp.setSource(pid);
  const r = exp.computeHealthRadar('active_source');
  const tb = getEl('explorer-v6-3-toolbar').innerHTML;
  const gd = getEl('catalogue-grid').innerHTML;
  const visibleProse = stripTags(tb + '\n' + gd);
  panelRadars[pid] = {
    elected: r.electedCount,
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
    synergyStripCount: (gd.match(/data-synergy-strip="/g) || []).length,
    loiCards: (gd.match(/data-nature="LOI_PASSIVE"/g) || []).length,
    twistCards: (gd.match(/data-twist="true"/g) || []).length,
    hasBad: badTokenRe.test(tb + '\n' + gd),
    hasSnake: (tb + gd).includes('\u{1F40D}'),
    proseSampleHasRawPic: /\bPIC_[A-Z0-9_]+\b/.test(visibleProse),
    proseSampleHasRawIcon: /\bICONE_[A-Z_]+\b/.test(visibleProse),
    proseSampleHasPlumbing: /\b(?:engine_sync_status|DESIGNED_V6_3|PASSE_1_CREATIF|A_CODER|transition_python|mots_par_face)\b/.test(visibleProse),
  };
}

// 2. Guide des 32 pictogrammes
exp.setSource('panel_1');
exp.openPictoGuide();
const guideHtml = getEl('catalogue-grid').innerHTML;
const guideCardsCount = (guideHtml.match(/class="x3-picto-guide-card"/g) || []).length;
const guideHasBad = badTokenRe.test(guideHtml);
exp.setPictoFilter('PIC_CROC');
const crocPictoSlots = exp.getFilteredSlotIds();
exp.resetFilters();

const panelsV63 = vm.runInContext('PANELS_V6_3', sandbox);

// 3. Filtre Ressource / Icône 1 clic (Producteurs <-> Consommateurs)
exp.focusResource('BLEU');
const bleuIndex = exp.computeResourceIndex('BLEU', panelsV63.panel_1.tuiles_ciblees);
const bleuHtml = getEl('catalogue-grid').innerHTML;
const bleuHasPanel = bleuHtml.includes('data-resource-focus="BLEU"') && bleuHtml.includes('Producteurs') && bleuHtml.includes('Consommateurs');
exp.focusResource('ICONE_PIEGEAGE');
const piegIndex = exp.computeResourceIndex('ICONE_PIEGEAGE', panelsV63.panel_1.tuiles_ciblees);
exp.clearResourceFocus();

// 4. Vue 1b — Duel Panel 1 | Panel 2 | Panel 3
exp.openDuelForSlot('G1');
const duelHtml = getEl('catalogue-grid').innerHTML;
const duelCols = Array.from(duelHtml.matchAll(/data-duel-col="([^"]+)"/g)).map(m => m[1]);
const duelHasBad = badTokenRe.test(duelHtml);

// 5. Vue 2 — Simulateur de Table 3 à 6 Peuples
exp.setView('simulator');
const simResults = {};
for (const preset of ['N3-HEI', 'N3-ERO', 'N3-MRO', 'N6-HEMROI']) {
  exp.setSimPreset(preset);
  const s = exp.analyzeTableSimulation(exp.getState().simPeuples, 'panel_1');
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
  };
}

// 6. Pilier D — Élection, Annotations, Hybridation, Persistance, Archive v6.2, Exports Gemini & Antigravity
exp.setView('dashboard');
exp.fillUnelectedFrom('panel_1');
const canonRadarFullP1 = exp.computeHealthRadar('canon');

// Remplacer G2 par panel_2 pour tester détection 2K3 cassée quand on mixe deux panels
exp.electSlot('G2', 'panel_2');
const canonRadarMixedTwist = exp.computeHealthRadar('canon');
// Revenir à panel_1 sur G2
exp.electSlot('G2', 'panel_1');

// Annotations sur G1 & R4
exp.setSlotStatus('G1', 'A_HYBRIDER');
exp.setSlotRating('G1', 5);
exp.toggleSlotFavorite('G1');
exp.setSlotCommentLive('G1', 'Combiner Face 1 de P1 avec Face 2 de P2');
exp.setSlotStatus('R4', 'HESITATION');
exp.setSlotCommentLive('R4', 'Arbitrer le Twist H>R entre P1 et P3');

const dashHtml = getEl('catalogue-grid').innerHTML;
const dashHasArbitrage = dashHtml.includes('data-arbitrage-list="true"') && dashHtml.includes('G1') && dashHtml.includes('R4');
const dashHasBad = badTokenRe.test(dashHtml);

// Éditeur & Hybridation sur G1 : importer Face 2 depuis panel_2 et sauver
exp.openEditor('G1', 'panel_1');
exp.importEditorFromPanel('panel_2', 'face_2');
exp.updateEditorField('carte_joueur.titre_complet', 'Le Jaguar hybride des rives');
exp.saveEditorToCanon();

exp.setSource('canon');
exp.setView('explorer');
exp.setExplorerSubView('cards');
const canonGridHtml = getEl('catalogue-grid').innerHTML;
const canonShowsModifiedBadge = canonGridHtml.includes('Modifié par l’auteur') && canonGridHtml.includes('Le Jaguar hybride des rives');

// Archive v6.2 en lecture seule
exp.setSource('archive_v6_2');
const archiveHtml = getEl('catalogue-grid').innerHTML;
const archiveOk = archiveHtml.includes('Archive v6.2') && !badTokenRe.test(archiveHtml) && (archiveHtml.match(/data-component="grande-carte"/g) || []).length === 30;
exp.setSource('canon');

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

// Export & ré-import Workspace Antigravity
const exportedWorkspace = exp.buildAuthorWorkspaceExport();
const storedRaw = storageMap['amazonia_atelier_v6_3_workspace_v1'] || null;
// Restaurer G1 à l'original P1 avant export candidat strict
exp.restoreOriginalSlot('G1');
const candidateCanonStrict = exp.buildCandidateCanonV63('panel_1');

// Tester ré-import du workspace sauvegardé (doit retrouver la surcharge G1)
exp.importWorkspaceObject(exportedWorkspace);
const reimportedG1Modified = exp.getWorkspace().slots.G1.is_modified;
const reimportedG1Title = exp.getWorkspace().slots.G1.custom_tile.carte_joueur.titre_complet;

console.log(JSON.stringify({
  ok: true,
  total_assises: all197.length,
  counts_by_n: countsByN,
  panel_radars: panelRadars,
  panel_renders: panelRenders,
  picto_guide: {
    cards_count: guideCardsCount,
    has_bad: guideHasBad,
    croc_slots_count: crocPictoSlots.length,
  },
  resource_focus: {
    bleu_has_panel: bleuHasPanel,
    bleu_producers: bleuIndex.producers.length,
    piegeage_producers: piegIndex.producers.length,
    piegeage_guardians: piegIndex.consumersIcon.length,
  },
  duel: {
    cols: duelCols,
    has_bad: duelHasBad,
  },
  simulator: simResults,
  dashboard: {
    has_arbitrage: dashHasArbitrage,
    has_bad: dashHasBad,
  },
  canon_radar_full_p1: {
    elected: canonRadarFullP1.electedCount,
    twists2K3: Boolean(canonRadarFullP1.twists.triangles2K3),
    loisMax: canonRadarFullP1.lois.maxPerAssise,
    eveil: canonRadarFullP1.eveil.status,
    sommeil: canonRadarFullP1.sommeil.status,
    enrac: canonRadarFullP1.enrac.status,
    a0: canonRadarFullP1.a0.status,
  },
  canon_radar_mixed_twist_2k3: Boolean(canonRadarMixedTwist.twists.triangles2K3),
  canon_shows_modified_badge: canonShowsModifiedBadge,
  archive_ok: archiveOk,
  gemini_briefs: geminiBriefs,
  workspace_saved_in_localstorage: Boolean(storedRaw),
  workspace_schema: exportedWorkspace.schema_version,
  workspace_reimported_g1_modified: reimportedG1Modified,
  workspace_reimported_g1_title: reimportedG1Title,
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
        f"Échec du harnais Node vm Explorateur v6.3.1 :\n"
        f"STDOUT:\n{proc.stdout}\nSTDERR:\n{proc.stderr}"
    )
    lines = [line for line in proc.stdout.strip().splitlines() if line.strip()]
    return dict(json.loads(lines[-1]))


def test_v63_studio_files_utf8_lf_and_index_wiring() -> None:
    """Vérifie UTF-8 sans BOM, fins LF et branchement propre dans docs/index.html."""
    for path in (PANELS_V6_3_JS, EXPLORER_V6_3_JS, EXPLORER_V6_3_CSS, STUDIO_INDEX):
        assert path.is_file(), f"Fichier attendu manquant : {path}"
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {path.name}"
        assert b"\r\n" not in raw, f"CRLF interdit dans {path.name}"
        raw.decode("utf-8")

    html = STUDIO_INDEX.read_text(encoding="utf-8")
    assert 'href="explorer_v6_3.css"' in html
    assert 'id="explorer-v6-3-toolbar"' in html
    panels_tag = '<script src="data/panels_v6_3_data.js"></script>'
    exp_tag = '<script src="explorer_v6_3.js"></script>'
    assert panels_tag in html
    assert exp_tag in html
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


def test_explorer_v63_bicomponent_radar_simulator_draft_and_strict_candidate_export() -> None:
    """Valide les 4 piliers UX/UI v6.3.1 et la conformité Python stricte du Canon candidat exporté."""
    payload = _run_v63_harness()
    assert payload["ok"] is True

    # 1. Modèle exact des 197 assises
    assert payload["total_assises"] == 197
    assert payload["counts_by_n"] == {"3": 20, "4": 45, "5": 72, "6": 60}

    # 2. Pilier A & C : Rendu Bi-Composant + Zéro plomberie + Radar 100 % OK sur les 3 panels
    for pid in ("panel_1", "panel_2", "panel_3"):
        rad = payload["panel_radars"][pid]
        assert rad["elected"] == 30
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
        assert rnd["synergyStripCount"] == 30
        assert rnd["loiCards"] == rad["loisCount"]
        assert rnd["twistCards"] == 6
        assert rnd["hasBad"] is False
        assert rnd["hasSnake"] is False
        assert rnd["proseSampleHasRawPic"] is False, f"Code brut PIC_* visible sur {pid}"
        assert rnd["proseSampleHasRawIcon"] is False, f"Code brut ICONE_* visible sur {pid}"
        assert rnd["proseSampleHasPlumbing"] is False, f"Plomberie technique visible sur {pid}"

    # 3. Guide des 32 pictogrammes
    pg = payload["picto_guide"]
    assert pg["cards_count"] == 32
    assert pg["has_bad"] is False
    assert pg["croc_slots_count"] >= 1

    # 4. Pilier B : Focus Ressource / Icône (Producteurs <-> Consommateurs)
    rf = payload["resource_focus"]
    assert rf["bleu_has_panel"] is True
    assert rf["bleu_producers"] >= 1
    assert rf["piegeage_producers"] >= 1
    assert rf["piegeage_guardians"] >= 1

    # 5. Vue 1b : Duel P1 | P2 | P3
    assert payload["duel"]["cols"] == ["panel_1", "panel_2", "panel_3"]
    assert payload["duel"]["has_bad"] is False

    # 6. Vue 2 : Simulateur de Table 3..6 Peuples
    sim = payload["simulator"]
    assert sim["N3-HEI"]["tilesCount"] == 6
    assert sim["N3-HEI"]["modules"] == {"gardiens": False, "reves": True, "essaim": True}
    assert sim["N3-HEI"]["accessoriesCount"] == 3
    assert sim["N3-HEI"]["hasWheelSvg"] is True
    assert sim["N3-HEI"]["hasBad"] is False

    assert sim["N3-ERO"]["tilesCount"] == 6
    assert sim["N3-ERO"]["hasBad"] is False

    assert sim["N3-MRO"]["tilesCount"] == 6
    assert sim["N3-MRO"]["modules"] == {"gardiens": True, "reves": False, "essaim": False}

    assert sim["N6-HEMROI"]["tilesCount"] == 12
    assert sim["N6-HEMROI"]["accessoriesCount"] == 6
    assert sim["N6-HEMROI"]["chainsCount"] >= 1
    assert sim["N6-HEMROI"]["hasBad"] is False

    # 7. Vue 3 : Tableau de bord & Radar Mon Canon (y compris détection 2K3 cassée en mixant)
    assert payload["dashboard"]["has_arbitrage"] is True
    assert payload["dashboard"]["has_bad"] is False
    assert payload["canon_radar_full_p1"]["elected"] == 30
    assert payload["canon_radar_full_p1"]["twists2K3"] is True
    assert payload["canon_radar_mixed_twist_2k3"] is False
    assert payload["canon_shows_modified_badge"] is True
    assert payload["archive_ok"] is True

    # 8. Pilier D : Briefs Gemini (4 périmètres, zéro code brut) & Persistance Workspace
    gb = payload["gemini_briefs"]
    for sc in ("to_arbitrate", "active_context", "notes_and_edits", "canon_summary"):
        assert gb[sc]["words"] > 20
        assert gb[sc]["hasRawPic"] is False
        assert gb[sc]["hasPlumbing"] is False
    assert gb["to_arbitrate"]["tileCount"] == 2
    assert gb["to_arbitrate"]["containsG1Note"] is True
    assert gb["notes_and_edits"]["containsG1Note"] is True

    assert payload["workspace_saved_in_localstorage"] is True
    assert payload["workspace_schema"] == "6.3.1-workspace"
    assert payload["workspace_reimported_g1_modified"] is True
    assert payload["workspace_reimported_g1_title"] == "Le Jaguar hybride des rives"

    # 9. Pont Antigravity : le JSON candidat exporté depuis le navigateur passe strict Python + audit_197 !
    cand = payload["candidate_canon_strict"]
    schema_errs = validate_tiles_canon_v6_3(cand, strict=True)
    assert schema_errs == [], f"Export tiles_canon_v6_3.json invalide : {schema_errs}"
    audit_rep = audit_tiles_catalog_197(cand, allow_draft=False)
    assert audit_rep["verdict_global"] == "OK", f"Audit 197 échoué sur export candidat : {audit_rep['errors']}"
