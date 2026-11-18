"""Palier 3 — Lot 06 : Rêves R1:A..R4:D (11 profils, 100 % stateless stdlib PyPy 3.11)."""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_1_CONSTRUCTION,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_6_1_REDUCTION_VOLONTAIRE,
    HOOK_EFFECT_RESUME,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_apprentissage,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
)
from engine.state import (
    CARD_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RETIRED,
    PIEGE_AUCUN,
    TILE_R_BASE,
    TRACK_LEN,
    GameState,
    is_tactique_code,
)

__all__ = (
    "LOT_06_PROFILES",
    "PFLAG_ALL_PARRIED_ABATTEUSE",
    "PFLAG_ALL_PARRIED_BULLDOZER",
    "R2_A_OPEN_BITS",
    "r1_a_handler",
    "r1_b_handler",
    "r1_c_handler",
    "r2_a_handler",
    "r2_b_handler",
    "r3_a_handler",
    "r3_b_handler",
    "r4_a_handler",
    "r4_b_handler",
    "r4_c_handler",
    "r4_d_handler",
)

LOT_06_PROFILES: tuple[tuple[str, str], ...] = (
    ("R1", "A"),
    ("R1", "B"),
    ("R1", "C"),
    ("R2", "A"),
    ("R2", "B"),
    ("R3", "A"),
    ("R3", "B"),
    ("R4", "A"),
    ("R4", "B"),
    ("R4", "C"),
    ("R4", "D"),
)

# Compteur unaire monotone des ouvertures de R2:A en 3.2 (plage libre 55..60 de TRANS_ONCE_PER_TURN, RAZ en 6.2)
R2_A_OPEN_BITS: tuple[int, ...] = (55, 56, 57, 58, 59, 60)

# Bits libres de TRANS_PARCEL_FLAGS sur (ray, 1) (RAZ en 6.2) pour mémoriser all_parried par machine (R2:B)
PFLAG_ALL_PARRIED_ABATTEUSE: int = 1 << 5
PFLAG_ALL_PARRIED_BULLDOZER: int = 1 << 6

DEC_RETRAIT_APPRENTISSAGE_6_1_NAME: str = "RETRAIT_APPRENTISSAGE_6_1"


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


# ---------------------------------------------------------------------------
# 1. R1:A — Le Tambour des Deux Mondes (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


def _adjacent_tactique_pairs(state: GameState) -> list[tuple[int, int]]:
    pairs: list[tuple[int, int]] = []
    for idx in range(TRACK_LEN - 1):
        c_left = state.get_tactique_at_rank(idx)
        c_right = state.get_tactique_at_rank(idx + 1)
        if is_tactique_code(c_left) and is_tactique_code(c_right):
            pairs.append((idx, idx + 1))
    return pairs


@register_tile("R1", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r1_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, avant l'avancée de ce Rêve, échange deux tuiles Tactique adjacentes."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        pairs = _adjacent_tactique_pairs(state)
        if not pairs:
            return
        if len(pairs) == 1:
            ra, rb = pairs[0]
            prim_permutation_piste(state, "SWAP_RANKS", rank_a=ra, rank_b=rb)
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(pairs),
            {"effect_kind": "TAMBOUR_SWAP_TACTIQUES"},
            slot_id="R1",
            profile="A",
            resume_tag="SWAP_TACT",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        ra, rb = ctx["choice"]
        prim_permutation_piste(state, "SWAP_RANKS", rank_a=int(ra), rank_b=int(rb))


# ---------------------------------------------------------------------------
# 2. R1:B — Le Tambour des Deux Mondes (Humains) : SIMPLE_CONTINU | LOI 3.2
# ---------------------------------------------------------------------------


@register_tile("R1", "B", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r1_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Loi 3.2 : à son ouverture en 3.2, R1 avance de jusqu'à 2 rangs vers la gauche (plafonné au Rang 1)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        prim_mod_loi_du_coeur(state, "LOI_REVE_DOUBLE_AVANCEE")
        cur_pos = state.find_tactique_rank(TILE_R_BASE + 1)
        # STEP_3_2_FINISH_REVE effectuera déjà +1 avancée vers la gauche (plafonnée au Rang 1)
        if cur_pos is None or cur_pos <= 1:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            (1, 2),
            {"effect_kind": "REVE_DOUBLE_AVANCEE", "current_rank": cur_pos + 1},
            slot_id="R1",
            profile="B",
            resume_tag="ADV_R1_B",
        )
        return

    if hook == HOOK_EFFECT_RESUME and int(ctx["choice"]) == 2:
        cur_pos = state.find_tactique_rank(TILE_R_BASE + 1)
        if cur_pos is not None and cur_pos > 0:
            prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cur_pos)


