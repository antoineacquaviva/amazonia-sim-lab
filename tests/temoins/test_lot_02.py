"""Tests unitaires témoins du Lot 02 (10 profils Gardiens G1..G5 hors pilote)."""

from __future__ import annotations

import engine.effects  # noqa: F401
from engine.core_engine import (
    DEC_POSE_DEFENSEUR_1,
    apply_choice,
    compute_parade_seuil,
    list_legal_targets,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects.lot_02 import LOT_02_PROFILES
from engine.effects.registry import list_registered_tiles
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PFLAG_MATAMATA_MARK,
    PIEGE_ACTIF,
    PIEGE_DECLENCHE,
    STEP_1_3_DICE,
    STEP_4_1_FURTIVITE,
    TACTIQUES_SPEC,
    GameConfig,
    GameState,
    machine_card_code,
)


def test_lot_02_all_10_profiles_registered() -> None:
    registered = set(list_registered_tiles())
    for pair in LOT_02_PROFILES:
        assert pair in registered, f"Profil manquant dans le registre : {pair}"


# ---------------------------------------------------------------------------
# 1. G1:B — Le Bond du Jaguar (MOD_SEUIL + PARADE_JAGUAR Surchauffe)
# Témoin : "1er maillon de la chaîne des parades (avant Harpie et Piège) :
# consomme automatiquement 2 bleus, allume 1. Parade et laisse un éventuel
# Piège intact (non déclenché)."
# ---------------------------------------------------------------------------
def test_g1_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G1", "B"), ("G10", "A")),
        exp_seed=1201,
    )
    state = GameState(cfg)

    # 1) Face 1 : -2 Seuil sur la seule machine portant >= 1 jeton Puissance, puis passage Face 2
    state.set_gardien_at_case(2, 1, face=1, used=False)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    seuil_before = compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1])
    assert seuil_before == 4  # base 3 + 1 rouge

    state.light_trigger(2)
    sweep_gardiens(state)
    assert state.get_machine_seuil_mod_turn(0, MACHINE_ABATTEUSE) == -2
    assert compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 2
    assert state.get_gardien_at_case(2) == (1, 2, True)  # Passé en Face 2 !

    # RAZ 6.2 du modificateur transitoire de Face 1
    state.cleanup_end_of_turn_6_2()
    assert state.get_machine_seuil_mod_turn(0, MACHINE_ABATTEUSE) == 0
    assert state.get_gardien_at_case(2) == (1, 2, False)

    # 2) Face 2 (témoin exact) : Bulldozer en p=2 avec 2 bleus attaque sur T6 (SUR_PLACE + DEVANT, avancée 1),
    # alors que p=2 porte un Piège actif + 1 Défenseur et que G10:A attend sur la case 1 (1. Parade).
    state.set_gardien_at_case(1, 10, face=1, used=False)
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=0, bleus=2)
    state.set_parcel_piege(1, 2, PIEGE_ACTIF)
    state.set_parcel_defenseurs(1, 2, 1)

    resolve_single_machine_attack(state, 1, MACHINE_BULLDOZER, TACTIQUES_SPEC[6])

    # Jaguar a agi en 1er maillon : 2 bleus consommés, recul p=2 -> p=1 (au lieu d'avancer),
    # Piège resté PIEGE_ACTIF (non déclenché), arbres intacts sur p=2 et p=3, et case 1 allumée (G10 ouvert) !
    assert state.get_machine_tokens(1, MACHINE_BULLDOZER) == (1, 0)  # 0 bleu restant (+1 rouge T6)
    assert state.get_machine_pos_status(1, MACHINE_BULLDOZER)[0] == 1
    assert state.get_parcel_piege(1, 2) == PIEGE_ACTIF
    assert state.get_parcel_arbres(1, 2) == 2
    assert state.get_parcel_arbres(1, 3) == 3
    assert state.get_gardien_at_case(1)[2] is True  # Case 1 (Parade) a bien été allumée !

    # En Ratissage : pare automatiquement en défaussant 2 bleus mais ne recule pas
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    state.set_machine_tokens(2, MACHINE_ABATTEUSE, rouges=0, bleus=2)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_machine_pos_status(2, MACHINE_ABATTEUSE)[:2] == (4, MACHINE_STATUS_RATISSAGE)
    assert state.get_parcel_arbres(2, 4) == 3


