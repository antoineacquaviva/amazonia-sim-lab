"""Catalogue actif v5.5 — Les 10 Rêves STANDARD_A (R1:A..R10:A).

Compatibilité complète avec le socle gelé v5.5 :
- Activation sur coût d'activation (1 Défenseur annule 1 machine) et avancée CLEAR_RANK_ONLY ;
- Partition stricte des 6 déclencheurs (création d'entité via effet de tuile : light_trigger=False) ;
- 100 % stateless, zéro accès `_buf`, zéro `random`, stdlib PyPy 3.11 pure.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_puissance,
    prim_mod_seuil,
    prim_partage_info_etat_gardien,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    PIEGE_AUCUN,
    TRACK_LEN,
    GameState,
)

__all__ = (
    "REVES_V5_5_PROFILES",
    "r1_a_handler",
    "r2_a_handler",
    "r3_a_handler",
    "r4_a_handler",
    "r5_a_handler",
    "r6_a_handler",
    "r7_a_handler",
    "r8_a_handler",
    "r9_a_handler",
    "r10_a_handler",
)

REVES_V5_5_PROFILES: tuple[tuple[str, str], ...] = (
    ("R1", "A"),
    ("R2", "A"),
    ("R3", "A"),
    ("R4", "A"),
    ("R5", "A"),
    ("R6", "A"),
    ("R7", "A"),
    ("R8", "A"),
    ("R9", "A"),
    ("R10", "A"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _rays_for_peuples(state: GameState, p1: str, p2: str) -> list[int]:
    out: list[int] = []
    for code in (p1, p2):
        seat = state.cfg.seat_of_peuple(code)
        if seat is not None and seat not in out:
            out.append(seat)
    return out


def _machines_with_red_token(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                rouges, bleus = state.get_machine_tokens(r, mt)
                if rouges >= 1 and bleus < 15:
                    out.append((r, mt))
    return out


def _total_insects_on_ray(state: GameState, ray: int) -> int:
    total = 0
    for p in range(1, state.cfg.p_max + 1):
        if not state.is_route_forestiere(ray, p):
            total += state.get_parcel_insectes(ray, p)
    return total


# ---------------------------------------------------------------------------
# R1:A & R2:A — Emplacements neutres dans le socle initial v5.5
# ---------------------------------------------------------------------------


@register_tile("R1", "A", hooks=(HOOK_3_2_OUVERTURE_REVE,))
def r1_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Emplacement neutre dans le socle initial v5.5 (piste des Tactiques fixe)."""
    _ = (state, hook, ctx)


