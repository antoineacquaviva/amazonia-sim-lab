"""Bot Baseline B0 (Réflexe, K_max = 0) — 100 % stdlib PyPy 3.11, isolation stricte v6.1."""

from __future__ import annotations

from typing import Any

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
    DEC_ORDRE_CONSTRUCTION_3_1,
    DEC_PLACEMENT_NID_3_1,
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    DEC_REPTILE_POSE_CROC_3_2,
    DEC_REVISION_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import DecisionRequest, GameOver
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
    GARDIEN_BET_CAP,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_P,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PLUME_CALME,
    PLUME_CHAUD,
    PLUME_KIND_RAY,
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
    HandObs,
    PlayerObservation,
    is_reve_code,
    is_tactique_code,
    machine_threat_key_3_2,
    unpack_machine_card,
)

__all__ = (
    "BotB0",
    "choose_b0",
    "play_game_b0",
)


def _tiebreak_u64(cfg: GameConfig, obs: PlayerObservation, opt_idx: int) -> int:
    """Bris d'égalité déterministe sans biais de siège 0 via rng.py (zéro accès `_buf`)."""
    salt = (obs.step * 31 + opt_idx) & 0xFFFFFFFF
    return rand_u64(
        cfg.exp_seed,
        cfg.rep_id,
        SRC_BOT_TIEBREAK,
        obs.tour,
        obs.observer_seat,
        salt,
    )


def _compute_threat_and_machine_masks(
    obs: PlayerObservation,
    cfg: GameConfig,
    own_hand: HandObs,
) -> tuple[int, int]:
    """Calcule en entier 30 bits (zéro allocation) les masques de menaces connues et de machines."""
    threat_mask = 0
    machine_mask = 0
    n = obs.n_players
    p_max = cfg.p_max

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                bit = 1 << (r * MAX_P + (pos - 1))
                machine_mask |= bit
                if st == MACHINE_STATUS_RATISSAGE:
                    threat_mask |= bit

    if own_hand.card is not None and 1 <= own_hand.card <= 2 * n:
        ray, m_type = unpack_machine_card(own_hand.card)
        lec_m = own_hand.lecture_m
        if lec_m is not None and 1 <= lec_m <= 6:
            t_code, _ = obs.tactique_code_bugs(lec_m - 1)
            # Sous un Rêve sans Défenseur (inactif), la machine exécute la Tactique imprimée T{lec_m}
            if is_reve_code(t_code) and obs.reve_activation_defenders(lec_m) == 0:
                t_code = lec_m
            if is_tactique_code(t_code):
                pos, st = obs.machine_pos_status(ray, m_type)
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    spec = TACTIQUES_SPEC[t_code]
                    for c_kind in spec.cibles:
                        if c_kind == "SUR_PLACE":
                            if not obs.is_route(ray, pos):
                                threat_mask |= 1 << (ray * MAX_P + (pos - 1))
                        elif c_kind == "DEVANT":
                            for p_cand in range(pos + 1, p_max + 1):
                                if not obs.is_route(ray, p_cand):
                                    threat_mask |= 1 << (ray * MAX_P + (p_cand - 1))
                                    break

    return threat_mask, machine_mask


