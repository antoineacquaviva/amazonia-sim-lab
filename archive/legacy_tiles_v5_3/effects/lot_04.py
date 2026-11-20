"""Palier 3 — Lot 04 : Gardiens Reptiles & Oiseaux G10:B..G12:C (10 profils)."""

from __future__ import annotations

from typing import Any

from engine.primitives import (
    HOOK_2_1_PORTEE_DEF1,
    HOOK_3_1_CONSTRUCTION,
    HOOK_5_3_PRE_RETRAIT,
    HOOK_5_APRES_PARADE_PIEGE,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_LAW_QUERY,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    _record_phys_ops,
    prim_creation_entite,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    prim_mod_seuil,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
    register_tile,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    PFLAG_AUTO_PARADE_ONCE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    TRACK_LEN,
    GameState,
    is_reve_code,
)

__all__ = (
    "DOUBLE_FACE_UPGRADE_GARDIENS",
    "LOT_04_PROFILES",
    "PFLAG_TRAP_PARRIED_ABATTEUSE",
    "PFLAG_TRAP_PARRIED_BULLDOZER",
    "g10_b_handler",
    "g10_c_handler",
    "g10_d_handler",
    "g11_a_handler",
    "g11_b_handler",
    "g11_c_handler",
    "g11_d_handler",
    "g12_a_handler",
    "g12_b_handler",
    "g12_c_handler",
)

LOT_04_PROFILES: tuple[tuple[str, str], ...] = (
    ("G10", "B"),
    ("G10", "C"),
    ("G10", "D"),
    ("G11", "A"),
    ("G11", "B"),
    ("G11", "C"),
    ("G11", "D"),
    ("G12", "A"),
    ("G12", "B"),
    ("G12", "C"),
)

# Gardiens à cycle DOUBLE_FACE_UPGRADE (exclut explicitement G14:C qui est DOUBLE_FACE_CYCLE)
DOUBLE_FACE_UPGRADE_GARDIENS: tuple[tuple[str, str], ...] = (
    ("G1", "A"),
    ("G1", "B"),
    ("G2", "A"),
    ("G2", "B"),
    ("G5", "A"),
    ("G5", "B"),
    ("G9", "A"),
    ("G9", "B"),
    ("G11", "A"),
    ("G11", "B"),
)

# Bits libres de TRANS_PARCEL_FLAGS (remis à 0 automatiquement en 6.2) pour tracer les couples Piège-machine
PFLAG_TRAP_PARRIED_ABATTEUSE: int = 1 << 3
PFLAG_TRAP_PARRIED_BULLDOZER: int = 1 << 4


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _gardien_face_on_track(state: GameState, g_num: int) -> tuple[int, int]:
    """Retourne (case_1_6, face_1_2) si le Gardien g_num est en jeu sur la piste, sinon (0, 0)."""
    for c in range(1, TRACK_LEN + 1):
        gn, face = state.get_gardien_at_case(c)
        if gn == g_num:
            return c, face
    return 0, 0


def _find_oh_lisiere(state: GameState) -> int | None:
    """Retourne l'indice de la lisière Oiseaux–Humains si O et H sont adjacents à table."""
    o_seat = state.cfg.seat_of_peuple("O")
    h_seat = state.cfg.seat_of_peuple("H")
    if o_seat is None or h_seat is None:
        return None
    n = state.cfg.n_players
    if (o_seat + 1) % n == h_seat:
        return o_seat
    if (h_seat + 1) % n == o_seat:
        return h_seat
    return None


def _leftmost_reve_rank(state: GameState) -> int | None:
    """Retourne l'indice 0..5 du Rêve le plus à gauche sur la Piste des Tactiques."""
    for r_idx in range(TRACK_LEN):
        if is_reve_code(state.get_tactique_at_rank(r_idx)):
            return r_idx
    return None


# ---------------------------------------------------------------------------
# G10:B — Gardien du Puits (Reptiles) : SIMPLE_CONTINU | LOI 5.3
# ---------------------------------------------------------------------------


