# STATUS.md — Journal d'avancement `amazonia-sim-lab`

## État des paliers

- [x] **Pré-requis Infra & Poste** : Setup poste Windows 11, `uv`, CPython 3.12, PyPy 3.11, projet GCP `amazonia-sim` (`europe-west9`), bucket `gs://amazonia-sim-runs` (avec `roles/storage.objectAdmin` pour `769540335158-compute@developer.gserviceaccount.com`) et registre `sim-workers`.
- [x] **Palier 0 (Socle & Smoke Cloud)** : Mémoire IA (`PROJECT_CHARTER_V1.md`, `GEMINI.md`, `STATUS.md`, `.agents/rules/*`), `verify_lot.py` et Smoke-Test Cloud Run PyPy->GCS->DuckDB validés.
- [x] **Palier 0 (Suite)** : Contrat JSON Studio `v5.3.1` (`T1..T6`, Sabotages par dilution, `economie_bot`, `data/spec_bundle_v5_3_1.json` et `engine/effects/mode3_reference.json`).
- [x] **Palier 1** : Noyau scellé (`state.py` `384B`, `rng.py`, `primitives.py`, `core_engine.py` Modes 1 & 2), `contracts/core_state_api.md`, Bot `B0` et tir Cloud 100k parties (`data/digest_palier1_b0.json`).
- [ ] **Palier 2** : Bots `B1/B2` (Ticks 1..3 + révision 2.2 + graphe `economie_bot`), 4 capteurs `telemetry.py`, Forks Micro et Lot Pilote de 8 tuiles.
- [ ] **Palier 3** : Usinage stateless des 92 profils restants en 10 lots + 100 tests `temoin`.
- [ ] **Palier 4** : Campagnes Cloud Batch Spot (`Sequential Halving` 128 châssis + `MAP-Elites / CVaR_20% / Shapley` Canon Unique 32 tuiles).

## Notes de session
- *2026-11-17* : Initialisation de l'environnement local (`uv 0.13.8`, Python `3.12.16`, PyPy `3.11.17`) et des droits GCS. Socle Palier 0 + Smoke-Test Cloud Run validés.
- *2026-11-17* : Réalignement sur `amazonia-doc-studio` (`0716c70d`, `22de237d`) : Sabotage par dilution permanente, retrait double aux dés, correctif `A10` (Siège `T4` alimente l'Apprentissage). `data/studio_lock.json`, `contracts/AUDIT_STUDIO_V5_3.md` et `.agents/rules/rule-kernel.md` mis à jour. Prêt pour génération de `spec_bundle_v5_3_1.json`.
- *2026-11-17* : **Palier 1 — Passe 1A terminée** : implémentation 100 % stdlib PyPy 3.11 / CPython 3.12 de `engine/rng.py`, `engine/state.py`, `engine/primitives.py` + `engine/effects/registry.py`, `engine/core_engine.py` (Modes 1 & 2, 128 châssis, invariants v5.3) et harnais `tests/test_kernel_invariants.py`.
- *2026-11-17* : **Palier 1 — Passe 1B terminée & Noyau Scellé** :
  - Buffer `GameState` élargi à `bytearray(384)` (`352` octets alloués, `32` octets de réserve libre `[352..384)`), `DECK_CARDS` porté à `64` slots (`32B`) et plage transitoire `[261..352)` (`91B`) équipée des accesseurs pour les 100 profils (`TRANS_PARCEL_SEUIL_MOD`, `TRANS_PARCEL_FLAGS`, `TRANS_ONCE_PER_TURN` 64 bits, `TRANS_PENDING_APPRENTISSAGE` + compteur de retraits volontaires `6.1`).
  - Correction d'un cas limite d'impasse totale sur forêt 100 % rasée (`_LOC_IMPASSE = 255` sur `PASSER_IMPASSE`, attrapé sur `rep_id=19901` et couvert par `test_20`) + garde-fou permanent `max_steps = 2000` dans `step_until_decision` et `play_game_b0`.
  - Génération AST de `contracts/core_state_api.md`, scellement SHA-256 des 4 modules du noyau dans `contracts/kernel_locks.sha256`, implémentation de `bots/bot_b0.py` (`K_max = 0`, isolation stricte sur snapshot assaini `PlayerObservation`) et activation de la porte `[6/6]` PyPy Invariant Fuzzer (`1 000` parties) dans `verify_lot.py` (`6/6` vert, `40/40` tests `pytest`).
  - Tir réel Cloud Run Jobs `amazonia-palier1` (`amazonia-palier1-xqgks`, `10` tâches × `2` vCPU PyPy 3.11 en `europe-west9`) : **100 000 parties** exécutées en **17,18 s CPU moy. par worker** (**36,24 s** murale provisioning inclus), débit cumulé **5 866 parties/s** (`5 386 parties/s` effectifs), archivage Parquet + synthèse DuckDB dans `data/digest_palier1_b0.json` (`12,1 Ko`).
