"""Catalogue stateless Canon 0 v6.2 — 15 Gardiens actifs (G1:A..G15:A).

Zéro état global mutable, zéro accès à `_buf`, zéro `import random`, 100 % stdlib PyPy 3.11.
Zéro dette mémoire (`mem_debt_score == 0`) : tous les effets agissent exclusivement
sur les pions et jetons physiques du plateau via les 7 Primitives Formelles.
"""

from __future__ import annotations

from typing import Any

from engine.effects.registry import register_tile
from engine.primitives import (
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    list_machines_targeting_parcel,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_puissance,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
)
from engine.state import (
    CALE_ECAILLE,
    CALE_NONE,
    CALE_SABOTAGE,
    DUEL_NONE,
    DUEL_TERRITOIRE_TENU,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    MAX_ECAILLES,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PLUME_CALME,
    PLUME_CHAUD,
    PLUME_KIND_RANK,
    PLUME_KIND_RAY,
    PLUME_NONE,
    STEP_3_2_REVEAL,
    SYNERGY_META,
    TRACK_LEN,
    GameState,
    is_reve_code,
    is_tactique_code,
    unpack_machine_card,
)

__all__ = ()


def _gov_for_slot(state: GameState, slot_id: str) -> int:
    peuple = SYNERGY_META[slot_id][1]
    seat = state.cfg.seat_of_peuple(peuple)
    return seat if seat is not None else state.coordonnateur


def _plume_ray(state: GameState) -> int | None:
    face, kind, idx, _ = state.get_oiseau_plume()
    if face != PLUME_NONE and kind == PLUME_KIND_RAY and 0 <= idx < state.cfg.n_players:
        return idx
    return None


def _all_plume_move_options(state: GameState) -> tuple[Any, ...]:
    opts: list[Any] = ["PASSER"]
    for face in (PLUME_CHAUD, PLUME_CALME):
        for r in range(state.cfg.n_players):
            opts.append((face, PLUME_KIND_RAY, r))
    for face in (PLUME_CHAUD, PLUME_CALME):
        for rk in range(TRACK_LEN):
            opts.append((face, PLUME_KIND_RANK, rk))
    return tuple(opts)


def _machines_with_red_tokens(
    state: GameState,
    *,
    only_ray: int | None = None,
    candidates: tuple[tuple[int, int], ...] | None = None,
) -> tuple[tuple[int, int], ...]:
    out: list[tuple[int, int]] = []
    if candidates is not None:
        pairs = candidates
    else:
        rays = (only_ray,) if only_ray is not None else tuple(range(state.cfg.n_players))
        pairs = tuple((r, mt) for r in rays for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER))
    for r, mt in pairs:
        pos, st, _ = state.get_machine_pos_status(r, mt)
        if st == MACHINE_STATUS_RETIRED or pos == 0:
            continue
        rouges, bleus = state.get_machine_tokens(r, mt)
        if rouges >= 1 and bleus < 15:
            out.append((r, mt))
    return tuple(out)


def _list_g3_moves(
    state: GameState,
    *,
    adjacent_only: bool,
    excluded_pawns: frozenset[tuple[int, int]],
) -> tuple[tuple[int, int, int, int], ...]:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    moves: list[tuple[int, int, int, int]] = []
    for sr in range(n):
        for p in range(1, p_max + 1):
            if state.is_route_forestiere(sr, p) or state.get_parcel_souches(sr, p) < 1:
                continue
            avail_pawns = [
                pw for pw in state.list_defenders_on_parcel(sr, p) if pw not in excluded_pawns
            ]
            if not avail_pawns:
                continue
            if adjacent_only:
                dst_rays = sorted({(sr - 1) % n, (sr + 1) % n} - {sr})
            else:
                dst_rays = [dr for dr in range(n) if dr != sr]
            for dr in dst_rays:
                if not state.is_route_forestiere(dr, p) and state.get_parcel_souches(dr, p) >= 1:
                    moves.append((sr, p, dr, p))
    return tuple(moves)


def _pick_unexcluded_pawn_on_parcel(
    state: GameState,
    ray: int,
    p: int,
    excluded_pawns: frozenset[tuple[int, int]],
) -> tuple[int, int] | None:
    for pw in state.list_defenders_on_parcel(ray, p):
        if pw not in excluded_pawns:
            return pw
    return None


def _g15_eligible_swap_pairs(state: GameState) -> tuple[tuple[int, int], ...]:
    n = state.cfg.n_players
    elig: list[tuple[int, int]] = []
    for s in range(n):
        if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
            continue
        card, _, _, lec_m, bound_t = state.get_player_hand(s)
        if not (1 <= card <= 2 * n):
            continue
        r, mt = unpack_machine_card(card)
        pos, st, _ = state.get_machine_pos_status(r, mt)
        _, _, attacked = state.get_machine_turn_stats(r, mt)
        if st != MACHINE_STATUS_NORMAL or pos == 0 or attacked:
            continue
        if is_tactique_code(bound_t):
            eff_rank = bound_t
        elif state.step == STEP_3_2_REVEAL and 1 <= lec_m <= TRACK_LEN:
            eff_rank = lec_m
        else:
            continue
        elig.append((s, eff_rank))

    pairs: list[tuple[int, int]] = []
    for i in range(len(elig)):
        sa, ra = elig[i]
        for j in range(i + 1, len(elig)):
            sb, rb = elig[j]
            if ra != rb:
                pairs.append((sa, sb))
    return tuple(pairs)


