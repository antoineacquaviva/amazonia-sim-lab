"""Moteur heuristique B1 (Découverte, k=1) et B2 (Cœur de cible, k=2, graphe economie_bot)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from bots.belief_and_ticks import (
    BeliefSummary,
    build_belief_summary,
    resolve_step2_full_with_ticks,
)
from engine.core_engine import (
    DEC_CHOIX_CASE_GARDIEN,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_ORDRE_ATTAQUE_5_1,
    DEC_ORDRE_CONSTRUCTION_3_1,
    DEC_ORDRE_NID_4_2,
    DEC_ORDRE_RATISSAGE_5_2,
    DEC_PLACEMENT_NID_3_1,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest, GameOver
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CANONICAL_DOTATION,
    CARD_SABOTAGE,
    FAMILLE_CROISSANCE,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    GARDIEN_BET_CAP,
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
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameConfig,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    unpack_machine_card,
)

__all__ = (
    "ALL_12_RESOURCES",
    "BotB1",
    "BotB2",
    "EconomieNode",
    "choose_b1",
    "choose_b2",
    "choose_b2_open",
    "count_active_laws_from_obs",
    "get_economie_catalog",
    "play_game_b1",
    "play_game_b2",
    "play_game_b2_open",
    "score_target_b1",
    "score_target_b2",
)

ALL_12_RESOURCES: tuple[str, ...] = (
    "RES_INSECTE",
    "RES_PIEGE",
    "RES_DEFENSEUR",
    "RES_JETON_BLEU",
    "RES_JETON_ROUGE",
    "RES_APPRENTISSAGE",
    "RES_SEUIL_PARADE",
    "RES_DILUTION_SABOTAGE",
    "RES_SOUCHE",
    "RES_ARBRE",
    "RES_POSITION_MACHINE",
    "RES_POSITION_PISTE",
)

# Loi exacte de M = min(D1, D2) sur 2D6 équilibrés : P(M = k) = (13 - 2k) / 36 pour k = 1..6
_MIN_2D6_PROBS_H: tuple[float, ...] = (
    11.0 / 36.0,
    9.0 / 36.0,
    7.0 / 36.0,
    5.0 / 36.0,
    3.0 / 36.0,
    1.0 / 36.0,
)

# Courbe temporelle de RES_DILUTION_SABOTAGE (Tours 1..8) :
# calibrée sur l'espérance cumulée d'annulations d'activations machine sur les (8 - tour) distributions
# futures en 1.2 après injection au remélange 6.3 (+ création d'émetteurs coopératifs Tick 1).
_SABOTAGE_TOUR_WEIGHT: tuple[float, ...] = (
    285.0,  # index 0 (inutilisé)
    285.0,  # Tour 1 (7 distributions futures)
    270.0,  # Tour 2 (6 distributions futures)
    245.0,  # Tour 3 (5 distributions futures)
    210.0,  # Tour 4 (4 distributions futures)
    165.0,  # Tour 5 (3 distributions futures)
    95.0,   # Tour 6 (2 distributions futures)
    25.0,   # Tour 7 (1 seule distribution au Tour 8)
    0.0,    # Tour 8 (0 remélange futur)
)


def _tactique_danger(rank_1_6: int, tour: int, eff_red: int = 1) -> float:
    """Danger tactique dynamique v6.0 d'une case 1..6 selon Acte 1/2 (CHARGE vs ASSAUT) et puissance."""
    if not (1 <= rank_1_6 <= TRACK_LEN):
        return 30.0
    is_double = rank_1_6 in (3, 6)
    base = 72.0 if is_double else (28.0 if rank_1_6 in (2, 5) else 22.0)
    if is_tactique_charge(rank_1_6, tour):
        # En CHARGE : jetons ignorés à la frappe mais risque de +1 jeton Puissance durable
        rem_turns = max(0, 8 - tour)
        return base + (24.0 + 6.5 * rem_turns) * (1.25 if is_double else 1.0)
    # En ASSAUT : tous les jetons Puissance s'appliquent au seuil de parade
    return base + 22.0 * max(0, eff_red) * (1.35 if is_double else 1.0)


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


class _EconomieStore:
    cache: ClassVar[dict[tuple[str, str], EconomieNode] | None] = None
    last_b1_obs: ClassVar[PlayerObservation | None] = None
    last_b1_laws: ClassVar[int] = 0
    last_b2_obs: ClassVar[PlayerObservation | None] = None
    last_b2_res: ClassVar[dict[str, float]] = {}
    last_b2_trigs: ClassVar[tuple[float, ...]] = ()


def get_economie_catalog() -> dict[tuple[str, str], EconomieNode]:
    """Charge une seule fois le graphe orienté `economie_bot` depuis `data/spec_bundle_v6_0.json`."""
    if _EconomieStore.cache is not None:
        return _EconomieStore.cache

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
                inputs_requis=tuple(str(x) for x in eb.get("inputs_requis", [])),
                outputs_produits=tuple(str(x) for x in eb.get("outputs_produits", [])),
            )

    _EconomieStore.cache = nodes
    return nodes


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


def _b1_forgetting_penalty(
    obs: PlayerObservation, cfg: GameConfig, active_laws: int, item_salt: int
) -> float:
    """Oubli stochastique contrôlé de B1 via rng.py dès que > 2 lois sont actives simultanément."""
    if active_laws <= 2:
        return 0.0
    excess = active_laws - 2
    # Probabilité d'oubli bornée : 22 % par loi excédentaire au-delà de 2 (plafond 66 %)
    threshold_permille = min(660, excess * 220)
    roll = (
        rand_u64(
            cfg.exp_seed,
            cfg.rep_id,
            SRC_BOT_TIEBREAK,
            obs.tour,
            obs.observer_seat + 64,
            item_salt & 0xFFFFFFFF,
        )
        % 1000
    )
    if roll < threshold_permille:
        # Perturbation d'évaluation due à l'oubli de la loi par un joueur Découverte (B1)
        sign = 1.0 if (roll & 1) else -1.0
        return sign * (55.0 + 25.0 * excess)
    return 0.0


# ---------------------------------------------------------------------------
# Graphe dynamique B2 (`economie_bot` k=2 + Lookahead 5.1 -> 6.2)
# ---------------------------------------------------------------------------


def _compute_b2_resource_and_trigger_values(
    obs: PlayerObservation, cfg: GameConfig, _belief: BeliefSummary
) -> tuple[dict[str, float], tuple[float, ...]]:
    """Calcule dynamiquement la valeur des 12 `RES_*` et la propagation k=2 des `TRIG_1..6`."""
    if _EconomieStore.last_b2_obs is obs:
        return _EconomieStore.last_b2_res, _EconomieStore.last_b2_trigs

    n = obs.n_players
    p_max = cfg.p_max
    tour = min(8, max(1, obs.tour))
    machines = obs.machines
    gardiens = obs.piste_gardiens

    # Pression globale sur les Arbres et risque de Routes
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

    # Proximité des victoires anticipées en 5.3 (Sommeil bloc des k Rêves en tête / Réveil Gardiens)
    total_reves_cfg = cfg.total_reves_partie
    reves_ranks = [
        r_idx + 1
        for r_idx in range(TRACK_LEN)
        if is_reve_code(obs.tactique_code_bugs(r_idx)[0])
    ]
    reves_in_head = sum(1 for rk in reves_ranks if rk <= total_reves_cfg)

    face1_g = 0
    for c in range(TRACK_LEN):
        g_slot = gardiens[c]
        if g_slot.gardien_num > 0 and g_slot.face != 2:
            face1_g += 1

    if obs.mode >= 3 and total_reves_cfg > 0 and len(reves_ranks) >= total_reves_cfg:
        reve_push_mult = 1.75 if reves_in_head >= total_reves_cfg - 1 else 1.40
    elif obs.mode >= 3 and total_reves_cfg > 0 and len(reves_ranks) > 0:
        reve_push_mult = 1.25
    else:
        reve_push_mult = 1.0
    reveil_awaken_bonus = (
        45.0 if (obs.gardien_pari_enabled and obs.mode >= 3 and face1_g > 0) else 0.0
    )

    res_val: dict[str, float] = {
        "RES_ARBRE": 115.0 + 7.0 * fragile_parcels,
        "RES_SOUCHE": 16.0,
        "RES_DEFENSEUR": 68.0 + 4.0 * fragile_parcels,
        "RES_PIEGE": 95.0 + 5.0 * total_rouges,
        "RES_INSECTE": 52.0 if total_insects < 2 * n else 34.0,
        "RES_SEUIL_PARADE": 62.0 + 4.0 * fragile_parcels,
        "RES_JETON_BLEU": 64.0 + (22.0 if tour <= 6 else 8.0),
        "RES_JETON_ROUGE": 72.0 + 8.0 * max(0, 8 - tour),
        "RES_APPRENTISSAGE": (48.0 * reve_push_mult) if tour <= 7 else 8.0,
        "RES_DILUTION_SABOTAGE": _SABOTAGE_TOUR_WEIGHT[tour],
        "RES_POSITION_MACHINE": 70.0 + 4.0 * fragile_parcels,
        "RES_POSITION_PISTE": 78.0 * reve_push_mult,
    }

    # Propagation k = 2 sur les déclencheurs TRIG_1..6 des Gardiens présents sur la piste
    trig_val = [12.0] * (TRACK_LEN + 1)
    if obs.mode >= 2:
        econ = get_economie_catalog() if obs.mode >= 3 else None
        for c in range(1, TRACK_LEN + 1):
            g_slot = gardiens[c - 1]
            if g_slot.gardien_num > 0 and g_slot.remaining_defenders >= 1 and g_slot.tile_id is not None:
                v_open = 38.0 + (reveil_awaken_bonus if g_slot.face == 1 else 0.0)
                if econ is not None:
                    prof = cfg.profile_for_slot(g_slot.tile_id)
                    node = econ.get((g_slot.tile_id, prof)) if prof is not None else None
                    if node is not None:
                        v_open += sum(
                            res_val.get(out_tok, 20.0) * 0.45 for out_tok in node.outputs_produits
                        )
                trig_val[c] = v_open

        resonance_4 = trig_val[4] if obs.gardien_available_at_case(4) else 0.0
        for c in range(1, TRACK_LEN + 1):
            if c != 4 and obs.gardien_available_at_case(c):
                trig_val[c] += 0.55 * resonance_4
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
                                    trig_val[c] += 0.40 * trig_val[t_idx]

    trigs_tuple = tuple(trig_val[1:])
    _EconomieStore.last_b2_obs = obs
    _EconomieStore.last_b2_res = res_val
    _EconomieStore.last_b2_trigs = trigs_tuple
    return res_val, trigs_tuple


