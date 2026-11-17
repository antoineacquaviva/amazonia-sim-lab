"""Machine à états déterministe suspendable des 6 étapes (Modes 1 & 2, 128 châssis v5.3)."""

from __future__ import annotations

from typing import Any

from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_REVEIL_GARDIENS,
    CAUSE_TOUR_8,
    HOOK_1_3_LECTURE_DE,
    HOOK_2_1_DEBUT,
    HOOK_3_1_CONSTRUCTION,
    HOOK_3_2_OUVERTURE_REVE,
    HOOK_3_2_REVELATION,
    HOOK_4_1_FURTIVITE,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_4_3_COLONIE_FIN,
    HOOK_5_3_PRE_RETRAIT,
    HOOK_5_DEFENSE_PARCELLE,
    HOOK_5_PARADE_HARPIE,
    HOOK_5_PARADE_JAGUAR,
    HOOK_5_SEUIL_PARADE,
    HOOK_5_TERRASSEMENT,
    HOOK_6_1_BUG,
    HOOK_6_1_REDUCTION_VOLONTAIRE,
    HOOK_6_2_AVANCEMENT,
    HOOK_REPOUSSE_FINALE,
    DecisionRequest,
    GameOver,
    apply_machine_nid_contact,
    dispatch_hook,
    get_tile_registration,
    prim_creation_entite,
    prim_deplacement,
    prim_mod_apprentissage,
    prim_partage_info_etat_gardien,
    prim_permutation_piste,
    register_tile,
)
from engine.rng import SRC_DICE, roll_d6
from engine.state import (
    FACE_DEFINITIF,
    FACE_REFLEXION,
    FAMILLE_GARDIEN,
    FAMILLE_REVE,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RETIRED,
    MACHINE_STATUS_SIEGE,
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
    STEP_1_1_SIEGE,
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
    STEP_5_2_SIEGES,
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
    "DEC_ORDRE_SIEGE_5_2",
    "DEC_PLACEMENT_NID_3_1",
    "DEC_POSE_DEFENSEUR_1",
    "DEC_POSE_DEFENSEUR_2",
    "DEC_RETRAIT_APPRENTISSAGE_6_1",
    "DEC_REVISION_DEFENSEUR_2",
    "apply_choice",
    "apply_repousse_finale",
    "apply_step2_def1",
    "apply_step2_def2",
    "compute_parade_seuil",
    "ensure_builtin_migration_registered",
    "insert_reve_on_track",
    "is_machine_active_this_turn",
    "list_legal_targets",
    "lock_all_def2_in_place",
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
DEC_LIBERATION_BATISSEUR_3_1: str = "LIBERATION_BATISSEUR_3_1"
DEC_PLACEMENT_NID_3_1: str = "PLACEMENT_NID_3_1"
DEC_ORDRE_NID_4_2: str = "ORDRE_NID_4_2"
DEC_MIGRATION_INSECTE_4_3: str = "MIGRATION_INSECTE_4_3"
DEC_COLONIE_A_OPEN: str = "COLONIE_A_OPEN"
DEC_ORDRE_ATTAQUE_5_1: str = "ORDRE_ATTAQUE_TACTIQUE_5_1"
DEC_ORDRE_SIEGE_5_2: str = "ORDRE_SIEGE_5_2"
DEC_RETRAIT_APPRENTISSAGE_6_1: str = "RETRAIT_APPRENTISSAGE_6_1"


# ---------------------------------------------------------------------------
# Profils standards Migration A/A sur le bus de hooks (actifs dès le Mode 2)
# ---------------------------------------------------------------------------


def _bug_a_handler(state: GameState, _hook: str, _ctx: dict[str, Any]) -> None:
    """SLOT_BUG_CERVEAU.A : -1 Apprentissage par Insecte si > 0, sinon Insecte conservé."""
    for rank_idx in range(TRACK_LEN):
        case_num = rank_idx + 1
        bugs = state.get_bugs_at_case(case_num)
        app = state.get_apprentissage_at_rank(rank_idx)
        if bugs > 0 and app > 0:
            consumed = min(bugs, app)
            state.set_bugs_at_case(case_num, bugs - consumed)
            prim_mod_apprentissage(state, rank_idx, -consumed)


def _colonie_a_handler(state: GameState, _hook: str, ctx: dict[str, Any]) -> list[int]:
    """SLOT_COLONISATION_GARDIENS.A : signale les cases 1..6 éligibles à l'ouverture."""
    start_case = int(ctx.get("start_case", 1))
    eligible: list[int] = []
    for c in range(start_case, TRACK_LEN + 1):
        if state.get_colonie_at_case(c) >= 1:
            g_num, _, used = state.get_gardien_at_case(c)
            if g_num > 0 and not used:
                eligible.append(c)
    return eligible


def ensure_builtin_migration_registered() -> None:
    """Garantit l'enregistrement de Bug A et Colonie A sur le bus."""
    if get_tile_registration("SLOT_BUG_CERVEAU", "A") is None:
        register_tile("SLOT_BUG_CERVEAU", "A", hooks=(HOOK_6_1_BUG,))(_bug_a_handler)
    if get_tile_registration("SLOT_COLONISATION_GARDIENS", "A") is None:
        register_tile("SLOT_COLONISATION_GARDIENS", "A", hooks=(HOOK_4_3_COLONIE_FIN,))(
            _colonie_a_handler
        )


ensure_builtin_migration_registered()


# ---------------------------------------------------------------------------
# Balayage à plat des Gardiens (1 -> 6) & Résonance 4
# ---------------------------------------------------------------------------


def sweep_gardiens(state: GameState) -> int:
    """Balayage croissant 1..6 répété tant qu'une case allumée porte un Gardien disponible.

    Retourne le nombre de Gardiens ouverts durant cette fenêtre de balayage.
    """
    if state.cfg.mode == 1:
        state.triggers_lit = 0
        return 0

    opened_total = 0
    while True:
        opened_in_pass = False
        for case_num in range(1, TRACK_LEN + 1):
            if state.is_trigger_lit(case_num):
                g_num, _, used = state.get_gardien_at_case(case_num)
                if g_num > 0 and not used:
                    state.clear_trigger(case_num)
                    prim_partage_info_etat_gardien(
                        state, "MARK_GARDIEN_OPENED", case_1_6=case_num
                    )
                    opened_total += 1
                    opened_in_pass = True
        if not opened_in_pass:
            break

    state.triggers_lit = 0
    return opened_total


# ---------------------------------------------------------------------------
# Gouvernance & aides Étape 2 (Anti-blocage + Furtivité 4 slots)
# ---------------------------------------------------------------------------


def _governor_for_peuple(state: GameState, peuple_code: str) -> int:
    seat = state.cfg.seat_of_peuple(peuple_code)
    return seat if seat is not None else state.coordonnateur


# Tables immuables pré-allouées de cibles et d'options pour éviter ~2M d'allocations de tuples / 1k parties
_FORET_TARGETS: tuple[tuple[tuple[str, int, int], ...], ...] = tuple(
    tuple(("FORET", r, p) for p in range(MAX_P + 1)) for r in range(MAX_N)
)
_FURT_TARGETS: tuple[tuple[tuple[tuple[str, int, int, int], tuple[str, int, int, int]], ...], ...] = tuple(
    tuple((("FURTIVITE", l_idx, p, 0), ("FURTIVITE", l_idx, p, 1)) for p in range(MAX_P + 1))
    for l_idx in range(MAX_N)
)
_LIS_TARGETS: tuple[tuple[str, int], ...] = tuple(
    ("LISIERE", slot_idx) for slot_idx in range(NUM_SYNERGY_SLOTS)
)
_ALL_CANONICAL_TARGETS: tuple[tuple[Any, ...], ...] = (
    tuple(t for row in _FORET_TARGETS for t in row[1:])
    + tuple(t for row in _FURT_TARGETS for pair in row[1:] for t in pair)
    + _LIS_TARGETS
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
        return _FURT_TARGETS[a][b][c // 2]
    if kind == "LISIERE":
        return _LIS_TARGETS[a]
    return None


def list_legal_targets(
    state: GameState,
    seat: int,
    *,
    is_first_defender: bool,
    exclude_own_def2: bool = False,
) -> tuple[tuple[Any, ...], ...]:
    """Énumère toutes les poses légales (anti-blocage v5.3) pour un Défenseur de `seat`."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    own_spot = _current_def_canonical_spot(state, seat, 1) if exclude_own_def2 else None

    if is_first_defender:
        rays, lisieres, lis_slots = _DEF1_LOCAL_RANGES[(n, seat)]
    else:
        rays = _RAYS_BY_N[n]
        lisieres = rays
        lis_slots = _LIS_SLOTS_BY_N[n]

    targets: list[tuple[Any, ...]] = []

    # 1. Parcelles Forêt non rasées
    for r in rays:
        f_row = _FORET_TARGETS[r]
        for p in range(1, p_max + 1):
            if not state.is_route_forestiere(r, p):
                targets.append(f_row[p])

    # 2. Cases Furtivité (rive non face à une Route, < 2 Défenseurs sur la case)
    for l_idx in lisieres:
        fu_row = _FURT_TARGETS[l_idx]
        r1 = (l_idx + 1) % n
        for p in range(1, p_max + 1):
            tot_defs = state.get_furtivite_total_defs(l_idx, p)
            if (
                own_spot is not None
                and own_spot[0] == "FURTIVITE"
                and own_spot[1] == l_idx
                and own_spot[2] == p
            ):
                tot_defs -= 1
            if tot_defs >= 2:
                continue
            pair = fu_row[p]
            if not state.is_route_forestiere(l_idx, p):
                targets.append(pair[0])
            if not state.is_route_forestiere(r1, p):
                targets.append(pair[1])

    # 3. Tuiles de Synergie en lisière (interdites en Mode 1, non construites et < 2 bâtisseurs)
    if state.cfg.mode >= 2:
        for slot_idx in lis_slots:
            st, nb = state.get_lisiere_tile_state(slot_idx)
            cand_l = _LIS_TARGETS[slot_idx]
            if own_spot == cand_l:
                nb = max(0, nb - 1)
            if st == LISIERE_UNCONSTRUCTED and nb < 2:
                targets.append(cand_l)

    # Repli exceptionnel si 100 % du territoire local d'un siège est intégralement rasé/plein
    if not targets and is_first_defender:
        return list_legal_targets(state, seat, is_first_defender=False, exclude_own_def2=False)

    return tuple(targets)


def _apply_defender_target(
    state: GameState, seat: int, def_idx: int, target: tuple[Any, ...], face: int
) -> None:
    kind = target[0]
    if kind == "FORET":
        _, r, p = target
        state.place_defender_foret(seat, def_idx, int(r), int(p), face)
    elif kind == "FURTIVITE":
        _, l_idx, p, rive = target
        state.enter_furtivite(seat, def_idx, int(l_idx), int(p), int(rive), face)
    elif kind == "LISIERE":
        _, slot_idx = target
        state.place_defender_lisiere_tile(seat, def_idx, int(slot_idx), face)
    elif kind == "PASSER_IMPASSE":
        state.mark_defender_impasse(seat, def_idx, face)
        return
    else:
        raise ValueError(f"Cible Défenseur invalide : {target}")


def apply_step2_def1(
    state: GameState, seat: int, target: tuple[Any, ...], *, check_legal: bool = True
) -> None:
    """API publique (bots & moteur) : pose le 1er Défenseur d'un siège sur face définitive."""
    if check_legal:
        legal = list_legal_targets(state, seat, is_first_defender=True)
        if legal:
            assert target in legal, f"Cible 2.1 illégale pour siège {seat} : {target}"
    _apply_defender_target(state, seat, 0, target, FACE_DEFINITIF)


def apply_step2_def2(
    state: GameState, seat: int, action: tuple[str, Any], *, check_legal: bool = True
) -> bool:
    """API publique (bots & moteur) : pose ou révise le 2e Défenseur d'un siège.

    Retourne True si un déplacement physique a eu lieu (utile pour le suivi des passes 2.2).
    """
    act_type, target = action
    if act_type == "GARDER_REFLEXION":
        return False
    if act_type == "VERROUILLER_DEFINITIF":
        state.flip_defender2_to_definitif_in_place(seat)
        return False

    face = FACE_DEFINITIF if act_type in ("POSER_DEFINITIF", "DEPLACER_DEFINITIF") else FACE_REFLEXION
    prev_spot = _current_def_canonical_spot(state, seat, 1)
    if check_legal:
        legal = list_legal_targets(state, seat, is_first_defender=False, exclude_own_def2=True)
        if legal:
            assert target in legal, f"Cible 2.2 illégale pour siège {seat} : {target}"
    _apply_defender_target(state, seat, 1, target, face)
    return prev_spot != target


def lock_all_def2_in_place(state: GameState) -> None:
    """Retournement simultané sur place de tous les 2es Défenseurs encore en réflexion."""
    for s in range(state.cfg.n_players):
        if state.get_player_def_loc_raw(s, 1) != 0 and not state.is_player_def2_definitif(s):
            state.flip_defender2_to_definitif_in_place(s)
    state.step2_locked = True


# ---------------------------------------------------------------------------
# Étape 3.1 : Insertion d'un Rêve & Constructions obligatoires
# ---------------------------------------------------------------------------


def insert_reve_on_track(state: GameState, r_num: int) -> int | None:
    """Règle A11 : éjecte la Tactique la plus à droite, glissement partiel à gauche,
    insertion du Rêve en case 6, Bugs fixes sur leurs numéros d'emplacement.

    Retourne le code de la Tactique éjectée (1..6).
    """
    assert 1 <= r_num <= 10
    hole_idx: int | None = None
    for idx in range(TRACK_LEN - 1, -1, -1):
        code = state.get_tactique_at_rank(idx)
        if is_tactique_code(code):
            hole_idx = idx
            break
    assert hole_idx is not None, "Aucune Tactique restante à éjecter"

    ejected_code = state.get_tactique_at_rank(hole_idx)
    for idx in range(hole_idx, TRACK_LEN - 1):
        state.set_tactique_at_rank(idx, state.get_tactique_at_rank(idx + 1))
        state.set_apprentissage_at_rank(idx, state.get_apprentissage_at_rank(idx + 1))

    state.set_tactique_at_rank(TRACK_LEN - 1, TILE_R_BASE + r_num)
    state.set_apprentissage_at_rank(TRACK_LEN - 1, 0)
    return ejected_code


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


def _liberation_options_n3(
    state: GameState, slot_idx: int
) -> tuple[tuple[int, int, int, int], ...]:
    """Options de libération d'1 bâtisseur à N=3 : (b_seat, b_def_idx, ray, p_first)."""
    if state.cfg.n_players != 3:
        return ()
    lisiere_idx = slot_idx // 2
    r0 = lisiere_idx
    r1 = (lisiere_idx + 1) % state.cfg.n_players
    valid_rays: list[tuple[int, int]] = []
    for r in (r0, r1):
        p_first = state.first_non_razed_from_border(r)
        if p_first is not None and (r, p_first) not in valid_rays:
            valid_rays.append((r, p_first))
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


# ---------------------------------------------------------------------------
# Étape 4.1 & Étape 5 : Attaques d'un seul tenant, Parades & Routes
# ---------------------------------------------------------------------------


def is_machine_active_this_turn(state: GameState, ray: int, m_type: int) -> bool:
    """Vrai si la machine est en Siège ou activée par une carte non annulée en 3.2."""
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
        return False
    if st == MACHINE_STATUS_SIEGE:
        return True
    target_card = machine_card_code(ray, m_type)
    for s in range(state.cfg.n_players):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if card == target_card and bound_t > 0:
            return True
    return False


def _effective_machine_power(state: GameState, ray: int, m_type: int) -> tuple[int, int]:
    rouges, bleus = state.get_machine_tokens(ray, m_type)
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
            r_o, b_o = state.get_machine_tokens(ray, other_type)
            rouges += r_o
            bleus += b_o
    return rouges, bleus


def compute_parade_seuil(
    state: GameState, ray: int, m_type: int, target_p: int, tactique: TactiqueSpec
) -> int:
    """Calcule le Seuil de Parade effectif (plancher 1) pour une frappe sur (ray, target_p)."""
    base = state.cfg.dotation_arbres[target_p - 1]
    offset = state.cfg.offset_seuil_parade
    rouges, bleus = _effective_machine_power(state, ray, m_type)
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
    # Nettoyer toute présence résiduelle sur la parcelle rasée (inoccupable)
    m_num, _ = state.get_parcel_nid(ray, razed_p)
    if m_num > 0:
        state.clear_nid(m_num)
        l_slot = state.find_lisiere_slot_by_tile_id(f"M{m_num}")
        if l_slot is not None:
            state.set_lisiere_tile_state(l_slot, LISIERE_UNCONSTRUCTED, 0)

    state.set_parcel_insectes(ray, razed_p, 0)
    state.set_parcel_piege(ray, razed_p, PIEGE_AUCUN)

    # Renvoyer en main d'éventuels Défenseurs restés sur la parcelle rasée
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw != 0:
                kind, a, b, _ = state.decode_def_loc(raw)
                if kind == "FORET" and a == ray and b == razed_p:
                    state.remove_player_defender(s, d)
    state.set_parcel_defenseurs(ray, razed_p, 0)

    # Repli automatique des machines présentes sur (ray, razed_p)
    for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
        pos, st, pending_s = state.get_machine_pos_status(ray, mt)
        if st == MACHINE_STATUS_RETIRED or pos != razed_p:
            continue
        p_back = state.next_non_razed_towards_border(ray, razed_p)
        if p_back is not None:
            state.set_machine_pos_status(ray, mt, p_back, st, pending_s)
            apply_machine_nid_contact(state, ray, p_back)
        else:
            p_fwd = state.next_non_razed_towards_heart(ray, razed_p)
            if p_fwd is not None:
                state.set_machine_pos_status(ray, mt, p_fwd, st, pending_s)
                apply_machine_nid_contact(state, ray, p_fwd)
            else:
                # Tout le rayon est rasé : retrait définitif de la partie
                state.set_machine_pos_status(ray, mt, 0, MACHINE_STATUS_RETIRED, False)
                state.set_machine_tokens(ray, mt, 0, 0)


def resolve_single_machine_attack(
    state: GameState, ray: int, m_type: int, tactique: TactiqueSpec, *, is_siege: bool = False
) -> None:
    """Résout une machine d'un seul tenant : cibles dynamiques -> frappes -> avancée -> Rouge -> Gardiens."""
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
        state.set_machine_turn_stats(ray, m_type, 0, False, True)
        return

    # 1. Lecture dynamique des cibles depuis la position réelle (en sautant toute Route)
    targets: list[int] = []
    for c_type in tactique.cibles:
        if c_type == "SUR_PLACE":
            if not state.is_route_forestiere(ray, pos):
                targets.append(pos)
        elif c_type == "DEVANT":
            p_dev = state.next_non_razed_towards_heart(ray, pos)
            if p_dev is not None:
                targets.append(p_dev)

    damaged_parcels = 0
    aborted_by_jaguar = False

    # 2. Résolution séquentielle des frappes
    for target_p in targets:
        if state.is_route_forestiere(ray, target_p):
            continue

        # Maillon 1 : Bond du Jaguar (Mode 3+)
        jag_ctx: dict[str, Any] = {"ray": ray, "m_type": m_type, "target_p": target_p, "parried": False}
        dispatch_hook(state, HOOK_5_PARADE_JAGUAR, jag_ctx)
        if jag_ctx.get("parried"):
            state.light_trigger(1)
            aborted_by_jaguar = True
            break

        # Maillon 2 : Piquée de la Harpie (Mode 3+ ou flag PFLAG_AUTO_PARADE_ONCE)
        if (
            state.has_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE)
            and state.get_parcel_defenseurs(ray, target_p) >= 2
        ):
            state.set_parcel_flag_turn(ray, target_p, PFLAG_AUTO_PARADE_ONCE, False)
            state.light_trigger(1)
            continue

        har_ctx: dict[str, Any] = {"ray": ray, "m_type": m_type, "target_p": target_p, "parried": False}
        dispatch_hook(state, HOOK_5_PARADE_HARPIE, har_ctx)
        if har_ctx.get("parried"):
            state.light_trigger(1)
            continue

        # Calcul de la Défense totale sur la parcelle à cet instant
        local_defs = state.get_parcel_defenseurs(ray, target_p)
        local_ins = state.get_parcel_insectes(ray, target_p)
        def_ctx: dict[str, Any] = {
            "ray": ray,
            "m_type": m_type,
            "target_p": target_p,
            "def_points": local_defs,
            "ins_points": local_ins,
            "remote_support": 0,
        }
        dispatch_hook(state, HOOK_5_DEFENSE_PARCELLE, def_ctx)
        def_non_ins = int(def_ctx["def_points"]) + int(def_ctx["remote_support"])
        total_def = def_non_ins + int(def_ctx["ins_points"])

        # Maillon 3 : Piège Embuscade (armé dès que Défense totale >= 1)
        piege_st = state.get_parcel_piege(ray, target_p)
        if piege_st in (PIEGE_ACTIF, PIEGE_DECLENCHE) and total_def >= 1:
            state.set_parcel_piege(ray, target_p, PIEGE_DECLENCHE)
            state.light_trigger(1)
            continue

        # Maillon 4 : Parade classique (défausse immédiate des Insectes manquants, zéro dette)
        seuil = compute_parade_seuil(state, ray, m_type, target_p, tactique)
        if total_def >= seuil:
            manque = max(0, seuil - def_non_ins)
            if manque > 0:
                ins_to_discard = min(local_ins, manque)
                state.set_parcel_insectes(ray, target_p, local_ins - ins_to_discard)
            state.light_trigger(1)
            continue

        # Non parée : application des dégâts
        arbres_before = state.get_parcel_arbres(ray, target_p)
        souches_before = state.get_parcel_souches(ray, target_p)
        arbres_after = arbres_before
        souches_after = souches_before

        if m_type == MACHINE_ABATTEUSE:
            if arbres_before > 0:
                cut = min(2, arbres_before)
                arbres_after -= cut
                souches_after += cut
            elif (
                (is_siege or st == MACHINE_STATUS_SIEGE)
                and state.cfg.role_abatteuse_fin_de_piste == "ARRACHE_1_SOUCHE_SI_SANS_ARBRE"
                and souches_before > 0
            ):
                souches_after -= 1
        else:
            cut = min(1, arbres_before)
            arbres_after -= cut
            souches_after += cut
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
            souches_after = min(souches_after, max(0, int(terr_ctx["protected_souches"])))

        state.set_parcel_arbres_souches(ray, target_p, arbres_after, souches_after)
        if arbres_after < arbres_before or souches_after < souches_before:
            damaged_parcels += 1

        if arbres_after == 0 and souches_after == 0:
            _handle_route_creation(state, ray, target_p)

    # 3. Avancée éventuelle (T3 / T6) si machine toujours en jeu et hors Siège
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    if not aborted_by_jaguar and cur_st == MACHINE_STATUS_NORMAL and cur_pos > 0 and tactique.avancee > 0:
        for _ in range(tactique.avancee):
            cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
            if cur_st != MACHINE_STATUS_NORMAL or cur_pos == 0:
                break
            p_next = state.next_non_razed_towards_heart(ray, cur_pos)
            if p_next is not None:
                prim_deplacement(
                    state,
                    "MACHINE",
                    src_ray=ray,
                    m_type=m_type,
                    dst_ray=ray,
                    dst_p=p_next,
                )
            else:
                if state.cfg.declenchement_fin_de_piste == "DEPASSEMENT_DERNIERE_PARCELLE":
                    state.set_machine_pos_status(ray, m_type, cur_pos, cur_st, True)

    # 4. Gain éventuel de jeton Puissance rouge (T4 / T5 / T6 / Siège)
    cur_pos, cur_st, _ = state.get_machine_pos_status(ray, m_type)
    gained_red = False
    if cur_st != MACHINE_STATUS_RETIRED and cur_pos > 0 and tactique.gain_rouge > 0:
        r_tok, b_tok = state.get_machine_tokens(ray, m_type)
        if r_tok < 15:
            state.set_machine_tokens(ray, m_type, r_tok + tactique.gain_rouge, b_tok)
            gained_red = True

    state.set_machine_turn_stats(ray, m_type, damaged_parcels, gained_red, True)

    # 5. Fin du bloc machine -> balayage à plat des Gardiens 1 -> 6
    sweep_gardiens(state)


# ---------------------------------------------------------------------------
# Étape 5.3 : Repousse Finale & calcul GameOver
# ---------------------------------------------------------------------------


def apply_repousse_finale(state: GameState) -> GameOver:
    """Applique la Repousse Finale (+1 Arbre par parcelle non rasée ayant >= 1 Souche,
    plafonné à la dotation initiale) et retourne l'objet GameOver.
    """
    cause = CAUSE_TOUR_8
    if state.cfg.mode >= 2 and is_reve_code(state.get_tactique_at_rank(0)):
        cause = CAUSE_REVE_RANG_1
    elif (
        state.cfg.mode >= 2
        and state.seuil_reveil >= 3
        and state.count_used_gardiens_on_track() >= state.seuil_reveil
    ):
        cause = CAUSE_REVEIL_GARDIENS

    for r in range(state.cfg.n_players):
        for p in range(1, state.cfg.p_max + 1):
            if state.is_route_forestiere(r, p):
                continue
            souches = state.get_parcel_souches(r, p)
            if souches >= 1:
                rep_ctx: dict[str, Any] = {"ray": r, "p": p, "max_repousse": 1}
                dispatch_hook(state, HOOK_REPOUSSE_FINALE, rep_ctx)
                prim_creation_entite(
                    state,
                    "ARBRE",
                    ray=r,
                    p=p,
                    count=int(rep_ctx["max_repousse"]),
                    light_trigger=False,
                )

    score = state.total_arbres_plateau()
    init_total = state.cfg.n_players * sum(state.cfg.dotation_arbres)
    ratio = score / init_total if init_total > 0 else 0.0
    state.step = STEP_GAME_OVER
    return GameOver(
        tour_fin=state.tour,
        cause_fin=cause,
        score_arbres=score,
        ratio_arbres=ratio,
    )


def _check_end_of_game_condition(state: GameState) -> bool:
    if state.cfg.mode >= 2:
        if is_reve_code(state.get_tactique_at_rank(0)):
            return True
        if state.seuil_reveil >= 3 and state.count_used_gardiens_on_track() >= state.seuil_reveil:
            return True
    return state.tour >= 8


# ---------------------------------------------------------------------------
# Helpers internes pour Migration 4.3, Siège 1.1/6.3 et files d'attente
# ---------------------------------------------------------------------------


def _transition_eligible_machines_to_siege(state: GameState, *, remove_from_deck: bool) -> None:
    for r in range(state.cfg.n_players):
        last_p = state.last_non_razed_parcel(r)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, pending_s = state.get_machine_pos_status(r, mt)
            if st != MACHINE_STATUS_NORMAL or pos == 0:
                continue
            should_siege = pending_s or (
                state.cfg.declenchement_fin_de_piste == "ARRIVEE_DERNIERE_PARCELLE"
                and last_p is not None
                and pos == last_p
            )
            if should_siege:
                state.set_machine_pos_status(r, mt, pos, MACHINE_STATUS_SIEGE, False)
                if remove_from_deck:
                    state.remove_machine_card_from_deck_if_present(machine_card_code(r, mt))


def _list_insect_1cran_moves(
    state: GameState, src: tuple[str, int, int]
) -> tuple[tuple[Any, ...], ...]:
    """Options de migration à 0 ou 1 cran pour un Insecte situé sur `src`."""
    n = state.cfg.n_players
    loc_type, idx_a, p = src
    opts: list[tuple[Any, ...]] = [("RESTER",)]

    if loc_type == "FORET":
        r = idx_a
        if state.is_route_forestiere(r, p) or state.get_parcel_insectes(r, p) == 0:
            return (("RESTER",),)

        # Radial vers le cœur / vers la bordure (sautant les Routes Forestières)
        p_fwd = state.next_non_razed_towards_heart(r, p)
        if p_fwd is not None:
            opts.append(("FORET", r, p_fwd))
        p_back = state.next_non_razed_towards_border(r, p)
        if p_back is not None:
            opts.append(("FORET", r, p_back))

        # Latéral vers les 2 cases Furtivité bordant ce rayon à même profondeur p
        right_l = r
        left_l = (r - 1) % n
        for l_adj in (right_l, left_l):
            if state.get_furtivite_insectes(l_adj, p) < 15:
                cand = ("FURTIVITE", l_adj, p)
                if cand not in opts:
                    opts.append(cand)

        # Aller simple vers Bug / Colonie depuis la dernière parcelle non rasée (Mode 2+)
        if state.cfg.mode >= 2 and p == state.last_non_razed_parcel(r):
            for c in range(1, TRACK_LEN + 1):
                opts.append(("BUG", c))
            for c in range(1, TRACK_LEN + 1):
                opts.append(("COLONIE", c))

    else:
        l_idx = idx_a
        if state.get_furtivite_insectes(l_idx, p) == 0:
            return (("RESTER",),)
        for rive in (0, 1):
            adj_ray = state.lisiere_ray_for_rive(l_idx, rive)
            if not state.is_route_forestiere(adj_ray, p):
                cand_f = ("FORET", adj_ray, p)
                if cand_f not in opts:
                    opts.append(cand_f)

    return tuple(opts)


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
        # Contrainte stricte : Abatteuse avant Bulldozer sur un même rayon
        if MACHINE_ABATTEUSE in mts:
            eligible.append((r, MACHINE_ABATTEUSE))
        else:
            eligible.append((r, MACHINE_BULLDOZER))
    return eligible


def _eligible_siege_machines(state: GameState) -> list[tuple[int, int]]:
    eligible: list[tuple[int, int]] = []
    for offset in range(state.cfg.n_players):
        r = (state.coordonnateur + offset) % state.cfg.n_players
        ab_pos, ab_st, _ = state.get_machine_pos_status(r, MACHINE_ABATTEUSE)
        _, _, ab_att = state.get_machine_turn_stats(r, MACHINE_ABATTEUSE)
        bu_pos, bu_st, _ = state.get_machine_pos_status(r, MACHINE_BULLDOZER)
        _, _, bu_att = state.get_machine_turn_stats(r, MACHINE_BULLDOZER)

        if ab_st == MACHINE_STATUS_SIEGE and ab_pos > 0 and not ab_att:
            eligible.append((r, MACHINE_ABATTEUSE))
        elif bu_st == MACHINE_STATUS_SIEGE and bu_pos > 0 and not bu_att:
            eligible.append((r, MACHINE_BULLDOZER))
    return eligible


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
            state.step = STEP_3_1_CONSTRUCT
        else:
            state.set_step2_pass_state(pass_idx + 1, False)
            state._continuation.append(("STEP2_REV_QUEUE", rem_seats, 0))
        return None

    if tag == "CONSTRUCT_SLOT":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        return _begin_single_construction(state, slot_idx)

    if tag == "CHECK_LIBERATION_3_1":
        slot_idx = int(top[1])
        state._continuation.pop(0)
        lib_opts = _liberation_options_n3(state, slot_idx)
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
            state.step = STEP_5_1_TACTIQUES
        return None

    if tag == "COLONIE_SCAN_4_3":
        next_case = int(top[1])
        state._continuation.pop(0)
        hook_res = dispatch_hook(state, HOOK_4_3_COLONIE_FIN, {"start_case": next_case})
        eligible_cases: list[int] = hook_res[0] if hook_res else []
        if not eligible_cases:
            state.step = STEP_5_1_TACTIQUES
            return None
        c_num = eligible_cases[0]
        g_num, _, _ = state.get_gardien_at_case(c_num)
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
            state.step = STEP_5_2_SIEGES
            return None
        code = state.get_tactique_at_rank(r_idx)
        if not is_tactique_code(code):
            state._continuation[0] = ("TACTIQUE_RANK_5_1", r_idx + 1)
            return None
        eligible_m = _eligible_tactique_machines_at_rank(state, code)
        if not eligible_m:
            state._continuation[0] = ("TACTIQUE_RANK_5_1", r_idx + 1)
            return None
        if len(eligible_m) == 1:
            rm, mt = eligible_m[0]
            resolve_single_machine_attack(state, rm, mt, TACTIQUES_SPEC[code])
            return None
        req = DecisionRequest(
            decideur=state.coordonnateur,
            decision_type=DEC_ORDRE_ATTAQUE_5_1,
            options=tuple(eligible_m),
            context={"rank": r_idx + 1, "tactique": code_to_tile_id(code)},
        )
        state._continuation.insert(0, ("APPLY_TACTIQUE_5_1", code))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if tag == "VOLUNTARY_APP_6_1":
        state._continuation.pop(0)
        rem_cnt, dec_seat = state.get_pending_voluntary_app_reduction()
        ranks_pos = tuple(
            idx
            for idx in range(TRACK_LEN)
            if is_tactique_code(state.get_tactique_at_rank(idx))
            and state.get_apprentissage_at_rank(idx) > 0
        )
        if rem_cnt > 0 and ranks_pos:
            req = DecisionRequest(
                decideur=dec_seat if 0 <= dec_seat < n else state.coordonnateur,
                decision_type=DEC_RETRAIT_APPRENTISSAGE_6_1,
                options=("PASSER", *ranks_pos),
                context={"remaining": rem_cnt, "tour": state.tour},
            )
            state._continuation.insert(0, ("APPLY_VOLUNTARY_APP_6_1",))
            state._continuation.insert(0, ("WAIT_DECISION", req))
            return req
        state.clear_pending_voluntary_app_reduction(0, 0)
        dispatch_hook(state, HOOK_6_1_BUG, {})
        state.step = STEP_6_2_EVOLUTION
        return None

    raise RuntimeError(f"Continuation inconnue : {tag}")


def _run_step_3_2(state: GameState) -> None:
    n = state.cfg.n_players
    prim_partage_info_etat_gardien(state, "OPEN_PARAVENTS")
    dispatch_hook(state, HOOK_3_2_REVELATION, {})

    initial_track = [state.get_tactique_at_rank(i) for i in range(TRACK_LEN)]
    reve_hits_by_rank: list[int] = [0] * TRACK_LEN
    for s in range(n):
        card, d1, d2, lec_m, _ = state.get_player_hand(s)
        if 1 <= card <= 12 and 1 <= lec_m <= 6:
            code_m = initial_track[lec_m - 1]
            if is_tactique_code(code_m):
                state.set_player_hand(s, card, d1, d2, lec_m, code_m)
            elif is_reve_code(code_m):
                state.set_player_hand(s, card, d1, d2, lec_m, 0)
                reve_hits_by_rank[lec_m - 1] += 1

    for r_idx in range(TRACK_LEN):
        hits = reve_hits_by_rank[r_idx]
        if hits <= 0:
            continue
        reve_code = initial_track[r_idx]
        r_num = reve_code - TILE_R_BASE
        if state.cfg.regle_ouverture_reve_multiple == "UNIQUE_PAR_TOUR":
            open_count = 0 if state.has_reve_opened_this_turn(r_num) else 1
        else:
            open_count = hits

        for _ in range(open_count):
            state.mark_reve_opened_this_turn(r_num)
            state.light_trigger(5)
            dispatch_hook(state, HOOK_3_2_OUVERTURE_REVE, {"slot_id": f"R{r_num}", "r_num": r_num})
            cur_pos_r = state.find_tactique_rank(reve_code)
            if cur_pos_r is not None and cur_pos_r > 0:
                prim_permutation_piste(state, "ADVANCE_REVE_LEFT", rank_a=cur_pos_r)
            sweep_gardiens(state)

    state.step = STEP_4_1_FURTIVITE


def _run_step_4_1(state: GameState) -> None:
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    for off in range(n):
        l_idx = (state.coordonnateur + off) % n
        for p in range(1, p_max + 1):
            d0 = state.get_furtivite_nb_def_rive(l_idx, p, 0)
            d1 = state.get_furtivite_nb_def_rive(l_idx, p, 1)
            ins = state.get_furtivite_insectes(l_idx, p)

            rive: int | None = None
            use_ins = False
            if d0 == 2:
                rive = 0
            elif d1 == 2:
                rive = 1
            elif d0 == 1 and d1 == 0 and ins >= 1:
                rive = 0
                use_ins = True
            elif d1 == 1 and d0 == 0 and ins >= 1:
                rive = 1
                use_ins = True

            if rive is None:
                continue

            t_ray = state.lisiere_ray_for_rive(l_idx, rive)
            if state.is_route_forestiere(t_ray, p):
                continue

            dispatch_hook(state, HOOK_4_1_FURTIVITE, {"lisiere": l_idx, "p": p, "rive": rive})
            present_m = state.machines_on_parcel(t_ray, p)
            if not present_m:
                if state.get_parcel_piege(t_ray, p) == PIEGE_AUCUN:
                    if use_ins:
                        state.set_furtivite_insectes(l_idx, p, ins - 1)
                    prim_creation_entite(state, "PIEGE", ray=t_ray, p=p, light_trigger=True)
                    sweep_gardiens(state)
            else:
                if not any(is_machine_active_this_turn(state, t_ray, mt) for mt in present_m):
                    if use_ins:
                        state.set_furtivite_insectes(l_idx, p, ins - 1)
                    prim_creation_entite(state, "SABOTAGE", count=1, light_trigger=True)
                    sweep_gardiens(state)

    state.step = STEP_4_2_NIDS


def _run_step_6_1(state: GameState) -> None:
    n = state.cfg.n_players
    card_tactique_by_machine: dict[tuple[int, int], int] = {}
    for s in range(n):
        card, _, _, _, bound_t = state.get_player_hand(s)
        if 1 <= card <= 12 and bound_t > 0:
            card_tactique_by_machine[((card - 1) // 2, (card - 1) % 2)] = bound_t

    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            pos, st, _ = state.get_machine_pos_status(r, mt)
            if st == MACHINE_STATUS_RETIRED or pos == 0:
                continue
            target_t_code: int | None = None
            if st == MACHINE_STATUS_SIEGE:
                target_t_code = 4
            elif (r, mt) in card_tactique_by_machine:
                target_t_code = card_tactique_by_machine[(r, mt)]

            if target_t_code is None:
                continue
            t_rank = state.find_tactique_rank(target_t_code)
            if t_rank is None:
                continue

            dmg_cnt, gained_red, _ = state.get_machine_turn_stats(r, mt)
            _, bleus = state.get_machine_tokens(r, mt)
            gain = max(0, dmg_cnt + (1 if gained_red else 0) - bleus)
            if gain > 0:
                prim_mod_apprentissage(state, t_rank, gain)

    for r_idx in range(TRACK_LEN):
        pend_delta = state.get_pending_apprentissage_at_rank(r_idx)
        if pend_delta != 0 and is_tactique_code(state.get_tactique_at_rank(r_idx)):
            prim_mod_apprentissage(state, r_idx, pend_delta)
            state.add_pending_apprentissage_at_rank(r_idx, -pend_delta)

    dispatch_hook(state, HOOK_6_1_REDUCTION_VOLONTAIRE, {})
    rem_vol, _ = state.get_pending_voluntary_app_reduction()
    if rem_vol > 0:
        state._continuation.append(("VOLUNTARY_APP_6_1",))
        return

    dispatch_hook(state, HOOK_6_1_BUG, {})
    state.step = STEP_6_2_EVOLUTION


def _run_step_6_2(state: GameState) -> GameOver | None:
    scores = [
        state.get_apprentissage_at_rank(i)
        if is_tactique_code(state.get_tactique_at_rank(i))
        else 0
        for i in range(TRACK_LEN)
    ]
    max_sc = max(scores)
    if max_sc >= 1 and scores.count(max_sc) == 1:
        win_idx = scores.index(max_sc)
        av_ctx: dict[str, Any] = {"winner_idx": win_idx, "blocked": False}
        dispatch_hook(state, HOOK_6_2_AVANCEMENT, av_ctx)
        if not av_ctx.get("blocked") and win_idx > 0:
            prim_permutation_piste(state, "SWAP_RANKS", rank_a=win_idx, rank_b=win_idx - 1)
    else:
        dispatch_hook(state, HOOK_6_2_AVANCEMENT, {"winner_idx": None, "tie": True})

    if state.cfg.mode >= 3 and is_reve_code(state.get_tactique_at_rank(0)):
        return apply_repousse_finale(state)

    state.cleanup_end_of_turn_6_2()
    state.step = STEP_6_3_END_TURN
    return None


def _advance_main_step(state: GameState) -> DecisionRequest | GameOver | None:
    """Exécute un pas de l'étape principale state.step."""
    n = state.cfg.n_players
    p_max = state.cfg.p_max
    step = state.step

    if step == STEP_GAME_OVER:
        return apply_repousse_finale(state)

    if step == STEP_1_1_SIEGE:
        _transition_eligible_machines_to_siege(state, remove_from_deck=True)
        state.step = STEP_1_2_DEAL
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
        for off in range(n):
            s = (start_seat + off) % n
            state.set_player_hand(s, state.draw_next_machine_card(), 0, 0, 0, 0)
        state.step = STEP_1_3_DICE
        return None

    if step == STEP_1_3_DICE:
        for s in range(n):
            card, _, _, _, _ = state.get_player_hand(s)
            if 1 <= card <= 12:
                peuple_id = PEUPLE_TO_ID[state.cfg.peuples[s]]
                d1 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 0)
                d2 = roll_d6(state.cfg.exp_seed, state.cfg.rep_id, SRC_DICE, state.tour, peuple_id, 1)
                state.set_player_hand(s, card, d1, d2, min(d1, d2), 0)
                dispatch_hook(state, HOOK_1_3_LECTURE_DE, {"seat": s})
            else:
                state.set_player_hand(s, card, 0, 0, 0, 0)
        state.step = STEP_2_1_DEF1
        dispatch_hook(state, HOOK_2_1_DEBUT, {})
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
        state.step = STEP_2_2_DEF2
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
            state.step = STEP_3_1_CONSTRUCT
            return None

        refl_seats = tuple(
            (state.coordonnateur + off) % n
            for off in range(n)
            if state.get_player_def_loc_raw((state.coordonnateur + off) % n, 1) != 0
            and not state.is_player_def2_definitif((state.coordonnateur + off) % n)
        )
        if not refl_seats:
            lock_all_def2_in_place(state)
            state.step = STEP_3_1_CONSTRUCT
        else:
            state.set_step2_pass_state(1, False)
            state._continuation.append(("STEP2_REV_QUEUE", refl_seats, 0))
        return None

    if step == STEP_3_1_CONSTRUCT:
        if state.cfg.mode == 1:
            state.step = STEP_3_2_REVEAL
            return None
        ready_slots = [
            (state.coordonnateur * 2 + off) % (2 * n)
            for off in range(2 * n)
            if state.get_lisiere_tile_state((state.coordonnateur * 2 + off) % (2 * n))
            == (LISIERE_UNCONSTRUCTED, 2)
        ]
        if not ready_slots:
            state.step = STEP_3_2_REVEAL
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
        _run_step_4_1(state)
        return None

    if step == STEP_4_2_NIDS:
        if state.cfg.mode == 1:
            state.step = STEP_4_3_MIGRATION
            return None
        eligible_nids: list[int] = []
        for m_num in range(1, 6):
            pos_info = state.get_nid_position(m_num)
            if pos_info is not None:
                r, p, active_turn = pos_info
                if not active_turn and state.get_parcel_defenseurs(r, p) >= 1:
                    eligible_nids.append(m_num)
        if not eligible_nids:
            state.step = STEP_4_3_MIGRATION
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
            state.step = STEP_5_1_TACTIQUES
        return None

    if step == STEP_5_1_TACTIQUES:
        state._continuation.append(("TACTIQUE_RANK_5_1", 0))
        return None

    if step == STEP_5_2_SIEGES:
        eligible_s = _eligible_siege_machines(state)
        if not eligible_s:
            state.step = STEP_5_3_END_CHECK
            return None
        if len(eligible_s) == 1:
            rm, mt = eligible_s[0]
            resolve_single_machine_attack(state, rm, mt, TACTIQUES_SPEC[4], is_siege=True)
            return None
        req = DecisionRequest(
            state.coordonnateur, DEC_ORDRE_SIEGE_5_2, tuple(eligible_s), {"tour": state.tour}
        )
        state._continuation.append(("APPLY_SIEGE_5_2",))
        state._continuation.insert(0, ("WAIT_DECISION", req))
        return req

    if step == STEP_5_3_END_CHECK:
        dispatch_hook(state, HOOK_5_3_PRE_RETRAIT, {})
        for r in range(n):
            for p in range(1, p_max + 1):
                if state.get_parcel_piege(r, p) == PIEGE_DECLENCHE:
                    state.set_parcel_piege(r, p, PIEGE_AUCUN)
        if _check_end_of_game_condition(state):
            return apply_repousse_finale(state)
        state.step = STEP_6_1_APPRENTISSAGE
        return None

    if step == STEP_6_1_APPRENTISSAGE:
        _run_step_6_1(state)
        return None

    if step == STEP_6_2_EVOLUTION:
        return _run_step_6_2(state)

    if step == STEP_6_3_END_TURN:
        _transition_eligible_machines_to_siege(state, remove_from_deck=False)
        state.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
        state.coordonnateur = (state.coordonnateur + 1) % n
        state.tour += 1
        state.step = STEP_1_1_SIEGE
        return None

    raise RuntimeError(f"Étape moteur inconnue : {step}")


def step_until_decision(state: GameState, *, max_internal_steps: int = 2000) -> DecisionRequest | GameOver:
    """Avance la machine à états jusqu'à la prochaine DecisionRequest ou jusqu'à GameOver."""
    ensure_builtin_migration_registered()
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


def _begin_single_construction(state: GameState, slot_idx: int) -> DecisionRequest | None:
    """Construit la tuile en lisière `slot_idx` (suspend si un choix de gouverneur est requis)."""
    st, nb = state.get_lisiere_tile_state(slot_idx)
    if st != LISIERE_UNCONSTRUCTED or nb < 2:
        return None

    tile_id = state.cfg.lisiere_slots[slot_idx]
    fam, orig_code, num = SYNERGY_META[tile_id]
    gov = _governor_for_peuple(state, orig_code)
    dispatch_hook(state, HOOK_3_1_CONSTRUCTION, {"slot_id": tile_id, "slot_idx": slot_idx})

    if fam == FAMILLE_GARDIEN:
        free_cases = tuple(
            c for c in range(1, TRACK_LEN + 1) if state.get_gardien_at_case(c)[0] == 0
        )
        state._continuation.insert(0, ("CHECK_LIBERATION_3_1", slot_idx))
        if not free_cases:
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
            return None
        if len(free_cases) == 1:
            state.set_gardien_at_case(free_cases[0], num, 1, False)
            state.set_lisiere_tile_state(slot_idx, LISIERE_CONSTRUCTED, nb)
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
        # Cas dégénéré où aucune parcelle des 2 rayons n'est libre : tuile marquée sans boucle
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
    prim_creation_entite(state, "INSECTE", ray=r, p=p, count=created, light_trigger=True)
    dispatch_hook(
        state,
        HOOK_4_2_NID_APRES_PROD,
        {"slot_id": f"M{m_num}", "m_num": m_num, "ray": r, "p": p},
    )
    sweep_gardiens(state)


def apply_choice(state: GameState, choice: Any) -> None:
    """Applique le choix légal répondant à la DecisionRequest courante."""
    assert state._continuation and state._continuation[0][0] == "WAIT_DECISION", (
        "Aucune DecisionRequest en attente"
    )
    _, req = state._continuation.pop(0)
    assert choice in req.options, f"Choix illégal {choice!r} hors de {req.options!r}"

    assert state._continuation, "Continuation manquante après WAIT_DECISION"
    top = state._continuation[0]
    tag = top[0]

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
        state._continuation.insert(0, ("CONSTRUCT_SLOT", int(choice)))
        return

    if tag == "APPLY_GARDIEN_CASE_3_1":
        _, slot_idx, g_num = state._continuation.pop(0)
        _, nb = state.get_lisiere_tile_state(int(slot_idx))
        state.set_gardien_at_case(int(choice), int(g_num), 1, False)
        state.set_lisiere_tile_state(int(slot_idx), LISIERE_CONSTRUCTED, nb)
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
        _resolve_nid_block(state, int(choice))
        return

    if tag == "APPLY_MIGRATION_4_3":
        _, src = state._continuation.pop(0)
        loc_type, idx_a, src_p = src
        dst_kind = choice[0]
        if dst_kind != "RESTER":
            src_kwargs: dict[str, Any] = (
                {"src_lisiere": idx_a, "src_p": src_p}
                if loc_type == "FURTIVITE"
                else {"src_ray": idx_a, "src_p": src_p}
            )
            if dst_kind == "FORET":
                prim_deplacement(
                    state, "INSECTE", dst_ray=int(choice[1]), dst_p=int(choice[2]), **src_kwargs
                )
            elif dst_kind == "FURTIVITE":
                prim_deplacement(
                    state,
                    "INSECTE",
                    dst_lisiere=int(choice[1]),
                    dst_p=int(choice[2]),
                    **src_kwargs,
                )
            elif dst_kind in ("BUG", "COLONIE"):
                prim_deplacement(
                    state,
                    "INSECTE",
                    global_track=dst_kind,
                    global_case=int(choice[1]),
                    **src_kwargs,
                )
        assert state._continuation and state._continuation[0][0] == "MIGRATION_QUEUE_4_3"
        _, q_tup, cur = state._continuation[0]
        state._continuation[0] = ("MIGRATION_QUEUE_4_3", q_tup, cur + 1)
        return

    if tag == "APPLY_COLONIE_4_3":
        _, c_num = state._continuation.pop(0)
        case_int = int(c_num)
        if choice == "OUVRIR":
            cur_col = state.get_colonie_at_case(case_int)
            assert cur_col >= 1
            state.set_colonie_at_case(case_int, cur_col - 1)
            prim_partage_info_etat_gardien(state, "MARK_GARDIEN_OPENED", case_1_6=case_int)
            sweep_gardiens(state)
        state._continuation.insert(0, ("COLONIE_SCAN_4_3", case_int + 1))
        return

    if tag == "APPLY_TACTIQUE_5_1":
        _, t_code = state._continuation.pop(0)
        rm, mt = choice
        resolve_single_machine_attack(state, int(rm), int(mt), TACTIQUES_SPEC[int(t_code)])
        return

    if tag == "APPLY_SIEGE_5_2":
        state._continuation.pop(0)
        rm, mt = choice
        resolve_single_machine_attack(state, int(rm), int(mt), TACTIQUES_SPEC[4], is_siege=True)
        return

    if tag == "APPLY_VOLUNTARY_APP_6_1":
        state._continuation.pop(0)
        rem_cnt, dec_seat = state.get_pending_voluntary_app_reduction()
        if choice == "PASSER":
            state.clear_pending_voluntary_app_reduction(0, 0)
        else:
            prim_mod_apprentissage(state, int(choice), -1)
            state.clear_pending_voluntary_app_reduction(max(0, rem_cnt - 1), dec_seat)
        state._continuation.insert(0, ("VOLUNTARY_APP_6_1",))
        return

    raise RuntimeError(f"Tag de continuation inconnu : {tag}")