# ---------------------------------------------------------------------------
# G1 (M>R) — Le Bond du Jaguar
# ---------------------------------------------------------------------------


def _g1_finish_f2_flip(state: GameState, dst_r: int, dst_p: int) -> None:
    targeting = list_machines_targeting_parcel(state, dst_r, dst_p, mobile_only=False)
    red_cands = _machines_with_red_tokens(state, candidates=targeting)
    if not red_cands:
        return
    if len(red_cands) == 1:
        prim_mod_puissance(state, red_cands[0][0], red_cands[0][1], flip_rouge_to_bleu=1)
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G1"),
        red_cands,
        {"effect_kind": "G1_F2_FLIP_RED", "dst": (dst_r, dst_p)},
        slot_id="G1",
        profile="A",
        resume_tag="F2_FLIP",
    )


@register_tile("G1", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g1_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G1 (M>R) Le Bond du Jaguar :
    F1 : Déplacez 1 Défenseur en attente vers une parcelle ciblée des Mammifères ou des Reptiles.
    F2 : Déplacez 1 Défenseur en attente vers une parcelle ciblée, puis retournez 1 jeton rouge en bleu
         sur une machine qui la vise.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if tag == "MOVE":
            face, src_s, src_d = ctx["payload"]
            dst_r, dst_p = int(choice[0]), int(choice[1])
            prim_deplacement(
                state,
                "DEFENSEUR",
                src_seat=int(src_s),
                src_def_idx=int(src_d),
                dst_ray=dst_r,
                dst_p=dst_p,
            )
            if int(face) >= 2:
                _g1_finish_f2_flip(state, dst_r, dst_p)
        elif tag == "F2_FLIP":
            prim_mod_puissance(state, int(choice[0]), int(choice[1]), flip_rouge_to_bleu=1)
        return

    face = int(ctx.get("face", 1))
    waiting = state.list_available_waiting_defenders()
    if not waiting:
        return
    targets = list_targeted_parcels(state)
    if face == 1:
        allowed_rays = {
            s
            for s in (state.cfg.seat_of_peuple("M"), state.cfg.seat_of_peuple("R"))
            if s is not None
        }
        targets = tuple(rp for rp in targets if rp[0] in allowed_rays)
    if not targets:
        return

    src_s, src_d = waiting[0]
    if len(targets) == 1:
        dst_r, dst_p = targets[0]
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=src_s,
            src_def_idx=src_d,
            dst_ray=dst_r,
            dst_p=dst_p,
        )
        if face >= 2:
            _g1_finish_f2_flip(state, dst_r, dst_p)
        return

    push_effect_decision(
        state,
        _gov_for_slot(state, "G1"),
        targets,
        {"effect_kind": "G1_MOVE_WAITING", "face": face},
        slot_id="G1",
        profile="A",
        resume_tag="MOVE",
        resume_payload=(face, src_s, src_d),
    )


# ---------------------------------------------------------------------------
# G2 (R>M) — L'Étreinte de l'Anaconda
# ---------------------------------------------------------------------------


