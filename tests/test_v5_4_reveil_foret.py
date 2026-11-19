"""Tests unitaires dédiés à la règle Réveil de la Forêt (v5.4.1)."""

from __future__ import annotations

import json
from pathlib import Path

from bots.belief_and_ticks import resolve_step2_2_from_state
from bots.bot_b3_rh import _gameover_utility
from bots.heuristic_engine import score_target_b2
from campaigns.worker_main import _execute_manifest_unit, resolve_manifest_plan
from engine.core_engine import (
    apply_step2_def2,
    list_legal_targets,
    lock_all_def2_in_place,
    resolve_single_machine_attack,
    step_until_decision,
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
    LISIERE_CONSTRUCTED,
    LISIERE_EJECTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    NUM_CHASSIS,
    STEP_2_2_DEF2,
    STEP_5_3_END_CHECK,
    STEP_6_3_END_TURN,
    TACTIQUES_SPEC,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parent.parent


def test_reveil_activation_and_hors_chassis_bijection() -> None:
    """Actif uniquement si >= 1 Animal Sauvage (M/R/O) et préserve NUM_CHASSIS == 384."""
    assert NUM_CHASSIS == 384

    cfg_no_animal = GameConfig(n_players=3, mode=2, peuples=("H", "E", "I"))
    assert cfg_no_animal.nb_animaux_sauvages == 0
    assert cfg_no_animal.reveil_quota == 0

    cfg_mode1 = GameConfig(n_players=4, mode=1, peuples=("M", "R", "O", "H"))
    assert cfg_mode1.nb_animaux_sauvages == 3
    assert cfg_mode1.reveil_quota == 0

    cfg_q_n = GameConfig(
        n_players=4, mode=2, peuples=("M", "H", "E", "I"), reveil_quota_mode="N"
    )
    assert cfg_q_n.nb_animaux_sauvages == 1
    assert cfg_q_n.reveil_quota == 4

    cfg_q_nm1 = GameConfig(
        n_players=4, mode=2, peuples=("M", "H", "E", "I"), reveil_quota_mode="N_MINUS_1"
    )
    assert cfg_q_nm1.reveil_quota == 3

    cfg_q_2 = GameConfig(
        n_players=5, mode=2, peuples=("M", "R", "H", "E", "I"), reveil_quota_mode="2"
    )
    assert cfg_q_2.reveil_quota == 2


def test_universal_face1_to_face2_and_g14_c_exception() -> None:
    """Tout Gardien ouvert en Face 1 passe Face 2 (Mode 2 neutre & Mode 3 monoface), sauf G14:C."""
    load_all_effects()

    # Mode 2 neutre : ouverture sur Face 1 -> Face 2
    cfg_m2 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"))
    st_m2 = GameState(cfg_m2)
    st_m2.set_gardien_at_case(1, 1, face=1, used=False)
    assert prim_partage_info_etat_gardien(st_m2, "MARK_GARDIEN_OPENED", case_1_6=1) is True
    assert st_m2.get_gardien_at_case(1) == (1, 2, True)

    # Mode 3 profil monoface (G7:A) : ouverture sur Face 1 -> Face 2
    cfg_mono = GameConfig(
        n_players=4, mode=3, peuples=("M", "H", "R", "O"), tile_profiles=(("G7", "A"),)
    )
    st_mono = GameState(cfg_mono)
    st_mono.set_gardien_at_case(2, 7, face=1, used=False)
    assert prim_partage_info_etat_gardien(st_mono, "MARK_GARDIEN_OPENED", case_1_6=2) is True
    assert st_mono.get_gardien_at_case(2) == (7, 2, True)

    # G14:C : sans Insecte chez R, reste Face 1 (À jeun) et n'est PAS éligible au Réveil
    cfg_g14 = GameConfig(
        n_players=4, mode=3, peuples=("R", "I", "M", "H"), tile_profiles=(("G14", "C"),)
    )
    st_g14 = GameState(cfg_g14)
    st_g14.set_gardien_at_case(3, 14, face=1, used=False)
    assert prim_partage_info_etat_gardien(st_g14, "MARK_GARDIEN_OPENED", case_1_6=3) is True
    assert st_g14.get_gardien_at_case(3) == (14, 1, True)
    st_g14.cleanup_end_of_turn_6_2()
    assert ("GARDIEN_REVEIL", 3) not in list_legal_targets(st_g14, 0, is_first_defender=False)

    # G14:C nourri -> passe Face 2 (Rassasié) et devient éligible au Réveil le tour suivant
    st_g14.set_parcel_insectes(0, 1, 1)
    assert prim_partage_info_etat_gardien(st_g14, "MARK_GARDIEN_OPENED", case_1_6=3) is True
    assert st_g14.get_gardien_at_case(3) == (14, 2, True)
    st_g14.cleanup_end_of_turn_6_2()
    assert ("GARDIEN_REVEIL", 3) in list_legal_targets(st_g14, 0, is_first_defender=False)


def test_step2_2_engagement_frees_case_and_orphans_have_no_effect() -> None:
    """Engagement au quota Q libère immédiatement la case 1..6 ; 0 < count < Q = orphelins sans effet."""
    cfg = GameConfig(
        n_players=4, mode=2, peuples=("M", "R", "O", "H"), reveil_quota_mode="N_MINUS_1"
    )
    assert cfg.reveil_quota == 3
    st = GameState(cfg)
    st.set_gardien_at_case(2, 1, face=2, used=False)
    st.set_gardien_at_case(5, 2, face=1, used=False)

    # 1er Défenseur ne peut jamais cibler GARDIEN_REVEIL ; Face 1 non éligible même pour 2e Défenseur
    assert ("GARDIEN_REVEIL", 2) not in list_legal_targets(st, 0, is_first_defender=True)
    assert ("GARDIEN_REVEIL", 2) in list_legal_targets(st, 0, is_first_defender=False)
    assert ("GARDIEN_REVEIL", 5) not in list_legal_targets(st, 0, is_first_defender=False)

    # Cas 1 : 0 < count < Q (2 sur 3) -> aucun Réveil engagé, Gardien reste sur la case 2
    st_orphan = st.clone()
    apply_step2_def2(st_orphan, 0, ("POSER_DEFINITIF", ("GARDIEN_REVEIL", 2)))
    apply_step2_def2(st_orphan, 1, ("POSER_DEFINITIF", ("GARDIEN_REVEIL", 2)))
    lock_all_def2_in_place(st_orphan)
    assert st_orphan.reveil_engaged_gardien == 0
    assert st_orphan.get_gardien_at_case(2) == (1, 2, False)

    # Cas 2 : count == Q (3 sur 3) -> Gardien retiré, case 2 immédiatement libre pour 3.1
    trk = TelemetryTracker()
    apply_step2_def2(st, 0, ("POSER_DEFINITIF", ("GARDIEN_REVEIL", 2)), telemetry=trk)
    apply_step2_def2(st, 1, ("POSER_DEFINITIF", ("GARDIEN_REVEIL", 2)), telemetry=trk)
    apply_step2_def2(st, 2, ("POSER_DEFINITIF", ("GARDIEN_REVEIL", 2)), telemetry=trk)
    # 4e joueur ne peut plus cibler la case 2 déjà pleine au quota Q
    assert ("GARDIEN_REVEIL", 2) not in list_legal_targets(st, 3, is_first_defender=False)
    lock_all_def2_in_place(st)
    assert st.reveil_engaged_gardien == 1
    assert st.get_gardien_at_case(2) == (0, 1, False)


def test_step5_3_success_vs_real_damage_route_and_6_3_fate() -> None:
    """5.3 déclenche Réveil si 0 dommage réel ; dommage réel (y compris Route->RETIRED) échoue et résout 6.3."""
    # A. Succès en 5.3 (0 dommage réel)
    cfg_ok = GameConfig(n_players=3, mode=2, peuples=("M", "R", "O"), reveil_quota_mode="2")
    st_ok = GameState(cfg_ok)
    st_ok.tour = 3
    st_ok.reveil_engaged_gardien = 1
    st_ok.real_damage_this_turn = False
    st_ok.step = STEP_5_3_END_CHECK
    res_ok = step_until_decision(st_ok)
    assert isinstance(res_ok, GameOver)
    assert res_ok.cause_fin == CAUSE_REVEIL_GARDIENS
    assert res_ok.tour_fin == 3

    # B. Échec suite à dommage réel entraînant création de Route et retrait de la machine (RETIRED)
    for fate, expected_status in (
        ("LISIERE_FACE_1", LISIERE_UNCONSTRUCTED),
        ("RETRAIT_DEFINITIF", LISIERE_EJECTED),
    ):
        cfg_fail = GameConfig(
            n_players=3,
            mode=2,
            peuples=("M", "R", "O"),
            reveil_quota_mode="2",
            reveil_gardien_fate=fate,
        )
        st = GameState(cfg_fail)
        g1_slot = st.find_lisiere_slot_by_tile_id("G1")
        assert g1_slot is not None
        st.set_lisiere_tile_state(g1_slot, LISIERE_CONSTRUCTED, 0)
        st.reveil_engaged_gardien = 1

        # Raser tout le rayon 0 sauf p=1 (1 Arbre, 0 Souche) -> Bulldozer rase p=1 et devient RETIRED !
        for p in range(2, cfg_fail.p_max + 1):
            st.set_parcel_arbres_souches(0, p, 0, 0)
        st.set_parcel_arbres_souches(0, 1, 1, 0)
        st.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)

        trk = TelemetryTracker()
        trk.on_reveil_attempt(st)
        resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1], telemetry=trk)
        assert st.get_machine_pos_status(0, MACHINE_BULLDOZER)[1] == MACHINE_STATUS_RETIRED
        assert st.real_damage_this_turn is True

        # En 5.3 : le Réveil échoue (ne termine pas la partie au Tour 1)
        st.step = STEP_5_3_END_CHECK
        st.tour = 1
        # Sauter directement en 6.3 pour vérifier le sort du Gardien et la télémétrie
        st.step = STEP_6_3_END_TURN
        step_until_decision(st, telemetry=trk)
        assert st.reveil_engaged_gardien == 0
        assert st.get_lisiere_tile_state(g1_slot)[0] == expected_status
        ts = trk.summary()
        assert ts.reveil_attempts == 1
        assert ts.reveil_failures == 1


