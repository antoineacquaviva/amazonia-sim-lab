# AMAZONIA DOC STUDIO — Référentiel Fonctionnel & Technique (`v6.4` SSOT)

> **Usage IA (Pièce Jointe de Prompt)** : Ce document décrit l'architecture SSOT `v6.4`, les 9 évolutions Cœur, le lexique officiel des 6 Verbes du Cœur, la Passe 2 consolidée des 30 tuiles et les garde-fous automatiques d'**Amazonia Doc Studio**. Toute modification proposée par une IA doit éditer les contrats de `contracts/`, exécuter `uv run python scripts/build_studio_artifacts.py` et passer `uv run python verify_lot.py` à 100 % au vert.

---

## 1. Identité & Rôle dans l'Écosystème

- **Projet** : *Amazonia : Dernier Rempart* — Jeu de société coopératif asymétrique à communication muette (`3` à `6` joueurs, `8` tours max en `2` Actes).
- **Socle éditorial & tuiles actif** : **`v6.4` (`schema_version: "6.4.0"`)** — *Consolidation Cœur (9 évolutions) + 6 Verbes du Cœur + Passe 2 des 30 Tuiles* (voir `docs/cadrage_v6_4.md` et `docs/panel_canon_v6_4.md`).
- **Archives & Noyau PyPy sanctuarisés (Phase A)** :
  - Tag Git immuable `archive/v6.3.2-panel-passe1` posé avant la migration `v6.4`.
  - Le noyau PyPy `v6.2` (`contracts/kernel_locks.sha256`, `contracts/v6_2_socle_locks.sha256`, `engine/`, `contracts/rules_canon_v6_2.json`, `contracts/physical_and_edge_invariants.json`, `contracts/tiles_canon_v6_2.json`, `contracts/tiles_canon_v6_3.json`, `contracts/panels/panel_{1,2,3}.json`) demeure 100 % intact jusqu'au lancement de la Phase B (Jalons 4 & 5 PyPy `v6.4`).
- **Dépôt & Hébergement** :
  - GitHub : `https://github.com/antoineacquaviva/amazonia-sim-lab` (`docs/`)
  - Production (GitHub Pages) : `https://antoineacquaviva.github.io/amazonia-sim-lab/`
- **Architecture Source Unique de Vérité (SSOT `v6.4`)** :
  1. `contracts/rules_canon_v6_4.json` : contrat formel typé du Cœur `v6.4` (châssis unique verrouillé `P4_2233` départ décalé `Bulldozer p=1 / Abatteuse p=2`, 9 évolutions Cœur, lexique des 6 Verbes du Cœur, matériel fini recto-verso, sac opaque, supports fixes, formule de Seuil, 6 icônes Gardiens directes, séquence du tour, 3 modules, accessoires `3 + 3`, Enracinement Sentinelle sur Rive Sabotage).
  2. `contracts/physical_and_edge_invariants_v6_4.json` : registre permanent des **22 invariants** (`INV-01` à `INV-22`, catégories `MATERIEL`, `CAS_LIMITE`, `GOUVERNANCE`) avec assertions vérifiables dans le livret joueur (`data-inv="INV-XX"`).
  3. `contracts/tiles_canon_v6_4.json` & `contracts/tiles_canon_v6_4.schema.json` : catalogue Canon `v6.4` consolidé Passe 2 (`30` emplacements bi-composants `tuile_plateau` + `carte_joueur`, `31` pictogrammes unifiés, `0` erreur de schéma strict et `197` assises `OK` sous `scripts/audit_197.py`).
  4. `contracts/tiles_canon_v6_3.json`, `contracts/panels/panel_{1,2,3}.json` & `contracts/tiles_canon_v6_2.json` : archives consultables en lecture seule dans l'Explorateur (`Archive v6.3 (Passe 1)`, `Archive v6.2` et `Archives Duel P1·P2·P3`).
  5. **Compilateur dérivé unique** (`scripts/build_studio_artifacts.py`) : génère sans aucune constante métier codée en dur les fichiers dérivés `v6.4` (`docs/data/canon_v6_4_data.js`, `docs/data/catalog_v6_4.json`, `docs/data/spec_formelle_v6_4.json`) ainsi que la couche archive/runtime `v6.2` (`docs/data/amazonia_data_v6_0.js`, `catalog_v6_0.json`, `spec_formelle_v6_0.json`, `panels_v6_3_data.js`, `data/spec_bundle_v6_0.json` et `data/studio_lock.json`).

