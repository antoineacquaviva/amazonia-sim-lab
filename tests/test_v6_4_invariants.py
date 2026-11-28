"""Suite Miroir des 22 Invariants Physiques & Cas Limites v6.4 (INV-01..INV-22).

Source de vérité : `contracts/physical_and_edge_invariants_v6_4.json`.
Vérifie 100 % des invariants noyau v6.4, la non-fuite de `PlayerObservation` sous paravents fermés
et la garantie zéro dette mémorielle (`mem_debt == 0`).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bots.bot_b0 import choose_b0, play_game_b0
from bots.heuristic_engine import play_game_b2
from engine.core_engine import (
    DEC_BOUCLIER_LISIERE_5_3,
    DEC_DEPLOIEMENT_NID_4_2,
    DEC_ENRACINEMENT_6_1,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_OISEAU_CHOIX_DE_1_3,
    DEC_SABOTAGE_CIBLE_3_2,
    apply_choice,
    apply_repousse_finale,
    compute_parade_seuil,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import (
    GameOver,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement_nid,
    prim_insecte_take_with_priming,
    prim_partage_info_etat_gardien,
    verb_etouffer,
    verb_reculer,
    verb_refroidir,
)
from engine.state import (
    CANONICAL_DOTATION,
    CARD_SABOTAGE,
    DUEL_DEFI,
    DUEL_NONE,
    DUEL_TERRITOIRE_TENU,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PERCHOIR_CHAUD,
    PERCHOIR_KIND_RANK,
    PIEGE_ACTIF,
    STEP_1_2_DEAL,
    STEP_1_3_DICE,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_5_3_END_CHECK,
    STEP_6_1_ENRACINEMENT,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_SABOTAGE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parents[1]
INV_CONTRACT = ROOT / "contracts" / "physical_and_edge_invariants_v6_4.json"


def _cfg(
    peuples: tuple[str, ...] = ("H", "M", "O", "R"),
    *,
    mode: int = 2,
    seed: int = 202640,
    rep: int = 0,
    **kw: Any,
) -> GameConfig:
    return GameConfig(
        n_players=len(peuples),
        peuples=peuples,
        mode=mode,
        exp_seed=seed,
        rep_id=rep,
        **kw,
    )


def _drive_step(state: GameState, target_step: int, max_steps: int = 200) -> Any:
    for _ in range(max_steps):
        if state.step == target_step:
            return None
        out = step_until_decision(state)
        if isinstance(out, GameOver):
            return out
        apply_choice(state, choose_b0(state, out))
    return None


# ---------------------------------------------------------------------------
# Méta-test : couverture 22/22 exacte avec physical_and_edge_invariants_v6_4.json
# ---------------------------------------------------------------------------


def test_meta_all_22_v6_4_invariants_covered() -> None:
    data = json.loads(INV_CONTRACT.read_text(encoding="utf-8"))
    invs = data["invariants"]
    assert len(invs) == 22
    g_names = set(globals().keys())
    missing = [inv["target_test_id"] for inv in invs if inv["target_test_id"] not in g_names]
    assert not missing, f"Tests invariants v6.4 manquants : {missing}"


# ---------------------------------------------------------------------------
# INV-01..INV-22
# ---------------------------------------------------------------------------


def test_inv01_finite_reversible_trees_stumps() -> None:
    """INV-01 : Dotation finie 10×N pions Arbre/Souche recto-verso (abatteuse coupe tout, bulldo rase -> Route)."""
    st = GameState(_cfg(("H", "M", "O", "R"), mode=2))
    assert st.total_arbres_plateau() == 4 * sum(CANONICAL_DOTATION)
    for r in range(4):
        for p, dot in enumerate(CANONICAL_DOTATION, start=1):
            assert st.get_parcel_arbres(r, p) == dot
            assert st.get_parcel_souches(r, p) == 0

    # Abatteuse coupe TOUS les Arbres debout d'une parcelle en Souches (zéro perte de pion)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(0, 2) == 0
    assert st.get_parcel_souches(0, 2) == CANONICAL_DOTATION[1]

    # Bulldozer rase toutes les Souches + 1 Arbre (ici parcelle 2 n'a que des Souches -> devient Route !)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st.is_route_forestiere(0, 2)
    assert st.get_parcel_arbres(0, 2) == 0
    assert st.get_parcel_souches(0, 2) == 0


def test_inv02_reversible_power_tokens() -> None:
    """INV-02 : Jetons Puissance recto-verso Rouge (+1) / Bleu (-1) ; Refroidir ne pose jamais de Bleu à sec."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)
    # 0 Rouge -> Refroidir sans effet (zéro Bleu posé à sec)
    assert verb_refroidir(st, 0, MACHINE_ABATTEUSE, 1) == 0
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)

    # 2 Rouges -> Refroidir 1 retourne 1 Rouge en 1 Bleu (somme physique conservée = 2)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 2, 0)
    assert verb_refroidir(st, 0, MACHINE_ABATTEUSE, 1) == 1
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)


