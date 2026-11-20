"""Tests unitaires v5.4.4 : Pari unique Gardiens, Consommation symétrique Rêves,
Éveil par mobilisation croisée (PARITY / PARITY_CAP_ONIRIQUE), FREE_SLOT_ONLY et cascade 5->4.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from bots.belief_and_ticks import resolve_step2_2_from_state
from bots.bot_b3_rh import _gameover_utility
from bots.heuristic_engine import score_target_b2
from campaigns.digest_builder import build_active_core_rules
from campaigns.worker_main import _execute_manifest_unit, resolve_manifest_plan
from engine.core_engine import (
    apply_step2_def2,
    list_legal_targets,
    lock_all_def2_in_place,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects import load_all_effects
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    GameOver,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    NUM_CHASSIS,
    STEP_2_2_DEF2,
    STEP_3_2_REVEAL,
    STEP_5_1_TACTIQUES,
    STEP_5_3_END_CHECK,
    TILE_R_BASE,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parent.parent


def test_pari_unique_par_gardien_toutes_cases() -> None:
    """Chaque Gardien construit (cases 1..6) ne peut recevoir au maximum qu'1 seul Défenseur en 2.2."""
    assert NUM_CHASSIS == 192

    # Sans Animal Sauvage (H, E, I) : cible GARDIEN_PARI interdite
    cfg_no_animal = GameConfig(n_players=3, mode=2, peuples=("H", "E", "I"))
    assert cfg_no_animal.nb_animaux_sauvages == 0
    assert cfg_no_animal.nb_peuples_oniriques == 2
    st_no = GameState(cfg_no_animal)
    st_no.set_gardien_at_case(1, 1, face=1)
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_no, 0, is_first_defender=False)

    # Mode 1 : interdit même avec Animaux Sauvages
    cfg_m1 = GameConfig(n_players=4, mode=1, peuples=("M", "R", "O", "H"))
    st_m1 = GameState(cfg_m1)
    st_m1.set_gardien_at_case(1, 1, face=1)
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_m1, 0, is_first_defender=False)

    # Mode 2 avec Animaux Sauvages : max 1 Défenseur uniformément sur les 6 cases (y compris 1 et 4)
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"))
    assert cfg.nb_animaux_sauvages == 3
    assert cfg.nb_peuples_oniriques == 1
    st = GameState(cfg)
    for c in range(1, 7):
        st.set_gardien_at_case(c, c, face=1)

    # 1er Défenseur ne peut jamais cibler GARDIEN_PARI
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st, 0, is_first_defender=True)
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st, 0, is_first_defender=True)

    # Pose sur case 1 puis case 4 : un 2e joueur ne peut plus cibler ni 1 ni 4
    apply_step2_def2(st, 0, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    apply_step2_def2(st, 1, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    legal_s2 = list_legal_targets(st, 2, is_first_defender=False)
    assert ("GARDIEN_PARI", 1) not in legal_s2
    assert ("GARDIEN_PARI", 4) not in legal_s2
    assert ("GARDIEN_PARI", 2) in legal_s2
    assert ("GARDIEN_PARI", 5) in legal_s2

    # Tentative directe de cumul sur case 1 ou case 4 doit échouer
    with pytest.raises(AssertionError):
        st.place_defender_gardien_pari(2, 1, FACE_DEFINITIF)
    with pytest.raises(AssertionError):
        st.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)


def test_gardien_zero_def_inactive_and_case4_antiloop() -> None:
    """0 Déf = inactif ; 1 Déf = 1 ouverture ; l'ouverture sur 4. Gardien ne ré-allume jamais 4."""
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"))
    st = GameState(cfg)
    st.set_gardien_at_case(1, 1, face=1)
    st.set_gardien_at_case(4, 2, face=1)

    # Sans Défenseur : inactif
    st.light_trigger(1)
    assert sweep_gardiens(st) == 0

    # 1 Défenseur sur case 1 et 1 Défenseur sur case 4
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 4, FACE_DEFINITIF)

    # Déclenchement case 1 : ouvre case 1 -> allume 4 -> ouvre case 4 -> 4 reste éteinte !
    st.light_trigger(1)
    opened = sweep_gardiens(st)
    assert opened == 2
    assert st.count_gardien_pari_defenders_at_case(1) == 0
    assert st.count_gardien_pari_consumed_at_case(1) == 1
    assert st.count_gardien_pari_defenders_at_case(4) == 0
    assert st.count_gardien_pari_consumed_at_case(4) == 1
    assert not st.is_trigger_lit(4)

    # Nouveau déclenchement case 1 : 0 Défenseur restant -> plus aucune ouverture
    st.light_trigger(1)
    assert sweep_gardiens(st) == 0


