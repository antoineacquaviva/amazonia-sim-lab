"""Tests dédiés au gel du socle v5.5, au catalogue actif Mode 4 (32 slots),
à `defense_attribution` et au manifeste `baseline_mode4_v5_5.json`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

import engine.effects  # noqa: F401
import run_campaign as rc_mod
from campaigns.digest_builder import load_spec_bundle
from campaigns.worker_main import resolve_manifest_plan, run_campaign_manifest
from engine.core_engine import (
    apply_choice,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects.registry import list_registered_tiles
from engine.primitives import (
    DEC_EFFET_TUILE,
    HOOK_4_2_NID_APRES_PROD,
    HOOK_5_CIBLAGE_MACHINE,
    DecisionRequest,
    GameOver,
    dispatch_hook,
    prim_permutation_piste,
)
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    MACHINE_STATUS_RATISSAGE,
    PFLAG_AUTO_PARADE_ONCE,
    PIEGE_ACTIF,
    STEP_2_1_DEF1,
    STEP_3_2_REVEAL,
    STEP_5_1_TACTIQUES,
    STEP_5_3_END_CHECK,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parent.parent


def _resolve_pending_decisions(
    state: GameState,
    *,
    telemetry: TelemetryTracker | None = None,
    prefer_non_pass: bool = True,
) -> None:
    """Résout toute décision d'effet de tuile immédiatement en attente sur la pile."""
    for _ in range(16):
        if not state._continuation or state._continuation[0][0] != "WAIT_DECISION":
            break
        req = state._continuation[0][1]
        if (
            not isinstance(req, DecisionRequest)
            or req.decision_type != DEC_EFFET_TUILE
            or not req.options
        ):
            break
        opts: list[Any] = list(req.options)
        if prefer_non_pass and len(opts) > 1 and opts[0] == "PASSER":
            choice = opts[1]
        else:
            choice = opts[0]
        apply_choice(state, choice, telemetry=telemetry)
    if state._continuation and state._continuation[0][0] == "RESUME_SWEEP_GARDIENS":
        state._continuation.pop(0)


# ---------------------------------------------------------------------------
# 1. Enregistrement complet des 30 tuiles actives STANDARD_A + 4 migrations
# ---------------------------------------------------------------------------


def test_v5_5_all_30_active_tiles_and_4_migrations_registered() -> None:
    registered = set(list_registered_tiles())
    expected_30 = (
        {(f"G{i}", "A") for i in range(1, 16)}
        | {(f"R{i}", "A") for i in range(1, 11)}
        | {(f"M{i}", "A") for i in range(1, 6)}
    )
    expected_migrations = {
        ("SLOT_BUG_CERVEAU", "A"),
        ("SLOT_BUG_CERVEAU", "B"),
        ("SLOT_COLONISATION_GARDIENS", "A"),
        ("SLOT_COLONISATION_GARDIENS", "B"),
    }
    assert expected_30 <= registered
    assert expected_migrations <= registered

    bundle = load_spec_bundle()
    assert bundle["meta"]["schema_version"] == "6.0.0-alpha"
    assert len(bundle["catalogue_tuiles"]) == 32
    for slot_id, prof in expected_30:
        assert slot_id in bundle["catalogue_tuiles"]
        assert prof in bundle["catalogue_tuiles"][slot_id]["profils"]


# ---------------------------------------------------------------------------
# 2. Double activation sur Gardiens (2 Défenseurs) & passage Face 2 en 5.3
# ---------------------------------------------------------------------------


