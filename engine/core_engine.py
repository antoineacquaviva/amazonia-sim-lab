"""Machine à états déterministe suspendable des 6 étapes (Modes 1..4, 128 châssis v5.3)."""

from __future__ import annotations

from typing import Any

from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    HOOK_1_3_LECTURE_DE,
    HOOK_2_1_DEBUT,
    HOOK_2_1_PORTEE_DEF1,
    HOOK_3_1_CONSTRUCTION,
    HOOK_3_2_APRES_REVELATION,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_4_1_FURTIVITE,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_3_COLONIE_FIN,
    HOOK_4_3_MIGRATION_DESTS,
    HOOK_5_3_PRE_RETRAIT,
    HOOK_5_APRES_PARADE_PIEGE,
    HOOK_5_CIBLAGE_MACHINE,
    HOOK_5_DEBUT,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_FIN_ATTAQUE_MACHINE,
    HOOK_5_LAW_QUERY,
    HOOK_5_ORDRE_RAYON,
    HOOK_5_PARADE_CLASSIQUE,
    HOOK_5_PARADE_HARPIE,
    HOOK_5_PARADE_JAGUAR,
    HOOK_5_SEUIL_PARADE,
    HOOK_5_TERRASSEMENT,
    HOOK_6_1_BUG,
    HOOK_EFFECT_RESUME,
    HOOK_REPOUSSE_FINALE,
    DecisionRequest,
    GameOver,
    _get_active_telemetry,
    _record_phys_ops,
    _set_active_telemetry,
    apply_machine_nid_contact,
    dispatch_hook,
    get_tile_registration,
    has_pending_decision,
    prim_creation_entite,
    prim_deplacement,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    push_effect_decision,
    register_tile,
)
from engine.rng import SRC_DICE, roll_d6
from engine.state import (
    CARD_NONE,
    CARD_SABOTAGE,
    DOUBLE_FACE_UPGRADE_GARDIENS,
    FACE_DEFINITIF,
    FACE_REFLEXION,
    FAMILLE_GARDIEN,
    FAMILLE_REVE,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
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
    PEUPLE_TO_ID,
    PFLAG_AUTO_PARADE_ONCE,
    PFLAG_MATAMATA_MARK,
    PFLAG_SANCTUAIRE_SOUCHE,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    PIEGE_DECLENCHE,
    RATISSAGE_TACTIQUE_SPEC,
    STEP_1_1_RATISSAGE,
    STEP_1_2_DEAL,
    STEP_1_3_DICE,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_4_3_MIGRATION,
    STEP_5_1_TACTIQUES,
    STEP_5_2_RATISSAGE,
    STEP_5_3_END_CHECK,
    STEP_6_1_APPRENTISSAGE,
    STEP_6_2_EVOLUTION,
    STEP_6_3_END_TURN,
    STEP_GAME_OVER,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    GameState,
    TactiqueSpec,
    code_to_tile_id,
    is_reve_code,
    is_tactique_charge,
    is_tactique_code,
    machine_card_code,
)

__all__ = (
    "DEC_CHOIX_CASE_GARDIEN",
    "DEC_COLONIE_A_OPEN",
    "DEC_LIBERATION_BATISSEUR_3_1",
    "DEC_MIGRATION_INSECTE_4_3",
    "DEC_ORDRE_ATTAQUE_5_1",
    "DEC_ORDRE_CONSTRUCTION_3_1",
    "DEC_ORDRE_NID_4_2",
    "DEC_ORDRE_RATISSAGE_5_2",
    "DEC_PLACEMENT_NID_3_1",
    "DEC_POSE_DEFENSEUR_1",
    "DEC_POSE_DEFENSEUR_2",
    "DEC_POSE_PIEGE_FURTIVITE_4_1",
    "DEC_RETRAIT_APPRENTISSAGE_6_1",
    "DEC_REVISION_DEFENSEUR_2",
    "advance_step2_to_2_2",
    "apply_choice",
    "apply_repousse_finale",
    "apply_step2_def1",
    "apply_step2_def2",
    "clear_step2_pending_wait",
    "compute_parade_seuil",
    "ensure_builtin_migration_registered",
    "finish_step2_to_3_1",
    "insert_reve_on_track",
    "is_machine_active_this_turn",
    "list_legal_targets",
    "lock_all_def2_in_place",
    "rebind_step_3_2_hand",
    "resolve_single_machine_attack",
    "step_until_decision",
    "sweep_gardiens",
)

# Types canoniques de DecisionRequest
DEC_POSE_DEFENSEUR_1: str = "POSE_DEFENSEUR_1"
DEC_POSE_DEFENSEUR_2: str = "POSE_DEFENSEUR_2"
DEC_REVISION_DEFENSEUR_2: str = "REVISION_DEFENSEUR_2"
DEC_ORDRE_CONSTRUCTION_3_1: str = "ORDRE_CONSTRUCTION_3_1"
DEC_CHOIX_CASE_GARDIEN: str = "CHOIX_CASE_GARDIEN"
DEC_POSE_PIEGE_FURTIVITE_4_1: str = "POSE_PIEGE_FURTIVITE_4_1"
DEC_LIBERATION_BATISSEUR_3_1: str = "LIBERATION_BATISSEUR_3_1"
DEC_PLACEMENT_NID_3_1: str = "PLACEMENT_NID_3_1"
DEC_ORDRE_NID_4_2: str = "ORDRE_NID_4_2"
DEC_MIGRATION_INSECTE_4_3: str = "MIGRATION_INSECTE_4_3"
DEC_COLONIE_A_OPEN: str = "COLONIE_A_OPEN"
DEC_ORDRE_ATTAQUE_5_1: str = "ORDRE_ATTAQUE_TACTIQUE_5_1"
DEC_ORDRE_RATISSAGE_5_2: str = "ORDRE_RATISSAGE_5_2"
DEC_RETRAIT_APPRENTISSAGE_6_1: str = "RETRAIT_APPRENTISSAGE_6_1"


def _transition_step(state: GameState, new_step: int) -> None:
    prev_step = state.step
    if prev_step != new_step:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_step_transition(state, prev_step, new_step)
        state.step = new_step


# ---------------------------------------------------------------------------
# Profils standards Migration (Bug B, Colonie A) sur le bus de hooks (Mode 2+)
# ---------------------------------------------------------------------------


