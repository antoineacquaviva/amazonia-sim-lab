"""Catalogue Canon v6.4 — Les 5 Nids de l'Essaim (M1..M5, profil 'A').

100 % stateless, stdlib pure PyPy 3.11, zéro `_buf`, zéro `random`, zéro dette mémorielle (`mem_debt == 0`).
Source de vérité : `contracts/tiles_canon_v6_4.json`.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_APRES_DEVIATION,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_2_NID_AVANT_PROD,
    HOOK_5_PARADE_SOLDATS,
    HOOK_EFFECT_RESUME,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_deplacement_nid,
    push_continuation_sequence,
    push_effect_decision,
    verb_alterer,
    verb_semer_au_sac,
)
from engine.state import (
    CHAMAN_TAMBOUR,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    PERCHOIR_KIND_RAY,
    TRACK_LEN,
    TRIG_INSECTE,
    GameState,
    is_reve_code,
)

__all__ = (
    "m1_pelage_paresseux_v6_4",
    "m2_termitiere_forteresse_v6_4",
    "m3_bivouac_legionnaires_v6_4",
    "m4_rucher_melipones_v6_4",
    "m5_mycelium_luminescent_v6_4",
)


def _gov(state: GameState, peuple: str) -> int:
    for s, p in enumerate(state.cfg.peuples):
        if p == peuple:
            return s
    return state.coordonnateur


def _ray_distance_circular(n: int, r1: int, r2: int) -> int:
    d = abs(r1 - r2)
    return min(d, n - d)


def _occupied_nid_parcels(state: GameState, exclude_m: int = 0) -> set[tuple[int, int]]:
    out: set[tuple[int, int]] = set()
    for m_num in range(1, 6):
        if m_num == exclude_m:
            continue
        info = state.get_nid_position(m_num)
        if info is not None:
            out.add((info[0], info[1]))
    return out


def _nid_adjacent_free_parcels(
    state: GameState, ray: int, p: int, occupied: set[tuple[int, int]]
) -> list[tuple[int, int]]:
    """Parcelles libres adjacentes (radial en sautant les Routes + latéral même profondeur sur rayons voisins)."""
    n = state.cfg.n_players
    out: list[tuple[int, int]] = []
    p_heart = state.next_non_razed_towards_heart(ray, p)
    if p_heart is not None and (ray, p_heart) not in occupied:
        out.append((ray, p_heart))
    p_bord = state.next_non_razed_towards_border(ray, p)
    if p_bord is not None and (ray, p_bord) not in occupied:
        out.append((ray, p_bord))
    for nr in sorted({(ray - 1) % n, (ray + 1) % n}):
        if nr != ray and not state.is_route_forestiere(nr, p) and (nr, p) not in occupied:
            out.append((nr, p))
    return out


def _adjacent_non_razed_parcels(state: GameState, ray: int, p: int) -> set[tuple[int, int]]:
    n = state.cfg.n_players
    adj: set[tuple[int, int]] = set()
    p_heart = state.next_non_razed_towards_heart(ray, p)
    if p_heart is not None:
        adj.add((ray, p_heart))
    p_bord = state.next_non_razed_towards_border(ray, p)
    if p_bord is not None:
        adj.add((ray, p_bord))
    for nr in ((ray - 1) % n, (ray + 1) % n):
        if nr != ray and not state.is_route_forestiere(nr, p):
            adj.add((nr, p))
    return adj


# ---------------------------------------------------------------------------
# M1 — Le Pelage du Paresseux (I>M)
# ---------------------------------------------------------------------------


@register_tile("M1", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m1_pelage_paresseux_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """M1 Le Pelage du Paresseux v6.4 : embarque 1–2 Insectes passagers sur 1 machine (son rayon ou voisin).

    Le saut à la parade (avec retournement Duel natif) et la descente au ménage sont natifs dans le noyau.
    """
    if hook == HOOK_4_2_NID_APRES_PROD:
        ray, p = int(ctx["ray"]), int(ctx["p"])
        ins = state.get_parcel_insectes(ray, p)
        if ins < 1:
            return
        n = state.cfg.n_players
        near_rays = sorted({ray, (ray - 1) % n, (ray + 1) % n})
        opts: list[Any] = ["PASSER"]
        for r_m in near_rays:
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r_m, mt)
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    cur_pass = state.get_machine_passenger_insects(r_m, mt)
                    max_add = min(2, ins, 3 - cur_pass)
                    for cnt in range(1, max_add + 1):
                        opts.append((r_m, mt, cnt))
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(opts),
            {"effect_kind": "M1_EMBARQUER", "nid_ray": ray, "nid_p": p},
            slot_id="M1",
            profile="A",
            resume_tag="M1_BOARD",
            resume_payload=(ray, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        ray, p = int(ctx["payload"][0]), int(ctx["payload"][1])
        r_m, mt, cnt = int(ch[0]), int(ch[1]), int(ch[2])
        avail = state.get_parcel_insectes(ray, p)
        cur_pass = state.get_machine_passenger_insects(r_m, mt)
        actual = min(cnt, avail, 3 - cur_pass)
        if actual >= 1:
            state.set_parcel_insectes(ray, p, avail - actual)
            state.set_machine_passenger_insects(r_m, mt, cur_pass + actual)


# ---------------------------------------------------------------------------
# M2 — La Termitière-Forteresse (I>R)
# ---------------------------------------------------------------------------


@register_tile("M2", "A", hooks=(HOOK_5_PARADE_SOLDATS, HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m2_termitiere_forteresse_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """M2 La Termitière-Forteresse v6.4 : Soldats à glu (2 Insectes parent seuls quel que soit le Seuil) + Semer Écaille ou Croc."""
    if hook == HOOK_5_PARADE_SOLDATS:
        info = state.get_nid_position(2)
        if info is None:
            return
        r_n, p_n, _ = info
        if int(ctx["ray"]) != r_n or int(ctx["target_p"]) != p_n:
            return
        if state.get_parcel_insectes(r_n, p_n) < 2:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("SOLDATS_A_GLU", "PASSER"),
            {
                "effect_kind": "M2_SOLDATS_A_GLU",
                "ray": r_n,
                "p": p_n,
                "seuil": int(ctx["seuil"]),
            },
            slot_id="M2",
            profile="A",
            resume_tag="M2_SOLDATS",
            resume_payload=(r_n, p_n, ctx["resume_parried"], ctx["resume_declined"]),
        )
        return

    if hook == HOOK_4_2_NID_APRES_PROD:
        ray, p = int(ctx["ray"]), int(ctx["p"])
        opts: list[str] = ["PASSER"]
        if state.cfg.accessories_enabled:
            if state.count_total_ecailles_in_play() < 4:
                opts.append("SEMER_ECAILLE")
            croc_pos = state.get_croc_parcel()
            has_mobile_here = any(
                state.get_machine_pos_status(ray, mt)[0] == p
                and state.get_machine_pos_status(ray, mt)[1] == MACHINE_STATUS_NORMAL
                for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
            )
            if croc_pos is None and has_mobile_here and not state.is_route_forestiere(ray, p):
                opts.append("POSER_CROC")
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(opts),
            {"effect_kind": "M2_PROD_REPTILE", "ray": ray, "p": p},
            slot_id="M2",
            profile="A",
            resume_tag="M2_PROD",
            resume_payload=(ray, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = str(ctx["choice"])
        if tag == "M2_SOLDATS":
            r_n, p_n, res_parried, res_declined = ctx["payload"]
            if ch == "SOLDATS_A_GLU" and state.get_parcel_insectes(int(r_n), int(p_n)) >= 2:
                state.set_parcel_insectes(
                    int(r_n), int(p_n), state.get_parcel_insectes(int(r_n), int(p_n)) - 2
                )
                state.light_trigger(TRIG_INSECTE)
                d_st, d_r, d_p = state.get_duel_state()
                if d_st != 0 and d_r == int(r_n) and d_p == int(p_n):
                    state.flip_duel_to_territoire_tenu()
                push_continuation_sequence(state, (res_parried,))
            else:
                push_continuation_sequence(state, (res_declined,))
        elif tag == "M2_PROD":
            ray, p = int(ctx["payload"][0]), int(ctx["payload"][1])
            if ch == "SEMER_ECAILLE":
                verb_semer_au_sac(state, "ECAILLE", 1)
            elif ch == "POSER_CROC":
                prim_creation_entite(state, "CROC", ray=ray, p=p)


# ---------------------------------------------------------------------------
# M3 — Le Bivouac des Légionnaires (I>O)
# ---------------------------------------------------------------------------


@register_tile("M3", "A", hooks=(HOOK_4_2_NID_AVANT_PROD, HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m3_bivouac_legionnaires_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """M3 Le Bivouac des Légionnaires v6.4 : marche 1 parcelle (ou 2 vers Perchoir) avant Prod + Front de raid 1–2 Insectes."""
    if hook == HOOK_4_2_NID_AVANT_PROD:
        ray, p = int(ctx["ray"]), int(ctx["p"])
        occupied = _occupied_nid_parcels(state, exclude_m=3)
        step1 = _nid_adjacent_free_parcels(state, ray, p, occupied)
        dests: set[tuple[int, int]] = set(step1)

        p_face, p_kind, p_val, _ = state.get_oiseau_perchoir_signal()
        if p_face != 0 and p_kind == PERCHOIR_KIND_RAY and 0 <= p_val < state.cfg.n_players:
            n = state.cfg.n_players
            d0 = _ray_distance_circular(n, ray, p_val)
            for r1, p1 in step1:
                d1 = _ray_distance_circular(n, r1, p_val)
                if d1 <= d0:
                    for r2, p2 in _nid_adjacent_free_parcels(state, r1, p1, occupied):
                        if (r2, p2) != (ray, p) and _ray_distance_circular(n, r2, p_val) <= d1:
                            dests.add((r2, p2))

        if not dests:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("PASSER", *sorted(dests)),
            {"effect_kind": "M3_BIVOUAC_MARCHE", "src_ray": ray, "src_p": p},
            slot_id="M3",
            profile="A",
            resume_tag="M3_MOVE",
        )
        return

    if hook == HOOK_4_2_NID_APRES_PROD:
        ray, p = int(ctx["ray"]), int(ctx["p"])
        ins = state.get_parcel_insectes(ray, p)
        if ins < 1:
            return
        adj = _adjacent_non_razed_parcels(state, ray, p)
        targeted_adj = sorted(rp for rp in list_targeted_parcels(state) if rp in adj)
        if not targeted_adj:
            return
        opts: list[Any] = ["PASSER"]
        max_send = min(2, ins)
        for dst_r, dst_p in targeted_adj:
            for cnt in range(1, max_send + 1):
                opts.append((dst_r, dst_p, cnt))
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(opts),
            {"effect_kind": "M3_FRONT_DE_RAID", "src_ray": ray, "src_p": p},
            slot_id="M3",
            profile="A",
            resume_tag="M3_RAID",
            resume_payload=(ray, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        if tag == "M3_MOVE":
            prim_deplacement_nid(state, 3, int(ch[0]), int(ch[1]))
        elif tag == "M3_RAID":
            src_r, src_p = int(ctx["payload"][0]), int(ctx["payload"][1])
            dst_r, dst_p, cnt = int(ch[0]), int(ch[1]), int(ch[2])
            for _ in range(cnt):
                if state.get_parcel_insectes(src_r, src_p) >= 1:
                    prim_deplacement(
                        state,
                        "INSECTE",
                        src_ray=src_r,
                        src_p=src_p,
                        dst_ray=dst_r,
                        dst_p=dst_p,
                    )


# ---------------------------------------------------------------------------
# M4 — Le Rucher des Mélipones (I>H)
# ---------------------------------------------------------------------------


def _m4_tambour_forest_parcel(state: GameState) -> tuple[int, int] | None:
    for s in range(state.cfg.n_players):
        if state.cfg.peuples[s] != "H":
            continue
        for d in (0, 1):
            if state.get_humain_chaman_archetype(d) == CHAMAN_TAMBOUR:
                kind, a, b, _ = state.decode_def_loc(state.get_player_def_loc_raw(s, d))
                if kind == "FORET" and not state.is_route_forestiere(a, b):
                    return (a, b)
    return None


def _m4_prompt(state: GameState, ray: int, p: int, rem: int) -> None:
    if rem <= 0 or state.get_parcel_insectes(ray, p) < 1:
        return
    waiting = state.list_available_waiting_defenders()
    if not waiting:
        return
    dests: list[tuple[int, int]] = []
    if not state.is_route_forestiere(ray, p):
        dests.append((ray, p))
    t_pos = _m4_tambour_forest_parcel(state)
    if t_pos is not None and t_pos not in dests:
        dests.append(t_pos)
    if not dests:
        return
    opts: list[Any] = ["PASSER"]
    for s_w, d_w in waiting:
        for dst_r, dst_p in dests:
            opts.append((s_w, d_w, dst_r, dst_p))
    push_effect_decision(
        state,
        _gov(state, "I"),
        tuple(opts),
        {"effect_kind": "M4_MELIPONES_RELEVER", "nid_ray": ray, "nid_p": p, "rem": rem},
        slot_id="M4",
        profile="A",
        resume_tag="M4_LIFT",
        resume_payload=(ray, p, rem),
    )


@register_tile("M4", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m4_rucher_melipones_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """M4 Le Rucher des Mélipones v6.4 : 1–2 Insectes défaussés -> relève 1–2 Défenseurs en attente sur M4 ou Tambour."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        _m4_prompt(state, int(ctx["ray"]), int(ctx["p"]), 2)
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        ray, p, rem = int(ctx["payload"][0]), int(ctx["payload"][1]), int(ctx["payload"][2])
        s_w, d_w, dst_r, dst_p = int(ch[0]), int(ch[1]), int(ch[2]), int(ch[3])
        ins = state.get_parcel_insectes(ray, p)
        if ins >= 1:
            state.set_parcel_insectes(ray, p, ins - 1)
            prim_deplacement(
                state, "DEFENSEUR", src_seat=s_w, src_def_idx=d_w, dst_ray=dst_r, dst_p=dst_p
            )
            _m4_prompt(state, ray, p, rem - 1)


