# Comparatif des 3 Panels Candidats (`v6.3.1`) — Arbitrage d’auteur (Étape 2b)

*Généré automatiquement depuis `contracts/panels/panel_1.json`, `panel_2.json` et `panel_3.json` (validés à `0 erreur` par `scripts/tiles_v6_3_schema.py --strict` et `scripts/audit_197.py`).*

---

## 1. Tableau de bord comparatif (`audit_197` · 197 assises · 4 Murs Porteurs `M1..M4`)

| Critère | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Source / modèle** | Modèle 1 — Candidat 1 (19 inchangés) + REPONSE_IA1 (11 révisés) | Modèle 2 — Candidat 2 (19 inchangés) + REPONSE_IA2 (11 révisés + filet R2) | Modèle 3 — Candidat 3 (4 inchangés) + REPONSE_IA3 Lots A1/A2/A3/B (26 révisés + correctifs Red Team) |
| **Verdict global (`audit_197`)** | **OK** (0 erreur) | **OK** (0 erreur) | **OK** (0 erreur) |
| **Murs `M1 / M2 / M3 / M4`** | OK / OK / OK / OK | OK / OK / OK / OK | OK / OK / OK / OK |
| **Schéma bi-composant `v6.3.1`** | OK (0 erreur, `C02` purgé) | OK (0 erreur, `C02` purgé) | OK (0 erreur, `C02` purgé) |
| **Twists `2K3` (`Q02`)** | 6 : G12, G2, G7, M3, R10, R4 | 6 : G15, G3, G9, M1, R1, R8 | 6 : G6, G8, G9, M1, R10, R5 |
| **Lois passives (`Q01` ≤ 5, max/assise ≤ 2)** | 4/5 (max 2/assise) : M5, R2, R7, R8 | 2/5 (max 2/assise) : M1, R8 | 3/5 (max 2/assise) : M5, R2, R8 |
| **Catalyseurs Éveil (`I04` ≥ 9)** | 11 : G1, G11, G12, G13, G14, G15, G3, G4, G5, G8, G9 | 13 : G1, G10, G11, G12, G13, G14, G15, G2, G3, G4, G6, G7, G8 | 11 : G1, G10, G11, G12, G13, G14, G15, G4, G5, G7, G9 |
| **Leviers de Rêve (`I05`)** | 7 (G8, R1, R10, R2, R4, R8, R9) · E couverts : 4/4 | 5 (R1, R10, R7, R8, R9) · E couverts : 4/4 | 6 (R10, R4, R5, R7, R8, R9) · E couverts : 4/4 |
| **Synergies Enracinement (`I06` 3–5)** | 4 : G15, G3, G7, R1 | 4 : G12, G7, M4, R2 | 4 : G15, G3, M4, R3 |
| **Synergies optionnelles couvertes (`/64`)** | 23 déclarées (100 % sur 64/64 assises) | 32 déclarées (100 % sur 64/64 assises) | 68 déclarées (100 % sur 64/64 assises) |

> **Note d’assemblage Étape 2a (4 micro-correctifs Red Team appliqués)** : (1) filet plancher solo ajouté sur `Panel 2 · R2` (*à défaut, sur une mobile sans Altération de E ou H*) ; (2) physique `v6.2` exacte des encoches rétablie sur `Panel 3 · G1` (*Rugissement d’Éveil* + repli solo) et `Panel 3 · G5` (*Relais d’Éveil* sans retrait de l’encoche, zéro compteur de Résonance `v6.0`) ; (3) casting verrouillé `Le Caïman noir` (`fenetre_badge: ACTIVATION`) sur `Panel 3 · G9` et renommage `Le Songe de la Carapace de Limon` sur `Panel 3 · R4` ; (4) mapping complet vers les 32 codes `PIC_*` officiels, suppression de toute référence brute d’étape (`C01`), et séparation `entrees_plancher` / `entrees_synergie` sur les 90 fiches.

---

## 2. Sommaire des 15 lisières (`X ↔ Y`)

