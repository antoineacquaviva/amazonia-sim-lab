"""Catalogue modulaire stateless des effets de tuiles.

Phase CORE_STABILIZATION (Mode 2 à blanc) : le stock historique des 100 profils
v5.3 (Lots 01..10) est archivé dans ``archive/legacy_tiles_v5_3/`` (tag Git
``archive/v5.4.3-legacy-100-tiles``). Les futurs lots conçus après le Core Freeze
seront enregistrés ici via ``@register_tile``.
"""

from __future__ import annotations

import importlib

from engine.effects.registry import list_registered_tiles

__all__ = (
    "LOADED_LOT_MODULES",
    "load_all_effects",
)

LOADED_LOT_MODULES: tuple[str, ...] = ()


def load_all_effects() -> tuple[tuple[str, str], ...]:
    """Charge de façon idempotente tous les lots d'effets actifs (vide en Phase Cœur)."""
    for mod_name in LOADED_LOT_MODULES:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    return list_registered_tiles()
