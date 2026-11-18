"""Tests témoins déterministes du Lot 05 (G13:A..G15:B & Migrations B/C, 11 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_MIGRATION_INSECTE_4_3,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects import load_all_effects
from engine.effects.lot_05 import LOT_05_PROFILES
from engine.effects.registry import get_tile_registration
from engine.primitives import (
    DEC_EFFET_TUILE,
    DecisionRequest,
    apply_machine_nid_contact,
)
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    PIEGE_ACTIF,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_3_MIGRATION,
    STEP_6_2_EVOLUTION,
    STEP_6_3_END_TURN,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
)


def _make_state(*profiles: tuple[str, str], peuples: tuple[str, ...] = ("M", "O", "R", "I")) -> GameState:
    load_all_effects()
    cfg = GameConfig(
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
        tile_profiles=tuple(profiles),
    )
    return GameState(cfg)


def test_lot_05_all_11_profiles_registered() -> None:
    """Vérifie que les 11 profils du Lot 05 sont enregistrés (total cumulé : 51/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_05_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 51


def test_g13_a_temoin_breche_tamanoir_pose_insecte() -> None:
    """Témoin G13:A : pose 1 Insecte sur une parcelle ou case Furtivité contenant >= 1 Défenseur (allume 6).

    Peut compléter un binôme furtif avant 4.1 ou renforcer une Parade en 5.
    """
    state = _make_state(("G13", "A"))
    state.set_gardien_at_case(1, 13, 1, False)
    # 1 Défenseur en Furtivité sur (lisière 0, p=2, rive 0) et 1 Défenseur en Forêt (2, 1)
    state.enter_furtivite(0, 0, 0, 2, 0, FACE_DEFINITIF)
    state.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)

    state.light_trigger(1)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 0  # Mammifères
    assert set(req.options) == {("FORET", 2, 1), ("FURTIVITE", 0, 2)}

    # Compléter le binôme furtif sur ("FURTIVITE", 0, 2)
    apply_choice(state, ("FURTIVITE", 0, 2))
    assert state.get_furtivite_insectes(0, 2) == 1
    assert state.is_trigger_lit(6)

    # En 4.1, le binôme hybride (1 Défenseur + 1 Insecte) sur (0, 2) pose un Piège !
    state.step = STEP_4_1_FURTIVITE
    step_until_decision(state)
    assert state.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert state.get_furtivite_insectes(0, 2) == 0


def test_g13_b_temoin_construction_hybride_insecte_3_1() -> None:
    """Témoin G13:B : en 3.1, construit une tuile en lisière avec 1 Défenseur + 1 Insecte de Furtivité."""
    state = _make_state(("G13", "B"))
    state.set_gardien_at_case(1, 13, 1, False)

    # Lisière 0 (entre siège 0 et siège 1) porte le slot 0 avec 1 seul Défenseur bâtisseur
    slot_idx = 0
    state.place_defender_lisiere_tile(0, 0, slot_idx, FACE_DEFINITIF)
    assert state.get_lisiere_tile_state(slot_idx) == (LISIERE_UNCONSTRUCTED, 1)

    # 1 Insecte sur la case Furtivité (lisière 0, p=2) et 1 autre sur (lisière 0, p=3)
    state.set_furtivite_insectes(0, 2, 1)
    state.set_furtivite_insectes(0, 3, 1)

    # Laisser uniquement la case 6 libre sur la piste des Gardiens si le slot 0 est un Gardien
    for c in range(2, 6):
        state.set_gardien_at_case(c, c, 1, False)

    state.step = STEP_3_1_CONSTRUCT
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.context.get("slot_id") == "G13"
    assert req.options == (2, 3)

    # Choisir de défausser l'Insecte de Furtivité en p=2
    apply_choice(state, 2)
    assert state.get_furtivite_insectes(0, 2) == 0
    assert state.get_furtivite_insectes(0, 3) == 1

    # Terminer la construction du slot 0
    while state.step == STEP_3_1_CONSTRUCT:
        out = step_until_decision(state)
        assert isinstance(out, DecisionRequest)
        apply_choice(state, out.options[0])

    st_after, _ = state.get_lisiere_tile_state(slot_idx)
    assert st_after == LISIERE_CONSTRUCTED


