"""Tests unitaires v5.4.6 / v5.4.7 : partition stricte des 6 déclencheurs (3.2 & 5.1, 4.2 Nids exclu),
verrouillage 4. Gardien sur DISTINCT_OPEN_1, Bouclier de lisière (SLOT_COLONISATION_GARDIENS=B),
manifeste validation_socle_v5_5 (5 760 parties) et agrégateur digest JSON.
"""

from __future__ import annotations

import gzip
import json
from pathlib import Path

from bots.heuristic_engine import play_game_b2
from campaigns.worker_main import _execute_manifest_unit, resolve_manifest_plan
from engine.core_engine import (
    DEC_POSE_PIEGE_FURTIVITE_4_1,
    _advance_continuation,
    _resolve_nid_block,
    _run_step_3_2,
    apply_choice,
    resolve_single_machine_attack,
    step_until_decision,
    sweep_gardiens,
)
from engine.effects import load_all_effects
from engine.primitives import DecisionRequest, GameOver
from engine.state import (
    CARD_SABOTAGE,
    FACE_DEFINITIF,
    FURT_RIVE_PIEGE,
    FURT_RIVE_SABOTAGE,
    LISIERE_CONSTRUCTED,
    LISIERE_UNCONSTRUCTED,
    MACHINE_ABATTEUSE,
    MACHINE_BULLDOZER,
    MACHINE_STATUS_NORMAL,
    PIEGE_ACTIF,
    STEP_3_2_REVEAL,
    STEP_4_1_FURTIVITE,
    STEP_4_3_MIGRATION,
    STEP_5_3_END_CHECK,
    TACTIQUES_SPEC,
    TILE_R_BASE,
    GameConfig,
    GameState,
    machine_card_code,
)
from engine.telemetry import TelemetryTracker
from run_campaign import aggregate_campaign_duckdb

ROOT = Path(__file__).resolve().parents[1]


