"""Lot 10 — 7 derniers profils Croissance (M4:A,B,D, M5:A..D) portant le catalogue à 100/100."""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_3_MIGRATION_DESTS,
    HOOK_5_3_PRE_RETRAIT,
    HOOK_5_LAW_QUERY,
    HOOK_5_TERRASSEMENT,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    push_effect_decision,
)
from engine.state import (
    PFLAG_SANCTUAIRE_SOUCHE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    TRACK_LEN,
    GameState,
)

LOT_10_PROFILES: tuple[tuple[str, str], ...] = (
    ("M4", "A"),
    ("M4", "B"),
    ("M4", "D"),
    ("M5", "A"),
    ("M5", "B"),
    ("M5", "C"),
    ("M5", "D"),
)


def _gov(state: GameState, peuple: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple)
    return seat if seat is not None else state.coordonnateur


def _next_non_razed_towards_heart(state: GameState, ray: int, p: int) -> int | None:
    for dp in range(p + 1, state.cfg.p_max + 1):
        if not state.is_route_forestiere(ray, dp):
            return dp
    return None


# ---------------------------------------------------------------------------
# 1. M4:A — La Ruche des Mélipones (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M4", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, vous pouvez défausser 1 Insecte de M4 pour +1 Sabotage (case 3)."""
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
            prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=True)


# ---------------------------------------------------------------------------
# 2. M4:B — La Ruche des Mélipones (Insectes) : LOI 5.3
# ---------------------------------------------------------------------------


@register_tile("M4", "B", hooks=(HOOK_5_3_PRE_RETRAIT, HOOK_5_LAW_QUERY))
def m4_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5.3 : les Pièges déclenchés du rayon de M4 glissent vers le cœur (sans allumer 2)."""
    prim_mod_loi_du_coeur(state, "LOI_PIEGE_GLISSE_VERS_CENTRE", active=True)
    pos = state.get_nid_position(4)
    if hook == HOOK_5_LAW_QUERY:
        return pos is not None

    if hook == HOOK_5_3_PRE_RETRAIT and pos is not None:
        nid_r = pos[0]
        moved_any = False
        for p in range(state.cfg.p_max, 0, -1):
            if state.get_parcel_piege(nid_r, p) != PIEGE_DECLENCHE:
                continue
            dst_p = _next_non_razed_towards_heart(state, nid_r, p)
            if dst_p is not None and state.get_parcel_piege(nid_r, dst_p) == PIEGE_AUCUN:
                state.set_parcel_piege(nid_r, p, PIEGE_AUCUN)
                state.set_parcel_piege(nid_r, dst_p, PIEGE_ACTIF)
                moved_any = True
        return moved_any
    return False


# ---------------------------------------------------------------------------
# 3. M4:D — Les mélipones convoyeurs (Insectes) : LOI 5.3 RÉCUPÉRATION
# ---------------------------------------------------------------------------


@register_tile("M4", "D", hooks=(HOOK_5_3_PRE_RETRAIT, HOOK_EFFECT_RESUME, HOOK_5_LAW_QUERY))
def m4_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5.3 : 1 fois/tour, fait glisser ensemble 1 Piège déclenché + 1 Insecte vers le cœur."""
    prim_mod_loi_du_coeur(state, "LOI_CONVOI_PIEGE_INSECTE", active=True)
    pos = state.get_nid_position(4)
    if hook == HOOK_5_LAW_QUERY:
        return pos is not None

    if hook == HOOK_5_3_PRE_RETRAIT:
        if pos is None or state.has_slot_used_once_per_turn("M4"):
            return False
        nid_r = pos[0]
        cands: list[tuple[int, int]] = []
        for p in range(state.cfg.p_max, 0, -1):
            if (
                state.get_parcel_piege(nid_r, p) == PIEGE_DECLENCHE
                and state.get_parcel_insectes(nid_r, p) >= 1
            ):
                dst_p = _next_non_razed_towards_heart(state, nid_r, p)
                if dst_p is not None and state.get_parcel_piege(nid_r, dst_p) == PIEGE_AUCUN:
                    cands.append((p, dst_p))
        if not cands:
            return False
        push_effect_decision(
            state,
            _gov(state, "I"),
            ("PASSER", *cands),
            {"effect_kind": "M4_CONVOI_5_3", "ray": nid_r},
            slot_id="M4",
            profile="D",
            resume_tag="CONVOI",
            resume_payload=(nid_r,),
        )
        return True

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return False
        nid_r = int(ctx["payload"][0])
        sp, dp = int(choice[0]), int(choice[1])
        if (
            state.get_parcel_piege(nid_r, sp) == PIEGE_DECLENCHE
            and state.get_parcel_insectes(nid_r, sp) >= 1
            and state.get_parcel_piege(nid_r, dp) == PIEGE_AUCUN
        ):
            state.set_parcel_piege(nid_r, sp, PIEGE_AUCUN)
            state.set_parcel_piege(nid_r, dp, PIEGE_ACTIF)
            prim_deplacement(
                state, "INSECTE", src_ray=nid_r, src_p=sp, dst_ray=nid_r, dst_p=dp, count=1
            )
            state.light_trigger(2)
            state.mark_slot_used_once_per_turn("M4")
            return True
    return False


