"""Collecteur léger des 4 capteurs cognitifs, de l'attribution défensive et du Rasoir d'Ockham (100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import NamedTuple

from engine.state import (
    CARD_NONE,
    CARD_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    STEP_1_2_DEAL,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_4_3_MIGRATION,
    STEP_5_1_TACTIQUES,
    STEP_5_3_END_CHECK,
    STEP_6_2_EVOLUTION,
    STEP_6_3_END_TURN,
    STEP_GAME_OVER,
    TRACK_LEN,
    GameState,
    is_reve_code,
)

__all__ = (
    "DEFENSE_ATTRIBUTION_FIELDS",
    "DILEMMA_CHOICE_FIELDS",
    "OCKHAM_COUNT_FIELDS",
    "REVEIL_ANATOMY_FIELDS",
    "V6_METRICS_FIELDS",
    "TelemetrySummary",
    "TelemetryTracker",
    "count_active_transient_modifiers",
)

V6_METRICS_FIELDS: tuple[str, ...] = (
    "power_tokens_end_act1",
    "act1_reached",
    "power_tokens_end_game",
    "charge_gains",
    "charge_gains_act1",
    "charge_gains_act2",
    "furtivite_1_rive_turns",
)

DEFENSE_ATTRIBUTION_FIELDS: tuple[str, ...] = (
    "da_parade_classique",
    "da_piege",
    "da_parade_avec_insectes",
    "da_reve_annulation",
    "da_sabotage_revele",
    "da_insecte_bug_deviation",
    "da_arbres_repousse_finale",
)

OCKHAM_COUNT_FIELDS: tuple[str, ...] = (
    "ok_furt_rive_piege",
    "ok_furt_rive_sabotage",
    "ok_furt_rive_piege_lost",
    "ok_furt_rive_sabotage_lost",
    "ok_furt_orphan_pawns",
    "ok_furt_failed_binomes",
    "ok_furt_multi_rive_turns",
    "ok_pieges_placed",
    "ok_pieges_triggered",
    "ok_pieges_unused_end",
    "ok_pont_routier_jumps",
    "ok_routes_created",
    "ok_repli_bordure",
    "ok_repli_coeur_exception",
    "ok_retrait_definitif_machine",
    "ok_abatteuse_ratissage_0_arbre",
    "ok_contact_nid_renvois",
    "ok_contact_nid_insectes_perdus",
    "ok_penurie_cartes_machine",
    "ok_charge_activations",
    "ok_charge_zero_gain",
    "ok_charge_zero_gain_parried",
    "ok_charge_zero_gain_barren",
    "ok_ratissage_entries_6_3",
    "ok_ratissage_activations",
    "ok_sabotage_acquired",
    "ok_sabotage_unrevealed_end",
    "ok_mig_moves",
    "ok_mig_wasted_end",
    "ok_bugs_unused_end",
    "ok_colonie_unused_end",
    "ok_insectes_foret_unused_end",
    "ok_bouclier_saves",
    "ok_gardien_return_lisiere",
    "ok_gardien_face2_upgrades",
    "ok_cascade_case4_openings",
    "ok_cascade_second_pass_sweeps",
    "ok_tour8_blocked_sommeil",
    "ok_tour8_blocked_eveil",
    "ok_liberation_batisseur_3j",
    "ok_def1_global_fallback",
    "ok_impasse_totale",
)

DILEMMA_CHOICE_FIELDS: tuple[str, ...] = (
    "dil_bug_passer",
    "dil_bug_minus",
    "dil_bug_plus",
    "dil_mig_stay",
    "dil_mig_foret",
    "dil_mig_bug",
    "dil_mig_colonie",
    "dil_def1_foret",
    "dil_def1_lisiere",
    "dil_def1_furtivite",
    "dil_def1_reve",
    "dil_def2_foret",
    "dil_def2_lisiere",
    "dil_def2_furtivite",
    "dil_def2_reve",
    "dil_def2_gardien",
    "dil_step2_turns_with_move",
    "dil_step2_turns_zero_move",
    "dil_ordre_constr_3_1",
    "dil_ordre_nid_4_2",
    "dil_ordre_att_5_1",
    "dil_ordre_rat_5_2",
    "dil_gardien_c1",
    "dil_gardien_c2",
    "dil_gardien_c3",
    "dil_gardien_c4",
    "dil_gardien_c5",
    "dil_gardien_c6",
)

REVEIL_ANATOMY_FIELDS: tuple[str, ...] = (
    "rs_count",
    "rs_tour",
    "rs_ratio_arbres_bp",
    "rs_t1",
    "rs_t2",
    "rs_t3",
    "rs_t4",
    "rs_t5",
    "rs_t6",
    "rs_t7",
    "rs_t8",
    "rs_def_gardien",
    "rs_def_parade",
    "rs_def_resonance",
    "rs_def_other_cases",
    "rs_distinct_gardiens_bet",
    "rs_def_reve",
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
    "rs_reves_opened",
    "rs_trig1_lit",
    "rs_trig2_lit",
    "rs_trig3_lit",
    "rs_trig4_lit",
    "rs_trig5_lit",
    "rs_trig6_lit",
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
    "rf_def_parade",
    "rf_def_resonance",
    "rf_def_other_cases",
    "rf_distinct_gardiens_bet",
    "rf_def_reve",
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
    "rf_reves_opened",
    "rf_trig1_lit",
    "rf_trig2_lit",
    "rf_trig3_lit",
    "rf_trig4_lit",
    "rf_trig5_lit",
    "rf_trig6_lit",
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

    # Verrous 1/tour et drapeaux transitoires d'effets mémorisés sans jeton physique (ex: G6 A avant 3.2)
    for lock_idx in range(64):
        if state.has_used_once_per_turn(lock_idx):
            active += 1

    return active


class TelemetrySummary(NamedTuple):
    """Synthèse par partie des capteurs cognitifs, d'attribution défensive et du Rasoir d'Ockham."""

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
    gardien_bets_won: int = 0
    gardien_bets_lost: int = 0
    bouclier_lisiere_saves: int = 0
    reves_activated: int = 0
    machines_cancelled_by_reve: int = 0
    machines_bypassed_inactive_reve: int = 0
    # Comptabilité d'attribution défensive (da_*)
    da_parade_classique: int = 0
    da_piege: int = 0
    da_parade_avec_insectes: int = 0
    da_reve_annulation: int = 0
    da_sabotage_revele: int = 0
    da_insecte_bug_deviation: int = 0
    da_arbres_repousse_finale: int = 0
    # Compteurs spécifiques cœur v6.1
    power_tokens_end_act1: int = 0
    act1_reached: int = 0
    power_tokens_end_game: int = 0
    charge_gains: int = 0
    charge_gains_act1: int = 0
    charge_gains_act2: int = 0
    furtivite_1_rive_turns: int = 0
    # Instrumentation Rasoir d'Ockham (ok_*)
    ok_furt_rive_piege: int = 0
    ok_furt_rive_sabotage: int = 0
    ok_furt_rive_piege_lost: int = 0
    ok_furt_rive_sabotage_lost: int = 0
    ok_furt_orphan_pawns: int = 0
    ok_furt_failed_binomes: int = 0
    ok_furt_multi_rive_turns: int = 0
    ok_pieges_placed: int = 0
    ok_pieges_triggered: int = 0
    ok_pieges_unused_end: int = 0
    ok_pont_routier_jumps: int = 0
    ok_routes_created: int = 0
    ok_repli_bordure: int = 0
    ok_repli_coeur_exception: int = 0
    ok_retrait_definitif_machine: int = 0
    ok_abatteuse_ratissage_0_arbre: int = 0
    ok_contact_nid_renvois: int = 0
    ok_contact_nid_insectes_perdus: int = 0
    ok_penurie_cartes_machine: int = 0
    ok_charge_activations: int = 0
    ok_charge_zero_gain: int = 0
    ok_charge_zero_gain_parried: int = 0
    ok_charge_zero_gain_barren: int = 0
    ok_ratissage_entries_6_3: int = 0
    ok_ratissage_activations: int = 0
    ok_sabotage_acquired: int = 0
    ok_sabotage_unrevealed_end: int = 0
    ok_mig_moves: int = 0
    ok_mig_wasted_end: int = 0
    ok_bugs_unused_end: int = 0
    ok_colonie_unused_end: int = 0
    ok_insectes_foret_unused_end: int = 0
    ok_bouclier_saves: int = 0
    ok_gardien_return_lisiere: int = 0
    ok_gardien_face2_upgrades: int = 0
    ok_cascade_case4_openings: int = 0
    ok_cascade_second_pass_sweeps: int = 0
    ok_tour8_blocked_sommeil: int = 0
    ok_tour8_blocked_eveil: int = 0
    ok_liberation_batisseur_3j: int = 0
    ok_def1_global_fallback: int = 0
    ok_impasse_totale: int = 0
    # Distributions de choix pour détection des faux dilemmes (dil_*)
    dil_bug_passer: int = 0
    dil_bug_minus: int = 0
    dil_bug_plus: int = 0
    dil_mig_stay: int = 0
    dil_mig_foret: int = 0
    dil_mig_bug: int = 0
    dil_mig_colonie: int = 0
    dil_def1_foret: int = 0
    dil_def1_lisiere: int = 0
    dil_def1_furtivite: int = 0
    dil_def1_reve: int = 0
    dil_def2_foret: int = 0
    dil_def2_lisiere: int = 0
    dil_def2_furtivite: int = 0
    dil_def2_reve: int = 0
    dil_def2_gardien: int = 0
    dil_step2_turns_with_move: int = 0
    dil_step2_turns_zero_move: int = 0
    dil_ordre_constr_3_1: int = 0
    dil_ordre_nid_4_2: int = 0
    dil_ordre_att_5_1: int = 0
    dil_ordre_rat_5_2: int = 0
    dil_gardien_c1: int = 0
    dil_gardien_c2: int = 0
    dil_gardien_c3: int = 0
    dil_gardien_c4: int = 0
    dil_gardien_c5: int = 0
    dil_gardien_c6: int = 0
    # Anatomie diagnostique des tours d'Éveil réussi (rs_*)
    rs_count: int = 0
    rs_tour: int = 0
    rs_ratio_arbres_bp: int = 0
    rs_t1: int = 0
    rs_t2: int = 0
    rs_t3: int = 0
    rs_t4: int = 0
    rs_t5: int = 0
    rs_t6: int = 0
    rs_t7: int = 0
    rs_t8: int = 0
    rs_def_gardien: int = 0
    rs_def_parade: int = 0
    rs_def_resonance: int = 0
    rs_def_other_cases: int = 0
    rs_distinct_gardiens_bet: int = 0
    rs_def_reve: int = 0
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
    rs_reves_opened: int = 0
    rs_trig1_lit: int = 0
    rs_trig2_lit: int = 0
    rs_trig3_lit: int = 0
    rs_trig4_lit: int = 0
    rs_trig5_lit: int = 0
    rs_trig6_lit: int = 0
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
    # Anatomie comparative des tentatives d'Éveil échouées (rf_*)
    rf_count: int = 0
    rf_tour: int = 0
    rf_def_gardien: int = 0
    rf_def_parade: int = 0
    rf_def_resonance: int = 0
    rf_def_other_cases: int = 0
    rf_distinct_gardiens_bet: int = 0
    rf_def_reve: int = 0
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
    rf_reves_opened: int = 0
    rf_trig1_lit: int = 0
    rf_trig2_lit: int = 0
    rf_trig3_lit: int = 0
    rf_trig4_lit: int = 0
    rf_trig5_lit: int = 0
    rf_trig6_lit: int = 0
    rf_sabotage_in_deck: int = 0
    tile_activations: tuple[tuple[str, int], ...] = ()


@dataclass(slots=True)
class TelemetryTracker:
    """Collecteur optionnel sans état global mutable mesurant la charge cognitive et le Rasoir d'Ockham."""

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
    gardien_bets_won: int = 0
    gardien_bets_lost: int = 0
    bouclier_lisiere_saves: int = 0
    reves_activated: int = 0
    machines_cancelled_by_reve: int = 0
    machines_bypassed_inactive_reve: int = 0
    da_parade_classique: int = 0
    da_piege: int = 0
    da_parade_avec_insectes: int = 0
    da_reve_annulation: int = 0
    da_sabotage_revele: int = 0
    da_insecte_bug_deviation: int = 0
    da_arbres_repousse_finale: int = 0
    # Compteurs spécifiques cœur v6.1
    power_tokens_end_act1: int = 0
    act1_reached: int = 0
    power_tokens_end_game: int = 0
    charge_gains: int = 0
    charge_gains_act1: int = 0
    charge_gains_act2: int = 0
    furtivite_1_rive_turns: int = 0
    _turn_furt_total_rives_exec: int = 0
    _turn_step2_moved: bool = False
    _turn_closed: bool = False
    # Instrumentation Rasoir d'Ockham (ok_*)
    ok_furt_rive_piege: int = 0
    ok_furt_rive_sabotage: int = 0
    ok_furt_rive_piege_lost: int = 0
    ok_furt_rive_sabotage_lost: int = 0
    ok_furt_orphan_pawns: int = 0
    ok_furt_failed_binomes: int = 0
    ok_furt_multi_rive_turns: int = 0
    ok_pieges_placed: int = 0
    ok_pieges_triggered: int = 0
    ok_pieges_unused_end: int = 0
    ok_pont_routier_jumps: int = 0
    ok_routes_created: int = 0
    ok_repli_bordure: int = 0
    ok_repli_coeur_exception: int = 0
    ok_retrait_definitif_machine: int = 0
    ok_abatteuse_ratissage_0_arbre: int = 0
    ok_contact_nid_renvois: int = 0
    ok_contact_nid_insectes_perdus: int = 0
    ok_penurie_cartes_machine: int = 0
    ok_charge_activations: int = 0
    ok_charge_zero_gain: int = 0
    ok_charge_zero_gain_parried: int = 0
    ok_charge_zero_gain_barren: int = 0
    ok_ratissage_entries_6_3: int = 0
    ok_ratissage_activations: int = 0
    ok_sabotage_acquired: int = 0
    ok_sabotage_unrevealed_end: int = 0
    ok_mig_moves: int = 0
    ok_mig_wasted_end: int = 0
    ok_bugs_unused_end: int = 0
    ok_colonie_unused_end: int = 0
    ok_insectes_foret_unused_end: int = 0
    ok_bouclier_saves: int = 0
    ok_gardien_return_lisiere: int = 0
    ok_gardien_face2_upgrades: int = 0
    ok_cascade_case4_openings: int = 0
    ok_cascade_second_pass_sweeps: int = 0
    ok_tour8_blocked_sommeil: int = 0
    ok_tour8_blocked_eveil: int = 0
    ok_liberation_batisseur_3j: int = 0
    ok_def1_global_fallback: int = 0
    ok_impasse_totale: int = 0
    # Distributions de choix pour détection des faux dilemmes (dil_*)
    dil_bug_passer: int = 0
    dil_bug_minus: int = 0
    dil_bug_plus: int = 0
    dil_mig_stay: int = 0
    dil_mig_foret: int = 0
    dil_mig_bug: int = 0
    dil_mig_colonie: int = 0
    dil_def1_foret: int = 0
    dil_def1_lisiere: int = 0
    dil_def1_furtivite: int = 0
    dil_def1_reve: int = 0
    dil_def2_foret: int = 0
    dil_def2_lisiere: int = 0
    dil_def2_furtivite: int = 0
    dil_def2_reve: int = 0
    dil_def2_gardien: int = 0
    dil_step2_turns_with_move: int = 0
    dil_step2_turns_zero_move: int = 0
    dil_ordre_constr_3_1: int = 0
    dil_ordre_nid_4_2: int = 0
    dil_ordre_att_5_1: int = 0
    dil_ordre_rat_5_2: int = 0
    dil_gardien_c1: int = 0
    dil_gardien_c2: int = 0
    dil_gardien_c3: int = 0
    dil_gardien_c4: int = 0
    dil_gardien_c5: int = 0
    dil_gardien_c6: int = 0
    # État transitoire du tour courant pour l'anatomie de l'Éveil
    _turn_strikes: int = 0
    _turn_reves_opened: int = 0
    _turn_trig_lit_mask: int = 0
    _turn_reveil_active: bool = False
    _turn_def_snap: tuple[int, int, int, int, int, int, int, int, int, int, int] | None = None
    _turn_pre5_snap: tuple[int, ...] | None = None
    # Accumulateurs Éveils réussis (rs_*)
    rs_count: int = 0
    rs_tour: int = 0
    rs_ratio_arbres_bp: int = 0
    rs_t1: int = 0
    rs_t2: int = 0
    rs_t3: int = 0
    rs_t4: int = 0
    rs_t5: int = 0
    rs_t6: int = 0
    rs_t7: int = 0
    rs_t8: int = 0
    rs_def_gardien: int = 0
    rs_def_parade: int = 0
    rs_def_resonance: int = 0
    rs_def_other_cases: int = 0
    rs_distinct_gardiens_bet: int = 0
    rs_def_reve: int = 0
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
    rs_reves_opened: int = 0
    rs_trig1_lit: int = 0
    rs_trig2_lit: int = 0
    rs_trig3_lit: int = 0
    rs_trig4_lit: int = 0
    rs_trig5_lit: int = 0
    rs_trig6_lit: int = 0
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
    # Accumulateurs tentatives d'Éveil échouées (rf_*)
    rf_count: int = 0
    rf_tour: int = 0
    rf_def_gardien: int = 0
    rf_def_parade: int = 0
    rf_def_resonance: int = 0
    rf_def_other_cases: int = 0
    rf_distinct_gardiens_bet: int = 0
    rf_def_reve: int = 0
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
    rf_reves_opened: int = 0
    rf_trig1_lit: int = 0
    rf_trig2_lit: int = 0
    rf_trig3_lit: int = 0
    rf_trig4_lit: int = 0
    rf_trig5_lit: int = 0
    rf_trig6_lit: int = 0
    rf_sabotage_in_deck: int = 0
    # Compteurs exacts d'activations réelles par emplacement (32 slots Mode 4 / socle)
    tile_activations: dict[str, int] = field(default_factory=dict)
    _turn_gardiens_seen_mask: int = 0
    _turn_reves_seen_mask: int = 0

    def record_tile_activation(self, slot_id: str, count: int = 1) -> None:
        """Incrémente le compteur d'activations réelles pour l'emplacement `slot_id`."""
        if count > 0 and slot_id:
            self.tile_activations[slot_id] = self.tile_activations.get(slot_id, 0) + count

    def _sync_turn_tile_activations(self, state: GameState) -> None:
        """Capture sans doublon intra-tour les Gardiens (G1..G15) et Rêves (R1..R10) ouverts."""
        for c in range(1, TRACK_LEN + 1):
            if state.has_gardien_opened_this_turn(c):
                g_num, _ = state.get_gardien_at_case(c)
                if g_num > 0:
                    bit = 1 << (g_num - 1)
                    if not (self._turn_gardiens_seen_mask & bit):
                        self._turn_gardiens_seen_mask |= bit
                        self.record_tile_activation(f"G{g_num}", 1)
        for r_num in range(1, 11):
            if state.has_reve_opened_this_turn(r_num):
                bit_r = 1 << (r_num - 1)
                if not (self._turn_reves_seen_mask & bit_r):
                    self._turn_reves_seen_mask |= bit_r
                    self.record_tile_activation(f"R{r_num}", 1)

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

    def _finalize_reveil_turn(
        self,
        state: GameState,
        *,
        succeeded: bool,
        ratio_arbres: float | None = None,
    ) -> None:
        if not self._turn_reveil_active or self._turn_pre5_snap is None:
            return
        self._turn_reveil_active = False
        pre5 = self._turn_pre5_snap
        self._turn_pre5_snap = None
        def_snap = self._turn_def_snap or (state.tour, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self._turn_def_snap = None

        (
            tour,
            def_gard,
            def_parade,
            def_res,
            def_other,
            distinct_g_bet,
            def_reve,
            def1_for,
            def2_for,
            def_furt,
            def_lis,
        ) = def_snap
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
        reves_opened = self._turn_reves_opened
        t_mask = self._turn_trig_lit_mask
        trig1_lit = 1 if (t_mask & (1 << 0)) else 0
        trig2_lit = 1 if (t_mask & (1 << 1)) else 0
        trig3_lit = 1 if (t_mask & (1 << 2)) else 0
        trig4_lit = 1 if (t_mask & (1 << 3)) else 0
        trig5_lit = 1 if (t_mask & (1 << 4)) else 0
        trig6_lit = 1 if (t_mask & (1 << 5)) else 0

        if succeeded:
            if ratio_arbres is None:
                init_tot = n * sum(state.cfg.dotation_arbres)
                ratio_arbres = state.total_arbres_plateau() / init_tot if init_tot > 0 else 0.0
            self.rs_count += 1
            self.rs_tour += tour
            self.rs_ratio_arbres_bp += round(ratio_arbres * 10000.0)
            if tour == 1:
                self.rs_t1 += 1
            elif tour == 2:
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
            self.rs_def_parade += def_parade
            self.rs_def_resonance += def_res
            self.rs_def_other_cases += def_other
            self.rs_distinct_gardiens_bet += distinct_g_bet
            self.rs_def_reve += def_reve
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
            self.rs_reves_opened += reves_opened
            self.rs_trig1_lit += trig1_lit
            self.rs_trig2_lit += trig2_lit
            self.rs_trig3_lit += trig3_lit
            self.rs_trig4_lit += trig4_lit
            self.rs_trig5_lit += trig5_lit
            self.rs_trig6_lit += trig6_lit
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
            self.reveil_failures += 1
            self.rf_count += 1
            self.rf_tour += tour
            self.rf_def_gardien += def_gard
            self.rf_def_parade += def_parade
            self.rf_def_resonance += def_res
            self.rf_def_other_cases += def_other
            self.rf_distinct_gardiens_bet += distinct_g_bet
            self.rf_def_reve += def_reve
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
            self.rf_reves_opened += reves_opened
            self.rf_trig1_lit += trig1_lit
            self.rf_trig2_lit += trig2_lit
            self.rf_trig3_lit += trig3_lit
            self.rf_trig4_lit += trig4_lit
            self.rf_trig5_lit += trig5_lit
            self.rf_trig6_lit += trig6_lit
            self.rf_sabotage_in_deck += sab_in_deck

    def on_furtivite_rive_executed(self, _cell_key: int, action_kind: str = "") -> None:
        """Enregistre l'exécution d'une rive Furtivité complète en 4.1."""
        self._turn_furt_total_rives_exec += 1
        if action_kind == "PIEGE":
            self.ok_furt_rive_piege += 1
        elif action_kind == "SABOTAGE":
            self.ok_furt_rive_sabotage += 1

    def on_furtivite_orphan_pawn(self, count: int = 1) -> None:
        """Enregistre un pion Défenseur resté seul (1/2) sur une rive en 4.1 (perdu à blanc)."""
        if count > 0:
            self.ok_furt_orphan_pawns += count

    def on_furtivite_failed_binome(self, count: int = 1, *, rive: str = "") -> None:
        """Enregistre un binôme 2/2 en 4.1 perdant son pari (Rive Piège hors m(r)==2 ou Rive Sabotage hors m(r)==0)."""
        if count > 0:
            self.ok_furt_failed_binomes += count
            if rive == "PIEGE":
                self.ok_furt_rive_piege_lost += count
            elif rive == "SABOTAGE":
                self.ok_furt_rive_sabotage_lost += count

    def on_furtivite_step_end(self) -> None:
        """Clôture le suivi des rives Furtivité résolues à l'Étape 4.1 pour le tour courant."""
        if self._turn_furt_total_rives_exec >= 1:
            self.furtivite_1_rive_turns += 1
        if self._turn_furt_total_rives_exec >= 2:
            self.ok_furt_multi_rive_turns += 1
        self._turn_furt_total_rives_exec = 0

    def on_charge_gain(self, count: int = 1, *, tour: int = 1) -> None:
        """Enregistre un gain de jeton Puissance issu du mode CHARGE."""
        if count > 0:
            self.charge_gains += count
            if tour <= 4:
                self.charge_gains_act1 += count
            else:
                self.charge_gains_act2 += count

    def on_charge_activation_resolved(
        self, *, gained_red: bool, all_parried: bool
    ) -> None:
        """Enregistre l'issue d'une activation de machine en mode CHARGE (gain ou 0 gain)."""
        self.ok_charge_activations += 1
        if not gained_red:
            self.ok_charge_zero_gain += 1
            if all_parried:
                self.ok_charge_zero_gain_parried += 1
            else:
                self.ok_charge_zero_gain_barren += 1

    def on_step2_def1_placed(self, target_kind: str) -> None:
        """Enregistre la famille de cible choisie en 2.1."""
        if target_kind == "FORET":
            self.dil_def1_foret += 1
        elif target_kind == "LISIERE":
            self.dil_def1_lisiere += 1
        elif target_kind == "FURTIVITE":
            self.dil_def1_furtivite += 1
        elif target_kind == "REVE_ACTIVATION":
            self.dil_def1_reve += 1
        elif target_kind == "PASSER_IMPASSE":
            self.ok_impasse_totale += 1

    def on_step2_revision_moved(self) -> None:
        """Signale qu'au moins un 2e Défenseur s'est déplacé durant les passes de révision 2.2."""
        self._turn_step2_moved = True

    def on_step2_locked_summary(self, state: GameState) -> None:
        """Enregistre la distribution finale des 2es Défenseurs verrouillés à la sortie de 2.2."""
        if self._turn_step2_moved:
            self.dil_step2_turns_with_move += 1
        else:
            self.dil_step2_turns_zero_move += 1
        self._turn_step2_moved = False
        for s in range(state.cfg.n_players):
            raw = state.get_player_def_loc_raw(s, 1)
            if raw == 0:
                continue
            kind, _a, _b, _c = state.decode_def_loc(raw)
            if kind == "FORET":
                self.dil_def2_foret += 1
            elif kind == "LISIERE":
                self.dil_def2_lisiere += 1
            elif kind == "FURTIVITE":
                self.dil_def2_furtivite += 1
            elif kind in ("REVE_ACTIVATION", "REVE_ACTIVATION_CONSUMED"):
                self.dil_def2_reve += 1
            elif kind in ("GARDIEN_PARI", "GARDIEN_PARI_CONSUMED"):
                self.dil_def2_gardien += 1
            elif kind == "IMPASSE":
                self.ok_impasse_totale += 1

    def on_migration_decision(self, dst_kind: str) -> None:
        """Enregistre le choix de migration 4.3 parmi >= 2 destinations légales."""
        if dst_kind == "RESTER":
            self.dil_mig_stay += 1
        else:
            self.ok_mig_moves += 1
            if dst_kind == "FORET":
                self.dil_mig_foret += 1
            elif dst_kind == "BUG":
                self.dil_mig_bug += 1
            elif dst_kind == "COLONIE":
                self.dil_mig_colonie += 1

    def on_bug_3_2_decision(self, choice: str) -> None:
        """Enregistre le choix de Déviation Synaptique 3.2 (PASSER / M_MOINS_1 / M_PLUS_1)."""
        if choice == "PASSER":
            self.dil_bug_passer += 1
        elif choice == "M_MOINS_1":
            self.dil_bug_minus += 1
        elif choice == "M_PLUS_1":
            self.dil_bug_plus += 1

    def on_gardien_case_chosen(self, case_1_6: int) -> None:
        """Enregistre la case 1..6 choisie à la construction d'un Gardien (si >= 2 cases libres)."""
        if case_1_6 == 1:
            self.dil_gardien_c1 += 1
        elif case_1_6 == 2:
            self.dil_gardien_c2 += 1
        elif case_1_6 == 3:
            self.dil_gardien_c3 += 1
        elif case_1_6 == 4:
            self.dil_gardien_c4 += 1
        elif case_1_6 == 5:
            self.dil_gardien_c5 += 1
        elif case_1_6 == 6:
            self.dil_gardien_c6 += 1

    def on_step_transition(self, state: GameState, prev_step: int, next_step: int) -> None:
        """Accumule `mem_debt_score` à chaque sous-étape traversée au sein d'un tour."""
        if prev_step == STEP_4_1_FURTIVITE and next_step == STEP_4_2_NIDS:
            self.on_furtivite_step_end()
        if prev_step == STEP_4_2_NIDS and next_step == STEP_4_3_MIGRATION:
            for nid_num in range(1, 6):
                if state.get_nid_position(nid_num) is not None:
                    self.record_tile_activation(f"M{nid_num}", 1)
        if prev_step in (STEP_3_2_REVEAL, STEP_5_3_END_CHECK) or next_step in (
            STEP_4_1_FURTIVITE,
            STEP_5_3_END_CHECK,
            STEP_6_2_EVOLUTION,
            STEP_6_3_END_TURN,
        ):
            self._sync_turn_tile_activations(state)
        if next_step == STEP_1_2_DEAL and prev_step == STEP_6_3_END_TURN:
            self._turn_closed = False
            self._turn_strikes = 0
            self._turn_reves_opened = 0
            self._turn_trig_lit_mask = 0
            self._turn_gardiens_seen_mask = 0
            self._turn_reves_seen_mask = 0
            self._turn_reveil_active = False
            self._turn_def_snap = None
            self._turn_pre5_snap = None
            self._turn_furt_total_rives_exec = 0
            self._turn_step2_moved = False
            return
        if next_step == STEP_5_1_TACTIQUES:
            self._turn_strikes = 0
            if self._turn_reveil_active:
                self._snapshot_pre_step5(state)
        elif (
            next_step == STEP_6_2_EVOLUTION
            and self._turn_reveil_active
            and self._turn_pre5_snap is not None
        ):
            self._finalize_reveil_turn(state, succeeded=False)
        if prev_step != STEP_GAME_OVER:
            self.mem_debt_score += count_active_transient_modifiers(state)

    def on_game_over_ratio(self, state: GameState, *, cause: str, ratio_arbres: float) -> None:
        """Finalise l'anatomie d'Éveil, les jetons Puissance et les reliquats Ockham de fin de partie."""
        self._sync_turn_tile_activations(state)
        tot_pow = state.total_power_tokens_plateau()
        if state.tour >= 4 and self.act1_reached == 0:
            self.power_tokens_end_act1 = tot_pow
            self.act1_reached = 1
        self.power_tokens_end_game = tot_pow

        # Reliquats inutilisés en fin de partie (Pièges, Insectes Forêt/Bug/Colonie, Sabotages)
        n = state.cfg.n_players
        p_max = state.cfg.p_max
        unused_pieges = 0
        unused_ins_board = 0
        for r in range(n):
            for p in range(1, p_max + 1):
                if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                    unused_pieges += 1
                unused_ins_board += state.get_parcel_insectes(r, p)
        unused_bugs = 0
        unused_colonie = 0
        for c in range(1, TRACK_LEN + 1):
            unused_bugs += state.get_bugs_at_case(c)
            unused_colonie += state.get_colonie_at_case(c)

        self.ok_pieges_unused_end = unused_pieges
        self.ok_insectes_foret_unused_end = unused_ins_board
        self.ok_bugs_unused_end = unused_bugs
        self.ok_colonie_unused_end = unused_colonie
        wasted_bugs = min(self.dil_mig_bug, unused_bugs)
        wasted_col = min(self.dil_mig_colonie, unused_colonie)
        wasted_wheel = min(self.dil_mig_foret, unused_ins_board)
        self.ok_mig_wasted_end = wasted_bugs + wasted_col + wasted_wheel
        self.ok_sabotage_unrevealed_end = max(
            0, self.ok_sabotage_acquired - self.da_sabotage_revele
        )

        if self._turn_reveil_active and self._turn_pre5_snap is not None:
            self._finalize_reveil_turn(
                state,
                succeeded=(cause == "REVEIL_GARDIENS"),
                ratio_arbres=ratio_arbres,
            )

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
        state: GameState,
        *,
        repasses: int,
        opened: int,
        in_combat: bool,
        opened_in_later_pass: int = 0,
    ) -> None:
        """Enregistre une fenêtre de balayage `sweep_gardiens` (repassages 1->6 et ouvertures)."""
        self.interrupt_windows_count += 1
        self.cascade_sweeps += repasses
        self.gardiens_opened_total += opened
        if opened > 0:
            self._sync_turn_tile_activations(state)
        if opened_in_later_pass > 0:
            self.ok_cascade_second_pass_sweeps += 1
        if in_combat and opened > 0:
            self.mid_combat_interrupts += opened

    def on_gardien_bets_resolved(
        self, _state: GameState, *, bets_won: int, bets_lost: int
    ) -> None:
        """Enregistre les paris d'activation Gardiens gagnés et perdus en 5.3."""
        self.gardien_bets_won += bets_won
        self.gardien_bets_lost += bets_lost

    def on_reveil_attempt(self, state: GameState) -> None:
        """Enregistre un tour de tentative d'Éveil (N Défenseurs engagés sur la Piste des Gardiens en 2.2)."""
        self.reveil_attempts += 1
        self._turn_reveil_active = True
        def_gard = 0
        def_parade = 0
        def_res = 0
        def_other = 0
        distinct_gardien_cases: set[int] = set()
        def_reve = 0
        def1_for = 0
        def2_for = 0
        def_furt = 0
        def_lis = 0
        for s in range(state.cfg.n_players):
            for def_idx in (0, 1):
                kind, a, _b, _c = state.decode_def_loc(state.get_player_def_loc_raw(s, def_idx))
                if kind in ("GARDIEN_PARI", "GARDIEN_PARI_CONSUMED"):
                    def_gard += 1
                    distinct_gardien_cases.add(a)
                    if a == 1:
                        def_parade += 1
                    if a == 4:
                        def_res += 1
                    else:
                        def_other += 1
                elif kind in ("REVE_ACTIVATION", "REVE_ACTIVATION_CONSUMED"):
                    def_reve += 1
                elif kind == "FORET":
                    if def_idx == 0:
                        def1_for += 1
                    else:
                        def2_for += 1
                elif kind == "FURTIVITE":
                    def_furt += 1
                elif kind == "LISIERE":
                    def_lis += 1
        self._turn_def_snap = (
            state.tour,
            def_gard,
            def_parade,
            def_res,
            def_other,
            len(distinct_gardien_cases),
            def_reve,
            def1_for,
            def2_for,
            def_furt,
            def_lis,
        )

    def on_reveil_failure(self, _state: GameState) -> None:
        """Enregistre explicitement l'échec d'une tentative d'Éveil."""
        self.reveil_failures += 1

    def on_bouclier_lisiere_save(self, count: int = 1) -> None:
        """Enregistre le nombre de Gardiens sauvés du retour en lisière par Bouclier de lisière en 5.3."""
        if count > 0:
            self.bouclier_lisiere_saves += count
            self.ok_bouclier_saves += count
            self.record_tile_activation("SLOT_COLONISATION_GARDIENS", count)

    def on_trigger_lit(self, case_num: int) -> None:
        """Enregistre l'allumage de chacune des 6 cases déclencheurs 1..6 durant le tour."""
        if 1 <= case_num <= TRACK_LEN:
            self._turn_trig_lit_mask |= 1 << (case_num - 1)

    def on_reve_activated(self, count: int = 1) -> None:
        """Enregistre une ouverture de Rêve activée en Étape 3.2."""
        if count > 0:
            self.reves_activated += count
            self._turn_reves_opened += count

    def on_machines_cancelled_by_reve(self, count: int) -> None:
        """Enregistre les cartes Machine annulées par un Rêve activé en Étape 3.2."""
        if count > 0:
            self.machines_cancelled_by_reve += count
            self.da_reve_annulation += count

    def on_machines_bypassed_inactive_reve(self, count: int) -> None:
        """Enregistre les cartes Machine exécutant la Tactique imprimée sous un Rêve inactif."""
        if count > 0:
            self.machines_bypassed_inactive_reve += count

    def on_defense_parade_classique(self, count: int = 1) -> None:
        """Enregistre les frappes parées par Défenseurs seuls (ou parade auto Jaguar/Harpie)."""
        if count > 0:
            self.da_parade_classique += count

    def on_defense_piege(self, count: int = 1) -> None:
        """Enregistre les frappes neutralisées par un Piège armé en 5.1/5.2."""
        if count > 0:
            self.da_piege += count

    def on_defense_parade_avec_insectes(self, count: int = 1) -> None:
        """Enregistre les frappes parées via Parade classique en défaussant >= 1 Insecte."""
        if count > 0:
            self.da_parade_avec_insectes += count

    def on_defense_sabotage_revele(self, count: int = 1) -> None:
        """Enregistre les cartes Sabotage révélées en 3.2 (activation machine neutralisée)."""
        if count > 0:
            self.da_sabotage_revele += count

    def on_defense_bug_deviation(self, count: int = 1) -> None:
        """Enregistre les déviations de dé M par Insecte sur la Piste des Tactiques en 3.2."""
        if count > 0:
            self.da_insecte_bug_deviation += count
            self.record_tile_activation("SLOT_BUG_CERVEAU", count)

    def on_defense_repousse_finale(self, trees_regrown: int) -> None:
        """Enregistre le nombre total d'Arbres repoussés depuis les Souches en fin de partie."""
        if trees_regrown > 0:
            self.da_arbres_repousse_finale += trees_regrown

    def on_end_turn(self, state: GameState, *, game_over: bool) -> None:
        """Clôture le ratio `physical_ops / max(1, decisions_joueurs)` du tour écoulé."""
        self._sync_turn_tile_activations(state)
        if not game_over and state.tour == 4 and self.act1_reached == 0:
            self.power_tokens_end_act1 = state.total_power_tokens_plateau()
            self.act1_reached = 1
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
        """Retourne l'instantané immuable des capteurs de la partie."""
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
            gardien_bets_won=self.gardien_bets_won,
            gardien_bets_lost=self.gardien_bets_lost,
            bouclier_lisiere_saves=self.bouclier_lisiere_saves,
            reves_activated=self.reves_activated,
            machines_cancelled_by_reve=self.machines_cancelled_by_reve,
            machines_bypassed_inactive_reve=self.machines_bypassed_inactive_reve,
            da_parade_classique=self.da_parade_classique,
            da_piege=self.da_piege,
            da_parade_avec_insectes=self.da_parade_avec_insectes,
            da_reve_annulation=self.da_reve_annulation,
            da_sabotage_revele=self.da_sabotage_revele,
            da_insecte_bug_deviation=self.da_insecte_bug_deviation,
            da_arbres_repousse_finale=self.da_arbres_repousse_finale,
            power_tokens_end_act1=self.power_tokens_end_act1,
            act1_reached=self.act1_reached,
            power_tokens_end_game=self.power_tokens_end_game,
            charge_gains=self.charge_gains,
            charge_gains_act1=self.charge_gains_act1,
            charge_gains_act2=self.charge_gains_act2,
            furtivite_1_rive_turns=self.furtivite_1_rive_turns,
            ok_furt_rive_piege=self.ok_furt_rive_piege,
            ok_furt_rive_sabotage=self.ok_furt_rive_sabotage,
            ok_furt_rive_piege_lost=self.ok_furt_rive_piege_lost,
            ok_furt_rive_sabotage_lost=self.ok_furt_rive_sabotage_lost,
            ok_furt_orphan_pawns=self.ok_furt_orphan_pawns,
            ok_furt_failed_binomes=self.ok_furt_failed_binomes,
            ok_furt_multi_rive_turns=self.ok_furt_multi_rive_turns,
            ok_pieges_placed=self.ok_pieges_placed,
            ok_pieges_triggered=self.ok_pieges_triggered,
            ok_pieges_unused_end=self.ok_pieges_unused_end,
            ok_pont_routier_jumps=self.ok_pont_routier_jumps,
            ok_routes_created=self.ok_routes_created,
            ok_repli_bordure=self.ok_repli_bordure,
            ok_repli_coeur_exception=self.ok_repli_coeur_exception,
            ok_retrait_definitif_machine=self.ok_retrait_definitif_machine,
            ok_abatteuse_ratissage_0_arbre=self.ok_abatteuse_ratissage_0_arbre,
            ok_contact_nid_renvois=self.ok_contact_nid_renvois,
            ok_contact_nid_insectes_perdus=self.ok_contact_nid_insectes_perdus,
            ok_penurie_cartes_machine=self.ok_penurie_cartes_machine,
            ok_charge_activations=self.ok_charge_activations,
            ok_charge_zero_gain=self.ok_charge_zero_gain,
            ok_charge_zero_gain_parried=self.ok_charge_zero_gain_parried,
            ok_charge_zero_gain_barren=self.ok_charge_zero_gain_barren,
            ok_ratissage_entries_6_3=self.ok_ratissage_entries_6_3,
            ok_ratissage_activations=self.ok_ratissage_activations,
            ok_sabotage_acquired=self.ok_sabotage_acquired,
            ok_sabotage_unrevealed_end=self.ok_sabotage_unrevealed_end,
            ok_mig_moves=self.ok_mig_moves,
            ok_mig_wasted_end=self.ok_mig_wasted_end,
            ok_bugs_unused_end=self.ok_bugs_unused_end,
            ok_colonie_unused_end=self.ok_colonie_unused_end,
            ok_insectes_foret_unused_end=self.ok_insectes_foret_unused_end,
            ok_bouclier_saves=self.ok_bouclier_saves,
            ok_gardien_return_lisiere=self.ok_gardien_return_lisiere,
            ok_gardien_face2_upgrades=self.ok_gardien_face2_upgrades,
            ok_cascade_case4_openings=self.ok_cascade_case4_openings,
            ok_cascade_second_pass_sweeps=self.ok_cascade_second_pass_sweeps,
            ok_tour8_blocked_sommeil=self.ok_tour8_blocked_sommeil,
            ok_tour8_blocked_eveil=self.ok_tour8_blocked_eveil,
            ok_liberation_batisseur_3j=self.ok_liberation_batisseur_3j,
            ok_def1_global_fallback=self.ok_def1_global_fallback,
            ok_impasse_totale=self.ok_impasse_totale,
            dil_bug_passer=self.dil_bug_passer,
            dil_bug_minus=self.dil_bug_minus,
            dil_bug_plus=self.dil_bug_plus,
            dil_mig_stay=self.dil_mig_stay,
            dil_mig_foret=self.dil_mig_foret,
            dil_mig_bug=self.dil_mig_bug,
            dil_mig_colonie=self.dil_mig_colonie,
            dil_def1_foret=self.dil_def1_foret,
            dil_def1_lisiere=self.dil_def1_lisiere,
            dil_def1_furtivite=self.dil_def1_furtivite,
            dil_def1_reve=self.dil_def1_reve,
            dil_def2_foret=self.dil_def2_foret,
            dil_def2_lisiere=self.dil_def2_lisiere,
            dil_def2_furtivite=self.dil_def2_furtivite,
            dil_def2_reve=self.dil_def2_reve,
            dil_def2_gardien=self.dil_def2_gardien,
            dil_step2_turns_with_move=self.dil_step2_turns_with_move,
            dil_step2_turns_zero_move=self.dil_step2_turns_zero_move,
            dil_ordre_constr_3_1=self.dil_ordre_constr_3_1,
            dil_ordre_nid_4_2=self.dil_ordre_nid_4_2,
            dil_ordre_att_5_1=self.dil_ordre_att_5_1,
            dil_ordre_rat_5_2=self.dil_ordre_rat_5_2,
            dil_gardien_c1=self.dil_gardien_c1,
            dil_gardien_c2=self.dil_gardien_c2,
            dil_gardien_c3=self.dil_gardien_c3,
            dil_gardien_c4=self.dil_gardien_c4,
            dil_gardien_c5=self.dil_gardien_c5,
            dil_gardien_c6=self.dil_gardien_c6,
            rs_count=self.rs_count,
            rs_tour=self.rs_tour,
            rs_ratio_arbres_bp=self.rs_ratio_arbres_bp,
            rs_t1=self.rs_t1,
            rs_t2=self.rs_t2,
            rs_t3=self.rs_t3,
            rs_t4=self.rs_t4,
            rs_t5=self.rs_t5,
            rs_t6=self.rs_t6,
            rs_t7=self.rs_t7,
            rs_t8=self.rs_t8,
            rs_def_gardien=self.rs_def_gardien,
            rs_def_parade=self.rs_def_parade,
            rs_def_resonance=self.rs_def_resonance,
            rs_def_other_cases=self.rs_def_other_cases,
            rs_distinct_gardiens_bet=self.rs_distinct_gardiens_bet,
            rs_def_reve=self.rs_def_reve,
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
            rs_reves_opened=self.rs_reves_opened,
            rs_trig1_lit=self.rs_trig1_lit,
            rs_trig2_lit=self.rs_trig2_lit,
            rs_trig3_lit=self.rs_trig3_lit,
            rs_trig4_lit=self.rs_trig4_lit,
            rs_trig5_lit=self.rs_trig5_lit,
            rs_trig6_lit=self.rs_trig6_lit,
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
            rf_def_parade=self.rf_def_parade,
            rf_def_resonance=self.rf_def_resonance,
            rf_def_other_cases=self.rf_def_other_cases,
            rf_distinct_gardiens_bet=self.rf_distinct_gardiens_bet,
            rf_def_reve=self.rf_def_reve,
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
            rf_reves_opened=self.rf_reves_opened,
            rf_trig1_lit=self.rf_trig1_lit,
            rf_trig2_lit=self.rf_trig2_lit,
            rf_trig3_lit=self.rf_trig3_lit,
            rf_trig4_lit=self.rf_trig4_lit,
            rf_trig5_lit=self.rf_trig5_lit,
            rf_trig6_lit=self.rf_trig6_lit,
            rf_sabotage_in_deck=self.rf_sabotage_in_deck,
            tile_activations=tuple(sorted(self.tile_activations.items())),
        )