def _g10_b_pending_pairs(state: GameState) -> list[tuple[int, int, int]]:
    pairs: list[tuple[int, int, int]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if state.get_parcel_piege(r, p) != PIEGE_DECLENCHE:
                continue
            for mt, mask in (
                (MACHINE_ABATTEUSE, PFLAG_TRAP_PARRIED_ABATTEUSE),
                (MACHINE_BULLDOZER, PFLAG_TRAP_PARRIED_BULLDOZER),
            ):
                if not state.has_parcel_flag_turn(r, p, mask):
                    continue
                pos, st, _ = state.get_machine_pos_status(r, mt)
                rouges, _ = state.get_machine_tokens(r, mt)
                if st != MACHINE_STATUS_RETIRED and pos > 0 and rouges >= 1:
                    pairs.append((r, p, mt))
    return pairs


def _g10_b_step_queue(state: GameState) -> None:
    pairs = _g10_b_pending_pairs(state)
    if not pairs:
        return
    r, p, mt = pairs[0]
    gov = _gov(state, "R")
    opts = (
        ("RETIRER_ROUGE", r, mt, p),
        ("SURCHAUFFE_BLEU", r, mt, p),
    )
    push_effect_decision(
        state,
        gov,
        opts,
        {"effect_kind": "PUITS_PIEGE_PUISSANCE_5_3", "ray": r, "p": p, "m_type": mt},
        slot_id="G10",
        profile="B",
        resume_tag="PUITS_5_3",
        resume_payload=(r, p, mt),
    )


@register_tile(
    "G10",
    "B",
    hooks=(
        HOOK_5_APRES_PARADE_PIEGE,
        HOOK_5_3_PRE_RETRAIT,
        HOOK_5_LAW_QUERY,
        HOOK_EFFECT_RESUME,
    ),
)
def g10_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi 5.3 : chaque Piège déclenché retire 1 Rouge (ou retourne 1 Rouge en Bleu) par machine parée."""
    if hook == HOOK_5_APRES_PARADE_PIEGE:
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        target_p = int(ctx["target_p"])
        mask = (
            PFLAG_TRAP_PARRIED_ABATTEUSE
            if m_type == MACHINE_ABATTEUSE
            else PFLAG_TRAP_PARRIED_BULLDOZER
        )
        state.set_parcel_flag_turn(ray, target_p, mask, True)
        return None

    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        return state.get_parcel_piege(ray, target_p) in (PIEGE_ACTIF, PIEGE_DECLENCHE)

    if hook == HOOK_5_3_PRE_RETRAIT:
        prim_mod_loi_du_coeur(state, "LOI_PUITS_PIEGE_PUISSANCE_5_3")
        _g10_b_step_queue(state)
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        r, p, mt = ctx["payload"]
        r_i, p_i, mt_i = int(r), int(p), int(mt)
        mask = (
            PFLAG_TRAP_PARRIED_ABATTEUSE
            if mt_i == MACHINE_ABATTEUSE
            else PFLAG_TRAP_PARRIED_BULLDOZER
        )
        state.set_parcel_flag_turn(r_i, p_i, mask, False)
        if isinstance(choice, tuple) and len(choice) == 4:
            act = str(choice[0])
            if act == "RETIRER_ROUGE":
                prim_mod_puissance(state, r_i, mt_i, delta_rouges=-1)
            elif act == "SURCHAUFFE_BLEU":
                prim_mod_puissance(state, r_i, mt_i, flip_rouge_to_bleu=1)
        _g10_b_step_queue(state)
    return None


# ---------------------------------------------------------------------------
# G10:C — Gardien du Puits (Reptiles) : SIMPLE_CONTINU | OUVERTURE (CASE 6)
# ---------------------------------------------------------------------------


@register_tile(
    "G10",
    "C",
    hooks=(HOOK_3_1_CONSTRUCTION, HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g10_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Câblage obligatoire sur 6 : défausse 1 Insecte de Forêt -> +1 carte Sabotage (allume 3)."""
    if hook == HOOK_3_1_CONSTRUCTION:
        if ctx.get("slot_id") == "G10":
            ctx["allowed_cases"] = (6,)
        return None

    if hook == HOOK_GARDIEN_OUVERTURE:
        if int(ctx.get("case", 0)) != 6:
            return None
        cands: list[tuple[int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    cands.append((r, p))
        if not cands:
            return None
        gov = _gov(state, "R")
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "CONVERSION_INSECTE_SABOTAGE_G10C"},
            slot_id="G10",
            profile="C",
            resume_tag="CONV_SABOTAGE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice != "PASSER" and isinstance(choice, tuple):
            r_c, p_c = int(choice[0]), int(choice[1])
            cur_ins = state.get_parcel_insectes(r_c, p_c)
            if cur_ins >= 1:
                state.set_parcel_insectes(r_c, p_c, cur_ins - 1)
                _record_phys_ops(state, 1)
                prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=True)
    return None


# ---------------------------------------------------------------------------
# G10:D — Gardien du Puits (Reptiles) : SIMPLE_CONTINU | LOI APRÈS PARADE PIÈGE
# ---------------------------------------------------------------------------


@register_tile(
    "G10",
    "D",
    hooks=(HOOK_5_APRES_PARADE_PIEGE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g10_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi : 1x/tour après Parade par Piège sur R ou E, crée 1 Insecte sur une autre parcelle piégée de R/E."""
    r_seat = state.cfg.seat_of_peuple("R")
    e_seat = state.cfg.seat_of_peuple("E")
    re_rays = tuple(s for s in (r_seat, e_seat) if s is not None)

    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        return (
            not state.has_slot_used_once_per_turn("G10")
            and ray in re_rays
            and state.get_parcel_piege(ray, target_p) in (PIEGE_ACTIF, PIEGE_DECLENCHE)
        )

    if hook == HOOK_5_APRES_PARADE_PIEGE:
        if state.has_slot_used_once_per_turn("G10"):
            return None
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        if ray not in re_rays:
            return None
        cands: list[tuple[int, int]] = []
        for r in re_rays:
            for p in range(1, state.cfg.p_max + 1):
                if (r, p) == (ray, target_p) or state.is_route_forestiere(r, p):
                    continue
                if state.get_parcel_piege(r, p) in (PIEGE_ACTIF, PIEGE_DECLENCHE):
                    cands.append((r, p))
        if not cands:
            return None
        prim_mod_loi_du_coeur(state, "LOI_EMBUSCADE_CREE_SENTINELLE")
        gov = _gov(state, "R")
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "SENTINELLE_EMBUSCADE_G10D", "src_ray": ray, "src_p": target_p},
            slot_id="G10",
            profile="D",
            resume_tag="CREATE_SENTINELLE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice != "PASSER" and isinstance(choice, tuple):
            r_dst, p_dst = int(choice[0]), int(choice[1])
            state.mark_slot_used_once_per_turn("G10")
            prim_creation_entite(state, "INSECTE", ray=r_dst, p=p_dst, count=1, light_trigger=True)
    return None


# ---------------------------------------------------------------------------
# G11:A — Gardien de la Harpie (Oiseaux) : DOUBLE_FACE_UPGRADE | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile(
    "G11",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g11_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Face 1 : -1 Seuil sur une parcelle (-2 si >= 2 Défenseurs). Face 2 : pare auto 1 attaque si >= 2 Déf."""
    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        return state.has_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE)

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx["face"])
        case_num = int(ctx["case"])
        gov = _gov(state, "O")
        if face == 1:
            cands_f1: list[tuple[int, int]] = []
            for r in range(state.cfg.n_players):
                for p in range(1, state.cfg.p_max + 1):
                    if not state.is_route_forestiere(r, p):
                        cands_f1.append((r, p))
            if not cands_f1:
                return None
            if len(cands_f1) == 1:
                r0, p0 = cands_f1[0]
                delta = -2 if state.get_parcel_defenseurs(r0, p0) >= 2 else -1
                prim_mod_seuil(state, delta, ray=r0, p=p0)
                return None
            push_effect_decision(
                state,
                gov,
                cands_f1,
                {"effect_kind": "HARPIE_MOD_SEUIL_F1", "face": 1},
                slot_id="G11",
                profile="A",
                resume_tag="F1_SEUIL",
                resume_payload=(case_num,),
            )
            return None

        # Face 2 autonome : pare automatiquement 1 attaque sur une parcelle contenant >= 2 Défenseurs
        cands_f2 = [
            (r, p)
            for r in range(state.cfg.n_players)
            for p in range(1, state.cfg.p_max + 1)
            if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 2
        ]
        if not cands_f2:
            cands_f2 = [
                (r, p)
                for r in range(state.cfg.n_players)
                for p in range(1, state.cfg.p_max + 1)
                if not state.is_route_forestiere(r, p)
            ]
        if not cands_f2:
            return None
        if len(cands_f2) == 1:
            r0, p0 = cands_f2[0]
            state.set_parcel_flag_turn(r0, p0, PFLAG_AUTO_PARADE_ONCE, True)
            _record_phys_ops(state, 1)
            return None
        push_effect_decision(
            state,
            gov,
            cands_f2,
            {"effect_kind": "HARPIE_AUTO_PARADE_F2", "face": 2},
            slot_id="G11",
            profile="A",
            resume_tag="F2_AUTO_PARADE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        tag = ctx["resume_tag"]
        r_c, p_c = ctx["choice"]
        r_i, p_i = int(r_c), int(p_c)
        if tag == "F1_SEUIL":
            (case_num,) = ctx["payload"]
            delta = -2 if state.get_parcel_defenseurs(r_i, p_i) >= 2 else -1
            prim_mod_seuil(state, delta, ray=r_i, p=p_i)
        elif tag == "F2_AUTO_PARADE":
            state.set_parcel_flag_turn(r_i, p_i, PFLAG_AUTO_PARADE_ONCE, True)
            _record_phys_ops(state, 1)
    return None


# ---------------------------------------------------------------------------
# G11:B — Gardien de la Harpie (Oiseaux) : DOUBLE_FACE_UPGRADE | LOI 5
# ---------------------------------------------------------------------------


def _g11_b_remote_support_for_parcel(state: GameState, ray: int, target_p: int, face: int) -> int:
    if state.is_route_forestiere(ray, target_p):
        return 0
    n = state.cfg.n_players
    l_right = ray
    l_left = (ray - 1) % n
    adj_lisieres = (l_right,) if l_right == l_left else (l_right, l_left)

    bonus = 0
    if face == 1:
        # Face 1 : tout Défenseur isolé sur une case Furtivité ajoute +1 aux 2 parcelles en face
        for l_adj in adj_lisieres:
            if state.get_furtivite_total_defs(l_adj, target_p) == 1:
                bonus += 1
    else:
        # Face 2 (autonome) : Défenseur isolé en Furtivité (+1 en face) + bâtisseurs restés en lisière (+1 sur p=1)
        for l_adj in adj_lisieres:
            if state.get_furtivite_total_defs(l_adj, target_p) == 1:
                bonus += 1
            if target_p == 1:
                for slot_idx in (2 * l_adj, 2 * l_adj + 1):
                    _, nb_builders = state.get_lisiere_tile_state(slot_idx)
                    bonus += nb_builders
    return bonus


@register_tile(
    "G11",
    "B",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_DEFENSE_PARCELLE, HOOK_5_LAW_QUERY),
)
def g11_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Face 1/2 (Loi 5) : soutien en Défense depuis Furtivité isolée (et bâtisseurs en lisière sur p=1 en Face 2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        return None

    case_num, face = _gardien_face_on_track(state, 11)
    if case_num == 0:
        return False if hook == HOOK_5_LAW_QUERY else None

    ray = int(ctx["ray"])
    target_p = int(ctx["target_p"])
    bonus = _g11_b_remote_support_for_parcel(state, ray, target_p, face)

    if hook == HOOK_5_LAW_QUERY:
        return bonus > 0

    if hook == HOOK_5_DEFENSE_PARCELLE and bonus > 0:
        prim_mod_loi_du_coeur(state, "LOI_SOUTIEN_LISIERE_DEFENSE")
        ctx["remote_support"] = int(ctx["remote_support"]) + bonus
    return None


# ---------------------------------------------------------------------------
# G11:C — Gardien de la Harpie (Oiseaux) : SIMPLE_CONTINU | LOI 2.1
# ---------------------------------------------------------------------------


@register_tile("G11", "C", hooks=(HOOK_2_1_PORTEE_DEF1,))
def g11_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi 2.1 : tout Peuple peut poser son 1er Défenseur sur une case Furtivité O–H ayant >= 1 Insecte."""
    if hook == HOOK_2_1_PORTEE_DEF1:
        l_oh = _find_oh_lisiere(state)
        if l_oh is None:
            return None
        extras: list[tuple[Any, ...]] = list(ctx.get("extra_targets", ()))
        added = False
        for p in range(1, state.cfg.p_max + 1):
            if state.get_furtivite_insectes(l_oh, p) < 1:
                continue
            if state.get_furtivite_total_defs(l_oh, p) >= 2:
                continue
            for rive in (0, 1):
                t_ray = state.lisiere_ray_for_rive(l_oh, rive)
                if not state.is_route_forestiere(t_ray, p):
                    cand = ("FURTIVITE", l_oh, p, rive)
                    if cand not in extras:
                        extras.append(cand)
                        added = True
        if added:
            prim_mod_loi_du_coeur(state, "LOI_DEFENSEUR_1_CASE_INSECTE")
            ctx["extra_targets"] = extras
    return None


# ---------------------------------------------------------------------------
# G11:D — Gardien de la Harpie (Oiseaux) : SIMPLE_CONTINU | LOI 5
# ---------------------------------------------------------------------------


def _g11_d_remote_support_for_parcel(state: GameState, ray: int, target_p: int) -> int:
    o_seat = state.cfg.seat_of_peuple("O")
    h_seat = state.cfg.seat_of_peuple("H")
    if ray not in (o_seat, h_seat) or state.is_route_forestiere(ray, target_p):
        return 0
    if state.get_parcel_piege(ray, target_p) not in (PIEGE_ACTIF, PIEGE_DECLENCHE):
        return 0
    n = state.cfg.n_players
    l_right = ray
    l_left = (ray - 1) % n
    adj_lisieres = (l_right,) if l_right == l_left else (l_right, l_left)
    bonus = 0
    for l_adj in adj_lisieres:
        if state.get_furtivite_total_defs(l_adj, target_p) >= 1:
            bonus += 1
    return bonus


@register_tile("G11", "D", hooks=(HOOK_5_DEFENSE_PARCELLE, HOOK_5_LAW_QUERY))
def g11_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi 5 : chaque case Furtivité avec >= 1 Défenseur fournit 1 Défense aux parcelles piégées O/H en face."""
    ray = int(ctx["ray"])
    target_p = int(ctx["target_p"])
    bonus = _g11_d_remote_support_for_parcel(state, ray, target_p)

    if hook == HOOK_5_LAW_QUERY:
        return bonus > 0

    if hook == HOOK_5_DEFENSE_PARCELLE and bonus > 0:
        prim_mod_loi_du_coeur(state, "LOI_FURTIVITE_ARME_PIEGES")
        ctx["remote_support"] = int(ctx["remote_support"]) + bonus
    return None


# ---------------------------------------------------------------------------
# G12:A — Gardien du Vent (Oiseaux) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile("G12", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g12_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Échange une tuile Rêve de la Piste des Tactiques avec sa voisine de gauche (r -> r-1)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        cands = [
            r_idx
            for r_idx in range(1, TRACK_LEN)
            if is_reve_code(state.get_tactique_at_rank(r_idx))
        ]
        if not cands:
            return None
        if len(cands) == 1:
            prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cands[0])
            return None
        gov = _gov(state, "O")
        push_effect_decision(
            state,
            gov,
            cands,
            {"effect_kind": "ADVANCE_REVE_G12A"},
            slot_id="G12",
            profile="A",
            resume_tag="ADV_REVE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        r_idx = int(ctx["choice"])
        if 1 <= r_idx < TRACK_LEN and is_reve_code(state.get_tactique_at_rank(r_idx)):
            prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=r_idx)
    return None


