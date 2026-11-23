"""Tests d'invariants du Lot 1 — Intégrité causale, manifestes stricts, cercles équilibrés & mélange stable."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pytest

from bots.belief_and_ticks import resolve_step2_full_with_ticks
from bots.heuristic_engine import choose_b2, play_game_b2, score_target_b2
from campaigns.designs import (
    balanced_neighbor_mirror_pairs,
    balanced_neighbor_mirror_tables,
    mirror_peuples,
)
from campaigns.worker_main import resolve_manifest_plan
from engine.core_engine import (
    DEC_POSE_DEFENSEUR_1,
    DEC_POSE_DEFENSEUR_2,
    apply_choice,
    step_until_decision,
)
from engine.primitives import GameOver
from engine.state import (
    CARD_SABOTAGE,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_RATISSAGE,
    PEUPLES_ORDER,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    GameConfig,
    GameState,
)
from scripts_cloud.fuzz_invariants import BoundAttackInvariantTracker

ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Suppression du biais placebo dans les forks d'ablation
# ---------------------------------------------------------------------------


def _play_game_b2_with_placebo_filter(state: GameState) -> GameOver:
    """Rejoue une partie B2 complète avec un filtre d'actions autorisant 100 % des cibles."""

    def _allow_all(_target: tuple[Any, ...], _is_first: bool) -> bool:
        return True

    steps = 0
    while True:
        steps += 1
        assert steps <= 2000
        out = step_until_decision(state, max_internal_steps=2000)
        if isinstance(out, GameOver):
            return out
        if state.step in (STEP_2_1_DEF1, STEP_2_2_DEF2) and out.decision_type in (
            DEC_POSE_DEFENSEUR_1,
            DEC_POSE_DEFENSEUR_2,
        ):
            resolve_step2_full_with_ticks(
                state,
                score_target_b2,
                k_max_passes=3,
                epsilon_base=24.0,
                epsilon_step=12.0,
                target_filter=_allow_all,
            )
            continue
        apply_choice(state, choose_b2(state, out))


def test_placebo_action_filter_matches_standard_b2_exact_50_seeds() -> None:
    """Un filtre autorisant 100 % des actions reproduit bit-à-bit B2 standard (poses T1 + score final)."""
    for rep in range(50):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "O", "H"),
            exp_seed=20269001,
            rep_id=rep,
            max_revision_passes=3,
        )
        # A. Égalité exacte des poses dès le Tour 1
        s_ref = GameState(cfg)
        s_plc = GameState(cfg)
        step_until_decision(s_ref)
        step_until_decision(s_plc)
        assert s_ref.step == STEP_2_1_DEF1 and s_plc.step == STEP_2_1_DEF1
        resolve_step2_full_with_ticks(
            s_ref, score_target_b2, k_max_passes=3, epsilon_base=24.0, epsilon_step=12.0
        )
        resolve_step2_full_with_ticks(
            s_plc,
            score_target_b2,
            k_max_passes=3,
            epsilon_base=24.0,
            epsilon_step=12.0,
            target_filter=lambda _t, _f: True,
        )
        assert s_plc.raw_used_bytes() == s_ref.raw_used_bytes(), (
            f"Biais placebo détecté dès Tour 1 sur rep={rep}"
        )

        # B. Égalité exacte sur toute la partie (score final, tour, cause)
        g_ref = GameState(cfg)
        g_plc = GameState(cfg)
        res_ref = play_game_b2(g_ref, k_max_passes=3)
        res_plc = _play_game_b2_with_placebo_filter(g_plc)
        assert res_plc == res_ref
        assert g_plc.raw_used_bytes() == g_ref.raw_used_bytes()


# ---------------------------------------------------------------------------
# 2. Validation stricte des manifestes et du registre d'effets
# ---------------------------------------------------------------------------


def _base_valid_manifest(mode: int = 4) -> dict[str, Any]:
    return {
        "campaign_name": "test_strict_manifest",
        "mode": mode,
        "player_counts": [4],
        "games_per_configuration": 4,
        "bot": "B2",
        "k_max": 3,
        "slot_profile_comparisons": {},
    }


@pytest.mark.parametrize(
    "bad_key,bad_val",
    [
        ("Offset_Seuil_Parad", 1),
        ("Mise_En_Place_Tactiques", "FIXE"),
        ("P_Max", 5),
        ("reve_advance_mode", "SAUT"),
        ("chassis_axes", {"Profil_Piste": ["P4_2233"]}),
        ("cle_inconnue_xyz", True),
    ],
)
def test_manifest_rejects_unknown_or_obsolete_keys(bad_key: str, bad_val: Any) -> None:
    manifest = _base_valid_manifest(mode=2)
    manifest[bad_key] = bad_val
    with pytest.raises(ValueError, match="Clé\\(s\\) ou axe\\(s\\) inconnu"):
        resolve_manifest_plan(manifest)


