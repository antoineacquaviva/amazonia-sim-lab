"""Économie unifiée de B2 en monnaie unique « arbres marginalement sauvés » (100 % stdlib PyPy 3.11).

Toutes les constantes d'équilibrage de B2 sont centralisées dans `B2Weights` (< 100 paramètres nommés),
exprimées en équivalent-arbres (`1.0` = 1 arbre marginalement sauvé).
La conversion vers l'échelle centi-arbres (`TREE_SCORE_UNIT = 100.0`) assure la compatibilité exacte
avec les seuils de révision (`epsilon_base = 24.0` = 0,24 arbre) et le harnais existant.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, ClassVar

from bots.belief_and_ticks import (
    BeliefSummary,
    any_tile_text_active,
    is_tile_text_active,
)
from engine.state import (
    CANONICAL_DOTATION,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    FAMILLE_CROISSANCE,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    GARDIEN_BET_CAP,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TRACK_LEN,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_RESONANCE,
    TRIG_REVE,
    GameConfig,
    PlayerObservation,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    machine_card_code,
    resolve_reve_rank_cancellations,
    unpack_machine_card,
)

__all__ = (
    "ALL_ACTIVE_RESOURCES",
    "DEFAULT_B2_WEIGHTS",
    "TREE_SCORE_UNIT",
    "B2Weights",
    "EconomieNode",
    "ForestMarginalBreakdown",
    "any_tile_text_active",
    "best_untrapped_parcel_trees",
    "compute_b2_resource_and_trigger_values_trees",
    "estimate_expected_gardien_triggers",
    "furtivite_ray_deduction",
    "get_economie_catalog",
    "is_own_hand_covered",
    "is_tile_text_active",
    "score_forest_marginal_trees",
    "score_gardien_pari_marginal_trees",
    "score_lisiere_marginal_trees",
    "score_reve_marginal_trees",
    "score_target_b2_trees",
    "score_tile_construction_trees",
)

# 1.0 arbre marginalement sauvé == 100.0 centi-arbres sur l'échelle de révision
TREE_SCORE_UNIT: float = 100.0

ALL_ACTIVE_RESOURCES: tuple[str, ...] = (
    "RES_INSECTE",
    "RES_PIEGE",
    "RES_DEFENSEUR",
    "RES_JETON_BLEU",
    "RES_JETON_ROUGE",
    "RES_SEUIL_PARADE",
    "RES_DILUTION_SABOTAGE",
    "RES_SOUCHE",
    "RES_ARBRE",
    "RES_POSITION_MACHINE",
    "RES_POSITION_PISTE",
)

# Loi exacte de M = min(D1, D2) sur 2D6 équilibrés : P(M = k) = (13 - 2k) / 36 pour k = 1..6
_MIN_2D6_PROBS: tuple[float, ...] = (
    11.0 / 36.0,
    9.0 / 36.0,
    7.0 / 36.0,
    5.0 / 36.0,
    3.0 / 36.0,
    1.0 / 36.0,
)


@dataclass(frozen=True, slots=True)
class B2Weights:
    """Jeu unique et centralisé des constantes de B2 (< 100 paramètres), toutes en équivalent-arbres."""

    # --- 1. Forêt & combat discret (14 paramètres) ---
    forest_base_trees: float = 0.25
    forest_trapped_base_trees: float = 0.15
    route_penalty_trees: float = 1.15
    charge_penalty_early: float = 1.25
    charge_penalty_mid: float = 0.95
    charge_penalty_late: float = 0.45
    insect_saved_trees: float = 0.35
    souche_saved_trees: float = 0.12
    own_ray_trees: float = 0.15
    nid_base_trees: float = 1.65
    coop_gap2_share: float = 0.68
    coop_gap2_held_share: float = 0.50
    coop_gap3_share: float = 0.32
    held_completion_bonus: float = 0.30

    # --- 2. Économie des ressources & déclencheurs Gardiens (16 paramètres) ---
    res_arbre_w: float = 1.00
    res_souche_w: float = 0.12
    res_defenseur_w: float = 0.48
    res_piege_w: float = 0.72
    res_insecte_w: float = 0.35
    res_seuil_w: float = 0.45
    res_bleu_w: float = 0.48
    res_rouge_w: float = 0.55
    res_pos_mach_w: float = 0.48
    res_pos_piste_w: float = 0.52
    sabotage_turn1_trees: float = 1.85
    sabotage_decay_exp: float = 1.15
    trig_open_trees: float = 0.30
    trig_resonance_share: float = 0.48
    trig_chain_share: float = 0.32
    econ_output_share: float = 0.22

    # --- 3. Construction de Lisières (9 paramètres) ---
    lisiere_complete_base: float = 1.65
    lisiere_complete_mult: float = 0.65
    lisiere_solo_held_base: float = 0.40
    lisiere_open_covered_base: float = 1.25
    lisiere_open_default_base: float = 0.48
    lisiere_reve_struct: float = 0.95
    lisiere_croissance_struct: float = 0.85
    lisiere_gardien_eveil_struct: float = 0.80
    lisiere_gardien_mode4_struct: float = 0.72

    # --- 4. Furtivité : Rive Piège & Rive Sabotage (11 paramètres) ---
    furt_piege_complete_base: float = 1.95
    furt_piege_open_certain_base: float = 1.50
    furt_piege_signal_base: float = 0.92
    furt_trap_value_mult: float = 0.38
    furt_sab_complete_base: float = 1.55
    furt_sab_open_base: float = 1.10
    furt_sab_waste_penalty: float = 0.42
    furt_scarcity_completed: float = 0.95
    furt_scarcity_other_rive: float = 0.85
    furt_scarcity_open: float = 0.65
    furt_trap_seuil_bonus: float = 0.32

    # --- 5. Activation de Rêves (9 paramètres) ---
    reve_base_trees: float = 0.85
    reve_advance_trees: float = 0.48
    reve_piege_saved_trees: float = 0.35
    reve_trig5_trees: float = 0.40
    reve_flex_21_trees: float = 0.42
    reve_eveil_arm_n56_trees: float = 2.85
    reve_eveil_arm_n34_trees: float = 2.15
    reve_speculative_trees: float = 1.45
    reve_ally_decay: float = 0.85

    # --- 6. Pari Gardiens & Éveil de la Forêt (10 paramètres) ---
    eveil_finish_trees: float = 4.20
    eveil_progress_trees: float = 2.75
    eveil_start_trees: float = 2.15
    eveil_tree_ratio_scale: float = 1.75
    eveil_n56_mult: float = 1.22
    eveil_n34_caution_mult: float = 0.82
    gardien_mode4_probable_trees: float = 1.05
    gardien_mode4_face1_bonus: float = 0.25
    gardien_mode4_marginal_trees: float = 0.55
    gardien_bouclier_trees: float = 0.18

    def charge_penalty_for_tour(self, tour: int) -> float:
        if tour <= 2:
            return self.charge_penalty_early
        if tour <= 4:
            return self.charge_penalty_mid
        if tour <= 6:
            return self.charge_penalty_late
        if tour == 7:
            return 0.25 * self.charge_penalty_late
        return 0.0

    def sabotage_value_for_tour(self, tour: int) -> float:
        if tour >= 8:
            return 0.0
        frac = max(0.0, float(8 - tour) / 7.0)
        return self.sabotage_turn1_trees * (frac**self.sabotage_decay_exp)

    @classmethod
    def param_count(cls) -> int:
        return len(fields(cls))


assert B2Weights.param_count() < 100, f"B2Weights dépasse 100 paramètres : {B2Weights.param_count()}"

DEFAULT_B2_WEIGHTS: B2Weights = B2Weights()


@dataclass(frozen=True, slots=True)
class EconomieNode:
    """Nœud immuable du graphe orienté `economie_bot` extrait de spec_bundle_v6_0.json."""

    slot_id: str
    profile: str
    famille: str
    peuple_origine: str
    role: str
    portee: str
    is_law: bool
    cablage: tuple[int, ...]
    inputs_requis: tuple[str, ...]
    outputs_produits: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ForestMarginalBreakdown:
    """Décomposition transparente en équivalent-arbres d'une pose Forêt sur `(r, p)`."""

    immediate_trees_saved: float
    route_avoided_trees: float
    charge_denied_trees: float
    insect_saved_trees: float
    souche_saved_trees: float
    trigger_trees: float
    coop_staging_trees: float
    nid_trees: float
    total_trees: float


class _EconomieCache:
    catalog: ClassVar[dict[tuple[str, str], EconomieNode] | None] = None
    last_obs: ClassVar[PlayerObservation | None] = None
    last_cfg: ClassVar[GameConfig | None] = None
    last_weights: ClassVar[B2Weights | None] = None
    last_res: ClassVar[dict[str, float]] = {}
    last_trigs: ClassVar[tuple[float, ...]] = ()


