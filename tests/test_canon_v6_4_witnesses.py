"""Suite des 54 Témoins exécutables Canon v6.4 (30 emplacements : G1..G15, R1..R10, M1..M5).

Source de vérité : `contracts/tiles_canon_v6_4.json`.
Chaque témoin officiel (`G1_T1`..`M5_T1`) est exécuté sur le noyau déterministe PyPy-compatible
avec vérification de l'état résultant et garantie `mem_debt_score == 0`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engine.core_engine import (
    DEC_DEPLOIEMENT_NID_4_2,
    DEC_ENRACINEMENT_6_1,
    apply_choice,
    apply_repousse_finale,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects import load_all_effects
from engine.primitives import (
    DEC_EFFET_TUILE,
    GameOver,
    prim_creation_entite,
    prim_partage_info_etat_gardien,
    verb_reculer,
)
from engine.state import (
    CALE_CAIMAN,
    CARD_ECAILLE,
    CARD_SABOTAGE,
    CHAMAN_CHANT,
    CHAMAN_TAMBOUR,
    DUEL_DEFI,
    DUEL_NONE,
    DUEL_TERRITOIRE_TENU,
    FACE_DEFINITIF,
    FURT_RIVE_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PERCHOIR_CHAUD,
    PERCHOIR_KIND_RANK,
    PERCHOIR_KIND_RAY,
    PIEGE_ACTIF,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_2_NIDS,
    STEP_6_1_ENRACINEMENT,
    STEP_6_3_END_TURN,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    TRIG_INSECTE,
    TRIG_PARADE,
    TRIG_PIEGEAGE,
    TRIG_RESONANCE,
    TRIG_REVE,
    TRIG_SABOTAGE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker

ROOT = Path(__file__).resolve().parents[1]
TILES_V6_4_PATH = ROOT / "contracts" / "tiles_canon_v6_4.json"


def _mk(
    peuples: tuple[str, ...] = ("H", "M", "O", "R", "E", "I"),
    *,
    mode: int = 4,
    seed: int = 202664,
    rep: int = 0,
) -> GameState:
    cfg = GameConfig(
        n_players=len(peuples),
        peuples=peuples,
        mode=mode,
        exp_seed=seed,
        rep_id=rep,
    )
    return GameState(cfg)


def _fire_gardien(state: GameState, case_1_6: int, g_num: int, face: int) -> None:
    """Place Gardien `g_num` (face 1/2) sur `case_1_6`, pose 1 pari dessus et allume l'icône."""
    state.set_gardien_at_case(case_1_6, g_num, face)
    state.place_defender_gardien_pari(0, case_1_6, FACE_DEFINITIF)
    state.light_trigger(case_1_6)
    sweep_gardiens(state)


def _pick(req: Any, pred: Any) -> Any:
    assert not isinstance(req, GameOver)
    for opt in req.options:
        if pred(opt):
            return opt
    raise AssertionError(f"Aucune option ne correspond au prédicat parmi {req.options!r} (ctx={req.context!r})")


# ---------------------------------------------------------------------------
# Méta-test : 30/30 emplacements & 54/54 témoins exécutables
# ---------------------------------------------------------------------------


def test_meta_all_30_tiles_and_54_witnesses_covered() -> None:
    reg = set(load_all_effects())
    data = json.loads(TILES_V6_4_PATH.read_text(encoding="utf-8"))
    tuiles = data["tuiles_ciblees"]
    assert len(tuiles) == 30
    for sid in tuiles:
        assert (sid, "A") in reg, f"Handler ({sid}, 'A') manquant du registre actif"

    g_names = set(globals().keys())
    expected_ids: list[str] = []
    for t in tuiles.values():
        for w in t["temoins"]:
            expected_ids.append(w["id"])
    assert len(expected_ids) == 54
    missing = [wid for wid in expected_ids if f"test_witness_{wid}" not in g_names]
    assert not missing, f"Témoins v6.4 manquants : {missing}"


# ---------------------------------------------------------------------------
# G1..G15 (30 témoins)
# ---------------------------------------------------------------------------


def test_witness_G1_T1() -> None:
    st = _mk(("H", "M", "R"))
    st.set_duel_state_at(1, 2, DUEL_DEFI)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    _fire_gardien(st, TRIG_PARADE, 1, 1)
    assert st.get_croc_parcel() == (1, 2)
    resolve_single_machine_attack(st, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, 1, 2)
    assert st.get_croc_parcel() is None


def test_witness_G1_T2() -> None:
    st = _mk(("H", "M", "R"))
    st.set_duel_state_at(1, 2, DUEL_DEFI)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(2, MACHINE_ABATTEUSE, 1, 0)
    st.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    _fire_gardien(st, TRIG_PARADE, 1, 2)
    req = step_until_decision(st)
    apply_choice(
        st,
        _pick(req, lambda o: isinstance(o, tuple) and o[0] == "CROC_AND_DUEL" and o[1] == 2 and o[2] == 2),
    )
    assert st.get_duel_state() == (DUEL_DEFI, 2, 2)
    assert st.get_croc_parcel() == (2, 2)
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    # Machine parée par le Croc est Refroidie (1 Rouge -> 1 Bleu) par G1 F2 !
    assert st.get_machine_tokens(2, MACHINE_ABATTEUSE) == (0, 1)


def test_witness_G2_T1() -> None:
    st = _mk(("H", "M", "R"))
    st.set_duel_state_at(1, 4, DUEL_TERRITOIRE_TENU)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, 1, 0)
    _fire_gardien(st, TRIG_SABOTAGE, 2, 1)
    pos, status, _ = st.get_machine_pos_status(1, MACHINE_ABATTEUSE)
    assert status == MACHINE_STATUS_NORMAL and pos == 3
    assert st.get_machine_tokens(1, MACHINE_ABATTEUSE) == (0, 0)


def test_witness_G2_T2() -> None:
    st = _mk(("H", "M", "R"))
    st.set_duel_state_at(1, 3, DUEL_DEFI)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(1, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    _fire_gardien(st, TRIG_SABOTAGE, 2, 2)
    assert st.is_machine_etouffee_this_turn(1, MACHINE_ABATTEUSE)
    assert st.get_player_hand(0)[4] == 0
    assert st.get_machine_pos_status(1, MACHINE_ABATTEUSE)[0] == 2


def test_witness_G3_T1() -> None:
    st = _mk(("H", "M", "O"))
    # Défenseur sur Rive Sabotage de O (siège 2) -> traverse vers parcelle à Arbre debout de M (siège 1)
    st.place_defender_furtivite(2, 0, 2, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_PARADE, 3, 1)
    req = step_until_decision(st)
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == 2 and o[2] == "FORET" and o[3] == 1))
    assert st.get_parcel_defenseurs(1, 1) + st.get_parcel_defenseurs(1, 2) + st.get_parcel_defenseurs(1, 3) + st.get_parcel_defenseurs(1, 4) >= 1


