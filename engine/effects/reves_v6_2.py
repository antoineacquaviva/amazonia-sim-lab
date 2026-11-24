"""Catalogue stateless Canon 0 v6.2 — 10 Rêves actifs (R1:A..R10:A).

Zéro état global mutable, zéro accès à `_buf`, zéro `import random`, 100 % stdlib PyPy 3.11.
Zéro dette mémoire (`mem_debt_score == 0`).
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_EFFECT_RESUME,
    HOOK_ENRACINEMENT,
    HOOK_REPOUSSE_FINALE,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_permutation_piste,
    push_effect_decision,
)
from engine.state import (
    DUEL_NONE,
    FURT_RIVE_PIEGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_AUCUN,
    PLUME_KIND_RAY,
    PLUME_NONE,
    SYNERGY_META,
    TILE_R_BASE,
    TRACK_LEN,
    GameState,
    is_reve_code,
    unpack_machine_card,
)

__all__ = ()


def _gov_for_slot(state: GameState, slot_id: str) -> int:
    peuple = SYNERGY_META[slot_id][1]
    seat = state.cfg.seat_of_peuple(peuple)
    return seat if seat is not None else state.coordonnateur


def _current_reve_case(state: GameState, r_num: int, fallback_case: int) -> int:
    rk = state.find_tactique_rank(TILE_R_BASE + r_num)
    return (rk + 1) if rk is not None else fallback_case


def _mobile_unaltered_machines(state: GameState) -> tuple[tuple[int, int], ...]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not state.has_machine_alteration(r, mt):
                out.append((r, mt))
    return tuple(out)


# ---------------------------------------------------------------------------
# R1 (H>E) — Le Seuil des Deux Mondes
# ---------------------------------------------------------------------------


@register_tile("R1", "A", (HOOK_3_2_OUVERTURE_REVE,))
def eff_r1_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R1 (H>E) Le Seuil des Deux Mondes :
    À l'ouverture, chaque Défenseur de ce Rêve peut annuler une machine visant un rang voisin
    sans Rêve plutôt qu'une machine de son rang.
    """
    _ = hook_name
    if ctx.get("phase") != "CANDIDATES":
        return
    r_idx = int(ctx["r_idx"])
    extra_out: list[tuple[int, int, int, int, int]] = ctx["extra_entries"]
    n = state.cfg.n_players

    for adj_idx in (r_idx - 1, r_idx + 1):
        if not (0 <= adj_idx < TRACK_LEN):
            continue
        if is_reve_code(state.get_tactique_at_rank(adj_idx)):
            continue
        adj_case = adj_idx + 1
        for s in range(n):
            if (
                state.was_seat_altered_this_turn(s)
                or state.was_seat_cancelled_by_reve_this_turn(s)
            ):
                continue
            card, d1, d2, lec_m, bound_t = state.get_player_hand(s)
            if not (1 <= card <= 2 * n) or lec_m != adj_case:
                continue
            # Rang < r_idx déjà lié (bound_t == adj_case) ; rang > r_idx pas encore lié (bound_t == 0)
            if (adj_idx < r_idx and bound_t == adj_case) or (adj_idx > r_idx and bound_t == 0):
                extra_out.append((s, card, d1, d2, lec_m))


# ---------------------------------------------------------------------------
# R2 (E>H) — Le Voile de l'Oubli
# ---------------------------------------------------------------------------