def get_economie_catalog() -> dict[tuple[str, str], EconomieNode]:
    """Charge une seule fois le graphe orienté `economie_bot` (purgé de `RES_APPRENTISSAGE`)."""
    if _EconomieCache.catalog is not None:
        return _EconomieCache.catalog

    data_dir = Path(__file__).resolve().parent.parent / "data"
    spec_path = data_dir / "spec_bundle_v6_0.json"
    if not spec_path.is_file():
        spec_path = data_dir / "spec_bundle_v5_5.json"
    raw = json.loads(spec_path.read_text(encoding="utf-8"))
    cat = raw["catalogue_tuiles"]
    nodes: dict[tuple[str, str], EconomieNode] = {}

    for slot_id, slot_val in cat.items():
        fam = str(slot_val.get("famille", ""))
        orig = str(slot_val.get("peuple_origine", ""))
        for prof_key, prof_val in slot_val.get("profils", {}).items():
            eb = prof_val.get("economie_bot") or {}
            prim_str = str(prof_val.get("primitive", "")).upper()
            fen_str = str(prof_val.get("fenetre", "")).upper()
            is_law = ("MOD_LOI_DU_COEUR" in prim_str) or ("LOI" in fen_str)
            cab_raw = prof_val.get("cablage") or []
            cablage = tuple(int(x) for x in cab_raw) if isinstance(cab_raw, list) else ()
            nodes[(slot_id, prof_key)] = EconomieNode(
                slot_id=slot_id,
                profile=prof_key,
                famille=fam,
                peuple_origine=orig,
                role=str(eb.get("role", "MODULATEUR")),
                portee=str(eb.get("portee", "LOCAL_RAYON")),
                is_law=is_law,
                cablage=cablage,
                inputs_requis=tuple(
                    str(x) for x in eb.get("inputs_requis", []) if str(x) != "RES_APPRENTISSAGE"
                ),
                outputs_produits=tuple(
                    str(x) for x in eb.get("outputs_produits", []) if str(x) != "RES_APPRENTISSAGE"
                ),
            )

    _EconomieCache.catalog = nodes
    return nodes


def _next_non_razed_obs(obs: PlayerObservation, p_max: int, ray: int, from_p: int) -> int | None:
    for p_c in range(from_p + 1, p_max + 1):
        if not obs.is_route(ray, p_c):
            return p_c
    return None


def compute_b2_resource_and_trigger_values_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> tuple[dict[str, float], tuple[float, ...]]:
    """Calcule les valeurs marginales en équivalent-arbres des 11 `RES_*` actifs et de `TRIG_1..6`."""
    _ = belief
    if (
        _EconomieCache.last_obs is obs
        and _EconomieCache.last_cfg is cfg
        and _EconomieCache.last_weights is weights
    ):
        return _EconomieCache.last_res, _EconomieCache.last_trigs

    n = obs.n_players
    p_max = cfg.p_max
    tour = obs.tour
    machines = obs.machines
    gardiens = obs.piste_gardiens

    fragile_parcels = 0
    total_insects = 0
    total_rouges = 0
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            m_obs = machines[r * 2 + mt]
            if m_obs.status != MACHINE_STATUS_RETIRED and m_obs.position > 0:
                total_rouges += m_obs.rouges
        for p in range(1, p_max + 1):
            if obs.is_route(r, p):
                continue
            arb = obs.parcel_arbres(r, p)
            total_insects += obs.parcel_insectes(r, p)
            if arb <= 1:
                fragile_parcels += 1

    frag_scale = 0.04 * fragile_parcels
    total_reves_cfg = cfg.total_reves_partie
    active_reves_ranks = [
        r_idx + 1
        for r_idx in range(TRACK_LEN)
        if is_reve_code(obs.tactique_code_bugs(r_idx)[0])
        and is_tile_text_active(cfg, obs.piste_tactiques[r_idx].tile_id)
    ]
    active_reves_in_head = sum(1 for rk in active_reves_ranks if rk <= total_reves_cfg)

    if total_reves_cfg > 0 and len(active_reves_ranks) >= total_reves_cfg:
        reve_push_mult = 1.65 if active_reves_in_head >= total_reves_cfg - 1 else 1.35
    elif total_reves_cfg > 0 and len(active_reves_ranks) > 0:
        reve_push_mult = 1.20
    else:
        reve_push_mult = 1.0

    res_val: dict[str, float] = {
        "RES_ARBRE": weights.res_arbre_w + frag_scale,
        "RES_SOUCHE": weights.res_souche_w,
        "RES_DEFENSEUR": weights.res_defenseur_w + 0.5 * frag_scale,
        "RES_PIEGE": weights.res_piege_w + 0.04 * total_rouges,
        "RES_INSECTE": weights.res_insecte_w * (1.15 if total_insects < 2 * n else 0.78),
        "RES_SEUIL_PARADE": weights.res_seuil_w + 0.5 * frag_scale,
        "RES_JETON_BLEU": weights.res_bleu_w + (0.18 if tour <= 6 else 0.06),
        "RES_JETON_ROUGE": weights.res_rouge_w + 0.06 * max(0, 8 - tour),
        "RES_DILUTION_SABOTAGE": weights.sabotage_value_for_tour(tour),
        "RES_POSITION_MACHINE": weights.res_pos_mach_w + 0.5 * frag_scale,
        "RES_POSITION_PISTE": weights.res_pos_piste_w * reve_push_mult,
    }

    trig_val = [0.10] * (TRACK_LEN + 1)
    if obs.mode >= 2:
        has_any_text = any_tile_text_active(cfg)
        econ = get_economie_catalog() if has_any_text else None
        for c in range(1, TRACK_LEN + 1):
            g_slot = gardiens[c - 1]
            if g_slot.gardien_num > 0 and g_slot.remaining_defenders >= 1 and g_slot.tile_id is not None:
                g_text_active = is_tile_text_active(cfg, g_slot.tile_id)
                awaken_g = 0.40 if (obs.gardien_pari_enabled and g_text_active and g_slot.face == 1) else 0.0
                v_open = weights.trig_open_trees + awaken_g
                if econ is not None and g_text_active:
                    prof = cfg.profile_for_slot(g_slot.tile_id)
                    node = econ.get((g_slot.tile_id, prof)) if prof is not None else None
                    if node is not None:
                        v_open += sum(
                            res_val.get(out_tok, 0.18) * weights.econ_output_share
                            for out_tok in node.outputs_produits
                        )
                trig_val[c] = v_open

        res_6 = trig_val[TRIG_RESONANCE] if obs.gardien_available_at_case(TRIG_RESONANCE) else 0.0
        for c in range(1, TRACK_LEN + 1):
            if c != TRIG_RESONANCE and obs.gardien_available_at_case(c):
                trig_val[c] += weights.trig_resonance_share * res_6
            if econ is not None:
                g_slot = gardiens[c - 1]
                if g_slot.tile_id is not None and g_slot.remaining_defenders >= 1:
                    prof = cfg.profile_for_slot(g_slot.tile_id)
                    node = econ.get((g_slot.tile_id, prof)) if prof is not None else None
                    if node is not None:
                        for out_tok in node.outputs_produits:
                            if out_tok.startswith("TRIG_"):
                                t_idx = int(out_tok[5:])
                                if t_idx != c and 1 <= t_idx <= 6:
                                    trig_val[c] += weights.trig_chain_share * trig_val[t_idx]

    trigs_tuple = tuple(trig_val[1:])
    _EconomieCache.last_obs = obs
    _EconomieCache.last_cfg = cfg
    _EconomieCache.last_weights = weights
    _EconomieCache.last_res = res_val
    _EconomieCache.last_trigs = trigs_tuple
    return res_val, trigs_tuple


# ---------------------------------------------------------------------------
# Phase isolée Forêt : évaluateur exact par scénarios discrets de frappes
# ---------------------------------------------------------------------------