@register_tile("G2", "A", (HOOK_GARDIEN_OUVERTURE,))
def eff_g2_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G2 (R>M) L'Étreinte de l'Anaconda :
    F1 : Ajoutez 1 Sabotage au sac, ou 2 si le jeton Duel est sur Territoire tenu.
    F2 : Ajoutez 2 Sabotages au sac, ou 3 si le jeton Duel est sur Territoire tenu.
    """
    _ = hook_name
    face = int(ctx.get("face", 1))
    duel_st, _, _ = state.get_duel_state()
    bonus = 1 if duel_st == DUEL_TERRITOIRE_TENU else 0
    cnt = (2 if face >= 2 else 1) + bonus
    prim_creation_entite(state, "SABOTAGE", count=cnt, light_trigger=False)


# ---------------------------------------------------------------------------
# G3 (M>O) — La Voltige de l'Atèle
# ---------------------------------------------------------------------------


@register_tile("G3", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g3_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G3 (M>O) La Voltige de l'Atèle :
    F1 : Déplacez 1 Défenseur d'une parcelle à Souche vers la parcelle de même profondeur
         d'un rayon voisin portant aussi une Souche.
    F2 : Déplacez jusqu'à 2 Défenseurs entre parcelles à Souche de même profondeur sur toute la roue.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        face, step_i, excluded = ctx["payload"]
        sr, sp, dr, dp = int(choice[0]), int(choice[1]), int(choice[2]), int(choice[3])
        excl_set = frozenset(excluded)
        pawn = _pick_unexcluded_pawn_on_parcel(state, sr, sp, excl_set)
        if pawn is None:
            return
        prim_deplacement(
            state,
            "DEFENSEUR",
            src_seat=pawn[0],
            src_def_idx=pawn[1],
            dst_ray=dr,
            dst_p=dp,
        )
        if int(face) >= 2 and int(step_i) == 1:
            next_excl = excl_set | {pawn}
            moves2 = _list_g3_moves(state, adjacent_only=False, excluded_pawns=next_excl)
            if moves2:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G3"),
                    ("PASSER", *moves2),
                    {"effect_kind": "G3_VOLTIGE", "face": int(face), "step": 2},
                    slot_id="G3",
                    profile="A",
                    resume_tag="STEP",
                    resume_payload=(int(face), 2, tuple(sorted(next_excl))),
                )
        return

    face = int(ctx.get("face", 1))
    moves = _list_g3_moves(state, adjacent_only=(face == 1), excluded_pawns=frozenset())
    if not moves:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G3"),
        ("PASSER", *moves),
        {"effect_kind": "G3_VOLTIGE", "face": face, "step": 1},
        slot_id="G3",
        profile="A",
        resume_tag="STEP",
        resume_payload=(face, 1, ()),
    )


# ---------------------------------------------------------------------------
# G4 (O>M) — Le Cri d'Alarme de l'Ara
# ---------------------------------------------------------------------------


@register_tile("G4", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g4_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G4 (O>M) Le Cri d'Alarme de l'Ara :
    F1 : Un Gardien voisin de l'Ara glisse 1 de ses Défenseurs de pari dans une encoche
         (sans activer son effet ni incrémenter la Résonance).
    F2 : Chacun des deux Gardiens voisins de l'Ara glisse 1 de ses Défenseurs de pari dans une encoche.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        prim_partage_info_etat_gardien(
            state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=int(ctx["choice"])
        )
        return

    face = int(ctx.get("face", 1))
    case_ara = int(ctx.get("case", 1))
    neighbors = tuple(
        c
        for c in (case_ara - 1, case_ara + 1)
        if 1 <= c <= TRACK_LEN
        and state.get_gardien_at_case(c)[0] > 0
        and state.count_gardien_pari_defenders_at_case(c) >= 1
    )
    if not neighbors:
        return
    if face >= 2:
        for c in neighbors:
            prim_partage_info_etat_gardien(state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=c)
        return
    if len(neighbors) == 1:
        prim_partage_info_etat_gardien(state, "SLIDE_GARDIEN_PARI_ONLY", case_1_6=neighbors[0])
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G4"),
        neighbors,
        {"effect_kind": "G4_SLIDE_NEIGHBOR", "case": case_ara},
        slot_id="G4",
        profile="A",
        resume_tag="PICK_NEIGHBOR",
    )


# ---------------------------------------------------------------------------
# G5 (R>O) — Le Coup de Queue de l'Iguane
# ---------------------------------------------------------------------------


def _g5_prompt_f2_move_piege(state: GameState) -> None:
    targeted = list_targeted_parcels(state)
    dsts = [rp for rp in targeted if state.get_parcel_piege(rp[0], rp[1]) == PIEGE_AUCUN]
    if not dsts:
        return
    srcs: list[tuple[int, int]] = []
    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(r, p) and state.get_parcel_piege(r, p) == PIEGE_ACTIF:
                srcs.append((r, p))
    if not srcs:
        return
    moves = tuple(
        (sr, sp, dr, dp)
        for sr, sp in srcs
        for dr, dp in dsts
        if (sr, sp) != (dr, dp)
    )
    if not moves:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G5"),
        ("PASSER", *moves),
        {"effect_kind": "G5_F2_MOVE_PIEGE"},
        slot_id="G5",
        profile="A",
        resume_tag="MOVE_PIEGE",
    )


@register_tile("G5", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g5_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G5 (R>O) Le Coup de Queue de l'Iguane :
    F1 : Posez le Croc sur une parcelle ciblée du rayon Reptile ou du rayon marqué par la Plume de Vigie.
    F2 : Posez le Croc sur une parcelle ciblée, puis déplacez 1 Piège ordinaire vers une autre parcelle ciblée.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if tag == "PLACE_CROC":
            (face,) = ctx["payload"]
            if choice != "PASSER":
                prim_creation_entite(state, "CROC", ray=int(choice[0]), p=int(choice[1]))
            if int(face) >= 2:
                _g5_prompt_f2_move_piege(state)
        elif tag == "MOVE_PIEGE" and choice != "PASSER":
            prim_deplacement(
                state,
                "PIEGE",
                src_ray=int(choice[0]),
                src_p=int(choice[1]),
                dst_ray=int(choice[2]),
                dst_p=int(choice[3]),
            )
        return

    face = int(ctx.get("face", 1))
    targets = list_targeted_parcels(state)
    if face == 1:
        allowed_rays: set[int] = set()
        seat_r = state.cfg.seat_of_peuple("R")
        if seat_r is not None:
            allowed_rays.add(seat_r)
        p_ray = _plume_ray(state)
        if p_ray is not None:
            allowed_rays.add(p_ray)
        targets = tuple(rp for rp in targets if rp[0] in allowed_rays)

    if not targets:
        if face >= 2:
            _g5_prompt_f2_move_piege(state)
        return

    cur_croc = state.get_croc_parcel()
    if cur_croc is None and len(targets) == 1:
        prim_creation_entite(state, "CROC", ray=targets[0][0], p=targets[0][1])
        if face >= 2:
            _g5_prompt_f2_move_piege(state)
        return

    opts: tuple[Any, ...] = ("PASSER", *targets) if cur_croc is not None else targets
    push_effect_decision(
        state,
        _gov_for_slot(state, "G5"),
        opts,
        {"effect_kind": "G5_PLACE_CROC", "face": face},
        slot_id="G5",
        profile="A",
        resume_tag="PLACE_CROC",
        resume_payload=(face,),
    )


# ---------------------------------------------------------------------------
# G6 (O>R) — Le Bec du Toucan
# ---------------------------------------------------------------------------


@register_tile("G6", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g6_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G6 (O>R) Le Bec du Toucan :
    F1 : Sur le rayon marqué par la Plume de Vigie, retournez 1 jeton rouge d'une machine en bleu.
    F2 : Retournez sur leur face bleue jusqu'à 2 jetons rouges répartis sur 1 ou 2 machines.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        (rem_after,) = ctx["payload"]
        prim_mod_puissance(state, int(choice[0]), int(choice[1]), flip_rouge_to_bleu=1)
        if int(rem_after) >= 1:
            cands2 = _machines_with_red_tokens(state)
            if not cands2:
                return
            if len(cands2) == 1:
                prim_mod_puissance(state, cands2[0][0], cands2[0][1], flip_rouge_to_bleu=1)
                return
            push_effect_decision(
                state,
                _gov_for_slot(state, "G6"),
                cands2,
                {"effect_kind": "G6_FLIP_RED", "face": 2, "remaining": 1},
                slot_id="G6",
                profile="A",
                resume_tag="FLIP",
                resume_payload=(0,),
            )
        return

    face = int(ctx.get("face", 1))
    if face == 1:
        p_ray = _plume_ray(state)
        if p_ray is None:
            return
        cands = _machines_with_red_tokens(state, only_ray=p_ray)
        if not cands:
            return
        if len(cands) == 1:
            prim_mod_puissance(state, cands[0][0], cands[0][1], flip_rouge_to_bleu=1)
            return
        push_effect_decision(
            state,
            _gov_for_slot(state, "G6"),
            cands,
            {"effect_kind": "G6_FLIP_RED", "face": 1, "remaining": 1},
            slot_id="G6",
            profile="A",
            resume_tag="FLIP",
            resume_payload=(0,),
        )
        return

    # Face 2 : jusqu'à 2 jetons rouges retournés en bleu sur 1 ou 2 machines
    cands = _machines_with_red_tokens(state)
    if not cands:
        return
    if len(cands) == 1:
        prim_mod_puissance(state, cands[0][0], cands[0][1], flip_rouge_to_bleu=2)
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G6"),
        cands,
        {"effect_kind": "G6_FLIP_RED", "face": 2, "remaining": 2},
        slot_id="G6",
        profile="A",
        resume_tag="FLIP",
        resume_payload=(1,),
    )


# ---------------------------------------------------------------------------
# G7 (M>H) — Le Sentier du Tapir
# ---------------------------------------------------------------------------


@register_tile("G7", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g7_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G7 (M>H) Le Sentier du Tapir :
    F1 : Posez 1 Piège sur une parcelle ciblée portant au moins 1 Souche.
    F2 : Posez 1 Piège sur une parcelle ciblée à Souche, et 1 sur chaque parcelle ciblée
         bordée par une tuile enracinée (max 1 Piège ordinaire par parcelle, INV-17).
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        r_c, p_c = int(choice[0]), int(choice[1])
        if not state.is_route_forestiere(r_c, p_c) and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN:
            prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=False)
        return

    face = int(ctx.get("face", 1))
    targeted = list_targeted_parcels(state)
    if face >= 2:
        for r_t, p_t in targeted:
            if (
                state.is_parcel_bordered_by_rooted_tile(r_t, p_t)
                and state.get_parcel_piege(r_t, p_t) == PIEGE_AUCUN
            ):
                prim_creation_entite(state, "PIEGE", ray=r_t, p=p_t, light_trigger=False)

    souche_cands = tuple(
        (r_t, p_t)
        for r_t, p_t in targeted
        if state.get_parcel_souches(r_t, p_t) >= 1
        and state.get_parcel_piege(r_t, p_t) == PIEGE_AUCUN
    )
    if not souche_cands:
        return
    if len(souche_cands) == 1:
        prim_creation_entite(
            state, "PIEGE", ray=souche_cands[0][0], p=souche_cands[0][1], light_trigger=False
        )
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G7"),
        souche_cands,
        {"effect_kind": "G7_PIEGE_SOUCHE", "face": face},
        slot_id="G7",
        profile="A",
        resume_tag="PLACE_PIEGE",
    )


# ---------------------------------------------------------------------------
# G8 (M>E) — Le Mirage du Boto
# ---------------------------------------------------------------------------


def _g8_retreatable_machines(
    state: GameState,
    *,
    only_duel_targets: bool,
    excluded: frozenset[tuple[int, int]],
) -> tuple[tuple[int, int], ...]:
    if only_duel_targets:
        duel_st, dr, dp = state.get_duel_state()
        if duel_st == DUEL_NONE:
            return ()
        base = list_machines_targeting_parcel(state, dr, dp, mobile_only=True)
    else:
        base = tuple(
            (r, mt)
            for r in range(state.cfg.n_players)
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        )
    out: list[tuple[int, int]] = []
    for r, mt in base:
        if (r, mt) in excluded:
            continue
        pos, st, _ = state.get_machine_pos_status(r, mt)
        if st != MACHINE_STATUS_NORMAL or pos <= 0:
            continue
        if state.next_non_razed_towards_border(r, pos) is not None:
            out.append((r, mt))
    return tuple(out)


@register_tile("G8", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g8_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G8 (M>E) Le Mirage du Boto :
    F1 : Faites reculer d'1 parcelle une machine mobile qui vise la parcelle du jeton Duel.
    F2 : Faites reculer d'1 parcelle une machine mobile, ou deux si le Duel est sur Territoire tenu.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        face, rem_after, excluded = ctx["payload"]
        rm, mt = int(choice[0]), int(choice[1])
        pos, st, _ = state.get_machine_pos_status(rm, mt)
        if st == MACHINE_STATUS_NORMAL and pos > 0:
            p_back = state.next_non_razed_towards_border(rm, pos)
            if p_back is not None:
                prim_deplacement(
                    state, "MACHINE", src_ray=rm, m_type=mt, dst_ray=rm, dst_p=p_back
                )
        if int(rem_after) >= 1:
            next_excl = frozenset(excluded) | {(rm, mt)}
            cands2 = _g8_retreatable_machines(state, only_duel_targets=False, excluded=next_excl)
            if cands2:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G8"),
                    ("PASSER", *cands2),
                    {"effect_kind": "G8_RETREAT_MACHINE", "face": int(face), "step": 2},
                    slot_id="G8",
                    profile="A",
                    resume_tag="RETREAT",
                    resume_payload=(int(face), 0, tuple(sorted(next_excl))),
                )
        return

    face = int(ctx.get("face", 1))
    duel_st, _, _ = state.get_duel_state()
    cands = _g8_retreatable_machines(
        state, only_duel_targets=(face == 1), excluded=frozenset()
    )
    if not cands:
        return
    rem_after = 1 if (face >= 2 and duel_st == DUEL_TERRITOIRE_TENU) else 0
    push_effect_decision(
        state,
        _gov_for_slot(state, "G8"),
        ("PASSER", *cands),
        {"effect_kind": "G8_RETREAT_MACHINE", "face": face, "step": 1},
        slot_id="G8",
        profile="A",
        resume_tag="RETREAT",
        resume_payload=(face, rem_after, ()),
    )


# ---------------------------------------------------------------------------
# G9 (R>H) — Le Guet du Caïman noir
# ---------------------------------------------------------------------------


@register_tile("G9", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g9_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G9 (R>H) Le Guet du Caïman noir :
    F1 : Glissez sous une machine mobile 1 jeton Sabotage (annule sa prochaine avancée puis rejoint le sac).
    F2 : Glissez sous une machine mobile 1 jeton Écaille de la réserve Reptile (plafond 4, INV-20).
    """
    if hook_name == HOOK_EFFECT_RESUME:
        (cale_type,) = ctx["payload"]
        choice = ctx["choice"]
        prim_creation_entite(
            state,
            "CALE",
            ray=int(choice[0]),
            m_type=int(choice[1]),
            cale_type=int(cale_type),
            light_trigger=False,
        )
        return

    face = int(ctx.get("face", 1))
    cale_type = CALE_ECAILLE if face >= 2 else CALE_SABOTAGE
    if cale_type == CALE_ECAILLE and state.count_total_ecailles_in_play() >= MAX_ECAILLES:
        return
    cands = tuple(
        (r, mt)
        for r in range(state.cfg.n_players)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
        if state.get_machine_pos_status(r, mt)[1] == MACHINE_STATUS_NORMAL
        and state.get_machine_pos_status(r, mt)[0] > 0
        and state.get_machine_cale(r, mt) == CALE_NONE
    )
    if not cands:
        return
    if len(cands) == 1:
        prim_creation_entite(
            state,
            "CALE",
            ray=cands[0][0],
            m_type=cands[0][1],
            cale_type=cale_type,
            light_trigger=False,
        )
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G9"),
        cands,
        {"effect_kind": "G9_PLACE_CALE", "face": face, "cale_type": cale_type},
        slot_id="G9",
        profile="A",
        resume_tag="CALE",
        resume_payload=(cale_type,),
    )


