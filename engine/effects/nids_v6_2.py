"""Catalogue stateless Canon 0 v6.2 — 5 Nids actifs (M1:A..M5:A).

Zéro état global mutable, zéro accès à `_buf`, zéro `import random`, 100 % stdlib PyPy 3.11.
Zéro dette mémoire (`mem_debt_score == 0`). Seuls M2 et M3 sont des Lois passives (2/30).
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_3_MIGRATION_DESTS,
    HOOK_5_LAW_QUERY,
    HOOK_5_PARADE_CLASSIQUE,
    HOOK_EFFECT_RESUME,
    HOOK_REPOUSSE_FINALE,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_puissance,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    PLUME_KIND_RAY,
    PLUME_NONE,
    SYNERGY_META,
    GameState,
)

__all__ = ()


def _gov_for_slot(state: GameState, slot_id: str) -> int:
    peuple = SYNERGY_META[slot_id][1]
    seat = state.cfg.seat_of_peuple(peuple)
    return seat if seat is not None else state.coordonnateur


# ---------------------------------------------------------------------------
# M1 (I>M) — La Fourmilière Coupe-Feuilles
# ---------------------------------------------------------------------------


@register_tile("M1", "A", (HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def eff_m1_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """M1 (I>M) La Fourmilière Coupe-Feuilles :
    Après production, 1 Insecte de ce Nid peut monter sur une machine de son rayon
    et défendre chaque parcelle qu'elle frappe (descente sur place au ménage 6.2).
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_nid, p_nid = ctx["payload"]
        if state.get_parcel_insectes(int(r_nid), int(p_nid)) >= 1:
            prim_deplacement(
                state,
                "INSECTE",
                src_ray=int(r_nid),
                src_p=int(p_nid),
                dst_ray=int(r_nid),
                dst_machine_type=int(choice),
                count=1,
            )
        return

    if not state.cfg.has_insectes_peuple or int(ctx.get("m_num", 0)) != 1:
        return
    r_nid, p_nid = int(ctx["ray"]), int(ctx["p"])
    if state.get_parcel_insectes(r_nid, p_nid) < 1:
        return
    mts = tuple(
        mt
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        if state.get_machine_pos_status(r_nid, mt)[1] != MACHINE_STATUS_RETIRED
        and state.get_machine_pos_status(r_nid, mt)[0] > 0
    )
    if not mts:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "M1"),
        ("PASSER", *mts),
        {"effect_kind": "M1_EMBARK_INSECT", "ray": r_nid, "p": p_nid},
        slot_id="M1",
        profile="A",
        resume_tag="EMBARK",
        resume_payload=(r_nid, p_nid),
    )


# ---------------------------------------------------------------------------
# M2 (I>R) — La Termitière à Glu (LOI PASSIVE)
# ---------------------------------------------------------------------------


@register_tile("M2", "A", (HOOK_5_LAW_QUERY, HOOK_5_PARADE_CLASSIQUE))
def eff_m2_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> bool | None:
    """M2 (I>R) La Termitière à Glu (Loi passive tant que construit en forêt) :
    En Parade : Pour chaque Insecte défaussé en Parade sur la parcelle de ce Nid,
    ajoutez 1 jeton Sabotage au sac.
    """
    pos = state.get_nid_position(2)
    if pos is None:
        return False if hook_name == HOOK_5_LAW_QUERY else None
    same_parcel = pos[0] == int(ctx["ray"]) and pos[1] == int(ctx["target_p"])
    if hook_name == HOOK_5_LAW_QUERY:
        return same_parcel
    if same_parcel:
        ins_disc = int(ctx.get("ins_to_discard", 0))
        if ins_disc >= 1:
            prim_creation_entite(state, "SABOTAGE", count=ins_disc, light_trigger=False)
    return None


# ---------------------------------------------------------------------------
# M3 (I>O) — La Branche des Guêpes Cazadores (LOI PASSIVE)
# ---------------------------------------------------------------------------


@register_tile("M3", "A", (HOOK_4_3_MIGRATION_DESTS,))
def eff_m3_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """M3 (I>O) La Branche des Guêpes Cazadores (Loi passive tant que construit en forêt) :
    En Migration : Les Insectes de ce Nid peuvent migrer latéralement vers la parcelle
    de même profondeur du rayon marqué par la Plume de Vigie (hors Route Forestière).
    """
    _ = hook_name
    if ctx.get("phase") == "APPLIED":
        return
    pos = state.get_nid_position(3)
    if pos is None:
        return
    r_m3, p_m3, _ = pos
    if ctx.get("src") != ("FORET", r_m3, p_m3):
        return
    face_p, kind_p, idx_p, _ = state.get_oiseau_plume()
    if (
        face_p != PLUME_NONE
        and kind_p == PLUME_KIND_RAY
        and 0 <= idx_p < state.cfg.n_players
        and idx_p != r_m3
        and not state.is_route_forestiere(idx_p, p_m3)
    ):
        dest = ("FORET", idx_p, p_m3)
        opts: list[Any] = ctx["opts"]
        if dest not in opts:
            opts.append(dest)