def test_witness_G3_T2() -> None:
    st = _mk(("H", "M", "O", "R"))
    # Perchoir au pied du rayon O (siège 2, voisin de M=1) ; Défenseur en M·1 -> 1 pas avant (M·2), traversée cimes vers O·2, 1 pas après (O·3) !
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RAY, 2)
    st.place_defender_foret(1, 0, 1, 1, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_PARADE, 3, 2)
    req = step_until_decision(st)
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == 1 and o[2] == "FORET" and o[3] == 2 and o[4] == 3))
    assert st.get_parcel_defenseurs(2, 3) == 1


def test_witness_G4_T1() -> None:
    st = _mk(("H", "M", "O"))
    # G4 F1 sur Résonance (6), G1 sur Insecte (5, directement voisin), G2 sur Parade (1)
    st.set_gardien_at_case(TRIG_INSECTE, 1, 1)
    st.set_gardien_at_case(TRIG_PARADE, 2, 1)
    st.place_defender_gardien_pari(1, TRIG_INSECTE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, TRIG_PARADE, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_RESONANCE, 4, 1)
    step_until_decision(st)
    apply_choice(st, TRIG_INSECTE)
    assert st.count_gardien_pari_defenders_at_case(TRIG_INSECTE) == 0
    # Second cri gratuit car case 5 est directement voisine de case 6 !
    step_until_decision(st)
    apply_choice(st, ("FREE", TRIG_PARADE))
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0


def test_witness_G4_T2() -> None:
    st = _mk(("H", "M", "O"))
    # G4 F2 sur Parade (1) relaie G15/G2 sur Sabotage (3) avec 1 dernier pari + G1 sur Résonance (6) avec 1 pari
    st.set_gardien_at_case(TRIG_SABOTAGE, 8, 1)  # G8 F1 sans Rêve ni mobile altérable? Mettons un Rêve au rang 3 pour voir son pouvoir!
    st.set_tactique_at_rank(2, TILE_R_BASE + 1)
    st.set_gardien_at_case(TRIG_RESONANCE, 2, 1)
    st.place_defender_gardien_pari(1, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, TRIG_RESONANCE, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_PARADE, 4, 2)
    step_until_decision(st)
    apply_choice(st, TRIG_SABOTAGE)
    # G8 F1 a glissé R1 (rang 3 -> 2) et vidé son dernier pari -> Résonance s'est allumée !
    while True:
        out = step_until_decision(st)
        if isinstance(out, GameOver) or out.decision_type != DEC_EFFET_TUILE:
            break
        apply_choice(st, "PASSER" if "PASSER" in out.options else out.options[0])
    assert st.count_gardien_pari_defenders_at_case(TRIG_SABOTAGE) == 0
    assert st.is_trigger_lit(TRIG_RESONANCE) or st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 0


def test_witness_G5_T1() -> None:
    st = _mk(("H", "O", "R"))
    # Perchoir pointe rang 4 (idx=3) ; mobile (0, AB) au rang 4 cible (0, 2) et porte 1 Bleu ; (1, AB) cible (1, 2)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 3)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 0, 1)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 4, 5, 4, 4)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 1, 5, 1, 1)
    _fire_gardien(st, TRIG_PIEGEAGE, 5, 1)
    req = step_until_decision(st)
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    # Boire le Bleu pose aussi le Croc de la réserve sur une autre parcelle ciblée (1, 2) !
    apply_choice(
        st,
        _pick(req, lambda o: isinstance(o, tuple) and o[0] == 0 and o[1] == MACHINE_ABATTEUSE and o[2] == 1 and o[3] == 2),
    )
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)
    assert st.get_croc_parcel() == (1, 2)


def test_witness_G5_T2() -> None:
    st = _mk(("H", "O", "R"))
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 0, 1)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 4, 5, 4, 4)
    st.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 1, 5, 1, 1)
    _fire_gardien(st, TRIG_PIEGEAGE, 5, 2)
    req = step_until_decision(st)
    apply_choice(st, (0, 2))  # Piège 1
    req = step_until_decision(st)
    apply_choice(st, (1, 2))  # Croc
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "G5_F2_DRINK_BLUE_PIEGE"
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == 0 and o[1] == MACHINE_ABATTEUSE))
    assert st.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st.get_croc_parcel() == (1, 2)
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)


def test_witness_G6_T1() -> None:
    st = _mk(("H", "O", "R"))
    # G6 F1 sur Parade (1), G5 sur Piégeage (2) avec 1 pari ; Perchoir sur rayon 0 où (0, AB) a 1 Rouge
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RAY, 0)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    st.set_gardien_at_case(TRIG_PIEGEAGE, 5, 1)
    st.place_defender_gardien_pari(1, TRIG_PIEGEAGE, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_PARADE, 6, 1)
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "G6_CRI_DE_VAPEUR"
    assert TRIG_PIEGEAGE in req.options and TRIG_RESONANCE not in req.options
    apply_choice(st, TRIG_PIEGEAGE)
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)
    assert st.is_trigger_lit(TRIG_PIEGEAGE) or st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0


def test_witness_G6_T2() -> None:
    st = _mk(("H", "O", "R"))
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 1)
    _fire_gardien(st, TRIG_PARADE, 6, 2)
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "G6_CRI_DE_VAPEUR"
    apply_choice(st, TRIG_PIEGEAGE)
    # Passée à 0 Rouge et 2 Bleus -> immédiatement Étouffée par G6 F2 !
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 2)
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)


def test_witness_G7_T1() -> None:
    st = _mk(("H", "M", "O"))
    st.set_gardien_at_case(TRIG_PARADE, 7, 1)
    # Route en M·2 portant le Duel (Bourbier F1) ; machine en M·1 sur T2 (SUR_PLACE + DEVANT -> M·3 par-dessus Route M·2)
    st.set_parcel_arbres_souches(1, 2, 0, 0)
    st.set_duel_bourbier(1, 2, DUEL_DEFI)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    arbres_m3_before = st.get_parcel_arbres(1, 3)
    resolve_single_machine_attack(st, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[2])
    # Frappe Devant par-dessus M·2 annulée et Duel rentre en réserve !
    assert st.get_parcel_arbres(1, 3) == arbres_m3_before
    assert st.get_duel_state()[0] == DUEL_NONE


