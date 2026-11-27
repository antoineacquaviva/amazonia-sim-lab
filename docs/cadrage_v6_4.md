# Document de cadrage (`v6.4`) — Consolidation Cœur, Passe 2 des 30 Tuiles & Plan Phase B (PyPy)

**Projet :** *Amazonia : Dernier Rempart*  
**Version cible :** **`v6.4.0`** (`contracts/rules_canon_v6_4.json`, `contracts/physical_and_edge_invariants_v6_4.json`, `contracts/tiles_canon_v6_4.json`)  
**Archive de référence sanctuarisée :**
- Socle `v6.2.0` + `Canon 0` : tag Git `archive/v6.2.0-socle-canon0` et verrou `contracts/v6_2_socle_locks.sha256` (noyau PyPy verrouillé dans `contracts/kernel_locks.sha256` durant toute la Phase A).
- Panel Canonique `v6.3.1` Passe 1 & banc de montage `v6.3.2` : tag Git `archive/v6.3.2-panel-passe1` (`contracts/tiles_canon_v6_3.json` et `contracts/panels/panel_{1,2,3}.json` conservés intacts).

---

## 1. Vue d’ensemble de la bascule `v6.4` (Phase A → Phase B)

La `v6.4` consolide simultanément le **Cœur du jeu** (9 évolutions d’épuration physique, de zéro-mémoire et de fluidité sur table) et la **Passe 2 éditoriale & combinatoire** des **30 Tuiles de Synergie** bi-composant (*Mini-Tuile Plateau* + *Grande Carte Joueur*).

Tout ce qui ne figure pas parmi les 9 évolutions ci-dessous demeure **strictement identique au socle `v6.2.0`** :
- Châssis canonique unique **`P4_2233`** (`4` parcelles gravées `2–2–3–3`, dotation finie recto-verso `10 × N` pions `Arbre debout / Souche`), départ décalé (**Bulldozer en parcelle 1**, **Abatteuse en parcelle 2**).
- Abatteuse coupe tous les Arbres debout en Souches (0 Souche retirée) ; Bulldozer retourne 1 Arbre en Souche puis retire toutes les Souches (`0 Arbre / 0 Souche` = Route Forestière).
- Réglette fixe `1–6` à bandelette d’Acte réversible (`Face A` Acte 1 Tours `1–4` : `1–3` Charge / `4–6` Assaut ; `Face B` Acte 2 Tours `5–8` : `1–3` Assaut / `4–6` Charge), **double frappe (`Sur place` puis `Devant`) et `−1` au Seuil de Parade aux rangs `3` et `6` (*En avançant*)**, `Bleus Surchauffe (−1)` actifs dans tous les modes (`Charge`, `Assaut`, `Ratissage`), gain Charge plafonné à `+1` rouge max/activation sur frappe réelle non parée ni piégée.
- Ratissage physique (`+1` jeton rouge convertible en bleu, `0` bonus imprimé, immobile, parcelle comptant comme ciblée tant qu’elle n’a pas frappé), parcelles ciblées figées au début de l’activation, repli de bordure couvrant l’avancée *En avançant* (0 double bond), zéro écrasement au contact hors Route, Pièges autonomes `SINGLE_STRIKE` (max 1/parcelle ; Croc cohabite et pare en premier), Bouclier de lisière facultatif gouverné par `I`, gouvernance unitaire et clôture du temps de réflexion à `N − 1` joueurs validés.
- **4 Murs Porteurs Physiques (`M1..M4`)** et invariants `C01`, `I01..I07`, `Q01..Q02` intégralement maintenus sur les **197 assises canoniques** (`42` compositions, `64` assises/tuile, zéro contrainte `C02`).

---

## 2. Les 9 évolutions exactes du Cœur (`v6.2.0` → `v6.4.0`)

