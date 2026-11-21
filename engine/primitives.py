"""Bus des 8 Primitives Formelles, structures de décision/fin et registre de hooks."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, NamedTuple

from engine.state import (
    FACE_DEFINITIF,
    FAMILLE_CROISSANCE,
    FAMILLE_GARDIEN,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_STATUS_RETIRED,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    SYNERGY_META,
    TRACK_LEN,
    GameState,
    is_reve_code,
)

__all__ = (
    "ALL_PRIMITIVES",
    "CAUSE_REVEIL_GARDIENS",
    "CAUSE_REVE_RANG_1",
    "CAUSE_TOUR_8",
    "DEC_EFFET_TUILE",
    "HOOK_1_3_LECTURE_DE",
    "HOOK_2_1_DEBUT",
    "HOOK_2_1_PORTEE_DEF1",
    "HOOK_3_1_CONSTRUCTION",
    "HOOK_3_2_APRES_REVELATION",
    "HOOK_3_2_OUVERTURE_REVE",
    "HOOK_3_2_REVELATION",
    "HOOK_4_1_FURTIVITE",
    "HOOK_4_2_NID_APRES_PROD",
    "HOOK_4_3_COLONIE_FIN",
    "HOOK_4_3_MIGRATION_DESTS",
    "HOOK_5_3_PRE_RETRAIT",
    "HOOK_5_APRES_PARADE_PIEGE",
    "HOOK_5_CIBLAGE_MACHINE",
    "HOOK_5_CONTACT_NID",
    "HOOK_5_DEBUT",
    "HOOK_5_DEFENSE_PARCELLE",
    "HOOK_5_FIN_ATTAQUE_MACHINE",
    "HOOK_5_LAW_QUERY",
    "HOOK_5_ORDRE_RAYON",
    "HOOK_5_PARADE_CLASSIQUE",
    "HOOK_5_PARADE_HARPIE",
    "HOOK_5_PARADE_JAGUAR",
    "HOOK_5_SEUIL_PARADE",
    "HOOK_5_TERRASSEMENT",
    "HOOK_6_1_BUG",
    "HOOK_6_1_REDUCTION_VOLONTAIRE",
    "HOOK_6_2_AVANCEMENT",
    "HOOK_EFFECT_RESUME",
    "HOOK_GARDIEN_OUVERTURE",
    "HOOK_REPOUSSE_FINALE",
    "PRIM_CREATION_ENTITE",
    "PRIM_DEPLACEMENT",
    "PRIM_MOD_APPRENTISSAGE",
    "PRIM_MOD_LOI_DU_COEUR",
    "PRIM_MOD_PUISSANCE",
    "PRIM_MOD_SEUIL",
    "PRIM_PARTAGE_INFO_ETAT_GARDIEN",
    "PRIM_PERMUTATION_PISTE",
    "DecisionRequest",
    "EffectHandler",
    "GameOver",
    "TileRegistration",
    "apply_machine_nid_contact",
    "clear_tile_registry",
    "dispatch_hook",
    "get_tile_registration",
    "has_pending_decision",
    "list_registered_tiles",
    "prim_creation_entite",
    "prim_deplacement",
    "prim_mod_apprentissage",
    "prim_mod_loi_du_coeur",
    "prim_mod_puissance",
    "prim_mod_seuil",
    "prim_partage_info_etat_gardien",
    "prim_permutation_piste",
    "push_effect_decision",
    "register_tile",
)

# Causes canoniques de fin de partie
CAUSE_TOUR_8: str = "TOUR_8_ATTEINT"
CAUSE_REVE_RANG_1: str = "REVE_RANG_1"
CAUSE_REVEIL_GARDIENS: str = "REVEIL_GARDIENS"

# Type canonique de décision émise par un effet de tuile
DEC_EFFET_TUILE: str = "EFFET_TUILE"

# Les 8 Primitives Formelles v5.3
PRIM_MOD_SEUIL: str = "MOD_SEUIL"
PRIM_CREATION_ENTITE: str = "CREATION_ENTITE"
PRIM_DEPLACEMENT: str = "DEPLACEMENT"
PRIM_MOD_PUISSANCE: str = "MOD_PUISSANCE"
PRIM_MOD_APPRENTISSAGE: str = "MOD_APPRENTISSAGE"
PRIM_PERMUTATION_PISTE: str = "PERMUTATION_PISTE"
PRIM_PARTAGE_INFO_ETAT_GARDIEN: str = "PARTAGE_INFO_ETAT_GARDIEN"
PRIM_MOD_LOI_DU_COEUR: str = "MOD_LOI_DU_COEUR"

ALL_PRIMITIVES: tuple[str, ...] = (
    PRIM_MOD_SEUIL,
    PRIM_CREATION_ENTITE,
    PRIM_DEPLACEMENT,
    PRIM_MOD_PUISSANCE,
    PRIM_MOD_APPRENTISSAGE,
    PRIM_PERMUTATION_PISTE,
    PRIM_PARTAGE_INFO_ETAT_GARDIEN,
    PRIM_MOD_LOI_DU_COEUR,
)

# Fenêtres / Hooks du bus d'exécution
HOOK_1_3_LECTURE_DE: str = "HOOK_1_3_LECTURE_DE"
HOOK_2_1_DEBUT: str = "HOOK_2_1_DEBUT"
HOOK_2_1_PORTEE_DEF1: str = "HOOK_2_1_PORTEE_DEF1"
HOOK_3_1_CONSTRUCTION: str = "HOOK_3_1_CONSTRUCTION"
HOOK_3_2_REVELATION: str = "HOOK_3_2_REVELATION"
HOOK_3_2_OUVERTURE_REVE: str = "HOOK_3_2_OUVERTURE_REVE"
HOOK_3_2_APRES_REVELATION: str = "HOOK_3_2_APRES_REVELATION"
HOOK_GARDIEN_OUVERTURE: str = "HOOK_GARDIEN_OUVERTURE"
HOOK_4_1_FURTIVITE: str = "HOOK_4_1_FURTIVITE"
HOOK_4_2_NID_APRES_PROD: str = "HOOK_4_2_NID_APRES_PROD"
HOOK_4_3_COLONIE_FIN: str = "HOOK_4_3_COLONIE_FIN"
HOOK_4_3_MIGRATION_DESTS: str = "HOOK_4_3_MIGRATION_DESTS"
HOOK_5_DEBUT: str = "HOOK_5_DEBUT"
HOOK_5_ORDRE_RAYON: str = "HOOK_5_ORDRE_RAYON"
HOOK_5_CIBLAGE_MACHINE: str = "HOOK_5_CIBLAGE_MACHINE"
HOOK_5_LAW_QUERY: str = "HOOK_5_LAW_QUERY"
HOOK_5_PARADE_JAGUAR: str = "HOOK_5_PARADE_JAGUAR"
HOOK_5_PARADE_HARPIE: str = "HOOK_5_PARADE_HARPIE"
HOOK_5_SEUIL_PARADE: str = "HOOK_5_SEUIL_PARADE"
HOOK_5_DEFENSE_PARCELLE: str = "HOOK_5_DEFENSE_PARCELLE"
HOOK_5_APRES_PARADE_PIEGE: str = "HOOK_5_APRES_PARADE_PIEGE"
HOOK_5_PARADE_CLASSIQUE: str = "HOOK_5_PARADE_CLASSIQUE"
HOOK_5_TERRASSEMENT: str = "HOOK_5_TERRASSEMENT"
HOOK_5_CONTACT_NID: str = "HOOK_5_CONTACT_NID"
HOOK_5_FIN_ATTAQUE_MACHINE: str = "HOOK_5_FIN_ATTAQUE_MACHINE"
HOOK_5_3_PRE_RETRAIT: str = "HOOK_5_3_PRE_RETRAIT"
HOOK_6_1_REDUCTION_VOLONTAIRE: str = "HOOK_6_1_REDUCTION_VOLONTAIRE"
HOOK_6_1_BUG: str = "HOOK_6_1_BUG"
HOOK_6_2_AVANCEMENT: str = "HOOK_6_2_AVANCEMENT"
HOOK_REPOUSSE_FINALE: str = "HOOK_REPOUSSE_FINALE"
HOOK_EFFECT_RESUME: str = "HOOK_EFFECT_RESUME"


class _TelemetryCtx:
    """Point d'accroche interne à coût zéro quand aucun TelemetryTracker n'est actif."""

    active: ClassVar[Any | None] = None


def _set_active_telemetry(tracker: Any | None) -> Any | None:
    prev = _TelemetryCtx.active
    _TelemetryCtx.active = tracker
    return prev


def _get_active_telemetry() -> Any | None:
    return _TelemetryCtx.active


def _record_phys_ops(state: GameState, count: int) -> None:
    trk = _TelemetryCtx.active
    if trk is not None and count > 0:
        trk.record_physical_ops(state, count)


class DecisionRequest(NamedTuple):
    """Suspension déterministe de la machine à états demandant un choix légal à un siège."""

    decideur: int
    decision_type: str
    options: tuple[Any, ...]
    context: dict[str, Any]


class GameOver(NamedTuple):
    """Résultat final d'une partie après Repousse Finale."""

    tour_fin: int
    cause_fin: str
    score_arbres: int
    ratio_arbres: float