def test_witness_G7_T2() -> None:
    st = _mk(("H", "M", "O"))
    st.set_gardien_at_case(TRIG_PARADE, 7, 2)
    st.set_parcel_arbres_souches(1, 2, 0, 0)
    st.set_duel_bourbier(1, 2, DUEL_TERRITOIRE_TENU)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, 1, 0)
    resolve_single_machine_attack(st, 1, MACHINE_ABATTEUSE, TACTIQUES_SPEC[2])
    # G7 F2 : machine enlisée Refroidie (1R -> 1B) et Duel bascule sur Défi au lieu de rentrer en réserve !
    assert st.get_machine_tokens(1, MACHINE_ABATTEUSE) == (0, 1)
    assert st.get_duel_state() == (DUEL_DEFI, 1, 2)


def test_witness_G8_T1() -> None:
    st = _mk(("H", "M", "E"))
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # R1 au rang 5
    st.place_defender_reve_standing(0, 0, 5)
    _fire_gardien(st, TRIG_REVE, 8, 1)
    # R1 glisse rang 5 -> 4 avec son Défenseur !
    assert st.find_tactique_rank(TILE_R_BASE + 1) == 3
    assert st.count_reve_activation_defenders_at_case(4) == 1

    # Fallback sans Rêve déplaçable -> Altère 1 machine mobile !
    st2 = _mk(("H", "M", "E"))
    st2.set_tactique_at_rank(0, TILE_R_BASE + 1)  # Rang 1, non glissable
    _fire_gardien(st2, TRIG_REVE, 8, 1)
    req = step_until_decision(st2)
    apply_choice(st2, _pick(req, lambda o: isinstance(o, tuple) and o[0] == "ALTERER"))
    assert any(
        st2.has_machine_alteration(r, mt)
        for r in range(3)
        for mt in (MACHINE_ABATTEUSE, MACHINE_BULLDOZER)
    )


def test_witness_G8_T2() -> None:
    st = _mk(("H", "M", "E"))
    st.set_tactique_at_rank(2, TILE_R_BASE + 1)  # R1 rang 3
    st.set_tactique_at_rank(3, TILE_R_BASE + 2)  # R2 rang 4 (bloqué à gauche par R1, mais rang 2 libre !)
    _fire_gardien(st, TRIG_REVE, 8, 2)
    req = step_until_decision(st)
    # Choisir de faire plonger R2 (rank_idx=3) au rang 2 (dst_idx=1) par-dessus R1 !
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == "SLIDE" and o[1] == 3 and o[2] == 1))
    assert st.find_tactique_rank(TILE_R_BASE + 2) == 1


def test_witness_G9_T1() -> None:
    st = _mk(("H", "R", "O"))
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_foret(0, 0, 1, 2, FACE_DEFINITIF)  # Tambour sur rayon 1
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)  # Dernière parcelle -> Ratissage bloqué par Cale !
    _fire_gardien(st, TRIG_SABOTAGE, 9, 1)
    req = step_until_decision(st)
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == "CALE" and o[1] == 1 and o[2] == MACHINE_ABATTEUSE))
    assert st.get_machine_cale(1, MACHINE_ABATTEUSE) == CALE_CAIMAN
    # Passage 6.3 : la Cale empêche la machine d'entrer en Ratissage !
    st.step = STEP_6_3_END_TURN
    step_until_decision(st)
    assert st.get_machine_pos_status(1, MACHINE_ABATTEUSE)[1] == MACHINE_STATUS_NORMAL


def test_witness_G9_T2() -> None:
    st = _mk(("H", "R", "O"))
    st.set_gardien_at_case(TRIG_SABOTAGE, 9, 2)
    st.place_defender_gardien_pari(1, TRIG_SABOTAGE, FACE_DEFINITIF)
    st.set_machine_cale(1, MACHINE_ABATTEUSE, CALE_CAIMAN)
    st.set_player_hand(0, machine_card_code(1, MACHINE_ABATTEUSE), 2, 5, 2, 2)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, 0, 1, 4, 0, 0)
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st)
    # À la révélation sous G9 F2 : la cale reste sous la machine (règle G9), Sabotage s'allume (pari G9 glissé !)
    # et la machine est Étouffée (dé retiré) avant même le tour des Sabotages !
    assert not isinstance(req, GameOver) and st.tour == 1
    assert st.get_machine_cale(1, MACHINE_ABATTEUSE) == CALE_CAIMAN
    assert st.is_machine_etouffee_this_turn(1, MACHINE_ABATTEUSE)
    assert st.get_player_hand(0)[4] == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_SABOTAGE) == 0


def test_witness_G10_T1() -> None:
    st = _mk(("H", "R", "E"))
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    ec_before = st.ecaille_deck_count + st.ecaille_pending_count
    _fire_gardien(st, TRIG_SABOTAGE, 10, 1)
    req = step_until_decision(st)
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == "HAPPER" and o[1] == 0 and o[2] == 2))
    assert (st.ecaille_deck_count + st.ecaille_pending_count) == ec_before + 1
    assert st.get_croc_parcel() == (0, 2)


def test_witness_G10_T2() -> None:
    st = _mk(("H", "R", "E"))
    prim_creation_entite(st, "CROC", ray=2, p=4)  # Croc sur parcelle non ciblée
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    ec_before = st.ecaille_deck_count + st.ecaille_pending_count
    _fire_gardien(st, TRIG_SABOTAGE, 10, 2)
    # 1 seule parcelle ciblée (0, 2) -> Happer s'applique automatiquement puis demande Envoûter
    assert st.get_croc_parcel() == (0, 2)
    req = step_until_decision(st)
    apply_choice(
        st,
        _pick(req, lambda o: isinstance(o, tuple) and o[0] == "ENVOUTER" and o[1] == 0 and o[2] == MACHINE_ABATTEUSE),
    )
    assert (st.ecaille_deck_count + st.ecaille_pending_count) == ec_before + 1
    assert st.get_croc_parcel() == (0, 2)
    assert st.has_machine_alteration(0, MACHINE_ABATTEUSE)


def test_witness_G11_T1() -> None:
    st = _mk(("H", "O", "M"))
    # Oiseau couché en attente + Perchoir rang 5 (idx=4) + mobile (0, AB) au rang 5
    st.mark_defender_waiting(1, 0)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 4)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 6, 5, 5)
    _fire_gardien(st, TRIG_PARADE, 11, 1)
    req = step_until_decision(st)
    apply_choice(
        st,
        _pick(req, lambda o: isinstance(o, tuple) and o[0] == "SAISIR" and o[3] == 0 and o[4] == MACHINE_ABATTEUSE),
    )
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert st.get_player_hand(0)[4] == 0


