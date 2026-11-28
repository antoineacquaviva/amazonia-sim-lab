"""Suite miroir normative v6.2 — INV-01 à INV-22 (miroir 100 % exact de contracts/physical_and_edge_invariants.json)."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from engine.core_engine import (
    DEC_BOUCLIER_LISIERE_5_3,
    DEC_CHOIX_CIBLE_REVE_3_2,
    DEC_ENRACINEMENT_6_1,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_OISEAU_DE_ENVOL_1_3,
    DEC_OISEAU_PERCHOIR_1_1,
    DEC_REPTILE_POSE_CROC_3_2,
    DEC_REVISION_DEFENSEUR_2,
    _advance_continuation,
    _advance_main_step,
    apply_choice,
    apply_mammifere_duel_choice,
    apply_oiseau_plume_choice,
    apply_repousse_finale,
    apply_step2_def2,
    list_legal_targets,
    list_targeted_parcels,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    HOOK_ENRACINEMENT,
    DecisionRequest,
    GameOver,
    apply_machine_nid_contact,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_puissance,
    prim_permutation_piste,
)
from engine.state import (
    CALE_ECAILLE,
    CALE_NONE,
    CALE_SABOTAGE,
    CANONICAL_DOTATION,
    CARD_ECAILLE,
    CARD_NONE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    DUEL_DEFI,
    DUEL_NONE,
    DUEL_TERRITOIRE_TENU,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    FAMILLE_GARDIEN,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    LISIERE_CONSTRUCTED,
    LISIERE_ROOTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MAX_ECAILLES,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PLUME_CHAUD,
    PLUME_KIND_RAY,
    RATISSAGE_TACTIQUE_SPEC,
    STEP_1_2_DEAL,
    STEP_1_3_DICE,
    STEP_2_2_DEF2,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_5_3_END_CHECK,
    STEP_6_2_EVOLUTION,
    STEP_6_3_END_TURN,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_REVE,
    TRIG_SABOTAGE,
    GameConfig,
    GameState,
    is_tactique_charge,
    machine_card_code,
    tile_id_to_code,
)


def step_once(st: GameState) -> DecisionRequest | GameOver | None:
    if st._continuation:
        return _advance_continuation(st)
    return _advance_main_step(st)


# Registre d'association stricte INV-XX -> fonction de test
INVARIANT_REGISTRY: dict[str, Callable[[], None]] = {}


def invariant(inv_id: str) -> Callable[[Callable[[], None]], Callable[[], None]]:
    """Décorateur enregistrant un test miroir pour un identifiant `INV-XX`."""

    def _decorator(fn: Callable[[], None]) -> Callable[[], None]:
        assert inv_id not in INVARIANT_REGISTRY, f"Doublon de registre : {inv_id}"
        INVARIANT_REGISTRY[inv_id] = fn
        return fn

    return _decorator


def _mk_state(
    peuples: tuple[str, ...] = ("M", "R", "O", "H"),
    *,
    mode: int = 3,
    seed: int = 123,
    symmetric_core_only: bool = False,
) -> GameState:
    cfg = GameConfig(
        n_players=len(peuples),
        mode=mode,
        peuples=peuples,
        exp_seed=seed,
        rep_id=1,
        symmetric_core_only=symmetric_core_only,
    )
    return GameState(cfg)


@invariant("INV-01")
def test_inv01_finite_reversible_trees_stumps() -> None:
    """INV-01 : Dotation finie 10*N recto-verso, Abatteuse coupe tous Arbres, Bulldozer coupe 1 + retire Souches."""
    st = _mk_state(("M", "R", "O", "H"), mode=2, seed=11)
    assert st.total_arbres_plateau() == 10 * st.cfg.n_players
    total_souches = sum(
        st.get_parcel_souches(r, p)
        for r in range(st.cfg.n_players)
        for p in range(1, st.cfg.p_max + 1)
    )
    assert total_souches == 0

    # Parcelle (0, 3) : dotation 3 -> 2 Arbres, 1 Souche
    st.set_parcel_arbres_souches(0, 3, 2, 1)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    # Abatteuse retourne tous les Arbres debout en Souches sans retirer la Souche déjà présente -> (0, 3)
    assert st.get_parcel_arbres(0, 3) == 0
    assert st.get_parcel_souches(0, 3) == 3

    # Bulldozer sur (0, 4) dotation 3 avec 2 Arbres et 1 Souche : retourne 1 Arbre puis retire toutes Souches -> (1, 0)
    st.set_parcel_arbres_souches(0, 4, 2, 1)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(0, 4) == 1
    assert st.get_parcel_souches(0, 4) == 0
    assert not st.is_route_forestiere(0, 4)

    # 2e passage Bulldozer sur (0, 4) -> 0 Arbre, 0 Souche => Route Forestière
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st.is_route_forestiere(0, 4)

    # Repousse finale plafonnée physiquement par les Souches survivantes (<= dotation)
    st.set_parcel_arbres_souches(0, 3, 2, 1)
    st.root_tile_at_parcel(0, 0, 3, tier_souches=2)
    apply_repousse_finale(st)
    assert st.get_parcel_arbres(0, 3) == 3
    assert st.get_parcel_souches(0, 3) == 0
    assert st.get_parcel_arbres(0, 3) + st.get_parcel_souches(0, 3) <= CANONICAL_DOTATION[2]


@invariant("INV-02")
def test_inv02_reversible_power_tokens() -> None:
    """INV-02 : Jetons Puissance recto-verso Rouge (+1) / Bleu Surchauffe (-1) conservés au retournement."""
    st = _mk_state(("M", "R", "O", "H"), mode=2, seed=12)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 2, 0)
    prim_mod_puissance(st, 0, MACHINE_ABATTEUSE, flip_rouge_to_bleu=1)
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)
    assert sum(st.get_machine_tokens(0, MACHINE_ABATTEUSE)) == 2


@invariant("INV-03")
def test_inv03_two_reversible_defenders_and_human_chamans() -> None:
    """INV-03 : 2 Défenseurs recto-verso, verrouillage Plume à la validation du 2e pion, binôme Chamanes H."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=13)
    st.tour = 1
    st.step = STEP_2_2_DEF2
    st.set_gardien_at_case(1, 1, 1)
    # 1er Défenseur jamais autorisé sur GARDIEN_PARI
    legal_def1_m = list_legal_targets(st, 0, is_first_defender=True)
    assert all(t[0] != "GARDIEN_PARI" for t in legal_def1_m)

    # Humains (seat 3 = H) : binôme Tambour + Chant imposé ; Tambour accède aux rayons alliés en 2.1
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    assert st.get_humain_chaman_archetype(0) == CHAMAN_TAMBOUR
    assert st.get_humain_chaman_archetype(1) == CHAMAN_CHANT
    legal_h_tambour = list_legal_targets(st, 3, is_first_defender=True)
    assert ("FORET", 0, 1) in legal_h_tambour

    # Oiseau (seat 2 = O) pose Plume puis verrouille son 2e Défenseur -> Plume figée irréversiblement
    apply_oiseau_plume_choice(st, (PLUME_CHAUD, PLUME_KIND_RAY, 0))
    assert st.get_oiseau_plume()[3] is False
    apply_step2_def2(st, 2, ("POSER_DEFINITIF", ("FORET", 2, 1)), check_legal=False)
    assert st.is_player_def2_definitif(2) is True
    assert st.get_oiseau_plume()[3] is True