# ---------------------------------------------------------------------------
# M5 — Le Mycélium luminescent (I>E)
# ---------------------------------------------------------------------------


@register_tile("M5", "A", hooks=(HOOK_3_2_APRES_DEVIATION, HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m5_mycelium_luminescent_v6_4(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """M5 Le Mycélium luminescent v6.4 : Loi passive (Déviation vers Rêve -> Altérer + recycle si < 2) + Filaments oniriques."""
    if hook == HOOK_3_2_APRES_DEVIATION:
        info = state.get_nid_position(5)
        if info is None:
            return
        r_n, p_n, _ = info
        new_case = int(ctx["new_case"])
        if 1 <= new_case <= TRACK_LEN and is_reve_code(state.get_tactique_at_rank(new_case - 1)):
            verb_alterer(state, int(ctx["ray"]), int(ctx["m_type"]))
            if state.get_parcel_insectes(r_n, p_n) < 2 and state.cfg.has_insectes_peuple:
                prim_creation_entite(state, "INSECTE", ray=r_n, p=p_n, light_trigger=False)
        return

    if hook == HOOK_4_2_NID_APRES_PROD:
        ray, p = int(ctx["ray"]), int(ctx["p"])
        opts: list[Any] = ["PASSER"]
        if state.get_parcel_insectes(ray, p) >= 1:
            for c in range(1, TRACK_LEN + 1):
                opts.append(("BUG_RANK", c))
        for r_m in range(state.cfg.n_players):
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r_m, mt)
                if (
                    st == MACHINE_STATUS_NORMAL
                    and pos > 0
                    and not state.has_machine_alteration(r_m, mt)
                ):
                    opts.append(("ALTERER", r_m, mt))
        if len(opts) <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(opts),
            {"effect_kind": "M5_FILAMENTS_ONIRIQUES", "ray": ray, "p": p},
            slot_id="M5",
            profile="A",
            resume_tag="M5_PROD",
            resume_payload=(ray, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ch = ctx["choice"]
        if ch == "PASSER":
            return
        ray, p = int(ctx["payload"][0]), int(ctx["payload"][1])
        if str(ch[0]) == "BUG_RANK":
            prim_deplacement(
                state, "INSECTE", src_ray=ray, src_p=p, global_track="BUG", global_case=int(ch[1])
            )
        elif str(ch[0]) == "ALTERER":
            verb_alterer(state, int(ch[1]), int(ch[2]))
