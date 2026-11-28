"""Tests de régression et témoins dédiés aux correctifs d'audit (idempotence, dispatch Mode 4,
micro-forks, chronologie, composition d'effets, traçabilité Studio & CRN miroir)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import engine.effects  # noqa: F401
from bots.belief_and_ticks import build_belief_summary
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import _score_effect_option
from campaigns.designs import run_micro_fork_on_config
from campaigns.digest_builder import (
    DEFAULT_BUNDLE_PATH,
    build_active_core_rules,
    load_spec_bundle,
)
from campaigns.worker_main import (
    resolve_manifest_plan,
    run_campaign_manifest,
)
from engine.core_engine import (
    apply_choice,
    apply_repousse_finale,
    compute_parade_seuil,
    step_until_decision,
    sweep_gardiens,
)
from engine.primitives import DEC_EFFET_TUILE, DecisionRequest, GameOver
from engine.state import (
    FACE_DEFINITIF,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    STEP_3_1_CONSTRUCT,
    STEP_3_2_REVEAL,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT: Path = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# 1. Idempotence stricte de la Repousse Finale (score terminal stable)
# ---------------------------------------------------------------------------
def test_terminal_repousse_finale_idempotent_exact_audit_repro() -> None:
    """Relire un état fini est strictement idempotent (aucune seconde Repousse Finale)."""
    cfg = GameConfig(
        n_players=4,
        mode=1,
        peuples=("M", "R", "O", "H"),
        exp_seed=42,
        rep_id=0,
    )
    st = GameState(cfg)
    trk = TelemetryTracker()

    res1 = play_game_b0(st, max_steps=2000, telemetry=trk)
    bytes_after_end = st.raw_used_bytes()
    turns_measured_after_end = trk.turns_measured
    assert st.repousse_finale_applied is True
    assert st.get_observation(0).repousse_finale_applied is True

    res2 = step_until_decision(st, telemetry=trk)
    res3 = apply_repousse_finale(st)
    res4 = step_until_decision(st, telemetry=trk)

    assert isinstance(res2, GameOver)
    assert isinstance(res3, GameOver)
    assert isinstance(res4, GameOver)
    assert res1 == res2 == res3 == res4
    assert st.raw_used_bytes() == bytes_after_end
    assert trk.turns_measured == turns_measured_after_end


def test_terminal_repousse_finale_idempotent_mode3() -> None:
    """Idempotence vérifiée aussi en Mode 3 avec tuiles actives."""
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        exp_seed=1234,
        rep_id=2,
    )
    st = GameState(cfg)
    res1 = play_game_b0(st, max_steps=2000)
    raw1 = st.raw_used_bytes()
    res2 = step_until_decision(st)
    assert isinstance(res2, GameOver)
    assert res1 == res2
    assert st.raw_used_bytes() == raw1


# ---------------------------------------------------------------------------
# 2. Dispatch bot DEC_EFFET_TUILE par effect_kind (invariance de siège & anti-collision Canon 0 v6.2)
# ---------------------------------------------------------------------------
def test_bot_g6_a_shift_lecture_m_twin_position_seat_invariant() -> None:
    """Position jumelle Déviation Synaptique (±1) : suit le Rêve indépendamment du siège."""
    cfg = GameConfig(
        n_players=4,
        mode=4,
        peuples=("M", "R", "O", "H"),
        exp_seed=99,
    )

    for seat in range(4):
        st_a = GameState(cfg)
        st_a.step = STEP_3_2_REVEAL
        st_a.set_tactique_at_rank(0, 1)
        st_a.set_tactique_at_rank(1, 2)
        st_a.set_tactique_at_rank(2, TILE_R_BASE + 1)
        st_a.place_defender_reve_activation(seat, 3, 1)
        st_a.set_player_hand(seat, machine_card_code(seat, MACHINE_ABATTEUSE), 2, 1, 2, 2)

        obs_a = st_a.get_observation(seat)
        belief_a = build_belief_summary(obs_a, cfg)
        req_a = DecisionRequest(
            decision_type=DEC_EFFET_TUILE,
            decideur=seat,
            options=("M_MOINS_1", "M_PLUS_1", "PASSER"),
            context={
                "slot_id": "SLOT_BUG_CERVEAU",
                "effect_kind": "BUG_DEVIATION_SYNAPTIQUE_3_2",
                "case": 2,
                "target_seat": seat,
            },
        )
        sc_plus = _score_effect_option(obs_a, cfg, belief_a, req_a, "M_PLUS_1", is_b2=True)
        sc_minus = _score_effect_option(obs_a, cfg, belief_a, req_a, "M_MOINS_1", is_b2=True)
        assert sc_plus > sc_minus, f"Siège {seat} : M_PLUS_1 doit dévier la machine sur le Rêve défendu"

    for seat in range(4):
        st_b = GameState(cfg)
        st_b.step = STEP_3_2_REVEAL
        st_b.set_tactique_at_rank(0, TILE_R_BASE + 1)
        st_b.set_tactique_at_rank(1, 2)
        st_b.set_tactique_at_rank(2, 3)
        st_b.place_defender_reve_activation(seat, 1, 1)
        st_b.set_player_hand(seat, machine_card_code(seat, MACHINE_ABATTEUSE), 2, 1, 2, 2)

        obs_b = st_b.get_observation(seat)
        belief_b = build_belief_summary(obs_b, cfg)
        req_b = DecisionRequest(
            decision_type=DEC_EFFET_TUILE,
            decideur=seat,
            options=("M_MOINS_1", "M_PLUS_1", "PASSER"),
            context={
                "slot_id": "SLOT_BUG_CERVEAU",
                "effect_kind": "BUG_DEVIATION_SYNAPTIQUE_3_2",
                "case": 2,
                "target_seat": seat,
            },
        )
        sc_plus = _score_effect_option(obs_b, cfg, belief_b, req_b, "M_PLUS_1", is_b2=True)
        sc_minus = _score_effect_option(obs_b, cfg, belief_b, req_b, "M_MOINS_1", is_b2=True)
        assert sc_minus > sc_plus, f"Siège {seat} : M_MOINS_1 doit dévier la machine sur le Rêve défendu"


def test_bot_effect_option_dispatch_no_tuple_or_int_collisions() -> None:
    """Vérifie que les effect_kind actifs Canon 0 (machine, rayon, Rêve, parcelle) ne collident pas."""
    cfg = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "H"), exp_seed=77)
    st = GameState(cfg)
    st.step = STEP_3_2_REVEAL
    st.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=3, bleus=0)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, rouges=0, bleus=0)
    st.set_parcel_arbres_souches(0, 1, 0, 0)
    st.set_parcel_arbres_souches(1, 1, 2, 0)
    st.set_gardien_at_case(1, 1, face=1)
    st.set_tactique_at_rank(0, 1)
    st.set_tactique_at_rank(1, 6)
    st.set_tactique_at_rank(2, 2)
    st.set_tactique_at_rank(3, TILE_R_BASE + 1)

    obs = st.get_observation(0)
    belief = build_belief_summary(obs, cfg)

    # 1. Machine pair (ray=0, m_type=1 Bulldozer) ne doit PAS être jugée comme parcelle (0, 1) rasée
    req_mach = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=((0, MACHINE_BULLDOZER), (1, MACHINE_ABATTEUSE)),
        context={"slot_id": "G6", "effect_kind": "G6_REFROIDIR"},
    )
    sc_bull = _score_effect_option(obs, cfg, belief, req_mach, (0, MACHINE_BULLDOZER), is_b2=True)
    sc_abat = _score_effect_option(obs, cfg, belief, req_mach, (1, MACHINE_ABATTEUSE), is_b2=True)
    assert sc_bull > sc_abat

    # 2. Glissement de pari Gardien (G4_FIRST_CRI : case avec 1 pari restant prioritaire sur 2 paris)
    st.set_gardien_at_case(2, 2, face=1)
    st.set_gardien_at_case(4, 3, face=1)
    st.place_defender_gardien_pari(0, 2, 1)
    st.place_defender_gardien_pari(1, 4, 1)
    st.place_defender_gardien_pari(2, 4, 1)
    obs2 = st.get_observation(0)
    belief2 = build_belief_summary(obs2, cfg)
    req_g4 = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=(2, 4),
        context={"slot_id": "G4", "effect_kind": "G4_FIRST_CRI", "g4_case": 1},
    )
    assert _score_effect_option(obs2, cfg, belief2, req_g4, 2, is_b2=True) > _score_effect_option(
        obs2, cfg, belief2, req_g4, 4, is_b2=True
    )

    # 3. Glissement Rêve Canon 0 (G12_SLIDE_REVE) : le rang portant un Rêve obtient un score > PASSER
    req_g12 = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=(3, "PASSER"),
        context={"slot_id": "G12", "effect_kind": "G12_SLIDE_REVE", "steps": 1},
    )
    assert _score_effect_option(obs, cfg, belief, req_g12, 3, is_b2=True) > _score_effect_option(
        obs, cfg, belief, req_g12, "PASSER", is_b2=True
    )


# ---------------------------------------------------------------------------
# 3. Micro-Fork : politique future identique & ancre inatteignable -> None
# ---------------------------------------------------------------------------
def test_micro_fork_zero_delta_when_no_divergence_and_unreachable_anchor() -> None:
    """Si 0 mouvement en 2.2 -> écart exact = 0.0 ; ancre inatteignable retourne None."""
    cfg = GameConfig(
        n_players=3,
        mode=1,
        peuples=("M", "E", "I"),
        exp_seed=42,
        rep_id=0,
        max_revision_passes=3,
    )
    rec = run_micro_fork_on_config(
        cfg,
        target_tour=2,
        is_b2=True,
        n_selection_rollouts=3,
        n_eval_rollouts=4,
    )
    assert rec is not None
    if not rec.diverged_in_2_2:
        assert rec.v_k0_priv_eval == rec.v_k3_priv_eval
        assert rec.delta_v_negociation == 0.0
        assert rec.g_naive_selection == 0.0
        assert rec.g_unbiased_eval == 0.0

    assert run_micro_fork_on_config(cfg, target_tour=99, is_b2=True) is None


# ---------------------------------------------------------------------------
# 4. Chronologie 3.1 -> 3.2 -> 4.1, témoin d'interaction et synchronisation digest
# ---------------------------------------------------------------------------
def test_chronology_witness_3_1_reve_cancels_3_2_machine_and_preserves_4_1_m_r() -> None:
    """Témoin chronologique jumeau : un Rêve activé en 3.2 annule la machine et sauve la parcelle en 5.1,
    tout en conservant m(r) indépendant de l'annulation par Rêve en 4.1."""

    def _run_twin(*, build_reve_in_3_1: bool) -> tuple[int, int, tuple[int, ...]]:
        cfg = GameConfig(
            n_players=4,
            mode=3,
            peuples=("M", "R", "O", "H"),
            tile_profiles=(("R1", "A"),),
            exp_seed=505,
        )
        st = GameState(cfg)
        st.step = STEP_3_1_CONSTRUCT
        st.step2_locked = True
        st.coordonnateur = 0

        for idx in range(6):
            st.set_tactique_at_rank(idx, idx + 1)

        reve_slot: int | None = None
        for slot_idx, tid in enumerate(cfg.lisiere_slots):
            if tid.startswith("R"):
                reve_slot = slot_idx
                break
        assert reve_slot is not None
        if build_reve_in_3_1:
            r_num = int(cfg.lisiere_slots[reve_slot][1:])
            st.set_tactique_at_rank(5, TILE_R_BASE + r_num)
            st.place_defender_reve_activation(1, 6, FACE_DEFINITIF)
        st.set_lisiere_tile_state(reve_slot, LISIERE_UNCONSTRUCTED, 0)

        st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 1, 6, 0)
        for s in (1, 2, 3):
            st.set_player_hand(s, 0, 1, 1, 1, 0)

        st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
        st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
        st.place_defender_furtivite(0, 0, 0, 1, FACE_DEFINITIF)
        st.place_defender_furtivite(2, 1, 0, 1, FACE_DEFINITIF)

        for _ in range(16):
            req = step_until_decision(st)
            if isinstance(req, GameOver) or st.tour > 1:
                break
            apply_choice(st, "PASSER" if "PASSER" in req.options else req.options[0])

        return (
            st.sabotage_deck_count,
            st.get_parcel_arbres(0, 4),
            tuple(st.get_tactique_at_rank(i) for i in range(6)),
        )

    sab_with, arbres_with, track_with = _run_twin(build_reve_in_3_1=True)
    sab_without, arbres_without, track_without = _run_twin(build_reve_in_3_1=False)

    assert any(code >= TILE_R_BASE for code in track_with)
    assert sab_with == 0
    assert arbres_with == 3

    assert not any(code >= TILE_R_BASE for code in track_without)
    assert sab_without == 0
    assert arbres_without < arbres_with