@invariant("INV-04")
def test_inv04_reflection_closure_n_minus_1() -> None:
    """INV-04 : Dès que N-1 joueurs ont validé Définitif, le dernier n'a qu'1 ultime ajustement puis validation."""
    st = _mk_state(("M", "R", "O"), mode=2, seed=14)
    st.tour = 1
    st.step = STEP_2_2_DEF2
    for s in range(3):
        st.place_defender_foret(s, 0, s, 1, FACE_DEFINITIF)
    st.place_defender_foret(0, 1, 0, 2, FACE_DEFINITIF)
    st.place_defender_foret(1, 1, 1, 2, FACE_DEFINITIF)
    st.place_defender_foret(2, 1, 2, 2, FACE_REFLEXION)
    st.set_step2_pass_state(1, True)

    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_REVISION_DEFENSEUR_2
    assert req.decideur == 2
    assert req.context.get("final_adjustment_n_minus_1") is True
    kinds = {opt[0] for opt in req.options}
    assert "GARDER_REFLEXION" not in kinds
    assert "DEPLACER_REFLEXION" not in kinds
    assert "VERROUILLER_DEFINITIF" in kinds
    assert "DEPLACER_DEFINITIF" in kinds

    move_opt = next(o for o in req.options if o[0] == "DEPLACER_DEFINITIF")
    apply_choice(st, move_opt)
    assert st.is_player_def2_definitif(2) is True


@invariant("INV-05")
def test_inv05_opaque_bag_tokens_and_remise() -> None:
    """INV-05 : Sac opaque (2N Machines + Sabotages + <=4 Écailles), Perchoir caché à autrui, remise au ménage."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=15)
    # Ajouter 6 Écailles -> plafond strict MAX_ECAILLES == 4
    for _ in range(6):
        prim_creation_entite(st, "ECAILLE", count=1)
    assert st.count_total_ecailles_in_play() == MAX_ECAILLES

    # Perchoir posé par O (seat 2) : visible par O, strictement masqué pour autrui même paravents ouverts !
    st.oiseau_perchoir_card = CARD_ECAILLE
    st.paravents_ouverts = True
    obs_o = st.get_observation(2)
    obs_m = st.get_observation(0)
    assert obs_o.oiseau_has_perchoir is True
    assert obs_o.oiseau_perchoir_card == CARD_ECAILLE
    assert obs_m.oiseau_has_perchoir is True
    assert obs_m.oiseau_perchoir_card is None

    # Remise au ménage 6.3 : Perchoir et jetons révélés retournent dans le sac, Ratissage reste dehors
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL, False)
    st.step = STEP_6_3_END_TURN
    st._continuation.clear()
    out = step_until_decision(st)
    assert not isinstance(out, GameOver)
    assert st.oiseau_perchoir_card == CARD_NONE
    # Machine (0, 0) passée en Ratissage -> hors du sac, 7 machines + 4 Écailles = 11 jetons dans le sac
    assert st.get_machine_pos_status(0, MACHINE_ABATTEUSE)[1] == MACHINE_STATUS_RATISSAGE
    assert st.deck_len == 7 + MAX_ECAILLES


@invariant("INV-06")
def test_inv06_shortage_clockwise_bird_last() -> None:
    """INV-06 : Pénurie servie dans le sens horaire depuis le Coordonnateur avec Oiseau (O) toujours en dernier."""
    # O est en seat 1, Coordonnateur = seat 0 -> ordre de service : 0, 2, 3, puis 1 (O en dernier!)
    st = _mk_state(("M", "O", "R", "H"), mode=3, seed=16)
    st.tour = 2
    st.coordonnateur = 0
    st.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    st.deck_cursor = st.deck_len - 3
    st.step = STEP_1_2_DEAL
    st._continuation.clear()
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert st.get_player_hand(0)[0] != CARD_NONE
    assert st.get_player_hand(2)[0] != CARD_NONE
    assert st.get_player_hand(3)[0] != CARD_NONE
    assert st.get_player_hand(1)[0] == CARD_NONE  # O servi en dernier -> pénurie

    # Avec >= 2 jetons restants au tour de O : O regarde 2 jetons, en garde 1 et pose l'autre sur le Perchoir
    st2 = _mk_state(("M", "O", "R", "H"), mode=3, seed=16)
    st2.tour = 2
    st2.coordonnateur = 0
    st2.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    st2.step = STEP_1_2_DEAL
    st2._continuation.clear()
    req2 = step_until_decision(st2)
    assert isinstance(req2, DecisionRequest)
    assert req2.decision_type == DEC_OISEAU_PERCHOIR_1_1
    assert req2.decideur == 1
    assert len(req2.options) == 2
    keep_card, perch_card = req2.options
    apply_choice(st2, keep_card)
    assert st2.get_player_hand(1)[0] == keep_card
    assert st2.oiseau_perchoir_card == perch_card


@invariant("INV-07")
def test_inv07_universal_dice_roll_no_audio_leak() -> None:
    """INV-07 : Tous les joueurs lancent leurs dés sous paravent (même sur Sabotage/Écaille, jet ignoré)."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=17)
    st.tour = 1
    st.paravents_ouverts = False
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(1, CARD_ECAILLE, 0, 0, 0, 0)
    st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 0, 0, 0, 0)
    st.set_player_hand(3, machine_card_code(3, MACHINE_BULLDOZER), 0, 0, 0, 0)
    st.step = STEP_1_3_DICE
    st._continuation.clear()

    req = step_until_decision(st)
    for s_sab in (0, 1):
        c, d1, d2, lec, b_t = st.get_player_hand(s_sab)
        assert c in (CARD_SABOTAGE, CARD_ECAILLE)
        assert 1 <= d1 <= 6 and 1 <= d2 <= 6
        assert lec == 0 and b_t == 0
    # Zéro fuite vers un observateur adverse sous paravents fermés
    obs_h = st.get_observation(3)
    assert obs_h.hand_of(0).card is None and obs_h.hand_of(0).d1 is None
    assert obs_h.hand_of(1).card is None and obs_h.hand_of(1).d1 is None
    assert obs_h.oiseau_de_envol is None
    # O (seat 2) a lancé son Dé d'Envol (1..6) et reçoit le choix si de_envol != min(d1, d2)
    de_env, _ = st.get_oiseau_de_envol()
    assert 1 <= de_env <= 6
    if isinstance(req, DecisionRequest) and req.decision_type == DEC_OISEAU_DE_ENVOL_1_3:
        assert req.decideur == 2
        assert de_env in req.options