def _active_machine_mask(obs: PlayerObservation) -> int:
    mask = 0
    for r in range(obs.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st = obs.machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                mask |= 1 << (r * MAX_P + (pos - 1))
    return mask


def _ray_ratissage_count(obs: PlayerObservation, ray: int) -> int:
    cnt = 0
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st = obs.machine_pos_status(ray, mt)
        if st == MACHINE_STATUS_RATISSAGE and pos > 0:
            cnt += 1
    return cnt


def _ray_has_untrapped_parcel(obs: PlayerObservation, cfg: GameConfig, ray: int) -> bool:
    for p in range(1, cfg.p_max + 1):
        if not obs.is_route(ray, p) and obs.parcel_piege(ray, p) == PIEGE_AUCUN:
            return True
    return False


def _score_defender_target(
    obs: PlayerObservation,
    cfg: GameConfig,
    target: tuple[Any, ...],
    threat_mask: int,
    machine_mask: int,
    own_hand: HandObs,
    drew_sabotage_or_none: bool,
    is_first_defender: bool,
    has_open_furt_rive: bool,
) -> int:
    """Score heuristique réflexe B0 v6.1 (entier, K_max = 0, zéro inférence bayésienne)."""
    kind = target[0]

    if kind == "FORET":
        _, r, p = target
        r_i, p_i = int(r), int(p)
        defs = obs.parcel_defenseurs(r_i, p_i)
        cur_def = defs + obs.parcel_insectes(r_i, p_i)
        seuil_base = CANONICAL_DOTATION[p_i - 1]
        bit = 1 << (r_i * MAX_P + (p_i - 1))
        score = 100

        # Piège autonome v6.1 (SINGLE_STRIKE, sans Embuscade) : ne pas gaspiller un Défenseur dessus
        if obs.parcel_piege(r_i, p_i) == PIEGE_ACTIF:
            return 65
        if obs.mode >= 2 and defs == 0 and obs.parcel_has_nid(r_i, p_i):
            score += 480
        if (threat_mask & bit) and cur_def < seuil_base:
            score += 600 if r_i == obs.observer_seat else 520
        if (machine_mask & bit) and cur_def < seuil_base:
            score += 180
        if obs.parcel_arbres(r_i, p_i) == 1:
            score += 60
        return score

    if kind == "LISIERE":
        _, slot_idx = target
        if obs.mode < 2 or int(slot_idx) >= 2 * obs.n_players:
            return 0
        tile_id, _, constructors = obs.lisiere_tile_info(int(slot_idx))
        fam, _, _ = SYNERGY_META[tile_id]
        fam_bonus = 90 if fam == FAMILLE_REVE else (70 if fam == FAMILLE_CROISSANCE else 50)
        if constructors == 1:
            return 580 + fam_bonus
        if drew_sabotage_or_none and obs.tour <= 6:
            return 420 + fam_bonus
        return 240 + fam_bonus

    if kind == "FURTIVITE":
        _, ray, rive = target
        ray_i, rive_i = int(ray), int(rive)
        if not obs.is_ray_furtivite_open(ray_i):
            return 0
        d_rv = obs.furtivite_ray_rive_defs(ray_i, rive_i)
        if d_rv >= 2:
            return 0
        own_card_ray = (
            unpack_machine_card(own_hand.card)[0]
            if (own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players)
            else -1
        )
        own_on_ray = own_card_ray == ray_i
        rat_cnt = _ray_ratissage_count(obs, ray_i)
        has_untrapped = _ray_has_untrapped_parcel(obs, cfg, ray_i)

        # En 2.1 : ne pas jeter son pion au hasard sur les 2N rives vides (garde-fou anti-orphelins).
        # Seul réflexe élémentaire : on voit 1 machine en Ratissage sur ce rayon ET on tient l'autre carte -> m(r)=2 !
        if is_first_defender:
            if rive_i == FURT_RIVE_PIEGE and own_on_ray and rat_cnt == 1 and has_untrapped:
                return 360
            return 55

        # En 2.2 : si un partenaire a déjà amorcé cette rive (1/2), compléter le binôme si cohérent !
        if d_rv == 1:
            if rive_i == FURT_RIVE_PIEGE:
                if has_untrapped and (own_on_ray or rat_cnt >= 1):
                    return 500
                if has_untrapped and drew_sabotage_or_none:
                    return 390
                return 110
            if rive_i == FURT_RIVE_SABOTAGE:
                if obs.tour <= 6 and rat_cnt == 0 and not own_on_ray:
                    return 480
                return 95

        # En 2.2 sur rive vide (0/2) : ne pas ouvrir une seconde rive si une 1/2 attend déjà
        if has_open_furt_rive:
            return 60
        if rive_i == FURT_RIVE_PIEGE and own_on_ray and rat_cnt == 1 and has_untrapped:
            return 370
        if rive_i == FURT_RIVE_SABOTAGE and drew_sabotage_or_none and obs.tour <= 6 and rat_cnt == 0:
            return 270
        return 65

    if kind == "GARDIEN_PARI":
        _, case_c = target
        c_i = int(case_c)
        if not obs.gardien_pari_enabled or not obs.gardien_present_at_case(c_i):
            return 0
        own_c = obs.player_def2_gardien_pari_case(obs.observer_seat)
        allies_c = obs.gardien_pari_defenders(c_i) - (1 if own_c == c_i else 0)
        if allies_c >= GARDIEN_BET_CAP:
            return 0
        total_g = obs.total_gardien_pari_defenders()
        if obs.tour <= 7 and total_g >= obs.n_players - 1 and drew_sabotage_or_none:
            return 450
        if obs.tour <= 7 and total_g >= 1 and drew_sabotage_or_none:
            return 280
        return 100

    if kind == "REVE_ACTIVATION":
        _, case_c = target
        c_i = int(case_c)
        if obs.reve_at_case(c_i) <= 0:
            return 0
        own_hits = (
            own_hand.card is not None
            and 1 <= own_hand.card <= 2 * obs.n_players
            and own_hand.lecture_m == c_i
        )
        # Éviter de poser son 2e Défenseur sur un Rêve où l'on a déjà mis son 1er Défenseur pour sa propre carte
        if (not is_first_defender) and obs.player_def1_reve_case(obs.observer_seat) == c_i:
            return 45
        return 435 if own_hits else 70

    return 0


class BotB0:
    """Agent réflexe B0 v6.1 (`K_max = 0`) opérant exclusivement sur `PlayerObservation`."""

    @staticmethod
    def choose(obs: PlayerObservation, decision: DecisionRequest, cfg: GameConfig) -> Any:
        opts = decision.options
        assert len(opts) >= 1
        if len(opts) == 1:
            return opts[0]

        dtype = decision.decision_type

        if dtype in (DEC_POSE_DEFENSEUR_1, DEC_POSE_DEFENSEUR_2):
            own_hand = obs.hand_of(obs.observer_seat)
            drew_sab = (not own_hand.has_card) or (
                own_hand.card in (CARD_SABOTAGE, CARD_ECAILLE)
            )
            threat_mask, machine_mask = _compute_threat_and_machine_masks(obs, cfg, own_hand)

            is_def1 = dtype == DEC_POSE_DEFENSEUR_1
            has_open_furt_rive = False
            if not is_def1:
                for r_chk in range(obs.n_players):
                    if obs.is_ray_furtivite_open(r_chk) and (
                        obs.furtivite_ray_rive_defs(r_chk, FURT_RIVE_PIEGE) == 1
                        or obs.furtivite_ray_rive_defs(r_chk, FURT_RIVE_SABOTAGE) == 1
                    ):
                        has_open_furt_rive = True
                        break

            best_choice = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0

            if is_def1:
                for idx, opt in enumerate(opts):
                    sc = _score_defender_target(
                        obs,
                        cfg,
                        opt,
                        threat_mask,
                        machine_mask,
                        own_hand,
                        drew_sab,
                        True,
                        False,
                    )
                    if sc > best_sc:
                        best_sc = sc
                        best_tb = -1
                        best_idx = idx
                        best_choice = opt
                    elif sc == best_sc:
                        if best_tb < 0:
                            best_tb = _tiebreak_u64(cfg, obs, best_idx)
                        tb = _tiebreak_u64(cfg, obs, idx)
                        if tb > best_tb:
                            best_tb = tb
                            best_idx = idx
                            best_choice = opt
                return best_choice

            # DEC_POSE_DEFENSEUR_2 (K_max = 0 : pose directe en choix définitif)
            for idx, opt in enumerate(opts):
                act_kind, target = opt
                if act_kind != "POSER_DEFINITIF":
                    continue
                sc = _score_defender_target(
                    obs,
                    cfg,
                    target,
                    threat_mask,
                    machine_mask,
                    own_hand,
                    drew_sab,
                    False,
                    has_open_furt_rive,
                )
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_choice = opt
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_choice = opt
            return best_choice

        if dtype == DEC_REVISION_DEFENSEUR_2:
            for opt in opts:
                if opt[0] == "VERROUILLER_DEFINITIF":
                    return opt
            return opts[0]

        if dtype == DEC_OISEAU_PERCHOIR_1_1:
            # Préfère garder un Sabotage ou une Écaille en main (zéro frappe), sinon bris d'égalité
            for cand_c in opts:
                if int(cand_c) in (CARD_SABOTAGE, CARD_ECAILLE):
                    return cand_c
            best_c = opts[0]
            best_score_c = -10**9
            for idx, cand_c in enumerate(opts):
                ci = int(cand_c)
                if 1 <= ci <= 2 * obs.n_players:
                    rm, mt = unpack_machine_card(ci)
                    pos, _ = obs.machine_pos_status(rm, mt)
                    sc_c = -10 * pos - 5 * obs.machine_effective_rouges(rm, mt)
                else:
                    sc_c = 0
                if sc_c > best_score_c:
                    best_score_c = sc_c
                    best_c = cand_c
            return best_c

        if dtype == DEC_OISEAU_DE_ENVOL_1_3:
            # Choisit le rang qui tombe sur un Rêve ou qui déclenche le moins de frappes
            best_rk = opts[0]
            best_sc_rk = -10**9
            for rk in opts:
                ri = int(rk)
                t_c, _ = obs.tactique_code_bugs(ri - 1)
                if is_reve_code(t_c):
                    sc_rk = 200 if obs.reve_activation_defenders(ri) >= 1 else 120
                elif is_tactique_code(t_c):
                    spec = TACTIQUES_SPEC[t_c]
                    sc_rk = -40 * len(spec.cibles) - 20 * spec.mod_seuil
                else:
                    sc_rk = 0
                if sc_rk > best_sc_rk:
                    best_sc_rk = sc_rk
                    best_rk = rk
            return best_rk

        if dtype == DEC_HUMAIN_CHAMAN_2_1:
            own_hand = obs.hand_of(obs.observer_seat)
            own_hits_reve = (
                own_hand.card is not None
                and 1 <= own_hand.card <= 2 * obs.n_players
                and own_hand.lecture_m is not None
                and obs.reve_at_case(own_hand.lecture_m) > 0
            )
            if own_hits_reve and CHAMAN_CHANT in opts:
                return CHAMAN_CHANT
            if CHAMAN_TAMBOUR in opts:
                return CHAMAN_TAMBOUR
            return opts[0]

        if dtype == DEC_MAMMIFERE_DUEL_2:
            if (
                obs.duel_state != DUEL_TERRITOIRE_TENU
                and "POSER_DUEL_DEFI" in opts
            ):
                return "POSER_DUEL_DEFI"
            return "PASSER" if "PASSER" in opts else opts[0]

        if dtype == DEC_OISEAU_PLUME_2:
            own_hand = obs.hand_of(obs.observer_seat)
            if own_hand.card is not None and 1 <= own_hand.card <= 2 * obs.n_players:
                r_m, _ = unpack_machine_card(own_hand.card)
                cand_pl = (PLUME_CHAUD, PLUME_KIND_RAY, r_m)
                if cand_pl in opts:
                    return cand_pl
            elif (not own_hand.has_card) or own_hand.card in (CARD_SABOTAGE, CARD_ECAILLE):
                cand_pl = (PLUME_CALME, PLUME_KIND_RAY, obs.observer_seat)
                if cand_pl in opts:
                    return cand_pl
            return "PASSER" if "PASSER" in opts else opts[0]

        if dtype == DEC_REPTILE_POSE_CROC_3_2:
            best_rp = opts[0]
            best_sc_rp = -1
            for idx, rp in enumerate(opts):
                r_c, p_c = int(rp[0]), int(rp[1])
                sc_rp = (
                    obs.parcel_arbres(r_c, p_c) * 40
                    + (60 if obs.parcel_piege(r_c, p_c) == PIEGE_AUCUN else 0)
                    + (45 if obs.parcel_has_nid(r_c, p_c) else 0)
                    + p_c * 15
                )
                if sc_rp > best_sc_rp:
                    best_sc_rp = sc_rp
                    best_rp = rp
            return best_rp

        if dtype == DEC_CHOIX_CIBLE_REVE_3_2:
            def _seat_threat_b0(s_id: int) -> tuple[int, int, int, int, int]:
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
                    tuple(sorted((_seat_threat_b0(int(s_i)) for s_i in combo), reverse=True)),
                    _tiebreak_u64(cfg, obs, opts.index(combo)),
                ),
            )

        if dtype == DEC_BOUCLIER_LISIERE_5_3:
            if obs.tour < 8 and "UTILISER_BOUCLIER" in opts:
                return "UTILISER_BOUCLIER"
            return "LAISSER_RETOURNER" if "LAISSER_RETOURNER" in opts else opts[0]

        if dtype == DEC_ENRACINEMENT_6_1:
            if obs.tour < 7:
                return "PASSER" if "PASSER" in opts else opts[0]
            reves_on = sum(1 for c_r in range(1, TRACK_LEN + 1) if obs.reve_at_case(c_r) > 0)
            best_root: Any = "PASSER" if "PASSER" in opts else opts[0]
            best_sc_rt = 0
            for opt in opts:
                if opt == "PASSER":
                    continue
                sl_idx, p_rt = int(opt[0]), int(opt[1])
                tid_rt, _, _ = obs.lisiere_tile_info(sl_idx)
                fam_rt, _, _ = SYNERGY_META[tid_rt]
                if fam_rt == FAMILLE_REVE and obs.tour == 7 and reves_on >= max(1, cfg.total_reves_partie - 1):
                    continue
                souches = obs.parcel_souches(obs.observer_seat, p_rt)
                if souches <= 0:
                    continue
                sc_rt = souches * 100 + p_rt * 10
                if sc_rt > best_sc_rt:
                    best_sc_rt = sc_rt
                    best_root = opt
            return best_root

        if dtype == DEC_POSE_PIEGE_FURTIVITE_4_1:
            ray_p = int(decision.context.get("ray", obs.observer_seat))
            m_mask = _active_machine_mask(obs)
            best_p = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, cand_p in enumerate(opts):
                p_i = int(cand_p)
                has_m = bool(m_mask & (1 << (ray_p * MAX_P + (p_i - 1))))
                sc = (
                    (120 if has_m else 0)
                    + obs.parcel_arbres(ray_p, p_i) * 35
                    + (45 if obs.parcel_has_nid(ray_p, p_i) else 0)
                )
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_p = cand_p
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_p = cand_p
            return best_p

        if dtype == DEC_ORDRE_CONSTRUCTION_3_1:
            best_slot = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, slot_idx in enumerate(opts):
                tid, _, _ = obs.lisiere_tile_info(int(slot_idx))
                fam, _, _ = SYNERGY_META[tid]
                prio = 3 if fam == FAMILLE_REVE else (2 if fam == FAMILLE_CROISSANCE else 1)
                if prio > best_sc:
                    best_sc = prio
                    best_tb = -1
                    best_idx = idx
                    best_slot = slot_idx
                elif prio == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_slot = slot_idx
            return best_slot

        if dtype == DEC_CHOIX_CASE_GARDIEN:
            has_ins_p = "I" in cfg.peuples
            best_case = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, c_num in enumerate(opts):
                c_int = int(c_num)
                if c_int == TRIG_PARADE:
                    w = 60
                elif c_int == TRIG_INSECTE:
                    w = 55 if has_ins_p else 20
                elif c_int == TRIG_RESONANCE:
                    w = 50
                elif c_int == TRIG_PIEGEAGE:
                    w = 45
                elif c_int == TRIG_SABOTAGE:
                    w = 35
                elif c_int == TRIG_REVE:
                    w = 30
                else:
                    w = 25
                if w > best_sc:
                    best_sc = w
                    best_tb = -1
                    best_idx = idx
                    best_case = c_num
                elif w == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_case = c_num
            return best_case

        if dtype == DEC_PLACEMENT_NID_3_1:
            best_nid_pos = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, (r, p) in enumerate(opts):
                sc = int(p) * 100 + obs.parcel_arbres(int(r), int(p))
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_nid_pos = (r, p)
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_nid_pos = (r, p)
            return best_nid_pos

        if dtype == DEC_LIBERATION_BATISSEUR_3_1:
            m_mask = _active_machine_mask(obs)
            best_lib = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, opt in enumerate(opts):
                _, _, r, p = opt
                has_m = bool(m_mask & (1 << (int(r) * MAX_P + (int(p) - 1))))
                sc = 100 if has_m else 50
                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_lib = opt
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_lib = opt
            return best_lib

        if dtype == DEC_MIGRATION_INSECTE_4_3:
            src = decision.context.get("source", ("FORET", 0, 1))
            src_kind, _, src_p = src
            m_mask = _active_machine_mask(obs)
            best_mv = opts[0]
            best_sc = -1
            best_tb = -1
            best_idx = 0
            for idx, mv in enumerate(opts):
                mk = mv[0]
                sc = 50
                if mk == "COLONIE":
                    sc = 500 if obs.gardien_available_at_case(int(mv[1])) else 260
                elif mk == "BUG":
                    t_code, t_bugs = obs.tactique_code_bugs(int(mv[1]) - 1)
                    sc = 420 if (is_tactique_code(t_code) and t_bugs == 0) else 220
                elif mk == "FORET":
                    dst_r, dst_p = int(mv[1]), int(mv[2])
                    if obs.mode >= 2 and src_kind == "FORET" and dst_p > int(src_p):
                        sc = 300
                    elif m_mask & (1 << (dst_r * MAX_P + (dst_p - 1))):
                        sc = 250
                    else:
                        sc = 80
                elif mk == "RESTER":
                    sc = 150

                if sc > best_sc:
                    best_sc = sc
                    best_tb = -1
                    best_idx = idx
                    best_mv = mv
                elif sc == best_sc:
                    if best_tb < 0:
                        best_tb = _tiebreak_u64(cfg, obs, best_idx)
                    tb = _tiebreak_u64(cfg, obs, idx)
                    if tb > best_tb:
                        best_tb = tb
                        best_idx = idx
                        best_mv = mv
            return best_mv

        best_gen = opts[0]
        best_u_gen = _tiebreak_u64(cfg, obs, 0)
        for idx in range(1, len(opts)):
            u = _tiebreak_u64(cfg, obs, idx)
            if u > best_u_gen:
                best_u_gen = u
                best_gen = opts[idx]
        return best_gen


