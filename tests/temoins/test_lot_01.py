"""Tests unitaires témoins du Lot 01 (Lot Pilote des 8 Primitives Formelles)."""

from __future__ import annotations

import engine.effects  # noqa: F401
from engine.core_engine import (
    apply_choice,
    compute_parade_seuil,
    insert_reve_on_track,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects.lot_01 import LOT_01_PROFILES
from engine.effects.registry import list_registered_tiles
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker


def test_lot_01_all_8_profiles_registered() -> None:
    registered = set(list_registered_tiles())
    for pair in LOT_01_PROFILES:
        assert pair in registered, f"Profil manquant dans le registre : {pair}"


# ---------------------------------------------------------------------------
# 1. G1:A — Le Bond du Jaguar (MOD_PUISSANCE, DOUBLE_FACE_UPGRADE)
# Témoin : "En Face 2, permet de retourner au plus 2 jetons rouges au total,
# répartis librement entre une ou deux machines."
# ---------------------------------------------------------------------------
def test_g1_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G1", "A"),),
        exp_seed=101,
    )
    state = GameState(cfg)

    # 1) Face 1 : 1 rouge -> 1 bleu sur l'unique machine éligible, puis passage auto en Face 2
    state.set_gardien_at_case(1, 1, face=1, used=False)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    state.light_trigger(1)
    opened = sweep_gardiens(state)
    assert opened == 1
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)
    assert state.get_gardien_at_case(1) == (1, 2, True)  # Passé sur Face 2 !

    # 2) Face 2 autonome : répartir 2 retournements entre deux machines (ou s'arrêter via PASSER)
    state.cleanup_end_of_turn_6_2()
    assert state.get_gardien_at_case(1) == (1, 2, False)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=1)
    state.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=2, bleus=0)
    state.light_trigger(1)
    sweep_gardiens(state)

    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decision_type == DEC_EFFET_TUILE
    assert req1.decideur == 0  # Peuple M
    assert "PASSER" in req1.options
    apply_choice(state, (0, MACHINE_ABATTEUSE))

    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert "PASSER" in req2.options
    # Machine 0 n'a plus de rouge -> seule Machine 1 reste éligible (+ PASSER)
    assert (0, MACHINE_ABATTEUSE) not in req2.options
    assert (1, MACHINE_BULLDOZER) in req2.options
    apply_choice(state, (1, MACHINE_BULLDOZER))

    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 2)
    assert state.get_machine_tokens(1, MACHINE_BULLDOZER) == (1, 1)


# ---------------------------------------------------------------------------
# 2. G2:A — L’Étreinte de l’Anaconda (DEPLACEMENT MACHINE)
# Témoin : "Saute les Routes Forestières (et détruit par contact un éventuel Nid
# non protégé à l’arrivée). Les cibles de la machine se liront depuis sa nouvelle
# position réelle à l’instant où elle attaque."
# ---------------------------------------------------------------------------
def test_g2_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "I", "R", "O"),
        tile_profiles=(("G2", "A"),),
        exp_seed=202,
    )
    state = GameState(cfg)

    # Rayon 0 : p=1 possède un Nid M1 + 3 Insectes ; p=2 est une Route Forestière (0/0) ;
    # Abatteuse en p=3 avec 1 Défenseur.
    m1_slot = state.find_lisiere_slot_by_tile_id("M1")
    assert m1_slot is not None
    state.set_lisiere_tile_state(m1_slot, LISIERE_CONSTRUCTED, 0)
    state.set_parcel_nid(0, 1, 1, False)
    state.set_parcel_insectes(0, 1, 3)
    state.set_parcel_arbres_souches(0, 2, 0, 0)  # Route Forestière en p=2
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_parcel_defenseurs(0, 3, 1)

    state.set_gardien_at_case(2, 2, face=1, used=False)
    state.light_trigger(2)
    sweep_gardiens(state)

    # L'Abatteuse a sauté la Route p=2 pour atterrir en p=1, renvoyant M1 en lisière et vidant les Insectes !
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 1
    assert state.get_parcel_nid(0, 1) == (0, False)
    assert state.get_parcel_insectes(0, 1) == 0
    assert state.get_lisiere_tile_state(m1_slot) == (LISIERE_UNCONSTRUCTED, 0)
    assert state.get_gardien_at_case(2)[1] == 2  # Passé en Face 2

    # Quand l'Abatteuse attaque ensuite sur T1 (SUR_PLACE), elle frappe p=1 (et non plus p=3 !)
    arbres_p3_before = state.get_parcel_arbres(0, 3)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 3) == arbres_p3_before
    assert state.get_parcel_arbres(0, 1) == 0


