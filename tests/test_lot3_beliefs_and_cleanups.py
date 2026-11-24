"""Tests Lot 3 — Alignement exact des croyances Rêves, auto-exclusion, purge RES_APPRENTISSAGE et ordres 5.1/5.2/4.2."""

from __future__ import annotations

import pytest

from bots.belief_and_ticks import build_belief_summary, compute_private_urgency
from bots.bot_b0 import _compute_threat_and_machine_masks
from bots.heuristic_engine import (
    ALL_ACTIVE_RESOURCES,
    BotB1,
    BotB2,
    _compute_b2_resource_and_trigger_values,
    get_economie_catalog,
)
from engine.core_engine import (
    DEC_ORDRE_ATTAQUE_5_1,
    DEC_ORDRE_NID_4_2,
    DEC_ORDRE_RATISSAGE_5_2,
    _advance_continuation,
    _run_step_3_2,
    apply_choice,
)
from engine.primitives import DecisionRequest
from engine.rng import rand_u64
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MAX_P,
    PIEGE_ACTIF,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    STEP_3_2_REVEAL,
    STEP_4_2_NIDS,
    STEP_5_1_TACTIQUES,
    STEP_5_2_RATISSAGE,
    GameConfig,
    GameState,
    machine_card_code,
    resolve_reve_rank_cancellations,
    tile_id_to_code,
)

R1_CODE = tile_id_to_code("R1")


def _resolve_reves_3_2_with_b2(st_eng: GameState) -> None:
    """Exécute la révélation 3.2 v6.2 en répondant aux choix de cible Rêve avec BotB2."""
    for s in range(st_eng.cfg.n_players):
        card, d1, d2, lec_m, _bound = st_eng.get_player_hand(s)
        st_eng.set_player_hand(s, card, d1, d2, lec_m, 0)
    st_eng.step = STEP_3_2_REVEAL
    st_eng._continuation.clear()
    _run_step_3_2(st_eng)
    while st_eng._continuation:
        req = _advance_continuation(st_eng)
        if isinstance(req, DecisionRequest):
            choice = BotB2.choose(st_eng.get_observation(req.decideur), req, st_eng.cfg)
            apply_choice(st_eng, choice)


def _setup_mode2_state(seed: int = 42, n_players: int = 4) -> GameState:
    peuples = ("M", "R", "O", "H", "E", "I")[:n_players]
    cfg = GameConfig(n_players=n_players, mode=2, peuples=peuples, exp_seed=seed, rep_id=1)
    st = GameState(cfg)
    st.tour = 2
    st.step = STEP_2_2_DEF2
    return st


def test_reve_open_paravents_two_machines_one_defender_exact_engine_concordance() -> None:
    """Cas exact de l'audit : 2 machines visent le même rang Rêve avec 1 Défenseur.

    Avec paravents ouverts, seat 0 est annulé et seat 1 NE l'est PAS (frappe la Tactique imprimée).
    """
    st = _setup_mode2_state(seed=101)
    st.paravents_ouverts = True
    # Rêve R1 placé au rang 1 (Tactique imprimée T1 = SUR_PLACE)
    st.set_tactique_at_rank(0, R1_CODE)
    # 1 seul Défenseur sur le Rêve rang 1
    st.place_defender_reve_activation(2, 1, FACE_DEFINITIF, def_idx=0)

    # Deux machines de force strictement égale (pos=2, eff_red=0, NORMAL) visant toutes deux le rang 1
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 0, 0)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, 0, 0)

    c0 = machine_card_code(0, MACHINE_ABATTEUSE)
    c1 = machine_card_code(1, MACHINE_ABATTEUSE)
    st.set_player_hand(0, c0, 1, 2, 1, 1)
    st.set_player_hand(1, c1, 1, 2, 1, 1)
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)

    bel0 = build_belief_summary(st.get_observation(0), st.cfg)
    bel1 = build_belief_summary(st.get_observation(1), st.cfg)

    # Seat 0 gagne le départage (-seat) -> annulé ; Seat 1 non annulé -> attaque T1 (SUR_PLACE sur r=1, p=2)
    assert bel0.own_machine_cancelled_by_reve is True
    assert bel0.own_machine_cancel_prob == pytest.approx(1.0)
    assert bel1.own_machine_cancelled_by_reve is False
    assert bel1.own_machine_cancel_prob == pytest.approx(0.0)
    assert bel1.parcel_strike_prob[0 * MAX_P + (2 - 1)] == pytest.approx(0.0)
    assert bel1.parcel_strike_prob[1 * MAX_P + (2 - 1)] == pytest.approx(1.0)

    # Concordance 100 % avec l'exécution réelle du moteur en 3.2 (BotB2 choisit la combo de menace max)
    st_eng = st.clone()
    _resolve_reves_3_2_with_b2(st_eng)
    assert st_eng.get_player_hand(0)[4] == 0
    assert st_eng.get_player_hand(1)[4] == 1


