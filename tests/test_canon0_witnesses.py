"""Suite unitaire exhaustive des 35 témoins Canon 0 v6.2 (`contracts/tiles_canon_v6_2.json`).

Inclut un méta-test garantissant la couverture 100 % des 35 identifiants de témoins
(`G1_T1`..`M5_T2`) directement exécutés sur le moteur déterministe v6.2.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import engine.effects  # noqa: F401
from engine.core_engine import (
    DEC_CHOIX_CIBLE_REVE_3_2,
    DEC_MIGRATION_INSECTE_4_3,
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    DEC_REPTILE_POSE_CROC_3_2,
    _advance_continuation,
    _advance_main_step,
    apply_choice,
    apply_repousse_finale,
    compute_parade_seuil,
    list_targeted_parcels,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import (
    DEC_EFFET_TUILE,
    DecisionRequest,
    GameOver,
    _set_active_telemetry,
)
from engine.state import (
    CALE_NONE,
    CALE_SABOTAGE,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    DUEL_TERRITOIRE_TENU,
    FACE_DEFINITIF,
    FURT_RIVE_PIEGE,
    LISIERE_CONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    PLUME_CHAUD,
    PLUME_KIND_RAY,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_4_3_MIGRATION,
    STEP_5_1_TACTIQUES,
    STEP_6_1_ENRACINEMENT,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_REVE,
    TRIG_SABOTAGE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parent.parent
TILES_CANON_PATH = ROOT / "contracts" / "tiles_canon_v6_2.json"


def _make_state(
    peuples: tuple[str, ...],
    *,
    tour: int = 1,
    step: int = STEP_5_1_TACTIQUES,
    mode: int = 4,
) -> GameState:
    cfg = GameConfig(n_players=len(peuples), mode=mode, peuples=peuples, exp_seed=777, rep_id=0)
    st = GameState(cfg)
    st.tour = tour
    st.step = step
    st.paravents_ouverts = True
    return st


def _trig_lit(trk: TelemetryTracker, case_1_6: int) -> bool:
    return bool(trk._turn_trig_lit_mask & (1 << (case_1_6 - 1)))


def _drive(
    state: GameState,
    chooser: Any,
    *,
    stop_step: int | None = None,
    telemetry: TelemetryTracker | None = None,
    max_iters: int = 200,
) -> GameOver | None:
    prev = _set_active_telemetry(telemetry) if telemetry is not None else None
    try:
        for _ in range(max_iters):
            if stop_step is not None and state.step == stop_step and not state._continuation:
                return None
            if state._continuation:
                out: DecisionRequest | GameOver | None = _advance_continuation(state)
            else:
                out = _advance_main_step(state)
            if isinstance(out, GameOver):
                return out
            if isinstance(out, DecisionRequest):
                choice = chooser(out)
                apply_choice(state, choice, telemetry=telemetry)
        raise AssertionError(
            f"Boucle témoin non terminée (step={state.step}, cont={state._continuation})"
        )
    finally:
        if telemetry is not None:
            _set_active_telemetry(prev)


# ---------------------------------------------------------------------------
# Méta-test : 100 % des 35 témoins du contrat couverts
# ---------------------------------------------------------------------------


def test_meta_all_35_contract_witnesses_covered() -> None:
    raw = json.loads(TILES_CANON_PATH.read_text(encoding="utf-8"))
    expected_ids: set[str] = set()
    for tile in raw["tuiles_ciblees"].values():
        for w in tile["profils"]["A"].get("temoins", []):
            expected_ids.add(str(w["id"]))
    assert len(expected_ids) == 35, f"Attendu 35 témoins dans le contrat, trouvé {len(expected_ids)}"

    covered_ids = {
        name.removeprefix("test_witness_").upper()
        for name, obj in globals().items()
        if name.startswith("test_witness_") and callable(obj)
    }
    missing = sorted(expected_ids - covered_ids)
    extra = sorted(covered_ids - expected_ids)
    assert not missing, f"Témoins contrat non couverts : {missing}"
    assert not extra, f"Tests témoins hors contrat : {extra}"


# ---------------------------------------------------------------------------
# Gardiens G1..G15 (16 témoins)
# ---------------------------------------------------------------------------


def test_witness_g1_t1() -> None:
    """G1_T1 (Jaguar) : parade rang 1 ouvre G1 -> bond bâtisseur en attente sur Duel p3-M -> 2e parade, pari gagné."""
    st = _make_state(("M", "R", "O", "H"), tour=1, step=STEP_5_1_TACTIQUES)
    s_m = 0
    st.set_gardien_at_case(TRIG_PARADE, 1, 1)
    st.place_defender_gardien_pari(2, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, TRIG_PARADE, FACE_DEFINITIF)

    # Bâtisseur en attente après 3.1
    st.mark_defender_waiting(2, 0)
    # p1-M (2 Arbres, 2 Def) ciblée par B_M rang 1 (Seuil 2)
    st.place_defender_foret(0, 0, s_m, 1, FACE_DEFINITIF)
    st.place_defender_foret(1, 0, s_m, 1, FACE_DEFINITIF)
    # p3-M (3 Arbres, 2 Def + Duel DEFI) ciblée par A_M rang 4 (Assaut, Seuil 3)
    st.place_defender_foret(0, 1, s_m, 3, FACE_DEFINITIF)
    st.place_defender_foret(1, 1, s_m, 3, FACE_DEFINITIF)
    st.set_duel_defi(s_m, 3)

    st.set_machine_pos_status(s_m, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(s_m, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_m, MACHINE_BULLDOZER), 1, 2, 1, 1)
    st.set_player_hand(1, machine_card_code(s_m, MACHINE_ABATTEUSE), 4, 5, 4, 4)

    # Attaque rang 1 : B_M -> p1-M parée -> ouvre G1 -> déplace bâtisseur en attente sur p3-M
    resolve_single_machine_attack(st, s_m, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st.get_parcel_defenseurs(s_m, 3) == 3
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 1

    # Attaque rang 4 : A_M -> p3-M parée par 3 Defs -> Duel Territoire tenu -> 2e ouverture G1 -> 0 pari restant
    resolve_single_machine_attack(st, s_m, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert st.get_parcel_arbres(s_m, 3) == 3
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, s_m, 3)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0


def test_witness_g2_t1() -> None:
    """G2_T1 (Anaconda) : Duel sur Territoire tenu -> F1 ajoute 2 jetons Sabotage en attente."""
    st = _make_state(("M", "R", "O", "H"), tour=2, step=STEP_5_1_TACTIQUES)
    st.set_gardien_at_case(TRIG_SABOTAGE, 2, 1)
    st.place_defender_gardien_pari(1, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.set_duel_defi(0, 2)
    assert st.flip_duel_to_territoire_tenu()

    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    assert st.sabotage_pending_count == 2


def test_witness_g3_t1() -> None:
    """G3_T1 (Atèle) : p2-M et p2-O à Souche -> voltige légale (interdite vers p2-R sans Souche) -> parade p2-O."""
    st = _make_state(("R", "M", "O", "H"), tour=2, step=STEP_5_1_TACTIQUES)
    s_r, s_m, s_o = 0, 1, 2
    st.set_gardien_at_case(TRIG_PARADE, 3, 1)
    st.place_defender_gardien_pari(1, TRIG_PARADE, FACE_DEFINITIF)

    st.set_parcel_arbres_souches(s_m, 2, 1, 1)
    st.set_parcel_arbres_souches(s_o, 2, 1, 1)
    st.set_parcel_arbres_souches(s_r, 2, 2, 0)  # Sans Souche !

    st.place_defender_foret(s_m, 0, s_m, 2, FACE_DEFINITIF)
    st.place_defender_foret(s_o, 0, s_o, 2, FACE_DEFINITIF)
    st.set_machine_pos_status(s_o, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)

    st.light_trigger(TRIG_PARADE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert req.decision_type == DEC_EFFET_TUILE
    assert (s_m, 2, s_o, 2) in req.options
    assert (s_m, 2, s_r, 2) not in req.options

    apply_choice(st, (s_m, 2, s_o, 2))
    assert st.get_parcel_defenseurs(s_o, 2) == 2

    resolve_single_machine_attack(st, s_o, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(s_o, 2) == 1
    assert st.get_parcel_souches(s_o, 2) == 1


def test_witness_g4_t1() -> None:
    """G4_T1 (Ara) : Piège déclenché ouvre l'Ara (case 2) -> glisse le pari du voisin (case 1) sans l'activer."""
    st = _make_state(("O", "M", "R", "H"), tour=2, step=STEP_5_1_TACTIQUES)
    st.set_gardien_at_case(TRIG_PARADE, 2, 1)  # G2 Anaconda en case 1 (ne doit PAS s'activer !)
    st.set_gardien_at_case(TRIG_PIEGEAGE, 4, 1)  # G4 Ara en case 2
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, TRIG_PIEGEAGE, FACE_DEFINITIF)

    st.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    trk = TelemetryTracker()
    resolve_single_machine_attack(st, 0, MACHINE_BULLDOZER, TACTIQUES_SPEC[1], telemetry=trk)

    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0
    assert st.count_gardien_pari_consumed_at_case(TRIG_PARADE) == 1
    # G2 sur case 1 ne s'est PAS activé : 0 Sabotage ajouté et 1 seul Gardien ouvert (G4)
    assert st.sabotage_pending_count == 0
    assert trk.gardiens_opened_total == 1
    assert _trig_lit(trk, TRIG_PIEGEAGE)
    assert not _trig_lit(trk, TRIG_PARADE)


def test_witness_g5_t1() -> None:
    """G5_T1 (Iguane) : Croc pare B_R p1-R -> G5 repose Croc sur p3-R -> 2e parade A_R, 0 pari restant."""
    st = _make_state(("R", "O", "M", "H"), tour=2, step=STEP_5_1_TACTIQUES)
    s_r = 0
    st.set_gardien_at_case(TRIG_PIEGEAGE, 5, 1)
    st.place_defender_gardien_pari(0, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, TRIG_PIEGEAGE, FACE_DEFINITIF)

    st.set_croc_parcel(s_r, 1)
    st.set_machine_pos_status(s_r, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(s_r, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_r, MACHINE_BULLDOZER), 1, 2, 1, 1)
    st.set_player_hand(1, machine_card_code(s_r, MACHINE_ABATTEUSE), 4, 5, 4, 4)

    resolve_single_machine_attack(st, s_r, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
    assert st.get_croc_parcel() == (s_r, 3)
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 1

    resolve_single_machine_attack(st, s_r, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert st.get_croc_parcel() is None
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0


def test_witness_g6_t1() -> None:
    """G6_T1 (Toucan) : Plume sur R -> 1 rouge -> 1 bleu sur A_R : Seuil 4 -> 2, parade à 2 Défenseurs."""
    st = _make_state(("O", "R", "M", "H"), tour=1, step=STEP_5_1_TACTIQUES)
    s_r = 1
    st.set_oiseau_plume(PLUME_CHAUD, PLUME_KIND_RAY, s_r, locked=True)
    st.set_gardien_at_case(TRIG_SABOTAGE, 6, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)

    st.set_machine_pos_status(s_r, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(s_r, MACHINE_ABATTEUSE, 2, 0)
    st.place_defender_foret(0, 0, s_r, 2, FACE_DEFINITIF)
    st.place_defender_foret(1, 0, s_r, 2, FACE_DEFINITIF)

    seuil_avant = compute_parade_seuil(st, s_r, MACHINE_ABATTEUSE, 2, TACTIQUES_SPEC[4])
    assert seuil_avant == 4

    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)

    rouges, bleus = st.get_machine_tokens(s_r, MACHINE_ABATTEUSE)
    assert rouges == 1 and bleus == 1
    seuil_apres = compute_parade_seuil(st, s_r, MACHINE_ABATTEUSE, 2, TACTIQUES_SPEC[4])
    assert seuil_apres == 2

    resolve_single_machine_attack(st, s_r, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    assert st.get_parcel_arbres(s_r, 2) == 2


def test_witness_g7_t1() -> None:
    """G7_T1 (Tapir) : Piège sur p3-H (1 Arbre, 2 Souches) sauve la parcelle du Bulldozer vs Route sans Piège."""
    def _run_case(with_tapir: bool) -> tuple[int, int, bool]:
        st = _make_state(("M", "H", "R", "O"), tour=2, step=STEP_5_1_TACTIQUES)
        s_h = 1
        st.set_parcel_arbres_souches(s_h, 3, 1, 2)
        st.set_machine_pos_status(s_h, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
        st.set_player_hand(0, machine_card_code(s_h, MACHINE_BULLDOZER), 1, 2, 1, 1)
        if with_tapir:
            st.set_gardien_at_case(TRIG_PIEGEAGE, 7, 1)
            st.place_defender_gardien_pari(0, TRIG_PIEGEAGE, FACE_DEFINITIF)
            st.light_trigger(TRIG_PIEGEAGE)
            sweep_gardiens(st)
            assert st.get_parcel_piege(s_h, 3) == PIEGE_ACTIF
        resolve_single_machine_attack(st, s_h, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
        return (
            st.get_parcel_arbres(s_h, 3),
            st.get_parcel_souches(s_h, 3),
            st.is_route_forestiere(s_h, 3),
        )

    assert _run_case(True) == (1, 2, False)
    assert _run_case(False) == (0, 0, True)


def test_witness_g8_t1() -> None:
    """G8_T1 (Boto) : A_M p3 visant Devant p4-M (Duel) recule en p2 -> cibles décalées, p4-M sauvé (3), p3-M -> [0,3]."""
    st = _make_state(("M", "E", "R", "H"), tour=2, step=STEP_5_1_TACTIQUES)
    s_m = 0
    st.set_gardien_at_case(TRIG_SABOTAGE, 8, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(s_m, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_m, MACHINE_ABATTEUSE), 2, 5, 2, 2)
    st.set_duel_defi(s_m, 4)

    assert list_targeted_parcels(st) == ((s_m, 4),)
    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert (s_m, MACHINE_ABATTEUSE) in req.options
    apply_choice(st, (s_m, MACHINE_ABATTEUSE))
    assert st.get_machine_pos_status(s_m, MACHINE_ABATTEUSE)[0] == 2

    resolve_single_machine_attack(st, s_m, MACHINE_ABATTEUSE, TACTIQUES_SPEC[2])
    assert st.get_parcel_arbres(s_m, 4) == 3
    assert (st.get_parcel_arbres(s_m, 3), st.get_parcel_souches(s_m, 3)) == (0, 3)


def test_witness_g9_t1() -> None:
    """G9_T1 (Caïman noir) : A_R calée en p3 sur T3 (En avançant) frappe mais n'avance pas ; cale -> 1 Sabotage 6.3."""
    st = _make_state(("R", "H", "M", "O"), tour=2, step=STEP_5_1_TACTIQUES)
    s_r = 0
    st.set_gardien_at_case(TRIG_SABOTAGE, 9, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(s_r, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    apply_choice(st, (s_r, MACHINE_ABATTEUSE))
    assert st.get_machine_cale(s_r, MACHINE_ABATTEUSE) == CALE_SABOTAGE

    resolve_single_machine_attack(st, s_r, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert st.get_machine_pos_status(s_r, MACHINE_ABATTEUSE)[0] == 3
    assert st.get_machine_cale(s_r, MACHINE_ABATTEUSE) == CALE_NONE
    assert st.sabotage_pending_count == 1


def test_witness_g10_t1() -> None:
    """G10_T1 (Matamata) : F1 ajoute 1 Écaille ; au tour suivant révélée -> TRIG_SABOTAGE + Croc sur p2-E -> pare."""
    st = _make_state(("R", "E", "M", "O"), tour=1, step=STEP_5_1_TACTIQUES)
    s_e = 1
    st.set_gardien_at_case(TRIG_SABOTAGE, 10, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    assert st.ecaille_pending_count == 1
    assert st.count_total_ecailles_in_play() == 1

    # Tour suivant : Écaille révélée en 3.2 -> allume TRIG_SABOTAGE + pose Croc sur p2-E ciblée
    st.cleanup_end_of_turn_6_2()
    st.tour = 2
    st.step = STEP_3_2_REVEAL
    st.set_machine_pos_status(s_e, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, CARD_ECAILLE, 1, 2, 0, 0)
    st.set_player_hand(1, machine_card_code(s_e, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.decision_type == DEC_REPTILE_POSE_CROC_3_2:
            return (s_e, 2)
        return req.options[0]

    trk = TelemetryTracker()
    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE, telemetry=trk)
    assert st.get_croc_parcel() == (s_e, 2)
    assert _trig_lit(trk, TRIG_SABOTAGE)

    st.step = STEP_5_1_TACTIQUES
    resolve_single_machine_attack(st, s_e, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_parcel_arbres(s_e, 2) == 2
    assert st.get_croc_parcel() is None
    assert _trig_lit(trk, TRIG_PIEGEAGE)


def test_witness_g11_t1() -> None:
    """G11_T1 (Harpie) : Plume sur H -> pose 1 Piège sur p2-H ciblée -> pare et allume TRIG_PIEGEAGE."""
    st = _make_state(("O", "H", "M", "R"), tour=2, step=STEP_5_1_TACTIQUES)
    s_h = 1
    st.set_oiseau_plume(PLUME_CHAUD, PLUME_KIND_RAY, s_h, locked=True)
    st.set_gardien_at_case(TRIG_SABOTAGE, 11, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(s_h, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_h, MACHINE_ABATTEUSE), 1, 2, 1, 1)

    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    assert st.get_parcel_piege(s_h, 2) == PIEGE_ACTIF

    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_h, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_parcel_arbres(s_h, 2) == 2
    assert _trig_lit(trk, TRIG_PIEGEAGE)


def test_witness_g12_t1() -> None:
    """G12_T1 (Ibijau) : Sabotage ouvre G12 avant Rêves -> R7 (rang 4) glisse au rang 3 -> annule machine -> TRIG_REVE."""
    st = _make_state(("O", "E", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    st.paravents_ouverts = False
    st.set_gardien_at_case(TRIG_SABOTAGE, 12, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)

    st.set_tactique_at_rank(3, TILE_R_BASE + 7)  # R7 au rang 4
    st.set_tactique_at_rank(5, TILE_R_BASE + 2)  # R2 au rang 6
    st.place_defender_reve_activation(1, 4, FACE_DEFINITIF, def_idx=0)  # Défenseur sur R7

    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, machine_card_code(2, MACHINE_ABATTEUSE), 3, 5, 3, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "G12_SLIDE_REVE":
            return 3  # rank_idx 3 = rang 4 (R7)
        return req.options[0]

    trk = TelemetryTracker()
    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE, telemetry=trk)
    assert st.get_tactique_at_rank(2) == TILE_R_BASE + 7  # rang 3 = R7
    assert st.get_tactique_at_rank(5) == TILE_R_BASE + 2  # rang 6 = R2
    assert st.get_player_hand(1)[4] == 0  # Machine annulée !
    assert st.was_seat_cancelled_by_reve_this_turn(1)
    assert _trig_lit(trk, TRIG_SABOTAGE)
    assert _trig_lit(trk, TRIG_REVE)


def test_witness_g13_t1() -> None:
    """G13_T1 (Tamanoir) : 2 Insectes de p1-I -> p3-I ciblée (1 Def, Seuil 3) -> parade avec dépense + TRIG_INSECTE."""
    st = _make_state(("M", "I", "R", "O"), tour=2, step=STEP_5_1_TACTIQUES)
    s_i = 1
    st.set_gardien_at_case(TRIG_PARADE, 13, 1)
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)

    st.set_parcel_insectes(s_i, 1, 2)
    st.place_defender_foret(s_i, 0, s_i, 3, FACE_DEFINITIF)
    st.set_machine_pos_status(s_i, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_i, MACHINE_ABATTEUSE), 1, 2, 1, 1)

    st.light_trigger(TRIG_PARADE)
    sweep_gardiens(st)
    req1 = step_until_decision(st)
    assert isinstance(req1, DecisionRequest)
    assert (s_i, 1, s_i, 3) in req1.options
    apply_choice(st, (s_i, 1, s_i, 3))

    req2 = step_until_decision(st)
    assert isinstance(req2, DecisionRequest)
    assert (s_i, 1) in req2.options
    apply_choice(st, (s_i, 1))
    assert st.get_parcel_insectes(s_i, 3) == 2

    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_i, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert (st.get_parcel_arbres(s_i, 3), st.get_parcel_souches(s_i, 3)) == (3, 0)
    assert st.get_parcel_insectes(s_i, 3) == 0
    assert _trig_lit(trk, TRIG_INSECTE)


def test_witness_g14_t1() -> None:
    """G14_T1 (Téju — action) : défausse 1 des 2 Insectes du Nid p2-R -> Piège p3-R pare (TRIG_PIEGEAGE), Nid produit +1."""
    st = _make_state(("R", "I", "M", "O"), tour=2, step=STEP_4_2_NIDS)
    s_r = 0
    st.set_gardien_at_case(TRIG_SABOTAGE, 14, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)

    st.set_parcel_nid(s_r, 2, 2, False)  # M2 sur p2-R
    st.set_parcel_insectes(s_r, 2, 2)
    st.place_defender_foret(1, 0, s_r, 2, FACE_DEFINITIF)
    st.set_machine_pos_status(s_r, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    # Avant 4.2, G14 ouvre et prélève 1 Insecte sur p2-R pour piéger p3-R
    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert (s_r, 2, 3) in req.options
    apply_choice(st, (s_r, 2, 3))
    assert st.get_parcel_piege(s_r, 3) == PIEGE_ACTIF
    assert st.get_parcel_insectes(s_r, 2) == 1

    # 4.2 : le Nid n'a plus que 1 Insecte -> produit +1 (total 2)
    ins_before = st.get_parcel_insectes(s_r, 2)
    _drive(st, lambda r: r.options[0], stop_step=STEP_4_3_MIGRATION)
    assert st.get_parcel_insectes(s_r, 2) - ins_before == 1
    assert st.get_parcel_insectes(s_r, 2) == 2

    # 5.1 : le Piège pare seul A_R -> TRIG_PIEGEAGE, p3-R conserve 3 Arbres
    st.step = STEP_5_1_TACTIQUES
    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_r, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_parcel_arbres(s_r, 3) == 3
    assert _trig_lit(trk, TRIG_PIEGEAGE)


def test_witness_g14_t2() -> None:
    """G14_T2 (Téju — attente) : PASSER conserve la masse critique 2 -> Nid produit +2, p3-R sans Piège tombe à [0,3]."""
    st = _make_state(("R", "I", "M", "O"), tour=2, step=STEP_4_2_NIDS)
    s_r = 0
    st.set_gardien_at_case(TRIG_SABOTAGE, 14, 1)
    st.place_defender_gardien_pari(0, TRIG_SABOTAGE, FACE_DEFINITIF)

    st.set_parcel_nid(s_r, 2, 2, False)
    st.set_parcel_insectes(s_r, 2, 2)
    st.place_defender_foret(1, 0, s_r, 2, FACE_DEFINITIF)
    st.set_machine_pos_status(s_r, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    st.light_trigger(TRIG_SABOTAGE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    apply_choice(st, "PASSER")

    ins_before = st.get_parcel_insectes(s_r, 2)
    _drive(st, lambda r: r.options[0], stop_step=STEP_4_3_MIGRATION)
    assert st.get_parcel_insectes(s_r, 2) - ins_before == 2

    st.step = STEP_5_1_TACTIQUES
    resolve_single_machine_attack(st, s_r, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert (st.get_parcel_arbres(s_r, 3), st.get_parcel_souches(s_r, 3)) == (0, 3)


def test_witness_g15_t1() -> None:
    """G15_T1 (Colibri) : Acte 2, échange A_M rang 3 (Assaut, En avançant) <-> B_M rang 5 (Charge, Devant) -> n'avance pas."""
    st = _make_state(("O", "I", "M", "R"), tour=5, step=STEP_5_1_TACTIQUES)
    s_m = 2
    st.set_gardien_at_case(TRIG_PARADE, 15, 1)
    st.place_defender_gardien_pari(0, TRIG_PARADE, FACE_DEFINITIF)

    st.set_machine_pos_status(s_m, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(s_m, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(s_m, MACHINE_ABATTEUSE), 3, 4, 3, 3)
    st.set_player_hand(1, machine_card_code(s_m, MACHINE_BULLDOZER), 5, 6, 5, 5)

    st.light_trigger(TRIG_PARADE)
    sweep_gardiens(st)
    req = step_until_decision(st)
    assert isinstance(req, DecisionRequest)
    assert (0, 1) in req.options
    apply_choice(st, (0, 1))

    assert st.get_player_hand(0)[4] == 5  # Abatteuse désormais rang 5 (Charge, Devant, avancee=0)
    assert st.get_player_hand(1)[4] == 3  # Bulldozer désormais rang 3

    resolve_single_machine_attack(st, s_m, MACHINE_ABATTEUSE, TACTIQUES_SPEC[5])
    assert st.get_machine_pos_status(s_m, MACHINE_ABATTEUSE)[0] == 2  # N'a pas avancé


# ---------------------------------------------------------------------------
# Rêves R1..R10 (12 témoins)
# ---------------------------------------------------------------------------


def test_witness_r1_t1() -> None:
    """R1_T1 (Seuil des Deux Mondes) : R1 au rang 4 annule A_M sur le rang voisin 3 sans Rêve et allume TRIG_REVE."""
    st = _make_state(("H", "E", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    st.paravents_ouverts = False
    st.set_tactique_at_rank(3, TILE_R_BASE + 1)  # R1 au rang 4 ; rang 3 = T3 (vide de Rêve)
    st.place_defender_reve_activation(0, 4, FACE_DEFINITIF, def_idx=0)
    st.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 3, 4, 3, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    assert st.get_tactique_at_rank(2) == 3  # case 3 sans Rêve
    trk = TelemetryTracker()
    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE, telemetry=trk)
    assert st.get_player_hand(0)[4] == 0
    assert st.was_seat_cancelled_by_reve_this_turn(0)
    assert _trig_lit(trk, TRIG_REVE)


def test_witness_r2_t1() -> None:
    """R2_T1 (Voile de l'Oubli — ouverture) : R2 annule B_H et l'altère ; au tour suivant B_H recule en p1 sans frapper."""
    st = _make_state(("E", "H", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    s_h = 1
    st.paravents_ouverts = False
    st.set_machine_pos_status(s_h, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st.set_tactique_at_rank(2, TILE_R_BASE + 2)  # R2 au rang 3
    st.place_defender_reve_activation(0, 3, FACE_DEFINITIF, def_idx=0)
    st.set_player_hand(0, machine_card_code(s_h, MACHINE_BULLDOZER), 3, 4, 3, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE)
    assert st.has_machine_alteration(s_h, MACHINE_BULLDOZER)

    # Tour suivant : révélation de B_H -> altérée, recule vers p1, bound_t=0
    st.cleanup_end_of_turn_6_2()
    st.tour = 3
    st.step = STEP_3_2_REVEAL
    st.set_player_hand(0, machine_card_code(s_h, MACHINE_BULLDOZER), 2, 3, 2, 0)
    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE)
    assert st.was_seat_altered_this_turn(0)
    assert st.get_player_hand(0)[4] == 0
    assert st.get_machine_pos_status(s_h, MACHINE_BULLDOZER)[0] == 1


def test_witness_r2_t2() -> None:
    """R2_T2 (Voile de l'Oubli — Enraciné) : enraciner R2 altère jusqu'à 2 machines mobiles (A_H, B_E) + repousse p3-E."""
    st = _make_state(("E", "H", "M", "R"), tour=6, step=STEP_6_1_ENRACINEMENT)
    s_e, s_h = 0, 1
    slot_r2 = st.find_lisiere_slot_by_tile_id("R2")
    assert slot_r2 is not None
    st.set_lisiere_tile_state(slot_r2, LISIERE_CONSTRUCTED, 0)
    st.set_tactique_at_rank(4, TILE_R_BASE + 2)
    st.set_parcel_arbres_souches(s_e, 3, 1, 2)

    chosen_order = [(s_h, MACHINE_ABATTEUSE), (s_e, MACHINE_BULLDOZER)]
    idx_ref = [0]

    def _choose(req: DecisionRequest) -> Any:
        if req.decision_type == "ENRACINEMENT_6_1":
            return (slot_r2, 3) if req.decideur == s_e else "PASSER"
        if req.context.get("effect_kind") == "R2_ROOT_ALTER":
            pick = chosen_order[idx_ref[0]]
            idx_ref[0] += 1
            return pick
        return req.options[0]

    _drive(st, _choose, stop_step=63)
    assert st.has_machine_alteration(s_h, MACHINE_ABATTEUSE)
    assert st.has_machine_alteration(s_e, MACHINE_BULLDOZER)

    st.tour = 8
    apply_repousse_finale(st)
    assert (st.get_parcel_arbres(s_e, 3), st.get_parcel_souches(s_e, 3)) == (2, 1)


def test_witness_r3_t1() -> None:
    """R3_T1 (Danse des Esprits-Fauves) : Chant annule au rang 5 (R3 -> 4), rejoint le Duel -> parade -> Territoire tenu."""
    st = _make_state(("H", "M", "R", "O"), tour=2, step=STEP_3_2_REVEAL)
    s_h, s_m = 0, 1
    st.paravents_ouverts = False
    st.set_tactique_at_rank(4, TILE_R_BASE + 3)  # R3 au rang 5
    st.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st.place_defender_reve_activation(s_h, 5, FACE_DEFINITIF, def_idx=0)
    st.set_duel_defi(s_m, 2)
    st.place_defender_foret(s_m, 0, s_m, 2, FACE_DEFINITIF)
    st.set_machine_pos_status(s_m, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)

    st.set_player_hand(0, machine_card_code(2, MACHINE_BULLDOZER), 5, 6, 5, 0)
    st.set_player_hand(1, machine_card_code(s_m, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    trk = TelemetryTracker()
    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE, telemetry=trk)
    assert st.get_tactique_at_rank(3) == TILE_R_BASE + 3  # R3 glissé au rang 4
    assert st.get_parcel_defenseurs(s_m, 2) == 2
    assert _trig_lit(trk, TRIG_REVE)

    st.step = STEP_5_1_TACTIQUES
    resolve_single_machine_attack(st, s_m, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, s_m, 2)
    assert _trig_lit(trk, TRIG_PARADE)


def test_witness_r4_t1() -> None:
    """R4_T1 (Sommeil de la Pierre-Serpent) : m(R)==2 et 1 allié Rive Piège -> R4 complète -> Piège posé en 4.1."""
    st = _make_state(("H", "R", "M", "O"), tour=2, step=STEP_3_2_REVEAL)
    s_h, s_r = 0, 1
    st.paravents_ouverts = False
    st.set_tactique_at_rank(3, TILE_R_BASE + 4)  # R4 au rang 4
    st.place_defender_reve_activation(s_h, 4, FACE_DEFINITIF, def_idx=0)
    st.place_defender_furtivite(2, 0, s_r, FURT_RIVE_PIEGE, FACE_DEFINITIF)

    # 2 machines mobilisées sur rayon R
    st.set_player_hand(0, machine_card_code(s_r, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st.set_player_hand(1, machine_card_code(s_r, MACHINE_BULLDOZER), 2, 3, 2, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "R4_COMPLETE_FURT":
            return s_r
        if req.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1:
            return 2
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_2_NIDS)
    assert st.count_mobilized_machines_for_ray(s_r) == 2
    assert st.get_furtivite_nb_def_rive(s_r, 1, FURT_RIVE_PIEGE) == 2
    assert st.get_parcel_piege(s_r, 2) == PIEGE_ACTIF


def test_witness_r5_t1() -> None:
    """R5_T1 (Vision des Plumes Claires) : Plume sur O -> Défenseur de R5 descend défendre p3-O ciblée -> parade."""
    st = _make_state(("H", "O", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    s_h, s_o = 0, 1
    st.paravents_ouverts = False
    st.set_oiseau_plume(PLUME_CHAUD, PLUME_KIND_RAY, s_o, locked=True)
    st.set_tactique_at_rank(4, TILE_R_BASE + 5)  # R5 au rang 5
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_reve_activation(s_h, 5, FACE_DEFINITIF, def_idx=0)
    st.place_defender_reve_activation(s_o, 5, FACE_DEFINITIF, def_idx=0)
    st.place_defender_foret(2, 0, s_o, 3, FACE_DEFINITIF)
    st.set_machine_pos_status(s_o, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    st.set_player_hand(0, machine_card_code(s_o, MACHINE_ABATTEUSE), 1, 2, 1, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE)
    # Tambour sur R5 -> 2 Défenseurs descendus + 1 déjà là = 3 Défenseurs sur p3-O (Seuil 3) !
    assert st.get_parcel_defenseurs(s_o, 3) == 3

    st.step = STEP_5_1_TACTIQUES
    resolve_single_machine_attack(st, s_o, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_parcel_arbres(s_o, 3) == 3


def test_witness_r6_t1() -> None:
    """R6_T1 (Miel des Ancêtres — Enraciné) : enraciné face à p3-H (1A,2S) voisin p2-H (1A,1S) -> [2,1] & [2,0]."""
    st = _make_state(("H", "I", "M", "R"), tour=8, step=STEP_5_1_TACTIQUES)
    s_h = 0
    slot_r6 = st.find_lisiere_slot_by_tile_id("R6")
    assert slot_r6 is not None
    st.set_parcel_arbres_souches(s_h, 3, 1, 2)
    st.set_parcel_arbres_souches(s_h, 2, 1, 1)
    st.root_tile_at_parcel(slot_r6, s_h, 3, tier_souches=1)

    apply_repousse_finale(st)
    assert (st.get_parcel_arbres(s_h, 3), st.get_parcel_souches(s_h, 3)) == (2, 1)
    assert (st.get_parcel_arbres(s_h, 2), st.get_parcel_souches(s_h, 2)) == (2, 0)


def test_witness_r6_t2() -> None:
    """R6_T2 (Miel des Ancêtres — ouverture) : Défenseur de R6 rejoint Nid sans Défenseur -> production +1 en 4.2."""
    st = _make_state(("H", "I", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    s_h, s_i = 0, 1
    st.paravents_ouverts = False
    st.set_tactique_at_rank(3, TILE_R_BASE + 6)  # R6 au rang 4
    st.place_defender_reve_activation(s_h, 4, FACE_DEFINITIF, def_idx=0)
    st.set_parcel_nid(s_i, 2, 4, False)  # M4 sans Défenseur ni Insecte

    st.set_player_hand(0, 0, 1, 2, 0, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    _drive(st, lambda r: "PASSER" if "PASSER" in r.options else r.options[0], stop_step=STEP_4_3_MIGRATION)
    assert st.get_parcel_defenseurs(s_i, 2) == 1
    assert st.get_parcel_insectes(s_i, 2) == 1


def test_witness_r7_t1() -> None:
    """R7_T1 (Ombre du Maître des Bois) : R7 défendu rang 6 sans machine -> glisse en 5 et pousse R1 en 4."""
    st = _make_state(("E", "M", "R", "H"), tour=2, step=STEP_3_2_REVEAL)
    st.paravents_ouverts = False
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 au rang 5
    st.set_tactique_at_rank(5, TILE_R_BASE + 7)  # R7 au rang 6
    st.place_defender_reve_activation(0, 6, FACE_DEFINITIF, def_idx=0)

    st.set_player_hand(0, 0, 1, 2, 0, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    _drive(st, lambda r: r.options[0], stop_step=STEP_4_1_FURTIVITE)
    assert st.get_tactique_at_rank(3) == TILE_R_BASE + 1  # rang 4 = R1
    assert st.get_tactique_at_rank(4) == TILE_R_BASE + 7  # rang 5 = R7


def test_witness_r8_t1() -> None:
    """R8_T1 (Mirage du Fleuve-Miroir) : retire 1 des 2 Souches de p2-R (2->1) et glisse R8 de 5 en 3."""
    st = _make_state(("E", "R", "I"), tour=2, step=STEP_3_2_REVEAL)
    s_e, s_r = 0, 1
    st.paravents_ouverts = False
    st.set_tactique_at_rank(4, TILE_R_BASE + 8)  # R8 au rang 5
    st.place_defender_reve_activation(s_e, 5, FACE_DEFINITIF, def_idx=0)
    st.set_parcel_arbres_souches(s_r, 2, 0, 2)
    assert st.get_parcel_souches(s_r, 2) == 2

    st.set_player_hand(0, 0, 1, 2, 0, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        ek = req.context.get("effect_kind")
        if ek == "R8_PICK_SOUCHE":
            return (s_r, 2)
        if ek == "R8_PICK_REVE_STEPS":
            return (8, 2)
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE)
    assert st.get_parcel_souches(s_r, 2) == 1
    assert not st.is_route_forestiere(s_r, 2)
    assert st.get_tactique_at_rank(2) == TILE_R_BASE + 8  # rang 3 = R8


def test_witness_r9_t1() -> None:
    """R9_T1 (Écho des Voix Célestes) : Perchoir cache A_O -> R9 révèle, altère A_O et pose Piège p2-O."""
    st = _make_state(("E", "O", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    s_e, s_o = 0, 1
    st.paravents_ouverts = False
    card_ao = machine_card_code(s_o, MACHINE_ABATTEUSE)
    st.oiseau_perchoir_card = card_ao
    # Avant révélation par R9, le Perchoir est strictement masqué pour E
    assert st.get_observation(s_e).oiseau_perchoir_card is None

    st.set_tactique_at_rank(3, TILE_R_BASE + 9)  # R9 au rang 4
    st.place_defender_reve_activation(s_e, 4, FACE_DEFINITIF, def_idx=0)
    st.set_player_hand(0, 0, 1, 2, 0, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "R9_PLACE_PIEGE":
            return (s_o, 2)
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE)
    assert st.has_machine_alteration(s_o, MACHINE_ABATTEUSE)
    assert st.get_parcel_piege(s_o, 2) == PIEGE_ACTIF
    obs_e = st.get_observation(s_e)
    assert obs_e.is_oiseau_perchoir_revealed
    assert obs_e.oiseau_perchoir_card == card_ao


def test_witness_r10_t1() -> None:
    """R10_T1 (Nuée des Songes) : annule machine -> l'altère + pose 1 Insecte sur Nid (1->2) -> production +2 en 4.2."""
    st = _make_state(("E", "I", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    s_e, s_i = 0, 1
    st.paravents_ouverts = False
    st.set_tactique_at_rank(2, TILE_R_BASE + 10)  # R10 au rang 3
    st.place_defender_reve_activation(s_e, 3, FACE_DEFINITIF, def_idx=0)

    st.set_parcel_nid(s_i, 2, 5, False)  # M5 sur p2-I avec 1 Insecte et 1 Défenseur
    st.set_parcel_insectes(s_i, 2, 1)
    st.place_defender_foret(s_i, 0, s_i, 2, FACE_DEFINITIF)

    st.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 3, 4, 3, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "R10_PLACE_INSECT":
            return ("NID", 5, s_i, 2)
        if "PASSER" in req.options:
            return "PASSER"
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE)
    assert st.get_player_hand(0)[4] == 0
    assert st.has_machine_alteration(2, MACHINE_ABATTEUSE)
    assert st.get_parcel_insectes(s_i, 2) == 2

    ins_before = st.get_parcel_insectes(s_i, 2)
    _drive(st, _choose, stop_step=STEP_4_3_MIGRATION)
    assert st.get_parcel_insectes(s_i, 2) - ins_before == 2


# ---------------------------------------------------------------------------
# Nids M1..M5 (7 témoins)
# ---------------------------------------------------------------------------


def test_witness_m1_t1() -> None:
    """M1_T1 (Fourmilière Coupe-Feuilles) : passager sur A_M complète parade p3-M (Seuil 3) -> TRIG_INSECTE, passager 0."""
    st = _make_state(("I", "M", "R", "O"), tour=2, step=STEP_4_2_NIDS)
    s_m = 1
    st.set_parcel_nid(s_m, 2, 1, False)  # M1 sur p2-M
    st.set_parcel_insectes(s_m, 2, 1)
    st.place_defender_foret(0, 0, s_m, 2, FACE_DEFINITIF)

    st.set_machine_pos_status(s_m, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.place_defender_foret(1, 0, s_m, 3, FACE_DEFINITIF)
    st.place_defender_foret(2, 0, s_m, 3, FACE_DEFINITIF)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "M1_EMBARK_INSECT":
            return MACHINE_ABATTEUSE
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_3_MIGRATION)
    assert st.get_machine_passenger_insects(s_m, MACHINE_ABATTEUSE) == 1

    st.step = STEP_5_1_TACTIQUES
    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_m, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_parcel_arbres(s_m, 3) == 3
    assert st.get_machine_passenger_insects(s_m, MACHINE_ABATTEUSE) == 0
    assert _trig_lit(trk, TRIG_INSECTE)


def test_witness_m2_t1() -> None:
    """M2_T1 (Termitière à Glu — Loi passive) : 2 Insectes défaussés en Parade sur M2 -> +2 Sabotages 6.3, TRIG_INSECTE."""
    st = _make_state(("I", "R", "M", "O"), tour=2, step=STEP_5_1_TACTIQUES)
    s_i = 0
    st.set_parcel_nid(s_i, 3, 2, False)  # M2 sur p3-I (dotation 3)
    st.place_defender_foret(s_i, 0, s_i, 3, FACE_DEFINITIF)
    st.set_parcel_insectes(s_i, 3, 2)
    st.set_machine_pos_status(s_i, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_i, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert st.get_parcel_arbres(s_i, 3) == 3
    assert st.sabotage_pending_count == 2
    assert _trig_lit(trk, TRIG_INSECTE)
    assert not _trig_lit(trk, TRIG_SABOTAGE)


def test_witness_m3_t1() -> None:
    """M3_T1 (Branche des Guêpes Cazadores — Loi passive) : Migration latérale p3-I -> p3-H (Plume H) -> parade p3-H."""
    st = _make_state(("I", "O", "H", "M"), tour=2, step=STEP_4_3_MIGRATION)
    s_i, s_h = 0, 2
    st.set_oiseau_plume(PLUME_CHAUD, PLUME_KIND_RAY, s_h, locked=True)
    st.set_parcel_nid(s_i, 3, 3, False)  # M3 sur p3-I
    st.set_parcel_insectes(s_i, 3, 3)

    st.set_parcel_arbres_souches(s_h, 3, 3, 1)
    st.place_defender_foret(s_h, 0, s_h, 3, FACE_DEFINITIF)
    st.place_defender_foret(3, 0, s_h, 3, FACE_DEFINITIF)
    st.set_machine_pos_status(s_h, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    moved_once = [False]

    def _choose(req: DecisionRequest) -> Any:
        if req.decision_type == DEC_MIGRATION_INSECTE_4_3 and not moved_once[0]:
            assert ("FORET", s_h, 3) in req.options
            moved_once[0] = True
            return ("FORET", s_h, 3)
        return ("RESTER",)

    _drive(st, _choose, stop_step=STEP_5_1_TACTIQUES)
    assert st.get_parcel_insectes(s_h, 3) == 1

    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_h, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1], telemetry=trk)
    assert (st.get_parcel_arbres(s_h, 3), st.get_parcel_souches(s_h, 3)) == (3, 1)
    assert _trig_lit(trk, TRIG_INSECTE)


def test_witness_m4_t1() -> None:
    """M4_T1 (Ruche des Mélipones — Tambour) : envoie 1 Insecte sur Tambour p4-E -> parade Devant (p4-E=3, TRIG_INSECTE)."""
    st = _make_state(("I", "H", "E", "M"), tour=2, step=STEP_4_2_NIDS)
    s_i, s_h, s_e = 0, 1, 2
    st.set_parcel_nid(s_i, 2, 4, False)  # M4 sur p2-I
    st.place_defender_foret(s_i, 0, s_i, 2, FACE_DEFINITIF)

    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_foret(s_h, 0, s_e, 4, FACE_DEFINITIF)
    st.set_machine_pos_status(s_e, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "M4_AFTER_PROD":
            return ("TAMBOUR", s_e, 4)
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_3_MIGRATION)
    assert st.get_parcel_insectes(s_e, 4) == 1

    st.step = STEP_5_1_TACTIQUES
    # T3 (SUR_PLACE p3-E + DEVANT p4-E, mod_seuil -1 -> Seuil 2 sur p3 et p4)
    trk = TelemetryTracker()
    resolve_single_machine_attack(st, s_e, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3], telemetry=trk)
    assert st.get_parcel_arbres(s_e, 4) == 3
    assert _trig_lit(trk, TRIG_INSECTE)


def test_witness_m4_t2() -> None:
    """M4_T2 (Ruche des Mélipones — Surchauffe) : production +1 -> défausse 1 Insecte -> 1 rouge retourné en bleu."""
    st = _make_state(("I", "H", "E", "M"), tour=2, step=STEP_4_2_NIDS)
    s_i, s_e = 0, 2
    st.set_parcel_nid(s_i, 2, 4, False)
    st.place_defender_foret(s_i, 0, s_i, 2, FACE_DEFINITIF)
    st.set_machine_tokens(s_e, MACHINE_ABATTEUSE, 1, 0)

    def _choose(req: DecisionRequest) -> Any:
        if req.context.get("effect_kind") == "M4_AFTER_PROD":
            return ("SURCHAUFFE", s_e, MACHINE_ABATTEUSE)
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_3_MIGRATION)
    assert st.get_machine_tokens(s_e, MACHINE_ABATTEUSE) == (0, 1)
    assert st.get_parcel_insectes(s_i, 2) == 0


def test_witness_m5_t1() -> None:
    """M5_T1 (Jardin du Diable — Enraciné) : p3-I (0A, 3S, 2 Insectes) -> 1 base + 2 Insectes = [3, 0] au décompte."""
    st = _make_state(("I", "E", "M", "R"), tour=8, step=STEP_5_1_TACTIQUES)
    s_i = 0
    slot_m5 = st.find_lisiere_slot_by_tile_id("M5")
    assert slot_m5 is not None
    st.set_parcel_arbres_souches(s_i, 3, 0, 3)
    st.set_parcel_insectes(s_i, 3, 2)
    st.root_tile_at_parcel(slot_m5, s_i, 3, tier_souches=1)

    apply_repousse_finale(st)
    assert (st.get_parcel_arbres(s_i, 3), st.get_parcel_souches(s_i, 3)) == (3, 0)


def test_witness_m5_t2() -> None:
    """M5_T2 (Jardin du Diable — déplacement Souche) : Insecte vers p2-E à Souche sauve la parcelle vs Route sans Insecte."""
    def _run_case(move_insect: bool) -> tuple[int, bool]:
        st = _make_state(("I", "E", "M", "R"), tour=2, step=STEP_4_2_NIDS)
        s_i, s_e = 0, 1
        st.set_parcel_nid(s_i, 2, 5, False)  # M5 sur p2-I
        st.place_defender_foret(s_i, 0, s_i, 2, FACE_DEFINITIF)
        st.set_parcel_arbres_souches(s_e, 2, 1, 1)
        st.place_defender_foret(s_e, 0, s_e, 2, FACE_DEFINITIF)
        st.set_machine_pos_status(s_e, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)

        def _choose(req: DecisionRequest) -> Any:
            if req.context.get("effect_kind") == "M5_MOVE_SOUCHE":
                return (s_e, 2) if move_insect else "PASSER"
            return req.options[0]

        _drive(st, _choose, stop_step=STEP_4_3_MIGRATION)
        st.step = STEP_5_1_TACTIQUES
        resolve_single_machine_attack(st, s_e, MACHINE_BULLDOZER, TACTIQUES_SPEC[1])
        total_veg = st.get_parcel_arbres(s_e, 2) + st.get_parcel_souches(s_e, 2)
        return total_veg, st.is_route_forestiere(s_e, 2)

    assert _run_case(True) == (2, False)
    assert _run_case(False) == (0, True)


def test_r1_overloaded_choice_and_chant_slide() -> None:
    """Vérifie le choix propriétaire de R1 en surcharge (rang propre + rang voisin vide) + glissement Chant."""
    st = _make_state(("H", "E", "M", "R"), tour=2, step=STEP_3_2_REVEAL)
    st.paravents_ouverts = False
    st.set_tactique_at_rank(3, TILE_R_BASE + 1)  # R1 au rang 4 ; rangs 3 et 5 sans Rêve
    st.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st.place_defender_reve_activation(0, 4, FACE_DEFINITIF, def_idx=0)  # 1 seul Défenseur (Chant)

    # 1 machine au rang 4 (propre) + 1 machine au rang 5 (voisin vide)
    st.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 4, 5, 4, 0)
    st.set_player_hand(1, machine_card_code(3, MACHINE_BULLDOZER), 5, 6, 5, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.set_player_hand(3, 0, 1, 2, 0, 0)

    saw_choice = [False]

    def _choose(req: DecisionRequest) -> Any:
        if req.decision_type == DEC_CHOIX_CIBLE_REVE_3_2:
            saw_choice[0] = True
            assert (0,) in req.options and (1,) in req.options
            return (0,)  # Annule la machine de son propre rang -> Chant glisse R1 en rang 3 !
        return req.options[0]

    _drive(st, _choose, stop_step=STEP_4_1_FURTIVITE)
    assert saw_choice[0]
    assert st.was_seat_cancelled_by_reve_this_turn(0)
    assert st.get_player_hand(1)[4] == 5  # Rang 5 non annulée -> bien liée à 5
    assert st.get_tactique_at_rank(2) == TILE_R_BASE + 1  # Chant a glissé R1 de 4 en 3 !


@pytest.mark.parametrize(
    "slot_id",
    [f"G{i}" for i in range(1, 16)]
    + [f"R{i}" for i in range(1, 11)]
    + [f"M{i}" for i in range(1, 6)],
)
def test_all_30_canon0_registered_profile_a(slot_id: str) -> None:
    from engine.effects.registry import get_tile_registration

    reg = get_tile_registration(slot_id, "A")
    assert reg is not None, f"Tuile Canon 0 non enregistrée : {slot_id}:A"
    assert len(reg.hooks) >= 1


def test_197_canonical_assises_and_lot0_canon0_crn_plans() -> None:
    from campaigns.designs import (
        BENCHMARK_ASSISE_KEYS,
        build_paired_197_calibration_configs,
        build_plan_canon0_197,
        build_plan_lot0_197,
        canonicalize_dihedral_assise,
        enumerate_197_canonical_assises,
    )

    assises = enumerate_197_canonical_assises()
    assert len(assises) == 197
    by_n = {n: [a for a in assises if a.n_players == n] for n in (3, 4, 5, 6)}
    assert {n: len(v) for n, v in by_n.items()} == {3: 20, 4: 45, 5: 72, 6: 60}
    assert len({a.key for a in assises}) == 197
    assert len({a.composition_key for a in assises}) == 42

    keys = {a.key for a in assises}
    for bk in BENCHMARK_ASSISE_KEYS:
        assert bk in keys, f"Table témoin manquante : {bk}"

    # Invariance diédrale (rotation + miroir)
    for a in assises[:25]:
        rot = a.peuples[1:] + a.peuples[:1]
        rev = tuple(reversed(a.peuples))
        assert canonicalize_dihedral_assise(rot)[0] == a.key
        assert canonicalize_dihedral_assise(rev)[0] == a.key

    plan_l0 = build_plan_lot0_197(reps_per_assise=2, exp_seed=777)
    plan_c0 = build_plan_canon0_197(reps_per_assise=2, exp_seed=777)
    paired = build_paired_197_calibration_configs(reps_per_assise=2, exp_seed=777)
    assert len(plan_l0) == 394 and len(plan_c0) == 394 and len(paired) == 394
    for a, c_l0, c_c0 in paired:
        assert c_l0.mode == 3 and c_c0.mode == 4
        assert c_l0.peuples == a.peuples and c_c0.peuples == a.peuples
        assert c_l0.exp_seed == c_c0.exp_seed == 777
        assert c_l0.rep_id == c_c0.rep_id
        active_slot = c_l0.lisiere_slots[0]
        assert dict(c_l0.tile_profiles)[active_slot] == "NEUTRE"
        assert c_l0.profile_for_slot(active_slot) is None
        assert c_c0.profile_for_slot(active_slot) == "A"


def test_verify_lot_anti_noop_guard_rejects_dummy_and_accepts_canon0() -> None:
    import verify_lot as vl
    from engine.primitives import HOOK_GARDIEN_OUVERTURE, _RegistryStore, register_tile

    canon_doc = json.loads((ROOT / "contracts" / "tiles_canon_v6_2.json").read_text(encoding="utf-8"))
    checked, errs = vl.check_active_tile_handlers_non_noop(canon_doc["tuiles_ciblees"])
    assert checked == 30 and errs == []

    # Vérifier que la garde rejette un handler no-op synthétique
    snap_k = dict(_RegistryStore.by_key)
    snap_h = {k: list(v) for k, v in _RegistryStore.by_hook.items()}
    try:

        @register_tile("G1", "DUMMY_NOOP", (HOOK_GARDIEN_OUVERTURE,))
        def _dummy_noop(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
            """Docstring uniquement."""
            _ = (state, hook, ctx)

        fake_tiles = {"G1": {"profils": {"DUMMY_NOOP": {"engine_sync_status": "ACTIVE_VERIFIED"}}}}
        cnt, bad_errs = vl.check_active_tile_handlers_non_noop(fake_tiles)
        assert cnt == 1
        assert len(bad_errs) == 1 and "no-op" in bad_errs[0]
    finally:
        _RegistryStore.by_key.clear()
        _RegistryStore.by_key.update(snap_k)
        _RegistryStore.by_hook.clear()
        _RegistryStore.by_hook.update(snap_h)

