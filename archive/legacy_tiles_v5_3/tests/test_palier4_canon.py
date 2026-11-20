"""Tests unitaires et d'intégration déterministes du Palier 4 (MAP-Elites, Shapley, B3 & DuckDB)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import engine.effects  # noqa: F401
from bots import BotB3, choose_b3, play_game_b3
from bots.bot_b3_rh import determinize_state_from_obs
from campaigns.designs import MANDATORY_6_CIRCLES, mirror_peuples
from campaigns.map_elites import (
    ADJACENT_16_SLOT_PAIRS,
    CANONICAL_32_SLOTS,
    GenomeEvaluation,
    MapElitesArchive2D,
    ShapleySurrogateOrder2,
    build_127_circular_tables,
    build_diverse_seed_genomes,
    cognitive_complexity_x,
    decode_genome_key,
    encode_genome_key,
    genome_to_tile_profiles,
    load_catalog_slot_profiles,
    load_mode3_reference_genome,
    mutate_genome_shapley_70_30,
    shannon_entropy_3_ends,
)
from campaigns.worker_main import (
    run_campaign_palier4_phase_a,
    run_campaign_palier4_phase_b,
)
from engine.core_engine import step_until_decision
from engine.primitives import DecisionRequest, GameOver
from engine.state import (
    CARD_SABOTAGE,
    MATRICE_PAIRES,
    PEUPLES_ORDER,
    GameConfig,
    GameState,
    machine_card_code,
)
from scripts_cloud.run_palier4_cloud import (
    BATCH_MACHINE_TYPE,
    BATCH_MAX_RUN_DURATION,
    MAX_PALIER4_DIGEST_BYTES,
    build_cloud_batch_job_spec,
    synthesize_palier4_with_duckdb,
)


def _canon_rot(peuples: tuple[str, ...]) -> tuple[str, ...]:
    rmap = {code: idx for idx, code in enumerate(PEUPLES_ORDER)}
    best = min(range(len(peuples)), key=lambda i: rmap[peuples[i]])
    return peuples[best:] + peuples[:best]


def test_b3_determinization_zero_leak_and_reproducibility() -> None:
    """Vérifie que B3 opère sans la moindre fuite des mains adverses ni de l'ordre secret du paquet."""
    tp = genome_to_tile_profiles(load_mode3_reference_genome())
    cfg = GameConfig(
        n_players=4,
        mode=4,
        peuples=("M", "R", "O", "H"),
        tile_profiles=tp,
        exp_seed=20264444,
        rep_id=3,
        max_revision_passes=3,
    )
    st = GameState(cfg)
    out = step_until_decision(st, max_internal_steps=2000)
    while isinstance(out, DecisionRequest) and st.paravents_ouverts:
        c = choose_b3(st, out, n_determinizations=1, horizon_turns=1)
        from engine.core_engine import apply_choice

        apply_choice(st, c)
        out = step_until_decision(st, max_internal_steps=2000)

    assert isinstance(out, DecisionRequest)
    assert not st.paravents_ouverts
    seat = out.decideur

    s1 = st.clone()
    s2 = st.clone()

    # Altérer lourdement sur `s2` les mains adverses masquées ET l'ordre secret du paquet Machine
    for opp in range(cfg.n_players):
        if opp == seat:
            continue
        cur_c, _, _, _, _ = s2.get_player_hand(opp)
        if cur_c != 0:
            if opp % 2 == 0:
                s2.set_player_hand(opp, CARD_SABOTAGE, 0, 0, 0, 0)
            else:
                s2.set_player_hand(opp, machine_card_code(opp, 0), 6, 5, 5, 1)

    orig_rem = s1.get_observation(seat).deck_remaining_count
    orig_sab = s1.sabotage_deck_count
    orig_pend = s1.sabotage_pending_count
    # Forcer un remélange secret différent sur `s2` puis restaurer les compteurs publics
    s2.reshuffle_count += 3
    s2.rebuild_and_shuffle_machine_deck(increment_reshuffle=False)
    s2.reshuffle_count -= 3
    s2.sabotage_deck_count = orig_sab
    s2.sabotage_pending_count = orig_pend
    s2.deck_cursor = max(0, s2.deck_len - orig_rem)

    obs1 = s1.get_observation(seat)
    obs2 = s2.get_observation(seat)
    assert obs1 == obs2

    det1 = determinize_state_from_obs(s1, obs1, det_idx=0)
    det2 = determinize_state_from_obs(s2, obs2, det_idx=0)
    assert det1.raw_used_bytes() == det2.raw_used_bytes()
    assert BotB3.choose_from_determinized(s1, obs1, out) == BotB3.choose_from_determinized(
        s2, obs2, out
    )
    assert choose_b3(s1, out) == choose_b3(s2, out)

    # Partie complète B3 déterministe en Mode 4
    g1 = play_game_b3(GameState(cfg), n_determinizations=1, horizon_turns=1)
    g2 = play_game_b3(GameState(cfg), n_determinizations=1, horizon_turns=1)
    assert isinstance(g1, GameOver)
    assert g1 == g2


