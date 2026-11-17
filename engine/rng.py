"""PRNG déterministe adressable par événement (CRN & Forks, 100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import TypeVar

__all__ = (
    "MASK64",
    "SRC_BOT_TIEBREAK",
    "SRC_DICE",
    "SRC_MACHINE_SHUFFLE",
    "SRC_TACTICS_SETUP",
    "rand_below",
    "rand_event",
    "rand_u64",
    "roll_d6",
    "shuffle_deterministic",
)

T = TypeVar("T")

MASK64: int = 0xFFFFFFFFFFFFFFFF

# Constantes d'adressage par source d'événement (sans branch_id sur événements comparables)
SRC_DICE: int = 1
SRC_MACHINE_SHUFFLE: int = 2
SRC_TACTICS_SETUP: int = 3
SRC_BOT_TIEBREAK: int = 4

# Constantes de diffusion 64 bits (SplitMix64 / Weyl)
_K0: int = 0x9E3779B97F4A7C15
_K1: int = 0xBF58476D1CE4E5B9
_K2: int = 0x94D049BB133111EB
_K3: int = 0xD6E8FEB86659FD93
_K4: int = 0xA0761D6478BD642F
_K5: int = 0xE7037ED1A0B428DB


def _mix64(z: int) -> int:
    """Finaliseur bijectif SplitMix64 sur 64 bits."""
    z = ((z ^ (z >> 30)) * _K1) & MASK64
    z = ((z ^ (z >> 27)) * _K2) & MASK64
    return (z ^ (z >> 31)) & MASK64


def rand_u64(
    exp_seed: int,
    rep_id: int,
    source_type: int,
    tour: int,
    entity_id: int,
    draw_idx: int,
) -> int:
    """Génère un entier 64 bits déterministe pur à partir du tuple d'adresse à 6 clés.

    Conçu sans état global ni hashlib pour tourner à pleine vitesse sous le JIT de PyPy 3.11
    tout en garantissant l'indépendance CRN stricte entre sources, tours et entités.
    """
    h = (
        ((exp_seed & MASK64) * _K0)
        ^ (((rep_id + 1) & MASK64) * _K3)
        ^ (((source_type + 1) * _K4) & MASK64)
        ^ (((tour + 1) * _K5) & MASK64)
        ^ (((entity_id + 1) * _K1) & MASK64)
        ^ (((draw_idx + 1) * _K2) & MASK64)
    ) & MASK64
    return _mix64(h)


# Alias conforme à rule-kernel.md
rand_event = rand_u64


def rand_below(
    upper: int,
    exp_seed: int,
    rep_id: int,
    source_type: int,
    tour: int,
    entity_id: int,
    draw_idx: int,
) -> int:
    """Retourne un entier uniforme dans [0, upper) par réduction entière 128 bits."""
    assert upper > 0, "upper doit être strictement positif"
    u = rand_u64(exp_seed, rep_id, source_type, tour, entity_id, draw_idx)
    return (u * upper) >> 64


def roll_d6(
    exp_seed: int,
    rep_id: int,
    source_type: int,
    tour: int,
    entity_id: int,
    draw_idx: int,
) -> int:
    """Lance un dé à 6 faces déterministe retournant une valeur dans 1..6."""
    return rand_below(6, exp_seed, rep_id, source_type, tour, entity_id, draw_idx) + 1


def shuffle_deterministic(
    items: Sequence[T],
    exp_seed: int,
    rep_id: int,
    source_type: int,
    tour: int,
    entity_id: int = 0,
) -> list[T]:
    """Retourne une copie mélangée par Fisher-Yates adressé par idx décroissant."""
    out: list[T] = list(items)
    n = len(out)
    for idx in range(n - 1, 0, -1):
        j = rand_below(idx + 1, exp_seed, rep_id, source_type, tour, entity_id, idx)
        out[idx], out[j] = out[j], out[idx]
    return out