EffectHandler = Callable[[GameState, str, dict[str, Any]], Any]


@dataclass(frozen=True, slots=True)
class TileRegistration:
    slot_id: str
    profile: str
    hooks: tuple[str, ...]
    handler: EffectHandler


class _RegistryStore:
    """Stockage interne des profils stateless enregistrés via @register_tile."""

    by_key: ClassVar[dict[tuple[str, str], TileRegistration]] = {}
    by_hook: ClassVar[dict[str, list[TileRegistration]]] = {}


def register_tile(
    slot_id: str,
    profile: str,
    hooks: Sequence[str] = (),
) -> Callable[[EffectHandler], EffectHandler]:
    """Décorateur d'enregistrement d'un profil stateless (slot_id, profile)."""
    hooks_tuple = tuple(hooks)

    def _decorator(fn: EffectHandler) -> EffectHandler:
        reg = TileRegistration(
            slot_id=slot_id,
            profile=profile,
            hooks=hooks_tuple,
            handler=fn,
        )
        key = (slot_id, profile)
        old = _RegistryStore.by_key.get(key)
        if old is not None:
            for h in old.hooks:
                lst = _RegistryStore.by_hook.get(h, [])
                _RegistryStore.by_hook[h] = [r for r in lst if (r.slot_id, r.profile) != key]
        _RegistryStore.by_key[key] = reg
        for h in hooks_tuple:
            _RegistryStore.by_hook.setdefault(h, []).append(reg)
        return fn

    return _decorator


