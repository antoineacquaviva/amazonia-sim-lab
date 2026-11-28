"""Catalogue Canon v6.4 — Les 10 Rêves / Grandes Cartes (R1..R10, profil 'A').

100 % stateless, stdlib pure PyPy 3.11, zéro `_buf`, zéro `random`, zéro dette mémorielle (`mem_debt == 0`).
Source de vérité : `contracts/tiles_canon_v6_4.json`.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_ECAILLE_REVELEE,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_5_CIBLAGE_MACHINE,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_EFFECT_RESUME,
    HOOK_MACHINE_RECUL,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_deplacement_nid,
    prim_insecte_take_with_priming,
    prim_permutation_piste,
    push_effect_decision,
    verb_alterer,
    verb_etouffer,
    verb_glisser_reve,
    verb_refroidir,
    verb_semer_au_sac,
)
from engine.state import (
    CHAMAN_TAMBOUR,
    DUEL_DEFI,
    DUEL_NONE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    PERCHOIR_KIND_RANK,
    PERCHOIR_KIND_RAY,
    TILE_R_BASE,
    TRACK_LEN,
    TRIG_REVE,
    GameState,
    is_reve_code,
)

__all__ = (
    "r1_liane_esprits_v6_4",
    "r2_fleuve_cendre_v6_4",
    "r3_chamane_jaguar_v6_4",
    "r4_pirogue_anaconda_v6_4",
    "r5_ciel_deux_eaux_v6_4",
    "r6_tucandeira_v6_4",
    "r7_curupira_v6_4",
    "r8_mue_obsidienne_v6_4",
    "r9_matinta_pereira_v6_4",
    "r10_ruche_vagabonde_v6_4",
)

ENTITY_REVE_NUMS: tuple[int, ...] = (2, 7, 8, 9, 10)


def _gov(state: GameState, peuple: str) -> int:
    for s, p in enumerate(state.cfg.peuples):
        if p == peuple:
            return s
    return state.coordonnateur


def _peuple_rays(state: GameState, *peuples: str) -> tuple[int, ...]:
    out: list[int] = []
    for s, p in enumerate(state.cfg.peuples):
        if p in peuples:
            out.append(s)
    return tuple(out)


def _is_tambour(state: GameState, seat: int, def_idx: int) -> bool:
    return (
        state.cfg.peuples[seat] == "H"
        and state.get_humain_chaman_archetype(def_idx) == CHAMAN_TAMBOUR
    )


def _find_tambour(state: GameState) -> tuple[int, int] | None:
    for s in range(state.cfg.n_players):
        if state.cfg.peuples[s] != "H":
            continue
        for d in (0, 1):
            if state.get_humain_chaman_archetype(d) == CHAMAN_TAMBOUR:
                return (s, d)
    return None


def _slidable_reve_indices(state: GameState) -> tuple[int, ...]:
    out: list[int] = []
    for idx in range(1, TRACK_LEN):
        if is_reve_code(state.get_tactique_at_rank(idx)) and not is_reve_code(
            state.get_tactique_at_rank(idx - 1)
        ):
            out.append(idx)
    return tuple(out)


def _alterable_mobiles(
    state: GameState, allowed_rays: tuple[int, ...] | None = None
) -> tuple[tuple[int, int], ...]:
    rays = range(state.cfg.n_players) if allowed_rays is None else allowed_rays
    out: list[tuple[int, int]] = []
    for r in rays:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(r, mt):
                out.append((r, mt))
    return tuple(out)


def _coolable_machines(
    state: GameState, allowed_rays: tuple[int, ...] | None = None
) -> tuple[tuple[int, int], ...]:
    rays = range(state.cfg.n_players) if allowed_rays is None else allowed_rays
    out: list[tuple[int, int]] = []
    for r in rays:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0 and state.get_machine_tokens(r, mt)[0] >= 1:
                out.append((r, mt))
    return tuple(out)


def _active_mobile_seats(state: GameState) -> list[tuple[int, int, int, int]]:
    """Retourne `(seat, ray, m_type, lec_m)` pour toutes les mobiles encore actives à l'ouverture."""
    out: list[tuple[int, int, int, int]] = []
    for s in range(state.cfg.n_players):
        if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
            continue
        card, _, _, lec_m, _ = state.get_player_hand(s)
        if 1 <= card <= 12 and 1 <= lec_m <= TRACK_LEN:
            r, mt = (card - 1) // 2, (card - 1) % 2
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.is_machine_etouffee_this_turn(r, mt):
                out.append((s, r, mt, lec_m))
    return out


# ---------------------------------------------------------------------------
# R1 — La Liane des Esprits (H>E)
# ---------------------------------------------------------------------------