def _machine_discrete_strike_dist(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    m_type: int,
    target_p: int,
) -> tuple[tuple[int, bool, float], ...]:
    """Distribution discrète des frappes `(seuil, is_charge, prob)` de `(ray, m_type)` sur `(ray, target_p)`.

    Retourne une liste de scénarios mutuellement exclusifs (la somme des probabilités <= 1.0 ;
    le complément `1 - sum(p)` correspond au scénario « pas de frappe »).
    """
    pos, st = obs.machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos <= 0 or obs.is_route(ray, target_p):
        return ()

    p_max = cfg.p_max
    base_seuil = CANONICAL_DOTATION[target_p - 1]
    eff_red = obs.machine_effective_rouges(ray, m_type)
    bleus = obs.machines[ray * 2 + m_type].bleus

    if st == MACHINE_STATUS_RATISSAGE:
        if pos != target_p:
            return ()
        s_rat = max(1, base_seuil + eff_red - bleus)
        return ((s_rat, False, 1.0),)

    # Machine NORMAL : vérifier quels rangs 1..6 frappent target_p
    hits_sp = pos == target_p
    p_dev = _next_non_razed_obs(obs, p_max, ray, pos)
    hits_dev = p_dev == target_p
    if not (hits_sp or hits_dev):
        return ()

    card_code = machine_card_code(ray, m_type)
    n = obs.n_players
    own_seat = obs.observer_seat

    # Vérifier si la carte est dans une main visible (own_seat ou paravents ouverts)
    holder_seat = -1
    holder_lec = 0
    unknown_holders = 0
    known_cards_cnt = 0
    known_sab_cnt = 0
    for s in range(n):
        h = obs.hand_of(s)
        if not h.has_card:
            continue
        if h.card is None:
            unknown_holders += 1
        elif h.card in (CARD_SABOTAGE, CARD_ECAILLE):
            known_sab_cnt += 1
        elif 1 <= h.card <= 2 * n:
            known_cards_cnt += 1
            if h.card == card_code:
                holder_seat = s
                holder_lec = h.lecture_m or 0

    by_outcome: dict[tuple[int, bool], float] = {}

    if holder_seat >= 0:
        if not (1 <= holder_lec <= TRACK_LEN):
            return ()
        spec = TACTIQUES_SPEC[holder_lec]
        hits_here = ("SUR_PLACE" in spec.cibles and hits_sp) or (
            "DEVANT" in spec.cibles and hits_dev
        )
        if not hits_here:
            return ()
        t_code, _ = obs.tactique_code_bugs(holder_lec - 1)
        p_exec = 1.0
        if is_reve_code(t_code):
            n_def_r = obs.reve_activation_defenders(holder_lec)
            if n_def_r >= 1:
                if obs.paravents_ouverts:
                    rank_entries: list[tuple[int, int, int, int]] = []
                    for s_k in range(n):
                        hk = obs.hand_of(s_k)
                        if (
                            hk.has_card
                            and hk.card is not None
                            and 1 <= hk.card <= 2 * n
                            and hk.lecture_m == holder_lec
                        ):
                            rk, mtk = unpack_machine_card(hk.card)
                            pk, stk = obs.machine_pos_status(rk, mtk)
                            if stk == MACHINE_STATUS_NORMAL and pk > 0:
                                rank_entries.append(
                                    (s_k, pk, stk, obs.machine_effective_rouges(rk, mtk))
                                )
                    if holder_seat in resolve_reve_rank_cancellations(rank_entries, n_def_r):
                        p_exec = 0.0
                elif holder_seat == own_seat:
                    p_exec = max(0.0, 1.0 - belief.own_machine_cancel_prob)
                else:
                    p_exec = 0.0
        if p_exec <= 1e-6:
            return ()
        is_chg = is_tactique_charge(holder_lec, obs.tour)
        seuil = max(1, base_seuil + (0 if is_chg else eff_red) - bleus + spec.mod_seuil)
        return ((seuil, is_chg, p_exec),)

    # Carte non visible : impossible si paravents ouverts ou 0 main inconnue
    if obs.paravents_ouverts or unknown_holders == 0:
        return ()

    # Probabilité que cette carte soit dans une main adverse inconnue (calée sur belief.p_neighbor_sabotage)
    total_norm = 0
    for r_d in range(n):
        for mt_d in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            mp_d, ms_d = obs.machine_pos_status(r_d, mt_d)
            if ms_d == MACHINE_STATUS_NORMAL and mp_d > 0:
                total_norm += 1
    unseen_norm = max(1, total_norm - known_cards_cnt)
    exp_active_draws = unknown_holders * (1.0 - belief.p_neighbor_sabotage)

    # Pondération locale par les signaux publics alliés (excluant nos propres pions)
    own_f1 = obs.player_def1_furtivite_target(own_seat)
    own_f2 = obs.player_def2_furtivite_target(own_seat)
    own_on_p = (1 if own_f1 == (ray, 0) else 0) + (1 if own_f2 == (ray, 0) else 0)
    own_on_s = (1 if own_f1 == (ray, 1) else 0) + (1 if own_f2 == (ray, 1) else 0)
    ally_piege = max(0, obs.furtivite_ray_rive_defs(ray, 0) - own_on_p)
    ally_sab = max(0, obs.furtivite_ray_rive_defs(ray, 1) - own_on_s)
    w_boost = 1.0 + 0.55 * min(1, ally_piege) - (0.20 if (ally_sab >= 1 and ally_piege == 0) else 0.0)
    p_card = min(0.95, (exp_active_draws / float(unseen_norm)) * max(0.45, w_boost))

    for rk in range(1, TRACK_LEN + 1):
        spec = TACTIQUES_SPEC[rk]
        hits_here = ("SUR_PLACE" in spec.cibles and hits_sp) or (
            "DEVANT" in spec.cibles and hits_dev
        )
        if not hits_here:
            continue
        p_rk = p_card * _MIN_2D6_PROBS[rk - 1]
        t_code, _ = obs.tactique_code_bugs(rk - 1)
        if is_reve_code(t_code):
            n_def_r = obs.reve_activation_defenders(rk)
            if n_def_r >= 1:
                # Une machine adverse sur un Rêve défendu par n_def_r pions est annulée sauf surcharge
                p_overload = min(0.35, max(0.0, (unknown_holders - n_def_r) * _MIN_2D6_PROBS[rk - 1]))
                p_rk *= p_overload
        if p_rk <= 1e-6:
            continue
        is_chg = is_tactique_charge(rk, obs.tour)
        seuil = max(1, base_seuil + (0 if is_chg else eff_red) - bleus + spec.mod_seuil)
        key = (seuil, is_chg)
        by_outcome[key] = by_outcome.get(key, 0.0) + p_rk

    # Normaliser si la somme dépasse 1.0 (sécurité numérique)
    tot_p = sum(by_outcome.values())
    if tot_p > 1.0:
        inv = 1.0 / tot_p
        return tuple((s, c, p * inv) for (s, c), p in by_outcome.items())
    return tuple((s, c, p) for (s, c), p in by_outcome.items())


def _eval_parcel_outcome_with_defs(
    arbres: int,
    souches: int,
    defs: int,
    ins: int,
    has_piege: bool,
    strike_ab: tuple[int, bool] | None,
    strike_bu: tuple[int, bool] | None,
    weights: B2Weights,
    tour: int,
    trig_1_v: float,
    trig_6_v: float,
) -> tuple[float, float, float, float, float, float]:
    """Simule l'issue exacte d'un scénario discret `(strike_ab, strike_bu)` avec `defs` Défenseurs.

    Retourne `(trees_left, route_created, charge_gained, ins_left, souches_left, trig_val)`.
    Lorsque les deux machines frappent la même parcelle, applique l'ordre optimal du Lot 3
    (minimisant la perte d'arbres puis la création de Route).
    """

    def _run_order(seq: tuple[tuple[int, int, bool], ...]) -> tuple[int, int, int, int, int, float]:
        a = arbres
        s = souches
        i = ins
        pg = has_piege
        rt = 0
        chg = 0
        tv = 0.0
        for mt, seuil, is_c in seq:
            if a == 0 and s == 0:
                break
            if pg:
                pg = False
                continue
            if defs + i >= seuil:
                manque = max(0, seuil - defs)
                used = min(i, manque)
                i -= used
                tv += trig_6_v if used >= 1 else trig_1_v
                continue
            if mt == MACHINE_ABATTEUSE:
                s += a
                a = 0
            else:
                cut = min(1, a)
                a -= cut
                s = 0
            if a == 0 and s == 0:
                rt = 1
                i = 0
                pg = False
            if is_c:
                chg += 1
        return (a, rt, chg, i, s, tv)

    if strike_ab is not None and strike_bu is not None:
        o1 = _run_order(((MACHINE_ABATTEUSE, strike_ab[0], strike_ab[1]), (MACHINE_BULLDOZER, strike_bu[0], strike_bu[1])))
        o2 = _run_order(((MACHINE_BULLDOZER, strike_bu[0], strike_bu[1]), (MACHINE_ABATTEUSE, strike_ab[0], strike_ab[1])))
        # Ordre optimal du coordinateur (maximise arbres restants, minimise routes & charge)
        c_pen = weights.charge_penalty_for_tour(tour)
        v1 = o1[0] - o1[1] * weights.route_penalty_trees - o1[2] * c_pen + o1[3] * weights.insect_saved_trees + o1[4] * weights.souche_saved_trees
        v2 = o2[0] - o2[1] * weights.route_penalty_trees - o2[2] * c_pen + o2[3] * weights.insect_saved_trees + o2[4] * weights.souche_saved_trees
        chosen = o1 if v1 >= v2 else o2
    elif strike_ab is not None:
        chosen = _run_order(((MACHINE_ABATTEUSE, strike_ab[0], strike_ab[1]),))
    elif strike_bu is not None:
        chosen = _run_order(((MACHINE_BULLDOZER, strike_bu[0], strike_bu[1]),))
    else:
        return (float(arbres), 0.0, 0.0, float(ins), float(souches), 0.0)

    return (
        float(chosen[0]),
        float(chosen[1]),
        float(chosen[2]),
        float(chosen[3]),
        float(chosen[4]),
        chosen[5],
    )