def test_v5_5_double_activation_g9_a_and_face2_only_in_5_3_on_bet_won() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=4,
        peuples=("M", "R", "O", "I"),
        exp_seed=5501,
    )
    st = GameState(cfg)
    st.tour = 2
    st.set_gardien_at_case(3, 9, face=1)  # G9:A sur case 3 (Sabotage)
    st.place_defender_gardien_pari(0, 3, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    sab_before = st.sabotage_pending_count

    # 1re ouverture -> +1 Sabotage en attente, reste Face 1, n'allume PAS le déclencheur 3
    st.light_trigger(3)
    assert sweep_gardiens(st) == 1
    assert st.sabotage_pending_count == sab_before + 1
    assert st.get_gardien_at_case(3) == (9, 1)
    assert st.count_gardien_pari_defenders_at_case(3) == 1
    assert not st.is_trigger_lit(3)

    # 2e ouverture (2e Défenseur glissé) -> +1 Sabotage en attente, reste Face 1 jusqu'en 5.3
    st.light_trigger(3)
    assert sweep_gardiens(st) == 1
    assert st.sabotage_pending_count == sab_before + 2
    assert st.get_gardien_at_case(3) == (9, 1)
    assert st.count_gardien_pari_defenders_at_case(3) == 0

    # Étape 5.3 : pari gagné -> reste en piste et passe Face 2 !
    st.step = STEP_5_3_END_CHECK
    res_53 = step_until_decision(st)
    assert not isinstance(res_53, GameOver)
    assert st.get_gardien_at_case(3) == (9, 2)

    # Tour suivant en Face 2 : 1 déclenchement ajoute +2 Sabotages en attente
    st.place_defender_gardien_pari(0, 3, FACE_DEFINITIF)
    sab_f2 = st.sabotage_pending_count
    st.light_trigger(3)
    assert sweep_gardiens(st) == 1
    assert st.sabotage_pending_count == sab_f2 + 2
    assert st.get_gardien_at_case(3) == (9, 2)


def test_v5_5_double_bet_lost_saved_by_bouclier_keeps_face1_no_upgrade() -> None:
    cfg = GameConfig(
        n_players=4,
        mode=4,
        peuples=("M", "R", "O", "I"),
        exp_seed=5502,
    )
    assert cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"
    st = GameState(cfg)
    st.tour = 2
    st.set_gardien_at_case(1, 1, face=1)  # G1:A (double-face) sur case 1
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=2, bleus=0)
    # Pari à 2 Défenseurs + 1 Insecte Bouclier sur la case 1
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st.set_colonie_at_case(1, 1)

    # Un seul déclenchement (1 Défenseur glissé, 1 Défenseur encore sur la tuile -> pari perdu !)
    st.light_trigger(1)
    assert sweep_gardiens(st) == 1
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (1, 1)
    assert st.get_gardien_at_case(1) == (1, 1)
    assert st.count_gardien_pari_defenders_at_case(1) == 1

    # En 5.3 : Bouclier de lisière consomme l'Insecte et maintient G1:A en piste SUR SA FACE ACTUELLE (Face 1)
    st.step = STEP_5_3_END_CHECK
    trk = TelemetryTracker()
    res_53 = step_until_decision(st, telemetry=trk)
    assert not isinstance(res_53, GameOver)  # pari perdu -> pas d'Éveil
    assert st.get_gardien_at_case(1) == (1, 1)
    assert st.get_colonie_at_case(1) == 0
    ts = trk.summary()
    assert ts.gardien_bets_lost == 1
    assert ts.bouclier_lisiere_saves == 1
    assert ts.gardien_bets_won == 0


