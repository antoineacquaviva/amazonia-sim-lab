"""Tests témoins déterministes du Lot 06 (Rêves R1:A..R4:D, 11 profils)."""

from __future__ import annotations

from engine.core_engine import (
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_RETRAIT_APPRENTISSAGE_6_1,
    _run_step_6_1,
    apply_choice,
    compute_parade_seuil,
    insert_reve_on_track,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.effects import load_all_effects
from engine.effects.lot_06 import LOT_06_PROFILES
from engine.effects.registry import clear_tile_registry, get_tile_registration
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    DEC_EFFET_TUILE,
    HOOK_GARDIEN_OUVERTURE,
    DecisionRequest,
    GameOver,
    register_tile,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_3_MIGRATION,
    STEP_5_3_END_CHECK,
    STEP_6_1_APPRENTISSAGE,
    STEP_6_2_EVOLUTION,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    GameConfig,
    GameState,
    machine_card_code,
)


def _make_state(
    *profiles: tuple[str, str],
    peuples: tuple[str, ...] = ("H", "R", "E", "M"),
) -> GameState:
    load_all_effects()
    cfg = GameConfig(
        n_players=len(peuples),
        mode=3,
        peuples=peuples,
        tile_profiles=tuple(profiles),
    )
    return GameState(cfg)


def _add_step_4_3_stop_anchor(state: GameState) -> None:
    """Pose 1 Insecte témoin sur le dernier rayon pour suspendre proprement en 4.3 (avant ménage 6.2)."""
    anchor_ray = state.cfg.n_players - 1
    p_anchor = state.cfg.p_max
    state.set_parcel_insectes(anchor_ray, p_anchor, state.get_parcel_insectes(anchor_ray, p_anchor) + 1)


def _setup_reve_opening_3_2(
    state: GameState,
    r_num: int,
    rank_0_5: int,
    reader_seat: int = 0,
    *,
    stop_in_4_3: bool = True,
) -> None:
    """Place le Rêve R{r_num} au rang `rank_0_5` et configure la main de `reader_seat` pour le lire en 3.2."""
    state.set_tactique_at_rank(rank_0_5, TILE_R_BASE + r_num)
    card = machine_card_code(reader_seat, MACHINE_ABATTEUSE)
    m_val = rank_0_5 + 1
    state.set_player_hand(reader_seat, card, m_val, 6, m_val, 0)
    if stop_in_4_3:
        _add_step_4_3_stop_anchor(state)
    state.step = STEP_3_2_REVEAL


def test_lot_06_all_11_profiles_registered() -> None:
    """Vérifie que les 11 profils du Lot 06 sont enregistrés (total cumulé >= 62/100)."""
    registered = load_all_effects()
    for slot_id, prof in LOT_06_PROFILES:
        assert (slot_id, prof) in registered
        assert get_tile_registration(slot_id, prof) is not None
    assert len(registered) >= 62