---

## 2. Les 9 Évolutions du Cœur & 22 Invariants (`v6.4` — `INV-01` à `INV-22`)

### 2.1. Matériel fini, réversible et auto-vérifiant
- **Arbres / Souches (`INV-01`)** : dotation finie exacte de `10 × N` pions uniques recto-verso (`Arbre debout` / `Souche`, zéro réserve illimitée). L'Abatteuse retourne tous les Arbres debout en Souche sans toucher aux Souches ; le Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches ; la repousse finale par Enracinement retourne des Souches survivantes en Arbres debout au décompte final uniquement.
- **Jetons Puissance (`INV-02`)** : pièces recto-verso `Rouge (+1)` / `Bleu Surchauffe (−1)`. **Refroidir** = retourner 1 Rouge existant sur sa face Bleu Surchauffe (jamais de Bleu posé à sec).
- **Défenseurs (`INV-03`, `INV-04`)** : modèle unique de 2 pions recto-verso (`Réflexion` / `Définitif`) par joueur. 1er pion posé directement face `Définitif` (jamais sur les Gardiens) ; 2e pion posé face `Réflexion` puis retourné irréversiblement sur `Définitif` (figeant simultanément le jeton Duel ou le Perchoir de Vigie). Clôture à `N−1` joueurs validés (au plus 1 ultime ajustement). Chez les Humains (`H`) : uniquement 2 pions Chamanes (`1 Tambour` et `1 Chant` recto-verso).

### 2.2. Sac opaque, Sabotage différé & Oiseau épuré
- **Sac opaque & Sabotage différé (`INV-05`, `INV-06`)** : sac contenant `2N` jetons Machine épais, jetons Sabotage ordinaires et jusqu'à `4` jetons Sabotage `Écaille` (tuiles `R`). Les jetons non piochés restent cachés. Lorsqu'un **Sabotage ordinaire** est révélé à l'ouverture (hors Écaille), il allume `Sabotage` et son porteur vise `1` machine de son rayon ou d'un rayon voisin : s'il y a au moins `1` Rouge (mobile ou Ratissage), il la **Refroidit** ; sinon, si elle est mobile, il la fait **Reculer** d'`1` parcelle vers la bordure. En pénurie, distribution horaire depuis le Coordonnateur, **Oiseau toujours servi en dernier**.
- **Oiseau épuré (`INV-07`, `INV-20`)** : tous les joueurs lancent uniquement leurs **2 dés standards `1–6`** sous paravent fermé (même sur Sabotage ou Écaille, jet ignoré). Sur un jeton Machine, **l'Oiseau (`O`) choisit librement lequel de ses 2 dés il retient** (l'autre est son dé écarté). Une seule pièce mobile orientable — le **Perchoir de Vigie** (*Chaud* ↔ *Calme*) — porte face cachée le 2e jeton regardé au sac et se place sous paravents fermés au pied d'un rayon ou pointé vers un rang `1–6` (figé à la validation finale).

