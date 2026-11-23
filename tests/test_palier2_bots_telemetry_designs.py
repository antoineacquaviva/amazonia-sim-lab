"""Tests unitaires Palier 2 : Télémétrie (4 capteurs), Bots B1/B2 isolés et Plans/Micro-Forks."""

from __future__ import annotations

import engine.effects  # noqa: F401
from bots.belief_and_ticks import (
    build_belief_summary,
    compute_private_urgency,
    order_seats_by_tick_and_urgency,
    resolve_step2_full_with_ticks,
)
from bots.heuristic_engine import (
    ALL_ACTIVE_RESOURCES,
    choose_b1,
    choose_b2,
    count_active_laws_from_obs,
    get_economie_catalog,
    play_game_b1,
    play_game_b2,
    score_target_b1,
    score_target_b2,
)
from campaigns.designs import (
    MANDATORY_6_CIRCLES,
    aggregate_micro_forks,
    inter_block_ci95,
    paired_mirror_blocks,
    run_micro_fork_on_config,
    sequential_halving_select,
)
from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.primitives import DecisionRequest, prim_mod_seuil
from engine.state import (
    CARD_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    STEP_3_2_REVEAL,
    STEP_4_3_MIGRATION,
    STEP_5_1_TACTIQUES,
    TACTIQUES_SPEC,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker


# ---------------------------------------------------------------------------
# 1. Isolation stricte de B1 et B2 sous paravent fermé (exigence explicite Palier 2)
# ---------------------------------------------------------------------------
def test_b1_and_b2_strict_isolation_under_closed_paravents() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=202602, rep_id=9)
    s_a = GameState(cfg)
    req_a = step_until_decision(s_a)
    assert isinstance(req_a, DecisionRequest)
    assert s_a.paravents_ouverts is False

    s_b = s_a.clone()
    decideur = req_a.decideur

    # Modifier radicalement les mains et dés cachés de TOUS les voisins dans s_b
    for offset in (1, 2, 3):
        nb = (decideur + offset) % cfg.n_players
        s_a.set_player_hand(nb, CARD_SABOTAGE, 0, 0, 0, 0)
        s_b.set_player_hand(nb, machine_card_code(decideur, MACHINE_BULLDOZER), 6, 6, 6, 0)

    req_b = step_until_decision(s_b)
    assert isinstance(req_b, DecisionRequest)

    obs_a = s_a.get_observation(decideur)
    obs_b = s_b.get_observation(decideur)
    assert obs_a == obs_b
    assert build_belief_summary(obs_a, cfg) == build_belief_summary(obs_b, cfg)
    assert compute_private_urgency(obs_a, cfg) == compute_private_urgency(obs_b, cfg)
    assert choose_b1(s_a, req_a) == choose_b1(s_b, req_b)
    assert choose_b2(s_a, req_a) == choose_b2(s_b, req_b)


# ---------------------------------------------------------------------------
# 2. Ticks 1..3 : Émetteur Sabotage au Tick 1, zéro biais siège 0, arrêt révision 2.2
# ---------------------------------------------------------------------------
def test_ticks_sabotage_altruist_tick1_zero_seat0_bias_and_early_stop() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=4242, rep_id=3)
    state = GameState(cfg)
    _ = step_until_decision(state)

    # Forcer le siège 2 à détenir CARD_SABOTAGE et le siège 0 à détenir une carte annulée sur Rêve
    state.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    obs2 = state.get_observation(2)
    tick2, u2 = compute_private_urgency(obs2, cfg)
    assert tick2 == 1
    assert u2 >= 0.88

    # Vérifier l'absence de biais de siège 0 lorsque tous les sièges ont exactement la même urgence
    first_winners = [0, 0, 0, 0]
    for rep in range(120):
        c_rep = GameConfig(n_players=4, mode=1, exp_seed=777, rep_id=rep)
        ordered = order_seats_by_tick_and_urgency(
            [(0, 2, 0.50), (1, 2, 0.50), (2, 2, 0.50), (3, 2, 0.50)],
            c_rep,
            tour=1,
            sous_etape=211,
        )
        first_winners[ordered[0]] += 1
    for cnt in first_winners:
        assert 15 <= cnt <= 45, f"Biais détecté dans le bris d'égalité PRNG : {first_winners}"

    # Vérifier l'arrêt immédiat en 2.2 quand epsilon_base est très élevé (0 mouvement en passe 1)
    stats = resolve_step2_full_with_ticks(
        state, score_target_b2, k_max_passes=4, epsilon_base=1e6
    )
    assert stats["passes_executed"] == 1
    assert stats["revision_moves"] == 0
    assert state.step > 22


