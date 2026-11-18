"""Lot 09 — Implémentation stateless des 12 profils de Croissance (M1:A..M3:D).

Règles strictes :
- 100 % stdlib PyPy 3.11 (zéro dépendance externe, zéro _buf, zéro random, zéro global mutable).
- Utilise exclusivement les constantes, accesseurs et primitives de contracts/core_state_api.md.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_4_1_FURTIVITE,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_5_CONTACT_NID,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_LAW_QUERY,
    HOOK_5_PARADE_CLASSIQUE,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    TRACK_LEN,
    GameState,
)

LOT_09_PROFILES: tuple[tuple[str, str], ...] = (
    ("M1", "A"),
    ("M1", "B"),
    ("M1", "C"),
    ("M1", "D"),
    ("M2", "A"),
    ("M2", "B"),
    ("M2", "C"),
    ("M2", "D"),
    ("M3", "A"),
    ("M3", "B"),
    ("M3", "C"),
    ("M3", "D"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _nid_1cran_moves(state: GameState, r: int, p: int) -> list[tuple[Any, ...]]:
    n = state.cfg.n_players
    opts: list[tuple[Any, ...]] = []
    p_fwd = state.next_non_razed_towards_heart(r, p)
    if p_fwd is not None:
        opts.append(("FORET", r, p_fwd))
    p_back = state.next_non_razed_towards_border(r, p)
    if p_back is not None:
        opts.append(("FORET", r, p_back))
    right_l = r
    left_l = (r - 1) % n
    for l_adj in (right_l, left_l):
        if state.get_furtivite_insectes(l_adj, p) < 15:
            cand = ("FURTIVITE", l_adj, p)
            if cand not in opts:
                opts.append(cand)
    if p == state.last_non_razed_parcel(r):
        for c in range(1, TRACK_LEN + 1):
            opts.append(("BUG", c))
        for c in range(1, TRACK_LEN + 1):
            opts.append(("COLONIE", c))
    return opts


def _apply_insect_1cran_move(
    state: GameState, src_r: int, src_p: int, mv: tuple[Any, ...]
) -> None:
    mk = str(mv[0])
    if mk == "FORET":
        prim_deplacement(
            state,
            "INSECTE",
            src_ray=src_r,
            src_p=src_p,
            dst_ray=int(mv[1]),
            dst_p=int(mv[2]),
            count=1,
        )
    elif mk == "FURTIVITE":
        prim_deplacement(
            state,
            "INSECTE",
            src_ray=src_r,
            src_p=src_p,
            dst_lisiere=int(mv[1]),
            dst_p=int(mv[2]),
            count=1,
        )
    elif mk in ("BUG", "COLONIE"):
        prim_deplacement(
            state,
            "INSECTE",
            src_ray=src_r,
            src_p=src_p,
            global_track=mk,
            global_case=int(mv[1]),
            count=1,
        )


# ---------------------------------------------------------------------------
# 1. M1:A — La Fourmilière Coupe-Feuilles (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M1", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m1_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, déplace 1 Défenseur de M1 vers toute autre parcelle Forêt non rasée."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 1:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_defenseurs(r, p) < 1:
            return
        cands: list[tuple[int, int]] = []
        for dr in range(state.cfg.n_players):
            for dp in range(1, state.cfg.p_max + 1):
                if (dr, dp) != (r, p) and not state.is_route_forestiere(dr, dp):
                    cands.append((dr, dp))
        if not cands:
            return
        if len(cands) == 1:
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_ray=r,
                src_p=p,
                dst_ray=cands[0][0],
                dst_p=cands[0][1],
                count=1,
            )
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(cands),
            {"effect_kind": "M1_DEPLACER_DEFENSEUR", "src_ray": r, "src_p": p},
            slot_id="M1",
            profile="A",
            resume_tag="MOVE_DEF",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        dr, dp = int(ctx["choice"][0]), int(ctx["choice"][1])
        if state.get_parcel_defenseurs(sr, sp) >= 1 and not state.is_route_forestiere(dr, dp):
            prim_deplacement(
                state, "DEFENSEUR", src_ray=sr, src_p=sp, dst_ray=dr, dst_p=dp, count=1
            )


# ---------------------------------------------------------------------------
# 2. M1:B — La Fourmilière Coupe-Feuilles (Insectes) : LOI 5 (Carapaces)
# ---------------------------------------------------------------------------


@register_tile("M1", "B", hooks=(HOOK_5_PARADE_CLASSIQUE, HOOK_5_LAW_QUERY))
def m1_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 (Carapaces) : 1 fois/tour sur M1, si >=1 Défenseur local, épargne 1 Insecte défaussé."""
    prim_mod_loi_du_coeur(state, "LOI_CARAPACES_EPARGNE_INSECTE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(1) is not None

    if hook == HOOK_5_PARADE_CLASSIQUE:
        if state.has_slot_used_once_per_turn("M1"):
            return False
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        if state.get_parcel_nid(ray, target_p)[0] != 1:
            return False
        if int(ctx["local_defs"]) < 1 or int(ctx["ins_to_discard"]) < 1:
            return False
        ctx["ins_to_discard"] = int(ctx["ins_to_discard"]) - 1
        state.mark_slot_used_once_per_turn("M1")
        return True
    return False


# ---------------------------------------------------------------------------
# 3. M1:C — La piste des fourmis légionnaires (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M1", "C", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m1_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, vous pouvez déplacer 1 Insecte de M1 sur son rayon."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 1:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_insectes(r, p) < 1:
            return
        dsts = [
            dp
            for dp in range(1, state.cfg.p_max + 1)
            if dp != p and not state.is_route_forestiere(r, dp)
        ]
        if not dsts:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("PASSER", *dsts),
            {"effect_kind": "M1_DEPLACER_INSECTE_RAYON", "ray": r, "src_p": p},
            slot_id="M1",
            profile="C",
            resume_tag="MOVE_INS",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        dp = int(choice)
        if state.get_parcel_insectes(sr, sp) >= 1 and not state.is_route_forestiere(sr, dp):
            prim_deplacement(
                state, "INSECTE", src_ray=sr, src_p=sp, dst_ray=sr, dst_p=dp, count=1
            )


# ---------------------------------------------------------------------------
# 4. M1:D — Les fourmis sentinelles (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M1", "D", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m1_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, vous pouvez envoyer jusqu'à 2 Insectes vers des Pièges du rayon."""
    gov = _gov(state, "I")

    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 1:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_insectes(r, p) < 1:
            return
        traps = [
            dp
            for dp in range(1, state.cfg.p_max + 1)
            if dp != p
            and not state.is_route_forestiere(r, dp)
            and state.get_parcel_piege(r, dp) == PIEGE_ACTIF
        ]
        if not traps:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *traps),
            {"effect_kind": "M1_SENTINELLES_PIEGES", "step": 1, "ray": r, "src_p": p},
            slot_id="M1",
            profile="D",
            resume_tag="TRAP_1",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        dp = int(choice)
        if state.get_parcel_insectes(sr, sp) >= 1 and not state.is_route_forestiere(sr, dp):
            prim_deplacement(
                state, "INSECTE", src_ray=sr, src_p=sp, dst_ray=sr, dst_p=dp, count=1
            )
        if rtag == "TRAP_1" and state.get_parcel_insectes(sr, sp) >= 1:
            rem_traps = [
                p_idx
                for p_idx in range(1, state.cfg.p_max + 1)
                if p_idx != sp
                and p_idx != dp
                and not state.is_route_forestiere(sr, p_idx)
                and state.get_parcel_piege(sr, p_idx) == PIEGE_ACTIF
            ]
            if rem_traps:
                push_effect_decision(
                    state,
                    gov,
                    ("PASSER", *rem_traps),
                    {"effect_kind": "M1_SENTINELLES_PIEGES", "step": 2, "ray": sr, "src_p": sp},
                    slot_id="M1",
                    profile="D",
                    resume_tag="TRAP_2",
                    resume_payload=(sr, sp),
                )


