# Panel v6.3 — Revue 2 · Passe 1 · Fiches révisées

*Amazonia : Dernier Rempart* · socle **`v6.2.0`** verrouillé (`rules_canon_v6_2.json`, `physical_and_edge_invariants.json`) · `cadrage_tuiles_v6_3.md` complété par les **4 Murs porteurs physiques**.
Ce document remplace 11 fiches du Panel 1 ; les 19 autres restent inchangées.

---

## 0. Vue d’ensemble

| Tuile | Défaut relevé | Correction |
|---|---|---|
| **G7** · Le Tapir `M>H` | Souche retournée en cours de partie et déplacée d’une parcelle à l’autre (Murs 1 et 3) | **Réinvention** : le Duel ou un Chamane posé sur une Route en fait un *sentier*, parcelle vide que les machines ne sautent plus ; Enraciné lu au seul décompte final |
| **G5** · L’Iguane vert `R>O` | Inerte tant qu’aucun Bleu n’est en jeu (Mur 4) | Piège garanti, guidé par la Plume ; boire un Bleu devient l’amplificateur (Croc en Face 1, second plongeon en Face 2) |
| **G15** · Le Colibri `O>I` | Pollinisation = repousse active (Mur 1) ; rien à porter avant le 1er Nid (Mur 4) | Amorçage depuis la réserve ; Pollinisation = +1 Insecte au Nid visité ; Fleur signalée par la Plume |
| **R1** · La Liane des Esprits `H>E` | Aucun effet propre sans Rêve des Entités à sa droite (Mur 4) | La liane grimpe d’1 rang, ou serre une machine de plus |
| **G4 · G8 · G10 · G13 · G14 · R6 · R10** | Coup dans le vide si la tuile est construite en premier | Clause plancher d’une phrase ; icône de repli pour les Gardiens dont l’icône conseillée ne s’allume pas seule |

**Architecture conservée.** Twists 2K3 `{G2, G7, R4}` + `{G12, R10, M3}` · étoile de 4 Lois passives `{R2, R7, R8, M5}` (aucune loi ajoutée : le sentier du Tapir est un état porté par des pièces) · synergies d’Enracinement (I06) `{G3, G7, G15, R1}` = 4.

**Conventions de lecture**
- **Plancher** : clause qui garantit un effet utile quand la tuile est seule sur le plateau (Mur 4) ; elle s’efface dès que l’état attendu existe.
- **Amplificateur** : bonus qui ne joue que si une autre tuile a produit l’état requis (Bleu, Nid, Rêve…).
- **Icône de repli** : l’icône d’un Gardien se choisit à sa construction et ne change plus ensuite (Mur 3). Un Gardien construit en premier prend son icône de repli ; s’il retombe en lisière puis est reconstruit, il peut rejoindre son icône conseillée.
- **« Aucun Insecte en jeu »** : aucun jeton Insecte sur un Nid, une parcelle, un rang de la Réglette, une icône de la Piste ou une machine.
- **Plafond d’activation** (lecture du Panel 1, à confirmer en §4) : chaque activation fait glisser 1 Défenseur en pari dans une encoche ; un Gardien s’active donc au plus deux fois par tour.
- **Témoins de démarrage** : un Gardien ou un Rêve construit au Tour 1 reçoit ses premiers paris ou Défenseurs au Tour 2 ; les témoins solo se jouent donc au Tour 2.

---

## 1. Réinvention

### G7 · Le Tapir, jardinier des sentiers (`M>H`)

*Remplace intégralement la fiche G7 du Panel 1.*

**Identité & Rôles** — Rôles : `TWIST_2K3` · `ENRACINEMENT` — Nature : `ACTION`

*Moteur de lisière M–H (mis à jour)* : Duel (M) ou Chamane (H) posé sur une Route → sentier : frappes et avancées absorbées, machine repoussée quand il cède ; Duel qui rejoint un Chamane = Territoire tenu ‖ Défenseur d’un Rêve (H) → bond vers la parcelle du Duel (M) ou du rayon annulé → double emploi annulation + parade *(R3, inchangé)*.

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Parade
- **Pictogrammes** : ⚡ Brique-Twist 2K3 · 🛣️ Route → sentier · ⚔️ Duel · 🥁 Chamane (Tambour / Chant)
- **Face 1** : « Duel ou Chamane sur une Route = sentier : parcelle vide, plus sautée · sinon Duel → Chamane = Territoire tenu »
- **Face 2** : « + frappes des parcelles voisines détournées sur le sentier · l’Abatteuse n’en déloge plus le Duel »
- **Enraciné** : « Fin de partie : Duel + Chamane sur une parcelle = 1 repousse de plus »
- **Résumé** : *Change les Routes en sentiers où les machines s’enlisent.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Le Tapir terrestre (*Tapirus terrestris*), animal entier : grand herbivore à la trompe mobile, robe brun sombre et courte crinière, qui avance au crépuscule dans un sentier de boue tracé en travers d’une trouée de bulldozer. Empreintes à quatre doigts dans la glaise ; à l’orée, un chamane suit la piste, tambour à la main.

> *Le Tapir ne contourne rien : il trace. Là où la machine a laissé une plaie de terre nue, il passe et repasse, et la plaie devient sentier. Les hommes l’empruntent depuis toujours ; les machines, elles, s’y enlisent. Quant aux graines semées en chemin, elles attendront la fin des combats pour lever.*

**Face 1 — Le sentier battu.** Quand le Tapir s’active, choisissez l’un de ses deux pas.
- **Fouler une Route.** Posez le jeton Duel sur une Route Forestière de n’importe quel rayon — pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère —, ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon. Cette Route devient un **sentier**.
- **Frayer** (toujours possible, même sans aucune Route en jeu). Posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère. S’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu : les hommes tiennent déjà ce terrain.

**Encadré « Le sentier »** *(imprimé au recto comme au verso de la Grande Carte)*
1. **Ce qu’il est.** Tant qu’il porte le Duel ou un Chamane, le sentier compte comme une parcelle, avec le chiffre gravé de sa case, bien qu’il ne porte ni Arbre ni Souche.
2. **Ce qu’il change.** Les machines ne le sautent plus : une frappe Devant le vise, une avancée s’y arrête. Une frappe sur le sentier ne fait jamais gagner de Rouge.
3. **Ce qu’il accueille.** Défenseurs, Piège et Insectes, comme toute parcelle. Le Duel y suit ses règles habituelles : une parade le retourne sur Territoire tenu ; une frappe non parée et non piégée le renvoie en réserve.
4. **Ce qui le défait.** Une frappe de Bulldozer non parée le refait Route. Et dès qu’il ne porte plus ni Duel ni Chamane (frappe, déplacement, retour des Défenseurs au ménage), il redevient Route : la case est vidée comme toute Route, et une machine qui s’y trouve se replie comme sur une Route qui vient de se créer.
5. **Ses limites.** Jamais de sentier sur la dernière case d’un rayon. Si le Tapir quitte la Piste des Gardiens, chaque sentier redevient aussitôt Route. Aucun pion Arbre ou Souche n’est jamais déplacé.

