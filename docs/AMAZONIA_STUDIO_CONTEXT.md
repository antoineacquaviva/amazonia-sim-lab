# AMAZONIA DOC STUDIO — Référentiel Fonctionnel & Technique (v5.5)

> **Usage IA (Pièce Jointe de Prompt)** : Ce document décrit l'architecture, le périmètre fonctionnel, les modèles de données et les règles strictes de maintenance de l'application **Amazonia Doc Studio**. Toute modification proposée par une IA doit respecter le découplage des 4 couches et les invariants techniques détaillés en Section 5.

---

## 1. Identité & Rôle dans l'Écosystème

- **Projet** : *Amazonia : Dernier Rempart* — Jeu de société coopératif asymétrique à communication muette (3 à 6 joueurs, 8 tours max).
- **Application** : **Amazonia Doc Studio** (`v5.5`, `schema_version: "5.5.0"` — Socle figé).
- **Dépôt & Hébergement** :
  - GitHub : `https://github.com/antoineacquaviva/amazonia-sim-lab` (`docs/`)
  - Production (GitHub Pages) : `https://antoineacquaviva.github.io/amazonia-sim-lab/`
- **Vocation (« Source Unique de Vérité »)** : Maintenir dans un référentiel unique et sans dérive documentaire :
  1. Le **Livret de Règles Officiel** destiné aux joueurs humains (refondu de zéro en v5.5 en 7 chapitres didactiques, zéro jargon technique, imprimable en PDF propre).
  2. La **Bibliothèque complète d'asymétrie** (32 emplacements / **101 profils** `A`, `B`, `C`, `D` incluant les 30 tuiles actives `STANDARD_A` + `SLOT_BUG_CERVEAU:B` + `SLOT_COLONISATION_GARDIENS:B`).
  3. Le **Journal de traçabilité des versions et arbitrages** (`v4.3` → `v5.5`).
  4. Le **Contrat formel JSON** consommé par le simulateur Monte-Carlo Python (`amazonia-sim-lab`) et le futur portage **Board Game Arena (BGA)**.

---

## 2. Périmètre Fonctionnel (Interface Utilisateur)

L'application est une **SPA statique sans bundler** (compatible `file://` et HTTPS) articulée autour d'un bandeau configurateur persistant et de 4 vues synchronisées en temps réel via l'état réactif `state`.

### 2.1. Bandeau Supérieur & Configurateur d'Instance
- **Presets (`bundleId`)** : `STANDARD_A` (socle actif v5.5 avec `SLOT_BUG_CERVEAU=B` et `SLOT_COLONISATION_GARDIENS=B`), presets d'exploration et `CUSTOM`.
- **Cercle des Peuples (`peuplesCercle`)** : 3 à 6 Peuples actifs ordonnés autour de la table parmi `M` (Mammifères), `R` (Reptiles), `O` (Oiseaux), `H` (Humains), `E` (Entités Magiques), `I` (Insectes). Détermine via `MATRICE_PAIRES` les `2N` Tuiles de Synergie sur les `N` lisières.
- **Slots de Migration (`slotsInsectes`)** : `SLOT_BUG_CERVEAU` (`B` par défaut : Déviation de dé `±1` sur Piste des Tactiques) et `SLOT_COLONISATION_GARDIENS` (`B` par défaut : Bouclier de lisière en `5.3`).
- **Les 6 Axes du Châssis (`CHASSIS_AXES_SPEC` — $6 \times 2^5 = 192$ configurations)** :
  1. `Profil_Piste` : 6 profils homogènes (`P4_2233`, `P4_2223`, `P4_1223`, `P5_22233`, `P5_22223`, `P5_12223`).
  2. `Regle_Ouverture_Reve_Multiple` : `UNIQUE_PAR_TOUR` (défaut) | `PAR_DE_M_DESIGNE`.
  3. `Offset_Seuil_Parade` : `0` (défaut) | `1`.
  4. `Placement_Initial_Machines` : `MEME_PARCELLE_P1` (défaut) | `BULLDOZER_P1_ABATTEUSE_P2`.
  5. `Role_Abatteuse_Fin_De_Piste` : `STANDARD_COUPE_ARBRE` (défaut) | `ARRACHE_1_SOUCHE_SI_SANS_ARBRE`.
  6. `Synergie_Binome_Machines` : `INDIVIDUELLE` (défaut) | `MUTUALISATION_PUISSANCE_MEME_PARCELLE`.