def get_tile_registration(slot_id: str, profile: str) -> TileRegistration | None:
    return _RegistryStore.by_key.get((slot_id, profile))


def list_registered_tiles() -> tuple[tuple[str, str], ...]:
    return tuple(sorted(_RegistryStore.by_key.keys()))


def clear_tile_registry() -> None:
    _RegistryStore.by_key.clear()
    _RegistryStore.by_hook.clear()


def has_pending_decision(state: GameState) -> bool:
    """Retourne True si une DecisionRequest est déjà en tête de la pile de continuation."""
    return bool(state._continuation and state._continuation[0][0] == "WAIT_DECISION")


def push_effect_decision(
    state: GameState,
    decideur: int,
    options: Sequence[Any],
    context: dict[str, Any],
    *,
    slot_id: str,
    profile: str,
    resume_tag: str = "RESUME",
    resume_payload: tuple[Any, ...] = (),
    decision_type: str = DEC_EFFET_TUILE,
) -> DecisionRequest:
    """Suspend proprement un effet de tuile sur une DecisionRequest gouvernée par `decideur`."""
    opts_tuple = tuple(options)
    assert len(opts_tuple) >= 1, f"Options vides interdites pour {slot_id}:{profile}"
    assert 0 <= decideur < state.cfg.n_players
    ctx_copy = dict(context)
    ctx_copy.setdefault("slot_id", slot_id)
    ctx_copy.setdefault("profile", profile)
    req = DecisionRequest(
        decideur=decideur,
        decision_type=decision_type,
        options=opts_tuple,
        context=ctx_copy,
    )
    state._continuation.insert(
        0,
        ("APPLY_EFFECT_CHOICE", slot_id, profile, resume_tag, tuple(resume_payload)),
    )
    state._continuation.insert(0, ("WAIT_DECISION", req))
    return req


def _is_slot_in_play_for_hook(state: GameState, slot_id: str) -> bool:
    """Vérifie qu'un emplacement est effectivement en jeu avant d'exécuter son hook."""
    if slot_id in ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"):
        return state.cfg.mode >= 2
    meta = SYNERGY_META.get(slot_id)
    if meta is None:
        return False
    fam, _, num = meta
    if fam == FAMILLE_GARDIEN:
        for c in range(1, TRACK_LEN + 1):
            g_num, _ = state.get_gardien_at_case(c)
            if g_num == num:
                return True
        return False
    if fam == FAMILLE_CROISSANCE:
        return state.get_nid_position(num) is not None
    # Rêve sur la Piste des Tactiques
    return state.find_tactique_rank(100 + num) is not None