def test_g14_a_temoin_ecaille_teju_conversion_piege() -> None:
    """Témoin G14:A : défausse 1 Insecte de Forêt pour poser 1 Piège sur elle ou une adjacente (allume 2)."""
    state = _make_state(("G14", "A"))
    state.set_gardien_at_case(1, 14, 1, False)
    # Parcelle (2, 2) chez Reptiles avec 1 Défenseur + 1 Insecte
    state.set_parcel_defenseurs(2, 2, 1)
    state.set_parcel_insectes(2, 2, 1)

    state.light_trigger(1)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 2  # Reptiles
    assert ("PASSER", (2, 2, 2), (2, 2, 1), (2, 2, 3)) == req.options

    # Poser le Piège sur (2, 2) : le Défenseur restant maintient le Piège armé !
    apply_choice(state, (2, 2, 2))
    assert state.get_parcel_insectes(2, 2) == 0
    assert state.get_parcel_piege(2, 2) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(2, 2) == 1
    assert state.is_trigger_lit(2)


def test_g14_b_temoin_nid_indestructible_au_contact() -> None:
    """Témoin G14:B : protège les Nids (M) et leurs Insectes contre tout mouvement de machine, mais pas contre une Route."""
    state = _make_state(("G14", "B"))
    state.set_gardien_at_case(1, 14, 1, False)

    # Placer le Nid M1 sur (2, 2) avec 3 Insectes
    state.set_parcel_nid(2, 2, 1, False)
    state.set_parcel_insectes(2, 2, 3)

    # 1. Contact machine sur (2, 2) -> le Nid M1 et ses 3 Insectes sont intégralement préservés !
    destroyed = apply_machine_nid_contact(state, 2, 2)
    assert not destroyed
    assert state.get_parcel_nid(2, 2) == (1, False)
    assert state.get_parcel_insectes(2, 2) == 3

    # 2. En revanche, la transformation de (2, 2) en Route Forestière (0/0) par un Bulldozer détruit le Nid
    state.set_parcel_insectes(2, 2, 0)  # Retirer les Insectes pour que la frappe du Bulldozer ne soit pas parée
    state.set_parcel_arbres_souches(2, 2, 1, 0)
    state.set_machine_pos_status(2, 1, 2, 1, False)  # Bulldozer en (2, 2)
    resolve_single_machine_attack(state, 2, 1, TACTIQUES_SPEC[1])
    assert state.is_route_forestiere(2, 2)
    assert state.get_parcel_nid(2, 2) == (0, False)


def test_g14_c_temoin_ventre_plein_cycle_2_temps() -> None:
    """Témoin G14:C : cycle fermé à 2 temps (À jeun -> Rassasié -> Piège + À jeun avant cascade case 2)."""
    state = _make_state(("G14", "C"))
    # G14:C en case 2 même !
    state.set_gardien_at_case(2, 14, 1, False)
    # Reptiles est au siège 2 : 1 Insecte sur (2, 1) et (2, 3)
    state.set_parcel_insectes(2, 1, 1)
    state.set_parcel_insectes(2, 3, 1)

    # Temps 1 (Face 1 À jeun) : défausse 1 Insecte chez R -> retourne sur Face 2 (Rassasié)
    state.light_trigger(2)
    sweep_gardiens(state)
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.options == (1, 3)
    apply_choice(state, 1)
    assert state.get_parcel_insectes(2, 1) == 0
    assert state.get_gardien_at_case(2) == (14, 2, True)

    # Tour suivant : marqueur utilisé retiré, G14:C est sur Face 2 (Rassasié)
    state.set_gardien_at_case(2, 14, 2, False)
    # Retirer les machines de (2, 1) pour avoir plusieurs parcelles sans machine ni Piège
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 3, 1, False)
    state.set_machine_pos_status(2, 1, 3, 1, False)

    state.light_trigger(2)
    sweep_gardiens(state)
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert req2.options == (1, 2, 4)
    apply_choice(state, 2)

    # Le Piège est posé sur (2, 2), le Gardien est retourné sur Face 1 (À jeun), et la case 2 est allumée
    assert state.get_parcel_piege(2, 2) == PIEGE_ACTIF
    assert state.get_gardien_at_case(2) == (14, 1, True)


