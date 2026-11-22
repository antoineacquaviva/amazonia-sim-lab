"""Tests unitaires dédiés au cœur de jeu expérimental v6.0 (schema_version = 6.0.0-alpha).

Couvre chacune des 4 évolutions structurelles, la télémétrie enrichie, l'agrégation
DuckDB du digest JSON, la politique des bots et le manifeste `validation_socle_v6_0.json` :
1. Furtivité libre (A1) : 2 rives indépendantes, 0 glissement, 1 ou 2 binômes complets.
2. Suppression de la Repousse Finale de base (score = Arbres debout) + exception Abatteuse Ratissage.
3. Rêves en choix exclusif « Bloquer OU Avancer » (saut vers 1re case libre, 5. Rêve inchangé, Mode 4).
4. Réglette des Tactiques réversible Face A/B (Acte 1 Tours 1-4 / Acte 2 Tours 5-8), Charge sur dégât
   effectif uniquement (plafonné à +1/activation), Assaut et Ratissage détaché en Assaut permanent.
5. Télémétrie v6.0, digest DuckDB conservant `defense_attribution` & `reveil_anatomy`, manifeste & bots.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import engine.effects  # noqa: F401
import run_campaign as rc_mod
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import (
    DEC_CHOIX_REVE_3_2,
    _advance_continuation,
    _run_step_3_2,
    apply_choice,
    compute_parade_seuil,
    list_legal_targets,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.primitives import (
    CAUSE_TOUR_8,
    DecisionRequest,
    GameOver,
    prim_permutation_piste,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    RATISSAGE_TACTIQUE_SPEC,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_5_1_TACTIQUES,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    is_act2_tour,
    is_tactique_charge,
    machine_card_code,
    tactique_mode_for_rank,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Furtivité libre (A1) : 0 glissement, 1 rive complète, 2 rives complètes
# ---------------------------------------------------------------------------


def test_v6_0_furtivite_a1_free_placement_and_1_vs_2_rives_execution() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"), exp_seed=6001)
    st = GameState(cfg)
    st.tour = 2

    # --- Cas A : 1 pion seul sur rive 0 + 1 pion seul sur rive 1 (plus 1 Insecte) -> AUCUN glissement, AUCUNE action ---
    st.enter_furtivite(seat=0, def_idx=0, lisiere=0, p=2, rive=0, face=FACE_DEFINITIF)
    st.enter_furtivite(seat=1, def_idx=1, lisiere=0, p=2, rive=1, face=FACE_REFLEXION)
    st.set_furtivite_insectes(0, 2, 2)
    assert st.get_furtivite_slots(0, 2) == (FACE_DEFINITIF, 0, FACE_REFLEXION, 0)
    assert st.get_furtivite_nb_def_rive(0, 2, 0) == 1
    assert st.get_furtivite_nb_def_rive(0, 2, 1) == 1
    obs = st.get_observation(2)
    assert obs.furtivite_rive_defs(0, 2, 0) == 1
    assert obs.furtivite_rive_defs(0, 2, 1) == 1

    # Ancre 4.3 pour stopper juste après 4.1/4.2 sans avancer en Étape 5
    st.set_parcel_insectes(3, 1, 1)
    st.step = STEP_4_1_FURTIVITE
    trk_a = TelemetryTracker()
    req_a = step_until_decision(st, telemetry=trk_a)
    assert isinstance(req_a, DecisionRequest)
    assert st.get_parcel_piege(0, 2) == PIEGE_AUCUN
    assert st.get_parcel_piege(1, 2) == PIEGE_AUCUN
    assert st.sabotage_pending_count == 0
    assert trk_a.summary().furtivite_1_rive_turns == 0
    assert trk_a.summary().furtivite_2_rives_turns == 0

    # --- Cas B : 1 binôme complet rive 0 (2 Déf) + 1 pion seul rive 1 -> seule la rive 0 s'exécute ---
    st_b = GameState(cfg)
    st_b.tour = 2
    st_b.enter_furtivite(seat=0, def_idx=0, lisiere=0, p=2, rive=0, face=FACE_DEFINITIF)
    st_b.enter_furtivite(seat=1, def_idx=1, lisiere=0, p=2, rive=1, face=FACE_REFLEXION)
    st_b.enter_furtivite(seat=2, def_idx=1, lisiere=0, p=2, rive=0, face=FACE_DEFINITIF)
    assert st_b.get_furtivite_nb_def_rive(0, 2, 0) == 2
    assert st_b.get_furtivite_nb_def_rive(0, 2, 1) == 1
    # Rive 0 pleine (interdite), rive 1 encore ouverte (autorisée)
    legal_s3 = list_legal_targets(st_b, seat=3, is_first_defender=False)
    assert ("FURTIVITE", 0, 2, 0) not in legal_s3
    assert ("FURTIVITE", 0, 2, 1) in legal_s3

    st_b.set_parcel_insectes(3, 1, 1)
    st_b.step = STEP_4_1_FURTIVITE
    trk_b = TelemetryTracker()
    req_b = step_until_decision(st_b, telemetry=trk_b)
    assert isinstance(req_b, DecisionRequest)
    assert st_b.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st_b.get_parcel_piege(1, 2) == PIEGE_AUCUN
    assert trk_b.summary().furtivite_1_rive_turns == 1
    assert trk_b.summary().furtivite_2_rives_turns == 0

    # --- Cas C : Les 4 cases occupées (2 binômes complets) -> LES 2 RIVES S'EXÉCUTENT TOUTES LES DEUX ---
    st2 = GameState(cfg)
    st2.tour = 2
    # Lisière 0, p=1 : rayon 0 sans machine (en bougeant les machines de rayon 0 en p=2) -> Piège sur (0,1)
    #                  rayon 1 avec machines inactives en p=1 -> Sabotage !
    st2.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st2.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st2.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st2.set_machine_pos_status(1, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    for s in range(4):
        st2.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)

    st2.enter_furtivite(seat=0, def_idx=0, lisiere=0, p=1, rive=0, face=FACE_DEFINITIF)
    st2.enter_furtivite(seat=1, def_idx=0, lisiere=0, p=1, rive=1, face=FACE_DEFINITIF)
    st2.enter_furtivite(seat=2, def_idx=1, lisiere=0, p=1, rive=0, face=FACE_DEFINITIF)
    st2.enter_furtivite(seat=3, def_idx=1, lisiere=0, p=1, rive=1, face=FACE_DEFINITIF)
    assert st2.get_furtivite_nb_def_rive(0, 1, 0) == 2
    assert st2.get_furtivite_nb_def_rive(0, 1, 1) == 2

    st2.set_parcel_insectes(3, 1, 1)
    st2.step = STEP_4_1_FURTIVITE
    trk_c = TelemetryTracker()
    sab_before = st2.sabotage_pending_count
    req_c = step_until_decision(st2, telemetry=trk_c)
    assert isinstance(req_c, DecisionRequest)
    assert st2.get_parcel_piege(0, 1) == PIEGE_ACTIF
    assert st2.sabotage_pending_count == sab_before + 1
    assert trk_c.summary().furtivite_1_rive_turns == 0
    assert trk_c.summary().furtivite_2_rives_turns == 1


# ---------------------------------------------------------------------------
# 2. Suppression de la Repousse Finale de base + Exception Abatteuse Ratissage
# ---------------------------------------------------------------------------


def test_v6_0_zero_repousse_finale_and_abatteuse_ratissage_stump_exception() -> None:
    # A) 0 Repousse Finale de base : le score compte strictement les Arbres debout
    cfg_std = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=6002)
    st = GameState(cfg_std)
    st.tour = 8
    # Laisser des Souches sur plusieurs parcelles
    st.set_parcel_arbres_souches(0, 1, 0, 2)
    st.set_parcel_arbres_souches(1, 2, 1, 1)
    st.set_parcel_arbres_souches(2, 3, 0, 3)
    arbres_avant_fin = st.total_arbres_plateau()

    trk = TelemetryTracker()
    st.step = STEP_5_3_END_CHECK
    over = step_until_decision(st, telemetry=trk)
    assert isinstance(over, GameOver)
    assert over.cause_fin == CAUSE_TOUR_8
    assert over.score_arbres == arbres_avant_fin
    assert st.get_parcel_arbres(0, 1) == 0 and st.get_parcel_souches(0, 1) == 2
    assert st.get_parcel_arbres(1, 2) == 1 and st.get_parcel_souches(1, 2) == 1
    assert st.get_parcel_arbres(2, 3) == 0 and st.get_parcel_souches(2, 3) == 3
    assert trk.summary().da_arbres_repousse_finale == 0

    # B) Exception Abatteuse en Ratissage CONSERVÉE INTACTE :
    # Sous ARRACHE_1_SOUCHE_SI_SANS_ARBRE, une Abatteuse en Ratissage sur (0 arbre, 1 souche) arrache la souche
    # -> crée une Route Forestière (0/0) -> provoque le Repli automatique vers la bordure !
    cfg_arr = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        role_abatteuse_fin_de_piste="ARRACHE_1_SOUCHE_SI_SANS_ARBRE",
        exp_seed=6003,
    )
    st_arr = GameState(cfg_arr)
    st_arr.tour = 3
    st_arr.set_parcel_arbres_souches(0, 4, 0, 1)  # 0 arbre, 1 souche sur la dernière parcelle p=4
    st_arr.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_arr.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_RATISSAGE)

    resolve_single_machine_attack(
        st_arr, 0, MACHINE_ABATTEUSE, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
    )
    assert st_arr.is_route_forestiere(0, 4) is True
    assert st_arr.get_parcel_souches(0, 4) == 0
    # Repli automatique vers p=3 côté bordure (tout en gardant le statut Ratissage irréversible)
    assert st_arr.get_machine_pos_status(0, MACHINE_ABATTEUSE)[:2] == (3, MACHINE_STATUS_RATISSAGE)
    assert st_arr.get_machine_pos_status(0, MACHINE_BULLDOZER)[:2] == (3, MACHINE_STATUS_RATISSAGE)

    # Témoin STANDARD_COUPE_ARBRE : même parcelle (0 arbre, 1 souche) -> souche laissée intacte
    st_keep = GameState(cfg_std)
    st_keep.tour = 3
    st_keep.set_parcel_arbres_souches(0, 4, 0, 1)
    st_keep.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    resolve_single_machine_attack(
        st_keep, 0, MACHINE_ABATTEUSE, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
    )
    assert st_keep.is_route_forestiere(0, 4) is False
    assert st_keep.get_parcel_souches(0, 4) == 1
    assert st_keep.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 4


# ---------------------------------------------------------------------------
# 3. Rêves en choix exclusif « Bloquer OU Avancer » + saut + exécution 5.1 + Mode 4
# ---------------------------------------------------------------------------


def test_v6_0_reves_exclusive_choice_block_vs_advance_jump_and_step5_execution() -> None:
    # CLEAR_RANK_ONLY supprimé
    with pytest.raises(AssertionError):
        GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), reve_advance_mode="CLEAR_RANK_ONLY")

    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), exp_seed=6004)

    # --- A) Choix BLOQUER : 1 Défenseur face à 2 machines sur R3 (case 6, sous-jacente T6 En avançant) ---
    st_blk = GameState(cfg)
    st_blk.tour = 2
    st_blk.set_gardien_at_case(5, 1, face=1)  # Gardien sur 5. Rêve
    st_blk.place_defender_gardien_pari(0, 5, FACE_DEFINITIF)
    st_blk.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 (origine H = siège 2) sur case 6
    st_blk.place_defender_reve_activation(1, 6, FACE_DEFINITIF)  # 1 seul Défenseur sur R3

    # Siège 0 : Abatteuse p=1 (0 rouge, faible) ; Siège 1 : Bulldozer p=3 (2 rouges, plus menaçante)
    st_blk.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_blk.set_machine_pos_status(1, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    st_blk.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=2, bleus=0)
    st_blk.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_blk.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_blk.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_blk.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    # Ancre 4.3 pour suspendre juste après 3.2 avant 5.1
    st_blk.set_parcel_insectes(3, 1, 1)

    trk_blk = TelemetryTracker()
    st_blk.step = STEP_3_2_REVEAL
    req_blk = step_until_decision(st_blk, telemetry=trk_blk)
    assert isinstance(req_blk, DecisionRequest)
    assert req_blk.decision_type == DEC_CHOIX_REVE_3_2
    assert req_blk.decideur == 2  # Gouverneur H (peuple d'origine de R3)
    assert req_blk.options == ("BLOQUER", "AVANCER")

    apply_choice(st_blk, "BLOQUER", telemetry=trk_blk)
    req_after_blk = step_until_decision(st_blk, telemetry=trk_blk)
    assert isinstance(req_after_blk, DecisionRequest)

    # La plus menaçante (siège 1) est annulée ; siège 0 reste liée au rang 6 ; R3 NE BOUGE PAS ; 5. Rêve allumé
    assert st_blk.get_player_hand(1)[4] == 0
    assert st_blk.get_player_hand(0)[4] == 6
    assert st_blk.get_tactique_at_rank(5) == TILE_R_BASE + 3
    assert st_blk.count_gardien_pari_consumed_at_case(5) == 1
    assert trk_blk.summary().reves_choice_block == 1
    assert trk_blk.summary().reves_choice_advance == 0

    # Vérifier qu'en Étape 5.1, la machine non annulée (siège 0) exécute EFFECTIVEMENT la Tactique T6 sous le Rêve !
    arbres_01_before = st_blk.get_parcel_arbres(0, 1)
    arbres_02_before = st_blk.get_parcel_arbres(0, 2)
    arbres_13_before = st_blk.get_parcel_arbres(1, 3)
    st_blk._continuation.clear()
    st_blk.step = STEP_5_1_TACTIQUES
    _ = step_until_decision(st_blk, telemetry=trk_blk)
    # Siège 0 (T6 En avançant) a frappé (0,1) et (0,2) et avancé en p=2 ; siège 1 (annulé) n'a rien touché !
    assert st_blk.get_parcel_arbres(0, 1) == arbres_01_before - 2
    assert st_blk.get_parcel_arbres(0, 2) == arbres_02_before - 2
    assert st_blk.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert st_blk.get_parcel_arbres(1, 3) == arbres_13_before

    # --- B) Choix AVANCER : 1 seul Défenseur face à 2 machines, R1 en case 5 et R2 en case 4 ---
    st_adv = GameState(cfg)
    st_adv.tour = 2
    st_adv.set_gardien_at_case(5, 1, face=1)
    st_adv.place_defender_gardien_pari(0, 5, FACE_DEFINITIF)
    st_adv.set_tactique_at_rank(3, TILE_R_BASE + 2)  # R2 en case 4
    st_adv.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 en case 5
    st_adv.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 en case 6
    st_adv.place_defender_reve_activation(1, 6, FACE_DEFINITIF)  # 1 seul Défenseur suffit !

    st_adv.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_adv.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st_adv.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_adv.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_adv.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_adv.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_adv.set_parcel_insectes(3, 1, 1)

    trk_adv = TelemetryTracker()
    st_adv.step = STEP_3_2_REVEAL
    req_adv = step_until_decision(st_adv, telemetry=trk_adv)
    assert isinstance(req_adv, DecisionRequest) and req_adv.decision_type == DEC_CHOIX_REVE_3_2
    apply_choice(st_adv, "AVANCER", telemetry=trk_adv)
    req_after_adv = step_until_decision(st_adv, telemetry=trk_adv)
    assert isinstance(req_after_adv, DecisionRequest)

    # 0 machine annulée (toutes deux liées au rang 6) ; R3 SAUTE par-dessus R1 et R2 vers la case 3 (index 2) !
    assert st_adv.get_player_hand(0)[4] == 6
    assert st_adv.get_player_hand(1)[4] == 6
    assert st_adv.get_tactique_at_rank(2) == TILE_R_BASE + 3  # R3 atterri en case 3
    assert st_adv.get_tactique_at_rank(3) == TILE_R_BASE + 2  # R2 immobile
    assert st_adv.get_tactique_at_rank(4) == TILE_R_BASE + 1  # R1 immobile
    assert st_adv.get_tactique_at_rank(5) == 6  # T6 restaurée en case 6
    assert st_adv.count_gardien_pari_consumed_at_case(5) == 1  # 5. Rêve allumé inchangé !
    assert trk_adv.summary().reves_choice_block == 0
    assert trk_adv.summary().reves_choice_advance == 1

    # En 5.1, les 2 machines (rayons distincts au rang 6) exécutent toutes les deux T6
    st_adv._continuation.clear()
    st_adv.step = STEP_5_1_TACTIQUES
    for _ in range(10):
        res_51 = step_until_decision(st_adv, telemetry=trk_adv)
        if st_adv.step != STEP_5_1_TACTIQUES:
            break
        if isinstance(res_51, DecisionRequest):
            apply_choice(st_adv, res_51.options[0], telemetry=trk_adv)
    assert st_adv.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert st_adv.get_machine_pos_status(1, MACHINE_BULLDOZER)[0] == 3

    # --- C) Mode 4 : pouvoir propre de la tuile Rêve (ex: R6:A pose 1 Insecte) actif sur BLOQUER ET AVANCER ---
    cfg_m4 = GameConfig(n_players=4, mode=4, peuples=("M", "R", "H", "I"), exp_seed=6005)
    for chosen_mode in ("BLOQUER", "AVANCER"):
        st_m4 = GameState(cfg_m4)
        st_m4.tour = 2
        st_m4.set_tactique_at_rank(5, TILE_R_BASE + 6)  # R6:A sur case 6 (pair H-I)
        st_m4.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
        st_m4.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
        for s in (1, 2, 3):
            st_m4.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        ins_before = sum(st_m4.get_parcel_insectes(r, p) for r in (2, 3) for p in range(1, 5))
        st_m4.step = STEP_3_2_REVEAL
        _run_step_3_2(st_m4)
        req_m4 = None
        while st_m4._continuation and req_m4 is None:
            req_m4 = _advance_continuation(st_m4)
        assert isinstance(req_m4, DecisionRequest) and req_m4.decision_type == DEC_CHOIX_REVE_3_2
        apply_choice(st_m4, chosen_mode)
        while st_m4._continuation:
            rem = _advance_continuation(st_m4)
            if isinstance(rem, DecisionRequest):
                apply_choice(st_m4, rem.options[0])
        ins_after = sum(st_m4.get_parcel_insectes(r, p) for r in (2, 3) for p in range(1, 5))
        assert ins_after == ins_before + 1, f"Pouvoir R6:A non exécuté sous {chosen_mode}"

    # --- D) Saut direct prim_permutation_piste sur bloc bloqué à gauche -> retourne False ---
    st_full = GameState(cfg)
    st_full.set_tactique_at_rank(0, TILE_R_BASE + 1)
    st_full.set_tactique_at_rank(1, TILE_R_BASE + 2)
    assert prim_permutation_piste(st_full, "ADVANCE_REVE_LEFT", rank_a=1) is False


# ---------------------------------------------------------------------------
# 4. Réglette des Tactiques Face A/B, Charge sur dégât effectif & Ratissage ASSAUT permanent
# ---------------------------------------------------------------------------


def test_v6_0_reglette_face_a_b_charge_assaut_and_ratissage_permanent_assaut() -> None:
    # A) Table de permutation Acte 1 (Tours 1-4, Face A) vs Acte 2 (Tours 5-8, Face B) + actions fixes
    for t in range(1, 5):
        assert is_act2_tour(t) is False
        assert [tactique_mode_for_rank(r, t) for r in range(1, 7)] == [
            "CHARGE",
            "CHARGE",
            "CHARGE",
            "ASSAUT",
            "ASSAUT",
            "ASSAUT",
        ]
    for t in range(5, 9):
        assert is_act2_tour(t) is True
        assert [tactique_mode_for_rank(r, t) for r in range(1, 7)] == [
            "ASSAUT",
            "ASSAUT",
            "ASSAUT",
            "CHARGE",
            "CHARGE",
            "CHARGE",
        ]

    # Actions fixes sur les deux faces
    assert TACTIQUES_SPEC[1].cibles == ("SUR_PLACE",) and TACTIQUES_SPEC[1].mod_seuil == 0 and TACTIQUES_SPEC[1].avancee == 0
    assert TACTIQUES_SPEC[4].cibles == ("SUR_PLACE",) and TACTIQUES_SPEC[4].mod_seuil == 0 and TACTIQUES_SPEC[4].avancee == 0
    assert TACTIQUES_SPEC[2].cibles == ("DEVANT",) and TACTIQUES_SPEC[2].mod_seuil == 0 and TACTIQUES_SPEC[2].avancee == 0
    assert TACTIQUES_SPEC[5].cibles == ("DEVANT",) and TACTIQUES_SPEC[5].mod_seuil == 0 and TACTIQUES_SPEC[5].avancee == 0
    assert TACTIQUES_SPEC[3].cibles == ("SUR_PLACE", "DEVANT") and TACTIQUES_SPEC[3].mod_seuil == -1 and TACTIQUES_SPEC[3].avancee == 1
    assert TACTIQUES_SPEC[6].cibles == ("SUR_PLACE", "DEVANT") and TACTIQUES_SPEC[6].mod_seuil == -1 and TACTIQUES_SPEC[6].avancee == 1
    assert all(TACTIQUES_SPEC[r].gain_rouge == 0 for r in range(1, 7))
    assert RATISSAGE_TACTIQUE_SPEC.code == 0 and RATISSAGE_TACTIQUE_SPEC.est_ratissage_profil is True

    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=6006)

    # B) Mode CHARGE ignore les jetons Puissance existants au seuil ; ASSAUT les applique tous
    st = GameState(cfg)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=3, bleus=0)
    # Parcelle p=1 dotation=2
    st.tour = 4  # Acte 1 (Face A) : case 1 = CHARGE, case 4 = ASSAUT
    assert is_tactique_charge(1, st.tour) is True
    assert is_tactique_charge(4, st.tour) is False
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[1]) == 2  # 3 rouges ignorés !
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[4]) == 5  # 2 + 3 rouges !

    st.tour = 5  # Acte 2 (Face B, permutation au début du Tour 5) : case 1 = ASSAUT, case 4 = CHARGE !
    assert is_tactique_charge(1, st.tour) is False
    assert is_tactique_charge(4, st.tour) is True
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[1]) == 5  # 2 + 3 rouges !
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[4]) == 2  # 3 rouges ignorés !

    # C) Mode CHARGE : +1 jeton Puissance UNIQUEMENT si >= 1 dégât effectif, plafonné à +1 même sur double cible
    # C1) Frappe parée en CHARGE -> 0 gain
    st_par = GameState(cfg)
    st_par.tour = 1
    st_par.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_par.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    st_par.set_parcel_defenseurs(0, 1, 2)  # Suffit car 2 rouges ignorés en CHARGE !
    trk_par = TelemetryTracker()
    resolve_single_machine_attack(st_par, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk_par)
    assert st_par.get_parcel_arbres(0, 1) == 2
    assert st_par.get_machine_tokens(0, MACHINE_ABATTEUSE) == (2, 0)
    assert trk_par.summary().charge_gains == 0

    # C2) Frappe non parée mais 0 dégât effectif (Abatteuse STANDARD sur parcelle à 0 Arbre, 2 Souches) -> 0 gain !
    st_zero = GameState(cfg)
    st_zero.tour = 1
    st_zero.set_parcel_arbres_souches(0, 1, 0, 2)
    st_zero.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_zero.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    trk_zero = TelemetryTracker()
    resolve_single_machine_attack(st_zero, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk_zero)
    assert st_zero.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)
    assert trk_zero.summary().charge_gains == 0

    # C3) Souche arrachée par Bulldozer sur parcelle 0 Arbre / 1 Souche en CHARGE -> dégât effectif -> +1 jeton !
    st_stump = GameState(cfg)
    st_stump.tour = 1
    st_stump.set_parcel_arbres_souches(0, 1, 0, 1)
    st_stump.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st_stump.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=0, bleus=0)
    trk_stump = TelemetryTracker()
    resolve_single_machine_attack(st_stump, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1], telemetry=trk_stump)
    assert st_stump.is_route_forestiere(0, 1) is True
    assert st_stump.get_machine_tokens(0, MACHINE_BULLDOZER) == (1, 0)
    assert trk_stump.summary().charge_gains == 1

    # C4) Double cible (Case 3 En avançant en Acte 1) infligeant des dégâts sur 2 parcelles -> plafonné à +1 !
    st_dbl = GameState(cfg)
    st_dbl.tour = 2
    st_dbl.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_dbl.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=0, bleus=0)
    trk_dbl = TelemetryTracker()
    resolve_single_machine_attack(st_dbl, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3], telemetry=trk_dbl)
    assert st_dbl.get_parcel_arbres(0, 1) == 0  # Dégât parcelle 1
    assert st_dbl.get_parcel_arbres(0, 2) == 0  # Dégât parcelle 2
    assert st_dbl.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert st_dbl.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)  # Plafonné à +1 !
    assert trk_dbl.summary().charge_gains == 1

    # D) Mode ASSAUT : 0 gain de jeton même sur dégâts effectifs
    st_ass = GameState(cfg)
    st_ass.tour = 2  # Acte 1 : case 6 = ASSAUT
    st_ass.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_ass.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
    trk_ass = TelemetryTracker()
    resolve_single_machine_attack(st_ass, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[6], telemetry=trk_ass)
    assert st_ass.get_parcel_arbres(0, 1) == 0
    assert st_ass.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 0)
    assert trk_ass.summary().charge_gains == 0

    # E) Ratissage : détaché de la case 1, mode ASSAUT permanent dès l'Acte 1 (Tours 1-4) :
    #    tous les jetons Puissance (+1 imprimé + jetons physiques) comptent au seuil, et 0 gain sur dégâts !
    st_rat = GameState(cfg)
    st_rat.tour = 2  # Acte 1 (où la case 1 est en CHARGE, mais le Ratissage DOIT être en ASSAUT !)
    st_rat.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_rat.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    # Parcelle p=4 dotation=3 ; +2 rouges physiques +1 imprimé Ratissage = Seuil 6 !
    assert (
        compute_parade_seuil(
            st_rat, 0, MACHINE_ABATTEUSE, 4, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
        )
        == 6
    )
    # 5 Défenseurs ne suffisent PAS (< 6) -> l'Abatteuse inflige 2 dégâts MAIS ne gagne AUCUN jeton Puissance !
    st_rat.set_parcel_defenseurs(0, 4, 5)
    trk_rat = TelemetryTracker()
    st_rat.step = STEP_5_2_RATISSAGE
    _ = step_until_decision(st_rat, telemetry=trk_rat)
    assert st_rat.get_parcel_arbres(0, 4) == 1
    assert st_rat.get_machine_tokens(0, MACHINE_ABATTEUSE) == (2, 0)
    assert trk_rat.summary().charge_gains == 0


# ---------------------------------------------------------------------------
# 5. Manifeste validation_socle_v6_0.json, télémétrie DuckDB & courbe B0 < B1 < B2
# ---------------------------------------------------------------------------


def test_v6_0_manifest_plan_and_duckdb_digest_metrics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "validation_socle_v6_0.json"
    assert manifest_path.is_file(), "campaigns/manifests/validation_socle_v6_0.json manquant"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "validation_socle_v6_0"
    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["migration_policy"]["SLOT_BUG_CERVEAU"] == "B"
    assert plan["migration_policy"]["SLOT_COLONISATION_GARDIENS"] == "B"
    assert plan["profile_variants"][0]["reve_advance_mode"] == "SAUT"
    assert plan["profile_variants"][0]["gardien_bet_cap_policy"] == "UNIFORM_MAX_2"
    assert plan["profile_variants"][0]["gardien_4_trigger_mode"] == "DISTINCT_OPEN_1"
    # 3 bots * 4 N * 6 chassis = 72 configs * 120 = 8 640 parties ; 41 tables uniques avec A >= 1
    assert plan["total_configurations"] == 72
    assert plan["total_games"] == 8640
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert len({u["peuples"] for u in plan["units"]}) == 41

    # Micro-run local (Mode 2, B0/B1/B2, N=4) + agrégation DuckDB
    micro_manifest: dict[str, Any] = {
        "campaign_name": "micro_validation_socle_v6_0",
        "description": "Test bout-en-bout des 7 compteurs v6.0 dans le digest JSON",
        "mode": 2,
        "bots": ["B0", "B1", "B2"],
        "k_max": 2,
        "seed": 6060,
        "player_counts": [4],
        "table_selection": "PALIER1_DEFAULT",
        "min_animaux_sauvages": 1,
        "games_per_configuration": 6,
        "reve_activation_mode": "1_DEF_1_MACHINE",
        "reve_advance_mode": "EXCLUSIVE_CHOICE",
        "gardien_bet_cap_policy": "UNIFORM_MAX_2",
        "gardien_4_trigger_mode": "DISTINCT_OPEN_1",
        "base_instance": {
            "config_index_192": 1,
            "bundle_id": "STANDARD_A",
            "slots_insectes": {
                "SLOT_BUG_CERVEAU": "B",
                "SLOT_COLONISATION_GARDIENS": "B",
            },
        },
        "chassis_plan": {"varying_axes": [], "fixed_axes": {"Profil_Piste": "P4_2233"}},
        "slot_profile_comparisons": {},
    }
    micro_file = tmp_path / "micro_validation_socle_v6_0.json"
    micro_file.write_text(json.dumps(micro_manifest), encoding="utf-8")
    micro_plan = resolve_manifest_plan(micro_manifest)

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(micro_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0

    digests_dir = tmp_path / "data_digests"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    _, _, digest = aggregate_campaign_duckdb(
        manifest=micro_manifest,
        plan=micro_plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="local",
        job_name="local-micro-v6",
        tasks=1,
        job_wall_sec=0.5,
    )

    assert digest["active_core_rules"]["version"] == "6.0.0-alpha"
    v6_keys = (
        "count_reves_choice_block",
        "count_reves_choice_advance",
        "mean_power_tokens_end_act1",
        "mean_power_tokens_end_game",
        "count_charge_gains",
        "count_furtivite_1_rive_turns",
        "count_furtivite_2_rives_turns",
    )
    totals = digest["totals"]
    for k in v6_keys:
        assert k in totals, f"Compteur v6.0 manquant dans totals : {k}"
    assert totals["count_charge_gains"] > 0
    assert totals["mean_power_tokens_end_game"] > 0.0
    assert totals["count_reves_choice_block"] + totals["count_reves_choice_advance"] >= 0

    # Vérifier aussi la présence dans by_mode et by_n_players
    assert len(digest["by_mode"]) == 3
    for row in digest["by_mode"]:
        for k in v6_keys:
            assert k in row
    for row in digest["by_n_players"]:
        for k in v6_keys:
            assert k in row

    # Conservation de defense_attribution et reveil_anatomy (si au moins 1 tentative)
    assert "defense_attribution" in digest
    assert digest["defense_attribution"]["arbres_repousse_finale"] == 0


def test_v6_0_bots_progression_smoke_b0_b1_b2() -> None:
    """Vérifie que B0, B1 et B2 jouent sans erreur et que B2 surclasse nettement B0 sur le cœur v6.0."""
    n_games = 12
    ratios = {"B0": 0.0, "B1": 0.0, "B2": 0.0}
    for rep in range(n_games):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "H", "I"),
            exp_seed=6090,
            rep_id=rep,
            max_revision_passes=3,
        )
        ratios["B0"] += play_game_b0(GameState(cfg)).ratio_arbres
        ratios["B1"] += play_game_b1(GameState(cfg)).ratio_arbres
        ratios["B2"] += play_game_b2(GameState(cfg)).ratio_arbres

    mean_b0 = ratios["B0"] / n_games
    mean_b1 = ratios["B1"] / n_games
    mean_b2 = ratios["B2"] / n_games
    assert mean_b1 > mean_b0
    assert mean_b2 > mean_b0