**Face 2 — Le sentier qui égare.** Quand le Tapir s’active, choisissez l’un de ses deux pas.
- **Fouler une Route.** Posez le jeton Duel sur une Route Forestière de n’importe quel rayon (pris dans la réserve ou là où il se trouve, sur sa face actuelle, même sans Défenseur Mammifère), ou faites-y descendre le Tambour ou le Chant depuis la parcelle voisine de cette Route, sur le même rayon : elle devient un sentier.
- **Frayer** (toujours possible). Posez le jeton Duel, sur sa face actuelle, sur une parcelle ciblée, même sans Défenseur Mammifère ; s’il y rejoint le Tambour ou le Chant, retournez-le aussitôt sur Territoire tenu.

En Face 2, le sentier obéit à l’encadré avec deux pas de plus :
- **Les machines s’égarent.** Quand une machine attaque, avant de figer ses cibles : si l’une d’elles est la parcelle juste avant ou juste après un sentier sur ce rayon, vous pouvez détourner cette frappe sur le sentier.
- **La boue tient.** Une frappe d’Abatteuse non parée sur un sentier ne déloge plus le Duel : seul un Bulldozer non paré refait la Route.

**Enraciné — Les graines du sentier.** Au décompte final, en plus de sa repousse habituelle (1 Souche, ou 2 s’il était en Face 2, sur la parcelle qu’il regarde), le Tapir fait repousser 1 Souche de la parcelle qui porte le jeton Duel, si le Tambour ou le Chant s’y tient aussi. Cette clause ne se lit qu’au décompte final.

**Dilemme.** *Choix* : fouler une Route — avec le Duel, qui tient d’un tour à l’autre, ou avec un Chamane, jusqu’au ménage — ou frayer pour poster le Duel en Territoire tenu auprès d’un Chamane. *Renoncement* : le Duel posé sur un sentier ne garde plus aucune parcelle boisée ; le Chamane qui descend abandonne la parcelle qu’il gardait ; un Bulldozer non paré refait la Route en vidant la case.

**Double activation.** Deux pas, deux sentiers : la première activation pose le Duel sur une Route, la seconde y fait descendre un Chamane sur une autre, ou sur la même pour que le sentier survive au départ du Duel. Chaque frappe parée sur un sentier allume Parade, l’icône du Tapir. En Face 2, chaque sentier attire en plus les frappes de ses deux voisines.

#### Cas témoins
**G7_T1 — le sentier tenu par le Tambour.** Tour 3, Acte 1. Rayon H : la parcelle 1 (2 Arbres) porte le Bulldozer (rang 3), l’Abatteuse (rang 5) et le Tambour ; la parcelle 2 est une Route ; la parcelle 3 porte 3 Arbres. Après une parade au rang 1, le Tapir (sur Parade) s’active : le Tambour descend sur la Route, qui devient sentier (chiffre gravé 2).
- **Rang 3** (En avançant, Charge, Seuil 2 − 1 = 1) : le Bulldozer frappe la parcelle 1, non parée (il y reste 1 Arbre ; +1 Rouge), puis le sentier au lieu de la parcelle 3 : le Tambour pare seul (icône Parade). La machine avance sur le sentier, et non en parcelle 3.
- **Rang 5** (Devant, Assaut, Seuil 2) : l’Abatteuse frappe le sentier au lieu de la parcelle 3 ; non parée, elle n’y trouve rien à couper.
- **Ménage** : le Tambour rentre en main ; le sentier redevient Route et le Bulldozer, qui s’y tenait, se replie en parcelle 1.

*Bilan* : la parcelle 3 n’a reçu aucune des deux frappes qui la menaçaient, et le Bulldozer finit le tour là où il l’avait commencé.

**G7_T2 — plancher (Frayer).** Tour 2, Acte 1, aucune Route en jeu ; le Tapir, construit au Tour 1, porte 1 pari. Rayon M : le Bulldozer, en parcelle 1 (2 Arbres), est révélé au rang 6 ; la parcelle est gardée par 1 Défenseur Mammifère et par le Tambour, posé chez les Mammifères au 1er temps. Après une parade au rang 2, le Tapir s’active et fraye : le Duel quitte la réserve, rejoint le Tambour et arrive face Territoire tenu. Au rang 6 (En avançant, Assaut, Seuil 2 − 1 = 1), la frappe Sur place est parée (Parade) et Territoire tenu interdit l’avancée : le Bulldozer reste en parcelle 1.

---

## 2. Ajustements ciblés

### G5 · L’Iguane vert, dormeur des hautes branches (`R>O`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` — Nature : `ACTION`

*Moteur de lisière R–O (mis à jour)* : Plume de Vigie (O) → Piège là où elle signale ; Bleu (Surchauffe rayonnée par le Toucan) bu → Croc ou second plongeon (R) ‖ Rouge → Bleu sur la cible désignée par la Plume (O) ; Face 2 : 0 Rouge et 2 Bleus = machine calée ; ces Bleus nourrissent l’Iguane *(G6, inchangé)*.

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Piégeage
- **Pictogrammes** : 🪤 Piège autonome · 🪶 Plume de Vigie · 🦷 Croc Reptile · 🔵 Bleu bu (amplificateur)
- **Face 1** : « Piège là où signale la Plume (sinon rayon R ou O) · Bleu bu = le Croc tombe aussi »
- **Face 2** : « Piège + Croc sur toute parcelle ciblée · Bleu bu = second plongeon »
- **Résumé** : *Tombe en Piège au cri des oiseaux.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** L’Iguane vert (*Iguana iguana*), animal entier : grand lézard à la crête dorsale dressée, allongé au soleil sur une branche au-dessus de l’eau, l’œil tourné vers un oiseau qui donne l’alerte.

> *L’Iguane boit la chaleur du jour, immobile des heures durant. Au cri d’alerte des oiseaux, il se laisse tomber de quinze mètres et touche l’eau sans une égratignure : un éclair vert, là où personne ne l’attendait.*

**Face 1 — La chute au cri des oiseaux.** Quand l’Iguane vert s’active, il se laisse tomber : posez 1 Piège sur une parcelle ciblée qui n’en porte pas encore, sur le rayon désigné par la Plume de Vigie, ou visée par une machine du rang qu’elle désigne. Si la Plume n’est pas en jeu ou ne signale aucune parcelle ciblée, il tombe au plus près : sur une parcelle ciblée du rayon Reptile ou du rayon de l’Oiseau. S’il n’y en a aucune, il guette : posez le Piège sur n’importe quelle parcelle sans Piège du rayon Reptile, où il attendra la prochaine frappe.
**Boire la chaleur (amplificateur).** Avant de tomber, vous pouvez boire 1 Bleu : retirez-le d’une machine de n’importe quel rayon et remettez-le dans la réserve (la machine perd la Surchauffe correspondante). Gorgé de chaleur, l’Iguane tombe avec ses mâchoires : si le Croc est dans la réserve Reptile, postez-le sur la parcelle du Piège. Il y pare en premier, le Piège ensuite.

