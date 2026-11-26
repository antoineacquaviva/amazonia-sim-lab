# Panel Canonique `v6.3.1` — Passe 1 Assemblée (Support de travail Étape 3)

*Source contractuelle : `contracts/tiles_canon_v6_3.json` (`schema_version = 6.3.1`, `etape_active = ETAPE_3_AFFINAGE_EDITORIAL`, généré le `2026-11-26`). Validé à **100 % (`0 erreur`)** par `scripts/tiles_v6_3_schema.py` et `scripts/audit_197.py` sans `--allow-draft`.*

---

## 1. Synthèse de l’assemblage & Santé sur les `197` assises

### 1.1 Provenance des 30 emplacements retenus

| Source archivée (`contracts/panels/`) | Effectif | Emplacements extraits | Ajustement appliqué |
|---|---:|---|---|
| `panel_1.json` | **22** | `G1`, `G2`, `G4`, `G5`, `G6`, `G7`, `G8`, `G9`, `G12`, `G13`, `G14`, `G15`, `R1`, `R3`, `R4`, `R6`, `R7`, `R9`, `M1`, `M2`, `M3`, `M4` | Extraction verbatim |
| `panel_2.json` | **4** | `G3`, `G11`, `R2`, `R5` | `G3` (*L’Atèle*) reclassé hors-twist (`est_twist=false`, `TWIST_2K3` retiré, `CATALYSEUR_EVEIL` conservé) |
| `panel_3.json` | **4** | `G10`, `R8`, `R10`, `M5` | Extraction verbatim |

### 1.2 Tableau de bord `audit_197` (`197` assises · `42` compositions · `64` assises/tuile)

| Contrôle | Verdict | Détail mesuré |
|---|---|---|
| **Murs Porteurs `M1..M4`** | **OK** | `M1`=OK · `M2`=OK · `M3`=OK · `M4`=OK |
| **Dette mémorielle (`C01`) & Zéro `C02` (`I07`)** | **OK** | `0` modificateur flottant, `0` code d’étape, `0` terme obsolète, `c02_word_count_purged=true` |
| **Clôture `I01` & Synergies optionnelles** | **OK** | `0` violation Insectes / plancher ; **34** synergies optionnelles couvertes à `64/64` assises |
| **Autonomie `A=0` (`I02`)** | **OK** | `6/6` tuiles `M4, M5, R1, R10, R2, R6` sans dépendance Gardien |
| **Divergence des 15 lisières (`I03`)** | **OK** | `15/15` lisières divergentes en sortie principale, `0` boucle fermée à 2 états |
| **Couverture Éveil (`I04`)** | **OK** | **12** catalyseurs (`M`: 2, `R`: 3, `O`: 3 vers `{H,E,I}` ; `3/3` lisières Animal–Animal ; `0` assise `A≥1` découverte) |
| **Couverture Sommeil (`I05`)** | **OK** | **6** leviers (`G8, R1, R10, R4, R8, R9`) · `4/4` lisières de `E` couvertes (`E–M, E–R, E–O, E–I`) · `0/30` assise `(E sans H)` découverte |
| **Enracinements (`I06`)** | **OK** | **4** synergies (`G15, G7, R1, R2`, cible `3–5`) |
| **Lois passives (`Q01`)** | **OK** | **3/5** (`M5, R7, R8`) — étoile centrée sur `E`, max **2**/assise (`0` sur 53, `1` sur 96, `2` sur 48) |
| **Twists `2K3` (`Q02`)** | **OK** | **6** twists exacts : Triangle 1 `R>M (G2) → M>H (G7) → H>R (R4)` + Triangle 2 `O>E (G12) → E>I (R10) → I>O (M3)` |
| **Schéma bi-composant & Casting (`V63`)** | **OK** | `30/30` emplacements stricts, `15/15` Gardiens verrouillés, `0` phrase sur Mini-Tuile |

### 1.3 Carte des rôles consolidée

- **⚡ Twists `2K3` (6)** : `G2=R>M`, `G7=M>H`, `G12=O>E`, `R4=H>R`, `R10=E>I`, `M3=I>O`
- **⚖️ Lois passives (3)** : `R7=E>M`, `R8=E>R`, `M5=I>E`
- **⭐ Catalyseurs d’Éveil (12)** : `G1=M>R`, `G3=M>O`, `G4=O>M`, `G5=R>O`, `G8=M>E`, `G9=R>H`, `G10=R>E`, `G11=O>H`, `G12=O>E`, `G13=M>I`, `G14=R>I`, `G15=O>I`
- **🌙 Leviers de Rêve (6)** : `G8=M>E`, `R1=H>E`, `R4=H>R`, `R8=E>R`, `R9=E>O`, `R10=E>I`
- **🌱 Synergies d’Enracinement (4)** : `G7=M>H`, `G15=O>I`, `R1=H>E`, `R2=E>H`
- **🔓 Autonomie `A=0` (6)** : `R1=H>E`, `R2=E>H`, `R6=H>I`, `R10=E>I`, `M4=I>H`, `M5=I>E`

### 1.4 Vue synoptique des 15 frontières (`X ↔ Y`) et divergence `I03`

