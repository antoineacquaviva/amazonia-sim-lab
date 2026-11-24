# AMAZONIA DOC STUDIO — Référentiel Fonctionnel & Technique (`v6.2` SSOT)

> **Usage IA (Pièce Jointe de Prompt)** : Ce document décrit l'architecture SSOT `v6.2`, les arbitrages d'auteur définitifs, le modèle de données et les garde-fous automatiques d'**Amazonia Doc Studio**. Toute modification proposée par une IA doit éditer les contrats de `contracts/`, exécuter `uv run python scripts/build_studio_artifacts.py` et passer `uv run python verify_lot.py` à 100 % au vert.

---

## 1. Identité & Rôle dans l'Écosystème

- **Projet** : *Amazonia : Dernier Rempart* — Jeu de société coopératif asymétrique à communication muette (`3` à `6` joueurs, `8` tours max en `2` Actes).
- **Cible unifiée** : **`v6.2` (`schema_version: "6.2.0"`)** — *Socle épuré + Asymétrie Hybride `3 + 3` + Enracinement volontaire + Canon 0 de 30 tuiles*.
- **Dépôt & Hébergement** :
  - GitHub : `https://github.com/antoineacquaviva/amazonia-sim-lab` (`docs/`)
  - Production (GitHub Pages) : `https://antoineacquaviva.github.io/amazonia-sim-lab/`
- **Architecture Source Unique de Vérité (SSOT)** :
  1. `contracts/rules_canon_v6_2.json` : contrat formel typé unique (châssis unique verrouillé `P4_2233` départ décalé `Bulldozer p=1 / Abatteuse p=2`, matériel fini recto-verso, sac opaque, supports fixes, formule de Seuil, 6 icônes Gardiens, séquence du tour, 3 modules, accessoires `3 + 3`, Enracinement volontaire).
  2. `contracts/physical_and_edge_invariants.json` : registre permanent des **22 invariants** (`INV-01` à `INV-22`, catégories `MATERIEL`, `CAS_LIMITE`, `GOUVERNANCE`) avec assertions vérifiables dans le livret joueur (`data-inv="INV-XX"`).
  3. `contracts/tiles_canon_v6_2.json` : catalogue canonique des **30 emplacements** (`G1..G15`, `R1..R10`, `M1..M5` — 30 profils `A`, `48` faces `≤ 25` mots, `35` témoins, `carte_des_roles`, `rapport_audit_197` sur 197 assises et `vivier_candidats_B_C_phase_5`). Les règles de déviation `±1` et de Bouclier de lisière facultatif sont désormais des règles natives du **Module Essaim**.
  4. **Compilateur dérivé unique** (`scripts/build_studio_artifacts.py`) : génère sans aucune constante métier codée en dur les fichiers dérivés de `docs/data/` (`amazonia_data_v6_0.js`, `catalog_v6_0.json`, `spec_formelle_v6_0.json`) ainsi que `data/spec_bundle_v6_0.json` et `data/studio_lock.json`.

---

## 2. Arbitrages d'Auteur Définitifs (`v6.2` — `INV-01` à `INV-22`)

### 2.1. Matériel fini, réversible et auto-vérifiant
- **Arbres / Souches (`INV-01`)** : dotation finie exacte de `10 × N` pions uniques recto-verso (`Arbre debout` / `Souche`, zéro réserve illimitée). L'Abatteuse retourne tous les Arbres debout en Souche sans toucher aux Souches ; le Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches ; toute repousse finale retourne des Souches survivantes en Arbres debout (plafond physique automatique).
- **Jetons Puissance (`INV-02`)** : pièces recto-verso `Rouge (+1)` / `Bleu Surchauffe (−1)`.
- **Défenseurs (`INV-03`, `INV-04`)** : modèle unique de 2 pions recto-verso (`Réflexion` / `Définitif`) par joueur. 1er pion posé directement face `Définitif` (jamais sur les Gardiens) ; 2e pion posé face `Réflexion` puis retourné irréversiblement sur `Définitif` (figeant simultanément le jeton Duel ou la Plume de Vigie). Dès que `N−1` joueurs ont validé, le dernier effectue au plus 1 ultime ajustement. Chez les Humains (`H`) : uniquement 2 pions Chamanes (`1 Tambour` et `1 Chant` recto-verso), binôme imposé auto-vérifiant.