**Face 2 — Le plongeon.** Quand l’Iguane vert s’active, il plonge où il veut : posez 1 Piège sur n’importe quelle parcelle ciblée qui n’en porte pas encore, de n’importe quel rayon, et postez-y le Croc s’il est dans la réserve Reptile (si la Plume de Vigie est face Chaud, prenez le Croc où qu’il se trouve sur le plateau). Le Croc pare en premier, le Piège ensuite.
**Boire la chaleur (amplificateur).** Avant de plonger, vous pouvez boire 1 Bleu (retiré d’une machine de n’importe quel rayon, rendu à la réserve) : l’Iguane plonge une seconde fois et pose 1 second Piège sur une autre parcelle ciblée sans Piège. Chacune de ces parades allume Piégeage.

**Dilemme.** *Choix* : tomber seul là où la Plume l’indique, ou boire un Bleu pour emporter le Croc (Face 1) ou plonger deux fois (Face 2) ; de préférence le Bleu d’une machine déjà annulée, ou dont le Seuil est déjà tombé à 1. *Renoncement* : la machine qui perd son Bleu redevient plus difficile à parer, et ce Bleu manquera au Toucan pour la faire caler ; le Croc emporté ne garde plus la parcelle où une Écaille l’avait posté.

**Double activation.** Chaque Piège qui pare allume Piégeage, l’icône de l’Iguane : la chute appelle la chute, une fois par pari. Deux chutes couvrent les deux parcelles d’un « En avançant » (Sur place et Devant), ou deux fois la même parcelle visée par l’Abatteuse puis le Bulldozer. Avec le Toucan à ses côtés, chaque chute boit son Bleu : le Croc tombe à chaque fois s’il a regagné la réserve (Face 1), et quatre Pièges couvrent la forêt (Face 2).

#### Cas témoins
**G5_T1 — plancher, sans Toucan.** Tour 2, Acte 1 ; le Toucan n’est pas construit : aucun Bleu en jeu. La Plume de Vigie est posée face Chaud au pied du rayon O, dont la parcelle 2 est visée au rang 4 par l’Abatteuse (Sur place) puis au rang 5 par le Bulldozer (Devant). Au rang 1, un Piège gagné en Furtivité pare (Piégeage) : l’Iguane (sur Piégeage, 2 paris) s’active et tombe sur la parcelle 2. Au rang 4, son Piège pare l’Abatteuse (Piégeage) : seconde activation, nouveau Piège sur la même parcelle, qui pare le Bulldozer au rang 5. La parcelle garde ses 2 Arbres.

**G5_T2 — amplifié par le Toucan.** Face 1. Le Toucan a retourné 1 Rouge en Bleu sur l’Abatteuse du rayon M, annulée à l’ouverture par un Rêve. La Plume désigne le rayon R, dont la parcelle 3 est visée au rang 4 par l’Abatteuse et au rang 5 par le Bulldozer. Après une parade de Piège au rang 2, l’Iguane boit le Bleu de la machine annulée (sans dommage : elle ne frappera pas) et tombe avec le Croc sur la parcelle 3 : le Croc pare l’Abatteuse, le Piège pare le Bulldozer (deux fois Piégeage). Le doublé qui aurait changé la parcelle en Route est neutralisé.

---

### G15 · Le Colibri, porteur de gouttes et de pollen (`O>I`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` · `ENRACINEMENT` — Nature : `ACTION`

*Moteur de lisière O–I (mis à jour)* : Insecte (I) transporté à vol d’oiseau (O) vers la parcelle menacée → parade Insecte ; amorçage depuis la réserve ; escale sur un Nid = +1 Insecte ; Plume → dépôt sur la Réglette ; Enracinement voisin bonifié ‖ Nid (I) qui lève le camp à chaque Production, guidé par la Plume de Vigie (O) ; front de raid vers la parcelle visée *(M3, inchangé)*.

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Parade
- **Pictogrammes** : 🐜 Insecte · ➡️ Transport aérien · 🪹 Nid (pollinisation) · 🌱 Enracinement
- **Face 1** : « 1 Insecte pris n’importe où → n’importe quelle parcelle · aucun Insecte en jeu = 1 de la réserve »
- **Face 2** : « 2 Insectes · arrivée sur un Nid = +1 Insecte · Plume près d’un rang = dépôt sur la Réglette »
- **Enraciné** : « Fin de partie : tuiles enracinées voisines, 1 repousse de plus »
- **Résumé** : *Transporte l’Essaim à vol d’oiseau.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Le Colibri (*Phaethornis*, ermite des sous-bois), animal entier : minuscule oiseau en vol stationnaire devant une fleur d’héliconia ; dans la lumière rasante, on devine les acariens des fleurs qui voyagent dans ses narines, de corolle en corolle.

> *Quand la forêt brûla, raconte-t-on, le colibri allait et venait avec une goutte d’eau dans le bec : il faisait sa part. De fleur en fleur, il transporte aussi de minuscules passagers : rien n’est trop petit pour sauver la forêt.*

**Face 1 — Le porteur de gouttes.** Quand le Colibri s’active, il emporte un passager : déplacez 1 Insecte depuis n’importe quel Nid, parcelle, rang de la Réglette ou icône de la Piste des Gardiens vers n’importe quelle parcelle de n’importe quel rayon. Il y participe normalement aux parades (une parade aidée par un Insecte allume l’icône Insecte).
**Amorçage — narines fleuries (plancher).** S’il n’y a encore aucun Insecte en jeu, le Colibri en rapporte un des fleurs : prenez-le dans la réserve de l’Essaim.

**Face 2 — La tournée.** Quand le Colibri s’active, il fait sa tournée : déplacez jusqu’à 2 Insectes, pris n’importe où (Nid, parcelle, rang de la Réglette, icône de la Piste des Gardiens), vers une ou deux parcelles de n’importe quels rayons, où ils participent aux parades. S’il n’y a encore aucun Insecte en jeu, le premier vient de la réserve de l’Essaim.
**Pollinisation.** Si l’un d’eux arrive sur un Nid, ce Nid produit aussitôt 1 Insecte, sans allumer d’icône ni appliquer son pouvoir de Nid.
**Fleur signalée.** Si la Plume de Vigie est posée près d’un rang de la Réglette, vous pouvez déposer l’un de ces passagers sur ce rang plutôt que sur une parcelle : il y servira à une déviation, une lanterne ou un rite.

**Enraciné — La part du colibri.** Au décompte final, chaque autre tuile enracinée au pied de son rayon ou d’un rayon voisin fait repousser 1 Souche de plus.

**Dilemme.** *Choix* : quel Insecte déplacer, et d’où — vider un rang, un Nid ou une icône pour compléter une parade imminente ; en Face 2, faire escale sur un Nid pour le polliniser, ou déposer un passager là où siffle la Plume. *Renoncement* : chaque Insecte emporté laisse un trou ailleurs (une déviation, une Production plus faible, un Bouclier de lisière en moins) ; un passager posé sur la Réglette ne pare rien ce tour-ci.