def _r1_pull_and_echo(state: GameState, e_num: int) -> None:
    r1_idx = state.find_tactique_rank(TILE_R_BASE + 1)
    e_idx = state.find_tactique_rank(TILE_R_BASE + e_num)
    if r1_idx is None or e_idx is None or e_idx <= r1_idx:
        return

    if e_idx == r1_idx + 1:
        # Déjà collé contre R1 : Glisser la paire ensemble d'1 rang libre vers la gauche
        if r1_idx > 0 and not is_reve_code(state.get_tactique_at_rank(r1_idx - 1)):
            state.move_reve_to_free_rank(r1_idx, r1_idx - 1)
            state.move_reve_to_free_rank(e_idx, r1_idx)
    else:
        # Glisser e_num jusqu'au rang libre immédiatement à droite de R1
        dst_free: int | None = None
        for k in range(r1_idx + 1, e_idx):
            if not is_reve_code(state.get_tactique_at_rank(k)):
                dst_free = k
                break
        if dst_free is not None:
            state.move_reve_to_free_rank(e_idx, dst_free)

    # Écho chamane : si le Tambour défendait R1 et que le Rêve Entités tiré n'est pas défendu,
    # il peut aussitôt passer debout sur ce Rêve afin qu'il se résolve à son tour.
    r1_cur = state.find_tactique_rank(TILE_R_BASE + 1)
    e_cur = state.find_tactique_rank(TILE_R_BASE + e_num)
    if r1_cur is None or e_cur is None:
        return
    if state.has_reve_opened_this_turn(e_num):
        return
    if state.count_reve_activation_defenders_at_case(e_cur + 1) >= 1:
        return
    tambour_on_r1: tuple[int, int] | None = None
    for s, d in state.list_defenders_on_reve_case(r1_cur + 1):
        if _is_tambour(state, s, d):
            tambour_on_r1 = (s, d)
            break
    if tambour_on_r1 is None:
        return
    push_effect_decision(
        state,
        _gov(state, "H"),
        ("PASSER_TAMBOUR", "PASSER"),
        {
            "effect_kind": "R1_ECHO_TAMBOUR",
            "e_num": e_num,
            "target_case": e_cur + 1,
        },
        slot_id="R1",
        profile="A",
        resume_tag="R1_ECHO",
        resume_payload=(tambour_on_r1[0], tambour_on_r1[1], e_num),
    )


