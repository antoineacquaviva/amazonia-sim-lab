"""Bus des 7 Primitives Formelles, 6 Verbes du Cœur v6.4, structures de décision/fin et registre de hooks Mode 4."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, NamedTuple

from engine.state import (
    CALE_ECAILLE,
    CALE_NONE,
    CALE_SABOTAGE,
    FACE_DEFINITIF,
    FAMILLE_CROISSANCE,
    FAMILLE_GARDIEN,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    MACHINE_STATUS_RETIRED,
    MAX_ECAILLES,
    PIEGE_ACTIF,
    PIEGE_AUCUN,
    STEP_3_2_REVEAL,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRACK_LEN,
    TRIG_INSECTE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_SABOTAGE,
    GameState,
    is_reve_code,
    is_tactique_code,
    machine_card_code,
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
    "HOOK_3_2_APRES_DEVIATION",
    "HOOK_3_2_APRES_REVELATION",
    "HOOK_3_2_CALE_REVEAL",
    "HOOK_3_2_ECAILLE_REVELEE",
    "HOOK_3_2_OUVERTURE_REVE",
    "HOOK_3_2_REVELATION",
    "HOOK_4_1_FURTIVITE",
    "HOOK_4_2_NID_APRES_PROD",
    "HOOK_4_2_NID_AVANT_PROD",
    "HOOK_4_3_MIGRATION_DESTS",
    "HOOK_5_3_PRE_RETRAIT",
    "HOOK_5_APRES_PARADE_PIEGE",
    "HOOK_5_BOURBIER_CHECK",
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
    "HOOK_5_PARADE_PONTE",
    "HOOK_5_PARADE_SOLDATS",
    "HOOK_5_SEUIL_PARADE",
    "HOOK_5_TERRASSEMENT",
    "HOOK_EFFECT_RESUME",
    "HOOK_ENRACINEMENT",
    "HOOK_GARDIEN_OUVERTURE",
    "HOOK_MACHINE_RECUL",
    "HOOK_REPOUSSE_FINALE",
    "PRIM_CREATION_ENTITE",
    "PRIM_DEPLACEMENT",
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
    "list_machines_targeting_parcel",
    "list_registered_tiles",
    "list_targeted_parcels",
    "prim_creation_entite",
    "prim_deplacement",
    "prim_deplacement_nid",
    "prim_insecte_take_with_priming",
    "prim_mod_loi_du_coeur",
    "prim_mod_puissance",
    "prim_mod_seuil",
    "prim_partage_info_etat_gardien",
    "prim_permutation_piste",
    "push_continuation_sequence",
    "push_effect_decision",
    "register_tile",
    "verb_alterer",
    "verb_etouffer",
    "verb_glisser_reve",
    "verb_reculer",
    "verb_refroidir",
    "verb_semer_au_sac",
)

# Causes canoniques de fin de partie
CAUSE_TOUR_8: str = "TOUR_8_ATTEINT"
CAUSE_REVE_RANG_1: str = "REVE_RANG_1"
CAUSE_REVEIL_GARDIENS: str = "REVEIL_GARDIENS"

# Type canonique de décision émise par un effet de tuile
DEC_EFFET_TUILE: str = "EFFET_TUILE"

# Les 7 Primitives Formelles actives v6.4 / Mode 4
PRIM_MOD_SEUIL: str = "MOD_SEUIL"
PRIM_CREATION_ENTITE: str = "CREATION_ENTITE"
PRIM_DEPLACEMENT: str = "DEPLACEMENT"
PRIM_MOD_PUISSANCE: str = "MOD_PUISSANCE"
PRIM_PERMUTATION_PISTE: str = "PERMUTATION_PISTE"
PRIM_PARTAGE_INFO_ETAT_GARDIEN: str = "PARTAGE_INFO_ETAT_GARDIEN"
PRIM_MOD_LOI_DU_COEUR: str = "MOD_LOI_DU_COEUR"

ALL_PRIMITIVES: tuple[str, ...] = (
    PRIM_MOD_SEUIL,
    PRIM_CREATION_ENTITE,
    PRIM_DEPLACEMENT,
    PRIM_MOD_PUISSANCE,
    PRIM_PERMUTATION_PISTE,
    PRIM_PARTAGE_INFO_ETAT_GARDIEN,
    PRIM_MOD_LOI_DU_COEUR,
)

# Fenêtres / Hooks du bus d'exécution v6.4
HOOK_1_3_LECTURE_DE: str = "HOOK_1_3_LECTURE_DE"
HOOK_2_1_DEBUT: str = "HOOK_2_1_DEBUT"
HOOK_2_1_PORTEE_DEF1: str = "HOOK_2_1_PORTEE_DEF1"
HOOK_3_1_CONSTRUCTION: str = "HOOK_3_1_CONSTRUCTION"
HOOK_3_2_REVELATION: str = "HOOK_3_2_REVELATION"
HOOK_3_2_CALE_REVEAL: str = "HOOK_3_2_CALE_REVEAL"
HOOK_3_2_ECAILLE_REVELEE: str = "HOOK_3_2_ECAILLE_REVELEE"
HOOK_3_2_APRES_DEVIATION: str = "HOOK_3_2_APRES_DEVIATION"
HOOK_3_2_OUVERTURE_REVE: str = "HOOK_3_2_OUVERTURE_REVE"
HOOK_3_2_APRES_REVELATION: str = "HOOK_3_2_APRES_REVELATION"
HOOK_GARDIEN_OUVERTURE: str = "HOOK_GARDIEN_OUVERTURE"
HOOK_4_1_FURTIVITE: str = "HOOK_4_1_FURTIVITE"
HOOK_4_2_NID_AVANT_PROD: str = "HOOK_4_2_NID_AVANT_PROD"
HOOK_4_2_NID_APRES_PROD: str = "HOOK_4_2_NID_APRES_PROD"
HOOK_4_3_MIGRATION_DESTS: str = "HOOK_4_3_MIGRATION_DESTS"
HOOK_5_DEBUT: str = "HOOK_5_DEBUT"
HOOK_5_ORDRE_RAYON: str = "HOOK_5_ORDRE_RAYON"
HOOK_5_CIBLAGE_MACHINE: str = "HOOK_5_CIBLAGE_MACHINE"
HOOK_5_BOURBIER_CHECK: str = "HOOK_5_BOURBIER_CHECK"
HOOK_5_LAW_QUERY: str = "HOOK_5_LAW_QUERY"
HOOK_5_PARADE_JAGUAR: str = "HOOK_5_PARADE_JAGUAR"
HOOK_5_PARADE_HARPIE: str = "HOOK_5_PARADE_HARPIE"
HOOK_5_PARADE_PONTE: str = "HOOK_5_PARADE_PONTE"
HOOK_5_PARADE_SOLDATS: str = "HOOK_5_PARADE_SOLDATS"
HOOK_5_SEUIL_PARADE: str = "HOOK_5_SEUIL_PARADE"
HOOK_5_DEFENSE_PARCELLE: str = "HOOK_5_DEFENSE_PARCELLE"
HOOK_5_APRES_PARADE_PIEGE: str = "HOOK_5_APRES_PARADE_PIEGE"
HOOK_5_PARADE_CLASSIQUE: str = "HOOK_5_PARADE_CLASSIQUE"
HOOK_5_TERRASSEMENT: str = "HOOK_5_TERRASSEMENT"
HOOK_5_CONTACT_NID: str = "HOOK_5_CONTACT_NID"
HOOK_5_FIN_ATTAQUE_MACHINE: str = "HOOK_5_FIN_ATTAQUE_MACHINE"
HOOK_5_3_PRE_RETRAIT: str = "HOOK_5_3_PRE_RETRAIT"
HOOK_MACHINE_RECUL: str = "HOOK_MACHINE_RECUL"
HOOK_ENRACINEMENT: str = "HOOK_ENRACINEMENT"
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


def push_continuation_sequence(
    state: GameState, frames: Sequence[tuple[Any, ...]]
) -> None:
    """Empile une séquence de frames en tête de continuation dans leur ordre chronologique naturel (C3-02)."""
    if frames:
        state._continuation[0:0] = list(frames)


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
    push_continuation_sequence(
        state,
        (
            ("WAIT_DECISION", req),
            ("APPLY_EFFECT_CHOICE", slot_id, profile, resume_tag, tuple(resume_payload)),
        ),
    )
    return req


def _is_slot_in_play_for_hook(
    state: GameState, slot_id: str, hook_name: str = ""
) -> bool:
    """Vérifie qu'un emplacement est effectivement en jeu avant d'exécuter son hook."""
    if slot_id in ("SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"):
        return state.cfg.mode >= 2 and state.cfg.has_insectes_peuple
    meta = SYNERGY_META.get(slot_id)
    if meta is None:
        return False
    if hook_name in (HOOK_ENRACINEMENT, HOOK_REPOUSSE_FINALE) or (
        slot_id == "R2" and hook_name == HOOK_3_2_REVELATION
    ):
        l_slot = state.find_lisiere_slot_by_tile_id(slot_id)
        if l_slot is not None and state.is_slot_rooted(l_slot):
            return True
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
        if not _is_slot_in_play_for_hook(state, reg.slot_id, hook_name):
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
    m_type: int = 0,
    cale_type: int = CALE_SABOTAGE,
    count: int = 1,
    light_trigger: bool = True,
) -> None:
    """Primitive 2 : CREATION_ENTITE — crée Insecte, Piège, Croc, Sabotage, Écaille, Altération, Cale ou Arbre."""
    assert count >= 1
    if entity_type == "INSECTE":
        if not state.cfg.has_insectes_peuple:
            return
        assert lisiere is None, "Insectes en Furtivité strictement interdits en v6.2"
        state.set_parcel_insectes(ray, p, state.get_parcel_insectes(ray, p) + count)
        _record_phys_ops(state, count)
        if light_trigger:
            state.light_trigger(TRIG_INSECTE)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(TRIG_INSECTE)
        return

    if entity_type == "PASSENGER_INSECTE":
        if not state.cfg.has_insectes_peuple:
            return
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st == MACHINE_STATUS_RETIRED or pos == 0:
            return
        cur = state.get_machine_passenger_insects(ray, m_type)
        state.set_machine_passenger_insects(ray, m_type, min(15, cur + count))
        _record_phys_ops(state, count)
        return

    if entity_type == "PIEGE":
        assert not state.is_route_forestiere(ray, p), "Impossible de piéger une Route Forestière"
        assert state.get_parcel_piege(ray, p) == PIEGE_AUCUN, "Parcelle déjà piégée"
        state.set_parcel_piege(ray, p, PIEGE_ACTIF)
        _record_phys_ops(state, 1)
        trk = _get_active_telemetry()
        if trk is not None:
            trk.ok_pieges_placed += 1
            if light_trigger:
                trk.on_trigger_lit(TRIG_PIEGEAGE)
        if light_trigger:
            state.light_trigger(TRIG_PIEGEAGE)
        return

    if entity_type == "CROC":
        assert not state.is_route_forestiere(ray, p), "Impossible de poser le Croc sur une Route Forestière"
        state.set_croc_parcel(ray, p)
        _record_phys_ops(state, 1)
        return

    if entity_type == "SABOTAGE":
        state.add_permanent_sabotage(count=count, light_case_3=light_trigger)
        trk = _get_active_telemetry()
        if trk is not None:
            trk.ok_sabotage_acquired += count
            if light_trigger:
                trk.on_trigger_lit(TRIG_SABOTAGE)
        _record_phys_ops(state, count)
        return

    if entity_type == "ECAILLE":
        added = state.add_ecaille_to_bag(count=count)
        if added > 0:
            trk = _get_active_telemetry()
            if trk is not None:
                trk.ok_sabotage_acquired += added
                if light_trigger:
                    trk.on_trigger_lit(TRIG_SABOTAGE)
            if light_trigger:
                state.light_trigger(TRIG_SABOTAGE)
            _record_phys_ops(state, added)
        return

    if entity_type == "ALTERATION":
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st != MACHINE_STATUS_NORMAL or pos == 0:
            return
        if state.has_machine_alteration(ray, m_type):
            return
        state.set_machine_alteration(ray, m_type, True)
        _record_phys_ops(state, 1)
        return

    if entity_type == "CALE":
        pos, st, _ = state.get_machine_pos_status(ray, m_type)
        if st != MACHINE_STATUS_NORMAL or pos == 0:
            return
        if state.get_machine_cale(ray, m_type) != CALE_NONE:
            return
        if cale_type == CALE_ECAILLE and state.count_total_ecailles_in_play() >= MAX_ECAILLES:
            return
        state.set_machine_cale(ray, m_type, cale_type)
        _record_phys_ops(state, 1)
        return

    if entity_type == "BUG":
        if not state.cfg.has_insectes_peuple:
            return
        assert 1 <= p <= TRACK_LEN
        state.set_bugs_at_case(p, min(255, state.get_bugs_at_case(p) + count))
        _record_phys_ops(state, count)
        if light_trigger:
            state.light_trigger(TRIG_INSECTE)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(TRIG_INSECTE)
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
    """Règle v6.2 (INV-16) : zéro écrasement au contact hors Route Forestière.

    Nids, Insectes, Pièges, Croc et Duel cohabitent pacifiquement avec toute machine en forêt.
    Seule la création d'une Route Forestière (0 Arbre, 0 Souche) vide la case.
    """
    _ = (state, ray, p)
    return False


def _tracked_defenders_at(
    state: GameState,
    *,
    src_ray: int,
    src_p: int,
    src_lisiere: int | None,
    src_lisiere_slot: int | None,
    from_waiting: bool = False,
    src_seat: int | None = None,
) -> list[tuple[int, int]]:
    matched: list[tuple[int, int]] = []
    for s in range(state.cfg.n_players):
        if src_seat is not None and s != src_seat:
            continue
        for d in (0, 1):
            raw = state.get_player_def_loc_raw(s, d)
            if raw == 0:
                continue
            kind, a, b, _ = state.decode_def_loc(raw)
            if from_waiting:
                if kind == "WAITING":
                    matched.append((s, d))
            elif src_lisiere_slot is not None:
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
    from_waiting: bool = False,
    src_seat: int | None = None,
    src_def_idx: int | None = None,
    dst_furtivite_rive: int | None = None,
    m_type: int = 0,
    dst_machine_type: int | None = None,
    global_track: str | None = None,
    global_case: int = 1,
    count: int = 1,
) -> bool:
    """Primitive 3 : DEPLACEMENT — déplace Insecte, Machine mobile, Piège ou Défenseur."""
    if entity_type == "INSECTE":
        if not state.cfg.has_insectes_peuple:
            return False
        assert src_lisiere is None and dst_lisiere is None, (
            "Insectes en Furtivité strictement interdits en v6.2"
        )
        cur = state.get_parcel_insectes(src_ray, src_p)
        assert cur >= count
        state.set_parcel_insectes(src_ray, src_p, cur - count)

        if dst_machine_type is not None:
            pos_m, st_m, _ = state.get_machine_pos_status(dst_ray, dst_machine_type)
            assert st_m != MACHINE_STATUS_RETIRED and pos_m > 0
            cur_p = state.get_machine_passenger_insects(dst_ray, dst_machine_type)
            state.set_machine_passenger_insects(dst_ray, dst_machine_type, min(15, cur_p + count))
        elif global_track == "BUG":
            state.set_bugs_at_case(global_case, state.get_bugs_at_case(global_case) + count)
        elif global_track == "COLONIE":
            state.set_colonie_at_case(global_case, state.get_colonie_at_case(global_case) + count)
        else:
            assert not state.is_route_forestiere(dst_ray, dst_p)
            state.set_parcel_insectes(dst_ray, dst_p, state.get_parcel_insectes(dst_ray, dst_p) + count)
        _record_phys_ops(state, count)
        return True

    if entity_type == "MACHINE":
        pos, st, pending_s = state.get_machine_pos_status(src_ray, m_type)
        # INV-12 : une machine en Ratissage est strictement immobile
        if st != MACHINE_STATUS_NORMAL or pos == 0:
            return False
        assert not state.is_route_forestiere(dst_ray, dst_p)
        state.set_machine_pos_status(dst_ray, m_type, dst_p, st, pending_s)
        _record_phys_ops(state, 1)
        return True

    if entity_type == "PIEGE":
        assert state.get_parcel_piege(src_ray, src_p) == PIEGE_ACTIF, "Aucun Piège ordinaire à déplacer"
        assert not state.is_route_forestiere(dst_ray, dst_p), "Piège interdit sur Route Forestière"
        assert state.get_parcel_piege(dst_ray, dst_p) == PIEGE_AUCUN, "Parcelle cible déjà piégée"
        state.set_parcel_piege(src_ray, src_p, PIEGE_AUCUN)
        state.set_parcel_piege(dst_ray, dst_p, PIEGE_ACTIF)
        _record_phys_ops(state, 1)
        return True

    if entity_type == "DEFENSEUR":
        assert count >= 1
        if src_seat is not None and src_def_idx is not None:
            if dst_furtivite_rive is not None:
                state.place_defender_furtivite(
                    src_seat, src_def_idx, dst_ray, dst_furtivite_rive, FACE_DEFINITIF
                )
            else:
                assert not state.is_route_forestiere(dst_ray, dst_p)
                state.place_defender_foret(src_seat, src_def_idx, dst_ray, dst_p, FACE_DEFINITIF)
            _record_phys_ops(state, 1)
            return True
        assert not state.is_route_forestiere(dst_ray, dst_p)
        tracked = _tracked_defenders_at(
            state,
            src_ray=src_ray,
            src_p=src_p,
            src_lisiere=src_lisiere,
            src_lisiere_slot=src_lisiere_slot,
            from_waiting=from_waiting,
            src_seat=src_seat,
        )
        moved_tracked = min(count, len(tracked))
        for idx in range(moved_tracked):
            s_id, d_id = tracked[idx]
            state.place_defender_foret(s_id, d_id, dst_ray, dst_p, FACE_DEFINITIF)
        rem_untracked = count - moved_tracked
        if rem_untracked > 0:
            assert src_lisiere is None and src_lisiere_slot is None and not from_waiting, (
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


def prim_permutation_piste(
    state: GameState,
    action: str,
    *,
    rank_a: int = 0,
    rank_b: int = 0,
    seat: int = 0,
    seat_a: int = 0,
    seat_b: int = 0,
    delta_m: int = 0,
    rebind_tactique: bool = False,
) -> bool:
    """Primitive 5 : PERMUTATION_PISTE — glissement contigu Rêve, échange de rangs ou décalage dé M."""
    if action == "ADVANCE_REVE_LEFT":
        assert 0 <= rank_a < TRACK_LEN
        code = state.get_tactique_at_rank(rank_a)
        assert is_reve_code(code), "La tuile ciblée n'est pas un Rêve"
        # INV-15 : 1 seul physique de poussée de bloc contigu vers la gauche + Défenseurs solidaires
        new_rank = state.shift_reve_block_left(rank_a)
        if new_rank is None:
            return False
        _record_phys_ops(state, 1)
        return True

    if action == "SWAP_RANKS":
        assert 0 <= rank_a < TRACK_LEN and 0 <= rank_b < TRACK_LEN
        if rank_a == rank_b:
            return False
        state.swap_tactique_ranks(rank_a, rank_b)
        _record_phys_ops(state, 1)
        return True

    if action == "SWAP_MACHINE_RANKS":
        if seat_a == seat_b:
            return False
        card_a, d1_a, d2_a, lec_a, bound_a = state.get_player_hand(seat_a)
        card_b, d1_b, d2_b, lec_b, bound_b = state.get_player_hand(seat_b)
        state.set_player_hand(seat_a, card_a, d1_a, d2_a, lec_b, bound_b)
        state.set_player_hand(seat_b, card_b, d1_b, d2_b, lec_a, bound_a)
        _record_phys_ops(state, 2)
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

    if action == "SLIDE_GARDIEN_PARI_ONLY":
        g_num, _ = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        if not state.consume_one_gardien_pari_defender(case_1_6):
            return False
        _record_phys_ops(state, 1)
        return True

    if action == "MARK_GARDIEN_OPENED":
        g_num, face = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        if not state.consume_one_gardien_pari_defender(case_1_6):
            return False
        # Glisse 1 Défenseur dans son encoche latérale (jusqu'en 6.2) ;
        # le passage Face 1 -> Face 2 a lieu en 5.3 si le pari est gagné.
        _record_phys_ops(state, 1)
        state.mark_gardien_opened_this_turn(case_1_6)

        # INV-09 v6.4 : Résonance (6e position) s'allume UNIQUEMENT si cette vraie activation
        # vide le dessus du Gardien (dernier pari glissé en encoche), jamais depuis Résonance elle-même.
        should_light_res = False
        if case_1_6 != TRIG_RESONANCE:
            if state.count_gardien_pari_defenders_at_case(case_1_6) == 0:
                should_light_res = True
        else:
            trk_res = _get_active_telemetry()
            if trk_res is not None:
                trk_res.ok_cascade_case4_openings += 1

        sync_frame = ("LIGHT_TRIGGER_SYNC", TRIG_RESONANCE)
        if should_light_res:
            push_continuation_sequence(state, (sync_frame,))
        dispatch_hook(
            state,
            HOOK_GARDIEN_OUVERTURE,
            {"slot_id": f"G{g_num}", "case": case_1_6, "face": face},
        )
        if should_light_res and state._continuation and state._continuation[0] == sync_frame:
            state._continuation.pop(0)
            state.light_trigger(TRIG_RESONANCE)
            trk = _get_active_telemetry()
            if trk is not None:
                trk.on_trigger_lit(TRIG_RESONANCE)
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
        if g_num == 7:
            state.clear_all_bourbiers()
        elif g_num == 9:
            state.clear_all_cales()
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
        trk_ret = _get_active_telemetry()
        if trk_ret is not None:
            trk_ret.ok_gardien_return_lisiere += 1
        _record_phys_ops(state, 1)
        return True

    raise ValueError(f"PARTAGE_INFO_ETAT_GARDIEN inconnue : {action}")


def prim_mod_loi_du_coeur(state: GameState, law_id: str, *, active: bool = True) -> bool:
    """Primitive 8 : MOD_LOI_DU_COEUR — point d'entrée typé des Lois passives/temporaires."""
    _ = (state, law_id, active)
    return active