def test_reve_open_paravents_100pct_concordance_randomized_scenarios() -> None:
    """Fuzz 60 scénarios Rêves multi-machines : 100 % de concordance croyance paravents ouverts <-> moteur."""
    for idx in range(60):
        st = _setup_mode2_state(seed=700 + idx, n_players=4)
        st.paravents_ouverts = True
        rank = int(rand_u64(700, idx, 1, 1, 0, 0) % 6) + 1
        st.set_tactique_at_rank(rank - 1, R1_CODE)

        n_defs = int(rand_u64(700, idx, 2, 1, 0, 0) % 4)  # 0..3 défenseurs
        for d_i in range(n_defs):
            st.place_defender_reve_activation(d_i % 4, rank, FACE_DEFINITIF, def_idx=d_i // 4)

        assigned: list[tuple[int, int, int]] = []
        for s in range(4):
            r_m = s
            mt = int(rand_u64(700, idx, 3, 1, s, 0) % 2)
            pos = int(rand_u64(700, idx, 4, 1, s, 0) % 4) + 1
            red = int(rand_u64(700, idx, 5, 1, s, 0) % 3)
            st.set_machine_pos_status(r_m, mt, pos, MACHINE_STATUS_NORMAL, False)
            st.set_machine_tokens(r_m, mt, red, 0)
            c = machine_card_code(r_m, mt)
            st.set_player_hand(s, c, rank, rank, rank, rank)
            assigned.append((s, r_m, mt))

        # Croyances de chaque siège avant 3.2
        predicted_cancelled: dict[int, bool] = {}
        for s in range(4):
            bel = build_belief_summary(st.get_observation(s), st.cfg)
            predicted_cancelled[s] = bel.own_machine_cancelled_by_reve

        # Résolution moteur réelle en 3.2 (owner B2 choisit la combo max menace)
        st_eng = st.clone()
        _resolve_reves_3_2_with_b2(st_eng)

        for s, _r_m, _mt in assigned:
            actual_cancelled = st_eng.get_player_hand(s)[4] == 0
            assert predicted_cancelled[s] == actual_cancelled, (
                f"Divergence moteur/croyance scénario {idx}, seat={s}, n_defs={n_defs}"
            )


def test_undefended_reve_triggers_printed_tactic_in_belief_urgency_and_b0() -> None:
    """Un Rêve sans défenseur (0 def) ne masque jamais la menace de la Tactique imprimée (B0, urgence, croyances)."""
    st = _setup_mode2_state(seed=202)
    st.step = STEP_2_1_DEF1
    st.paravents_ouverts = False
    # Rêve R1 au rang 1 (T1 = SUR_PLACE), 0 défenseur dessus
    st.set_tactique_at_rank(0, R1_CODE)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 1)
    for s in (1, 2, 3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)

    obs0 = st.get_observation(0)
    bel0 = build_belief_summary(obs0, st.cfg)
    assert bel0.own_machine_cancelled_by_reve is False
    assert bel0.parcel_strike_prob[0 * MAX_P + (2 - 1)] >= 0.999

    tick0, urg0 = compute_private_urgency(obs0, st.cfg)
    assert tick0 in (1, 2)
    assert urg0 > 0.0

    threat_mask, _ = _compute_threat_and_machine_masks(obs0, st.cfg, obs0.hand_of(0))
    assert (threat_mask & (1 << (0 * MAX_P + (2 - 1)))) != 0