@register_tile("R1", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r1_liane_esprits_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R1 La Liane des Esprits v6.4 : tire 1 Rêve Entités + Écho Tambour debout + Enracinement sans bloquer Sommeil."""
    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        r1_idx = state.find_tactique_rank(TILE_R_BASE + 1)
        if r1_idx is None:
            return
        entity_right: list[int] = []
        for idx in range(r1_idx + 1, TRACK_LEN):
            code = state.get_tactique_at_rank(idx)
            if is_reve_code(code):
                rn = code - TILE_R_BASE
                if rn in ENTITY_REVE_NUMS:
                    entity_right.append(rn)
        if len(entity_right) == 1:
            _r1_pull_and_echo(state, entity_right[0])
            return
        if len(entity_right) > 1:
            push_effect_decision(
                state,
                _gov(state, "H"),
                tuple(entity_right),
                {"effect_kind": "R1_PULL_ENTITY", "r1_case": r1_idx + 1},
                slot_id="R1",
                profile="A",
                resume_tag="R1_PULL",
            )
            return

        # Aucun Rêve Entités à droite : glisse R1 d'1 rang libre à gauche,
        # sinon Étouffe 1 mobile supplémentaire sur son rang.
        if r1_idx > 0 and not is_reve_code(state.get_tactique_at_rank(r1_idx - 1)):
            verb_glisser_reve(state, r1_idx)
            return
        extras = [s for s, _r, _mt, lm in _active_mobile_seats(state) if lm == r1_idx + 1]
        if len(extras) == 1:
            s0 = extras[0]
            card = state.get_player_hand(s0)[0]
            verb_etouffer(state, (card - 1) // 2, (card - 1) % 2, seat=s0)
            state.mark_seat_cancelled_by_reve_this_turn(s0)
            state.light_trigger(TRIG_REVE)
        elif len(extras) > 1:
            push_effect_decision(
                state,
                _gov(state, "H"),
                tuple(extras),
                {"effect_kind": "R1_EXTRA_ETOUFFER", "case": r1_idx + 1},
                slot_id="R1",
                profile="A",
                resume_tag="R1_EXTRA",
            )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "R1_PULL":
            _r1_pull_and_echo(state, int(ch))
        elif tag == "R1_ECHO":
            if ch == "PASSER_TAMBOUR":
                s_t, d_t, e_num = int(ctx["payload"][0]), int(ctx["payload"][1]), int(ctx["payload"][2])
                e_cur = state.find_tactique_rank(TILE_R_BASE + e_num)
                if e_cur is not None and not state.has_reve_opened_this_turn(e_num):
                    state.place_defender_reve_standing(s_t, d_t, e_cur + 1)
        elif tag == "R1_EXTRA":
            s0 = int(ch)
            card = state.get_player_hand(s0)[0]
            if 1 <= card <= 12:
                verb_etouffer(state, (card - 1) // 2, (card - 1) % 2, seat=s0)
                state.mark_seat_cancelled_by_reve_this_turn(s0)
                state.light_trigger(TRIG_REVE)


# ---------------------------------------------------------------------------
# R2 — Le Fleuve sous la cendre (E>H)
# ---------------------------------------------------------------------------


@register_tile("R2", "A", hooks=(HOOK_3_2_REVELATION, HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r2_fleuve_cendre_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R2 Le Fleuve sous la cendre v6.4 : Linceul de cendre (jetons face cachée 0 Furtivité), Altérer/Tambour, Gué marqué."""
    if hook == HOOK_3_2_REVELATION and ctx.get("phase") == "ALTERATION_LOST":
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        r2_idx = state.find_tactique_rank(TILE_R_BASE + 2)
        if r2_idx is not None and len(state.list_defenders_on_reve_case(r2_idx + 1)) >= 1:
            state.mark_machine_facedown_this_turn(ray, m_type)
            return
        r2_slot = state.find_lisiere_slot_by_tile_id("R2")
        if r2_slot is not None:
            rinfo = state.get_slot_rooted_info(r2_slot)
            if rinfo is not None and rinfo[0] == ray:
                state.mark_machine_facedown_this_turn(ray, m_type)
        return

    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        # Toute machine Étouffée par R2 retourne son jeton face cachée (compte 0 en Furtivité)
        for s_raw in ctx.get("cancelled_seats", ()):
            card = state.get_player_hand(int(s_raw))[0]
            if 1 <= card <= 12:
                state.mark_machine_facedown_this_turn((card - 1) // 2, (card - 1) % 2)

        r2_idx = state.find_tactique_rank(TILE_R_BASE + 2)
        tambour = _find_tambour(state)
        tambour_in_forest = False
        if tambour is not None:
            raw_t = state.get_player_def_loc_raw(tambour[0], tambour[1])
            tambour_in_forest = state.decode_def_loc(raw_t)[0] == "FORET"

        allowed_rays = None if tambour_in_forest else _peuple_rays(state, "E", "H")
        opts: list[Any] = ["PASSER"]
        for r, mt in _alterable_mobiles(state, allowed_rays):
            opts.append(("ALTERER", r, mt))

        if tambour is not None and r2_idx is not None:
            waiting = state.list_available_waiting_defenders()
            if tambour in waiting:
                for idx in range(r2_idx + 1, TRACK_LEN):
                    code = state.get_tactique_at_rank(idx)
                    if is_reve_code(code):
                        rn = code - TILE_R_BASE
                        if (
                            not state.has_reve_opened_this_turn(rn)
                            and state.count_reve_activation_defenders_at_case(idx + 1) == 0
                        ):
                            opts.append(("TAMBOUR", rn))

        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(opts),
            {"effect_kind": "R2_FLEUVE_CHOICE", "tambour_in_forest": tambour_in_forest},
            slot_id="R2",
            profile="A",
            resume_tag="R2_ACT",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        kind = str(ch[0])
        if kind == "ALTERER":
            verb_alterer(state, int(ch[1]), int(ch[2]))
        elif kind == "TAMBOUR":
            rn = int(ch[1])
            tambour = _find_tambour(state)
            dst_idx = state.find_tactique_rank(TILE_R_BASE + rn)
            if tambour is not None and dst_idx is not None and not state.has_reve_opened_this_turn(rn):
                state.place_defender_reve_standing(tambour[0], tambour[1], dst_idx + 1)


# ---------------------------------------------------------------------------
# R3 — Le Chamane-Jaguar (H>M)
# ---------------------------------------------------------------------------


def _r3_destinations(
    state: GameState, cancelled_rays: tuple[int, ...], cancelled_machines: tuple[tuple[int, int], ...]
) -> tuple[tuple[int, int], ...]:
    dests: set[tuple[int, int]] = set()
    d_st, d_r, d_p = state.get_duel_state()
    if d_st != DUEL_NONE and not state.is_route_forestiere(d_r, d_p):
        dests.add((d_r, d_p))

    if cancelled_rays:
        ray_set = set(cancelled_rays)
        targeted_on_rays = [
            (r, p) for (r, p) in list_targeted_parcels(state) if r in ray_set
        ]
        for rp in targeted_on_rays:
            dests.add(rp)
        # Si la machine tout juste Étouffée était la seule source de ciblage de son rayon,
        # sa parcelle actuelle (et sa cible Devant non-Route) reste une parcelle ciblée du rayon.
        for r_m, mt_m in cancelled_machines:
            pos_m, st_m, _ = state.get_machine_pos_status(r_m, mt_m)
            if st_m != MACHINE_STATUS_RETIRED and pos_m > 0:
                if not state.is_route_forestiere(r_m, pos_m):
                    dests.add((r_m, pos_m))
                p_dev = state.next_non_razed_towards_heart(r_m, pos_m)
                if p_dev is not None and not state.is_route_forestiere(r_m, p_dev):
                    dests.add((r_m, p_dev))
    else:
        for r in _peuple_rays(state, "H", "M"):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p):
                    dests.add((r, p))
    return tuple(sorted(dests))


def _r3_prompt_next(
    state: GameState,
    defs: tuple[tuple[int, int], ...],
    idx: int,
    cancelled_rays: tuple[int, ...],
    cancelled_machines: tuple[tuple[int, int], ...],
) -> None:
    if idx >= len(defs):
        return
    s, d = defs[idx]
    dests = _r3_destinations(state, cancelled_rays, cancelled_machines)
    if not dests:
        _r3_prompt_next(state, defs, idx + 1, cancelled_rays, cancelled_machines)
        return
    is_tambour = _is_tambour(state, s, d)
    opts: list[Any] = ["PASSER"]
    for r, p in dests:
        opts.append(("JUMP", r, p))
    if is_tambour and state.cfg.accessories_enabled:
        for r, p in dests:
            opts.append(("JUMP_DUEL", r, p))
    push_effect_decision(
        state,
        s,
        tuple(opts),
        {"effect_kind": "R3_CHAMANE_JAGUAR_BOND", "is_tambour": is_tambour, "seat": s, "def_idx": d},
        slot_id="R3",
        profile="A",
        resume_tag="R3_JUMP",
        resume_payload=(defs, idx, cancelled_rays, cancelled_machines),
    )


@register_tile("R3", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r3_chamane_jaguar_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R3 Le Chamane-Jaguar v6.4 : bond des Défenseurs vers Duel/rayon ciblé + Écho Tambour emportant le Duel."""
    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        cur_case = int(ctx["case"])
        defs = tuple(state.list_defenders_on_reve_case(cur_case))
        if not defs:
            return
        c_rays: set[int] = set()
        c_machs: list[tuple[int, int]] = []
        for s_raw in ctx.get("cancelled_seats", ()):
            card = state.get_player_hand(int(s_raw))[0]
            if 1 <= card <= 12:
                r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                c_rays.add(r_m)
                c_machs.append((r_m, mt_m))
        _r3_prompt_next(state, defs, 0, tuple(sorted(c_rays)), tuple(c_machs))
        return

    if hook == HOOK_EFFECT_RESUME:
        defs, idx, c_rays_t, c_machs_t = ctx["payload"]
        ch = ctx["choice"]
        s, d = defs[int(idx)]
        if ch != "PASSER":
            mode, dst_r, dst_p = str(ch[0]), int(ch[1]), int(ch[2])
            prim_deplacement(
                state, "DEFENSEUR", src_seat=s, src_def_idx=d, dst_ray=dst_r, dst_p=dst_p
            )
            if mode == "JUMP_DUEL" and state.cfg.accessories_enabled:
                d_st, _, _ = state.get_duel_state()
                face = d_st if d_st != DUEL_NONE else DUEL_DEFI
                state.set_duel_state_at(dst_r, dst_p, face)
        _r3_prompt_next(state, defs, int(idx) + 1, c_rays_t, c_machs_t)


# ---------------------------------------------------------------------------
# R4 — La Pirogue-Anaconda (H>R)
# ---------------------------------------------------------------------------


@register_tile("R4", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r4_pirogue_anaconda_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R4 La Pirogue-Anaconda v6.4 : Poussée collective (si en queue) ou Retour (échange à droite) + Semer 1 Écaille."""
    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        r4_idx = state.find_tactique_rank(TILE_R_BASE + 4)
        if r4_idx is None:
            return
        reve_ranks = [i for i in range(TRACK_LEN) if is_reve_code(state.get_tactique_at_rank(i))]
        is_rightmost = r4_idx == max(reve_ranks)
        can_poussee = is_rightmost and any(
            i > 0 and not is_reve_code(state.get_tactique_at_rank(i - 1)) for i in reve_ranks
        )
        can_retour = any(i > r4_idx for i in reve_ranks)
        opts: list[str] = ["PASSER"]
        if can_poussee:
            opts.append("POUSSEE")
        if can_retour:
            opts.append("RETOUR")
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(opts),
            {"effect_kind": "R4_PIROGUE", "r4_case": r4_idx + 1},
            slot_id="R4",
            profile="A",
            resume_tag="R4_ACT",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = str(ctx["choice"])
        if ch == "POUSSEE":
            moved = False
            for idx in range(1, TRACK_LEN):
                if (
                    is_reve_code(state.get_tactique_at_rank(idx))
                    and not is_reve_code(state.get_tactique_at_rank(idx - 1))
                    and verb_glisser_reve(state, idx)
                ):
                    moved = True
            if moved:
                verb_semer_au_sac(state, "ECAILLE", 1)
        elif ch == "RETOUR":
            r4_idx = state.find_tactique_rank(TILE_R_BASE + 4)
            if r4_idx is not None:
                right_reves = [
                    i
                    for i in range(r4_idx + 1, TRACK_LEN)
                    if is_reve_code(state.get_tactique_at_rank(i))
                ]
                if right_reves:
                    prim_permutation_piste(
                        state, "SWAP_RANKS", rank_a=r4_idx, rank_b=right_reves[0]
                    )
                    verb_semer_au_sac(state, "ECAILLE", 1)


# ---------------------------------------------------------------------------
# R5 — Le Ciel à deux eaux (H>O)
# ---------------------------------------------------------------------------


def _r5_seat_in_perchoir(state: GameState, ray: int, lec_m: int) -> bool:
    p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
    if p_face == 0:
        return False
    if p_kind == PERCHOIR_KIND_RANK and 0 <= p_idx < TRACK_LEN:
        return lec_m == (p_idx + 1)
    if p_kind == PERCHOIR_KIND_RAY and state.oiseau_perchoir_card != 0:
        return ray == p_idx
    return False


def _r5_perchoir_active(state: GameState) -> bool:
    p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
    if p_face == 0:
        return False
    return (p_kind == PERCHOIR_KIND_RANK and 0 <= p_idx < TRACK_LEN) or (
        p_kind == PERCHOIR_KIND_RAY and state.oiseau_perchoir_card != 0
    )


@register_tile("R5", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r5_ciel_deux_eaux_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R5 Le Ciel à deux eaux v6.4 : échange miroir ±3 (avant annulations) + Écho Chant (bascule seule) & Tambour (Refroidir)."""
    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "PRE_CANCEL":
        cur_case = int(ctx["case"])
        has_chant = state.is_chant_on_reve_case(cur_case)
        has_tambour = state.is_tambour_on_reve_case(cur_case)
        actives = _active_mobile_seats(state)
        if not actives:
            return

        p_act = _r5_perchoir_active(state)
        all_swaps: list[tuple[str, int, int]] = []
        perch_swaps: list[tuple[str, int, int]] = []
        for i in range(len(actives)):
            s1, r1, _, lm1 = actives[i]
            for j in range(i + 1, len(actives)):
                s2, r2, _, lm2 = actives[j]
                if abs(lm1 - lm2) == 3:
                    item = ("SWAP", s1, s2)
                    all_swaps.append(item)
                    if p_act and (
                        _r5_seat_in_perchoir(state, r1, lm1) or _r5_seat_in_perchoir(state, r2, lm2)
                    ):
                        perch_swaps.append(item)
        swaps = perch_swaps if perch_swaps else all_swaps

        flips: list[tuple[str, int, int]] = []
        if has_chant:
            all_flips: list[tuple[str, int, int]] = []
            perch_flips: list[tuple[str, int, int]] = []
            for s1, r1, _, lm1 in actives:
                mirror = lm1 + 3 if lm1 <= 3 else lm1 - 3
                item_f = ("FLIP", s1, mirror)
                all_flips.append(item_f)
                if p_act and _r5_seat_in_perchoir(state, r1, lm1):
                    perch_flips.append(item_f)
            flips = perch_flips if perch_flips else all_flips

        opts: list[Any] = ["PASSER", *swaps, *flips]
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(opts),
            {
                "effect_kind": "R5_CIEL_EAUX",
                "r5_case": cur_case,
                "has_chant": has_chant,
                "has_tambour": has_tambour,
            },
            slot_id="R5",
            profile="A",
            resume_tag="R5_MOVE",
            resume_payload=(1 if has_tambour else 0,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "R5_MOVE":
            if ch == "PASSER":
                return
            has_tambour = bool(ctx["payload"][0])
            kind = str(ch[0])
            moved_seats: list[int] = []
            if kind == "SWAP":
                s1, s2 = int(ch[1]), int(ch[2])
                prim_permutation_piste(state, "SWAP_MACHINE_RANKS", seat_a=s1, seat_b=s2)
                moved_seats = [s1, s2]
            elif kind == "FLIP":
                s1, dst_rank = int(ch[1]), int(ch[2])
                card, d1, d2, _, _ = state.get_player_hand(s1)
                state.set_player_hand(s1, card, d1, d2, dst_rank, dst_rank)
                moved_seats = [s1]
            if has_tambour and moved_seats:
                cool_cands: list[tuple[int, int]] = []
                for sm in moved_seats:
                    card = state.get_player_hand(sm)[0]
                    if 1 <= card <= 12:
                        rm, mtm = (card - 1) // 2, (card - 1) % 2
                        if state.get_machine_tokens(rm, mtm)[0] >= 1:
                            cool_cands.append((rm, mtm))
                if len(cool_cands) == 1:
                    verb_refroidir(state, cool_cands[0][0], cool_cands[0][1], 1)
                elif len(cool_cands) > 1:
                    push_effect_decision(
                        state,
                        _gov(state, "H"),
                        tuple(cool_cands),
                        {"effect_kind": "R5_TAMBOUR_REFROIDIR"},
                        slot_id="R5",
                        profile="A",
                        resume_tag="R5_COOL",
                    )
        elif tag == "R5_COOL":
            verb_refroidir(state, int(ch[0]), int(ch[1]), 1)


# ---------------------------------------------------------------------------
# R6 — La Tucandeira (H>I)
# ---------------------------------------------------------------------------


def _r6_prompt_pick(
    state: GameState, cur_case: int, allowed_rays: tuple[int, ...], rem: int
) -> None:
    if rem <= 0:
        return
    opts: list[Any] = ["PASSER"]
    if state.count_total_insects_on_board() == 0:
        if state.cfg.has_insectes_peuple:
            opts.append(("RESERVE",))
    else:
        for r in allowed_rays:
            for p in range(1, state.cfg.p_max + 1):
                if state.get_parcel_insectes(r, p) >= 1:
                    opts.append(("PARCEL", r, p))
    if len(opts) <= 1:
        return
    push_effect_decision(
        state,
        _gov(state, "H"),
        tuple(opts),
        {"effect_kind": "R6_CUEILLIR", "case": cur_case, "rem": rem},
        slot_id="R6",
        profile="A",
        resume_tag="R6_PICK",
        resume_payload=(cur_case, allowed_rays, rem),
    )


def _r6_prompt_sting(state: GameState, cur_case: int, has_chant: bool) -> None:
    if state.get_bugs_at_case(cur_case) < 1:
        return
    allowed_ranks = {cur_case}
    if has_chant:
        if cur_case > 1:
            allowed_ranks.add(cur_case - 1)
        if cur_case < TRACK_LEN:
            allowed_ranks.add(cur_case + 1)
    targets = tuple(s for s, _r, _mt, lm in _active_mobile_seats(state) if lm in allowed_ranks)
    if not targets:
        return
    push_effect_decision(
        state,
        _gov(state, "H"),
        ("PASSER", *targets),
        {"effect_kind": "R6_PIQURES", "case": cur_case, "has_chant": has_chant},
        slot_id="R6",
        profile="A",
        resume_tag="R6_STING",
        resume_payload=(cur_case, 1 if has_chant else 0),
    )


@register_tile("R6", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r6_tucandeira_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R6 La Tucandeira v6.4 : cueillette (+ amorçage natif + Écho Tambour) & piqûres d'Étouffement (+ Écho Chant ±1)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        phase = str(ctx.get("phase", ""))
        cur_case = int(ctx["case"])
        if phase == "PRE_CANCEL":
            has_tambour = state.is_tambour_on_reve_case(cur_case)
            allowed_rays = _peuple_rays(state, "H", "I") if has_tambour else _peuple_rays(state, "H")
            _r6_prompt_pick(state, cur_case, allowed_rays, 2 if has_tambour else 1)
            return
        if phase == "OPEN":
            has_chant = state.is_chant_on_reve_case(cur_case)
            _r6_prompt_sting(state, cur_case, has_chant)
            return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        if tag == "R6_PICK":
            cur_case, allowed_rays, rem = int(ctx["payload"][0]), ctx["payload"][1], int(ctx["payload"][2])
            ok, _ = prim_insecte_take_with_priming(state, ch)
            if ok:
                prim_creation_entite(state, "BUG", p=cur_case, count=1, light_trigger=False)
            _r6_prompt_pick(state, cur_case, allowed_rays, rem - 1)
        elif tag == "R6_STING":
            cur_case, has_chant_i = int(ctx["payload"][0]), int(ctx["payload"][1])
            s_t = int(ch)
            bugs = state.get_bugs_at_case(cur_case)
            card = state.get_player_hand(s_t)[0]
            if bugs >= 1 and 1 <= card <= 12:
                state.set_bugs_at_case(cur_case, bugs - 1)
                verb_etouffer(state, (card - 1) // 2, (card - 1) % 2, seat=s_t)
                state.mark_seat_cancelled_by_reve_this_turn(s_t)
                state.light_trigger(TRIG_REVE)
            _r6_prompt_sting(state, cur_case, bool(has_chant_i))


# ---------------------------------------------------------------------------
# R7 — Le Curupira (E>M)
# ---------------------------------------------------------------------------


@register_tile(
    "R7",
    "A",
    hooks=(
        HOOK_5_CIBLAGE_MACHINE,
        HOOK_5_FIN_ATTAQUE_MACHINE,
        HOOK_5_LAW_QUERY,
        HOOK_MACHINE_RECUL,
        HOOK_3_2_OUVERTURE_REVE,
    ),
)
def r7_curupira_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """R7 Le Curupira v6.4 : loi passive marche à reculons + tout Recul hors Duel Défi -> Territoire tenu + Altérer sur Étouffées."""
    r7_idx = state.find_tactique_rank(TILE_R_BASE + 7)
    r7_rank = (r7_idx + 1) if r7_idx is not None else 0

    if hook == HOOK_5_LAW_QUERY:
        return (
            r7_rank > 0
            and not bool(ctx.get("is_ratissage"))
            and int(ctx.get("tactique_code", 0)) == r7_rank
        )

    if hook == HOOK_5_CIBLAGE_MACHINE:
        if (
            r7_rank > 0
            and not bool(ctx.get("is_ratissage"))
            and int(ctx.get("tactique_code", 0)) == r7_rank
        ):
            ray = int(ctx["ray"])
            pos = int(ctx["pos"])
            new_targets: list[tuple[str, int]] = []
            for c_type, tp in ctx["targets"]:
                if c_type == "DEVANT":
                    p_back = state.next_non_razed_towards_border(ray, pos)
                    if p_back is not None:
                        new_targets.append(("DEVANT", p_back))
                else:
                    new_targets.append((c_type, tp))
            ctx["targets"] = new_targets
        return None

    if hook == HOOK_5_FIN_ATTAQUE_MACHINE:
        if (
            r7_rank > 0
            and not bool(ctx.get("is_ratissage"))
            and int(ctx.get("tactique_code", 0)) == r7_rank
        ):
            ctx["reverse_advance"] = True
            ctx["no_red_on_sur_place"] = True
        return None

    if hook == HOOK_MACHINE_RECUL:
        if r7_rank > 0:
            ray = int(ctx["ray"])
            old_pos = int(ctx["old_pos"])
            d_st, d_r, d_p = state.get_duel_state()
            if d_st == DUEL_DEFI and d_r == ray and d_p == old_pos:
                state.flip_duel_to_territoire_tenu()
        return None

    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        for s_raw in ctx.get("cancelled_seats", ()):
            card = state.get_player_hand(int(s_raw))[0]
            if 1 <= card <= 12:
                verb_alterer(state, (card - 1) // 2, (card - 1) % 2)
        return None
    return None


# ---------------------------------------------------------------------------
# R8 — La Mue d'obsidienne (E>R)
# ---------------------------------------------------------------------------


def _r8_prompt_step2(state: GameState) -> None:
    opts: list[Any] = ["PASSER"]
    for r, mt in _alterable_mobiles(state):
        opts.append(("ALTERER", r, mt))
    for r, mt in _coolable_machines(state):
        opts.append(("REFROIDIR", r, mt))
    if len(opts) <= 1:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        tuple(opts),
        {"effect_kind": "R8_ALTER_OR_COOL"},
        slot_id="R8",
        profile="A",
        resume_tag="R8_STEP2",
    )


def _r8_trigger_mue(state: GameState) -> None:
    slidables = _slidable_reve_indices(state)
    if not slidables:
        _r8_prompt_step2(state)
        return
    if len(slidables) == 1:
        verb_glisser_reve(state, slidables[0])
        _r8_prompt_step2(state)
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        tuple(idx + 1 for idx in slidables),
        {"effect_kind": "R8_SLIDE_REVE"},
        slot_id="R8",
        profile="A",
        resume_tag="R8_SLIDE",
    )


@register_tile("R8", "A", hooks=(HOOK_3_2_ECAILLE_REVELEE, HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r8_mue_obsidienne_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R8 La Mue d'obsidienne v6.4 : loi passive sur Écaille révélée + résolution défendue (Glisser Rêve + Altérer/Refroidir)."""
    if hook == HOOK_3_2_ECAILLE_REVELEE:
        if state.find_tactique_rank(TILE_R_BASE + 8) is not None:
            _r8_trigger_mue(state)
        return

    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        _r8_trigger_mue(state)
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if tag == "R8_SLIDE":
            verb_glisser_reve(state, int(ch) - 1)
            _r8_prompt_step2(state)
        elif tag == "R8_STEP2" and ch != "PASSER":
            if str(ch[0]) == "ALTERER":
                verb_alterer(state, int(ch[1]), int(ch[2]))
            elif str(ch[0]) == "REFROIDIR":
                verb_refroidir(state, int(ch[1]), int(ch[2]), 1)


# ---------------------------------------------------------------------------
# R9 — La Matinta Pereira (E>O)
# ---------------------------------------------------------------------------


def _r9_siffler_after_remove(state: GameState, rem_siffler: int) -> None:
    slidables = _slidable_reve_indices(state)
    if len(slidables) == 1:
        verb_glisser_reve(state, slidables[0])
        _r9_prompt_second_siffler(state, rem_siffler - 1)
        return
    if len(slidables) > 1:
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(idx + 1 for idx in slidables),
            {"effect_kind": "R9_SIFFLER_SLIDE"},
            slot_id="R9",
            profile="A",
            resume_tag="R9_SLIDE",
            resume_payload=(rem_siffler - 1,),
        )
        return
    _r9_prompt_second_siffler(state, rem_siffler - 1)


def _r9_prompt_second_siffler(state: GameState, rem_siffler: int) -> None:
    if rem_siffler <= 0:
        return
    altered: list[tuple[str, int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if state.has_machine_alteration(r, mt):
                altered.append(("SIFFLER", r, mt))
    if not altered:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        ("PASSER", *altered),
        {"effect_kind": "R9_SIFFLER_SECOND"},
        slot_id="R9",
        profile="A",
        resume_tag="R9_SIFF2",
    )


@register_tile("R9", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r9_matinta_pereira_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R9 La Matinta Pereira v6.4 : vol jusqu'à 2 rangs vers Perchoir + Maudire OU Siffler (1–2 Altérations -> Glisser + Refroidir)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        phase = str(ctx.get("phase", ""))
        if phase == "PRE_CANCEL":
            r9_idx = state.find_tactique_rank(TILE_R_BASE + 9)
            if r9_idx is None:
                return
            p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
            if p_face == 0 or p_kind != PERCHOIR_KIND_RANK or not (0 <= p_idx < TRACK_LEN):
                return
            target_idx = p_idx
            if target_idx == r9_idx:
                return
            step = 1 if target_idx > r9_idx else -1
            free_dsts: list[int] = []
            k = r9_idx + step
            while (k <= target_idx if step > 0 else k >= target_idx) and len(free_dsts) < 2:
                if not is_reve_code(state.get_tactique_at_rank(k)):
                    free_dsts.append(k + 1)
                k += step
            if not free_dsts:
                return
            push_effect_decision(
                state,
                _gov(state, "E"),
                ("PASSER", *free_dsts),
                {"effect_kind": "R9_VOL_BRUME", "r9_case": r9_idx + 1, "perchoir_rank": p_idx + 1},
                slot_id="R9",
                profile="A",
                resume_tag="R9_VOL",
            )
            return

        if phase == "OPEN":
            cur_case = int(ctx["case"])
            p_face, p_kind, p_idx, _ = state.get_oiseau_perchoir_signal()
            p_rank_1_6 = (p_idx + 1) if (p_face != 0 and p_kind == PERCHOIR_KIND_RANK) else 0
            maudire_set: set[tuple[int, int]] = set()
            # 1) Mobiles de ce rang (y compris tout juste Étouffées)
            for s_raw in ctx.get("cancelled_seats", ()):
                card = state.get_player_hand(int(s_raw))[0]
                if 1 <= card <= 12:
                    rm, mtm = (card - 1) // 2, (card - 1) % 2
                    pos, st, _ = state.get_machine_pos_status(rm, mtm)
                    if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(rm, mtm):
                        maudire_set.add((rm, mtm))
            for s in range(state.cfg.n_players):
                card, _, _, lec_m, _ = state.get_player_hand(s)
                if 1 <= card <= 12 and (lec_m == cur_case or (p_rank_1_6 > 0 and lec_m == p_rank_1_6)):
                    rm, mtm = (card - 1) // 2, (card - 1) % 2
                    pos, st, _ = state.get_machine_pos_status(rm, mtm)
                    if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(rm, mtm):
                        maudire_set.add((rm, mtm))
            # 2) Mobiles du rayon du Perchoir
            if p_face != 0 and p_kind == PERCHOIR_KIND_RAY and 0 <= p_idx < state.cfg.n_players:
                for rm, mtm in _alterable_mobiles(state, (p_idx,)):
                    maudire_set.add((rm, mtm))
            # 3) À défaut : mobiles du rayon Entités
            if not maudire_set:
                for rm, mtm in _alterable_mobiles(state, _peuple_rays(state, "E")):
                    maudire_set.add((rm, mtm))

            opts: list[Any] = ["PASSER"]
            for rm, mtm in sorted(maudire_set):
                opts.append(("MAUDIRE", rm, mtm))
            for r in range(state.cfg.n_players):
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                    if state.has_machine_alteration(r, mt):
                        opts.append(("SIFFLER", r, mt))
            if len(opts) <= 1:
                return
            push_effect_decision(
                state,
                _gov(state, "E"),
                tuple(opts),
                {"effect_kind": "R9_MAUDIRE_OU_SIFFLER", "r9_case": cur_case},
                slot_id="R9",
                profile="A",
                resume_tag="R9_OPEN",
            )
            return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        if tag == "R9_VOL":
            r9_idx = state.find_tactique_rank(TILE_R_BASE + 9)
            if r9_idx is not None:
                state.move_reve_to_free_rank(r9_idx, int(ch) - 1)
        elif tag == "R9_OPEN":
            kind, r, mt = str(ch[0]), int(ch[1]), int(ch[2])
            if kind == "MAUDIRE":
                verb_alterer(state, r, mt)
            elif kind == "SIFFLER":
                state.set_machine_alteration(r, mt, False)
                verb_refroidir(state, r, mt, 1)
                _r9_siffler_after_remove(state, 2)
        elif tag == "R9_SLIDE":
            verb_glisser_reve(state, int(ch) - 1)
            rem = int(ctx["payload"][0])
            _r9_prompt_second_siffler(state, rem)
        elif tag == "R9_SIFF2":
            r, mt = int(ch[1]), int(ch[2])
            state.set_machine_alteration(r, mt, False)
            verb_refroidir(state, r, mt, 1)
            _r9_siffler_after_remove(state, 1)


# ---------------------------------------------------------------------------
# R10 — La Ruche vagabonde (E>I)
# ---------------------------------------------------------------------------


def _r10_prompt_branch(state: GameState) -> None:
    opts: list[Any] = ["PASSER"]
    # Branche 1 : Envol de la Ruche (déménager 1 Nid vers toute parcelle forestière sans autre Nid)
    occupied_nids: set[tuple[int, int]] = set()
    active_nids: list[tuple[int, int, int]] = []
    for m_num in range(1, 6):
        pos_info = state.get_nid_position(m_num)
        if pos_info is not None:
            r_n, p_n, _ = pos_info
            occupied_nids.add((r_n, p_n))
            active_nids.append((m_num, r_n, p_n))
    for m_num, r_n, p_n in active_nids:
        for dst_r in range(state.cfg.n_players):
            for dst_p in range(1, state.cfg.p_max + 1):
                if (dst_r, dst_p) == (r_n, p_n):
                    continue
                if state.is_route_forestiere(dst_r, dst_p) or (dst_r, dst_p) in occupied_nids:
                    continue
                opts.append(("ENVOL", m_num, dst_r, dst_p))

    # Branche 2 : Essaim spectral (+1 Insecte réserve sur E, I ou BUG 1..6 + Altérer mobile)
    if state.cfg.has_insectes_peuple:
        for r in _peuple_rays(state, "E", "I"):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p):
                    opts.append(("SPECTRAL_FORET", r, p))
        for c in range(1, TRACK_LEN + 1):
            opts.append(("SPECTRAL_BUG", c))

    if len(opts) <= 1:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        tuple(opts),
        {"effect_kind": "R10_BRANCH"},
        slot_id="R10",
        profile="A",
        resume_tag="R10_BRANCH",
    )


def _r10_prompt_after_envol(state: GameState, dst_r: int, dst_p: int) -> None:
    opts: list[Any] = ["PASSER"]
    for r, mt in _alterable_mobiles(state, (dst_r,)):
        opts.append(("ALTERER", r, mt))
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st, _ = state.get_machine_pos_status(dst_r, mt)
        if st != MACHINE_STATUS_RETIRED and pos == dst_p and state.get_machine_tokens(dst_r, mt)[0] >= 1:
            opts.append(("REFROIDIR", dst_r, mt))
    if len(opts) <= 1:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        tuple(opts),
        {"effect_kind": "R10_ENVOL_BONUS", "dst_r": dst_r, "dst_p": dst_p},
        slot_id="R10",
        profile="A",
        resume_tag="R10_BONUS",
    )


def _r10_prompt_after_spectral(state: GameState) -> None:
    alts = _alterable_mobiles(state)
    if not alts:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        ("PASSER", *(("ALTERER", r, mt) for r, mt in alts)),
        {"effect_kind": "R10_SPECTRAL_ALTER"},
        slot_id="R10",
        profile="A",
        resume_tag="R10_BONUS",
    )


