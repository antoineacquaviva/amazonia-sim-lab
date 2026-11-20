"""Lot 08 — Implémentation stateless des 9 profils de Rêves (R8:A..R10:D).

Clôture 100 % de la famille REVE (31/31).

Règles strictes :
- 100 % stdlib PyPy 3.11 (zéro dépendance externe, zéro _buf, zéro random, zéro global mutable).
- Utilise exclusivement les constantes, accesseurs et primitives de contracts/core_state_api.md.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_5_LAW_QUERY,
    HOOK_5_TERRASSEMENT,
    HOOK_6_2_AVANCEMENT,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    prim_mod_seuil,
    prim_permutation_piste,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameState,
)

LOT_08_PROFILES: tuple[tuple[str, str], ...] = (
    ("R8", "A"),
    ("R8", "B"),
    ("R8", "C"),
    ("R8", "D"),
    ("R9", "A"),
    ("R9", "B"),
    ("R10", "A"),
    ("R10", "B"),
    ("R10", "D"),
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


def _total_insects_on_ray(state: GameState, ray: int) -> int:
    return sum(
        state.get_parcel_insectes(ray, p)
        for p in range(1, state.cfg.p_max + 1)
        if not state.is_route_forestiere(ray, p)
    )


def _machines_targeting_parcel(state: GameState, ray: int, p: int) -> list[int]:
    """Retourne les m_type sur `ray` dont la cible en 3.2 inclut `(ray, p)`."""
    matched: list[int] = []
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st, _ = state.get_machine_pos_status(ray, mt)
        if st == MACHINE_STATUS_RATISSAGE and pos == p:
            matched.append(mt)
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if not (1 <= card <= 12) or bound_t not in TACTIQUES_SPEC:
            continue
        rm, mt = (card - 1) // 2, (card - 1) % 2
        if rm != ray or mt in matched:
            continue
        pos, st, _ = state.get_machine_pos_status(rm, mt)
        if st != MACHINE_STATUS_NORMAL or pos <= 0:
            continue
        spec = TACTIQUES_SPEC[bound_t]
        for c_kind in spec.cibles:
            if c_kind == "SUR_PLACE" and pos == p:
                matched.append(mt)
                break
            if c_kind == "DEVANT" and state.next_non_razed_towards_heart(rm, pos) == p:
                matched.append(mt)
                break
    return matched


# ---------------------------------------------------------------------------
# 1. R8:A — Le Mirage du Fleuve-Miroir (Entités) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R8", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r8_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Piège sur une parcelle non rasée sans Piège des rayons E ou R (allume 2)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        er_rays = _rays_for_peuples(state, "E", "R")
        if not er_rays:
            return
        cands: list[tuple[int, int]] = []
        for r in er_rays:
            for p in range(1, state.cfg.p_max + 1):
                if (
                    not state.is_route_forestiere(r, p)
                    and state.get_parcel_piege(r, p) == PIEGE_AUCUN
                ):
                    cands.append((r, p))
        if not cands:
            return
        if len(cands) == 1:
            prim_creation_entite(
                state, "PIEGE", ray=cands[0][0], p=cands[0][1], light_trigger=True
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
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=True)


# ---------------------------------------------------------------------------
# 2. R8:B — Le Mirage du Fleuve-Miroir (Entités) : LOI TERRASSEMENT
# ---------------------------------------------------------------------------


@register_tile("R8", "B", hooks=(HOOK_5_TERRASSEMENT, HOOK_5_LAW_QUERY))
def r8_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi de terrassement : sur E et R, laisse 1 Souche si >= 1 Défenseur ou Insecte local."""
    prim_mod_loi_du_coeur(state, "LOI_DERNIERE_SOUCHE_INDESTRUCTIBLE", active=True)
    er_rays = _rays_for_peuples(state, "E", "R")
    if hook == HOOK_5_LAW_QUERY:
        if "ray" in ctx:
            return int(ctx["ray"]) in er_rays
        return bool(er_rays)

    ray = int(ctx["ray"])
    target_p = int(ctx["target_p"])
    if ray not in er_rays:
        return False
    if state.get_parcel_defenseurs(ray, target_p) >= 1 or state.get_parcel_insectes(ray, target_p) >= 1:
        ctx["protected_souches"] = max(int(ctx["protected_souches"]), 1)
        return True
    return False


