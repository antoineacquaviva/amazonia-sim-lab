"""Catalogue modulaire stateless des effets de tuiles v5.5 (30 tuiles actives STANDARD_A).

Les 30 tuiles actives (G1:A..G15:A, R1:A..R10:A, M1:A..M5:A) sont chargées de façon
idempotente pour les Modes 3 et 4 (les slots de migration SLOT_BUG_CERVEAU et
SLOT_COLONISATION_GARDIENS sont enregistrés nativement dans ``engine.core_engine``).
Le stock historique de variantes alternatives v5.3 reste archivé dans
``archive/legacy_tiles_v5_3/``.
"""

from __future__ import annotations

import importlib

from engine.effects.registry import list_registered_tiles

__all__ = (
    "LOADED_LOT_MODULES",
    "load_all_effects",
)

LOADED_LOT_MODULES: tuple[str, ...] = (
    "engine.effects.gardiens_v5_5",
    "engine.effects.reves_v5_5",
    "engine.effects.croissance_v5_5",
)


def load_all_effects() -> tuple[tuple[str, str], ...]:
    """Charge de façon idempotente les 30 tuiles actives du catalogue v5.5."""
    for mod_name in LOADED_LOT_MODULES:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    return list_registered_tiles()


load_all_effects()
