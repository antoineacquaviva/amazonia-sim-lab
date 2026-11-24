"""Moteur heuristique B1 (Découverte, k=1) et B2 (Cœur de cible, k=2, économie unifiée arbres + CRN)."""

from __future__ import annotations

from typing import Any, ClassVar

from bots.b2_economy import (
    ALL_ACTIVE_RESOURCES,
    DEFAULT_B2_WEIGHTS,
    TREE_SCORE_UNIT,
    B2Weights,
    EconomieNode,
    best_untrapped_parcel_trees,
    compute_b2_resource_and_trigger_values_trees,
    furtivite_ray_deduction,
    get_economie_catalog,
    is_own_hand_covered,
    score_gardien_pari_marginal_trees,
    score_reve_marginal_trees,
    score_target_b2_trees,
    score_tile_construction_trees,
)
from bots.b2_rollouts import arbitrate_step2_gardien_reve_crn
from bots.belief_and_ticks import (
    BeliefSummary,
    build_belief_summary,
    resolve_step2_full_with_ticks,
    softmax_select_index,
)
from engine.core_engine import (
    DEC_BOUCLIER_LISIERE_5_3,
    DEC_CHOIX_CASE_GARDIEN,
    DEC_CHOIX_CIBLE_REVE_3_2,
    DEC_ENRACINEMENT_6_1,
    DEC_HUMAIN_CHAMAN_2_1,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_MAMMIFERE_DUEL_2,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_OISEAU_DE_ENVOL_1_3,
    DEC_OISEAU_PERCHOIR_1_1,
    DEC_OISEAU_PLUME_2,
    DEC_ORDRE_ATTAQUE_5_1,
    DEC_ORDRE_CONSTRUCTION_3_1,
    DEC_ORDRE_NID_4_2,
    DEC_ORDRE_RATISSAGE_5_2,
    DEC_PLACEMENT_NID_3_1,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    DEC_REPTILE_POSE_CROC_3_2,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest, GameOver
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CANONICAL_DOTATION,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    DUEL_TERRITOIRE_TENU,
    FAMILLE_CROISSANCE,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PLUME_CALME,
    PLUME_CHAUD,
    PLUME_KIND_RAY,
    RATISSAGE_TACTIQUE_SPEC,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TRACK_LEN,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_REVE,
    TRIG_SABOTAGE,
    GameConfig,
    GameState,
    PlayerObservation,
    TactiqueSpec,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    machine_card_code,
    machine_threat_key_3_2,
    unpack_machine_card,
)

__all__ = (
    "ALL_ACTIVE_RESOURCES",
    "DEFAULT_B2_WEIGHTS",
    "DEFAULT_TAU_B1",
    "TREE_SCORE_UNIT",
    "B2Weights",
    "BotB1",
    "BotB2",
    "EconomieNode",
    "choose_b1",
    "choose_b2",
    "choose_b2_open",
    "count_active_laws_from_obs",
    "get_economie_catalog",
    "make_b1_scorer",
    "make_b2_scorer",
    "play_game_b1",
    "play_game_b2",
    "play_game_b2_open",
    "score_target_b1",
    "score_target_b2",
)

# Température softmax calibrée de B1 (60.0 centi-arbres = 0,60 arbre, active dès 0 loi : B0 < B1 < B2)
DEFAULT_TAU_B1: float = 60.0


def _tactique_danger(rank_1_6: int, tour: int, eff_red: int = 1) -> float:
    """Danger tactique dynamique v6.1 d'une case 1..6 selon Acte 1/2 (CHARGE vs ASSAUT) et puissance."""
    if not (1 <= rank_1_6 <= TRACK_LEN):
        return 30.0
    is_double = rank_1_6 in (3, 6)
    base = 72.0 if is_double else (28.0 if rank_1_6 in (2, 5) else 22.0)
    if is_tactique_charge(rank_1_6, tour):
        rem_turns = max(0, 8 - tour)
        return base + (24.0 + 6.5 * rem_turns) * (1.25 if is_double else 1.0)
    return base + 22.0 * max(0, eff_red) * (1.35 if is_double else 1.0)


class _EconomieStore:
    last_b1_obs: ClassVar[PlayerObservation | None] = None
    last_b1_laws: ClassVar[int] = 0


def _tiebreak(cfg: GameConfig, obs: PlayerObservation, opt_idx: int, salt: int = 0) -> int:
    return rand_u64(
        cfg.exp_seed,
        cfg.rep_id,
        SRC_BOT_TIEBREAK,
        obs.tour,
        obs.observer_seat,
        ((obs.step + salt) * 37 + opt_idx) & 0xFFFFFFFF,
    )


def count_active_laws_from_obs(obs: PlayerObservation, cfg: GameConfig) -> int:
    """Compte les Lois `MOD_LOI_DU_COEUR` actives sur le plateau uniquement depuis `obs` et `cfg`."""
    if obs.mode < 3:
        return 0
    if _EconomieStore.last_b1_obs is obs:
        return _EconomieStore.last_b1_laws
    econ = get_economie_catalog()
    count = 0

    for mig_slot in ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"):
        prof = cfg.profile_for_slot(mig_slot)
        if prof is not None:
            node = econ.get((mig_slot, prof))
            if node is not None and node.is_law:
                count += 1

    for g_obs in obs.piste_gardiens:
        if g_obs.tile_id is not None:
            prof = cfg.profile_for_slot(g_obs.tile_id)
            if prof is not None:
                node = econ.get((g_obs.tile_id, prof))
                if node is not None and node.is_law:
                    count += 1

    for t_obs in obs.piste_tactiques:
        if is_reve_code(t_obs.code):
            prof = cfg.profile_for_slot(t_obs.tile_id)
            if prof is not None:
                node = econ.get((t_obs.tile_id, prof))
                if node is not None and node.is_law:
                    count += 1

    for lis in obs.lisieres:
        if lis.tile_id.startswith("M") and lis.status == LISIERE_CONSTRUCTED:
            prof = cfg.profile_for_slot(lis.tile_id)
            if prof is not None:
                node = econ.get((lis.tile_id, prof))
                if node is not None and node.is_law:
                    count += 1

    _EconomieStore.last_b1_obs = obs
    _EconomieStore.last_b1_laws = count
    return count


# ---------------------------------------------------------------------------
# Graphe dynamique B2 (`economie_bot` k=2 + Lookahead 5.1 -> 6.2)
# ---------------------------------------------------------------------------