@invariant("INV-08")
def test_inv08_fixed_track_and_reversible_act_strip() -> None:
    """INV-08 : Réglette fixe 1..6 et bandelette d'Acte réversible au Tour 5 sans déplacer Rêves ni Insectes."""
    st = _mk_state(("M", "R", "O", "H", "I"), mode=3, seed=18)
    r1_code = tile_id_to_code("R1")
    st.set_tactique_at_rank(2, r1_code)
    st.set_bugs_at_case(1, 2)
    assert TACTIQUES_SPEC[1].cibles == ("SUR_PLACE",)
    assert TACTIQUES_SPEC[2].cibles == ("DEVANT",)
    assert TACTIQUES_SPEC[3].mod_seuil == -1
    assert TACTIQUES_SPEC[6].mod_seuil == -1

    # Acte I (Tours 1..4) vs Acte II (Tours 5..8)
    assert is_tactique_charge(1, 4) is True and is_tactique_charge(1, 5) is False
    assert is_tactique_charge(4, 4) is False and is_tactique_charge(4, 5) is True

    # Transition Tour 4 -> Tour 5 en 6.3 ne déplace ni les Rêves ni les Insectes de la Réglette
    st.tour = 4
    st.step = STEP_6_3_END_TURN
    st._continuation.clear()
    _ = step_until_decision(st)
    assert st.tour == 5
    assert st.get_tactique_at_rank(2) == r1_code
    assert st.get_bugs_at_case(1) == 2


@invariant("INV-09")
def test_inv09_six_guardian_icons_resonance_sixth_counter() -> None:
    """INV-09 : Ordre canonique 1..6, Résonance en 6e avec compteur sans écrasement et reprise gauche -> droite."""
    assert (TRIG_PARADE, TRIG_PIEGEAGE, TRIG_SABOTAGE, TRIG_REVE, TRIG_INSECTE, TRIG_RESONANCE) == (
        1,
        2,
        3,
        4,
        5,
        6,
    )
    st = _mk_state(("M", "R", "O", "H"), mode=2, seed=19)
    st.set_gardien_at_case(TRIG_PARADE, 1, 1)
    st.set_gardien_at_case(TRIG_PIEGEAGE, 2, 1)
    st.set_gardien_at_case(TRIG_RESONANCE, 3, 1)
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, TRIG_RESONANCE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, TRIG_RESONANCE, FACE_DEFINITIF)

    # Allumer 1 et 2 dans une même passe -> Résonance (6) doit s'activer DEUX fois sans écrasement de bit !
    st.light_trigger(TRIG_PARADE)
    st.light_trigger(TRIG_PIEGEAGE)
    sweep_gardiens(st)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 0
    assert st.count_gardien_pari_consumed_at_case(TRIG_RESONANCE) == 2