# ---------------------------------------------------------------------------
# G10 (R>E) — L'Affût de la Matamata
# ---------------------------------------------------------------------------


@register_tile("G10", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g10_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G10 (R>E) L'Affût de la Matamata :
    F1 : Ajoutez 1 jeton Écaille de la réserve Reptile au sac (plafond 4, INV-20).
    F2 : Ajoutez 1 jeton Écaille au sac, puis altérez une machine mobile révélée.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        prim_creation_entite(
            state, "ALTERATION", ray=int(choice[0]), m_type=int(choice[1]), light_trigger=False
        )
        return

    face = int(ctx.get("face", 1))
    prim_creation_entite(state, "ECAILLE", count=1, light_trigger=False)
    if face < 2:
        return

    n = state.cfg.n_players
    revealed_mobile: list[tuple[int, int]] = []
    seen: set[tuple[int, int]] = set()
    for s in range(n):
        card = state.get_player_hand(s)[0]
        if 1 <= card <= 2 * n:
            r, mt = unpack_machine_card(card)
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if (
                st == MACHINE_STATUS_NORMAL
                and pos > 0
                and not state.has_machine_alteration(r, mt)
                and (r, mt) not in seen
            ):
                seen.add((r, mt))
                revealed_mobile.append((r, mt))
    if not revealed_mobile:
        return
    if len(revealed_mobile) == 1:
        prim_creation_entite(
            state,
            "ALTERATION",
            ray=revealed_mobile[0][0],
            m_type=revealed_mobile[0][1],
            light_trigger=False,
        )
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G10"),
        tuple(sorted(revealed_mobile)),
        {"effect_kind": "G10_F2_ALTER_REVEALED"},
        slot_id="G10",
        profile="A",
        resume_tag="ALTER",
    )


