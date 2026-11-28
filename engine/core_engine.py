"""Machine à états déterministe suspendable des 6 étapes (Socle canonique v6.4, 3+3 épuré, Enracinement Sentinelle & Mode 4)."""

from __future__ import annotations

from itertools import combinations
from typing import Any

from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    HOOK_1_3_LECTURE_DE,
    HOOK_2_1_DEBUT,
    HOOK_2_1_PORTEE_DEF1,
    HOOK_3_1_CONSTRUCTION,
    HOOK_3_2_APRES_DEVIATION,
    HOOK_3_2_APRES_REVELATION,
    HOOK_3_2_CALE_REVEAL,
    HOOK_3_2_ECAILLE_REVELEE,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_4_1_FURTIVITE,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_2_NID_AVANT_PROD,
    HOOK_5_3_PRE_RETRAIT,
    HOOK_5_APRES_PARADE_PIEGE,
    HOOK_5_BOURBIER_CHECK,
    HOOK_5_CIBLAGE_MACHINE,
    HOOK_5_DEBUT,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_5_ORDRE_RAYON,
    HOOK_5_PARADE_CLASSIQUE,
    HOOK_5_PARADE_HARPIE,
    HOOK_5_PARADE_JAGUAR,
    HOOK_5_PARADE_PONTE,
    HOOK_5_PARADE_SOLDATS,
    HOOK_5_SEUIL_PARADE,
    HOOK_5_TERRASSEMENT,
    HOOK_EFFECT_RESUME,
    HOOK_ENRACINEMENT,
    HOOK_REPOUSSE_FINALE,
    DecisionRequest,
    GameOver,
    _get_active_telemetry,
    _record_phys_ops,
    _set_active_telemetry,
    dispatch_hook,
    get_tile_registration,
    has_pending_decision,
    list_machines_targeting_parcel,
    list_targeted_parcels,
    prim_creation_entite,
    prim_deplacement,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_continuation_sequence,
    push_effect_decision,
    register_tile,
    verb_etouffer,
    verb_glisser_reve,
    verb_reculer,
    verb_refroidir,
    verb_semer_au_sac,
)
from engine.rng import SRC_DICE, roll_d6
from engine.state import (
    CALE_CAIMAN,
    CALE_NONE,
    CANONICAL_DOTATION,
    CARD_ECAILLE,
    CARD_NONE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_NONE,
    CHAMAN_TAMBOUR,
    DUEL_DEFI,
    DUEL_NONE,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    FAMILLE_CROISSANCE,
    FAMILLE_GARDIEN,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    GARDIEN_BET_CAP,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_N,
    MAX_P,
    NUM_SYNERGY_SLOTS,
    PERCHOIR_CALME,
    PERCHOIR_CHAUD,
    PERCHOIR_KIND_RANK,
    PERCHOIR_KIND_RAY,
    PERCHOIR_NONE,
    PEUPLE_TO_ID,
    PFLAG_AUTO_PARADE_ONCE,
    PFLAG_MATAMATA_MARK,
    PFLAG_SANCTUAIRE_SOUCHE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    RATISSAGE_TACTIQUE_SPEC,
    STEP_1_2_DEAL,
    STEP_1_3_DICE,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_5_1_TACTIQUES,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    STEP_6_1_ENRACINEMENT,
    STEP_6_2_EVOLUTION,
    STEP_6_3_END_TURN,
    STEP_GAME_OVER,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_REVE,
    TRIG_SABOTAGE,
    GameState,
    TactiqueSpec,
    code_to_tile_id,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    machine_card_code,
    machine_threat_key_3_2,
)

__all__ = (
    "DEC_BOUCLIER_LISIERE_5_3",
    "DEC_CHOIX_CASE_GARDIEN",
    "DEC_CHOIX_CIBLE_REVE_3_2",
    "DEC_DEPLOIEMENT_NID_4_2",
    "DEC_ENRACINEMENT_6_1",
    "DEC_HUMAIN_CHAMAN_2_1",
    "DEC_LIBERATION_BATISSEUR_3_1",
    "DEC_MAMMIFERE_DUEL_2",
    "DEC_OISEAU_CHOIX_DE_1_3",
    "DEC_OISEAU_PERCHOIR_1_1",
    "DEC_OISEAU_PERCHOIR_2",
    "DEC_OISEAU_PLUME_2",
    "DEC_ORDRE_ATTAQUE_5_1",
    "DEC_ORDRE_CONSTRUCTION_3_1",
    "DEC_ORDRE_NID_4_2",
    "DEC_ORDRE_RATISSAGE_5_2",
    "DEC_PLACEMENT_NID_3_1",
    "DEC_POSE_DEFENSEUR_1",
    "DEC_POSE_DEFENSEUR_2",
    "DEC_POSE_PIEGE_FURTIVITE_4_1",
    "DEC_REPTILE_POSE_CROC_3_2",
    "DEC_REVISION_DEFENSEUR_2",
    "DEC_SABOTAGE_CIBLE_3_2",
    "advance_step2_to_2_2",
    "apply_choice",
    "apply_mammifere_duel_choice",
    "apply_oiseau_plume_choice",
    "apply_repousse_finale",
    "apply_step2_def1",
    "apply_step2_def2",
    "clear_step2_pending_wait",
    "compute_parade_seuil",
    "ensure_builtin_migration_registered",
    "finish_step2_to_3_1",
    "insert_reve_on_track",
    "is_machine_active_this_turn",
    "is_tile_placeable",
    "list_legal_targets",
    "list_machines_targeting_parcel",
    "list_targeted_parcels",
    "lock_all_def2_in_place",
    "rebind_step_3_2_hand",
    "resolve_single_machine_attack",
    "step_until_decision",
    "sweep_gardiens",
)

# Types canoniques de DecisionRequest (socle v6.4 + accessoires 3+3 épurés + Enracinement Sentinelle)
DEC_OISEAU_PERCHOIR_1_1: str = "OISEAU_PERCHOIR_1_1"
DEC_OISEAU_CHOIX_DE_1_3: str = "OISEAU_CHOIX_DE_1_3"
DEC_HUMAIN_CHAMAN_2_1: str = "HUMAIN_CHAMAN_2_1"
DEC_MAMMIFERE_DUEL_2: str = "MAMMIFERE_DUEL_2"
DEC_OISEAU_PLUME_2: str = "OISEAU_PLUME_2"
DEC_OISEAU_PERCHOIR_2: str = DEC_OISEAU_PLUME_2
DEC_POSE_DEFENSEUR_1: str = "POSE_DEFENSEUR_1"
DEC_POSE_DEFENSEUR_2: str = "POSE_DEFENSEUR_2"
DEC_REVISION_DEFENSEUR_2: str = "REVISION_DEFENSEUR_2"
DEC_ORDRE_CONSTRUCTION_3_1: str = "ORDRE_CONSTRUCTION_3_1"
DEC_CHOIX_CASE_GARDIEN: str = "CHOIX_CASE_GARDIEN"
DEC_SABOTAGE_CIBLE_3_2: str = "SABOTAGE_CIBLE_3_2"
DEC_REPTILE_POSE_CROC_3_2: str = "REPTILE_POSE_CROC_3_2"
DEC_CHOIX_CIBLE_REVE_3_2: str = "CHOIX_CIBLE_REVE_3_2"
DEC_POSE_PIEGE_FURTIVITE_4_1: str = "POSE_PIEGE_FURTIVITE_4_1"
DEC_LIBERATION_BATISSEUR_3_1: str = "LIBERATION_BATISSEUR_3_1"
DEC_PLACEMENT_NID_3_1: str = "PLACEMENT_NID_3_1"
DEC_ORDRE_NID_4_2: str = "ORDRE_NID_4_2"
DEC_DEPLOIEMENT_NID_4_2: str = "DEPLOIEMENT_NID_4_2"
DEC_ORDRE_ATTAQUE_5_1: str = "ORDRE_ATTAQUE_TACTIQUE_5_1"
DEC_ORDRE_RATISSAGE_5_2: str = "ORDRE_RATISSAGE_5_2"
DEC_BOUCLIER_LISIERE_5_3: str = "BOUCLIER_LISIERE_5_3"
DEC_ENRACINEMENT_6_1: str = "ENRACINEMENT_6_1"


def _transition_step(state: GameState, new_step: int) -> None:
    prev_step = state.step
    if prev_step != new_step:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_step_transition(state, prev_step, new_step)
        state.step = new_step


# ---------------------------------------------------------------------------
# Règles natives Essaim v6.4 (Déviation ±1, Bouclier de lisière facultatif gouverné par I)
# ---------------------------------------------------------------------------


def _bug_b_step_queue(state: GameState, start_seat: int) -> None:
    if not state.cfg.has_insectes_peuple:
        return
    n = state.cfg.n_players
    for s in range(start_seat, n):
        if state.was_seat_altered_this_turn(s):
            continue
        card, _, _, lec_m, _ = state.get_player_hand(s)
        if not (1 <= card <= 12 and 1 <= lec_m <= TRACK_LEN):
            continue
        r, mt = (card - 1) // 2, (card - 1) % 2
        if state.is_machine_etouffee_this_turn(r, mt):
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


def _bug_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """Règle native Essaim v6.4 (INV-15/21) : en 3.2, défausse 1 Insecte du rang M pour décaler M de ±1."""
    if not state.cfg.has_insectes_peuple:
        return None
    if hook == HOOK_3_2_REVELATION:
        if ctx.get("phase") == "BUG_DEVIATIONS" or not ctx:
            _bug_b_step_queue(state, 0)
        return None
    if hook == HOOK_EFFECT_RESUME:
        choice = str(ctx["choice"])
        seat, case_num = ctx["payload"]
        s_int, c_int = int(seat), int(case_num)
        trk_b = _get_active_telemetry()
        if trk_b is not None:
            trk_b.on_bug_3_2_decision(choice)
        # Empiler la suite de la file AVANT sweep_gardiens pour préserver l'ordre chronologique
        push_continuation_sequence(state, (("BUG_B_CONTINUE_3_2", s_int + 1),))
        if choice in ("M_MOINS_1", "M_PLUS_1"):
            bugs = state.get_bugs_at_case(c_int)
            if bugs >= 1:
                state.set_bugs_at_case(c_int, bugs - 1)
                _record_phys_ops(state, 1)
                delta = -1 if choice == "M_MOINS_1" else 1
                prim_permutation_piste(
                    state, "SHIFT_LECTURE_M", seat=s_int, delta_m=delta, rebind_tactique=False
                )
                state.mark_seat_deviated_by_bug_this_turn(s_int)
                card, _, _, new_m, _ = state.get_player_hand(s_int)
                if 1 <= card <= 12 and state.cfg.mode >= 3:
                    r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                    dispatch_hook(
                        state,
                        HOOK_3_2_APRES_DEVIATION,
                        {
                            "seat": s_int,
                            "ray": r_m,
                            "m_type": mt_m,
                            "old_case": c_int,
                            "new_case": new_m,
                        },
                    )
                state.light_trigger(TRIG_INSECTE)
                if trk_b is not None:
                    trk_b.on_trigger_lit(TRIG_INSECTE)
                    trk_b.on_defense_bug_deviation(1)
                sweep_gardiens(state)
    return None


def _colonie_b_handler(_state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """SLOT_COLONISATION_GARDIENS.B (Bouclier de lisière facultatif v6.4) : résolu nativement en 5.3."""
    return


def ensure_builtin_migration_registered() -> None:
    """Garantit l'enregistrement des 2 slots Essaim scellés (Bug=B, Colonie=B) sur le bus."""
    if get_tile_registration("SLOT_BUG_CERVEAU", "B") is None:
        register_tile(
            "SLOT_BUG_CERVEAU", "B", hooks=(HOOK_3_2_REVELATION, HOOK_EFFECT_RESUME)
        )(_bug_b_handler)
    if get_tile_registration("SLOT_COLONISATION_GARDIENS", "B") is None:
        register_tile("SLOT_COLONISATION_GARDIENS", "B", hooks=())(_colonie_b_handler)


ensure_builtin_migration_registered()
__import__("engine.effects")


# ---------------------------------------------------------------------------
# Piste des Gardiens directe v6.4 (0 balayage, 0 reprise arrière, Résonance au dernier pari, INV-09)
# ---------------------------------------------------------------------------


def _sweep_gardiens_from(
    state: GameState,
    start_case: int,
    in_combat: bool,
    opened_total: int,
    resonance_fired: bool = False,
) -> int:
    """Résout directement les icônes allumées `start_case..5` (1 passage, sans reprise arrière),
    puis l'icône 6 (Résonance) au plus 1 fois pour cette vague si un dernier pari a glissé (INV-09).
    """
    for case_num in range(start_case, TRACK_LEN):
        if state.is_trigger_lit(case_num):
            state.clear_trigger(case_num)
            g_num, _ = state.get_gardien_at_case(case_num)
            if g_num > 0 and state.count_gardien_pari_defenders_at_case(case_num) >= 1:
                opened_total += 1
                resume_frame = (
                    "RESUME_SWEEP_GARDIENS",
                    case_num + 1,
                    1 if in_combat else 0,
                    opened_total,
                    1 if resonance_fired else 0,
                )
                push_continuation_sequence(state, (resume_frame,))
                prim_partage_info_etat_gardien(
                    state, "MARK_GARDIEN_OPENED", case_1_6=case_num
                )
                if state._continuation and state._continuation[0] == resume_frame:
                    state._continuation.pop(0)
                else:
                    return opened_total

    # Icône 6 (Résonance) : 1 seule activation par vague si au moins un dernier pari a été glissé
    if start_case <= TRIG_RESONANCE and not resonance_fired and state.is_trigger_lit(TRIG_RESONANCE):
        state.clear_trigger(TRIG_RESONANCE)
        resonance_fired = True
        g_num, _ = state.get_gardien_at_case(TRIG_RESONANCE)
        if g_num > 0 and state.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) >= 1:
            opened_total += 1
            resume_frame = (
                "RESUME_SWEEP_GARDIENS",
                TRIG_RESONANCE + 1,
                1 if in_combat else 0,
                opened_total,
                1,
            )
            push_continuation_sequence(state, (resume_frame,))
            prim_partage_info_etat_gardien(
                state, "MARK_GARDIEN_OPENED", case_1_6=TRIG_RESONANCE
            )
            if state._continuation and state._continuation[0] == resume_frame:
                state._continuation.pop(0)
            else:
                return opened_total

    state.triggers_lit = 0
    trk = _get_active_telemetry()
    if trk is not None:
        trk.on_gardien_sweep(
            state,
            repasses=0,
            opened=opened_total,
            in_combat=in_combat,
            opened_in_later_pass=0,
        )
    return opened_total


