"""Catalogue modulaire stateless Canon v6.4 (30 tuiles actives STANDARD_A).

Les 30 tuiles actives (`G1:A..G15:A`, `R1:A..R10:A`, `M1:A..M5:A`) sont chargées de façon
idempotente pour les Modes 3 et 4 (les slots natifs `SLOT_BUG_CERVEAU` et
`SLOT_COLONISATION_GARDIENS` sont enregistrés dans ``engine.core_engine``).
Les catalogues historiques restent archivés dans ``archive/effects_v6_2/``,
``archive/effects_v5_5/`` et ``archive/legacy_tiles_v5_3/``.
"""

from __future__ import annotations

import importlib

from engine.effects.registry import list_registered_tiles

__all__ = (
    "LOADED_LOT_MODULES",
    "load_all_effects",
)

LOADED_LOT_MODULES: tuple[str, ...] = (
    "engine.effects.gardiens_v6_4",
    "engine.effects.reves_v6_4",
    "engine.effects.nids_v6_4",
)


def load_all_effects() -> tuple[tuple[str, str], ...]:
    """Charge de façon idempotente les 30 tuiles actives Canon v6.4."""
    for mod_name in LOADED_LOT_MODULES:
        mod = importlib.import_module(mod_name)
        importlib.reload(mod)
    return list_registered_tiles()


load_all_effects()