def test_step5_3_bet_won_upgrade_vs_bet_lost_return_lisiere() -> None:
    """En 5.3 : pari gagné reste (Face 2 en Mode 3/4 si double-face) ; pari perdu retourne en lisière Face 1."""
    load_all_effects()

    cfg_m2 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"))
    st_m2 = GameState(cfg_m2)
    st_m2.tour = 2
    g1_slot = st_m2.find_lisiere_slot_by_tile_id("G1")
    g2_slot = st_m2.find_lisiere_slot_by_tile_id("G2")
    assert g1_slot is not None and g2_slot is not None
    st_m2.set_lisiere_tile_state(g1_slot, LISIERE_CONSTRUCTED, 0)
    st_m2.set_lisiere_tile_state(g2_slot, LISIERE_CONSTRUCTED, 0)
    st_m2.set_gardien_at_case(1, 1, face=1)
    st_m2.set_gardien_at_case(2, 2, face=1)
    st_m2.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_m2.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    assert prim_partage_info_etat_gardien(st_m2, "MARK_GARDIEN_OPENED", case_1_6=1) is True

    trk = TelemetryTracker()
    st_m2.step = STEP_5_3_END_CHECK
    step_until_decision(st_m2, telemetry=trk)
    assert st_m2.get_gardien_at_case(1) == (1, 1)
    assert st_m2.get_gardien_at_case(2) == (0, 1)
    assert st_m2.get_lisiere_tile_state(g2_slot)[0] == LISIERE_UNCONSTRUCTED
    ts = trk.summary()
    assert ts.gardien_bets_won == 1
    assert ts.gardien_bets_lost == 1


