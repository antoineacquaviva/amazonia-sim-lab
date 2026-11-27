# Catalogue Canonique `v6.4` — Passe 2 Affinée (30 Tuiles Bi-Composant)

**Projet :** *Amazonia : Dernier Rempart*  
**Contrat SSOT :** `contracts/tiles_canon_v6_4.json` (`schema_version = 6.4.0`, `statut_global = PANEL_30_AFFINE`)  
**Cœur associé :** `contracts/rules_canon_v6_4.json` & `contracts/physical_and_edge_invariants_v6_4.json`  
**Audit 197 assises :** **`OK`** (`0` erreur — `M1..M4 = OK`, `I01..I07 = OK`, `Q01..Q02 = OK`, zéro contrainte `C02`)  

## Synthèse de la Carte des Rôles (`v6.4`)

- **Catalyseurs d’Éveil (`13`) :** G1=M>R, G3=M>O, G4=O>M, G5=R>O, G6=O>R, G8=M>E, G9=R>H, G10=R>E, G11=O>H, G12=O>E, G13=M>I, G14=R>I, G15=O>I
- **Leviers de Rêve (`6`) :** G8=M>E, R1=H>E, R4=H>R, R8=E>R, R9=E>O, R10=E>I
- **Synergies d’Enracinement (`4`) :** G7=M>H, G15=O>I, R1=H>E, R2=E>H
- **Lois passives (`3`, max `2`/assise) :** R7=E>M, R8=E>R, M5=I>E
- **Autonomes `A = 0` (`6`) :** R1=H>E, R2=E>H, R6=H>I, R10=E>I, M4=I>H, M5=I>E
- **Briques-Twists `2K3` (`6`) :** G2=R>M, G7=M>H, G12=O>E, R4=H>R, R10=E>I, M3=I>O

## Rappel des 6 Verbes du Cœur (`v6.4`)

1. **Refroidir** : `1 Rouge existant → Bleu Surchauffe` (`M2` : zéro Bleu à sec).
2. **Altérer** : `+1 Altération` (réserve `E`) sur une machine mobile sans Altération.
3. **Reculer** : `−1` parcelle vers la bordure sur une machine mobile (saute les Routes).
4. **Étouffer** : neutralise toute l’activation restante (jeton à `90°` + dé retiré, ou Ratissage tourné à `90°`). Le mot **cale** est exclusif au *Caïman noir*.
5. **Semer au sac** : glisse `1` jeton disponible (Sabotage ou Écaille) dans le sac opaque sans allumer d’icône.
6. **Glisser un Rêve** : déplace un Rêve sur la Réglette `1–6` avec ses Défenseurs dans leur état actuel (debout/couchés).

---

## Gardiens — 15 Tuiles (Casting animalier verrouillé)

### G1 (`M>R`) — Le Jaguar, seigneur des berges

- **Lisière :** Mammifères → Reptiles | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Piégeage
- **Mini-Tuile (`Le Jaguar`) :** *Poste le Croc aux côtés du Duel* | 🦷 `PIC_CROC` · ⚔️ `PIC_DUEL` · 🔵 `PIC_BLEU`
  - **Mots-clés Face 1 :** `Croc → parcelle du Duel · sinon Duel sur parcelle ciblée puis Croc dessus`
  - **Mots-clés Face 2 :** `Croc (+ Duel) → toute parcelle ciblée · parade du Croc = Refroidir 1 Rouge`
- **Vecteurs :** Duel (M) + Croc (R) → embuscade sur la parcelle du Duel → Piégeage en cascade · Face 2 : Refroidit la machine parée
- **Ambiance :** *Le Jaguar ne craint ni l’eau ni les écailles : il chasse le caïman sur sa propre berge et le tue d’une seule morsure au crâne. Là où il rôde, la rive appartient de nouveau à la forêt.*
- **Face 1 :** Prenez le Croc où qu’il se trouve (réserve Reptile ou plateau) et posez-le sur la parcelle du jeton Duel. Si le Duel est en réserve, posez d’abord le Duel face Défi sur une parcelle ciblée de votre choix, puis posez le Croc dessus.
- **Face 2 :** Même effet, mais vous pouvez poser le Croc — et, au choix, déplacer le Duel avec lui en conservant sa face — sur n’importe quelle parcelle ciblée du plateau. Chaque fois que le Croc pare une attaque à ce tour, Refroidissez cette machine si elle porte au moins 1 jeton Rouge.
- **Décision :** Poste le Croc sur la parcelle du Duel (ou sur toute cible en Face 2) et Refroidit l’attaquante. *(Renoncement : Mobilise l’unique Croc sur une seule parcelle ; le Croc n’est plus libre pour les pontes ou une autre embuscade tant qu’il n’a pas paré.)*
- **Double ouverture :** Première activation : le Croc se poste sur la parcelle du Duel ; sa parade allume Piégeage (l’icône du Jaguar) et retourne le Duel sur Territoire tenu (règle native), ouvrant une seconde activation qui reposte aussitôt le Croc pour la frappe suivante.
- **Entrées plancher :** `DUEL, CROC` | **Synergies :** `ROUGE` | **Sorties :** `CROC_POSTE, CROC, TERRITOIRE, BLEU`
- **Heuristique bot :** Prioritaire dès qu’une parcelle ciblée porte le Duel ou une attaque à fort Seuil ; en Face 2, combine Piégeage en boucle et Refroidissement sur machine chargée.
  - **Témoin `G1_T1` (`A_CODER`) :** Duel face Défi sur M·2 ; Jaguar F1 pose le Croc (pris en réserve Reptile) sur M·2 ; la frappe parée par le Croc allume Piégeage et retourne nativement le Duel sur Territoire tenu.
  - **Témoin `G1_T2` (`A_CODER`) :** Jaguar F2 déplace Duel + Croc sur une parcelle ciblée d’un rayon voisin ; la machine parée par le Croc est immédiatement Refroidie (1 Rouge → Bleu).

### G2 (`R>M`) — L’Anaconda vert, l’étau des eaux dormantes

- **Lisière :** Reptiles → Mammifères | **Nature :** `ACTION` | **Rôles :** TWIST_2K3 | **Icône conseillée :** Parade
- **Mini-Tuile (`L’Anaconda vert`) :** *Arrache une machine à son Ratissage* | ⚡ `PIC_TWIST` · ⚔️ `PIC_DUEL` · ⏪ `PIC_RECUL` · 🚫 `PIC_ANNULATION`
  - **Mots-clés Face 1 :** `Ratissage sur Territoire tenu OU 2 Défenseurs → jeton au sac · Reculer 1`
  - **Mots-clés Face 2 :** `Duel OU 2 Défenseurs → rompt Ratissage OU Étouffe et Recule 1 mobile`
- **Vecteurs :** Territoire tenu ou 2 Défenseurs → machine arrachée au Ratissage (jeton au sac + Reculer) · Face 2 : Étouffer et Reculer une mobile
- **Ambiance :** *L’Anaconda attend des heures, invisible sous la lentille d’eau. Quand la proie s’aventure au bord, chaque expiration resserre ses anneaux, et il l’entraîne là où plus rien ne pousse : au fond.*
- **Face 1 :** Choisissez une machine en Ratissage dont la parcelle porte le Duel sur sa face Territoire tenu ou au moins 2 Défenseurs : elle quitte immédiatement son Ratissage, son jeton Machine retourne dans le sac opaque (elle perd son éventuel jeton Rouge de Ratissage s’il peut être retiré, en conservant ses autres jetons), et vous la faites Reculer d’1 parcelle vers la bordure. S’il n’y a aucune machine en Ratissage éligible, choisissez une machine mobile visant la parcelle du Duel ou une parcelle portant au moins 2 Défenseurs et faites-la Reculer d’1 parcelle.
- **Face 2 :** Même effet dès que la parcelle porte le Duel (quelle que soit sa face) ou au moins 2 Défenseurs ; de plus, vous pouvez choisir à la place une machine mobile active visant cette parcelle pour l’Étouffer et la faire Reculer d’1 parcelle vers la bordure.
- **Décision :** Rompt un Ratissage (ou fait Reculer / Étouffe une machine mobile sur parcelle verrouillée). *(Renoncement : Remet le jeton Machine dans le sac opaque et exige de concentrer 2 Défenseurs ou le Duel sur la parcelle menacée.)*
- **Double ouverture :** Les deux machines d’un rayon finissent souvent ensemble en Ratissage sur la dernière parcelle : deux activations arrachent successivement l’Abatteuse puis le Bulldozer, ou combinent arrachage et Étouffement d’une mobile en Face 2.
- **Entrées plancher :** `RATISSAGE, DUEL` | **Synergies :** `TERRITOIRE` | **Sorties :** `RATISSAGE_ROMPU, RECUL, ANNULATION`
- **Heuristique bot :** Prioritaire dès qu’une machine entre en Ratissage sur une parcelle défendue ou tenue par le Duel ; en Face 2, neutralise directement la mobile la plus dangereuse.
  - **Témoin `G2_T1` (`A_CODER`) :** Abatteuse en Ratissage sur la dernière parcelle portant Territoire tenu : Anaconda F1 la sort du Ratissage, remet son jeton au sac et la fait Reculer d’1 parcelle.
  - **Témoin `G2_T2` (`A_CODER`) :** Anaconda F2 sur une mobile active visant la parcelle du Duel : la machine est Étouffée (jeton à 90°, dé retiré) et Recule d’1 parcelle.

### G3 (`M>O`) — L’Atèle, acrobate des hautes cimes

- **Lisière :** Mammifères → Oiseaux | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Sabotage
- **Mini-Tuile (`L’Atèle`) :** *Fait traverser un Défenseur par la cime* | 🌳 `PIC_ARBRE` · 🛣️ `PIC_ROUTE` · 🛡️ `PIC_DEFENSEUR` · 🦅 `PIC_PERCHOIR`
  - **Mots-clés Face 1 :** `2 cimes même profondeur (M ↔ O) OU Rive ↔ cime · 1 pas avant`
  - **Mots-clés Face 2 :** `Rayon du Perchoir ↔ voisins · Rive ↔ cime · 1 pas avant et après`
- **Vecteurs :** Arbres debout + Routes + Perchoir (O) → traversée haute et Saut de lisière (Rive ↔ Arbre) → redéploiement instantané de Parade
- **Ambiance :** *L’atèle essaie le poids d’une branche avant de lâcher la précédente. Au-dessous de lui, le chemin a disparu.*
- **Face 1 :** Déplacez 1 Défenseur entre deux parcelles de même profondeur portant un Arbre debout, situées sur le rayon Mammifères et le rayon Oiseaux (en sautant les Routes intermédiaires). Avant la traversée, ce Défenseur peut faire 1 pas sur son rayon de départ. Saut de lisière : l’une des deux extrémités (départ ou arrivée) peut être une Rive de Furtivité de ces deux rayons, l’autre devant rester une parcelle portant un Arbre debout.
- **Face 2 :** Même effet entre le rayon désigné par le Perchoir de Vigie (ou le rayon Oiseaux si le Perchoir pointe un rang) et l’un de ses rayons voisins, avec jusqu’à 1 pas avant la traversée et 1 pas après (y compris en Saut de lisière depuis ou vers une Rive de Furtivité de ces rayons).
- **Décision :** Redéploie un Défenseur entre rayons ou entre une Rive de Furtivité et la canopée pour compléter une Parade ou une Rive. *(Renoncement : Quitter une Rive ou un rayon fragilise la défense ou le contrôle de Furtivité laissé derrière soi.)*
- **Double ouverture :** Deux traversées amènent les deux Défenseurs nécessaires à une Parade décisive, ou basculent un pion d’une Rive de Furtivité vers le cœur puis un autre vers une Rive.
- **Entrées plancher :** `ARBRE, ROUTE, DEFENSEUR_REDEPLOYE` | **Synergies :** `PERCHOIR` | **Sorties :** `DEFENSEUR_REDEPLOYE`
- **Heuristique bot :** Évalue chaque Défenseur excédentaire ou sur Rive déjà gagnée/perdue pour compléter une Parade à manque de 1 ou sécuriser une Rive 2/2.
  - **Témoin `G3_T1` (`A_CODER`) :** Saut de lisière F1 : un Défenseur sur la Rive Sabotage de O traverse directement sur une parcelle à Arbre debout de M pour compléter une Parade.
  - **Témoin `G3_T2` (`A_CODER`) :** Atèle F2 avec Perchoir au pied d’un rayon voisin : 1 pas avant, traversée entre cimes, puis 1 pas après pour atteindre exactement la parcelle menacée.