# ---------------------------------------------------------------------------
# G11 (O>H) — Le Piqué de la Harpie
# ---------------------------------------------------------------------------


def _g11_prompt_f2_plume(state: GameState) -> None:
    if not state.cfg.accessories_enabled:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G11"),
        _all_plume_move_options(state),
        {"effect_kind": "G11_F2_MOVE_PLUME"},
        slot_id="G11",
        profile="A",
        resume_tag="MOVE_PLUME",
    )


@register_tile("G11", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g11_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G11 (O>H) Le Piqué de la Harpie :
    F1 : Posez 1 Piège sur une parcelle ciblée du rayon marqué par la Plume de Vigie.
    F2 : Posez 1 Piège sur une parcelle ciblée de n'importe quel rayon, puis déplacez la Plume de Vigie.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if tag == "PIEGE":
            (face,) = ctx["payload"]
            r_c, p_c = int(choice[0]), int(choice[1])
            if not state.is_route_forestiere(r_c, p_c) and state.get_parcel_piege(r_c, p_c) == PIEGE_AUCUN:
                prim_creation_entite(state, "PIEGE", ray=r_c, p=p_c, light_trigger=False)
            if int(face) >= 2:
                _g11_prompt_f2_plume(state)
        elif tag == "MOVE_PLUME" and choice != "PASSER":
            locked = state.get_oiseau_plume()[3]
            state.set_oiseau_plume(
                int(choice[0]), int(choice[1]), int(choice[2]), locked=locked
            )
        return

    face = int(ctx.get("face", 1))
    targeted = list_targeted_parcels(state)
    if face == 1:
        p_ray = _plume_ray(state)
        if p_ray is None:
            return
        cands = tuple(
            (r, p)
            for r, p in targeted
            if r == p_ray and state.get_parcel_piege(r, p) == PIEGE_AUCUN
        )
    else:
        cands = tuple(
            (r, p) for r, p in targeted if state.get_parcel_piege(r, p) == PIEGE_AUCUN
        )

    if not cands:
        if face >= 2:
            _g11_prompt_f2_plume(state)
        return
    if len(cands) == 1:
        prim_creation_entite(
            state, "PIEGE", ray=cands[0][0], p=cands[0][1], light_trigger=False
        )
        if face >= 2:
            _g11_prompt_f2_plume(state)
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G11"),
        cands,
        {"effect_kind": "G11_PLACE_PIEGE", "face": face},
        slot_id="G11",
        profile="A",
        resume_tag="PIEGE",
        resume_payload=(face,),
    )


