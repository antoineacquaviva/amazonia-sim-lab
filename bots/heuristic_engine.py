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
    TRACK_LEN,
    GameConfig,
    GameState,
    PlayerObservation,
    is_reve_code,
    is_tactique_code,
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

# Courbe temporelle de RES_DILUTION_SABOTAGE (Tours 1..8) :
# forte aux Tours 1..5 (nombreux remélanges 6.3 restants), faible au Tour 7, nulle au Tour 8.
_SABOTAGE_TOUR_WEIGHT: tuple[float, ...] = (
    95.0,  # index 0 (inutilisé)
    95.0,  # Tour 1
    88.0,  # Tour 2
    78.0,  # Tour 3
    68.0,  # Tour 4
    56.0,  # Tour 5
    32.0,  # Tour 6
    12.0,  # Tour 7
    2.0,   # Tour 8 (uniquement déclencheur 3 résiduel, 0 remélange futur)
)


@dataclass(frozen=True, slots=True)
class EconomieNode:
    """Nœud immuable du graphe orienté `economie_bot` extrait de spec_bundle_v5_3_1.json."""

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
    """Charge une seule fois le graphe orienté `economie_bot` depuis `data/spec_bundle_v5_4.json`."""
    if _EconomieStore.cache is not None:
        return _EconomieStore.cache

    spec_path = Path(__file__).resolve().parent.parent / "data" / "spec_bundle_v5_4.json"
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
        "RES_ARBRE": 95.0 + 6.0 * fragile_parcels,
        "RES_SOUCHE": 42.0 + (18.0 if tour >= 6 else 6.0),
        "RES_DEFENSEUR": 68.0 + 4.0 * fragile_parcels,
        "RES_PIEGE": 76.0 + 3.5 * total_rouges,
        "RES_INSECTE": 52.0 if total_insects < 2 * n else 34.0,
        "RES_SEUIL_PARADE": 62.0 + 4.0 * fragile_parcels,
        "RES_JETON_BLEU": 64.0 + (22.0 if tour <= 6 else 8.0),
        "RES_JETON_ROUGE": 58.0 + 4.0 * max(0, 8 - tour),
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
        # En v5.4, TOUTES les tuiles Rêves en jeu (2 ou 4) doivent être construites et groupées en tête !
        reves_on_track = sum(1 for t in obs.piste_tactiques if is_reve_code(t.code))
        target_reves = max(1, cfg.total_reves_partie)
        if reves_on_track < target_reves:
            struct_v = 195.0 if reves_on_track == 0 else (165.0 if reves_on_track + 1 == target_reves else 145.0)
        else:
            struct_v = 85.0
        if tour >= 7 and reves_on_track < target_reves - 1:
            struct_v *= 0.45
    elif fam == FAMILLE_CROISSANCE:
        struct_v = 165.0 if tour <= 5 else 90.0
    else:
        g_on_track = sum(1 for g in obs.piste_gardiens if g.gardien_num > 0)
        struct_v = 160.0 if (obs.gardien_pari_enabled and g_on_track < 2) else 105.0

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
) -> tuple[float, float, float, float, float, float]:
    """Estime le nombre attendu de déclencheurs sur les cases 1..6 (strictement sur PlayerObservation).

    Partition stricte v5.4.6 (« 1 événement = au plus 1 déclencheur ») :
    - 3.2 : 3. Sabotage (carte Sabotage révélée) > 6. Insecte (déviation Bug) > 5. Rêve (dé M sur Rêve, avec ou sans Défenseur).
    - 4.1 Furtivité : n'allume plus ni 2. Piégeage ni 3. Sabotage.
    - 4.2 Nids : +1/+2 Insectes -> 6. Insecte.
    - 5.1/5.2 : 2. Piégeage (Piège armé) > 6. Insecte (Parade classique défaussant >=1 Insecte) > 1. Parade (Défenseurs seuls).
    - 4. Gardien (indice 3) : calculé dynamiquement dans `_score_gardien_pari` selon `gardien_4_trigger_mode`.
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
            defs = obs.parcel_defenseurs(r, p)
            ins = obs.parcel_insectes(r, p)
            cur_def = defs + ins
            piege_armed = obs.parcel_piege(r, p) == PIEGE_ACTIF and cur_def >= 1
            seuil_e = belief.parcel_expected_seuil[idx]
            if piege_armed:
                # 2. Piégeage uniquement (jamais 1. Parade)
                exp_piege += min(1.35, s_prob)
            elif defs >= seuil_e:
                # 1. Parade uniquement (Défenseurs seuls, sans dépense d'Insecte)
                exp_parade += min(1.35, s_prob)
            elif cur_def >= seuil_e and ins >= 1:
                # 6. Insecte uniquement (Parade classique défaussant >= 1 Insecte)
                exp_insecte += min(1.35, s_prob)
            elif defs >= seuil_e - 0.5 and defs >= 1 and ins == 0:
                exp_parade += 0.45 * min(1.0, s_prob)
            elif cur_def >= seuil_e - 0.5 and ins >= 1:
                exp_insecte += 0.45 * min(1.0, s_prob)

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
            # On ne dévie pas hors d'un Rêve sauf nécessité -> 5. Rêve garanti (avec ou sans Défenseur dessus)
            exp_reve += 0.95
        elif own_bugs >= 1:
            # Un Bug présent sur notre rang M peut dévier le dé -> allume 6. Insecte (et non 5. Rêve)
            exp_insecte += 0.80

    # Espérance prudente pour les (n - 1) autres sièges (strictement sur information publique)
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
        exp_sabotage += 0.72 * min(float(sab_others), float(n - 1) * p_other_sab)

    # Rêves présents sur la piste fixe T1..T6 : allument 5. Rêve même sans Défenseur sur le Rêve !
    n_reves_on_track = sum(1 for c_r in range(1, TRACK_LEN + 1) if obs.reve_at_case(c_r) > 0)
    if n_reves_on_track > 0:
        p_other_mach = max(0.0, 1.0 - p_other_sab)
        exp_reve += 0.70 * float(n - 1) * p_other_mach * (n_reves_on_track / 6.0)

    # Bugs présents sur la piste Tactiques (hors Rêves) pouvant dévier les autres machines -> 6. Insecte
    if bug_b_active:
        n_bug_ranks = sum(
            1
            for c_b in range(1, TRACK_LEN + 1)
            if obs.reve_at_case(c_b) == 0 and obs.tactique_code_bugs_app(c_b - 1)[1] >= 1
        )
        if n_bug_ranks > 0:
            p_other_mach = max(0.0, 1.0 - p_other_sab)
            exp_insecte += 0.50 * min(
                float(n_bug_ranks), float(n - 1) * p_other_mach * (n_bug_ranks / 6.0)
            )

    # 3) Étape 4.2 : Nids portant >= 1 Défenseur produisent des Insectes -> 6. Insecte
    for r in range(n):
        for p in range(1, p_max + 1):
            if obs.parcel_has_nid(r, p) and obs.parcel_defenseurs(r, p) >= 1:
                exp_insecte += 1.0

    # 4) Bonus Colonie 4.3 : uniquement actif sous SLOT_COLONISATION_GARDIENS == 'A'
    #    (sous profil 'B' Bouclier de lisière, l'Insecte protège en 5.3 mais n'ouvre pas le Gardien)
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
    """Évalue la cible `('GARDIEN_PARI', case_c)` en 2.2 (strictement sur PlayerObservation).

    Règle v5.4.6 :
    - Plafond de pari `gardien_bet_cap_policy` (`UNIFORM_MAX_2` : max 2/Gardien cases 1..6) et Éveil
      de la Forêt 100 % Piste des Gardiens (les N Défenseurs sur la Piste des Gardiens).
    - 5. Rêve est désormais utilisable durant un Éveil (allumé par tout dé M non dévié sur un Rêve).
    - 4. Gardien suit `gardien_4_trigger_mode` (`DISTINCT_OPEN_1` ou `DISTINCT_WON_2`).
    - À 3J-4J, B2 ne force pas l'Éveil lorsque la survie normale offre une meilleure espérance d'Arbres.
    """
    if not obs.gardien_pari_enabled or not obs.gardien_present_at_case(case_c):
        return 0.0

    own_pari_case = obs.player_def2_gardien_pari_case(obs.observer_seat)
    allies_on_case = max(
        0, obs.gardien_pari_defenders(case_c) - (1 if own_pari_case == case_c else 0)
    )
    cap_case = cfg.gardien_bet_cap_for_case(case_c)
    if allies_on_case >= cap_case:
        return 0.0

    exp_trigs = _estimate_expected_gardien_triggers(obs, cfg, belief)
    n = obs.n_players
    allies_g = max(0, obs.total_gardien_pari_defenders() - (1 if own_pari_case > 0 else 0))
    unplaced_allies = max(0, (n - 1) - allies_g)
    colonie_is_a = cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "A"
    colonie_is_b = cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"

    # Capacité physique totale sur les Gardiens construits et capacité attendue hors case 4
    total_slots_cap = 0
    total_non_res_cap = 0.0
    distinct_other_cap = 0.0
    distinct_other_bet_exp = 0.0
    distinct_other_won_exp = 0.0
    has_other_empty_supported = False
    for c_k in (1, 2, 3, 5, 6):
        if obs.gardien_present_at_case(c_k):
            cap_k_phys = cfg.gardien_bet_cap_for_case(c_k)
            total_slots_cap += cap_k_phys
            t_k = exp_trigs[c_k - 1]
            cap_k = min(float(cap_k_phys), t_k)
            total_non_res_cap += cap_k
            distinct_other_cap += min(1.0, t_k)
            bets_k = max(
                0, obs.gardien_pari_defenders(c_k) - (1 if own_pari_case == c_k else 0)
            )
            if bets_k >= 1:
                distinct_other_bet_exp += min(1.0, t_k)
                if t_k >= float(bets_k) - 0.25:
                    distinct_other_won_exp += 1.0
                elif t_k >= float(bets_k) - 0.55:
                    distinct_other_won_exp += 0.5
            elif c_k != case_c and t_k >= 0.85:
                has_other_empty_supported = True

    has_res = obs.gardien_present_at_case(4)
    cap_4 = cfg.gardien_bet_cap_for_case(4)
    if has_res:
        total_slots_cap += cap_4
    col4_bonus = 0.85 if (colonie_is_a and obs.piste_colonie[3] >= 1) else 0.0
    if cfg.gardien_4_trigger_mode == "DISTINCT_WON_2":
        res_cap = min(float(cap_4), max(0.0, distinct_other_cap - 1.0) + col4_bonus) if has_res else 0.0
    else:  # "DISTINCT_OPEN_1"
        res_cap = min(float(cap_4), distinct_other_cap + col4_bonus) if has_res else 0.0
    total_gardien_cap = total_non_res_cap + res_cap

    if case_c == 4:
        if cfg.gardien_4_trigger_mode == "DISTINCT_WON_2":
            potential_won = min(
                distinct_other_cap, distinct_other_won_exp + 0.70 * unplaced_allies
            )
            exp_for_case = max(0.0, potential_won - 1.0) + col4_bonus
        else:  # "DISTINCT_OPEN_1"
            potential_open = min(
                distinct_other_cap, distinct_other_bet_exp + 0.80 * unplaced_allies
            )
            exp_for_case = potential_open + col4_bonus
    else:
        exp_for_case = exp_trigs[case_c - 1]

    needed_triggers = allies_on_case + 1

    # Ratio d'Arbres actuel et pression machine (pour décider si l'Éveil bat la survie normale à 3J-4J)
    total_init = max(1, n * sum(cfg.dotation_arbres))
    cur_arbres = sum(
        obs.parcel_arbres(r, p) for r in range(n) for p in range(1, cfg.p_max + 1)
    )
    tree_ratio = cur_arbres / total_init

    bouclier_safety = (
        22.0 if (colonie_is_b and obs.piste_colonie[case_c - 1] >= 1) else 0.0
    )

    supported = exp_for_case >= (float(needed_triggers) - 0.20)
    marginally_supported = exp_for_case >= (float(needed_triggers) - 0.50)
    eveil_feasible = (
        obs.tour <= 7
        and total_slots_cap >= n
        and total_gardien_cap >= (n - 0.45)
    )

    # Calibration B2 à 3J-4J : ne pas forcer l'Éveil quand la survie normale offre une meilleure espérance d'Arbres
    eveil_value_mult = 1.0
    if is_b2 and n <= 4:
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
        high_pressure = total_rat >= 1 or total_red >= (n + 2) or obs.tour >= 6
        if obs.tour <= 3 and not high_pressure and tree_ratio < 0.88:
            # Trop tôt à 3J-4J : développer la forêt/défendre rapporte davantage d'Arbres
            eveil_feasible = False
        elif tree_ratio < 0.62 and obs.tour <= 5 and not high_pressure:
            # Forêt déjà entamée mais encore temps de stabiliser et profiter de la Repousse Finale
            eveil_feasible = False
        elif allies_g == 0 and exp_for_case < (float(needed_triggers) + 0.05) and not high_pressure:
            # Ne pas initier un Éveil spéculatif à 3J-4J sans certitude solide
            eveil_feasible = False
        else:
            # Compétition loyale avec la défense de parcelle vitale (évite de sacrifier des Arbres)
            eveil_value_mult = 0.78 if (not high_pressure and obs.tour <= 5) else 0.94

    # 1. Opportunité d'Éveil de la Forêt 100 % Piste des Gardiens (Tours 1..7)
    if eveil_feasible:
        eveil_penalty = 0.0
        # Privilégier d'abord les cases motrices (1,2,3,5,6) avant 4. Gardien s'il en reste à alimenter
        if (
            case_c == 4
            and (
                (
                    cfg.gardien_4_trigger_mode == "DISTINCT_WON_2"
                    and distinct_other_won_exp < (float(needed_triggers) + 0.85)
                )
                or (
                    cfg.gardien_4_trigger_mode == "DISTINCT_OPEN_1"
                    and distinct_other_bet_exp < (float(needed_triggers) - 0.15)
                )
            )
            and distinct_other_cap > distinct_other_bet_exp + 0.35
        ):
            eveil_penalty += 45.0
        # Préférence pour répartir sur des Gardiens distincts avant d'empiler un 2e pari
        # (d'autant plus crucial sous DISTINCT_OPEN_1 et DISTINCT_WON_2 !)
        if allies_on_case >= 1 and has_other_empty_supported:
            eveil_penalty += 38.0

        margin_bonus = 18.0 * max(0.0, min(1.5, exp_for_case - float(needed_triggers)))

        if supported:
            if allies_g >= n - 1:
                base = (650.0 + 250.0 * tree_ratio) if is_b2 else (580.0 + 195.0 * tree_ratio)
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
            if allies_g >= 1:
                prog = allies_g / max(1, n - 1)
                base = (
                    (475.0 + 165.0 * prog + 170.0 * tree_ratio)
                    if is_b2
                    else (420.0 + 130.0 * prog + 135.0 * tree_ratio)
                )
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
            if belief.drew_sabotage_or_none or total_gardien_cap >= (n + 0.15) or obs.tour >= 4:
                base = (400.0 + 175.0 * tree_ratio) if is_b2 else (350.0 + 145.0 * tree_ratio)
                return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)
        elif marginally_supported and allies_g >= n - 1:
            base = (510.0 + 180.0 * tree_ratio) if is_b2 else (455.0 + 145.0 * tree_ratio)
            return max(40.0, base * eveil_value_mult + margin_bonus + bouclier_safety - eveil_penalty)

    # 2. Jeu courant : pari prudent en Mode 3/4 uniquement si l'activation est probable
    if obs.mode >= 3:
        if exp_for_case >= (float(needed_triggers) + 0.10):
            g_face = obs.gardien_face_at_case(case_c)
            face_bonus = 45.0 if g_face == 1 else 15.0
            return (275.0 if is_b2 else 240.0) + face_bonus + bouclier_safety
        if supported:
            return (165.0 if is_b2 else 145.0) + bouclier_safety
        return 25.0

    # En Mode 2 (Gardiens neutres), hors opportunité d'Éveil, éviter tout pari inutile/risqué
    return 20.0


def _score_reve_activation(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    case_c: int,
    *,
    is_b2: bool,
) -> float:
    """Évalue la cible `('REVE_ACTIVATION', case_c)` en 2.2 (strictement sur PlayerObservation)."""
    if obs.reve_at_case(case_c) <= 0:
        return 0.0

    own_hand = obs.hand_of(obs.observer_seat)
    own_card = own_hand.card
    own_hits_reve = (
        own_card is not None and 1 <= own_card <= 12 and own_hand.lecture_m == case_c
    )

    cancel_val = 0.0
    if own_hits_reve and own_card is not None:
        ray = (own_card - 1) // 2
        m_type = (own_card - 1) % 2
        pos, st = obs.machine_pos_status(ray, m_type)
        is_active = st != MACHINE_STATUS_RETIRED and pos > 0
        if is_active:
            eff_red = obs.machine_effective_rouges(ray, m_type)
            # T4..T6 (+1 rouge, seuil -1/-2) et T3/T6 (double frappe + avance) sont très menaçantes
            cancel_val = 140.0 + 55.0 * eff_red + 35.0 * case_c
        else:
            cancel_val = 30.0

    if cfg.reve_advance_mode == "FREE_SLOT_ONLY":
        can_advance = case_c > 1 and obs.reve_at_case(case_c - 1) == 0
    else:
        can_advance = any(obs.reve_at_case(c2) == 0 for c2 in range(1, case_c))
    advance_val = (185.0 if is_b2 else 155.0) if can_advance else 25.0

    # Bonus de victoire imminente par Sommeil si tous les Rêves sont sur la piste et à 1 cran du bloc
    total_r = cfg.total_reves_partie
    if can_advance and total_r > 0:
        reves_on_track = sum(1 for c2 in range(1, TRACK_LEN + 1) if obs.reve_at_case(c2) > 0)
        if reves_on_track == total_r:
            gaps_before_block = sum(
                1 for c2 in range(1, total_r + 1) if obs.reve_at_case(c2) == 0
            )
            if gaps_before_block == 1:
                advance_val += 260.0

    total_on_case = obs.reve_activation_defenders(case_c)
    own_reve_case = obs.player_def2_reve_case(obs.observer_seat)
    allies = max(0, total_on_case - (1 if own_reve_case == case_c else 0))

    act_mode = cfg.reve_activation_mode
    if act_mode == "1_DEF_1_MACHINE":
        if own_hits_reve:
            if cfg.reve_advance_mode == "CLEAR_RANK_ONLY":
                # En CLEAR_RANK_ONLY, le Rêve n'avance que si TOUTES les machines du rang sont annulées :
                # notre Défenseur reste indispensable pour vider le rang même si des alliés y sont déjà,
                # mais la probabilité d'avancée dépend des autres sièges non couverts.
                uncovered_others = max(0, (obs.n_players - 1) - allies)
                prob_clear = max(0.25, (1.0 - 0.14) ** uncovered_others)
                adv_contrib = advance_val * prob_clear
            else:
                adv_contrib = advance_val if allies == 0 else (0.25 * advance_val)
            return 260.0 + cancel_val + adv_contrib
        return 45.0

    if act_mode == "1_DEF_ALL_RANK":
        if allies >= 1:
            # Un allié couvre déjà tout ce rang M : rediriger notre Défenseur ailleurs !
            return 25.0
        if own_hits_reve:
            return 300.0 + cancel_val + advance_val
        return 55.0

    # BINOME_ALL_RANK
    if allies >= 2:
        return 20.0
    if allies == 1:
        if own_hits_reve:
            return 350.0 + cancel_val + advance_val
        if belief.drew_sabotage_or_none:
            return 240.0 + advance_val
        return 175.0 + 0.7 * advance_val
    # allies == 0
    if own_hits_reve:
        return 250.0 + 0.8 * cancel_val + 0.85 * advance_val
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
        # Parer une frappe attendue (exactement sur la marge du seuil ou en soutien d'insectes)
        if s_prob > 0.08 and cur_def < seuil_e:
            gap = seuil_e - cur_def
            reach_mult = 1.0 if gap <= 1.25 else (0.58 if gap <= 2.25 else 0.25)
            urgency = 580.0 * min(1.6, s_prob) * reach_mult
            # Danger vital de création de Route Forestière (0/0) par Bulldozer ou dernier Arbre
            if arbres <= 1 and (belief.parcel_bulldo_prob[idx] > 0.15 or souches == 0):
                urgency += 175.0 * min(1.2, s_prob)
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
        nb_d, f_ins = obs.furtivite_defs_and_ins(l_i, p_i)
        t_ray = l_i if rv == 0 else (l_i + 1) % obs.n_players
        idx = t_ray * MAX_P + (p_i - 1)

        has_m = any(
            obs.machine_pos_status(t_ray, mt)[0] == p_i
            and obs.machine_pos_status(t_ray, mt)[1] != MACHINE_STATUS_RETIRED
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        partner_ready = (nb_d == 1) or (f_ins >= 1)
        useful_trap = (not has_m) and obs.parcel_piege(t_ray, p_i) == PIEGE_AUCUN
        # Un Sabotage 4.1 ne passe que si la machine présente n'est PAS en Siège et a une chance d'être inactive
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
            base_f = 545.0 if useful_trap else 515.0
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


def score_target_b2(
    obs: PlayerObservation,
    cfg: GameConfig,
    belief: BeliefSummary,
    target: tuple[Any, ...],
    is_first_defender: bool,
) -> float:
    """Évaluation B2 (`k=2`) : graphe orienté `economie_bot` (12 `RES_*`, `TRIG_1..6`) + lookahead 5.1->6.2."""
    _ = is_first_defender
    res_val, trig_vals = _compute_b2_resource_and_trigger_values(obs, cfg, belief)
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        r_i, p_i = int(r), int(p)
        idx = r_i * MAX_P + (p_i - 1)
        defs = obs.parcel_defenseurs(r_i, p_i)
        ins = obs.parcel_insectes(r_i, p_i)
        cur_def = defs + ins
        s_prob = belief.parcel_strike_prob[idx]
        seuil_e = belief.parcel_expected_seuil[idx]
        arbres = obs.parcel_arbres(r_i, p_i)
        souches = obs.parcel_souches(r_i, p_i)

        score = 90.0
        trig_1_v = trig_vals[0]  # 1. Parade (Défenseurs seuls)
        trig_2_v = trig_vals[1]  # 2. Piégeage (frappe bloquée par Piège)
        trig_6_v = trig_vals[5]  # 6. Insecte (Nid / Parade avec dépense d'Insecte)

        # 1. Armement d'un Piège Embuscade : pare n'importe quel Seuil + épargne les Insectes + allume 2. Piégeage
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and cur_def == 0:
            saved_ins_v = min(3, ins) * res_val["RES_INSECTE"] * 0.4
            piege_bet_bonus = 95.0 if obs.gardien_pari_defenders(2) >= 1 else 0.0
            score += 410.0 + s_prob * (310.0 + trig_2_v + saved_ins_v + piege_bet_bonus)

        # 2. Activation d'un Nid en 4.2 : produit +1/+2 Insectes + TRIG_6 + pouvoir du Nid
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            prod_cnt = 1 if ins <= 1 else 2
            score += 360.0 + prod_cnt * res_val["RES_INSECTE"] + 0.85 * trig_6_v

        # 3. Lookahead 5.1 -> 6.2 sur les dégâts évités (Arbres, Route 0/0 et déclencheur 1. Parade ou 6. Insecte)
        if s_prob > 0.05:
            piege_armed = obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF and cur_def >= 1
            if not piege_armed and cur_def < seuil_e:
                gap = seuil_e - cur_def
                # Partition 5.1 : si defs+1 >= seuil_e -> 1. Parade ; sinon (dépense d'Insecte) -> 6. Insecte
                parade_trig_v = trig_1_v if (defs + 1 >= seuil_e) else trig_6_v
                if gap <= 1.25:
                    expected_trees_saved = min(2.0, float(max(1, arbres)))
                    route_catastrophe = (
                        220.0
                        if (arbres <= 1 and (belief.parcel_bulldo_prob[idx] > 0.12 or souches == 0))
                        else 0.0
                    )
                    app_denial = 0.75 * res_val["RES_APPRENTISSAGE"]
                    score += s_prob * (
                        expected_trees_saved * res_val["RES_ARBRE"] * 2.4
                        + route_catastrophe
                        + app_denial
                        + 0.8 * parade_trig_v
                    )
                elif gap <= 2.25:
                    # Premier pilier d'une défense à 2 pions (signal de coordination vers le voisin)
                    score += s_prob * (230.0 + 0.45 * res_val["RES_ARBRE"])
            elif not piege_armed and cur_def >= seuil_e and ins > 0 and defs < seuil_e:
                # Épargner 1 Insecte qui aurait été défaussé par la parade classique !
                score += s_prob * (0.85 * res_val["RES_INSECTE"])

        # Valeur de Repousse Finale de préserver au moins 1 Souche hors Route
        if arbres == 0 and souches >= 1 and belief.parcel_bulldo_prob[idx] > 0.15 and cur_def < seuil_e:
            score += belief.parcel_bulldo_prob[idx] * 210.0

        return score

    if kind == "LISIERE":
        _, slot_idx = target
        s_idx = int(slot_idx)
        if obs.mode < 2 or s_idx >= 2 * obs.n_players:
            return 0.0
        tile_id, st_l, constructors = obs.lisiere_tile_info(s_idx)
        if st_l != LISIERE_UNCONSTRUCTED:
            return 0.0

        tile_v = _score_tile_construction_b2(obs, cfg, tile_id, res_val, trig_vals)
        # Bonus à N=3 : 1 bâtisseur sera libéré immédiatement en forêt en 3.1 !
        lib_bonus = 0.45 * res_val["RES_DEFENSEUR"] if obs.n_players == 3 else 0.0
        if constructors == 1:
            return 470.0 + tile_v * 1.25 + lib_bonus
        if belief.drew_sabotage_or_none:
            return 390.0 + tile_v * 1.15 + lib_bonus
        return 185.0 + tile_v * 0.90 + lib_bonus

    if kind == "FURTIVITE":
        _, l_idx, p, rive = target
        l_i, p_i, rv = int(l_idx), int(p), int(rive)
        nb_d, f_ins = obs.furtivite_defs_and_ins(l_i, p_i)
        t_ray = l_i if rv == 0 else (l_i + 1) % obs.n_players
        idx = t_ray * MAX_P + (p_i - 1)

        has_m = any(
            obs.machine_pos_status(t_ray, mt)[0] == p_i
            and obs.machine_pos_status(t_ray, mt)[1] != MACHINE_STATUS_RETIRED
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        has_siege = any(
            obs.machine_pos_status(t_ray, mt) == (p_i, MACHINE_STATUS_RATISSAGE)
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
        partner_ready = (nb_d == 1) or (f_ins >= 1)

        action_v = 0.0
        if not has_m and obs.parcel_piege(t_ray, p_i) == PIEGE_AUCUN:
            # 4.1 Préparer un Piège en amont (n'allume plus 2. Piégeage en 4.1, mais prépare 2. Piégeage en 5.1 !)
            m_approaching = any(
                obs.machine_pos_status(t_ray, mt)[1] != MACHINE_STATUS_RETIRED
                and 0 < obs.machine_pos_status(t_ray, mt)[0] < p_i
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
            )
            s_future = 1.0 + 0.8 * belief.parcel_strike_prob[idx] + (0.45 if m_approaching else 0.0)
            prep_trig2 = (0.45 * trig_vals[1]) if (obs.gardien_present_at_case(2) and obs.tour <= 6) else 0.0
            action_v = res_val["RES_PIEGE"] * s_future + prep_trig2
        elif has_m and not has_siege:
            # 4.1 Saboter le chantier (n'allume plus 3. Sabotage en 4.1, mais dilue le paquet pour futurs 3.2 !)
            p_inactive = max(0.0, 1.0 - min(1.0, belief.parcel_strike_prob[idx]))
            prep_trig3 = (0.35 * trig_vals[2]) if (obs.gardien_present_at_case(3) and obs.tour <= 6) else 0.0
            action_v = p_inactive * (res_val["RES_DILUTION_SABOTAGE"] * 1.45 + prep_trig3)

        if action_v <= 5.0:
            return 85.0
        if partner_ready:
            return 415.0 + action_v * 1.35
        if belief.drew_sabotage_or_none:
            return 320.0 + action_v * 1.15
        return 145.0 + action_v * 0.75

    if kind == "GARDIEN_PARI":
        _, case_c = target
        return _score_gardien_pari(obs, cfg, belief, int(case_c), is_b2=True)

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        return _score_reve_activation(obs, cfg, belief, int(case_c), is_b2=True)

    return 0.0


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
            # Préférer T1/T2 (douces) à T6/T3/T4/T5 (violentes)
            return 150.0 + (_TACTIQUE_DANGER[old_code] - _TACTIQUE_DANGER[new_code]) * 4.0
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
        d_m = -1 if opt == "M_MOINS_1" else 1
        new_m = max(1, min(6, old_m + d_m))
        old_c, _, _ = obs.tactique_code_bugs_app(old_m - 1)
        new_c, _, _ = obs.tactique_code_bugs_app(new_m - 1)
        bet6_bonus = 260.0 if (is_b2 and obs.gardien_pari_defenders(6) >= 1) else 0.0
        bet5_pen = -320.0 if (is_b2 and is_reve_code(old_c) and obs.gardien_pari_defenders(5) >= 1) else 0.0
        if is_reve_code(new_c) and not is_reve_code(old_c):
            return 760.0 + bet6_bonus
        if is_reve_code(old_c) and not is_reve_code(new_c):
            return -200.0 + bet5_pen
        if is_tactique_code(old_c) and is_tactique_code(new_c):
            return 35.0 + (_TACTIQUE_DANGER[old_c] - _TACTIQUE_DANGER[new_c]) * 4.0 + bet6_bonus
        return 20.0 + bet6_bonus + bet5_pen

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
        if src_kind == "FORET":
            sr, sp = int(src_a), int(src_p)
            sr_idx = sr * MAX_P + (sp - 1)
            # Garder un Piège armé ou une parade vitale sur la parcelle source !
            if (
                obs.parcel_piege(sr, sp) == PIEGE_ACTIF
                and obs.parcel_defenseurs(sr, sp) == 0
                and obs.parcel_insectes(sr, sp) == 1
            ):
                return ("RESTER",)
            if (
                is_b2
                and belief.parcel_strike_prob[sr_idx] >= 0.85
                and obs.parcel_defenseurs(sr, sp) + obs.parcel_insectes(sr, sp)
                == int(belief.parcel_expected_seuil[sr_idx])
            ):
                return ("RESTER",)

        def _mig_sc(mv: tuple[Any, ...]) -> float:
            mk = mv[0]
            if mk == "COLONIE":
                c_num = int(mv[1])
                if cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B":
                    # Bouclier de lisière : en 4.3, protéger en priorité les Gardiens menacés de perte
                    # de pari en 5.3 (surtout cases 3 et 5 dont la fenêtre 3.2 est déjà passée !).
                    has_g = obs.gardien_present_at_case(c_num)
                    rem_bets = obs.gardien_pari_defenders(c_num)
                    cur_col = obs.piste_colonie[c_num - 1]
                    if has_g and rem_bets >= 1 and cur_col == 0:
                        if c_num in (3, 5):
                            return 640.0 if is_b2 else 560.0
                        return 510.0 if is_b2 else 460.0
                    if has_g and cur_col == 0:
                        return 345.0 if is_b2 else 280.0
                    return 135.0
                if obs.gardien_available_at_case(c_num):
                    return 560.0 if is_b2 else 500.0
                return 240.0
            if mk == "BUG":
                c_num = int(mv[1])
                t_code, t_bugs, _ = obs.tactique_code_bugs_app(c_num - 1)
                if is_tactique_code(t_code) and t_bugs == 0:
                    # B2 cible en priorité les Tactiques dangereuses (T6, T3) ou placées juste à droite d'un Rêve !
                    right_of_reve = (
                        c_num >= 2 and is_reve_code(obs.tactique_code_bugs_app(c_num - 2)[0])
                    )
                    danger_b = 110.0 if t_code in (3, 6) else 45.0
                    return 410.0 + danger_b + (95.0 if (is_b2 and right_of_reve) else 0.0)
                return 190.0
            if mk == "FORET":
                dr, dp = int(mv[1]), int(mv[2])
                d_idx = dr * MAX_P + (dp - 1)
                if (
                    obs.parcel_piege(dr, dp) == PIEGE_ACTIF
                    and obs.parcel_defenseurs(dr, dp) + obs.parcel_insectes(dr, dp) == 0
                ):
                    return 520.0
                if belief.parcel_strike_prob[d_idx] >= 0.75 and (
                    obs.parcel_defenseurs(dr, dp) + obs.parcel_insectes(dr, dp)
                    < belief.parcel_expected_seuil[d_idx]
                ):
                    return 390.0
                if obs.mode >= 2 and src_kind == "FORET" and dp > int(src_p):
                    return 310.0
                return 95.0
            if mk == "FURTIVITE":
                fl, fp = int(mv[1]), int(mv[2])
                nb_d, f_ins = obs.furtivite_defs_and_ins(fl, fp)
                return 260.0 if (nb_d == 1 and f_ins == 0) else 90.0
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