def _matching_registrations(
    state: GameState, hook_name: str, target_slot: str | None
) -> list[TileRegistration]:
    regs = _RegistryStore.by_hook.get(hook_name)
    if not regs:
        return []
    out: list[TileRegistration] = []
    for reg in regs:
        if target_slot is not None and reg.slot_id != target_slot:
            continue
        if state.cfg.profile_for_slot(reg.slot_id) != reg.profile:
            continue
        if not _is_slot_in_play_for_hook(state, reg.slot_id):
            continue
        out.append(reg)
    return out


def dispatch_hook(state: GameState, hook_name: str, ctx: dict[str, Any] | None = None) -> list[Any]:
    """Exécute le bus de hooks pour les tuiles en jeu ayant un profil actif.

    En Mode 1 : retourne immédiatement [].
    En Mode 2 : neutralise les textes de G/R/M (profile_for_slot -> None) tout en
    laissant passer les hooks structurels et Migration A/A.
    Si un handler suspend via push_effect_decision, met en file les handlers restants.
    """
    if state.cfg.mode == 1:
        return []
    regs = _RegistryStore.by_hook.get(hook_name)
    if not regs:
        return []
    payload = ctx if ctx is not None else {}
    target_slot = payload.get("slot_id")
    matched = _matching_registrations(state, hook_name, target_slot)
    if not matched:
        return []

    results: list[Any] = []
    for idx, reg in enumerate(matched):
        rem_slots = tuple(r.slot_id for r in matched[idx + 1 :])
        resume_frame: tuple[Any, ...] | None = None
        if rem_slots:
            frozen_ctx = tuple(
                (k, v)
                for k, v in payload.items()
                if isinstance(v, (int, str, bool, float, tuple, type(None)))
            )
            resume_frame = ("RESUME_HOOK_QUEUE", hook_name, rem_slots, frozen_ctx)
            state._continuation.insert(0, resume_frame)

        results.append(reg.handler(state, hook_name, payload))

        if resume_frame is not None:
            if state._continuation and state._continuation[0] == resume_frame:
                state._continuation.pop(0)
            else:
                return results
        elif has_pending_decision(state):
            return results
    return results


# ---------------------------------------------------------------------------
# Implémentation propre des 8 Primitives Formelles v5.3
# ---------------------------------------------------------------------------


def prim_mod_seuil(
    state: GameState,
    delta: int,
    *,
    ray: int | None = None,
    p: int | None = None,
    m_type: int | None = None,
) -> None:
    """Primitive 1 : MOD_SEUIL — modifie le Seuil de Parade (parcelle, rayon, machine ou global)."""
    if ray is not None and m_type is not None:
        state.add_machine_seuil_mod_turn(ray, m_type, delta)
    elif ray is not None and p is not None:
        state.add_parcel_seuil_mod_turn(ray, p, delta)
    elif ray is not None:
        for depth in range(1, state.cfg.p_max + 1):
            if not state.is_route_forestiere(ray, depth):
                state.add_parcel_seuil_mod_turn(ray, depth, delta)
    else:
        state.add_global_mod_seuil_turn(delta)


def prim_creation_entite(
    state: GameState,
    entity_type: str,
    *,
    ray: int = 0,
    p: int = 1,
    lisiere: int | None = None,
    count: int = 1,
    light_trigger: bool = True,
) -> None:
    """Primitive 2 : CREATION_ENTITE — crée Insecte, Piège, Sabotage ou Arbre (Repousse)."""
    assert count >= 1
    if entity_type == "INSECTE":
        if lisiere is not None:
            state.set_furtivite_insectes(lisiere, p, state.get_furtivite_insectes(lisiere, p) + count)
        else:
            state.set_parcel_insectes(ray, p, state.get_parcel_insectes(ray, p) + count)
        _record_phys_ops(state, count)
        if light_trigger:
            state.light_trigger(6)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(6)
        return

    if entity_type == "PIEGE":
        assert not state.is_route_forestiere(ray, p), "Impossible de piéger une Route Forestière"
        assert state.get_parcel_piege(ray, p) == PIEGE_AUCUN, "Parcelle déjà piégée"
        state.set_parcel_piege(ray, p, PIEGE_ACTIF)
        _record_phys_ops(state, 1)
        if light_trigger:
            state.light_trigger(2)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(2)
        return

    if entity_type == "SABOTAGE":
        state.add_permanent_sabotage(count=count, light_case_3=light_trigger)
        if light_trigger:
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(3)
        _record_phys_ops(state, count)
        return

    if entity_type == "ARBRE":
        assert not state.is_route_forestiere(ray, p)
        arbres = state.get_parcel_arbres(ray, p)
        souches = state.get_parcel_souches(ray, p)
        cap = state.cfg.dotation_arbres[p - 1]
        converted = min(count, souches, max(0, cap - arbres))
        if converted > 0:
            state.set_parcel_arbres_souches(ray, p, arbres + converted, souches - converted)
            _record_phys_ops(state, converted)
        return

    raise ValueError(f"CREATION_ENTITE inconnue : {entity_type}")