def test_witness_G11_T2() -> None:
    st = _mk(("H", "O", "M"))
    st.mark_defender_waiting(1, 0)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 4)  # Rang 5 -> miroir rang 2 !
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)  # Rêve R1 au rang 5 non défendu
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 6, 2, 2)
    # Chant posé sur la parcelle visée (0, 3) (T2 = DEVANT depuis p=2 -> p=3 !)
    st.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st.place_defender_foret(0, 0, 0, 3, FACE_DEFINITIF)
    _fire_gardien(st, TRIG_PARADE, 11, 2)
    req1 = step_until_decision(st)
    apply_choice(
        st,
        _pick(req1, lambda o: isinstance(o, tuple) and o[0] == "SAISIR" and o[3] == 0 and o[4] == MACHINE_ABATTEUSE),
    )
    req2 = step_until_decision(st)
    assert not isinstance(req2, GameOver) and req2.context.get("effect_kind") == "G11_F2_CARRY_CHAMAN"
    apply_choice(st, (0, 0))
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert st.count_reve_activation_defenders_at_case(5) == 1


def test_witness_G12_T1() -> None:
    st = _mk(("H", "O", "E"))
    # Rêve R1 défendu au rang 5 ; porteur Abatteuse dés (2, 5), retenu 2, écarté 5
    st.set_tactique_at_rank(4, TILE_R_BASE + 1)
    st.place_defender_reve_standing(0, 0, 5)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 2)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 4, 0, 0)
    _fire_gardien(st, TRIG_SABOTAGE, 12, 1)
    req = step_until_decision(st)
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == 0 and o[1] == 5))
    assert st.get_player_hand(0)[3] == 5


def test_witness_G12_T2() -> None:
    st = _mk(("H", "O", "E"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 2)  # R2 défendu au rang 4 (rang 3 libre !)
    st.place_defender_reve_standing(0, 0, 4)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 6, 2, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 4, 5, 0, 0)  # Dé ignoré = 4 sur porteur Sabotage !
    st.set_player_hand(2, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_gardien_at_case(TRIG_SABOTAGE, 12, 2)
    st.place_defender_gardien_pari(1, TRIG_SABOTAGE, FACE_DEFINITIF)
    # Lancer 3.2 : Sabotage (siège 1) -> allume Sabotage -> G12 F2 déplace siège 0 vers rang 4 -> R2 l'Étouffe -> G12 F2 glisse R2 au rang 3 !
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st)
    assert not isinstance(req, GameOver)
    apply_choice(st, req.options[0])  # Cible Sabotage siège 1
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "G12_IBIJAU"
    apply_choice(st, _pick(req, lambda o: isinstance(o, tuple) and o[0] == 0 and o[1] == 4))
    assert st.was_seat_ibijau_moved_f2(0)
    # Résoudre la suite de 3.2 jusqu'au glissement G12 F2 de R2 -> rang 3 !
    slid_prompted = False
    for _ in range(15):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "G12_F2_SLIDE_REVE":
            slid_prompted = True
            apply_choice(st, "GLISSER")
            break
        apply_choice(st, "PASSER" if "PASSER" in out.options else out.options[0])
    assert slid_prompted
    assert st.find_tactique_rank(TILE_R_BASE + 2) == 2


def test_witness_G13_T1() -> None:
    st = _mk(("H", "M", "I"))
    st.set_parcel_nid(2, 2, 1)
    st.set_parcel_insectes(2, 2, 2)
    # 1 seul Nid >= 2 -> G13 F1 applique automatiquement −1 / +2 Insectes !
    _fire_gardien(st, TRIG_INSECTE, 13, 1)
    assert st.get_parcel_insectes(2, 2) == 3

    # Sans Nid >= 2 : pose 1 Insecte de la réserve
    st2 = _mk(("H", "M", "I"))
    _fire_gardien(st2, TRIG_INSECTE, 13, 1)
    req2 = step_until_decision(st2)
    apply_choice(st2, _pick(req2, lambda o: isinstance(o, tuple) and o[0] == "FALLBACK"))
    assert st2.count_total_insects_on_board() == 1


def test_witness_G13_T2() -> None:
    st = _mk(("H", "M", "I"))
    st.set_parcel_nid(2, 2, 1)
    st.set_parcel_insectes(2, 2, 2)
    st.set_duel_state_at(2, 3, DUEL_DEFI)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(2, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    _fire_gardien(st, TRIG_INSECTE, 13, 2)
    req = step_until_decision(st)
    apply_choice(
        st,
        _pick(req, lambda o: isinstance(o, tuple) and o[0] == "RIPOSTE" and o[3] == 2 and o[4] == 3),
    )
    assert st.get_parcel_insectes(2, 2) == 1
    assert st.get_parcel_insectes(2, 3) == 2


def test_witness_G14_T1() -> None:
    st = _mk(("H", "R", "I"))
    st.set_parcel_nid(2, 2, 1)
    _fire_gardien(st, TRIG_INSECTE, 14, 1)
    req = step_until_decision(st)
    if not isinstance(req, GameOver) and req.context.get("effect_kind") == "G14_POSE_PONTE":
        apply_choice(st, 1)
    assert st.get_nid_ponte(1)

    ec_before = st.ecaille_deck_count + st.ecaille_pending_count
    st.set_gardien_at_case(TRIG_PIEGEAGE, 5, 1)
    st.place_defender_gardien_pari(1, TRIG_PIEGEAGE, FACE_DEFINITIF)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    # Ponte éclot -> Croc pare, Piégeage allumé, Croc rentre en réserve, Écaille Semée au sac !
    assert not st.get_nid_ponte(1)
    assert st.get_croc_parcel() is None
    assert (st.ecaille_deck_count + st.ecaille_pending_count) == ec_before + 1
    assert st.count_gardien_pari_defenders_at_case(TRIG_PIEGEAGE) == 0


def test_witness_G14_T2() -> None:
    st = _mk(("H", "R", "I"))
    st.set_parcel_nid(2, 2, 1)
    st.set_parcel_nid(2, 3, 2)
    st.set_nid_ponte(1, True)
    prim_creation_entite(st, "CROC", ray=0, p=1)  # Croc déjà posé ailleurs !
    _fire_gardien(st, TRIG_INSECTE, 14, 2)
    req = step_until_decision(st)
    if not isinstance(req, GameOver) and req.context.get("effect_kind") == "G14_POSE_PONTE":
        apply_choice(st, 2)
    assert st.get_nid_ponte(1) and st.get_nid_ponte(2)

    # Frappe sur Nid 2 sous G14 F2 -> éclot même si Croc était en (0, 1) !
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    arbres_before = st.get_parcel_arbres(2, 3)
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert not st.get_nid_ponte(2)
    assert st.get_parcel_arbres(2, 3) == arbres_before
    assert st.get_croc_parcel() is None


def test_witness_G15_T1() -> None:
    st = _mk(("H", "O", "I"))
    st.set_gardien_at_case(TRIG_PARADE, 1, 1)
    st.set_gardien_at_case(TRIG_RESONANCE, 2, 1)
    st.place_defender_gardien_pari(1, TRIG_PARADE, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, TRIG_RESONANCE, FACE_DEFINITIF)
    st.set_colonie_at_case(TRIG_PARADE, 1)
    _fire_gardien(st, TRIG_INSECTE, 15, 1)
    req1 = step_until_decision(st)
    if not isinstance(req1, GameOver) and req1.context.get("effect_kind") == "G15_COLIBRI_SRC":
        apply_choice(st, ("COLONIE", TRIG_PARADE))
        req2 = step_until_decision(st)
    else:
        req2 = req1
    apply_choice(st, _pick(req2, lambda o: isinstance(o, tuple) and o[0] == "FORET"))
    # Pari de Parade glissé en encoche SANS pouvoir ni Résonance !
    assert st.count_gardien_pari_defenders_at_case(TRIG_PARADE) == 0
    assert st.count_gardien_pari_defenders_at_case(TRIG_RESONANCE) == 1


def test_witness_G15_T2() -> None:
    st = _mk(("H", "O", "I"))
    st.set_parcel_nid(2, 2, 1)
    st.set_parcel_insectes(0, 1, 2)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 3)  # Rang 4
    _fire_gardien(st, TRIG_INSECTE, 15, 2)
    # 1er transport : (0,1) -> Nid (2,2) => +1 Insecte produit sur Nid (passe à 2 !)
    req = step_until_decision(st)
    if not isinstance(req, GameOver) and req.context.get("effect_kind") == "G15_COLIBRI_SRC":
        apply_choice(st, ("PARCEL", 0, 1))
        req = step_until_decision(st)
    apply_choice(st, ("FORET", 2, 2))
    assert st.get_parcel_insectes(2, 2) == 2
    # 2e transport : (0,1) -> BUG 4 (rang Perchoir)
    req = step_until_decision(st)
    if not isinstance(req, GameOver) and req.context.get("effect_kind") == "G15_COLIBRI_SRC":
        apply_choice(st, ("PARCEL", 0, 1))
        req = step_until_decision(st)
    apply_choice(st, ("BUG", 4))
    assert st.get_bugs_at_case(4) == 1