# ---------------------------------------------------------------------------
# Les 6 Verbes du Cœur v6.4 & Primitives natives Essaim (INV-21)
# ---------------------------------------------------------------------------


def verb_refroidir(state: GameState, ray: int, m_type: int, count: int = 1) -> int:
    """Verbe 1 (Refroidir) : retourne jusqu'à `count` jetons Rouges existants en Bleus Surchauffe (−1).

    Fonctionne sur machine mobile OU en Ratissage ; jamais de Bleu posé à sec depuis la réserve (INV-02).
    """
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0 or count <= 0:
        return 0
    rouges, _ = state.get_machine_tokens(ray, m_type)
    converted = min(count, rouges)
    if converted <= 0:
        return 0
    prim_mod_puissance(state, ray, m_type, flip_rouge_to_bleu=converted)
    return converted


def verb_alterer(state: GameState, ray: int, m_type: int) -> bool:
    """Verbe 2 (Altérer) : pose 1 jeton d'Altération sur une machine mobile sans Altération (jamais Ratissage)."""
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st != MACHINE_STATUS_NORMAL or pos == 0:
        return False
    if state.has_machine_alteration(ray, m_type):
        return False
    prim_creation_entite(state, "ALTERATION", ray=ray, m_type=m_type)
    return True


def verb_reculer(state: GameState, ray: int, m_type: int) -> bool:
    """Verbe 3 (Reculer) : déplace une machine mobile d'1 parcelle vers la bordure en sautant les Routes.

    Sans effet sur une machine en Ratissage ou déjà sur la 1re parcelle ; déclenche `HOOK_MACHINE_RECUL` (R7).
    """
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st != MACHINE_STATUS_NORMAL or pos <= 1:
        return False
    dst_p = state.next_non_razed_towards_border(ray, pos)
    if dst_p is None:
        return False
    moved = prim_deplacement(
        state,
        "MACHINE",
        src_ray=ray,
        src_p=pos,
        dst_ray=ray,
        dst_p=dst_p,
        m_type=m_type,
    )
    if moved:
        dispatch_hook(
            state,
            HOOK_MACHINE_RECUL,
            {"ray": ray, "m_type": m_type, "old_pos": pos, "new_pos": dst_p},
        )
    return moved


