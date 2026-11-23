"""Tests du Lot 2 : statistiques appariées, IC95 groupés par table, CVaR directe, A/B tuiles et panel B0..B2_OPEN."""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path
from typing import Any

import pytest

import campaigns.digest_builder as db_mod
import run_campaign as rc_mod
from bots.heuristic_engine import play_game_b2, play_game_b2_open
from campaigns.digest_builder import (
    AUTHOR_REPORTING_INSTRUCTIONS,
    GEMINI_EDITORIAL_STYLE_INSTRUCTIONS,
)
from campaigns.stats_tools import (
    assess_sign_stability,
    circle_dispersion_summary,
    cvar_exact_values,
    cvar_with_bootstrap_ci95,
    estimate_required_pairs,
    holm_bonferroni_adjust,
    paired_diff_cluster_ci95,
    sequential_ci_elimination,
)
from campaigns.worker_main import (
    CALIBRATION_BOT_PANEL,
    resolve_manifest_plan,
    run_campaign_manifest,
)
from engine.state import GameConfig, GameState
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb, run_pilot_sample_size_estimation

ROOT = Path(__file__).resolve().parent.parent
STUDIO_INDEX = ROOT / "docs" / "index.html"
STUDIO_DATA = ROOT / "docs" / "data" / "amazonia_data_v6_0.js"
STUDIO_LIVRET = ROOT / "docs" / "data" / "livret_v6_0.js"


# ---------------------------------------------------------------------------
# 1. Primitives statistiques (campaigns/stats_tools.py)
# ---------------------------------------------------------------------------


def test_paired_diff_cluster_ci95_single_and_multi_cluster() -> None:
    single = paired_diff_cluster_ci95({"T1": [0.05, 0.03, 0.04]})
    assert single["estimable"] is False
    assert single["status"] == "non_estimable_single_table"
    assert single["ci95_low"] is None and single["ci95_high"] is None
    assert single["mean_delta"] == pytest.approx(0.04, abs=1e-5)

    multi = paired_diff_cluster_ci95(
        {
            "T1": [0.04, 0.06],
            "T2": [0.05, 0.07],
            "T3": [0.03, 0.05],
            "T4": [0.06, 0.04],
        }
    )
    assert multi["estimable"] is True
    assert multi["n_tables"] == 4
    assert multi["n_pairs"] == 8
    assert multi["mean_delta"] == pytest.approx(0.05, abs=1e-5)
    assert multi["ci95_low"] > 0.0
    assert multi["ci95_low"] < multi["mean_delta"] < multi["ci95_high"]
    assert multi["p_value"] < 0.01


def test_circle_dispersion_weighted_mean_and_single_circle_non_estimable() -> None:
    # 1 seul cercle : incertitude explicitement non estimable (jamais d'intervalle dégénéré [m, m])
    one = circle_dispersion_summary([0.4472], [120])
    assert one["estimable"] is False
    assert one["status"] == "non_estimable_single_circle"
    assert one["ci95_low"] is None and one["ci95_high"] is None
    assert "non estimable" in str(one.get("uncertainty_note", "")).lower()

    # Pondération par effectifs : 6 parties à 0.80 et 120 parties à 0.50 -> moyenne exacte pondérée
    weighted = circle_dispersion_summary([0.80, 0.50], [6, 120])
    expected_mean = (6 * 0.80 + 120 * 0.50) / 126.0
    assert weighted["estimable"] is True
    assert weighted["mean_ratio_arbres"] == pytest.approx(expected_mean, abs=1e-4)
    assert weighted["ci95_low"] < weighted["mean_ratio_arbres"] < weighted["ci95_high"]


