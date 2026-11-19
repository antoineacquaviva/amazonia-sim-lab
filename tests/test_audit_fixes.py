"""Tests de régression et témoins dédiés aux correctifs issus de l'audit externe (v5.3)."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import engine.effects  # noqa: F401
from bots.belief_and_ticks import build_belief_summary
from bots.bot_b0 import play_game_b0
from bots.heuristic_engine import _score_effect_option
from campaigns.designs import run_micro_fork_on_config
from campaigns.digest_builder import (
    DEFAULT_BUNDLE_PATH,
    axes_dict_to_chassis_id,
    build_active_core_rules,
    chassis_id_to_studio_index_384,
    load_spec_bundle,
    studio_index_384_to_chassis_id,
)
from campaigns.worker_main import (
    _execute_micro_fork_unit,
    build_shuffled_halving_cohorts,
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
    """Repro exacte de l'audit (B0, N=4, mode 1, graine 42, rep 0) : relire un état fini est idempotent."""
    cfg = GameConfig.from_chassis_index(
        0,
        n_players=4,
        mode=1,
        peuples=("M", "R", "O", "H"),
        exp_seed=42,
        rep_id=0,
    )
    st = GameState(cfg)
    trk = TelemetryTracker()

    res1 = play_game_b0(st, max_steps=2000, chassis_id=0, telemetry=trk)
    bytes_after_end = st.raw_used_bytes()
    turns_measured_after_end = trk.turns_measured
    assert st.repousse_finale_applied is True
    assert st.get_observation(0).repousse_finale_applied is True

    # Appels répétés sur l'état terminal : aucune seconde Repousse Finale ni mutation d'état
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
    cfg = GameConfig.from_chassis_index(
        0,
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        exp_seed=1234,
        rep_id=2,
    )
    st = GameState(cfg)
    res1 = play_game_b0(st, max_steps=2000, chassis_id=0)
    raw1 = st.raw_used_bytes()
    res2 = step_until_decision(st)
    assert isinstance(res2, GameOver)
    assert res1 == res2
    assert st.raw_used_bytes() == raw1


# ---------------------------------------------------------------------------
# 2. Dispatch bot DEC_EFFET_TUILE par effect_kind (positions jumelles G6:A & anti-collision)
# ---------------------------------------------------------------------------
def test_bot_g6_a_shift_lecture_m_twin_position_seat_invariant() -> None:
    """Position jumelle G6:A : (seat, +1) / (seat, -1) suit le Rêve, jamais une parcelle (seat, 1)."""
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G6", "A"),),
        exp_seed=99,
    )

    # Cas A : Rêve en rang 3 (index 2) -> depuis lecture M=2, +1 annule la machine !
    for seat in range(4):
        st_a = GameState(cfg)
        st_a.step = STEP_3_2_REVEAL
        st_a.set_tactique_at_rank(0, 1)
        st_a.set_tactique_at_rank(1, 2)
        st_a.set_tactique_at_rank(2, TILE_R_BASE + 1)
        st_a.set_player_hand(seat, machine_card_code(seat, MACHINE_ABATTEUSE), 2, 1, 2, 2)

        obs_a = st_a.get_observation(seat)
        belief_a = build_belief_summary(obs_a, cfg)
        req_a = DecisionRequest(
            decision_type=DEC_EFFET_TUILE,
            decideur=seat,
            options=((seat, -1), (seat, 1), "PASSER"),
            context={"slot_id": "G6", "effect_kind": "SHIFT_LECTURE_M"},
        )
        sc_plus = _score_effect_option(obs_a, cfg, belief_a, req_a, (seat, 1), is_b2=True)
        sc_minus = _score_effect_option(obs_a, cfg, belief_a, req_a, (seat, -1), is_b2=True)
        assert sc_plus == 750.0, f"Siège {seat} : (seat, +1) doit annuler la machine sur le Rêve"
        assert sc_plus > sc_minus

    # Cas B : Rêve en rang 1 (index 0) -> depuis lecture M=2, -1 annule la machine !
    for seat in range(4):
        st_b = GameState(cfg)
        st_b.step = STEP_3_2_REVEAL
        st_b.set_tactique_at_rank(0, TILE_R_BASE + 1)
        st_b.set_tactique_at_rank(1, 2)
        st_b.set_tactique_at_rank(2, 3)
        st_b.set_player_hand(seat, machine_card_code(seat, MACHINE_ABATTEUSE), 2, 1, 2, 2)

        obs_b = st_b.get_observation(seat)
        belief_b = build_belief_summary(obs_b, cfg)
        req_b = DecisionRequest(
            decision_type=DEC_EFFET_TUILE,
            decideur=seat,
            options=((seat, -1), (seat, 1), "PASSER"),
            context={"slot_id": "G6", "effect_kind": "SHIFT_LECTURE_M"},
        )
        sc_plus = _score_effect_option(obs_b, cfg, belief_b, req_b, (seat, 1), is_b2=True)
        sc_minus = _score_effect_option(obs_b, cfg, belief_b, req_b, (seat, -1), is_b2=True)
        assert sc_minus == 750.0, f"Siège {seat} : (seat, -1) doit annuler la machine sur le Rêve"
        assert sc_minus > sc_plus