def _score_tile_construction_b2(
    obs: PlayerObservation,
    cfg: GameConfig,
    tile_id: str,
    res_val: dict[str, float],
    trig_vals: tuple[float, ...],
) -> float:
    fam, _, _ = SYNERGY_META[tile_id]
    tour = obs.tour
    # Valeur structurelle Mode 2+ (bouclier Rêve 2.1/2.2 + déclencheur 5. Rêve, production Nid, Pari Gardiens)
    if fam == FAMILLE_REVE:
        reves_on_track = sum(1 for t in obs.piste_tactiques if is_reve_code(t.code))
        target_reves = max(1, cfg.total_reves_partie)
        if obs.mode == 2:
            # En Mode 2 v6.1 (blocage pur sans déplacement Sommeil), 1 à 2 Rêves sur la Réglette
            # suffisent comme bouclier 1-Défenseur (dès 2.1 !) et déclencheur 5. Rêve pour l'Éveil.
            if reves_on_track == 0:
                struct_v = 185.0 if tour <= 5 else (115.0 if tour == 6 else 55.0)
            elif reves_on_track == 1:
                struct_v = 140.0 if tour <= 5 else (85.0 if tour == 6 else 40.0)
            else:
                struct_v = 65.0 if tour <= 5 else 30.0
        else:
            if reves_on_track < target_reves:
                struct_v = (
                    195.0
                    if reves_on_track == 0
                    else (170.0 if reves_on_track + 1 == target_reves else 150.0)
                )
            else:
                struct_v = 85.0
            if tour >= 7 and reves_on_track < target_reves - 1:
                struct_v *= 0.45
    elif fam == FAMILLE_CROISSANCE:
        struct_v = 175.0 if tour <= 5 else 90.0
    else:
        g_on_track = sum(1 for g in obs.piste_gardiens if g.gardien_num > 0)
        # Pour l'Éveil sous UNIFORM_MAX_2, il faut au minimum ceil(N / 2) Gardiens (2 à 3-4J, 3 à 5-6J) !
        min_g_eveil = (obs.n_players + 1) // 2
        if obs.gardien_pari_enabled:
            if g_on_track < min_g_eveil:
                struct_v = 165.0
            elif obs.mode >= 3:
                struct_v = 105.0
            elif obs.n_players >= 5 and g_on_track == min_g_eveil and tour <= 6:
                # Un 4e Gardien neutre à 5-6J diversifie les déclencheurs disponibles pour l'Éveil
                struct_v = 125.0
            else:
                # En Mode 2 (Gardiens neutres), ne pas gaspiller de Défenseurs sur des Gardiens surnuméraires
                struct_v = 45.0
        else:
            struct_v = 105.0 if obs.mode >= 3 else 45.0

    if obs.mode < 3:
        return struct_v

    econ = get_economie_catalog()
    prof = cfg.profile_for_slot(tile_id)
    if prof is None:
        return struct_v
    node = econ.get((tile_id, prof))
    if node is None:
        return struct_v

    econ_bonus = 0.0
    for out_tok in node.outputs_produits:
        if out_tok in res_val:
            econ_bonus += 0.55 * res_val[out_tok]
        elif out_tok.startswith("TRIG_"):
            t_i = int(out_tok[5:]) - 1
            if 0 <= t_i < 6:
                econ_bonus += 0.50 * trig_vals[t_i]

    # Pénalité légère si un input matériel rare (ex: RES_PIEGE / RES_INSECTE) est totalement absent du plateau
    if "RES_INSECTE" in node.inputs_requis and fam != FAMILLE_CROISSANCE:
        has_any_ins = any(
            obs.parcel_insectes(r, p) > 0
            for r in range(obs.n_players)
            for p in range(1, cfg.p_max + 1)
        )
        if not has_any_ins:
            econ_bonus -= 30.0

    if node.is_law and tour <= 5:
        econ_bonus += 35.0
    return struct_v + econ_bonus


def _estimate_expected_gardien_triggers(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    *,
    for_eveil: bool = False,
) -> tuple[float, float, float, float, float, float]:
    """Estime le nombre attendu de déclencheurs sur les cases 1..6 (strictement sur PlayerObservation).

    Si `for_eveil=True`, ne compte en forêt et sur les Rêves que les 1ers Défenseurs (`parcel_def1_count`,
    `reve_def1_count`), car lors d'un Éveil 100 % Gardiens tous les `N` 2es Défenseurs vont sur les Gardiens.
    """
    n = obs.n_players
    p_max = cfg.p_max

    exp_parade = 0.0
    exp_piege = 0.0
    exp_sabotage = 0.0
    exp_reve = 0.0
    exp_insecte = 0.0

    # 1) Étapes 5.1 / 5.2 : partition stricte par frappe bloquée (2. Piégeage > 6. Insecte > 1. Parade)
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
            piege_armed = obs.parcel_piege(r, p) == PIEGE_ACTIF
            seuil_e = belief.parcel_expected_seuil[idx]
            c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
            if piege_armed:
                # 2. Piégeage autonome SINGLE_STRIKE (pare exactement 1 frappe puis est défaussé)
                exp_piege += min(1.0, s_prob)
            elif defs >= seuil_e:
                # 1. Parade uniquement (Défenseurs seuls, sans dépense d'Insecte)
                exp_parade += min(1.35, s_prob)
            elif cur_def >= seuil_e and ins >= 1:
                # 6. Insecte uniquement (Parade classique défaussant >= 1 Insecte)
                exp_insecte += min(1.35, s_prob)
            elif defs >= seuil_e - 0.55 and defs >= 1 and ins == 0:
                exp_parade += 0.50 * min(1.0, s_prob)
            elif cur_def >= seuil_e - 0.55 and ins >= 1:
                exp_insecte += 0.50 * min(1.0, s_prob)
            elif cur_def >= 1 and c_prob > 0.20 and cur_def >= (CANONICAL_DOTATION[p - 1] - 0.25):
                # En Acte 2, une frappe tombant sur une case CHARGE (4..6) ignore les rouges et peut être parée !
                if ins >= 1 and defs < CANONICAL_DOTATION[p - 1]:
                    exp_insecte += 0.55 * min(1.0, c_prob)
                else:
                    exp_parade += 0.55 * min(1.0, c_prob)

    # Bonus Furtivité Rive Piège déjà complétée (en 2.1 si for_eveil, sinon 2.1+2.2) -> Piège autonome posé en 4.1 !
    for r_f in range(n):
        cnt_rp = (
            obs.furtivite_ray_def1_rive_count(r_f, FURT_RIVE_PIEGE)
            if for_eveil
            else obs.furtivite_ray_rive_defs(r_f, FURT_RIVE_PIEGE)
        )
        if cnt_rp == 2:
            exp_piege += 0.75

    # 2) Étape 3.2 : partition stricte par carte révélée (3. Sabotage > 6. Insecte Bug > 5. Rêve actif)
    own_hand = obs.hand_of(obs.observer_seat)
    own_card = own_hand.card
    own_is_sab = own_card == CARD_SABOTAGE
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
        own_on_reve = obs.reve_at_case(own_m) > 0
        own_bugs = obs.tactique_code_bugs(own_m - 1)[1]
        if own_on_reve:
            r_defs_own = (
                obs.reve_def1_count(own_m)
                if for_eveil
                else obs.reve_activation_defenders(own_m)
            )
            if r_defs_own >= 1:
                exp_reve += 0.95
                if r_defs_own == 1:
                    own_reve_consumed_sole_def = own_m
        elif own_bugs >= 1:
            # Un Bug présent sur notre rang M peut dévier le dé -> allume 6. Insecte (et non 5. Rêve)
            exp_insecte += 0.85

    # Espérance prudente pour les (n - 1) autres sièges (strictement sur information publique et loi exacte min(2D6))
    active_deck_machines = 0
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            m_pos, m_st = obs.machine_pos_status(r, mt)
            if m_st == MACHINE_STATUS_NORMAL and m_pos > 0:
                active_deck_machines += 1
    sab_in_deck = obs.sabotage_deck_count
    sab_others = max(0, sab_in_deck - (1 if own_is_sab else 0))
    total_deck_est = max(n, active_deck_machines + sab_in_deck)
    p_other_sab = min(0.85, sab_others / max(1.0, float(total_deck_est - 1)))
    if sab_others >= 1:
        exp_sabotage += 0.75 * min(float(sab_others), float(n - 1) * p_other_sab)

    p_other_mach = max(0.0, 1.0 - p_other_sab)
    # En v6.1, un 1er Défenseur (2.1) posé sur un Rêve y reste pendant l'Éveil 100 % Gardiens et allume 5. Rêve !
    prob_reve_rank = 0.0
    for c_r in range(1, TRACK_LEN + 1):
        if obs.reve_at_case(c_r) <= 0 or c_r == own_reve_consumed_sole_def:
            continue
        r_defs = obs.reve_def1_count(c_r) if for_eveil else obs.reve_activation_defenders(c_r)
        if r_defs >= 1:
            prob_reve_rank += _MIN_2D6_PROBS_H[c_r - 1]
    if prob_reve_rank > 0.0:
        exp_reve += 0.84 * float(n - 1) * p_other_mach * prob_reve_rank

    # Bugs présents sur la piste Tactiques (hors Rêves) pouvant dévier les autres machines -> 6. Insecte
    total_bugs_avail = 0
    prob_bug_rank = 0.0
    for c_b in range(1, TRACK_LEN + 1):
        if obs.reve_at_case(c_b) == 0:
            b_cnt = obs.tactique_code_bugs(c_b - 1)[1]
            if b_cnt >= 1:
                total_bugs_avail += b_cnt
                prob_bug_rank += _MIN_2D6_PROBS_H[c_b - 1]
    if total_bugs_avail > 0:
        exp_insecte += 0.72 * min(
            float(total_bugs_avail), float(n - 1) * p_other_mach * prob_bug_rank
        )

    return (exp_parade, exp_piege, exp_sabotage, 0.0, exp_reve, exp_insecte)