def verb_etouffer(
    state: GameState, ray: int, m_type: int, *, seat: int | None = None
) -> bool:
    """Verbe 4 (Étouffer) : neutralise toute l'activation restante de la machine à ce tour (90° + dé retiré).

    Couvre aussi bien une machine mobile (jeton incliné à 90° et dé retiré de 1..6) qu'une machine en
    Ratissage (tournée à 90° sur place jusqu'au ménage, INV-08 / INV-12).
    """
    pos, st, _ = state.get_machine_pos_status(ray, m_type)
    if st == MACHINE_STATUS_RETIRED or pos == 0:
        return False
    already = state.is_machine_etouffee_this_turn(ray, m_type)
    state.mark_machine_etouffee_this_turn(ray, m_type)
    if st == MACHINE_STATUS_NORMAL:
        target_code = machine_card_code(ray, m_type)
        holder = seat
        if holder is None:
            for s in range(state.cfg.n_players):
                c_code, _, _, _, _ = state.get_player_hand(s)
                if c_code == target_code:
                    holder = s
                    break
        if holder is not None:
            c_code, d1, d2, lec_m, bound_t = state.get_player_hand(holder)
            if c_code == target_code and bound_t != 0:
                state.set_player_hand(holder, c_code, d1, d2, lec_m, 0)
    if not already:
        _record_phys_ops(state, 1)
    return not already