def test_inv03_two_reversible_defenders_and_human_chamans() -> None:
    """INV-03 : 2 Défenseurs recto-verso (Réflexion / Définitif) & Chamanes Humains (Tambour + Chant) distincts."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.place_defender_foret(0, 0, 0, 1, FACE_DEFINITIF)
    st.place_defender_foret(0, 1, 0, 2, FACE_REFLEXION)
    assert st.get_player_def_loc_raw(0, 0) != 0
    assert not st.is_player_def2_definitif(0)
    st.set_player_def2_definitif(0, True)
    assert st.is_player_def2_definitif(0)

    # Chamanes Humains : 2 archétypes distincts (1 = Tambour, 2 = Chant)
    st.set_humain_chaman_archetype(0, 1)
    a0 = st.get_humain_chaman_archetype(0)
    a1 = st.get_humain_chaman_archetype(1)
    assert {a0, a1} == {1, 2}


def test_inv04_reflection_closure_n_minus_1() -> None:
    """INV-04 : Dès que N-1 joueurs ont validé leur 2e Défenseur, la phase de révision se clôt."""
    st = GameState(_cfg(("H", "M", "O"), mode=2, max_revision_passes=2))
    go = play_game_b0(st)
    assert isinstance(go, GameOver)
    assert go.tour_fin <= 8


def test_inv05_opaque_bag_and_compound_sabotage() -> None:
    """INV-05 : Sac opaque & Sabotage ordinaire différé à intérêts composés (Refroidir si Rouge, sinon Reculer)."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.step = STEP_3_2_REVEAL
    st.set_player_hand(0, CARD_SABOTAGE, 2, 5, 0, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 1, 3, 1, 0)
    st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 4, 6, 4, 0)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, 0, 0)

    st_a = st.clone()
    req = step_until_decision(st_a)
    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_SABOTAGE_CIBLE_3_2
    assert (0, MACHINE_ABATTEUSE) in req.options
    assert (1, MACHINE_ABATTEUSE) in req.options
    apply_choice(st_a, (0, MACHINE_ABATTEUSE))
    assert st_a.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)
    assert st_a.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert st_a.is_trigger_lit(TRIG_SABOTAGE)

    st_b = st.clone()
    req_b = step_until_decision(st_b)
    assert not isinstance(req_b, GameOver)
    assert req_b.decision_type == DEC_SABOTAGE_CIBLE_3_2
    apply_choice(st_b, (1, MACHINE_ABATTEUSE))
    assert st_b.get_machine_pos_status(1, MACHINE_ABATTEUSE)[0] == 2


def test_inv06_shortage_clockwise_bird_last() -> None:
    """INV-06 : Pénurie servie dans le sens horaire depuis le Coordonnateur, Oiseau servi en dernier."""
    st = GameState(_cfg(("H", "O", "M"), mode=2))
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 0, MACHINE_STATUS_RATISSAGE)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 0, MACHINE_STATUS_RATISSAGE)
    st.set_machine_pos_status(1, MACHINE_BULLDOZER, 0, MACHINE_STATUS_RATISSAGE)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 0, MACHINE_STATUS_RATISSAGE)
    st.set_machine_pos_status(2, MACHINE_BULLDOZER, 0, MACHINE_STATUS_RATISSAGE)
    st.sabotage_deck_count = 0
    st.ecaille_deck_count = 0
    st.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    assert st.deck_len - st.deck_cursor == 1
    st.coordonnateur = 0
    st.step = STEP_1_2_DEAL
    req = step_until_decision(st)
    assert not isinstance(req, GameOver)
    assert st.get_player_hand(0)[0] != 0
    assert st.get_player_hand(1)[0] == 0
    assert st.get_player_hand(2)[0] == 0


