"""Tests de validation v6.4 Phase C : Tuiles à blanc sans biais bot, 197 assises,
micro-forks v6.4, audit Ockham (delta == 0), traces human_trace_1.0, reprise Cloud Batch Spot
et publication double (digest exécutif < 35 Ko + rapport Markdown complet).
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path
from typing import Any

import pytest

import campaigns.digest_builder as db_mod
import run_campaign as rc_mod
from bots.belief_and_ticks import any_tile_text_active, is_tile_text_active
from bots.bot_b0 import play_game_b0
from bots.bot_b3_rh import play_game_b3
from bots.heuristic_engine import play_game_b1, play_game_b2, play_game_b2_open
from bots.human_eval import load_human_traces_jsonl
from campaigns.designs import ALL_V6_4_FORK_FAMILIES, run_v6_4_causal_forks_on_config
from campaigns.modular_studies import (
    _EMBEDDED_TILES_CANON_FALLBACK,
    CANONICAL_15_EDGES,
    CANONICAL_30_TILES,
    build_tile_profiles_from_active_subset,
    get_disjoint_motors,
    get_pivot_motors,
    get_pivot_tiles,
    get_role_motors,
    load_tile_canon_metadata,
    resolve_modular_study_variants,
)
from campaigns.ockham_and_traces import (
    RemarkableBookmarkTracker,
    V64DecisionAuditRecorder,
    extract_remarkable_traces_jsonl,
    select_top_remarkable_bookmarks,
    summarize_v64_ockham_audit,
)
from campaigns.reporting import (
    build_executive_digest,
    format_campaign_quote_5_lines,
    generate_balancing_alerts,
    render_campaign_markdown_report,
)
from campaigns.worker_main import (
    resolve_manifest_plan,
    run_campaign_manifest,
)
from engine.state import GameConfig, GameState


def _all_neutre_profiles() -> tuple[tuple[str, str], ...]:
    return build_tile_profiles_from_active_subset(())


# ---------------------------------------------------------------------------
# 1. Zéro biais bot sur Tuiles à blanc (Mode 2 == Mode 4 ALL_NEUTRE sur B0..B3)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("bot_name", ["B0", "B1", "B2", "B2_OPEN", "B3"])
def test_mode2_equals_mode4_all_neutre_bit_exact_for_all_bots(bot_name: str) -> None:
    """Chaque bot (B0..B3) doit jouer à l'identique bit-à-bit entre Mode 2 et Mode 4 ALL_NEUTRE."""
    all_neutre = _all_neutre_profiles()
    peuples_cases = (
        [("M", "R", "O", "H")]
        if bot_name == "B3"
        else [
            ("M", "R", "O", "H"),
            ("M", "O", "E", "I"),
            ("R", "H", "E"),
        ]
    )
    for idx, peuples in enumerate(peuples_cases):
        cfg_m2 = GameConfig(
            n_players=len(peuples),
            peuples=peuples,
            mode=2,
            exp_seed=20261128 + idx,
            rep_id=idx,
            tile_profiles=(),
        )
        cfg_m4 = GameConfig(
            n_players=len(peuples),
            peuples=peuples,
            mode=4,
            exp_seed=20261128 + idx,
            rep_id=idx,
            tile_profiles=all_neutre,
        )
        assert not any_tile_text_active(cfg_m2)
        assert not any_tile_text_active(cfg_m4)
        for tid in CANONICAL_30_TILES:
            assert not is_tile_text_active(cfg_m4, tid)

        if bot_name == "B0":
            r2 = play_game_b0(GameState(cfg_m2))
            r4 = play_game_b0(GameState(cfg_m4))
        elif bot_name == "B1":
            r2 = play_game_b1(GameState(cfg_m2))
            r4 = play_game_b1(GameState(cfg_m4))
        elif bot_name == "B2":
            r2 = play_game_b2(GameState(cfg_m2))
            r4 = play_game_b2(GameState(cfg_m4))
        elif bot_name == "B2_OPEN":
            r2 = play_game_b2_open(GameState(cfg_m2))
            r4 = play_game_b2_open(GameState(cfg_m4))
        else:
            r2 = play_game_b3(GameState(cfg_m2), n_determinizations=1, max_candidates=3, horizon_turns=1)
            r4 = play_game_b3(GameState(cfg_m4), n_determinizations=1, max_candidates=3, horizon_turns=1)

        assert (r2.score_arbres, r2.tour_fin, r2.cause_fin) == (
            r4.score_arbres,
            r4.tour_fin,
            r4.cause_fin,
        ), f"Divergence {bot_name} sur {peuples}: M2={r2} vs M4_NEUTRE={r4}"