def test_strict_partition_3_2_sabotage_gt_bug_insecte_gt_reve_and_4_1_no_trigger() -> None:
    """Partition stricte 3.2 (3. Sabotage > 6. Insecte Bug > 5. Rêve actif) et 4.1 sans déclencheur 2/3."""
    load_all_effects()
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "H"),
    )
    st = GameState(cfg)
    st.tour = 2

    # Placer un Rêve (R3) sur le rang 5 (case 5) muni d'1 Défenseur
    st.set_tactique_at_rank(4, TILE_R_BASE + 3)
    st.place_defender_reve_activation(3, 5, FACE_DEFINITIF, def_idx=0)
    # Poser 1 Bug sur le rang 4 (case 4) pour dévier le siège 1 vers le rang 5 (Rêve défendu !)
    st.set_bugs_at_case(4, 1)

    # Placer des Gardiens avec paris sur cases 3, 5, 6 (1 Défenseur chacun)
    st.set_gardien_at_case(3, 1, face=1)
    st.set_gardien_at_case(5, 2, face=1)
    st.set_gardien_at_case(6, 3, face=1)
    st.place_defender_gardien_pari(0, 3, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 5, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)

    # Mains sous paravent :
    # - Siège 0 : CARD_SABOTAGE -> allume 3. Sabotage uniquement
    # - Siège 1 : Machine (ray 0 Abatteuse) dé M=4 -> déviée par Bug vers M=5 (Rêve) -> allume 6. Insecte UNIQUEMENT (PAS 5. Rêve !)
    # - Siège 2 : Machine (ray 1 Abatteuse) dé M=2 -> pas sur Rêve, pas de Bug -> 0 déclencheur
    # - Siège 3 : CARD_SABOTAGE -> 2e Sabotage (mais case 3 n'a qu'1 Déf)
    st.set_player_hand(0, CARD_SABOTAGE, 0, 0, 0, 0)
    st.set_player_hand(1, machine_card_code(0, MACHINE_ABATTEUSE), 4, 4, 4, 0)
    st.set_player_hand(2, machine_card_code(1, MACHINE_ABATTEUSE), 2, 2, 2, 0)
    st.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)

    trk = TelemetryTracker()
    st.step = STEP_3_2_REVEAL
    req = step_until_decision(st, telemetry=trk)
    assert not isinstance(req, GameOver)
    assert req.context.get("effect_kind") == "BUG_DEVIATION_SYNAPTIQUE_3_2"
    assert "M_PLUS_1" in req.options

    # Dévier siège 1 de 4 -> 5 (sur le Rêve !) puis drainer uniquement la fin de 3.2
    apply_choice(st, "M_PLUS_1", telemetry=trk)
    while st._continuation:
        res_c = _advance_continuation(st)
        assert res_c is None

    # Vérification de la partition stricte :
    # - 3. Sabotage s'est allumée (siège 0/3) -> Gardien 3 consommé
    assert st.count_gardien_pari_consumed_at_case(3) == 1
    # - 6. Insecte s'est allumée (déviation Bug siège 1) -> Gardien 6 consommé
    assert st.count_gardien_pari_consumed_at_case(6) == 1
    # - 5. Rêve NE S'EST PAS ALLUMÉE car siège 1 avait déjà consommé son déclencheur sur 6. Insecte !
    assert st.count_gardien_pari_consumed_at_case(5) == 0
    assert st.count_gardien_pari_defenders_at_case(5) == 1

    # Cas 2 (v6.1 REVE_TRIG=ACTIF figé) :
    # - Rêve SANS Défenseur -> inerte, 5. Rêve NE S'ALLUME PAS
    st2_inert = GameState(cfg)
    st2_inert.tour = 2
    st2_inert.set_tactique_at_rank(4, TILE_R_BASE + 3)  # R3 sur case 5, 0 Défenseur
    st2_inert.set_gardien_at_case(5, 2, face=1)
    st2_inert.place_defender_gardien_pari(0, 5, FACE_DEFINITIF)
    st2_inert.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)
    for s in (1, 2, 3):
        st2_inert.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 1, 1, 1, 0)
    st2_inert.step = STEP_3_2_REVEAL
    _run_step_3_2(st2_inert)
    assert st2_inert.get_player_hand(0)[4] == 5
    assert st2_inert.count_gardien_pari_consumed_at_case(5) == 0

    # - Rêve AVEC 1 Défenseur (posé en 2.1) -> annule la machine ET allume 5. Rêve !
    st2 = GameState(cfg)
    st2.tour = 2
    st2.set_tactique_at_rank(4, TILE_R_BASE + 3)  # R3 sur case 5
    st2.place_defender_reve_activation(1, 5, FACE_DEFINITIF, def_idx=0)
    st2.set_gardien_at_case(5, 2, face=1)
    st2.place_defender_gardien_pari(0, 5, FACE_DEFINITIF)
    st2.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 5, 5, 5, 0)
    for s in (1, 2, 3):
        st2.set_player_hand(s, machine_card_code(s, MACHINE_ABATTEUSE), 1, 1, 1, 0)
    st2.step = STEP_3_2_REVEAL
    _run_step_3_2(st2)
    while st2._continuation:
        assert _advance_continuation(st2) is None
    assert st2.get_player_hand(0)[4] == 0
    assert st2.count_gardien_pari_consumed_at_case(5) == 1
    assert st2.count_gardien_pari_defenders_at_case(5) == 0

    # Cas 3 : Furtivité 4.1 « Chaud vs Calme » (pose d'un Piège et acquisition d'un Sabotage) N'allume ni 2. Piégeage ni 3. Sabotage !
    st3 = GameState(cfg)
    st3.tour = 2
    st3.paravents_ouverts = True
    st3.set_gardien_at_case(2, 1, face=1)
    st3.set_gardien_at_case(3, 2, face=1)
    st3.place_defender_gardien_pari(0, 2, FACE_DEFINITIF)
    st3.place_defender_gardien_pari(1, 3, FACE_DEFINITIF)
    # Rayon 0 : m(0) = 2 cartes révélées -> Rive Piège gagnée ; Rayon 1 : m(1) = 0 -> Rive Sabotage gagnée
    st3.set_player_hand(0, machine_card_code(0, MACHINE_ABATTEUSE), 1, 1, 1, 1)
    st3.set_player_hand(1, machine_card_code(0, MACHINE_BULLDOZER), 2, 2, 2, 2)
    st3.set_player_hand(2, CARD_SABOTAGE, 0, 0, 0, 0)
    st3.set_player_hand(3, CARD_SABOTAGE, 0, 0, 0, 0)
    st3.place_defender_furtivite(0, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st3.place_defender_furtivite(2, 0, 0, FURT_RIVE_PIEGE, FACE_DEFINITIF)
    st3.place_defender_furtivite(1, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    st3.place_defender_furtivite(3, 0, 1, FURT_RIVE_SABOTAGE, FACE_DEFINITIF)
    sab_before = st3.sabotage_pending_count
    st3.step = STEP_4_1_FURTIVITE
    req3 = step_until_decision(st3)
    assert isinstance(req3, DecisionRequest) and req3.decision_type == DEC_POSE_PIEGE_FURTIVITE_4_1
    assert req3.decideur == 0
    apply_choice(st3, 2)
    while st3._continuation:
        assert _advance_continuation(st3) is None
    assert st3.get_parcel_piege(0, 2) == PIEGE_ACTIF
    assert st3.sabotage_pending_count == sab_before + 1
    assert st3.count_gardien_pari_consumed_at_case(2) == 0
    assert st3.count_gardien_pari_consumed_at_case(3) == 0


def test_strict_partition_5_1_piegeage_gt_insecte_gt_parade() -> None:
    """Partition stricte 5.1 (au plus 1 déclencheur par frappe bloquée) : 2. Piégeage > 6. Insecte > 1. Parade."""
    load_all_effects()
    cfg = GameConfig(n_players=4, mode=2, peuples=("M", "R", "O", "I"))

    # Cas A : Frappe arrêtée par un Piège armé -> allume 2. Piégeage UNIQUEMENT (PAS 1. Parade ni 6. Insecte)
    st_a = GameState(cfg)
    st_a.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_a.set_gardien_at_case(1, 1, face=1)
    st_a.set_gardien_at_case(2, 2, face=1)
    st_a.set_gardien_at_case(6, 3, face=1)
    st_a.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_a.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st_a.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    st_a.set_parcel_piege(0, 1, PIEGE_ACTIF)
    st_a.set_parcel_defenseurs(0, 1, 1)
    st_a.set_parcel_insectes(0, 1, 2)

    resolve_single_machine_attack(st_a, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st_a.count_gardien_pari_consumed_at_case(2) == 1
    assert st_a.count_gardien_pari_consumed_at_case(1) == 0
    assert st_a.count_gardien_pari_consumed_at_case(6) == 0

    # Cas B : Parade classique qui défausse >= 1 Insecte -> allume 6. Insecte UNIQUEMENT (PAS 1. Parade ni 2. Piégeage)
    st_b = GameState(cfg)
    st_b.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_b.set_gardien_at_case(1, 1, face=1)
    st_b.set_gardien_at_case(2, 2, face=1)
    st_b.set_gardien_at_case(6, 3, face=1)
    st_b.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_b.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st_b.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    # Seuil sur p=1 (P4_2233, T1) = 2 : 1 Défenseur + 1 Insecte -> défausse 1 Insecte
    st_b.set_parcel_defenseurs(0, 1, 1)
    st_b.set_parcel_insectes(0, 1, 1)

    resolve_single_machine_attack(st_b, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st_b.get_parcel_insectes(0, 1) == 0
    assert st_b.count_gardien_pari_consumed_at_case(6) == 1
    assert st_b.count_gardien_pari_consumed_at_case(1) == 0
    assert st_b.count_gardien_pari_consumed_at_case(2) == 0

    # Cas C : Parade classique par les seuls Défenseurs (sans Piège et sans dépense d'Insecte) -> allume 1. Parade UNIQUEMENT
    st_c = GameState(cfg)
    st_c.set_machine_pos_status(0, MACHINE_ABATTEUSE, 1, MACHINE_STATUS_NORMAL)
    st_c.set_gardien_at_case(1, 1, face=1)
    st_c.set_gardien_at_case(2, 2, face=1)
    st_c.set_gardien_at_case(6, 3, face=1)
    st_c.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st_c.place_defender_gardien_pari(1, 2, FACE_DEFINITIF)
    st_c.place_defender_gardien_pari(2, 6, FACE_DEFINITIF)
    # Seuil sur p=1 = 2 : 2 Défenseurs (+ 1 Insecte non dépensé !) -> 0 Insecte défaussé -> 1. Parade uniquement
    st_c.set_parcel_defenseurs(0, 1, 2)
    st_c.set_parcel_insectes(0, 1, 1)

    resolve_single_machine_attack(st_c, 0, MACHINE_ABATTEUSE, TACTIQUES_SPEC[1])
    assert st_c.get_parcel_insectes(0, 1) == 1
    assert st_c.count_gardien_pari_consumed_at_case(1) == 1
    assert st_c.count_gardien_pari_consumed_at_case(2) == 0
    assert st_c.count_gardien_pari_consumed_at_case(6) == 0


def test_nid_4_2_production_never_lights_trigger_6_insecte() -> None:
    """v5.4.7 : la production d'un Nid en 4.2 crée des Insectes mais n'allume JAMAIS 6. Insecte."""
    load_all_effects()
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "I"),
    )
    st = GameState(cfg)
    st.tour = 2
    st.set_gardien_at_case(6, 1, face=1)
    st.place_defender_gardien_pari(0, 6, FACE_DEFINITIF)
    st.set_parcel_nid(0, 1, 1, active_ce_tour=False)
    st.set_parcel_insectes(0, 1, 0)

    # Production 4.2 (0 Insecte -> +1 Insecte) : NE DOIT PAS allumer 6. Insecte ni ouvrir le Gardien !
    _resolve_nid_block(st, 1)
    assert st.get_parcel_insectes(0, 1) == 1
    assert not st.is_trigger_lit(6)
    assert st.count_gardien_pari_consumed_at_case(6) == 0
    assert st.count_gardien_pari_defenders_at_case(6) == 1

    # Production 4.2 à seuil +2 (2 Insectes -> +2 Insectes = 4) : toujours AUCUN déclenchement 6. Insecte !
    st.set_parcel_insectes(0, 1, 2)
    st.set_nid_activated(1, False)
    _resolve_nid_block(st, 1)
    assert st.get_parcel_insectes(0, 1) == 4
    assert not st.is_trigger_lit(6)
    assert st.count_gardien_pari_consumed_at_case(6) == 0
    assert st.count_gardien_pari_defenders_at_case(6) == 1


def test_gardien_4_trigger_mode_locked_distinct_open_1() -> None:
    """Case 4. Gardien scellée sur la règle native DISTINCT_OPEN_1 (anti-boucle conservé)."""
    load_all_effects()

    # 1re ouverture de chaque autre Gardien distinct allume 4 ; 2e ouverture du même NON
    cfg1 = GameConfig(
        n_players=5,
        mode=2,
        peuples=("M", "R", "O", "H", "I"),
    )
    st1 = GameState(cfg1)
    st1.set_gardien_at_case(1, 1, face=1)
    st1.set_gardien_at_case(2, 2, face=1)
    st1.set_gardien_at_case(4, 3, face=1)
    st1.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st1.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st1.place_defender_gardien_pari(2, 2, FACE_DEFINITIF)
    st1.place_defender_gardien_pari(3, 4, FACE_DEFINITIF)
    st1.place_defender_gardien_pari(4, 4, FACE_DEFINITIF)

    # 1re ouverture case 1 -> allume 4 -> ouvre 4 (anti-boucle : 4 ne se ré-allume pas)
    st1.light_trigger(1)
    assert sweep_gardiens(st1) == 2
    assert st1.count_gardien_pari_consumed_at_case(4) == 1
    assert st1.count_gardien_pari_defenders_at_case(4) == 1

    # 2e ouverture du MÊME Gardien (case 1) -> n'allume PAS 4 !
    st1.light_trigger(1)
    assert sweep_gardiens(st1) == 1
    assert st1.count_gardien_pari_consumed_at_case(4) == 1
    assert st1.count_gardien_pari_defenders_at_case(4) == 1

    # 1re ouverture d'un 2e autre Gardien distinct (case 2) -> allume 4 -> consomme le 2e Déf sur 4 !
    st1.light_trigger(2)
    assert sweep_gardiens(st1) == 2
    assert st1.count_gardien_pari_consumed_at_case(4) == 2
    assert st1.count_gardien_pari_defenders_at_case(4) == 0


def test_bouclier_de_lisiere_saves_tile_but_keeps_bet_lost_for_eveil() -> None:
    """Bouclier de lisière natif : sauve la tuile en 5.3 contre 1 Insecte, mais le pari reste PERDU."""
    load_all_effects()
    cfg = GameConfig(
        n_players=4,
        mode=2,
        peuples=("M", "R", "O", "I"),
    )
    assert cfg.profile_for_slot("SLOT_COLONISATION_GARDIENS") == "B"

    st = GameState(cfg)
    st.tour = 3
    g1_slot = st.find_lisiere_slot_by_tile_id("G1")
    g2_slot = st.find_lisiere_slot_by_tile_id("G2")
    assert g1_slot is not None and g2_slot is not None
    st.set_lisiere_tile_state(g1_slot, LISIERE_CONSTRUCTED, 0)
    st.set_lisiere_tile_state(g2_slot, LISIERE_CONSTRUCTED, 0)
    st.set_gardien_at_case(1, 1, face=1)
    st.set_gardien_at_case(2, 2, face=1)
    # 1 Insecte Bouclier sur case 1, 0 Insecte sur case 2
    st.set_colonie_at_case(1, 1)
    st.set_colonie_at_case(2, 0)

    # Les 4 Défenseurs engagés en pari sur Gardiens (tentative d'Éveil) :
    # - 2 sur case 1 (1 seul déclenchement -> 1 restant = pari perdu, MAIS Bouclier sur case 1 !)
    # - 2 sur case 2 (1 seul déclenchement -> 1 restant = pari perdu, SANS Bouclier sur case 2)
    st.place_defender_gardien_pari(0, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(1, 1, FACE_DEFINITIF)
    st.place_defender_gardien_pari(2, 2, FACE_DEFINITIF)
    st.place_defender_gardien_pari(3, 2, FACE_DEFINITIF)

    # En 4.3, le Bouclier sur case 1 reste intact jusqu'en 5.3 (pas d'ouverture forcée)
    st.set_parcel_insectes(3, 1, 1)  # Ancre 4.3
    st.step = STEP_4_3_MIGRATION
    req_43 = step_until_decision(st)
    assert isinstance(req_43, DecisionRequest)
    assert st.get_colonie_at_case(1) == 1
    st._continuation.clear()
    st.set_parcel_insectes(3, 1, 0)

    # 1 ouverture sur case 1 et 1 sur case 2 -> 1 Déf restant sur chaque case (paris perdus)
    st.light_trigger(1)
    sweep_gardiens(st)
    st.light_trigger(2)
    sweep_gardiens(st)

    # Le pari sauvé par Bouclier de lisière doit quand même rester PERDU pour l'Éveil !
    trk = TelemetryTracker()
    st.step = STEP_5_3_END_CHECK
    res = step_until_decision(st, telemetry=trk)
    assert not isinstance(res, GameOver), "Un pari sauvé par Bouclier de lisière reste PERDU pour l'Éveil !"

    # Case 1 : Bouclier a défaussé l'Insecte, G1 reste en piste sur Face 1
    assert st.get_colonie_at_case(1) == 0
    assert st.get_gardien_at_case(1) == (1, 1)
    assert st.get_lisiere_tile_state(g1_slot)[0] == LISIERE_CONSTRUCTED

    # Case 2 : pas de Bouclier -> G2 retourne en lisière Face 1
    assert st.get_gardien_at_case(2) == (0, 1)
    assert st.get_lisiere_tile_state(g2_slot)[0] == LISIERE_UNCONSTRUCTED

    ts = trk.summary()
    assert ts.gardien_bets_lost == 2
    assert ts.gardien_bets_won == 0
    assert ts.bouclier_lisiere_saves == 1


def test_validation_socle_v6_1_manifest_6840_and_digest_schema() -> None:
    """Manifeste validation_socle_v6_1 (6 840 parties, B0/B1/B2, P4_2233 unique) + reveil_anatomy."""
    manifest_path = ROOT / "campaigns" / "manifests" / "validation_socle_v6_1.json"
    assert manifest_path.is_file()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    plan = resolve_manifest_plan(manifest)

    assert plan["mode"] == 2
    assert plan["bots"] == ("B0", "B1", "B2")
    assert list(plan["player_counts"]) == [3, 4, 5, 6]
    assert plan["profil_piste"] == "P4_2233"
    assert plan["total_games"] == 6_840
    assert len(plan["profile_variants"]) == 1

    # Micro-smoke B2 + agrégateur DuckDB vérifiant tous les champs reveil_anatomy & v6.1
    mini_manifest = dict(manifest)
    mini_manifest.pop("bots", None)
    mini_manifest["bot"] = "B2"
    mini_manifest["campaign_name"] = "test_validation_socle_v6_1_mini"
    mini_manifest["player_counts"] = [4]
    mini_manifest["games_per_configuration"] = 2
    mini_plan = resolve_manifest_plan(mini_manifest)
    rows = [_execute_manifest_unit(u) for u in mini_plan["units"][:4]]
    assert all("count_bouclier_lisiere_saves" in r for r in rows)
    assert all("rs_trig1_lit" in r and "rs_trig6_lit" in r for r in rows)

    if sum(int(r["rs_count"]) + int(r["rf_count"]) for r in rows) == 0:
        rows[0]["rs_count"] = 1
        rows[0]["rs_tour"] = 4
        rows[0]["rs_trig1_lit"] = 1
        rows[0]["rs_trig3_lit"] = 1
        rows[0]["count_bouclier_lisiere_saves"] = 2

    work_dir = ROOT / ".tmp_runs" / "test_validation_socle_v6_1_mini"
    shards_dir = work_dir / "shards"
    shards_dir.mkdir(parents=True, exist_ok=True)
    shard_path = shards_dir / "shard_00.jsonl.gz"
    with gzip.open(shard_path, "wt", encoding="utf-8") as fh:
        for r in rows:
            r["task_index"] = 0
            r["task_games"] = sum(int(x["n_games"]) for x in rows)
            r["task_wall_sec"] = 0.1
            r["task_games_per_sec"] = 100.0
            fh.write(json.dumps(r) + "\n")

    parquet_path = work_dir / "cells.parquet"
    digest_path = ROOT / "data" / "digests" / "digest_test_validation_socle_v6_1_mini.json"
    legacy_digest_path = ROOT / "data" / "digest_test_validation_socle_v6_1_mini.json"
    prompt_path = ROOT / "data" / "digests" / "PROMPT_GEMINI_test_validation_socle_v6_1_mini.md"
    try:
        _, _, digest = aggregate_campaign_duckdb(
            manifest=mini_manifest,
            plan=mini_plan,
            shards_dir=shards_dir,
            parquet_path=parquet_path,
            backend="local",
            job_name="unit-test-v61",
            tasks=1,
            job_wall_sec=0.1,
        )
        assert "by_variant_x_n_players" in digest
        assert "by_variant_x_n_animaux_sauvages" in digest
        assert "count_bouclier_lisiere_saves" in digest["totals"]

        ra = digest["reveil_anatomy"]["global"]
        for key in (
            "count_bouclier_lisiere_saves",
            "pct_trigger_1_parade_lit",
            "pct_trigger_2_piegeage_lit",
            "pct_trigger_3_sabotage_lit",
            "pct_trigger_4_gardien_lit",
            "pct_trigger_5_reve_lit",
            "pct_trigger_6_insecte_lit",
        ):
            assert key in ra, f"Clé manquante dans reveil_anatomy.global : {key}"
    finally:
        for p_clean in (digest_path, legacy_digest_path, prompt_path, shard_path, parquet_path):
            if p_clean.exists():
                p_clean.unlink()

    # Smoke B2 sur 3J et 4J avec Bouclier de lisière et DISTINCT_OPEN_1 natifs
    for n_pl, peup in ((3, ("M", "R", "I")), (4, ("M", "R", "H", "I"))):
        cfg_s = GameConfig(
            n_players=n_pl,
            mode=2,
            peuples=peup,
            exp_seed=5470 + n_pl,
        )
        over = play_game_b2(GameState(cfg_s), k_max_passes=3)
        assert 1 <= over.tour_fin <= 8
        assert 0.0 <= over.ratio_arbres <= 1.0