def _bug_a_handler(state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """SLOT_BUG_CERVEAU.A : obsolète (Apprentissage supprimé en v5.4.2) — no-op."""
    _ = state


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


def _bug_b_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> Any:
    """SLOT_BUG_CERVEAU.B (défaut v5.4.2) : en 3.2, défausse 1 Bug du rang M pour décaler M de ±1."""
    if hook == HOOK_3_2_REVELATION:
        _bug_b_step_queue(state, 0)
        return None
    if hook == HOOK_EFFECT_RESUME:
        choice = str(ctx["choice"])
        seat, case_num = ctx["payload"]
        s_int, c_int = int(seat), int(case_num)
        trk_b = _get_active_telemetry()
        if trk_b is not None:
            trk_b.on_bug_3_2_decision(choice)
        if choice in ("M_MOINS_1", "M_PLUS_1"):
            bugs = state.get_bugs_at_case(c_int)
            if bugs >= 1:
                state.set_bugs_at_case(c_int, bugs - 1)
                _record_phys_ops(state, 1)
                delta = -1 if choice == "M_MOINS_1" else 1
                prim_permutation_piste(
                    state, "SHIFT_LECTURE_M", seat=s_int, delta_m=delta, rebind_tactique=False
                )
                # Partition stricte 3.2 : cette carte Machine consomme son déclencheur sur 6. Insecte
                state.mark_seat_deviated_by_bug_this_turn(s_int)
                state.light_trigger(6)
                if trk_b is not None:
                    trk_b.on_trigger_lit(6)
                    trk_b.on_defense_bug_deviation(1)
                sweep_gardiens(state)
        _bug_b_step_queue(state, s_int + 1)
    return None


def _colonie_a_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> list[int]:
    """SLOT_COLONISATION_GARDIENS.A : signale les cases 1..6 éligibles à l'ouverture."""
    start_case = int(ctx.get("start_case", 1))
    eligible: list[int] = []
    for c in range(start_case, TRACK_LEN + 1):
        if state.get_colonie_at_case(c) >= 1:
            g_num, _ = state.get_gardien_at_case(c)
            if g_num > 0 and state.count_gardien_pari_defenders_at_case(c) >= 1:
                eligible.append(c)
    return eligible


def _colonie_b_handler(_state: GameState, _hook: str, _ctx: dict[str, Any]) -> list[int]:
    """SLOT_COLONISATION_GARDIENS.B (Bouclier de lisière) : résolu en 5.3, no-op en 4.3."""
    return []


def ensure_builtin_migration_registered() -> None:
    """Garantit l'enregistrement de Bug A/B et Colonie A/B (Bouclier de lisière) sur le bus."""
    if get_tile_registration("SLOT_BUG_CERVEAU", "A") is None:
        register_tile("SLOT_BUG_CERVEAU", "A", hooks=(HOOK_6_1_BUG,))(_bug_a_handler)
    if get_tile_registration("SLOT_BUG_CERVEAU", "B") is None:
        register_tile(
            "SLOT_BUG_CERVEAU", "B", hooks=(HOOK_3_2_REVELATION, HOOK_EFFECT_RESUME)
        )(_bug_b_handler)
    if get_tile_registration("SLOT_COLONISATION_GARDIENS", "A") is None:
        register_tile("SLOT_COLONISATION_GARDIENS", "A", hooks=(HOOK_4_3_COLONIE_FIN,))(
            _colonie_a_handler
        )
    if get_tile_registration("SLOT_COLONISATION_GARDIENS", "B") is None:
        register_tile("SLOT_COLONISATION_GARDIENS", "B", hooks=(HOOK_4_3_COLONIE_FIN,))(
            _colonie_b_handler
        )


ensure_builtin_migration_registered()
__import__("engine.effects")


# ---------------------------------------------------------------------------
# Balayage à plat des Gardiens (1 -> 6) & Résonance 4 (suspendable si effet à choix)
# ---------------------------------------------------------------------------


def _sweep_gardiens_from(
    state: GameState,
    start_case: int,
    opened_in_pass: bool,
    repasses_count: int,
    in_combat: bool,
    opened_total: int,
    opened_in_later_pass: int = 0,
) -> int:
    while True:
        for case_num in range(start_case, TRACK_LEN + 1):
            if state.is_trigger_lit(case_num):
                g_num, _ = state.get_gardien_at_case(case_num)
                if g_num > 0 and state.count_gardien_pari_defenders_at_case(case_num) >= 1:
                    state.clear_trigger(case_num)
                    opened_total += 1
                    if repasses_count >= 1:
                        opened_in_later_pass += 1
                    opened_in_pass = True
                    resume_frame = (
                        "RESUME_SWEEP_GARDIENS",
                        case_num + 1,
                        1,
                        repasses_count,
                        1 if in_combat else 0,
                        opened_total,
                        opened_in_later_pass,
                    )
                    state._continuation.insert(0, resume_frame)
                    prim_partage_info_etat_gardien(
                        state, "MARK_GARDIEN_OPENED", case_1_6=case_num
                    )
                    if state._continuation and state._continuation[0] == resume_frame:
                        state._continuation.pop(0)
                    else:
                        return opened_total
        if not opened_in_pass:
            break
        repasses_count += 1
        start_case = 1
        opened_in_pass = False

    state.triggers_lit = 0
    trk = _get_active_telemetry()
    if trk is not None:
        trk.on_gardien_sweep(
            state,
            repasses=repasses_count,
            opened=opened_total,
            in_combat=in_combat,
            opened_in_later_pass=opened_in_later_pass,
        )
    return opened_total


def sweep_gardiens(state: GameState, *, telemetry: Any | None = None) -> int:
    """Balayage croissant 1..6 répété tant qu'une case allumée porte un Gardien disponible.

    Retourne le nombre de Gardiens ouverts durant cette fenêtre (ou déjà ouverts avant suspension).
    """
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        if state.cfg.mode == 1:
            state.triggers_lit = 0
            return 0
        if state.triggers_lit == 0:
            return 0
        in_combat = state.step in (STEP_5_1_TACTIQUES, STEP_5_2_RATISSAGE)
        return _sweep_gardiens_from(state, 1, False, 0, in_combat, 0)
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
    if not use_global:
        rays, _, lis_slots = _DEF1_LOCAL_RANGES[(n, seat)]
    else:
        rays = all_rays
        lis_slots = _LIS_SLOTS_BY_N[n]

    targets: list[tuple[Any, ...]] = []

    # 1. Parcelles Forêt non rasées (rayon local en 2.1, tous les rayons en 2.2)
    for r in rays:
        f_row = _FORET_TARGETS[r]
        for p in range(1, p_max + 1):
            if not state.is_route_forestiere(r, p):
                targets.append(f_row[p])

    # 2. Tuiles de Synergie en lisière (interdites en Mode 1, non construites et < 2 bâtisseurs)
    if state.cfg.mode >= 2:
        for slot_idx in lis_slots:
            st, nb = state.get_lisiere_tile_state(slot_idx)
            cand_l = _LIS_TARGETS[slot_idx]
            if own_spot == cand_l:
                nb = max(0, nb - 1)
            if st == LISIERE_UNCONSTRUCTED and nb < 2:
                targets.append(cand_l)

    # Repli anti-blocage si le territoire local (Forêt + Lisière) d'un siège en 2.1 est 100 % rasé/plein :
    # étend la portée Forêt + Lisière à toute la table sans jamais exposer GARDIEN_PARI au 1er Défenseur.
    if not targets and not use_global:
        for r in all_rays:
            f_row = _FORET_TARGETS[r]
            for p in range(1, p_max + 1):
                if not state.is_route_forestiere(r, p):
                    targets.append(f_row[p])
        if state.cfg.mode >= 2:
            for slot_idx in _LIS_SLOTS_BY_N[n]:
                st, nb = state.get_lisiere_tile_state(slot_idx)
                if st == LISIERE_UNCONSTRUCTED and nb < 2:
                    targets.append(_LIS_TARGETS[slot_idx])

    # 3. Furtivité v6.1 (« Chaud vs Calme » au pied de chaque rayon non intégralement rasé, libre en 2.1 et 2.2)
    for r_idx in all_rays:
        if not state.is_ray_furtivite_open(r_idx):
            continue
        pair = _FURT_TARGETS[r_idx]
        for rv in (FURT_RIVE_PIEGE, FURT_RIVE_SABOTAGE):
            d_rv = state.get_furtivite_nb_def_rive(r_idx, 1, rv)
            if own_spot == pair[rv]:
                d_rv -= 1
            if d_rv < 2:
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
            if cnt_case >= state.cfg.gardien_bet_cap_for_case(c_num):
                continue
            targets.append(cand_pari)

    # 5. Activation de Rêve sur la Réglette (ouverte en 2.1 ET en 2.2 en v6.1, Mode >= 2)
    if state.cfg.mode >= 2:
        for c_num in range(1, TRACK_LEN + 1):
            if is_reve_code(state.get_tactique_at_rank(c_num - 1)):
                targets.append(_REVE_ACTIVATION_TARGETS[c_num])

    if extra_targets and not use_global:
        for ext_t in extra_targets:
            if ext_t not in targets:
                targets.append(ext_t)

    return tuple(targets)


def list_legal_targets(
    state: GameState,
    seat: int,
    *,
    is_first_defender: bool,
    exclude_own_def2: bool = False,
) -> tuple[tuple[Any, ...], ...]:
    """Énumère toutes les poses légales (anti-blocage v6.1) pour un Défenseur de `seat`."""
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
        if len(target) == 3:
            _, ray_idx, rive = target
            state.place_defender_furtivite(seat, def_idx, int(ray_idx), int(rive), face)
        else:
            _, l_idx, p, rive = target
            state.enter_furtivite(seat, def_idx, int(l_idx), int(p), int(rive), face)
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


def clear_step2_pending_wait(state: GameState) -> None:
    """Purge une attente séquentielle 2.1/2.2 pour piloter l'Étape 2 en Ticks simultanés 1..3."""
    if not state._continuation or state._continuation[0][0] != "WAIT_DECISION":
        return
    req = state._continuation[0][1]
    if req.decision_type in (
        DEC_POSE_DEFENSEUR_1,
        DEC_POSE_DEFENSEUR_2,
        DEC_REVISION_DEFENSEUR_2,
    ):
        state._continuation.pop(0)
        if state._continuation and state._continuation[0][0] in (
            "APPLY_DEF1",
            "APPLY_DEF2_INIT",
            "STEP2_REV_QUEUE",
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
        _apply_defender_target(state, seat, 0, target, FACE_DEFINITIF)
        if telemetry is not None:
            telemetry.record_player_decision(state, seat)
        trk = _get_active_telemetry()
        if trk is not None:
            t_kind = str(target[0])
            trk.on_step2_def1_placed(t_kind)
            if t_kind in ("FORET", "LISIERE"):
                rays_loc, _, slots_loc = _DEF1_LOCAL_RANGES[(state.cfg.n_players, seat)]
                out_of_local = (
                    (t_kind == "FORET" and int(target[1]) not in rays_loc)
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
    et enregistrement télémétrique d'une tentative d'Éveil si les N 2es Défenseurs sont sur la Piste des Gardiens.
    """
    flipped = 0
    for s in range(state.cfg.n_players):
        if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s):
            state.flip_defender2_to_definitif_in_place(s)
            flipped += 1
    if flipped > 0:
        _record_phys_ops(state, flipped)

    if not state.step2_locked:
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_step2_locked_summary(state)
            if state.is_eveil_attempt_eligible():
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


def _move_all_builders_to_nid_parcel(state: GameState, slot_idx: int, ray: int, p: int) -> None:
    _, nb = state.get_lisiere_tile_state(slot_idx)
    tracked = _tracked_builders_on_slot(state, slot_idx)
    for s, d in tracked:
        state.place_defender_foret(s, d, ray, p, FACE_DEFINITIF)
    untracked = max(0, nb - len(tracked))
    if untracked > 0:
        state.set_parcel_defenseurs(ray, p, state.get_parcel_defenseurs(ray, p) + untracked)
    state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, 0)
    _record_phys_ops(state, 1 + max(nb, len(tracked)))


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
# Étape 4.1 & Étape 5 : Attaques d'un seul tenant, Parades & Routes
# ---------------------------------------------------------------------------


def is_machine_active_this_turn(state: GameState, ray: int, m_type: int) -> bool:
    """Vrai si la machine est en Ratissage ou activée par une carte non annulée en 3.2."""
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
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
    if state.cfg.synergie_binome_machines == "MUTUALISATION_PUISSANCE_MEME_PARCELLE":
        pos_self, st_self, _ = state.get_machine_pos_status(ray, m_type)
        other_type = MACHINE_BULLDOZER if m_type == MACHINE_ABATTEUSE else MACHINE_ABATTEUSE
        pos_other, st_other, _ = state.get_machine_pos_status(ray, other_type)
        if (
            st_self != MACHINE_STATUS_RETIRED
            and st_other != MACHINE_STATUS_RETIRED
            and pos_self > 0
            and pos_self == pos_other
        ):
            r_o = state.get_machine_effective_rouges(ray, other_type)
            _, b_o = state.get_machine_tokens(ray, other_type)
            rouges += r_o
            bleus += b_o
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

    v6.0 :
    - Mode CHARGE (hors Ratissage) : les jetons Puissance (rouges) déjà sur la machine sont ignorés.
    - Mode ASSAUT & Ratissage permanent : tous les jetons Puissance comptent (dont le +1 imprimé du Ratissage).
    """
    base = state.cfg.dotation_arbres[target_p - 1]
    offset = state.cfg.offset_seuil_parade
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
        + offset
        + tactique.mod_seuil
        + extra_mod
        + int(ctx["delta_seuil"])
    )
    return max(1, raw)


def _handle_route_creation(state: GameState, ray: int, razed_p: int) -> None:
    """Transforme (ray, razed_p) en Route Forestière (0/0) et applique le repli A09."""
    trk = _get_active_telemetry()
    if trk is not None:
        trk.ok_routes_created += 1
    ops = 0
    ins_here = state.get_parcel_insectes(ray, razed_p)
    m_num, _ = state.get_parcel_nid(ray, razed_p)
    if m_num > 0:
        state.clear_nid(m_num)
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

    # Repli automatique des machines présentes sur (ray, razed_p)
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
            apply_machine_nid_contact(state, ray, p_back)
        else:
            p_fwd = state.next_non_razed_towards_heart(ray, razed_p)
            if p_fwd is not None:
                state.set_machine_pos_status(ray, mt, p_fwd, st, pending_s)
                ops += 1
                if trk is not None:
                    trk.ok_repli_coeur_exception += 1
                    if p_fwd > razed_p + 1:
                        trk.ok_pont_routier_jumps += 1
                apply_machine_nid_contact(state, ray, p_fwd)
            else:
                r_tok, b_tok = state.get_machine_tokens(ray, mt)
                state.set_machine_pos_status(ray, mt, 0, MACHINE_STATUS_RETIRED, False)
                state.set_machine_tokens(ray, mt, 0, 0)
                ops += 1 + r_tok + b_tok
                if trk is not None:
                    trk.ok_retrait_definitif_machine += 1
    if ops > 0:
        _record_phys_ops(state, ops)


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
) -> None:
    trk = _get_active_telemetry()
    aborted_by_jaguar = False

    for t_idx in range(start_idx, len(targets)):
        c_type, target_p = targets[t_idx]
        if state.is_route_forestiere(ray, target_p):
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
            state.light_trigger(1)
            if trk is not None:
                trk.on_trigger_lit(1)
                trk.on_defense_parade_classique(1)
            parried_strikes += 1
            aborted_by_jaguar = True
            break

        # Maillon 2 : Piquée de la Harpie (Mode 3+ ou flag PFLAG_AUTO_PARADE_ONCE)
        if (
            state.has_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE)
            and state.get_parcel_defenseurs(ray, target_p) >= 2
        ):
            state.set_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE, False)
            state.light_trigger(1)
            if trk is not None:
                trk.on_trigger_lit(1)
                trk.on_defense_parade_classique(1)
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
            state.light_trigger(1)
            if trk is not None:
                trk.on_trigger_lit(1)
                trk.on_defense_parade_classique(1)
            parried_strikes += 1
            continue

        # Calcul de la Défense totale sur la parcelle à cet instant
        local_defs = state.get_parcel_defenseurs(ray, target_p)
        local_ins = state.get_parcel_insectes(ray, target_p)
        def_ctx: dict[str, Any] = {
            "ray": ray,
            "m_type": m_type,
            "target_p": target_p,
            "cible_type": c_type,
            "def_points": local_defs,
            "ins_points": local_ins,
            "remote_support": 0,
        }
        dispatch_hook(state, HOOK_5_DEFENSE_PARCELLE, def_ctx)
        def_non_ins = int(def_ctx["def_points"]) + int(def_ctx["remote_support"])
        total_def = def_non_ins + int(def_ctx["ins_points"])

        # Maillon 3 : Piège autonome v6.1 (SINGLE_STRIKE figé, sans Embuscade)
        # Pare exactement 1 frappe puis est défaussé aussitôt -> allume uniquement 2. Piégeage
        piege_st = state.get_parcel_piege(ray, target_p)
        if piege_st == PIEGE_ACTIF:
            _record_phys_ops(state, 1)
            if trk is not None:
                trk.ok_pieges_triggered += 1
            state.set_parcel_piege(ray, target_p, PIEGE_AUCUN)
            state.light_trigger(2)
            if trk is not None:
                trk.on_trigger_lit(2)
                trk.on_defense_piege(1)
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
            )
            if state.cfg.mode >= 3:
                state._continuation.insert(0, resume_f)
            dispatch_hook(
                state,
                HOOK_5_APRES_PARADE_PIEGE,
                {"ray": ray, "m_type": m_type, "target_p": target_p},
            )
            if state.cfg.mode >= 3:
                if state._continuation and state._continuation[0] == resume_f:
                    state._continuation.pop(0)
                else:
                    return
            continue

        # Maillon 4 : Parade classique (défausse immédiate des Insectes manquants, zéro dette)
        # Partition stricte : >= 1 Insecte défaussé -> 6. Insecte uniquement ; sinon -> 1. Parade uniquement.
        seuil = compute_parade_seuil(
            state,
            ray,
            m_type,
            target_p,
            tactique,
            cible_type=c_type,
            is_ratissage=effective_ratissage,
        )
        if total_def >= seuil:
            manque = max(0, seuil - def_non_ins)
            final_discard = 0
            if manque > 0:
                ins_to_discard = min(local_ins, manque)
                pc_ctx: dict[str, Any] = {
                    "ray": ray,
                    "target_p": target_p,
                    "local_defs": local_defs,
                    "manque": manque,
                    "ins_to_discard": ins_to_discard,
                }
                dispatch_hook(state, HOOK_5_PARADE_CLASSIQUE, pc_ctx)
                final_discard = max(0, min(local_ins, int(pc_ctx["ins_to_discard"])))
                if final_discard > 0:
                    state.set_parcel_insectes(ray, target_p, local_ins - final_discard)
                    _record_phys_ops(state, final_discard)
            if final_discard >= 1:
                state.light_trigger(6)
                if trk is not None:
                    trk.on_trigger_lit(6)
                    trk.on_defense_parade_avec_insectes(1)
            else:
                state.light_trigger(1)
                if trk is not None:
                    trk.on_trigger_lit(1)
                    trk.on_defense_parade_classique(1)
            parried_strikes += 1
            continue

        # Non parée : application des dégâts
        arbres_before = state.get_parcel_arbres(ray, target_p)
        souches_before = state.get_parcel_souches(ray, target_p)
        arbres_after = arbres_before
        souches_after = souches_before
        dmg_ops = 0

        if m_type == MACHINE_ABATTEUSE:
            if arbres_before > 0:
                # v6.1 : l'Abatteuse coupe TOUS les Arbres debout de la parcelle (en Souches)
                cut = arbres_before
                arbres_after = 0
                souches_after += cut
                dmg_ops += cut
            elif effective_ratissage and souches_before > 0 and trk is not None:
                # v6.1 : l'Abatteuse ne touche jamais aux Souches (micro-règle souche supprimée)
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
        "is_ratissage": effective_ratissage,
        "is_charge": is_charge_atk,
        "all_parried": all_parried,
        "damaged_parcels": damaged_parcels,
        "allow_advance": True,
        "allow_red_gain": True,
    }
    dispatch_hook(state, HOOK_5_FIN_ATTAQUE_MACHINE, fin_ctx)

    # 3. Avancée éventuelle (T3 / T6) si machine toujours en jeu et hors Ratissage
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    if (
        not aborted_by_jaguar
        and bool(fin_ctx["allow_advance"])
        and cur_st == MACHINE_STATUS_NORMAL
        and cur_pos > 0
        and tactique.avancee > 0
    ):
        for _ in range(tactique.avancee):
            cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
            if cur_st != MACHINE_STATUS_NORMAL or cur_pos == 0:
                break
            p_next = state.next_non_razed_towards_heart(ray, cur_pos)
            if p_next is not None:
                if trk is not None and p_next > cur_pos + 1:
                    trk.ok_pont_routier_jumps += 1
                prim_deplacement(
                    state,
                    "MACHINE",
                    src_ray=ray,
                    m_type=m_type,
                    dst_ray=ray,
                    dst_p=p_next,
                )

    # 4. Mode CHARGE (v6.1) : +1 jeton Puissance max par activation selon `charge_gain_mode` :
    #    - DEGAT_EFFECTIF : >= 1 parcelle réellement endommagée ;
    #    - FRAPPE_NON_PAREE : >= 1 frappe exécutée sur une parcelle réelle non-Route ni parée ni piégée
    #      (une attaque Devant hors-plateau depuis la dernière parcelle ne fait jamais gagner de jeton).
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    qualifies_charge_gain = (
        (damaged_parcels >= 1)
        if state.cfg.charge_gain_mode == "DEGAT_EFFECTIF"
        else (executed_strikes >= 1 and unparried_real_strikes >= 1)
    )
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

    # 5. Fin du bloc machine -> balayage à plat des Gardiens 1 -> 6
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
    """Résout une machine d'un seul tenant : cibles dynamiques -> frappes -> avancée -> Charge -> Gardiens."""
    prev_trk = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st == MACHINE_STATUS_RETIRED or pos == 0:
            state.set_machine_turn_stats(ray, m_type, 0, False, True)
            return

        effective_ratissage = is_ratissage or st == MACHINE_STATUS_RATISSAGE
        trk = _get_active_telemetry()
        if effective_ratissage and trk is not None:
            trk.ok_ratissage_activations += 1

        # 1. Lecture dynamique des cibles depuis la position réelle (en sautant toute Route)
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
        )
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)


