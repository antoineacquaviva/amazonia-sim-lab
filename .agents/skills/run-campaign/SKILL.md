---
name: run-campaign
description: >-
  Lance des simulations de parties et répond aux questions d'équilibrage en français courant :
  utiliser dès que l'auteur demande de tester une idée, simuler des parties, mener une étude
  Tuiles à blanc (solo, retrait LOO, carrés 2x2, moteurs), couvrir les 197 assises, comparer
  B0..B3, lancer des micro-forks v6.4, auditer les faux dilemmes Ockham ou extraire des parties
  remarquables.
---

# Skill `run-campaign` — Campagnes Modulaires, « Tuiles à blanc » & Cloud Batch Spot (`v6.4`)

## 1. Traduction d'une Demande en Français Naturel vers un Manifeste `v6.4`

Traduire directement l'intention de l'auteur en un manifeste JSON dans `campaigns/<nom>.json` (schéma `6.4`, `manifest_type: "campaign_plan"` ou `"campaign_suite"`), en mobilisant à la carte :

### A. Études modulaires « Tuiles à blanc » (`tile_study`, sans biais de bot `B0..B3`)
Toute tuile placée à `"NEUTRE"` conserve 100 % de sa physique (construction, lisière, coût, icône, présence autour de la table) sans son pouvoir texte ; tous les bots (`B0`, `B1`, `B2`, `B2_OPEN`, `B3`) s'adaptent dynamiquement aux emplacements neutres.
- **`SUBSET`** (ou raccourcis top-level `active_slots` / `neutral_slots`) : activer exactement un sous-ensemble ciblé parmi les 30 tuiles (`"ALL"`, `"G"`, `"R"`, `"M"`, `"EDGE:M_R"`, `"MOTOR:SOMMEIL_REVES"` ou liste explicite), toutes les autres à `"NEUTRE"`.
- **`SOLO_ISOLATED`** : 1 tuile active à la fois contre `ALL_NEUTRE` (plancher solo en paires CRN).
- **`LEAVE_ONE_OUT`** : 29 tuiles actives contre `ALL_ACTIVE` (perte en écosystème `Δ_éco`).
- **`SOLO_AND_ECOSYSTEM`** : combinaison dédupliquée (`62` variantes pour `30` tuiles) mesurant `Δ_solo`, `Δ_éco` et le levier synergique `L_syn = Δ_éco − Δ_solo` avec IC 95 % groupés par table (`CR1`) et correction de Holm-Bonferroni.
- **`EDGE_2X2`** : carrés factoriels `2×2` (`00`, `10`, `01`, `11`) des `15` lisières de `MATRICE_PAIRES` (`46` variantes dédupliquées sur fond `ALL_NEUTRE` ou `ALL_ACTIVE`), mesurant l'interaction pure `I_2x2 = Y11 − Y10 − Y01 + Y00`.
- **`MOTORS_SOLO` / `MOTORS_ABLATION` / `MOTORS_BOTH`** : moteurs du jeu dérivés automatiquement de `contracts/tiles_canon_v6_4.json` — `motor_family`: `"DISJOINT"` (`5` moteurs couvrant `30/30` tuiles sans recouvrement), `"PIVOT"` (`7` moteurs fonctionnels incluant les tuiles-pivots multi-moteurs), `"ROLE"` (`6` familles de rôles) ou `"ALL"`.
- **`CUSTOM_VARIANTS`** : liste libre de variantes nommées `{variant_id, active_slots}`.

### B. Arsenal analytique mobilisable à la carte
- **Couverture exhaustive des `197` assises** : `"table_selection": "ALL_197_ASSISES"` (avec `"reps_per_assise": K`) ou `"BENCHMARK_ASSISES"` (assises repères rapides) ou `"BALANCED_CIRCLES"` (cercles miroirs équilibrés `3..6` joueurs).
- **Spectre complet des bots (`B0` → `B3`)** : `"bots": ["B0", "B1", "B2", "B2_OPEN", "B3"]`. Pour contenir le coût de `B3` (IS-MCTS) tout en gardant un appariement CRN strict face à `B2` pour traquer les stratégies dégénérées, configurer `"b3_config": {"reps_cap_per_table": 4, "n_determinizations": 2, "max_candidates": 4, "horizon_turns": 2}`.
- **Micro-forks causaux `v6.4`** : `"micro_forks": true` et `"fork_families"` au choix parmi `CORE_2_1_2_2`, `FURTIVITE_SENTINELLES` (Rives Piège/Sabotage, Sentinelles enracinées et Enracinement `6.1`), `EVEIL_A_PLUS_1` (pari Éveil cumulatif `A+1` et paris Gardiens), `CHAMANES` (Tambour vs Chant), `ALTERATION` (gains d'Altération) et `GARDIEN_ICONES` (choix d'icône `1..6`).
- **Audit Ockham `v6.4` (`delta == 0`)** : `"include_v64_ockham_audit": true` enregistre sans altérer la partie tous les choix internes `v6.4` et embranchements d'effets de tuiles pour signaler tout faux dilemme (`> 90 %`).
- **Extraction automatique de parties remarquables (`human_trace_1.0`)** : `"extract_remarkable_traces": {"enabled": true, "max_games": 8}` sélectionne et rejoue les parties les plus instructives (pire effondrement, meilleure survie, Sommeil éclair, Éveil réussi, grande cascade, Tour 8 serré, écart `B3` vs `B2`) dans `docs/traces/traces_<nom>.jsonl`, directement ouvrable hors-ligne dans `docs/human_logger.html`.
- **Suite orchestrée multi-étapes (`campaign_suite`)** : chaîner plusieurs études complémentaires dans un seul manifeste (`"manifest_type": "campaign_suite"`, `"stages": [...]`), avec reprise par étape et rapport maître consolidé. Modèles prêts à l'emploi : `campaigns/manifests/etude_modulaire_v6_4.json` et `campaigns/manifests/suite_complete_v6_4.json`.