def test_cvar_uniform_alpha_and_deterministic_bootstrap() -> None:
    # Distribution uniforme sur [0.1, 0.2, ..., 1.0] (10 parties) : les 20 % les plus bas sont [0.1, 0.2] -> 0.15
    vals_10 = [i / 10.0 for i in range(1, 11)]
    assert cvar_exact_values(vals_10, alpha=0.20) == pytest.approx(0.15, abs=1e-6)

    # 6 parties : alpha*6 = 1.2 -> exactement (1.0 * v0 + 0.2 * v1) / 1.2 (pas d'effet de seuil 2/6 = 33 %!)
    vals_6 = [0.20, 0.50, 0.60, 0.70, 0.80, 0.90]
    expected_6 = (0.20 + 0.2 * 0.50) / 1.2
    assert cvar_exact_values(vals_6, alpha=0.20) == pytest.approx(expected_6, abs=1e-6)

    # Bootstrap déterministe
    clusters = [{2000: 2, 5000: 3}, {3000: 2, 6000: 3}, {2500: 2, 5500: 3}, {1500: 2, 7000: 3}]
    b1 = cvar_with_bootstrap_ci95(clusters, alpha=0.20, n_boot=200, seed=42)
    b2 = cvar_with_bootstrap_ci95(clusters, alpha=0.20, n_boot=200, seed=42)
    assert b1 == b2
    assert b1["estimable"] is True
    assert b1["bootstrap_level"] == "cluster_table"
    assert b1["ci95_low"] <= b1["cvar"] <= b1["ci95_high"]


def test_sample_size_holm_sequential_elimination_and_sign_stability() -> None:
    diffs = [0.01, -0.02, 0.03, 0.00, 0.04, -0.01, 0.02, 0.01, -0.03, 0.02]
    est = estimate_required_pairs(diffs, target_delta=0.01, z=1.96)
    mean_d = sum(diffs) / len(diffs)
    sigma = math.sqrt(sum((x - mean_d) ** 2 for x in diffs) / (len(diffs) - 1))
    assert est["required_pairs_ci95"] == max(10, math.ceil((1.96 * sigma / 0.01) ** 2))

    # Holm-Bonferroni
    holm = holm_bonferroni_adjust([("A", 0.005), ("B", 0.03), ("C", 0.04), ("D", None)], alpha=0.05)
    assert holm["A"]["holm_adjusted_p"] == pytest.approx(0.015, abs=1e-6)
    assert holm["A"]["reject_h0"] is True
    assert holm["B"]["holm_adjusted_p"] == pytest.approx(0.06, abs=1e-6)
    assert holm["B"]["reject_h0"] is False
    assert holm["D"]["holm_adjusted_p"] is None

    # Élimination séquentielle par IC
    elim = sequential_ci_elimination(
        [
            {"id": "best", "mean": 0.72, "ci95_low": 0.70, "ci95_high": 0.74},
            {"id": "close", "mean": 0.69, "ci95_low": 0.67, "ci95_high": 0.71},
            {"id": "dominated", "mean": 0.62, "ci95_low": 0.60, "ci95_high": 0.65},
        ]
    )
    assert elim["retained_ids"] == ["best", "close"]
    assert elim["eliminated_ids"] == ["dominated"]

    # Stabilité du signe B1 / B2 / B2_OPEN
    stable = assess_sign_stability(
        {
            "B1": {"mean_delta": -0.04, "ci95_low": -0.06, "ci95_high": -0.02},
            "B2": {"mean_delta": -0.02, "ci95_low": -0.03, "ci95_high": -0.01},
            "B2_OPEN": {"mean_delta": -0.015, "ci95_low": -0.025, "ci95_high": -0.005},
        }
    )
    assert stable["all_panel_present"] is True
    assert stable["sign_stable"] is True
    assert stable["status"] == "STABLE_NEGATIVE"

    flipped = assess_sign_stability(
        {
            "B1": {"mean_delta": -0.04},
            "B2": {"mean_delta": 0.02},
            "B2_OPEN": {"mean_delta": 0.03},
        }
    )
    assert flipped["sign_stable"] is False
    assert flipped["status"] == "INCONSISTENT_SIGN"


# ---------------------------------------------------------------------------
# 2. Panel de bots (B2_OPEN) & télémétrie d'activations par tuile
# ---------------------------------------------------------------------------