# ---------------------------------------------------------------------------
# 3. R1:C — La Part rendue à la forêt (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


@register_tile("R1", "C", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r1_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À chaque ouverture en 3.2, peut renvoyer 1 Gardien en lisière (Face 1, non utilisé) pour avancer jusqu'à 2 rangs."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        cur_pos = state.find_tactique_rank(TILE_R_BASE + 1)
        if cur_pos is None or cur_pos <= 0:
            return
        g_cases = [c for c in range(1, TRACK_LEN + 1) if state.get_gardien_at_case(c)[0] > 0]
        if not g_cases:
            return
        opts: list[Any] = ["PASSER"]
        for c in g_cases:
            if cur_pos >= 2:
                opts.append((c, 2))
            opts.append((c, 1))
        push_effect_decision(
            state,
            _gov(state, "H"),
            tuple(opts),
            {"effect_kind": "OFFRANDE_GARDIEN_AVANCEE_REVE", "current_rank": cur_pos + 1},
            slot_id="R1",
            profile="C",
            resume_tag="OFFRANDE_R1_C",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        case_g, total_steps = int(choice[0]), int(choice[1])
        prim_partage_info_etat_gardien(state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=case_g)
        if total_steps >= 2:
            cur_pos = state.find_tactique_rank(TILE_R_BASE + 1)
            if cur_pos is not None and cur_pos > 0:
                prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cur_pos)


# ---------------------------------------------------------------------------
# 4. R2:A — Le Voile de l'Oubli (Entités Magiques) : SIMPLE_CONTINU | 3.2 -> 6.1
# ---------------------------------------------------------------------------


def _r2_a_prompt_next(state: GameState, remaining: int) -> None:
    if remaining <= 0:
        return
    ranks_pos = [
        idx
        for idx in range(TRACK_LEN)
        if is_tactique_code(state.get_tactique_at_rank(idx))
        and state.get_apprentissage_at_rank(idx) > 0
    ]
    if not ranks_pos:
        return
    push_effect_decision(
        state,
        _gov(state, "E"),
        ("PASSER", *ranks_pos),
        {"effect_kind": "VOILE_OUBLI_RETRAIT_6_1", "remaining": remaining, "tour": state.tour},
        slot_id="R2",
        profile="A",
        resume_tag="VOILE_6_1",
        resume_payload=(remaining,),
        decision_type=DEC_RETRAIT_APPRENTISSAGE_6_1_NAME,
    )


@register_tile(
    "R2",
    "A",
    hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_6_1_REDUCTION_VOLONTAIRE, HOOK_EFFECT_RESUME),
)
def r2_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """En 6.1 ce tour-ci (avant les Insectes Bug), retire jusqu'à 2 jetons Apprentissage sur la Piste des Tactiques."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        for bit_idx in R2_A_OPEN_BITS:
            if not state.has_used_once_per_turn(bit_idx):
                state.mark_used_once_per_turn(bit_idx)
                break
        return

    if hook == HOOK_6_1_REDUCTION_VOLONTAIRE:
        if ctx.get("phase") is not None:
            return
        if state.has_slot_used_once_per_turn("R2"):
            return
        openings = sum(1 for bit_idx in R2_A_OPEN_BITS if state.has_used_once_per_turn(bit_idx))
        if openings <= 0:
            return
        state.mark_slot_used_once_per_turn("R2")
        _r2_a_prompt_next(state, 2 * openings)
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        rem = int(ctx["payload"][0])
        prim_mod_apprentissage(state, int(choice), -1)
        _r2_a_prompt_next(state, rem - 1)


# ---------------------------------------------------------------------------
# 5. R2:B — Le Voile de l'Oubli (Entités Magiques) : SIMPLE_CONTINU | LOI 6.1
# ---------------------------------------------------------------------------


@register_tile(
    "R2",
    "B",
    hooks=(HOOK_5_FIN_ATTAQUE_MACHINE, HOOK_6_1_REDUCTION_VOLONTAIRE, HOOK_5_LAW_QUERY),
)
def r2_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi 6.1 : une machine dont toutes les frappes sont parées ne rapporte aucun jeton Apprentissage."""
    if hook == HOOK_5_LAW_QUERY:
        prim_mod_loi_du_coeur(state, "LOI_PARADE_ANNULE_APPRENTISSAGE")
        return True

    if hook == HOOK_5_FIN_ATTAQUE_MACHINE:
        if bool(ctx.get("all_parried")):
            ray = int(ctx["ray"])
            m_type = int(ctx["m_type"])
            mask = (
                PFLAG_ALL_PARRIED_ABATTEUSE
                if m_type == MACHINE_ABATTEUSE
                else PFLAG_ALL_PARRIED_BULLDOZER
            )
            state.set_parcel_flag_turn(ray, 1, mask, True)
        return None

    if hook == HOOK_6_1_REDUCTION_VOLONTAIRE and ctx.get("phase") == "MACHINE_GAIN":
        prim_mod_loi_du_coeur(state, "LOI_PARADE_ANNULE_APPRENTISSAGE")
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        mask = (
            PFLAG_ALL_PARRIED_ABATTEUSE
            if m_type == MACHINE_ABATTEUSE
            else PFLAG_ALL_PARRIED_BULLDOZER
        )
        if state.has_parcel_flag_turn(ray, 1, mask):
            ctx["gain"] = 0
    return None