# ---------------------------------------------------------------------------
# Étape 5.3 : Fin de partie (0 Repousse Finale de base en v6.0) & calcul GameOver
# ---------------------------------------------------------------------------


def apply_repousse_finale(state: GameState) -> GameOver:
    """Clôture la partie de manière strictement idempotente et calcule le score coopératif.

    v6.0 : 0 Souche ne repousse automatiquement dans le cœur (le score compte uniquement
    les Arbres debout, sauf effet de tuile explicite sur HOOK_REPOUSSE_FINALE en Mode 3/4).
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
                and state.total_gardien_pari_engaged() == state.cfg.n_players
                and state.total_gardien_pari_remaining() == 0
            ):
                trk.ok_tour8_blocked_eveil += 1
        arbres_before_repousse = state.total_arbres_plateau()
        if state.cfg.mode >= 3:
            for r in range(state.cfg.n_players):
                for p in range(1, state.cfg.p_max + 1):
                    if state.is_route_forestiere(r, p):
                        continue
                    souches = state.get_parcel_souches(r, p)
                    if souches >= 1:
                        rep_ctx: dict[str, Any] = {"ray": r, "p": p, "max_repousse": 0}
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
# Helpers internes pour Migration 4.3, Ratissage 1.1/6.3 et files d'attente
# ---------------------------------------------------------------------------


def _transition_eligible_machines_to_ratissage(state: GameState, *, remove_from_deck: bool) -> None:
    ops = 0
    for r in range(state.cfg.n_players):
        last_p = state.last_non_razed_parcel(r)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_NORMAL or pos == 0:
                continue
            if last_p is not None and pos == last_p:
                state.set_machine_pos_status(r, mt, pos, MACHINE_STATUS_RATISSAGE, False)
                ops += 1
                if remove_from_deck:
                    state.remove_machine_card_from_deck_if_present(machine_card_code(r, mt))
    if ops > 0:
        _record_phys_ops(state, ops)
        trk = _get_active_telemetry()
        if trk is not None:
            if remove_from_deck:
                trk.ok_ratissage_entries_1_1 += ops
            else:
                trk.ok_ratissage_entries_6_3 += ops


def _list_insect_1cran_moves(
    state: GameState, src: tuple[str, int, int]
) -> tuple[tuple[Any, ...], ...]:
    """Options de migration à 0 ou 1 cran pour un Insecte situé sur `src` (v6.1 : hors Furtivité)."""
    loc_type, idx_a, p = src
    opts: list[tuple[Any, ...]] = [("RESTER",)]

    if loc_type == "FORET":
        r = idx_a
        if state.is_route_forestiere(r, p) or state.get_parcel_insectes(r, p) == 0:
            return (("RESTER",),)

        p_fwd = state.next_non_razed_towards_heart(r, p)
        if p_fwd is not None:
            opts.append(("FORET", r, p_fwd))
        p_back = state.next_non_razed_towards_border(r, p)
        if p_back is not None:
            opts.append(("FORET", r, p_back))

        if state.cfg.mode >= 2 and p == state.last_non_razed_parcel(r):
            for c in range(1, TRACK_LEN + 1):
                opts.append(("BUG", c))
            for c in range(1, TRACK_LEN + 1):
                opts.append(("COLONIE", c))
    else:
        l_idx = idx_a
        if state.get_furtivite_insectes(l_idx, p) == 0:
            return (("RESTER",),)
        p_first = state.first_non_razed_from_border(l_idx)
        if p_first is not None:
            opts.append(("FORET", l_idx, p_first))

    if state.cfg.mode >= 3:
        dispatch_hook(state, HOOK_4_3_MIGRATION_DESTS, {"src": src, "opts": opts})

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

        ab_ok = ab_st == MACHINE_STATUS_RATISSAGE and ab_pos > 0 and not ab_att
        bu_ok = bu_st == MACHINE_STATUS_RATISSAGE and bu_pos > 0 and not bu_att
        if _is_ray_bulldozer_first(state, r) and bu_ok:
            eligible.append((r, MACHINE_BULLDOZER))
        elif ab_ok:
            eligible.append((r, MACHINE_ABATTEUSE))
        elif bu_ok:
            eligible.append((r, MACHINE_BULLDOZER))
    return eligible


# ---------------------------------------------------------------------------
# Étapes 3.2 et 4.1 suspendables (Mode 2/3/4) & rapides sans allocation
# ---------------------------------------------------------------------------


def _machine_threat_key_3_2(state: GameState, seat: int, card: int) -> tuple[int, int, int, int, int]:
    """Clé de priorité décroissante de menace pour l'annulation par un Rêve en 3.2."""
    ray = (card - 1) // 2
    m_type = (card - 1) % 2
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    active = 1 if (st != MACHINE_STATUS_RETIRED and pos > 0) else 0
    is_rat = 1 if st == MACHINE_STATUS_RATISSAGE else 0
    eff_red = state.get_machine_effective_rouges(ray, m_type) if active else 0
    return (active, is_rat, eff_red, pos, -seat)