def sweep_gardiens(state: GameState, *, telemetry: Any | None = None) -> int:
    """Activation directe de l'icône allumée (1..5, sans reprise arrière) puis Résonance (6) 1 fois max (INV-09)."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        if state.cfg.mode == 1:
            state.triggers_lit = 0
            return 0
        if state.triggers_lit == 0:
            return 0
        in_combat = state.step in (STEP_5_1_TACTIQUES, STEP_5_2_RATISSAGE)
        return _sweep_gardiens_from(state, 1, in_combat, 0, False)
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


# ---------------------------------------------------------------------------
# Gouvernance & aides Étape 2 (Anti-blocage + Furtivité 4 slots + Ticks 1..3)
# ---------------------------------------------------------------------------


def _governor_for_peuple(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


# Tables immuables pré-allouées de cibles et d'options pour éviter ~2M d'allocations de tuples / 1k parties
_FORET_TARGETS: tuple[tuple[tuple[str, int, int], ...], ...] = tuple(
    tuple(("FORET", r, p) for p in range(MAX_P + 1)) for r in range(MAX_N)
)
_FURT_TARGETS: tuple[tuple[tuple[str, int, int], tuple[str, int, int]], ...] = tuple(
    (("FURTIVITE", r_idx, FURT_RIVE_PIEGE), ("FURTIVITE", r_idx, FURT_RIVE_SABOTAGE))
    for r_idx in range(MAX_N)
)
_LIS_TARGETS: tuple[tuple[str, int], ...] = tuple(
    ("LISIERE", slot_idx) for slot_idx in range(NUM_SYNERGY_SLOTS)
)
_GARDIEN_PARI_TARGETS: tuple[tuple[str, int], ...] = tuple(
    ("GARDIEN_PARI", case_c) for case_c in range(TRACK_LEN + 1)
)
_REVE_ACTIVATION_TARGETS: tuple[tuple[str, int], ...] = tuple(
    ("REVE_ACTIVATION", case_c) for case_c in range(TRACK_LEN + 1)
)
_ALL_CANONICAL_TARGETS: tuple[tuple[Any, ...], ...] = (
    tuple(t for row in _FORET_TARGETS for t in row[1:])
    + tuple(t for pair in _FURT_TARGETS for t in pair)
    + _LIS_TARGETS
    + _GARDIEN_PARI_TARGETS[1:]
    + _REVE_ACTIVATION_TARGETS[1:]
)
_DEF2_DEFINITIF_WRAP: dict[tuple[Any, ...], tuple[str, tuple[Any, ...]]] = {
    t: ("POSER_DEFINITIF", t) for t in _ALL_CANONICAL_TARGETS
}
_DEF2_REFLEXION_WRAP: dict[tuple[Any, ...], tuple[str, tuple[Any, ...]]] = {
    t: ("POSER_REFLEXION", t) for t in _ALL_CANONICAL_TARGETS
}
_RAYS_BY_N: tuple[tuple[int, ...], ...] = tuple(tuple(range(k)) for k in range(MAX_N + 1))
_LIS_SLOTS_BY_N: tuple[tuple[int, ...], ...] = tuple(
    tuple(range(2 * k)) for k in range(MAX_N + 1)
)
_DEF1_LOCAL_RANGES: dict[tuple[int, int], tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]] = {
    (n_val, s_val): (
        (s_val,),
        (s_val, (s_val - 1) % n_val),
        (s_val * 2, s_val * 2 + 1, ((s_val - 1) % n_val) * 2, ((s_val - 1) % n_val) * 2 + 1),
    )
    for n_val in range(3, MAX_N + 1)
    for s_val in range(n_val)
}
_STEP_2_1_CTX_BY_TOUR: tuple[dict[str, Any], ...] = tuple(
    {"tour": t, "step": "2.1"} for t in range(17)
)
_STEP_2_2_CTX_BY_TOUR: tuple[dict[str, Any], ...] = tuple(
    {"tour": t, "step": "2.2"} for t in range(17)
)


def _current_def_canonical_spot(state: GameState, seat: int, def_idx: int) -> tuple[Any, ...] | None:
    raw = state.get_player_def_loc_raw(seat, def_idx)
    if raw == 0:
        return None
    kind, a, b, c = state.decode_def_loc(raw)
    if kind == "FORET":
        return _FORET_TARGETS[a][b]
    if kind == "FURTIVITE":
        return _FURT_TARGETS[a][c // 2]
    if kind == "LISIERE":
        return _LIS_TARGETS[a]
    if kind == "GARDIEN_PARI":
        return _GARDIEN_PARI_TARGETS[a]
    if kind == "REVE_ACTIVATION":
        return _REVE_ACTIVATION_TARGETS[a]
    return None


def is_tile_placeable(state: GameState, slot_idx: int) -> bool:
    """Vrai si la tuile de lisière `slot_idx` possède au moins 1 emplacement légal sur le plateau (INV-19)."""
    if state.cfg.mode < 2 or not (0 <= slot_idx < 2 * state.cfg.n_players):
        return False
    tile_id = state.cfg.lisiere_slots[slot_idx]
    fam, _, _ = SYNERGY_META[tile_id]
    if fam == FAMILLE_GARDIEN:
        for c in range(1, TRACK_LEN + 1):
            if state.get_gardien_at_case(c)[0] == 0:
                return True
        return False
    if fam == FAMILLE_REVE:
        for i in range(TRACK_LEN):
            if not is_reve_code(state.get_tactique_at_rank(i)):
                return True
        return False
    if fam == FAMILLE_CROISSANCE:
        if not state.cfg.has_insectes_peuple:
            return False
        lisiere_idx = slot_idx // 2
        r0 = lisiere_idx
        r1 = (lisiere_idx + 1) % state.cfg.n_players
        for r in (r0, r1):
            for p in range(1, state.cfg.p_max + 1):
                if (
                    not state.is_route_forestiere(r, p)
                    and not state.machines_on_parcel(r, p)
                    and state.get_parcel_nid(r, p)[0] == 0
                ):
                    return True
        return False
    return False


def _list_legal_targets_impl(
    state: GameState,
    seat: int,
    *,
    is_first_defender: bool,
    exclude_own_def2: bool = False,
    force_global: bool = False,
) -> tuple[tuple[Any, ...], ...]:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    own_spot = _current_def_canonical_spot(state, seat, 1) if exclude_own_def2 else None

    use_global = force_global or (not is_first_defender)
    extra_targets: tuple[tuple[Any, ...], ...] = ()
    if is_first_defender and state.cfg.mode >= 3:
        portee_ctx: dict[str, Any] = {"seat": seat, "global_range": False, "extra_targets": []}
        dispatch_hook(state, HOOK_2_1_PORTEE_DEF1, portee_ctx)
        use_global = use_global or bool(portee_ctx.get("global_range"))
        extra_targets = tuple(portee_ctx.get("extra_targets", ()))

    all_rays = _RAYS_BY_N[n]
    # Humains (H) : le pion Tambour peut aussi être posé en 2.1 sur une parcelle de n'importe quel autre Peuple (INV-20)
    is_humain_tambour_2_1 = (
        is_first_defender
        and state.cfg.accessories_enabled
        and state.cfg.peuples[seat] == "H"
        and state.get_humain_chaman_archetype(0) in (CHAMAN_NONE, CHAMAN_TAMBOUR)
    )

    if not use_global:
        rays, _, lis_slots = _DEF1_LOCAL_RANGES[(n, seat)]
        if is_humain_tambour_2_1:
            rays = all_rays
    else:
        rays = all_rays
        lis_slots = _LIS_SLOTS_BY_N[n]

    targets: list[tuple[Any, ...]] = []

    # 1. Parcelles Forêt non rasées (rayon local en 2.1 ou tous les rayons si Tambour H / 2.2)
    for r in rays:
        f_row = _FORET_TARGETS[r]
        for p in range(1, p_max + 1):
            if not state.is_route_forestiere(r, p):
                targets.append(f_row[p])

    # 2. Tuiles de Synergie en lisière (interdit de compléter/poser une tuile impossible à placer, INV-19)
    if state.cfg.mode >= 2:
        for slot_idx in lis_slots:
            st, nb = state.get_lisiere_tile_state(slot_idx)
            cand_l = _LIS_TARGETS[slot_idx]
            if own_spot == cand_l:
                nb = max(0, nb - 1)
            if st == LISIERE_UNCONSTRUCTED and nb < 2 and is_tile_placeable(state, slot_idx):
                targets.append(cand_l)

    # 3. Furtivité v6.4 (« Chaud vs Calme » + Effet Sentinelle sur Rive Sabotage, INV-14)
    for r_idx in all_rays:
        if not state.is_ray_furtivite_open(r_idx):
            continue
        pair = _FURT_TARGETS[r_idx]
        for rv in (FURT_RIVE_PIEGE, FURT_RIVE_SABOTAGE):
            cap_rv = state.get_furtivite_rive_capacity(r_idx, rv)
            d_rv = state.get_furtivite_nb_def_rive(r_idx, 1, rv)
            if own_spot == pair[rv]:
                d_rv -= 1
            if d_rv < cap_rv:
                targets.append(pair[rv])

    # 4. Pari d'activation des Gardiens (réservé au 2e Défenseur en 2.2, Mode >= 2, >= 1 Animal Sauvage)
    if not is_first_defender and state.cfg.mode >= 2 and state.cfg.nb_animaux_sauvages >= 1:
        for c_num in range(1, TRACK_LEN + 1):
            g_num, _ = state.get_gardien_at_case(c_num)
            if g_num == 0:
                continue
            cand_pari = _GARDIEN_PARI_TARGETS[c_num]
            cnt_case = state.count_gardien_pari_defenders_at_case(c_num)
            if own_spot == cand_pari:
                cnt_case = max(0, cnt_case - 1)
            if cnt_case >= GARDIEN_BET_CAP:
                continue
            targets.append(cand_pari)

    # 5. Activation de Rêve sur la Réglette (ouverte en 2.1 ET en 2.2, Mode >= 2)
    if state.cfg.mode >= 2:
        for c_num in range(1, TRACK_LEN + 1):
            if is_reve_code(state.get_tactique_at_rank(c_num - 1)):
                targets.append(_REVE_ACTIVATION_TARGETS[c_num])

    if extra_targets and not use_global:
        for ext_t in extra_targets:
            if ext_t not in targets:
                targets.append(ext_t)

    # Repli 2.1 strict (INV-19) : UNIQUEMENT si le joueur n'a AUCUN coup légal au 1er temps de pose,
    # autorise la pose du 1er Défenseur sur une parcelle forêt d'un allié (sans jamais exposer GARDIEN_PARI).
    if not targets and is_first_defender and not use_global:
        for r in all_rays:
            f_row = _FORET_TARGETS[r]
            for p in range(1, p_max + 1):
                if not state.is_route_forestiere(r, p):
                    targets.append(f_row[p])

    return tuple(targets)


def list_legal_targets(
    state: GameState,
    seat: int,
    *,
    is_first_defender: bool,
    exclude_own_def2: bool = False,
) -> tuple[tuple[Any, ...], ...]:
    """Énumère toutes les poses légales (INV-19, Tambour H, zéro tuile inplaçable) pour un Défenseur de `seat`."""
    return _list_legal_targets_impl(
        state,
        seat,
        is_first_defender=is_first_defender,
        exclude_own_def2=exclude_own_def2,
    )


def _apply_defender_target(
    state: GameState, seat: int, def_idx: int, target: tuple[Any, ...], face: int
) -> None:
    kind = target[0]
    if kind == "FORET":
        _, r, p = target
        state.place_defender_foret(seat, def_idx, int(r), int(p), face)
        _record_phys_ops(state, 1)
    elif kind == "FURTIVITE":
        _, ray_idx, rive = target
        state.place_defender_furtivite(seat, def_idx, int(ray_idx), int(rive), face)
        _record_phys_ops(state, 1)
    elif kind == "LISIERE":
        _, slot_idx = target
        state.place_defender_lisiere_tile(seat, def_idx, int(slot_idx), face)
        _record_phys_ops(state, 1)
    elif kind == "GARDIEN_PARI":
        assert def_idx == 1, "Seul le 2e Défenseur peut cibler GARDIEN_PARI"
        _, case_c = target
        state.place_defender_gardien_pari(seat, int(case_c), face)
        _record_phys_ops(state, 1)
    elif kind == "REVE_ACTIVATION":
        _, case_c = target
        state.place_defender_reve_activation(seat, int(case_c), face, def_idx=def_idx)
        _record_phys_ops(state, 1)
    elif kind == "PASSER_IMPASSE":
        state.mark_defender_impasse(seat, def_idx, face)
        return
    else:
        raise ValueError(f"Cible Défenseur invalide : {target}")


def apply_mammifere_duel_choice(
    state: GameState, place_defi: bool, ray: int, p: int
) -> None:
    """Applique le choix du joueur Mammifère (M) de poser/déplacer le jeton Duel face DEFI sur (ray, p)."""
    if not state.cfg.accessories_enabled or state.cfg.seat_of_peuple("M") is None:
        return
    if place_defi and not state.is_route_forestiere(ray, p):
        state.set_duel_defi(ray, p)
        _record_phys_ops(state, 1)


def apply_oiseau_plume_choice(state: GameState, choice: Any) -> None:
    """Applique la pose ou l'ajustement du Perchoir de Vigie orientable par O ('PASSER' ou (face, kind, idx))."""
    if not state.cfg.accessories_enabled or state.cfg.seat_of_peuple("O") is None:
        return
    if choice == "PASSER" or choice is None:
        return
    face, kind, idx = choice
    state.set_oiseau_perchoir_signal(int(face), int(kind), int(idx), locked=False)
    _record_phys_ops(state, 1)


def _list_oiseau_plume_options(state: GameState) -> tuple[Any, ...]:
    opts: list[Any] = ["PASSER"]
    for face in (PERCHOIR_CHAUD, PERCHOIR_CALME):
        for r in range(state.cfg.n_players):
            opts.append((face, PERCHOIR_KIND_RAY, r))
        for k in range(TRACK_LEN):
            opts.append((face, PERCHOIR_KIND_RANK, k))
    return tuple(opts)


def clear_step2_pending_wait(state: GameState) -> None:
    """Purge une attente séquentielle 2.1/2.2 (y compris accessoires H/M/O) pour piloter l'Étape 2 en Ticks."""
    if not state._continuation or state._continuation[0][0] != "WAIT_DECISION":
        return
    req = state._continuation[0][1]
    if req.decision_type in (
        DEC_POSE_DEFENSEUR_1,
        DEC_POSE_DEFENSEUR_2,
        DEC_REVISION_DEFENSEUR_2,
        DEC_HUMAIN_CHAMAN_2_1,
        DEC_MAMMIFERE_DUEL_2,
        DEC_OISEAU_PLUME_2,
    ):
        state._continuation.pop(0)
        if state._continuation and state._continuation[0][0] in (
            "APPLY_DEF1",
            "APPLY_DEF2_INIT",
            "STEP2_REV_QUEUE",
            "APPLY_HUMAIN_CHAMAN_2_1",
            "APPLY_MAMMIFERE_DUEL_2",
            "APPLY_OISEAU_PLUME_2",
        ):
            state._continuation.pop(0)


def advance_step2_to_2_2(state: GameState, *, telemetry: Any | None = None) -> None:
    """Clôture proprement 2.1 pilotée par Ticks et ouvre 2.2."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        clear_step2_pending_wait(state)
        state.set_step2_pass_state(0, False)
        _transition_step(state, STEP_2_2_DEF2)
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


def finish_step2_to_3_1(state: GameState, *, telemetry: Any | None = None) -> None:
    """Verrouille simultanément tous les 2es Défenseurs en place et passe à l'Étape 3.1."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        clear_step2_pending_wait(state)
        lock_all_def2_in_place(state)
        _transition_step(state, STEP_3_1_CONSTRUCT)
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


def apply_step2_def1(
    state: GameState,
    seat: int,
    target: tuple[Any, ...],
    *,
    check_legal: bool = True,
    telemetry: Any | None = None,
) -> None:
    """API publique (bots & moteur) : pose le 1er Défenseur d'un siège sur face définitive."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        if check_legal:
            legal = list_legal_targets(state, seat, is_first_defender=True)
            if legal:
                assert target in legal, f"Cible 2.1 illégale pour siège {seat} : {target}"
        # Humains (H) : si appelé directement par un bot tick sans pré-choix explicite, déduit l'archétype du binôme
        if (
            state.cfg.accessories_enabled
            and state.cfg.peuples[seat] == "H"
            and state.get_humain_chaman_archetype(0) == CHAMAN_NONE
        ):
            if target[0] == "FORET" and int(target[1]) != seat:
                state.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
            elif target[0] == "REVE_ACTIVATION":
                state.set_humain_chaman_archetype(0, CHAMAN_CHANT)
            else:
                state.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
        _apply_defender_target(state, seat, 0, target, FACE_DEFINITIF)
        if telemetry is not None:
            telemetry.record_player_decision(state, seat)
        trk = _get_active_telemetry()
        if trk is not None:
            t_kind = str(target[0])
            trk.on_step2_def1_placed(t_kind)
            if t_kind in ("FORET", "LISIERE"):
                rays_loc, _, slots_loc = _DEF1_LOCAL_RANGES[(state.cfg.n_players, seat)]
                is_h_tambour = (
                    state.cfg.accessories_enabled
                    and state.cfg.peuples[seat] == "H"
                    and state.get_humain_chaman_archetype(0) == CHAMAN_TAMBOUR
                )
                out_of_local = (
                    (t_kind == "FORET" and int(target[1]) not in rays_loc and not is_h_tambour)
                    or (t_kind == "LISIERE" and int(target[1]) not in slots_loc)
                )
                if out_of_local and state.cfg.mode <= 2:
                    trk.ok_def1_global_fallback += 1
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


def apply_step2_def2(
    state: GameState,
    seat: int,
    action: tuple[str, Any],
    *,
    check_legal: bool = True,
    telemetry: Any | None = None,
) -> bool:
    """API publique (bots & moteur) : pose ou révise le 2e Défenseur d'un siège.

    Retourne True si un déplacement physique a eu lieu (utile pour le suivi des passes 2.2).
    """
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        act_type, target = action
        if act_type == "GARDER_REFLEXION":
            if telemetry is not None:
                telemetry.record_player_decision(state, seat)
            return False
        if act_type == "VERROUILLER_DEFINITIF":
            state.flip_defender2_to_definitif_in_place(seat)
            if state.cfg.accessories_enabled and state.cfg.peuples[seat] == "O":
                state.lock_oiseau_plume()
            _record_phys_ops(state, 1)
            if telemetry is not None:
                telemetry.record_player_decision(state, seat)
            return False

        face = (
            FACE_DEFINITIF
            if act_type in ("POSER_DEFINITIF", "DEPLACER_DEFINITIF")
            else FACE_REFLEXION
        )
        prev_spot = _current_def_canonical_spot(state, seat, 1)
        if check_legal:
            legal = list_legal_targets(state, seat, is_first_defender=False, exclude_own_def2=True)
            if legal:
                assert target in legal, f"Cible 2.2 illégale pour siège {seat} : {target}"
        _apply_defender_target(state, seat, 1, target, face)
        if face == FACE_DEFINITIF and state.cfg.accessories_enabled and state.cfg.peuples[seat] == "O":
            state.lock_oiseau_plume()
        if telemetry is not None:
            telemetry.record_player_decision(state, seat)
        moved = prev_spot != target
        if moved and prev_spot is not None:
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_step2_revision_moved()
        return moved
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


def lock_all_def2_in_place(state: GameState) -> None:
    """Retournement simultané sur place de tous les 2es Défenseurs encore en réflexion,
    figeant la Plume de Vigie (INV-03) et enregistrant toute tentative d'Éveil.
    """
    flipped = 0
    for s in range(state.cfg.n_players):
        if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s):
            state.flip_defender2_to_definitif_in_place(s)
            flipped += 1
    if state.cfg.accessories_enabled and state.cfg.seat_of_peuple("O") is not None:
        state.lock_oiseau_plume()
    if flipped > 0:
        _record_phys_ops(state, flipped)

    if not state.step2_locked:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_step2_locked_summary(state)
            if state.is_eveil_attempt_eligible():
                f1_bet = sum(
                    1
                    for c_i in range(1, TRACK_LEN + 1)
                    if state.get_gardien_at_case(c_i)[0] > 0
                    and state.get_gardien_at_case(c_i)[1] == 1
                    and state.count_gardien_pari_defenders_at_case(c_i) >= 1
                )
                if (
                    state.count_face2_gardiens_on_track() + f1_bet
                    >= state.cfg.nb_animaux_sauvages + 1
                ):
                    trk.on_reveil_attempt(state)

    state.step2_locked = True


# ---------------------------------------------------------------------------
# Étape 3.1 : Insertion d'un Rêve & Constructions obligatoires
# ---------------------------------------------------------------------------


def insert_reve_on_track(state: GameState, r_num: int) -> int | None:
    """Pose un Rêve construit par-dessus la case libre la plus à droite (6, puis 5, ...).
    Aucune Tactique n'est éjectée (piste fixe T1..T6 imprimée en dur).
    """
    assert 1 <= r_num <= 10
    target_idx: int | None = None
    for idx in range(TRACK_LEN - 1, -1, -1):
        if not is_reve_code(state.get_tactique_at_rank(idx)):
            target_idx = idx
            break
    assert target_idx is not None, "Aucune case libre sur la piste pour poser le Rêve"
    state.set_tactique_at_rank(target_idx, TILE_R_BASE + r_num)
    _record_phys_ops(state, 1)
    return None


def _tracked_builders_on_slot(state: GameState, slot_idx: int) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, _, _ = state.decode_def_loc(raw)
                if kind == "LISIERE" and a == slot_idx:
                    out.append((s, d))
    return out


def _send_slot_builders_to_waiting(state: GameState, slot_idx: int) -> None:
    """Couche tous les bâtisseurs restants de la tuile construite « en attente » devant leur propriétaire (INV-19)."""
    tracked = _tracked_builders_on_slot(state, slot_idx)
    for s, d in tracked:
        state.mark_defender_waiting(s, d)
    state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, 0)
    if tracked:
        _record_phys_ops(state, len(tracked))


def _valid_adjacent_first_parcels_3_1(
    state: GameState, slot_idx: int
) -> tuple[tuple[int, int], ...]:
    lisiere_idx = slot_idx // 2
    r0 = lisiere_idx
    r1 = (lisiere_idx + 1) % state.cfg.n_players
    valid_rays: list[tuple[int, int]] = []
    for r in (r0, r1):
        p_first = state.first_non_razed_from_border(r)
        if p_first is not None and (r, p_first) not in valid_rays:
            valid_rays.append((r, p_first))
    return tuple(valid_rays)


def _liberation_options_one(
    state: GameState, slot_idx: int
) -> tuple[tuple[int, int, int, int], ...]:
    """Options de libération d'1 bâtisseur : (b_seat, b_def_idx, ray, p_first)."""
    valid_rays = _valid_adjacent_first_parcels_3_1(state, slot_idx)
    if not valid_rays:
        return ()

    tracked = _tracked_builders_on_slot(state, slot_idx)
    opts: list[tuple[int, int, int, int]] = []
    if tracked:
        for b_seat, b_def in tracked:
            for r, p_first in valid_rays:
                opts.append((b_seat, b_def, r, p_first))
    else:
        _, nb = state.get_lisiere_tile_state(slot_idx)
        if nb >= 1:
            for r, p_first in valid_rays:
                opts.append((-1, 0, r, p_first))
    return tuple(opts)


def _apply_builder_liberation(state: GameState, slot_idx: int, choice: tuple[int, int, int, int]) -> None:
    b_seat, b_def, r, p_first = choice
    if b_seat >= 0:
        state.place_defender_foret(b_seat, b_def, r, p_first, FACE_DEFINITIF)
    else:
        st, nb = state.get_lisiere_tile_state(slot_idx)
        state.set_lisiere_tile_state(slot_idx, st, max(0, nb - 1))
        state.set_parcel_defenseurs(r, p_first, state.get_parcel_defenseurs(r, p_first) + 1)
    _record_phys_ops(state, 1)
    trk = _get_active_telemetry()
    if trk is not None and state.cfg.n_players == 3:
        trk.ok_liberation_batisseur_3j += 1


def rebind_step_3_2_hand(state: GameState, seat: int) -> None:
    """Recalcule la liaison Tactique d'un siège en 3.2 après modification de sa lecture M (ex: G6 A)."""
    card, d1, d2, lec_m, _ = state.get_player_hand(seat)
    if 1 <= card <= 12 and 1 <= lec_m <= 6:
        code_m = state.get_tactique_at_rank(lec_m - 1)
        if is_tactique_code(code_m):
            state.set_player_hand(seat, card, d1, d2, lec_m, code_m)
        else:
            state.set_player_hand(seat, card, d1, d2, lec_m, 0)


# ---------------------------------------------------------------------------
# Étape 4.1 & Étape 5 : Attaques d'un seul tenant, Parades, Accessoires & Routes
# ---------------------------------------------------------------------------


def is_machine_active_this_turn(state: GameState, ray: int, m_type: int) -> bool:
    """Vrai si la machine est en Ratissage ou activée par un jeton non Étouffé/non annulé en 3.2."""
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
        return False
    if state.is_machine_etouffee_this_turn(ray, m_type):
        return False
    if st == MACHINE_STATUS_RATISSAGE:
        return True
    target_card = machine_card_code(ray, m_type)
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if card == target_card and bound_t > 0:
            return True
    return False


def _effective_machine_power(state: GameState, ray: int, m_type: int) -> tuple[int, int]:
    rouges = state.get_machine_effective_rouges(ray, m_type)
    _, bleus = state.get_machine_tokens(ray, m_type)
    return rouges, bleus