@invariant("INV-10")
def test_inv10_guardian_visible_notches_and_zero_bet_no_upgrade() -> None:
    """INV-10 : Encoches visibles en 5.3 : rem>=1 perdu, rem==0&cons>=1 gagné (Face 2), rem==0&cons==0 reste Face 1."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=20)
    st.tour = 2
    g_slots = [
        (idx, tid, SYNERGY_META[tid][2])
        for idx, tid in enumerate(st.cfg.lisiere_slots)
        if SYNERGY_META[tid][0] == FAMILLE_GARDIEN
    ]
    assert len(g_slots) >= 3
    (s0, _, g0), (s1, _, g1), (s2, _, g2) = g_slots[:3]

    # Case 1 : pari gagné (0 rem, 1 cons) -> passe Face 2
    st.set_gardien_at_case(1, g0, 1)
    st.set_lisiere_tile_state(s0, LISIERE_CONSTRUCTED, 0)
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.consume_one_gardien_pari_defender(1)
    # Case 2 : aucune mise (0 rem, 0 cons) -> reste en place sur Face 1 sans évoluer
    st.set_gardien_at_case(2, g1, 1)
    st.set_lisiere_tile_state(s1, LISIERE_CONSTRUCTED, 0)
    # Case 3 : pari perdu (1 rem, 0 cons) -> retourne en lisière Face 1
    st.set_gardien_at_case(3, g2, 2)
    st.set_lisiere_tile_state(s2, LISIERE_CONSTRUCTED, 0)
    st.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)

    st.step = STEP_5_3_END_CHECK
    st._continuation.clear()
    _ = step_until_decision(st)

    assert st.get_gardien_at_case(1) == (g0, 2)  # Gagné -> Face 2
    assert st.get_gardien_at_case(2) == (g1, 1)  # Zéro mise -> reste Face 1
    assert st.get_gardien_at_case(3)[0] == 0  # Perdu -> renvoyé en lisière
    assert st.get_lisiere_tile_state(s2)[0] == LISIERE_UNCONSTRUCTED


@invariant("INV-11")
def test_inv11_parade_threshold_blue_in_all_modes() -> None:
    """INV-11 : Bleus Surchauffe (-1) actifs dans TOUS les modes (Charge, Assaut, Ratissage), rouges ignorés en Charge."""
    st = _mk_state(("M", "R", "O", "H"), mode=2, seed=21)
    st.tour = 1  # Acte I : T1 = CHARGE, T4 = ASSAUT

    # 1. Mode Charge (T1) : parcelle p=3 (dotation 3), 2 rouges (ignorés) + 1 bleu (-1) => Seuil = 3 - 1 = 2 !
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 2, 1)
    st.place_defender_foret(0, 0, 0, 3, FACE_DEFINITIF)
    st.place_defender_foret(1, 0, 0, 3, FACE_DEFINITIF)
    trees_before = st.get_parcel_arbres(0, 3)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(0, 3) == trees_before
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (2, 1)

    # 2. Mode Charge non parée : gain plafonné à +1 rouge sur T3 (2 frappes)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, 0, 0)
    resolve_single_machine_attack(st, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert st.get_machine_tokens(1, MACHINE_ABATTEUSE)[0] == 1

    # 3. Mode Assaut (T4) : dotation 3 + 2 rouges - 1 bleu => Seuil = 4 (3 defs insuffisant)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(2, MACHINE_ABATTEUSE, 2, 1)
    for idx_d in range(3):
        st.place_defender_foret(idx_d, 1, 2, 3, FACE_DEFINITIF)
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert st.get_parcel_arbres(2, 3) == 0

    # 4. Mode Ratissage : dotation 3 + 1 rouge - 2 bleus => Seuil = 2
    st.set_machine_pos_status(3, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE, False)
    st.set_machine_tokens(3, MACHINE_ABATTEUSE, 1, 2)
    st.place_defender_foret(0, 1, 3, 4, FACE_DEFINITIF)
    st.place_defender_foret(3, 0, 3, 4, FACE_DEFINITIF)
    t3_before = st.get_parcel_arbres(3, 4)
    resolve_single_machine_attack(st, 3, MACHINE_ABATTEUSE, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True)
    assert st.get_parcel_arbres(3, 4) == t3_before


@invariant("INV-12")
def test_inv12_ratissage_physical_red_immobile_targeted() -> None:
    """INV-12 : Ratissage donne +1 rouge physique (convertible), zéro +1 virtuel, immobile et parcelle ciblée."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=22)
    st.tour = 2
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 1)
    st.step = STEP_6_3_END_TURN
    st._continuation.clear()
    _ = step_until_decision(st)

    # Passage en Ratissage : conserve (1, 1) + 1 rouge physique => (2, 1), zéro +1 virtuel !
    assert st.get_machine_pos_status(0, MACHINE_ABATTEUSE)[1] == MACHINE_STATUS_RATISSAGE
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (2, 1)
    assert st.get_machine_effective_rouges(0, MACHINE_ABATTEUSE) == 2
    # Ce rouge physique est convertible en bleu
    prim_mod_puissance(st, 0, MACHINE_ABATTEUSE, flip_rouge_to_bleu=1)
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 2)
    # Immobile : impossible de reculer une machine en Ratissage
    prim_deplacement(st, "MACHINE", src_ray=0, m_type=MACHINE_ABATTEUSE, dst_ray=0, dst_p=3)
    assert st.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 4
    # Parcelle ciblée tant qu'elle n'a pas frappé ce tour, puis retirée après frappe
    assert (0, 4) in list_targeted_parcels(st)
    st.set_machine_turn_stats(0, MACHINE_ABATTEUSE, 0, False, True)
    assert (0, 4) not in list_targeted_parcels(st)


@invariant("INV-13")
def test_inv13_frozen_targets_and_border_retreat_no_double_jump() -> None:
    """INV-13 : Cibles figées au début de l'activation & repli de bordure remplace l'avancée de En avançant."""
    st = _mk_state(("M", "R", "O", "H"), mode=2, seed=23)
    st.set_parcel_arbres_souches(0, 1, 1, 0)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL, False)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[3])
    assert st.is_route_forestiere(0, 1)
    # Jamais de double bond p=1 -> p=3 : reste exactement en p=2 !
    assert st.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 2