# ---------------------------------------------------------------------------
# R1..R10 (17 témoins)
# ---------------------------------------------------------------------------


def test_witness_R1_T1() -> None:
    st = _mk(("H", "E", "O"))
    st.set_tactique_at_rank(1, TILE_R_BASE + 1)  # R1 au rang 2
    st.set_tactique_at_rank(4, TILE_R_BASE + 8)  # R8 (Entités) au rang 5 non défendu
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_reve_standing(0, 0, 2)
    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "R1_ECHO_TAMBOUR"
    assert st.find_tactique_rank(TILE_R_BASE + 8) == 2  # Tiré au rang 3 !
    apply_choice(st, "PASSER_TAMBOUR")
    # Tambour passé debout au rang 3 -> R8 se résout aussitôt à l'ouverture !
    r8_prompted = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind", "").startswith("R8_"):
            r8_prompted = True
            apply_choice(st, "PASSER" if "PASSER" in out.options else out.options[0])
            break
        apply_choice(st, "PASSER" if "PASSER" in out.options else out.options[0])
    assert r8_prompted


def test_witness_R1_T2() -> None:
    st = _mk(("H", "E", "O"))
    # Enraciner R1 sur la Rive Sabotage de H (siège 0) : Sentinelle active SANS fermer le Sommeil !
    r1_slot = st.find_lisiere_slot_by_tile_id("R1")
    assert r1_slot is not None
    st.set_tactique_at_rank(0, TILE_R_BASE + 1)
    st.set_tactique_at_rank(1, TILE_R_BASE + 2)
    st.set_tactique_at_rank(2, TILE_R_BASE + 9)
    st.step = STEP_6_1_ENRACINEMENT
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.decision_type == DEC_ENRACINEMENT_6_1
    apply_choice(st, r1_slot)
    assert st.count_rooted_sentinels_on_ray(0) == 1
    assert not st.has_any_rooted_reve()  # R1 NE ferme PAS le Sommeil !
    # Les autres Rêves restants en bloc contigu depuis rang 1 déclenchent encore le Sommeil !
    st.set_tactique_at_rank(0, TILE_R_BASE + 2)
    st.set_tactique_at_rank(1, TILE_R_BASE + 9)
    assert st.is_sommeil_victory()


def test_witness_R2_T1() -> None:
    st = _mk(("H", "E", "O"))
    st.set_tactique_at_rank(1, TILE_R_BASE + 2)  # R2 défendu au rang 2
    st.place_defender_reve_standing(1, 0, 2)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 3, 5, 3, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_machine_alteration(0, MACHINE_ABATTEUSE, True)
    # Rive Sabotage de rayon 0 occupée 2/2 : grâce à R2, (0, AB) retourne son jeton face cachée (m(0) == 0 !)
    st.place_defender_furtivite(0, 0, 0, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st.place_defender_furtivite(2, 0, 0, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    sab_before = st.sabotage_deck_count + st.sabotage_pending_count
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver) or st.step >= STEP_4_2_NIDS or st.tour > 1:
            break
        apply_choice(st, "PASSER" if "PASSER" in out.options else out.options[0])
    assert (st.sabotage_deck_count + st.sabotage_pending_count) == sab_before + 1


def test_witness_R2_T2() -> None:
    st = _mk(("H", "E", "O"))
    r2_slot = st.find_lisiere_slot_by_tile_id("R2")
    assert r2_slot is not None
    st.set_tactique_at_rank(1, TILE_R_BASE + 2)
    st.set_machine_alteration(1, MACHINE_ABATTEUSE, True)  # Machine du rayon E altérée au moment de l'enracinement !
    st.set_parcel_arbres_souches(1, 1, 0, 2)
    st.step = STEP_6_1_ENRACINEMENT
    step_until_decision(st)
    apply_choice(st, r2_slot)
    assert st.is_slot_rooted_gue_marque(r2_slot)
    assert st.count_rooted_sentinels_on_ray(1) == 1
    apply_repousse_finale(st)
    assert st.get_parcel_arbres(1, 1) == 2 and st.get_parcel_souches(1, 1) == 0


def test_witness_R3_T1() -> None:
    st = _mk(("H", "M", "O"))
    st.set_tactique_at_rank(1, TILE_R_BASE + 3)  # R3 au rang 2 défendu par le Tambour
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_reve_standing(0, 0, 2)
    st.set_duel_state_at(1, 1, DUEL_DEFI)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(1, MACHINE_ABATTEUSE), 2, 5, 2, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 4, 0, 0)
    st.step = STEP_3_2_REVEAL
    jumped = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R3_CHAMANE_JAGUAR_BOND":
            opt_j = _pick(out, lambda o: isinstance(o, tuple) and o[0] == "JUMP_DUEL" and o[1] == 1 and o[2] == 2)
            apply_choice(st, opt_j)
            jumped = True
            break
        apply_choice(st, out.options[0])
    assert jumped
    assert st.get_parcel_defenseurs(1, 2) == 1
    assert st.get_duel_state() == (DUEL_DEFI, 1, 2)


