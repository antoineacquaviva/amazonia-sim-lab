# Document de cadrage (`v6.3`) — Refonte créative des 30 Tuiles de Synergie & Dédoublement Tuile / Carte

**Projet :** *Amazonia : Dernier Rempart*  
**Socle verrouillé :** Règles cœur **`v6.2.0`** (`contracts/rules_canon_v6_2.json` & `physical_and_edge_invariants.json` — intouchables)  
**Périmètre :** Conception, affinage, encodage et équilibrage d'un **panel canonique de 30 Tuiles de Synergie** (`1` par emplacement orienté `Origine>Voisin`, couvrant les `42` compositions et `197` assises). *L'écriture éventuelle de variantes B/C est hors périmètre tant que ce panel de 30 tuiles n'a pas atteint l'excellence ludique.*

---

## 1. Intention d'auteur et changement de paradigme (`v6.2` → `v6.3`)

Le travail précédent a validé un socle `v6.2` d'une grande propreté physique, mais la contrainte formelle `C02` (« 1 phrase ≤ 25 mots et ≤ 1 condition par face ») a agi comme un filtre destructeur (loi de Goodhart) : elle a éliminé les twists structurels, appauvri les synergies inter-peuples en micro-effets atomiques, et réduit les Gardiens à un organe ou un geste ponctuel plutôt qu'à un animal totem.

La `v6.3` inverse cette hiérarchie grâce à deux décisions fondatrices :
1. **Dédoublement matériel de chaque Tuile de Synergie** en une **Mini-Tuile Plateau** (ergonomie visuelle collective) et une **Grande Carte Joueur** (immersion totémique + texte de règle complet sans plafond de mots).
2. **Conception en deux passes dissociées** :
   * **Passe 1 (Sélection par la richesse)** : concevoir et retenir 30 tuiles sur des critères exclusifs d'**originalité**, de **diversité mécanique**, de **puissance synergique** (vraies briques de moteurs multi-maillons) et de **twists** modifiant les repères du cœur.
   * **Passe 2 (Affinage par la clarté)** : retravailler l'ergonomie physique et la limpidité éditoriale des 30 tuiles choisies, **sans jamais amputer l'ambition de leur effet**.

---

## 2. Architecture matérielle : le duo Mini-Tuile + Grande Carte

Conformément au principe de **gouvernance unitaire** (`v6.2`), chaque Tuile de Synergie appartient et obéit exclusivement au joueur de son Peuple d'origine. Elle est matérialisée par deux composants liés :

### 2.1 La Mini-Tuile Plateau (repère spatial à 360°)
Placée en lisière à la mise en place, puis déplacée sur la Piste des Gardiens (avec ses 2 encoches latérales de pari), la Réglette `1–6`, une parcelle de Forêt (Nid) ou au pied d'un rayon (Enracinée).
* **Contenu strictement synthétique** : Nom court de l'entité, badge de lisière orienté (`Origine>Voisin`), indicateur d'état (`Face 1` / `Face 2` / `Enraciné`), fenêtre ou icône d'activation, et **résumé visuel** composé de 2 à 4 pictogrammes et mots-clés (`resume_plateau`).
* **Zéro phrase rédigée** : aucun joueur n'a besoin de lire du texte à l'envers au centre de la table.

### 2.2 La Grande Carte Joueur (modèle Fiches Chamanes Humains)
Conservée devant le joueur du Peuple d'origine dès la mise en place (et retournée ou marquée lorsqu'elle passe en Face 2 ou s'enracine). Elle remplit deux vocations :
1. **Vocation immersive (`illustration` + `pitch_ambiance`)** :
   * **Pour les 15 Gardiens (`M`, `R`, `O`)** : le titre et l'illustration célèbrent **l'animal sauvage entier dans son biotope amazonien** (ex. *Le Jaguar*, *L'Anaconda vert*, *La Harpie féroce*, *La Matamata*, *L'Ibijau*), et non un organe ou une action isolée (*interdiction des titres du type « Le Bec du… » ou « Le Coup de queue de… »*). Un court texte d'ambiance incarne son comportement éthologique.
   * **Pour les 10 Rêves (`H`, `E`) et 5 Nids (`I`)** : même exigence d'incarnation visuelle et narrative (visions chamaniques/mythiques pour les Rêves ; architectures vivantes de la colonie pour les Nids).
