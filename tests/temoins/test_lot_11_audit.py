"""Lot 11 — Audit automatisé 100/100 du catalogue Studio v5.3.1 et validation Mode 3."""

from __future__ import annotations

import json
from pathlib import Path

from bots.bot_b0 import play_game_b0
from engine.core_engine import ensure_builtin_migration_registered
from engine.effects import load_all_effects
from engine.effects.registry import (
    clear_tile_registry,
    get_tile_registration,
    list_registered_tiles,
)
from engine.primitives import GameOver
from engine.state import STEP_GAME_OVER, GameConfig, GameState

ROOT = Path(__file__).resolve().parent.parent.parent
SPEC_PATH = ROOT / "data" / "spec_bundle_v5_3_1.json"
MODE3_REF_PATH = ROOT / "engine" / "effects" / "mode3_reference.json"


def _load_spec_pairs() -> set[tuple[str, str]]:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    ct = spec["catalogue_tuiles"]
    return {(slot, prof) for slot, meta in ct.items() for prof in meta["profils"]}


def test_lot_11_catalogue_100_pour_100_couverture() -> None:
    """Vérifie la couverture exacte 100/100 contre data/spec_bundle_v5_3_1.json."""
    clear_tile_registry()
    ensure_builtin_migration_registered()
    load_all_effects()

    registered = set(list_registered_tiles())
    expected = _load_spec_pairs()

    assert len(expected) == 100
    assert registered == expected, (
        f"Manquants={sorted(expected - registered)} | Extra={sorted(registered - expected)}"
    )

    for slot_id, prof in sorted(expected):
        reg = get_tile_registration(slot_id, prof)
        assert reg is not None, f"{slot_id}:{prof} absent du registre"
        assert len(reg.hooks) >= 1, f"{slot_id}:{prof} sans hook"
        assert callable(reg.handler), f"{slot_id}:{prof} handler non appelable"


def test_lot_11_mode3_reference_json_valide() -> None:
    """Vérifie l'intégrité complète de engine/effects/mode3_reference.json (32 sélections)."""
    ensure_builtin_migration_registered()
    load_all_effects()
    spec_pairs = _load_spec_pairs()

    ref = json.loads(MODE3_REF_PATH.read_text(encoding="utf-8"))
    assert ref["schema_version"] == "5.3.1"
    selections = ref["selections"]
    assert len(selections) == 32

    for slot_id, meta in selections.items():
        prof = meta["profile"]
        assert (slot_id, prof) in spec_pairs, f"{slot_id}:{prof} absent du spec_bundle"
        assert get_tile_registration(slot_id, prof) is not None, f"{slot_id}:{prof} non enregistré"


def test_lot_11_mode3_reference_simulation_bout_en_bout() -> None:
    """Joue une partie complète Mode 3 sur la sélection de référence 32 tuiles."""
    ensure_builtin_migration_registered()
    load_all_effects()

    ref = json.loads(MODE3_REF_PATH.read_text(encoding="utf-8"))
    tile_profiles = tuple((slot_id, meta["profile"]) for slot_id, meta in ref["selections"].items())
    cfg = GameConfig(n_players=4, mode=3, tile_profiles=tile_profiles)
    state = GameState(cfg)
    go = play_game_b0(state, max_steps=2000)

    assert isinstance(go, GameOver)
    assert state.step == STEP_GAME_OVER


def test_lot_11_tous_modules_temoins_presents() -> None:
    """Vérifie la présence des fichiers de tests témoins pour les Lots 01..10."""
    temoins_dir = ROOT / "tests" / "temoins"
    for idx in range(1, 11):
        path = temoins_dir / f"test_lot_{idx:02d}.py"
        assert path.is_file(), f"Fichier témoin manquant : {path}"
