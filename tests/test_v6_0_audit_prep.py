"""Tests unitaires de l'instrumentation d'acceptation v6.1 et Rasoir d'Ockham :
- REVE_TRIG=ACTIF figé et partition stricte 6. Insecte > 5. Rêve
- Sabotage actif sur B1/B2/B3 en Furtivité « Chaud vs Calme » et mem_debt == 0
- Couverture intégrale du Référentiel d'acceptation (acceptance_v6, game_cvar20_ratio, charge_assaut_metrics, furtivite_metrics)
- Instrumentation Rasoir d'Ockham (46 micro-règles + 8 embranchements de dilemmes)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import duckdb
import pytest

import run_campaign as rc_mod
from bots.bot_b3_rh import play_game_b3
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import apply_choice, step_until_decision
from engine.primitives import DecisionRequest
from engine.state import (
    CARD_SABOTAGE,
    CHARGE_GAIN_MODES,
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_STATUS_NORMAL,
    REVE_5_TRIGGER_MODES,
    STEP_3_2_REVEAL,
    STEP_GAME_OVER,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import (
    DILEMMA_CHOICE_FIELDS,
    OCKHAM_COUNT_FIELDS,
    TelemetryTracker,
)
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


def test_v6_1_reve_5_trigger_locked_actif_and_partition() -> None:
    """Vérifie REVE_TRIG=ACTIF figé ainsi que la partition stricte 6. Insecte > 5. Rêve."""
    assert REVE_5_TRIGGER_MODES == ("ACTIF",)
    assert CHARGE_GAIN_MODES == ("DEGAT_EFFECTIF", "FRAPPE_NON_PAREE")

    for bad_trig in ("PASSIF", "INVALID"):
        with pytest.raises(AssertionError, match="reve_5_trigger_mode"):
            GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), reve_5_trigger_mode=bad_trig)

    # 1) Rêve en case 6 SANS Défenseur touché par un dé M=6 -> inerte, 5. Rêve NE s'allume PAS
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=7101)
    st_inert = GameState(cfg)
    st_inert.tour = 2
    st_inert.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_inert.set_gardien_at_case(5, 1, 1)
    st_inert.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_inert.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_inert.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_inert.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_inert.set_parcel_insectes(3, 1, 1)
    st_inert.step = STEP_3_2_REVEAL
    _ = step_until_decision(st_inert)
    assert st_inert.has_gardien_opened_this_turn(5) is False
    assert st_inert.count_gardien_pari_defenders_at_case(5) == 1

    # 2) Partition stricte 6. Insecte > 5. Rêve : carte déviée par Bug vers un Rêve défendu -> seul 6. Insecte s'allume !
    st_bug = GameState(cfg)
    st_bug.tour = 2
    st_bug.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_bug.place_defender_reve_activation(0, 6, FACE_DEFINITIF, def_idx=0)
    st_bug.set_bugs_at_case(5, 1)
    st_bug.set_gardien_at_case(5, 1, 1)
    st_bug.set_gardien_at_case(6, 2, 1)
    st_bug.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_bug.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    st_bug.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_bug.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)
    for s in (1, 2, 3):
        st_bug.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_bug.set_parcel_insectes(3, 1, 1)
    st_bug.step = STEP_3_2_REVEAL
    req_bug = step_until_decision(st_bug)
    assert isinstance(req_bug, DecisionRequest)
    apply_choice(st_bug, "M_PLUS_1")
    _ = step_until_decision(st_bug)
    assert st_bug.has_gardien_opened_this_turn(6) is True
    assert st_bug.has_gardien_opened_this_turn(5) is False
    assert st_bug.get_player_hand(0)[4] == 0  # La machine déviée a bien été annulée par le Défenseur sur R1 !

    # 3) Rêve portant >= 1 Défenseur (posé en 2.1) annulant une carte non déviée -> 5. Rêve s'allume !
    st_act = GameState(cfg)
    st_act.tour = 2
    st_act.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_act.set_gardien_at_case(5, 1, 1)
    st_act.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_act.place_defender_reve_activation(0, 6, FACE_DEFINITIF, def_idx=0)
    st_act.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_act.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_act.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_act.set_parcel_insectes(3, 1, 1)
    st_act.step = STEP_3_2_REVEAL
    _ = step_until_decision(st_act)
    assert st_act.has_gardien_opened_this_turn(5) is True
    assert st_act.count_gardien_pari_defenders_at_case(5) == 0


def test_v6_1_furtivite_piege_and_sabotage_active_in_b2_b1_and_b3() -> None:
    """Vérifie que B1, B2 et B3 exploitent Rive Piège et Rive Sabotage avec mem_debt_score == 0."""
    sab_acq_b2 = 0
    pieges_b2 = 0
    sab_acq_b1 = 0
    pieges_b1 = 0
    tables = (("M", "R", "O"), ("M", "R", "H", "I"), ("M", "R", "O", "H", "E"))
    for rep in range(36):
        peuples = tables[rep % len(tables)]
        cfg = GameConfig.from_chassis_index(
            0,
            n_players=len(peuples),
            mode=2,
            peuples=peuples,
            exp_seed=7300,
            rep_id=rep,
            max_revision_passes=3,
        )
        trk2 = TelemetryTracker()
        out2 = play_game_b2(GameState(cfg), telemetry=trk2)
        s2 = trk2.summary()
        assert s2.mem_debt_score == 0
        assert out2.tour_fin <= 8
        sab_acq_b2 += s2.ok_sabotage_acquired
        pieges_b2 += s2.ok_pieges_placed

        trk1 = TelemetryTracker()
        _ = play_game_b1(GameState(cfg), telemetry=trk1)
        s1 = trk1.summary()
        assert s1.mem_debt_score == 0
        sab_acq_b1 += s1.ok_sabotage_acquired
        pieges_b1 += s1.ok_pieges_placed

    assert pieges_b2 >= 5, f"Rive Piège B2 inerte : pieges_b2={pieges_b2}"
    assert sab_acq_b2 >= 2, f"Rive Sabotage B2 inerte : sab_acq_b2={sab_acq_b2}"
    assert pieges_b1 + sab_acq_b1 >= 3

    cfg_b3 = GameConfig.from_chassis_index(
        0,
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        exp_seed=7399,
        rep_id=0,
        max_revision_passes=3,
    )
    st_b3 = GameState(cfg_b3)
    trk_b3 = TelemetryTracker()
    out_b3 = play_game_b3(st_b3, n_determinizations=2, max_candidates=2, telemetry=trk_b3)
    assert st_b3.step == STEP_GAME_OVER
    assert out_b3.tour_fin <= 8
    assert trk_b3.summary().mem_debt_score == 0
    obs_b3 = st_b3.get_observation(0)
    assert obs_b3.reve_5_trigger_mode == "ACTIF"
    assert obs_b3.charge_gain_mode == "DEGAT_EFFECTIF"


def test_v6_1_macro_and_micro_forks_digest_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Vérifie validation_socle_v6_1.json + forks_causalite_v6_1.json et tous les blocs du digest v6.1."""
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "validation_socle_v6_1.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["chassis_ids"] == (24,)
    assert len(plan["profile_variants"]) == 2
    assert {v["variant_id"] for v in plan["profile_variants"]} == {
        "CHARGE=DEGAT_EFFECTIF",
        "CHARGE=FRAPPE_NON_PAREE",
    }
    assert plan["total_configurations"] == 24
    assert plan["total_games"] == 13_680

    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_audit_socle_v6_1"
    micro_manifest["games_per_configuration"] = 3
    micro_file = tmp_path / "micro_audit_socle_v6_1.json"
    micro_file.write_text(json.dumps(micro_manifest), encoding="utf-8")
    micro_plan = resolve_manifest_plan(micro_manifest)
    assert micro_plan["total_games"] == 72

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(micro_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0

    digests_dir = tmp_path / "data_digests"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    parquet_path = tmp_path / "cells.parquet"
    _, _, digest = aggregate_campaign_duckdb(
        manifest=micro_manifest,
        plan=micro_plan,
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        backend="local",
        job_name="local-micro-audit-v61",
        tasks=1,
        job_wall_sec=0.8,
    )

    assert digest["totals"]["total_games"] == 72
    assert "game_cvar20_ratio" in digest["totals"]
    con_pq = duckdb.connect(":memory:")
    pq_tot_row = con_pq.execute(
        f"SELECT CAST(SUM(n_games) AS INTEGER) FROM read_parquet('{parquet_path.as_posix()}')"
    ).fetchone()
    assert pq_tot_row is not None and int(pq_tot_row[0]) == 72
    con_pq.close()

    acc = digest["acceptance_v6"]
    assert len(acc["bot_hierarchy_and_cognition"]) == 2
    assert all(h["zero_mem_debt_all_bots"] is True for h in acc["bot_hierarchy_and_cognition"])
    for eq in acc["equity_by_bot_x_variant"]:
        assert all("game_cvar20_ratio" in r for r in eq["by_n_players"])

    fu_blk = digest["furtivite_metrics"]["global"]
    for k in (
        "rives_piege_per_game",
        "rives_piege_lost_per_game",
        "win_rate_rive_piege_pct",
        "rives_sabotage_per_game",
        "rives_sabotage_lost_per_game",
        "win_rate_rive_sabotage_pct",
        "pieges_placed_per_game",
        "pieges_triggered_per_game",
        "piege_multi_strike_parries_per_game",
    ):
        assert k in fu_blk

    ok_blk = digest["ockham_razor"]
    assert len(OCKHAM_COUNT_FIELDS) == 46
    assert len(DILEMMA_CHOICE_FIELDS) == 32
    assert len(ok_blk["primary"]["micro_rules"]) == 46
    assert len(ok_blk["primary"]["decision_branches"]) == 8

    cc_blk = digest["cross_check_v6_0_to_v6_1"]
    assert cc_blk["baseline_campaign"] == "audit_exhaustif_socle_v6_0"
    assert cc_blk["reference_bot"] == "B2"
    p1 = cc_blk["phase1_blocking_audit"]
    assert p1["abatteuse_ratissage_souche"]["verdict"] == "REMOVED_IN_V6_1_STANDARD_COUPE_ARBRE"
    assert p1["invariants_and_fuzzing"]["zero_mem_debt_all_bots"] is True
    assert p1["autonomous_piege_scope"]["configured_piege_scope_modes"] == ["SINGLE_STRIKE"]
    p2 = cc_blk["phase2_displacement_targets_b2_by_variant"]
    assert set(p2.keys()) == {"CHARGE=DEGAT_EFFECTIF", "CHARGE=FRAPPE_NON_PAREE"}
    for vid_k, v_blk in p2.items():
        assert v_blk["n_games_ref_bot"] > 0, vid_k
        for sec in (
            "difficulte_globale",
            "eveil_actif_et_reve_2_1",
            "equite_et_sommeil",
            "furtivite_chaud_vs_calme_et_pieges_autonomes",
            "summary",
        ):
            assert sec in v_blk
        assert v_blk["equite_et_sommeil"]["in_target_sommeil_zero"] is True

