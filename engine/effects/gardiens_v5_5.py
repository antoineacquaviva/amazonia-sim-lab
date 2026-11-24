"""Catalogue actif v5.5 — Les 15 Gardiens STANDARD_A (G1:A..G15:A).

Compatibilité complète avec le socle gelé v5.5 :
- Double activation native sur un Gardien (pari uniforme de 0, 1 ou 2 Défenseurs glissés) ;
- Passage Face 1 -> Face 2 exclusivement en 5.3 sur pari gagné (jamais à l'ouverture) ;
- Partition stricte des 6 déclencheurs (création d'entité via effet de tuile : light_trigger=False) ;
- 100 % stateless, zéro accès `_buf`, zéro `random`, stdlib PyPy 3.11 pure.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_3_2_APRES_REVELATION,
    HOOK_3_2_REVELATION,
    HOOK_5_CIBLAGE_MACHINE,
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
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    PFLAG_AUTO_PARADE_ONCE,
    PFLAG_MATAMATA_MARK,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TRACK_LEN,
    GameState,
    is_reve_code,
)

__all__ = (
    "GARDIENS_V5_5_PROFILES",
    "g1_a_handler",
    "g2_a_handler",
    "g3_a_handler",
    "g4_a_handler",
    "g5_a_handler",
    "g6_a_handler",
    "g7_a_handler",
    "g8_a_handler",
    "g9_a_handler",
    "g10_a_handler",
    "g11_a_handler",
    "g12_a_handler",
    "g13_a_handler",
    "g14_a_handler",
    "g15_a_handler",
)

GARDIENS_V5_5_PROFILES: tuple[tuple[str, str], ...] = (
    ("G1", "A"),
    ("G2", "A"),
    ("G3", "A"),
    ("G4", "A"),
    ("G5", "A"),
    ("G6", "A"),
    ("G7", "A"),
    ("G8", "A"),
    ("G9", "A"),
    ("G10", "A"),
    ("G11", "A"),
    ("G12", "A"),
    ("G13", "A"),
    ("G14", "A"),
    ("G15", "A"),
)

# Plage transitoire libre 32..63 de TRANS_ONCE_PER_TURN (RAZ automatique en 6.2)
# G6:A : jusqu'à 2 ouvertures préparées avant 3.2 (double pari v5.5)
G6_A_PREP_1_BIT: int = 40
G6_A_PREP_2_BIT: int = 41

# G8:A : jusqu'à 2 préparations avant 3.2 + 2 emplacements de décalage de ciblage (6 bits chacun)
G8_A_PREP_1_BIT: int = 42
G8_A_PREP_2_BIT: int = 43
G8_A_SLOT1_BASE: int = 44  # bits 44..49 : [active, ray_b0, ray_b1, ray_b2, m_type, dir_heart]
G8_A_SLOT2_BASE: int = 50  # bits 50..55 : [active, ray_b0, ray_b1, ray_b2, m_type, dir_heart]


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


def _has_tracked_defender_furtivite(state: GameState, l_idx: int, p: int) -> bool:
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw == 0:
                continue
            kind, a, b, _ = state.decode_def_loc(raw)
            if kind == "FURTIVITE" and a == l_idx and b == p:
                return True
    return False


def _has_tracked_defender_lisiere(state: GameState, slot_idx: int) -> bool:
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw == 0:
                continue
            kind, a, _, _ = state.decode_def_loc(raw)
            if kind == "LISIERE" and a == slot_idx:
                return True
    return False


def _execute_defender_move(
    state: GameState, move_choice: tuple[tuple[Any, ...], tuple[int, int]]
) -> None:
    src_spec, (dst_r, dst_p) = move_choice
    src_kind = str(src_spec[0])
    if src_kind == "FORET":
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_ray=int(src_spec[1]),
            src_p=int(src_spec[2]),
            dst_ray=int(dst_r),
            dst_p=int(dst_p),
            count=1,
        )
    elif src_kind == "FURTIVITE":
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


# ---------------------------------------------------------------------------
# G1:A — Le Bond du Jaguar (MOD_PUISSANCE, double-face 5.3)
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
    """Face 1 : 1 rouge -> bleu. Face 2 : jusqu'à 2 rouges -> bleus. Flip Face 2 en 5.3 uniquement."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx["face"])
        cands = _machines_with_red(state)
        if not cands:
            return
        if face == 1:
            if len(cands) == 1:
                prim_mod_puissance(state, cands[0][0], cands[0][1], flip_rouge_to_bleu=1)
                return
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MACHINE_SURCHAUFFE", "face": 1},
                slot_id="G1",
                profile="A",
                resume_tag="F1_PICK",
            )
            return

        # Face 2 autonome : jusqu'à 2 jetons rouges en bleus Surchauffe
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
        if rtag == "F1_PICK":
            rm, mt = choice
            prim_mod_puissance(state, int(rm), int(mt), flip_rouge_to_bleu=1)
            return
        if rtag == "F2_PICK":
            if choice == "PASSER":
                return
            rem = int(ctx["payload"][0])
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
# G2:A — L'Étreinte de l'Anaconda (DEPLACEMENT MACHINE, double-face 5.3)
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
    """Face 1 : recul 1 machine non en Ratissage avec >= 1 Déf. Face 2 : toute machine non en Ratissage."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx["face"])
        cands = _reculable_machines(state, require_defender=(face == 1))
        if not cands:
            return
        if len(cands) == 1:
            _apply_machine_recul_1(state, cands[0][0], cands[0][1])
            return
        push_effect_decision(
            state,
            gov,
            cands,
            {"effect_kind": "MACHINE_RECUL", "face": face},
            slot_id="G2",
            profile="A",
            resume_tag="RECUL",
        )
        return

    if hook == HOOK_EFFECT_RESUME:
        rm, mt = ctx["choice"]
        _apply_machine_recul_1(state, int(rm), int(mt))


# ---------------------------------------------------------------------------
# G3:A — La Voltige de l'Atèle (DEPLACEMENT DEFENSEUR adjacent + lisière)
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

    for r_idx in range(n):
        for p in range(1, p_max + 1):
            if (
                state.get_furtivite_total_defs(r_idx, p) >= 1
                and _has_tracked_defender_furtivite(state, r_idx, p)
            ):
                p_dst = state.first_non_razed_from_border(r_idx) if p == 1 else p
                if p_dst is not None and not state.is_route_forestiere(r_idx, p_dst):
                    moves.append((("FURTIVITE", r_idx, p), (r_idx, p_dst)))

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
    """Déplace 1 Défenseur (Forêt, Furtivité ou constructeur en lisière) vers une parcelle adjacente."""
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
# G4:A — Le Cri d'Alarme de l'Ara (MOD_SEUIL + SACRIFICE 3.2)
# ---------------------------------------------------------------------------


def _targeted_parcels_after_revelation(state: GameState) -> list[tuple[int, int]]:
    targeted: list[tuple[int, int]] = []
    n = state.cfg.n_players

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            _, _, attacked = state.get_machine_turn_stats(r, mt)
            if (
                st == MACHINE_STATUS_RATISSAGE
                and pos > 0
                and not attacked
                and not state.is_route_forestiere(r, pos)
                and (r, pos) not in targeted
            ):
                targeted.append((r, pos))

    for s in range(n):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and bound_t in TACTIQUES_SPEC:
            rm, mt = (card - 1) // 2, (card - 1) % 2
            pos, st, _ = state.get_machine_pos_status(rm, mt)
            _, _, attacked = state.get_machine_turn_stats(rm, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not attacked:
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
            if (
                state.get_furtivite_total_defs(r, p) >= 1
                and _has_tracked_defender_furtivite(state, r, p)
            ):
                sources.append(("FURTIVITE", r, p))

    moves: list[tuple[tuple[str, int, int], tuple[int, int]]] = []
    for src in sources:
        for dst_r, dst_p in targeted_parcels:
            if src == ("FORET", dst_r, dst_p):
                continue
            moves.append((src, (dst_r, dst_p)))
    return moves


@register_tile(
    "G4",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_3_2_APRES_REVELATION, HOOK_EFFECT_RESUME),
)
def g4_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Ouverture : -1 Seuil sur parcelle O ou M (cumulable). Sacrifice 3.2 : déplace jusqu'à 2 Déf."""
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
            _execute_defender_move(state, choice)
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
            _execute_defender_move(state, choice)