### G4 (`O>M`) — L’Ara rouge, sentinelle de la collpa

- **Lisière :** Oiseaux → Mammifères | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Résonance
- **Mini-Tuile (`L’Ara rouge`) :** *Fait avancer ou réveille d’autres Gardiens* | ⭐ `PIC_PARI_ENCOCHE` · 🔔 `PIC_RESONANCE` · ⚔️ `PIC_DUEL`
  - **Mots-clés Face 1 :** `1 pari tiers → encoche · Second cri si icône voisine OU Territoire → Défi`
  - **Mots-clés Face 2 :** `Active 1 Gardien tiers avec pari · Second cri si icône voisine OU Territoire → Défi`
- **Vecteurs :** Pari Gardien → glissement en encoche (F1) ou activation en relais (F2) · Second cri gratuit sur icône voisine OU Territoire tenu → Défi
- **Ambiance :** *À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.*
- **Face 1 :** Glissez 1 pari d’un autre Gardien en piste dans son encoche libre (sans déclencher son pouvoir ni allumer la Résonance). Second cri : si ce premier Gardien siège sur une icône directement voisine de celle de l’Ara rouge sur la Piste — ou si vous retournez le jeton Duel de sa face Territoire tenu sur sa face Défi —, répétez cet effet sur un second Gardien (ou une seconde fois sur le même). Sentinelle seule : s’il n’y a aucun autre Gardien avec pari en piste, glissez aussitôt un second pari de l’Ara rouge lui-même dans son encoche.
- **Face 2 :** Activez immédiatement en relais 1 autre Gardien en piste portant au moins 1 pari (il glisse 1 pari en encoche et résout son pouvoir, pouvant allumer la Résonance s’il glisse ainsi son dernier pari). Le Second cri (gratuit sur une icône directement voisine de l’Ara rouge, ou en retournant Territoire tenu sur Défi) et le repli Sentinelle seule s’appliquent à l’identique.
- **Décision :** Sécurise (F1) ou réveille en relais (F2) jusqu’à deux Gardiens ; récompense le placement sur des icônes voisines ou la dépense de Territoire tenu. *(Renoncement : En Face 1, sécuriser un pari renonce au pouvoir actif de ce Gardien et ne déclenche pas la Résonance.)*
- **Double ouverture :** Deux activations font boucler un Gardien à 2 paris sur une icône silencieuse ou déclenchent un relais en chaîne en Face 2 ; dès qu’une activation vide le dernier pari d’un Gardien en Face 2, la Résonance se déclenche.
- **Entrées plancher :** `GARDIEN` | **Synergies :** `TERRITOIRE` | **Sorties :** `PARI_GLISSE, ACTIVATION_RELAIS, DEFI`
- **Heuristique bot :** Maximise le taux de passage Face 2 des Gardiens en piste ; privilégie un premier choix sur une icône adjacente à l’Ara pour obtenir le Second cri gratuitement.
  - **Témoin `G4_T1` (`A_CODER`) :** Ara F1 sur Résonance (position 6) choisit un Gardien sur Insecte (position 5, directement voisine) : 1 pari glisse sans pouvoir ni Résonance, et Second cri est gratuit pour un second Gardien.
  - **Témoin `G4_T2` (`A_CODER`) :** Ara F2 active en relais un Gardien sur son dernier pari : ce Gardien résout son pouvoir, vide son dessus et allume Résonance.

### G5 (`R>O`) — L’Iguane vert, dormeur des hautes branches

- **Lisière :** Reptiles → Oiseaux | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Piégeage
- **Mini-Tuile (`L’Iguane vert`) :** *Tombe en Piège sous le Perchoir* | 🪤 `PIC_PIEGE` · 🦅 `PIC_PERCHOIR` · 🦷 `PIC_CROC` · 🔵 `PIC_BLEU`
  - **Mots-clés Face 1 :** `Piège sur cible du Perchoir (sinon R OU O) · Bleu bu = Croc aussi`
  - **Mots-clés Face 2 :** `Piège + Croc partout · Bleu bu = second plongeon`
- **Vecteurs :** Perchoir de Vigie (O) → Piège sur la zone guettée (sinon R ou O) · Bleu bu → Croc (F1) ou second plongeon (F2) → Piégeage en boucle
- **Ambiance :** *L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.*
- **Face 1 :** Posez 1 Piège ordinaire disponible sur une parcelle ciblée libre de Piège désignée par le Perchoir de Vigie (sur son rayon s’il est au pied d’un rayon, ou sur une parcelle visée par une machine du rang qu’il pointe ; à défaut, sur le rayon Reptiles ou le rayon Oiseaux). Si cette machine porte au moins 1 jeton Bleu Surchauffe, vous pouvez en défausser 1 (l’Iguane boit la fraîcheur) pour poser aussi le Croc disponible depuis la réserve Reptile sur une autre parcelle ciblée de votre choix.
- **Face 2 :** Même effet sur n’importe quelle parcelle ciblée du plateau, et vous posez aussi le Croc disponible sur une seconde parcelle ciblée. Si vous buvez 1 jeton Bleu d’une machine visée, résolvez un second plongeon (1 Piège supplémentaire sur une autre parcelle ciblée libre).
- **Décision :** Pose un Piège chirurgical guidé par le Perchoir et peut convertir un Bleu ennemi en Croc (F1) ou en double plongeon (F2). *(Renoncement : Boire un Bleu rend sa pleine puissance à la machine qui le portait si elle survit au piégeage.)*
- **Double ouverture :** Chaque Piège ou Croc qui pare allume Piégeage (l’icône de l’Iguane) : deux chutes couvrent les deux parcelles d’un En avançant, ou boivent un Bleu pour déclencher Croc ou double plongeon.
- **Entrées plancher :** `PERCHOIR` | **Synergies :** `BLEU` | **Sorties :** `PIEGE, CROC`
- **Heuristique bot :** Cible les parcelles à plus fort Seuil sans Défenseur ; boit un Bleu uniquement sur une machine déjà piégée ou facile à parer afin de multiplier les déclenchements de Piégeage.
  - **Témoin `G5_T1` (`A_CODER`) :** Perchoir pointant le rang 4 : Iguane F1 pose 1 Piège sur la parcelle ciblée par la machine du rang 4 ; si elle porte un Bleu, boire ce Bleu pose aussi le Croc de la réserve.
  - **Témoin `G5_T2` (`A_CODER`) :** Iguane F2 pose Piège + Croc sur deux parcelles ciblées de son choix, puis boit 1 Bleu pour effectuer un second plongeon.

### G6 (`O>R`) — Le Toucan toco, le bec-radiateur

- **Lisière :** Oiseaux → Reptiles | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Parade
- **Mini-Tuile (`Le Toucan toco`) :** *Refroidit les machines et relance la Piste* | 🔴 `PIC_ROUGE` · 🔵 `PIC_BLEU` · 🦅 `PIC_PERCHOIR` · 🚫 `PIC_ANNULATION`
  - **Mots-clés Face 1 :** `Refroidir sous le Perchoir (sinon O OU voisin) · 0 Rouge = allume 1 icône à droite`
  - **Mots-clés Face 2 :** `Refroidir partout · 0 Rouge et 2 Bleus = Étouffer · Cri de vapeur actif`
- **Vecteurs :** Perchoir (O) + Rouge → Refroidir · Cri de vapeur (0 Rouge restant OU 0 Rouge éligible) → allume 1 icône à droite sur la Piste · Face 2 : Étouffer à 0 Rouge et ≥ 2 Bleus
- **Ambiance :** *Le bec du toucan toco est un radiateur vivant : il y dirige son sang pour relâcher la chaleur du jour. Au-dessus des machines brûlantes, il rend la fournaise au monde, et le métal s’essouffle.*
- **Face 1 :** Refroidissez 1 machine désignée par le Perchoir de Vigie (sur son rayon s’il est au pied d’un rayon, ou une machine du rang qu’il pointe ; à défaut, une machine du rayon Oiseaux ou d’un rayon voisin). Cri de vapeur : si cette machine n’a plus aucun jeton Rouge après ce Refroidissement — ou s’il n’y avait aucune machine éligible portant un jeton Rouge —, allumez immédiatement 1 icône de votre choix située strictement à droite de celle du Toucan toco sur la Piste des Gardiens (hors Résonance).
- **Face 2 :** Même effet, mais vous pouvez Refroidir n’importe quelle machine du plateau (mobile ou en Ratissage). De plus, si la machine refroidie atteint 0 jeton Rouge et au moins 2 jetons Bleus Surchauffe, vous l’Étouffez immédiatement (le Cri de vapeur s’applique aussi).
- **Décision :** Refroidit une machine ciblée pour réduire son Seuil (ou l’Étouffer en Face 2) et allume une icône à droite sur la Piste via le Cri de vapeur. *(Renoncement : Cibler une machine à 1 seul Rouge maximise le Cri de vapeur en piste, mais laisse intacte une machine à 2 ou 3 Rouges ailleurs.)*
- **Double ouverture :** Assis sur Parade, la première activation Refroidit une machine et, si elle tombe à 0 Rouge (ou sans cible Rouge), le Cri de vapeur allume une icône située à droite du Toucan sur la Piste (hors Résonance) pour relancer d’autres Gardiens ; en Face 2, la seconde activation pousse une machine à 0 Rouge et ≥ 2 Bleus pour l’Étouffer.
- **Entrées plancher :** `ROUGE, PERCHOIR` | **Synergies :** `BLEU` | **Sorties :** `BLEU, ANNULATION_SURCHAUFFE`
- **Heuristique bot :** Siège idéal sur Parade pour maximiser les icônes à droite ; priorise les machines à 1 Rouge (Cri de vapeur immédiat) ou à 1 Rouge + 1 Bleu en Face 2 (Étouffement).
  - **Témoin `G6_T1` (`A_CODER`) :** Toucan F1 assis sur Parade Refroidit la machine à 1 Rouge sous le Perchoir : elle passe à 0 Rouge et Cri de vapeur allume Piégeage (à droite de Parade, hors Résonance).
  - **Témoin `G6_T2` (`A_CODER`) :** Toucan F2 Refroidit partout une machine portant 1 Rouge et 1 Bleu : elle passe à 0 Rouge et 2 Bleus, est immédiatement Étouffée et déclenche Cri de vapeur.

### G7 (`M>H`) — Le Tapir, jardinier des sentiers

- **Lisière :** Mammifères → Humains | **Nature :** `ACTION` | **Rôles :** TWIST_2K3, ENRACINEMENT | **Icône conseillée :** Parade
- **Mini-Tuile (`Le Tapir`) :** *Transforme les Routes en Bourbiers* | ⚡ `PIC_TWIST` · 🛣️ `PIC_ROUTE` · ⚔️ `PIC_DUEL` · 🌱 `PIC_ENRACINEMENT`
  - **Mots-clés Face 1 :** `Duel OU Chamane sur Route = Bourbier bloque 1re traversée OU Frayer Duel`
  - **Mots-clés Face 2 :** `Bourbier Refroidit (sinon Reculer 1) · Territoire tenu bascule sur Défi`
  - **Mots-clés Enraciné :** `Décompte final · Duel + Chamane = +1 Souche`
