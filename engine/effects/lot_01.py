"""Lot 01 — Lot Pilote des 8 Primitives Formelles (stateless, 100 % stdlib PyPy 3.11)."""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_APRES_REVELATION,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_5_LAW_QUERY,
    HOOK_5_SEUIL_PARADE,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_mod_puissance,
    prim_mod_seuil,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
)
from engine.state import (
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    MACHINE_STATUS_SIEGE,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameState,
)

__all__ = (
    "LOT_01_PROFILES",
    "g1_a_handler",
    "g2_a_handler",
    "g4_a_handler",
    "g6_a_handler",
    "g7_a_handler",
    "g9_c_handler",
    "g10_a_handler",
    "r5_a_handler",
)

LOT_01_PROFILES: tuple[tuple[str, str], ...] = (
    ("G1", "A"),
    ("G2", "A"),
    ("G4", "A"),
    ("G6", "A"),
    ("G7", "A"),
    ("G10", "A"),
    ("R5", "A"),
    ("G9", "C"),
)

# Drapeaux transitoires (plage libre 32..63 de TRANS_ONCE_PER_TURN, RAZ automatique en 6.2)
G6_A_PREPARED_LOCK: int = 40
G6_A_RESOLVED_LOCK: int = 41


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


# ---------------------------------------------------------------------------
# 1. G1:A — Le Bond du Jaguar (MOD_PUISSANCE, DOUBLE_FACE_UPGRADE)
# ---------------------------------------------------------------------------


def _machines_with_red(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_RETIRED and pos > 0:
                rouges, bleus = state.get_machine_tokens(r, mt)
                if rouges >= 1 and bleus < 15:
                    out.append((r, mt))
    return out


@register_tile("G1", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g1_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Face 1 : 1 rouge -> bleu (puis passage Face 2). Face 2 : jusqu'à 2 rouges -> bleus."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        case_num = int(ctx["case"])
        face = int(ctx["face"])
        cands = _machines_with_red(state)

        if face == 1:
            if not cands:
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return
            if len(cands) == 1:
                rm, mt = cands[0]
                prim_mod_puissance(state, rm, mt, flip_rouge_to_bleu=1)
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MACHINE_SURCHAUFFE", "face": 1},
                slot_id="G1",
                profile="A",
                resume_tag="F1_PICK",
                resume_payload=(case_num,),
            )
            return

        # Branche Face 2 strictement autonome ("jusqu'à 2 jetons rouges en bleus")
        if not cands:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *cands),
            {"effect_kind": "MACHINE_SURCHAUFFE", "face": 2, "remaining": 2},
            slot_id="G1",
            profile="A",
            resume_tag="F2_PICK",
            resume_payload=(2,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]
        payload: tuple[Any, ...] = ctx["payload"]

        if rtag == "F1_PICK":
            case_num = int(payload[0])
            rm, mt = choice
            prim_mod_puissance(state, int(rm), int(mt), flip_rouge_to_bleu=1)
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
            )
            return

        if rtag == "F2_PICK":
            rem = int(payload[0])
            if choice == "PASSER":
                return
            rm, mt = choice
            prim_mod_puissance(state, int(rm), int(mt), flip_rouge_to_bleu=1)
            if rem > 1:
                cands_next = _machines_with_red(state)
                if cands_next:
                    push_effect_decision(
                        state,
                        gov,
                        ("PASSER", *cands_next),
                        {"effect_kind": "MACHINE_SURCHAUFFE", "face": 2, "remaining": rem - 1},
                        slot_id="G1",
                        profile="A",
                        resume_tag="F2_PICK",
                        resume_payload=(rem - 1,),
                    )


# ---------------------------------------------------------------------------
# 2. G2:A — L’Étreinte de l’Anaconda (DEPLACEMENT MACHINE, DOUBLE_FACE_UPGRADE)
# ---------------------------------------------------------------------------


def _reculable_machines(state: GameState, *, require_defender: bool) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_NORMAL or pos <= 0:
                continue
            if require_defender and state.get_parcel_defenseurs(r, pos) < 1:
                continue
            if state.next_non_razed_towards_border(r, pos) is not None:
                out.append((r, mt))
    return out


def _apply_machine_recul_1(state: GameState, r: int, mt: int) -> None:
    pos, st, _ = state.get_machine_pos_status(r, mt)
    if st != MACHINE_STATUS_NORMAL or pos <= 0:
        return
    dst_p = state.next_non_razed_towards_border(r, pos)
    if dst_p is not None:
        prim_deplacement(state, "MACHINE", src_ray=r, m_type=mt, dst_ray=r, dst_p=dst_p)