def test_r1_a_temoin_tambour_echange_tactiques_avant_avancee() -> None:
    """Témoin R1:A : échange deux Tactiques adjacentes avant l'avancée de R1 pour faire éjecter T6."""
    state = _make_state(("R1", "A"))
    # Piste initiale : [T1, T2, T3, T6, T5, R1] -> échanger T6 (idx 3) et T5 (idx 4) pousse T6 à droite
    track_init = (1, 2, 3, 6, 5, TILE_R_BASE + 1)
    for idx, code in enumerate(track_init):
        state.set_tactique_at_rank(idx, code)
    _setup_reve_opening_3_2(state, 1, 5, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert req.decideur == 0  # Humains
    assert (3, 4) in req.options
    assert (4, 5) not in req.options  # R1 n'est pas une Tactique
    assert state.is_trigger_lit(5)

    # Pousser T6 de l'indice 3 vers l'indice 4 avant que R1 n'avance de 5 vers 4 !
    apply_choice(state, (3, 4))
    anchor_req = step_until_decision(state)
    assert isinstance(anchor_req, DecisionRequest)
    assert anchor_req.decision_type == DEC_MIGRATION_INSECTE_4_3

    # Après l'échange (T5 en 3, T6 en 4) puis l'avancée de R1 (4 <-> 5) : [T1, T2, T3, T5, R1, T6]
    after_track = tuple(state.get_tactique_at_rank(i) for i in range(TRACK_LEN))
    assert after_track == (1, 2, 3, 5, TILE_R_BASE + 1, 6)

    # Le prochain Rêve construit éjecte bien T6 (la Tactique la plus à droite) !
    ejected = insert_reve_on_track(state, 2)
    assert ejected == 6


def test_r1_b_temoin_double_avancee_sommeil_contremaitre() -> None:
    """Témoin R1:B : avance de jusqu'à 2 rangs vers la gauche pour compléter le bloc de Rêves en tête (5.3)."""
    state = _make_state(("R1", "B"), peuples=("H", "R", "O", "M"))
    # 1 peuple onirique (H) => 2 Rêves en jeu : R2 déjà en rang 1 (index 0), R1 en rang 4 (index 3)
    track_init = (TILE_R_BASE + 2, 1, 2, TILE_R_BASE + 1, 3, 4)
    for idx, code in enumerate(track_init):
        state.set_tactique_at_rank(idx, code)
    _setup_reve_opening_3_2(state, 1, 3, reader_seat=0)

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 0  # Humains
    assert req.options == (1, 2)

    # Choisir d'avancer de 2 rangs -> R1 atteint le Rang 2 (index 1), complétant le bloc [R2, R1] !
    apply_choice(state, 2)
    step_until_decision(state)
    assert state.get_tactique_at_rank(0) == TILE_R_BASE + 2
    assert state.get_tactique_at_rank(1) == TILE_R_BASE + 1

    # En fin de 5.3, le Sommeil du Contremaître déclenche la victoire par bloc de Rêves en tête
    state._continuation.clear()
    state.step = STEP_5_3_END_CHECK
    out = step_until_decision(state)
    assert isinstance(out, GameOver)
    assert out.cause_fin == CAUSE_REVE_RANG_1


def test_r1_c_temoin_offrande_gardien_sans_sacrifice() -> None:
    """Témoin R1:C : renvoie 1 Gardien en lisière (Face 1, sans sacrifice) pour avancer de 2 rangs."""
    state = _make_state(("R1", "C"), ("G4", "A"), peuples=("H", "O", "M", "E"))
    g4_slot = state.find_lisiere_slot_by_tile_id("G4")
    assert g4_slot is not None
    state.set_lisiere_tile_state(g4_slot, LISIERE_CONSTRUCTED, 0)
    # G4 sur la piste en case 2, Face 2, déjà marqué utilisé
    state.set_gardien_at_case(2, 4, 2, True)

    # R1 au Rang 4 (index 3)
    track_init = (1, 2, 3, TILE_R_BASE + 1, 4, 5)
    for idx, code in enumerate(track_init):
        state.set_tactique_at_rank(idx, code)
    _setup_reve_opening_3_2(state, 1, 3, reader_seat=0)

    # Tester d'abord l'option PASSER sur un clone
    clone_pass = state.clone()
    req_pass = step_until_decision(clone_pass)
    assert isinstance(req_pass, DecisionRequest)
    assert "PASSER" in req_pass.options
    apply_choice(clone_pass, "PASSER")
    step_until_decision(clone_pass)
    assert clone_pass.step == STEP_4_3_MIGRATION
    assert clone_pass.find_tactique_rank(TILE_R_BASE + 1) == 2  # Avancé d'1 seul rang
    assert clone_pass.get_gardien_at_case(2) == (4, 2, True)

    # Sur l'état principal : payer l'offrande de G4 (case 2) pour avancer de 2 rangs (index 3 -> index 1)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert (2, 2) in req.options
    apply_choice(state, (2, 2))
    step_until_decision(state)

    assert state.step == STEP_4_3_MIGRATION
    assert state.find_tactique_rank(TILE_R_BASE + 1) == 1
    assert state.get_gardien_at_case(2) == (0, 1, False)
    assert state.get_lisiere_tile_state(g4_slot) == (LISIERE_UNCONSTRUCTED, 0)


def test_r2_a_temoin_voile_oubli_avant_bugs_6_1() -> None:
    """Témoin R2:A : retire jusqu'à 2 jetons Apprentissage en 6.1 avant les Bugs (épargne Bug et crée égalité)."""
    state = _make_state(("R2", "A"), ("SLOT_BUG_CERVEAU", "B"), peuples=("H", "E", "I", "M"))
    # Piste : [T1, T2, T3, T4, T5, R2]
    for idx in range(5):
        state.set_tactique_at_rank(idx, idx + 1)
    _setup_reve_opening_3_2(state, 2, 5, reader_seat=1)
    step_until_decision(state)
    assert state.find_tactique_rank(TILE_R_BASE + 2) == 4

    # Passer à 6.1 du même tour : T1 (idx 0)=2, T2 (idx 1)=1 + 1 Bug en case 2, T3 (idx 2)=1
    state._continuation.clear()
    state.set_apprentissage_at_rank(0, 2)
    state.set_apprentissage_at_rank(1, 1)
    state.set_apprentissage_at_rank(2, 1)
    state.set_bugs_at_case(2, 1)  # Case 2 = idx 1 (T2)

    state.step = STEP_6_1_APPRENTISSAGE
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decision_type == DEC_RETRAIT_APPRENTISSAGE_6_1
    assert req1.decideur == 1  # Entités Magiques
    assert req1.options == ("PASSER", 0, 1, 2)

    # 1er retrait sur T2 (idx 1) : tombe à 0 AVANT les Bugs -> le Bug en case 2 sera épargné !
    apply_choice(state, 1)
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    assert req2.options == ("PASSER", 0, 2)

    # 2e retrait sur T1 (idx 0) : tombe de 2 à 1 -> égalité 1-1 avec T3 (idx 2) !
    apply_choice(state, 0)
    assert state.get_apprentissage_at_rank(0) == 1
    assert state.get_apprentissage_at_rank(1) == 0
    assert state.get_apprentissage_at_rank(2) == 1

    # Exécuter la fin de 6.1 (Bugs) + 6.2 (Évolution) : égalité en tête -> aucun avancement Tactique et Bug préservé !
    before_t = tuple(state.get_tactique_at_rank(i) for i in range(TRACK_LEN))
    step_until_decision(state)
    after_t = tuple(state.get_tactique_at_rank(i) for i in range(TRACK_LEN))
    assert state.get_bugs_at_case(2) == 1
    assert after_t == before_t


def test_r2_b_temoin_parade_totale_vs_route_forestiere_6_1() -> None:
    """Témoin R2:B : machine 100 % parée -> 0 Apprentissage (même avec gain rouge) ; Route Forestière != parée."""
    state = _make_state(("R2", "B"))
    for idx in range(5):
        state.set_tactique_at_rank(idx, idx + 1)
    state.set_tactique_at_rank(5, TILE_R_BASE + 2)

    # Machine A : Abatteuse rayon 0 liée à T5 (SUR_PLACE + DEVANT, gain_rouge=1), 100 % parée en (0, 1) et (0, 2)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    state.set_parcel_piege(0, 1, PIEGE_ACTIF)
    state.set_parcel_defenseurs(0, 1, 1)
    state.set_parcel_piege(0, 2, PIEGE_ACTIF)
    state.set_parcel_defenseurs(0, 2, 1)
    state.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 6, 5, 5)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[5])
    assert state.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)

    # Machine B : Abatteuse rayon 1 liée à T4 (cible SUR_PLACE, gain_rouge=1), posée sur une Route Forestière (1, 1) !
    state.set_parcel_arbres_souches(1, 1, 0, 0)
    assert state.is_route_forestiere(1, 1)
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    state.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 4, 6, 4, 4)
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert state.get_machine_tokens(1, MACHINE_ABATTEUSE) == (1, 0)

    # Exécuter _run_step_6_1 : T5 (idx 4) reçoit 0 jeton, tandis que T4 (idx 3) reçoit +1 jeton !
    state.step = STEP_6_1_APPRENTISSAGE
    _run_step_6_1(state)
    assert state.step == STEP_6_2_EVOLUTION
    assert state.get_apprentissage_at_rank(4) == 0  # T5 annulé par R2:B
    assert state.get_apprentissage_at_rank(3) == 1  # T4 sur Route Forestière NON parée -> +1 !


