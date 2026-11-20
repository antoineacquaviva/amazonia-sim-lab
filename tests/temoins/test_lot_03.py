"""Tests unitaires témoins du Lot 03 (10 profils Gardiens G5:C..G9:B)."""

from __future__ import annotations

import engine.effects  # noqa: F401
from engine.core_engine import (
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects.lot_03 import LOT_03_PROFILES
from engine.effects.registry import list_registered_tiles
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    STEP_1_3_DICE,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_5_1_TACTIQUES,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)


def test_lot_03_all_10_profiles_registered() -> None:
    registered = set(list_registered_tiles())
    for pair in LOT_03_PROFILES:
        assert pair in registered, f"Profil manquant dans le registre : {pair}"


# ---------------------------------------------------------------------------
# 1. G5:C — Le Perchoir du caïman (LOI 5 : soutien machine -> devant sur R et O)
# Témoin : "Ce point de soutien à distance suffit à armer un Piège Embuscade sur
# la parcelle devant la machine, même si celle-ci est vide de pion."
# ---------------------------------------------------------------------------
def test_g5_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("R", "O", "M", "H"),
        tile_profiles=(("G5", "C"), ("G10", "A")),
        exp_seed=1301,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(4, 5, face=1)
    state.place_defender_gardien_pari(0, 4, 2)
    state.set_gardien_at_case(1, 10, face=1)
    state.place_defender_gardien_pari(1, 1, 2)

    # Rayon R (0) : Abatteuse en p=1 avec 1 Défenseur sur p=1 ; p=2 devant porte un Piège mais 0 pion !
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.place_defender_foret(0, 0, 0, 1, FACE_DEFINITIF)
    state.set_parcel_piege(0, 2, PIEGE_ACTIF)
    assert state.get_parcel_defenseurs(0, 2) == 0
    assert state.get_parcel_insectes(0, 2) == 0
    arbres_p2_before = state.get_parcel_arbres(0, 2)

    # T2 frappe uniquement DEVANT (p=2) : le Défenseur en p=1 apporte +1 soutien à distance -> arme le Piège !
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[2])
    assert state.get_parcel_piege(0, 2) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(0, 2) == arbres_p2_before
    assert state.count_gardien_pari_consumed_at_case(1) >= 1  # Case 1 (Parade) s'est bien allumée !

    # Hors périmètre (rayon M = 2) : le soutien ne s'applique pas -> Piège inerte non armé, arbres coupés
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    state.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)
    state.set_parcel_piege(2, 2, PIEGE_ACTIF)
    arbres_m2_before = state.get_parcel_arbres(2, 2)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[2])
    assert state.get_parcel_piege(2, 2) == PIEGE_ACTIF
    assert state.get_parcel_arbres(2, 2) < arbres_m2_before


