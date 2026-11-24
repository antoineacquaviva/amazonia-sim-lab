---
name: palier-2
description: >-
  Construit et valide les joueurs virtuels coopératifs muets, les capteurs de charge mentale
  et l'évaluation par micro-forks sans biais placebo sur le socle actif.
---

# Skill `palier-2` — Bots Coopératifs Muets, Capteurs Cognitifs & Micro-Forks (`v6.2`)

## Pré-requis & Architecture Duale
1. Lire `GEMINI.md`, `STATUS.md`, `.agents/rules/rule-bots-telemetry.md`, `.agents/rules/rule-kernel.md` et `contracts/core_state_api.md`.
2. Respecter l'architecture duale stricte : `engine/`, `bots/` et `campaigns/` doivent rester **100 % Python 3.11 stdlib pure** (compatible PyPy 3.11, zéro `numpy`/`scipy`/`duckdb`).

## Composants Validés
1. **Capteurs Cognitifs (`engine/telemetry.py`)** : `mem_debt_score` (cible `0.0`), `law_stack_mean`/`max` (plafond Canon 0 `<= 2`), `fiddliness_ratio` (`3` ops par Insecte déplacé en Migration), `cascade_sweeps` & `mid_combat_interrupts`.
2. **Bots Coopératifs Muets (`bots/`)** :
   - Isolation stricte sur `PlayerObservation` (zéro fuite des jetons piochés, du Perchoir ou des dés adverses sous paravent fermé) ;
   - `B0` réflexe (`K_max = 0`), `B1` découverte (bruit softmax calibrable `DEFAULT_TAU_B1`), `B2` économie unifiée en arbres sauvés (`bots/b2_economy.py` lisant `data/spec_bundle_v6_0.json` sur les 11 `RES_*` actifs + rollouts CRN `bots/b2_rollouts.py`), `B2_OPEN` et `B3` Rolling Horizon (`bots/bot_b3_rh.py`).
3. **Plans Expérimentaux (`campaigns/designs.py`)** : `balanced_neighbor_mirror_tables`, micro-forks sans biais placebo via `TargetFilter`, séparation stricte sélection/évaluation (`Delta_V_negociation`, `C_prive`, `rho_delta`).
4. **Validation** : `uv run python verify_lot.py` 100 % vert (incluant `pytest` et le fuzzer PyPy sous garde-fou `max_steps = 2000`).