def verb_semer_au_sac(
    state: GameState, token_type: str = "SABOTAGE", count: int = 1
) -> int:
    """Verbe 5 (Semer au sac) : glisse `count` jetons (SABOTAGE ou ECAILLE) au sac sans allumer d'icône."""
    assert count >= 1
    if token_type == "SABOTAGE":
        prim_creation_entite(state, "SABOTAGE", count=count, light_trigger=False)
        return count
    if token_type == "ECAILLE":
        before = state.count_total_ecailles_in_play()
        prim_creation_entite(state, "ECAILLE", count=count, light_trigger=False)
        return max(0, state.count_total_ecailles_in_play() - before)
    raise ValueError(f"verb_semer_au_sac type inconnu : {token_type}")


def verb_glisser_reve(
    state: GameState,
    rank_0_5: int,
    *,
    dst_rank_0_5: int | None = None,
    push_block: bool = False,
) -> int | None:
    """Verbe 6 (Glisser un Rêve) : déplace un Rêve sur la Réglette avec ses Défenseurs (debout/couchés)."""
    assert 0 <= rank_0_5 < TRACK_LEN
    if not is_reve_code(state.get_tactique_at_rank(rank_0_5)):
        return None
    if dst_rank_0_5 is not None:
        if state.move_reve_to_free_rank(rank_0_5, dst_rank_0_5):
            _record_phys_ops(state, 1)
            return dst_rank_0_5
        return None
    if push_block:
        new_r = state.shift_reve_block_left(rank_0_5)
        if new_r is not None:
            _record_phys_ops(state, 1)
        return new_r
    new_r = state.slide_reve_1_free_left(rank_0_5)
    if new_r is not None:
        _record_phys_ops(state, 1)
    return new_r