@invariant("INV-14")
def test_inv14_machine_tokens_visible_until_furtivite() -> None:
    """INV-14 : m(r) compte Machines révélées du rayon + Ratissage (indépendant Rêve/Altération/Sabotage/Écaille)."""
    st = _mk_state(("M", "R", "O", "H", "E"), mode=3, seed=24)
    st.tour = 2
    st.paravents_ouverts = True
    # Rayon 0 : Abatteuse en main (annulée par Rêve -> bound_t=0!) + Bulldozer en Ratissage => m(0) == 2 !
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_RATISSAGE, False)
    # Rayon 1 : aucune machine révélée ni en Ratissage (joueurs tiennent Sabotage & Écaille) => m(1) == 0 !
    st.set_player_hand(1, CARD_SABOTAGE, 2, 3, 0, 0)
    st.set_player_hand(2, CARD_ECAILLE, 4, 5, 0, 0)
    st.place_defender_furtivite(0, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.place_defender_furtivite(1, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.place_defender_furtivite(2, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_furtivite(3, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)

    sab_before = st.sabotage_pending_count
    st.step = STEP_4_1_FURTIVITE
    st._continuation.clear()
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert req.context.get("ray") == 0
    apply_choice(st, req.options[0])
    # Avancer le reste de STEP_4_1_FURTIVITE (rayon 1 -> Rive Sabotage)
    while st.step == STEP_4_1_FURTIVITE:
        step_once(st)
    assert st.sabotage_pending_count == sab_before + 1


@invariant("INV-15")
def test_inv15_opening_order_reve_owner_choice_and_moving_defenders() -> None:
    """INV-15 : Ordre 3.2, choix propriétaire sur Rêve surchargé, TRIG_REVE sur déviée, et Défenseurs solidaires."""
    st = _mk_state(("M", "R", "O", "H", "I"), mode=3, seed=25)
    st.tour = 2
    r1_code = tile_id_to_code("R1")  # propriétaire H (seat 3)
    st.set_tactique_at_rank(1, r1_code)  # rang 2
    st.set_tactique_at_rank(2, tile_id_to_code("R2"))  # rang 3
    st.place_defender_reve_activation(0, 2, FACE_DEFINITIF, def_idx=0)
    st.place_defender_reve_activation(1, 3, FACE_DEFINITIF, def_idx=0)
    st.set_gardien_at_case(TRIG_REVE, 1, 1)
    st.place_defender_gardien_pari(2, TRIG_REVE, FACE_DEFINITIF)

    # 2 machines sur le rang 2 (seat 0 et seat 1) -> propriétaire H (seat 3) doit choisir laquelle annuler !
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 4, 2, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 2, 5, 2, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(3, CARD_NONE, 0, 0, 0, 0)
    st.set_player_hand(4, CARD_NONE, 0, 0, 0, 0)

    st.step = STEP_3_2_REVEAL
    st._continuation.clear()
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_CHOIX_CIBLE_REVE_3_2
    assert req.decideur == 3  # Propriétaire de R1 = H
    assert (1,) in req.options and (0,) in req.options
    # Le propriétaire choisit explicitement d'annuler seat 1 (contrairement à l'ancien -seat qui annulait seat 0)
    apply_choice(st, (1,))
    while st.step == STEP_3_2_REVEAL:
        step_once(st)
    assert st.get_player_hand(1)[4] == 0  # seat 1 annulé
    assert st.get_player_hand(0)[4] == 2  # seat 0 exécute la tactique imprimée rang 2
    assert st.count_gardien_pari_defenders_at_case(TRIG_REVE) == 0  # TRIG_REVE (4) allumé !

    # Poussée de bloc contigu vers la gauche : les Défenseurs migrent AVEC leur Rêve !
    st2 = _mk_state(("M", "R", "O", "H"), mode=3, seed=25)
    st2.set_tactique_at_rank(1, r1_code)
    st2.set_tactique_at_rank(2, tile_id_to_code("R2"))
    st2.place_defender_reve_activation(0, 2, FACE_DEFINITIF, def_idx=0)
    st2.place_defender_reve_activation(1, 3, FACE_DEFINITIF, def_idx=0)
    prim_permutation_piste(st2, "ADVANCE_REVE_LEFT", rank_a=2)
    assert st2.get_tactique_at_rank(0) == r1_code
    assert st2.get_tactique_at_rank(1) == tile_id_to_code("R2")
    assert st2.count_reve_activation_defenders_at_case(1) == 1
    assert st2.count_reve_activation_defenders_at_case(2) == 1
    assert st2.count_reve_activation_defenders_at_case(3) == 0


@invariant("INV-16")
def test_inv16_zero_crush_on_contact_route_clears_cell() -> None:
    """INV-16 : Zéro écrasement au contact machine hors Route ; seule la Route Forestière vide la case."""
    st = _mk_state(("M", "R", "O", "I"), mode=3, seed=26)
    nid_slot = next(
        idx
        for idx, tid in enumerate(st.cfg.lisiere_slots)
        if tid.startswith("M")
    )
    m_num = SYNERGY_META[st.cfg.lisiere_slots[nid_slot]][2]
    st.set_parcel_nid(0, 2, m_num, True)
    st.set_lisiere_tile_state(nid_slot, LISIERE_CONSTRUCTED, 0)
    st.set_parcel_insectes(0, 2, 2)
    st.set_parcel_piege(0, 2, PIEGE_ACTIF)
    st.set_duel_defi(0, 2)

    # Déplacement de machine sur (0, 2) : zéro destruction !
    assert apply_machine_nid_contact(st, 0, 2) is False
    prim_deplacement(st, "MACHINE", src_ray=0, m_type=MACHINE_ABATTEUSE, dst_ray=0, dst_p=2)
    assert st.get_parcel_nid(0, 2) == (m_num, True)
    assert st.get_parcel_insectes(0, 2) == 2
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st.get_duel_state() == (DUEL_DEFI, 0, 2)

    # Création d'une Route Forestière sur (0, 2) : vide tout et renvoie Nid en lisière reconstructible
    st.set_parcel_piege(0, 2, PIEGE_AUCUN)
    st.set_parcel_insectes(0, 2, 1)
    st.set_parcel_arbres_souches(0, 2, 1, 0)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)
    st.set_machine_tokens(0, MACHINE_BULLDOZER, 3, 0)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[4])
    assert st.is_route_forestiere(0, 2)
    assert st.get_parcel_nid(0, 2) == (0, False)
    assert st.get_lisiere_tile_state(nid_slot)[0] == LISIERE_UNCONSTRUCTED
    assert st.get_parcel_insectes(0, 2) == 0
    assert st.get_duel_state() == (DUEL_NONE, 0, 0)


@invariant("INV-17")
def test_inv17_max_one_trap_and_croc_cohabitation_priority() -> None:
    """INV-17 : Max 1 Piège ordinaire autonome par parcelle ; Croc cohabite et pare EN PREMIER."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=27)
    prim_creation_entite(st, "PIEGE", ray=0, p=2)
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    # Une 2e création de Piège ordinaire sur la même parcelle est strictement interdite (plafond 1)
    with pytest.raises(AssertionError):
        prim_creation_entite(st, "PIEGE", ray=0, p=2)
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    # Croc cohabite avec le Piège ordinaire
    prim_creation_entite(st, "CROC", ray=0, p=2)
    assert st.get_croc_parcel() == (0, 2)
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF

    # 1re frappe sur (0, 2) avec 0 Défenseur : Croc pare EN PREMIER, allume TRIG_PIEGEAGE, Piège ordinaire intact !
    st.set_gardien_at_case(TRIG_PIEGEAGE, 1, 1)
    st.place_defender_gardien_pari(0, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    t_before = st.get_parcel_arbres(0, 2)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(0, 2) == t_before
    assert st.get_croc_parcel() is None
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0
    assert st.count_gardien_pari_consumed_at_case(TRIG_PIEGEAGE) == 1

    # 2e frappe sur (0, 2) : Piège ordinaire pare à son tour de manière autonome puis est défaussé
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(0, 2) == t_before
    assert st.get_parcel_piege(0, 2) == PIEGE_AUCUN


@invariant("INV-18")
def test_inv18_optional_bouclier_lisiere_governed_by_insects() -> None:
    """INV-18 : Bouclier de lisière facultatif en 5.3 gouverné par I (choisit de défausser ou conserver l'Insecte)."""
    for choice_str, expect_on_track, expect_col in (
        ("UTILISER_BOUCLIER", True, 0),
        ("LAISSER_RETOURNER", False, 1),
    ):
        st = _mk_state(("M", "R", "O", "I"), mode=3, seed=28)
        st.tour = 2
        g_slot = next(
            idx for idx, tid in enumerate(st.cfg.lisiere_slots) if SYNERGY_META[tid][0] == FAMILLE_GARDIEN
        )
        g_num = SYNERGY_META[st.cfg.lisiere_slots[g_slot]][2]
        st.set_gardien_at_case(1, g_num, 1)
        st.set_lisiere_tile_state(g_slot, LISIERE_CONSTRUCTED, 0)
        st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)  # Pari perdu (1 rem)
        st.set_colonie_at_case(1, 1)

        st.step = STEP_5_3_END_CHECK
        st._continuation.clear()
        req = step_until_decision(st)
        assert isinstance(req, DecisionRequest)
        assert req.decision_type == DEC_BOUCLIER_LISIERE_5_3
        assert req.decideur == 3  # Gouverné par le joueur Insectes (I)
        apply_choice(st, choice_str)
        while st.step == STEP_5_3_END_CHECK:
            step_once(st)

        assert (st.get_gardien_at_case(1)[0] == g_num) is expect_on_track
        assert st.get_colonie_at_case(1) == expect_col
        if expect_on_track:
            assert st.get_gardien_at_case(1)[1] == 1  # Reste sur sa face actuelle (pari toujours perdu)


@invariant("INV-19")
def test_inv19_unplaceable_tile_ban_builders_waiting_and_3p_bonus() -> None:
    """INV-19 : Interdiction de tuile inplaçable, repli 2.1 strict, bâtisseurs en attente & bonus 3J."""
    # 1. Tuile Gardien inplaçable quand les 6 cases sont occupées -> exclue des cibles légales
    st = _mk_state(("M", "R", "O"), mode=3, seed=29)
    g_slot = next(
        idx for idx, tid in enumerate(st.cfg.lisiere_slots) if SYNERGY_META[tid][0] == FAMILLE_GARDIEN
    )
    for c_i in range(1, 7):
        st.set_gardien_at_case(c_i, c_i, 1)
    legal_m = list_legal_targets(st, 0, is_first_defender=True)
    assert ("LISIERE", g_slot) not in legal_m

    # 2. Bonus 3J sur construction d'un Gardien en 3.1 : 1 bâtisseur libéré en forêt, l'autre passe en attente !
    st3 = _mk_state(("M", "R", "O"), mode=3, seed=29)
    st3.tour = 1
    st3.place_defender_lisiere_tile(0, 0, g_slot, FACE_DEFINITIF)
    st3.place_defender_lisiere_tile(1, 0, g_slot, FACE_DEFINITIF)
    st3.step = STEP_3_1_CONSTRUCT
    st3._continuation.clear()
    req_case = step_until_decision(st3)
    assert isinstance(req_case, DecisionRequest)
    apply_choice(st3, req_case.options[0])
    req_lib = step_until_decision(st3)
    assert isinstance(req_lib, DecisionRequest)
    assert req_lib.decision_type == DEC_LIBERATION_BATISSEUR_3_1
    apply_choice(st3, req_lib.options[0])
    # Exécuter la continuation SEND_REMAINING_BUILDERS_WAITING_3_1
    while st3.step == STEP_3_1_CONSTRUCT:
        step_once(st3)
    assert len(st3.list_waiting_defenders()) == 1  # Le 2e bâtisseur est immédiatement en attente !


@invariant("INV-20")
def test_inv20_accessories_3_plus_3_alteration_and_ecaille() -> None:
    """INV-20 : Accessoires 3+3 (H Chant glissement, M Duel bloque avancée, E Altération, R Écaille/Croc/Cale)."""
    # 1. H Chant : Rêve portant Chant qui annule >= 1 machine et 0 machine restante glisse d'1 rang à gauche
    st_h = _mk_state(("M", "R", "O", "H"), mode=3, seed=30)
    st_h.tour = 2
    r1_c = tile_id_to_code("R1")
    st_h.set_tactique_at_rank(2, r1_c)  # rang 3
    st_h.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st_h.place_defender_reve_activation(3, 3, FACE_DEFINITIF, def_idx=0)
    st_h.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 3, 5, 3, 0)
    st_h.step = STEP_3_2_REVEAL
    st_h._continuation.clear()
    while st_h.step == STEP_3_2_REVEAL:
        step_once(st_h)
    assert st_h.get_tactique_at_rank(1) == r1_c  # Glissé du rang 3 vers le rang 2 !

    # 2. M Duel : DEFI -> TERRITOIRE_TENU sur parade Défenseur, bloque avancée T3
    st_m = _mk_state(("M", "R", "O", "H"), mode=3, seed=30)
    st_m.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st_m.place_defender_foret(0, 0, 0, 2, FACE_DEFINITIF)
    st_m.place_defender_foret(1, 0, 0, 2, FACE_DEFINITIF)
    apply_mammifere_duel_choice(st_m, True, 0, 2)
    assert st_m.get_duel_state() == (DUEL_DEFI, 0, 2)
    resolve_single_machine_attack(st_m, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert st_m.get_duel_state() == (DUEL_TERRITOIRE_TENU, 0, 2)
    assert st_m.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2  # Avancée T3 bloquée par Duel !

    # 3. E Altération : recule d'1 parcelle sans frapper à la révélation 3.2
    st_e = _mk_state(("M", "R", "O", "E"), mode=3, seed=30)
    st_e.tour = 2
    st_e.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    prim_creation_entite(st_e, "ALTERATION", ray=0, m_type=MACHINE_ABATTEUSE)
    assert st_e.has_machine_alteration(0, MACHINE_ABATTEUSE) is True
    st_e.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st_e.step = STEP_3_2_REVEAL
    st_e._continuation.clear()
    while st_e.step == STEP_3_2_REVEAL:
        step_once(st_e)
    assert st_e.has_machine_alteration(0, MACHINE_ABATTEUSE) is False
    assert st_e.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2  # Reculée sans frapper
    assert st_e.get_player_hand(0)[4] == 0

    # 4. R Écaille pose le Croc en 3.2 + Cale absorbe l'avancée et remet le jeton au sac
    st_r = _mk_state(("M", "R", "O", "H"), mode=3, seed=30)
    st_r.tour = 2
    st_r.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL, False)
    st_r.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL, False)
    st_r.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st_r.set_player_hand(1, CARD_ECAILLE, 3, 4, 0, 0)
    st_r.set_player_hand(2, machine_card_code(1, MACHINE_BULLDOZER), 1, 2, 1, 0)
    st_r.step = STEP_3_2_REVEAL
    st_r._continuation.clear()
    req_c = step_until_decision(st_r)
    assert isinstance(req_c, DecisionRequest)
    assert req_c.decision_type == DEC_REPTILE_POSE_CROC_3_2
    apply_choice(st_r, req_c.options[0])
    assert st_r.get_croc_parcel() == req_c.options[0]

    prim_creation_entite(st_r, "CALE", ray=0, m_type=MACHINE_ABATTEUSE, cale_type=CALE_SABOTAGE)
    assert st_r.get_machine_cale(0, MACHINE_ABATTEUSE) == CALE_SABOTAGE
    sab_before = st_r.sabotage_pending_count
    resolve_single_machine_attack(st_r, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert st_r.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2  # Avancée absorbée par la Cale !
    assert st_r.get_machine_cale(0, MACHINE_ABATTEUSE) == CALE_NONE
    assert st_r.sabotage_pending_count == sab_before + 1
    prim_creation_entite(st_r, "CALE", ray=0, m_type=MACHINE_ABATTEUSE, cale_type=CALE_ECAILLE)
    assert st_r.get_machine_cale(0, MACHINE_ABATTEUSE) == CALE_ECAILLE


@invariant("INV-21")
def test_inv21_swarm_module_closure_and_passenger_dismount() -> None:
    """INV-21 : Clôture stricte du Module Essaim sans I ; descente sur place de l'Insecte passager au ménage."""
    st_no_i = _mk_state(("M", "R", "O", "H"), mode=3, seed=31)
    assert st_no_i.cfg.has_insectes_peuple is False
    prim_creation_entite(st_no_i, "INSECTE", ray=0, p=1, count=1)
    assert st_no_i.get_parcel_insectes(0, 1) == 0
    st_no_i.light_trigger(TRIG_INSECTE)
    assert not st_no_i.is_trigger_lit(TRIG_INSECTE)
    st_no_i.step = STEP_4_2_NIDS
    st_no_i._continuation.clear()
    _ = step_until_decision(st_no_i)
    assert st_no_i.step != STEP_4_2_NIDS

    # Avec I : Insecte passager non dépensé descend sur place au ménage 6.2
    st_i = _mk_state(("M", "R", "O", "I"), mode=3, seed=31)
    assert st_i.cfg.has_insectes_peuple is True
    st_i.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL, False)
    prim_creation_entite(st_i, "PASSENGER_INSECTE", ray=0, m_type=MACHINE_ABATTEUSE)
    assert st_i.get_machine_passenger_insects(0, MACHINE_ABATTEUSE) == 1
    st_i.cleanup_end_of_turn_6_2()
    assert st_i.get_machine_passenger_insects(0, MACHINE_ABATTEUSE) == 0
    assert st_i.get_parcel_insectes(0, 3) == 1