@register_tile("R2", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_ENRACINEMENT, HOOK_EFFECT_RESUME))
def eff_r2_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R2 (E>H) Le Voile de l'Oubli :
    Ouverture : Quand ce Rêve annule une machine, altérez-la.
    Enraciné : Lors de son enracinement, altérez jusqu'à 2 machines mobiles.
    """
    if hook_name == HOOK_3_2_OUVERTURE_REVE:
        if ctx.get("phase") == "CANDIDATES":
            return
        for s in ctx.get("cancelled_seats", ()):
            card = state.get_player_hand(int(s))[0]
            if 1 <= card <= 2 * state.cfg.n_players:
                rm, mt = unpack_machine_card(card)
                prim_creation_entite(state, "ALTERATION", ray=rm, m_type=mt, light_trigger=False)
        return

    if hook_name == HOOK_ENRACINEMENT:
        cands = _mobile_unaltered_machines(state)
        if not cands:
            return
        if len(cands) <= 2:
            for rm, mt in cands:
                prim_creation_entite(state, "ALTERATION", ray=rm, m_type=mt, light_trigger=False)
            return
        push_effect_decision(
            state,
            _gov_for_slot(state, "R2"),
            cands,
            {"effect_kind": "R2_ROOT_ALTER", "remaining": 2},
            slot_id="R2",
            profile="A",
            resume_tag="ROOT_ALTER",
            resume_payload=(1,),
        )
        return

    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        (rem_after,) = ctx["payload"]
        prim_creation_entite(
            state, "ALTERATION", ray=int(choice[0]), m_type=int(choice[1]), light_trigger=False
        )
        if int(rem_after) >= 1:
            cands2 = _mobile_unaltered_machines(state)
            if not cands2:
                return
            if len(cands2) == 1:
                prim_creation_entite(
                    state, "ALTERATION", ray=cands2[0][0], m_type=cands2[0][1], light_trigger=False
                )
                return
            push_effect_decision(
                state,
                _gov_for_slot(state, "R2"),
                cands2,
                {"effect_kind": "R2_ROOT_ALTER", "remaining": 1},
                slot_id="R2",
                profile="A",
                resume_tag="ROOT_ALTER",
                resume_payload=(0,),
            )


# ---------------------------------------------------------------------------
# R3 (H>M) — La Danse des Esprits-Fauves
# ---------------------------------------------------------------------------


@register_tile("R3", "A", (HOOK_3_2_OUVERTURE_REVE,))
def eff_r3_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R3 (H>M) La Danse des Esprits-Fauves :
    À l'ouverture, après ses annulations (et un éventuel glissement du Chant),
    1 Défenseur de ce Rêve rejoint la parcelle du jeton Duel.
    """
    _ = hook_name
    if ctx.get("phase") == "CANDIDATES":
        return
    duel_st, dr, dp = state.get_duel_state()
    if duel_st == DUEL_NONE or state.is_route_forestiere(dr, dp):
        return
    cur_case = _current_reve_case(state, 3, int(ctx.get("case", 1)))
    defs = state.list_defenders_on_reve_case(cur_case)
    if not defs:
        return
    src_s, src_d = defs[0]
    prim_deplacement(
        state,
        "DEFENSEUR",
        src_seat=src_s,
        src_def_idx=src_d,
        dst_ray=dr,
        dst_p=dp,
    )


# ---------------------------------------------------------------------------
# R4 (H>R) — Le Sommeil de la Pierre-Serpent
# ---------------------------------------------------------------------------


@register_tile("R4", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def eff_r4_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R4 (H>R) Le Sommeil de la Pierre-Serpent :
    À l'ouverture, 1 Défenseur de ce Rêve peut compléter la Rive Piège d'un rayon
    comptant 2 machines mobilisées (`m(r) == 2`).
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        src_s, src_d = ctx["payload"]
        dst_ray = int(choice)
        if (
            state.is_ray_furtivite_open(dst_ray)
            and state.get_furtivite_nb_def_rive(dst_ray, 1, FURT_RIVE_PIEGE) == 1
        ):
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_seat=int(src_s),
                src_def_idx=int(src_d),
                dst_ray=dst_ray,
                dst_furtivite_rive=FURT_RIVE_PIEGE,
            )
        return

    if ctx.get("phase") == "CANDIDATES":
        return
    cur_case = _current_reve_case(state, 4, int(ctx.get("case", 1)))
    defs = state.list_defenders_on_reve_case(cur_case)
    if not defs:
        return
    valid_rays = tuple(
        r
        for r in range(state.cfg.n_players)
        if state.is_ray_furtivite_open(r)
        and state.count_mobilized_machines_for_ray(r) == 2
        and state.get_furtivite_nb_def_rive(r, 1, FURT_RIVE_PIEGE) == 1
    )
    if not valid_rays:
        return
    src_s, src_d = defs[0]
    push_effect_decision(
        state,
        _gov_for_slot(state, "R4"),
        ("PASSER", *valid_rays),
        {"effect_kind": "R4_COMPLETE_FURT"},
        slot_id="R4",
        profile="A",
        resume_tag="COMPLETE_FURT",
        resume_payload=(src_s, src_d),
    )


# ---------------------------------------------------------------------------
# R5 (H>O) — La Vision des Plumes Claires
# ---------------------------------------------------------------------------


