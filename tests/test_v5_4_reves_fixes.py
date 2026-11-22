"""Tests dédiés à la Piste des Tactiques fixe T1..T6, purge 6.1,
SLOT_BUG_CERVEAU=B par défaut et activation des Rêves en 2.1 + 2.2 (v6.1 CLEAR_RANK_ONLY).
"""

from __future__ import annotations

import json
from pathlib import Path

from bots.heuristic_engine import play_game_b2
from campaigns.worker_main import resolve_manifest_plan
from engine.core_engine import (
    apply_step2_def1,
    apply_step2_def2,
    insert_reve_on_track,
    list_legal_targets,
    step_until_decision,
)
from engine.primitives import prim_permutation_piste
from engine.state import (
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    NUM_CHASSIS,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    STEP_3_2_REVEAL,
    TILE_R_BASE,
    TRACK_LEN,
    GameConfig,
    GameState,
    code_to_tile_id,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parent.parent


def test_fixed_track_192_chassis_and_bug_b_default() -> None:
    assert NUM_CHASSIS == 192
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=5420)
    assert cfg.reve_activation_mode == "1_DEF_1_MACHINE"
    assert cfg.profile_for_slot("SLOT_BUG_CERVEAU") == "B"
    assert cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"
    assert cfg.reve_advance_mode == "CLEAR_RANK_ONLY"

    st = GameState(cfg)
    assert [code_to_tile_id(st.get_tactique_at_rank(i)) for i in range(TRACK_LEN)] == [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
    ]
    # SWAP_RANKS est neutralisé sur piste fixe
    assert prim_permutation_piste(st, "SWAP_RANKS", rank_a=0, rank_b=1) is False
    assert [code_to_tile_id(st.get_tactique_at_rank(i)) for i in range(TRACK_LEN)] == [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
    ]


def test_reve_construction_rightmost_free_and_jump_push_advance() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), exp_seed=5421)
    st = GameState(cfg)

    # 1er Rêve -> case 6 (index 5), 2e Rêve -> case 5 (index 4) sans éjecter de Tactique
    assert insert_reve_on_track(st, 1) is None
    assert insert_reve_on_track(st, 2) is None
    assert [code_to_tile_id(st.get_tactique_at_rank(i)) for i in range(6)] == [
        "T1",
        "T2",
        "T3",
        "T4",
        "R2",
        "R1",
    ]

    # Primitive Mode 4 : Avancée de R1 (index 5) alors que index 4 porte R2 -> SAUTE vers la 1re case libre à gauche (index 3)
    assert prim_permutation_piste(st, "ADVANCE_REVE_LEFT", rank_a=5) is True
    assert [code_to_tile_id(st.get_tactique_at_rank(i)) for i in range(6)] == [
        "T1",
        "T2",
        "T3",
        "R1",
        "R2",
        "T6",
    ]

    st.set_tactique_at_rank(0, TILE_R_BASE + 2)
    st.set_tactique_at_rank(1, TILE_R_BASE + 1)
    st.set_tactique_at_rank(3, 4)
    st.set_tactique_at_rank(4, 5)
    assert prim_permutation_piste(st, "ADVANCE_REVE_LEFT", rank_a=1) is False


def test_step_2_1_and_2_2_reve_activation_open_while_gardien_stays_def2_only() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=5422)
    st = GameState(cfg)
    insert_reve_on_track(st, 1)  # R1 en case 6
    st.set_gardien_at_case(1, 1, face=1)

    targets_def1 = list_legal_targets(st, 0, is_first_defender=True)
    targets_def2 = list_legal_targets(st, 0, is_first_defender=False)
    # v6.1 : 2.1 est ouverte aux Rêves ; seule la Piste des Gardiens reste réservée à 2.2
    assert ("REVE_ACTIVATION", 6) in targets_def1
    assert ("REVE_ACTIVATION", 6) in targets_def2
    assert ("REVE_ACTIVATION", 5) not in targets_def1
    assert ("GARDIEN_PARI", 1) not in targets_def1
    assert ("GARDIEN_PARI", 1) in targets_def2

    st.step = STEP_2_1_DEF1
    apply_step2_def1(st, 0, ("REVE_ACTIVATION", 6))
    st.step = STEP_2_2_DEF2
    apply_step2_def2(st, 1, ("POSER_DEFINITIF", ("REVE_ACTIVATION", 6)))
    assert st.count_reve_activation_defenders_at_case(6) == 2
    obs = st.get_observation(2)
    assert obs.reve_at_case(6) == 1
    assert obs.reve_activation_defenders(6) == 2
    assert obs.reve_def1_count(6) == 1
    assert obs.player_def1_reve_case(0) == 6
    assert obs.player_def2_reve_case(1) == 6