---

## 2. Pré-Vérification Silencieuse & Devis Obligatoire en 5 Lignes

1. **Pré-vérification (silencieuse)** :
   - Vérifier la validité du manifeste et afficher le devis exact sans rien lancer :
     ```bash
     uv run python run_campaign.py campaigns/<nom>.json --quote-only
     ```
   - Optionnel en cas de nouveau schéma complexe : micro-validation locale rapide (`0 €`, aucun appel GCP) via `--backend local --skip-git-push` sur un extrait minimal.
   - **Zéro appel API LLM payant (`0,00 €`)** : interdiction absolue d'appeler une API Gemini/Vertex depuis Python.
2. **Devis auteur en 5 lignes (toujours présenté en français clair avant un tir Cloud)** :
   1. **Objectif** : question de design / hypothèse testée.
   2. **Étude** : variantes comparées (Tuiles à blanc, moteurs, micro-forks, audit Ockham, traces).
   3. **Tables & bots** : tailles `3..6` joueurs (`197` assises ou cercles miroirs) et bots mobilisés.
   4. **Volume & durée** : nombre total de parties simulées et durée murale estimée.
   5. **Infra & coût** : backend (`Cloud Run Jobs` gratuit ou `Cloud Batch Spot` avec reprise auto), coût Cloud estimé en euros et **`API LLM 0,00 €`**.

---

## 3. Pilotage Fluide des Longs Tirs Cloud Batch Spot (depuis `CLI Project`)

Lancer la commande unique bout-en-bout :
```bash
uv run python run_campaign.py campaigns/<nom>.json
```
- **Routage automatique (`europe-west9`)** : `<= 50 000` parties → Cloud Run Jobs ; `> 50 000` parties (ou `--backend batch`) → **Cloud Batch Spot** (`c3d-highcpu-4` ou `c3-standard-8`, auto-détection SHA-256 de l'image Docker `worker-pypy`).
- **Résilience Spot autonome** :
  - Chaque worker gère `SIGTERM` (préemption Spot code `50001` / `143`), écrit des checkpoints incrémentaux sur GCS (`--checkpoint-every=20`) et saute les shards déjà complétés (`--skip-existing-shards`).
  - L'orchestrateur relance automatiquement jusqu'à `--max-spot-waves 4` vagues ne ciblant que les shards manquants (`--task-indices`), en journalisant l'état dans `.tmp_runs/campaigns/<nom>/<run_id>/run_state.json` (et `suite_state.json` pour une suite).
  - En cas d'interruption manuelle ou de reprise ultérieure, relancer exactement au point d'arrêt sans recalculer les shards ni les étapes déjà terminés :
    ```bash
    uv run python run_campaign.py campaigns/<nom>.json --backend batch --resume-run-id <run_id>
    ```

---

## 4. Publication Automatique Double & Restitution Auteur

À l'issue de l'agrégation DuckDB + archivage `.tmp_runs/.../cells.parquet` (ZSTD), `run_campaign.py` publie automatiquement (UTF-8 sans BOM, LF) :
1. **Digest exécutif léger (`< 35 Ko`) dans `docs/digests/digest_<nom>.json`** (+ mise à jour de `docs/digests/index.json` avec `verdict`, compteurs d'alertes `danger`/`warn` et liens vers le rapport et les traces) — prêt pour copie en 1 tap dans *Amazonia Doc Studio* et dépôt dans Gemini web.
2. **Rapport Markdown lisible complet dans `docs/rapports/rapport_<nom>.md`** — alertes automatiques d'équilibrage, synthèse globale, spectre `B0..B3` + audit anti-stratégies dégénérées `B3`, ventilation `3J–6J` & `197` assises, tableaux complets Solo / LOO / Levier Synergique `L_syn` / Carrés `2×2` / Moteurs, micro-forks `v6.4`, audit Ockham et index des parties remarquables.
3. **Digest complet non tronqué & dossier Gemini** dans `data/digests/digest_<nom>.json` et `data/digests/PROMPT_GEMINI_<nom>.md`.
4. **Traces remarquables (`human_trace_1.0`)** dans `docs/traces/traces_<nom>.jsonl` (si activées), inspectables en 1 clic via **Importer JSONL** dans `docs/human_logger.html`.
5. **Commit & push GitHub Pages** (`origin main`), désactivable via `--skip-git-push` lors d'une validation locale (`--backend local`).
