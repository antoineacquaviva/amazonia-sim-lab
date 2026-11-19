# AMAZONIA DOC STUDIO — Référentiel Fonctionnel & Technique (v5.3)

> **Usage IA (Pièce Jointe de Prompt)** : Ce document décrit l'architecture, le périmètre fonctionnel, les modèles de données et les règles strictes de maintenance de l'application **Amazonia Doc Studio**. Toute modification proposée par une IA doit respecter le découplage des 4 couches et les invariants techniques détaillés en Section 5.

---

## 1. Identité & Rôle dans l'Écosystème

- **Projet** : *Amazonia : Dernier Rempart* — Jeu de société coopératif asymétrique à communication muette (3 à 6 joueurs, 8 tours max).
- **Application** : **Amazonia Doc Studio** (`v5.3` consolidée — 25 arbitrages formels).
- **Dépôt & Hébergement** :
  - GitHub : `https://github.com/antoineacquaviva/amazonia-doc-studio`
  - Production (GitHub Pages) : `https://antoineacquaviva.github.io/amazonia-doc-studio/`
- **Vocation (« Source Unique de Vérité »)** : Maintenir dans un référentiel unique et sans dérive documentaire :
  1. Le **Livret de Règles Didactique** dynamique destiné aux joueurs humains (imprimable en PDF propre).
  2. La **Bibliothèque complète d'asymétrie** (32 emplacements / **100 profils** `A`, `B`, `C`, `D`).
  3. Le **Journal de traçabilité des versions et arbitrages** (`v4.3` → `v5.3`).
  4. Le **Contrat formel JSON** consommé par le simulateur Monte-Carlo Python (`amazonia-sim` / `foret-automate-lab`) et le portage **Board Game Arena (BGA)**.

---

## 2. Périmètre Fonctionnel (Interface Utilisateur)

L'application est une **SPA statique sans bundler** (compatible `file://` et HTTPS) articulée autour d'un bandeau configurateur persistant et de 4 vues synchronisées en temps réel via l'état réactif `state`.

### 2.1. Bandeau Supérieur & Configurateur d'Instance
- **Presets (`bundleId`)** : `STANDARD_A`, `ESSAI_52_EMBUSCADE`, 5 modules `N=3` joueurs (`52_CAPYBARA_D`, `52_HARPIE_D`, `52_DENDROBATE_D`, `52_PIERRE_D`, `52_ATELE_D`) ou `CUSTOM`.
- **Cercle des Peuples (`peuplesCercle`)** : 3 à 6 Peuples actifs ordonnés autour de la table parmi `M` (Mammifères), `R` (Reptiles), `O` (Oiseaux), `H` (Humains), `E` (Entités Magiques), `I` (Insectes). Détermine via `MATRICE_PAIRES` les `2N` Tuiles de Synergie sur les `N` lisières.
- **Slots de Migration (`slotsInsectes`)** : `SLOT_BUG_CERVEAU` (`A/B/C`) et `SLOT_COLONISATION_GARDIENS` (`A/C`).
- **Les 7 Axes du Châssis (`CHASSIS_AXES_SPEC` — $2^7 = 128$ configurations)** :
  1. `P_Max` : `4` (`P4_2233` `[2,2,3,3]` = $10N$ Arbres, défaut) | `5` (`P5_22233` `[2,2,2,3,3]` = $12N$ Arbres).
  2. `Regle_Ouverture_Reve_Multiple` : `UNIQUE_PAR_TOUR` (défaut) | `PAR_DE_M_DESIGNE`.
  3. `Offset_Seuil_Parade` : `0` (défaut) | `1`.
  4. `Mise_En_Place_Tactiques` : `ORDRE_FIXE_T1_T6` (défaut) | `ALEATOIRE`.
  5. `Declenchement_Fin_De_Piste` : `ARRIVEE_DERNIERE_PARCELLE` (défaut) | `DEPASSEMENT_DERNIERE_PARCELLE`.
  6. `Role_Abatteuse_Fin_De_Piste` : `STANDARD_COUPE_ARBRE` (défaut) | `ARRACHE_1_SOUCHE_SI_SANS_ARBRE`.
  7. `Synergie_Binome_Machines` : `INDIVIDUELLE` (défaut) | `MUTUALISATION_PUISSANCE_MEME_PARCELLE`.