def test_single_active_tile_text_guard_and_plume_stability() -> None:
    """Seule la tuile activée est reconnue active par les bots ; Oiseau Plume ne crashe pas."""
    profs = build_tile_profiles_from_active_subset(("G1", "G7"))
    cfg = GameConfig(
        n_players=4,
        peuples=("M", "R", "O", "H"),
        mode=4,
        exp_seed=20261129,
        rep_id=0,
        tile_profiles=profs,
    )
    assert is_tile_text_active(cfg, "G1")
    assert is_tile_text_active(cfg, "G7")
    assert not is_tile_text_active(cfg, "G2")
    assert not is_tile_text_active(cfg, "R1")
    assert any_tile_text_active(cfg, ("G1", "G2"))
    assert not any_tile_text_active(cfg, ("G2", "R1"))
    res = play_game_b2(GameState(cfg))
    assert 0 <= res.score_arbres <= 40


# ---------------------------------------------------------------------------
# 2. Moteur d'études modulaires « Tuiles à blanc » & 197 Assises
# ---------------------------------------------------------------------------


def test_modular_studies_catalog_parity_motors_and_deduplication() -> None:
    """Vérifie parité fallback vs tiles_canon_v6_4.json, partition 30/30, pivots, 2x2 et LOO."""
    meta_live = load_tile_canon_metadata()
    live_tiles = meta_live["tuiles_ciblees"]
    fb_tiles = _EMBEDDED_TILES_CANON_FALLBACK["tuiles_ciblees"]
    assert set(live_tiles.keys()) == set(CANONICAL_30_TILES)
    assert set(fb_tiles.keys()) == set(CANONICAL_30_TILES)
    for tid in CANONICAL_30_TILES:
        assert live_tiles[tid]["nature"] == fb_tiles[tid]["nature"]
        assert set(live_tiles[tid]["entrees"]) == set(fb_tiles[tid]["entrees"])
        assert set(live_tiles[tid]["sorties"]) == set(fb_tiles[tid]["sorties"])
        assert set(live_tiles[tid]["roles_portes"]) == set(fb_tiles[tid]["roles_portes"])

    disjoint = get_disjoint_motors()
    assert len(disjoint) == 5
    all_disj_slots = [s for slots in disjoint.values() for s in slots]
    assert len(all_disj_slots) == 30
    assert set(all_disj_slots) == set(CANONICAL_30_TILES)
    assert get_disjoint_motors(_EMBEDDED_TILES_CANON_FALLBACK) == disjoint

    pivots_m = get_pivot_motors()
    assert len(pivots_m) == 7
    assert get_pivot_motors(_EMBEDDED_TILES_CANON_FALLBACK) == pivots_m
    piv_tiles = get_pivot_tiles()
    assert len(piv_tiles) >= 15

    roles_m = get_role_motors()
    assert len(roles_m) >= 5

    # SOLO_AND_ECOSYSTEM sur les 30 tuiles -> exactement 62 variantes uniques
    vs_se = resolve_modular_study_variants({"study_type": "SOLO_AND_ECOSYSTEM", "slots": "ALL"})
    assert len(vs_se) == 62

    # EDGE_2X2 sur les 15 lisières -> exactement 46 variantes dédupliquées (1 ALL_NEUTRE + 30 solos + 15 paires)
    vs_2x2 = resolve_modular_study_variants(
        {"study_type": "EDGE_2X2", "edges": "ALL", "background": "ALL_NEUTRE"}
    )
    assert len(CANONICAL_15_EDGES) == 15
    assert len(vs_2x2) == 46

    # MOTORS_BOTH (DISJOINT) -> ALL_NEUTRE + ALL_ACTIVE + 5 solos + 5 ablations = 12 variantes
    vs_mot = resolve_modular_study_variants({"study_type": "MOTORS_BOTH", "motor_family": "DISJOINT"})
    assert len(vs_mot) == 12

    # Raccourci top-level active_slots -> 1 variante BASE avec G1/R1 actifs et les 28 autres NEUTRE
    plan_top = resolve_manifest_plan(
        {
            "schema_version": "6.4",
            "campaign_name": "test_active_top",
            "mode": 4,
            "player_counts": [4],
            "games_per_configuration": 2,
            "bot": "B2",
            "active_slots": ["G1", "R1"],
        }
    )
    assert len(plan_top["profile_variants"]) == 1
    top_p = dict(plan_top["profile_variants"][0]["tile_profiles"])
    assert top_p["G1"] == "A" and top_p["R1"] == "A" and top_p["G2"] == "NEUTRE"

    # Étude SUBSET avec baselines ALL_NEUTRE + ALL_ACTIVE -> 3 variantes
    plan_sub = resolve_manifest_plan(
        {
            "schema_version": "6.4",
            "campaign_name": "test_subset",
            "mode": 4,
            "player_counts": [4],
            "games_per_configuration": 2,
            "bot": "B2",
            "tile_study": {
                "study_type": "SUBSET",
                "active_slots": ["G1", "R1"],
                "include_baselines": ["ALL_NEUTRE", "ALL_ACTIVE"],
            },
        }
    )
    assert len(plan_sub["profile_variants"]) == 3
    sub_var = next(v for v in plan_sub["profile_variants"] if v["study_role"] == "subset")
    sub_p = dict(sub_var["tile_profiles"])
    assert sub_p["G1"] == "A"
    assert sub_p["R1"] == "A"
    assert sub_p["G2"] == "NEUTRE"