# ---------------------------------------------------------------------------
# 2. G6:B — L’Œil Double du Toucan (LOI 1.3 : O et R peuvent retenir max(D1, D2))
# Témoin : "Permet d’aller chercher volontairement les Rêves insérés aux rangs 5 et 6."
# ---------------------------------------------------------------------------
def test_g6_b_temoin() -> None:
    # Choisissons une graine déterministe où O et R tirent D1 != D2 avec max(D1, D2) en rang 5 ou 6
    chosen_seed = 1302
    for cand_seed in range(1300, 1450):
        probe_cfg = GameConfig(
            n_players=4,
            mode=3,
            peuples=("O", "R", "M", "H"),
            tile_profiles=(("G6", "B"),),
            exp_seed=cand_seed,
        )
        probe = GameState(probe_cfg)
        probe.set_gardien_at_case(1, 6, face=1)
        probe.place_defender_gardien_pari(0, 1, 2)
        probe.set_player_hand(0, 1, 0, 0, 0, 0)
        probe.set_player_hand(1, 2, 0, 0, 0, 0)
        probe.step = STEP_1_3_DICE
        req_p = step_until_decision(probe)
        if isinstance(req_p, DecisionRequest) and int(req_p.context.get("max_m", 0)) in (5, 6):
            _, d1_r, d2_r, _, _ = probe.get_player_hand(1)
            if d1_r != d2_r:
                chosen_seed = cand_seed
                break

    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("O", "R", "M", "H"),
        tile_profiles=(("G6", "B"),),
        exp_seed=chosen_seed,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 6, face=1)
    state.place_defender_gardien_pari(1, 1, 2)

    # Insérer un Rêve R1 aux rangs 5 et 6 (indices 4 et 5)
    state.set_tactique_at_rank(4, TILE_R_BASE + 1)
    state.set_tactique_at_rank(5, TILE_R_BASE + 2)

    state.set_player_hand(0, 1, 0, 0, 0, 0)  # O
    state.set_player_hand(1, 2, 0, 0, 0, 0)  # R
    state.set_player_hand(2, 3, 0, 0, 0, 0)  # M (non éligible)
    state.set_player_hand(3, 4, 0, 0, 0, 0)  # H (non éligible)
    state.step = STEP_1_3_DICE

    # 1) Siège O (0) décide pour lui-même derrière son paravent -> choisit RETENIR_MAX (rang 5 ou 6 = Rêve !)
    req_o = step_until_decision(state)
    assert isinstance(req_o, DecisionRequest)
    assert req_o.decision_type == DEC_EFFET_TUILE
    assert req_o.decideur == 0
    assert req_o.options == ("PASSER", "RETENIR_MAX")
    max_o = int(req_o.context["max_m"])
    assert max_o in (5, 6)
    apply_choice(state, "RETENIR_MAX")
    assert state.get_player_hand(0)[3] == max_o

    # 2) Siège R (1) décide pour lui-même -> choisit PASSER (conserve min(D1, D2))
    req_r = step_until_decision(state)
    assert isinstance(req_r, DecisionRequest)
    assert req_r.decideur == 1
    min_r = int(req_r.context["min_m"])
    apply_choice(state, "PASSER")
    assert state.get_player_hand(1)[3] == min_r

    # 3) M et H ne reçoivent aucune demande en 1.3 -> on arrive directement à 2.1 !
    req_next = step_until_decision(state)
    assert isinstance(req_next, DecisionRequest)
    assert req_next.decision_type != DEC_EFFET_TUILE


