"""Tests témoins déterministes du Lot 07 (Rêves R5:B..R7:C, 10 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    apply_repousse_finale,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.effects import load_all_effects
from engine.effects.lot_07 import LOT_07_PROFILES
from engine.effects.registry import get_tile_registration
from engine.primitives import (
    DEC_EFFET_TUILE,
    HOOK_5_LAW_QUERY,
    DecisionRequest,
    dispatch_hook,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PIEGE_ACTIF,
    PIEGE_DECLENCHE,
    STEP_1_3_DICE,
    STEP_3_2_REVEAL,
    STEP_4_3_MIGRATION,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
)


def _make_state(
    *profiles: tuple[str, str],
    peuples: tuple[str, ...] = ("M", "R", "O", "H", "E", "I"),
) -> GameState:
    load_all_effects()
    cfg = GameConfig(
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
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


def test_lot_07_all_10_profiles_registered() -> None:
    """Vérifie que les 10 profils du Lot 07 sont enregistrés (total cumulé : 72/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_07_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 70


def test_r5_b_temoin_plumes_claires_humains_max_d1_d2() -> None:
    """Témoin R5:B : en 1.3, les Humains peuvent retenir max(D1, D2) pour cibler un Rêve en fin de piste."""
    state = _make_state(("R5", "B"))
    h_seat = state.cfg.seat_of_peuple("H")
    assert h_seat is not None
    state.set_tactique_at_rank(5, TILE_R_BASE + 5)
    state.set_player_hand(h_seat, 1, 0, 0, 0, 0)

    state.step = STEP_1_3_DICE
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == h_seat
    assert req.options == ("PASSER", "RETENIR_MAX")

    _, d1, d2, _, _ = state.get_player_hand(h_seat)
    apply_choice(state, "RETENIR_MAX")
    _, _, _, lec_m, _ = state.get_player_hand(h_seat)
    assert lec_m == max(d1, d2)


def test_r5_c_temoin_reve_nid_vide_piege_cible_vide_ho() -> None:
    """Témoin R5:C : pose 1 Piège sur une parcelle ciblée H/O vide (allume la case 2)."""
    state = _make_state(("R5", "C"), peuples=("M", "O", "H", "I"))
    o_seat = state.cfg.seat_of_peuple("O")
    h_seat = state.cfg.seat_of_peuple("H")
    assert o_seat is not None and h_seat is not None

    # Machine O en Siège sur (o_seat, 2) -> parcelle ciblée et vide ; (h_seat, 1) non ciblée
    state.set_machine_pos_status(o_seat, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_RATISSAGE)
    state.set_tactique_at_rank(4, TILE_R_BASE + 5)
    state.place_defender_reve_activation(0, 5, 2)
    _clear_hands(state)
    _add_step_4_3_stop_anchor(state)
    state.set_player_hand(0, 1, 5, 5, 5, 0)  # M cible (0,1) qui n'est pas H/O
    state.step = STEP_3_2_REVEAL

    # Placer un Gardien G1 (effet neutre car non enregistré ici) sur la case 2 pour vérifier le déclencheur 2
    state.set_gardien_at_case(2, 1, 1, False)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == h_seat
    assert req.options == ("PASSER", (o_seat, 2))

    apply_choice(state, (o_seat, 2))
    assert state.get_parcel_piege(o_seat, 2) == PIEGE_ACTIF
    step_until_decision(state)
    # La case 2 allumée a ouvert le Gardien en case 2 !
    assert state.get_gardien_at_case(2)[2] is True

    # Avant la frappe, 1 Défenseur suffit à déclencher l'Embuscade
    state.set_parcel_defenseurs(o_seat, 2, 1)
    resolve_single_machine_attack(state, o_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_piege(o_seat, 2) == PIEGE_DECLENCHE


def test_r5_d_temoin_reve_veilleur_arme_piege_ho() -> None:
    """Témoin R5:D : crée 1 Insecte sur une parcelle piégée H/O (allume la case 6)."""
    state = _make_state(("R5", "D"), peuples=("M", "O", "H", "I"))
    o_seat = state.cfg.seat_of_peuple("O")
    h_seat = state.cfg.seat_of_peuple("H")
    assert o_seat is not None and h_seat is not None

    state.set_parcel_piege(o_seat, 3, PIEGE_ACTIF)
    state.set_gardien_at_case(6, 1, 1, False)
    _setup_reve_opening_3_2(state, 5, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == h_seat
    assert req.options == ("PASSER", (o_seat, 3))

    apply_choice(state, (o_seat, 3))
    assert state.get_parcel_insectes(o_seat, 3) == 1
    step_until_decision(state)
    assert state.get_gardien_at_case(6)[2] is True


def test_r6_a_temoin_miel_ancetres_pose_insecte_hi_3_2() -> None:
    """Témoin R6:A : pose 1 Insecte sur une parcelle non rasée H ou I en 3.2 (allume la case 6)."""
    state = _make_state(("R6", "A"), peuples=("M", "R", "H", "I"))
    h_seat = state.cfg.seat_of_peuple("H")
    i_seat = state.cfg.seat_of_peuple("I")
    assert h_seat is not None and i_seat is not None

    state.set_gardien_at_case(6, 1, 1, False)
    _setup_reve_opening_3_2(state, 6, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == h_seat
    assert "PASSER" not in req.options
    assert (h_seat, 2) in req.options
    assert (i_seat, 1) in req.options

    apply_choice(state, (h_seat, 2))
    assert state.get_parcel_insectes(h_seat, 2) == 1
    step_until_decision(state)
    assert state.get_gardien_at_case(6)[2] is True


def test_r6_b_temoin_miel_ancetres_active_nid_insectes_sans_bloquer_4_2() -> None:
    """Témoin R6:B : déclenche la création d'Insectes d'1 Nid en 3.2 (+1/+2, allume 6) sans bloquer 4.2."""
    state = _make_state(("R6", "B"), ("M1", "B"), peuples=("M", "R", "H", "I"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    # Nid M1 en (i_seat, 2) avec 2 Insectes et 1 Défenseur :
    # En 3.2, R6:B produit +2 Insectes (2 -> 4) et laisse active_ce_tour=False ;
    # En 4.2, le Nid s'active normalement et produit +2 Insectes supplémentaires (4 -> 6) !
    state.set_parcel_nid(i_seat, 2, 1, active_ce_tour=False)
    state.set_parcel_insectes(i_seat, 2, 2)
    state.set_parcel_defenseurs(i_seat, 2, 1)
    state.set_gardien_at_case(6, 1, 1, False)
    _setup_reve_opening_3_2(state, 6, 3, reader_seat=0)

    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_insectes(i_seat, 2) == 6
    assert state.get_nid_position(1) == (i_seat, 2, True)
    assert state.get_gardien_at_case(6)[2] is True


def test_r6_c_temoin_terra_preta_repousse_deux_souches_hi() -> None:
    """Témoin R6:C : une parcelle H avec 3 Souches rend 2 Arbres debout au décompte final."""
    state = _make_state(("R6", "C"), peuples=("M", "R", "H", "I"))
    h_seat = state.cfg.seat_of_peuple("H")
    r_seat = state.cfg.seat_of_peuple("R")
    assert h_seat is not None and r_seat is not None

    state.set_tactique_at_rank(2, TILE_R_BASE + 6)
    # Parcelle (h_seat, 3) dotation 3 : 0 Arbre, 3 Souches -> +2 Arbres
    state.set_parcel_arbres_souches(h_seat, 3, 0, 3)
    # Parcelle (r_seat, 3) hors H/I : 0 Arbre, 3 Souches -> +1 Arbre seulement
    state.set_parcel_arbres_souches(r_seat, 3, 0, 3)

    assert dispatch_hook(state, HOOK_5_LAW_QUERY, {"ray": h_seat}) == [True]
    apply_repousse_finale(state)
    assert state.get_parcel_arbres(h_seat, 3) == 2
    assert state.get_parcel_souches(h_seat, 3) == 1
    assert state.get_parcel_arbres(r_seat, 3) == 1


def test_r6_d_temoin_chemins_veilleur_nid_vers_piege_4_3() -> None:
    """Témoin R6:D : en 4.3, un Insecte quittant un Nid H/I rejoint directement une parcelle piégée."""
    state = _make_state(("R6", "D"), peuples=("M", "R", "H", "I"))
    h_seat = state.cfg.seat_of_peuple("H")
    assert h_seat is not None

    state.set_tactique_at_rank(2, TILE_R_BASE + 6)
    state.set_parcel_nid(h_seat, 1, 1, active_ce_tour=False)
    state.set_parcel_insectes(h_seat, 1, 1)
    state.set_parcel_piege(h_seat, 4, PIEGE_ACTIF)

    state.step = STEP_4_3_MIGRATION
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert ("FORET", h_seat, 4) in req.options

    apply_choice(state, ("FORET", h_seat, 4))
    assert state.get_parcel_insectes(h_seat, 1) == 0
    assert state.get_parcel_insectes(h_seat, 4) == 1


def test_r7_a_temoin_ombre_maitre_bois_recul_machine_em_3_2() -> None:
    """Témoin R7:A : fait reculer d'1 parcelle non rasée vers la bordure une machine hors Siège sur E ou M."""
    state = _make_state(("R7", "A"))
    e_seat = state.cfg.seat_of_peuple("E")
    m_seat = state.cfg.seat_of_peuple("M")
    assert e_seat is not None and m_seat is not None

    # Abatteuse E en p=3 (p=2 rasée -> recul vers p=1 !) ; Abatteuse M en Ratissage (exclue)
    state.set_parcel_arbres_souches(e_seat, 2, 0, 0)
    state.set_machine_pos_status(e_seat, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(m_seat, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_RATISSAGE)
    _setup_reve_opening_3_2(state, 7, 3, reader_seat=0)

    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_machine_pos_status(e_seat, MACHINE_ABATTEUSE)[0] == 1
    assert state.get_machine_pos_status(m_seat, MACHINE_ABATTEUSE)[0] == 3


def test_r7_b_temoin_endiguement_ratissage_em_et_voisins() -> None:
    """Témoin R7:B (v5.4) : machines en Ratissage sur E/M et voisins ont -1 Seuil de Parade (plancher 1)."""
    state = _make_state(("R7", "B"), peuples=("M", "R", "O", "H", "E", "I"))
    e_seat = state.cfg.seat_of_peuple("E")
    o_seat = state.cfg.seat_of_peuple("O")
    assert e_seat is not None and o_seat is not None
    # Voisin de E (seat 4) = H (seat 3) et I (seat 5) ; O (seat 2) n'est ni E/M ni voisin
    h_seat = state.cfg.seat_of_peuple("H")
    assert h_seat is not None

    state.set_tactique_at_rank(2, TILE_R_BASE + 7)
    # Parcelle 4 dotation 3, offset 0, T1 mod_seuil 0, Ratissage +1 rouge imprimé -> Seuil normal = 4 ; avec R7:B = 3 !
    state.set_machine_pos_status(h_seat, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    state.set_parcel_defenseurs(h_seat, 4, 3)

    state.set_machine_pos_status(o_seat, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    state.set_parcel_defenseurs(o_seat, 4, 3)

    resolve_single_machine_attack(state, h_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    # Sur H (voisin de E) : parée grâce au -1 Seuil (Seuil=3 <= 3 Déf) !
    assert state.get_parcel_arbres(h_seat, 4) == state.cfg.dotation_arbres[3]
    assert state.get_machine_tokens(h_seat, MACHINE_ABATTEUSE)[0] == 0

    resolve_single_machine_attack(state, o_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    # Sur O (hors E/M et voisins) : non parée (Seuil=4 > 3 Déf) -> Abatteuse coupe 2 Arbres (T1: 0 rouge ajouté)
    assert state.get_parcel_arbres(o_seat, 4) == state.cfg.dotation_arbres[3] - 2
    assert state.get_machine_tokens(o_seat, MACHINE_ABATTEUSE)[0] == 0


def test_r7_c_temoin_bras_mort_fleuve_passage_direct_em_4_3() -> None:
    """Témoin R7:C : en 4.3, un Insecte traverse directement entre E et M à la même profondeur."""
    state = _make_state(("R7", "C"))
    e_seat = state.cfg.seat_of_peuple("E")
    m_seat = state.cfg.seat_of_peuple("M")
    assert e_seat is not None and m_seat is not None

    state.set_tactique_at_rank(2, TILE_R_BASE + 7)
    state.set_parcel_insectes(e_seat, 3, 1)

    state.step = STEP_4_3_MIGRATION
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert ("FORET", m_seat, 3) in req.options

    apply_choice(state, ("FORET", m_seat, 3))
    assert state.get_parcel_insectes(e_seat, 3) == 0
    assert state.get_parcel_insectes(m_seat, 3) == 1