### A. Lisières Animal ↔ Animal (3 lisières · 6 Gardiens)
- **Lisière `M ↔ R`** (Mammifères ↔ Reptiles) : [`G1` (`M>R`) & `G2` (`R>M`)](#lisiere-m-r-g1-g2)
- **Lisière `M ↔ O`** (Mammifères ↔ Oiseaux) : [`G3` (`M>O`) & `G4` (`O>M`)](#lisiere-m-o-g3-g4)
- **Lisière `R ↔ O`** (Reptiles ↔ Oiseaux) : [`G5` (`R>O`) & `G6` (`O>R`)](#lisiere-r-o-g5-g6)

### B. Lisières Animal ↔ Onirique (6 lisières · 6 Gardiens + 6 Rêves)
- **Lisière `M ↔ H`** (Mammifères ↔ Humains) : [`G7` (`M>H`) & `R3` (`H>M`)](#lisiere-m-h-g7-r3)
- **Lisière `M ↔ E`** (Mammifères ↔ Entités Magiques) : [`G8` (`M>E`) & `R7` (`E>M`)](#lisiere-m-e-g8-r7)
- **Lisière `R ↔ H`** (Reptiles ↔ Humains) : [`G9` (`R>H`) & `R4` (`H>R`)](#lisiere-r-h-g9-r4)
- **Lisière `R ↔ E`** (Reptiles ↔ Entités Magiques) : [`G10` (`R>E`) & `R8` (`E>R`)](#lisiere-r-e-g10-r8)
- **Lisière `O ↔ H`** (Oiseaux ↔ Humains) : [`G11` (`O>H`) & `R5` (`H>O`)](#lisiere-o-h-g11-r5)
- **Lisière `O ↔ E`** (Oiseaux ↔ Entités Magiques) : [`G12` (`O>E`) & `R9` (`E>O`)](#lisiere-o-e-g12-r9)

### C. Lisières Animal ↔ Essaim (3 lisières · 3 Gardiens + 3 Nids)
- **Lisière `M ↔ I`** (Mammifères ↔ Insectes) : [`G13` (`M>I`) & `M1` (`I>M`)](#lisiere-m-i-g13-m1)
- **Lisière `R ↔ I`** (Reptiles ↔ Insectes) : [`G14` (`R>I`) & `M2` (`I>R`)](#lisiere-r-i-g14-m2)
- **Lisière `O ↔ I`** (Oiseaux ↔ Insectes) : [`G15` (`O>I`) & `M3` (`I>O`)](#lisiere-o-i-g15-m3)

### D. Triangle Autonome A = 0 `{H, E, I}` (3 lisières · 4 Rêves + 2 Nids)
- **Lisière `H ↔ E`** (Humains ↔ Entités Magiques) : [`R1` (`H>E`) & `R2` (`E>H`)](#lisiere-h-e-r1-r2)
- **Lisière `H ↔ I`** (Humains ↔ Insectes) : [`R6` (`H>I`) & `M4` (`I>H`)](#lisiere-h-i-r6-m4)
- **Lisière `E ↔ I`** (Entités Magiques ↔ Insectes) : [`R10` (`E>I`) & `M5` (`I>E`)](#lisiere-e-i-r10-m5)

---

## A. Lisières Animal ↔ Animal (3 lisières · 6 Gardiens)

<a id="lisiere-m-r-g1-g2"></a>
### Lisière `M ↔ R` — Mammifères ↔ Reptiles (`G1` & `G2`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G1`** (`M>R`, GARDIEN) | **Le Jaguar, seigneur des berges** — Le Croc chasse aux côtés du Duel (⭐ Éveil · sortie `CROC_POSTE`) | **Le Jaguar** — Gué marqué / Chaleur à revers (⭐ Éveil · sortie `BLEU`) | **Le Jaguar, Souverain des Berges** — Surchauffe féline ou pari sauvé (⭐ Éveil · sortie `PARI_GLISSE`) |
| **`G2`** (`R>M`, GARDIEN) | **L’Anaconda vert, l’étau des eaux dormantes** — Arrache une machine à son Ratissage (⚡ Twist 2K3 · sortie `RATISSAGE_ROMPU`) | **L’Anaconda vert** — Mobile ← un pas · Croc sur la trace / traction vers Croc ou Duel (⭐ Éveil · sortie `RECUL`) | **L’Anaconda vert, Souffle Glacé de l’Igapó** — Constriction thermique et mue Reptile (Brique fluide · sortie `BLEU`) |

#### Emplacement `G1` (`M>R` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Jaguar, seigneur des berges** | **Le Jaguar** | **Le Jaguar, Souverain des Berges** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Piégeage** | ACTIVATION / **Piégeage** | ACTIVATION / **Parade** |
| **Pictogrammes** | 🦷 `PIC_CROC` · ⚔️ `PIC_DUEL` · 🔵 `PIC_BLEU` | ⚔️ `PIC_DUEL` · 🦷 `PIC_CROC` · 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` | ⚔️ `PIC_DUEL` · 🔵 `PIC_BLEU` · 🦷 `PIC_CROC` · ⭐ `PIC_PARI_ENCOCHE` |
| **Résumé Mini-Tuile** | Le Croc chasse aux côtés du Duel | Gué marqué / Chaleur à revers | Surchauffe féline ou pari sauvé |
| **Mots-clés Face 1** | Croc → parcelle du Duel · parade du Croc = Territoire tenu | Gué marqué | 1 🔴→🔵 (si 0 🔴 : 🦷) OU glisse 1 pari allié → ⭐ (repli : ♻️ → ⚔️/M) |
| **Mots-clés Face 2** | Croc et Duel → toute parcelle ciblée · machine parée = 1 Rouge en Bleu | Chaleur à revers | 1 🔴→🔵 (ou 🦷) · si Territoire tenu : ET glisse 1 pari allié → ⭐ |
| **Plancher (`M4`)** | `DUEL`, `CROC` | `DUEL`, `ROUGE`, `RANG_MACHINE`, `RATISSAGE` | `DUEL`, `ROUGE`, `GARDIEN` |
| **Synergies (`I01`)** | — | `CROC` | `DEFENSEUR_ATTENTE` |
| **Sorties (`I03`)** | `CROC_POSTE`, `CROC`, `TERRITOIRE`, `BLEU` | `BLEU` | `PARI_GLISSE`, `BLEU`, `CROC`, `TERRITOIRE` |

- **Panel 1 — Le Jaguar, seigneur des berges** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : Le Jaguar ne craint ni l’eau ni les écailles : il chasse le caïman sur sa propre berge et le tue d’une seule morsure au crâne. Là où il rôde, la rive appartient de nouveau à la forêt.
  - **Face 1** :
  > Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur la parcelle qui porte le jeton Duel, quelle que soit sa face. Le Croc y pare en premier, comme toujours, puis regagne la réserve Reptile. Pacte de la berge : tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne aussi le Duel sur Territoire tenu, comme si un Défenseur l’avait parée. Si le Duel n’est pas en forêt, le Jaguar ne fait rien.
  - **Face 2** :
  > Quand le Jaguar s’active : prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et postez-le sur n’importe quelle parcelle ciblée, de n’importe quel rayon. Le jeton Duel peut traverser le fleuve avec lui : déplacez-le sur cette parcelle, sur sa face actuelle, même sans Défenseur Mammifère. Le Croc y pare en premier puis regagne la réserve Reptile ; tant que le Croc et le Duel partagent une parcelle, une frappe que le Croc y pare retourne le Duel sur Territoire tenu. Morsure au crâne : la machine dont le Croc vient de parer la frappe retourne aussi 1 de ses Rouges en Bleu.
  - **Dilemme** — *Choix* : Où poster le Croc : sur le Duel pour sceller un Territoire tenu, ou (Face 2) sur la parcelle ciblée la plus menacée d’un autre rayon, Duel compris. · *Renoncement* : Déplacer le Croc dégarnit la parcelle où une Écaille l’avait posé ; et l’icône Piégeage ne s’allume que si une frappe tombe réellement sur lui.
  - **Double activation** : Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume Piégeage, l’icône même où siège le Jaguar, d’où une seconde activation qui le reposte aussitôt pour la frappe suivante. Deux activations = deux parades du Croc et un Duel scellé sur Territoire tenu dès la première.
  - **Témoin `G1_T1`** : Croc en réserve, Duel face Défi sur la parcelle 3 du rayon M ; le Jaguar s’active : le Croc y est posté ; le Bulldozer frappe la parcelle 3 : le Croc pare (Piégeage) et regagne la réserve ; le Duel passe sur Territoire tenu.

- **Panel 2 — Le Jaguar** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : Au gué, le jaguar laisse passer la première silhouette. La seconde trouve l’eau déjà troublée.
  - **Face 1** :
  > À chaque activation, choisissez une machine qui cible encore la parcelle du Duel ou du Croc. Vous pouvez retourner sur elle un Rouge en Bleu.
  - **Face 2** :
  > À chaque activation, choisissez une machine qui cible encore la parcelle du Duel ou du Croc. Vous pouvez retourner un de ses Rouges en Bleu et le laisser sur elle, ou le déposer face Bleue sur l’autre machine de son rayon.
  - **Dilemme** — *Choix* : Où laisser la Surchauffe du gué ? · *Renoncement* : La transmettre au Bulldozer laisse l’Abatteuse plus difficile à parer.
  - **Double activation** : Deux passages peuvent épuiser deux Rouges du même assaillant ou préparer séparément les deux machines du gué.
  - **Témoin `G1_T1`** : Le Croc garde le gué. En Face 2, le Jaguar prend un Rouge à l’Abatteuse qui le vise et le donne en Bleu au Bulldozer. En Charge, son seuil gravé de 2 tombe à 1.

- **Panel 3 — Le Jaguar, Souverain des Berges** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : « Là où la forêt refuse de céder un pas, l'ombre tachetée bondit et réveille les anciens esprits. »
  - **Face 1** :
  > Lors d'une Parade sur la parcelle du Duel avec au moins 1 Défenseur, retournez d'abord le Duel sur Territoire tenu avant de résoudre Le Jaguar. À l'activation, choisissez l'un des deux effets :
  > 1. Bond Thermique : ciblez 1 machine du plateau et retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe ; si cette machine ne porte aucun Rouge, posez ou déplacez le pion Croc (depuis la réserve Reptile ou le plateau) sur sa parcelle.
  > 2. Rugissement d'Éveil : faites glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir) ; si aucun autre Gardien construit ne porte de Défenseur en pari, relevez à la place 1 Défenseur couché en attente (ou déplacez 1 Défenseur d'une parcelle non ciblée) sur la parcelle du Duel ou sur une parcelle ciblée du rayon Mammifère.
  - **Face 2** :
  > Résolvez Bond Thermique ou Rugissement d'Éveil (comme en Face 1). Si le jeton Duel est sur sa face Territoire tenu au moment de cette activation, résolvez les deux effets successivement (Bond Thermique puis Rugissement d'Éveil).
  - **Dilemme** — *Choix* : Trancher en Face 1 (et en Face 2 tant que le Duel reste en Défi) entre neutraliser une menace physique immédiate (Rouge → Bleu ou Croc avant une attaque) et sécuriser le pari compromis d'un autre Gardien pour préserver l'Éveil de la Forêt. · *Renoncement* : Sauver un pari allié par Rugissement d'Éveil renonce à l'appui de terrain immédiat tant que Territoire tenu n'est pas verrouillé en Face 2.
  - **Double activation** : Engager 2 Défenseurs sur G1 exige 2 Parades aux attaques (puisque G1 ne peut jamais faire glisser son propre second pari). La 1re Parade permet d'affaiblir la machine située sur la parcelle du Duel (1 Rouge → Bleu, abaissant son Seuil de Parade de 2 points en Assaut ou Ratissage), ce qui facilite la réussite de la 2nde Parade sur ce Duel : celui-ci bascule alors en Territoire tenu, fait glisser le 2nd pari de G1 dans sa seconde encoche et déclenche en Face 2 le double effet complet.
  - **Témoin `G1_T1`** : Tour 4 (Acte 1, 4 joueurs), 4 Défenseurs engagés sur la Piste des Gardiens (2 sur G1 Face 2 Parade, 1 sur Piégeage, 1 sur Sabotage non déclenché à l'ouverture). Aux attaques, une Parade au rang 2 active G1 (Bond Thermique : Rouge → Bleu sur l'Abatteuse du rang 5, seuil 4 → 2). Au rang 5, la Parade sur la parcelle du Duel le bascule en Territoire tenu et déclenche la 2nde activation de G1 : pose du Croc + Rugissement d'Éveil qui fait glisser le pari du Gardien Sabotage dans son encoche libre → 0 pari perdu, Éveil.

#### Emplacement `G2` (`R>M` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **L’Anaconda vert, l’étau des eaux dormantes** | **L’Anaconda vert** | **L’Anaconda vert, Souffle Glacé de l’Igapó** |
| **Rôles & Nature** | ⚡ Twist 2K3 (`ACTION`) | ⭐ Éveil (`ACTION`) | Brique fluide (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Parade** | ACTIVATION / **Sabotage** | ACTIVATION / **Piégeage** |
| **Pictogrammes** | ⚡ `PIC_TWIST` · ⚔️ `PIC_DUEL` · ⏪ `PIC_RECUL` | ⏪ `PIC_RECUL` · 🦷 `PIC_CROC` · ⚔️ `PIC_DUEL` | 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` · 🦎 `PIC_ECAILLE` · ⚔️ `PIC_DUEL` |
| **Résumé Mini-Tuile** | Arrache une machine à son Ratissage | Mobile ← un pas · Croc sur la trace / traction vers Croc ou Duel | Constriction thermique et mue Reptile |
| **Mots-clés Face 1** | Ratissage sur Territoire tenu ou 2 Défenseurs → jeton au sac · recul 1 | Repli au gué | 1 🔴→🔵 (si 0 🔴 : ⏪ 1) OU +1 🦎 au sac + 🦷 hors ⚔️ |
| **Mots-clés Face 2** | Duel ou 2 Défenseurs · Ratissage arraché · machine mobile noyée et reculée | Rabattre sur la marque | Rayon ⚔️ = jusqu’à 2 🔴→🔵 · si Territoire tenu = Constriction ET 🦎/🦷 |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `RATISSAGE`, `DUEL` | `CROC`, `RANG_MACHINE` | `ROUGE`, `ECAILLE`, `CROC` |
| **Synergies (`I01`)** | `TERRITOIRE` | `DUEL` | `DUEL`, `TERRITOIRE` |
| **Sorties (`I03`)** | `RATISSAGE_ROMPU`, `RECUL`, `ANNULATION` | `RECUL`, `CROC` | `BLEU`, `ECAILLE`, `CROC`, `RECUL` |

- **Panel 1 — L’Anaconda vert, l’étau des eaux dormantes** *(⚡ Twist 2K3 · ACTIVATION / **Parade**)*
  - *Ambiance* : L’Anaconda attend des heures, invisible sous la lentille d’eau. Quand la proie s’aventure au bord, chaque expiration resserre ses anneaux, et il l’entraîne là où plus rien ne pousse : au fond.
  - **Face 1** :
  > Quand l’Anaconda vert s’active : choisissez une machine en Ratissage dont la parcelle porte le jeton Duel face Territoire tenu, ou au moins 2 Défenseurs. L’étau l’arrache à son Ratissage : reprenez le jeton Machine glissé sous elle et remettez-le dans le sac ; la machine redevient mobile et recule d’1 parcelle vers la bordure (en sautant les Routes Forestières), en conservant tous ses jetons Puissance. Faute de jeton tiré, elle n’attaque plus avant le ménage ; au ménage, n’étant plus sur la dernière parcelle, elle ne rentre pas en Ratissage.
  - **Face 2** :
  > Quand l’Anaconda vert s’active : choisissez une machine dont la parcelle porte le jeton Duel (sur l’une ou l’autre face) ou au moins 2 Défenseurs. Si elle est en Ratissage, l’étau l’en arrache : reprenez son jeton Machine et remettez-le dans le sac ; elle redevient mobile, recule d’1 parcelle vers la bordure (en sautant les Routes Forestières) en conservant ses jetons Puissance, et n’attaque plus avant le ménage. Si elle est mobile et n’a pas encore attaqué, l’Anaconda la noie : inclinez son jeton Machine (elle est annulée) et faites-la reculer d’1 parcelle vers la bordure.
  - **Dilemme** — *Choix* : Arracher maintenant la machine en Ratissage, ou la laisser au fond tant que son jeton n’alourdit pas le sac. · *Renoncement* : Le jeton Machine rendu au sac rend chaque pioche future plus dangereuse ; et le Duel engagé sur la dernière parcelle ne couvre plus la lisière.
  - **Double activation** : Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la même dernière parcelle : la première activation arrache l’Abatteuse, la seconde le Bulldozer, tant que le Duel tient la parcelle. En Face 2, la seconde activation peut aussi noyer la machine mobile qui s’apprête à frapper le Duel.
  - **Témoin `G2_T1`** : Bulldozer en Ratissage (2 Rouges) sur la dernière parcelle du rayon R, Duel face Territoire tenu sur cette parcelle ; l’Anaconda s’active au rang 2 : jeton remis au sac, Bulldozer mobile en parcelle 3, aucune frappe de Ratissage.

- **Panel 2 — L’Anaconda vert** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : L’eau se retire autour des anneaux. Il ne reste qu’un gué.
  - **Face 1** :
  > Repli au gué. Choisissez une mobile de R ou M qui n’est pas en cours d’activation et dispose d’un pas vers la bordure. Faites-la reculer de ce pas, sans frappe. Vous pouvez prendre le Croc en réserve ou en forêt et le poser sur la parcelle qu’elle quitte. Vous pouvez aussi vous limiter à poster le Croc sur une parcelle de R ou M de votre choix (ou sur une parcelle survivante d’un autre rayon si R et M sont entièrement Route), même avant qu’une machine la cible.
  - **Face 2** :
  > Rabattre sur la marque. Vous disposez du Repli au gué. Vous pouvez à la place choisir une mobile non engagée à un pas radial du Croc ou du Duel. Tirez-la sur la marque, même vers le cœur. Si vous le souhaitez, placez ensuite le Croc sur la parcelle libérée. Le Duel garde sa place et sa face. Ces deux manœuvres laissent les machines en Ratissage à leur poste.
  - **Dilemme** — *Choix* : Laisser le Croc sous la machine pour couvrir Sur place, ou le refermer derrière elle pour couvrir Devant et offrir au Jaguar une autre cible marquée. · *Renoncement* : Repositionner le Croc libère la parcelle qu’il gardait ; en Face 2, attirer une mobile vers le cœur rapproche son front si elle n’est pas neutralisée dans le tour.
  - **Double activation** : Deux replis peuvent ramener deux mobiles d’un pas chacun. En Face 2, le premier passage peut laisser le Croc au gué libéré et le second y attirer une mobile du voisinage.
  - **Témoin `G2_T1`** : Le Duel est en M·2. À l’ouverture, l’Abatteuse de M occupe M·3, porte un Rouge et doit frapper Sur place au rang 4. G2 la ramène en M·2 et laisse le Croc en M·3. Un Piège arrête une frappe de rang 1 et active G1 sur Piégeage : la cible encore à jouer est le Duel en M·2, G1 retourne le Rouge de l’Abatteuse sur place (seuil de rang 4 abaissé de 3 à 1 en Acte 1), le Croc reste en M·3.

- **Panel 3 — L’Anaconda vert, Souffle Glacé de l’Igapó** *(Brique fluide · ACTIVATION / **Piégeage**)*
  - *Ambiance* : « Sous l'eau noire du méandre, ses anneaux glacés étouffent la ferraille avant même qu'elle ne gronde. »
  - **Face 1** :
  > À l'activation, choisissez l'un des deux effets :
  > 1. Constriction : ciblez 1 machine du plateau et retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe ; si cette machine ne porte aucun Rouge et est mobile, faites-la reculer d'1 parcelle vers la bordure (en sautant toute Route Forestière).
  > 2. Sillage d'Écaille : versez 1 jeton Écaille de la réserve Reptile dans le sac opaque (s'il en reste en réserve) et posez ou déplacez le pion Croc sur toute parcelle autre que celle portant le Duel.
  - **Face 2** :
  > Résolvez Constriction ou Sillage d'Écaille (comme en Face 1), avec deux amplifications liées au Duel :
  > • Si Constriction cible une machine située sur le rayon portant le Duel, retournez sur elle jusqu'à 2 jetons Rouge existants en Bleu Surchauffe (ou 1 Rouge → Bleu suivi d'un recul d'1 parcelle si elle n'avait qu'1 seul Rouge et est mobile).
  > • Si le Duel est sur sa face Territoire tenu, résolvez Constriction ET Sillage d'Écaille lors de cette même activation.
  - **Dilemme** — *Choix* : Arbitrer entre le soulagement thermique immédiat d'une machine menaçante (Constriction) et l'enrichissement structurel du sac en Écailles assorti d'un Croc hors Duel (Sillage d'Écaille). · *Renoncement* : Laisser la parcelle du Duel libre d'être parée par les Mammifères pour débloquer Territoire tenu plutôt que d'y poser le Croc.
  - **Double activation** : Avec 2 Défenseurs engagés sur Piégeage et 2 Pièges déclenchés aux attaques, la 1re activation peut refroidir la machine postée sur le Duel (Rouge → Bleu) afin d'assurer sa Parade par M sur un rang intermédiaire ; une fois le Duel retourné sur Territoire tenu, la 2nde activation de G2 sur un Piège ultérieur déploie simultanément la double Constriction et Sillage d'Écaille (replaçant aussitôt le Croc sur une parcelle dont le Piège vient de céder).
  - **Témoin `G2_T1`** : Tour 5 (Acte 2), G2 Face 2 sur Piégeage (1 pari). Sur M, le Bulldozer est paré au rang 1 (Duel → Territoire tenu) et l'Abatteuse (rang 3, 2 Rouges, seuil 4) attend. Au rang 2, un Piège sur R active G2 Face 2 : grâce à Territoire tenu, Constriction retourne les 2 Rouges de l'Abatteuse en 2 Bleus (seuil ramené au minimum 1) ET Sillage d'Écaille ajoute 1 Écaille au sac et pose le Croc en parcelle 2 de R.

---

<a id="lisiere-m-o-g3-g4"></a>
### Lisière `M ↔ O` — Mammifères ↔ Oiseaux (`G3` & `G4`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G3`** (`M>O`, GARDIEN) | **L’Atèle, funambule de la canopée** — Pont de canopée entre rayons voisins (⭐ Éveil · 🌱 Enracinement · sortie `DEFENSEUR_REDEPLOYE`) | **L’Atèle** — Deux cimes · traverse / Plume · trajet en L (⭐ Éveil · ⚡ Twist 2K3 · sortie `DEFENSEUR_REDEPLOYE`) | **L’Atèle, Acrobate des Hautes Voûtes** — Croise les machines sous les cimes (🌱 Enracinement · sortie `RECUL`) |
| **`G4`** (`O>M`, GARDIEN) | **L’Ara rouge, sentinelle de la collpa** — Cri d’alarme qui fait avancer les paris (⭐ Éveil · sortie `PARI_GLISSE`) | **L’Ara rouge** — Cri · transfert de mise / Cri · évacuation (⭐ Éveil · sortie `PARI_REORIENTE`) | **L’Ara rouge, Vigie Écarlate de la Collpa** — Rallie la garde au cri d’alerte (⭐ Éveil · sortie `DEFENSEUR_REDEPLOYE`) |

#### Emplacement `G3` (`M>O` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **L’Atèle, funambule de la canopée** | **L’Atèle** | **L’Atèle, Acrobate des Hautes Voûtes** |
| **Rôles & Nature** | ⭐ Éveil · 🌱 Enracinement (`ACTION`) | ⭐ Éveil · ⚡ Twist 2K3 (`ACTION`) | 🌱 Enracinement (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Parade** | ACTIVATION / **Sabotage** | ACTIVATION / **Sabotage** |
| **Pictogrammes** | 🛡️ `PIC_DEFENSEUR` · 🌳 `PIC_ARBRE` · 🪶 `PIC_PLUME` · 🌱 `PIC_ENRACINEMENT` | 🌳 `PIC_ARBRE` · 🛣️ `PIC_ROUTE` · 🛡️ `PIC_DEFENSEUR` · 🪶 `PIC_PLUME` | 🌳 `PIC_ARBRE` · ⏪ `PIC_RECUL` · ⚔️ `PIC_DUEL` · 🌱 `PIC_ENRACINEMENT` |
| **Résumé Mini-Tuile** | Pont de canopée entre rayons voisins | Deux cimes · traverse / Plume · trajet en L | Croise les machines sous les cimes |
| **Mots-clés Face 1** | 1 Défenseur → même numéro du rayon voisin · Arbre debout des deux côtés | Deux cimes · traverse | Rayon M / O / 🪶 : permute les 2 machines mobiles OU ⏪ -1 (+ déplace ⚔️ sous 🌳) |
| **Mots-clés Face 2** | Troupe de 2 · traversée en chaîne · Plume Chaud franchit 1 clairière | Plume · trajet en L | Tout rayon : permute les 2 mobiles OU ⏪ -1 · Puis 🔴→🔵 (ou ⚔️ sur Territoire tenu) |
| **Mots-clés Enraciné** | Canopée intacte → 1 repousse de plus chez le voisin | — | Décompte final : +1 🪵→🌳 sur une autre parcelle (M ou O) si ≥ 2 parcelles gardent 🌳 |
| **Plancher (`M4`)** | `ARBRE`, `PLUME` | `ARBRE`, `ROUTE`, `DEFENSEUR_REDEPLOYE` | `ARBRE`, `RANG_MACHINE`, `PLUME` |
| **Synergies (`I01`)** | `DUEL` | `PLUME` | `DUEL`, `ROUGE`, `SOUCHE` |
| **Sorties (`I03`)** | `DEFENSEUR_REDEPLOYE`, `PARADE_CANOPEE`, `ARBRE` | `DEFENSEUR_REDEPLOYE` | `RECUL`, `DUEL`, `BLEU`, `ARBRE` |

- **Panel 1 — L’Atèle, funambule de la canopée** *(⭐ Éveil · 🌱 Enracinement · ACTIVATION / **Parade**)*
  - *Ambiance* : L’Atèle ne descend presque jamais au sol : sa route, c’est le toit de la forêt. Tant que les cimes se touchent, la troupe passe d’un territoire à l’autre ; qu’une trouée s’ouvre, et le chemin se rompt.
  - **Face 1** :
  > Quand l’Atèle s’active : faites franchir la canopée à 1 Défenseur (de n’importe quel joueur, sur sa face actuelle) : déplacez-le d’une parcelle vers la parcelle de même numéro d’un rayon voisin, à condition que ces deux parcelles portent chacune au moins 1 Arbre debout. Une Route Forestière ou une parcelle réduite à des Souches rompt la canopée : aucun franchissement depuis elle ni vers elle. Si ce Défenseur accompagnait le jeton Duel, le Duel le suit sur sa face actuelle. Arrivé, le Défenseur compte normalement pour toutes les frappes qui n’ont pas encore été résolues.
  - **Face 2** :
  > Quand l’Atèle s’active : faites franchir la canopée à une troupe d’au plus 2 Défenseurs partis de la même parcelle (et au jeton Duel s’il les accompagne). Déplacez-les ensemble vers la parcelle de même numéro d’un rayon voisin, puis, si vous le voulez, poursuivez de rayon voisin en rayon voisin tant que la canopée reste continue : chaque parcelle traversée, à ce même numéro, porte au moins 1 Arbre debout. La troupe s’arrête où vous voulez. Une Route Forestière l’arrête toujours ; mais si la Plume de Vigie est posée face Chaud au pied du rayon d’arrivée, la troupe peut traverser ou atteindre une parcelle réduite à des Souches. Arrivés, les Défenseurs comptent pour toutes les frappes non encore résolues.
  - **Enraciné** :
  > Enraciné : l’Atèle sème par-delà la lisière. Au décompte final, si la parcelle face à laquelle il est enraciné et la parcelle de même numéro d’un rayon voisin portent toutes deux encore au moins 1 Arbre debout (la canopée tient), retournez 1 Souche de cette parcelle voisine en Arbre debout, en plus de sa repousse normale.
  - **Dilemme** — *Choix* : Quel Défenseur faire traverser, et vers quel voisin : renforcer la frappe imminente d’à côté ou garder la parcelle de départ. · *Renoncement* : Le Défenseur qui traverse abandonne les frappes à venir sur sa parcelle d’origine ; et laisser une parcelle devenir clairière rompt durablement le pont.
  - **Double activation** : Chaque activation fait traverser un Défenseur différent, ou le même deux fois : la troupe pare au rang 1 sur un rayon, puis passe chez le voisin pour parer au rang 4. Chaque parade ainsi complétée allume Parade, l’icône même de l’Atèle.
  - **Témoin `G3_T1`** : Défenseur O sur la parcelle 2 (2 Arbres) du rayon O ; la parcelle 2 du rayon M (1 Arbre) est visée au rang 4 avec 1 Défenseur, seuil 2 ; l’Atèle s’active après une parade au rang 1 : le Défenseur passe sur la parcelle 2 du rayon M, la frappe du rang 4 est parée.

- **Panel 2 — L’Atèle** *(⭐ Éveil · ⚡ Twist 2K3 · ACTIVATION / **Sabotage**)*
  - *Ambiance* : L’atèle essaie le poids d’une branche avant de lâcher la précédente. Au-dessous de lui, le chemin a disparu.
  - **Face 1** :
  > À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux. Il traverse leur frontière entre deux parcelles de même profondeur portant chacune un Arbre debout. Avant de traverser, il peut faire un pas radial sur son rayon, en sautant les Routes. Le Duel reste en place.
  - **Face 2** :
  > À chaque activation, vous pouvez déplacer un Défenseur en forêt entre les rayons Mammifères et Oiseaux, ou entre le rayon portant la Plume et un de ses voisins. Traversez entre deux parcelles de même profondeur portant chacune un Arbre. Vous pouvez ajouter un pas radial avant et un après la traversée, en sautant les Routes. Le Duel reste en place.
  - **Dilemme** — *Choix* : Quelle cime peut-on dégarnir pour tenir l’autre rive ? · *Renoncement* : Le pion quitte réellement sa première ligne de défense.
  - **Double activation** : Deux traversées amènent les deux pions nécessaires à une Parade ou desservent deux rayons différents.
  - **Témoin `G3_T1`** : En Face 2, un Défenseur quitte M1, saute la Route M2 jusqu’à M3, traverse entre les arbres M3 et O3, puis descend en O4. Il rejoint le Défenseur qui attend un Ratissage de seuil 2.

- **Panel 3 — L’Atèle, Acrobate des Hautes Voûtes** *(🌱 Enracinement · ACTIVATION / **Sabotage**)*
  - *Ambiance* : « D'un bond de trente mètres dans les houppiers, il agite les branches à contre-courant : en bas, l'abatteuse retourne vers les souches et le bulldozer perd sa trace. »
  - **Face 1** :
  > Lorsque L’Atèle s’active, ciblez le rayon Mammifères, le rayon Oiseaux ou le rayon désigné par la Plume de Vigie (si la Plume désigne un rang 1–6, ciblez le rayon d’une machine présente sur ce rang). Choisissez l’une des deux feintes : échangez les parcelles des 2 machines mobiles de ce rayon si aucune des deux n’a encore résolu son activation à ce tour, ou faites reculer d’1 parcelle vers la bordure 1 machine mobile de ce rayon (en sautant toute Route Forestière). Ensuite, si le jeton Duel est sur ce rayon ou dans la réserve Mammifères, vous pouvez le poser ou le déplacer (en conservant sa face actuelle) sur une parcelle de ce rayon portant au moins 1 Arbre debout et au moins 1 Défenseur.
  - **Face 2** :
  > Lorsque L’Atèle s’active, ciblez n’importe quel rayon du plateau : échangez les parcelles de ses 2 machines mobiles non encore résolues à ce tour, ou faites reculer d’1 parcelle vers la bordure 1 machine mobile de ce rayon. De plus, appliquez un effet au choix sur ce rayon : retournez 1 jeton Rouge existant en Bleu Surchauffe sur l’une de ses machines, ou posez ou déplacez le jeton Duel directement sur sa face Territoire tenu auprès d’un Défenseur présent sur une parcelle de ce rayon portant au moins 1 Arbre debout.
  - **Enraciné** :
  > Au décompte final, en plus de sa régénération normale d’Enracinement sur sa parcelle (1 Souche en Face 1, ou 2 Souches en Face 2), retournez 1 Souche supplémentaire en Arbre debout sur une autre parcelle non-Route de votre rayon ou du rayon Oiseaux voisin si au moins 2 parcelles de votre rayon portent encore chacune au moins 1 Arbre debout.
  - **Dilemme** — *Choix* : Désynchroniser le binôme adverse en renvoyant l'Abatteuse frapper à blanc sur une clairière de Souches pendant que le Bulldozer est déporté sur une parcelle boisée, ou conserver L'Atèle jusqu'en fin de partie avant de l'enraciner pour jusqu'à 3 Arbres au décompte final. · *Renoncement* : Échanger les deux machines sauve une clairière de Souches contre le Bulldozer, mais rapproche ce Bulldozer du cœur du rayon pour les tours suivants s'il n'est pas contenu par le Duel.
  - **Double activation** : Deux activations permettent soit de désorganiser successivement deux rayons menacés avant leurs frappes, soit sur un même rayon de faire reculer une machine mobile puis d'échanger le binôme pour renvoyer l'Abatteuse tout au bord de la forêt.
  - **Témoin `G3_T1`** : Sur le rayon Oiseaux marqué par la Plume, parcelle 2 ne porte que 2 Souches sous le Bulldozer (rang 4) tandis que l'Abatteuse est en parcelle 3 (3 Arbres, rang 2). À l'ouverture sur un Sabotage, L'Atèle (Face 1) échange leurs positions : l'Abatteuse frappe parcelle 2 à blanc (0 Arbre coupé) et le Bulldozer frappe parcelle 3 boisée sans pouvoir créer de Route.

#### Emplacement `G4` (`O>M` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **L’Ara rouge, sentinelle de la collpa** | **L’Ara rouge** | **L’Ara rouge, Vigie Écarlate de la Collpa** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Résonance** | ACTIVATION / **Résonance** | ACTIVATION / **Parade** |
| **Pictogrammes** | ⭐ `PIC_PARI_ENCOCHE` · 🔔 `PIC_RESONANCE` · ⚔️ `PIC_DUEL` | 🪶 `PIC_PLUME` · ⭐ `PIC_PARI_ENCOCHE` · 🛡️ `PIC_DEFENSEUR` | 🪶 `PIC_PLUME` · ♻️ `PIC_DEFENSEUR_ATTENTE` · 🛡️ `PIC_DEFENSEUR` · ⚔️ `PIC_DUEL` |
| **Résumé Mini-Tuile** | Cri d’alarme qui fait avancer les paris | Cri · transfert de mise / Cri · évacuation | Rallie la garde au cri d’alerte |
| **Mots-clés Face 1** | 1 pari d’un autre Gardien → encoche · Territoire tenu → Défi = 2e cri · seul en piste : son 2e pari glisse aussi | Cri · transfert de mise | 🪶 Chaud : 1 ♻️ (ou 🛡️ non ciblé) → parcelle ciblée · 🪶 Calme : 1 🛡️ → parcelle ciblée + ⚔️ Tenu (si ≥ 2 🛡️) |
| **Mots-clés Face 2** | Un autre Gardien avec pari s’active · Territoire tenu → Défi = 2e réveil · seul en piste : son 2e pari glisse aussi | Cri · évacuation | Jusqu’à 2 (♻️ ou 🛡️ non ciblés) → parcelles ciblées · Sur ⚔️/🪶 : ⚔️ Tenu OU 🔴→🔵 |
| **Plancher (`M4`)** | `GARDIEN` | `PLUME`, `GARDIEN` | `PLUME`, `DEFENSEUR_ATTENTE` |
| **Synergies (`I01`)** | `TERRITOIRE` | — | `DUEL`, `ROUGE` |
| **Sorties (`I03`)** | `PARI_GLISSE`, `ACTIVATION_RELAIS`, `DEFI` | `PARI_REORIENTE`, `DEFENSEUR_EVACUE` | `DEFENSEUR_REDEPLOYE`, `TERRITOIRE`, `BLEU` |

- **Panel 1 — L’Ara rouge, sentinelle de la collpa** *(⭐ Éveil · ACTIVATION / **Résonance**)*
  - *Ambiance* : À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.
  - **Face 1** :
  > Le cri d’alarme. Quand l’Ara rouge s’active : faites glisser 1 Défenseur posé en pari sur un autre Gardien construit vers une encoche libre de ce même Gardien. Cela ne résout pas le pouvoir de ce Gardien et n’allume aucune icône. Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour faire glisser de la même façon un 2e Défenseur, posé en pari sur un Gardien différent du premier.
  > Sentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, l’Ara crie pour sa propre volée : faites aussi glisser son second pari, s’il en porte un, dans son encoche encore libre.
  - **Face 2** :
  > La volée se lève. Quand l’Ara rouge s’active : choisissez un autre Gardien construit qui porte au moins 1 Défenseur en pari ; il s’active aussitôt (son Défenseur glisse dans une encoche et vous résolvez son pouvoir comme si son icône venait de s’allumer ; s’il s’agit de sa 1re activation du tour, la Résonance la compte). Écho de la collpa : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour réveiller de la même façon un 2e Gardien, différent du premier. L’Ara ne se réveille jamais lui-même.
  > Sentinelle seule (plancher) : si aucun autre Gardien construit ne porte de Défenseur en pari, faites aussi glisser le second pari de l’Ara, s’il en porte un, dans son encoche encore libre, sans résoudre son pouvoir une seconde fois.
  - **Dilemme** — *Choix* : Quel pari faire progresser — celui du Gardien le plus en retard, ou celui dont le pouvoir doit frapper maintenant (Face 2). · *Renoncement* : Retourner le Duel sur Défi pour un 2e cri libère l’avancée des machines de sa parcelle aux rangs 3 et 6 ; construit en premier, l’Ara posé sur Parade s’active seul, mais renonce à la cascade de la Résonance tant qu’il reste en piste.
  - **Double activation** : Chaque cri fait progresser un pari différent : deux activations bouclent le pari d’un Gardien qui ne s’allume jamais (deux glissements sur la même tuile) ou en sécurisent deux. En Face 2, chaque cri déclenche en plus le pouvoir du Gardien réveillé, et chaque 1re activation ainsi provoquée relance la Résonance. Seul en piste, une seule activation boucle son propre pari de deux Défenseurs.
  - **Témoin `G4_T1`** : La Matamata porte 1 pari et 0 encoche occupée ; l’Ara s’active : le pari glisse dans l’encoche ; en fin d’attaques, 0 pion sur la Matamata et 1 encoche : pari gagné.

- **Panel 2 — L’Ara rouge** *(⭐ Éveil · ACTIVATION / **Résonance**)*
  - *Ambiance* : Une bande d’aras décolle du talus. Ceux qui ne voient pas le danger entendent les premiers oiseaux.
  - **Face 1** :
  > À chaque activation, si la Plume indique un rayon, vous pouvez déplacer un Défenseur encore posé sur un Gardien vers un autre Gardien construit. Comptez sur le Gardien d’arrivée les pions dessus et dans ses encoches. Leur total après transfert ne peut dépasser deux. Le pion arrive dessus.
  - **Face 2** :
  > À chaque activation, où que soit posée la Plume, vous pouvez transférer un Défenseur encore posé sur un Gardien vers le dessus d’un autre Gardien construit, dans la limite de deux pions dessus et en encoches réunis. Vous pouvez aussi évacuer ce Défenseur sur une parcelle encore ciblée. Un pion en encoche reste en place.
  - **Dilemme** — *Choix* : Rallier un pari encore gagnable ou évacuer le parieur ? · *Renoncement* : Évacuer en forêt sacrifie sa contribution à l’Éveil.
  - **Double activation** : Deux cris transfèrent deux parieurs séparément, dans la limite des places réellement libres.
  - **Témoin `G4_T1`** : Plume sur M. Deux parieurs attendent sur Rêve après le dernier Rêve. L’Ara en transfère un sur Piégeage avant que le Croc pare. Cette activation peut alors faire glisser le parieur normalement.

- **Panel 3 — L’Ara rouge, Vigie Écarlate de la Collpa** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : « Quand le couple écarlate décolle de la falaise d’argile, son cri porte si loin que la forêt entière a déjà refermé ses rangs avant l’arrivée des chenilles. »
  - **Face 1** :
  > Lorsque L’Ara rouge s’active, observez la face de la Plume de Vigie et ciblez le rayon qu’elle désigne, le rayon d’une machine située sur son rang, ou le rayon portant le jeton Duel (à défaut, le rayon Oiseaux ou Mammifères) :
  > • Si la Plume affiche Chaud (ou n’est pas posée) : prenez 1 Défenseur couché en attente (bâtisseur en lisière ou pion couché en Furtivité, de n’importe quel joueur) — ou, s’il n’en existe aucun, 1 Défenseur debout sur une parcelle non ciblée — et placez-le debout (face Définitif) sur une parcelle ciblée de ce rayon.
  > • Si la Plume affiche Calme : déplacez 1 Défenseur debout d’une parcelle non ciblée (ou relevez 1 Défenseur couché en attente) vers une parcelle ciblée de ce rayon ; si cette parcelle d’arrivée porte le jeton Duel face Défi et réunit désormais au moins 2 Défenseurs, retournez immédiatement le Duel sur Territoire tenu.
  - **Face 2** :
  > Lorsque L’Ara rouge s’active, mobilisez en couple jusqu’à 2 Défenseurs (chacun relevé parmi les Défenseurs couchés en attente ou déplacé depuis une parcelle non ciblée) et placez-les debout sur une ou deux parcelles ciblées de n’importe quels rayons. De plus, si au moins l’un d’eux rejoint la parcelle du jeton Duel ou le rayon désigné par la Plume de Vigie, choisissez 1 bonus : retournez immédiatement le jeton Duel (s’il est accompagné d’au moins 1 Défenseur) sur Territoire tenu, ou retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine visant cette parcelle.
  - **Dilemme** — *Choix* : Orienter sous paravent la Plume sur Chaud pour recycler un bâtisseur couché lors d'un tour de construction, ou sur Calme pour verrouiller immédiatement Territoire tenu avant l'avancée des rangs 3 ou 6. · *Renoncement* : Engager ses Défenseurs du second déploiement en pari sur les Gardiens pour viser l'Éveil dégarnit la forêt au départ et rend la table tributaire du ralliement de L'Ara.
  - **Double activation** : Placé sur Parade, L'Ara rouge transforme une première Parade aux rangs bas en réaction en chaîne : il relève un bâtisseur couché pour atteindre le Seuil de Parade d'un rang suivant, ce qui rallume Parade et déclenche sa seconde activation (jusqu'à 4 Défenseurs mobilisés en Face 2 sur un seul tour).
  - **Témoin `G4_T1`** : Deux alliés ont construit un Gardien à l'ouverture (2 bâtisseurs couchés) et la Plume est Chaud au pied du rayon M où parcelle 3 (Seuil 3) porte le Duel et 2 Défenseurs. Une Parade au rang 1 active L'Ara rouge Face 1 : il relève 1 bâtisseur en parcelle 3 (garde à 3). Au rang 3, la frappe est parée, le Duel passe Territoire tenu et Parade rallume la 2nde activation de L'Ara.

---

<a id="lisiere-r-o-g5-g6"></a>
### Lisière `R ↔ O` — Reptiles ↔ Oiseaux (`G5` & `G6`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G5`** (`R>O`, GARDIEN) | **L’Iguane vert, dormeur des hautes branches** — Tombe en Piège au cri des oiseaux (⭐ Éveil · sortie `PIEGE`) | **L’Iguane vert** — Chaud · Calme / Deux versants (Brique fluide · sortie `BLEU`) | **L’Iguane vert, Guetteur Solaire des Cimes** — Défenseur redéployé et canopée refroidie (⭐ Éveil · sortie `DEFENSEUR_REDEPLOYE`) |
| **`G6`** (`O>R`, GARDIEN) | **Le Toucan toco, le bec-radiateur** — Rend la chaleur aux machines (Brique fluide · sortie `BLEU`) | **Le Toucan toco** — Sur place ↔ Devant / Bleu · échange des dés du rayon (⭐ Éveil · sortie `RANG_MACHINE`) | **Le Toucan toco, Contrebandier du Kapokier** — Échange de machine via Perchoir (⚡ Twist 2K3 · sortie `ANNULATION`) |

#### Emplacement `G5` (`R>O` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **L’Iguane vert, dormeur des hautes branches** | **L’Iguane vert** | **L’Iguane vert, Guetteur Solaire des Cimes** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | Brique fluide (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Piégeage** | ACTIVATION / **Parade** | ACTIVATION / **Parade** |
| **Pictogrammes** | 🪤 `PIC_PIEGE` · 🪶 `PIC_PLUME` · 🦷 `PIC_CROC` · 🔵 `PIC_BLEU` | 🪶 `PIC_PLUME` · 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` · 🦎 `PIC_ECAILLE` | 🛡️ `PIC_DEFENSEUR` · 🪶 `PIC_PLUME` · 🦎 `PIC_ECAILLE` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Tombe en Piège au cri des oiseaux | Chaud · Calme / Deux versants | Défenseur redéployé et canopée refroidie |
| **Mots-clés Face 1** | Piège là où signale la Plume (sinon rayon R ou O) · Bleu bu = le Croc tombe aussi | Chaud · Calme | 1 ♻️/🛡️ non ciblé → forêt (sur 🪶 : +1 pari allié → ⭐) + [🔴→🔵/⏪/🦷 OU +1 🦎 & révéler 🦅] |
| **Mots-clés Face 2** | Piège + Croc sur toute parcelle ciblée · Bleu bu = second plongeon | Deux versants | Idem + 🪶 Chaud/Machine 🦅 = les 2 · 🪶 Calme/💥🦎 🦅 = +1 pari allié → ⭐ |
| **Plancher (`M4`)** | `PLUME` | `PLUME`, `ROUGE` | `ROUGE`, `ECAILLE`, `PLUME` |
| **Synergies (`I01`)** | `BLEU` | — | `DEFENSEUR_ATTENTE`, `PERCHOIR`, `GARDIEN` |
| **Sorties (`I03`)** | `PIEGE`, `CROC` | `BLEU`, `ECAILLE` | `DEFENSEUR_REDEPLOYE`, `PARI_GLISSE`, `ECAILLE`, `BLEU`, `CROC` |

- **Panel 1 — L’Iguane vert, dormeur des hautes branches** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.
  - **Face 1** :
  > La chute au cri des oiseaux. Quand l’Iguane vert s’active, il se laisse tomber : posez 1 Piège sur une parcelle ciblée qui n’en porte pas encore, sur le rayon désigné par la Plume de Vigie, ou visée par une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu ou ne signale aucune parcelle ciblée, il tombe au plus près : sur une parcelle ciblée du rayon Reptile ou du rayon de l’Oiseau. S’il n’y en a aucune, il guette : posez le Piège sur n’importe quelle parcelle libre de Piège ordinaire du rayon Reptile, où il attendra la prochaine frappe.
  > Boire la chaleur (amplificateur) : avant de tomber, vous pouvez boire 1 Bleu : retirez-le d’une machine de n’importe quel rayon et remettez-le dans la réserve (la machine perd la Surchauffe correspondante). Gorgé de chaleur, l’Iguane tombe avec ses mâchoires : si le Croc est dans la réserve Reptile, postez-le sur la parcelle du Piège. Il y pare en premier, le Piège ensuite.
  - **Face 2** :
  > Le plongeon. Quand l’Iguane vert s’active, il plonge où il veut : posez 1 Piège sur n’importe quelle parcelle ciblée qui n’en porte pas encore, de n’importe quel rayon, et postez-y le Croc s’il est dans la réserve Reptile (si la Plume de Vigie est face Chaud, prenez le Croc où qu’il se trouve sur le plateau). Le Croc pare en premier, le Piège ensuite.
  > Boire la chaleur (amplificateur) : avant de plonger, vous pouvez boire 1 Bleu (retiré d’une machine de n’importe quel rayon, rendu à la réserve) : l’Iguane plonge une seconde fois et pose 1 second Piège sur une autre parcelle ciblée libre de Piège ordinaire. Chacune de ces parades allume Piégeage.
  - **Dilemme** — *Choix* : Tomber seul là où la Plume l’indique, ou boire un Bleu pour emporter le Croc (Face 1) ou plonger deux fois (Face 2) ; de préférence le Bleu d’une machine déjà annulée, ou dont le Seuil est déjà tombé à 1. · *Renoncement* : La machine qui perd son Bleu redevient plus difficile à parer, et ce Bleu manquera au Toucan pour la faire caler ; le Croc emporté ne garde plus la parcelle où une Écaille l’avait posté.
  - **Double activation** : Chaque Piège qui pare allume Piégeage, l’icône de l’Iguane : la chute appelle la chute, une fois par pari. Deux chutes couvrent les deux parcelles d’un « En avançant » (Sur place et Devant), ou deux fois la même parcelle visée par l’Abatteuse puis le Bulldozer. Avec le Toucan à ses côtés, chaque chute boit son Bleu : le Croc tombe à chaque fois s’il a regagné la réserve (Face 1), et quatre Pièges couvrent la forêt (Face 2).
  - **Témoin `G5_T1`** : Plancher sans Toucan (Tour 2, Acte 1) : aucun Bleu en jeu. La Plume est posée face Chaud au pied du rayon O, dont la parcelle 2 est visée au rang 4 par l’Abatteuse (Sur place) puis au rang 5 par le Bulldozer (Devant). Un Piège pare au rang 1 (Piégeage) : l’Iguane (2 paris) tombe sur la parcelle 2 ; au rang 4 son Piège pare l’Abatteuse (Piégeage), seconde activation, nouveau Piège sur la même parcelle qui pare le Bulldozer au rang 5.

- **Panel 2 — L’Iguane vert** *(Brique fluide · ACTIVATION / **Parade**)*
  - *Ambiance* : Entre soleil et feuillage, l’iguane change de branche et le fleuve change de couleur sous lui.
  - **Face 1** :
  > À chaque activation, si la Plume montre Chaud, choisissez un rayon et prenez un Rouge sur une de ses machines. Posez-le face Bleue sur l’autre machine du même rayon. Si elle montre Calme, vous pouvez glisser une Écaille de la réserve dans le sac.
  - **Face 2** :
  > À chaque activation, choisissez entre glisser une Écaille de la réserve dans le sac et transférer un Rouge d’une machine, face Bleue, sur l’autre de son rayon. Si la Plume indique ce rayon, le Bleu peut aussi rester sur la machine d’origine.
  - **Dilemme** — *Choix* : Quelle machine doit profiter de l’ombre ? · *Renoncement* : En transférant le jeton, on laisse la donneuse sans la réduction bleue.
  - **Double activation** : Deux transferts peuvent faire basculer un seuil élevé. En Face 2, mue et transfert restent deux choix indépendants.
  - **Témoin `G5_T1`** : Plume Chaud. Un Rouge quitte l’Abatteuse pour devenir le premier Bleu du Bulldozer. Le Toucan peut désormais installer un Piège sur une cible de ce dernier.

- **Panel 3 — L’Iguane vert, Guetteur Solaire des Cimes** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : « Immobile à la cime baignée de soleil, il boit la fièvre de l'acier et guide le vol des sentinelles. »
  - **Face 1** :
  > À l'activation (son Défenseur en pari glissant normalement dans son encoche), résolvez successivement :
  > 1. Relais d'Éveil : relevez 1 Défenseur couché en attente (bâtisseur en lisière ou pion de rive couché) — ou déplacez 1 Défenseur debout depuis une parcelle non ciblée — vers une parcelle de forêt de votre choix (où il participe aux Parades restantes). S'il rejoint le rayon ou une parcelle visée par le rang marqué par la Plume de Vigie (ou si aucun Défenseur n'est disponible à redéployer), faites en outre glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir).
  > 2. Bain Solaire — choisissez l'une des deux actions :
  > • Insolation : retournez 1 jeton Rouge existant en Bleu Surchauffe sur 1 machine du plateau ; si cette machine n'a aucun Rouge, reculez-la d'1 parcelle vers la bordure (si mobile) ou posez/déplacez le Croc sur sa parcelle.
  > • Mue de Vigie : versez 1 jeton Écaille de la réserve Reptile dans le sac opaque (s'il n'en reste plus, posez ou déplacez le Croc sur toute parcelle) ; si le Perchoir de Vigie porte un jeton face cachée, vous pouvez le révéler sur le Perchoir (et poser/déplacer le Croc si c'est une Écaille).
  - **Face 2** :
  > Résolvez Relais d'Éveil puis Bain Solaire (comme en Face 1), enrichis par l'état public de la Vigie d'Oiseau :
  > • Si la Plume de Vigie affiche Chaud ou si une Machine est visible sur le Perchoir, résolvez les deux actions de Bain Solaire (Insolation ET Mue de Vigie).
  > • Si la Plume de Vigie affiche Calme ou si un Sabotage ou une Écaille est visible sur le Perchoir, faites en outre glisser 1 Défenseur encore posé en pari sur un autre Gardien construit vers une encoche libre de ce Gardien (sans déclencher son pouvoir).
  - **Dilemme** — *Choix* : Orienter au déploiement la Plume sur Chaud pour cumuler Insolation et Mue de Vigie, ou sur Calme pour sécuriser un pari Gardien allié ; choisir à l'activation où projeter le Défenseur relevé (colmater une parcelle critique ou suivre la Plume). · *Renoncement* : Sans Machine visible sur le Perchoir, la Plume ne peut pas offrir à la fois le double Bain Solaire (Chaud) et le glissement de pari bonus (Calme).
  - **Double activation** : Engager 2 Défenseurs sur G5 conserve intacts les engagements visuels de ses encoches tout en projetant des renforts : la 1re activation relève un Défenseur couché en attente (ou déplace un Défenseur d'une parcelle non ciblée) sur une parcelle menacée d'un rang ultérieur, aidant à réussir la 2nde Parade qui fait glisser le 2nd pari de G5 dans sa seconde encoche et double la production d'Écailles et de conversions Rouge → Bleu.
  - **Témoin `G5_T1`** : Tour 3 (Acte 1), G5 Face 2 sur Parade (1 pari), Plume Calme au pied du rayon R, Machine visible sur le Perchoir (via G6), 1 bâtisseur couché en attente et 1 pari en attente sur un Gardien Rêve. Aux attaques, une Parade au rang 1 active G5 (son parieur glisse dans son encoche) : Relais d'Éveil relève le bâtisseur en parcelle 3 de R (rayon Plume), la Machine sur le Perchoir cumule Insolation (Rouge → Bleu sur l'Abatteuse de R, seuil 4 → 2) + Mue de Vigie (+1 Écaille au sac), et Plume Calme fait glisser le pari du Gardien Rêve dans son encoche libre.

#### Emplacement `G6` (`O>R` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Toucan toco, le bec-radiateur** | **Le Toucan toco** | **Le Toucan toco, Contrebandier du Kapokier** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | ⭐ Éveil (`ACTION`) | ⚡ Twist 2K3 (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Résonance** | ACTIVATION / **Piégeage** | ACTIVATION / **Sabotage** |
| **Pictogrammes** | 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` · 🪶 `PIC_PLUME` · 🚫 `PIC_ANNULATION` | 🔢 `PIC_RANG_MACHINE` · 💥 `PIC_SABOTAGE` · 🔵 `PIC_BLEU` · 🪶 `PIC_PLUME` | 🦅 `PIC_PERCHOIR` · ⚡ `PIC_TWIST` · 🔵 `PIC_BLEU` · 🦷 `PIC_CROC` |
| **Résumé Mini-Tuile** | Rend la chaleur aux machines | Sur place ↔ Devant / Bleu · échange des dés du rayon | Échange de machine via Perchoir |
| **Mots-clés Face 1** | 1 Rouge → Bleu sur la cible désignée par la Plume | Appel bref | Révéler 🦅 + 1 🔴→🔵 (si 0 🔴 : ⏪ 1 ou 🪤) · + 🪤 si 💥 · + 🦷 si 🦎 |
| **Mots-clés Face 2** | 1 Rouge → Bleu partout · 0 Rouge et 2 Bleus = machine calée | Écho thermique | Révéler 🦅 : échanger 💥/🦎 contre 1 Machine active (+ 🦷 si 🦎) OU Piqué (x2 si Machine sur 🦅) |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `ROUGE`, `PLUME` | `RANG_MACHINE`, `SABOTAGE` | `PERCHOIR`, `ROUGE`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `BLEU` | `BLEU` | `SABOTAGE`, `ECAILLE` |
| **Sorties (`I03`)** | `BLEU`, `ANNULATION_SURCHAUFFE` | `RANG_MACHINE`, `SABOTAGE` | `ANNULATION`, `BLEU`, `PIEGE`, `RECUL` |

- **Panel 1 — Le Toucan toco, le bec-radiateur** *(Brique fluide · ACTIVATION / **Résonance**)*
  - *Ambiance* : Le bec du toucan toco est un radiateur vivant : il y dirige son sang pour relâcher la chaleur du jour. Au-dessus des machines brûlantes, il rend la fournaise au monde, et le métal s’essouffle.
  - **Face 1** :
  > Quand le Toucan toco s’active : il rayonne : retournez 1 Rouge en Bleu sur une machine, mobile ou en Ratissage, du rayon désigné par la Plume de Vigie, ou sur une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu, visez une machine du rayon de l’Oiseau ou d’un rayon voisin.
  - **Face 2** :
  > Quand le Toucan toco s’active : il rayonne sur toute la forêt : retournez 1 Rouge en Bleu sur une machine de n’importe quel rayon, mobile ou en Ratissage. Coup de chaleur : si cette machine ne porte alors plus aucun Rouge mais au moins 2 Bleus, et qu’elle n’a pas encore attaqué, elle cale : inclinez son jeton Machine à 90° (pour une machine en Ratissage, tournez la machine elle-même d’un quart de tour) ; elle est annulée jusqu’au ménage, où elle reprend sa position.
  - **Dilemme** — *Choix* : Disperser la Surchauffe pour abaisser plusieurs Seuils, ou la concentrer sur une seule machine pour la faire caler (Face 2). · *Renoncement* : Chaque Bleu concentré sur la machine à caler n’aide pas les autres parades ; et l’Iguane voisin voudra boire ces mêmes Bleus.
  - **Double activation** : La surchauffe se construit en deux temps : la première activation convertit un Rouge, la seconde le dernier Rouge de la même machine ; en Face 2, celle-ci cale aussitôt (0 Rouge, 2 Bleus) avant même d’attaquer. Sur Résonance, le Toucan s’active de nouveau à chaque 1re activation d’un autre Gardien.
  - **Témoin `G6_T1`** : Abatteuse en Mode Assaut, 2 Rouges, parcelle gravée 3 (Seuil 5) ; le Toucan s’active : 1 Rouge et 1 Bleu, Seuil 3.

- **Panel 2 — Le Toucan toco** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : Un cri désigne l’arbre. Son écho désigne celui d’à côté.
  - **Face 1** :
  > Appel bref. Choisissez une mobile à jouer. Déplacez son dé entre les rangs 1 et 2, ou entre 4 et 5, dans un sens ou dans l’autre (en cours d’attaques, vers un rang strictement ultérieur au rang en cours). Elle garde son mode et change de cible entre Sur place et Devant. Vous pouvez choisir la fausse alerte à la place et glisser un Sabotage ordinaire de la réserve dans le sac. Il y attend une prochaine pioche.
  - **Face 2** :
  > Écho thermique. Vous gardez les deux appels de la Face 1. Une troisième possibilité s’ouvre si les deux mobiles d’un même rayon sont à jouer à des rangs différents et que l’une porte un Bleu. Échangez leurs rangs. Chacune lit toute la tactique et le mode de son nouveau rang. Le Bleu reste sur sa machine. Les jetons Machine restent devant leur rayon.
  - **Dilemme** — *Choix* : Décaler une attaque pour la livrer à un Piège ou à des Défenseurs dès ce tour, ou choisir la fausse alerte pour améliorer les pioches futures ; en Face 2, échanger deux rangs via un Bleu. · *Renoncement* : La fausse alerte ne soulage pas le tour en cours ; l’échange de Face 2 engage à la fois les tactiques et les modes des deux attaques du rayon.
  - **Double activation** : Le premier cri peut envoyer une mobile sur une case piégée. Si cette frappe déclenche le deuxième passage, le Toucan peut encore décaler une attaque ultérieure ou alimenter le sac.
  - **Témoin `G6_T1`** : En Acte 1, l’Abatteuse R·2 (rang 4, 1 Rouge) et le Bulldozer R·1 (rang 2, nu). G5 (Plume Chaud) dépose le Rouge de l’Abatteuse face Bleue sur le Bulldozer. Un Piège active G6 Face 2 : les dés 2 et 4 s’échangent. L’Abatteuse frappe R·3 en Charge au rang 2 et le Bulldozer frappe R·1 en Assaut au rang 4 au seuil de 1 grâce au Bleu.

- **Panel 3 — Le Toucan toco, Contrebandier du Kapokier** *(⚡ Twist 2K3 · ACTIVATION / **Sabotage**)*
  - *Ambiance* : « D'un claquement de bec au sommet du kapokier, il escamote la menace dans les feuillages avant que la piste ne s'ouvre. »
  - **Face 1** :
  > S'il y a un jeton face cachée sur le Perchoir de Vigie, révélez-le (il y reste face visible). Ciblez ensuite 1 machine du plateau : retournez sur elle 1 jeton Rouge existant en Bleu Surchauffe — ou, si cette machine ne porte aucun Rouge, au choix reculez-la d'1 parcelle vers la bordure (si mobile) ou posez 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire de son rayon.
  > Bonus de Perchoir : si le jeton visible sur le Perchoir est un Sabotage, posez en plus 1 Piège ordinaire sur toute parcelle dépourvue de Piège ordinaire ; s'il s'agit d'une Écaille, posez ou déplacez en plus le pion Croc sur toute parcelle. (Si le Perchoir est vide ou montre une Machine, seul l'effet de base s'applique.)
  - **Face 2** :
  > S'il y a un jeton face cachée sur le Perchoir de Vigie, révélez-le, puis choisissez l'un des deux modes :
  > 1. Échange de Vigie (uniquement si le Perchoir porte un Sabotage ou une Écaille) : échangez ce jeton avec 1 jeton Machine actif non annulé (n'ayant pas encore agi ce tour) situé devant n'importe quel rayon. Cette Machine est placée face visible sur le Perchoir : elle libère son dé de rang, n'agit pas ce tour et, si l'échange a lieu avant la Furtivité, ne compte plus dans m(r) lors de la Furtivité. Le Sabotage ou l'Écaille prend sa place devant ce rayon sans relancer de balayage Gardiens ; si c'est une Écaille, posez ou déplacez en plus le Croc sur toute parcelle.
  > 2. Piqué Thermique (toujours disponible, quel que soit l'état du Perchoir) : appliquez l'effet de base de la Face 1 (1 Rouge → Bleu, ou à défaut de Rouge sur la machine : Recul d'1 parcelle si mobile ou 1 Piège ordinaire sur son rayon) ; si une Machine est visible sur le Perchoir, appliquez cet effet de base sur jusqu'à 2 machines distinctes.
  - **Dilemme** — *Choix* : Inverser dès la pioche le choix habituel d'Oiseau : garder la Machine sous son paravent et cacher un Sabotage ou une Écaille sur le Perchoir pour capturer en Face 2 la pire Machine révélée sur toute la table. · *Renoncement* : Cacher un Sabotage ou une Écaille sur le Perchoir renonce à son déclenchement immédiat à l'ouverture au profit de l'échange ciblé.
  - **Double activation** : Les deux activations en Face 2 s'enchaînent naturellement l'une dans l'autre : lors de la 1re activation, Échange de Vigie extrait un Sabotage ou une Écaille du Perchoir et y enferme une Machine active ; lors de la 2nde activation dans le même tour, puisque cette Machine occupe désormais le Perchoir, Piqué Thermique est automatiquement survolté et refroidit (Rouge → Bleu), recule ou piège 2 autres machines distinctes sur le plateau.
  - **Témoin `G6_T1`** : Tour 3 (Acte 1), O garde sa Machine et cache 1 Écaille sur le Perchoir ; G6 Face 2 sur Sabotage (2 paris), 2 Défenseurs sur la Rive Sabotage de R. À l'ouverture, 1er Sabotage → Échange de Vigie capture la Machine de R sur le Perchoir et pose le Croc en parcelle 2 d'O ; 2nd Sabotage → Piqué Thermique survolté (x2) recule l'Abatteuse d'O et refroidit un Bulldozer. À la Furtivité, m(R)=0 gagne la Rive Sabotage.

---

## B. Lisières Animal ↔ Onirique (6 lisières · 6 Gardiens + 6 Rêves)

<a id="lisiere-m-h-g7-r3"></a>
### Lisière `M ↔ H` — Mammifères ↔ Humains (`G7` & `R3`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G7`** (`M>H`, GARDIEN) | **Le Tapir, jardinier des sentiers** — Change les Routes en sentiers où les machines s’enlisent (⚡ Twist 2K3 · 🌱 Enracinement · sortie `SENTIER_ROUTE`) | **Le Tapir** — Guide + Duel · pas du Chamane / permutation / repousse en amont (⭐ Éveil · 🌱 Enracinement · sortie `DEFENSEUR_REDEPLOYE`) | **Le Tapir, Ouvreur des Sentiers Profonds** — Refroidir ou reculer, déplacer Duel (⭐ Éveil · sortie `BLEU`) |
| **`R3`** (`H>M`, REVE) | **La Vision du Chamane-Jaguar** — Annule puis bondit défendre la forêt (Brique fluide · sortie `CHAMANE_EN_FORET`) | **Les Pas dans l’eau** — Défi devant · Tenu derrière (Brique fluide · sortie `PIEGE`) | **L’Appel du Singe Hurleur** — Piéger les sentes, enracinement bonifié (🌱 Enracinement · sortie `PIEGE`) |

#### Emplacement `G7` (`M>H` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Tapir, jardinier des sentiers** | **Le Tapir** | **Le Tapir, Ouvreur des Sentiers Profonds** |
| **Rôles & Nature** | ⚡ Twist 2K3 · 🌱 Enracinement (`ACTION`) | ⭐ Éveil · 🌱 Enracinement (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Parade** | ACTIVATION / **Sabotage** | ACTIVATION / **Parade** |
| **Pictogrammes** | ⚡ `PIC_TWIST` · 🛣️ `PIC_ROUTE` · ⚔️ `PIC_DUEL` · 🥁 `PIC_TAMBOUR` | ⚔️ `PIC_DUEL` · 🥁 `PIC_TAMBOUR` · 🎶 `PIC_CHANT` · 🌱 `PIC_ENRACINEMENT` | 🔵 `PIC_BLEU` · ⏪ `PIC_RECUL` · ⚔️ `PIC_DUEL` · 🥁 `PIC_TAMBOUR` |
| **Résumé Mini-Tuile** | Change les Routes en sentiers où les machines s’enlisent | Guide + Duel · pas du Chamane / permutation / repousse en amont | Refroidir ou reculer, déplacer Duel |
| **Mots-clés Face 1** | Duel ou Chamane sur Route = sentier (parcelle vide, plus sautée) · sinon Duel → Chamane = Territoire tenu | Ouvrir la sente | 1x [🔴→🔵 ou ⏪ 1] + relayer ⚔️ (🥁/🎶 : 🌙 ←1) |
| **Mots-clés Face 2** | + frappes des parcelles voisines détournées sur le sentier · l’Abatteuse n’en déloge plus le Duel | Croisée du Chant | 2x [🔴→🔵 et/ou ⏪ 1] + relayer ⚔️ (🥁/🎶 : 2 🌙 ←1) |
| **Mots-clés Enraciné** | Fin de partie : Duel + Chamane sur une parcelle = 1 repousse de plus | Souche en amont · Final | — |
| **Plancher (`M4`)** | `ROUTE`, `DUEL`, `TAMBOUR`, `CHANT` | `DUEL`, `DEFENSEUR_ATTENTE`, `TAMBOUR`, `CHANT` | `ROUGE`, `DUEL`, `TAMBOUR`, `CHANT` |
| **Synergies (`I01`)** | `CHAMANE_EN_FORET` | `SOUCHE` | `POSITION_REVE` |
| **Sorties (`I03`)** | `SENTIER_ROUTE`, `TERRITOIRE`, `ARBRE` | `DEFENSEUR_REDEPLOYE`, `DUEL`, `ARBRE` | `BLEU`, `RECUL`, `TERRITOIRE`, `RANG_REVE` |

- **Panel 1 — Le Tapir, jardinier des sentiers** *(⚡ Twist 2K3 · 🌱 Enracinement · ACTIVATION / **Parade**)*
  - *Ambiance* : Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.
  - **Face 1** :
  > Le sentier battu. Quand le Tapir s’active, choisissez l’un de ses deux pas :
  > • Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon — pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère —, ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon. Cette Route devient un sentier.
  > • Frayer (toujours possible, même sans aucune Route en jeu) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère. S’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu : les hommes tiennent déjà ce terrain.
  > Le sentier : (1) tant qu’il porte le Duel ou un Chamane, le sentier compte comme une parcelle, avec le chiffre gravé de sa case, bien qu’il ne porte ni Arbre ni Souche ; (2) les machines ne le sautent plus : une frappe Devant le vise, une avancée s’y arrête, et une frappe sur le sentier ne fait jamais gagner de Rouge ; (3) il accueille Défenseurs, Piège et autres pièces de défense comme toute parcelle, et le Duel y suit ses règles habituelles (parade → Territoire tenu ; frappe non parée et non piégée → retour en réserve) ; (4) une frappe de Bulldozer non parée le refait Route, et dès qu’il ne porte plus ni Duel ni Chamane (frappe, déplacement, retour des Défenseurs au ménage), il redevient Route : la case est vidée et toute machine qui s’y trouve se replie comme sur une Route qui vient de se créer ; (5) jamais de sentier sur la dernière case d’un rayon, tout sentier redevient aussitôt Route si le Tapir quitte la Piste des Gardiens, et aucun pion Arbre ou Souche n’est jamais déplacé.
  - **Face 2** :
  > Le sentier qui égare. Quand le Tapir s’active, choisissez l’un de ses deux pas :
  > • Fouler une Route : posez le jeton Duel sur une Route Forestière de n’importe quel rayon (pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère), ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon : elle devient un sentier.
  > • Frayer (toujours possible) : posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère ; s’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu.
  > En Face 2, le sentier obéit aux règles du sentier avec deux pas de plus :
  > • Les machines s’égarent : quand une machine attaque, avant de figer ses cibles, si l’une d’elles est la parcelle juste avant ou juste après un sentier sur ce rayon, vous pouvez détourner cette frappe sur le sentier.
  > • La boue tient : une frappe d’Abatteuse non parée sur un sentier ne déloge plus le Duel : seul un Bulldozer non paré refait la Route.
  - **Enraciné** :
  > Les graines du sentier. Au décompte final, en plus de sa repousse habituelle (1 Souche, ou 2 s’il était en Face 2, sur la parcelle qu’il regarde), le Tapir fait repousser 1 Souche de la parcelle qui porte le jeton Duel, si le Tambour ou le Chant s’y tient aussi. Cette clause ne se lit qu’au décompte final.
  - **Dilemme** — *Choix* : Fouler une Route — avec le Duel, qui tient d’un tour à l’autre, ou avec un Chamane, jusqu’au ménage — ou frayer pour poster le Duel en Territoire tenu auprès d’un Chamane. · *Renoncement* : Le Duel posé sur un sentier ne garde plus aucune parcelle boisée ; le Chamane qui descend abandonne la parcelle qu’il gardait ; un Bulldozer non paré refait la Route en vidant la case.
  - **Double activation** : Deux pas, deux sentiers : la première activation pose le Duel sur une Route, la seconde y fait descendre un Chamane sur une autre, ou sur la même pour que le sentier survive au départ du Duel. Chaque frappe parée sur un sentier allume Parade, l’icône du Tapir. En Face 2, chaque sentier attire en plus les frappes de ses deux voisines.
  - **Témoin `G7_T1`** : Le sentier tenu par le Tambour (Tour 3, Acte 1) : sur le rayon H, parcelle 1 (2 Arbres) porte Bulldozer (rang 3), Abatteuse (rang 5) et Tambour ; parcelle 2 est une Route ; parcelle 3 porte 3 Arbres. Après une parade au rang 1, le Tapir (sur Parade) fait descendre le Tambour sur la Route (sentier gravé 2). Au rang 3 le Bulldozer frappe la parcelle 1 puis le sentier (paré par le Tambour, Parade) et s’arrête sur le sentier ; au rang 5 l’Abatteuse frappe le sentier à vide ; au ménage le sentier redevient Route et le Bulldozer se replie en parcelle 1. Parcelle 3 intacte.

- **Panel 2 — Le Tapir** *(⭐ Éveil · 🌱 Enracinement · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Le premier passage coûte au tapir. Le second appartient à qui le suit.
  - **Face 1** :
  > Ouvrir la sente. Prenez un de vos Défenseurs hors Gardien et hors encoche, y compris sur une rive, un Rêve, une lisière ou en attente. Placez-le debout sur une parcelle de M ou H (ou sur une parcelle survivante d’un autre rayon si M et H sont entièrement Route) avec le Duel, repris en réserve ou en forêt et tourné sur Défi. Si le Tambour ou le Chant se trouve à un pas radial de l’arrivée, vous pouvez l’y conduire. Le Chamane et le guide compteront tous deux à la Parade. Vous pouvez choisir une parcelle où le Chamane se trouve déjà.
  - **Face 2** :
  > Croisée du Chant. Vous pouvez ouvrir la sente. Vous pouvez aussi permuter un Défenseur Mammifère et un Chamane, si l’un se trouve sur le Duel et l’autre sur une autre parcelle ou sur un Rêve. Échangez physiquement leurs postes. Le Duel garde sa face et sa parcelle. Le Chant arrivé sur un Rêve encore à lire y exercera son pouvoir à l’ouverture. Un Rêve déjà lu poursuit son tour.
  - **Enraciné** :
  > Au décompte final. Si la parcelle désignée a survécu, appliquez-y la repousse ordinaire. Puis vous pouvez retourner une Souche sur la prochaine parcelle non-Route de ce rayon, côté cœur, même si la première parcelle n’avait plus de Souche. À défaut de parcelle ou de Souche en amont, le bonus vaut zéro.
  - **Dilemme** — *Choix* : Réunir le Tambour et le Duel pour donner à R3 les deux directions de pose de son Piège, ou permuter le Chant sur la Réglette en Face 2. · *Renoncement* : Envoyer le Chant sur la Réglette peut ouvrir le Sommeil, au prix d’un défenseur de front ; reprendre le Duel le remet sur sa face Défi.
  - **Double activation** : Une première percée rassemble deux pions. En Face 2, le second passage peut échanger le Chamane arrivé avec un Mammifère déjà sur un Rêve. Le Duel reste couvert.
  - **Témoin `G7_T1`** : Avant la lecture de R3, G7 ouvre la sente en M·2 avec un Mammifère et y amène le Tambour depuis M·1 : R3 défendu peut poser son Piège en M·1 ou M·3. Enraciné Face 2 devant M·2 (2 Souches en M·2, 1 en M·3), les trois Souches survivantes se retournent au décompte final (deux au pied de la tuile et une en amont).

- **Panel 3 — Le Tapir, Ouvreur des Sentiers Profonds** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : « Lourd comme le tonnerre sourd du tambour, il fend les broussailles pour porter le défi là où la lisière vacille. »
  - **Face 1** :
  > À l'activation de ce Gardien, sur 1 machine au choix, retournez 1 jeton Rouge existant en Bleu Surchauffe OU reculez-la d'1 parcelle vers la bordure si elle est mobile (en sautant radialement toute Route Forestière). Vous pouvez ensuite déplacer le jeton Duel (face Territoire tenu) vers une autre parcelle ayant au moins 1 Défenseur.
  > Accord M>H : si le Duel se trouve alors sur le rayon du Tambour, ou si la machine ciblée est sur le rang du Chant, glissez 1 Rêve d'1 rang libre à gauche.
  - **Face 2** :
  > À l'activation de ce Gardien, appliquez deux fois l'effet physique sur 1 ou 2 machines (retourner 1 jeton Rouge existant en Bleu Surchauffe et/ou reculer d'1 parcelle une machine mobile). Vous pouvez ensuite déplacer le jeton Duel (face Territoire tenu) vers une autre parcelle ayant au moins 1 Défenseur.
  > Accord M>H : si le Duel occupe le rayon du Tambour ou si au moins une machine ciblée est sur le rang du Chant, glissez jusqu'à 2 Rêves d'1 rang libre à gauche (ou un même Rêve de 2 rangs libres à gauche).
  - **Dilemme** — *Choix* : Refroidir (Rouge → Bleu) une machine chaude pour abaisser durablement son Seuil dans tous les modes, ou reculer une machine mobile loin d'une parcelle gravée 3 / du Ratissage ; relayer le Duel sur le rayon du Tambour pour faire glisser un Rêve. · *Renoncement* : Déraciner le Duel de sa parcelle initiale expose celle-ci à une seconde machine plus tardive.
  - **Double activation** : Engager 2 Défenseurs sur G7 crée un effet domino naturel sur l'icône Parade : une première Parade facile en début d'attaques déclenche la 1re activation de G7, qui abaisse le Seuil d'une machine d'un rang ultérieur (Rouge → Bleu et/ou Recul) tout en relayant le Duel sur sa parcelle pour bloquer l'avancée +1 ; cette seconde parcelle réussit alors sa Parade et rallume Parade pour le 2nd pari de G7.
  - **Témoin `G7_T1`** : Tour 3 (Acte 1, 4 joueurs), G7 Face 1 sur Parade (2 paris). Au rang 3, Parade sur M (Duel bloque l'avancée) → 1re activation de G7 : retourne le Rouge du Bulldozer de H (rang 6) en Bleu, relaie le Duel (Territoire tenu) en parcelle 3 de H (rayon du Tambour) et glisse un Rêve du rang 4 au rang 3. Au rang 6, seuil du Bulldozer réduit de 3 à 1 → Parade réussie, 2nde activation de G7 qui le recule en parcelle 2 et passage Face 2.

#### Emplacement `R3` (`H>M` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Vision du Chamane-Jaguar** | **Les Pas dans l’eau** | **L’Appel du Singe Hurleur** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | Brique fluide (`ACTION`) | 🌱 Enracinement (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | 🌙 `PIC_REVE` · 🛡️ `PIC_DEFENSEUR` · ⚔️ `PIC_DUEL` | ⚔️ `PIC_DUEL` · 🥁 `PIC_TAMBOUR` · 🪤 `PIC_PIEGE` | 🪤 `PIC_PIEGE` · 🥁 `PIC_TAMBOUR` · ⚔️ `PIC_DUEL` · 🌱 `PIC_ENRACINEMENT` |
| **Résumé Mini-Tuile** | Annule puis bondit défendre la forêt | Défi devant · Tenu derrière | Piéger les sentes, enracinement bonifié |
| **Mots-clés Face 1** | Après annulation · ses Défenseurs bondissent vers le Duel ou une parcelle visée | Défi devant · Tenu derrière | +1 🪤 (🥁/⚔️) · avec 🎶 et/ou ⚔️ : 🔴→🔵 et/ou 🌙 ←1 |
| **Mots-clés Enraciné** | — | — | Décompte final : régénère 2 🪵 sur H + 1 🪵 sur rayon allié 0-Route (priorité M) |
| **Plancher (`M4`)** | `RANG_REVE`, `DUEL` | `DUEL`, `TERRITOIRE`, `ROUTE` | `POSITION_REVE`, `TAMBOUR`, `DUEL` |
| **Synergies (`I01`)** | `ANNULATION` | `TAMBOUR` | `CHANT`, `ROUGE`, `SOUCHE` |
| **Sorties (`I03`)** | `CHAMANE_EN_FORET`, `DEFENSEUR_REDEPLOYE`, `TERRITOIRE` | `PIEGE` | `PIEGE`, `BLEU`, `RANG_REVE`, `ARBRE` |

- **Panel 1 — La Vision du Chamane-Jaguar** *(Brique fluide · OUVERTURE)*
  - *Ambiance* : Chez les peuples du Haut Rio Negro, un même mot désigne le chamane et le jaguar. Quand la vision le prend, le chamane quitte le rêve sur quatre pattes et bondit là où la forêt saigne.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution : une fois ses annulations faites, chaque Défenseur posé sur ce Rêve peut bondir hors de lui, sur sa face Définitif, vers la parcelle qui porte le jeton Duel, ou vers une parcelle ciblée du rayon d’une machine que ce Rêve vient d’annuler. Il y compte pour toutes les parades à venir. Sur la parcelle du Duel, un Défenseur Humain arrivé ainsi compte comme un Défenseur Mammifère pour retourner le Duel sur Territoire tenu.
  - **Dilemme** — *Choix* : Où bondir : sur le Duel pour sceller un Territoire tenu, ou sur la parcelle visée du rayon dont une machine vient d’être annulée. · *Renoncement* : Engager un Défenseur sur ce Rêve, c’est parier qu’une machine tombera sur son rang : s’il n’annule rien, il ne peut bondir que vers le Duel.
  - **Témoin `R3_T1`** : Rêve H au rang 2 défendu par le Chant ; il annule l’Abatteuse du rayon M ; le Chant bondit sur la parcelle 3 du rayon M (Duel face Défi, 1 Défenseur M) ; la frappe du Bulldozer y est parée (Seuil 2) ; le Duel passe sur Territoire tenu.

- **Panel 2 — Les Pas dans l’eau** *(Brique fluide · OUVERTURE)*
  - *Ambiance* : À chaque pas du Tambour, une empreinte se remplit avant que la pluie ne tombe.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, si le Duel est en forêt, vous pouvez poser un Piège ordinaire de la réserve un pas radial vers le cœur depuis le Duel face Défi, ou vers la bordure depuis le Territoire tenu. Sautez les Routes. Si le Tambour est sur le Duel, vous choisissez le sens. Il faut une parcelle libre de Piège ordinaire.
  - **Dilemme** — *Choix* : Couvrir l’avancée ou garder l’arrière ? · *Renoncement* : Un Tambour engagé auprès du Duel ne défend pas un Rêve.
  - **Témoin `R3_T1`** : Le Duel face Défi est en M2, le Tambour aussi. Les Humains choisissent M1 derrière le Duel. Le Piège y intercepte un Bulldozer pendant que la Parade en M2 peut établir le Territoire tenu.

- **Panel 3 — L’Appel du Singe Hurleur** *(🌱 Enracinement · OUVERTURE)*
  - *Ambiance* : « Son cri d'aube court de cime en cime, scellant les frontières des grands fauves pour que la graine dorme jusqu'au renouveau. »
  - **Face 1** :
  > À l'ouverture, lorsque ce Rêve est défendu (après le choix éventuel des machines annulées), posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire du rayon portant le Tambour ou le jeton Duel (ou du rayon de H si aucune n'est éligible).
  > Écho territorial (H>M) : vérifiez combien des conditions suivantes sont réunies (0, 1 ou 2) : (1) le Chant occupe le rang de ce Rêve ou ce Rêve vient d'annuler au moins 1 machine ; (2) le jeton Duel est en jeu en forêt alliée.
  > • 1 condition : retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine de l'un de ces rayons, OU glissez 1 Rêve d'1 rang libre à gauche.
  > • 2 conditions : appliquez les deux effets ci-dessus (si aucune machine de ces rayons n'a de Rouge, posez à la place 1 second Piège ordinaire sur une autre parcelle dépourvue de Piège ordinaire des rayons du Tambour ou du Duel).
  - **Enraciné** :
  > Si H enracine volontairement cette tuile au ménage au pied de son rayon devant une parcelle non-Route, elle perd son pouvoir actif et rend impossible le Sommeil du Contremaître ; aucune Souche n'est retournée lors de la pose ni pendant les Tours 1 à 8. Uniquement lors du décompte final (quelle que soit la fin de partie), au lieu de régénérer 1 seule Souche, retournez jusqu'à 2 Souches existantes en Arbres debout sur leurs parcelles du rayon de H (en commençant par sa parcelle d'attache), plus 1 Souche existante en Arbre debout sur un autre rayon allié sans aucune Route Forestière (en priorité celui de M s'il est sans Route, sinon un rayon portant une autre tuile Enracinée).
  - **Dilemme** — *Choix* : Conserver R3 actif sur la Réglette pour tisser des Pièges protecteurs et garder ouverte la voie du Sommeil, ou l'enraciner au ménage avant qu'une Route ne condamne le rayon pour verrouiller jusqu'à 3 régénérations au décompte final. · *Renoncement* : Enraciner R3 ferme définitivement la victoire par Sommeil du Contremaître et éteint sa production de Pièges.
  - **Témoin `R3_T1`** : Tour 4, Tambour en parcelle 2 de H, Chant sur R3 au rang 3, Duel en parcelle 2 de M. À l'ouverture, R3 annule 1 machine au rang 3, pose 1 Piège en parcelle 2 de H, puis (2 conditions réunies) retourne 1 Rouge en Bleu sur M ET glisse un Rêve du rang 5 au rang 4. Enraciné au Tour 6 devant une parcelle non-Route (0 repousse immédiate), il retourne 2 Souches sur H + 1 Souche sur M sans Route au décompte final.

---

<a id="lisiere-m-e-g8-r7"></a>
### Lisière `M ↔ E` — Mammifères ↔ Entités Magiques (`G8` & `R7`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G8`** (`M>E`, GARDIEN) | **Le Boto, l’encantado du fleuve** — Fait nager les Rêves vers le rang 1 (⭐ Éveil · 🌙 Levier Rêve · sortie `POSITION_REVE`) | **Le Boto** — Écho · veilleur / Écho · plongeur (⭐ Éveil · sortie `DEFENSEUR_REDEPLOYE`) | **Le Boto, Enchanteur des Eaux Roses** — Refoule par les souches et altère (⚡ Twist 2K3 · sortie `RECUL`) |
| **`R7`** (`E>M`, REVE) | **Le Curupira, protecteur aux pieds retournés** — Les machines de son rang marchent à reculons (⚖️ Loi passive · sortie `RECUL`) | **La Pirogue sans rameur** — Remous · amarrage (🌙 Levier Rêve · sortie `ALTERATION`) | **Le Songe du Brame des Brumes** — Glisse un rêve, arme le Duel (🌙 Levier Rêve · sortie `RANG_REVE`) |

#### Emplacement `G8` (`M>E` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Boto, l’encantado du fleuve** | **Le Boto** | **Le Boto, Enchanteur des Eaux Roses** |
| **Rôles & Nature** | ⭐ Éveil · 🌙 Levier Rêve (`ACTION`) | ⭐ Éveil (`ACTION`) | ⚡ Twist 2K3 (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Rêve** | ACTIVATION / **Sabotage** | ACTIVATION / **Parade** |
| **Pictogrammes** | ⬅️ `PIC_AVANCEE_REVE` · 🌙 `PIC_REVE` · 🌀 `PIC_ALTERATION` | 🌀 `PIC_ALTERATION` · 🌙 `PIC_REVE` · ♻️ `PIC_DEFENSEUR_ATTENTE` · 🛡️ `PIC_DEFENSEUR` | ⏪ `PIC_RECUL` · 🌀 `PIC_ALTERATION` · 🔵 `PIC_BLEU` · ⚔️ `PIC_DUEL` |
| **Résumé Mini-Tuile** | Fait nager les Rêves vers le rang 1 | Écho · veilleur / Écho · plongeur | Refoule par les souches et altère |
| **Mots-clés Face 1** | 1 Rêve glisse d’1 rang à gauche ou échange avec son voisin · aucun Rêve ne nage = 1 Altération | Écho · veilleur | Recul 1 + Chenal Souches + 🌀 / 🔴→🔵 |
| **Mots-clés Face 2** | 1 Rêve glisse de 2 rangs ou plonge sous son voisin · ou échange · aucun Rêve ne nage = 1 Altération | Écho · plongeur | Toute mobile + 🌀 / 🔴→🔵 + Chenal + ⚔️ Tenu |
| **Mots-clés Enraciné** | — | — | Standard (1 ou 2 Souches finales) |
| **Plancher (`M4`)** | `POSITION_REVE`, `RANG_REVE` | `DEFENSEUR_ATTENTE`, `RANG_MACHINE`, `POSITION_REVE` | `SOUCHE`, `RANG_MACHINE`, `DUEL` |
| **Synergies (`I01`)** | — | `ALTERATION` | `ALTERATION`, `ROUGE` |
| **Sorties (`I03`)** | `POSITION_REVE`, `ALTERATION`, `ANNULATION` | `DEFENSEUR_REDEPLOYE` | `RECUL`, `ALTERATION`, `BLEU`, `TERRITOIRE` |

- **Panel 1 — Le Boto, l’encantado du fleuve** *(⭐ Éveil · 🌙 Levier Rêve · ACTIVATION / **Rêve**)*
  - *Ambiance* : Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.
  - **Face 1** :
  > La nage. Quand le Boto s’active : faites nager un Rêve : glissez-le d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent). Si ce rang est occupé, vous pouvez à la place échanger ce Rêve avec le Rêve qui l’occupe (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
  > L’encantado (plancher) : si aucun Rêve ne peut nager (Réglette sans Rêve, ou seul Rêve déjà au rang 1), le Boto envoûte à la place une machine : posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.
  - **Face 2** :
  > La plongée vers l’Encante. Quand le Boto s’active : faites glisser un Rêve d’1 ou 2 rangs libres vers la gauche (ses Défenseurs le suivent), ou faites-le plonger sous le Rêve qui le précède : il ressort sur le premier rang libre situé à gauche de celui-ci. Vous pouvez aussi, à la place, échanger deux Rêves voisins (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
  > L’encantado (plancher) : si aucun Rêve ne peut nager ni plonger, posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.
  - **Dilemme** — *Choix* : Faire nager le Rêve vers le rang où des machines viennent d’être révélées (annulation immédiate) ou vers le bloc du Sommeil ; sans Rêve, envoûter la machine qui menacera la parcelle la plus boisée à sa prochaine sortie. · *Renoncement* : Un Rêve déplacé quitte le rang qu’il couvrait : les machines qui y arriveraient ensuite (déviées ou relues) ne seront plus annulées.
  - **Double activation** : Deux nages font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2), ou compactent deux Rêves séparés : le plus court chemin vers le Sommeil quand les Humains ne sont pas à la table. Posé sur Rêve, le Boto nage dès la première annulation ; posé sur Sabotage, il déplace les Rêves avant même leur résolution. Sans Rêve, deux envoûtements sur deux machines différentes.
  - **Témoin `G8_T1`** : Rêve E au rang 5 non résolu, machine révélée au rang 4 ; un Rêve au rang 2 annule et allume Rêve ; le Boto s’active : le Rêve E passe au rang 4 et annule la machine.

- **Panel 2 — Le Boto** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Dans l’eau trouble, le boto tourne autour d’un tronc. Un second remous lui répond au-delà des branches.
  - **Face 1** :
  > À chaque activation, vous pouvez relever un bâtisseur en attente sur une parcelle encore ciblée de M ou E. Avant la résolution du premier Rêve, vous pouvez plutôt le poser sur un Rêve au rang d’une machine mobile visible et active.
  - **Face 2** :
  > À chaque activation, vous pouvez prendre un bâtisseur en attente ou un Défenseur en forêt et le poser sur une autre parcelle encore ciblée. Avant le premier Rêve, vous pouvez plutôt le poser sur un Rêve au rang d’une machine mobile visible et active, ou sur tout Rêve si une machine en forêt porte une Altération.
  - **Dilemme** — *Choix* : Faire entendre l’écho en forêt ou sur un Rêve ? · *Renoncement* : Un veilleur envoyé sur la Réglette ne compte plus au seuil de Parade en forêt.
  - **Double activation** : Deux appels peuvent garnir deux Rêves ou placer deux Défenseurs sur le même front forestier.
  - **Témoin `G8_T1`** : Un Sabotage active le Boto avant les Rêves. Il relève un bâtisseur sur le Rêve du rang 4. Celui-ci annule la machine de rang 4 et allume Rêve.

- **Panel 3 — Le Boto, Enchanteur des Eaux Roses** *(⚡ Twist 2K3 · ACTIVATION / **Parade**)*
  - *Ambiance* : « Dans le brouillard du fleuve en crue, chaque souche coupée devient un tourbillon qui ramène le fer à son point de départ. »
  - **Face 1** :
  > Lorsque Le Boto s'active, choisissez 1 machine mobile située sur le rayon Mammifère, sur le rayon Entités, sur le rayon portant le jeton Duel, ou portant déjà un jeton d'Altération :
  > 1. Chenal des Souches : faites reculer cette machine d'1 parcelle vers la bordure de son rayon ; puis, tant que la parcelle où elle se trouve ou la parcelle suivante vers la bordure contient au moins 1 Souche, continuez de la faire glisser vers la bordure à travers toutes ces parcelles consécutives à Souches (en sautant les Routes Forestières, sans dépasser la 1re parcelle du rayon). Tout jeton d'Altération déjà présent sur elle y demeure attaché.
  > 2. Brume Rose : si cette machine ne porte pas encore de jeton d'Altération — et qu'elle a traversé ou rejoint au moins 1 Souche (ou le jeton Duel), ou qu'elle était déjà sur la 1re parcelle — posez sur elle 1 jeton d'Altération de la réserve Entités. Si elle portait déjà un jeton d'Altération au début de cette activation et possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
  - **Face 2** :
  > Lorsque Le Boto s'active, choisissez n'importe quelle machine mobile du plateau :
  > 1. Si elle ne porte pas encore de jeton d'Altération, posez d'abord sur elle 1 jeton d'Altération de la réserve Entités ; si elle en portait déjà un et possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe. Faites-la ensuite reculer le long du Chenal des Souches comme en Face 1.
  > 2. Mirage du Détroit : vous pouvez déplacer immédiatement le jeton Duel (depuis la réserve Mammifère ou depuis sa parcelle actuelle) sur la parcelle d'arrivée de cette machine, directement tourné sur sa face Territoire tenu. Si le jeton Duel s'y trouvait déjà sur Territoire tenu, retournez 1 jeton Rouge d'une machine de ce rayon (mobile ou en Ratissage) sur sa face Bleue Surchauffe.
  - **Dilemme** — *Choix* : Exploiter une chaîne de Souches derrière le front comme toboggan de refoulement jusqu'à la bordure tout en altérant la machine ; en Face 2, verrouiller Territoire tenu sur la bordure rejointe. · *Renoncement* : Laisser des Souches intactes expose ces parcelles à un Bulldozer non neutralisé ; déplacer le Duel en Face 2 dégarnit le barrage précédemment tenu.
  - **Double activation** : Lors d'une double mise gagnante (ex. 2 parades dans le tour sur Parade), Le Boto refoule et altère deux machines distinctes — ou s'acharne deux fois sur la même machine mobile : la 1re activation la renvoie en bordure et l'altère, la 2nde convertit l'un de ses jetons Rouges en Bleu Surchauffe et y verrouille le Territoire tenu.
  - **Témoin `G8_T1`** : Tour 4, sur le rayon Entités, les parcelles 1, 2 et 3 portent chacune 1 Souche et l'Abatteuse est en parcelle 4 (1 Rouge, 0 Altération). Sur Parade, Le Boto Face 1 la recule en 3 (Souche) puis la fait glisser d'un trait à travers 2 jusqu'en parcelle 1 et pose sur elle 1 jeton d'Altération.

#### Emplacement `R7` (`E>M` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Curupira, protecteur aux pieds retournés** | **La Pirogue sans rameur** | **Le Songe du Brame des Brumes** |
| **Rôles & Nature** | ⚖️ Loi passive (`LOI_PASSIVE`) | 🌙 Levier Rêve (`ACTION`) | 🌙 Levier Rêve (`ACTION`) |
| **Fenêtre / Icône** | PERMANENT | OUVERTURE | OUVERTURE |
| **Pictogrammes** | ⚖️ `PIC_LOI_PASSIVE` · ⏪ `PIC_RECUL` · 🔢 `PIC_RANG_MACHINE` · ⚔️ `PIC_DUEL` | ⚔️ `PIC_DUEL` · 🌀 `PIC_ALTERATION` · ⬅️ `PIC_AVANCEE_REVE` | ⬅️ `PIC_AVANCEE_REVE` · ⚔️ `PIC_DUEL` · 🌀 `PIC_ALTERATION` · 🪵 `PIC_SOUCHE` |
| **Résumé Mini-Tuile** | Les machines de son rang marchent à reculons | Remous · amarrage | Glisse un rêve, arme le Duel |
| **Mots-clés Face 1** | Loi · à son rang Devant = derrière · avancée = recul · Sur place sans gain de Rouge | Remous · amarrage | Glisse 1G + [⚔️ Tenu & 🌀/🔴→🔵 OU 2e Glisse si 🪵/⚔️] |
| **Mots-clés Enraciné** | — | — | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `RANG_REVE`, `POSITION_REVE`, `RANG_MACHINE` | `DUEL`, `RANG_MACHINE`, `POSITION_REVE` | `POSITION_REVE`, `DUEL`, `SOUCHE` |
| **Synergies (`I01`)** | `DUEL` | — | `ALTERATION`, `ROUGE` |
| **Sorties (`I03`)** | `RECUL`, `TERRITOIRE` | `ALTERATION`, `RANG_REVE` | `RANG_REVE`, `TERRITOIRE`, `ALTERATION`, `BLEU` |

- **Panel 1 — Le Curupira, protecteur aux pieds retournés** *(⚖️ Loi passive · PERMANENT)*
  - *Ambiance* : Le Curupira protège les bêtes et punit qui abat trop d’arbres. Ses pieds tournés à l’envers laissent des traces qui égarent les chasseurs : qui croit le suivre s’éloigne de lui, et retourne d’où il vient.
  - **Face 1** :
  > Loi passive — Pieds à l’envers (tant que le Curupira est sur la Réglette, défendu ou non) : toute machine non annulée qui attaque depuis le rang du Curupira marche à reculons. Sa frappe « Devant » vise la parcelle située derrière elle, côté bordure (en sautant les Routes Forestières ; s’il n’y en a aucune, la frappe se perd). L’avancée d’« En avançant » devient un recul d’1 parcelle. Une frappe « Sur place » depuis ce rang ne fait gagner aucun Rouge en Mode Charge. Protecteur des bêtes : quand une machine recule ainsi hors de la parcelle qui porte le jeton Duel face Défi, retournez le Duel sur Territoire tenu. Comme tout Rêve défendu, le Curupira annule à son rang 1 machine par Défenseur : à vous de choisir celles que vous laissez marcher à reculons.
  - **Dilemme** — *Choix* : Annuler une machine de son rang, ou la laisser marcher à reculons : frappe derrière elle, puis recul d’1 parcelle. · *Renoncement* : Une machine laissée active frappe quand même : derrière elle, une parcelle de bordure encore boisée peut y perdre ses Arbres.
  - **Témoin `R7_T1`** : Curupira au rang 3 (Acte 1, Charge) ; un Bulldozer en parcelle 2, non annulé, frappe la parcelle 2 puis la parcelle 1 (derrière), et recule en parcelle 1.

- **Panel 2 — La Pirogue sans rameur** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : La pirogue remonte le courant. Sous sa coque, le reflet descend vers le gué.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez poser une Altération de la réserve sur une machine mobile de M ou E qui n’en porte pas. Si elle se trouve sur la parcelle du Duel, vous pouvez aussi avancer ce Rêve d’un rang vers la gauche si la case est libre. Les Défenseurs embarqués suivent.
  - **Dilemme** — *Choix* : Marquer la machine la plus dangereuse ou amarrer la pirogue au Duel ? · *Renoncement* : Une meilleure position sur la Réglette peut coûter le recul d’une autre machine.
  - **Témoin `R7_T1`** : Duel et Bulldozer mobile occupent M2. La Pirogue le marque et passe de 5 à 4. À sa prochaine révélation, le Bulldozer recule sans frapper mais compte pour la Furtivité.

- **Panel 3 — Le Songe du Brame des Brumes** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : « Quand le brame des esprits répond au défi du fauve, la clairière blessée se referme comme un rempart invisible devant les chenilles. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :
  > 1. Foulée Onirique : faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).
  > 2. Appel du Territoire Spectral : choisissez 1 seul des deux effets suivants :
  > • Ancrer la Harde : si le jeton Duel est déjà en forêt sur sa face Défi, retournez-le immédiatement sur sa face Territoire tenu ; s'il est dans la réserve Mammifère, posez-le sur sa face Défi sur n'importe quelle parcelle contenant au moins 1 Défenseur ou 1 Souche. Ensuite, sur le rayon portant désormais le Duel, posez 1 jeton d'Altération sur une machine mobile sans Altération (ou retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine de ce rayon).
  > • Hantise des Souches : si au moins 1 machine annulée par ce Rêve — ou au moins 1 machine mobile portant déjà un jeton d'Altération — appartient à un rayon comptant au moins 1 Souche (ou portant le Duel), faites glisser une seconde fois un Rêve en jeu (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.
  - **Dilemme** — *Choix* : Choisir Ancrer la Harde pour verrouiller Territoire tenu dès l'ouverture et poser une Altération, ou Hantise des Souches pour convertir les Souches en double bond vers le Sommeil. · *Renoncement* : Verrouiller le Duel renonce au double glissement de Rêve ; accélérer le Sommeil renonce au verrouillage préventif du Duel.
  - **Témoin `R7_T1`** : Tour 3, R7 défendu au rang 5 ; Duel (face Défi) en parcelle 2 de M face à l'Abatteuse (rang 3 En avançant, 0 Altération). À l'ouverture, R7 glisse au rang 4 libre puis choisit Ancrer la Harde : le Duel passe sur Territoire tenu (bloquant l'avancée du rang 3) et l'Abatteuse reçoit 1 Altération.

---

<a id="lisiere-r-h-g9-r4"></a>
### Lisière `R ↔ H` — Reptiles ↔ Humains (`G9` & `R4`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G9`** (`R>H`, GARDIEN) | **Le Caïman noir, l’ombre sous la pirogue** — Tient une machine au fond des eaux noires (⭐ Éveil · sortie `CALE`) | **Le Caïman noir** — Croc entre R et H → rive bénéficiaire · deux guetteurs groupés / répartis (⚡ Twist 2K3 · sortie `CROC`) | **Le Caïman noir, Maître des Eaux Noires** — Piocher au sac, tordre Furtivité (⚡ Twist 2K3 · ⭐ Éveil · sortie `ECAILLE`) |
| **`R4`** (`H>R`, REVE) | **La Pirogue-Anaconda des Ancêtres** — Piston de Rêves qui pousse le convoi (⚡ Twist 2K3 · 🌙 Levier Rêve · sortie `PISTON_REVES`) | **Le Tambour des deux berges** — Rayon annulé / pointe du Croc / foyer H · filet vers cible ou veilleur à terre (Brique fluide · sortie `PIEGE`) | **Le Songe de la Carapace de Limon** — Engloutir machine annulée au sac (🌙 Levier Rêve · sortie `RANG_REVE`) |

#### Emplacement `G9` (`R>H` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Caïman noir, l’ombre sous la pirogue** | **Le Caïman noir** | **Le Caïman noir, Maître des Eaux Noires** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⚡ Twist 2K3 (`ACTION`) | ⚡ Twist 2K3 · ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Sabotage** | ACTIVATION / **Sabotage** | ACTIVATION / **Sabotage** |
| **Pictogrammes** | 🧱 `PIC_CALE` · 💥 `PIC_SABOTAGE` · 🥁 `PIC_TAMBOUR` · ⏪ `PIC_RECUL` | 🦷 `PIC_CROC` · 🛡️ `PIC_DEFENSEUR` · 🪤 `PIC_PIEGE` · ⚡ `PIC_TWIST` | ⚡ `PIC_TWIST` · 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC` · 💥 `PIC_SABOTAGE` |
| **Résumé Mini-Tuile** | Tient une machine au fond des eaux noires | Croc entre R et H → rive bénéficiaire · deux guetteurs groupés / répartis | Piocher au sac, tordre Furtivité |
| **Mots-clés Face 1** | Sabotage révélé → cale · machine tenue sans Ratissage · rayon Reptile, Humain ou du Tambour | Confluent 1 + 1 | +1 🦎 au sac + 🦷 + Happe 1 jeton du sac (💥/🦎=résoudre · Machine=sac ou inclinée m(r)+1) |
| **Mots-clés Face 2** | Cale partout · machine calée révélée = annulée · Sabotage rallumé | Guetteurs séparés | +1 🦎 au sac + 🦷 + Happe 2 jetons du sac + Accord 🥁/🎶 (🔴→🔵 + 🌙 ←1) |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `SABOTAGE`, `ECAILLE` | `CROC`, `FURTIVITE`, `RANG_MACHINE` | `ECAILLE`, `CROC`, `SABOTAGE`, `TAMBOUR`, `CHANT` |
| **Synergies (`I01`)** | `TAMBOUR` | `CHANT` | `ROUGE`, `POSITION_REVE` |
| **Sorties (`I03`)** | `CALE`, `RECUL`, `ANNULATION` | `CROC`, `PIEGE` | `ECAILLE`, `CROC`, `MOBILISATION`, `BLEU`, `RANG_REVE` |

- **Panel 1 — Le Caïman noir, l’ombre sous la pirogue** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Le Caïman noir saisit et ne lâche plus : il tient sa proie contre le fond jusqu’à ce qu’elle cesse de lutter. Les pêcheurs le savent : dans les eaux noires, ce qu’il a pris ne remonte pas.
  - **Face 1** :
  > Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous une machine mobile du rayon Reptile, du rayon Humain ou du rayon où se trouve le Tambour (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile de ces rayons, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée est tenue : elle ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage (si elle termine le ménage sur la dernière parcelle, son jeton ne glisse pas sous elle). Quand son jeton Machine est révélé, la cale s’agite dans la séquence des Sabotages : allumez l’icône Sabotage, puis balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.
  - **Face 2** :
  > Quand le Caïman noir s’active, choisissez. La prise : prenez un jeton Sabotage ou Écaille révélé à cette ouverture et glissez-le en cale sous n’importe quelle machine mobile (une seule cale à la fois sur toute la table ; ce jeton ne rejoindra pas le sac au ménage). Ou, si la cale est déjà en jeu : déplacez-la sous une autre machine mobile, ou traînez la machine calée d’1 parcelle vers la bordure. La machine calée ne peut ni avancer, ni être poussée vers le cœur, ni entrer en Ratissage. La noyade : quand son jeton Machine est révélé, inclinez-le aussitôt (elle est annulée) ; puis, dans la séquence des Sabotages, la cale allume l’icône Sabotage et balayage. La cale regagne le sac dès que le Caïman noir quitte la Piste des Gardiens.
  - **Dilemme** — *Choix* : Quelle machine tenir : celle qui approche de la dernière parcelle (bloquer le Ratissage) ou celle qui menace la parcelle du Tambour. · *Renoncement* : Le jeton pris en cale ne dilue plus le sac : chaque pioche suivante a plus de chances de réveiller une machine.
  - **Double activation** : La première activation pose la cale (souvent sur le Sabotage qui vient d’allumer l’icône), la seconde traîne la machine calée d’1 parcelle vers la bordure ou déplace la cale vers une machine plus menaçante. Et chaque fois que la machine calée est révélée, la cale rallume Sabotage pour toute la Piste.
  - **Témoin `G9_T1`** : Un Sabotage est révélé ; le Caïman (sur Sabotage) s’active : cale sous l’Abatteuse du rayon H en parcelle 3 ; elle finit le ménage en parcelle 4 mais n’entre pas en Ratissage.

- **Panel 2 — Le Caïman noir** *(⚡ Twist 2K3 · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Chacun des deux guetteurs n’a vu qu’un sillage. Le caïman les a vus tous les deux.
  - **Face 1** :
  > Confluent. Prenez l’unique Croc en réserve, en forêt ou à l’affût. Soit vous le postez sur une parcelle de R ou H (ou d’un autre rayon si R et H sont entièrement Route), soit vous le couchez entre les deux pieds de rayon R et H, si leurs rives sont ouvertes. Sa pointe désigne le rayon qui pourra gagner. Cette position arme un seul affût pour la prochaine Furtivité. À cette fenêtre, calculez normalement les deux mobilisations. Si m(R) = 1 et m(H) = 1 et que la Rive Piège pointée porte deux Défenseurs, elle gagne un Piège. Le propriétaire du rayon pointé en choisit la parcelle légale. Les autres paris suivent leur règle ordinaire.
  > Dénouement de l’affût : après cette Furtivité, rendez le Croc en réserve, succès ou échec. Un affût armé après la Furtivité attend celle du tour suivant. Un nouvel emploi du Croc remplace l’ancien. Si G9 quitte la piste, rendez immédiatement un Croc encore à l’affût. La face visible de G9 à la Furtivité fait foi. Jetons inclinés et Ratissages comptent dans leur propre rayon comme d’habitude.
  - **Face 2** :
  > Guetteurs séparés. Même choix entre Croc en forêt et affût. Au confluent 1 + 1, vous pouvez aussi former l’équipage avec un Défenseur de chacune des deux Rives Piège. Attribuez un seul Piège au rayon pointé. Un Chamane compte comme le pion de la rive où il se tient.
  > Dénouement de l’affût : après cette Furtivité, rendez le Croc en réserve, succès ou échec. Un affût armé après la Furtivité attend celle du tour suivant. Un nouvel emploi du Croc remplace l’ancien. Si G9 quitte la piste, rendez immédiatement un Croc encore à l’affût. La face visible de G9 à la Furtivité fait foi. Jetons inclinés et Ratissages comptent dans leur propre rayon comme d’habitude.
  - **Dilemme** — *Choix* : Poster le Croc en forêt pour garantir un coup d’arrêt sur une parcelle, ou le risquer au confluent entre R et H pour transformer deux demi-mobilisations en Piège placé au choix du propriétaire du rayon. · *Renoncement* : Le Croc couché à l’affût ne pare aucune frappe tant que la Furtivité n’est pas passée, et rentre en réserve même si l’affût échoue.
  - **Double activation** : Un passage arme l’affût. Le second peut inverser sa pointe avant le verdict, le rompre pour une frappe urgente, ou reposter en forêt le Croc libéré après la Furtivité.
  - **Témoin `G9_T1`** : G9 Face 2 pointe vers H. Le jeton de l’Abatteuse H est incliné après annulation ; sur R, seul le Bulldozer en Ratissage est mobilisé. Chaque Rive Piège porte 1 pion (dont le Chant sur H). Les compteurs valent 1 et 1 : les deux guetteurs répartis font gagner 1 Piège à H (posé en H·3) et le Croc revient en réserve.

- **Panel 3 — Le Caïman noir, Maître des Eaux Noires** *(⚡ Twist 2K3 · ⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : « Sous le miroir d'encre du fleuve, seul l'éclair d'une écaille trahit la mâchoire qui happe l'intrus avant l'assaut. »
  - **Face 1** :
  > À l'activation de ce Gardien, ajoutez 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu) et posez ou déplacez le pion Croc sur une parcelle alliée.
  > Twist 2K3 — La Happe : piochez ensuite 1 jeton au hasard dans le Sac opaque :
  > • Sabotage ou Écaille : résolvez-le immédiatement comme un jeton révélé à l'ouverture (effet du Sabotage ou pose/repositionnement du Croc, allumage de l'icône Sabotage et nouveau balayage des Gardiens ; il suit ensuite le ménage normal).
  > • Machine (du rayon r) : au choix, remettez-la dans le Sac opaque, OU échouez-la inclinée à 90° sans dé au pied de son rayon r (neutralisée sans rang, elle n'agit pas aux attaques, mais compte comme visible et inclinée pour +1 dans m(r) à la Furtivité avant de rentrer au sac au ménage).
  > Accord R>H : si le Croc occupe le rayon du Tambour OU si le Chant occupe un rang ayant au moins 1 machine annulée ou aucune machine active, retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine (ou glissez 1 Rêve d'1 rang libre à gauche si aucun Rouge n'est présent).
  - **Face 2** :
  > À l'activation de ce Gardien, ajoutez 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu) et posez ou déplacez le pion Croc sur une parcelle alliée.
  > Double Happe : piochez jusqu'à 2 jetons dans le Sac opaque et appliquez à chacun d'eux (dans l'ordre de votre choix) les règles de La Happe (Sabotage ou Écaille résolu immédiatement avec allumage de Sabotage et balayage Gardiens ; Machine remise au sac ou posée inclinée à 90° sans dé au pied de son rayon pour +1 à m(r) sans action).
  > Accord R>H : avec le Croc sur le rayon du Tambour ou le Chant sur un rang sans machine active restante, retournez jusqu'à 1 jeton Rouge existant en Bleu Surchauffe ET glissez 1 Rêve d'1 rang libre à gauche.
  - **Dilemme** — *Choix* : Lorsqu'une Machine surgit de La Happe, l'échouer inclinée pour monter m(r) de 1 à 2 et remporter la Rive Piège gratuitement, ou la rejeter dans le Sac opaque ; placer le Croc sur le rayon du Tambour pour déclencher l'accord chamanique. · *Renoncement* : Échouer une Machine compromet une éventuelle Rive Sabotage (m(r) = 0) sur ce rayon ; aligner le Croc sur le Tambour peut le détourner d'une parcelle plus critique ailleurs.
  - **Double activation** : Sur l'icône Sabotage, engager 2 Défenseurs sur G9 catalyse directement l'Éveil de la Forêt même lorsqu'un seul joueur détient un Sabotage ou une Écaille sous son paravent : la 1re activation injecte d'abord une Écaille au sac puis déclenche La Happe ; tout Sabotage ou Écaille pêché dans le sac rallume aussitôt Sabotage, faisant glisser en chaîne le 2nd pari de G9 tout en posant deux fois le Croc et en sculptant m(r) avant la Furtivité.
  - **Témoin `G9_T1`** : Tour 5 (Acte 2), G9 Face 1 sur Sabotage (2 paris), 2 Défenseurs sur Rive Piège de R, Tambour en parcelle 2 de R. Un seul Sabotage est révélé et m(R)=1 : la 1re activation de G9 ajoute 1 Écaille, pose le Croc en parcelle 2 de R (accord R>H : Rouge → Bleu) et happe une Écaille qui rallume Sabotage ! La 2nde activation happe la 2nde Machine de R et l'échoue inclinée sans dé → m(R)=2 à la Furtivité (Rive Piège gagnée) et passage Face 2.

#### Emplacement `R4` (`H>R` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Pirogue-Anaconda des Ancêtres** | **Le Tambour des deux berges** | **Le Songe de la Carapace de Limon** |
| **Rôles & Nature** | ⚡ Twist 2K3 · 🌙 Levier Rêve (`ACTION`) | Brique fluide (`ACTION`) | 🌙 Levier Rêve (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | ⚡ `PIC_TWIST` · ⬅️ `PIC_AVANCEE_REVE` · 🌙 `PIC_REVE` · 🦎 `PIC_ECAILLE` | 🥁 `PIC_TAMBOUR` · 🪤 `PIC_PIEGE` · 🦷 `PIC_CROC` · 🛡️ `PIC_DEFENSEUR` | 🚫 `PIC_ANNULATION` · 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC` · 🎶 `PIC_CHANT` |
| **Résumé Mini-Tuile** | Piston de Rêves qui pousse le convoi | Rayon annulé / pointe du Croc / foyer H · filet vers cible ou veilleur à terre | Engloutir machine annulée au sac |
| **Mots-clés Face 1** | En queue · tout le convoi glisse d’1 ‖ Retour · échange avec le Rêve de droite ‖ mue = 1 Écaille au sac | Traversée · Débarquement | Machine inclinée → au Sac opaque (m(r) - 1) + 1 🦎 au sac · 🥁/🎶 : 🦷 + 🌙 ←1 |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `POSITION_REVE`, `RANG_REVE` | `POSITION_REVE`, `TAMBOUR` | `POSITION_REVE`, `ANNULATION`, `TAMBOUR`, `CHANT` |
| **Synergies (`I01`)** | — | `ANNULATION`, `PIEGE`, `CROC` | `ECAILLE`, `ROUGE` |
| **Sorties (`I03`)** | `PISTON_REVES`, `POSITION_REVE`, `ECAILLE` | `PIEGE`, `DEFENSEUR_REDEPLOYE` | `RANG_REVE`, `ECAILLE`, `CROC`, `BLEU` |

- **Panel 1 — La Pirogue-Anaconda des Ancêtres** *(⚡ Twist 2K3 · 🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : Au commencement, racontent les peuples du Rio Negro, les ancêtres remontèrent le fleuve dans le ventre d’un anaconda-pirogue, de halte en halte, jusqu’à devenir des hommes. La pirogue pousse encore les rêves vers l’amont.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution (après ses annulations), choisissez une manœuvre. Poussée : si la Pirogue est le Rêve le plus à droite de la Réglette, elle pousse tout le convoi : chaque Rêve, du plus à gauche au plus à droite (la Pirogue en dernier), glisse d’1 rang vers la gauche si ce rang est libre. Retour : la Pirogue échange sa place avec le premier Rêve situé à sa droite, même séparé d’elle par des rangs libres ; chacun garde ses Défenseurs, et ce Rêve, s’il n’a pas encore été résolu, se résout aussitôt depuis sa nouvelle place. Mue de l’anaconda : après chaque manœuvre, le joueur Reptile peut glisser 1 Écaille de sa réserve dans le sac.
  - **Dilemme** — *Choix* : Pousser le convoi entier (si la Pirogue est en queue) ou reculer en échangeant avec le Rêve de droite pour le faire remonter d’un coup. · *Renoncement* : Le Retour éloigne la Pirogue vers les rangs rares et la détache du bloc du Sommeil ; tant qu’elle n’est pas en queue, elle ne peut pas pousser.
  - **Témoin `R4_T1`** : Rêves aux rangs 3 et 4, Pirogue au rang 6 (rangs 1, 2 et 5 libres) : Poussée : Rêves aux rangs 2, 3 et Pirogue au rang 5 ; mue : 1 Écaille au sac.

- **Panel 2 — Le Tambour des deux berges** *(Brique fluide · OUVERTURE)*
  - *Ambiance* : Un coup résonne du côté où la machine s’est tue. Sur l’autre berge, quelqu’un ramasse le filet.
  - **Face 1** :
  > Appeler la berge. Après les annulations de ce Rêve défendu, choisissez le rayon d’une machine qu’il vient d’annuler, le rayon que pointe le Croc à l’affût du Caïman, ou votre propre rayon H. Si le rayon choisi est entièrement Route, prenez un autre rayon ouvert.
  > Transporter : prenez un Piège ordinaire sur le rayon choisi et portez-le sur une parcelle encore ciblée d’un autre rayon, libre de Piège ordinaire. Si le Tambour occupait la parcelle de départ, vous pouvez l’emporter avec le Piège.
  > Débarquer : vous pouvez aussi prendre un Défenseur de ce Rêve et le poser sur une parcelle du rayon choisi ou sur une place libre de l’une de ses deux rives de Furtivité. Cette option reste ouverte à zéro annulation et même si aucun Piège n’est en jeu. Les annulations déjà résolues sont acquises. Une rive ainsi rejointe sera évaluée à la Furtivité.
  - **Dilemme** — *Choix* : Exporter un Piège (et éventuellement le Tambour) vers une cible urgente ailleurs, ou débarquer un Défenseur du Rêve sur le terrain ou sur une rive de Furtivité. · *Renoncement* : Débarquer un veilleur complète un équipage avant la Furtivité mais dégarnit la Réglette ; exporter un filet découvre la parcelle de départ.
  - **Témoin `R4_T1`** : R4 défendu par le Chant se résout à rang vide (rayon R libre de Piège ordinaire). Le Croc de G9 Face 2 pointe vers R et un Défenseur attend sur la Rive Piège de H. R4 débarque le Chant sur celle de R : à la Furtivité avec m(R)=1 et m(H)=1, G9 réunit l’équipage partagé et R gagne 1 Piège. Seul, R4 débarque le Chant sur H·2.

- **Panel 3 — Le Songe de la Carapace de Limon** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : « Feuille morte parmi les feuilles noyées, sa carapace engloutit le vacarme du fer dans le silence du limon. »
  - **Face 1** :
  > À l'ouverture, lorsque ce Rêve est défendu (après le choix éventuel des machines annulées ici), choisissez 1 jeton Machine incliné à 90° (annulé par ce Rêve ou par un Rêve précédent) et plongez-le immédiatement dans le Sac opaque en retirant son dé de la Réglette : disparu sous l'eau avant la Furtivité, ce jeton ne compte plus dans m(r) pour la Furtivité (soit m(r) − 1, tout en restant comptabilisé comme machine annulée à ce tour pour le Chant et pour allumer l'icône Rêve). (Plancher : si aucune machine n'est inclinée, retournez 1 jeton Rouge existant en Bleu Surchauffe sur une machine mobile ou glissez 1 Rêve d'1 rang libre à gauche.)
  > Ajoutez ensuite 1 jeton Écaille de la réserve Reptile dans le Sac opaque (s'il en reste, max 4 en jeu).
  > Sillage H>R : si la machine engloutie provenait du rayon du Tambour ou du rang du Chant (ou si au moins 1 Écaille est déjà sortie du sac à ce tour), posez ou déplacez le pion Croc sur une parcelle alliée et glissez 1 Rêve d'1 rang libre à gauche.
  - **Dilemme** — *Choix* : Engloutir une machine annulée d'un rayon à m(r)=1 pour le ramener à m(r)=0 et remporter la Rive Sabotage (+1 Sabotage au sac), tout en injectant 1 Écaille et en posant le Croc. · *Renoncement* : Engloutir cette machine renonce à m(r)=2 sur une Rive Piège et remet dès maintenant ce jeton Machine en circulation dans le Sac opaque avant une éventuelle Happe de G9.
  - **Témoin `R4_T1`** : Tour 4, 2 Défenseurs sur Rive Sabotage de H (vise m(H)=0), Tambour en parcelle 1 de H, Chant et 1 Défenseur sur R4 au rang 2 où tombe l'unique Machine de H. R4 annule cette machine, l'engloutit aussitôt dans le Sac opaque (m(H) retombe à 0), ajoute 1 Écaille au sac, pose le Croc et glisse un autre Rêve à gauche (Sillage H>R), puis le Chant avance R4 au rang 1. À la Furtivité, m(H)=0 gagne la Rive Sabotage.

---

<a id="lisiere-r-e-g10-r8"></a>
### Lisière `R ↔ E` — Reptiles ↔ Entités Magiques (`G10` & `R8`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G10`** (`R>E`, GARDIEN) | **La Matamata, la souche qui respire** — Avale un jeton Machine et le garde hors du sac (Brique fluide · sortie `JETON_AVALE`) | **La Matamata** — Litière · aspiration / Leurre dédoublé (⭐ Éveil · sortie `CROC`) | **La Matamata, Guetteuse des Feuilles Mortes** — Injecte Écaille, embusque Croc, altère (⭐ Éveil · sortie `ECAILLE`) |
| **`R8`** (`E>R`, REVE) | **Le Boitatá, serpent de feu** — Le feu des machines se retourne contre elles (⚖️ Loi passive · 🌙 Levier Rêve · sortie `ROUGE_RETOURNE`) | **La Peau du fleuve** — Mue · rang révélé (🌙 Levier Rêve · ⚖️ Loi passive · ⚡ Twist 2K3 · sortie `RANG_REVE`) | **Le Rêve de la Mue d’Obsidienne** — Écailles glissent rêves · Croc refroidit (⚖️ Loi passive · 🌙 Levier Rêve · sortie `RANG_REVE`) |

#### Emplacement `G10` (`R>E` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Matamata, la souche qui respire** | **La Matamata** | **La Matamata, Guetteuse des Feuilles Mortes** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Rêve** | ACTIVATION / **Rêve** | ACTIVATION / **Piégeage** |
| **Pictogrammes** | 🌙 `PIC_REVE` · 🚫 `PIC_ANNULATION` · 🪵 `PIC_SOUCHE` · ⭐ `PIC_PARI_ENCOCHE` | 🪵 `PIC_SOUCHE` · 🦷 `PIC_CROC` · 🪤 `PIC_PIEGE` | 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC` · 🌀 `PIC_ALTERATION` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Avale un jeton Machine et le garde hors du sac | Litière · aspiration / Leurre dédoublé | Injecte Écaille, embusque Croc, altère |
| **Mots-clés Face 1** | Machine annulée par un Rêve → jeton avalé hors du sac · sans annulation : machine qui a déjà attaqué · encoche vide au ménage = proie rendue | Litière · aspiration | +1 🦎 sac + [🦷 ciblé & 🔴→🔵 OU 🌀] |
| **Mots-clés Face 2** | Ou machine révélée sur clairière de Souches → annulée et avalée | Leurre dédoublé | +1 🦎/🔴→🔵 + 🦷 ciblé ET 🌀 |
| **Mots-clés Enraciné** | — | — | Standard (1 ou 2 Souches finales) |
| **Plancher (`M4`)** | `RANG_MACHINE` | `SOUCHE`, `RANG_MACHINE`, `RATISSAGE` | `ECAILLE`, `CROC`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `ANNULATION`, `SOUCHE` | `PIEGE` | `ALTERATION`, `ROUGE` |
| **Sorties (`I03`)** | `JETON_AVALE`, `ANNULATION` | `CROC`, `PIEGE` | `ECAILLE`, `CROC`, `ALTERATION`, `BLEU` |

- **Panel 1 — La Matamata, la souche qui respire** *(Brique fluide · ACTIVATION / **Rêve**)*
  - *Ambiance* : On la prend pour une souche, pour un tas de feuilles mortes. Puis la gueule s’ouvre en un éclair et l’eau s’engouffre : la proie a disparu avant même d’avoir compris.
  - **Face 1** :
  > La gueule. Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture (son jeton est encore incliné devant son rayon). La Matamata l’avale : posez son jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée (elle n’attaque pas) et ne peut pas entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.
  > Proie de passage (plancher) : si aucun Rêve n’a annulé de machine à cette ouverture, la Matamata avale à la place, de la même façon, le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).
  > Digestion : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.
  - **Face 2** :
  > L’affût de la clairière. Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture, ou une machine révélée qui n’a pas encore attaqué et qui se trouve sur une parcelle réduite à des Souches (aucun Arbre debout). La Matamata l’avale : la seconde est annulée (inclinez son jeton) ; posez ce jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée ni entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.
  > Proie de passage (plancher) : si aucune de ces deux proies n’existe, la Matamata avale à la place le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).
  > Digestion : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.
  - **Dilemme** — *Choix* : Garder la même proie tour après tour (en pariant sur la Matamata) ou l’échanger contre une machine plus menaçante. · *Renoncement* : Pour ne pas digérer, la Matamata exige une encoche occupée à chaque ménage — un Défenseur engagé en pari sur elle plutôt qu’en forêt.
  - **Double activation** : La première activation avale la proie de l’ouverture ; la seconde peut l’échanger contre une machine plus dangereuse annulée plus à droite, ou (Face 2) avaler une machine posée sur une clairière avant qu’elle ne frappe. Seule en piste, la seconde troque la proie de passage contre la machine la plus proche de la dernière parcelle, pour lui interdire le Ratissage. Chaque activation glisse un pari : or c’est une encoche occupée au ménage qui empêche la Matamata de digérer.
  - **Témoin `G10_T1`** : Un Rêve au rang 2 annule le Bulldozer du rayon E ; la Matamata (sur Rêve) s’active : jeton avalé ; au tour suivant, le sac contient 2N − 1 jetons Machine.

- **Panel 2 — La Matamata** *(⭐ Éveil · ACTIVATION / **Rêve**)*
  - *Ambiance* : Feuille entre les feuilles, la matamata attend que l’eau lui amène sa prise.
  - **Face 1** :
  > À chaque activation, choisissez une parcelle encore ciblée portant une Souche. Vous pouvez y poser le Croc de la réserve ou y attirer un Piège ordinaire d’une autre parcelle du même rayon, si la destination est libre de Piège ordinaire.
  - **Face 2** :
  > À chaque activation, choisissez une parcelle encore ciblée. Vous pouvez y attirer un Piège ordinaire d’une autre parcelle de son rayon si elle peut le recevoir. Vous pouvez plutôt y poser le Croc de la réserve et, si vous y recouvrez un Piège ordinaire, envoyer ce Piège sur une autre parcelle encore ciblée de ce rayon, libre de Piège ordinaire.
  - **Dilemme** — *Choix* : Garder deux intercepteurs ensemble ou faire glisser le leurre ? · *Renoncement* : Une parcelle dégarnie de son Piège n’arrêtera plus une deuxième frappe après le Croc.
  - **Double activation** : Une aspiration attire le Piège, la suivante peut le remplacer par le Croc et couvrir une autre cible. Deux rayons peuvent aussi fournir deux Pièges.
  - **Témoin `G10_T1`** : Deux machines d’un rayon visent des parcelles différentes. La Matamata F2 couvre la première avec le Croc et en extrait le Piège pour la seconde. Deux frappes, deux événements Piégeage.

- **Panel 3 — La Matamata, Guetteuse des Feuilles Mortes** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : « On croit marcher sur un lit de feuilles mortes ; déjà le vide s'est ouvert sous l'acier et la vase glacée l'aspire. »
  - **Face 1** :
  > Lorsque La Matamata s'active :
  > 1. Mue de Vase : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque.
  > 2. Gueule Aspirante : choisissez 1 seule des deux manœuvres suivantes :
  > • Happer la Proie : si le jeton Croc est dans la réserve Reptile, posez-le sur n'importe quelle parcelle ciblée (par une machine qui n'a pas encore frappé à ce tour, mobile ou en Ratissage) ; en outre, si une machine ciblant cette parcelle porte déjà un jeton d'Altération ou possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
  > • Vase Hallucinogène : posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération ; si le jeton Croc se trouve déjà sur le plateau sur une parcelle non ciblée, vous pouvez le déplacer sur une parcelle ciblée de ce rayon.
  - **Face 2** :
  > Lorsque La Matamata s'active :
  > 1. S'il reste au moins 1 jeton Écaille chez les Reptiles, glissez-le dans le sac opaque ; si les 4 Écailles sont déjà sorties, retournez 1 jeton Rouge existant d'une machine du plateau sur sa face Bleue Surchauffe.
  > 2. Résolvez les deux effets de Gueule Aspirante dans l'ordre de votre choix : déployez (ou repositionnez depuis une parcelle non ciblée) le Croc sur une parcelle ciblée avec son retournement Rouge → Bleu, ET posez 1 jeton d'Altération sur une machine mobile sans Altération (si toutes les machines mobiles sont déjà altérées, retournez 1 jeton Rouge existant → Bleu Surchauffe sur une machine altérée).
  - **Dilemme** — *Choix* : En Face 1, choisir Happer la Proie pour recycler aussitôt le Croc et allumer Piégeage (en synergie avec R8), ou Vase Hallucinogène pour neutraliser le tour suivant par Altération. · *Renoncement* : En Face 1, les deux manœuvres s'excluent mutuellement : sécuriser le tour courant via le Croc renonce à l'Altération préventive du tour suivant.
  - **Double activation** : Posée sur Piégeage, La Matamata excelle en double mise : dès qu'un premier Piège ou le Croc pare une attaque (le Croc regagnant aussitôt la réserve Reptile avant le balayage), sa 1re activation redéploie immédiatement le Croc sur une seconde parcelle ciblée plus tard dans l'ordre des rangs ; lorsque ce Croc pare à son tour, il rallume Piégeage et déclenche tout seul la 2nde activation de La Matamata.
  - **Témoin `G10_T1`** : Tour 3, La Matamata Face 1 sur Piégeage (2 paris). Au rang 2, le Croc pare une Abatteuse (rentre en réserve, allume Piégeage) : 1re activation → +1 Écaille au sac + Happer la Proie repose le Croc devant le Bulldozer du rang 5 (Rouge → Bleu). Au rang 5, le Croc pare et rallume Piégeage : 2nde activation (Face 2) → +1 Écaille + Vase Hallucinogène altère le Bulldozer.

#### Emplacement `R8` (`E>R` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Boitatá, serpent de feu** | **La Peau du fleuve** | **Le Rêve de la Mue d’Obsidienne** |
| **Rôles & Nature** | ⚖️ Loi passive · 🌙 Levier Rêve (`LOI_PASSIVE`) | 🌙 Levier Rêve · ⚖️ Loi passive · ⚡ Twist 2K3 (`LOI_PASSIVE`) | ⚖️ Loi passive · 🌙 Levier Rêve (`LOI_PASSIVE`) |
| **Fenêtre / Icône** | PERMANENT | RETRAIT ALTÉRATION / OUVERTURE | PERMANENT |
| **Pictogrammes** | ⚖️ `PIC_LOI_PASSIVE` · 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` · ⬅️ `PIC_AVANCEE_REVE` | 🌀 `PIC_ALTERATION` · ⬅️ `PIC_AVANCEE_REVE` · 🦷 `PIC_CROC` · ⚖️ `PIC_LOI_PASSIVE` | ⚖️ `PIC_LOI_PASSIVE` · 🦎 `PIC_ECAILLE` · 🌀 `PIC_ALTERATION` · 🦷 `PIC_CROC` |
| **Résumé Mini-Tuile** | Le feu des machines se retourne contre elles | Mue · rang révélé | Écailles glissent rêves · Croc refroidit |
| **Mots-clés Face 1** | Loi · à son rang chaque Rouge compte comme un Bleu · annule = glisse d’1 rang | Mue · rang révélé | Passif : 🦎/Défendu → Glisse 1G & 🌀 · 🦷 pare → 🔴→🔵 (sinon ⏪ 1) |
| **Mots-clés Enraciné** | — | — | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `ROUGE`, `RANG_REVE`, `RANG_MACHINE` | `ALTERATION`, `RANG_MACHINE`, `POSITION_REVE` | `POSITION_REVE`, `ALTERATION`, `RANG_MACHINE` |
| **Synergies (`I01`)** | — | `CROC` | `ECAILLE`, `CROC`, `ROUGE` |
| **Sorties (`I03`)** | `ROUGE_RETOURNE`, `POSITION_REVE`, `ANNULATION` | `RANG_REVE`, `ALTERATION` | `RANG_REVE`, `ALTERATION`, `BLEU`, `RECUL` |

- **Panel 1 — Le Boitatá, serpent de feu** *(⚖️ Loi passive · 🌙 Levier Rêve · PERMANENT)*
  - *Ambiance* : Pendant le grand déluge, le Boitatá survécut dans un trou et se nourrit de la lumière des yeux des bêtes mortes ; depuis, son corps brûle. Il poursuit ceux qui incendient la forêt, et leur propre feu se retourne contre eux.
  - **Face 1** :
  > Loi passive — Le feu retourné (tant que le Boitatá est sur la Réglette, défendu ou non) : pour toute machine qui attaque depuis le rang du Boitatá, chaque Rouge compte comme un Bleu dans le Seuil de Parade (−1 au lieu de +1), dans tous les modes. Pouvoir du Boitatá (quand il est défendu) — le serpent ondule : quand ce Rêve annule au moins 1 machine, il glisse ensuite d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent).
  - **Dilemme** — *Choix* : Annuler les machines de son rang pour faire onduler le Boitatá vers la gauche, ou laisser attaquer une machine bourrée de Rouges devenue presque inoffensive. · *Renoncement* : Une machine laissée active frappe toujours ; et chaque rang gagné vers la gauche emporte la loi du feu vers un autre rang.
  - **Témoin `R8_T1`** : Machine en Mode Assaut au rang du Boitatá, 3 Rouges, parcelle gravée 3 : Seuil = 3 − 3 = 1 (minimum) au lieu de 6.

- **Panel 2 — La Peau du fleuve** *(🌙 Levier Rêve · ⚖️ Loi passive · ⚡ Twist 2K3 · RETRAIT ALTÉRATION / OUVERTURE)*
  - *Ambiance* : Le fleuve abandonne son ancienne courbe. Le lit vide garde un instant la forme de ce qui va arriver.
  - **Face 1** :
  > Sur la Réglette, même sans Défenseur, ce Rêve peut prendre le rang révélé d’une mobile dont on retire l’Altération, s’il est libre et à sa gauche. Déplacez-le avec ses Défenseurs avant les Sabotages. La machine recule et reste privée de frappe comme prévu. Pour plusieurs retraits simultanés, les Entités choisissent leur ordre. Au pouvoir de ce Rêve défendu, vous pouvez altérer une mobile sans Altération de E ou R, ou de tout rayon portant le Croc. Posez le jeton de la réserve.
  - **Dilemme** — *Choix* : Sauter vers le Sommeil ou conserver le rang d’une annulation certaine ? · *Renoncement* : À son arrivée, la machine qui a payé le passage est déjà neutralisée. Il faut une autre machine pour y réussir une annulation.
  - **Témoin `R8_T1`** : Une mobile altérée révèle 2. La Peau, défendue en 5, rejoint le 2 libre. La première machine recule. Une seconde machine de rang 2 peut alors être annulée par le Rêve.

- **Panel 3 — Le Rêve de la Mue d’Obsidienne** *(⚖️ Loi passive · 🌙 Levier Rêve · PERMANENT)*
  - *Ambiance* : « Le reptile abandonne son ancienne peau aux esprits de la nuit ; quiconque y mord sent le gel remonter jusqu'au cœur du moteur. »
  - **Face 1** :
  > Tant que ce Rêve occupe un rang de la Réglette (même sans Défenseur posé sur lui) :
  > • Piston d'Écaille (À l'ouverture) : chaque fois qu'un jeton Écaille est révélé à l'ouverture des paravents — ainsi que lorsque ce Rêve lui-même est défendu à sa résolution d'ouverture — faites glisser 1 Rêve en jeu de votre choix (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
  > • Venin d'Obsidienne (Aux attaques) : chaque fois que le jeton Croc Reptile pare la frappe d'une machine (juste avant que le Croc ne regagne la réserve Reptile) : si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge) et qu'elle est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).
  - **Dilemme** — *Choix* : Laisser R8 sans Défenseur pour profiter passivement des Écailles et du Croc tout en économisant des poses, ou le défendre activement pour garantir un glissement et une Altération même sans Écaille tirée. · *Renoncement* : Défendre R8 immobilise un Défenseur sur la Réglette ; le laisser vide renonce à l'annulation sur son rang et au déclenchement garanti lors des tours sans Écaille.
  - **Témoin `R8_T1`** : Tour 5, R8 non défendu au rang 4, un autre Rêve au rang 3. Une Écaille révélée pose le Croc en parcelle 3 de R et déclenche Piston d'Écaille (Rêve 3 → 2 + Altération sur une Abatteuse). Aux attaques, un Bulldozer sans Rouge est paré par le Croc : Venin d'Obsidienne le recule en parcelle 2 avant le retour du Croc en réserve.

---

<a id="lisiere-o-h-g11-r5"></a>
### Lisière `O ↔ H` — Oiseaux ↔ Humains (`G11` & `R5`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G11`** (`O>H`, GARDIEN) | **La Harpie féroce, reine des hautes cimes** — Arrache une machine depuis le Perchoir (⭐ Éveil · sortie `PROIE_ARRACHEE`) | **La Harpie féroce** — Oiseau au sol / Oiseau sur jeton Machine · miroir → Chamane au Rêve (⭐ Éveil · sortie `DEFENSEUR_REDEPLOYE`) | **La Harpie féroce, Souveraine des Grands Fromagers** — Cloue au sol la cible isolée (⭐ Éveil · sortie `PIEGE`) |
| **`R5`** (`H>O`, REVE) | **Le Vol du Chamane-Oiseau** — Un Rêve qui veille sur deux rangs (Brique fluide · sortie `ANNULATION_ENVOL`) | **Le Ciel à deux eaux** — Rangs miroirs · échange (Brique fluide · sortie `RANG_MACHINE`) | **La Vision du Condor des Brumes** — ⚡ Dé écarté 🎲 → Rang V / ⬅️ (⚡ Twist 2K3 · 🌙 Levier Rêve · sortie `RANG_MACHINE`) |

#### Emplacement `G11` (`O>H` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Harpie féroce, reine des hautes cimes** | **La Harpie féroce** | **La Harpie féroce, Souveraine des Grands Fromagers** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Sabotage** | ACTIVATION / **Parade** | ACTIVATION / **Piégeage** |
| **Pictogrammes** | 🦅 `PIC_PERCHOIR` · 💥 `PIC_SABOTAGE` · 🚫 `PIC_ANNULATION` · 🌙 `PIC_REVE` | 🪶 `PIC_PLUME` · 🔢 `PIC_RANG_MACHINE` · 🛡️ `PIC_DEFENSEUR` · 🎶 `PIC_CHANT` | 🪤 `PIC_PIEGE` · 🔢 `PIC_RANG_MACHINE` · ⏪ `PIC_RECUL` · 🥁 `PIC_TAMBOUR` |
| **Résumé Mini-Tuile** | Arrache une machine depuis le Perchoir | Oiseau au sol / Oiseau sur jeton Machine · miroir → Chamane au Rêve | Cloue au sol la cible isolée |
| **Mots-clés Face 1** | Sabotage du Perchoir ↔ machine révélée · Sabotage rallumé · proie perchée recule | Fondre ou saisir | Rayon 🪶 / 🥁 / machine seule sur son rang : +1 🪤 · Si seule sur son rang (ou rang 🎶) : ⏪ -1 |
| **Mots-clés Face 2** | Tout jeton du Perchoir ↔ machine · machine perchée lâchée au rang d’un Rêve Humain | Piqué miroir | Tout rayon : +1 🪤 · Puis sur 1 machine du rayon : ⏪ -1 (si mobile) ET 🔴→🔵 (si ≥ 1 🔴) |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `PERCHOIR`, `SABOTAGE` | `DE_ENVOL`, `PLUME`, `DEFENSEUR_ATTENTE`, `RANG_MACHINE` | `PLUME`, `TAMBOUR`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `POSITION_REVE` | `CHANT`, `POSITION_REVE` | `CHANT`, `ROUGE` |
| **Sorties (`I03`)** | `PROIE_ARRACHEE`, `SABOTAGE`, `RECUL` | `DEFENSEUR_REDEPLOYE`, `ANNULATION` | `PIEGE`, `RECUL`, `BLEU` |

- **Panel 1 — La Harpie féroce, reine des hautes cimes** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : La Harpie peut guetter une journée entière sans bouger une plume. Puis elle plonge à travers les branches et emporte sa proie dans les hauteurs, là où personne ne la reprendra.
  - **Face 1** :
  > Quand la Harpie féroce s’active : si le jeton posé sur le Perchoir de Vigie est un Sabotage ou une Écaille, la Harpie fond sur sa proie : échangez-le avec le jeton d’une machine révélée qui n’est ni annulée ni encore résolue. Cette machine perd son activation : son jeton rejoint le Perchoir, face cachée. Le Sabotage ou l’Écaille, révélé à sa place, allume l’icône Sabotage, puis balayage (une Écaille pose aussi le Croc, comme d’habitude). Si le Perchoir porte déjà un jeton Machine, la Harpie emporte cette proie : faites reculer la machine correspondante d’1 parcelle vers la bordure.
  - **Face 2** :
  > Quand la Harpie féroce s’active : échangez le jeton posé sur le Perchoir de Vigie avec le jeton d’une machine révélée qui n’est ni annulée ni encore résolue ; cette machine perd son activation et son jeton rejoint le Perchoir, face cachée. Si le jeton venu du Perchoir est un Sabotage ou une Écaille, il est révélé à sa place : il allume l’icône Sabotage, puis balayage (une Écaille pose aussi le Croc). Si c’est un jeton Machine, la Harpie lâche cette proie dans le rêve des hommes : sa machine est révélée sur le rang d’un Rêve Humain défendu qui n’a pas encore été résolu, où ce Rêve pourra l’annuler ; sans un tel Rêve, cet échange est impossible.
  - **Dilemme** — *Choix* : Au tirage, l’Oiseau choisit quel jeton percher : garder la Machine et percher le Sabotage pour la Harpie, ou l’inverse. · *Renoncement* : Percher le Sabotage oblige l’Oiseau à jouer lui-même la Machine et ses dés ; une Harpie qui ne s’active pas laisse ce Sabotage inutile au Perchoir.
  - **Double activation** : Le Perchoir change de nature après un piqué : il porte la machine arrachée. La seconde activation emporte cette proie d’1 parcelle (Face 1) ou la lâche sur le rang d’un Rêve Humain qui l’annule (Face 2) : deux machines neutralisées pour un seul Sabotage perché. Chaque Sabotage révélé rallume la Piste.
  - **Témoin `G11_T1`** : Perchoir = Sabotage ; un Bulldozer est révélé au rang 2 ; la Harpie (sur Sabotage) s’active au premier Sabotage : échange ; le Bulldozer est inactif, le Sabotage révélé rallume Sabotage, la mobilisation de son rayon baisse de 1.

- **Panel 2 — La Harpie féroce** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : Au cri du guetteur, on regarde le ciel. L’ombre est déjà passée.
  - **Face 1** :
  > Fondre ou saisir (après ouverture des paravents). Prenez un Défenseur Oiseau disponible en forêt, sur une rive, un Rêve, une lisière ou en attente. Pour fondre, posez-le sur la parcelle d’une machine ou un pas radial devant elle, même si elle ne doit pas frapper ce tour. Pour saisir, choisissez une mobile à jouer au rang qu’indique votre Dé d’Envol. Laissez-le visible à l’ouverture, même sur un Sabotage. S’il sert de dé de machine, lisez sa face actuelle. Posez le Défenseur sur son jeton Machine révélé. La machine cesse aussitôt d’être active et perd toute son activation. Son jeton reste droit et visible pour la Furtivité, son dé lisible à son rang. Le pion engagé dans la saisie revient en main au ménage.
  - **Face 2** :
  > Piqué miroir. Vous pouvez fondre ou saisir comme en Face 1. Si la Plume indique le rang du Dé d’Envol ou son miroir (1↔4, 2↔5, 3↔6), les deux rangs s’ouvrent à la saisie. Après une saisie sur l’un des deux, vous pouvez porter un Chamane en forêt, depuis une parcelle que cette machine menaçait, sur un Rêve au rang miroir de la prise. Il y défendra le Rêve si sa lecture est encore à venir. Le rang lu est celui du dé au moment du piqué, après tout échange de R5.
  - **Dilemme** — *Choix* : Fondre au sol pour participer à plusieurs Parades, ou saisir un jeton Machine pour retirer toute son activation du tour ; en Face 2, monter le Chant sur le Rêve miroir. · *Renoncement* : L’Oiseau posé sur un jeton Machine ne défendra aucune autre frappe du tour ; monter le Chant peut vider la parcelle menacée par une seconde machine.
  - **Double activation** : Un premier piqué met un Oiseau au sol pour une Parade. Au second, ce même pion peut saisir une autre menace. Deux saisies demandent deux Oiseaux disponibles.
  - **Témoin `G11_T1`** : Dé d’Envol 3 visible, Plume sur 6. R5 échange les rangs 3 et 6 (le Bulldozer H·1 passe au rang 6 ; le Chant est en H·2). L’icône Rêve active G11 Face 2 : un Oiseau saisit le Bulldozer au rang 6 et porte le Chant sur un Rêve encore à lire au rang 3, qui annule l’autre mobile et glisse au rang 2 libre.

- **Panel 3 — La Harpie féroce, Souveraine des Grands Fromagers** *(⭐ Éveil · ACTIVATION / **Piégeage**)*
  - *Ambiance* : « Tant que les engins roulent en meute, l’ombre plane en silence ; dès que l’un d’eux s’isole à l’écart du convoi, les serres s’abattent du haut du fromager. »
  - **Face 1** :
  > Lorsque La Harpie féroce s’active, ciblez un rayon désigné par la Plume de Vigie, portant le Tambour, ou contenant une machine qui est la seule machine non annulée présente sur son rang 1–6 (à défaut, ciblez le rayon Oiseaux) :
  > • Posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire de ce rayon.
  > • Serre Zénithale : si une machine mobile de ce rayon est la seule machine non annulée sur son rang 1–6 (ou si son dé occupe le rang d’un Rêve portant le Chant), faites-la reculer d’1 parcelle vers la bordure (en sautant toute Route Forestière).
  - **Face 2** :
  > Lorsque La Harpie féroce s’active, ciblez n’importe quel rayon du plateau :
  > • Posez 1 Piège ordinaire de la réserve sur une parcelle dépourvue de Piège ordinaire de ce rayon (ou de tout autre rayon si toutes ses parcelles sont déjà piégées).
  > • Choisissez 1 machine de ce rayon : si elle est mobile, faites-la reculer d’1 parcelle vers la bordure ; et si elle porte au moins 1 jeton Rouge (y compris une machine en Ratissage), retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
  - **Dilemme** — *Choix* : Coordonner le Dé d'Envol ou R5 pour expédier une machine dangereuse seule sur un rang élevé afin que La Harpie la recule ET pose un Piège devant sa nouvelle cible, ou piquer directement sur le rayon du Tambour. · *Renoncement* : Isoler une machine sur un rang tardif (5 ou 6) pour déclencher la Serre Zénithale peut la faire passer en Assaut (Acte 1) ou en En avançant (rang 6) si le Piège est consommé avant son tour.
  - **Double activation** : Placée sur Piégeage, La Harpie s'auto-alimente tout en restant sur son icône : un premier Piège déclenché aux rangs bas (ou le Croc) active La Harpie, qui recule et piège une machine d'un rang supérieur ; lorsque cette seconde machine percute ce nouveau Piège plus tard aux attaques, Piégeage se rallume et déclenche la seconde activation de La Harpie.
  - **Témoin `G11_T1`** : À l'ouverture, R5 utilise un dé écarté 5 pour projeter le Bulldozer de H seul sur le rang 5 (Devant, parcelle 3) et allume Rêve. La Harpie Face 1 (sur Rêve) recule ce Bulldozer en parcelle 2 et pose 1 Piège ordinaire en parcelle 3 : au rang 5, le Bulldozer frappe Devant en parcelle 3, percute le Piège et allume Piégeage.

#### Emplacement `R5` (`H>O` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Vol du Chamane-Oiseau** | **Le Ciel à deux eaux** | **La Vision du Condor des Brumes** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | Brique fluide (`ACTION`) | ⚡ Twist 2K3 · 🌙 Levier Rêve (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | 🌙 `PIC_REVE` · 🦅 `PIC_PERCHOIR` · 🚫 `PIC_ANNULATION` · 🎲 `PIC_DES_PARAVENT` | 🪶 `PIC_PLUME` · 🔢 `PIC_RANG_MACHINE` · 🦅 `PIC_PERCHOIR` | ⚡ `PIC_TWIST` · 🎲 `PIC_DES_PARAVENT` · 🔢 `PIC_RANG_MACHINE` · ⬅️ `PIC_AVANCEE_REVE` |
| **Résumé Mini-Tuile** | Un Rêve qui veille sur deux rangs | Rangs miroirs · échange | ⚡ Dé écarté 🎲 → Rang V / ⬅️ |
| **Mots-clés Face 1** | Annule aussi au rang du Dé d’Envol · 1 machine par Défenseur au total | Rangs miroirs · échange | ⚡ Lit 1 🎲 écarté (V) : machine → rang V OU ce 🌙 → V / ⬅️ (les 2 si 🎶 ou 🪶 rang) |
| **Plancher (`M4`)** | `DE_ENVOL`, `RANG_REVE` | `PLUME`, `RANG_MACHINE` | `DES_SOUS_PARAVENT`, `DE_ENVOL`, `POSITION_REVE` |
| **Synergies (`I01`)** | `ANNULATION` | `PERCHOIR` | `CHANT`, `PLUME` |
| **Sorties (`I03`)** | `ANNULATION_ENVOL` | `RANG_MACHINE` | `RANG_MACHINE`, `RANG_REVE` |

- **Panel 1 — Le Vol du Chamane-Oiseau** *(Brique fluide · OUVERTURE)*
  - *Ambiance* : Quand le chamane chante jusqu’à l’aube, son âme quitte son corps et prend des plumes. De là-haut, elle voit deux chemins à la fois : celui où dort le rêve, et celui où l’oiseau a lancé son dé.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution : l’âme du chamane s’envole avec le Dé d’Envol. Ce Rêve peut annuler, en plus des machines de son propre rang, les machines révélées sur le rang indiqué par le Dé d’Envol de l’Oiseau, toujours à raison d’1 machine par Défenseur au total. Une machine annulée ainsi ne peut plus l’être par le Rêve qui occupe éventuellement ce rang.
  - **Dilemme** — *Choix* : Défendre ce Rêve avec plusieurs Défenseurs pour couvrir deux rangs, ou n’en garder qu’un pour la forêt. · *Renoncement* : Le Dé d’Envol n’est connu qu’à l’ouverture : un Défenseur posé ici peut n’avoir rien à annuler si aucun des deux rangs ne reçoit de machine.
  - **Témoin `R5_T1`** : Rêve H au rang 6 défendu par 2 Défenseurs ; Dé d’Envol = 1 ; deux machines révélées au rang 1 : toutes deux annulées.

- **Panel 2 — Le Ciel à deux eaux** *(Brique fluide · OUVERTURE)*
  - *Ambiance* : Les deux rives montrent le même ciel. Une seule voit l’orage arriver.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez échanger les rangs de deux machines visibles encore actives, distants exactement de trois. La Plume doit indiquer l’un de ces rangs. Si le Perchoir porte un jeton face cachée, une Plume au pied du rayon d’une des deux machines convient aussi. Laissez le jeton caché sur son Perchoir. Placez leurs dés de machine aux rangs échangés, sans déplacer leurs jetons de rayon. Chacune garde sa tactique imprimée mais change de mode. Les Rêves encore à résoudre lisent les nouveaux rangs.
  - **Dilemme** — *Choix* : Quelle machine doit passer en Charge et laquelle attaquera plus tôt ? · *Renoncement* : Le changement de mode vaut pour les deux. Il peut renforcer la machine qu’on laisse en Assaut.
  - **Témoin `R5_T1`** : Acte I, Plume en 1, une Abatteuse en 1 échange avec un Bulldozer chargé de Rouges en 4. Le Bulldozer passe en Charge sur place. L’Abatteuse passe en Assaut en 4 devant un Rêve encore à résoudre.

- **Panel 3 — La Vision du Condor des Brumes** *(⚡ Twist 2K3 · 🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : « Rien de ce qui roule dans l'ombre des mains humaines n'échappe à l'œil qui plane au-dessus des nuages : même le destin écarté trace encore une route. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu, choisissez 1 dé non retenu visible devant le paravent ouvert de l'Oiseau, des Humains, ou de tout joueur ayant révélé un Sabotage ou une Écaille (c'est-à-dire le Dé d'Envol non choisi, le dé standard supérieur non retenu d'un porteur de Machine, ou l'un des dés lancés à blanc sur un Sabotage/Écaille). Soit V sa valeur (de 1 à 6). Appliquez 1 présage au choix — ou les deux si ce Rêve porte le Chant ou si la Plume de Vigie est posée près d'un rang 1–6 :
  > • Courant Ascendant : déplacez le dé actif d'1 machine mobile non annulée de votre choix directement sur le rang V de la Réglette (si un Rêve défendu situé strictement à droite de ce Rêve ne s'est pas encore résolu et occupe le rang V, il pourra annuler cette machine lors de son tour de résolution !).
  > • Aile du Songe : si le rang V ne porte aucun autre Rêve et est situé à gauche de ce Rêve, déplacez ce Rêve (avec ses Défenseurs solidaires) directement sur le rang V ; sinon, faites glisser ce Rêve vers le premier rang libre à sa gauche (vers le rang 1).
  - **Dilemme** — *Choix* : Sous paravent fermé, l'Oiseau fait face à un vrai casse-tête d'initié : s'il obtient min(D1,D2) = 3 et Dé d'Envol = 1, garde-t-il 1 pour adoucir sa propre machine, ou retient-il 3 afin de laisser le 1 disponible comme dé écarté pour catapulter Le Condor des Brumes directement de la case 6 à la case 1 ! · *Renoncement* : Téléporter une machine ennemie vers un Rêve situé plus à droite neutralise cette machine mais consomme l'annulation de ce second Rêve.
  - **Témoin `R5_T1`** : R5 construit au rang 6 est défendu avec le Chant, tandis que l'Oiseau a révélé un Sabotage dont les dés lancés sous paravent affichent 1 et 5 : R5 lit le dé écarté 1, saute directement du rang 6 au rang 1 par Aile du Songe ET projette par Courant Ascendant un Bulldozer d'Assaut du rang 5 vers le Mode Charge au rang 1 !

---

<a id="lisiere-o-e-g12-r9"></a>
### Lisière `O ↔ E` — Oiseaux ↔ Entités Magiques (`G12` & `R9`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G12`** (`O>E`, GARDIEN) | **L’Ibijau, les yeux fendus de la nuit** — Relit le dé écarté et pousse la machine vers un Rêve (⭐ Éveil · ⚡ Twist 2K3 · sortie `RANG_RELU`) | **L’Ibijau** — Poste désert / Relais de camouflage / Dernier affût (⭐ Éveil · 🌱 Enracinement · sortie `PIEGE`) | **L’Ibijau, Veilleur Fantôme des Souches Grises** — Endort les machines altérées (⭐ Éveil · sortie `ALTERATION`) |
| **`R9`** (`E>O`, REVE) | **La Matinta Pereira, siffleuse de minuit** — Le Rêve vole là où siffle la Plume (🌙 Levier Rêve · sortie `POSITION_REVE`) | **Le Ciel sous l’écorce** — Poste sacrifié · étoile basse (🌙 Levier Rêve · sortie `RANG_REVE`) | **Le Rêve de l’Éclipse de Plumes** — +🌀 + 🌙 ⬅️ + bonus 🪶/🦅 (🌙 Levier Rêve · sortie `RANG_REVE`) |

#### Emplacement `G12` (`O>E` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **L’Ibijau, les yeux fendus de la nuit** | **L’Ibijau** | **L’Ibijau, Veilleur Fantôme des Souches Grises** |
| **Rôles & Nature** | ⭐ Éveil · ⚡ Twist 2K3 (`ACTION`) | ⭐ Éveil · 🌱 Enracinement (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Sabotage** | ACTIVATION / **Sabotage** | ACTIVATION / **Rêve** |
| **Pictogrammes** | ⚡ `PIC_TWIST` · 🎲 `PIC_DES_PARAVENT` · 🔢 `PIC_RANG_MACHINE` · 🌙 `PIC_REVE` | 🪶 `PIC_PLUME` · 🪤 `PIC_PIEGE` · 🪵 `PIC_SOUCHE` · 🌱 `PIC_ENRACINEMENT` | 🌀 `PIC_ALTERATION` · 🪵 `PIC_SOUCHE` · 🚫 `PIC_ANNULATION` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Relit le dé écarté et pousse la machine vers un Rêve | Poste désert / Relais de camouflage / Dernier affût | Endort les machines altérées |
| **Mots-clés Face 1** | Machine révélée → rang de son dé écarté | Poste désert | Mobile sur 🪵 ou 🪶 : si sans 🌀 → pose 1 🌀 (+🔴→🔵) · Si déjà 🌀 → 🚫 à ce tour (ou ⏪ -1) |
| **Mots-clés Face 2** | Ou dé ignoré d’un porteur de Sabotage · le Rêve qui l’annule glisse d’1 rang | Relais de camouflage | Toute mobile : +🌀 + (🔴→🔵 ou ⏪ -1), si déjà 🌀 → 🚫 + 🪤 · Ratissage : 🔴→🔵 + 🪤 |
| **Mots-clés Enraciné** | — | Dernier affût | — |
| **Plancher (`M4`)** | `DES_SOUS_PARAVENT`, `RANG_MACHINE`, `POSITION_REVE` | `PLUME`, `RANG_MACHINE`, `RATISSAGE` | `SOUCHE`, `PLUME`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `SABOTAGE` | `SOUCHE`, `PIEGE` | `ALTERATION`, `ROUGE` |
| **Sorties (`I03`)** | `RANG_RELU`, `ANNULATION_INDUITE` | `PIEGE`, `DEFENSEUR_REDEPLOYE` | `ALTERATION`, `ANNULATION`, `BLEU`, `RECUL`, `PIEGE` |

- **Panel 1 — L’Ibijau, les yeux fendus de la nuit** *(⭐ Éveil · ⚡ Twist 2K3 · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Le jour, l’Ibijau n’est qu’un bout de branche morte. Pourtant il voit : deux fentes dans ses paupières closes guettent tout. La nuit, sa plainte descendante raconte, dit-on, l’histoire d’une jeune femme changée en oiseau, qui pleure encore celui qu’elle a perdu.
  - **Face 1** :
  > Quand l’Ibijau s’active : ses paupières closes voient le dé écarté. Choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez le plus haut des deux dés standards du joueur qui a tiré son jeton : la machine quitte son rang et prend celui de ce dé (si les deux dés étaient égaux, rien ne change). Une machine ne peut jamais être déplacée vers un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement.
  - **Face 2** :
  > Quand l’Ibijau s’active : choisissez une machine révélée qui n’est ni annulée ni encore résolue, puis lisez l’un de ces dés : le plus haut des deux dés standards du joueur qui a tiré son jeton, ou n’importe lequel des deux dés d’un joueur qui a tiré un Sabotage ou une Écaille (des dés d’ordinaire ignorés). La machine quitte son rang et prend celui du dé lu, jamais un rang dont les attaques sont déjà résolues. Arrivée sur le rang d’un Rêve qui n’a pas encore été résolu, elle peut y être annulée normalement ; la complainte de l’urutau guide alors ce Rêve : s’il l’annule, il glisse ensuite d’1 rang vers la gauche si ce rang est libre.
  - **Dilemme** — *Choix* : Quelle machine relire : celle dont le dé écarté tombe pile sur un Rêve défendu, ou celle qu’il faut chasser d’un rang « Sur place » vers un rang moins nuisible. · *Renoncement* : Le dé écarté est presque toujours plus haut : la machine relue peut atterrir sur un rang d’Assaut ou d’En avançant et frapper plus fort si aucun Rêve ne l’y attend.
  - **Double activation** : Chaque Sabotage révélé rallume l’icône de l’Ibijau : deux activations poussent deux machines vers les Rêves de droite avant leur résolution. En Face 2, il puise aussi dans les dés « morts » des porteurs de Sabotage, ce qui lui offre presque toujours un rang utile.
  - **Témoin `G12_T1`** : Bulldozer révélé au rang 1 (dés 1 et 5) ; Rêve E défendu au rang 5 ; l’Ibijau s’active au premier Sabotage : le Bulldozer passe au rang 5 puis est annulé par le Rêve (icône Rêve).

- **Panel 2 — L’Ibijau** *(⭐ Éveil · 🌱 Enracinement · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Là où l’œil croit compter deux branches, l’ibijau attend que le jour finisse.
  - **Face 1** :
  > À chaque activation, vous pouvez poser un Piège ordinaire de la réserve sur une parcelle encore ciblée, sans Défenseur ni Piège ordinaire, du rayon portant la Plume.
  - **Face 2** :
  > À chaque activation, vous pouvez poser un Piège ordinaire de la réserve sur une parcelle encore ciblée, sans Défenseur ni Piège ordinaire. Si elle ne porte que des Souches, vous pouvez aussi déplacer un Défenseur en forêt d’une autre parcelle de son rayon vers la parcelle voisine de la cible, côté cœur, en sautant les Routes.
  - **Enraciné** :
  > Quand vous enracinez l’Ibijau, vous pouvez transférer un Piège ordinaire de n’importe quelle parcelle vers la parcelle désignée si elle est libre de Piège ordinaire.
  - **Dilemme** — *Choix* : Couvrir une case vide ou y envoyer un Défenseur ? · *Renoncement* : Un seul Défenseur déjà sur le poste empêche d’y installer le guet.
  - **Double activation** : Deux affûts couvrent deux parcelles désertes. Une première pose peut aussi être renouvelée après le passage d’une machine.
  - **Témoin `G12_T1`** : Plume en E. L’Ibijau piège E3 vide de Défenseurs. Les Entités peuvent y garder ce Piège contre un Bulldozer ou le sacrifier avec le Rêve du Ciel sous l’écorce.

- **Panel 3 — L’Ibijau, Veilleur Fantôme des Souches Grises** *(⭐ Éveil · ACTIVATION / **Rêve**)*
  - *Ambiance* : « Immobile sur sa souche comme un éclat d’écorce morte, il pousse à la nuit tombée une plainte si lente que l’engin déjà égaré s’endort sur place. »
  - **Face 1** :
  > Lorsque L’Ibijau s’active, ciblez 1 machine mobile occupant une parcelle qui porte au moins 1 Souche, ou appartenant au rayon ou au rang désigné par la Plume de Vigie (à défaut, une machine mobile du rayon Oiseaux ou Entités) :
  > • Si elle ne porte pas de jeton d’Altération : prenez 1 jeton d’Altération de la réserve Entités et posez-le sur elle ; de plus, si elle porte au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges en Bleu Surchauffe.
  > • Si elle porte déjà un jeton d’Altération : laissez ce jeton d’Altération sur elle (pour sa prochaine révélation) et, si son jeton Machine est révélé, non annulé et n’a pas encore résolu son activation à ce tour, inclinez-le à 90° (cette machine est annulée à ce tour) ; sinon, faites-la reculer d’1 parcelle vers la bordure.
  - **Face 2** :
  > Lorsque L’Ibijau s’active, ciblez n’importe quelle machine du plateau :
  > • Si elle est mobile et sans Altération : posez 1 jeton d’Altération de la réserve Entités sur elle, puis au choix retournez 1 de ses jetons Rouges existants en Bleu Surchauffe ou faites-la reculer d’1 parcelle vers la bordure.
  > • Si elle est mobile et porte déjà une Altération : laissez son Altération sur elle, inclinez son jeton Machine à 90° (annulée à ce tour si elle n’a pas encore agi ; sinon recul d’1 parcelle) et posez 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire de son rayon.
  > • Si elle est en Ratissage : retournez 1 de ses jetons Rouges existants en Bleu Surchauffe et posez 1 Piège ordinaire sur sa parcelle si elle en est dépourvue.
  - **Dilemme** — *Choix* : Semer une nouvelle Altération sur une machine intacte pour préparer le tour suivant, ou frapper une machine déjà altérée (par R9 ou une première activation) pour cumuler deux tours complets de neutralisation. · *Renoncement* : Concentrer deux activations sur la même machine la verrouille pour deux tours, mais laisse une seconde machine active frapper librement à ce tour.
  - **Double activation** : Même seul sans R9, deux activations dans le même tour (par exemple sur deux Sabotages ou via Résonance) réalisent le combo complet sur une même cible : la première pose l'Altération (+ Rouge → Bleu), la seconde endort immédiatement la machine à 90° (+ Piège en Face 2, allumant Piégeage en cascade). Avec R9 en jeu, deux activations endorment coup sur coup les deux machines altérées par l'Éclipse.
  - **Témoin `G12_T1`** : À l'ouverture, R9 (Éclipse de Plumes) pose 2 Altérations (dont une Abatteuse en parcelle 2 à 1 Souche) et allume Rêve. L'Ibijau Face 1 (sur Rêve) incline le jeton de l'Abatteuse à 90° : elle est annulée à ce tour ET conserve son Altération pour reculer sans frapper à sa prochaine pioche.

#### Emplacement `R9` (`E>O` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Matinta Pereira, siffleuse de minuit** | **Le Ciel sous l’écorce** | **Le Rêve de l’Éclipse de Plumes** |
| **Rôles & Nature** | 🌙 Levier Rêve (`ACTION`) | 🌙 Levier Rêve (`ACTION`) | 🌙 Levier Rêve (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | 🪶 `PIC_PLUME` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION` | 🪶 `PIC_PLUME` · 🪤 `PIC_PIEGE` · 🦅 `PIC_PERCHOIR` · ⬅️ `PIC_AVANCEE_REVE` | 🪶 `PIC_PLUME` · 🦅 `PIC_PERCHOIR` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION` |
| **Résumé Mini-Tuile** | Le Rêve vole là où siffle la Plume | Poste sacrifié · étoile basse | +🌀 + 🌙 ⬅️ + bonus 🪶/🦅 |
| **Mots-clés Face 1** | Vole de 2 rangs au plus vers la Plume · 0 annulation = 1 Altération | Poste sacrifié · étoile basse | +1 🌀 + 1 🌙 ⬅️ + regarde 🦅 (Chaud/Machine : +2e 🌀 · Calme/🚫 : +2e ⬅️) |
| **Plancher (`M4`)** | `PLUME`, `RANG_REVE` | `PLUME`, `PIEGE`, `POSITION_REVE` | `PLUME`, `PERCHOIR`, `POSITION_REVE` |
| **Synergies (`I01`)** | — | `DE_ENVOL` | `ANNULATION` |
| **Sorties (`I03`)** | `POSITION_REVE`, `ALTERATION` | `RANG_REVE`, `ALTERATION` | `RANG_REVE`, `ALTERATION` |

- **Panel 1 — La Matinta Pereira, siffleuse de minuit** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : Le sifflement de la Matinta semble venir de partout à la fois. Promettez-lui du tabac et elle s’en va ; refusez, et votre nuit sera maudite.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution, avant d’annuler : la Matinta vole vers le sifflement : si la Plume de Vigie est posée près d’un rang de la Réglette, déplacez ce Rêve, avec ses Défenseurs, d’au plus 2 rangs en direction de ce rang (sans le dépasser ni traverser un rang occupé), puis annulez-y normalement ; un Rêve ne se résout qu’une fois par ouverture. Malédiction : si ce Rêve n’annule finalement aucune machine, posez 1 jeton d’Altération sur une machine mobile de votre choix qui n’en porte pas.
  - **Dilemme** — *Choix* : Pour l’Oiseau : poser la Plume près du rang où il sait qu’une machine tombera (la sienne ou celle vue au Perchoir), ou près d’un rang qui compacte le bloc du Sommeil. · *Renoncement* : Poser la Plume près d’un rang, c’est renoncer à l’utiliser au pied d’un rayon pour signaler Chaud ou Calme aux rives de Furtivité.
  - **Témoin `R9_T1`** : Matinta défendue au rang 4 ; la Plume est posée près du rang 2, libre, où l’Oiseau a révélé sa machine : le Rêve vole de 2 rangs jusqu’au rang 2 et l’annule.

- **Panel 2 — Le Ciel sous l’écorce** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : On détache une écaille de bois. Derrière elle, une étoile attendait à hauteur de main.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, si la Plume indique un rayon, vous pouvez y défausser un Piège ordinaire pour avancer ce Rêve d’un rang libre vers la gauche. Si le Dé d’Envol montre le rang d’arrivée, vous pouvez ensuite poser une Altération de la réserve sur une mobile de ce rayon qui n’en porte pas. Les Défenseurs suivent le Rêve.
  - **Dilemme** — *Choix* : Brûler un guet de l’Ibijau pour gagner un rang ? · *Renoncement* : Si le Dé d’Envol ne coïncide pas, la machine de ce rayon conserve son prochain passage.
  - **Témoin `R9_T1`** : Plume en E, Dé d’Envol sur 3. Le Ciel en 4 sacrifie le Piège de l’Ibijau, rejoint le 3 libre et altère le Bulldozer mobile d’E.

- **Panel 3 — Le Rêve de l’Éclipse de Plumes** *(🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : « Là où tombe la plume de vigie, la lune s'éteint pour les hommes de fer : leurs phares éclairent une forêt qui a déjà bougé. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu :
  > 1. Posez 1 jeton d'Altération sur 1 machine mobile qui n'en porte pas encore, ET faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).
  > 2. Consultez secrètement le jeton posé sur le Perchoir de Vigie de l'Oiseau (s'il est face cachée, reposez-le face cachée sans le révéler au reste de la table), puis appliquez 1 bonus d'Éclipse au choix parmi ceux déverrouillés :
  > • Éclipse Chaude (déverrouillée si la Plume de Vigie est face Chaud OU si le Perchoir porte un jeton Machine) : posez 1 second jeton d'Altération sur une machine mobile qui n'en porte pas encore, choisie sur le rayon ou le rang marqué par la Plume — ou directement sur la machine correspondant au jeton du Perchoir.
  > • Éclipse Calme (déverrouillée si la Plume de Vigie est face Calme OU si ce Rêve a annulé au moins 1 machine à cette ouverture) : faites glisser d'1 rang libre vers la gauche un Rêve en jeu de votre choix (le même Rêve pour un double glissement, ou un second Rêve).
  - **Dilemme** — *Choix* : Sous paravents fermés, l'Oiseau oriente silencieusement l'Éclipse par la face (Chaud vs Calme) de sa Plume et le jeton caché sur son Perchoir ; à l'ouverture, les Entités choisissent entre doubler le ralentissement physique (2 Altérations) ou doubler la compression de la Réglette vers le Sommeil (2 glissements de Rêve). · *Renoncement* : Pousser deux fois les Rêves vers la gauche rapproche la victoire par Sommeil mais renonce à neutraliser la prochaine ouverture d'une seconde machine mobile.
  - **Témoin `R9_T1`** : Dans une partie E–O–M (sans H), l'Oiseau a caché 1 Bulldozer sur son Perchoir de Vigie et posé sa Plume face Calme au pied du rayon Mammifère. R9, construit au rang 4 et défendu, consulte le Perchoir (déverrouillant Éclipse Chaude via la Machine cachée ET Éclipse Calme via la Plume Calme) : E choisit Éclipse Calme, pose 1 Altération et fait glisser deux fois R9 (de 4 en 3, puis de 3 en 2, sautant le rang 1 déjà occupé) pour assembler instantanément le bloc contigu 1..2 !

---

## C. Lisières Animal ↔ Essaim (3 lisières · 3 Gardiens + 3 Nids)

<a id="lisiere-m-i-g13-m1"></a>
### Lisière `M ↔ I` — Mammifères ↔ Insectes (`G13` & `M1`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G13`** (`M>I`, GARDIEN) | **Le Tamanoir, le grand mangeur qui épargne** — Mange un peu, fait riposter beaucoup (⭐ Éveil · sortie `RIPOSTE_ESSAIM`) | **Le Tamanoir** — Ouvrière au départ · guide un pas / traversée de la file + Duel (⭐ Éveil · sortie `DEFENSEUR_REDEPLOYE`) | **Le Tamanoir, Sentinelle à Crinière des Fourmilières** — Aspire l'essaim, dresse le Duel (⭐ Éveil · sortie `TERRITOIRE`) |
| **`M1`** (`I>M`, CROISSANCE) | **Le Pelage du Paresseux** — Des passagers qui voyagent sur les machines (Brique fluide · sortie `INSECTE_PASSAGER`) | **Le Nid de la contre-sape** — Nid → file au sol → Défenseur · un paiement par case (⚡ Twist 2K3 · ⚖️ Loi passive · sortie `PARADE_GALERIE`) | **Le Bivouac des Légionnaires, Marée Noire des Sous-Bois** — Raid latéral d'essaim entre rayons (⚡ Twist 2K3 · sortie `RAID_LATERAL`) |

#### Emplacement `G13` (`M>I` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Tamanoir, le grand mangeur qui épargne** | **Le Tamanoir** | **Le Tamanoir, Sentinelle à Crinière des Fourmilières** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Insecte** | ACTIVATION / **Parade** | ACTIVATION / **Parade** |
| **Pictogrammes** | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · ⚔️ `PIC_DUEL` | ⚔️ `PIC_DUEL` · 🐜 `PIC_INSECTE` · 🛡️ `PIC_DEFENSEUR` · ➡️ `PIC_MIGRATION` | 🐜 `PIC_INSECTE` · ⚔️ `PIC_DUEL` · ➡️ `PIC_MIGRATION` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Mange un peu, fait riposter beaucoup | Ouvrière au départ · guide un pas / traversée de la file + Duel | Aspire l'essaim, dresse le Duel |
| **Mots-clés Face 1** | Nid à 2 Insectes ou plus · 1 Insecte mangé → riposte de 2 · sans Nid à éventrer : 1 Insecte de la réserve | Ouvrir le front | +1 🐜 (+Aspire 2 voisins & +1 Réglette/Icône) + ⚔️ Tenu & 🔴→🔵 |
| **Mots-clés Face 2** | Riposte posée sur parcelle ciblée adjacente · parade aidée = Territoire tenu · sans Nid : idem | Longer la colonne | Toute parcelle + Déplace ⚔️ Tenu + 2 voisins & +1 Réglette/Icône |
| **Mots-clés Enraciné** | — | Ordinaire | Standard (1 ou 2 Souches finales) |
| **Plancher (`M4`)** | `INSECTE`, `DUEL` | `DUEL` | `DUEL` |
| **Synergies (`I01`)** | `NID` | `INSECTE` | `INSECTE`, `ROUGE`, `GARDIEN` |
| **Sorties (`I03`)** | `RIPOSTE_ESSAIM`, `INSECTE`, `TERRITOIRE` | `DEFENSEUR_REDEPLOYE`, `INSECTE`, `DUEL` | `TERRITOIRE`, `INSECTE`, `INSECTE_RANG`, `BLEU` |

- **Panel 1 — Le Tamanoir, le grand mangeur qui épargne** *(⭐ Éveil · ACTIVATION / **Insecte**)*
  - *Ambiance* : Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.
  - **Face 1** :
  > La récolte. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1 (le Tamanoir ne vide jamais un Nid). L’Essaim riposte aussitôt : ce Nid produit 2 Insectes, sans allumer d’icône ni appliquer son pouvoir de Nid. Ces Insectes restent sur le Nid et participent normalement aux parades sur sa parcelle.
  > Termitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, le Tamanoir fouille une termitière sauvage : prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée, où il participe aux parades.
  - **Face 2** :
  > La garde dressée. Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1. L’Essaim riposte : ce Nid produit 2 Insectes, sans allumer d’icône, que vous pouvez faire jaillir : posez-les sur la parcelle du Nid ou sur une parcelle ciblée adjacente (même rayon, ou même numéro d’un rayon voisin), où ils participeront aux parades. La garde dressée : si le jeton Duel se trouve sur l’une de ces parcelles, une parade aidée par ces Insectes y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère.
  > Termitière sauvage (plancher) : s’il n’existe aucun Nid à éventrer, prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée ; la garde dressée s’y applique.
  - **Dilemme** — *Choix* : Quel Nid éventrer — celui qui riposte le plus près de la frappe à venir, ou celui qu’il faut regonfler avant la Production. · *Renoncement* : L’Insecte mangé manque à une déviation ou à un Bouclier de lisière ; un Nid réduit à 1 Insecte ne peut plus être éventré.
  - **Double activation** : Deux éventrements, deux ripostes : soit deux Nids différents gonflent à la veille des frappes, soit le même Nid riposte deux fois. En Face 2, chaque riposte jaillit sur la parcelle menacée et fait allumer Insecte à la parade, l’icône du Tamanoir. Sans Nid à éventrer, la seconde termitière sauvage peut porter un Nid tout juste construit jusqu’à ses 2 Insectes.
  - **Témoin `G13_T1`** : Nid à 3 Insectes ; le Tamanoir s’active : 3 − 1 + 2 = 4 Insectes sur le Nid.

- **Panel 2 — Le Tamanoir** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : À chaque pas du géant, la terre s’ouvre derrière lui.
  - **Face 1** :
  > Ouvrir le front. Faites sortir un Insecte de la réserve sur une parcelle de M ou I (ou sur une parcelle survivante d’un autre rayon si M et I sont entièrement Route). Si l’un de vos Défenseurs y est debout, vous pouvez le faire avancer d’un pas radial dans le sens choisi. L’ouvrière reste au départ. Si le Défenseur part du Duel, laissez-le en place sur sa face actuelle ou emportez-le à l’arrivée face Défi.
  - **Face 2** :
  > Longer la colonne. Faites sortir l’Insecte comme en Face 1. Depuis sa parcelle, vous pouvez conduire un de vos Défenseurs dans un sens le long d’une file continue de parcelles portant chacune au moins un Insecte au sol. Arrêtez-vous sur une autre parcelle de la file ou sur la première parcelle au-delà, même vide. Les Insectes restent en place. Le choix d’emporter le Duel face Défi ou de conserver sa face au départ vous appartient toujours.
  - **Dilemme** — *Choix* : Laisser l’ouvrière derrière le combattant pour préparer la galerie de M1 et porter le Défenseur sur la frappe suivante, avec ou sans déplacement du Duel. · *Renoncement* : Emporter un Territoire tenu ouvre un nouveau Défi mais libère l’ancien passage.
  - **Double activation** : À chaque passage, garnissez la case que le Mammifère s’apprête à quitter. Deux percées successives laissent une file de deux parcelles occupées et un Défenseur au débouché.
  - **Témoin `G13_T1`** : Une ouvrière occupe M1 en M·1 ; un Mammifère et son Duel face Défi sont en M·2. G13 fait sortir une ouvrière en M·2 et conduit le Mammifère avec le Duel en M·3. Contre une frappe au seuil de 3, M1 paie 1 ouvrière de M·2 et 1 de M·1 : Parade allumant Insecte et Duel retourné sur Territoire tenu.

- **Panel 3 — Le Tamanoir, Sentinelle à Crinière des Fourmilières** *(⭐ Éveil · ACTIVATION / **Parade**)*
  - *Ambiance* : « Quand le grand fourmilier se dresse debout, la forêt entière converge vers ses griffes : pas un essaim, pas un fauve ne recule d'un pouce. »
  - **Face 1** :
  > Lorsque Le Tamanoir s'active, choisissez 1 parcelle portant le jeton Duel ou au moins 1 Défenseur Mammifère (ou, à défaut, n'importe quelle parcelle du rayon Mammifère ou du rayon Insectes) :
  > 1. Langue Fouettante : posez 1 jeton Insecte de la réserve sur cette parcelle. En outre, s'il existe au moins 1 Insecte sur une parcelle de même numéro (1..4) d'un rayon immédiatement voisin (sans franchir de case devenue Route Forestière), vous pouvez aspirer latéralement jusqu'à 2 de ces Insectes sur la parcelle choisie ET poser 1 Insecte supplémentaire de la réserve directement sur un rang 1–6 de la Réglette ou sur une icône de la Piste des Gardiens.
  > 2. Posture Debout : si le jeton Duel est dans la réserve Mammifère, vous pouvez le poser sur sa face Défi sur cette parcelle ; s'il s'y trouve déjà sur Défi, retournez-le sur Territoire tenu. Enfin, sur 1 machine présente sur cette parcelle (ou ciblant cette parcelle), retournez 1 jeton Rouge existant sur sa face Bleue Surchauffe.
  - **Face 2** :
  > Lorsque Le Tamanoir s'active, choisissez n'importe quelle parcelle de la forêt :
  > 1. Posez 1 Insecte de la réserve sur cette parcelle, ET posez 1 Insecte de la réserve directement sur un rang 1–6 de la Réglette ou sur une icône de la Piste des Gardiens ; vous pouvez en outre aspirer latéralement jusqu'à 2 Insectes situés sur les parcelles de même numéro (1..4) des deux rayons immédiatement voisins (sans franchir de Route Forestière).
  > 2. Vous pouvez déplacer le jeton Duel (depuis la réserve Mammifère ou sa parcelle actuelle) sur cette parcelle, directement tourné sur Territoire tenu, puis retourner 1 jeton Rouge existant sur sa face Bleue Surchauffe sur une machine présente sur (ou ciblant) cette parcelle.
  - **Dilemme** — *Choix* : Aspirer latéralement les Insectes des rayons voisins pour concentrer un bastion imprenable autour du Duel et projeter un Insecte supplémentaire sur la Réglette ou en Bouclier de lisière. · *Renoncement* : L'aspiration dégarnit les parcelles adjacentes où un allié comptait peut-être sur ces ouvrières pour une Parade.
  - **Double activation** : Sur une double activation (ex. posé sur Parade ou Insecte), la 1re activation arme le Duel (ou le passe de Défi à Territoire tenu), refroidit une première machine et concentre l'Essaim ; la 2nde activation renforce un second front ou empile de nouveaux Insectes sur la Réglette et les icônes de la Piste des Gardiens pour sécuriser les paris d'Éveil.
  - **Témoin `G13_T1`** : Tour 3, M1 a déployé des Insectes en parcelle 2 des rayons voisins. Une Parade au rang 1 active Le Tamanoir Face 1 sur la parcelle 2 de M (1 Défenseur, Duel Défi, Bulldozer 2 Rouges seuil 4) : il pose 1 Insecte, aspire 2 Insectes voisins (1 Déf + 3 Ins = 4), pose 1 Insecte sur une icône Gardien, passe Duel sur Territoire tenu et retourne 1 Rouge en Bleu (seuil 4 → 2). Parade Insecte aisée au rang 4.

#### Emplacement `M1` (`I>M` · CROISSANCE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Pelage du Paresseux** | **Le Nid de la contre-sape** | **Le Bivouac des Légionnaires, Marée Noire des Sous-Bois** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | ⚡ Twist 2K3 · ⚖️ Loi passive (`LOI_PASSIVE`) | ⚡ Twist 2K3 (`ACTION`) |
| **Fenêtre / Icône** | PRODUCTION | PRODUCTION / FRAPPE | PRODUCTION |
| **Pictogrammes** | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · ➡️ `PIC_MIGRATION` · ⚔️ `PIC_DUEL` | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · ⚔️ `PIC_DUEL` · ⚡ `PIC_TWIST` | ⚡ `PIC_TWIST` · ➡️ `PIC_MIGRATION` · ⚔️ `PIC_DUEL` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Des passagers qui voyagent sur les machines | Nid → file au sol → Défenseur · un paiement par case | Raid latéral d'essaim entre rayons |
| **Mots-clés Face 1** | 2 Insectes montent sur une machine voisine · sautent sur la parcelle frappée · descente au ménage | Galerie continue | Raid latéral 1–3 🐜 même profondeur (stop 🛣️) + ⚔️ Tenu/+1 🐜 + 🔴→🔵/⏪ 1 |
| **Mots-clés Enraciné** | — | Ordinaire | Standard (1 Souche finale) |
| **Plancher (`M4`)** | `NID`, `INSECTE` | `NID_ACTIVE`, `INSECTE` | `NID_ACTIVE`, `INSECTE`, `ROUTE` |
| **Synergies (`I01`)** | `DUEL` | `DUEL` | `DUEL`, `ROUGE` |
| **Sorties (`I03`)** | `INSECTE_PASSAGER`, `TERRITOIRE` | `PARADE_GALERIE`, `TERRITOIRE` | `RAID_LATERAL`, `TERRITOIRE`, `BLEU`, `RECUL`, `INSECTE` |

- **Panel 1 — Le Pelage du Paresseux** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : La fourrure du paresseux est un monde : des algues, des champignons, des papillons qui n’existent nulle part ailleurs. Ces passagers voyagent sans bouger leurs ailes, et savent descendre au bon endroit.
  - **Face 1** :
  > Production (quand ce Nid est défendu, après avoir produit) : les passagers embarquent : jusqu’à 2 Insectes de ce Nid montent, comme passagers, sur une machine mobile de sa parcelle ou d’une parcelle adjacente du même rayon, et voyagent avec elle. Quand cette machine frappe une parcelle, ses passagers peuvent sauter sur la parcelle frappée et y compter comme Insectes présents pour la parade. Si cette parcelle porte le jeton Duel, une parade aidée par un passager y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère. Au ménage, tout passager non dépensé descend sur place, sur la parcelle de sa machine.
  - **Dilemme** — *Choix* : Sur quelle machine embarquer : celle qui va frapper une parcelle à défendre, ou celle qui avance vers le cœur pour y déposer l’Essaim au ménage. · *Renoncement* : Les passagers quittent le Nid : sa prochaine Production sera plus faible et sa parcelle perd ces renforts.
  - **Témoin `M1_T1`** : 2 passagers sur le Bulldozer du rayon M ; il frappe la parcelle 3 (1 Défenseur, Seuil 3) : les 2 passagers sautent, parade avec Insectes (icône Insecte).

- **Panel 2 — Le Nid de la contre-sape** *(⚡ Twist 2K3 · ⚖️ Loi passive · PRODUCTION / FRAPPE)*
  - *Ambiance* : Le guetteur tient seul au jour. Sous ses pieds, toute la berge répond.
  - **Face 1** :
  > Ouvrir la galerie. Après la Production ordinaire de ce Nid défendu, vous pouvez faire avancer un Insecte de sa parcelle d’un pas radial. La Migration vient ensuite. Vous pouvez aussi le garder au Nid, déjà en mesure de soutenir la parcelle voisine.
  > Payer depuis la galerie (Loi passive). Tant que M1 est en forêt, à une frappe sur une autre parcelle de son rayon portant au moins un Défenseur, vous pouvez choisir une Parade de galerie après le Croc et le Piège. Il faut une file ininterrompue d’Insectes au sol du Nid jusqu’à la parcelle voisine de la cible, Nid compris. Comptez les points qui manquent aux Défenseurs pour atteindre le seuil réel. En partant de la case de la file la plus proche de la cible, défaussez un Insecte par parcelle successive, à hauteur de ce manque. Il faut pouvoir payer tout le manque ainsi. Ce paiement remplace la dépense locale d’Insectes pour cette frappe. Avec au moins un Insecte dépensé, allumez seulement Insecte. Un Défenseur participant sur le Défi peut le retourner sur Territoire tenu.
  - **Dilemme** — *Choix* : Empiler les ouvrières au Nid pour entretenir la Production à deux, ou les étirer une par case pour allonger la portée de la galerie. · *Renoncement* : Payer depuis l’extrémité de la galerie peut rompre la continuité avant une seconde frappe sur le rayon.
  - **Témoin `M1_T1`** : M1, défendu en I·1, commence sa 1re Production à zéro et garde son unique ouvrière au Nid. Un Défenseur en I·2 subit une frappe au seuil de 2 (parcelle libre de Piège ordinaire) : I dépense l’ouvrière d’I·1 (1 Défenseur + 1 Insecte = 2). Au seuil de 3, même deux ouvrières empilées en I·1 n’auraient fourni qu’un seul point par la galerie.

- **Panel 3 — Le Bivouac des Légionnaires, Marée Noire des Sous-Bois** *(⚡ Twist 2K3 · PRODUCTION)*
  - *Ambiance* : « Là où la forêt tient encore debout d'un seul tenant, la légion ignore les frontières : ses ponts vivants submergent trois vallées en une heure. »
  - **Face 1** :
  > À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :
  > 1. Colonne de Raid Latérale (Twist topologique) : choisissez une profondeur de forêt (parcelle 1, 2, 3 ou 4) contenant au moins 1 Insecte sur le rayon de ce Nid (ou sur le rayon portant le jeton Duel). Vous pouvez déplacer latéralement de 1 à 3 Insectes présents sur cette parcelle de départ en les répartissant sur des parcelles de même numéro (1..4) le long de rayons voisins consécutifs (vers la gauche et/ou vers la droite autour du plateau), sans jamais franchir une case devenue Route Forestière. (Ces Insectes pourront ensuite migrer normalement le long de leur nouveau rayon à la Migration.)
  > 2. Morsure d'Avant-Garde : choisissez 1 parcelle ayant reçu au moins 1 Insecte de cette Colonne (ou la parcelle de ce Nid si aucun Insecte n'a changé de rayon) :
  > • Si le jeton Duel s'y trouve sur sa face Défi, retournez-le immédiatement sur Territoire tenu et ajoutez +1 Insecte de la réserve sur cette parcelle ;
  > • De plus, sur 1 machine occupant cette parcelle : si elle possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge) et qu'elle est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).
  - **Dilemme** — *Choix* : Projeter 1 à 3 Insectes latéralement chez les voisins pour irriguer toute la table avant la Migration et activer Morsure d'Avant-Garde sur le Duel ou une machine. · *Renoncement* : Vider le Nid sous le seuil de 2 Insectes fait retomber sa prochaine Production à +1 ; une Route Forestière sur la profondeur choisie coupe définitivement le pont latéral.
  - **Témoin `M1_T1`** : Tour 4 (I, M, H, O ; parcelle 2 d'O est Route). M1 en parcelle 2 de I (2 Insectes) produit +2 (total 4), garde 2 Insectes et envoie 1 en parcelle 2 de M (Duel Défi + Abatteuse sans Rouge) et 1 en parcelle 2 de H (bloqué avant O par la Route). Morsure d'Avant-Garde sur M·2 passe le Duel sur Territoire tenu (+1 Insecte) et recule l'Abatteuse en M·1.

---

<a id="lisiere-r-i-g14-m2"></a>
### Lisière `R ↔ I` — Reptiles ↔ Insectes (`G14` & `M2`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G14`** (`R>I`, GARDIEN) | **Le Téju, la ponte au cœur de la termitière** — Pond une Écaille au cœur d’un Nid (⭐ Éveil · sortie `PONTE`) | **Le Téju** — Sol / fosse ouverte → piste · retour au sol → filet redéployé (⭐ Éveil · sortie `INSECTE_RANG`) | **Le Téju, Maraudeur Doré des Termitières** — Traque machines marquées, déploie Croc (⭐ Éveil · sortie `CROC`) |
| **`M2`** (`I>R`, CROISSANCE) | **La Termitière-Forteresse** — Forteresse d’argile et soldats à glu (Brique fluide · sortie `PARADE_SOLDATS`) | **Le Nid des fours d’argile** — Ouvrière → Piège proche / Piège lointain ↔ ouvrière du Nid (Brique fluide · sortie `PIEGE`) | **La Termitière Cuirassée, Bastion d’Argile et d’Écailles** — +🦎 Sac + 🐜 sur machine 🔴 / rang (Brique fluide · sortie `ECAILLE`) |

#### Emplacement `G14` (`R>I` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Téju, la ponte au cœur de la termitière** | **Le Téju** | **Le Téju, Maraudeur Doré des Termitières** |
| **Rôles & Nature** | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) | ⭐ Éveil (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Insecte** | ACTIVATION / **Sabotage** | ACTIVATION / **Sabotage** |
| **Pictogrammes** | 🦎 `PIC_ECAILLE` · 🪹 `PIC_NID` · 🦷 `PIC_CROC` · 🪤 `PIC_PIEGE` | 🐜 `PIC_INSECTE` · 🪤 `PIC_PIEGE` · 🔢 `PIC_RANG_MACHINE` · ⭐ `PIC_PARI_ENCOCHE` | 🦎 `PIC_ECAILLE` · 🐜 `PIC_INSECTE` · 🔵 `PIC_BLEU` · 🦷 `PIC_CROC` |
| **Résumé Mini-Tuile** | Pond une Écaille au cœur d’un Nid | Sol / fosse ouverte → piste · retour au sol → filet redéployé | Traque machines marquées, déploie Croc |
| **Mots-clés Face 1** | Écaille sous un Nid (sans Nid libre : au sol, rayon R ou I) · frappe → le Croc éclot et pare | Fouille | +1 🦎 sac & +1 🐜 (machine/rang) + Machine avec 🐜 : 🔴→🔵 & (-1 🐜 → 🦷) |
| **Mots-clés Face 2** | Le Croc éclot d’où qu’il soit et pare chaque frappe jusqu’au ménage | Rabattre au terrier | +2 🐜, 2 machines 🔴→🔵 & 🦷 gratuit |
| **Mots-clés Enraciné** | — | Ordinaire | Standard (1 ou 2 Souches finales) |
| **Plancher (`M4`)** | `ECAILLE`, `CROC` | `INSECTE` | `ECAILLE`, `CROC`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `NID` | `PIEGE`, `INSECTE_RANG`, `GARDIEN` | `INSECTE`, `INSECTE_RANG`, `ROUGE` |
| **Sorties (`I03`)** | `PONTE`, `CROC`, `ECAILLE` | `INSECTE_RANG`, `INSECTE_ICONE`, `INSECTE` | `CROC`, `BLEU`, `ECAILLE`, `INSECTE` |

- **Panel 1 — Le Téju, la ponte au cœur de la termitière** *(⭐ Éveil · ACTIVATION / **Insecte**)*
  - *Ambiance* : La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.
  - **Face 1** :
  > La ponte. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. Éclosion : quand une machine frappe la parcelle de ce Nid et que le Croc est dans la réserve Reptile, la ponte éclot avant toute parade : postez le Croc sur cette parcelle ; il pare cette frappe en premier (allumez Piégeage) puis regagne la réserve, et l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
  > Ponte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, le Téju pond dans la litière : posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte. Elle éclot de la même façon quand une machine frappe cette parcelle, et regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois : pondre de nouveau au sol la déplace.
  - **Face 2** :
  > La nichée. Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. La nichée : quand une machine frappe la parcelle de ce Nid, la ponte éclot avant toute parade : postez le Croc sur cette parcelle, où qu’il se trouve (réserve Reptile ou autre parcelle) ; il pare cette frappe en premier (allumez Piégeage) et, au lieu de regagner la réserve, reste sur place pour parer de même chaque frappe suivante sur cette parcelle jusqu’au ménage, où il regagne la réserve tandis que l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
  > Ponte au sol (plancher) : s’il n’existe aucun Nid construit sans ponte, posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte : la nichée y éclot de la même façon, et l’Écaille regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois.
  - **Dilemme** — *Choix* : Sous quel Nid pondre — celui dont la parcelle est visée ce tour, ou un Nid exposé à long terme près du cœur ; sans Nid, quelle parcelle couver. · *Renoncement* : L’Écaille couvée n’est plus dans le sac tant qu’elle n’a pas éclos (moins de Sabotages tirés) ; un Croc parti éclore ne protège plus la parcelle où une Écaille l’avait posté.
  - **Double activation** : Chaque activation installe une ponte sous un Nid différent : deux Nids protégés, deux éclosions possibles, deux icônes Piégeage. En Face 2, une seule ponte suffit à tenir une parcelle pendant toute la phase d’attaques. Sans Nid, la seconde activation déplace la ponte au sol vers la parcelle la plus menacée.
  - **Témoin `G14_T1`** : Ponte sous le Nid de la parcelle 2 du rayon I ; le Bulldozer frappe cette parcelle ; le Croc est en réserve : éclosion, parade du Croc (Piégeage), Écaille au sac.

- **Panel 2 — Le Téju** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : Une motte saute. Les ouvrières trouvent une issue là où le filet tenait encore.
  - **Face 1** :
  > Fouille. Faites sortir un Insecte de la réserve au sol sur une parcelle de R ou I (ou sur une parcelle survivante d’un autre rayon si R et I sont entièrement Route). Vous pouvez à la place ouvrir une fosse sur l’un de ces rayons : rendez un Piège ordinaire de ce rayon à la réserve et posez l’Insecte de la réserve directement sur un rang de la Réglette ou sur l’icône d’un Gardien en piste. L’Insecte pourra servir à la prochaine déviation légale ou au Bouclier de lisière, au choix de I.
  - **Face 2** :
  > Rabattre au terrier. Vous pouvez effectuer la Fouille. Vous pouvez aussi choisir un Piège ordinaire de R ou I et y rabattre un Insecte depuis un rang ou une icône. Posez-le au sol à la place du Piège, puis déplacez ce Piège sur une autre parcelle encore ciblée du même rayon, libre de Piège ordinaire. Les deux destinations doivent être légales avant le rabattage.
  - **Dilemme** — *Choix* : Faire sortir une ouvrière au sol, briser un Piège de M2 pour propulser l’Essaim sur les pistes centrales, ou rappeler en Face 2 une ouvrière pour redéployer le Piège ailleurs. · *Renoncement* : Ouvrir une fosse consomme le Piège ordinaire ; rappeler un Insecte en Face 2 retire une déviation ou un Bouclier de lisière possible.
  - **Double activation** : Deux Sabotages révélés successivement donnent deux fouilles avant les déviations. La première ouvrière peut gagner le rang d’une machine par une fosse, la seconde rejoindre un Nid au sol, à temps pour sa Production.
  - **Témoin `G14_T1`** : M2 a façonné un Piège en I·1 ; une mobile est révélée au rang 4 et deux Sabotages s’ouvrent. G14 (2 paris sur Sabotage) ouvre le Piège au 1er balayage et pose une ouvrière sur le rang 4, puis fait sortir une ouvrière sur M2 au 2nd balayage. I dévie la mobile au rang 3 (allume Insecte). Sans Piège, la sortie au sol reste disponible.

- **Panel 3 — Le Téju, Maraudeur Doré des Termitières** *(⭐ Éveil · ACTIVATION / **Sabotage**)*
  - *Ambiance* : « Réveillé par la fièvre du métal et le crépitement des soldats d'argile, le téju fond droit sur la source de chaleur. »
  - **Face 1** :
  > Lorsque Le Téju s'active :
  > 1. Terrier Solaire : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; ET posez 1 jeton Insecte de la réserve soit sur la parcelle d'une machine de votre choix, soit sur un rang 1–6 de la Réglette occupé par le dé d'une machine.
  > 2. Morsure Thermique : choisissez ensuite 1 machine du plateau dont la parcelle ou le rang 1–6 sur la Réglette contient au moins 1 Insecte :
  > • Si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ;
  > • En outre, si le jeton Croc est dans la réserve Reptile, vous pouvez défausser 1 Insecte présent sur la parcelle ou sur le rang 1–6 de cette machine pour poser immédiatement le Croc sur n'importe quelle parcelle ciblée (par une machine non encore activée à ce tour, mobile ou en Ratissage).
  - **Face 2** :
  > Lorsque Le Téju s'active :
  > 1. S'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; ET posez 2 jetons Insectes de la réserve, répartis librement sur des parcelles occupées par des machines et/ou sur des rangs 1–6 occupés par des dés de machines.
  > 2. Appliquez Morsure Thermique sur jusqu'à 2 machines distinctes dont la parcelle ou le rang contient au moins 1 Insecte (retournant 1 jeton Rouge existant → Bleu Surchauffe sur chacune d'elles) ; de plus, si au moins l'une d'elles est ainsi ciblée et que le Croc est dans la réserve Reptile, posez immédiatement le Croc sur une parcelle ciblée sans avoir à défausser d'Insecte.
  - **Dilemme** — *Choix* : En Face 1, consommer un Insecte posé sur la parcelle ou le rang d'une machine Rouge (notamment celui parachuté par M2) pour déployer aussitôt le Croc et allumer Piégeage. · *Renoncement* : Défausser cet Insecte le retire d'une Parade Insecte ou d'une déviation ±1 au tour suivant.
  - **Double activation** : Posé sur Piégeage ou Sabotage, Le Téju enchaîne deux injections d'Écailles, refroidit deux machines Rouges marquées par M2 et recycle le Croc entre deux attaques pour catalyser les paris de toute la Piste des Gardiens.
  - **Témoin `G14_T1`** : Tour 4, à la Production, M2 a parachuté 1 Insecte sur le rang 5 d'un Bulldozer (2 Rouges). Aux attaques (rang 1), le Croc pare une Abatteuse (Piégeage) et active Le Téju Face 1 : +1 Écaille au sac, +1 Insecte sur une autre machine Rouge, puis Morsure Thermique sur le Bulldozer du rang 5 (1 Rouge → Bleu, défausse l'Insecte du rang 5 pour reposer le Croc devant ce Bulldozer).

#### Emplacement `M2` (`I>R` · CROISSANCE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Termitière-Forteresse** | **Le Nid des fours d’argile** | **La Termitière Cuirassée, Bastion d’Argile et d’Écailles** |
| **Rôles & Nature** | Brique fluide (`ACTION`) | Brique fluide (`ACTION`) | Brique fluide (`ACTION`) |
| **Fenêtre / Icône** | PRODUCTION | PRODUCTION | PRODUCTION |
| **Pictogrammes** | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC` | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · 🪤 `PIC_PIEGE` · ➡️ `PIC_MIGRATION` | 🪹 `PIC_NID` · 🦎 `PIC_ECAILLE` · 🐜 `PIC_INSECTE` · 🔴 `PIC_ROUGE` |
| **Résumé Mini-Tuile** | Forteresse d’argile et soldats à glu | Ouvrière → Piège proche / Piège lointain ↔ ouvrière du Nid | +🦎 Sac + 🐜 sur machine 🔴 / rang |
| **Mots-clés Face 1** | 2 Insectes du Nid parent seuls toute frappe · Production = 1 Écaille au sac ou Croc posté | Cuire ou déterrer | +1 🦎 Sac (ou +1 🐜 si 0 🦎 réserve) · Si 💥/🦎 ou 🔴 : +1 🐜 sur machine 🔴 ou rang 1–6 |
| **Mots-clés Enraciné** | — | Ordinaire | — |
| **Plancher (`M4`)** | `NID`, `INSECTE` | `NID_ACTIVE`, `INSECTE` | `NID_ACTIVE`, `ROUGE` |
| **Synergies (`I01`)** | — | `PIEGE` | `SABOTAGE`, `ECAILLE` |
| **Sorties (`I03`)** | `PARADE_SOLDATS`, `ECAILLE`, `CROC` | `PIEGE`, `INSECTES_TRANSPORTES` | `ECAILLE`, `INSECTE` |

- **Panel 1 — La Termitière-Forteresse** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : Le mur de la termitière est plus dur que la brique. Ses soldats, la tête en forme de seringue, projettent une glu qui colle tout ce qui ose y toucher. Les reptiles le savent : il n’est pas d’abri plus sûr.
  - **Face 1** :
  > Les soldats (quand une machine frappe la parcelle de ce Nid) : avant la parade classique, vous pouvez défausser 2 Insectes de ce Nid ; ils parent cette frappe à eux seuls, quel que soit le Seuil de Parade (allumez l’icône Insecte). Argile d’écailles (à la Production, quand ce Nid est défendu, après avoir produit), choisissez : le joueur Reptile glisse 1 Écaille de sa réserve dans le sac ; ou, si le Croc est dans la réserve Reptile et qu’une machine mobile se trouve sur la parcelle de ce Nid, postez le Croc sur cette parcelle.
  - **Dilemme** — *Choix* : Faire tenir la termitière par ses soldats (2 Insectes par frappe) ou garder ces Insectes pour produire et migrer. · *Renoncement* : Chaque défense des soldats vide le Nid de 2 Insectes et affaiblit sa prochaine Production ; une Écaille glissée au sac ne servira plus aux pontes du Téju.
  - **Témoin `M2_T1`** : Nid à 3 Insectes en parcelle 2 ; une Abatteuse en Mode Assaut à 2 Rouges y frappe (Seuil 4) sans aucun Défenseur : 2 Insectes défaussés, frappe parée, icône Insecte.

- **Panel 2 — Le Nid des fours d’argile** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : Les potières savent quelle croûte portera une patte et laquelle cédera sous une roue.
  - **Face 1** :
  > Cuire ou déterrer. Après la Production ordinaire de ce Nid défendu, vous pouvez cuire un couvercle : rendez un Insecte du Nid à la réserve et posez un Piège ordinaire de la réserve sur le Nid ou à un pas radial, sur une parcelle libre de Piège ordinaire. Vous pouvez plutôt déterrer un Piège situé sur une autre parcelle du rayon : échangez-le contre un Insecte du Nid. Le Piège arrive sur le Nid, qui doit être libre de Piège ordinaire, et l’Insecte arrive au sol sur la parcelle libérée. Il pourra migrer normalement. Dans les deux cas, vérifiez la place et les pièces disponibles avant le paiement.
  - **Dilemme** — *Choix* : Cuire une ouvrière en Piège autonome, la garder au Nid pour approcher la Production à deux, ou déterrer un filet lointain pour protéger le Nid tout en avançant l’ouvrière. · *Renoncement* : Dépenser la première ouvrière ramène le Nid à zéro et ralentit la montée en régime de l’Essaim.
  - **Témoin `M2_T1`** : Le Nid défendu en R·3 produit sa 1re ouvrière (aucun Piège ni Croc sur R). I dépense cette ouvrière et pose un Piège ordinaire en R·4 ; le Nid revient à zéro. Si le Bulldozer en Ratissage y frappe, le Piège pare sans Défenseur et allume Piégeage.

- **Panel 3 — La Termitière Cuirassée, Bastion d’Argile et d’Écailles** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : « Cuite par la chaleur même des moteurs, sa muraille secrète des plaques de pierre vive qui grippent les engrenages de toute la forêt. »
  - **Face 1** :
  > À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :
  > 1. Carapace Minérale : s'il reste au moins 1 jeton Écaille dans la réserve Reptile, glissez-le dans le sac opaque ; sinon (si les 4 Écailles sont déjà hors de la réserve Reptile), ajoutez +1 Insecte de la réserve sur la parcelle de ce Nid.
  > 2. Réplique Thermique : si au moins 1 Sabotage ou Écaille a été révélé à cette ouverture OU si au moins 1 machine du plateau porte un jeton Rouge (y compris en Ratissage), prenez 1 Insecte supplémentaire de la réserve et posez-le directement soit sur la parcelle d'une machine portant au moins 1 jeton Rouge, soit sur un rang 1–6 de la Réglette occupé par le dé d'une telle machine.
  - **Dilemme** — *Choix* : Parachuter l'Insecte bonus directement sur la parcelle d'une machine en Ratissage (d'où il pourra parer sur place ou migrer immédiatement depuis la dernière parcelle vers une icône Gardien !) ou l'installer tout de suite sur un rang 1–6 pour préparer une déviation ±1 dès la prochaine ouverture. · *Renoncement* : Défendre M2 chaque tour vide rapidement la réserve d'Écailles Reptiles vers le sac (maximisant la dilution, mais privant temporairement un effet comme G9 d'Écaille fraîche en réserve tant qu'aucune n'a été consommée).
  - **Témoin `M2_T1`** : Au Tour 3, M2 est défendu alors qu'un Bulldozer allié en parcelle 4 est déjà passé en Ratissage (+1 jeton Rouge physique). Après sa production standard, M2 glisse 1 Écaille dans le sac opaque et pose +1 Insecte de la réserve directement en parcelle 4 sur le Bulldozer en Ratissage : à la Migration qui suit immédiatement, cet Insecte peut soit rester en parcelle 4 pour préparer une Parade Insecte + la cible du Téju, soit sauter directement de la parcelle 4 vers la Piste des Gardiens !

---

<a id="lisiere-o-i-g15-m3"></a>
### Lisière `O ↔ I` — Oiseaux ↔ Insectes (`G15` & `M3`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`G15`** (`O>I`, GARDIEN) | **Le Colibri, porteur de gouttes et de pollen** — Transporte l’Essaim à vol d’oiseau (⭐ Éveil · 🌱 Enracinement · sortie `INSECTE_TRANSPORTE`) | **Le Colibri** — Grand dé · nectar / Nectar · vol retour (⭐ Éveil · ⚡ Twist 2K3 · sortie `INSECTE_RANG`) | **Le Colibri, Joyau Émeraude des Cimes** — Pollinise pistes, valide paris, régénère (⭐ Éveil · 🌱 Enracinement · sortie `PARI_GLISSE`) |
| **`M3`** (`I>O`, CROISSANCE) | **Le Bivouac des Légionnaires** — Un Nid nomade qui suit la Plume (⚡ Twist 2K3 · sortie `NID_NOMADE`) | **Le Nid des feuilles cousues** — Chaud · sentinelle / Calme · rappel (Brique fluide · sortie `INSECTE_ICONE`) | **Le Nid Tisserand des Cimes, Hamac de Soie des Hauts Vents** — 🦅/🪶 → projection directe 🐜 sur rang 1–6 (Brique fluide · sortie `INSECTE_RANG`) |

#### Emplacement `G15` (`O>I` · GARDIEN)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Colibri, porteur de gouttes et de pollen** | **Le Colibri** | **Le Colibri, Joyau Émeraude des Cimes** |
| **Rôles & Nature** | ⭐ Éveil · 🌱 Enracinement (`ACTION`) | ⭐ Éveil · ⚡ Twist 2K3 (`ACTION`) | ⭐ Éveil · 🌱 Enracinement (`ACTION`) |
| **Fenêtre / Icône** | ACTIVATION / **Parade** | OUVERTURE / ACTIVATION / **Sabotage** | ACTIVATION / **Insecte** |
| **Pictogrammes** | 🐜 `PIC_INSECTE` · ➡️ `PIC_MIGRATION` · 🪹 `PIC_NID` · 🌱 `PIC_ENRACINEMENT` | 🎲 `PIC_DES_PARAVENT` · 🐜 `PIC_INSECTE` · ➡️ `PIC_MIGRATION` · 🔢 `PIC_RANG_MACHINE` | 🐜 `PIC_INSECTE` · ⭐ `PIC_PARI_ENCOCHE` · 🔵 `PIC_BLEU` · 🌱 `PIC_ENRACINEMENT` |
| **Résumé Mini-Tuile** | Transporte l’Essaim à vol d’oiseau | Grand dé · nectar / Nectar · vol retour | Pollinise pistes, valide paris, régénère |
| **Mots-clés Face 1** | 1 Insecte pris n’importe où → n’importe quelle parcelle · aucun Insecte en jeu = 1 de la réserve | Grand dé · nectar | +1 🐜 (Dé Envol/🪶, ou Icône si Calme) + [Piqué 🔴→🔵/⏪ 1 OU -1 🐜 Icône → ⭐] |
| **Mots-clés Face 2** | 2 Insectes · arrivée sur un Nid = +1 Insecte · Plume près d’un rang = dépôt sur la Réglette | Nectar · vol retour | +1 🐜 libre (dont Icône) + Les 2 effets |
| **Mots-clés Enraciné** | Fin de partie : tuiles enracinées voisines, 1 repousse de plus | — | Fin : +1 🪵 sur ≤ 2 parcelles avec 🐜/🪹 |
| **Plancher (`M4`)** | `PLUME` | `DES_SOUS_PARAVENT`, `INSECTE`, `RANG_MACHINE` | `DE_ENVOL`, `PLUME`, `GARDIEN` |
| **Synergies (`I01`)** | `INSECTE`, `NID` | `INSECTE_RANG` | `INSECTE`, `INSECTE_RANG`, `ROUGE`, `SOUCHE` |
| **Sorties (`I03`)** | `INSECTE_TRANSPORTE`, `INSECTE`, `INSECTE_RANG`, `ARBRE` | `INSECTE_RANG`, `INSECTE_RAPATRIE` | `PARI_GLISSE`, `INSECTE_RANG`, `BLEU`, `RECUL`, `ARBRE` |

- **Panel 1 — Le Colibri, porteur de gouttes et de pollen** *(⭐ Éveil · 🌱 Enracinement · ACTIVATION / **Parade**)*
  - *Ambiance* : Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.
  - **Face 1** :
  > Le porteur de gouttes. Quand le Colibri s’active, il emporte un passager : déplacez 1 Insecte depuis n’importe quel Nid, parcelle, rang de la Réglette ou icône de la Piste des Gardiens vers n’importe quelle parcelle de n’importe quel rayon. Il y participe normalement aux parades (une parade aidée par un Insecte allume l’icône Insecte).
  > Amorçage — narines fleuries (plancher) : s’il n’y a encore aucun Insecte en jeu, le Colibri en rapporte un des fleurs : prenez-le dans la réserve de l’Essaim.
  - **Face 2** :
  > La tournée. Quand le Colibri s’active, il fait sa tournée : déplacez jusqu’à 2 Insectes, pris n’importe où (Nid, parcelle, rang de la Réglette, icône de la Piste des Gardiens), vers une ou deux parcelles de n’importe quels rayons, où ils participent aux parades. S’il n’y a encore aucun Insecte en jeu, le premier vient de la réserve de l’Essaim.
  > Pollinisation : si l’un d’eux arrive sur un Nid, ce Nid produit aussitôt 1 Insecte, sans allumer d’icône ni appliquer son pouvoir de Nid.
  > Fleur signalée : si la Plume de Vigie est posée près d’un rang de la Réglette, vous pouvez déposer l’un de ces passagers sur ce rang plutôt que sur une parcelle : il y servira à une déviation, une lanterne ou un rite.
  - **Enraciné** :
  > La part du colibri. Au décompte final, chaque autre tuile enracinée au pied de son rayon ou d’un rayon voisin fait repousser 1 Souche de plus.
  - **Dilemme** — *Choix* : Quel Insecte déplacer, et d’où — vider un rang, un Nid ou une icône pour compléter une parade imminente ; en Face 2, faire escale sur un Nid pour le polliniser, ou déposer un passager là où siffle la Plume. · *Renoncement* : Chaque Insecte emporté laisse un trou ailleurs (une déviation, une Production plus faible, un Bouclier de lisière en moins) ; un passager posé sur la Réglette ne pare rien ce tour-ci.
  - **Double activation** : Une goutte par activation : la première complète la parade d’une frappe imminente, la seconde ravitaille une autre parcelle ou, en Face 2, pollinise un Nid qui produira +2 à sa prochaine Production. Chaque parade aidée allume Insecte et relance la Piste.
  - **Témoin `G15_T1`** : Amorçage (Tour 2, aucun Nid construit, aucun Insecte en jeu) : la parcelle 3 du rayon M est visée au rang 4 (Seuil 3) et gardée par 2 Défenseurs. Après une parade au rang 1, le Colibri (sur Parade) apporte 1 Insecte de la réserve sur cette parcelle ; au rang 4, parade réussie avec cet Insecte défaussé (icône Insecte).

- **Panel 2 — Le Colibri** *(⭐ Éveil · ⚡ Twist 2K3 · OUVERTURE / ACTIVATION / **Sabotage**)*
  - *Ambiance* : Le colibri revient de corolle en corolle par le même chemin. Une fleur vidée change le sens de sa tournée.
  - **Face 1** :
  > À l’ouverture, laissez visible le plus grand dé standard de l’Oiseau à sa valeur lancée, même sur Sabotage ou Écaille. En cas de double, gardez le dé inutilisé. À chaque activation, vous pouvez envoyer un Insecte au sol de O ou I directement sur le rang indiqué par ce dé. L’envoi ne dépense pas l’Insecte et ne déclenche pas de déviation à lui seul.
  - **Face 2** :
  > À l’ouverture, conservez visible le plus grand dé standard de l’Oiseau à sa valeur lancée, même sur Sabotage ou Écaille. En cas de double, gardez le dé inutilisé. À chaque activation, vous pouvez envoyer un Insecte au sol de n’importe quel rayon directement sur ce rang, ou en ramener un de ce rang sur une parcelle encore ciblée. Un transfert seul n’allume aucune icône.
  - **Dilemme** — *Choix* : Stocker un vol sur la Réglette ou ramener le dernier renfort vers une frappe ? · *Renoncement* : Une ouvrière descendue du rang ne pourra plus y dévier une machine.
  - **Double activation** : Deux vols peuvent fournir deux déviations distinctes au même rang ou évacuer deux ouvrières vers deux cibles.
  - **Témoin `G15_T1`** : L’Oiseau a tiré Sabotage et lancé 2 et 5. Le Colibri envoie une ouvrière sur 5 lors du balayage du Sabotage. À la fenêtre suivante, elle peut être défaussée pour dévier la machine de 5 à 4 sur un Rêve défendu.

- **Panel 3 — Le Colibri, Joyau Émeraude des Cimes** *(⭐ Éveil · 🌱 Enracinement · ACTIVATION / **Insecte**)*
  - *Ambiance* : « Cent battements d'ailes par seconde : là où le joyau vert effleure la corolle, l'essaim trouve sa route et la forêt garde mémoire de sa floraison. »
  - **Face 1** :
  > Lorsque Le Colibri s'active :
  > 1. Pollen des Cimes : posez 1 jeton Insecte de la réserve soit sur le rang 1–6 de la Réglette indiqué par le Dé d'Envol de l'Oiseau, soit sur l'emplacement marqué par la Plume de Vigie (sur ce rang 1–6, ou sur la 1re parcelle du rayon au pied duquel repose la Plume) — OU, si la Plume de Vigie affiche sa face Calme, directement sur l'icône de votre choix de la Piste des Gardiens.
  > 2. L'Appel du Colibri : choisissez 1 seul des deux effets suivants :
  > • Piqué Vertigineux : sur 1 machine dont le dé occupe un rang portant au moins 1 Insecte (ou située sur le rayon marqué par la Plume de Vigie), retournez 1 jeton Rouge existant sur sa face Bleue Surchauffe ; si elle ne porte aucun jeton Rouge et est mobile, faites-la reculer d'1 parcelle vers la bordure de son rayon (en sautant les Routes Forestières, sans dépasser la 1re parcelle).
  > • Nectar d'Éveil : défaussez 1 Insecte présent sur l'icône d'un Gardien de la Piste des Gardiens portant encore au moins 1 Défenseur en pari : glissez immédiatement 1 de ces Défenseurs dans une encoche latérale libre de ce Gardien (sécurisant cette mise pour la Face 2 ou l'Éveil de la Forêt, sans déclencher le pouvoir de ce Gardien).
  - **Face 2** :
  > Lorsque Le Colibri s'active :
  > 1. Posez 1 jeton Insecte de la réserve sur le rang du Dé d'Envol, sur l'emplacement marqué par la Plume de Vigie, OU directement sur n'importe quelle icône de la Piste des Gardiens (quelle que soit la face de la Plume).
  > 2. Résolvez les deux effets de L'Appel du Colibri (Piqué Vertigineux ET Nectar d'Éveil).
  - **Enraciné** :
  > Pollinisation Suprême (Décompte final uniquement). Au décompte final (Tour 8, Sommeil ou Éveil), tant que la parcelle d'ancrage du Colibri n'est pas devenue une Route Forestière, en plus de sa régénération standard sur cette parcelle (1 Souche retournée en Arbre debout en Face 1, ou 2 en Face 2), retournez 1 Souche survivante supplémentaire en Arbre debout sur chacune d'au plus 2 autres parcelles de la forêt contenant au moins 1 Insecte ou 1 Nid (à défaut, sur d'autres parcelles du rayon Oiseau).
  - **Dilemme** — *Choix* : Consommer un Insecte d'icône (via M3 ou Plume Calme) par Nectar d'Éveil pour convertir un Bouclier de lisière en vrai pari gagné, ou enraciner Le Colibri en Face 2 pour sauver jusqu'à 4 Souches au décompte final. · *Renoncement* : Défausser l'Insecte d'icône retire le Bouclier de lisière en cas de seconde mise non validée ; enraciner Le Colibri sacrifie son catalyseur d'Éveil actif.
  - **Double activation** : Sur Insecte (allumé une 1re fois à l'ouverture par déviation ±1, puis une 2nde fois aux attaques par Parade Insecte), Le Colibri pose 2 Insectes aériens, refroidit ou refoule une machine et fait glisser un pari allié bloqué pour boucler l'Éveil de la Forêt.
  - **Témoin `G15_T1`** : Tour 6, M3 a projeté 1 Insecte sur Sabotage où un Gardien allié porte encore 1 pari. Aux attaques, une Parade Insecte active Le Colibri Face 2 : il pose 1 Insecte sur le rang 4 du Dé d'Envol, retourne 1 Rouge en Bleu par Piqué Vertigineux, puis défausse l'Insecte de Sabotage par Nectar d'Éveil pour glisser le dernier pari d'Éveil. Enraciné Face 2, il retourne jusqu'à 4 Souches au décompte final.

#### Emplacement `M3` (`I>O` · CROISSANCE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Bivouac des Légionnaires** | **Le Nid des feuilles cousues** | **Le Nid Tisserand des Cimes, Hamac de Soie des Hauts Vents** |
| **Rôles & Nature** | ⚡ Twist 2K3 (`ACTION`) | Brique fluide (`ACTION`) | Brique fluide (`ACTION`) |
| **Fenêtre / Icône** | PRODUCTION | PRODUCTION | PRODUCTION |
| **Pictogrammes** | ⚡ `PIC_TWIST` · 🪹 `PIC_NID` · ➡️ `PIC_MIGRATION` · 🪶 `PIC_PLUME` | 🪹 `PIC_NID` · 🪶 `PIC_PLUME` · 🐜 `PIC_INSECTE` · ⭐ `PIC_PARI_ENCOCHE` | 🪹 `PIC_NID` · 🦅 `PIC_PERCHOIR` · 🪶 `PIC_PLUME` · 🐜 `PIC_INSECTE` |
| **Résumé Mini-Tuile** | Un Nid nomade qui suit la Plume | Chaud · sentinelle / Calme · rappel | 🦅/🪶 → projection directe 🐜 sur rang 1–6 |
| **Mots-clés Face 1** | Chaque Production · le Nid se déplace d’1 parcelle (2 vers la Plume) · raid de 2 Insectes | Chaud · sentinelle / Calme · rappel | 1 🐜 du 🪹 → rang Dé d’Envol ou 🪶 · Si 🪶 rayon/Calme : +1 🐜 réserve ou icône |
| **Plancher (`M4`)** | `NID`, `INSECTE` | `NID_ACTIVE`, `PLUME`, `INSECTE` | `NID_ACTIVE`, `DE_ENVOL`, `PLUME` |
| **Synergies (`I01`)** | `PLUME` | `INSECTE_RANG`, `GARDIEN` | `GARDIEN` |
| **Sorties (`I03`)** | `NID_NOMADE`, `INSECTE` | `INSECTE_ICONE`, `INSECTE_RAPPELE` | `INSECTE_RANG`, `INSECTE` |

- **Panel 1 — Le Bivouac des Légionnaires** *(⚡ Twist 2K3 · PRODUCTION)*
  - *Ambiance* : Le bivouac n’a pas de murs : ce sont les fourmis elles-mêmes, accrochées les unes aux autres. Chaque nuit, la colonne repart ; et derrière son front de raid, les oiseaux fourmiliers suivent, guettant ce qui s’enfuit.
  - **Face 1** :
  > Nid nomade (à chaque Production, avant de produire, que ce Nid soit défendu ou non) : le bivouac lève le camp : déplacez ce Nid, avec ses Insectes, vers une parcelle libre (sans machine ni autre Nid) adjacente : sur le même rayon, ou à la parcelle de même numéro d’un rayon voisin. Si ce déplacement le rapproche du rayon désigné par la Plume de Vigie, ou le garde sur ce rayon, il peut enchaîner 2 parcelles adjacentes libres au lieu d’1 : les oiseaux fourmiliers guident la colonne. Puis, s’il est défendu à sa nouvelle place, il produit normalement. Front de raid (après la production) : jusqu’à 2 Insectes du bivouac peuvent se poster sur une parcelle adjacente visée par une machine révélée, où ils participeront aux parades.
  - **Dilemme** — *Choix* : Où lever le camp : vers la parcelle menacée pour y lancer le raid, ou loin d’un Bulldozer qui menace d’en faire une Route. · *Renoncement* : Le bivouac qui quitte la parcelle de son Défenseur ne produit pas ; et un Nid qui s’approche des machines risque d’être renvoyé en lisière.
  - **Témoin `M3_T1`** : Bivouac en parcelle 1 du rayon I ; la Plume est au pied du rayon O voisin : le Nid passe en parcelle 1 du rayon O puis en parcelle 2 (2 pas vers la Plume) ; défendu là, il produit.

- **Panel 2 — Le Nid des feuilles cousues** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : À la couture de deux feuilles, une chaîne d’ouvrières tend ou relâche le fil.
  - **Face 1** :
  > Après la production de ce Nid défendu, si la Plume montre Chaud, vous pouvez déplacer un Insecte d’un rang de la Réglette vers l’icône d’un Gardien en piste. Si elle montre Calme, vous pouvez rappeler un Insecte d’une icône sur la parcelle du Nid. Le Bouclier de lisière reste au choix des Insectes au verdict et un pari perdu le reste même si le Bouclier maintient le Gardien.
  - **Dilemme** — *Choix* : Coudre une assurance à un Gardien ou refaire la masse du Nid ? · *Renoncement* : L’Insecte retiré du rang ne servira pas à une déviation.
  - **Témoin `M3_T1`** : Le Colibri a laissé une ouvrière sur 5. Avec Plume Chaud, le Nid la place sur l’icône d’un Gardien menacé. Au verdict, I peut la dépenser pour maintenir sa Face 2 malgré le pari perdu.

- **Panel 3 — Le Nid Tisserand des Cimes, Hamac de Soie des Hauts Vents** *(Brique fluide · PRODUCTION)*
  - *Ambiance* : « Pourquoi ramper à travers les souches quand un seul fil tendu sous l'aile de l'oiseau suffit à traverser toute la canopée ? »
  - **Face 1** :
  > À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :
  > 1. Fil d'Envol : prenez 1 Insecte présent sur la parcelle de ce Nid (ou sur une parcelle du rayon Oiseau) et placez-le directement sur le rang 1–6 de la Réglette indiqué par le Dé d'Envol de l'Oiseau — OU, si la Plume de Vigie est posée près d'un rang 1–6, sur ce rang (sans passer par la dernière parcelle).
  > 2. Brise de Vigie : si la Plume de Vigie est posée au pied du rayon de ce Nid ou du rayon Oiseau, OU si elle est sur sa face Calme, choisissez 1 bonus : ajoutez +1 Insecte de la réserve sur la parcelle de ce Nid, OU projetez 1 Insecte présent sur la parcelle de ce Nid directement sur l'icône de votre choix de la Piste des Gardiens (pour préparer un Bouclier de lisière ou l'appel du Colibri).
  - **Dilemme** — *Choix* : Même construit dès le Tour 1 en parcelle 1, M3 contourne les 3 tours de marche vers la parcelle 4 : l'Oiseau choisit sous paravent s'il utilise sa Plume pour désigner un rang libre précis à l'Essaim ou s'il la pose face Calme au pied d'un rayon pour générer +1 Insecte ou un Bouclier de lisière instantané. · *Renoncement* : Projeter 2 Insectes hors du Nid en un seul tour dégarnit la parcelle du Nid et risque de ramener sa production suivante de +2 à +1 si moins de 2 Insectes y restent.
  - **Témoin `M3_T1`** : Dès le Tour 1, M3 est construit en parcelle 3 du rayon Insectes (sans machine au départ décalé !) et défendu au Tour 2. L'Oiseau a obtenu 4 sur son Dé d'Envol et posé sa Plume face Calme près du rang 2. Après production, M3 catapulte directement 1 Insecte sur le rang 2 (Plume) et gagne +1 Insecte bonus sur le Nid (face Calme) sans avoir jamais eu besoin d'atteindre la parcelle 4 !

---

## D. Triangle Autonome A = 0 `{H, E, I}` (3 lisières · 4 Rêves + 2 Nids)

<a id="lisiere-h-e-r1-r2"></a>
### Lisière `H ↔ E` — Humains ↔ Entités Magiques (`R1` & `R2`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`R1`** (`H>E`, REVE) | **La Liane des Esprits** — Tire un Rêve des Entités contre elle (🔓 A=0 · 🌙 Levier Rêve · 🌱 Enracinement · sortie `REVE_COMPACTE`) | **La Nasse à contre-courant** — Reflux à droite · bloc à gauche (🌙 Levier Rêve · ⚡ Twist 2K3 · 🔓 A=0 · sortie `RANG_REVE`) | **Le Chant du Voyage Astral** — Guide Tambour ou purifie Chant (🔓 A=0 · sortie `DEFENSEUR_REDEPLOYE`) |
| **`R2`** (`E>H`, REVE) | **La Iara, mère des eaux** — Le Chant remonte le fleuve plus facilement (🔓 A=0 · ⚖️ Loi passive · 🌙 Levier Rêve · sortie `GLISSEMENT_CHANT`) | **Le Fleuve sous la cendre** — Tambour / Souches → Altération · ancrage marqué → Souche finale supplémentaire (🔓 A=0 · 🌱 Enracinement · sortie `ALTERATION`) | **Le Pacte des Doubles Chamaniques** — Le Tambour reflète l'altération mystique (🔓 A=0 · ⚖️ Loi passive · sortie `ALTERATION`) |

#### Emplacement `R1` (`H>E` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Liane des Esprits** | **La Nasse à contre-courant** | **Le Chant du Voyage Astral** |
| **Rôles & Nature** | 🔓 A=0 · 🌙 Levier Rêve · 🌱 Enracinement (`ACTION`) | 🌙 Levier Rêve · ⚡ Twist 2K3 · 🔓 A=0 (`ACTION`) | 🔓 A=0 (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | 🌙 `PIC_REVE` · ⬅️ `PIC_AVANCEE_REVE` · 🚫 `PIC_ANNULATION` · 🌱 `PIC_ENRACINEMENT` | 🌙 `PIC_REVE` · ⬅️ `PIC_AVANCEE_REVE` · 🎶 `PIC_CHANT` · ⚡ `PIC_TWIST` | 🌀 `PIC_ALTERATION` · 🥁 `PIC_TAMBOUR` · 🎶 `PIC_CHANT` · ⬅️ `PIC_AVANCEE_REVE` |
| **Résumé Mini-Tuile** | Tire un Rêve des Entités contre elle | Reflux à droite · bloc à gauche | Guide Tambour ou purifie Chant |
| **Mots-clés Face 1** | Rêve des Entités tiré contre la Liane · collé = la paire glisse à gauche · aucun à droite = la Liane grimpe d’1 rang, sinon serre 1 machine de plus | Reflux à droite · bloc à gauche | 🌀/🔴→🔵 + [Téléporte 🥁 & 🔴→🔵/🌀 OU 🎶 : annule +1 machine sinon Glisse 1G] |
| **Mots-clés Enraciné** | Enracinée sans fermer le Sommeil | — | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `POSITION_REVE`, `RANG_REVE` | `POSITION_REVE`, `RANG_REVE` | `POSITION_REVE`, `TAMBOUR`, `CHANT` |
| **Synergies (`I01`)** | — | — | `ALTERATION`, `ROUGE` |
| **Sorties (`I03`)** | `REVE_COMPACTE`, `POSITION_REVE`, `ANNULATION` | `RANG_REVE` | `DEFENSEUR_REDEPLOYE`, `RANG_REVE`, `ALTERATION`, `ANNULATION`, `BLEU` |

- **Panel 1 — La Liane des Esprits** *(🔓 A=0 · 🌙 Levier Rêve · 🌱 Enracinement · OUVERTURE)*
  - *Ambiance* : On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution, après ses annulations : la liane s’enroule. Choisissez un Rêve des Entités situé plus à droite sur la Réglette. S’il reste au moins un rang libre entre eux, faites glisser ce Rêve jusqu’au rang libre qui touche la Liane (ses Défenseurs le suivent). S’il touche déjà la Liane, elle l’entraîne : la Liane glisse d’1 rang vers la gauche si ce rang est libre, et ce Rêve glisse d’1 rang à sa suite. Un Rêve déplacé qui n’a pas encore été résolu se résout ensuite depuis sa nouvelle place.
  > La liane grimpe (plancher) : s’il n’y a aucun Rêve des Entités à sa droite, la Liane s’enroule sur elle-même : elle glisse d’1 rang vers la gauche si ce rang est libre (ses Défenseurs la suivent ; elle ne se résout pas une seconde fois). Si elle ne peut pas glisser (rang occupé, ou Liane déjà au rang 1), elle serre : elle annule 1 machine de plus sur son rang.
  - **Enraciné** :
  > La Liane nourrit encore les rêves : contrairement aux autres Rêves enracinés, elle ne rend pas le Sommeil impossible. Au décompte final, elle fait repousser 1 Souche comme toute tuile enracinée.
  - **Dilemme** — *Choix* : Tirer le Rêve des Entités pour combler un trou du bloc, ou faire glisser la paire vers le rang 1 ; seule, grimper vers le bloc ou serrer une machine de plus. · *Renoncement* : Le Rêve tiré abandonne le rang qu’il couvrait ; une Liane qui grimpe quitte un rang où des machines pourraient encore tomber ; enraciner la Liane lui retire ce pouvoir mais garde le Sommeil possible.
  - **Témoin `R1_T1`** : L’enroulement : Liane au rang 3 défendue, Rêve des Entités au rang 6, rangs 4 et 5 libres : le Rêve des Entités glisse au rang 4.

- **Panel 2 — La Nasse à contre-courant** *(🌙 Levier Rêve · ⚡ Twist 2K3 · 🔓 A=0 · OUVERTURE)*
  - *Ambiance* : La nasse cède d’une maille. Une brassée de rêves passe dans l’autre sens.
  - **Face 1** :
  > Au pouvoir de ce Rêve défendu, vous pouvez le reculer d’un rang libre vers la droite pour avancer d’un rang vers la gauche un bloc d’un ou deux autres Rêves contigus. Le bloc doit être entièrement à gauche du rang quitté et avoir une case libre à sa gauche. Déplacez d’abord la Nasse puis le bloc, en commençant par son Rêve le plus à gauche. Tous les Défenseurs suivent. Reprenez la lecture des Rêves à droite de la nouvelle case de la Nasse. Aucun Rêve déplacé ne se résout de nouveau.
  - **Dilemme** — *Choix* : Accepter un trou derrière le bloc pour gagner deux rangs à gauche ? · *Renoncement* : La Nasse recule elle-même. Il faudra encore la ramener pour obtenir le Sommeil.
  - **Témoin `R1_T1`** : Rêves en 3 et 4, Nasse défendue en 5, rangs 2 et 6 libres. La Nasse passe en 6, les deux Rêves passent en 2 et 3, avec leurs pions. Aucun ne se résout deux fois.

- **Panel 3 — Le Chant du Voyage Astral** *(🔓 A=0 · OUVERTURE)*
  - *Ambiance* : « Le corps demeure près des braises, mais le battement du tambour franchit trois vallées avant que la scie n'ait touché l'écorce. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :
  > 1. Voile d'Altération : posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore (ou, sur une machine mobile portant déjà une Altération et au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe).
  > 2. Danse du Tambour et du Chant : choisissez 1 seule des deux transes suivantes :
  > • Transe du Tambour : si le pion Tambour se trouve actuellement sur une parcelle de forêt ou sur un Rêve de la Réglette, déplacez-le immédiatement vers n'importe quelle parcelle de n'importe quel rayon du plateau ; sur 1 machine présente sur (ou ciblant) cette parcelle d'arrivée, retournez 1 jeton Rouge existant en Bleu Surchauffe (ou, si elle n'a aucun Rouge, est mobile et sans Altération, posez sur elle 1 jeton d'Altération).
  > • Transe du Chant : désignez le Rêve portant le pion Chant (ou ce Rêve R1 lui-même si le Chant n'occupe aucun Rêve). S'il reste au moins 1 machine active sur son rang, annulez 1 machine supplémentaire sur ce rang (inclinez son jeton à 90° ; si le pion Chant est sur ce Rêve et qu'aucune machine active n'y reste, le Chant déclenche aussitôt son glissement d'1 rang vers la gauche) ; sinon (si aucune machine active n'occupe ce rang et que ce Rêve n'a pas encore glissé à cette ouverture), faites glisser ce Rêve (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.
  - **Dilemme** — *Choix* : Choisir Transe du Tambour pour corriger à livres ouverts la position du Tambour (et déclencher R2), ou Transe du Chant pour annuler une seconde machine ou faire glisser un Rêve même sur un rang vide. · *Renoncement* : Redéployer le Tambour renonce à l'annulation supplémentaire ou au glissement gratuit du Chant, et inversement.
  - **Témoin `R1_T1`** : Tour 4 (table {H, E, I}), Tambour posé au 1er déploiement en parcelle 2 de I (où la machine recule par Altération) et Chant au 2nd déploiement sur R1 au rang 5 (rang vide). R1 pose 1 Altération (Voile d'Altération) puis tranche : Transe du Tambour téléporte le Tambour en parcelle 3 de E et retourne le Rouge du Bulldozer en Bleu, OU Transe du Chant glisse R1 du rang 5 au rang 3 libre.

#### Emplacement `R2` (`E>H` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Iara, mère des eaux** | **Le Fleuve sous la cendre** | **Le Pacte des Doubles Chamaniques** |
| **Rôles & Nature** | 🔓 A=0 · ⚖️ Loi passive · 🌙 Levier Rêve (`LOI_PASSIVE`) | 🔓 A=0 · 🌱 Enracinement (`ACTION`) | 🔓 A=0 · ⚖️ Loi passive (`LOI_PASSIVE`) |
| **Fenêtre / Icône** | PERMANENT | OUVERTURE | PERMANENT |
| **Pictogrammes** | ⚖️ `PIC_LOI_PASSIVE` · 🎶 `PIC_CHANT` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION` | 🪵 `PIC_SOUCHE` · 🌀 `PIC_ALTERATION` · 🥁 `PIC_TAMBOUR` · 🌱 `PIC_ENRACINEMENT` | ⚖️ `PIC_LOI_PASSIVE` · 🥁 `PIC_TAMBOUR` · 🌀 `PIC_ALTERATION` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Le Chant remonte le fleuve plus facilement | Tambour / Souches → Altération · ancrage marqué → Souche finale supplémentaire | Le Tambour reflète l'altération mystique |
| **Mots-clés Face 1** | Loi · le Chant fait glisser dès 1 machine annulée · restantes du rang = Altération | Lit sec · Marque | Passif : Défendu ou 🌙 annule (rayon 🥁/🔴) → 🌀 · Parade 🥁 → 🔴→🔵 (sinon 🌀) |
| **Mots-clés Enraciné** | — | Gué marqué · Final | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `CHANT`, `ANNULATION` | `POSITION_REVE`, `RANG_MACHINE` | `POSITION_REVE`, `TAMBOUR`, `RANG_MACHINE` |
| **Synergies (`I01`)** | — | `TAMBOUR`, `SOUCHE`, `DEFENSEUR_ATTENTE` | `ANNULATION`, `ROUGE` |
| **Sorties (`I03`)** | `GLISSEMENT_CHANT`, `ALTERATION` | `ALTERATION`, `DEFENSEUR_REDEPLOYE`, `ARBRE` | `ALTERATION`, `BLEU` |

- **Panel 1 — La Iara, mère des eaux** *(🔓 A=0 · ⚖️ Loi passive · 🌙 Levier Rêve · PERMANENT)*
  - *Ambiance* : Les pêcheurs qui entendent la Iara chanter ne rentrent pas au village. Mais pour qui la sert, son chant fait remonter les rêves vers leur source.
  - **Face 1** :
  > Loi passive — Le chant qui remonte le fleuve (tant que la Iara est sur la Réglette, défendue ou non) : un Rêve défendu par le Chant glisse d’1 rang vers la gauche, si ce rang est libre, dès qu’il annule au moins 1 machine, même si une autre machine reste active à son rang. Pouvoir de la Iara (quand elle est défendue, à sa résolution) : l’envoûtement : chaque machine mobile de son rang qui reste non annulée, faute de Défenseurs, reçoit 1 jeton d’Altération si elle n’en porte pas déjà.
  - **Dilemme** — *Choix* : Où poser le Chant : sur le Rêve qui annulera au moins une machine, même partiellement couvert, pour le faire remonter. · *Renoncement* : Un Rêve qui glisse en laissant une machine active la laisse frapper ; et défendre la Iara mobilise un Défenseur qui aurait pu garder la forêt.
  - **Témoin `R2_T1`** : Chant sur un Rêve H au rang 4 où tombent 2 machines ; il en annule 1 : grâce à la loi, le Rêve glisse au rang 3 bien qu’une machine reste active.

- **Panel 2 — Le Fleuve sous la cendre** *(🔓 A=0 · 🌱 Enracinement · OUVERTURE)*
  - *Ambiance* : Sous la cendre, l’eau se souvient du lit qu’elle occupait. Le premier arbre à boire lui rend son chemin.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez poser une Altération de la réserve sur une mobile sans Altération dans le rayon du Tambour en forêt, ou sur une mobile d’un rayon dont une parcelle ne porte que des Souches (à défaut, sur une mobile sans Altération de E ou H). Vous pouvez à la place relever le Tambour en attente sur un Rêve non défendu à droite de celui-ci. Il y participera à la résolution ordinaire.
  - **Enraciné** :
  > Gué marqué. À l’enracinement, si une machine mobile porte une Altération sur la parcelle désignée, vous pouvez tourner la Grande Carte d’un quart de tour, côté « Gué marqué » vers le haut. Ce repère conserve le droit au bonus, même après le départ de la machine. Le Sommeil se ferme dès l’ancrage. Au décompte final seulement, si la parcelle a survécu, retournez-y une Souche au titre de l’ancrage ordinaire, puis une autre si le gué est marqué. Chaque retournement exige une Souche encore présente.
  - **Dilemme** — *Choix* : Altérer une mobile grâce au Tambour ou aux Souches (ou sur E/H à défaut), relever le Tambour en attente sur un Rêve plus à droite, ou enraciner le Fleuve sur une parcelle altérée pour marquer le gué. · *Renoncement* : Enraciner le Fleuve sur le gué abandonne ses deux usages actifs et ferme définitivement la voie du Sommeil.
  - **Témoin `R2_T1`** : À l’ouverture, le Tambour est en E·1 ; R2 défendu altère une mobile en E·3. Au ménage du Tour 5, elle s’y trouve encore avec son Altération et deux Souches. E enracine R2 devant E·3 et tourne sa Grande Carte (les Souches restent face Souche pendant la bataille). Au décompte final, si les deux Souches survivent, les deux deviennent Arbres en E·3.

- **Panel 3 — Le Pacte des Doubles Chamaniques** *(🔓 A=0 · ⚖️ Loi passive · PERMANENT)*
  - *Ambiance* : « Chaque battement de peau tendue résonne des deux côtés du voile : là où l'homme tient bon, l'esprit retourne la fièvre du fer contre lui. »
  - **Face 1** :
  > Tant que ce Rêve occupe un rang de la Réglette (même sans Défenseur posé sur lui) :
  > • Double de Veille (À l'ouverture) : lorsque ce Rêve est défendu à sa résolution d'ouverture, OU chaque fois qu'un autre Rêve défendu annule au moins 1 machine qui appartient au rayon portant le Tambour Humain ou qui possède au moins 1 jeton Rouge, posez 1 jeton d'Altération de la réserve Entités sur une machine mobile de votre choix qui n'en porte pas encore.
  > • Double de Frappe (Aux attaques) : chaque fois qu'une frappe de machine est parée par des Défenseurs sur la parcelle portant le Tambour Humain : si cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe ; sinon (si elle ne porte aucun jeton Rouge), si elle est mobile et ne porte pas encore d'Altération, posez sur elle 1 jeton d'Altération de la réserve Entités.
  - **Dilemme** — *Choix* : Envoyer le Tambour dès le 1er déploiement sur le rayon le plus exposé pour maximiser à la fois Double de Veille à l'ouverture et Double de Frappe aux attaques. · *Renoncement* : Engager le Tambour au 1er déploiement avant l'ouverture des paravents le fige sur ce rayon si R1 n'est pas défendu pour le déplacer.
  - **Témoin `R2_T1`** : Tour 3 (table {H, E, I}), R2 non défendu au rang 6, autre Rêve défendu au rang 2, Tambour en parcelle 2 de H. Le Rêve du rang 2 annule l'Abatteuse de H (rayon du Tambour) → Double de Veille pose 1 Altération sur l'Abatteuse de I. Aux attaques, le Bulldozer de H (1 Rouge) est paré sur la parcelle du Tambour → Double de Frappe retourne son Rouge en Bleu.

---

<a id="lisiere-h-i-r6-m4"></a>
### Lisière `H ↔ I` — Humains ↔ Insectes (`R6` & `M4`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`R6`** (`H>I`, REVE) | **Le Rite de la Tucandeira** — L’Essaim multiplie les annulations du Rêve (🔓 A=0 · sortie `ANNULATION_RENFORCEE`) | **Le Chant des chambres creuses** — Tambour en forêt · montée au rang (🔓 A=0 · sortie `INSECTE_RANG`) | **Le Rêve des Mélipones d’Or** — Essaime le miel, danse déviante (🔓 A=0 · sortie `INSECTE_RANG`) |
| **`M4`** (`I>H`, CROISSANCE) | **Le Rucher des Mélipones** — Le miel relève les bâtisseurs (🔓 A=0 · sortie `DEFENSEUR_REDEPLOYE`) | **Le Nid des calebasses** — Convoi vers le Tambour / Essaimage (🌱 Enracinement · 🔓 A=0 · sortie `INSECTES_EN_CONVOI`) | **Le Jardin des Fourmis Sacrées, Clairière du Pacte Ancien** — Tresse pièges, fertilise la fin (🔓 A=0 · 🌱 Enracinement · sortie `PIEGE`) |

#### Emplacement `R6` (`H>I` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Rite de la Tucandeira** | **Le Chant des chambres creuses** | **Le Rêve des Mélipones d’Or** |
| **Rôles & Nature** | 🔓 A=0 (`ACTION`) | 🔓 A=0 (`ACTION`) | 🔓 A=0 (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | 🌙 `PIC_REVE` · 🐜 `PIC_INSECTE` · 🚫 `PIC_ANNULATION` | 🥁 `PIC_TAMBOUR` · 🐜 `PIC_INSECTE` · 🔢 `PIC_RANG_MACHINE` · 🌙 `PIC_REVE` | 🐜 `PIC_INSECTE` · 🔢 `PIC_RANG_MACHINE` · 🔵 `PIC_BLEU` · 🎶 `PIC_CHANT` |
| **Résumé Mini-Tuile** | L’Essaim multiplie les annulations du Rêve | Tambour en forêt · montée au rang | Essaime le miel, danse déviante |
| **Mots-clés Face 1** | 1 Insecte du rayon Humain → son rang (aucun en jeu : de la réserve) · chaque Insecte défaussé = 1 annulation de plus | Tambour en forêt · montée au rang | +2 🐜 (Réglette/🥁/🪹) + Décale 1 dé ±1 (🔴→🔵 si 🐜/🌙) + 🎶 libre → Glisse 1G |
| **Mots-clés Enraciné** | — | — | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `INSECTE`, `ANNULATION` | `TAMBOUR`, `INSECTE`, `RANG_MACHINE`, `POSITION_REVE` | `POSITION_REVE`, `RANG_MACHINE`, `TAMBOUR`, `CHANT` |
| **Synergies (`I01`)** | `INSECTE_RANG` | — | `NID`, `INSECTE_RANG`, `ROUGE` |
| **Sorties (`I03`)** | `ANNULATION_RENFORCEE`, `INSECTE_RANG` | `INSECTE_RANG` | `INSECTE_RANG`, `RANG_MACHINE`, `BLEU`, `RANG_REVE` |

- **Panel 1 — Le Rite de la Tucandeira** *(🔓 A=0 · OUVERTURE)*
  - *Ambiance* : Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution : la cueillette : vous pouvez d’abord déplacer 1 Insecte d’une parcelle du rayon Humain vers le rang de ce Rêve.
  > Amorçage — cueillette sauvage (plancher) : s’il n’y a encore aucun Insecte en jeu, prenez-le dans la réserve de l’Essaim.
  > Puis le gant de tucandeiras : en plus d’1 machine par Défenseur, ce Rêve annule 1 machine supplémentaire de son rang pour chaque Insecte que vous défaussez de ce rang.
  - **Dilemme** — *Choix* : Combien d’Insectes offrir au gant — un par machine qui resterait sinon active sur le rang. · *Renoncement* : Les Insectes consumés au rite ne dévieront plus de dés et ne pareront plus de frappes.
  - **Témoin `R6_T1`** : Rêve au rang 1 défendu par 1 Défenseur ; 3 machines au rang 1 et 2 Insectes sur ce rang : 3 machines annulées (1 + 2), 2 Insectes défaussés.

- **Panel 2 — Le Chant des chambres creuses** *(🔓 A=0 · OUVERTURE)*
  - *Ambiance* : Le Chamane approche l’oreille de la calebasse. Des pas minuscules y battent déjà le rappel.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, si le Tambour est en forêt, vous pouvez prendre un Insecte au sol sur sa parcelle et le poser sur le rang de ce Rêve ou sur celui d’une machine visible encore active. Si cette machine menace la parcelle du Tambour, vous pouvez aussi transporter un second Insecte de cette parcelle sur le même rang. La fenêtre de déviation de cette ouverture est déjà passée.
  - **Dilemme** — *Choix* : Parier sur le prochain tirage ou garder autour du Tambour de quoi parer aujourd’hui ? · *Renoncement* : Les ouvrières montées au rang manquent aux frappes imminentes.
  - **Témoin `R6_T1`** : Le Nid des calebasses a rassemblé trois ouvrières auprès du Tambour. Au tour suivant, le Chant en envoie deux sur 3, rang d’une machine qui vise le Tambour. Elles y attendent la prochaine ouverture.

- **Panel 3 — Le Rêve des Mélipones d’Or** *(🔓 A=0 · OUVERTURE)*
  - *Ambiance* : « La danse des abeilles sacrées ne se trompe jamais d'angle : un bourdonnement suffit à égarer le fer hors du sentier. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :
  > 1. Miel de Veille : prenez 2 jetons Insectes de la réserve et répartissez-les librement entre les rangs 1–6 de la Réglette, la parcelle portant le Tambour, et/ou une parcelle portant un Nid (si ni le Tambour ni aucun Nid ne sont en forêt, vous pouvez aussi les placer sur une parcelle du rayon Humain).
  > 2. Danse Frétillante : vous pouvez décaler le dé révélé d'1 machine encore active de −1 ou +1 rang sur la Réglette (entre 1 et 6) ; si ce dé rejoint un rang portant au moins 1 Insecte ou un Rêve défendu situé plus à droite (non encore résolu), et que cette machine possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe. Enfin, si un Rêve portant le pion Chant n'a pas encore glissé à cette ouverture et que son rang ne contient désormais plus aucune machine active, faites-le glisser immédiatement (avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche.
  - **Dilemme** — *Choix* : Répartir les 2 Insectes entre un Nid (pour franchir le seuil ≥ 2 avant la Production), le Tambour ou la Réglette ; puis choisir entre dégager le rang du Chant ou faire basculer une machine Rouge d'Assaut vers Charge. · *Renoncement* : Alimenter un Nid ou le Tambour renonce à garnir la Réglette pour les déviations futures et le refroidissement de Danse Frétillante.
  - **Témoin `R6_T1`** : Tour 3 (Acte 1), R6 défendu par le Chant au rang 4 face à 2 machines (Abatteuse + Bulldozer 2 Rouges). R6 annule l'Abatteuse, pose 1 Insecte sur M4 (passe à 2 avant Production) et 1 sur le rang 3, puis décale le Bulldozer de 4 → 3 (Charge, seuil −1, 1 Rouge → Bleu) ; le rang 4 étant vidé, le Chant fait glisser R6 à gauche.

#### Emplacement `M4` (`I>H` · CROISSANCE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Rucher des Mélipones** | **Le Nid des calebasses** | **Le Jardin des Fourmis Sacrées, Clairière du Pacte Ancien** |
| **Rôles & Nature** | 🔓 A=0 (`ACTION`) | 🌱 Enracinement · 🔓 A=0 (`ACTION`) | 🔓 A=0 · 🌱 Enracinement (`ACTION`) |
| **Fenêtre / Icône** | PRODUCTION | PRODUCTION | PRODUCTION |
| **Pictogrammes** | 🪹 `PIC_NID` · ♻️ `PIC_DEFENSEUR_ATTENTE` · 🥁 `PIC_TAMBOUR` · 🐜 `PIC_INSECTE` | 🪹 `PIC_NID` · 🥁 `PIC_TAMBOUR` · 🐜 `PIC_INSECTE` · 🌱 `PIC_ENRACINEMENT` | 🪤 `PIC_PIEGE` · 💥 `PIC_SABOTAGE` · 🔵 `PIC_BLEU` · 🌱 `PIC_ENRACINEMENT` |
| **Résumé Mini-Tuile** | Le miel relève les bâtisseurs | Convoi vers le Tambour / Essaimage | Tresse pièges, fertilise la fin |
| **Mots-clés Face 1** | 1 Insecte → 1 bâtisseur relevé sur le Nid ou le Tambour · deux fois au plus | Convoi vers le Tambour | [-1 🐜 → +1 🪤 (🪹/H/🥁) OU +1 💥 sac & 🔴→🔵] + Si 🥁/🎶 : +1 🐜 (Réglette/🪹) |
| **Mots-clés Enraciné** | — | Essaimage | Fin : +1 🪵 sur ≤ 2 parcelles (rayon H ou 🪤 / ≥ 2 🐜) |
| **Plancher (`M4`)** | `NID`, `INSECTE`, `DEFENSEUR_ATTENTE` | `NID_ACTIVE`, `INSECTE`, `TAMBOUR`, `ROUTE` | `NID_ACTIVE`, `INSECTE` |
| **Synergies (`I01`)** | `TAMBOUR` | — | `TAMBOUR`, `CHANT`, `ROUGE`, `SOUCHE` |
| **Sorties (`I03`)** | `DEFENSEUR_REDEPLOYE`, `INSECTE` | `INSECTES_EN_CONVOI`, `INSECTE_RANG` | `PIEGE`, `SABOTAGE`, `BLEU`, `INSECTE_RANG`, `ARBRE` |

- **Panel 1 — Le Rucher des Mélipones** *(🔓 A=0 · PRODUCTION)*
  - *Ambiance* : Les mélipones n’ont pas de dard ; elles offrent leur miel aux peuples qui les protègent depuis des siècles. Une gorgée, et ceux qui ont bâti jusqu’à l’épuisement se relèvent pour défendre la forêt.
  - **Face 1** :
  > Production (quand ce Nid est défendu, après avoir produit) : le miel des mélipones : défaussez 1 Insecte de ce Nid pour relever 1 Défenseur couché en attente (bâtisseur d’une tuile construite à ce tour) : son propriétaire le pose aussitôt, face Définitif, sur la parcelle de ce Nid ou sur la parcelle qui porte le Tambour, où il compte pour les parades. Vous pouvez recommencer une seconde fois en défaussant 1 autre Insecte.
  - **Dilemme** — *Choix* : Relever un bâtisseur (souvent celui qui vient d’achever une tuile) pour défendre le Nid ou la parcelle du Tambour. · *Renoncement* : Chaque gorgée coûte un Insecte qui ne déviera ni ne parera ; et il faut avoir construit à ce tour pour avoir un bâtisseur à relever.
  - **Témoin `M4_T1`** : Un Rêve vient d’être construit par 2 bâtisseurs couchés ; Production du Rucher défendu : 1 Insecte défaussé, 1 bâtisseur posé sur la parcelle du Tambour.

- **Panel 2 — Le Nid des calebasses** *(🌱 Enracinement · 🔓 A=0 · PRODUCTION)*
  - *Ambiance* : Quand le Tambour résonne, la courge vide vibre jusque dans les chambres où repose le couvain.
  - **Face 1** :
  > Après la production de ce Nid défendu, si le Tambour occupe une autre parcelle du même rayon, vous pouvez y conduire autant d’Insectes du Nid que vous le souhaitez. Le convoi suit le rayon, en sautant les Routes, avant la Migration.
  - **Enraciné** :
  > Quand vous enracinez ce Nid, laissez ses Insectes sur leur parcelle. Vous pouvez ensuite donner à un de ces Insectes au sol un pas radial vers le cœur, Routes sautées, ou le poser sur un rang librement choisi s’il est déjà sur la dernière parcelle.
  - **Dilemme** — *Choix* : Combien d’ouvrières confier au Tambour ? · *Renoncement* : Au-dessous de deux ouvrières restantes, la prochaine Production tombe à une.
  - **Témoin `M4_T1`** : Quatre ouvrières après Production en H2. Deux gagnent le Tambour en H4 en sautant la Route H3. Deux restent au Nid et permettront une nouvelle ponte de deux.

- **Panel 3 — Le Jardin des Fourmis Sacrées, Clairière du Pacte Ancien** *(🔓 A=0 · 🌱 Enracinement · PRODUCTION)*
  - *Ambiance* : « Autour du jardin sacré, les lianes mordent d'acide ; dessous, la terre noire des ancêtres attend l'heure de relever la futaie. »
  - **Face 1** :
  > À l'étape de Production des Nids, immédiatement après que ce Nid défendu a produit ses Insectes (+1 ou +2, avant la Migration) :
  > 1. Lianes Formiques : choisissez 1 seule des deux options suivantes :
  > • Fosse de Lianes : défaussez 1 Insecte présent sur la parcelle de ce Nid (ou sur la parcelle portant le Tambour) pour poser immédiatement 1 Piège ordinaire sur une parcelle dépourvue de Piège ordinaire appartenant au rayon de ce Nid, au rayon Humain, ou au rayon portant le Tambour.
  > • Cendre de Bivouac : glissez 1 jeton Sabotage ordinaire dans le sac opaque, ET sur 1 machine située sur le rayon de ce Nid ou sur le rayon portant le Tambour qui possède au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
  > 2. Harmonie du Chant : si le pion Tambour occupe la parcelle de ce Nid — OU si le pion Chant occupe actuellement un Rêve sur la Réglette — posez +1 jeton Insecte de la réserve directement sur un rang 1–6 de la Réglette ou sur la parcelle de ce Nid.
  - **Enraciné** :
  > Terre Noire des Ancêtres (Décompte final uniquement). Au décompte final (quelle que soit l'issue qui met fin à la partie), tant que la parcelle d'ancrage de cette tuile n'est pas devenue une Route Forestière, en plus de la 1 Souche retournée en Arbre debout sur sa parcelle d'ancrage, retournez jusqu'à 2 Souches survivantes supplémentaires en Arbres debout, choisies sur des parcelles distinctes appartenant au rayon Humain et/ou contenant au moins 1 Piège ordinaire ou au moins 2 Insectes (max 1 Souche supplémentaire par parcelle ainsi choisie).
  - **Dilemme** — *Choix* : Sacrifier 1 Insecte pour poser un Piège autonome par Fosse de Lianes, ou diluer le sac et refroidir une machine par Cendre de Bivouac ; enraciner M4 sans bloquer le Sommeil pour régénérer jusqu'à 3 Souches au décompte final. · *Renoncement* : Enraciner M4 renonce définitivement à sa fabrique de Pièges et de Sabotages ; Fosse de Lianes consomme 1 Insecte qui peut faire redescendre le Nid sous 2 Insectes.
  - **Témoin `M4_T1`** : Tour 6 (table {H, E, I} visant le Sommeil), M4 en parcelle 1 de I (2 Insectes, défendu), Chant sur un Rêve : produit +2 (4), dépense 1 Insecte pour 1 Piège en H·3 (Fosse de Lianes) et regagne +1 Insecte (Harmonie du Chant). Enraciné au ménage du Tour 6 sans bloquer le Sommeil, il retourne 3 Souches en Arbres debout au décompte final du Tour 7.

---

<a id="lisiere-e-i-r10-m5"></a>
### Lisière `E ↔ I` — Entités Magiques ↔ Insectes (`R10` & `M5`)

| Emplacement | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **`R10`** (`E>I`, REVE) | **La Mère des Lucioles** — Les rangs vides deviennent des lanternes (🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve · sortie `LANTERNE`) | **Les Lanternes englouties** — Lanterne du rang · plongée (🌙 Levier Rêve · 🔓 A=0 · sortie `RANG_REVE`) | **La Transe de la Ruche Vagabonde** — Glisse rêve, déménage une ruche (🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve · sortie `RANG_REVE`) |
| **`M5`** (`I>E`, CROISSANCE) | **Le Jardin du Diable** — Une clairière que nulle Route n’efface (🔓 A=0 · ⚖️ Loi passive · sortie `SOUCHE_SANCTUARISEE`) | **Le Nid des reflets** — Reflet droit · reflet incliné (🔓 A=0 · sortie `INSECTE_RANG`) | **Le Mycélium Luminescent, Réseau Spectral des Racines Noires** — Déviations vers rêves altèrent, recyclent (🔓 A=0 · ⚖️ Loi passive · sortie `ALTERATION`) |

#### Emplacement `R10` (`E>I` · REVE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **La Mère des Lucioles** | **Les Lanternes englouties** | **La Transe de la Ruche Vagabonde** |
| **Rôles & Nature** | 🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve (`ACTION`) | 🌙 Levier Rêve · 🔓 A=0 (`ACTION`) | 🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve (`ACTION`) |
| **Fenêtre / Icône** | OUVERTURE | OUVERTURE | OUVERTURE |
| **Pictogrammes** | ⚡ `PIC_TWIST` · 🐜 `PIC_INSECTE` · 🚫 `PIC_ANNULATION` · ⬅️ `PIC_AVANCEE_REVE` | 🐜 `PIC_INSECTE` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION` | ⬅️ `PIC_AVANCEE_REVE` · 🪹 `PIC_NID` · 🌀 `PIC_ALTERATION` · 🔵 `PIC_BLEU` |
| **Résumé Mini-Tuile** | Les rangs vides deviennent des lanternes | Lanterne du rang · plongée | Glisse rêve, déménage une ruche |
| **Mots-clés Face 1** | Rang libre avec Insecte = lanterne · aucun en jeu : 1 luciole de la réserve · 1 Insecte défaussé annule 1 machine · puis glisse d’1 rang | Lanterne du rang · plongée | Glisse 1G + [Déplace 1 🪹 (+🐜 & 🛡️) partout & 🌀/🔴→🔵 OU +1 🐜 & +1 🌀] |
| **Mots-clés Enraciné** | — | — | Standard (1 Souche finale, bloque Sommeil) |
| **Plancher (`M4`)** | `INSECTE`, `RANG_MACHINE` | `INSECTE_RANG`, `INSECTE`, `POSITION_REVE`, `RANG_MACHINE` | `POSITION_REVE`, `RANG_MACHINE` |
| **Synergies (`I01`)** | `INSECTE_RANG` | — | `NID`, `INSECTE`, `ROUGE` |
| **Sorties (`I03`)** | `LANTERNE`, `ANNULATION`, `POSITION_REVE` | `RANG_REVE`, `ALTERATION`, `INSECTE_IMMERGE` | `RANG_REVE`, `NID_DEPLACE`, `ALTERATION`, `INSECTE`, `BLEU` |

- **Panel 1 — La Mère des Lucioles** *(🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : Là où aucun rêve ne veille, la Mère des Lucioles allume ses lanternes. Les égarés suivent ces lumières et rentrent chez eux ; les machines, elles, s’arrêtent, aveuglées, au milieu du chemin.
  - **Face 1** :
  > Quand ce Rêve est défendu, à sa résolution : les lanternes s’allument.
  > Amorçage — première luciole (plancher) : s’il n’y a encore aucun Insecte en jeu, posez d’abord 1 Insecte de la réserve de l’Essaim sur un rang de la Réglette libre de tout Rêve.
  > Chaque rang laissé libre de tout Rêve et portant au moins 1 Insecte devient une lanterne : pour chaque machine révélée et non annulée sur un tel rang, vous pouvez défausser 1 Insecte de ce rang pour l’annuler (inclinez son jeton). Ces annulations comptent comme celles de ce Rêve. Le chemin de lumière : si au moins une lanterne a annulé une machine, ce Rêve glisse ensuite d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent), au risque d’éteindre la lanterne qui s’y trouvait.
  - **Dilemme** — *Choix* : Laisser volontairement des rangs libres de tout Rêve pour y allumer des lanternes, ou compacter les Rêves vers le Sommeil. · *Renoncement* : Chaque rang occupé par un Rêve éteint une lanterne ; chaque Insecte consumé ne déviera plus de dé.
  - **Témoin `R10_T1`** : Mère des Lucioles défendue au rang 5 ; le rang 1, libre, porte 2 Insectes et reçoit 2 machines : 2 annulations par la lanterne, puis le Rêve glisse au rang 4.

- **Panel 2 — Les Lanternes englouties** *(🌙 Levier Rêve · 🔓 A=0 · OUVERTURE)*
  - *Ambiance* : Une lumière s’éteint à la surface. Sous les racines, le cortège gagne une longueur de pirogue.
  - **Face 1** :
  > À l’ouverture, après les annulations de ce Rêve défendu, vous pouvez retirer un Insecte du rang de ce Rêve pour avancer celui-ci d’un rang libre vers la gauche avec ses Défenseurs. Posez cet Insecte au sol sur une parcelle de E ou I portant une machine mobile. S’il y rejoint un autre Insecte au sol, vous pouvez poser une Altération de la réserve sur une mobile de cette parcelle qui n’en porte pas. Le mouvement exige les deux destinations légales.
  - **Dilemme** — *Choix* : Garder l’Insecte pour dévier ou le faire plonger à l’endroit d’une future frappe ? · *Renoncement* : La Réglette perd son aiguilleur pour gagner un rang de Sommeil.
  - **Témoin `R10_T1`** : Le Nid des reflets a garni le rang 4. Les Lanternes en 4 passent en 3 libre. L’ouvrière rejoint une autre en E2 et les Entités y altèrent l’Abatteuse mobile.

- **Panel 3 — La Transe de la Ruche Vagabonde** *(🔓 A=0 · ⚡ Twist 2K3 · 🌙 Levier Rêve · OUVERTURE)*
  - *Ambiance* : « Guidé par le songe, le nid décroche ses racines d'écorce et traverse la nuit : quand l'acier frappe la clairière, la ruche est déjà derrière lui. »
  - **Face 1** :
  > À l'ouverture des paravents, lorsque ce Rêve est défendu (après avoir résolu ses éventuelles annulations de machines sur son rang) :
  > 1. Sillage Onirique : faites glisser 1 Rêve en jeu de votre choix (ce Rêve ou un autre, avec ses Défenseurs solidaires) sur le premier rang libre situé à sa gauche (vers le rang 1).
  > 2. Transhumance de la Ruche (Twist spatial) : choisissez 1 seul des deux effets suivants :
  > • Envol de la Ruche (si au moins 1 Nid est en forêt) : déplacez 1 Nid construit — en emportant simultanément avec lui tous les Insectes et tous les Défenseurs présents sur sa parcelle — vers n'importe quelle autre parcelle dépourvue d'autre Nid sur n'importe quel rayon du plateau (y compris hors des rayons voisins des Insectes, et y compris sur une parcelle occupée par une machine). Ensuite, posez 1 jeton d'Altération de la réserve Entités sur une machine mobile sans Altération du rayon rejoint — ou, sur une machine occupant la parcelle rejointe et possédant au moins 1 jeton Rouge, retournez 1 de ses jetons Rouges sur sa face Bleue Surchauffe.
  > • Essaim Spectral (toujours disponible, y compris si aucun Nid n'est en forêt) : posez 1 jeton Insecte de la réserve sur une parcelle du rayon Entités ou du rayon Insectes (ou sur un rang 1–6 de la Réglette), ET posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
  - **Dilemme** — *Choix* : Téléporter un Nid défendu et toute sa garnison directement devant une machine lointaine pour produire sur place à la Production puis parer aux attaques, ou choisir Essaim Spectral en solo. · *Renoncement* : Déménager le Nid abandonne son ancien secteur et expose le Nid au renvoi en lisière si un Bulldozer transforme la parcelle rejointe en Route Forestière.
  - **Témoin `R10_T1`** : Tour 4 (table {H, E, I}), M5 en parcelle 1 de I (1 Défenseur, 2 Insectes) tandis qu'un Bulldozer (1 Rouge, seuil 4) menace la parcelle 4 de H. R10 glisse du rang 3 au rang 2 libre puis choisit Envol de la Ruche : M5 atterrit en H·4 avec son Défenseur et ses 2 Insectes, retourne le Rouge en Bleu (seuil 4 → 2), produit +2 Insectes à la Production et pare aisément aux attaques.

#### Emplacement `M5` (`I>E` · CROISSANCE)

| Attribut | Panel 1 | Panel 2 | Panel 3 |
|---|---|---|---|
| **Titre complet** | **Le Jardin du Diable** | **Le Nid des reflets** | **Le Mycélium Luminescent, Réseau Spectral des Racines Noires** |
| **Rôles & Nature** | 🔓 A=0 · ⚖️ Loi passive (`LOI_PASSIVE`) | 🔓 A=0 (`ACTION`) | 🔓 A=0 · ⚖️ Loi passive (`LOI_PASSIVE`) |
| **Fenêtre / Icône** | PERMANENT | PRODUCTION | PERMANENT |
| **Pictogrammes** | ⚖️ `PIC_LOI_PASSIVE` · 🪵 `PIC_SOUCHE` · 🛣️ `PIC_ROUTE` · 🐜 `PIC_INSECTE` | 🪹 `PIC_NID` · 🔢 `PIC_RANG_MACHINE` · 🐜 `PIC_INSECTE` · 🚫 `PIC_ANNULATION` | ⚖️ `PIC_LOI_PASSIVE` · 🌙 `PIC_REVE` · 🌀 `PIC_ALTERATION` · 🐜 `PIC_INSECTE` |
| **Résumé Mini-Tuile** | Une clairière que nulle Route n’efface | Reflet droit · reflet incliné | Déviations vers rêves altèrent, recyclent |
| **Mots-clés Face 1** | Loi · jamais de Route ici · le Bulldozer n’y retire aucune Souche · 2 Insectes vers un rang libre | Reflet droit · reflet incliné | Passif : Déviation ±1 vers 🌙 → +1 🌀 & recycle 🐜 sur M5 (si <2) · Production → 1 🐜 vers Réglette OU +1 🌀 |
| **Mots-clés Enraciné** | — | — | Standard (1 Souche finale) |
| **Plancher (`M4`)** | `NID`, `INSECTE`, `SOUCHE` | `NID_ACTIVE`, `INSECTE`, `RANG_MACHINE` | `NID_ACTIVE`, `INSECTE` |
| **Synergies (`I01`)** | — | `ANNULATION` | `INSECTE_RANG`, `POSITION_REVE` |
| **Sorties (`I03`)** | `SOUCHE_SANCTUARISEE`, `INSECTE_RANG` | `INSECTE_RANG` | `ALTERATION`, `INSECTE_RANG`, `INSECTE` |

- **Panel 1 — Le Jardin du Diable** *(🔓 A=0 · ⚖️ Loi passive · PERMANENT)*
  - *Ambiance* : Les habitants l’appellent le jardin du diable : rien n’y pousse que ce que les fourmis tolèrent, et l’on dit qu’un esprit de la forêt y cultive ses arbres. Ni les hommes ni leurs machines n’osent y arracher les souches.
  - **Face 1** :
  > Loi passive (tant que ce Nid est sur sa parcelle) : la parcelle du Jardin ne peut jamais devenir une Route Forestière : un Bulldozer qui y frappe sans être paré retourne 1 Arbre debout en Souche mais n’y retire aucune Souche ; une Abatteuse y frappe normalement. Les sentinelles du Jardin (à la Production, quand ce Nid est défendu, après avoir produit) : jusqu’à 2 Insectes de ce Nid peuvent migrer directement vers un rang de la Réglette laissé libre de tout Rêve.
  - **Dilemme** — *Choix* : Sur quelle parcelle bâtir le Jardin : la plus menacée de devenir Route (elle devient indestructible) ou celle d’où l’Essaim rejoint le plus vite la Réglette. · *Renoncement* : Le Jardin protège ses Souches, pas ses Arbres : l’Abatteuse y frappe toujours ; et chaque Insecte envoyé sur la Réglette quitte la défense de la forêt.
  - **Témoin `M5_T1`** : Jardin sur la parcelle 2 (1 Arbre, 0 Souche) ; un Bulldozer non paré frappe : 0 Arbre, 1 Souche ; aucune Route ; le Nid reste en place.

- **Panel 2 — Le Nid des reflets** *(🔓 A=0 · PRODUCTION)*
  - *Ambiance* : Sous le nid de papier, chaque remous porte deux images. Les ouvrières suivent celle qui tremble encore.
  - **Face 1** :
  > Après la production de ce Nid défendu, choisissez un jeton Machine révélé du rayon du Nid. Posez un Insecte du Nid sur le rang de son dé. Si le jeton est incliné par une annulation, vous pouvez choisir à la place un rang voisin de ce dé, entre 1 et 6. Gardez les jetons visibles avec leur orientation et leurs dés de machine jusqu’à cette lecture. Utilisez le rang après toute déviation. Un jeton de Ratissage sous sa machine ne donne pas de départ.
  - **Dilemme** — *Choix* : Lire la menace visible ou exploiter le reflet d’une machine annulée ? · *Renoncement* : La cohorte investie dans la Réglette ne pare plus sur la parcelle du Nid.
  - **Témoin `M5_T1`** : Le Rêve a incliné le jeton d’une machine déviée en 5. Après Production, le Nid choisit le rang 4 voisin. Cette ouvrière pourra payer la plongée des Lanternes en 4 à une prochaine ouverture.

- **Panel 3 — Le Mycélium Luminescent, Réseau Spectral des Racines Noires** *(🔓 A=0 · ⚖️ Loi passive · PERMANENT)*
  - *Ambiance* : « Ce que l'insecte touche là-haut résonne aussitôt sous l'humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé. »
  - **Face 1** :
  > Tant que ce Nid est en forêt (même sans Défenseur posé sur lui — et en plus de sa production standard +1 ou +2 lorsqu'il est défendu) :
  > • Spores de Déviation (À l'ouverture) : chaque fois qu'un Insecte posé sur la Réglette est défaussé à l'ouverture pour décaler le dé d'une machine (±1) vers un rang portant un Rêve (défendu ou non), posez immédiatement 1 jeton d'Altération de la réserve Entités sur cette machine mobile si elle n'en porte pas encore (elle peut ensuite être annulée normalement si ce Rêve est défendu) ; de plus, si la parcelle de ce Nid contient alors strictement moins de 2 Insectes, replacez cet Insecte sur la parcelle de ce Nid au lieu de le remettre en réserve.
  > • Filaments Oniriques (À la Production des Nids) : lorsque ce Nid est défendu à l'étape de Production, après sa production standard (+1 ou +2, avant la Migration), choisissez 1 effet : transférez directement 1 Insecte présent sur sa parcelle vers le rang 1–6 de votre choix de la Réglette, OU posez 1 jeton d'Altération de la réserve Entités sur une machine mobile qui n'en porte pas encore.
  - **Dilemme** — *Choix* : Expédier 1 Insecte sur la Réglette à la Production pour amorcer la boucle Spores de Déviation (en restant sous 2 Insectes pour recycler gratuitement l'ouvrière), ou poser immédiatement 1 Altération directe. · *Renoncement* : Rester sous 2 Insectes sur M5 maintient sa production à +1 au lieu de +2 ; dévier une machine vers un Rêve non défendu lui inflige une Altération mais ne l'annule pas à ce tour.
  - **Témoin `M5_T1`** : Tour 3, M5 défendu (0 Insecte) produit +1 et envoie cet Insecte sur le rang 4 via Filaments Oniriques (M5 revient à 0). À l'ouverture du Tour 4, I dévie une Abatteuse du rang 4 vers le Rêve du rang 3 : Spores de Déviation pose 1 Altération sur l'Abatteuse et replace l'Insecte sur M5 (< 2 Insectes), puis le Rêve défendu annule l'Abatteuse à ce tour.

---

## 3. Grille d’arbitrage Étape 2b (30 emplacements)

| Emplacement | Lisière | Panel 1 | Panel 2 | Panel 3 | Arbitrage retenu |
|---|---|---|---|---|---|
| **`G1`** (`M>R`) | `M ↔ R` | Le Jaguar, seigneur des berges | Le Jaguar | Le Jaguar, Souverain des Berges | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G2`** (`R>M`) | `M ↔ R` | L’Anaconda vert, l’étau des eaux dormantes | L’Anaconda vert | L’Anaconda vert, Souffle Glacé de l’Igapó | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G3`** (`M>O`) | `M ↔ O` | L’Atèle, funambule de la canopée | L’Atèle | L’Atèle, Acrobate des Hautes Voûtes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G4`** (`O>M`) | `M ↔ O` | L’Ara rouge, sentinelle de la collpa | L’Ara rouge | L’Ara rouge, Vigie Écarlate de la Collpa | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G5`** (`R>O`) | `R ↔ O` | L’Iguane vert, dormeur des hautes branches | L’Iguane vert | L’Iguane vert, Guetteur Solaire des Cimes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G6`** (`O>R`) | `R ↔ O` | Le Toucan toco, le bec-radiateur | Le Toucan toco | Le Toucan toco, Contrebandier du Kapokier | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G7`** (`M>H`) | `M ↔ H` | Le Tapir, jardinier des sentiers | Le Tapir | Le Tapir, Ouvreur des Sentiers Profonds | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R3`** (`H>M`) | `M ↔ H` | La Vision du Chamane-Jaguar | Les Pas dans l’eau | L’Appel du Singe Hurleur | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G8`** (`M>E`) | `M ↔ E` | Le Boto, l’encantado du fleuve | Le Boto | Le Boto, Enchanteur des Eaux Roses | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R7`** (`E>M`) | `M ↔ E` | Le Curupira, protecteur aux pieds retournés | La Pirogue sans rameur | Le Songe du Brame des Brumes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G9`** (`R>H`) | `R ↔ H` | Le Caïman noir, l’ombre sous la pirogue | Le Caïman noir | Le Caïman noir, Maître des Eaux Noires | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R4`** (`H>R`) | `R ↔ H` | La Pirogue-Anaconda des Ancêtres | Le Tambour des deux berges | Le Songe de la Carapace de Limon | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G10`** (`R>E`) | `R ↔ E` | La Matamata, la souche qui respire | La Matamata | La Matamata, Guetteuse des Feuilles Mortes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R8`** (`E>R`) | `R ↔ E` | Le Boitatá, serpent de feu | La Peau du fleuve | Le Rêve de la Mue d’Obsidienne | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G11`** (`O>H`) | `O ↔ H` | La Harpie féroce, reine des hautes cimes | La Harpie féroce | La Harpie féroce, Souveraine des Grands Fromagers | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R5`** (`H>O`) | `O ↔ H` | Le Vol du Chamane-Oiseau | Le Ciel à deux eaux | La Vision du Condor des Brumes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G12`** (`O>E`) | `O ↔ E` | L’Ibijau, les yeux fendus de la nuit | L’Ibijau | L’Ibijau, Veilleur Fantôme des Souches Grises | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R9`** (`E>O`) | `O ↔ E` | La Matinta Pereira, siffleuse de minuit | Le Ciel sous l’écorce | Le Rêve de l’Éclipse de Plumes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G13`** (`M>I`) | `M ↔ I` | Le Tamanoir, le grand mangeur qui épargne | Le Tamanoir | Le Tamanoir, Sentinelle à Crinière des Fourmilières | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`M1`** (`I>M`) | `M ↔ I` | Le Pelage du Paresseux | Le Nid de la contre-sape | Le Bivouac des Légionnaires, Marée Noire des Sous-Bois | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G14`** (`R>I`) | `R ↔ I` | Le Téju, la ponte au cœur de la termitière | Le Téju | Le Téju, Maraudeur Doré des Termitières | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`M2`** (`I>R`) | `R ↔ I` | La Termitière-Forteresse | Le Nid des fours d’argile | La Termitière Cuirassée, Bastion d’Argile et d’Écailles | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`G15`** (`O>I`) | `O ↔ I` | Le Colibri, porteur de gouttes et de pollen | Le Colibri | Le Colibri, Joyau Émeraude des Cimes | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`M3`** (`I>O`) | `O ↔ I` | Le Bivouac des Légionnaires | Le Nid des feuilles cousues | Le Nid Tisserand des Cimes, Hamac de Soie des Hauts Vents | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R1`** (`H>E`) | `H ↔ E` | La Liane des Esprits | La Nasse à contre-courant | Le Chant du Voyage Astral | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R2`** (`E>H`) | `H ↔ E` | La Iara, mère des eaux | Le Fleuve sous la cendre | Le Pacte des Doubles Chamaniques | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R6`** (`H>I`) | `H ↔ I` | Le Rite de la Tucandeira | Le Chant des chambres creuses | Le Rêve des Mélipones d’Or | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`M4`** (`I>H`) | `H ↔ I` | Le Rucher des Mélipones | Le Nid des calebasses | Le Jardin des Fourmis Sacrées, Clairière du Pacte Ancien | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`R10`** (`E>I`) | `E ↔ I` | La Mère des Lucioles | Les Lanternes englouties | La Transe de la Ruche Vagabonde | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
| **`M5`** (`I>E`) | `E ↔ I` | Le Jardin du Diable | Le Nid des reflets | Le Mycélium Luminescent, Réseau Spectral des Racines Noires | ☐ P1 / ☐ P2 / ☐ P3 / ☐ Hybride |
