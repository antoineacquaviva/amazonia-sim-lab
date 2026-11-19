"""Harnais de conformité v5.3 du noyau déterministe scellé (Modes 1 & 2, 128 châssis)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from bots.bot_b0 import choose_b0, play_game_b0
from campaigns.worker_main import build_palier1_cells, run_campaign_palier1
from engine.core_engine import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    DEC_COLONIE_A_OPEN,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_POSE_DEFENSEUR_2,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    compute_parade_seuil,
    insert_reve_on_track,
    list_legal_targets,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import (
    ALL_PRIMITIVES,
    DecisionRequest,
    GameOver,
    prim_creation_entite,
    prim_mod_seuil,
)
from engine.rng import (
    SRC_DICE,
    SRC_MACHINE_SHUFFLE,
    rand_u64,
    roll_d6,
    shuffle_deterministic,
)
from engine.state import (
    BUF_CAPACITY,
    CARD_SABOTAGE,
    DECK_SLOTS_CAPACITY,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MIN_FREE_RESERVE_BYTES,
    PEUPLE_TO_ID,
    PFLAG_AUTO_PARADE_ONCE,
    PFLAG_MATAMATA_MARK,
    PFLAG_SANCTUAIRE_SOUCHE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    STATE_BUF_SIZE,
    STEP_1_2_DEAL,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    STEP_6_1_APPRENTISSAGE,
    STEP_GAME_OVER,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    code_to_tile_id,
    get_layout_report,
    machine_card_code,
)


# ---------------------------------------------------------------------------
# Test 1 : Clone indépendant à l'octet près et budget mémoire 384B (>= 32B libres)
# ---------------------------------------------------------------------------
def test_01_clone_byte_independence_and_memory_budget() -> None:
    report = get_layout_report()
    assert report["capacity_bytes"] == STATE_BUF_SIZE == BUF_CAPACITY == 384
    assert DECK_SLOTS_CAPACITY == 64
    assert report["free_bytes"] >= MIN_FREE_RESERVE_BYTES == 32
    assert 0 < report["used_bytes"] <= 384 - 32

    cfg = GameConfig(n_players=6, mode=2, exp_seed=101, rep_id=7)
    s1 = GameState(cfg)
    req = step_until_decision(s1)
    assert isinstance(req, DecisionRequest)

    snap_before = s1.raw_used_bytes()
    s2 = s1.clone()
    assert s2.raw_used_bytes() == snap_before
    assert s2._buf is not s1._buf
    assert s2._continuation is not s1._continuation

    # Muter profondément le clone ne doit modifier aucun octet de l'original
    apply_choice(s2, req.options[0])
    s2.set_parcel_insectes(0, 1, 9)
    s2.set_machine_tokens(1, MACHINE_ABATTEUSE, 3, 2)
    s2.add_permanent_sabotage(2, light_case_3=True)

    assert s1.raw_used_bytes() == snap_before
    assert s2.raw_used_bytes() != snap_before


# ---------------------------------------------------------------------------
# Test 2 : Isolation stricte de get_observation() sous paravent fermé vs ouvert
# ---------------------------------------------------------------------------
def test_02_observation_strict_isolation_paravents() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=2026, rep_id=1)
    state = GameState(cfg)

    # Avancer jusqu'à 2.1 : cartes distribuées et dés lancés sous paravent fermé
    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)
    assert state.paravents_ouverts is False

    obs0 = state.get_observation(0)
    assert not hasattr(obs0, "_buf")
    assert not hasattr(obs0, "deck_cards")
    assert obs0.paravents_ouverts is False

    # Le siège 0 voit sa propre main/dés, mais toutes les autres mains sont masquées
    assert obs0.hands[0].card is not None
    assert obs0.hands[0].d1 is not None
    assert obs0.hands[0].lecture_m is not None
    for other_seat in (1, 2, 3):
        assert obs0.hands[other_seat].has_card is True
        assert obs0.hands[other_seat].card is None
        assert obs0.hands[other_seat].d1 is None
        assert obs0.hands[other_seat].d2 is None
        assert obs0.hands[other_seat].lecture_m is None
        assert obs0.hands[other_seat].bound_tactique is None

    # Placer 1 Insecte sur la roue pour suspendre le moteur en 4.3 du Tour 1 (après 3.2, avant 6.2)
    state.set_parcel_insectes(0, 1, 1)

    # Aller jusqu'après l'ouverture des paravents en 3.2 (arrêt en 4.3 du Tour 1)
    while not state.paravents_ouverts:
        r = step_until_decision(state)
        assert isinstance(r, DecisionRequest)
        if state.paravents_ouverts:
            break
        apply_choice(state, r.options[0])

    assert state.tour == 1
    assert state.paravents_ouverts is True
    obs0_open = state.get_observation(0)
    assert obs0_open.paravents_ouverts is True
    for s in range(4):
        assert obs0_open.hands[s].card is not None
        assert obs0_open.hands[s].d1 is not None


# ---------------------------------------------------------------------------
# Test 3 : Indépendance CRN totale entre dilution Sabotage et jets de dés
# ---------------------------------------------------------------------------
def test_03_crn_independence_sabotage_vs_future_dice() -> None:
    cfg = GameConfig(n_players=4, mode=1, exp_seed=99999, rep_id=42)
    s_clean = GameState(cfg)
    s_diluted = GameState(cfg)

    # Ajouter 5 cartes Sabotage uniquement dans la branche diluée et remélanger (6.3)
    s_diluted.add_permanent_sabotage(5, light_case_3=False)
    s_diluted.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
    s_clean.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)

    assert s_diluted.deck_len == s_clean.deck_len + 5

    # Pour tous les tours futurs 2..8 et tous les peuples, les jets 2D6 adressés par compteur
    # doivent rester bit-à-bit identiques quelle que soit l'histoire des mélanges Sabotage
    for tour in range(2, 9):
        for p_code in cfg.peuples:
            pid = PEUPLE_TO_ID[p_code]
            d1_a = roll_d6(s_clean.cfg.exp_seed, s_clean.cfg.rep_id, SRC_DICE, tour, pid, 0)
            d2_a = roll_d6(s_clean.cfg.exp_seed, s_clean.cfg.rep_id, SRC_DICE, tour, pid, 1)
            d1_b = roll_d6(s_diluted.cfg.exp_seed, s_diluted.cfg.rep_id, SRC_DICE, tour, pid, 0)
            d2_b = roll_d6(s_diluted.cfg.exp_seed, s_diluted.cfg.rep_id, SRC_DICE, tour, pid, 1)
            assert (d1_a, d2_a) == (d1_b, d2_b)

    # Vérifier aussi le déterminisme pur de shuffle_deterministic et rand_u64
    deck_a = shuffle_deterministic([1, 2, 3, 4, 13, 13], 77, 3, SRC_MACHINE_SHUFFLE, 2, 0)
    deck_b = shuffle_deterministic([1, 2, 3, 4, 13, 13], 77, 3, SRC_MACHINE_SHUFFLE, 2, 0)
    assert deck_a == deck_b
    assert rand_u64(77, 3, SRC_DICE, 4, 2, 0) != rand_u64(77, 3, SRC_DICE, 4, 2, 1)


# ---------------------------------------------------------------------------
# Test 4 : Sabotage par dilution permanente (Étape 1 = 0 dé lancé, 0 activation)
# ---------------------------------------------------------------------------
def test_04_sabotage_drawn_in_step1_rolls_zero_dice_and_loses_activation() -> None:
    cfg = GameConfig(n_players=3, mode=1, exp_seed=1234, rep_id=0)
    state = GameState(cfg)

    # Forcer un paquet contenant uniquement des cartes Sabotage sauf 1 carte Machine
    m_card = machine_card_code(0, MACHINE_ABATTEUSE)
    state._store_deck_cards([CARD_SABOTAGE, m_card, CARD_SABOTAGE])
    state.step = STEP_1_2_DEAL

    req = step_until_decision(state)
    assert isinstance(req, DecisionRequest)

    sabotage_seats = 0
    machine_seats = 0
    for s in range(3):
        card, d1, d2, lec_m, bound_t = state.get_player_hand(s)
        if card == CARD_SABOTAGE:
            sabotage_seats += 1
            assert (d1, d2, lec_m, bound_t) == (0, 0, 0, 0)
        else:
            machine_seats += 1
            assert card == m_card
            assert 1 <= d1 <= 6 and 1 <= d2 <= 6
            assert lec_m == min(d1, d2)

    assert sabotage_seats == 2
    assert machine_seats == 1


# ---------------------------------------------------------------------------
# Test 5 : Furtivité à 4 emplacements jumeaux (tirage à l'entrée vs flip sur place)
# ---------------------------------------------------------------------------
def test_05_furtivite_4_twin_slots_pull_vs_in_place_flip() -> None:
    cfg = GameConfig(n_players=4, mode=1, exp_seed=55)
    state = GameState(cfg)

    # Siège 0 pose son 1er Défenseur sur lisière 0, p=2, rive 0 (slot 0, face définitif)
    state.enter_furtivite(seat=0, def_idx=0, lisiere=0, p=2, rive=0, face=FACE_DEFINITIF)
    assert state.get_furtivite_slots(0, 2) == (FACE_DEFINITIF, 0, 0, 0)
    assert state.get_furtivite_nb_def_rive(0, 2, 0) == 1
    assert state.get_furtivite_nb_def_rive(0, 2, 1) == 0

    # Siège 1 ENTRE avec son 2e Défenseur sur la rive 1 en face réflexion :
    # le pion du siège 0 doit être tiré automatiquement sur le jumeau de la rive 1 (slot 3) !
    state.enter_furtivite(seat=1, def_idx=1, lisiere=0, p=2, rive=1, face=FACE_REFLEXION)
    assert state.get_furtivite_slots(0, 2) == (0, 0, FACE_REFLEXION, FACE_DEFINITIF)
    assert state.get_furtivite_nb_def_rive(0, 2, 0) == 0
    assert state.get_furtivite_nb_def_rive(0, 2, 1) == 2

    # Retourner réflexion -> définitif sur place ne déplace ni ne tire aucun pion
    state.flip_defender2_to_definitif_in_place(seat=1)
    assert state.get_furtivite_slots(0, 2) == (0, 0, FACE_DEFINITIF, FACE_DEFINITIF)
    assert state.is_player_def2_definitif(1) is True

    # Case pleine (2 Défenseurs) : interdite à un 3e Défenseur d'un autre joueur
    legal_s2 = list_legal_targets(state, seat=2, is_first_defender=False)
    assert ("FURTIVITE", 0, 2, 0) not in legal_s2
    assert ("FURTIVITE", 0, 2, 1) not in legal_s2


# ---------------------------------------------------------------------------
# Test 6 : Saut des Routes sur un rayon vs blocage latéral Furtivité
# ---------------------------------------------------------------------------
def test_06_route_bridge_radial_jump_and_lateral_blocking() -> None:
    cfg = GameConfig(n_players=4, mode=1, exp_seed=66)
    state = GameState(cfg)

    # Transformer (rayon=0, p=2) en Route Forestière (0 Arbre, 0 Souche)
    state.set_parcel_arbres_souches(0, 2, 0, 0)
    assert state.is_route_forestiere(0, 2) is True

    # Radialement : depuis p=1, viser DEVANT ou avancer saute p=2 et cible p=3 !
    assert state.next_non_razed_towards_heart(0, 1) == 3
    assert state.next_non_razed_towards_border(0, 3) == 1

    # Vérifier la frappe T3 (SUR_PLACE + DEVANT + avancée 1) d'une Abatteuse en p=1
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    arbres_p3_before = state.get_parcel_arbres(0, 3)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert state.get_parcel_arbres(0, 3) == arbres_p3_before - 2
    pos_after, _, _ = state.get_machine_pos_status(0, MACHINE_ABATTEUSE)
    assert pos_after == 3  # A sauté la Route en p=2 !

    # Latéralement : rive 0 de lisière 0 à p=2 fait face à la Route (0, 2) -> interdite !
    # Tandis que la rive 1 de lisière 0 à p=2 fait face à (1, 2) intacte -> autorisée !
    legal_0 = list_legal_targets(state, seat=0, is_first_defender=True)
    assert ("FORET", 0, 2) not in legal_0
    assert ("FURTIVITE", 0, 2, 0) not in legal_0
    assert ("FURTIVITE", 0, 2, 1) in legal_0
    assert ("LISIERE", 0) not in legal_0  # Mode 1 : G/R/M interdit


# ---------------------------------------------------------------------------
# Test 7 : Chaîne Piège Embuscade (Déf >= 1 vs 0) puis Parade classique immédiate
# ---------------------------------------------------------------------------
def test_07_trap_ambush_vs_inert_and_classic_parade_immediate_discard() -> None:
    cfg = GameConfig(n_players=4, mode=1, exp_seed=77)
    state = GameState(cfg)

    # Cas A : Piège INERTE si Défense == 0 -> l'Abatteuse T1 coupe 2 Arbres et le Piège ne pare pas
    state.set_parcel_piege(0, 1, PIEGE_ACTIF)
    state.set_parcel_defenseurs(0, 1, 0)
    state.set_parcel_insectes(0, 1, 0)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(0, 1) == 0
    assert state.get_parcel_souches(0, 1) == 2
    assert state.get_parcel_piege(0, 1) == PIEGE_ACTIF  # Non déclenché !

    # Cas B : Piège ARMÉ sur (1, 3) avec 0 Défenseur mais 1 Insecte (Défense totale = 1 >= 1)
    # Machine avec 3 jetons rouges (Seuil = 3 + 3 = 6), mais Embuscade pare sans défausser l'Insecte !
    state.set_machine_pos_status(1, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(1, MACHINE_ABATTEUSE, 3, 0)
    state.set_parcel_piege(1, 3, PIEGE_ACTIF)
    state.set_parcel_insectes(1, 3, 1)
    resolve_single_machine_attack(state, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(1, 3) == 3  # Intact !
    assert state.get_parcel_insectes(1, 3) == 1  # Épargné par l'Embuscade !
    assert state.get_parcel_piege(1, 3) == PIEGE_DECLENCHE

    # Cas C : Parade classique sans Piège sur (2, 3) [Seuil imprimé = 3, +1 Rouge -> Seuil = 4]
    # 1 Défenseur + 5 Insectes -> pare en défaussant immédiatement (4 - 1) = 3 Insectes !
    state.set_machine_pos_status(2, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    state.set_machine_tokens(2, MACHINE_BULLDOZER, 1, 0)
    state.set_parcel_defenseurs(2, 3, 1)
    state.set_parcel_insectes(2, 3, 5)
    resolve_single_machine_attack(state, 2, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(2, 3) == 3
    assert state.get_parcel_insectes(2, 3) == 2  # 5 - 3 = 2 Insectes restants et libres


# ---------------------------------------------------------------------------
# Test 8 : Création d'une Route Forestière (0/0) et repli des machines (A09)
# ---------------------------------------------------------------------------
def test_08_route_creation_and_machine_retreat_rules() -> None:
    cfg = GameConfig(n_players=3, mode=1, exp_seed=88)
    state = GameState(cfg)

    # 1) Parcelle p=2 avec 1 Arbre et 1 Souche ; Abatteuse et Bulldozer toutes deux en p=2
    state.set_parcel_arbres_souches(0, 2, 1, 1)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    state.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)

    # Le Bulldozer T1 coupe l'Arbre restant puis terrasse les 2 Souches -> 0/0 Route !
    # Les deux machines doivent reculer vers p=1 (côté bordure par défaut)
    resolve_single_machine_attack(state, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.is_route_forestiere(0, 2) is True
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 1
    assert state.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 1

    # 2) Si p=1 tombe aussi à 0/0 (bordure toute rasée), repli vers p=3 côté cœur !
    state.set_parcel_arbres_souches(0, 1, 1, 0)
    resolve_single_machine_attack(state, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.is_route_forestiere(0, 1) is True
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 3
    assert state.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 3

    # 3) Si p=3 et p=4 sont rasées à leur tour -> retrait définitif des machines (pos=0, RETIRED)
    state.set_parcel_arbres_souches(0, 4, 0, 0)
    state.set_parcel_arbres_souches(0, 3, 0, 2)
    resolve_single_machine_attack(state, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_machine_pos_status(0, MACHINE_BULLDOZER)[:2] == (0, MACHINE_STATUS_RETIRED)
    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[:2] == (0, MACHINE_STATUS_RETIRED)


# ---------------------------------------------------------------------------
# Test 9 : Contact Machine-Nid renvoyant le Nid en lisière reconstructible
# ---------------------------------------------------------------------------
def test_09_machine_nid_contact_returns_nid_reconstructible_and_clears_insects() -> None:
    cfg = GameConfig(n_players=6, mode=2, exp_seed=99)  # Inclut I en siège 5 (M1, M5 présents)
    state = GameState(cfg)

    m1_slot = state.find_lisiere_slot_by_tile_id("M1")
    assert m1_slot is not None
    state.set_lisiere_tile_state(m1_slot, LISIERE_CONSTRUCTED, 0)
    state.set_parcel_nid(0, 2, 1, False)
    state.set_parcel_insectes(0, 2, 4)
    state.set_parcel_defenseurs(0, 2, 2)
    state.set_parcel_piege(0, 2, PIEGE_ACTIF)

    # Abatteuse en p=1 avance en p=2 sur T3 (même si ses frappes sont parées par le Piège !)
    state.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(state, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])

    assert state.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert state.get_parcel_nid(0, 2) == (0, False)
    assert state.get_parcel_insectes(0, 2) == 0  # Insectes défaussés au contact !
    assert state.get_parcel_defenseurs(0, 2) == 2  # Défenseurs préservés !
    assert state.get_parcel_piege(0, 2) in (PIEGE_ACTIF, PIEGE_DECLENCHE)  # Piège préservé !
    assert state.get_lisiere_tile_state(m1_slot) == (LISIERE_UNCONSTRUCTED, 0)  # Reconstructible !


# ---------------------------------------------------------------------------
# Test 10 : Insertion d'un Rêve sur la case libre la plus à droite (piste fixe T1..T6, Bugs fixes)
# ---------------------------------------------------------------------------
def test_10_reve_insertion_partial_slide_and_fixed_bugs() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=1010)
    state = GameState(cfg)

    # Piste initiale artificielle : [T1, R1, T3, T4, R2, R3]
    custom_track = [1, TILE_R_BASE + 1, 3, 4, TILE_R_BASE + 2, TILE_R_BASE + 3]
    for i, c in enumerate(custom_track):
        state.set_tactique_at_rank(i, c)
    # Placer des Bugs sur les cases 4, 5, 6
    state.set_bugs_at_case(4, 2)
    state.set_bugs_at_case(5, 1)
    state.set_bugs_at_case(6, 3)

    # Insérer R4 : case libre la plus à droite = case 4 (index 3), aucune Tactique éjectée ni glissée !
    ejected = insert_reve_on_track(state, 4)
    assert ejected is None
    resulting_ids = [code_to_tile_id(state.get_tactique_at_rank(i)) for i in range(6)]
    assert resulting_ids == ["T1", "R1", "T3", "R4", "R2", "R3"]

    # Les Insectes Bug sont restés strictement fixes sur les numéros d'emplacement 4, 5, 6
    assert state.get_bugs_at_case(4) == 2
    assert state.get_bugs_at_case(5) == 1
    assert state.get_bugs_at_case(6) == 3


# ---------------------------------------------------------------------------
# Test 11 : Ratissage v5.4.2 (T1 autonome en 5.2, piste fixe sans Apprentissage)
# ---------------------------------------------------------------------------
def test_11_ratissage_autonomy_when_t1_ejected_vs_learning_when_present() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=1111)

    s_rat = GameState(cfg)
    s_rat.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    s_rat.step = STEP_5_2_RATISSAGE
    track_before = [s_rat.get_tactique_at_rank(i) for i in range(6)]
    _ = step_until_decision(s_rat)

    # L'attaque autonome du Ratissage a bien eu lieu en 5.2 avec +1 puissance imprimée
    assert s_rat.get_parcel_arbres(0, 4) == 1  # 3 - 2 = 1 Arbre
    assert s_rat.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)
    assert s_rat.get_machine_effective_rouges(0, MACHINE_ABATTEUSE) == 1
    # Piste T1..T6 inchangée (aucun Apprentissage ni glissement en Étape 6)
    assert [s_rat.get_tactique_at_rank(i) for i in range(6)] == track_before
    assert all(s_rat.get_apprentissage_at_rank(i) == 0 for i in range(6))


# ---------------------------------------------------------------------------
# Test 12 : Étape 6.1 supprimée (aucune consommation Bug A ni déplacement Tactiques)
# ---------------------------------------------------------------------------
def test_12_bug_a_preserved_at_zero_and_consumed_when_positive() -> None:
    cfg = GameConfig(n_players=6, mode=2, exp_seed=1212)
    assert cfg.profile_for_slot("SLOT_BUG_CERVEAU") == "B"
    state = GameState(cfg)

    state.set_bugs_at_case(1, 2)
    state.set_bugs_at_case(2, 1)

    m_card = machine_card_code(0, MACHINE_ABATTEUSE)
    state.set_player_hand(0, m_card, 2, 5, 2, 2)
    state.set_machine_turn_stats(0, MACHINE_ABATTEUSE, damaged_count=2, gained_red=False, attacked=True)

    state.step = STEP_6_1_APPRENTISSAGE
    _ = step_until_decision(state)

    # Aucun Apprentissage en 6.1 : les Bugs restent intacts pour 3.2 (profil B) et T1..T6 reste fixe !
    assert state.get_bugs_at_case(1) == 2
    assert state.get_bugs_at_case(2) == 1
    assert [code_to_tile_id(state.get_tactique_at_rank(i)) for i in range(6)] == [
        "T1",
        "T2",
        "T3",
        "T4",
        "T5",
        "T6",
    ]


# ---------------------------------------------------------------------------
# Test 13 : Cascades Gardiens à plat 1 -> 6 avec Résonance 4 sans boucle infinie
# ---------------------------------------------------------------------------
def test_13_flat_gardien_cascade_with_resonance_4_no_infinite_loop() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=1313)
    state = GameState(cfg)

    # Placer G1 en case 2, G2 en case 4 (Résonance !) et G5 en case 6, tous disponibles
    state.set_gardien_at_case(2, 1, face=1, used=False)
    state.set_gardien_at_case(4, 2, face=1, used=False)
    state.set_gardien_at_case(6, 5, face=1, used=False)

    # Allumer uniquement la case 2 (Piège) :
    # En 1->6, G1 s'ouvre en case 2 -> allume Résonance 4 -> G2 s'ouvre en case 4 -> rallume 4,
    # mais G2 est déjà marqué utilisé et case 6 n'est pas allumée -> arrêt propre à 2 ouvertures !
    prim_creation_entite(state, "PIEGE", ray=0, p=2, light_trigger=True)
    opened = sweep_gardiens(state)

    assert opened == 2
    assert state.get_gardien_at_case(2)[2] is True
    assert state.get_gardien_at_case(4)[2] is True
    assert state.get_gardien_at_case(6)[2] is False
    assert state.triggers_lit == 0


# ---------------------------------------------------------------------------
# Test 14 : Fin anticipée en 5.3 (Rêve rang 1 et Réveil Gardiens) + Repousse Finale sans Étape 6
# ---------------------------------------------------------------------------
def test_14_early_victory_in_5_3_triggers_final_regrowth_skipping_step_6() -> None:
    # Sous-cas A : Bloc complet de 4 Rêves (H + E = 2 peuples oniriques) en tête au Tour 3
    cfg_reve = GameConfig(n_players=4, mode=2, peuples=("M", "H", "E", "O"), exp_seed=1414)
    s_reve = GameState(cfg_reve)
    s_reve.tour = 3
    for idx, r_num in enumerate((1, 2, 3, 4)):
        s_reve.set_tactique_at_rank(idx, TILE_R_BASE + r_num)  # Bloc [R1..R4] en rangs 0..3
    # Parcelle (0, 1) avec 0 Arbre mais 2 Souches (non rasée) -> doit repousser de +1 Arbre !
    # Parcelle (1, 1) avec 2 Arbres et 1 Souche (plafond dotation=2) -> plafonnée à 2 Arbres !
    s_reve.set_parcel_arbres_souches(0, 1, 0, 2)
    s_reve.set_parcel_arbres_souches(1, 1, 2, 1)
    s_reve.set_parcel_piege(0, 1, PIEGE_DECLENCHE)
    s_reve.step = STEP_5_3_END_CHECK

    res_a = step_until_decision(s_reve)
    assert isinstance(res_a, GameOver)
    assert res_a.tour_fin == 3  # Pas de passage à tour + 1 (Étape 6 sautée) !
    assert res_a.cause_fin == CAUSE_REVE_RANG_1
    assert s_reve.get_parcel_arbres(0, 1) == 1
    assert s_reve.get_parcel_souches(0, 1) == 1
    assert s_reve.get_parcel_arbres(1, 1) == 2  # Plafonné à la dotation initiale !
    assert s_reve.get_parcel_piege(0, 1) == PIEGE_AUCUN  # Piège déclenché retiré avant fin

    # Sous-cas B : Réveil de la Forêt (N=4, >= 1 Animal Sauvage -> Gardien engagé + 0 dommage réel)
    cfg_gard = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=1415)
    s_gard = GameState(cfg_gard)
    assert cfg_gard.reveil_quota == 4
    s_gard.tour = 4
    s_gard.reveil_engaged_gardien = 1
    s_gard.real_damage_this_turn = False
    s_gard.step = STEP_5_3_END_CHECK

    res_b = step_until_decision(s_gard)
    assert isinstance(res_b, GameOver)
    assert res_b.tour_fin == 4
    assert res_b.cause_fin == CAUSE_REVEIL_GARDIENS
    assert s_gard.step == STEP_GAME_OVER


# ---------------------------------------------------------------------------
# Test 15 : Parties complètes Mode 1 & Mode 2 + balayage multi-châssis jusqu'à GameOver
# ---------------------------------------------------------------------------
def _run_minimal_legal_automaton(state: GameState, *, active_mode2_play: bool = False) -> GameOver:
    """Automate déterministe légal minimal pilotant une partie complète jusqu'à GameOver."""
    steps_guard = 0
    while True:
        steps_guard += 1
        assert steps_guard < 5000, "Boucle infinie détectée dans la machine à états"
        out = step_until_decision(state)
        if isinstance(out, GameOver):
            return out

        opts = out.options
        assert len(opts) >= 1
        chosen: Any = opts[0]

        if active_mode2_play:
            # Exercer activement les constructions lisière, Furtivité, révision 2.2 et Migration
            if out.decision_type == "POSE_DEFENSEUR_1":
                lis_opts = [o for o in opts if o[0] == "LISIERE"]
                chosen = lis_opts[0] if lis_opts else opts[0]
            elif out.decision_type == DEC_POSE_DEFENSEUR_2:
                lis_refl = [o for o in opts if o[0] == "POSER_REFLEXION" and o[1][0] == "LISIERE"]
                furt_refl = [o for o in opts if o[0] == "POSER_REFLEXION" and o[1][0] == "FURTIVITE"]
                chosen = lis_refl[0] if lis_refl else (furt_refl[0] if furt_refl else opts[-1])
            elif out.decision_type == DEC_REVISION_DEFENSEUR_2:
                chosen = ("VERROUILLER_DEFINITIF", None)
            elif out.decision_type == DEC_MIGRATION_INSECTE_4_3:
                col_or_bug = [o for o in opts if o[0] in ("COLONIE", "BUG")]
                fwd = [o for o in opts if o[0] == "FORET"]
                chosen = col_or_bug[0] if col_or_bug else (fwd[0] if fwd else opts[0])
            elif out.decision_type == DEC_COLONIE_A_OPEN:
                chosen = "OUVRIR"

        apply_choice(state, chosen)