def _score_gardien_pari(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
) -> float:
    """Évalue la cible `('GARDIEN_PARI', case_c)` en 2.2 (strictement sur PlayerObservation)."""
    if not obs.gardien_pari_enabled or not obs.gardien_present_at_case(case_c):
        return 0.0

    own_pari_case = obs.player_def2_gardien_pari_case(obs.observer_seat)
    allies_on_case = max(
        0, obs.gardien_pari_defenders(case_c) - (1 if own_pari_case == case_c else 0)
    )
    if allies_on_case >= GARDIEN_BET_CAP:
        return 0.0

    eveil_trigs = _estimate_expected_gardien_triggers(obs, cfg, belief, for_eveil=True)
    n = obs.n_players
    allies_g = max(0, obs.total_gardien_pari_defenders() - (1 if own_pari_case > 0 else 0))
    unplaced_allies = max(0, (n - 1) - allies_g)

    # Capacité physique totale sur les Gardiens construits et capacité attendue hors case 4 (sous hypothèse d'Éveil)
    total_slots_cap = 0
    total_non_res_cap = 0.0
    distinct_other_cap = 0.0
    distinct_other_bet_exp = 0.0
    has_other_empty_supported = False
    for c_k in (1, 2, 3, 5, 6):
        if obs.gardien_present_at_case(c_k):
            total_slots_cap += GARDIEN_BET_CAP
            t_k = eveil_trigs[c_k - 1]
            cap_k = min(float(GARDIEN_BET_CAP), t_k)
            total_non_res_cap += cap_k
            distinct_other_cap += min(1.0, t_k)
            bets_k = max(
                0, obs.gardien_pari_defenders(c_k) - (1 if own_pari_case == c_k else 0)
            )
            if bets_k >= 1:
                distinct_other_bet_exp += min(1.0, t_k)
            elif c_k != case_c and t_k >= 0.85:
                has_other_empty_supported = True

    has_res = obs.gardien_present_at_case(4)
    if has_res:
        total_slots_cap += GARDIEN_BET_CAP
    res_cap = min(float(GARDIEN_BET_CAP), distinct_other_cap) if has_res else 0.0
    total_gardien_cap = total_non_res_cap + res_cap

    if case_c == 4:
        exp_for_case = min(
            distinct_other_cap, distinct_other_bet_exp + 0.80 * unplaced_allies
        )
    else:
        exp_for_case = eveil_trigs[case_c - 1]

    needed_triggers = allies_on_case + 1

    total_init = max(1, n * sum(CANONICAL_DOTATION))
    cur_arbres = sum(
        obs.parcel_arbres(r, p) for r in range(n) for p in range(1, cfg.p_max + 1)
    )
    tree_ratio = cur_arbres / total_init

    bouclier_safety = 28.0 if obs.piste_colonie[case_c - 1] >= 1 else 0.0

    # Tolérance légèrement plus souple à 5-6J (6 déclencheurs simultanés, boucliers de lisière actifs)
    sup_tol = 0.28 if (is_b2 and n >= 5) else 0.18
    cap_tol = 0.65 if (is_b2 and n >= 5) else 0.40
    supported = exp_for_case >= (float(needed_triggers) - sup_tol)
    marginally_supported = exp_for_case >= (float(needed_triggers) - (sup_tol + 0.25))
    eveil_feasible = (
        obs.tour <= 7
        and total_slots_cap >= n
        and total_gardien_cap >= (n - cap_tol)
    )

    total_rat = sum(
        1
        for m_obj in obs.machines
        if m_obj.status == MACHINE_STATUS_RATISSAGE
    )
    total_red = sum(
        obs.machine_effective_rouges(m_obj.ray, m_obj.m_type)
        for m_obj in obs.machines
        if m_obj.status != MACHINE_STATUS_RETIRED and m_obj.position > 0
    )

    # Calibration B2 à 3J-4J : ne pas forcer l'Éveil quand la survie normale offre une meilleure espérance d'Arbres
    eveil_value_mult = 1.0
    if is_b2 and n <= 4:
        high_pressure = total_rat >= 1 or total_red >= (n + 2) or obs.tour >= 6
        too_early_or_speculative = (not high_pressure) and (
            (obs.tour <= 3 and tree_ratio < 0.88)
            or (tree_ratio < 0.58 and obs.tour <= 5)
            or (allies_g == 0 and exp_for_case < (float(needed_triggers) + 0.05))
        )
        if too_early_or_speculative:
            eveil_feasible = False
        else:
            eveil_value_mult = 0.80 if (not high_pressure and obs.tour <= 5) else 0.96
    elif is_b2 and n >= 5:
        # À 5-6J en v6.0, stopper la partie en Acte 2 (Tours 4..7) évite des vagues d'ASSAUT massives :
        # réaligner l'échelle d'Éveil pour qu'elle puisse surpasser une parade individuelle FORET (~850-950).
        rem_turns = max(0, 8 - obs.tour)
        eveil_value_mult = 1.18 + 0.06 * min(3, rem_turns)

    # 1. Opportunité d'Éveil de la Forêt 100 % Piste des Gardiens (Tours 1..7)
    if eveil_feasible:
        eveil_penalty = 0.0
        if (
            case_c == 4
            and distinct_other_bet_exp < (float(needed_triggers) - 0.15)
            and distinct_other_cap > distinct_other_bet_exp + 0.35
        ):
            eveil_penalty += 45.0
        if allies_on_case >= 1 and has_other_empty_supported:
            eveil_penalty += 38.0

        margin_bonus = 22.0 * max(0.0, min(1.5, exp_for_case - float(needed_triggers)))

        if supported:
            if allies_g >= n - 1:
                base = (820.0 + 260.0 * tree_ratio) if is_b2 else (580.0 + 195.0 * tree_ratio)
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
            if allies_g >= 1:
                prog = allies_g / max(1, n - 1)
                base = (
                    (575.0 + 245.0 * prog + 175.0 * tree_ratio)
                    if is_b2
                    else (420.0 + 130.0 * prog + 135.0 * tree_ratio)
                )
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
            if belief.drew_sabotage_or_none or total_gardien_cap >= (n + 0.05) or obs.tour >= 4:
                base = (495.0 + 185.0 * tree_ratio) if is_b2 else (350.0 + 145.0 * tree_ratio)
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
        elif marginally_supported and allies_g >= max(2, n - 2):
            base = (690.0 + 190.0 * tree_ratio) if is_b2 else (455.0 + 145.0 * tree_ratio)
            return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)

    # 2. Jeu courant : pari prudent en Mode 3/4 uniquement si l'activation est probable
    if obs.mode >= 3:
        cur_trigs = _estimate_expected_gardien_triggers(obs, cfg, belief, for_eveil=False)
        cur_exp = (
            eveil_trigs[3] if case_c == 4 else cur_trigs[case_c - 1]
        )
        if cur_exp >= (float(needed_triggers) + 0.10):
            g_face = obs.gardien_face_at_case(case_c)
            face_bonus = 45.0 if g_face == 1 else 15.0
            return (275.0 if is_b2 else 240.0) + face_bonus + bouclier_safety
        if cur_exp >= (float(needed_triggers) - 0.15):
            return (165.0 if is_b2 else 145.0) + bouclier_safety
        return 25.0

    # En Mode 2 (Gardiens neutres), hors opportunité d'Éveil, éviter tout pari inutile/risqué
    return 20.0


def _is_own_hand_covered(obs: PlayerObservation, cfg: GameConfig) -> bool:
    """Vrai si le joueur n'a aucune frappe non parée issue de sa propre carte sous paravent."""
    own_hand = obs.hand_of(obs.observer_seat)
    if (not own_hand.has_card) or own_hand.card == CARD_SABOTAGE:
        return True
    if own_hand.card is None or not (1 <= own_hand.card <= 2 * obs.n_players):
        return True
    lec = own_hand.lecture_m
    if lec is None or not (1 <= lec <= TRACK_LEN):
        return True
    r_m, mt_m = unpack_machine_card(own_hand.card)
    pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
    if st_m != 0 or pos_m <= 0:  # Retirée ou déjà en Ratissage (géré hors main)
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
            for p_c in range(pos_m + 1, cfg.p_max + 1):
                if not obs.is_route(r_m, p_c):
                    target_ps.append(p_c)
                    break
    for tp in target_ps:
        if obs.parcel_piege(r_m, tp) == PIEGE_ACTIF:
            continue
        tot_d = obs.parcel_defenseurs(r_m, tp) + obs.parcel_insectes(r_m, tp)
        seuil_tp = max(
            1,
            CANONICAL_DOTATION[tp - 1]
            + eff_red
            - bleus
            + spec.mod_seuil,
        )
        can_hurt = is_chg or obs.parcel_arbres(r_m, tp) >= 1 or mt_m == MACHINE_BULLDOZER
        if tot_d < seuil_tp and can_hurt:
            return False
    return True


