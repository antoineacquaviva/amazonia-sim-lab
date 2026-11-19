"""Lot 02 — Gardiens G1..G5 hors pilote (10 profils stateless, 100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_2_1_DEBUT,
    HOOK_2_1_PORTEE_DEF1,
    HOOK_4_1_FURTIVITE,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_5_PARADE_JAGUAR,
    HOOK_5_SEUIL_PARADE,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    prim_mod_seuil,
    prim_partage_info_etat_gardien,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PFLAG_MATAMATA_MARK,
    PIEGE_AUCUN,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameState,
    machine_card_code,
)

__all__ = (
    "LOT_02_PROFILES",
    "g1_b_handler",
    "g2_b_handler",
    "g2_c_handler",
    "g3_a_handler",
    "g3_b_handler",
    "g3_c_handler",
    "g3_d_handler",
    "g4_b_handler",
    "g5_a_handler",
    "g5_b_handler",
)

LOT_02_PROFILES: tuple[tuple[str, str], ...] = (
    ("G1", "B"),
    ("G2", "B"),
    ("G2", "C"),
    ("G3", "A"),
    ("G3", "B"),
    ("G3", "C"),
    ("G3", "D"),
    ("G4", "B"),
    ("G5", "A"),
    ("G5", "B"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _gardien_face_on_track(state: GameState, g_num: int) -> int:
    for c in range(1, TRACK_LEN + 1):
        gn, face, _ = state.get_gardien_at_case(c)
        if gn == g_num:
            return face
    return 0


def _has_tracked_defender_furtivite(state: GameState, l_idx: int, p: int) -> bool:
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, b, _ = state.decode_def_loc(raw)
                if kind == "FURTIVITE" and a == l_idx and b == p:
                    return True
    return False


def _has_tracked_defender_lisiere(state: GameState, slot_idx: int) -> bool:
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, _, _ = state.decode_def_loc(raw)
                if kind == "LISIERE" and a == slot_idx:
                    return True
    return False


def _execute_defender_move(state: GameState, move_choice: tuple[Any, tuple[int, int]]) -> None:
    src_spec, (dst_r, dst_p) = move_choice
    src_kind = str(src_spec[0])
    if src_kind == "FURTIVITE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_lisiere=int(src_spec[1]),
            src_p=int(src_spec[2]),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    elif src_kind == "LISIERE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_lisiere_slot=int(src_spec[1]),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    else:
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_ray=int(src_spec[1]),
            src_p=int(src_spec[2]),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )


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
# 1. G1:B — Le Bond du Jaguar (MOD_SEUIL Face 1 + PARADE_JAGUAR Face 2)
# ---------------------------------------------------------------------------


def _machines_with_power(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                rouges = state.get_machine_effective_rouges(r, mt)
                _, bleus = state.get_machine_tokens(r, mt)
                if rouges + bleus >= 1:
                    out.append((r, mt))
    return out


@register_tile(
    "G1",
    "B",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_PARADE_JAGUAR, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g1_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 : -2 Seuil sur 1 machine avec >= 1 jeton Puissance. Face 2 : Surchauffe >= 2 bleus."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        case_num = int(ctx["case"])
        face = int(ctx["face"])
        if face == 1:
            cands = _machines_with_power(state)
            if not cands:
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return None
            if len(cands) == 1:
                prim_mod_seuil(state, -2, ray=cands[0][0], m_type=cands[0][1])
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return None
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MOD_SEUIL_MACHINE", "face": 1},
                slot_id="G1",
                profile="B",
                resume_tag="F1_SEUIL",
                resume_payload=(case_num,),
            )
            return None
        # Branche Face 2 autonome : Loi 5 passive (marqueur déjà posé par MARK_GARDIEN_OPENED)
        return None

    if hook == HOOK_EFFECT_RESUME:
        case_num = int(ctx["payload"][0])
        rm, mt = ctx["choice"]
        prim_mod_seuil(state, -2, ray=int(rm), m_type=int(mt))
        prim_partage_info_etat_gardien(
            state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
        )
        return None

    if hook == HOOK_5_LAW_QUERY:
        if _gardien_face_on_track(state, 1) != 2:
            return False
        prim_mod_loi_du_coeur(state, "LOI_JAGUAR_SURCHAUFFE_PARADE", active=True)
        return True

    if hook == HOOK_5_PARADE_JAGUAR:
        if _gardien_face_on_track(state, 1) != 2:
            return False
        prim_mod_loi_du_coeur(state, "LOI_JAGUAR_SURCHAUFFE_PARADE", active=True)
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        _, bleus = state.get_machine_tokens(ray, m_type)
        if bleus < 2:
            return False
        prim_mod_puissance(state, ray, m_type, delta_bleus=-2)
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st == MACHINE_STATUS_NORMAL and pos > 0:
            dst_p = state.next_non_razed_towards_border(ray, pos)
            if dst_p is not None:
                prim_deplacement(
                    state, "MACHINE", src_ray=ray, m_type=m_type, dst_ray=ray, dst_p=dst_p
                )
        ctx["parried"] = True
        return True

    return None


# ---------------------------------------------------------------------------
# 2. G2:B — L’Étreinte de l’Anaconda (LOI_MACHINE_PAREE_SANS_ELAN, DOUBLE_FACE)
# ---------------------------------------------------------------------------


@register_tile(
    "G2",
    "B",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_FIN_ATTAQUE_MACHINE, HOOK_5_LAW_QUERY),
)
def g2_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 : machine toute parée n'avance pas sur T3/T6. Face 2 : ni avancée ni rouge sur T3..T6."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        if int(ctx["face"]) == 1:
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=int(ctx["case"]), new_face=2
            )
        return None

    face = _gardien_face_on_track(state, 2)
    if face not in (1, 2):
        return False

    prim_mod_loi_du_coeur(state, "LOI_MACHINE_PAREE_SANS_ELAN", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return True

    if hook == HOOK_5_FIN_ATTAQUE_MACHINE:
        if not ctx.get("all_parried"):
            return False
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        tid = str(ctx["tactique"])
        if len(tid) == 2 and tid[0] == "T" and "1" <= tid[1] <= "6":
            spec = TACTIQUES_SPEC[int(tid[1])]
            cur_pos, _, _ = state.get_machine_pos_status(ray, m_type)
            if (
                "DEVANT" in spec.cibles
                and 0 < cur_pos < state.cfg.p_max
                and state.next_non_razed_towards_heart(ray, cur_pos) is None
            ):
                return False

        if face == 1:
            if tid in ("T3", "T6"):
                ctx["allow_advance"] = False
            return True

        # Branche Face 2 strictement autonome
        if tid in ("T3", "T4", "T5", "T6") or bool(ctx.get("is_ratissage")):
            ctx["allow_advance"] = False
            ctx["allow_red_gain"] = False
        return True

    return None


# ---------------------------------------------------------------------------
# 3. G2:C — La fuite sous les feuilles (DEPLACEMENT INSECTE TOUS)
# ---------------------------------------------------------------------------


@register_tile("G2", "C", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g2_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez déplacer tous les Insectes d'une parcelle vers la prochaine non rasée (bord/cœur)."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        opts: list[tuple[int, int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    p_b = state.next_non_razed_towards_border(r, p)
                    if p_b is not None:
                        opts.append((r, p, p_b))
                    p_h = state.next_non_razed_towards_heart(r, p)
                    if p_h is not None:
                        opts.append((r, p, p_h))
        if not opts:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *opts),
            {"effect_kind": "MOVE_ALL_INSECTES"},
            slot_id="G2",
            profile="C",
            resume_tag="MOVE_INS",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        r, src_p, dst_p = int(choice[0]), int(choice[1]), int(choice[2])
        cnt = state.get_parcel_insectes(r, src_p)
        if cnt >= 1 and not state.is_route_forestiere(r, dst_p):
            prim_deplacement(
                state,
                "INSECTE",
                src_ray=r,
                src_p=src_p,
                dst_ray=r,
                dst_p=dst_p,
                count=cnt,
            )


# ---------------------------------------------------------------------------
# 4. G3:A — La Voltige de l’Atèle (DEPLACEMENT DEFENSEUR adjacent + lisière)
# ---------------------------------------------------------------------------


def _build_g3_a_moves(state: GameState) -> list[tuple[tuple[Any, ...], tuple[int, int]]]:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    moves: list[tuple[tuple[Any, ...], tuple[int, int]]] = []

    for r in range(n):
        for p in range(1, p_max + 1):
            if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 1:
                p_b = state.next_non_razed_towards_border(r, p)
                if p_b is not None:
                    moves.append((("FORET", r, p), (r, p_b)))
                p_h = state.next_non_razed_towards_heart(r, p)
                if p_h is not None:
                    moves.append((("FORET", r, p), (r, p_h)))

    for l_idx in range(n):
        r0 = l_idx
        r1 = (l_idx + 1) % n
        for p in range(1, p_max + 1):
            if (
                state.get_furtivite_total_defs(l_idx, p) >= 1
                and _has_tracked_defender_furtivite(state, l_idx, p)
            ):
                if not state.is_route_forestiere(r0, p):
                    moves.append((("FURTIVITE", l_idx, p), (r0, p)))
                if r1 != r0 and not state.is_route_forestiere(r1, p):
                    moves.append((("FURTIVITE", l_idx, p), (r1, p)))

    for slot_idx in range(2 * n):
        _, nb = state.get_lisiere_tile_state(slot_idx)
        if nb >= 1 and _has_tracked_defender_lisiere(state, slot_idx):
            l_idx = slot_idx // 2
            seen_dst: list[tuple[int, int]] = []
            for r_adj in (l_idx, (l_idx + 1) % n):
                p_first = state.first_non_razed_from_border(r_adj)
                if p_first is not None and (r_adj, p_first) not in seen_dst:
                    seen_dst.append((r_adj, p_first))
                    moves.append((("LISIERE", slot_idx), (r_adj, p_first)))

    return moves


@register_tile("G3", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g3_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Déplace 1 Défenseur (y compris constructeur en bordure de lisière) vers une Forêt adjacente."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        moves = _build_g3_a_moves(state)
        if not moves:
            return
        if len(moves) == 1:
            _execute_defender_move(state, moves[0])
            return
        push_effect_decision(
            state,
            gov,
            moves,
            {"effect_kind": "VOLTIGE_ATELE"},
            slot_id="G3",
            profile="A",
            resume_tag="MOVE_DEF",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        _execute_defender_move(state, ctx["choice"])


# ---------------------------------------------------------------------------
# 5. G3:B — La Voltige de l’Atèle (LOI 4.1 -> 5 : glissement gratuit vers Forêt)
# ---------------------------------------------------------------------------


@register_tile("G3", "B", hooks=(HOOK_4_1_FURTIVITE,))
def g3_b_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
    """Loi 4.1 : 1/tour, après l'action d'un binôme sur lisière M ou O, 1 Défenseur glisse en face."""
    if ctx.get("phase") == "PRE":
        return
    if state.has_slot_used_once_per_turn("G3"):
        return

    n = state.cfg.n_players
    l_idx = int(ctx["lisiere"])
    p = int(ctx["p"])
    rive = int(ctx["rive"])

    m_seat = state.cfg.seat_of_peuple("M")
    o_seat = state.cfg.seat_of_peuple("O")
    r0 = l_idx
    r1 = (l_idx + 1) % n
    if r0 not in (m_seat, o_seat) and r1 not in (m_seat, o_seat):
        return

    t_ray = state.lisiere_ray_for_rive(l_idx, rive)
    if state.is_route_forestiere(t_ray, p):
        return
    if not _has_tracked_defender_furtivite(state, l_idx, p):
        return

    if not ctx.get("handled"):
        d_rive = state.get_furtivite_nb_def_rive(l_idx, p, rive)
        d_other = state.get_furtivite_nb_def_rive(l_idx, p, 1 - rive)
        ins = state.get_furtivite_insectes(l_idx, p)
        use_ins = d_rive == 1 and d_other == 0 and ins >= 1

        present_m = state.machines_on_parcel(t_ray, p)
        if not present_m:
            if state.get_parcel_piege(t_ray, p) != PIEGE_AUCUN:
                return
            if use_ins:
                state.set_furtivite_insectes(l_idx, p, ins - 1)
            prim_creation_entite(state, "PIEGE", ray=t_ray, p=p, light_trigger=True)
            ctx["handled"] = True
        else:
            if any(_is_machine_active_turn(state, t_ray, mt) for mt in present_m):
                return
            if use_ins:
                state.set_furtivite_insectes(l_idx, p, ins - 1)
            prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=True)
            ctx["handled"] = True

    prim_mod_loi_du_coeur(state, "LOI_FURTIVITE_GLISSE_EN_FORET_ETAPE_5", active=True)
    prim_deplacement(
        state,
        "DEFENSEUR",
        src_lisiere=l_idx,
        src_p=p,
        dst_ray=t_ray,
        dst_p=p,
        count=1,
    )
    state.mark_slot_used_once_per_turn("G3")


# ---------------------------------------------------------------------------
# 6. G3:C — Le passage des singes-lianes (DEPLACEMENT TRAVERSEE M<->O)
# ---------------------------------------------------------------------------


@register_tile("G3", "C", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g3_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez faire passer 1 Défenseur entre M et O à la même profondeur (parcelles non rasées)."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        r_m = state.cfg.seat_of_peuple("M")
        r_o = state.cfg.seat_of_peuple("O")
        if r_m is None or r_o is None:
            return
        opts: list[tuple[tuple[str, int, int], tuple[int, int]]] = []
        for p in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(r_m, p) and not state.is_route_forestiere(r_o, p):
                if state.get_parcel_defenseurs(r_m, p) >= 1:
                    opts.append((("FORET", r_m, p), (r_o, p)))
                if state.get_parcel_defenseurs(r_o, p) >= 1:
                    opts.append((("FORET", r_o, p), (r_m, p)))
        if not opts:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *opts),
            {"effect_kind": "TRAVERSEE_M_O"},
            slot_id="G3",
            profile="C",
            resume_tag="TRAVERSEE",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice != "PASSER":
            _execute_defender_move(state, choice)


# ---------------------------------------------------------------------------
# 7. G3:D — Les sentinelles des lianes (DEPLACEMENT FURTIVITE -> PARCELLE_PIEGEE)
# ---------------------------------------------------------------------------


@register_tile("G3", "D", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g3_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Vous pouvez déplacer 1 Défenseur d'une case Furtivité vers une parcelle piégée M/O en face."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        n = state.cfg.n_players
        eligible_rays = tuple(
            s for code in ("M", "O") if (s := state.cfg.seat_of_peuple(code)) is not None
        )
        if not eligible_rays:
            return

        opts: list[tuple[tuple[str, int, int], tuple[int, int]]] = []
        for l_idx in range(n):
            for p in range(1, state.cfg.p_max + 1):
                if (
                    state.get_furtivite_total_defs(l_idx, p) >= 1
                    and _has_tracked_defender_furtivite(state, l_idx, p)
                ):
                    for dst_r in (l_idx, (l_idx + 1) % n):
                        if (
                            dst_r in eligible_rays
                            and not state.is_route_forestiere(dst_r, p)
                            and state.get_parcel_piege(dst_r, p) != PIEGE_AUCUN
                        ):
                            cand = (("FURTIVITE", l_idx, p), (dst_r, p))
                            if cand not in opts:
                                opts.append(cand)
        if not opts:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *opts),
            {"effect_kind": "FURTIVITE_VERS_PIEGE"},
            slot_id="G3",
            profile="D",
            resume_tag="TO_TRAP",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice != "PASSER":
            _execute_defender_move(state, choice)


# ---------------------------------------------------------------------------
# 8. G4:B — Le Cri d’Alarme de l’Ara (LOI 2.1 portée globale + SACRIFICE Début 2)
# ---------------------------------------------------------------------------


@register_tile(
    "G4",
    "B",
    hooks=(HOOK_2_1_DEBUT, HOOK_2_1_PORTEE_DEF1, HOOK_EFFECT_RESUME),
)
def g4_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 (Loi 2.1) : O et M posent leur 1er Déf à portée globale. Sacrifice Début 2 : paravents."""
    gov = _gov(state, "O")

    if hook == HOOK_2_1_PORTEE_DEF1:
        seat = int(ctx["seat"])
        o_seat = state.cfg.seat_of_peuple("O")
        m_seat = state.cfg.seat_of_peuple("M")
        if seat == o_seat or seat == m_seat:
            prim_mod_loi_du_coeur(state, "LOI_PORTEE_GLOBALE_DEF1_O_M", active=True)
            ctx["global_range"] = True
            return True
        return False

    if hook == HOOK_2_1_DEBUT:
        if state.paravents_ouverts:
            return None
        g4_case: int | None = None
        for c in range(1, TRACK_LEN + 1):
            if state.get_gardien_at_case(c)[0] == 4:
                g4_case = c
                break
        if g4_case is None:
            return None
        push_effect_decision(
            state,
            gov,
            ("PASSER", "SACRIFIER_G4_PARAVENTS"),
            {"effect_kind": "SACRIFICE_G4_PARAVENTS"},
            slot_id="G4",
            profile="B",
            resume_tag="SAC_2_1",
            resume_payload=(g4_case,),
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        if ctx["choice"] == "SACRIFIER_G4_PARAVENTS":
            g4_case = int(ctx["payload"][0])
            prim_partage_info_etat_gardien(state, "OPEN_PARAVENTS")
            prim_partage_info_etat_gardien(
                state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=g4_case
            )
        return None

    return None


# ---------------------------------------------------------------------------
# 9. G5:A — L’Affût de la Matamata (OUVERTURE LOI TEMP 5 sur parcelles désignées)
# ---------------------------------------------------------------------------


def _unmarked_matamata_parcels(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if (
                not state.is_route_forestiere(r, p)
                and not state.has_parcel_flag_turn(r, p, PFLAG_MATAMATA_MARK)
            ):
                out.append((r, p))
    return out


@register_tile(
    "G5",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 : marque 1 parcelle (-1 Seuil si Souche). Face 2 : marque jusqu'à 2 parcelles."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        case_num = int(ctx["case"])
        face = int(ctx["face"])
        cands = _unmarked_matamata_parcels(state)

        if face == 1:
            if not cands:
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return None
            if len(cands) == 1:
                state.set_parcel_flag_turn(
                    cands[0][0], cands[0][1], PFLAG_MATAMATA_MARK, True
                )
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return None
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MOD_SEUIL_PARCELLE", "face": 1},
                slot_id="G5",
                profile="A",
                resume_tag="F1_MARK",
                resume_payload=(case_num,),
            )
            return None

        # Branche Face 2 strictement autonome ("jusqu'à 2 parcelles non rasées")
        if not cands:
            return None
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "MOD_SEUIL_PARCELLE", "face": 2, "remaining": 2},
            slot_id="G5",
            profile="A",
            resume_tag="F2_MARK",
            resume_payload=(2,),
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        payload: tuple[Any, ...] = ctx["payload"]

        if rtag == "F1_MARK":
            case_num = int(payload[0])
            r_c, p_c = choice
            state.set_parcel_flag_turn(int(r_c), int(p_c), PFLAG_MATAMATA_MARK, True)
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
            )
            return None

        if rtag == "F2_MARK":
            rem = int(payload[0])
            if choice == "PASSER":
                return None
            r_c, p_c = choice
            state.set_parcel_flag_turn(int(r_c), int(p_c), PFLAG_MATAMATA_MARK, True)
            if rem > 1:
                cands_next = _unmarked_matamata_parcels(state)
                if cands_next:
                    push_effect_decision(
                        state,
                        gov,
                        ("PASSER", *cands_next),
                        {"effect_kind": "MOD_SEUIL_PARCELLE", "face": 2, "remaining": rem - 1},
                        slot_id="G5",
                        profile="A",
                        resume_tag="F2_MARK",
                        resume_payload=(rem - 1,),
                    )
        return None

    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        active = state.has_parcel_flag_turn(ray, target_p, PFLAG_MATAMATA_MARK)
        if active:
            prim_mod_loi_du_coeur(state, "LOI_SOUCHES_REDUISENT_SEUIL", active=True)
        return active

    return None