def test_all_197_assises_resolution_and_b3_cap() -> None:
    """ALL_197_ASSISES couvre exactement les 197 assises canoniques et applique reps_cap_per_table à B3."""
    plan = resolve_manifest_plan(
        {
            "schema_version": "6.4",
            "campaign_name": "test_197",
            "mode": 4,
            "player_counts": [3, 4, 5, 6],
            "table_selection": "ALL_197_ASSISES",
            "reps_per_assise": 6,
            "bots": ["B2", "B3"],
            "b3_config": {"reps_cap_per_table": 2, "n_determinizations": 1},
        }
    )
    b2_units = [u for u in plan["units"] if u["bot"] == "B2"]
    b3_units = [u for u in plan["units"] if u["bot"] == "B3"]
    assert len(b2_units) == 197
    assert len(b3_units) == 197
    assert all(u["n_games"] == 6 for u in b2_units)
    assert all(u["n_games"] == 2 for u in b3_units)
    assert len({u["assise_key"] for u in b2_units}) == 197


# ---------------------------------------------------------------------------
# 3. Micro-forks causaux v6.4
# ---------------------------------------------------------------------------


def test_v6_4_causal_forks_fire_and_respect_family_filter() -> None:
    """Vérifie le déclenchement des familles de micro-forks v6.4 et le filtrage sélectif."""
    profs = build_tile_profiles_from_active_subset(CANONICAL_30_TILES)
    cfg = GameConfig(
        n_players=4,
        peuples=("M", "R", "O", "H"),
        mode=4,
        exp_seed=20261128,
        rep_id=0,
        tile_profiles=profs,
    )
    full_res = run_v6_4_causal_forks_on_config(
        cfg,
        n_eval_rollouts=2,
        fork_families=ALL_V6_4_FORK_FAMILIES,
    )
    fired = (
        int(full_res.has_2_1_anchor)
        + int(full_res.mf_2_2 is not None)
        + int(full_res.has_2_1_chaman_fork)
        + int(full_res.has_alteration_fork)
        + int(full_res.has_3_1_gardien_icone_fork)
        + int(full_res.has_eveil_fork)
        + int(full_res.has_furt_sentinelle_fork)
        + int(full_res.has_6_1_enracinement_fork)
    )
    assert fired >= 3

    # Filtrage sélectif : seule la famille CHAMANES active
    chaman_only = run_v6_4_causal_forks_on_config(
        cfg,
        n_eval_rollouts=1,
        fork_families=("CHAMANES",),
    )
    assert chaman_only.has_2_1_chaman_fork is True
    assert chaman_only.mf_2_2 is None
    assert chaman_only.has_alteration_fork is False
    assert chaman_only.has_3_1_gardien_icone_fork is False