@register_tile("R2", "A", hooks=(HOOK_3_2_OUVERTURE_REVE,))
def r2_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Emplacement neutre dans le socle initial v5.5 (en attente de reconception post-baseline)."""
    _ = (state, hook, ctx)


# ---------------------------------------------------------------------------
# R3:A — La Danse des Esprits-Fauves (DEPLACEMENT jusqu'à 2 DEFENSEURS)
# ---------------------------------------------------------------------------


def _r3_a_tracked_sources(state: GameState) -> list[tuple[str, int, int]]:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    sources: list[tuple[str, int, int]] = []

    for r in range(n):
        for p in range(1, p_max + 1):
            if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 1:
                sources.append(("FORET", r, p))

    tracked_furt: set[tuple[int, int]] = set()
    tracked_lis: set[int] = set()
    for s in range(n):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw == 0:
                continue
            kind, a, b, _ = state.decode_def_loc(raw)
            if kind == "FURTIVITE":
                tracked_furt.add((a, b))
            elif kind == "LISIERE":
                tracked_lis.add(a)

    for l_idx in range(n):
        for p in range(1, p_max + 1):
            if (l_idx, p) in tracked_furt and state.get_furtivite_total_defs(l_idx, p) >= 1:
                sources.append(("FURTIVITE", l_idx, p))

    for slot_idx in range(2 * n):
        if slot_idx in tracked_lis and state.get_lisiere_tile_state(slot_idx)[1] >= 1:
            sources.append(("LISIERE", slot_idx, 0))

    return sources


def _r3_a_build_moves(
    state: GameState,
) -> list[tuple[tuple[str, int, int], tuple[int, int]]]:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    dests = [
        (r, p)
        for r in range(n)
        for p in range(1, p_max + 1)
        if not state.is_route_forestiere(r, p)
    ]
    if not dests:
        return []
    sources = _r3_a_tracked_sources(state)
    moves: list[tuple[tuple[str, int, int], tuple[int, int]]] = []
    for src in sources:
        for dst_r, dst_p in dests:
            if src == ("FORET", dst_r, dst_p):
                continue
            moves.append((src, (dst_r, dst_p)))
    return moves


def _r3_a_apply_single_move(
    state: GameState, choice: tuple[tuple[str, int, int], tuple[int, int]]
) -> None:
    (src_kind, src_a, src_p), (dst_r, dst_p) = choice
    if src_kind == "FORET":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_ray=int(src_a),
            src_p=int(src_p),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    elif src_kind == "FURTIVITE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_lisiere=int(src_a),
            src_p=int(src_p),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    elif src_kind == "LISIERE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_lisiere_slot=int(src_a),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )


@register_tile("R3", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r3_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, déplace jusqu'à 2 Défenseurs (y compris constructeurs en lisière)."""
    gov = _gov(state, "H")

    if hook == HOOK_3_2_OUVERTURE_REVE:
        moves = _r3_a_build_moves(state)
        if not moves:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *moves),
            {"effect_kind": "DANSE_REDEPLOIEMENT_DEFENSEURS", "step": 1},
            slot_id="R3",
            profile="A",
            resume_tag="DANSE_MOVE_1",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        _r3_a_apply_single_move(state, choice)
        if rtag == "DANSE_MOVE_1":
            moves_2 = _r3_a_build_moves(state)
            if moves_2:
                push_effect_decision(
                    state,
                    gov,
                    ("PASSER", *moves_2),
                    {"effect_kind": "DANSE_REDEPLOIEMENT_DEFENSEURS", "step": 2},
                    slot_id="R3",
                    profile="A",
                    resume_tag="DANSE_MOVE_2",
                )


# ---------------------------------------------------------------------------
# R4:A — Le Sommeil de la Pierre-Serpent (MOD_PUISSANCE SURCHAUFFE)
# ---------------------------------------------------------------------------