@register_tile("G2", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g2_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Face 1 : recul 1 machine hors Siège sur parcelle avec >= 1 Déf. Face 2 : toute machine hors Siège."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        case_num = int(ctx["case"])
        face = int(ctx["face"])

        if face == 1:
            cands = _reculable_machines(state, require_defender=True)
            if not cands:
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return
            if len(cands) == 1:
                _apply_machine_recul_1(state, cands[0][0], cands[0][1])
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MACHINE_RECUL", "face": 1},
                slot_id="G2",
                profile="A",
                resume_tag="F1_RECUL",
                resume_payload=(case_num,),
            )
            return

        # Branche Face 2 strictement autonome
        cands_f2 = _reculable_machines(state, require_defender=False)
        if not cands_f2:
            return
        if len(cands_f2) == 1:
            _apply_machine_recul_1(state, cands_f2[0][0], cands_f2[0][1])
            return
        push_effect_decision(
            state,
            gov,
            cands_f2,
            {"effect_kind": "MACHINE_RECUL", "face": 2},
            slot_id="G2",
            profile="A",
            resume_tag="F2_RECUL",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        rm, mt = ctx["choice"]
        _apply_machine_recul_1(state, int(rm), int(mt))
        if rtag == "F1_RECUL":
            case_num = int(ctx["payload"][0])
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
            )


# ---------------------------------------------------------------------------
# 3. G4:A — Le Cri d’Alarme de l’Ara (MOD_SEUIL + SACRIFICE 3.2 DEPLACEMENT)
# ---------------------------------------------------------------------------


