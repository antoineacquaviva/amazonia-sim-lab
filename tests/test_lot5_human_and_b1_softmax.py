"""Tests de validation du Lot 5 — Journalisation humaine `human_trace_1.0`, accord CRN et softmax B1."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import bots.heuristic_engine as he_mod
from bots.belief_and_ticks import build_belief_summary, softmax_select_index
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import (
    DEFAULT_TAU_B1,
    make_b1_scorer,
    play_game_b1,
    play_game_b2,
    score_target_b1,
    score_target_b2,
)
from bots.human_eval import (
    HUMAN_TRACE_SCHEMA_VERSION,
    HumanDecisionRecord,
    calibrate_tau_b1_on_human_traces,
    evaluate_bot_human_agreement,
    load_human_traces_jsonl,
    reconstruct_state_from_trace_record,
    record_human_decision_from_state,
    write_human_traces_jsonl,
)
from bots.human_eval import (
    main as human_eval_main,
)
from campaigns.designs import balanced_neighbor_mirror_tables
from engine.core_engine import (
    advance_step2_to_2_2,
    apply_step2_def1,
    list_legal_targets,
    step_until_decision,
)
from engine.state import (
    FACE_DEFINITIF,
    FACE_REFLEXION,
    STEP_2_1_DEF1,
    STEP_2_2_DEF2,
    GameConfig,
    GameState,
    tile_id_to_code,
)

REPO_ROOT = Path(__file__).resolve().parent.parent


def _prepare_step2_state(
    *,
    mode: int = 2,
    peuples: tuple[str, ...] = ("M", "R", "O", "H"),
    exp_seed: int = 505,
    rep_id: int = 0,
    step: int = STEP_2_1_DEF1,
) -> GameState:
    cfg = GameConfig(
        n_players=len(peuples),
        mode=mode,
        peuples=peuples,
        exp_seed=exp_seed,
        rep_id=rep_id,
    )
    st = GameState(cfg)
    step_until_decision(st)
    assert st.step == STEP_2_1_DEF1
    if step == STEP_2_2_DEF2:
        for seat in range(cfg.n_players):
            legal1 = list_legal_targets(st, seat, is_first_defender=True)
            obs = st.get_observation(seat)
            bel = build_belief_summary(obs, cfg)
            best1 = max(legal1, key=lambda t: score_target_b2(obs, cfg, bel, t, True))
            apply_step2_def1(st, seat, best1, check_legal=True)
        advance_step2_to_2_2(st)
        assert st.step == STEP_2_2_DEF2
    return st


def test_lot5_b1_forgetting_penalty_removed_and_softmax_active_at_zero_laws() -> None:
    """Lot 5 : `_b1_forgetting_penalty` est purgé et B1 applique son bruit softmax dès 0 loi active."""
    assert not hasattr(he_mod, "_b1_forgetting_penalty")
    assert DEFAULT_TAU_B1 > 0.0
    scorer = make_b1_scorer(DEFAULT_TAU_B1)
    assert scorer.softmax_tau == DEFAULT_TAU_B1

    # Vérifier softmax_select_index en Mode 2 (0 loi active) : déterministe et non dégénéré
    st = _prepare_step2_state(mode=2, exp_seed=510, rep_id=0)
    obs = st.get_observation(0)
    scores = [100.0, 95.0, 85.0, 40.0]

    # tau = 0.0 -> argmax strict et déterministe
    idx_greedy = softmax_select_index(scores, 0.0, st.cfg, obs, salt=7)
    assert idx_greedy == 0
    assert softmax_select_index(scores, 0.0, st.cfg, obs, salt=7) == idx_greedy

    # tau = DEFAULT_TAU_B1 -> déterministe à sel fixe, mais varie selon les sels (même à 0 loi)
    first_draw = softmax_select_index(scores, DEFAULT_TAU_B1, st.cfg, obs, salt=1)
    assert softmax_select_index(scores, DEFAULT_TAU_B1, st.cfg, obs, salt=1) == first_draw
    draws = {softmax_select_index(scores, DEFAULT_TAU_B1, st.cfg, obs, salt=s) for s in range(40)}
    assert len(draws) >= 2, f"Softmax doit explorer plusieurs cibles proches (draws={draws})"

    # En partie complète Mode 2 (0 loi active), B1(DEFAULT_TAU_B1) diverge de B1(tau=0.0)
    divergences = 0
    for rep in range(10):
        cfg = GameConfig(
            n_players=4,
            mode=2,
            peuples=("M", "R", "O", "H"),
            exp_seed=511,
            rep_id=rep,
        )
        r_noisy = play_game_b1(GameState(cfg), tau_b1=DEFAULT_TAU_B1)
        r_greedy = play_game_b1(GameState(cfg), tau_b1=0.0)
        if r_noisy.score_arbres != r_greedy.score_arbres or r_noisy.tour_fin != r_greedy.tour_fin:
            divergences += 1
    assert divergences >= 2, (
        f"B1 softmax doit rester actif à 0 loi (Mode 2), divergences={divergences}/10"
    )


def test_lot5_b1_softmax_determinism_and_hierarchy_mode2_and_mode4() -> None:
    """Lot 5 : B1 softmax est strictement déterministe et respecte B0 < B1 < B2 en Mode 2 et Mode 4."""
    # Déterminisme exact
    cfg_det = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "H"), exp_seed=520, rep_id=3)
    res_a = play_game_b1(GameState(cfg_det), tau_b1=DEFAULT_TAU_B1)
    res_b = play_game_b1(GameState(cfg_det), tau_b1=DEFAULT_TAU_B1)
    assert res_a == res_b

    # Hiérarchie B0 < B1(DEFAULT_TAU_B1) < B2 sur cercles équilibrés (Mode 2 = 0 loi active & Mode 4)
    tables = balanced_neighbor_mirror_tables(4, max_tables=6, exp_seed=521)
    for mode, reps_per_table in ((2, 2), (4, 1)):
        s_b0: list[float] = []
        s_b1: list[float] = []
        s_b2: list[float] = []
        for idx, (_lbl, peuples) in enumerate(tables):
            for r in range(reps_per_table):
                cfg = GameConfig(
                    n_players=4,
                    mode=mode,
                    peuples=peuples,
                    exp_seed=521 + mode * 10,
                    rep_id=idx * 10 + r,
                )
                s_b0.append(play_game_b0(GameState(cfg)).ratio_arbres)
                s_b1.append(play_game_b1(GameState(cfg), tau_b1=DEFAULT_TAU_B1).ratio_arbres)
                s_b2.append(play_game_b2(GameState(cfg)).ratio_arbres)
        m0 = sum(s_b0) / len(s_b0)
        m1 = sum(s_b1) / len(s_b1)
        m2 = sum(s_b2) / len(s_b2)
        assert m0 < m1 < m2, (
            f"Hiérarchie B0 < B1 < B2 rompue en Mode {mode} : B0={m0:.4f}, B1={m1:.4f}, B2={m2:.4f}"
        )


def test_lot5_human_trace_jsonl_roundtrip_and_strict_validation(tmp_path: Path) -> None:
    """Lot 5 : sérialisation JSONL `human_trace_1.0` sans perte via mutateurs publics et validation stricte."""
    st = _prepare_step2_state(
        mode=2,
        peuples=("M", "H", "I", "R"),
        exp_seed=530,
        rep_id=2,
        step=STEP_2_2_DEF2,
    )
    # Enrichir l'état pour vérifier le round-trip complet (Gardien, Rêve, Bugs, Colonie, Furtivité)
    st.set_gardien_at_case(2, 1, 1)
    st.set_tactique_at_rank(4, tile_id_to_code("R1"))
    st.set_bugs_at_case(3, 2)
    st.set_colonie_at_case(2, 1)
    st.place_defender_furtivite(1, 1, 1, 0, FACE_REFLEXION, preferred_twin=1)
    st.place_defender_gardien_pari(2, 2, FACE_DEFINITIF)
    st.place_defender_reve_activation(3, 5, FACE_REFLEXION, def_idx=1)

    seat = 0
    legal = list_legal_targets(st, seat, is_first_defender=False, exclude_own_def2=True)
    assert legal
    chosen = legal[0]

    rec = record_human_decision_from_state(
        st,
        seat,
        chosen,
        game_id="playtest_roundtrip",
        decision_id=1,
        player_level="expert",
        notes="test fidélité état",
    )
    jsonl_path = tmp_path / "traces.jsonl"
    write_human_traces_jsonl(jsonl_path, [rec])
    loaded = load_human_traces_jsonl(jsonl_path)
    assert len(loaded) == 1
    assert loaded[0] == rec

    rebuilt = reconstruct_state_from_trace_record(loaded[0])
    obs_orig = st.get_observation(seat)
    obs_rebuilt = rebuilt.get_observation(seat)
    assert obs_rebuilt.tour == obs_orig.tour
    assert obs_rebuilt.step == obs_orig.step
    assert obs_rebuilt.hand_of(seat) == obs_orig.hand_of(seat)
    assert obs_rebuilt.piste_tactiques == obs_orig.piste_tactiques
    assert obs_rebuilt.piste_gardiens == obs_orig.piste_gardiens
    assert obs_rebuilt.piste_colonie == obs_orig.piste_colonie
    assert [rebuilt.get_bugs_at_case(c) for c in range(1, 7)] == [
        st.get_bugs_at_case(c) for c in range(1, 7)
    ]
    assert obs_rebuilt.lisieres == obs_orig.lisieres
    assert obs_rebuilt.foret == obs_orig.foret
    assert obs_rebuilt.furtivite == obs_orig.furtivite
    assert obs_rebuilt.machines == obs_orig.machines
    for s_idx in range(st.cfg.n_players):
        assert rebuilt.get_player_def_loc_raw(s_idx, 0) == st.get_player_def_loc_raw(s_idx, 0)
        assert rebuilt.get_player_def_loc_raw(s_idx, 1) == st.get_player_def_loc_raw(s_idx, 1)
    assert list_legal_targets(rebuilt, seat, is_first_defender=False, exclude_own_def2=True) == legal

    # Validation stricte : rejet schema_version inconnu & action illégale
    bad_schema = rec.to_json_dict()
    bad_schema["schema_version"] = "human_trace_0.9"
    with pytest.raises(ValueError, match="schema_version"):
        HumanDecisionRecord.from_json_dict(bad_schema)

    bad_target = rec.to_json_dict()
    bad_target["chosen_target"] = ["FORET", 99, 9]
    with pytest.raises(ValueError, match="chosen_target"):
        HumanDecisionRecord.from_json_dict(bad_target)


def test_lot5_evaluate_bot_human_agreement_and_crn_regret() -> None:
    """Lot 5 : calcul top-1/top-k, rang moyen, log-vraisemblance et écart d'arbres CRN (2.1 et 2.2)."""
    records_b2: list[HumanDecisionRecord] = []
    records_subopt: list[HumanDecisionRecord] = []
    dec_id = 0
    for step in (STEP_2_1_DEF1, STEP_2_2_DEF2):
        is_first = step == STEP_2_1_DEF1
        for rep in range(3):
            st = _prepare_step2_state(mode=2, exp_seed=540, rep_id=rep, step=step)
            seat = rep % 4
            legal = list_legal_targets(
                st, seat, is_first_defender=is_first, exclude_own_def2=(not is_first)
            )
            obs = st.get_observation(seat)
            bel = build_belief_summary(obs, st.cfg)
            ranked_b2 = sorted(
                legal,
                key=lambda t: (-score_target_b2(obs, st.cfg, bel, t, is_first), legal.index(t)),
            )
            dec_id += 1
            records_b2.append(
                record_human_decision_from_state(
                    st, seat, ranked_b2[0], game_id="synth_b2", decision_id=dec_id
                )
            )
            records_subopt.append(
                record_human_decision_from_state(
                    st, seat, ranked_b2[-1], game_id="synth_subopt", decision_id=dec_id
                )
            )

    rep_b2 = evaluate_bot_human_agreement(
        records_b2,
        bots=("B0", "B1", "B2", "B2_OPEN"),
        top_k=3,
        n_crn_rollouts=4,
    )
    assert rep_b2["schema_version"] == HUMAN_TRACE_SCHEMA_VERSION
    assert rep_b2["n_decisions"] == len(records_b2)
    b2_stats = rep_b2["by_bot"]["B2"]
    assert b2_stats["top1_agreement"] == 1.0
    assert b2_stats["top3_agreement"] == 1.0
    assert b2_stats["mean_human_rank"] == 1.0
    assert b2_stats["mean_tree_gap_bot_minus_human"] == 0.0
    for bot_key in ("B0", "B1", "B2", "B2_OPEN"):
        st_bot = rep_b2["by_bot"][bot_key]
        assert 0.0 <= st_bot["top1_agreement"] <= st_bot["top3_agreement"] <= 1.0
        assert st_bot["mean_human_rank"] >= 1.0
        assert st_bot["mean_softmax_log_likelihood"] is not None
        assert st_bot["mean_tree_gap_bot_minus_human"] is not None

    # Sur traces humaines sous-optimales, B2 doit afficher un écart positif en arbres sauvés
    rep_sub = evaluate_bot_human_agreement(
        records_subopt, bots=("B2",), top_k=3, n_crn_rollouts=4
    )
    assert rep_sub["by_bot"]["B2"]["top1_agreement"] == 0.0
    assert rep_sub["by_bot"]["B2"]["mean_tree_gap_bot_minus_human"] > 0.0