# ---------------------------------------------------------------------------
# 3. G6:C — Le Vol en ciseaux (ECHANGE_ATOMIQUE Défenseur O/R <-> Insecte Furtivité)
# Témoin : "Avant 4.1, permet de former et d’orienter un binôme de 2 Défenseurs
# en Furtivité tout en envoyant l’Insecte défendre la forêt."
# ---------------------------------------------------------------------------
def test_g6_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("O", "R", "M", "H"),
        tile_profiles=(("G6", "C"),),
        exp_seed=1303,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(2, 6, face=1)
    state.place_defender_gardien_pari(0, 2, 2)

    # Lisière commune O(0)-R(1) = lisière 0, profondeur p=2 :
    # - 1 Défenseur déjà en Furtivité sur rive 0 (face à O), + 1 Insecte en Furtivité
    # - 1 Défenseur en Forêt sur O (rayon 0, p=2), 0 Insecte en Forêt sur (0, 2)
    state.enter_furtivite(1, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    state.set_furtivite_insectes(0, 2, 1)
    state.place_defender_foret(0, 0, 0, 2, FACE_DEFINITIF)
    assert state.get_furtivite_nb_def_rive(0, 2, 0) == 1
    assert state.get_furtivite_nb_def_rive(0, 2, 1) == 0

    # 1) Vérification de l'option PASSER
    state.light_trigger(2)
    sweep_gardiens(state)
    req_pass = step_until_decision(state)
    assert isinstance(req_pass, DecisionRequest)
    assert "PASSER" in req_pass.options
    assert (0, 2, 1) in req_pass.options  # Échanger depuis O(0,2) et orienter sur rive 1 (vers R) !
    apply_choice(state, "PASSER")
    assert state.get_parcel_defenseurs(0, 2) == 1
    assert state.get_furtivite_insectes(0, 2) == 1

    # 2) Activation effective : oriente le binôme de 2 Défenseurs vers R (rive 1) et envoie l'Insecte en Forêt O(0,2)
    state.cleanup_end_of_turn_6_2()
    state.place_defender_gardien_pari(2, 2, FACE_DEFINITIF)
    state.enter_furtivite(1, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    state.set_furtivite_insectes(0, 2, 1)
    state.place_defender_foret(0, 0, 0, 2, FACE_DEFINITIF)

    state.light_trigger(2)
    sweep_gardiens(state)
    req_do = step_until_decision(state)
    assert isinstance(req_do, DecisionRequest)
    apply_choice(state, (0, 2, 1))

    # Résultat atomique : 2 Défenseurs réunis sur rive 1 (vers R), 0 sur rive 0, 0 Insecte Furtivité,
    # et 1 Insecte arrivé sur la parcelle Forêt O(0, 2) !
    assert state.get_furtivite_nb_def_rive(0, 2, 0) == 0
    assert state.get_furtivite_nb_def_rive(0, 2, 1) == 2
    assert state.get_furtivite_insectes(0, 2) == 0
    assert state.get_parcel_defenseurs(0, 2) == 0
    assert state.get_parcel_insectes(0, 2) == 1


# ---------------------------------------------------------------------------
# 4. G7:B — Le Barrage du Capybara (LOI 4.1 : Piège sous machine)
# Témoin : "Fait sauter le verrou majeur du minage en Furtivité."
# (+ synergie explicite du texte : armement immédiat si G3:B fait glisser 1 Défenseur dessus)
# ---------------------------------------------------------------------------
def test_g7_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "O", "R", "H"),
        tile_profiles=(("G7", "B"), ("G3", "B")),
        exp_seed=1304,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(2, 7, face=1)
    state.place_defender_gardien_pari(0, 2, 2)
    state.set_gardien_at_case(4, 3, face=1)
    state.place_defender_gardien_pari(1, 4, 2)

    # Rayon M (0), p=2 occupée par une Abatteuse en Siège (normalement impossible à piéger NI à saboter en 4.1 !)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_RATISSAGE)
    state.enter_furtivite(0, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    state.enter_furtivite(1, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    # Un Insecte témoin en (2, 1) suspendra la boucle en 4.3 juste après 4.1 (avant les Sièges 5.2 !)
    state.set_parcel_insectes(2, 1, 1)
    assert state.get_parcel_piege(0, 2) == PIEGE_AUCUN

    state.step = STEP_4_1_FURTIVITE
    step_until_decision(state)

    # G7:B a posé le Piège sous la machine en Siège (case 2 allumée) ET G3:B a glissé 1 Défenseur dessus (armé !)
    assert state.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert state.get_parcel_defenseurs(0, 2) == 1
    assert state.count_gardien_pari_consumed_at_case(2) >= 1  # Case 2 s'est allumée !

    # Vérification de la frappe de Ratissage : le Piège sous la machine pare immédiatement !
    arbres_before = state.get_parcel_arbres(0, 2)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], is_ratissage=True)
    assert state.get_parcel_piege(0, 2) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(0, 2) == arbres_before


# ---------------------------------------------------------------------------
# 5. G7:C — La Loutre géante (LOI 5 : Défenseurs après le 1er doublés sur M et H)
# Témoin : "2 Défenseurs valent 3 points de Défense, épargnant les Insectes locaux."
# ---------------------------------------------------------------------------
def test_g7_c_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "H", "O", "R"),
        tile_profiles=(("G7", "C"), ("G10", "A")),
        exp_seed=1305,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(4, 7, face=1)
    state.place_defender_gardien_pari(0, 4, 2)
    state.set_gardien_at_case(1, 10, face=1)
    state.place_defender_gardien_pari(1, 1, 2)

    # Rayon M (0), p=2 : 2 Défenseurs + 2 Insectes locaux face à un Seuil de 3 (T1 base 2 + 1 rouge)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    state.place_defender_foret(0, 0, 0, 2, FACE_DEFINITIF)
    state.place_defender_foret(1, 0, 0, 2, FACE_DEFINITIF)
    state.set_parcel_insectes(0, 2, 2)
    arbres_before = state.get_parcel_arbres(0, 2)

    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])

    # 2 Défenseurs = 2 + (2 - 1) = 3 points de Défense >= Seuil 3 -> parade réussie et 0 Insecte sacrifié !
    assert state.get_parcel_arbres(0, 2) == arbres_before
    assert state.get_parcel_insectes(0, 2) == 2
    assert state.count_gardien_pari_consumed_at_case(1) >= 1  # Case 1 (Parade) s'est bien allumée !

    # Hors périmètre (rayon O = 2) : 2 Défenseurs ne valent que 2 points (< Seuil 3) -> 1 Insecte local est sacrifié
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(2, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    state.place_defender_foret(2, 0, 2, 2, FACE_DEFINITIF)
    state.place_defender_foret(3, 0, 2, 2, FACE_DEFINITIF)
    state.set_parcel_insectes(2, 2, 2)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_insectes(2, 2) == 1


# ---------------------------------------------------------------------------
# 6. G7:D — Le barrage habité du Capybara (OUVERTURE : Piège sur M/H habité)
# Témoin : "Pose un Piège immédiatement armé par la présence locale (un soutien
# distant seul ne suffit pas pour la pose)."
# ---------------------------------------------------------------------------
def test_g7_d_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "H", "R", "O"),
        tile_profiles=(("G7", "D"),),
        exp_seed=1306,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(4, 7, face=1)
    state.place_defender_gardien_pari(0, 4, 2)

    # Sur M(0) : p=1 a 1 Défenseur mais p=2 est vide (soutien distant éventuel ne suffit PAS pour p=2 !)
    # Sur H(1) : p=2 est occupée par une machine ET contient 1 Insecte local -> éligible !
    # Sur R(2) : p=1 contient 1 Défenseur mais n'est ni M ni H -> non éligible !
    state.place_defender_foret(0, 0, 0, 1, FACE_DEFINITIF)
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_parcel_insectes(1, 2, 1)
    state.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)

    state.light_trigger(4)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.options == ("PASSER", (0, 1), (1, 2))
    assert (0, 2) not in req.options  # Vide de pion local -> interdit !
    assert (2, 1) not in req.options  # Rayon R -> interdit !

    # Pose sur H(1, 2) occupée par le Bulldozer : Piège actif + case 2 allumée !
    apply_choice(state, (1, 2))
    assert state.get_parcel_piege(1, 2) == PIEGE_ACTIF
    assert state.is_trigger_lit(2) is True