### 2.2. Sac opaque de jetons & Lancer de dés universel
- **Sac opaque (`INV-05`, `INV-06`)** : contient `2N` jetons Machine épais, jetons Sabotage ordinaires et jusqu'à `4` jetons Sabotage `Écaille` (tuiles `R`). Les jetons non piochés restent cachés sans être consultés. En cas de pénurie, distribution horaire depuis le Coordonnateur, **Oiseau toujours servi en dernier**.
- **Dés universels (`INV-07`)** : sous paravent fermé, **tous** les joueurs lancent leurs dés (2 dés standards + Dé d'Envol `1–6` chez `O` sur mini-paravent gradué `1–6`), même sur Sabotage ou Écaille (jet ignoré), éliminant toute fuite sonore.

### 2.3. Supports fixes & Piste des Gardiens à 6 icônes
- **Réglette fixe `1–6` + bandelette d'Acte réversible (`INV-08`)** : cases Rêves au-dessus des actions imprimées (`1/4 Sur place`, `2/5 Devant`, `3/6 En avançant −1`) ; seule la bandelette d'Acte dessous est retournée au début du Tour 5 sans déplacer ni Rêves ni Insectes.
- **Piste des Gardiens à 6 icônes sans numéros (`INV-09`)** : ordre gauche → droite `[PARADE, PIEGEAGE, SABOTAGE, REVE, INSECTE, RESONANCE]` (`1..6` en interne uniquement). La **Résonance** est en 6e et dernière position avec compteur individuel d'activations sans écrasement de bit et reprise gauche → droite si une icône plus à gauche se rallume.
- **Deux encoches latérales visibles par Gardien (`INV-10`)** : en fin d'attaques, `≥ 1` pion encore sur la tuile = pari perdu ; `0` pion dessus et `≥ 1` encoche occupée = pari gagné (passage Face 2) ; `0` pion dessus et `0` encoche occupée = aucune mise engagée (reste en place sur sa face actuelle sans évoluer).

### 2.4. Seuil, Ratissage, Parcelles ciblées, Contacts & Gouvernance
- **Seuil de Parade unifié (`INV-11`)** : en Mode Charge, seuls les jetons rouges sont ignorés ; les **jetons bleus Surchauffe (`−1`) s'appliquent dans TOUS les modes** (Charge, Assaut et Ratissage), `−1` aux rangs `3` et `6`, `minimum 1`. Gain Charge = `+1` rouge max/activation (`FRAPPE_NON_PAREE`).
- **Ratissage physique (`INV-12`)** : au ménage, toute machine terminant sur la dernière parcelle de son rayon glisse son jeton Machine sous elle (hors sac), conserve ses jetons Puissance antérieurs et gagne **`+1` jeton rouge physique** (convertible en bleu ; suppression définitive du `+1` imprimé). Une machine en Ratissage ne se déplace jamais (ni avancée, ni recul, ni cale, ni Altération, ni rang), mais sa parcelle compte pleinement comme « parcelle ciblée » tant qu'elle n'a pas frappé.
- **Parcelles ciblées & Repli de bordure (`INV-13`)** : les parcelles visées par une machine sont figées au début de son activation (toute cible devenue Route entre-temps est annulée sans report). Une poussée de Route en bordure vers le cœur couvre et remplace l'avancée finale de `En avançant` (jamais de double bond `+2`).
- **Ouverture, Rêves & Furtivité (`INV-14`, `INV-15`)** : les jetons Machine révélés restent visibles devant leur rayon jusqu'au verdict de Furtivité (inclinés à 90° s'ils sont annulés). Ordre : Sabotage/Écaille un par un (+ balayage) → déviation `±1` une par une (+ balayage) → Rêves défendus de gauche à droite (le propriétaire choisit quelle(s) machine(s) sont annulées y compris déviées, résout intégralement le pouvoir propre dès que défendu même à 0 machine hors *« Quand ce Rêve annule… »*, puis allume `REVE` + balayage si `≥ 1` annulation). Les Défenseurs posés sur un Rêve se déplacent toujours avec lui.
- **Zéro écrasement hors Route & Pièges (`INV-16`, `INV-17`)** : déplacer une machine laisse Nids, Insectes, Pièges et Duel intacts. Seule la création d'une Route Forestière vide la case (Nid en lisière reconstructible, Défenseurs en main, Piège/Croc/Insectes/Duel en réserve). Max 1 Piège ordinaire autonome (`SINGLE_STRIKE`) par parcelle ; le `Croc` Reptile peut cohabiter et pare en premier.
- **Gouvernance & Poses (`INV-18`, `INV-19`)** : Bouclier de lisière facultatif gouverné par `I` ; interdiction de compléter une tuile impossible à placer ; repli de 1re pose sur une parcelle alliée si aucun emplacement légal ; bâtisseurs couchés « en attente » devant leur propriétaire dès construction, avec maintien du bonus à 3 joueurs libérant 1 bâtisseur vers une parcelle adjacente sur Gardien ou Rêve.