def choose_b0(state: GameState, decision: DecisionRequest) -> Any:
    """Point d'entrée isolé : extrait uniquement `PlayerObservation` pour `decision.decideur`."""
    obs = state.get_observation(decision.decideur)
    return BotB0.choose(obs, decision, state.cfg)


def play_game_b0(
    state: GameState,
    *,
    max_steps: int = 2000,
    chassis_id: int = -1,
    telemetry: Any | None = None,
) -> GameOver:
    """Exécute une partie complète pilotée par B0 jusqu'à GameOver avec garde-fou max_steps."""
    steps = 0
    while True:
        steps += 1
        if steps > max_steps:
            cfg = state.cfg
            raise RuntimeError(
                f"Garde-fou max_steps={max_steps} dépassé : "
                f"mode={cfg.mode}, chassis_id={chassis_id}, n_players={cfg.n_players}, "
                f"exp_seed={cfg.exp_seed}, rep_id={cfg.rep_id}, tour={state.tour}, "
                f"step={state.step}, continuation={state._continuation!r}, "
                f"state_hex={state.raw_used_bytes().hex()}"
            )
        out = step_until_decision(
            state, max_internal_steps=max(2000, max_steps), telemetry=telemetry
        )
        if isinstance(out, GameOver):
            return out
        choice = choose_b0(state, out)
        apply_choice(state, choice, telemetry=telemetry)