# ---------------------------------------------------------------------------
# 7. G8:A — Le Sillage du Boto (3.2 / OUVERTURE : décalage des frappes non-Siège)
# Témoin : "Saute les Routes Forestières ; le décalage s’applique aux cibles lues
# depuis la position réelle de la machine à l’instant où elle attaque."
# ---------------------------------------------------------------------------
def test_g8_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "I", "O", "R"),
        tile_profiles=(("G8", "A"),),
        exp_seed=1307,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 8, face=1)
    state.place_defender_gardien_pari(0, 1, 2)

    # Ouvert avant 3.2 -> préparé pour la Révélation 3.2
    state.light_trigger(1)
    sweep_gardiens(state)

    # Rayon M(0) : Abatteuse en p=2, Route Forestière (0/0) en p=3, intacte en p=4 (4 Arbres)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_parcel_arbres_souches(0, 3, 0, 0)  # Route Forestière en p=3 !
    state.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 0)

    state.step = STEP_3_2_REVEAL
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G8"
    assert (0, MACHINE_ABATTEUSE, 1) in req.options
    assert (0, MACHINE_ABATTEUSE, -1) in req.options

    # Choisir +1 (vers le cœur)
    apply_choice(state, (0, MACHINE_ABATTEUSE, 1))

    # Vérifions aussi la seconde partie du témoin : si la machine recule en p=1 avant son attaque
    # (position réelle à l'instant où elle attaque = p=1), alors T1 lit sa cible depuis p=1
    # puis la décale de +1 parcelle non rasée -> frappe p=2, SANS déplacer la machine !
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    arbres_p1 = state.get_parcel_arbres(0, 1)
    arbres_p2 = state.get_parcel_arbres(0, 2)
    arbres_p4 = state.get_parcel_arbres(0, 4)

    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 1) == arbres_p1
    assert state.get_parcel_arbres(0, 2) == arbres_p2 - 2
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 1

    # Testons maintenant le saut de Route Forestière p=3 depuis p=2 avec +1 : frappe p=4 !
    state.cleanup_end_of_turn_6_2()
    state.place_defender_gardien_pari(2, 1, FACE_DEFINITIF)
    state.paravents_ouverts = True
    state.step = STEP_3_2_REVEAL
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.light_trigger(1)
    sweep_gardiens(state)
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    apply_choice(state, (0, MACHINE_ABATTEUSE, 1))

    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 4) == arbres_p4 - 2  # A sauté la Route Forestière p=3 !
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2