**Double activation.** Une goutte par activation : la première complète la parade d’une frappe imminente, la seconde ravitaille une autre parcelle ou, en Face 2, pollinise un Nid qui produira +2 à sa prochaine Production. Chaque parade aidée allume Insecte et relance la Piste.

#### Cas témoins
**G15_T1 — amorçage.** Tour 2 : aucun Nid construit, aucun Insecte en jeu. La parcelle 3 du rayon M est visée au rang 4 (Seuil 3) et gardée par 2 Défenseurs. Après une parade au rang 1, le Colibri (sur Parade) s’active : narines fleuries, 1 Insecte de la réserve vole sur cette parcelle. Au rang 4, parade avec cet Insecte défaussé (icône Insecte).

**G15_T2 — pollinisation (Face 2).** Un Nid porte 1 Insecte en parcelle 2 du rayon I ; 1 Insecte attend sur le rang 4 de la Réglette. Le Colibri porte ce dernier sur le Nid (2 Insectes) : pollinisation, +1 (3 Insectes). Son second passager, pris sur l’icône Insecte de la Piste, rejoint la parcelle 3 du rayon O, visée au rang 5. À la Production suivante, le Nid défendu produira +2.

---

### R1 · La Liane des Esprits (`H>E`)

**Identité & Rôles** — Rôles : `AUTONOMIE_A0` · `LEVIER_REVE` · `ENRACINEMENT` — Nature : `ACTION`

*Moteur de lisière H–E (mis à jour)* : Rêve Humain défendu → Rêve des Entités tiré contre lui → bloc contigu vers le Sommeil ; seule, la Liane grimpe ou serre ; Enracinement qui ne ferme pas le Sommeil ‖ Chant (H) assoupli par la loi de la Iara (E) → glissement de Rêve dès la première annulation ; machines laissées au rang envoûtées (Altération) *(R2, inchangé)*.

#### Mini-Tuile Plateau
- **Fenêtre** : OUVERTURE (Rêve, face unique)
- **Pictogrammes** : 🌙 Tuile Rêve · ⬅️ Glissement de Rêve · 🌿 Enroulement · 🌱 Enracinement
- **Règle** : « Rêve des Entités tiré contre la Liane · collé = la paire glisse à gauche · aucun à droite = la Liane grimpe d’1 rang, sinon serre 1 machine de plus »
- **Enraciné** : « Enracinée sans fermer le Sommeil »
- **Résumé** : *Tire un Rêve des Entités contre elle.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Vision chamanique de l’ayahuasca : une liane torsadée qui relie le monde des hommes à celui des esprits ; ses vrilles s’enroulent autour d’un rêve lumineux et l’attirent vers le chamane.

> *On l’appelle la liane des âmes. Celui qui boit sa sève voit les esprits de la forêt, et la liane les tire vers lui, un à un, jusqu’à ce qu’ils dansent ensemble.*

**Règle (face unique).** Quand ce Rêve est défendu, à sa résolution, après ses annulations : la liane s’enroule. Choisissez un Rêve des Entités situé plus à droite sur la Réglette. S’il reste au moins un rang libre entre eux, faites glisser ce Rêve jusqu’au rang libre qui touche la Liane (ses Défenseurs le suivent). S’il touche déjà la Liane, elle l’entraîne : la Liane glisse d’1 rang vers la gauche si ce rang est libre, et ce Rêve glisse d’1 rang à sa suite. Un Rêve déplacé qui n’a pas encore été résolu se résout ensuite depuis sa nouvelle place.
**La liane grimpe (plancher).** S’il n’y a aucun Rêve des Entités à sa droite, la Liane s’enroule sur elle-même : elle glisse d’1 rang vers la gauche si ce rang est libre (ses Défenseurs la suivent ; elle ne se résout pas une seconde fois). Si elle ne peut pas glisser (rang occupé, ou Liane déjà au rang 1), elle serre : elle annule 1 machine de plus sur son rang.

**Enraciné.** La Liane nourrit encore les rêves : contrairement aux autres Rêves enracinés, elle ne rend pas le Sommeil impossible. Au décompte final, elle fait repousser 1 Souche comme toute tuile enracinée.

**Dilemme.** *Choix* : tirer le Rêve des Entités pour combler un trou du bloc, ou faire glisser la paire vers le rang 1 ; seule, grimper vers le bloc ou serrer une machine de plus. *Renoncement* : le Rêve tiré abandonne le rang qu’il couvrait ; une Liane qui grimpe quitte un rang où des machines pourraient encore tomber ; enraciner la Liane lui retire ce pouvoir mais garde le Sommeil possible.

#### Cas témoins
**R1_T1 — l’enroulement.** Liane au rang 3 défendue, Rêve des Entités au rang 6, rangs 4 et 5 libres : le Rêve des Entités glisse au rang 4.

**R1_T2 — plancher.** Tour 2, aucun Rêve des Entités construit. La Liane, au rang 6, défendue par 1 Défenseur, annule la machine de son rang puis grimpe au rang 5. Quelques tours plus tard, collée au rang 2 contre un Rêve Humain au rang 1, elle reçoit 2 machines avec 1 seul Défenseur : elle en annule une, puis serre la seconde.

---

## 3. Passe d’autonomie solo

**Scénario testé.** La tuile est construite en tout premier au Tour 1 et agit au Tour 2, alors qu’aucun autre Gardien, aucun Rêve et aucun Nid n’est en jeu.

| Tuile | Coup dans le vide constaté | Plancher ajouté | Icône de repli |
|---|---|---|---|
| **G4** | Aucun autre pari à pousser ; Résonance ne s’allume jamais seule | *Sentinelle seule* : son 2e pari glisse aussi | Parade |
| **G8** | Aucun Rêve à faire nager ; icône Rêve éteinte | *L’encantado* : 1 Altération | Sabotage |
| **G10** | Aucune annulation de Rêve ; icône Rêve éteinte | *Proie de passage* : machine qui a déjà attaqué | Parade |
| **G13** | Aucun Nid à éventrer ; icône Insecte éteinte | *Termitière sauvage* : 1 Insecte de la réserve | Parade |
| **G14** | Aucun Nid où pondre ; icône Insecte éteinte | *Ponte au sol* (rayon R ou I) | Parade |
| **R6** | Annulation de base intacte, mais ni cueillette ni gant | *Amorçage* : 1 Insecte de la réserve sur son rang | — |
| **R10** | Annulation de base intacte, mais aucune lanterne | *Amorçage* : 1 luciole sur un rang libre | — |

---

### G4 · L’Ara rouge, sentinelle de la collpa (`O>M`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Résonance · *repli, si l’Ara est le premier Gardien construit : Parade*
- **Pictogrammes** : ⭐ Encoche / sécurisation de pari · 🔔 Résonance · ⚔️ Duel (Défi / Territoire tenu)
- **Face 1** : « 1 pari d’un autre Gardien → encoche · Territoire tenu → Défi = 2e cri · seul en piste : son 2e pari glisse aussi »
- **Face 2** : « Un autre Gardien avec pari s’active · Territoire tenu → Défi = 2e réveil · seul en piste : son 2e pari glisse aussi »
- **Résumé** : *Cri d’alarme qui fait avancer les paris.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** L’Ara rouge (*Ara macao*), animal entier : perroquet écarlate, jaune et bleu, agrippé à une falaise d’argile (collpa) au milieu de sa volée, le bec ouvert sur le cri d’alarme.

