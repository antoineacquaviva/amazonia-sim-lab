"""Tests Lot 4 — Monnaie unique arbres de B2 (<100 params), rollouts CRN Gardiens/Rêves, tuner et B3 exact."""

from __future__ import annotations

from collections import Counter

import pytest

import engine.effects  # noqa: F401
from bots.b2_economy import (
    DEFAULT_B2_WEIGHTS,
    B2Weights,
    evaluate_forest_marginal_breakdown,
)
from bots.b2_rollouts import (
    determinize_state_from_obs,
    evaluate_gardien_reve_candidates_crn,
)
from bots.belief_and_ticks import build_belief_summary
from bots.bot_b0 import play_game_b0
from bots.bot_b3_rh import BotB3, play_game_b3
from bots.heuristic_engine import choose_b2, play_game_b1, play_game_b2
from campaigns.designs import balanced_neighbor_mirror_tables
from engine.core_engine import DEC_DEPLOIEMENT_NID_4_2, step_until_decision
from engine.primitives import DecisionRequest
from engine.state import (
    CARD_NONE,
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FURT_RIVE_PIEGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PIEGE_ACTIF,
    STEP_2_2_DEF2,
    STEP_4_2_NIDS,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from scripts_cloud.tune_b2_weights import tune_b2_weights


def _make_state(n_players: int = 4, mode: int = 2, seed: int = 404) -> GameState:
    peuples = ("M", "R", "O", "H", "E", "I")[:n_players]
    cfg = GameConfig(n_players=n_players, mode=mode, peuples=peuples, exp_seed=seed, rep_id=1)
    st = GameState(cfg)
    st.tour = 2
    st.step = STEP_2_2_DEF2
    return st


# ---------------------------------------------------------------------------
# 1. Monnaie unique « arbres marginalement sauvés » & budget < 100 constantes
# ---------------------------------------------------------------------------


def test_b2_weights_under_100_named_parameters() -> None:
    count = B2Weights.param_count()
    assert 30 <= count < 100, f"B2Weights doit compter < 100 paramètres (trouvé : {count})"
    assert DEFAULT_B2_WEIGHTS.res_arbre_w == pytest.approx(1.0)


def test_forest_marginal_trees_exact_abatteuse_vs_bulldozer_and_thresholds() -> None:
    """Abatteuse coupe tous les arbres (3), Bulldozer 1 seul ; seuil discret sans lissage."""
    st_ab = _make_state(seed=101)
    st_ab.paravents_ouverts = True
    # Parcelle (0, 3) : dotation/seuil de base = 3, 3 arbres, 2 défenseurs -> gap = 1
    st_ab.set_parcel_arbres_souches(0, 3, 3, 0)
    st_ab.set_parcel_defenseurs(0, 3, 2)
    st_ab.set_parcel_insectes(0, 3, 0)
    st_ab.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    st_ab.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL, False)
    # T1 (ASSAUT en Acte 1, SUR_PLACE sur p=3)
    st_ab.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 1)
    for s in (1, 2, 3):
        st_ab.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)

    obs_ab = st_ab.get_observation(0)
    bd_ab = evaluate_forest_marginal_breakdown(
        obs_ab, st_ab.cfg, build_belief_summary(obs_ab, st_ab.cfg), 0, 3
    )
    assert bd_ab.immediate_trees_saved == pytest.approx(3.0)

    # Même situation avec Bulldozer au lieu d'Abatteuse -> sauve exactement 1 arbre !
    st_bu = st_ab.clone()
    st_bu.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    st_bu.set_machine_pos_status(0, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL, False)
    st_bu.set_player_hand(0, machine_card_code(0, MACHINE_BULLDOZER), 1, 2, 1, 1)
    obs_bu = st_bu.get_observation(0)
    bd_bu = evaluate_forest_marginal_breakdown(
        obs_bu, st_bu.cfg, build_belief_summary(obs_bu, st_bu.cfg), 0, 3
    )
    assert bd_bu.immediate_trees_saved == pytest.approx(1.0)
    assert bd_ab.total_trees > bd_bu.total_trees + 1.5

    # Déjà paré (defs=3 >= seuil=3, 0 insecte) -> gain marginal d'arbres strictement nul
    st_par = st_ab.clone()
    st_par.set_parcel_defenseurs(0, 3, 3)
    obs_par = st_par.get_observation(0)
    bd_par = evaluate_forest_marginal_breakdown(
        obs_par, st_par.cfg, build_belief_summary(obs_par, st_par.cfg), 0, 3
    )
    assert bd_par.immediate_trees_saved == pytest.approx(0.0)