def test_manifest_requires_explicit_mode_aligned_with_game_config() -> None:
    manifest = _base_valid_manifest(mode=2)
    del manifest["mode"]
    with pytest.raises(ValueError, match="Champ obligatoire 'mode'"):
        resolve_manifest_plan(manifest)

    # Lorsque k_max est omis, le défaut s'aligne sur GameConfig.max_revision_passes (4)
    m_default_k = _base_valid_manifest(mode=2)
    del m_default_k["k_max"]
    plan = resolve_manifest_plan(m_default_k)
    assert plan["k_max"] == GameConfig(mode=2).max_revision_passes


@pytest.mark.parametrize(
    "bad_comp",
    [
        {"G1": ["A", "B"]},
        {"G7": ["B"]},
        {"R3": ["D"]},
        {"SLOT_BUG_CERVEAU": ["A"]},
        {"G99": ["A"]},
    ],
)
def test_manifest_rejects_unimplemented_tile_profiles_in_mode4(bad_comp: dict[str, list[str]]) -> None:
    manifest = _base_valid_manifest(mode=4)
    manifest["slot_profile_comparisons"] = bad_comp
    with pytest.raises(ValueError):
        resolve_manifest_plan(manifest)


def test_manifest_rejects_tile_profile_override_in_mode2_and_accepts_neutre_in_mode4() -> None:
    m_mode2 = _base_valid_manifest(mode=2)
    m_mode2["slot_profile_comparisons"] = {"G1": ["A"]}
    with pytest.raises(ValueError, match="Mode 3 ou 4"):
        resolve_manifest_plan(m_mode2)

    m_mode4 = _base_valid_manifest(mode=4)
    m_mode4["slot_profile_comparisons"] = {"G1": ["A", "NEUTRE"]}
    plan = resolve_manifest_plan(m_mode4)
    assert plan["tested_tiles"] == (("G1", "A"), ("G1", "NEUTRE"))

    cfg_neutre = GameConfig(mode=4, tile_profiles=(("G1", "NEUTRE"),))
    assert cfg_neutre.profile_for_slot("G1") is None
    assert cfg_neutre.profile_for_slot("G2") == "A"


# ---------------------------------------------------------------------------
# 3. Échantillonnage équilibré des cercles de voisinage (N=3..6)
# ---------------------------------------------------------------------------


def _neighbor_edge_counts(tables: tuple[tuple[str, tuple[str, ...]], ...]) -> Counter[tuple[str, str]]:
    all_edges = [
        (PEUPLES_ORDER[i], PEUPLES_ORDER[j])
        if PEUPLES_ORDER[i] < PEUPLES_ORDER[j]
        else (PEUPLES_ORDER[j], PEUPLES_ORDER[i])
        for i in range(6)
        for j in range(i + 1, 6)
    ]
    counts: Counter[tuple[str, str]] = Counter({e: 0 for e in all_edges})
    for _tid, peuples in tables:
        n = len(peuples)
        for idx in range(n):
            a = peuples[idx]
            b = peuples[(idx + 1) % n]
            counts[(a, b) if a < b else (b, a)] += 1
    return counts


def test_balanced_neighbor_circles_cover_all_15_edges_equitably_for_all_n() -> None:
    """Chaque paire de voisins (et donc les 30 lisières) est équilibrée pour N=3..6, y compris à 6J."""
    # Préfixes exacts (en nombre de paires miroirs -> 2 tables par paire)
    exact_pair_counts = {3: 10, 4: 15, 5: 6, 6: 5}
    for n_pl, k_pairs in exact_pair_counts.items():
        tables = balanced_neighbor_mirror_tables(
            n_pl, min_animaux_sauvages=1, max_tables=2 * k_pairs, exp_seed=20261201
        )
        assert len(tables) == 2 * k_pairs
        # Vérification stricte de l'appariement par paires miroirs
        for i in range(0, len(tables), 2):
            assert mirror_peuples(tables[i][1]) == tables[i + 1][1]
        ec = _neighbor_edge_counts(tables)
        assert len(ec) == 15
        assert min(ec.values()) == max(ec.values()) > 0, (
            f"Déséquilibre d'arêtes pour N={n_pl}, k_pairs={k_pairs}: {dict(ec)}"
        )

    # Troncature petite (ex. 10 parties à 4J/6J) : pas de biais M/R ni de cercle unique à 6J
    manifest = {
        "campaign_name": "test_balanced_truncation",
        "mode": 2,
        "player_counts": [3, 4, 5, 6],
        "games_per_configuration": 20,
        "table_selection": "ALL_PEUPLE_COMBOS",
        "min_animaux_sauvages": 1,
        "bot": "B2",
        "seed": 20261201,
    }
    plan = resolve_manifest_plan(manifest)
    for n_pl in (3, 4, 5, 6):
        n_units = [u for u in plan["units"] if u["n_players"] == n_pl]
        unique_circles = {u["peuples"] for u in n_units}
        assert len(unique_circles) == 20, f"Attendu 20 cercles orientés à N={n_pl}"
        assert all(u["is_mirror_pair"] is True for u in n_units)
        # Vérifier qu'aucun peuple n'est écrasé par M/R
        p_counts = Counter(p for u in n_units for p in u["peuples"])
        assert max(p_counts.values()) - min(p_counts.values()) <= 2

    # À 6J avec 60 paires miroirs : couvre les 60 cercles canoniques (120 orientés)
    pairs_6 = balanced_neighbor_mirror_pairs(6, min_animaux_sauvages=1, exp_seed=42)
    assert len(pairs_6) == 60