# ---------------------------------------------------------------------------
# G12:B — Gardien du Vent (Oiseaux) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


def _is_upgrade_gardien_in_game(state: GameState, g_num: int) -> bool:
    slot_id = f"G{g_num}"
    prof = state.cfg.profile_for_slot(slot_id)
    if prof is not None:
        return (slot_id, prof) in DOUBLE_FACE_UPGRADE_GARDIENS
    return g_num in (1, 2, 5, 9, 11)


@register_tile("G12", "B", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g12_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Retourne gratuitement un autre Gardien évolutif en jeu sur sa Face 2 (ou ouvre un autre Gardien disponible)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        my_case = int(ctx.get("case", 0))
        opts: list[tuple[str, int]] = []
        for c in range(1, TRACK_LEN + 1):
            if c == my_case:
                continue
            g_num, face = state.get_gardien_at_case(c)
            if g_num <= 0 or g_num == 12:
                continue
            if face == 1 and _is_upgrade_gardien_in_game(state, g_num):
                opts.append(("FLIP_FACE2", c))
            if state.count_gardien_pari_defenders_at_case(c) >= 1:
                opts.append(("OPEN_SLOT", c))
        if not opts:
            return None
        if len(opts) == 1:
            act, target_c = opts[0]
            if act == "FLIP_FACE2":
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=target_c, new_face=2
                )
            else:
                prim_partage_info_etat_gardien(
                    state, "MARK_GARDIEN_OPENED", case_1_6=target_c
                )
            return None
        gov = _gov(state, "O")
        push_effect_decision(
            state,
            gov,
            opts,
            {"effect_kind": "VENT_RELAIS_GARDIEN_G12B"},
            slot_id="G12",
            profile="B",
            resume_tag="RELAIS_GARDIEN",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        act, target_c = ctx["choice"]
        c_i = int(target_c)
        if str(act) == "FLIP_FACE2":
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=c_i, new_face=2
            )
        elif str(act) == "OPEN_SLOT":
            prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=c_i)
    return None