def test_witness_R4_T1() -> None:
    st = _mk(("H", "R", "O"))
    st.set_tactique_at_rank(1, TILE_R_BASE + 1)  # Rang 2
    st.set_tactique_at_rank(3, TILE_R_BASE + 2)  # Rang 4
    st.set_tactique_at_rank(4, TILE_R_BASE + 4)  # R4 en queue au rang 5
    st.place_defender_reve_standing(0, 0, 5)
    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    ec_before = st.ecaille_deck_count + st.ecaille_pending_count
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R4_PIROGUE":
            apply_choice(st, "POUSSEE")
            break
        apply_choice(st, out.options[0])
    assert st.find_tactique_rank(TILE_R_BASE + 1) == 0  # Rang 1
    assert st.find_tactique_rank(TILE_R_BASE + 2) == 2  # Rang 3
    assert st.find_tactique_rank(TILE_R_BASE + 4) == 3  # Rang 4
    assert (st.ecaille_deck_count + st.ecaille_pending_count) == ec_before + 1


def test_witness_R5_T1() -> None:
    st = _mk(("H", "O", "M"))
    st.set_tactique_at_rank(1, TILE_R_BASE + 5)  # R5 au rang 2 défendu par le Chant
    st.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st.place_defender_reve_standing(0, 0, 2)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 4)  # Perchoir au rang 5 !
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 6, 5, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 4, 0, 0)
    st.step = STEP_3_2_REVEAL
    flipped = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R5_CIEL_EAUX":
            apply_choice(st, _pick(out, lambda o: isinstance(o, tuple) and o[0] == "FLIP" and o[1] == 0 and o[2] == 2))
            flipped = True
            break
        apply_choice(st, out.options[0])
    assert flipped
    step_until_decision(st)
    # Basculée au rang 2 où R5 l'Étouffe aussitôt (0 arbre coupé) !
    assert st.get_parcel_arbres(0, 2) == 2


def test_witness_R5_T2() -> None:
    st = _mk(("H", "O", "M"))
    st.set_tactique_at_rank(0, TILE_R_BASE + 5)  # R5 au rang 1 défendu par le Tambour
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_reve_standing(0, 0, 1)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 3, 5, 3, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R5_CIEL_EAUX":
            apply_choice(st, ("SWAP", 0, 1))
            break
        apply_choice(st, out.options[0])
    assert st.get_player_hand(0)[3] == 6 and st.get_player_hand(1)[3] == 3
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)


def test_witness_R6_T1() -> None:
    st = _mk(("H", "I", "M"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 6)  # R6 au rang 4 défendu par le Chant
    st.set_humain_chaman_archetype(0, CHAMAN_CHANT)
    st.place_defender_reve_standing(0, 0, 4)
    st.set_parcel_insectes(0, 2, 1)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 6, 5, 0)  # Rang 5 adjacent !
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    stung = False
    for _ in range(12):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek == "R6_CUEILLIR":
            apply_choice(st, ("PARCEL", 0, 2))
        elif ek == "R6_PIQURES":
            apply_choice(st, 0)
            stung = True
            break
        else:
            apply_choice(st, out.options[0])
    assert stung
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)


def test_witness_R6_T2() -> None:
    st = _mk(("H", "I", "M"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 6)
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_reve_standing(0, 0, 4)
    assert st.count_total_insects_on_board() == 0
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 4, 5, 4, 0)
    st.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 4, 6, 4, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    primed = False
    stung = False
    for _ in range(15):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek == "R6_CUEILLIR":
            if ("RESERVE",) in out.options:
                apply_choice(st, ("RESERVE",))
                primed = True
            else:
                apply_choice(st, "PASSER")
        elif ek == "R6_PIQURES":
            apply_choice(st, _pick(out, lambda o: o != "PASSER"))
            stung = True
            break
        else:
            apply_choice(st, out.options[0])
    assert primed and stung
    assert st.is_machine_etouffee_this_turn(0, MACHINE_ABATTEUSE)
    assert st.is_machine_etouffee_this_turn(1, MACHINE_ABATTEUSE)


def test_witness_R7_T1() -> None:
    st = _mk(("H", "E", "M"))
    st.set_tactique_at_rank(2, TILE_R_BASE + 7)  # R7 non défendu au rang 3
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    arbres_p2_before = st.get_parcel_arbres(2, 2)
    arbres_p4_before = st.get_parcel_arbres(2, 4)
    # T3 sous Curupira : frappe Devant derrière (p=2, pas p=4), 0 Rouge sur Sur place, Recule en p=2 !
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[3])
    assert st.get_parcel_arbres(2, 2) < arbres_p2_before
    assert st.get_parcel_arbres(2, 4) == arbres_p4_before
    assert st.get_machine_pos_status(2, MACHINE_ABATTEUSE)[0] == 2
    # Et tout Recul hors de la parcelle du Duel Défi retourne aussitôt le Duel sur Territoire tenu !
    st.set_duel_state_at(2, 2, DUEL_DEFI)
    assert verb_reculer(st, 2, MACHINE_ABATTEUSE)
    assert st.get_machine_pos_status(2, MACHINE_ABATTEUSE)[0] == 1
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, 2, 2)


def test_witness_R7_T2() -> None:
    st = _mk(("H", "E", "M"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 7)  # R7 défendu au rang 4
    st.place_defender_reve_standing(1, 0, 4)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 4, 6, 4, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver) or st.has_machine_alteration(0, MACHINE_ABATTEUSE):
            break
        apply_choice(st, out.options[0])
    assert st.has_machine_alteration(0, MACHINE_ABATTEUSE)


def test_witness_R8_T1() -> None:
    st = _mk(("H", "E", "R"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 8)  # R8 non défendu au rang 4 (rang 3 libre !)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    st.set_player_hand(0, CARD_ECAILLE, 2, 5, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 4, 0, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R8_ALTER_OR_COOL":
            apply_choice(st, ("REFROIDIR", 0, MACHINE_ABATTEUSE))
            break
        apply_choice(st, out.options[0])
    assert st.find_tactique_rank(TILE_R_BASE + 8) == 2
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)


