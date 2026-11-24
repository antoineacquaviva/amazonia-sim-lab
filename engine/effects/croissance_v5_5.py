"""Catalogue actif v5.5 — Les 5 Nids / Croissance STANDARD_A (M1:A..M5:A).

Compatibilité complète avec le socle gelé v5.5 :
- Partition stricte des 6 déclencheurs (jamais déclenché en 4.2, light_trigger=False) ;
- Contrôle strict des jetons rouges physiques sur M2:A ;
- 100 % stateless, zéro accès `_buf`, zéro `random`, stdlib PyPy 3.11 pure.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_4_2_NID_APRES_PROD,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_puissance,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    PFLAG_SANCTUAIRE_SOUCHE,
    TRACK_LEN,
    GameState,
)

__all__ = (
    "CROISSANCE_V5_5_PROFILES",
    "m1_a_handler",
    "m2_a_handler",
    "m3_a_handler",
    "m4_a_handler",
    "m5_a_handler",
)

CROISSANCE_V5_5_PROFILES: tuple[tuple[str, str], ...] = (
    ("M1", "A"),
    ("M2", "A"),
    ("M3", "A"),
    ("M4", "A"),
    ("M5", "A"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _nid_1cran_moves(state: GameState, r: int, p: int) -> list[tuple[Any, ...]]:
    if not state.cfg.has_insectes_peuple:
        return []
    opts: list[tuple[Any, ...]] = []
    p_fwd = state.next_non_razed_towards_heart(r, p)
    if p_fwd is not None:
        opts.append(("FORET", r, p_fwd))
    p_back = state.next_non_razed_towards_border(r, p)
    if p_back is not None:
        opts.append(("FORET", r, p_back))
    if p == state.last_non_razed_parcel(r):
        for c in range(1, TRACK_LEN + 1):
            opts.append(("BUG", c))
        if state.cfg.nb_animaux_sauvages >= 1:
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
# M1:A — La Fourmilière Coupe-Feuilles (4.2 DEPLACEMENT DEFENSEUR)
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
        cands: list[tuple[int, int]] = [
            (dr, dp)
            for dr in range(state.cfg.n_players)
            for dp in range(1, state.cfg.p_max + 1)
            if (dr, dp) != (r, p) and not state.is_route_forestiere(dr, dp)
        ]
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
# M2:A — La Termitière à Glu (4.2 MOD_PUISSANCE SURCHAUFFE VOISINE)
# ---------------------------------------------------------------------------


@register_tile("M2", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m2_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, retourne 1 jeton rouge physique d'une machine du rayon ou voisin."""
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
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    rouges, bleus = state.get_machine_tokens(mr, mt)
                    if rouges >= 1 and bleus < 15:
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
# M3:A — La Branche des Guêpes Cazadores (4.2 DEPLACEMENT jusqu'à 2 INSECTES)
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
# M4:A — La Ruche des Mélipones (4.2 CREATION_ENTITE SABOTAGE avec coût)
# ---------------------------------------------------------------------------


@register_tile("M4", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, peut défausser 1 Insecte de M4 pour +1 Sabotage permanent."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 4:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_insectes(r, p) < 1:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("PASSER", "DILUER_SABOTAGE"),
            {"effect_kind": "M4_SABOTAGE_4_2", "ray": r, "p": p},
            slot_id="M4",
            profile="A",
            resume_tag="M4_SAB",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME and ctx["choice"] == "DILUER_SABOTAGE":
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        cur = state.get_parcel_insectes(sr, sp)
        if cur >= 1:
            state.set_parcel_insectes(sr, sp, cur - 1)
            prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=False)


# ---------------------------------------------------------------------------
# M5:A — La Clairière du Jardin du Diable (4.2 SANCTUAIRE_SOUCHE avec coût)
# ---------------------------------------------------------------------------


@register_tile("M5", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, peut défausser 1 Insecte de M5 pour SANCTUAIRE_SOUCHE ce tour."""
    if hook == HOOK_4_2_NID_APRES_PROD:
        if int(ctx["m_num"]) != 5:
            return
        r, p = int(ctx["ray"]), int(ctx["p"])
        if state.get_parcel_insectes(r, p) < 1:
            return
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("PASSER", "SANCTUAIRE_SOUCHE"),
            {"effect_kind": "M5_SANCTUAIRE_4_2", "ray": r, "p": p},
            slot_id="M5",
            profile="A",
            resume_tag="SANCT",
            resume_payload=(r, p),
        )
        return

    if hook == HOOK_EFFECT_RESUME and ctx["choice"] == "SANCTUAIRE_SOUCHE":
        sr, sp = int(ctx["payload"][0]), int(ctx["payload"][1])
        cur = state.get_parcel_insectes(sr, sp)
        if cur >= 1:
            state.set_parcel_insectes(sr, sp, cur - 1)
            state.set_parcel_flag_turn(sr, sp, PFLAG_SANCTUAIRE_SOUCHE, True)
