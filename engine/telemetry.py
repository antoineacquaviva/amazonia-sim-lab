"""Collecteur léger des 4 capteurs cognitifs v5.3 (100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple

from engine.state import (
    CARD_NONE,
    CARD_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    STEP_1_1_RATISSAGE,
    STEP_5_1_TACTIQUES,
    STEP_6_1_APPRENTISSAGE,
    STEP_6_3_END_TURN,
    STEP_GAME_OVER,
    TRACK_LEN,
    GameState,
    is_reve_code,
)

__all__ = (
    "REVEIL_ANATOMY_FIELDS",
    "TelemetrySummary",
    "TelemetryTracker",
    "count_active_transient_modifiers",
)

REVEIL_ANATOMY_FIELDS: tuple[str, ...] = (
    "rs_count",
    "rs_tour",
    "rs_t2",
    "rs_t3",
    "rs_t4",
    "rs_t5",
    "rs_t6",
    "rs_t7",
    "rs_t8",
    "rs_def_gardien",
    "rs_def1_foret",
    "rs_def2_foret",
    "rs_def_furtivite",
    "rs_def_lisiere",
    "rs_cards_sabotage",
    "rs_cards_none",
    "rs_cards_machine",
    "rs_cancelled_reve",
    "rs_bound_tactique",
    "rs_ratissage_active",
    "rs_machines_retired",
    "rs_machines_attacked",
    "rs_reves_on_track",
    "rs_sabotage_in_deck",
    "rs_strikes",
    "rs_pre_insects",
    "rs_pre_pieges",
    "rs_insects_spent",
    "rs_pieges_triggered",
    "rs_cat_zero_strikes",
    "rs_cat_piege",
    "rs_cat_insects_no_piege",
    "rs_cat_pure_def_or_empty",
    "rf_count",
    "rf_tour",
    "rf_def_gardien",
    "rf_def1_foret",
    "rf_def2_foret",
    "rf_cards_sabotage",
    "rf_cancelled_reve",
    "rf_bound_tactique",
    "rf_ratissage_active",
    "rf_machines_attacked",
    "rf_strikes",
    "rf_insects_spent",
    "rf_pieges_triggered",
    "rf_reves_on_track",
    "rf_sabotage_in_deck",
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
    # Anatomie diagnostique des tours de Réveil réussi (rs_*)
    rs_count: int = 0
    rs_tour: int = 0
    rs_t2: int = 0
    rs_t3: int = 0
    rs_t4: int = 0
    rs_t5: int = 0
    rs_t6: int = 0
    rs_t7: int = 0
    rs_t8: int = 0
    rs_def_gardien: int = 0
    rs_def1_foret: int = 0
    rs_def2_foret: int = 0
    rs_def_furtivite: int = 0
    rs_def_lisiere: int = 0
    rs_cards_sabotage: int = 0
    rs_cards_none: int = 0
    rs_cards_machine: int = 0
    rs_cancelled_reve: int = 0
    rs_bound_tactique: int = 0
    rs_ratissage_active: int = 0
    rs_machines_retired: int = 0
    rs_machines_attacked: int = 0
    rs_reves_on_track: int = 0
    rs_sabotage_in_deck: int = 0
    rs_strikes: int = 0
    rs_pre_insects: int = 0
    rs_pre_pieges: int = 0
    rs_insects_spent: int = 0
    rs_pieges_triggered: int = 0
    rs_cat_zero_strikes: int = 0
    rs_cat_piege: int = 0
    rs_cat_insects_no_piege: int = 0
    rs_cat_pure_def_or_empty: int = 0
    # Anatomie comparative des tentatives de Réveil échouées (rf_*)
    rf_count: int = 0
    rf_tour: int = 0
    rf_def_gardien: int = 0
    rf_def1_foret: int = 0
    rf_def2_foret: int = 0
    rf_cards_sabotage: int = 0
    rf_cancelled_reve: int = 0
    rf_bound_tactique: int = 0
    rf_ratissage_active: int = 0
    rf_machines_attacked: int = 0
    rf_strikes: int = 0
    rf_insects_spent: int = 0
    rf_pieges_triggered: int = 0
    rf_reves_on_track: int = 0
    rf_sabotage_in_deck: int = 0


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
    # État transitoire du tour courant pour l'anatomie du Réveil
    _turn_strikes: int = 0
    _turn_reveil_active: bool = False
    _turn_def_snap: tuple[int, int, int, int, int, int] | None = None
    _turn_pre5_snap: tuple[int, ...] | None = None
    # Accumulateurs Réveils réussis (rs_*)
    rs_count: int = 0
    rs_tour: int = 0
    rs_t2: int = 0
    rs_t3: int = 0
    rs_t4: int = 0
    rs_t5: int = 0
    rs_t6: int = 0
    rs_t7: int = 0
    rs_t8: int = 0
    rs_def_gardien: int = 0
    rs_def1_foret: int = 0
    rs_def2_foret: int = 0
    rs_def_furtivite: int = 0
    rs_def_lisiere: int = 0
    rs_cards_sabotage: int = 0
    rs_cards_none: int = 0
    rs_cards_machine: int = 0
    rs_cancelled_reve: int = 0
    rs_bound_tactique: int = 0
    rs_ratissage_active: int = 0
    rs_machines_retired: int = 0
    rs_machines_attacked: int = 0
    rs_reves_on_track: int = 0
    rs_sabotage_in_deck: int = 0
    rs_strikes: int = 0
    rs_pre_insects: int = 0
    rs_pre_pieges: int = 0
    rs_insects_spent: int = 0
    rs_pieges_triggered: int = 0
    rs_cat_zero_strikes: int = 0
    rs_cat_piege: int = 0
    rs_cat_insects_no_piege: int = 0
    rs_cat_pure_def_or_empty: int = 0
    # Accumulateurs tentatives de Réveil échouées (rf_*)
    rf_count: int = 0
    rf_tour: int = 0
    rf_def_gardien: int = 0
    rf_def1_foret: int = 0
    rf_def2_foret: int = 0
    rf_cards_sabotage: int = 0
    rf_cancelled_reve: int = 0
    rf_bound_tactique: int = 0
    rf_ratissage_active: int = 0
    rf_machines_attacked: int = 0
    rf_strikes: int = 0
    rf_insects_spent: int = 0
    rf_pieges_triggered: int = 0
    rf_reves_on_track: int = 0
    rf_sabotage_in_deck: int = 0

    def _snapshot_pre_step5(self, state: GameState) -> None:
        n = state.cfg.n_players
        p_max = state.cfg.p_max
        cards_sab = 0
        cards_none = 0
        cards_mach = 0
        cancelled_reve = 0
        bound_tact = 0
        for s in range(n):
            card, _d1, _d2, _lecture_m, bound_t = state.get_player_hand(s)
            if card == CARD_SABOTAGE:
                cards_sab += 1
            elif card == CARD_NONE:
                cards_none += 1
            elif 1 <= card <= 12:
                cards_mach += 1
                if bound_t > 0:
                    bound_tact += 1
                else:
                    cancelled_reve += 1

        ratissage_active = 0
        machines_retired = 0
        for r in range(n):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r, mt)
                if st == MACHINE_STATUS_RATISSAGE and pos > 0:
                    ratissage_active += 1
                elif st == MACHINE_STATUS_RETIRED or pos == 0:
                    machines_retired += 1

        reves_on_track = 0
        for rk in range(TRACK_LEN):
            if is_reve_code(state.get_tactique_at_rank(rk)):
                reves_on_track += 1

        sab_in_deck = int(state.sabotage_deck_count)

        pre_insects = 0
        pre_pieges = 0
        for r in range(n):
            for p in range(1, p_max + 1):
                pre_insects += state.get_parcel_insectes(r, p)
                if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                    pre_pieges += 1

        self._turn_pre5_snap = (
            cards_sab,
            cards_none,
            cards_mach,
            cancelled_reve,
            bound_tact,
            ratissage_active,
            machines_retired,
            reves_on_track,
            sab_in_deck,
            pre_insects,
            pre_pieges,
        )

    def _finalize_reveil_turn(self, state: GameState) -> None:
        if not self._turn_reveil_active or self._turn_pre5_snap is None:
            return
        self._turn_reveil_active = False
        pre5 = self._turn_pre5_snap
        self._turn_pre5_snap = None
        def_snap = self._turn_def_snap or (state.tour, 0, 0, 0, 0, 0)
        self._turn_def_snap = None

        tour, def_gard, def1_for, def2_for, def_furt, def_lis = def_snap
        (
            cards_sab,
            cards_none,
            cards_mach,
            cancelled_reve,
            bound_tact,
            ratissage_active,
            machines_retired,
            reves_on_track,
            sab_in_deck,
            pre_insects,
            pre_pieges,
        ) = pre5

        n = state.cfg.n_players
        p_max = state.cfg.p_max
        post_insects = 0
        post_pieges = 0
        for r in range(n):
            for p in range(1, p_max + 1):
                post_insects += state.get_parcel_insectes(r, p)
                if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                    post_pieges += 1

        machines_attacked = 0
        for r in range(n):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                _, _, attacked = state.get_machine_turn_stats(r, mt)
                if attacked:
                    machines_attacked += 1

        insects_spent = max(0, pre_insects - post_insects)
        pieges_triggered = max(0, pre_pieges - post_pieges)
        strikes = self._turn_strikes
        succeeded = (not state.real_damage_this_turn) and (not state.is_sommeil_victory())

        if succeeded:
            self.rs_count += 1
            self.rs_tour += tour
            if tour == 2:
                self.rs_t2 += 1
            elif tour == 3:
                self.rs_t3 += 1
            elif tour == 4:
                self.rs_t4 += 1
            elif tour == 5:
                self.rs_t5 += 1
            elif tour == 6:
                self.rs_t6 += 1
            elif tour == 7:
                self.rs_t7 += 1
            elif tour >= 8:
                self.rs_t8 += 1
            self.rs_def_gardien += def_gard
            self.rs_def1_foret += def1_for
            self.rs_def2_foret += def2_for
            self.rs_def_furtivite += def_furt
            self.rs_def_lisiere += def_lis
            self.rs_cards_sabotage += cards_sab
            self.rs_cards_none += cards_none
            self.rs_cards_machine += cards_mach
            self.rs_cancelled_reve += cancelled_reve
            self.rs_bound_tactique += bound_tact
            self.rs_ratissage_active += ratissage_active
            self.rs_machines_retired += machines_retired
            self.rs_machines_attacked += machines_attacked
            self.rs_reves_on_track += reves_on_track
            self.rs_sabotage_in_deck += sab_in_deck
            self.rs_strikes += strikes
            self.rs_pre_insects += pre_insects
            self.rs_pre_pieges += pre_pieges
            self.rs_insects_spent += insects_spent
            self.rs_pieges_triggered += pieges_triggered
            if strikes == 0:
                self.rs_cat_zero_strikes += 1
            elif pieges_triggered > 0:
                self.rs_cat_piege += 1
            elif insects_spent > 0:
                self.rs_cat_insects_no_piege += 1
            else:
                self.rs_cat_pure_def_or_empty += 1
        else:
            self.rf_count += 1
            self.rf_tour += tour
            self.rf_def_gardien += def_gard
            self.rf_def1_foret += def1_for
            self.rf_def2_foret += def2_for
            self.rf_cards_sabotage += cards_sab
            self.rf_cancelled_reve += cancelled_reve
            self.rf_bound_tactique += bound_tact
            self.rf_ratissage_active += ratissage_active
            self.rf_machines_attacked += machines_attacked
            self.rf_strikes += strikes
            self.rf_insects_spent += insects_spent
            self.rf_pieges_triggered += pieges_triggered
            self.rf_reves_on_track += reves_on_track
            self.rf_sabotage_in_deck += sab_in_deck

    def on_step_transition(self, state: GameState, prev_step: int, next_step: int) -> None:
        """Accumule `mem_debt_score` à chaque sous-étape traversée au sein d'un tour."""
        if next_step == STEP_1_1_RATISSAGE and prev_step == STEP_6_3_END_TURN:
            self._turn_closed = False
            self._turn_strikes = 0
            self._turn_reveil_active = False
            self._turn_def_snap = None
            self._turn_pre5_snap = None
            return
        if next_step == STEP_5_1_TACTIQUES:
            self._turn_strikes = 0
            if self._turn_reveil_active:
                self._snapshot_pre_step5(state)
        elif next_step in (STEP_GAME_OVER, STEP_6_1_APPRENTISSAGE):
            if self._turn_reveil_active and self._turn_pre5_snap is not None:
                self._finalize_reveil_turn(state)
        if prev_step != STEP_GAME_OVER:
            self.mem_debt_score += count_active_transient_modifiers(state)

    def on_machine_strike(self, _state: GameState, _ray: int, eligible_laws_count: int) -> None:
        """Enregistre le nombre de MOD_LOI_DU_COEUR actifs et éligibles sur le rayon frappé."""
        self.strike_count += 1
        self._turn_strikes += 1
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

    def on_reveil_attempt(self, state: GameState) -> None:
        """Enregistre l'engagement d'un Gardien Face 2 pour le Réveil en fin d'Étape 2.2."""
        self.reveil_attempts += 1
        self._turn_reveil_active = True
        def_gard = 0
        def1_for = 0
        def2_for = 0
        def_furt = 0
        def_lis = 0
        for s in range(state.cfg.n_players):
            for def_idx in (0, 1):
                kind, _a, _b, _c = state.decode_def_loc(state.get_player_def_loc_raw(s, def_idx))
                if kind == "GARDIEN_REVEIL":
                    def_gard += 1
                elif kind == "FORET":
                    if def_idx == 0:
                        def1_for += 1
                    else:
                        def2_for += 1
                elif kind == "FURTIVITE":
                    def_furt += 1
                elif kind == "LISIERE":
                    def_lis += 1
        self._turn_def_snap = (state.tour, def_gard, def1_for, def2_for, def_furt, def_lis)

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
            rs_count=self.rs_count,
            rs_tour=self.rs_tour,
            rs_t2=self.rs_t2,
            rs_t3=self.rs_t3,
            rs_t4=self.rs_t4,
            rs_t5=self.rs_t5,
            rs_t6=self.rs_t6,
            rs_t7=self.rs_t7,
            rs_t8=self.rs_t8,
            rs_def_gardien=self.rs_def_gardien,
            rs_def1_foret=self.rs_def1_foret,
            rs_def2_foret=self.rs_def2_foret,
            rs_def_furtivite=self.rs_def_furtivite,
            rs_def_lisiere=self.rs_def_lisiere,
            rs_cards_sabotage=self.rs_cards_sabotage,
            rs_cards_none=self.rs_cards_none,
            rs_cards_machine=self.rs_cards_machine,
            rs_cancelled_reve=self.rs_cancelled_reve,
            rs_bound_tactique=self.rs_bound_tactique,
            rs_ratissage_active=self.rs_ratissage_active,
            rs_machines_retired=self.rs_machines_retired,
            rs_machines_attacked=self.rs_machines_attacked,
            rs_reves_on_track=self.rs_reves_on_track,
            rs_sabotage_in_deck=self.rs_sabotage_in_deck,
            rs_strikes=self.rs_strikes,
            rs_pre_insects=self.rs_pre_insects,
            rs_pre_pieges=self.rs_pre_pieges,
            rs_insects_spent=self.rs_insects_spent,
            rs_pieges_triggered=self.rs_pieges_triggered,
            rs_cat_zero_strikes=self.rs_cat_zero_strikes,
            rs_cat_piege=self.rs_cat_piege,
            rs_cat_insects_no_piege=self.rs_cat_insects_no_piege,
            rs_cat_pure_def_or_empty=self.rs_cat_pure_def_or_empty,
            rf_count=self.rf_count,
            rf_tour=self.rf_tour,
            rf_def_gardien=self.rf_def_gardien,
            rf_def1_foret=self.rf_def1_foret,
            rf_def2_foret=self.rf_def2_foret,
            rf_cards_sabotage=self.rf_cards_sabotage,
            rf_cancelled_reve=self.rf_cancelled_reve,
            rf_bound_tactique=self.rf_bound_tactique,
            rf_ratissage_active=self.rf_ratissage_active,
            rf_machines_attacked=self.rf_machines_attacked,
            rf_strikes=self.rf_strikes,
            rf_insects_spent=self.rf_insects_spent,
            rf_pieges_triggered=self.rf_pieges_triggered,
            rf_reves_on_track=self.rf_reves_on_track,
            rf_sabotage_in_deck=self.rf_sabotage_in_deck,
        )