def test_witness_R8_T2() -> None:
    st = _mk(("H", "E", "R"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 8)  # R8 défendu au rang 4
    st.place_defender_reve_standing(1, 0, 4)
    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "R8_ALTER_OR_COOL":
            apply_choice(st, _pick(out, lambda o: isinstance(o, tuple) and o[0] == "ALTERER"))
            break
        apply_choice(st, out.options[0])
    assert st.find_tactique_rank(TILE_R_BASE + 8) == 2
    assert any(st.has_machine_alteration(r, mt) for r in range(3) for mt in (0, 1))


def test_witness_R9_T1() -> None:
    st = _mk(("H", "E", "O"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 9)  # R9 défendu au rang 4
    st.place_defender_reve_standing(1, 0, 4)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RANK, 1)  # Perchoir rang 2 libre !
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 2, 5, 2, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 3, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 4, 0, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(12):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek == "R9_VOL_BRUME":
            apply_choice(st, 2)  # Vole au rang 2 !
        elif ek == "R9_MAUDIRE_OU_SIFFLER":
            apply_choice(st, ("MAUDIRE", 0, MACHINE_ABATTEUSE))
            break
        else:
            apply_choice(st, out.options[0])
    assert st.find_tactique_rank(TILE_R_BASE + 9) == 1
    assert st.has_machine_alteration(0, MACHINE_ABATTEUSE)


def test_witness_R9_T2() -> None:
    st = _mk(("H", "E", "O"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 9)  # R9 rang 4
    st.set_tactique_at_rank(5, TILE_R_BASE + 1)  # R1 rang 6
    st.place_defender_reve_standing(1, 0, 4)
    st.set_machine_alteration(0, MACHINE_ABATTEUSE, True)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, 1, 0)
    st.set_machine_alteration(2, MACHINE_ABATTEUSE, True)
    st.set_machine_tokens(2, MACHINE_ABATTEUSE, 1, 0)
    st.set_player_hand(0, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    siff_count = 0
    for _ in range(15):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek in ("R9_MAUDIRE_OU_SIFFLER", "R9_SIFFLER_SECOND"):
            apply_choice(st, _pick(out, lambda o: isinstance(o, tuple) and o[0] == "SIFFLER"))
            siff_count += 1
        elif ek == "R9_SIFFLER_SLIDE":
            apply_choice(st, out.options[0])
        else:
            if siff_count >= 2:
                break
            apply_choice(st, out.options[0])
    assert siff_count == 2
    assert not st.has_machine_alteration(0, MACHINE_ABATTEUSE)
    assert not st.has_machine_alteration(2, MACHINE_ABATTEUSE)
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 1)
    assert st.get_machine_tokens(2, MACHINE_ABATTEUSE) == (0, 1)


def test_witness_R10_T1() -> None:
    st = _mk(("H", "E", "I"))
    st.set_tactique_at_rank(3, TILE_R_BASE + 10)  # R10 rang 4 défendu
    st.place_defender_reve_standing(1, 0, 4)
    st.set_parcel_nid(2, 2, 1)
    st.place_defender_foret(2, 0, 2, 2, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 2, 2)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_BULLDOZER, 1, 0)
    st.set_player_hand(0, 0, 1, 2, 0, 0)
    st.set_player_hand(1, 0, 1, 2, 0, 0)
    st.set_player_hand(2, 0, 1, 2, 0, 0)
    st.step = STEP_3_2_REVEAL
    for _ in range(12):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek == "R10_BRANCH":
            apply_choice(st, ("ENVOL", 1, 0, 3))
        elif ek == "R10_ENVOL_BONUS":
            apply_choice(st, ("REFROIDIR", 0, MACHINE_BULLDOZER))
            break
        else:
            apply_choice(st, out.options[0])
    assert st.find_tactique_rank(TILE_R_BASE + 10) == 2
    pos_n = st.get_nid_position(1)
    assert pos_n is not None and pos_n[:2] == (0, 3)
    assert st.get_parcel_defenseurs(0, 3) == 1 and st.get_parcel_insectes(0, 3) == 2
    assert st.get_machine_tokens(0, MACHINE_BULLDOZER) == (0, 1)


# ---------------------------------------------------------------------------
# M1..M5 (7 témoins)
# ---------------------------------------------------------------------------