@register_tile("R5", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def eff_r5_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R5 (H>O) La Vision des Plumes Claires :
    À l'ouverture, 1 Défenseur de ce Rêve, ou 2 avec le Tambour, rejoint une parcelle ciblée
    du rayon marqué par la Plume de Vigie.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        cur_case, p_ray, rem_after = ctx["payload"]
        defs_now = state.list_defenders_on_reve_case(int(cur_case))
        if not defs_now:
            return
        src_s, src_d = defs_now[0]
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=src_s,
            src_def_idx=src_d,
            dst_ray=int(choice[0]),
            dst_p=int(choice[1]),
        )
        if int(rem_after) >= 1:
            defs2 = state.list_defenders_on_reve_case(int(cur_case))
            targets2 = tuple(rp for rp in list_targeted_parcels(state) if rp[0] == int(p_ray))
            if defs2 and targets2:
                if len(targets2) == 1:
                    prim_deplacement(
                        state,
                        "DEFENSEUR",
                        src_seat=defs2[0][0],
                        src_def_idx=defs2[0][1],
                        dst_ray=targets2[0][0],
                        dst_p=targets2[0][1],
                    )
                    return
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "R5"),
                    targets2,
                    {"effect_kind": "R5_DEPLOY_PLUME", "ray": int(p_ray), "step": 2},
                    slot_id="R5",
                    profile="A",
                    resume_tag="DEPLOY",
                    resume_payload=(int(cur_case), int(p_ray), 0),
                )
        return

    if ctx.get("phase") == "CANDIDATES":
        return
    face_p, kind_p, idx_p, _ = state.get_oiseau_plume()
    if face_p == PLUME_NONE or kind_p != PLUME_KIND_RAY or idx_p >= state.cfg.n_players:
        return
    targets = tuple(rp for rp in list_targeted_parcels(state) if rp[0] == idx_p)
    if not targets:
        return
    cur_case = _current_reve_case(state, 5, int(ctx.get("case", 1)))
    defs = state.list_defenders_on_reve_case(cur_case)
    if not defs:
        return
    max_moves = 2 if state.is_tambour_on_reve_case(cur_case) else 1
    n_moves = min(max_moves, len(defs))

    if len(targets) == 1:
        for i in range(n_moves):
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_seat=defs[i][0],
                src_def_idx=defs[i][1],
                dst_ray=targets[0][0],
                dst_p=targets[0][1],
            )
        return

    push_effect_decision(
        state,
        _gov_for_slot(state, "R5"),
        targets,
        {"effect_kind": "R5_DEPLOY_PLUME", "ray": idx_p, "step": 1},
        slot_id="R5",
        profile="A",
        resume_tag="DEPLOY",
        resume_payload=(cur_case, idx_p, n_moves - 1),
    )


# ---------------------------------------------------------------------------
# R6 (H>I) — Le Miel des Ancêtres
# ---------------------------------------------------------------------------


@register_tile("R6", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_REPOUSSE_FINALE, HOOK_EFFECT_RESUME))
def eff_r6_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R6 (H>I) Le Miel des Ancêtres :
    Ouverture : 1 Défenseur de ce Rêve rejoint la parcelle d'un Nid pour activer sa production.
    Enraciné : Au décompte final, retournez aussi 1 Souche d'une parcelle voisine en Arbre debout
               (Pont routier sur son rayon).
    """
    if hook_name == HOOK_REPOUSSE_FINALE:
        if ctx.get("phase") != "ROOTED_TILE":
            return
        r_root, p_root = int(ctx["ray"]), int(ctx["p"])
        if state.is_route_forestiere(r_root, p_root):
            return
        nbr_cands: list[tuple[int, int]] = []
        for p_nbr in (
            state.next_non_razed_towards_border(r_root, p_root),
            state.next_non_razed_towards_heart(r_root, p_root),
        ):
            if p_nbr is None:
                continue
            souches = state.get_parcel_souches(r_root, p_nbr)
            arbres = state.get_parcel_arbres(r_root, p_nbr)
            cap = state.cfg.dotation_arbres[p_nbr - 1]
            if souches >= 1 and arbres < cap:
                nbr_cands.append((souches, p_nbr))
        if nbr_cands:
            best_p = max(nbr_cands, key=lambda item: (item[0], -item[1]))[1]
            prim_creation_entite(state, "ARBRE", ray=r_root, p=best_p, count=1, light_trigger=False)
        return

    if hook_name == HOOK_EFFECT_RESUME:
        src_s, src_d = ctx["payload"]
        choice = ctx["choice"]
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=int(src_s),
            src_def_idx=int(src_d),
            dst_ray=int(choice[0]),
            dst_p=int(choice[1]),
        )
        return

    if ctx.get("phase") == "CANDIDATES" or not state.cfg.has_insectes_peuple:
        return
    cur_case = _current_reve_case(state, 6, int(ctx.get("case", 1)))
    defs = state.list_defenders_on_reve_case(cur_case)
    if not defs:
        return
    nid_parcels: list[tuple[int, int]] = []
    for m_num in range(1, 6):
        pos = state.get_nid_position(m_num)
        if pos is not None and not state.is_route_forestiere(pos[0], pos[1]):
            nid_parcels.append((pos[0], pos[1]))
    if not nid_parcels:
        return
    src_s, src_d = defs[0]
    if len(nid_parcels) == 1:
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=src_s,
            src_def_idx=src_d,
            dst_ray=nid_parcels[0][0],
            dst_p=nid_parcels[0][1],
        )
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "R6"),
        tuple(nid_parcels),
        {"effect_kind": "R6_JOIN_NID"},
        slot_id="R6",
        profile="A",
        resume_tag="JOIN_NID",
        resume_payload=(src_s, src_d),
    )


# ---------------------------------------------------------------------------
# R7 (E>M) — L'Ombre du Maître des Bois
# ---------------------------------------------------------------------------


@register_tile("R7", "A", (HOOK_3_2_OUVERTURE_REVE,))
def eff_r7_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R7 (E>M) L'Ombre du Maître des Bois :
    À l'ouverture, si ce Rêve défendu n'annule aucune machine, faites-le glisser d'1 rang à gauche.
    """
    _ = hook_name
    if ctx.get("phase") == "CANDIDATES":
        return
    if int(ctx.get("n_cancel", 0)) != 0:
        return
    rk = state.find_tactique_rank(TILE_R_BASE + 7)
    if rk is not None:
        prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=rk)


