"""Tests unitaires v5.4.5 : Plafond pari Gardiens max 2 (UNIFORM_MAX_2 vs MAX_2_RES_MAX_1),
échec partiel pari à 2 Défenseurs, Éveil 100 % Gardiens (rejet si Défenseur sur Rêve),
avancée des Rêves CLEAR_RANK_ONLY vs JUMP_PUSH, télémétrie & manifeste calibration_pari_max2_v5_4.
"""

from __future__ import annotations

import gzip
import json
import shutil
from pathlib import Path

import pytest

from bots.belief_and_ticks import resolve_step2_2_from_state
from bots.bot_b3_rh import _gameover_utility
from bots.heuristic_engine import score_target_b2
from campaigns.digest_builder import build_active_core_rules
from campaigns.worker_main import _execute_manifest_unit, resolve_manifest_plan
from engine.core_engine import (
    _run_step_3_2,
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


def test_gardien_bet_cap_uniform_max_2_vs_max_2_res_max_1() -> None:
    """UNIFORM_MAX_2 autorise max 2 Défenseurs sur 1..6 (dont case 4) ; MAX_2_RES_MAX_1 plafonne case 4 à 1."""
    assert NUM_CHASSIS == 192

    # Sans Animal Sauvage (H, E, I) : cible GARDIEN_PARI interdite
    cfg_no_animal = GameConfig(n_players=3, mode=2, peuples=("H", "E", "I"))
    assert cfg_no_animal.nb_animaux_sauvages == 0
    st_no = GameState(cfg_no_animal)
    st_no.set_gardien_at_case(1, 1, face=1)
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_no, 0, is_first_defender=False)

    # Mode 1 : interdit même avec Animaux Sauvages
    cfg_m1 = GameConfig(n_players=4, mode=1, peuples=("M", "R", "O", "H"))
    st_m1 = GameState(cfg_m1)
    st_m1.set_gardien_at_case(1, 1, face=1)
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_m1, 0, is_first_defender=False)

    # 1. UNIFORM_MAX_2 : max 2 sur cases 1..6 y compris case 4, 3e interdit
    cfg_u2 = GameConfig(
        n_players=5,
        mode=2,
        peuples=("M", "R", "O", "H", "I"),
        gardien_bet_cap_policy="UNIFORM_MAX_2",
    )
    st_u2 = GameState(cfg_u2)
    for c in range(1, 7):
        st_u2.set_gardien_at_case(c, c, face=1)

    # 1er Défenseur ne peut jamais cibler GARDIEN_PARI
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_u2, 0, is_first_defender=True)
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st_u2, 0, is_first_defender=True)

    # Pose de 2 Défenseurs sur case 1 et 2 Défenseurs sur case 4 -> légal en UNIFORM_MAX_2
    apply_step2_def2(st_u2, 0, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert ("GARDIEN_PARI", 1) in list_legal_targets(st_u2, 1, is_first_defender=False)
    apply_step2_def2(st_u2, 1, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_u2, 2, is_first_defender=False)

    apply_step2_def2(st_u2, 2, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert ("GARDIEN_PARI", 4) in list_legal_targets(st_u2, 3, is_first_defender=False)
    apply_step2_def2(st_u2, 3, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st_u2, 4, is_first_defender=False)

    with pytest.raises(AssertionError):
        st_u2.place_defender_gardien_pari(4, 1, FACE_DEFINITIF)
    with pytest.raises(AssertionError):
        st_u2.place_defender_gardien_pari(4, 4, FACE_DEFINITIF)

    # 2. MAX_2_RES_MAX_1 : max 2 sur 1,2,3,5,6 mais max 1 sur case 4 (4. Gardien)
    cfg_r1 = GameConfig(
        n_players=5,
        mode=2,
        peuples=("M", "R", "O", "H", "I"),
        gardien_bet_cap_policy="MAX_2_RES_MAX_1",
    )
    st_r1 = GameState(cfg_r1)
    for c in range(1, 7):
        st_r1.set_gardien_at_case(c, c, face=1)

    # Case 1 accepte bien 2 Défenseurs
    apply_step2_def2(st_r1, 0, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert ("GARDIEN_PARI", 1) in list_legal_targets(st_r1, 1, is_first_defender=False)
    apply_step2_def2(st_r1, 1, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert ("GARDIEN_PARI", 1) not in list_legal_targets(st_r1, 2, is_first_defender=False)

    # Case 4 plafonnée à 1 seul Défenseur
    apply_step2_def2(st_r1, 2, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st_r1, 3, is_first_defender=False)
    with pytest.raises(AssertionError):
        st_r1.place_defender_gardien_pari(3, 4, FACE_DEFINITIF)


def test_gardien_two_def_antiloop_and_partial_failure_returns_lisiere() -> None:
    """2 Déf sur case 1 + 2 Déf sur case 4 (anti-boucle 4) ; échec partiel (1/2 déclenchements) -> retour lisière Face 1."""
    load_all_effects()

    # 1. Double déclenchement + anti-boucle 4. Gardien en UNIFORM_MAX_2
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        gardien_bet_cap_policy="UNIFORM_MAX_2",
    )
    st = GameState(cfg)
    st.set_gardien_at_case(1, 1, face=1)
    st.set_gardien_at_case(4, 2, face=1)

    # 0 Défenseur -> inactif
    st.light_trigger(1)
    assert sweep_gardiens(st) == 0

    # 2 Défenseurs sur case 1 et 2 Défenseurs sur case 4
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, 4, FACE_DEFINITIF)

    # 1er déclenchement case 1 : ouvre case 1 (1 consommé, 1 restant) -> allume 4 -> ouvre case 4 (1 consommé, 1 restant) -> anti-boucle : 4 éteinte !
    st.light_trigger(1)
    assert sweep_gardiens(st) == 2
    assert st.count_gardien_pari_defenders_at_case(1) == 1
    assert st.count_gardien_pari_consumed_at_case(1) == 1
    assert st.count_gardien_pari_defenders_at_case(4) == 1
    assert st.count_gardien_pari_consumed_at_case(4) == 1
    assert not st.is_trigger_lit(4)

    # 2e déclenchement case 1 : consomme le 2e Défenseur sur case 1, mais sous v5.4.6 DISTINCT_OPEN_1
    # une 2e ouverture du même autre Gardien ne ré-allume PAS 4. Gardien !
    st.light_trigger(1)
    assert sweep_gardiens(st) == 1
    assert st.count_gardien_pari_defenders_at_case(1) == 0
    assert st.count_gardien_pari_consumed_at_case(1) == 2
    assert st.count_gardien_pari_defenders_at_case(4) == 1
    assert st.count_gardien_pari_consumed_at_case(4) == 1

    # Un 2e autre Gardien distinct (case 2) qui s'ouvre pour la 1re fois du tour allume 4. Gardien !
    st.set_gardien_at_case(2, 3, face=1)
    st.set_player_def_loc_raw(0, 1, 0)
    st.place_defender_gardien_pari(0, 2, FACE_DEFINITIF)
    st.light_trigger(2)
    assert sweep_gardiens(st) == 2
    assert st.count_gardien_pari_defenders_at_case(4) == 0
    assert st.count_gardien_pari_consumed_at_case(4) == 2
    assert not st.is_trigger_lit(4)

    # 2. Échec partiel d'un pari à 2 Défenseurs : 1 seul déclenchement -> 1 Défenseur restant -> retour immédiat en lisière Face 1
    st_part = GameState(cfg)
    st_part.tour = 2
    g1_slot = st_part.find_lisiere_slot_by_tile_id("G1")
    g2_slot = st_part.find_lisiere_slot_by_tile_id("G2")
    assert g1_slot is not None and g2_slot is not None
    st_part.set_lisiere_tile_state(g1_slot, LISIERE_CONSTRUCTED, 0)
    st_part.set_lisiere_tile_state(g2_slot, LISIERE_CONSTRUCTED, 0)
    st_part.set_gardien_at_case(1, 1, face=1)
    st_part.set_gardien_at_case(2, 2, face=1)
    # 2 Défenseurs sur case 1 (G1), 1 Défenseur sur case 2 (G2)
    st_part.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_part.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st_part.place_defender_gardien_pari(2, 2, FACE_DEFINITIF)

    # 1 seul déclenchement sur case 1 (échec partiel : 1 consommé, 1 restant) et 1 sur case 2 (gagné : 1 consommé, 0 restant)
    assert prim_partage_info_etat_gardien(st_part, "MARK_GARDIEN_OPENED", case_1_6=1) is True
    assert prim_partage_info_etat_gardien(st_part, "MARK_GARDIEN_OPENED", case_1_6=2) is True
    assert st_part.count_gardien_pari_defenders_at_case(1) == 1
    assert st_part.count_gardien_pari_consumed_at_case(1) == 1

    trk = TelemetryTracker()
    st_part.step = STEP_5_3_END_CHECK
    step_until_decision(st_part, telemetry=trk)
    # G1 (échec partiel 1/2) retourne immédiatement en lisière Face 1 ; G2 (1/1) reste en piste
    assert st_part.get_gardien_at_case(1) == (0, 1)
    assert st_part.get_lisiere_tile_state(g1_slot)[0] == LISIERE_UNCONSTRUCTED
    assert st_part.get_gardien_at_case(2) == (2, 1)
    ts = trk.summary()
    assert ts.gardien_bets_won == 1
    assert ts.gardien_bets_lost == 1


def test_eveil_100_pourcent_gardiens_rejet_reve_et_priorite_tour8() -> None:
    """Éveil 100 % Gardiens : réussit si les N Défenseurs sont sur Gardiens et 0 restant ; rejeté si >= 1 sur Rêve."""
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        gardien_bet_cap_policy="UNIFORM_MAX_2",
    )

    # Cas A : 3 Défenseurs sur Gardiens + 1 Défenseur sur un Rêve (même si le Rêve annule 1 machine !) -> Éveil REJETÉ !
    st_rej = GameState(cfg)
    st_rej.tour = 3
    st_rej.set_gardien_at_case(1, 1, face=1)
    st_rej.set_gardien_at_case(4, 2, face=1)
    st_rej.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 sur case 6
    st_rej.set_player_hand(0, 1, 6, 6, 6, 0)  # Machine sur case 6
    st_rej.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st_rej.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_rej.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)

    st_rej.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_rej.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st_rej.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_rej.place_defender_reve_activation(3, 6, FACE_DEFINITIF)

    assert st_rej.is_eveil_attempt_eligible() is False
    st_rej.step = STEP_3_2_REVEAL
    _run_step_3_2(st_rej)
    assert st_rej.total_reve_activation_consumed() == 1
    assert st_rej.total_reve_activation_remaining() == 0
    st_rej.light_trigger(1)
    sweep_gardiens(st_rej)
    st_rej.light_trigger(1)
    sweep_gardiens(st_rej)
    assert st_rej.total_gardien_pari_consumed() == 3
    assert st_rej.total_gardien_pari_remaining() == 0
    # Rejeté car seulement 3/4 Défenseurs sur la Piste des Gardiens (1 était sur un Rêve)
    assert st_rej.is_eveil_gardiens_victory() is False
    st_rej.step = STEP_5_3_END_CHECK
    res_rej = step_until_decision(st_rej)
    assert not isinstance(res_rej, GameOver)

    # Cas B : les N=4 Défenseurs engagés sur la Piste des Gardiens (1 sur case 1, 1 sur case 2, 2 sur case 4) -> Éveil RÉUSSI + télémétrie !
    st_ok = GameState(cfg)
    st_ok.tour = 3
    st_ok.set_gardien_at_case(1, 1, face=1)
    st_ok.set_gardien_at_case(2, 3, face=1)
    st_ok.set_gardien_at_case(4, 2, face=1)
    for s in range(4):
        st_ok.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_ok.place_defender_gardien_pari(0, 1, FACE_REFLEXION)
    st_ok.place_defender_gardien_pari(1, 2, FACE_REFLEXION)
    st_ok.place_defender_gardien_pari(2, 4, FACE_REFLEXION)
    st_ok.place_defender_gardien_pari(3, 4, FACE_REFLEXION)

    trk = TelemetryTracker()
    lock_all_def2_in_place(st_ok)
    assert st_ok.is_eveil_attempt_eligible() is True
    trk.on_reveil_attempt(st_ok)

    # 2 Gardiens distincts (case 1 puis case 2) -> consomment 1 Déf sur 1, 1 Déf sur 2 et les 2 Déf sur 4
    st_ok.light_trigger(1)
    sweep_gardiens(st_ok, telemetry=trk)
    st_ok.light_trigger(2)
    sweep_gardiens(st_ok, telemetry=trk)
    assert st_ok.total_gardien_pari_consumed() == 4
    assert st_ok.total_gardien_pari_remaining() == 0
    assert st_ok.is_eveil_gardiens_victory() is True

    trk.on_step_transition(st_ok, STEP_2_2_DEF2, STEP_5_1_TACTIQUES)
    st_ok.step = STEP_5_3_END_CHECK
    res_ok = step_until_decision(st_ok, telemetry=trk)
    assert isinstance(res_ok, GameOver)
    assert res_ok.cause_fin == CAUSE_REVEIL_GARDIENS

    ts = trk.summary()
    assert ts.rs_count == 1
    assert ts.rs_def_gardien == 4
    assert ts.rs_def_parade == 1
    assert ts.rs_def_resonance == 2
    assert ts.rs_distinct_gardiens_bet == 3
    assert ts.rs_def_reve == 0
    assert ts.rs_trig4_lit == 1

    # Cas C : Priorité absolue à CAUSE_TOUR_8 au Tour 8
    st_t8 = GameState(cfg)
    st_t8.tour = 8
    st_t8.set_gardien_at_case(1, 1, face=1)
    st_t8.set_gardien_at_case(4, 2, face=1)
    st_t8.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(3, 4, FACE_DEFINITIF)
    st_t8.light_trigger(1)
    sweep_gardiens(st_t8)
    st_t8.light_trigger(1)
    sweep_gardiens(st_t8)
    st_t8.step = STEP_5_3_END_CHECK
    res_t8 = step_until_decision(st_t8)
    assert isinstance(res_t8, GameOver)
    assert res_t8.cause_fin == CAUSE_TOUR_8