def _targeted_parcels_after_revelation(state: GameState) -> list[tuple[int, int]]:
    targeted: list[tuple[int, int]] = []
    n = state.cfg.n_players

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if (
                st == MACHINE_STATUS_SIEGE
                and pos > 0
                and not state.is_route_forestiere(r, pos)
                and (r, pos) not in targeted
            ):
                targeted.append((r, pos))

    for s in range(n):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and bound_t in TACTIQUES_SPEC:
            rm, mt = (card - 1) // 2, (card - 1) % 2
            pos, st, _ = state.get_machine_pos_status(rm, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0:
                spec = TACTIQUES_SPEC[bound_t]
                for c_kind in spec.cibles:
                    if c_kind == "SUR_PLACE" and not state.is_route_forestiere(rm, pos):
                        if (rm, pos) not in targeted:
                            targeted.append((rm, pos))
                    elif c_kind == "DEVANT":
                        p_dev = state.next_non_razed_towards_heart(rm, pos)
                        if p_dev is not None and (rm, p_dev) not in targeted:
                            targeted.append((rm, p_dev))
    return targeted


def _build_g4_defender_moves(
    state: GameState, targeted_parcels: list[tuple[int, int]]
) -> list[tuple[tuple[str, int, int], tuple[int, int]]]:
    if not targeted_parcels:
        return []
    sources: list[tuple[str, int, int]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 1:
                sources.append(("FORET", r, p))
        for p in range(1, state.cfg.p_max + 1):
            if state.get_furtivite_total_defs(r, p) >= 1:
                sources.append(("FURTIVITE", r, p))

    moves: list[tuple[tuple[str, int, int], tuple[int, int]]] = []
    for src in sources:
        for dst_r, dst_p in targeted_parcels:
            if src == ("FORET", dst_r, dst_p):
                continue
            moves.append((src, (dst_r, dst_p)))
    return moves


def _execute_g4_single_move(
    state: GameState, move_choice: tuple[tuple[str, int, int], tuple[int, int]]
) -> None:
    src_spec, (dst_r, dst_p) = move_choice
    src_kind, src_a, src_p = src_spec
    if src_kind == "FURTIVITE":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_lisiere=int(src_a),
            src_p=int(src_p),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    else:
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_ray=int(src_a),
            src_p=int(src_p),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )


@register_tile(
    "G4",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_3_2_APRES_REVELATION, HOOK_EFFECT_RESUME),
)
def g4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Ouverture : -1 Seuil sur parcelle O ou M. Sacrifice 3.2 : déplace jusqu'à 2 Défenseurs."""
    gov = _gov(state, "O")

    if hook == HOOK_GARDIEN_OUVERTURE:
        parcels: list[tuple[int, int]] = []
        for p_code in ("O", "M"):
            r_seat = state.cfg.seat_of_peuple(p_code)
            if r_seat is not None:
                for p in range(1, state.cfg.p_max + 1):
                    if not state.is_route_forestiere(r_seat, p) and (r_seat, p) not in parcels:
                        parcels.append((r_seat, p))
        if not parcels:
            return
        if len(parcels) == 1:
            prim_mod_seuil(state, -1, ray=parcels[0][0], p=parcels[0][1])
            return
        push_effect_decision(
            state,
            gov,
            parcels,
            {"effect_kind": "MOD_SEUIL_PARCELLE"},
            slot_id="G4",
            profile="A",
            resume_tag="OPEN_SEUIL",
        )
        return

    if hook == HOOK_3_2_APRES_REVELATION:
        g4_case: int | None = None
        for c in range(1, TRACK_LEN + 1):
            if state.get_gardien_at_case(c)[0] == 4:
                g4_case = c
                break
        if g4_case is None:
            return
        targeted = _targeted_parcels_after_revelation(state)
        moves = _build_g4_defender_moves(state, targeted)
        if not moves:
            return
        push_effect_decision(
            state,
            gov,
            ("PASSER", *moves),
            {"effect_kind": "SACRIFICE_G4_MOVE", "step": 1},
            slot_id="G4",
            profile="A",
            resume_tag="SAC_STEP_1",
            resume_payload=(g4_case,),
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        choice = ctx["choice"]

        if rtag == "OPEN_SEUIL":
            r_c, p_c = choice
            prim_mod_seuil(state, -1, ray=int(r_c), p=int(p_c))
            return

        if rtag == "SAC_STEP_1":
            if choice == "PASSER":
                return
            g4_case = int(ctx["payload"][0])
            _execute_g4_single_move(state, choice)
            prim_partage_info_etat_gardien(
                state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=g4_case
            )
            moves_2 = _build_g4_defender_moves(state, _targeted_parcels_after_revelation(state))
            if moves_2:
                push_effect_decision(
                    state,
                    gov,
                    ("PASSER", *moves_2),
                    {"effect_kind": "SACRIFICE_G4_MOVE_2", "step": 2},
                    slot_id="G4",
                    profile="A",
                    resume_tag="SAC_STEP_2",
                )
            return

        if rtag == "SAC_STEP_2" and choice != "PASSER":
            _execute_g4_single_move(state, choice)


# ---------------------------------------------------------------------------
# 4. G6:A — L’Œil Double du Toucan (PERMUTATION_PISTE LECTURE_DE_M)
# ---------------------------------------------------------------------------


def _shift_m_options(state: GameState) -> list[tuple[int, int]]:
    opts: list[tuple[int, int]] = []
    for s in range(state.cfg.n_players):
        card, _, _, lec_m, _ = state.get_player_hand(s)
        if 1 <= card <= 12 and 1 <= lec_m <= 6:
            if lec_m > 1:
                opts.append((s, -1))
            if lec_m < 6:
                opts.append((s, 1))
    return opts


@register_tile(
    "G6",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_3_2_REVELATION, HOOK_EFFECT_RESUME),
)
def g6_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """En 3.2, décale de -1 ou +1 rang la lecture du dé M d'un joueur (préparé si ouvert avant 3.2)."""
    gov = _gov(state, "O")

    if hook == HOOK_GARDIEN_OUVERTURE:
        if state.step < STEP_3_2_REVEAL or not state.paravents_ouverts:
            state.mark_used_once_per_turn(G6_A_PREPARED_LOCK)
            return
        if state.step == STEP_3_2_REVEAL and not state.has_used_once_per_turn(G6_A_RESOLVED_LOCK):
            state.mark_used_once_per_turn(G6_A_RESOLVED_LOCK)
            opts = _shift_m_options(state)
            if not opts:
                return
            if len(opts) == 1:
                prim_permutation_piste(
                    state,
                    "SHIFT_LECTURE_M",
                    seat=opts[0][0],
                    delta_m=opts[0][1],
                    rebind_tactique=True,
                )
                return
            push_effect_decision(
                state,
                gov,
                opts,
                {"effect_kind": "SHIFT_LECTURE_M"},
                slot_id="G6",
                profile="A",
                resume_tag="SHIFT_AFTER_BIND",
            )
        return

    if hook == HOOK_3_2_REVELATION:
        if not state.has_used_once_per_turn(G6_A_PREPARED_LOCK):
            return
        if state.has_used_once_per_turn(G6_A_RESOLVED_LOCK):
            return
        state.mark_used_once_per_turn(G6_A_RESOLVED_LOCK)
        opts = _shift_m_options(state)
        if not opts:
            return
        if len(opts) == 1:
            prim_permutation_piste(
                state,
                "SHIFT_LECTURE_M",
                seat=opts[0][0],
                delta_m=opts[0][1],
                rebind_tactique=False,
            )
            return
        push_effect_decision(
            state,
            gov,
            opts,
            {"effect_kind": "SHIFT_LECTURE_M"},
            slot_id="G6",
            profile="A",
            resume_tag="SHIFT_PRE_BIND",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        s_id, d_m = ctx["choice"]
        prim_permutation_piste(
            state,
            "SHIFT_LECTURE_M",
            seat=int(s_id),
            delta_m=int(d_m),
            rebind_tactique=(rtag == "SHIFT_AFTER_BIND"),
        )


# ---------------------------------------------------------------------------
# 5. G7:A — Le Barrage du Capybara (CREATION_ENTITE PIEGE sur Souche)
# ---------------------------------------------------------------------------


@register_tile("G7", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g7_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Piège sur toute parcelle non rasée avec >= 1 Souche et aucun Piège (allume 2)."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        cands: list[tuple[int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if (
                    not state.is_route_forestiere(r, p)
                    and state.get_parcel_souches(r, p) >= 1
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
            gov,
            cands,
            {"effect_kind": "PIEGE_SOUCHE"},
            slot_id="G7",
            profile="A",
            resume_tag="PLACE_TRAP",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        r_c, p_c = ctx["choice"]
        if (
            not state.is_route_forestiere(int(r_c), int(p_c))
            and state.get_parcel_piege(int(r_c), int(p_c)) == PIEGE_AUCUN
        ):
            prim_creation_entite(
                state, "PIEGE", ray=int(r_c), p=int(p_c), light_trigger=True
            )


# ---------------------------------------------------------------------------
# 6. G10:A — La Brume de la Dendrobate (MOD_APPRENTISSAGE mémorisé pour 6.1)
# ---------------------------------------------------------------------------


@register_tile("G10", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
def g10_a_handler(state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """Mémorise -1 jeton Apprentissage volontaire en 6.1 avant la résolution des Bugs."""
    gov = _gov(state, "R")
    state.add_pending_voluntary_app_reduction(1, gov)


# ---------------------------------------------------------------------------
# 7. R5:A — La Vision des Plumes Claires (PARTAGE_INFO_ETAT_GARDIEN en 3.2)
# ---------------------------------------------------------------------------


@register_tile("R5", "A", hooks=(HOOK_3_2_OUVERTURE_REVE, HOOK_EFFECT_RESUME))
def r5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """À l'ouverture en 3.2, ouvre immédiatement un Gardien disponible (allume 4 en résonance)."""
    gov = _gov(state, "H")

    if hook == HOOK_3_2_OUVERTURE_REVE:
        avail = [
            c
            for c in range(1, TRACK_LEN + 1)
            if state.get_gardien_at_case(c)[0] > 0 and not state.get_gardien_at_case(c)[2]
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
# 8. G9:C — La Peau de boue (MOD_LOI_DU_COEUR : LOI_ROUGES_IGNORES_DEVANT)
# ---------------------------------------------------------------------------


def _is_reptile_or_human_ray(state: GameState, ray: int) -> bool:
    r_seat = state.cfg.seat_of_peuple("R")
    h_seat = state.cfg.seat_of_peuple("H")
    return ray == r_seat or ray == h_seat


@register_tile("G9", "C", hooks=(HOOK_5_SEUIL_PARADE, HOOK_5_LAW_QUERY))
def g9_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool:
    """Loi 5 : Sur les rayons R et H, ignore tous les jetons rouges quand la machine frappe devant."""
    prim_mod_loi_du_coeur(state, "LOI_ROUGES_IGNORES_DEVANT", active=True)
    ray = int(ctx["ray"])
    eligible = _is_reptile_or_human_ray(state, ray)
    if hook == HOOK_5_LAW_QUERY:
        return eligible
    if eligible and ctx.get("cible_type") == "DEVANT":
        ctx["rouges"] = 0
    return eligible