def prim_deplacement_nid(
    state: GameState, m_num: int, dst_ray: int, dst_p: int
) -> bool:
    """Déménagement unifié d'un Nid (INV-21) : emporte tous ses Insectes, Défenseurs et son éventuelle ponte."""
    pos_info = state.get_nid_position(m_num)
    if pos_info is None:
        return False
    src_ray, src_p, active = pos_info
    if (src_ray, src_p) == (dst_ray, dst_p):
        return False
    if state.is_route_forestiere(dst_ray, dst_p):
        return False
    existing_nid, _ = state.get_parcel_nid(dst_ray, dst_p)
    if existing_nid != 0:
        return False
    # Déplacement du Nid (la ponte G14 est indexée par m_num et suit automatiquement)
    state.set_parcel_nid(dst_ray, dst_p, m_num, active_ce_tour=active)
    # Transport simultané de tous les Insectes de la parcelle
    ins = state.get_parcel_insectes(src_ray, src_p)
    if ins > 0:
        state.set_parcel_insectes(src_ray, src_p, 0)
        state.set_parcel_insectes(dst_ray, dst_p, min(255, state.get_parcel_insectes(dst_ray, dst_p) + ins))
    # Transport simultané de tous les Défenseurs de la parcelle
    for s_id, d_id in state.list_defenders_on_parcel(src_ray, src_p):
        state.place_defender_foret(s_id, d_id, dst_ray, dst_p, FACE_DEFINITIF)
    _record_phys_ops(state, 1)
    return True