# ---------------------------------------------------------------------------
# R8 (E>R) — Le Mirage du Fleuve-Miroir
# ---------------------------------------------------------------------------


def _r8_slide_options(state: GameState) -> tuple[tuple[int, int], ...]:
    opts: list[tuple[int, int]] = []
    for rk in range(TRACK_LEN):
        code = state.get_tactique_at_rank(rk)
        if not is_reve_code(code):
            continue
        dest1 = state.get_reve_advance_dest_rank(rk)
        if dest1 is None:
            continue
        r_num = code - TILE_R_BASE
        opts.append((r_num, 1))
        # Un 2e glissement est possible si au moins 2 cases non-Rêve existent à gauche de `rk`
        non_reves_left = sum(
            1 for j in range(rk) if not is_reve_code(state.get_tactique_at_rank(j))
        )
        if non_reves_left >= 2:
            opts.append((r_num, 2))
    return tuple(opts)


@register_tile("R8", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def eff_r8_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R8 (E>R) Le Mirage du Fleuve-Miroir :
    À l'ouverture, ce Rêve défendu peut retirer définitivement 1 Souche sans vider sa parcelle
    (`arbres + souches >= 2` avant retrait) pour glisser un Rêve d'1 ou 2 rangs à gauche.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        if tag == "PICK_SOUCHE":
            sr, sp = int(choice[0]), int(choice[1])
            slide_opts = _r8_slide_options(state)
            if not slide_opts:
                return
            if len(slide_opts) == 1:
                r_num_t, steps = slide_opts[0]
                arbres = state.get_parcel_arbres(sr, sp)
                souches = state.get_parcel_souches(sr, sp)
                if souches >= 1 and arbres + souches >= 2:
                    state.set_parcel_arbres_souches(sr, sp, arbres, souches - 1)
                    code = TILE_R_BASE + r_num_t
                    for _ in range(steps):
                        rk_now = state.find_tactique_rank(code)
                        if rk_now is None or not prim_permutation_piste(
                            state, "ADVANCE_REVE_LEFT", rank_a=rk_now
                        ):
                            break
                return
            push_effect_decision(
                state,
                _gov_for_slot(state, "R8"),
                slide_opts,
                {"effect_kind": "R8_PICK_REVE_STEPS", "src_parcel": (sr, sp)},
                slot_id="R8",
                profile="A",
                resume_tag="PICK_SLIDE",
                resume_payload=(sr, sp),
            )
        elif tag == "PICK_SLIDE":
            sr, sp = ctx["payload"]
            r_num_t, steps = int(choice[0]), int(choice[1])
            arbres = state.get_parcel_arbres(int(sr), int(sp))
            souches = state.get_parcel_souches(int(sr), int(sp))
            if souches >= 1 and arbres + souches >= 2:
                state.set_parcel_arbres_souches(int(sr), int(sp), arbres, souches - 1)
                code = TILE_R_BASE + r_num_t
                for _ in range(steps):
                    rk_now = state.find_tactique_rank(code)
                    if rk_now is None or not prim_permutation_piste(
                        state, "ADVANCE_REVE_LEFT", rank_a=rk_now
                    ):
                        break
        return

    if ctx.get("phase") == "CANDIDATES":
        return
    if not _r8_slide_options(state):
        return
    souche_parcels = tuple(
        (r, p)
        for r in range(state.cfg.n_players)
        for p in range(1, state.cfg.p_max + 1)
        if state.get_parcel_souches(r, p) >= 1
        and (state.get_parcel_arbres(r, p) + state.get_parcel_souches(r, p)) >= 2
    )
    if not souche_parcels:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "R8"),
        ("PASSER", *souche_parcels),
        {"effect_kind": "R8_PICK_SOUCHE"},
        slot_id="R8",
        profile="A",
        resume_tag="PICK_SOUCHE",
    )