# ---------------------------------------------------------------------------
# M4 (I>H) — La Ruche des Mélipones
# ---------------------------------------------------------------------------


@register_tile("M4", "A", (HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def eff_m4_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """M4 (I>H) La Ruche des Mélipones :
    Après production, envoyez 1 Insecte de ce Nid rejoindre le Tambour en forêt
    ou défaussez-le pour retourner 1 jeton rouge en bleu sur n'importe quelle machine.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_nid, p_nid = ctx["payload"]
        cur = state.get_parcel_insectes(int(r_nid), int(p_nid))
        if cur < 1:
            return
        if choice[0] == "TAMBOUR":
            prim_deplacement(
                state,
                "INSECTE",
                src_ray=int(r_nid),
                src_p=int(p_nid),
                dst_ray=int(choice[1]),
                dst_p=int(choice[2]),
                count=1,
            )
        elif choice[0] == "SURCHAUFFE":
            state.set_parcel_insectes(int(r_nid), int(p_nid), cur - 1)
            prim_mod_puissance(state, int(choice[1]), int(choice[2]), flip_rouge_to_bleu=1)
        return

    if not state.cfg.has_insectes_peuple or int(ctx.get("m_num", 0)) != 4:
        return
    r_nid, p_nid = int(ctx["ray"]), int(ctx["p"])
    if state.get_parcel_insectes(r_nid, p_nid) < 1:
        return

    opts: list[Any] = ["PASSER"]
    t_loc = state.get_humain_tambour_parcel()
    if (
        t_loc is not None
        and t_loc != (r_nid, p_nid)
        and not state.is_route_forestiere(t_loc[0], t_loc[1])
    ):
        opts.append(("TAMBOUR", t_loc[0], t_loc[1]))
    for mr in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(mr, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            rouges, bleus = state.get_machine_tokens(mr, mt)
            if rouges >= 1 and bleus < 15:
                opts.append(("SURCHAUFFE", mr, mt))
    if len(opts) <= 1:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "M4"),
        tuple(opts),
        {"effect_kind": "M4_AFTER_PROD", "ray": r_nid, "p": p_nid},
        slot_id="M4",
        profile="A",
        resume_tag="M4_ACT",
        resume_payload=(r_nid, p_nid),
    )


# ---------------------------------------------------------------------------
# M5 (I>E) — Le Jardin du Diable
# ---------------------------------------------------------------------------


@register_tile("M5", "A", (HOOK_4_2_NID_APRES_PROD, HOOK_REPOUSSE_FINALE, HOOK_EFFECT_RESUME))
def eff_m5_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """M5 (I>E) Le Jardin du Diable :
    Après production : Déplacez 1 Insecte de ce Nid vers une parcelle à Souche de son rayon
                       ou du rayon des Entités.
    Enraciné : Au décompte final, chaque Insecte présent sur sa parcelle y retourne
               1 Souche survivante supplémentaire en Arbre debout.
    """
    if hook_name == HOOK_REPOUSSE_FINALE:
        if ctx.get("phase") != "ROOTED_TILE":
            return
        r_root, p_root = int(ctx["ray"]), int(ctx["p"])
        if state.is_route_forestiere(r_root, p_root):
            return
        ins = state.get_parcel_insectes(r_root, p_root)
        if ins > 0:
            prim_creation_entite(
                state, "ARBRE", ray=r_root, p=p_root, count=ins, light_trigger=False
            )
        return

    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_nid, p_nid = ctx["payload"]
        if state.get_parcel_insectes(int(r_nid), int(p_nid)) >= 1:
            prim_deplacement(
                state,
                "INSECTE",
                src_ray=int(r_nid),
                src_p=int(p_nid),
                dst_ray=int(choice[0]),
                dst_p=int(choice[1]),
                count=1,
            )
        return

    if not state.cfg.has_insectes_peuple or int(ctx.get("m_num", 0)) != 5:
        return
    r_nid, p_nid = int(ctx["ray"]), int(ctx["p"])
    if state.get_parcel_insectes(r_nid, p_nid) < 1:
        return
    allowed_rays = {r_nid}
    seat_e = state.cfg.seat_of_peuple("E")
    if seat_e is not None:
        allowed_rays.add(seat_e)
    dests = tuple(
        (dr, dp)
        for dr in sorted(allowed_rays)
        for dp in range(1, state.cfg.p_max + 1)
        if (dr, dp) != (r_nid, p_nid)
        and not state.is_route_forestiere(dr, dp)
        and state.get_parcel_souches(dr, dp) >= 1
    )
    if not dests:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "M5"),
        ("PASSER", *dests),
        {"effect_kind": "M5_MOVE_SOUCHE", "ray": r_nid, "p": p_nid},
        slot_id="M5",
        profile="A",
        resume_tag="MOVE_SOUCHE",
        resume_payload=(r_nid, p_nid),
    )