def evaluate_forest_marginal_breakdown(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    p: int,
    *,
    is_held: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    trig_vals: tuple[float, ...] | None = None,
) -> ForestMarginalBreakdown:
    """Évalue exactement en arbres marginalement sauvés l'ajout d'un Défenseur sur `(ray, p)`."""
    if obs.is_route(ray, p):
        return ForestMarginalBreakdown(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

    if trig_vals is None:
        _, trig_vals = compute_b2_resource_and_trigger_values_trees(obs, cfg, belief, weights)

    raw_defs = obs.parcel_defenseurs(ray, p)
    defs = max(0, raw_defs - 1) if is_held else raw_defs
    ins = obs.parcel_insectes(ray, p)
    arbres = obs.parcel_arbres(ray, p)
    souches = obs.parcel_souches(ray, p)
    has_piege = obs.parcel_piege(ray, p) == PIEGE_ACTIF
    tour = obs.tour
    c_pen = weights.charge_penalty_for_tour(tour)
    trig_1_v = trig_vals[TRIG_PARADE - 1]
    trig_6_v = trig_vals[TRIG_INSECTE - 1]

    dist_ab = _machine_discrete_strike_dist(obs, cfg, belief, ray, MACHINE_ABATTEUSE, p)
    dist_bu = _machine_discrete_strike_dist(obs, cfg, belief, ray, MACHINE_BULLDOZER, p)

    p_no_ab = max(0.0, 1.0 - sum(x[2] for x in dist_ab))
    p_no_bu = max(0.0, 1.0 - sum(x[2] for x in dist_bu))
    opts_ab: list[tuple[tuple[int, bool] | None, float]] = [(None, p_no_ab)]
    for s, c, pr in dist_ab:
        opts_ab.append(((s, c), pr))
    opts_bu: list[tuple[tuple[int, bool] | None, float]] = [(None, p_no_bu)]
    for s, c, pr in dist_bu:
        opts_bu.append(((s, c), pr))

    d_trees = 0.0
    d_route = 0.0
    d_charge = 0.0
    d_ins = 0.0
    d_souches = 0.0
    d_trig = 0.0
    d_coop = 0.0
    any_direct_gain_prob = 0.0

    for st_ab, p_ab in opts_ab:
        if p_ab <= 1e-7:
            continue
        for st_bu, p_bu in opts_bu:
            p_joint = p_ab * p_bu
            if p_joint <= 1e-7 or (st_ab is None and st_bu is None):
                continue

            o0 = _eval_parcel_outcome_with_defs(
                arbres, souches, defs, ins, has_piege, st_ab, st_bu, weights, tour, trig_1_v, trig_6_v
            )
            o1 = _eval_parcel_outcome_with_defs(
                arbres, souches, defs + 1, ins, has_piege, st_ab, st_bu, weights, tour, trig_1_v, trig_6_v
            )

            dt = max(0.0, o1[0] - o0[0])
            dr = max(0.0, o0[1] - o1[1]) * weights.route_penalty_trees
            dc = max(0.0, o0[2] - o1[2]) * c_pen
            di = max(0.0, o1[3] - o0[3]) * weights.insect_saved_trees
            ds = max(0.0, o1[4] - o0[4]) * weights.souche_saved_trees
            dg = max(0.0, o1[5] - o0[5])

            direct_val = dt + dr + dc + di + ds + dg
            if direct_val > 1e-6:
                d_trees += p_joint * dt
                d_route += p_joint * dr
                d_charge += p_joint * dc
                d_ins += p_joint * di
                d_souches += p_joint * ds
                d_trig += p_joint * dg
                any_direct_gain_prob += p_joint
            else:
                # Staging coopératif discret (gap == 2 ou gap == 3) : évaluer exactement le gain à +2 ou +3
                o2 = _eval_parcel_outcome_with_defs(
                    arbres, souches, defs + 2, ins, has_piege, st_ab, st_bu, weights, tour, trig_1_v, trig_6_v
                )
                g2 = (
                    max(0.0, o2[0] - o0[0])
                    + max(0.0, o0[1] - o2[1]) * weights.route_penalty_trees
                    + max(0.0, o0[2] - o2[2]) * c_pen
                    + max(0.0, o2[3] - o0[3]) * weights.insect_saved_trees
                    + max(0.0, o2[4] - o0[4]) * weights.souche_saved_trees
                    + max(0.0, o2[5] - o0[5])
                )
                if g2 > 1e-6:
                    share2 = weights.coop_gap2_held_share if is_held else weights.coop_gap2_share
                    d_coop += p_joint * share2 * g2
                elif not is_held and arbres >= 1:
                    o3 = _eval_parcel_outcome_with_defs(
                        arbres, souches, defs + 3, ins, has_piege, st_ab, st_bu, weights, tour, trig_1_v, trig_6_v
                    )
                    g3 = (
                        max(0.0, o3[0] - o0[0])
                        + max(0.0, o0[1] - o3[1]) * weights.route_penalty_trees
                        + max(0.0, o0[2] - o3[2]) * c_pen
                    )
                    if g3 > 1e-6:
                        d_coop += p_joint * weights.coop_gap3_share * g3

    nid_v = 0.0
    if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(ray, p):
        prod_cnt = 1 if ins <= 1 else 2
        nid_v = weights.nid_base_trees + prod_cnt * weights.insect_saved_trees + (
            0.25 if is_held else 0.0
        )

    base_v = weights.forest_trapped_base_trees if has_piege else weights.forest_base_trees
    own_b = weights.own_ray_trees if (ray == obs.observer_seat and (any_direct_gain_prob > 0.05 or d_coop > 0.1)) else 0.0
    held_b = weights.held_completion_bonus if (is_held and any_direct_gain_prob >= 0.45) else 0.0

    total = base_v + d_trees + d_route + d_charge + d_ins + d_souches + d_trig + d_coop + nid_v + own_b + held_b
    return ForestMarginalBreakdown(
        immediate_trees_saved=d_trees,
        route_avoided_trees=d_route,
        charge_denied_trees=d_charge,
        insect_saved_trees=d_ins,
        souche_saved_trees=d_souches,
        trigger_trees=d_trig,
        coop_staging_trees=d_coop,
        nid_trees=nid_v,
        total_trees=total,
    )


def score_forest_marginal_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    p: int,
    *,
    is_held: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    trig_vals: tuple[float, ...] | None = None,
) -> float:
    """Retourne l'espérance d'arbres marginalement sauvés d'un Défenseur sur `(ray, p)`."""
    return evaluate_forest_marginal_breakdown(
        obs, cfg, belief, ray, p, is_held=is_held, weights=weights, trig_vals=trig_vals
    ).total_trees


# ---------------------------------------------------------------------------
# Utilitaires d'inférence publics (Furtivité, main couverte, déclencheurs Gardiens)
# ---------------------------------------------------------------------------


def is_own_hand_covered(obs: PlayerObservation, cfg: GameConfig) -> bool:
    """Vrai si le joueur n'a aucune frappe non parée issue de sa propre carte sous paravent."""
    own_hand = obs.hand_of(obs.observer_seat)
    if (not own_hand.has_card) or own_hand.card in (CARD_SABOTAGE, CARD_ECAILLE):
        return True
    if own_hand.card is None or not (1 <= own_hand.card <= 2 * obs.n_players):
        return True
    lec = own_hand.lecture_m
    if lec is None or not (1 <= lec <= TRACK_LEN):
        return True
    r_m, mt_m = unpack_machine_card(own_hand.card)
    pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
    if st_m != MACHINE_STATUS_NORMAL or pos_m <= 0:
        return True
    t_code, _ = obs.tactique_code_bugs(lec - 1)
    if is_reve_code(t_code) and obs.reve_activation_defenders(lec) >= 1:
        return True
    eff_t = lec if is_reve_code(t_code) else t_code
    if not is_tactique_code(eff_t):
        return True
    spec = TACTIQUES_SPEC[eff_t]
    is_chg = is_tactique_charge(eff_t, obs.tour)
    eff_red = 0 if is_chg else obs.machine_effective_rouges(r_m, mt_m)
    bleus = obs.machines[r_m * 2 + mt_m].bleus

    target_ps: list[int] = []
    for c_kind in spec.cibles:
        if c_kind == "SUR_PLACE" and not obs.is_route(r_m, pos_m):
            target_ps.append(pos_m)
        elif c_kind == "DEVANT":
            p_c = _next_non_razed_obs(obs, cfg.p_max, r_m, pos_m)
            if p_c is not None:
                target_ps.append(p_c)
    for tp in target_ps:
        if obs.parcel_piege(r_m, tp) == PIEGE_ACTIF:
            continue
        tot_d = obs.parcel_defenseurs(r_m, tp) + obs.parcel_insectes(r_m, tp)
        seuil_tp = max(1, CANONICAL_DOTATION[tp - 1] + eff_red - bleus + spec.mod_seuil)
        can_hurt = is_chg or obs.parcel_arbres(r_m, tp) >= 1 or mt_m == MACHINE_BULLDOZER
        if tot_d < seuil_tp and can_hurt:
            return False
    return True