def prim_insecte_take_with_priming(
    state: GameState, src: tuple[Any, ...]
) -> tuple[bool, int]:
    """Prélève 1 Insecte depuis `src` (ou réserve si 0 Insecte en jeu — Amorçage natif INV-21).

    Retourne `(ok, colonie_case_or_0)` où `colonie_case_or_0` vaut `1..6` si prélevé sur une icône Gardien.
    """
    if not state.cfg.has_insectes_peuple:
        return False, 0
    tag = src[0]
    if tag == "RESERVE":
        if state.count_total_insects_on_board() == 0:
            _record_phys_ops(state, 1)
            return True, 0
        return False, 0
    if tag == "PARCEL":
        r, p = int(src[1]), int(src[2])
        cur = state.get_parcel_insectes(r, p)
        if cur <= 0:
            return False, 0
        state.set_parcel_insectes(r, p, cur - 1)
        _record_phys_ops(state, 1)
        return True, 0
    if tag == "BUG":
        c = int(src[1])
        cur = state.get_bugs_at_case(c)
        if cur <= 0:
            return False, 0
        state.set_bugs_at_case(c, cur - 1)
        _record_phys_ops(state, 1)
        return True, 0
    if tag == "COLONIE":
        c = int(src[1])
        cur = state.get_colonie_at_case(c)
        if cur <= 0:
            return False, 0
        state.set_colonie_at_case(c, cur - 1)
        _record_phys_ops(state, 1)
        return True, c
    if tag == "PASSENGER":
        r, mt = int(src[1]), int(src[2])
        cur = state.get_machine_passenger_insects(r, mt)
        if cur <= 0:
            return False, 0
        state.set_machine_passenger_insects(r, mt, cur - 1)
        _record_phys_ops(state, 1)
        return True, 0
    return False, 0


