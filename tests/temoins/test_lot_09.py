"""Tests témoins déterministes du Lot 09 (Croissance M1:A..M3:D, 12 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.effects import load_all_effects
from engine.effects.lot_09 import LOT_09_PROFILES
from engine.effects.registry import get_tile_registration
from engine.primitives import (
    DEC_EFFET_TUILE,
    DecisionRequest,
    prim_deplacement,
)
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    PIEGE_DECLENCHE,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
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


def test_lot_09_all_12_profiles_registered() -> None:
    """Vérifie que les 12 profils du Lot 09 sont enregistrés (91 modules + 2 socle = 93/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_09_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 91


def test_m1_a_temoin_fourmiliere_deplace_defenseur_avant_balayage_6() -> None:
    """Témoin M1:A : après production en 4.2, déplace 1 Défenseur de M1 avant le balayage de la case 6."""
    state = _make_state(("M1", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 1, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    state.set_gardien_at_case(6, 1, 1)
    state.place_defender_gardien_pari(0, 6, 2)

    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == i_seat
    assert (0, 3) in req.options
    # La case 6 n'est pas encore balayée pendant la suspension du bloc indivisible du Nid !
    assert state.count_gardien_pari_consumed_at_case(6) == 0

    apply_choice(state, (0, 3))
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_defenseurs(i_seat, 1) == 0
    assert state.get_parcel_defenseurs(0, 3) == 1
    assert state.count_gardien_pari_consumed_at_case(6) >= 1


def test_m1_b_temoin_carapaces_epargne_1_insecte_parade_classique() -> None:
    """Témoin M1:B : 1 fois/tour sur M1 avec >=1 Défenseur, épargne 1 Insecte défaussé en Parade."""
    state = _make_state(("M1", "B"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    # Parcelle (i_seat, 4) dotation 3 -> T1 Seuil = 3 ; 1 Défenseur + 2 Insectes -> manque = 2 -> épargne 1 (1 défaussé)
    state.set_parcel_nid(i_seat, 4, 1, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 4, 1)
    state.set_parcel_insectes(i_seat, 4, 2)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)

    resolve_single_machine_attack(state, i_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_insectes(i_seat, 4) == 1
    assert state.get_parcel_arbres(i_seat, 4) == state.cfg.dotation_arbres[3]
    assert state.has_slot_used_once_per_turn("M1")


def test_m1_c_temoin_fourmis_legionnaires_migration_globale_des_4_3() -> None:
    """Témoin M1:C : envoie 1 Insecte sur la dernière parcelle en 4.2 -> peut migrer vers Bug/Colonie en 4.3."""
    state = _make_state(("M1", "C"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None
    last_p = state.cfg.p_max

    state.set_parcel_nid(i_seat, 1, 1, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)

    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == i_seat
    assert "PASSER" in req.options
    assert last_p in req.options

    apply_choice(state, last_p)
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert ("BUG", 1) in req_mig.options
    assert ("COLONIE", 1) in req_mig.options


def test_m1_d_temoin_fourmis_sentinelles_arment_2_pieges_en_4_2() -> None:
    """Témoin M1:D : envoie jusqu'à 2 Insectes de M1 vers 2 Pièges distincts du rayon en 4.2."""
    state = _make_state(("M1", "D"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 1, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    state.set_parcel_insectes(i_seat, 1, 1)  # >=1 -> produit +1 => 2 Insectes sur M1
    state.set_parcel_piege(i_seat, 2, PIEGE_ACTIF)
    state.set_parcel_piege(i_seat, 4, PIEGE_ACTIF)

    state.step = STEP_4_2_NIDS
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decision_type == DEC_EFFET_TUILE
    assert req1.options == ("PASSER", 2, 4)

    apply_choice(state, 2)
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert req2.decision_type == DEC_EFFET_TUILE
    assert req2.options == ("PASSER", 4)

    apply_choice(state, 4)
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_insectes(i_seat, 1) == 0
    assert state.get_parcel_insectes(i_seat, 2) == 1
    assert state.get_parcel_insectes(i_seat, 4) == 1


def test_m2_a_temoin_termitiere_glu_surchauffe_voisine_4_2() -> None:
    """Témoin M2:A : après production en 4.2, retourne 1 rouge en bleu sur rayon ou voisin."""
    state = _make_state(("M2", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 2, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    # Machine voisine sur rayon 0 avec 2 rouges
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, 2, 0)

    state.step = STEP_4_2_NIDS
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)


def test_m2_b_temoin_termitiere_glu_insecte_furtif_permanent_4_1() -> None:
    """Témoin M2:B : en 4.1 sur les lisières bordant M2, l'Insecte du binôme n'est pas défaussé."""
    state = _make_state(("M2", "B"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 2, active_ce_tour=False)
    # Lisière i_seat (droite) : 1 Défenseur rive 0 + 1 Insecte furtif
    state.enter_furtivite(0, 0, i_seat, 2, 0, FACE_DEFINITIF)
    state.set_furtivite_insectes(i_seat, 2, 1)

    state.step = STEP_4_1_FURTIVITE
    step_until_decision(state)
    assert state.get_parcel_piege(i_seat, 2) == PIEGE_ACTIF
    assert state.get_furtivite_insectes(i_seat, 2) == 1


def test_m2_c_temoin_souche_creuse_survit_contact_si_souche() -> None:
    """Témoin M2:C : le Nid M2 et ses Insectes survivent au contact si >= 1 Souche locale."""
    state = _make_state(("M2", "C"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 2, active_ce_tour=False)
    state.set_parcel_insectes(i_seat, 2, 2)
    state.set_parcel_arbres_souches(i_seat, 2, 1, 1)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)

    prim_deplacement(
        state, "MACHINE", src_ray=i_seat, m_type=MACHINE_ABATTEUSE, dst_ray=i_seat, dst_p=2
    )
    assert state.get_nid_position(2) == (i_seat, 2, False)
    assert state.get_parcel_insectes(i_seat, 2) == 2


def test_m2_d_temoin_termitiere_gardee_survit_piege_declenche_si_presence() -> None:
    """Témoin M2:D : survit si Piège (même déclenché) + >=1 Déf/Ins ; sinon retourne en lisière."""
    state = _make_state(("M2", "D"), peuples=("M", "O", "R", "I"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 2, active_ce_tour=False)
    state.set_parcel_piege(i_seat, 2, PIEGE_DECLENCHE)
    state.set_parcel_insectes(i_seat, 2, 1)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)

    prim_deplacement(
        state, "MACHINE", src_ray=i_seat, m_type=MACHINE_ABATTEUSE, dst_ray=i_seat, dst_p=2
    )
    assert state.get_nid_position(2) == (i_seat, 2, False)

    # Sans Défenseur ni Insecte sur le Nid -> retourne en lisière !
    state.set_parcel_insectes(i_seat, 2, 0)
    prim_deplacement(
        state, "MACHINE", src_ray=i_seat, m_type=MACHINE_ABATTEUSE, dst_ray=i_seat, dst_p=2
    )
    assert state.get_nid_position(2) is None
    m2_slot = state.find_lisiere_slot_by_tile_id("M2")
    assert m2_slot is not None
    assert state.get_lisiere_tile_state(m2_slot) == (LISIERE_UNCONSTRUCTED, 0)


def test_m3_a_temoin_guepes_cazadores_2_insectes_1cran_avant_4_3() -> None:
    """Témoin M3:A : après production en 4.2, déplace d'1 cran jusqu'à 2 Insectes (portée 2 crans)."""
    state = _make_state(("M3", "A"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 1, 3, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 1, 1)
    state.set_parcel_insectes(i_seat, 1, 1)  # +1 en 4.2 => 2 Insectes sur M3

    state.step = STEP_4_2_NIDS
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decision_type == DEC_EFFET_TUILE
    assert ("FORET", i_seat, 2) in req1.options

    apply_choice(state, ("FORET", i_seat, 2))
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert req2.decision_type == DEC_EFFET_TUILE

    apply_choice(state, ("FORET", i_seat, 2))
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_insectes(i_seat, 1) == 0
    assert state.get_parcel_insectes(i_seat, 2) == 2


def test_m3_b_temoin_pouponniere_autonome_sans_defenseur_4_2() -> None:
    """Témoin M3:B : M3 s'active sans Défenseur en 4.2 s'il contient >= 2 Insectes (+2/tour)."""
    state = _make_state(("M3", "B"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 3, active_ce_tour=False)
    state.set_parcel_insectes(i_seat, 2, 2)
    assert state.get_parcel_defenseurs(i_seat, 2) == 0

    state.step = STEP_4_2_NIDS
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_insectes(i_seat, 2) == 4
    assert state.get_nid_position(3) == (i_seat, 2, True)


def test_m3_c_temoin_scarabee_hercule_defense_double_insectes() -> None:
    """Témoin M3:C : 1 Défenseur + 2 Insectes (5 en Défense) parent un Seuil de 5 en défaussant 2 Insectes."""
    state = _make_state(("M3", "C"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    # Parcelle 4 dotation 3 -> Seuil avec T6? Prenons T4/T5/T1 : avec Abatteuse +2 rouges, Seuil T1 = 3 + 2 = 5 !
    state.set_parcel_nid(i_seat, 4, 3, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 4, 1)
    state.set_parcel_insectes(i_seat, 4, 2)
    state.set_machine_pos_status(i_seat, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(i_seat, MACHINE_ABATTEUSE, 2, 0)

    # Manque = 5 - 1 = 4 -> ceil(4/2) = 2 Insectes défaussés
    resolve_single_machine_attack(state, i_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(i_seat, 4) == state.cfg.dotation_arbres[3]
    assert state.get_parcel_insectes(i_seat, 4) == 0

    # Vérifions aussi l'arrondi supérieur avec manque impair : Seuil = 4 (1 rouge), 1 Déf + 2 Ins -> manque = 3 -> ceil(3/2) = 2
    state.set_parcel_insectes(i_seat, 4, 2)
    state.set_machine_tokens(i_seat, MACHINE_ABATTEUSE, 1, 0)
    resolve_single_machine_attack(state, i_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(i_seat, 4) == state.cfg.dotation_arbres[3]
    assert state.get_parcel_insectes(i_seat, 4) == 0

    # Vérifions manque = 2 : Seuil = 3 (0 rouge), 1 Déf + 2 Ins -> manque = 2 -> ceil(2/2) = 1 Insecte défaussé !
    state.set_parcel_insectes(i_seat, 4, 2)
    state.set_machine_tokens(i_seat, MACHINE_ABATTEUSE, 0, 0)
    resolve_single_machine_attack(state, i_seat, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(i_seat, 4) == state.cfg.dotation_arbres[3]
    assert state.get_parcel_insectes(i_seat, 4) == 1


def test_m3_d_temoin_guepes_aguets_auto_piege_nid_4_2() -> None:
    """Témoin M3:D : après production en 4.2, pose 1 Piège sur M3 (allume la case 2)."""
    state = _make_state(("M3", "D"))
    i_seat = state.cfg.seat_of_peuple("I")
    assert i_seat is not None

    state.set_parcel_nid(i_seat, 2, 3, active_ce_tour=False)
    state.set_parcel_defenseurs(i_seat, 2, 1)
    state.set_gardien_at_case(2, 1, 1)
    state.place_defender_gardien_pari(0, 2, 2)

    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == i_seat
    assert req.options == ("PASSER", "POSER_PIEGE")

    apply_choice(state, "POSER_PIEGE")
    req_mig = step_until_decision(state)
    assert isinstance(req_mig, DecisionRequest)
    assert req_mig.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert state.get_parcel_piege(i_seat, 2) == PIEGE_ACTIF
    assert state.get_parcel_insectes(i_seat, 2) == 1
    assert state.count_gardien_pari_consumed_at_case(2) >= 1