def test_closed_paravents_reve_cancel_prob_calibrated_against_draws() -> None:
    """Paravents fermés : la probabilité d'annulation Poisson-Binomiale suit la fréquence empirique."""
    st_base = _setup_mode2_state(seed=303, n_players=4)
    st_base.paravents_ouverts = False
    st_base.set_tactique_at_rank(0, R1_CODE)  # Rêve au rang 1 (min 2D6 = 11/36)
    st_base.place_defender_reve_activation(2, 1, FACE_DEFINITIF, def_idx=0)  # 1 seul défenseur

    # Observer seat 3 a une machine faible (pos=1, red=0) visant le rang 1.
    # Toutes les autres machines normales sont plus fortes (pos=3, red=1) : toute machine adverse tirant 1 bat seat 3 !
    for r in range(4):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if r == 3 and mt == MACHINE_BULLDOZER:
                st_base.set_machine_pos_status(r, mt, 1, MACHINE_STATUS_NORMAL, False)
                st_base.set_machine_tokens(r, mt, 0, 0)
            else:
                st_base.set_machine_pos_status(r, mt, 3, MACHINE_STATUS_NORMAL, False)
                st_base.set_machine_tokens(r, mt, 1, 0)

    # Seat 3 connaît uniquement sa main ; seats 0, 1, 2 sont masqués (0 Sabotage dans le paquet)
    own_card = machine_card_code(3, MACHINE_BULLDOZER)
    st_base.set_player_hand(3, own_card, 1, 2, 1, 1)
    for s in (0, 1, 2):
        st_base.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 2, 3, 2, 2)

    bel3 = build_belief_summary(st_base.get_observation(3), st_base.cfg)
    # 3 adversaires tirent indépendamment M=1 avec prob 11/36 -> P(aucun ne tire 1) = (25/36)^3 ≈ 0.3349
    expected_cancel_exact = (25.0 / 36.0) ** 3
    assert 0.25 <= bel3.own_machine_cancel_prob <= 0.45
    assert abs(bel3.own_machine_cancel_prob - expected_cancel_exact) < 0.08

    # Vérification empirique sur 400 tirages indépendants des 3 dés adverses via resolve_reve_rank_cancellations
    emp_cancelled = 0
    for trial in range(400):
        entries: list[tuple[int, int, int, int]] = [(3, 1, MACHINE_STATUS_NORMAL, 0)]
        for s in (0, 1, 2):
            d1 = int(rand_u64(303, trial, 10, 1, s, 0) % 6) + 1
            d2 = int(rand_u64(303, trial, 10, 1, s, 1) % 6) + 1
            if min(d1, d2) == 1:
                entries.append((s, 3, MACHINE_STATUS_NORMAL, 1))
        if 3 in resolve_reve_rank_cancellations(entries, 1):
            emp_cancelled += 1
    emp_rate = emp_cancelled / 400.0
    assert abs(bel3.own_machine_cancel_prob - emp_rate) < 0.10