# ---------------------------------------------------------------------------
# 4. Audit Ockham v6.4 (delta == 0) & Traces remarquables (human_trace_1.0)
# ---------------------------------------------------------------------------


def test_v64_ockham_recorder_zero_delta_and_false_dilemma_detection() -> None:
    """V64DecisionAuditRecorder est strictement lecture seule (delta == 0) et signale les > 90 %."""
    profs = build_tile_profiles_from_active_subset(CANONICAL_30_TILES)
    cfg = GameConfig(
        n_players=4,
        peuples=("M", "R", "O", "H"),
        mode=4,
        exp_seed=20261130,
        rep_id=2,
        tile_profiles=profs,
    )
    rec = V64DecisionAuditRecorder()
    res_plain = play_game_b2(GameState(cfg))
    res_audit = play_game_b2(GameState(cfg), on_decision=rec)
    assert (res_plain.score_arbres, res_plain.tour_fin, res_plain.cause_fin) == (
        res_audit.score_arbres,
        res_audit.tour_fin,
        res_audit.cause_fin,
    )
    compact = rec.to_compact_dict()
    assert compact["internal"], "Au moins un choix interne v6.4 doit être enregistré"

    # Vérification de la détection d'un faux dilemme (> 90 % sur >= 20 décisions)
    synthetic = {
        "internal": {
            "faux_dilemme_test": {"OPTION_A": 24, "OPTION_B": 1},
            "vrai_dilemme_test": {"OPTION_A": 13, "OPTION_B": 12},
        },
        "tile_effects": {},
    }
    summary = summarize_v64_ockham_audit(synthetic, false_dilemma_threshold_pct=90.0, min_samples=20)
    assert "faux_dilemme_test" in summary["flagged_false_dilemmas"]["internal"]
    assert "vrai_dilemme_test" not in summary["flagged_false_dilemmas"]["internal"]


def test_remarkable_traces_export_roundtrip_human_trace_1_0(tmp_path: Path) -> None:
    """L'export des parties remarquables produit un JSONL human_trace_1.0 valide pour human_logger.html."""
    profs = build_tile_profiles_from_active_subset(CANONICAL_30_TILES)
    tracker = RemarkableBookmarkTracker()
    for rep in range(3):
        cfg = GameConfig(
            n_players=4,
            peuples=("M", "R", "O", "H"),
            mode=4,
            exp_seed=20261201,
            rep_id=rep,
            tile_profiles=profs,
        )
        res = play_game_b2(GameState(cfg))
        tracker.observe(
            cfg=cfg,
            res=res,
            bot="B2",
            variant_id="ALL_ACTIVE",
            assise_key="4J:M-R-O-H",
        )
    selected = select_top_remarkable_bookmarks(tracker.to_json_list(), max_games=2)
    assert 1 <= len(selected) <= 2

    out_jsonl = tmp_path / "traces_test.jsonl"
    meta = extract_remarkable_traces_jsonl(selected, output_path=out_jsonl, campaign_name="test_tr")
    assert out_jsonl.exists()
    assert meta["n_games"] == len(selected)
    assert meta["n_decisions"] > 0

    loaded = load_human_traces_jsonl(out_jsonl)
    assert len(loaded) == meta["n_decisions"]
    assert all(rec.schema_version == "human_trace_1.0" for rec in loaded)


# ---------------------------------------------------------------------------
# 5. Résilience préemption Spot (checkpoints worker + vagues Cloud Batch)
# ---------------------------------------------------------------------------