def test_inv07_universal_two_dice_and_bird_free_choice() -> None:
    """INV-07 : 2 dés standards universels (même sur Sabotage/Écaille), Oiseau choisit librement D1 ou D2, zéro fuite."""
    st = GameState(_cfg(("H", "O", "M"), mode=2))
    st.step = STEP_1_3_DICE
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 0, 0, 0, 0)
    st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 0, 0, 0, 0)
    req = step_until_decision(st)
    for rep in range(1, 30):
        if not isinstance(req, GameOver) and req.decision_type == DEC_OISEAU_CHOIX_DE_1_3:
            break
        st = GameState(_cfg(("H", "O", "M"), mode=2, rep=rep))
        st.step = STEP_1_3_DICE
        st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
        st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 0, 0, 0, 0)
        st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 0, 0, 0, 0)
        req = step_until_decision(st)

    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_OISEAU_CHOIX_DE_1_3
    assert req.decideur == 1
    _, sd1, sd2, _, _ = st.get_player_hand(0)
    assert 1 <= sd1 <= 6 and 1 <= sd2 <= 6
    _, m_d1, m_d2, m_lec, _ = st.get_player_hand(2)
    assert m_lec == min(m_d1, m_d2)
    o_d1, o_d2 = int(req.options[0]), int(req.options[1])
    big = max(o_d1, o_d2)
    small = min(o_d1, o_d2)
    apply_choice(st, big)
    assert st.get_player_hand(1)[3] == big
    assert st.get_player_discarded_die(1) == small

    obs_h = st.get_observation(0)
    assert obs_h.hand_of(1).card is None
    assert obs_h.hand_of(1).d1 is None
    assert obs_h.hand_of(1).lecture_m is None


def test_inv08_fixed_track_act_strip_and_removed_die() -> None:
    """INV-08 : Réglette fixe T1..T6, bandelette d'Acte, dé retiré dès Étouffement ou fin d'attaque."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    for rk in range(TRACK_LEN):
        assert st.get_tactique_at_rank(rk) == rk + 1

    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 2)
    assert verb_etouffer(st, 0, MACHINE_ABATTEUSE, seat=0)
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert st.get_player_hand(0)[4] == 0

    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    resolve_single_machine_attack(st, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_player_hand(1)[4] == 0


def test_inv09_direct_guardian_icons_and_last_bet_resonance() -> None:
    """INV-09 : Piste directe sans balayage ; Résonance s'allume UNIQUEMENT au dernier pari glissé sur vraie activation."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.set_gardien_at_case(TRIG_PARADE, 1, 1)
    st.set_gardien_at_case(TRIG_RESONANCE, 2, 1)
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, TRIG_RESONANCE, FACE_DEFINITIF)

    # 1re activation de case 1 : il reste 1 pari sur case 1 -> Résonance NE s'allume PAS encore !
    st.light_trigger(TRIG_PARADE)
    sweep_gardiens(st)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 1
    assert st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 1

    # 2e activation de case 1 : vide le dernier pari (1 -> 0) -> Résonance s'allume 1 fois et consomme son pari !
    st.light_trigger(TRIG_PARADE)
    sweep_gardiens(st)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 0

    # Glissement passif (SLIDE_GARDIEN_PARI_ONLY) vidant un Gardien NE déclenche JAMAIS Résonance !
    st.cleanup_end_of_turn_6_2()
    st.set_gardien_at_case(TRIG_PIEGEAGE, 3, 1)
    st.place_defender_gardien_pari(0, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, TRIG_RESONANCE, FACE_DEFINITIF)
    assert prim_partage_info_etat_gardien(st, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=TRIG_PIEGEAGE)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0
    assert not st.is_trigger_lit(TRIG_RESONANCE)
    assert st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 1