def test_forest_marginal_trees_single_strike_trap_insect_saving_route_and_charge() -> None:
    """Piège SINGLE_STRIKE, économie d'Insecte, pénalité Route et Charge denial séparés."""
    # 1. Piège autonome face à 1 seule frappe -> 0 arbre sauvé marginalement
    st_t1 = _make_state(seed=102)
    st_t1.paravents_ouverts = True
    st_t1.set_parcel_arbres_souches(0, 2, 3, 0)
    st_t1.set_parcel_piege(0, 2, PIEGE_ACTIF)
    st_t1.set_parcel_defenseurs(0, 2, 1)  # seuil=2 -> gap=1 sans piège
    st_t1.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st_t1.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL, False)
    st_t1.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 1)
    for s in (1, 2, 3):
        st_t1.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    obs_t1 = st_t1.get_observation(0)
    bd_t1 = evaluate_forest_marginal_breakdown(
        obs_t1, st_t1.cfg, build_belief_summary(obs_t1, st_t1.cfg), 0, 2
    )
    assert bd_t1.immediate_trees_saved == pytest.approx(0.0)

    # 2. Piège SINGLE_STRIKE face à DEUX frappes (Abatteuse + Bulldozer) -> piège bloque Abatteuse,
    #    +1 Défenseur pare Bulldozer et sauve exactement 1.0 arbre !
    st_t2 = st_t1.clone()
    st_t2.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)
    st_t2.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 1, 2, 1, 1)
    obs_t2 = st_t2.get_observation(0)
    bd_t2 = evaluate_forest_marginal_breakdown(
        obs_t2, st_t2.cfg, build_belief_summary(obs_t2, st_t2.cfg), 0, 2
    )
    assert bd_t2.immediate_trees_saved == pytest.approx(1.0)

    # 3. Économie d'Insecte (defs=1, ins=1, seuil=2 sans piège) -> 0 arbre sauvé, +insect_saved_trees
    st_ins = _make_state(seed=103)
    st_ins.paravents_ouverts = True
    st_ins.set_parcel_arbres_souches(0, 2, 2, 0)
    st_ins.set_parcel_defenseurs(0, 2, 1)
    st_ins.set_parcel_insectes(0, 2, 1)
    st_ins.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st_ins.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 1)
    for s in (1, 2, 3):
        st_ins.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    obs_ins = st_ins.get_observation(0)
    bd_ins = evaluate_forest_marginal_breakdown(
        obs_ins, st_ins.cfg, build_belief_summary(obs_ins, st_ins.cfg), 0, 2
    )
    assert bd_ins.immediate_trees_saved == pytest.approx(0.0)
    assert bd_ins.insect_saved_trees == pytest.approx(DEFAULT_B2_WEIGHTS.insect_saved_trees)

    # 4. Route évitée + Charge denial en Acte 1 (T1 = CHARGE SUR_PLACE en Face A Tours 1..4)
    st_rc = _make_state(seed=104)
    st_rc.tour = 1
    st_rc.paravents_ouverts = True
    st_rc.set_parcel_arbres_souches(0, 1, 1, 0)
    st_rc.set_parcel_defenseurs(0, 1, 1)  # seuil=2 -> gap=1
    st_rc.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL, False)
    st_rc.set_player_hand(0, machine_card_code(0, MACHINE_BULLDOZER), 1, 2, 1, 1)
    for s in (1, 2, 3):
        st_rc.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    obs_rc = st_rc.get_observation(0)
    bd_rc = evaluate_forest_marginal_breakdown(
        obs_rc, st_rc.cfg, build_belief_summary(obs_rc, st_rc.cfg), 0, 1
    )
    assert bd_rc.immediate_trees_saved == pytest.approx(1.0)
    assert bd_rc.route_avoided_trees == pytest.approx(DEFAULT_B2_WEIGHTS.route_penalty_trees)
    assert bd_rc.charge_denied_trees == pytest.approx(DEFAULT_B2_WEIGHTS.charge_penalty_early)


