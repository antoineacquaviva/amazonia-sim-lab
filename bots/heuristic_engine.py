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
    DEC_CHOIX_REVE_3_2,
    DEC_COLONIE_A_OPEN,
    DEC_LIBERATION_BATISSEUR_3_1,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_ORDRE_ATTAQUE_5_1,
    DEC_ORDRE_CONSTRUCTION_3_1,
    DEC_ORDRE_NID_4_2,
    DEC_ORDRE_RATISSAGE_5_2,
    DEC_PLACEMENT_NID_3_1,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_RETRAIT_APPRENTISSAGE_6_1,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest, GameOver
from engine.rng import SRC_BOT_TIEBREAK, rand_u64
from engine.state import (
    CARD_SABOTAGE,
    FAMILLE_CROISSANCE,
    FAMILLE_REVE,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
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
    "count_active_laws_from_obs",
    "get_economie_catalog",
    "play_game_b1",
    "play_game_b2",
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
# forte aux Tours 1..5 (nombreux remélanges 6.3 restants + activation du déclencheur 3. Sabotage),
# modérée au Tour 6, faible au Tour 7, quasi nulle au Tour 8.
_SABOTAGE_TOUR_WEIGHT: tuple[float, ...] = (
    175.0,  # index 0 (inutilisé)
    175.0,  # Tour 1
    165.0,  # Tour 2
    150.0,  # Tour 3
    130.0,  # Tour 4
    105.0,  # Tour 5
    68.0,   # Tour 6
    28.0,   # Tour 7
    4.0,    # Tour 8 (0 remélange futur)
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
    total_souches = 0
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
            sch = obs.parcel_souches(r, p)
            total_souches += sch
            total_insects += obs.parcel_insectes(r, p)
            if arb <= 1:
                fragile_parcels += 1

    # Proximité des victoires anticipées en 5.3 (Sommeil bloc des k Rêves en tête / Réveil Gardiens)
    total_reves_cfg = cfg.total_reves_partie
    reves_ranks = [
        r_idx + 1
        for r_idx in range(TRACK_LEN)
        if is_reve_code(obs.tactique_code_bugs_app(r_idx)[0])
    ]
    reves_in_head = sum(1 for rk in reves_ranks if rk <= total_reves_cfg)

    face1_g = 0
    face2_g = 0
    for c in range(TRACK_LEN):
        g_slot = gardiens[c]
        if g_slot.gardien_num > 0:
            if g_slot.face == 2:
                face2_g += 1
            else:
                face1_g += 1

    if total_reves_cfg > 0 and len(reves_ranks) >= total_reves_cfg:
        reve_push_mult = 1.75 if reves_in_head >= total_reves_cfg - 1 else 1.40
    elif total_reves_cfg > 0 and len(reves_ranks) > 0:
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
        "RES_PIEGE": 80.0 + 4.0 * total_rouges,
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
        econ = get_economie_catalog()
        for c in range(1, TRACK_LEN + 1):
            g_slot = gardiens[c - 1]
            if g_slot.gardien_num > 0 and g_slot.remaining_defenders >= 1 and g_slot.tile_id is not None:
                v_open = 38.0 + (reveil_awaken_bonus if g_slot.face == 1 else 0.0)
                if obs.mode >= 3:
                    prof = cfg.profile_for_slot(g_slot.tile_id)
                    node = econ.get((g_slot.tile_id, prof or "A"))
                    if node is not None:
                        v_open += sum(
                            res_val.get(out_tok, 20.0) * 0.45 for out_tok in node.outputs_produits
                        )
                trig_val[c] = v_open

        resonance_4 = trig_val[4] if obs.gardien_available_at_case(4) else 0.0
        for c in range(1, TRACK_LEN + 1):
            if c != 4 and obs.gardien_available_at_case(c):
                trig_val[c] += 0.55 * resonance_4
            if obs.mode >= 3:
                g_slot = gardiens[c - 1]
                if g_slot.tile_id is not None and g_slot.remaining_defenders >= 1:
                    prof = cfg.profile_for_slot(g_slot.tile_id)
                    node = econ.get((g_slot.tile_id, prof or "A"))
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
    # Valeur structurelle Mode 2+ (victoire Sommeil en bloc des k Rêves, production Nid, Pari Gardiens)
    if fam == FAMILLE_REVE:
        # TOUTES les tuiles Rêves en jeu (2 ou 4) doivent être construites et groupées en tête !
        reves_on_track = sum(1 for t in obs.piste_tactiques if is_reve_code(t.code))
        target_reves = max(1, cfg.total_reves_partie)
        if reves_on_track < target_reves:
            struct_v = 195.0 if reves_on_track == 0 else (170.0 if reves_on_track + 1 == target_reves else 150.0)
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
    prof = cfg.profile_for_slot(tile_id) or "A"
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

    Si `for_eveil=True`, ne compte en forêt que les 1ers Défenseurs (`parcel_def1_count`), car lors d'un
    Éveil 100 % Gardiens, tous les `N` 2es Défenseurs quitteront la forêt pour la Piste des Gardiens.
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
            piege_armed = obs.parcel_piege(r, p) == PIEGE_ACTIF and cur_def >= 1
            seuil_e = belief.parcel_expected_seuil[idx]
            c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
            if piege_armed:
                # 2. Piégeage uniquement (1 seul déclenchement par piège armé)
                exp_piege += min(1.05, s_prob)
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
            elif cur_def >= 1 and c_prob > 0.20 and cur_def >= (cfg.dotation_arbres[p - 1] + cfg.offset_seuil_parade - 0.25):
                # En Acte 2, une frappe tombant sur une case CHARGE (4..6) ignore les rouges et peut être parée !
                if ins >= 1 and defs < (cfg.dotation_arbres[p - 1] + cfg.offset_seuil_parade):
                    exp_insecte += 0.55 * min(1.0, c_prob)
                else:
                    exp_parade += 0.55 * min(1.0, c_prob)

    # 2) Étape 3.2 : partition stricte par carte révélée (3. Sabotage > 6. Insecte Bug > 5. Rêve)
    # Information certaine sous notre propre paravent :
    own_hand = obs.hand_of(obs.observer_seat)
    own_card = own_hand.card
    bug_b_active = cfg.profile_for_slot("SLOT_BUG_CERVEAU") == "B"
    own_is_sab = own_card == CARD_SABOTAGE
    if own_is_sab:
        exp_sabotage += 1.0
    elif (
        own_card is not None
        and own_hand.lecture_m is not None
        and 1 <= own_card <= 12
        and 1 <= own_hand.lecture_m <= TRACK_LEN
    ):
        own_m = own_hand.lecture_m
        own_on_reve = obs.reve_at_case(own_m) > 0
        own_bugs = obs.tactique_code_bugs_app(own_m - 1)[1] if bug_b_active else 0
        if own_on_reve:
            # 5. Rêve garanti (avec ou sans Défenseur dessus)
            exp_reve += 0.95
        elif own_bugs >= 1:
            # Un Bug présent sur notre rang M peut dévier le dé -> allume 6. Insecte (et non 5. Rêve)
            exp_insecte += 0.85

    # Espérance prudente pour les (n - 1) autres sièges (strictement sur information publique et loi exacte min(2D6))
    active_deck_machines = 0
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            m_pos, m_st = obs.machine_pos_status(r, mt)
            if m_st == 0 and m_pos > 0:  # MACHINE_STATUS_NORMAL
                active_deck_machines += 1
    sab_in_deck = obs.sabotage_deck_count
    sab_others = max(0, sab_in_deck - (1 if own_is_sab else 0))
    total_deck_est = max(n, active_deck_machines + sab_in_deck)
    p_other_sab = min(0.85, sab_others / max(1.0, float(total_deck_est - 1)))
    if sab_others >= 1:
        exp_sabotage += 0.75 * min(float(sab_others), float(n - 1) * p_other_sab)

    p_other_mach = max(0.0, 1.0 - p_other_sab)
    # Rêves présents sur la piste fixe T1..T6 : pondération par la vraie loi P(min(2D6) = c) !
    prob_reve_rank = sum(
        _MIN_2D6_PROBS_H[c_r - 1]
        for c_r in range(1, TRACK_LEN + 1)
        if obs.reve_at_case(c_r) > 0
    )
    if prob_reve_rank > 0.0:
        exp_reve += 0.82 * float(n - 1) * p_other_mach * prob_reve_rank

    # Bugs présents sur la piste Tactiques (hors Rêves) pouvant dévier les autres machines -> 6. Insecte
    if bug_b_active:
        total_bugs_avail = 0
        prob_bug_rank = 0.0
        for c_b in range(1, TRACK_LEN + 1):
            if obs.reve_at_case(c_b) == 0:
                b_cnt = obs.tactique_code_bugs_app(c_b - 1)[1]
                if b_cnt >= 1:
                    total_bugs_avail += b_cnt
                    prob_bug_rank += _MIN_2D6_PROBS_H[c_b - 1]
        if total_bugs_avail > 0:
            exp_insecte += 0.72 * min(
                float(total_bugs_avail), float(n - 1) * p_other_mach * prob_bug_rank
            )

    # 3) Bonus Colonie 4.3 : uniquement actif sous SLOT_COLONISATION_GARDIENS == 'A'
    if cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "A":
        piste_col = obs.piste_colonie
        if piste_col[0] >= 1:
            exp_parade += 0.85
        if piste_col[1] >= 1:
            exp_piege += 0.85
        if piste_col[2] >= 1:
            exp_sabotage += 0.85
        if piste_col[4] >= 1:
            exp_reve += 0.85
        if piste_col[5] >= 1:
            exp_insecte += 0.85

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
    cap_case = cfg.gardien_bet_cap_for_case(case_c)
    if allies_on_case >= cap_case:
        return 0.0

    eveil_trigs = _estimate_expected_gardien_triggers(obs, cfg, belief, for_eveil=True)
    n = obs.n_players
    allies_g = max(0, obs.total_gardien_pari_defenders() - (1 if own_pari_case > 0 else 0))
    unplaced_allies = max(0, (n - 1) - allies_g)
    colonie_is_a = cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "A"
    colonie_is_b = cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"

    # Capacité physique totale sur les Gardiens construits et capacité attendue hors case 4 (sous hypothèse d'Éveil)
    total_slots_cap = 0
    total_non_res_cap = 0.0
    distinct_other_cap = 0.0
    distinct_other_bet_exp = 0.0
    has_other_empty_supported = False
    for c_k in (1, 2, 3, 5, 6):
        if obs.gardien_present_at_case(c_k):
            cap_k_phys = cfg.gardien_bet_cap_for_case(c_k)
            total_slots_cap += cap_k_phys
            t_k = eveil_trigs[c_k - 1]
            cap_k = min(float(cap_k_phys), t_k)
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
    cap_4 = cfg.gardien_bet_cap_for_case(4)
    if has_res:
        total_slots_cap += cap_4
    col4_bonus = 0.85 if (colonie_is_a and obs.piste_colonie[3] >= 1) else 0.0
    res_cap = min(float(cap_4), distinct_other_cap + col4_bonus) if has_res else 0.0
    total_gardien_cap = total_non_res_cap + res_cap

    if case_c == 4:
        potential_open = min(
            distinct_other_cap, distinct_other_bet_exp + 0.80 * unplaced_allies
        )
        exp_for_case = potential_open + col4_bonus
    else:
        exp_for_case = eveil_trigs[case_c - 1]

    needed_triggers = allies_on_case + 1

    total_init = max(1, n * sum(cfg.dotation_arbres))
    cur_arbres = sum(
        obs.parcel_arbres(r, p) for r in range(n) for p in range(1, cfg.p_max + 1)
    )
    tree_ratio = cur_arbres / total_init

    bouclier_safety = (
        28.0 if (colonie_is_b and obs.piste_colonie[case_c - 1] >= 1) else 0.0
    )

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
    t_code, _, _ = obs.tactique_code_bugs_app(lec - 1)
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
        tot_d = obs.parcel_defenseurs(r_m, tp) + obs.parcel_insectes(r_m, tp)
        if obs.parcel_piege(r_m, tp) == PIEGE_ACTIF and tot_d >= 1:
            continue
        seuil_tp = max(
            1,
            cfg.dotation_arbres[tp - 1]
            + cfg.offset_seuil_parade
            + eff_red
            - bleus
            + spec.mod_seuil,
        )
        if tot_d < seuil_tp and (obs.parcel_arbres(r_m, tp) >= 1 or mt_m == MACHINE_BULLDOZER):
            return False
    return True


def _score_reve_activation(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
) -> float:
    """Évalue la cible `('REVE_ACTIVATION', case_c)` en 2.2 (choix exclusif v6.0 BLOQUER / AVANCER)."""
    if obs.reve_at_case(case_c) <= 0:
        return 0.0

    own_hand = obs.hand_of(obs.observer_seat)
    own_card = own_hand.card
    own_hits_reve = (
        own_card is not None and 1 <= own_card <= 2 * obs.n_players and own_hand.lecture_m == case_c
    )

    cancel_val = 0.0
    if own_hits_reve and own_card is not None:
        ray = (own_card - 1) // 2
        m_type = (own_card - 1) % 2
        pos, st = obs.machine_pos_status(ray, m_type)
        is_active = st != MACHINE_STATUS_RETIRED and pos > 0
        if is_active:
            eff_red = obs.machine_effective_rouges(ray, m_type)
            danger = _tactique_danger(case_c, obs.tour, eff_red)
            if is_b2:
                # 1 seul Défenseur sur le Rêve annule TOUTE la machine (1 ou 2 frappes, tout seuil, Charge incluse) !
                cancel_val = 290.0 + danger * 3.8 + (65.0 if m_type == MACHINE_BULLDOZER else 0.0)
            else:
                cancel_val = 120.0 + danger * 2.2 + (45.0 if m_type == MACHINE_BULLDOZER else 0.0)
        else:
            cancel_val = 25.0

    dest_c: int | None = None
    cascade_discount = 1.0
    adv_mode = cfg.reve_advance_mode
    if adv_mode == "PAS_A_PAS":
        if case_c >= 2:
            if obs.reve_at_case(case_c - 1) == 0:
                dest_c = case_c - 1
            elif (
                case_c >= 3
                and obs.reve_activation_defenders(case_c - 1) >= 1
                and obs.reve_at_case(case_c - 2) == 0
            ):
                dest_c = case_c - 1
                cascade_discount = 0.45 * belief.reve_open_prob_by_rank[case_c - 2]
    else:
        for c2 in range(case_c - 1, 0, -1):
            if obs.reve_at_case(c2) == 0:
                dest_c = c2
                break
        if adv_mode == "SAUT_MAX_1_PAR_TOUR":
            for cl in range(1, case_c):
                if obs.reve_at_case(cl) > 0 and obs.reve_activation_defenders(cl) >= 1:
                    has_left_free = any(obs.reve_at_case(j) == 0 for j in range(1, cl))
                    if has_left_free:
                        p_left = belief.reve_open_prob_by_rank[cl - 1]
                        cascade_discount *= max(0.25, 1.0 - 0.75 * p_left)

    can_advance = dest_c is not None and obs.tour <= 7
    advance_val = 0.0
    sommeil_1_step = False
    if can_advance and dest_c is not None:
        prob_gain = (_MIN_2D6_PROBS_H[dest_c - 1] - _MIN_2D6_PROBS_H[case_c - 1]) * 480.0
        advance_val = (175.0 if is_b2 else 135.0) + prob_gain * (max(0, 8 - obs.tour) / 7.0)
        total_r = cfg.total_reves_partie
        if total_r > 0:
            reves_on_track = sum(1 for c2 in range(1, TRACK_LEN + 1) if obs.reve_at_case(c2) > 0)
            if reves_on_track == total_r:
                gaps_before_block = sum(
                    1 for c2 in range(1, total_r + 1) if obs.reve_at_case(c2) == 0
                )
                if gaps_before_block == 1 and case_c > total_r and dest_c <= total_r:
                    sommeil_1_step = True
                    advance_val += 420.0 if is_b2 else 250.0
                elif case_c > total_r:
                    advance_val += 125.0 if is_b2 else 70.0
        advance_val *= cascade_discount

    total_on_case = obs.reve_activation_defenders(case_c)
    own_reve_case = obs.player_def2_reve_case(obs.observer_seat)
    allies = max(0, total_on_case - (1 if own_reve_case == case_c else 0))

    act_mode = cfg.reve_activation_mode
    if act_mode == "1_DEF_1_MACHINE":
        if own_hits_reve:
            if allies == 0:
                best_branch = max(cancel_val, advance_val)
                option_flex = 0.35 * min(cancel_val, advance_val)
                return (310.0 if is_b2 else 255.0) + best_branch + option_flex
            return (220.0 + cancel_val) if not sommeil_1_step else (110.0 + 0.45 * cancel_val)
        if allies == 0 and can_advance:
            p_hit = belief.reve_open_prob_by_rank[case_c - 1]
            if sommeil_1_step and p_hit >= 0.20:
                return (310.0 if is_b2 else 220.0) + p_hit * advance_val
            if is_b2 and _is_own_hand_covered(obs, cfg) and p_hit >= 0.32 and obs.tour <= 6 and cascade_discount >= 0.50:
                return 235.0 + p_hit * advance_val
        return 40.0

    if act_mode == "1_DEF_ALL_RANK":
        if allies >= 1:
            return 25.0
        if own_hits_reve:
            return 280.0 + max(cancel_val, advance_val) + 0.35 * min(cancel_val, advance_val)
        return 50.0

    # BINOME_ALL_RANK
    if allies >= 2:
        return 20.0
    if allies == 1:
        if own_hits_reve:
            return 340.0 + max(cancel_val, advance_val) + 0.35 * min(cancel_val, advance_val)
        if belief.drew_sabotage_or_none:
            return 220.0 + advance_val
        return 165.0 + 0.7 * advance_val
    if own_hits_reve:
        return 240.0 + 0.8 * max(cancel_val, advance_val)
    return 40.0


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
    _ = is_first_defender
    active_laws = count_active_laws_from_obs(obs, cfg)
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        r_i, p_i = int(r), int(p)
        idx = r_i * MAX_P + (p_i - 1)
        defs = obs.parcel_defenseurs(r_i, p_i)
        ins = obs.parcel_insectes(r_i, p_i)
        cur_def = defs + ins
        s_prob = belief.parcel_strike_prob[idx]
        c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
        seuil_e = belief.parcel_expected_seuil[idx]
        arbres = obs.parcel_arbres(r_i, p_i)
        souches = obs.parcel_souches(r_i, p_i)

        score = 95.0
        # Armer un Piège inerte sur parcelle menacée
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and cur_def == 0:
            score += 420.0 + 260.0 * min(1.5, s_prob)
        # Activer un Nid en forêt
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            score += 470.0
        # Parer une frappe attendue (valorisation directe des Arbres debout, 0 Repousse Finale)
        if s_prob > 0.08 and cur_def < seuil_e:
            gap = seuil_e - cur_def
            reach_mult = 1.0 if gap <= 1.25 else (0.58 if gap <= 2.25 else 0.25)
            tree_weight = 1.10 if arbres >= 2 else (0.95 if arbres == 1 else 0.35)
            urgency = 600.0 * min(1.6, s_prob) * reach_mult * tree_weight
            # Prévention légère des gains de Puissance sur case CHARGE (plus marquée en Acte 1)
            if c_prob > 0.08 and gap <= 1.25 and (arbres >= 1 or belief.parcel_bulldo_prob[idx] > 0.15):
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
        fam_bonus = 95.0 if fam == FAMILLE_REVE else (80.0 if fam == FAMILLE_CROISSANCE else 60.0)
        if constructors == 1:
            base_l = 610.0 + fam_bonus
        elif belief.drew_sabotage_or_none and obs.tour <= 7:
            # Émetteur altruiste Sabotage au Tick 1 : ouvre prioritairement un chantier coopératif !
            base_l = 525.0 + fam_bonus
        else:
            base_l = 255.0 + fam_bonus
        return base_l + _b1_forgetting_penalty(obs, cfg, active_laws, 300 + s_idx)

    if kind == "FURTIVITE":
        _, l_idx, p, rive = target
        l_i, p_i, rv = int(l_idx), int(p), int(rive)
        d_rv = obs.furtivite_rive_defs(l_i, p_i, rv)
        t_ray = l_i if rv == 0 else (l_i + 1) % obs.n_players
        idx = t_ray * MAX_P + (p_i - 1)

        has_m = any(
            obs.machine_pos_status(t_ray, mt)[0] == p_i
            and obs.machine_pos_status(t_ray, mt)[1] != MACHINE_STATUS_RETIRED
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        # Furtivité libre A1 : seul un binôme complet de 2 Défenseurs sur cette même rive déclenche l'action
        partner_ready = d_rv == 1
        useful_trap = (not has_m) and obs.parcel_piege(t_ray, p_i) == PIEGE_AUCUN
        has_siege = any(
            obs.machine_pos_status(t_ray, mt) == (p_i, MACHINE_STATUS_RATISSAGE)
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        useful_sab = (
            has_m
            and (not has_siege)
            and belief.parcel_strike_prob[idx] < 0.85
            and obs.tour <= 6
        )

        if partner_ready and (useful_trap or useful_sab):
            base_f = 550.0 if useful_trap else 520.0
        elif belief.drew_sabotage_or_none and (useful_trap or useful_sab):
            base_f = 435.0 if useful_trap else 405.0
        else:
            base_f = 135.0
        return base_f + _b1_forgetting_penalty(obs, cfg, active_laws, 500 + l_i * 10 + p_i)

    if kind == "GARDIEN_PARI":
        _, case_c = target
        c_i = int(case_c)
        return _score_gardien_pari(obs, cfg, belief, c_i, is_b2=False) + _b1_forgetting_penalty(
            obs, cfg, active_laws, 700 + c_i
        )

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        c_i = int(case_c)
        return _score_reve_activation(obs, cfg, belief, c_i, is_b2=False) + _b1_forgetting_penalty(
            obs, cfg, active_laws, 800 + c_i
        )

    return 0.0


def _score_target_b2_core(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    *,
    is_held: bool = False,
) -> float:
    """Noyau d'évaluation B2 (`k=2`, graphe `economie_bot` + économie v6.0 Acte 1 CHARGE / Acte 2 ASSAUT).

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
        s_prob = belief.parcel_strike_prob[idx]
        c_prob = belief.parcel_charge_prob[idx] if belief.parcel_charge_prob else 0.0
        seuil_e = belief.parcel_expected_seuil[idx]
        arbres = obs.parcel_arbres(r_i, p_i)
        souches = obs.parcel_souches(r_i, p_i)

        score = 90.0
        trig_1_v = trig_vals[0]  # 1. Parade (Défenseurs seuls)
        trig_2_v = trig_vals[1]  # 2. Piégeage (frappe bloquée par Piège)
        trig_6_v = trig_vals[5]  # 6. Insecte (Parade avec dépense d'Insecte uniquement en 5.1)

        # Charge denial : en Acte 1 (Tours 1-4), empêcher un dégât effectif sur une case CHARGE évite
        # +1 jeton Puissance durable qui renforcera les attaques ASSAUT (cases 1-3) de tout l'Acte 2 !
        can_inflict_damage = (arbres >= 1) or (souches >= 1 and belief.parcel_bulldo_prob[idx] > 0.10)
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
        charge_denial = (
            min(1.40, c_prob) * charge_unit_v if (c_prob > 0.05 and can_inflict_damage) else 0.0
        )

        # 1. Armement d'un Piège Embuscade : pare n'importe quel Seuil + épargne les Insectes + bloque Charge
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and cur_def == 0:
            saved_ins_v = min(3, ins) * res_val["RES_INSECTE"] * 0.4
            piege_bet_bonus = 95.0 if obs.gardien_pari_defenders(2) >= 1 else 0.0
            score += (
                420.0
                + s_prob * (320.0 + trig_2_v + saved_ins_v + piege_bet_bonus)
                + 0.9 * charge_denial
                + (35.0 if is_held else 0.0)
            )

        # 2. Activation d'un Nid en 4.2 : produit +1/+2 Insectes + pouvoir du Nid (n'allume jamais 6. Insecte)
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            prod_cnt = 1 if ins <= 1 else 2
            score += 375.0 + prod_cnt * res_val["RES_INSECTE"] + (35.0 if is_held else 0.0)

        # 3. Lookahead 5.1 -> 6.2 : valorisation directe des Arbres debout (0 Repousse Finale) + Charge denial
        if s_prob > 0.05:
            piege_armed = obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and cur_def >= 1
            if not piege_armed and cur_def < seuil_e:
                gap = seuil_e - cur_def
                parade_trig_v = trig_1_v if (defs + 1 >= seuil_e) else trig_6_v
                expected_trees_saved = min(2.0, float(arbres))
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
                    cheap_act1_b = (
                        55.0 if (obs.tour <= 4 and c_prob > 0.12 and can_inflict_damage) else 0.0
                    )
                    score += full_parade_v + cheap_act1_b + own_ray_b + (45.0 if is_held else 0.0)
                elif gap <= 2.25:
                    # Parade bon marché à 2 Défenseurs : forte priorité sur menace directe certaine
                    # (propre carte ou Ratissage, s_prob >= 0.85), modérée sur suspicion bayésienne diffuse
                    # afin de laisser les joueurs disponibles construire Nids, Rêves et Gardiens !
                    if is_held:
                        score += (0.48 if s_prob >= 0.85 else 0.34) * full_parade_v + own_ray_b
                    elif s_prob >= 0.85:
                        cheap_act1_b = (
                            65.0 if (obs.tour <= 4 and c_prob > 0.12 and can_inflict_damage) else 0.0
                        )
                        score += 0.62 * full_parade_v + cheap_act1_b + own_ray_b
                    else:
                        score += 0.40 * full_parade_v + own_ray_b
                elif gap <= 3.25 and arbres >= 1 and not is_held:
                    score += (0.28 if s_prob >= 0.85 else 0.18) * full_parade_v
            elif not piege_armed and cur_def >= seuil_e and ins > 0 and defs < seuil_e:
                # Épargner 1 Insecte qui aurait été défaussé par la parade classique !
                score += s_prob * (0.85 * res_val["RES_INSECTE"])

        if arbres == 0 and souches >= 1 and belief.parcel_bulldo_prob[idx] > 0.15 and cur_def < seuil_e:
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
        _, l_idx, p, rive = target
        l_i, p_i, rv = int(l_idx), int(p), int(rive)
        raw_d_rv = obs.furtivite_rive_defs(l_i, p_i, rv)
        d_rv = max(0, raw_d_rv - 1) if is_held else raw_d_rv
        d_other = obs.furtivite_rive_defs(l_i, p_i, 1 - rv)
        t_ray = l_i if rv == 0 else (l_i + 1) % obs.n_players
        if obs.is_route(t_ray, p_i):
            return 40.0
        idx = t_ray * MAX_P + (p_i - 1)

        present_mts = [
            mt
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
            if obs.machine_pos_status(t_ray, mt)[0] == p_i
            and obs.machine_pos_status(t_ray, mt)[1] != MACHINE_STATUS_RETIRED
        ]
        has_m = len(present_mts) > 0
        has_siege = any(
            obs.machine_pos_status(t_ray, mt) == (p_i, MACHINE_STATUS_RATISSAGE)
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        partner_ready = d_rv == 1

        # Comptage public des autres rives de Furtivité déjà engagées sur le plateau ce tour :
        # évite de vider la forêt (et supprime le sur-investissement à 2 rives, notamment à 3J-4J).
        other_completed_rives = 0
        other_open_rives = 0
        for l2 in range(obs.n_players):
            for p2 in range(1, cfg.p_max + 1):
                for rv2 in (0, 1):
                    if l2 == l_i and p2 == p_i and rv2 == rv:
                        continue
                    cnt2 = obs.furtivite_rive_defs(l2, p2, rv2)
                    if cnt2 == 2:
                        other_completed_rives += 1
                    elif cnt2 == 1:
                        other_open_rives += 1

        action_v = 0.0
        if not has_m and obs.parcel_piege(t_ray, p_i) == PIEGE_AUCUN:
            # 4.1 Préparer un Piège : UNIQUEMENT s'il existe au moins une machine active en amont (< p_i) !
            upstream_positions: list[int] = []
            max_up_red = 0
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                mp_u, ms_u = obs.machine_pos_status(t_ray, mt)
                if ms_u != MACHINE_STATUS_RETIRED and 0 < mp_u < p_i:
                    upstream_positions.append(mp_u)
                    max_up_red = max(max_up_red, obs.machine_effective_rouges(t_ray, mt))
            if upstream_positions:
                dist = p_i - max(upstream_positions)
                arbres_t = obs.parcel_arbres(t_ray, p_i)
                souches_t = obs.parcel_souches(t_ray, p_i)
                has_value_to_protect = arbres_t >= 1 or souches_t >= 1
                if has_value_to_protect and not (dist >= 2 and obs.tour >= 6):
                    seuil_assaut = (
                        cfg.dotation_arbres[p_i - 1] + cfg.offset_seuil_parade + max_up_red
                    )
                    already_armed = (
                        obs.parcel_insectes(t_ray, p_i) + obs.parcel_defenseurs(t_ray, p_i)
                    ) >= 1
                    s_now = belief.parcel_strike_prob[idx]
                    # Coût réel d'un Piège : 2 Défenseurs en 4.1 + (0 si déjà occupé, sinon 1 pion d'armement).
                    # En Acte 1 (Tours 1-3), si seuil_assaut <= 2 et pas de frappe imminente déjà armée,
                    # parer directement en forêt coûte moins de Défenseurs que passer par la Furtivité !
                    effective_saving = float(seuil_assaut) - (1.8 if already_armed else 2.6)
                    imminent_armed_hit = already_armed and dist == 1 and s_now >= 0.45 and max_up_red >= 1
                    min_sav = 1.2 if obs.tour <= 3 else (0.9 if obs.tour == 4 else 0.3)
                    if imminent_armed_hit:
                        action_v = 110.0 + 75.0 * min(1.5, s_now) + 32.0 * max(0.0, effective_saving)
                    elif effective_saving >= min_sav and dist == 1:
                        act1_disc = 0.60 if obs.tour <= 3 else (0.85 if obs.tour == 4 else 1.0)
                        action_v = act1_disc * (65.0 + 58.0 * effective_saving + 45.0 * min(1.2, s_now))
                    elif effective_saving >= 1.4 and dist == 2 and obs.tour == 4:
                        action_v = 0.45 * (55.0 + 45.0 * effective_saving)
                    if action_v > 0.0 and obs.gardien_present_at_case(2) and obs.tour <= 6:
                        action_v += 0.35 * trig_vals[1]
        elif has_m and not has_siege and obs.tour <= 5:
            # 4.1 Saboter le chantier : uniquement aux Tours 1..5 (assez de remélanges restants)
            # et seulement si la probabilité que TOUTES les machines présentes soient inactives est élevée !
            own_hand = obs.hand_of(obs.observer_seat)
            own_hits_here = False
            if own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players:
                own_r, own_mt = unpack_machine_card(own_hand.card)
                if own_r == t_ray and own_mt in present_mts:
                    own_hits_here = True
            if not own_hits_here:
                active_deck_m = 0
                for r_d in range(obs.n_players):
                    for mt_d in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                        mp_d, ms_d = obs.machine_pos_status(r_d, mt_d)
                        if ms_d == 0 and mp_d > 0:
                            active_deck_m += 1
                sab_cnt = obs.sabotage_deck_count
                deck_rem = max(obs.n_players, active_deck_m + sab_cnt) - (
                    1 if own_hand.has_card else 0
                )
                other_draws = max(0, obs.n_players - 1)
                if len(present_mts) == 1:
                    p_inactive = max(0.0, 1.0 - other_draws / max(1.0, float(deck_rem)))
                else:
                    p1 = max(0.0, 1.0 - other_draws / max(1.0, float(deck_rem)))
                    p2 = max(0.0, 1.0 - other_draws / max(1.0, float(max(1, deck_rem - 1))))
                    p_inactive = p1 * p2
                # Sous MEME_PARCELLE_P1 (2 machines, p_inactive ~ 0.22), 78 % de risque de perdre 2 Défenseurs !
                if p_inactive >= 0.42:
                    sab_stock_mult = (
                        1.25 if sab_cnt == 0 else (0.90 if sab_cnt == 1 else (0.55 if sab_cnt == 2 else 0.25))
                    )
                    prep_trig3 = (
                        (0.65 * trig_vals[2] + (40.0 if sab_cnt == 0 else 15.0))
                        if obs.gardien_present_at_case(3)
                        else 0.0
                    )
                    gross_sab = res_val["RES_DILUTION_SABOTAGE"] * sab_stock_mult * 0.95 + prep_trig3
                    # Retrancher la perte sèche attendue des 2 Défenseurs en cas de machine active en 3.2
                    waste_risk_pen = (1.0 - p_inactive) * (115.0 if obs.tour <= 4 else 85.0)
                    action_v = max(0.0, p_inactive * gross_sab - waste_risk_pen)

        if action_v <= 12.0:
            return 75.0

        # Coût de rareté des Défenseurs : pénalise fortement une 2e rive simultanée (et l'Acte 1 à 3J-4J)
        scarcity_pen = 0.0
        if other_completed_rives >= 1:
            scarcity_pen += 220.0 if obs.n_players <= 4 else 145.0
        if d_other >= 1:
            scarcity_pen += 165.0 if obs.n_players <= 4 else 110.0
        if not partner_ready and other_open_rives >= 1:
            scarcity_pen += 130.0
        if obs.tour <= 4 and obs.n_players == 3:
            scarcity_pen += 55.0

        if partner_ready:
            return max(75.0, 395.0 + action_v * 1.22 - scarcity_pen + (35.0 if is_held else 0.0))
        if is_held:
            # Seul (1/2) sur la rive en révision 2.2 -> se replier vers la forêt !
            return 95.0
        if belief.drew_sabotage_or_none:
            return max(75.0, 290.0 + action_v * 1.05 - scarcity_pen)
        # Un joueur détenant une carte Machine active n'ouvre pas seul une rive de Furtivité
        return max(70.0, 110.0 + action_v * 0.35 - scarcity_pen)

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
        base_rv = _score_reve_activation(obs, cfg, belief, int(case_c), is_b2=True)
        if is_held:
            c_i = int(case_c)
            own_hand = obs.hand_of(obs.observer_seat)
            own_hits = (
                own_hand.card is not None
                and 1 <= own_hand.card <= 2 * obs.n_players
                and own_hand.lecture_m == c_i
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
        _ = is_first_defender
        return _score_target_b2_core(obs, cfg, belief, target, is_held=False)

    @staticmethod
    def held_score(
        obs: PlayerObservation,
        cfg: GameConfig,
        belief: BeliefSummary,
        cur_spot: tuple[Any, ...],
    ) -> float:
        return _score_target_b2_core(obs, cfg, belief, cur_spot, is_held=True)


score_target_b2 = _B2TargetScorer()


# ---------------------------------------------------------------------------
# Politique complète hors Étape 2 (Étapes 3, 4, 5, 6 et Effets de tuiles)
# ---------------------------------------------------------------------------


_MACHINE_PAIR_EFFECT_KINDS: frozenset[str] = frozenset(
    {
        "MACHINE_SURCHAUFFE",
        "MACHINE_RECUL",
        "MOD_SEUIL_MACHINE",
        "REMOVE_RED_R_H",
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
        "PIEGE_HABITE_G7D",
        "CONVERSION_INSECTE_SABOTAGE_G10C",
        "SENTINELLE_EMBUSCADE_G10D",
        "HARPIE_MOD_SEUIL_F1",
        "HARPIE_AUTO_PARADE_F2",
        "CONVERSION_PIEGE_REVE_G12C",
        "SECONDE_RIVE_PIEGE_HR",
        "PIEGE_CIBLE_VIDE_HO",
        "INSECTE_SUR_PIEGE_HO",
        "POSE_INSECTE_HI",
        "PIEGE_ER_3_2",
        "M1_DEPLACER_DEFENSEUR",
    }
)

_TACTIQUE_DANGER: dict[int, float] = {1: 10.0, 2: 12.0, 4: 45.0, 5: 48.0, 3: 70.0, 6: 95.0}


def _score_effect_option(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    decision: DecisionRequest,
    opt: Any,
    *,
    is_b2: bool,
) -> float:
    """Évalue génériquement une option de `DEC_EFFET_TUILE` (Lot 01..10) sur `PlayerObservation`.

    Le dispatch est strictement gouverné par `effect_kind` afin d'éviter toute collision
    entre tuples d'entiers de sémantiques distinctes (ex. `(seat, +1)` de `SHIFT_LECTURE_M`
    vs `(ray, p)` d'une parcelle ou `(ray, m_type)` d'une machine).
    """
    slot_id = str(decision.context.get("slot_id", ""))
    kind_hint = str(decision.context.get("effect_kind", ""))

    if opt == "PASSER":
        # Pour un sacrifice (ex: G4 A), ne sacrifier que si le gain dépasse nettement la valeur de G4 en piste !
        if "SACRIFICE" in kind_hint or slot_id == "G4":
            g_cnt = sum(1 for g in obs.piste_gardiens if g.gardien_num > 0)
            sole_g = obs.gardien_pari_enabled and g_cnt == 1
            return 380.0 if sole_g else 240.0
        if kind_hint == "OFFRANDE_GARDIEN_AVANCEE_REVE":
            return 180.0
        return 25.0

    # 1. Décalage lecture dé M `(seat, delta_m)` (ex: G6:A) — dispatch explicite AVANT tout barème parcelle
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
        old_code, _, _ = obs.tactique_code_bugs_app(old_m - 1)
        new_code, _, _ = obs.tactique_code_bugs_app(new_m - 1)
        # Décaler une carte Machine sur un Rêve l'annule ET ouvre/avance le Rêve : jackpot !
        if is_reve_code(new_code) and not is_reve_code(old_code):
            return 750.0
        if is_reve_code(old_code) and not is_reve_code(new_code):
            return -200.0
        if is_tactique_code(old_code) and is_tactique_code(new_code):
            r_m, mt_m = unpack_machine_card(h.card)
            eff_r = obs.machine_effective_rouges(r_m, mt_m)
            return 150.0 + (_tactique_danger(old_code, obs.tour, eff_r) - _tactique_danger(new_code, obs.tour, eff_r)) * 4.0
        return 80.0

    # 2. Machine `(ray, m_type)` (G1:A/B, G2:A, G9:B, R4:A, R7:A, R10:A, M2:A)
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
            sc += 40.0  # -1 Apprentissage durable en 6.1 !
        return sc

    # 2b. Échange de deux tuiles Tactique adjacentes `(rank_a, rank_b)` (R1:A)
    if (
        kind_hint == "TAMBOUR_SWAP_TACTIQUES"
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
    ):
        ra, rb = int(opt[0]), int(opt[1])
        ca, _, app_a = obs.tactique_code_bugs_app(ra)
        cb, _, app_b = obs.tactique_code_bugs_app(rb)
        da = _TACTIQUE_DANGER.get(ca, 40.0)
        db = _TACTIQUE_DANGER.get(cb, 40.0)
        # Préférer placer la Tactique la plus douce vers les petits rangs (ra < rb) et éloigner la plus violente
        return 140.0 + (da - db) * 2.5 + (app_b - app_a) * 15.0

    # 2c. Offrande d'un Gardien `(case_1_6, total_steps)` (R1:C)
    if (
        kind_hint == "OFFRANDE_GARDIEN_AVANCEE_REVE"
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
    ):
        case_g, total_steps = int(opt[0]), int(opt[1])
        cur_rank = int(decision.context.get("current_rank", 4))
        if total_steps < 2:
            # Ne rien gagner au-delà de l'avancée gratuite : toujours inférieur à PASSER (180.0)
            return 20.0
        # Avancée supplémentaire de +1 rang : jackpot si le Rêve atteint le Rang 1 (victoire !)
        win_bonus = 620.0 if cur_rank <= 3 else (260.0 if cur_rank == 4 else 140.0)
        used_bonus = 45.0 if not obs.gardien_available_at_case(case_g) else 0.0
        return win_bonus + used_bonus - (7 - case_g) * 8.0

    # 2d. Convoi 5.3 `(src_p, dst_p)` sur un rayon fixé (M4:D)
    if (
        kind_hint == "M4_CONVOI_5_3"
        and isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
    ):
        nid_r = int(decision.context.get("ray", 0))
        sp, dp = int(opt[0]), int(opt[1])
        dst_idx = nid_r * MAX_P + (dp - 1)
        dst_defs = obs.parcel_defenseurs(nid_r, dp) + obs.parcel_insectes(nid_r, dp)
        return 150.0 + belief.parcel_strike_prob[dst_idx] * 240.0 + (120.0 if dst_defs >= 1 else 0.0) + (dp - sp) * 20.0

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
        if kind_hint in ("PIEGE_SOUCHE", "PIEGE_HABITE_G7D", "SECONDE_RIVE_PIEGE_HR", "PIEGE_ER_3_2") and defs >= 1:
            sc += 220.0  # Embuscade immédiatement armée !
        elif kind_hint == "MOD_SEUIL_PARCELLE" and 0 < defs < belief.parcel_expected_seuil[idx]:
            sc += 200.0
        elif kind_hint in ("HARPIE_MOD_SEUIL_F1", "HARPIE_AUTO_PARADE_F2"):
            if obs.parcel_defenseurs(r_p, p_p) >= 2:
                sc += 240.0
        elif kind_hint in ("SENTINELLE_EMBUSCADE_G10D", "INSECTE_SUR_PIEGE_HO"):
            # Armer en priorité une parcelle piégée encore désarmée (0 Défenseur, 0 Insecte)
            sc += 280.0 if defs == 0 else 60.0
        elif kind_hint == "CONVERSION_INSECTE_SABOTAGE_G10C":
            # Sacrifier un Insecte là où la frappe est improbable ou déjà couverte
            sc = 210.0 - s_prob * 180.0 + (45.0 if defs >= 2 else 0.0)
        elif kind_hint == "CONVERSION_PIEGE_REVE_G12C":
            reve_r = int(decision.context.get("reve_rank", 2))
            win_bonus = 600.0 if reve_r == 1 else 240.0
            sc = 150.0 + win_bonus - s_prob * 160.0
        return sc

    # 4. Déplacement d'un Défenseur `(src_spec, (dst_r, dst_p))` (G3:A/C/D, G4:A, R3:A, R8:D, M3:A)
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

    # 5. Déplacement groupé d'Insectes `(r, src_p, dst_p)` (ex: G2:C, R10:D)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint in ("MOVE_ALL_INSECTES", "PIEGE_ET_REDEPLOIEMENT_INSECTE")
    ):
        r_i, src_p, dst_p = opt
        src_idx = r_i * MAX_P + (src_p - 1)
        dst_idx = r_i * MAX_P + (dst_p - 1)
        return (
            100.0
            + (belief.parcel_strike_prob[dst_idx] - belief.parcel_strike_prob[src_idx]) * 260.0
            + (dst_p - src_p) * 35.0
        )

    # 5b. Échange atomique Vol en ciseaux `(src_ray, p, dst_rive)` (G6:C)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint == "ECHANGE_CISEAUX_G6C"
    ):
        src_r, p_c, dst_rv = opt
        l_c = int(decision.context.get("lisiere", src_r))
        t_ray = l_c if dst_rv == 0 else (l_c + 1) % obs.n_players
        nb_d, _ = obs.furtivite_defs_and_ins(l_c, p_c)
        binome_bonus = 240.0 if nb_d == 1 else 60.0
        trap_bonus = 140.0 if obs.parcel_piege(t_ray, p_c) == PIEGE_AUCUN else 20.0
        return 120.0 + binome_bonus + trap_bonus

    # 5c. Sillage du Boto `(ray, m_type, delta_dir)` (G8:A)
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

    # 6. Choix en 1.3 de retenir max(D1, D2) derrière paravent (G6:B, R5:B)
    if opt == "RETENIR_MAX" and kind_hint == "CHOIX_DE_M_1_3":
        min_m = int(decision.context.get("min_m", 1))
        max_m = int(decision.context.get("max_m", 1))
        old_c, _, _ = obs.tactique_code_bugs_app(min_m - 1)
        new_c, _, _ = obs.tactique_code_bugs_app(max_m - 1)
        if is_reve_code(new_c) and not is_reve_code(old_c):
            return 720.0
        if is_reve_code(old_c) and not is_reve_code(new_c):
            return 10.0
        if is_tactique_code(old_c) and is_tactique_code(new_c):
            return 85.0 + (_TACTIQUE_DANGER[old_c] - _TACTIQUE_DANGER[new_c]) * 3.5
        return 70.0

    # 6b. Choix 4.1 entre PIEGE sous machine (G7:B) et SABOTAGE
    if opt in ("PIEGE", "SABOTAGE") and kind_hint == "FURTIVITE_PIEGE_OU_SABOTAGE":
        r_f = int(decision.context.get("ray", 0))
        p_f = int(decision.context.get("p", 1))
        has_sup = obs.parcel_defenseurs(r_f, p_f) + obs.parcel_insectes(r_f, p_f) >= 1
        if opt == "PIEGE":
            return 340.0 if has_sup else 210.0
        return 260.0 if obs.tour <= 6 else 180.0

    # 6c. Inversion Bulldozer avant Abatteuse sur rayon `r` (G8:B)
    if isinstance(opt, int) and kind_hint == "INVERSION_BOTO_G8B":
        bu_obs = obs.machines[opt * 2 + MACHINE_BULLDOZER]
        p_bu = bu_obs.position
        if 1 <= p_bu <= cfg.p_max and obs.parcel_souches(opt, p_bu) == 0:
            return 360.0  # 0 Souche à terrasser si le Bulldozer passe avant l'Abatteuse !
        return 60.0

    # 6d. Sacrifice d'ouverture anticipée des paravents (ex: G4:B)
    if opt == "SACRIFIER_G4_PARAVENTS":
        return 310.0 if obs.tour >= 6 else 180.0

    # 6e. Loi 5.3 du Puits `(act, r, mt, p)` : retourner Rouge en Bleu vaut double (Seuil -2 + -1 App 6.1) (G10:B)
    if (
        isinstance(opt, tuple)
        and len(opt) == 4
        and kind_hint == "PUITS_PIEGE_PUISSANCE_5_3"
    ):
        return 360.0 if opt[0] == "SURCHAUFFE_BLEU" else 220.0

    # 6f. Avancement d'un Rêve `r_idx` vers la gauche (G12:A) : privilégier le Rêve le plus proche du Rang 1
    if isinstance(opt, int) and kind_hint == "ADVANCE_REVE_G12A":
        return 750.0 if opt == 1 else (380.0 - opt * 40.0)

    # 6g. Relais du Vent `("FLIP_FACE2" | "OPEN_SLOT", case_c)` (G12:B)
    if (
        isinstance(opt, tuple)
        and len(opt) == 2
        and isinstance(opt[0], str)
        and isinstance(opt[1], int)
        and kind_hint == "VENT_RELAIS_GARDIEN_G12B"
    ):
        act_v, case_v = opt[0], opt[1]
        if act_v == "OPEN_SLOT":
            return 340.0 + (7 - case_v) * 15.0
        return 290.0 + (7 - case_v) * 10.0

    # 6h. Pose d'Insecte La Brèche du Tamanoir `("FORET" | "FURTIVITE", idx_a, p)` (G13:A)
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

    # 6i. Écaille du Téju `(r, src_p, dst_p)` (G14:A) ou Porteurs du Téju `(r, src_p, dst_p)` (G14:D)
    if (
        isinstance(opt, tuple)
        and len(opt) == 3
        and isinstance(opt[0], int)
        and isinstance(opt[1], int)
        and isinstance(opt[2], int)
        and kind_hint in ("ECAILLE_TEJU_CONVERSION_PIEGE", "PORTEURS_TEJU_DEPLACER_INSECTE")
    ):
        r_t, src_p, dst_p = int(opt[0]), int(opt[1]), int(opt[2])
        src_idx = r_t * MAX_P + (src_p - 1)
        dst_idx = r_t * MAX_P + (dst_p - 1)
        src_defs = obs.parcel_defenseurs(r_t, src_p) + obs.parcel_insectes(r_t, src_p)
        dst_defs = obs.parcel_defenseurs(r_t, dst_p) + obs.parcel_insectes(r_t, dst_p)
        if kind_hint == "ECAILLE_TEJU_CONVERSION_PIEGE":
            # Ne pas consommer le dernier pion qui devait armer le Piège !
            rem_on_dst = (dst_defs - 1) if src_p == dst_p else dst_defs
            arm_bonus = 240.0 if rem_on_dst >= 1 else -90.0
            return (
                180.0
                + arm_bonus
                + belief.parcel_strike_prob[dst_idx] * 280.0
                - (140.0 if src_defs == 1 and obs.parcel_piege(r_t, src_p) == PIEGE_ACTIF else 0.0)
            )
        # G14:D : envoyer l'Insecte armer un Piège désarmé (dst_defs == 0)
        arm_d_bonus = 290.0 if dst_defs == 0 else 70.0
        disarm_pen = 220.0 if (src_defs == 1 and obs.parcel_piege(r_t, src_p) == PIEGE_ACTIF) else 0.0
        return (
            160.0
            + arm_d_bonus
            - disarm_pen
            + (belief.parcel_strike_prob[dst_idx] - belief.parcel_strike_prob[src_idx]) * 220.0
        )

    # 6j. Profondeur `p` sur un rayon connu (G14:C, M1:C, M1:D, G13:B)
    if isinstance(opt, int) and kind_hint in (
        "VENTRE_PLEIN_NOURRIR_F1",
        "VENTRE_PLEIN_PIEGE_F2",
        "M1_DEPLACER_INSECTE_RAYON",
        "M1_SENTINELLES_PIEGES",
        "BRECHE_TAMANOIR_HYBRIDE_3_1",
    ):
        r_rep = int(decision.context.get("ray", decision.context.get("lisiere", 0)))
        p_rep = int(opt)
        idx_rep = r_rep * MAX_P + (p_rep - 1)
        defs_rep = obs.parcel_defenseurs(r_rep, p_rep) + obs.parcel_insectes(r_rep, p_rep)
        if kind_hint == "VENTRE_PLEIN_NOURRIR_F1":
            return 220.0 - belief.parcel_strike_prob[idx_rep] * 150.0 + (45.0 if defs_rep >= 2 else 0.0)
        if kind_hint == "M1_SENTINELLES_PIEGES":
            return 180.0 + belief.parcel_strike_prob[idx_rep] * 240.0 + (260.0 if defs_rep == 0 else 40.0)
        if kind_hint == "M1_DEPLACER_INSECTE_RAYON":
            return 150.0 + belief.parcel_strike_prob[idx_rep] * 260.0 + (120.0 if obs.parcel_piege(r_rep, p_rep) == PIEGE_ACTIF and defs_rep == 0 else 0.0)
        if kind_hint == "BRECHE_TAMANOIR_HYBRIDE_3_1":
            return 160.0 - p_rep * 10.0
        return 210.0 + belief.parcel_strike_prob[idx_rep] * 270.0 + (180.0 if defs_rep >= 1 else 0.0)

    # 6k. Envol du Batará Suiveur `(loc, idx_a, p, track, case_1_6)` (G15:A)
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
        t_code, bugs_c, app_c = obs.tactique_code_bugs_app(c_b - 1)
        is_t = 1 <= t_code <= 6
        return 210.0 + (95.0 if is_t and bugs_c == 0 else 20.0) + app_c * 35.0 - src_pen

    # 6l. Déviation Synaptique `"M_MOINS_1" | "M_PLUS_1"` en 3.2 (SLOT_BUG_CERVEAU:B)
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
        old_c, _, _ = obs.tactique_code_bugs_app(old_m - 1)
        new_c, _, _ = obs.tactique_code_bugs_app(new_m - 1)
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

    # 6m. Double avancée de Rêve `1 | 2` (R1:B)
    if isinstance(opt, int) and kind_hint == "REVE_DOUBLE_AVANCEE":
        cur_rank = int(decision.context.get("current_rank", 4))
        if opt >= 2:
            return 720.0 if cur_rank <= 3 else 420.0
        return 120.0

    # 6n. Retrait d'Apprentissage en 6.1 `rank_idx` (R2:A)
    if isinstance(opt, int) and kind_hint == "VOILE_OUBLI_RETRAIT_6_1":
        t_code, _, app_c = obs.tactique_code_bugs_app(opt)
        return 180.0 + app_c * 65.0 + _TACTIQUE_DANGER.get(t_code, 30.0) + (6 - opt) * 12.0

    # 6o. Activation d'un Nid `m_num` en 3.2 (R6:B)
    if isinstance(opt, int) and kind_hint == "ACTIVER_NID_INSECTES_3_2":
        foret_obs = obs.foret
        for r_n in range(obs.n_players):
            row_n = foret_obs[r_n]
            for p_n in range(1, cfg.p_max + 1):
                if row_n[p_n - 1].nid_id == opt:
                    idx_n = r_n * MAX_P + (p_n - 1)
                    return 160.0 + belief.parcel_strike_prob[idx_n] * 240.0 + obs.parcel_insectes(r_n, p_n) * 35.0
        return 150.0

    # 6p. Choix de machine `m_type` sur rayon cible (R8:D SURCHAUFFE_CIBLE_DESTINATION)
    if isinstance(opt, int) and kind_hint == "SURCHAUFFE_CIBLE_DESTINATION":
        dr = int(decision.context.get("ray", 0))
        m_obs = obs.machines[dr * 2 + opt]
        return 160.0 + m_obs.position * 45.0 + (m_obs.rouges + m_obs.bleus) * 45.0 + (30.0 if opt == MACHINE_BULLDOZER else 0.0)

    # 6q. Réduction de Seuil -2 sur tout un rayon `ray` (R9:A)
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

    # 7. Choix d'une case Gardien 1..6 à ouvrir (ex: R5:A) — explicitement gardé par effect_kind
    if isinstance(opt, int) and kind_hint in ("OPEN_GARDIEN", "") and 1 <= opt <= 6:
        if is_b2:
            _, trig_vals = _compute_b2_resource_and_trigger_values(obs, cfg, belief)
            return 200.0 + trig_vals[opt - 1] * 2.0
        return 200.0 + (7 - opt) * 15.0

    return 100.0


def _choose_reve_3_2_policy(
    obs: PlayerObservation,
    cfg: GameConfig,
    decision: DecisionRequest,
    *,
    is_b2: bool,
) -> str:
    """Arbitrage réaliste v6.0 entre BLOQUER (annulation) et AVANCER (saut gauche / Sommeil)."""
    opts = decision.options
    if "AVANCER" not in opts:
        return "BLOQUER"
    if "BLOQUER" not in opts:
        return "AVANCER"

    can_adv = bool(decision.context.get("can_advance", False))
    if not can_adv or obs.tour >= 8:
        # Impossible d'avancer ou Tour 8 (priorité absolue Tour 8 -> 0 intérêt d'avancer)
        return "BLOQUER"

    case_c = int(decision.context.get("case", 1))
    n_def = max(1, int(decision.context.get("n_defenders", 1)))
    m_seats = tuple(int(s) for s in decision.context.get("machine_seats", ()))
    p_max = cfg.p_max

    dest_ctx = decision.context.get("dest_case")
    dest_c: int | None = None
    if isinstance(dest_ctx, int) and 1 <= dest_ctx < case_c:
        dest_c = int(dest_ctx)
    elif cfg.reve_advance_mode == "PAS_A_PAS":
        if case_c >= 2 and obs.reve_at_case(case_c - 1) == 0:
            dest_c = case_c - 1
    else:
        for c2 in range(case_c - 1, 0, -1):
            if obs.reve_at_case(c2) == 0:
                dest_c = c2
                break
    if dest_c is None:
        return "BLOQUER"

    # 1. Valeur d'AVANCER : proximité Sommeil + gain de probabilité min(2D6) sur les tours restants
    total_r = cfg.total_reves_partie
    reves_on = sum(1 for c2 in range(1, TRACK_LEN + 1) if obs.reve_at_case(c2) > 0)
    sommeil_now = False
    if total_r > 0 and reves_on == total_r:
        in_block_after = sum(
            1
            for c2 in range(1, total_r + 1)
            if (c2 == dest_c) or (c2 != case_c and obs.reve_at_case(c2) > 0)
        )
        sommeil_now = in_block_after == total_r

    rem_turns = max(0, 8 - obs.tour)
    jump_span = max(1, case_c - dest_c)
    prob_gain = (_MIN_2D6_PROBS_H[dest_c - 1] - _MIN_2D6_PROBS_H[case_c - 1]) * (
        780.0 if is_b2 else 950.0
    ) * (rem_turns / 7.0)
    advance_val = prob_gain + (32.0 if is_b2 else 45.0) * jump_span

    if sommeil_now:
        # Terminer la partie en 5.3 par Sommeil sauve tous les tours restants !
        advance_val += 680.0 + 190.0 * max(0, 7 - obs.tour)
    elif total_r > 0:
        if reves_on == total_r and case_c > total_r:
            advance_val += (245.0 if is_b2 else 195.0) + 38.0 * jump_span
        elif is_b2:
            # Si tous les Rêves ne sont pas encore construits, n'accorder un fort bonus d'avancée
            # que si le Sommeil reste réaliste dans le temps restant !
            missing_r = max(0, total_r - reves_on)
            if missing_r <= max(0, 6 - obs.tour) and dest_c <= 3:
                advance_val += 110.0
            elif obs.tour <= 5:
                advance_val += 55.0
        elif obs.tour <= 5 and dest_c <= 3:
            advance_val += 125.0
        elif obs.tour <= 6:
            advance_val += 80.0

    # 2. Valeur de BLOQUER : dégâts réels évités + Charge denial sur les min(n_def, len(m_seats)) machines annulées
    is_charge = is_tactique_charge(case_c, obs.tour)
    spec = TACTIQUES_SPEC[case_c]
    n_cancel = len(m_seats) if cfg.reve_activation_mode != "1_DEF_1_MACHINE" else min(n_def, len(m_seats))

    ranked_machines: list[tuple[tuple[int, int, int, int, int], int, int, int]] = []
    for s in m_seats:
        h = obs.hand_of(s)
        if h.card is None or not (1 <= h.card <= 2 * obs.n_players):
            continue
        r_m, mt_m = unpack_machine_card(h.card)
        pos_m, st_m = obs.machine_pos_status(r_m, mt_m)
        active = 1 if (st_m != MACHINE_STATUS_RETIRED and pos_m > 0) else 0
        is_rat = 1 if st_m == MACHINE_STATUS_RATISSAGE else 0
        eff_red = obs.machine_effective_rouges(r_m, mt_m) if active else 0
        ranked_machines.append(((active, is_rat, eff_red, pos_m, -s), r_m, mt_m, pos_m))
    ranked_machines.sort(key=lambda item: item[0], reverse=True)

    block_val = 0.0
    for key_t, r_m, mt_m, pos_m in ranked_machines[:n_cancel]:
        if key_t[0] == 0:
            continue
        eff_red = key_t[2]
        if not is_b2:
            block_val += 165.0 + _tactique_danger(case_c, obs.tour, eff_red) * 1.6
            continue

        # B2 : évaluation fine par cible réelle (paravents ouverts : état exact connu)
        # Si la frappe est déjà parée en forêt, block_val reste bas -> B2 profite d'AVANCER gratuitement !
        # Si la frappe détruit des Arbres debout (0 Repousse Finale) ou charge un jeton Puissance en Acte 1,
        # B2 bloque prioritairement sauf victoire Sommeil immédiate !
        m_obs = obs.machines[r_m * 2 + mt_m]
        rouges_for_seuil = 0 if is_charge else eff_red
        bleus = m_obs.bleus
        would_damage_any = False

        target_ps: list[int] = []
        for c_kind in spec.cibles:
            if c_kind == "SUR_PLACE" and not obs.is_route(r_m, pos_m):
                target_ps.append(pos_m)
            elif c_kind == "DEVANT":
                for p_cand in range(pos_m + 1, p_max + 1):
                    if not obs.is_route(r_m, p_cand):
                        target_ps.append(p_cand)
                        break

        for tp in target_ps:
            defs = obs.parcel_defenseurs(r_m, tp)
            ins = obs.parcel_insectes(r_m, tp)
            tot_def = defs + ins
            piege_armed = obs.parcel_piege(r_m, tp) == PIEGE_ACTIF and tot_def >= 1
            seuil = max(
                1,
                cfg.dotation_arbres[tp - 1]
                + cfg.offset_seuil_parade
                + rouges_for_seuil
                - bleus
                + spec.mod_seuil,
            )
            if piege_armed:
                block_val += 20.0
            elif tot_def >= seuil:
                manque = max(0, seuil - defs)
                block_val += 18.0 + 48.0 * min(ins, manque)
            else:
                arbres = obs.parcel_arbres(r_m, tp)
                souches = obs.parcel_souches(r_m, tp)
                if mt_m == MACHINE_ABATTEUSE:
                    trees_lost = min(2, arbres)
                    if trees_lost > 0:
                        would_damage_any = True
                    block_val += trees_lost * 245.0
                else:
                    trees_lost = min(1, arbres)
                    stumps_lost = souches + trees_lost
                    if trees_lost > 0 or stumps_lost > 0:
                        would_damage_any = True
                    route_pen = 215.0 if (arbres <= 1) else 0.0
                    block_val += trees_lost * 245.0 + route_pen

        if spec.avancee > 0:
            block_val += 80.0
        if is_charge and would_damage_any:
            block_val += 225.0 if obs.tour <= 4 else (105.0 if obs.tour <= 6 else 35.0)

    return "AVANCER" if advance_val > block_val else "BLOQUER"


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

    if dtype == DEC_CHOIX_REVE_3_2:
        return _choose_reve_3_2_policy(obs, cfg, decision, is_b2=is_b2)

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

    if dtype == DEC_COLONIE_A_OPEN:
        if "OUVRIR" in opts:
            case_c = int(decision.context.get("case", 1))
            if obs.gardien_available_at_case(case_c):
                return "OUVRIR"
        return "PASSER" if "PASSER" in opts else opts[0]

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
        # Placer un Gardien Loi ou clé sur les déclencheurs les plus fréquents (1: Parade, 6: Insecte, 4: Résonance, 2: Piège)
        case_weights = {1: 95.0, 6: 88.0, 4: 82.0, 2: 76.0, 5: 68.0, 3: 58.0}
        tid = str(decision.context.get("tile_id", ""))
        if is_b2 and obs.mode >= 3 and tid:
            econ = get_economie_catalog()
            node = econ.get((tid, cfg.profile_for_slot(tid) or "A"))
            if node is not None and node.is_law:
                # Une Loi gagne son marqueur utilisé dès que sa case s'allume -> case 1 ou 4 idéale pour le Réveil !
                case_weights = {1: 110.0, 4: 105.0, 6: 95.0, 2: 85.0, 5: 75.0, 3: 65.0}
        return max(opts, key=lambda c: (case_weights.get(int(c), 50.0), _tiebreak(cfg, obs, int(c), 3)))

    if dtype == DEC_PLACEMENT_NID_3_1:
        def _nid_parcel_sc(rp: tuple[int, int]) -> tuple[float, int]:
            r_n, p_n = int(rp[0]), int(rp[1])
            idx = r_n * MAX_P + (p_n - 1)
            # B2 évite les parcelles directement sur la trajectoire immédiate d'une machine et vise près du cœur (Migration 4.3 !)
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
            # Garder un Piège armé ou une parade vitale sur la parcelle source !
            if (
                obs.parcel_piege(sr, sp) == PIEGE_ACTIF
                and sr_defs == 0
                and sr_ins == 1
            ):
                return ("RESTER",)
            sr_seuil = belief.parcel_expected_seuil[sr_idx]
            if (
                is_b2
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
        total_bugs = sum(obs.tactique_code_bugs_app(c_b)[1] for c_b in range(TRACK_LEN))
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
                if cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B":
                    # Bouclier de lisière : priorité aux Gardiens menacés de perte de pari en 5.3,
                    # rendement décroissant sur les boucliers purement préventifs (rem_bets == 0).
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
                if obs.gardien_available_at_case(c_num):
                    return 560.0 if is_b2 else 500.0
                return 240.0
            if mk == "BUG":
                c_num = int(mv[1])
                t_code, t_bugs, _ = obs.tactique_code_bugs_app(c_num - 1)
                if is_tactique_code(t_code) and t_bugs == 0:
                    # Rendement décroissant après 1-2 Bugs sur la piste des Tactiques
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
                        c_num >= 2 and is_reve_code(obs.tactique_code_bugs_app(c_num - 2)[0])
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
                if (
                    obs.parcel_piege(dr, dp) == PIEGE_ACTIF
                    and d_defs + d_ins == 0
                ):
                    return 575.0
                if belief.parcel_strike_prob[d_idx] >= 0.50 and (d_defs + d_ins) < d_seuil:
                    if (d_defs + d_ins + 1) >= d_seuil:
                        # Complète une Parade classique avec Insecte -> sauve des Arbres + allume 6. Insecte !
                        return 610.0 + (65.0 if g6_bet else 0.0)
                    return 440.0
                if is_b2 and obs.parcel_has_nid(dr, dp) and d_ins == 1:
                    # Passe un Nid au seuil de production +2 Insectes
                    return 420.0
                if (
                    is_b2
                    and obs.parcel_arbres(dr, dp) >= 1
                    and d_ins < 2
                    and _has_frontline_machine(dr, dp)
                ):
                    return 445.0 if total_forest_ins <= n_pl + 1 else 365.0
                if obs.mode >= 2 and src_kind == "FORET" and dp > int(src_p):
                    return 290.0
                return 95.0
            if mk == "FURTIVITE":
                # En Furtivité libre A1, les Insectes ne complètent plus de binôme 4.1 (transit uniquement)
                return 80.0
            # RESTER : valoriser la conservation d'une réserve forestière (soutien Parade, Nid +2, 6. Insecte)
            if is_b2 and src_kind == "FORET":
                sr_r, sp_r = int(src_a), int(src_p)
                cur_ins_r = obs.parcel_insectes(sr_r, sp_r)
                stay_sc = 180.0
                if obs.parcel_has_nid(sr_r, sp_r) and cur_ins_r <= 2:
                    stay_sc += 250.0
                elif (
                    obs.parcel_arbres(sr_r, sp_r) >= 1
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

    if dtype == DEC_RETRAIT_APPRENTISSAGE_6_1:
        # B2 retire en priorité l'Apprentissage de la Tactique en tête menaçant de faire reculer un Rêve
        # ou d'amener T6/T3 vers la gauche (et épargne un Bug si la Tactique tombe à 0 !).
        best_r = opts[0]
        best_r_sc = -1.0
        for opt in opts:
            if opt == "PASSER":
                sc = 0.0
            else:
                r_idx = int(opt)
                t_code, bugs, app = obs.tactique_code_bugs_app(r_idx)
                saves_bug = 95.0 if (app == 1 and bugs > 0) else 0.0
                pushes_reve = (
                    140.0
                    if (r_idx >= 1 and is_reve_code(obs.tactique_code_bugs_app(r_idx - 1)[0]))
                    else 0.0
                )
                danger_t = 75.0 if t_code in (3, 6) else 25.0
                sc = 120.0 + app * 30.0 + (saves_bug + pushes_reve + danger_t if is_b2 else 0.0)
            if sc > best_r_sc:
                best_r_sc, best_r = sc, opt
        return best_r

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


def _play_game_cooperative(
    state: GameState,
    *,
    is_b2: bool,
    k_max_passes: int | None = None,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
) -> GameOver:
    scorer = score_target_b2 if is_b2 else score_target_b1
    chooser = choose_b2 if is_b2 else choose_b1
    steps = 0

    while True:
        steps += 1
        if steps > max_steps:
            cfg = state.cfg
            raise RuntimeError(
                f"Garde-fou max_steps={max_steps} dépassé ({'B2' if is_b2 else 'B1'}) : "
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