# ---------------------------------------------------------------------------
# 3. R8:C — Le Mapinguari (Entités) : LOI 3.2 ANNULATION
# ---------------------------------------------------------------------------


@register_tile("R8", "C", hooks=(HOOK_3_2_REVELATION, HOOK_5_LAW_QUERY))
def r8_c_handler(state: GameState, hook: str, _ctx: dict[str, Any]) -> bool:
    """Loi 3.2 : chaque machine dont R8 annule l'attaque en 3.2 recule d'1 parcelle."""
    prim_mod_loi_du_coeur(state, "LOI_REVE_ANNULE_MACHINE_RECULE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return True

    if hook == HOOK_3_2_REVELATION:
        r8_rank = state.find_tactique_rank(TILE_R_BASE + 8)
        if r8_rank is None:
            return False
        target_m = r8_rank + 1
        moved = False
        for s in range(state.cfg.n_players):
            card, _, _, lec_m, _ = state.get_player_hand(s)
            if not (1 <= card <= 12) or lec_m != target_m:
                continue
            rm, mt = (card - 1) // 2, (card - 1) % 2
            pos, st, _ = state.get_machine_pos_status(rm, mt)
            if st != MACHINE_STATUS_NORMAL or pos <= 0:
                continue
            dst_p = state.next_non_razed_towards_border(rm, pos)
            if dst_p is not None:
                prim_deplacement(state, "MACHINE", src_ray=rm, m_type=mt, dst_ray=rm, dst_p=dst_p)
                moved = True
        return moved
    return False


# ---------------------------------------------------------------------------
# 4. R8:D — L’appel des berges gardées (Entités) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R8", "D", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r8_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez transférer 1 Défenseur E/R vers une parcelle piégée E/R, puis +1 bleu."""
    gov = _gov(state, "E")

    if hook == HOOK_3_2_OUVERTURE_REVE:
        er_rays = _rays_for_peuples(state, "E", "R")
        if not er_rays:
            return
        srcs: list[tuple[int, int]] = []
        dsts: list[tuple[int, int]] = []
        for r in er_rays:
            for p in range(1, state.cfg.p_max + 1):
                if state.is_route_forestiere(r, p):
                    continue
                if state.get_parcel_defenseurs(r, p) >= 1:
                    srcs.append((r, p))
                if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                    dsts.append((r, p))
        pairs = tuple((src, dst) for src in srcs for dst in dsts if src != dst)
        if not pairs:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *pairs),
            {"effect_kind": "TRANSFERT_DEF_PIEGE_ER"},
            slot_id="R8",
            profile="D",
            resume_tag="MOVE_DEF",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        if rtag == "MOVE_DEF":
            if choice == "PASSER":
                return
            (sr, sp), (dr, dp) = choice
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_ray=int(sr),
                src_p=int(sp),
                dst_ray=int(dr),
                dst_p=int(dp),
                count=1,
            )
            m_cands = [
                mt
                for mt in _machines_targeting_parcel(state, int(dr), int(dp))
                if state.get_machine_effective_rouges(int(dr), mt) >= 1
            ]
            if not m_cands:
                return
            if len(m_cands) == 1:
                prim_mod_puissance(state, int(dr), m_cands[0], flip_rouge_to_bleu=1)
                return
            push_effect_decision(
                state,
                gov,
                tuple(m_cands),
                {"effect_kind": "SURCHAUFFE_CIBLE_DESTINATION", "ray": int(dr)},
                slot_id="R8",
                profile="D",
                resume_tag="FLIP_ROUGE",
                resume_payload=(int(dr),),
            )
            return

        if rtag == "FLIP_ROUGE":
            dr = int(ctx["payload"][0])
            prim_mod_puissance(state, dr, int(choice), flip_rouge_to_bleu=1)


# ---------------------------------------------------------------------------
# 5. R9:A — L’Écho des Voix Célestes (Entités) : SIMPLE_CONTINU | 3.2
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
# 6. R9:B — L’Écho des Voix Célestes (Entités) : LOI 6.2
# ---------------------------------------------------------------------------


