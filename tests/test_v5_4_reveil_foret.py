"""Tests unitaires dédiés au Pari d'activation des Gardiens & Éveil de la Forêt (v5.4.3)."""

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
    STEP_5_1_TACTIQUES,
    STEP_5_3_END_CHECK,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parent.parent


def test_pari_gardiens_activation_and_hors_chassis_bijection() -> None:
    """Actif uniquement si >= 1 Animal Sauvage (M/R/O), bijection 192/192 et cap 4. Résonance."""
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

    # UNLIMITED : cumul autorisé sur 4. Résonance
    cfg_unlim = GameConfig(
        n_players=4, mode=2, peuples=("M", "R", "O", "H"), gardien_resonance_cap="UNLIMITED"
    )
    st_u = GameState(cfg_unlim)
    st_u.set_gardien_at_case(4, 2, face=1)
    # 1er Défenseur ne peut jamais cibler GARDIEN_PARI
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st_u, 0, is_first_defender=True)
    assert ("GARDIEN_PARI", 4) in list_legal_targets(st_u, 0, is_first_defender=False)
    apply_step2_def2(st_u, 0, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert ("GARDIEN_PARI", 4) in list_legal_targets(st_u, 1, is_first_defender=False)
    apply_step2_def2(st_u, 1, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert st_u.count_gardien_pari_defenders_at_case(4) == 2

    # MAX_1_DEF : plafond 1 seul 2e Défenseur sur 4. Résonance (mais cumul libre sur les autres cases)
    cfg_cap = GameConfig(
        n_players=4, mode=2, peuples=("M", "R", "O", "H"), gardien_resonance_cap="MAX_1_DEF"
    )
    st_c = GameState(cfg_cap)
    st_c.set_gardien_at_case(1, 1, face=1)
    st_c.set_gardien_at_case(4, 2, face=1)
    apply_step2_def2(st_c, 0, ("POSER_DEFINITIF", ("GARDIEN_PARI", 4)))
    assert ("GARDIEN_PARI", 4) not in list_legal_targets(st_c, 1, is_first_defender=False)
    # Cumul toujours autorisé sur case 1
    apply_step2_def2(st_c, 1, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert ("GARDIEN_PARI", 1) in list_legal_targets(st_c, 2, is_first_defender=False)
    apply_step2_def2(st_c, 2, ("POSER_DEFINITIF", ("GARDIEN_PARI", 1)))
    assert st_c.count_gardien_pari_defenders_at_case(1) == 2


def test_gardien_zero_def_inactive_multi_activation_and_resonance_antiloop() -> None:
    """0 Déf = inactif ; X Défs = X activations ; anti-boucle stricte sur 4. Résonance."""
    cfg = GameConfig(
        n_players=4, mode=2, peuples=("M", "R", "O", "H"), gardien_resonance_cap="UNLIMITED"
    )
    st = GameState(cfg)
    st.set_gardien_at_case(1, 1, face=1)
    st.set_gardien_at_case(4, 2, face=1)

    # Sans Défenseur : inactif !
    st.light_trigger(1)
    assert sweep_gardiens(st) == 0

    # 2 Défenseurs sur case 1, 2 Défenseurs sur case 4 (Résonance)
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, 4, FACE_DEFINITIF)

    # 1er déclenchement case 1 : ouvre case 1 (1 restant) -> allume 4 -> ouvre case 4 (1 restant)
    # ANTI-BOUCLE : l'ouverture de 4 ne ré-allume PAS 4 !
    st.light_trigger(1)
    opened_1 = sweep_gardiens(st)
    assert opened_1 == 2
    assert st.count_gardien_pari_defenders_at_case(1) == 1
    assert st.count_gardien_pari_consumed_at_case(1) == 1
    assert st.count_gardien_pari_defenders_at_case(4) == 1
    assert st.count_gardien_pari_consumed_at_case(4) == 1

    # 2e déclenchement case 1 : consomme le 2e Défenseur sur 1 et le 2e sur 4
    st.light_trigger(1)
    opened_2 = sweep_gardiens(st)
    assert opened_2 == 2
    assert st.count_gardien_pari_defenders_at_case(1) == 0
    assert st.count_gardien_pari_defenders_at_case(4) == 0

    # 3e déclenchement case 1 : 0 Défenseur restant -> plus aucune ouverture
    st.light_trigger(1)
    assert sweep_gardiens(st) == 0


def test_step5_3_bet_won_upgrade_vs_bet_lost_return_lisiere() -> None:
    """En 5.3 : pari gagné reste (Face 2 en Mode 3/4 si double-face) ; pari perdu retourne en lisière Face 1."""
    load_all_effects()

    # Mode 2 neutre : pas de passage Face 2 même si pari gagné
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
    # Seule la case 1 s'ouvre (pari gagné), case 2 non ouverte (pari perdu)
    assert prim_partage_info_etat_gardien(st_m2, "MARK_GARDIEN_OPENED", case_1_6=1) is True
    assert st_m2.get_gardien_at_case(1) == (1, 1)  # Pas de flip à l'ouverture

    trk = TelemetryTracker()
    st_m2.step = STEP_5_3_END_CHECK
    step_until_decision(st_m2, telemetry=trk)
    # Case 1 (pari gagné) reste en piste Face 1 (Mode 2 neutre)
    assert st_m2.get_gardien_at_case(1) == (1, 1)
    # Case 2 (pari perdu) retournée en lisière Face 1
    assert st_m2.get_gardien_at_case(2) == (0, 1)
    assert st_m2.get_lisiere_tile_state(g2_slot)[0] == LISIERE_UNCONSTRUCTED
    ts = trk.summary()
    assert ts.gardien_bets_won == 1
    assert ts.gardien_bets_lost == 1

    # Mode 3/4 : Gardien double-face (G1:A) passe Face 2 en 5.3 si pari gagné (et pas à l'ouverture)
    cfg_m3 = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G1", "A"), ("G7", "A")),
    )
    st_m3 = GameState(cfg_m3)
    st_m3.tour = 2
    st_m3.set_gardien_at_case(1, 1, face=1)  # G1:A (double-face)
    st_m3.set_gardien_at_case(3, 7, face=1)  # G7:A (monoface)
    st_m3.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_m3.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    assert prim_partage_info_etat_gardien(st_m3, "MARK_GARDIEN_OPENED", case_1_6=1) is True
    assert prim_partage_info_etat_gardien(st_m3, "MARK_GARDIEN_OPENED", case_1_6=3) is True
    assert st_m3.get_gardien_at_case(1) == (1, 1)  # Encore Face 1 avant 5.3 !
    assert st_m3.get_gardien_at_case(3) == (7, 1)

    st_m3.step = STEP_5_3_END_CHECK
    step_until_decision(st_m3)
    assert st_m3.get_gardien_at_case(1) == (1, 2)  # G1:A promu en Face 2 en 5.3 !
    assert st_m3.get_gardien_at_case(3) == (7, 1)  # G7:A monoface reste Face 1 !


def test_eveil_de_la_foret_and_tour8_priority() -> None:
    """Éveil de la Forêt aux Tours 1..7 si N 2es Défenseurs engagés et tous paris gagnés ; Tour 8 prioritaire."""
    # A. Éveil réussi au Tour 3 (réparti sur case 1 et case 4. Résonance)
    cfg = GameConfig(
        n_players=3, mode=2, peuples=("M", "R", "O"), gardien_resonance_cap="UNLIMITED"
    )
    st = GameState(cfg)
    st.tour = 3
    st.set_gardien_at_case(1, 1, face=1)
    st.set_gardien_at_case(4, 2, face=1)
    st.place_defender_gardien_pari(0, 1, FACE_REFLEXION)
    st.place_defender_gardien_pari(1, 1, FACE_REFLEXION)
    st.place_defender_gardien_pari(2, 4, FACE_REFLEXION)

    trk = TelemetryTracker()
    lock_all_def2_in_place(st)
    # Simuler on_reveil_attempt + snapshot pre5 comme dans le flux normal
    trk.on_reveil_attempt(st)
    trk.on_step_transition(st, STEP_2_2_DEF2, STEP_5_1_TACTIQUES)

    # 2 Parades -> 2 ouvertures de case 1 + 1 ouverture de case 4 -> 0 restant !
    st.light_trigger(1)
    sweep_gardiens(st, telemetry=trk)
    st.light_trigger(1)
    sweep_gardiens(st, telemetry=trk)
    assert st.total_gardien_pari_remaining() == 0
    assert st.total_gardien_pari_engaged() == 3

    st.step = STEP_5_3_END_CHECK
    res = step_until_decision(st, telemetry=trk)
    assert isinstance(res, GameOver)
    assert res.cause_fin == CAUSE_REVEIL_GARDIENS
    assert res.tour_fin == 3
    ts = trk.summary()
    assert ts.reveil_attempts == 1
    assert ts.reveil_failures == 0
    assert ts.gardien_bets_won == 2
    assert ts.gardien_bets_lost == 0
    assert ts.rs_count == 1
    assert ts.rs_t3 == 1
    assert ts.rs_def_resonance == 1
    assert ts.rs_def_other_cases == 2
    assert ts.rs_ratio_arbres_bp > 0

    # B. Priorité absolue à CAUSE_TOUR_8 au Tour 8 même si tous les paris sont gagnés !
    st_t8 = GameState(cfg)
    st_t8.tour = 8
    st_t8.set_gardien_at_case(1, 1, face=1)
    st_t8.set_gardien_at_case(4, 2, face=1)
    st_t8.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st_t8.place_defender_gardien_pari(2, 4, FACE_DEFINITIF)
    st_t8.light_trigger(1)
    sweep_gardiens(st_t8)
    st_t8.light_trigger(1)
    sweep_gardiens(st_t8)
    st_t8.step = STEP_5_3_END_CHECK
    res_t8 = step_until_decision(st_t8)
    assert isinstance(res_t8, GameOver)
    assert res_t8.cause_fin == CAUSE_TOUR_8
    assert res_t8.tour_fin == 8


def test_b2_clean_withdrawal_and_b3_utility() -> None:
    """B2 se retire proprement en Mode 2 si l'équipe ne réunit pas N Défs ; B3 aligne Éveil à +0.03."""
    go_rev = GameOver(tour_fin=4, cause_fin=CAUSE_REVEIL_GARDIENS, score_arbres=20, ratio_arbres=0.5)
    go_som = GameOver(tour_fin=4, cause_fin=CAUSE_REVE_RANG_1, score_arbres=20, ratio_arbres=0.5)
    go_t8 = GameOver(tour_fin=8, cause_fin=CAUSE_TOUR_8, score_arbres=20, ratio_arbres=0.5)
    assert _gameover_utility(go_rev) == _gameover_utility(go_som)
    assert _gameover_utility(go_rev) > _gameover_utility(go_t8)

    # B2 en Mode 2 : 1 seul joueur en réflexion sur GARDIEN_PARI, 2 alliés verrouillés en forêt -> retrait propre
    cfg = GameConfig(n_players=3, mode=2, peuples=("M", "R", "O"))
    st = GameState(cfg)
    st.tour = 3
    st.set_gardien_at_case(1, 1, face=1)
    for s in range(3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        st.place_defender_foret(s, 0, s, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(0, 1, FACE_REFLEXION)
    st.place_defender_foret(1, 1, 1, 2, FACE_DEFINITIF)
    st.place_defender_foret(2, 1, 2, 2, FACE_DEFINITIF)
    st.step = STEP_2_2_DEF2

    resolve_step2_2_from_state(st, score_target_b2, k_max_passes=2)
    assert st.count_gardien_pari_defenders_at_case(1) == 0


def test_calibration_pari_gardiens_manifest_resolution_and_micro_unit() -> None:
    """Le manifeste calibration_pari_gardiens_v5_4.json résout 6 châssis × 2 variantes × N=3..6 (A>=1)."""
    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_pari_gardiens_v5_4.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["player_counts"] == [3, 4, 5, 6]
    assert len(plan["profile_variants"]) == 2
    assert {v["gardien_resonance_cap"] for v in plan["profile_variants"]} == {
        "UNLIMITED",
        "MAX_1_DEF",
    }
    assert plan["total_configurations"] == 4 * 6 * 2
    assert all(int(u["n_animaux_sauvages"]) >= 1 for u in plan["units"])
    assert all(u["reve_activation_mode"] == "1_DEF_1_MACHINE" for u in plan["units"])

    # Exécuter une micro-unité (1 partie) pour vérifier les colonnes Parquet / télémétrie
    micro_unit = dict(plan["units"][0])
    micro_unit["n_games"] = 1
    row = _execute_manifest_unit(micro_unit)
    assert "count_reveil_attempts" in row
    assert "count_reveil_failures" in row
    assert "count_gardien_bets_won" in row
    assert "count_gardien_bets_lost" in row
    assert "rs_ratio_arbres_bp" in row
    assert "rs_def_resonance" in row
    assert "rs_def_other_cases" in row
    assert row["gardien_resonance_cap"] in ("UNLIMITED", "MAX_1_DEF")