# ---------------------------------------------------------------------------
# G5:A — L'Affût de la Matamata (MOD_LOI_DU_COEUR temp 5, double-face 5.3)
# ---------------------------------------------------------------------------


def _unmarked_matamata_parcels(state: GameState) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(r, p) and not state.has_parcel_flag_turn(
                r, p, PFLAG_MATAMATA_MARK
            ):
                out.append((r, p))
    return out


@register_tile(
    "G5",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_SEUIL_PARADE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g5_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> bool | None:
    """Face 1 : marque 1 parcelle (-1 Seuil si >= 1 Souche). Face 2 : marque jusqu'à 2 parcelles."""
    gov = _gov(state, "R")

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx["face"])
        cands = _unmarked_matamata_parcels(state)
        if not cands:
            return None
        if face == 1:
            if len(cands) == 1:
                state.set_parcel_flag_turn(cands[0][0], cands[0][1], PFLAG_MATAMATA_MARK, True)
                return None
            push_effect_decision(
                state,
                gov,
                cands,
                {"effect_kind": "MOD_SEUIL_PARCELLE", "face": 1},
                slot_id="G5",
                profile="A",
                resume_tag="F1_MARK",
            )
            return None

        # Face 2 autonome : jusqu'à 2 parcelles non rasées
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
        if rtag == "F1_MARK":
            r_c, p_c = choice
            state.set_parcel_flag_turn(int(r_c), int(p_c), PFLAG_MATAMATA_MARK, True)
            return None
        if rtag == "F2_MARK":
            if choice == "PASSER":
                return None
            rem = int(ctx["payload"][0])
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

    if hook == HOOK_5_SEUIL_PARADE:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        if (
            state.has_parcel_flag_turn(ray, target_p, PFLAG_MATAMATA_MARK)
            and state.get_parcel_souches(ray, target_p) >= 1
        ):
            ctx["delta"] = int(ctx.get("delta", 0)) - 1
            return True
        return False

    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        active = state.has_parcel_flag_turn(ray, target_p, PFLAG_MATAMATA_MARK)
        if active:
            prim_mod_loi_du_coeur(state, "LOI_SOUCHES_REDUISENT_SEUIL", active=True)
        return active

    return None