# ---------------------------------------------------------------------------
# G12 (O>E) — Le Chant de l'Ibijau
# ---------------------------------------------------------------------------


@register_tile("G12", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g12_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G12 (O>E) Le Chant de l'Ibijau :
    F1 : Faites glisser un Rêve d'1 rang vers la gauche (poussée de bloc contigu + Défenseurs, INV-15).
    F2 : Faites glisser un Rêve de 2 rangs vers la gauche.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        (steps,) = ctx["payload"]
        rk = int(choice)
        code = state.get_tactique_at_rank(rk)
        if not is_reve_code(code):
            return
        for _ in range(int(steps)):
            cur_rk = state.find_tactique_rank(code)
            if cur_rk is None or not prim_permutation_piste(
                state, "ADVANCE_REVE_LEFT", rank_a=cur_rk
            ):
                break
        return

    face = int(ctx.get("face", 1))
    steps = 2 if face >= 2 else 1
    slidable = tuple(
        rk
        for rk in range(TRACK_LEN)
        if is_reve_code(state.get_tactique_at_rank(rk))
        and state.get_reve_advance_dest_rank(rk) is not None
    )
    if not slidable:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G12"),
        ("PASSER", *slidable),
        {"effect_kind": "G12_SLIDE_REVE", "face": face, "steps": steps},
        slot_id="G12",
        profile="A",
        resume_tag="SLIDE",
        resume_payload=(steps,),
    )


# ---------------------------------------------------------------------------
# G13 (M>I) — La Langue du Tamanoir
# ---------------------------------------------------------------------------


