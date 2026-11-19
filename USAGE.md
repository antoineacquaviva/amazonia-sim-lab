# Aide-Mémoire Auteur — `amazonia-sim-lab`

## 1. Avancer la construction du simulateur
Ouvrez une **nouvelle conversation** par étape pour garder les réponses vives et précises :
- **Palier 2** *(déjà validé)* : joueurs virtuels coopératifs muets, capteurs et 1er lot de tuiles.
- **Lots de tuiles suivants (`Lot 02` à `Lot 11`)** : dites simplement *« Code le prochain lot de tuiles »*.
- **Sélection finale** (quand les 100 tuiles sont codées) : dites *« Cherche la sélection canonique de 32 tuiles »*.

## 2. Lancer des simulations en français courant (exemples)
- *« Simule des parties pour comparer les variantes A, B et C du Gardien G3 de 3 à 6 joueurs. »*
- *« Mesure l'effet sur la survie des arbres si on décale le seuil de parade de +1. »*
- *« Observe comment tournent les parties à 3 joueurs par rapport à 6 joueurs avec les tuiles actuelles. »*
- *« Cherche quelles combinaisons de règles donnent le meilleur équilibre entre les 3 fins de partie. »*

## 3. Lire un bilan détaillé dans l'application Gemini (Téléphone Android & PC)
À la fin de chaque tir, le simulateur génère un dossier 100 % auto-portant (`active_core_rules` + `tested_tiles_rules` + quantiles, `CVaR_20%`, intervalles inter-blocs, `telemetry` et `tile_metrics`) publié dans `docs/digests/digest_<nom>.json` (`< 35 Ko` visé) :
- **Geste unique Mobile & PC (Recommandé — depuis Amazonia Doc Studio)** :
  1. Ouvrez **Amazonia Doc Studio** (GitHub Pages ou `docs/index.html`).
  2. **Sélectionnez la campagne** dans le menu déroulant `📊 Bilan simulation` du bandeau supérieur (ou importez un `.json` en local).
  3. Touchez / cliquez sur **`📋 Copier Bilan Gemini`** (`✅ Bilan copié (XX Ko)`).
  4. **Collez directement dans Gemini** (l'amorce d'activation + tout le digest auto-portant sont copiés en 1 tap, sans `Shift + Clic` ni passage par l'Explorateur).
- **Alternatives locales / hors-ligne** :
  - `data/digests/PROMPT_GEMINI_<nom>.md` (glisser-déposer ou `Ctrl+V` sur PC, ou Google Drive `Amazonia_Digests` sur Android).

## 4. Mettre à jour après une retouche dans *Amazonia Doc Studio*
Dites simplement ici : *« J'ai modifié des règles / des tuiles dans Doc Studio, mets le simulateur à jour. »*

## 5. Basculer entre le PC Windows 11 et le portable Ubuntu
- **En arrivant sur une machine** : `git pull`
- **En quittant une machine** : `git push`