@register_tile("R10", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r10_ruche_vagabonde_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """R10 La Ruche vagabonde v6.4 : Glisser 1 Rêve + Envol d'un Nid (+ Altérer/Refroidir) OU Essaim spectral (+ Altérer)."""
    if hook == HOOK_3_2_OUVERTURE_REVE and ctx.get("phase") == "OPEN":
        slidables = _slidable_reve_indices(state)
        if not slidables:
            _r10_prompt_branch(state)
            return
        if len(slidables) == 1:
            verb_glisser_reve(state, slidables[0])
            _r10_prompt_branch(state)
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(idx + 1 for idx in slidables),
            {"effect_kind": "R10_SLIDE_REVE"},
            slot_id="R10",
            profile="A",
            resume_tag="R10_SLIDE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        if tag == "R10_SLIDE":
            verb_glisser_reve(state, int(ch) - 1)
            _r10_prompt_branch(state)
        elif tag == "R10_BRANCH":
            kind = str(ch[0])
            if kind == "ENVOL":
                m_num, dst_r, dst_p = int(ch[1]), int(ch[2]), int(ch[3])
                if prim_deplacement_nid(state, m_num, dst_r, dst_p):
                    _r10_prompt_after_envol(state, dst_r, dst_p)
            elif kind == "SPECTRAL_FORET":
                prim_creation_entite(
                    state, "INSECTE", ray=int(ch[1]), p=int(ch[2]), light_trigger=False
                )
                _r10_prompt_after_spectral(state)
            elif kind == "SPECTRAL_BUG":
                prim_creation_entite(state, "BUG", p=int(ch[1]), count=1, light_trigger=False)
                _r10_prompt_after_spectral(state)
        elif tag == "R10_BONUS":
            if str(ch[0]) == "ALTERER":
                verb_alterer(state, int(ch[1]), int(ch[2]))
            elif str(ch[0]) == "REFROIDIR":
                verb_refroidir(state, int(ch[1]), int(ch[2]), 1)
