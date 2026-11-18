"""Lot 07 — Implémentation stateless des 10 profils de Rêves (R5:B..R7:C).

Règles strictes :
- 100 % stdlib PyPy 3.11 (zéro dépendance externe, zéro _buf, zéro random, zéro global mutable).
- Utilise exclusivement les constantes, accesseurs et primitives de contracts/core_state_api.md.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_1_3_LECTURE_DE,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_4_3_MIGRATION_DESTS,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_5_SEUIL_PARADE,
    HOOK_EFFECT_RESUME,
    HOOK_REPOUSSE_FINALE,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_SIEGE,
    NUM_NIDS,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    TACTIQUES_SPEC,
    GameState,
)

LOT_07_PROFILES: tuple[tuple[str, str], ...] = (
    ("R5", "B"),
    ("R5", "C"),
    ("R5", "D"),
    ("R6", "A"),
    ("R6", "B"),
    ("R6", "C"),
    ("R6", "D"),
    ("R7", "A"),
    ("R7", "B"),
    ("R7", "C"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _rays_for_peuples(state: GameState, *peuples: str) -> tuple[int, ...]:
    rays: list[int] = []
    for p_code in peuples:
        seat = state.cfg.seat_of_peuple(p_code)
        if seat is not None and seat not in rays:
            rays.append(seat)
    return tuple(rays)


def _targeted_parcels_after_revelation(state: GameState) -> list[tuple[int, int]]:
    targeted: list[tuple[int, int]] = []
    n = state.cfg.n_players

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if (
                st == MACHINE_STATUS_SIEGE
                and pos > 0
                and not state.is_route_forestiere(r, pos)
                and (r, pos) not in targeted
            ):
                targeted.append((r, pos))

    for s in range(n):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and bound_t in TACTIQUES_SPEC:
            rm, mt = (card - 1) // 2, (card - 1) % 2
            pos, st, _ = state.get_machine_pos_status(rm, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0:
                spec = TACTIQUES_SPEC[bound_t]
                for c_kind in spec.cibles:
                    if c_kind == "SUR_PLACE" and not state.is_route_forestiere(rm, pos):
                        if (rm, pos) not in targeted:
                            targeted.append((rm, pos))
                    elif c_kind == "DEVANT":
                        p_dev = state.next_non_razed_towards_heart(rm, pos)
                        if p_dev is not None and (rm, p_dev) not in targeted:
                            targeted.append((rm, p_dev))
    return targeted


# ---------------------------------------------------------------------------
# 1. R5:B — La Vision des Plumes Claires (Humains) : LOI 1.3 | max(D1, D2)
# ---------------------------------------------------------------------------


@register_tile("R5", "B", hooks=(HOOK_1_3_LECTURE_DE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME))
def r5_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Loi 1.3 : Le peuple d'origine H peut retenir M = max(D1, D2) derrière son paravent."""
    prim_mod_loi_du_coeur(state, "LOI_DE_M_CHOIX_MIN_MAX", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return False

    if hook == HOOK_1_3_LECTURE_DE:
        seat = int(ctx["seat"])
        h_seat = state.cfg.seat_of_peuple("H")
        if h_seat is None or seat != h_seat:
            return None
        card, d1, d2, _, _ = state.get_player_hand(seat)
        if not (1 <= card <= 12) or d1 == d2:
            return None
        push_effect_decision(
            state,
            seat,
            ("PASSER", "RETENIR_MAX"),
            {"effect_kind": "CHOIX_DE_M_1_3", "min_m": min(d1, d2), "max_m": max(d1, d2)},
            slot_id="R5",
            profile="B",
            resume_tag="CHOIX_M",
            resume_payload=(seat,),
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        seat = int(ctx["payload"][0])
        if ctx["choice"] == "RETENIR_MAX":
            card, d1, d2, _, bound_t = state.get_player_hand(seat)
            if 1 <= card <= 12 and d1 > 0 and d2 > 0:
                state.set_player_hand(seat, card, d1, d2, max(d1, d2), bound_t)
    return None


# ---------------------------------------------------------------------------
# 2. R5:C — Le Rêve du nid vide (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R5", "C", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r5_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez poser 1 Piège sur une parcelle ciblée H/O vide (0 Déf, 0 Ins, 0 Piège)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        ho_rays = _rays_for_peuples(state, "H", "O")
        if not ho_rays:
            return
        targeted = _targeted_parcels_after_revelation(state)
        cands = [
            (r, p)
            for r, p in targeted
            if r in ho_rays
            and not state.is_route_forestiere(r, p)
            and state.get_parcel_defenseurs(r, p) == 0
            and state.get_parcel_insectes(r, p) == 0
            and state.get_parcel_piege(r, p) == PIEGE_AUCUN
        ]
        if not cands:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            ("PASSER", *cands),
            {"effect_kind": "PIEGE_CIBLE_VIDE_HO"},
            slot_id="R5",
            profile="C",
            resume_tag="PIEGE_VIDE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_c, p_c = int(choice[0]), int(choice[1])
        if (
            not state.is_route_forestiere(r_c, p_c)
            and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN
        ):
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=True)


# ---------------------------------------------------------------------------
# 3. R5:D — Le rêve du veilleur (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R5", "D", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r5_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez créer 1 Insecte sur une parcelle piégée des Humains ou des Oiseaux (allume 6)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        ho_rays = _rays_for_peuples(state, "H", "O")
        if not ho_rays:
            return
        cands: list[tuple[int, int]] = []
        for r in ho_rays:
            for p in range(1, state.cfg.p_max + 1):
                if (
                    not state.is_route_forestiere(r, p)
                    and state.get_parcel_piege(r, p) == PIEGE_ACTIF
                ):
                    cands.append((r, p))
        if not cands:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            ("PASSER", *cands),
            {"effect_kind": "INSECTE_SUR_PIEGE_HO"},
            slot_id="R5",
            profile="D",
            resume_tag="POSE_INS",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_c, p_c = int(choice[0]), int(choice[1])
        if not state.is_route_forestiere(r_c, p_c):
            prim_creation_entite(state, "INSECTE", ray=r_c, p=p_c, count=1, light_trigger=True)


# ---------------------------------------------------------------------------
# 4. R6:A — Le Miel des Ancêtres (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R6", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r6_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Insecte sur une parcelle non rasée d'un rayon H ou I (allume la case 6)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        hi_rays = _rays_for_peuples(state, "H", "I")
        if not hi_rays:
            return
        cands: list[tuple[int, int]] = []
        for r in hi_rays:
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p):
                    cands.append((r, p))
        if not cands:
            return
        if len(cands) == 1:
            prim_creation_entite(
                state, "INSECTE", ray=cands[0][0], p=cands[0][1], count=1, light_trigger=True
            )
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(cands),
            {"effect_kind": "POSE_INSECTE_HI"},
            slot_id="R6",
            profile="A",
            resume_tag="POSE_INS",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        r_c, p_c = int(ctx["choice"][0]), int(ctx["choice"][1])
        if not state.is_route_forestiere(r_c, p_c):
            prim_creation_entite(state, "INSECTE", ray=r_c, p=p_c, count=1, light_trigger=True)


