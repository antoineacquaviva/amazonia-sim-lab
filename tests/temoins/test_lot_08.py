"""Tests témoins déterministes du Lot 08 (Rêves R8:A..R10:D, 9 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.effects import load_all_effects
from engine.effects.lot_08 import LOT_08_PROFILES
from engine.effects.registry import get_tile_registration
from engine.primitives import (
    DEC_EFFET_TUILE,
    DecisionRequest,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    STEP_3_2_REVEAL,
    STEP_6_2_EVOLUTION,
    STEP_GAME_OVER,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
)


def _make_state(
    *profiles: tuple[str, str],
    peuples: tuple[str, ...] = ("M", "R", "O", "H", "E", "I"),
    regle_ouverture_reve_multiple: str = "UNIQUE_PAR_TOUR",
) -> GameState:
    load_all_effects()
    cfg = GameConfig(
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
        regle_ouverture_reve_multiple=regle_ouverture_reve_multiple,
        tile_profiles=tuple(profiles),
    )
    return GameState(cfg)


def _clear_hands(state: GameState) -> None:
    for s in range(state.cfg.n_players):
        state.set_player_hand(s, 0, 0, 0, 0, 0)


def _add_step_4_3_stop_anchor(state: GameState) -> None:
    """Place 1 Insecte témoin sur le dernier rayon pour arrêter step_until_decision en 4.3 avant 6.2."""
    last_r = state.cfg.n_players - 1
    if state.get_parcel_insectes(last_r, 1) == 0:
        state.set_parcel_insectes(last_r, 1, 1)


def _setup_reve_opening_3_2(
    state: GameState, r_num: int, rank_idx: int, *, reader_seat: int = 0
) -> None:
    _clear_hands(state)
    _add_step_4_3_stop_anchor(state)
    state.set_tactique_at_rank(rank_idx, TILE_R_BASE + r_num)
    act_seat = next(
        (s for s in range(state.cfg.n_players) if state.get_player_def_loc_raw(s, 1) == 0),
        reader_seat,
    )
    state.place_defender_reve_activation(act_seat, rank_idx + 1, 2)
    state.set_player_hand(reader_seat, 1, rank_idx + 1, rank_idx + 1, rank_idx + 1, 0)
    state.step = STEP_3_2_REVEAL


def test_lot_08_all_9_profiles_registered() -> None:
    """Vérifie que les 9 profils du Lot 08 sont enregistrés (79 modules + 2 socle = 81/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_08_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 79


def test_r8_a_temoin_mirage_fleuve_miroir_piege_er_3_2() -> None:
    """Témoin R8:A : pose 1 Piège sur une parcelle non rasée E ou R en 3.2 (allume la case 2)."""
    state = _make_state(("R8", "A"), peuples=("M", "R", "E", "I"))
    e_seat = state.cfg.seat_of_peuple("E")
    r_seat = state.cfg.seat_of_peuple("R")
    assert e_seat is not None and r_seat is not None

    state.set_gardien_at_case(2, 1, 1, False)
    _setup_reve_opening_3_2(state, 8, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert "PASSER" not in req.options
    assert (e_seat, 2) in req.options
    assert (r_seat, 1) in req.options

    apply_choice(state, (e_seat, 2))
    assert state.get_parcel_piege(e_seat, 2) == PIEGE_ACTIF
    step_until_decision(state)
    assert state.get_gardien_at_case(2)[2] is True


def test_r8_b_temoin_sanctuarisation_terrassement_er() -> None:
    """Témoin R8:B : sur E/R, un Bulldozer laisse 1 Souche si >= 1 Défenseur ou Insecte local."""
    state = _make_state(("R8", "B"), peuples=("M", "R", "E", "I"))
    e_seat = state.cfg.seat_of_peuple("E")
    r_seat = state.cfg.seat_of_peuple("R")
    assert e_seat is not None and r_seat is not None

    state.set_tactique_at_rank(2, TILE_R_BASE + 8)
    # Parcelle E avec 0 Arbre, 1 Souche et 1 Défenseur -> le Bulldozer ne rase pas en Route !
    state.set_parcel_arbres_souches(e_seat, 1, 0, 1)
    state.set_parcel_defenseurs(e_seat, 1, 1)
    state.set_machine_pos_status(e_seat, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)

    # Parcelle R avec 0 Arbre, 1 Souche et 0 Défenseur / 0 Insecte -> devient Route Forestière !
    state.set_parcel_arbres_souches(r_seat, 1, 0, 1)
    state.set_machine_pos_status(r_seat, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)

    resolve_single_machine_attack(state, e_seat, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_souches(e_seat, 1) == 1
    assert not state.is_route_forestiere(e_seat, 1)

    resolve_single_machine_attack(state, r_seat, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_souches(r_seat, 1) == 0
    assert state.is_route_forestiere(r_seat, 1)


def test_r8_c_temoin_mapinguari_recul_machines_annulees_3_2() -> None:
    """Témoin R8:C : chaque machine annulée par R8 en 3.2 recule d'1 parcelle (même en UNIQUE_PAR_TOUR)."""
    state = _make_state(("R8", "C"), regle_ouverture_reve_multiple="UNIQUE_PAR_TOUR")
    _clear_hands(state)
    _add_step_4_3_stop_anchor(state)
    state.set_tactique_at_rank(2, TILE_R_BASE + 8)

    # Deux joueurs lisent M=3 (R8) en mode UNIQUE_PAR_TOUR : les 2 machines doivent reculer !
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_player_hand(0, 1, 3, 3, 3, 0)  # ray 0, abatteuse
    state.set_player_hand(1, 4, 3, 3, 3, 0)  # ray 1, bulldozer
    state.step = STEP_3_2_REVEAL

    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert state.get_machine_pos_status(1, MACHINE_BULLDOZER)[0] == 1


def test_r8_d_temoin_berges_gardees_transfert_def_et_surchauffe() -> None:
    """Témoin R8:D : transfère 1 Défenseur E/R vers une parcelle piégée E/R puis +1 bleu sur cible."""
    state = _make_state(("R8", "D"), peuples=("M", "R", "E", "I"))
    e_seat = state.cfg.seat_of_peuple("E")
    r_seat = state.cfg.seat_of_peuple("R")
    assert e_seat is not None and r_seat is not None

    # Défenseur sur (r_seat, 1), Piège actif sur (e_seat, 2), Abatteuse E en (e_seat, 2) avec 2 rouges
    state.set_parcel_defenseurs(r_seat, 1, 1)
    state.set_parcel_piege(e_seat, 2, PIEGE_ACTIF)
    state.set_machine_pos_status(e_seat, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(e_seat, MACHINE_ABATTEUSE, 2, 0)

    _clear_hands(state)
    _add_step_4_3_stop_anchor(state)
    state.set_tactique_at_rank(0, 1)  # T1 = SUR_PLACE
    state.set_tactique_at_rank(3, TILE_R_BASE + 8)
    state.place_defender_reve_activation(0, 4, 2)
    # Joueur 0 ouvre R8 (M=4) ; Joueur 2 (E) lie Abatteuse E (card = e_seat*2 + 1 = 5) à T1 (M=1)
    state.set_player_hand(0, 1, 4, 4, 4, 0)
    state.set_player_hand(e_seat, e_seat * 2 + 1, 1, 1, 1, 0)
    state.step = STEP_3_2_REVEAL

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert "PASSER" in req.options
    move_opt = ((r_seat, 1), (e_seat, 2))
    assert move_opt in req.options

    apply_choice(state, move_opt)
    step_until_decision(state)
    assert state.get_parcel_defenseurs(r_seat, 1) == 0
    assert state.get_parcel_defenseurs(e_seat, 2) == 1
    assert state.get_machine_tokens(e_seat, MACHINE_ABATTEUSE) == (1, 1)


def test_r9_a_temoin_echo_voix_celestes_mod_seuil_rayon_moins_2() -> None:
    """Témoin R9:A : réduit de -2 le Seuil de Parade sur toutes les parcelles d'un rayon."""
    state = _make_state(("R9", "A"))
    e_seat = state.cfg.seat_of_peuple("E")
    assert e_seat is not None
    _setup_reve_opening_3_2(state, 9, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert req.options == tuple(range(state.cfg.n_players))

    apply_choice(state, 2)
    step_until_decision(state)
    for p in range(1, state.cfg.p_max + 1):
        assert state.get_parcel_seuil_mod_turn(2, p) == -2
    assert state.get_parcel_seuil_mod_turn(0, 1) == 0


def test_r9_b_temoin_echo_voix_celestes_egalite_6_2_declenche_repousse_finale() -> None:
    """R9:B neutralisé en v5.4.2 (Apprentissage supprimé ; à réajuster en Mode 4)."""
    state = _make_state(("R9", "B"))
    track = (TILE_R_BASE + 1, TILE_R_BASE + 2, TILE_R_BASE + 3, 4, TILE_R_BASE + 9, 6)
    for idx, code in enumerate(track):
        state.set_tactique_at_rank(idx, code)
    state.step = STEP_6_2_EVOLUTION
    _ = step_until_decision(state)
    assert state.get_tactique_at_rank(4) == TILE_R_BASE + 9
    assert state.step != STEP_GAME_OVER


def test_r10_a_temoin_nuee_songes_scaling_insectes_machine() -> None:
    """Témoin R10:A : réduit le Seuil d'1 machine de -1 par Insecte sur son rayon en 3.2."""
    state = _make_state(("R10", "A"))
    e_seat = state.cfg.seat_of_peuple("E")
    assert e_seat is not None

    # 3 Insectes sur le rayon 1 + Abatteuse 1 en jeu
    state.set_parcel_insectes(1, 2, 2)
    state.set_parcel_insectes(1, 3, 1)
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    _setup_reve_opening_3_2(state, 10, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert (1, MACHINE_ABATTEUSE) in req.options

    apply_choice(state, (1, MACHINE_ABATTEUSE))
    step_until_decision(state)
    assert state.get_machine_seuil_mod_turn(1, MACHINE_ABATTEUSE) == -3


def test_r10_b_temoin_conversion_insecte_roue_avancee_supplementaire() -> None:
    """Témoin R10:B : défausse 1 Insecte de la roue pour avancer R10 d'1 rang supplémentaire."""
    state = _make_state(("R10", "B"))
    e_seat = state.cfg.seat_of_peuple("E")
    assert e_seat is not None

    # R10 en Rang 4 (index 3) + 1 Insecte sur (0, 2) + 1 Insecte sur Bug 1 (exclu)
    track = (1, 2, 3, TILE_R_BASE + 10, 4, 5)
    for idx, code in enumerate(track):
        state.set_tactique_at_rank(idx, code)
    state.set_parcel_insectes(0, 2, 1)
    state.set_bugs_at_case(1, 1)
    _clear_hands(state)
    _add_step_4_3_stop_anchor(state)
    state.set_player_hand(0, 1, 4, 4, 4, 0)
    state.place_defender_reve_activation(0, 4, 2)
    state.step = STEP_3_2_REVEAL

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert "PASSER" in req.options
    assert ("FORET", 0, 2) in req.options

    apply_choice(state, ("FORET", 0, 2))
    step_until_decision(state)
    assert state.get_parcel_insectes(0, 2) == 0
    # +1 par conversion (3->2) et +1 par avancée normale (2->1) => index 1 (Rang 2)
    assert state.find_tactique_rank(TILE_R_BASE + 10) == 1


def test_r10_d_temoin_releve_lucioles_piege_et_deplacement_atomique() -> None:
    """Témoin R10:D : pose 1 Piège (E/I avec >=1 Déf & >=1 Ins) puis déplace 1 Insecte (allume 2)."""
    state = _make_state(("R10", "D"), peuples=("M", "R", "E", "I"))
    e_seat = state.cfg.seat_of_peuple("E")
    assert e_seat is not None

    state.set_parcel_defenseurs(e_seat, 1, 1)
    state.set_parcel_insectes(e_seat, 1, 1)
    state.set_gardien_at_case(2, 1, 1, False)
    _setup_reve_opening_3_2(state, 10, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == e_seat
    assert "PASSER" in req.options
    assert (e_seat, 1, 4) in req.options

    apply_choice(state, (e_seat, 1, 4))
    assert state.get_parcel_piege(e_seat, 1) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(e_seat, 1) == 1
    assert state.get_parcel_insectes(e_seat, 1) == 0
    assert state.get_parcel_insectes(e_seat, 4) == 1

    step_until_decision(state)
    assert state.get_gardien_at_case(2)[2] is True