def apply_machine_nid_contact(state: GameState, ray: int, p: int) -> bool:
    """Règle A16 : tout mouvement entrant d'une machine sur un Nid non protégé le renvoie
    en lisière (reconstructible) et défausse tous les Insectes locaux.
    """
    m_num, _ = state.get_parcel_nid(ray, p)
    if m_num == 0:
        return False

    ctx: dict[str, Any] = {"ray": ray, "p": p, "m_num": m_num, "protected": False}
    dispatch_hook(state, HOOK_5_CONTACT_NID, ctx)
    if ctx.get("protected"):
        return False

    state.clear_nid(m_num)
    tile_id = f"M{m_num}"
    l_slot = state.find_lisiere_slot_by_tile_id(tile_id)
    if l_slot is not None:
        state.set_lisiere_tile_state(l_slot, LISIERE_UNCONSTRUCTED, 0)
    ins_before = state.get_parcel_insectes(ray, p)
    state.set_parcel_insectes(ray, p, 0)
    _record_phys_ops(state, 1 + ins_before)
    return True


def _tracked_defenders_at(
    state: GameState,
    *,
    src_ray: int,
    src_p: int,
    src_lisiere: int | None,
    src_lisiere_slot: int | None,
) -> list[tuple[int, int]]:
    matched: list[tuple[int, int]] = []
    for s in range(state.cfg.n_players):
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw == 0:
                continue
            kind, a, b, _ = state.decode_def_loc(raw)
            if src_lisiere_slot is not None:
                if kind == "LISIERE" and a == src_lisiere_slot:
                    matched.append((s, d))
            elif src_lisiere is not None:
                if kind == "FURTIVITE" and a == src_lisiere and b == src_p:
                    matched.append((s, d))
            elif kind == "FORET" and a == src_ray and b == src_p:
                matched.append((s, d))
    return matched