def furtivite_ray_deduction(
    obs: PlayerObservation,
    cfg: GameConfig,
    ray: int,
    *,
    is_first_defender: bool,
) -> tuple[int, int, bool, int, float, float]:
    """Déduction bayésienne muette exacte (`mem_debt = 0.0`) sur l'activité `m(ray)` d'un rayon."""
    n = obs.n_players
    own_seat = obs.observer_seat
    own_hand = obs.hand_of(own_seat)

    rat_cnt = 0
    norm_cnt = 0
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos_m, st_m = obs.machine_pos_status(ray, mt)
        if st_m == MACHINE_STATUS_RATISSAGE and pos_m > 0:
            rat_cnt += 1
        elif st_m == MACHINE_STATUS_NORMAL and pos_m > 0:
            norm_cnt += 1

    active_cnt = rat_cnt + norm_cnt
    own_card_is_ray = False
    if own_hand.card is not None and 1 <= own_hand.card <= 2 * n:
        r_c, mt_c = unpack_machine_card(own_hand.card)
        if r_c == ray and obs.machine_pos_status(r_c, mt_c)[1] == MACHINE_STATUS_NORMAL:
            own_card_is_ray = True

    own_f1 = obs.player_def1_furtivite_target(own_seat)
    own_f2 = obs.player_def2_furtivite_target(own_seat)
    ally_def1_piege = max(
        0,
        obs.furtivite_ray_def1_rive_count(ray, FURT_RIVE_PIEGE)
        - (1 if own_f1 == (ray, FURT_RIVE_PIEGE) else 0),
    )
    ally_on_piege = max(
        0,
        obs.furtivite_ray_rive_defs(ray, FURT_RIVE_PIEGE)
        - (1 if own_f1 == (ray, FURT_RIVE_PIEGE) else 0)
        - (1 if own_f2 == (ray, FURT_RIVE_PIEGE) else 0),
    )
    ally_on_sab = max(
        0,
        obs.furtivite_ray_rive_defs(ray, FURT_RIVE_SABOTAGE)
        - (1 if own_f1 == (ray, FURT_RIVE_SABOTAGE) else 0)
        - (1 if own_f2 == (ray, FURT_RIVE_SABOTAGE) else 0),
    )

    total_norm_deck = 0
    for r_d in range(n):
        for mt_d in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            mp_d, ms_d = obs.machine_pos_status(r_d, mt_d)
            if ms_d == MACHINE_STATUS_NORMAL and mp_d > 0:
                total_norm_deck += 1
    unknown_holders = sum(
        1 for s in range(n) if s != own_seat and obs.hand_of(s).has_card and obs.hand_of(s).card is None
    )
    c_total = max(n, total_norm_deck + obs.sabotage_deck_count)
    c_other = max(1, c_total - (1 if own_hand.has_card else 0))
    k_opp = min(c_other, unknown_holders)

    if active_cnt < 2:
        p_m2 = 0.0
    elif rat_cnt == 2:
        p_m2 = 1.0
    elif rat_cnt == 1:
        p_m2 = (
            1.0
            if (own_card_is_ray or ((not is_first_defender) and ally_on_piege >= 1))
            else float(k_opp) / float(c_other)
        )
    elif own_card_is_ray:
        p_m2 = 1.0 if ally_on_piege >= 1 else float(k_opp) / float(c_other)
    elif ally_def1_piege >= 2:
        p_m2 = 1.0
    elif ally_def1_piege == 1:
        c_rem = max(1, c_other - 1)
        k_rem = max(0, min(c_rem, k_opp - 1))
        p_m2 = float(k_rem) / float(c_rem)
    elif k_opp >= 2 and c_other >= 2:
        p_m2 = (float(k_opp) / float(c_other)) * (float(k_opp - 1) / float(c_other - 1))
    else:
        p_m2 = 0.0

    if rat_cnt >= 1 or own_card_is_ray or ally_on_piege >= 1:
        p_m0 = 0.0
    elif norm_cnt == 0:
        p_m0 = 1.0
    else:
        cert_cnt = 1 if (ally_on_sab >= 1 or not is_first_defender) else 0
        c_eff = max(1, c_other - cert_cnt)
        k_eff = max(0, min(c_eff, k_opp - cert_cnt))
        rem_undrawn = c_eff - k_eff
        if norm_cnt == 1:
            p_m0 = max(0.0, float(rem_undrawn) / float(c_eff))
        elif rem_undrawn < 2 or c_eff < 2:
            p_m0 = 0.0
        else:
            p_m0 = (float(rem_undrawn) / float(c_eff)) * (
                float(rem_undrawn - 1) / float(c_eff - 1)
            )
        if p_m0 > 0.0 and not is_first_defender:
            defs_on_ray = sum(
                obs.parcel_defenseurs(ray, p_c)
                for p_c in range(1, cfg.p_max + 1)
                if not obs.is_route(ray, p_c)
            )
            if defs_on_ray == 0:
                odds = (p_m0 / max(1e-6, 1.0 - p_m0)) * 1.42
                p_m0 = odds / (1.0 + odds)
            elif defs_on_ray >= 2:
                odds = (p_m0 / max(1e-6, 1.0 - p_m0)) * 0.55
                p_m0 = odds / (1.0 + odds)

    return rat_cnt, norm_cnt, own_card_is_ray, ally_def1_piege, p_m2, p_m0