def test_mobilisation_croisee_parity_vs_parity_cap_onirique_and_tour8() -> None:
    """Mobilisation croisée : PARITY (g >= r), PARITY_CAP_ONIRIQUE (g >= r et r <= nb_oniriques), priorité Tour 8."""
    from engine.core_engine import _run_step_3_2

    # Table N=4 : M, R, O, H -> A=3, nb_peuples_oniriques=1 (H seul)
    # Répartition 2 Gardiens + 2 Rêves :
    # - sous PARITY : 2 >= 2 -> Éveil RÉUSSI !
    # - sous PARITY_CAP_ONIRIQUE : r=2 > nb_oniriques=1 -> Éveil REFUSÉ !
    for policy, expected_eveil in (("PARITY", True), ("PARITY_CAP_ONIRIQUE", False)):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "O", "H"),
            reve_activation_mode="1_DEF_1_MACHINE",
            reveil_reves_policy=policy,
        )
        st = GameState(cfg)
        st.tour = 3
        st.set_gardien_at_case(1, 1, face=1)
        st.set_gardien_at_case(4, 2, face=1)
        st.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 sur case 6
        # Mains : 2 machines pointant sur case 6 (R3)
        st.set_player_hand(0, 1, 6, 6, 6, 0)
        st.set_player_hand(1, 3, 6, 6, 6, 0)
        st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
        st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)

        # 2 Défenseurs sur Gardiens (cases 1 & 4) + 2 Défenseurs sur Rêve (case 6)
        st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
        st.place_defender_gardien_pari(1, 4, FACE_DEFINITIF)
        st.place_defender_reve_activation(2, 6, FACE_DEFINITIF)
        st.place_defender_reve_activation(3, 6, FACE_DEFINITIF)

        # Étape 3.2 : les 2 Défenseurs sur le Rêve annulent 2 machines -> 2 consommés, 0 restant !
        st.step = STEP_3_2_REVEAL
        _run_step_3_2(st)
        assert st.total_reve_activation_consumed() == 2
        assert st.total_reve_activation_remaining() == 0

        # Ouverture case 1 -> allume 4 -> ouvre case 4 -> 2 Gardiens consommés, 0 restant !
        st.light_trigger(1)
        sweep_gardiens(st)
        assert st.total_gardien_pari_consumed() == 2
        assert st.total_gardien_pari_remaining() == 0

        assert st.is_eveil_gardiens_victory() is expected_eveil
        st.step = STEP_5_3_END_CHECK
        res = step_until_decision(st)
        if expected_eveil:
            assert isinstance(res, GameOver)
            assert res.cause_fin == CAUSE_REVEIL_GARDIENS
        else:
            assert not isinstance(res, GameOver)

    # Sous PARITY_CAP_ONIRIQUE avec 3 Gardiens + 1 Rêve (r=1 <= nb_oniriques=1) : Éveil RÉUSSI !
    cfg_cap_ok = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        reveil_reves_policy="PARITY_CAP_ONIRIQUE",
    )
    st_ok = GameState(cfg_cap_ok)
    st_ok.tour = 4
    st_ok.set_gardien_at_case(1, 1, face=1)
    st_ok.set_gardien_at_case(5, 2, face=1)
    st_ok.set_gardien_at_case(4, 3, face=1)
    st_ok.set_tactique_at_rank(5, TILE_R_BASE + 3)
    st_ok.set_player_hand(0, 1, 6, 6, 6, 0)
    st_ok.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st_ok.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_ok.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_ok.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_ok.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_ok.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_ok.place_defender_reve_activation(3, 6, FACE_DEFINITIF)
    st_ok.step = STEP_3_2_REVEAL
    _run_step_3_2(st_ok)
    st_ok.light_trigger(1)
    sweep_gardiens(st_ok)
    assert st_ok.is_eveil_gardiens_victory() is True

    # Défenseur surnuméraire sur Rêve (non consommé) = pari perdu -> Éveil REFUSÉ !
    st_lost = GameState(cfg_cap_ok)
    st_lost.tour = 4
    st_lost.set_gardien_at_case(1, 1, face=1)
    st_lost.set_gardien_at_case(4, 2, face=1)
    st_lost.set_gardien_at_case(5, 3, face=1)
    st_lost.set_tactique_at_rank(5, TILE_R_BASE + 3)
    # Aucune machine ne pointe sur case 6 -> Défenseur sur Rêve NON consommé !
    st_lost.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st_lost.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st_lost.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_lost.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_lost.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_lost.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_lost.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_lost.place_defender_reve_activation(3, 6, FACE_DEFINITIF)
    st_lost.step = STEP_3_2_REVEAL
    _run_step_3_2(st_lost)
    assert st_lost.total_reve_activation_consumed() == 0
    assert st_lost.total_reve_activation_remaining() == 1
    st_lost.light_trigger(1)
    sweep_gardiens(st_lost)
    assert st_lost.is_eveil_gardiens_victory() is False

    # Priorité absolue à CAUSE_TOUR_8 au Tour 8 même si tous les paris sont gagnés
    st_t8 = GameState(cfg_cap_ok)
    st_t8.tour = 8
    st_t8.set_gardien_at_case(1, 1, face=1)
    st_t8.set_gardien_at_case(5, 2, face=1)
    st_t8.set_gardien_at_case(4, 3, face=1)
    st_t8.set_tactique_at_rank(5, TILE_R_BASE + 3)
    st_t8.set_player_hand(0, 1, 6, 6, 6, 0)
    st_t8.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st_t8.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_t8.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_t8.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_t8.place_defender_reve_activation(3, 6, FACE_DEFINITIF)
    st_t8.step = STEP_3_2_REVEAL
    _run_step_3_2(st_t8)
    st_t8.light_trigger(1)
    sweep_gardiens(st_t8)
    st_t8.step = STEP_5_3_END_CHECK
    res_t8 = step_until_decision(st_t8)
    assert isinstance(res_t8, GameOver)
    assert res_t8.cause_fin == CAUSE_TOUR_8


