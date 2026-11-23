"""Smoke-tests dédiés aux prises d'accroche du futur Mode 4 (Panier 2 — 30 tuiles asymétriques).

Vérifie que l'assainissement v6.1 a préservé intact l'ensemble du câblage Mode 4 :
1. Sélection des 2*N tuiles actives selon le voisinage autour de la table (MATRICE_PAIRES)
   et gouvernance unitaire par peuple d'origine.
2. Présence physique des Souches et hook `HOOK_REPOUSSE_FINALE` (0 de base en socle,
   repousse active via tuile Mode 4 avec comptabilité `da_arbres_repousse_finale`).
3. Déplacement de Rêve déclenché par pouvoir de tuile (`ADVANCE_REVE_LEFT`) et fin
   `Sommeil du Contremaître` en 5.3 (bloc continu `1..k` -> `CAUSE_REVE_RANG_1`).
4. Pipeline complet des Gardiens : ouverture (`HOOK_GARDIEN_OUVERTURE`), retournement
   Face 1 -> Face 2 en 5.3 sur pari gagné, balayage à plat des cascades `1..6` sans
   pile imbriquée (`sweep_gardiens`), Lois passives (`HOOK_5_LAW_QUERY`) et inversion
   `min/max` de lecture du dé secret (`HOOK_1_3_LECTURE_DE`).
5. Pouvoirs propres des Rêves (`HOOK_3_2_OUVERTURE_REVE`), Nids (`4.2` bloc indivisible
   + `HOOK_4_2_NID_APRES_PROD`), Pièges localisés (`HOOK_5_APRES_PARADE_PIEGE`) et
   synergies liées au Sabotage / Furtivité (`HOOK_4_1_FURTIVITE`).
6. Parties complètes Mode 4 couvrant les 30 tuiles actives (`G1..G15`, `R1..R10`, `M1..M5`)
   avec `B0`, `B1`, `B2` et invariants de conservation intacts.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any

import engine.effects  # noqa: F401
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import play_game_b1, play_game_b2
from engine.core_engine import (
    _advance_continuation,
    _resolve_nid_block,
    _run_step_3_2,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import (
    CAUSE_REVE_RANG_1,
    CAUSE_TOUR_8,
    HOOK_1_3_LECTURE_DE,
    HOOK_4_1_FURTIVITE,
    HOOK_5_APRES_PARADE_PIEGE,
    HOOK_REPOUSSE_FINALE,
    DecisionRequest,
    EffectHandler,
    GameOver,
    _RegistryStore,
    prim_mod_loi_du_coeur,
    prim_permutation_piste,
    register_tile,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FURT_RIVE_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MATRICE_PAIRES,
    PIEGE_ACTIF,
    STEP_1_3_DICE,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_5_3_END_CHECK,
    SYNERGY_META,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker

# Cercles couvrant N=3..6 et l'intégralité des 15 paires de MATRICE_PAIRES (30 tuiles actives)
ALL_30_TILES_CIRCLES: tuple[tuple[str, ...], ...] = (
    ("M", "R", "O"),
    ("M", "R", "H", "I"),
    ("M", "R", "O", "H", "E"),
    ("M", "R", "O", "H", "E", "I"),
    ("M", "O", "E", "R", "I", "H"),
    ("M", "E", "R", "H", "O", "I"),
)


@contextmanager
def _temporary_tile_hook(
    slot_id: str, profile: str, hooks: tuple[str, ...], handler: EffectHandler
) -> Iterator[None]:
    """Enregistre temporairement un profil de tuile test et restaure le registre global ensuite."""
    snap_by_key = dict(_RegistryStore.by_key)
    snap_by_hook = {k: list(v) for k, v in _RegistryStore.by_hook.items()}
    try:
        register_tile(slot_id, profile, hooks=hooks)(handler)
        yield
    finally:
        _RegistryStore.by_key.clear()
        _RegistryStore.by_key.update(snap_by_key)
        _RegistryStore.by_hook.clear()
        _RegistryStore.by_hook.update(snap_by_hook)


def test_panier2_2xn_adjacency_selection_and_unitary_governance() -> None:
    """Sélection des 2*N tuiles actives selon les paires adjacentes et gouvernance par peuple."""
    seen_all_30: set[str] = set()
    for peuples in ALL_30_TILES_CIRCLES:
        n = len(peuples)
        cfg = GameConfig(n_players=n, mode=4, peuples=peuples, exp_seed=7401)
        assert len(cfg.lisiere_slots) == 2 * n
        assert len(set(cfg.lisiere_slots)) == 2 * n

        # Chaque paire adjacente (p_i, p_{i+1}) fournit exactement ses 2 tuiles de MATRICE_PAIRES
        for idx in range(n):
            p_left = peuples[idx]
            p_right = peuples[(idx + 1) % n]
            expected_pair = MATRICE_PAIRES[f"{p_left}_{p_right}"]
            actual_pair = (cfg.lisiere_slots[2 * idx], cfg.lisiere_slots[2 * idx + 1])
            assert actual_pair == expected_pair
            for tid in actual_pair:
                seen_all_30.add(tid)
                # Gouvernance unitaire : chaque tuile a un peuple d'origine présent à la table
                _, origin_peuple, _ = SYNERGY_META[tid]
                assert origin_peuple in (p_left, p_right)
                gov_seat = cfg.seat_of_peuple(origin_peuple)
                assert gov_seat is not None and peuples[gov_seat] == origin_peuple

    expected_30 = (
        {f"G{i}" for i in range(1, 16)}
        | {f"R{i}" for i in range(1, 11)}
        | {f"M{i}" for i in range(1, 6)}
    )
    assert seen_all_30 == expected_30


def test_panier2_souches_and_hook_repousse_finale() -> None:
    """Souches physiques + HOOK_REPOUSSE_FINALE : 0 en socle, repousse active via tuile Mode 4."""

    def _regrow_1_on_stump(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
        _ = state
        ctx["max_repousse"] = max(int(ctx["max_repousse"]), 1)

    with _temporary_tile_hook("G10", "T_REP", (HOOK_REPOUSSE_FINALE,), _regrow_1_on_stump):
        cfg = GameConfig(
            n_players=4,
            mode=4,
            peuples=("M", "R", "O", "H"),
            tile_profiles=(("G10", "T_REP"),),
            exp_seed=7402,
        )
        st = GameState(cfg)
        st.tour = 8
        st.set_gardien_at_case(1, 10, face=1)  # G10 en jeu sur la piste des Gardiens
        st.set_parcel_arbres_souches(0, 1, 0, 2)  # 2 souches -> +1 arbre repoussé
        st.set_parcel_arbres_souches(1, 2, 1, 1)  # 1 souche -> +1 arbre repoussé
        arbres_avant = st.total_arbres_plateau()

        trk = TelemetryTracker()
        st.step = STEP_5_3_END_CHECK
        over = step_until_decision(st, telemetry=trk)
        assert isinstance(over, GameOver)
        assert over.cause_fin == CAUSE_TOUR_8
        assert over.score_arbres == arbres_avant + 2
        assert trk.summary().da_arbres_repousse_finale == 2


def test_panier2_tile_driven_reve_advance_and_sommeil_contremaitre_5_3() -> None:
    """Avancée d'un Rêve par pouvoir de tuile (`ADVANCE_REVE_LEFT`) et fin Sommeil `1..k` en 5.3."""
    cfg = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "H"), exp_seed=7403)
    st = GameState(cfg)
    st.tour = 4
    # 1 Peuple Onirique (H) -> 2 Rêves dans la partie (O-H et H-M) -> total_reves_partie == 2
    assert cfg.total_reves_partie == 2
    # Placer R1 au rang 1 (idx 0) et R2 au rang 3 (idx 2) -> NON contigu -> pas de Sommeil
    st.set_tactique_at_rank(0, TILE_R_BASE + 1)
    st.set_tactique_at_rank(2, TILE_R_BASE + 2)
    assert st.is_sommeil_victory() is False

    # Pouvoir de tuile Mode 4 faisant avancer R2 d'une case vers la gauche (idx 2 -> idx 1)
    assert prim_permutation_piste(st, "ADVANCE_REVE_LEFT", rank_a=2) is True
    assert st.get_tactique_at_rank(1) == TILE_R_BASE + 2
    assert st.is_sommeil_victory() is True

    st.step = STEP_5_3_END_CHECK
    over = step_until_decision(st)
    assert isinstance(over, GameOver)
    assert over.cause_fin == CAUSE_REVE_RANG_1