def best_untrapped_parcel_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    trig_piege_trees: float,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Valeur en équivalent-arbres du meilleur Piège autonome posable en 4.1 sur `ray`."""
    best_v = 0.0
    for p_c in range(1, cfg.p_max + 1):
        if obs.is_route(ray, p_c) or obs.parcel_piege(ray, p_c) != PIEGE_AUCUN:
            continue
        idx = ray * MAX_P + (p_c - 1)
        arbres = obs.parcel_arbres(ray, p_c)
        souches = obs.parcel_souches(ray, p_c)
        seuil_e = belief.parcel_expected_seuil[idx]
        s_prob = belief.parcel_strike_prob[idx]
        has_m = False
        max_red = 0
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            mp, ms = obs.machine_pos_status(ray, mt)
            if ms != MACHINE_STATUS_RETIRED and 0 < mp <= p_c:
                has_m = True
                max_red = max(max_red, obs.machine_effective_rouges(ray, mt))
        if not has_m and arbres == 0 and souches == 0:
            v_p = 0.35
        else:
            tree_v = float(arbres) * (1.15 if has_m else 0.55)
            seuil_saving = max(0.0, seuil_e - 1.5) * weights.furt_trap_seuil_bonus + max_red * 0.22
            nid_prot = 0.65 if obs.parcel_has_nid(ray, p_c) else 0.0
            route_prot = 0.70 * weights.route_penalty_trees if (arbres <= 1 and has_m) else 0.0
            v_p = 0.65 + tree_v + seuil_saving + nid_prot + route_prot + 0.65 * trig_piege_trees + 0.20 * min(1.5, s_prob)
        best_v = max(best_v, v_p)
    return best_v


def estimate_expected_gardien_triggers(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    *,
    for_eveil: bool = False,
) -> tuple[float, float, float, float, float, float]:
    """Estime le nombre attendu de déclencheurs sur les cases 1..6 (strictement sur `PlayerObservation`)."""
    n = obs.n_players
    p_max = cfg.p_max

    exp_parade = 0.0
    exp_piege = 0.0
    exp_sabotage = 0.0
    exp_reve = 0.0
    exp_insecte = 0.0

    for r in range(n):
        for p in range(1, p_max + 1):
            if obs.is_route(r, p):
                continue
            idx = r * MAX_P + (p - 1)
            s_prob = belief.parcel_strike_prob[idx]
            if s_prob <= 0.08:
                continue
            defs = obs.parcel_def1_count(r, p) if for_eveil else obs.parcel_defenseurs(r, p)
            ins = obs.parcel_insectes(r, p)
            cur_def = defs + ins
            seuil_e = belief.parcel_expected_seuil[idx]
            c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
            if obs.parcel_piege(r, p) == PIEGE_ACTIF:
                exp_piege += min(1.0, s_prob)
            elif defs >= seuil_e:
                exp_parade += min(1.35, s_prob)
            elif cur_def >= seuil_e and ins >= 1:
                exp_insecte += min(1.35, s_prob)
            elif defs >= seuil_e - 0.55 and defs >= 1 and ins == 0:
                exp_parade += 0.50 * min(1.0, s_prob)
            elif cur_def >= seuil_e - 0.55 and ins >= 1:
                exp_insecte += 0.50 * min(1.0, s_prob)
            elif cur_def >= 1 and c_prob > 0.20 and cur_def >= (CANONICAL_DOTATION[p - 1] - 0.25):
                if ins >= 1 and defs < CANONICAL_DOTATION[p - 1]:
                    exp_insecte += 0.55 * min(1.0, c_prob)
                else:
                    exp_parade += 0.55 * min(1.0, c_prob)

    for r_f in range(n):
        cnt_rp = (
            obs.furtivite_ray_def1_rive_count(r_f, FURT_RIVE_PIEGE)
            if for_eveil
            else obs.furtivite_ray_rive_defs(r_f, FURT_RIVE_PIEGE)
        )
        if cnt_rp == 2:
            exp_piege += 0.75

    own_hand = obs.hand_of(obs.observer_seat)
    own_card = own_hand.card
    own_is_sab = own_card in (CARD_SABOTAGE, CARD_ECAILLE)
    own_reve_consumed_sole_def = -1
    if own_is_sab:
        exp_sabotage += 1.0
    elif (
        own_card is not None
        and own_hand.lecture_m is not None
        and 1 <= own_card <= 2 * n
        and 1 <= own_hand.lecture_m <= TRACK_LEN
    ):
        own_m = own_hand.lecture_m
        own_bugs = obs.tactique_code_bugs(own_m - 1)[1]
        if obs.reve_at_case(own_m) > 0:
            r_defs_own = (
                obs.reve_def1_count(own_m) if for_eveil else obs.reve_activation_defenders(own_m)
            )
            if r_defs_own >= 1:
                exp_reve += 0.95
                if r_defs_own == 1:
                    own_reve_consumed_sole_def = own_m
        elif own_bugs >= 1:
            exp_insecte += 0.85

    active_deck_machines = sum(
        1
        for r in range(n)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        if obs.machine_pos_status(r, mt)[1] == MACHINE_STATUS_NORMAL
        and obs.machine_pos_status(r, mt)[0] > 0
    )
    sab_in_deck = obs.sabotage_deck_count + obs.ecaille_deck_count
    sab_others = max(0, sab_in_deck - (1 if own_is_sab else 0))
    total_deck_est = max(n, active_deck_machines + sab_in_deck)
    p_other_sab = min(0.85, sab_others / max(1.0, float(total_deck_est - 1)))
    if sab_others >= 1:
        exp_sabotage += 0.75 * min(float(sab_others), float(n - 1) * p_other_sab)

    p_other_mach = max(0.0, 1.0 - p_other_sab)
    prob_reve_rank = 0.0
    for c_r in range(1, TRACK_LEN + 1):
        if obs.reve_at_case(c_r) <= 0 or c_r == own_reve_consumed_sole_def:
            continue
        r_defs = obs.reve_def1_count(c_r) if for_eveil else obs.reve_activation_defenders(c_r)
        if r_defs >= 1:
            prob_reve_rank += _MIN_2D6_PROBS[c_r - 1]
    if prob_reve_rank > 0.0:
        exp_reve += 0.84 * float(n - 1) * p_other_mach * prob_reve_rank

    total_bugs_avail = 0
    prob_bug_rank = 0.0
    for c_b in range(1, TRACK_LEN + 1):
        if obs.reve_at_case(c_b) == 0:
            b_cnt = obs.tactique_code_bugs(c_b - 1)[1]
            if b_cnt >= 1:
                total_bugs_avail += b_cnt
                prob_bug_rank += _MIN_2D6_PROBS[c_b - 1]
    if total_bugs_avail > 0:
        exp_insecte += 0.72 * min(
            float(total_bugs_avail), float(n - 1) * p_other_mach * prob_bug_rank
        )

    return (exp_parade, exp_piege, exp_sabotage, exp_reve, exp_insecte, 0.0)


# ---------------------------------------------------------------------------
# Lisières, Furtivité, Rêves et Gardiens dans la même monnaie « arbres »
# ---------------------------------------------------------------------------


def score_tile_construction_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    tile_id: str,
    res_val: dict[str, float],
    trig_vals: tuple[float, ...],
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Valeur en équivalent-arbres de la construction d'une tuile de lisière."""
    fam, _, _ = SYNERGY_META[tile_id]
    tour = obs.tour
    late_decay = 1.0 if tour <= 5 else (0.62 if tour == 6 else 0.30)
    tile_active = is_tile_text_active(cfg, tile_id)

    if fam == FAMILLE_REVE:
        reves_on_track = sum(1 for t in obs.piste_tactiques if is_reve_code(t.code))
        target_reves = max(1, cfg.total_reves_partie)
        if not tile_active:
            sat = 1.0 if reves_on_track == 0 else (0.75 if reves_on_track == 1 else 0.35)
            struct_v = weights.lisiere_reve_struct * sat * late_decay
        else:
            sat = 1.15 if reves_on_track == 0 else (0.95 if reves_on_track < target_reves else 0.48)
            struct_v = weights.lisiere_reve_struct * sat * (0.45 if tour >= 7 else 1.0)
    elif fam == FAMILLE_CROISSANCE:
        struct_v = weights.lisiere_croissance_struct * late_decay
    else:
        g_on_track = sum(1 for g in obs.piste_gardiens if g.gardien_num > 0)
        min_g_eveil = (obs.n_players + 1) // 2
        if obs.gardien_pari_enabled and g_on_track < min_g_eveil:
            struct_v = weights.lisiere_gardien_eveil_struct
        elif tile_active:
            struct_v = weights.lisiere_gardien_mode4_struct
        elif obs.gardien_pari_enabled and obs.n_players >= 5 and g_on_track == min_g_eveil and tour <= 6:
            struct_v = 0.78 * weights.lisiere_gardien_eveil_struct
        else:
            struct_v = 0.35

    if not tile_active:
        return struct_v

    econ = get_economie_catalog()
    prof = cfg.profile_for_slot(tile_id)
    node = econ.get((tile_id, prof)) if prof is not None else None
    if node is None:
        return struct_v

    econ_bonus = 0.0
    for out_tok in node.outputs_produits:
        if out_tok in res_val:
            econ_bonus += weights.econ_output_share * res_val[out_tok]
        elif out_tok.startswith("TRIG_"):
            t_i = int(out_tok[5:]) - 1
            if 0 <= t_i < 6:
                econ_bonus += weights.econ_output_share * trig_vals[t_i]

    if "RES_INSECTE" in node.inputs_requis and fam != FAMILLE_CROISSANCE:
        has_any_ins = any(
            obs.parcel_insectes(r, p) > 0
            for r in range(obs.n_players)
            for p in range(1, cfg.p_max + 1)
        )
        if not has_any_ins:
            econ_bonus -= 0.25

    if node.is_law and tour <= 5:
        econ_bonus += 0.30
    return struct_v + econ_bonus


def score_lisiere_marginal_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    slot_idx: int,
    *,
    is_held: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    res_val: dict[str, float] | None = None,
    trig_vals: tuple[float, ...] | None = None,
) -> float:
    """Valeur en équivalent-arbres d'une pose sur le chantier de lisière `slot_idx`."""
    if obs.mode < 2 or slot_idx >= 2 * obs.n_players:
        return 0.0
    tile_id, st_l, raw_constructors = obs.lisiere_tile_info(slot_idx)
    if st_l != LISIERE_UNCONSTRUCTED:
        return 0.0
    if res_val is None or trig_vals is None:
        res_val, trig_vals = compute_b2_resource_and_trigger_values_trees(obs, cfg, belief, weights)

    constructors = max(0, raw_constructors - 1) if is_held else raw_constructors
    tile_v = score_tile_construction_trees(obs, cfg, tile_id, res_val, trig_vals, weights)
    lib_bonus = 0.42 * res_val["RES_DEFENSEUR"] if obs.n_players == 3 else 0.0

    if constructors == 1:
        return (
            weights.lisiere_complete_base
            + tile_v * weights.lisiere_complete_mult
            + lib_bonus
            + (0.45 if is_held else 0.0)
        )
    if is_held:
        return weights.lisiere_solo_held_base + 0.55 * tile_v
    if tile_v >= 1.00 and (belief.drew_sabotage_or_none or is_own_hand_covered(obs, cfg)):
        return weights.lisiere_open_covered_base + 1.15 * tile_v + lib_bonus
    if belief.drew_sabotage_or_none and tile_v >= 0.65:
        return 0.85 * weights.lisiere_open_covered_base + tile_v + lib_bonus
    return weights.lisiere_open_default_base + 0.85 * tile_v + lib_bonus