def _bind_hands_and_resolve_reves_3_2(
    state: GameState,
) -> tuple[
    tuple[tuple[int, int, bool, str], ...],
    tuple[int, ...],
]:
    """Lie les mains révélées en 3.2, résout le blocage automatique des Rêves défendus et collecte les déclencheurs.

    Socle v6.1 :
    - Pas de choix AVANCER ni de déplacement des Rêves en 3.2 (CLEAR_RANK_ONLY).
    - Tout Rêve portant >= 1 Défenseur et visé par >= 1 machine annule 1 machine par Défenseur
      (en priorisant la plus menaçante) ; les machines restantes exécutent la Tactique imprimée dessous.
    - Partition stricte 3.2 (« 1 carte révélée = au plus 1 déclencheur ») :
      * 3. Sabotage : carte Sabotage révélée chez un joueur ;
      * 6. Insecte : sinon, dé dévié par un Bug en 3.2 (déjà allumé dans `_bug_b_handler`) ;
      * 5. Rêve (`REVE_TRIG=ACTIF` figé) : allumé uniquement lorsqu'un Rêve portant >= 1 Défenseur
        annule réellement >= 1 machine ET qu'au moins 1 carte présente sur ce rang n'a pas été déviée par un Bug.
    """
    n = state.cfg.n_players
    initial_track = [state.get_tactique_at_rank(i) for i in range(TRACK_LEN)]
    seats_by_rank: list[list[tuple[int, int, int, int, int]]] = [[] for _ in range(TRACK_LEN)]
    reveal_triggers: list[int] = []
    sabotages_revealed = 0
    for s in range(n):
        card, d1, d2, lec_m, _ = state.get_player_hand(s)
        if card == CARD_SABOTAGE:
            reveal_triggers.append(3)
            sabotages_revealed += 1
        elif 1 <= card <= 12 and 1 <= lec_m <= 6:
            seats_by_rank[lec_m - 1].append((s, card, d1, d2, lec_m))

    act_mode = state.cfg.reve_activation_mode
    trk = _get_active_telemetry()
    if trk is not None and sabotages_revealed > 0:
        trk.on_defense_sabotage_revele(sabotages_revealed)
    reve_open_items: list[tuple[int, int, bool, str]] = []

    for r_idx in range(TRACK_LEN):
        entries = seats_by_rank[r_idx]
        if not entries:
            continue
        case_1_6 = r_idx + 1
        code_m = initial_track[r_idx]
        if not is_reve_code(code_m):
            for s, card, d1, d2, lec_m in entries:
                state.set_player_hand(s, card, d1, d2, lec_m, case_1_6)
            continue

        # Un Rêve occupe la case case_1_6 par-dessus la Tactique imprimée T{case_1_6}
        n_def = state.count_reve_activation_defenders_at_case(case_1_6)
        min_needed = 2 if act_mode == "BINOME_ALL_RANK" else 1
        if n_def < min_needed:
            # Rêve inerte : toutes les machines exécutent la Tactique imprimée dessous, 0 déclencheur
            for s, card, d1, d2, lec_m in entries:
                state.set_player_hand(s, card, d1, d2, lec_m, case_1_6)
            if trk is not None:
                trk.on_machines_bypassed_inactive_reve(len(entries))
            continue

        r_num = code_m - TILE_R_BASE
        if trk is not None:
            trk.on_reve_choice("BLOQUER", dual_options=False)

        if act_mode == "1_DEF_1_MACHINE":
            if n_def >= len(entries):
                cancelled_seats = {e[0] for e in entries}
            else:
                ranked = sorted(
                    entries,
                    key=lambda e: _machine_threat_key_3_2(state, e[0], e[1]),
                    reverse=True,
                )
                cancelled_seats = {e[0] for e in ranked[:n_def]}
        elif act_mode == "1_DEF_ALL_RANK":
            cancelled_seats = {e[0] for e in entries} if n_def >= 1 else set()
        else:
            cancelled_seats = {e[0] for e in entries} if n_def >= 2 else set()

        for s, card, d1, d2, lec_m in entries:
            if s in cancelled_seats:
                state.set_player_hand(s, card, d1, d2, lec_m, 0)
            else:
                state.set_player_hand(s, card, d1, d2, lec_m, case_1_6)

        n_cancel = len(cancelled_seats)
        n_bypass = len(entries) - n_cancel
        if n_cancel > 0:
            if act_mode == "1_DEF_1_MACHINE":
                consumed_reves = state.consume_reve_activation_defenders(case_1_6, n_cancel)
            elif act_mode == "1_DEF_ALL_RANK":
                consumed_reves = state.consume_reve_activation_defenders(case_1_6, 1)
            else:
                consumed_reves = state.consume_reve_activation_defenders(case_1_6, 2)
            if consumed_reves > 0:
                _record_phys_ops(state, consumed_reves)

            if any(not state.was_seat_deviated_by_bug_this_turn(e[0]) for e in entries):
                reveal_triggers.append(5)

            if state.cfg.regle_ouverture_reve_multiple == "UNIQUE_PAR_TOUR":
                open_count = 0 if state.has_reve_opened_this_turn(r_num) else 1
            else:
                open_count = n_cancel
            if state.cfg.mode <= 2:
                if open_count >= 1:
                    state.mark_reve_opened_this_turn(r_num)
                    if trk is not None:
                        trk.on_reve_activated(open_count)
            else:
                for _ in range(open_count):
                    reve_open_items.append((code_m, r_num, False, "BLOQUER"))

        if trk is not None:
            if n_cancel > 0:
                trk.on_machines_cancelled_by_reve(n_cancel)
            if n_bypass > 0:
                trk.on_machines_bypassed_inactive_reve(n_bypass)

    return tuple(reve_open_items), tuple(reveal_triggers)