def test_lot5_calibrate_tau_b1_distinguishes_sharp_vs_noisy_humans() -> None:
    """Lot 5 : la calibration MLE de `tau_b1` estime une température plus basse sur des traces précises."""
    sharp_records: list[HumanDecisionRecord] = []
    noisy_records: list[HumanDecisionRecord] = []
    for rep in range(6):
        st = _prepare_step2_state(mode=2, exp_seed=550, rep_id=rep, step=STEP_2_1_DEF1)
        seat = rep % 4
        legal = list_legal_targets(st, seat, is_first_defender=True)
        obs = st.get_observation(seat)
        bel = build_belief_summary(obs, st.cfg)
        ranked_b1 = sorted(
            legal,
            key=lambda t: (-score_target_b1(obs, st.cfg, bel, t, True), legal.index(t)),
        )
        sharp_records.append(
            record_human_decision_from_state(
                st, seat, ranked_b1[0], game_id="sharp", decision_id=rep + 1
            )
        )
        noisy_idx = min(len(ranked_b1) - 1, max(1, len(ranked_b1) // 2))
        noisy_records.append(
            record_human_decision_from_state(
                st, seat, ranked_b1[noisy_idx], game_id="noisy", decision_id=rep + 1
            )
        )

    fit_sharp = calibrate_tau_b1_on_human_traces(sharp_records)
    fit_noisy = calibrate_tau_b1_on_human_traces(noisy_records)
    assert fit_sharp["n_decisions"] == len(sharp_records)
    assert fit_noisy["n_decisions"] == len(noisy_records)
    assert fit_sharp["best_tau_b1"] < fit_noisy["best_tau_b1"], (
        f"sharp tau ({fit_sharp['best_tau_b1']}) doit être < noisy tau ({fit_noisy['best_tau_b1']})"
    )


def test_lot5_cli_and_static_html_logger_compatibility(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Lot 5 : CLI `bots.human_eval` et journaliseur HTML statique `docs/human_logger.html` compatibles."""
    html_path = REPO_ROOT / "docs" / "human_logger.html"
    assert html_path.is_file()
    raw_bytes = html_path.read_bytes()
    assert not raw_bytes.startswith(b"\xef\xbb\xbf"), "UTF-8 sans BOM obligatoire"
    assert b"\r" not in raw_bytes, "Fins de ligne LF uniquement"
    html_text = raw_bytes.decode("utf-8")
    assert HUMAN_TRACE_SCHEMA_VERSION in html_text
    assert "() => [1, 0]" in html_text

    # Simuler un enregistrement JSONL tel qu'exporté par docs/human_logger.html (legal_targets=[])
    html_like_record: dict[str, Any] = {
        "schema_version": HUMAN_TRACE_SCHEMA_VERSION,
        "game_id": "playtest_html_01",
        "decision_id": 1,
        "config": {
            "n_players": 4,
            "mode": 2,
            "peuples": ["M", "R", "O", "H"],
            "exp_seed": 42,
            "rep_id": 0,
            "tile_profiles": [],
        },
        "tour": 1,
        "step": STEP_2_1_DEF1,
        "seat": 0,
        "is_first_defender": True,
        "board_state": {
            "tour": 1,
            "step": STEP_2_1_DEF1,
            "coordonnateur": 0,
            "paravents_ouverts": False,
            "sabotage_deck_count": 0,
            "sabotage_pending_count": 0,
            "parcels": [
                [
                    {
                        "arbres": ar,
                        "souches": 0,
                        "insectes": 0,
                        "piege": 0,
                        "nid_id": 0,
                        "nid_active": 0,
                    }
                    for ar in (2, 2, 3, 3)
                ]
                for _ in range(4)
            ],
            "machines": [
                {
                    "ray": r,
                    "m_type": mt,
                    "pos": 2 if mt == 0 else 1,
                    "status": 0,
                    "pending_siege": 0,
                    "rouges": 0,
                    "bleus": 0,
                }
                for r in range(4)
                for mt in (0, 1)
            ],
            "hands": [[1, 2, 4, 2, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "piste_tactiques": [1, 2, 3, 4, 5, 6],
            "piste_gardiens": [[0, 1]] * 6,
            "lisieres": [[1, 0]] * 8,
            "defenders": [],
        },
        "legal_targets": [],
        "chosen_target": ["FORET", 0, 2],
        "player_level": "intermediaire",
        "notes": "protège la parcelle 2 contre l'Abatteuse en main",
    }
    jsonl_path = tmp_path / "html_export.jsonl"
    jsonl_path.write_text(
        json.dumps(html_like_record, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )

    rc_eval = human_eval_main(["evaluate", str(jsonl_path), "--rollouts", "2"])
    assert rc_eval == 0
    out_eval = json.loads(capsys.readouterr().out)
    assert out_eval["n_decisions"] == 1
    assert "B2" in out_eval["by_bot"]

    rc_fit = human_eval_main(["fit-tau", str(jsonl_path)])
    assert rc_fit == 0
    out_fit = json.loads(capsys.readouterr().out)
    assert out_fit["n_decisions"] == 1
    assert out_fit["best_tau_b1"] > 0.0