# ---------------------------------------------------------------------------
# 3. G4:A — Le Cri d’Alarme de l’Ara (MOD_SEUIL + SACRIFICE 3.2)
# Témoin : "Le renvoi en lisière libère la case Gardien pour une future construction ;
# le Gardien repasse Face 1 et perd son marqueur « utilisé »."
# ---------------------------------------------------------------------------
def test_g4_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G4", "A"),),
        exp_seed=404,
    )
    state = GameState(cfg)
    assert cfg.reveil_quota == 4

    g4_slot = state.find_lisiere_slot_by_tile_id("G4")
    assert g4_slot is not None
    state.set_lisiere_tile_state(g4_slot, LISIERE_CONSTRUCTED, 0)
    state.set_gardien_at_case(1, 4, face=1, used=False)

    # 1) Ouverture : -1 Seuil sur une parcelle de O (siège 1) ou M (siège 0), RAZ en 6.2
    state.light_trigger(1)
    sweep_gardiens(state)
    req_open = step_until_decision(state)
    assert isinstance(req_open, DecisionRequest)
    assert req_open.decideur == 1  # Peuple O
    assert (1, 3) in req_open.options
    apply_choice(state, (1, 3))
    assert state.get_parcel_seuil_mod_turn(1, 3) == -1

    # 2) Sacrifice en 3.2 après révélation : déplace jusqu'à 2 Défenseurs vers des parcelles ciblées
    # Siège 0 possède la carte Abatteuse du rayon 2 en p=2 sur T1 (cible (2, 2))
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 1, 5, 1, 0)
    state.place_defender_foret(0, 0, 0, 1, 2)
    state.place_defender_foret(1, 0, 1, 1, 2)
    state.set_parcel_insectes(0, 1, 1)  # Suspend en 4.3 du Tour 1 pour inspecter l'état avant 6.2
    state.step = STEP_3_2_REVEAL

    req_sac1 = step_until_decision(state)
    assert isinstance(req_sac1, DecisionRequest)
    assert req_sac1.decideur == 1
    assert "PASSER" in req_sac1.options
    move1 = (("FORET", 0, 1), (2, 2))
    assert move1 in req_sac1.options
    apply_choice(state, move1)

    req_sac2 = step_until_decision(state)
    assert isinstance(req_sac2, DecisionRequest)
    move2 = (("FORET", 1, 1), (2, 2))
    assert move2 in req_sac2.options
    apply_choice(state, move2)

    # Les 2 Défenseurs sont arrivés sur (2, 2), la case 1 Gardien est vide et G4 est de retour en lisière
    assert state.get_parcel_defenseurs(2, 2) == 2
    assert state.get_gardien_at_case(1) == (0, 1, False)
    assert state.get_lisiere_tile_state(g4_slot)[0] == LISIERE_UNCONSTRUCTED


