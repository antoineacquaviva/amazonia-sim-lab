"""Tests témoins déterministes du Lot 04 (G10:B..G12:C — 10 Gardiens Reptiles & Oiseaux)."""

from __future__ import annotations

from engine.core_engine import (
    CAUSE_REVE_RANG_1,
    apply_choice,
    list_legal_targets,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects import load_all_effects
from engine.effects.lot_04 import LOT_04_PROFILES
from engine.effects.registry import get_tile_registration
from engine.primitives import DecisionRequest, GameOver
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    STEP_4_2_NIDS,
    STEP_5_3_END_CHECK,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
)


def _make_mode3_state(
    tile_profiles: tuple[tuple[str, str], ...],
    *,
    peuples: tuple[str, ...] = ("M", "O", "R", "H"),
    seed: int = 42,
) -> GameState:
    load_all_effects()
    base = GameConfig.from_chassis_index(
        0,
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
        exp_seed=seed,
        rep_id=0,
    )
    cfg = GameConfig(
        n_players=base.n_players,
        mode=3,
        peuples=base.peuples,
        exp_seed=base.exp_seed,
        rep_id=base.rep_id,
        p_max=base.p_max,
        dotation_arbres=base.dotation_arbres,
        lisiere_slots=base.lisiere_slots,
        tile_profiles=tile_profiles,
    )
    return GameState(cfg)


def test_lot_04_all_10_profiles_registered() -> None:
    load_all_effects()
    for slot_id, prof in LOT_04_PROFILES:
        assert get_tile_registration(slot_id, prof) is not None, f"Manquant : {slot_id}:{prof}"


def test_g10_b_temoin() -> None:
    """G10:B — S’applique en 5.3 avant le retrait des Pièges déclenchés, une fois par couple Piège–machine parée."""
    state = _make_mode3_state((("G10", "B"),))
    state.set_gardien_at_case(2, 10, 1, False)

    # Sur le rayon 2 (R), p=1 a un Piège armé par 1 Défenseur ; Abatteuse et Bulldozer avec 2 jetons Rouges
    state.set_parcel_piege(2, 1, PIEGE_ACTIF)
    state.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    state.set_machine_tokens(2, MACHINE_ABATTEUSE, 2, 0)
    state.set_machine_pos_status(2, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL, False)
    state.set_machine_tokens(2, MACHINE_BULLDOZER, 2, 0)

    # L'Abatteuse attaque (2, 1) DEUX fois et le Bulldozer attaque (2, 1) UNE fois -> 2 couples (Piège, machine)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    resolve_single_machine_attack(state, 2, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_piege(2, 1) == PIEGE_DECLENCHE

    # Passage en 5.3 : G10:B s'applique avant retrait du Piège, une seule fois par couple Piège–machine parée
    state.step = STEP_5_3_END_CHECK
    req_ab = step_until_decision(state)
    assert isinstance(req_ab, DecisionRequest)
    assert req_ab.context.get("slot_id") == "G10"
    assert state.get_parcel_piege(2, 1) == PIEGE_DECLENCHE
    assert ("SURCHAUFFE_BLEU", 2, MACHINE_ABATTEUSE, 1) in req_ab.options

    apply_choice(state, ("SURCHAUFFE_BLEU", 2, MACHINE_ABATTEUSE, 1))
    assert state.get_machine_tokens(2, MACHINE_ABATTEUSE) == (1, 1)

    # La décision suivante concerne directement le Bulldozer (l'Abatteuse n'est pas sollicitée une 2e fois)
    req_bu = step_until_decision(state)
    assert isinstance(req_bu, DecisionRequest)
    assert req_bu.context.get("slot_id") == "G10"
    assert ("RETIRER_ROUGE", 2, MACHINE_BULLDOZER, 1) in req_bu.options
    apply_choice(state, ("RETIRER_ROUGE", 2, MACHINE_BULLDOZER, 1))
    assert state.get_machine_tokens(2, MACHINE_BULLDOZER) == (1, 0)

    # Plus aucune décision G10:B ; STEP_5_3_FINISH retire ensuite le Piège déclenché
    step_until_decision(state)
    assert state.get_parcel_piege(2, 1) == PIEGE_AUCUN


