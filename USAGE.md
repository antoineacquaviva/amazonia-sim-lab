# Aide-Mémoire Auteur — `amazonia-sim-lab` (`v6.4`)

## 1. Lancer des simulations & études modulaires en français courant (exemples)
Formulez simplement votre question de design ; la skill `run-campaign` génère le manifeste `campaigns/<nom>.json`, affiche un **devis clair en 5 lignes (`0,00 €` API LLM)** avant lancement et orchestre le tir :
- **Tuiles à blanc (solo, retrait LOO, synergie)** : *« Mesure le plancher solo, la perte au retrait et le levier synergique de chacune des 30 tuiles en paires CRN. »*
- **Carrés `2×2` & moteurs** : *« Teste les carrés 2×2 des 15 lisières et compare les 5 moteurs disjoints et les 7 moteurs à tuiles-pivots seuls puis par ablation. »*
- **197 assises & stratégies dégénérées** : *« Couvre les 197 assises de 3 à 6 joueurs sur B0..B3 pour traquer d'éventuelles stratégies dégénérées et extraire les parties remarquables. »*
- **Micro-forks `v6.4` & Ockham** : *« Lance les micro-forks causaux v6.4 (Sentinelles, Éveil A+1, Chamanes, Altération, icônes Gardiens) et audite les faux dilemmes > 90 %. »*

Modèles prêts à l'emploi : `campaigns/manifests/etude_modulaire_v6_4.json` et `campaigns/manifests/suite_complete_v6_4.json`.

## 2. Commandes utiles (`run_campaign.py`)
- **Devis 5 lignes sans rien lancer (`0 €`)** : `uv run python run_campaign.py campaigns/<nom>.json --quote-only`
- **Validation locale (`0 €`, sans GCP)** : `uv run python run_campaign.py campaigns/<nom>.json --backend local --skip-git-push`
- **Grand tir Cloud Batch Spot (reprise auto sur préemption)** : `uv run python run_campaign.py campaigns/<nom>.json --backend batch --max-spot-waves 4`
- **Reprendre un tir ou une suite interrompue** : `uv run python run_campaign.py campaigns/<nom>.json --backend batch --resume-run-id <run_id>`

## 3. Lire les bilans, rapports Markdown et parties remarquables
À l'issue de chaque campagne (ou `campaign_suite`), le pipeline publie automatiquement :
- **Digest exécutif léger (`< 35 Ko`) + alertes automatiques** : `docs/digests/digest_<nom>.json` (copie 1-tap `📋 Copier Bilan Gemini` dans *Amazonia Doc Studio* → `docs/index.html` ou GitHub Pages).
- **Rapport Markdown lisible complet** : `docs/rapports/rapport_<nom>.md` (alertes, `3J–6J`, `197` assises, `B0..B3`, Solo/LOO/`2×2`/Moteurs, micro-forks `v6.4`, Ockham).
- **Digest complet archivé & dossier Gemini** : `data/digests/digest_<nom>.json` et `data/digests/PROMPT_GEMINI_<nom>.md`.
- **Parties remarquables (`human_trace_1.0`)** : `docs/traces/traces_<nom>.jsonl` — ouvrez `docs/human_logger.html` puis cliquez sur **Importer JSONL** pour rejouer visuellement chaque partie remarquable hors-ligne.

## 4. Mettre à jour après une retouche dans *Amazonia Doc Studio*
Dites simplement : *« J'ai modifié des règles / des tuiles dans Doc Studio, mets le simulateur à jour. »*

## 5. Hygiène Git multi-postes
- **En arrivant** : `git pull --ff-only origin main`
- **En quittant** : `uv run python verify_lot.py` puis `git push origin main`