def _compute_b2_resource_and_trigger_values(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> tuple[dict[str, float], tuple[float, ...]]:
    """Retourne les valeurs des 11 `RES_*` actifs et `TRIG_1..6` en centi-arbres."""
    res_t, trig_t = compute_b2_resource_and_trigger_values_trees(obs, cfg, belief, weights)
    return (
        {k: v * TREE_SCORE_UNIT for k, v in res_t.items()},
        tuple(v * TREE_SCORE_UNIT for v in trig_t),
    )


def _score_tile_construction_b2(
    obs: PlayerObservation,
    cfg: GameConfig,
    tile_id: str,
    res_val: dict[str, float],
    trig_vals: tuple[float, ...],
) -> float:
    inv = 1.0 / TREE_SCORE_UNIT
    res_t = {k: v * inv for k, v in res_val.items()}
    trig_t = tuple(v * inv for v in trig_vals)
    return score_tile_construction_trees(obs, cfg, tile_id, res_t, trig_t) * TREE_SCORE_UNIT


def _score_gardien_pari(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
) -> float:
    val_trees = score_gardien_pari_marginal_trees(obs, cfg, belief, case_c, is_held=False)
    scale = TREE_SCORE_UNIT if is_b2 else (0.76 * TREE_SCORE_UNIT)
    return val_trees * scale


def _is_own_hand_covered(obs: PlayerObservation, cfg: GameConfig) -> bool:
    return is_own_hand_covered(obs, cfg)


def _score_reve_activation(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
    is_first_defender: bool = False,
) -> float:
    val_trees = score_reve_marginal_trees(
        obs, cfg, belief, case_c, is_held=False, is_first_defender=is_first_defender
    )
    scale = TREE_SCORE_UNIT if is_b2 else (0.78 * TREE_SCORE_UNIT)
    return val_trees * scale


def _furtivite_ray_deduction(
    obs: PlayerObservation,
    cfg: GameConfig,
    ray: int,
    *,
    is_first_defender: bool,
) -> tuple[int, int, bool, int, float, float]:
    return furtivite_ray_deduction(obs, cfg, ray, is_first_defender=is_first_defender)


def _best_untrapped_parcel_value_on_ray(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    _res_arbre: float,
    trig_piege_v: float,
) -> float:
    return (
        best_untrapped_parcel_trees(obs, cfg, belief, ray, trig_piege_v / TREE_SCORE_UNIT)
        * TREE_SCORE_UNIT
    )


# ---------------------------------------------------------------------------
# Fonctions de score de cibles Défenseurs pour B1 (k=1) et B2 (k=2)
# ---------------------------------------------------------------------------


def _score_target_b1_core(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    is_first_defender: bool,
) -> float:
    """Évaluation tactique 1-coup de B1 (le bruit novice est porté par le softmax `tau_b1`)."""
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        r_i, p_i = int(r), int(p)
        idx = r_i * MAX_P + (p_i - 1)
        defs = obs.parcel_defenseurs(r_i, p_i)
        ins = obs.parcel_insectes(r_i, p_i)
        cur_def = defs + ins
        raw_s_prob = belief.parcel_strike_prob[idx]
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF:
            s_prob = max(0.0, raw_s_prob - 0.95)
        else:
            s_prob = raw_s_prob
        c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
        seuil_e = belief.parcel_expected_seuil[idx]
        arbres = obs.parcel_arbres(r_i, p_i)
        souches = obs.parcel_souches(r_i, p_i)

        score = 95.0
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            score += 470.0
        if s_prob > 0.08 and cur_def < seuil_e:
            gap = seuil_e - cur_def
            reach_mult = 1.0 if gap <= 1.25 else (0.58 if gap <= 2.25 else 0.25)
            tree_weight = 1.10 if arbres >= 2 else (0.95 if arbres == 1 else 0.35)
            urgency = 600.0 * min(1.6, s_prob) * reach_mult * tree_weight
            if c_prob > 0.08 and gap <= 1.25:
                urgency += min(1.2, c_prob) * (75.0 if obs.tour <= 4 else 30.0)
            if arbres <= 1 and (belief.parcel_bulldo_prob[idx] > 0.15 or souches == 0):
                urgency += 150.0 * min(1.2, s_prob)
            if r_i == obs.observer_seat:
                urgency += 40.0
            score += urgency
        return score

    if kind == "LISIERE":
        _, slot_idx = target
        s_idx = int(slot_idx)
        if obs.mode < 2 or s_idx >= 2 * obs.n_players:
            return 0.0
        tile_id, st_l, constructors = obs.lisiere_tile_info(s_idx)
        if st_l != LISIERE_UNCONSTRUCTED:
            return 0.0
        fam, _, _ = SYNERGY_META[tile_id]
        reves_built = sum(1 for t in obs.piste_tactiques if is_reve_code(t.code))
        if fam == FAMILLE_REVE:
            fam_bonus = 95.0 if (obs.mode >= 3 or reves_built < 2) else 35.0
        elif fam == FAMILLE_CROISSANCE:
            fam_bonus = 85.0
        else:
            fam_bonus = 65.0
        if constructors == 1:
            return 610.0 + fam_bonus
        if belief.drew_sabotage_or_none and obs.tour <= 7:
            return 525.0 + fam_bonus
        return 255.0 + fam_bonus

    if kind == "FURTIVITE":
        _, ray, rive = target
        r_i, rv = int(ray), int(rive)
        if not obs.is_ray_furtivite_open(r_i):
            return 0.0
        d_rv = obs.furtivite_ray_rive_defs(r_i, rv)
        if d_rv >= 2:
            return 0.0
        partner_ready = d_rv == 1

        other_completed_rives = 0
        other_open_rives = 0
        for r2 in range(obs.n_players):
            for rv2 in (FURT_RIVE_PIEGE, FURT_RIVE_SABOTAGE):
                if r2 == r_i and rv2 == rv:
                    continue
                cnt2 = obs.furtivite_ray_rive_defs(r2, rv2)
                if cnt2 == 2:
                    other_completed_rives += 1
                elif cnt2 == 1:
                    other_open_rives += 1

        rat_cnt, _, own_card_is_ray, _, p_m2, p_m0 = _furtivite_ray_deduction(
            obs, cfg, r_i, is_first_defender=is_first_defender
        )

        if rv == FURT_RIVE_PIEGE:
            trap_v = _best_untrapped_parcel_value_on_ray(obs, cfg, belief, r_i, 115.0, 25.0)
            if trap_v <= 10.0:
                return 25.0
            if partner_ready and p_m2 >= 0.99:
                return 685.0 + 0.25 * trap_v
            if (
                is_first_defender
                and p_m2 >= 0.99
                and other_open_rives == 0
                and other_completed_rives == 0
                and (own_card_is_ray or r_i == obs.observer_seat)
            ):
                return 415.0 + 0.16 * trap_v
            if (
                (not is_first_defender)
                and (not partner_ready)
                and other_open_rives == 0
                and other_completed_rives == 0
                and (
                    (rat_cnt == 2 and belief.drew_sabotage_or_none)
                    or (own_card_is_ray and p_m2 >= 0.38 and trap_v >= 280.0)
                )
            ):
                return 345.0 + 0.18 * trap_v
            return 30.0

        sab_cnt_b1 = obs.sabotage_deck_count + obs.sabotage_pending_count
        ray_undef_b1 = sum(obs.parcel_def1_count(r_i, p) for p in range(1, cfg.p_max + 1)) == 0
        if obs.tour >= 8 or p_m0 < 0.24 or sab_cnt_b1 >= 3:
            return 30.0
        if partner_ready and p_m0 >= 0.30 and other_completed_rives == 0:
            return (545.0 if obs.tour <= 4 else 470.0) + 115.0 * p_m0
        if (
            (not is_first_defender)
            and other_open_rives == 0
            and other_completed_rives == 0
            and belief.drew_sabotage_or_none
            and obs.tour <= 5
            and p_m0 >= 0.28
        ):
            return (420.0 if sab_cnt_b1 <= 1 else 360.0) + 90.0 * p_m0
        if (
            (not is_first_defender)
            and other_open_rives == 0
            and other_completed_rives == 0
            and sab_cnt_b1 <= 1
            and obs.tour <= 4
            and p_m0 >= 0.32
            and (ray_undef_b1 or _is_own_hand_covered(obs, cfg))
        ):
            return 385.0 + 85.0 * p_m0 + (30.0 if ray_undef_b1 else 0.0)
        return 35.0

    if kind == "GARDIEN_PARI":
        return _score_gardien_pari(obs, cfg, belief, int(target[1]), is_b2=False)

    if kind == "REVE_ACTIVATION":
        return _score_reve_activation(
            obs, cfg, belief, int(target[1]), is_b2=False, is_first_defender=is_first_defender
        )

    return 0.0


class _B1TargetScorer:
    """Évaluateur B1 (Découverte) avec sélection softmax déterministe calibrable `softmax_tau`."""

    def __init__(self, softmax_tau: float = DEFAULT_TAU_B1) -> None:
        self.softmax_tau = max(0.0, float(softmax_tau))

    def __call__(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        target: tuple[Any, ...],
        is_first_defender: bool,
    ) -> float:
        return _score_target_b1_core(obs, cfg, belief, target, is_first_defender)


def make_b1_scorer(tau_b1: float = DEFAULT_TAU_B1) -> _B1TargetScorer:
    """Construit un évaluateur B1 paramétré par une température softmax `tau_b1` (0.0 = argmax)."""
    return _B1TargetScorer(softmax_tau=tau_b1)


score_target_b1 = _B1TargetScorer(softmax_tau=DEFAULT_TAU_B1)


def _score_target_b2_core(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    *,
    is_held: bool = False,
    is_first_defender: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
) -> float:
    """Noyau d'évaluation B2 en centi-arbres (`100.0 == 1.0 arbre marginalement sauvé`)."""
    return (
        score_target_b2_trees(
            obs,
            cfg,
            belief,
            target,
            is_held=is_held,
            is_first_defender=is_first_defender,
            weights=weights,
        )
        * TREE_SCORE_UNIT
    )


class _B2TargetScorer:
    """Évaluateur B2 unifié en équivalent-arbres (`B2Weights` < 100 paramètres)."""

    retreat_orphans: bool = True

    def __init__(self, weights: B2Weights = DEFAULT_B2_WEIGHTS) -> None:
        self.weights = weights

    def __call__(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        target: tuple[Any, ...],
        is_first_defender: bool,
    ) -> float:
        return _score_target_b2_core(
            obs,
            cfg,
            belief,
            target,
            is_held=False,
            is_first_defender=is_first_defender,
            weights=self.weights,
        )

    def held_score(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        cur_spot: tuple[Any, ...],
    ) -> float:
        return _score_target_b2_core(
            obs,
            cfg,
            belief,
            cur_spot,
            is_held=True,
            is_first_defender=False,
            weights=self.weights,
        )


def make_b2_scorer(weights: B2Weights = DEFAULT_B2_WEIGHTS) -> _B2TargetScorer:
    """Construit un évaluateur B2 paramétré par un jeu `B2Weights` (pour tuning automatique)."""
    return _B2TargetScorer(weights=weights)


score_target_b2 = _B2TargetScorer()


# ---------------------------------------------------------------------------
# Politique complète hors Étape 2 (Étapes 3, 4, 5, 6 et Effets de tuiles)
# ---------------------------------------------------------------------------


# Câblage recommandé Canon 0 v6.2 (contracts/tiles_canon_v6_2.json)
_CANON0_GARDIEN_CABLAGE: dict[str, tuple[int, int]] = {
    "G1": (TRIG_PARADE, TRIG_RESONANCE),
    "G2": (TRIG_SABOTAGE, TRIG_RESONANCE),
    "G3": (TRIG_PARADE, TRIG_RESONANCE),
    "G4": (TRIG_PIEGEAGE, TRIG_PARADE),
    "G5": (TRIG_PIEGEAGE, TRIG_RESONANCE),
    "G6": (TRIG_SABOTAGE, TRIG_PARADE),
    "G7": (TRIG_PIEGEAGE, TRIG_RESONANCE),
    "G8": (TRIG_SABOTAGE, TRIG_PARADE),
    "G9": (TRIG_SABOTAGE, TRIG_RESONANCE),
    "G10": (TRIG_SABOTAGE, TRIG_RESONANCE),
    "G11": (TRIG_SABOTAGE, TRIG_PIEGEAGE),
    "G12": (TRIG_SABOTAGE, TRIG_REVE),
    "G13": (TRIG_INSECTE, TRIG_PARADE),
    "G14": (TRIG_PIEGEAGE, TRIG_SABOTAGE),
    "G15": (TRIG_PARADE, TRIG_RESONANCE),
}


def _parcel_value_for_defense(
    obs: PlayerObservation,
    belief: BeliefSummary,
    r: int,
    p: int,
    *,
    extra_def: int = 0,
    is_trap: bool = False,
) -> float:
    """Estime la valeur tactique de protéger ou renforcer la parcelle `(r, p)`."""
    idx = r * MAX_P + (p - 1)
    arbres = obs.parcel_arbres(r, p)
    souches = obs.parcel_souches(r, p)
    defs = obs.parcel_defenseurs(r, p)
    ins = obs.parcel_insectes(r, p)
    seuil = belief.parcel_expected_seuil[idx]
    s_prob = max(0.35, belief.parcel_strike_prob[idx])
    has_trap = obs.parcel_piege(r, p) == PIEGE_ACTIF
    bulldo_p = belief.parcel_bulldo_prob[idx]

    sc = s_prob * (arbres * 55.0 + souches * (30.0 if bulldo_p >= 0.35 else 12.0))
    if obs.parcel_has_nid(r, p):
        sc += 65.0
    duel_st, duel_r, duel_p = obs.duel_state
    if duel_st != 0 and duel_r == r and duel_p == p:
        sc += 110.0 if duel_st == 1 else 60.0
    if is_trap:
        if has_trap:
            sc -= 260.0
        if defs + ins < seuil:
            sc += 240.0 + (95.0 if bulldo_p >= 0.35 and arbres <= 1 else 0.0)
        else:
            ins_saved = min(ins, max(0, int(seuil) - defs))
            sc += 40.0 + ins_saved * 65.0
    else:
        if has_trap:
            sc -= 180.0
        elif defs + ins < seuil:
            if defs + ins + extra_def >= seuil:
                sc += 340.0
            else:
                sc += 140.0
        else:
            sc += 10.0
    return sc


def _machine_danger_score(
    obs: PlayerObservation,
    cfg: GameConfig,
    rm: int,
    mt: int,
    *,
    prefer_assaut_flip: bool = False,
    prefer_near_ratissage: bool = False,
) -> float:
    m_obs = obs.machines[rm * 2 + mt]
    pos = m_obs.position
    st = m_obs.status
    if st == MACHINE_STATUS_RETIRED or pos <= 0:
        return -100.0
    sc = 80.0 + pos * 38.0 + m_obs.rouges * 52.0 - m_obs.bleus * 12.0
    if mt == MACHINE_ABATTEUSE:
        sc += 35.0
    if st == MACHINE_STATUS_RATISSAGE:
        sc += 190.0 if prefer_assaut_flip else 110.0
    if prefer_near_ratissage and st == MACHINE_STATUS_NORMAL and pos >= cfg.p_max - 1:
        sc += 250.0
    if prefer_assaut_flip:
        # Vérifier si la machine est actuellement révélée sur un rang d'Assaut (-2 net sur rouge->bleu !)
        card_c = machine_card_code(rm, mt)
        for s in range(obs.n_players):
            h = obs.hand_of(s)
            if h.card == card_c:
                rk = h.bound_tactique if (h.bound_tactique and is_tactique_code(h.bound_tactique)) else (h.lecture_m or 0)
                if 1 <= rk <= TRACK_LEN:
                    if not is_tactique_charge(rk, obs.tour):
                        sc += 155.0
                    else:
                        sc += 45.0
                    if rk in (3, 6):
                        sc += 35.0
                break
    return sc


def _score_effect_option(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    decision: DecisionRequest,
    opt: Any,
    *,
    is_b2: bool,
) -> float:
    """Évalue une option de `DEC_EFFET_TUILE` (Canon 0 v6.2 — 30 tuiles + Bug B) sur `PlayerObservation`."""
    kind_hint = str(decision.context.get("effect_kind", ""))
    n = obs.n_players
    p_max = cfg.p_max

    if opt == "PASSER":
        if kind_hint in ("G8_RETREAT_MACHINE", "G15_SWAP_RANKS", "G3_VOLTIGE"):
            return 120.0
        if kind_hint in ("G14_F1_DISCARD_PIEGE", "G14_F2_SRC_INSECT"):
            return 165.0
        if kind_hint in ("M1_EMBARK_INSECT", "M4_AFTER_PROD", "M5_MOVE_SOUCHE"):
            return 155.0
        if kind_hint == "R8_PICK_SOUCHE":
            return 210.0
        if kind_hint == "G12_SLIDE_REVE":
            return 115.0
        if kind_hint in ("G13_MOVE_INS_1", "G13_MOVE_INS_2", "G13_F2_PLACE_DUEL_ONLY"):
            return 110.0
        if kind_hint == "G5_PLACE_CROC":
            return 220.0
        if kind_hint == "G5_F2_MOVE_PIEGE":
            return 175.0
        return 25.0

    # --- Déviation Synaptique 3.2 (SLOT_BUG_CERVEAU:B) — icônes v6.2 : 4=REVE, 5=INSECTE ---
    if (
        isinstance(opt, str)
        and opt in ("M_MOINS_1", "M_PLUS_1")
        and kind_hint == "BUG_DEVIATION_SYNAPTIQUE_3_2"
    ):
        old_m = int(decision.context.get("case", 1))
        target_s = int(decision.context.get("target_seat", obs.observer_seat))
        d_m = -1 if opt == "M_MOINS_1" else 1
        new_m = max(1, min(6, old_m + d_m))
        old_c, _ = obs.tactique_code_bugs(old_m - 1)
        new_c, _ = obs.tactique_code_bugs(new_m - 1)
        eff_r = 1
        h_tgt = obs.hand_of(target_s)
        if h_tgt.card is not None and 1 <= h_tgt.card <= 2 * n:
            rt, mtt = unpack_machine_card(h_tgt.card)
            eff_r = obs.machine_effective_rouges(rt, mtt)
        bet_ins_bonus = 260.0 if (is_b2 and obs.gardien_pari_defenders(TRIG_INSECTE) >= 1) else 0.0
        bet_rev_pen = (
            -320.0
            if (is_b2 and is_reve_code(old_c) and obs.gardien_pari_defenders(TRIG_REVE) >= 1)
            else 0.0
        )
        if is_reve_code(new_c) and not is_reve_code(old_c):
            has_def_new = obs.reve_activation_defenders(new_m) >= 1
            return (760.0 if has_def_new else 95.0) + bet_ins_bonus
        if is_reve_code(old_c) and not is_reve_code(new_c):
            return -200.0 + bet_rev_pen
        d_old = _tactique_danger(old_m, obs.tour, eff_r)
        d_new = _tactique_danger(new_m, obs.tour, eff_r)
        return 35.0 + (d_old - d_new) * 4.0 + bet_ins_bonus

    # --- G1 (Jaguar) ---
    if kind_hint == "G1_MOVE_WAITING":
        dr, dp = int(opt[0]), int(opt[1])
        return 100.0 + _parcel_value_for_defense(obs, belief, dr, dp, extra_def=1)

    if kind_hint in ("G1_F2_FLIP_RED", "G6_FLIP_RED"):
        return _machine_danger_score(obs, cfg, int(opt[0]), int(opt[1]), prefer_assaut_flip=True)

    # --- G3 (Atèle) ---
    if kind_hint == "G3_VOLTIGE":
        sr, sp, dr, dp = int(opt[0]), int(opt[1]), int(opt[2]), int(opt[3])
        s_idx = sr * MAX_P + (sp - 1)
        src_defs = obs.parcel_defenseurs(sr, sp) + obs.parcel_insectes(sr, sp)
        src_seuil = belief.parcel_expected_seuil[s_idx]
        src_threat = belief.parcel_strike_prob[s_idx]
        src_cost = 40.0
        if obs.parcel_piege(sr, sp) != PIEGE_ACTIF and src_threat >= 0.30:
            src_cost = 420.0 if (src_defs >= src_seuil and src_defs - 1 < src_seuil) else 220.0 * src_threat
        dst_gain = _parcel_value_for_defense(obs, belief, dr, dp, extra_def=1)
        return dst_gain - src_cost

    # --- G4 (Ara) ---
    if kind_hint == "G4_SLIDE_NEIGHBOR":
        c_nbr = int(opt)
        rem = obs.gardien_pari_defenders(c_nbr)
        face = obs.gardien_face_at_case(c_nbr)
        # Terminer un pari (rem == 1 -> 0) et promouvoir Face 1 -> Face 2 est prioritaire
        return 200.0 + (180.0 if rem == 1 else 90.0) + (95.0 if face == 1 else 25.0)

    # --- G5 (Iguane) ---
    if kind_hint == "G5_PLACE_CROC":
        dr, dp = int(opt[0]), int(opt[1])
        return _parcel_value_for_defense(obs, belief, dr, dp, is_trap=True)

    if kind_hint == "G5_F2_MOVE_PIEGE":
        sr, sp, dr, dp = int(opt[0]), int(opt[1]), int(opt[2]), int(opt[3])
        s_idx = sr * MAX_P + (sp - 1)
        src_loss = belief.parcel_strike_prob[s_idx] * (obs.parcel_arbres(sr, sp) * 60.0 + 180.0)
        dst_gain = _parcel_value_for_defense(obs, belief, dr, dp, is_trap=True)
        return dst_gain - src_loss

    # --- G7 (Tapir) ---
    if kind_hint == "G7_PIEGE_SOUCHE":
        dr, dp = int(opt[0]), int(opt[1])
        idx = dr * MAX_P + (dp - 1)
        souches = obs.parcel_souches(dr, dp)
        return (
            _parcel_value_for_defense(obs, belief, dr, dp, is_trap=True)
            + souches * 65.0
            + belief.parcel_bulldo_prob[idx] * 140.0
        )

    # --- G8 (Boto) ---
    if kind_hint == "G8_RETREAT_MACHINE":
        rm, mt = int(opt[0]), int(opt[1])
        pos, st = obs.machine_pos_status(rm, mt)
        if st != MACHINE_STATUS_NORMAL or pos <= 1:
            return 0.0
        p_back = 0
        for cand_p in range(pos - 1, 0, -1):
            if not obs.is_route(rm, cand_p):
                p_back = cand_p
                break
        if p_back <= 0:
            return 0.0
        cur_arb = obs.parcel_arbres(rm, pos)
        back_arb = obs.parcel_arbres(rm, p_back)
        sc = 110.0 + (220.0 if pos >= p_max - 1 else 0.0)
        if back_arb == 0:
            sc += 210.0  # Recul sur clairière de Souches : frappe à blanc pour Abatteuse !
        elif back_arb < cur_arb:
            sc += 75.0 * (cur_arb - back_arb)
        elif back_arb > cur_arb and mt == MACHINE_ABATTEUSE:
            sc -= 90.0 * (back_arb - cur_arb)
        duel_st, duel_r, duel_p = obs.duel_state
        if duel_st != 0 and duel_r == rm and duel_p >= pos:
            sc += 130.0
        return sc

    # --- G9 (Caïman noir) ---
    if kind_hint == "G9_PLACE_CALE":
        rm, mt = int(opt[0]), int(opt[1])
        sc = _machine_danger_score(obs, cfg, rm, mt, prefer_near_ratissage=True)
        card_c = machine_card_code(rm, mt)
        for s in range(n):
            h = obs.hand_of(s)
            if h.card == card_c and (h.bound_tactique in (3, 6) or h.lecture_m in (3, 6)):
                sc += 160.0  # Absorbe l'avancée dès ce tour !
                break
        return sc

    # --- G10 F2 & R2 Enraciné (Altération) ---
    if kind_hint in ("G10_F2_ALTER_REVEALED", "R2_ROOT_ALTER"):
        return _machine_danger_score(obs, cfg, int(opt[0]), int(opt[1]), prefer_near_ratissage=True)

    # --- G11 (Harpie) & R9 (Écho) ---
    if kind_hint in ("G11_PLACE_PIEGE", "R9_PLACE_PIEGE"):
        return _parcel_value_for_defense(obs, belief, int(opt[0]), int(opt[1]), is_trap=True)

    if kind_hint == "G11_F2_MOVE_PLUME":
        face_p, kind_p, idx_p = int(opt[0]), int(opt[1]), int(opt[2])
        if kind_p != PLUME_KIND_RAY or face_p != PLUME_CHAUD:
            return 20.0
        # Pointer la Plume sur le rayon le plus boisé & menacé
        ray_sc = sum(
            obs.parcel_arbres(idx_p, p) * 20.0 + belief.parcel_strike_prob[idx_p * MAX_P + (p - 1)] * 85.0
            for p in range(1, p_max + 1)
            if not obs.is_route(idx_p, p)
        )
        return 100.0 + ray_sc

    # --- G12 (Ibijau) ---
    if kind_hint == "G12_SLIDE_REVE":
        rk = int(opt)
        steps = int(decision.context.get("steps", 1))
        case_now = rk + 1
        n_def_now = obs.reve_activation_defenders(case_now)
        dst_case = max(1, case_now - steps)
        # Avant résolution des Rêves : jackpot si le Rêve défendu glisse sous une machine active !
        hits_now = 0
        hits_dst = 0
        if obs.paravents_ouverts:
            for s in range(n):
                h = obs.hand_of(s)
                if h.card is not None and 1 <= h.card <= 2 * n and h.bound_tactique == 0:
                    if h.lecture_m == case_now:
                        hits_now += 1
                    elif h.lecture_m == dst_case:
                        hits_dst += 1
        sc = 180.0 + (7 - dst_case) * 28.0
        if n_def_now >= 1 and hits_dst > hits_now:
            sc += 580.0
        elif n_def_now >= 1 and hits_now > hits_dst:
            sc -= 360.0
        if (
            not obs.has_any_rooted_reve
            and cfg.total_reves_partie > 0
            and dst_case <= cfg.total_reves_partie
            and case_now > cfg.total_reves_partie
        ):
            sc += 210.0
        return sc

    # --- G13 (Tamanoir) ---
    if kind_hint == "G13_MOVE_INS_1":
        sr, sp, dr, dp = int(opt[0]), int(opt[1]), int(opt[2]), int(opt[3])
        src_ins = obs.parcel_insectes(sr, sp)
        src_pen = 160.0 if (obs.parcel_has_nid(sr, sp) and src_ins <= 2) else 25.0
        if obs.parcel_piege(sr, sp) != PIEGE_ACTIF and belief.parcel_strike_prob[sr * MAX_P + (sp - 1)] >= 0.45:
            src_pen += 120.0
        dst_gain = _parcel_value_for_defense(obs, belief, dr, dp, extra_def=1)
        return dst_gain - src_pen

    if kind_hint == "G13_MOVE_INS_2":
        sr, sp = int(opt[0]), int(opt[1])
        dr, dp = decision.context.get("dst", (sr, sp))
        src_ins = obs.parcel_insectes(sr, sp)
        src_pen = 165.0 if (obs.parcel_has_nid(sr, sp) and src_ins <= 2) else 25.0
        dst_gain = _parcel_value_for_defense(obs, belief, int(dr), int(dp), extra_def=1)
        return dst_gain - src_pen

    if kind_hint == "G13_F2_PLACE_DUEL_ONLY":
        if obs.duel_state[0] == DUEL_TERRITOIRE_TENU:
            return 10.0
        dr, dp = int(opt[0]), int(opt[1])
        idx = dr * MAX_P + (dp - 1)
        defs = obs.parcel_defenseurs(dr, dp)
        return 190.0 if (defs >= 1 and defs + obs.parcel_insectes(dr, dp) >= belief.parcel_expected_seuil[idx]) else 40.0

    # --- G14 (Téju) ---
    if kind_hint == "G14_F1_DISCARD_PIEGE":
        sr, sp, dp = int(opt[0]), int(opt[1]), int(opt[2])
        src_ins = obs.parcel_insectes(sr, sp)
        nid_pen = 195.0 if (obs.parcel_has_nid(sr, sp) and src_ins <= 2) else 35.0
        dst_gain = _parcel_value_for_defense(obs, belief, sr, dp, is_trap=True)
        return dst_gain - nid_pen

    if kind_hint == "G14_F2_SRC_INSECT":
        sr, sp = int(opt[0]), int(opt[1])
        src_ins = obs.parcel_insectes(sr, sp)
        if obs.parcel_has_nid(sr, sp) and src_ins <= 2:
            return 115.0  # Éviter de casser la masse critique 2 d'un Nid
        return 260.0 + min(3, src_ins) * 20.0 - belief.parcel_strike_prob[sr * MAX_P + (sp - 1)] * 95.0

    if kind_hint == "G14_F2_DST_TRAP_OR_CROC":
        kind_d, dr, dp = str(opt[0]), int(opt[1]), int(opt[2])
        sc = _parcel_value_for_defense(obs, belief, dr, dp, is_trap=True)
        if kind_d == "CROC" and obs.croc_parcel is None:
            sc += 55.0
        return sc

    # --- G15 (Colibri) ---
    if kind_hint == "G15_SWAP_RANKS":
        sa, sb = int(opt[0]), int(opt[1])
        ha = obs.hand_of(sa)
        hb = obs.hand_of(sb)
        if ha.card is None or hb.card is None:
            return 50.0
        ra, mta = unpack_machine_card(ha.card)
        rb, mtb = unpack_machine_card(hb.card)
        rka = ha.bound_tactique if (ha.bound_tactique and is_tactique_code(ha.bound_tactique)) else (ha.lecture_m or 1)
        rkb = hb.bound_tactique if (hb.bound_tactique and is_tactique_code(hb.bound_tactique)) else (hb.lecture_m or 1)
        red_a = obs.machine_effective_rouges(ra, mta)
        red_b = obs.machine_effective_rouges(rb, mtb)
        pos_a = obs.machine_pos_status(ra, mta)[0]
        pos_b = obs.machine_pos_status(rb, mtb)[0]
        # Coût avant vs après (Assaut + avancée sur machine chargée/proche cœur = très dangereux !)
        def _rank_cost(r_m: int, mt_m: int, pos_m: int, red_m: int, rk: int) -> float:
            c_rk = _tactique_danger(rk, obs.tour, red_m)
            if rk in (3, 6) and pos_m >= p_max - 1:
                c_rk += 55.0
            if not is_tactique_charge(rk, obs.tour):
                c_rk += red_m * 18.0
            if mt_m == MACHINE_ABATTEUSE:
                c_rk += obs.parcel_arbres(r_m, pos_m) * 6.0 if pos_m > 0 else 0.0
            return c_rk

        before = _rank_cost(ra, mta, pos_a, red_a, rka) + _rank_cost(rb, mtb, pos_b, red_b, rkb)
        after = _rank_cost(ra, mta, pos_a, red_a, rkb) + _rank_cost(rb, mtb, pos_b, red_b, rka)
        return 120.0 + (before - after) * 3.5

    # --- R4 (Sommeil de la Pierre-Serpent) ---
    if kind_hint == "R4_COMPLETE_FURT":
        r_f = int(opt)
        ray_arbres = sum(obs.parcel_arbres(r_f, p) for p in range(1, p_max + 1))
        return 260.0 + ray_arbres * 22.0

    # --- R5 (Vision des Plumes Claires) ---
    if kind_hint == "R5_DEPLOY_PLUME":
        return 100.0 + _parcel_value_for_defense(obs, belief, int(opt[0]), int(opt[1]), extra_def=1)

    # --- R6 (Miel des Ancêtres) ---
    if kind_hint == "R6_JOIN_NID":
        nr, np = int(opt[0]), int(opt[1])
        has_def = obs.parcel_defenseurs(nr, np) >= 1
        ins_n = obs.parcel_insectes(nr, np)
        return (380.0 if not has_def else 90.0) + (110.0 if ins_n >= 2 else 30.0)

    # --- R8 (Mirage du Fleuve-Miroir) ---
    if kind_hint == "R8_PICK_SOUCHE":
        sr, sp = int(opt[0]), int(opt[1])
        if obs.has_any_rooted_reve:
            return 90.0  # Sommeil impossible : inutile de sacrifier une Souche sauf urgence
        souches = obs.parcel_souches(sr, sp)
        sc = 220.0 + (120.0 if souches >= 2 else 0.0)
        if obs.parcel_is_bordered_by_rooted_tile(sr, sp):
            sc -= 240.0
        return sc

    if kind_hint == "R8_PICK_REVE_STEPS":
        r_num_t, steps_t = int(opt[0]), int(opt[1])
        cur_rk = next(
            (rk for rk in range(TRACK_LEN) if obs.reve_at_case(rk + 1) == r_num_t),
            TRACK_LEN - 1,
        )
        return 150.0 + steps_t * 140.0 + cur_rk * 25.0

    # --- R10 (Nuée des Songes) ---
    if kind_hint == "R10_PLACE_INSECT":
        if opt[0] == "NID":
            nr, np = int(opt[2]), int(opt[3])
            ins_n = obs.parcel_insectes(nr, np)
            def_n = obs.parcel_defenseurs(nr, np)
            if ins_n == 1 and def_n >= 1:
                return 430.0  # Passe la masse critique 1 -> 2 avant 4.2 !
            return 220.0 if def_n >= 1 else 140.0
        c_rk = int(opt[1])
        _, bugs_c = obs.tactique_code_bugs(c_rk - 1)
        return 280.0 if bugs_c == 0 else 150.0

    # --- M1 (Fourmilière Coupe-Feuilles) ---
    if kind_hint == "M1_EMBARK_INSECT":
        r_nid = int(decision.context.get("ray", 0))
        p_nid = int(decision.context.get("p", 1))
        mt = int(opt)
        cur_ins = obs.parcel_insectes(r_nid, p_nid)
        sc = _machine_danger_score(obs, cfg, r_nid, mt, prefer_assaut_flip=True)
        if cur_ins <= 2:
            sc -= 140.0  # Garder >= 2 Insectes au Nid sauf machine très dangereuse
        return sc

    # --- M4 (Ruche des Mélipones) ---
    if kind_hint == "M4_AFTER_PROD":
        r_nid = int(decision.context.get("ray", 0))
        p_nid = int(decision.context.get("p", 1))
        cur_ins = obs.parcel_insectes(r_nid, p_nid)
        nid_keep_pen = 110.0 if cur_ins <= 2 else 0.0
        if opt[0] == "SURCHAUFFE":
            return (
                _machine_danger_score(obs, cfg, int(opt[1]), int(opt[2]), prefer_assaut_flip=True)
                + 95.0
                - nid_keep_pen
            )
        if opt[0] == "TAMBOUR":
            tr, tp = int(opt[1]), int(opt[2])
            return _parcel_value_for_defense(obs, belief, tr, tp, extra_def=1) - nid_keep_pen

    # --- M5 (Jardin du Diable) ---
    if kind_hint == "M5_MOVE_SOUCHE":
        r_nid = int(decision.context.get("ray", 0))
        p_nid = int(decision.context.get("p", 1))
        dr, dp = int(opt[0]), int(opt[1])
        cur_ins = obs.parcel_insectes(r_nid, p_nid)
        nid_keep_pen = 140.0 if (cur_ins <= 2 and obs.tour <= 5) else 15.0
        souches_d = obs.parcel_souches(dr, dp)
        idx_d = dr * MAX_P + (dp - 1)
        # Valoriser les parcelles à Souches sur notre rayon (cible d'enracinement M5) ou menacées !
        root_bonus = 95.0 if (dr == obs.observer_seat and souches_d >= 2) else 0.0
        safe_bonus = 60.0 if belief.parcel_bulldo_prob[idx_d] < 0.25 else 0.0
        def_val = _parcel_value_for_defense(obs, belief, dr, dp, extra_def=1)
        return max(def_val, 140.0 + souches_d * 45.0 + root_bonus + safe_bonus) - nid_keep_pen

    return 100.0


def _choose_pose_piege_4_1_policy(
    obs: PlayerObservation,
    cfg: GameConfig,
    decision: DecisionRequest,
    *,
    is_b2: bool,
) -> int:
    """Choisit la parcelle (non-Route, sans Piège) où poser le Piège gagné en 4.1 par le propriétaire du rayon."""
    opts = tuple(int(p) for p in decision.options)
    if len(opts) == 1:
        return opts[0]

    ray = int(decision.context.get("ray", decision.decideur))
    p_max = cfg.p_max

    # À l'étape 4.1, les paravents sont ouverts : les Tactiques exactes (5.1) et Ratissages (5.2) sont connus !
    active_attacks: list[tuple[int, int, Any, bool, bool]] = []
    for s in range(obs.n_players):
        h = obs.hand_of(s)
        if (
            h.card is not None
            and 1 <= h.card <= 2 * obs.n_players
            and h.bound_tactique is not None
            and is_tactique_code(h.bound_tactique)
        ):
            r_m, mt_m = unpack_machine_card(h.card)
            if r_m == ray:
                pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
                if st_m == MACHINE_STATUS_NORMAL and pos_m > 0:
                    active_attacks.append(
                        (
                            mt_m,
                            pos_m,
                            TACTIQUES_SPEC[h.bound_tactique],
                            is_tactique_charge(h.bound_tactique, obs.tour),
                            False,
                        )
                    )
    for mt_m in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos_m, st_m = obs.machine_pos_status(ray, mt_m)
        if st_m == MACHINE_STATUS_RATISSAGE and pos_m > 0:
            active_attacks.append((mt_m, pos_m, TACTIQUES_SPEC[1], False, True))

    best_p = opts[0]
    best_sc = -1e9
    best_tb = -1

    for idx_o, cand_p in enumerate(opts):
        arbres = obs.parcel_arbres(ray, cand_p)
        souches = obs.parcel_souches(ray, cand_p)
        defs = obs.parcel_defenseurs(ray, cand_p)
        ins = obs.parcel_insectes(ray, cand_p)
        tot_def = defs + ins

        # Frappes visant exactement cand_p ce tour-ci
        strikes_hitting: list[tuple[int, int, bool, bool]] = []
        for mt_m, pos_m, spec, is_chg, is_rat in active_attacks:
            eff_red = 0 if is_chg else obs.machine_effective_rouges(ray, mt_m)
            bleus = obs.machines[ray * 2 + mt_m].bleus
            seuil = max(
                1,
                CANONICAL_DOTATION[cand_p - 1]
                + eff_red
                - bleus
                + spec.mod_seuil,
            )
            for c_kind in spec.cibles:
                if c_kind == "SUR_PLACE" and pos_m == cand_p:
                    strikes_hitting.append((mt_m, seuil, is_chg, is_rat))
                elif c_kind == "DEVANT":
                    for p_nx in range(pos_m + 1, p_max + 1):
                        if not obs.is_route(ray, p_nx):
                            if p_nx == cand_p:
                                strikes_hitting.append((mt_m, seuil, is_chg, is_rat))
                            break

        sc = 25.0 + arbres * 24.0 + souches * 6.0
        if obs.parcel_has_nid(ray, cand_p):
            sc += 95.0 if is_b2 else 55.0

        # Proximité des machines actives du rayon (pour un Piège persistant si non consommé dès ce tour)
        for mt_q in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            mp_q, ms_q = obs.machine_pos_status(ray, mt_q)
            if ms_q != MACHINE_STATUS_RETIRED and mp_q > 0:
                if cand_p == mp_q:
                    sc += 55.0 + 18.0 * obs.machine_effective_rouges(ray, mt_q)
                elif cand_p > mp_q:
                    dist_q = cand_p - mp_q
                    sc += max(10.0, 48.0 - 12.0 * dist_q)

        max_blocked = min(1, len(strikes_hitting))
        rem_arb = arbres
        rem_sch = souches
        for mt_h, seuil_h, is_chg_h, _ in strikes_hitting[:max_blocked]:
            if tot_def >= seuil_h:
                # Déjà paré en forêt : le Piège épargne surtout les Insectes défaussés et allume 2. Piégeage
                ins_saved = min(ins, max(0, seuil_h - defs))
                sc += 35.0 + ins_saved * (65.0 if is_b2 else 35.0)
            else:
                if mt_h == MACHINE_ABATTEUSE:
                    cut = rem_arb
                    rem_arb = 0
                    rem_sch += cut
                    sc += cut * 285.0 + 60.0
                    if is_chg_h:
                        sc += 210.0 if obs.tour <= 4 else 90.0
                else:
                    cut = min(1, rem_arb)
                    r_route = 240.0 if (rem_arb <= 1) else 0.0
                    rem_arb = max(0, rem_arb - cut)
                    rem_sch = 0
                    sc += cut * 285.0 + r_route + 85.0
                    if is_chg_h:
                        sc += 210.0 if obs.tour <= 4 else 90.0
            if is_b2 and obs.gardien_present_at_case(2):
                sc += 45.0

        tb = _tiebreak(cfg, obs, idx_o, 14)
        if sc > best_sc + 1e-9 or (abs(sc - best_sc) <= 1e-9 and tb > best_tb):
            best_sc, best_p, best_tb = sc, cand_p, tb

    return best_p


def _choose_policy(
    obs: PlayerObservation,
    decision: DecisionRequest,
    cfg: GameConfig,
    *,
    is_b2: bool,
    tau_b1: float = DEFAULT_TAU_B1,
) -> Any:
    opts = decision.options
    assert len(opts) >= 1
    if len(opts) == 1:
        return opts[0]

    dtype = decision.decision_type
    eff_tau = 0.0 if is_b2 else max(0.0, float(tau_b1))

    if dtype == DEC_POSE_PIEGE_FURTIVITE_4_1:
        return _choose_pose_piege_4_1_policy(obs, cfg, decision, is_b2=is_b2)

    scorer = score_target_b2 if is_b2 else score_target_b1
    belief = build_belief_summary(obs, cfg)

    if dtype == DEC_POSE_DEFENSEUR_1:
        scores_1 = [scorer(obs, cfg, belief, opt, True) for opt in opts]
        return opts[softmax_select_index(scores_1, eff_tau, cfg, obs, 1)]

    if dtype == DEC_POSE_DEFENSEUR_2:
        prefer_kind = "POSER_REFLEXION" if cfg.max_revision_passes > 0 else "POSER_DEFINITIF"
        filtered = [o for o in opts if o[0] == prefer_kind]
        if not filtered:
            filtered = list(opts)
        scores_2 = [scorer(obs, cfg, belief, opt[1], False) for opt in filtered]
        return filtered[softmax_select_index(scores_2, eff_tau, cfg, obs, 2)]

    if dtype == DEC_REVISION_DEFENSEUR_2:
        pass_idx = int(decision.context.get("pass", 1))
        eps = (24.0 if is_b2 else 32.0) + (pass_idx - 1) * 12.0
        move_opts = [o for o in opts if o[0] in ("DEPLACER_REFLEXION", "DEPLACER_DEFINITIF")]
        keep_opt: Any = None
        for o in opts:
            if o[0] in ("GARDER_REFLEXION", "VERROUILLER_DEFINITIF"):
                keep_opt = o
                break
        if not move_opts:
            return keep_opt if keep_opt is not None else opts[0]
        scores_rev = [scorer(obs, cfg, belief, mv[1], False) for mv in move_opts]
        pick_r = softmax_select_index(scores_rev, eff_tau, cfg, obs, 20 + pass_idx)
        if scores_rev[pick_r] > 520.0 + eps:
            return move_opts[pick_r]
        return keep_opt if keep_opt is not None else opts[0]

    if dtype == DEC_OISEAU_PERCHOIR_1_1:
        # Garde en main Sabotage/Écaille en priorité, sinon la carte machine la moins dangereuse
        for cand_c in opts:
            if int(cand_c) in (CARD_SABOTAGE, CARD_ECAILLE):
                return cand_c
        def _perchoir_sc(cand_c: int) -> tuple[float, int]:
            ci = int(cand_c)
            if 1 <= ci <= 2 * obs.n_players:
                rm, mt = unpack_machine_card(ci)
                pos_m, _ = obs.machine_pos_status(rm, mt)
                red_m = obs.machine_effective_rouges(rm, mt)
                arbres_m = obs.parcel_arbres(rm, pos_m) if pos_m > 0 else 0
                sc_m = -25.0 * pos_m - 20.0 * red_m - (15.0 if mt == MACHINE_BULLDOZER else 0.0) - 8.0 * arbres_m
            else:
                sc_m = 50.0
            return (sc_m, _tiebreak(cfg, obs, ci, 71))

        return max(opts, key=_perchoir_sc)

    if dtype == DEC_OISEAU_DE_ENVOL_1_3:
        own_h = obs.hand_of(obs.observer_seat)
        c_o = own_h.card
        def _envol_sc(rk: int) -> tuple[float, int]:
            ri = int(rk)
            t_c, t_bugs = obs.tactique_code_bugs(ri - 1)
            if is_reve_code(t_c):
                n_def_r = obs.reve_activation_defenders(ri)
                # Fort bonus pour tomber sur un Rêve (surtout déjà défendu ou défendable !)
                sc_r = 320.0 if n_def_r >= 1 else 185.0
                return (sc_r, _tiebreak(cfg, obs, ri, 72))
            sc_t = 0.0
            if is_tactique_code(t_c):
                spec = TACTIQUES_SPEC[t_c]
                is_chg = is_tactique_charge(t_c, obs.tour)
                sc_t -= 70.0 * len(spec.cibles)
                sc_t -= 30.0 * spec.mod_seuil
                if is_chg and obs.tour <= 6:
                    sc_t -= 45.0
                if t_bugs >= 1:
                    sc_t += 20.0
                if c_o is not None and 1 <= c_o <= 2 * obs.n_players:
                    rm, _ = unpack_machine_card(c_o)
                    pos_m, _ = obs.machine_pos_status(rm, unpack_machine_card(c_o)[1])
                    if pos_m > 0 and "SUR_PLACE" in spec.cibles and obs.parcel_piege(rm, pos_m) == PIEGE_ACTIF:
                        sc_t += 55.0
            return (sc_t, _tiebreak(cfg, obs, ri, 72))

        return max(opts, key=_envol_sc)

    if dtype == DEC_HUMAIN_CHAMAN_2_1:
        own_h = obs.hand_of(obs.observer_seat)
        own_hits_reve = (
            own_h.card is not None
            and 1 <= own_h.card <= 2 * obs.n_players
            and own_h.lecture_m is not None
            and obs.reve_at_case(own_h.lecture_m) > 0
        )
        if own_hits_reve and CHAMAN_CHANT in opts:
            return CHAMAN_CHANT
        if CHAMAN_TAMBOUR in opts:
            return CHAMAN_TAMBOUR
        return opts[0]

    if dtype == DEC_MAMMIFERE_DUEL_2:
        r_d = int(decision.context.get("ray", obs.observer_seat))
        p_d = int(decision.context.get("p", 1))
        idx_d = r_d * MAX_P + (p_d - 1)
        duel_st = obs.duel_state[0]
        if (
            duel_st != DUEL_TERRITOIRE_TENU
            and "POSER_DUEL_DEFI" in opts
            and (belief.parcel_strike_prob[idx_d] >= 0.15 or duel_st == 0)
        ):
            return "POSER_DUEL_DEFI"
        return "PASSER" if "PASSER" in opts else opts[0]

    if dtype == DEC_OISEAU_PLUME_2:
        own_h = obs.hand_of(obs.observer_seat)
        if own_h.card is not None and 1 <= own_h.card <= 2 * obs.n_players:
            r_o, _ = unpack_machine_card(own_h.card)
            cand_pl = (PLUME_CHAUD, PLUME_KIND_RAY, r_o)
            if cand_pl in opts:
                return cand_pl
        elif (not own_h.has_card) or own_h.card in (CARD_SABOTAGE, CARD_ECAILLE):
            target_r = obs.observer_seat
            if is_b2 and obs.mode >= 4:
                # Coordonner la Plume (face Calme honnête) avec G6/G11/R5/M3 sur le rayon le plus utile
                has_plume_tile = False
                for sl_p in range(obs.n_players * 5):
                    tid_p, _, st_p = obs.lisiere_tile_info(sl_p)
                    if st_p == LISIERE_CONSTRUCTED and tid_p in ("G6", "G11", "R5", "M3"):
                        has_plume_tile = True
                        break
                if has_plume_tile:
                    best_r_sc = -1.0
                    for r_c in range(obs.n_players):
                        r_sc = sum(
                            belief.parcel_strike_prob[r_c * MAX_P + (p_c - 1)]
                            * (obs.parcel_arbres(r_c, p_c) * 2.0 + 1.0)
                            for p_c in range(1, cfg.p_max + 1)
                            if not obs.is_route(r_c, p_c)
                        )
                        if r_sc > best_r_sc:
                            best_r_sc = r_sc
                            target_r = r_c
            cand_pl = (PLUME_CALME, PLUME_KIND_RAY, target_r)
            if cand_pl in opts:
                return cand_pl
        return "PASSER" if "PASSER" in opts else opts[0]

    if dtype == DEC_REPTILE_POSE_CROC_3_2:
        def _croc_sc(rp: tuple[int, int]) -> tuple[float, int]:
            r_c, p_c = int(rp[0]), int(rp[1])
            idx_c = r_c * MAX_P + (p_c - 1)
            defs_c = obs.parcel_defenseurs(r_c, p_c) + obs.parcel_insectes(r_c, p_c)
            seuil_c = belief.parcel_expected_seuil[idx_c]
            uncovered = 140.0 if defs_c < seuil_c else 15.0
            no_trap = 80.0 if obs.parcel_piege(r_c, p_c) == PIEGE_AUCUN else 10.0
            arbres_c = obs.parcel_arbres(r_c, p_c) * 45.0
            bulldo_b = 75.0 * belief.parcel_bulldo_prob[idx_c]
            nid_b = 55.0 if obs.parcel_has_nid(r_c, p_c) else 0.0
            return (uncovered + no_trap + arbres_c + bulldo_b + nid_b, _tiebreak(cfg, obs, idx_c, 73))

        return max(opts, key=_croc_sc)

    if dtype == DEC_CHOIX_CIBLE_REVE_3_2:
        def _seat_threat_h(s_id: int) -> tuple[int, int, int, int, int]:
            h_s = obs.hand_of(s_id)
            if h_s.card is not None and 1 <= h_s.card <= 2 * obs.n_players:
                rm, mt = unpack_machine_card(h_s.card)
                pos_m, st_m = obs.machine_pos_status(rm, mt)
                return machine_threat_key_3_2(
                    s_id, pos_m, st_m, obs.machine_effective_rouges(rm, mt)
                )
            return (0, 0, 0, 0, -s_id)

        return max(
            opts,
            key=lambda combo: (
                tuple(sorted((_seat_threat_h(int(s_i)) for s_i in combo), reverse=True)),
                _tiebreak(cfg, obs, opts.index(combo), 74),
            ),
        )

    if dtype == DEC_BOUCLIER_LISIERE_5_3:
        g_face = int(decision.context.get("face", 1))
        if (obs.tour <= 7 or g_face == 2) and "UTILISER_BOUCLIER" in opts:
            return "UTILISER_BOUCLIER"
        return "LAISSER_RETOURNER" if "LAISSER_RETOURNER" in opts else opts[0]

    if dtype == DEC_ENRACINEMENT_6_1:
        # Enraciner en fin de partie (Tours 6-8) avec ciblages Canon 0 (R2, R6, M5, G7)
        if obs.tour < 6:
            return "PASSER" if "PASSER" in opts else opts[0]
        reves_on = sum(1 for c_r in range(1, TRACK_LEN + 1) if obs.reve_at_case(c_r) > 0)
        g7_f2_active = any(
            g_sl.gardien_num == 7 and g_sl.face == 2 for g_sl in obs.piste_gardiens
        )
        mobile_active = sum(
            1
            for r_m in range(obs.n_players)
            for mt_m in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
            if obs.machine_pos_status(r_m, mt_m)[1] == MACHINE_STATUS_NORMAL
            and obs.machine_pos_status(r_m, mt_m)[0] > 0
        )
        best_rt: Any = "PASSER" if "PASSER" in opts else opts[0]
        best_sc_rt = 0.0
        for opt in opts:
            if opt == "PASSER":
                continue
            sl_idx, p_rt = int(opt[0]), int(opt[1])
            souches = obs.parcel_souches(obs.observer_seat, p_rt)
            tid_rt, _, _ = obs.lisiere_tile_info(sl_idx)
            fam_rt, _, num_rt = SYNERGY_META[tid_rt]
            # Éviter d'enraciner un Rêve si la victoire Sommeil est à portée avant le Tour 8
            if fam_rt == FAMILLE_REVE and obs.tour <= 7 and reves_on >= max(1, cfg.total_reves_partie - 1):
                continue
            gain_trees = 1
            if tid_rt.startswith("G"):
                for c_g in range(1, TRACK_LEN + 1):
                    g_sl = obs.piste_gardiens[c_g - 1]
                    if g_sl.gardien_num == num_rt and g_sl.face == 2:
                        gain_trees = 2
                        break
            elif obs.mode >= 4 and tid_rt == "M5":
                gain_trees = 1 + obs.parcel_insectes(obs.observer_seat, p_rt)

            effective_gain = min(souches, gain_trees)
            if obs.mode >= 4 and tid_rt == "R6":
                # R6 enraciné : retourne +1 Souche survivante sur une parcelle voisine (Pont routier)
                has_neigh_souche = False
                for step_d in (-1, 1):
                    p_cur = p_rt + step_d
                    while 1 <= p_cur <= cfg.p_max and obs.is_route(obs.observer_seat, p_cur):
                        p_cur += step_d
                    if 1 <= p_cur <= cfg.p_max and obs.parcel_souches(obs.observer_seat, p_cur) >= 1:
                        has_neigh_souche = True
                        break
                if has_neigh_souche:
                    effective_gain += 1

            r2_tempo_bonus = 0.0
            if obs.mode >= 4 and tid_rt == "R2" and obs.tour <= 7 and mobile_active >= 1:
                r2_tempo_bonus = 125.0 * float(min(2, mobile_active))

            if effective_gain <= 0 and r2_tempo_bonus <= 0.0:
                continue
            if obs.tour == 6 and effective_gain < 2 and r2_tempo_bonus < 120.0:
                continue
            # Privilégier les parcelles plus proches du cœur (moins exposées aux routes) et Face 2
            sc_rt = 100.0 * float(effective_gain) + r2_tempo_bonus + 12.0 * float(p_rt)
            if g7_f2_active and obs.tour <= 7:
                sc_rt += 28.0
            if obs.tour == 8:
                sc_rt += 50.0
            if sc_rt > best_sc_rt:
                best_sc_rt = sc_rt
                best_rt = opt
        return best_rt

    if dtype == DEC_EFFET_TUILE:
        scores_e = [_score_effect_option(obs, cfg, belief, decision, opt, is_b2=is_b2) for opt in opts]
        return opts[softmax_select_index(scores_e, eff_tau, cfg, obs, 7)]

    if dtype == DEC_ORDRE_CONSTRUCTION_3_1:
        res_val, trig_vals = (
            _compute_b2_resource_and_trigger_values(obs, cfg, belief)
            if is_b2
            else ({}, (20.0,) * 6)
        )
        scores_c: list[float] = []
        for slot_idx in opts:
            tid, _, _ = obs.lisiere_tile_info(int(slot_idx))
            if is_b2:
                sc = _score_tile_construction_b2(obs, cfg, tid, res_val, trig_vals)
            else:
                fam, _, _ = SYNERGY_META[tid]
                sc = 300.0 if fam == FAMILLE_REVE else (200.0 if fam == FAMILLE_CROISSANCE else 100.0)
            scores_c.append(sc)
        return opts[softmax_select_index(scores_c, eff_tau, cfg, obs, 31)]

    if dtype == DEC_CHOIX_CASE_GARDIEN:
        has_ins_peuple = "I" in cfg.peuples
        sab_tot = (
            obs.sabotage_deck_count
            + obs.sabotage_pending_count
            + obs.ecaille_deck_count
            + obs.ecaille_pending_count
        )
        reves_on = sum(1 for c2 in range(1, TRACK_LEN + 1) if obs.reve_at_case(c2) > 0)
        g_on_1_5 = sum(1 for c2 in range(1, 6) if obs.gardien_present_at_case(c2))
        w_ins = 88.0 if has_ins_peuple else 25.0
        w_sab = 89.0 if (is_b2 and sab_tot >= 2) else (81.0 if (is_b2 and sab_tot == 1) else 62.0)
        if cfg.total_reves_partie == 0:
            w_rev = 25.0
        else:
            w_rev = 83.0 if (is_b2 and reves_on >= 1) else 68.0
        w_res = 82.0 + (28.0 if (is_b2 and g_on_1_5 >= 2) else 0.0)
        case_weights = {
            TRIG_PARADE: 95.0,
            TRIG_PIEGEAGE: 79.0,
            TRIG_SABOTAGE: w_sab,
            TRIG_REVE: w_rev,
            TRIG_INSECTE: w_ins,
            TRIG_RESONANCE: w_res,
        }
        tid = str(decision.context.get("tile_id", ""))
        if obs.mode >= 4 and tid in _CANON0_GARDIEN_CABLAGE:
            p_trig, f_trig = _CANON0_GARDIEN_CABLAGE[tid]

            def _trig_viable(tr: int) -> bool:
                if tr == TRIG_SABOTAGE:
                    return sab_tot >= 1 or tid in ("G2", "G9", "G10")
                if tr == TRIG_INSECTE:
                    return has_ins_peuple
                if tr == TRIG_REVE:
                    return cfg.total_reves_partie > 0
                if tr == TRIG_RESONANCE:
                    return g_on_1_5 >= 1
                return True

            p_bonus = (44.0 if _trig_viable(p_trig) else 10.0) if is_b2 else (22.0 if _trig_viable(p_trig) else 5.0)
            f_bonus = (24.0 if _trig_viable(f_trig) else 6.0) if is_b2 else (12.0 if _trig_viable(f_trig) else 3.0)
            case_weights[p_trig] = case_weights.get(p_trig, 50.0) + p_bonus
            case_weights[f_trig] = case_weights.get(f_trig, 50.0) + f_bonus
            if tid == "G4":
                # Ara : maximiser le nombre de Gardiens voisins immédiats sur la piste 1..6
                for c_opt in opts:
                    ci = int(c_opt)
                    n_adj = (1 if (ci > 1 and obs.gardien_present_at_case(ci - 1)) else 0) + (
                        1 if (ci < TRACK_LEN and obs.gardien_present_at_case(ci + 1)) else 0
                    )
                    adj_b = n_adj * (38.0 if is_b2 else 20.0) + (14.0 if 2 <= ci <= 5 else 0.0)
                    case_weights[ci] = case_weights.get(ci, 50.0) + adj_b
        elif is_b2 and obs.mode >= 3 and tid:
            econ = get_economie_catalog()
            prof_g = cfg.profile_for_slot(tid)
            node = econ.get((tid, prof_g)) if prof_g is not None else None
            if node is not None and node.is_law:
                case_weights = {
                    TRIG_PARADE: 110.0,
                    TRIG_PIEGEAGE: 86.0,
                    TRIG_SABOTAGE: (92.0 if sab_tot >= 1 else 68.0),
                    TRIG_REVE: (85.0 if cfg.total_reves_partie > 0 else 35.0),
                    TRIG_INSECTE: (95.0 if has_ins_peuple else 25.0),
                    TRIG_RESONANCE: 105.0,
                }
        return max(opts, key=lambda c: (case_weights.get(int(c), 50.0), _tiebreak(cfg, obs, int(c), 3)))

    if dtype == DEC_PLACEMENT_NID_3_1:
        def _nid_parcel_sc(rp: tuple[int, int]) -> tuple[float, int]:
            r_n, p_n = int(rp[0]), int(rp[1])
            idx = r_n * MAX_P + (p_n - 1)
            safety = -180.0 * belief.parcel_strike_prob[idx]
            depth_v = p_n * 65.0 + obs.parcel_arbres(r_n, p_n) * 18.0
            return (depth_v + safety, _tiebreak(cfg, obs, idx, 4))

        return max(opts, key=_nid_parcel_sc)

    if dtype == DEC_LIBERATION_BATISSEUR_3_1:
        def _lib_sc(opt: tuple[int, int, int, int]) -> tuple[float, int]:
            _, _, r_l, p_l = opt
            sc = scorer(obs, cfg, belief, ("FORET", int(r_l), int(p_l)), False)
            return (sc, _tiebreak(cfg, obs, int(r_l) * 10 + int(p_l), 5))

        return max(opts, key=_lib_sc)

    if dtype == DEC_MIGRATION_INSECTE_4_3:
        src = decision.context.get("source", ("FORET", 0, 1))
        src_kind, src_a, src_p = src
        n_pl = obs.n_players
        p_max = cfg.p_max
        if src_kind == "FORET":
            sr, sp = int(src_a), int(src_p)
            sr_idx = sr * MAX_P + (sp - 1)
            sr_defs = obs.parcel_defenseurs(sr, sp)
            sr_ins = obs.parcel_insectes(sr, sp)
            sr_seuil = belief.parcel_expected_seuil[sr_idx]
            # En v6.2 les Pièges sont autonomes : ne retenir un Insecte que s'il boucle une Parade classique !
            if (
                is_b2
                and obs.parcel_piege(sr, sp) != PIEGE_ACTIF
                and belief.parcel_strike_prob[sr_idx] >= 0.50
                and sr_defs < sr_seuil
                and (sr_defs + sr_ins) >= sr_seuil
                and (sr_defs + sr_ins - 1) < sr_seuil
            ):
                return ("RESTER",)

        total_forest_ins = sum(
            obs.parcel_insectes(r_f, p_f)
            for r_f in range(n_pl)
            for p_f in range(1, p_max + 1)
        )
        total_bugs = sum(obs.tactique_code_bugs(c_b)[1] for c_b in range(TRACK_LEN))
        total_colonies = sum(obs.piste_colonie)
        g_ins_present = obs.gardien_present_at_case(TRIG_INSECTE)
        g_ins_bet = obs.gardien_pari_defenders(TRIG_INSECTE) >= 1

        def _has_frontline_machine(r_q: int, p_q: int) -> bool:
            for mt_q in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                mp_q, ms_q = obs.machine_pos_status(r_q, mt_q)
                if ms_q != MACHINE_STATUS_RETIRED and (mp_q == p_q or mp_q == p_q - 1):
                    return True
            return False

        def _mig_sc(mv: tuple[Any, ...]) -> float:
            mk = mv[0]
            if mk == "COLONIE":
                c_num = int(mv[1])
                has_g = obs.gardien_present_at_case(c_num)
                rem_bets = obs.gardien_pari_defenders(c_num)
                cur_col = obs.piste_colonie[c_num - 1]
                if has_g and rem_bets >= 1 and cur_col == 0:
                    if c_num in (TRIG_SABOTAGE, TRIG_REVE):
                        return 620.0 if is_b2 else 560.0
                    return 485.0 if is_b2 else 450.0
                if has_g and cur_col == 0:
                    if not is_b2:
                        return 280.0
                    if total_colonies == 0:
                        return 340.0
                    if total_colonies == 1:
                        return 250.0
                    return 155.0
                return 115.0
            if mk == "BUG":
                c_num = int(mv[1])
                t_code, t_bugs = obs.tactique_code_bugs(c_num - 1)
                if is_tactique_code(t_code) and t_bugs == 0:
                    if is_b2:
                        if total_bugs == 0:
                            base_bug = 440.0
                        elif total_bugs == 1:
                            base_bug = 380.0
                        elif total_bugs == 2:
                            base_bug = 280.0
                        else:
                            base_bug = 180.0
                    else:
                        base_bug = 410.0
                    right_of_reve = (
                        c_num >= 2 and is_reve_code(obs.tactique_code_bugs(c_num - 2)[0])
                    )
                    danger_b = 65.0 if t_code in (3, 6) else 25.0
                    g_ins_b = 45.0 if (is_b2 and g_ins_present and total_bugs <= 1) else 0.0
                    return base_bug + danger_b + (55.0 if (is_b2 and right_of_reve) else 0.0) + g_ins_b
                return 150.0
            if mk == "FORET":
                dr, dp = int(mv[1]), int(mv[2])
                d_idx = dr * MAX_P + (dp - 1)
                d_defs = obs.parcel_defenseurs(dr, dp)
                d_ins = obs.parcel_insectes(dr, dp)
                d_seuil = belief.parcel_expected_seuil[d_idx]
                has_p_dst = obs.parcel_piege(dr, dp) == PIEGE_ACTIF
                if not has_p_dst and belief.parcel_strike_prob[d_idx] >= 0.50 and (d_defs + d_ins) < d_seuil:
                    if (d_defs + d_ins + 1) >= d_seuil:
                        return 610.0 + (65.0 if g_ins_bet else 0.0)
                    return 440.0
                if is_b2 and obs.parcel_has_nid(dr, dp) and d_ins == 1:
                    return 420.0
                if (
                    is_b2
                    and not has_p_dst
                    and obs.parcel_arbres(dr, dp) >= 1
                    and d_ins < 2
                    and _has_frontline_machine(dr, dp)
                ):
                    return 445.0 if total_forest_ins <= n_pl + 1 else 365.0
                if obs.mode >= 2 and src_kind == "FORET" and dp > int(src_p):
                    return 290.0
                return 95.0
            # RESTER : valoriser la conservation d'une réserve forestière (soutien Parade, Nid +2, 5. Insecte)
            if is_b2 and src_kind == "FORET":
                sr_r, sp_r = int(src_a), int(src_p)
                cur_ins_r = obs.parcel_insectes(sr_r, sp_r)
                stay_sc = 180.0
                if obs.parcel_has_nid(sr_r, sp_r) and cur_ins_r <= 2:
                    stay_sc += 250.0
                elif (
                    obs.parcel_piege(sr_r, sp_r) != PIEGE_ACTIF
                    and obs.parcel_arbres(sr_r, sp_r) >= 1
                    and cur_ins_r <= 2
                    and _has_frontline_machine(sr_r, sp_r)
                ):
                    stay_sc += 255.0
                    if total_forest_ins <= n_pl:
                        stay_sc += 55.0
                    if g_ins_present:
                        stay_sc += 35.0
                elif obs.parcel_arbres(sr_r, sp_r) >= 1 and cur_ins_r == 1 and total_forest_ins <= n_pl:
                    stay_sc += 210.0
                return stay_sc
            return 160.0  # RESTER

        mig_scores = [_mig_sc(opt) for opt in opts]
        return opts[softmax_select_index(mig_scores, eff_tau, cfg, obs, 43)]

    if dtype == DEC_ORDRE_ATTAQUE_5_1:
        rank_ctx = int(decision.context.get("rank", 1))
        return _choose_best_attack_order(
            obs, cfg, opts, rank_1_6=rank_ctx, is_ratissage=False
        )

    if dtype == DEC_ORDRE_RATISSAGE_5_2:
        return _choose_best_attack_order(
            obs, cfg, opts, rank_1_6=None, is_ratissage=True
        )

    if dtype == DEC_ORDRE_NID_4_2:
        return _choose_best_nid_order_4_2(obs, opts)

    best_idx = max(range(len(opts)), key=lambda i: _tiebreak(cfg, obs, i, 11))
    return opts[best_idx]


def _simulate_ray_machine_seq_loss(
    obs: PlayerObservation,
    cfg: GameConfig,
    ray: int,
    seq: tuple[int, ...],
    tactique: TactiqueSpec,
    *,
    is_ratissage: bool,
) -> tuple[int, int, int, int, int, int]:
    """Simule localement l'ordre de frappe d'une séquence de machines sur un même rayon depuis `obs`.

    Retourne un tuple de coût minimaliste à minimiser lexicographiquement :
    `(trees_lost, routes_created, charge_red_gains, insects_spent, traps_used, souches_lost)`.
    """
    p_max = cfg.p_max
    arbres = [0] * (p_max + 1)
    souches = [0] * (p_max + 1)
    defs = [0] * (p_max + 1)
    ins = [0] * (p_max + 1)
    piege = [PIEGE_AUCUN] * (p_max + 1)
    is_route = [True] * (p_max + 1)
    for p in range(1, p_max + 1):
        arbres[p] = obs.parcel_arbres(ray, p)
        souches[p] = obs.parcel_souches(ray, p)
        defs[p] = obs.parcel_defenseurs(ray, p)
        ins[p] = obs.parcel_insectes(ray, p)
        piege[p] = obs.parcel_piege(ray, p)
        is_route[p] = obs.is_route(ray, p)

    init_trees = sum(arbres[1:])
    init_souches = sum(souches[1:])

    m_pos = [0, 0]
    m_st = [MACHINE_STATUS_RETIRED, MACHINE_STATUS_RETIRED]
    m_red = [0, 0]
    m_blue = [0, 0]
    machines_obs = obs.machines
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st = obs.machine_pos_status(ray, mt)
        m_pos[mt] = pos
        m_st[mt] = st
        m_red[mt] = obs.machine_effective_rouges(ray, mt)
        m_blue[mt] = machines_obs[ray * 2 + mt].bleus

    def _next_fwd(from_p: int) -> int | None:
        for p_i in range(from_p + 1, p_max + 1):
            if not is_route[p_i]:
                return p_i
        return None

    def _next_back(from_p: int) -> int | None:
        for p_i in range(from_p - 1, 0, -1):
            if not is_route[p_i]:
                return p_i
        return None

    routes_created = 0
    charge_red_gains = 0
    insects_spent = 0
    traps_used = 0

    for mt in seq:
        pos = m_pos[mt]
        st = m_st[mt]
        if st == MACHINE_STATUS_RETIRED or pos <= 0:
            continue
        eff_rat = is_ratissage or st == MACHINE_STATUS_RATISSAGE
        is_charge = (not eff_rat) and is_tactique_charge(tactique.code, obs.tour)

        targets: list[int] = []
        for c_type in tactique.cibles:
            if c_type == "SUR_PLACE":
                if not is_route[pos]:
                    targets.append(pos)
            elif c_type == "DEVANT":
                p_dev = _next_fwd(pos)
                if p_dev is not None:
                    targets.append(p_dev)

        unparried = 0
        for tp in targets:
            if is_route[tp]:
                continue
            if piege[tp] == PIEGE_ACTIF:
                piege[tp] = PIEGE_AUCUN
                traps_used += 1
                continue
            base_s = CANONICAL_DOTATION[tp - 1]
            seuil = max(
                1,
                base_s + (0 if is_charge else m_red[mt]) - m_blue[mt] + tactique.mod_seuil,
            )
            if defs[tp] + ins[tp] >= seuil:
                manque = max(0, seuil - defs[tp])
                used = min(ins[tp], manque)
                ins[tp] -= used
                insects_spent += used
                continue
            unparried += 1
            if mt == MACHINE_ABATTEUSE:
                cut = arbres[tp]
                arbres[tp] = 0
                souches[tp] += cut
            else:
                cut = min(1, arbres[tp])
                arbres[tp] -= cut
                souches[tp] = 0
            if arbres[tp] == 0 and souches[tp] == 0:
                is_route[tp] = True
                defs[tp] = 0
                ins[tp] = 0
                piege[tp] = PIEGE_AUCUN
                routes_created += 1
                for m_other in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                    if m_st[m_other] != MACHINE_STATUS_RETIRED and m_pos[m_other] == tp:
                        p_b = _next_back(tp)
                        if p_b is not None:
                            m_pos[m_other] = p_b
                        else:
                            p_f = _next_fwd(tp)
                            if p_f is not None:
                                m_pos[m_other] = p_f
                            else:
                                m_pos[m_other] = 0
                                m_st[m_other] = MACHINE_STATUS_RETIRED

        if is_charge and unparried >= 1 and m_st[mt] != MACHINE_STATUS_RETIRED and m_pos[mt] > 0:
            charge_red_gains += 1
            m_red[mt] = min(15, m_red[mt] + 1)

        if (not eff_rat) and m_st[mt] == MACHINE_STATUS_NORMAL and m_pos[mt] > 0 and tactique.avancee > 0:
            for _ in range(tactique.avancee):
                p_nxt = _next_fwd(m_pos[mt])
                if p_nxt is not None:
                    m_pos[mt] = p_nxt

    trees_lost = init_trees - sum(arbres[1:])
    souches_lost = max(0, init_souches - sum(souches[1:]))
    return (trees_lost, routes_created, charge_red_gains, insects_spent, traps_used, souches_lost)


def _attack_lights_available_gardien_trigger(
    obs: PlayerObservation,
    cfg: GameConfig,
    ray: int,
    m_type: int,
    tactique: TactiqueSpec,
    *,
    is_ratissage: bool,
) -> int:
    """Retourne 1 si résoudre `(ray, m_type)` en premier allume un déclencheur Gardien (1, 2 ou 6) actif."""
    if obs.mode < 2:
        return 0
    pos, st = obs.machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos <= 0:
        return 0
    eff_rat = is_ratissage or st == MACHINE_STATUS_RATISSAGE
    is_charge = (not eff_rat) and is_tactique_charge(tactique.code, obs.tour)
    eff_red = obs.machine_effective_rouges(ray, m_type)
    bleus = obs.machines[ray * 2 + m_type].bleus
    p_max = cfg.p_max

    targets: list[int] = []
    for c_type in tactique.cibles:
        if c_type == "SUR_PLACE":
            if not obs.is_route(ray, pos):
                targets.append(pos)
        elif c_type == "DEVANT":
            for p_i in range(pos + 1, p_max + 1):
                if not obs.is_route(ray, p_i):
                    targets.append(p_i)
                    break

    for tp in targets:
        if obs.parcel_piege(ray, tp) == PIEGE_ACTIF:
            if obs.gardien_available_at_case(TRIG_PIEGEAGE):
                return 1
            continue
        seuil = max(
            1,
            CANONICAL_DOTATION[tp - 1]
            + (0 if is_charge else eff_red)
            - bleus
            + tactique.mod_seuil,
        )
        d_cnt = obs.parcel_defenseurs(ray, tp)
        i_cnt = obs.parcel_insectes(ray, tp)
        if d_cnt + i_cnt >= seuil:
            trig = TRIG_INSECTE if (seuil > d_cnt and i_cnt > 0) else TRIG_PARADE
            if obs.gardien_available_at_case(trig):
                return 1
    return 0


def _choose_best_attack_order(
    obs: PlayerObservation,
    cfg: GameConfig,
    opts: tuple[Any, ...],
    *,
    rank_1_6: int | None,
    is_ratissage: bool,
) -> Any:
    """Choisit de manière déterministe la machine minimisant la perte d'arbres en 5.1 ou 5.2."""
    tactique = (
        RATISSAGE_TACTIQUE_SPEC
        if (is_ratissage or rank_1_6 is None or rank_1_6 not in TACTIQUES_SPEC)
        else TACTIQUES_SPEC[rank_1_6]
    )

    by_ray: dict[int, list[int]] = {}
    for opt in opts:
        r_i, mt_i = int(opt[0]), int(opt[1])
        by_ray.setdefault(r_i, []).append(mt_i)

    deferred_losers: set[tuple[int, int]] = set()
    pair_gain: dict[tuple[int, int], tuple[int, int, int, int, int, int]] = {}
    zero_gain = (0, 0, 0, 0, 0, 0)

    for r_i, mts in by_ray.items():
        if len(mts) == 2:
            m0, m1 = mts[0], mts[1]
            loss_01 = _simulate_ray_machine_seq_loss(
                obs, cfg, r_i, (m0, m1), tactique, is_ratissage=is_ratissage
            )
            loss_10 = _simulate_ray_machine_seq_loss(
                obs, cfg, r_i, (m1, m0), tactique, is_ratissage=is_ratissage
            )
            if loss_01 < loss_10:
                deferred_losers.add((r_i, m1))
                pair_gain[(r_i, m0)] = (
                    loss_10[0] - loss_01[0],
                    loss_10[1] - loss_01[1],
                    loss_10[2] - loss_01[2],
                    loss_10[3] - loss_01[3],
                    loss_10[4] - loss_01[4],
                    loss_10[5] - loss_01[5],
                )
            elif loss_10 < loss_01:
                deferred_losers.add((r_i, m0))
                pair_gain[(r_i, m1)] = (
                    loss_01[0] - loss_10[0],
                    loss_01[1] - loss_10[1],
                    loss_01[2] - loss_10[2],
                    loss_01[3] - loss_10[3],
                    loss_01[4] - loss_10[4],
                    loss_01[5] - loss_10[5],
                )

    def _priority_key(opt: Any) -> tuple[Any, ...]:
        r_i, mt_i = int(opt[0]), int(opt[1])
        is_allowed_first = 0 if (r_i, mt_i) in deferred_losers else 1
        gain = pair_gain.get((r_i, mt_i), zero_gain)
        lights_g = _attack_lights_available_gardien_trigger(
            obs, cfg, r_i, mt_i, tactique, is_ratissage=is_ratissage
        )
        return (is_allowed_first, gain, lights_g, -r_i, -mt_i)

    return max(opts, key=_priority_key)


def _choose_best_nid_order_4_2(
    obs: PlayerObservation,
    opts: tuple[Any, ...],
) -> Any:
    """Choisit de manière déterministe l'ordre d'activation des Nids en 4.2 depuis `obs`."""
    nid_loc: dict[int, tuple[int, int]] = {}
    for r_i, row in enumerate(obs.foret):
        for p_off, parcel in enumerate(row):
            if parcel.nid_id > 0:
                nid_loc[parcel.nid_id] = (r_i, p_off + 1)

    def _nid_key(opt: Any) -> tuple[int, int, int, int]:
        m_num = int(opt)
        loc = nid_loc.get(m_num)
        if loc is None:
            return (0, 0, 0, -m_num)
        r_i, p_i = loc
        threat = 0
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            m_pos, m_st = obs.machine_pos_status(r_i, mt)
            if m_st != MACHINE_STATUS_RETIRED and m_pos in (p_i, p_i - 1):
                threat += 1
        arbres = obs.parcel_arbres(r_i, p_i)
        cur_ins = obs.parcel_insectes(r_i, p_i)
        # Prioriser les Nids sur parcelles menacées et riches en arbres (et ceux qui produisent +2)
        prod_bonus = 2 if cur_ins >= 2 else 1
        return (threat, arbres, prod_bonus, -m_num)

    return max(opts, key=_nid_key)


class BotB1:
    """Bot Découverte B1 (`k = 1`, bruit novice calibrable par softmax déterministe `tau_b1`)."""

    @staticmethod
    def choose(
        obs: PlayerObservation,
        decision: DecisionRequest,
        cfg: GameConfig,
        *,
        tau_b1: float = DEFAULT_TAU_B1,
    ) -> Any:
        return _choose_policy(obs, decision, cfg, is_b2=False, tau_b1=tau_b1)


class BotB2:
    """Bot Cœur de cible B2 (`k = 2`, économie unifiée arbres < 100 params + CRN Gardiens/Rêves)."""

    @staticmethod
    def choose(obs: PlayerObservation, decision: DecisionRequest, cfg: GameConfig) -> Any:
        return _choose_policy(obs, decision, cfg, is_b2=True)


def choose_b1(
    state: GameState,
    decision: DecisionRequest,
    *,
    tau_b1: float = DEFAULT_TAU_B1,
) -> Any:
    """Point d'entrée isolé B1 : extrait uniquement PlayerObservation pour `decision.decideur`."""
    obs = state.get_observation(decision.decideur)
    return BotB1.choose(obs, decision, state.cfg, tau_b1=tau_b1)


def choose_b2(state: GameState, decision: DecisionRequest) -> Any:
    """Point d'entrée isolé B2 : extrait uniquement PlayerObservation pour `decision.decideur`."""
    obs = state.get_observation(decision.decideur)
    return BotB2.choose(obs, decision, state.cfg)


def choose_b2_open(state: GameState, decision: DecisionRequest) -> Any:
    """Plafond contrefactuel à paravents ouverts (équipe omnisciente, zéro mutation des règles)."""
    if state.paravents_ouverts:
        obs = state.get_observation(decision.decideur)
    else:
        saved = state.paravents_ouverts
        state.paravents_ouverts = True
        try:
            obs = state.get_observation(decision.decideur)
        finally:
            state.paravents_ouverts = saved
    return BotB2.choose(obs, decision, state.cfg)


def _play_game_cooperative(
    state: GameState,
    *,
    is_b2: bool,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
    counterfactual_open_paravents: bool = False,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    gardien_reve_rollouts: int = 8,
    tau_b1: float = DEFAULT_TAU_B1,
) -> GameOver:
    if is_b2:
        scorer: Any = score_target_b2 if weights is DEFAULT_B2_WEIGHTS else make_b2_scorer(weights)
    else:
        scorer = score_target_b1 if tau_b1 == DEFAULT_TAU_B1 else make_b1_scorer(tau_b1)

    if is_b2 and counterfactual_open_paravents:
        chooser = choose_b2_open
        bot_label = "B2_OPEN"
    elif is_b2:
        chooser = choose_b2
        bot_label = "B2"
    else:
        def _choose_b1_tau(st_in: GameState, dec_in: DecisionRequest) -> Any:
            return choose_b1(st_in, dec_in, tau_b1=tau_b1)

        chooser = choose_b1 if tau_b1 == DEFAULT_TAU_B1 else _choose_b1_tau
        bot_label = "B1"

    def _post_rev_crn(st_now: GameState) -> int:
        return arbitrate_step2_gardien_reve_crn(
            st_now,
            chooser=chooser,
            counterfactual_open_paravents=counterfactual_open_paravents,
            n_rollouts=gardien_reve_rollouts,
            telemetry=telemetry,
        )

    post_hook = _post_rev_crn if (is_b2 and gardien_reve_rollouts > 0 and state.cfg.mode >= 3) else None
    steps = 0

    while True:
        steps += 1
        if steps > max_steps:
            cfg = state.cfg
            raise RuntimeError(
                f"Garde-fou max_steps={max_steps} dépassé ({bot_label}) : "
                f"mode={cfg.mode}, chassis_id={chassis_id}, n_players={cfg.n_players}, "
                f"exp_seed={cfg.exp_seed}, rep_id={cfg.rep_id}, tour={state.tour}, "
                f"step={state.step}, continuation={state._continuation!r}"
            )
        out = step_until_decision(
            state, max_internal_steps=max(2000, max_steps), telemetry=telemetry
        )
        if isinstance(out, GameOver):
            return out

        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_HUMAIN_CHAMAN_2_1,
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            resolve_step2_full_with_ticks(
                state,
                scorer,
                k_max_passes=k_max_passes,
                epsilon_base=24.0 if is_b2 else 32.0,
                epsilon_step=12.0,
                telemetry=telemetry,
                counterfactual_open_paravents=counterfactual_open_paravents,
                post_revision_hook=post_hook,
            )
            continue

        choice = chooser(state, out)
        apply_choice(state, choice, telemetry=telemetry)


def play_game_b1(
    state: GameState,
    *,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
    tau_b1: float = DEFAULT_TAU_B1,
) -> GameOver:
    """Exécute une partie complète pilotée par B1 (Ticks 1..3 + softmax calibrable `tau_b1`)."""
    return _play_game_cooperative(
        state,
        is_b2=False,
        k_max_passes=k_max_passes,
        max_steps=max_steps,
        chassis_id=chassis_id,
        telemetry=telemetry,
        gardien_reve_rollouts=0,
        tau_b1=tau_b1,
    )


def play_game_b2(
    state: GameState,
    *,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    gardien_reve_rollouts: int = 8,
) -> GameOver:
    """Exécute une partie complète pilotée par B2 (économie arbres unifiée + CRN Gardiens/Rêves)."""
    return _play_game_cooperative(
        state,
        is_b2=True,
        k_max_passes=k_max_passes,
        max_steps=max_steps,
        chassis_id=chassis_id,
        telemetry=telemetry,
        weights=weights,
        gardien_reve_rollouts=gardien_reve_rollouts,
    )


def play_game_b2_open(
    state: GameState,
    *,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
    weights: B2Weights = DEFAULT_B2_WEIGHTS,
    gardien_reve_rollouts: int = 8,
) -> GameOver:
    """Plafond d'équipe omnisciente à paravents ouverts (`counterfactual_open_paravents=True`)."""
    return _play_game_cooperative(
        state,
        is_b2=True,
        k_max_passes=k_max_passes,
        max_steps=max_steps,
        chassis_id=chassis_id,
        telemetry=telemetry,
        counterfactual_open_paravents=True,
        weights=weights,
        gardien_reve_rollouts=gardien_reve_rollouts,
    )