@invariant("INV-22")
def test_inv22_voluntary_rooting_regrowth_and_sleep_lock() -> None:
    """INV-22 : Enracinement volontaire en 6.1, Sommeil bloqué si Rêve enraciné, repousse 1/2 sur toutes fins."""
    st = _mk_state(("M", "R", "O", "H"), mode=3, seed=32)
    st.tour = 7
    # Trouver un Gardien de M (seat 0) et un Rêve de H (seat 3) dans la dotation générée
    g_m_slot = next(
        idx
        for idx, tid in enumerate(st.cfg.lisiere_slots)
        if SYNERGY_META[tid][0] == FAMILLE_GARDIEN and SYNERGY_META[tid][1] == "M"
    )
    g_m_num = SYNERGY_META[st.cfg.lisiere_slots[g_m_slot]][2]
    r_h_slot = next(
        idx
        for idx, tid in enumerate(st.cfg.lisiere_slots)
        if SYNERGY_META[tid][0] == FAMILLE_REVE and SYNERGY_META[tid][1] == "H"
    )
    r_h_tid = st.cfg.lisiere_slots[r_h_slot]

    st.set_gardien_at_case(1, g_m_num, 2)
    st.set_lisiere_tile_state(g_m_slot, LISIERE_CONSTRUCTED, 0)
    st.set_colonie_at_case(1, 1)
    st.set_tactique_at_rank(0, tile_id_to_code(r_h_tid))
    st.set_lisiere_tile_state(r_h_slot, LISIERE_CONSTRUCTED, 0)
    st.set_parcel_arbres_souches(0, 3, 1, 2)
    st.set_parcel_arbres_souches(3, 2, 1, 1)

    st.step = STEP_6_2_EVOLUTION
    st._continuation.clear()
    req_m = step_until_decision(st)
    assert isinstance(req_m, DecisionRequest)
    assert req_m.decision_type == DEC_ENRACINEMENT_6_1
    assert req_m.decideur == 0
    assert (g_m_slot, 3) in req_m.options
    apply_choice(st, (g_m_slot, 3))

    req_h = step_until_decision(st)
    assert isinstance(req_h, DecisionRequest)
    assert req_h.decision_type == DEC_ENRACINEMENT_6_1
    assert req_h.decideur == 3
    assert (r_h_slot, 2) in req_h.options
    apply_choice(st, (r_h_slot, 2))

    assert st.get_lisiere_tile_state(g_m_slot)[0] == LISIERE_ROOTED
    assert st.get_gardien_at_case(1)[0] == 0
    assert st.get_colonie_at_case(1) == 1  # L'Insecte reste sur l'icône !
    assert st.has_any_rooted_reve() is True
    assert st.is_sommeil_victory() is False  # Rêve enraciné rend le Sommeil impossible !

    # 1. Fin TOUR_8 : repousse F2 (+2) et Rêve (+1) appliquée
    st_t8 = st.clone()
    st_t8.tour = 8
    go_t8 = apply_repousse_finale(st_t8)
    assert go_t8.cause_fin == CAUSE_TOUR_8
    assert st_t8.get_parcel_arbres(0, 3) == 3  # 1 + 2 Souches retournées par Gardien Face 2
    assert st_t8.get_parcel_souches(0, 3) == 0
    assert st_t8.get_parcel_arbres(3, 2) == 2  # 1 + 1 Souche retournée par Rêve
    assert st_t8.get_parcel_souches(3, 2) == 0

    # 2. Fin EVEIL : tous les N 2es Défenseurs consommés sur Gardiens au Tour 7 -> repousse appliquée
    st_ev = st.clone()
    st_ev.tour = 7
    st_ev.set_gardien_at_case(2, 2, 1)
    st_ev.set_gardien_at_case(3, 3, 1)
    st_ev.place_defender_gardien_pari(0, 2, FACE_DEFINITIF)
    st_ev.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st_ev.place_defender_gardien_pari(2, 3, FACE_DEFINITIF)
    st_ev.place_defender_gardien_pari(3, 3, FACE_DEFINITIF)
    st_ev.consume_one_gardien_pari_defender(2)
    st_ev.consume_one_gardien_pari_defender(2)
    st_ev.consume_one_gardien_pari_defender(3)
    st_ev.consume_one_gardien_pari_defender(3)
    go_ev = apply_repousse_finale(st_ev)
    assert go_ev.cause_fin == CAUSE_REVEIL_GARDIENS
    assert st_ev.get_parcel_arbres(0, 3) == 3
    assert st_ev.get_parcel_arbres(3, 2) == 2

    # 3. Fin SOMMEIL (avec Gardien F2 enraciné mais aucun Rêve enraciné) -> repousse appliquée
    st_som = _mk_state(("M", "R", "O", "H"), mode=3, seed=32)
    st_som.tour = 7
    reves_in_game = [
        tid for tid in st_som.cfg.lisiere_slots if SYNERGY_META[tid][0] == FAMILLE_REVE
    ]
    for rk_i, r_tid in enumerate(reves_in_game):
        st_som.set_tactique_at_rank(rk_i, tile_id_to_code(r_tid))
    st_som.set_parcel_arbres_souches(0, 3, 1, 2)
    st_som.root_tile_at_parcel(g_m_slot, 0, 3, tier_souches=2)
    go_som = apply_repousse_finale(st_som)
    assert go_som.cause_fin == CAUSE_REVE_RANG_1
    assert st_som.get_parcel_arbres(0, 3) == 3

    assert HOOK_ENRACINEMENT == "HOOK_ENRACINEMENT"


def test_all_registered_invariants_covered() -> None:
    """Méta-test : 100 % des invariants de contracts/physical_and_edge_invariants.json sont couverts à l'identique."""
    contract_path = Path(__file__).resolve().parent.parent / "contracts" / "physical_and_edge_invariants.json"
    data = json.loads(contract_path.read_text(encoding="utf-8"))
    invariants_list: list[dict[str, Any]] = data["invariants"]
    contract_ids = {str(item["id"]) for item in invariants_list}
    assert set(INVARIANT_REGISTRY.keys()) == contract_ids
    for item in invariants_list:
        inv_id = str(item["id"])
        expected_fn_name = str(item["target_test_id"])
        actual_fn = INVARIANT_REGISTRY[inv_id]
        assert actual_fn.__name__ == expected_fn_name, (
            f"Mismatch pour {inv_id} : attendu {expected_fn_name}, obtenu {actual_fn.__name__}"
        )
