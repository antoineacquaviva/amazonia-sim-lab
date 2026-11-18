"""Catalogue modulaire stateless des effets de tuiles (Lots 01..10)."""

from __future__ import annotations

import importlib

from engine.effects import lot_01, lot_02, lot_03, lot_04
from engine.effects.registry import list_registered_tiles

__all__ = (
    "load_all_effects",
    "lot_01",
    "lot_02",
    "lot_03",
    "lot_04",
)

LOADED_LOT_MODULES: tuple[str, ...] = (
    "engine.effects.lot_01",
    "engine.effects.lot_02",
    "engine.effects.lot_03",
    "engine.effects.lot_04",
)


def load_all_effects() -> tuple[tuple[str, str], ...]:
    """Charge de façon idempotente tous les lots d'effets livrés (et ré-enregistre après clear)."""
    for mod_name in LOADED_LOT_MODULES:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    return list_registered_tiles()