def test_g14_d_temoin_porteurs_teju_armement_distance() -> None:
    """Témoin G14:D : déplace 1 Insecte de R ou I vers une autre parcelle piégée du même rayon à toute distance."""
    state = _make_state(("G14", "D"))
    state.set_gardien_at_case(1, 14, 1, False)
    # Rayon Reptiles (r=2) : 1 Insecte en p=1, 1 Piège désarmé en bout de rayon p=3
    state.set_parcel_insectes(2, 1, 1)
    state.set_parcel_piege(2, 3, PIEGE_ACTIF)

    state.light_trigger(1)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.options == ("PASSER", (2, 1, 3))

    apply_choice(state, (2, 1, 3))
    assert state.get_parcel_insectes(2, 1) == 0
    assert state.get_parcel_insectes(2, 3) == 1
    assert state.get_parcel_piege(2, 3) == PIEGE_ACTIF


def test_g15_a_temoin_batara_migration_directe() -> None:
    """Témoin G15:A : fait migrer immédiatement 1 Insecte de n'importe quelle case de la roue vers Bug ou Colonie."""
    state = _make_state(("G15", "A"))
    state.set_gardien_at_case(1, 15, 1, False)
    # 1 Insecte en p=1 (pas besoin d'attendre la dernière parcelle non rasée !)
    state.set_parcel_insectes(1, 1, 1)

    state.light_trigger(1)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert ("FORET", 1, 1, "BUG", 4) in req.options
    assert ("FORET", 1, 1, "COLONIE", 2) in req.options

    apply_choice(state, ("FORET", 1, 1, "COLONIE", 2))
    assert state.get_parcel_insectes(1, 1) == 0
    assert state.get_colonie_at_case(2) == 1


def test_g15_b_temoin_loi_4_3_deux_crans() -> None:
    """Témoin G15:B : en 4.3, un Insecte peut traverser une lisière puis entrer sur la forêt voisine (2 crans)."""
    state = _make_state(("G15", "B"))
    state.set_gardien_at_case(1, 15, 1, False)
    # 1 Insecte sur la parcelle Forêt (0, 2)
    state.set_parcel_insectes(0, 2, 1)

    state.step = STEP_4_3_MIGRATION
    # 1er cran : de ("FORET", 0, 2) vers ("FURTIVITE", 0, 2)
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert ("FURTIVITE", 0, 2) in req1.options
    apply_choice(state, ("FURTIVITE", 0, 2))
    assert state.get_furtivite_insectes(0, 2) == 1

    # 2e cran offert par G15:B : de ("FURTIVITE", 0, 2) vers la forêt voisine ("FORET", 1, 2) !
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert req2.decision_type == DEC_MIGRATION_INSECTE_4_3
    assert req2.context.get("cran") == 2
    assert ("FORET", 1, 2) in req2.options
    apply_choice(state, ("FORET", 1, 2))

    assert state.get_furtivite_insectes(0, 2) == 0
    assert state.get_parcel_insectes(1, 2) == 1