def test_g10_c_temoin() -> None:
    """G10:C — En 4.2, l’Insecte produit par un Nid peut payer ce coût après le bloc indivisible du Nid pour diluer durablement le paquet Machine."""
    state = _make_mode3_state(
        (("G10", "C"), ("G1", "A"), ("M1", "B")),
        peuples=("M", "O", "R", "I"),
    )
    # G10:C câblé sur 6. Insecte ; G1:A témoin sur 3. Sabotage
    state.set_gardien_at_case(6, 10, 1, False)
    state.set_gardien_at_case(3, 1, 1, False)

    # Nid M1 sur (3, 1) habité par 1 Défenseur (0 Insecte avant 4.2)
    state.set_parcel_nid(3, 1, 1, False)
    state.place_defender_foret(3, 0, 3, 1, FACE_DEFINITIF)
    sab_pending_before = state.sabotage_pending_count

    # Étape 4.2 : le Nid produit 1 Insecte et allume la case 6 -> G10:C s'ouvre après le bloc du Nid
    state.step = STEP_4_2_NIDS
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G10"
    assert (3, 1) in req.options

    # L'Insecte tout juste produit par le Nid paye le coût -> +1 Sabotage (allume la case 3)
    apply_choice(state, (3, 1))
    assert state.get_parcel_insectes(3, 1) == 0
    assert state.sabotage_pending_count == sab_pending_before + 1

    # Le balayage en cours fait une repasse 1..6 et ouvre G1:A en case 3 (allumée par la création du Sabotage)
    state._continuation.append(("WAIT_DECISION", DecisionRequest(0, "STOP", ("OK",), {})))
    step_until_decision(state)
    assert state.get_gardien_at_case(3)[2] is True
    assert state.get_gardien_at_case(6)[2] is True


def test_g10_d_temoin() -> None:
    """G10:D — Une première Embuscade réussie crée la sentinelle qui arme immédiatement une seconde Embuscade."""
    state = _make_mode3_state(
        (("G10", "D"),),
        peuples=("M", "O", "R", "E"),
    )
    state.set_gardien_at_case(2, 10, 1, False)

    # Rayon 2 (R) : p=1 a un Piège armé par 1 Défenseur ; p=2 a un Piège DÉSARMÉ (0 Défenseur, 0 Insecte)
    state.set_parcel_piege(2, 1, PIEGE_ACTIF)
    state.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)
    state.set_parcel_piege(2, 2, PIEGE_ACTIF)
    assert state.get_parcel_defenseurs(2, 2) == 0
    assert state.get_parcel_insectes(2, 2) == 0

    arbres_p2_before = state.get_parcel_arbres(2, 2)
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)

    # T3 frappe SUR_PLACE (p=1) puis DEVANT (p=2) : la 1re parade par Piège suspend pour G10:D
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G10"
    assert (2, 2) in req.options

    # On crée la sentinelle Insecte sur (2, 2), ce qui arme immédiatement le second Piège pour la frappe DEVANT !
    apply_choice(state, (2, 2))
    assert state.get_parcel_insectes(2, 2) == 1

    # On laisse la 2e frappe (DEVANT sur p=2) se résoudre : le Piège de p=2 est désormais armé et pare la frappe !
    state._continuation.append(("WAIT_DECISION", DecisionRequest(0, "STOP", ("OK",), {})))
    step_until_decision(state)
    assert state.get_parcel_piege(2, 2) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(2, 2) == arbres_p2_before


def test_g11_a_temoin() -> None:
    """G11:A — 2e maillon de la chaîne des parades (après Jaguar, avant Piège) : pare la frappe sans déclencher un éventuel Piège présent."""
    state = _make_mode3_state((("G11", "A"),))
    # G11:A déjà retourné en Face 2 sur la case 4
    state.set_gardien_at_case(4, 11, 2, False)

    # Parcelle (1, 1) avec 2 Défenseurs ET un Piège actif ; une autre parcelle (0, 1) avec 2 Défenseurs pour provoquer le choix
    state.place_defender_foret(1, 0, 1, 1, FACE_DEFINITIF)
    state.place_defender_foret(1, 1, 1, 1, FACE_DEFINITIF)
    state.set_parcel_piege(1, 1, PIEGE_ACTIF)
    state.place_defender_foret(0, 0, 0, 1, FACE_DEFINITIF)
    state.place_defender_foret(0, 1, 0, 1, FACE_DEFINITIF)

    state.light_trigger(4)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G11"
    apply_choice(state, (1, 1))

    # L'Abatteuse attaque (1, 1) avec T1 : la Piquée de la Harpie (2e maillon) pare AVANT le Piège (3e maillon)
    arbres_before = state.get_parcel_arbres(1, 1)
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])

    assert state.get_parcel_arbres(1, 1) == arbres_before
    # Le Piège n'a PAS été déclenché et reste PIEGE_ACTIF !
    assert state.get_parcel_piege(1, 1) == PIEGE_ACTIF


