"""Tests unitaires v6.0 : variantes Rêves (SAUT, PAS_A_PAS, SAUT_MAX_1_PAR_TOUR), B2 Acte 1 & calibration_sommeil_v6_0."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import run_campaign as rc_mod
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import DEC_CHOIX_REVE_3_2, apply_choice, step_until_decision
from engine.primitives import DecisionRequest, prim_permutation_piste
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    REVE_ADVANCE_MODES,
    STEP_3_2_REVEAL,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


def test_v6_0_reve_advance_mode_pas_a_pas() -> None:
    """PAS_A_PAS : avance uniquement d'1 case adjacente libre à gauche ; sinon seul BLOQUER est proposé."""
    assert REVE_ADVANCE_MODES == ("SAUT", "PAS_A_PAS", "SAUT_MAX_1_PAR_TOUR")

    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        reve_advance_mode="PAS_A_PAS",
        exp_seed=6101,
    )

    # 1) Case adjacente libre à gauche (R3 en case 6, R1 en case 4 -> case 5 libre) :
    #    AVANCER déplace R3 uniquement en case 5 (et NON en case 3 par saut !).
    st = GameState(cfg)
    st.tour = 2
    st.set_tactique_at_rank(3, TILE_R_BASE + 1)  # R1 en case 4
    st.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 (H = siège 2) en case 6
    st.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_parcel_insectes(3, 1, 1)  # Ancre de suspension 4.3

    trk = TelemetryTracker()
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st, telemetry=trk)
    assert isinstance(req, DecisionRequest) and req.decision_type == DEC_CHOIX_REVE_3_2
    assert req.options == ("BLOQUER", "AVANCER")
    assert req.context["can_advance"] is True
    assert req.context["dest_case"] == 5

    apply_choice(st, "AVANCER", telemetry=trk)
    _ = step_until_decision(st, telemetry=trk)

    assert st.get_tactique_at_rank(4) == TILE_R_BASE + 3  # R3 avancé d'1 seule case (case 5)
    assert st.get_tactique_at_rank(3) == TILE_R_BASE + 1  # R1 toujours en case 4
    assert st.get_tactique_at_rank(2) == 3  # Case 3 restée T3 !
    assert st.get_tactique_at_rank(5) == 6  # Case 6 restaurée en T6
    assert st.get_player_hand(0)[4] == 6  # Machine non annulée

    # 2) Case adjacente à gauche occupée par un autre Rêve (R1 en case 5, R3 en case 6, cases 1..4 libres) :
    #    sous PAS_A_PAS, R3 ne peut PAS sauter par-dessus R1 -> seul BLOQUER est possible !
    st_blk = GameState(cfg)
    st_blk.tour = 2
    st_blk.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 en case 5 (bloque la case adjacente !)
    st_blk.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 en case 6
    st_blk.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st_blk.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_blk.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st_blk.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st_blk.set_parcel_insectes(3, 1, 1)

    assert prim_permutation_piste(st_blk, "ADVANCE_REVE_LEFT", rank_a=5) is False

    st_blk.step = STEP_3_2_REVEAL
    req_blocked = step_until_decision(st_blk)
    assert isinstance(req_blocked, DecisionRequest) and req_blocked.decision_type == DEC_CHOIX_REVE_3_2
    assert req_blocked.options == ("BLOQUER",)
    assert req_blocked.context["can_advance"] is False
    assert req_blocked.context["dest_case"] is None

    apply_choice(st_blk, "BLOQUER")
    _ = step_until_decision(st_blk)
    assert st_blk.get_player_hand(0)[4] == 0  # Machine annulée par BLOQUER
    assert st_blk.get_tactique_at_rank(5) == TILE_R_BASE + 3  # R3 immobile en case 6

    # 3) Cascade gauche -> droite dans le même tour en PAS_A_PAS (R1 en case 5 et R3 en case 6 tous deux actifs) :
    #    R1 (plus proche du Sommeil) décide en 1er ; s'il avance en case 4, la case 5 se libère et R3 peut avancer !
    st_cas = GameState(cfg)
    st_cas.tour = 2
    st_cas.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 en case 5
    st_cas.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 en case 6
    st_cas.place_defender_reve_activation(0, 5, FACE_DEFINITIF)
    st_cas.place_defender_reve_activation(1, 6, FACE_DEFINITIF)
    st_cas.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_cas.set_machine_pos_status(1, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st_cas.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)
    st_cas.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st_cas.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st_cas.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st_cas.set_parcel_insectes(3, 1, 1)

    st_cas.step = STEP_3_2_REVEAL
    req_first = step_until_decision(st_cas)
    assert isinstance(req_first, DecisionRequest) and req_first.decision_type == DEC_CHOIX_REVE_3_2
    assert req_first.context["case"] == 5
    assert req_first.options == ("BLOQUER", "AVANCER")

    # Clone témoin où R1 choisit BLOQUER -> R3 reste bloqué derrière R1 !
    st_cas_hold = st_cas.clone()
    apply_choice(st_cas_hold, "BLOQUER")
    req_second_hold = step_until_decision(st_cas_hold)
    assert isinstance(req_second_hold, DecisionRequest) and req_second_hold.decision_type == DEC_CHOIX_REVE_3_2
    assert req_second_hold.context["case"] == 6
    assert req_second_hold.options == ("BLOQUER",)

    # Branche où R1 choisit AVANCER -> R1 libère la case 5 -> R3 peut à son tour AVANCER en case 5 !
    apply_choice(st_cas, "AVANCER")
    req_second_adv = step_until_decision(st_cas)
    assert isinstance(req_second_adv, DecisionRequest) and req_second_adv.decision_type == DEC_CHOIX_REVE_3_2
    assert req_second_adv.context["case"] == 6
    assert req_second_adv.options == ("BLOQUER", "AVANCER")
    assert req_second_adv.context["dest_case"] == 5
    apply_choice(st_cas, "AVANCER")
    _ = step_until_decision(st_cas)
    assert st_cas.get_tactique_at_rank(3) == TILE_R_BASE + 1  # R1 en case 4
    assert st_cas.get_tactique_at_rank(4) == TILE_R_BASE + 3  # R3 en case 5
    assert st_cas.get_tactique_at_rank(5) == 6


