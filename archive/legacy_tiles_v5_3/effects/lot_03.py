"""Lot 03 — Gardiens G5:C..G9:B (10 profils stateless, 100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_1_3_LECTURE_DE,
    HOOK_3_2_APRES_REVELATION,
    HOOK_3_2_REVELATION,
    HOOK_4_1_FURTIVITE,
    HOOK_5_CIBLAGE_MACHINE,
    HOOK_5_DEBUT,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_LAW_QUERY,
    HOOK_5_ORDRE_RAYON,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    push_effect_decision,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameState,
    machine_card_code,
)

__all__ = (
    "LOT_03_PROFILES",
    "g5_c_handler",
    "g6_b_handler",
    "g6_c_handler",
    "g7_b_handler",
    "g7_c_handler",
    "g7_d_handler",
    "g8_a_handler",
    "g8_b_handler",
    "g9_a_handler",
    "g9_b_handler",
)

LOT_03_PROFILES: tuple[tuple[str, str], ...] = (
    ("G5", "C"),
    ("G6", "B"),
    ("G6", "C"),
    ("G7", "B"),
    ("G7", "C"),
    ("G7", "D"),
    ("G8", "A"),
    ("G8", "B"),
    ("G9", "A"),
    ("G9", "B"),
)

# Bits transitoires (42..54) dans TRANS_ONCE_PER_TURN (remis à zéro automatiquement en 6.2)
G8_A_PREPARED_LOCK: int = 42
G8_A_RESOLVED_LOCK: int = 43
G8_A_ACTIVE_SHIFT_LOCK: int = 44
G8_A_RAY_BIT0: int = 45  # 45..47 : rayon 0..5 sur 3 bits
G8_A_MTYPE_BIT: int = 48  # 0 = Abatteuse, 1 = Bulldozer
G8_A_DIR_HEART_BIT: int = 49  # 0 = -1 (vers bordure), 1 = +1 (vers cœur)

G8_B_ACTIVE_INV_LOCK: int = 50
G8_B_RAY_BIT0: int = 51  # 51..53 : rayon 0..5 sur 3 bits

G9_B_F2_AT_3_2_START_LOCK: int = 54


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _gardien_face_on_track(state: GameState, g_num: int) -> int:
    for c in range(1, TRACK_LEN + 1):
        gn, face = state.get_gardien_at_case(c)
        if gn == g_num:
            return face
    return 0


def _common_lisiere(state: GameState, p1: str, p2: str) -> int | None:
    s1 = state.cfg.seat_of_peuple(p1)
    s2 = state.cfg.seat_of_peuple(p2)
    if s1 is None or s2 is None:
        return None
    n = state.cfg.n_players
    if (s1 + 1) % n == s2:
        return s1
    if (s2 + 1) % n == s1:
        return s2
    return None


def _find_tracked_defender_foret(state: GameState, ray: int, p: int) -> tuple[int, int] | None:
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, b, _ = state.decode_def_loc(raw)
                if kind == "FORET" and a == ray and b == p:
                    return (s, d)
    return None


def _is_machine_active_turn(state: GameState, ray: int, m_type: int) -> bool:
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
        return False
    if st == MACHINE_STATUS_RATISSAGE:
        return True
    t_card = machine_card_code(ray, m_type)
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if card == t_card and bound_t > 0:
            return True
    return False


# ---------------------------------------------------------------------------
# 1. G5:C — Le Perchoir du caïman (LOI 5 : soutien machine -> devant sur R et O)
# ---------------------------------------------------------------------------


@register_tile("G5", "C", hooks=(HOOK_5_DEFENSE_PARCELLE, HOOK_5_LAW_QUERY))
def g5_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 : sur R et O, sur frappe DEVANT, chaque Défenseur sur la machine soutient (+1)."""
    r_seat = state.cfg.seat_of_peuple("R")
    o_seat = state.cfg.seat_of_peuple("O")
    ray = int(ctx["ray"])
    eligible_ray = ray in (r_seat, o_seat)

    prim_mod_loi_du_coeur(state, "LOI_SOUTIEN_MACHINE_VERS_DEVANT", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return eligible_ray and ctx.get("cible_type") == "DEVANT"

    if not eligible_ray or ctx.get("cible_type") != "DEVANT":
        return False

    m_type = int(ctx["m_type"])
    target_p = int(ctx["target_p"])
    m_pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or m_pos <= 0 or m_pos == target_p:
        return False
    if state.is_route_forestiere(ray, m_pos):
        return False

    defs_on_machine = state.get_parcel_defenseurs(ray, m_pos)
    if defs_on_machine <= 0:
        return False

    ctx["remote_support"] = int(ctx["remote_support"]) + defs_on_machine
    return True


# ---------------------------------------------------------------------------
# 2. G6:B — L’Œil Double du Toucan (LOI 1.3 : O et R peuvent retenir max(D1, D2))
# ---------------------------------------------------------------------------


@register_tile(
    "G6",
    "B",
    hooks=(HOOK_1_3_LECTURE_DE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g6_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Loi 1.3 : derrière leur paravent, O et R peuvent retenir M = max(D1, D2)."""
    prim_mod_loi_du_coeur(state, "LOI_DE_M_CHOIX_MIN_MAX", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return False

    if hook == HOOK_1_3_LECTURE_DE:
        seat = int(ctx["seat"])
        o_seat = state.cfg.seat_of_peuple("O")
        r_seat = state.cfg.seat_of_peuple("R")
        if seat not in (o_seat, r_seat):
            return None
        card, d1, d2, _, _ = state.get_player_hand(seat)
        if not (1 <= card <= 12) or d1 == d2:
            return None
        push_effect_decision(
            state,
            seat,
            ("PASSER", "RETENIR_MAX"),
            {"effect_kind": "CHOIX_DE_M_1_3", "min_m": min(d1, d2), "max_m": max(d1, d2)},
            slot_id="G6",
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
# 3. G6:C — Le Vol en ciseaux (ECHANGE_ATOMIQUE Défenseur O/R <-> Insecte Furtivité)
# ---------------------------------------------------------------------------


def _build_g6_c_options(state: GameState, l_idx: int) -> list[tuple[int, int, int]]:
    opts: list[tuple[int, int, int]] = []
    r0 = state.lisiere_ray_for_rive(l_idx, 0)
    r1 = state.lisiere_ray_for_rive(l_idx, 1)
    for p in range(1, state.cfg.p_max + 1):
        if state.get_furtivite_insectes(l_idx, p) < 1:
            continue
        if state.get_furtivite_total_defs(l_idx, p) >= 2:
            continue
        valid_rives: list[int] = []
        if not state.is_route_forestiere(r0, p):
            valid_rives.append(0)
        if not state.is_route_forestiere(r1, p):
            valid_rives.append(1)
        if not valid_rives:
            continue
        for src_ray in (r0, r1):
            if (
                not state.is_route_forestiere(src_ray, p)
                and state.get_parcel_defenseurs(src_ray, p) >= 1
                and _find_tracked_defender_foret(state, src_ray, p) is not None
            ):
                for dst_rive in valid_rives:
                    opts.append((src_ray, p, dst_rive))
    return opts


@register_tile("G6", "C", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g6_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Échange atomique 1 Défenseur (O/R) <-> 1 Insecte de la case Furtivité commune O-R."""
    gov = _gov(state, "O")

    if hook == HOOK_GARDIEN_OUVERTURE:
        l_idx = _common_lisiere(state, "O", "R")
        if l_idx is None:
            return
        opts = _build_g6_c_options(state, l_idx)
        if not opts:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *opts),
            {"effect_kind": "ECHANGE_CISEAUX_G6C", "lisiere": l_idx},
            slot_id="G6",
            profile="C",
            resume_tag="SWAP_OR",
            resume_payload=(l_idx,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        l_idx = int(ctx["payload"][0])
        src_ray, p, dst_rive = int(choice[0]), int(choice[1]), int(choice[2])
        if (
            state.get_furtivite_insectes(l_idx, p) < 1
            or state.get_furtivite_total_defs(l_idx, p) >= 2
            or state.is_route_forestiere(src_ray, p)
            or state.is_route_forestiere(state.lisiere_ray_for_rive(l_idx, dst_rive), p)
        ):
            return
        tracked = _find_tracked_defender_foret(state, src_ray, p)
        if tracked is None:
            return
        seat_d, def_idx = tracked
        face_d = (
            FACE_DEFINITIF
            if (def_idx == 0 or state.is_player_def2_definitif(seat_d))
            else FACE_REFLEXION
        )
        state.enter_furtivite(seat_d, def_idx, l_idx, p, dst_rive, face_d)
        prim_deplacement(
            state,
            "INSECTE",
            src_lisiere=l_idx,
            src_p=p,
            dst_ray=src_ray,
            dst_p=p,
            count=1,
        )


# ---------------------------------------------------------------------------
# 4. G7:B — Le Barrage du Capybara (LOI 4.1 : Piège autorisé sous machine)
# ---------------------------------------------------------------------------


@register_tile("G7", "B", hooks=(HOOK_4_1_FURTIVITE, HOOK_5_LAW_QUERY))
def g7_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Loi 4.1 : les binômes en Furtivité peuvent poser un Piège même sous une machine."""
    prim_mod_loi_du_coeur(state, "LOI_PIEGE_SOUS_MACHINE_OU_CIBLE", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return False

    if ctx.get("phase") == "PRE":
        ctx["allow_piege_under_machine"] = True
        ctx["decideur_piege"] = _gov(state, "M")
    return None


# ---------------------------------------------------------------------------
# 5. G7:C — La Loutre géante (LOI 5 : Défenseurs après le 1er valent 2 sur M et H)
# ---------------------------------------------------------------------------


@register_tile("G7", "C", hooks=(HOOK_5_DEFENSE_PARCELLE, HOOK_5_LAW_QUERY))
def g7_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 : sur M et H, chaque Défenseur physique après le premier apporte 2 points."""
    m_seat = state.cfg.seat_of_peuple("M")
    h_seat = state.cfg.seat_of_peuple("H")
    ray = int(ctx["ray"])
    eligible = ray in (m_seat, h_seat)

    prim_mod_loi_du_coeur(state, "LOI_DEFENSEURS_APRES_PREMIER_DOUBLES", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return eligible

    if not eligible:
        return False

    target_p = int(ctx["target_p"])
    local_defs = state.get_parcel_defenseurs(ray, target_p)
    bonus = max(0, local_defs - 1)
    if bonus <= 0:
        return False
    ctx["def_points"] = int(ctx["def_points"]) + bonus
    return True


# ---------------------------------------------------------------------------
# 6. G7:D — Le barrage habité du Capybara (OUVERTURE : Piège sur M/H habité)
# ---------------------------------------------------------------------------


def _habited_trap_candidates_m_h(state: GameState) -> list[tuple[int, int]]:
    rays: list[int] = []
    for p_code in ("M", "H"):
        s = state.cfg.seat_of_peuple(p_code)
        if s is not None and s not in rays:
            rays.append(s)
    cands: list[tuple[int, int]] = []
    for r in rays:
        for p in range(1, state.cfg.p_max + 1):
            if (
                not state.is_route_forestiere(r, p)
                and state.get_parcel_piege(r, p) == PIEGE_AUCUN
                and (state.get_parcel_defenseurs(r, p) + state.get_parcel_insectes(r, p)) >= 1
            ):
                cands.append((r, p))
    return cands


@register_tile("G7", "D", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g7_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez poser 1 Piège sur M ou H sans Piège avec >= 1 Défenseur ou Insecte local."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        cands = _habited_trap_candidates_m_h(state)
        if not cands:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "PIEGE_HABITE_G7D"},
            slot_id="G7",
            profile="D",
            resume_tag="POSE_PIEGE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r_c, p_c = int(choice[0]), int(choice[1])
        if not state.is_route_forestiere(r_c, p_c) and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN:
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=True)


# ---------------------------------------------------------------------------
# 7. G8:A — Le Sillage du Boto (3.2 / OUVERTURE : décalage des frappes non-Siège)
# ---------------------------------------------------------------------------


def _encode_g8_a_shift(state: GameState, ray: int, m_type: int, delta_dir: int) -> None:
    state.mark_used_once_per_turn(G8_A_ACTIVE_SHIFT_LOCK)
    for b in range(3):
        if (ray >> b) & 1:
            state.mark_used_once_per_turn(G8_A_RAY_BIT0 + b)
    if m_type == MACHINE_BULLDOZER:
        state.mark_used_once_per_turn(G8_A_MTYPE_BIT)
    if delta_dir > 0:
        state.mark_used_once_per_turn(G8_A_DIR_HEART_BIT)


def _decode_g8_a_shift(state: GameState) -> tuple[int, int, bool] | None:
    if not state.has_used_once_per_turn(G8_A_ACTIVE_SHIFT_LOCK):
        return None
    ray = 0
    for b in range(3):
        if state.has_used_once_per_turn(G8_A_RAY_BIT0 + b):
            ray |= 1 << b
    m_type = (
        MACHINE_BULLDOZER
        if state.has_used_once_per_turn(G8_A_MTYPE_BIT)
        else MACHINE_ABATTEUSE
    )
    towards_heart = state.has_used_once_per_turn(G8_A_DIR_HEART_BIT)
    return (ray, m_type, towards_heart)


def _g8_a_shift_options(state: GameState) -> list[tuple[int, int, int]]:
    opts: list[tuple[int, int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            _, _, attacked = state.get_machine_turn_stats(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not attacked:
                opts.append((r, mt, -1))
                opts.append((r, mt, 1))
    return opts


def _prompt_or_apply_g8_a(state: GameState, gov: int) -> None:
    if state.has_used_once_per_turn(G8_A_RESOLVED_LOCK):
        return
    state.mark_used_once_per_turn(G8_A_RESOLVED_LOCK)
    opts = _g8_a_shift_options(state)
    if not opts:
        return
    if len(opts) == 1:
        _encode_g8_a_shift(state, opts[0][0], opts[0][1], opts[0][2])
        return
    push_effect_decision(
        state,
        gov,
        opts,
        {"effect_kind": "CIBLAGE_BOTO_G8A"},
        slot_id="G8",
        profile="A",
        resume_tag="SHIFT_STRIKES",
    )


@register_tile(
    "G8",
    "A",
    hooks=(
        HOOK_GARDIEN_OUVERTURE,
        HOOK_3_2_APRES_REVELATION,
        HOOK_5_CIBLAGE_MACHINE,
        HOOK_EFFECT_RESUME,
    ),
)
def g8_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Décale d'1 parcelle non rasée (-1 ou +1) toutes les frappes d'1 machine hors Siège."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        if state.step < STEP_3_2_REVEAL or not state.paravents_ouverts:
            state.mark_used_once_per_turn(G8_A_PREPARED_LOCK)
            return None
        _prompt_or_apply_g8_a(state, gov)
        return None

    if hook == HOOK_3_2_APRES_REVELATION:
        if state.has_used_once_per_turn(G8_A_PREPARED_LOCK):
            _prompt_or_apply_g8_a(state, gov)
        return None

    if hook == HOOK_EFFECT_RESUME:
        r_c, mt_c, d_c = ctx["choice"]
        _encode_g8_a_shift(state, int(r_c), int(mt_c), int(d_c))
        return None

    if hook == HOOK_5_CIBLAGE_MACHINE:
        if bool(ctx.get("is_ratissage")):
            return False
        decoded = _decode_g8_a_shift(state)
        if decoded is None:
            return False
        sel_r, sel_mt, towards_heart = decoded
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        if ray != sel_r or m_type != sel_mt:
            return False
        tid = str(ctx["tactique"])
        if len(tid) != 2 or tid[0] != "T" or not ("1" <= tid[1] <= "6"):
            return False
        spec = TACTIQUES_SPEC[int(tid[1])]
        pos = int(ctx["pos"])
        new_targets: list[tuple[str, int]] = []
        for c_type in spec.cibles:
            base_p: int | None = None
            if c_type == "SUR_PLACE":
                base_p = pos
            elif c_type == "DEVANT":
                base_p = state.next_non_razed_towards_heart(ray, pos)
            if base_p is None:
                continue
            shifted_p = (
                state.next_non_razed_towards_heart(ray, base_p)
                if towards_heart
                else state.next_non_razed_towards_border(ray, base_p)
            )
            if shifted_p is not None and not state.is_route_forestiere(ray, shifted_p):
                new_targets.append((c_type, shifted_p))
        ctx["targets"] = new_targets
        return True

    return None


# ---------------------------------------------------------------------------
# 8. G8:B — Le Sillage du Boto (LOI 5 : Bulldozer avant Abatteuse sur 1 rayon)
# ---------------------------------------------------------------------------


def _encode_g8_b_ray(state: GameState, ray: int) -> None:
    state.mark_used_once_per_turn(G8_B_ACTIVE_INV_LOCK)
    for b in range(3):
        if (ray >> b) & 1:
            state.mark_used_once_per_turn(G8_B_RAY_BIT0 + b)


def _decode_g8_b_ray(state: GameState) -> int | None:
    if not state.has_used_once_per_turn(G8_B_ACTIVE_INV_LOCK):
        return None
    ray = 0
    for b in range(3):
        if state.has_used_once_per_turn(G8_B_RAY_BIT0 + b):
            ray |= 1 << b
    return ray


@register_tile(
    "G8",
    "B",
    hooks=(HOOK_5_DEBUT, HOOK_5_ORDRE_RAYON, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g8_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Loi 5 : sur 1 rayon au choix/tour où Abatteuse et Bulldozer sont actifs, Bulldozer d'abord."""
    gov = _gov(state, "M")

    if hook == HOOK_5_DEBUT:
        if state.has_slot_used_once_per_turn("G8"):
            return None
        dual_rays = [
            r
            for r in range(state.cfg.n_players)
            if _is_machine_active_turn(state, r, MACHINE_ABATTEUSE)
            and _is_machine_active_turn(state, r, MACHINE_BULLDOZER)
        ]
        if not dual_rays:
            return None
        push_effect_decision(
            state,
            gov,
            ("PASSER", *dual_rays),
            {"effect_kind": "INVERSION_BOTO_G8B"},
            slot_id="G8",
            profile="B",
            resume_tag="INVERT_RAY",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return None
        state.mark_slot_used_once_per_turn("G8")
        _encode_g8_b_ray(state, int(choice))
        prim_mod_loi_du_coeur(state, "LOI_INVERSION_ETAPE_5_1_ET_5_2", active=True)
        return None

    inv_ray = _decode_g8_b_ray(state)
    active_on_ray = inv_ray is not None and inv_ray == int(ctx["ray"])
    if active_on_ray:
        prim_mod_loi_du_coeur(state, "LOI_INVERSION_ETAPE_5_1_ET_5_2", active=True)

    if hook == HOOK_5_LAW_QUERY:
        return active_on_ray

    if hook == HOOK_5_ORDRE_RAYON:
        if active_on_ray:
            ctx["bulldozer_first"] = True
        return active_on_ray

    return None


# ---------------------------------------------------------------------------
# 9. G9:A — Le Guet du Caïman Noir (DOUBLE_FACE : +1 puis +2 cartes Sabotage)
# ---------------------------------------------------------------------------


@register_tile("G9", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
def g9_a_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
    """Face 1 : +1 Sabotage permanent (flip Face 2 en 5.3 si pari gagné). Face 2 : +2 Sabotages permanents."""
    face = int(ctx["face"])

    if face == 1:
        prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=True)
        return

    # Branche Face 2 strictement autonome
    prim_creation_entite(state, "SABOTAGE", count=2, light_trigger=True)


# ---------------------------------------------------------------------------
# 10. G9:B — Le Guet du Caïman Noir (LOI 4.1 Sabotage actif + Face 2 LOI 3.2)
# ---------------------------------------------------------------------------


def _machines_with_red_on_r_h(state: GameState) -> list[tuple[int, int]]:
    rays: list[int] = []
    for p_code in ("R", "H"):
        s = state.cfg.seat_of_peuple(p_code)
        if s is not None and s not in rays:
            rays.append(s)
    out: list[tuple[int, int]] = []
    for r in rays:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                rouges, _ = state.get_machine_tokens(r, mt)
                if rouges >= 1:
                    out.append((r, mt))
    return out


def _resolve_g9_b_sabotage_step(state: GameState, gov: int, remaining: int) -> None:
    while remaining > 0:
        cands = _machines_with_red_on_r_h(state)
        if not cands:
            break
        if len(cands) == 1:
            prim_mod_puissance(state, cands[0][0], cands[0][1], delta_rouges=-1)
            remaining -= 1
            continue
        push_effect_decision(
            state,
            gov,
            cands,
            {"effect_kind": "REMOVE_RED_R_H", "remaining": remaining},
            slot_id="G9",
            profile="B",
            resume_tag="REM_RED_3_2",
            resume_payload=(remaining,),
        )
        return
    state.light_trigger(3)


@register_tile(
    "G9",
    "B",
    hooks=(
        HOOK_GARDIEN_OUVERTURE,
        HOOK_3_2_REVELATION,
        HOOK_3_2_APRES_REVELATION,
        HOOK_4_1_FURTIVITE,
        HOOK_5_LAW_QUERY,
        HOOK_EFFECT_RESUME,
    ),
)
def g9_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 : Sabotage 4.1 même actif/Siège. Face 2 : idem + en 3.2 chaque Sabotage -> case 3 & -1 rouge R/H."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        return None

    face = _gardien_face_on_track(state, 9)
    if face not in (1, 2):
        return False

    if hook == HOOK_5_LAW_QUERY:
        prim_mod_loi_du_coeur(state, "LOI_SABOTAGE_ACTIF_ET_REVELATION", active=True)
        return False

    if hook == HOOK_4_1_FURTIVITE:
        if face == 1:
            prim_mod_loi_du_coeur(state, "LOI_SABOTAGE_ACTIF_ET_REVELATION", active=True)
            if ctx.get("phase") == "PRE":
                ctx["allow_sabotage_active"] = True
            return None
        # Branche Face 2 strictement autonome
        prim_mod_loi_du_coeur(state, "LOI_SABOTAGE_ACTIF_ET_REVELATION", active=True)
        if ctx.get("phase") == "PRE":
            ctx["allow_sabotage_active"] = True
        return None

    if hook == HOOK_3_2_REVELATION:
        if face == 2:
            state.mark_used_once_per_turn(G9_B_F2_AT_3_2_START_LOCK)
        return None

    if hook == HOOK_3_2_APRES_REVELATION:
        if face != 2 or not state.has_used_once_per_turn(G9_B_F2_AT_3_2_START_LOCK):
            return None
        sab_revealed = sum(
            1
            for s in range(state.cfg.n_players)
            if state.get_player_hand(s)[0] == CARD_SABOTAGE
        )
        if sab_revealed <= 0:
            return None
        prim_mod_loi_du_coeur(state, "LOI_SABOTAGE_ACTIF_ET_REVELATION", active=True)
        _resolve_g9_b_sabotage_step(state, gov, sab_revealed)
        return None

    if hook == HOOK_EFFECT_RESUME:
        remaining = int(ctx["payload"][0])
        r_m, mt_m = ctx["choice"]
        prim_mod_puissance(state, int(r_m), int(mt_m), delta_rouges=-1)
        _resolve_g9_b_sabotage_step(state, gov, remaining - 1)
        return None

    return None
