"""Tests dédiés à la Piste des Tactiques fixe T1..T6,
SLOT_BUG_CERVEAU=B natif et activation des Rêves en 2.1 + 2.2 (v6.1 1_DEF_1_MACHINE / CLEAR_RANK_ONLY).
"""

from __future__ import annotations

from bots.heuristic_engine import play_game_b2
from engine.core_engine import (
    DEC_CHOIX_CIBLE_REVE_3_2,
    apply_choice,
    apply_step2_def1,
    apply_step2_def2,
    insert_reve_on_track,
    list_legal_targets,
    step_until_decision,
)
from engine.primitives import DecisionRequest, prim_permutation_piste
from engine.state import (
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
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


def test_fixed_track_and_bug_b_default() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=5420)
    assert cfg.profile_for_slot("SLOT_BUG_CERVEAU") == "B"
    assert cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"

    st = GameState(cfg)
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

    # v6.2 (INV-15) : poussée de bloc contigu vers la gauche (R2, R1 glissent ensemble vers 3, 4)
    assert prim_permutation_piste(st, "ADVANCE_REVE_LEFT", rank_a=5) is True
    assert [code_to_tile_id(st.get_tactique_at_rank(i)) for i in range(6)] == [
        "T1",
        "T2",
        "T3",
        "R2",
        "R1",
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


def test_reve_activation_1_def_1_machine_and_telemetry() -> None:
    def _run_case(n_defs: int) -> tuple[int, int, int | None, int, int, int]:
        cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=5423)
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
        st.set_parcel_nid(3, 2, 1)  # Ancre 4.2 (I présent)
        st.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)
        st.step = STEP_3_2_REVEAL
        trk = TelemetryTracker()
        res = step_until_decision(st, telemetry=trk)
        if isinstance(res, DecisionRequest) and res.decision_type == DEC_CHOIX_CIBLE_REVE_3_2:
            assert (1,) in res.options
            apply_choice(st, (1,), telemetry=trk)
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

    # v6.2 : 1_DEF_1_MACHINE avec choix propriétaire sur surcharge + blocage pur (Rêve reste en index 4)
    assert _run_case(0) == (5, 5, 4, 0, 0, 2)
    assert _run_case(1) == (5, 0, 4, 1, 1, 1)
    assert _run_case(2) == (0, 0, 4, 1, 2, 0)

    cfg_b2 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), exp_seed=5424)
    over = play_game_b2(GameState(cfg_b2), k_max_passes=3, telemetry=TelemetryTracker())
    assert 1 <= over.tour_fin <= 8
    assert 0.0 <= over.ratio_arbres <= 1.0