def test_bot_effect_option_dispatch_no_tuple_or_int_collisions() -> None:
    """Vérifie que Bulldozer (ray, 1), offrande (g_case, step), avancée Rêve (1 vs 2), rayon, swap ne collident pas."""
    cfg = GameConfig(n_players=4, mode=3, peuples=("M", "R", "O", "H"), exp_seed=77)
    st = GameState(cfg)
    st.step = STEP_3_2_REVEAL
    # Bulldozer sur rayon 0 possède 3 jetons rouges (haute menace), Abatteuse sur rayon 1 n'a 0 rouge
    st.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=3, bleus=0)
    st.set_machine_tokens(1, MACHINE_ABATTEUSE, rouges=0, bleus=0)
    st.set_parcel_arbres_souches(0, 1, 0, 0)  # Parcelle (0, 1) rasée (0 arbre) pour démasquer une collision parcelle !
    st.set_parcel_arbres_souches(1, 1, 4, 0)
    st.set_gardien_at_case(1, 1, face=1, used=False)
    st.set_tactique_at_rank(0, 1)  # T1 (danger faible)
    st.set_tactique_at_rank(1, 6)  # T6 (danger fort)
    st.set_tactique_at_rank(2, 2)
    st.set_tactique_at_rank(3, TILE_R_BASE + 1)

    obs = st.get_observation(0)
    belief = build_belief_summary(obs, cfg)

    # 1. Machine pair (ray=0, m_type=1 Bulldozer) ne doit PAS être jugée comme parcelle (0, 1) rasée
    req_mach = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=((0, MACHINE_BULLDOZER), (1, MACHINE_ABATTEUSE)),
        context={"slot_id": "G1", "effect_kind": "PIERRE_SERPENT_SURCHAUFFE"},
    )
    sc_bull = _score_effect_option(obs, cfg, belief, req_mach, (0, MACHINE_BULLDOZER), is_b2=True)
    sc_abat = _score_effect_option(obs, cfg, belief, req_mach, (1, MACHINE_ABATTEUSE), is_b2=True)
    assert sc_bull > sc_abat

    # 2. Offrande Gardien -> Avancée Rêve : +2 strictement préféré à +1 (pas de confusion parcelle)
    req_offr = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=((1, 1), (1, 2)),
        context={"slot_id": "R1", "effect_kind": "OFFRANDE_GARDIEN_AVANCEE_REVE"},
    )
    assert _score_effect_option(obs, cfg, belief, req_offr, (1, 2), is_b2=True) > _score_effect_option(
        obs, cfg, belief, req_offr, (1, 1), is_b2=True
    )

    # 3. Avancée Rêve (int 1 vs 2) : +2 strictement préféré à +1 (pas de confusion Gardien 1 vs 2)
    req_adv = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=(1, 2),
        context={"slot_id": "R1", "effect_kind": "REVE_DOUBLE_AVANCEE"},
    )
    assert _score_effect_option(obs, cfg, belief, req_adv, 2, is_b2=True) > _score_effect_option(
        obs, cfg, belief, req_adv, 1, is_b2=True
    )

    # 4. Mod seuil sur un rayon entier (ray=0 très menacé vs ray=1 calme)
    req_ray = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=(0, 1),
        context={"slot_id": "R9", "effect_kind": "MOD_SEUIL_RAYON_MOINS_2"},
    )
    assert _score_effect_option(obs, cfg, belief, req_ray, 0, is_b2=True) > _score_effect_option(
        obs, cfg, belief, req_ray, 1, is_b2=True
    )

    # 5. Swap de Tactiques : (1, 2) repousse la létale T6 vers la droite (mieux que (0, 1) qui l'amène en rang 1 !)
    req_swap = DecisionRequest(
        decision_type=DEC_EFFET_TUILE,
        decideur=0,
        options=((0, 1), (1, 2)),
        context={"slot_id": "R1", "effect_kind": "TAMBOUR_SWAP_TACTIQUES"},
    )
    assert _score_effect_option(obs, cfg, belief, req_swap, (1, 2), is_b2=True) > _score_effect_option(
        obs, cfg, belief, req_swap, (0, 1), is_b2=True
    )