# ---------------------------------------------------------------------------
# 2. G2:B — L’Étreinte de l’Anaconda (LOI_MACHINE_PAREE_SANS_ELAN)
# Témoin : "Une frappe annulée sur une parcelle déjà rasée en Route Forestière
# ne compte pas comme parée pour cette loi."
# ---------------------------------------------------------------------------
def test_g2_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G2", "B"),),
        exp_seed=1202,
    )
    state = GameState(cfg)

    # 1) Face 1 en case 1 (1. Parade) : Abatteuse en p=1 sur T6 dont les 2 frappes (p=1, p=2) sont parées.
    # Sur Face 1 : elle N'AVANCE PAS, gagne encore son rouge T6, puis G2:B s'ouvre en case 1 et passe Face 2 !
    state.set_gardien_at_case(1, 2, face=1, used=False)
    state.set_parcel_defenseurs(0, 1, 2)
    state.set_parcel_defenseurs(0, 2, 2)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[6])

    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 1  # Bloquée en p=1 !
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)  # Gain rouge conservé en Face 1
    assert state.get_gardien_at_case(1) == (2, 2, True)  # Passé en Face 2 après ouverture !

    # 2) Face 2 : Bulldozer en p=1 sur T6 entièrement paré -> ni avancée, ni gain de jeton rouge !
    state.set_parcel_defenseurs(1, 1, 2)
    state.set_parcel_defenseurs(1, 2, 2)
    resolve_single_machine_attack(state, 1, MACHINE_BULLDOZER, TACTIQUES_SPEC[6])
    assert state.get_machine_pos_status(1, MACHINE_BULLDOZER)[0] == 1
    assert state.get_machine_tokens(1, MACHINE_BULLDOZER) == (0, 0)

    # Idem en Ratissage T1 entièrement paré sur Face 2 : pas de jeton rouge !
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    state.set_parcel_defenseurs(2, 4, 3)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_machine_tokens(2, MACHINE_ABATTEUSE) == (0, 0)

    # 3) Témoin exact : sur le rayon 3, p=4 est déjà rasée en Route Forestière (0/0) et la machine est en p=3.
    # - Sur T5 (DEVANT annulée sur Route p=4) : ne compte PAS comme parée -> gagne +1 rouge !
    # - Sur T6 (SUR_PLACE p=3 parée, mais DEVANT p=4 annulée sur Route) : ne compte PAS comme toute parée -> +1 rouge !
    state.set_parcel_arbres_souches(3, 4, 0, 0)
    state.set_machine_pos_status(3, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(state, 3, MACHINE_ABATTEUSE, TACTIQUES_SPEC[5])
    assert state.get_machine_tokens(3, MACHINE_ABATTEUSE) == (1, 0)

    state.set_machine_pos_status(3, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    state.set_parcel_defenseurs(3, 3, 3)
    resolve_single_machine_attack(state, 3, MACHINE_BULLDOZER, TACTIQUES_SPEC[6])
    assert state.get_machine_tokens(3, MACHINE_BULLDOZER) == (1, 0)


# ---------------------------------------------------------------------------
# 3. G2:C — La fuite sous les feuilles (DEPLACEMENT INSECTE TOUS)
# Témoin : "3 Insectes en p=1, Route en p=2, Nid en p=3 : les 3 arrivent
# ensemble en p=3 sans allumer la case 6 (tous les Insectes présents sur la
# roue sont libres)."
# ---------------------------------------------------------------------------
def test_g2_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "I"),
        tile_profiles=(("G2", "C"), ("G10", "A")),
        exp_seed=1203,
    )
    state = GameState(cfg)

    # Rayon 1 (R) : 3 Insectes en p=1, Route Forestière en p=2, Nid M1 en p=3.
    # G10:A posé en case 6 (Naissance) pour vérifier que la case 6 NE S'ALLUME PAS !
    state.set_parcel_insectes(1, 1, 3)
    state.set_parcel_arbres_souches(1, 2, 0, 0)
    state.set_parcel_nid(1, 3, 1, False)
    state.set_gardien_at_case(1, 2, face=1, used=False)
    state.set_gardien_at_case(6, 10, face=1, used=False)

    state.light_trigger(1)
    sweep_gardiens(state)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 1  # Peuple R
    assert "PASSER" in req.options
    assert (1, 1, 3) in req.options

    apply_choice(state, (1, 1, 3))
    assert state.get_parcel_insectes(1, 1) == 0
    assert state.get_parcel_insectes(1, 3) == 3
    assert state.is_trigger_lit(6) is False
    assert state.get_gardien_at_case(6)[2] is False  # Case 6 non allumée !


