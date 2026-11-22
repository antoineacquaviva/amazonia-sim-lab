"""Tests unitaires de préparation de l'audit exhaustif v6.0 :
- Chantier 1 : Sabotage actif sur B1/B2/B3, verrouillage ADV=SAUT & P4_2233 unique
- Chantier 2 : REVE_TRIG in {PASSIF, ACTIF} et ADV_COST in {1DEF, 2DEF, ONIRIQUE_COUNT}
- Chantier 3 : Couverture intégrale du Référentiel d'acceptation v6.x (acceptance_v6, sommeil_temporality, charge_assaut_metrics, furtivite_metrics)
- Chantier 4 : Instrumentation Rasoir d'Ockham (41 micro-règles + 8 embranchements de faux dilemmes)
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
from engine.core_engine import DEC_CHOIX_REVE_3_2, apply_choice, step_until_decision
from engine.primitives import DecisionRequest
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    REVE_5_TRIGGER_MODES,
    REVE_ADVANCE_COST_MODES,
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


def test_v6_0_reve_5_trigger_passif_vs_actif_and_partition() -> None:
    """Vérifie REVE_TRIG=PASSIF vs REVE_TRIG=ACTIF ainsi que la partition stricte 6. Insecte > 5. Rêve."""
    assert REVE_5_TRIGGER_MODES == ("PASSIF", "ACTIF")

    with pytest.raises(AssertionError, match="reve_5_trigger_mode"):
        GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), reve_5_trigger_mode="INVALID")

    # 1) Rêve en case 6 SANS Défenseur touché par un dé M=6 :
    #    - PASSIF -> 5. Rêve s'allume
    #    - ACTIF  -> 5. Rêve NE s'allume PAS
    for mode_trig, expected_lit in (("PASSIF", True), ("ACTIF", False)):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "H", "I"),
            reve_5_trigger_mode=mode_trig,
            exp_seed=7101,
        )
        st = GameState(cfg)
        st.tour = 2
        st.set_tactique_at_rank(5, TILE_R_BASE + 1)  # Rêve en case 6, 0 Défenseur
        st.set_gardien_at_case(5, 1, 1)  # Gardien posé sur 5. Rêve
        st.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)  # Pari engagé sur 5. Rêve
        st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
        st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
        for s in (1, 2, 3):
            st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        st.set_parcel_insectes(3, 1, 1)  # Ancre 4.3

        st.step = STEP_3_2_REVEAL
        _ = step_until_decision(st)
        assert st.has_gardien_opened_this_turn(5) is expected_lit
        assert st.count_gardien_pari_defenders_at_case(5) == (0 if expected_lit else 1)

    # 1b) Partition stricte 6. Insecte > 5. Rêve : si la carte est déviée par un Bug en 3.2 vers un Rêve,
    #     seul 6. Insecte s'ouvre (jamais 5. Rêve), même si le Rêve porte un Défenseur !
    cfg_bug = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "I"),
        reve_5_trigger_mode="ACTIF",
        exp_seed=7103,
    )
    st_bug = GameState(cfg_bug)
    st_bug.tour = 2
    st_bug.set_tactique_at_rank(5, TILE_R_BASE + 1)  # Rêve en case 6
    st_bug.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_bug.set_bugs_at_case(5, 1)  # 1 Bug sur case 5
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
    apply_choice(st_bug, "M_PLUS_1")  # Dévier M=5 -> M+1=6 (sur le Rêve !)
    req_rv_bug = step_until_decision(st_bug)
    assert isinstance(req_rv_bug, DecisionRequest) and req_rv_bug.decision_type == DEC_CHOIX_REVE_3_2
    apply_choice(st_bug, "BLOQUER")
    _ = step_until_decision(st_bug)
    assert st_bug.has_gardien_opened_this_turn(6) is True  # 6. Insecte ouvert !
    assert st_bug.has_gardien_opened_this_turn(5) is False  # 5. Rêve bloqué par partition !

    # 2) Sous ACTIF, un Rêve portant >= 1 Défenseur qui s'active réellement (BLOQUER ou AVANCER) allume 5. Rêve
    for choice_str in ("BLOQUER", "AVANCER"):
        cfg_act = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "H", "I"),
            reve_5_trigger_mode="ACTIF",
            exp_seed=7102,
        )
        st_act = GameState(cfg_act)
        st_act.tour = 2
        st_act.set_tactique_at_rank(5, TILE_R_BASE + 1)
        st_act.set_gardien_at_case(5, 1, 1)
        st_act.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
        st_act.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
        st_act.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
        st_act.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
        for s in (1, 2, 3):
            st_act.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        st_act.set_parcel_insectes(3, 1, 1)

        st_act.step = STEP_3_2_REVEAL
        req = step_until_decision(st_act)
        assert isinstance(req, DecisionRequest) and req.decision_type == DEC_CHOIX_REVE_3_2
        apply_choice(st_act, choice_str)
        _ = step_until_decision(st_act)
        assert st_act.has_gardien_opened_this_turn(5) is True
        assert st_act.count_gardien_pari_defenders_at_case(5) == 0


def test_v6_0_reve_advance_cost_1def_2def_and_onirique_count() -> None:
    """Vérifie ADV_COST in {1DEF, 2DEF, ONIRIQUE_COUNT} (1 Déf à 1 Onirique vs 2 Déf à 2 Oniriques)."""
    assert REVE_ADVANCE_COST_MODES == ("1DEF", "2DEF", "ONIRIQUE_COUNT")

    with pytest.raises(AssertionError, match="reve_advance_cost_mode"):
        GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), reve_advance_cost_mode="3DEF")

    # Vérifie ONIRIQUE_COUNT à 1 Peuple Onirique (1 Déf suffit) vs 2 Peuples Oniriques (2 Déf requis)
    cfg_oni_1 = GameConfig(
        n_players=3,
        mode=2,
        peuples=("M", "R", "H"),
        reve_advance_cost_mode="ONIRIQUE_COUNT",
        exp_seed=7200,
    )
    assert cfg_oni_1.nb_peuples_oniriques == 1
    assert cfg_oni_1.required_defenders_for_reve_advance() == 1

    st_o1 = GameState(cfg_oni_1)
    st_o1.tour = 2
    st_o1.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_o1.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_o1.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_o1.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_o1.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st_o1.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_o1.step = STEP_3_2_REVEAL
    req_o1 = step_until_decision(st_o1)
    assert isinstance(req_o1, DecisionRequest) and req_o1.decision_type == DEC_CHOIX_REVE_3_2
    assert req_o1.options == ("BLOQUER", "AVANCER")

    cfg_2d = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        reve_advance_cost_mode="ONIRIQUE_COUNT",
        reve_5_trigger_mode="ACTIF",
        exp_seed=7201,
    )
    assert cfg_2d.nb_peuples_oniriques == 2
    assert cfg_2d.required_defenders_for_reve_advance() == 2

    # Cas A : 1 seul Défenseur sur le Rêve à 2 Oniriques -> seul BLOQUER est légal, annule 1 machine sur 2
    st_1 = GameState(cfg_2d)
    st_1.tour = 2
    st_1.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_1.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_1.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_1.set_machine_pos_status(1, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st_1.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_1.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_1.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_1.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_1.set_parcel_insectes(3, 1, 1)

    trk_1 = TelemetryTracker()
    st_1.step = STEP_3_2_REVEAL
    req_1 = step_until_decision(st_1, telemetry=trk_1)
    assert isinstance(req_1, DecisionRequest) and req_1.decision_type == DEC_CHOIX_REVE_3_2
    assert req_1.options == ("BLOQUER",)
    assert req_1.context["can_advance"] is False
    assert req_1.context["required_advance_defenders"] == 2

    apply_choice(st_1, "BLOQUER", telemetry=trk_1)
    _ = step_until_decision(st_1, telemetry=trk_1)
    cancelled_1 = sum(1 for s in (0, 1) if st_1.get_player_hand(s)[4] == 0)
    assert cancelled_1 == 1
    assert st_1.get_tactique_at_rank(5) == TILE_R_BASE + 1
    assert trk_1.summary().dil_reve_forced_block == 1

    # Cas B : 2 Défenseurs sur le Rêve -> ("BLOQUER", "AVANCER") proposé, AVANCER consomme 2 Défenseurs
    st_2 = GameState(cfg_2d)
    st_2.tour = 2
    st_2.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_2.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_2.place_defender_reve_activation(1, 6, FACE_DEFINITIF)
    st_2.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_2.set_machine_pos_status(1, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st_2.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_2.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_2.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_2.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_2.set_parcel_insectes(3, 1, 1)

    trk_2 = TelemetryTracker()
    st_2.step = STEP_3_2_REVEAL
    req_2 = step_until_decision(st_2, telemetry=trk_2)
    assert isinstance(req_2, DecisionRequest) and req_2.decision_type == DEC_CHOIX_REVE_3_2
    assert req_2.options == ("BLOQUER", "AVANCER")
    assert req_2.context["can_advance"] is True
    assert req_2.context["dest_case"] == 5

    apply_choice(st_2, "AVANCER", telemetry=trk_2)
    assert st_2.count_reve_activation_consumed_at_case(6) == 2
    _ = step_until_decision(st_2, telemetry=trk_2)
    assert st_2.get_tactique_at_rank(4) == TILE_R_BASE + 1
    assert st_2.get_player_hand(0)[4] == 6 and st_2.get_player_hand(1)[4] == 6
    assert trk_2.summary().dil_reve_dual_advance == 1


def test_v6_0_sabotage_revived_in_b2_b1_and_b3() -> None:
    """Vérifie que le Sabotage n'est plus mort sur B2 (et B1/B3) et que mem_debt_score reste strictement nul."""
    sab_acq_b2 = 0
    sab_rev_b2 = 0
    sab_acq_b1 = 0
    tables = (("M", "R", "O"), ("M", "R", "H", "I"), ("M", "R", "O", "H", "E"))
    for rep in range(36):
        peuples = tables[rep % len(tables)]
        cfg = GameConfig.from_chassis_index(
            0,
            n_players=len(peuples),
            mode=2,
            peuples=peuples,
            reve_5_trigger_mode="ACTIF",
            reve_advance_cost_mode="ONIRIQUE_COUNT",
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
        sab_rev_b2 += s2.da_sabotage_revele

        trk1 = TelemetryTracker()
        _ = play_game_b1(GameState(cfg), telemetry=trk1)
        assert trk1.summary().mem_debt_score == 0
        sab_acq_b1 += trk1.summary().ok_sabotage_acquired

    assert sab_acq_b2 >= 3, f"Sabotage B2 toujours inerte : sab_acq_b2={sab_acq_b2}"
    assert sab_rev_b2 >= 1, f"Aucun Sabotage tiré en 1.2 sur B2 : sab_rev_b2={sab_rev_b2}"
    assert sab_acq_b1 >= 1, f"Sabotage B1 inerte : sab_acq_b1={sab_acq_b1}"

    cfg_b3 = GameConfig.from_chassis_index(
        0,
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        reve_5_trigger_mode="ACTIF",
        reve_advance_cost_mode="ONIRIQUE_COUNT",
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
    assert obs_b3.reve_advance_cost_mode == "ONIRIQUE_COUNT"


def test_v6_0_audit_manifest_2x3_and_digest_coverage(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Vérifie audit_exhaustif_socle_v6_0.json (2x3 variantes, P4_2233 unique, 41 040 parties) et les blocs digest v6.x."""
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "audit_exhaustif_socle_v6_0.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert "initiation_block" not in manifest
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "audit_exhaustif_socle_v6_0"
    assert plan["chassis_ids"] == (0,)  # P4_2233 unique
    assert len(plan["profile_variants"]) == 6
    assert {v["variant_id"] for v in plan["profile_variants"]} == {
        "REVE_TRIG=PASSIF|ADV_COST=1DEF",
        "REVE_TRIG=PASSIF|ADV_COST=2DEF",
        "REVE_TRIG=PASSIF|ADV_COST=ONIRIQUE_COUNT",
        "REVE_TRIG=ACTIF|ADV_COST=1DEF",
        "REVE_TRIG=ACTIF|ADV_COST=2DEF",
        "REVE_TRIG=ACTIF|ADV_COST=ONIRIQUE_COUNT",
    }
    # 6 variantes * 3 bots * 4 tailles * 570 = 41 040 parties
    assert plan["total_configurations"] == 72
    assert plan["total_games"] == 41_040
    assert all(u["chassis_id"] == 0 for u in plan["units"])

    # Micro-run local couvrant 2 variantes (dont ONIRIQUE_COUNT), B0/B1/B2, N=3..6
    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_audit_socle_v6_0"
    micro_manifest["games_per_configuration"] = 3
    micro_manifest["reve_5_trigger_modes"] = ["PASSIF", "ACTIF"]
    micro_manifest["reve_advance_cost_modes"] = ["ONIRIQUE_COUNT"]

    micro_file = tmp_path / "micro_audit_socle_v6_0.json"
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
        job_name="local-micro-audit-v6",
        tasks=1,
        job_wall_sec=0.8,
    )

    assert digest["totals"]["total_games"] == 72
    assert [r["chassis_id"] for r in digest["by_chassis"]] == [0]
    assert "initiation_block" not in digest

    con_pq = duckdb.connect(":memory:")
    pq_tot_row = con_pq.execute(
        f"SELECT CAST(SUM(n_games) AS INTEGER) FROM read_parquet('{parquet_path.as_posix()}')"
    ).fetchone()
    assert pq_tot_row is not None
    assert int(pq_tot_row[0]) == 72
    con_pq.close()

    assert "acceptance_v6" in digest
    acc = digest["acceptance_v6"]
    assert len(acc["bot_hierarchy_and_cognition"]) == 2
    assert all(h["zero_mem_debt_all_bots"] is True for h in acc["bot_hierarchy_and_cognition"])
    eq_b2 = [e for e in acc["equity_by_bot_x_variant"] if e["bot"] == "B2"]
    assert len(eq_b2) == 2
    for eq in eq_b2:
        assert len(eq["by_n_players"]) == 4
        assert all("table_cvar20_ratio" in r for r in eq["by_n_players"])
        assert all("table_cvar20_ratio" in r for r in eq["by_n_animaux_sauvages"])
        assert all("table_cvar20_ratio" in r for r in eq["by_has_insectes"])
        assert all("table_cvar20_ratio" in r for r in eq["by_n_peuples_oniriques"])

    assert "sommeil_temporality" in digest
    st_blk = digest["sommeil_temporality"]
    assert set(st_blk["global"]["tour_counts"].keys()) == {f"T{t}" for t in range(1, 8)}
    assert "pct_before_t5_of_sommeil" in st_blk["global"]
    assert all("ratio_6j_over_3j" in r for r in st_blk["by_variant_x_bot"])

    assert "charge_assaut_metrics" in digest
    ca_blk = digest["charge_assaut_metrics"]
    assert len(ca_blk["by_bot_x_n_players"]) == 12
    for row in ca_blk["by_bot_x_n_players"]:
        assert row["n_machines"] == 2 * row["n_players"]
        assert "tokens_per_machine_end_act1" in row
        assert "share_charge_gains_act1_pct" in row

    assert "furtivite_metrics" in digest
    fu_blk = digest["furtivite_metrics"]
    for k in (
        "turns_1_rive_per_game",
        "turns_2_rives_per_game",
        "rives_piege_per_game",
        "rives_sabotage_per_game",
        "orphan_pawns_per_game",
    ):
        assert k in fu_blk["global"]

    assert "ockham_razor" in digest
    ok_blk = digest["ockham_razor"]
    assert ok_blk["reference_policy"] == "B2"
    assert len(OCKHAM_COUNT_FIELDS) == 41
    assert len(DILEMMA_CHOICE_FIELDS) == 31
    assert len(ok_blk["primary"]["micro_rules"]) == 41
    assert len(ok_blk["primary"]["decision_branches"]) == 8