# ---------------------------------------------------------------------------
# 5. M2:A — La Termitière à Glu (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M2", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m2_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, retourne 1 jeton rouge d'une machine du rayon ou voisin."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 2:
            return
        r = int(ctx["ray"])
        n = state.cfg.n_players
        adj_rays: list[int] = []
        for cand_r in (r, (r - 1) % n, (r + 1) % n):
            if cand_r not in adj_rays:
                adj_rays.append(cand_r)
        cands: list[tuple[int, int]] = []
        for mr in adj_rays:
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(mr, mt)
                if (
                    st != MACHINE_STATUS_RETIRED
                    and pos > 0
                    and state.get_machine_tokens(mr, mt)[0] >= 1
                ):
                    cands.append((mr, mt))
        if not cands:
            return
        if len(cands) == 1:
            prim_mod_puissance(state, cands[0][0], cands[0][1], flip_rouge_to_bleu=1)
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            tuple(cands),
            {"effect_kind": "M2_SURCHAUFFE_VOISINE"},
            slot_id="M2",
            profile="A",
            resume_tag="FLIP_GLU",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        mr, mt = int(ctx["choice"][0]), int(ctx["choice"][1])
        prim_mod_puissance(state, mr, mt, flip_rouge_to_bleu=1)


# ---------------------------------------------------------------------------
# 6. M2:B — La Termitière à Glu (Insectes) : LOI 4.1 (Insecte furtif permanent)
# ---------------------------------------------------------------------------