def compute_parade_seuil(
    state: GameState,
    ray: int,
    m_type: int,
    target_p: int,
    tactique: TactiqueSpec,
    *,
    cible_type: str = "SUR_PLACE",
    is_ratissage: bool = False,
) -> int:
    """Calcule le Seuil de Parade effectif (plancher 1) pour une frappe sur (ray, target_p).

    Formule unifiée v6.4 (INV-11, P4_2233 = 2-2-3-3) :
    - Mode CHARGE (hors Ratissage) : seuls les jetons rouges sont ignorés (`rouges = 0`).
    - Jetons bleus Surchauffe (−1) : actifs dans TOUS les modes (Charge, Assaut, Ratissage).
    - Rangs 3 et 6 (`En avançant`) : −1 (`tactique.mod_seuil`).
    - Plancher : minimum 1.
    """
    base = CANONICAL_DOTATION[target_p - 1]
    is_charge = (not is_ratissage) and is_tactique_charge(tactique.code, state.tour)
    rouges, bleus = _effective_machine_power(state, ray, m_type)
    if is_charge:
        rouges = 0
    extra_mod = (
        state.get_global_mod_seuil_turn()
        + state.get_machine_seuil_mod_turn(ray, m_type)
        + state.get_parcel_seuil_mod_turn(ray, target_p)
    )
    if (
        state.has_parcel_flag_turn(ray, target_p, PFLAG_MATAMATA_MARK)
        and state.get_parcel_souches(ray, target_p) >= 1
    ):
        extra_mod -= 1

    ctx: dict[str, Any] = {
        "ray": ray,
        "m_type": m_type,
        "target_p": target_p,
        "tactique": tactique.tile_id,
        "cible_type": cible_type,
        "is_ratissage": is_ratissage,
        "is_charge": is_charge,
        "rouges": rouges,
        "bleus": bleus,
        "delta_seuil": 0,
    }
    dispatch_hook(state, HOOK_5_SEUIL_PARADE, ctx)
    raw = (
        base
        + int(ctx["rouges"])
        - int(ctx["bleus"])
        + tactique.mod_seuil
        + extra_mod
        + int(ctx["delta_seuil"])
    )
    return max(1, raw)


def _handle_route_creation(state: GameState, ray: int, razed_p: int) -> None:
    """Transforme (ray, razed_p) en Route Forestière (0/0), vide la case (INV-16) et applique le repli (INV-13)."""
    trk = _get_active_telemetry()
    if trk is not None:
        trk.ok_routes_created += 1
    ops = 0
    ins_here = state.get_parcel_insectes(ray, razed_p)
    m_num, _ = state.get_parcel_nid(ray, razed_p)
    if m_num > 0:
        state.clear_nid(m_num)  # Rend aussi l'éventuelle ponte G14 en réserve Reptile (INV-16)
        ops += 1
        l_slot = state.find_lisiere_slot_by_tile_id(f"M{m_num}")
        if l_slot is not None:
            state.set_lisiere_tile_state(l_slot, LISIERE_UNCONSTRUCTED, 0)
        if trk is not None:
            trk.ok_contact_nid_renvois += 1
            if ins_here > 0:
                trk.ok_contact_nid_insectes_perdus += ins_here

    if ins_here > 0:
        state.set_parcel_insectes(ray, razed_p, 0)
        ops += ins_here
    if state.get_parcel_piege(ray, razed_p) != PIEGE_AUCUN:
        state.set_parcel_piege(ray, razed_p, PIEGE_AUCUN)
        ops += 1
    # INV-16 : Croc et Duel sur la case rasée retournent en réserve
    if state.get_croc_parcel() == (ray, razed_p):
        state.clear_croc()
        ops += 1
    duel_st, duel_r, duel_p = state.get_duel_state()
    if duel_st != DUEL_NONE and duel_r == ray and duel_p == razed_p:
        state.clear_duel()
        ops += 1

    # Renvoyer en main d'éventuels Défenseurs restés sur la parcelle rasée
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, b, _ = state.decode_def_loc(raw)
                if kind == "FORET" and a == ray and b == razed_p:
                    state.remove_player_defender(s, d)
                    ops += 1
    state.set_parcel_defenseurs(ray, razed_p, 0)

    # Repli automatique des machines présentes sur (ray, razed_p) — zéro écrasement de Nid (INV-16)
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st, pending_s = state.get_machine_pos_status(ray, mt)
        if st == MACHINE_STATUS_RETIRED or pos != razed_p:
            continue
        p_back = state.next_non_razed_towards_border(ray, razed_p)
        if p_back is not None:
            state.set_machine_pos_status(ray, mt, p_back, st, pending_s)
            ops += 1
            if trk is not None:
                trk.ok_repli_bordure += 1
                if p_back < razed_p - 1:
                    trk.ok_pont_routier_jumps += 1
        else:
            p_fwd = state.next_non_razed_towards_heart(ray, razed_p)
            if p_fwd is not None:
                state.set_machine_pos_status(ray, mt, p_fwd, st, pending_s)
                # INV-13 : la poussée vers le cœur sur bordure rasée couvre l'avancée finale En avançant
                state.mark_machine_pushed_heart_this_turn(ray, mt)
                ops += 1
                if trk is not None:
                    trk.ok_repli_coeur_exception += 1
                    if p_fwd > razed_p + 1:
                        trk.ok_pont_routier_jumps += 1
            else:
                r_tok, b_tok = state.get_machine_tokens(ray, mt)
                state.set_machine_pos_status(ray, mt, 0, MACHINE_STATUS_RETIRED, False)
                state.set_machine_tokens(ray, mt, 0, 0)
                # Retrait définitif : retourne Altération & Cale G9 en réserve, purge passagers
                if state.has_machine_alteration(ray, mt):
                    state.set_machine_alteration(ray, mt, False)
                    ops += 1
                if state.get_machine_cale(ray, mt) != CALE_NONE:
                    state.set_machine_cale(ray, mt, CALE_NONE)
                    ops += 1
                p_ins = state.get_machine_passenger_insects(ray, mt)
                if p_ins > 0:
                    state.set_machine_passenger_insects(ray, mt, 0)
                    ops += p_ins
                ops += 1 + r_tok + b_tok
                if trk is not None:
                    trk.ok_retrait_definitif_machine += 1
    if ops > 0:
        _record_phys_ops(state, ops)


def _maybe_flip_duel_on_parade_or_trap(state: GameState, ray: int, target_p: int) -> None:
    """INV-20 v6.4 (Duel unifié) : toute frappe parée ou piégée par N'IMPORTE QUEL MOYEN
    (Défenseur, Insectes, Piège ordinaire, Croc, Soldats à glu, Ponte) sur la parcelle du Duel
    le retourne aussitôt sur `TERRITOIRE_TENU`.
    """
    if (
        not state.is_route_forestiere(ray, target_p)
        and state.get_duel_state() == (DUEL_DEFI, ray, target_p)
        and state.flip_duel_to_territoire_tenu()
    ):
        _record_phys_ops(state, 1)


def _clear_mobile_die_after_attack(state: GameState, ray: int, m_type: int) -> None:
    """INV-08 : retire immédiatement le dé d'une machine mobile de la Réglette sitôt son attaque terminée."""
    target_code = machine_card_code(ray, m_type)
    for s in range(state.cfg.n_players):
        card, d1, d2, lec_m, bound_t = state.get_player_hand(s)
        if card == target_code and bound_t != 0:
            state.set_player_hand(s, card, d1, d2, lec_m, 0)
            break