### 2.1 Oiseau épuré (`INV-07`, `INV-20`) — 2 dés universels & Perchoir de Vigie orientable
- **Suppression du 3e dé dédié et du support gradué séparé** : sous paravent fermé, **tous les joueurs** (y compris l’Oiseau) lancent uniquement leurs **2 dés standards `1–6`** (même sur Sabotage ou Écaille, jet ignoré — zéro fuite sonore).
- **Choix libre du dé chez l’Oiseau** : s’il détient un jeton Machine, l’Oiseau (`O`) choisit librement lequel de ses **2 dés** il retient comme dé de machine (au lieu du plus petit `min(D1, D2)` pour les autres Peuples) ; l’autre dé devient son **dé écarté** (pleinement lisible par `G12` *L’Ibijau*).
- **Fusion en une seule pièce mobile orientable : le *Perchoir de Vigie*** (*Chaud* à une extrémité, *Calme* à l’autre). Toujours servi en dernier à la pioche, l’Oiseau regarde jusqu’à `2` jetons du sac, en garde `1` (si possible) et pose l’autre face cachée sur son Perchoir. Sous paravents fermés, il place ou ajuste ce Perchoir (même vide en cas de pénurie) **au pied d’un rayon** ou **pointé vers un rang `1–6` de la Réglette**, le bout *Chaud* ou *Calme* orienté vers sa cible. Le Perchoir est figé irréversiblement lorsqu’il valide son 2e Défenseur sur face *Définitif*, et son jeton caché retourne au sac au ménage.

### 2.2 Duel unifié (`INV-20`)
- Toute frappe sur la parcelle du jeton **Duel** qui est **parée ou piégée par n’importe quel moyen** — Défenseur de tout Peuple, Insectes, Piège ordinaire autonome ou Croc Reptile — retourne aussitôt le Duel sur **Territoire tenu** (bloquant l’avancée `+1` aux rangs `3` et `6`).
- Seule une frappe **ni parée ni piégée** sur sa parcelle (ou la création d’une Route Forestière) renvoie le Duel en réserve Mammifère.
- *Impact tuiles* : purge des clauses d’exception devenues redondantes sur `G1`, `G13`, `R3` et `M1`.

### 2.3 Module Essaim sans étape de Migration + Amorçage & Transport natifs + Bonus 3J unifié (`INV-19`, `INV-21`)
- **Suppression complète de la sous-étape de Migration** : zéro retournement/redressement d’Insectes, zéro micro-comptabilité radiale.
- **Déploiement direct à la Production (Étape 4)** : chaque Nid défendu produit **`+1` Insecte** (`0–1` présent sur sa parcelle) ou **`+2` Insectes** (`≥ 2` présents), sans allumer d’icône ; **chaque Insecte ainsi créé est immédiatement posé au choix** :
  - sur la parcelle de **ce Nid**,
  - sur une **parcelle adjacente de son rayon** (vers la bordure ou vers le cœur, en sautant les Routes Forestières),
  - ou — **si ce Nid occupe la dernière parcelle de son rayon** — sur un **rang `1–6` de la Réglette** ou une **icône de la Piste des Gardiens** ;
  puis le pouvoir propre du Nid s’applique.
- **Amorçage natif** : si un effet de tuile demande de déplacer ou de prélever un Insecte en jeu alors qu’**aucun Insecte n’est présent sur le plateau**, prenez `1` Insecte dans la réserve de l’Essaim.
- **Déménagement unifié d’un Nid** : tout Nid déplacé par un effet de tuile (`R10`, `M3`…) emporte simultanément **tous ses Insectes, tous les Défenseurs** présents sur sa parcelle et toute éventuelle **ponte** (`G14`) glissée sous lui.
- **Bonus à 3 joueurs unifié (`INV-19`)** : dans une partie à `3` joueurs, construire **un Gardien, un Rêve ou un Nid** libère immédiatement `1` des `2` bâtisseurs vers une parcelle adjacente (sauf si les deux rayons voisins sont entièrement rasés).