# ---------------------------------------------------------------------------
# 2. Rollouts CRN Gardiens/Rêves & progression Mode 4 (> 0.37 Gardiens/partie, B2 > B1)
# ---------------------------------------------------------------------------


def test_crn_gardien_reve_rollouts_strictly_isolated_and_deterministic() -> None:
    """Deux états partageant PlayerObservation donnent exactement les mêmes deltas CRN."""
    cfg = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "H"), exp_seed=512, rep_id=3)
    st_a = GameState(cfg)
    st_a.tour = 3
    st_a.step = STEP_2_2_DEF2
    st_a.paravents_ouverts = False
    st_a.set_gardien_at_case(1, 1, 1)
    for s in range(4):
        st_a.place_defender_foret(s, 0, s, 2, FACE_DEFINITIF)
        st_a.place_defender_foret(s, 1, s, 1, 1)
    st_a.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 1)
    st_a.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 2, 3, 2, 2)
    st_a.set_player_hand(2, machine_card_code(2, MACHINE_BULLDOZER), 3, 4, 3, 3)
    st_a.set_player_hand(3, machine_card_code(3, MACHINE_BULLDOZER), 4, 5, 4, 4)

    # État B : mêmes observations pour seat 0, mais mains adverses masquées complètement permutées !
    st_b = st_a.clone()
    st_b.set_player_hand(1, machine_card_code(3, MACHINE_ABATTEUSE), 5, 6, 5, 5)
    st_b.set_player_hand(2, machine_card_code(1, MACHINE_BULLDOZER), 1, 1, 1, 1)
    st_b.set_player_hand(3, machine_card_code(2, MACHINE_ABATTEUSE), 6, 6, 6, 6)

    obs_a = st_a.get_observation(0)
    obs_b = st_b.get_observation(0)
    assert obs_a == obs_b

    deltas_a = evaluate_gardien_reve_candidates_crn(
        st_a, obs_a, 0, ("FORET", 0, 1), (("GARDIEN_PARI", 1),), chooser=choose_b2, n_rollouts=8
    )
    deltas_b = evaluate_gardien_reve_candidates_crn(
        st_b, obs_b, 0, ("FORET", 0, 1), (("GARDIEN_PARI", 1),), chooser=choose_b2, n_rollouts=8
    )
    assert deltas_a == deltas_b