def test_g11_b_temoin() -> None:
    """G11:B — Fournit un soutien à distance capable d’armer les Pièges Embuscade en face."""
    state = _make_mode3_state((("G11", "B"),))
    state.set_gardien_at_case(2, 11, 1, False)

    # Parcelle (1, 1) (Oiseaux) contient un Piège SANS Défenseur ni Insecte sur la parcelle
    state.set_parcel_piege(1, 1, PIEGE_ACTIF)
    assert state.get_parcel_defenseurs(1, 1) == 0
    assert state.get_parcel_insectes(1, 1) == 0

    # Un Défenseur isolé est en Furtivité sur la lisière 0 (M_O, entre 0 et 1) à profondeur p=1
    state.enter_furtivite(0, 0, 0, 1, 0, FACE_DEFINITIF)
    assert state.get_furtivite_total_defs(0, 1) == 1

    arbres_before = state.get_parcel_arbres(1, 1)
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])

    # Le soutien à distance (+1 Défense) a armé le Piège Embuscade de (1, 1), qui a paré la frappe !
    assert state.get_parcel_piege(1, 1) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(1, 1) == arbres_before

    # En Face 2, un Défenseur constructeur resté en bordure de lisière ajoute aussi +1 en Défense sur p=1 adjacent
    state.set_gardien_at_case(2, 11, 2, False)
    state.remove_player_defender(0, 0)
    state.set_parcel_piege(1, 1, PIEGE_ACTIF)
    # 1 bâtisseur sur le slot 2 (lisière 1, entre rayon 1 et rayon 2)
    state.set_lisiere_tile_state(2, LISIERE_UNCONSTRUCTED, 1)
    resolve_single_machine_attack(state, 1, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_piege(1, 1) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(1, 1) == arbres_before


def test_g11_c_temoin() -> None:
    """G11:C — Offre un point d’ancrage global dès 2.1 (le Défenseur se pose sur l’un des 4 emplacements valides de la case)."""
    # Table à 4 joueurs ("M", "O", "H", "R") : la lisière O–H est l_idx = 1 (entre siège 1=O et siège 2=H)
    state = _make_mode3_state(
        (("G11", "C"),),
        peuples=("M", "O", "H", "R"),
    )
    state.set_gardien_at_case(3, 11, 1, False)

    # Sans Insecte sur la lisière O–H (l_idx=1), le joueur 0 (M) n'a pas accès à la lisière 1 en 2.1
    targets_before = list_legal_targets(state, 0, is_first_defender=True)
    assert ("FURTIVITE", 1, 2, 0) not in targets_before
    assert ("FURTIVITE", 1, 2, 1) not in targets_before

    # Avec 1 Insecte sur la case Furtivité (l_idx=1, p=2), le joueur 0 (M) et le joueur 3 (R) peuvent s'y ancrer dès 2.1 !
    state.set_furtivite_insectes(1, 2, 1)
    targets_m = list_legal_targets(state, 0, is_first_defender=True)
    targets_r = list_legal_targets(state, 3, is_first_defender=True)
    assert ("FURTIVITE", 1, 2, 0) in targets_m
    assert ("FURTIVITE", 1, 2, 1) in targets_m
    assert ("FURTIVITE", 1, 2, 0) in targets_r
    assert ("FURTIVITE", 1, 2, 1) in targets_r


def test_g11_d_temoin() -> None:
    """G11:D — Permet à un binôme de travailler en Furtivité en 4.1 tout en armant à distance les Pièges en face à l’Étape 5."""
    state = _make_mode3_state(
        (("G11", "D"),),
        peuples=("M", "O", "H", "R"),
    )
    state.set_gardien_at_case(2, 11, 1, False)

    # Binôme de 2 Défenseurs en Furtivité sur la lisière 1 (O–H) à profondeur p=1
    state.enter_furtivite(1, 0, 1, 1, 0, FACE_DEFINITIF)
    state.enter_furtivite(2, 0, 1, 1, 0, FACE_DEFINITIF)
    assert state.get_furtivite_total_defs(1, 1) == 2

    # Piège posé sur la parcelle (1, 1) (Oiseaux) sans aucun Défenseur ni Insecte sur la parcelle
    state.set_parcel_piege(1, 1, PIEGE_ACTIF)
    arbres_before = state.get_parcel_arbres(1, 1)

    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])

    # Le binôme en Furtivité a fourni 1 point de Défense à la parcelle piégée d'Oiseaux en face -> Embuscade armée !
    assert state.get_parcel_piege(1, 1) == PIEGE_DECLENCHE
    assert state.get_parcel_arbres(1, 1) == arbres_before


