"""Agents coopératifs muets d'Amazonia : Dernier Rempart (PyPy 3.11 stdlib pure)."""

from __future__ import annotations

from bots.bot_b0 import BotB0, choose_b0, play_game_b0
from bots.bot_b3_rh import BotB3, choose_b3, play_game_b3
from bots.heuristic_engine import (
    BotB1,
    BotB2,
    choose_b1,
    choose_b2,
    play_game_b1,
    play_game_b2,
)

__all__ = (
    "BotB0",
    "BotB1",
    "BotB2",
    "BotB3",
    "choose_b0",
    "choose_b1",
    "choose_b2",
    "choose_b3",
    "play_game_b0",
    "play_game_b1",
    "play_game_b2",
    "play_game_b3",
)