# ---------------------------------------------------------------------------
# 8. G8:B — Le Sillage du Boto (LOI 5 : Bulldozer avant Abatteuse)
# Témoin : "Sur 3 Arbres sans Souche : le Bulldozer coupe 1 Arbre (0 Souche à
# terrasser), puis l’Abatteuse coupe les 2 Arbres restants en 2 Souches
# (évite la Route Forestière !)."
# ---------------------------------------------------------------------------
def test_g8_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "I", "O", "R"),
        tile_profiles=(("G8", "B"),),
        exp_seed=1308,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(3, 8, face=1)
    state.place_defender_gardien_pari(0, 3, 2)

    # Rayon 0, parcelle p=3 : exactement 3 Arbres et 0 Souche !
    state.set_tactique_at_rank(0, 1)  # T1 : SUR_PLACE, avancée 0
    state.set_tactique_at_rank(1, 5)  # T5 : SUR_PLACE + DEVANT, avancée 0
    state.set_parcel_arbres_souches(0, 3, 3, 0)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    state.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 1, 1, 1)
    state.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 1, 1, 1, 1)

    state.paravents_ouverts = True
    state.step = STEP_5_1_TACTIQUES
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.options == ("PASSER", 0)

    # Activer l'inversion sur le rayon 0 : Bulldozer résolu avant Abatteuse !
    apply_choice(state, 0)
    step_until_decision(state)

    # Bulldozer a coupé 1 Arbre (0 Souche à terrasser -> 2 Arbres, 0 Souche),
    # puis Abatteuse a coupé les 2 Arbres restants en 2 Souches -> (0 Arbre, 2 Souches), PAS de Route Forestière !
    assert state.get_parcel_arbres(0, 3) == 0
    assert state.get_parcel_souches(0, 3) == 2
    assert state.is_route_forestiere(0, 3) is False


# ---------------------------------------------------------------------------
# 9. G9:A — Le Guet du Caïman Noir (DOUBLE_FACE : +1 puis +2 cartes Sabotage)
# Témoin : "Dilue durablement le paquet Machine en réaction à n’importe quel
# Déclencheur (réserve de cartes Sabotage illimitée)."
# ---------------------------------------------------------------------------
def test_g9_a_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("R", "O", "M", "H"),
        tile_profiles=(("G9", "A"), ("G10", "A")),
        exp_seed=1309,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 9, face=1)
    state.place_defender_gardien_pari(0, 1, 2)
    state.set_gardien_at_case(3, 10, face=1)
    state.place_defender_gardien_pari(1, 3, 2)
    sab_deck_init = state.sabotage_deck_count
    assert state.sabotage_pending_count == 0

    # 1) Face 1 : +1 Sabotage mis de côté + allume case 3 (active G10 en cascade !) + passe en Face 2
    state.light_trigger(1)
    sweep_gardiens(state)
    assert state.sabotage_pending_count == 1
    assert state.count_gardien_pari_consumed_at_case(3) >= 1
    assert state.get_gardien_at_case(1) == (9, 1)
    from engine.core_engine import _resolve_gardien_bets_5_3
    _resolve_gardien_bets_5_3(state)
    assert state.get_gardien_at_case(1) == (9, 2)

    # Remélange 6.3 : intègre durablement la carte au paquet Machine
    state.cleanup_end_of_turn_6_2()
    state.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    state.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
    assert state.sabotage_deck_count == sab_deck_init + 1
    assert state.sabotage_pending_count == 0

    # 2) Face 2 autonome : +2 Sabotages mis de côté + allume case 3 (active à nouveau G10 !)
    state.light_trigger(1)
    sweep_gardiens(state)
    assert state.sabotage_pending_count == 2
    assert state.count_gardien_pari_consumed_at_case(3) >= 1
    state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
    assert state.sabotage_deck_count == sab_deck_init + 3