- **Vecteurs :** Duel ou Chamane sur Route → Bourbier bloquant la 1re traversée/frappe · Frayer → Duel + Territoire tenu · Face 2 : Refroidir ou Reculer · Enraciné : +1 Souche finale
- **Ambiance :** *Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.*
- **Face 1 :** Choisissez : Fouler une Route — posez le jeton Duel (pris où qu’il se trouve, face actuelle) sur une Route Forestière, ou glissez le Tambour ou le Chant depuis une parcelle adjacente sur une Route de son rayon. Tant que Le Tapir est en piste, cette Route devient un Bourbier : la première machine qui devrait la franchir en avançant ou en frappant Devant voit cette avancée ou cette frappe annulée, puis le Duel retourne en réserve (ou le Chamane est couché en attente). Ou Frayer — posez le Duel (pris partout) sur une parcelle ciblée ; s’il y rejoint un Chamane, retournez le Duel sur Territoire tenu.
- **Face 2 :** Même effet, et la machine enlisée dans un Bourbier est en outre Refroidie si elle porte au moins 1 jeton Rouge (sinon, si elle est mobile, faites-la Reculer d’1 parcelle). De plus, un Bourbier tenu par le Duel sur sa face Territoire tenu bascule sur sa face Défi au lieu de rentrer en réserve.
- **Enraciné :** Au décompte final, si le jeton Duel et au moins un Chamane occupent la même parcelle survivante, retournez 1 Souche supplémentaire en Arbre debout sur ce rayon.
- **Décision :** Bloque une avancée ou une frappe Devant par-dessus une Route via un Bourbier, ou scelle le Duel auprès d’un Chamane. *(Renoncement : Engager le Duel ou un Chamane dans un Bourbier le prive de sa présence sur une parcelle forestière active ; enraciner Le Tapir dissipe aussitôt ses Bourbiers.)*
- **Double ouverture :** Deux activations installent un Bourbier sur une Route clé puis posent le Duel sur une parcelle ciblée (ou créent deux Bourbiers distincts avec Duel et Chamane) ; en Face 2, un Bourbier en Territoire tenu résiste à une première machine.
- **Entrées plancher :** `ROUTE, DUEL, TAMBOUR, CHANT` | **Synergies :** `CHAMANE_EN_FORET, ROUGE` | **Sorties :** `BOURBIER_ROUTE, TERRITOIRE, BLEU, RECUL, ARBRE`
- **Heuristique bot :** Prioritaire dès qu’une Route sépare une machine d’une parcelle riche en Arbres ; en absence de Route utile, Frayer sécurise Territoire tenu sur un Chamane.
  - **Témoin `G7_T1` (`A_CODER`) :** Route en M·2 portant le Duel (Bourbier F1) : une machine en M·1 qui doit frapper Devant (M·3) ou avancer par-dessus M·2 voit cette frappe/avancée annulée et le Duel rentre en réserve.
  - **Témoin `G7_T2` (`A_CODER`) :** Tapir F2 avec Duel face Territoire tenu en Bourbier : la machine enlisée est Refroidie (ou Recule d’1) et le Duel bascule sur Défi au lieu de rentrer en réserve.

### G8 (`M>E`) — Le Boto, l’encantado du fleuve

- **Lisière :** Mammifères → Entités | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL, LEVIER_REVE | **Icône conseillée :** Rêve
- **Mini-Tuile (`Le Boto`) :** *Fait glisser les Rêves vers le rang 1* | ⬅️ `PIC_AVANCEE_REVE` · 🌙 `PIC_REVE` · 🌀 `PIC_ALTERATION`
  - **Mots-clés Face 1 :** `Glisser 1 Rêve 1 rang à gauche OU échanger voisins · aucun = Altérer`
  - **Mots-clés Face 2 :** `Glisser 1 Rêve 2 rangs OU plonger sous voisin · aucun = Altérer`
- **Vecteurs :** Rêve glissé d’1 rang à gauche ou échangé (Face 2 : 2 rangs / plongée sous voisin) · plancher sans Rêve : Altérer 1 mobile
- **Ambiance :** *Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.*
- **Face 1 :** Choisissez un Rêve sur la Réglette et Glissez-le d’1 rang libre vers la gauche, ou échangez deux Rêves occupant deux rangs voisins (en conservant l’état debout ou couché de leurs Défenseurs). Si aucun Rêve ne peut bouger (ou s’il n’y a aucun Rêve sur la Réglette), Altérez 1 machine mobile de votre choix.
- **Face 2 :** Même effet, mais le Rêve choisi peut Glisser jusqu’à 2 rangs libres vers la gauche — ou plonger par-dessus un Rêve voisin jusqu’au premier rang libre immédiatement à sa gauche. S’il n’y a toujours aucun mouvement possible, Altérez 1 machine mobile.
- **Décision :** Accélère la convergence des Rêves vers les rangs 1–2–3 pour le Sommeil, ou Altère une mobile en plancher solo. *(Renoncement : Déplacer un Rêve vers la gauche peut lui faire manquer une machine qui allait attaquer sur un rang élevé.)*
- **Double ouverture :** Deux activations font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2) ou compactent deux Rêves séparés vers le Sommeil ; sans Rêve en jeu, elles Altèrent deux machines différentes.
- **Entrées plancher :** `POSITION_REVE, RANG_REVE` | **Synergies :** `—` | **Sorties :** `POSITION_REVE, ALTERATION, ANNULATION`
- **Heuristique bot :** Levier majeur du Sommeil quand E joue sans H ; fait converger les Rêves à gauche dès l’Acte 1, sinon pose des Altérations.
  - **Témoin `G8_T1` (`A_CODER`) :** Boto F1 Glisse un Rêve du rang 5 au rang 4 libre (emportant ses Défenseurs) ; sans Rêve déplaçable, il Altère 1 machine mobile depuis la réserve Entités.
  - **Témoin `G8_T2` (`A_CODER`) :** Boto F2 fait plonger un Rêve du rang 4 par-dessus un Rêve au rang 3 pour atterrir au rang 2 libre.

### G9 (`R>H`) — Le Caïman noir, l’ombre sous la pirogue

- **Lisière :** Reptiles → Humains | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Sabotage
- **Mini-Tuile (`Le Caïman noir`) :** *Pose la cale exclusive sous une machine* | 🧱 `PIC_CALE` · 💥 `PIC_SABOTAGE` · 🥁 `PIC_TAMBOUR` · ⏪ `PIC_RECUL`
  - **Mots-clés Face 1 :** `Jeton Sabotage révélé → cale sous mobile (R · H · Tambour) · bloque Ratissage`
  - **Mots-clés Face 2 :** `Cale partout · mobile calée révélée = Étouffée · Sabotage rallumé`
- **Vecteurs :** Sabotage ou Écaille révélé → cale sous machine mobile (R, H ou Tambour) → Ratissage bloqué · Face 2 : cale partout et machine calée révélée Étouffée
- **Ambiance :** *Le Caïman noir saisit et ne lâche plus : il tient sa proie contre le fond jusqu’à ce qu’elle cesse de lutter. Les pêcheurs le savent : dans les eaux noires, ce qu’il a pris ne remonte pas.*
- **Face 1 :** Glissez le jeton cale (pris en réserve ou déjà sous une autre machine) sous une machine mobile du rayon Reptiles, du rayon Humains ou du rayon portant le Tambour (sinon, faites Reculer d’1 parcelle la machine actuellement calée). Tant qu’elle porte la cale, cette machine ne peut pas entrer en Ratissage, et chaque fois que son jeton Machine est révélé à l’ouverture, allumez aussitôt l’icône Sabotage (la cale reste sous elle jusqu’à ce qu’elle soit déplacée ou que le Caïman noir quitte la piste).
- **Face 2 :** Même effet sur n’importe quelle machine mobile du plateau ; de plus, chaque fois que la machine calée est révélée à l’ouverture, allumez Sabotage et Étouffez-la immédiatement (elle ne frappe pas).
- **Décision :** Verrouille la machine la plus menaçante sous la cale (bloque Ratissage, rallume Sabotage et l’Étouffe en Face 2). *(Renoncement : Une seule cale existe en jeu ; la déplacer libère la machine précédemment retenue.)*
- **Double ouverture :** La première activation pose la cale (sur le Sabotage qui vient d’allumer l’icône), la seconde fait Reculer la machine calée d’1 parcelle ou déplace la cale ; chaque révélation de la machine calée rallume Sabotage sur la Piste.
- **Entrées plancher :** `SABOTAGE, ECAILLE` | **Synergies :** `TAMBOUR` | **Sorties :** `CALE, RECUL, ANNULATION`
- **Heuristique bot :** Pose la cale en priorité sur une machine proche de la dernière parcelle (anti-Ratissage) ou sur la plus chargée en Rouges en Face 2.
  - **Témoin `G9_T1` (`A_CODER`) :** Caïman F1 pose la cale sous l’Abatteuse du rayon du Tambour : elle ne peut pas entrer en Ratissage et sa révélation au tour suivant rallume Sabotage.
  - **Témoin `G9_T2` (`A_CODER`) :** Caïman F2 : lorsque la machine calée est révélée à l’ouverture, Sabotage s’allume et la machine est Étouffée (jeton à 90°, dé retiré).

### G10 (`R>E`) — La Matamata, guetteuse des feuilles mortes

