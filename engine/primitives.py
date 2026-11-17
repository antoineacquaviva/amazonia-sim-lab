"""Bus des 8 Primitives Formelles, structures de décision/fin et registre de hooks."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any, ClassVar, NamedTuple

from engine.state import (
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
    "HOOK_1_3_LECTURE_DE",
    "HOOK_2_1_DEBUT",
    "HOOK_3_1_CONSTRUCTION",
    "HOOK_3_2_OUVERTURE_REVE",
    "HOOK_3_2_REVELATION",
    "HOOK_4_1_FURTIVITE",
    "HOOK_4_2_NID_APRES_PROD",
    "HOOK_4_3_COLONIE_FIN",
    "HOOK_5_3_PRE_RETRAIT",
    "HOOK_5_CONTACT_NID",
    "HOOK_5_DEFENSE_PARCELLE",
    "HOOK_5_PARADE_HARPIE",
    "HOOK_5_PARADE_JAGUAR",
    "HOOK_5_SEUIL_PARADE",
    "HOOK_5_TERRASSEMENT",
    "HOOK_6_1_BUG",
    "HOOK_6_1_REDUCTION_VOLONTAIRE",
    "HOOK_6_2_AVANCEMENT",
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
    "list_registered_tiles",
    "prim_creation_entite",
    "prim_deplacement",
    "prim_mod_apprentissage",
    "prim_mod_loi_du_coeur",
    "prim_mod_puissance",
    "prim_mod_seuil",
    "prim_partage_info_etat_gardien",
    "prim_permutation_piste",
    "register_tile",
)

# Causes canoniques de fin de partie
CAUSE_TOUR_8: str = "TOUR_8_ATTEINT"
CAUSE_REVE_RANG_1: str = "REVE_RANG_1"
CAUSE_REVEIL_GARDIENS: str = "REVEIL_GARDIENS"

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
HOOK_3_1_CONSTRUCTION: str = "HOOK_3_1_CONSTRUCTION"
HOOK_3_2_REVELATION: str = "HOOK_3_2_REVELATION"
HOOK_3_2_OUVERTURE_REVE: str = "HOOK_3_2_OUVERTURE_REVE"
HOOK_GARDIEN_OUVERTURE: str = "HOOK_GARDIEN_OUVERTURE"
HOOK_4_1_FURTIVITE: str = "HOOK_4_1_FURTIVITE"
HOOK_4_2_NID_APRES_PROD: str = "HOOK_4_2_NID_APRES_PROD"
HOOK_4_3_COLONIE_FIN: str = "HOOK_4_3_COLONIE_FIN"
HOOK_5_PARADE_JAGUAR: str = "HOOK_5_PARADE_JAGUAR"
HOOK_5_PARADE_HARPIE: str = "HOOK_5_PARADE_HARPIE"
HOOK_5_SEUIL_PARADE: str = "HOOK_5_SEUIL_PARADE"
HOOK_5_DEFENSE_PARCELLE: str = "HOOK_5_DEFENSE_PARCELLE"
HOOK_5_TERRASSEMENT: str = "HOOK_5_TERRASSEMENT"
HOOK_5_CONTACT_NID: str = "HOOK_5_CONTACT_NID"
HOOK_5_3_PRE_RETRAIT: str = "HOOK_5_3_PRE_RETRAIT"
HOOK_6_1_REDUCTION_VOLONTAIRE: str = "HOOK_6_1_REDUCTION_VOLONTAIRE"
HOOK_6_1_BUG: str = "HOOK_6_1_BUG"
HOOK_6_2_AVANCEMENT: str = "HOOK_6_2_AVANCEMENT"
HOOK_REPOUSSE_FINALE: str = "HOOK_REPOUSSE_FINALE"


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
            g_num, _, _ = state.get_gardien_at_case(c)
            if g_num == num:
                return True
        return False
    if fam == FAMILLE_CROISSANCE:
        return state.get_nid_position(num) is not None
    # Rêve sur la Piste des Tactiques
    return state.find_tactique_rank(100 + num) is not None


def dispatch_hook(state: GameState, hook_name: str, ctx: dict[str, Any] | None = None) -> list[Any]:
    """Exécute le bus de hooks pour les tuiles en jeu ayant un profil actif.

    En Mode 1 : retourne immédiatement [].
    En Mode 2 : neutralise les textes de G/R/M (profile_for_slot -> None) tout en
    laissant passer les hooks structurels et Migration A/A.
    """
    if state.cfg.mode == 1:
        return []
    regs = _RegistryStore.by_hook.get(hook_name)
    if not regs:
        return []
    payload = ctx if ctx is not None else {}
    target_slot = payload.get("slot_id")
    results: list[Any] = []
    for reg in regs:
        if target_slot is not None and reg.slot_id != target_slot:
            continue
        active_prof = state.cfg.profile_for_slot(reg.slot_id)
        if active_prof != reg.profile:
            continue
        if not _is_slot_in_play_for_hook(state, reg.slot_id):
            continue
        results.append(reg.handler(state, hook_name, payload))
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
        if light_trigger:
            state.light_trigger(6)
        return

    if entity_type == "PIEGE":
        assert not state.is_route_forestiere(ray, p), "Impossible de piéger une Route Forestière"
        assert state.get_parcel_piege(ray, p) == PIEGE_AUCUN, "Parcelle déjà piégée"
        state.set_parcel_piege(ray, p, PIEGE_ACTIF)
        if light_trigger:
            state.light_trigger(2)
        return

    if entity_type == "SABOTAGE":
        state.add_permanent_sabotage(count=count, light_case_3=light_trigger)
        return

    if entity_type == "ARBRE":
        assert not state.is_route_forestiere(ray, p)
        arbres = state.get_parcel_arbres(ray, p)
        souches = state.get_parcel_souches(ray, p)
        cap = state.cfg.dotation_arbres[p - 1]
        converted = min(count, souches, max(0, cap - arbres))
        if converted > 0:
            state.set_parcel_arbres_souches(ray, p, arbres + converted, souches - converted)
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
    state.set_parcel_insectes(ray, p, 0)
    return True


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
        return True

    if entity_type == "MACHINE":
        pos, st, pending_s = state.get_machine_pos_status(src_ray, m_type)
        if st == MACHINE_STATUS_RETIRED or pos == 0:
            return False
        assert not state.is_route_forestiere(dst_ray, dst_p)
        state.set_machine_pos_status(dst_ray, m_type, dst_p, st, pending_s)
        apply_machine_nid_contact(state, dst_ray, dst_p)
        return True

    if entity_type == "DEFENSEUR":
        assert not state.is_route_forestiere(dst_ray, dst_p)
        cur = state.get_parcel_defenseurs(src_ray, src_p)
        assert cur >= count
        state.set_parcel_defenseurs(src_ray, src_p, cur - count)
        state.set_parcel_defenseurs(dst_ray, dst_p, state.get_parcel_defenseurs(dst_ray, dst_p) + count)
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
    if flip_rouge_to_bleu > 0:
        converted = min(flip_rouge_to_bleu, rouges)
        rouges -= converted
        bleus += converted
    rouges = max(0, min(15, rouges + delta_rouges))
    bleus = max(0, min(15, bleus + delta_bleus))
    state.set_machine_tokens(ray, m_type, rouges, bleus)


def prim_mod_apprentissage(state: GameState, rank_0_5: int, delta: int) -> None:
    """Primitive 5 : MOD_APPRENTISSAGE — ajoute ou retire des jetons Apprentissage."""
    cur = state.get_apprentissage_at_rank(rank_0_5)
    state.set_apprentissage_at_rank(rank_0_5, max(0, min(255, cur + delta)))


def prim_permutation_piste(
    state: GameState,
    action: str,
    *,
    rank_a: int = 0,
    rank_b: int = 0,
    seat: int = 0,
    delta_m: int = 0,
) -> bool:
    """Primitive 6 : PERMUTATION_PISTE — échange sur piste centrale, avancée Rêve ou lecture M."""
    if action == "SWAP_RANKS":
        assert 0 <= rank_a < TRACK_LEN and 0 <= rank_b < TRACK_LEN
        if rank_a == rank_b:
            return False
        ca = state.get_tactique_at_rank(rank_a)
        cb = state.get_tactique_at_rank(rank_b)
        aa = state.get_apprentissage_at_rank(rank_a)
        ab = state.get_apprentissage_at_rank(rank_b)
        state.set_tactique_at_rank(rank_a, cb)
        state.set_tactique_at_rank(rank_b, ca)
        state.set_apprentissage_at_rank(rank_a, ab)
        state.set_apprentissage_at_rank(rank_b, aa)
        # Note : les Insectes Bug restent fixes sur leur numéro d'emplacement imprimé !
        return True

    if action == "ADVANCE_REVE_LEFT":
        assert 0 <= rank_a < TRACK_LEN
        code = state.get_tactique_at_rank(rank_a)
        assert is_reve_code(code), "La tuile ciblée n'est pas un Rêve"
        if rank_a == 0:
            return False
        return prim_permutation_piste(state, "SWAP_RANKS", rank_a=rank_a, rank_b=rank_a - 1)

    if action == "SHIFT_LECTURE_M":
        card, d1, d2, lec_m, bound_t = state.get_player_hand(seat)
        if lec_m == 0:
            return False
        new_m = max(1, min(6, lec_m + delta_m))
        state.set_player_hand(seat, card, d1, d2, new_m, bound_t)
        return new_m != lec_m

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
        state.paravents_ouverts = True
        return True

    if action == "MARK_GARDIEN_OPENED":
        g_num, face, used = state.get_gardien_at_case(case_1_6)
        if g_num == 0 or used:
            return False
        # Marquage immédiat avant application du texte + Résonance 4
        state.set_gardien_at_case(case_1_6, g_num, face, True)
        dispatch_hook(
            state,
            HOOK_GARDIEN_OUVERTURE,
            {"slot_id": f"G{g_num}", "case": case_1_6, "face": face},
        )
        state.light_trigger(4)
        return True

    if action == "FLIP_GARDIEN_FACE":
        g_num, _, used = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        state.set_gardien_at_case(case_1_6, g_num, new_face, used)
        return True

    if action == "RETURN_GARDIEN_TO_LISIERE":
        g_num, _, _ = state.get_gardien_at_case(case_1_6)
        if g_num == 0:
            return False
        state.set_gardien_at_case(case_1_6, 0, 1, False)
        l_slot = state.find_lisiere_slot_by_tile_id(f"G{g_num}")
        if l_slot is not None:
            st, _ = state.get_lisiere_tile_state(l_slot)
            if st == LISIERE_CONSTRUCTED:
                state.set_lisiere_tile_state(l_slot, LISIERE_UNCONSTRUCTED, 0)
        return True

    raise ValueError(f"PARTAGE_INFO_ETAT_GARDIEN inconnue : {action}")


def prim_mod_loi_du_coeur(state: GameState, law_id: str, *, active: bool = True) -> bool:
    """Primitive 8 : MOD_LOI_DU_COEUR — point d'entrée typé des Lois passives/temporaires."""
    _ = (state, law_id, active)
    return active
