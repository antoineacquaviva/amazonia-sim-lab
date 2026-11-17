# STATUS.md — Journal d'avancement `amazonia-sim-lab`

## État des paliers

- [x] **Pré-requis Infra & Poste** : Setup poste Windows 11, `uv`, CPython 3.12, PyPy 3.11, projet GCP `amazonia-sim` (`europe-west9`), bucket `gs://amazonia-sim-runs` (avec `roles/storage.objectAdmin` pour `769540335158-compute@developer.gserviceaccount.com`) et registre `sim-workers`.
- [x] **Palier 0 (Socle & Smoke Cloud)** : Mémoire IA (`PROJECT_CHARTER_V1.md`, `GEMINI.md`, `STATUS.md`, `.agents/rules/*`), `verify_lot.py` et Smoke-Test Cloud Run PyPy->GCS->DuckDB validés.
- [ ] **Palier 0 (Suite)** : Contrat JSON Studio `v5.3.1` (`T1..T6`, Sabotages, `economie_bot`).
- [ ] **Palier 1** : Noyau scellé (`state.py`, `rng.py`, `primitives.py`, `core_engine.py` Modes 1 & 2), `contracts/core_state_api.md`, Bot `B0` et tir Cloud 100k parties.
- [ ] **Palier 2** : Bots `B1/B2` (Ticks 1..3 + révision 2.2 + graphe `economie_bot`), 4 capteurs `telemetry.py`, Forks Micro et Lot Pilote de 8 tuiles.
- [ ] **Palier 3** : Usinage stateless des 92 profils restants en 10 lots + 100 tests `temoin`.
- [ ] **Palier 4** : Campagnes Cloud Batch Spot (`Sequential Halving` 128 châssis + `MAP-Elites / CVaR_20% / Shapley` Canon Unique 32 tuiles).

## Notes de session
- *2026-11-17* : Initialisation de l'environnement local (`uv 0.13.8`, Python `3.12.16`, PyPy `3.11.17`) et des droits GCS. Démarrage du Palier 0.