def _score_reve_activation(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
    is_first_defender: bool = False,
) -> float:
    """Évalue la cible `('REVE_ACTIVATION', case_c)` en 2.1 ou 2.2 (blocage pur v6.1 + allumage 5. Rêve)."""
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
    own_cur_on_case = (1 if (is_first_defender and own_def1_r == case_c) else 0) + (
        1 if (not is_first_defender and own_def2_r == case_c) else 0
    )
    allies = max(0, total_on_case - own_cur_on_case)

    # 1. Neutralisation directe de notre propre carte Machine connue sous paravent (2.1 ou 2.2)
    if own_hits_reve and own_card is not None:
        ray, m_type = unpack_machine_card(own_card)
        pos, st = obs.machine_pos_status(ray, m_type)
        if st != MACHINE_STATUS_NORMAL or pos <= 0:
            # Machine déjà retirée / en Ratissage : ne bloque aucune frappe réelle
            return 45.0

        eff_red = obs.machine_effective_rouges(ray, m_type)
        danger = _tactique_danger(case_c, obs.tour, eff_red)
        if not is_b2:
            base_b1 = 235.0 + danger * 2.2 + (45.0 if m_type == MACHINE_BULLDOZER else 0.0)
            if is_first_defender and ray != own_seat:
                base_b1 += 65.0
            return base_b1 * (0.85 if allies >= 1 else 1.0)

        # B2 : évaluation fine des frappes évitées par 1 seul Défenseur sur la Tactique imprimée T{case_c}
        spec = TACTIQUES_SPEC[case_c]
        is_chg = is_tactique_charge(case_c, obs.tour)
        rouges_for_seuil = 0 if is_chg else eff_red
        bleus = obs.machines[ray * 2 + m_type].bleus
        target_ps: list[int] = []
        for c_kind in spec.cibles:
            if c_kind == "SUR_PLACE" and not obs.is_route(ray, pos):
                target_ps.append(pos)
            elif c_kind == "DEVANT":
                for p_cand in range(pos + 1, cfg.p_max + 1):
                    if not obs.is_route(ray, p_cand):
                        target_ps.append(p_cand)
                        break

        saved_v = 0.0
        would_gain_charge = False
        for tp in target_ps:
            defs_tp = obs.parcel_defenseurs(ray, tp)
            ins_tp = obs.parcel_insectes(ray, tp)
            tot_tp = defs_tp + ins_tp
            seuil_tp = max(
                1,
                CANONICAL_DOTATION[tp - 1]
                + rouges_for_seuil
                - bleus
                + spec.mod_seuil,
            )
            if obs.parcel_piege(ray, tp) == PIEGE_ACTIF:
                saved_v += 45.0  # Épargne le Piège autonome pour une autre machine (ex: Ratissage) !
            elif tot_tp >= seuil_tp:
                manque_d = max(0, seuil_tp - defs_tp)
                saved_v += 25.0 + 55.0 * min(ins_tp, manque_d)
            else:
                arbres = obs.parcel_arbres(ray, tp)
                would_gain_charge = True
                if m_type == MACHINE_ABATTEUSE:
                    trees_lost = arbres
                    saved_v += trees_lost * 270.0 + (85.0 if seuil_tp >= 2 else 25.0)
                else:
                    trees_lost = min(1, arbres)
                    route_pen = 225.0 if arbres <= 1 else 0.0
                    saved_v += trees_lost * 270.0 + route_pen + (85.0 if seuil_tp >= 2 else 30.0)

        if spec.avancee > 0:
            saved_v += 90.0
        if is_chg and would_gain_charge:
            saved_v += 225.0 if obs.tour <= 4 else (105.0 if obs.tour <= 6 else 35.0)
        if obs.gardien_present_at_case(5) and allies == 0:
            saved_v += 75.0  # Allume 5. Rêve au passage !

        # En 2.1, neutraliser sa carte sur un Rêve garde 2.2 100 % flexible (surtout si ray != own_seat !)
        flex_2_1 = (95.0 if ray != own_seat else 45.0) if is_first_defender else 0.0
        ally_mult = 1.0 if allies == 0 else (0.86 if allies == 1 else 0.72)
        return (210.0 + saved_v + flex_2_1) * ally_mult

    # 2. Pose proactive en 2.1 par B2 pour allumer `5. Rêve` lors d'un tour d'Éveil (notamment à 5J-6J)
    #    tout en laissant les `N` 2es Défenseurs libres d'aller sur la Piste des Gardiens en 2.2 !
    if is_b2 and is_first_defender and obs.tour <= 7 and obs.gardien_pari_enabled:
        g5_present = obs.gardien_present_at_case(5)
        g_cnt = sum(1 for c_g in range(1, TRACK_LEN + 1) if obs.gardien_present_at_case(c_g))
        min_g_eveil = (obs.n_players + 1) // 2
        any_reve_armed = any(
            obs.reve_def1_count(c_r) >= 1
            for c_r in range(1, TRACK_LEN + 1)
            if obs.reve_at_case(c_r) > 0
        )
        # Choisir uniquement le Rêve le plus à gauche (probabilité min(2D6) maximale)
        best_reve_case = 0
        for c_r in range(1, TRACK_LEN + 1):
            if obs.reve_at_case(c_r) > 0:
                best_reve_case = c_r
                break

        if (
            g5_present
            and g_cnt >= min_g_eveil
            and not any_reve_armed
            and case_c == best_reve_case
            and (belief.drew_sabotage_or_none or _is_own_hand_covered(obs, cfg))
        ):
            est_active_holders = max(1, obs.n_players - 1 - obs.sabotage_deck_count)
            p_hit_any = 1.0 - ((1.0 - _MIN_2D6_PROBS_H[case_c - 1]) ** est_active_holders)
            min_p_arm = 0.28 if obs.n_players >= 5 else 0.36
            if p_hit_any >= min_p_arm:
                eveil_arm_base = 635.0 if obs.n_players >= 5 else (515.0 if obs.tour >= 4 else 410.0)
                return eveil_arm_base + 140.0 * p_hit_any

    # 3. Couverture spéculative légère en 2.1 sur un Rêve très fréquent (T1/T2) en Acte 2 si joueur couvert
    if (
        is_b2
        and is_first_defender
        and case_c <= 2
        and allies == 0
        and obs.tour >= 5
        and belief.drew_sabotage_or_none
    ):
        p_rk = belief.reve_open_prob_by_rank[case_c - 1]
        if p_rk >= 0.52:
            return 360.0 + 180.0 * p_rk

    return 30.0


def _furtivite_ray_deduction(
    obs: PlayerObservation,
    cfg: GameConfig,
    ray: int,
    *,
    is_first_defender: bool,
) -> tuple[int, int, bool, int, float, float]:
    """Déduction bayésienne muette exacte (`mem_debt = 0.0`) sur l'activité `m(ray)` d'un rayon `ray`.

    Retourne `(rat_cnt, norm_cnt, own_card_is_ray, ally_on_piege, p_m2, p_m0)` :
    - `p_m2` : probabilité que `m(ray) == 2` (condition de gain de `Rive Piège`).
    - `p_m0` : probabilité que `m(ray) == 0` (condition de gain de `Rive Sabotage`).
    """
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

    # Comptage symétrique sans mémoire (mem_debt = 0.0) sur le cycle courant
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

    # 1. Probabilité exacte de double menace m(ray) == 2 (Rive Piège)
    if active_cnt < 2:
        p_m2 = 0.0
    elif rat_cnt == 2:
        p_m2 = 1.0
    elif rat_cnt == 1:
        if own_card_is_ray or ((not is_first_defender) and ally_on_piege >= 1):
            p_m2 = 1.0
        else:
            p_m2 = float(k_opp) / float(c_other)
    else:
        # rat_cnt == 0, norm_cnt == 2
        if own_card_is_ray:
            if ally_on_piege >= 1:
                p_m2 = 1.0
            else:
                p_m2 = float(k_opp) / float(c_other)
        else:
            if ally_def1_piege >= 2:
                p_m2 = 1.0
            elif ally_def1_piege == 1:
                c_rem = max(1, c_other - 1)
                k_rem = max(0, min(c_rem, k_opp - 1))
                p_m2 = float(k_rem) / float(c_rem)
            elif k_opp >= 2 and c_other >= 2:
                p_m2 = (float(k_opp) / float(c_other)) * (float(k_opp - 1) / float(c_other - 1))
            else:
                p_m2 = 0.0

    # 2. Probabilité exacte de piste calme m(ray) == 0 (Rive Sabotage)
    if rat_cnt >= 1 or own_card_is_ray or ally_on_piege >= 1:
        p_m0 = 0.0
    elif norm_cnt == 0:
        p_m0 = 1.0
    else:
        # En 2.2 (où step 3c replie tout 1/2 non rejoint), évaluer p_m0 conditionnellement au binôme (2 non-détenteurs)
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
        # Mise à jour bayésienne publique en 2.2 selon la présence de Défenseurs en forêt sur ray
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


def _best_untrapped_parcel_value_on_ray(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    ray: int,
    res_arbre: float,
    trig_piege_v: float,
) -> float:
    """Estime la valeur du meilleur Piège autonome posable en 4.1 sur le rayon `ray`."""
    best_v = 0.0
    for p_c in range(1, cfg.p_max + 1):
        if obs.is_route(ray, p_c) or obs.parcel_piege(ray, p_c) != PIEGE_AUCUN:
            continue
        idx = ray * MAX_P + (p_c - 1)
        arbres = obs.parcel_arbres(ray, p_c)
        souches = obs.parcel_souches(ray, p_c)
        seuil_e = belief.parcel_expected_seuil[idx]
        s_prob = belief.parcel_strike_prob[idx]
        # Quand Rive Piège gagne (m(ray) == 2), les 2 machines du rayon sont actives ce tour !
        has_m_here_or_up = False
        max_red = 0
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            mp, ms = obs.machine_pos_status(ray, mt)
            if ms != MACHINE_STATUS_RETIRED and 0 < mp <= p_c:
                has_m_here_or_up = True
                max_red = max(max_red, obs.machine_effective_rouges(ray, mt))
        if not has_m_here_or_up and arbres == 0 and souches == 0:
            v_p = 45.0
        else:
            tree_v = arbres * res_arbre * (1.35 if has_m_here_or_up else 0.65)
            seuil_saving = max(0.0, seuil_e - 1.5) * 48.0 + max_red * 28.0
            nid_prot = 75.0 if obs.parcel_has_nid(ray, p_c) else 0.0
            route_prot = 135.0 if (arbres <= 1 and has_m_here_or_up) else 0.0
            v_p = (
                85.0
                + tree_v
                + seuil_saving
                + nid_prot
                + route_prot
                + 0.65 * trig_piege_v
                + 25.0 * min(1.5, s_prob)
            )
        best_v = max(best_v, v_p)
    return best_v


# ---------------------------------------------------------------------------
# Fonctions de score de cibles Défenseurs pour B1 (k=1) et B2 (k=2)
# ---------------------------------------------------------------------------