def test_worker_checkpoint_resume_and_skip_existing_shards(tmp_path: Path) -> None:
    """Le worker reprend depuis un checkpoint partiel sans doublon et saute un shard déjà existant."""
    manifest = {
        "schema_version": "6.4",
        "campaign_name": "test_ckpt",
        "mode": 4,
        "player_counts": [4],
        "games_per_configuration": 2,
        "bot": "B0",
        "tile_study": {"study_type": "SUBSET", "slots": ["G1"]},
    }
    m_path = tmp_path / "m.json"
    m_path.write_text(json.dumps(manifest), encoding="utf-8")
    shards_dir = tmp_path / "shards"
    ckpt_dir = shards_dir / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)

    # 1. Exécution complète de référence (shard 0/1)
    rc_ref = run_campaign_manifest(
        manifest_source=str(m_path),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
        checkpoint_every=1,
    )
    assert rc_ref == 0
    shard_file = shards_dir / "shard_00.jsonl.gz"
    assert shard_file.exists()
    with gzip.open(shard_file, "rt", encoding="utf-8") as fh:
        ref_rows = [json.loads(line) for line in fh if line.strip()]
    assert len(ref_rows) >= 2

    # 2. skip_existing_shards ne réécrit pas un shard déjà complet
    mtime_before = shard_file.stat().st_mtime_ns
    rc_skip = run_campaign_manifest(
        manifest_source=str(m_path),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
        skip_existing_shards=True,
    )
    assert rc_skip == 0
    assert shard_file.stat().st_mtime_ns == mtime_before

    # 3. Simulation d'une reprise après préemption Spot : on garde seulement 1 ligne en checkpoint
    shard_file.unlink()
    ckpt_file = ckpt_dir / "ckpt_00.jsonl.gz"
    with gzip.open(ckpt_file, "wt", encoding="utf-8") as fh:
        fh.write(json.dumps(ref_rows[0]) + "\n")

    rc_resume = run_campaign_manifest(
        manifest_source=str(m_path),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
        checkpoint_every=1,
    )
    assert rc_resume == 0
    with gzip.open(shard_file, "rt", encoding="utf-8") as fh:
        resumed_rows = [json.loads(line) for line in fh if line.strip()]
    assert len(resumed_rows) == len(ref_rows)
    assert [(r["variant_id"], r["table_id"], r["sum_arbres"]) for r in resumed_rows] == [
        (r["variant_id"], r["table_id"], r["sum_arbres"]) for r in ref_rows
    ]