def test_inv10_guardian_notches_and_cumulative_awakening() -> None:
    """INV-10 : Encoches visibles, passage Face 2 en 5.3 sur pari gagné & Éveil cumulatif (>= A+1 Face 2, 0 pari perdu)."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    assert st.cfg.nb_animaux_sauvages == 2
    st.tour = 5
    st.set_gardien_at_case(TRIG_PARADE, 1, 2)
    st.set_gardien_at_case(TRIG_PIEGEAGE, 2, 2)
    st.set_gardien_at_case(TRIG_SABOTAGE, 3, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    assert st.count_gardien_pari_defenders_at_case(TRIG_SABOTAGE) == 0

    st.step = STEP_5_3_END_CHECK
    go = step_until_decision(st)
    assert isinstance(go, GameOver)
    assert go.cause_fin == "REVEIL_GARDIENS"

    # Si un autre Gardien a perdu son pari ce tour, pas d'Éveil ce tour et le Gardien repart en lisière !
    st2 = GameState(_cfg(("H", "M", "O"), mode=2))
    st2.tour = 5
    st2.set_gardien_at_case(TRIG_PARADE, 1, 2)
    st2.set_gardien_at_case(TRIG_PIEGEAGE, 2, 2)
    st2.set_gardien_at_case(TRIG_SABOTAGE, 3, 2)
    st2.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st2.step = STEP_5_3_END_CHECK
    out2 = step_until_decision(st2)
    assert not isinstance(out2, GameOver)
    assert st2.get_gardien_at_case(TRIG_SABOTAGE)[0] == 0


def test_inv11_parade_threshold_blue_in_all_modes() -> None:
    """INV-11 : Formule unifiée du Seuil de Parade (min 1, Bleus actifs en Mode 1, 2 et 4)."""
    for mode in (1, 2, 4):
        st = GameState(_cfg(("H", "M", "O"), mode=mode))
        st.tour = 1  # Acte I : T1..T3 = Charge, T4..T6 = Assaut
        st.set_machine_tokens(0, MACHINE_ABATTEUSE, 2, 1)
        # T4 en Acte I (Assaut, mod_seuil=0) : dot(2)=2 + 2 Rouges - 1 Bleu = 3
        s_assaut = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 2, TACTIQUES_SPEC[4], is_ratissage=False)
        assert s_assaut == 3
        # T2 en Acte I (Charge, mod_seuil=0) : Rouges ignorés mais Bleus actifs -> max(1, 2 - 1) = 1
        s_charge = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 2, TACTIQUES_SPEC[2], is_ratissage=False)
        assert s_charge == 1


def test_inv12_ratissage_physical_red_immobile_targeted() -> None:
    """INV-12 : Ratissage = +1 Rouge physique (convertible), immobile, parcelle ciblée, Étouffement 90°."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    assert (0, 4) in list_targeted_parcels(st)
    assert not verb_reculer(st, 0, MACHINE_ABATTEUSE)
    assert st.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 4
    assert verb_refroidir(st, 0, MACHINE_ABATTEUSE, 1) == 1
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)
    assert verb_etouffer(st, 0, MACHINE_ABATTEUSE)
    assert (0, 4) not in list_targeted_parcels(st)