> *À la collpa, une sentinelle veille pendant que la volée mange l’argile. Au premier danger, son cri déchire l’aube : en un battement d’ailes, toute la forêt est debout.*

**Face 1 — Le cri d’alarme.** Quand l’Ara rouge s’active : faites glisser 1 Défenseur posé en pari sur un autre Gardien construit vers une encoche libre de ce même Gardien. Ce glissement ne résout pas le pouvoir de ce Gardien et n’allume aucune icône. *Écho de la collpa* : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour faire glisser de la même façon un 2e Défenseur, posé en pari sur un Gardien différent du premier.
**Sentinelle seule (plancher).** Si aucun autre Gardien construit ne porte de Défenseur en pari, l’Ara crie pour sa propre volée : faites aussi glisser son second pari, s’il en porte un, dans son encoche encore libre.

**Face 2 — La volée se lève.** Quand l’Ara rouge s’active : choisissez un autre Gardien construit qui porte au moins 1 Défenseur en pari ; il s’active aussitôt (son Défenseur glisse dans une encoche et vous résolvez son pouvoir comme si son icône venait de s’allumer ; s’il s’agit de sa 1re activation du tour, la Résonance la compte). *Écho de la collpa* : si le jeton Duel est face Territoire tenu, vous pouvez le retourner sur Défi pour réveiller de la même façon un 2e Gardien, différent du premier. L’Ara ne se réveille jamais lui-même.
**Sentinelle seule (plancher).** Si aucun autre Gardien construit ne porte de Défenseur en pari, faites aussi glisser le second pari de l’Ara, s’il en porte un, dans son encoche encore libre, sans résoudre son pouvoir une seconde fois.

**Dilemme.** *Choix* : quel pari faire progresser — celui du Gardien le plus en retard, ou celui dont le pouvoir doit frapper maintenant (Face 2). *Renoncement* : retourner le Duel sur Défi pour un 2e cri libère l’avancée des machines de sa parcelle aux rangs 3 et 6 ; construit en premier, l’Ara posé sur Parade s’active seul, mais renonce à la cascade de la Résonance tant qu’il reste en piste.

**Double activation.** Chaque cri fait progresser un pari différent : deux activations bouclent le pari d’un Gardien qui ne s’allume jamais (deux glissements sur la même tuile) ou en sécurisent deux. En Face 2, chaque cri déclenche en plus le pouvoir du Gardien réveillé, et chaque 1re activation ainsi provoquée relance la Résonance. Seul en piste, une seule activation boucle son propre pari de deux Défenseurs.

#### Cas témoins
**G4_T1.** La Matamata porte 1 pari et 0 encoche occupée ; l’Ara s’active : le pari glisse dans l’encoche ; en fin d’attaques, 0 pion sur la Matamata et 1 encoche : pari gagné.

**G4_T2 — plancher.** Tour 2 : l’Ara, construit au Tour 1 et posé sur Parade, est le seul Gardien en piste ; il porte 2 paris. Après une parade au rang 1, il s’active : son 1er pari glisse dans une encoche ; sentinelle seule, le 2nd aussi. En fin d’attaques, 0 pion sur la tuile et 2 encoches occupées : pari gagné, l’Ara passe en Face 2.

---

### G8 · Le Boto, l’encantado du fleuve (`M>E`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` · `LEVIER_REVE` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Rêve · *repli : Sabotage (s’allume sans Rêve, et avant leur résolution)*
- **Pictogrammes** : ⬅️ Déplacement de Rêve · 🌙 Tuile Rêve · 🌀 Jeton Altération
- **Face 1** : « 1 Rêve glisse d’1 rang à gauche ou échange avec son voisin · aucun Rêve ne nage = 1 Altération »
- **Face 2** : « 1 Rêve glisse de 2 rangs ou plonge sous son voisin · ou échange · aucun Rêve ne nage = 1 Altération »
- **Résumé** : *Fait nager les Rêves vers le rang 1.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Le Boto (*Inia geoffrensis*), dauphin rose de l’Amazone, animal entier, glissant entre les troncs d’une forêt inondée ; sur l’eau sombre se reflète la silhouette d’un homme en blanc.

> *Les nuits de fête, dit-on, le Boto sort du fleuve sous les traits d’un bel homme en blanc. Avant l’aube, il replonge vers l’Encante, la cité sous les eaux, et les rêves le suivent dans le courant.*

**Face 1 — La nage.** Quand le Boto s’active : faites nager un Rêve : glissez-le d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent). Si ce rang est occupé, vous pouvez à la place échanger ce Rêve avec le Rêve qui l’occupe (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
**L’encantado (plancher).** Si aucun Rêve ne peut nager (Réglette sans Rêve, ou seul Rêve déjà au rang 1), le Boto envoûte à la place une machine : posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.

**Face 2 — La plongée vers l’Encante.** Quand le Boto s’active : faites glisser un Rêve d’1 ou 2 rangs libres vers la gauche (ses Défenseurs le suivent), ou faites-le plonger sous le Rêve qui le précède : il ressort sur le premier rang libre situé à gauche de celui-ci. Vous pouvez aussi, à la place, échanger deux Rêves voisins (chacun garde ses Défenseurs). Un Rêve déplacé avant sa résolution annule et résout son pouvoir depuis sa nouvelle place ; un Rêve déjà résolu ne se résout pas une seconde fois.
**L’encantado (plancher).** Si aucun Rêve ne peut nager ni plonger, posez 1 jeton d’Altération, pris dans la réserve des Entités, sur une machine mobile qui n’en porte pas encore.

**Dilemme.** *Choix* : faire nager le Rêve vers le rang où des machines viennent d’être révélées (annulation immédiate) ou vers le bloc du Sommeil ; sans Rêve, envoûter la machine qui menacera la parcelle la plus boisée à sa prochaine sortie. *Renoncement* : un Rêve déplacé quitte le rang qu’il couvrait : les machines qui y arriveraient ensuite (déviées ou relues) ne seront plus annulées.

**Double activation.** Deux nages font gagner deux rangs au même Rêve (jusqu’à quatre en Face 2), ou compactent deux Rêves séparés : le plus court chemin vers le Sommeil quand les Humains ne sont pas à la table. Posé sur Rêve, le Boto nage dès la première annulation ; posé sur Sabotage, il déplace les Rêves avant même leur résolution. Sans Rêve, deux envoûtements sur deux machines différentes.

#### Cas témoins
**G8_T1.** Rêve E au rang 5 non résolu, machine révélée au rang 4 ; un Rêve au rang 2 annule et allume Rêve ; le Boto s’active : le Rêve E passe au rang 4 et annule la machine.

**G8_T2 — plancher.** Tour 2 : aucun Rêve construit. Le Boto, construit au Tour 1 et posé sur Sabotage, s’active au premier Sabotage révélé : l’encantado pose 1 Altération sur l’Abatteuse du rayon M, en parcelle 2. Au tour où son jeton est de nouveau tiré, l’Altération est retirée : l’Abatteuse compte dans m(r) mais recule en parcelle 1 sans frapper.

---

### G10 · La Matamata, la souche qui respire (`R>E`)

**Identité & Rôles** — Rôles : `BRIQUE_FLUIDE` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Rêve · *repli : Parade*
- **Pictogrammes** : 🌙 Tuile Rêve · 🚫 Machine annulée · 🪵 Souche · ⭐ Encoche
- **Face 1** : « Machine annulée par un Rêve → jeton avalé hors du sac · sans annulation : machine qui a déjà attaqué · encoche vide au ménage = proie rendue »
- **Face 2** : « Ou machine révélée sur clairière de Souches → annulée et avalée »
- **Résumé** : *Avale un jeton Machine et le garde hors du sac.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** La Matamata (*Chelus fimbriata*), tortue d’eau douce entière, carapace d’écorce et tête frangée de feuilles mortes, immobile au fond d’un ruisseau ambré, la gueule entrouverte.

> *On la prend pour une souche, pour un tas de feuilles mortes. Puis la gueule s’ouvre en un éclair et l’eau s’engouffre : la proie a disparu avant même d’avoir compris.*

**Face 1 — La gueule.** Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture (son jeton est encore incliné devant son rayon). La Matamata l’avale : posez son jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée (elle n’attaque pas) et ne peut pas entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.
**Proie de passage (plancher).** Si aucun Rêve n’a annulé de machine à cette ouverture, la Matamata avale à la place, de la même façon, le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).
*Digestion* : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.