def test_slot_bug_cerveau_b_temoin_deviation_synaptique_3_2() -> None:
    """Témoin SLOT_BUG_CERVEAU:B : en 3.2, défausse 1 Bug sur le rang M pour dévier la lecture vers un Rêve voisin."""
    state = _make_state(("SLOT_BUG_CERVEAU", "B"))
    # Placer un Rêve R1 au rang 3 (index 2) et une Tactique T2 au rang 2 (index 1)
    state.set_tactique_at_rank(1, 2)
    state.set_tactique_at_rank(2, TILE_R_BASE + 1)
    # 1 Insecte Bug sur la case 2
    state.set_bugs_at_case(2, 1)
    # 1 Insecte sur la roue pour que step_until_decision s'arrête en 4.3 après 3.2
    state.set_parcel_insectes(0, 1, 1)

    # Le joueur 0 a tiré la carte Machine 1 avec lecture M = 2
    state.set_player_hand(0, 1, 2, 5, 2, 0)
    for s in range(1, 4):
        state.set_player_hand(s, 0, 0, 0, 0, 0)

    state.step = STEP_3_2_REVEAL
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 3  # Gouverneur Insectes
    assert req.options == ("PASSER", "M_MOINS_1", "M_PLUS_1")

    # Dévier M=2 vers M+1=3 (qui porte le Rêve R1 !)
    apply_choice(state, "M_PLUS_1")
    assert state.get_bugs_at_case(2) == 0

    # R1:A s'ouvre en 3.2 : résoudre son échange (3, 4) puis avancer la fin de 3.2 (arrêt en 4.3)
    req_r1 = step_until_decision(state)
    assert isinstance(req_r1, DecisionRequest)
    assert req_r1.decision_type == DEC_EFFET_TUILE
    apply_choice(state, (3, 4))

    step_until_decision(state)
    card, _, _, lec_m, bound_t = state.get_player_hand(0)
    assert card == 1
    assert lec_m == 3
    assert bound_t == 0
    assert state.get_tactique_at_rank(1) == TILE_R_BASE + 1


def test_slot_bug_cerveau_c_temoin_cigale_bloque_6_2() -> None:
    """Témoin SLOT_BUG_CERVEAU:C : bloque l'avancée en 6.2 sur un rang avec >= 1 Bug, l'Insecte reste et 100 % des jetons Apprentissage sont remis à zéro."""
    state = _make_state(("SLOT_BUG_CERVEAU", "C"))
    t_rank2_before = state.get_tactique_at_rank(1)
    t_rank3_before = state.get_tactique_at_rank(2)

    # Le rang 3 (index 2, case 3) est strictement seul en tête avec 3 jetons Apprentissage, mais porte 1 Bug
    state.set_apprentissage_at_rank(2, 3)
    state.set_apprentissage_at_rank(4, 1)
    state.set_bugs_at_case(3, 1)

    state.step = STEP_6_2_EVOLUTION
    # _advance_main_step exécute _run_step_6_2 et passe à STEP_6_3_END_TURN
    from engine.core_engine import _run_step_6_2

    over = _run_step_6_2(state)
    assert over is None
    assert state.step == STEP_6_3_END_TURN

    # L'avancée a été bloquée par la Cigale
    assert state.get_tactique_at_rank(1) == t_rank2_before
    assert state.get_tactique_at_rank(2) == t_rank3_before
    # L'Insecte Bug est resté sur la case 3
    assert state.get_bugs_at_case(3) == 1
    # 100 % des jetons d'Apprentissage de toutes les tuiles sont remis à zéro
    for idx in range(6):
        assert state.get_apprentissage_at_rank(idx) == 0


def test_slot_colonisation_gardiens_c_temoin_lucioles_auto_4_3() -> None:
    """Témoin SLOT_COLONISATION_GARDIENS:C : en fin de 4.3, ouvre automatiquement le Gardien disponible et l'Insecte reste sur sa case."""
    state = _make_state(("SLOT_COLONISATION_GARDIENS", "C"), ("G13", "A"))
    # G13:A en case 3, disponible, et 1 Insecte Colonie en case 3
    state.set_gardien_at_case(3, 13, 1, False)
    state.set_colonie_at_case(3, 1)
    # 2 cibles valides pour G13:A : Forêt (0, 1) et Forêt (1, 1) -> suspend en 4.3 dès que G13:A s'ouvre automatiquement !
    state.set_parcel_defenseurs(0, 1, 1)
    state.set_parcel_defenseurs(1, 1, 1)

    state.step = STEP_4_3_MIGRATION
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.context.get("slot_id") == "G13"

    # Le Gardien G13:A en case 3 a été ouvert automatiquement sans décision de Colonisation,
    # et l'Insecte Colonie est toujours présent sur la case 3 !
    assert state.get_gardien_at_case(3) == (13, 1, True)
    assert state.get_colonie_at_case(3) == 1
    apply_choice(state, ("FORET", 0, 1))
    assert state.get_parcel_insectes(0, 1) == 1