def test_inter_effect_composition_witness_g1_a_then_g2_a_updates_parade() -> None:
    """Témoin de composition d'effets Mode 4 : G1 (rouge->bleu) puis G2 (recul machine) mettent à jour le seuil."""
    from engine.effects.registry import clear_tile_registry, register_tile
    from engine.primitives import (
        HOOK_GARDIEN_OUVERTURE,
        prim_deplacement,
        prim_mod_puissance,
    )

    clear_tile_registry()
    try:
        @register_tile("G1", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
        def _mock_g1(state: GameState, hook: str, context: dict[str, object]) -> None:
            del context
            if hook == HOOK_GARDIEN_OUVERTURE:
                prim_mod_puissance(state, 0, MACHINE_ABATTEUSE, flip_rouge_to_bleu=1)

        @register_tile("G2", "A", hooks=(HOOK_GARDIEN_OUVERTURE,))
        def _mock_g2(state: GameState, hook: str, context: dict[str, object]) -> None:
            del context
            if hook == HOOK_GARDIEN_OUVERTURE:
                prim_deplacement(
                    state, "MACHINE", src_ray=0, dst_ray=0, dst_p=2, m_type=MACHINE_ABATTEUSE
                )

        cfg = GameConfig(
            n_players=4,
            mode=3,
            peuples=("M", "R", "O", "H"),
            tile_profiles=(("G1", "A"), ("G2", "A")),
            exp_seed=606,
        )
        st = GameState(cfg)
        st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
        st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
        st.set_parcel_defenseurs(0, 3, 1)

        # Mode ASSAUT (T4) : p=3 (base 3) + 2 rouges = 5
        seuil_avant = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[4])
        assert seuil_avant == 5

        st.set_gardien_at_case(1, 1, face=1)
        st.set_gardien_at_case(2, 2, face=1)
        st.place_defender_gardien_pari(0, 1, 2)
        st.place_defender_gardien_pari(1, 2, 2)
        st.light_trigger(1)
        assert sweep_gardiens(st) == 1
        assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)

        st.light_trigger(2)
        assert sweep_gardiens(st) == 1
        pos_after, _, _ = st.get_machine_pos_status(0, MACHINE_ABATTEUSE)
        assert pos_after == 2

        # Composition : nouvelle position p=2 (base 2) + 1 rouge - 1 bleu = 2
        seuil_apres = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, pos_after, TACTIQUES_SPEC[4])
        assert seuil_apres == 2
    finally:
        from engine.core_engine import ensure_builtin_migration_registered
        from engine.effects import load_all_effects

        clear_tile_registry()
        ensure_builtin_migration_registered()
        load_all_effects()