def test_r3_a_temoin_recyclage_batisseurs_lisiere_en_3_2() -> None:
    """Témoin R3:A : recycle en 3.2 jusqu'à 2 Défenseurs (dont des bâtisseurs restés en lisière) vers la Forêt."""
    state = _make_state(("R3", "A"), peuples=("H", "M", "R", "E"))
    state.place_defender_lisiere_tile(0, 0, 0, FACE_DEFINITIF)
    state.place_defender_lisiere_tile(1, 0, 0, FACE_DEFINITIF)
    state.set_lisiere_tile_state(0, LISIERE_CONSTRUCTED, 2)

    _setup_reve_opening_3_2(state, 3, 5, reader_seat=0)
    req1 = step_until_decision(state)
    assert isinstance(req1, DecisionRequest)
    assert req1.decideur == 0  # Humains
    assert "PASSER" in req1.options
    move_1 = (("LISIERE", 0, 0), (1, 2))
    assert move_1 in req1.options

    apply_choice(state, move_1)
    req2 = step_until_decision(state)
    assert isinstance(req2, DecisionRequest)
    move_2 = (("LISIERE", 0, 0), (2, 3))
    assert move_2 in req2.options

    apply_choice(state, move_2)
    step_until_decision(state)

    assert state.step == STEP_4_3_MIGRATION
    assert state.get_lisiere_tile_state(0) == (LISIERE_CONSTRUCTED, 0)
    assert state.get_parcel_defenseurs(1, 2) == 1
    assert state.get_parcel_defenseurs(2, 3) == 1