- **Lisière :** Reptiles → Entités | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Piégeage
- **Mini-Tuile (`La Matamata`) :** *Sème une Écaille, embusque le Croc ou Altère* | 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC` · 🌀 `PIC_ALTERATION`
  - **Mots-clés Face 1 :** `Semer 1 Écaille · Happer (Croc réserve → cible) OU Envoûter (Altérer 1 mobile)`
  - **Mots-clés Face 2 :** `Semer 1 Écaille · Happer (Croc partout → cible) · Envoûter (Altérer 1 mobile)`
- **Vecteurs :** Semer 1 Écaille au sac → Happer (Croc sur parcelle ciblée) OU Envoûter (Altérer 1 mobile) · Face 2 : Happer ET Envoûter
- **Ambiance :** *On croit marcher sur un lit de feuilles mortes ; déjà le vide s’est ouvert sous l’acier et la vase glacée l’aspire.*
- **Face 1 :** Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), puis choisissez : Happer — prenez le Croc dans la réserve Reptile et posez-le sur une parcelle ciblée de votre choix ; ou Envoûter — Altérez 1 machine mobile de votre choix et, si le Croc se trouve déjà sur une parcelle non ciblée, vous pouvez le déplacer sur une parcelle ciblée du rayon de cette machine.
- **Face 2 :** Semez au sac 1 Écaille disponible depuis la réserve Reptile (si disponible), puis résolvez à la fois Happer (en pouvant prendre le Croc soit dans la réserve Reptile, soit sur une parcelle non ciblée) et Envoûter.
- **Décision :** Enrichit le sac en Écailles puis arbitre en Face 1 entre embuscade immédiate du Croc (Happer) et pression onirique (Envoûter) ; cumule les deux en Face 2. *(Renoncement : En Face 1, choisir Happer renonce à l’Altération ; choisir Envoûter laisse le Croc en réserve s’il n’est pas déjà en jeu.)*
- **Double ouverture :** Assise sur Piégeage, la première activation Sème 1 Écaille et poste le Croc ; dès que ce Croc pare une attaque (regagnant la réserve Reptile), il rallume Piégeage et déclenche la seconde activation de La Matamata.
- **Entrées plancher :** `ECAILLE, CROC, RANG_MACHINE` | **Synergies :** `ALTERATION` | **Sorties :** `ECAILLE, CROC, ALTERATION`
- **Heuristique bot :** Sème des Écailles tôt pour gonfler le sac ; en Face 1, choisit Happer dès qu’une cible menacée peut rallumer Piégeage, sinon Envoûter.
  - **Témoin `G10_T1` (`A_CODER`) :** Matamata F1 Sème 1 Écaille au sac et choisit Happer : le Croc de la réserve Reptile se poste sur une parcelle ciblée, prêt à rallumer Piégeage.
  - **Témoin `G10_T2` (`A_CODER`) :** Matamata F2 Sème 1 Écaille, repositionne le Croc depuis une parcelle non ciblée vers une cible (Happer) et Altère 1 machine mobile (Envoûter).

### G11 (`O>H`) — La Harpie féroce, l’ombre sous la voûte

- **Lisière :** Oiseaux → Humains | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Parade
- **Mini-Tuile (`La Harpie féroce`) :** *Fond au sol ou saisit une machine sous le Perchoir* | 🦅 `PIC_PERCHOIR` · 🔢 `PIC_RANG_MACHINE` · 🛡️ `PIC_DEFENSEUR` · 🚫 `PIC_ANNULATION`
  - **Mots-clés Face 1 :** `Recycle 1 Oiseau → Fondre devant machine OU Saisir sur rang du Perchoir (Étouffer)`
  - **Mots-clés Face 2 :** `Saisir sur rang du Perchoir OU miroir · porte 1 Chamane vers Rêve opposé`
- **Vecteurs :** Défenseur Oiseau recyclé + Perchoir (O) → Fondre en forêt OU Saisir pour Étouffer sur le rang pointé · Face 2 : rang miroir + Chamane porté sur un Rêve
- **Ambiance :** *Au cri du guetteur, on regarde le ciel. L’ombre est déjà passée.*
- **Face 1 :** Prenez 1 Défenseur Oiseau (en forêt, sur une Rive de Furtivité, sur un Rêve, en lisière ou en attente) et choisissez : Fondre — posez-le sur la parcelle d’une machine ou 1 pas devant elle (en sautant les Routes) ; ou Saisir — si le Perchoir de Vigie pointe un rang 1–6, posez cet Oiseau directement sur le jeton d’une machine mobile active de ce rang pour l’Étouffer jusqu’au ménage.
- **Face 2 :** Même effet, mais Saisir vise aussi bien le rang pointé par le Perchoir de Vigie que son rang miroir (1↔4, 2↔5, 3↔6). De plus, après avoir saisi une machine, vous pouvez emporter 1 Chamane depuis une parcelle visée par cette machine et le poser debout sur un Rêve occupant le rang opposé (son miroir).
- **Décision :** Recycle un Défenseur Oiseau pour renforcer une Parade (Fondre) ou Étouffer net une machine sur le rang guetté (Saisir). *(Renoncement : L’Oiseau posé en saisie reste immobilisé sur le jeton Machine jusqu’au ménage et ne défend plus la forêt ni les Rives.)*
- **Double ouverture :** Un premier piqué pose un Oiseau au sol pour compléter une Parade (qui rallume son icône) ; le second piqué saisit une machine sous le Perchoir pour l’Étouffer.
- **Entrées plancher :** `PERCHOIR, DEFENSEUR_ATTENTE, RANG_MACHINE` | **Synergies :** `CHANT, TAMBOUR, POSITION_REVE` | **Sorties :** `DEFENSEUR_REDEPLOYE, ANNULATION`
- **Heuristique bot :** Privilégie le recyclage d’un Oiseau couché en attente ou libéré ; choisit Saisir sur la mobile la plus létale du rang du Perchoir (et miroir en F2), sinon Fondre pour boucler une Parade.
  - **Témoin `G11_T1` (`A_CODER`) :** Harpie F1 recycle 1 Oiseau couché en attente et choisit Saisir sur le rang 5 pointé par le Perchoir : la mobile du rang 5 est Étouffée jusqu’au ménage.
  - **Témoin `G11_T2` (`A_CODER`) :** Harpie F2 saisit une mobile au rang 2 (miroir du Perchoir au rang 5), puis porte le Chant depuis sa parcelle visée debout sur un Rêve au rang 5.

### G12 (`O>E`) — L’Ibijau, les yeux fendus de la nuit

- **Lisière :** Oiseaux → Entités | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL, TWIST_2K3 | **Icône conseillée :** Sabotage
- **Mini-Tuile (`L’Ibijau`) :** *Relit le dé écarté vers un Rêve* | ⚡ `PIC_TWIST` · 🎲 `PIC_DES_PARAVENT` · 🔢 `PIC_RANG_MACHINE` · 🌙 `PIC_REVE`
  - **Mots-clés Face 1 :** `Dé d’une mobile révélée → rang de son dé écarté sous paravent`
  - **Mots-clés Face 2 :** `OU dé ignoré d’un Sabotage · Rêve qui l’Étouffe Glisse 1 rang à gauche`
- **Vecteurs :** Dé écarté sous paravent (et 2 dés ignorés des porteurs de Sabotage/Écaille en F2) → nouveau rang → Étouffement sur Rêve et glissement du Rêve
- **Ambiance :** *Le jour, l’Ibijau n’est qu’un bout de branche morte. Pourtant il voit : deux fentes dans ses paupières closes guettent tout. La nuit, sa plainte descendante raconte, dit-on, l’histoire d’une jeune femme changée en oiseau, qui pleure encore celui qu’elle a perdu.*
- **Face 1 :** Choisissez une machine mobile révélée dont le dé est encore sur la Réglette : déplacez son dé sur le rang indiqué par le dé écarté sous le paravent de son porteur (fonctionne à l’identique pour l’Oiseau, dont le second dé est son dé écarté). Si la machine change ainsi de rang, elle est résolue sur son nouveau rang (et peut y être Étouffée par un Rêve encore debout ou subir une Loi passive de ce rang).
- **Face 2 :** Même effet, et vous pouvez aussi choisir à la place l’un des 2 dés ignorés d’un joueur ayant révélé un Sabotage ou une Écaille ce tour-ci. De plus, si la machine ainsi déplacée est Étouffée par un Rêve, vous pouvez aussitôt Glisser ce Rêve d’1 rang libre vers la gauche.
- **Décision :** Pousse une machine mobile hors d’un rang létal ou directement sous un Rêve défendu en relisant les dés écartés sous paravent. *(Renoncement : Le dé écarté est souvent plus élevé que le dé retenu : l’utiliser hors Rêve peut faire passer une machine en Assaut ou en En avançant.)*
- **Double ouverture :** Chaque Sabotage révélé allume l’icône de L’Ibijau : deux activations déplacent deux mobiles vers les Rêves encore à résoudre, et en Face 2 puisent aussi dans les dés ignorés des porteurs de Sabotage ou d’Écaille.
- **Entrées plancher :** `DES_SOUS_PARAVENT, RANG_MACHINE, POSITION_REVE` | **Synergies :** `SABOTAGE` | **Sorties :** `RANG_RELU, ANNULATION_INDUITE`
- **Heuristique bot :** Priorise tout déplacement amenant une mobile sur un Rêve défendu encore debout (ou hors d’un rang 3/6 En avançant) ; en F2, exploite les dés ignorés des Sabotages.
  - **Témoin `G12_T1` (`A_CODER`) :** Porteur d’Abatteuse (dés 2 et 5, retenu 2, écarté 5) alors qu’un Rêve défendu siège au rang 5 : Ibijau F1 déplace son dé du rang 2 au rang 5 où le Rêve l’Étouffe.
  - **Témoin `G12_T2` (`A_CODER`) :** Ibijau F2 relit un dé ignoré (4) d’un porteur de Sabotage pour amener une mobile sur le Rêve du rang 4 ; Étouffée, elle permet de Glisser ce Rêve au rang 3 libre.

### G13 (`M>I`) — Le Tamanoir, le grand mangeur qui épargne

- **Lisière :** Mammifères → Insectes | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Insecte
- **Mini-Tuile (`Le Tamanoir`) :** *Éventre un Nid pour déclencher une riposte* | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · ⚔️ `PIC_DUEL`
  - **Mots-clés Face 1 :** `Nid à 2 Insectes OU plus · −1 → +2 · sans Nid éligible = +1 réserve`
  - **Mots-clés Face 2 :** `Riposte projetée sur parcelle ciblée adjacente · sans Nid = +1 réserve`
- **Vecteurs :** Nid à ≥ 2 Insectes éventré (−1 → +2) ou repli réserve (+1) · Face 2 : riposte projetée sur parcelle ciblée adjacente
- **Ambiance :** *Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.*
- **Face 1 :** Choisissez un Nid portant au moins 2 Insectes : défaussez 1 de ses Insectes pour en ajouter aussitôt 2 de la réserve sur ce Nid (gain net de +1 Insecte). S’il n’y a aucun Nid portant au moins 2 Insectes sur le plateau, prenez 1 Insecte de la réserve de l’Essaim et posez-le sur la parcelle d’un Nid (ou, à défaut, sur la parcelle du jeton Duel ou sur une parcelle du rayon Mammifères ou Insectes).
- **Face 2 :** Même effet, mais les 2 Insectes de la riposte peuvent être posés directement sur une parcelle ciblée adjacente au Nid (en sautant les Routes) — y compris sur la parcelle du Duel pour y parer et le retourner nativement sur Territoire tenu.
- **Décision :** Multiplie le stock d’Insectes d’un Nid mûr (ou amorce un Nid vide) et projette la riposte sur les parcelles ciblées en Face 2. *(Renoncement : Exige de maintenir au moins 2 Insectes sur un Nid au lieu de les dépenser tous en parade.)*
- **Double ouverture :** Deux éventrements font gonfler deux Nids (ou deux fois le même) juste avant les attaques ; en Face 2, chaque riposte jaillit directement sur une parcelle ciblée adjacente pour allumer Insecte à la parade.
- **Entrées plancher :** `INSECTE, DUEL` | **Synergies :** `NID` | **Sorties :** `RIPOSTE_ESSAIM, INSECTE, TERRITOIRE`
- **Heuristique bot :** Eventre en priorité un Nid à ≥ 2 Insectes adjacent à une parcelle ciblée (en F2) ou sur le point de produire ; sinon utilise le repli réserve pour porter un Nid à 2 Insectes.
  - **Témoin `G13_T1` (`A_CODER`) :** Nid à 2 Insectes : Tamanoir F1 en défausse 1 et ajoute 2 Insectes de la réserve (le Nid passe à 3 Insectes) ; sans Nid à ≥ 2, pose 1 Insecte de la réserve.
  - **Témoin `G13_T2` (`A_CODER`) :** Tamanoir F2 éventre un Nid à 2 Insectes et projette les 2 Insectes de la riposte sur une parcelle ciblée adjacente portant le Duel face Défi.

### G14 (`R>I`) — Le Téju, la ponte au cœur de la termitière

- **Lisière :** Reptiles → Insectes | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL | **Icône conseillée :** Insecte
- **Mini-Tuile (`Le Téju`) :** *Pond une Écaille protectrice sous un Nid* | 🦎 `PIC_ECAILLE` · 🪹 `PIC_NID` · 🦷 `PIC_CROC` · 🪤 `PIC_PIEGE`
  - **Mots-clés Face 1 :** `Écaille sous 1 Nid → Croc éclot sur frappe et Sème Écaille · sans Nid = Semer + Croc`
  - **Mots-clés Face 2 :** `Jusqu’à 2 pontes (OU 1 ponte + Croc) · le Croc éclot d’où qu’il soit`
- **Vecteurs :** Écaille en ponte sous un Nid (sinon Semer 1 Écaille + Croc sur cible R/I) → éclosion du Croc sur frappe → Piégeage + Écaille semée au sac
- **Ambiance :** *La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.*
- **Face 1 :** Glissez 1 Écaille (prise dans la réserve Reptile ou parmi les Écailles révélées à ce tour) sous un Nid sans ponte (max 1 ponte en jeu). À la première frappe contre la parcelle de ce Nid, si le Croc est en réserve Reptile, il éclot aussitôt sur place : il pare cette frappe (allumant Piégeage), retourne en réserve Reptile et l’Écaille est Semée au sac. S’il n’y a aucun Nid sans ponte (ou déjà 1 ponte en jeu), Semez au sac 1 Écaille disponible et posez le Croc disponible depuis la réserve sur une parcelle ciblée du rayon Reptiles ou du rayon Insectes.
- **Face 2 :** Même effet, mais vous pouvez maintenir jusqu’à 2 pontes simultanées sous des Nids différents (ou 1 ponte + le Croc posté ailleurs), et lors d’une éclosion le Croc peut accourir d’où qu’il se trouve (réserve Reptile ou plateau), puis rentre normalement en réserve Reptile après sa parade.
- **Décision :** Protège un Nid vital contre sa prochaine frappe tout en préparant une Écaille à Semer au sac (et couvre deux Nids en Face 2). *(Renoncement : Immobilise une Écaille hors du sac tant que la ponte n’éclot pas, et exige en Face 1 de garder le Croc en réserve pour l’éclosion.)*
- **Double ouverture :** Deux activations installent deux pontes sous deux Nids (en Face 2) ou combinent une ponte sous un Nid et un Croc directement posté ; chaque éclosion allume Piégeage et Sème l’Écaille au sac.
- **Entrées plancher :** `ECAILLE, CROC` | **Synergies :** `NID` | **Sorties :** `PONTE, CROC, ECAILLE`
- **Heuristique bot :** Pose une ponte dès qu’un Nid est à portée de frappe ; sans Nid libre, Sème une Écaille et poste le Croc directement sur la parcelle la plus menacée de R ou I.
  - **Témoin `G14_T1` (`A_CODER`) :** Téju F1 glisse 1 Écaille sous un Nid ; une frappe sur ce Nid fait éclore le Croc de la réserve (parade + Piégeage + Croc revient en réserve + Écaille Semée au sac).
  - **Témoin `G14_T2` (`A_CODER`) :** Téju F2 entretient 2 pontes simultanées et fait éclore le Croc même s’il était posté sur une autre parcelle, avant qu’il regagne normalement la réserve.

### G15 (`O>I`) — Le Colibri, porteur de gouttes et de pollen

- **Lisière :** Oiseaux → Insectes | **Nature :** `ACTION` | **Rôles :** CATALYSEUR_EVEIL, ENRACINEMENT | **Icône conseillée :** Parade
- **Mini-Tuile (`Le Colibri`) :** *Transporte l’Essaim et accélère les paris* | 🐜 `PIC_INSECTE` · 🦅 `PIC_PERCHOIR` · ⭐ `PIC_PARI_ENCOCHE` · 🌱 `PIC_ENRACINEMENT`
  - **Mots-clés Face 1 :** `1 Insecte → toute parcelle · pris sur icône d’un Gardien = 1 pari en encoche`
  - **Mots-clés Face 2 :** `2 Insectes · arrivée Nid = +1 Insecte · dépôt possible sur rang du Perchoir`
  - **Mots-clés Enraciné :** `Décompte final · +1 Souche par autre tuile enracinée sur O OU voisins`
- **Vecteurs :** Insecte transporté à vol d’oiseau (amorçage natif) → prélèvement sur icône de Gardien = 1 pari en encoche · Face 2 : 2 Insectes + pollinisation + dépôt Perchoir · Enraciné : +1 Souche par tuile voisine
- **Ambiance :** *Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.*
- **Face 1 :** Déplacez 1 Insecte depuis n’importe où sur le plateau vers n’importe quelle parcelle forestière (l’amorçage natif de l’Essaim s’applique si aucun Insecte n’est en jeu). Si cet Insecte est prélevé sur l’icône d’un Gardien en piste portant au moins 1 pari, glissez aussitôt 1 pari de ce Gardien dans son encoche (sans déclencher son pouvoir ni allumer la Résonance).
- **Face 2 :** Même effet avec jusqu’à 2 Insectes. De plus, chaque fois qu’un Insecte transporté arrive sur la parcelle d’un Nid, produisez aussitôt 1 Insecte supplémentaire de la réserve sur ce Nid ; et si le Perchoir de Vigie pointe un rang 1–6, vous pouvez déposer l’un des Insectes directement sur ce rang de la Réglette.
- **Enraciné :** Au décompte final, retournez 1 Souche supplémentaire en Arbre debout sur le rayon de chaque autre tuile enracinée située sur le rayon Oiseaux ou sur l’un de ses deux rayons voisins.
- **Décision :** Ravitaille n’importe quelle parcelle ou déviation, ou prélève un Insecte sur la Piste des Gardiens pour sécuriser un pari. *(Renoncement : Prélever un Insecte sur une icône de Gardien le prive de son rôle de déclencheur sur la Piste ; enraciner Le Colibri sacrifie sa logistique aérienne.)*
- **Double ouverture :** Deux vols complètent une parade urgente puis pollinisent un Nid (Face 2) ou prélèvent un Insecte sur la Piste des Gardiens pour glisser un pari en encoche.
- **Entrées plancher :** `PERCHOIR` | **Synergies :** `INSECTE, NID, GARDIEN` | **Sorties :** `INSECTE_TRANSPORTE, INSECTE, INSECTE_RANG, PARI_GLISSE, ARBRE`
- **Heuristique bot :** Priorise le prélèvement sur une icône de Gardien ayant un pari bloqué ; en Face 2, pollinise les Nids à 1 Insecte et alimente le rang pointé par le Perchoir.
  - **Témoin `G15_T1` (`A_CODER`) :** Colibri F1 prélève 1 Insecte posé sur l’icône d’un Gardien en piste et le dépose sur une parcelle menacée : 1 pari de ce Gardien glisse en encoche sans pouvoir ni Résonance.
  - **Témoin `G15_T2` (`A_CODER`) :** Colibri F2 transporte 2 Insectes : le premier arrive sur un Nid (+1 Insecte produit), le second est déposé sur le rang pointé par le Perchoir de Vigie.

## Rêves — 10 Tuiles (Humains & Entités)

### R1 (`H>E`) — La Liane des Esprits

- **Lisière :** Humains → Entités | **Nature :** `ACTION` | **Rôles :** AUTONOMIE_A0, LEVIER_REVE, ENRACINEMENT | **Icône conseillée :** —
- **Mini-Tuile (`La Liane des Esprits`) :** *Tire un Rêve des Entités et relaie le Tambour* | 🌙 `PIC_REVE` · ⬅️ `PIC_AVANCEE_REVE` · 🥁 `PIC_TAMBOUR` · 🌱 `PIC_ENRACINEMENT`
  - **Mots-clés Face 1 :** `Tire 1 Rêve des Entités · collé = paire Glisse à gauche · Écho Tambour debout dessus`
  - **Mots-clés Enraciné :** `Enracinée sur Rive Sabotage de H sans fermer le Sommeil`
- **Vecteurs :** Rêve Humain défendu → tire un Rêve des Entités contre lui (bloc contigu) · Écho chamane : le Tambour passe debout sur le Rêve tiré · Enraciné sans fermer le Sommeil
- **Ambiance :** *On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.*
- **Règle :** Défendu : après avoir résolu ses annulations habituelles, choisissez un Rêve des Entités situé à droite de La Liane des Esprits et Glissez-le jusqu’au rang libre immédiatement à droite de la Liane (s’il est déjà collé contre elle, Glissez la paire ensemble d’1 rang libre vers la gauche). S’il n’y a aucun Rêve des Entités à droite, Glissez la Liane d’1 rang libre vers la gauche (ou, si le rang à sa gauche est occupé, Étouffez 1 machine mobile supplémentaire sur son rang). Écho chamane : si le Tambour défendait La Liane des Esprits, il peut aussitôt après ces annulations passer debout sur le Rêve des Entités ainsi tiré — s’il n’était pas défendu — afin que ce Rêve se résolve à son tour à l’ouverture.
- **Enraciné :** Enracinée sur la Rive Sabotage du rayon Humains, La Liane des Esprits ne ferme pas la victoire par Sommeil Profond (les autres Rêves peuvent encore former un bloc contigu suffisant).
- **Décision :** Compacte les Rêves vers le Sommeil et permet au Tambour de déclencher en relais un Rêve des Entités non défendu, tout en restant enracinable sans briser le Sommeil. *(Renoncement : Passer le Tambour debout sur le Rêve des Entités le prive d’une descente en forêt et expose ce second Rêve à son propre rang.)*
- **Entrées plancher :** `POSITION_REVE, RANG_REVE` | **Synergies :** `TAMBOUR` | **Sorties :** `REVE_COMPACTE, POSITION_REVE, ANNULATION`
- **Heuristique bot :** Défendue en priorité avec le Tambour dès qu’un Rêve Entités non défendu siège à sa droite ; candidate sûre à l’Enracinement en fin de partie sans bloquer le Sommeil.
  - **Témoin `R1_T1` (`A_CODER`) :** Liane défendue au rang 2 par le Tambour, Rêve Entités non défendu au rang 5 : la Liane tire ce Rêve au rang 3 puis Écho chamane passe le Tambour debout au rang 3 pour le résoudre aussitôt.
  - **Témoin `R1_T2` (`A_CODER`) :** Liane enracinée sur la Rive Sabotage de H : elle apporte l’Effet Sentinelle permanent sans fermer la victoire par Sommeil Profond.

### R2 (`E>H`) — Le Fleuve sous la cendre

- **Lisière :** Entités → Humains | **Nature :** `ACTION` | **Rôles :** AUTONOMIE_A0, ENRACINEMENT | **Icône conseillée :** —
- **Mini-Tuile (`Le Fleuve sous la cendre`) :** *Masque la Furtivité, Altère et marque le Gué* | 🌀 `PIC_ALTERATION` · 🥁 `PIC_TAMBOUR` · 🪵 `PIC_SOUCHE` · 🌱 `PIC_ENRACINEMENT`
  - **Mots-clés Face 1 :** `Linceul = jeton face cachée (0) · Altérer 1 mobile OU relever Tambour sur Rêve à droite`
  - **Mots-clés Enraciné :** `Gué de cendre sur E · machine altérée = 90° · 2 Souches finales`
- **Vecteurs :** Linceul de cendre (altérée/Étouffée → face cachée = 0 en Furtivité) + Altérer OU relever Tambour sur Rêve à droite · Enraciné : Gué de cendre + Gué marqué 90° → 2 Souches finales
- **Ambiance :** *Sous la cendre, l’eau se souvient du lit qu’elle occupait. Le premier arbre à boire lui rend son chemin.*
- **Règle :** Linceul de cendre : tant que Le Fleuve sous la cendre est défendu à ce tour, chaque machine qui perd son Altération à l’ouverture ou qui est Étouffée par ce Rêve retourne son jeton Machine face cachée devant son rayon (il compte pour 0 dans le compte de Furtivité de ce rayon). De plus, à sa résolution, choisissez : Altérez 1 machine mobile (de n’importe quel rayon si le Tambour est en forêt, sinon du rayon Entités ou du rayon Humains) ; ou relevez le Tambour en attente pour le poser debout sur un Rêve non défendu situé à droite de ce Rêve.
- **Enraciné :** Gué de cendre (Rive Sabotage du rayon Entités ; ferme le Sommeil) : toute machine du rayon Entités qui perd son Altération à l’ouverture retourne son jeton face cachée devant le rayon Entités (il compte pour 0 dans son compte de Furtivité). Si au moins 1 machine du rayon Entités porte une Altération au moment de l’enracinement, tournez cette Grande Carte à 90° (Gué marqué). Au décompte final, une carte en Gué marqué retourne 2 Souches survivantes au lieu d’1 en Arbres debout sur le rayon Entités.
- **Décision :** Assure la Rive Sabotage en masquant les jetons en Furtivité, Altère ou relève le Tambour, puis double son rapport de Souches en s’enracinant sur un Gué marqué. *(Renoncement : Enraciner Le Fleuve sous la cendre ferme la victoire par Sommeil Profond ; manquer le marquage d’une machine altérée sur E limite son enracinement à 1 Souche.)*
- **Entrées plancher :** `POSITION_REVE, RANG_MACHINE` | **Synergies :** `TAMBOUR, DEFENSEUR_ATTENTE, ALTERATION` | **Sorties :** `ALTERATION, DEFENSEUR_REDEPLOYE, ARBRE`
- **Heuristique bot :** Défendu dès que E vise la Rive Sabotage ou veut relever un Tambour en attente ; s’enracine au Tour 5–7 dès qu’une machine de E porte une Altération (Gué marqué).
  - **Témoin `R2_T1` (`A_CODER`) :** Fleuve défendu : une mobile perd son Altération à l’ouverture et retourne son jeton face cachée (compte 0 en Furtivité), permettant de gagner la Rive Sabotage à 0 machine visible.
  - **Témoin `R2_T2` (`A_CODER`) :** Enraciné sur la Rive Sabotage de E alors qu’une machine de E est altérée : carte tournée à 90° (Gué marqué), retournant 2 Souches en Arbres au décompte final + Effet Sentinelle permanent.

### R3 (`H>M`) — La Vision du Chamane-Jaguar

- **Lisière :** Humains → Mammifères | **Nature :** `ACTION` | **Rôles :** Standard | **Icône conseillée :** —
- **Mini-Tuile (`Le Chamane-Jaguar`) :** *Étouffe puis fait bondir ses Défenseurs* | 🌙 `PIC_REVE` · 🛡️ `PIC_DEFENSEUR` · 🥁 `PIC_TAMBOUR` · ⚔️ `PIC_DUEL`
  - **Mots-clés Face 1 :** `Après résolution · Défenseurs bondissent en forêt · Écho Tambour emporte le Duel`
- **Vecteurs :** Défenseurs du Rêve après résolution → bond vers Duel ou parcelle ciblée · Écho chamane : le Tambour emporte le Duel sur sa parcelle d’arrivée
- **Ambiance :** *Chez les peuples du Haut Rio Negro, un même mot désigne le chamane et le jaguar. Quand la vision le prend, le chamane quitte le rêve sur quatre pattes et bondit là où la forêt saigne.*
- **Règle :** Défendu : après avoir résolu ses annulations habituelles, chacun des Défenseurs qui défendaient ce Rêve peut bondir directement sur la parcelle du jeton Duel ou sur une parcelle ciblée du rayon d’une machine tout juste Étouffée par ce Rêve (au lieu de rester couché sur le Rêve ; s’il n’a Étouffé aucune machine, ils peuvent bondir sur le rayon Humains ou le rayon Mammifères). Écho chamane : si le Tambour bondit ainsi, il peut emporter le jeton Duel (pris où qu’il se trouve, en conservant sa face actuelle) et le poser sur sa parcelle d’arrivée.
- **Décision :** Transforme chaque Défenseur du Rêve en renfort de Parade immédiat et permet au Tambour de repositionner le Duel où la bataille se joue. *(Renoncement : Quitter le Rêve ne retire pas son blocage déjà résolu, mais oblige à choisir quelle parcelle sauver avec le Duel.)*
- **Entrées plancher :** `RANG_REVE, DUEL` | **Synergies :** `ANNULATION, TAMBOUR` | **Sorties :** `CHAMANE_EN_FORET, DEFENSEUR_REDEPLOYE, TERRITOIRE`
- **Heuristique bot :** Défendue en priorité par le Tambour pour obtenir un double service (Étouffement à l’ouverture + Parade avec Duel repositionné aux attaques).
  - **Témoin `R3_T1` (`A_CODER`) :** Vision défendue par le Tambour : après avoir Étouffé la machine du rang, le Tambour bondit sur une parcelle ciblée en emportant le jeton Duel (Écho chamane).

### R4 (`H>R`) — La Pirogue-Anaconda des ancêtres

- **Lisière :** Humains → Reptiles | **Nature :** `ACTION` | **Rôles :** TWIST_2K3, LEVIER_REVE | **Icône conseillée :** —
- **Mini-Tuile (`La Pirogue-Anaconda`) :** *Pousse tout le convoi et Sème des Écailles* | ⚡ `PIC_TWIST` · ⬅️ `PIC_AVANCEE_REVE` · 🌙 `PIC_REVE` · 🦎 `PIC_ECAILLE`
  - **Mots-clés Face 1 :** `En queue = convoi Glisse 1G · OU échange à droite · chaque mue = Semer 1 Écaille`
- **Vecteurs :** Rêve-piston : Poussée en queue (tout le convoi Glisse d’1) OU Retour (échange à droite) · chaque mue Sème 1 Écaille au sac
- **Ambiance :** *Au commencement, racontent les peuples du Rio Negro, les ancêtres remontèrent le fleuve dans le ventre d’un anaconda-pirogue, de halte en halte, jusqu’à devenir des hommes. La pirogue pousse encore les rêves vers l’amont.*
- **Règle :** Défendu : après ses annulations habituelles, choisissez : Poussée — si La Pirogue-Anaconda est le Rêve le plus à droite de la Réglette (ou le seul), Glissez ensemble tous les Rêves de la Réglette d’1 rang libre vers la gauche (en commençant par le plus à gauche) ; ou Retour — échangez La Pirogue-Anaconda avec le premier Rêve situé à sa droite (en conservant l’état debout ou couché de leurs Défenseurs). Chaque fois qu’un mouvement est effectué ainsi, Semez au sac 1 Écaille disponible depuis la réserve Reptile.
- **Décision :** Pousse tout le convoi des Rêves d’un bloc vers les rangs 1–2–3 ou recule pour relancer un cycle de poussée tout en Semant des Écailles au sac. *(Renoncement : Choisir Retour éloigne temporairement la Pirogue du bloc gauche en échange d’un repositionnement en queue et d’une Écaille.)*
- **Entrées plancher :** `POSITION_REVE, RANG_REVE` | **Synergies :** `—` | **Sorties :** `PISTON_REVES, POSITION_REVE, ECAILLE`
- **Heuristique bot :** Défendue en queue de convoi pour compacter vers le Sommeil tout en enrichissant le sac en Écailles.
  - **Témoin `R4_T1` (`A_CODER`) :** Pirogue-Anaconda en queue au rang 5 avec deux Rêves aux rangs 2 et 4 : Poussée Glisse les trois Rêves aux rangs 1, 3 et 4 et Sème 1 Écaille au sac.

### R5 (`H>O`) — Le Ciel à deux eaux

- **Lisière :** Humains → Oiseaux | **Nature :** `ACTION` | **Rôles :** Standard | **Icône conseillée :** —
- **Mini-Tuile (`Le Ciel à deux eaux`) :** *Inverse les rangs miroirs sous le Perchoir* | 🦅 `PIC_PERCHOIR` · 🔢 `PIC_RANG_MACHINE` · 🥁 `PIC_TAMBOUR` · 🎶 `PIC_CHANT`
  - **Mots-clés Face 1 :** `Échange 2 mobiles à ±3 rangs sous le Perchoir · Écho Chant seul · Tambour Refroidit`
- **Vecteurs :** Perchoir de Vigie (O) → échange de 2 mobiles actives à ±3 rangs (1↔4, 2↔5, 3↔6) · Écho chamane : Chant bascule 1 mobile seule · Tambour Refroidit 1 déplacée
- **Ambiance :** *Les deux rives montrent le même ciel. Une seule voit l’orage arriver.*
- **Règle :** Défendu : avant ses annulations habituelles, si le Perchoir de Vigie pointe un rang 1–6 (ou est au pied d’un rayon en portant un jeton caché), vous pouvez échanger les dés de 2 machines mobiles actives séparées d’exactement 3 rangs (1↔4, 2↔5 ou 3↔6) dont l’une au moins est désignée par le Perchoir (sinon, échangez deux mobiles actives de votre choix séparées de 3 rangs). Écho chamane : si le Chant défend ce Rêve, vous pouvez aussi basculer 1 machine mobile seule vers son rang miroir même sans machine active en face ; si le Tambour défend ce Rêve, Refroidissez l’une des machines ainsi déplacées si elle porte au moins 1 jeton Rouge.
- **Décision :** Bascule une machine d’Assaut vers Charge (ou vers le rang d’un Rêve), avec souplesse de bascule solo via le Chant ou Refroidissement via le Tambour. *(Renoncement : Échanger deux mobiles expose le rang miroir à la seconde machine si aucun Rêve ne l’y attend.)*
- **Entrées plancher :** `PERCHOIR, RANG_MACHINE` | **Synergies :** `TAMBOUR, CHANT, ROUGE` | **Sorties :** `RANG_MACHINE, BLEU`
- **Heuristique bot :** Défendu avec Chant (bascule solo vers ce Rêve ou un Rêve à droite) ou Tambour (échange + Refroidissement d’une machine à Rouge).
  - **Témoin `R5_T1` (`A_CODER`) :** Ciel défendu par le Chant au rang 2 avec Perchoir au rang 5 : la mobile du rang 5 bascule seule sur son miroir au rang 2 où le Rêve l’Étouffe aussitôt.
  - **Témoin `R5_T2` (`A_CODER`) :** Ciel défendu par le Tambour échange deux mobiles entre les rangs 3 et 6 et Refroidit celle qui porte 1 Rouge.

### R6 (`H>I`) — Le Rite de la Tucandeira

- **Lisière :** Humains → Insectes | **Nature :** `ACTION` | **Rôles :** AUTONOMIE_A0 | **Icône conseillée :** —
- **Mini-Tuile (`La Tucandeira`) :** *L’Essaim multiplie les Étouffements du Rêve* | 🌙 `PIC_REVE` · 🐜 `PIC_INSECTE` · 🚫 `PIC_ANNULATION` · 🥁 `PIC_TAMBOUR`
  - **Mots-clés Face 1 :** `Cueille 1 Insecte de H → chaque défaussé Étouffe +1 · Écho Tambour 2 (H/I) · Chant ±1`
- **Vecteurs :** Cueillette d’1 Insecte de H sur ce rang (amorçage natif) → chaque Insecte défaussé Étouffe +1 machine · Écho chamane : Tambour cueille jusqu’à 2 (H/I) · Chant Étouffe aussi à ±1
- **Ambiance :** *Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.*
- **Règle :** Défendu : avant de résoudre ses annulations, vous pouvez cueillir 1 Insecte depuis le rayon Humains pour le poser sur le rang de ce Rêve (l’amorçage natif de l’Essaim s’applique si aucun Insecte n’est sur le plateau). Puis, lors de sa résolution, chaque Insecte que vous défaussez depuis ce rang Étouffe 1 machine mobile supplémentaire de ce rang (en plus du quota habituel de ses Défenseurs). Écho chamane : si le Tambour défend ce Rêve, vous pouvez cueillir jusqu’à 2 Insectes depuis le rayon Humains ou le rayon Insectes ; si le Chant défend ce Rêve, chaque Insecte défaussé peut Étouffer une machine mobile soit sur ce rang, soit sur un rang directement adjacent (±1).
- **Décision :** Transforme des Insectes en Étouffements multiples dès l’ouverture, élargis à ±1 rang avec le Chant ou à 2 cueillettes avec le Tambour. *(Renoncement : Défausser des Insectes sur la Réglette les retire de la défense forestière et de la croissance des Nids.)*
- **Entrées plancher :** `INSECTE, ANNULATION` | **Synergies :** `INSECTE_RANG, TAMBOUR, CHANT` | **Sorties :** `ANNULATION_RENFORCEE, INSECTE_RANG`
- **Heuristique bot :** Défendue par le Chant pour couvrir 3 rangs (rang ±1) avec un seul Défenseur + Insectes, ou par le Tambour pour nettoyer un encombrement de 2–3 machines sur le même rang.
  - **Témoin `R6_T1` (`A_CODER`) :** Tucandeira défendue par le Chant au rang 4 : cueille 1 Insecte de H et le défausse pour Étouffer une machine mobile au rang 5 adjacent (Écho chamane).
  - **Témoin `R6_T2` (`A_CODER`) :** Tucandeira défendue par le Tambour avec 0 Insecte en jeu : amorçage natif en réserve, puis chaque Insecte défaussé Étouffe +1 machine du rang.

### R7 (`E>M`) — Le Curupira, protecteur aux pieds retournés

- **Lisière :** Entités → Mammifères | **Nature :** `LOI_PASSIVE` | **Rôles :** LOI_PASSIVE | **Icône conseillée :** —
- **Mini-Tuile (`Le Curupira`) :** *Inverse la marche et Altère les Étouffées* | ⚖️ `PIC_LOI_PASSIVE` · ⏪ `PIC_RECUL` · ⚔️ `PIC_DUEL` · 🌀 `PIC_ALTERATION`
  - **Mots-clés Face 1 :** `Loi · son rang marche à reculons · tout Recul hors Duel = Territoire · Défendu = Altérer`
- **Vecteurs :** Loi passive : machines sur son rang marchent à reculons + tout Recul hors du Duel (toute cause) retourne Territoire tenu · Défendu : mobiles Étouffées aussi Altérées
- **Ambiance :** *Le Curupira protège les bêtes et punit qui abat trop d’arbres. Ses pieds tournés à l’envers laissent des traces qui égarent les chasseurs : qui croit le suivre s’éloigne de lui, et retourne d’où il vient.*
- **Règle :** Loi passive : toute machine mobile qui attaque depuis le rang du Curupira marche à reculons — sa frappe Devant vise la parcelle derrière elle vers la bordure (en sautant les Routes), son avancée la fait Reculer d’1 parcelle vers la bordure, et sa frappe Sur place ne gagne jamais de jeton Rouge. De plus, partout sur le plateau, toute machine qui Recule hors de la parcelle du jeton Duel face Défi — quelle qu’en soit la cause — retourne aussitôt le Duel sur sa face Territoire tenu. Défendu : chaque machine mobile Étouffée sur son rang est en outre Altérée.
- **Décision :** Laisse Le Curupira sans Défenseur pour faire reculer les machines de son rang et sceller Territoire tenu, ou le défend pour Étouffer et Altérer simultanément. *(Renoncement : Défendre Le Curupira Étouffe la machine au lieu de la laisser reculer d’elle-même, mais pose une Altération pour le tour suivant.)*
- **Entrées plancher :** `RANG_REVE, POSITION_REVE, RANG_MACHINE` | **Synergies :** `DUEL` | **Sorties :** `RECUL, TERRITOIRE, ALTERATION`
- **Heuristique bot :** Positionné sur un rang En avançant (3 ou 6) pour casser l’avancée sans Défenseur ; défendu lorsqu’une mobile critique doit être à la fois Étouffée et Altérée.
  - **Témoin `R7_T1` (`A_CODER`) :** Curupira non défendu au rang 3 : une machine au rang 3 frappe derrière et Recule hors de la parcelle du Duel face Défi, le retournant sur Territoire tenu.
  - **Témoin `R7_T2` (`A_CODER`) :** Curupira défendu au rang 4 : la mobile Étouffée par ce Rêve reçoit en outre 1 jeton d’Altération de la réserve Entités.

### R8 (`E>R`) — La Mue d’obsidienne

- **Lisière :** Entités → Reptiles | **Nature :** `LOI_PASSIVE` | **Rôles :** LOI_PASSIVE, LEVIER_REVE | **Icône conseillée :** —
- **Mini-Tuile (`La Mue d’obsidienne`) :** *Écailles et Rêve glissent, Altèrent ou Refroidissent* | ⚖️ `PIC_LOI_PASSIVE` · 🦎 `PIC_ECAILLE` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION`
  - **Mots-clés Face 1 :** `Loi · chaque Écaille révélée OU Défendu → Glisser 1 Rêve 1G + Altérer OU Refroidir`