def test_v6_0_reve_advance_mode_saut_max_1_par_tour() -> None:
    """SAUT_MAX_1_PAR_TOUR : saut à la 1re case libre à gauche, max 1 AVANCER/tour, priorité au Rêve le plus à gauche."""
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        reve_advance_mode="SAUT_MAX_1_PAR_TOUR",
        exp_seed=6102,
    )

    # R1 en case 5 (plus à gauche / proche du Sommeil) et R3 en case 6, cases 1..4 libres
    st = GameState(cfg)
    st.tour = 2
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 en case 5
    st.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 en case 6
    st.place_defender_reve_activation(0, 5, FACE_DEFINITIF)
    st.place_defender_reve_activation(1, 6, FACE_DEFINITIF)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(1, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_BULLDOZER), 6, 6, 6, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_parcel_insectes(3, 1, 1)

    st.step = STEP_3_2_REVEAL
    req_left = step_until_decision(st)
    assert isinstance(req_left, DecisionRequest) and req_left.decision_type == DEC_CHOIX_REVE_3_2
    # Priorité stricte au Rêve le plus à gauche (case 5 avant case 6)
    assert req_left.context["case"] == 5
    assert req_left.options == ("BLOQUER", "AVANCER")
    assert req_left.context["dest_case"] == 4

    # Clone B : si le Rêve de gauche choisit BLOQUER, le quota n'est PAS consommé -> R3 peut sauter par-dessus R1 en case 4 !
    st_b = st.clone()
    trk_b = TelemetryTracker()
    apply_choice(st_b, "BLOQUER", telemetry=trk_b)
    req_right_b = step_until_decision(st_b, telemetry=trk_b)
    assert isinstance(req_right_b, DecisionRequest) and req_right_b.decision_type == DEC_CHOIX_REVE_3_2
    assert req_right_b.context["case"] == 6
    assert req_right_b.options == ("BLOQUER", "AVANCER")
    assert req_right_b.context["dest_case"] == 4  # Saute par-dessus R1 resté en case 5 !
    apply_choice(st_b, "AVANCER", telemetry=trk_b)
    _ = step_until_decision(st_b, telemetry=trk_b)
    assert st_b.get_tactique_at_rank(3) == TILE_R_BASE + 3  # R3 a sauté en case 4
    assert st_b.get_tactique_at_rank(4) == TILE_R_BASE + 1  # R1 resté en case 5
    assert trk_b.summary().reves_choice_block == 1
    assert trk_b.summary().reves_choice_advance == 1

    # Branche A : le Rêve de gauche (R1) choisit AVANCER -> R3 est forcé à BLOQUER ce tour-ci !
    trk_a = TelemetryTracker()
    apply_choice(st, "AVANCER", telemetry=trk_a)
    req_right_a = step_until_decision(st, telemetry=trk_a)
    assert isinstance(req_right_a, DecisionRequest) and req_right_a.decision_type == DEC_CHOIX_REVE_3_2
    assert req_right_a.context["case"] == 6
    assert req_right_a.options == ("BLOQUER",)
    assert req_right_a.context["can_advance"] is False
    assert st.reve_advances_this_turn == 1

    apply_choice(st, "BLOQUER", telemetry=trk_a)
    _ = step_until_decision(st, telemetry=trk_a)
    assert st.get_tactique_at_rank(3) == TILE_R_BASE + 1  # R1 avancé en case 4
    assert st.get_tactique_at_rank(5) == TILE_R_BASE + 3  # R3 resté en case 6
    assert st.get_player_hand(1)[4] == 0  # Machine de R3 bien annulée
    assert trk_a.summary().reves_choice_advance == 1
    assert trk_a.summary().reves_choice_block == 1

    # Fin de tour 6.2 : remise à zéro du compteur -> au tour suivant, un Rêve peut à nouveau avancer
    st.cleanup_end_of_turn_6_2()
    assert st.reve_advances_this_turn == 0
    assert st.get_reve_advance_dest_rank(5, check_turn_cap=True) == 4