| Frontière | `X>Y` (Source) | Sortie principale `X>Y` | `Y>X` (Source) | Sortie principale `Y>X` | Divergence `I03` |
|---|---|---|---|---|---|
| [`M ↔ R`](#frontiere-m-r-g1-g2) | **`G1`** Le Jaguar, seigneur des berges (`panel_1`) | `CROC_POSTE` | **`G2`** L’Anaconda vert, l’étau des eaux dormantes (`panel_1`) | `RATISSAGE_ROMPU` | ✅ Divergent · 0 boucle |
| [`M ↔ O`](#frontiere-m-o-g3-g4) *(hybride)* | **`G3`** L’Atèle (`panel_2`) | `DEFENSEUR_REDEPLOYE` | **`G4`** L’Ara rouge, sentinelle de la collpa (`panel_1`) | `PARI_GLISSE` | ✅ Divergent · 0 boucle |
| [`R ↔ O`](#frontiere-r-o-g5-g6) | **`G5`** L’Iguane vert, dormeur des hautes branches (`panel_1`) | `PIEGE` | **`G6`** Le Toucan toco, le bec-radiateur (`panel_1`) | `BLEU` | ✅ Divergent · 0 boucle |
| [`M ↔ H`](#frontiere-m-h-g7-r3) | **`G7`** Le Tapir, jardinier des sentiers (`panel_1`) | `SENTIER_ROUTE` | **`R3`** La Vision du Chamane-Jaguar (`panel_1`) | `CHAMANE_EN_FORET` | ✅ Divergent · 0 boucle |
| [`M ↔ E`](#frontiere-m-e-g8-r7) | **`G8`** Le Boto, l’encantado du fleuve (`panel_1`) | `POSITION_REVE` | **`R7`** Le Curupira, protecteur aux pieds retournés (`panel_1`) | `RECUL` | ✅ Divergent · 0 boucle |
| [`R ↔ H`](#frontiere-r-h-g9-r4) | **`G9`** Le Caïman noir, l’ombre sous la pirogue (`panel_1`) | `CALE` | **`R4`** La Pirogue-Anaconda des Ancêtres (`panel_1`) | `PISTON_REVES` | ✅ Divergent · 0 boucle |
| [`R ↔ E`](#frontiere-r-e-g10-r8) | **`G10`** La Matamata, Guetteuse des Feuilles Mortes (`panel_3`) | `ECAILLE` | **`R8`** Le Rêve de la Mue d’Obsidienne (`panel_3`) | `RANG_REVE` | ✅ Divergent · 0 boucle |
| [`O ↔ H`](#frontiere-o-h-g11-r5) | **`G11`** La Harpie féroce (`panel_2`) | `DEFENSEUR_REDEPLOYE` | **`R5`** Le Ciel à deux eaux (`panel_2`) | `RANG_MACHINE` | ✅ Divergent · 0 boucle |
| [`O ↔ E`](#frontiere-o-e-g12-r9) | **`G12`** L’Ibijau, les yeux fendus de la nuit (`panel_1`) | `RANG_RELU` | **`R9`** La Matinta Pereira, siffleuse de minuit (`panel_1`) | `POSITION_REVE` | ✅ Divergent · 0 boucle |
| [`M ↔ I`](#frontiere-m-i-g13-m1) | **`G13`** Le Tamanoir, le grand mangeur qui épargne (`panel_1`) | `RIPOSTE_ESSAIM` | **`M1`** Le Pelage du Paresseux (`panel_1`) | `INSECTE_PASSAGER` | ✅ Divergent · 0 boucle |
| [`R ↔ I`](#frontiere-r-i-g14-m2) | **`G14`** Le Téju, la ponte au cœur de la termitière (`panel_1`) | `PONTE` | **`M2`** La Termitière-Forteresse (`panel_1`) | `PARADE_SOLDATS` | ✅ Divergent · 0 boucle |
| [`O ↔ I`](#frontiere-o-i-g15-m3) | **`G15`** Le Colibri, porteur de gouttes et de pollen (`panel_1`) | `INSECTE_TRANSPORTE` | **`M3`** Le Bivouac des Légionnaires (`panel_1`) | `NID_NOMADE` | ✅ Divergent · 0 boucle |
| [`H ↔ E`](#frontiere-h-e-r1-r2) *(hybride)* | **`R1`** La Liane des Esprits (`panel_1`) | `REVE_COMPACTE` | **`R2`** Le Fleuve sous la cendre (`panel_2`) | `ALTERATION` | ✅ Divergent · 0 boucle |
| [`H ↔ I`](#frontiere-h-i-r6-m4) | **`R6`** Le Rite de la Tucandeira (`panel_1`) | `ANNULATION_RENFORCEE` | **`M4`** Le Rucher des Mélipones (`panel_1`) | `DEFENSEUR_REDEPLOYE` | ✅ Divergent · 0 boucle |
| [`E ↔ I`](#frontiere-e-i-r10-m5) | **`R10`** La Transe de la Ruche Vagabonde (`panel_3`) | `RANG_REVE` | **`M5`** Le Mycélium Luminescent, Réseau Spectral des Racines Noires (`panel_3`) | `ALTERATION` | ✅ Divergent · 0 boucle |

---

## 2. Fiches complètes par frontière (`X ↔ Y`)

### A. Lisières Animal ↔ Animal (3 lisières · 6 Gardiens)

<a id="frontiere-m-r-g1-g2"></a>
#### Frontière `M ↔ R` — Mammifères ↔ Reptiles (`G1` & `G2`)

> **Paire `panel_1`** · Divergence `I03` : `G1` → **`CROC_POSTE`** vs `G2` → **`RATISSAGE_ROMPU`** (✅ divergent, 0 boucle).

##### `G1` (`M>R` · GARDIEN) — Le Jaguar, seigneur des berges

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Jaguar** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Piégeage** |
| **Pictogrammes** | 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) · 🔵 Jeton Surchauffe Bleu (−1 tous modes) (`PIC_BLEU`) |
| **Résumé plateau** | Le Croc chasse aux côtés du Duel |
| **Mots-clés Face 1** | Croc → parcelle du Duel · parade du Croc = Territoire tenu |
| **Mots-clés Face 2** | Croc et Duel → toute parcelle ciblée · machine parée = 1 Rouge en Bleu |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Jaguar (Panthera onca) — grand félin tacheté, animal entier sur une plage de sable noir du rio, surgissant des herbes vers un caïman qui se chauffe
- **Pitch d’ambiance** : *Le Jaguar ne craint ni l’eau ni les écailles : il chasse le caïman sur sa propre berge et le tue d’une seule morsure au crâne. Là où il rôde, la rive appartient de nouveau à la forêt.*
- **Brief illustration** : Plan large crépusculaire sur une berge de várzea : le Jaguar entier, musculature tendue, rosettes nettes, avance à demi immergé dans l’eau noire ; au premier plan, une gueule de caïman entrouverte (évocation du Croc) ; au fond, des troncs coupés et la lueur orangée d’une machine. Palette ocre, vert profond, reflets d’or sur l’eau.
- **Règle — Face 1** :
> Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur la parcelle qui porte le jeton Duel, quelle que soit sa face. Le Croc y pare en premier, comme toujours, puis regagne la réserve Reptile. Pacte de la berge : tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne aussi le Duel sur Territoire tenu, comme si un Défenseur l’avait parée. Si le Duel n’est pas en forêt, le Jaguar ne fait rien.
- **Règle — Face 2** :
> Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur n’importe quelle parcelle ciblée, de n’importe quel rayon. Le jeton Duel peut traverser le fleuve avec lui : déplacez-le sur cette parcelle, sur sa face actuelle, même sans Défenseur Mammifère. Le Croc y pare en premier puis regagne la réserve Reptile ; tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne le Duel sur Territoire tenu. Morsure au crâne : la machine dont le Croc vient de parer la frappe retourne aussi 1 de ses Rouges en Bleu.
- **Décision (Choix)** : Où poster le Croc : sur le Duel pour sceller un Territoire tenu, ou (Face 2) sur la parcelle ciblée la plus menacée d’un autre rayon, Duel compris.
- **Renoncement** : Déplacer le Croc dégarnit la parcelle où une Écaille l’avait posé ; et l’icône Piégeage ne s’allume que si une frappe tombe réellement sur lui.
- **Double activation (Gardien)** : Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume Piégeage, l’icône même où siège le Jaguar, d’où une seconde activation qui le reposte aussitôt pour la frappe suivante. Deux activations = deux parades du Croc et un Duel scellé sur Territoire tenu dès la première.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `DUEL`, `CROC` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `CROC_POSTE`, `CROC`, `TERRITOIRE`, `BLEU` · **Déclencheurs amorcés** : `ICONE_PIEGEAGE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Piégeage. Poster le Croc sur le Duel si une machine révélée vise sa parcelle ; sinon (Face 2) sur la parcelle ciblée la plus boisée. Ne jamais retirer le Croc d’une parcelle dont la frappe n’est pas résolue sans cible plus menacée.

**Témoins (2)**

- **`G1_T1`** (`A_CODER`) : Croc en réserve, Duel face Défi sur la parcelle 3 du rayon M ; le Jaguar s’active : le Croc y est posté ; le Bulldozer frappe la parcelle 3 : le Croc pare (Piégeage) et regagne la réserve ; le Duel passe sur Territoire tenu.
- **`G1_T2`** (`A_CODER`) : Face 2 : Croc et Duel postés sur la parcelle 2 ciblée du rayon H ; une Abatteuse portant 2 Rouges frappe, le Croc pare : Duel sur Territoire tenu, Abatteuse à 1 Rouge et 1 Bleu.

##### `G2` (`R>M` · GARDIEN) — L’Anaconda vert, l’étau des eaux dormantes

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⚡ Twist 2K3

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **L’Anaconda vert** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Parade** |
| **Pictogrammes** | ⚡ Brique-Twist 2K3 (`PIC_TWIST`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) · ⏪ Recul de machine (−1 parcelle) (`PIC_RECUL`) |
| **Résumé plateau** | Arrache une machine à son Ratissage |
| **Mots-clés Face 1** | Ratissage sur Territoire tenu ou 2 Défenseurs → jeton au sac · recul 1 |
| **Mots-clés Face 2** | Duel ou 2 Défenseurs · Ratissage arraché · machine mobile noyée et reculée |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : L’Anaconda vert (Eunectes murinus) — serpent géant entier, anneaux olive tachetés de noir, enroulé dans les eaux d’un igapó
- **Pitch d’ambiance** : *L’Anaconda attend des heures, invisible sous la lentille d’eau. Quand la proie s’aventure au bord, chaque expiration resserre ses anneaux, et il l’entraîne là où plus rien ne pousse : au fond.*
- **Brief illustration** : Vue semi-immergée : l’Anaconda vert entier, anneaux déroulés sous la surface, enserre les chenilles d’une machine de déboisement à demi engloutie ; sur la berge, les empreintes fraîches d’un jaguar. Lumière verte filtrée, eau sombre et miroitante.
- **Règle — Face 1** :
> Quand l’Anaconda vert s’active : choisissez une machine en Ratissage dont la parcelle porte le jeton Duel face Territoire tenu, ou au moins 2 Défenseurs. L’étau l’arrache à son Ratissage : reprenez le jeton Machine glissé sous elle et remettez-le dans le sac ; la machine redevient mobile et recule d’1 parcelle vers la bordure (en sautant les Routes Forestières), en conservant tous ses jetons Puissance. Faute de jeton tiré, elle n’attaque plus avant le ménage ; au ménage, n’étant plus sur la dernière parcelle, elle ne rentre pas en Ratissage.
- **Règle — Face 2** :
> Quand l’Anaconda vert s’active : choisissez une machine dont la parcelle porte le jeton Duel (sur l’une ou l’autre face) ou au moins 2 Défenseurs. Si elle est en Ratissage, l’étau l’en arrache : reprenez son jeton Machine et remettez-le dans le sac ; elle redevient mobile, recule d’1 parcelle vers la bordure (en sautant les Routes Forestières) en conservant ses jetons Puissance, et n’attaque plus avant le ménage. Si elle est mobile et n’a pas encore attaqué, l’Anaconda la noie : inclinez son jeton Machine (elle est annulée) et faites-la reculer d’1 parcelle vers la bordure.
- **Décision (Choix)** : Arracher maintenant la machine en Ratissage, ou la laisser au fond tant que son jeton n’alourdit pas le sac.
- **Renoncement** : Le jeton Machine rendu au sac rend chaque pioche future plus dangereuse ; et le Duel engagé sur la dernière parcelle ne couvre plus la lisière.
- **Double activation (Gardien)** : Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la même dernière parcelle : la première activation arrache l’Abatteuse, la seconde le Bulldozer, tant que le Duel tient la parcelle. En Face 2, la seconde activation peut aussi noyer la machine mobile qui s’apprête à frapper le Duel.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `RATISSAGE`, `DUEL` · **Entrées synergie (`I01`)** : `TERRITOIRE`
- **Sorties (`I03`)** : `RATISSAGE_ROMPU`, `RECUL`, `ANNULATION` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Siéger sur Parade. Arracher en priorité la machine en Ratissage la plus chargée en Rouges ; refuser si le sac ne contient plus qu’1 Sabotage et qu’il reste au moins 4 tours.

**Témoins (2)**

- **`G2_T1`** (`A_CODER`) : Bulldozer en Ratissage (2 Rouges) sur la dernière parcelle du rayon R, Duel face Territoire tenu sur cette parcelle ; l’Anaconda s’active au rang 2 : jeton remis au sac, Bulldozer mobile en parcelle 3, aucune frappe de Ratissage.
- **`G2_T2`** (`A_CODER`) : Face 2 : une Abatteuse mobile du rang 5 vise la parcelle du Duel (face Défi) ; l’Anaconda s’active au rang 2 : Abatteuse annulée (jeton incliné) et reculée d’1 parcelle.

---

<a id="frontiere-m-o-g3-g4"></a>
#### Frontière `M ↔ O` — Mammifères ↔ Oiseaux (`G3` & `G4`)

> **Frontière hybride `panel_2` × `panel_1`** · Divergence `I03` : `G3` → **`DEFENSEUR_REDEPLOYE`** vs `G4` → **`PARI_GLISSE`** (✅ divergent, 0 boucle).

##### `G3` (`M>O` · GARDIEN) — L’Atèle

- **Provenance** : `panel_2.json` *(reclassé hors-twist depuis `panel_2`)* · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **L’Atèle** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Sabotage** |
| **Pictogrammes** | 🌳 Arbre debout (`PIC_ARBRE`) · 🛣️ Route forestière (`PIC_ROUTE`) · 🛡️ Défenseur (`PIC_DEFENSEUR`) · 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) |
| **Résumé plateau** | Deux cimes · traverse / Plume · trajet en L |
| **Mots-clés Face 1** | Deux cimes · traverse |
| **Mots-clés Face 2** | Plume · trajet en L |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Atèle dans la canopée
- **Pitch d’ambiance** : *L’atèle essaie le poids d’une branche avant de lâcher la précédente. Au-dessous de lui, le chemin a disparu.*
- **Brief illustration** : Atèle entier suspendu par la queue entre deux couronnes. En contrebas, une trouée coupe le chemin radial.
- **Règle — Face 1** :
> À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux. Il traverse leur frontière entre deux parcelles de même profondeur portant chacune un Arbre debout. Avant de traverser, il peut faire un pas radial sur son rayon, en sautant les Routes. Le Duel reste en place.
- **Règle — Face 2** :
> À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux, ou entre le rayon portant la Plume et un de ses voisins. Traversez entre deux parcelles de même profondeur portant chacune un Arbre. Vous pouvez ajouter un pas radial avant et un après la traversée, en sautant les Routes. Le Duel reste en place.
- **Décision (Choix)** : Quelle cime peut-on dégarnir pour tenir l’autre rive ?
- **Renoncement** : Le pion quitte réellement sa première ligne de défense.
- **Double activation (Gardien)** : Deux traversées amènent les deux pions nécessaires à une Parade ou desservent deux rayons différents.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `ARBRE`, `ROUTE`, `DEFENSEUR_REDEPLOYE` · **Entrées synergie (`I01`)** : `PLUME`
- **Sorties (`I03`)** : `DEFENSEUR_REDEPLOYE` · **Déclencheurs amorcés** : `ICONE_PARADE` · **Paiement** : —
- **Heuristique bot** : Chercher une destination qui fait atteindre le seuil exact. Écarter les trajets qui feraient perdre une Parade plus coûteuse au départ.

**Témoins (2)**

- **`G3_T1`** (`OK`) : En Face 2, un Défenseur quitte M1, saute la Route M2 jusqu’à M3, traverse entre les arbres M3 et O3, puis descend en O4. Il rejoint le Défenseur qui attend un Ratissage de seuil 2.
- **`G3_T2`** (`OK`) : Deux traversées F1 entre deux cimes de même profondeur portent deux Défenseurs de M vers une cible d’O de seuil 2.

##### `G4` (`O>M` · GARDIEN) — L’Ara rouge, sentinelle de la collpa

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **L’Ara rouge** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Résonance** |
| **Pictogrammes** | ⭐ Encoche / sécurisation de pari Gardien (`PIC_PARI_ENCOCHE`) · 🔔 Icône Résonance / cascade de Gardiens (`PIC_RESONANCE`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) |
| **Résumé plateau** | Cri d’alarme qui fait avancer les paris |
| **Mots-clés Face 1** | 1 pari d’un autre Gardien → encoche · Territoire tenu → Défi = 2e cri · seul en piste : son 2e pari glisse aussi |
| **Mots-clés Face 2** | Un autre Gardien avec pari s’active · Territoire tenu → Défi = 2e réveil · seul en piste : son 2e pari glisse aussi |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : L’Ara rouge (Ara macao), animal entier agrippé à une falaise d’argile
- **Pitch d’ambiance** : *À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.*
- **Brief illustration** : L’Ara rouge (Ara macao), animal entier : perroquet écarlate, jaune et bleu, agrippé à une falaise d’argile (collpa) au milieu de sa volée, le bec ouvert sur le cri d’alarme.
- **Règle — Face 1** :
> Le cri d’alarme. Quand l’Ara rouge s’active : faites glisser 1 Défenseur posé en pari sur un autre Gardien construit vers une encoche libre de ce même Gardien. Cela ne résout pas le pouvoir de ce Gardien et n’allume aucune icône. Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour faire glisser de la même façon un 2e Défenseur, posé en pari sur un Gardien différent du premier.
> Sentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, l’Ara crie pour sa propre volée : faites aussi glisser son second pari, s’il en porte un, dans son encoche encore libre.
- **Règle — Face 2** :
> La volée se lève. Quand l’Ara rouge s’active : choisissez un autre Gardien construit qui porte au moins 1 Défenseur en pari ; il s’active aussitôt (son Défenseur glisse dans une encoche et vous résolvez son pouvoir comme si son icône venait de s’allumer ; s’il s’agit de sa 1re activation du tour, la Résonance la compte). Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour réveiller de la même façon un 2e Gardien, différent du premier. L’Ara ne se réveille jamais lui-même.
> Sentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, faites aussi glisser le second pari de l’Ara, s’il en porte un, dans son encoche encore libre, sans résoudre son pouvoir une seconde fois.
- **Décision (Choix)** : Quel pari faire progresser — celui du Gardien le plus en retard, ou celui dont le pouvoir doit frapper maintenant (Face 2).
- **Renoncement** : Retourner le Duel sur Défi pour un 2e cri libère l’avancée des machines de sa parcelle aux rangs 3 et 6 ; construit en premier, l’Ara posé sur Parade s’active seul, mais renonce à la cascade de la Résonance tant qu’il reste en piste.
- **Double activation (Gardien)** : Chaque cri fait progresser un pari différent : deux activations bouclent le pari d’un Gardien qui ne s’allume jamais (deux glissements sur la même tuile) ou en sécurisent deux. En Face 2, chaque cri déclenche en plus le pouvoir du Gardien réveillé, et chaque 1re activation ainsi provoquée relance la Résonance. Seul en piste, une seule activation boucle son propre pari de deux Défenseurs.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `GARDIEN` · **Entrées synergie (`I01`)** : `TERRITOIRE`
- **Sorties (`I03`)** : `PARI_GLISSE`, `ACTIVATION_RELAIS`, `DEFI` · **Déclencheurs amorcés** : `ICONE_RESONANCE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Résonance (ou Parade en repli si premier Gardien construit). Glisser d’abord le pari du Gardien dont l’icône a le moins de chances de s’allumer ; n’utiliser l’Écho (Territoire tenu → Défi) que si l’Éveil est atteignable au tour même.

**Témoins (2)**

- **`G4_T1`** (`A_CODER`) : La Matamata porte 1 pari et 0 encoche occupée ; l’Ara s’active : le pari glisse dans l’encoche ; en fin d’attaques, 0 pion sur la Matamata et 1 encoche : pari gagné.
- **`G4_T2`** (`A_CODER`) : Plancher (Tour 2) : l’Ara, construit au Tour 1 et posé sur Parade (icône de repli), est le seul Gardien en piste ; il porte 2 paris. Après une parade au rang 1, il s’active : son 1er pari glisse dans une encoche ; sentinelle seule, le 2nd aussi. En fin d’attaques, 0 pion sur la tuile et 2 encoches occupées : pari gagné, l’Ara passe en Face 2.

---

<a id="frontiere-r-o-g5-g6"></a>
#### Frontière `R ↔ O` — Reptiles ↔ Oiseaux (`G5` & `G6`)

> **Paire `panel_1`** · Divergence `I03` : `G5` → **`PIEGE`** vs `G6` → **`BLEU`** (✅ divergent, 0 boucle).

##### `G5` (`R>O` · GARDIEN) — L’Iguane vert, dormeur des hautes branches

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **L’Iguane vert** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Piégeage** |
| **Pictogrammes** | 🪤 Piège autonome (`PIC_PIEGE`) · 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) · 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) · 🔵 Jeton Surchauffe Bleu (−1 tous modes) (`PIC_BLEU`) |
| **Résumé plateau** | Tombe en Piège au cri des oiseaux |
| **Mots-clés Face 1** | Piège là où signale la Plume (sinon rayon R ou O) · Bleu bu = le Croc tombe aussi |
| **Mots-clés Face 2** | Piège + Croc sur toute parcelle ciblée · Bleu bu = second plongeon |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : L’Iguane vert (Iguana iguana), animal entier allongé sur une branche au-dessus de l’eau
- **Pitch d’ambiance** : *L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.*
- **Brief illustration** : L’Iguane vert (Iguana iguana), animal entier : grand lézard à la crête dorsale dressée, allongé au soleil sur une branche au-dessus de l’eau, l’œil tourné vers un oiseau qui donne l’alerte.
- **Règle — Face 1** :
> La chute au cri des oiseaux. Quand l’Iguane vert s’active, il se laisse tomber : posez 1 Piège sur une parcelle ciblée qui n’en porte pas encore, sur le rayon désigné par la Plume de Vigie, ou visée par une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu ou ne signale aucune parcelle ciblée, il tombe au plus près : sur une parcelle ciblée du rayon Reptile ou du rayon de l’Oiseau. S’il n’y en a aucune, il guette : posez le Piège sur n’importe quelle parcelle libre de Piège ordinaire du rayon Reptile, où il attendra la prochaine frappe.
> Boire la chaleur (amplificateur) : avant de tomber, vous pouvez boire 1 Bleu : retirez-le d’une machine de n’importe quel rayon et remettez-le dans la réserve (la machine perd la Surchauffe correspondante). Gorgé de chaleur, l’Iguane tombe avec ses mâchoires : si le Croc est dans la réserve Reptile, postez-le sur la parcelle du Piège. Il y pare en premier, le Piège ensuite.
- **Règle — Face 2** :
> Le plongeon. Quand l’Iguane vert s’active, il plonge où il veut : posez 1 Piège sur n’importe quelle parcelle ciblée qui n’en porte pas encore, de n’importe quel rayon, et postez-y le Croc s’il est dans la réserve Reptile (si la Plume de Vigie est face Chaud, prenez le Croc où qu’il se trouve sur le plateau). Le Croc pare en premier, le Piège ensuite.
> Boire la chaleur (amplificateur) : avant de plonger, vous pouvez boire 1 Bleu (retiré d’une machine de n’importe quel rayon, rendu à la réserve) : l’Iguane plonge une seconde fois et pose 1 second Piège sur une autre parcelle ciblée libre de Piège ordinaire. Chacune de ces parades allume Piégeage.
- **Décision (Choix)** : Tomber seul là où la Plume l’indique, ou boire un Bleu pour emporter le Croc (Face 1) ou plonger deux fois (Face 2) ; de préférence le Bleu d’une machine déjà annulée, ou dont le Seuil est déjà tombé à 1.
- **Renoncement** : La machine qui perd son Bleu redevient plus difficile à parer, et ce Bleu manquera au Toucan pour la faire caler ; le Croc emporté ne garde plus la parcelle où une Écaille l’avait posté.
- **Double activation (Gardien)** : Chaque Piège qui pare allume Piégeage, l’icône de l’Iguane : la chute appelle la chute, une fois par pari. Deux chutes couvrent les deux parcelles d’un « En avançant » (Sur place et Devant), ou deux fois la même parcelle visée par l’Abatteuse puis le Bulldozer. Avec le Toucan à ses côtés, chaque chute boit son Bleu : le Croc tombe à chaque fois s’il a regagné la réserve (Face 1), et quatre Pièges couvrent la forêt (Face 2).

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `PLUME` · **Entrées synergie (`I01`)** : `BLEU`
- **Sorties (`I03`)** : `PIEGE`, `CROC` · **Déclencheurs amorcés** : `ICONE_PIEGEAGE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Piégeage. En autonomie, poser le Piège sur la parcelle ciblée signalée par la Plume qui porte le plus d’Arbres debout ; avec un Bleu disponible, boire celui d’une machine annulée ou à Seuil 1 pour ajouter le Croc (Face 1) ou doubler la pose de Pièges (Face 2).

**Témoins (2)**

- **`G5_T1`** (`A_CODER`) : Plancher sans Toucan (Tour 2, Acte 1) : aucun Bleu en jeu. La Plume est posée face Chaud au pied du rayon O, dont la parcelle 2 est visée au rang 4 par l’Abatteuse (Sur place) puis au rang 5 par le Bulldozer (Devant). Un Piège pare au rang 1 (Piégeage) : l’Iguane (2 paris) tombe sur la parcelle 2 ; au rang 4 son Piège pare l’Abatteuse (Piégeage), seconde activation, nouveau Piège sur la même parcelle qui pare le Bulldozer au rang 5.
- **`G5_T2`** (`A_CODER`) : Amplifié par le Toucan (Face 1) : le Toucan a retourné 1 Rouge en Bleu sur l’Abatteuse du rayon M, annulée à l’ouverture par un Rêve. La Plume désigne le rayon R, dont la parcelle 3 est visée aux rangs 4 et 5. Après une parade de Piège au rang 2, l’Iguane boit le Bleu de la machine annulée et tombe avec le Croc sur la parcelle 3 : le Croc pare l’Abatteuse, le Piège pare le Bulldozer (deux fois Piégeage).

##### `G6` (`O>R` · GARDIEN) — Le Toucan toco, le bec-radiateur

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : Brique fluide

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Toucan toco** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Résonance** |
| **Pictogrammes** | 🔴 Jeton Puissance Rouge (+1) (`PIC_ROUGE`) · 🔵 Jeton Surchauffe Bleu (−1 tous modes) (`PIC_BLEU`) · 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) · 🚫 Machine annulée (jeton incliné 90°) (`PIC_ANNULATION`) |
| **Résumé plateau** | Rend la chaleur aux machines |
| **Mots-clés Face 1** | 1 Rouge → Bleu sur la cible désignée par la Plume |
| **Mots-clés Face 2** | 1 Rouge → Bleu partout · 0 Rouge et 2 Bleus = machine calée |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Toucan toco (Ramphastos toco) — oiseau entier au bec orange démesuré, perché au sommet d’un arbre émergent
- **Pitch d’ambiance** : *Le bec du toucan toco est un radiateur vivant : il y dirige son sang pour relâcher la chaleur du jour. Au-dessus des machines brûlantes, il rend la fournaise au monde, et le métal s’essouffle.*
- **Brief illustration** : Contre-jour brûlant : le Toucan toco entier, bec orange incandescent, se découpe sur un ciel blanc de chaleur ; des volutes de chaleur partent de son bec vers une machine en contrebas dont les jauges virent au bleu ; un iguane se chauffe sur une branche voisine. Orange, noir, bleu électrique.
- **Règle — Face 1** :
> Quand le Toucan toco s’active : il rayonne : retournez 1 Rouge en Bleu sur une machine, mobile ou en Ratissage, du rayon désigné par la Plume de Vigie, ou sur une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu, visez une machine du rayon de l’Oiseau ou d’un rayon voisin.
- **Règle — Face 2** :
> Quand le Toucan toco s’active : il rayonne sur toute la forêt : retournez 1 Rouge en Bleu sur une machine de n’importe quel rayon, mobile ou en Ratissage. Coup de chaleur : si cette machine ne porte alors plus aucun Rouge mais au moins 2 Bleus, et qu’elle n’a pas encore attaqué, elle cale : inclinez son jeton Machine à 90° (pour une machine en Ratissage, tournez la machine elle-même d’un quart de tour) ; elle est annulée jusqu’au ménage, où elle reprend sa position.
- **Décision (Choix)** : Disperser la Surchauffe pour abaisser plusieurs Seuils, ou la concentrer sur une seule machine pour la faire caler (Face 2).
- **Renoncement** : Chaque Bleu concentré sur la machine à caler n’aide pas les autres parades ; et l’Iguane voisin voudra boire ces mêmes Bleus.
- **Double activation (Gardien)** : La surchauffe se construit en deux temps : la première activation convertit un Rouge, la seconde le dernier Rouge de la même machine ; en Face 2, celle-ci cale aussitôt (0 Rouge, 2 Bleus) avant même d’attaquer. Sur Résonance, le Toucan s’active de nouveau à chaque 1re activation d’un autre Gardien.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `ROUGE`, `PLUME` · **Entrées synergie (`I01`)** : `BLEU`
- **Sorties (`I03`)** : `BLEU`, `ANNULATION_SURCHAUFFE` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Siéger sur Résonance. Convertir d’abord le Rouge d’une machine en Assaut qui n’a pas encore attaqué ; en Face 2, finir la machine à 1 seul Rouge qui porte déjà au moins 1 Bleu.

**Témoins (2)**

- **`G6_T1`** (`A_CODER`) : Abatteuse en Mode Assaut, 2 Rouges, parcelle gravée 3 (Seuil 5) ; le Toucan s’active : 1 Rouge et 1 Bleu, Seuil 3.
- **`G6_T2`** (`A_CODER`) : Face 2 : Bulldozer à 1 Rouge et 1 Bleu au rang 6, pas encore résolu ; le Toucan s’active : 0 Rouge, 2 Bleus, le Bulldozer cale et n’attaque pas.

---

### B. Lisières Animal ↔ Onirique (6 lisières · 6 Gardiens + 6 Rêves)

<a id="frontiere-m-h-g7-r3"></a>
#### Frontière `M ↔ H` — Mammifères ↔ Humains (`G7` & `R3`)

> **Paire `panel_1`** · Divergence `I03` : `G7` → **`SENTIER_ROUTE`** vs `R3` → **`CHAMANE_EN_FORET`** (✅ divergent, 0 boucle).

##### `G7` (`M>H` · GARDIEN) — Le Tapir, jardinier des sentiers

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⚡ Twist 2K3 · 🌱 Enracinement

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Tapir** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Parade** |
| **Pictogrammes** | ⚡ Brique-Twist 2K3 (`PIC_TWIST`) · 🛣️ Route forestière (`PIC_ROUTE`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) · 🥁 Chamane Tambour (Humains) (`PIC_TAMBOUR`) |
| **Résumé plateau** | Change les Routes en sentiers où les machines s’enlisent |
| **Mots-clés Face 1** | Duel ou Chamane sur Route = sentier (parcelle vide, plus sautée) · sinon Duel → Chamane = Territoire tenu |
| **Mots-clés Face 2** | + frappes des parcelles voisines détournées sur le sentier · l’Abatteuse n’en déloge plus le Duel |
| **Mots-clés Enraciné** | Fin de partie : Duel + Chamane sur une parcelle = 1 repousse de plus |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Tapir terrestre (Tapirus terrestris), animal entier avançant dans un sentier de boue
- **Pitch d’ambiance** : *Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.*
- **Brief illustration** : Le Tapir terrestre (Tapirus terrestris), animal entier : grand herbivore à la trompe mobile, robe brun sombre et courte crinière, qui avance au crépuscule dans un sentier de boue tracé en travers d’une trouée de bulldozer. Empreintes à quatre doigts dans la glaise ; à l’orée, un chamane suit la piste, tambour à la main.
- **Règle — Face 1** :
> Le sentier battu. Quand le Tapir s’active, choisissez l’un de ses deux pas :
> • Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon — pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère —, ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon. Cette Route devient un sentier.
> • Frayer (toujours possible, même sans aucune Route en jeu) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère. S’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu : les hommes tiennent déjà ce terrain.
> Le sentier : (1) tant qu’il porte le Duel ou un Chamane, le sentier compte comme une parcelle, avec le chiffre gravé de sa case, bien qu’il ne porte ni Arbre ni Souche ; (2) les machines ne le sautent plus : une frappe Devant le vise, une avancée s’y arrête, et une frappe sur le sentier ne fait jamais gagner de Rouge ; (3) il accueille Défenseurs, Piège et autres pièces de défense comme toute parcelle, et le Duel y suit ses règles habituelles (parade → Territoire tenu ; frappe non parée et non piégée → retour en réserve) ; (4) une frappe de Bulldozer non parée le refait Route, et dès qu’il ne porte plus ni Duel ni Chamane (frappe, déplacement, retour des Défenseurs au ménage), il redevient Route : la case est vidée et toute machine qui s’y trouve se replie comme sur une Route qui vient de se créer ; (5) jamais de sentier sur la dernière case d’un rayon, tout sentier redevient aussitôt Route si le Tapir quitte la Piste des Gardiens, et aucun pion Arbre ou Souche n’est jamais déplacé.
- **Règle — Face 2** :
> Le sentier qui égare. Quand le Tapir s’active, choisissez l’un de ses deux pas :
> • Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon (pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère), ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon : elle devient un sentier.
> • Frayer (toujours possible) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère ; s’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu.
> En Face 2, le sentier obéit aux règles du sentier avec deux pas de plus :
> • Les machines s’égarent : quand une machine attaque, avant de figer ses cibles, si l’une d’elles est la parcelle juste avant ou juste après un sentier sur ce rayon, vous pouvez détourner cette frappe sur le sentier.
> • La boue tient : une frappe d’Abatteuse non parée sur un sentier ne déloge plus le Duel : seul un Bulldozer non paré refait la Route.
- **Règle — Enraciné** :
> Les graines du sentier. Au décompte final, en plus de sa repousse habituelle (1 Souche, ou 2 s’il était en Face 2, sur la parcelle qu’il regarde), le Tapir fait repousser 1 Souche de la parcelle qui porte le jeton Duel, si le Tambour ou le Chant s’y tient aussi. Cette clause ne se lit qu’au décompte final.
- **Décision (Choix)** : Fouler une Route — avec le Duel, qui tient d’un tour à l’autre, ou avec un Chamane, jusqu’au ménage — ou frayer pour poster le Duel en Territoire tenu auprès d’un Chamane.
- **Renoncement** : Le Duel posé sur un sentier ne garde plus aucune parcelle boisée ; le Chamane qui descend abandonne la parcelle qu’il gardait ; un Bulldozer non paré refait la Route en vidant la case.
- **Double activation (Gardien)** : Deux pas, deux sentiers : la première activation pose le Duel sur une Route, la seconde y fait descendre un Chamane sur une autre, ou sur la même pour que le sentier survive au départ du Duel. Chaque frappe parée sur un sentier allume Parade, l’icône du Tapir. En Face 2, chaque sentier attire en plus les frappes de ses deux voisines.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `ROUTE`, `DUEL`, `TAMBOUR`, `CHANT` · **Entrées synergie (`I01`)** : `CHAMANE_EN_FORET`
- **Sorties (`I03`)** : `SENTIER_ROUTE`, `TERRITOIRE`, `ARBRE` · **Déclencheurs amorcés** : `ICONE_PARADE` · **Paiement** : `P_SOUCHE`
- **Heuristique bot** : Siéger sur Parade. S’il existe une Route devant une parcelle boisée menacée, y poser le Duel ou y faire descendre un Chamane pour absorber les frappes Devant et bloquer l’avancée ; sans Route, Frayer auprès du Tambour/Chant pour verrouiller Territoire tenu. Enraciner en fin de partie si Duel et Chamane peuvent se réunir sur une parcelle à Souches.

**Témoins (2)**

- **`G7_T1`** (`A_CODER`) : Le sentier tenu par le Tambour (Tour 3, Acte 1) : sur le rayon H, parcelle 1 (2 Arbres) porte Bulldozer (rang 3), Abatteuse (rang 5) et Tambour ; parcelle 2 est une Route ; parcelle 3 porte 3 Arbres. Après une parade au rang 1, le Tapir (sur Parade) fait descendre le Tambour sur la Route (sentier gravé 2). Au rang 3 le Bulldozer frappe la parcelle 1 puis le sentier (paré par le Tambour, Parade) et s’arrête sur le sentier ; au rang 5 l’Abatteuse frappe le sentier à vide ; au ménage le sentier redevient Route et le Bulldozer se replie en parcelle 1. Parcelle 3 intacte.
- **`G7_T2`** (`A_CODER`) : Plancher Frayer (Tour 2, Acte 1, aucune Route en jeu) : le Tapir, construit au Tour 1, porte 1 pari. Sur le rayon M, le Bulldozer en parcelle 1 (2 Arbres) est révélé au rang 6 face à 1 Défenseur Mammifère et le Tambour. Après une parade au rang 2, le Tapir fraye : le Duel quitte la réserve, rejoint le Tambour et arrive face Territoire tenu. Au rang 6, la frappe Sur place est parée et Territoire tenu bloque l’avancée en parcelle 1.

##### `R3` (`H>M` · REVE) — La Vision du Chamane-Jaguar

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : Brique fluide

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Chamane-Jaguar** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · 🛡️ Défenseur (`PIC_DEFENSEUR`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) |
| **Résumé plateau** | Annule puis bondit défendre la forêt |
| **Mots-clés Face 1** | Après annulation · ses Défenseurs bondissent vers le Duel ou une parcelle visée |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Vision chamanique de la métamorphose — un chamane dont l’ombre devient celle d’un jaguar en plein bond
- **Pitch d’ambiance** : *Chez les peuples du Haut Rio Negro, un même mot désigne le chamane et le jaguar. Quand la vision le prend, le chamane quitte le rêve sur quatre pattes et bondit là où la forêt saigne.*
- **Brief illustration** : Nuit de cérémonie : un chamane danse autour d’un feu, coiffe de plumes, corps peint ; son ombre projetée sur la canopée est celle d’un jaguar bondissant, qui atterrit sur une parcelle menacée à côté du jeton Duel. Rouges braise, noirs, taches dorées.
- **Règle — Face 1** :
> Quand ce Rêve est défendu, à sa résolution : une fois ses annulations faites, chaque Défenseur posé sur ce Rêve peut bondir hors de lui, sur sa face Définitif, vers la parcelle qui porte le jeton Duel, ou vers une parcelle ciblée du rayon d’une machine que ce Rêve vient d’annuler. Il y compte pour toutes les parades à venir. Sur la parcelle du Duel, un Défenseur Humain arrivé ainsi compte comme un Défenseur Mammifère pour retourner le Duel sur Territoire tenu.
- **Décision (Choix)** : Où bondir : sur le Duel pour sceller un Territoire tenu, ou sur la parcelle visée du rayon dont une machine vient d’être annulée.
- **Renoncement** : Engager un Défenseur sur ce Rêve, c’est parier qu’une machine tombera sur son rang : s’il n’annule rien, il ne peut bondir que vers le Duel.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `RANG_REVE`, `DUEL` · **Entrées synergie (`I01`)** : `ANNULATION`
- **Sorties (`I03`)** : `CHAMANE_EN_FORET`, `DEFENSEUR_REDEPLOYE`, `TERRITOIRE` · **Déclencheurs amorcés** : `ICONE_PARADE` · **Paiement** : —
- **Heuristique bot** : Défendre ce Rêve quand le Duel est posé sur une parcelle à Seuil 2 ou plus ; bondir vers la parcelle visée dont le déficit est exactement 1.

**Témoins (1)**

- **`R3_T1`** (`A_CODER`) : Rêve H au rang 2 défendu par le Chant ; il annule l’Abatteuse du rayon M ; le Chant bondit sur la parcelle 3 du rayon M (Duel face Défi, 1 Défenseur M) ; la frappe du Bulldozer y est parée (Seuil 2) ; le Duel passe sur Territoire tenu.

---

<a id="frontiere-m-e-g8-r7"></a>
#### Frontière `M ↔ E` — Mammifères ↔ Entités Magiques (`G8` & `R7`)

> **Paire `panel_1`** · Divergence `I03` : `G8` → **`POSITION_REVE`** vs `R7` → **`RECUL`** (✅ divergent, 0 boucle).

##### `G8` (`M>E` · GARDIEN) — Le Boto, l’encantado du fleuve

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil · 🌙 Levier Rêve

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Boto** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Rêve** |
| **Pictogrammes** | ⬅️ Déplacement / avancée de Rêve (`PIC_AVANCEE_REVE`) · 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) |
| **Résumé plateau** | Fait nager les Rêves vers le rang 1 |
| **Mots-clés Face 1** | 1 Rêve glisse d’1 rang à gauche ou échange avec son voisin · aucun Rêve ne nage = 1 Altération |
| **Mots-clés Face 2** | 1 Rêve glisse de 2 rangs ou plonge sous son voisin · ou échange · aucun Rêve ne nage = 1 Altération |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Boto (Inia geoffrensis), dauphin rose de l’Amazone glissant entre les troncs inondés
- **Pitch d’ambiance** : *Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.*
- **Brief illustration** : Le Boto (Inia geoffrensis), dauphin rose de l’Amazone, animal entier, glissant entre les troncs d’une forêt inondée ; sur l’eau sombre se reflète la silhouette d’un homme en blanc.
- **Règle — Face 1** :
> La nage. Quand le Boto s’active : faites nager un Rêve : glissez-le d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent). Si ce rang est occupé, vous pouvez à la place échanger ce Rêve avec le Rêve qui l’occupe (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
> L’encantado (plancher) : si aucun Rêve ne peut nager (Réglette sans Rêve, ou seul Rêve déjà au rang 1), le Boto envoûte à la place une machine : posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.
- **Règle — Face 2** :
> La plongée vers l’Encante. Quand le Boto s’active : faites glisser un Rêve d’1 ou 2 rangs libres vers la gauche (ses Défenseurs le suivent), ou faites-le plonger sous le Rêve qui le précède : il ressort sur le premier rang libre situé à gauche de celui-ci. Vous pouvez aussi, à la place, échanger deux Rêves voisins (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
> L’encantado (plancher) : si aucun Rêve ne peut nager ni plonger, posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.
- **Décision (Choix)** : Faire nager le Rêve vers le rang où des machines viennent d’être révélées (annulation immédiate) ou vers le bloc du Sommeil ; sans Rêve, envoûter la machine qui menacera la parcelle la plus boisée à sa prochaine sortie.
- **Renoncement** : Un Rêve déplacé quitte le rang qu’il couvrait : les machines qui y arriveraient ensuite (déviées ou relues) ne seront plus annulées.
- **Double activation (Gardien)** : Deux nages font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2), ou compactent deux Rêves séparés : le plus court chemin vers le Sommeil quand les Humains ne sont pas à la table. Posé sur Rêve, le Boto nage dès la première annulation ; posé sur Sabotage, il déplace les Rêves avant même leur résolution. Sans Rêve, deux envoûtements sur deux machines différentes.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `RANG_REVE` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `POSITION_REVE`, `ALTERATION`, `ANNULATION` · **Déclencheurs amorcés** : `ICONE_REVE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Rêve (ou Sabotage en repli avant le premier Rêve). Si une machine révélée occupe un rang libre juste à gauche d’un Rêve non résolu, nager vers elle ; sinon compacter vers le rang 1 pour viser le Sommeil ; sans Rêve en jeu, altérer la machine mobile la plus avancée.

**Témoins (2)**

- **`G8_T1`** (`A_CODER`) : Rêve E au rang 5 non résolu, machine révélée au rang 4 ; un Rêve au rang 2 annule et allume Rêve ; le Boto s’active : le Rêve E passe au rang 4 et annule la machine.
- **`G8_T2`** (`A_CODER`) : Plancher (Tour 2, aucun Rêve construit) : le Boto, construit au Tour 1 et posé sur Sabotage (icône de repli), s’active au premier Sabotage révélé : l’encantado pose 1 Altération sur l’Abatteuse du rayon M en parcelle 2. À sa prochaine révélation, elle compte dans m(r) mais recule en parcelle 1 sans frapper.

##### `R7` (`E>M` · REVE) — Le Curupira, protecteur aux pieds retournés

- **Provenance** : `panel_1.json` · **Nature** : `LOI_PASSIVE` · **Rôles** : ⚖️ Loi passive

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Curupira** |
| **Fenêtre / Icône** | `PERMANENT` |
| **Pictogrammes** | ⚖️ Loi passive permanente (`PIC_LOI_PASSIVE`) · ⏪ Recul de machine (−1 parcelle) (`PIC_RECUL`) · 🔢 Rang de machine sur la Réglette 1–6 (`PIC_RANG_MACHINE`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) |
| **Résumé plateau** | Les machines de son rang marchent à reculons |
| **Mots-clés Face 1** | Loi · à son rang Devant = derrière · avancée = recul · Sur place sans gain de Rouge |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Curupira — esprit protecteur de la forêt, petit être à la chevelure de flammes rouges et aux pieds tournés vers l’arrière
- **Pitch d’ambiance** : *Le Curupira protège les bêtes et punit qui abat trop d’arbres. Ses pieds tournés à l’envers laissent des traces qui égarent les chasseurs : qui croit le suivre s’éloigne de lui, et retourne d’où il vient.*
- **Brief illustration** : Sentier boueux au crépuscule : le Curupira, chevelure flamboyante, court en sens inverse de ses propres empreintes ; des chenilles de machine suivent ces traces et reculent vers la lisière ; derrière lui, un jaguar et un tapir l’observent, à l’abri. Rouges flamme, verts sombres, boue ocre.
- **Règle — Face 1** :
> Loi passive — Pieds à l’envers (tant que le Curupira est sur la Réglette, défendu ou non) : toute machine non annulée qui attaque depuis le rang du Curupira marche à reculons. Sa frappe « Devant » vise la parcelle située derrière elle, côté bordure (en sautant les Routes Forestières ; s’il n’y en a aucune, la frappe se perd). L’avancée d’« En avançant » devient un recul d’1 parcelle. Une frappe « Sur place » depuis ce rang ne fait gagner aucun Rouge en Mode Charge. Protecteur des bêtes : quand une machine recule ainsi hors de la parcelle qui porte le jeton Duel face Défi, retournez le Duel sur Territoire tenu. Comme tout Rêve défendu, le Curupira annule à son rang 1 machine par Défenseur : à vous de choisir celles que vous laissez marcher à reculons.
- **Décision (Choix)** : Annuler une machine de son rang, ou la laisser marcher à reculons : frappe derrière elle, puis recul d’1 parcelle.
- **Renoncement** : Une machine laissée active frappe quand même : derrière elle, une parcelle de bordure encore boisée peut y perdre ses Arbres.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `RANG_REVE`, `POSITION_REVE`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `DUEL`
- **Sorties (`I03`)** : `RECUL`, `TERRITOIRE` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Laisser marcher à reculons la machine dont la parcelle de derrière est une Route ou une clairière ; annuler en priorité celle dont la parcelle de derrière est la plus boisée.

**Témoins (2)**

- **`R7_T1`** (`A_CODER`) : Curupira au rang 3 (Acte 1, Charge) ; un Bulldozer en parcelle 2, non annulé, frappe la parcelle 2 puis la parcelle 1 (derrière), et recule en parcelle 1.
- **`R7_T2`** (`A_CODER`) : Abatteuse au rang 2 du Curupira, en parcelle 1 (aucune parcelle derrière elle) : sa frappe se perd.

---

<a id="frontiere-r-h-g9-r4"></a>
#### Frontière `R ↔ H` — Reptiles ↔ Humains (`G9` & `R4`)

> **Paire `panel_1`** · Divergence `I03` : `G9` → **`CALE`** vs `R4` → **`PISTON_REVES`** (✅ divergent, 0 boucle).

##### `G9` (`R>H` · GARDIEN) — Le Caïman noir, l’ombre sous la pirogue

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Caïman noir** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Sabotage** |
| **Pictogrammes** | 🧱 Cale sous machine mobile (Reptiles) (`PIC_CALE`) · 💥 Jeton Sabotage (sac opaque) (`PIC_SABOTAGE`) · 🥁 Chamane Tambour (Humains) (`PIC_TAMBOUR`) · ⏪ Recul de machine (−1 parcelle) (`PIC_RECUL`) |
| **Résumé plateau** | Tient une machine au fond des eaux noires |
| **Mots-clés Face 1** | Sabotage révélé → cale · machine tenue sans Ratissage · rayon Reptile, Humain ou du Tambour |
| **Mots-clés Face 2** | Cale partout · machine calée révélée = annulée · Sabotage rallumé |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Caïman noir (Melanosuchus niger) — grand crocodilien entier, dos cuirassé à fleur d’eau dans un lac d’eaux noires
- **Pitch d’ambiance** : *Le Caïman noir saisit et ne lâche plus : il tient sa proie contre le fond jusqu’à ce qu’elle cesse de lutter. Les pêcheurs le savent : dans les eaux noires, ce qu’il a pris ne remonte pas.*
- **Brief illustration** : Nuit sans lune sur un lac d’eaux noires : le Caïman noir entier, seuls ses yeux rouges et sa crête dorsale affleurent ; sa gueule agrippe la roue d’une machine embourbée sur la berge ; en arrière-plan, la proue sculptée d’une pirogue et la lueur d’un tambour. Noirs profonds, reflets rubis.
- **Règle — Face 1** :
> Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous une machine mobile du rayon Reptile, du rayon Humain ou du rayon où se trouve le Tambour (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile de ces rayons, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée est tenue : elle ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage (si elle termine le ménage sur la dernière parcelle, son jeton ne glisse pas sous elle). Quand son jeton Machine est révélé, la cale s’agite dans la séquence des Sabotages : allumez l’icône Sabotage, puis balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.
- **Règle — Face 2** :
> Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous n’importe quelle machine mobile (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage. La noyade : quand son jeton Machine est révélé, inclinez-le aussitôt (elle est annulée) ; puis, dans la séquence des Sabotages, la cale allume l’icône Sabotage et balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.
- **Décision (Choix)** : Quelle machine tenir : celle qui approche de la dernière parcelle (bloquer le Ratissage) ou celle qui menace la parcelle du Tambour.
- **Renoncement** : Le jeton pris en cale ne dilue plus le sac : chaque pioche suivante a plus de chances de réveiller une machine.
- **Double activation (Gardien)** : La première activation pose la cale (souvent sur le Sabotage qui vient d’allumer l’icône), la seconde traîne la machine calée d’1 parcelle vers la bordure ou déplace la cale vers une machine plus menaçante. Et chaque fois que la machine calée est révélée, la cale rallume Sabotage pour toute la Piste.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `SABOTAGE`, `ECAILLE` · **Entrées synergie (`I01`)** : `TAMBOUR`
- **Sorties (`I03`)** : `CALE`, `RECUL`, `ANNULATION` · **Déclencheurs amorcés** : `ICONE_SABOTAGE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Sabotage. Caler la machine mobile la plus proche de la dernière parcelle ; garder une Écaille plutôt qu’un Sabotage ordinaire pour la cale seulement si le Croc est déjà sur le plateau.

**Témoins (2)**

- **`G9_T1`** (`A_CODER`) : Un Sabotage est révélé ; le Caïman (sur Sabotage) s’active : cale sous l’Abatteuse du rayon H en parcelle 3 ; elle finit le ménage en parcelle 4 mais n’entre pas en Ratissage.
- **`G9_T2`** (`A_CODER`) : Tour suivant : le jeton de la machine calée est révélé : l’icône Sabotage s’allume ; en Face 2, la machine est en outre annulée.

##### `R4` (`H>R` · REVE) — La Pirogue-Anaconda des Ancêtres

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⚡ Twist 2K3 · 🌙 Levier Rêve

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Pirogue-Anaconda** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | ⚡ Brique-Twist 2K3 (`PIC_TWIST`) · ⬅️ Déplacement / avancée de Rêve (`PIC_AVANCEE_REVE`) · 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · 🦎 Jeton Sabotage Écaille (Reptiles) (`PIC_ECAILLE`) |
| **Résumé plateau** | Piston de Rêves qui pousse le convoi |
| **Mots-clés Face 1** | En queue · tout le convoi glisse d’1 ‖ Retour · échange avec le Rêve de droite ‖ mue = 1 Écaille au sac |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Vision mythique de la pirogue-serpent — l’anaconda géant dont le ventre porta les ancêtres en remontant le fleuve
- **Pitch d’ambiance** : *Au commencement, racontent les peuples du Rio Negro, les ancêtres remontèrent le fleuve dans le ventre d’un anaconda-pirogue, de halte en halte, jusqu’à devenir des hommes. La pirogue pousse encore les rêves vers l’amont.*
- **Brief illustration** : Fleuve cosmique au crépuscule : une immense pirogue dont la coque est le corps d’un anaconda, tête dressée à la proue, remonte le courant ; à son bord, d’autres Rêves lumineux comme des passagers ; dans son sillage, des écailles scintillantes tombent à l’eau. Bleus nuit, verts olive, éclats d’argent.
- **Règle — Face 1** :
> Quand ce Rêve est défendu, à sa résolution (après ses annulations), choisissez une manœuvre. Poussée : si la Pirogue est le Rêve le plus à droite de la Réglette, elle pousse tout le convoi : chaque Rêve, du plus à gauche au plus à droite (la Pirogue en dernier), glisse d’1 rang vers la gauche si ce rang est libre. Retour : la Pirogue échange sa place avec le premier Rêve situé à sa droite, même séparé d’elle par des rangs libres ; chacun garde ses Défenseurs, et ce Rêve, s’il n’a pas encore été résolu, se résout aussitôt depuis sa nouvelle place. Mue de l’anaconda : après chaque manœuvre, le joueur Reptile peut glisser 1 Écaille de sa réserve dans le sac.
- **Décision (Choix)** : Pousser le convoi entier (si la Pirogue est en queue) ou reculer en échangeant avec le Rêve de droite pour le faire remonter d’un coup.
- **Renoncement** : Le Retour éloigne la Pirogue vers les rangs rares et la détache du bloc du Sommeil ; tant qu’elle n’est pas en queue, elle ne peut pas pousser.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `RANG_REVE` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `PISTON_REVES`, `POSITION_REVE`, `ECAILLE` · **Déclencheurs amorcés** : — · **Paiement** : `P_RANG`
- **Heuristique bot** : Si la Pirogue est en queue, Poussée ; sinon Retour quand le Rêve de droite est défendu et qu’une machine révélée occupe le rang de la Pirogue.

**Témoins (2)**

- **`R4_T1`** (`A_CODER`) : Rêves aux rangs 3 et 4, Pirogue au rang 6 (rangs 1, 2 et 5 libres) : Poussée : Rêves aux rangs 2, 3 et Pirogue au rang 5 ; mue : 1 Écaille au sac.
- **`R4_T2`** (`A_CODER`) : Pirogue au rang 2, Rêve E au rang 5 non résolu : Retour : le Rêve E passe au rang 2 et se résout aussitôt, la Pirogue passe au rang 5.

---

<a id="frontiere-r-e-g10-r8"></a>
#### Frontière `R ↔ E` — Reptiles ↔ Entités Magiques (`G10` & `R8`)

> **Paire `panel_3`** · Divergence `I03` : `G10` → **`ECAILLE`** vs `R8` → **`RANG_REVE`** (✅ divergent, 0 boucle).

##### `G10` (`R>E` · GARDIEN) — La Matamata, Guetteuse des Feuilles Mortes

- **Provenance** : `panel_3.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Matamata** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Piégeage** |
| **Pictogrammes** | 🦎 Jeton Sabotage Écaille (Reptiles) (`PIC_ECAILLE`) · 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) · 🔵 Jeton Surchauffe Bleu (−1 tous modes) (`PIC_BLEU`) |
| **Résumé plateau** | Injecte Écaille, embusque Croc, altère |
| **Mots-clés Face 1** | +1 🦎 sac + [🦷 ciblé & 🔴→🔵 OU 🌀] |
| **Mots-clés Face 2** | +1 🦎/🔴→🔵 + 🦷 ciblé ET 🌀 |
| **Mots-clés Enraciné** | Standard (1 ou 2 Souches finales) |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Tortue matamata entière camouflée au fond d'un igarapé ouvrant sa large gueule
- **Pitch d’ambiance** : *« On croit marcher sur un lit de feuilles mortes ; déjà le vide s'est ouvert sous l'acier et la vase glacée l'aspire. »*
- **Brief illustration** : Indiscernable d'un amas d'écorces sombres et de feuilles mortes au fond d'un igarapé peu profond, une tortue matamata entière ouvre brusquement sa large gueule triangulaire dans un remous spectral qui fige les rouages d'un engin.
- **Règle — Face 1** :
> Lorsque La Matamata s'active :
> 1. Mue de Vase : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque.
> 2. Gueule Aspirante : choisissez 1 seule des deux manœuvres suivantes :
> • Happer la Proie : si le jeton Croc est dans la réserve Reptile, posez-le sur n'importe quelle parcelle ciblée (par une machine qui n'a pas encore frappé à ce tour, mobile ou en Ratissage) ; en outre, si une machine ciblant cette parcelle porte déjà un jeton d'Altération ou possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
> • Vase Hallucinogène : posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération ; si le jeton Croc se trouve déjà sur le plateau sur une parcelle non ciblée, vous pouvez le déplacer sur une parcelle ciblée de ce rayon.
- **Règle — Face 2** :
> Lorsque La Matamata s'active :
> 1. S'il reste au moins 1 jeton Écaille chez les Reptiles, glissez-le dans le sac opaque ; si les 4 Écailles sont déjà sorties, retournez 1 jeton Rouge existant d'une machine du plateau sur sa face Bleue Surchauffe.
> 2. Résolvez les deux effets de Gueule Aspirante dans l'ordre de votre choix : déployez (ou repositionnez depuis une parcelle non ciblée) le Croc sur une parcelle ciblée avec son retournement Rouge → Bleu, ET posez 1 jeton d'Altération sur une machine mobile sans Altération (si toutes les machines mobiles sont déjà altérées, retournez 1 jeton Rouge existant → Bleu Surchauffe sur une machine altérée).
- **Décision (Choix)** : En Face 1, choisir Happer la Proie pour recycler aussitôt le Croc et allumer Piégeage (en synergie avec R8), ou Vase Hallucinogène pour neutraliser le tour suivant par Altération.
- **Renoncement** : En Face 1, les deux manœuvres s'excluent mutuellement : sécuriser le tour courant via le Croc renonce à l'Altération préventive du tour suivant.
- **Double activation (Gardien)** : Posée sur Piégeage, La Matamata excelle en double mise : dès qu'un premier Piège ou le Croc pare une attaque (le Croc regagnant aussitôt la réserve Reptile avant le balayage), sa 1re activation redéploie immédiatement le Croc sur une seconde parcelle ciblée plus tard dans l'ordre des rangs ; lorsque ce Croc pare à son tour, il rallume Piégeage et déclenche tout seul la 2nde activation de La Matamata.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `ECAILLE`, `CROC`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `ALTERATION`, `ROUGE`
- **Sorties (`I03`)** : `ECAILLE`, `CROC`, `ALTERATION`, `BLEU` · **Déclencheurs amorcés** : `ICONE_PIEGEAGE`, `ICONE_SABOTAGE` · **Paiement** : `P_PARI`
- **Heuristique bot** : Siéger sur Piégeage avec 2 paris. Dès que le Croc revient en réserve, choisir Happer la Proie pour le reposer sur la prochaine parcelle ciblée afin d'auto-chaîner la 2nde activation.

**Témoins (1)**

- **`G10_T1`** (`A_CODER`) : Tour 3, La Matamata Face 1 sur Piégeage (2 paris). Au rang 2, le Croc pare une Abatteuse (rentre en réserve, allume Piégeage) : 1re activation → +1 Écaille au sac + Happer la Proie repose le Croc devant le Bulldozer du rang 5 (Rouge → Bleu). Au rang 5, le Croc pare et rallume Piégeage : 2nde activation (Face 2) → +1 Écaille + Vase Hallucinogène altère le Bulldozer.

##### `R8` (`E>R` · REVE) — Le Rêve de la Mue d’Obsidienne

- **Provenance** : `panel_3.json` · **Nature** : `LOI_PASSIVE` · **Rôles** : ⚖️ Loi passive · 🌙 Levier Rêve

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Mue d’Obsidienne** |
| **Fenêtre / Icône** | `PERMANENT` |
| **Pictogrammes** | ⚖️ Loi passive permanente (`PIC_LOI_PASSIVE`) · 🦎 Jeton Sabotage Écaille (Reptiles) (`PIC_ECAILLE`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) · 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) |
| **Résumé plateau** | Écailles glissent rêves · Croc refroidit |
| **Mots-clés Face 1** | Passif : 🦎/Défendu → Glisse 1G & 🌀 · 🦷 pare → 🔴→🔵 (sinon ⏪ 1) |
| **Mots-clés Enraciné** | Standard (1 Souche finale, bloque Sommeil) |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Mue translucide d'obsidienne d'un grand serpent enroulée autour d'une lame givrée
- **Pitch d’ambiance** : *« Le reptile abandonne son ancienne peau aux esprits de la nuit ; quiconque y mord sent le gel remonter jusqu'au cœur du moteur. »*
- **Brief illustration** : Suspendue entre deux troncs noirs baignés de lueurs violettes, la mue translucide et tranchante comme du verre volcanique d'un grand serpent s'enroule autour d'une lame de scie couverte de givre bleu.
- **Règle — Face 1** :
> Tant que ce Rêve occupe un rang de la Réglette (même sans Défenseur posé sur lui) :
> • Piston d'Écaille (À l'ouverture) : chaque fois qu'un jeton Écaille est révélé à l'ouverture des paravents — ainsi que lorsque ce Rêve lui-même est défendu à sa résolution d'ouverture — faites glisser 1 Rêve en jeu de votre choix (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
> • Venin d'Obsidienne (Aux attaques) : chaque fois que le jeton Croc Reptile pare la frappe d'une machine (juste avant que le Croc ne regagne la réserve Reptile) : si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge) et qu'elle est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).
- **Décision (Choix)** : Laisser R8 sans Défenseur pour profiter passivement des Écailles et du Croc tout en économisant des poses, ou le défendre activement pour garantir un glissement et une Altération même sans Écaille tirée.
- **Renoncement** : Défendre R8 immobilise un Défenseur sur la Réglette ; le laisser vide renonce à l'annulation sur son rang et au déclenchement garanti lors des tours sans Écaille.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `ALTERATION`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `ECAILLE`, `CROC`, `ROUGE`
- **Sorties (`I03`)** : `RANG_REVE`, `ALTERATION`, `BLEU`, `RECUL` · **Déclencheurs amorcés** : `ICONE_REVE` · **Paiement** : —
- **Heuristique bot** : Construire R8 tôt avec des Écailles au sac (via G10/M2) pour générer glissements de Rêves et Altérations sans consommer de Défenseur ; le défendre si son rang porte une menace.

**Témoins (1)**

- **`R8_T1`** (`A_CODER`) : Tour 5, R8 non défendu au rang 4, un autre Rêve au rang 3. Une Écaille révélée pose le Croc en parcelle 3 de R et déclenche Piston d'Écaille (Rêve 3 → 2 + Altération sur une Abatteuse). Aux attaques, un Bulldozer sans Rouge est paré par le Croc : Venin d'Obsidienne le recule en parcelle 2 avant le retour du Croc en réserve.

---

<a id="frontiere-o-h-g11-r5"></a>
#### Frontière `O ↔ H` — Oiseaux ↔ Humains (`G11` & `R5`)

> **Paire `panel_2`** · Divergence `I03` : `G11` → **`DEFENSEUR_REDEPLOYE`** vs `R5` → **`RANG_MACHINE`** (✅ divergent, 0 boucle).

##### `G11` (`O>H` · GARDIEN) — La Harpie féroce

- **Provenance** : `panel_2.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Harpie féroce** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Parade** |
| **Pictogrammes** | 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) · 🔢 Rang de machine sur la Réglette 1–6 (`PIC_RANG_MACHINE`) · 🛡️ Défenseur (`PIC_DEFENSEUR`) · 🎶 Chamane Chant (Humains) (`PIC_CHANT`) |
| **Résumé plateau** | Oiseau au sol / Oiseau sur jeton Machine · miroir → Chamane au Rêve |
| **Mots-clés Face 1** | Fondre ou saisir |
| **Mots-clés Face 2** | Piqué miroir |
| **Mots-clés Enraciné** | Ordinaire |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : La Harpie féroce entière plongeant sous la voûte, ailes repliées entre deux troncs
- **Pitch d’ambiance** : *Au cri du guetteur, on regarde le ciel. L’ombre est déjà passée.*
- **Brief illustration** : La harpie entière plonge sous la voûte, ailes repliées juste assez pour passer entre deux troncs. Son ombre se referme sur un toit de tôle.
- **Règle — Face 1** :
> Fondre ou saisir (après ouverture des paravents). Prenez un Défenseur Oiseau disponible en forêt, sur une rive, un Rêve, une lisière ou en attente. Pour fondre, posez-le sur la parcelle d’une machine ou un pas radial devant elle, même si elle ne doit pas frapper ce tour. Pour saisir, choisissez une mobile à jouer au rang qu’indique votre Dé d’Envol. Laissez-le visible à l’ouverture, même sur un Sabotage. S’il sert de dé de machine, lisez sa face actuelle. Posez le Défenseur sur son jeton Machine révélé. La machine cesse aussitôt d’être active et perd toute son activation. Son jeton reste droit et visible pour la Furtivité, son dé lisible à son rang. Le pion engagé dans la saisie revient en main au ménage.
- **Règle — Face 2** :
> Piqué miroir. Vous pouvez fondre ou saisir comme en Face 1. Si la Plume indique le rang du Dé d’Envol ou son miroir (1↔4, 2↔5, 3↔6), les deux rangs s’ouvrent à la saisie. Après une saisie sur l’un des deux, vous pouvez porter un Chamane en forêt, depuis une parcelle que cette machine menaçait, sur un Rêve au rang miroir de la prise. Il y défendra le Rêve si sa lecture est encore à venir. Le rang lu est celui du dé au moment du piqué, après tout échange de R5.
- **Décision (Choix)** : Fondre au sol pour participer à plusieurs Parades, ou saisir un jeton Machine pour retirer toute son activation du tour ; en Face 2, monter le Chant sur le Rêve miroir.
- **Renoncement** : L’Oiseau posé sur un jeton Machine ne défendra aucune autre frappe du tour ; monter le Chant peut vider la parcelle menacée par une seconde machine.
- **Double activation (Gardien)** : Un premier piqué met un Oiseau au sol pour une Parade. Au second, ce même pion peut saisir une autre menace. Deux saisies demandent deux Oiseaux disponibles.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `DE_ENVOL`, `PLUME`, `DEFENSEUR_ATTENTE`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `CHANT`, `POSITION_REVE`
- **Sorties (`I03`)** : `DEFENSEUR_REDEPLOYE`, `ANNULATION` · **Déclencheurs amorcés** : `ICONE_PARADE` · **Paiement** : —
- **Heuristique bot** : Saisir en priorité une mobile coûteuse au rang du Dé d’Envol (ou son miroir en Face 2 avec la Plume) ; à défaut, fondre avec un bâtisseur couché sur une parcelle menacée.

**Témoins (1)**

- **`G11_T1`** (`A_CODER`) : Dé d’Envol 3 visible, Plume sur 6. R5 échange les rangs 3 et 6 (le Bulldozer H·1 passe au rang 6 ; le Chant est en H·2). L’icône Rêve active G11 Face 2 : un Oiseau saisit le Bulldozer au rang 6 et porte le Chant sur un Rêve encore à lire au rang 3, qui annule l’autre mobile et glisse au rang 2 libre.

##### `R5` (`H>O` · REVE) — Le Ciel à deux eaux

- **Provenance** : `panel_2.json` · **Nature** : `ACTION` · **Rôles** : Brique fluide

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Ciel à deux eaux** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) · 🔢 Rang de machine sur la Réglette 1–6 (`PIC_RANG_MACHINE`) · 🦅 Perchoir de Vigie & Dé d’Envol (Oiseaux) (`PIC_PERCHOIR`) |
| **Résumé plateau** | Rangs miroirs · échange |
| **Mots-clés Face 1** | Rangs miroirs · échange |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Vision d’un ciel reflété dans le fleuve
- **Pitch d’ambiance** : *Les deux rives montrent le même ciel. Une seule voit l’orage arriver.*
- **Brief illustration** : Un bras de fleuve reflète deux horizons décalés sous une même ligne de pluie.
- **Règle — Face 1** :
> À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez échanger les rangs de deux machines visibles encore actives, distants exactement de trois. La Plume doit indiquer l’un de ces rangs. Si le Perchoir porte un jeton face cachée, une Plume au pied du rayon d’une des deux machines convient aussi. Laissez le jeton caché sur son Perchoir. Placez leurs dés de machine aux rangs échangés, sans déplacer leurs jetons de rayon. Chacune garde sa tactique imprimée mais change de mode. Les Rêves encore à résoudre lisent les nouveaux rangs.
- **Décision (Choix)** : Quelle machine doit passer en Charge et laquelle attaquera plus tôt ?
- **Renoncement** : Le changement de mode vaut pour les deux. Il peut renforcer la machine qu’on laisse en Assaut.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `PLUME`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `PERCHOIR`
- **Sorties (`I03`)** : `RANG_MACHINE` · **Déclencheurs amorcés** : `ICONE_REVE` · **Paiement** : —
- **Heuristique bot** : Échanger si la perte de force ou l’annulation de la machine la plus dangereuse dépasse le risque créé au rang opposé.

**Témoins (1)**

- **`R5_T1`** (`OK`) : Acte I, Plume en 1, une Abatteuse en 1 échange avec un Bulldozer chargé de Rouges en 4. Le Bulldozer passe en Charge sur place. L’Abatteuse passe en Assaut en 4 devant un Rêve encore à résoudre.

---

<a id="frontiere-o-e-g12-r9"></a>
#### Frontière `O ↔ E` — Oiseaux ↔ Entités Magiques (`G12` & `R9`)

> **Paire `panel_1`** · Divergence `I03` : `G12` → **`RANG_RELU`** vs `R9` → **`POSITION_REVE`** (✅ divergent, 0 boucle).

##### `G12` (`O>E` · GARDIEN) — L’Ibijau, les yeux fendus de la nuit

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil · ⚡ Twist 2K3

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **L’Ibijau** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Sabotage** |
| **Pictogrammes** | ⚡ Brique-Twist 2K3 (`PIC_TWIST`) · 🎲 Dés lancés sous paravent (`PIC_DES_PARAVENT`) · 🔢 Rang de machine sur la Réglette 1–6 (`PIC_RANG_MACHINE`) · 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) |
| **Résumé plateau** | Relit le dé écarté et pousse la machine vers un Rêve |
| **Mots-clés Face 1** | Machine révélée → rang de son dé écarté |
| **Mots-clés Face 2** | Ou dé ignoré d’un porteur de Sabotage · le Rêve qui l’annule glisse d’1 rang |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : L’Ibijau (Nyctibius griseus) — oiseau nocturne entier, figé à la verticale au bout d’une branche cassée, confondu avec elle
- **Pitch d’ambiance** : *Le jour, l’Ibijau n’est qu’un bout de branche morte. Pourtant il voit : deux fentes dans ses paupières closes guettent tout. La nuit, sa plainte descendante raconte, dit-on, l’histoire d’une jeune femme changée en oiseau, qui pleure encore celui qu’elle a perdu.*
- **Brief illustration** : Clair de lune : l’Ibijau entier, plumage d’écorce grise, se tient droit au sommet d’un chicot ; ses paupières sont closes mais deux fentes laissent filtrer un regard d’or ; sous lui, les paravents des joueurs laissent deviner des dés ; un Rêve violet flotte à l’horizon. Gris, or, violet.
- **Règle — Face 1** :
> Quand l’Ibijau s’active : ses paupières closes voient le dé écarté. Choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez le plus haut des deux dés standards du joueur qui a tiré son jeton : la machine quitte son rang et prend celui de ce dé (si les deux dés étaient égaux, rien ne change). Une machine ne peut jamais être déplacée vers un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement.
- **Règle — Face 2** :
> Quand l’Ibijau s’active : choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez l’un de ces dés : le plus haut des deux dés standards du joueur qui a tiré son jeton, ou n’importe lequel des deux dés d’un joueur qui a tiré un Sabotage ou une Écaille (des dés d’ordinaire ignorés). La machine quitte son rang et prend celui du dé lu, jamais un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement ; la complainte de l’urutau guide alors ce Rêve : s’il l’annule, il glisse ensuite d’1 rang vers la gauche si ce rang est libre.
- **Décision (Choix)** : Quelle machine relire : celle dont le dé écarté tombe pile sur un Rêve défendu, ou celle qu’il faut chasser d’un rang « Sur place » vers un rang moins nuisible.
- **Renoncement** : Le dé écarté est presque toujours plus haut : la machine relue peut atterrir sur un rang d’Assaut ou d’En avançant et frapper plus fort si aucun Rêve ne l’y attend.
- **Double activation (Gardien)** : Chaque Sabotage révélé rallume l’icône de l’Ibijau : deux activations poussent deux machines vers les Rêves de droite avant leur résolution. En Face 2, il puise aussi dans les dés « morts » des porteurs de Sabotage, ce qui lui offre presque toujours un rang utile.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `DES_SOUS_PARAVENT`, `RANG_MACHINE`, `POSITION_REVE` · **Entrées synergie (`I01`)** : `SABOTAGE`
- **Sorties (`I03`)** : `RANG_RELU`, `ANNULATION_INDUITE` · **Déclencheurs amorcés** : `ICONE_REVE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Sabotage. Relire la machine dont le dé écarté correspond à un Rêve défendu non résolu ; à défaut, ne pas relire vers un rang d’Assaut En avançant.

**Témoins (2)**

- **`G12_T1`** (`A_CODER`) : Bulldozer révélé au rang 1 (dés 1 et 5) ; Rêve E défendu au rang 5 ; l’Ibijau s’active au premier Sabotage : le Bulldozer passe au rang 5 puis est annulé par le Rêve (icône Rêve).
- **`G12_T2`** (`A_CODER`) : Dés égaux (3 et 3) : la machine reste au rang 3 ; en Face 2, l’Ibijau peut à la place lire le 6 d’un porteur de Sabotage.

##### `R9` (`E>O` · REVE) — La Matinta Pereira, siffleuse de minuit

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : 🌙 Levier Rêve

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Matinta Pereira** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) · ⬅️ Déplacement / avancée de Rêve (`PIC_AVANCEE_REVE`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) |
| **Résumé plateau** | Le Rêve vole là où siffle la Plume |
| **Mots-clés Face 1** | Vole de 2 rangs au plus vers la Plume · 0 annulation = 1 Altération |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : La Matinta Pereira — vieille sorcière de la forêt qui prend la forme d’un oiseau noir au sifflement strident
- **Pitch d’ambiance** : *Le sifflement de la Matinta semble venir de partout à la fois. Promettez-lui du tabac et elle s’en va ; refusez, et votre nuit sera maudite.*
- **Brief illustration** : Minuit sur un village sur pilotis : une vieille femme drapée de noir se dissout en un oiseau sombre qui s’élève en sifflant ; son vol trace une ligne lumineuse vers une plume posée près d’un rang de la Réglette ; sur un seuil, une offrande de tabac. Noirs, violets, argent lunaire.
- **Règle — Face 1** :
> Quand ce Rêve est défendu, à sa résolution, avant d’annuler : la Matinta vole vers le sifflement : si la Plume de Vigie est posée près d’un rang de la Réglette, déplacez ce Rêve, avec ses Défenseurs, d’au plus 2 rangs en direction de ce rang (sans le dépasser ni traverser un rang occupé), puis annulez-y normalement ; un Rêve ne se résout qu’une fois par ouverture. Malédiction : si ce Rêve n’annule finalement aucune machine, posez 1 jeton d’Altération sur une machine mobile de votre choix qui n’en porte pas.
- **Décision (Choix)** : Pour l’Oiseau : poser la Plume près du rang où il sait qu’une machine tombera (la sienne ou celle vue au Perchoir), ou près d’un rang qui compacte le bloc du Sommeil.
- **Renoncement** : Poser la Plume près d’un rang, c’est renoncer à l’utiliser au pied d’un rayon pour signaler Chaud ou Calme aux rives de Furtivité.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `PLUME`, `RANG_REVE` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `POSITION_REVE`, `ALTERATION` · **Déclencheurs amorcés** : `ICONE_REVE` · **Paiement** : —
- **Heuristique bot** : Côté Oiseau : poser la Plume près du rang de sa propre machine s’il est libre. Côté Entités : défendre la Matinta dès que la Plume est posée près d’un rang.

**Témoins (2)**

- **`R9_T1`** (`A_CODER`) : Matinta défendue au rang 4 ; la Plume est posée près du rang 2, libre, où l’Oiseau a révélé sa machine : le Rêve vole de 2 rangs jusqu’au rang 2 et l’annule.
- **`R9_T2`** (`A_CODER`) : Plume au pied d’un rayon (pas près d’un rang) et aucune machine au rang 6 : la Matinta n’annule rien et pose 1 Altération.

---

### C. Lisières Animal ↔ Essaim (3 lisières · 3 Gardiens + 3 Nids)

<a id="frontiere-m-i-g13-m1"></a>
#### Frontière `M ↔ I` — Mammifères ↔ Insectes (`G13` & `M1`)

> **Paire `panel_1`** · Divergence `I03` : `G13` → **`RIPOSTE_ESSAIM`** vs `M1` → **`INSECTE_PASSAGER`** (✅ divergent, 0 boucle).

##### `G13` (`M>I` · GARDIEN) — Le Tamanoir, le grand mangeur qui épargne

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Tamanoir** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Insecte** |
| **Pictogrammes** | 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) |
| **Résumé plateau** | Mange un peu, fait riposter beaucoup |
| **Mots-clés Face 1** | Nid à 2 Insectes ou plus · 1 Insecte mangé → riposte de 2 · sans Nid à éventrer : 1 Insecte de la réserve |
| **Mots-clés Face 2** | Riposte posée sur parcelle ciblée adjacente · parade aidée = Territoire tenu · sans Nid : idem |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier éventrant une termitière
- **Pitch d’ambiance** : *Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.*
- **Brief illustration** : Le Tamanoir (Myrmecophaga tridactyla), fourmilier géant entier, longue tête tubulaire et queue en panache, éventrant une termitière de sa griffe ; des soldats jaillissent déjà des galeries.
- **Règle — Face 1** :
> La récolte. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1 (le Tamanoir ne vide jamais un Nid). L’Essaim riposte aussitôt : ce Nid produit 2 Insectes, sans allumer d’icône ni appliquer son pouvoir de Nid. Ces Insectes restent sur le Nid et participent normalement aux parades sur sa parcelle.
> Termitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, le Tamanoir fouille une termitière sauvage : prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée, où il participe aux parades.
- **Règle — Face 2** :
> La garde dressée. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1. L’Essaim riposte : ce Nid produit 2 Insectes, sans allumer d’icône, que vous pouvez faire jaillir : posez-les sur la parcelle du Nid ou sur une parcelle ciblée adjacente (même rayon, ou même numéro d’un rayon voisin), où ils participeront aux parades. La garde dressée : si le jeton Duel se trouve sur l’une de ces parcelles, une parade aidée par ces Insectes y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère.
> Termitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée ; la garde dressée s’y applique.
- **Décision (Choix)** : Quel Nid éventrer — celui qui riposte le plus près de la frappe à venir, ou celui qu’il faut regonfler avant la Production.
- **Renoncement** : L’Insecte mangé manque à une déviation ou à un Bouclier de lisière ; un Nid réduit à 1 Insecte ne peut plus être éventré.
- **Double activation (Gardien)** : Deux éventrements, deux ripostes : soit deux Nids différents gonflent à la veille des frappes, soit le même Nid riposte deux fois. En Face 2, chaque riposte jaillit sur la parcelle menacée et fait allumer Insecte à la parade, l’icône du Tamanoir. Sans Nid à éventrer, la seconde termitière sauvage peut porter un Nid tout juste construit jusqu’à ses 2 Insectes.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `INSECTE`, `DUEL` · **Entrées synergie (`I01`)** : `NID`
- **Sorties (`I03`)** : `RIPOSTE_ESSAIM`, `INSECTE`, `TERRITOIRE` · **Déclencheurs amorcés** : `ICONE_INSECTE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Insecte (ou Parade en repli sans Nid). Éventrer le Nid le plus proche d’une parcelle visée ; en Face 2, faire jaillir la riposte sur la parcelle visée dont le déficit au Seuil est au plus 2.

**Témoins (2)**

- **`G13_T1`** (`A_CODER`) : Nid à 3 Insectes ; le Tamanoir s’active : 3 − 1 + 2 = 4 Insectes sur le Nid.
- **`G13_T2`** (`A_CODER`) : Plancher (Tour 2, aucun Nid construit) : la parcelle 2 du rayon M est visée au rang 4 (Assaut, Seuil 2) et gardée par 1 Défenseur. Après une parade au rang 1, le Tamanoir (sur Parade, icône de repli) fouille une termitière sauvage et pose 1 Insecte de la réserve sur cette parcelle ; au rang 4, parade réussie avec cet Insecte (icône Insecte).

##### `M1` (`I>M` · CROISSANCE) — Le Pelage du Paresseux

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : Brique fluide

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Pelage du Paresseux** |
| **Fenêtre / Icône** | `PRODUCTION` |
| **Pictogrammes** | 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) · ➡️ Migration / phorésie de l’Essaim (`PIC_MIGRATION`) · ⚔️ Jeton Duel — Défi / Territoire tenu (Mammifères) (`PIC_DUEL`) |
| **Résumé plateau** | Des passagers qui voyagent sur les machines |
| **Mots-clés Face 1** | 2 Insectes montent sur une machine voisine · sautent sur la parcelle frappée · descente au ménage |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Nid vivant — le pelage d’un paresseux à trois doigts, verdi d’algues, où vivent des papillons et de minuscules passagers
- **Pitch d’ambiance** : *La fourrure du paresseux est un monde : des algues, des champignons, des papillons qui n’existent nulle part ailleurs. Ces passagers voyagent sans bouger leurs ailes, et savent descendre au bon endroit.*
- **Brief illustration** : Gros plan sur un paresseux suspendu à une branche, sa fourrure verte d’algues grouillant de petits papillons et d’insectes ; certains s’envolent vers la chenille d’une machine qui passe sous l’arbre et s’y agrippent ; sur la parcelle voisine, le jeton Duel. Verts mousse, gris, ambre.
- **Règle — Face 1** :
> Production (quand ce Nid est défendu, après avoir produit) : les passagers embarquent : jusqu’à 2 Insectes de ce Nid montent, comme passagers, sur une machine mobile de sa parcelle ou d’une parcelle adjacente du même rayon, et voyagent avec elle. Quand cette machine frappe une parcelle, ses passagers peuvent sauter sur la parcelle frappée et y compter comme Insectes présents pour la parade. Si cette parcelle porte le jeton Duel, une parade aidée par un passager y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère. Au ménage, tout passager non dépensé descend sur place, sur la parcelle de sa machine.
- **Décision (Choix)** : Sur quelle machine embarquer : celle qui va frapper une parcelle à défendre, ou celle qui avance vers le cœur pour y déposer l’Essaim au ménage.
- **Renoncement** : Les passagers quittent le Nid : sa prochaine Production sera plus faible et sa parcelle perd ces renforts.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `NID`, `INSECTE` · **Entrées synergie (`I01`)** : `DUEL`
- **Sorties (`I03`)** : `INSECTE_PASSAGER`, `TERRITOIRE` · **Déclencheurs amorcés** : `ICONE_INSECTE` · **Paiement** : —
- **Heuristique bot** : Embarquer sur la machine révélée au rang le plus élevé (elle frappe tard, quand les autres parades sont connues) ; sinon sur celle qui avance vers le cœur.

**Témoins (2)**

- **`M1_T1`** (`A_CODER`) : 2 passagers sur le Bulldozer du rayon M ; il frappe la parcelle 3 (1 Défenseur, Seuil 3) : les 2 passagers sautent, parade avec Insectes (icône Insecte).
- **`M1_T2`** (`A_CODER`) : Un passager non dépensé ; sa machine termine en dernière parcelle : au ménage, il descend sur cette parcelle.

---

<a id="frontiere-r-i-g14-m2"></a>
#### Frontière `R ↔ I` — Reptiles ↔ Insectes (`G14` & `M2`)

> **Paire `panel_1`** · Divergence `I03` : `G14` → **`PONTE`** vs `M2` → **`PARADE_SOLDATS`** (✅ divergent, 0 boucle).

##### `G14` (`R>I` · GARDIEN) — Le Téju, la ponte au cœur de la termitière

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Téju** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Insecte** |
| **Pictogrammes** | 🦎 Jeton Sabotage Écaille (Reptiles) (`PIC_ECAILLE`) · 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) · 🪤 Piège autonome (`PIC_PIEGE`) |
| **Résumé plateau** | Pond une Écaille au cœur d’un Nid |
| **Mots-clés Face 1** | Écaille sous un Nid (sans Nid libre : au sol, rayon R ou I) · frappe → le Croc éclot et pare |
| **Mots-clés Face 2** | Le Croc éclot d’où qu’il soit et pare chaque frappe jusqu’au ménage |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Téju (Tupinambis teguixin), grand lézard entier noir et doré griffant une termitière
- **Pitch d’ambiance** : *La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.*
- **Brief illustration** : Le Téju (Tupinambis teguixin), grand lézard entier à la robe noire et dorée, griffant la paroi d’une termitière pour y pondre ; à ses pieds, la litière de feuilles où s’enfouissent les pontes sans abri.
- **Règle — Face 1** :
> La ponte. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. Éclosion : quand une machine frappe la parcelle de ce Nid et que le Croc est dans la réserve Reptile, la ponte éclot avant toute parade : postez le Croc sur cette parcelle ; il pare cette frappe en premier (allumez Piégeage) puis regagne la réserve, et l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
> Ponte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, le Téju pond dans la litière : posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte. Elle éclot de la même façon quand une machine frappe cette parcelle, et regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois : pondre de nouveau au sol la déplace.
- **Règle — Face 2** :
> La nichée. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. La nichée : quand une machine frappe la parcelle de ce Nid, la ponte éclot avant toute parade : postez le Croc sur cette parcelle, où qu’il se trouve (réserve Reptile ou autre parcelle) ; il pare cette frappe en premier (allumez Piégeage) et, au lieu de regagner la réserve, reste sur place pour parer de même chaque frappe suivante sur cette parcelle jusqu’au ménage, où il regagne la réserve tandis que l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
> Ponte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte : la nichée y éclot de la même façon, et l’Écaille regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois.
- **Décision (Choix)** : Sous quel Nid pondre — celui dont la parcelle est visée ce tour, ou un Nid exposé à long terme près du cœur ; sans Nid, quelle parcelle couver.
- **Renoncement** : L’Écaille couvée n’est plus dans le sac tant qu’elle n’a pas éclos (moins de Sabotages tirés) ; un Croc parti éclore ne protège plus la parcelle où une Écaille l’avait posté.
- **Double activation (Gardien)** : Chaque activation installe une ponte sous un Nid différent : deux Nids protégés, deux éclosions possibles, deux icônes Piégeage. En Face 2, une seule ponte suffit à tenir une parcelle pendant toute la phase d’attaques. Sans Nid, la seconde activation déplace la ponte au sol vers la parcelle la plus menacée.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `ECAILLE`, `CROC` · **Entrées synergie (`I01`)** : `NID`
- **Sorties (`I03`)** : `PONTE`, `CROC`, `ECAILLE` · **Déclencheurs amorcés** : `ICONE_PIEGEAGE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Insecte (ou Parade en repli sans Nid). Pondre sous le Nid dont la parcelle est visée par une machine révélée ; sinon sous le Nid le plus proche du cœur, ou en ponte au sol sur une parcelle menacée de R ou I.

**Témoins (2)**

- **`G14_T1`** (`A_CODER`) : Ponte sous le Nid de la parcelle 2 du rayon I ; le Bulldozer frappe cette parcelle ; le Croc est en réserve : éclosion, parade du Croc (Piégeage), Écaille au sac.
- **`G14_T2`** (`A_CODER`) : Plancher (Tour 2, aucun Nid construit) : après une parade au rang 1, le Téju (sur Parade, icône de repli) pond au sol 1 Écaille face cachée au bord de la parcelle 2 du rayon R. Au rang 4, l’Abatteuse frappe cette parcelle : éclosion du Croc (Piégeage) puis retour en réserve et Écaille au sac.

##### `M2` (`I>R` · CROISSANCE) — La Termitière-Forteresse

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : Brique fluide

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Termitière-Forteresse** |
| **Fenêtre / Icône** | `PRODUCTION` |
| **Pictogrammes** | 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) · 🦎 Jeton Sabotage Écaille (Reptiles) (`PIC_ECAILLE`) · 🦷 Croc Reptile (réutilisable) (`PIC_CROC`) |
| **Résumé plateau** | Forteresse d’argile et soldats à glu |
| **Mots-clés Face 1** | 2 Insectes du Nid parent seuls toute frappe · Production = 1 Écaille au sac ou Croc posté |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Nid vivant — une termitière de terre cuite au soleil, hérissée de cheminées, défendue par des soldats à tête-seringue
- **Pitch d’ambiance** : *Le mur de la termitière est plus dur que la brique. Ses soldats, la tête en forme de seringue, projettent une glu qui colle tout ce qui ose y toucher. Les reptiles le savent : il n’est pas d’abri plus sûr.*
- **Brief illustration** : Une termitière haute comme un homme, parois ocres striées, cheminées fumantes ; à sa base, des soldats à tête en pointe projettent une glu luisante sur la chenille d’une machine ; un lézard se chauffe au sommet ; quelques écailles d’argile brillent sur la paroi. Ocres, rouilles, éclats dorés.
- **Règle — Face 1** :
> Les soldats (quand une machine frappe la parcelle de ce Nid) : avant la parade classique, vous pouvez défausser 2 Insectes de ce Nid ; ils parent cette frappe à eux seuls, quel que soit le Seuil de Parade (allumez l’icône Insecte). Argile d’écailles (à la Production, quand ce Nid est défendu, après avoir produit), choisissez : le joueur Reptile glisse 1 Écaille de sa réserve dans le sac ; ou, si le Croc est dans la réserve Reptile et qu’une machine mobile se trouve sur la parcelle de ce Nid, postez le Croc sur cette parcelle.
- **Décision (Choix)** : Faire tenir la termitière par ses soldats (2 Insectes par frappe) ou garder ces Insectes pour produire et migrer.
- **Renoncement** : Chaque défense des soldats vide le Nid de 2 Insectes et affaiblit sa prochaine Production ; une Écaille glissée au sac ne servira plus aux pontes du Téju.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `NID`, `INSECTE` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `PARADE_SOLDATS`, `ECAILLE`, `CROC` · **Déclencheurs amorcés** : `ICONE_INSECTE`, `ICONE_PIEGEAGE` · **Paiement** : —
- **Heuristique bot** : Faire parer les soldats quand le Seuil de la frappe dépasse Défenseurs + Insectes disponibles ; à la Production, poster le Croc si une machine mobile partage la parcelle.

**Témoins (2)**

- **`M2_T1`** (`A_CODER`) : Nid à 3 Insectes en parcelle 2 ; une Abatteuse en Mode Assaut à 2 Rouges y frappe (Seuil 4) sans aucun Défenseur : 2 Insectes défaussés, frappe parée, icône Insecte.
- **`M2_T2`** (`A_CODER`) : Production défendue, aucune machine sur la parcelle : le joueur Reptile glisse 1 Écaille au sac.

---

<a id="frontiere-o-i-g15-m3"></a>
#### Frontière `O ↔ I` — Oiseaux ↔ Insectes (`G15` & `M3`)

> **Paire `panel_1`** · Divergence `I03` : `G15` → **`INSECTE_TRANSPORTE`** vs `M3` → **`NID_NOMADE`** (✅ divergent, 0 boucle).

##### `G15` (`O>I` · GARDIEN) — Le Colibri, porteur de gouttes et de pollen

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⭐ Éveil · 🌱 Enracinement

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Colibri** |
| **Fenêtre / Icône** | `ACTIVATION` · Icône conseillée : **Parade** |
| **Pictogrammes** | 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) · ➡️ Migration / phorésie de l’Essaim (`PIC_MIGRATION`) · 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🌱 Enracinement volontaire (`PIC_ENRACINEMENT`) |
| **Résumé plateau** | Transporte l’Essaim à vol d’oiseau |
| **Mots-clés Face 1** | 1 Insecte pris n’importe où → n’importe quelle parcelle · aucun Insecte en jeu = 1 de la réserve |
| **Mots-clés Face 2** | 2 Insectes · arrivée sur un Nid = +1 Insecte · Plume près d’un rang = dépôt sur la Réglette |
| **Mots-clés Enraciné** | Fin de partie : tuiles enracinées voisines, 1 repousse de plus |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Le Colibri (Phaethornis), minuscule oiseau entier en vol stationnaire devant une fleur d’héliconia
- **Pitch d’ambiance** : *Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.*
- **Brief illustration** : Le Colibri (Phaethornis, ermite des sous-bois), animal entier : minuscule oiseau en vol stationnaire devant une fleur d’héliconia ; dans la lumière rasante, on devine les acariens des fleurs qui voyagent dans ses narines, de corolle en corolle.
- **Règle — Face 1** :
> Le porteur de gouttes. Quand le Colibri s’active, il emporte un passager : déplacez 1 Insecte depuis n’importe quel Nid, parcelle, rang de la Réglette ou icône de la Piste des Gardiens vers n’importe quelle parcelle de n’importe quel rayon. Il y participe normalement aux parades (une parade aidée par un Insecte allume l’icône Insecte).
> Amorçage — narines fleuries (plancher) : s’il n’y a encore aucun Insecte en jeu, le Colibri en rapporte un des fleurs : prenez-le dans la réserve de l’Essaim.
- **Règle — Face 2** :
> La tournée. Quand le Colibri s’active, il fait sa tournée : déplacez jusqu’à 2 Insectes, pris n’importe où (Nid, parcelle, rang de la Réglette, icône de la Piste des Gardiens), vers une ou deux parcelles de n’importe quels rayons, où ils participent aux parades. S’il n’y a encore aucun Insecte en jeu, le premier vient de la réserve de l’Essaim.
> Pollinisation : si l’un d’eux arrive sur un Nid, ce Nid produit aussitôt 1 Insecte, sans allumer d’icône ni appliquer son pouvoir de Nid.
> Fleur signalée : si la Plume de Vigie est posée près d’un rang de la Réglette, vous pouvez déposer l’un de ces passagers sur ce rang plutôt que sur une parcelle : il y servira à une déviation, une lanterne ou un rite.
- **Règle — Enraciné** :
> La part du colibri. Au décompte final, chaque autre tuile enracinée au pied de son rayon ou d’un rayon voisin fait repousser 1 Souche de plus.
- **Décision (Choix)** : Quel Insecte déplacer, et d’où — vider un rang, un Nid ou une icône pour compléter une parade imminente ; en Face 2, faire escale sur un Nid pour le polliniser, ou déposer un passager là où siffle la Plume.
- **Renoncement** : Chaque Insecte emporté laisse un trou ailleurs (une déviation, une Production plus faible, un Bouclier de lisière en moins) ; un passager posé sur la Réglette ne pare rien ce tour-ci.
- **Double activation (Gardien)** : Une goutte par activation : la première complète la parade d’une frappe imminente, la seconde ravitaille une autre parcelle ou, en Face 2, pollinise un Nid qui produira +2 à sa prochaine Production. Chaque parade aidée allume Insecte et relance la Piste.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `PLUME` · **Entrées synergie (`I01`)** : `INSECTE`, `NID`
- **Sorties (`I03`)** : `INSECTE_TRANSPORTE`, `INSECTE`, `INSECTE_RANG`, `ARBRE` · **Déclencheurs amorcés** : `ICONE_INSECTE` · **Paiement** : —
- **Heuristique bot** : Siéger sur Parade. Transporter l’Insecte (ou amorcer depuis la réserve) vers la parcelle visée non résolue dont le déficit au Seuil est exactement 1 ; en Face 2, polliniser un Nid à 1 Insecte ou alimenter la Réglette via la Plume ; enraciner en fin de partie si deux tuiles voisines sont déjà enracinées.

**Témoins (2)**

- **`G15_T1`** (`A_CODER`) : Amorçage (Tour 2, aucun Nid construit, aucun Insecte en jeu) : la parcelle 3 du rayon M est visée au rang 4 (Seuil 3) et gardée par 2 Défenseurs. Après une parade au rang 1, le Colibri (sur Parade) apporte 1 Insecte de la réserve sur cette parcelle ; au rang 4, parade réussie avec cet Insecte défaussé (icône Insecte).
- **`G15_T2`** (`A_CODER`) : Pollinisation (Face 2) : un Nid porte 1 Insecte en parcelle 2 du rayon I et 1 Insecte attend sur le rang 4. Le Colibri porte ce dernier sur le Nid (2 Insectes → pollinisation +1 = 3 Insectes), puis porte un second passager depuis l’icône Insecte vers la parcelle 3 du rayon O visée au rang 5.

##### `M3` (`I>O` · CROISSANCE) — Le Bivouac des Légionnaires

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : ⚡ Twist 2K3

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Bivouac des Légionnaires** |
| **Fenêtre / Icône** | `PRODUCTION` |
| **Pictogrammes** | ⚡ Brique-Twist 2K3 (`PIC_TWIST`) · 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · ➡️ Migration / phorésie de l’Essaim (`PIC_MIGRATION`) · 🪶 Plume de Vigie — Chaud / Calme (Oiseaux) (`PIC_PLUME`) |
| **Résumé plateau** | Un Nid nomade qui suit la Plume |
| **Mots-clés Face 1** | Chaque Production · le Nid se déplace d’1 parcelle (2 vers la Plume) · raid de 2 Insectes |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Nid vivant nomade — le bivouac des fourmis légionnaires, boule de centaines de milliers de corps entrelacés suspendue sous un tronc
- **Pitch d’ambiance** : *Le bivouac n’a pas de murs : ce sont les fourmis elles-mêmes, accrochées les unes aux autres. Chaque nuit, la colonne repart ; et derrière son front de raid, les oiseaux fourmiliers suivent, guettant ce qui s’enfuit.*
- **Brief illustration** : Aube : sous un tronc couché, une masse vivante de fourmis légionnaires forme des chambres et des couloirs de leurs propres corps ; une colonne s’étire déjà vers la parcelle voisine ; au-dessus, des oiseaux fourmiliers suivent le front de raid, et une plume de vigie est plantée au bout du chemin. Bruns rouges, noirs, lumière rasante.
- **Règle — Face 1** :
> Nid nomade (à chaque Production, avant de produire, que ce Nid soit défendu ou non) : le bivouac lève le camp : déplacez ce Nid, avec ses Insectes, vers une parcelle libre (sans machine ni autre Nid) adjacente : sur le même rayon, ou à la parcelle de même numéro d’un rayon voisin. Si ce déplacement le rapproche du rayon désigné par la Plume de Vigie, ou le garde sur ce rayon, il peut enchaîner 2 parcelles adjacentes libres au lieu d’1 : les oiseaux fourmiliers guident la colonne. Puis, s’il est défendu à sa nouvelle place, il produit normalement. Front de raid (après la production) : jusqu’à 2 Insectes du bivouac peuvent se poster sur une parcelle adjacente visée par une machine révélée, où ils participeront aux parades.
- **Décision (Choix)** : Où lever le camp : vers la parcelle menacée pour y lancer le raid, ou loin d’un Bulldozer qui menace d’en faire une Route.
- **Renoncement** : Le bivouac qui quitte la parcelle de son Défenseur ne produit pas ; et un Nid qui s’approche des machines risque d’être renvoyé en lisière.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `NID`, `INSECTE` · **Entrées synergie (`I01`)** : `PLUME`
- **Sorties (`I03`)** : `NID_NOMADE`, `INSECTE` · **Déclencheurs amorcés** : `ICONE_INSECTE` · **Paiement** : —
- **Heuristique bot** : Lever le camp vers une parcelle visée adjacente qui porte un Défenseur (pour produire) ; fuir toute parcelle réduite à 1 pièce visée par un Bulldozer.

**Témoins (2)**

- **`M3_T1`** (`A_CODER`) : Bivouac en parcelle 1 du rayon I ; la Plume est au pied du rayon O voisin : le Nid passe en parcelle 1 du rayon O puis en parcelle 2 (2 pas vers la Plume) ; défendu là, il produit.
- **`M3_T2`** (`A_CODER`) : Front de raid : 2 Insectes du bivouac se postent sur la parcelle 3 visée du rayon O.

---

### D. Triangle Autonome A = 0 `{H, E, I}` (3 lisières · 4 Rêves + 2 Nids)

<a id="frontiere-h-e-r1-r2"></a>
#### Frontière `H ↔ E` — Humains ↔ Entités Magiques (`R1` & `R2`)

> **Frontière hybride `panel_1` × `panel_2`** · Divergence `I03` : `R1` → **`REVE_COMPACTE`** vs `R2` → **`ALTERATION`** (✅ divergent, 0 boucle).

##### `R1` (`H>E` · REVE) — La Liane des Esprits

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : 🔓 A=0 · 🌙 Levier Rêve · 🌱 Enracinement

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Liane des Esprits** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · ⬅️ Déplacement / avancée de Rêve (`PIC_AVANCEE_REVE`) · 🚫 Machine annulée (jeton incliné 90°) (`PIC_ANNULATION`) · 🌱 Enracinement volontaire (`PIC_ENRACINEMENT`) |
| **Résumé plateau** | Tire un Rêve des Entités contre elle |
| **Mots-clés Face 1** | Rêve des Entités tiré contre la Liane · collé = la paire glisse à gauche · aucun à droite = la Liane grimpe d’1 rang, sinon serre 1 machine de plus |
| **Mots-clés Enraciné** | Enracinée sans fermer le Sommeil |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Vision chamanique de l’ayahuasca : une liane torsadée reliant le monde des hommes à celui des esprits
- **Pitch d’ambiance** : *On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.*
- **Brief illustration** : Vision chamanique de l’ayahuasca : une liane torsadée qui relie le monde des hommes à celui des esprits ; ses vrilles s’enroulent autour d’un rêve lumineux et l’attirent vers le chamane.
- **Règle — Face 1** :
> Quand ce Rêve est défendu, à sa résolution, après ses annulations : la liane s’enroule. Choisissez un Rêve des Entités situé plus à droite sur la Réglette. S’il reste au moins un rang libre entre eux, faites glisser ce Rêve jusqu’au rang libre qui touche la Liane (ses Défenseurs le suivent). S’il touche déjà la Liane, elle l’entraîne : la Liane glisse d’1 rang vers la gauche si ce rang est libre, et ce Rêve glisse d’1 rang à sa suite. Un Rêve déplacé qui n’a pas encore été résolu se résout ensuite depuis sa nouvelle place.
> La liane grimpe (plancher) : s’il n’y a aucun Rêve des Entités à sa droite, la Liane s’enroule sur elle-même : elle glisse d’1 rang vers la gauche si ce rang est libre (ses Défenseurs la suivent ; elle ne se résout pas une seconde fois). Si elle ne peut pas glisser (rang occupé, ou Liane déjà au rang 1), elle serre : elle annule 1 machine de plus sur son rang.
- **Règle — Enraciné** :
> La Liane nourrit encore les rêves : contrairement aux autres Rêves enracinés, elle ne rend pas le Sommeil impossible. Au décompte final, elle fait repousser 1 Souche comme toute tuile enracinée.
- **Décision (Choix)** : Tirer le Rêve des Entités pour combler un trou du bloc, ou faire glisser la paire vers le rang 1 ; seule, grimper vers le bloc ou serrer une machine de plus.
- **Renoncement** : Le Rêve tiré abandonne le rang qu’il couvrait ; une Liane qui grimpe quitte un rang où des machines pourraient encore tomber ; enraciner la Liane lui retire ce pouvoir mais garde le Sommeil possible.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `RANG_REVE` · **Entrées synergie (`I01`)** : —
- **Sorties (`I03`)** : `REVE_COMPACTE`, `POSITION_REVE`, `ANNULATION` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Tirer le Rêve E le plus à droite ; s’il est collé et que le rang de gauche est libre, faire glisser la paire ; seule, grimper vers le rang 1 ou serrer une 2e machine sur son rang. Enraciner la Liane en fin de partie sans craindre de fermer le Sommeil.

**Témoins (2)**

- **`R1_T1`** (`A_CODER`) : L’enroulement : Liane au rang 3 défendue, Rêve des Entités au rang 6, rangs 4 et 5 libres : le Rêve des Entités glisse au rang 4.
- **`R1_T2`** (`A_CODER`) : Plancher (Tour 2, aucun Rêve des Entités construit) : la Liane, au rang 6 avec 1 Défenseur, annule la machine de son rang puis grimpe au rang 5 ; plus tard, collée au rang 2 contre un Rêve Humain au rang 1 avec 2 machines et 1 Défenseur, elle en annule une puis serre la seconde.

##### `R2` (`E>H` · REVE) — Le Fleuve sous la cendre

- **Provenance** : `panel_2.json` · **Nature** : `ACTION` · **Rôles** : 🔓 A=0 · 🌱 Enracinement

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Fleuve sous la cendre** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🪵 Souche (retournable en Arbre) (`PIC_SOUCHE`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) · 🥁 Chamane Tambour (Humains) (`PIC_TAMBOUR`) · 🌱 Enracinement volontaire (`PIC_ENRACINEMENT`) |
| **Résumé plateau** | Tambour / Souches → Altération · ancrage marqué → Souche finale supplémentaire |
| **Mots-clés Face 1** | Lit sec · Marque |
| **Mots-clés Enraciné** | Gué marqué · Final |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Filet d’eau lumineuse rejoignant une souche sous un banc de cendre dans un méandre asséché
- **Pitch d’ambiance** : *Sous la cendre, l’eau se souvient du lit qu’elle occupait. Le premier arbre à boire lui rend son chemin.*
- **Brief illustration** : Un filet d’eau lumineuse rejoint une souche sous un banc de cendre, dans un méandre asséché.
- **Règle — Face 1** :
> À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez poser une Altération de la réserve sur une mobile sans Altération dans le rayon du Tambour en forêt, ou sur une mobile d’un rayon dont une parcelle ne porte que des Souches (à défaut, sur une mobile sans Altération de E ou H). Vous pouvez à la place relever le Tambour en attente sur un Rêve non défendu à droite de celui-ci. Il y participera à la résolution ordinaire.
- **Règle — Enraciné** :
> Gué marqué. À l’enracinement, si une machine mobile porte une Altération sur la parcelle désignée, vous pouvez tourner la Grande Carte d’un quart de tour, côté « Gué marqué » vers le haut. Ce repère conserve le droit au bonus, même après le départ de la machine. Le Sommeil se ferme dès l’ancrage. Au décompte final seulement, si la parcelle a survécu, retournez-y une Souche au titre de l’ancrage ordinaire, puis une autre si le gué est marqué. Chaque retournement exige une Souche encore présente.
- **Décision (Choix)** : Altérer une mobile grâce au Tambour ou aux Souches (ou sur E/H à défaut), relever le Tambour en attente sur un Rêve plus à droite, ou enraciner le Fleuve sur une parcelle altérée pour marquer le gué.
- **Renoncement** : Enraciner le Fleuve sur le gué abandonne ses deux usages actifs et ferme définitivement la voie du Sommeil.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `TAMBOUR`, `SOUCHE`, `DEFENSEUR_ATTENTE`
- **Sorties (`I03`)** : `ALTERATION`, `DEFENSEUR_REDEPLOYE`, `ARBRE` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Altérer une mobile avancée via le Tambour, une clairière de Souches ou le repli E/H ; relever le Tambour en attente sur un Rêve menacé à droite si disponible ; enraciner sur une parcelle altérée à ≥ 2 Souches lorsque le Sommeil est hors de portée.

**Témoins (1)**

- **`R2_T1`** (`A_CODER`) : À l’ouverture, le Tambour est en E·1 ; R2 défendu altère une mobile en E·3. Au ménage du Tour 5, elle s’y trouve encore avec son Altération et deux Souches. E enracine R2 devant E·3 et tourne sa Grande Carte (les Souches restent face Souche pendant la bataille). Au décompte final, si les deux Souches survivent, les deux deviennent Arbres en E·3.

---

<a id="frontiere-h-i-r6-m4"></a>
#### Frontière `H ↔ I` — Humains ↔ Insectes (`R6` & `M4`)

> **Paire `panel_1`** · Divergence `I03` : `R6` → **`ANNULATION_RENFORCEE`** vs `M4` → **`DEFENSEUR_REDEPLOYE`** (✅ divergent, 0 boucle).

##### `R6` (`H>I` · REVE) — Le Rite de la Tucandeira

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : 🔓 A=0

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **La Tucandeira** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) · 🚫 Machine annulée (jeton incliné 90°) (`PIC_ANNULATION`) |
| **Résumé plateau** | L’Essaim multiplie les annulations du Rêve |
| **Mots-clés Face 1** | 1 Insecte du rayon Humain → son rang (aucun en jeu : de la réserve) · chaque Insecte défaussé = 1 annulation de plus |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Gants tressés de fourmis tucandeiras portés lors d’une danse rituelle
- **Pitch d’ambiance** : *Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.*
- **Brief illustration** : Vision rituelle : les gants tressés de fourmis tucandeiras du rite de passage, portés par un jeune initié qui danse ; à ses pieds, les fourmis fraîchement cueillies en forêt.
- **Règle — Face 1** :
> Quand ce Rêve est défendu, à sa résolution : la cueillette : vous pouvez d’abord déplacer 1 Insecte d’une parcelle du rayon Humain vers le rang de ce Rêve.
> Amorçage — cueillette sauvage (plancher) : s’il n’y a encore aucun Insecte en jeu, prenez-le dans la réserve de l’Essaim.
> Puis le gant de tucandeiras : en plus d’1 machine par Défenseur, ce Rêve annule 1 machine supplémentaire de son rang pour chaque Insecte que vous défaussez de ce rang.
- **Décision (Choix)** : Combien d’Insectes offrir au gant — un par machine qui resterait sinon active sur le rang.
- **Renoncement** : Les Insectes consumés au rite ne dévieront plus de dés et ne pareront plus de frappes.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `INSECTE`, `ANNULATION` · **Entrées synergie (`I01`)** : `INSECTE_RANG`
- **Sorties (`I03`)** : `ANNULATION_RENFORCEE`, `INSECTE_RANG` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Défausser autant d’Insectes que de machines non couvertes au rang du Rêve (avec amorçage depuis la réserve si aucun Insecte n’est en jeu), en gardant 1 Insecte sur la Réglette si une déviation utile reste possible.

**Témoins (2)**

- **`R6_T1`** (`A_CODER`) : Rêve au rang 1 défendu par 1 Défenseur ; 3 machines au rang 1 et 2 Insectes sur ce rang : 3 machines annulées (1 + 2), 2 Insectes défaussés.
- **`R6_T2`** (`A_CODER`) : Plancher (Tour 2, aucun Nid construit, aucun Insecte en jeu) : le Rite, au rang 3, est défendu par 1 Défenseur face à 2 machines. Cueillette sauvage : 1 Insecte de la réserve sur le rang 3 ; le gant annule les 2 machines (1 + 1) et l’Insecte est défaussé.

##### `M4` (`I>H` · CROISSANCE) — Le Rucher des Mélipones

- **Provenance** : `panel_1.json` · **Nature** : `ACTION` · **Rôles** : 🔓 A=0

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Le Rucher des Mélipones** |
| **Fenêtre / Icône** | `PRODUCTION` |
| **Pictogrammes** | 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · ♻️ Défenseur en attente (bâtisseur / rive / Rêve) (`PIC_DEFENSEUR_ATTENTE`) · 🥁 Chamane Tambour (Humains) (`PIC_TAMBOUR`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) |
| **Résumé plateau** | Le miel relève les bâtisseurs |
| **Mots-clés Face 1** | 1 Insecte → 1 bâtisseur relevé sur le Nid ou le Tambour · deux fois au plus |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Nid vivant — une ruche d’abeilles sans dard (mélipones) logée dans un tronc creux, avec son tube d’entrée de cire
- **Pitch d’ambiance** : *Les mélipones n’ont pas de dard ; elles offrent leur miel aux peuples qui les protègent depuis des siècles. Une gorgée, et ceux qui ont bâti jusqu’à l’épuisement se relèvent pour défendre la forêt.*
- **Brief illustration** : Tronc creux au bord d’un jardin villageois : un tube de cire brune où entrent et sortent de petites abeilles sans dard ; un chamane y recueille une calebasse de miel ; à côté, deux bâtisseurs couchés se relèvent, revigorés. Miels ambrés, bruns, verts tendres.
- **Règle — Face 1** :
> Production (quand ce Nid est défendu, après avoir produit) : le miel des mélipones : défaussez 1 Insecte de ce Nid pour relever 1 Défenseur couché en attente (bâtisseur d’une tuile construite à ce tour) : son propriétaire le pose aussitôt, face Définitif, sur la parcelle de ce Nid ou sur la parcelle qui porte le Tambour, où il compte pour les parades. Vous pouvez recommencer une seconde fois en défaussant 1 autre Insecte.
- **Décision (Choix)** : Relever un bâtisseur (souvent celui qui vient d’achever une tuile) pour défendre le Nid ou la parcelle du Tambour.
- **Renoncement** : Chaque gorgée coûte un Insecte qui ne déviera ni ne parera ; et il faut avoir construit à ce tour pour avoir un bâtisseur à relever.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `NID`, `INSECTE`, `DEFENSEUR_ATTENTE` · **Entrées synergie (`I01`)** : `TAMBOUR`
- **Sorties (`I03`)** : `DEFENSEUR_REDEPLOYE`, `INSECTE` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Relever un bâtisseur dès que la parcelle du Nid ou du Tambour est visée avec un déficit de 1 au Seuil.

**Témoins (1)**

- **`M4_T1`** (`A_CODER`) : Un Rêve vient d’être construit par 2 bâtisseurs couchés ; Production du Rucher défendu : 1 Insecte défaussé, 1 bâtisseur posé sur la parcelle du Tambour.

---

<a id="frontiere-e-i-r10-m5"></a>
#### Frontière `E ↔ I` — Entités Magiques ↔ Insectes (`R10` & `M5`)

> **Paire `panel_3`** · Divergence `I03` : `R10` → **`RANG_REVE`** vs `M5` → **`ALTERATION`** (✅ divergent, 0 boucle).

##### `R10` (`E>I` · REVE) — La Transe de la Ruche Vagabonde

- **Provenance** : `panel_3.json` · **Nature** : `ACTION` · **Rôles** : 🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Ruche Vagabonde** |
| **Fenêtre / Icône** | `OUVERTURE` |
| **Pictogrammes** | ⬅️ Déplacement / avancée de Rêve (`PIC_AVANCEE_REVE`) · 🪹 Nid de l’Essaim (exclusif lisières de I) (`PIC_NID`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) · 🔵 Jeton Surchauffe Bleu (−1 tous modes) (`PIC_BLEU`) |
| **Résumé plateau** | Glisse rêve, déménage une ruche |
| **Mots-clés Face 1** | Glisse 1G + [Déplace 1 🪹 (+🐜 & 🛡️) partout & 🌀/🔴→🔵 OU +1 🐜 & +1 🌀] |
| **Mots-clés Enraciné** | Standard (1 Souche finale, bloque Sommeil) |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Immense ruche d'écorce vivante flottant dans la nuit portée par des filaments de brume
- **Pitch d’ambiance** : *« Guidé par le songe, le nid décroche ses racines d'écorce et traverse la nuit : quand l'acier frappe la clairière, la ruche est déjà derrière lui. »*
- **Brief illustration** : Portée par des filaments de brume violette à travers la nuit amazonienne, une immense ruche d'écorce vivante flotte entre les troncs avec toute sa nuée lumineuse pour venir se greffer juste devant la lame d'un engin surpris.
- **Règle — Face 1** :
> À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :
> 1. Sillage Onirique : faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).
> 2. Transhumance de la Ruche (Twist spatial) : choisissez 1 seul des deux effets suivants :
> • Envol de la Ruche (si au moins 1 Nid est en forêt) : déplacez 1 Nid construit — en emportant simultanément avec lui tous les Insectes et tous les Défenseurs présents sur sa parcelle — vers n'importe quelle autre parcelle dépourvue d'autre Nid sur n'importe quel rayon du plateau (y compris hors des rayons voisins des Insectes, et y compris sur une parcelle occupée par une machine). Ensuite, posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération du rayon rejoint — ou, sur une machine occupant la parcelle rejointe et possédant au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
> • Essaim Spectral (toujours disponible, y compris si aucun Nid n'est en forêt) : posez 1 jeton Insecte de la réserve sur une parcelle du rayon Entités ou du rayon Insectes (ou sur un rang 1–6 de la Réglette), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
- **Décision (Choix)** : Téléporter un Nid défendu et toute sa garnison directement devant une machine lointaine pour produire sur place à la Production puis parer aux attaques, ou choisir Essaim Spectral en solo.
- **Renoncement** : Déménager le Nid abandonne son ancien secteur et expose le Nid au renvoi en lisière si un Bulldozer transforme la parcelle rejointe en Route Forestière.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `POSITION_REVE`, `RANG_MACHINE` · **Entrées synergie (`I01`)** : `NID`, `INSECTE`, `ROUGE`
- **Sorties (`I03`)** : `RANG_REVE`, `NID_DEPLACE`, `ALTERATION`, `INSECTE`, `BLEU` · **Déclencheurs amorcés** : — · **Paiement** : `P_RANG`
- **Heuristique bot** : Glisser un Rêve chaque tour et téléporter un Nid garni directement sur la parcelle la plus menacée du plateau (en retournant un Rouge en Bleu) ; sans Nid en forêt, jouer Essaim Spectral.

**Témoins (1)**

- **`R10_T1`** (`A_CODER`) : Tour 4 (table {H, E, I}), M5 en parcelle 1 de I (1 Défenseur, 2 Insectes) tandis qu'un Bulldozer (1 Rouge, seuil 4) menace la parcelle 4 de H. R10 glisse du rang 3 au rang 2 libre puis choisit Envol de la Ruche : M5 atterrit en H·4 avec son Défenseur et ses 2 Insectes, retourne le Rouge en Bleu (seuil 4 → 2), produit +2 Insectes à la Production et pare aisément aux attaques.

##### `M5` (`I>E` · CROISSANCE) — Le Mycélium Luminescent, Réseau Spectral des Racines Noires

- **Provenance** : `panel_3.json` · **Nature** : `LOI_PASSIVE` · **Rôles** : 🔓 A=0 · ⚖️ Loi passive

**Mini-Tuile Plateau (`tuile_plateau`)**

| Champ | Contenu |
|---|---|
| **Nom court** | **Mycélium Luminescent** |
| **Fenêtre / Icône** | `PERMANENT` |
| **Pictogrammes** | ⚖️ Loi passive permanente (`PIC_LOI_PASSIVE`) · 🌙 Tuile Rêve sur la Réglette 1–6 (`PIC_REVE`) · 🌀 Jeton Altération (Entités) (`PIC_ALTERATION`) · 🐜 Jeton Insecte (exclusif lisières de I) (`PIC_INSECTE`) |
| **Résumé plateau** | Déviations vers rêves altèrent, recyclent |
| **Mots-clés Face 1** | Passif : Déviation ±1 vers 🌙 → +1 🌀 & recycle 🐜 sur M5 (si <2) · Production → 1 🐜 vers Réglette OU +1 🌀 |
| **Mots-clés Enraciné** | Standard (1 Souche finale) |

**Grande Carte Joueur (`carte_joueur`)**

- **Entité illustrée** : Entrelacs de champignons bioluminescents bleu-vert sous un grand arbre creux
- **Pitch d’ambiance** : *« Ce que l'insecte touche là-haut résonne aussitôt sous l'humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé. »*
- **Brief illustration** : Sous l'humus sombre d'un grand arbre creux colonisé par les insectes, un entrelacs de champignons bioluminescents bleu-vert relie les galeries souterraines jusqu'aux chenilles d'un bulldozer égaré dans une brume de spores.
- **Règle — Face 1** :
> Tant que ce Nid est en forêt (même sans Défenseur posé sur lui — et en plus de sa production standard +1 ou +2 lorsqu'il est défendu) :
> • Spores de Déviation (À l'ouverture) : chaque fois qu'un Insecte posé sur la Réglette est défaussé à l'ouverture pour décaler le dé d'une machine (±1) vers un rang portant un Rêve (défendu ou non), posez immédiatement 1 jeton d'Altération de la réserve Entités sur cette machine mobile si elle n'en porte pas encore (elle peut ensuite être annulée normalement si ce Rêve est défendu) ; de plus, si la parcelle de ce Nid contient alors strictement moins de 2 Insectes, replacez cet Insecte sur la parcelle de ce Nid au lieu de le remettre en réserve.
> • Filaments Oniriques (À la Production des Nids) : lorsque ce Nid est défendu à l'étape de Production, après sa production standard (+1 ou +2, avant la Migration), choisissez 1 effet : transférez directement 1 Insecte présent sur sa parcelle vers le rang 1–6 de votre choix de la Réglette, OU posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
- **Décision (Choix)** : Expédier 1 Insecte sur la Réglette à la Production pour amorcer la boucle Spores de Déviation (en restant sous 2 Insectes pour recycler gratuitement l'ouvrière), ou poser immédiatement 1 Altération directe.
- **Renoncement** : Rester sous 2 Insectes sur M5 maintient sa production à +1 au lieu de +2 ; dévier une machine vers un Rêve non défendu lui inflige une Altération mais ne l'annule pas à ce tour.

**Flux mécaniques & Bot**

- **Entrées plancher (`M4`)** : `NID_ACTIVE`, `INSECTE` · **Entrées synergie (`I01`)** : `INSECTE_RANG`, `POSITION_REVE`
- **Sorties (`I03`)** : `ALTERATION`, `INSECTE_RANG`, `INSECTE` · **Déclencheurs amorcés** : — · **Paiement** : —
- **Heuristique bot** : Maintenir un flux d'Insectes sur les rangs adjacents aux Rêves via Filaments Oniriques pour transformer chaque déviation ±1 en double neutralisation (annulation + Altération) avec recyclage gratuit sur M5.

**Témoins (1)**

- **`M5_T1`** (`A_CODER`) : Tour 3, M5 défendu (0 Insecte) produit +1 et envoie cet Insecte sur le rang 4 via Filaments Oniriques (M5 revient à 0). À l'ouverture du Tour 4, I dévie une Abatteuse du rang 4 vers le Rêve du rang 3 : Spores de Déviation pose 1 Altération sur l'Abatteuse et replace l'Insecte sur M5 (< 2 Insectes), puis le Rêve défendu annule l'Abatteuse à ce tour.

---

## 3. Points d’harmonisation éditoriale & ergonomique repérés pour l’Étape 3 (Passe 2)

Les 30 fiches ci-dessus sont extraites fidèlement de leur panel d’origine (seul `G3` a été reclassé hors-twist). Pour la Passe 2 (harmonisation de voix et ergonomie finale avant encodage PyPy en Étape 4), les écarts de style inter-panels suivants mériteront un lissage homogène :

1. **Titres complets des Gardiens (`carte_joueur.titre_complet`)** : les 12 Gardiens issus de `panel_1` et `G10` (`panel_3`) portent un épithète évocateur (*« Le Jaguar, seigneur des berges »*, *« La Matamata, Guetteuse des Feuilles Mortes »*), tandis que `G3` (*L’Atèle*) et `G11` (*La Harpie féroce*, issus de `panel_2`) portent uniquement le nom de l’animal ; harmoniser le style des épithètes et la casse (`panel_3` utilise des majuscules de titre).
2. **Zéro code interne dans le texte joueur** : `G11` (`Face 2`, issu de `panel_2`) mentionne explicitement le code interne `« R5 »` (*« après tout échange de R5 »*) ; remplacer en Passe 2 par une formulation joueur (*« après tout échange du Ciel à deux eaux »* ou formulation générique de chronologie d’ouverture).
3. **Homogénéité du champ `mots_cles_plateau.enracine`** : les 22 fiches `panel_1` sans rôle `ENRACINEMENT` laissent ce champ à `null`, alors que `G11` (`panel_2` : `"Ordinaire"`) et `G10`, `R8`, `R10`, `M5` (`panel_3` : `"Standard (...)"`) y inscrivent une mention standard ; unifier sur `null` hors des 4 synergies d’Enracinement (`G7`, `G15`, `R1`, `R2`).
4. **Homogénéité typographique & structurelle des textes** : unifier les apostrophes typographiques (`’` vs `'` dans `panel_3`), la mise en forme des choix/puces (`panel_1` narratif en paragraphes nommés vs `panel_2` compact vs `panel_3` numéroté `1. / 2. / •`), et la voix des encadrés *Décision / Renoncement*.
5. **Format des champs `vecteurs` et statut des `temoins`** : uniformiser le style de `vecteurs` (phrase fléchée `panel_1` vs formule tokens `panel_2` vs `SCREAMING_SNAKE` `panel_3`) et remettre tous les témoins sur le statut `A_CODER` avant leur implémentation exécutable PyPy en Étape 4 (`G3_T1`, `G3_T2` et `R5_T1` portent actuellement `OK` depuis la maquette Python locale de `panel_2`).
