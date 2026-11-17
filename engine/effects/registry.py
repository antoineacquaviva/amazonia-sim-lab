"""Registre stateless des effets de tuiles (conforme au garde-fou AST verify_lot.py)."""

from __future__ import annotations

from engine.primitives import (
    EffectHandler,
    TileRegistration,
    clear_tile_registry,
    dispatch_hook,
    get_tile_registration,
    list_registered_tiles,
    register_tile,
)

__all__ = (
    "EffectHandler",
    "TileRegistration",
    "clear_tile_registry",
    "dispatch_hook",
    "get_tile_registration",
    "list_registered_tiles",
    "register_tile",
)