def test_v6_0_calibration_sommeil_manifest_and_cross_table_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Valide calibration_sommeil_v6_0.json et la table croisée by_variant_x_bot_x_n_players dans le digest."""
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_sommeil_v6_0.json"
    assert manifest_path.is_file(), "campaigns/manifests/calibration_sommeil_v6_0.json manquant"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "calibration_sommeil_v6_0"
    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert [v["reve_advance_mode"] for v in plan["profile_variants"]] == [
        "SAUT",
        "PAS_A_PAS",
        "SAUT_MAX_1_PAR_TOUR",
    ]
    assert [v["variant_id"] for v in plan["profile_variants"]] == [
        "ADV=SAUT",
        "ADV=PAS_A_PAS",
        "ADV=SAUT_MAX_1_PAR_TOUR",
    ]
    # 3 variantes * 3 bots * 4 tailles * 6 châssis = 216 configurations ; 41 tables uniques A >= 1
    assert plan["total_configurations"] == 216
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert len({u["peuples"] for u in plan["units"]}) == 41

    # Micro-run sur 2 variantes x 3 bots x 2 tailles (N=3, 6) pour vérifier by_variant_x_bot_x_n_players
    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_calibration_sommeil_v6_0"
    micro_manifest["player_counts"] = [3, 6]
    micro_manifest["games_per_configuration"] = 2
    micro_manifest["reve_advance_modes"] = ["SAUT", "PAS_A_PAS"]
    micro_manifest["chassis_plan"] = {
        "varying_axes": [],
        "fixed_axes": {"Profil_Piste": "P4_2233"},
    }

    micro_file = tmp_path / "micro_calibration_sommeil_v6_0.json"
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
        job_name="local-micro-sommeil-v6",
        tasks=1,
        job_wall_sec=0.5,
    )

    assert "by_variant_x_bot_x_n_players" in digest
    cross_rows = digest["by_variant_x_bot_x_n_players"]
    # 2 variantes * 3 bots * 2 tailles = 12 lignes exactes
    assert len(cross_rows) == 12

    required_cols = (
        "variant_id",
        "bot",
        "n_players",
        "n_games",
        "mean_ratio_arbres",
        "table_cvar20_ratio",
        "pct_tour_8",
        "pct_reve_rang_1",
        "pct_reveil_gardiens",
        "count_reveil_attempts",
        "mean_power_tokens_end_act1",
        "count_furtivite_1_rive_turns",
        "count_furtivite_2_rives_turns",
    )
    for row in cross_rows:
        for col in required_cols:
            assert col in row, f"Colonne manquante dans by_variant_x_bot_x_n_players : {col}"

    combos = {(r["variant_id"], r["bot"], r["n_players"]) for r in cross_rows}
    assert combos == {
        (v, b, n)
        for v in ("ADV=SAUT", "ADV=PAS_A_PAS")
        for b in ("B0", "B1", "B2")
        for n in (3, 6)
    }


def test_v6_0_b2_beats_b1_beats_b0_smoke() -> None:
    """Vérifie sur un échantillon apparié Mode 2 que la hiérarchie B0 < B1 < B2 est restaurée."""
    n_games = 18
    sums = {"B0": 0.0, "B1": 0.0, "B2": 0.0}
    f2_b2 = 0
    for rep in range(n_games):
        n_pl = (3, 4, 5)[rep % 3]
        peuples = (("M", "H", "I"), ("M", "R", "H", "I"), ("M", "R", "O", "H", "I"))[rep % 3]
        cfg = GameConfig.from_chassis_index(
            rep % 6,
            n_players=n_pl,
            mode=2,
            peuples=peuples,
            exp_seed=6199,
            rep_id=rep,
            max_revision_passes=3,
        )
        sums["B0"] += play_game_b0(GameState(cfg)).ratio_arbres
        sums["B1"] += play_game_b1(GameState(cfg)).ratio_arbres
        trk_b2 = TelemetryTracker()
        sums["B2"] += play_game_b2(GameState(cfg), telemetry=trk_b2).ratio_arbres
        f2_b2 += trk_b2.summary().furtivite_2_rives_turns

    assert sums["B0"] < sums["B1"] < sums["B2"], f"Hiérarchie violée : {sums}"
    assert f2_b2 <= 2