# ---------------------------------------------------------------------------
# 4. G6:A — L’Œil Double du Toucan (PERMUTATION_PISTE LECTURE_DE_M)
# Témoin : "Si ouvert avant 3.2, prépare le décalage pour la révélation du tour courant."
# ---------------------------------------------------------------------------
def test_g6_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G6", "A"),),
        exp_seed=606,
    )
    state = GameState(cfg)

    # Insérer un Rêve R5 en case 6 (index 5) puis le placer en rang 3 (index 2)
    insert_reve_on_track(state, 5)
    state.set_tactique_at_rank(2, TILE_R_BASE + 5)
    state.set_tactique_at_rank(5, 3)

    # Ouvrir G6:A AVANT 3.2 (alors que state.step == 21 et paravents fermés)
    state.set_gardien_at_case(3, 6, face=1, used=False)
    state.light_trigger(3)
    sweep_gardiens(state)
    assert state.get_gardien_at_case(3)[2] is True

    # Le joueur 0 a tiré Abatteuse rayon 0 avec lecture_m = 2 (T2). Décaler de +1 l'amène sur rang 3 (R5) !
    # En v5.4.2, un 2e Défenseur est posé sur le Rêve en case 3 pour l'activer.
    state.place_defender_reve_activation(0, 3, FACE_DEFINITIF)
    state.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 0)
    state.set_parcel_insectes(0, 1, 1)  # Suspend en 4.3 du Tour 1 (avant ménage 6.2 !)
    state.step = STEP_3_2_REVEAL

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 2  # Peuple O
    assert (0, 1) in req.options
    apply_choice(state, (0, 1))

    # Continuer 3.2 : la lecture M=3 touche R5 -> la machine de siège 0 est annulée (bound_t == 0) et R5 avance !
    _ = step_until_decision(state)
    card, _, _, lec_m, bound_t = state.get_player_hand(0)
    assert card == machine_card_code(0, MACHINE_ABATTEUSE)
    assert lec_m == 3
    assert bound_t == 0  # Annulée par R5 !
    assert state.find_tactique_rank(TILE_R_BASE + 5) == 1  # R5 avancé du rang 3 au rang 2 !


# ---------------------------------------------------------------------------
# 5. G7:A — Le Barrage du Capybara (CREATION_ENTITE PIEGE sur Souche)
# Témoin : "Fonctionne sur toute la roue dès qu’une Souche est présente."
# ---------------------------------------------------------------------------
def test_g7_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G7", "A"),),
        exp_seed=707,
    )
    state = GameState(cfg)

    # Seule la parcelle éloignée (rayon 2, p=4) porte 1 Souche ET une machine en place !
    state.set_parcel_arbres_souches(2, 4, 2, 1)
    state.set_machine_pos_status(2, MACHINE_BULLDOZER, 4, MACHINE_STATUS_NORMAL)
    state.set_gardien_at_case(1, 7, face=1, used=False)
    # Placer un second Gardien neutre en case 2 pour vérifier que G7:A allume bien la case 2 !
    state.set_gardien_at_case(2, 3, face=1, used=False)

    state.light_trigger(1)
    opened = sweep_gardiens(state)

    assert state.get_parcel_piege(2, 4) == PIEGE_ACTIF
    assert opened == 2  # G7 ouvert en case 1 -> Piège posé -> allume case 2 -> ouvre G3 en case 2 !


# ---------------------------------------------------------------------------
# 6. G10:A — La Brume de la Dendrobate (neutralisée en v5.4.2 — Apprentissage supprimé)
# ---------------------------------------------------------------------------
def test_g10_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "I"),
        tile_profiles=(("G10", "A"),),
        exp_seed=1010,
    )
    state = GameState(cfg)
    trk = TelemetryTracker()

    # G10:A s'ouvre proprement sans lever d'erreur (no-op en v5.4.2, à réajuster en Mode 4)
    state.set_gardien_at_case(6, 10, face=1, used=False)
    state.light_trigger(6)
    opened = sweep_gardiens(state, telemetry=trk)
    assert opened == 1
    assert state.get_gardien_at_case(6) == (10, 2, True)
    assert state.get_pending_voluntary_app_reduction() == (0, 0)