### 2.4 Pied du rayon unifié : 100 % des Enracinements sur la Rive Sabotage (`INV-14`, `INV-22`)
- Les `2` rives de `2` places au pied de chaque rayon actif sont conservées (*Rive Piège* gagnée à `m(r) == 2`, *Rive Sabotage* gagnée à `m(r) == 0` ajoutant `+1` Sabotage au sac sans allumer d’icône).
- **Emplacement unique d’Enracinement** : au ménage (avant remise au sac), tout Enracinement volontaire (max `1` tuile construite de son Peuple / joueur / tour, interdit si le rayon est 100 % Routes) se pose **sur une place libre de la Rive Sabotage du rayon du joueur**. Comme chaque Peuple gouverne au plus `2` tuiles sur la partie, les `2` places suffisent toujours.
- La tuile enracinée quitte sa piste ou sa parcelle (en y laissant ses Insectes), perd son pouvoir actif hors clause **`Enraciné`**, et un Rêve enraciné ferme le Sommeil (sauf mention contraire explicite : `R1` *La Liane des Esprits*).
- **Effet Sentinelle permanent** : chaque tuile enracinée occupe en permanence **`1` des `2` places** de la Rive Sabotage de son rayon :
  - `1` tuile enracinée = **`1` seul Défenseur actif** suffit pour compléter la Rive Sabotage ;
  - `2` tuiles enracinées = Rive Sabotage **`2/2` permanente à `0` Défenseur** à chaque tour où `m(r) == 0`.
  - La *Rive Piège* exige toujours `2` Défenseurs actifs.
- **Décompte final uniquement (`M1`)** : fin de l’alignement face à une parcelle précise ; chaque tuile enracinée retourne **`1` Souche survivante** (`Face 1` / unique) ou **`2` Souches** (`Face 2`) en Arbres debout, **librement choisies parmi les parcelles survivantes de son rayon**.

### 2.5 Sabotage différé à intérêts composés (`INV-05`, `INV-15`)
- Lorsqu’un **jeton Sabotage ordinaire** est révélé à l’ouverture (hors `Écaille`, qui conserve sa règle Reptile : allume `Sabotage` + pose le `Croc` sur une parcelle ciblée), en plus de ne mobiliser aucune machine et d’allumer l’icône `Sabotage`, le joueur qui l’a pioché vise **`1` machine de son rayon ou d’un rayon voisin** :
  - si elle porte au moins `1` jeton Rouge (mobile ou en Ratissage), il la **Refroidit** (`1 Rouge → Bleu Surchauffe`) ;
  - sinon, si elle est mobile, il la fait **Reculer** d’`1` parcelle vers la bordure (en sautant les Routes).

### 2.6 Piste des Gardiens directe sans balayage + Résonance au « dernier pari » (`INV-09`, `INV-10`)
- **Zéro balayage gauche → droite, zéro reprise en arrière** : lorsqu’un événement allume son unique icône parmi `[Parade, Piégeage, Sabotage, Rêve, Insecte]`, seuls les Gardiens posés sur cette icône portant `≥ 1` pari s’activent immédiatement (`1` pari glisse en encoche).
- **Résonance (6e icône) déclenchée au « dernier pari »** : si cette vague d’activation vide le dessus d’au moins un Gardien (**dernier pari glissé en encoche** lors d’une vraie activation — exclu sur un glissement passif sans activation tel que `G4` *L’Ara rouge* Face 1 ou `G15` *Le Colibri*), l’icône **Résonance** s’allume aussitôt après, **une seule fois pour cette vague**, sans jamais boucler sur elle-même.

### 2.7 Éveil de la Forêt cumulatif en piste (`INV-10`)
- Aux Tours `1` à `7` (si au moins `1` Peuple Animal Sauvage `A ≥ 1` joue ; priorité absolue au Tour 8 ; priorité du Sommeil sur l’Éveil en cas de réalisation simultanée), l’**Éveil de la Forêt** est remporté en fin d’attaques dès que les deux conditions suivantes sont réunies :
  1. **Au moins `A + 1` Gardiens en piste sont sur leur `Face 2`** (`2/2` à `A = 1`, `3/4` à `A = 2`, `4/6` à `A = 3`) ;
  2. **Aucun pari de Gardien n’a été perdu à ce tour** (un Gardien maintenu en piste par le *Bouclier de lisière* conserve sa Face 2 pour la suite de la partie, mais son pari demeure perdu à ce tour et empêche l’Éveil à ce tour).