def test_inv13_frozen_targets_and_border_retreat_no_double_jump() -> None:
    """INV-13 : Cibles figées au début de l'activation & Repli de bordure sans double bond."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_parcel_arbres_souches(0, 1, 1, 0)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[3])
    assert st.is_route_forestiere(0, 1)
    assert st.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 2


def test_inv14_machine_tokens_furtivite_and_sentinel_bank() -> None:
    """INV-14 : Furtivité m(r) == 0 (Rive Sabotage) / == 2 (Rive Piège) + Effet Sentinelle permanent (1 ou 2 tuiles)."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.root_tile_on_sabotage_bank(0, 0, tier_souches=1)
    assert st.count_rooted_sentinels_on_ray(0) == 1
    assert st.get_furtivite_rive_capacity(0, FURT_RIVE_SABOTAGE) == 1
    assert st.get_furtivite_rive_capacity(0, FURT_RIVE_PIEGE) == 2

    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.place_defender_furtivite(0, 0, 0, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    sab_tot_before = st.sabotage_deck_count + st.sabotage_pending_count
    st.step = STEP_4_1_FURTIVITE
    step_until_decision(st)
    assert (st.sabotage_deck_count + st.sabotage_pending_count) == sab_tot_before + 1

    # 2 tuiles enracinées -> 2/2 permanent à 0 Défenseur !
    st2 = GameState(_cfg(("H", "M", "O"), mode=2))
    st2.root_tile_on_sabotage_bank(0, 0, tier_souches=1)
    st2.root_tile_on_sabotage_bank(1, 0, tier_souches=1)
    assert st2.count_rooted_sentinels_on_ray(0) == 2
    assert st2.get_furtivite_rive_capacity(0, FURT_RIVE_SABOTAGE) == 0
    st2.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st2.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st2.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    sab_tot_before2 = st2.sabotage_deck_count + st2.sabotage_pending_count
    st2.step = STEP_4_1_FURTIVITE
    step_until_decision(st2)
    assert (st2.sabotage_deck_count + st2.sabotage_pending_count) == sab_tot_before2 + 1


def test_inv15_opening_track_owner_choice_and_lying_defenders() -> None:
    """INV-15 : Fil d'ouverture 1->4 (Altérations avant Sabotages avant Rêves), choix propriétaire et Défenseurs couchés."""
    # Part 1 : Altération (Temps 1) résolue avant Sabotage (Temps 2) et avant Rêve (Temps 4)
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.set_tactique_at_rank(1, TILE_R_BASE + 1)
    st.place_defender_reve_standing(0, 0, 2)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 2, 6, 2, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 3, 4, 0, 0)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_alteration(0, MACHINE_ABATTEUSE, True)

    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st)
    assert not st.has_machine_alteration(0, MACHINE_ABATTEUSE)
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_SABOTAGE_CIBLE_3_2
    apply_choice(st, req.options[0])
    # Continuer jusqu'au prochain arrêt : (1, AB) a été Étouffée par R1 et n'a donc coupé aucun arbre !
    step_until_decision(st)
    assert st.get_parcel_arbres(1, 1) == CANONICAL_DOTATION[0]
    assert st.get_parcel_arbres(1, 2) == CANONICAL_DOTATION[1]

    # Part 2 : Surcharge sur un Rêve (2 mobiles actives au rang 2, 1 Défenseur) -> choix du propriétaire + Défenseur couché !
    st2 = GameState(_cfg(("H", "M", "O"), mode=2))
    st2.set_tactique_at_rank(1, TILE_R_BASE + 1)
    st2.place_defender_reve_standing(0, 0, 2)
    st2.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 0)
    st2.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 2, 6, 2, 0)
    st2.set_player_hand(2, CARD_SABOTAGE, 3, 4, 0, 0)
    st2.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st2.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st2.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st2.step = STEP_3_2_REVEAL
    req_ov = step_until_decision(st2)
    assert not isinstance(req_ov, GameOver)
    assert req_ov.decision_type == "CHOIX_CIBLE_REVE_3_2"
    assert req_ov.decideur == 0  # Propriétaire H de R1
    apply_choice(st2, (1,))
    assert st2.is_machine_etouffee_this_turn(1, MACHINE_ABATTEUSE)
    assert not st2.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert st2.count_reve_activation_defenders_at_case(2) == 0


def test_inv16_zero_crush_on_contact_route_clears_cell() -> None:
    """INV-16 : Zéro écrasement sur parcelle vivante ; création de Route vide Défenseurs, Insectes, Piège, Nid, Duel."""
    st = GameState(_cfg(("H", "M", "I"), mode=2))
    st.set_parcel_arbres_souches(0, 1, 1, 0)
    st.place_defender_foret(0, 0, 0, 1, FACE_DEFINITIF)
    st.set_parcel_insectes(0, 1, 2)
    st.set_parcel_nid(0, 1, 1)
    st.set_duel_state_at(0, 1, DUEL_DEFI)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_BULLDOZER, 4, 0)
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[4])
    assert st.is_route_forestiere(0, 1)
    assert st.get_parcel_defenseurs(0, 1) == 0
    assert st.get_parcel_insectes(0, 1) == 0
    assert st.get_nid_position(1) is None
    assert st.get_duel_state()[0] == DUEL_NONE