def test_reve_advance_mode_clear_rank_only_vs_jump_push() -> None:
    """CLEAR_RANK_ONLY : 1/2 machine annulée -> Rêve s'ouvre (5. Rêve) mais n'avance pas ; 2/2 -> avance (saut/poussée)."""
    # 1. CLEAR_RANK_ONLY : 2 machines au rang 6 (R3), 1 seul Défenseur sur R3 -> 1/2 annulée
    cfg_cr = GameConfig(
        n_players=3,
        mode=2,
        peuples=("M", "H", "I"),
        reve_activation_mode="1_DEF_1_MACHINE",
        reve_advance_mode="CLEAR_RANK_ONLY",
    )
    st_partial = GameState(cfg_cr)
    st_partial.set_gardien_at_case(5, 1, face=1)
    st_partial.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 sur case 6
    st_partial.set_player_hand(0, 1, 6, 6, 6, 0)  # Machine 1 sur case 6
    st_partial.set_player_hand(1, 3, 6, 6, 6, 0)  # Machine 2 sur case 6
    st_partial.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_partial.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_partial.place_defender_gardien_pari(2, 5, FACE_DEFINITIF)

    st_partial.step = STEP_3_2_REVEAL
    _run_step_3_2(st_partial)
    # R3 s'est ouvert (5. Rêve allumé -> Gardien case 5 ouvert, 1 machine annulée, 1 machine passée sous le Rêve)
    assert st_partial.has_reve_opened_this_turn(3) is True
    assert st_partial.count_gardien_pari_consumed_at_case(5) == 1
    assert st_partial.total_reve_activation_consumed() == 1
    assert st_partial.total_reve_activation_remaining() == 0
    # 1 machine annulée (bound_tact == 0), 1 machine passée sous le Rêve (bound_tact == 6)
    bound_vals = sorted([st_partial.get_player_hand(0)[4], st_partial.get_player_hand(1)[4]])
    assert bound_vals == [0, 6]
    # Mais R3 N'A PAS AVANCÉ car 1 machine est passée sous le Rêve !
    assert st_partial.get_tactique_at_rank(5) == TILE_R_BASE + 3
    assert st_partial.get_tactique_at_rank(4) == 5  # T5 intacte

    # 2. CLEAR_RANK_ONLY : 2/2 machines annulées au rang 6 (avec R1 en case 5 pour tester saut/poussée) -> R3 s'ouvre ET avance !
    st_full = GameState(cfg_cr)
    st_full.set_gardien_at_case(5, 1, face=1)
    st_full.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 sur case 5
    st_full.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 sur case 6
    st_full.set_player_hand(0, 1, 6, 6, 6, 0)
    st_full.set_player_hand(1, 3, 6, 6, 6, 0)
    st_full.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_full.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_full.place_defender_reve_activation(1, 6, FACE_DEFINITIF)
    st_full.place_defender_gardien_pari(2, 5, FACE_DEFINITIF)

    st_full.step = STEP_3_2_REVEAL
    _run_step_3_2(st_full)
    assert st_full.has_reve_opened_this_turn(3) is True
    assert st_full.count_gardien_pari_consumed_at_case(5) == 1
    assert st_full.total_reve_activation_consumed() == 2
    assert st_full.get_player_hand(0)[4] == 0
    assert st_full.get_player_hand(1)[4] == 0
    # Toutes les machines du rang 6 annulées -> saut/poussée vers la 1re case libre à gauche (cases 4..5) !
    assert st_full.get_tactique_at_rank(3) == TILE_R_BASE + 1
    assert st_full.get_tactique_at_rank(4) == TILE_R_BASE + 3
    assert st_full.get_tactique_at_rank(5) == 6  # T6 restaurée

    # 3. Témoin JUMP_PUSH : 1/2 machine annulée -> R3 s'ouvre ET avance immédiatement
    cfg_jp = GameConfig(
        n_players=3,
        mode=2,
        peuples=("M", "H", "I"),
        reve_activation_mode="1_DEF_1_MACHINE",
        reve_advance_mode="JUMP_PUSH",
    )
    st_jp = GameState(cfg_jp)
    st_jp.set_tactique_at_rank(5, TILE_R_BASE + 3)
    st_jp.set_player_hand(0, 1, 6, 6, 6, 0)
    st_jp.set_player_hand(1, 3, 6, 6, 6, 0)
    st_jp.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_jp.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_jp.step = STEP_3_2_REVEAL
    _run_step_3_2(st_jp)
    assert st_jp.get_tactique_at_rank(4) == TILE_R_BASE + 3
    assert st_jp.get_tactique_at_rank(5) == 6


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