def score_target_b1(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    is_first_defender: bool,
) -> float:
    """Évaluation tactique 1-coup de B1 (+ oubli stochastique si > 2 lois actives)."""
    active_laws = count_active_laws_from_obs(obs, cfg)
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
        # Activer un Nid en forêt
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            score += 470.0
        # Parer une frappe attendue non couverte par un Piège autonome
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

        score += _b1_forgetting_penalty(obs, cfg, active_laws, 100 + idx)
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
            base_l = 610.0 + fam_bonus
        elif belief.drew_sabotage_or_none and obs.tour <= 7:
            base_l = 525.0 + fam_bonus
        else:
            base_l = 255.0 + fam_bonus
        return base_l + _b1_forgetting_penalty(obs, cfg, active_laws, 300 + s_idx)

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
                # Complétion prioritaire d'une rive amorcée lorsque m(r) == 2 est certain
                base_f = 685.0 + 0.25 * trap_v
            elif (
                is_first_defender
                and p_m2 >= 0.99
                and other_open_rives == 0
                and other_completed_rives == 0
                and (own_card_is_ray or r_i == obs.observer_seat)
            ):
                # Amorce 2.1 uniquement sur certitude privée/publique forte (rat_cnt==2 ou 1 Ratissage + carte en main)
                base_f = 415.0 + 0.16 * trap_v
            elif (
                (not is_first_defender)
                and (not partner_ready)
                and other_open_rives == 0
                and other_completed_rives == 0
                and (
                    (rat_cnt == 2 and belief.drew_sabotage_or_none)
                    or (own_card_is_ray and p_m2 >= 0.38 and trap_v >= 280.0)
                )
            ):
                # Ouverture réversible en 2.2 (filet anti-orphelin 3c si non rejoint)
                base_f = 345.0 + 0.18 * trap_v
            else:
                base_f = 30.0
        else:
            sab_cnt_b1 = obs.sabotage_deck_count + obs.sabotage_pending_count
            ray_undef_b1 = sum(obs.parcel_def1_count(r_i, p) for p in range(1, cfg.p_max + 1)) == 0
            if obs.tour >= 8 or p_m0 < 0.24 or sab_cnt_b1 >= 3:
                base_f = 30.0
            elif partner_ready and p_m0 >= 0.30 and other_completed_rives == 0:
                base_f = (545.0 if obs.tour <= 4 else 470.0) + 115.0 * p_m0
            elif (
                (not is_first_defender)
                and other_open_rives == 0
                and other_completed_rives == 0
                and belief.drew_sabotage_or_none
                and obs.tour <= 5
                and p_m0 >= 0.28
            ):
                base_f = (420.0 if sab_cnt_b1 <= 1 else 360.0) + 90.0 * p_m0
            elif (
                (not is_first_defender)
                and other_open_rives == 0
                and other_completed_rives == 0
                and sab_cnt_b1 <= 1
                and obs.tour <= 4
                and p_m0 >= 0.32
                and (ray_undef_b1 or _is_own_hand_covered(obs, cfg))
            ):
                base_f = 385.0 + 85.0 * p_m0 + (30.0 if ray_undef_b1 else 0.0)
            else:
                base_f = 35.0
        return base_f + _b1_forgetting_penalty(obs, cfg, active_laws, 500 + r_i * 4 + rv)

    if kind == "GARDIEN_PARI":
        _, case_c = target
        c_i = int(case_c)
        return _score_gardien_pari(obs, cfg, belief, c_i, is_b2=False) + _b1_forgetting_penalty(
            obs, cfg, active_laws, 700 + c_i
        )

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        c_i = int(case_c)
        return _score_reve_activation(
            obs, cfg, belief, c_i, is_b2=False, is_first_defender=is_first_defender
        ) + _b1_forgetting_penalty(obs, cfg, active_laws, 800 + c_i)

    return 0.0


def _score_target_b2_core(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    *,
    is_held: bool = False,
    is_first_defender: bool = False,
) -> float:
    """Noyau d'évaluation B2 (`k=2`, graphe `economie_bot` + économie v6.1 Acte 1 CHARGE / Acte 2 ASSAUT).

    Si `is_held=True`, soustrait 1 Défenseur virtuel sur `target` pour mesurer la vraie valeur marginale
    du maintien du 2e Défenseur déjà posé dessus (symétrie exacte avec `exclude_own_def2=True`).
    """
    res_val, trig_vals = _compute_b2_resource_and_trigger_values(obs, cfg, belief)
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        r_i, p_i = int(r), int(p)
        idx = r_i * MAX_P + (p_i - 1)
        raw_defs = obs.parcel_defenseurs(r_i, p_i)
        defs = max(0, raw_defs - 1) if is_held else raw_defs
        ins = obs.parcel_insectes(r_i, p_i)
        cur_def = defs + ins
        raw_s_prob = belief.parcel_strike_prob[idx]
        has_auto_piege = obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF
        if has_auto_piege:
            # Piège autonome v6.1 (SINGLE_STRIKE figé) : couvre la 1re frappe puis est défaussé
            s_prob = max(0.0, raw_s_prob - 0.95)
        else:
            s_prob = raw_s_prob
        c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
        seuil_e = belief.parcel_expected_seuil[idx]
        arbres = obs.parcel_arbres(r_i, p_i)
        souches = obs.parcel_souches(r_i, p_i)

        score = 90.0 if not has_auto_piege else 55.0
        trig_1_v = trig_vals[0]  # 1. Parade (Défenseurs seuls)
        trig_6_v = trig_vals[5]  # 6. Insecte (Parade avec dépense d'Insecte uniquement en 5.1)

        # Charge denial : sous FRAPPE_NON_PAREE (gelé v6.1), toute frappe non parée sur parcelle non-Route gagne +1 Puissance !
        if obs.tour <= 2:
            charge_unit_v = 250.0
        elif obs.tour <= 4:
            charge_unit_v = 220.0
        elif obs.tour <= 6:
            charge_unit_v = 105.0
        elif obs.tour == 7:
            charge_unit_v = 35.0
        else:
            charge_unit_v = 0.0
        charge_denial = min(1.40, c_prob) * charge_unit_v if c_prob > 0.05 else 0.0

        # 1. Activation d'un Nid en 4.2 : produit +1/+2 Insectes + pouvoir du Nid (n'allume jamais 6. Insecte)
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            prod_cnt = 1 if ins <= 1 else 2
            score += 375.0 + prod_cnt * res_val["RES_INSECTE"] + (35.0 if is_held else 0.0)

        # 2. Lookahead 5.1 -> 6.2 : valorisation directe des Arbres debout (0 Repousse Finale) + Charge denial
        if s_prob > 0.05:
            if cur_def < seuil_e:
                gap = seuil_e - cur_def
                parade_trig_v = trig_1_v if (defs + 1 >= seuil_e) else trig_6_v
                expected_trees_saved = float(arbres)
                route_catastrophe = (
                    210.0
                    if (arbres <= 1 and (belief.parcel_bulldo_prob[idx] > 0.10 or souches == 0))
                    else 0.0
                )
                own_ray_b = 35.0 if r_i == obs.observer_seat else 0.0
                full_parade_v = (
                    min(1.55, s_prob)
                    * (
                        expected_trees_saved * res_val["RES_ARBRE"] * 2.65
                        + route_catastrophe
                        + 0.8 * parade_trig_v
                    )
                    + charge_denial
                )
                if gap <= 1.25:
                    # 1 Défenseur boucle immédiatement la parade !
                    cheap_act1_b = 55.0 if (obs.tour <= 4 and c_prob > 0.12) else 0.0
                    score += full_parade_v + cheap_act1_b + own_ray_b + (45.0 if is_held else 0.0)
                elif gap <= 2.25:
                    if is_held:
                        score += (0.48 if s_prob >= 0.85 else 0.34) * full_parade_v + own_ray_b
                    elif s_prob >= 0.85:
                        cheap_act1_b = 65.0 if (obs.tour <= 4 and c_prob > 0.12) else 0.0
                        score += 0.62 * full_parade_v + cheap_act1_b + own_ray_b
                    else:
                        score += 0.40 * full_parade_v + own_ray_b
                elif gap <= 3.25 and arbres >= 1 and not is_held:
                    score += (0.28 if s_prob >= 0.85 else 0.18) * full_parade_v
            elif cur_def >= seuil_e and ins > 0 and defs < seuil_e:
                # Épargner 1 Insecte qui aurait été défaussé par la parade classique !
                score += s_prob * (0.85 * res_val["RES_INSECTE"])

        if (
            s_prob > 0.05
            and arbres == 0
            and souches >= 1
            and belief.parcel_bulldo_prob[idx] > 0.15
            and cur_def < seuil_e
        ):
            score += belief.parcel_bulldo_prob[idx] * 65.0 + 0.45 * charge_denial

        return score

    if kind == "LISIERE":
        _, slot_idx = target
        s_idx = int(slot_idx)
        if obs.mode < 2 or s_idx >= 2 * obs.n_players:
            return 0.0
        tile_id, st_l, raw_constructors = obs.lisiere_tile_info(s_idx)
        if st_l != LISIERE_UNCONSTRUCTED:
            return 0.0
        constructors = max(0, raw_constructors - 1) if is_held else raw_constructors

        tile_v = _score_tile_construction_b2(obs, cfg, tile_id, res_val, trig_vals)
        lib_bonus = 0.45 * res_val["RES_DEFENSEUR"] if obs.n_players == 3 else 0.0
        if constructors == 1:
            return 515.0 + tile_v * 1.32 + lib_bonus + (55.0 if is_held else 0.0)
        if is_held:
            # Resté seul (1/2) en révision 2.2 sans partenaire -> se replier si mieux ailleurs !
            return 140.0 + tile_v * 0.55
        if tile_v >= 120.0 and (belief.drew_sabotage_or_none or _is_own_hand_covered(obs, cfg)):
            return 375.0 + tile_v * 1.22 + lib_bonus
        if belief.drew_sabotage_or_none and tile_v >= 80.0:
            return 320.0 + tile_v * 1.05 + lib_bonus
        return 195.0 + tile_v * 0.90 + lib_bonus

    if kind == "FURTIVITE":
        _, ray, rive = target
        r_i, rv = int(ray), int(rive)
        if not obs.is_ray_furtivite_open(r_i):
            return 0.0
        raw_d_rv = obs.furtivite_ray_rive_defs(r_i, rv)
        d_rv = max(0, raw_d_rv - 1) if is_held else raw_d_rv
        if d_rv >= 2:
            return 0.0
        d_other = obs.furtivite_ray_rive_defs(r_i, 1 - rv)
        partner_ready = d_rv == 1

        # Comptage public des autres rives de Furtivité déjà engagées sur le plateau ce tour
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

        # Rive Piège (pari « double menace » m(r) == 2 -> 1 Piège autonome posé par le propriétaire du rayon r)
        if rv == FURT_RIVE_PIEGE:
            trap_v = _best_untrapped_parcel_value_on_ray(
                obs, cfg, belief, r_i, res_val["RES_ARBRE"], trig_vals[1]
            )
            if trap_v <= 20.0:
                return 25.0

            # Cas 1 : Pari CERTAIN à 100 % (p_m2 >= 0.99)
            if p_m2 >= 0.99:
                if partner_ready:
                    # Priorité absolue en 2.2 (ou complétion directe en 2.1) : 1 seul Défenseur restant gagne un Piège autonome !
                    return 595.0 + 0.52 * trap_v + (65.0 if is_held else 0.0)
                if is_first_defender:
                    # Amorcer en 2.1 quand m(r) == 2 est déjà certain (ex: 1 Ratissage + notre carte, ou 2 Ratissages)
                    return 485.0 + 0.42 * trap_v
                # En 2.2 à 0/2 quand rat_cnt == 2 : ouvrir l'invitation si joueur disponible (3c replie si non rejoint)
                if rat_cnt == 2 and other_open_rives == 0 and (
                    belief.drew_sabotage_or_none or _is_own_hand_covered(obs, cfg)
                ):
                    return 375.0 + 0.35 * trap_v + (-15.0 if is_held else 0.0)
                return 45.0

            # Cas 2 : Signal muet en 2.2 (réversible via 3c si aucun allié ne détient la 2e carte de r_i !)
            # En 2.1 (irréversible), ne jamais risquer un pion orphelin à 40-45 % quand rat_cnt == 0.
            if (
                (not is_first_defender)
                and (not partner_ready)
                and own_card_is_ray
                and p_m2 >= 0.38
                and other_open_rives == 0
                and other_completed_rives == 0
                and trap_v >= 280.0
            ):
                held_adj = -12.0 if is_held else 0.0
                return 315.0 + p_m2 * (0.46 * trap_v) + held_adj

            return 30.0

        # Rive Sabotage (pari « piste calme » m(r) == 0 -> +1 carte Sabotage au remélange 6.3)
        sab_cnt = obs.sabotage_deck_count + obs.sabotage_pending_count
        if obs.tour >= 8 or p_m0 < 0.24 or sab_cnt >= 3:
            return 25.0

        ray_undef_2_1 = sum(obs.parcel_def1_count(r_i, p) for p in range(1, cfg.p_max + 1)) == 0
        total_norm_deck = sum(
            1
            for m_obj in obs.machines
            if m_obj.status == MACHINE_STATUS_NORMAL and m_obj.position > 0
        )
        next_deck_size = max(float(obs.n_players), float(total_norm_deck + sab_cnt + 1))
        p_next_draw = min(1.0, float(obs.n_players) / next_deck_size)
        sab_stock_mult = 1.50 if sab_cnt == 0 else (0.95 if sab_cnt == 1 else 0.50)
        prep_trig3 = 0.0
        if obs.gardien_present_at_case(3):
            prep_trig3 += 0.85 * trig_vals[2] + (75.0 if sab_cnt == 0 else 30.0)
        elif obs.gardien_pari_enabled and sab_cnt == 0 and obs.tour <= 5:
            prep_trig3 += 75.0

        dilution_factor = 0.72 + 0.82 * p_next_draw
        gross_sab = res_val["RES_DILUTION_SABOTAGE"] * sab_stock_mult * dilution_factor + prep_trig3
        waste_risk_pen = (1.0 - p_m0) * (64.0 if (sab_cnt == 0 and obs.tour <= 4) else 76.0)
        action_v = max(0.0, p_m0 * gross_sab - waste_risk_pen)
        if action_v <= 8.0:
            return 40.0

        scarcity_pen = 0.0
        if other_completed_rives >= 1:
            scarcity_pen += 220.0 if obs.n_players <= 4 else 145.0
        if d_other >= 1:
            scarcity_pen += 180.0
        if not partner_ready and other_open_rives >= 1:
            scarcity_pen += 140.0
        if not ray_undef_2_1 and not is_first_defender:
            scarcity_pen += 55.0

        if partner_ready:
            return max(55.0, 465.0 + action_v * 1.35 - scarcity_pen + (45.0 if is_held else 0.0))

        # Préférer ouvrir Rive Sabotage en 2.2 (où 3c replie tout pion 1/2 non rejoint !) sur un rayon calme non défendu en 2.1
        held_solo_adj = -12.0 if is_held else 0.0
        if not is_first_defender:
            if belief.drew_sabotage_or_none and p_m0 >= 0.28:
                return max(55.0, 365.0 + action_v * 1.22 - scarcity_pen + held_solo_adj)
            if (
                (_is_own_hand_covered(obs, cfg) or (ray_undef_2_1 and sab_cnt == 0 and obs.tour <= 3))
                and p_m0 >= 0.30
                and (obs.tour <= 4 or sab_cnt == 0)
            ):
                return max(55.0, 345.0 + action_v * 1.18 - scarcity_pen + held_solo_adj)
        elif (
            obs.n_players >= 4
            and sab_cnt == 0
            and obs.tour <= 3
            and belief.drew_sabotage_or_none
            and p_m0 >= 0.34
        ):
            return max(55.0, 270.0 + action_v * 0.95 - scarcity_pen)

        return max(40.0, 95.0 + action_v * 0.30 - scarcity_pen + held_solo_adj)

    if kind == "GARDIEN_PARI":
        _, case_c = target
        base_gp = _score_gardien_pari(obs, cfg, belief, int(case_c), is_b2=True)
        if is_held:
            tot_on_track = obs.total_gardien_pari_defenders()
            if obs.tour <= 7 and tot_on_track >= obs.n_players:
                return base_gp + 420.0
            if obs.tour <= 7 and tot_on_track >= 2:
                return base_gp + 45.0
            return base_gp - 90.0
        return base_gp

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        base_rv = _score_reve_activation(
            obs, cfg, belief, int(case_c), is_b2=True, is_first_defender=is_first_defender
        )
        if is_held:
            c_i = int(case_c)
            own_hand = obs.hand_of(obs.observer_seat)
            own_hits = (
                own_hand.card is not None
                and 1 <= own_hand.card <= 2 * obs.n_players
                and own_hand.lecture_m == c_i
                and obs.player_def1_reve_case(obs.observer_seat) != c_i
            )
            return base_rv + (55.0 if own_hits else -35.0)
        return base_rv

    return 0.0