def test_15_full_game_mode1_and_mode2_and_chassis_sweep() -> None:
    assert len(ALL_PRIMITIVES) == 8

    # Partie complète Mode 1 (Cœur symétrique, 4 joueurs -> fin au Tour 8)
    cfg_m1 = GameConfig(n_players=4, mode=1, exp_seed=20261117, rep_id=0)
    s_m1_a = GameState(cfg_m1)
    s_m1_b = GameState(cfg_m1)
    over_m1_a = _run_minimal_legal_automaton(s_m1_a)
    over_m1_b = _run_minimal_legal_automaton(s_m1_b)

    assert over_m1_a == over_m1_b  # Reproductibilité bit-à-bit
    assert s_m1_a.raw_used_bytes() == s_m1_b.raw_used_bytes()
    assert over_m1_a.tour_fin == 8
    assert over_m1_a.cause_fin == CAUSE_TOUR_8
    assert 0.0 <= over_m1_a.ratio_arbres <= 1.0

    # Partie complète Mode 2 (Asymétrie à vide, N=3 et N=6 avec constructions G/R/M + Migration A/A)
    for n_pl in (3, 6):
        cfg_m2 = GameConfig(n_players=n_pl, mode=2, exp_seed=4242, rep_id=n_pl)
        s_m2 = GameState(cfg_m2)
        over_m2 = _run_minimal_legal_automaton(s_m2, active_mode2_play=True)
        assert 1 <= over_m2.tour_fin <= 8
        assert over_m2.cause_fin in (CAUSE_TOUR_8, CAUSE_REVE_RANG_1, CAUSE_REVEIL_GARDIENS)
        assert 0.0 <= over_m2.ratio_arbres <= 1.0

    # Vérification des 7 axes sur un échantillon couvrant tous les bits des 128 châssis (0..127)
    for chassis_idx in (0, 1, 2, 4, 8, 16, 32, 64, 85, 127):
        cfg_ch = GameConfig.from_chassis_index(chassis_idx, n_players=4, mode=2, exp_seed=700 + chassis_idx)
        over_ch = _run_minimal_legal_automaton(GameState(cfg_ch), active_mode2_play=True)
        assert 1 <= over_ch.tour_fin <= 8