# ---------------------------------------------------------------------------
# 4. G3:A — La Voltige de l’Atèle (DEPLACEMENT DEFENSEUR adjacent + lisière)
# Témoin : "Un constructeur en bordure peut rejoindre p=1 d’un rayon bordant
# sa lisière."
# ---------------------------------------------------------------------------
def test_g3_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G3", "A"),),
        exp_seed=1204,
    )
    state = GameState(cfg)

    # 1 constructeur posé en bordure de lisière 0 (entre rayon 0 M et rayon 1 O, slot_idx = 0)
    state.place_defender_lisiere_tile(1, 0, 0, FACE_DEFINITIF)
    assert state.get_lisiere_tile_state(0) == (LISIERE_UNCONSTRUCTED, 1)

    state.set_gardien_at_case(2, 3, face=1, used=False)
    state.light_trigger(2)
    sweep_gardiens(state)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 0  # Peuple M
    move_to_r1 = (("LISIERE", 0), (1, 1))
    assert (("LISIERE", 0), (0, 1)) in req.options
    assert move_to_r1 in req.options

    apply_choice(state, move_to_r1)
    assert state.get_lisiere_tile_state(0) == (LISIERE_UNCONSTRUCTED, 0)
    assert state.get_parcel_defenseurs(1, 1) == 1


# ---------------------------------------------------------------------------
# 5. G3:B — La Voltige de l’Atèle (LOI 4.1 -> 5 : glissement gratuit en Forêt)
# Témoin : "Idéal pour agir en Furtivité en 4.1 puis armer un Piège Embuscade
# en Forêt à l’Étape 5."
# ---------------------------------------------------------------------------
def test_g3_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G3", "B"),),
        exp_seed=1205,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(5, 3, face=1, used=False)

    # Binôme 1 sur lisière 0 (entre M=0 et O=1) en p=2 orienté rive 0 (face à M p=2)
    state.enter_furtivite(0, 0, 0, 2, 0, FACE_DEFINITIF)
    state.enter_furtivite(1, 0, 0, 2, 0, FACE_DEFINITIF)
    # Binôme 2 sur lisière 1 (entre O=1 et R=2) en p=2 orienté rive 0 (face à O p=2) pour vérifier la limite 1/tour
    state.enter_furtivite(1, 1, 1, 2, 0, FACE_DEFINITIF)
    state.enter_furtivite(2, 0, 1, 2, 0, FACE_DEFINITIF)

    state.set_parcel_insectes(0, 1, 1)  # Suspend en 4.3 avant ménage
    state.step = STEP_4_1_FURTIVITE
    _ = step_until_decision(state)

    # Le Binôme 1 a posé un Piège en (0, 2) ET fait glisser 1 Défenseur sur (0, 2) !
    assert state.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(0, 2) == 1
    assert state.get_furtivite_total_defs(0, 2) == 1
    assert state.has_slot_used_once_per_turn("G3") is True

    # Le Binôme 2 a bien posé son Piège en (1, 2), mais sans second glissement (quota 1/tour déjà consommé)
    assert state.get_parcel_piege(1, 2) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(1, 2) == 0
    assert state.get_furtivite_total_defs(1, 2) == 2

    # À l'Étape 5, une Abatteuse avec 3 rouges frappant (0, 2) est parée net par l'Embuscade armée !
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=3, bleus=0)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_piege(0, 2) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(0, 2) == 2


# ---------------------------------------------------------------------------
# 6. G3:C — Le passage des singes-lianes (DEPLACEMENT TRAVERSEE M<->O)
# Témoin : "Une Parade chez M ouvre G3 C : un Défenseur ayant paré traverse
# chez O à même profondeur. La première Parade reste acquise."
# ---------------------------------------------------------------------------
def test_g3_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G3", "C"),),
        exp_seed=1206,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 3, face=1, used=False)

    # M (siège 0) possède 2 Défenseurs en p=2 ; O (siège 1) n'en a qu'1 en p=2 (insuffisant seul contre seuil 2).
    state.place_defender_foret(0, 0, 0, 2, FACE_DEFINITIF)
    state.place_defender_foret(0, 1, 0, 2, FACE_DEFINITIF)
    state.place_defender_foret(1, 0, 1, 2, FACE_DEFINITIF)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)

    # 1re attaque chez M en p=2 : parée -> allume case 1 -> ouvre G3:C !
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 2) == 2  # 1re Parade acquise !

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 0  # Peuple M
    assert "PASSER" in req.options
    cross_move = (("FORET", 0, 2), (1, 2))
    assert cross_move in req.options

    apply_choice(state, cross_move)
    assert state.get_parcel_defenseurs(0, 2) == 1
    assert state.get_parcel_defenseurs(1, 2) == 2
    assert state.get_parcel_arbres(0, 2) == 2  # Toujours intacte

    # 2e attaque chez O en p=2 : désormais parée grâce au Défenseur ayant traversé !
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(1, 2) == 2