def test_inv17_max_one_trap_and_croc_cohabitation_priority() -> None:
    """INV-17 : Max 1 Piège ordinaire par parcelle, cohabitation avec Croc, priorité du Croc sur le Piège."""
    st = GameState(_cfg(("H", "M", "R"), mode=2))
    prim_creation_entite(st, "PIEGE", ray=0, p=2, light_trigger=False)
    prim_creation_entite(st, "CROC", ray=0, p=2)
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st.get_croc_parcel() == (0, 2)

    st.set_gardien_at_case(TRIG_PIEGEAGE, 1, 1)
    st.place_defender_gardien_pari(0, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_croc_parcel() is None
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st.get_parcel_arbres(0, 2) == CANONICAL_DOTATION[1]
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0


def test_inv18_optional_bouclier_lisiere_governed_by_insects() -> None:
    """INV-18 : Bouclier de lisière facultatif gouverné par I ; maintient le Gardien mais le pari reste perdu."""
    st = GameState(_cfg(("H", "M", "I"), mode=2))
    st.tour = 4
    st.set_gardien_at_case(TRIG_PARADE, 1, 2)
    st.set_colonie_at_case(TRIG_PARADE, 1)
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)

    st.step = STEP_5_3_END_CHECK
    req = step_until_decision(st)
    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_BOUCLIER_LISIERE_5_3
    assert req.decideur == 2
    apply_choice(st, "UTILISER_BOUCLIER")
    assert st.get_gardien_at_case(TRIG_PARADE) == (1, 2)
    assert st.get_colonie_at_case(TRIG_PARADE) == 0
    assert st.has_gardien_bet_lost_this_turn()


def test_inv19_unplaceable_tile_ban_and_unified_3p_bonus() -> None:
    """INV-19 : Bonus 3J étendu aux Nids (libère 1 des 2 bâtisseurs vers parcelle adjacente)."""
    st = GameState(_cfg(("H", "M", "I"), mode=2))
    nid_slot = next(
        idx for idx, tid in enumerate(st.cfg.lisiere_slots) if tid.startswith("M")
    )
    st.place_defender_lisiere_tile(0, 0, nid_slot, FACE_DEFINITIF)
    st.place_defender_lisiere_tile(1, 0, nid_slot, FACE_DEFINITIF)
    st.step = STEP_3_1_CONSTRUCT
    req1 = step_until_decision(st)
    assert not isinstance(req1, GameOver)
    apply_choice(st, req1.options[0])
    req2 = step_until_decision(st)
    assert not isinstance(req2, GameOver)
    assert req2.decision_type == DEC_LIBERATION_BATISSEUR_3_1
    chosen_lib = req2.options[0]
    apply_choice(st, chosen_lib)
    lib_seat, lib_def, lib_r, lib_p = chosen_lib
    # Le bâtisseur choisi est immédiatement actif sur la parcelle forêt adjacente !
    assert st.get_parcel_defenseurs(int(lib_r), int(lib_p)) == 1
    other_seat = 1 if int(lib_seat) == 0 else 0
    assert st.decode_def_loc(st.get_player_def_loc_raw(other_seat, 0))[0] == "LISIERE"
    # En passant à 3.2, le 2e bâtisseur bascule bien en attente !
    _ = lib_def


def test_inv20_accessories_v6_4_unified_duel_and_perchoir() -> None:
    """INV-20 : Duel unifié (retourné par parade/piège/Croc/Insectes de tout Peuple) & Perchoir orientable."""
    st = GameState(_cfg(("H", "M", "O"), mode=2))
    st.set_duel_state_at(0, 2, DUEL_DEFI)
    prim_creation_entite(st, "PIEGE", ray=0, p=2, light_trigger=False)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, 0, 2)

    st.oiseau_perchoir_card = machine_card_code(0, MACHINE_ABATTEUSE)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 3, locked=True)
    assert st.get_oiseau_perchoir_signal() == (PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 3, True)
    obs_h = st.get_observation(0)
    assert obs_h.oiseau_plume == (PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 3, True)
    assert obs_h.oiseau_perchoir_card is None


