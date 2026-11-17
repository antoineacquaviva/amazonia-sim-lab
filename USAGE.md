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

## 3. Lire un bilan détaillé dans Gemini web
À la fin de chaque tir, un fichier léger est créé dans `data/digests/digest_<nom>.json` (ex. `digest_palier2_coeur_muet.json`).
Ouvrez un **nouveau chat Gemini web**, glissez-y ce fichier `.json` et demandez : *« Analyse ce bilan pour l'équilibrage d'Amazonia »*.

## 4. Mettre à jour après une retouche dans *Amazonia Doc Studio*
Dites simplement ici : *« J'ai modifié des règles / des tuiles dans Doc Studio, mets le simulateur à jour. »*

## 5. Basculer entre le PC Windows 11 et le portable Ubuntu
- **En arrivant sur une machine** : `git pull`
- **En quittant une machine** : `git push`