**Face 2 — L’affût de la clairière.** Quand la Matamata s’active : choisissez une machine qu’un Rêve vient d’annuler à cette ouverture, ou une machine révélée qui n’a pas encore attaqué et qui se trouve sur une parcelle réduite à des Souches (aucun Arbre debout). La Matamata l’avale : la seconde est annulée (inclinez son jeton) ; posez ce jeton Machine face cachée sur la Mini-Tuile de la Matamata au lieu de le remettre dans le sac. Tant qu’il y reste, cette machine ne peut pas être tirée ni entrer en Ratissage. La Matamata ne garde qu’une proie : si elle en avale une nouvelle, l’ancienne regagne aussitôt le sac.
**Proie de passage (plancher).** Si aucune de ces deux proies n’existe, la Matamata avale à la place le jeton d’une machine révélée qui a déjà attaqué ce tour (jamais une machine en Ratissage).
*Digestion* : au début du ménage, avant le retour des Défenseurs, si aucune encoche de la Matamata n’est occupée, sa proie regagne le sac ; de même si la Matamata quitte la Piste des Gardiens.

**Dilemme.** *Choix* : garder la même proie tour après tour (en pariant sur la Matamata) ou l’échanger contre une machine plus menaçante. *Renoncement* : pour ne pas digérer, la Matamata exige une encoche occupée à chaque ménage — un Défenseur engagé en pari sur elle plutôt qu’en forêt.

**Double activation.** La première activation avale la proie de l’ouverture ; la seconde peut l’échanger contre une machine plus dangereuse annulée plus à droite, ou (Face 2) avaler une machine posée sur une clairière avant qu’elle ne frappe. Seule en piste, la seconde troque la proie de passage contre la machine la plus proche de la dernière parcelle, pour lui interdire le Ratissage. Chaque activation glisse un pari : or c’est une encoche occupée au ménage qui empêche la Matamata de digérer.

#### Cas témoins
**G10_T1.** Un Rêve au rang 2 annule le Bulldozer du rayon E ; la Matamata (sur Rêve) s’active : jeton avalé ; au tour suivant, le sac contient 2N − 1 jetons Machine.

**G10_T2 — plancher.** Tour 2 : aucun Rêve construit. L’Abatteuse du rayon E a frappé au rang 2 ; au rang 3, une parade allume Parade : la Matamata, construite au Tour 1 et posée sur Parade, s’active et avale le jeton de cette Abatteuse. Au ménage, une encoche de la Matamata est occupée : pas de digestion. Au Tour 3, le sac ne contient que 2N − 1 jetons Machine, et cette Abatteuse ne peut pas entrer en Ratissage.

---

### G13 · Le Tamanoir, le grand mangeur qui épargne (`M>I`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Insecte · *repli : Parade*
- **Pictogrammes** : 🪹 Nid de l’Essaim · 🐜 Insecte · ⚔️ Duel (Défi / Territoire tenu)
- **Face 1** : « Nid à 2 Insectes ou plus · 1 Insecte mangé → riposte de 2 · sans Nid à éventrer : 1 Insecte de la réserve »
- **Face 2** : « Riposte posée sur parcelle ciblée adjacente · parade aidée = Territoire tenu · sans Nid : idem »
- **Résumé** : *Mange un peu, fait riposter beaucoup.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Le Tamanoir (*Myrmecophaga tridactyla*), fourmilier géant entier, longue tête tubulaire et queue en panache, éventrant une termitière de sa griffe ; des soldats jaillissent déjà des galeries.

> *Le Tamanoir avale des dizaines de milliers d’insectes par jour, mais ne s’attarde jamais plus d’une minute sur un même nid : il repart avant l’arrivée des soldats, et le nid survit. Une récolte qui ne détruit pas.*

**Face 1 — La récolte.** Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1 (le Tamanoir ne vide jamais un Nid). L’Essaim riposte aussitôt : ce Nid produit 2 Insectes, sans allumer d’icône ni appliquer son pouvoir de Nid. Ces Insectes restent sur le Nid et participent normalement aux parades sur sa parcelle.
**Termitière sauvage (plancher).** S’il n’existe aucun Nid à éventrer, le Tamanoir fouille une termitière sauvage : prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée, où il participe aux parades.

**Face 2 — La garde dressée.** Quand le Tamanoir s’active : il éventre un Nid construit qui porte au moins 2 Insectes : défaussez-en 1. L’Essaim riposte : ce Nid produit 2 Insectes, sans allumer d’icône, que vous pouvez faire jaillir : posez-les sur la parcelle du Nid ou sur une parcelle ciblée adjacente (même rayon, ou même numéro d’un rayon voisin), où ils participeront aux parades. *La garde dressée* : si le jeton Duel se trouve sur l’une de ces parcelles, une parade aidée par ces Insectes y retourne le Duel sur Territoire tenu, même sans Défenseur Mammifère.
**Termitière sauvage (plancher).** S’il n’existe aucun Nid à éventrer, prenez 1 Insecte dans la réserve de l’Essaim et posez-le sur un Nid construit ou sur une parcelle ciblée ; la garde dressée s’y applique.

**Dilemme.** *Choix* : quel Nid éventrer — celui qui riposte le plus près de la frappe à venir, ou celui qu’il faut regonfler avant la Production. *Renoncement* : l’Insecte mangé manque à une déviation ou à un Bouclier de lisière ; un Nid réduit à 1 Insecte ne peut plus être éventré.