def test_digest_active_core_rules_chronology_matches_v6_2() -> None:
    """Vérifie que build_active_core_rules expose la chronologie canonique (Construction -> Ouverture -> Furtivité)."""
    rules = build_active_core_rules()
    etapes = rules["spec_formelle"]["etapes_1_a_6"]
    keys = list(etapes.keys())
    assert keys[2] == "etape_3_CONSTRUCTION_ET_REVELATION"
    assert keys[3] == "etape_4_FURTIVITE_ET_PRODUCTION_ESSAIM"
    assert "Construction" in etapes[keys[2]] and "ouverture" in etapes[keys[2]].lower()
    assert "Furtivité" in etapes[keys[3]]
    assert not any("REVELATION_ET_FURTIVITE" in k for k in keys)


# ---------------------------------------------------------------------------
# 5. Traçabilité complète (amazonia_data_v6_0.js + livret_v6_0.js + spec_bundle_sha256) & economie_bot
# ---------------------------------------------------------------------------
def test_traceability_hashes_and_economie_bot_fixes() -> None:
    """Vérifie le verrouillage SHA-256 complet et les flux du graphe economie_bot Canon v6.4."""
    lock = json.loads((ROOT / "data" / "studio_lock.json").read_text(encoding="utf-8"))
    js_sha = hashlib.sha256((ROOT / "docs" / "data" / "amazonia_data_v6_0.js").read_bytes()).hexdigest()
    livret_sha = hashlib.sha256((ROOT / "docs" / "data" / "livret_v6_0.js").read_bytes()).hexdigest()
    bundle_sha = hashlib.sha256(DEFAULT_BUNDLE_PATH.read_bytes()).hexdigest()

    assert lock["files"]["amazonia_data_v6_0.js"]["sha256"] == js_sha
    assert lock["files"]["livret_v6_0.js"]["sha256"] == livret_sha

    bundle = load_spec_bundle()
    assert bundle["meta"]["studio_sha256"]["amazonia_data_v6_0.js"]["sha256"] == js_sha
    assert bundle["meta"]["studio_sha256"]["livret_v6_0.js"]["sha256"] == livret_sha

    rules = build_active_core_rules()
    assert rules["studio_sha256"]["amazonia_data_v6_0.js"] == js_sha
    assert rules["studio_sha256"]["livret_v6_0.js"] == livret_sha
    assert rules["spec_bundle_sha256"] == bundle_sha

    profiles_by_key = {
        (slot_id, prof_letter): prof_data["economie_bot"]
        for slot_id, slot_data in bundle["catalogue_tuiles"].items()
        for prof_letter, prof_data in slot_data["profils"].items()
    }
    assert len(profiles_by_key) == 30
    assert "RES_JETON_BLEU" in profiles_by_key[("G1", "A")]["outputs_produits"]
    assert "RES_PIEGE" in profiles_by_key[("G1", "A")]["outputs_produits"]
    assert "RES_JETON_ROUGE" in profiles_by_key[("G6", "A")]["inputs_requis"]
    assert "RES_JETON_BLEU" in profiles_by_key[("G6", "A")]["outputs_produits"]
    assert "RES_INSECTE" in profiles_by_key[("G14", "A")]["inputs_requis"]
    assert "RES_PIEGE" in profiles_by_key[("G14", "A")]["outputs_produits"]
    assert "RES_DILUTION_SABOTAGE" in profiles_by_key[("G10", "A")]["outputs_produits"]
    assert "RES_INSECTE" in profiles_by_key[("M4", "A")]["inputs_requis"]
    assert "RES_DEFENSEUR" in profiles_by_key[("M4", "A")]["outputs_produits"]
    assert "RES_SOUCHE" in profiles_by_key[("R2", "A")]["inputs_requis"]
    assert "RES_ARBRE" in profiles_by_key[("R2", "A")]["outputs_produits"]