def test_v5_5_double_activation_g6_a_g8_a_and_g11_a_f2() -> None:
    # --- G6:A : double préparation avant 3.2 + rebinding post-bind sur piste fixe ---
    cfg6 = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "H"), exp_seed=5503)
    st6 = GameState(cfg6)
    st6.step = STEP_2_1_DEF1
    st6.paravents_ouverts = False
    st6.set_gardien_at_case(5, 6, face=1)  # G6:A
    st6.place_defender_gardien_pari(0, 5, FACE_DEFINITIF)
    st6.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)

    # Deux activations préparées avant 3.2 -> 2 bits de préparation allumés
    st6.light_trigger(5)
    assert sweep_gardiens(st6) == 1
    st6.light_trigger(5)
    assert sweep_gardiens(st6) == 1
    assert st6.has_used_once_per_turn(40) and st6.has_used_once_per_turn(41)

    # Test rebind post-bind de prim_permutation_piste("SHIFT_LECTURE_M") sur piste fixe T1..T6
    st6.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 4, 3, 4, 4)
    assert prim_permutation_piste(st6, "SHIFT_LECTURE_M", seat=0, delta_m=1, rebind_tactique=True)
    _, _, _, new_m, new_bound = st6.get_player_hand(0)
    assert (new_m, new_bound) == (5, 5)

    # --- G8:A : double activation -> 2 slots de décalage appliqués séquentiellement en 5.1 ---
    cfg8 = GameConfig(n_players=4, mode=4, peuples=("M", "H", "R", "E"), exp_seed=5504)
    st8 = GameState(cfg8)
    st8.step = STEP_5_1_TACTIQUES
    st8.paravents_ouverts = True
    st8.set_gardien_at_case(1, 8, face=1)
    st8.set_machine_pos_status(0, MACHINE_ABATTEUSE, 3, MACHINE_STATUS_NORMAL)
    st8.set_machine_pos_status(0, MACHINE_BULLDOZER, 0, 2)  # retiré
    for r in range(1, 4):
        st8.set_machine_pos_status(r, MACHINE_ABATTEUSE, 0, 2)
        st8.set_machine_pos_status(r, MACHINE_BULLDOZER, 0, 2)
    st8.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st8.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)

    # 1re ouverture : choisit (0, Abatteuse, -1) ; 2e ouverture : choisit aussi (0, Abatteuse, -1)
    st8.light_trigger(1)
    assert sweep_gardiens(st8) == 1
    _resolve_pending_decisions(st8)
    st8.light_trigger(1)
    assert sweep_gardiens(st8) == 1
    _resolve_pending_decisions(st8)

    ctx_cib: dict[str, Any] = {
        "ray": 0,
        "m_type": MACHINE_ABATTEUSE,
        "is_ratissage": False,
        "targets": [("SUR_PLACE", 3)],
    }
    res_cib = dispatch_hook(st8, HOOK_5_CIBLAGE_MACHINE, ctx_cib)
    assert res_cib and ctx_cib["targets"] == [("SUR_PLACE", 1)]

    # --- G11:A Face 2 : double activation marque 2 parcelles distinctes en Auto-Parade ---
    cfg11 = GameConfig(n_players=4, mode=4, peuples=("M", "R", "O", "H"), exp_seed=5505)
    st11 = GameState(cfg11)
    st11.set_gardien_at_case(1, 11, face=2)
    st11.set_parcel_defenseurs(0, 1, 2)
    st11.set_parcel_defenseurs(1, 1, 2)
    st11.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st11.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)

    st11.light_trigger(1)
    assert sweep_gardiens(st11) == 1
    _resolve_pending_decisions(st11)
    st11.light_trigger(1)
    assert sweep_gardiens(st11) == 1
    _resolve_pending_decisions(st11)

    assert st11.has_parcel_flag_turn(0, 1, PFLAG_AUTO_PARADE_ONCE)
    assert st11.has_parcel_flag_turn(1, 1, PFLAG_AUTO_PARADE_ONCE)


# ---------------------------------------------------------------------------
# 3. Partition stricte des déclencheurs sur effets de tuiles & M2:A physique
# ---------------------------------------------------------------------------