# ---------------------------------------------------------------------------
# 3. Micro-Fork : politique future identique & suivi des ancres manquées
# ---------------------------------------------------------------------------
def test_micro_fork_zero_delta_on_exact_audit_repro() -> None:
    """Repro exacte de l'audit (chassis 0, M-E-I, B2, graine 42, rep 0, tour 2) : écart = 0.0 si 0 mouvement."""
    cfg = GameConfig.from_chassis_index(
        0,
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
    assert rec.diverged_in_2_2 is False
    assert rec.v_k0_priv_eval == rec.v_k3_priv_eval
    assert rec.delta_v_negociation == 0.0
    assert rec.g_naive_selection == 0.0
    assert rec.g_unbiased_eval == 0.0


def test_micro_fork_unreachable_anchor_returns_none_and_counts_missed() -> None:
    """Une ancre de tour non atteinte retourne None (aucun repli silencieux vers Tour 1)."""
    cfg = GameConfig.from_chassis_index(
        0,
        n_players=3,
        mode=1,
        peuples=("M", "E", "I"),
        exp_seed=42,
        rep_id=0,
        max_revision_passes=3,
    )
    assert run_micro_fork_on_config(cfg, target_tour=99, is_b2=True) is None

    # Vérification du compteur fork_anchors_missed dans _execute_micro_fork_unit
    rows = _execute_micro_fork_unit(
        {
            "mode": 1,
            "bot_name": "B2",
            "block_id": 0,
            "n_players": 3,
            "table_id": "M-E-I",
            "mirror_pair_id": "M-E-I__I-E-M",
            "peuples": ("M", "E", "I"),
            "exp_seed": 42,
            "rep_ids": (0,),
        }
    )
    assert len(rows) == 1
    assert "fork_anchors_missed" in rows[0]
    assert int(rows[0]["fork_anchors"]) + int(rows[0]["fork_anchors_missed"]) == 1


# ---------------------------------------------------------------------------
# 4. Chronologie 3.1 -> 3.2 -> 4.1, témoin d'interaction et synchronisation digest
# ---------------------------------------------------------------------------
def test_chronology_witness_3_1_reve_cancels_3_2_machine_and_enables_4_1_furtivite() -> None:
    """Témoin chronologique jumeau : un Rêve bâti en 3.1 annule en 3.2 une machine sur case 6,
    débloque son Sabotage en Furtivité 4.1 (+1 carte Sabotage) et sauve la parcelle en 5.1."""

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

        # Piste tactique : cases 1..6 remplies de Tactiques T1..T6
        for idx in range(6):
            st.set_tactique_at_rank(idx, idx + 1)

        # Trouve un emplacement lisière portant un Rêve : 2 bâtisseurs si on veut le bâtir en 3.1, 0 sinon
        reve_slot: int | None = None
        for slot_idx, tid in enumerate(cfg.lisiere_slots):
            if tid.startswith("R"):
                reve_slot = slot_idx
                break
        assert reve_slot is not None
        st.set_lisiere_tile_state(reve_slot, LISIERE_UNCONSTRUCTED, 2 if build_reve_in_3_1 else 0)

        # Siège 0 détient la carte Abatteuse (rayon 0) avec lecture M=6 (pointait sur T6 avant 3.1)
        st.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 6, 1, 6, 0)
        for s in (1, 2, 3):
            st.set_player_hand(s, 0, 1, 1, 1, 0)

        # Abatteuse rayon 0 en parcelle p=4 + 2 Défenseurs en Furtivité (lisière 0, p=4, rive 0 -> rayon 0)
        st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_NORMAL)
        st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=1, bleus=0)
        st.enter_furtivite(0, 0, 0, 4, 0, FACE_DEFINITIF)
        st.enter_furtivite(0, 1, 0, 4, 0, FACE_DEFINITIF)

        # Exécute tout le reste du Tour 1 (3.1 -> 3.2 -> 4.1 -> 5.1 -> 6.x) jusqu'au Tour 2
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

    # Avec Rêve bâti en 3.1 : inséré en case 6, annule l'Abatteuse en 3.2 (et s'ouvre -> glisse en case 5),
    # déclenche le Sabotage en Furtivité 4.1 (+1 carte Sabotage permanente) et préserve les 3 arbres en 5.1 !
    assert any(code >= TILE_R_BASE for code in track_with)
    assert sab_with == 1
    assert arbres_with == 3

    # Sans Rêve bâti en 3.1 : aucun Rêve en piste, machine active en 3.2 -> 0 Sabotage en 4.1 et coupe en 5.1 !
    assert not any(code >= TILE_R_BASE for code in track_without)
    assert sab_without == 0
    assert arbres_without < arbres_with