# ---------------------------------------------------------------------------
# 3. B1 (oubli stochastique si > 2 lois) & B2 (graphe economie_bot 12 RES_* + Sabotage)
# ---------------------------------------------------------------------------
def test_b1_law_forgetting_and_b2_economie_graph_sabotage_decay() -> None:
    econ = get_economie_catalog()
    assert len(econ) == 101
    seen_res = {tok for node in econ.values() for tok in node.outputs_produits if tok.startswith("RES_")}
    assert seen_res == set(ALL_ACTIVE_RESOURCES)
    assert "RES_APPRENTISSAGE" not in seen_res

    # B1 : > 2 lois actives simultanément sur le plateau déclenchent l'oubli stochastique contrôlé
    cfg_laws = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G2", "B"), ("G5", "B"), ("G9", "C"), ("G11", "B")),
        exp_seed=9191,
        rep_id=1,
    )
    st_laws = GameState(cfg_laws)
    st_laws.set_gardien_at_case(1, 2, 1)
    st_laws.set_gardien_at_case(2, 5, 1)
    st_laws.set_gardien_at_case(3, 9, 1)
    st_laws.set_gardien_at_case(4, 11, 1)
    obs_laws = st_laws.get_observation(0)
    assert count_active_laws_from_obs(obs_laws, cfg_laws) == 4

    bel_laws = build_belief_summary(obs_laws, cfg_laws)
    diffs = 0
    for r in range(4):
        for p in range(1, 5):
            sc_4 = score_target_b1(obs_laws, cfg_laws, bel_laws, ("FORET", r, p), False)
            # Avec <= 2 lois (en retirant 2 Gardiens), l'oubli stochastique disparaît totalement
            st_2 = st_laws.clone()
            st_2.set_gardien_at_case(3, 0, 1)
            st_2.set_gardien_at_case(4, 0, 1)
            obs_2 = st_2.get_observation(0)
            assert count_active_laws_from_obs(obs_2, cfg_laws) == 2
            sc_2 = score_target_b1(obs_2, cfg_laws, build_belief_summary(obs_2, cfg_laws), ("FORET", r, p), False)
            if abs(sc_4 - sc_2) > 1.0:
                diffs += 1
    assert diffs >= 2

    # B2 : RES_DILUTION_SABOTAGE fortement valorisée au Tour 1 vs faiblement au Tour 8
    cfg_sab = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=303)
    st_t1 = GameState(cfg_sab)
    st_t1.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st_t1.place_defender_furtivite(1, 0, 0, 1, 2)  # Partenaire prêt en 2.1 sur Rive Sabotage du rayon 0
    st_t8 = st_t1.clone()
    st_t8.tour = 8

    obs_t1 = st_t1.get_observation(0)
    obs_t8 = st_t8.get_observation(0)
    sc_sab_t1 = score_target_b2(obs_t1, cfg_sab, build_belief_summary(obs_t1, cfg_sab), ("FURTIVITE", 0, 1), False)
    sc_sab_t8 = score_target_b2(obs_t8, cfg_sab, build_belief_summary(obs_t8, cfg_sab), ("FURTIVITE", 0, 1), False)
    assert sc_sab_t1 > sc_sab_t8 + 40.0


