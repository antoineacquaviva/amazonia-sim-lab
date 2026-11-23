"""Tests dédiés aux règles consolidées du châssis unique v6.1 :
1. Châssis unique P4_2233 (4 parcelles 2-2-3-3, 10 arbres/rayon) et départ décalé (Bulldozer p=1, Abatteuse p=2).
2. Condition de victoire Sommeil du Contremaître (Mode 4) : tous les Rêves en jeu
   (2 × peuples oniriques = 0, 2 ou 4) en bloc contigu en tête de piste.
3. Ratissage : bascule uniquement en 6.3, +1 puissance rouge imprimé conservant les rouges acquis,
   T1 Sur place systématique et piste T1..T6 fixe.
"""

from __future__ import annotations

from engine.core_engine import (
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.primitives import CAUSE_REVE_RANG_1, GameOver
from engine.state import (
    ABATTEUSE_INIT_PARCEL,
    BULLDOZER_INIT_PARCEL,
    CANONICAL_ARBRES_PAR_RAYON,
    CANONICAL_DOTATION,
    CANONICAL_P_MAX,
    CANONICAL_PROFIL_PISTE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    STEP_6_3_END_TURN,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    code_to_tile_id,
)


def test_v6_1_canonical_track_p4_2233_and_split_machine_placement() -> None:
    cfg = GameConfig(n_players=4, mode=1, exp_seed=5401)
    assert cfg.profil_piste == CANONICAL_PROFIL_PISTE == "P4_2233"
    assert cfg.p_max == CANONICAL_P_MAX == 4
    assert cfg.dotation_arbres == CANONICAL_DOTATION == (2, 2, 3, 3)

    state = GameState(cfg)
    total_trees = 0
    for ray in range(4):
        assert state.get_machine_pos_status(ray, MACHINE_BULLDOZER) == (
            BULLDOZER_INIT_PARCEL,
            MACHINE_STATUS_NORMAL,
            False,
        )
        assert state.get_machine_pos_status(ray, MACHINE_ABATTEUSE) == (
            ABATTEUSE_INIT_PARCEL,
            MACHINE_STATUS_NORMAL,
            False,
        )
        for p in range(1, CANONICAL_P_MAX + 1):
            arbres = state.get_parcel_arbres(ray, p)
            assert arbres == CANONICAL_DOTATION[p - 1]
            total_trees += arbres
    assert total_trees == 4 * CANONICAL_ARBRES_PAR_RAYON


def test_v6_1_sommeil_victory_zero_one_two_oniric_peoples() -> None:
    # 0 peuple onirique -> impossible (total_reves_partie == 0)
    st0 = GameState(GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"), exp_seed=5403))
    assert st0.cfg.total_reves_partie == 0
    st0.set_tactique_at_rank(0, TILE_R_BASE + 1)
    assert st0.is_sommeil_victory() is False

    # 1 peuple onirique (H) -> 2 Rêves en bloc en [0, 1]
    st1 = GameState(GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=5404))
    assert st1.cfg.total_reves_partie == 2
    st1.set_tactique_at_rank(0, TILE_R_BASE + 1)
    assert st1.is_sommeil_victory() is False  # 1 seul Rêve en tête

    st1.set_tactique_at_rank(2, TILE_R_BASE + 2)
    assert st1.is_sommeil_victory() is False  # 2 Rêves non contigus ([0, 2])

    st1.set_tactique_at_rank(0, 1)
    st1.set_tactique_at_rank(1, TILE_R_BASE + 1)
    st1.set_tactique_at_rank(2, TILE_R_BASE + 2)
    assert st1.is_sommeil_victory() is False  # Bloc [1, 2] mais pas en tête

    st1.set_tactique_at_rank(0, TILE_R_BASE + 1)
    st1.set_tactique_at_rank(1, TILE_R_BASE + 2)
    assert st1.is_sommeil_victory() is True
    st1.step = STEP_5_3_END_CHECK
    over1 = step_until_decision(st1)
    assert isinstance(over1, GameOver)
    assert over1.cause_fin == CAUSE_REVE_RANG_1

    # 2 peuples oniriques (H, E) -> 4 Rêves en bloc en [0, 1, 2, 3]
    st2 = GameState(GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), exp_seed=5405))
    assert st2.cfg.total_reves_partie == 4
    for idx, r_num in enumerate((1, 2, 3)):
        st2.set_tactique_at_rank(idx, TILE_R_BASE + r_num)
    assert st2.is_sommeil_victory() is False  # 3/4 Rêves seulement

    st2.set_tactique_at_rank(4, TILE_R_BASE + 4)
    assert st2.is_sommeil_victory() is False  # Trou à l'index 3

    st2.set_tactique_at_rank(3, TILE_R_BASE + 4)
    assert st2.is_sommeil_victory() is True


def test_v6_1_ratissage_flip_6_3_printed_red_and_fixed_track() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=5406)
    state = GameState(cfg)
    # Abatteuse sur la dernière parcelle (p=4) avec 1 jeton Rouge physique déjà acquis
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    # Bulldozer aussi en p=4, Normal, 0 rouge
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_NORMAL)

    # Bascule en Ratissage permanent exclusivement en 6.3
    state.step = STEP_6_3_END_TURN
    step_until_decision(state)
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE) == (
        4,
        MACHINE_STATUS_RATISSAGE,
        False,
    )
    assert state.get_machine_pos_status(0, MACHINE_BULLDOZER) == (
        4,
        MACHINE_STATUS_RATISSAGE,
        False,
    )

    # Conservation des jetons rouges physiques + ajout du +1 rouge imprimé
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)
    assert state.get_machine_effective_rouges(0, MACHINE_ABATTEUSE) == 2
    assert state.get_machine_effective_rouges(0, MACHINE_BULLDOZER) == 1

    # Mode individuel v6.1 : Seuil Abatteuse = base(3) + T1(0) + 2 rouges effectifs = 5 !
    # Avec 4 Défenseurs -> attaque non parée ; avec 5 Défenseurs -> parée.
    state.set_parcel_defenseurs(0, 4, 4)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_arbres(0, 4) == 0  # Coupe tous les Arbres debout de la parcelle
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)  # T1: gain_rouge=0

    state.set_parcel_arbres_souches(0, 4, 3, 0)
    state.set_parcel_defenseurs(0, 4, 5)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_arbres(0, 4) == 3

    # Piste fixe T1..T6 : le Ratissage applique T1 en 5.2 sans déplacer les Tactiques en Étape 6
    st_fixed = GameState(cfg)
    st_fixed.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_fixed.step = STEP_5_2_RATISSAGE
    step_until_decision(st_fixed)
    assert [code_to_tile_id(st_fixed.get_tactique_at_rank(i)) for i in range(6)] == [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
    ]