def _g13_step1_options(state: GameState, *, same_ray: bool) -> tuple[tuple[int, int, int, int], ...]:
    targets = list_targeted_parcels(state)
    if not targets:
        return ()
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    srcs = [
        (r, p)
        for r in range(n)
        for p in range(1, p_max + 1)
        if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1
    ]
    out: list[tuple[int, int, int, int]] = []
    for dr, dp in targets:
        for sr, sp in srcs:
            if (sr, sp) == (dr, dp):
                continue
            if same_ray and sr != dr:
                continue
            out.append((sr, sp, dr, dp))
    return tuple(out)


@register_tile("G13", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g13_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G13 (M>I) La Langue du Tamanoir :
    F1 : Déplacez jusqu'à 2 Insectes d'un même rayon vers une parcelle ciblée de ce rayon.
    F2 : Déplacez jusqu'à 2 Insectes vers une parcelle ciblée, puis posez-y le jeton Duel face Défi.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if tag == "STEP1":
            (face,) = ctx["payload"]
            if choice == "PASSER":
                return
            sr, sp, dr, dp = int(choice[0]), int(choice[1]), int(choice[2]), int(choice[3])
            prim_deplacement(
                state, "INSECTE", src_ray=sr, src_p=sp, dst_ray=dr, dst_p=dp, count=1
            )
            # 2e Insecte optionnel vers la même parcelle ciblée (dr, dp)
            srcs2: list[tuple[int, int]] = []
            rays2 = (dr,) if int(face) == 1 else tuple(range(state.cfg.n_players))
            for r2 in rays2:
                for p2 in range(1, state.cfg.p_max + 1):
                    if (
                        (r2, p2) != (dr, dp)
                        and not state.is_route_forestiere(r2, p2)
                        and state.get_parcel_insectes(r2, p2) >= 1
                    ):
                        srcs2.append((r2, p2))
            if srcs2:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G13"),
                    ("PASSER", *srcs2),
                    {"effect_kind": "G13_MOVE_INS_2", "face": int(face), "dst": (dr, dp)},
                    slot_id="G13",
                    profile="A",
                    resume_tag="STEP2",
                    resume_payload=(int(face), dr, dp),
                )
            elif int(face) >= 2 and state.cfg.accessories_enabled:
                state.set_duel_defi(dr, dp)
        elif tag == "STEP2":
            face, dr, dp = ctx["payload"]
            if choice != "PASSER":
                prim_deplacement(
                    state,
                    "INSECTE",
                    src_ray=int(choice[0]),
                    src_p=int(choice[1]),
                    dst_ray=int(dr),
                    dst_p=int(dp),
                    count=1,
                )
            if int(face) >= 2 and state.cfg.accessories_enabled:
                state.set_duel_defi(int(dr), int(dp))
        elif tag == "DUEL_ONLY" and choice != "PASSER" and state.cfg.accessories_enabled:
            state.set_duel_defi(int(choice[0]), int(choice[1]))
        return

    face = int(ctx.get("face", 1))
    if not state.cfg.has_insectes_peuple:
        if face >= 2 and state.cfg.accessories_enabled:
            targets = list_targeted_parcels(state)
            if targets:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G13"),
                    ("PASSER", *targets),
                    {"effect_kind": "G13_F2_PLACE_DUEL_ONLY"},
                    slot_id="G13",
                    profile="A",
                    resume_tag="DUEL_ONLY",
                )
        return

    opts1 = _g13_step1_options(state, same_ray=(face == 1))
    if not opts1:
        if face >= 2 and state.cfg.accessories_enabled:
            targets = list_targeted_parcels(state)
            if targets:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G13"),
                    ("PASSER", *targets),
                    {"effect_kind": "G13_F2_PLACE_DUEL_ONLY"},
                    slot_id="G13",
                    profile="A",
                    resume_tag="DUEL_ONLY",
                )
        return

    push_effect_decision(
        state,
        _gov_for_slot(state, "G13"),
        ("PASSER", *opts1),
        {"effect_kind": "G13_MOVE_INS_1", "face": face},
        slot_id="G13",
        profile="A",
        resume_tag="STEP1",
        resume_payload=(face,),
    )


# ---------------------------------------------------------------------------
# G14 (R>I) — Le Terrier du Téju
# ---------------------------------------------------------------------------