@register_tile("M2", "B", hooks=(HOOK_4_1_FURTIVITE, HOOK_5_LAW_QUERY))
def m2_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 4.1 : sur les deux lisières bordant M2, l'Insecte d'un binôme n'est pas défaussé."""
    prim_mod_loi_du_coeur(state, "LOI_INSECTE_FURTIF_PERMANENT", active=True)
    pos_info = state.get_nid_position(2)
    if hook == HOOK_5_LAW_QUERY:
        return pos_info is not None

    if hook == HOOK_4_1_FURTIVITE and ctx.get("phase") == "PRE" and pos_info is not None:
        nid_r = pos_info[0]
        n = state.cfg.n_players
        if int(ctx["lisiere"]) in (nid_r, (nid_r - 1) % n):
            ctx["keep_insect"] = True
            return True
    return False


# ---------------------------------------------------------------------------
# 7. M2:C — La souche creuse (Insectes) : LOI CONTACT MACHINE
# ---------------------------------------------------------------------------


@register_tile("M2", "C", hooks=(HOOK_5_CONTACT_NID, HOOK_5_LAW_QUERY))
def m2_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi contact : M2 survit au contact d'une machine si sa parcelle porte >= 1 Souche."""
    prim_mod_loi_du_coeur(state, "LOI_NID_CONTACT_SOUCHE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(2) is not None

    if (
        hook == HOOK_5_CONTACT_NID
        and int(ctx["m_num"]) == 2
        and state.get_parcel_souches(int(ctx["ray"]), int(ctx["p"])) >= 1
    ):
        ctx["protected"] = True
        return True
    return False


# ---------------------------------------------------------------------------
# 8. M2:D — La termitière gardée (Insectes) : LOI CONTACT MACHINE
# ---------------------------------------------------------------------------


@register_tile("M2", "D", hooks=(HOOK_5_CONTACT_NID, HOOK_5_LAW_QUERY))
def m2_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi contact : M2 survit si sa parcelle porte 1 Piège ET >= 1 Défenseur ou Insecte."""
    prim_mod_loi_du_coeur(state, "LOI_NID_CONTACT_PIEGE_GARDE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(2) is not None

    if hook == HOOK_5_CONTACT_NID and int(ctx["m_num"]) == 2:
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_piege(r, p) != PIEGE_AUCUN and (
            state.get_parcel_defenseurs(r, p) >= 1 or state.get_parcel_insectes(r, p) >= 1
        ):
            ctx["protected"] = True
            return True
    return False


# ---------------------------------------------------------------------------
# 9. M3:A — La Branche des Guêpes Cazadores (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M3", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m3_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, déplace d'1 cran jusqu'à 2 Insectes présents sur M3."""
    gov = _gov(state, "I")

    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 3:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_insectes(r, p) < 1:
            return
        moves = _nid_1cran_moves(state, r, p)
        if not moves:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *moves),
            {"effect_kind": "M3_CAZADORES_1CRAN", "step": 1, "ray": r, "p": p},
            slot_id="M3",
            profile="A",
            resume_tag="CAZ_1",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        if state.get_parcel_insectes(sr, sp) >= 1:
            _apply_insect_1cran_move(state, sr, sp, choice)
        if rtag == "CAZ_1" and state.get_parcel_insectes(sr, sp) >= 1:
            moves_2 = _nid_1cran_moves(state, sr, sp)
            if moves_2:
                push_effect_decision(
                    state,
                    gov,
                    ("PASSER", *moves_2),
                    {"effect_kind": "M3_CAZADORES_1CRAN", "step": 2, "ray": sr, "p": sp},
                    slot_id="M3",
                    profile="A",
                    resume_tag="CAZ_2",
                    resume_payload=(sr, sp),
                )