def _is_curupira_reverse_rank(state: GameState, rank_1_6: int) -> bool:
    """Vrai si R7 (Le Curupira) siège activement au rang `rank_1_6` (marche à reculons)."""
    if state.cfg.mode < 4 or state.cfg.profile_for_slot("R7") is None:
        return False
    return state.get_tactique_at_rank(rank_1_6 - 1) == TILE_R_BASE + 7


def list_targeted_parcels(state: GameState) -> tuple[tuple[int, int], ...]:
    """Retourne toutes les « parcelles ciblées » actuelles (hors machines Étouffées, incluant Ratissages, INV-12)."""
    targeted: set[tuple[int, int]] = set()
    n = state.cfg.n_players

    # 1. Machines normales révélées et non encore résolues (non Étouffées, non annulées, non altérées)
    for s in range(n):
        if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
            continue
        card, _, _, lec_m, bound_t = state.get_player_hand(s)
        if not (1 <= card <= 12):
            continue
        r, mt = (card - 1) // 2, (card - 1) % 2
        if state.is_machine_etouffee_this_turn(r, mt):
            continue
        if is_tactique_code(bound_t):
            t_code = bound_t
        elif state.step == STEP_3_2_REVEAL and 1 <= lec_m <= TRACK_LEN:
            t_code = lec_m
        else:
            continue
        pos, st, _ = state.get_machine_pos_status(r, mt)
        _, _, attacked = state.get_machine_turn_stats(r, mt)
        if st != MACHINE_STATUS_NORMAL or pos == 0 or attacked:
            continue
        rev_dev = _is_curupira_reverse_rank(state, t_code)
        spec = TACTIQUES_SPEC[t_code]
        for c_type in spec.cibles:
            if c_type == "SUR_PLACE":
                if not state.is_route_forestiere(r, pos):
                    targeted.add((r, pos))
            elif c_type == "DEVANT":
                p_dev = (
                    state.next_non_razed_towards_border(r, pos)
                    if rev_dev
                    else state.next_non_razed_towards_heart(r, pos)
                )
                if p_dev is not None:
                    targeted.add((r, p_dev))

    # 2. Machines en Ratissage non Étouffées n'ayant pas encore frappé ce tour (INV-12)
    for r in range(n):
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if state.is_machine_etouffee_this_turn(r, mt):
                continue
            pos, st, _ = state.get_machine_pos_status(r, mt)
            _, _, attacked = state.get_machine_turn_stats(r, mt)
            if (
                st == MACHINE_STATUS_RATISSAGE
                and pos > 0
                and not attacked
                and not state.is_route_forestiere(r, pos)
            ):
                targeted.add((r, pos))

    return tuple(sorted(targeted))