def test_inter_effect_composition_witness_g1_a_then_g2_a_updates_parade() -> None:
    """Témoin de composition d'effets : G1:A retourne rouge->bleu puis G2:A recule la machine et le seuil reflète les deux."""
    cfg = GameConfig(
        n_players=4,
        mode=3,
        peuples=("M", "R", "O", "H"),
        tile_profiles=(("G1", "A"), ("G2", "A")),
        exp_seed=606,
    )
    st = GameState(cfg)
    # En P4, dotation_arbres = (2, 2, 3, 3) : p=3 a dotation 3, p=2 a dotation 2.
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    st.set_parcel_defenseurs(0, 3, 1)

    # Avant les deux effets : en p=3, dotation=3 + 2 rouges = seuil 5
    seuil_avant = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, 3, TACTIQUES_SPEC[1])
    assert seuil_avant == 5

    # 1) G1:A s'ouvre sur Déclencheur 1 -> transforme 1 rouge en 1 bleu sur Abatteuse (reste 1 rouge, 1 bleu)
    st.set_gardien_at_case(1, 1, face=1, used=False)
    st.set_gardien_at_case(2, 2, face=1, used=False)
    st.light_trigger(1)
    assert sweep_gardiens(st) == 1
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)

    # 2) G2:A s'ouvre sur Déclencheur 2 -> recule l'Abatteuse de p=3 vers p=2
    st.light_trigger(2)
    assert sweep_gardiens(st) == 1
    pos_after, _, _ = st.get_machine_pos_status(0, MACHINE_ABATTEUSE)
    assert pos_after == 2

    # Composition : nouvelle position p=2 (dotation=2) + 1 rouge - 1 bleu = seuil 2 !
    seuil_apres = compute_parade_seuil(st, 0, MACHINE_ABATTEUSE, pos_after, TACTIQUES_SPEC[1])
    assert seuil_apres == 2


def test_digest_active_core_rules_chronology_matches_v5_3() -> None:
    """Vérifie que build_active_core_rules expose la chronologie v5.3 réelle (3.1 -> 3.2 -> 4.1)."""
    rules = build_active_core_rules()
    etapes = rules["spec_formelle"]["etapes_1_a_6"]
    keys = list(etapes.keys())
    assert keys[2] == "etape_3_CONSTRUCTION_ET_REVELATION"
    assert keys[3] == "etape_4_FURTIVITE_NIDS_ET_MIGRATION"
    assert "3.1" in etapes[keys[2]] and "3.2" in etapes[keys[2]]
    assert "4.1" in etapes[keys[3]]
    assert not any("REVELATION_ET_FURTIVITE" in k for k in keys)