def test_reve_advance_mode_free_slot_only_vs_jump_push() -> None:
    """FREE_SLOT_ONLY n'avance un Rêve que si la case immédiatement à gauche est libre (sinon sur place)."""
    # Configuration de piste : [T1, T2, T3, T4, R1 (case 5), R2 (case 6)]
    # Activation de R2 (rank_a=5) alors que case 5 (rank 4) est occupée par R1 :
    # - JUMP_PUSH : pousse [R1, R2] en cases 4..5, case 6 redevient T6
    cfg_jp = GameConfig(n_players=3, mode=2, peuples=("M", "H", "I"), reve_advance_mode="JUMP_PUSH")
    st_jp = GameState(cfg_jp)
    st_jp.set_tactique_at_rank(4, TILE_R_BASE + 1)
    st_jp.set_tactique_at_rank(5, TILE_R_BASE + 2)
    moved_jp = prim_permutation_piste(st_jp, "ADVANCE_REVE_LEFT", rank_a=5)
    assert moved_jp is True
    assert st_jp.get_tactique_at_rank(3) == TILE_R_BASE + 1
    assert st_jp.get_tactique_at_rank(4) == TILE_R_BASE + 2
    assert st_jp.get_tactique_at_rank(5) == 6  # T6 restaurée

    # - FREE_SLOT_ONLY : case 5 (rank 4) occupée par R1 -> R2 reste sur place !
    cfg_fs = GameConfig(
        n_players=3, mode=2, peuples=("M", "H", "I"), reve_advance_mode="FREE_SLOT_ONLY"
    )
    st_fs = GameState(cfg_fs)
    st_fs.set_tactique_at_rank(4, TILE_R_BASE + 1)
    st_fs.set_tactique_at_rank(5, TILE_R_BASE + 2)
    moved_blocked = prim_permutation_piste(st_fs, "ADVANCE_REVE_LEFT", rank_a=5)
    assert moved_blocked is False
    assert st_fs.get_tactique_at_rank(4) == TILE_R_BASE + 1
    assert st_fs.get_tactique_at_rank(5) == TILE_R_BASE + 2

    # En revanche, R1 (rank 4) a la case 4 (rank 3) immédiatement libre -> R1 avance d'1 cran !
    moved_free = prim_permutation_piste(st_fs, "ADVANCE_REVE_LEFT", rank_a=4)
    assert moved_free is True
    assert st_fs.get_tactique_at_rank(3) == TILE_R_BASE + 1
    assert st_fs.get_tactique_at_rank(4) == 5  # T5 restaurée
    assert st_fs.get_tactique_at_rank(5) == TILE_R_BASE + 2


def test_cascade_reve_to_case5_to_case4_and_telemetry() -> None:
    """Cascade complète Rêve (3.2) -> 5. Rêve -> 4. Gardien -> Éveil en 5.3 + télémétrie complète."""
    # Table N=3 : M, R, H (A=2, nb_oniriques=1)
    # 1 Défenseur sur Rêve (case 6) + 1 sur 5. Rêve + 1 sur 4. Gardien -> g=2 >= r=1 -> Éveil !
    cfg = GameConfig(
        n_players=3,
        mode=2,
        peuples=("M", "R", "H"),
        reveil_reves_policy="PARITY_CAP_ONIRIQUE",
        reve_advance_mode="FREE_SLOT_ONLY",
    )
    st = GameState(cfg)
    st.tour = 3
    st.set_gardien_at_case(5, 1, face=1)
    st.set_gardien_at_case(4, 2, face=1)
    st.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 sur case 6
    st.set_player_hand(0, 1, 6, 6, 6, 0)  # Machine pointant sur case 6 (R3)
    st.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)

    st.place_defender_reve_activation(0, 6, FACE_REFLEXION)
    st.place_defender_gardien_pari(1, 5, FACE_REFLEXION)
    st.place_defender_gardien_pari(2, 4, FACE_REFLEXION)

    trk = TelemetryTracker()
    lock_all_def2_in_place(st)
    assert st.is_eveil_attempt_eligible() is True
    trk.on_reveil_attempt(st)

    # Étape 3.2 : R3 annule la machine -> Déf consommé -> allume 5. Rêve -> ouvre G5 -> allume 4. Gardien -> ouvre G4 !
    st.step = STEP_3_2_REVEAL
    step_until_decision(st, telemetry=trk)
    assert st.total_reve_activation_consumed() == 1
    assert st.total_reve_activation_remaining() == 0
    assert st.count_gardien_pari_consumed_at_case(5) == 1
    assert st.count_gardien_pari_consumed_at_case(4) == 1
    assert st.total_gardien_pari_remaining() == 0
    # R3 a avancé d'1 cran en case 5 (rank 4) car libre
    assert st.get_tactique_at_rank(4) == TILE_R_BASE + 3

    trk.on_step_transition(st, STEP_2_2_DEF2, STEP_5_1_TACTIQUES)
    st.step = STEP_5_3_END_CHECK
    res = step_until_decision(st, telemetry=trk)
    assert isinstance(res, GameOver)
    assert res.cause_fin == CAUSE_REVEIL_GARDIENS
    ts = trk.summary()
    assert ts.rs_count == 1
    assert ts.rs_def_gardien == 2
    assert ts.rs_def_reve == 1
    assert ts.rs_reves_opened == 1
    assert ts.rs_trig5_lit == 1
    assert ts.rs_trig4_lit == 1