### 2.8 Matérialisation zéro-mémoire & Fil d’ouverture imprimé (`INV-08`, `INV-14`, `INV-15`)
- **Fil d’ouverture imprimé sur la Réglette** : `1. Altérations → 2. Sabotages & Écailles → 3. Déviations (±1) → 4. Rêves défendus (gauche → droite)`.
- **Dé retiré** : dès qu’une machine mobile est **Étouffée** ou a **terminé son attaque**, son dé quitte immédiatement la Réglette (seuls les dés encore posés sur `1–6` désignent des machines mobiles devant encore attaquer ; le jeton Machine reste devant son rayon jusqu’à la Furtivité).
- **Défenseurs couchés sur Rêve résolu** : dès qu’un Rêve défendu a terminé sa résolution à l’ouverture, couchez ses Défenseurs à plat dessus (`debout` = encore à résoudre ; `couché` = déjà résolu).

### 2.9 Lexique officiel des 6 Verbes du Cœur
Définis dans le Livret et employés de manière uniforme dans les 30 cartes :
1. **Refroidir** : retourner `1` jeton Rouge existant d’une machine (mobile ou en Ratissage) sur sa face Bleu Surchauffe (`−1` dans tous les modes ; jamais de Bleu posé à sec depuis la réserve — Mur `M2`).
2. **Altérer** : poser `1` jeton d’Altération de la réserve Entités sur une machine mobile qui n’en porte pas encore (max `1` par machine ; jamais sur Ratissage).
3. **Reculer** : déplacer une machine mobile d’`1` parcelle vers la bordure de son rayon en sautant les Routes Forestières (jamais hors plateau ni sur Ratissage).
4. **Étouffer** : neutraliser toute l’activation restante d’une machine à ce tour (jeton Machine mobile incliné à `90°` devant son rayon et **dé retiré** de la Réglette ; ou machine en Ratissage tournée à `90°` sur place jusqu’au ménage). Annuler une machine via un Rêve revient à l’Étouffer. Le mot **cale** devient **100 % exclusif** au jeton glissé sous une machine mobile par `G9` *Le Caïman noir*.
5. **Semer au sac** : glisser `1` jeton disponible (Sabotage ou Écaille) dans le sac opaque sans allumer d’icône.
6. **Glisser un Rêve** : déplacer une tuile Rêve sur la Réglette `1–6` en emportant ses Défenseurs dans leur état actuel (debout ou couchés).

---

## 3. Charte éditoriale Passe 2 & Consolidation des 30 Tuiles (`contracts/tiles_canon_v6_4.json`)

- **Mini-Tuiles Plateau (`tuile_plateau`) — Grammaire télégraphique unifiée** :
  - Zéro émoji dans `mots_cles_plateau.*` et `resume_plateau` (`2–4` codes `PIC_*` dans `pictogrammes`, incluant `PIC_TWIST` sur les 6 Twists `{G2, G7, R4, G12, R10, M3}` et `PIC_LOI_PASSIVE` sur les 3 Lois `{R7, R8, M5}`).
  - 3 opérateurs visuels uniques : `→`, `=`, `·` ou `OU` (aucun crochet `[...]`, aucun `&`, aucun `‖`, aucune ponctuation `.!?`).
  - `resume_plateau` : rôle fonctionnel clair en `4–8` mots.
  - `mots_cles_plateau.enracine` : **`null` obligatoire** sur les 26 tuiles hors rôle `ENRACINEMENT` ; rempli uniquement sur `G7, G15, R1, R2`.
  - `nom_court` : casting animalier verrouillé sur `G1..G15`, article défini systématique (`Le / La / L’`) sur `R1..R10` et `M1..M5`.
- **Grandes Cartes Joueur (`carte_joueur`)** :
  - Apostrophes typographiques `’`, suppression des guillemets autour de `pitch_ambiance`, zéro code interne (`R5`, `R8`, `M5`, `E·3`…) dans les textes joueur, épithètes en minuscules françaises sur les 15 Gardiens, Faces 2 différentielles concises, vecteurs normalisés en style fléché `Entrée → Effet → Sortie`, `paiement: []` sur `G10`.