def test_self_signal_exclusion_lisiere_and_furtivite() -> None:
    """Les propres pions de l'observateur ne doivent jamais gonfler les signaux coopératifs alliés."""
    st = _setup_mode2_state(seed=404, n_players=4)
    st.paravents_ouverts = False
    st.sabotage_deck_count = 2
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    for s in (1, 2, 3):
        st.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 2, 3, 2, 2)

    bel_clean = build_belief_summary(st.get_observation(0), st.cfg)

    # Seat 0 pose son propre def1 sur une lisière et son propre def2 sur Rive Sabotage du rayon 0
    st_self = st.clone()
    st_self.place_defender_lisiere_tile(0, 0, 0, FACE_DEFINITIF)
    st_self.place_defender_furtivite(0, 1, 0, 1, FACE_REFLEXION)
    bel_self = build_belief_summary(st_self.get_observation(0), st_self.cfg)

    assert bel_self.coop_lisiere_signals == bel_clean.coop_lisiere_signals == 0
    assert bel_self.coop_furtivite_signals == bel_clean.coop_furtivite_signals == 0
    assert bel_self.p_neighbor_sabotage == pytest.approx(bel_clean.p_neighbor_sabotage)
    assert bel_self.parcel_strike_prob == bel_clean.parcel_strike_prob

    # Seat 0 pose son propre def1 sur Rive Piège du rayon 1 : ne doit pas gonfler la menace du rayon 1 !
    st_self_p = st.clone()
    st_self_p.place_defender_furtivite(0, 0, 1, 0, FACE_DEFINITIF)
    bel_self_p = build_belief_summary(st_self_p.get_observation(0), st_self_p.cfg)
    assert bel_self_p.coop_furtivite_signals == 0
    assert bel_self_p.parcel_strike_prob == bel_clean.parcel_strike_prob

    # En revanche, quand un ALLIÉ (seat 1) pose sur lisière + Rive Sabotage, les signaux augmentent !
    st_ally = st.clone()
    st_ally.place_defender_lisiere_tile(1, 0, 0, FACE_DEFINITIF)
    st_ally.place_defender_furtivite(1, 1, 0, 1, FACE_REFLEXION)
    bel_ally = build_belief_summary(st_ally.get_observation(0), st_ally.cfg)
    assert bel_ally.coop_lisiere_signals == 1
    assert bel_ally.coop_furtivite_signals == 1
    assert bel_ally.p_neighbor_sabotage > bel_clean.p_neighbor_sabotage


def test_res_apprentissage_completely_purged() -> None:
    """RES_APPRENTISSAGE ne doit plus exister dans les ressources actives ni le graphe economie_bot."""
    assert "RES_APPRENTISSAGE" not in ALL_ACTIVE_RESOURCES
    assert len(ALL_ACTIVE_RESOURCES) == 11

    econ = get_economie_catalog()
    for node in econ.values():
        assert "RES_APPRENTISSAGE" not in node.inputs_requis
        assert "RES_APPRENTISSAGE" not in node.outputs_produits

    st = _setup_mode2_state(seed=505)
    obs0 = st.get_observation(0)
    res_val, _ = _compute_b2_resource_and_trigger_values(
        obs0, st.cfg, build_belief_summary(obs0, st.cfg)
    )
    assert "RES_APPRENTISSAGE" not in res_val
    assert set(res_val.keys()) == set(ALL_ACTIVE_RESOURCES)