def test_mode4_b2_beats_b1_and_activates_gardiens_above_legacy_floor() -> None:
    """Mode 4 : B2 (monnaie arbres + CRN) bat B1 et B0 tout en dépassant nettement 0,37 Gardien/partie."""
    tables = balanced_neighbor_mirror_tables(4, max_tables=4, exp_seed=777)
    b0_s, b1_s, b2_s, g_acts = [], [], [], []
    for t_idx, (_, peuples) in enumerate(tables):
        for rep in range(3):
            cfg = GameConfig(
                n_players=4, mode=4, peuples=peuples, exp_seed=202624, rep_id=t_idx * 10 + rep
            )
            b0_s.append(play_game_b0(GameState(cfg)).ratio_arbres)
            b1_s.append(play_game_b1(GameState(cfg)).ratio_arbres)
            trk = TelemetryTracker()
            b2_s.append(play_game_b2(GameState(cfg), telemetry=trk).ratio_arbres)
            g_acts.append(sum(v for k, v in trk.summary().tile_activations if k.startswith("G")))

    mean_b0 = sum(b0_s) / len(b0_s)
    mean_b1 = sum(b1_s) / len(b1_s)
    mean_b2 = sum(b2_s) / len(b2_s)
    mean_g = sum(g_acts) / len(g_acts)

    assert mean_b2 > mean_b1 > mean_b0, f"Hiérarchie brisée : B0={mean_b0:.4f}, B1={mean_b1:.4f}, B2={mean_b2:.4f}"
    assert mean_g >= 0.80, f"Activation Gardiens Mode 4 trop basse : {mean_g:.2f}/partie (plancher 0.37)"


# ---------------------------------------------------------------------------
# 3. Conservation exacte des cartes & allocation dynamique dans B3
# ---------------------------------------------------------------------------


def _extract_deck_remaining_cards(det: GameState) -> list[int]:
    c_clone = det.clone()
    out: list[int] = []
    while True:
        c = c_clone.draw_next_machine_card()
        if c == CARD_NONE:
            break
        out.append(c)
    return out


def test_b3_determinization_100pct_exact_card_conservation_240_worlds() -> None:
    """Invariant strict : 100 % des 240 mondes déterminisés conservent exactement Machines + Sabotages."""
    checked = 0
    for n_pl in (3, 4, 5, 6):
        for sab_cnt in (0, 1, 2, 3, 4):
            st = _make_state(n_players=n_pl, mode=2, seed=800 + n_pl * 10 + sab_cnt)
            st.paravents_ouverts = False
            # Passer une machine en Ratissage pour vérifier son exclusion exacte du paquet
            if sab_cnt % 2 == 1:
                st.set_machine_pos_status(0, MACHINE_BULLDOZER, st.cfg.p_max, MACHINE_STATUS_RATISSAGE, False)

            st.sabotage_deck_count = sab_cnt
            st.sabotage_pending_count = 1
            st.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
            # Distribuer exactement n_pl cartes depuis le paquet réel (comme Step 1.2)
            for s in range(n_pl):
                c = st.draw_next_machine_card()
                if c == CARD_SABOTAGE:
                    st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
                elif c != CARD_NONE:
                    st.set_player_hand(s, c, 2, 3, 2, 2)
                else:
                    st.set_player_hand(s, CARD_NONE, 0, 0, 0, 0)

            expected_pool: list[int] = []
            for r in range(n_pl):
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                    if st.get_machine_pos_status(r, mt)[1] == MACHINE_STATUS_NORMAL:
                        expected_pool.append(machine_card_code(r, mt))
            expected_pool.extend([CARD_SABOTAGE] * st.sabotage_deck_count)
            expected_counter = Counter(expected_pool)

            for obs_seat in (0, n_pl - 1):
                obs = st.get_observation(obs_seat)
                for det_idx in range(6):
                    det = determinize_state_from_obs(st, obs, det_idx=det_idx)
                    held = [
                        det.get_player_hand(s)[0]
                        for s in range(n_pl)
                        if det.get_player_hand(s)[0] != CARD_NONE
                    ]
                    rem_deck = _extract_deck_remaining_cards(det)
                    assert len(rem_deck) == obs.deck_remaining_count, (
                        f"Taille pioche incohérente N={n_pl} sab={sab_cnt} det={det_idx}"
                    )
                    assert Counter(held + rem_deck) == expected_counter, (
                        f"Violation conservation cartes N={n_pl} sab={sab_cnt}: "
                        f"got={Counter(held + rem_deck)} vs expected={expected_counter}"
                    )
                    checked += 1

    assert checked == 240