def test_127_circular_tables_and_descriptors() -> None:
    """Contrôle la suite exacte de 127 tables circulaires (N=3..6) et les descripteurs 2D."""
    tables = build_127_circular_tables()
    assert len(tables) == 127
    assert {t.n_players for t in tables} == {3, 4, 5, 6}

    table_peuples = {_canon_rot(t.peuples) for t in tables}
    for _, mand in MANDATORY_6_CIRCLES:
        assert _canon_rot(mand) in table_peuples
        assert _canon_rot(mirror_peuples(mand)) in table_peuples

    present_slots = {"SLOT_BUG_CERVEAU", "SLOT_COLONISATION_GARDIENS"}
    for t in tables:
        n = t.n_players
        for i in range(n):
            a, b = MATRICE_PAIRES[f"{t.peuples[i]}_{t.peuples[(i + 1) % n]}"]
            present_slots.add(a)
            present_slots.add(b)
    assert present_slots == set(CANONICAL_32_SLOTS)
    assert len(ADJACENT_16_SLOT_PAIRS) == 16

    assert shannon_entropy_3_ends(20, 0, 0) == 0.0
    assert math.isclose(shannon_entropy_3_ends(15, 15, 15), 1.0, rel_tol=1e-9)
    h_mid = shannon_entropy_3_ends(20, 10, 5)
    assert 0.5 < h_mid < 1.0

    x_lo = cognitive_complexity_x(1.0, 0.2, 5.0, 0.2)
    x_hi = cognitive_complexity_x(9.0, 1.5, 9.0, 2.2)
    assert 0.0 <= x_lo < x_hi <= 1.0


def test_map_elites_archive_and_shapley_70_30() -> None:
    """Vérifie la grille MAP-Elites 2D, la décomposition ANOVA de Shapley d'ordre 2 et le ratio 70/30."""
    cat = load_catalog_slot_profiles()
    assert sum(len(v) for v in cat.values()) == 100

    seeds = build_diverse_seed_genomes(40, exp_seed=20264222)
    # Synthétiser une cible avec fort bonus sur G1:B et forte synergie sur la paire voisine (G1:B, G2:C)
    targets: list[float] = []
    for g in seeds:
        y = 0.50
        if g[0] == "B":
            y += 0.20
        if g[0] == "B" and g[1] == "C":
            y += 0.25
        targets.append(y)

    surr = ShapleySurrogateOrder2(ridge_lambda=1.0)
    surr.fit(seeds, targets)
    assert surr.is_fitted

    # Centrage ANOVA exact : somme nulle des effets principaux sur chacun des 32 emplacements
    for s in CANONICAL_32_SLOTS:
        s_sum = sum(surr.phi_main[(s, p)] for p in cat[s])
        assert abs(s_sum) < 1e-9

    # Marges nulles sur chacune des 16 paires d'interactions d'ordre 2
    for sa, sb in ADJACENT_16_SLOT_PAIRS:
        for pa in cat[sa]:
            row_sum = sum(surr.phi_pair[(sa, pa, sb, pb)] for pb in cat[sb])
            assert abs(row_sum) < 1e-9
        for pb in cat[sb]:
            col_sum = sum(surr.phi_pair[(sa, pa, sb, pb)] for pa in cat[sa])
            assert abs(col_sum) < 1e-9

    assert surr.phi_main[("G1", "B")] > surr.phi_main[("G1", "A")]
    best_g1_g2 = max(
        ((pa, pb) for pa in cat["G1"] for pb in cat["G2"]),
        key=lambda ab: surr.phi_pair[("G1", ab[0], "G2", ab[1])],
    )
    assert best_g1_g2 == ("B", "C")
    assert surr.phi_pair[("G1", "B", "G2", "C")] > 0.01

    # Vérifier le partage ~70 % guidé / ~30 % exploration uniforme sur 200 tirages indépendants
    ref_g = load_mode3_reference_genome()
    guided_flags = [
        mutate_genome_shapley_70_30(
            ref_g, surr, seen_keys=None, exp_seed=20264333, gen_idx=1, mut_idx=m_i
        )[1]
        for m_i in range(200)
    ]
    guided_ratio = sum(1 for fl in guided_flags if fl) / len(guided_flags)
    assert 0.60 <= guided_ratio <= 0.80

    # Vérifier l'archive MAP-Elites 2D et l'extraction du front de Pareto
    arch = MapElitesArchive2D(n_bins_x=8, n_bins_y=8)

    def _dummy_ev(gk_idx: int, x_c: float, ent: float, fit: float) -> GenomeEvaluation:
        g = seeds[gk_idx]
        gk = encode_genome_key(g)
        assert decode_genome_key(gk) == g
        return GenomeEvaluation(
            genome_key=gk,
            genome=g,
            chassis_id=19,
            n_tables=127,
            n_games=127,
            mean_ratio_arbres=fit,
            median_table_ratio=fit,
            cvar20_tables=fit,
            by_n_mean_ratio={3: fit, 4: fit, 5: fit, 6: fit},
            by_n_cvar20={3: fit, 4: fit, 5: fit, 6: fit},
            mirror_asymmetry_mean=0.02,
            mean_tours=6.5,
            pct_tour_8=40.0,
            pct_reve_rang_1=35.0,
            pct_reveil_gardiens=25.0,
            shannon_entropy=ent,
            mem_debt_mean=2.0,
            law_stack_mean=0.4,
            law_stack_max=2,
            fiddliness_mean=5.5,
            cascade_sweeps_mean=0.5,
            mid_combat_interrupts_mean=0.1,
            x_cognitive=x_c,
            cell_fitness=fit,
            editorial_score=fit + 0.18 * ent - 0.16 * x_c,
            cpu_sec=0.1,
        )

    e_weak = _dummy_ev(0, 0.30, 0.80, 0.45)
    e_strong_same_cell = _dummy_ev(1, 0.31, 0.81, 0.62)
    e_dominated = _dummy_ev(2, 0.70, 0.40, 0.40)
    assert arch.add(e_weak)
    assert arch.add(e_strong_same_cell)
    assert not arch.add(e_weak)
    assert arch.add(e_dominated)
    assert len(arch.cells) == 2

    front = arch.pareto_front()
    assert len(front) == 1
    assert front[0].genome_key == e_strong_same_cell.genome_key