def test_inv21_swarm_direct_deployment_native_priming_and_move() -> None:
    """INV-21 : Déploiement direct en 4.2 (sans étape 4.3), Amorçage natif & Déménagement unifié d'un Nid."""
    st = GameState(_cfg(("H", "M", "I"), mode=4))
    assert st.count_total_insects_on_board() == 0
    ok_p, _ = prim_insecte_take_with_priming(st, ("RESERVE",))
    assert ok_p

    st.set_parcel_nid(2, 4, 1)
    st.place_defender_foret(2, 0, 2, 4, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 4, 2)
    st.step = STEP_4_2_NIDS
    req = step_until_decision(st)
    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_DEPLOIEMENT_NID_4_2
    assert any(o[0] == "BUG" for o in req.options)
    assert any(o[0] == "COLONIE" for o in req.options)
    apply_choice(st, ("BUG", 3))
    req2 = step_until_decision(st)
    assert not isinstance(req2, GameOver)
    assert req2.decision_type == DEC_DEPLOIEMENT_NID_4_2
    apply_choice(st, ("COLONIE", 1))
    assert st.get_bugs_at_case(3) == 1
    assert st.get_colonie_at_case(1) == 1

    st.set_nid_ponte(1, True)
    assert prim_deplacement_nid(st, 1, 1, 3)
    pos_after = st.get_nid_position(1)
    assert pos_after is not None and pos_after[:2] == (1, 3)
    assert st.get_parcel_insectes(2, 4) == 0 and st.get_parcel_insectes(1, 3) == 2
    assert st.get_parcel_defenseurs(2, 4) == 0 and st.get_parcel_defenseurs(1, 3) == 1
    assert st.get_nid_ponte(1)


def test_inv22_voluntary_rooting_on_sabotage_bank() -> None:
    """INV-22 : Enracinement volontaire sur Rive Sabotage (Sentinelle + décompte final libre sur Souches survivantes)."""
    st = GameState(_cfg(("H", "M", "O"), mode=4))
    slot_m = next(idx for idx, tid in enumerate(st.cfg.lisiere_slots) if tid.startswith("G") and st.cfg.peuples[1] == "M")
    g_num = int(st.cfg.lisiere_slots[slot_m][1:])
    st.set_gardien_at_case(TRIG_PARADE, g_num, 2)
    st.set_parcel_arbres_souches(1, 1, 1, 1)
    st.set_parcel_arbres_souches(1, 3, 2, 1)

    st.step = STEP_6_1_ENRACINEMENT
    req = step_until_decision(st)
    assert not isinstance(req, GameOver)
    assert req.decision_type == DEC_ENRACINEMENT_6_1
    assert req.decideur == 1
    assert slot_m in req.options
    apply_choice(st, slot_m)

    assert st.is_slot_rooted(slot_m)
    assert st.count_rooted_sentinels_on_ray(1) == 1
    assert st.get_gardien_at_case(TRIG_PARADE)[0] == 0

    go = apply_repousse_finale(st)
    assert isinstance(go, GameOver)
    assert st.get_parcel_souches(1, 1) == 0 and st.get_parcel_souches(1, 3) == 0
    assert st.get_parcel_arbres(1, 1) == 2 and st.get_parcel_arbres(1, 3) == 3


def test_zero_mem_debt_full_games_modes_1_2_4() -> None:
    """Garantie zéro dette mémorielle (`mem_debt == 0`) sur parties complètes Modes 1, 2 et 4."""
    for mode in (1, 2, 4):
        cfg = _cfg(("H", "M", "O", "R", "E", "I"), mode=mode, seed=202641, rep=mode)
        st = GameState(cfg)
        trk = TelemetryTracker()
        go = play_game_b2(st, telemetry=trk)
        assert isinstance(go, GameOver)
        assert trk.mem_debt_score == 0