def test_r3_b_temoin_liberation_batisseurs_n4_et_n3_des_construction() -> None:
    """Témoin R3:B : prend effet dès la construction de R3:B (1 bâtisseur à N=4, tous par propriétaire à N=3)."""
    # 1. Table à N=4 joueurs : H (siège 0) et M (siège 1) construisent R3:B sur leur lisière
    state_n4 = _make_state(("R3", "B"), peuples=("H", "M", "R", "E"))
    _add_step_4_3_stop_anchor(state_n4)
    r3_slot_n4 = state_n4.find_lisiere_slot_by_tile_id("R3")
    assert r3_slot_n4 is not None
    state_n4.place_defender_lisiere_tile(0, 0, r3_slot_n4, FACE_DEFINITIF)
    state_n4.place_defender_lisiere_tile(1, 0, r3_slot_n4, FACE_DEFINITIF)

    state_n4.step = STEP_3_1_CONSTRUCT
    req_n4 = step_until_decision(state_n4)
    assert isinstance(req_n4, DecisionRequest)
    assert req_n4.decision_type == DEC_LIBERATION_BATISSEUR_3_1
    assert req_n4.decideur == 0  # Humains (peuple_origine de R3)
    assert (1, 0, 1, 1) in req_n4.options

    apply_choice(state_n4, (1, 0, 1, 1))
    step_until_decision(state_n4)
    assert state_n4.step == STEP_4_3_MIGRATION
    assert state_n4.get_lisiere_tile_state(r3_slot_n4) == (LISIERE_CONSTRUCTED, 1)
    assert state_n4.get_parcel_defenseurs(1, 1) == 1

    # 2. Table à N=3 joueurs : tous les bâtisseurs présents sont libérés, chacun choisissant sa rive !
    state_n3 = _make_state(("R3", "B"), peuples=("H", "M", "R"))
    _add_step_4_3_stop_anchor(state_n3)
    r3_slot_n3 = state_n3.find_lisiere_slot_by_tile_id("R3")
    assert r3_slot_n3 is not None
    state_n3.place_defender_lisiere_tile(0, 0, r3_slot_n3, FACE_DEFINITIF)
    state_n3.place_defender_lisiere_tile(1, 0, r3_slot_n3, FACE_DEFINITIF)

    state_n3.step = STEP_3_1_CONSTRUCT
    req_b0 = step_until_decision(state_n3)
    assert isinstance(req_b0, DecisionRequest)
    assert req_b0.decision_type == DEC_LIBERATION_BATISSEUR_3_1
    assert req_b0.decideur == 0
    apply_choice(state_n3, (0, 0, 0, 1))

    req_b1 = step_until_decision(state_n3)
    assert isinstance(req_b1, DecisionRequest)
    assert req_b1.decision_type == DEC_LIBERATION_BATISSEUR_3_1
    assert req_b1.decideur == 1
    apply_choice(state_n3, (1, 0, 1, 1))

    step_until_decision(state_n3)
    assert state_n3.step == STEP_4_3_MIGRATION
    assert state_n3.get_lisiere_tile_state(r3_slot_n3) == (LISIERE_CONSTRUCTED, 0)
    assert state_n3.get_parcel_defenseurs(0, 1) == 1
    assert state_n3.get_parcel_defenseurs(1, 1) == 1


def test_r4_a_temoin_pierre_serpent_surchauffe_reduit_seuil_de_2() -> None:
    """Témoin R4:A : retourne 1 Rouge en Bleu Surchauffe en 3.2, réduisant de 2 le seuil brut dès ce tour."""
    state = _make_state(("R4", "A"))
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)
    state.set_machine_tokens(1, MACHINE_BULLDOZER, 2, 0)
    state.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    state.set_machine_tokens(2, MACHINE_ABATTEUSE, 1, 0)

    seuil_before = compute_parade_seuil(state, 1, MACHINE_BULLDOZER, 2, TACTIQUES_SPEC[1])

    _setup_reve_opening_3_2(state, 4, 5, reader_seat=0)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 0  # Humains
    assert set(req.options) == {(1, MACHINE_BULLDOZER), (2, MACHINE_ABATTEUSE)}

    apply_choice(state, (1, MACHINE_BULLDOZER))
    step_until_decision(state)

    assert state.get_machine_tokens(1, MACHINE_BULLDOZER) == (1, 1)
    seuil_after = compute_parade_seuil(state, 1, MACHINE_BULLDOZER, 2, TACTIQUES_SPEC[1])
    assert seuil_before - seuil_after == 2


