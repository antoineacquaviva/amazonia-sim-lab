"""Tests unitaires v6.0 : verrouillage ADV=SAUT, B2 Acte 1, repli 2.1 & table croisée by_variant_x_bot_x_n_players."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import run_campaign as rc_mod
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import (
    DEC_CHOIX_REVE_3_2,
    apply_choice,
    list_legal_targets,
    step_until_decision,
)
from engine.primitives import DecisionRequest
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    LISIERE_CONSTRUCTED,
    MACHINE_ABATTEUSE,
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


def test_v6_0_reve_advance_mode_locked_to_saut() -> None:
    """ADV=SAUT est figé comme règle unique de déplacement des Rêves ; PAS_A_PAS et SAUT_MAX_1_PAR_TOUR sont rejetés."""
    assert REVE_ADVANCE_MODES == ("SAUT",)

    for legacy_mode in ("PAS_A_PAS", "SAUT_MAX_1_PAR_TOUR", "CLEAR_RANK_ONLY"):
        with pytest.raises(AssertionError, match="reve_advance_mode"):
            GameConfig(
                n_players=4,
                mode=2,
                peuples=("M", "R", "H", "E"),
                reve_advance_mode=legacy_mode,
                exp_seed=6101,
            )

    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "H", "E"),
        reve_advance_mode="SAUT",
        exp_seed=6102,
    )
    # R1 en case 5 et R3 en case 6 : sous SAUT, R3 saute par-dessus R1 directement en case 4 !
    st = GameState(cfg)
    st.tour = 2
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 en case 5
    st.set_tactique_at_rank(5, TILE_R_BASE + 3)  # R3 en case 6
    st.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_parcel_insectes(3, 1, 1)

    trk = TelemetryTracker()
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st, telemetry=trk)
    assert isinstance(req, DecisionRequest) and req.decision_type == DEC_CHOIX_REVE_3_2
    assert req.options == ("BLOQUER", "AVANCER")
    assert req.context["dest_case"] == 4

    apply_choice(st, "AVANCER", telemetry=trk)
    _ = step_until_decision(st, telemetry=trk)
    assert st.get_tactique_at_rank(3) == TILE_R_BASE + 3  # R3 a sauté en case 4
    assert st.get_tactique_at_rank(4) == TILE_R_BASE + 1  # R1 resté en case 5
    assert st.get_tactique_at_rank(5) == 6


def test_v6_0_calibration_sommeil_manifest_and_cross_table_digest(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Valide calibration_sommeil_v6_0.json figé (SAUT + P4_2233) et by_variant_x_bot_x_n_players."""
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "calibration_sommeil_v6_0.json"
    assert manifest_path.is_file(), "campaigns/manifests/calibration_sommeil_v6_0.json manquant"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "calibration_sommeil_v6_0"
    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["chassis_ids"] == (0,)
    assert [v["reve_advance_mode"] for v in plan["profile_variants"]] == ["SAUT"]
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert len({u["peuples"] for u in plan["units"]}) == 41

    # Vérifier le rejet explicite de PAS_A_PAS dans resolve_manifest_plan
    bad_manifest = dict(manifest)
    bad_manifest["reve_advance_modes"] = ["SAUT", "PAS_A_PAS"]
    with pytest.raises(ValueError, match="reve_advance_mode"):
        resolve_manifest_plan(bad_manifest)

    # Micro-run sur 2 variantes REVE_TRIG x 3 bots x 2 tailles (N=3, 6) pour vérifier by_variant_x_bot_x_n_players
    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_calibration_sommeil_v6_0"
    micro_manifest["player_counts"] = [3, 6]
    micro_manifest["games_per_configuration"] = 2
    micro_manifest["reve_5_trigger_modes"] = ["PASSIF", "ACTIF"]

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
        for v in ("REVE_TRIG=PASSIF", "REVE_TRIG=ACTIF")
        for b in ("B0", "B1", "B2")
        for n in (3, 6)
    }


def test_v6_0_b2_beats_b1_beats_b0_smoke() -> None:
    """Vérifie sur un échantillon apparié Mode 2 (P4_2233) que la hiérarchie B0 < B1 < B2 est respectée."""
    n_games = 18
    sums = {"B0": 0.0, "B1": 0.0, "B2": 0.0}
    f2_b2 = 0
    for rep in range(n_games):
        n_pl = (3, 4, 5)[rep % 3]
        peuples = (("M", "H", "I"), ("M", "R", "H", "I"), ("M", "R", "O", "H", "I"))[rep % 3]
        cfg = GameConfig.from_chassis_index(
            0,
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
    assert f2_b2 <= 3


def test_v6_0_def1_local_razed_fallback_never_exposes_gardien_pari_or_reve_activation() -> None:
    """Non-régression 2.1 Mode 2 : si le territoire local d'un siège est 100 % rasé/construit,
    le repli global du 1er Défenseur n'expose jamais GARDIEN_PARI ni REVE_ACTIVATION.
    """
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=6201)
    st = GameState(cfg)
    st.tour = 6
    st.set_gardien_at_case(1, 1, 1)
    st.set_gardien_at_case(4, 2, 1)
    st.set_tactique_at_rank(5, TILE_R_BASE + 1)

    for r in (0, 1, 3):
        for p in range(1, cfg.p_max + 1):
            st.set_parcel_arbres_souches(r, p, 0, 0)
    for slot_idx in (0, 1, 6, 7):
        st.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, 2)

    legal_def1_partial = list_legal_targets(st, 0, is_first_defender=True)
    assert len(legal_def1_partial) > 0
    assert all(t[0] not in ("GARDIEN_PARI", "REVE_ACTIVATION") for t in legal_def1_partial)
    assert ("FORET", 2, 1) in legal_def1_partial

    assert play_game_b0(st.clone()).tour_fin <= 8
    assert play_game_b1(st.clone()).tour_fin <= 8
    assert play_game_b2(st.clone()).tour_fin <= 8

    for p in range(1, cfg.p_max + 1):
        st.set_parcel_arbres_souches(2, p, 0, 0)
    for slot_idx in range(2 * cfg.n_players):
        st.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, 2)

    assert list_legal_targets(st, 0, is_first_defender=True) == ()
    legal_def2_full = list_legal_targets(st, 0, is_first_defender=False)
    assert ("GARDIEN_PARI", 1) in legal_def2_full
    assert ("REVE_ACTIVATION", 6) in legal_def2_full

    assert play_game_b0(st.clone()).tour_fin <= 8
    assert play_game_b1(st.clone()).tour_fin <= 8
    assert play_game_b2(st.clone()).tour_fin <= 8
