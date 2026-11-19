"""Tests dédiés aux évolutions de règles v5.4.

Couvre les 4 axes d'évolution v5.4 :
1. 6 profils de pistes (`P4_2233`, `P4_2223`, `P4_1223`, `P5_22233`, `P5_22223`, `P5_12223`).
2. Option de placement initial des machines (`MEME_PARCELLE_P1` vs `BULLDOZER_P1_ABATTEUSE_P2`),
   remplaçant `DEPASSEMENT_DERNIERE_PARCELLE` (supprimée) — espace 384 configurations.
3. Nouvelle règle de victoire Sommeil du Contremaître : tous les Rêves en jeu
   (2 × peuples oniriques = 0, 2 ou 4) en bloc contigu en tête de piste.
4. Passage « Siège » → « Ratissage » : retournement permanent en dernière parcelle non rasée,
   +1 puissance rouge imprimé (traité comme +1 rouge à tous égards, conservant les rouges acquis),
   T1 Sur place systématique et alimentation de T1 en 6.1 Apprentissage.
"""

from __future__ import annotations

import pytest

from campaigns.digest_builder import (
    chassis_id_to_studio_index_384,
    studio_index_384_to_chassis_id,
)
from engine.core_engine import (
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.primitives import CAUSE_REVE_RANG_1, GameOver
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    NUM_CHASSIS,
    STEP_1_1_RATISSAGE,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TOPOLOGIES_DOTATION,
    GameConfig,
    GameState,
    code_to_tile_id,
    decode_chassis_index,
)


@pytest.mark.parametrize(
    ("profil", "expected_p_max", "expected_dotation"),
    [
        ("P4_2233", 4, (2, 2, 3, 3)),
        ("P4_2223", 4, (2, 2, 2, 3)),
        ("P4_1223", 4, (1, 2, 2, 3)),
        ("P5_22233", 5, (2, 2, 2, 3, 3)),
        ("P5_22223", 5, (2, 2, 2, 2, 3)),
        ("P5_12223", 5, (1, 2, 2, 2, 3)),
    ],
)
def test_v5_4_six_track_profiles_setup(
    profil: str, expected_p_max: int, expected_dotation: tuple[int, ...]
) -> None:
    assert TOPOLOGIES_DOTATION[profil] == expected_dotation
    cfg = GameConfig(n_players=4, mode=1, profil_piste=profil, exp_seed=5401)
    assert cfg.p_max == expected_p_max
    assert cfg.dotation_arbres == expected_dotation

    state = GameState(cfg)
    total_trees = 0
    for ray in range(4):
        for p in range(1, expected_p_max + 1):
            arbres = state.get_parcel_arbres(ray, p)
            assert arbres == expected_dotation[p - 1]
            total_trees += arbres
    assert total_trees == 4 * sum(expected_dotation)


def test_v5_4_initial_machine_placement_options() -> None:
    cfg_same = GameConfig(
        n_players=4,
        mode=1,
        placement_initial_machines="MEME_PARCELLE_P1",
        exp_seed=5402,
    )
    st_same = GameState(cfg_same)
    for ray in range(4):
        assert st_same.get_machine_pos_status(ray, MACHINE_BULLDOZER) == (
            1,
            MACHINE_STATUS_NORMAL,
            False,
        )
        assert st_same.get_machine_pos_status(ray, MACHINE_ABATTEUSE) == (
            1,
            MACHINE_STATUS_NORMAL,
            False,
        )

    cfg_split = GameConfig(
        n_players=4,
        mode=1,
        placement_initial_machines="BULLDOZER_P1_ABATTEUSE_P2",
        exp_seed=5402,
    )
    st_split = GameState(cfg_split)
    for ray in range(4):
        assert st_split.get_machine_pos_status(ray, MACHINE_BULLDOZER) == (
            1,
            MACHINE_STATUS_NORMAL,
            False,
        )
        assert st_split.get_machine_pos_status(ray, MACHINE_ABATTEUSE) == (
            2,
            MACHINE_STATUS_NORMAL,
            False,
        )


def test_v5_4_chassis_384_bijection() -> None:
    assert NUM_CHASSIS == 384
    seen_studio: set[int] = set()
    for cid in range(NUM_CHASSIS):
        decoded = decode_chassis_index(cid)
        assert decoded["profil_piste"] in TOPOLOGIES_DOTATION
        assert decoded["placement_initial_machines"] in (
            "MEME_PARCELLE_P1",
            "BULLDOZER_P1_ABATTEUSE_P2",
        )
        sidx = chassis_id_to_studio_index_384(cid)
        assert 1 <= sidx <= 384
        assert studio_index_384_to_chassis_id(sidx) == cid
        seen_studio.add(sidx)
    assert len(seen_studio) == 384


def test_v5_4_sommeil_victory_zero_one_two_oniric_peoples() -> None:
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


def test_v5_4_ratissage_flip_printed_red_mutualisation_and_t1_learning() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=2,
        profil_piste="P4_2233",
        synergie_binome_machines="MUTUALISATION_PUISSANCE_MEME_PARCELLE",
        exp_seed=5406,
    )
    state = GameState(cfg)
    # Abatteuse sur la dernière parcelle (p=4) avec 1 jeton Rouge physique déjà acquis
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    # Bulldozer aussi en p=4, Normal, 0 rouge
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_NORMAL)

    # Étape 1.1 : les deux machines sur la dernière parcelle passent en Ratissage permanent
    state.step = STEP_1_1_RATISSAGE
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

    # Mutualisation sur la même parcelle : Seuil = base(3) + T1(0) + (2 + 1) rouges effectifs = 6 !
    # Avec 5 Défenseurs, l'attaque n'est PAS parée ; avec 6 Défenseurs, elle est parée.
    state.set_parcel_defenseurs(0, 4, 5)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_arbres(0, 4) == 1  # 3 - 2 = 1 Arbre coupé
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)  # T1: gain_rouge=0

    # Retour à 3 Arbres + 6 Défenseurs -> parée !
    state.set_parcel_arbres_souches(0, 4, 3, 0)
    state.set_parcel_defenseurs(0, 4, 6)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_arbres(0, 4) == 3

    # Alimentation de T1 en 6.1 Apprentissage : placer T1 en rang 1 (index 1) sur un état propre
    st_learn = GameState(cfg)
    st_learn.set_tactique_at_rank(0, 2)
    st_learn.set_tactique_at_rank(1, 1)
    st_learn.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_learn.step = STEP_5_2_RATISSAGE
    # Exécuter 5.2 -> 5.3 -> 6.1 -> 6.2 -> Tour 2
    step_until_decision(st_learn)
    assert code_to_tile_id(st_learn.get_tactique_at_rank(0)) == "T1"
