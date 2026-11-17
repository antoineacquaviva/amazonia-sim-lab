---
name: run-campaign
description: >-
  Lance des simulations de parties et répond aux questions d'équilibrage en français courant :
  utiliser dès que l'auteur demande de tester une idée, simuler des parties, mesurer l'effet
  d'une règle, comparer des variantes A/B/C/D d'une tuile, observer comment une partie tourne,
  vérifier la difficulté de 3 à 6 joueurs ou chercher de bonnes configurations.
---

# Skill `run-campaign` — Simulations à la Demande & Synthèse Auteur

## 1. Pré-Vérification Métier en Coulisses (Silencieuse pour l'Auteur)
Avant de lancer une simulation, l'agent vérifie seul en arrière-plan :
1. **Disponibilité des tuiles** : tous les profils concernés sont bien codés dans `list_registered_tiles()` (sans `NEEDS_KERNEL_HOOK`).
2. **Présence réelle autour de la table (`MATRICE_PAIRES`)** : si l'auteur teste une ou plusieurs tuiles `G/R/M`, filtrer automatiquement les cercles de peuples où ces tuiles sont effectivement en jeu (toujours en paires miroirs `(Cercle, Cercle_Miroir)` sur les mêmes tirages aléatoires).
3. **Sécurité & rapidité** : garde-fou `max_steps = 2000` actif et micro-essai local de **20 parties** sous PyPy en `< 1,5 s`.
4. **Choix automatique du moteur d'exécution en coulisses (sans jamais exposer le jargon à l'auteur)** :
   - Question ciblée sur une décision d'étape 2 ou l'effet caché des paravents -> **analyse par bifurcations contrôlées** (`campaigns/designs.py`).
   - Tir rapide **<= 5 min** (jusqu'à ~`500 000` parties `B0` ou ~`100 000` parties `B2`) -> exécution parallèle gratuite sur `europe-west9` (`--workers=2`).
   - Recherche longue **5 min à 2 h** -> exécution parallèle longue sur `europe-west9` (`c3d-highcpu` Spot, `maxRunDuration: "7200s"`).
   - **Zéro appel API LLM payant** : interdiction absolue d'appeler une API Gemini/Vertex depuis Python.

---

## 2. Devis de Validation en 5 Lignes (Français Clair d'Auteur, Zéro Jargon Cloud)
Toujours présenter ce devis simple de **5 lignes** en français naturel avant de lancer le calcul :
1. **Question testée** : reformulation limpide de l'hypothèse de jeu étudiée.
2. **Ce qu'on compare** : règles, variantes `A/B/C/D` de tuiles ou comportements de joueurs virtuels mis face à face.
3. **Tables & nombre de joueurs couverts** : configurations de peuples et tailles de table (`3`, `4`, `5` et/ou `6` joueurs, avec miroirs).
4. **Volume & durée estimée** : nombre total de parties simulées et temps d'attente estimé (en secondes ou minutes).
5. **Coût estimé** : **`0 €`** (palier gratuit) ou montant estimé en euros sur les crédits.

---

## 3. Exécution & Rapatriement Automatique
1. Mettre à jour l'image worker PyPy uniquement si `engine/`, `bots/` ou `campaigns/` a changé depuis le dernier tir.
2. Exécuter le tir sur `europe-west9` en fixant explicitement `--workers=<vcpu_par_tache>`.
3. Rapatrier les résultats dans `.tmp_runs/<nom_campagne>/shards/`.

---

## 4. Synthèse Analytique DuckDB & Fichier `digest_<nom_campagne>.json` (`< 30 Ko`)
Avec **CPython 3.12 + DuckDB** (`uv run python ...`) :
1. Archiver les données détaillées en `.tmp_runs/<nom_campagne>/cells.parquet` (compression ZSTD).
2. Calculer les indicateurs utiles à l'auteur :
   - Taux moyen d'Arbres sauvés, médiane et **pire quintile des tables (`20 %` les plus dures)**,
   - Durée moyenne en tours et répartition des 3 fins (*Fin du Tour 8*, *Rêve au rang 1*, *Réveil des Gardiens*),
   - Charge mentale mesurée par les 4 capteurs (éléments à retenir, lois simultanées, manipulations par décision, cascades),
   - Marge d'incertitude à `95 %` entre tables miroirs.
3. Écrire `data/digests/digest_<nom_campagne>.json` (UTF-8 sans BOM, LF, **strictement `< 30 Ko`**) prêt à être glissé dans un chat Gemini web.