def test_cloud_batch_spot_multi_wave_recovery_mocked(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Simule une préemption Spot sur la vague 1 : la vague 2 ne relance que le shard manquant."""
    present_shards: set[int] = set()
    launched_waves: list[tuple[int, tuple[int, ...] | None]] = []

    def fake_list_shards(_gcloud: str, _prefix: str) -> set[int]:
        return set(present_shards)

    def fake_batch_job(
        _gcloud: str,
        *,
        wave_idx: int = 1,
        task_indices: tuple[int, ...] | None = None,
        **_kwargs: Any,
    ) -> tuple[str, float]:
        launched_waves.append((wave_idx, task_indices))
        if wave_idx == 1:
            # Les shards 0 et 2 réussissent, le shard 1 est préempté Spot
            present_shards.update({0, 2})
            raise RuntimeError("PREEMPTION_SPOT_50001")
        # Vague 2 : uniquement le shard 1 est relancé et réussit
        assert task_indices == (1,)
        present_shards.add(1)
        return f"amazonia-wave{wave_idx}", 12.5

    monkeypatch.setattr(rc_mod, "_list_gcs_present_shard_indices", fake_list_shards)
    monkeypatch.setattr(rc_mod, "_run_cloud_batch_job", fake_batch_job)

    run_dir = tmp_path / "spot_run"
    job_name, wall_sec = rc_mod._run_cloud_batch_with_spot_recovery(
        "gcloud",
        campaign_name="spot_test",
        run_id="20261128T000000Z_abc12345",
        manifest_gcs_uri="gs://bucket/manifest.json",
        gcs_prefix="campaigns/spot_test/run1",
        tasks=3,
        timeout_sec=1800,
        run_dir=run_dir,
        max_spot_waves=4,
    )
    assert job_name == "amazonia-wave2"
    assert wall_sec == 12.5
    assert launched_waves == [(1, None), (2, (1,))]
    state_json = json.loads((run_dir / "run_state.json").read_text(encoding="utf-8"))
    assert state_json["status"] == "COMPLETE"
    assert state_json["present_shards"] == [0, 1, 2]


# ---------------------------------------------------------------------------
# 6. Devis 5 lignes, Alertes, Digest exécutif < 35 Ko, Rapport MD & Suites locales
# ---------------------------------------------------------------------------


def test_quote_5_lines_alerts_executive_digest_and_markdown() -> None:
    """Vérifie le devis en 5 lignes exactes (0 € LLM), les alertes et le budget < 35 Ko."""
    manifest = {
        "schema_version": "6.4",
        "campaign_name": "quote_test",
        "description": "Test devis modulaire",
        "mode": 4,
        "player_counts": [3, 4],
        "games_per_configuration": 4,
        "bots": ["B2", "B3"],
        "tile_study": {"study_type": "SOLO_ISOLATED", "slots": ["G1", "R1"]},
        "include_v64_ockham_audit": True,
    }
    plan = resolve_manifest_plan(manifest)
    quote = format_campaign_quote_5_lines(manifest, plan, backend="batch", tasks=4, workers=4)
    lines = [ln for ln in quote.splitlines() if ln.strip()]
    assert len(lines) == 5
    assert "0,00 €" in lines[4]

    # Vérifie que build_executive_digest compresse un très gros digest sous 35 Ko
    huge_digest: dict[str, Any] = {
        "campaign": "huge_test",
        "generated_at_utc": "2026-11-28T00:00:00Z",
        "plan": {"mode": 4, "player_counts": [3, 4], "bots": ["B2", "B3"]},
        "totals": {
            "total_games": 5000,
            "mean_ratio_arbres": 0.42,
            "cvar20_ratio": 0.20,
            "pct_tour_8": 60.0,
            "pct_reve_rang_1": 10.0,
            "pct_reveil_gardiens": 2.0,
            "pct_effondrement": 28.0,
            "mean_tours": 7.1,
        },
        "b3_degenerate_audit": {
            "enabled": True,
            "paired_tables": 10,
            "delta_b3_minus_b2_ratio": 0.14,
            "ending_shifts_pts": {"sommeil": 20.0},
            "degenerate_flag": True,
        },
        "assises_197_summary": {
            "n_assises_covered": 197,
            "n_compositions_covered": 42,
            "worst_assises": [{"assise_key": "3J:H-E-I", "mean_ratio_arbres": 0.35, "n_games": 10}],
            "best_assises": [{"assise_key": "6J:M-R-O-H-E-I", "mean_ratio_arbres": 0.80, "n_games": 10}],
            "all_assises": [{"assise_key": f"A{i}", "pad": "x" * 250} for i in range(197)],
        },
    }
    alerts = generate_balancing_alerts(huge_digest)
    codes = {a["code"] for a in alerts}
    assert "SURVIE_BASSE" in codes
    assert "CVAR20_CRITIQUE" in codes
    assert "B3_STRATEGIE_DEGENEREE" in codes

    exec_d = build_executive_digest(huge_digest, max_bytes=34_000)
    raw_exec = json.dumps(exec_d, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert len(raw_exec) < 35_000
    assert exec_d["digest_mode"] == "EXECUTIVE"

    md = render_campaign_markdown_report(exec_d)
    assert "## 1. Alertes automatiques" in md
    assert "B3_STRATEGIE_DEGENEREE" in md


def test_end_to_end_local_modular_study_and_campaign_suite(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Exécute localement (--backend local) une étude Tuiles à blanc + B3 + Ockham + Traces
    puis une campaign_suite à 2 étapes avec reprise --resume-run-id (zéro appel Cloud).
    """
    digests_dir = tmp_path / "data" / "digests"
    docs_digests_dir = tmp_path / "docs" / "digests"
    docs_index = docs_digests_dir / "index.json"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    docs_digests_dir.mkdir(parents=True, exist_ok=True)
    docs_index.write_text(json.dumps({"schema_version": "1.0", "digests": []}) + "\n", encoding="utf-8")

    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "DOCS_DIGESTS_DIR", docs_digests_dir)
    monkeypatch.setattr(rc_mod, "DOCS_DIGESTS_INDEX", docs_index)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    # A. Campagne modulaire locale combinant EDGE_2X2 (1 lisière), B2 + B3, Ockham & Traces
    mod_manifest = {
        "schema_version": "6.4",
        "manifest_type": "campaign_plan",
        "campaign_name": "e2e_mod_edge_mr",
        "description": "Validation locale 2x2 lisière M_R + B2/B3 + Ockham + Traces",
        "mode": 4,
        "player_counts": [4],
        "table_selection": "BENCHMARK_ASSISES",
        "reps_per_assise": 1,
        "bots": ["B2", "B3"],
        "b3_config": {"reps_cap_per_table": 1, "n_determinizations": 1, "max_candidates": 2, "horizon_turns": 1},
        "include_v64_ockham_audit": True,
        "extract_remarkable_traces": {"enabled": True, "max_games": 2},
        "tile_study": {
            "study_type": "EDGE_2X2",
            "edges": ["M_R"],
            "background": "ALL_NEUTRE",
        },
        "seed": 20261202,
    }
    mod_path = tmp_path / "e2e_mod_edge_mr.json"
    mod_path.write_text(json.dumps(mod_manifest), encoding="utf-8")

    # --quote-only doit réussir sans créer .tmp_runs
    assert rc_mod.main([str(mod_path), "--quote-only"]) == 0
    assert not (tmp_path / ".tmp_runs").exists()

    # Exécution locale complète
    rc1 = rc_mod.main([str(mod_path), "--backend", "local", "--skip-git-push"])
    assert rc1 == 0

    studio_digest = docs_digests_dir / "digest_e2e_mod_edge_mr.json"
    report_md = tmp_path / "docs" / "rapports" / "rapport_e2e_mod_edge_mr.md"
    traces_jsonl = tmp_path / "docs" / "traces" / "traces_e2e_mod_edge_mr.jsonl"
    assert studio_digest.exists()
    assert studio_digest.stat().st_size < 35_000
    assert report_md.exists()
    assert traces_jsonl.exists()

    d_exec = json.loads(studio_digest.read_text(encoding="utf-8"))
    assert "modular_study" in d_exec
    assert "M_R" in d_exec["modular_study"]["edges_2x2"]
    assert "b3_degenerate_audit" in d_exec and d_exec["b3_degenerate_audit"]["enabled"]
    assert "alerts" in d_exec and len(d_exec["alerts"]) >= 1
    assert "executive_summary" in d_exec
    md_txt = report_md.read_text(encoding="utf-8")
    assert not report_md.read_bytes().startswith(b"\xef\xbb\xbf")
    assert "\r\n" not in md_txt
    assert "Carrés factoriels `2×2`" in md_txt
    assert "Audit anti-stratégies dégénérées" in md_txt
    loaded_tr = load_human_traces_jsonl(traces_jsonl)
    assert len(loaded_tr) > 0

    # B. Suite orchestrée multi-étapes (campaign_suite) + reprise idempotente --resume-run-id
    suite_manifest = {
        "schema_version": "6.4",
        "manifest_type": "campaign_suite",
        "campaign_name": "e2e_suite_v6_4",
        "description": "Mini-suite locale 2 étapes",
        "seed": 20261203,
        "player_counts": [4],
        "stages": [
            {
                "stage_name": "st1_subset",
                "mode": 4,
                "table_selection": "BENCHMARK_ASSISES",
                "reps_per_assise": 1,
                "bot": "B0",
                "active_slots": ["G1"],
            },
            {
                "stage_name": "st2_forks",
                "mode": 4,
                "table_selection": "BENCHMARK_ASSISES",
                "reps_per_assise": 1,
                "bot": "B2",
                "micro_forks": True,
                "fork_families": ["CHAMANES"],
            },
        ],
    }
    suite_path = tmp_path / "e2e_suite_v6_4.json"
    suite_path.write_text(json.dumps(suite_manifest), encoding="utf-8")

    assert rc_mod.main([str(suite_path), "--quote-only"]) == 0
    rc2 = rc_mod.main(
        [str(suite_path), "--backend", "local", "--resume-run-id", "suite_fixed_id", "--skip-git-push"]
    )
    assert rc2 == 0
    master_digest_p = docs_digests_dir / "digest_e2e_suite_v6_4.json"
    master_report_p = tmp_path / "docs" / "rapports" / "rapport_e2e_suite_v6_4.md"
    assert master_digest_p.exists() and master_digest_p.stat().st_size < 35_000
    assert master_report_p.exists()
    master_d = json.loads(master_digest_p.read_text(encoding="utf-8"))
    assert len(master_d["stages_summary"]) == 2
    assert "Récapitulatif de la suite orchestrée" in master_report_p.read_text(encoding="utf-8")

    # Reprise immédiate : les 2 étapes sont déjà terminées et sautées proprement
    rc3 = rc_mod.main(
        [str(suite_path), "--backend", "local", "--resume-run-id", "suite_fixed_id", "--skip-git-push"]
    )
    assert rc3 == 0