# ---------------------------------------------------------------------------
# 4. M5:A — La Clairière du Jardin du Diable (Insectes) : 4.2 APRÈS PRODUCTION
# ---------------------------------------------------------------------------


@register_tile("M5", "A", hooks=(HOOK_4_2_NID_APRES_PROD, HOOK_EFFECT_RESUME))
def m5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Après production en 4.2, défausse 1 Insecte de M5 pour activer SANCTUAIRE_SOUCHE ce tour."""
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


# ---------------------------------------------------------------------------
# 5. M5:B — La Clairière du Jardin du Diable (Insectes) : LOI 4.3
# ---------------------------------------------------------------------------


@register_tile("M5", "B", hooks=(HOOK_4_3_MIGRATION_DESTS, HOOK_5_LAW_QUERY))
def m5_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 4.3 (Tunnel du cœur) : 1 fois/tour, défausse 1 Insecte de M5 pour migrer vers piste."""
    prim_mod_loi_du_coeur(state, "LOI_TUNNEL_MIGRATION_DIRECTE", active=True)
    pos = state.get_nid_position(5)
    if hook == HOOK_5_LAW_QUERY:
        return pos is not None

    if hook == HOOK_4_3_MIGRATION_DESTS and pos is not None:
        nid_r, nid_p, _ = pos
        if ctx["src"] != ("FORET", nid_r, nid_p):
            return False
        if ctx.get("phase") == "APPLIED":
            cur = state.get_parcel_insectes(nid_r, nid_p)
            if not state.has_slot_used_once_per_turn("M5") and cur >= 1:
                state.set_parcel_insectes(nid_r, nid_p, cur - 1)
                state.mark_slot_used_once_per_turn("M5")
                return True
            return False

        if state.has_slot_used_once_per_turn("M5") or state.get_parcel_insectes(nid_r, nid_p) < 2:
            return False
        opts: list[tuple[Any, ...]] = ctx["opts"]
        added = False
        for track in ("BUG", "COLONIE"):
            for c in range(1, TRACK_LEN + 1):
                cand = (track, c)
                if cand not in opts:
                    opts.append(cand)
                    added = True
        return added
    return False


# ---------------------------------------------------------------------------
# 6. M5:C — Le Figuier étrangleur (Insectes) : LOI TERRASSEMENT BULLDOZER
# ---------------------------------------------------------------------------


@register_tile("M5", "C", hooks=(HOOK_5_TERRASSEMENT, HOOK_5_LAW_QUERY))
def m5_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi de terrassement : sur la parcelle de M5, les Bulldozers ne terrassent aucune Souche."""
    prim_mod_loi_du_coeur(state, "LOI_SOUCHES_PROTEGEES_PAR_NID", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return state.get_nid_position(5) is not None

    if (
        hook == HOOK_5_TERRASSEMENT
        and state.get_parcel_nid(int(ctx["ray"]), int(ctx["target_p"]))[0] == 5
    ):
        ctx["protected_souches"] = int(ctx["souches_after_cut"])
        return True
    return False


# ---------------------------------------------------------------------------
# 7. M5:D — Le jardin des relèveuses (Insectes) : LOI 5.3 PRÉ-RETRAIT
# ---------------------------------------------------------------------------


@register_tile("M5", "D", hooks=(HOOK_5_3_PRE_RETRAIT, HOOK_5_LAW_QUERY))
def m5_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5.3 : si Piège déclenché sur M5 actif ce tour, crée 1 Insecte avant retrait (case 6)."""
    prim_mod_loi_du_coeur(state, "LOI_NID_RELEVE_APRES_EMBUSCADE", active=True)
    pos = state.get_nid_position(5)
    if hook == HOOK_5_LAW_QUERY:
        return pos is not None

    if hook == HOOK_5_3_PRE_RETRAIT and pos is not None:
        nid_r, nid_p, active_ce_tour = pos
        if active_ce_tour and state.get_parcel_piege(nid_r, nid_p) == PIEGE_DECLENCHE:
            prim_creation_entite(state, "INSECTE", ray=nid_r, p=nid_p, count=1, light_trigger=True)
            return True
    return False