# ---------------------------------------------------------------------------
# 10. M3:B — La Branche des Guêpes Cazadores (Insectes) : LOI 4.2 (Pouponnière)
# ---------------------------------------------------------------------------


@register_tile("M3", "B", hooks=(HOOK_5_LAW_QUERY,))
def m3_b_handler(state: GameState, hook: str, _ctx: dict[str, Any]) -> bool:
    """Loi 4.2 (Pouponnière) : M3 s'active sans Défenseur en 4.2 s'il contient >= 2 Insectes."""
    prim_mod_loi_du_coeur(state, "LOI_NID_AUTONOME", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(3) is not None
    return False


# ---------------------------------------------------------------------------
# 11. M3:C — Le Scarabée Hercule (Insectes) : LOI 5 (Défense double Insectes)
# ---------------------------------------------------------------------------


@register_tile(
    "M3",
    "C",
    hooks=(HOOK_5_DEFENSE_PARCELLE, HOOK_5_PARADE_CLASSIQUE, HOOK_5_LAW_QUERY),
)
def m3_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 : sur la parcelle de M3, chaque Insecte vaut 2 en Défense (défausse ceil(manque/2))."""
    prim_mod_loi_du_coeur(state, "LOI_INSECTES_DEFENSE_DOUBLE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(3) is not None

    ray = int(ctx["ray"])
    target_p = int(ctx["target_p"])
    if state.get_parcel_nid(ray, target_p)[0] != 3:
        return False

    if hook == HOOK_5_DEFENSE_PARCELLE:
        ctx["ins_points"] = int(ctx["ins_points"]) * 2
        return True

    if hook == HOOK_5_PARADE_CLASSIQUE:
        manque = int(ctx.get("manque", ctx["ins_to_discard"]))
        local_ins = state.get_parcel_insectes(ray, target_p)
        ctx["ins_to_discard"] = min(local_ins, (manque + 1) // 2)
        return True
    return False


# ---------------------------------------------------------------------------
# 12. M3:D — Les guêpes aux aguets (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M3", "D", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m3_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, si M3 contient >=1 Insecte et 0 Piège, peut poser 1 Piège."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 3:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if (
            not state.is_route_forestiere(r, p)
            and state.get_parcel_insectes(r, p) >= 1
            and state.get_parcel_piege(r, p) == PIEGE_AUCUN
        ):
            push_effect_decision(
                state,
                _gov(state, "I"),
                ("PASSER", "POSER_PIEGE"),
                {"effect_kind": "M3_AUTO_PIEGE_NID", "ray": r, "p": p},
                slot_id="M3",
                profile="D",
                resume_tag="PIEGE_M3",
                resume_payload=(r, p),
            )
        return

    if hook == HOOK_EFFECT_RESUME and ctx["choice"] == "POSER_PIEGE":
        r, p = int(ctx["payload"][0]), int(ctx["payload"][1])
        if (
            not state.is_route_forestiere(r, p)
            and state.get_parcel_piege(r, p) == PIEGE_AUCUN
        ):
            prim_creation_entite(state, "PIEGE", ray=r, p=p, light_trigger=True)