2. **Vocation réglementaire (`texte_regle`)** :
   * Texte de règle **clair, structuré et complet**, sans limite a priori de nombre de mots, de phrases ou de conditions.
   * Il explicite sans zone grise : le déclencheur/fenêtre, le choix donné au gouverneur (coût, cible, embranchement), l'effet exact sur le matériel, ainsi que l'évolution `Face 1` / `Face 2` et l'éventuelle clause `Enraciné`.

---

## 3. Rappels intangibles du socle `v6.2` (Terrain de jeu des tuiles)

Toute tuile `v6.3` s'appuie exclusivement sur la physique exacte de la `v6.2` :

* **Sac opaque et Paravents muets (Étape 1)** : `2N` jetons Machine + jetons Sabotage + jusqu'à `4` Écailles. Pioche secrète d'`1` jeton (Oiseau servi dernier : regarde `2` jetons, en garde `1`, pose l'autre face cachée sur son *Perchoir de Vigie*). **Tous les joueurs lancent leurs dés sous paravent `1–6`**, même avec un Sabotage ou une Écaille (jet ignoré par défaut — *espace fertile pour des twists lisant les dés sous paravent ou écartés*).
* **Déploiement en 2 temps (Étape 2)** : `2.1` simultané face *Définitif* (forêt, ses 2 lisières constructibles, rives de Furtivité ouvertes, Rêves en jeu ; jamais sur Gardiens). `2.2` face *Réflexion* partout (dont Gardiens : `0`, `1` ou `2` Défenseurs max par Gardien) puis validation *Définitif* figeant *Duel* et *Plume de Vigie*.
* **Ouverture et Constructions (Étape 3)** : constructions obligatoires à 2 bâtisseurs (couchés en attente). Ouverture simultanée : retrait d'une éventuelle *Altération* sur machine révélée ($\rightarrow$ recul d'`1` parcelle sans frappe). Séquence stricte : `Sabotages / Écailles` un par un (+ balayage Gardiens) $\rightarrow$ `Déviations Insecte ±1` une par une (+ balayage) $\rightarrow$ `Rêves défendus` de gauche à droite (le propriétaire choisit les machines annulées y compris déviées, résout le pouvoir du Rêve, puis allume l'icône `Rêve` + balayage si $\ge 1$ machine annulée).
* **Furtivité et Essaim (Étape 4)** : Furtivité par rayon selon $m(r) =$ jetons Machine visibles du rayon (droits ou inclinés) $+$ machines en Ratissage du rayon (`m(r)=2` $\rightarrow$ Rive Piège ; `m(r)=0` $\rightarrow$ Rive Sabotage). Si `I` joue : Production des Nids défendus (`+1` si `0–1` Insecte, `+2` si `≥ 2`, sans allumer d'icône) puis Migration radiale double sens (et sortie depuis la dernière parcelle vers un rang `1–6` ou une icône Gardien).
* **Attaques et Verdict (Étape 5)** : Rangs `1` à `6` puis `Ratissage` (Abatteuse avant Bulldozer). Bandelette d'Acte retournée seule au Tour 5 (`Acte 1` : 1–3 Charge / 4–6 Assaut ; `Acte 2` : 1–3 Assaut / 4–6 Charge).
  * **Seuil de Parade** = chiffre gravé (`2–2–3–3`) $+$ `Rouges` (*Assaut* et *Ratissage* uniquement) $-$ **`Bleus Surchauffe` (actifs dans TOUS les modes : Charge, Assaut, Ratissage)** $- 1$ aux rangs `3` et `6` (min `1`).
  * **Chaîne de défense** : `Croc` puis `Piège autonome` (icône `Piégeage`, 0 pion requis) sinon Parade classique (`Défenseurs seuls` $\rightarrow$ icône `Parade` ; `avec Insectes défaussés` $\rightarrow$ icône `Insecte`).
  * **Piste des Gardiens à 6 icônes non numérotées** : `[Parade, Piégeage, Sabotage, Rêve, Insecte, Résonance]` balayées de gauche à droite après chaque action/tuile terminée (`1 événement = au plus 1 icône` ; `Résonance` en 6e position avec compteur individuel sur la 1re activation des autres Gardiens ; reprise à gauche si une icône antérieure s'allume). Verdict des paris via les 2 encoches visibles (`Bouclier de lisière` Insecte facultatif : sauve la face de la tuile mais laisse le pari perdu).
* **Ménage et Enracinement (Étape 6)** : descente sur place d'un Insecte passager non dépensé ; **Enracinement volontaire** (max `1` tuile construite/joueur/tour au pied de son rayon face à une parcelle non Route : perd son pouvoir actif hors clause *Enraciné*, rend le Sommeil impossible si Rêve, régénère `1` Souche en F1/unique ou `2` Souches en F2 au décompte final, quelle que soit la fin : Tour 8, Sommeil ou Éveil). Passage en Ratissage à `+1` Rouge physique (parcelle comptant comme ciblée).
* **Accessoires `3 + 3`** :
  * *Actifs T1* : **Humains** (`1 Tambour` posable en `2.1` chez tout allié + `1 Chant` avançant un Rêve d'1 rang à gauche s'il annule la dernière machine du rang) ; **Mammifères** (`1 jeton Duel` *Défi* $\leftrightarrow$ *Territoire tenu* bloquant l'avancée `+1`) ; **Oiseaux** (`Dé d'Envol 1–6`, `Perchoir de Vigie`, `Plume de Vigie` *Chaud/Calme*).
  * *Progressifs via tuiles* : **Entités** (`jetons Altération` sur machine mobile, max 1) ; **Reptiles** (`4 jetons Écaille`, `1 Croc` réutilisable, `max 1 cale` sous machine mobile) ; **Insectes** (`jetons Insectes` et `Nids` strictement réservés aux 10 tuiles des 5 lisières de `I`).
  * *Spécialisation par Grande Carte* : une Grande Carte `E` ou `R` peut enrichir ou détourner l'effet du jeton *Altération*, *Écaille*, *Croc* ou d'une *cale* lorsqu'il se résout, tant que le support physique sur le plateau reste sans ambiguïté (`mem_debt = 0`).

### 3.2 Les 4 Murs Porteurs Physiques (`M1` à `M4` — bloquants dans `audit_197.py`)

Suite au retour d'expérience des 3 premiers panels candidats (`panel_1`, `panel_2`, `panel_3`), quatre invariants physiques intangibles bornent toute conception `v6.3` :

1. **Unité de temps de la bataille (`M1_TEMPS_BATAILLE`)** : interdiction stricte de retourner une `Souche` en `Arbre debout` pendant les Tours `1` à `8` (ni à l'activation, ni à l'ouverture, ni à la production, ni au ménage, ni au moment de la pose d'un Enracinement). Toute régénération `Souche → Arbre debout` se résout **exclusivement au décompte final** (via la règle d'Enracinement volontaire et les clauses `enracine` explicitement lues *au décompte final*). *Lire la présence d'un Arbre debout comme condition spatiale (ex. pont de canopée) reste 100 % valide.*
2. **Conservation thermique (`M2_CONSERVATION_THERMIQUE`)** : aucun jeton Bleu *Surchauffe* ne peut être posé à sec depuis la réserve sur une machine dépourvue de jeton Rouge. Un Bleu provient toujours du retournement (sur place ou transféré d'une machine à une autre) d'un jeton Rouge déjà présent sur une machine (ou d'une loi modifiant la lecture d'un Rouge existant dans le Seuil).
3. **Intégrité `2–2–3–3` et fixité d'icône (`M3_INTEGRITE_PLATEAU_ET_ICONES`)** :
   * Les pions `Arbre / Souche` ne changent jamais de parcelle (respect strict de la dotation gravée `2–2–3–3`) et aucune tuile ne coupe volontairement un Arbre debout allié en Souche comme coût.
   * Une Mini-Tuile Gardien en piste ne saute pas d'une icône à une autre lors de son activation (**au plus `1` seul emplacement Twist sur `30`** dans tout un panel peut, s'il le souhaite, faire exception comme Twist dédié ; jamais en mécanique générique répétée ni sur une tuile fluide).
4. **Autonomie plancher en solo (`M4_AUTONOMIE_PLANCHER_SOLO`)** : toute tuile construite seule doit avoir un effet utile garanti dès sa `Face 1` sans dépendre de la construction préalable d'une autre tuile — **pas même sa jumelle de lisière `Y>X`** (qui peut ne pas être construite, retomber en lisière ou être enracinée).
   * Une tuile ne peut donc pas exiger comme prérequis bloquant (`entrees_plancher`) un état créé exclusivement par d'autres tuiles (`BLEU`, `CALE`, `INSECTE_PASSAGER`, ni `ALTEREE`/`ALTERATION` hors origine `E`, ni `ECAILLE`/`CROC` hors origine `R` — sauf si la tuile précise explicitement qu'elle prélève elle-même ce jeton dans la réserve physique du voisin présent sur sa lisière).
   * En revanche, ces états inter-tuiles restent pleinement encouragés comme **alternatives (`OU`)** ou **amplificateurs / synergies optionnelles (`Si…` / `Face 2`)**, déclarés dans `entrees_synergie`.

---

## 4. Casting verrouillé des 15 Gardiens (Figures animales)

Chaque emplacement Gardien incarne un unique animal emblématique d'Amazonie :
* **Mammifères (`M`)** : `G1 (M>R)` **Le Jaguar** · `G3 (M>O)` **L'Atèle** · `G7 (M>H)` **Le Tapir** · `G8 (M>E)` **Le Boto** · `G13 (M>I)` **Le Tamanoir**
* **Reptiles (`R`)** : `G2 (R>M)` **L'Anaconda vert** · `G5 (R>O)` **L'Iguane vert** · `G9 (R>H)` **Le Caïman noir** · `G10 (R>E)` **La Matamata** · `G14 (R>I)` **Le Téju**
* **Oiseaux (`O`)** : `G4 (O>M)` **L'Ara rouge** · `G6 (O>R)` **Le Toucan toco** · `G11 (O>H)` **La Harpie féroce** · `G12 (O>E)` **L'Ibijau** · `G15 (O>I)` **Le Colibri**

---

## 5. Critères de conception en 2 temps et Invariants structurels

### 5.1 Temps 1 — Critères de création et de sélection du Panel 30
1. **Vraies briques de moteurs inter-peuples** : chaque tuile crée des ponts francs entre la grammaire de son Peuple d'origine et celle de son voisin de lisière (recycler des bâtisseurs/rives perdantes, sculpter la frontière Charge/Assaut, retourner ou consommer la *Surchauffe bleue*, transformer les Souches/Clairières/Routes/Ratissages en leviers tactiques, nourrir ou projeter l'Essaim, orchestrer les cascades des 6 icônes).
2. **Focalisation mécanique (anti-couteau suisse)** : privilégier **une mécanique signature forte, lisible et mémorable par tuile** plutôt qu'un empilement de 3–4 micro-effets disjoints. La liberté rédactionnelle de la Grande Carte (`I07`) sert à expliquer clairement une mécanique profonde (son coût, son dilemme, sa synergie et ses cas limites), jamais à diluer l'identité d'une tuile dans une liste hétéroclite de bonus.
3. **Twists assumés et effets signature** : au moins `6` Briques-Twists distribuées en $2K_3$ (`1` par Peuple d'origine, au plus `1` par lisière) viennent tordre une règle familière du cœur (lecture d'un dé écarté ou sous paravent, phorésie sur machine, archipel de Souches, piston de Rêves, déménagement de Nid ou d'ancrage, torsion de l'ordre d'attaque, sacrifice de Souche ou de Piège). Les `24` autres briques, dites fluides, doivent elles aussi posséder une forte personnalité ludique (zéro simple « distributeur passif de +1 jeton » sans dilemme).
4. **Dilemme tactique réel** : chaque activation ou positionnement confronte le gouverneur à un renoncement concret (tempo vs masse critique, verrou local vs dilution du sac, pouvoir actif vs Enracinement, Sommeil vs Éveil).

### 5.2 Temps 2 — Critères d'affinage et d'hygiène (sans appauvrissement)
* **Dette mémorielle nulle (`mem_debt = 0`)** : interdiction de tout modificateur flottant non porté par une pièce physique (pion, jeton, cale, orientation ou emplacement de tuile).
* **Économie de manipulation** : pas de micro-comptabilité à chaque sous-étape ; respect strict du plafond de **$\le 5$ vraies lois passives permanentes** dans le panel de 30 tuiles (placées de sorte qu'aucune des 197 assises n'en reçoive plus de `2`).
* **Clarté éditoriale** : vocabulaire unifié `v6.2` sur la Grande Carte ; synthèse visuelle immédiate sur la Mini-Tuile.

### 5.3 Invariants mathématiques maintenus sur les 197 assises (`audit_197`)
* **`M1` à `M4` (4 Murs Porteurs Physiques)** : unité de temps de la bataille (`M1`), conservation thermique (`M2`), intégrité `2–2–3–3` & fixité d'icône `≤ 1` Twist (`M3`), et autonomie plancher en solo dès la `Face 1` (`M4`).
* **`I01` Clôture de disponibilité & séparation plancher / synergie** :
  * **Plancher bloquant (`entrees_plancher`, contrôlé par `M4`)** : ne peut exiger qu'un état garanti en solo par le socle, le Peuple d'origine, le voisin de lisière (accessoires T1 ou prélèvement explicite dans la réserve du voisin) ou la tuile elle-même — jamais une dépendance bloquante à la construction d'une autre tuile, pas même sa jumelle `Y>X`.
  * **Synergies optionnelles (`entrees_synergie`, alternatives `OU` / bonus `Si…` / `Face 2`)** : doivent rester disponibles sur les `64` assises (via le socle, les Peuples assis, la tuile elle-même ou sa jumelle `Y>X` co-présente à 100 %) et respecter l'exclusivité stricte des Insectes aux 10 tuiles des 5 lisières de `I`.
* **`I02` Autonomie `A = 0` sur `{H, E, I}`** : `R1, R2, R6, R10, M4, M5` ne dépendent jamais d'un Gardien ni de la Piste des Gardiens.
* **`I03` Divergence de lisière** : `X>Y` et `Y>X` produisent des sorties principales distinctes et ne forment jamais une boucle infinie fermée à deux.
* **`I04` Couverture Éveil `(i) + (ii)`** : pour chaque Animal (`M, R, O`), au moins 2 de ses 3 Gardiens tournés vers `{H, E, I}` et au moins 1 Gardien sur chaque lisière Animal–Animal (`M–R`, `M–O`, `R–O`) portent un catalyseur d'ouverture/sécurisation de pari (`≥ 9` Gardiens, et 100 % des 15 Gardiens rentables en double activation).
* **`I05` Couverture Sommeil (`E` sans `H`)** : au moins 3 des 4 lisières `E–M, E–R, E–O, E–I` offrent un levier de mouvement de Rêve (couvrant les 30 assises où `E` joue sans `H`).
* **`I06` Synergies d'Enracinement** : `3` à `5` tuiles du panel bonifient, déclenchent un coup d'éclat ou protègent l'Enracinement volontaire.
* **`I07` Zéro contrainte de comptage de mots** : l'ancienne porte `C02` (≤ 25 mots / 1 phrase / ≤ 1 condition) est définitivement supprimée des contrats et des scripts de vérification.

---

## 6. Contrat de données cible d'une Tuile (`v6.3.1`) & Staging Multi-Panels

### 6.1 Structure d'une entrée de catalogue (`contracts/tiles_canon_v6_3.schema.json`)
Chaque entrée de `contracts/tiles_canon_v6_3.json` (et des panels candidats `contracts/panels/panel_*.json`) distinguera clairement :
1. **Identité & Rôle** : `id` (`G1`), `alias_oriente` (`M>R`), `famille`, `origine`, `voisin`, `roles_portes`, `est_twist`, `vecteurs`, `entrees_plancher` (prérequis bloquants solo `M4`), `entrees_synergie` (synergies optionnelles `OU` / `Si…` / `Face 2`), `entrees` (union complète rétro-compatible), `sorties`, `paiement`, `nature` (`ACTION` | `LOI_PASSIVE`).
2. **`tuile_plateau` (Mini-Tuile)** : `nom_court` (ex. `"Le Jaguar"`), `fenetre_badge`, `icone_conseillee`, `pictogrammes` (liste normalisée), `mots_cles_plateau` (aide-mémoire ultra-court par face/état), `resume_plateau`.
3. **`carte_joueur` (Grande Carte)** : `titre_complet`, `entite_illustree` (animal sauvage / vision / nid), `brief_illustration`, `pitch_ambiance`, `texte_regle` (structuré par `face_1`, `face_2` optionnelle, `enracine` optionnel), `decision_et_renoncement`.
4. **Exécution & Preuve** : `temoins` (1 à 3 tests unitaires exécutables), `heuristique_bot`, `engine_sync_status`, `statut_conception`.

### 6.2 Accueil et comparaison parallèle des 3 panels candidats (`contracts/panels/`)
Les 3 catalogues indépendants issus de nos 3 modèles sont conservés en parallèle dans `contracts/panels/` (`panel_1.json`, `panel_2.json`, `panel_3.json`) avant assemblage du panel retenu dans `contracts/tiles_canon_v6_3.json` :
* Validation unitaire d'un panel : `uv run python scripts/audit_197.py contracts/panels/panel_1.json`
* Audit comparatif des 3 panels côte à côte : `uv run python scripts/audit_197.py --panels-dir contracts/panels`