# ---------------------------------------------------------------------------
# R9 (E>O) — L'Écho des Voix Célestes
# ---------------------------------------------------------------------------


@register_tile("R9", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def eff_r9_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R9 (E>O) L'Écho des Voix Célestes :
    À l'ouverture, si le Perchoir de Vigie cache un jeton Machine, révélez-le, altérez sa machine
    et posez 1 Piège sur son rayon.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        r_c, p_c = int(choice[0]), int(choice[1])
        if not state.is_route_forestiere(r_c, p_c) and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN:
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=False)
        return

    if ctx.get("phase") == "CANDIDATES":
        return
    card_p = state.oiseau_perchoir_card
    if not (1 <= card_p <= 2 * state.cfg.n_players):
        return
    state.reveal_oiseau_perchoir()
    r_m, mt_m = unpack_machine_card(card_p)
    prim_creation_entite(state, "ALTERATION", ray=r_m, m_type=mt_m, light_trigger=False)

    valid_p = tuple(
        (r_m, p)
        for p in range(1, state.cfg.p_max + 1)
        if not state.is_route_forestiere(r_m, p) and state.get_parcel_piege(r_m, p) == PIEGE_AUCUN
    )
    if not valid_p:
        return
    if len(valid_p) == 1:
        prim_creation_entite(
            state, "PIEGE", ray=valid_p[0][0], p=valid_p[0][1], light_trigger=False
        )
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "R9"),
        valid_p,
        {"effect_kind": "R9_PLACE_PIEGE", "ray": r_m},
        slot_id="R9",
        profile="A",
        resume_tag="PLACE_PIEGE",
    )


# ---------------------------------------------------------------------------
# R10 (E>I) — La Nuée des Songes
# ---------------------------------------------------------------------------


def _r10_place_one_insect_step(state: GameState, cur_case: int, remaining: int) -> None:
    if remaining <= 0 or not state.cfg.has_insectes_peuple:
        return
    opts: list[tuple[Any, ...]] = [("RANG", cur_case)]
    for m_num in range(1, 6):
        pos = state.get_nid_position(m_num)
        if pos is not None and not state.is_route_forestiere(pos[0], pos[1]):
            opts.append(("NID", m_num, pos[0], pos[1]))
    if len(opts) == 1:
        prim_creation_entite(state, "BUG", p=cur_case, count=remaining, light_trigger=False)
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "R10"),
        tuple(opts),
        {"effect_kind": "R10_PLACE_INSECT", "remaining": remaining},
        slot_id="R10",
        profile="A",
        resume_tag="PLACE_INS",
        resume_payload=(cur_case, remaining - 1),
    )


@register_tile("R10", "A", (HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def eff_r10_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """R10 (E>I) La Nuée des Songes :
    Quand ce Rêve annule une machine, altérez-la et posez 1 Insecte sur un Nid ou sur ce rang.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        cur_case, rem_after = ctx["payload"]
        if choice[0] == "RANG":
            prim_creation_entite(state, "BUG", p=int(choice[1]), count=1, light_trigger=False)
        elif choice[0] == "NID":
            prim_creation_entite(
                state, "INSECTE", ray=int(choice[2]), p=int(choice[3]), count=1, light_trigger=False
            )
        if int(rem_after) >= 1:
            _r10_place_one_insect_step(state, int(cur_case), int(rem_after))
        return

    if ctx.get("phase") == "CANDIDATES":
        return
    cancelled = tuple(ctx.get("cancelled_seats", ()))
    if not cancelled:
        return
    for s in cancelled:
        card = state.get_player_hand(int(s))[0]
        if 1 <= card <= 2 * state.cfg.n_players:
            rm, mt = unpack_machine_card(card)
            prim_creation_entite(state, "ALTERATION", ray=rm, m_type=mt, light_trigger=False)
    cur_case = _current_reve_case(state, 10, int(ctx.get("case", 1)))
    _r10_place_one_insect_step(state, cur_case, len(cancelled))