def prim_deplacement(
    state: GameState,
    entity_type: str,
    *,
    src_ray: int = 0,
    src_p: int = 1,
    dst_ray: int = 0,
    dst_p: int = 1,
    src_lisiere: int | None = None,
    dst_lisiere: int | None = None,
    src_lisiere_slot: int | None = None,
    m_type: int = 0,
    global_track: str | None = None,
    global_case: int = 1,
    count: int = 1,
) -> bool:
    """Primitive 3 : DEPLACEMENT — déplace Insecte, Machine ou Défenseur."""
    if entity_type == "INSECTE":
        if src_lisiere is not None:
            cur = state.get_furtivite_insectes(src_lisiere, src_p)
            assert cur >= count
            state.set_furtivite_insectes(src_lisiere, src_p, cur - count)
        else:
            cur = state.get_parcel_insectes(src_ray, src_p)
            assert cur >= count
            state.set_parcel_insectes(src_ray, src_p, cur - count)

        if global_track == "BUG":
            state.set_bugs_at_case(global_case, state.get_bugs_at_case(global_case) + count)
        elif global_track == "COLONIE":
            state.set_colonie_at_case(global_case, state.get_colonie_at_case(global_case) + count)
        elif dst_lisiere is not None:
            state.set_furtivite_insectes(
                dst_lisiere, dst_p, state.get_furtivite_insectes(dst_lisiere, dst_p) + count
            )
        else:
            assert not state.is_route_forestiere(dst_ray, dst_p)
            state.set_parcel_insectes(dst_ray, dst_p, state.get_parcel_insectes(dst_ray, dst_p) + count)
        _record_phys_ops(state, count)
        return True

    if entity_type == "MACHINE":
        pos, st, pending_s = state.get_machine_pos_status(src_ray, m_type)
        if st == MACHINE_STATUS_RETIRED or pos == 0:
            return False
        assert not state.is_route_forestiere(dst_ray, dst_p)
        state.set_machine_pos_status(dst_ray, m_type, dst_p, st, pending_s)
        _record_phys_ops(state, 1)
        apply_machine_nid_contact(state, dst_ray, dst_p)
        return True

    if entity_type == "DEFENSEUR":
        assert not state.is_route_forestiere(dst_ray, dst_p)
        assert count >= 1
        tracked = _tracked_defenders_at(
            state,
            src_ray=src_ray,
            src_p=src_p,
            src_lisiere=src_lisiere,
            src_lisiere_slot=src_lisiere_slot,
        )
        moved_tracked = min(count, len(tracked))
        for idx in range(moved_tracked):
            s_id, d_id = tracked[idx]
            state.place_defender_foret(s_id, d_id, dst_ray, dst_p, FACE_DEFINITIF)
        rem_untracked = count - moved_tracked
        if rem_untracked > 0:
            assert src_lisiere is None and src_lisiere_slot is None, (
                "Déplacement non suivi autorisé uniquement depuis une parcelle Forêt"
            )
            cur = state.get_parcel_defenseurs(src_ray, src_p)
            assert cur >= rem_untracked
            state.set_parcel_defenseurs(src_ray, src_p, cur - rem_untracked)
            state.set_parcel_defenseurs(
                dst_ray, dst_p, state.get_parcel_defenseurs(dst_ray, dst_p) + rem_untracked
            )
        _record_phys_ops(state, count)
        return True

    raise ValueError(f"DEPLACEMENT inconnu : {entity_type}")


def prim_mod_puissance(
    state: GameState,
    ray: int,
    m_type: int,
    *,
    delta_rouges: int = 0,
    delta_bleus: int = 0,
    flip_rouge_to_bleu: int = 0,
) -> None:
    """Primitive 4 : MOD_PUISSANCE — ajuste les jetons Puissance rouges et bleus Surchauffe."""
    rouges, bleus = state.get_machine_tokens(ray, m_type)
    ops = 0
    if flip_rouge_to_bleu > 0:
        converted = min(flip_rouge_to_bleu, rouges)
        rouges -= converted
        bleus += converted
        ops += converted
    new_rouges = max(0, min(15, rouges + delta_rouges))
    new_bleus = max(0, min(15, bleus + delta_bleus))
    ops += abs(new_rouges - rouges) + abs(new_bleus - bleus)
    state.set_machine_tokens(ray, m_type, new_rouges, new_bleus)
    _record_phys_ops(state, ops)


def prim_mod_apprentissage(state: GameState, rank_0_5: int, delta: int) -> None:
    """Primitive 5 : MOD_APPRENTISSAGE — neutralisée (Apprentissage supprimé en v5.4.2)."""
    _ = (state, rank_0_5, delta)


def prim_permutation_piste(
    state: GameState,
    action: str,
    *,
    rank_a: int = 0,
    rank_b: int = 0,
    seat: int = 0,
    delta_m: int = 0,
    rebind_tactique: bool = False,
) -> bool:
    """Primitive 6 : PERMUTATION_PISTE — avancée Rêve (saut/poussée) ou lecture M sur piste fixe T1..T6."""
    if action == "SWAP_RANKS":
        # Piste des Tactiques T1..T6 imprimée en dur : aucune permutation de Tactiques.
        _ = (rank_a, rank_b)
        return False

    if action == "ADVANCE_REVE_LEFT":
        assert 0 <= rank_a < TRACK_LEN
        code = state.get_tactique_at_rank(rank_a)
        assert is_reve_code(code), "La tuile ciblée n'est pas un Rêve"
        if rank_a == 0:
            return False
        if state.cfg.reve_advance_mode == "FREE_SLOT_ONLY":
            if is_reve_code(state.get_tactique_at_rank(rank_a - 1)):
                return False
            state.set_tactique_at_rank(rank_a - 1, code)
            state.set_tactique_at_rank(rank_a, rank_a + 1)
            _record_phys_ops(state, 1)
            return True
        dest: int | None = None
        for j in range(rank_a - 1, -1, -1):
            if not is_reve_code(state.get_tactique_at_rank(j)):
                dest = j
                break
        if dest is None:
            return False
        # Poussée du bloc contigu de Rêves vers la première case libre à gauche ;
        # la case libérée retrouve sa Tactique imprimée T1..T6 (rank_a + 1).
        for idx in range(dest, rank_a):
            state.set_tactique_at_rank(idx, state.get_tactique_at_rank(idx + 1))
        state.set_tactique_at_rank(rank_a, rank_a + 1)
        _record_phys_ops(state, rank_a - dest)
        return True

    if action == "SHIFT_LECTURE_M":
        card, d1, d2, lec_m, bound_t = state.get_player_hand(seat)
        if lec_m == 0:
            return False
        new_m = max(1, min(6, lec_m + delta_m))
        new_bound = bound_t
        if rebind_tactique and 1 <= card <= 12 and bound_t > 0:
            # Piste fixe T1..T6 : la Tactique imprimée au rang new_m s'applique toujours
            new_bound = new_m
        state.set_player_hand(seat, card, d1, d2, new_m, new_bound)
        if new_m != lec_m:
            _record_phys_ops(state, 1)
            return True
        return False

    raise ValueError(f"PERMUTATION_PISTE inconnue : {action}")