def test_v5_5_tile_effects_strict_trigger_partition_and_m2_physical_red() -> None:
    # Table H-M-I-R : H-M (G7), M-I (G13) et I-R (M2) sont tous adjacents !
    cfg = GameConfig(n_players=4, mode=4, peuples=("H", "M", "I", "R"), exp_seed=5506)
    st = GameState(cfg)

    # G7:A pose un Piège sans allumer le déclencheur 2
    st.set_parcel_arbres_souches(0, 1, 1, 1)
    st.set_gardien_at_case(1, 7, face=1)
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.triggers_lit = 0
    st.light_trigger(1)
    assert sweep_gardiens(st) == 1
    assert st.get_parcel_piege(0, 1) == PIEGE_ACTIF
    assert not st.is_trigger_lit(2)

    # G13:A pose un Insecte sans allumer le déclencheur 6
    st.set_parcel_defenseurs(1, 1, 1)
    st.set_gardien_at_case(3, 13, face=1)
    st.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    st.triggers_lit = 0
    st.light_trigger(3)
    assert sweep_gardiens(st) == 1
    assert st.get_parcel_insectes(1, 1) == 1
    assert not st.is_trigger_lit(6)

    # M2:A (paire R-I active, Nid M2 construit sur (0,1)) ignore une machine en Ratissage avec 0 rouge physique
    st.set_parcel_nid(0, 1, 2)
    st.set_machine_pos_status(0, MACHINE_ABATTEUSE, 4, MACHINE_STATUS_RATISSAGE)
    st.set_machine_tokens(0, MACHINE_ABATTEUSE, rouges=0, bleus=0)
    st.set_machine_pos_status(0, MACHINE_BULLDOZER, 2, MACHINE_STATUS_NORMAL)
    st.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=0, bleus=0)
    for r in range(1, 4):
        st.set_machine_pos_status(r, MACHINE_ABATTEUSE, 0, 2)
        st.set_machine_pos_status(r, MACHINE_BULLDOZER, 0, 2)
    dispatch_hook(st, HOOK_4_2_NID_APRES_PROD, {"m_num": 2, "ray": 0, "p": 1})
    assert st.get_machine_tokens(0, MACHINE_ABATTEUSE) == (0, 0)

    # Maintenant on met 1 rouge physique sur le Bulldozer voisin -> M2:A le retourne en bleu
    st.set_machine_tokens(0, MACHINE_BULLDOZER, rouges=1, bleus=0)
    dispatch_hook(st, HOOK_4_2_NID_APRES_PROD, {"m_num": 2, "ray": 0, "p": 1})
    assert st.get_machine_tokens(0, MACHINE_BULLDOZER) == (0, 1)


# ---------------------------------------------------------------------------
# 4. Comptabilité exacte `defense_attribution` en télémétrie
# ---------------------------------------------------------------------------