def test_b2_open_ceiling_and_tile_activation_telemetry() -> None:
    cfg = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "I"), exp_seed=20261201, rep_id=7)
    trk_b2 = TelemetryTracker()
    res_b2 = play_game_b2(GameState(cfg), telemetry=trk_b2)
    trk_open = TelemetryTracker()
    res_open = play_game_b2_open(GameState(cfg), telemetry=trk_open)

    # Déterminisme strict de B2_OPEN
    res_open_2 = play_game_b2_open(GameState(cfg))
    assert res_open == res_open_2
    assert 0.0 <= res_b2.ratio_arbres <= 1.0
    assert 0.0 <= res_open.ratio_arbres <= 1.0

    # Les compteurs d'activations par emplacement ne contiennent que des emplacements canoniques > 0
    acts = dict(trk_b2.summary().tile_activations)
    assert all(v > 0 for v in acts.values())


def test_template_calibration_panel_manifest_resolves_cleanly() -> None:
    tpl_path = ROOT / "campaigns" / "manifests" / "template_calibration_panel_v6_1.json"
    assert tpl_path.is_file()
    manifest = json.loads(tpl_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)
    assert plan["bots"] == CALIBRATION_BOT_PANEL == ("B0", "B1", "B2", "B2_OPEN")
    assert plan["ab_tile_protocol"] == "ACTIVE_VS_NEUTRE"
    assert plan["ab_slots"] == ("G1", "G2", "R1", "M1")


# ---------------------------------------------------------------------------
# 3. Protocole A/B apparié bout-en-bout, IC95, 1 cercle non estimable, pré-campagne
# ---------------------------------------------------------------------------