# ---------------------------------------------------------------------------
# Test 16 : Hygiène d'encodage UTF-8 sans BOM et fins de ligne LF sur le noyau
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "rel_path",
    [
        "engine/rng.py",
        "engine/state.py",
        "engine/primitives.py",
        "engine/core_engine.py",
        "engine/effects/registry.py",
        "engine/effects/lot_01.py",
        "engine/telemetry.py",
        "bots/bot_b0.py",
        "bots/belief_and_ticks.py",
        "bots/heuristic_engine.py",
        "campaigns/designs.py",
        "campaigns/worker_main.py",
        "contracts/core_state_api.md",
        "contracts/kernel_locks.sha256",
        "data/digest_palier2_coeur_muet.json",
        "scripts_cloud/export_api_doc.py",
        "scripts_cloud/fuzz_invariants.py",
        "scripts_cloud/run_palier1_cloud.py",
        "scripts_cloud/run_palier2_cloud.py",
        "scripts_cloud/studio_paths.py",
        "scripts_cloud/sync_studio.py",
        "scripts_cloud/build_spec_bundle.py",
        "USAGE.md",
        ".agents/skills/sync-evolution/SKILL.md",
        ".agents/skills/run-campaign/SKILL.md",
        "tests/test_kernel_invariants.py",
        "tests/temoins/test_lot_01.py",
        "tests/test_palier2_bots_telemetry_designs.py",
    ],
)
def test_16_utf8_no_bom_and_lf_line_endings(rel_path: str) -> None:
    root = Path(__file__).resolve().parent.parent
    raw = (root / rel_path).read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf"), f"BOM UTF-8 interdit dans {rel_path}"
    assert b"\r\n" not in raw, f"CRLF interdit dans {rel_path} (LF requis)"
    raw.decode("utf-8")