@register_tile("R9", "B", hooks=(HOOK_6_2_AVANCEMENT, HOOK_5_LAW_QUERY))
def r9_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Neutralisé en v5.4.2 (Apprentissage supprimé ; à réajuster pour le Mode 4)."""
    _ = (state, hook, ctx)
    return False


# ---------------------------------------------------------------------------
# 7. R10:A — La Nuée des Songes (Entités) : SIMPLE_CONTINU | 3.2
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


# ---------------------------------------------------------------------------
# 8. R10:B — La Nuée des Songes (Entités) : SIMPLE_CONTINU | 3.2 (Conversion)
# ---------------------------------------------------------------------------


@register_tile("R10", "B", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r10_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez défausser 1 Insecte de la roue pour faire avancer R10 d'1 rang de plus."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        r10_rank = state.find_tactique_rank(TILE_R_BASE + 10)
        if r10_rank is None or r10_rank <= 0:
            return
        cands: list[tuple[str, int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    cands.append(("FORET", r, p))
                if state.get_furtivite_insectes(r, p) >= 1:
                    cands.append(("FURTIVITE", r, p))
        if not cands:
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            ("PASSER", *cands),
            {"effect_kind": "CONVERSION_INSECTE_AVANCEE_R10"},
            slot_id="R10",
            profile="B",
            resume_tag="CONV_INS",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        kind, idx_a, p = str(choice[0]), int(choice[1]), int(choice[2])
        paid = False
        if kind == "FORET":
            cur = state.get_parcel_insectes(idx_a, p)
            if cur >= 1:
                state.set_parcel_insectes(idx_a, p, cur - 1)
                paid = True
        elif kind == "FURTIVITE":
            cur = state.get_furtivite_insectes(idx_a, p)
            if cur >= 1:
                state.set_furtivite_insectes(idx_a, p, cur - 1)
                paid = True
        if paid:
            r10_rank = state.find_tactique_rank(TILE_R_BASE + 10)
            if r10_rank is not None and r10_rank > 0:
                prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=r10_rank)


# ---------------------------------------------------------------------------
# 9. R10:D — La relève des lucioles (Entités) : SIMPLE_CONTINU | 3.2 (Groupe)
# ---------------------------------------------------------------------------


@register_tile("R10", "D", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r10_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez poser 1 Piège (E/I avec >=1 Déf & >=1 Ins) puis déplacer 1 Insecte du rayon."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        ei_rays = _rays_for_peuples(state, "E", "I")
        if not ei_rays:
            return
        cands: list[tuple[int, int, int]] = []
        for r in ei_rays:
            non_razed = [
                p for p in range(1, state.cfg.p_max + 1) if not state.is_route_forestiere(r, p)
            ]
            if len(non_razed) < 2:
                continue
            for src_p in non_razed:
                if (
                    state.get_parcel_piege(r, src_p) == PIEGE_AUCUN
                    and state.get_parcel_defenseurs(r, src_p) >= 1
                    and state.get_parcel_insectes(r, src_p) >= 1
                ):
                    for dst_p in non_razed:
                        if dst_p != src_p:
                            cands.append((r, src_p, dst_p))
        if not cands:
            return
        push_effect_decision(
            state,
            _gov(state, "E"),
            ("PASSER", *cands),
            {"effect_kind": "PIEGE_ET_REDEPLOIEMENT_INSECTE"},
            slot_id="R10",
            profile="D",
            resume_tag="GROUPE_LUCIOLES",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_c, src_p, dst_p = int(choice[0]), int(choice[1]), int(choice[2])
        if (
            not state.is_route_forestiere(r_c, src_p)
            and not state.is_route_forestiere(r_c, dst_p)
            and state.get_parcel_piege(r_c, src_p) == PIEGE_AUCUN
            and state.get_parcel_insectes(r_c, src_p) >= 1
        ):
            prim_creation_entite(state, "PIEGE", ray=r_c, p=src_p, light_trigger=False)
            prim_deplacement(
                state,
                "INSECTE",
                src_ray=r_c,
                src_p=src_p,
                dst_ray=r_c,
                dst_p=dst_p,
                count=1,
            )
            state.light_trigger(2)