def test_paired_ab_active_vs_neutre_end_to_end_and_no_survival_rate(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Vérifie le protocole A/B apparié (G1 vs G2 co-lisières distincts, IC95, Holm, panel, pas de survival_rate)."""
    manifest: dict[str, Any] = {
        "campaign_name": "lot2_ab_panel_test",
        "description": "Test A/B apparié sur G1, G2 (co-lisières M-R) et M1 avec panel B0..B2_OPEN.",
        "mode": 4,
        "bots": "CALIBRATION_PANEL",
        "k_max": 2,
        "seed": 20261201,
        "player_counts": [4],
        "table_selection": "BALANCED_CIRCLES",
        "min_animaux_sauvages": 1,
        "games_per_configuration": 6,
        "ab_tile_protocol": "ACTIVE_VS_NEUTRE",
        "ab_slots": ["G1", "G2", "M1"],
        "base_instance": {"bundle_id": "STANDARD_A"},
    }
    manifest_file = tmp_path / "lot2_ab.json"
    manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
    plan = resolve_manifest_plan(manifest)
    assert plan["bots"] == ("B0", "B1", "B2", "B2_OPEN")

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(manifest_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0

    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", tmp_path / "digests")
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    _, _, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="local",
        job_name="local-lot2-ab",
        tasks=1,
        job_wall_sec=1.0,
    )

    # 1. Suppression définitive de survival_rate & CVaR directe + IC bootstrap
    totals = digest["totals"]
    assert "survival_rate" not in totals
    assert totals["cvar20_ratio"] == totals["game_cvar20_ratio"]
    assert totals["cvar20_ci95_low"] is not None and totals["cvar20_ci95_high"] is not None
    assert totals["cvar20_ci95_low"] <= totals["cvar20_ratio"] <= totals["cvar20_ci95_high"]

    # 2. Moyenne unifiée entre totals et inter_block_intervals / circle_dispersion
    ib = digest["inter_block_intervals"]
    cd = digest["circle_dispersion"]
    assert ib["global"]["mean_ratio_arbres"] == pytest.approx(totals["mean_ratio_arbres"], abs=1e-4)
    assert cd["global"]["mean_ratio_arbres"] == pytest.approx(totals["mean_ratio_arbres"], abs=1e-4)
    assert cd["global"]["estimable"] is True

    # 3. paired_comparisons complet avec panel B0/B1/B2/B2_OPEN, IC95 groupés, Holm et stabilité
    pc = digest["paired_comparisons"]
    assert pc["has_full_calibration_panel"] is True
    assert pc["reference_variant_id"] == "BASE"
    assert len(pc["variants_vs_reference"]) >= 1
    for v_entry in pc["variants_vs_reference"]:
        assert "global" in v_entry
        assert "by_bot" in v_entry
        assert "by_bot_x_n_players" in v_entry
        assert "sign_stability_b1_b2_open" in v_entry
        assert "holm_adjusted_p" in v_entry
    assert "sequential_ci_elimination" in pc
    assert any(b["comparison"] == "B2_OPEN_minus_B2" for b in pc["bot_panel_diffs"])

    # 4. tile_metrics A/B apparié (protocole ACTIVE_VS_NEUTRE + activations_per_game + stratification)
    tm = digest["tile_metrics"]
    assert set(tm.keys()) == {"G1:A", "G2:A", "M1:A"}
    for entry in tm.values():
        assert entry["protocol"] == "PAIRED_AB_ACTIVE_VS_NEUTRE"
        assert entry["ref_profile"] == "NEUTRE"
        assert "activations_per_game" in entry and entry["activations_per_game"] >= 0.0
        assert isinstance(entry["low_activation_lt1"], bool)
        assert "holm_adjusted_p" in entry
        assert "sign_stability_b1_b2_open" in entry
        assert isinstance(entry["by_bot_x_n_players"], list)

    # 5. Consignes aval exigent la citation des IC 95 %
    assert "intervalles de confiance à 95 %" in GEMINI_EDITORIAL_STYLE_INSTRUCTIONS
    assert "incertitude_obligatoire" in AUTHOR_REPORTING_INSTRUCTIONS


def test_single_circle_digest_reports_non_estimable_dispersion(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Lorsqu'un seul cercle est exécuté, l'incertitude inter-cercles est marquée 'non estimable'."""
    manifest: dict[str, Any] = {
        "campaign_name": "lot2_single_circle",
        "mode": 2,
        "bot": "B2",
        "k_max": 2,
        "seed": 20261201,
        "player_counts": [6],
        "games_per_configuration": 1,
        "base_instance": {"peuples_cercle": ["M", "R", "O", "H", "E", "I"]},
    }
    m_path = tmp_path / "single.json"
    m_path.write_text(json.dumps(manifest), encoding="utf-8")
    plan = resolve_manifest_plan(manifest)

    shards_dir = tmp_path / "shards"
    assert (
        run_campaign_manifest(
            manifest_source=str(m_path),
            task_index=0,
            task_count=1,
            workers=1,
            local_out_dir=str(shards_dir),
        )
        == 0
    )

    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", tmp_path / "digests")
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    _, _, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="local",
        job_name="local-single-circle",
        tasks=1,
        job_wall_sec=0.5,
    )
    g_disp = digest["circle_dispersion"]["global"]
    assert g_disp["n_circles"] == 1
    assert g_disp["estimable"] is False
    assert g_disp["status"] == "non_estimable_single_circle"
    assert g_disp["ci95_low"] is None and g_disp["ci95_high"] is None


def test_pilot_sample_size_estimator_runs_locally() -> None:
    manifest: dict[str, Any] = {
        "campaign_name": "lot2_pilot_sizing",
        "mode": 4,
        "bot": "B2",
        "k_max": 1,
        "seed": 20261201,
        "player_counts": [4],
        "games_per_configuration": 4,
        "slot_profile_comparisons": {"G7": ["A", "NEUTRE"]},
        "base_instance": {"bundle_id": "STANDARD_A"},
    }
    res = run_pilot_sample_size_estimation(manifest, pilot_pairs=6, target_delta=0.03)
    assert res["target_delta"] == 0.03
    assert len(res["estimates"]) == 1
    g_est = res["estimates"][0]["global"]
    assert g_est["n_pilot_pairs"] == 6
    assert g_est["required_pairs_ci95"] >= 10


# ---------------------------------------------------------------------------
# 4. Studio docs/index.html : affichage A/B apparié + masquage si < 1 act./partie
# ---------------------------------------------------------------------------