# ---------------------------------------------------------------------------
# G6:A — L'Œil Double du Toucan (PERMUTATION_PISTE LECTURE_DE_M, double activation v5.5)
# ---------------------------------------------------------------------------


def _hands_already_bound_in_3_2(state: GameState) -> bool:
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and bound_t > 0:
            return True
    return False


def _shift_m_options(state: GameState, *, post_bind: bool) -> list[tuple[int, int]]:
    opts: list[tuple[int, int]] = []
    for s in range(state.cfg.n_players):
        card, _, _, lec_m, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and 1 <= lec_m <= 6:
            if post_bind and bound_t == 0:
                continue
            if lec_m > 1:
                opts.append((s, -1))
            if lec_m < 6:
                opts.append((s, 1))
    return opts


def _trigger_g6_a_shift(
    state: GameState, gov: int, *, post_bind: bool, remaining_prep: int = 0
) -> None:
    opts = _shift_m_options(state, post_bind=post_bind)
    if not opts:
        return
    if len(opts) == 1:
        prim_permutation_piste(
            state,
            "SHIFT_LECTURE_M",
            seat=opts[0][0],
            delta_m=opts[0][1],
            rebind_tactique=post_bind,
        )
        if remaining_prep > 0:
            _trigger_g6_a_shift(state, gov, post_bind=post_bind, remaining_prep=remaining_prep - 1)
        return
    push_effect_decision(
        state,
        gov,
        opts,
        {"effect_kind": "SHIFT_LECTURE_M"},
        slot_id="G6",
        profile="A",
        resume_tag="SHIFT_AFTER_BIND" if post_bind else "SHIFT_PRE_BIND",
        resume_payload=(remaining_prep,),
    )