- **Vecteurs :** Loi passive 100 % Ouverture : chaque Écaille révélée (ou ce Rêve défendu) → Glisser 1 Rêve d’1 rang libre à gauche + Altérer 1 mobile OU Refroidir 1 machine
- **Ambiance :** *Le reptile abandonne son ancienne peau aux esprits de la nuit ; chaque écaille qui tombe ouvre un sillon d’ombre vers le cœur du sommeil.*
- **Règle :** Loi passive (Ouverture) : chaque fois qu’une Écaille Reptile est révélée à l’ouverture — ainsi que lorsque La Mue d’obsidienne est défendue et résolue —, Glissez 1 Rêve de votre choix d’1 rang libre vers la gauche, puis choisissez : Altérez 1 machine mobile ou Refroidissez 1 machine portant au moins 1 jeton Rouge.
- **Décision :** Convertit chaque Écaille révélée (et chaque défense propre) en avancée vers le Sommeil couplée à une Altération ou un Refroidissement. *(Renoncement : Arbitrer entre Altérer une mobile pour le tour suivant ou Refroidir immédiatement une menace chargée de ce tour.)*
- **Entrées plancher :** `POSITION_REVE, ALTERATION, RANG_MACHINE` | **Synergies :** `ECAILLE, ROUGE` | **Sorties :** `RANG_REVE, ALTERATION, BLEU`
- **Heuristique bot :** Levier passif très rentable avec les Écailles semées par R ; privilégie Refroidir sur menace immédiate à fort Seuil, sinon Altérer pour préparer le tour suivant.
  - **Témoin `R8_T1` (`A_CODER`) :** Une Écaille est révélée à l’ouverture : La Mue d’obsidienne (même non défendue) Glisse 1 Rêve d’1 rang libre à gauche et Refroidit 1 machine à Rouge.
  - **Témoin `R8_T2` (`A_CODER`) :** La Mue d’obsidienne défendue à l’ouverture : après ses annulations, elle Glisse 1 Rêve d’1 rang libre à gauche et Altère 1 machine mobile.