@register_tile("R4", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, retourne 1 jeton Puissance rouge d'une machine sur sa face bleue."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        cands = _machines_with_red_token(state)
        if not cands:
            return
        if len(cands) == 1:
            prim_mod_puissance(state, cands[0][0], cands[0][1], flip_rouge_to_bleu=1)
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(cands),
            {"effect_kind": "PIERRE_SERPENT_SURCHAUFFE"},
            slot_id="R4",
            profile="A",
            resume_tag="SURCHAUFFE_R4_A",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rm, mt = ctx["choice"]
        prim_mod_puissance(state, int(rm), int(mt), flip_rouge_to_bleu=1)


# ---------------------------------------------------------------------------
# R5:A — La Vision des Plumes Claires (OUVRIR GARDIEN en 3.2)
# ---------------------------------------------------------------------------


@register_tile("R5", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, ouvre immédiatement un Gardien ayant >= 1 Défenseur en pari."""
    gov = _gov(state, "H")

    if hook == HOOK_3_2_OUVERTURE_REVE:
        avail = [
            c
            for c in range(1, TRACK_LEN + 1)
            if state.get_gardien_at_case(c)[0] > 0
            and state.count_gardien_pari_defenders_at_case(c) >= 1
        ]
        if not avail:
            return
        if len(avail) == 1:
            prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=avail[0])
            return
        push_effect_decision(
            state,
            gov,
            avail,
            {"effect_kind": "OPEN_GARDIEN"},
            slot_id="R5",
            profile="A",
            resume_tag="OPEN_G",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        chosen_case = int(ctx["choice"])
        prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=chosen_case)


# ---------------------------------------------------------------------------
# R6:A — Le Miel des Ancêtres (CREATION_ENTITE INSECTE sur H/I)
# ---------------------------------------------------------------------------


@register_tile("R6", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r6_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Insecte sur une parcelle non rasée d'un rayon H ou I (light_trigger=False)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        hi_rays = _rays_for_peuples(state, "H", "I")
        if not hi_rays:
            return
        cands: list[tuple[int, int]] = [
            (r, p)
            for r in hi_rays
            for p in range(1, state.cfg.p_max + 1)
            if not state.is_route_forestiere(r, p)
        ]
        if not cands:
            return
        if len(cands) == 1:
            prim_creation_entite(
                state, "INSECTE", ray=cands[0][0], p=cands[0][1], count=1, light_trigger=False
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
            prim_creation_entite(
                state, "INSECTE", ray=r_c, p=p_c, count=1, light_trigger=False
            )


# ---------------------------------------------------------------------------
# R7:A — L'Ombre du Maître des Bois (DEPLACEMENT MACHINE RECUL sur E/M)
# ---------------------------------------------------------------------------


def _reculable_em_machines(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in _rays_for_peuples(state, "E", "M"):
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
    """Recule d'1 parcelle non rasée vers la bordure une machine hors Ratissage sur E ou M."""
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
# R8:A — Le Mirage du Fleuve-Miroir (CREATION_ENTITE PIEGE sur E/R)
# ---------------------------------------------------------------------------


@register_tile("R8", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r8_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R (light_trigger=False)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        er_rays = _rays_for_peuples(state, "E", "R")
        if not er_rays:
            return
        cands: list[tuple[int, int]] = [
            (r, p)
            for r in er_rays
            for p in range(1, state.cfg.p_max + 1)
            if not state.is_route_forestiere(r, p)
            and state.get_parcel_piege(r, p) == PIEGE_AUCUN
        ]
        if not cands:
            return
        if len(cands) == 1:
            prim_creation_entite(
                state, "PIEGE", ray=cands[0][0], p=cands[0][1], light_trigger=False
            )
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(cands),
            {"effect_kind": "PIEGE_ER_3_2"},
            slot_id="R8",
            profile="A",
            resume_tag="POSE_PIEGE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        r_c, p_c = int(ctx["choice"][0]), int(ctx["choice"][1])
        if (
            not state.is_route_forestiere(r_c, p_c)
            and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN
        ):
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=False)


# ---------------------------------------------------------------------------
# R9:A — L'Écho des Voix Célestes (MOD_SEUIL -2 RAYON)
# ---------------------------------------------------------------------------


@register_tile("R9", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r9_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Réduit de -2 le Seuil de Parade sur toutes les parcelles d'un rayon au choix."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        opts = tuple(range(state.cfg.n_players))
        push_effect_decision(
            state,
            _gov(state, "E"),
            opts,
            {"effect_kind": "MOD_SEUIL_RAYON_MOINS_2"},
            slot_id="R9",
            profile="A",
            resume_tag="RAY_SEUIL",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        prim_mod_seuil(state, -2, ray=int(ctx["choice"]))


# ---------------------------------------------------------------------------
# R10:A — La Nuée des Songes (MOD_SEUIL SCALING INSECTES)
# ---------------------------------------------------------------------------


@register_tile("R10", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r10_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Réduit le Seuil de Parade d'1 machine de -1 par Insecte sur son rayon."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        cands: list[tuple[int, int]] = []
        for r in range(state.cfg.n_players):
            if _total_insects_on_ray(state, r) <= 0:
                continue
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                pos, st, _ = state.get_machine_pos_status(r, mt)
                if st != MACHINE_STATUS_RETIRED and pos > 0:
                    cands.append((r, mt))
        if not cands:
            return
        if len(cands) == 1:
            rm, mt = cands[0]
            ins_r = _total_insects_on_ray(state, rm)
            if ins_r > 0:
                prim_mod_seuil(state, -ins_r, ray=rm, m_type=mt)
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            tuple(cands),
            {"effect_kind": "SCALING_INSECTES_SEUIL"},
            slot_id="R10",
            profile="A",
            resume_tag="SCALING_M",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rm, mt = int(ctx["choice"][0]), int(ctx["choice"][1])
        ins_r = _total_insects_on_ray(state, rm)
        if ins_r > 0:
            prim_mod_seuil(state, -ins_r, ray=rm, m_type=mt)