- **Export IA contextuel (`✨ Copier contexte Gemini`)** : Copie un JSON structuré (`_meta`, `regles_coeur`, `instance`, `tuiles_ciblees`) limité aux tuiles en jeu ou filtrées (`Shift + Clic` = export complet + tête du changelog).
- **Bilan de Campagne & Copie 1-Tap (`📊 Bilan simulation` + `📋 Copier Bilan Gemini`)** : Charge `digests/index.json` (ou import local `.json` en `file://`) et copie en 1 seul tap l'amorce d'analyse + le `digest_*.json` 100 % auto-portant (`active_core_rules`, `tested_tiles_rules`, `defense_attribution`, quantiles, `CVaR_20%`, intervalles inter-blocs, `telemetry`, `tile_metrics`).

### 2.2. Les 4 Vues Synchronisées
1. **📖 1. Livret Didactique (`#view-livret`)** : Livret joueur refondu de zéro en 7 sections (Présentation & Objectif, Matériel & Mise en place, Vue d'ensemble d'un tour, Déroulé étape par étape, Les Peuples et leurs mécaniques propres, Fin de partie & Repousse Finale, Mémento de table) avec tableau des `2N` tuiles et surlignage ambre commutable.
2. **🧩 2. Explorateur des Profils (`#view-catalogue`)** : Recherche plein texte, filtres par famille/peuple/lettre/tags, comparaison `A/B/C/D`, bandeau socle figé `v5.5` et indicateurs `tile_metrics` du bilan actif.
3. **🔍 3. Évolutions & Arbitrages (`#view-changelog`)** : Différentiel historique structuré `Avant / Après` de `v4.3` à `v5.5`.
4. **💻 4. Spec & JSON Simulateur (`#view-json`)** : Export, téléchargement `.json` et réimportation d'un manifeste d'instance (`schema_version: "5.5.0"`).

---

## 3. Architecture Technique & Découplage des 4 Couches

```text
docs/
├── index.html                      # Coquille UI (Tailwind CDN), état réactif state, filtres, export JSON/Gemini
├── AMAZONIA_STUDIO_CONTEXT.md      # Présent référentiel fonctionnel & technique pour prompts IA
├── data/
│   ├── amazonia_data_v5_5.js       # Source JS : PEUPLES, MATRICE_PAIRES, TOPOLOGIES_PISTE_SPEC, CHASSIS_AXES_SPEC,
│   │                               # CATALOGUE_TUILES (32 slots / 101 profils), VERSION_CHANGELOG, SPEC_FORMELLE_V5_5
│   ├── livret_v5_5.js              # Règles humaines découplées : REGLES_COEUR_SYNTHESE + renderDidacticRulebook()
│   ├── catalog_v5_5.json           # Miroir JSON pur du catalogue et du châssis (pour Python / BGA)
│   └── spec_formelle_v5_5.json     # Contrat formel normé du socle figé v5.5
└── scripts/                        # Scripts incrémentaux d'audit et de synchronisation (Node.js)
```

**Ordre de chargement dans `index.html`** : `data/amazonia_data_v5_5.js` → `data/livret_v5_5.js` → script inline d'UI (`refreshAllUI()`).

---

## 4. Invariants Mécaniques Cœur Figés (`v5.5`)