### R9 (`E>O`) — La Matinta Pereira, siffleuse de minuit

- **Lisière :** Entités → Oiseaux | **Nature :** `ACTION` | **Rôles :** LEVIER_REVE | **Icône conseillée :** —
- **Mini-Tuile (`La Matinta Pereira`) :** *Vole vers le Perchoir, maudit ou siffle* | 🦅 `PIC_PERCHOIR` · ⬅️ `PIC_AVANCEE_REVE` · 🌀 `PIC_ALTERATION` · 🔵 `PIC_BLEU`
  - **Mots-clés Face 1 :** `Vole ≤ 2 rangs vers Perchoir · Maudire (Altérer) OU retirer 1–2 Altérations → Glisser + Refroidir`
- **Vecteurs :** Perchoir de Vigie (O) → vol de 2 rangs avant annulation · puis Maudire (Altérer) OU Siffler dans la brume (retire 1–2 Altérations → Glisse 1–2 Rêves à gauche + Refroidit)
- **Ambiance :** *Le sifflement de la Matinta semble venir de partout à la fois. Promettez-lui du tabac et elle s’en va ; refusez, et votre nuit sera maudite.*
- **Règle :** Défendu : avant de résoudre ses annulations, si le Perchoir de Vigie pointe un rang 1–6, Glissez La Matinta Pereira jusqu’à 2 rangs libres en direction de ce rang (elle peut s’y poser s’il est libre). Après ses annulations habituelles, choisissez : Maudire — Altérez 1 machine mobile de ce rang (même tout juste Étouffée) ou du rayon ou du rang désigné par le Perchoir (à défaut, du rayon Entités) ; ou Siffler dans la brume — retirez 1 ou 2 jetons d’Altération en jeu (rendus à la réserve Entités) : pour chaque Altération ainsi retirée, Glissez 1 Rêve d’1 rang libre vers la gauche et, si la machine réveillée porte au moins 1 jeton Rouge, Refroidissez-la.
- **Décision :** Intercepte une machine en volant vers le Perchoir, puis accumule des Altérations (Maudire) ou les encaisse en tempo Sommeil + Refroidissement (Siffler dans la brume). *(Renoncement : Retirer des Altérations par Siffler dans la brume renonce à leur effacement au tour suivant mais accélère nettement la convergence des Rêves.)*
- **Entrées plancher :** `PERCHOIR, RANG_REVE` | **Synergies :** `ALTERATION, ROUGE` | **Sorties :** `POSITION_REVE, ALTERATION, BLEU`
- **Heuristique bot :** Vole vers le rang du Perchoir pour Étouffer la cible ; choisit Siffler dans la brume dès que 1–2 Altérations sont mûres pour fermer le Sommeil ou Refroidir.
  - **Témoin `R9_T1` (`A_CODER`) :** Matinta défendue au rang 4 avec Perchoir pointant le rang 2 libre : elle vole au rang 2, Étouffe la mobile présente et choisit Maudire pour l’Altérer.
  - **Témoin `R9_T2` (`A_CODER`) :** Matinta choisit Siffler dans la brume en retirant 2 Altérations en jeu : elle Glisse 2 Rêves d’1 rang libre à gauche et Refroidit chaque machine réveillée portant un Rouge.