# ---------------------------------------------------------------------------
# 6. CRN miroirs et agrégats DuckDB Mode 4 enrichis
# ---------------------------------------------------------------------------
def test_manifest_crn_mirror_and_duckdb_mode4(tmp_path: Path, monkeypatch: Any) -> None:
    """Vérifie l'appariement CRN miroir et les métriques DuckDB Mode 4 sur P4_2233."""
    manifest: dict[str, Any] = {
        "campaign_name": "audit_crn_check",
        "description": "Validation CRN miroir & métriques Mode 4",
        "player_counts": [4],
        "games_per_configuration": 4,
        "bot": "B0",
        "mode": 4,
        "slot_profile_comparisons": {"G7": ["A", "NEUTRE"]},
        "base_instance": {
            "bundle_id": "STANDARD_A",
            "peuples_cercle": ["M", "R", "O", "H"],
        },
    }
    plan = resolve_manifest_plan(manifest)
    assert plan["base_bundle_id"] == "STANDARD_A"
    assert len(plan["base_tile_profiles"]) == 32
    assert len(plan["resolved_32_slots_sha256"]) == 64
    assert plan["profil_piste"] == "P4_2233"

    for v_id in ("G7:A", "G7:NEUTRE"):
        v_units = [u for u in plan["units"] if u["variant_id"] == v_id]
        assert len(v_units) == 2
        assert v_units[0]["rep_start"] == 0
        assert v_units[1]["rep_start"] == 0
        assert v_units[0]["is_mirror_pair"] is True
        assert v_units[1]["is_mirror_pair"] is True

    manifest_file = tmp_path / "audit_crn_check.json"
    manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
    shards_dir = tmp_path / "shards"
    assert run_campaign_manifest(
        manifest_source=str(manifest_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    ) == 0

    import campaigns.digest_builder as db_mod
    import run_campaign as rc_mod

    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", tmp_path / "digests")
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    _, _, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=tmp_path / "cells.parquet",
        backend="cloudrun",
        job_name="amazonia-audit-test",
        tasks=1,
        job_wall_sec=0.5,
        run_id="20261119T000000Z_deadbeef",
        gcs_prefix="campaigns/audit_crn_check/20261119T000000Z_deadbeef",
    )
    assert "table_cvar20_ratio" in digest["totals"]
    assert "cvar20_ci95_low" in digest["totals"]
    assert "cvar20_ci95_high" in digest["totals"]
    assert "survival_rate" not in digest["totals"]
    assert "mean_physical_ops" in digest["telemetry"]
    assert "mean_player_decisions" in digest["telemetry"]
    assert digest["telemetry"]["mean_physical_ops"] > 0
    assert digest["telemetry"]["mean_player_decisions"] > 0
    assert digest["mode4_catalog"]["base_bundle_id"] == "STANDARD_A"
    assert digest["mode4_catalog"]["n_resolved_slots"] == 32
    assert digest["execution"]["run_id"] == "20261119T000000Z_deadbeef"