# ---------------------------------------------------------------------------
# 7. R5:A — La Vision des Plumes Claires (PARTAGE_INFO_ETAT_GARDIEN en 3.2)
# Témoin : "Allume aussi le Déclencheur 4 en résonance après l’effet du Gardien."
# ---------------------------------------------------------------------------
def test_r5_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("R5", "A"), ("G1", "A"), ("G10", "A")),
        exp_seed=505,
    )
    state = GameState(cfg)

    # Placer R5 en rang 2 (index 1) ; G1:A en case 2 ; G10:A en case 4 (Résonance !)
    insert_reve_on_track(state, 5)
    state.set_tactique_at_rank(1, TILE_R_BASE + 5)
    state.set_tactique_at_rank(5, 6)
    state.place_defender_reve_activation(3, 2, FACE_DEFINITIF)

    state.set_gardien_at_case(2, 1, face=1, used=False)
    state.set_gardien_at_case(4, 10, face=1, used=False)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    state.set_parcel_insectes(0, 1, 1)  # Ancre d'arrêt en 4.3 avant la fin du Tour 1

    # Le joueur 3 (H) a lecture_m = 2 -> touche R5 en 3.2 !
    state.set_player_hand(3, machine_card_code(3, MACHINE_ABATTEUSE), 2, 6, 2, 0)
    state.step = STEP_3_2_REVEAL

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 3  # Peuple H gouverne R5
    assert set(req.options) == {2, 4}
    # H choisit d'ouvrir G1:A en case 2 : G1:A retourne le rouge en bleu, allume Résonance 4,
    # puis le balayage 3.2 ouvre G10:A en case 4 !
    apply_choice(state, 2)
    _ = step_until_decision(state)

    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)
    assert state.get_gardien_at_case(2)[2] is True
    assert state.get_gardien_at_case(4)[2] is True  # Ouvert par Résonance 4 !
    assert state.find_tactique_rank(TILE_R_BASE + 5) == 0  # R5 avancé au rang 1 !


# ---------------------------------------------------------------------------
# 8. G9:C — La Peau de boue (MOD_LOI_DU_COEUR : LOI_ROUGES_IGNORES_DEVANT)
# Témoin : "Une machine T6 avec 2 rouges et 1 bleu frappant devant elle sur
# base 3 a un seuil de 3 + 0 - 1 - 2 = 1."
# ---------------------------------------------------------------------------
def test_g9_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G9", "C"),),
        exp_seed=909,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 9, face=1, used=False)

    # Machine sur rayon Reptiles (siège 1) en p=2, avec 2 rouges et 1 bleu, frappant sur T6 :
    # - SUR_PLACE (p=2, base 2) : rouges NON ignorés -> 2 + 2 - 1 - 2 = 1 ? Testons sur p=3 (base 3) :
    #   SUR_PLACE sur base 3 -> 3 + 2 - 1 - 2 = 2 !
    # - DEVANT (p=3, base 3) : rouges IGNORÉS -> 3 + 0 - 1 - 2 = 0 -> plancher 1 !
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(1, MACHINE_ABATTEUSE, rouges=2, bleus=1)

    seuil_devant_r = compute_parade_seuil(
        state, 1, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[6], cible_type="DEVANT"
    )
    seuil_sur_place_r = compute_parade_seuil(
        state, 1, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[6], cible_type="SUR_PLACE"
    )
    # Sur le rayon Mammifères (siège 0, hors R/H), DEVANT conserve ses 2 rouges : 3 + 2 - 1 - 2 = 2
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=1)
    seuil_devant_m = compute_parade_seuil(
        state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[6], cible_type="DEVANT"
    )

    assert seuil_devant_r == 1  # Témoin exact : max(1, 3 + 0 - 1 - 2) == 1
    assert seuil_sur_place_r == 2
    assert seuil_devant_m == 2