def score_furtivite_marginal_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    rive: int,
    *,
    is_held: bool = False,
    is_first_defender: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    res_val: dict[str, float] | None = None,
    trig_vals: tuple[float, ...] | None = None,
) -> float:
    """Valeur en équivalent-arbres d'une pose Furtivité (`Rive Piège` ou `Rive Sabotage`)."""
    if not obs.is_ray_furtivite_open(ray):
        return 0.0
    raw_d_rv = obs.furtivite_ray_rive_defs(ray, rive)
    d_rv = max(0, raw_d_rv - 1) if is_held else raw_d_rv
    sentinels = obs.rooted_sentinels_on_ray(ray) if rive == FURT_RIVE_SABOTAGE else 0
    cap_rv = max(0, 2 - sentinels)
    if d_rv >= cap_rv:
        return 0.0
    if res_val is None or trig_vals is None:
        res_val, trig_vals = compute_b2_resource_and_trigger_values_trees(obs, cfg, belief, weights)

    d_other = obs.furtivite_ray_rive_defs(ray, 1 - rive)
    partner_ready = (d_rv + sentinels) == 1

    other_completed_rives = 0
    other_open_rives = 0
    for r2 in range(obs.n_players):
        for rv2 in (FURT_RIVE_PIEGE, FURT_RIVE_SABOTAGE):
            if r2 == ray and rv2 == rive:
                continue
            s2 = obs.rooted_sentinels_on_ray(r2) if rv2 == FURT_RIVE_SABOTAGE else 0
            cnt2 = obs.furtivite_ray_rive_defs(r2, rv2) + s2
            if cnt2 >= 2:
                other_completed_rives += 1
            elif cnt2 == 1:
                other_open_rives += 1

    rat_cnt, _, own_card_is_ray, _, p_m2, p_m0 = furtivite_ray_deduction(
        obs, cfg, ray, is_first_defender=is_first_defender
    )

    if rive == FURT_RIVE_PIEGE:
        trap_v = best_untrapped_parcel_trees(obs, cfg, belief, ray, trig_vals[1], weights)
        if trap_v <= 0.20:
            return 0.20
        if p_m2 >= 0.99:
            if partner_ready:
                return (
                    weights.furt_piege_complete_base
                    + weights.furt_trap_value_mult * trap_v
                    + (0.50 if is_held else 0.0)
                )
            if is_first_defender:
                return weights.furt_piege_open_certain_base + 0.42 * trap_v
            if rat_cnt == 2 and other_open_rives == 0 and (
                belief.drew_sabotage_or_none or is_own_hand_covered(obs, cfg)
            ):
                return 0.78 * weights.furt_piege_open_certain_base + 0.35 * trap_v + (-0.12 if is_held else 0.0)
            return 0.35
        if (
            (not is_first_defender)
            and (not partner_ready)
            and own_card_is_ray
            and p_m2 >= 0.38
            and other_open_rives == 0
            and other_completed_rives == 0
            and trap_v >= 2.20
        ):
            return weights.furt_piege_signal_base + p_m2 * (0.45 * trap_v) + (-0.10 if is_held else 0.0)
        return 0.25

    # Rive Sabotage (v6.4 : Sabotage différé à intérêts composés + Effet Sentinelle des Enracinements)
    sab_cnt = obs.sabotage_deck_count + obs.sabotage_pending_count
    if obs.tour >= 8 or p_m0 < 0.24 or sab_cnt >= 3:
        return 0.20

    ray_undef_2_1 = sum(obs.parcel_def1_count(ray, p) for p in range(1, cfg.p_max + 1)) == 0
    total_norm = sum(
        1 for m in obs.machines if m.status == MACHINE_STATUS_NORMAL and m.position > 0
    )
    next_deck_sz = max(float(obs.n_players), float(total_norm + sab_cnt + 1))
    p_next_draw = min(1.0, float(obs.n_players) / next_deck_sz)
    sab_stock_mult = 1.45 if sab_cnt == 0 else (0.92 if sab_cnt == 1 else 0.48)
    prep_trig3 = 0.0
    if obs.gardien_present_at_case(3):
        prep_trig3 += 0.80 * trig_vals[2] + (0.60 if sab_cnt == 0 else 0.25)
    elif obs.gardien_pari_enabled and sab_cnt == 0 and obs.tour <= 5:
        prep_trig3 += 0.55

    gross_sab = (res_val["RES_DILUTION_SABOTAGE"] * 1.18) * sab_stock_mult * (0.72 + 0.80 * p_next_draw) + prep_trig3
    action_v = max(0.0, p_m0 * gross_sab - (1.0 - p_m0) * weights.furt_sab_waste_penalty)
    if action_v <= 0.08:
        return 0.32

    scarcity = 0.0
    if other_completed_rives >= 1:
        scarcity += weights.furt_scarcity_completed * (1.0 if obs.n_players <= 4 else 0.72)
    if d_other >= 1:
        scarcity += weights.furt_scarcity_other_rive
    if not partner_ready and other_open_rives >= 1:
        scarcity += weights.furt_scarcity_open
    if not ray_undef_2_1 and not is_first_defender and sentinels == 0:
        scarcity += 0.45

    if partner_ready:
        sent_b = 0.45 if sentinels >= 1 else 0.0
        return max(0.45, weights.furt_sab_complete_base + 1.25 * action_v + sent_b - scarcity + (0.35 if is_held else 0.0))

    held_adj = -0.10 if is_held else 0.0
    if not is_first_defender:
        if belief.drew_sabotage_or_none and p_m0 >= 0.28:
            return max(0.45, weights.furt_sab_open_base + 1.15 * action_v - scarcity + held_adj)
        if (
            (is_own_hand_covered(obs, cfg) or (ray_undef_2_1 and sab_cnt == 0 and obs.tour <= 3))
            and p_m0 >= 0.30
            and (obs.tour <= 4 or sab_cnt == 0)
        ):
            return max(0.45, 0.92 * weights.furt_sab_open_base + 1.10 * action_v - scarcity + held_adj)
    elif obs.n_players >= 4 and sab_cnt == 0 and obs.tour <= 3 and belief.drew_sabotage_or_none and p_m0 >= 0.34:
        return max(0.45, 0.75 * weights.furt_sab_open_base + 0.90 * action_v - scarcity)

    return max(0.32, 0.75 + 0.30 * action_v - scarcity + held_adj)


def score_reve_marginal_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_held: bool = False,
    is_first_defender: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Valeur en équivalent-arbres d'une pose sur le Rêve en case `case_c`."""
    if obs.reve_at_case(case_c) <= 0:
        return 0.0

    own_seat = obs.observer_seat
    own_hand = obs.hand_of(own_seat)
    own_card = own_hand.card
    own_def1_r = obs.player_def1_reve_case(own_seat)
    own_def2_r = obs.player_def2_reve_case(own_seat)
    already_self_cancelled = (not is_first_defender) and (own_def1_r == case_c)
    own_hits_reve = (
        (not already_self_cancelled)
        and own_card is not None
        and 1 <= own_card <= 2 * obs.n_players
        and own_hand.lecture_m == case_c
    )

    total_on_case = obs.reve_activation_defenders(case_c)
    own_cur = (1 if (is_first_defender and own_def1_r == case_c) else 0) + (
        1 if (not is_first_defender and own_def2_r == case_c) else 0
    )
    allies = max(0, total_on_case - own_cur)

    if own_hits_reve and own_card is not None:
        ray, m_type = unpack_machine_card(own_card)
        pos, st = obs.machine_pos_status(ray, m_type)
        if st != MACHINE_STATUS_NORMAL or pos <= 0:
            return 0.35

        spec = TACTIQUES_SPEC[case_c]
        is_chg = is_tactique_charge(case_c, obs.tour)
        eff_red = 0 if is_chg else obs.machine_effective_rouges(ray, m_type)
        bleus = obs.machines[ray * 2 + m_type].bleus

        target_ps: list[int] = []
        for c_kind in spec.cibles:
            if c_kind == "SUR_PLACE" and not obs.is_route(ray, pos):
                target_ps.append(pos)
            elif c_kind == "DEVANT":
                p_dev = _next_non_razed_obs(obs, cfg.p_max, ray, pos)
                if p_dev is not None:
                    target_ps.append(p_dev)

        saved_trees = 0.0
        would_gain_charge = False
        for tp in target_ps:
            defs_tp = obs.parcel_defenseurs(ray, tp)
            ins_tp = obs.parcel_insectes(ray, tp)
            seuil_tp = max(1, CANONICAL_DOTATION[tp - 1] + eff_red - bleus + spec.mod_seuil)
            if obs.parcel_piege(ray, tp) == PIEGE_ACTIF:
                saved_trees += weights.reve_piege_saved_trees
            elif defs_tp + ins_tp >= seuil_tp:
                manque = max(0, seuil_tp - defs_tp)
                saved_trees += 0.20 + weights.insect_saved_trees * min(ins_tp, manque)
            else:
                arbres = obs.parcel_arbres(ray, tp)
                would_gain_charge = True
                if m_type == MACHINE_ABATTEUSE:
                    saved_trees += float(arbres) * 2.15 + (0.65 if seuil_tp >= 2 else 0.20)
                else:
                    saved_trees += float(min(1, arbres)) * 2.15 + (
                        weights.route_penalty_trees if arbres <= 1 else 0.0
                    ) + (0.65 if seuil_tp >= 2 else 0.22)

        if spec.avancee > 0:
            saved_trees += weights.reve_advance_trees
        if is_chg and would_gain_charge:
            saved_trees += weights.charge_penalty_for_tour(obs.tour)
        if obs.gardien_present_at_case(TRIG_REVE) and allies == 0:
            saved_trees += weights.reve_trig5_trees

        flex = (weights.reve_flex_21_trees if ray != own_seat else 0.45 * weights.reve_flex_21_trees) if is_first_defender else 0.0
        ally_mult = 1.0 if allies == 0 else (weights.reve_ally_decay ** allies)
        val = (weights.reve_base_trees + saved_trees + flex) * ally_mult
        if is_held:
            val += 0.45
        return val

    # Pose proactive en 2.1 pour allumer 4. Rêve pendant l'Éveil
    if is_first_defender and obs.tour <= 7 and obs.gardien_pari_enabled:
        g5_present = obs.gardien_present_at_case(TRIG_REVE)
        g_cnt = sum(1 for c_g in range(1, TRACK_LEN + 1) if obs.gardien_present_at_case(c_g))
        min_g_eveil = (obs.n_players + 1) // 2
        any_reve_armed = any(
            obs.reve_def1_count(c_r) >= 1
            for c_r in range(1, TRACK_LEN + 1)
            if obs.reve_at_case(c_r) > 0
        )
        best_reve_case = next(
            (c_r for c_r in range(1, TRACK_LEN + 1) if obs.reve_at_case(c_r) > 0), 0
        )
        if (
            g5_present
            and g_cnt >= min_g_eveil
            and not any_reve_armed
            and case_c == best_reve_case
            and (belief.drew_sabotage_or_none or is_own_hand_covered(obs, cfg))
        ):
            est_active = max(1, obs.n_players - 1 - obs.sabotage_deck_count)
            p_hit_any = 1.0 - ((1.0 - _MIN_2D6_PROBS[case_c - 1]) ** est_active)
            min_p = 0.28 if obs.n_players >= 5 else 0.36
            if p_hit_any >= min_p:
                arm_base = (
                    weights.reve_eveil_arm_n56_trees
                    if obs.n_players >= 5
                    else weights.reve_eveil_arm_n34_trees * (1.0 if obs.tour >= 4 else 0.82)
                )
                return arm_base + 1.15 * p_hit_any

    if (
        is_first_defender
        and case_c <= 2
        and allies == 0
        and obs.tour >= 5
        and belief.drew_sabotage_or_none
    ):
        p_rk = belief.reve_open_prob_by_rank[case_c - 1]
        if p_rk >= 0.52:
            return weights.reve_speculative_trees + 1.45 * p_rk

    return 0.25 - (0.30 if is_held else 0.0)