- **Carte des rôles `v6.4`** :
  - **6 Twists `2K3`** : Triangle 1 `{G2 (R>M), G7 (M>H), R4 (H>R)}` + Triangle 2 `{G12 (O>E), R10 (E>I), M3 (I>O)}`.
  - **3 Lois passives (`Q01`)** : `{R7, R8, M5}` (étoile centrée sur `E`, max `2`/assise sur les `197` assises).
  - **13 Catalyseurs d’Éveil (`I04`)** : `G1, G3, G4, G5, G6, G8, G9, G10, G11, G12, G13, G14, G15` (`G6` *Le Toucan toco* rejoint les catalyseurs via *Cri de vapeur*, câblage conseillé `ICONE_PARADE`).
  - **6 Leviers de Rêve (`I05`)** : `G8, R1, R4, R8, R9, R10` (`4/4` lisières de `E`, `30/30` assises `E` sans `H`).
  - **4 Synergies d’Enracinement (`I06`)** : `G7, G15, R1, R2`.
  - **6 Autonomes `A = 0` (`I02`)** : `R1, R2, R6, R10, M4, M5`.

---

## 4. Feuille de route Phase B — Portage PyPy & Calibration `197` assises (après relecture Studio)

Une fois la Phase A (Jalons 1–3) relue et validée par l’auteur dans *Amazonia Doc Studio* :

### Jalon 4 — Noyau PyPy `v6.4`, Bots `B0..B2` & Calibration `Lot 0`
1. **Ouverture contrôlée du noyau déterministe PyPy (`engine/{state,primitives,core_engine}.py`)** :
   - Encodage des 9 évolutions du Cœur `v6.4` (Oiseau 2 dés + choix libre + Perchoir orientable unifié ; Duel unifié ; Essaim sans Migration à déploiement direct + amorçage + transport de Nid + bonus 3J sur Nids ; Enracinement sur Rive Sabotage avec Effet Sentinelle permanent et choix libre des Souches au décompte final ; Sabotage ordinaire différé Refroidir/Reculer ; Piste directe sans balayage + Résonance au dernier pari ; Éveil cumulatif `A + 1` Face 2 & `0` pari perdu ; fil d’ouverture `1→4` + dé retiré + pions couchés sur Rêve résolu).
   - Régénération de `contracts/core_state_api.md`, mise à niveau de la suite miroir `tests/test_invariants_mirror.py` (`INV-01..INV-22` `v6.4`) et du fuzzer PyPy (`scripts_cloud/fuzz_invariants.py`), re-scellement `contracts/kernel_locks.sha256`.
2. **Bots `B0..B2` & Calibration `Lot 0`** :
   - Alignement des agents (`bots/bot_b0.py`, `bots/belief_and_ticks.py`, `bots/heuristic_engine.py`, `bots/b2_economy.py`, `bots/b2_rollouts.py`, `bots/bot_b3_rh.py`) sur le Cœur `v6.4`.
   - Campagne de référence `Lot 0` `v6.4` (Modes 2 & 3 neutres) sur les `197` assises canoniques pour établir la ligne de base `v6.4` (difficulté, taux de Sommeil / Éveil / Tour 8, invariance `N = 3..6`).

### Jalon 5 — Encodage des 30 Tuiles `v6.4`, Témoins Exécutables & Campagne `197` Assises
1. **Catalogue stateless PyPy (`engine/effects/{gardiens,reves,nids}_v6_4.py`)** :
   - Archivage propre de `engine/effects/*_v6_2.py` vers `archive/effects_v6_2/` et implémentation 100 % stateless (`@register_tile`, AST pur, `mem_debt == 0`) des 30 tuiles de `contracts/tiles_canon_v6_4.json` (`engine_sync_status` → `ACTIVE_VERIFIED`).
   - Passage des témoins (`G1_T1..M5_T1`) en tests déterministes exécutables (`tests/test_canon_v6_4_witnesses.py`, statut `OK`).
2. **Heuristiques bots synergiques & Bascule bundle `v6.4`** :
   - Intégration des heuristiques synergiques `v6.4` dans `bots/`, bascule complète de `data/spec_bundle_v6_0.json` sur le SSOT `v6.4`.
3. **Campagne Monte-Carlo `197` assises (`Lot 0` vs `Canon v6.4`)** :
   - Tir CRN complet sur les `197` assises (`N = 3..6`, `42` compositions, paires `B1 Lot 0` vs `B2 Canon v6.4` + contrôles `B2 Lot 0` et `B3`), vérification des critères *Core Freeze* (`45–60 %` d’arbres sauvés, 3 fins vivantes, `B0 < B1 < B2 ≤ B3`, `mem_debt = 0`, `law_stack_max ≤ 2`), publication du digest dans `docs/digests/`.
