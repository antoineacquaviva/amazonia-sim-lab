"""Tests unitaires v6.1 : châssis unique P4_2233, hiérarchie B0 < B1 < B2, ouverture 2.1 Rêves & Furtivité,
et table croisée by_variant_x_bot_x_n_players.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import run_campaign as rc_mod
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import list_legal_targets
from engine.state import (
    CANONICAL_DOTATION,
    CANONICAL_P_MAX,
    CANONICAL_PROFIL_PISTE,
    LISIERE_CONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    TILE_R_BASE,
    GameConfig,
    GameState,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


def test_v6_1_canonical_chassis_locked_p4_2233() -> None:
    """En v6.1, le socle exécute directement le châssis unique P4_2233 sans commutateurs obsolètes."""
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "E"), exp_seed=6101)
    assert cfg.profil_piste == CANONICAL_PROFIL_PISTE == "P4_2233"
    assert cfg.p_max == CANONICAL_P_MAX == 4
    assert cfg.dotation_arbres == CANONICAL_DOTATION == (2, 2, 3, 3)


def test_v6_1_cross_table_digest_by_variant_x_bot_x_n_players(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Valide validation_socle_v6_1.json (P4_2233) et by_variant_x_bot_x_n_players."""
    import campaigns.digest_builder as db_mod

    manifest_path = ROOT / "campaigns" / "manifests" / "validation_socle_v6_1.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "validation_socle_v6_1"
    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["profil_piste"] == "P4_2233"
    assert all(u["n_animaux_sauvages"] >= 1 for u in plan["units"])
    assert len({u["peuples"] for u in plan["units"]}) == 41

    micro_manifest: dict[str, Any] = dict(manifest)
    micro_manifest["campaign_name"] = "micro_cross_v6_1"
    micro_manifest["player_counts"] = [3, 6]
    micro_manifest["games_per_configuration"] = 2

    micro_file = tmp_path / "micro_cross_v6_1.json"
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
        job_name="local-micro-cross-v61",
        tasks=1,
        job_wall_sec=0.5,
    )

    assert "by_variant_x_bot_x_n_players" in digest
    cross_rows = digest["by_variant_x_bot_x_n_players"]
    assert len(cross_rows) == 6
    combos = {(r["variant_id"], r["bot"], r["n_players"]) for r in cross_rows}
    assert combos == {("BASE", b, n) for b in ("B0", "B1", "B2") for n in (3, 6)}


def test_v6_1_b2_beats_b1_beats_b0_smoke() -> None:
    """Vérifie sur un échantillon apparié Mode 2 (P4_2233) que la hiérarchie B0 < B1 < B2 est respectée."""
    n_games = 18
    sums = {"B0": 0.0, "B1": 0.0, "B2": 0.0}
    for rep in range(n_games):
        n_pl = (3, 4, 5)[rep % 3]
        peuples = (("M", "H", "I"), ("M", "R", "H", "I"), ("M", "R", "O", "H", "I"))[rep % 3]
        cfg = GameConfig(
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

    assert sums["B0"] < sums["B1"] < sums["B2"], f"Hiérarchie violée : {sums}"


def test_v6_1_def1_never_exposes_gardien_pari_even_when_territory_razed() -> None:
    """En v6.1, 2.1 expose Rêves et Furtivité ouverte, mais JAMAIS GARDIEN_PARI (même sous repli rasé)."""
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=6201)
    st = GameState(cfg)
    st.tour = 6
    st.set_gardien_at_case(1, 1, 1)
    st.set_gardien_at_case(4, 2, 1)
    st.set_tactique_at_rank(5, TILE_R_BASE + 1)

    for r in (0, 1, 3):
        for p in range(1, cfg.p_max + 1):
            st.set_parcel_arbres_souches(r, p, 0, 0)
        st.set_machine_pos_status(r, MACHINE_ABATTEUSE, 0, MACHINE_STATUS_RETIRED)
        st.set_machine_pos_status(r, MACHINE_BULLDOZER, 0, MACHINE_STATUS_RETIRED)
    for slot_idx in (0, 1, 6, 7):
        st.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, 2)

    legal_def1 = list_legal_targets(st, 0, is_first_defender=True)
    assert ("REVE_ACTIVATION", 6) in legal_def1
    assert ("FURTIVITE", 2, 0) in legal_def1
    assert ("FURTIVITE", 0, 0) not in legal_def1
    assert all(t[0] != "GARDIEN_PARI" for t in legal_def1)

    assert play_game_b0(st.clone()).tour_fin <= 8
    assert play_game_b1(st.clone()).tour_fin <= 8
    assert play_game_b2(st.clone()).tour_fin <= 8