def score_gardien_pari_marginal_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_held: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Valeur en équivalent-arbres d'un pari Gardien `('GARDIEN_PARI', case_c)` (v6.4 Éveil cumulatif A+1 Face 2)."""
    if not obs.gardien_pari_enabled or not obs.gardien_present_at_case(case_c):
        return 0.0

    own_pari_case = obs.player_def2_gardien_pari_case(obs.observer_seat)
    allies_on_case = max(
        0, obs.gardien_pari_defenders(case_c) - (1 if own_pari_case == case_c else 0)
    )
    if allies_on_case >= GARDIEN_BET_CAP:
        return 0.0

    g_slot = obs.piste_gardiens[case_c - 1]
    g_active = is_tile_text_active(cfg, g_slot.tile_id)
    g_face = obs.gardien_face_at_case(case_c)
    if (not g_active) and (obs.tour >= 8 or g_face >= 2 or allies_on_case >= 1):
        return 0.05

    eveil_trigs = estimate_expected_gardien_triggers(obs, cfg, belief, for_eveil=True)
    cur_trigs = estimate_expected_gardien_triggers(obs, cfg, belief, for_eveil=False)
    n = obs.n_players
    req_eveil = cfg.nb_animaux_sauvages + 1
    face2_now = obs.count_face2_gardiens_on_track()
    other_f1_bet = sum(
        1
        for ck in range(1, TRACK_LEN + 1)
        if ck != case_c
        and obs.gardien_present_at_case(ck)
        and obs.gardien_face_at_case(ck) == 1
        and max(0, obs.gardien_pari_defenders(ck) - (1 if own_pari_case == ck else 0)) >= 1
    )

    distinct_other_cap = 0.0
    distinct_other_bet_exp = 0.0
    for c_k in (1, 2, 3, 4, 5):
        if obs.gardien_present_at_case(c_k):
            t_k = eveil_trigs[c_k - 1]
            distinct_other_cap += min(1.0, t_k)
            bets_k = max(0, obs.gardien_pari_defenders(c_k) - (1 if own_pari_case == c_k else 0))
            if bets_k >= 1:
                distinct_other_bet_exp += min(1.0, t_k)

    if case_c == TRIG_RESONANCE:
        exp_for_case = min(distinct_other_cap, distinct_other_bet_exp)
    else:
        exp_for_case = max(eveil_trigs[case_c - 1], cur_trigs[case_c - 1])
    needed = allies_on_case + 1

    total_init = max(1, n * sum(CANONICAL_DOTATION))
    cur_arbres = sum(obs.parcel_arbres(r, p) for r in range(n) for p in range(1, cfg.p_max + 1))
    tree_ratio = cur_arbres / total_init
    bouclier_safety = weights.gardien_bouclier_trees if obs.piste_colonie[case_c - 1] >= 1 else 0.0

    sup_tol = 0.25 if n >= 5 else 0.18
    supported = exp_for_case >= (float(needed) - sup_tol)
    marginally_supported = exp_for_case >= (float(needed) - (sup_tol + 0.25))

    base_gp = 0.15
    if obs.tour <= 7 and cfg.nb_animaux_sauvages >= 1 and g_face == 1 and allies_on_case == 0:
        will_win_eveil_now = (face2_now + 1 + other_f1_bet) >= req_eveil
        eveil_mult = weights.eveil_n56_mult if n >= 5 else 1.0
        if supported:
            if will_win_eveil_now:
                base_gp = (
                    (weights.eveil_finish_trees + weights.eveil_tree_ratio_scale * tree_ratio)
                    * eveil_mult
                    + bouclier_safety
                )
            else:
                prog = float(face2_now + 1) / float(max(1, req_eveil))
                base_gp = (
                    (
                        weights.eveil_start_trees
                        + 1.65 * prog
                        + 0.65 * weights.eveil_tree_ratio_scale * tree_ratio
                    )
                    * eveil_mult
                    + bouclier_safety
                )
        elif marginally_supported and (will_win_eveil_now or g_active):
            base_gp = weights.eveil_progress_trees * 0.72 + 0.40 * tree_ratio + bouclier_safety

    if g_active:
        if exp_for_case >= (float(needed) + 0.02):
            face_b = weights.gardien_mode4_face1_bonus if g_face == 1 else 0.75
            mode4_v = weights.gardien_mode4_probable_trees + face_b + bouclier_safety
            if face2_now >= req_eveil and obs.tour <= 7 and exp_for_case < float(needed) + 0.35:
                mode4_v *= 0.35
            base_gp = max(base_gp, mode4_v)
        elif exp_for_case >= (float(needed) - 0.20):
            base_gp = max(base_gp, weights.gardien_mode4_marginal_trees + bouclier_safety)

    if is_held:
        if obs.tour <= 7 and g_face == 1 and supported:
            return base_gp + 0.45
        if g_active and base_gp >= weights.gardien_mode4_marginal_trees:
            return base_gp + 0.20
        return base_gp - 0.55
    return base_gp


def score_target_b2_trees(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    *,
    is_held: bool = False,
    is_first_defender: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Évaluateur unifié B2 retournant l'espérance en arbres marginalement sauvés."""
    res_val, trig_vals = compute_b2_resource_and_trigger_values_trees(obs, cfg, belief, weights)
    kind = target[0]

    if kind == "FORET":
        return score_forest_marginal_trees(
            obs,
            cfg,
            belief,
            int(target[1]),
            int(target[2]),
            is_held=is_held,
            weights=weights,
            trig_vals=trig_vals,
        )
    if kind == "LISIERE":
        return score_lisiere_marginal_trees(
            obs,
            cfg,
            belief,
            int(target[1]),
            is_held=is_held,
            weights=weights,
            res_val=res_val,
            trig_vals=trig_vals,
        )
    if kind == "FURTIVITE":
        return score_furtivite_marginal_trees(
            obs,
            cfg,
            belief,
            int(target[1]),
            int(target[2]),
            is_held=is_held,
            is_first_defender=is_first_defender,
            weights=weights,
            res_val=res_val,
            trig_vals=trig_vals,
        )
    if kind == "GARDIEN_PARI":
        return score_gardien_pari_marginal_trees(
            obs, cfg, belief, int(target[1]), is_held=is_held, weights=weights
        )
    if kind == "REVE_ACTIVATION":
        return score_reve_marginal_trees(
            obs,
            cfg,
            belief,
            int(target[1]),
            is_held=is_held,
            is_first_defender=is_first_defender,
            weights=weights,
        )
    return 0.0