**Double activation.** Deux éventrements, deux ripostes : soit deux Nids différents gonflent à la veille des frappes, soit le même Nid riposte deux fois. En Face 2, chaque riposte jaillit sur la parcelle menacée et fait allumer Insecte à la parade, l’icône du Tamanoir. Sans Nid à éventrer, la seconde termitière sauvage peut porter un Nid tout juste construit jusqu’à ses 2 Insectes.

#### Cas témoins
**G13_T1.** Nid à 3 Insectes ; le Tamanoir s’active : 3 − 1 + 2 = 4 Insectes sur le Nid.

**G13_T2 — plancher.** Tour 2 : aucun Nid construit. La parcelle 2 du rayon M est visée au rang 4 (Assaut, Seuil 2) et gardée par 1 Défenseur. Après une parade au rang 1, le Tamanoir (sur Parade) s’active : termitière sauvage, 1 Insecte de la réserve sur cette parcelle. Au rang 4, parade avec 1 Défenseur et l’Insecte défaussé (icône Insecte).

---

### G14 · Le Téju, la ponte au cœur de la termitière (`R>I`)

**Identité & Rôles** — Rôles : `CATALYSEUR_EVEIL` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : ACTIVATION · **Icône conseillée** : Insecte · *repli : Parade*
- **Pictogrammes** : 🦎 Écaille · 🪹 Nid de l’Essaim · 🦷 Croc Reptile · 🪤 Piège autonome
- **Face 1** : « Écaille sous un Nid (sans Nid libre : au sol, rayon R ou I) · frappe → le Croc éclot et pare »
- **Face 2** : « Le Croc éclot d’où qu’il soit et pare chaque frappe jusqu’au ménage »
- **Résumé** : *Pond une Écaille au cœur d’un Nid.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Le Téju (*Tupinambis teguixin*), grand lézard entier à la robe noire et dorée, griffant la paroi d’une termitière pour y pondre ; à ses pieds, la litière de feuilles où s’enfouissent les pontes sans abri.

> *La femelle Téju éventre une termitière vivante, y pond, puis s’en va : les termites réparent le mur et scellent les œufs dans une couveuse parfaite. Celui qui viendra détruire le nid y trouvera, à l’éclosion, des mâchoires toutes neuves.*

**Face 1 — La ponte.** Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. *Éclosion* : quand une machine frappe la parcelle de ce Nid et que le Croc est dans la réserve Reptile, la ponte éclot avant toute parade : postez le Croc sur cette parcelle ; il pare cette frappe en premier (allumez Piégeage) puis regagne la réserve, et l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
**Ponte au sol (plancher).** S’il n’existe aucun Nid construit sans ponte, le Téju pond dans la litière : posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte. Elle éclot de la même façon quand une machine frappe cette parcelle, et regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois : pondre de nouveau au sol la déplace.

**Face 2 — La nichée.** Quand le Téju s’active : il pond : prenez 1 Écaille dans la réserve Reptile (ou une Écaille révélée à cette ouverture) et glissez-la face cachée sous un Nid construit qui n’abrite pas encore de ponte. *La nichée* : quand une machine frappe la parcelle de ce Nid, la ponte éclot avant toute parade : postez le Croc sur cette parcelle, où qu’il se trouve (réserve Reptile ou autre parcelle) ; il pare cette frappe en premier (allumez Piégeage) et, au lieu de regagner la réserve, reste sur place pour parer de même chaque frappe suivante sur cette parcelle jusqu’au ménage, où il regagne la réserve tandis que l’Écaille de la ponte rejoint le sac. Un Nid qui se déplace emporte sa ponte ; un Nid renvoyé en lisière la rend à la réserve Reptile.
**Ponte au sol (plancher).** S’il n’existe aucun Nid construit sans ponte, posez l’Écaille face cachée au bord d’une parcelle du rayon Reptile ou du rayon Insecte : la nichée y éclot de la même façon, et l’Écaille regagne la réserve Reptile si cette parcelle devient Route. Une seule ponte au sol à la fois.

**Dilemme.** *Choix* : sous quel Nid pondre — celui dont la parcelle est visée ce tour, ou un Nid exposé à long terme près du cœur ; sans Nid, quelle parcelle couver. *Renoncement* : l’Écaille couvée n’est plus dans le sac tant qu’elle n’a pas éclos (moins de Sabotages tirés) ; un Croc parti éclore ne protège plus la parcelle où une Écaille l’avait posté.

**Double activation.** Chaque activation installe une ponte sous un Nid différent : deux Nids protégés, deux éclosions possibles, deux icônes Piégeage. En Face 2, une seule ponte suffit à tenir une parcelle pendant toute la phase d’attaques. Sans Nid, la seconde activation déplace la ponte au sol vers la parcelle la plus menacée.

#### Cas témoins
**G14_T1.** Ponte sous le Nid de la parcelle 2 du rayon I ; le Bulldozer frappe cette parcelle ; le Croc est en réserve : éclosion, parade du Croc (Piégeage), Écaille au sac.

**G14_T2 — plancher.** Tour 2 : aucun Nid construit. Après une parade au rang 1, le Téju (sur Parade) s’active : ponte au sol, 1 Écaille de la réserve Reptile posée face cachée au bord de la parcelle 2 du rayon R. Au rang 4, l’Abatteuse frappe cette parcelle ; le Croc est en réserve : éclosion, le Croc pare (Piégeage) puis regagne la réserve ; l’Écaille rejoint le sac.

---

### R6 · Le Rite de la Tucandeira (`H>I`)

**Identité & Rôles** — Rôles : `AUTONOMIE_A0` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : OUVERTURE (Rêve, face unique)
- **Pictogrammes** : 🌙 Tuile Rêve · 🐜 Insecte · 🚫 Machine annulée
- **Règle** : « 1 Insecte du rayon Humain → son rang (aucun en jeu : de la réserve) · chaque Insecte défaussé = 1 annulation de plus »
- **Résumé** : *L’Essaim multiplie les annulations du Rêve.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** Vision rituelle : les gants tressés de fourmis tucandeiras du rite de passage, portés par un jeune initié qui danse ; à ses pieds, les fourmis fraîchement cueillies en forêt.

> *Chez les Sateré-Mawé, pour devenir adulte, il faut glisser ses mains dans des gants grouillant de tucandeiras et danser malgré la douleur. Celui qui endure porte la force de l’Essaim.*

**Règle (face unique).** Quand ce Rêve est défendu, à sa résolution : *la cueillette* : vous pouvez d’abord déplacer 1 Insecte d’une parcelle du rayon Humain vers le rang de ce Rêve.
**Amorçage — cueillette sauvage (plancher).** S’il n’y a encore aucun Insecte en jeu, prenez-le dans la réserve de l’Essaim.
Puis *le gant de tucandeiras* : en plus d’1 machine par Défenseur, ce Rêve annule 1 machine supplémentaire de son rang pour chaque Insecte que vous défaussez de ce rang.