### 2.3. Supports fixes, Piste des Gardiens directe & Éveil cumulatif
- **Réglette fixe `1–6`, fil d'ouverture imprimé & zéro mémoire (`INV-08`, `INV-15`)** : bandelette d'Acte réversible retournée seule au début du Tour 5 sans déplacer ni Rêves ni Insectes. Fil d'ouverture imprimé : `1. Altérations → 2. Sabotages & Écailles → 3. Déviations ±1 → 4. Rêves défendus (de gauche à droite)`. Dès qu'une machine mobile est **Étouffée** ou a terminé son attaque, son **dé est immédiatement retiré** de la Réglette ; dès qu'un Rêve défendu est résolu, ses **Défenseurs sont couchés à plat dessus** (et se déplacent toujours avec lui lors des glissements).
- **Piste des Gardiens directe à 6 icônes & Résonance au dernier pari (`INV-09`)** : `[Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance]` sans balayage séquentiel ni retour en arrière. Seuls les Gardiens posés sur l'unique icône allumée par l'événement s'activent directement. Si cette activation vide le dessus d'au moins un Gardien (**dernier pari glissé en encoche** lors d'une vraie activation ; exclu sur glissement passif), l'icône **Résonance** s'allume aussitôt une seule fois pour cette vague sans boucler sur elle-même.
- **Encoches visibles & Éveil cumulatif en piste (`INV-10`)** : 2 encoches latérales visibles par Gardien. Aux Tours `1` à `7` (`A ≥ 1`, priorité absolue au Tour 8), l'**Éveil de la Forêt** est remporté en fin d'attaques dès qu'au moins **`A + 1` Gardiens en piste sont sur leur `Face 2`** (`2/2` à `A=1`, `3/4` à `A=2`, `4/6` à `A=3`) **ET qu'aucun pari de Gardien n'a été perdu à ce tour** (un Gardien maintenu par *Bouclier de lisière* garde sa Face 2 pour la suite mais son pari reste perdu à ce tour).

### 2.4. Seuil, Ratissage, Duel unifié, Essaim direct & Enracinement Sentinelle
- **Seuil unifié & Ratissage physique (`INV-11`, `INV-12`, `INV-13`)** : Seuil = gravé + rouges (Assaut/Ratissage uniquement ; ignorés en Charge) − bleus Surchauffe (actifs en tous modes) − `1` aux rangs `3` et `6`, min `1`. Ratissage = jeton Machine glissé dessous hors sac + `+1` rouge physique (convertible en bleu), immobile, parcelle ciblée, tourné à `90°` si Étouffé. Cibles figées au début de l'activation ; poussée de bordure couvrant l'avancée de *En avançant*.
- **Duel unifié (`INV-20`)** : toute frappe sur la parcelle du jeton **Duel** qui est **parée ou piégée par n'importe quel moyen** (Défenseur de tout Peuple, Insectes, Piège ordinaire ou Croc) retourne le Duel sur **Territoire tenu**. Seule une frappe ni parée ni piégée le renvoie en réserve.
- **Module Essaim direct & Bonus 3J unifié (`INV-18`, `INV-19`, `INV-21`)** : les jetons Insectes sont exclusifs aux 10 tuiles des 5 lisières de `I` et restent dans la boîte sans `I`. **Déploiement direct à la Production** (`+1` si `0–1` présent, `+2` si `≥ 2`, immédiatement posés sur ce Nid, parcelle adjacente en sautant les Routes, ou pistes centrales depuis la dernière parcelle), **Amorçage natif** (prélève `1` Insecte en réserve si un effet de tuile déplace/prélève un Insecte alors qu'il y en a `0` en jeu), **Déménagement unifié d'un Nid** (emporte simultanément tous ses Insectes, tous ses Défenseurs et sa ponte), Bouclier de lisière facultatif gouverné par `I`, et **bonus à 3 joueurs étendu aux Gardiens, Rêves et Nids**.
- **Enracinement Sentinelle sur Rive Sabotage (`INV-14`, `INV-22`)** : au ménage avant remise au sac, max `1` tuile construite/joueur/tour sur une place libre de la **Rive Sabotage** de son rayon (interdit si rayon 100 % Routes). **Effet Sentinelle permanent** : chaque tuile enracinée occupe en permanence `1` des `2` places de cette Rive Sabotage (`1` tuile = `1` seul Défenseur actif requis ; `2` tuiles = `2/2` permanent à `0` Défenseur quand `m(r) = 0`). Au décompte final uniquement, retourne `1` Souche (`Face 1`/unique) ou `2` Souches (`Face 2`) en Arbres debout, **librement choisies parmi les parcelles survivantes de son rayon**.
- **Lexique officiel des 6 Verbes du Cœur** : **Refroidir**, **Altérer**, **Reculer**, **Étouffer** (le mot *cale* étant 100 % exclusif au Caïman noir), **Semer au sac**, **Glisser un Rêve**.

---

## 3. Architecture Technique & Périmètre UI (`docs/`)

```text
contracts/
├── rules_canon_v6_4.json                  # SSOT Cœur v6.4 (9 évolutions, 6 Verbes, modules, 3+3, Enracinement)
├── physical_and_edge_invariants_v6_4.json # Registre permanent INV-01..INV-22 v6.4
├── tiles_canon_v6_4.json                  # Catalogue Canon v6.4 Passe 2 (30 tuiles, 31 pictos, 197 assises OK)
├── tiles_canon_v6_4.schema.json           # Schéma JSON strict v6.4
├── studio_rules_guards.json               # Garde-fous lexicaux, anti-vestiges & termes retirés v6.4
├── rules_canon_v6_2.json                  # Archive & runtime PyPy v6.2 (sanctuarisé jusqu'au Jalon 4)
├── tiles_canon_v6_3.json                  # Archive Passe 1 v6.3 (lecture seule)
├── panels/panel_{1,2,3}.json              # Archives Duel P1·P2·P3 (lecture seule)
├── kernel_locks.sha256                    # Empreintes SHA-256 noyau PyPy (intact Phase A)
└── v6_2_socle_locks.sha256                # Empreintes SHA-256 socle v6.2 (intact Phase A)

scripts/
├── build_canon_v6_4.py                    # Constructeur déterministe Passe 2 (tiles_canon_v6_4.json + panel_canon_v6_4.md)
├── build_studio_artifacts.py              # Compilateur dérivé unique (contracts/ -> docs/data/ + data/)
├── tiles_v6_3_schema.py                   # Validateur strict v6.3 & v6.4
└── audit_197.py                           # Auditeur mathématique 197 assises (M1..M4, C01, I01..I07, Q01..Q02)

docs/
├── index.html                             # SPA statique sans bundler (file:// & HTTPS), châssis verrouillé v6.4
├── explorer_v6_3.js                       # Explorateur Bi-Composant v6.4.0 (ouverture Canon v6.4 + Simulateur + Archives)
├── explorer_v6_3.css                      # Design system Canon v6.4 / Simulateur / Tiroirs / Archives Duel
├── cadrage_v6_4.md                        # Spécification complète v6.4 & feuille de route Phase B (Jalons 4 & 5)
├── panel_canon_v6_4.md                    # Livre de référence lisible des 30 tuiles Passe 2
├── AMAZONIA_STUDIO_CONTEXT.md             # Présent référentiel
└── data/
    ├── canon_v6_4_data.js                 # Dérivé JS v6.4 (6 Verbes, Cœur, 22 INV, 31 pictos, Canon 30 + Archive v6.3)
    ├── catalog_v6_4.json                  # Miroir JSON dérivé v6.4
    ├── spec_formelle_v6_4.json            # Contrat formel dérivé v6.4
    ├── livret_v6_0.js                     # Livret joueur modulaire v6.4 (LIVRET_SCHEMA_VERSION = "6.4.0", INV-01..22)
    ├── amazonia_data_v6_0.js              # Dérivé JS (VERSION_CHANGELOG[0] = v6.4, Archive v6.2, CHASSIS verrouillé)
    ├── panels_v6_3_data.js                # Dérivé JS Archives Duel P1·P2·P3
    ├── catalog_v6_0.json                  # Miroir JSON archive v6.2
    └── spec_formelle_v6_0.json            # Contrat formel archive v6.2
```

- **4 Vues synchronisées** : `1. Livret Didactique` (`v6.4`, 6 Verbes du Cœur, 22 `data-inv`, filtrage dynamique par table `3..6J`), `2. Explorateur & Canon v6.4` (ouverture par défaut sur les 30 tuiles `Canon v6.4 (Affiné)` avec Radar 197 **`✅ Équilibre OK`**, annotations live `🤔 À revoir` + `Note`, édition locale & export `tiles_canon_v6_4.json`, Simulateur de Table `3..6J` sur `Canon v6.4`, et accès lecture seule `Archive v6.3 (Passe 1)`, `Archive v6.2` et `Archives Duel P1·P2·P3`), `3. Évolutions & Arbitrages` (`v6.4` en tête), `4. Spec & JSON` (manifeste `6.4.0` + 6 Verbes du Cœur).

---

## 4. Règles d'Or de Maintenance & Phase B
1. **SSOT d'abord** : modifier `contracts/*_v6_4.json` puis exécuter `uv run python scripts/build_studio_artifacts.py`.
2. **Tableau de conservation `INV-01..INV-22`** : obligatoire avant toute condensation/refonte du livret (`data-inv="INV-XX"`).
3. **Porte de validation** : `uv run python verify_lot.py` doit passer à **`10/10` portes vertes** (SHA-256 noyau/socle, AST, zéro API LLM, cohérence Studio `v6.2` & `v6.4`, linter & audit `197` assises `v6.2`/`v6.3`/`v6.4`, scanner anti-vestiges & termes retirés `v6.4`, `ruff`, `pyright`, `pytest`, fuzzer PyPy).
4. **Phase B (à lancer après relecture auteur dans le Studio)** : Jalon 4 (Noyau PyPy `v6.4` + Bots `B0..B2` + calibration `Lot 0`) puis Jalon 5 (Encodage des 30 tuiles `v6.4` + témoins exécutables + campagne `197` assises).