- **Export IA contextuel (`✨ Copier contexte Gemini`)** : Copie un JSON structuré (`_meta`, `regles_coeur`, `instance`, `tuiles_ciblees`) limité aux tuiles en jeu ou filtrées (`Shift + Clic` = export complet des 100 profils + tête du changelog).

### 2.2. Les 4 Vues Synchronisées
1. **📖 1. Livret Didactique (`#view-livret`)** : Règles humaines complètes compilées dynamiquement pour l'instance active, avec tableau des `2N` tuiles, autorité par Peuple d'origine et surlignage ambre commutable des blocs dynamiques.
2. **🧩 2. Explorateur des 100 Profils (`#view-catalogue`)** : Recherche plein texte, filtres par famille/peuple/lettre/tags, comparaison côte à côte `A/B/C/D` et activation directe dans l'instance.
3. **🔍 3. Évolutions & Arbitrages (`#view-changelog`)** : Différentiel historique structuré `Avant / Après` de `v4.3` à `v5.3`.
4. **💻 4. Spec & JSON Simulateur (`#view-json`)** : Export, téléchargement `.json` et réimportation d'un manifeste d'instance (`schema_version: "5.3"`) + mémento des 8 Primitives Atomiques.

---

## 3. Architecture Technique & Découplage des 4 Couches

```text
amazonia-doc-studio/
├── index.html                      # Coquille UI (Tailwind CDN), état réactif state, filtres, export JSON/Gemini
├── AMAZONIA_STUDIO_CONTEXT.md      # Présent référentiel fonctionnel & technique pour prompts IA
├── data/
│   ├── amazonia_data_v5_3.js       # Source JS : PEUPLES, MATRICE_PAIRES, CHASSIS_AXES_SPEC,
│   │                               # CATALOGUE_TUILES (32 slots / 100 profils), VERSION_CHANGELOG, SPEC_FORMELLE_V5_3
│   ├── livret_v5_3.js              # Règles humaines découplées : REGLES_COEUR_SYNTHESE + renderDidacticRulebook()
│   ├── catalog_v5_3.json           # Miroir JSON pur du catalogue et du châssis (pour Python / BGA)
│   └── spec_formelle_v5_3.json     # Contrat formel normé des 6 étapes du tour et des 25 arbitrages v5.3
└── scripts/                        # Scripts incrémentaux d'audit et de synchronisation (Node.js & Python)
```

**Ordre de chargement dans `index.html`** : `data/amazonia_data_v5_3.js` → `data/livret_v5_3.js` → script inline d'UI (`refreshAllUI()`).

---

## 4. Modèles de Données & Invariants Mécaniques Cœur (v5.3)

### 4.1. Répartition des 32 Emplacements (100 Profils exactement)
- **Gardiens `G1..G15`** (45 profils) · **Rêves `R1..R10`** (31 profils) · **Nids de Croissance `M1..M5`** (19 profils) · **Slots Migration `SLOT_BUG_CERVEAU` & `SLOT_COLONISATION_GARDIENS`** (5 profils — `Colonisation B` et les anciens profils `E` sont supprimés en v5.3, soit exactement 100 profils).
- Chaque profil possède : `nom`, `cycle`, `cablage`, `fenetre`, `primitive` (parmi les 8 primitives : `MOD_SEUIL`, `CREATION_ENTITE`, `DEPLACEMENT`, `MOD_PUISSANCE`, `MOD_APPRENTISSAGE`, `PERMUTATION_PISTE`, `PARTAGE_INFO_ETAT_GARDIEN`, `MOD_LOI_DU_COEUR`), `tags`, `requires_options`, `texte` et `temoin`.