def test_palier4_batch_spec_and_end_to_end_synthesis(tmp_path: Path) -> None:
    """Teste la spec Cloud Batch Spot et la chaîne complète Phase A -> Phase B -> DuckDB -> Canon & Digest < 30 Ko."""
    spec = build_cloud_batch_job_spec(["--campaign-palier4-phase-b", "--workers=4"], task_count=4, parallelism=4)
    inst_pol = spec["allocationPolicy"]["instances"][0]["policy"]
    assert inst_pol["machineType"] == BATCH_MACHINE_TYPE
    assert inst_pol["provisioningModel"] == "SPOT"
    assert spec["taskGroups"][0]["taskSpec"]["maxRunDuration"] == BATCH_MAX_RUN_DURATION

    shards_dir = tmp_path / "shards"
    parquet_path = tmp_path / "cells.parquet"
    canon_path = tmp_path / "canon_unique_32.json"
    digests_dir = tmp_path / "digests"

    rc_a = run_campaign_palier4_phase_a(
        chassis_ids_csv="0,19",
        base_reps=1,
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=shards_dir.as_posix(),
    )
    assert rc_a == 0

    rc_b = run_campaign_palier4_phase_b(
        chassis_id=19,
        islands=1,
        n_init=2,
        n_generations=1,
        batch_per_gen=1,
        reps_127=1,
        top_finalists_k=1,
        depth_reps=1,
        fast_smoke=True,
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=shards_dir.as_posix(),
    )
    assert rc_b == 0

    canon_doc, full_digest = synthesize_palier4_with_duckdb(
        job_wall_sec=1.25,
        execution_mode="local",
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        canon_json_path=canon_path,
        digests_dir=digests_dir,
    )
    assert parquet_path.exists()
    assert canon_path.exists()
    assert len(canon_doc["selections"]) == 32
    assert len(canon_doc["canon_32_list"]) == 32

    digest_file = digests_dir / "digest_palier4_canon.json"
    prompt_file = digests_dir / "PROMPT_GEMINI_palier4_canon.md"
    assert digest_file.exists() and prompt_file.exists()
    assert len(digest_file.read_bytes()) < MAX_PALIER4_DIGEST_BYTES
    loaded = json.loads(digest_file.read_text(encoding="utf-8"))
    assert "active_core_rules" in loaded
    assert len(loaded["tested_tiles_rules"]) == 32
    assert loaded["campaign"] == full_digest["campaign"] == "palier4_canon"