# ---------------------------------------------------------------------------
# 10. G5:B — L’Affût de la Matamata (LOI 5 passive R/O puis tout le plateau)
# ---------------------------------------------------------------------------


@register_tile(
    "G5",
    "B",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_SEUIL_PARADE, HOOK_5_LAW_QUERY),
)
def g5_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 (Loi 5) : -1 Seuil si >= 1 Souche sur R et O. Face 2 : sur tout le plateau."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        if int(ctx["face"]) == 1:
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=int(ctx["case"]), new_face=2
            )
        return None

    face = _gardien_face_on_track(state, 5)
    ray = int(ctx["ray"])

    if face == 1:
        r_seat = state.cfg.seat_of_peuple("R")
        o_seat = state.cfg.seat_of_peuple("O")
        eligible = ray == r_seat or ray == o_seat
    elif face == 2:
        # Branche Face 2 strictement autonome
        eligible = True
    else:
        return False

    prim_mod_loi_du_coeur(state, "LOI_SOUCHES_REDUISENT_SEUIL", active=True)
    if hook == HOOK_5_LAW_QUERY:
        return eligible

    if hook == HOOK_5_SEUIL_PARADE:
        target_p = int(ctx["target_p"])
        if eligible and state.get_parcel_souches(ray, target_p) >= 1:
            ctx["delta_seuil"] = int(ctx["delta_seuil"]) - 1
        return eligible

    return None
