"""Palier 3 — Lot 05 : Gardiens G13:A..G15:B & Migrations B/C (11 profils, clôture des 45 Gardiens)."""

from __future__ import annotations

from typing import Any

from engine.primitives import (
    HOOK_3_1_CONSTRUCTION,
    HOOK_3_2_REVELATION,
    HOOK_4_3_COLONIE_FIN,
    HOOK_5_CONTACT_NID,
    HOOK_5_LAW_QUERY,
    HOOK_6_2_AVANCEMENT,
    HOOK_EFFECT_RESUME,
    HOOK_GARDIEN_OUVERTURE,
    _record_phys_ops,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_loi_du_coeur,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
    register_tile,
)
from engine.state import (
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    TRACK_LEN,
    GameState,
)

__all__ = (
    "LOT_05_PROFILES",
    "bug_b_handler",
    "bug_c_handler",
    "colonie_c_handler",
    "g13_a_handler",
    "g13_b_handler",
    "g14_a_handler",
    "g14_b_handler",
    "g14_c_handler",
    "g14_d_handler",
    "g15_a_handler",
    "g15_b_handler",
)

LOT_05_PROFILES: tuple[tuple[str, str], ...] = (
    ("G13", "A"),
    ("G13", "B"),
    ("G14", "A"),
    ("G14", "B"),
    ("G14", "C"),
    ("G14", "D"),
    ("G15", "A"),
    ("G15", "B"),
    ("SLOT_BUG_CERVEAU", "B"),
    ("SLOT_BUG_CERVEAU", "C"),
    ("SLOT_COLONISATION_GARDIENS", "C"),
)