### 2.5. Architecture Modulaire, Accessoires `3 + 3` & Enracinement
- **3 Modules activés selon la table** : *Gardiens & Éveil* (`M/R/O`), *Rêves & Sommeil* (`H/E`), *Essaim* (`I` — jetons Insectes exclusifs aux 10 tuiles des 5 lisières de `I`, absents de la boîte sans `I` ; descente sur place de l'Insecte passager au ménage, `INV-21`).
- **Accessoires `3 + 3` (`INV-20`)** : actifs dès le Tour 1 (`H` Tambour/Chant, `M` Duel `Défi ↔ Territoire tenu`, `O` Dé d'Envol/Perchoir/Plume) et progressifs via tuiles (`E` jeton d'Altération sur machine mobile max 1 : compte dans `m(r)` mais recule d'1 parcelle sans frapper ; `R` 4 jetons Écaille + Croc réutilisable + max 1 cale sous machine mobile via `G9` ; `I` Module Essaim).
- **Enracinement volontaire (`INV-22`)** : au ménage avant remise au sac, max 1 tuile construite de son Peuple/joueur/tour au pied de son rayon face à une parcelle : retourne `1` Souche (F1/unique) ou `2` (F2) en Arbre debout au décompte final (Tour 8, Sommeil ou Éveil) si la parcelle n'est pas devenue Route ; un Rêve enraciné rend le Sommeil impossible.

---

## 3. Architecture Technique & Périmètre UI (`docs/`)

```text
contracts/
├── rules_canon_v6_2.json              # SSOT règles, châssis unique, modules, 3+3, Enracinement
├── physical_and_edge_invariants.json  # Registre permanent INV-01..INV-22
├── tiles_canon_v6_2.json              # Catalogue Canon 0 (30 slots, 48 faces, 35 témoins)
├── studio_rules_guards.json           # Garde-fous lexicaux & éditoriaux
└── kernel_locks.sha256                # Empreintes SHA-256 du noyau Python (scellé jusqu'au Chantier 4)

scripts/
└── build_studio_artifacts.py          # Compilateur dérivé unique (contracts/ -> docs/data/ + data/)

docs/
├── index.html                         # SPA statique sans bundler (file:// & HTTPS), châssis verrouillé (0 écart)
├── AMAZONIA_STUDIO_CONTEXT.md         # Présent référentiel
└── data/
    ├── amazonia_data_v6_0.js          # Dérivé JS (CATALOGUE_TUILES Canon 0, CHASSIS_AXES_SPEC verrouillé, INV)
    ├── livret_v6_0.js                 # Livret joueur (refonte modulaire prévue au Chantier 2)
    ├── catalog_v6_0.json              # Miroir JSON dérivé v6.2
    └── spec_formelle_v6_0.json        # Contrat formel dérivé v6.2
```

- **Bandeau configurateur** : châssis verrouillé sur le standard unique `P4_2233` départ décalé (`Placement_Initial_Machines.defaultVal = "BULLDOZER_P1_ABATTEUSE_P2"`, `0 écart` à l'ouverture comme après `resetChassisToDefault()`, axes morts neutralisés), sélecteur de cercle `3..6` Peuples, sélecteur de bilan `digests/index.json` + copie 1-tap `📋 Copier Bilan Gemini` + export contextuel `✨ Copier contexte Gemini`.
- **4 Vues synchronisées** : `1. Livret Didactique`, `2. Explorateur (30 Profils Canon 0)`, `3. Évolutions & Arbitrages`, `4. Spec & JSON`.

---

## 4. Règles d'Or de Maintenance
1. **SSOT d'abord** : modifier `contracts/*.json` puis exécuter `uv run python scripts/build_studio_artifacts.py`.
2. **Micro-ADR en 4 questions** : obligatoire pour toute évolution de règle (voir `contracts/CORE_FREEZE_CRITERIA.md`).
3. **Tableau de conservation `INV-01..INV-22`** : obligatoire avant toute condensation/refonte du livret (`data-inv="INV-XX"`).
4. **Porte de validation** : `uv run python verify_lot.py` doit passer à **100 % vert** (linter des 30 tuiles, scanner global anti-vestiges, rendu headless Node `vm`, `ruff`, `pyright`, `pytest`, fuzzer PyPy, noyau scellé intact).