def test_bot_b2_retreat_and_b3_utility() -> None:
    """B2 replie un pari Gardien orphelin en Mode 2 ; B3 valorise CAUSE_REVEIL_GARDIENS."""
    cfg = GameConfig(n_players=3, mode=2, peuples=("M", "R", "O"))
    st = GameState(cfg)
    st.tour = 2
    st.set_gardien_at_case(1, 1, face=1)
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(1, 1, 2, 3, 2, 0)
    st.set_player_hand(2, 3, 2, 4, 2, 0)
    st.place_defender_gardien_pari(0, 1, FACE_REFLEXION)
    st.place_defender_foret(1, 1, 1, 1, FACE_DEFINITIF)
    st.place_defender_foret(2, 1, 2, 1, FACE_DEFINITIF)
    st.step = STEP_2_2_DEF2

    resolve_step2_2_from_state(st, score_target_b2, k_max_passes=2)
    assert st.total_gardien_pari_engaged() == 0

    go_t8 = GameOver(tour_fin=8, cause_fin=CAUSE_TOUR_8, score_arbres=20, ratio_arbres=0.5)
    go_rev = GameOver(tour_fin=4, cause_fin=CAUSE_REVEIL_GARDIENS, score_arbres=20, ratio_arbres=0.5)
    go_som = GameOver(tour_fin=4, cause_fin=CAUSE_REVE_RANG_1, score_arbres=20, ratio_arbres=0.5)
    assert _gameover_utility(go_rev) > _gameover_utility(go_t8)
    assert _gameover_utility(go_rev) == _gameover_utility(go_som)


def test_calibration_mobilisation_croisee_manifest_and_digest_schema() -> None:
    """Vérifie le manifeste 2x2 calibration_mobilisation_croisee_v5_4.json et la purge v5.4.1 dans fins_5_3."""
    manifest_path = (
        ROOT / "campaigns" / "manifests" / "calibration_mobilisation_croisee_v5_4.json"
    )
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["player_counts"] == [3, 4, 5, 6]
    assert len(plan["profile_variants"]) == 4
    v_ids = {v["variant_id"] for v in plan["profile_variants"]}
    assert v_ids == {
        "POL=PARITY|ADV=JUMP_PUSH",
        "POL=PARITY|ADV=FREE_SLOT_ONLY",
        "POL=PARITY_CAP_ONIRIQUE|ADV=JUMP_PUSH",
        "POL=PARITY_CAP_ONIRIQUE|ADV=FREE_SLOT_ONLY",
    }
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 1 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 2 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 3 for u in plan["units"])

    # Vérification de la purge du reliquat v5.4.1 dans active_core_rules.spec_formelle.fins_5_3
    core_rules = build_active_core_rules(chassis_ids=(0,))
    fins_5_3 = str(core_rules["spec_formelle"]["fins_5_3"])
    assert "v5.4.1" not in fins_5_3
    assert "Gardien Face 2" not in fins_5_3
    assert "0 dommage réel" not in fins_5_3
    assert "mobilisation croisée" in fins_5_3.lower()

    # Exécution d'une micro-unité de 2 parties
    micro_unit = dict(plan["units"][0])
    micro_unit["n_games"] = 2
    row = _execute_manifest_unit(micro_unit)
    assert row["n_games"] == 2
    assert row["reveil_reves_policy"] in ("PARITY", "PARITY_CAP_ONIRIQUE")
    assert row["reve_advance_mode"] in ("JUMP_PUSH", "FREE_SLOT_ONLY")
    assert "rs_def_reve" in row
    assert "rs_reves_opened" in row
    assert "rs_trig5_lit" in row
    assert "rs_trig4_lit" in row