### R10 (`E>I`) — La Transe de la Ruche vagabonde

- **Lisière :** Entités → Insectes | **Nature :** `ACTION` | **Rôles :** AUTONOMIE_A0, TWIST_2K3, LEVIER_REVE | **Icône conseillée :** —
- **Mini-Tuile (`La Ruche vagabonde`) :** *Glisse un Rêve et déménage une ruche* | ⚡ `PIC_TWIST` · ⬅️ `PIC_AVANCEE_REVE` · 🪹 `PIC_NID` · 🌀 `PIC_ALTERATION`
  - **Mots-clés Face 1 :** `Glisser 1 Rêve 1G · déménage 1 Nid + Altérer OU Refroidir · OU +1 Insecte + Altérer`
- **Vecteurs :** Glisser 1 Rêve d’1 rang à gauche + Envol de la Ruche (déménage 1 Nid avec garnison + Altérer ou Refroidir) OU Essaim spectral (+1 Insecte réserve + Altérer)
- **Ambiance :** *Guidé par le songe, le nid décroche ses racines d’écorce et traverse la nuit : quand l’acier frappe la clairière, la ruche est déjà derrière lui.*
- **Règle :** Défendu : après ses annulations habituelles, Glissez 1 Rêve de votre choix d’1 rang libre vers la gauche, puis choisissez : Envol de la Ruche — déménagez 1 Nid en jeu vers n’importe quelle parcelle forestière sans autre Nid (en emportant tous ses Insectes, tous ses Défenseurs et son éventuelle ponte selon la règle commune), puis Altérez 1 machine mobile du rayon rejoint ou Refroidissez 1 machine présente sur la parcelle rejointe ; ou Essaim spectral — prenez 1 Insecte dans la réserve de l’Essaim pour le poser sur le rayon Entités, le rayon Insectes ou un rang 1–6 de la Réglette, puis Altérez 1 machine mobile de votre choix.
- **Décision :** Avance vers le Sommeil tout en téléportant un Nid complet avec sa garnison (ou en injectant un Insecte + une Altération en plancher solo). *(Renoncement : Déménager un Nid avec ses Défenseurs dégarnit instantanément la parcelle de départ.)*
- **Entrées plancher :** `POSITION_REVE, RANG_MACHINE` | **Synergies :** `NID, INSECTE, ROUGE` | **Sorties :** `RANG_REVE, NID_DEPLACE, ALTERATION, INSECTE, BLEU`
- **Heuristique bot :** Exploite Envol de la Ruche pour projeter un Nid défendu sur une parcelle critique (ou la dernière parcelle d’un rayon pour débloquer le déploiement sur la Réglette).
  - **Témoin `R10_T1` (`A_CODER`) :** Table {H, E, I} : La Transe de la Ruche vagabonde Glisse un Rêve à gauche puis téléporte un Nid avec son Défenseur et ses 2 Insectes sur la parcelle menacée d’un autre rayon et Refroidit le Bulldozer sur place.

## Nids de l’Essaim — 5 Tuiles (Insectes)

### M1 (`I>M`) — Le Pelage du Paresseux

- **Lisière :** Insectes → Mammifères | **Nature :** `ACTION` | **Rôles :** Standard | **Icône conseillée :** —
- **Mini-Tuile (`Le Pelage du Paresseux`) :** *Des passagers qui voyagent sur les machines* | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · ➡️ `PIC_MIGRATION` · ⚔️ `PIC_DUEL`
  - **Mots-clés Face 1 :** `1–2 Insectes embarquent sur 1 machine voisine · sautent à la frappe · descente ménage`