def test_b2_clean_withdrawal_and_b3_utility() -> None:
    """B2 se retire proprement d'un Réveil incomplet en fin de réflexion ; B3 valorise Réveil à +0.03."""
    # B3 utility alignment
    go_rev = GameOver(tour_fin=4, cause_fin=CAUSE_REVEIL_GARDIENS, score_arbres=20, ratio_arbres=0.5)
    go_som = GameOver(tour_fin=4, cause_fin=CAUSE_REVE_RANG_1, score_arbres=20, ratio_arbres=0.5)
    go_t8 = GameOver(tour_fin=8, cause_fin=CAUSE_TOUR_8, score_arbres=20, ratio_arbres=0.5)
    assert _gameover_utility(go_rev) == _gameover_utility(go_som)
    assert _gameover_utility(go_rev) > _gameover_utility(go_t8)

    # B2 : 1 seul joueur en réflexion sur GARDIEN_REVEIL alors que Q=3 -> retrait propre avant verrouillage
    cfg = GameConfig(n_players=3, mode=2, peuples=("M", "R", "O"), reveil_quota_mode="N")
    st = GameState(cfg)
    st.tour = 3
    st.set_gardien_at_case(1, 1, face=2, used=False)
    for s in range(3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        st.place_defender_foret(s, 0, s, 1, 2)
    # Siège 0 pose en réflexion sur GARDIEN_REVEIL, sièges 1 et 2 verrouillés en forêt (ne peuvent pas rejoindre)
    st.place_defender_gardien_reveil(0, 1, 1)
    st.place_defender_foret(1, 1, 1, 2, 2)
    st.place_defender_foret(2, 1, 2, 2, 2)
    st.step = STEP_2_2_DEF2

    resolve_step2_2_from_state(st, score_target_b2, k_max_passes=2)
    # Siège 0 doit s'être retiré proprement (aucun orphelin laissé sur GARDIEN_REVEIL)
    assert st.count_reveil_defenders_at_case(1) == 0
    assert st.reveil_engaged_gardien == 0


def test_calibration_reveil_manifest_resolution_and_micro_unit() -> None:
    """Le manifeste calibration_reveil_v5_4.json résout exactement 6 châssis × 6 variantes × N=3..6 (A>=1)."""
    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_reveil_v5_4.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["player_counts"] == [3, 4, 5, 6]
    assert len(plan["profile_variants"]) == 6
    assert plan["total_configurations"] == 4 * 6 * 6
    assert all(int(u["n_animaux_sauvages"]) >= 1 for u in plan["units"])

    # Exécuter une micro-unité (1 partie) pour vérifier les nouvelles colonnes de télémétrie
    micro_unit = dict(plan["units"][0])
    micro_unit["n_games"] = 1
    row = _execute_manifest_unit(micro_unit)
    assert "count_reveil_attempts" in row
    assert "count_reveil_failures" in row
    assert "n_animaux_sauvages" in row
    assert row["reveil_quota_mode"] in ("N", "N_MINUS_1", "2")
    assert row["reveil_gardien_fate"] in ("LISIERE_FACE_1", "RETRAIT_DEFINITIF")