# ---------------------------------------------------------------------------
# 6. R3:A — La Danse des Esprits-Fauves (Humains) : SIMPLE_CONTINU | 3.2
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
    """À l'ouverture en 3.2, déplace jusqu'à 2 Défenseurs (y compris constructeurs en lisière) vers la Forêt."""
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
# 7. R3:B — La Danse des Esprits-Fauves (Humains) : SIMPLE_CONTINU | LOI 3.1
# ---------------------------------------------------------------------------


@register_tile("R3", "B", hooks=(HOOK_3_1_CONSTRUCTION,))
def r3_b_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
    """Loi 3.1 : libère 1 bâtisseur par le Peuple d'origine à N=4..6, ou tous les bâtisseurs à N=3 (par propriétaire)."""
    if ctx.get("liberation_query"):
        prim_mod_loi_du_coeur(state, "LOI_CONSTRUCTEURS_REJOIGNENT_FORET")
        n_p = int(ctx.get("n_players", state.cfg.n_players))
        ctx["liberate_mode"] = "ALL_BY_OWNER" if n_p == 3 else "ONE"


# ---------------------------------------------------------------------------
# 8. R4:A — Le Sommeil de la Pierre-Serpent (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


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


@register_tile("R4", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, retourne 1 jeton Puissance rouge d'une machine sur sa face bleue Surchauffe."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        cands = _machines_with_red_token(state)
        if not cands:
            return
        if len(cands) == 1:
            rm, mt = cands[0]
            prim_mod_puissance(state, rm, mt, flip_rouge_to_bleu=1)
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
# 9. R4:B — Le Sommeil de la Pierre-Serpent (Humains) : SIMPLE_CONTINU | LOI 3.2
# ---------------------------------------------------------------------------


@register_tile("R4", "B", hooks=(HOOK_3_2_REVELATION,))
def r4_b_handler(state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """Loi 3.2 : si >= 1 Défenseur en Furtivité et >= 1 Sabotage révélé en 3.2 -> +1 carte Sabotage (sans allumer 3)."""
    if state.has_slot_used_once_per_turn("R4"):
        return
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    has_furtive_def = any(
        state.get_furtivite_total_defs(l_idx, p) >= 1
        for l_idx in range(n)
        for p in range(1, p_max + 1)
    )
    if not has_furtive_def:
        return
    has_revealed_sabotage = any(
        state.get_player_hand(s)[0] == CARD_SABOTAGE for s in range(n)
    )
    if not has_revealed_sabotage:
        return
    prim_mod_loi_du_coeur(state, "LOI_SABOTAGE_REVELE_PROLIFERE")
    state.mark_slot_used_once_per_turn("R4")
    prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=False)


# ---------------------------------------------------------------------------
# 10. R4:C — Le Rêve de la seconde rive (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


def _find_adjacent_hr_rays(state: GameState) -> tuple[int, int] | None:
    h_seat = state.cfg.seat_of_peuple("H")
    r_seat = state.cfg.seat_of_peuple("R")
    if h_seat is None or r_seat is None:
        return None
    n = state.cfg.n_players
    if (h_seat + 1) % n == r_seat or (r_seat + 1) % n == h_seat:
        return h_seat, r_seat
    return None


@register_tile("R4", "C", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r4_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Face à une Route Forestière sur la lisière H-R, peut poser 1 Piège sur la parcelle non rasée sans Piège en face (allume 2)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        adj = _find_adjacent_hr_rays(state)
        if adj is None:
            return
        h_seat, r_seat = adj
        cands: list[tuple[int, int]] = []
        for p in range(1, state.cfg.p_max + 1):
            if (
                state.is_route_forestiere(h_seat, p)
                and not state.is_route_forestiere(r_seat, p)
                and state.get_parcel_piege(r_seat, p) == PIEGE_AUCUN
            ):
                cands.append((r_seat, p))
            if (
                state.is_route_forestiere(r_seat, p)
                and not state.is_route_forestiere(h_seat, p)
                and state.get_parcel_piege(h_seat, p) == PIEGE_AUCUN
            ):
                cands.append((h_seat, p))
        if not cands:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            ("PASSER", *cands),
            {"effect_kind": "SECONDE_RIVE_PIEGE_HR"},
            slot_id="R4",
            profile="C",
            resume_tag="PIEGE_R4_C",
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
# 11. R4:D — Le guetteur de pierre (Humains) : SIMPLE_CONTINU | 3.2
# ---------------------------------------------------------------------------


def _r4_d_guetteur_options(state: GameState) -> list[tuple[int, int, int]]:
    h_seat = state.cfg.seat_of_peuple("H")
    r_seat = state.cfg.seat_of_peuple("R")
    hr_rays = {s for s in (h_seat, r_seat) if s is not None}
    if not hr_rays:
        return []

    n = state.cfg.n_players
    p_max = state.cfg.p_max
    tracked_furt: set[tuple[int, int]] = set()
    for s in range(n):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, b, _ = state.decode_def_loc(raw)
                if kind == "FURTIVITE":
                    tracked_furt.add((a, b))

    opts: list[tuple[int, int, int]] = []
    for l_idx in range(n):
        for p in range(1, p_max + 1):
            if (l_idx, p) not in tracked_furt or state.get_furtivite_total_defs(l_idx, p) < 1:
                continue
            for rive in (0, 1):
                dst_ray = state.lisiere_ray_for_rive(l_idx, rive)
                if (
                    dst_ray in hr_rays
                    and not state.is_route_forestiere(dst_ray, p)
                    and state.get_parcel_piege(dst_ray, p) == PIEGE_AUCUN
                    and (l_idx, p, dst_ray) not in opts
                ):
                    opts.append((l_idx, p, dst_ray))
    return opts


@register_tile("R4", "D", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r4_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Peut déplacer 1 Défenseur de Furtivité vers une parcelle H ou R sans Piège en face et y poser 1 Piège (atomique, allume 2)."""
    if hook == HOOK_3_2_OUVERTURE_REVE:
        opts = _r4_d_guetteur_options(state)
        if not opts:
            return
        push_effect_decision(
            state,
            _gov(state, "H"),
            ("PASSER", *opts),
            {"effect_kind": "GUETTEUR_PIERRE_DEF_ET_PIEGE"},
            slot_id="R4",
            profile="D",
            resume_tag="GUETTEUR_R4_D",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        l_c, p_c, dst_r = int(choice[0]), int(choice[1]), int(choice[2])
        if (
            state.get_furtivite_total_defs(l_c, p_c) >= 1
            and not state.is_route_forestiere(dst_r, p_c)
            and state.get_parcel_piege(dst_r, p_c) == PIEGE_AUCUN
        ):
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_lisiere=l_c,
                src_p=p_c,
                dst_ray=dst_r,
                dst_p=p_c,
                count=1,
            )
            prim_creation_entite(state, "PIEGE", ray=dst_r, p=p_c, light_trigger=False)
            state.light_trigger(2)