# ---------------------------------------------------------------------------
# 4. Stabilité d'appariement du paquet Machine (mélange par carte)
# ---------------------------------------------------------------------------


def test_machine_deck_shuffle_preserves_relative_order_when_sabotage_inserted() -> None:
    """Insérer 1..3 cartes Sabotage conserve strictement l'ordre relatif des autres cartes."""
    for seed in range(100):
        cfg = GameConfig(n_players=4, mode=2, exp_seed=5000 + seed, rep_id=seed)
        s0 = GameState(cfg)
        s0.sabotage_deck_count = 0
        s0.sabotage_pending_count = 0
        s0.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
        deck0 = [s0.draw_next_machine_card() for _ in range(s0.deck_len)]

        for n_sab in (1, 2, 3):
            s_sab = GameState(cfg)
            s_sab.sabotage_deck_count = 0
            s_sab.sabotage_pending_count = n_sab
            s_sab.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
            deck_sab = [s_sab.draw_next_machine_card() for _ in range(s_sab.deck_len)]
            assert deck_sab.count(CARD_SABOTAGE) == n_sab
            machines_only = [c for c in deck_sab if c != CARD_SABOTAGE]
            assert machines_only == deck0, (
                f"L'insertion de {n_sab} Sabotage(s) a décalé l'ordre relatif sur seed={seed}"
            )

        # Retirer une machine passée en Ratissage conserve aussi l'ordre relatif des autres
        s_rat = GameState(cfg)
        s_rat.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
        s_rat.rebuild_and_shuffle_machine_deck(increment_reshuffle=True)
        deck_rat = [s_rat.draw_next_machine_card() for _ in range(s_rat.deck_len)]
        expected_without_m0 = [c for c in deck0 if c != 1]  # card_code(0, ABATTEUSE) == 1
        assert deck_rat == expected_without_m0
        # Vérifier aussi que le Bulldozer du rayon 0 (code 2) reste bien présent
        assert 2 in deck_rat and MACHINE_BULLDOZER == 1


# ---------------------------------------------------------------------------
# 5. Invariant bout-en-bout 3.2 -> 5.2 & hygiène documentaire post-fusion
# ---------------------------------------------------------------------------


def test_bound_machines_3_2_to_5_2_invariant_zero_violations() -> None:
    """Toute machine liée à une Tactique en fin de 3.2 attaque avant la fin de 5.2 sauf si retirée."""
    total_checked = 0
    for idx in range(24):
        mode = (1, 2, 4)[idx % 3]
        n_pl = 3 + (idx % 4)
        cfg = GameConfig(
            n_players=n_pl,
            mode=mode,
            peuples=PEUPLES_ORDER[:n_pl],
            exp_seed=777000 + mode * 100,
            rep_id=idx,
            max_revision_passes=3,
        )
        st = GameState(cfg)
        trk = BoundAttackInvariantTracker()
        play_game_b2(st, k_max_passes=3, telemetry=trk)
        assert not trk.violations
        total_checked += trk.checked_bindings
    assert total_checked > 50


def test_historical_v5_5_digests_marked_biased_and_spec_aligned() -> None:
    """Les 6 digests v5.4.2-v5.5 entachés sont marqués biaisés et le résidu Souche est purgé."""
    idx_data = json.loads((ROOT / "docs" / "digests" / "index.json").read_text(encoding="utf-8"))
    by_id = {entry["id"]: entry for entry in idx_data["digests"]}
    expected_biased = (
        "calibration_reves_fixes_v5_4",
        "calibration_mobilisation_croisee_v5_4",
        "calibration_pari_max2_v5_4",
        "calibration_declencheurs_v5_4",
        "validation_socle_v5_5",
        "baseline_mode4_v5_5",
    )
    for d_id in expected_biased:
        assert d_id in by_id, f"Digest historique {d_id} absent de docs/digests/index.json"
        assert by_id[d_id].get("status") == "biased_legacy_v5_5"
        assert by_id[d_id].get("bias_notice")
        assert "[ARCHIVÉ — BIAISÉ v5.5]" in str(by_id[d_id].get("label", ""))

    for rel in (
        "docs/data/spec_formelle_v6_0.json",
        "docs/data/catalog_v6_0.json",
        "docs/data/amazonia_data_v6_0.js",
        "docs/data/livret_v6_0.js",
    ):
        txt = (ROOT / rel).read_text(encoding="utf-8")
        assert "arrachant la dernière Souche" not in txt, f"Résidu Souche trouvé dans {rel}"
