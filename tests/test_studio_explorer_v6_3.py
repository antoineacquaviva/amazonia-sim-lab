"""Tests headless Node vm & pont Python dédiés à l'Atelier d'Arbitrage Bi-Composant v6.3.2.

Vérifie sans dépendance npm :
1. Encodage UTF-8 sans BOM, fins LF, compilation `docs/data/panels_v6_3_data.js` (y compris
   embarquement optionnel de `author_workspace_v6_3.json` & filtrage dans `audit_panels_directory`),
   et validation syntaxique stricte via `new vm.Script()`.
2. Ergonomie recentrée v6.3.2 :
   - Entrée par défaut en Duel `P1 | P2 | P3` sur 1 emplacement (`G1`), tous tiroirs fermés et
     détails (`<details class="x3-details-fold">`) repliés par défaut ;
   - Repli automatique du bandeau global Studio au clic sur l'onglet Catalogue (`switchTab('catalogue')`)
     et restauration de la préférence utilisateur sur les autres onglets ;
   - Trio d'annotation léger (`★ Garder`, `🤔 À revoir`, `Note` temps réel), navigation clavier
     `ArrowRight`/`ArrowLeft`/`Escape` et saut `Prochain à trancher` ;
   - Tiroirs à la demande : Index compact 30 emplacements, Radar Santé consolidé (197 assises + `2K3`)
     et Parcourir / Filtrer (Listes `Panel 1|2|3`, `Mon Canon`, `Archive v6.2`).
3. Rendu Bi-Composant (Mini-Tuile + Grande Carte), Guide des 32 pictogrammes, focus 1-clic
   Ressource/Icône (`Producteurs ⇄ Consommateurs`), absence totale de plomberie technique
   (`PIC_*`, `ICONE_*`, `engine_sync_status`, `A_CODER`, `transition_python`) et zéro compteur `C02`.
4. Simulateur de Table `3..6` Peuples, Éditeur/Hybrideur, Briefs Markdown Gemini ciblés (4 périmètres)
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

// 0. État initial v6.3.2 : Duel P1|P2|P3 par défaut sur G1, tiroirs fermés, repli bandeau auto
const initTb = getEl('explorer-v6-3-toolbar').innerHTML;
const initGd = getEl('catalogue-grid').innerHTML;
const initState = exp.getState();
const initCheck = {
  version: exp.VERSION,
  mode: initState.mode,
  slot: initState.currentSlotId,
  activeDrawer: initState.activeDrawer,
  hasSingleHealthPill: initTb.includes('data-health-pill="true"'),
  hasProgressPill: initTb.includes('data-progress-pill="true"'),
  hasArbitrateSlotG1: initGd.includes('data-arbitrate-slot="G1"'),
  duelCols: Array.from(initGd.matchAll(/data-duel-col="([^"]+)"/g)).map(m => m[1]),
  detailsFoldClosed: initGd.includes('<details class="x3-details-fold"') && !initGd.includes('<details class="x3-details-fold" open'),
  hasTrioBar: initGd.includes('data-trio-bar="G1"') && initGd.includes('data-review-btn="true"'),
  hasBad: badTokenRe.test(initTb + '\n' + initGd),
  hasSnake: (initTb + initGd).includes('\u{1F40D}'),
};

// Repli automatique du bandeau global Studio sur switchTab('catalogue') puis restauration sur 'livret'
sandbox.switchTab('catalogue');
const headerCollapsedOnCatalogue = getEl('header-collapsible-body').classList.contains('hidden');
const headerBtnOnCatalogue = getEl('btn-toggle-header').textContent;
sandbox.switchTab('livret');
const headerRestoredOnLivret = !getEl('header-collapsible-body').classList.contains('hidden');
sandbox.switchTab('catalogue');

// Navigation clavier : ArrowRight -> G2, ArrowLeft -> G1, Escape ferme tiroir
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

// 1. Modèle 197 assises & Rendu Bi-Composant + Zéro plomberie sur les 3 panels en Vue Liste
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

// 2. Guide des 32 pictogrammes + filtre picto
exp.openListView('panel_1');
exp.openPictoGuide();
const guideHtml = getEl('catalogue-grid').innerHTML;
const guideCardsCount = (guideHtml.match(/class="x3-picto-guide-card"/g) || []).length;
const guideHasBad = badTokenRe.test(guideHtml);
exp.setPictoFilter('PIC_CROC');
const crocPictoSlots = exp.getFilteredSlotIds();
exp.resetFilters();

const panelsV63 = vm.runInContext('PANELS_V6_3', sandbox);

// 3. Filtre Ressource / Icône 1 clic (Producteurs <-> Consommateurs)
exp.focusResource('BLEU', 'panel_1');
const bleuIndex = exp.computeResourceIndex('BLEU', panelsV63.panel_1.tuiles_ciblees);
const bleuHtml = getEl('catalogue-grid').innerHTML;
const bleuHasPanel = bleuHtml.includes('data-resource-focus="BLEU"') && bleuHtml.includes('Producteurs') && bleuHtml.includes('Consommateurs');
exp.focusResource('ICONE_PIEGEAGE', 'panel_1');
const piegIndex = exp.computeResourceIndex('ICONE_PIEGEAGE', panelsV63.panel_1.tuiles_ciblees);
exp.clearResourceFocus();

// 4. Écran 2 — Simulateur de Table 3 à 6 Peuples
exp.setMode('simulator');
exp.setSimSource('panel_1');
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

// 5. Trio d'annotation, Index 30 emplacements, Radar mixte, Hybridation, Archive v6.2 & Exports
exp.setMode('arbitrate');
exp.goToSlot('G1');
exp.keepSlot('G1', 'panel_1');
const nextPendingAfterG1 = exp.goToNextPending();
exp.goToSlot('G1');

// Ouvrir Index compact 30 emplacements et pré-remplir le reste depuis panel_1
exp.toggleDrawer('index30');
const indexDrawerHtml = getEl('explorer-v6-3-toolbar').innerHTML;
const indexDrawerSlotsCount = (indexDrawerHtml.match(/data-index-slot="/g) || []).length;
exp.fillUnelectedFrom('panel_1');
const canonRadarFullP1 = exp.computeHealthRadar('canon');

// Remplacer G2 par panel_2 pour tester détection 2K3 cassée quand on mixe deux panels
exp.keepSlot('G2', 'panel_2');
const canonRadarMixedTwist = exp.computeHealthRadar('canon');
// Revenir à panel_1 sur G2
exp.keepSlot('G2', 'panel_1');

// Trio d'annotation : À revoir + Note sur G1 & R4
exp.toggleSlotReview('G1');
exp.setSlotCommentLive('G1', 'Combiner Face 1 de P1 avec Face 2 de P2');
exp.toggleSlotReview('R4');
exp.setSlotCommentLive('R4', 'Arbitrer le Twist H>R entre P1 et P3');

// Éditeur & Hybridation sur G1 : importer Face 2 depuis panel_2 et sauver
exp.openEditor('G1', 'panel_1');
exp.importEditorFromPanel('panel_2', 'face_2');
exp.updateEditorField('carte_joueur.titre_complet', 'Le Jaguar hybride des rives');
exp.saveEditorToCanon();

exp.openListView('canon');
const canonListHtml = getEl('catalogue-grid').innerHTML;
const canonShowsModifiedBadge = canonListHtml.includes('Modifié') && canonListHtml.includes('Le Jaguar hybride des rives');

// Archive v6.2 en lecture seule
exp.openListView('archive_v6_2');
const archiveHtml = getEl('catalogue-grid').innerHTML;
const archiveOk = archiveHtml.includes('Archive v6.2') && !badTokenRe.test(archiveHtml) && (archiveHtml.match(/data-component="grande-carte"/g) || []).length === 30;
exp.setMode('arbitrate');

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
  init_check: initCheck,
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
  simulator: simResults,
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
        f"Échec du harnais Node vm Explorateur v6.3.2 :\n"
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


def test_explorer_v63_streamlined_atelier_radar_simulator_and_strict_export() -> None:
    """Valide l'Atelier épuré v6.3.2, le Radar 197 assises et la conformité Python stricte du Canon candidat."""
    payload = _run_v63_harness()
    assert payload["ok"] is True

    # 0. Entrée par défaut = Duel P1|P2|P3 sur G1, tiroirs fermés, repli bandeau auto
    ic = payload["init_check"]
    assert ic["version"] == "6.3.2"
    assert ic["mode"] == "arbitrate"
    assert ic["slot"] == "G1"
    assert ic["activeDrawer"] is None
    assert ic["hasSingleHealthPill"] is True
    assert ic["hasProgressPill"] is True
    assert ic["hasArbitrateSlotG1"] is True
    assert ic["duelCols"] == ["panel_1", "panel_2", "panel_3"]
    assert ic["detailsFoldClosed"] is True
    assert ic["hasTrioBar"] is True
    assert ic["hasBad"] is False
    assert ic["hasSnake"] is False

    hac = payload["header_auto_collapse"]
    assert hac["collapsed_on_catalogue"] is True
    assert "Afficher le bandeau" in hac["btn_on_catalogue"]
    assert hac["restored_on_livret"] is True

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

    # 1. Modèle exact des 197 assises
    assert payload["total_assises"] == 197
    assert payload["counts_by_n"] == {"3": 20, "4": 45, "5": 72, "6": 60}

    # 2. Rendu Bi-Composant + Zéro plomberie + Radar 100 % OK sur les 3 panels
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

    # 3. Guide des 32 pictogrammes
    pg = payload["picto_guide"]
    assert pg["cards_count"] == 32
    assert pg["has_bad"] is False
    assert pg["croc_slots_count"] >= 1

    # 4. Focus Ressource / Icône (Producteurs <-> Consommateurs)
    rf = payload["resource_focus"]
    assert rf["bleu_has_panel"] is True
    assert rf["bleu_producers"] >= 1
    assert rf["piegeage_producers"] >= 1
    assert rf["piegeage_guardians"] >= 1

    # 5. Écran 2 : Simulateur de Table 3..6 Peuples
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

    # 6. Radar Mon Canon (y compris détection 2K3 cassée en mixant) + Archive v6.2
    assert payload["canon_radar_full_p1"]["elected"] == 30
    assert payload["canon_radar_full_p1"]["overallStatus"] == "ok"
    assert payload["canon_radar_full_p1"]["twists2K3"] is True
    assert payload["canon_radar_mixed_twist_2k3"] is False
    assert payload["canon_shows_modified_badge"] is True
    assert payload["archive_ok"] is True

    # 7. Briefs Gemini (4 périmètres, zéro code brut) & Persistance Workspace
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

    # 8. Pont Antigravity : le JSON candidat exporté depuis le navigateur passe strict Python + audit_197 !
    cand = payload["candidate_canon_strict"]
    schema_errs = validate_tiles_canon_v6_3(cand, strict=True)
    assert schema_errs == [], f"Export tiles_canon_v6_3.json invalide : {schema_errs}"
    audit_rep = audit_tiles_catalog_197(cand, allow_draft=False)
    assert audit_rep["verdict_global"] == "OK", f"Audit 197 échoué sur export candidat : {audit_rep['errors']}"