def list_machines_targeting_parcel(
    state: GameState,
    ray: int,
    p: int,
    *,
    mobile_only: bool = False,
) -> tuple[tuple[int, int], ...]:
    """Retourne les machines `(ray, m_type)` non Étouffées n'ayant pas encore frappé qui visent `(ray, p)`."""
    matched: list[tuple[int, int]] = []
    n = state.cfg.n_players
    seen: set[tuple[int, int]] = set()

    for s in range(n):
        if state.was_seat_altered_this_turn(s) or state.was_seat_cancelled_by_reve_this_turn(s):
            continue
        card, _, _, lec_m, bound_t = state.get_player_hand(s)
        if not (1 <= card <= 12):
            continue
        r, mt = (card - 1) // 2, (card - 1) % 2
        if r != ray or state.is_machine_etouffee_this_turn(r, mt):
            continue
        if is_tactique_code(bound_t):
            t_code = bound_t
        elif state.step == STEP_3_2_REVEAL and 1 <= lec_m <= TRACK_LEN:
            t_code = lec_m
        else:
            continue
        pos, st, _ = state.get_machine_pos_status(r, mt)
        _, _, attacked = state.get_machine_turn_stats(r, mt)
        if st != MACHINE_STATUS_NORMAL or pos == 0 or attacked:
            continue
        rev_dev = _is_curupira_reverse_rank(state, t_code)
        spec = TACTIQUES_SPEC[t_code]
        hits = False
        for c_type in spec.cibles:
            if c_type == "SUR_PLACE" and pos == p and not state.is_route_forestiere(r, pos):
                hits = True
            elif c_type == "DEVANT":
                p_dev = (
                    state.next_non_razed_towards_border(r, pos)
                    if rev_dev
                    else state.next_non_razed_towards_heart(r, pos)
                )
                if p_dev == p:
                    hits = True
        if hits and (r, mt) not in seen:
            seen.add((r, mt))
            matched.append((r, mt))

    if not mobile_only:
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER):
            if state.is_machine_etouffee_this_turn(ray, mt):
                continue
            pos, st, _ = state.get_machine_pos_status(ray, mt)
            _, _, attacked = state.get_machine_turn_stats(ray, mt)
            if (
                st == MACHINE_STATUS_RATISSAGE
                and pos == p
                and not attacked
                and not state.is_route_forestiere(ray, pos)
                and (ray, mt) not in seen
            ):
                seen.add((ray, mt))
                matched.append((ray, mt))

    return tuple(sorted(matched))