def test_calibration_pari_max2_manifest_and_digest_schema() -> None:
    """Vérifie le manifeste 2x2 calibration_pari_max2_v5_4.json et active_core_rules v5.4.5."""
    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_pari_max2_v5_4.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["player_counts"] == [3, 4, 5, 6]
    assert len(plan["profile_variants"]) == 4
    v_ids = {v["variant_id"] for v in plan["profile_variants"]}
    assert v_ids == {
        "CAP=UNIFORM_MAX_2|ADV=JUMP_PUSH",
        "CAP=UNIFORM_MAX_2|ADV=CLEAR_RANK_ONLY",
        "CAP=MAX_2_RES_MAX_1|ADV=JUMP_PUSH",
        "CAP=MAX_2_RES_MAX_1|ADV=CLEAR_RANK_ONLY",
    }
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 1 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 2 for u in plan["units"])
    assert any(u["n_animaux_sauvages"] == 3 for u in plan["units"])

    # Vérification active_core_rules.spec_formelle.fins_5_3 v5.4.5
    core_rules = build_active_core_rules(chassis_ids=(0,))
    fins_5_3 = str(core_rules["spec_formelle"]["fins_5_3"])
    assert "v5.4.1" not in fins_5_3
    assert "Gardien Face 2" not in fins_5_3
    assert "mobilisation croisée" not in fins_5_3.lower()
    assert "100 % piste des gardiens" in fins_5_3.lower()

    # Exécution d'une micro-unité de 2 parties
    micro_unit = dict(plan["units"][0])
    micro_unit["n_games"] = 2
    row = _execute_manifest_unit(micro_unit)
    assert row["n_games"] == 2
    assert row["gardien_bet_cap_policy"] in ("UNIFORM_MAX_2", "MAX_2_RES_MAX_1")
    assert row["reve_advance_mode"] in ("JUMP_PUSH", "CLEAR_RANK_ONLY")
    assert "rs_def_parade" in row
    assert "rs_distinct_gardiens_bet" in row
    assert "rs_def_resonance" in row
    assert "rs_trig4_lit" in row