- **Piste des Tactiques fixe (`T1..T6`) & Rêves en coût d'activation** : Les 6 Tactiques sont imprimées en dur (zéro éjection, zéro Apprentissage `6.1`). Un Rêve construit se pose sur la case libre la plus à droite (`6 → 1`). À l'Étape `2.2`, chaque **Défenseur** posé sur un Rêve annule en `3.2` 1 machine pointant sur son rang (la plus menaçante en priorité). Le Rêve n'avance d'1 cran vers la gauche (saut/poussée vers la 1re case libre) que si **toutes** les machines pointant sur ce rang sont annulées ce tour-ci.
- **Piste des Gardiens & Pari uniforme (`0`, `1` ou `2` Défenseurs)** : En `2.2`, jusqu'à **2 Défenseurs** par Gardien construit (même plafond uniforme sur les 6 cases). Chaque déclenchement du Gardien glisse 1 Défenseur sous sa tuile et exécute son effet sur sa face actuelle. En `5.3` : pari gagné (tous les Défenseurs glissés) → reste en piste et passe Face 2 si double-face ; pari perdu (au moins 1 Défenseur encore dessus) → retourne en lisière Face 1, sauf Bouclier de lisière.
- **Partition stricte des 6 déclencheurs (« 1 événement = au plus 1 déclencheur »)** :
  - À l'ouverture des paravents (`3.2`) : `3. Sabotage` > `6. Insecte` (déviation par Insecte sur la Piste des Tactiques) > `5. Rêve` (dé `M` pointant sur un rang Rêve).
  - Pendant les attaques (`5.1`/`5.2`) : `2. Piégeage` > `6. Insecte` (Parade utilisant au moins 1 Insecte) > `1. Parade` (Parade par Défenseurs seuls).
  - Case `4. Gardien` : 1re ouverture du tour de chaque autre Gardien distinct (avec anti-boucle : un Gardien sur la case 4 ne se réactive jamais lui-même).
  - Ni la Furtivité (`4.1`) ni la production des Nids (`4.2`) n'allument de déclencheur.
- **Peuple Insectes (`v5.5`)** : Déviation de dé `±1` sur la Piste des Tactiques (`SLOT_BUG_CERVEAU=B`) et **Bouclier de lisière** sur la Piste des Gardiens (`SLOT_COLONISATION_GARDIENS=B` : en `5.3`, défausser 1 Insecte sur la case d'un Gardien ayant perdu son pari le maintient en piste sur sa face actuelle, le pari restant perdu).
- **3 Fins de partie & Repousse Finale (`5.3`)** : Priorité absolue au **Tour 8** ; aux Tours `1..7`, **Sommeil du Contremaître** (tous les Rêves en jeu en bloc contigu en tête de piste) et **Réveil de la Forêt** (100 % Piste des Gardiens : `>= 1` Animal Sauvage, tous les `N` Défenseurs engagés sur des Gardiens et aucun pari perdu). En toute fin de partie : Repousse Finale (`+1` Arbre debout sur chaque parcelle non rasée conservant au moins 1 Souche, dans la limite de sa dotation initiale).

---

## 5. Règles d'Or de Maintenance pour une IA Collaboratrice

1. **Synchronisation obligatoire des 4 couches** : Toute évolution de règle doit mettre à jour simultanément `docs/data/livret_v5_5.js` (`renderDidacticRulebook` **ET** `REGLES_COEUR_SYNTHESE`), `docs/data/amazonia_data_v5_5.js` (`CATALOGUE_TUILES`, `VERSION_CHANGELOG`, `SPEC_FORMELLE_V5_5`), `docs/data/catalog_v5_5.json` et `docs/data/spec_formelle_v5_5.json`, puis régénérer `data/studio_lock.json` et `data/spec_bundle_v5_5.json`.
2. **Patchs différentiels via Node `vm` + `JSON.stringify`** : Charger l'objet dans un contexte Node `vm`, muter les clés ciblées, resérialiser via `JSON.stringify` et vérifier par `new vm.Script()`.
3. **Qualité éditoriale du livret joueur (`livret_v5_5.js`)** : Zéro jargon technique ni code interne, zéro formulation rétrospective négative, toujours le terme simple « Défenseur », contrôlé automatiquement par `contracts/studio_rules_guards.json` et `tests/test_studio_render_and_guards.py`.
4. **Encodage & compatibilité statique** : Écrire tous les fichiers en **UTF-8 sans BOM** avec fins de ligne `\n` (LF), compatibles `file://` et HTTPS.