# ---------------------------------------------------------------------------
# 7. G3:D — Les sentinelles des lianes (FURTIVITE -> PARCELLE_PIEGEE M/O)
# Témoin : "Un binôme a agi en Furtivité face à M p=2 piégée : à l’ouverture,
# 1 Défenseur rejoint M p=2 pour armer l’Embuscade."
# ---------------------------------------------------------------------------
def test_g3_d_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G3", "D"),),
        exp_seed=1207,
    )
    state = GameState(cfg)
    # G3:D en case 2 (2. Piège) : dès que le binôme pose le Piège en M p=2, G3:D s'ouvre !
    state.set_gardien_at_case(2, 3, face=1, used=False)
    state.enter_furtivite(0, 0, 0, 2, 0, FACE_DEFINITIF)
    state.enter_furtivite(1, 0, 0, 2, 0, FACE_DEFINITIF)
    state.set_parcel_insectes(0, 1, 1)  # Suspend en 4.3
    state.step = STEP_4_1_FURTIVITE

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 0  # Peuple M
    assert "PASSER" in req.options
    move_to_trap = (("FURTIVITE", 0, 2), (0, 2))
    assert move_to_trap in req.options

    apply_choice(state, move_to_trap)
    _ = step_until_decision(state)

    assert state.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(0, 2) == 1
    assert state.get_furtivite_total_defs(0, 2) == 1

    # Embuscade armée en (0, 2) !
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=2, bleus=0)
    resolve_single_machine_attack(state, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_piege(0, 2) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(0, 2) == 2


# ---------------------------------------------------------------------------
# 8. G4:B — Le Cri d’Alarme de l’Ara (LOI 2.1 portée globale + SACRIFICE 2.1)
# Témoin : "Offre une visibilité publique complète des cartes et dés, mais la
# pose reste individuelle et sans concertation orale."
# ---------------------------------------------------------------------------
def test_g4_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G4", "B"),),
        exp_seed=1208,
    )
    state = GameState(cfg)
    g4_slot = state.find_lisiere_slot_by_tile_id("G4")
    assert g4_slot is not None
    state.set_lisiere_tile_state(g4_slot, LISIERE_CONSTRUCTED, 0)
    state.set_gardien_at_case(4, 4, face=1, used=True)

    # 1) Loi 2.1 (sans sacrifice) : O (siège 1) et M (siège 0) ont portée globale pour leur 1er Défenseur,
    # tandis que R (siège 2) reste restreint à son secteur local !
    for s in range(4):
        state.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 0, 0, 0, 0)
    state.step = STEP_1_3_DICE

    req_debut = step_until_decision(state)
    assert isinstance(req_debut, DecisionRequest)
    assert req_debut.decideur == 1  # Peuple O
    assert req_debut.options == ("PASSER", "SACRIFIER_G4_PARAVENTS")

    # Cas A : sur un clone où O passe le sacrifice, M et O voient tout le plateau en 2.1
    state_keep = state.clone()
    apply_choice(state_keep, "PASSER")
    req_m_def1 = step_until_decision(state_keep)
    assert isinstance(req_m_def1, DecisionRequest)
    assert req_m_def1.decision_type == DEC_POSE_DEFENSEUR_1
    assert state_keep.paravents_ouverts is False
    assert ("FORET", 2, 4) in list_legal_targets(state_keep, 0, is_first_defender=True)  # M -> rayon R !
    assert ("FORET", 3, 4) in list_legal_targets(state_keep, 1, is_first_defender=True)  # O -> rayon H !
    assert ("FORET", 0, 4) not in list_legal_targets(state_keep, 2, is_first_defender=True)  # R local uniquement

    # Cas B (témoin exact) : O sacrifie G4:B au début de l'Étape 2 -> paravents ouverts avant toute pose 2.1 !
    apply_choice(state, "SACRIFIER_G4_PARAVENTS")
    req_def1 = step_until_decision(state)
    assert isinstance(req_def1, DecisionRequest)
    assert req_def1.decision_type == DEC_POSE_DEFENSEUR_1
    assert state.paravents_ouverts is True
    assert state.get_gardien_at_case(4) == (0, 1, False)  # Perte du marqueur utilisé & case libérée
    assert state.get_lisiere_tile_state(g4_slot)[0] == LISIERE_UNCONSTRUCTED

    # Visibilité publique complète des cartes et dés dans PlayerObservation avant la pose !
    obs_m = state.get_observation(0)
    assert obs_m.paravents_ouverts is True
    for s in range(4):
        h_s = obs_m.hand_of(s)
        assert h_s.card == machine_card_code(s, MACHINE_ABATTEUSE)
        assert h_s.d1 is not None and h_s.d2 is not None and h_s.lecture_m is not None