_NODE_AB_STUDIO_HARNESS = r"""
const fs = require('fs');
const vm = require('vm');

const [indexPath, dataPath, livretPath] = process.argv.slice(1);
const html = fs.readFileSync(indexPath, 'utf8');
const dataJs = fs.readFileSync(dataPath, 'utf8');
const livretJs = fs.readFileSync(livretPath, 'utf8');

const m = html.match(/<script>(?!\s*tailwind)([\s\S]*?)<\/script>/g);
if (!m || m.length === 0) throw new Error('Script principal introuvable dans docs/index.html');
const appScript = m[m.length - 1].replace(/^<script>/, '').replace(/<\/script>$/, '');

const sandbox = {
  console,
  window: {},
  document: {
    getElementById: () => null,
    querySelector: () => null,
    querySelectorAll: () => [],
    addEventListener: () => {},
    createElement: () => ({ style: {}, classList: { add() {}, remove() {}, contains: () => false } }),
  },
  navigator: {},
  localStorage: { getItem: () => null, setItem: () => {}, removeItem: () => {} },
  fetch: () => Promise.reject(new Error('no fetch in unit test')),
  setTimeout,
  clearTimeout,
};
sandbox.window = sandbox;
vm.createContext(sandbox);
new vm.Script(dataJs).runInContext(sandbox);
new vm.Script(livretJs).runInContext(sandbox);
new vm.Script(appScript).runInContext(sandbox);

const syntheticDigest = {
  campaign: 'test_ab_studio',
  totals: { total_games: 120 },
  tile_metrics: {
    'G1:A': {
      slot: 'G1',
      profile: 'A',
      ref_profile: 'NEUTRE',
      protocol: 'PAIRED_AB_ACTIVE_VS_NEUTRE',
      ab_effect_estimable: true,
      n_pairs: 80,
      mean_delta_ratio: 0.025,
      ci95_low: 0.011,
      ci95_high: 0.039,
      activations_per_game: 1.65,
      low_activation_lt1: false,
      significant: true,
    },
    'G2:A': {
      slot: 'G2',
      profile: 'A',
      ref_profile: 'NEUTRE',
      protocol: 'PAIRED_AB_ACTIVE_VS_NEUTRE',
      ab_effect_estimable: true,
      n_pairs: 80,
      mean_delta_ratio: 0.018,
      ci95_low: -0.005,
      ci95_high: 0.041,
      activations_per_game: 0.42,
      low_activation_lt1: true,
      significant: false,
    },
  },
};

sandbox.__D = syntheticDigest;
vm.runInContext('state.activeDigest = __D; state.digestIndex = buildDigestIndex(__D);', sandbox);
const htmlG1 = vm.runInContext('renderSlotDigestFooter("G1", ["A"]);', sandbox);
const htmlG2 = vm.runInContext('renderSlotDigestFooter("G2", ["A"]);', sandbox);
const promptPrefix = vm.runInContext('DIGEST_GEMINI_PROMPT_PREFIX;', sandbox);

if (!htmlG1.includes('+2.50 pts') || !htmlG1.includes('IC95') || !htmlG1.includes('1.65 act./partie')) {
  throw new Error('G1 (>=1 act/partie) doit afficher delta A/B et IC95 : ' + htmlG1);
}
if (htmlG2.includes('+1.80 pts') || !htmlG2.includes('masqué') || !htmlG2.includes('non significatif')) {
  throw new Error('G2 (<1 act/partie) doit masquer le delta et signaler non significatif : ' + htmlG2);
}
if (!promptPrefix.includes('intervalles de confiance à 95 %')) {
  throw new Error('DIGEST_GEMINI_PROMPT_PREFIX doit exiger la citation des IC95');
}
console.log(JSON.stringify({ ok: true }));
"""


def test_studio_renders_paired_ab_and_hides_low_activation_tiles() -> None:
    proc = subprocess.run(
        ["node", "-e", _NODE_AB_STUDIO_HARNESS, str(STUDIO_INDEX), str(STUDIO_DATA), str(STUDIO_LIVRET)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, f"Échec harness Studio A/B:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"