class _B2TargetScorer:
    """Évaluateur B2 (`k=2`) : graphe `economie_bot` (12 `RES_*`, `TRIG_1..6`) + lookahead v6.0."""

    retreat_orphans: bool = True

    def __call__(
        self,
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        target: tuple[Any, ...],
        is_first_defender: bool,
    ) -> float:
        return _score_target_b2_core(
            obs, cfg, belief, target, is_held=False, is_first_defender=is_first_defender
        )

    @staticmethod
    def held_score(
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        cur_spot: tuple[Any, ...],
    ) -> float:
        return _score_target_b2_core(obs, cfg, belief, cur_spot, is_held=True, is_first_defender=False)


score_target_b2 = _B2TargetScorer()


# ---------------------------------------------------------------------------
# Politique complète hors Étape 2 (Étapes 3, 4, 5, 6 et Effets de tuiles)
# ---------------------------------------------------------------------------


_MACHINE_PAIR_EFFECT_KINDS: frozenset[str] = frozenset(
    {
        "MACHINE_SURCHAUFFE",
        "MACHINE_RECUL",
        "PIERRE_SERPENT_SURCHAUFFE",
        "MACHINE_RECUL_EM",
        "SCALING_INSECTES_SEUIL",
        "M2_SURCHAUFFE_VOISINE",
    }
)

_PARCEL_PAIR_EFFECT_KINDS: frozenset[str] = frozenset(
    {
        "MOD_SEUIL_PARCELLE",
        "PIEGE_SOUCHE",
        "HARPIE_MOD_SEUIL_F1",
        "HARPIE_AUTO_PARADE_F2",
        "POSE_INSECTE_HI",
        "PIEGE_ER_3_2",
        "M1_DEPLACER_DEFENSEUR",
    }
)


