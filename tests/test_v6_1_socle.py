"""Suite exhaustive de tests unitaires et cas limites du socle expérimental v6.1 (schema_version = 6.1.0-alpha).

Couvre systématiquement tous les arbitrages et cas limites de la Phase 1 :
1. Portée, non-empilement et cycle de vie des Pièges autonomes (TURN_PARCEL vs SINGLE_STRIKE,
   0 consommation des Défenseurs/Insectes présents, persistance, traversée Nid, effacement sur Route).
2. Rêves épurés en socle (CLEAR_RANK_ONLY), ouverture de 2.1 aux Rêves, partition stricte 3.2
   (Bug ±1 vers Rêve défendu : cas 1 carte vs 2 cartes), surplus de Défenseurs (2.1+2.2 vs 1 machine),
   Tour 1 / Rêve fraîchement bâti en 3.1, et déblocage de l'Éveil 100 % Gardiens à 6J via 5. Rêve en 2.1.
3. Furtivité « Chaud vs Calme » aux limites (rayon 100 % rasé fermé vs partiellement rasé ouvert,
   1 Ratissage + 1 carte = m(r)==2, indépendance vis-à-vis de Bug ±1 et d'annulation Rêve,
   Sabotage révélé = 0 rayon, auto-pose sur unique parcelle éligible, conservation cartes & pions).
4. Commutateur CHARGE_GAIN (DEGAT_EFFECTIF vs FRAPPE_NON_PAREE) et interactions T3/T6 « En avançant »
   (SUR_PLACE + saut de Pont routier + Contact Machine-Nid + DEVANT hors-plateau depuis last_p, plafond +1).
5. Campagne Micro de forks causaux v6.1 (2.1, 2.2, 4.1, 5.3), rejeu déterministe bit-à-bit et mem_debt == 0.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import engine.effects  # noqa: F401
import run_campaign as rc_mod
from bots.bot_b0 import play_game_b0
from bots.bot_b3_rh import play_game_b3
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.designs import run_v6_1_causal_forks_on_config
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import (
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    _advance_continuation,
    _run_step_3_2,
    apply_choice,
    apply_step2_def1,
    apply_step2_def2,
    insert_reve_on_track,
    list_legal_targets,
    lock_all_def2_in_place,
    resolve_single_machine_attack,
    step_until_decision,
)
from engine.primitives import (
    CAUSE_REVEIL_GARDIENS,
    DecisionRequest,
    GameOver,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_3_MIGRATION,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    STEP_6_2_EVOLUTION,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Pièges autonomes : portée unique SINGLE_STRIKE, non-empilement & cycle de vie
# ---------------------------------------------------------------------------


def test_v6_1_autonomous_piege_zero_def_preserves_allies_and_single_strike() -> None:
    # A) Piège autonome avec 0 Défenseur et 0 Insecte -> bloque seul, défaussé aussitôt, allume 2. Piégeage
    cfg_ss = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "I"),
        exp_seed=9101,
    )
    st0 = GameState(cfg_ss)
    # Vérifier le départ décalé canonique v6.1 (Bulldozer p=1, Abatteuse p=2)
    assert st0.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 1
    assert st0.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    st0.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st0.set_gardien_at_case(1, 1, 1)
    st0.set_gardien_at_case(2, 2, 1)
    st0.set_gardien_at_case(6, 3, 1)
    st0.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st0.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st0.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    st0.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st0.set_parcel_defenseurs(0, 1, 0)
    st0.set_parcel_insectes(0, 1, 0)

    trk0 = TelemetryTracker()
    resolve_single_machine_attack(st0, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4], telemetry=trk0)
    assert st0.get_parcel_arbres(0, 1) == 2
    assert st0.get_parcel_piege(0, 1) == PIEGE_AUCUN  # Défaussé aussitôt (SINGLE_STRIKE)
    assert st0.count_gardien_pari_consumed_at_case(2) == 1
    assert st0.count_gardien_pari_consumed_at_case(1) == 0
    assert st0.count_gardien_pari_consumed_at_case(6) == 0
    assert trk0.summary().ok_pieges_triggered == 1

    # B) Parcelle portant Piège + 1 Défenseur + 2 Insectes face à Seuil 5 :
    #    ni Défenseur ni Insecte consommés, Piège défaussé aussitôt, SEUL 2. Piégeage s'allume !
    st_co = GameState(cfg_ss)
    st_co.set_gardien_at_case(1, 1, 1)
    st_co.set_gardien_at_case(2, 2, 1)
    st_co.set_gardien_at_case(6, 3, 1)
    st_co.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_co.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st_co.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    st_co.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_co.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=3, bleus=0)
    st_co.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st_co.set_parcel_defenseurs(0, 1, 1)
    st_co.set_parcel_insectes(0, 1, 2)

    resolve_single_machine_attack(st_co, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert st_co.get_parcel_arbres(0, 1) == 2
    assert st_co.get_parcel_defenseurs(0, 1) == 1
    assert st_co.get_parcel_insectes(0, 1) == 2
    assert st_co.get_parcel_piege(0, 1) == PIEGE_AUCUN
    assert st_co.count_gardien_pari_consumed_at_case(2) == 1
    assert st_co.count_gardien_pari_consumed_at_case(1) == 0
    assert st_co.count_gardien_pari_consumed_at_case(6) == 0

    # C) SINGLE_STRIKE quand Abatteuse ET Bulldozer frappent (0, 4) :
    #    le Piège pare la 1re frappe (Abatteuse), est défaussé aussitôt, et laisse passer le Bulldozer !
    st_ss = GameState(cfg_ss)
    st_ss.tour = 3
    st_ss.set_parcel_piege(0, 4, PIEGE_ACTIF)
    st_ss.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_ss.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_RATISSAGE)
    trk_ss = TelemetryTracker()
    st_ss.step = STEP_5_2_RATISSAGE
    _ = step_until_decision(st_ss, telemetry=trk_ss)
    # Abatteuse parée, puis Bulldozer coupe 1 arbre et arrache la souche -> il reste 2 arbres, 0 souche !
    assert st_ss.get_parcel_arbres(0, 4) == 2
    assert st_ss.get_parcel_souches(0, 4) == 0
    assert st_ss.get_parcel_piege(0, 4) == PIEGE_AUCUN
    s_ss = trk_ss.summary()
    assert s_ss.ok_pieges_triggered == 1
    assert s_ss.da_piege == 1


def test_v6_1_piege_no_stacking_persistence_nid_traversal_and_route_clear() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "I"),
        exp_seed=9103,
    )
    st = GameState(cfg)
    st.tour = 2
    st.paravents_ouverts = True

    # 1) Non-empilement : si p=1,2,3 portent déjà PIEGE_ACTIF, seule p=4 est éligible -> auto-pose sur p=4 sans prompt !
    for p in (1, 2, 3):
        st.set_parcel_piege(0, p, PIEGE_ACTIF)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 1, 1, 1)
    st.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 2, 2, 2, 2)
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st.place_defender_furtivite(0, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.place_defender_furtivite(1, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.set_parcel_insectes(3, 1, 1)  # Ancre 4.3
    st.step = STEP_4_1_FURTIVITE
    req = step_until_decision(st)
    # Aucune DecisionRequest POSE_PIEGE_FURTIVITE_4_1 : posé directement sur l'unique parcelle libre (0, 4) !
    assert isinstance(req, DecisionRequest) and req.decision_type != DEC_POSE_PIEGE_FURTIVITE_4_1
    assert st.get_parcel_piege(0, 4) == PIEGE_ACTIF

    # Si TOUTES les parcelles non-Route du rayon portent déjà un Piège, Rive Piège ne s'empile pas
    st_full = st.clone()
    st_full._continuation.clear()
    assert st_full.get_furtivite_nb_def_rive(0, 1, FURT_RIVE_PIEGE) == 2
    trk_full = TelemetryTracker()
    st_full.step = STEP_4_1_FURTIVITE
    _ = step_until_decision(st_full, telemetry=trk_full)
    assert trk_full.summary().ok_furt_rive_piege_lost == 1

    # 2) Persistance d'un Piège non déclenché & préservation lors d'un Contact Machine-Nid :
    st_nid = GameState(cfg)
    st_nid.tour = 2
    st_nid.set_parcel_piege(0, 2, PIEGE_ACTIF)
    st_nid.set_parcel_nid(0, 2, 1, active_ce_tour=False)
    st_nid.set_parcel_insectes(0, 2, 3)
    st_nid.set_parcel_defenseurs(0, 2, 1)
    st_nid.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_nid.set_machine_pos_status(0, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    st_nid.set_parcel_arbres_souches(0, 3, 1, 0)
    resolve_single_machine_attack(st_nid, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    # (0,3) devient Route -> Bulldozer recule sur (0,2) -> renvoie le Nid et défausse les 3 Insectes,
    # MAIS le Piège non déclenché et le Défenseur sur (0,2) restent intacts !
    assert st_nid.is_route_forestiere(0, 3) is True
    assert st_nid.get_machine_pos_status(0, MACHINE_BULLDOZER)[0] == 2
    assert st_nid.get_parcel_nid(0, 2)[0] == 0
    assert st_nid.get_parcel_insectes(0, 2) == 0
    assert st_nid.get_parcel_defenseurs(0, 2) == 1
    assert st_nid.get_parcel_piege(0, 2) == PIEGE_ACTIF

    # Passage par 5.3 + 6.2 + 6.3 : le Piège non déclenché sur (0,2) persiste au Tour 3 !
    st_nid.step = STEP_5_3_END_CHECK
    _ = step_until_decision(st_nid)
    assert st_nid.tour == 3
    assert st_nid.get_parcel_piege(0, 2) == PIEGE_ACTIF

    # 3) Défausse immédiate du Piège sur 1re frappe puis transformation de la parcelle en Route sur 2e frappe
    st_rt = GameState(cfg)
    st_rt.tour = 2
    st_rt.set_parcel_arbres_souches(0, 1, 1, 0)
    st_rt.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st_rt.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_rt.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st_rt, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st_rt.get_parcel_piege(0, 1) == PIEGE_AUCUN
    resolve_single_machine_attack(st_rt, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st_rt.is_route_forestiere(0, 1) is True
    assert st_rt.get_parcel_piege(0, 1) == PIEGE_AUCUN


# ---------------------------------------------------------------------------
# 2. Partition stricte 3.2, Rêves 2.1 + 2.2, Tour 1 sans Rêve & Éveil à 6J
# ---------------------------------------------------------------------------


def test_v6_1_strict_partition_3_2_bug_onto_defended_reve_1_vs_2_cards_and_surplus_def() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=9201)

    # A) 1 Bug dévie 1 machine (M=5 -> 6) ET 1 autre carte non déviée pointe déjà sur M=6 (Rêve avec 2 Défenseurs) :
    #    - La carte déviée allume 6. Insecte ;
    #    - La carte NON déviée annulée par le 2e Défenseur allume 5. Rêve !
    #    Chaque carte n'allume qu'au plus 1 déclencheur ("1 événement = au plus 1 déclencheur").
    st = GameState(cfg)
    st.tour = 2
    st.set_tactique_at_rank(5, TILE_R_BASE + 1)  # R1 sur case 6
    st.place_defender_reve_activation(0, 6, FACE_DEFINITIF, def_idx=0)  # 2.1
    st.place_defender_reve_activation(1, 6, FACE_DEFINITIF, def_idx=1)  # 2.2
    st.set_bugs_at_case(5, 1)
    st.set_gardien_at_case(5, 1, 1)
    st.set_gardien_at_case(6, 2, 1)
    st.place_defender_gardien_pari(2, 5, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, 6, FACE_DEFINITIF)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)  # Sera déviée 5 -> 6
    st.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)  # Non déviée sur 6
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_parcel_insectes(3, 1, 1)

    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest) and "M_PLUS_1" in req.options
    apply_choice(st, "M_PLUS_1")
    _ = step_until_decision(st)
    assert st.get_player_hand(0)[4] == 0
    assert st.get_player_hand(1)[4] == 0
    assert st.has_gardien_opened_this_turn(6) is True
    assert st.has_gardien_opened_this_turn(5) is True

    # B) Surplus de Défenseurs : 2 Défenseurs (2.1 + 2.2) sur un Rêve face à 1 seule machine ->
    #    1 seul Défenseur consommé, 1 reste non consommé, et 6.2 rend proprement tous les Défenseurs
    st_sur = GameState(cfg)
    st_sur.tour = 2
    st_sur.set_tactique_at_rank(5, TILE_R_BASE + 1)
    st_sur.place_defender_reve_activation(0, 6, FACE_DEFINITIF, def_idx=0)
    st_sur.place_defender_reve_activation(1, 6, FACE_DEFINITIF, def_idx=1)
    st_sur.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_sur.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_sur.step = STEP_3_2_REVEAL
    _run_step_3_2(st_sur)
    while st_sur._continuation:
        assert _advance_continuation(st_sur) is None
    assert st_sur.count_reve_activation_consumed_at_case(6) == 1
    assert st_sur.count_reve_activation_defenders_at_case(6) == 1
    st_sur.step = STEP_6_2_EVOLUTION
    _ = step_until_decision(st_sur)
    assert st_sur.count_reve_activation_consumed_at_case(6) == 0
    assert st_sur.count_reve_activation_defenders_at_case(6) == 0

    # C) Tour 1 sans Rêve en piste + Rêve fraîchement bâti en 3.1 inerte en 3.2
    st_t1 = GameState(cfg)
    assert all(
        t[0] != "REVE_ACTIVATION" for t in list_legal_targets(st_t1, 0, is_first_defender=True)
    )
    assert all(
        t[0] != "REVE_ACTIVATION" for t in list_legal_targets(st_t1, 0, is_first_defender=False)
    )
    reve_slot = next(i for i, tid in enumerate(cfg.lisiere_slots) if tid.startswith("R"))
    st_t1.set_lisiere_tile_state(reve_slot, LISIERE_UNCONSTRUCTED, 2)
    st_t1.set_gardien_at_case(5, 1, 1)
    st_t1.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st_t1.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_t1.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_t1.set_parcel_insectes(3, 1, 1)
    st_t1.step = STEP_3_1_CONSTRUCT
    _ = step_until_decision(st_t1)
    # Le Rêve a été construit en case 6 en 3.1, mais sans Défenseur dessus -> inerte en 3.2, 5. Rêve NON allumé !
    assert st_t1.get_tactique_at_rank(5) >= TILE_R_BASE
    assert st_t1.has_gardien_opened_this_turn(5) is False
    assert st_t1.get_player_hand(0)[4] == 6


def test_v6_1_6j_eveil_unlocked_by_2_1_reve_lighting_case_5() -> None:
    """À 6 joueurs, un 1er Défenseur (2.1) posé sur un Rêve allume 5. Rêve en 3.2 pendant que les 6
    seconds Défenseurs (2.2) sont engagés sur la Piste des Gardiens -> victoire CAUSE_REVEIL_GARDIENS !
    """
    cfg = GameConfig(n_players=6, mode=2, peuples=("M", "R", "O", "H", "E", "I"), exp_seed=9206)
    st = GameState(cfg)
    st.tour = 4
    insert_reve_on_track(st, 1)  # R1 sur case 6
    # 4 Gardiens construits sur cases 3 (Sabotage), 4 (Résonance), 5 (Rêve), 6 (Insecte)
    st.set_gardien_at_case(3, 1, 1)
    st.set_gardien_at_case(4, 2, 1)
    st.set_gardien_at_case(5, 3, 1)
    st.set_gardien_at_case(6, 4, 1)
    st.set_bugs_at_case(2, 1)

    # Étape 2.1 : siège 3 (H) pose son 1er Défenseur sur R1 (case 6) !
    st.step = STEP_2_1_DEF1
    apply_step2_def1(st, 3, ("REVE_ACTIVATION", 6))
    for s in (0, 1, 2, 4, 5):
        apply_step2_def1(st, s, ("FORET", s, 1))

    # Étape 2.2 : les N=6 joueurs engagent tous leur 2e Défenseur sur la Piste des Gardiens :
    # - 2 sur case 3 (Sabotage), 2 sur case 4 (Résonance), 1 sur case 5 (Rêve !), 1 sur case 6 (Insecte)
    st.step = STEP_2_2_DEF2
    apply_step2_def2(st, 0, ("POSER_REFLEXION", ("GARDIEN_PARI", 3)))
    apply_step2_def2(st, 1, ("POSER_REFLEXION", ("GARDIEN_PARI", 3)))
    apply_step2_def2(st, 2, ("POSER_REFLEXION", ("GARDIEN_PARI", 4)))
    apply_step2_def2(st, 3, ("POSER_REFLEXION", ("GARDIEN_PARI", 4)))
    apply_step2_def2(st, 4, ("POSER_REFLEXION", ("GARDIEN_PARI", 5)))
    apply_step2_def2(st, 5, ("POSER_REFLEXION", ("GARDIEN_PARI", 6)))
    lock_all_def2_in_place(st)
    assert st.is_eveil_attempt_eligible() is True

    # Mains révélées en 3.2 : 2 Sabotages + 1 dé M=2 dévié par Bug + 1 dé M=6 annulé par le 1er Défenseur sur R1 !
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 2, 2, 2, 0)
    st.set_player_hand(3, machine_card_code(3, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st.set_player_hand(4, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(5, CARD_SABOTAGE, 0, 0, 0, 0)

    trk = TelemetryTracker()
    trk.on_reveil_attempt(st)
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st, telemetry=trk)
    assert isinstance(req, DecisionRequest) and "M_PLUS_1" in req.options
    apply_choice(st, "M_PLUS_1", telemetry=trk)

    while True:
        res = step_until_decision(st, telemetry=trk)
        if isinstance(res, GameOver):
            assert res.cause_fin == CAUSE_REVEIL_GARDIENS
            assert res.tour_fin == 4
            break
        apply_choice(st, res.options[0], telemetry=trk)


# ---------------------------------------------------------------------------
# 3. Furtivité « Chaud vs Calme » aux limites & conservation stricte
# ---------------------------------------------------------------------------


def test_v6_1_furtivite_ratissage_plus_card_and_independence_from_bug_and_reve() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=9301)

    # A) 1 machine en Ratissage permanent + 1 carte Machine révélée sur rayon 0 -> m(0) == 2 (Rive Piège GAGNÉE),
    #    MÊME SI cette carte Machine a été déviée par un Bug ET annulée par un Rêve en 3.2 !
    st = GameState(cfg)
    st.tour = 3
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st.set_tactique_at_rank(5, TILE_R_BASE + 1)  # R1 sur case 6
    st.place_defender_reve_activation(2, 6, FACE_DEFINITIF, def_idx=0)
    st.set_bugs_at_case(5, 1)  # Déviera M=5 -> 6 (R1) !

    # Binôme Rive Piège sur rayon 0 ; binôme Rive Sabotage sur rayon 0 (qui DOIT PERDRE car m(0)==2 !)
    # + binôme Rive Sabotage sur rayon 1 (aucune carte du rayon 1, uniquement Sabotages -> m(1)==0 GAGNÉ !)
    st.place_defender_furtivite(0, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.place_defender_furtivite(1, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st.place_defender_furtivite(0, 1, 0, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_furtivite(1, 1, 0, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_furtivite(3, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_furtivite(2, 1, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)

    st.set_player_hand(0, machine_card_code(0, MACHINE_BULLDOZER), 5, 5, 5, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_parcel_insectes(3, 1, 1)  # Ancre 4.3

    trk = TelemetryTracker()
    st.step = STEP_3_2_REVEAL
    req_bug = step_until_decision(st, telemetry=trk)
    assert isinstance(req_bug, DecisionRequest) and "M_PLUS_1" in req_bug.options
    apply_choice(st, "M_PLUS_1", telemetry=trk)  # Dévie vers 6 -> annulé par R1 !

    req_piege = step_until_decision(st, telemetry=trk)
    assert isinstance(req_piege, DecisionRequest)
    assert req_piege.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1
    assert req_piege.decideur == 0
    assert st.count_mobilized_machines_for_ray(0) == 2
    assert st.count_mobilized_machines_for_ray(1) == 0
    apply_choice(st, 4, telemetry=trk)
    _ = step_until_decision(st, telemetry=trk)

    assert st.get_parcel_piege(0, 4) == PIEGE_ACTIF
    assert st.sabotage_pending_count == 1  # Seul rayon 1 a gagné son Sabotage ; rayon 0 a perdu sa Rive Sabotage !
    ts = trk.summary()
    assert ts.ok_pieges_placed == 1
    assert ts.ok_sabotage_acquired == 1
    assert ts.ok_furt_rive_sabotage_lost == 1

    # B) Migration 4.3 : aucune option FURTIVITE proposée
    st_mig = GameState(cfg)
    st_mig.set_parcel_insectes(3, 2, 1)
    st_mig.step = STEP_4_3_MIGRATION
    req_mig = step_until_decision(st_mig)
    assert isinstance(req_mig, DecisionRequest)
    assert all(opt[0] != "FURTIVITE" for opt in req_mig.options)


# ---------------------------------------------------------------------------
# 4. Gain Charge gelé sur FRAPPE_NON_PAREE & cas limites T3/T6 En avançant
# ---------------------------------------------------------------------------


def test_v6_1_charge_gain_frozen_frappe_non_paree_and_t3_t6_edge_cases() -> None:
    cfg_fnp = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "I"),
        exp_seed=9401,
    )

    # 1) Abatteuse en Charge sur parcelle réelle (0 Arbre, 2 Souches) non parée :
    #    1 frappe réelle non parée -> +1 jeton !
    st = GameState(cfg_fnp)
    st.tour = 1  # T1 = Charge
    st.set_parcel_arbres_souches(0, 1, 0, 2)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE)[0] == 1

    # 2) Garde-fou strict hors-plateau : Devant (T2 en Acte 1 / T5 en Acte 2) lancé depuis last_p (p=4) ->
    #    JAMAIS de jeton !
    for tour_cur, tac_idx in ((2, 2), (6, 5)):
        st_off = GameState(cfg_fnp)
        st_off.tour = tour_cur
        st_off.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
        trk_off = TelemetryTracker()
        resolve_single_machine_attack(
            st_off, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[tac_idx], telemetry=trk_off
        )
        assert st_off.get_machine_tokens(0, MACHINE_ABATTEUSE)[0] == 0
        assert trk_off.summary().charge_gains == 0

    # 3) T3 / T6 (En avançant en Charge) :
    #    3a) Depuis p=1 avec Route en p=2 et Nid + Insectes en p=3 :
    #        frappe SUR_PLACE (0,1), saute le Pont routier (0,2) pour frapper DEVANT (0,3),
    #        avance sur (0,3) en déclenchant Contact Machine-Nid, et plafonne le gain à +1 jeton !
    st_adv = GameState(cfg_fnp)
    st_adv.tour = 1  # T3 = Charge
    st_adv.set_parcel_arbres_souches(0, 2, 0, 0)  # Pont routier en p=2
    st_adv.set_parcel_nid(0, 3, 1, active_ce_tour=False)
    st_adv.set_parcel_insectes(0, 3, 1)  # Seuil p=3 sous T3 = 3 - 1 = 2 > 1 Insecte -> non paré !
    st_adv.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    trk_adv = TelemetryTracker()
    resolve_single_machine_attack(
        st_adv, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3], telemetry=trk_adv
    )
    assert st_adv.get_parcel_arbres(0, 1) == 0  # Frappe SUR_PLACE
    assert st_adv.get_parcel_arbres(0, 3) == 0  # Frappe DEVANT à travers le Pont routier (coupe tous les Arbres)
    assert st_adv.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 3  # Avancée en p=3
    assert st_adv.get_parcel_nid(0, 3)[0] == 0  # Contact Machine-Nid !
    assert st_adv.get_parcel_insectes(0, 3) == 0
    assert st_adv.get_machine_tokens(0, MACHINE_ABATTEUSE)[0] == 1  # Plafonné à +1 !
    assert trk_adv.summary().charge_gains == 1

    #    3b) T6 (Charge en Acte 2, Tour 5) depuis la dernière parcelle p=4 (0 Arbre, 2 Souches) :
    #        SUR_PLACE cible p=4 (réelle), DEVANT hors-plateau ignorée :
    #        - si p=4 porte un Piège autonome -> 0 jeton ;
    #        - si p=4 n'est pas parée -> +1 jeton !
    st_p4_trap = GameState(cfg_fnp)
    st_p4_trap.tour = 5  # Acte 2 : T6 = Charge
    st_p4_trap.set_parcel_arbres_souches(0, 4, 0, 2)
    st_p4_trap.set_parcel_piege(0, 4, PIEGE_ACTIF)
    st_p4_trap.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st_p4_trap, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[6])
    assert st_p4_trap.get_machine_tokens(0, MACHINE_ABATTEUSE)[0] == 0

    st_p4_hit = GameState(cfg_fnp)
    st_p4_hit.tour = 5  # Acte 2 : T6 = Charge
    st_p4_hit.set_parcel_arbres_souches(0, 4, 0, 2)
    st_p4_hit.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st_p4_hit, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[6])
    assert st_p4_hit.get_machine_tokens(0, MACHINE_ABATTEUSE)[0] == 1


# ---------------------------------------------------------------------------
# 5. Campagne Micro de forks causaux v6.1 & déterminisme bit-à-bit B0/B1/B2/B3
# ---------------------------------------------------------------------------


def test_v6_1_causal_forks_manifest_and_deterministic_replays(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import campaigns.digest_builder as db_mod

    # A) Rejeu déterministe strict et mem_debt == 0 sur B0, B1, B2, B3
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "I"),
        exp_seed=9501,
        rep_id=3,
        max_revision_passes=3,
    )
    for runner in (play_game_b0, play_game_b1, play_game_b2):
        s_a = GameState(cfg)
        s_b = GameState(cfg)
        trk_a = TelemetryTracker()
        out_a = runner(s_a, telemetry=trk_a)
        out_b = runner(s_b)
        assert out_a == out_b
        assert s_a.raw_used_bytes() == s_b.raw_used_bytes()
        assert trk_a.summary().mem_debt_score == 0

    s_3a = GameState(cfg)
    s_3b = GameState(cfg)
    trk_3 = TelemetryTracker()
    assert play_game_b3(s_3a, n_determinizations=2, max_candidates=2, telemetry=trk_3) == play_game_b3(
        s_3b, n_determinizations=2, max_candidates=2
    )
    assert s_3a.raw_used_bytes() == s_3b.raw_used_bytes()
    assert trk_3.summary().mem_debt_score == 0

    # B) Validation directe de run_v6_1_causal_forks_on_config + pipeline forks_causalite_v6_1.json
    cf = run_v6_1_causal_forks_on_config(
        cfg, target_tour=2, is_b2=True, n_selection_rollouts=2, n_eval_rollouts=2
    )
    assert cf.has_2_1_anchor is True
    assert cf.mf_2_2 is not None
    assert cf.total_rollouts > 0

    forks_manifest_path = ROOT / "campaigns" / "manifests" / "forks_causalite_v6_1.json"
    assert forks_manifest_path.is_file()
    forks_manifest = json.loads(forks_manifest_path.read_text(encoding="utf-8"))
    full_plan = resolve_manifest_plan(forks_manifest)
    assert full_plan["micro_forks"] is True
    assert full_plan["profil_piste"] == "P4_2233"

    micro_forks: dict[str, Any] = dict(forks_manifest)
    micro_forks["campaign_name"] = "micro_forks_v6_1_unit"
    micro_forks["player_counts"] = [3, 4]
    micro_forks["games_per_configuration"] = 2
    micro_forks["fork_selection_rollouts"] = 1
    micro_forks["fork_eval_rollouts"] = 2
    mf_file = tmp_path / "micro_forks_v6_1_unit.json"
    mf_file.write_text(json.dumps(micro_forks), encoding="utf-8")
    mf_plan = resolve_manifest_plan(micro_forks)

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(mf_file),
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
        manifest=micro_forks,
        plan=mf_plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="local",
        job_name="local-micro-forks-v61",
        tasks=1,
        job_wall_sec=0.5,
    )
    assert "forks" in digest
    fb = digest["forks"]
    assert "mean_delta_v_negociation_2_2" in fb
    assert "causal_v6_1" in fb
    for fk in (
        "anchors_2_1",
        "mean_delta_v_2_1_b2_vs_b0",
        "anchors_2_1_reve",
        "anchors_furt_rive_piege",
        "anchors_furt_rive_sabotage",
        "anchors_4_1_pose_piege",
        "anchors_5_3_eveil",
    ):
        assert fk in fb["causal_v6_1"]
    assert len(fb["by_n_players"]) == 2