@register_tile(
    "G6",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_3_2_REVELATION, HOOK_EFFECT_RESUME),
)
def g6_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """En 3.2, décale de -1 ou +1 rang la lecture du dé M d'un joueur (compatible double pari)."""
    gov = _gov(state, "O")

    if hook == HOOK_GARDIEN_OUVERTURE:
        if state.step < STEP_3_2_REVEAL or not state.paravents_ouverts:
            if not state.has_used_once_per_turn(G6_A_PREP_1_BIT):
                state.mark_used_once_per_turn(G6_A_PREP_1_BIT)
            else:
                state.mark_used_once_per_turn(G6_A_PREP_2_BIT)
            return
        if state.step == STEP_3_2_REVEAL:
            post_bind = _hands_already_bound_in_3_2(state)
            _trigger_g6_a_shift(state, gov, post_bind=post_bind, remaining_prep=0)
        return

    if hook == HOOK_3_2_REVELATION:
        prep_cnt = int(state.has_used_once_per_turn(G6_A_PREP_1_BIT)) + int(
            state.has_used_once_per_turn(G6_A_PREP_2_BIT)
        )
        if prep_cnt <= 0:
            return
        _trigger_g6_a_shift(state, gov, post_bind=False, remaining_prep=prep_cnt - 1)
        return

    if hook == HOOK_EFFECT_RESUME:
        rtag = str(ctx["resume_tag"])
        post_bind = rtag == "SHIFT_AFTER_BIND"
        s_id, d_m = ctx["choice"]
        prim_permutation_piste(
            state,
            "SHIFT_LECTURE_M",
            seat=int(s_id),
            delta_m=int(d_m),
            rebind_tactique=post_bind,
        )
        payload = ctx.get("payload", ())
        rem_prep = int(payload[0]) if payload else 0
        if rem_prep > 0:
            _trigger_g6_a_shift(state, gov, post_bind=post_bind, remaining_prep=rem_prep - 1)


# ---------------------------------------------------------------------------
# G7:A — Le Barrage du Capybara (CREATION_ENTITE PIEGE sur Souche)
# ---------------------------------------------------------------------------


@register_tile("G7", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g7_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
    """Pose 1 Piège sur toute parcelle non rasée avec >= 1 Souche et aucun Piège (light_trigger=False)."""
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
                state, "PIEGE", ray=cands[0][0], p=cands[0][1], light_trigger=False
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
                state, "PIEGE", ray=int(r_c), p=int(p_c), light_trigger=False
            )


# ---------------------------------------------------------------------------
# G8:A — Le Sillage du Boto (DEPLACEMENT CIBLAGE, double activation v5.5)
# ---------------------------------------------------------------------------


def _encode_g8_a_shift_slot(
    state: GameState, base_bit: int, ray: int, m_type: int, direction: int
) -> None:
    state.mark_used_once_per_turn(base_bit)
    for b in range(3):
        if ray & (1 << b):
            state.mark_used_once_per_turn(base_bit + 1 + b)
    if m_type == MACHINE_BULLDOZER:
        state.mark_used_once_per_turn(base_bit + 4)
    if direction > 0:
        state.mark_used_once_per_turn(base_bit + 5)


def _encode_g8_a_next_shift(state: GameState, ray: int, m_type: int, direction: int) -> None:
    if not state.has_used_once_per_turn(G8_A_SLOT1_BASE):
        _encode_g8_a_shift_slot(state, G8_A_SLOT1_BASE, ray, m_type, direction)
    elif not state.has_used_once_per_turn(G8_A_SLOT2_BASE):
        _encode_g8_a_shift_slot(state, G8_A_SLOT2_BASE, ray, m_type, direction)


def _decode_g8_a_shifts(state: GameState) -> list[tuple[int, int, bool]]:
    out: list[tuple[int, int, bool]] = []
    for base_bit in (G8_A_SLOT1_BASE, G8_A_SLOT2_BASE):
        if not state.has_used_once_per_turn(base_bit):
            continue
        ray = 0
        for b in range(3):
            if state.has_used_once_per_turn(base_bit + 1 + b):
                ray |= 1 << b
        m_type = (
            MACHINE_BULLDOZER
            if state.has_used_once_per_turn(base_bit + 4)
            else MACHINE_ABATTEUSE
        )
        towards_heart = state.has_used_once_per_turn(base_bit + 5)
        out.append((ray, m_type, towards_heart))
    return out


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