@register_tile("G14", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g14_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G14 (R>I) Le Terrier du Téju :
    F1 : Défaussez 1 Insecte d'une parcelle pour poser 1 Piège sur cette parcelle ou une parcelle
         voisine de son rayon (saute les Routes Forestières / Pont routier).
    F2 : Défaussez 1 Insecte pour poser 1 Piège, ou le Croc, sur n'importe quelle parcelle ciblée.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        tag = str(ctx.get("resume_tag", ""))
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        if tag == "F1":
            sr, sp, dp = int(choice[0]), int(choice[1]), int(choice[2])
            cur = state.get_parcel_insectes(sr, sp)
            if cur >= 1 and not state.is_route_forestiere(sr, dp) and state.get_parcel_piege(sr, dp) == PIEGE_AUCUN:
                state.set_parcel_insectes(sr, sp, cur - 1)
                prim_creation_entite(state, "PIEGE", ray=sr, p=dp, light_trigger=False)
        elif tag == "F2_SRC":
            sr, sp = int(choice[0]), int(choice[1])
            targeted = list_targeted_parcels(state)
            dst_opts: list[tuple[str, int, int]] = []
            for dr, dp in targeted:
                if state.get_parcel_piege(dr, dp) == PIEGE_AUCUN:
                    dst_opts.append(("PIEGE", dr, dp))
                dst_opts.append(("CROC", dr, dp))
            if not dst_opts:
                return
            if len(dst_opts) == 1:
                kind_d, dr, dp = dst_opts[0]
                cur = state.get_parcel_insectes(sr, sp)
                if cur >= 1:
                    state.set_parcel_insectes(sr, sp, cur - 1)
                    prim_creation_entite(state, kind_d, ray=dr, p=dp, light_trigger=False)
                return
            push_effect_decision(
                state,
                _gov_for_slot(state, "G14"),
                tuple(dst_opts),
                {"effect_kind": "G14_F2_DST_TRAP_OR_CROC", "src": (sr, sp)},
                slot_id="G14",
                profile="A",
                resume_tag="F2_DST",
                resume_payload=(sr, sp),
            )
        elif tag == "F2_DST":
            sr, sp = ctx["payload"]
            kind_d, dr, dp = str(choice[0]), int(choice[1]), int(choice[2])
            cur = state.get_parcel_insectes(int(sr), int(sp))
            if cur >= 1 and not state.is_route_forestiere(dr, dp):
                if kind_d == "PIEGE" and state.get_parcel_piege(dr, dp) != PIEGE_AUCUN:
                    return
                state.set_parcel_insectes(int(sr), int(sp), cur - 1)
                prim_creation_entite(state, kind_d, ray=dr, p=dp, light_trigger=False)
        return

    if not state.cfg.has_insectes_peuple:
        return
    face = int(ctx.get("face", 1))
    n = state.cfg.n_players
    p_max = state.cfg.p_max

    if face == 1:
        f1_opts: list[tuple[int, int, int]] = []
        for sr in range(n):
            for sp in range(1, p_max + 1):
                if state.is_route_forestiere(sr, sp) or state.get_parcel_insectes(sr, sp) < 1:
                    continue
                nbrs: list[int] = [sp]
                p_back = state.next_non_razed_towards_border(sr, sp)
                if p_back is not None:
                    nbrs.append(p_back)
                p_fwd = state.next_non_razed_towards_heart(sr, sp)
                if p_fwd is not None:
                    nbrs.append(p_fwd)
                for dp in sorted(set(nbrs)):
                    if state.get_parcel_piege(sr, dp) == PIEGE_AUCUN:
                        f1_opts.append((sr, sp, dp))
        if not f1_opts:
            return
        push_effect_decision(
            state,
            _gov_for_slot(state, "G14"),
            ("PASSER", *f1_opts),
            {"effect_kind": "G14_F1_DISCARD_PIEGE"},
            slot_id="G14",
            profile="A",
            resume_tag="F1",
        )
        return

    # Face 2 : défausser 1 Insecte pour poser 1 Piège ou le Croc sur une parcelle ciblée
    targeted = list_targeted_parcels(state)
    if not targeted:
        return
    srcs = tuple(
        (r, p)
        for r in range(n)
        for p in range(1, p_max + 1)
        if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1
    )
    if not srcs:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G14"),
        ("PASSER", *srcs),
        {"effect_kind": "G14_F2_SRC_INSECT"},
        slot_id="G14",
        profile="A",
        resume_tag="F2_SRC",
    )


# ---------------------------------------------------------------------------
# G15 (O>I) — Le Va-et-vient du Colibri
# ---------------------------------------------------------------------------


@register_tile("G15", "A", (HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME))
def eff_g15_a(state: GameState, hook_name: str, ctx: dict[str, Any]) -> None:
    """G15 (O>I) Le Va-et-vient du Colibri :
    F1 : Échangez les rangs de deux machines révélées mobiles qui n'ont pas encore frappé.
    F2 : Échangez deux fois les rangs de deux machines révélées mobiles qui n'ont pas encore frappé.
    """
    if hook_name == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return
        face, step_i = ctx["payload"]
        prim_permutation_piste(
            state, "SWAP_MACHINE_RANKS", seat_a=int(choice[0]), seat_b=int(choice[1])
        )
        if int(face) >= 2 and int(step_i) == 1:
            pairs2 = _g15_eligible_swap_pairs(state)
            if pairs2:
                push_effect_decision(
                    state,
                    _gov_for_slot(state, "G15"),
                    ("PASSER", *pairs2),
                    {"effect_kind": "G15_SWAP_RANKS", "face": int(face), "step": 2},
                    slot_id="G15",
                    profile="A",
                    resume_tag="SWAP",
                    resume_payload=(int(face), 2),
                )
        return

    face = int(ctx.get("face", 1))
    pairs = _g15_eligible_swap_pairs(state)
    if not pairs:
        return
    push_effect_decision(
        state,
        _gov_for_slot(state, "G15"),
        ("PASSER", *pairs),
        {"effect_kind": "G15_SWAP_RANKS", "face": face, "step": 1},
        slot_id="G15",
        profile="A",
        resume_tag="SWAP",
        resume_payload=(face, 1),
    )