def test_g12_a_temoin() -> None:
    """G12:A — Si le Rêve atteint ainsi le Rang 1, le Sommeil du Contremaître sera validé lors de la vérification de fin d’attaques en 5.3."""
    state = _make_mode3_state((("G12", "A"), ("G1", "A")))
    state.set_gardien_at_case(2, 12, 1, False)
    # Gardien témoin en case 5 pour vérifier que G12:A n'allume PAS la case 5
    state.set_gardien_at_case(5, 1, 1, False)

    # Rêve R1 au Rang 2 (indice 1) et Rêve R2 au Rang 4 (indice 3) — 2 candidats -> décision Oiseaux
    t_rank0 = state.get_tactique_at_rank(0)
    state.set_tactique_at_rank(1, TILE_R_BASE + 1)
    state.set_tactique_at_rank(3, TILE_R_BASE + 2)

    state.light_trigger(2)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G12"
    assert 1 in req.options and 3 in req.options

    # On avance le Rêve du Rang 2 (indice 1) vers le Rang 1 (indice 0)
    apply_choice(state, 1)
    assert state.get_tactique_at_rank(0) == TILE_R_BASE + 1
    assert state.get_tactique_at_rank(1) == 2  # Tactique imprimée T2 révélée sur la piste fixe
    # Sans ouvrir son Slot ni allumer la case 5
    assert state.has_reve_opened_this_turn(1) is False
    assert state.get_gardien_at_case(5)[2] is False

    # Avec un seul Rêve en tête (sur 2 en jeu), pas encore Sommeil ; dès que R2 rejoint le Rang 2 -> Sommeil en 5.3 !
    assert state.is_sommeil_victory() is False
    state.set_tactique_at_rank(1, TILE_R_BASE + 2)
    state.set_tactique_at_rank(3, t_rank0)
    state.step = STEP_5_3_END_CHECK
    res = step_until_decision(state)
    assert isinstance(res, GameOver)
    assert res.cause_fin == CAUSE_REVE_RANG_1


def test_g12_b_temoin() -> None:
    """G12:B — Ne peut pas retourner gratuitement le cycle nourri de G14 C, mais peut ouvrir son Slot."""
    state = _make_mode3_state((("G12", "B"), ("G14", "C"), ("G11", "B")))
    # Case 1 : G12:B ; Case 3 : G14:C (DOUBLE_FACE_CYCLE, Face 1, non utilisé) ; Case 4 : G11:B (DOUBLE_FACE_UPGRADE, Face 1, déjà utilisé)
    state.set_gardien_at_case(1, 12, 1, False)
    state.set_gardien_at_case(3, 14, 1, False)
    state.set_gardien_at_case(4, 11, 1, True)

    state.light_trigger(1)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G12"

    # G14:C ne peut PAS être retourné gratuitement en Face 2, mais son Slot disponible peut être ouvert !
    assert ("FLIP_FACE2", 3) not in req.options
    assert ("OPEN_SLOT", 3) in req.options
    # G11:B est un Gardien évolutif (DOUBLE_FACE_UPGRADE) : il peut être retourné en Face 2 (mais son Slot est déjà utilisé)
    assert ("FLIP_FACE2", 4) in req.options
    assert ("OPEN_SLOT", 4) not in req.options

    apply_choice(state, ("FLIP_FACE2", 4))
    assert state.get_gardien_at_case(4) == (11, 2, True)


def test_g12_c_temoin() -> None:
    """G12:C — Peut consommer le Piège non déclenché pour avancer le Rêve le plus à gauche (excluant un Piège déclenché)."""
    state = _make_mode3_state((("G12", "C"),))
    # G12:C câblé sur 2. Piégeage
    state.set_gardien_at_case(2, 12, 1, False)

    # Rêve R1 au Rang 2 (indice 1) ; un Piège actif sur (0, 1) et un Piège déjà déclenché sur (1, 1)
    state.set_tactique_at_rank(1, TILE_R_BASE + 1)
    state.set_parcel_piege(0, 1, PIEGE_ACTIF)
    state.set_parcel_piege(1, 1, PIEGE_DECLENCHE)

    # L'allumage de la case 2 (ex: pose d'un Piège en 4.1) ouvre G12:C
    state.light_trigger(2)
    sweep_gardiens(state)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("slot_id") == "G12"
    # Seul le Piège non déclenché (0, 1) peut payer le coût ; le Piège déclenché (1, 1) est exclu !
    assert (0, 1) in req.options
    assert (1, 1) not in req.options

    apply_choice(state, (0, 1))
    assert state.get_parcel_piege(0, 1) == PIEGE_AUCUN
    assert state.get_tactique_at_rank(0) == TILE_R_BASE + 1

    # Compléter le bloc de 2 Rêves en tête (R1 + R2) valide le Sommeil du Contremaître en 5.3 !
    state.set_tactique_at_rank(1, TILE_R_BASE + 2)
    state.step = STEP_5_3_END_CHECK
    res = step_until_decision(state)
    assert isinstance(res, GameOver)
    assert res.cause_fin == CAUSE_REVE_RANG_1
