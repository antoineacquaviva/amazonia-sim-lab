"""Catalogue modulaire stateless Canon 0 v6.2 (30 tuiles actives STANDARD_A).

Les 30 tuiles actives (G1:A..G15:A, R1:A..R10:A, M1:A..M5:A) sont chargées de façon
idempotente pour les Modes 3 et 4 (les slots de migration SLOT_BUG_CERVEAU et
SLOT_COLONISATION_GARDIENS sont enregistrés nativement dans ``engine.core_engine``).
Les handlers transitoires v5.5 sont archivés dans ``archive/effects_v5_5/`` et le stock
historique v5.3 reste archivé dans ``archive/legacy_tiles_v5_3/``.
"""

from __future__ import annotations

import importlib

from engine.effects.registry import list_registered_tiles

__all__ = (
    "LOADED_LOT_MODULES",
    "load_all_effects",
)

LOADED_LOT_MODULES: tuple[str, ...] = (
    "engine.effects.gardiens_v6_2",
    "engine.effects.reves_v6_2",
    "engine.effects.nids_v6_2",
)


def load_all_effects() -> tuple[tuple[str, str], ...]:
    """Charge de façon idempotente les 30 tuiles actives Canon 0 v6.2."""
    for mod_name in LOADED_LOT_MODULES:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    return list_registered_tiles()


load_all_effects()