def prim_partage_info_etat_gardien(
    state: GameState,
    action: str,
    *,
    case_1_6: int = 1,
    new_face: int = 2,
) -> bool:
    """Primitive 7 : PARTAGE_INFO_ETAT_GARDIEN — états Gardiens & ouverture paravents."""
    if action == "OPEN_PARAVENTS":
        if not state.paravents_ouverts:
            state.paravents_ouverts = True
            _record_phys_ops(state, state.cfg.n_players)
        return True

    if action == "MARK_GARDIEN_OPENED":
        g_num, face = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        if not state.consume_one_gardien_pari_defender(case_1_6):
            return False
        # Retrait d'1 Défenseur (mis de côté jusqu'au ménage 6.2/6.3) ;
        # le passage Face 1 -> Face 2 des Gardiens double-face a lieu en 5.3 si le pari est gagné.
        _record_phys_ops(state, 1)

        # Déclenchement de 4. Gardien verrouillé sur DISTINCT_OPEN_1 (anti-boucle strict sur case 4) :
        # chaque autre Gardien distinct qui s'ouvre pour la 1re fois du tour allume 4. Gardien 1 fois.
        should_light_4 = False
        if case_1_6 != 4:
            first_open = not state.has_gardien_opened_this_turn(case_1_6)
            state.mark_gardien_opened_this_turn(case_1_6)
            should_light_4 = first_open

        sync_frame = ("LIGHT_TRIGGER_SYNC", 4)
        if should_light_4:
            state._continuation.insert(0, sync_frame)
        dispatch_hook(
            state,
            HOOK_GARDIEN_OUVERTURE,
            {"slot_id": f"G{g_num}", "case": case_1_6, "face": face},
        )
        if should_light_4 and state._continuation and state._continuation[0] == sync_frame:
            state._continuation.pop(0)
            state.light_trigger(4)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(4)
        return True

    if action == "FLIP_GARDIEN_FACE":
        g_num, old_face = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        state.set_gardien_at_case(case_1_6, g_num, new_face)
        if old_face != new_face:
            _record_phys_ops(state, 1)
        return True

    if action == "RETURN_GARDIEN_TO_LISIERE":
        g_num, _ = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        state.set_gardien_at_case(case_1_6, 0, 1)
        l_slot = state.find_lisiere_slot_by_tile_id(f"G{g_num}")
        if l_slot is not None:
            st, _ = state.get_lisiere_tile_state(l_slot)
            if st == LISIERE_CONSTRUCTED:
                rem_tracked = len(
                    _tracked_defenders_at(
                        state,
                        src_ray=0,
                        src_p=1,
                        src_lisiere=None,
                        src_lisiere_slot=l_slot,
                    )
                )
                state.set_lisiere_tile_state(l_slot, LISIERE_UNCONSTRUCTED, min(2, rem_tracked))
        _record_phys_ops(state, 1)
        return True

    raise ValueError(f"PARTAGE_INFO_ETAT_GARDIEN inconnue : {action}")


def prim_mod_loi_du_coeur(state: GameState, law_id: str, *, active: bool = True) -> bool:
    """Primitive 8 : MOD_LOI_DU_COEUR — point d'entrée typé des Lois passives/temporaires."""
    _ = (state, law_id, active)
    return active