def test_panier2_gardiens_full_hooks_cascade_face2_and_passive_die_inversion() -> None:
    """Ouverture Gardien, Face 1 -> Face 2 en 5.3, cascade plate 1..6, Lois passives & min/max dé."""
    # 1) Cascade plate 1..6 + Face 1 -> Face 2 sur pari gagné en 5.3 (G9:A sur case 3 + G1:A sur case 4)
    cfg = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "I"), exp_seed=7404)
    st = GameState(cfg)
    st.tour = 2
    st.set_gardien_at_case(3, 9, face=1)
    st.set_gardien_at_case(4, 1, face=1)
    st.place_defender_gardien_pari(0, 3, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 4, FACE_DEFINITIF)
    sab_before = st.sabotage_pending_count

    # Déclenchement case 3 -> ouvre G9:A (+1 Sabotage) -> allume case 4 (Résonance) -> ouvre G1:A !
    st.light_trigger(3)
    opened = sweep_gardiens(st)
    assert opened == 2
    assert st.sabotage_pending_count == sab_before + 1
    assert st.count_gardien_pari_defenders_at_case(3) == 0
    assert st.count_gardien_pari_defenders_at_case(4) == 0
    assert st.get_gardien_at_case(3) == (9, 1)  # Reste Face 1 jusqu'en 5.3

    st.step = STEP_5_3_END_CHECK
    res_53 = step_until_decision(st)
    assert not isinstance(res_53, GameOver)
    assert st.get_gardien_at_case(3) == (9, 2)  # Passé Face 2 en 5.3 sur pari gagné !
    assert st.get_gardien_at_case(4) == (1, 2)

    # 2) Loi passive d'inversion min/max de lecture du dé secret via HOOK_1_3_LECTURE_DE
    def _invert_die_to_max(state: GameState, _hook: str, ctx: dict[str, Any]) -> None:
        seat = int(ctx["seat"])
        card, d1, d2, _lec, bound = state.get_player_hand(seat)
        if 1 <= card <= 12:
            prim_mod_loi_du_coeur(state, "LOI_INV_LECTURE_DE_MAX", active=True)
            state.set_player_hand(seat, card, d1, d2, max(d1, d2), bound)

    with _temporary_tile_hook("G10", "T_DIE", (HOOK_1_3_LECTURE_DE,), _invert_die_to_max):
        cfg_d = GameConfig(
            n_players=4,
            mode=4,
            peuples=("M", "R", "O", "H"),
            tile_profiles=(("G10", "T_DIE"),),
            exp_seed=7405,
        )
        st_d = GameState(cfg_d)
        st_d.tour = 1
        st_d.set_gardien_at_case(2, 10, face=1)
        for s in range(4):
            st_d.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 0, 0, 0, 0)
        st_d.step = STEP_1_3_DICE
        _ = step_until_decision(st_d)
        checked_diff = 0
        for s in range(4):
            _, d1, d2, lec_m, _ = st_d.get_player_hand(s)
            assert lec_m == max(d1, d2)
            if d1 != d2:
                checked_diff += 1
        assert checked_diff >= 1