# ---------------------------------------------------------------------------
# 4. Les 4 capteurs cognitifs de engine/telemetry.py (incluant la règle 4.3 = +3 ops)
# ---------------------------------------------------------------------------
def test_telemetry_4_cognitive_sensors_and_4_3_three_ops_rule() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        exp_seed=5150,
    )
    state = GameState(cfg)
    trk = TelemetryTracker()

    # 1) Règle spéciale 4.3 : déplacer 1 Insecte = exactement +3 ops physiques ; RESTER = 0 op !
    state.set_parcel_insectes(0, 2, 2)
    state.step = STEP_4_3_MIGRATION
    req_m1 = step_until_decision(state, telemetry=trk)
    assert isinstance(req_m1, DecisionRequest)
    assert req_m1.decision_type == DEC_MIGRATION_INSECTE_4_3
    ops_before_move = trk.total_physical_ops
    apply_choice(state, ("FORET", 0, 3), telemetry=trk)
    assert trk.total_physical_ops - ops_before_move == 3

    req_m2 = step_until_decision(state, telemetry=trk)
    assert isinstance(req_m2, DecisionRequest)
    ops_before_stay = trk.total_physical_ops
    apply_choice(state, ("RESTER",), telemetry=trk)
    assert trk.total_physical_ops - ops_before_stay == 0

    # 2) Cascades & mid_combat_interrupts en Mode 2 (Pari Gardiens + Résonance)
    state.set_gardien_at_case(1, 9, face=1)
    state.set_gardien_at_case(4, 10, face=1)
    state.place_defender_gardien_pari(0, 1, 2)
    state.place_defender_gardien_pari(1, 4, 2)
    state.step = STEP_5_1_TACTIQUES
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.set_parcel_defenseurs(1, 1, 3)  # Pare la frappe sur R -> allume case 1 -> cascade 1 -> 4 !
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)

    snap_mid = trk.summary()
    assert snap_mid.cascade_sweeps >= 1
    assert snap_mid.mid_combat_interrupts == 2  # Gardien case 1 + Gardien case 4 durant 5.1 !

    # 3) mem_debt_score : 1 modificateur transitoire traversant 3.2 -> 4.1 -> ... -> 6.2
    st_mem = GameState(cfg)
    trk_mem = TelemetryTracker()
    prim_mod_seuil(st_mem, -1, ray=0, p=2)
    st_mem.step = STEP_3_2_REVEAL
    _ = step_until_decision(st_mem, telemetry=trk_mem)
    assert trk_mem.summary().mem_debt_score >= 7

    # 4) Partie complète B1 et B2 en Mode 2 avec télémétrie active
    trk_game = TelemetryTracker()
    over_b2 = play_game_b2(GameState(cfg), telemetry=trk_game)
    s_game = trk_game.summary()
    assert 1 <= over_b2.tour_fin <= 8
    assert s_game.fiddliness_ratio > 0.0
    assert s_game.turns_measured == over_b2.tour_fin

    over_b1 = play_game_b1(GameState(cfg))
    assert 1 <= over_b1.tour_fin <= 8


# ---------------------------------------------------------------------------
# 5. Plans expérimentaux en blocs miroirs & Micro-Forks sans biais (campaigns/designs.py)
# ---------------------------------------------------------------------------
def test_paired_mirror_blocks_and_unbiased_micro_fork() -> None:
    blocks = paired_mirror_blocks(blocks_per_n=3, reps_per_side=3, exp_seed=202611)
    assert len(blocks) >= 12

    # Vérifier la présence exacte des 6 cercles obligatoires de couverture complète
    all_orientations_in_blocks: set[tuple[str, ...]] = set()
    for blk in blocks:
        assert len(blk.rep_ids) == 3
        assert blk.peuples[0] == blk.mirror_peuples[0]
        all_orientations_in_blocks.add(blk.peuples)
        all_orientations_in_blocks.add(blk.mirror_peuples)

    for cid, req_circle in MANDATORY_6_CIRCLES:
        rotations = {req_circle[i:] + req_circle[:i] for i in range(len(req_circle))}
        assert rotations & all_orientations_in_blocks, f"Cercle obligatoire manquant : {cid}"

    mean_v, se_v, hw_v = inter_block_ci95([0.62, 0.65, 0.60, 0.68, 0.64])
    assert 0.60 < mean_v < 0.68 and se_v > 0.0 and hw_v > se_v

    # Micro-Fork en début d'Étape 2.2 (séparation stricte sélection vs évaluation)
    recs = []
    for rep in range(3):
        cfg_mf = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "H", "I"),
            exp_seed=8080,
            rep_id=rep,
        )
        mf = run_micro_fork_on_config(
            cfg_mf, target_tour=2, is_b2=True, n_selection_rollouts=2, n_eval_rollouts=3
        )
        assert mf is not None
        assert mf.tour_anchor == 2
        assert -1.0 <= mf.delta_v_negociation <= 1.0
        assert -1.0 <= mf.c_prive <= 1.0
        assert -1.0 <= mf.rho_delta <= 1.0
        recs.append(mf)

    agg = aggregate_micro_forks(recs)
    assert agg.n_anchors == 3

    # Sequential Halving
    kept = sequential_halving_select({0: 0.71, 1: 0.52, 2: 0.69, 3: 0.48})
    assert kept == (0, 2)
