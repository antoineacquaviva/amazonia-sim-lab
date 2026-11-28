"""Catalogue Canon v6.4 — Les 15 Gardiens double-face (G1..G15, profil 'A').

100 % stateless, stdlib pure PyPy 3.11, zéro `_buf`, zéro `random`, zéro dette mémorielle (`mem_debt == 0`).
Source de vérité : `contracts/tiles_canon_v6_4.json`.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_CALE_REVEAL,
    HOOK_5_APRES_PARADE_PIEGE,
    HOOK_5_BOURBIER_CHECK,
    HOOK_5_PARADE_PONTE,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    HOOK_REPOUSSE_FINALE,
    list_machines_targeting_parcel,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_insecte_take_with_priming,
    prim_mod_puissance,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_continuation_sequence,
    push_effect_decision,
    verb_alterer,
    verb_etouffer,
    verb_glisser_reve,
    verb_reculer,
    verb_refroidir,
    verb_semer_au_sac,
)
from engine.state import (
    CALE_CAIMAN,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    DUEL_DEFI,
    DUEL_NONE,
    DUEL_TERRITOIRE_TENU,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_ECAILLES,
    PERCHOIR_KIND_RANK,
    PERCHOIR_KIND_RAY,
    PERCHOIR_NONE,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    TRIG_INSECTE,
    TRIG_SABOTAGE,
    GameState,
    is_reve_code,
    is_tactique_code,
)

__all__ = (
    "g1_jaguar_v6_4",
    "g2_anaconda_v6_4",
    "g3_atele_v6_4",
    "g4_ara_v6_4",
    "g5_iguane_v6_4",
    "g6_toucan_v6_4",
    "g7_tapir_v6_4",
    "g8_boto_v6_4",
    "g9_caiman_v6_4",
    "g10_matamata_v6_4",
    "g11_harpie_v6_4",
    "g12_ibijau_v6_4",
    "g13_tamanoir_v6_4",
    "g14_teju_v6_4",
    "g15_colibri_v6_4",
)


def _gov(state: GameState, peuple: str) -> int:
    s = state.cfg.seat_of_peuple(peuple)
    return s if s is not None else state.coordonnateur


def _find_gardien_case_and_face(state: GameState, g_target: int) -> tuple[int, int] | None:
    for c in range(1, TRACK_LEN + 1):
        g_num, g_face = state.get_gardien_at_case(c)
        if g_num == g_target:
            return c, g_face
    return None


def _mirror_rank(rank_1_6: int) -> int:
    return rank_1_6 + 3 if rank_1_6 <= 3 else rank_1_6 - 3


def _regrow_one_souche_on_ray(state: GameState, ray: int) -> bool:
    for p in range(1, state.cfg.p_max + 1):
        if not state.is_route_forestiere(ray, p) and state.get_parcel_souches(ray, p) >= 1:
            before = state.get_parcel_arbres(ray, p)
            prim_creation_entite(state, "ARBRE", ray=ray, p=p, count=1, light_trigger=False)
            if state.get_parcel_arbres(ray, p) > before:
                return True
    return False


# ---------------------------------------------------------------------------
# G1 — Le Jaguar (M>R)
# ---------------------------------------------------------------------------


@register_tile(
    "G1",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_APRES_PARADE_PIEGE, HOOK_EFFECT_RESUME),
)
def g1_jaguar_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G1 Le Jaguar v6.4 : Croc sur Duel (F1) ; Croc + Duel déplacés sur cible & Croc Refroidit (F2)."""
    if hook == HOOK_5_APRES_PARADE_PIEGE:
        if not ctx.get("is_croc"):
            return
        info = _find_gardien_case_and_face(state, 1)
        if info is None or info[1] < 2:
            return
        # Sans dette mémorielle : actif ce tour ssi G1 (Face 2) s'est déjà ouvert à ce tour (encoche occupée)
        if state.has_gardien_opened_this_turn(info[0]):
            verb_refroidir(state, int(ctx["ray"]), int(ctx["m_type"]), 1)
        return

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        gov_m = _gov(state, "M")
        d_st, d_r, d_p = state.get_duel_state()
        duel_on_forest = d_st != DUEL_NONE and not state.is_route_forestiere(d_r, d_p)

        if face == 1:
            if duel_on_forest:
                prim_creation_entite(state, "CROC", ray=d_r, p=d_p)
                return
            targeted = list_targeted_parcels(state)
            if not targeted:
                return
            if len(targeted) == 1:
                r0, p0 = targeted[0]
                state.set_duel_defi(r0, p0)
                prim_creation_entite(state, "CROC", ray=r0, p=p0)
                return
            push_effect_decision(
                state,
                gov_m,
                targeted,
                {"effect_kind": "G1_F1_DUEL_CROC", "face": 1},
                slot_id="G1",
                profile="A",
                resume_tag="G1_F1",
            )
            return

        # Face 2 : poser le Croc (et au choix déplacer le Duel avec lui en conservant sa face) sur toute parcelle ciblée
        targeted = list_targeted_parcels(state)
        if not targeted:
            if duel_on_forest:
                prim_creation_entite(state, "CROC", ray=d_r, p=d_p)
            return
        opts: list[tuple[Any, ...]] = []
        for r_t, p_t in targeted:
            opts.append(("CROC_AND_DUEL", r_t, p_t))
            opts.append(("CROC_ONLY", r_t, p_t))
        push_effect_decision(
            state,
            gov_m,
            tuple(opts),
            {"effect_kind": "G1_F2_CROC_DUEL", "face": 2},
            slot_id="G1",
            profile="A",
            resume_tag="G1_F2",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G1_F1":
            r0, p0 = int(ch[0]), int(ch[1])
            state.set_duel_defi(r0, p0)
            prim_creation_entite(state, "CROC", ray=r0, p=p0)
        elif tag == "G1_F2":
            mode_ch, r0, p0 = str(ch[0]), int(ch[1]), int(ch[2])
            if mode_ch == "CROC_AND_DUEL":
                d_st, _, _ = state.get_duel_state()
                face_duel = d_st if d_st in (DUEL_DEFI, DUEL_TERRITOIRE_TENU) else DUEL_DEFI
                state.set_duel_state_at(r0, p0, face_duel, allow_route=False)
            prim_creation_entite(state, "CROC", ray=r0, p=p0)


# ---------------------------------------------------------------------------
# G2 — L'Anaconda vert (R>M)
# ---------------------------------------------------------------------------


def _g2_parcel_eligible(state: GameState, ray: int, p: int, face: int) -> bool:
    if state.is_route_forestiere(ray, p):
        return False
    if state.get_parcel_defenseurs(ray, p) >= 2:
        return True
    d_st, d_r, d_p = state.get_duel_state()
    if d_r == ray and d_p == p:
        if face == 1:
            return d_st == DUEL_TERRITOIRE_TENU
        return d_st in (DUEL_DEFI, DUEL_TERRITOIRE_TENU)
    return False


def _g2_apply_option(state: GameState, opt: tuple[Any, ...]) -> None:
    kind = str(opt[0])
    ray, m_type = int(opt[1]), int(opt[2])
    if kind == "EXIT_RATISSAGE":
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st == MACHINE_STATUS_RATISSAGE and pos > 0:
            state.set_machine_pos_status(ray, m_type, pos, MACHINE_STATUS_NORMAL, False)
            rouges, _ = state.get_machine_tokens(ray, m_type)
            if rouges >= 1:
                prim_mod_puissance(state, ray, m_type, delta_rouges=-1)
            verb_reculer(state, ray, m_type)
    elif kind == "RECULER":
        verb_reculer(state, ray, m_type)
    elif kind == "ETOUFFER_RECULER":
        verb_etouffer(state, ray, m_type)
        verb_reculer(state, ray, m_type)


@register_tile("G2", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g2_anaconda_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G2 L'Anaconda vert v6.4 : sort 1 Ratissage sur Duel/2 Déf (ou Recule/Étouffe mobile ciblant)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        n = state.cfg.n_players
        rat_opts: list[tuple[Any, ...]] = []
        for r in range(n):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r, mt)
                if st == MACHINE_STATUS_RATISSAGE and pos > 0 and _g2_parcel_eligible(state, r, pos, face):
                    rat_opts.append(("EXIT_RATISSAGE", r, mt))

        mob_opts: list[tuple[Any, ...]] = []
        seen_mob: set[tuple[int, int]] = set()
        for r in range(n):
            for p in range(1, state.cfg.p_max + 1):
                if not _g2_parcel_eligible(state, r, p, face):
                    continue
                for rm, mt in list_machines_targeting_parcel(state, r, p, mobile_only=True):
                    if (rm, mt) in seen_mob:
                        continue
                    pos_m, st_m, _ = state.get_machine_pos_status(rm, mt)
                    if st_m != MACHINE_STATUS_NORMAL or pos_m == 0:
                        continue
                    if face == 1:
                        if state.next_non_razed_towards_border(rm, pos_m) is not None:
                            seen_mob.add((rm, mt))
                            mob_opts.append(("RECULER", rm, mt))
                    else:
                        seen_mob.add((rm, mt))
                        mob_opts.append(("ETOUFFER_RECULER", rm, mt))

        opts: list[tuple[Any, ...]] = (
            rat_opts if (face == 1 and rat_opts) else (rat_opts + mob_opts)
        )
        if not opts:
            return
        if len(opts) == 1:
            _g2_apply_option(state, opts[0])
            return
        push_effect_decision(
            state,
            _gov(state, "R"),
            tuple(opts),
            {"effect_kind": "G2_ANACONDA", "face": face},
            slot_id="G2",
            profile="A",
            resume_tag="G2_APPLY",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _g2_apply_option(state, ctx["choice"])


# ---------------------------------------------------------------------------
# G3 — L'Atèle (M>O)
# ---------------------------------------------------------------------------


def _g3_radial_neighbors(state: GameState, ray: int, p: int) -> list[int]:
    out = [p]
    p_back = state.next_non_razed_towards_border(ray, p)
    if p_back is not None:
        out.append(p_back)
    p_fwd = state.next_non_razed_towards_heart(ray, p)
    if p_fwd is not None:
        out.append(p_fwd)
    return out


def _g3_collect_moves(state: GameState, face: int) -> tuple[tuple[Any, ...], ...]:
    n = state.cfg.n_players
    seat_m = state.cfg.seat_of_peuple("M")
    seat_o = state.cfg.seat_of_peuple("O")
    if face == 1:
        if seat_m is None or seat_o is None:
            return ()
        ray_pairs: list[tuple[int, int]] = [(seat_m, seat_o)]
    else:
        p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
        base_r = (
            p_idx
            if (p_face != PERCHOIR_NONE and p_kind == PERCHOIR_KIND_RAY and 0 <= p_idx < n)
            else (seat_o if seat_o is not None else 0)
        )
        ray_pairs = []
        for neigh in sorted({(base_r - 1) % n, (base_r + 1) % n}):
            if neigh != base_r:
                ray_pairs.append((base_r, neigh))

    moves: set[tuple[Any, ...]] = set()
    for r_a, r_b in ray_pairs:
        pair_set = (r_a, r_b)
        for s in range(n):
            for d in (0, 1):
                raw = state.get_player_def_loc_raw(s, d)
                if raw == 0:
                    continue
                kind, a, b, _c = state.decode_def_loc(raw)
                if kind == "FORET" and a in pair_set:
                    other_r = r_b if a == r_a else r_a
                    # 0 ou 1 pas radial avant la traversée
                    pre_ps = _g3_radial_neighbors(state, a, b)
                    for pre_p in pre_ps:
                        if state.get_parcel_arbres(a, pre_p) < 1:
                            continue
                        # Traversée cime -> cime à même profondeur
                        if (
                            not state.is_route_forestiere(other_r, pre_p)
                            and state.get_parcel_arbres(other_r, pre_p) >= 1
                        ):
                            if face == 1:
                                moves.add((s, d, "FORET", other_r, pre_p))
                            else:
                                for post_p in _g3_radial_neighbors(state, other_r, pre_p):
                                    moves.add((s, d, "FORET", other_r, post_p))
                        # Saut de lisière : arrivée sur une Rive de Furtivité ouverte des 2 rayons
                        for dst_r in pair_set:
                            if not state.is_ray_furtivite_open(dst_r):
                                continue
                            for rv in (FURT_RIVE_PIEGE, FURT_RIVE_SABOTAGE):
                                if state.get_furtivite_nb_def_rive(dst_r, 1, rv) < state.get_furtivite_rive_capacity(dst_r, rv):
                                    moves.add((s, d, "FURTIVITE", dst_r, rv))
                elif kind == "FURTIVITE" and a in pair_set:
                    # Saut de lisière : départ depuis une Rive de Furtivité -> parcelle à Arbre debout des 2 rayons
                    for dst_r in pair_set:
                        for p_dst in range(1, state.cfg.p_max + 1):
                            if (
                                not state.is_route_forestiere(dst_r, p_dst)
                                and state.get_parcel_arbres(dst_r, p_dst) >= 1
                            ):
                                if face == 1:
                                    moves.add((s, d, "FORET", dst_r, p_dst))
                                else:
                                    for post_p in _g3_radial_neighbors(state, dst_r, p_dst):
                                        moves.add((s, d, "FORET", dst_r, post_p))
    return tuple(sorted(moves))


def _g3_apply_move(state: GameState, opt: tuple[Any, ...]) -> None:
    s, d, dst_kind, dst_r, dst_v = int(opt[0]), int(opt[1]), str(opt[2]), int(opt[3]), int(opt[4])
    if dst_kind == "FORET":
        prim_deplacement(
            state, "DEFENSEUR", src_seat=s, src_def_idx=d, dst_ray=dst_r, dst_p=dst_v
        )
    elif dst_kind == "FURTIVITE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=s,
            src_def_idx=d,
            dst_ray=dst_r,
            dst_furtivite_rive=dst_v,
        )


@register_tile("G3", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g3_atele_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G3 L'Atèle v6.4 : pont de cimes entre M et O (ou Perchoir+voisin F2) + Saut de lisière."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        moves = _g3_collect_moves(state, face)
        if not moves:
            return
        push_effect_decision(
            state,
            _gov(state, "M"),
            ("PASSER", *moves),
            {"effect_kind": "G3_ATELE", "face": face},
            slot_id="G3",
            profile="A",
            resume_tag="G3_MOVE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = ctx["choice"]
        if ch != "PASSER":
            _g3_apply_move(state, ch)


# ---------------------------------------------------------------------------
# G4 — L'Ara rouge (O>M)
# ---------------------------------------------------------------------------


def _g4_other_bet_cases(state: GameState, g4_case: int) -> list[int]:
    out: list[int] = []
    for c in range(1, TRACK_LEN + 1):
        if c == g4_case:
            continue
        if state.get_gardien_at_case(c)[0] > 0 and state.count_gardien_pari_defenders_at_case(c) >= 1:
            out.append(c)
    return out


def _g4_prompt_second_cri(
    state: GameState, g4_case: int, face: int, first_case: int
) -> None:
    others2 = _g4_other_bet_cases(state, g4_case)
    if not others2:
        return
    is_adjacent = abs(first_case - g4_case) == 1
    d_st, _, _ = state.get_duel_state()
    can_flip_duel = d_st == DUEL_TERRITOIRE_TENU
    if not is_adjacent and not can_flip_duel:
        return
    opts: list[Any] = ["PASSER"]
    if is_adjacent:
        for c2 in others2:
            opts.append(("FREE", c2))
    else:
        for c2 in others2:
            opts.append(("FLIP_DUEL", c2))
    push_effect_decision(
        state,
        _gov(state, "O"),
        tuple(opts),
        {
            "effect_kind": "G4_SECOND_CRI",
            "face": face,
            "free_adjacent": is_adjacent,
        },
        slot_id="G4",
        profile="A",
        resume_tag="G4_STEP2",
        resume_payload=(g4_case, face),
    )


def _g4_fire_case(state: GameState, target_case: int, face: int) -> None:
    if face == 1:
        prim_partage_info_etat_gardien(state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=target_case)
    else:
        prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=target_case)


@register_tile("G4", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g4_ara_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G4 L'Ara rouge v6.4 : encoche passive (F1) / relais (F2) + Second cri gratuit voisin ou Duel + Sentinelle seule."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        g4_case = int(ctx["case"])
        face = int(ctx.get("face", 1))
        others = _g4_other_bet_cases(state, g4_case)
        if not others:
            # Sentinelle seule : glisse le second pari de G4 lui-même en encoche
            if state.count_gardien_pari_defenders_at_case(g4_case) >= 1:
                prim_partage_info_etat_gardien(
                    state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=g4_case
                )
            return
        if len(others) == 1:
            c1 = others[0]
            # Programmer Second cri après la résolution éventuelle de c1
            _g4_prompt_second_cri_after(state, g4_case, face, c1)
            return
        push_effect_decision(
            state,
            _gov(state, "O"),
            tuple(others),
            {"effect_kind": "G4_FIRST_CRI", "face": face, "g4_case": g4_case},
            slot_id="G4",
            profile="A",
            resume_tag="G4_STEP1",
            resume_payload=(g4_case, face),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        payload = ctx["payload"]
        g4_case, face = int(payload[0]), int(payload[1])
        if tag == "G4_STEP1":
            _g4_prompt_second_cri_after(state, g4_case, face, int(ch))
        elif tag == "G4_F2_SECOND_CRI":
            first_case = int(payload[2])
            _g4_prompt_second_cri(state, g4_case, face, first_case)
        elif tag == "G4_STEP2" and ch != "PASSER":
            mode2, c2 = str(ch[0]), int(ch[1])
            if mode2 == "FLIP_DUEL":
                state.flip_duel_to_defi()
            _g4_fire_case(state, c2, face)


def _g4_prompt_second_cri_after(
    state: GameState, g4_case: int, face: int, first_case: int
) -> None:
    """Exécute le 1er cri (F1 slide ou F2 relais) puis ouvre le Second cri si éligible."""
    if face == 1:
        _g4_fire_case(state, first_case, 1)
        _g4_prompt_second_cri(state, g4_case, 1, first_case)
        return
    # Empile d'abord le rappel différé de Second cri, puis lance le relais F2 devant lui :
    # si le relais suspend, G4_F2_SECOND_CRI s'exécutera automatiquement dès sa résolution !
    push_continuation_sequence(
        state,
        (("DEFERRED_EFFECT_CALLBACK", "G4", "A", "G4_F2_SECOND_CRI", (g4_case, 2, first_case)),),
    )
    _g4_fire_case(state, first_case, 2)


# ---------------------------------------------------------------------------
# G5 — L'Iguane vert (R>O)
# ---------------------------------------------------------------------------


def _g5_targeted_free_traps(state: GameState, face: int) -> tuple[tuple[int, int], ...]:
    all_t = list_targeted_parcels(state)
    free_all = tuple((r, p) for r, p in all_t if state.get_parcel_piege(r, p) == PIEGE_AUCUN)
    if face == 2:
        return free_all

    p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
    primary: list[tuple[int, int]] = []
    if p_face != PERCHOIR_NONE:
        if p_kind == PERCHOIR_KIND_RAY:
            primary = [(r, p) for r, p in free_all if r == p_idx]
        elif p_kind == PERCHOIR_KIND_RANK:
            rank_1_6 = p_idx + 1
            for s in range(state.cfg.n_players):
                if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
                    continue
                card, _, _, lec_m, bound_t = state.get_player_hand(s)
                eff_r = bound_t if is_tactique_code(bound_t) else (lec_m if state.step == STEP_3_2_REVEAL else 0)
                if 1 <= card <= 12 and eff_r == rank_1_6:
                    r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                    if state.is_machine_etouffee_this_turn(r_m, mt_m):
                        continue
                    for r_t, p_t in free_all:
                        if (
                            r_t == r_m
                            and (r_m, mt_m)
                            in list_machines_targeting_parcel(state, r_t, p_t, mobile_only=True)
                            and (r_t, p_t) not in primary
                        ):
                            primary.append((r_t, p_t))
    if primary:
        return tuple(primary)

    # À défaut : rayon Reptiles ou rayon Oiseaux
    fallback_rays = {
        s for s in (state.cfg.seat_of_peuple("R"), state.cfg.seat_of_peuple("O")) if s is not None
    }
    return tuple((r, p) for r, p in free_all if r in fallback_rays)


def _g5_after_trap_step(state: GameState, face: int, trap_r: int, trap_p: int) -> None:
    gov_r = _gov(state, "R")
    if face == 1:
        if state.get_croc_parcel() is not None:
            return
        blue_machines = [
            (rm, mt)
            for rm, mt in list_machines_targeting_parcel(state, trap_r, trap_p)
            if state.get_machine_tokens(rm, mt)[1] >= 1
        ]
        other_targets = [
            (r2, p2) for r2, p2 in list_targeted_parcels(state) if (r2, p2) != (trap_r, trap_p)
        ]
        if not blue_machines or not other_targets:
            return
        opts: list[Any] = ["PASSER"]
        for rm, mt in blue_machines:
            for r2, p2 in other_targets:
                opts.append((rm, mt, r2, p2))
        push_effect_decision(
            state,
            gov_r,
            tuple(opts),
            {"effect_kind": "G5_F1_DRINK_BLUE_CROC"},
            slot_id="G5",
            profile="A",
            resume_tag="G5_F1_DRINK",
        )
        return

    # Face 2 : poser aussi le Croc disponible sur une 2e parcelle ciblée, puis option de boire 1 Bleu pour un 2e Piège
    if state.get_croc_parcel() is None:
        other_targets = [
            (r2, p2) for r2, p2 in list_targeted_parcels(state) if (r2, p2) != (trap_r, trap_p)
        ]
        if not other_targets:
            other_targets = list(list_targeted_parcels(state))
        if len(other_targets) == 1:
            prim_creation_entite(state, "CROC", ray=other_targets[0][0], p=other_targets[0][1])
            _g5_f2_offer_drink(state, trap_r, trap_p)
            return
        if len(other_targets) > 1:
            push_effect_decision(
                state,
                gov_r,
                tuple(other_targets),
                {"effect_kind": "G5_F2_POSE_CROC"},
                slot_id="G5",
                profile="A",
                resume_tag="G5_F2_CROC",
                resume_payload=(trap_r, trap_p),
            )
            return
    _g5_f2_offer_drink(state, trap_r, trap_p)


def _g5_f2_offer_drink(state: GameState, trap_r: int, trap_p: int) -> None:
    blue_machines: list[tuple[int, int]] = []
    for r_t, p_t in list_targeted_parcels(state):
        for rm, mt in list_machines_targeting_parcel(state, r_t, p_t):
            if state.get_machine_tokens(rm, mt)[1] >= 1 and (rm, mt) not in blue_machines:
                blue_machines.append((rm, mt))
    free_traps = [
        (r2, p2)
        for r2, p2 in list_targeted_parcels(state)
        if state.get_parcel_piege(r2, p2) == PIEGE_AUCUN and (r2, p2) != (trap_r, trap_p)
    ]
    if not blue_machines or not free_traps:
        return
    opts: list[Any] = ["PASSER"]
    for rm, mt in blue_machines:
        for r2, p2 in free_traps:
            opts.append((rm, mt, r2, p2))
    push_effect_decision(
        state,
        _gov(state, "R"),
        tuple(opts),
        {"effect_kind": "G5_F2_DRINK_BLUE_PIEGE"},
        slot_id="G5",
        profile="A",
        resume_tag="G5_F2_DRINK",
    )


@register_tile("G5", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g5_iguane_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G5 L'Iguane vert v6.4 : Piège sous Perchoir + boire 1 Bleu -> Croc (F1) ; Piège+Croc + 2e plongeon (F2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        free_t = _g5_targeted_free_traps(state, face)
        if not free_t:
            if face == 2 and state.get_croc_parcel() is None:
                all_t = list_targeted_parcels(state)
                if len(all_t) == 1:
                    prim_creation_entite(state, "CROC", ray=all_t[0][0], p=all_t[0][1])
                elif len(all_t) > 1:
                    push_effect_decision(
                        state,
                        _gov(state, "R"),
                        all_t,
                        {"effect_kind": "G5_F2_POSE_CROC"},
                        slot_id="G5",
                        profile="A",
                        resume_tag="G5_F2_CROC_ONLY",
                    )
            return
        if len(free_t) == 1:
            r0, p0 = free_t[0]
            prim_creation_entite(state, "PIEGE", ray=r0, p=p0, light_trigger=False)
            _g5_after_trap_step(state, face, r0, p0)
            return
        push_effect_decision(
            state,
            _gov(state, "R"),
            free_t,
            {"effect_kind": "G5_POSE_PIEGE", "face": face},
            slot_id="G5",
            profile="A",
            resume_tag="G5_TRAP",
            resume_payload=(face,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G5_TRAP":
            face = int(ctx["payload"][0])
            r0, p0 = int(ch[0]), int(ch[1])
            prim_creation_entite(state, "PIEGE", ray=r0, p=p0, light_trigger=False)
            _g5_after_trap_step(state, face, r0, p0)
        elif tag == "G5_F1_DRINK":
            if ch != "PASSER":
                rm, mt, r2, p2 = int(ch[0]), int(ch[1]), int(ch[2]), int(ch[3])
                prim_mod_puissance(state, rm, mt, delta_bleus=-1)
                prim_creation_entite(state, "CROC", ray=r2, p=p2)
        elif tag == "G5_F2_CROC":
            trap_r, trap_p = int(ctx["payload"][0]), int(ctx["payload"][1])
            prim_creation_entite(state, "CROC", ray=int(ch[0]), p=int(ch[1]))
            _g5_f2_offer_drink(state, trap_r, trap_p)
        elif tag == "G5_F2_CROC_ONLY":
            prim_creation_entite(state, "CROC", ray=int(ch[0]), p=int(ch[1]))
        elif tag == "G5_F2_DRINK" and ch != "PASSER":
            rm, mt, r2, p2 = int(ch[0]), int(ch[1]), int(ch[2]), int(ch[3])
            prim_mod_puissance(state, rm, mt, delta_bleus=-1)
            prim_creation_entite(state, "PIEGE", ray=r2, p=p2, light_trigger=False)


# ---------------------------------------------------------------------------
# G6 — Le Toucan toco (O>R)
# ---------------------------------------------------------------------------


def _g6_eligible_red_machines(state: GameState, face: int) -> tuple[tuple[int, int], ...]:
    n = state.cfg.n_players
    all_red: list[tuple[int, int]] = []
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0 and state.get_machine_tokens(r, mt)[0] >= 1:
                all_red.append((r, mt))
    if face == 2:
        return tuple(all_red)

    p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
    primary: list[tuple[int, int]] = []
    if p_face != PERCHOIR_NONE:
        if p_kind == PERCHOIR_KIND_RAY:
            primary = [(r, mt) for r, mt in all_red if r == p_idx]
        elif p_kind == PERCHOIR_KIND_RANK:
            rank_1_6 = p_idx + 1
            for s in range(n):
                card, _, _, lec_m, bound_t = state.get_player_hand(s)
                eff_r = bound_t if is_tactique_code(bound_t) else lec_m
                if 1 <= card <= 12 and eff_r == rank_1_6:
                    rm, mt = (card - 1) // 2, (card - 1) % 2
                    if (rm, mt) in all_red and (rm, mt) not in primary:
                        primary.append((rm, mt))
    if primary:
        return tuple(primary)

    seat_o = state.cfg.seat_of_peuple("O")
    if seat_o is None:
        return tuple(all_red)
    allowed_rays = {seat_o, (seat_o - 1) % n, (seat_o + 1) % n}
    return tuple((r, mt) for r, mt in all_red if r in allowed_rays)


def _g6_maybe_cri_de_vapeur(state: GameState, g6_case: int) -> None:
    right_icons = tuple(
        c
        for c in range(g6_case + 1, TRACK_LEN)  # strictement à droite, hors Résonance (6)
        if c != TRIG_INSECTE or state.cfg.has_insectes_peuple
    )
    if not right_icons:
        return
    if len(right_icons) == 1:
        state.light_trigger(right_icons[0])
        return
    push_effect_decision(
        state,
        _gov(state, "O"),
        right_icons,
        {"effect_kind": "G6_CRI_DE_VAPEUR", "g6_case": g6_case},
        slot_id="G6",
        profile="A",
        resume_tag="G6_CRI",
    )


def _g6_cool_machine(
    state: GameState, ray: int, m_type: int, face: int, g6_case: int
) -> None:
    verb_refroidir(state, ray, m_type, 1)
    new_r, new_b = state.get_machine_tokens(ray, m_type)
    if face == 2 and new_r == 0 and new_b >= 2:
        verb_etouffer(state, ray, m_type)
    if new_r == 0:
        _g6_maybe_cri_de_vapeur(state, g6_case)


@register_tile("G6", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g6_toucan_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G6 Le Toucan toco v6.4 : Refroidir sous Perchoir (partout F2 + Étouffer à 0R/2B) + Cri de vapeur à droite."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        g6_case = int(ctx["case"])
        cands = _g6_eligible_red_machines(state, face)
        if not cands:
            _g6_maybe_cri_de_vapeur(state, g6_case)
            return
        if len(cands) == 1:
            _g6_cool_machine(state, cands[0][0], cands[0][1], face, g6_case)
            return
        push_effect_decision(
            state,
            _gov(state, "O"),
            cands,
            {"effect_kind": "G6_REFROIDIR", "face": face, "g6_case": g6_case},
            slot_id="G6",
            profile="A",
            resume_tag="G6_COOL",
            resume_payload=(face, g6_case),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G6_COOL":
            face, g6_case = int(ctx["payload"][0]), int(ctx["payload"][1])
            _g6_cool_machine(state, int(ch[0]), int(ch[1]), face, g6_case)
        elif tag == "G6_CRI":
            state.light_trigger(int(ch))


# ---------------------------------------------------------------------------
# G7 — Le Tapir (M>H)
# ---------------------------------------------------------------------------


def _g7_apply_choice(state: GameState, opt: tuple[Any, ...]) -> None:
    kind = str(opt[0])
    if kind == "FOULER_DUEL":
        r, p = int(opt[1]), int(opt[2])
        d_st, _, _ = state.get_duel_state()
        keep_face = d_st if d_st in (DUEL_DEFI, DUEL_TERRITOIRE_TENU) else DUEL_DEFI
        state.set_duel_bourbier(r, p, keep_face)
    elif kind == "FOULER_CHAMAN":
        s_h, d_idx, r, p = int(opt[1]), int(opt[2]), int(opt[3]), int(opt[4])
        state.place_defender_bourbier(s_h, d_idx, r, p)
    elif kind == "FRAYER":
        r, p = int(opt[1]), int(opt[2])
        d_st, _, _ = state.get_duel_state()
        keep_face = d_st if d_st in (DUEL_DEFI, DUEL_TERRITOIRE_TENU) else DUEL_DEFI
        seat_h = state.cfg.seat_of_peuple("H")
        has_chaman = False
        if seat_h is not None:
            for s_def, _d_def in state.list_defenders_on_parcel(r, p):
                if s_def == seat_h:
                    has_chaman = True
                    break
        state.set_duel_state_at(
            r, p, DUEL_TERRITOIRE_TENU if has_chaman else keep_face, allow_route=False
        )


@register_tile(
    "G7",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_BOURBIER_CHECK, HOOK_REPOUSSE_FINALE, HOOK_EFFECT_RESUME),
)
def g7_tapir_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G7 Le Tapir v6.4 : Bourbier sur Route (Duel ou Chamane) / Frayer + F2 Refroidir/Reculer + Enraciné."""
    if hook == HOOK_5_BOURBIER_CHECK:
        info = _find_gardien_case_and_face(state, 7)
        if info is None:
            return
        g7_face = info[1]
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        origin_pos = int(ctx["origin_pos"])
        target_p = int(ctx["target_p"])
        step_dir = 1 if target_p > origin_pos else -1
        for q in range(origin_pos + step_dir, target_p, step_dir):
            brb = state.get_bourbier_at(ray, q)
            if brb is None:
                continue
            ctx["cancelled"] = True
            if brb[0] == "DUEL":
                if g7_face == 2 and brb[1] == DUEL_TERRITOIRE_TENU:
                    state.flip_duel_to_defi()
                else:
                    state.clear_duel()
            else:
                state.mark_defender_waiting(brb[1], brb[2])
            if g7_face == 2:
                rouges, _ = state.get_machine_tokens(ray, m_type)
                if rouges >= 1:
                    verb_refroidir(state, ray, m_type, 1)
                else:
                    verb_reculer(state, ray, m_type)
            return
        return

    if hook == HOOK_REPOUSSE_FINALE:
        if ctx.get("phase") != "ROOTED_TILE" or ctx.get("slot_id") != "G7":
            return
        d_st, d_r, d_p = state.get_duel_state()
        if d_st == DUEL_NONE or state.is_route_forestiere(d_r, d_p):
            return
        seat_h = state.cfg.seat_of_peuple("H")
        if seat_h is None:
            return
        if any(s_def == seat_h for s_def, _ in state.list_defenders_on_parcel(d_r, d_p)):
            _regrow_one_souche_on_ray(state, d_r)
        return

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        n = state.cfg.n_players
        opts: list[tuple[Any, ...]] = []
        # 1. Fouler une Route avec Duel
        for r in range(n):
            for p in range(1, state.cfg.p_max + 1):
                if state.is_route_forestiere(r, p) and state.get_bourbier_at(r, p) is None:
                    opts.append(("FOULER_DUEL", r, p))
        # 2. Fouler une Route adjacente avec Tambour ou Chant
        seat_h = state.cfg.seat_of_peuple("H")
        if seat_h is not None:
            for d_idx in (0, 1):
                if state.get_humain_chaman_archetype(d_idx) not in (CHAMAN_TAMBOUR, CHAMAN_CHANT):
                    continue
                kind, hr, hp, _ = state.decode_def_loc(state.get_player_def_loc_raw(seat_h, d_idx))
                if kind == "FORET":
                    for q in (hp - 1, hp + 1):
                        if (
                            1 <= q <= state.cfg.p_max
                            and state.is_route_forestiere(hr, q)
                            and state.get_bourbier_at(hr, q) is None
                        ):
                            opts.append(("FOULER_CHAMAN", seat_h, d_idx, hr, q))
        # 3. Frayer : Duel sur parcelle ciblée
        for r_t, p_t in list_targeted_parcels(state):
            opts.append(("FRAYER", r_t, p_t))

        if not opts:
            return
        if len(opts) == 1:
            _g7_apply_choice(state, opts[0])
            return
        push_effect_decision(
            state,
            _gov(state, "M"),
            tuple(opts),
            {"effect_kind": "G7_TAPIR", "face": face},
            slot_id="G7",
            profile="A",
            resume_tag="G7_APPLY",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _g7_apply_choice(state, ctx["choice"])


# ---------------------------------------------------------------------------
# G8 — Le Boto (M>E)
# ---------------------------------------------------------------------------


def _g8_apply_opt(state: GameState, opt: tuple[Any, ...]) -> None:
    kind = str(opt[0])
    if kind == "SLIDE":
        verb_glisser_reve(state, int(opt[1]), dst_rank_0_5=int(opt[2]))
    elif kind == "SWAP":
        prim_permutation_piste(state, "SWAP_RANKS", rank_a=int(opt[1]), rank_b=int(opt[2]))
    elif kind == "ALTERER":
        verb_alterer(state, int(opt[1]), int(opt[2]))


@register_tile("G8", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g8_boto_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G8 Le Boto v6.4 : Glisser 1 Rêve (1 libre / swap F1 ; 2 libres / plongeon F2) sinon Altérer mobile."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        moves: list[tuple[Any, ...]] = []
        for rk in range(TRACK_LEN):
            if not is_reve_code(state.get_tactique_at_rank(rk)):
                continue
            if rk > 0 and not is_reve_code(state.get_tactique_at_rank(rk - 1)):
                moves.append(("SLIDE", rk, rk - 1))
                if face == 2 and rk >= 2 and not is_reve_code(state.get_tactique_at_rank(rk - 2)):
                    moves.append(("SLIDE", rk, rk - 2))
            if (
                face == 2
                and rk >= 2
                and is_reve_code(state.get_tactique_at_rank(rk - 1))
                and not is_reve_code(state.get_tactique_at_rank(rk - 2))
            ):
                # Plongeon par-dessus un Rêve voisin vers le 1er rang libre à sa gauche
                moves.append(("SLIDE", rk, rk - 2))
            if rk + 1 < TRACK_LEN and is_reve_code(state.get_tactique_at_rank(rk + 1)):
                moves.append(("SWAP", rk, rk + 1))

        if not moves:
            for r in range(state.cfg.n_players):
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                    pos, st, _ = state.get_machine_pos_status(r, mt)
                    if (
                        st == MACHINE_STATUS_NORMAL
                        and pos > 0
                        and not state.has_machine_alteration(r, mt)
                    ):
                        moves.append(("ALTERER", r, mt))
        if not moves:
            return
        if len(moves) == 1:
            _g8_apply_opt(state, moves[0])
            return
        push_effect_decision(
            state,
            _gov(state, "M"),
            tuple(moves),
            {"effect_kind": "G8_BOTO", "face": face},
            slot_id="G8",
            profile="A",
            resume_tag="G8_APPLY",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _g8_apply_opt(state, ctx["choice"])


# ---------------------------------------------------------------------------
# G9 — Le Caïman noir (R>H)
# ---------------------------------------------------------------------------


def _g9_apply_opt(state: GameState, opt: tuple[Any, ...]) -> None:
    kind = str(opt[0])
    r, mt = int(opt[1]), int(opt[2])
    if kind == "CALE":
        state.clear_all_cales()
        state.set_machine_cale(r, mt, CALE_CAIMAN)
    elif kind == "RECULER_CALEE":
        verb_reculer(state, r, mt)


@register_tile(
    "G9", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_3_2_CALE_REVEAL, HOOK_EFFECT_RESUME)
)
def g9_caiman_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G9 Le Caïman noir v6.4 : Cale exclusive bloquant Ratissage + rallume Sabotage à l'ouverture (+ Étouffer F2)."""
    if hook == HOOK_3_2_CALE_REVEAL:
        info = _find_gardien_case_and_face(state, 9)
        if info is None:
            return
        state.light_trigger(TRIG_SABOTAGE)
        if info[1] == 2:
            verb_etouffer(state, int(ctx["ray"]), int(ctx["m_type"]), seat=int(ctx["seat"]))
        return

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        n = state.cfg.n_players
        cur_cale = state.find_machine_with_cale()
        if face == 1:
            allowed_rays: set[int] = set()
            for p_code in ("R", "H"):
                s_p = state.cfg.seat_of_peuple(p_code)
                if s_p is not None:
                    allowed_rays.add(s_p)
            tamb = state.get_humain_tambour_parcel()
            if tamb is not None:
                allowed_rays.add(tamb[0])
        else:
            allowed_rays = set(range(n))

        opts: list[tuple[Any, ...]] = []
        for r in sorted(allowed_rays):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r, mt)
                if st == MACHINE_STATUS_NORMAL and pos > 0 and (r, mt) != cur_cale:
                    opts.append(("CALE", r, mt))
        if not opts and cur_cale is not None:
            opts.append(("RECULER_CALEE", cur_cale[0], cur_cale[1]))
        if not opts:
            return
        if len(opts) == 1:
            _g9_apply_opt(state, opts[0])
            return
        push_effect_decision(
            state,
            _gov(state, "R"),
            tuple(opts),
            {"effect_kind": "G9_CAIMAN", "face": face},
            slot_id="G9",
            profile="A",
            resume_tag="G9_APPLY",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _g9_apply_opt(state, ctx["choice"])


# ---------------------------------------------------------------------------
# G10 — La Matamata (R>E)
# ---------------------------------------------------------------------------


def _g10_untargeted_croc(state: GameState) -> bool:
    cp = state.get_croc_parcel()
    return cp is not None and cp not in list_targeted_parcels(state)


def _g10_apply_envouter(state: GameState, opt: tuple[Any, ...]) -> None:
    rm, mt = int(opt[1]), int(opt[2])
    verb_alterer(state, rm, mt)
    if len(opt) >= 5 and opt[3] is not None:
        prim_creation_entite(state, "CROC", ray=int(opt[3]), p=int(opt[4]))


def _g10_prompt_f2_envouter(state: GameState) -> None:
    env_opts: list[tuple[Any, ...]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(r, mt):
                env_opts.append(("ENVOUTER", r, mt, None, None))
    if not env_opts:
        return
    if len(env_opts) == 1:
        _g10_apply_envouter(state, env_opts[0])
        return
    push_effect_decision(
        state,
        _gov(state, "R"),
        tuple(env_opts),
        {"effect_kind": "G10_F2_ENVOUTER"},
        slot_id="G10",
        profile="A",
        resume_tag="G10_ENV",
    )


@register_tile("G10", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g10_matamata_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G10 La Matamata v6.4 : Semer 1 Écaille + Happer OU Envoûter (F1) / Happer ET Envoûter (F2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        verb_semer_au_sac(state, "ECAILLE", 1)
        targeted = list_targeted_parcels(state)
        gov_r = _gov(state, "R")

        if face == 1:
            opts: list[tuple[Any, ...]] = []
            if state.get_croc_parcel() is None:
                for r_t, p_t in targeted:
                    opts.append(("HAPPER", r_t, p_t))
            croc_untargeted = _g10_untargeted_croc(state)
            for r in range(state.cfg.n_players):
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                    pos, st, _ = state.get_machine_pos_status(r, mt)
                    if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(r, mt):
                        opts.append(("ENVOUTER", r, mt, None, None))
                        if croc_untargeted:
                            for r_t, p_t in targeted:
                                if r_t == r:
                                    opts.append(("ENVOUTER", r, mt, r_t, p_t))
            if not opts:
                return
            if len(opts) == 1:
                if opts[0][0] == "HAPPER":
                    prim_creation_entite(state, "CROC", ray=int(opts[0][1]), p=int(opts[0][2]))
                else:
                    _g10_apply_envouter(state, opts[0])
                return
            push_effect_decision(
                state,
                gov_r,
                tuple(opts),
                {"effect_kind": "G10_F1_MATAMATA"},
                slot_id="G10",
                profile="A",
                resume_tag="G10_F1",
            )
            return

        # Face 2 : Happer (Croc depuis réserve OU parcelle non ciblée) PUIS Envoûter
        can_happer = targeted and (state.get_croc_parcel() is None or _g10_untargeted_croc(state))
        if can_happer:
            if len(targeted) == 1:
                prim_creation_entite(state, "CROC", ray=targeted[0][0], p=targeted[0][1])
                _g10_prompt_f2_envouter(state)
                return
            push_effect_decision(
                state,
                gov_r,
                targeted,
                {"effect_kind": "G10_F2_HAPPER"},
                slot_id="G10",
                profile="A",
                resume_tag="G10_F2_HAP",
            )
            return
        _g10_prompt_f2_envouter(state)
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G10_F1":
            if ch[0] == "HAPPER":
                prim_creation_entite(state, "CROC", ray=int(ch[1]), p=int(ch[2]))
            else:
                _g10_apply_envouter(state, ch)
        elif tag == "G10_F2_HAP":
            prim_creation_entite(state, "CROC", ray=int(ch[0]), p=int(ch[1]))
            _g10_prompt_f2_envouter(state)
        elif tag == "G10_ENV":
            _g10_apply_envouter(state, ch)


# ---------------------------------------------------------------------------
# G11 — La Harpie féroce (O>H)
# ---------------------------------------------------------------------------


def _g11_machine_targets_snapshot(
    state: GameState, ray: int, m_type: int, rank_1_6: int
) -> tuple[tuple[int, int], ...]:
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st != MACHINE_STATUS_NORMAL or pos == 0:
        return ()
    out: list[tuple[int, int]] = []
    spec = TACTIQUES_SPEC[rank_1_6]
    rev_dev = (
        state.cfg.profile_for_slot("R7") is not None
        and state.get_tactique_at_rank(rank_1_6 - 1) == TILE_R_BASE + 7
    )
    for c_type in spec.cibles:
        if c_type == "SUR_PLACE" and not state.is_route_forestiere(ray, pos):
            out.append((ray, pos))
        elif c_type == "DEVANT":
            p_dev = (
                state.next_non_razed_towards_border(ray, pos)
                if rev_dev
                else state.next_non_razed_towards_heart(ray, pos)
            )
            if p_dev is not None:
                out.append((ray, p_dev))
    return tuple(out)


def _g11_apply_option(state: GameState, opt: tuple[Any, ...], face: int) -> None:
    seat_o = state.cfg.seat_of_peuple("O")
    if seat_o is None:
        return
    kind = str(opt[0])
    d_idx = int(opt[1])
    if kind == "FONDRE":
        prim_deplacement(
            state, "DEFENSEUR", src_seat=seat_o, src_def_idx=d_idx, dst_ray=int(opt[2]), dst_p=int(opt[3])
        )
        return
    if kind == "SAISIR":
        s_m, r_m, mt_m, rank_m = int(opt[2]), int(opt[3]), int(opt[4]), int(opt[5])
        targets_before = _g11_machine_targets_snapshot(state, r_m, mt_m, rank_m)
        state.place_defender_saisie_harpie(seat_o, d_idx, r_m, mt_m)
        verb_etouffer(state, r_m, mt_m, seat=s_m)
        if face == 2:
            opp_rank = _mirror_rank(rank_m)
            if is_reve_code(state.get_tactique_at_rank(opp_rank - 1)):
                seat_h = state.cfg.seat_of_peuple("H")
                if seat_h is not None:
                    chamans: list[tuple[int, int]] = []
                    for hd in (0, 1):
                        hk, hr, hp, _ = state.decode_def_loc(state.get_player_def_loc_raw(seat_h, hd))
                        if hk == "FORET" and (hr, hp) in targets_before:
                            chamans.append((seat_h, hd))
                    if chamans:
                        opts_c: list[Any] = ["PASSER", *chamans]
                        push_effect_decision(
                            state,
                            seat_o,
                            tuple(opts_c),
                            {
                                "effect_kind": "G11_F2_CARRY_CHAMAN",
                                "opp_rank": opp_rank,
                            },
                            slot_id="G11",
                            profile="A",
                            resume_tag="G11_CARRY",
                            resume_payload=(opp_rank,),
                        )


@register_tile("G11", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g11_harpie_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G11 La Harpie féroce v6.4 : Fondre ou Saisir au rang du Perchoir (+ miroir & transport Chamane F2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        seat_o = state.cfg.seat_of_peuple("O")
        if seat_o is None:
            return
        face = int(ctx.get("face", 1))
        eligible_defs: list[int] = []
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(seat_o, d)
            if raw == 0:
                continue
            dk, _, _, _ = state.decode_def_loc(raw)
            if dk in (
                "FORET",
                "FURTIVITE",
                "REVE_ACTIVATION",
                "REVE_ACTIVATION_CONSUMED",
                "LISIERE",
                "WAITING",
            ):
                eligible_defs.append(d)
        if not eligible_defs:
            return

        # 1. Cibles Fondre (parcelle d'une machine ou 1 pas devant elle en sautant les Routes)
        fondre_parcels: set[tuple[int, int]] = set()
        for r in range(state.cfg.n_players):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r, mt)
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    if not state.is_route_forestiere(r, pos):
                        fondre_parcels.add((r, pos))
                    p_fwd = state.next_non_razed_towards_heart(r, pos)
                    if p_fwd is not None:
                        fondre_parcels.add((r, p_fwd))

        # 2. Cibles Saisir (rang du Perchoir, + miroir en F2)
        saisir_ranks: set[int] = set()
        p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
        if p_face != PERCHOIR_NONE and p_kind == PERCHOIR_KIND_RANK:
            pr = p_idx + 1
            saisir_ranks.add(pr)
            if face == 2:
                saisir_ranks.add(_mirror_rank(pr))

        saisir_mobiles: list[tuple[int, int, int, int]] = []
        if saisir_ranks:
            for s in range(state.cfg.n_players):
                if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
                    continue
                card, _, _, lec_m, bound_t = state.get_player_hand(s)
                eff_r = bound_t if is_tactique_code(bound_t) else (lec_m if state.step == STEP_3_2_REVEAL else 0)
                if 1 <= card <= 12 and eff_r in saisir_ranks:
                    r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                    pos_m, st_m, _ = state.get_machine_pos_status(r_m, mt_m)
                    _, _, attacked = state.get_machine_turn_stats(r_m, mt_m)
                    if (
                        st_m == MACHINE_STATUS_NORMAL
                        and pos_m > 0
                        and not attacked
                        and not state.is_machine_etouffee_this_turn(r_m, mt_m)
                    ):
                        saisir_mobiles.append((s, r_m, mt_m, eff_r))

        opts: list[Any] = ["PASSER"]
        for d in eligible_defs:
            for s_m, r_m, mt_m, rk_m in saisir_mobiles:
                opts.append(("SAISIR", d, s_m, r_m, mt_m, rk_m))
            for r_f, p_f in sorted(fondre_parcels):
                opts.append(("FONDRE", d, r_f, p_f))
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            seat_o,
            tuple(opts),
            {"effect_kind": "G11_HARPIE", "face": face},
            slot_id="G11",
            profile="A",
            resume_tag="G11_ACT",
            resume_payload=(face,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G11_ACT" and ch != "PASSER":
            _g11_apply_option(state, ch, int(ctx["payload"][0]))
        elif tag == "G11_CARRY" and ch != "PASSER":
            opp_rank = int(ctx["payload"][0])
            s_h, d_h = int(ch[0]), int(ch[1])
            if is_reve_code(state.get_tactique_at_rank(opp_rank - 1)):
                state.place_defender_reve_standing(s_h, d_h, opp_rank)


# ---------------------------------------------------------------------------
# G12 — L'Ibijau (O>E)
# ---------------------------------------------------------------------------


def _g12_apply_move(state: GameState, seat_m: int, new_rank: int, face: int) -> None:
    card, d1, d2, _lec, bound_t = state.get_player_hand(seat_m)
    if not (1 <= card <= 12):
        return
    new_bound = new_rank if (bound_t > 0 or state.step != STEP_3_2_REVEAL) else 0
    state.set_player_hand(seat_m, card, d1, d2, new_rank, new_bound)
    if face == 2:
        state.mark_seat_ibijau_moved_f2(seat_m)


@register_tile("G12", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g12_ibijau_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G12 L'Ibijau v6.4 : déplace 1 dé mobile sur le dé écarté (+ dés ignorés Sabotage/Écaille & glissement Rêve F2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        n = state.cfg.n_players
        sab_ignored_dice: set[int] = set()
        if face == 2:
            for s_sb in range(n):
                c_sb, d1_sb, d2_sb, _, _ = state.get_player_hand(s_sb)
                if c_sb in (CARD_SABOTAGE, CARD_ECAILLE):
                    if 1 <= d1_sb <= TRACK_LEN:
                        sab_ignored_dice.add(d1_sb)
                    if 1 <= d2_sb <= TRACK_LEN:
                        sab_ignored_dice.add(d2_sb)

        opts: list[Any] = ["PASSER"]
        for s in range(n):
            if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
                continue
            card, _, _, lec_m, bound_t = state.get_player_hand(s)
            if not (1 <= card <= 12):
                continue
            eff_r = bound_t if is_tactique_code(bound_t) else (lec_m if state.step == STEP_3_2_REVEAL else 0)
            if eff_r == 0:
                continue
            r_m, mt_m = (card - 1) // 2, (card - 1) % 2
            pos_m, st_m, _ = state.get_machine_pos_status(r_m, mt_m)
            _, _, attacked = state.get_machine_turn_stats(r_m, mt_m)
            if (
                st_m != MACHINE_STATUS_NORMAL
                or pos_m == 0
                or attacked
                or state.is_machine_etouffee_this_turn(r_m, mt_m)
            ):
                continue
            cand_ranks: set[int] = set()
            disc = state.get_player_discarded_die(s)
            if 1 <= disc <= TRACK_LEN and disc != eff_r:
                cand_ranks.add(disc)
            if face == 2:
                for sd in sab_ignored_dice:
                    if sd != eff_r:
                        cand_ranks.add(sd)
            for nr in sorted(cand_ranks):
                opts.append((s, nr))

        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "O"),
            tuple(opts),
            {"effect_kind": "G12_IBIJAU", "face": face},
            slot_id="G12",
            profile="A",
            resume_tag="G12_MOVE",
            resume_payload=(face,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G12_MOVE" and ch != "PASSER":
            _g12_apply_move(state, int(ch[0]), int(ch[1]), int(ctx["payload"][0]))
        elif tag == "G12_F2_SLIDE_REVE" and ch == "GLISSER":
            r_num = int(ctx["payload"][0])
            cur_idx = state.find_tactique_rank(TILE_R_BASE + r_num)
            if cur_idx is not None:
                verb_glisser_reve(state, cur_idx)


# ---------------------------------------------------------------------------
# G13 — Le Tamanoir (M>I)
# ---------------------------------------------------------------------------


def _g13_adjacent_targeted_parcels(state: GameState, r: int, p: int) -> list[tuple[int, int]]:
    targeted = set(list_targeted_parcels(state))
    cands: list[tuple[int, int]] = []
    n = state.cfg.n_players
    p_fwd = state.next_non_razed_towards_heart(r, p)
    if p_fwd is not None and (r, p_fwd) in targeted:
        cands.append((r, p_fwd))
    p_back = state.next_non_razed_towards_border(r, p)
    if p_back is not None and (r, p_back) in targeted:
        cands.append((r, p_back))
    for nr in sorted({(r - 1) % n, (r + 1) % n}):
        if nr != r and (nr, p) in targeted and not state.is_route_forestiere(nr, p):
            cands.append((nr, p))
    return cands


def _g13_apply_opt(state: GameState, opt: tuple[Any, ...]) -> None:
    kind = str(opt[0])
    if kind == "RIPOSTE":
        sr, sp, dr, dp = int(opt[1]), int(opt[2]), int(opt[3]), int(opt[4])
        cur = state.get_parcel_insectes(sr, sp)
        if cur >= 1:
            state.set_parcel_insectes(sr, sp, cur - 1)
            prim_creation_entite(state, "INSECTE", ray=dr, p=dp, count=2, light_trigger=False)
    elif kind == "FALLBACK":
        prim_creation_entite(
            state, "INSECTE", ray=int(opt[1]), p=int(opt[2]), count=1, light_trigger=False
        )


@register_tile("G13", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g13_tamanoir_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G13 Le Tamanoir v6.4 : −1/+2 Insectes sur Nid >= 2 (projette sur cible adjacente F2), sinon +1 réserve."""
    if not state.cfg.has_insectes_peuple:
        return
    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        nids_ge2: list[tuple[int, int]] = []
        nids_all: list[tuple[int, int]] = []
        for m_num in range(1, 6):
            pos = state.get_nid_position(m_num)
            if pos is not None:
                rn, pn, _ = pos
                nids_all.append((rn, pn))
                if state.get_parcel_insectes(rn, pn) >= 2:
                    nids_ge2.append((rn, pn))

        opts: list[tuple[Any, ...]] = []
        if nids_ge2:
            for rn, pn in nids_ge2:
                opts.append(("RIPOSTE", rn, pn, rn, pn))
                if face == 2:
                    for dr, dp in _g13_adjacent_targeted_parcels(state, rn, pn):
                        opts.append(("RIPOSTE", rn, pn, dr, dp))
        elif nids_all:
            for rn, pn in nids_all:
                opts.append(("FALLBACK", rn, pn))
        else:
            d_st, dr, dp = state.get_duel_state()
            if d_st != DUEL_NONE and not state.is_route_forestiere(dr, dp):
                opts.append(("FALLBACK", dr, dp))
            for p_code in ("M", "I"):
                sp = state.cfg.seat_of_peuple(p_code)
                if sp is not None:
                    for p in range(1, state.cfg.p_max + 1):
                        if not state.is_route_forestiere(sp, p) and ("FALLBACK", sp, p) not in opts:
                            opts.append(("FALLBACK", sp, p))

        if not opts:
            return
        if len(opts) == 1:
            _g13_apply_opt(state, opts[0])
            return
        push_effect_decision(
            state,
            _gov(state, "M"),
            tuple(opts),
            {"effect_kind": "G13_TAMANOIR", "face": face},
            slot_id="G13",
            profile="A",
            resume_tag="G13_APPLY",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _g13_apply_opt(state, ctx["choice"])


# ---------------------------------------------------------------------------
# G14 — Le Téju (R>I)
# ---------------------------------------------------------------------------


def _g14_place_ponte(state: GameState, m_num: int) -> None:
    if state.count_total_ecailles_in_play() < MAX_ECAILLES:
        state.set_nid_ponte(m_num, True)
        return
    # Sinon prélève parmi les Écailles révélées à ce tour (déjà comptées dans ecaille_deck_count)
    if state.ecaille_deck_count >= 1:
        state.ecaille_deck_count -= 1
        state.set_nid_ponte(m_num, True)


def _g14_fallback(state: GameState) -> None:
    verb_semer_au_sac(state, "ECAILLE", 1)
    if state.get_croc_parcel() is not None:
        return
    ri_rays = {
        s for s in (state.cfg.seat_of_peuple("R"), state.cfg.seat_of_peuple("I")) if s is not None
    }
    cands = tuple((r, p) for r, p in list_targeted_parcels(state) if r in ri_rays)
    if len(cands) == 1:
        prim_creation_entite(state, "CROC", ray=cands[0][0], p=cands[0][1])
    elif len(cands) > 1:
        push_effect_decision(
            state,
            _gov(state, "R"),
            cands,
            {"effect_kind": "G14_FALLBACK_CROC"},
            slot_id="G14",
            profile="A",
            resume_tag="G14_CROC",
        )


@register_tile(
    "G14", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_PARADE_PONTE, HOOK_EFFECT_RESUME)
)
def g14_teju_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G14 Le Téju v6.4 : Écaille Ponte sous 1 Nid (2 en F2), éclot le Croc à la 1re frappe puis Sème Écaille."""
    if hook == HOOK_5_PARADE_PONTE:
        info = _find_gardien_case_and_face(state, 14)
        if info is None:
            return
        g14_face = info[1]
        m_num = int(ctx["m_num"])
        if not state.get_nid_ponte(m_num):
            return
        if g14_face == 1 and state.get_croc_parcel() is not None:
            return
        state.set_nid_ponte(m_num, False)
        state.clear_croc()  # Revient en réserve Reptile (y compris depuis le plateau en F2)
        verb_semer_au_sac(state, "ECAILLE", 1)
        ctx["hatched"] = True
        return

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        max_pontes = 1 if face == 1 else 2
        free_nids = tuple(
            m_num
            for m_num in range(1, 6)
            if state.get_nid_position(m_num) is not None and not state.get_nid_ponte(m_num)
        )
        has_revealed_ecaille = state.ecaille_deck_count >= 1 and any(
            state.get_player_hand(s)[0] == CARD_ECAILLE for s in range(state.cfg.n_players)
        )
        can_take_ecaille = state.count_total_ecailles_in_play() < MAX_ECAILLES or has_revealed_ecaille

        if free_nids and state.count_nid_pontes() < max_pontes and can_take_ecaille:
            if len(free_nids) == 1:
                _g14_place_ponte(state, free_nids[0])
                return
            push_effect_decision(
                state,
                _gov(state, "R"),
                free_nids,
                {"effect_kind": "G14_POSE_PONTE", "face": face},
                slot_id="G14",
                profile="A",
                resume_tag="G14_PONTE",
            )
            return

        _g14_fallback(state)
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "G14_PONTE":
            _g14_place_ponte(state, int(ch))
        elif tag == "G14_CROC":
            prim_creation_entite(state, "CROC", ray=int(ch[0]), p=int(ch[1]))


# ---------------------------------------------------------------------------
# G15 — Le Colibri (O>I)
# ---------------------------------------------------------------------------


def _g15_sources(state: GameState) -> tuple[tuple[Any, ...], ...]:
    if state.count_total_insects_on_board() == 0:
        return (("RESERVE",),)
    srcs: list[tuple[Any, ...]] = []
    for c in range(1, TRACK_LEN + 1):
        if state.get_colonie_at_case(c) >= 1:
            srcs.append(("COLONIE", c))
    for c in range(1, TRACK_LEN + 1):
        if state.get_bugs_at_case(c) >= 1:
            srcs.append(("BUG", c))
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if state.get_parcel_insectes(r, p) >= 1:
                srcs.append(("PARCEL", r, p))
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if state.get_machine_passenger_insects(r, mt) >= 1:
                srcs.append(("PASSENGER", r, mt))
    return tuple(srcs)


def _g15_dests(state: GameState, face: int, rank_drop_used: bool) -> tuple[tuple[Any, ...], ...]:
    dsts: list[tuple[Any, ...]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(r, p):
                dsts.append(("FORET", r, p))
    if face == 2 and not rank_drop_used:
        p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
        if p_face != PERCHOIR_NONE and p_kind == PERCHOIR_KIND_RANK:
            dsts.append(("BUG", p_idx + 1))
    return tuple(dsts)


def _g15_prompt_step(
    state: GameState, face: int, remaining: int, rank_drop_used: bool
) -> None:
    if remaining <= 0 or not state.cfg.has_insectes_peuple:
        return
    srcs = _g15_sources(state)
    dsts = _g15_dests(state, face, rank_drop_used)
    if not srcs or not dsts:
        return
    # Limiter le produit cartésien en sélectionnant d'abord la source puis la destination si besoin
    if len(srcs) == 1:
        push_effect_decision(
            state,
            _gov(state, "O"),
            ("PASSER", *dsts) if remaining < face else dsts,
            {"effect_kind": "G15_COLIBRI_DST", "face": face, "src": srcs[0], "remaining": remaining},
            slot_id="G15",
            profile="A",
            resume_tag="G15_DST",
            resume_payload=(face, remaining, 1 if rank_drop_used else 0, srcs[0]),
        )
        return
    push_effect_decision(
        state,
        _gov(state, "O"),
        ("PASSER", *srcs) if remaining < face else srcs,
        {"effect_kind": "G15_COLIBRI_SRC", "face": face, "remaining": remaining},
        slot_id="G15",
        profile="A",
        resume_tag="G15_SRC",
        resume_payload=(face, remaining, 1 if rank_drop_used else 0),
    )


@register_tile(
    "G15", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_REPOUSSE_FINALE, HOOK_EFFECT_RESUME)
)
def g15_colibri_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """G15 Le Colibri v6.4 : transport 1 Insecte (2 en F2) + encoche passive si icône Gardien + Enraciné."""
    if hook == HOOK_REPOUSSE_FINALE:
        if ctx.get("phase") != "ROOTED_TILE" or ctx.get("slot_id") != "G15":
            return
        seat_o = state.cfg.seat_of_peuple("O")
        if seat_o is None:
            return
        n = state.cfg.n_players
        allowed_rays = {seat_o, (seat_o - 1) % n, (seat_o + 1) % n}
        for _s_idx, tid, r_other, _sl, _tier in state.list_rooted_tiles():
            if tid != "G15" and r_other in allowed_rays:
                _regrow_one_souche_on_ray(state, r_other)
        return

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx.get("face", 1))
        _g15_prompt_step(state, face, 1 if face == 1 else 2, False)
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        if tag == "G15_SRC":
            face, rem, rd_i = int(ctx["payload"][0]), int(ctx["payload"][1]), int(ctx["payload"][2])
            dsts = _g15_dests(state, face, bool(rd_i))
            if not dsts:
                return
            push_effect_decision(
                state,
                _gov(state, "O"),
                dsts,
                {"effect_kind": "G15_COLIBRI_DST", "face": face, "src": ch, "remaining": rem},
                slot_id="G15",
                profile="A",
                resume_tag="G15_DST",
                resume_payload=(face, rem, rd_i, ch),
            )
            return
        if tag == "G15_DST":
            face = int(ctx["payload"][0])
            rem = int(ctx["payload"][1])
            rd_used = bool(ctx["payload"][2])
            src = ctx["payload"][3]
            ok, col_case = prim_insecte_take_with_priming(state, src)
            if not ok:
                return
            if (
                col_case > 0
                and state.get_gardien_at_case(col_case)[0] > 0
                and state.count_gardien_pari_defenders_at_case(col_case) >= 1
            ):
                # Prélèvement sur icône Gardien : glisse 1 pari en encoche SANS pouvoir ni Résonance
                prim_partage_info_etat_gardien(
                    state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=col_case
                )
            if ch[0] == "BUG":
                prim_creation_entite(state, "BUG", p=int(ch[1]), count=1, light_trigger=False)
                rd_used = True
            else:
                dr, dp = int(ch[1]), int(ch[2])
                prim_creation_entite(state, "INSECTE", ray=dr, p=dp, count=1, light_trigger=False)
                if face == 2 and state.get_parcel_nid(dr, dp)[0] > 0:
                    prim_creation_entite(
                        state, "INSECTE", ray=dr, p=dp, count=1, light_trigger=False
                    )
            if rem > 1:
                _g15_prompt_step(state, face, rem - 1, rd_used)