def _gov(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


# ---------------------------------------------------------------------------
# G13:A — La Brèche du Tamanoir (Mammifères) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile(
    "G13",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g13_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Pose 1 Insecte sur une parcelle non rasée ou case Furtivité avec >= 1 Défenseur (allume 6)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        n = state.cfg.n_players
        p_max = state.cfg.p_max
        cands: list[tuple[str, int, int]] = []
        for r in range(n):
            for p in range(1, p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_defenseurs(r, p) >= 1:
                    cands.append(("FORET", r, p))
        for l_idx in range(n):
            for p in range(1, p_max + 1):
                if (
                    state.get_furtivite_total_defs(l_idx, p) >= 1
                    and state.get_furtivite_insectes(l_idx, p) < 15
                ):
                    cands.append(("FURTIVITE", l_idx, p))
        if not cands:
            return None
        if len(cands) == 1:
            loc, idx_a, p = cands[0]
            if loc == "FORET":
                prim_creation_entite(state, "INSECTE", ray=idx_a, p=p, count=1, light_trigger=True)
            else:
                prim_creation_entite(
                    state, "INSECTE", lisiere=idx_a, p=p, count=1, light_trigger=True
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
                prim_creation_entite(state, "INSECTE", ray=idx_a, p=p, count=1, light_trigger=True)
            elif loc == "FURTIVITE":
                prim_creation_entite(
                    state, "INSECTE", lisiere=idx_a, p=p, count=1, light_trigger=True
                )
    return None


# ---------------------------------------------------------------------------
# G13:B — La Brèche du Tamanoir (Mammifères) : SIMPLE_CONTINU | LOI 3.1
# ---------------------------------------------------------------------------


@register_tile(
    "G13",
    "B",
    hooks=(HOOK_3_1_CONSTRUCTION, HOOK_EFFECT_RESUME),
)
def g13_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi 3.1 : construction en lisière avec 1 Défenseur + 1 Insecte de Furtivité de cette lisière."""
    if hook == HOOK_3_1_CONSTRUCTION:
        if not ctx.get("hybrid_pay"):
            return None
        prim_mod_loi_du_coeur(state, "LOI_CONSTRUCTION_HYBRIDE_INSECTE")
        l_idx = int(ctx["lisiere"])
        cands = [
            p
            for p in range(1, state.cfg.p_max + 1)
            if state.get_furtivite_insectes(l_idx, p) >= 1
        ]
        if not cands:
            return None
        if len(cands) == 1:
            p_sel = cands[0]
            cur_ins = state.get_furtivite_insectes(l_idx, p_sel)
            state.set_furtivite_insectes(l_idx, p_sel, cur_ins - 1)
            _record_phys_ops(state, 1)
            return None
        push_effect_decision(
            state,
            _gov(state, "M"),
            tuple(cands),
            {
                "effect_kind": "BRECHE_TAMANOIR_HYBRIDE_3_1",
                "lisiere": l_idx,
                "target_slot_id": ctx.get("target_slot_id", ""),
            },
            slot_id="G13",
            profile="B",
            resume_tag="HYBRIDE_3_1",
            resume_payload=(l_idx,),
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        p_sel = int(ctx["choice"])
        (l_idx,) = ctx["payload"]
        l_int = int(l_idx)
        cur_ins = state.get_furtivite_insectes(l_int, p_sel)
        if cur_ins >= 1:
            state.set_furtivite_insectes(l_int, p_sel, cur_ins - 1)
            _record_phys_ops(state, 1)
    return None


# ---------------------------------------------------------------------------
# G14:A — L'Écaille du Téju (Reptiles) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


def _g14_a_adjacent_untrapped_parcels(state: GameState, ray: int, p: int) -> list[int]:
    targets: list[int] = []
    if not state.is_route_forestiere(ray, p) and state.get_parcel_piege(ray, p) == PIEGE_AUCUN:
        targets.append(p)
    p_back = state.next_non_razed_towards_border(ray, p)
    if p_back is not None and state.get_parcel_piege(ray, p_back) == PIEGE_AUCUN:
        targets.append(p_back)
    p_fwd = state.next_non_razed_towards_heart(ray, p)
    if p_fwd is not None and state.get_parcel_piege(ray, p_fwd) == PIEGE_AUCUN:
        targets.append(p_fwd)
    return targets


@register_tile(
    "G14",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g14_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Défausse 1 Insecte d'une parcelle Forêt -> pose 1 Piège sur elle ou une parcelle adjacente (allume 2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        cands: list[tuple[int, int, int]] = []
        for r in range(state.cfg.n_players):
            for p in range(1, state.cfg.p_max + 1):
                if not state.is_route_forestiere(r, p) and state.get_parcel_insectes(r, p) >= 1:
                    for dst_p in _g14_a_adjacent_untrapped_parcels(state, r, p):
                        cands.append((r, p, dst_p))
        if not cands:
            return None
        opts = ("PASSER", *cands)
        push_effect_decision(
            state,
            _gov(state, "R"),
            opts,
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
                _record_phys_ops(state, 1)
                prim_creation_entite(state, "PIEGE", ray=r, p=dst_p, light_trigger=True)
    return None


# ---------------------------------------------------------------------------
# G14:B — L'Écaille du Téju (Reptiles) : SIMPLE_CONTINU | LOI DE CONTACT
# ---------------------------------------------------------------------------


@register_tile(
    "G14",
    "B",
    hooks=(HOOK_5_CONTACT_NID, HOOK_5_LAW_QUERY),
)
def g14_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Loi de contact : les Nids (M) de toute la roue et leurs Insectes sont préservés au contact machine."""
    if hook == HOOK_5_LAW_QUERY:
        ray = int(ctx["ray"])
        target_p = int(ctx["target_p"])
        return state.get_parcel_nid(ray, target_p)[0] > 0

    if hook == HOOK_5_CONTACT_NID:
        prim_mod_loi_du_coeur(state, "LOI_NID_INDESTRUCTIBLE_AU_CONTACT")
        ctx["protected"] = True
    return None


# ---------------------------------------------------------------------------
# G14:C — Le ventre plein (Reptiles) : DOUBLE_FACE_CYCLE | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile(
    "G14",
    "C",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g14_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Face 1 (À jeun) : défausse 1 Insecte chez R -> Rassasié ; Face 2 : pose 1 Piège chez R -> À jeun (allume 2)."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        case_num = int(ctx.get("case", 1))
        face = int(ctx.get("face", 1))
        r_seat = state.cfg.seat_of_peuple("R")
        if r_seat is None:
            return None

        if face == 1:
            cands_1 = [
                p
                for p in range(1, state.cfg.p_max + 1)
                if not state.is_route_forestiere(r_seat, p)
                and state.get_parcel_insectes(r_seat, p) >= 1
            ]
            if not cands_1:
                return None
            if len(cands_1) == 1:
                p_sel = cands_1[0]
                cur_ins = state.get_parcel_insectes(r_seat, p_sel)
                state.set_parcel_insectes(r_seat, p_sel, cur_ins - 1)
                _record_phys_ops(state, 1)
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=2
                )
                return None
            push_effect_decision(
                state,
                r_seat,
                tuple(cands_1),
                {"effect_kind": "VENTRE_PLEIN_NOURRIR_F1", "ray": r_seat},
                slot_id="G14",
                profile="C",
                resume_tag="F1_NOURRIR",
                resume_payload=(case_num, r_seat),
            )
            return None

        # Face 2 (Rassasié) : pose 1 Piège sur une parcelle non rasée de R sans machine ni Piège -> À jeun
        cands_2 = [
            p
            for p in range(1, state.cfg.p_max + 1)
            if not state.is_route_forestiere(r_seat, p)
            and not state.machines_on_parcel(r_seat, p)
            and state.get_parcel_piege(r_seat, p) == PIEGE_AUCUN
        ]
        if not cands_2:
            return None
        if len(cands_2) == 1:
            p_sel = cands_2[0]
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=case_num, new_face=1
            )
            prim_creation_entite(state, "PIEGE", ray=r_seat, p=p_sel, light_trigger=True)
            return None
        push_effect_decision(
            state,
            r_seat,
            tuple(cands_2),
            {"effect_kind": "VENTRE_PLEIN_PIEGE_F2", "ray": r_seat},
            slot_id="G14",
            profile="C",
            resume_tag="F2_PIEGE",
            resume_payload=(case_num, r_seat),
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        tag = str(ctx["resume_tag"])
        p_sel = int(ctx["choice"])
        case_num, r_seat = ctx["payload"]
        c_int, r_int = int(case_num), int(r_seat)
        if tag == "F1_NOURRIR":
            cur_ins = state.get_parcel_insectes(r_int, p_sel)
            if cur_ins >= 1:
                state.set_parcel_insectes(r_int, p_sel, cur_ins - 1)
                _record_phys_ops(state, 1)
                prim_partage_info_etat_gardien(
                    state, "FLIP_GARDIEN_FACE", case_1_6=c_int, new_face=2
                )
        elif tag == "F2_PIEGE" and state.get_parcel_piege(r_int, p_sel) == PIEGE_AUCUN:
            prim_partage_info_etat_gardien(
                state, "FLIP_GARDIEN_FACE", case_1_6=c_int, new_face=1
            )
            prim_creation_entite(state, "PIEGE", ray=r_int, p=p_sel, light_trigger=True)
    return None


# ---------------------------------------------------------------------------
# G14:D — Les porteurs du Téju (Reptiles) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile(
    "G14",
    "D",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g14_d_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Déplace 1 Insecte d'une parcelle de R ou I vers une autre parcelle piégée du même rayon."""
    if hook == HOOK_GARDIEN_OUVERTURE:
        rays: list[int] = []
        for code in ("R", "I"):
            s = state.cfg.seat_of_peuple(code)
            if s is not None and s not in rays:
                rays.append(s)
        cands: list[tuple[int, int, int]] = []
        for r in rays:
            for src_p in range(1, state.cfg.p_max + 1):
                if (
                    not state.is_route_forestiere(r, src_p)
                    and state.get_parcel_insectes(r, src_p) >= 1
                ):
                    for dst_p in range(1, state.cfg.p_max + 1):
                        if (
                            dst_p != src_p
                            and not state.is_route_forestiere(r, dst_p)
                            and state.get_parcel_piege(r, dst_p) in (PIEGE_ACTIF, PIEGE_DECLENCHE)
                        ):
                            cands.append((r, src_p, dst_p))
        if not cands:
            return None
        opts = ("PASSER", *cands)
        push_effect_decision(
            state,
            _gov(state, "R"),
            opts,
            {"effect_kind": "PORTEURS_TEJU_DEPLACER_INSECTE"},
            slot_id="G14",
            profile="D",
            resume_tag="PORTEURS_TEJU",
        )
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = ctx["choice"]
        if choice == "PASSER":
            return None
        if isinstance(choice, tuple) and len(choice) == 3:
            r, src_p, dst_p = int(choice[0]), int(choice[1]), int(choice[2])
            if state.get_parcel_insectes(r, src_p) >= 1:
                prim_deplacement(
                    state,
                    "INSECTE",
                    src_ray=r,
                    src_p=src_p,
                    dst_ray=r,
                    dst_p=dst_p,
                    count=1,
                )
    return None


# ---------------------------------------------------------------------------
# G15:A — L'Envol du Batará Suiveur (Oiseaux) : SIMPLE_CONTINU | OUVERTURE
# ---------------------------------------------------------------------------


@register_tile(
    "G15",
    "A",
    hooks=(HOOK_GARDIEN_OUVERTURE, HOOK_EFFECT_RESUME),
)
def g15_a_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Fait migrer immédiatement 1 Insecte de la roue vers une case 1..6 de Bug ou Colonie."""
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
        cands: list[tuple[str, int, int, str, int]] = []
        for loc, idx_a, p in srcs:
            for track in ("BUG", "COLONIE"):
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


# ---------------------------------------------------------------------------
# G15:B — L'Envol du Batará Suiveur (Oiseaux) : SIMPLE_CONTINU | LOI 4.3
# ---------------------------------------------------------------------------


@register_tile(
    "G15",
    "B",
    hooks=(HOOK_5_LAW_QUERY,),
)
def g15_b_handler(state: GameState, hook: str, _ctx: dict[str, Any]) -> Any:
    """Loi 4.3 : en 4.3, chaque Insecte sur la roue peut se déplacer de 0, 1 ou 2 crans."""
    if hook == HOOK_5_LAW_QUERY:
        prim_mod_loi_du_coeur(state, "LOI_AILES_ESSAIM_2_CRANS")
        return False
    return None


# ---------------------------------------------------------------------------
# SLOT_BUG_CERVEAU:B — Déviation Synaptique (Contrôle 3.2) : CONSOMME_ONESHOT | HOOK 3.2
# ---------------------------------------------------------------------------


def _bug_b_step_queue(state: GameState, start_seat: int) -> None:
    n = state.cfg.n_players
    for s in range(start_seat, n):
        card, _, _, lec_m, _ = state.get_player_hand(s)
        if not (1 <= card <= 12 and 1 <= lec_m <= TRACK_LEN):
            continue
        if state.get_bugs_at_case(lec_m) < 1:
            continue
        shifts: list[str] = ["PASSER"]
        if lec_m > 1:
            shifts.append("M_MOINS_1")
        if lec_m < TRACK_LEN:
            shifts.append("M_PLUS_1")
        gov_i = state.cfg.seat_of_peuple("I")
        decideur = gov_i if gov_i is not None else s
        push_effect_decision(
            state,
            decideur,
            tuple(shifts),
            {
                "effect_kind": "BUG_DEVIATION_SYNAPTIQUE_3_2",
                "target_seat": s,
                "case": lec_m,
            },
            slot_id="SLOT_BUG_CERVEAU",
            profile="B",
            resume_tag="DEVIATION_3_2",
            resume_payload=(s, lec_m),
        )
        return


@register_tile(
    "SLOT_BUG_CERVEAU",
    "B",
    hooks=(HOOK_3_2_REVELATION, HOOK_EFFECT_RESUME),
)
def bug_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """En 3.2, défausse 1 Insecte Bug du rang M d'un joueur pour décaler sa lecture M de +/-1."""
    if hook == HOOK_3_2_REVELATION:
        _bug_b_step_queue(state, 0)
        return None

    if hook == HOOK_EFFECT_RESUME:
        choice = str(ctx["choice"])
        seat, case_num = ctx["payload"]
        s_int, c_int = int(seat), int(case_num)
        if choice in ("M_MOINS_1", "M_PLUS_1"):
            bugs = state.get_bugs_at_case(c_int)
            if bugs >= 1:
                state.set_bugs_at_case(c_int, bugs - 1)
                _record_phys_ops(state, 1)
                delta = -1 if choice == "M_MOINS_1" else 1
                prim_permutation_piste(
                    state, "SHIFT_LECTURE_M", seat=s_int, delta_m=delta, rebind_tactique=False
                )
        _bug_b_step_queue(state, s_int + 1)
    return None


# ---------------------------------------------------------------------------
# SLOT_BUG_CERVEAU:C — La Cigale dans l'engrenage : PASSIF_CONTINU | LOI 6.2
# ---------------------------------------------------------------------------


@register_tile(
    "SLOT_BUG_CERVEAU",
    "C",
    hooks=(HOOK_6_2_AVANCEMENT,),
)
def bug_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Obsolète en v5.4.2 (piste T1..T6 fixe, Apprentissage supprimé) — no-op."""
    _ = (state, hook, ctx)
    return None


# ---------------------------------------------------------------------------
# SLOT_COLONISATION_GARDIENS:C — Les Lucioles : PASSIF_CONTINU | HOOK 4.3 FIN
# ---------------------------------------------------------------------------


@register_tile(
    "SLOT_COLONISATION_GARDIENS",
    "C",
    hooks=(HOOK_4_3_COLONIE_FIN,),
)
def colonie_c_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> list[tuple[str, int]]:
    """Fin 4.3 : chaque case avec >= 1 Insecte ouvre automatiquement son Gardien disponible sans défausse."""
    if hook == HOOK_4_3_COLONIE_FIN:
        start_case = int(ctx.get("start_case", 1))
        eligible: list[tuple[str, int]] = []
        for c in range(start_case, TRACK_LEN + 1):
            if state.get_colonie_at_case(c) >= 1:
                g_num, _, used = state.get_gardien_at_case(c)
                if g_num > 0 and not used:
                    eligible.append(("AUTO", c))
        return eligible
    return []