def _prompt_or_apply_g8_a(state: GameState, gov: int, *, remaining_prep: int = 0) -> None:
    if state.has_used_once_per_turn(G8_A_SLOT1_BASE) and state.has_used_once_per_turn(
        G8_A_SLOT2_BASE
    ):
        return
    opts = _g8_a_shift_options(state)
    if not opts:
        return
    if len(opts) == 1:
        _encode_g8_a_next_shift(state, opts[0][0], opts[0][1], opts[0][2])
        if remaining_prep > 0:
            _prompt_or_apply_g8_a(state, gov, remaining_prep=remaining_prep - 1)
        return
    push_effect_decision(
        state,
        gov,
        opts,
        {"effect_kind": "CIBLAGE_BOTO_G8A"},
        slot_id="G8",
        profile="A",
        resume_tag="SHIFT_STRIKES",
        resume_payload=(remaining_prep,),
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
    """Décale d'1 parcelle non rasée (-1 ou +1) toutes les frappes d'1 machine (compatible double pari)."""
    gov = _gov(state, "M")

    if hook == HOOK_GARDIEN_OUVERTURE:
        if state.step < STEP_3_2_REVEAL or not state.paravents_ouverts:
            if not state.has_used_once_per_turn(G8_A_PREP_1_BIT):
                state.mark_used_once_per_turn(G8_A_PREP_1_BIT)
            else:
                state.mark_used_once_per_turn(G8_A_PREP_2_BIT)
            return None
        _prompt_or_apply_g8_a(state, gov, remaining_prep=0)
        return None

    if hook == HOOK_3_2_APRES_REVELATION:
        prep_cnt = int(state.has_used_once_per_turn(G8_A_PREP_1_BIT)) + int(
            state.has_used_once_per_turn(G8_A_PREP_2_BIT)
        )
        if prep_cnt > 0:
            _prompt_or_apply_g8_a(state, gov, remaining_prep=prep_cnt - 1)
        return None

    if hook == HOOK_EFFECT_RESUME:
        r_c, mt_c, d_c = ctx["choice"]
        _encode_g8_a_next_shift(state, int(r_c), int(mt_c), int(d_c))
        payload = ctx.get("payload", ())
        rem_prep = int(payload[0]) if payload else 0
        if rem_prep > 0:
            _prompt_or_apply_g8_a(state, gov, remaining_prep=rem_prep - 1)
        return None

    if hook == HOOK_5_CIBLAGE_MACHINE:
        if bool(ctx.get("is_ratissage")):
            return False
        shifts = _decode_g8_a_shifts(state)
        if not shifts:
            return False
        ray = int(ctx["ray"])
        m_type = int(ctx["m_type"])
        applied = False
        cur_targets: list[tuple[str, int]] = list(ctx["targets"])
        for sel_r, sel_mt, towards_heart in shifts:
            if ray != sel_r or m_type != sel_mt:
                continue
            shifted_targets: list[tuple[str, int]] = []
            for c_type, base_p in cur_targets:
                shifted_p = (
                    state.next_non_razed_towards_heart(ray, base_p)
                    if towards_heart
                    else state.next_non_razed_towards_border(ray, base_p)
                )
                if shifted_p is not None and not state.is_route_forestiere(ray, shifted_p):
                    shifted_targets.append((c_type, shifted_p))
            cur_targets = shifted_targets
            applied = True
        if applied:
            ctx["targets"] = cur_targets
        return applied

    return None


# ---------------------------------------------------------------------------
# G9:A — Le Guet du Caïman Noir (CREATION_ENTITE SABOTAGE, double-face 5.3)
# ---------------------------------------------------------------------------


@register_tile("G9", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
def g9_a_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
    """Face 1 : +1 Sabotage permanent. Face 2 : +2 Sabotages permanents. Flip en 5.3 uniquement."""
    face = int(ctx["face"])
    if face == 1:
        prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=False)
        return
    prim_creation_entite(state, "SABOTAGE", count=2, light_trigger=False)


# ---------------------------------------------------------------------------
# G10:A — La Brume de la Dendrobate (neutralisé en v5.5 — en refonte post-baseline)
# ---------------------------------------------------------------------------


@register_tile("G10", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
def g10_a_handler(state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """Emplacement neutre dans le socle initial v5.5 (en attente de reconception post-baseline)."""
    _ = state


# ---------------------------------------------------------------------------
# G11:A — La Piquée de la Harpie (MOD_SEUIL / AUTO_PARADE, double-face 5.3)
# ---------------------------------------------------------------------------


@register_tile(
    "G11",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_5_LAW_QUERY, HOOK_EFFECT_RESUME),
)
def g11_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Face 1 : -1 Seuil (-2 si >= 2 Déf). Face 2 : pare auto 1 attaque sur parcelle >= 2 Déf."""
    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        return state.has_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE)

    if hook == HOOK_GARDIEN_OUVERTURE:
        face = int(ctx["face"])
        gov = _gov(state, "O")
        if face == 1:
            cands_f1: list[tuple[int, int]] = [
                (r, p)
                for r in range(state.cfg.n_players)
                for p in range(1, state.cfg.p_max + 1)
                if not state.is_route_forestiere(r, p)
            ]
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
            )
            return None

        # Face 2 autonome : exclure d'abord les parcelles déjà marquées (double activation v5.5)
        cands_f2 = [
            (r, p)
            for r in range(state.cfg.n_players)
            for p in range(1, state.cfg.p_max + 1)
            if not state.is_route_forestiere(r, p)
            and state.get_parcel_defenseurs(r, p) >= 2
            and not state.has_parcel_flag_turn(r, p, PFLAG_AUTO_PARADE_ONCE)
        ]
        if not cands_f2:
            cands_f2 = [
                (r, p)
                for r in range(state.cfg.n_players)
                for p in range(1, state.cfg.p_max + 1)
                if not state.is_route_forestiere(r, p)
                and not state.has_parcel_flag_turn(r, p, PFLAG_AUTO_PARADE_ONCE)
            ]
        if not cands_f2:
            return None
        if len(cands_f2) == 1:
            r0, p0 = cands_f2[0]
            state.set_parcel_flag_turn(r0, p0, PFLAG_AUTO_PARADE_ONCE, True)
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
        tag = str(ctx["resume_tag"])
        r_c, p_c = ctx["choice"]
        r_i, p_i = int(r_c), int(p_c)
        if tag == "F1_SEUIL":
            delta = -2 if state.get_parcel_defenseurs(r_i, p_i) >= 2 else -1
            prim_mod_seuil(state, delta, ray=r_i, p=p_i)
        elif tag == "F2_AUTO_PARADE":
            state.set_parcel_flag_turn(r_i, p_i, PFLAG_AUTO_PARADE_ONCE, True)
    return None


# ---------------------------------------------------------------------------
# G12:A — Le Chant de l'Ibijau (PERMUTATION_PISTE ADVANCE_REVE_LEFT)
# ---------------------------------------------------------------------------


@register_tile("G12", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g12_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Fait avancer d'1 rang vers la gauche une tuile Rêve de la Piste des Tactiques."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        cands = [
            r_idx
            for r_idx in range(1, TRACK_LEN)
            if is_reve_code(state.get_tactique_at_rank(r_idx))
            and any(not is_reve_code(state.get_tactique_at_rank(j)) for j in range(r_idx))
        ]
        if not cands:
            return None
        if len(cands) == 1:
            prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cands[0])
            return None
        push_effect_decision(
            state,
            _gov(state, "O"),
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
# G13:A — La Brèche du Tamanoir (CREATION_ENTITE INSECTE)
# ---------------------------------------------------------------------------


@register_tile("G13", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g13_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Pose 1 Insecte sur une parcelle non rasée portant >= 1 Défenseur."""
    if not state.cfg.has_insectes_peuple:
        return None
    if hook == HOOK_GARDIEN_OUVERTURE:
        n = state.cfg.n_players
        p_max = state.cfg.p_max
        cands: list[tuple[str, int, int]] = []
        for r in range(n):
            for p in range(1, p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 1:
                    cands.append(("FORET", r, p))
        if not cands:
            return None
        if len(cands) == 1:
            _, idx_a, p = cands[0]
            prim_creation_entite(
                state, "INSECTE", ray=idx_a, p=p, count=1, light_trigger=False
            )
            return None
        push_effect_decision(
            state,
            _gov(state, "M"),
            tuple(cands),
            {"effect_kind": "BRECHE_TAMANOIR_INSECTE"},
            slot_id="G13",
            profile="A",
            resume_tag="POSE_INSECTE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if isinstance(choice, tuple) and len(choice) == 3:
            loc, idx_a, p = str(choice[0]), int(choice[1]), int(choice[2])
            if loc == "FORET":
                prim_creation_entite(
                    state, "INSECTE", ray=idx_a, p=p, count=1, light_trigger=False
                )
    return None


# ---------------------------------------------------------------------------
# G14:A — L'Écaille du Téju (CREATION_ENTITE PIEGE avec coût Insecte)
# ---------------------------------------------------------------------------


def _g14_a_adjacent_untrapped_parcels(state: GameState, r: int, p: int) -> list[int]:
    out: list[int] = []
    if not state.is_route_forestiere(r, p) and state.get_parcel_piege(r, p) == PIEGE_AUCUN:
        out.append(p)
    p_b = state.next_non_razed_towards_border(r, p)
    if p_b is not None and state.get_parcel_piege(r, p_b) == PIEGE_AUCUN:
        out.append(p_b)
    p_h = state.next_non_razed_towards_heart(r, p)
    if p_h is not None and state.get_parcel_piege(r, p_h) == PIEGE_AUCUN:
        out.append(p_h)
    return out


@register_tile("G14", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g14_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Défausse 1 Insecte d'une parcelle Forêt -> pose 1 Piège sur elle ou une parcelle adjacente."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        cands: list[tuple[int, int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    for dst_p in _g14_a_adjacent_untrapped_parcels(state, r, p):
                        cands.append((r, p, dst_p))
        if not cands:
            return None
        push_effect_decision(
            state,
            _gov(state, "R"),
            ("PASSER", *cands),
            {"effect_kind": "ECAILLE_TEJU_CONVERSION_PIEGE"},
            slot_id="G14",
            profile="A",
            resume_tag="CONV_PIEGE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return None
        if isinstance(choice, tuple) and len(choice) == 3:
            r, src_p, dst_p = int(choice[0]), int(choice[1]), int(choice[2])
            cur_ins = state.get_parcel_insectes(r, src_p)
            if cur_ins >= 1 and state.get_parcel_piege(r, dst_p) == PIEGE_AUCUN:
                state.set_parcel_insectes(r, src_p, cur_ins - 1)
                prim_creation_entite(state, "PIEGE", ray=r, p=dst_p, light_trigger=False)
    return None


# ---------------------------------------------------------------------------
# G15:A — L'Envol du Batará Suiveur (DEPLACEMENT MIGRATION DIRECTE)
# ---------------------------------------------------------------------------


@register_tile("G15", "A", hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def g15_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Fait migrer immédiatement 1 Insecte de la roue vers une case 1..6 de Bug ou Colonie."""
    if not state.cfg.has_insectes_peuple:
        return None
    if hook == HOOK_GARDIEN_OUVERTURE:
        n = state.cfg.n_players
        p_max = state.cfg.p_max
        srcs: list[tuple[str, int, int]] = []
        for r in range(n):
            for p in range(1, p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    srcs.append(("FORET", r, p))
        for l_idx in range(n):
            for p in range(1, p_max + 1):
                if state.get_furtivite_insectes(l_idx, p) >= 1:
                    srcs.append(("FURTIVITE", l_idx, p))
        if not srcs:
            return None
        tracks: tuple[str, ...] = (
            ("BUG", "COLONIE") if state.cfg.nb_animaux_sauvages >= 1 else ("BUG",)
        )
        cands: list[tuple[str, int, int, str, int]] = []
        for loc, idx_a, p in srcs:
            for track in tracks:
                for c_num in range(1, TRACK_LEN + 1):
                    cands.append((loc, idx_a, p, track, c_num))
        push_effect_decision(
            state,
            _gov(state, "O"),
            tuple(cands),
            {"effect_kind": "BATARA_MIGRATION_DIRECTE"},
            slot_id="G15",
            profile="A",
            resume_tag="MIGRATION_DIRECTE",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if isinstance(choice, tuple) and len(choice) == 5:
            loc, idx_a, p, track, c_num = (
                str(choice[0]),
                int(choice[1]),
                int(choice[2]),
                str(choice[3]),
                int(choice[4]),
            )
            if loc == "FORET" and state.get_parcel_insectes(idx_a, p) >= 1:
                prim_deplacement(
                    state,
                    "INSECTE",
                    src_ray=idx_a,
                    src_p=p,
                    global_track=track,
                    global_case=c_num,
                    count=1,
                )
            elif loc == "FURTIVITE" and state.get_furtivite_insectes(idx_a, p) >= 1:
                prim_deplacement(
                    state,
                    "INSECTE",
                    src_lisiere=idx_a,
                    src_p=p,
                    global_track=track,
                    global_case=c_num,
                    count=1,
                )
    return None