def test_v5_5_defense_attribution_exact_counters() -> None:
    # A) 3.2 : Sabotage révélé + Bug B déviation + Rêve annulation
    cfg_32 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "H", "I"), exp_seed=5507)
    st_32 = GameState(cfg_32)
    # R1 sur case 5, 1 Défenseur d'activation sur case 5 -> annule la machine de siège 1
    st_32.set_tactique_at_rank(4, TILE_R_BASE + 1)
    st_32.place_defender_reve_activation(0, 5, FACE_DEFINITIF)
    # 1 Insecte Bug sur case 2 -> dévie le dé M=2 du siège 2
    st_32.set_bugs_at_case(2, 1)

    st_32.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_32.set_machine_pos_status(2, MACHINE_BULLDOZER, 1, MACHINE_STATUS_NORMAL)
    st_32.set_player_hand(0, CARD_SABOTAGE, 1, 1, 1, 0)
    st_32.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 5, 6, 5, 0)
    st_32.set_player_hand(2, machine_card_code(2, MACHINE_BULLDOZER), 2, 1, 2, 0)
    st_32.set_player_hand(3, 0, 0, 0, 0, 0)
    # Ancre 4.3 pour stopper juste après 3.2
    st_32.set_parcel_insectes(3, 1, 1)
    st_32.step = STEP_3_2_REVEAL

    trk_32 = TelemetryTracker()
    st_32.step = STEP_3_2_REVEAL
    res = step_until_decision(st_32, telemetry=trk_32)
    # Bug B propose de dévier le dé M=2 du siège 2 (option 1 = non-PASSER)
    assert isinstance(res, DecisionRequest) and res.decision_type == DEC_EFFET_TUILE
    non_pass = [opt for opt in res.options if opt != "PASSER"]
    assert non_pass
    apply_choice(st_32, non_pass[0], telemetry=trk_32)
    res_reve = step_until_decision(st_32, telemetry=trk_32)
    # v6.0 : choix exclusif BLOQUER sur R1 (case 5) pour annuler la machine du siège 1
    assert isinstance(res_reve, DecisionRequest) and res_reve.decision_type == "CHOIX_REVE_3_2"
    apply_choice(st_32, "BLOQUER", telemetry=trk_32)
    _ = step_until_decision(st_32, telemetry=trk_32)

    ts_32 = trk_32.summary()
    assert ts_32.da_sabotage_revele == 1
    assert ts_32.da_insecte_bug_deviation == 1
    assert ts_32.da_reve_annulation == 1

    # B) 5.1 : Piège + Parade classique + Parade avec Insectes + 0 Repousse Finale de base (v6.0)
    cfg_51 = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"), exp_seed=5508)
    st_51 = GameState(cfg_51)
    # T1 attaque SUR_PLACE (mod_seuil=0) ; dotation P4 p=1 est 2 arbres -> seuil 2
    # Siège 0 : Piège + 1 Défenseur (Défense >= 1 requise pour déclencher l'Embuscade, < seuil 2) sur (0,1)
    st_51.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_51.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st_51.set_parcel_defenseurs(0, 1, 1)
    st_51.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 6, 1, 1)
    # Siège 1 : Parade classique (2 Défenseurs seuls, 0 Insecte) sur (1,1)
    st_51.set_machine_pos_status(1, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_51.set_parcel_defenseurs(1, 1, 2)
    st_51.set_player_hand(1, machine_card_code(1, MACHINE_ABATTEUSE), 1, 6, 1, 1)
    # Siège 2 : Parade avec Insectes (1 Défenseur + 1 Insecte = 2 >= seuil 2) sur (2,1)
    st_51.set_machine_pos_status(2, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_51.set_parcel_defenseurs(2, 1, 1)
    st_51.set_parcel_insectes(2, 1, 1)
    st_51.set_player_hand(2, machine_card_code(2, MACHINE_ABATTEUSE), 1, 6, 1, 1)
    st_51.set_player_hand(3, 0, 0, 0, 0, 0)
    # 1 Souche sur (3,1) -> 0 repousse automatique en v6.0
    st_51.set_parcel_arbres_souches(3, 1, 1, 1)
    st_51.set_parcel_defenseurs(3, 1, 1)

    st_51.step = STEP_5_1_TACTIQUES
    st_51.tour = 8
    trk_51 = TelemetryTracker()
    for _ in range(16):
        res_51 = step_until_decision(st_51, telemetry=trk_51)
        if isinstance(res_51, GameOver):
            break
        apply_choice(st_51, res_51.options[0], telemetry=trk_51)
    ts_51 = trk_51.summary()
    assert ts_51.da_piege == 1
    assert ts_51.da_parade_classique == 1
    assert ts_51.da_parade_avec_insectes == 1
    assert ts_51.da_arbres_repousse_finale == 0

    # Vérification isolée : 0 Repousse Finale automatique en v6.0
    st_rep = GameState(cfg_51)
    st_rep.set_parcel_arbres_souches(0, 1, 0, 2)
    st_rep.set_parcel_arbres_souches(1, 1, 1, 1)
    st_rep.step = STEP_5_3_END_CHECK
    st_rep.tour = 8
    trk_rep = TelemetryTracker()
    res_rep = step_until_decision(st_rep, telemetry=trk_rep)
    assert isinstance(res_rep, GameOver)
    assert trk_rep.summary().da_arbres_repousse_finale == 0


# ---------------------------------------------------------------------------
# 5. Manifeste baseline_mode4_v5_5.json & micro-run Mode 4 multi-bots + 32 slots
# ---------------------------------------------------------------------------


def test_baseline_mode4_v5_5_manifest_plan() -> None:
    manifest_path = ROOT / "campaigns" / "manifests" / "baseline_mode4_v5_5.json"
    assert manifest_path.is_file(), "campaigns/manifests/baseline_mode4_v5_5.json manquant"
    raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    with pytest.raises(ValueError, match="EXCLUSIVE_CHOICE"):
        resolve_manifest_plan(raw_manifest)

    manifest = dict(raw_manifest)
    manifest["reve_advance_mode"] = "EXCLUSIVE_CHOICE"
    plan = resolve_manifest_plan(manifest)

    assert plan["campaign_name"] == "baseline_mode4_v5_5"
    assert plan["mode"] == 4
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["chassis_ids"] == (0, 1, 2, 3, 4, 5)
    assert plan["migration_policy"]["SLOT_BUG_CERVEAU"] == "B"
    assert plan["migration_policy"]["SLOT_COLONISATION_GARDIENS"] == "B"
    assert plan["profile_variants"][0]["reve_advance_mode"] == "SAUT"
    assert plan["include_full_tile_metrics"] is True
    # 3 bots * 4 N * 6 chassis * 1 profil = 72 configurations ; 72 * 120 = 8 640 parties
    assert plan["total_configurations"] == 72
    assert plan["total_games"] == 8640
    # Toutes les 42 tables uniques (C(6,3)+C(6,4)+C(6,5)+C(6,6)) présentes
    unique_tables = {u["peuples"] for u in plan["units"]}
    assert len(unique_tables) == 42


def test_local_mode4_multibot_micro_run_digest_has_32_tiles_and_defense_attribution(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import campaigns.digest_builder as db_mod

    manifest: dict[str, Any] = {
        "schema_version": "6.0.0-alpha",
        "manifest_type": "campaign_plan",
        "campaign_name": "micro_mode4_v6_0_test",
        "description": "Validation locale Mode 4 multi-bots B0/B1/B2 avec 32 slots et defense_attribution",
        "mode": 4,
        "bots": ["B0", "B1", "B2"],
        "k_max": 1,
        "player_counts": [3, 4],
        "table_selection": "ALL_PEUPLE_COMBOS",
        "min_animaux_sauvages": 0,
        "games_per_configuration": 20,
        "include_full_tile_metrics": True,
        "chassis_plan": {
            "varying_axes": [],
            "fixed_axes": {"Profil_Piste": "P4_2233"},
        },
        "base_instance": {
            "bundle_id": "STANDARD_A",
            "peuples_cercle": ["M", "R", "O", "H"],
            "slots_insectes": {
                "SLOT_BUG_CERVEAU": "B",
                "SLOT_COLONISATION_GARDIENS": "B",
            },
        },
    }
    manifest_file = tmp_path / "micro_mode4_v6_0_test.json"
    manifest_file.write_text(json.dumps(manifest), encoding="utf-8")
    plan = resolve_manifest_plan(manifest)

    shards_dir = tmp_path / "shards"
    rc = run_campaign_manifest(
        manifest_source=str(manifest_file),
        task_index=0,
        task_count=1,
        workers=1,
        local_out_dir=str(shards_dir),
    )
    assert rc == 0
    assert (shards_dir / "shard_00.jsonl.gz").exists()

    digests_dir = tmp_path / "data_digests"
    (tmp_path / "data").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(db_mod, "DEFAULT_DIGESTS_DIR", digests_dir)
    monkeypatch.setattr(db_mod, "ROOT", tmp_path)
    monkeypatch.setattr(rc_mod, "ROOT", tmp_path)

    parquet_path = tmp_path / "cells.parquet"
    digest_path, prompt_path, digest = aggregate_campaign_duckdb(
        manifest=manifest,
        plan=plan,
        shards_dir=shards_dir,
        parquet_path=parquet_path,
        backend="local",
        job_name="local-micro-mode4-v6-0",
        tasks=1,
        job_wall_sec=1.0,
    )
    assert digest_path.exists() and prompt_path.exists() and parquet_path.exists()
    assert digest["active_core_rules"]["version"] == "6.0.0-alpha"
    assert digest["totals"]["total_games"] == 3 * 2 * 20  # 120 parties

    # 1. Section defense_attribution complète + ventilation par bot (B0, B1, B2)
    da = digest["defense_attribution"]
    for key in (
        "parade_classique",
        "piege",
        "parade_avec_insectes",
        "reve_annulation",
        "sabotage_revele",
        "insecte_bug_deviation",
        "arbres_repousse_finale",
    ):
        assert key in da and isinstance(da[key], int) and da[key] >= 0
    assert "per_game" in da
    assert "by_bot" in da
    assert {row["bot"] for row in da["by_bot"]} == {"B0", "B1", "B2"}

    # 2. Section tile_metrics complète sur les 32 slots du catalogue actif
    tm = digest["tile_metrics"]
    expected_keys = (
        {f"G{i}:A" for i in range(1, 16)}
        | {f"R{i}:A" for i in range(1, 11)}
        | {f"M{i}:A" for i in range(1, 6)}
        | {"SLOT_BUG_CERVEAU:B", "SLOT_COLONISATION_GARDIENS:B"}
    )
    assert set(tm.keys()) == expected_keys
    for k, entry in tm.items():
        assert entry["n_games"] > 0, f"n_games nul pour le slot {k}"
        assert 0.0 <= entry["mean_ratio_arbres"] <= 1.0