# ---------------------------------------------------------------------------
# Test 17 : Modificateurs transitoires 384B (Seuil parcelle, Flags, 1/tour, 6.1) + RAZ 6.2
# ---------------------------------------------------------------------------
def test_17_transient_modifiers_384b_and_6_2_reset() -> None:
    cfg = GameConfig(n_players=6, mode=2, exp_seed=1717)
    state = GameState(cfg)

    # Support de forte dilution (ex: 30 Sabotages + 12 Machines = 42 cartes <= 64 slots)
    state.add_permanent_sabotage(30, light_case_3=False)
    state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
    assert state.deck_len == 42

    # Seuil par parcelle + Matamata + Sanctuaire Souche + Auto-Parade + verrous 1/tour
    prim_mod_seuil(state, -1, ray=0, p=3)
    state.set_parcel_flag_turn(0, 3, PFLAG_MATAMATA_MARK, True)
    state.set_parcel_arbres_souches(0, 3, 2, 1)  # 1 Souche présente -> Matamata -1 actif !
    assert compute_parade_seuil(state, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1]) == 1

    # Sanctuaire Souche : un Bulldozer non paré laisse 1 Souche au lieu de créer une Route 0/0
    state.set_parcel_arbres_souches(1, 2, 0, 2)
    state.set_parcel_flag_turn(1, 2, PFLAG_SANCTUAIRE_SOUCHE, True)
    state.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(state, 1, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert state.get_parcel_souches(1, 2) == 1
    assert not state.is_route_forestiere(1, 2)

    # Auto-Parade once (ex: G11 A Face 2) avec >= 2 Défenseurs
    state.set_parcel_defenseurs(2, 1, 2)
    state.set_parcel_flag_turn(2, 1, PFLAG_AUTO_PARADE_ONCE, True)
    state.set_machine_tokens(2, MACHINE_ABATTEUSE, 5, 0)
    resolve_single_machine_attack(state, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert state.get_parcel_arbres(2, 1) == 2
    assert not state.has_parcel_flag_turn(2, 1, PFLAG_AUTO_PARADE_ONCE)

    # Verrou 1/tour par slot + retrait volontaire mémorisé en 6.1 AVANT Bug A
    assert not state.has_slot_used_once_per_turn("G3")
    state.mark_slot_used_once_per_turn("G3")
    assert state.has_slot_used_once_per_turn("G3")

    state.set_bugs_at_case(1, 1)  # 1 Bug sur rang 1 (T1)
    state.step = STEP_6_1_APPRENTISSAGE
    _ = step_until_decision(state)

    # Le Bug en case 1 reste en place (Apprentissage 6.1 supprimé) et tous les modificateurs transitoires sont RAZ en 6.2 :
    assert state.get_bugs_at_case(1) == 1
    assert not state.has_slot_used_once_per_turn("G3")
    assert state.get_parcel_seuil_mod_turn(0, 3) == 0
    assert state.get_parcel_flags_turn(1, 2) == 0


# ---------------------------------------------------------------------------
# Test 18 : Bot B0 — Isolation stricte vis-à-vis de la main cachée d'un voisin
# ---------------------------------------------------------------------------
def test_18_bot_b0_strict_hidden_hand_isolation_and_gameplay() -> None:
    cfg = GameConfig(n_players=4, mode=2, exp_seed=1818, rep_id=5)
    s_a = GameState(cfg)
    req_a = step_until_decision(s_a)
    assert isinstance(req_a, DecisionRequest)
    assert not s_a.paravents_ouverts

    s_b = s_a.clone()
    decideur = req_a.decideur
    neighbor = (decideur + 1) % cfg.n_players

    # Modifier radicalement la main cachée et les dés du voisin dans s_b
    s_a.set_player_hand(neighbor, CARD_SABOTAGE, 0, 0, 0, 0)
    s_b.set_player_hand(neighbor, machine_card_code(decideur, MACHINE_BULLDOZER), 6, 6, 6, 0)

    req_b = step_until_decision(s_b)
    assert isinstance(req_b, DecisionRequest)

    # B0 doit produire exactement la même décision (zéro fuite d'information privée adverse)
    assert s_a.get_observation(decideur) == s_b.get_observation(decideur)
    assert choose_b0(s_a, req_a) == choose_b0(s_b, req_b)

    # Partie complète B0 en Mode 1 et Mode 2
    over_1 = play_game_b0(GameState(GameConfig(n_players=4, mode=1, exp_seed=3001)))
    over_2 = play_game_b0(GameState(GameConfig(n_players=5, mode=2, exp_seed=3002)))
    assert over_1.tour_fin == 8
    assert 1 <= over_2.tour_fin <= 8


# ---------------------------------------------------------------------------
# Test 19 : Plan expérimental Palier 1 (100k parties exactes & génération shard local)
# ---------------------------------------------------------------------------
def test_19_palier1_worker_grid_and_local_shard(tmp_path: Path) -> None:
    cells = build_palier1_cells(total_games=100_000)
    assert sum(c[7] for c in cells) == 100_000
    assert sum(c[7] for c in cells if c[0] == 1) == 50_000
    assert sum(c[7] for c in cells if c[0] == 2) == 50_000

    rc = run_campaign_palier1(
        total_games=40,
        task_index=0,
        task_count=2,
        workers=1,
        local_out_dir=str(tmp_path),
    )
    assert rc == 0
    assert (tmp_path / "shard_00.jsonl.gz").exists()


# ---------------------------------------------------------------------------
# Test 20 : Non-régression impasse totale (100 % Routes Forestières, rep_id=19901) + garde-fou
# ---------------------------------------------------------------------------
def test_20_impasse_total_razed_forest_and_max_steps_guard() -> None:
    # 1. Graine exacte attrapée sur Cloud Run (tâche 1 : mode=1, chassis=4, N=4, rep_id=19901)
    cfg_seed = GameConfig.from_chassis_index(
        4,
        n_players=4,
        mode=1,
        peuples=("E", "H", "O", "M"),
        exp_seed=20261117,
        rep_id=19901,
        coordonnateur_initial=(19901 - 19375) % 4,
        max_revision_passes=0,
    )
    over_seed = play_game_b0(GameState(cfg_seed), max_steps=2000, chassis_id=4)
    assert 1 <= over_seed.tour_fin <= 8
    assert 0.0 <= over_seed.ratio_arbres <= 1.0

    # 2. Plateau synthétique 100 % rasé dès le Tour 7 (avec passes de révision 2.2 activées)
    cfg_razed = GameConfig(n_players=3, mode=1, exp_seed=2020, max_revision_passes=2)
    st_razed = GameState(cfg_razed)
    st_razed.tour = 7
    for r in range(3):
        for p in range(1, 5):
            st_razed.set_parcel_arbres_souches(r, p, 0, 0)
    over_razed = play_game_b0(st_razed, max_steps=2000)
    assert over_razed.tour_fin == 8
    assert over_razed.score_arbres == 0

    # 3. Vérification explicite que max_steps lève bien RuntimeError si dépassé
    with pytest.raises(RuntimeError, match="max_steps=10"):
        play_game_b0(GameState(GameConfig(n_players=4, mode=1)), max_steps=10)