# ---------------------------------------------------------------------------
# 5. Bijection exhaustive 384/384 Studio config_index_384 <-> Engine chassis_id
# ---------------------------------------------------------------------------
def test_studio_config_index_384_exhaustive_384_bijection() -> None:
    """Vérifie les 384 correspondances exactes entre computeConfigurationIndex (Doc Studio) et le moteur."""
    js_script = r"""
    const fs = require('fs');
    const vm = require('vm');
    const code = fs.readFileSync('docs/data/amazonia_data_v5_4.js', 'utf8');
    const ctx = {};
    vm.createContext(ctx);
    vm.runInContext(code + '\nthis.__SPEC = CHASSIS_AXES_SPEC;', ctx);
    const spec = ctx.__SPEC;

    function computeConfigurationIndex(chassis) {
      let idx = 0;
      let mult = 1;
      for (let i = spec.length - 1; i >= 0; i--) {
        const ax = spec[i];
        const curVal = chassis[ax.key];
        const optIdx = ax.options.findIndex(o => String(o.val) === String(curVal));
        idx += (optIdx >= 0 ? optIdx : 0) * mult;
        mult *= ax.options.length;
      }
      return idx + 1;
    }

    const total = spec.reduce((acc, ax) => acc * ax.options.length, 1);
    const out = [];
    for (let cid = 0; cid < total; cid++) {
      let rem = cid;
      const chassis = {};
      for (let i = 0; i < spec.length; i++) {
        const radix = spec[i].options.length;
        chassis[spec[i].key] = spec[i].options[rem % radix].val;
        rem = Math.floor(rem / radix);
      }
      out.push({
        engine_chassis_id: cid,
        studio_config_index_384: computeConfigurationIndex(chassis),
        axes: chassis,
      });
    }
    process.stdout.write(JSON.stringify(out));
    """
    proc = subprocess.run(
        ["node", "-e", js_script],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    rows: list[dict[str, Any]] = json.loads(proc.stdout)
    assert len(rows) == 384

    seen_studio: set[int] = set()
    for row in rows:
        cid = int(row["engine_chassis_id"])
        studio_idx = int(row["studio_config_index_384"])
        axes = dict(row["axes"])
        seen_studio.add(studio_idx)

        assert chassis_id_to_studio_index_384(cid) == studio_idx
        assert studio_index_384_to_chassis_id(studio_idx) == cid
        assert axes_dict_to_chassis_id(axes) == cid

        cfg = GameConfig.from_chassis_index(cid)
        assert cfg.profil_piste == str(axes["Profil_Piste"])
        assert cfg.regle_ouverture_reve_multiple == str(axes["Regle_Ouverture_Reve_Multiple"])
        assert cfg.offset_seuil_parade == int(axes["Offset_Seuil_Parade"])
        assert cfg.mise_en_place_tactiques == str(axes["Mise_En_Place_Tactiques"])
        assert cfg.placement_initial_machines == str(axes["Placement_Initial_Machines"])
        assert cfg.role_abatteuse_fin_de_piste == str(axes["Role_Abatteuse_Fin_De_Piste"])
        assert cfg.synergie_binome_machines == str(axes["Synergie_Binome_Machines"])

    assert seen_studio == set(range(1, 385))
    # Contrôles explicites : STANDARD_A = Studio 1 = Engine 0 (P4_2233), P4_2223-only = Studio 65 = Engine 1
    assert studio_index_384_to_chassis_id(1) == 0
    assert GameConfig.from_chassis_index(0).profil_piste == "P4_2233"
    assert studio_index_384_to_chassis_id(65) == 1
    assert GameConfig.from_chassis_index(1).profil_piste == "P4_2223"

    # Import manifeste uniquement via config_index_384 sans fixed_axes
    plan_std = resolve_manifest_plan(
        {"campaign_name": "check_std", "base_instance": {"config_index_384": 1}}
    )
    assert plan_std["chassis_ids"] == (0,)
    assert plan_std["chassis_studio_indices_384"] == (1,)

    plan_p4_2223 = resolve_manifest_plan(
        {"campaign_name": "check_p4_2223", "base_instance": {"config_index_384": 65}}
    )
    assert plan_p4_2223["chassis_ids"] == (1,)
    assert plan_p4_2223["chassis_studio_indices_384"] == (65,)


# ---------------------------------------------------------------------------
# 6. Traçabilité complète (amazonia_data_v5_4.js + spec_bundle_sha256) & economie_bot
# ---------------------------------------------------------------------------
def test_traceability_hashes_and_economie_bot_fixes() -> None:
    """Vérifie le verrouillage SHA-256 complet et les correctifs du graphe economie_bot."""
    lock = json.loads((ROOT / "data" / "studio_lock.json").read_text(encoding="utf-8"))
    js_sha = hashlib.sha256((ROOT / "docs" / "data" / "amazonia_data_v5_4.js").read_bytes()).hexdigest()
    bundle_sha = hashlib.sha256(DEFAULT_BUNDLE_PATH.read_bytes()).hexdigest()

    assert lock["files"]["amazonia_data_v5_4.js"]["sha256"] == js_sha

    bundle = load_spec_bundle()
    assert bundle["meta"]["studio_sha256"]["amazonia_data_v5_4.js"]["sha256"] == js_sha

    rules = build_active_core_rules()
    assert rules["studio_sha256"]["amazonia_data_v5_4.js"] == js_sha
    assert rules["spec_bundle_sha256"] == bundle_sha

    # Correctifs economie_bot vérifiés dans le bundle généré
    profiles_by_key = {
        (slot_id, prof_letter): prof_data["economie_bot"]
        for slot_id, slot_data in bundle["catalogue_tuiles"].items()
        for prof_letter, prof_data in slot_data["profils"].items()
    }
    assert "TRIG_3" not in profiles_by_key[("R4", "B")]["outputs_produits"]
    assert "TRIG_2" not in profiles_by_key[("M4", "B")]["outputs_produits"]
    assert "RES_JETON_ROUGE" in profiles_by_key[("G1", "A")]["inputs_requis"]
    assert "RES_JETON_BLEU" in profiles_by_key[("G1", "A")]["outputs_produits"]
    assert "RES_JETON_ROUGE" not in profiles_by_key[("G1", "A")]["outputs_produits"]
    assert "RES_INSECTE" not in profiles_by_key[("G10", "C")]["outputs_produits"]
    assert "TRIG_6" not in profiles_by_key[("G10", "C")]["outputs_produits"]
    assert "RES_INSECTE" not in profiles_by_key[("M4", "A")]["outputs_produits"]
    assert "RES_INSECTE" in profiles_by_key[("R6", "B")]["outputs_produits"]
    assert "TRIG_6" in profiles_by_key[("R6", "B")]["outputs_produits"]


# ---------------------------------------------------------------------------
# 7. Cohortes Sequential Halving, CRN miroirs et agrégats DuckDB enrichis
# ---------------------------------------------------------------------------
def test_shuffled_halving_cohorts_and_manifest_crn_and_duckdb(tmp_path: Path, monkeypatch: Any) -> None:
    """Vérifie l'absence de biais modulo-16, l'appariement CRN miroir et les nouvelles métriques DuckDB."""
    cohorts_16 = build_shuffled_halving_cohorts(128, 16, seed=20264010)
    assert len(cohorts_16) == 16
    flat = [c for grp in cohorts_16 for c in grp]
    assert sorted(flat) == list(range(128))
    # Aucune cohorte ne doit avoir un résidu `cid % 16` constant (contrairement à l'ancien slicing)
    for grp in cohorts_16:
        assert len({c % 16 for c in grp}) > 1

    cohorts_1 = build_shuffled_halving_cohorts(128, 1, seed=20264010)
    assert cohorts_1 == (tuple(range(128)),)

    # Plan manifeste : appariement CRN miroir (rep_start == 0 sur les 2 orientations) + LOT_01_PILOT
    manifest: dict[str, Any] = {
        "campaign_name": "audit_crn_check",
        "description": "Validation CRN miroir & métriques audit",
        "player_counts": [4],
        "games_per_configuration": 4,
        "bot": "B0",
        "mode": 3,
        "chassis_plan": {"varying_axes": [], "fixed_axes": {"Profil_Piste": "P4_2233"}},
        "slot_profile_comparisons": {"G7": ["A", "B"]},
        "base_instance": {
            "bundle_id": "LOT_01_PILOT",
            "peuples_cercle": ["M", "R", "O", "H"],
        },
    }
    plan = resolve_manifest_plan(manifest)
    assert plan["base_bundle_id"] == "LOT_01_PILOT"
    assert len(plan["base_tile_profiles"]) == 32
    assert plan["migration_policy"]["fixed"] is True
    assert len(plan["resolved_32_slots_sha256"]) == 64
    assert plan["chassis_studio_indices_384"] == (1,)

    # Pour chaque variante, la paire miroir M-R-O-H / H-O-R-M partage rep_start == 0
    for v_id in ("G7:A", "G7:B"):
        v_units = [u for u in plan["units"] if u["variant_id"] == v_id]
        assert len(v_units) == 2
        assert v_units[0]["rep_start"] == 0
        assert v_units[1]["rep_start"] == 0
        assert v_units[0]["is_mirror_pair"] is True
        assert v_units[1]["is_mirror_pair"] is True

    # Exécution locale + agrégation DuckDB
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
    assert "within_table_cvar20_ratio" in digest["totals"]
    assert "mean_physical_ops" in digest["telemetry"]
    assert "mean_player_decisions" in digest["telemetry"]
    assert digest["telemetry"]["mean_physical_ops"] > 0
    assert digest["telemetry"]["mean_player_decisions"] > 0
    assert digest["by_chassis"][0]["studio_config_index_384"] == 1
    assert digest["selection_manifest"]["base_bundle_id"] == "LOT_01_PILOT"
    assert digest["selection_manifest"]["n_resolved_slots"] == 32
    assert digest["execution"]["run_id"] == "20261119T000000Z_deadbeef"