def test_digest_aggregator_cross_tabs_and_reveil_anatomy() -> None:
    """Vérifie by_variant_x_n_players, by_variant_x_n_animaux_sauvages et les nouveaux champs reveil_anatomy."""
    import gzip
    import shutil

    from run_campaign import _format_reveil_anatomy_row, aggregate_campaign_duckdb

    formatted = _format_reveil_anatomy_row(
        {
            "rs_count": 2,
            "rf_count": 1,
            "rs_tour": 8,
            "rs_ratio_arbres_bp": 15000,
            "rs_def_gardien": 5,
            "rs_def_reve": 3,
            "rs_reves_opened": 2,
            "rs_trig5_lit": 2,
            "rs_trig4_lit": 1,
            "rf_tour": 5,
            "rf_def_gardien": 2,
            "rf_def_reve": 1,
            "rf_reves_opened": 1,
            "rf_trig5_lit": 1,
            "rf_trig4_lit": 0,
        }
    )
    assert formatted["success_turn"]["defenders"]["mean_def_on_reve"] == 1.5
    assert formatted["success_turn"]["machine_attrition"]["mean_reves_opened"] == 1.0
    assert formatted["success_turn"]["machine_attrition"]["pct_trigger_5_reve_lit"] == 100.0
    assert formatted["success_turn"]["machine_attrition"]["pct_trigger_4_gardien_lit"] == 50.0
    assert formatted["failed_attempts_comparison"]["mean_def_on_reve"] == 1.0
    assert formatted["failed_attempts_comparison"]["mean_reves_opened"] == 1.0
    assert formatted["failed_attempts_comparison"]["pct_trigger_5_reve_lit"] == 100.0
    assert formatted["failed_attempts_comparison"]["pct_trigger_4_gardien_lit"] == 0.0

    # Micro-agrégation DuckDB bout-en-bout sur 2 variantes × N=3..4
    manifest = {
        "campaign_name": "test_mob_croisee_unit",
        "mode": 2,
        "bot": "B2",
        "k_max": 1,
        "seed": 12345,
        "player_counts": [3, 4],
        "table_selection": "PALIER1_DEFAULT",
        "min_animaux_sauvages": 1,
        "games_per_configuration": 2,
        "reve_activation_mode": "1_DEF_1_MACHINE",
        "reveil_reves_policies": ["PARITY", "PARITY_CAP_ONIRIQUE"],
        "reve_advance_modes": ["FREE_SLOT_ONLY"],
        "base_instance": {"config_index_192": 1},
        "chassis_plan": {"varying_axes": [], "fixed_axes": {}},
        "slot_profile_comparisons": {},
    }
    plan = resolve_manifest_plan(manifest)
    work_dir = ROOT / ".tmp_runs" / "test_mob_croisee_unit"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    shard_path = shards_dir / "shard_00.jsonl.gz"
    with gzip.open(shard_path, "wt", encoding="utf-8") as fh:
        for u in plan["units"]:
            r = _execute_manifest_unit(u)
            r["task_index"] = 0
            r["task_games"] = plan["total_games"]
            r["task_wall_sec"] = 0.1
            r["task_games_per_sec"] = 100.0
            fh.write(json.dumps(r) + "\n")

    digest_path = ROOT / "data" / "digests" / "digest_test_mob_croisee_unit.json"
    legacy_digest_path = ROOT / "data" / "digest_test_mob_croisee_unit.json"
    prompt_path = ROOT / "data" / "digests" / "PROMPT_GEMINI_test_mob_croisee_unit.md"
    try:
        _, _, digest = aggregate_campaign_duckdb(
            manifest=manifest,
            plan=plan,
            shards_dir=shards_dir,
            parquet_path=work_dir / "cells.parquet",
            backend="local",
            job_name="unit-test",
            tasks=1,
            job_wall_sec=0.1,
        )
        assert "by_variant_x_n_players" in digest
        assert len(digest["by_variant_x_n_players"]) == 4  # 2 variantes × 2 N
        assert "by_variant_x_n_animaux_sauvages" in digest
        assert len(digest["by_variant_x_n_animaux_sauvages"]) >= 2
    finally:
        for p in (digest_path, legacy_digest_path, prompt_path):
            if p.exists():
                p.unlink()
        if work_dir.exists():
            shutil.rmtree(work_dir)