def _run_step_3_2(state: GameState) -> None:
    prim_partage_info_etat_gardien(state, "OPEN_PARAVENTS")
    has_bug_b_work = (
        state.cfg.mode == 2
        and state.cfg.profile_for_slot("SLOT_BUG_CERVEAU") == "B"
        and any(state.get_bugs_at_case(c) > 0 for c in range(1, TRACK_LEN + 1))
    )
    if state.cfg.mode <= 2 and not has_bug_b_work:
        _, reveal_triggers = _bind_hands_and_resolve_reves_3_2(state)
        trk = _get_active_telemetry()
        for trig_c in reveal_triggers:
            state.light_trigger(trig_c)
            if trk is not None:
                trk.on_trigger_lit(trig_c)
            sweep_gardiens(state)
        _transition_step(state, STEP_4_1_FURTIVITE)
        return

    state._continuation.insert(0, ("STEP_3_2_BIND",))
    dispatch_hook(state, HOOK_3_2_REVELATION, {})


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
        # 3. Sabotage ne s'allume pas à l'acquisition en 4.1 (uniquement à la révélation en 3.2)
        prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=False)
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
    """Résout la Furtivité v6.1 (« Chaud vs Calme » par rayon `r` : Rive Piège `m(r)==2`, Rive Sabotage `m(r)==0`)."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    total_rives = 2 * n
    trk = _get_active_telemetry()

    for slot_idx in range(start_slot_idx, total_rives):
        off = slot_idx // 2
        rive = slot_idx & 1
        ray = (state.coordonnateur + off) % n
        cell_key = ray
        nb_def = state.get_furtivite_nb_def_rive(ray, 1, rive)
        if nb_def != 2:
            if nb_def == 1 and trk is not None:
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
                    state._continuation.insert(0, resume_frame)
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
            state._continuation.insert(0, ("RESUME_STEP_4_1", slot_idx + 1))
            state._continuation.insert(0, ("APPLY_PIEGE_FURTIVITE_4_1", ray, rive, cell_key))
            state._continuation.insert(0, ("WAIT_DECISION", req))
            return

        # Rive Sabotage (rive == FURT_RIVE_SABOTAGE) : pari gagné ssi m(ray) == 0
        if m_r != 0:
            if trk is not None:
                trk.on_furtivite_failed_binome(1, rive="SABOTAGE")
            continue

        resume_frame = ("RESUME_STEP_4_1", slot_idx + 1)
        if state.cfg.mode >= 3:
            state._continuation.insert(0, resume_frame)
        _execute_furtivite_4_1_action(state, ray, 1, rive, "SABOTAGE", cell_key)
        if state.cfg.mode >= 3:
            if state._continuation and state._continuation[0] == resume_frame:
                state._continuation.pop(0)
            else:
                return

    _transition_step(state, STEP_4_2_NIDS)


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

    if tag == "RESUME_HOOK_QUEUE":
        _, hook_name, rem_slots, frozen_ctx = state._continuation.pop(0)
        for idx, slot_id in enumerate(rem_slots):
            rest = rem_slots[idx + 1 :]
            r_frame: tuple[Any, ...] | None = None
            if rest:
                r_frame = ("RESUME_HOOK_QUEUE", hook_name, rest, frozen_ctx)
                state._continuation.insert(0, r_frame)
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
            opened_in_pass_i,
            repasses_cnt,
            in_combat_i,
            opened_tot,
            opened_later,
        ) = state._continuation.pop(0)
        _sweep_gardiens_from(
            state,
            int(next_case),
            bool(opened_in_pass_i),
            int(repasses_cnt),
            bool(in_combat_i),
            int(opened_tot),
            int(opened_later),
        )
        return None

    if tag == "SWEEP_GARDIENS_NOW":
        state._continuation.pop(0)
        sweep_gardiens(state)
        return None

    if tag == "STEP_1_3_HOOK_QUEUE":
        _, start_seat = state._continuation.pop(0)
        s_idx = int(start_seat)
        while s_idx < n:
            card, _, _, _, _ = state.get_player_hand(s_idx)
            if 1 <= card <= 12:
                next_f = ("STEP_1_3_HOOK_QUEUE", s_idx + 1)
                state._continuation.insert(0, next_f)
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

    if tag == "STEP_3_2_BIND":
        state._continuation.pop(0)
        reve_open_items, reveal_triggers = _bind_hands_and_resolve_reves_3_2(state)
        state._continuation.insert(0, ("STEP_3_2_POST",))
        if reve_open_items:
            state._continuation.insert(0, ("STEP_3_2_REVE_QUEUE", reve_open_items, 0))
        if reveal_triggers:
            state._continuation.insert(0, ("STEP_3_2_REVEAL_TRIGGERS", reveal_triggers, 0))
        return None

    if tag == "STEP_3_2_REVEAL_TRIGGERS":
        _, reveal_triggers, cur_idx = state._continuation.pop(0)
        if cur_idx < len(reveal_triggers):
            trig_c = int(reveal_triggers[cur_idx])
            if cur_idx + 1 < len(reveal_triggers):
                state._continuation.insert(
                    0, ("STEP_3_2_REVEAL_TRIGGERS", reveal_triggers, cur_idx + 1)
                )
            state.light_trigger(trig_c)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(trig_c)
            sweep_gardiens(state)
        return None

    if tag == "STEP_3_2_REVE_QUEUE":
        _, reve_q, cur_idx = state._continuation.pop(0)
        if cur_idx < len(reve_q):
            reve_code, r_num, should_advance, reve_choice = reve_q[cur_idx]
            if cur_idx + 1 < len(reve_q):
                state._continuation.insert(0, ("STEP_3_2_REVE_QUEUE", reve_q, cur_idx + 1))
            if (
                state.cfg.regle_ouverture_reve_multiple == "UNIQUE_PAR_TOUR"
                and state.has_reve_opened_this_turn(r_num)
            ):
                if should_advance:
                    state._continuation.insert(0, ("STEP_3_2_FINISH_REVE", int(reve_code), 1))
                return None
            state.mark_reve_opened_this_turn(r_num)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_reve_activated(1)
            state._continuation.insert(
                0, ("STEP_3_2_FINISH_REVE", int(reve_code), 1 if should_advance else 0)
            )
            dispatch_hook(
                state,
                HOOK_3_2_OUVERTURE_REVE,
                {"slot_id": f"R{r_num}", "r_num": int(r_num), "choice": str(reve_choice)},
            )
        return None

    if tag == "STEP_3_2_FINISH_REVE":
        _, reve_code, should_advance = state._continuation.pop(0)
        if should_advance:
            cur_pos_r = state.find_tactique_rank(int(reve_code))
            if cur_pos_r is not None and cur_pos_r > 0:
                prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cur_pos_r)
        sweep_gardiens(state)
        return None

    if tag == "STEP_3_2_POST":
        state._continuation.pop(0)
        state._continuation.insert(0, ("STEP_3_2_END",))
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
            cur_spot = _current_def_canonical_spot(state, seat, 1)
            legal_t = list_legal_targets(
                state, seat, is_first_defender=False, exclude_own_def2=True
            )
            rev_opts: list[tuple[str, Any]] = [
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
                context={"tour": state.tour, "pass": pass_idx},
            )
            state._continuation.insert(0, ("WAIT_DECISION", req))
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

    if tag == "CONSTRUCT_SLOT_PAID":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        return _finish_single_construction_after_cost(state, slot_idx)

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
                state._continuation.insert(
                    0, ("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, 0)
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
            state._continuation.insert(0, ("APPLY_LIBERATION_3_1", slot_idx))
            state._continuation.insert(0, ("WAIT_DECISION", req))
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
                state._continuation.insert(
                    0, ("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1)
                )
            return None

        owner_opts = tuple((b_seat, b_def, r, p_first) for r, p_first in valid_rays)
        if len(owner_opts) == 1:
            _apply_builder_liberation(state, slot_idx, owner_opts[0])
            if cursor + 1 < len(builders_q):
                state._continuation.insert(
                    0, ("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1)
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
        if cursor + 1 < len(builders_q):
            state._continuation.insert(
                0, ("LIBERATION_ALL_QUEUE_3_1", slot_idx, builders_q, cursor + 1)
            )
        state._continuation.insert(0, ("APPLY_LIBERATION_3_1", slot_idx))
        state._continuation.insert(0, ("WAIT_DECISION", req_owner))
        return req_owner

    if tag == "MIGRATION_QUEUE_4_3":
        queue_tuple: tuple[tuple[str, int, int], ...] = top[1]
        cursor = int(top[2])
        if cursor < len(queue_tuple):
            src = queue_tuple[cursor]
            moves = _list_insect_1cran_moves(state, src)
            if len(moves) <= 1:
                state._continuation[0] = ("MIGRATION_QUEUE_4_3", queue_tuple, cursor + 1)
                return None
            gov = _governor_for_peuple(state, "I")
            req = DecisionRequest(
                decideur=gov,
                decision_type=DEC_MIGRATION_INSECTE_4_3,
                options=moves,
                context={"source": src, "index": cursor},
            )
            state._continuation.insert(0, ("APPLY_MIGRATION_4_3", src))
            state._continuation.insert(0, ("WAIT_DECISION", req))
            return req

        state._continuation.pop(0)
        if state.cfg.mode >= 2:
            state._continuation.append(("COLONIE_SCAN_4_3", 1))
        else:
            _transition_step(state, STEP_5_1_TACTIQUES)
        return None

    if tag == "COLONIE_SCAN_4_3":
        next_case = int(top[1])
        state._continuation.pop(0)
        hook_res = dispatch_hook(state, HOOK_4_3_COLONIE_FIN, {"start_case": next_case})
        eligible_cases: list[int] = hook_res[0] if hook_res else []
        if not eligible_cases:
            _transition_step(state, STEP_5_1_TACTIQUES)
            return None
        first_item = eligible_cases[0]
        if isinstance(first_item, tuple) and first_item[0] == "AUTO":
            c_num = int(first_item[1])
            state._continuation.insert(0, ("COLONIE_SCAN_4_3", c_num + 1))
            sweep_frame = ("SWEEP_GARDIENS_NOW",)
            state._continuation.insert(0, sweep_frame)
            prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=c_num)
            if state._continuation and state._continuation[0] == sweep_frame:
                state._continuation.pop(0)
                sweep_gardiens(state)
            return None
        c_num = int(first_item)
        g_num, _ = state.get_gardien_at_case(c_num)
        gov = _governor_for_peuple(state, "I")
        req = DecisionRequest(
            decideur=gov,
            decision_type=DEC_COLONIE_A_OPEN,
            options=("PASSER", "OUVRIR"),
            context={"case": c_num, "gardien_id": f"G{g_num}"},
        )
        state._continuation.insert(0, ("APPLY_COLONIE_4_3", c_num))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if tag == "TACTIQUE_RANK_5_1":
        r_idx = int(top[1])
        if r_idx >= TRACK_LEN:
            state._continuation.pop(0)
            _transition_step(state, STEP_5_2_RATISSAGE)
            return None
        # Piste fixe T1..T6 : la Tactique imprimée au rang r_idx est toujours T{r_idx+1},
        # même si une tuile Rêve recouvre la case (machines non annulées / choix AVANCER).
        t_code = r_idx + 1
        eligible_m = _eligible_tactique_machines_at_rank(state, t_code)
        if not eligible_m:
            state._continuation[0] = ("TACTIQUE_RANK_5_1", r_idx + 1)
            return None
        if len(eligible_m) == 1:
            rm, mt = eligible_m[0]
            _resolve_tactique_5_1_machine(state, rm, mt, t_code)
            return None
        req = DecisionRequest(
            decideur=state.coordonnateur,
            decision_type=DEC_ORDRE_ATTAQUE_5_1,
            options=tuple(eligible_m),
            context={"rank": t_code, "tactique": code_to_tile_id(t_code)},
        )
        state._continuation.insert(0, ("APPLY_TACTIQUE_5_1", t_code))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if tag == "STEP_5_3_FINISH":
        state._continuation.pop(0)
        sweep_gardiens(state)
        if has_pending_decision(state):
            state._continuation.append(("STEP_5_3_CLEAN_TRAPS",))
            return None
        return _finish_step_5_3_traps_and_end_check(state)

    if tag == "STEP_5_3_CLEAN_TRAPS":
        state._continuation.pop(0)
        return _finish_step_5_3_traps_and_end_check(state)

    if tag == "VOLUNTARY_APP_6_1":
        state._continuation.pop(0)
        state.clear_pending_voluntary_app_reduction(0, 0)
        _transition_step(state, STEP_6_2_EVOLUTION)
        return None

    raise RuntimeError(f"Continuation inconnue : {tag}")


def _resolve_gardien_bets_5_3(state: GameState) -> None:
    """Résout les paris d'activation des Gardiens en 5.3 (avant le test de fin de partie).

    - Pari gagné (>=1 Défenseur posé en 2.2 et 0 restant en 5.3) : le Gardien reste sur la piste ;
      s'il s'agit d'un Gardien évolutif double-face encore en Face 1 (Mode 3/4), il passe en Face 2.
    - Pari perdu (>=1 Défenseur non consommé en 5.3) :
      * Si SLOT_COLONISATION_GARDIENS == 'B' (Bouclier de lisière) et >= 1 jeton Insecte sur sa case
        de la Piste des Gardiens : défausser 1 jeton Insecte pour empêcher le retour en lisière
        (le Gardien reste sur la piste sur sa face actuelle). Le pari reste toutefois PERDU (ne compte
        pas pour l'Éveil de la Forêt et ne fait pas passer en Face 2).
      * Sinon : le Gardien retourne immédiatement sur sa lisière d'origine (LISIERE_UNCONSTRUCTED, Face 1).
      Les Défenseurs reviennent aux joueurs en 6.2/6.3.
    """
    if state.cfg.mode < 2 or state.cfg.nb_animaux_sauvages < 1:
        return
    bouclier_active = state.cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"
    bets_won = 0
    bets_lost = 0
    bouclier_saves = 0
    face2_upgrades = 0
    for c_num in range(1, TRACK_LEN + 1):
        rem = state.count_gardien_pari_defenders_at_case(c_num)
        cons = state.count_gardien_pari_consumed_at_case(c_num)
        g_num, g_face = state.get_gardien_at_case(c_num)
        if rem >= 1:
            bets_lost += 1
            if g_num > 0:
                col_ins = state.get_colonie_at_case(c_num) if bouclier_active else 0
                if bouclier_active and col_ins >= 1:
                    state.set_colonie_at_case(c_num, col_ins - 1)
                    _record_phys_ops(state, 1)
                    bouclier_saves += 1
                else:
                    prim_partage_info_etat_gardien(
                        state, "RETURN_GARDIEN_TO_LISIERE", case_1_6=c_num
                    )
        elif cons >= 1:
            bets_won += 1
            if g_num > 0 and g_face == 1 and state.cfg.mode >= 3:
                slot_id = f"G{g_num}"
                prof = state.cfg.profile_for_slot(slot_id)
                if prof is not None and (slot_id, prof) in DOUBLE_FACE_UPGRADE_GARDIENS:
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


def _finish_step_5_3_traps_and_end_check(state: GameState) -> None:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    removed_traps = 0
    for r in range(n):
        for p in range(1, p_max + 1):
            if state.get_parcel_piege(r, p) == PIEGE_DECLENCHE:
                state.set_parcel_piege(r, p, PIEGE_AUCUN)
                removed_traps += 1
    if removed_traps > 0:
        _record_phys_ops(state, removed_traps)
    _resolve_gardien_bets_5_3(state)
    if _check_end_of_game_condition(state):
        _transition_step(state, STEP_GAME_OVER)
        return
    # Étape 6.1 Apprentissage supprimée en v5.4.2 : passage direct au ménage de fin de tour
    _transition_step(state, STEP_6_2_EVOLUTION)


def _run_step_6_1(state: GameState) -> None:
    """Étape 6.1 supprimée en v5.4.2 (Apprentissage purgé) : transition immédiate vers 6.2."""
    _transition_step(state, STEP_6_2_EVOLUTION)


def _run_step_6_2(state: GameState) -> GameOver | None:
    """Ménage de fin de tour (sans déplacement de Tactiques : piste T1..T6 fixe)."""
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
    _transition_step(state, STEP_6_3_END_TURN)
    return None


def _is_hybrid_construct_3_1_active(state: GameState) -> bool:
    if state.cfg.mode < 3 or state.cfg.profile_for_slot("G13") != "B":
        return False
    for c in range(1, TRACK_LEN + 1):
        if state.get_gardien_at_case(c)[0] == 13:
            return True
    return False


def _is_2cran_migration_4_3_active(state: GameState) -> bool:
    if state.cfg.mode < 3 or state.cfg.profile_for_slot("G15") != "B":
        return False
    for c in range(1, TRACK_LEN + 1):
        if state.get_gardien_at_case(c)[0] == 15:
            return True
    return False


def _lisiere_has_furtivite_insect(state: GameState, l_idx: int) -> bool:
    for p in range(1, state.cfg.p_max + 1):
        if state.get_furtivite_insectes(l_idx, p) >= 1:
            return True
    return False


def _is_slot_ready_for_construction_3_1(
    state: GameState, slot_idx: int, *, hybrid_active: bool
) -> bool:
    st, nb = state.get_lisiere_tile_state(slot_idx)
    if st != LISIERE_UNCONSTRUCTED:
        return False
    if nb == 2:
        return True
    if hybrid_active and nb == 1:
        return _lisiere_has_furtivite_insect(state, slot_idx // 2)
    return False


def _advance_main_step(state: GameState) -> DecisionRequest | GameOver | None:
    """Exécute un pas de l'étape principale state.step."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    step = state.step

    if step == STEP_GAME_OVER:
        return apply_repousse_finale(state)

    if step == STEP_1_1_RATISSAGE:
        # v6.1 : seul 6.3 fait basculer les machines en Ratissage (test redondant 1.1 supprimé)
        _transition_step(state, STEP_1_2_DEAL)
        return None

    if step == STEP_1_2_DEAL:
        best_trees = -1
        start_seat = state.coordonnateur
        for off in range(n):
            s = (state.coordonnateur + off) % n
            tr = state.total_arbres_rayon(s)
            if tr > best_trees:
                best_trees = tr
                start_seat = s
        dealt = 0
        shortages = 0
        for off in range(n):
            s = (start_seat + off) % n
            c = state.draw_next_machine_card()
            state.set_player_hand(s, c, 0, 0, 0, 0)
            if c != CARD_NONE:
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
        dice_ops = 0
        for s in range(n):
            card, _, _, _, _ = state.get_player_hand(s)
            if 1 <= card <= 12:
                peuple_id = PEUPLE_TO_ID[state.cfg.peuples[s]]
                d1 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 0)
                d2 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 1)
                state.set_player_hand(s, card, d1, d2, min(d1, d2), 0)
                dice_ops += 2
            else:
                state.set_player_hand(s, card, 0, 0, 0, 0)
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
                opts_1 = list_legal_targets(state, s, is_first_defender=True) or (("PASSER_IMPASSE",),)
                req = DecisionRequest(
                    s, DEC_POSE_DEFENSEUR_1, opts_1, _STEP_2_1_CTX_BY_TOUR[state.tour]
                )
                state._continuation.append(("APPLY_DEF1", s))
                state._continuation.insert(0, ("WAIT_DECISION", req))
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
                state._continuation.append(("APPLY_DEF2_INIT", s))
                state._continuation.insert(0, ("WAIT_DECISION", req))
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
        hybrid_active = _is_hybrid_construct_3_1_active(state)
        ready_slots = [
            (state.coordonnateur * 2 + off) % (2 * n)
            for off in range(2 * n)
            if _is_slot_ready_for_construction_3_1(
                state, (state.coordonnateur * 2 + off) % (2 * n), hybrid_active=hybrid_active
            )
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
        state._continuation.append(("APPLY_CONSTRUCT_ORDER",))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if step == STEP_3_2_REVEAL:
        _run_step_3_2(state)
        return None

    if step == STEP_4_1_FURTIVITE:
        _run_step_4_1_from(state, 0)
        return None

    if step == STEP_4_2_NIDS:
        if state.cfg.mode == 1:
            _transition_step(state, STEP_4_3_MIGRATION)
            return None
        eligible_nids: list[int] = []
        m3_b_auto = state.cfg.mode >= 3 and state.cfg.profile_for_slot("M3") == "B"
        for m_num in range(1, 6):
            pos_info = state.get_nid_position(m_num)
            if pos_info is not None:
                r, p, active_turn = pos_info
                if not active_turn and (
                    state.get_parcel_defenseurs(r, p) >= 1
                    or (m3_b_auto and m_num == 3 and state.get_parcel_insectes(r, p) >= 2)
                ):
                    eligible_nids.append(m_num)
        if not eligible_nids:
            _transition_step(state, STEP_4_3_MIGRATION)
            return None
        if len(eligible_nids) == 1:
            _resolve_nid_block(state, eligible_nids[0])
            return None
        gov = _governor_for_peuple(state, "I")
        req = DecisionRequest(gov, DEC_ORDRE_NID_4_2, tuple(eligible_nids), {"tour": state.tour})
        state._continuation.append(("APPLY_NID_4_2",))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if step == STEP_4_3_MIGRATION:
        wheel_queue: list[tuple[str, int, int]] = []
        for off in range(n):
            r = (state.coordonnateur + off) % n
            for p in range(1, p_max + 1):
                cnt = state.get_parcel_insectes(r, p)
                if cnt:
                    wheel_queue.extend([("FORET", r, p)] * cnt)
            for p in range(1, p_max + 1):
                cnt_f = state.get_furtivite_insectes(r, p)
                if cnt_f:
                    wheel_queue.extend([("FURTIVITE", r, p)] * cnt_f)
        if wheel_queue:
            state._continuation.append(("MIGRATION_QUEUE_4_3", tuple(wheel_queue), 0))
        elif state.cfg.mode >= 2:
            state._continuation.append(("COLONIE_SCAN_4_3", 1))
        else:
            _transition_step(state, STEP_5_1_TACTIQUES)
        return None

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
        state._continuation.append(("APPLY_RATISSAGE_5_2",))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if step == STEP_5_3_END_CHECK:
        if state.cfg.mode >= 3:
            state._continuation.insert(0, ("STEP_5_3_FINISH",))
            dispatch_hook(state, HOOK_5_3_PRE_RETRAIT, {})
            return None
        dispatch_hook(state, HOOK_5_3_PRE_RETRAIT, {})
        _finish_step_5_3_traps_and_end_check(state)
        if state.step == STEP_GAME_OVER:
            return apply_repousse_finale(state)
        return None

    if step == STEP_6_1_APPRENTISSAGE:
        _run_step_6_1(state)
        return None

    if step == STEP_6_2_EVOLUTION:
        return _run_step_6_2(state)

    if step == STEP_6_3_END_TURN:
        _transition_eligible_machines_to_ratissage(state, remove_from_deck=False)
        state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
        _record_phys_ops(state, 1)
        trk = _get_active_telemetry()
        if trk is not None:
            trk.on_end_turn(state, game_over=False)
        state.coordonnateur = (state.coordonnateur + 1) % n
        state.tour += 1
        _transition_step(state, STEP_1_1_RATISSAGE)
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
                    f"mode={cfg.mode}, chassis_id=?, n_players={cfg.n_players}, "
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
    if st != LISIERE_UNCONSTRUCTED:
        return None
    if nb == 1:
        if not _is_hybrid_construct_3_1_active(state):
            return None
        l_idx = slot_idx // 2
        if not _lisiere_has_furtivite_insect(state, l_idx):
            return None
        state._continuation.insert(0, ("CONSTRUCT_SLOT_PAID", slot_idx))
        dispatch_hook(
            state,
            HOOK_3_1_CONSTRUCTION,
            {
                "target_slot_id": state.cfg.lisiere_slots[slot_idx],
                "slot_idx": slot_idx,
                "hybrid_pay": True,
                "lisiere": l_idx,
            },
        )
        return None
    if nb < 2:
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

    if fam == FAMILLE_GARDIEN:
        allowed_cases = tuple(int(c) for c in constr_ctx.get("allowed_cases", ()))
        free_cases = tuple(
            c
            for c in range(1, TRACK_LEN + 1)
            if state.get_gardien_at_case(c)[0] == 0 and (not allowed_cases or c in allowed_cases)
        )
        state._continuation.insert(0, ("CHECK_LIBERATION_3_1", slot_idx))
        if not free_cases:
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
            return None
        if len(free_cases) == 1:
            state.set_gardien_at_case(free_cases[0], num, 1)
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
            _record_phys_ops(state, 1)
            return None
        req = DecisionRequest(
            decideur=gov,
            decision_type=DEC_CHOIX_CASE_GARDIEN,
            options=free_cases,
            context={"slot_idx": slot_idx, "tile_id": tile_id},
        )
        state._continuation.insert(0, ("APPLY_GARDIEN_CASE_3_1", slot_idx, num))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if fam == FAMILLE_REVE:
        insert_reve_on_track(state, num)
        state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
        state._continuation.insert(0, ("CHECK_LIBERATION_3_1", slot_idx))
        return None

    # FAMILLE_CROISSANCE (Nid M1..M5) : gouverné par I (ou Coordonnateur si I absent)
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
        return None

    if len(valid_parcels) == 1:
        rn, pn = valid_parcels[0]
        state.set_parcel_nid(rn, pn, num, False)
        _move_all_builders_to_nid_parcel(state, slot_idx, rn, pn)
        return None

    gov_nid = _governor_for_peuple(state, "I")
    req = DecisionRequest(
        decideur=gov_nid,
        decision_type=DEC_PLACEMENT_NID_3_1,
        options=tuple(valid_parcels),
        context={"slot_idx": slot_idx, "tile_id": tile_id},
    )
    state._continuation.insert(0, ("APPLY_NID_PLACE_3_1", slot_idx, num))
    state._continuation.insert(0, ("WAIT_DECISION", req))
    return req


def _resolve_nid_block(state: GameState, m_num: int) -> None:
    """Résout un Nid en 4.2 comme un bloc indivisible avant balayage Gardiens 1..6."""
    pos_info = state.get_nid_position(m_num)
    if pos_info is None:
        return
    r, p, _ = pos_info
    state.set_nid_activated(m_num, True)
    cur_ins = state.get_parcel_insectes(r, p)
    created = 1 if cur_ins <= 1 else 2
    # v5.4.7 : la production d'un Nid en 4.2 n'allume jamais 6. Insecte (partition stricte : 3.2 Bug ou 5.1 Parade Insecte uniquement)
    prim_creation_entite(state, "INSECTE", ray=r, p=p, count=created, light_trigger=False)
    if state.cfg.mode >= 3:
        sweep_frame = ("SWEEP_GARDIENS_NOW",)
        state._continuation.insert(0, sweep_frame)
        dispatch_hook(
            state,
            HOOK_4_2_NID_APRES_PROD,
            {"slot_id": f"M{m_num}", "m_num": m_num, "ray": r, "p": p},
        )
        if state._continuation and state._continuation[0] == sweep_frame:
            state._continuation.pop(0)
            sweep_gardiens(state)
        return
    dispatch_hook(
        state,
        HOOK_4_2_NID_APRES_PROD,
        {"slot_id": f"M{m_num}", "m_num": m_num, "ray": r, "p": p},
    )
    sweep_gardiens(state)


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

        if tag == "APPLY_DEF1":
            _, seat = state._continuation.pop(0)
            apply_step2_def1(state, int(seat), choice, check_legal=False)
            return

        if tag == "APPLY_DEF2_INIT":
            _, seat = state._continuation.pop(0)
            apply_step2_def2(state, int(seat), choice, check_legal=False)
            return

        if tag == "STEP2_REV_QUEUE":
            _, seats_tuple, cursor = top
            seat = seats_tuple[cursor]
            moved = apply_step2_def2(state, int(seat), choice, check_legal=False)
            if moved:
                p_idx, _ = state.get_step2_pass_state()
                state.set_step2_pass_state(p_idx, True)
            state._continuation[0] = ("STEP2_REV_QUEUE", seats_tuple, cursor + 1)
            return

        if tag == "APPLY_CONSTRUCT_ORDER":
            state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_constr_3_1 += 1
            state._continuation.insert(0, ("CONSTRUCT_SLOT", int(choice)))
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
            state.set_parcel_nid(int(rn), int(pn), int(m_num), False)
            _move_all_builders_to_nid_parcel(state, int(slot_idx), int(rn), int(pn))
            return

        if tag == "APPLY_NID_4_2":
            state._continuation.pop(0)
            if trk is not None and len(req.options) >= 2:
                trk.dil_ordre_nid_4_2 += 1
            _resolve_nid_block(state, int(choice))
            return

        if tag in ("APPLY_MIGRATION_4_3", "APPLY_MIGRATION_4_3_CRAN2"):
            _, src = state._continuation.pop(0)
            loc_type, idx_a, src_p = src
            dst_kind = choice[0]
            if trk is not None and len(req.options) >= 2:
                trk.on_migration_decision(str(dst_kind))
            new_wheel_src: tuple[str, int, int] | None = None
            if dst_kind != "RESTER":
                src_kwargs: dict[str, Any] = (
                    {"src_lisiere": idx_a, "src_p": src_p}
                    if loc_type == "FURTIVITE"
                    else {"src_ray": idx_a, "src_p": src_p}
                )
                if dst_kind == "FORET":
                    prim_deplacement(
                        state,
                        "INSECTE",
                        dst_ray=int(choice[1]),
                        dst_p=int(choice[2]),
                        **src_kwargs,
                    )
                    new_wheel_src = ("FORET", int(choice[1]), int(choice[2]))
                elif dst_kind == "FURTIVITE":
                    prim_deplacement(
                        state,
                        "INSECTE",
                        dst_lisiere=int(choice[1]),
                        dst_p=int(choice[2]),
                        **src_kwargs,
                    )
                    new_wheel_src = ("FURTIVITE", int(choice[1]), int(choice[2]))
                elif dst_kind in ("BUG", "COLONIE"):
                    prim_deplacement(
                        state,
                        "INSECTE",
                        global_track=dst_kind,
                        global_case=int(choice[1]),
                        **src_kwargs,
                    )
                    if (
                        state.cfg.mode >= 3
                        and loc_type == "FORET"
                        and src_p != state.last_non_razed_parcel(idx_a)
                    ):
                        dispatch_hook(
                            state,
                            HOOK_4_3_MIGRATION_DESTS,
                            {"phase": "APPLIED", "src": src, "choice": choice, "opts": []},
                        )
                if tag == "APPLY_MIGRATION_4_3":
                    # Règle spéciale 4.3 : déplacer (+1 dans prim_deplacement) + coucher suivi + redresser = 3 ops
                    _record_phys_ops(state, 2)
                if (
                    tag == "APPLY_MIGRATION_4_3"
                    and new_wheel_src is not None
                    and _is_2cran_migration_4_3_active(state)
                ):
                    moves_2 = _list_insect_1cran_moves(state, new_wheel_src)
                    if len(moves_2) > 1:
                        gov = _governor_for_peuple(state, "I")
                        req_2 = DecisionRequest(
                            decideur=gov,
                            decision_type=DEC_MIGRATION_INSECTE_4_3,
                            options=moves_2,
                            context={"source": new_wheel_src, "cran": 2},
                        )
                        state._continuation.insert(0, ("APPLY_MIGRATION_4_3_CRAN2", new_wheel_src))
                        state._continuation.insert(0, ("WAIT_DECISION", req_2))
                        return
            assert state._continuation and state._continuation[0][0] == "MIGRATION_QUEUE_4_3"
            _, q_tup, cur = state._continuation[0]
            state._continuation[0] = ("MIGRATION_QUEUE_4_3", q_tup, cur + 1)
            return

        if tag == "APPLY_COLONIE_4_3":
            _, c_num = state._continuation.pop(0)
            case_int = int(c_num)
            state._continuation.insert(0, ("COLONIE_SCAN_4_3", case_int + 1))
            if choice == "OUVRIR":
                cur_col = state.get_colonie_at_case(case_int)
                assert cur_col >= 1
                state.set_colonie_at_case(case_int, cur_col - 1)
                _record_phys_ops(state, 1)
                sweep_frame = ("SWEEP_GARDIENS_NOW",)
                state._continuation.insert(0, sweep_frame)
                prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=case_int)
                if state._continuation and state._continuation[0] == sweep_frame:
                    state._continuation.pop(0)
                    sweep_gardiens(state)
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

        if tag == "APPLY_VOLUNTARY_APP_6_1":
            state._continuation.pop(0)
            state.clear_pending_voluntary_app_reduction(0, 0)
            state._continuation.insert(0, ("VOLUNTARY_APP_6_1",))
            return

        raise RuntimeError(f"Tag de continuation inconnu : {tag}")
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev_trk)