def test_r4_b_temoin_sabotage_revele_prolifere_sans_case_3() -> None:
    """Témoin R4:B : +1 carte Sabotage max/tour (sans allumer case 3) si présence furtive + Sabotage révélé en 3.2."""
    state = _make_state(("R4", "B"))
    state.set_tactique_at_rank(5, TILE_R_BASE + 4)
    _add_step_4_3_stop_anchor(state)

    # Cas 1 : Sabotage révélé MAIS aucun Défenseur en Furtivité -> aucun ajout
    clone_no_furt = state.clone()
    clone_no_furt.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    clone_no_furt.step = STEP_3_2_REVEAL
    step_until_decision(clone_no_furt)
    assert clone_no_furt.step == STEP_4_3_MIGRATION
    assert clone_no_furt.sabotage_pending_count == 0

    # Cas 2 : 1 Défenseur en Furtivité ET 2 cartes Sabotage révélées -> +1 seule carte bonus, case 3 éteinte !
    state.enter_furtivite(0, 0, 0, 2, 0, FACE_DEFINITIF)
    state.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    state.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    state.step = STEP_3_2_REVEAL
    step_until_decision(state)

    assert state.step == STEP_4_3_MIGRATION
    assert state.sabotage_pending_count == 1
    assert not state.is_trigger_lit(3)


def test_r4_c_temoin_seconde_rive_piege_face_route_hr() -> None:
    """Témoin R4:C : face à une Route Forestière sur la lisière H-R, pose 1 Piège sur l'autre rive (allume 2)."""
    state = _make_state(("R4", "C"), peuples=("H", "R", "E", "M"))
    # Route Forestière sur Reptiles (1, 2) ; en face chez Humains (0, 2) : seulement des Souches + 1 machine présente !
    state.set_parcel_arbres_souches(1, 2, 0, 0)
    assert state.is_route_forestiere(1, 2)
    state.set_parcel_arbres_souches(0, 2, 0, 2)
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)

    _setup_reve_opening_3_2(state, 4, 5, reader_seat=0)
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert req.decideur == 0  # Humains
    assert req.options == ("PASSER", (0, 2))

    apply_choice(state, (0, 2))
    assert state.is_trigger_lit(2)
    step_until_decision(state)

    assert state.step == STEP_4_3_MIGRATION
    assert state.get_parcel_piege(0, 2) == PIEGE_ACTIF


def test_r4_d_temoin_guetteur_pierre_groupe_atomique_avant_cascade_case_2() -> None:
    """Témoin R4:D : déplace 1 Défenseur furtif + pose 1 Piège en groupe atomique avant les cascades de la case 2."""
    observed_at_cascade: list[tuple[int, int]] = []

    def _spy_g1(st: GameState, _hk: str, _cx: dict[str, object]) -> None:
        observed_at_cascade.append((st.get_parcel_piege(1, 2), st.get_parcel_defenseurs(1, 2)))

    try:
        load_all_effects()
        register_tile("G1", "Z_SPY_R4D", hooks=(HOOK_GARDIEN_OUVERTURE,))(_spy_g1)

        cfg = GameConfig(
            n_players=4,
            mode=3,
            peuples=("H", "R", "E", "M"),
            tile_profiles=(("R4", "D"), ("G1", "Z_SPY_R4D")),
        )
        state = GameState(cfg)
        state.set_gardien_at_case(2, 1, 1, False)
        state.enter_furtivite(0, 0, 0, 2, 0, FACE_DEFINITIF)
        assert state.get_parcel_piege(1, 2) == PIEGE_AUCUN
        assert state.get_parcel_defenseurs(1, 2) == 0

        _setup_reve_opening_3_2(state, 4, 5, reader_seat=0)
        req = step_until_decision(state)
        assert isinstance(req, DecisionRequest)
        assert req.decideur == 0  # Humains
        assert "PASSER" in req.options
        assert (0, 2, 0) in req.options
        assert (0, 2, 1) in req.options

        apply_choice(state, (0, 2, 1))
        assert state.is_trigger_lit(2)
        step_until_decision(state)

        assert state.step == STEP_4_3_MIGRATION
        assert state.get_furtivite_total_defs(0, 2) == 0
        assert state.get_parcel_piege(1, 2) == PIEGE_ACTIF
        assert state.get_parcel_defenseurs(1, 2) == 1
        assert observed_at_cascade == [(PIEGE_ACTIF, 1)]
    finally:
        clear_tile_registry()
        load_all_effects()