# ---------------------------------------------------------------------------
# G12:C — Gardien du Vent (Oiseaux) : SIMPLE_CONTINU | OUVERTURE (CASE 2)
# ---------------------------------------------------------------------------


@register_tile(
    "G12",
    "C",
    hooks=(HOOK_3_1_CONSTRUCTION, HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g12_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Câblage obligatoire sur 2 : retire 1 Piège non déclenché ce tour-ci -> avance d'1 rang le Rêve le plus à gauche."""
    if hook == HOOK_3_1_CONSTRUCTION:
        if ctx.get("slot_id") == "G12":
            ctx["allowed_cases"] = (2,)
        return None

    if hook == HOOK_GARDIEN_OUVERTURE:
        if int(ctx.get("case", 0)) != 2:
            return None
        left_reve = _leftmost_reve_rank(state)
        if left_reve is None or left_reve <= 0:
            return None
        cands: list[tuple[int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                    cands.append((r, p))
        if not cands:
            return None
        gov = _gov(state, "O")
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "CONVERSION_PIEGE_REVE_G12C", "reve_rank": left_reve},
            slot_id="G12",
            profile="C",
            resume_tag="CONV_PIEGE_REVE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice != "PASSER" and isinstance(choice, tuple):
            r_c, p_c = int(choice[0]), int(choice[1])
            left_reve = _leftmost_reve_rank(state)
            if (
                state.get_parcel_piege(r_c, p_c) == PIEGE_ACTIF
                and left_reve is not None
                and left_reve > 0
            ):
                state.set_parcel_piege(r_c, p_c, PIEGE_AUCUN)
                _record_phys_ops(state, 1)
                prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=left_reve)
    return None