def test_digest_aggregator_cross_tabs_and_reveil_anatomy() -> None:
    """Vérifie by_variant_x_n_players, by_variant_x_n_animaux_sauvages et les champs reveil_anatomy v5.4.5."""
    from run_campaign import _format_reveil_anatomy_row, aggregate_campaign_duckdb

    formatted = _format_reveil_anatomy_row(
        {
            "rs_count": 2,
            "rf_count": 1,
            "rs_tour": 8,
            "rs_ratio_arbres_bp": 15000,
            "rs_def_gardien": 8,
            "rs_def_parade": 3,
            "rs_def_resonance": 2,
            "rs_distinct_gardiens_bet": 5,
            "rs_def_reve": 0,
            "rs_reves_opened": 0,
            "rs_trig5_lit": 0,
            "rs_trig4_lit": 2,
            "rf_tour": 5,
            "rf_def_gardien": 4,
            "rf_def_parade": 2,
            "rf_def_resonance": 1,
            "rf_distinct_gardiens_bet": 3,
            "rf_def_reve": 0,
            "rf_reves_opened": 0,
            "rf_trig5_lit": 0,
            "rf_trig4_lit": 1,
        }
    )
    assert formatted["success_turn"]["defenders"]["mean_def_on_parade"] == 1.5
    assert formatted["success_turn"]["defenders"]["mean_def_on_resonance"] == 1.0
    assert formatted["success_turn"]["defenders"]["mean_distinct_gardiens_bet"] == 2.5
    assert formatted["success_turn"]["machine_attrition"]["pct_trigger_4_gardien_lit"] == 100.0
    assert formatted["failed_attempts_comparison"]["mean_def_on_parade"] == 2.0
    assert formatted["failed_attempts_comparison"]["mean_def_on_resonance"] == 1.0
    assert formatted["failed_attempts_comparison"]["mean_distinct_gardiens_bet"] == 3.0
    assert formatted["failed_attempts_comparison"]["pct_trigger_4_gardien_lit"] == 100.0

    # Micro-agrégation DuckDB bout-en-bout sur 2 variantes × N=3..4
    manifest = {
        "campaign_name": "test_pari_max2_unit",
        "mode": 2,
        "bot": "B2",
        "k_max": 1,
        "seed": 12345,
        "player_counts": [3, 4],
        "table_selection": "PALIER1_DEFAULT",
        "min_animaux_sauvages": 1,
        "games_per_configuration": 2,
        "reve_activation_mode": "1_DEF_1_MACHINE",
        "gardien_bet_cap_policies": ["UNIFORM_MAX_2", "MAX_2_RES_MAX_1"],
        "reve_advance_modes": ["CLEAR_RANK_ONLY"],
        "base_instance": {"config_index_192": 1},
        "chassis_plan": {"varying_axes": [], "fixed_axes": {}},
        "slot_profile_comparisons": {},
    }
    plan = resolve_manifest_plan(manifest)
    work_dir = ROOT / ".tmp_runs" / "test_pari_max2_unit"
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

    digest_path = ROOT / "data" / "digests" / "digest_test_pari_max2_unit.json"
    legacy_digest_path = ROOT / "data" / "digest_test_pari_max2_unit.json"
    prompt_path = ROOT / "data" / "digests" / "PROMPT_GEMINI_test_pari_max2_unit.md"
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
        assert "by_variant_x_n_animaux_sauvages" in digest
        assert len(digest["by_variant_x_n_players"]) == 4  # 2 variantes × N in {3, 4}
        assert len(digest["by_variant_x_n_animaux_sauvages"]) >= 2
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
        for p in (digest_path, legacy_digest_path, prompt_path):
            if p.exists():
                p.unlink()