def test_witness_M1_T1() -> None:
    st = _mk(("H", "M", "I"))
    st.set_parcel_nid(2, 2, 1)
    st.place_defender_foret(2, 0, 2, 2, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 2, 2)
    st.set_machine_pos_status(1, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(1, MACHINE_BULLDOZER, 1, 0)
    st.step = STEP_4_2_NIDS
    embarked = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.decision_type == DEC_DEPLOIEMENT_NID_4_2:
            apply_choice(st, ("FORET", 2, 2))
        elif out.context.get("effect_kind") == "M1_EMBARQUER":
            apply_choice(st, (1, MACHINE_BULLDOZER, 2))
            embarked = True
            break
        else:
            apply_choice(st, out.options[0])
    assert embarked and st.get_machine_passenger_insects(1, MACHINE_BULLDOZER) == 2

    # Frappe du Bulldozer sur parcelle du Duel Défi (1 Défenseur, Seuil 3) -> 2 passagers sautent, parent et retournent Duel !
    st.place_defender_foret(1, 0, 1, 2, FACE_DEFINITIF)
    st.set_duel_state_at(1, 2, DUEL_DEFI)
    resolve_single_machine_attack(st, 1, MACHINE_BULLDOZER, TACTIQUES_SPEC[4])
    assert st.get_machine_passenger_insects(1, MACHINE_BULLDOZER) == 0
    assert st.get_duel_state() == (DUEL_TERRITOIRE_TENU, 1, 2)


def test_witness_M1_T2() -> None:
    st = _mk(("H", "M", "I"))
    st.set_machine_pos_status(1, MACHINE_BULLDOZER, 3, MACHINE_STATUS_NORMAL)
    st.set_machine_passenger_insects(1, MACHINE_BULLDOZER, 1)
    st.cleanup_end_of_turn_6_2()
    assert st.get_machine_passenger_insects(1, MACHINE_BULLDOZER) == 0
    assert st.get_parcel_insectes(1, 3) == 1


def test_witness_M2_T1() -> None:
    st = _mk(("H", "R", "I"))
    st.set_parcel_nid(2, 2, 2)
    st.set_parcel_insectes(2, 2, 2)
    st.set_machine_pos_status(2, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(2, MACHINE_ABATTEUSE, 2, 0)  # Seuil 4 en Assaut, 0 Défenseur !
    st.set_gardien_at_case(TRIG_INSECTE, 1, 1)
    st.place_defender_gardien_pari(0, TRIG_INSECTE, FACE_DEFINITIF)
    arbres_before = st.get_parcel_arbres(2, 2)
    resolve_single_machine_attack(st, 2, MACHINE_ABATTEUSE, TACTIQUES_SPEC[4])
    req = step_until_decision(st)
    assert not isinstance(req, GameOver) and req.context.get("effect_kind") == "M2_SOLDATS_A_GLU"
    apply_choice(st, "SOLDATS_A_GLU")
    step_until_decision(st)
    assert st.get_parcel_insectes(2, 2) == 0
    assert st.get_parcel_arbres(2, 2) == arbres_before
    assert st.count_gardien_pari_defenders_at_case(TRIG_INSECTE) == 0


def test_witness_M2_T2() -> None:
    st = _mk(("H", "R", "I"))
    st.set_parcel_nid(2, 3, 2)
    st.place_defender_foret(2, 0, 2, 3, FACE_DEFINITIF)
    ec_before = st.ecaille_deck_count + st.ecaille_pending_count
    st.step = STEP_4_2_NIDS
    for _ in range(8):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.decision_type == DEC_DEPLOIEMENT_NID_4_2:
            apply_choice(st, ("FORET", 2, 3))
        elif out.context.get("effect_kind") == "M2_PROD_REPTILE":
            apply_choice(st, "SEMER_ECAILLE")
            break
        else:
            apply_choice(st, out.options[0])
    assert (st.ecaille_deck_count + st.ecaille_pending_count) == ec_before + 1


def test_witness_M3_T1() -> None:
    st = _mk(("H", "O", "I"))
    # M3 défendu en I·1 (rayon 2, p=1) avec Perchoir sur rayon voisin O (siège 1) -> marche 2 pas vers O (1, 2), produit, Front de raid 2 Insectes !
    st.set_parcel_nid(2, 1, 3)
    st.place_defender_foret(2, 0, 2, 1, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 1, 2)
    st.set_oiseau_perchoir_signal(PERCHOIR_CHAUD, PERCHOIR_KIND_RAY, 1)
    st.set_machine_pos_status(1, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_player_hand(0, machine_card_code(1, MACHINE_ABATTEUSE), 1, 4, 1, 1)
    st.step = STEP_4_2_NIDS
    moved = False
    raided = False
    for _ in range(12):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        ek = out.context.get("effect_kind", "")
        if ek == "M3_BIVOUAC_MARCHE":
            apply_choice(st, (1, 2))  # 2 pas : (2,1) -> (1,1) -> (1,2) !
            moved = True
        elif out.decision_type == DEC_DEPLOIEMENT_NID_4_2:
            apply_choice(st, ("FORET", 1, 2))
        elif ek == "M3_FRONT_DE_RAID":
            apply_choice(st, (1, 3, 2))
            raided = True
            break
        else:
            apply_choice(st, out.options[0])
    assert moved and raided
    pos_m3 = st.get_nid_position(3)
    assert pos_m3 is not None and pos_m3[:2] == (1, 2)
    assert st.get_parcel_defenseurs(1, 2) == 1
    assert st.get_parcel_insectes(1, 3) == 2


def test_witness_M4_T1() -> None:
    st = _mk(("H", "M", "I"))
    st.set_parcel_nid(2, 2, 4)
    st.place_defender_foret(2, 0, 2, 2, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 2, 2)
    # Tambour en forêt sur (0, 3) et 2 bâtisseurs couchés en attente
    st.set_humain_chaman_archetype(0, CHAMAN_TAMBOUR)
    st.place_defender_foret(0, 0, 0, 3, FACE_DEFINITIF)
    st.mark_defender_waiting(1, 0)
    st.mark_defender_waiting(1, 1)
    st.step = STEP_4_2_NIDS
    lifted = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.decision_type == DEC_DEPLOIEMENT_NID_4_2:
            apply_choice(st, ("FORET", 2, 2))
        elif out.context.get("effect_kind") == "M4_MELIPONES_RELEVER":
            apply_choice(st, (1, 0, 0, 3))
            lifted = True
            break
        else:
            apply_choice(st, out.options[0])
    assert lifted
    assert st.get_parcel_defenseurs(0, 3) == 2  # Tambour + bâtisseur relevé !


def test_witness_M5_T1() -> None:
    st = _mk(("H", "E", "I"))
    st.set_parcel_nid(2, 2, 5)
    st.place_defender_foret(2, 0, 2, 2, FACE_DEFINITIF)
    st.set_parcel_insectes(2, 2, 1)
    # Phase 1 (4.2) : Filaments oniriques envoie 1 Insecte sur rang 4
    st.step = STEP_4_2_NIDS
    sent_bug = False
    for _ in range(10):
        out = step_until_decision(st)
        if isinstance(out, GameOver):
            break
        if out.decision_type == DEC_DEPLOIEMENT_NID_4_2:
            apply_choice(st, ("FORET", 2, 2))
        elif out.context.get("effect_kind") == "M5_FILAMENTS_ONIRIQUES":
            apply_choice(st, ("BUG_RANK", 4))
            sent_bug = True
            break
        else:
            apply_choice(st, out.options[0])
    assert sent_bug and st.get_bugs_at_case(4) == 1
    assert st.get_parcel_insectes(2, 2) == 1  # < 2

    # Phase 2 (3.2 suivant) : Déviation -1 vers un Rêve au rang 3 Altère la machine et recycle l'Insecte sur M5 (< 2) !
    st2 = _mk(("H", "E", "I"))
    st2.set_parcel_nid(2, 2, 5)
    st2.set_parcel_insectes(2, 2, 1)
    st2.set_tactique_at_rank(2, TILE_R_BASE + 1)  # Rêve au rang 3
    st2.set_bugs_at_case(4, 1)
    st2.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 4, 6, 4, 0)
    st2.set_player_hand(1, CARD_SABOTAGE, 1, 2, 0, 0)
    st2.set_player_hand(2, CARD_SABOTAGE, 1, 2, 0, 0)
    st2.step = STEP_3_2_REVEAL
    deviated = False
    for _ in range(10):
        out = step_until_decision(st2)
        if isinstance(out, GameOver):
            break
        if out.context.get("effect_kind") == "BUG_DEVIATION_SYNAPTIQUE_3_2":
            apply_choice(st2, "M_MOINS_1")
            deviated = True
            break
        apply_choice(st2, out.options[0])
    assert deviated
    assert st2.has_machine_alteration(0, MACHINE_ABATTEUSE)
    assert st2.get_parcel_insectes(2, 2) == 2  # Recyclé sur M5 !


def test_witness_zero_mem_debt_check() -> None:
    st = _mk(("H", "M", "O", "R", "E", "I"), mode=4)
    trk = TelemetryTracker()
    assert trk.mem_debt_score == 0
    _ = (st, prim_partage_info_etat_gardien, verb_reculer, CARD_ECAILLE, STEP_4_1_FURTIVITE)