# ---------------------------------------------------------------------------
# 5. R6:B — Le Miel des Ancêtres (Humains) : SIMPLE_CONTINU | 3.2 (ACTIVER_NID)
# ---------------------------------------------------------------------------


def _activate_nid_insects_only(state: GameState, m_num: int) -> None:
    pos_info = state.get_nid_position(m_num)
    if pos_info is None:
        return
    r, p, _ = pos_info
    if state.is_route_forestiere(r, p):
        return
    cur_ins = state.get_parcel_insectes(r, p)
    created = 1 if cur_ins <= 1 else 2
    prim_creation_entite(state, "INSECTE", ray=r, p=p, count=created, light_trigger=True)


@register_tile("R6", "B", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r6_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Déclenche la création d'Insectes d'1 Nid en jeu (+1/+2, allume 6, sans activer 4.2)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        active_nids = [
            m_num for m_num in range(1, NUM_NIDS + 1) if state.get_nid_position(m_num) is not None
        ]
        if not active_nids:
            return
        if len(active_nids) == 1:
            _activate_nid_insects_only(state, active_nids[0])
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(active_nids),
            {"effect_kind": "ACTIVER_NID_INSECTES_3_2"},
            slot_id="R6",
            profile="B",
            resume_tag="ACTIVER_NID",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _activate_nid_insects_only(state, int(ctx["choice"]))


# ---------------------------------------------------------------------------
# 6. R6:C — La Terra Preta (Humains) : LOI REPOUSSE FINALE
# ---------------------------------------------------------------------------


@register_tile("R6", "C", hooks=(HOOK_REPOUSSE_FINALE, HOOK_5_LAW_QUERY))
def r6_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi Repousse finale : sur H ou I, retourne jusqu'à 2 Souches en Arbres (plafonné)."""
    prim_mod_loi_du_coeur(state, "LOI_REPOUSSE_DEUX_SOUCHES", active=True)
    hi_rays = _rays_for_peuples(state, "H", "I")
    if hook == HOOK_5_LAW_QUERY:
        if "ray" in ctx:
            return int(ctx["ray"]) in hi_rays
        return bool(hi_rays)

    ray = int(ctx["ray"])
    if ray in hi_rays:
        ctx["max_repousse"] = max(int(ctx["max_repousse"]), 2)
        return True
    return False


# ---------------------------------------------------------------------------
# 7. R6:D — Les chemins du veilleur (Humains) : LOI 4.3
# ---------------------------------------------------------------------------


@register_tile("R6", "D", hooks=(HOOK_4_3_MIGRATION_DESTS, HOOK_5_LAW_QUERY))
def r6_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 4.3 : un Insecte quittant un Nid sur H ou I peut rejoindre toute parcelle piégée du rayon."""
    prim_mod_loi_du_coeur(state, "LOI_NIDS_DESSERVENT_PIEGES", active=True)
    hi_rays = _rays_for_peuples(state, "H", "I")
    if hook == HOOK_5_LAW_QUERY:
        return bool(hi_rays)

    if hook == HOOK_4_3_MIGRATION_DESTS:
        src = ctx["src"]
        if src[0] != "FORET":
            return False
        r, src_p = int(src[1]), int(src[2])
        if r not in hi_rays:
            return False
        if state.get_parcel_nid(r, src_p)[0] == 0:
            return False
        opts: list[tuple[Any, ...]] = ctx["opts"]
        added = False
        for dst_p in range(1, state.cfg.p_max + 1):
            if (
                dst_p != src_p
                and not state.is_route_forestiere(r, dst_p)
                and state.get_parcel_piege(r, dst_p) == PIEGE_ACTIF
            ):
                cand = ("FORET", r, dst_p)
                if cand not in opts:
                    opts.append(cand)
                    added = True
        return added
    return False


# ---------------------------------------------------------------------------
# 8. R7:A — L’Ombre du Maître des Bois (Entités) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


def _reculable_em_machines(state: GameState) -> list[tuple[int, int]]:
    em_rays = _rays_for_peuples(state, "E", "M")
    out: list[tuple[int, int]] = []
    for r in em_rays:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if (
                st == MACHINE_STATUS_NORMAL
                and pos > 0
                and state.next_non_razed_towards_border(r, pos) is not None
            ):
                out.append((r, mt))
    return out


def _apply_recul_1(state: GameState, r: int, mt: int) -> None:
    pos, st, _ = state.get_machine_pos_status(r, mt)
    if st != MACHINE_STATUS_NORMAL or pos <= 0:
        return
    dst_p = state.next_non_razed_towards_border(r, pos)
    if dst_p is not None:
        prim_deplacement(state, "MACHINE", src_ray=r, m_type=mt, dst_ray=r, dst_p=dst_p)


@register_tile("R7", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r7_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Recule d'1 parcelle non rasée vers la bordure une machine hors Siège sur E ou M."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        cands = _reculable_em_machines(state)
        if not cands:
            return
        if len(cands) == 1:
            _apply_recul_1(state, cands[0][0], cands[0][1])
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(cands),
            {"effect_kind": "MACHINE_RECUL_EM"},
            slot_id="R7",
            profile="A",
            resume_tag="RECUL_EM",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rm, mt = int(ctx["choice"][0]), int(ctx["choice"][1])
        _apply_recul_1(state, rm, mt)


# ---------------------------------------------------------------------------
# 9. R7:B — L’Ombre du Maître des Bois (Entités) : LOI 5 (Endiguement Siège)
# ---------------------------------------------------------------------------


def _endiguement_rays(state: GameState) -> tuple[int, ...]:
    n = state.cfg.n_players
    rays: list[int] = []
    for base_r in _rays_for_peuples(state, "E", "M"):
        for r in (base_r, (base_r - 1) % n, (base_r + 1) % n):
            if r not in rays:
                rays.append(r)
    return tuple(rays)


@register_tile(
    "R7",
    "B",
    hooks=(HOOK_5_SEUIL_PARADE, HOOK_5_FIN_ATTAQUE_MACHINE, HOOK_5_LAW_QUERY),
)
def r7_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 : machines en Siège sur E, M et leurs voisins : 0 gain rouge et -1 Seuil."""
    prim_mod_loi_du_coeur(state, "LOI_ENDIGUEMENT_SIEGE_T4", active=True)
    rays = _endiguement_rays(state)
    if hook == HOOK_5_LAW_QUERY:
        if "ray" in ctx:
            return int(ctx["ray"]) in rays
        return bool(rays)

    if not bool(ctx.get("is_siege")):
        return False
    if int(ctx["ray"]) not in rays:
        return False

    if hook == HOOK_5_SEUIL_PARADE:
        ctx["delta_seuil"] = int(ctx["delta_seuil"]) - 1
        return True
    if hook == HOOK_5_FIN_ATTAQUE_MACHINE:
        ctx["allow_red_gain"] = False
        return True
    return False


# ---------------------------------------------------------------------------
# 10. R7:C — Le bras mort du fleuve (Entités) : LOI 4.3
# ---------------------------------------------------------------------------


@register_tile("R7", "C", hooks=(HOOK_4_3_MIGRATION_DESTS, HOOK_5_LAW_QUERY))
def r7_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 4.3 : un Insecte peut traverser directement entre E et M à la même profondeur."""
    prim_mod_loi_du_coeur(state, "LOI_PASSAGE_DIRECT_INSECTES", active=True)
    e_seat = state.cfg.seat_of_peuple("E")
    m_seat = state.cfg.seat_of_peuple("M")
    if hook == HOOK_5_LAW_QUERY:
        return e_seat is not None and m_seat is not None

    if hook == HOOK_4_3_MIGRATION_DESTS:
        if e_seat is None or m_seat is None:
            return False
        src = ctx["src"]
        if src[0] != "FORET":
            return False
        r, depth = int(src[1]), int(src[2])
        if r == e_seat:
            dst_r = m_seat
        elif r == m_seat:
            dst_r = e_seat
        else:
            return False
        if state.is_route_forestiere(dst_r, depth):
            return False
        opts: list[tuple[Any, ...]] = ctx["opts"]
        cand = ("FORET", dst_r, depth)
        if cand not in opts:
            opts.append(cand)
            return True
    return False