# ---------------------------------------------------------------------------
# 9. G5:A — L’Affût de la Matamata (LOI TEMP 5 sur parcelles désignées)
# Témoin : "Vérification dynamique à chaque frappe : si une Abatteuse crée une
# Souche sur la parcelle désignée, le Bulldozer suivant subit immédiatement
# le −1 au Seuil."
# ---------------------------------------------------------------------------
def test_g5_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G5", "A"),),
        exp_seed=1209,
    )
    state = GameState(cfg)

    # 1) Face 1 : R (siège 1) désigne la parcelle intacte (0, 3) (3 Arbres, 0 Souche, 2 Défenseurs).
    state.set_gardien_at_case(3, 5, face=1, used=False)
    state.set_parcel_defenseurs(0, 3, 2)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)

    state.light_trigger(3)
    sweep_gardiens(state)
    req_f1 = step_until_decision(state)
    assert isinstance(req_f1, DecisionRequest)
    assert req_f1.decideur == 1  # Peuple R
    assert (0, 3) in req_f1.options
    apply_choice(state, (0, 3))

    assert state.has_parcel_flag_turn(0, 3, PFLAG_MATAMATA_MARK) is True
    assert state.get_gardien_at_case(3) == (5, 2, True)  # Passé en Face 2 !

    # Avant Souche : 0 Souche sur (0, 3) -> Seuil T1 reste 3 -> l'Abatteuse n'est PAS parée par 2 Défenseurs
    # et coupe 2 Arbres (créant 2 Souches sur place !).
    assert compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 3
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 3) == 1
    assert state.get_parcel_souches(0, 3) == 2

    # Immédiatement après : le Bulldozer frappe (0, 3) qui porte désormais 2 Souches -> Seuil tombe à 3 - 1 = 2
    # -> les 2 Défenseurs parent le Bulldozer et sauvent la parcelle du terrassement !
    assert compute_parade_seuil(state, 0, MACHINE_BULLDOZER, 3, TACTIQUES_SPEC[1]) == 2
    resolve_single_machine_attack(state, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 3) == 1
    assert state.get_parcel_souches(0, 3) == 2

    # RAZ 6.2 + vérification Face 2 autonome (jusqu'à 2 parcelles avec PASSER)
    state.cleanup_end_of_turn_6_2()
    assert state.has_parcel_flag_turn(0, 3, PFLAG_MATAMATA_MARK) is False

    state.light_trigger(3)
    sweep_gardiens(state)
    req_f2_1 = step_until_decision(state)
    assert isinstance(req_f2_1, DecisionRequest)
    assert "PASSER" in req_f2_1.options
    apply_choice(state, (0, 3))

    req_f2_2 = step_until_decision(state)
    assert isinstance(req_f2_2, DecisionRequest)
    assert "PASSER" in req_f2_2.options
    assert (0, 3) not in req_f2_2.options
    apply_choice(state, (1, 2))
    assert state.has_parcel_flag_turn(0, 3, PFLAG_MATAMATA_MARK) is True
    assert state.has_parcel_flag_turn(1, 2, PFLAG_MATAMATA_MARK) is True


# ---------------------------------------------------------------------------
# 10. G5:B — L’Affût de la Matamata (LOI 5 R/O en Face 1, globale en Face 2)
# Témoin : "Vérifié dynamiquement à chaque frappe sur le Seuil Imprimé : dès
# qu’au moins 1 Souche est présente sur la parcelle à cet instant, le Seuil
# diminue de −1."
# ---------------------------------------------------------------------------
def test_g5_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G5", "B"),),
        exp_seed=1210,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(3, 5, face=1, used=False)

    # 1) Face 1 : sur rayon R (1) et O (2), dynamique selon Souche ; inactif sur M (0) et H (3) !
    assert compute_parade_seuil(state, 1, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 3  # 0 Souche
    state.set_parcel_arbres_souches(1, 3, 2, 1)
    state.set_parcel_arbres_souches(2, 3, 2, 1)
    state.set_parcel_arbres_souches(0, 3, 2, 1)
    assert compute_parade_seuil(state, 1, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 2  # R : -1
    assert compute_parade_seuil(state, 2, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 2  # O : -1
    assert compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 3  # M : inchangé

    # 2) Ouverture de G5:B -> passe en Face 2 -> s'applique désormais à tout le plateau (dont M et H) !
    state.light_trigger(3)
    sweep_gardiens(state)
    assert state.get_gardien_at_case(3) == (5, 2, True)
    assert compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 2  # M désormais à -1 !