def _score_effect_option(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    decision: DecisionRequest,
    opt: Any,
    *,
    is_b2: bool,
) -> float:
    """Évalue une option de `DEC_EFFET_TUILE` (catalogue actif 30 tuiles Mode 4 + Bug B) sur `PlayerObservation`.

    Le dispatch est strictement gouverné par `effect_kind` afin d'éviter toute collision
    entre tuples d'entiers de sémantiques distinctes (ex. `(seat, +1)` de `SHIFT_LECTURE_M`
    vs `(ray, p)` d'une parcelle ou `(ray, m_type)` d'une machine).
    """
    slot_id = str(decision.context.get("slot_id", ""))
    kind_hint = str(decision.context.get("effect_kind", ""))

    if opt == "PASSER":
        # Pour un sacrifice (ex: G4:A), ne sacrifier que si le gain dépasse nettement la valeur de G4 en piste !
        if "SACRIFICE" in kind_hint or slot_id == "G4":
            g_cnt = sum(1 for g in obs.piste_gardiens if g.gardien_num > 0)
            sole_g = obs.gardien_pari_enabled and g_cnt == 1
            return 380.0 if sole_g else 240.0
        return 25.0

    # 1. Décalage lecture dé M `(seat, delta_m)` (G6:A) — dispatch explicite AVANT tout barème parcelle
    if (
        kind_hint == "SHIFT_LECTURE_M"
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
    ):
        s_id, d_m = int(opt[0]), int(opt[1])
        h = obs.hand_of(s_id)
        if h.lecture_m is None or h.card is None or not (1 <= h.card <= 2 * obs.n_players):
            return 40.0
        old_m = h.lecture_m
        new_m = max(1, min(6, old_m + d_m))
        if new_m == old_m:
            return 5.0
        old_code, _ = obs.tactique_code_bugs(old_m - 1)
        new_code, _ = obs.tactique_code_bugs(new_m - 1)
        # Décaler une carte Machine sur un Rêve l'annule ET ouvre le Rêve : jackpot !
        if is_reve_code(new_code) and not is_reve_code(old_code):
            return 750.0
        if is_reve_code(old_code) and not is_reve_code(new_code):
            return -200.0
        if is_tactique_code(old_code) and is_tactique_code(new_code):
            r_m, mt_m = unpack_machine_card(h.card)
            eff_r = obs.machine_effective_rouges(r_m, mt_m)
            return 150.0 + (_tactique_danger(old_code, obs.tour, eff_r) - _tactique_danger(new_code, obs.tour, eff_r)) * 4.0
        return 80.0

    # 2. Machine `(ray, m_type)` (G1:A, G2:A, R4:A, R7:A, R10:A, M2:A)
    if (
        kind_hint in _MACHINE_PAIR_EFFECT_KINDS
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
    ):
        rm, mt = int(opt[0]), int(opt[1])
        m_obs = obs.machines[rm * 2 + mt]
        sc = 150.0 + m_obs.position * 45.0 + (m_obs.rouges + m_obs.bleus) * 45.0
        if mt == MACHINE_BULLDOZER:
            sc += 30.0
        if (
            is_b2
            and kind_hint
            in ("MACHINE_SURCHAUFFE", "PIERRE_SERPENT_SURCHAUFFE", "M2_SURCHAUFFE_VOISINE")
            and obs.tour <= 6
        ):
            sc += 40.0
        return sc

    # 3. Parcelle `(ray, p)` — restreint aux effect_kinds parcellaires (ou hint vide défensif)
    if (
        (kind_hint in _PARCEL_PAIR_EFFECT_KINDS or kind_hint == "")
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and 0 <= opt[0] < obs.n_players
        and 1 <= opt[1] <= cfg.p_max
    ):
        r_p, p_p = int(opt[0]), int(opt[1])
        idx = r_p * MAX_P + (p_p - 1)
        s_prob = belief.parcel_strike_prob[idx]
        defs = obs.parcel_defenseurs(r_p, p_p) + obs.parcel_insectes(r_p, p_p)
        sc = 120.0 + s_prob * 300.0 + p_p * 15.0
        if kind_hint in ("PIEGE_SOUCHE", "PIEGE_ER_3_2") and defs >= 1:
            sc += 220.0
        elif kind_hint == "MOD_SEUIL_PARCELLE" and 0 < defs < belief.parcel_expected_seuil[idx]:
            sc += 200.0
        elif kind_hint in ("HARPIE_MOD_SEUIL_F1", "HARPIE_AUTO_PARADE_F2") and (
            obs.parcel_defenseurs(r_p, p_p) >= 2
        ):
            sc += 240.0
        return sc

    # 4. Déplacement d'un Défenseur `(src_spec, (dst_r, dst_p))` (G3:A, G4:A, R3:A, M3:A)
    if isinstance(opt, tuple) and len(opt) == 2 and isinstance(opt[1], tuple) and len(opt[1]) == 2:
        src_spec, (dst_r, dst_p) = opt
        dr, dp = int(dst_r), int(dst_p)
        dst_idx = dr * MAX_P + (dp - 1)
        dst_gain = score_target_b2(obs, cfg, belief, ("FORET", dr, dp), False)
        src_loss = 80.0
        if isinstance(src_spec, tuple):
            if len(src_spec) >= 3 and src_spec[0] == "FORET":
                sr, sp = int(src_spec[1]), int(src_spec[2])
                src_idx = sr * MAX_P + (sp - 1)
                src_loss = 120.0 + belief.parcel_strike_prob[src_idx] * 320.0
            elif len(src_spec) == 2 and isinstance(src_spec[0], int) and isinstance(src_spec[1], int):
                sr, sp = int(src_spec[0]), int(src_spec[1])
                if 0 <= sr < obs.n_players and 1 <= sp <= cfg.p_max:
                    src_idx = sr * MAX_P + (sp - 1)
                    src_loss = 120.0 + belief.parcel_strike_prob[src_idx] * 320.0
        return dst_gain - src_loss + belief.parcel_strike_prob[dst_idx] * 90.0

    # 5. Sillage du Boto `(ray, m_type, delta_dir)` (G8:A)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint == "CIBLAGE_BOTO_G8A"
    ):
        r_b, mt_b, d_dir = opt
        m_obs = obs.machines[r_b * 2 + mt_b]
        p_pos = m_obs.position
        idx_pos = r_b * MAX_P + max(0, p_pos - 1)
        active_w = belief.parcel_strike_prob[idx_pos]
        # Décaler vers la bordure (-1) en bordure p=1 fait souvent tomber SUR_PLACE dans le vide !
        void_bonus = 180.0 if (d_dir == -1 and p_pos == 1) else (45.0 if d_dir == -1 else 0.0)
        return 140.0 + active_w * 320.0 + void_bonus + (25.0 if mt_b == MACHINE_BULLDOZER else 0.0)

    # 6. Avancement d'un Rêve `r_idx` vers la gauche (G12:A) : privilégier le Rêve le plus proche du Rang 1
    if isinstance(opt, int) and kind_hint == "ADVANCE_REVE_G12A":
        return 750.0 if opt == 1 else (380.0 - opt * 40.0)

    # 7. Pose d'Insecte La Brèche du Tamanoir `("FORET" | "FURTIVITE", idx_a, p)` (G13:A)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], str)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint == "BRECHE_TAMANOIR_INSECTE"
    ):
        loc_g13, idx_a, p_g13 = opt[0], opt[1], opt[2]
        if loc_g13 == "FURTIVITE":
            nb_d, f_ins = obs.furtivite_defs_and_ins(idx_a, p_g13)
            return 360.0 if (nb_d == 1 and f_ins == 0) else 150.0
        idx_f = idx_a * MAX_P + (p_g13 - 1)
        return 190.0 + belief.parcel_strike_prob[idx_f] * 260.0

    # 8. Écaille du Téju `(r, src_p, dst_p)` (G14:A)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint == "ECAILLE_TEJU_CONVERSION_PIEGE"
    ):
        r_t, src_p, dst_p = int(opt[0]), int(opt[1]), int(opt[2])
        dst_idx = r_t * MAX_P + (dst_p - 1)
        src_defs = obs.parcel_defenseurs(r_t, src_p) + obs.parcel_insectes(r_t, src_p)
        dst_defs = obs.parcel_defenseurs(r_t, dst_p) + obs.parcel_insectes(r_t, dst_p)
        rem_on_dst = (dst_defs - 1) if src_p == dst_p else dst_defs
        arm_bonus = 240.0 if rem_on_dst >= 1 else -90.0
        return (
            180.0
            + arm_bonus
            + belief.parcel_strike_prob[dst_idx] * 280.0
            - (140.0 if src_defs == 1 and obs.parcel_piege(r_t, src_p) == PIEGE_ACTIF else 0.0)
        )

    # 9. Envol du Batará Suiveur `(loc, idx_a, p, track, case_1_6)` (G15:A)
    if (
        isinstance(opt, tuple)
        and len(opt) == 5
        and isinstance(opt[0], str)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and isinstance(opt[3], str)
        and isinstance(opt[4], int)
        and kind_hint == "BATARA_MIGRATION_DIRECTE"
    ):
        loc_b, idx_b, p_b, trk_b, c_b = opt[0], opt[1], opt[2], opt[3], opt[4]
        src_pen = 0.0
        if loc_b == "FORET":
            src_pen = belief.parcel_strike_prob[idx_b * MAX_P + (p_b - 1)] * 130.0
        if trk_b == "COLONIE":
            has_g = obs.gardien_available_at_case(c_b)
            return 240.0 + (130.0 if has_g else 20.0) - src_pen
        t_code, bugs_c = obs.tactique_code_bugs(c_b - 1)
        is_t = 1 <= t_code <= 6
        return 210.0 + (95.0 if is_t and bugs_c == 0 else 20.0) - src_pen

    # 10. Déviation Synaptique `"M_MOINS_1" | "M_PLUS_1"` en 3.2 (SLOT_BUG_CERVEAU:B scellé v6.1)
    # Partition stricte 3.2 : dévier allume 6. Insecte (et empêche cette carte d'allumer 5. Rêve).
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
        if h_tgt.card is not None and 1 <= h_tgt.card <= 2 * obs.n_players:
            rt, mtt = unpack_machine_card(h_tgt.card)
            eff_r = obs.machine_effective_rouges(rt, mtt)
        bet6_bonus = 260.0 if (is_b2 and obs.gardien_pari_defenders(6) >= 1) else 0.0
        bet5_pen = -320.0 if (is_b2 and is_reve_code(old_c) and obs.gardien_pari_defenders(5) >= 1) else 0.0
        if is_reve_code(new_c) and not is_reve_code(old_c):
            has_def_new = obs.reve_activation_defenders(new_m) >= 1
            return (760.0 if has_def_new else 95.0) + bet6_bonus
        if is_reve_code(old_c) and not is_reve_code(new_c):
            return -200.0 + bet5_pen
        d_old = _tactique_danger(old_m, obs.tour, eff_r)
        d_new = _tactique_danger(new_m, obs.tour, eff_r)
        return 35.0 + (d_old - d_new) * 4.0 + bet6_bonus

    # 11. Réduction de Seuil -2 sur tout un rayon `ray` (R9:A)
    if isinstance(opt, int) and kind_hint == "MOD_SEUIL_RAYON_MOINS_2":
        ray_threat = sum(
            belief.parcel_strike_prob[opt * MAX_P + (p_r - 1)]
            * (1.0 + 0.35 * (obs.parcel_defenseurs(opt, p_r) + obs.parcel_insectes(opt, p_r)))
            for p_r in range(1, cfg.p_max + 1)
        )
        m_threat = 0.0
        for m_obj in obs.machines:
            if m_obj.ray == opt and m_obj.status != MACHINE_STATUS_RETIRED and m_obj.position > 0:
                m_threat += 15.0 + 18.0 * m_obj.rouges + (45.0 if m_obj.status == MACHINE_STATUS_RATISSAGE else 0.0)
        return 120.0 + ray_threat * 240.0 + m_threat

    # 12. Choix d'une case Gardien 1..6 à ouvrir (R5:A) — explicitement gardé par effect_kind
    if isinstance(opt, int) and kind_hint in ("OPEN_GARDIEN", "") and 1 <= opt <= 6:
        if is_b2:
            _, trig_vals = _compute_b2_resource_and_trigger_values(obs, cfg, belief)
            return 200.0 + trig_vals[opt - 1] * 2.0
        return 200.0 + (7 - opt) * 15.0

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
) -> Any:
    opts = decision.options
    assert len(opts) >= 1
    if len(opts) == 1:
        return opts[0]

    dtype = decision.decision_type

    if dtype == DEC_POSE_PIEGE_FURTIVITE_4_1:
        return _choose_pose_piege_4_1_policy(obs, cfg, decision, is_b2=is_b2)

    scorer = score_target_b2 if is_b2 else score_target_b1
    belief = build_belief_summary(obs, cfg)

    if dtype == DEC_POSE_DEFENSEUR_1:
        best_opt = opts[0]
        best_sc = scorer(obs, cfg, belief, opts[0], True)
        best_tb = -1
        best_i = 0
        for i in range(1, len(opts)):
            sc = scorer(obs, cfg, belief, opts[i], True)
            if sc > best_sc + 1e-9:
                best_sc, best_opt, best_i, best_tb = sc, opts[i], i, -1
            elif abs(sc - best_sc) <= 1e-9:
                if best_tb < 0:
                    best_tb = _tiebreak(cfg, obs, best_i, 1)
                tb = _tiebreak(cfg, obs, i, 1)
                if tb > best_tb:
                    best_tb, best_opt, best_i = tb, opts[i], i
        return best_opt

    if dtype == DEC_POSE_DEFENSEUR_2:
        prefer_kind = "POSER_REFLEXION" if cfg.max_revision_passes > 0 else "POSER_DEFINITIF"
        filtered = [(i, o) for i, o in enumerate(opts) if o[0] == prefer_kind]
        if not filtered:
            filtered = list(enumerate(opts))
        best_i, best_opt = filtered[0]
        best_sc = scorer(obs, cfg, belief, best_opt[1], False)
        best_tb = -1
        for i, opt in filtered[1:]:
            sc = scorer(obs, cfg, belief, opt[1], False)
            if sc > best_sc + 1e-9:
                best_sc, best_opt, best_i, best_tb = sc, opt, i, -1
            elif abs(sc - best_sc) <= 1e-9:
                if best_tb < 0:
                    best_tb = _tiebreak(cfg, obs, best_i, 2)
                tb = _tiebreak(cfg, obs, i, 2)
                if tb > best_tb:
                    best_tb, best_opt, best_i = tb, opt, i
        return best_opt

    if dtype == DEC_REVISION_DEFENSEUR_2:
        pass_idx = int(decision.context.get("pass", 1))
        eps = (24.0 if is_b2 else 32.0) + (pass_idx - 1) * 12.0
        move_opts = [(i, o) for i, o in enumerate(opts) if o[0] == "DEPLACER_REFLEXION"]
        if not move_opts:
            for o in opts:
                if o[0] == "GARDER_REFLEXION":
                    return o
            return opts[0]
        best_i, best_mv = move_opts[0]
        best_sc = scorer(obs, cfg, belief, best_mv[1], False)
        for i, mv in move_opts[1:]:
            sc = scorer(obs, cfg, belief, mv[1], False)
            if sc > best_sc:
                best_sc, best_mv, best_i = sc, mv, i
        _ = best_i
        if best_sc > 520.0 + eps:
            return best_mv
        for o in opts:
            if o[0] == "GARDER_REFLEXION":
                return o
        return opts[0]

    if dtype == DEC_EFFET_TUILE:
        best_e = opts[0]
        best_sc = _score_effect_option(obs, cfg, belief, decision, opts[0], is_b2=is_b2)
        best_tb = -1
        best_i = 0
        for i in range(1, len(opts)):
            sc = _score_effect_option(obs, cfg, belief, decision, opts[i], is_b2=is_b2)
            if sc > best_sc + 1e-9:
                best_sc, best_e, best_i, best_tb = sc, opts[i], i, -1
            elif abs(sc - best_sc) <= 1e-9:
                if best_tb < 0:
                    best_tb = _tiebreak(cfg, obs, best_i, 7)
                tb = _tiebreak(cfg, obs, i, 7)
                if tb > best_tb:
                    best_tb, best_e, best_i = tb, opts[i], i
        return best_e

    if dtype == DEC_ORDRE_CONSTRUCTION_3_1:
        res_val, trig_vals = (
            _compute_b2_resource_and_trigger_values(obs, cfg, belief)
            if is_b2
            else ({}, (20.0,) * 6)
        )
        best_s = opts[0]
        best_sc = -1e9
        for slot_idx in opts:
            tid, _, _ = obs.lisiere_tile_info(int(slot_idx))
            if is_b2:
                sc = _score_tile_construction_b2(obs, cfg, tid, res_val, trig_vals)
            else:
                fam, _, _ = SYNERGY_META[tid]
                sc = 300.0 if fam == FAMILLE_REVE else (200.0 if fam == FAMILLE_CROISSANCE else 100.0)
            if sc > best_sc:
                best_sc, best_s = sc, slot_idx
        return best_s

    if dtype == DEC_CHOIX_CASE_GARDIEN:
        has_ins_peuple = "I" in cfg.peuples
        sab_tot = obs.sabotage_deck_count + obs.sabotage_pending_count
        reves_on = sum(1 for c2 in range(1, TRACK_LEN + 1) if obs.reve_at_case(c2) > 0)
        w6 = 88.0 if has_ins_peuple else 25.0
        w3 = 89.0 if (is_b2 and sab_tot >= 2) else (81.0 if (is_b2 and sab_tot == 1) else 62.0)
        if cfg.total_reves_partie == 0:
            w5 = 25.0
        else:
            # En v6.1, un 1er Défenseur (2.1) posé sur un Rêve allume 5. Rêve même pendant un Éveil 100 % Gardiens !
            w5 = 83.0 if (is_b2 and reves_on >= 1) else 68.0
        case_weights = {1: 95.0, 6: w6, 4: 82.0, 2: 79.0, 5: w5, 3: w3}
        tid = str(decision.context.get("tile_id", ""))
        if is_b2 and obs.mode >= 3 and tid:
            econ = get_economie_catalog()
            prof_g = cfg.profile_for_slot(tid)
            node = econ.get((tid, prof_g)) if prof_g is not None else None
            if node is not None and node.is_law:
                case_weights = {
                    1: 110.0,
                    4: 105.0,
                    6: (95.0 if has_ins_peuple else 25.0),
                    2: 86.0,
                    3: (92.0 if sab_tot >= 1 else 68.0),
                    5: (85.0 if cfg.total_reves_partie > 0 else 35.0),
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
            # En v6.1 les Pièges sont autonomes : ne retenir un Insecte que s'il boucle une Parade classique !
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
        g6_present = obs.gardien_present_at_case(6)
        g6_bet = obs.gardien_pari_defenders(6) >= 1

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
                    if c_num in (3, 5):
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
                    g6_b = 45.0 if (is_b2 and g6_present and total_bugs <= 1) else 0.0
                    return base_bug + danger_b + (55.0 if (is_b2 and right_of_reve) else 0.0) + g6_b
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
                        return 610.0 + (65.0 if g6_bet else 0.0)
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
            # RESTER : valoriser la conservation d'une réserve forestière (soutien Parade, Nid +2, 6. Insecte)
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
                    if g6_present:
                        stay_sc += 35.0
                elif obs.parcel_arbres(sr_r, sp_r) >= 1 and cur_ins_r == 1 and total_forest_ins <= n_pl:
                    stay_sc += 210.0
                return stay_sc
            return 160.0  # RESTER

        best_mv = opts[0]
        best_m_sc = _mig_sc(opts[0])
        for idx_m in range(1, len(opts)):
            sc = _mig_sc(opts[idx_m])
            if sc > best_m_sc:
                best_m_sc, best_mv = sc, opts[idx_m]
        return best_mv

    if dtype in (DEC_ORDRE_ATTAQUE_5_1, DEC_ORDRE_RATISSAGE_5_2, DEC_ORDRE_NID_4_2):
        # Choix déterministe sans biais
        return max(opts, key=lambda o: _tiebreak(cfg, obs, hash(o) & 0xFFFF, 9))

    return max(opts, key=lambda o: _tiebreak(cfg, obs, hash(o) & 0xFFFF, 11))


class BotB1:
    """Bot Découverte B1 (`k = 1`, oubli stochastique si `> 2` lois actives)."""

    @staticmethod
    def choose(obs: PlayerObservation, decision: DecisionRequest, cfg: GameConfig) -> Any:
        return _choose_policy(obs, decision, cfg, is_b2=False)


class BotB2:
    """Bot Cœur de cible B2 (`k = 2`, graphe `economie_bot` 12 `RES_*` + `TRIG_1..6` + lookahead)."""

    @staticmethod
    def choose(obs: PlayerObservation, decision: DecisionRequest, cfg: GameConfig) -> Any:
        return _choose_policy(obs, decision, cfg, is_b2=True)


def choose_b1(state: GameState, decision: DecisionRequest) -> Any:
    """Point d'entrée isolé B1 : extrait uniquement PlayerObservation pour `decision.decideur`."""
    obs = state.get_observation(decision.decideur)
    return BotB1.choose(obs, decision, state.cfg)


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
) -> GameOver:
    scorer = score_target_b2 if is_b2 else score_target_b1
    if is_b2 and counterfactual_open_paravents:
        chooser = choose_b2_open
        bot_label = "B2_OPEN"
    elif is_b2:
        chooser = choose_b2
        bot_label = "B2"
    else:
        chooser = choose_b1
        bot_label = "B1"
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
) -> GameOver:
    """Exécute une partie complète pilotée par B1 (Ticks 1..3 + révision 2.2) sous garde-fou max_steps."""
    return _play_game_cooperative(
        state,
        is_b2=False,
        k_max_passes=k_max_passes,
        max_steps=max_steps,
        chassis_id=chassis_id,
        telemetry=telemetry,
    )


def play_game_b2(
    state: GameState,
    *,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
) -> GameOver:
    """Exécute une partie complète pilotée par B2 (Ticks 1..3 + révision 2.2 + economie_bot)."""
    return _play_game_cooperative(
        state,
        is_b2=True,
        k_max_passes=k_max_passes,
        max_steps=max_steps,
        chassis_id=chassis_id,
        telemetry=telemetry,
    )


def play_game_b2_open(
    state: GameState,
    *,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
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
    )