### 4.2. Invariants Mécaniques Cœur Consolidés (Socle des 25 Arbitrages)
- **Tirage & Dés épurés (Étape 1)** : Paquet contenant les cartes Machine hors Siège + toutes les cartes Sabotage acquises. Seul un joueur ayant tiré une **carte Machine** lance 2D6 sous paravent et retient `M = min(D1, D2)` (ou `max` sous Loi). Si le rang `M` porte un Rêve en `3.2`, la machine est annulée et le Rêve s'ouvre.
- **Sabotage par dilution permanente** : Toutes les cartes Sabotage sont identiques et sans effet propre (réserve illimitée). **1 Sabotage acquis** (`4.1`, `4.2`, Gardien) = `+1` carte Sabotage mise de côté et intégrée **définitivement** au paquet Machine au remélange de `6.3` (allume `3. Sabotage`). **1 carte Sabotage piochée à l'Étape 1** = 1 action du Contremaître perdue ce tour-ci (puis remélangée en `6.3`).
- **Gouvernance unitaire** : Chaque Tuile (`G`, `R`, `M`) et piste de Migration est décidée uniquement par le joueur de son `peuple_origine` (`origine`). Zéro vote de groupe.
- **Furtivité à 4 emplacements jumeaux** : 2 emplacements jumeaux par rive (max 2 Défenseurs/case). **Entrer** sur la case (toute face) tire l'éventuel autre Défenseur sur l'emplacement jumeau du même bord et oriente l'unique action du binôme en `4.1` (sur la parcelle de cette seule rive) ; **retourner** de *réflexion* à *définitif* se fait strictement sur place sans déplacement.
- **Combat d'un seul tenant & Chaîne des parades** : Ordre Tactiques `1 → 6` puis Sièges (Abatteuse avant Bulldozer sur un même rayon ; libre entre rayons distincts). Chaque machine résout d'un seul tenant ses cibles (lues depuis sa position réelle à l'instant de l'attaque en sautant les Routes Forestières), ses frappes (`1° Jaguar [2 bleus] → 2° Harpie → 3° Piège Embuscade [si Défense totale >= 1] → 4° Parade classique [défausse immédiate des Insectes manquants]`), son avancée `T3/T6` et son gain `+1 Rouge` `T4/T5/T6`. **Zéro dette d'Insectes et zéro verrouillage des parcelles ciblées** (seul un Piège déjà déclenché ce tour ne peut plus payer un coût volontaire avant son retrait en `5.3`).
- **Siège `T4` & Apprentissage (`6.1 / 6.2`)** : Toute machine sur la dernière parcelle non rasée est en Siège irréversible : son attaque reste autonome même si `T4` est éjectée, et en `6.1` elle génère normalement de l'Apprentissage sur `T4` tant que `T4` figure sur la piste (`+1`/parcelle réellement endommagée `+1`/Rouge acquis `-1`/Bleu présent, plancher 0). Retraits volontaires avant Bugs ; remise à zéro de 100 % des jetons Apprentissage en `6.2` dans tous les cas.
- **Cascades à plat (`1 → 6`) & Fin de partie** : Fin complète de l'effet/Nid en cours, marquage immédiat à l'ouverture, balayage croissant `1..6` répété, Faces 2 autonomes. Seuil de Réveil fixe calculé à la mise en place (inactif si `< 3` Gardiens). Vérification en fin de `5.3` (+ exception `R9 B` en `6.2`).

---

## 5. Règles d'Or de Maintenance pour une IA Collaboratrice

1. **Synchronisation obligatoire des 4 couches** : Toute évolution de règle doit mettre à jour simultanément `data/livret_v5_3.js` (`renderDidacticRulebook` **ET** `REGLES_COEUR_SYNTHESE`), `data/amazonia_data_v5_3.js` (`CATALOGUE_TUILES`, `VERSION_CHANGELOG`, `SPEC_FORMELLE_V5_3`), `data/catalog_v5_3.json` et `data/spec_formelle_v5_3.json`.
2. **Patchs différentiels via Node `vm` + `JSON.stringify`** : Ne jamais réécrire tout le catalogue à la main dans une réponse LLM ni injecter des chaînes JS par regex brutes (risque de casse sur les apostrophes `'` vs `’`). Charger l'objet dans un contexte Node `vm`, muter les clés ciblées, resérialiser via `JSON.stringify` et vérifier par `new vm.Script()`.
3. **Couple `texte` + `temoin` & Faces 2 autonomes** : Ne jamais laisser `temoin` vide et toujours mettre à jour `temoin` quand `texte` change. Sur un Gardien double-face, le texte de la **Face 2** doit se suffire à lui-même sans renvoyer à la Face 1 cachée.
4. **Encodage & PowerShell** : Écrire tous les fichiers en **UTF-8 sans BOM** avec fins de ligne `\n`. Sous Windows PowerShell 5.1, préférer l'exécution d'un fichier script (`node "scripts/xxx.js"`) aux one-liners `node -e "..."` (qui altèrent les guillemets doubles).