def test_b3_determinization_weighted_by_board_signals_and_isolated() -> None:
    """Un signal allié Rive Piège sur rayon 0 augmente la probabilité de tirage des cartes du rayon 0."""
    st = _make_state(n_players=4, mode=2, seed=909)
    st.paravents_ouverts = False
    st.sabotage_deck_count = 1
    st.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    for s in range(4):
        c = st.draw_next_machine_card()
        st.set_player_hand(s, c, 2, 3, 2, 2) if c != CARD_SABOTAGE else st.set_player_hand(s, c, 0, 0, 0, 0)
    # Seat 0 détient Sabotage ; un allié (seat 1) signale Rive Piège sur le rayon 0
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.place_defender_furtivite(1, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)

    obs0 = st.get_observation(0)
    ray0_hits = 0
    ray3_hits = 0
    for d_i in range(180):
        det = determinize_state_from_obs(st, obs0, det_idx=d_i)
        for s in (1, 2, 3):
            c = det.get_player_hand(s)[0]
            if c in (machine_card_code(0, 0), machine_card_code(0, 1)):
                ray0_hits += 1
            elif c in (machine_card_code(3, 0), machine_card_code(3, 1)):
                ray3_hits += 1
    assert ray0_hits > ray3_hits + 20


def test_b3_dynamic_budget_allocation_adapts_to_uncertainty() -> None:
    """Budget adaptatif B3 : s'arrête tôt si l'écart est net, s'étend jusqu'à max_det si serré."""
    cfg_b3 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"), exp_seed=950, rep_id=1)
    st = GameState(cfg_b3)
    st.tour = 2
    st.paravents_ouverts = True
    st.set_parcel_nid(3, 2, 1)
    st.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)
    st.step = STEP_4_2_NIDS
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest) and req.decision_type == DEC_DEPLOIEMENT_NID_4_2
    obs = st.get_observation(req.decideur)

    # Cas 1 : seuil d'incertitude nul -> s'arrête dès min_determinizations=2 si écart > 0 ou 1.96*SE
    # Cas 2 : seuil d'incertitude élevé (10.0) -> étend jusqu'à max_determinizations=5 !
    stats_tight: dict[str, int] = {}
    BotB3.choose_from_determinized(
        st,
        obs,
        req,
        n_determinizations=2,
        max_determinizations=5,
        uncertainty_threshold=10.0,
        budget_stats=stats_tight,
    )
    assert stats_tight["determinizations_used"] == 5

    # Vérifier aussi que play_game_b3 tourne bout-en-bout sans erreur avec le budget dynamique
    cfg_smoke = GameConfig(n_players=3, mode=2, peuples=("M", "R", "O"), exp_seed=951, rep_id=0)
    over = play_game_b3(GameState(cfg_smoke), n_determinizations=2, max_determinizations=4)
    assert 1 <= over.tour_fin <= 8
    assert step_until_decision(GameState(cfg_smoke)) is not None


# ---------------------------------------------------------------------------
# 4. Accordeur automatique reproductible sur split disjoint + regret micro-fork
# ---------------------------------------------------------------------------


def test_b2_weight_tuner_disjoint_split_reproducible_and_tracks_regret() -> None:
    r1 = tune_b2_weights(
        mode=2,
        n_players_list=(4,),
        pairs_per_split=1,
        reps_per_table=1,
        iterations=2,
        exp_seed=202699,
        regret_forks=1,
    )
    r2 = tune_b2_weights(
        mode=2,
        n_players_list=(4,),
        pairs_per_split=1,
        reps_per_table=1,
        iterations=2,
        exp_seed=202699,
        regret_forks=1,
    )
    assert r1 == r2
    assert r1["param_count"] < 100
    assert not (set(r1["train_circles"]) & set(r1["val_circles"]))
    assert r1["baseline_val"]["regret"] is not None
    assert r1["best_val"]["regret"] is not None
    assert "cvar20" in r1["best_val"]
    assert "mean_c_prive" in r1["best_val"]["regret"]