- **Vecteurs :** Insectes (I) embarqués en phorésie sur une machine → sautent en parade là où elle frappe → descente au ménage
- **Ambiance :** *La fourrure du paresseux est un monde : des algues, des champignons, des papillons qui n’existent nulle part ailleurs. Ces passagers voyagent sans bouger leurs ailes, et savent descendre au bon endroit.*
- **Règle :** Production (défendu) : après la production de ce Nid, vous pouvez embarquer 1 ou 2 Insectes présents sur la parcelle de ce Nid sur une machine située sur son rayon ou sur un rayon voisin (ils deviennent des passagers et se déplacent avec elle). Chaque fois que cette machine frappe une parcelle, avant la résolution de la parade, vous pouvez faire sauter tout ou partie de ses passagers sur la parcelle frappée pour aider la parade (une parade sur la parcelle du Duel le retourne nativement sur Territoire tenu). Au ménage, les passagers encore à bord descendent sur la parcelle où la machine s’est arrêtée.
- **Décision :** Embarque 1–2 Insectes en réserve mobile directement sur la machine ennemie pour parer sa frappe la plus dangereuse. *(Renoncement : Quitter le Nid réduit sa garnison sous le seuil de 2 Insectes pour la Production suivante.)*
- **Entrées plancher :** `NID, INSECTE` | **Synergies :** `DUEL` | **Sorties :** `INSECTE_PASSAGER, TERRITOIRE`
- **Heuristique bot :** Embarque 1–2 Insectes sur la machine la plus menaçante du rayon I ou voisin dès que le Nid conserve 2 Insectes (ou qu’une parade critique manque de 1–2).
  - **Témoin `M1_T1` (`A_CODER`) :** 2 passagers embarqués sur le Bulldozer : quand il frappe la parcelle du Duel face Défi (1 Défenseur, Seuil 3), les 2 passagers sautent, parent la frappe (icône Insecte) et retournent nativement le Duel sur Territoire tenu.
  - **Témoin `M1_T2` (`A_CODER`) :** Un passager non dépensé descend au ménage sur la dernière parcelle atteinte par sa machine.

### M2 (`I>R`) — La Termitière-Forteresse

- **Lisière :** Insectes → Reptiles | **Nature :** `ACTION` | **Rôles :** Standard | **Icône conseillée :** —
- **Mini-Tuile (`La Termitière-Forteresse`) :** *Forteresse d’argile et soldats à glu* | 🪹 `PIC_NID` · 🐜 `PIC_INSECTE` · 🦎 `PIC_ECAILLE` · 🦷 `PIC_CROC`
  - **Mots-clés Face 1 :** `2 Insectes du Nid parent tout Seuil · Production = Semer 1 Écaille OU Croc sur place`
- **Vecteurs :** Soldats (2 Insectes parent tout Seuil sur ce Nid) · Production défendue → Semer 1 Écaille au sac OU poster le Croc sur machine présente
- **Ambiance :** *Le mur de la termitière est plus dur que la brique. Ses soldats, la tête en forme de seringue, projettent une glu qui colle tout ce qui ose y toucher. Les reptiles le savent : il n’est pas d’abri plus sûr.*
- **Règle :** Soldats à glu : lorsqu’une machine frappe la parcelle de ce Nid, vous pouvez défausser 2 Insectes présents sur ce Nid pour parer seuls cette frappe quel que soit son Seuil (sans aucun Défenseur requis ; allume l’icône Insecte). Production (défendu) : après la production de ce Nid, choisissez — Semez au sac 1 Écaille disponible depuis la réserve Reptile ; ou, si une machine mobile se trouve sur la parcelle de ce Nid, posez le Croc disponible depuis la réserve Reptile sur cette parcelle.
- **Décision :** Défend sa propre parcelle contre n’importe quel Seuil avec 2 Insectes et alimente le sac en Écailles (ou pose le Croc). *(Renoncement : Dépenser 2 Insectes en Soldats à glu vide rapidement la termitière avant sa prochaine Production.)*
- **Entrées plancher :** `NID, INSECTE` | **Synergies :** `—` | **Sorties :** `PARADE_SOLDATS, ECAILLE, CROC`
- **Heuristique bot :** Défendue tôt pour Semer des Écailles au sac et maintenir ≥ 2 Insectes capables de parer seuls un Assaut à haut Seuil.
  - **Témoin `M2_T1` (`A_CODER`) :** Abatteuse en Assaut à Seuil 4 sur le Nid sans Défenseur : 2 Insectes défaussés parent seuls la frappe et allument l’icône Insecte.
  - **Témoin `M2_T2` (`A_CODER`) :** Production défendue sans machine présente : 1 Écaille de la réserve Reptile est Semée au sac.

### M3 (`I>O`) — Le Bivouac des Légionnaires

- **Lisière :** Insectes → Oiseaux | **Nature :** `ACTION` | **Rôles :** TWIST_2K3 | **Icône conseillée :** —
- **Mini-Tuile (`Le Bivouac des Légionnaires`) :** *Nid nomade guidé par le Perchoir* | ⚡ `PIC_TWIST` · 🪹 `PIC_NID` · ➡️ `PIC_MIGRATION` · 🦅 `PIC_PERCHOIR`
  - **Mots-clés Face 1 :** `Défendu avant prod → avance 1 pas (2 vers Perchoir) · prod · raid 1–2 Insectes`
- **Vecteurs :** Production (Nid défendu) → déménagement avant production (1 pas, ou 2 vers/sur le rayon du Perchoir, garnison emportée) → production → Front de raid (1–2 Insectes)
- **Ambiance :** *Le bivouac n’a pas de murs : ce sont les fourmis elles-mêmes, accrochées les unes aux autres. Chaque nuit, la colonne repart ; et derrière son front de raid, les oiseaux fourmiliers suivent, guettant ce qui s’enfuit.*
- **Règle :** Production (défendu) : avant de produire, si ce Nid est défendu, vous pouvez le déplacer d’1 parcelle libre adjacente (sans autre Nid ; en sautant les Routes, y compris latéralement entre parcelles de même profondeur) — ou jusqu’à 2 parcelles libres adjacentes en vous rapprochant ou en restant sur le rayon désigné par le Perchoir de Vigie — en emportant simultanément tous ses Insectes, tous ses Défenseurs et son éventuelle ponte selon la règle commune. Puis ce Nid produit normalement et lance son Front de raid : déplacez 1 ou 2 Insectes de ce Nid vers une parcelle ciblée adjacente.
- **Décision :** Déplace un bastion entier (Nid + Défenseurs + Insectes) vers le point chaud du tour puis projette un Front de raid de 1–2 Insectes. *(Renoncement : Exige un Défenseur sur le Nid pour lever le camp ; projeter 2 Insectes en raid expose le Nid lui-même à sa prochaine frappe.)*
- **Entrées plancher :** `NID, INSECTE` | **Synergies :** `PERCHOIR` | **Sorties :** `NID_NOMADE, INSECTE`
- **Heuristique bot :** Suit le Perchoir de Vigie ou la plus forte pression machine pour repositionner un Défenseur + Nid + Front de raid en une seule Production.
  - **Témoin `M3_T1` (`A_CODER`) :** Bivouac défendu en I·1 avec Perchoir au pied du rayon O voisin : il avance de 2 parcelles vers O avec son Défenseur et ses Insectes, produit, puis envoie 2 Insectes en Front de raid.

### M4 (`I>H`) — Le Rucher des Mélipones

- **Lisière :** Insectes → Humains | **Nature :** `ACTION` | **Rôles :** AUTONOMIE_A0 | **Icône conseillée :** —
- **Mini-Tuile (`Le Rucher des Mélipones`) :** *Le miel relève les bâtisseurs couchés* | 🪹 `PIC_NID` · ♻️ `PIC_DEFENSEUR_ATTENTE` · 🥁 `PIC_TAMBOUR` · 🐜 `PIC_INSECTE`
  - **Mots-clés Face 1 :** `1 Insecte → relève 1 bâtisseur en attente sur le Nid OU le Tambour (max 2)`
- **Vecteurs :** Insecte consommé à la Production → relève 1 bâtisseur en attente vers le Nid ou le Tambour (H), jusqu’à 2 fois
- **Ambiance :** *Les mélipones n’ont pas de dard ; elles offrent leur miel aux peuples qui les protègent depuis des siècles. Une gorgée, et ceux qui ont bâti jusqu’à l’épuisement se relèvent pour défendre la forêt.*
- **Règle :** Production (défendu) : après la production de ce Nid, vous pouvez défausser 1 ou 2 Insectes présents sur ce Nid. Pour chaque Insecte ainsi défaussé, relevez 1 Défenseur couché en attente (bâtisseur ou pion couché) et posez-le actif sur la parcelle de ce Nid ou sur la parcelle du Tambour.
- **Décision :** Convertit des Insectes en Défenseurs actifs au tour même où un joueur a construit, effaçant le coût de construction. *(Renoncement : Consomme les Insectes du Nid au lieu de les accumuler pour les parades ou les déviations.)*
- **Entrées plancher :** `NID, INSECTE, DEFENSEUR_ATTENTE` | **Synergies :** `TAMBOUR` | **Sorties :** `DEFENSEUR_REDEPLOYE, INSECTE`
- **Heuristique bot :** Prioritaire les tours de construction ; relève en priorité un bâtisseur vers la parcelle menacée du Tambour ou du Nid.
  - **Témoin `M4_T1` (`A_CODER`) :** Après construction d’un Rêve (2 bâtisseurs couchés), Le Rucher des Mélipones défendu défausse 1 Insecte pour relever 1 bâtisseur actif sur la parcelle du Tambour.

### M5 (`I>E`) — Le Mycélium luminescent, réseau spectral des racines noires

- **Lisière :** Insectes → Entités | **Nature :** `LOI_PASSIVE` | **Rôles :** AUTONOMIE_A0, LOI_PASSIVE | **Icône conseillée :** —
- **Mini-Tuile (`Le Mycélium luminescent`) :** *Déviations vers Rêves Altèrent et recyclent* | ⚖️ `PIC_LOI_PASSIVE` · 🌙 `PIC_REVE` · 🌀 `PIC_ALTERATION` · 🐜 `PIC_INSECTE`
  - **Mots-clés Face 1 :** `Loi · Déviation vers Rêve → Altérer + recycle si < 2 · Prod = 1 Insecte Réglette OU Altérer`
- **Vecteurs :** Loi passive : Déviation ±1 vers Rêve → Altérer + recycle l’Insecte sur ce Nid (si < 2) · Production défendue → 1 Insecte vers Réglette OU Altérer
- **Ambiance :** *Ce que l’insecte touche là-haut résonne aussitôt sous l’humus : un seul pas de travers dans les spores plonge la machine dans un cauchemar éveillé.*
- **Règle :** Spores de déviation (Loi passive) : chaque fois qu’un Insecte défaussé sur la Réglette dévie une machine mobile (±1) sur le rang d’un Rêve, Altérez cette machine ; de plus, si ce Nid porte strictement moins de 2 Insectes, replacez l’Insecte défaussé sur ce Nid au lieu de le rendre à la réserve. Filaments oniriques (Production défendue) : après la production de ce Nid, choisissez — déplacez 1 Insecte de ce Nid directement sur un rang 1–6 de la Réglette ; ou Altérez 1 machine mobile de votre choix.
- **Décision :** Nourrit la Réglette en Insectes de déviation depuis n’importe quelle parcelle (Filaments oniriques) et recycle les déviations vers les Rêves en Altérations. *(Renoncement : Envoyer un Insecte sur la Réglette laisse ce Nid sous le seuil de 2 Insectes jusqu’au prochain recyclage par déviation.)*
- **Entrées plancher :** `NID_ACTIVE, INSECTE` | **Synergies :** `INSECTE_RANG, POSITION_REVE` | **Sorties :** `ALTERATION, INSECTE_RANG, INSECTE`
- **Heuristique bot :** Défendu dès que possible pour alimenter les rangs adjacents aux Rêves en Insectes ; déclenche le recyclage automatique sur toute déviation vers un Rêve.
  - **Témoin `M5_T1` (`A_CODER`) :** Le Mycélium luminescent défendu envoie 1 Insecte sur le rang 4 (Filaments oniriques) ; au tour suivant, la déviation ±1 vers un Rêve au rang 3 Altère la machine et recycle l’Insecte sur ce Nid (< 2).