# ---------------------------------------------------------------------------
# 10. G9:B — Le Guet du Caïman Noir (LOI 4.1 Sabotage actif + Face 2 LOI 3.2)
# Témoin : "En Face 2, chaque panne tirée en 3.2 déclenche une cascade sur la
# case 3 (une seule activation max du Gardien câblé en 3) et affaiblit les
# machines sur R/H avant que la carte Sabotage ne soit remélangée en 6.3."
# ---------------------------------------------------------------------------
def test_g9_b_temoin() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("R", "H", "M", "O"),
        tile_profiles=(("G9", "B"), ("G10", "A")),
        exp_seed=1310,
    )
    state = GameState(cfg)
    state.set_gardien_at_case(1, 9, face=1)
    state.place_defender_gardien_pari(0, 1, 2)
    state.set_gardien_at_case(3, 10, face=1)
    state.place_defender_gardien_pari(1, 3, 2)

    # 1) Face 1 en 4.1 : binôme en Furtivité sabote même une machine en Siège !
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_RATISSAGE)
    state.enter_furtivite(0, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    state.enter_furtivite(1, 0, 0, 2, rive=0, face=FACE_DEFINITIF)
    # 1 Insecte témoin en (2, 1) suspend la boucle en 4.3 juste après 4.1
    state.set_parcel_insectes(2, 1, 1)
    state.step = STEP_4_1_FURTIVITE
    step_until_decision(state)
    assert state.sabotage_pending_count == 1
    assert state.count_gardien_pari_consumed_at_case(3) >= 1  # Case 3 allumée par le Sabotage 4.1 !

    # L'ouverture de G9 en Face 1 puis 5.3 le retourne en Face 2
    state.light_trigger(1)
    sweep_gardiens(state)
    assert state.get_gardien_at_case(1) == (9, 1)
    from engine.core_engine import _resolve_gardien_bets_5_3
    _resolve_gardien_bets_5_3(state)
    assert state.get_gardien_at_case(1) == (9, 2)

    # 2) Face 2 autonome en 3.2 (témoin exact) :
    # 2 cartes Sabotage révélées derrière les paravents ; machines sur R(0) et H(1) portent chacune 2 rouges ;
    # G10:A attend sur la case 3 (ne doit s'activer qu'UNE seule fois malgré 2 pannes révélées !).
    state._continuation.clear()
    state.cleanup_end_of_turn_6_2()
    state.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    state.set_parcel_insectes(2, 1, 1)
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 0, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=2, bleus=0)

    state.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    state.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    state.set_player_hand(2, 5, 2, 3, 2, 0)
    state.set_player_hand(3, 7, 1, 4, 1, 0)

    state.step = STEP_3_2_REVEAL
    req_1 = step_until_decision(state)
    assert isinstance(req_1, DecisionRequest)
    assert req_1.context.get("effect_kind") == "REMOVE_RED_R_H"
    apply_choice(state, (0, MACHINE_ABATTEUSE))

    req_2 = step_until_decision(state)
    assert isinstance(req_2, DecisionRequest)
    assert req_2.context.get("effect_kind") == "REMOVE_RED_R_H"
    apply_choice(state, (1, MACHINE_BULLDOZER))

    step_until_decision(state)

    # Les 2 machines sur R et H ont chacune perdu 1 jeton rouge (2 -> 1),
    # et le Gardien G10 câblé en case 3 s'est activé exactement 1 fois (pending_voluntary_app == 1) !
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)
    assert state.get_machine_tokens(1, MACHINE_BULLDOZER) == (1, 0)
    assert state.get_gardien_at_case(3) == (10, 1)
    assert state.count_gardien_pari_consumed_at_case(3) == 1
