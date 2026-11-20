"""Tests témoins déterministes du Lot 10 (Croissance M4:A,B,D, M5:A..D, 7 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.effects import load_all_effects
from engine.effects.lot_10 import LOT_10_PROFILES
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
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    STEP_4_2_NIDS,
    STEP_4_3_MIGRATION,
    STEP_5_3_END_CHECK,
    TACTIQUES_SPEC,
    GameConfig,
    GameState,
)


def _make_state(
    *profiles: tuple[str, str],
    peuples: tuple[str, ...] = ("M", "R", "O", "I"),
) -> GameState:
    load_all_effects()
    cfg = GameConfig(
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
        tile_profiles=tuple(profiles),
    )
    return GameState(cfg)


def test_lot_10_all_7_profiles_registered() -> None:
    """Vérifie que les 7 profils du Lot 10 sont enregistrés (98 modules + 2 socle = 100/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_10_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 98


def test_m4_a_temoin_ruche_melipones_sabotage_4_2() -> None:
    """Témoin M4:A : défausse 1 Insecte en 4.2 pour +1 Sabotage (case 3), puis scan 1->6."""
    state = _make_state(("M4", "A"), ("G1", "A"), ("G10", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 4, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(i_seat, MACHINE_ABATTEUSE, 1, 0)
    state.set_gardien_at_case(3, 1, 1)
    state.place_defender_gardien_pari(0, 3, 2)
    state.set_gardien_at_case(6, 10, 1)
    state.place_defender_gardien_pari(1, 6, 2)
    sab_before = state.sabotage_pending_count

    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.context.get("slot_id") == "M4"
    assert "PASSER" in req.options
    assert "DILUER_SABOTAGE" in req.options

    apply_choice(state, "DILUER_SABOTAGE")
    assert state.get_parcel_insectes(i_seat, 1) == 0
    assert state.sabotage_pending_count == sab_before + 1
    assert state.is_trigger_lit(3) is True
    assert state.is_trigger_lit(6) is True

    # Balayage 1 -> 6 : G1 (case 3) s'ouvre avant G10 (case 6)
    req_g3 = step_until_decision(state)
    assert isinstance(req_g3, DecisionRequest)
    assert req_g3.context.get("slot_id") == "G1"
    assert state.count_gardien_pari_consumed_at_case(3) >= 1
    apply_choice(state, (0, 0))


def test_m4_b_temoin_piege_declenche_glisse_vers_coeur_5_3() -> None:
    """Témoin M4:B : en 5.3 (cœur->bordure), les Pièges déclenchés glissent d'1 cran sans allumer 2."""
    state = _make_state(("M4", "B"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 4, active_ce_tour=True)
    state.set_parcel_piege(i_seat, 1, PIEGE_DECLENCHE)
    state.set_parcel_piege(i_seat, 2, PIEGE_DECLENCHE)
    state.set_parcel_piege(i_seat, 4, PIEGE_ACTIF)

    state.step = STEP_5_3_END_CHECK
    step_until_decision(state)

    assert state.tour == 2
    assert state.get_parcel_piege(i_seat, 1) == PIEGE_AUCUN
    assert state.get_parcel_piege(i_seat, 2) == PIEGE_ACTIF
    assert state.get_parcel_piege(i_seat, 3) == PIEGE_ACTIF
    assert state.get_parcel_piege(i_seat, 4) == PIEGE_ACTIF
    assert state.is_trigger_lit(2) is False


def test_m4_d_temoin_melipones_convoyeurs_convoi_5_3() -> None:
    """Témoin M4:D : 1 fois/tour en 5.3, convoie 1 Piège déclenché + 1 Insecte vers le cœur."""
    state = _make_state(("M4", "D"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 4, active_ce_tour=True)
    state.set_parcel_piege(i_seat, 1, PIEGE_DECLENCHE)
    state.set_parcel_insectes(i_seat, 1, 2)
    state.set_parcel_piege(i_seat, 3, PIEGE_DECLENCHE)
    state.set_parcel_insectes(i_seat, 3, 1)

    state.step = STEP_5_3_END_CHECK
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.context.get("slot_id") == "M4"
    assert "PASSER" in req.options
    assert (1, 2) in req.options
    assert (3, 4) in req.options

    apply_choice(state, (1, 2))
    assert state.is_trigger_lit(2) is True
    assert state.has_slot_used_once_per_turn("M4") is True

    step_until_decision(state)
    assert state.get_parcel_piege(i_seat, 1) == PIEGE_AUCUN
    assert state.get_parcel_piege(i_seat, 2) == PIEGE_ACTIF
    assert state.get_parcel_insectes(i_seat, 1) == 1
    assert state.get_parcel_insectes(i_seat, 2) == 1
    # Le second piège déclenché en p=3 est retiré normalement en 5.3
    assert state.get_parcel_piege(i_seat, 3) == PIEGE_AUCUN


def test_m5_a_temoin_sanctuaire_souche_4_2_persiste_apres_destruction_nid() -> None:
    """Témoin M5:A : SANCTUAIRE_SOUCHE payable à 0 Souche, persiste jusqu'à la fin du tour."""
    state = _make_state(("M5", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 5, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    state.set_parcel_arbres_souches(i_seat, 1, 1, 0)

    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "M5"
    assert "SANCTUAIRE_SOUCHE" in req.options

    apply_choice(state, "SANCTUAIRE_SOUCHE")
    assert state.get_parcel_insectes(i_seat, 1) == 0

    # Destruction simulée du Nid, puis attaque d'un Bulldozer (2 rouge) sur la parcelle
    state.clear_nid(5)
    state.set_machine_pos_status(i_seat, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(i_seat, MACHINE_BULLDOZER, 2, 0)
    resolve_single_machine_attack(state, i_seat, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])

    # 1 Arbre coupé -> 1 Souche, préservée par SANCTUAIRE_SOUCHE malgré la disparition du Nid
    assert state.get_parcel_arbres(i_seat, 1) == 0
    assert state.get_parcel_souches(i_seat, 1) == 1
    assert state.is_route_forestiere(i_seat, 1) is False


def test_m5_b_temoin_tunnel_coeur_migration_directe_4_3() -> None:
    """Témoin M5:B : 1 fois/tour en 4.3, défausse 1 Insecte de M5 pour migrer vers Bug/Colonie."""
    state = _make_state(("M5", "B"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 5, active_ce_tour=True)
    state.set_parcel_insectes(i_seat, 1, 2)

    state.step = STEP_4_3_MIGRATION
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert ("BUG", 3) in req.options
    assert ("COLONIE", 2) in req.options

    apply_choice(state, ("BUG", 3))
    assert state.get_bugs_at_case(3) == 1
    assert state.get_parcel_insectes(i_seat, 1) == 0
    assert state.has_slot_used_once_per_turn("M5") is True


def test_m5_c_temoin_figuier_etrangleur_protege_souches_bulldozer() -> None:
    """Témoin M5:C : Bulldozer coupe 1 Arbre sur M5 mais ne terrasse aucune Souche."""
    state = _make_state(("M5", "C"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 5, active_ce_tour=True)
    state.set_parcel_arbres_souches(i_seat, 2, 1, 2)
    state.set_machine_pos_status(i_seat, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(i_seat, MACHINE_BULLDOZER, 3, 0)

    resolve_single_machine_attack(state, i_seat, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(i_seat, 2) == 0
    assert state.get_parcel_souches(i_seat, 2) == 3
    assert state.is_route_forestiere(i_seat, 2) is False


def test_m5_d_temoin_jardin_releveuses_cree_insecte_5_3_allume_6() -> None:
    """Témoin M5:D : si Piège déclenché sur M5 actif ce tour, crée 1 Insecte en 5.3 (allume 6)."""
    state = _make_state(("M5", "D"), ("G1", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 5, active_ce_tour=True)
    state.set_parcel_piege(i_seat, 2, PIEGE_DECLENCHE)
    state.set_parcel_insectes(i_seat, 2, 0)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(i_seat, MACHINE_ABATTEUSE, 1, 0)
    state.set_gardien_at_case(6, 1, 1)
    state.place_defender_gardien_pari(0, 6, 2)

    state.step = STEP_5_3_END_CHECK
    req = step_until_decision(state)
    assert state.get_parcel_insectes(i_seat, 2) == 1
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G1"
    # Vérifie que le Gardien en case 6 s'est ouvert grâce à M5:D avant 6.1
    assert state.count_gardien_pari_consumed_at_case(6) >= 1