**Dilemme.** *Choix* : combien d’Insectes offrir au gant — un par machine qui resterait sinon active sur le rang. *Renoncement* : les Insectes consumés au rite ne dévieront plus de dés et ne pareront plus de frappes.

#### Cas témoins
**R6_T1.** Rêve au rang 1 défendu par 1 Défenseur ; 3 machines au rang 1 et 2 Insectes sur ce rang : 3 machines annulées (1 + 2), 2 Insectes défaussés.

**R6_T2 — plancher.** Tour 2 : aucun Nid construit, aucun Insecte en jeu. Le Rite, au rang 3, est défendu par 1 Défenseur ; 2 machines y sont révélées. Cueillette sauvage : 1 Insecte de la réserve sur le rang 3 ; le gant annule les 2 machines (1 + 1) et l’Insecte est défaussé.

---

### R10 · La Mère des Lucioles (`E>I`)

**Identité & Rôles** — Rôles : `AUTONOMIE_A0` · `TWIST_2K3` · `LEVIER_REVE` — Nature : `ACTION`

#### Mini-Tuile Plateau
- **Fenêtre** : OUVERTURE (Rêve, face unique)
- **Pictogrammes** : ⚡ Brique-Twist 2K3 · 🐜 Insecte · 🚫 Machine annulée · ⬅️ Glissement de Rêve
- **Règle** : « Rang libre avec Insecte = lanterne · aucun en jeu : 1 luciole de la réserve · 1 Insecte défaussé annule 1 machine · puis glisse d’1 rang »
- **Résumé** : *Les rangs vides deviennent des lanternes.*

#### Grande Carte Joueur
**Entité illustrée & brief visuel.** La Mère des Lucioles, esprit-lanterne de la forêt nocturne : une silhouette faite de milliers de points lumineux, penchée sur un chemin de lumière.

> *Là où aucun rêve ne veille, la Mère des Lucioles allume ses lanternes. Les égarés suivent ces lumières et rentrent chez eux ; les machines, elles, s’arrêtent, aveuglées, au milieu du chemin.*

**Règle (face unique).** Quand ce Rêve est défendu, à sa résolution : les lanternes s’allument.
**Amorçage — première luciole (plancher).** S’il n’y a encore aucun Insecte en jeu, posez d’abord 1 Insecte de la réserve de l’Essaim sur un rang de la Réglette libre de tout Rêve.
Chaque rang laissé libre de tout Rêve et portant au moins 1 Insecte devient une lanterne : pour chaque machine révélée et non annulée sur un tel rang, vous pouvez défausser 1 Insecte de ce rang pour l’annuler (inclinez son jeton). Ces annulations comptent comme celles de ce Rêve. *Le chemin de lumière* : si au moins une lanterne a annulé une machine, ce Rêve glisse ensuite d’1 rang vers la gauche si ce rang est libre (ses Défenseurs le suivent), au risque d’éteindre la lanterne qui s’y trouvait.

*Note éditoriale* : « Le sentier de lumière » devient « Le chemin de lumière », pour réserver le mot *sentier* à l’état créé par le Tapir.

**Dilemme.** *Choix* : laisser volontairement des rangs libres de tout Rêve pour y allumer des lanternes, ou compacter les Rêves vers le Sommeil. *Renoncement* : chaque rang occupé par un Rêve éteint une lanterne ; chaque Insecte consumé ne déviera plus de dé.

#### Cas témoins
**R10_T1.** Mère des Lucioles défendue au rang 5 ; le rang 1, libre, porte 2 Insectes et reçoit 2 machines : 2 annulations par la lanterne, puis le Rêve glisse au rang 4.

**R10_T2 — plancher.** Tour 2 : aucun Nid construit, aucun Insecte en jeu. La Mère des Lucioles, au rang 6, est défendue ; un Bulldozer est révélé au rang 2, libre de tout Rêve. Première luciole : 1 Insecte de la réserve sur le rang 2 ; la lanterne annule le Bulldozer (Insecte défaussé), puis le Rêve glisse au rang 5.

---

## 4. Contrôle des Murs et des invariants

| Tuile | Mur 1 · 0 repousse active | Mur 2 · Rouge → Bleu | Mur 3 · 2-2-3-3 & icône | Mur 4 · plancher solo |
|---|---|---|---|---|
| **G7** | Repousse au seul décompte final (Enraciné) | — | Aucun pion Arbre ou Souche déplacé ; le sentier requalifie une Route sans pièce ajoutée | *Frayer*, toujours jouable |
| **G5** | — | Bleu seulement retiré d’une machine, jamais posé | — | Piège garanti (Plume, puis rayon R ou O, puis guet) |
| **G15** | Pollinisation = +1 Insecte, plus aucune Souche retournée | — | — | Amorçage depuis la réserve |
| **R1** | — | — | — | La liane grimpe ou serre |
| **G4** | — | — | Icône de repli choisie à la construction | Sentinelle seule |
| **G8** | — | — | Repli Sabotage | L’encantado (Altération) |
| **G10** | — | — | Repli Parade | Proie de passage |
| **G13** | — | — | Repli Parade | Termitière sauvage |
| **G14** | — | — | Repli Parade ; ponte posée au bord de la parcelle, sans toucher aux pions | Ponte au sol |
| **R6** | — | — | — | Cueillette sauvage |
| **R10** | — | — | — | Première luciole |

**Invariants**
- **I01** : chaque plancher puise dans le socle, dans le Peuple d’origine ou chez le voisin de lisière (Plume pour G5 ; Altération pour G8 ; Écailles pour G14 ; Insectes de la réserve pour G13, G15, R6 et R10, toutes sur une lisière de `I`). Aucun plancher ne suppose la jumelle.
- **I02** : R1, R6 et R10 restent sans aucune dépendance à un Gardien.
- **I03** : G7 (Route → sentier) et R3 (Défenseurs du Rêve qui bondissent) gardent des sorties principales distinctes, sans boucle fermée.
- **I04** : catalyseurs inchangés (G1, G3, G4, G5, G8, G9, G11, G12, G13, G14, G15 = 11 ≥ 9).
- **I05** : leviers de Rêve inchangés sur `E–M` (G8), `E–R` (R8), `E–O` (R9), `E–I` (R10).
- **I06** : 4 synergies d’Enracinement `{G3, G7, G15, R1}`.
- **`mem_debt = 0`** : sentier porté par le Duel ou un Chamane ; ponte au sol par une Écaille ; proie par un jeton Machine ; envoûtement par un jeton d’Altération.

**À arbitrer avant la Passe 2**
1. **Plafond d’activation.** Ces fiches supposent qu’un Gardien ne s’active qu’en faisant glisser un pari, donc deux fois par tour au plus. Si le socle autorise des activations sans pari, les boucles de l’Iguane et du Téju demanderont un verrou explicite.
2. **Moment du décompte final.** L’Enraciné du Tapir le lit en fin d’Étape 5, avant le ménage, quand le Tambour et le Chant sont encore posés.
3. **Amorçage de l’Essaim.** G15, R6 et R10 partagent désormais la même clause ; la Passe 2 pourra la figer sous un mot-clé unique de Mini-Tuile.