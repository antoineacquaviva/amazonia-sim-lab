"""Collecteur léger des 4 capteurs cognitifs v5.3 (100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    STEP_1_1_RATISSAGE,
    STEP_6_3_END_TURN,
    STEP_GAME_OVER,
    TRACK_LEN,
    GameState,
)

__all__ = (
    "TelemetrySummary",
    "TelemetryTracker",
    "count_active_transient_modifiers",
)


def _bit_count_u8(val: int) -> int:
    c = 0
    v = val & 0xFF
    while v:
        v &= v - 1
        c += 1
    return c


def count_active_transient_modifiers(state: GameState) -> int:
    """Compte les TransientModifier actifs non portés par un jeton physique du plateau."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    active = 0

    if state.get_global_mod_seuil_turn() != 0:
        active += 1

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if state.get_machine_seuil_mod_turn(r, mt) != 0:
                active += 1
        for p in range(1, p_max + 1):
            if state.get_parcel_seuil_mod_turn(r, p) != 0:
                active += 1
            flags = state.get_parcel_flags_turn(r, p)
            if flags:
                active += _bit_count_u8(flags)

    for rank_idx in range(TRACK_LEN):
        if state.get_pending_apprentissage_at_rank(rank_idx) != 0:
            active += 1

    vol_cnt, _ = state.get_pending_voluntary_app_reduction()
    if vol_cnt > 0:
        active += vol_cnt

    # Verrous 1/tour et drapeaux transitoires d'effets mémorisés sans jeton physique (ex: G6 A avant 3.2)
    for lock_idx in range(64):
        if state.has_used_once_per_turn(lock_idx):
            active += 1

    return active


class TelemetrySummary(NamedTuple):
    """Synthèse par partie des 4 capteurs cognitifs définis dans rule-bots-telemetry.md."""

    mem_debt_score: int
    law_stack_mean: float
    law_stack_max: int
    fiddliness_ratio: float
    cascade_sweeps: int
    mid_combat_interrupts: int
    gardiens_opened_total: int
    interrupt_windows_count: int
    gardiens_per_window_mean: float
    total_physical_ops: int
    total_player_decisions: int
    turns_measured: int
    reveil_attempts: int = 0
    reveil_failures: int = 0


@dataclass(slots=True)
class TelemetryTracker:
    """Collecteur optionnel sans état global mutable mesurant la charge cognitive d'une partie."""

    mem_debt_score: int = 0
    strike_count: int = 0
    strike_law_sum: int = 0
    law_stack_max: int = 0
    turn_physical_ops: int = 0
    turn_player_decisions: int = 0
    total_physical_ops: int = 0
    total_player_decisions: int = 0
    sum_turn_fiddliness: float = 0.0
    turns_measured: int = 0
    cascade_sweeps: int = 0
    mid_combat_interrupts: int = 0
    gardiens_opened_total: int = 0
    interrupt_windows_count: int = 0
    reveil_attempts: int = 0
    reveil_failures: int = 0
    _turn_closed: bool = False

    def on_step_transition(self, state: GameState, prev_step: int, next_step: int) -> None:
        """Accumule `mem_debt_score` à chaque sous-étape traversée au sein d'un tour."""
        if next_step == STEP_1_1_RATISSAGE and prev_step == STEP_6_3_END_TURN:
            self._turn_closed = False
            return
        if prev_step != STEP_GAME_OVER:
            self.mem_debt_score += count_active_transient_modifiers(state)

    def on_machine_strike(self, _state: GameState, _ray: int, eligible_laws_count: int) -> None:
        """Enregistre le nombre de MOD_LOI_DU_COEUR actifs et éligibles sur le rayon frappé."""
        self.strike_count += 1
        self.strike_law_sum += eligible_laws_count
        self.law_stack_max = max(self.law_stack_max, eligible_laws_count)

    def record_physical_ops(self, _state: GameState, count: int) -> None:
        """Ajoute `count` manipulations physiques de pions/jetons/cartes pour le tour courant."""
        if count > 0:
            self.turn_physical_ops += count
            self.total_physical_ops += count

    def record_player_decision(self, _state: GameState, _seat: int) -> None:
        """Enregistre +1 décision joueur durant le tour courant."""
        self.turn_player_decisions += 1
        self.total_player_decisions += 1

    def on_gardien_sweep(
        self,
        _state: GameState,
        *,
        repasses: int,
        opened: int,
        in_combat: bool,
    ) -> None:
        """Enregistre une fenêtre de balayage `sweep_gardiens` (repassages 1->6 et ouvertures)."""
        self.interrupt_windows_count += 1
        self.cascade_sweeps += repasses
        self.gardiens_opened_total += opened
        if in_combat and opened > 0:
            self.mid_combat_interrupts += opened

    def on_reveil_attempt(self, _state: GameState) -> None:
        """Enregistre l'engagement d'un Gardien Face 2 pour le Réveil en fin d'Étape 2.2."""
        self.reveil_attempts += 1

    def on_reveil_failure(self, _state: GameState) -> None:
        """Enregistre l'échec d'une tentative de Réveil (dommage réel subi durant le tour)."""
        self.reveil_failures += 1

    def on_end_turn(self, _state: GameState, *, game_over: bool) -> None:
        """Clôture le ratio `physical_ops / max(1, decisions_joueurs)` du tour écoulé."""
        if self._turn_closed and game_over:
            return
        if self.turn_physical_ops > 0 or self.turn_player_decisions > 0:
            ratio = self.turn_physical_ops / max(1, self.turn_player_decisions)
            self.sum_turn_fiddliness += ratio
            self.turns_measured += 1
            self.turn_physical_ops = 0
            self.turn_player_decisions = 0
        if game_over:
            self._turn_closed = True

    def summary(self) -> TelemetrySummary:
        """Retourne l'instantané immuable des 4 capteurs cognitifs de la partie."""
        pending_turns = self.turns_measured
        pending_sum_fidd = self.sum_turn_fiddliness
        if not self._turn_closed and (self.turn_physical_ops > 0 or self.turn_player_decisions > 0):
            pending_sum_fidd += self.turn_physical_ops / max(1, self.turn_player_decisions)
            pending_turns += 1

        law_mean = (self.strike_law_sum / self.strike_count) if self.strike_count > 0 else 0.0
        fidd_mean = (pending_sum_fidd / pending_turns) if pending_turns > 0 else 0.0
        gard_win_mean = (
            self.gardiens_opened_total / self.interrupt_windows_count
            if self.interrupt_windows_count > 0
            else 0.0
        )
        return TelemetrySummary(
            mem_debt_score=self.mem_debt_score,
            law_stack_mean=law_mean,
            law_stack_max=self.law_stack_max,
            fiddliness_ratio=fidd_mean,
            cascade_sweeps=self.cascade_sweeps,
            mid_combat_interrupts=self.mid_combat_interrupts,
            gardiens_opened_total=self.gardiens_opened_total,
            interrupt_windows_count=self.interrupt_windows_count,
            gardiens_per_window_mean=gard_win_mean,
            total_physical_ops=self.total_physical_ops,
            total_player_decisions=self.total_player_decisions,
            turns_measured=pending_turns,
            reveil_attempts=self.reveil_attempts,
            reveil_failures=self.reveil_failures,
        )