def test_reve_activation_modes_a_b_c_and_telemetry() -> None:
    def _run_case(mode_name: str, n_defs: int) -> tuple[int, int, int | None, int, int, int]:
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "O", "H"),
            reve_activation_mode=mode_name,
            exp_seed=5423,
        )
        st = GameState(cfg)
        st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 sur case 5 (sous-jacente : T5)
        st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
        st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=0, bleus=0)
        st.set_machine_pos_status(1, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
        st.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=3, bleus=0)

        st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 6, 5, 0)
        st.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 5, 6, 5, 0)
        st.set_player_hand(2, 0, 0, 0, 0, 0)
        st.set_player_hand(3, 0, 0, 0, 0, 0)
        for s in range(n_defs):
            st.place_defender_reve_activation(s, 5, FACE_DEFINITIF)
        st.set_parcel_insectes(2, 1, 1)
        st.step = STEP_3_2_REVEAL
        trk = TelemetryTracker()
        _ = step_until_decision(st, telemetry=trk)
        ts = trk.summary()
        return (
            st.get_player_hand(0)[4],
            st.get_player_hand(1)[4],
            st.find_tactique_rank(TILE_R_BASE + 1),
            ts.reves_activated,
            ts.machines_cancelled_by_reve,
            ts.machines_bypassed_inactive_reve,
        )

    # Option A (1_DEF_1_MACHINE) avec blocage pur CLEAR_RANK_ONLY (le Rêve reste en index 4) :
    assert _run_case("1_DEF_1_MACHINE", 0) == (5, 5, 4, 0, 0, 2)
    assert _run_case("1_DEF_1_MACHINE", 1) == (5, 0, 4, 1, 1, 1)
    assert _run_case("1_DEF_1_MACHINE", 2) == (0, 0, 4, 1, 2, 0)

    # Option B (1_DEF_ALL_RANK) :
    assert _run_case("1_DEF_ALL_RANK", 0) == (5, 5, 4, 0, 0, 2)
    assert _run_case("1_DEF_ALL_RANK", 1) == (0, 0, 4, 1, 2, 0)

    # Option C (BINOME_ALL_RANK) :
    assert _run_case("BINOME_ALL_RANK", 1) == (5, 5, 4, 0, 0, 2)
    assert _run_case("BINOME_ALL_RANK", 2) == (0, 0, 4, 1, 2, 0)


def test_calibration_reves_fixes_manifest_and_b2_smoke() -> None:
    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_reves_fixes_v5_4.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["mode"] == 2
    assert plan["bot"] == "B2"
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["migration_policy"]["SLOT_BUG_CERVEAU"] == "B"
    assert plan["migration_policy"]["SLOT_COLONISATION_GARDIENS"] == "A"
    assert len(plan["profile_variants"]) == 3
    assert {v["reve_activation_mode"] for v in plan["profile_variants"]} == {
        "1_DEF_1_MACHINE",
        "1_DEF_ALL_RANK",
        "BINOME_ALL_RANK",
    }
    oniric_counts = {sum(1 for p in u["peuples"] if p in ("H", "E")) for u in plan["units"]}
    assert oniric_counts == {0, 1, 2}

    for mode_name in ("1_DEF_1_MACHINE", "1_DEF_ALL_RANK", "BINOME_ALL_RANK"):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "H", "E"),
            reve_activation_mode=mode_name,
            exp_seed=5424,
        )
        trk = TelemetryTracker()
        over = play_game_b2(GameState(cfg), k_max_passes=3, telemetry=trk)
        assert 1 <= over.tour_fin <= 8
        assert 0.0 <= over.ratio_arbres <= 1.0
