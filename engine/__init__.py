"""Noyau déterministe scellé d'Amazonia : Dernier Rempart (PyPy 3.11 stdlib pure)."""

from __future__ import annotations

from engine.core_engine import apply_choice, step_until_decision
from engine.primitives import DecisionRequest, GameOver
from engine.rng import rand_event, rand_u64, roll_d6, shuffle_deterministic
from engine.state import GameConfig, GameState, PlayerObservation, get_layout_report

__all__ = (
    "DecisionRequest",
    "GameConfig",
    "GameOver",
    "GameState",
    "PlayerObservation",
    "apply_choice",
    "get_layout_report",
    "rand_event",
    "rand_u64",
    "roll_d6",
    "shuffle_deterministic",
    "step_until_decision",
)