def test_deterministic_attack_order_5_1_and_5_2_minimizes_tree_loss() -> None:
    """5.1 & 5.2 : sur une parcelle piégée avec 3 arbres, envoyer l'Abatteuse en premier économise 2 arbres."""
    st = _setup_mode2_state(seed=606)
    st.paravents_ouverts = True
    st.step = STEP_5_1_TACTIQUES
    st.set_parcel_arbres_souches(0, 2, 3, 0)
    st.set_parcel_piege(0, 2, PIEGE_ACTIF)
    st.set_parcel_defenseurs(0, 2, 0)
    st.set_parcel_insectes(0, 2, 0)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)

    opts_ab_first = ((0, MACHINE_ABATTEUSE), (0, MACHINE_BULLDOZER))
    opts_bu_first = ((0, MACHINE_BULLDOZER), (0, MACHINE_ABATTEUSE))
    obs = st.get_observation(0)

    for opts in (opts_ab_first, opts_bu_first):
        req_51 = DecisionRequest(
            decideur=0,
            decision_type=DEC_ORDRE_ATTAQUE_5_1,
            options=opts,
            context={"rank": 1, "tactique": "T1"},
        )
        assert BotB2.choose(obs, req_51, st.cfg) == (0, MACHINE_ABATTEUSE)
        assert BotB1.choose(obs, req_51, st.cfg) == (0, MACHINE_ABATTEUSE)

    # Même test en Ratissage 5.2
    st.step = STEP_5_2_RATISSAGE
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_RATISSAGE, False)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_RATISSAGE, False)
    obs_rat = st.get_observation(0)
    for opts in (opts_ab_first, opts_bu_first):
        req_52 = DecisionRequest(
            decideur=0,
            decision_type=DEC_ORDRE_RATISSAGE_5_2,
            options=opts,
            context={"tour": st.tour},
        )
        assert BotB2.choose(obs_rat, req_52, st.cfg) == (0, MACHINE_ABATTEUSE)
        assert BotB1.choose(obs_rat, req_52, st.cfg) == (0, MACHINE_ABATTEUSE)


def test_deterministic_attack_order_avoids_unnecessary_route_creation() -> None:
    """Sans piège ni défense sur 2 arbres / 0 souche, Bulldozer avant Abatteuse évite de raser en Route."""
    st = _setup_mode2_state(seed=607)
    st.paravents_ouverts = True
    st.step = STEP_5_1_TACTIQUES
    st.set_parcel_arbres_souches(0, 2, 2, 0)
    st.set_parcel_defenseurs(0, 2, 0)
    st.set_parcel_insectes(0, 2, 0)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)

    obs = st.get_observation(0)
    for opts in (
        ((0, MACHINE_ABATTEUSE), (0, MACHINE_BULLDOZER)),
        ((0, MACHINE_BULLDOZER), (0, MACHINE_ABATTEUSE)),
    ):
        req = DecisionRequest(
            decideur=0,
            decision_type=DEC_ORDRE_ATTAQUE_5_1,
            options=opts,
            context={"rank": 1, "tactique": "T1"},
        )
        # Bulldozer -> (1 arbre, 0 souche) -> Abatteuse -> (0 arbre, 1 souche, PAS de Route !)
        # Abatteuse -> (0 arbre, 2 souches) -> Bulldozer -> (0 arbre, 0 souche = ROUTE !)
        assert BotB2.choose(obs, req, st.cfg) == (0, MACHINE_BULLDOZER)


def test_deterministic_nid_order_4_2_prioritizes_threatened_rich_parcel() -> None:
    """4.2 : le choix d'ordre des Nids est déterministe et priorise un Nid menacé et riche en arbres."""
    st = _setup_mode2_state(seed=608)
    st.paravents_ouverts = True
    st.step = STEP_4_2_NIDS
    # Nid 1 sur (ray=0, p=4) loin des machines, 1 arbre
    st.set_parcel_arbres_souches(0, 4, 1, 0)
    st.set_parcel_nid(0, 4, 1, active_ce_tour=False)
    # Nid 2 sur (ray=1, p=2) directement sous l'Abatteuse, 3 arbres
    st.set_parcel_arbres_souches(1, 2, 3, 0)
    st.set_parcel_nid(1, 2, 2, active_ce_tour=False)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)

    obs = st.get_observation(0)
    for opts in ((1, 2), (2, 1)):
        req = DecisionRequest(
            decideur=0,
            decision_type=DEC_ORDRE_NID_4_2,
            options=opts,
            context={"tour": st.tour},
        )
        assert BotB2.choose(obs, req, st.cfg) == 2
        assert BotB1.choose(obs, req, st.cfg) == 2