def test_panier2_reves_nids_pieges_and_sabotage_hooks() -> None:
    """Hooks propres des Rêves (3.2), Nids (4.2), Pièges localisés (5.1) et Furtivité/Sabotage (4.1)."""
    # 1) Rêve R6:A (HOOK_3_2_OUVERTURE_REVE) & Nid M2:A (4.2 bloc indivisible + HOOK_4_2_NID_APRES_PROD)
    cfg = GameConfig(n_players=4, mode=4, peuples=("H", "M", "I", "R"), exp_seed=7406)
    st = GameState(cfg)
    st.tour = 2
    st.set_tactique_at_rank(5, TILE_R_BASE + 6)
    st.place_defender_reve_activation(0, 6, FACE_DEFINITIF)
    st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 6, 6, 0)
    for s in (1, 2, 3):
        st.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
    ins_before = sum(st.get_parcel_insectes(r, p) for r in range(4) for p in range(1, 5))
    st.step = STEP_3_2_REVEAL
    _run_step_3_2(st)
    while st._continuation:
        rem = _advance_continuation(st)
        if isinstance(rem, DecisionRequest):
            apply_choice(st, rem.options[0])
    ins_after = sum(st.get_parcel_insectes(r, p) for r in range(4) for p in range(1, 5))
    assert ins_after == ins_before + 1

    # Bloc 4.2 Nid M2:A : production + retournement d'1 jeton rouge physique en bleu
    st.set_parcel_nid(0, 1, 2, active_ce_tour=False)
    st.set_parcel_insectes(0, 1, 0)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=1, bleus=0)
    for r in range(4):
        st.set_machine_pos_status(r, MACHINE_ABATTEUSE, 0, 2)
        if r != 0:
            st.set_machine_pos_status(r, MACHINE_BULLDOZER, 0, 2)
    _resolve_nid_block(st, 2)
    assert st.get_parcel_insectes(0, 1) == 1
    assert st.get_machine_tokens(0, MACHINE_BULLDOZER) == (0, 1)

    # 2) Hooks HOOK_5_APRES_PARADE_PIEGE (Piège localisé) & HOOK_4_1_FURTIVITE (synergie Sabotage)
    observed_events: list[tuple[str, dict[str, Any]]] = []

    def _observer_handler(state: GameState, hook: str, ctx: dict[str, Any]) -> None:
        _ = state
        observed_events.append((hook, dict(ctx)))

    with _temporary_tile_hook(
        "G10",
        "T_OBS",
        (HOOK_5_APRES_PARADE_PIEGE, HOOK_4_1_FURTIVITE),
        _observer_handler,
    ):
        cfg_obs = GameConfig(
            n_players=4,
            mode=4,
            peuples=("M", "R", "O", "H"),
            tile_profiles=(("G10", "T_OBS"),),
            exp_seed=7407,
        )
        st_obs = GameState(cfg_obs)
        st_obs.tour = 2
        st_obs.paravents_ouverts = True
        st_obs.set_gardien_at_case(1, 10, face=1)

        # Déclenchement HOOK_5_APRES_PARADE_PIEGE sur parade par Piège autonome en (0, 2)
        st_obs.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
        st_obs.set_parcel_piege(0, 2, PIEGE_ACTIF)
        resolve_single_machine_attack(st_obs, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])

        # Déclenchement HOOK_4_1_FURTIVITE (action == "SABOTAGE") sur Rive Sabotage gagnée (m(1) == 0)
        for s in range(4):
            st_obs.set_player_hand(s, CARD_SABOTAGE, 0, 0, 0, 0)
        st_obs.place_defender_furtivite(0, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
        st_obs.place_defender_furtivite(1, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
        st_obs.set_parcel_insectes(3, 1, 1)  # Ancre 4.3
        st_obs.step = STEP_4_1_FURTIVITE
        _ = step_until_decision(st_obs)

    piege_ev = [c for h, c in observed_events if h == HOOK_5_APRES_PARADE_PIEGE]
    furt_ev = [c for h, c in observed_events if h == HOOK_4_1_FURTIVITE]
    assert len(piege_ev) == 1 and piege_ev[0]["ray"] == 0 and piege_ev[0]["target_p"] == 2
    assert len(furt_ev) == 1 and furt_ev[0]["action"] == "SABOTAGE" and furt_ev[0]["ray"] == 1


def test_panier2_end_to_end_mode4_all_30_tiles_b0_b1_b2() -> None:
    """Smoke bout-en-bout Mode 4 sur 6 tables N=3..6 couvrant les 30 tuiles actives × B0/B1/B2."""
    for idx, peuples in enumerate(ALL_30_TILES_CIRCLES):
        cfg = GameConfig(
            n_players=len(peuples),
            mode=4,
            peuples=peuples,
            exp_seed=7410 + idx,
            rep_id=0,
            max_revision_passes=1,
        )
        for runner in (play_game_b0, play_game_b1, play_game_b2):
            st = GameState(cfg)
            trk = TelemetryTracker()
            over = runner(st, telemetry=trk)
            assert 1 <= over.tour_fin <= 8
            assert 0.0 <= over.ratio_arbres <= 1.0
            assert trk.summary().mem_debt_score >= 0
    # Et contrôle strict mem_debt == 0 en Mode 2 (socle blanc v6.1)
    cfg_m2 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=7420)
    trk_m2 = TelemetryTracker()
    over_m2 = play_game_b2(GameState(cfg_m2), telemetry=trk_m2)
    assert 1 <= over_m2.tour_fin <= 8
    assert trk_m2.summary().mem_debt_score == 0
