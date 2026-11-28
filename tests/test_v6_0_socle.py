"""Tests unitaires de non-régression du socle v6.x (Réglette 2 Actes, 0 Repousse Finale,
Rêves en blocage pur + Mode 4, Furtivité par rayon, télémétrie DuckDB & hiérarchie des bots).
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
    DEC_CHOIX_CIBLE_REVE_3_2,
    DEC_POSE_PIEGE_FURTIVITE_4_1,
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
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
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


def test_v6_furtivite_free_placement_and_1_vs_2_rives_execution() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"), exp_seed=6001)
    st = GameState(cfg)
    st.tour = 2
    st.paravents_ouverts = True

    # --- Cas A : 1 pion seul sur Rive Piège + 1 pion seul sur Rive Sabotage -> AUCUN glissement, AUCUNE action ---
    st.place_defender_furtivite(seat=0, def_idx=0, ray=0, rive=FURT_RIVE_PIEGE, face=FACE_DEFINITIF)
    st.place_defender_furtivite(seat=1, def_idx=1, ray=0, rive=FURT_RIVE_SABOTAGE, face=FACE_REFLEXION)
    assert st.get_furtivite_slots(0, 1) == (FACE_DEFINITIF, 0, FACE_REFLEXION, 0)
    assert st.get_furtivite_nb_def_rive(0, 1, 0) == 1
    assert st.get_furtivite_nb_def_rive(0, 1, 1) == 1
    obs = st.get_observation(2)
    assert obs.furtivite_ray_rive_defs(0, 0) == 1
    assert obs.furtivite_ray_rive_defs(0, 1) == 1

    st.set_parcel_nid(3, 2, 1)
    st.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)
    st.step = STEP_4_1_FURTIVITE
    trk_a = TelemetryTracker()
    req_a = step_until_decision(st, telemetry=trk_a)
    assert isinstance(req_a, DecisionRequest)
    assert all(st.get_parcel_piege(0, p) == PIEGE_AUCUN for p in range(1, 5))
    assert st.sabotage_pending_count == 0
    assert trk_a.summary().ok_furt_orphan_pawns == 2

    # --- Cas B : 1 binôme complet Rive Piège (m(0)=2) + 1 pion seul Rive Sabotage -> Rive Piège gagnée ---
    st_b = GameState(cfg)
    st_b.tour = 2
    st_b.paravents_ouverts = True
    st_b.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 1, 1, 1)
    st_b.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 2, 2, 2, 2)
    st_b.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_b.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_b.place_defender_furtivite(seat=0, def_idx=0, ray=0, rive=FURT_RIVE_PIEGE, face=FACE_DEFINITIF)
    st_b.place_defender_furtivite(seat=1, def_idx=1, ray=0, rive=FURT_RIVE_SABOTAGE, face=FACE_REFLEXION)
    st_b.place_defender_furtivite(seat=2, def_idx=1, ray=0, rive=FURT_RIVE_PIEGE, face=FACE_DEFINITIF)
    legal_s3 = list_legal_targets(st_b, seat=3, is_first_defender=False)
    assert ("FURTIVITE", 0, FURT_RIVE_PIEGE) not in legal_s3
    assert ("FURTIVITE", 0, FURT_RIVE_SABOTAGE) in legal_s3

    st_b.set_parcel_nid(3, 2, 1)
    st_b.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)
    st_b.step = STEP_4_1_FURTIVITE
    trk_b = TelemetryTracker()
    req_b = step_until_decision(st_b, telemetry=trk_b)
    assert isinstance(req_b, DecisionRequest) and req_b.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1
    assert req_b.decideur == 0
    apply_choice(st_b, 2, telemetry=trk_b)
    _ = step_until_decision(st_b, telemetry=trk_b)
    assert st_b.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert trk_b.summary().furtivite_1_rive_turns == 1

    # --- Cas C : Deux rayons différents gagnent simultanément (Rive Piège sur r=0 et Rive Sabotage sur r=1) ---
    st2 = GameState(cfg)
    st2.tour = 2
    st2.paravents_ouverts = True
    st2.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 1, 1, 1)
    st2.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 2, 2, 2, 2)
    st2.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st2.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st2.place_defender_furtivite(0, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st2.place_defender_furtivite(2, 1, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st2.place_defender_furtivite(1, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st2.place_defender_furtivite(3, 1, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st2.set_parcel_nid(3, 2, 1)
    st2.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)
    st2.step = STEP_4_1_FURTIVITE
    trk_c = TelemetryTracker()
    sab_before = st2.sabotage_pending_count
    req_c = step_until_decision(st2, telemetry=trk_c)
    assert isinstance(req_c, DecisionRequest) and req_c.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1
    apply_choice(st2, 1, telemetry=trk_c)
    _ = step_until_decision(st2, telemetry=trk_c)
    assert st2.get_parcel_piege(0, 1) == PIEGE_ACTIF
    assert st2.sabotage_pending_count == sab_before + 1


def test_v6_zero_repousse_finale_and_abatteuse_ratissage_stump_exception() -> None:
    cfg_std = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=6002)
    st = GameState(cfg_std)
    st.tour = 8
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
    assert trk.summary().da_arbres_repousse_finale == 0

    # En v6.1 scellé : l'Abatteuse coupe tous les Arbres debout et ne touche JAMAIS aux Souches
    cfg_arr = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
        exp_seed=6003,
    )
    st_arr = GameState(cfg_arr)
    st_arr.tour = 3
    st_arr.set_parcel_arbres_souches(0, 4, 0, 1)
    st_arr.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st_arr.set_machine_pos_status(0, MACHINE_BULLDOZER, 4, MACHINE_STATUS_RATISSAGE)

    trk_arr = TelemetryTracker()
    resolve_single_machine_attack(
        st_arr, 0, MACHINE_ABATTEUSE, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True, telemetry=trk_arr
    )
    assert st_arr.is_route_forestiere(0, 4) is False
    assert st_arr.get_parcel_souches(0, 4) == 1
    assert trk_arr.summary().ok_abatteuse_ratissage_0_arbre == 1

    # Sur une parcelle à 3 Arbres, l'Abatteuse coupe les 3 Arbres d'un seul coup !
    st_arr.set_parcel_arbres_souches(1, 3, 3, 0)
    st_arr.set_machine_pos_status(1, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st_arr, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st_arr.get_parcel_arbres(1, 3) == 0
    assert st_arr.get_parcel_souches(1, 3) == 3


def test_v6_reves_block_only_in_socle_step5_execution_and_mode4_power() -> None:
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=6004)
    st_blk = GameState(cfg)
    st_blk.tour = 2
    st_blk.set_gardien_at_case(4, 1, face=1)
    st_blk.place_defender_gardien_pari(0, 4, FACE_DEFINITIF)
    st_blk.set_tactique_at_rank(5, TILE_R_BASE + 3)
    st_blk.place_defender_reve_activation(1, 6, FACE_DEFINITIF, def_idx=0)  # 1er Défenseur (2.1) sur R3

    st_blk.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_blk.set_machine_pos_status(1, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    st_blk.set_machine_tokens(1, MACHINE_BULLDOZER, rouges=2, bleus=0)
    st_blk.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st_blk.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_blk.set_player_hand(2, 0, 0, 0, 0, 0)
    st_blk.set_player_hand(3, 0, 0, 0, 0, 0)
    st_blk.set_parcel_nid(3, 2, 1)  # Ancre 4.2 (I présent)
    st_blk.place_defender_foret(3, 0, 3, 2, FACE_DEFINITIF)

    trk_blk = TelemetryTracker()
    st_blk.step = STEP_3_2_REVEAL
    req_choice = step_until_decision(st_blk, telemetry=trk_blk)
    assert isinstance(req_choice, DecisionRequest)
    assert req_choice.decision_type == DEC_CHOIX_CIBLE_REVE_3_2
    assert (1,) in req_choice.options
    apply_choice(st_blk, (1,), telemetry=trk_blk)
    req_after_blk = step_until_decision(st_blk, telemetry=trk_blk)
    assert isinstance(req_after_blk, DecisionRequest)

    # Blocage v6.2 : propriétaire choisit siège 1 annulée, siège 0 liée à T6, R3 immobile, 4. Rêve allumé
    assert st_blk.get_player_hand(1)[4] == 0
    assert st_blk.get_player_hand(0)[4] == 6
    assert st_blk.get_tactique_at_rank(5) == TILE_R_BASE + 3
    assert st_blk.count_gardien_pari_consumed_at_case(4) == 1
    assert trk_blk.summary().da_reve_annulation == 1

    arbres_01_before = st_blk.get_parcel_arbres(0, 1)
    arbres_02_before = st_blk.get_parcel_arbres(0, 2)
    arbres_13_before = st_blk.get_parcel_arbres(1, 3)
    st_blk._continuation.clear()
    st_blk.step = STEP_5_1_TACTIQUES
    _ = step_until_decision(st_blk, telemetry=trk_blk)
    assert st_blk.get_parcel_arbres(0, 1) == arbres_01_before - 2
    assert st_blk.get_parcel_arbres(0, 2) == arbres_02_before - 2
    assert st_blk.get_machine_pos_status(0, MACHINE_ABATTEUSE)[0] == 2
    assert st_blk.get_parcel_arbres(1, 3) == arbres_13_before

    # Mode 4 : pouvoir propre de R10:A (altère la machine annulée + pose 1 Insecte) exécuté en 3.2
    cfg_m4 = GameConfig(n_players=4, mode=4, peuples=("M", "R", "E", "I"), exp_seed=6005)
    st_m4 = GameState(cfg_m4)
    st_m4.tour = 2
    st_m4.set_tactique_at_rank(5, TILE_R_BASE + 10)
    st_m4.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_m4.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st_m4.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_m4.set_player_hand(s, 0, 0, 0, 0, 0)
    bugs_before = st_m4.get_bugs_at_case(6)
    st_m4.step = STEP_3_2_REVEAL
    _run_step_3_2(st_m4)
    while st_m4._continuation:
        rem = _advance_continuation(st_m4)
        if isinstance(rem, DecisionRequest):
            ek = rem.context.get("effect_kind", "")
            if ek == "R10_BRANCH":
                apply_choice(st_m4, ("SPECTRAL_BUG", 6))
            elif ek == "R10_SPECTRAL_ALTER":
                apply_choice(st_m4, ("ALTERER", 0, MACHINE_ABATTEUSE))
            else:
                apply_choice(st_m4, rem.options[0])
    assert st_m4.get_bugs_at_case(6) == bugs_before + 1
    assert st_m4.has_machine_alteration(0, MACHINE_ABATTEUSE) is True

    st_full = GameState(cfg)
    st_full.set_tactique_at_rank(0, TILE_R_BASE + 1)
    st_full.set_tactique_at_rank(1, TILE_R_BASE + 2)
    assert prim_permutation_piste(st_full, "ADVANCE_REVE_LEFT", rank_a=1) is False


def test_v6_reglette_face_a_b_charge_assaut_and_ratissage_permanent_assaut() -> None:
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

    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=6006)
    st = GameState(cfg)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=3, bleus=0)
    st.tour = 4
    assert is_tactique_charge(1, st.tour) is True
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[1]) == 2
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[4]) == 5

    st.tour = 5
    assert is_tactique_charge(1, st.tour) is False
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[1]) == 5
    assert compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 1, TACTIQUES_SPEC[4]) == 2

    st_rat = GameState(cfg)
    st_rat.tour = 2
    st_rat.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    # v6.2 (INV-12) : 0 bonus imprimé virtuel ; 3 jetons rouges physiques (dont +1 reçu en 6.3) -> Seuil = 3 + 3 = 6
    st_rat.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=3, bleus=0)
    assert (
        compute_parade_seuil(
            st_rat, 0, MACHINE_ABATTEUSE, 4, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
        )
        == 6
    )
    st_rat.set_parcel_defenseurs(0, 4, 5)
    trk_rat = TelemetryTracker()
    st_rat.step = STEP_5_2_RATISSAGE
    _ = step_until_decision(st_rat, telemetry=trk_rat)
    assert st_rat.get_parcel_arbres(0, 4) == 0
    assert st_rat.get_machine_tokens(0, MACHINE_ABATTEUSE) == (3, 0)
    assert trk_rat.summary().charge_gains == 0


def test_v6_1_manifest_plan_and_duckdb_digest_metrics(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "validation_socle_v6_1.json"
    assert manifest_path.is_file(), "campaigns/manifests/validation_socle_v6_1.json manquant"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "validation_socle_v6_1"
    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["profil_piste"] == "P4_2233"
    assert plan["total_configurations"] == 12
    assert plan["total_games"] == 6_840
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert len({frozenset(u["peuples"]) for u in plan["units"]}) == 41
    assert len({u["peuples"] for u in plan["units"] if u["n_players"] == 6}) >= 20

    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_validation_socle_v6_1"
    micro_manifest["player_counts"] = [4]
    micro_manifest["games_per_configuration"] = 6
    micro_file = tmp_path / "micro_validation_socle_v6_1.json"
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
        job_name="local-micro-v61",
        tasks=1,
        job_wall_sec=0.5,
    )

    assert digest["active_core_rules"]["version"] == "6.4.0"
    assert digest["active_core_rules"]["chassis_canonique"]["profil_piste"] == "P4_2233"
    totals = digest["totals"]
    assert totals["count_charge_gains"] > 0
    assert totals["mean_power_tokens_end_game"] > 0.0
    assert "defense_attribution" in digest
    assert digest["defense_attribution"]["arbres_repousse_finale"] >= 0


def test_v6_bots_progression_smoke_b0_b1_b2() -> None:
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

    assert ratios["B1"] > ratios["B0"]
    assert ratios["B2"] > ratios["B0"]