def _resolve_machine_targets_from(
    state: GameState,
    ray: int,
    m_type: int,
    tactique: TactiqueSpec,
    effective_ratissage: bool,
    targets: tuple[tuple[str, int], ...],
    start_idx: int,
    damaged_parcels: int,
    parried_strikes: int,
    executed_strikes: int,
    unparried_sur_place: int = 0,
    unparried_devant: int = 0,
    soldats_declined_idx: int = -1,
) -> None:
    trk = _get_active_telemetry()
    aborted_by_jaguar = False

    for t_idx in range(start_idx, len(targets)):
        c_type, target_p = targets[t_idx]
        # INV-13 : cibles figées au début de l'activation ; toute cible devenue Route entre-temps est annulée sans report
        if state.is_route_forestiere(ray, target_p):
            continue

        # Contrôle Bourbier (G7 Le Tapir) lorsqu'une frappe DEVANT franchit une Route Forestière intermédiaire
        if c_type == "DEVANT" and state.cfg.mode >= 3:
            cur_m_pos, _, _ = state.get_machine_pos_status(ray, m_type)
            if cur_m_pos > 0 and abs(target_p - cur_m_pos) > 1:
                brb_ctx: dict[str, Any] = {
                    "action": "DEVANT",
                    "ray": ray,
                    "m_type": m_type,
                    "origin_pos": cur_m_pos,
                    "target_p": target_p,
                    "cancelled": False,
                }
                dispatch_hook(state, HOOK_5_BOURBIER_CHECK, brb_ctx)
                if brb_ctx.get("cancelled"):
                    continue

        executed_strikes += 1
        if trk is not None:
            law_res = dispatch_hook(
                state,
                HOOK_5_LAW_QUERY,
                {
                    "ray": ray,
                    "m_type": m_type,
                    "target_p": target_p,
                    "cible_type": c_type,
                    "is_ratissage": effective_ratissage,
                    "tactique_code": tactique.code,
                },
            )
            trk.on_machine_strike(state, ray, sum(1 for x in law_res if x))

        # Maillon 1 : Bond du Jaguar (Mode 3+)
        jag_ctx: dict[str, Any] = {
            "ray": ray,
            "m_type": m_type,
            "target_p": target_p,
            "parried": False,
        }
        dispatch_hook(state, HOOK_5_PARADE_JAGUAR, jag_ctx)
        if jag_ctx.get("parried"):
            state.light_trigger(TRIG_PARADE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_PARADE)
                trk.on_defense_parade_classique(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            aborted_by_jaguar = True
            break

        # Maillon 2 : Piquée de la Harpie (Mode 3+ ou flag PFLAG_AUTO_PARADE_ONCE)
        if (
            state.has_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE)
            and state.get_parcel_defenseurs(ray, target_p) >= 2
        ):
            state.set_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE, False)
            state.light_trigger(TRIG_PARADE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_PARADE)
                trk.on_defense_parade_classique(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            continue

        har_ctx: dict[str, Any] = {
            "ray": ray,
            "m_type": m_type,
            "target_p": target_p,
            "parried": False,
        }
        dispatch_hook(state, HOOK_5_PARADE_HARPIE, har_ctx)
        if har_ctx.get("parried"):
            state.light_trigger(TRIG_PARADE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_PARADE)
                trk.on_defense_parade_classique(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            continue

        # Calcul de la Défense totale sur la parcelle à cet instant (inclut Insecte passager M1, INV-21)
        local_defs = state.get_parcel_defenseurs(ray, target_p)
        local_ins = state.get_parcel_insectes(ray, target_p)
        pass_ins = (
            state.get_machine_passenger_insects(ray, m_type)
            if state.cfg.has_insectes_peuple
            else 0
        )
        avail_ins = local_ins + pass_ins
        def_ctx: dict[str, Any] = {
            "ray": ray,
            "m_type": m_type,
            "target_p": target_p,
            "cible_type": c_type,
            "def_points": local_defs,
            "ins_points": avail_ins,
            "remote_support": 0,
        }
        dispatch_hook(state, HOOK_5_DEFENSE_PARCELLE, def_ctx)
        def_non_ins = int(def_ctx["def_points"]) + int(def_ctx["remote_support"])
        total_def = def_non_ins + int(def_ctx["ins_points"])

        # Maillon 3a-ponte : Éclosion de Ponte sous un Nid (G14 Le Téju, Croc éclot en priorité)
        nid_here, _ = state.get_parcel_nid(ray, target_p)
        if nid_here > 0 and state.get_nid_ponte(nid_here) and state.cfg.mode >= 3:
            ponte_ctx: dict[str, Any] = {
                "ray": ray,
                "m_type": m_type,
                "target_p": target_p,
                "m_num": nid_here,
                "hatched": False,
            }
            dispatch_hook(state, HOOK_5_PARADE_PONTE, ponte_ctx)
            if ponte_ctx.get("hatched"):
                if trk is not None:
                    trk.ok_pieges_triggered += 1
                state.light_trigger(TRIG_PIEGEAGE)
                if trk is not None:
                    trk.on_trigger_lit(TRIG_PIEGEAGE)
                    trk.on_defense_piege(1)
                _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
                parried_strikes += 1
                resume_f = (
                    "RESUME_MACHINE_ATTACK_5",
                    ray,
                    m_type,
                    tactique.code,
                    1 if effective_ratissage else 0,
                    targets,
                    t_idx + 1,
                    damaged_parcels,
                    parried_strikes,
                    executed_strikes,
                    unparried_sur_place,
                    unparried_devant,
                    -1,
                )
                push_continuation_sequence(state, (resume_f,))
                dispatch_hook(
                    state,
                    HOOK_5_APRES_PARADE_PIEGE,
                    {"ray": ray, "m_type": m_type, "target_p": target_p, "is_croc": True},
                )
                if state._continuation and state._continuation[0] == resume_f:
                    state._continuation.pop(0)
                else:
                    return
                continue

        # Maillon 3a : Croc Reptile prioritaire sur Piège ordinaire en cas de cohabitation (INV-17)
        if state.get_croc_parcel() == (ray, target_p):
            state.clear_croc()
            _record_phys_ops(state, 1)
            if trk is not None:
                trk.ok_pieges_triggered += 1
            state.light_trigger(TRIG_PIEGEAGE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_PIEGEAGE)
                trk.on_defense_piege(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            resume_f = (
                "RESUME_MACHINE_ATTACK_5",
                ray,
                m_type,
                tactique.code,
                1 if effective_ratissage else 0,
                targets,
                t_idx + 1,
                damaged_parcels,
                parried_strikes,
                executed_strikes,
                unparried_sur_place,
                unparried_devant,
                -1,
            )
            if state.cfg.mode >= 3:
                push_continuation_sequence(state, (resume_f,))
            dispatch_hook(
                state,
                HOOK_5_APRES_PARADE_PIEGE,
                {"ray": ray, "m_type": m_type, "target_p": target_p, "is_croc": True},
            )
            if state.cfg.mode >= 3:
                if state._continuation and state._continuation[0] == resume_f:
                    state._continuation.pop(0)
                else:
                    return
            continue

        # Maillon 3b : Piège ordinaire autonome SINGLE_STRIKE (allume 2. Piégeage, défaussé aussitôt, INV-17)
        piege_st = state.get_parcel_piege(ray, target_p)
        if piege_st == PIEGE_ACTIF:
            _record_phys_ops(state, 1)
            if trk is not None:
                trk.ok_pieges_triggered += 1
            state.set_parcel_piege(ray, target_p, PIEGE_AUCUN)
            state.light_trigger(TRIG_PIEGEAGE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_PIEGEAGE)
                trk.on_defense_piege(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            resume_f = (
                "RESUME_MACHINE_ATTACK_5",
                ray,
                m_type,
                tactique.code,
                1 if effective_ratissage else 0,
                targets,
                t_idx + 1,
                damaged_parcels,
                parried_strikes,
                executed_strikes,
                unparried_sur_place,
                unparried_devant,
                -1,
            )
            if state.cfg.mode >= 3:
                push_continuation_sequence(state, (resume_f,))
            dispatch_hook(
                state,
                HOOK_5_APRES_PARADE_PIEGE,
                {"ray": ray, "m_type": m_type, "target_p": target_p, "is_croc": False},
            )
            if state.cfg.mode >= 3:
                if state._continuation and state._continuation[0] == resume_f:
                    state._continuation.pop(0)
                else:
                    return
            continue

        # Maillon 4 : Parade classique & Soldats à glu (M2)
        # Partition stricte v6.4 : >= 1 Insecte défaussé -> 5. INSECTE ; sinon -> 1. PARADE.
        seuil = compute_parade_seuil(
            state,
            ray,
            m_type,
            target_p,
            tactique,
            cible_type=c_type,
            is_ratissage=effective_ratissage,
        )

        # Maillon 4a : Soldats à glu (M2) si présent sur la parcelle, >= 2 Insectes et utile (échec ou économie)
        if (
            nid_here == 2
            and local_ins >= 2
            and state.cfg.mode >= 3
            and t_idx != soldats_declined_idx
            and (total_def < seuil or (seuil - def_non_ins) > 2)
        ):
            soldats_resume = (
                "RESUME_MACHINE_ATTACK_5",
                ray,
                m_type,
                tactique.code,
                1 if effective_ratissage else 0,
                targets,
                t_idx,
                damaged_parcels,
                parried_strikes,
                executed_strikes - 1,
                unparried_sur_place,
                unparried_devant,
                t_idx,
            )
            soldats_ctx: dict[str, Any] = {
                "ray": ray,
                "m_type": m_type,
                "target_p": target_p,
                "seuil": seuil,
                "parried": False,
                "t_idx": t_idx,
                "resume_parried": (
                    "RESUME_MACHINE_ATTACK_5",
                    ray,
                    m_type,
                    tactique.code,
                    1 if effective_ratissage else 0,
                    targets,
                    t_idx + 1,
                    damaged_parcels,
                    parried_strikes + 1,
                    executed_strikes,
                    unparried_sur_place,
                    unparried_devant,
                    -1,
                ),
                "resume_declined": soldats_resume,
            }
            dispatch_hook(state, HOOK_5_PARADE_SOLDATS, soldats_ctx)
            if has_pending_decision(state):
                return
            if soldats_ctx.get("parried"):
                state.light_trigger(TRIG_INSECTE)
                if trk is not None:
                    trk.on_trigger_lit(TRIG_INSECTE)
                    trk.on_defense_parade_avec_insectes(1)
                _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
                parried_strikes += 1
                continue

        if total_def >= seuil:
            manque = max(0, seuil - def_non_ins)
            final_discard = 0
            if manque > 0:
                ins_to_discard = min(avail_ins, manque)
                pc_ctx: dict[str, Any] = {
                    "ray": ray,
                    "target_p": target_p,
                    "local_defs": local_defs,
                    "manque": manque,
                    "ins_to_discard": ins_to_discard,
                }
                dispatch_hook(state, HOOK_5_PARADE_CLASSIQUE, pc_ctx)
                final_discard = max(0, min(avail_ins, int(pc_ctx["ins_to_discard"])))
                if final_discard > 0:
                    used_pass = min(pass_ins, final_discard)
                    used_local = final_discard - used_pass
                    if used_pass > 0:
                        state.set_machine_passenger_insects(ray, m_type, pass_ins - used_pass)
                    if used_local > 0:
                        state.set_parcel_insectes(ray, target_p, local_ins - used_local)
                    _record_phys_ops(state, final_discard)
            if final_discard >= 1:
                state.light_trigger(TRIG_INSECTE)
                if trk is not None:
                    trk.on_trigger_lit(TRIG_INSECTE)
                    trk.on_defense_parade_avec_insectes(1)
            else:
                state.light_trigger(TRIG_PARADE)
                if trk is not None:
                    trk.on_trigger_lit(TRIG_PARADE)
                    trk.on_defense_parade_classique(1)
            _maybe_flip_duel_on_parade_or_trap(state, ray, target_p)
            parried_strikes += 1
            continue

        # Non parée et non piégée : renvoie le Duel présent sur cette parcelle en réserve (INV-20)
        if c_type == "SUR_PLACE":
            unparried_sur_place += 1
        else:
            unparried_devant += 1
        duel_st, duel_r, duel_p = state.get_duel_state()
        if (
            duel_st != DUEL_NONE
            and duel_r == ray
            and duel_p == target_p
            and not state.is_route_forestiere(ray, target_p)
        ):
            state.clear_duel()
            _record_phys_ops(state, 1)

        # Application des dégâts (INV-01 : Abatteuse coupe tous les Arbres sans toucher aux Souches ;
        # Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches)
        arbres_before = state.get_parcel_arbres(ray, target_p)
        souches_before = state.get_parcel_souches(ray, target_p)
        arbres_after = arbres_before
        souches_after = souches_before
        dmg_ops = 0

        if m_type == MACHINE_ABATTEUSE:
            if arbres_before > 0:
                cut = arbres_before
                arbres_after = 0
                souches_after += cut
                dmg_ops += cut
            elif effective_ratissage and souches_before > 0 and trk is not None:
                trk.ok_abatteuse_ratissage_0_arbre += 1
        else:
            cut = min(1, arbres_before)
            arbres_after -= cut
            souches_after += cut
            dmg_ops += cut
            default_prot = (
                1 if state.has_parcel_flag_turn(ray, target_p, PFLAG_SANCTUAIRE_SOUCHE) else 0
            )
            terr_ctx: dict[str, Any] = {
                "ray": ray,
                "target_p": target_p,
                "souches_after_cut": souches_after,
                "protected_souches": default_prot,
            }
            dispatch_hook(state, HOOK_5_TERRASSEMENT, terr_ctx)
            new_souches = min(souches_after, max(0, int(terr_ctx["protected_souches"])))
            dmg_ops += max(0, souches_after - new_souches)
            souches_after = new_souches

        state.set_parcel_arbres_souches(ray, target_p, arbres_after, souches_after)
        if dmg_ops > 0:
            _record_phys_ops(state, dmg_ops)
        if arbres_after < arbres_before or souches_after < souches_before:
            damaged_parcels += 1

        if arbres_after == 0 and souches_after == 0:
            _handle_route_creation(state, ray, target_p)

    all_parried = executed_strikes > 0 and parried_strikes == executed_strikes
    unparried_real_strikes = max(0, executed_strikes - parried_strikes)
    is_charge_atk = (not effective_ratissage) and is_tactique_charge(tactique.code, state.tour)
    fin_ctx: dict[str, Any] = {
        "ray": ray,
        "m_type": m_type,
        "tactique": tactique.tile_id,
        "tactique_code": tactique.code,
        "is_ratissage": effective_ratissage,
        "is_charge": is_charge_atk,
        "all_parried": all_parried,
        "damaged_parcels": damaged_parcels,
        "unparried_sur_place": unparried_sur_place,
        "unparried_devant": unparried_devant,
        "allow_advance": True,
        "reverse_advance": False,
        "allow_red_gain": True,
        "no_red_on_sur_place": False,
    }
    dispatch_hook(state, HOOK_5_FIN_ATTAQUE_MACHINE, fin_ctx)

    # 3. Avancée éventuelle (T3 / T6) — ou Recul inversé si R7 Curupira sur ce rang —
    #    hors Ratissage, NON déjà poussée par Route en bordure (INV-13), NON bloquée par Duel Territoire tenu (INV-20),
    #    avec contrôle Bourbier G7 si franchissement d'une Route Forestière.
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    reverse_adv = bool(fin_ctx.get("reverse_advance"))
    if (
        not aborted_by_jaguar
        and bool(fin_ctx["allow_advance"])
        and cur_st == MACHINE_STATUS_NORMAL
        and cur_pos > 0
        and tactique.avancee > 0
        and (reverse_adv or not state.was_machine_pushed_heart_this_turn(ray, m_type))
    ):
        for _ in range(tactique.avancee):
            cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
            if cur_st != MACHINE_STATUS_NORMAL or cur_pos == 0:
                break
            if reverse_adv:
                p_next = state.next_non_razed_towards_border(ray, cur_pos)
            else:
                # INV-20 : Duel face TERRITOIRE_TENU bloque l'avancée des machines présentes sur sa parcelle
                if state.is_duel_territoire_tenu_at(ray, cur_pos):
                    break
                p_next = state.next_non_razed_towards_heart(ray, cur_pos)
            if p_next is not None:
                if abs(p_next - cur_pos) > 1 and state.cfg.mode >= 3:
                    brb_adv: dict[str, Any] = {
                        "action": "ADVANCE",
                        "ray": ray,
                        "m_type": m_type,
                        "origin_pos": cur_pos,
                        "target_p": p_next,
                        "cancelled": False,
                    }
                    dispatch_hook(state, HOOK_5_BOURBIER_CHECK, brb_adv)
                    if brb_adv.get("cancelled"):
                        break
                if trk is not None and abs(p_next - cur_pos) > 1:
                    trk.ok_pont_routier_jumps += 1
                if reverse_adv:
                    verb_reculer(state, ray, m_type)
                else:
                    prim_deplacement(
                        state,
                        "MACHINE",
                        src_ray=ray,
                        m_type=m_type,
                        dst_ray=ray,
                        dst_p=p_next,
                    )

    # 4. Mode CHARGE (INV-11 : FRAPPE_NON_PAREE) : +1 jeton rouge max/activation dès qu'au moins 1 frappe
    #    sur parcelle réelle non-Route n'est ni parée ni piégée (R7 exclut les frappes SUR_PLACE).
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    if bool(fin_ctx.get("no_red_on_sur_place")):
        qualifies_charge_gain = unparried_devant >= 1
    else:
        qualifies_charge_gain = executed_strikes >= 1 and unparried_real_strikes >= 1
    gained_red = False
    if (
        is_charge_atk
        and qualifies_charge_gain
        and bool(fin_ctx["allow_red_gain"])
        and cur_st != MACHINE_STATUS_RETIRED
        and cur_pos > 0
    ):
        r_tok, b_tok = state.get_machine_tokens(ray, m_type)
        if r_tok < 15:
            state.set_machine_tokens(ray, m_type, r_tok + 1, b_tok)
            _record_phys_ops(state, 1)
            gained_red = True
            if trk is not None:
                trk.on_charge_gain(1, tour=state.tour)
    if is_charge_atk and trk is not None:
        trk.on_charge_activation_resolved(gained_red=gained_red, all_parried=all_parried)

    state.set_machine_turn_stats(ray, m_type, damaged_parcels, gained_red, True)
    # INV-08 : dé immédiatement retiré de la Réglette sitôt l'attaque mobile terminée
    if not effective_ratissage:
        _clear_mobile_die_after_attack(state, ray, m_type)

    # 5. Fin du bloc machine -> activation directe des Gardiens (INV-09)
    sweep_gardiens(state)


def resolve_single_machine_attack(
    state: GameState,
    ray: int,
    m_type: int,
    tactique: TactiqueSpec,
    *,
    is_ratissage: bool = False,
    telemetry: Any | None = None,
) -> None:
    """Résout une machine d'un seul tenant : cibles figées -> frappes -> avancée -> Charge -> Gardiens."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st == MACHINE_STATUS_RETIRED or pos == 0 or state.is_machine_etouffee_this_turn(ray, m_type):
            state.set_machine_turn_stats(ray, m_type, 0, False, True)
            if not is_ratissage:
                _clear_mobile_die_after_attack(state, ray, m_type)
            return

        effective_ratissage = is_ratissage or st == MACHINE_STATUS_RATISSAGE
        trk = _get_active_telemetry()
        if effective_ratissage and trk is not None:
            trk.ok_ratissage_activations += 1

        # 1. Cibles figées au début de l'activation depuis la position réelle (en sautant toute Route, INV-13)
        targets: list[tuple[str, int]] = []
        for c_type in tactique.cibles:
            if c_type == "SUR_PLACE":
                if not state.is_route_forestiere(ray, pos):
                    targets.append((c_type, pos))
            elif c_type == "DEVANT":
                p_dev = state.next_non_razed_towards_heart(ray, pos)
                if p_dev is not None:
                    if trk is not None and p_dev > pos + 1:
                        trk.ok_pont_routier_jumps += 1
                    targets.append((c_type, p_dev))
        if state.cfg.mode >= 3:
            cib_ctx: dict[str, Any] = {
                "ray": ray,
                "m_type": m_type,
                "pos": pos,
                "tactique": tactique.tile_id,
                "tactique_code": tactique.code,
                "is_ratissage": effective_ratissage,
                "targets": targets,
            }
            dispatch_hook(state, HOOK_5_CIBLAGE_MACHINE, cib_ctx)
            targets = list(cib_ctx["targets"])

        _resolve_machine_targets_from(
            state,
            ray,
            m_type,
            tactique,
            effective_ratissage,
            tuple(targets),
            0,
            0,
            0,
            0,
            0,
            0,
            -1,
        )
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


# ---------------------------------------------------------------------------
# Étape 5.3 : Fin de partie, Repousse des tuiles Enracinées (INV-22) & GameOver
# ---------------------------------------------------------------------------


def _regrow_souches_on_ray(state: GameState, ray: int, count: int) -> int:
    """Retourne librement jusqu'à `count` Souches survivantes de `ray` en Arbres debout (INV-01 / INV-22)."""
    rem = count
    converted_total = 0
    for p in range(1, state.cfg.p_max + 1):
        if rem <= 0:
            break
        if state.is_route_forestiere(ray, p):
            continue
        souches = state.get_parcel_souches(ray, p)
        if souches <= 0:
            continue
        before_a = state.get_parcel_arbres(ray, p)
        prim_creation_entite(
            state, "ARBRE", ray=ray, p=p, count=min(rem, souches), light_trigger=False
        )
        gained = state.get_parcel_arbres(ray, p) - before_a
        converted_total += gained
        rem -= gained
    return converted_total


def apply_repousse_finale(state: GameState) -> GameOver:
    """Clôture la partie de manière strictement idempotente, applique l'Enracinement (INV-22) et calcule le score.

    v6.4 (INV-22) : sur les 3 fins (Tour 8, Sommeil, Éveil), chaque tuile enracinée sur la Rive Sabotage
    de son rayon y retourne 1 Souche (F1/unique) ou 2 Souches (F2 ou R2 Gué marqué) en Arbres debout,
    librement choisies parmi les parcelles survivantes de son rayon (plafond physique 10×N, INV-01).
    """
    # Priorité absolue à Tour 8 (au Tour 8, la fin est toujours TOUR_8)
    if state.tour >= 8:
        cause = CAUSE_TOUR_8
    elif state.cfg.mode >= 2 and state.is_sommeil_victory():
        cause = CAUSE_REVE_RANG_1
    elif state.is_eveil_gardiens_victory():
        cause = CAUSE_REVEIL_GARDIENS
    else:
        cause = CAUSE_TOUR_8

    if not state.repousse_finale_applied:
        trk = _get_active_telemetry()
        if trk is not None and state.tour >= 8 and state.cfg.mode >= 2:
            if state.is_sommeil_victory():
                trk.ok_tour8_blocked_sommeil += 1
            if (
                state.cfg.nb_animaux_sauvages >= 1
                and state.count_face2_gardiens_on_track() >= (state.cfg.nb_animaux_sauvages + 1)
                and not state.has_gardien_bet_lost_this_turn()
            ):
                trk.ok_tour8_blocked_eveil += 1
        arbres_before_repousse = state.total_arbres_plateau()

        # 1. Application native des tuiles enracinées volontairement sur la Rive Sabotage (INV-22)
        rooted_tiles = state.list_rooted_tiles()
        for _slot_idx, _tid, r_root, _slot_on_rive, tier_souches in rooted_tiles:
            _regrow_souches_on_ray(state, r_root, tier_souches)

        # 2. Extensions Mode 3/4 (G7 / G15 Enracinés sur phase ROOTED_TILE, plus phase PARCEL)
        if state.cfg.mode >= 3:
            for slot_idx, tid, r_root, slot_on_rive, tier_souches in rooted_tiles:
                dispatch_hook(
                    state,
                    HOOK_REPOUSSE_FINALE,
                    {
                        "phase": "ROOTED_TILE",
                        "slot_id": tid,
                        "slot_idx": slot_idx,
                        "ray": r_root,
                        "slot_on_rive": slot_on_rive,
                        "tier": tier_souches,
                        "max_repousse": 0,
                    },
                )
            for r in range(state.cfg.n_players):
                for p in range(1, state.cfg.p_max + 1):
                    if state.is_route_forestiere(r, p):
                        continue
                    souches = state.get_parcel_souches(r, p)
                    if souches >= 1:
                        rep_ctx: dict[str, Any] = {
                            "phase": "PARCEL",
                            "ray": r,
                            "p": p,
                            "max_repousse": 0,
                        }
                        dispatch_hook(state, HOOK_REPOUSSE_FINALE, rep_ctx)
                        max_rep = int(rep_ctx["max_repousse"])
                        if max_rep > 0:
                            prim_creation_entite(
                                state,
                                "ARBRE",
                                ray=r,
                                p=p,
                                count=max_rep,
                                light_trigger=False,
                            )
        state.repousse_finale_applied = True
        state._continuation.clear()
        _transition_step(state, STEP_GAME_OVER)
        score_now = state.total_arbres_plateau()
        arbres_regrown = max(0, score_now - arbres_before_repousse)
        init_now = state.cfg.n_players * sum(state.cfg.dotation_arbres)
        ratio_now = score_now / init_now if init_now > 0 else 0.0
        if trk is not None:
            trk.on_defense_repousse_finale(arbres_regrown)
            trk.on_game_over_ratio(state, cause=cause, ratio_arbres=ratio_now)
            trk.on_end_turn(state, game_over=True)

    score = state.total_arbres_plateau()
    init_total = state.cfg.n_players * sum(state.cfg.dotation_arbres)
    ratio = score / init_total if init_total > 0 else 0.0
    return GameOver(
        tour_fin=state.tour,
        cause_fin=cause,
        score_arbres=score,
        ratio_arbres=ratio,
    )


def _check_end_of_game_condition(state: GameState) -> bool:
    if state.tour >= 8:
        return True
    if state.cfg.mode >= 2:
        if state.is_sommeil_victory():
            return True
        if state.is_eveil_gardiens_victory():
            return True
    return False


# ---------------------------------------------------------------------------
# Helpers internes pour Migration 4.3, Ratissage physique 6.3 et files d'attente
# ---------------------------------------------------------------------------


def _transition_eligible_machines_to_ratissage(state: GameState) -> None:
    """Fait basculer en Ratissage en 6.3 toute machine normale sur la dernière parcelle :
    conserve tous ses jetons existants et gagne +1 jeton rouge physique (INV-12 ; 0 bonus imprimé).
    Une machine portant la cale du Caïman noir (G9) ne peut pas entrer en Ratissage.
    """
    ops = 0
    entries = 0
    for r in range(state.cfg.n_players):
        last_p = state.last_non_razed_parcel(r)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_NORMAL or pos == 0:
                continue
            if last_p is not None and pos == last_p:
                # G9 Le Caïman noir : tant qu'elle porte la cale, la machine ne peut pas entrer en Ratissage
                if state.get_machine_cale(r, mt) == CALE_CAIMAN:
                    continue
                state.set_machine_pos_status(r, mt, pos, MACHINE_STATUS_RATISSAGE, False)
                r_tok, b_tok = state.get_machine_tokens(r, mt)
                if r_tok < 15:
                    state.set_machine_tokens(r, mt, r_tok + 1, b_tok)
                    ops += 1
                # Une machine en Ratissage perd toute Altération (retour réserve Entités)
                if state.has_machine_alteration(r, mt):
                    state.set_machine_alteration(r, mt, False)
                    ops += 1
                ops += 1
                entries += 1
    if ops > 0:
        _record_phys_ops(state, ops)
    if entries > 0:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.ok_ratissage_entries_6_3 += entries


def _list_nid_deploy_options(
    state: GameState, ray: int, p: int
) -> tuple[tuple[Any, ...], ...]:
    """Options de Déploiement direct en 4.2 pour chaque Insecte créé par le Nid sur `(ray, p)` (INV-21)."""
    if not state.cfg.has_insectes_peuple or state.is_route_forestiere(ray, p):
        return ()
    opts: list[tuple[Any, ...]] = [("FORET", ray, p)]
    p_fwd = state.next_non_razed_towards_heart(ray, p)
    if p_fwd is not None:
        opts.append(("FORET", ray, p_fwd))
    p_back = state.next_non_razed_towards_border(ray, p)
    if p_back is not None:
        opts.append(("FORET", ray, p_back))
    if state.cfg.mode >= 2 and p == state.last_non_razed_parcel(ray):
        for c in range(1, TRACK_LEN + 1):
            opts.append(("BUG", c))
        for c in range(1, TRACK_LEN + 1):
            opts.append(("COLONIE", c))
    return tuple(opts)


def _is_ray_bulldozer_first(state: GameState, ray: int) -> bool:
    if state.cfg.mode < 3:
        return False
    ord_ctx: dict[str, Any] = {"ray": ray, "bulldozer_first": False}
    dispatch_hook(state, HOOK_5_ORDRE_RAYON, ord_ctx)
    return bool(ord_ctx.get("bulldozer_first"))


def _resolve_tactique_5_1_machine(state: GameState, rm: int, mt: int, rank_t_code: int) -> None:
    _, st, _ = state.get_machine_pos_status(rm, mt)
    if st == MACHINE_STATUS_RATISSAGE:
        resolve_single_machine_attack(state, rm, mt, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True)
        return
    eff_code = rank_t_code
    t_card = machine_card_code(rm, mt)
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if card == t_card and is_tactique_code(bound_t):
            eff_code = bound_t
            break
    resolve_single_machine_attack(state, rm, mt, TACTIQUES_SPEC[eff_code])


def _eligible_tactique_machines_at_rank(state: GameState, t_code: int) -> list[tuple[int, int]]:
    pending_by_ray: dict[int, list[int]] = {}
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if bound_t == t_code and 1 <= card <= 12:
            r, mt = (card - 1) // 2, (card - 1) % 2
            if state.is_machine_etouffee_this_turn(r, mt):
                continue
            pos, st, _ = state.get_machine_pos_status(r, mt)
            _, _, attacked = state.get_machine_turn_stats(r, mt)
            if st == MACHINE_STATUS_NORMAL and pos > 0 and not attacked:
                pending_by_ray.setdefault(r, []).append(mt)

    eligible: list[tuple[int, int]] = []
    for offset in range(state.cfg.n_players):
        r = (state.coordonnateur + offset) % state.cfg.n_players
        mts = pending_by_ray.get(r)
        if not mts:
            continue
        if _is_ray_bulldozer_first(state, r):
            if MACHINE_BULLDOZER in mts:
                eligible.append((r, MACHINE_BULLDOZER))
                continue
            bu_pos, bu_st, _ = state.get_machine_pos_status(r, MACHINE_BULLDOZER)
            _, _, bu_att = state.get_machine_turn_stats(r, MACHINE_BULLDOZER)
            if (
                not bu_att
                and bu_pos > 0
                and bu_st != MACHINE_STATUS_RETIRED
                and is_machine_active_this_turn(state, r, MACHINE_BULLDOZER)
            ):
                eligible.append((r, MACHINE_BULLDOZER))
                continue
        if MACHINE_ABATTEUSE in mts:
            eligible.append((r, MACHINE_ABATTEUSE))
        else:
            eligible.append((r, MACHINE_BULLDOZER))
    return eligible


def _eligible_ratissage_machines(state: GameState) -> list[tuple[int, int]]:
    eligible: list[tuple[int, int]] = []
    for offset in range(state.cfg.n_players):
        r = (state.coordonnateur + offset) % state.cfg.n_players
        ab_pos, ab_st, _ = state.get_machine_pos_status(r, MACHINE_ABATTEUSE)
        _, _, ab_att = state.get_machine_turn_stats(r, MACHINE_ABATTEUSE)
        bu_pos, bu_st, _ = state.get_machine_pos_status(r, MACHINE_BULLDOZER)
        _, _, bu_att = state.get_machine_turn_stats(r, MACHINE_BULLDOZER)

        ab_ok = (
            ab_st == MACHINE_STATUS_RATISSAGE
            and ab_pos > 0
            and not ab_att
            and not state.is_machine_etouffee_this_turn(r, MACHINE_ABATTEUSE)
        )
        bu_ok = (
            bu_st == MACHINE_STATUS_RATISSAGE
            and bu_pos > 0
            and not bu_att
            and not state.is_machine_etouffee_this_turn(r, MACHINE_BULLDOZER)
        )
        if _is_ray_bulldozer_first(state, r) and bu_ok:
            eligible.append((r, MACHINE_BULLDOZER))
        elif ab_ok:
            eligible.append((r, MACHINE_ABATTEUSE))
        elif bu_ok:
            eligible.append((r, MACHINE_BULLDOZER))
    return eligible


# ---------------------------------------------------------------------------
# Étapes 3.2 et 4.1 suspendables v6.4 (fil d'ouverture 1->4, Sentinelles Rive Sabotage)
# ---------------------------------------------------------------------------


def _machine_threat_key_3_2(state: GameState, seat: int, card: int) -> tuple[int, int, int, int, int]:
    """Clé de priorité décroissante de menace pour les bots sur un Rêve en 3.2."""
    ray = (card - 1) // 2
    m_type = (card - 1) % 2
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    eff_red = (
        state.get_machine_effective_rouges(ray, m_type)
        if (st != MACHINE_STATUS_RETIRED and pos > 0)
        else 0
    )
    return machine_threat_key_3_2(seat, pos, st, eff_red)


def _eligible_sabotage_targets_3_2(state: GameState, seat: int) -> tuple[tuple[int, int], ...]:
    """Cibles légales d'un jeton Sabotage ordinaire révélé par `seat` (INV-05) :
    machines de son rayon ou d'un rayon voisin pouvant être Refroidies (>= 1 Rouge, mobile ou Ratissage)
    ou Reculées (mobile à 0 Rouge non déjà en bordure).
    """
    n = state.cfg.n_players
    rays = sorted({seat, (seat - 1) % n, (seat + 1) % n})
    out: list[tuple[int, int]] = []
    for r in rays:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            rouges, _ = state.get_machine_tokens(r, mt)
            if rouges >= 1 or (
                st == MACHINE_STATUS_NORMAL
                and state.next_non_razed_towards_border(r, pos) is not None
            ):
                out.append((r, mt))
    return tuple(out)


def _apply_sabotage_target_3_2(state: GameState, ray: int, m_type: int) -> None:
    """Applique le Sabotage ordinaire différé (INV-05) : Refroidir si >= 1 Rouge, sinon Reculer si mobile."""
    rouges, _ = state.get_machine_tokens(ray, m_type)
    if rouges >= 1:
        verb_refroidir(state, ray, m_type, 1)
    else:
        verb_reculer(state, ray, m_type)


def _resolve_alterations_3_2(state: GameState) -> None:
    """Temps 1 du fil d'ouverture (INV-15 / INV-20) : toute machine révélée portant une Altération la perd,
    compte dans m(r) (sauf R2 Linceul/Gué), Recule d'1 parcelle vers la bordure et est Étouffée.
    """
    n = state.cfg.n_players
    for off in range(n):
        s = (state.coordonnateur + off) % n
        card, _, _, _, _ = state.get_player_hand(s)
        if not (1 <= card <= 12):
            continue
        r, mt = (card - 1) // 2, (card - 1) % 2
        if not state.has_machine_alteration(r, mt):
            continue
        state.set_machine_alteration(r, mt, False)
        state.mark_seat_altered_this_turn(s)
        verb_etouffer(state, r, mt, seat=s)
        verb_reculer(state, r, mt)
        _record_phys_ops(state, 1)
        if state.cfg.mode >= 3:
            dispatch_hook(
                state,
                HOOK_3_2_REVELATION,
                {"phase": "ALTERATION_LOST", "seat": s, "ray": r, "m_type": mt},
            )


def _bind_remaining_active_mobiles_3_2(state: GameState) -> None:
    """Pose les dés de toutes les mobiles non Étouffées/altérées/annulées sur leur rang 1..6."""
    for s in range(state.cfg.n_players):
        if (
            state.was_seat_altered_this_turn(s)
            or state.was_seat_cancelled_by_reve_this_turn(s)
        ):
            continue
        card, d1, d2, lec_m, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and 1 <= lec_m <= TRACK_LEN:
            r, mt = (card - 1) // 2, (card - 1) % 2
            if state.is_machine_etouffee_this_turn(r, mt):
                continue
            if bound_t == 0:
                state.set_player_hand(s, card, d1, d2, lec_m, lec_m)


def _resolve_defended_reve_3_2(
    state: GameState,
    r_idx: int,
    r_num: int,
    entries: tuple[tuple[int, int, int, int, int], ...],
    cancelled_seats: tuple[int, ...],
    extra_entries: tuple[tuple[int, int, int, int, int], ...] = (),
) -> None:
    """Résout un Rêve défendu en 3.2 (INV-15 / INV-20) :
    1) Étouffe les machines choisies par le propriétaire (jeton 90°, dé retiré).
    2) Si le Chamane CHANT défend ce Rêve, >= 1 machine Étouffée et 0 machine active restante : glisse d'1 rang à gauche.
    3) Exécute intégralement le pouvoir propre du Rêve (même à 0 machine hors mention contraire).
    4) Couche les Défenseurs restants à plat, gère G12 F2 si applicable, puis allume TRIG_REVE si >= 1 Étouffée + sweep.
    """
    case_1_6 = r_idx + 1
    cancelled_set = set(cancelled_seats)
    for s, card, d1, d2, lec_m in entries:
        r_m, mt_m = (card - 1) // 2, (card - 1) % 2
        if s in cancelled_set:
            verb_etouffer(state, r_m, mt_m, seat=s)
            state.mark_seat_cancelled_by_reve_this_turn(s)
        else:
            state.set_player_hand(s, card, d1, d2, lec_m, case_1_6)
    for s, card, d1, d2, lec_m in extra_entries:
        if s in cancelled_set:
            r_m, mt_m = (card - 1) // 2, (card - 1) % 2
            verb_etouffer(state, r_m, mt_m, seat=s)
            state.mark_seat_cancelled_by_reve_this_turn(s)

    n_cancel = len(cancelled_set)
    n_bypass_own = sum(1 for e in entries if e[0] not in cancelled_set)
    if n_cancel > 0:
        consumed = state.consume_reve_activation_defenders(case_1_6, n_cancel)
        if consumed > 0:
            _record_phys_ops(state, consumed)

    # Vérifier le Chamane CHANT avant tout déplacement/pouvoir (inclut debout et couché sur ce rang)
    chant_slides = (
        state.is_chant_on_reve_case(case_1_6) and n_cancel >= 1 and n_bypass_own == 0
    )

    state.mark_reve_opened_this_turn(r_num)
    trk = _get_active_telemetry()
    if trk is not None:
        trk.on_reve_activated(1)
        if n_cancel > 0:
            trk.on_machines_cancelled_by_reve(n_cancel)
        if n_bypass_own > 0:
            trk.on_machines_bypassed_inactive_reve(n_bypass_own)

    # Clôture post-pouvoir (couchage Défenseurs, bonus G12 F2, TRIG_REVE + sweep Gardiens)
    push_continuation_sequence(
        state,
        (("STEP_3_2_POST_REVE_FINISH", r_num, 1 if n_cancel >= 1 else 0, tuple(cancelled_seats)),),
    )

    if chant_slides:
        verb_glisser_reve(state, r_idx, push_block=True)

    cur_idx = state.find_tactique_rank(TILE_R_BASE + r_num)
    cur_case = (cur_idx + 1) if cur_idx is not None else case_1_6

    if state.cfg.mode >= 3:
        dispatch_hook(
            state,
            HOOK_3_2_OUVERTURE_REVE,
            {
                "phase": "OPEN",
                "slot_id": f"R{r_num}",
                "r_num": r_num,
                "case": cur_case,
                "cancelled_seats": tuple(cancelled_seats),
                "n_cancel": n_cancel,
                "choice": "BLOQUER",
            },
        )


def _run_step_3_2(state: GameState) -> None:
    """Fil d'ouverture imprimé v6.4 (INV-15) empilé chronologiquement via push_continuation_sequence :
    (0) Ouverture des paravents ;
    (1) Altérations (retrait, Étouffement + Recul) + Cales Caïman noir (G9) ;
    (2) Sabotages ordinaires (Refroidir sinon Reculer) & Écailles (Croc + R8) un par un ;
    (3) Déviations d'Insectes ±1 une par une (+ M5) ;
    (4) Rêves défendus de gauche à droite (PRE_CANCEL -> annulations -> pouvoir -> coucher -> TRIG_REVE) ;
    (5) Post-révélation Mode 3/4 + transition vers 4.1 Furtivité.
    """
    prim_partage_info_etat_gardien(state, "OPEN_PARAVENTS")
    _resolve_alterations_3_2(state)

    n = state.cfg.n_players
    cale_seats: list[int] = []
    sab_seats: list[int] = []
    for off in range(n):
        s = (state.coordonnateur + off) % n
        card = state.get_player_hand(s)[0]
        if card in (CARD_SABOTAGE, CARD_ECAILLE):
            sab_seats.append(s)
        elif 1 <= card <= 12 and not state.was_seat_altered_this_turn(s):
            r_m, mt_m = (card - 1) // 2, (card - 1) % 2
            if state.get_machine_cale(r_m, mt_m) == CALE_CAIMAN:
                cale_seats.append(s)

    frames: list[tuple[Any, ...]] = []
    if cale_seats and state.cfg.mode >= 3:
        frames.append(("STEP_3_2_CALE_QUEUE", tuple(cale_seats), 0))
    if sab_seats:
        frames.append(("STEP_3_2_SABOTAGE_QUEUE", tuple(sab_seats), 0))
    if state.cfg.mode >= 2 and (state.cfg.has_insectes_peuple or state.cfg.mode >= 3):
        frames.append(("STEP_3_2_BUG_DEVIATIONS",))
    frames.append(("STEP_3_2_REVES_SCAN", 1))
    if state.cfg.mode >= 3:
        frames.append(("STEP_3_2_POST",))
    frames.append(("STEP_3_2_END",))
    push_continuation_sequence(state, frames)


def _execute_furtivite_4_1_action(
    state: GameState,
    ray: int,
    p: int,
    rive: int,
    action_kind: str,
    cell_key: int = -1,
) -> None:
    if action_kind == "PIEGE":
        # 2. Piégeage ne s'allume pas à la pose en 4.1 (uniquement sur frappe bloquée en 5.1/5.2)
        prim_creation_entite(state, "PIEGE", ray=ray, p=p, light_trigger=False)
    else:
        # 3. Sabotage ne s'allume pas à l'acquisition en 4.1 (Semer au sac sans icône)
        verb_semer_au_sac(state, "SABOTAGE", 1)
    trk = _get_active_telemetry()
    if trk is not None and cell_key >= 0:
        trk.on_furtivite_rive_executed(cell_key, action_kind)
    if state.cfg.mode >= 3:
        dispatch_hook(
            state,
            HOOK_4_1_FURTIVITE,
            {
                "ray": ray,
                "p": p,
                "rive": rive,
                "phase": "POST",
                "handled": True,
                "action": action_kind,
            },
        )
    sweep_gardiens(state)


def _run_step_4_1_from(state: GameState, start_slot_idx: int) -> None:
    """Résout la Furtivité v6.4 (« Chaud vs Calme » + Effet Sentinelle sur Rive Sabotage, INV-14)."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    total_rives = 2 * n
    trk = _get_active_telemetry()

    for slot_idx in range(start_slot_idx, total_rives):
        off = slot_idx // 2
        rive = slot_idx & 1
        ray = (state.coordonnateur + off) % n
        if not state.is_ray_furtivite_open(ray):
            continue
        cell_key = ray
        nb_def = state.get_furtivite_nb_def_rive(ray, 1, rive)
        sentinels = (
            state.count_rooted_sentinels_on_ray(ray) if rive == FURT_RIVE_SABOTAGE else 0
        )
        total_occ = nb_def + sentinels
        if total_occ != 2:
            if nb_def == 1 and sentinels == 0 and trk is not None:
                trk.on_furtivite_orphan_pawn(1)
            continue

        m_r = state.count_mobilized_machines_for_ray(ray)
        if rive == FURT_RIVE_PIEGE:
            if m_r != 2:
                if trk is not None:
                    trk.on_furtivite_failed_binome(1, rive="PIEGE")
                continue

            valid_parcels = tuple(
                p
                for p in range(1, p_max + 1)
                if not state.is_route_forestiere(ray, p)
                and state.get_parcel_piege(ray, p) == PIEGE_AUCUN
            )
            if not valid_parcels:
                if trk is not None:
                    trk.on_furtivite_failed_binome(1, rive="PIEGE")
                continue

            if len(valid_parcels) == 1:
                resume_frame = ("RESUME_STEP_4_1", slot_idx + 1)
                if state.cfg.mode >= 3:
                    push_continuation_sequence(state, (resume_frame,))
                _execute_furtivite_4_1_action(
                    state, ray, valid_parcels[0], rive, "PIEGE", cell_key
                )
                if state.cfg.mode >= 3:
                    if state._continuation and state._continuation[0] == resume_frame:
                        state._continuation.pop(0)
                    else:
                        return
                continue

            req = DecisionRequest(
                decideur=ray,
                decision_type=DEC_POSE_PIEGE_FURTIVITE_4_1,
                options=valid_parcels,
                context={"ray": ray, "tour": state.tour},
            )
            push_continuation_sequence(
                state,
                (
                    ("WAIT_DECISION", req),
                    ("APPLY_PIEGE_FURTIVITE_4_1", ray, rive, cell_key),
                    ("RESUME_STEP_4_1", slot_idx + 1),
                ),
            )
            return

        # Rive Sabotage (rive == FURT_RIVE_SABOTAGE) : pari gagné ssi m(ray) == 0 (inclut Sentinelles 1/2)
        if m_r != 0:
            if nb_def >= 1 and trk is not None:
                trk.on_furtivite_failed_binome(1, rive="SABOTAGE")
            continue

        resume_frame = ("RESUME_STEP_4_1", slot_idx + 1)
        if state.cfg.mode >= 3:
            push_continuation_sequence(state, (resume_frame,))
        _execute_furtivite_4_1_action(state, ray, 1, rive, "SABOTAGE", cell_key)
        if state.cfg.mode >= 3:
            if state._continuation and state._continuation[0] == resume_frame:
                state._continuation.pop(0)
            else:
                return

    _transition_step(state, STEP_4_2_NIDS)


# ---------------------------------------------------------------------------
# Étape 5.3 (Paris Gardiens + Bouclier facultatif I + Éveil cumulatif) & Étape 6.1 (Enracinement Sentinelle)
# ---------------------------------------------------------------------------


def _resolve_gardien_bets_5_3_from(
    state: GameState,
    start_case: int,
    bets_won: int,
    bets_lost: int,
    bouclier_saves: int,
    face2_upgrades: int,
) -> DecisionRequest | None:
    """Résout les paris d'activation des Gardiens en 5.3 (INV-10 & INV-18).

    - `rem >= 1` : pari PERDU (marque `gardien_bet_lost_this_turn` empêchant l'Éveil ce tour ;
      retour en lisière Face 1, sauf choix facultatif de I de défausser 1 Insecte en Bouclier de lisière).
    - `rem == 0 and cons >= 1` : pari GAGNÉ (reste en piste et passe Face 2).
    - `rem == 0 and cons == 0` : aucune mise engagée (reste en place sur sa face actuelle sans évoluer).
    """
    if state.cfg.mode >= 2 and state.cfg.nb_animaux_sauvages >= 1:
        for c_num in range(start_case, TRACK_LEN + 1):
            rem = state.count_gardien_pari_defenders_at_case(c_num)
            cons = state.count_gardien_pari_consumed_at_case(c_num)
            g_num, g_face = state.get_gardien_at_case(c_num)
            if rem >= 1:
                bets_lost += 1
                state.mark_gardien_bet_lost_this_turn()
                if g_num > 0:
                    col_ins = state.get_colonie_at_case(c_num)
                    if col_ins >= 1 and state.cfg.has_insectes_peuple:
                        # INV-18 : Bouclier de lisière facultatif gouverné par I
                        gov_i = _governor_for_peuple(state, "I")
                        req = DecisionRequest(
                            decideur=gov_i,
                            decision_type=DEC_BOUCLIER_LISIERE_5_3,
                            options=("UTILISER_BOUCLIER", "LAISSER_RETOURNER"),
                            context={
                                "case": c_num,
                                "g_num": g_num,
                                "tile_id": f"G{g_num}",
                                "face": g_face,
                                "colonie_insectes": col_ins,
                                "tour": state.tour,
                            },
                        )
                        push_continuation_sequence(
                            state,
                            (
                                ("WAIT_DECISION", req),
                                (
                                    "APPLY_BOUCLIER_5_3",
                                    c_num,
                                    bets_won,
                                    bets_lost,
                                    bouclier_saves,
                                    face2_upgrades,
                                ),
                            ),
                        )
                        return req
                    prim_partage_info_etat_gardien(
                        state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=c_num
                    )
            elif cons >= 1:
                bets_won += 1
                if g_num > 0 and g_face == 1:
                    # INV-10 : passage Face 1 -> Face 2 sur pari gagné (les 15 Gardiens ont Face 2)
                    state.set_gardien_at_case(c_num, g_num, 2)
                    _record_phys_ops(state, 1)
                    face2_upgrades += 1

        trk = _get_active_telemetry()
        if trk is not None:
            if bets_won > 0 or bets_lost > 0:
                trk.on_gardien_bets_resolved(state, bets_won=bets_won, bets_lost=bets_lost)
            if bouclier_saves > 0:
                trk.on_bouclier_lisiere_save(bouclier_saves)
            if face2_upgrades > 0:
                trk.ok_gardien_face2_upgrades += face2_upgrades

    if _check_end_of_game_condition(state):
        _transition_step(state, STEP_GAME_OVER)
    else:
        _transition_step(state, STEP_6_2_EVOLUTION)
    return None


def _eligible_rooting_options_for_seat(
    state: GameState, seat: int
) -> tuple[Any, ...]:
    """Options d'Enracinement volontaire sur la Rive Sabotage de `seat` : ('PASSER', slot_idx, ...) (INV-22)."""
    if state.first_non_razed_from_border(seat) is None:
        return ()
    if state.count_rooted_sentinels_on_ray(seat) >= 2:
        return ()

    p_code = state.cfg.peuples[seat]
    eligible_slots: list[int] = []
    for slot_idx, tid in enumerate(state.cfg.lisiere_slots):
        if state.is_slot_rooted(slot_idx):
            continue
        fam, orig, num = SYNERGY_META[tid]
        if orig != p_code:
            continue
        on_board = False
        if fam == FAMILLE_GARDIEN:
            for c in range(1, TRACK_LEN + 1):
                if state.get_gardien_at_case(c)[0] == num:
                    on_board = True
                    break
        elif fam == FAMILLE_REVE:
            on_board = state.find_tactique_rank(TILE_R_BASE + num) is not None
        elif fam == FAMILLE_CROISSANCE:
            on_board = state.get_nid_position(num) is not None
        if on_board:
            eligible_slots.append(slot_idx)

    if not eligible_slots:
        return ()

    return ("PASSER", *eligible_slots)


def _apply_voluntary_rooting_6_1(state: GameState, seat: int, slot_idx: int) -> None:
    """Enracine une tuile construite du Peuple de `seat` sur la Rive Sabotage de `seat` (INV-14 / INV-22)."""
    tid = state.cfg.lisiere_slots[slot_idx]
    fam, orig, num = SYNERGY_META[tid]
    assert orig == state.cfg.peuples[seat], "Enracinement réservé aux tuiles de son propre Peuple"
    tier_souches = 1
    gue_marque = False
    if fam == FAMILLE_GARDIEN:
        for c in range(1, TRACK_LEN + 1):
            g_num, g_face = state.get_gardien_at_case(c)
            if g_num == num:
                tier_souches = g_face
                state.set_gardien_at_case(c, 0, 1)  # Laisse PISTE_COLONIE intact !
                if g_num == 7:
                    state.clear_all_bourbiers()
                elif g_num == 9:
                    state.clear_all_cales()
                break
    elif fam == FAMILLE_REVE:
        rank_r = state.find_tactique_rank(TILE_R_BASE + num)
        assert rank_r is not None
        state.set_tactique_at_rank(rank_r, rank_r + 1)  # Laisse PISTE_BUGS intact !
        # R2 (Gué de cendre) : si >= 1 machine du rayon E porte une Altération à l'enracinement -> Gué marqué (2 Souches)
        if tid == "R2" and state.cfg.profile_for_slot("R2") is not None:
            for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
                if state.has_machine_alteration(seat, mt):
                    gue_marque = True
                    tier_souches = 2
                    break
    elif fam == FAMILLE_CROISSANCE:
        assert state.get_nid_position(num) is not None
        state.clear_nid(num)  # Laisse FORET_INSECTES intact et rend la ponte G14 en réserve !

    state.root_tile_on_sabotage_bank(
        slot_idx, seat, tier_souches=tier_souches, gue_marque=gue_marque
    )
    _record_phys_ops(state, 1)
    if state.cfg.mode >= 3:
        dispatch_hook(
            state,
            HOOK_ENRACINEMENT,
            {
                "slot_id": tid,
                "slot_idx": slot_idx,
                "ray": seat,
                "tier": tier_souches,
                "gue_marque": gue_marque,
            },
        )


def _run_step_6_2(state: GameState) -> GameOver | None:
    """Ménage de fin de tour 6.2 : retour en main des Défenseurs, descente Insectes passagers & RAZ transitoires."""
    trk = _get_active_telemetry()
    if trk is not None:
        cleanup_ops = 0
        for s in range(state.cfg.n_players):
            for d in (0, 1):
                raw = state.get_player_def_loc_raw(s, d)
                if raw not in (0, 255):
                    cleanup_ops += 1
            if state.get_player_hand(s)[0] != CARD_NONE:
                cleanup_ops += 1
        _record_phys_ops(state, cleanup_ops)

    state.cleanup_end_of_turn_6_2()
    if state.cfg.enracinement_enabled:
        _transition_step(state, STEP_6_1_ENRACINEMENT)
    else:
        _transition_step(state, STEP_6_3_END_TURN)
    return None


# ---------------------------------------------------------------------------
# Boucle principale BGA-ready : step_until_decision & apply_choice
# ---------------------------------------------------------------------------


def _advance_continuation(state: GameState) -> DecisionRequest | None:
    """Exécute un pas de la file _continuation ; retourne une DecisionRequest si suspendu."""
    n = state.cfg.n_players
    top: tuple[Any, ...] = state._continuation[0]
    tag = str(top[0])

    if tag == "WAIT_DECISION":
        req_wait = top[1]
        assert isinstance(req_wait, DecisionRequest)
        return req_wait

    if tag == "LIGHT_TRIGGER_SYNC":
        _, case_num = state._continuation.pop(0)
        state.light_trigger(int(case_num))
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_trigger_lit(int(case_num))
        return None

    if tag == "DEFERRED_EFFECT_CALLBACK":
        _, slot_id, profile, resume_tag, payload = state._continuation.pop(0)
        reg = get_tile_registration(str(slot_id), str(profile))
        if reg is not None:
            reg.handler(
                state,
                HOOK_EFFECT_RESUME,
                {
                    "slot_id": str(slot_id),
                    "profile": str(profile),
                    "resume_tag": str(resume_tag),
                    "payload": payload,
                    "choice": None,
                },
            )
        return None

    if tag == "RESUME_HOOK_QUEUE":
        _, hook_name, rem_slots, frozen_ctx = state._continuation.pop(0)
        for idx, slot_id in enumerate(rem_slots):
            rest = rem_slots[idx + 1 :]
            r_frame: tuple[Any, ...] | None = None
            if rest:
                r_frame = ("RESUME_HOOK_QUEUE", hook_name, rest, frozen_ctx)
                push_continuation_sequence(state, (r_frame,))
            payload = dict(frozen_ctx)
            payload["slot_id"] = slot_id
            dispatch_hook(state, str(hook_name), payload)
            if r_frame is not None:
                if state._continuation and state._continuation[0] == r_frame:
                    state._continuation.pop(0)
                else:
                    return None
            elif has_pending_decision(state):
                return None
        return None

    if tag == "RESUME_SWEEP_GARDIENS":
        (
            _,
            next_case,
            in_combat_i,
            opened_tot,
            res_fired_i,
        ) = state._continuation.pop(0)
        _sweep_gardiens_from(
            state,
            int(next_case),
            bool(in_combat_i),
            int(opened_tot),
            bool(res_fired_i),
        )
        return None

    if tag == "SWEEP_GARDIENS_NOW":
        state._continuation.pop(0)
        sweep_gardiens(state)
        return None

    if tag == "STEP_1_3_FINISH":
        state._continuation.pop(0)
        if state.cfg.mode >= 3:
            push_continuation_sequence(state, (("STEP_1_3_HOOK_QUEUE", 0),))
        else:
            _transition_step(state, STEP_2_1_DEF1)
        return None

    if tag == "STEP_1_3_HOOK_QUEUE":
        _, start_seat = state._continuation.pop(0)
        s_idx = int(start_seat)
        while s_idx < n:
            card, _, _, _, _ = state.get_player_hand(s_idx)
            if 1 <= card <= 12:
                next_f = ("STEP_1_3_HOOK_QUEUE", s_idx + 1)
                push_continuation_sequence(state, (next_f,))
                dispatch_hook(state, HOOK_1_3_LECTURE_DE, {"seat": s_idx})
                if state._continuation and state._continuation[0] == next_f:
                    state._continuation.pop(0)
                    s_idx += 1
                else:
                    return None
            else:
                s_idx += 1
        _transition_step(state, STEP_2_1_DEF1)
        dispatch_hook(state, HOOK_2_1_DEBUT, {})
        return None

    if tag == "STEP_3_2_CALE_QUEUE":
        _, cale_seats, cur_idx = state._continuation.pop(0)
        if cur_idx < len(cale_seats):
            s = int(cale_seats[cur_idx])
            if cur_idx + 1 < len(cale_seats):
                push_continuation_sequence(
                    state, (("STEP_3_2_CALE_QUEUE", cale_seats, cur_idx + 1),)
                )
            card = state.get_player_hand(s)[0]
            if 1 <= card <= 12 and not state.was_seat_altered_this_turn(s):
                r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                if state.get_machine_cale(r_m, mt_m) == CALE_CAIMAN:
                    push_continuation_sequence(state, (("SWEEP_GARDIENS_NOW",),))
                    dispatch_hook(
                        state,
                        HOOK_3_2_CALE_REVEAL,
                        {"seat": s, "ray": r_m, "m_type": mt_m},
                    )
        return None

    if tag == "STEP_3_2_SABOTAGE_QUEUE":
        _, sab_seats, cur_idx = state._continuation.pop(0)
        if cur_idx < len(sab_seats):
            s = int(sab_seats[cur_idx])
            card = state.get_player_hand(s)[0]
            if cur_idx + 1 < len(sab_seats):
                push_continuation_sequence(
                    state, (("STEP_3_2_SABOTAGE_QUEUE", sab_seats, cur_idx + 1),)
                )
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_defense_sabotage_revele(1)
            state.light_trigger(TRIG_SABOTAGE)
            if trk is not None:
                trk.on_trigger_lit(TRIG_SABOTAGE)
            if card == CARD_SABOTAGE:
                # INV-05 v6.4 : Sabotage différé (Refroidir si >= 1 Rouge, sinon Reculer si mobile)
                targets_sab = _eligible_sabotage_targets_3_2(state, s)
                if len(targets_sab) == 1:
                    _apply_sabotage_target_3_2(state, targets_sab[0][0], targets_sab[0][1])
                    sweep_gardiens(state)
                    return None
                if len(targets_sab) > 1:
                    req_s = DecisionRequest(
                        decideur=s,
                        decision_type=DEC_SABOTAGE_CIBLE_3_2,
                        options=targets_sab,
                        context={"tour": state.tour, "seat_sabotage": s},
                    )
                    push_continuation_sequence(
                        state,
                        (
                            ("WAIT_DECISION", req_s),
                            ("APPLY_SABOTAGE_CIBLE_3_2",),
                            ("SWEEP_GARDIENS_NOW",),
                        ),
                    )
                    return req_s
                sweep_gardiens(state)
                return None

            if card == CARD_ECAILLE:
                # Écaille Reptile : pose Croc puis HOOK_3_2_ECAILLE_REVELEE (R8) puis sweep Gardiens
                post_ec: list[tuple[Any, ...]] = []
                if state.cfg.mode >= 3:
                    post_ec.append(("STEP_3_2_POST_ECAILLE_HOOK", s))
                post_ec.append(("SWEEP_GARDIENS_NOW",))
                if state.cfg.accessories_enabled:
                    targets_croc = list_targeted_parcels(state)
                    if len(targets_croc) == 1:
                        prim_creation_entite(
                            state, "CROC", ray=targets_croc[0][0], p=targets_croc[0][1]
                        )
                        push_continuation_sequence(state, post_ec)
                        return None
                    if len(targets_croc) > 1:
                        gov_r = _governor_for_peuple(state, "R")
                        req_c = DecisionRequest(
                            decideur=gov_r,
                            decision_type=DEC_REPTILE_POSE_CROC_3_2,
                            options=targets_croc,
                            context={"tour": state.tour, "seat_ecaille": s},
                        )
                        push_continuation_sequence(
                            state,
                            (
                                ("WAIT_DECISION", req_c),
                                ("APPLY_REPTILE_CROC_3_2",),
                                *post_ec,
                            ),
                        )
                        return req_c
                push_continuation_sequence(state, post_ec)
                return None
            sweep_gardiens(state)
        return None

    if tag == "STEP_3_2_POST_ECAILLE_HOOK":
        _, s_ec = state._continuation.pop(0)
        dispatch_hook(state, HOOK_3_2_ECAILLE_REVELEE, {"seat": int(s_ec)})
        return None

    if tag == "STEP_3_2_BUG_DEVIATIONS":
        state._continuation.pop(0)
        dispatch_hook(state, HOOK_3_2_REVELATION, {"phase": "BUG_DEVIATIONS"})
        return None

    if tag == "BUG_B_CONTINUE_3_2":
        _, next_seat = state._continuation.pop(0)
        _bug_b_step_queue(state, int(next_seat))
        return None

    if tag == "STEP_3_2_REVES_SCAN":
        _, first_entry_i = state._continuation.pop(0)
        if int(first_entry_i):
            _bind_remaining_active_mobiles_3_2(state)
        trk = _get_active_telemetry()
        # Chercher le Rêve le plus à gauche portant >= 1 Défenseur DEBOUT (non encore résolu, INV-15)
        for r_idx in range(TRACK_LEN):
            code_m = state.get_tactique_at_rank(r_idx)
            if not is_reve_code(code_m):
                continue
            r_num = code_m - TILE_R_BASE
            if state.has_reve_opened_this_turn(r_num):
                continue
            if state.count_reve_activation_defenders_at_case(r_idx + 1) < 1:
                continue
            # Trouvé : exécuter PRE_CANCEL (R5/R6/R9), puis annulations + OPEN, puis reprendre scan gauche->droite
            push_continuation_sequence(
                state,
                (
                    ("STEP_3_2_REVE_AFTER_PRE", r_num),
                    ("STEP_3_2_REVES_SCAN", 0),
                ),
            )
            if state.cfg.mode >= 3:
                dispatch_hook(
                    state,
                    HOOK_3_2_OUVERTURE_REVE,
                    {
                        "phase": "PRE_CANCEL",
                        "slot_id": f"R{r_num}",
                        "r_num": r_num,
                        "r_idx": r_idx,
                        "case": r_idx + 1,
                    },
                )
            return None

        # Aucun Rêve debout restant : lier définitivement toutes les mobiles encore actives
        _bind_remaining_active_mobiles_3_2(state)
        if trk is not None:
            for r_idx in range(TRACK_LEN):
                code_m = state.get_tactique_at_rank(r_idx)
                if is_reve_code(code_m) and not state.has_reve_opened_this_turn(code_m - TILE_R_BASE):
                    case_1_6 = r_idx + 1
                    byp = 0
                    for s in range(n):
                        if (
                            state.was_seat_altered_this_turn(s)
                            or state.was_seat_cancelled_by_reve_this_turn(s)
                        ):
                            continue
                        card, _, _, lec_m, bound_t = state.get_player_hand(s)
                        if 1 <= card <= 12 and bound_t == case_1_6:
                            r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                            if not state.is_machine_etouffee_this_turn(r_m, mt_m):
                                byp += 1
                    if byp > 0:
                        trk.on_machines_bypassed_inactive_reve(byp)
        return None

    if tag == "STEP_3_2_REVE_AFTER_PRE":
        _, r_num_raw = state._continuation.pop(0)
        r_num = int(r_num_raw)
        cur_r_idx = state.find_tactique_rank(TILE_R_BASE + r_num)
        if cur_r_idx is None or state.has_reve_opened_this_turn(r_num):
            return None
        case_1_6 = cur_r_idx + 1
        n_def = state.count_reve_activation_defenders_at_case(case_1_6)
        if n_def < 1:
            return None

        entries: list[tuple[int, int, int, int, int]] = []
        for s in range(n):
            if (
                state.was_seat_altered_this_turn(s)
                or state.was_seat_cancelled_by_reve_this_turn(s)
            ):
                continue
            card, d1, d2, lec_m, _ = state.get_player_hand(s)
            if 1 <= card <= 12 and lec_m == case_1_6:
                r_m, mt_m = (card - 1) // 2, (card - 1) % 2
                if not state.is_machine_etouffee_this_turn(r_m, mt_m):
                    entries.append((s, card, d1, d2, lec_m))

        entries_tup = tuple(entries)
        extra_list: list[tuple[int, int, int, int, int]] = []
        if state.cfg.mode >= 3:
            dispatch_hook(
                state,
                HOOK_3_2_OUVERTURE_REVE,
                {
                    "phase": "CANDIDATES",
                    "slot_id": f"R{r_num}",
                    "r_num": r_num,
                    "r_idx": cur_r_idx,
                    "case": case_1_6,
                    "own_entries": entries_tup,
                    "extra_entries": extra_list,
                },
            )
        own_seats = {e[0] for e in entries_tup}
        extra_tup = tuple(e for e in extra_list if e[0] not in own_seats)
        all_entries = entries_tup + extra_tup

        if len(all_entries) > n_def:
            # INV-15 : surcharge -> le propriétaire du Rêve choisit quelle(s) machine(s) Étouffer
            seat_list = tuple(e[0] for e in all_entries)
            combos = tuple(combinations(seat_list, n_def))
            gov_r = _governor_for_peuple(state, SYNERGY_META[f"R{r_num}"][1])
            req_rev = DecisionRequest(
                decideur=gov_r,
                decision_type=DEC_CHOIX_CIBLE_REVE_3_2,
                options=combos,
                context={
                    "case": case_1_6,
                    "r_num": r_num,
                    "tile_id": f"R{r_num}",
                    "n_def": n_def,
                    "entries": tuple((e[0], e[1]) for e in all_entries),
                    "tour": state.tour,
                },
            )
            push_continuation_sequence(
                state,
                (
                    ("WAIT_DECISION", req_rev),
                    ("APPLY_CHOIX_CIBLE_REVE_3_2", cur_r_idx, r_num, entries_tup, extra_tup),
                ),
            )
            return req_rev

        cancelled_all = tuple(e[0] for e in all_entries)
        _resolve_defended_reve_3_2(state, cur_r_idx, r_num, entries_tup, cancelled_all, extra_tup)
        return None

    if tag == "STEP_3_2_POST_REVE_FINISH":
        _, r_num_raw, lit_reve_i, cancelled_seats = state._continuation.pop(0)
        r_num = int(r_num_raw)
        # INV-15 : coucher à plat tous les Défenseurs encore debout sur ce Rêve désormais résolu
        cur_idx = state.find_tactique_rank(TILE_R_BASE + r_num)
        if cur_idx is not None:
            laid = state.lay_down_all_defenders_on_reve(cur_idx + 1)
            if laid > 0:
                _record_phys_ops(state, laid)

        # G12 Face 2 (L'Ibijau) : si une machine déplacée par G12 F2 vient d'être Étouffée par ce Rêve,
        # Oiseau peut aussitôt Glisser ce Rêve d'1 rang libre vers la gauche.
        if (
            state.cfg.mode >= 3
            and state.cfg.profile_for_slot("G12") is not None
            and cur_idx is not None
            and cur_idx > 0
            and not is_reve_code(state.get_tactique_at_rank(cur_idx - 1))
            and any(state.was_seat_ibijau_moved_f2(int(s_c)) for s_c in cancelled_seats)
        ):
            gov_o = _governor_for_peuple(state, "O")
            push_continuation_sequence(state, (("STEP_3_2_POST_REVE_SWEEP", int(lit_reve_i)),))
            push_effect_decision(
                state,
                gov_o,
                ("GLISSER", "PASSER"),
                {
                    "effect_kind": "G12_F2_SLIDE_REVE",
                    "r_num": r_num,
                    "rank": cur_idx + 1,
                },
                slot_id="G12",
                profile=state.cfg.profile_for_slot("G12") or "A",
                resume_tag="G12_F2_SLIDE_REVE",
                resume_payload=(r_num,),
            )
            return None

        if int(lit_reve_i) or state.is_trigger_lit(TRIG_REVE):
            state.light_trigger(TRIG_REVE)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(TRIG_REVE)
        sweep_gardiens(state)
        return None

    if tag == "STEP_3_2_POST_REVE_SWEEP":
        _, lit_reve_i = state._continuation.pop(0)
        if int(lit_reve_i) or state.is_trigger_lit(TRIG_REVE):
            state.light_trigger(TRIG_REVE)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(TRIG_REVE)
        sweep_gardiens(state)
        return None

    if tag == "STEP_3_2_POST":
        state._continuation.pop(0)
        dispatch_hook(state, HOOK_3_2_APRES_REVELATION, {})
        return None

    if tag == "STEP_3_2_END":
        state._continuation.pop(0)
        sweep_gardiens(state)
        if not has_pending_decision(state):
            _transition_step(state, STEP_4_1_FURTIVITE)
        else:
            state._continuation.append(("TRANSITION_TO_STEP", STEP_4_1_FURTIVITE))
        return None

    if tag == "TRANSITION_TO_STEP":
        _, dst_step = state._continuation.pop(0)
        _transition_step(state, int(dst_step))
        return None

    if tag == "RESUME_STEP_4_1":
        _, next_flat = state._continuation.pop(0)
        _run_step_4_1_from(state, int(next_flat))
        return None

    if tag == "RESUME_MACHINE_ATTACK_5":
        (
            _,
            ray,
            m_type,
            t_code,
            eff_ratissage_i,
            targets,
            next_t_idx,
            dmg_cnt,
            parried_cnt,
            exec_cnt,
            unp_sp,
            unp_dev,
            soldats_dec_idx,
        ) = state._continuation.pop(0)
        t_code_i = int(t_code)
        t_spec = RATISSAGE_TACTIQUE_SPEC if t_code_i == 0 else TACTIQUES_SPEC[t_code_i]
        _resolve_machine_targets_from(
            state,
            int(ray),
            int(m_type),
            t_spec,
            bool(eff_ratissage_i),
            targets,
            int(next_t_idx),
            int(dmg_cnt),
            int(parried_cnt),
            int(exec_cnt),
            int(unp_sp),
            int(unp_dev),
            int(soldats_dec_idx),
        )
        return None

    if tag == "STEP2_REV_QUEUE":
        seats_tuple: tuple[int, ...] = top[1]
        cursor = int(top[2])
        if cursor < len(seats_tuple):
            seat = seats_tuple[cursor]
            if state.is_player_def2_definitif(seat) or state.get_player_def_loc_raw(seat, 1) == 0:
                state._continuation[0] = ("STEP2_REV_QUEUE", seats_tuple, cursor + 1)
                return None
            # INV-04 : clôture à N-1 joueurs validés -> au plus 1 ultime ajustement puis validation Définitif
            refl_remaining = sum(
                1
                for s_chk in range(n)
                if state.get_player_def_loc_raw(s_chk, 1) != 0
                and not state.is_player_def2_definitif(s_chk)
            )
            final_n_minus_1 = refl_remaining == 1
            cur_spot = _current_def_canonical_spot(state, seat, 1)
            legal_t = list_legal_targets(
                state, seat, is_first_defender=False, exclude_own_def2=True
            )
            if final_n_minus_1:
                rev_opts: list[tuple[str, Any]] = [("VERROUILLER_DEFINITIF", None)]
                for t in legal_t:
                    if t != cur_spot:
                        rev_opts.append(("DEPLACER_DEFINITIF", t))
            else:
                rev_opts = [
                    ("GARDER_REFLEXION", None),
                    ("VERROUILLER_DEFINITIF", None),
                ]
                for t in legal_t:
                    if t != cur_spot:
                        rev_opts.append(("DEPLACER_REFLEXION", t))
                        rev_opts.append(("DEPLACER_DEFINITIF", t))
            pass_idx, _ = state.get_step2_pass_state()
            req = DecisionRequest(
                decideur=seat,
                decision_type=DEC_REVISION_DEFENSEUR_2,
                options=tuple(rev_opts),
                context={
                    "tour": state.tour,
                    "pass": pass_idx,
                    "final_adjustment_n_minus_1": final_n_minus_1,
                },
            )
            push_continuation_sequence(state, (("WAIT_DECISION", req),))
            return req

        state._continuation.pop(0)
        pass_idx, moved = state.get_step2_pass_state()
        rem_seats = tuple(
            (state.coordonnateur + off) % n
            for off in range(n)
            if state.get_player_def_loc_raw((state.coordonnateur + off) % n, 1) != 0
            and not state.is_player_def2_definitif((state.coordonnateur + off) % n)
        )
        if not moved or pass_idx >= state.cfg.max_revision_passes or not rem_seats:
            lock_all_def2_in_place(state)
            _transition_step(state, STEP_3_1_CONSTRUCT)
        else:
            state.set_step2_pass_state(pass_idx + 1, False)
            state._continuation.append(("STEP2_REV_QUEUE", rem_seats, 0))
        return None

    if tag == "CONSTRUCT_SLOT":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        return _begin_single_construction(state, slot_idx)

    if tag == "SEND_REMAINING_BUILDERS_WAITING_3_1":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        _send_slot_builders_to_waiting(state, slot_idx)
        return None

    if tag == "CHECK_LIBERATION_3_1":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        lib_mode = "ONE" if n == 3 else "NONE"
        if state.cfg.mode >= 3:
            lib_ctx: dict[str, Any] = {
                "liberation_query": True,
                "constructed_slot_id": state.cfg.lisiere_slots[slot_idx],
                "slot_idx": slot_idx,
                "n_players": n,
                "liberate_mode": lib_mode,
            }
            dispatch_hook(state, HOOK_3_1_CONSTRUCTION, lib_ctx)
            lib_mode = str(lib_ctx.get("liberate_mode", lib_mode))

        if lib_mode == "NONE":
            return None

        if lib_mode == "ALL_BY_OWNER":
            if not _valid_adjacent_first_parcels_3_1(state, slot_idx):
                return None
            tracked_b = _tracked_builders_on_slot(state, slot_idx)
            _, nb_b = state.get_lisiere_tile_state(slot_idx)
            untracked_cnt = max(0, nb_b - len(tracked_b))
            builders_q: tuple[tuple[int, int], ...] = (
                *tracked_b,
                *((-1, 0) for _ in range(untracked_cnt)),
            )
            if builders_q:
                push_continuation_sequence(
                    state, (("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, 0),)
                )
            return None

        lib_opts = _liberation_options_one(state, slot_idx)
        if len(lib_opts) == 1:
            _apply_builder_liberation(state, slot_idx, lib_opts[0])
        elif len(lib_opts) > 1:
            tile_id = state.cfg.lisiere_slots[slot_idx]
            _, orig, _ = SYNERGY_META[tile_id]
            gov = _governor_for_peuple(state, orig)
            req = DecisionRequest(
                decideur=gov,
                decision_type=DEC_LIBERATION_BATISSEUR_3_1,
                options=lib_opts,
                context={"slot_idx": slot_idx, "tile_id": tile_id},
            )
            push_continuation_sequence(
                state, (("WAIT_DECISION", req), ("APPLY_LIBERATION_3_1", slot_idx))
            )
            return req
        return None

    if tag == "LIBERATION_ALL_QUEUE_3_1":
        _, slot_idx_raw, builders_q_raw, cursor_raw = state._continuation.pop(0)
        slot_idx = int(slot_idx_raw)
        builders_q = tuple(builders_q_raw)
        cursor = int(cursor_raw)
        if cursor >= len(builders_q):
            return None
        valid_rays = _valid_adjacent_first_parcels_3_1(state, slot_idx)
        if not valid_rays:
            return None
        b_seat, b_def = builders_q[cursor]
        still_present = False
        if b_seat >= 0:
            raw_loc = state.get_player_def_loc_raw(b_seat, b_def)
            if raw_loc != 0:
                dk, da, _, _ = state.decode_def_loc(raw_loc)
                still_present = dk == "LISIERE" and da == slot_idx
        else:
            still_present = state.get_lisiere_tile_state(slot_idx)[1] >= 1

        if not still_present:
            if cursor + 1 < len(builders_q):
                push_continuation_sequence(
                    state, (("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1),)
                )
            return None

        owner_opts = tuple((b_seat, b_def, r, p_first) for r, p_first in valid_rays)
        if len(owner_opts) == 1:
            _apply_builder_liberation(state, slot_idx, owner_opts[0])
            if cursor + 1 < len(builders_q):
                push_continuation_sequence(
                    state, (("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1),)
                )
            return None

        tile_id = state.cfg.lisiere_slots[slot_idx]
        _, orig, _ = SYNERGY_META[tile_id]
        dec_owner = b_seat if 0 <= b_seat < n else _governor_for_peuple(state, orig)
        req_owner = DecisionRequest(
            decideur=dec_owner,
            decision_type=DEC_LIBERATION_BATISSEUR_3_1,
            options=owner_opts,
            context={"slot_idx": slot_idx, "tile_id": tile_id, "builder_index": cursor},
        )
        seq_frames: list[tuple[Any, ...]] = [
            ("WAIT_DECISION", req_owner),
            ("APPLY_LIBERATION_3_1", slot_idx),
        ]
        if cursor + 1 < len(builders_q):
            seq_frames.append(("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1))
        push_continuation_sequence(state, seq_frames)
        return req_owner

    if tag == "NID_PRODUCE_AFTER_MOVE_4_2":
        _, m_num_raw = state._continuation.pop(0)
        m_num = int(m_num_raw)
        pos_info = state.get_nid_position(m_num)
        if pos_info is None:
            return None
        r_n, p_n, _ = pos_info
        cur_ins = state.get_parcel_insectes(r_n, p_n)
        created = 1 if cur_ins <= 1 else 2
        push_continuation_sequence(
            state,
            (
                ("NID_DEPLOY_INSECT_4_2", m_num, created),
                ("NID_POST_PROD_4_2", m_num),
                ("SWEEP_GARDIENS_NOW",),
            ),
        )
        return None

    if tag == "NID_DEPLOY_INSECT_4_2":
        _, m_num_raw, rem_raw = state._continuation.pop(0)
        m_num = int(m_num_raw)
        rem = int(rem_raw)
        if rem <= 0:
            return None
        pos_info = state.get_nid_position(m_num)
        if pos_info is None:
            return None
        r_n, p_n, _ = pos_info
        opts_dep = _list_nid_deploy_options(state, r_n, p_n)
        if not opts_dep:
            return None
        if len(opts_dep) == 1:
            _apply_nid_deploy_choice_4_2(state, opts_dep[0])
            if rem > 1:
                push_continuation_sequence(state, (("NID_DEPLOY_INSECT_4_2", m_num, rem - 1),))
            return None
        gov_i = _governor_for_peuple(state, "I")
        req_dep = DecisionRequest(
            decideur=gov_i,
            decision_type=DEC_DEPLOIEMENT_NID_4_2,
            options=opts_dep,
            context={
                "m_num": m_num,
                "tile_id": f"M{m_num}",
                "ray": r_n,
                "p": p_n,
                "remaining": rem,
                "tour": state.tour,
            },
        )
        push_continuation_sequence(
            state,
            (
                ("WAIT_DECISION", req_dep),
                ("APPLY_DEPLOIEMENT_NID_4_2", m_num, rem),
            ),
        )
        return req_dep

    if tag == "NID_POST_PROD_4_2":
        _, m_num_raw = state._continuation.pop(0)
        m_num = int(m_num_raw)
        pos_info = state.get_nid_position(m_num)
        if pos_info is None:
            return None
        r_n, p_n, _ = pos_info
        dispatch_hook(
            state,
            HOOK_4_2_NID_APRES_PROD,
            {"slot_id": f"M{m_num}", "m_num": m_num, "ray": r_n, "p": p_n},
        )
        return None

    if tag == "TACTIQUE_RANK_5_1":
        # Toujours résoudre le rang 1..6 le plus bas ayant encore une mobile active (couvre aussi G12)
        found_code = 0
        eligible_m: list[tuple[int, int]] = []
        for rank_idx in range(TRACK_LEN):
            t_code_cand = rank_idx + 1
            cand_m = _eligible_tactique_machines_at_rank(state, t_code_cand)
            if cand_m:
                found_code = t_code_cand
                eligible_m = cand_m
                break
        if found_code == 0:
            state._continuation.pop(0)
            _transition_step(state, STEP_5_2_RATISSAGE)
            return None
        if len(eligible_m) == 1:
            rm, mt = eligible_m[0]
            _resolve_tactique_5_1_machine(state, rm, mt, found_code)
            return None
        req = DecisionRequest(
            decideur=state.coordonnateur,
            decision_type=DEC_ORDRE_ATTAQUE_5_1,
            options=tuple(eligible_m),
            context={"rank": found_code, "tactique": code_to_tile_id(found_code)},
        )
        push_continuation_sequence(
            state, (("WAIT_DECISION", req), ("APPLY_TACTIQUE_5_1", found_code))
        )
        return req

    if tag == "STEP_5_3_FINISH":
        state._continuation.pop(0)
        sweep_gardiens(state)
        if has_pending_decision(state):
            state._continuation.append(("STEP_5_3_CLEAN_TRAPS",))
            return None
        return _resolve_gardien_bets_5_3_from(state, 1, 0, 0, 0, 0)

    if tag == "STEP_5_3_CLEAN_TRAPS":
        state._continuation.pop(0)
        return _resolve_gardien_bets_5_3_from(state, 1, 0, 0, 0, 0)

    if tag == "STEP_6_1_ENRACINEMENT_QUEUE":
        _, seats_q, cur_idx = state._continuation.pop(0)
        s_pos = int(cur_idx)
        while s_pos < len(seats_q):
            s = int(seats_q[s_pos])
            opts_r = _eligible_rooting_options_for_seat(state, s)
            if len(opts_r) <= 1:
                s_pos += 1
                continue
            req_root = DecisionRequest(
                decideur=s,
                decision_type=DEC_ENRACINEMENT_6_1,
                options=opts_r,
                context={"seat": s, "peuple": state.cfg.peuples[s], "tour": state.tour},
            )
            seq_r: list[tuple[Any, ...]] = [
                ("WAIT_DECISION", req_root),
                ("APPLY_ENRACINEMENT_6_1", s),
            ]
            if s_pos + 1 < len(seats_q):
                seq_r.append(("STEP_6_1_ENRACINEMENT_QUEUE", seats_q, s_pos + 1))
            else:
                seq_r.append(("TRANSITION_TO_STEP", STEP_6_3_END_TURN))
            push_continuation_sequence(state, seq_r)
            return req_root
        _transition_step(state, STEP_6_3_END_TURN)
        return None

    raise RuntimeError(f"Continuation inconnue : {tag}")


def _advance_main_step(state: GameState) -> DecisionRequest | GameOver | None:
    """Exécute un pas de l'étape principale state.step."""
    n = state.cfg.n_players
    step = state.step

    if step == STEP_GAME_OVER:
        return apply_repousse_finale(state)

    if step == STEP_1_2_DEAL:
        # INV-06 : distribution horaire depuis le Coordonnateur en servant TOUJOURS l'Oiseau (O) en dernier
        seat_o = state.cfg.seat_of_peuple("O")
        order_non_o = [
            (state.coordonnateur + off) % n
            for off in range(n)
            if (state.coordonnateur + off) % n != seat_o
        ]
        dealt = 0
        shortages = 0
        for s in order_non_o:
            c = state.draw_next_machine_card()
            state.set_player_hand(s, c, 0, 0, 0, 0)
            if c != CARD_NONE:
                dealt += 1
            else:
                shortages += 1

        if seat_o is not None:
            if state.cfg.accessories_enabled:
                c1 = state.draw_next_machine_card()
                c2 = state.draw_next_machine_card()
                if c1 == CARD_NONE:
                    state.set_player_hand(seat_o, CARD_NONE, 0, 0, 0, 0)
                    state.oiseau_perchoir_card = CARD_NONE
                    shortages += 1
                elif c2 == CARD_NONE:
                    state.set_player_hand(seat_o, c1, 0, 0, 0, 0)
                    state.oiseau_perchoir_card = CARD_NONE
                    dealt += 1
                elif c1 == c2:
                    state.set_player_hand(seat_o, c1, 0, 0, 0, 0)
                    state.oiseau_perchoir_card = c2
                    dealt += 1
                else:
                    dealt += 1
                    if dealt > 0:
                        _record_phys_ops(state, dealt)
                    if shortages > 0:
                        trk = _get_active_telemetry()
                        if trk is not None:
                            trk.ok_penurie_cartes_machine += shortages
                    req_p = DecisionRequest(
                        decideur=seat_o,
                        decision_type=DEC_OISEAU_PERCHOIR_1_1,
                        options=(c1, c2),
                        context={"tour": state.tour, "candidates": (c1, c2)},
                    )
                    push_continuation_sequence(
                        state,
                        (
                            ("WAIT_DECISION", req_p),
                            ("APPLY_OISEAU_PERCHOIR_1_1", seat_o, c1, c2),
                        ),
                    )
                    return req_p
            else:
                c_o = state.draw_next_machine_card()
                state.set_player_hand(seat_o, c_o, 0, 0, 0, 0)
                if c_o != CARD_NONE:
                    dealt += 1
                else:
                    shortages += 1

        if dealt > 0:
            _record_phys_ops(state, dealt)
        if shortages > 0:
            trk = _get_active_telemetry()
            if trk is not None:
                trk.ok_penurie_cartes_machine += shortages
        _transition_step(state, STEP_1_3_DICE)
        return None

    if step == STEP_1_3_DICE:
        # INV-07 v6.4 : lancer universel de 2 dés standards 1..6 pour TOUS (0 Dé d'Envol).
        # L'Oiseau (O) choisit librement lequel de ses 2 dés (d1 ou d2) il retient s'il tient une machine.
        dice_ops = 0
        state.set_oiseau_chose_d2(False)
        for s in range(n):
            card, _, _, _, _ = state.get_player_hand(s)
            peuple_id = PEUPLE_TO_ID[state.cfg.peuples[s]]
            d1 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 0)
            d2 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 1)
            lec_m = min(d1, d2) if (1 <= card <= 12) else 0
            state.set_player_hand(s, card, d1, d2, lec_m, 0)
            dice_ops += 2

        seat_o = state.cfg.seat_of_peuple("O")
        if seat_o is not None and state.cfg.accessories_enabled:
            card_o, d1_o, d2_o, _, _ = state.get_player_hand(seat_o)
            if 1 <= card_o <= 12:
                if d1_o != d2_o:
                    _record_phys_ops(state, dice_ops)
                    req_ch_d = DecisionRequest(
                        decideur=seat_o,
                        decision_type=DEC_OISEAU_CHOIX_DE_1_3,
                        options=(d1_o, d2_o),
                        context={
                            "tour": state.tour,
                            "card": card_o,
                            "d1": d1_o,
                            "d2": d2_o,
                            "min_d": min(d1_o, d2_o),
                            "max_d": max(d1_o, d2_o),
                        },
                    )
                    push_continuation_sequence(
                        state,
                        (
                            ("WAIT_DECISION", req_ch_d),
                            ("APPLY_OISEAU_CHOIX_DE_1_3", seat_o, d1_o, d2_o),
                            ("STEP_1_3_FINISH",),
                        ),
                    )
                    return req_ch_d
                # d1_o == d2_o : aucun choix distinct, d1 retenu et d2 écarté
                state.set_oiseau_chose_d2(False)

        if dice_ops > 0:
            _record_phys_ops(state, dice_ops)
        if state.cfg.mode >= 3:
            state._continuation.append(("STEP_1_3_HOOK_QUEUE", 0))
            return None
        _transition_step(state, STEP_2_1_DEF1)
        return None

    if step == STEP_2_1_DEF1:
        for off in range(n):
            s = (state.coordonnateur + off) % n
            if state.get_player_def_loc_raw(s, 0) == 0:
                if (
                    state.cfg.accessories_enabled
                    and state.cfg.peuples[s] == "H"
                    and state.get_humain_chaman_archetype(0) == CHAMAN_NONE
                ):
                    req_ch = DecisionRequest(
                        decideur=s,
                        decision_type=DEC_HUMAIN_CHAMAN_2_1,
                        options=(CHAMAN_TAMBOUR, CHAMAN_CHANT),
                        context={"tour": state.tour, "step": "2.1"},
                    )
                    push_continuation_sequence(
                        state, (("WAIT_DECISION", req_ch), ("APPLY_HUMAIN_CHAMAN_2_1", s))
                    )
                    return req_ch
                opts_1 = list_legal_targets(state, s, is_first_defender=True) or (("PASSER_IMPASSE",),)
                req = DecisionRequest(
                    s, DEC_POSE_DEFENSEUR_1, opts_1, _STEP_2_1_CTX_BY_TOUR[state.tour]
                )
                push_continuation_sequence(state, (("WAIT_DECISION", req), ("APPLY_DEF1", s)))
                return req
        state.set_step2_pass_state(0, False)
        _transition_step(state, STEP_2_2_DEF2)
        return None

    if step == STEP_2_2_DEF2:
        for off in range(n):
            s = (state.coordonnateur + off) % n
            if state.get_player_def_loc_raw(s, 1) == 0:
                legal_2 = list_legal_targets(state, s, is_first_defender=False)
                if not legal_2:
                    opts_2: tuple[tuple[str, Any], ...] = (("POSER_DEFINITIF", ("PASSER_IMPASSE",)),)
                elif state.cfg.max_revision_passes <= 0:
                    opts_2 = tuple(_DEF2_DEFINITIF_WRAP[t] for t in legal_2)
                else:
                    built_2: list[tuple[str, Any]] = []
                    for t in legal_2:
                        built_2.append(_DEF2_DEFINITIF_WRAP[t])
                        built_2.append(_DEF2_REFLEXION_WRAP[t])
                    opts_2 = tuple(built_2)
                req = DecisionRequest(
                    s, DEC_POSE_DEFENSEUR_2, opts_2, _STEP_2_2_CTX_BY_TOUR[state.tour]
                )
                push_continuation_sequence(
                    state, (("WAIT_DECISION", req), ("APPLY_DEF2_INIT", s))
                )
                return req

        if state.cfg.max_revision_passes <= 0:
            lock_all_def2_in_place(state)
            _transition_step(state, STEP_3_1_CONSTRUCT)
            return None

        refl_seats = tuple(
            (state.coordonnateur + off) % n
            for off in range(n)
            if state.get_player_def_loc_raw((state.coordonnateur + off) % n, 1) != 0
            and not state.is_player_def2_definitif((state.coordonnateur + off) % n)
        )
        if not refl_seats:
            lock_all_def2_in_place(state)
            _transition_step(state, STEP_3_1_CONSTRUCT)
        else:
            state.set_step2_pass_state(1, False)
            state._continuation.append(("STEP2_REV_QUEUE", refl_seats, 0))
        return None

    if step == STEP_3_1_CONSTRUCT:
        if state.cfg.mode == 1:
            _transition_step(state, STEP_3_2_REVEAL)
            return None
        ready_slots = [
            (state.coordonnateur * 2 + off) % (2 * n)
            for off in range(2 * n)
            if state.get_lisiere_tile_state((state.coordonnateur * 2 + off) % (2 * n))
            == (LISIERE_UNCONSTRUCTED, 2)
        ]
        if not ready_slots:
            _transition_step(state, STEP_3_2_REVEAL)
            return None
        if len(ready_slots) == 1:
            state._continuation.append(("CONSTRUCT_SLOT", ready_slots[0]))
            return None
        req = DecisionRequest(
            state.coordonnateur,
            DEC_ORDRE_CONSTRUCTION_3_1,
            tuple(ready_slots),
            {"tiles": [state.cfg.lisiere_slots[idx] for idx in ready_slots], "tour": state.tour},
        )
        push_continuation_sequence(state, (("WAIT_DECISION", req), ("APPLY_CONSTRUCT_ORDER",)))
        return req

    if step == STEP_3_2_REVEAL:
        _run_step_3_2(state)
        return None

    if step == STEP_4_1_FURTIVITE:
        _run_step_4_1_from(state, 0)
        return None

    if step == STEP_4_2_NIDS:
        # INV-21 v6.4 : Déploiement direct à la Production (0 étape 4.3 Migration -> direct vers 5.1)
        if state.cfg.mode == 1 or not state.cfg.has_insectes_peuple:
            _transition_step(state, STEP_5_1_TACTIQUES)
            return None
        eligible_nids: list[int] = []
        for m_num in range(1, 6):
            pos_info = state.get_nid_position(m_num)
            if pos_info is not None:
                r, p, active_turn = pos_info
                if not active_turn and state.get_parcel_defenseurs(r, p) >= 1:
                    eligible_nids.append(m_num)
        if not eligible_nids:
            _transition_step(state, STEP_5_1_TACTIQUES)
            return None
        if len(eligible_nids) == 1:
            _resolve_nid_block(state, eligible_nids[0])
            return None
        gov = _governor_for_peuple(state, "I")
        req = DecisionRequest(gov, DEC_ORDRE_NID_4_2, tuple(eligible_nids), {"tour": state.tour})
        push_continuation_sequence(state, (("WAIT_DECISION", req), ("APPLY_NID_4_2",)))
        return req

    if step == STEP_5_1_TACTIQUES:
        state._continuation.append(("TACTIQUE_RANK_5_1", 0))
        if state.cfg.mode >= 3:
            dispatch_hook(state, HOOK_5_DEBUT, {})
        return None

    if step == STEP_5_2_RATISSAGE:
        eligible_s = _eligible_ratissage_machines(state)
        if not eligible_s:
            _transition_step(state, STEP_5_3_END_CHECK)
            return None
        if len(eligible_s) == 1:
            rm, mt = eligible_s[0]
            resolve_single_machine_attack(
                state, rm, mt, RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
            )
            return None
        req = DecisionRequest(
            state.coordonnateur, DEC_ORDRE_RATISSAGE_5_2, tuple(eligible_s), {"tour": state.tour}
        )
        push_continuation_sequence(state, (("WAIT_DECISION", req), ("APPLY_RATISSAGE_5_2",)))
        return req

    if step == STEP_5_3_END_CHECK:
        if state.cfg.mode >= 3:
            push_continuation_sequence(state, (("STEP_5_3_FINISH",),))
            dispatch_hook(state, HOOK_5_3_PRE_RETRAIT, {})
            return None
        dispatch_hook(state, HOOK_5_3_PRE_RETRAIT, {})
        req_b = _resolve_gardien_bets_5_3_from(state, 1, 0, 0, 0, 0)
        if req_b is not None:
            return req_b
        if state.step == STEP_GAME_OVER:
            return apply_repousse_finale(state)
        return None

    if step == STEP_6_2_EVOLUTION:
        return _run_step_6_2(state)

    if step == STEP_6_1_ENRACINEMENT:
        if not state.cfg.enracinement_enabled or state.cfg.mode < 2:
            _transition_step(state, STEP_6_3_END_TURN)
            return None
        seats_q = tuple((state.coordonnateur + off) % n for off in range(n))
        push_continuation_sequence(state, (("STEP_6_1_ENRACINEMENT_QUEUE", seats_q, 0),))
        return None

    if step == STEP_6_3_END_TURN:
        _transition_eligible_machines_to_ratissage(state)
        state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
        _record_phys_ops(state, 1)
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_end_turn(state, game_over=False)
        state.coordonnateur = (state.coordonnateur + 1) % n
        state.tour += 1
        _transition_step(state, STEP_1_2_DEAL)
        return None

    raise RuntimeError(f"Étape moteur inconnue : {step}")


def step_until_decision(
    state: GameState,
    *,
    max_internal_steps: int = 2000,
    telemetry: Any | None = None,
) -> DecisionRequest | GameOver:
    """Avance la machine à états jusqu'à la prochaine DecisionRequest ou jusqu'à GameOver."""
    ensure_builtin_migration_registered()
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        internal_steps = 0
        while True:
            internal_steps += 1
            if internal_steps > max_internal_steps:
                cfg = state.cfg
                raise RuntimeError(
                    f"Cycle interne détecté (> {max_internal_steps} sous-transitions) : "
                    f"mode={cfg.mode}, profil_piste={cfg.profil_piste}, n_players={cfg.n_players}, "
                    f"exp_seed={cfg.exp_seed}, rep_id={cfg.rep_id}, tour={state.tour}, "
                    f"step={state.step}, continuation={state._continuation!r}"
                )
            if state._continuation:
                res_cont = _advance_continuation(state)
                if res_cont is not None:
                    return res_cont
                continue
            res_step = _advance_main_step(state)
            if res_step is not None:
                return res_step
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


def _begin_single_construction(state: GameState, slot_idx: int) -> DecisionRequest | None:
    """Construit la tuile en lisière `slot_idx` (suspend si un choix de gouverneur est requis)."""
    st, nb = state.get_lisiere_tile_state(slot_idx)
    if st != LISIERE_UNCONSTRUCTED or nb < 2:
        return None
    return _finish_single_construction_after_cost(state, slot_idx)


def _finish_single_construction_after_cost(
    state: GameState, slot_idx: int
) -> DecisionRequest | None:
    _, nb = state.get_lisiere_tile_state(slot_idx)
    tile_id = state.cfg.lisiere_slots[slot_idx]
    fam, orig_code, num = SYNERGY_META[tile_id]
    gov = _governor_for_peuple(state, orig_code)
    constr_ctx: dict[str, Any] = {
        "slot_id": tile_id,
        "slot_idx": slot_idx,
        "allowed_cases": tuple(range(1, TRACK_LEN + 1)),
    }
    dispatch_hook(state, HOOK_3_1_CONSTRUCTION, constr_ctx)

    post_frames = (
        ("CHECK_LIBERATION_3_1", slot_idx),
        ("SEND_REMAINING_BUILDERS_WAITING_3_1", slot_idx),
    )

    if fam == FAMILLE_GARDIEN:
        allowed_cases = tuple(int(c) for c in constr_ctx.get("allowed_cases", ()))
        free_cases = tuple(
            c
            for c in range(1, TRACK_LEN + 1)
            if state.get_gardien_at_case(c)[0] == 0 and (not allowed_cases or c in allowed_cases)
        )
        if not free_cases:
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
            push_continuation_sequence(state, post_frames)
            return None
        if len(free_cases) == 1:
            state.set_gardien_at_case(free_cases[0], num, 1)
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
            _record_phys_ops(state, 1)
            push_continuation_sequence(state, post_frames)
            return None
        req = DecisionRequest(
            decideur=gov,
            decision_type=DEC_CHOIX_CASE_GARDIEN,
            options=free_cases,
            context={"slot_idx": slot_idx, "tile_id": tile_id},
        )
        push_continuation_sequence(
            state,
            (
                ("WAIT_DECISION", req),
                ("APPLY_GARDIEN_CASE_3_1", slot_idx, num),
                *post_frames,
            ),
        )
        return req

    if fam == FAMILLE_REVE:
        insert_reve_on_track(state, num)
        state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
        push_continuation_sequence(state, post_frames)
        return None

    # FAMILLE_CROISSANCE (Nid M1..M5) : gouverné par I ; Bonus 3J unifié étendu aux Nids (INV-19) !
    lisiere_idx = slot_idx // 2
    r0 = lisiere_idx
    r1 = (lisiere_idx + 1) % state.cfg.n_players
    valid_parcels: list[tuple[int, int]] = []
    for r in (r0, r1):
        for p in range(1, state.cfg.p_max + 1):
            if (
                not state.is_route_forestiere(r, p)
                and not state.machines_on_parcel(r, p)
                and state.get_parcel_nid(r, p)[0] == 0
                and (r, p) not in valid_parcels
            ):
                valid_parcels.append((r, p))

    if not valid_parcels:
        state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
        push_continuation_sequence(state, post_frames)
        return None

    if len(valid_parcels) == 1:
        rn, pn = valid_parcels[0]
        state.set_parcel_nid(rn, pn, num, False)
        state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
        _record_phys_ops(state, 1)
        push_continuation_sequence(state, post_frames)
        return None

    gov_nid = _governor_for_peuple(state, "I")
    req = DecisionRequest(
        decideur=gov_nid,
        decision_type=DEC_PLACEMENT_NID_3_1,
        options=tuple(valid_parcels),
        context={"slot_idx": slot_idx, "tile_id": tile_id},
    )
    push_continuation_sequence(
        state,
        (
            ("WAIT_DECISION", req),
            ("APPLY_NID_PLACE_3_1", slot_idx, num),
            *post_frames,
        ),
    )
    return req


def _apply_nid_deploy_choice_4_2(state: GameState, dest: tuple[Any, ...]) -> None:
    """Pose 1 Insecte nouvellement produit en 4.2 sur sa destination choisie sans allumer TRIG_INSECTE (INV-21)."""
    kind = dest[0]
    if kind == "FORET":
        prim_creation_entite(
            state, "INSECTE", ray=int(dest[1]), p=int(dest[2]), count=1, light_trigger=False
        )
    elif kind == "BUG":
        prim_creation_entite(state, "BUG", p=int(dest[1]), count=1, light_trigger=False)
    elif kind == "COLONIE":
        c = int(dest[1])
        state.set_colonie_at_case(c, min(255, state.get_colonie_at_case(c) + 1))
        _record_phys_ops(state, 1)
    else:
        raise ValueError(f"Destination Déploiement Nid 4.2 invalide : {dest!r}")


def _resolve_nid_block(state: GameState, m_num: int) -> None:
    """Résout un Nid en 4.2 : HOOK_4_2_NID_AVANT_PROD (M3) -> Production + Déploiement direct -> Pouvoir -> Sweep."""
    if not state.cfg.has_insectes_peuple:
        return
    pos_info = state.get_nid_position(m_num)
    if pos_info is None:
        return
    r, p, _ = pos_info
    state.set_nid_activated(m_num, True)
    push_continuation_sequence(state, (("NID_PRODUCE_AFTER_MOVE_4_2", m_num),))
    if state.cfg.mode >= 3:
        dispatch_hook(
            state,
            HOOK_4_2_NID_AVANT_PROD,
            {"slot_id": f"M{m_num}", "m_num": m_num, "ray": r, "p": p},
        )


def _maybe_prompt_mammifere_duel(state: GameState, seat: int, target: Any, step_lbl: str) -> None:
    """Si M vient de poser un Défenseur sur une parcelle forêt, propose de poser/déplacer le Duel face DEFI."""
    if (
        not state.cfg.accessories_enabled
        or state.cfg.peuples[seat] != "M"
        or not isinstance(target, tuple)
        or len(target) < 3
        or target[0] != "FORET"
    ):
        return
    r_m, p_m = int(target[1]), int(target[2])
    if state.is_route_forestiere(r_m, p_m):
        return
    if state.get_duel_state() == (DUEL_DEFI, r_m, p_m):
        return
    req_d = DecisionRequest(
        decideur=seat,
        decision_type=DEC_MAMMIFERE_DUEL_2,
        options=("POSER_DUEL_DEFI", "PASSER"),
        context={
            "ray": r_m,
            "p": p_m,
            "step": step_lbl,
            "current_duel": state.get_duel_state(),
            "tour": state.tour,
        },
    )
    push_continuation_sequence(
        state, (("WAIT_DECISION", req_d), ("APPLY_MAMMIFERE_DUEL_2", r_m, p_m))
    )


def apply_choice(
    state: GameState,
    choice: Any,
    *,
    telemetry: Any | None = None,
) -> None:
    """Applique le choix légal répondant à la DecisionRequest courante."""
    assert state._continuation and state._continuation[0][0] == "WAIT_DECISION", (
        "Aucune DecisionRequest en attente"
    )
    _, req = state._continuation.pop(0)
    assert choice in req.options, f"Choix illégal {choice!r} hors de {req.options!r}"

    assert state._continuation, "Continuation manquante après WAIT_DECISION"
    top = state._continuation[0]
    tag = top[0]

    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.record_player_decision(state, int(req.decideur))

        if tag == "APPLY_EFFECT_CHOICE":
            _, slot_id, profile, resume_tag, resume_payload = state._continuation.pop(0)
            reg = get_tile_registration(str(slot_id), str(profile))
            assert reg is not None, f"Profil non enregistré à la reprise : {slot_id}:{profile}"
            reg.handler(
                state,
                HOOK_EFFECT_RESUME,
                {
                    "slot_id": str(slot_id),
                    "profile": str(profile),
                    "choice": choice,
                    "resume_tag": str(resume_tag),
                    "payload": resume_payload,
                },
            )
            return

        if tag == "APPLY_OISEAU_PERCHOIR_1_1":
            _, seat_o_raw, c1_raw, c2_raw = state._continuation.pop(0)
            kept = int(choice)
            perched = int(c2_raw) if kept == int(c1_raw) else int(c1_raw)
            state.set_player_hand(int(seat_o_raw), kept, 0, 0, 0, 0)
            state.oiseau_perchoir_card = perched
            _record_phys_ops(state, 1)
            _transition_step(state, STEP_1_3_DICE)
            return

        if tag == "APPLY_OISEAU_CHOIX_DE_1_3":
            _, seat_o_raw, _d1_raw, d2_raw = state._continuation.pop(0)
            seat_o = int(seat_o_raw)
            chosen_m = int(choice)
            card, d1, d2, _, bound_t = state.get_player_hand(seat_o)
            state.set_player_hand(seat_o, card, d1, d2, chosen_m, bound_t)
            state.set_oiseau_chose_d2(chosen_m == int(d2_raw))
            return

        if tag == "APPLY_HUMAIN_CHAMAN_2_1":
            _, _seat_h_raw = state._continuation.pop(0)
            state.set_humain_chaman_archetype(0, int(choice))
            return

        if tag == "APPLY_MAMMIFERE_DUEL_2":
            _, r_m, p_m = state._continuation.pop(0)
            apply_mammifere_duel_choice(
                state, choice == "POSER_DUEL_DEFI", int(r_m), int(p_m)
            )
            return

        if tag == "APPLY_OISEAU_PLUME_2":
            state._continuation.pop(0)
            apply_oiseau_plume_choice(state, choice)
            return

        if tag == "APPLY_DEF1":
            _, seat_raw = state._continuation.pop(0)
            seat_i = int(seat_raw)
            apply_step2_def1(state, seat_i, choice, check_legal=False)
            _maybe_prompt_mammifere_duel(state, seat_i, choice, "2.1")
            if (
                state.cfg.accessories_enabled
                and state.cfg.peuples[seat_i] == "O"
                and state.get_oiseau_perchoir_signal()[0] == PERCHOIR_NONE
            ):
                req_pl = DecisionRequest(
                    decideur=seat_i,
                    decision_type=DEC_OISEAU_PLUME_2,
                    options=_list_oiseau_plume_options(state),
                    context={"step": "2.1", "tour": state.tour},
                )
                push_continuation_sequence(
                    state, (("WAIT_DECISION", req_pl), ("APPLY_OISEAU_PLUME_2",))
                )
            return

        if tag == "APPLY_DEF2_INIT":
            _, seat_raw = state._continuation.pop(0)
            seat_i = int(seat_raw)
            apply_step2_def2(state, seat_i, choice, check_legal=False)
            if isinstance(choice, tuple) and len(choice) == 2 and choice[0] in (
                "POSER_DEFINITIF",
                "POSER_REFLEXION",
            ):
                _maybe_prompt_mammifere_duel(state, seat_i, choice[1], "2.2")
            return

        if tag == "STEP2_REV_QUEUE":
            _, seats_tuple, cursor = top
            seat_i = int(seats_tuple[cursor])
            moved = apply_step2_def2(state, seat_i, choice, check_legal=False)
            if moved:
                p_idx, _ = state.get_step2_pass_state()
                state.set_step2_pass_state(p_idx, True)
            state._continuation[0] = ("STEP2_REV_QUEUE", seats_tuple, cursor + 1)
            if isinstance(choice, tuple) and len(choice) == 2 and choice[0] in (
                "DEPLACER_REFLEXION",
                "DEPLACER_DEFINITIF",
            ):
                _maybe_prompt_mammifere_duel(state, seat_i, choice[1], "2.2_rev")
            return

        if tag == "APPLY_CONSTRUCT_ORDER":
            state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_constr_3_1 += 1
            push_continuation_sequence(state, (("CONSTRUCT_SLOT", int(choice)),))
            return

        if tag == "APPLY_GARDIEN_CASE_3_1":
            _, slot_idx, g_num = state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.on_gardien_case_chosen(int(choice))
            _, nb = state.get_lisiere_tile_state(int(slot_idx))
            state.set_gardien_at_case(int(choice), int(g_num), 1)
            state.set_lisiere_tile_state(int(slot_idx), LISIERE_CONSTRUCTED, nb)
            _record_phys_ops(state, 1)
            return

        if tag == "APPLY_LIBERATION_3_1":
            _, slot_idx = state._continuation.pop(0)
            _apply_builder_liberation(state, int(slot_idx), choice)
            return

        if tag == "APPLY_NID_PLACE_3_1":
            _, slot_idx, m_num = state._continuation.pop(0)
            rn, pn = choice
            _, nb = state.get_lisiere_tile_state(int(slot_idx))
            state.set_parcel_nid(int(rn), int(pn), int(m_num), False)
            state.set_lisiere_tile_state(int(slot_idx), LISIERE_CONSTRUCTED, nb)
            _record_phys_ops(state, 1)
            return

        if tag == "APPLY_SABOTAGE_CIBLE_3_2":
            state._continuation.pop(0)
            r_s, mt_s = choice
            _apply_sabotage_target_3_2(state, int(r_s), int(mt_s))
            return

        if tag == "APPLY_REPTILE_CROC_3_2":
            state._continuation.pop(0)
            r_c, p_c = choice
            prim_creation_entite(state, "CROC", ray=int(r_c), p=int(p_c))
            return

        if tag == "APPLY_CHOIX_CIBLE_REVE_3_2":
            _, r_idx, r_num, entries_tup, extra_tup = state._continuation.pop(0)
            chosen_seats = tuple(int(s) for s in choice)
            _resolve_defended_reve_3_2(
                state, int(r_idx), int(r_num), entries_tup, chosen_seats, extra_tup
            )
            return

        if tag == "APPLY_NID_4_2":
            state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_nid_4_2 += 1
            _resolve_nid_block(state, int(choice))
            return

        if tag == "APPLY_DEPLOIEMENT_NID_4_2":
            _, m_num_raw, rem_raw = state._continuation.pop(0)
            m_num = int(m_num_raw)
            rem = int(rem_raw)
            dst_kind = str(choice[0])
            if trk is not None and len(req.options) >= 2:
                trk.on_migration_decision(dst_kind)
            _apply_nid_deploy_choice_4_2(state, choice)
            if rem > 1:
                push_continuation_sequence(state, (("NID_DEPLOY_INSECT_4_2", m_num, rem - 1),))
            return

        if tag == "APPLY_PIEGE_FURTIVITE_4_1":
            _, ray_i, rive_i, cell_key_i = state._continuation.pop(0)
            _execute_furtivite_4_1_action(
                state,
                int(ray_i),
                int(choice),
                int(rive_i),
                "PIEGE",
                int(cell_key_i),
            )
            return

        if tag == "APPLY_TACTIQUE_5_1":
            _, t_code = state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_att_5_1 += 1
            rm, mt = choice
            _resolve_tactique_5_1_machine(state, int(rm), int(mt), int(t_code))
            return

        if tag == "APPLY_RATISSAGE_5_2":
            state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_rat_5_2 += 1
            rm, mt = choice
            resolve_single_machine_attack(
                state, int(rm), int(mt), RATISSAGE_TACTIQUE_SPEC, is_ratissage=True
            )
            return

        if tag == "APPLY_BOUCLIER_5_3":
            _, c_num, bw, bl, bs, f2 = state._continuation.pop(0)
            c_int = int(c_num)
            bs_i = int(bs)
            if choice == "UTILISER_BOUCLIER":
                col_ins = state.get_colonie_at_case(c_int)
                if col_ins >= 1:
                    state.set_colonie_at_case(c_int, col_ins - 1)
                    _record_phys_ops(state, 1)
                    bs_i += 1
            else:
                prim_partage_info_etat_gardien(
                    state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=c_int
                )
            _resolve_gardien_bets_5_3_from(
                state, c_int + 1, int(bw), int(bl), bs_i, int(f2)
            )
            return

        if tag == "APPLY_ENRACINEMENT_6_1":
            _, seat_r = state._continuation.pop(0)
            if choice != "PASSER":
                _apply_voluntary_rooting_6_1(state, int(seat_r), int(choice))
            return

        raise RuntimeError(f"Tag de continuation inconnu : {tag}")
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)
