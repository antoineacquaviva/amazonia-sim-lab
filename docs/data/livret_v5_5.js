// =========================================================================
// data/livret_v5_5.js — Livret de Règles Joueur & Synthèse Cœur (Amazonia v5.5)
// =========================================================================

const REGLES_COEUR_SYNTHESE = {
  "but_et_format": "Jeu coopératif asymétrique à communication muette (3 à 6 joueurs parmi Mammifères, Reptiles, Oiseaux, Humains, Entités Magiques, Insectes ; 8 tours maximum). Objectif commun : maximiser le nombre d'Arbres debout après la Repousse Finale (plafonnée à la dotation initiale de chaque parcelle). Réserves de jetons et de cartes Sabotage illimitées.",
  "principes_transverses": {
    "gouvernance_unitaire": "Chaque Tuile de Synergie (Gardien, Rêve ou Nid) et chaque piste de Migration est décidée uniquement par le joueur de son Peuple d'origine. Les cartes Sabotage sont toutes identiques et diluent définitivement le paquet Machine.",
    "communication_muette": "Silence tactique complet tant que les paravents sont fermés : seuls les placements et ajustements visibles de vos Défenseurs communiquent vos intentions jusqu'à l'ouverture simultanée des paravents.",
    "pont_routier": "Le long d'un rayon de Forêt, toute Route Forestière est sautée automatiquement : viser devant, avancer, reculer ou migrer désignent toujours la prochaine parcelle non rasée dans cette direction. Latéralement entre Forêt et Furtivité, une Route Forestière est infranchissable et inoccupable.",
    "cascades_gardiens": "Terminez intégralement l'action ou la tuile en cours avant de parcourir la Piste des Gardiens de la case 1 à la case 6. Chaque événement allume au plus un seul déclencheur : à l'ouverture des paravents, Sabotage prime sur Insecte (déviation sur la Piste des Tactiques), qui prime sur Rêve ; pendant les attaques, Piégeage prime sur Insecte (Parade avec dépense d'au moins un Insecte), qui prime sur Parade par Défenseurs seuls ; la case 4. Gardien s'allume à la première ouverture du tour de chaque autre Gardien distinct (sans boucle sur elle-même) ; la Furtivité et la production des Nids n'allument aucun déclencheur."
  },
  "topologie_et_seuils_imprimes": {
    "roue": "N rayons de Forêt (de la bordure vers le cœur) alternés avec N lisières portant chacune 2 Tuiles de Synergie et une Piste de Furtivité à 4 emplacements jumeaux par case.",
    "dotations": "Chaque parcelle porte une dotation initiale d'Arbres égale à son Seuil imprimé fixe (4 ou 5 parcelles par rayon selon la topologie choisie).",
    "piste_tactiques": "Piste fixe de 6 cases imprimées en dur (T1 à T6). Les Rêves se posent par-dessus depuis la droite (case 6 puis 5, etc.) sans déplacer ni retirer les Tactiques imprimées.",
    "reveil_de_la_foret": "Actif dès qu'au moins un Peuple Animal Sauvage (Mammifères, Reptiles ou Oiseaux) participe à la partie. Chaque Gardien construit peut recevoir 0, 1 ou 2 Défenseurs en pari d'activation, glissés sous la tuile à chaque déclenchement. À la fin des attaques : si tous ses Défenseurs ont été glissés, le pari est gagné (le Gardien reste en piste et passe sur sa Face 2 s'il est double-face) ; s'il reste au moins un Défenseur dessus, le pari est perdu (le Gardien retourne en lisière Face 1, sauf si un Insecte présent sur sa case est défaussé en Bouclier de lisière pour le maintenir sur sa face actuelle, le pari restant perdu). Aux Tours 1 à 7, si les N joueurs ont tous engagé un Défenseur sur la Piste des Gardiens et qu'aucun pari n'est perdu, le Réveil de la Forêt met fin à la partie."
  },
  "sequence_tour_6_etapes": {
    "1_preparation": "Passage définitif en Ratissage pour toute machine présente sur la dernière parcelle non rasée de son rayon (+1 puissance imprimée et Tactique T1 Sur place). Distribution secrète d'une carte par joueur depuis le paquet Machine (en cas de pénurie, dans le sens horaire à partir du Peuple ayant le plus d'Arbres debout). Sous paravent fermé, chaque joueur ayant reçu une carte Machine lance 2 dés et retient la plus petite valeur (désignant le rang 1 à 6 sur la Piste des Tactiques) ; une carte Sabotage neutralise l'activation.",
    "2_pose_defenseurs": "Sous paravent fermé, chaque joueur place d'abord l'un de ses deux Défenseurs de façon irrévocable sur sa propre Forêt ou ses deux lisières, puis son autre Défenseur librement sur tout le plateau (d'abord face Réflexion avec ajustements muets, puis retourné face Définitif), y compris sur un Rêve pour activer son annulation ou en pari sur un Gardien construit (0, 1 ou 2 Défenseurs maximum par Gardien). Sur une case de Furtivité (4 emplacements jumeaux), entrer sur une rive attire aussitôt l'éventuel partenaire sur l'emplacement jumeau du même bord ; retourner son jeton en face Définitif se fait sur place.",
    "3_construction_et_revelation": "Construction obligatoire avant l'ouverture des paravents dès que 2 Défenseurs sont réunis sur une tuile de lisière (Gardien sur une case libre 1 à 6 ; Rêve par-dessus la case libre la plus à droite de la Piste des Tactiques ; Nid sur une parcelle non rasée sans machine ni autre Nid). Ouverture simultanée des paravents et fin du silence : résolution des cartes Sabotage, des déviations d'Insectes sur la Piste des Tactiques (±1 rang), puis des Rêves (chaque Défenseur posé sur un Rêve annule une machine pointant sur ce rang ; le Rêve avance d'un rang vers la gauche uniquement si toutes les machines de ce rang sont annulées).",
    "4_furtivite_nids_migration": "Furtivité : chaque binôme complet (2 Défenseurs sur la même rive, ou 1 Défenseur + 1 Insecte défaussé) réalise une action sur la parcelle en face — poser un Piège si aucune machine n'est présente, ou acquérir une carte Sabotage si au moins une machine inactive y stationne. Production des Nids : chaque Nid portant au moins un Défenseur crée 1 Insecte (ou 2 si au moins 2 Insectes y sont déjà) puis applique son effet propre en bloc indivisible. Migration : chaque Insecte peut se déplacer de 0 ou 1 cran (aller simple définitif depuis la dernière parcelle non rasée vers une case 1 à 6 de la Piste des Tactiques ou de la Piste des Gardiens).",
    "5_attaques_et_verdict": "Les machines agissent dans l'ordre des Tactiques 1 à 6 puis en Ratissage (Abatteuse avant Bulldozer sur un même rayon). Chaque machine lit ses cibles depuis sa position réelle et résout ses frappes selon la chaîne stricte : effets spéciaux, puis Piège armé (dès que la Défense totale vaut au moins 1), puis Parade classique (Défenseurs seuls ou complétés par la défausse immédiate des Insectes manquants). Dégâts non parés : Abatteuse coupe 2 Arbres en Souches ; Bulldozer coupe 1 Arbre en Souche et retire toutes les Souches non protégées (si 0 Arbre et 0 Souche, la parcelle devient une Route Forestière et les machines se replient vers la bordure). Fin des attaques : retrait des Pièges déclenchés, verdict des paris Gardiens (avec Bouclier de lisière éventuel) et test de fin de partie (priorité absolue au Tour 8 ; aux Tours 1 à 7 : Sommeil du Contremaître ou Réveil de la Forêt).",
    "6_fin_de_tour": "Retour en main de tous les Défenseurs, remise à zéro des effets temporaires, passage du marqueur Coordonnateur au joueur suivant et remélange du paquet Machine (hors machines en Ratissage) avec toutes les cartes Sabotage."
  },
  "supports_et_grammaire": {
    "declencheurs_gardiens_6": "1: Parade, 2: Piégeage, 3: Sabotage, 4: Gardien, 5: Rêve, 6: Insecte."
  }
};

function renderDidacticRulebook() {
  const n = state.peuplesCercle.length;
  const c = state.chassis;
  const { lisieres } = getActiveLisieresAndTiles();
  const topoSpec = TOPOLOGIES_PISTE_SPEC[c.Profil_Piste] || TOPOLOGIES_PISTE_SPEC.P4_2233;
  const totalArbres = n * topoSpec.somme;
  const pMax = topoSpec.p_max;
  const configNum = computeConfigurationIndex();
  const totalConfigs = CHASSIS_AXES_SPEC.reduce((acc, ax) => acc * ax.options.length, 1);

  const nbAnimauxSauvages = state.peuplesCercle.filter(p => p === 'M' || p === 'R' || p === 'O').length;
  const reveilActif = nbAnimauxSauvages >= 1;
  const nbPeuplesOniriques = state.peuplesCercle.filter(p => p === 'H' || p === 'E').length;
  const nbRevesEnJeu = 2 * nbPeuplesOniriques;
  const hasInsectes = state.peuplesCercle.includes('I');

  const placementTxt = c.Placement_Initial_Machines === 'BULLDOZER_P1_ABATTEUSE_P2'
    ? 'placez le <strong>Bulldozer sur la parcelle 1</strong> (bordure) et l’<strong>Abatteuse sur la parcelle 2</strong> de chaque rayon'
    : 'placez l’<strong>Abatteuse et le Bulldozer ensemble sur la parcelle 1</strong> (bordure) de chaque rayon';

  const seuilOffsetTxt = Number(c.Offset_Seuil_Parade) === 1
    ? '<strong>Seuil imprimé + 1 + jetons Puissance rouges − jetons Surchauffe bleus + modificateur de Tactique</strong>'
    : '<strong>Seuil imprimé + jetons Puissance rouges − jetons Surchauffe bleus + modificateur de Tactique</strong>';

  const abatteuseTxt = c.Role_Abatteuse_Fin_De_Piste === 'ARRACHE_1_SOUCHE_SI_SANS_ARBRE'
    ? 'coupe jusqu’à <strong>2 Arbres debout</strong> en Souches ; lorsqu’elle attaque en <strong>Ratissage</strong> sur une parcelle qui ne possède plus aucun Arbre debout, elle arrache <strong>1 Souche</strong>'
    : 'coupe jusqu’à <strong>2 Arbres debout</strong> en Souches (elle laisse les Souches intactes)';

  const synergieMachineTxt = c.Synergie_Binome_Machines === 'MUTUALISATION_PUISSANCE_MEME_PARCELLE'
    ? 'Lorsque les deux machines d’un même rayon occupent la même parcelle au moment de l’attaque, la machine active additionne ses propres jetons rouges et ceux de sa partenaire.'
    : 'Chaque machine attaque avec sa propre puissance, indépendamment de l’autre machine de son rayon.';

  const reveMultiTxt = c.Regle_Ouverture_Reve_Multiple === 'PAR_DE_M_DESIGNE'
    ? 'Si un Rêve annule plusieurs machines au cours du même tour, son pouvoir s’applique une fois pour chaque machine annulée.'
    : 'Un Rêve n’applique son pouvoir propre qu’une seule fois par tour, même s’il annule plusieurs machines ce tour-ci.';

  const bugProf = typeof getMigrationProfile === 'function'
    ? getMigrationProfile('tactiques')
    : { nom: 'Déviation de dé', texte: 'Défaussez 1 Insecte de la case visée pour décaler le dé d’une machine de −1 ou +1 rang (entre 1 et 6).' };
  const colonieProf = typeof getMigrationProfile === 'function'
    ? getMigrationProfile('gardiens')
    : { nom: 'Bouclier de lisière', texte: 'Défaussez 1 Insecte de la case d’un Gardien ayant perdu son pari pour le garder sur sa case et sur sa face actuelle (le pari reste perdu).' };

  const tableSummary = state.peuplesCercle.map(code => `${PEUPLES[code].icon} ${PEUPLES[code].nom}`).join(' · ');
  const dotationStr = topoSpec.dotation.join(' – ');

  const container = document.getElementById('rulebook-article');
  container.innerHTML = `
    <!-- EN-TÊTE ÉDITORIAL -->
    <header class="border-b-4 border-forest-800 pb-6 mb-8">
      <div class="flex flex-wrap items-start justify-between gap-4">
        <div>
          <div class="text-xs font-semibold uppercase tracking-[0.18em] text-forest-700 mb-1">
            Livret de Règles Officiel · Édition v5.5
          </div>
          <h1 class="text-3xl sm:text-4xl font-bold text-forest-950 tracking-tight">
            AMAZONIA : DERNIER REMPART
          </h1>
          <p class="text-sm text-slate-600 mt-1.5 font-medium">
            Jeu coopératif asymétrique à communication silencieuse · <strong>3 à 6 joueurs</strong> · <strong>8 tours maximum</strong>
          </p>
        </div>
        <div class="bg-forest-50 border border-forest-200 rounded-xl px-4 py-3 text-xs text-forest-900 space-y-1">
          <div><strong class="text-forest-800">Table configurée :</strong> <span class="dyn-span">${n} joueurs</span></div>
          <div><strong class="text-forest-800">Forêt initiale :</strong> <span class="dyn-span">${totalArbres} Arbres (${pMax} parcelles : ${dotationStr})</span></div>
          <div><strong class="text-forest-800">Réglage de table :</strong> #${configNum} / ${totalConfigs}</div>
        </div>
      </div>

      <div class="mt-4 bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-xs text-slate-700 flex flex-wrap items-center justify-between gap-2">
        <div><strong>Peuples autour de la table :</strong> <span class="dyn-span">${tableSummary}</span></div>
        <div class="flex flex-wrap gap-2">
          <span class="px-2 py-0.5 rounded-full ${reveilActif ? 'bg-amber-100 text-amber-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${reveilActif ? `🐾 Gardiens & Réveil actifs (${nbAnimauxSauvages} Peuple${nbAnimauxSauvages > 1 ? 's' : ''})` : '🐾 Sans Animaux Sauvages'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${nbRevesEnJeu > 0 ? 'bg-purple-100 text-purple-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${nbRevesEnJeu > 0 ? `🌙 ${nbRevesEnJeu} Rêves en jeu` : '🌙 Sans Peuples Oniriques'}
          </span>
          <span class="px-2 py-0.5 rounded-full ${hasInsectes ? 'bg-lime-100 text-lime-900' : 'bg-slate-200 text-slate-600'} font-semibold">
            ${hasInsectes ? '🐜 Peuple Insectes présent' : '🐜 Sans Insectes'}
          </span>
        </div>
      </div>
    </header>

    <!-- =================================================================== -->
    <!-- 1. PRÉSENTATION & OBJECTIF                                          -->
    <!-- =================================================================== -->
    <section id="sec-presentation" class="mb-10">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        1. Présentation &amp; Objectif
      </h2>

      <p class="text-sm text-slate-700 leading-relaxed mb-3">
        Les engins du Contremaître encerclent la grande forêt amazonienne. De chaque lisière, Abatteuses et Bulldozers s’enfoncent vers le cœur sacré, transformant les arbres centenaires en souches puis en routes de terre battue. Face à cette avancée implacable, les <strong>Peuples de la forêt</strong> — Mammifères, Reptiles, Oiseaux, Humains, Entités Magiques et Insectes — unissent leurs forces dans un silence tendu.
      </p>

      <p class="text-sm text-slate-700 leading-relaxed mb-4">
        <strong>Amazonia : Dernier Rempart</strong> est un jeu <strong>entièrement coopératif</strong>. Vous gagnez ou perdez ensemble autour d’un score commun : le <strong>nombre total d’Arbres encore debout à la fin de la partie, après la Repousse Finale</strong>. Chaque parcelle sauvée, chaque souche préservée des bulldozers et chaque tour gagné sur les machines comptent dans le bilan de la forêt.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mb-4 text-xs">
        <div class="bg-forest-50 border border-forest-200 rounded-xl p-3.5">
          <div class="font-bold text-forest-900 mb-1">⏳ Fin du 8<sup>e</sup> tour</div>
          <p class="text-slate-600">Tenez tête au Contremaître jusqu’au terme du 8<sup>e</sup> tour. Plus votre canopée aura résisté, plus votre score sera élevé.</p>
        </div>
        <div class="bg-purple-50 border border-purple-200 rounded-xl p-3.5">
          <div class="font-bold text-purple-900 mb-1">🌙 Sommeil du Contremaître</div>
          <p class="text-slate-600">Rassemblez toutes les tuiles Rêve de la partie en un bloc continu à gauche de la Piste des Tactiques pour endormir les machines avant le 8<sup>e</sup> tour.</p>
        </div>
        <div class="bg-amber-50 border border-amber-200 rounded-xl p-3.5">
          <div class="font-bold text-amber-900 mb-1">🌿 Réveil de la Forêt</div>
          <p class="text-slate-600">Engagez tous ensemble vos Défenseurs sur la Piste des Gardiens et remportez chaque pari du tour pour chasser les machines avant le 8<sup>e</sup> tour.</p>
        </div>
      </div>

      <div class="bg-emerald-50 border-l-4 border-emerald-600 rounded-r-xl p-3.5 text-xs text-emerald-950">
        <div class="font-bold uppercase tracking-wider text-emerald-800 mb-1">✨ Règle d’or — Gouvernance fluide, zéro débat interminable</div>
        <p>Chaque Tuile de Synergie (Gardien, Rêve ou Nid) et chaque piste d’Insectes appartient à un unique <strong>Peuple d’origine</strong>. Dès que son effet se déclenche, seul le joueur contrôlant ce Peuple tranche immédiatement le choix à faire. Les autres joueurs respectent sa décision et le rythme reste vif.</p>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 2. MATÉRIEL & MISE EN PLACE                                         -->
    <!-- =================================================================== -->
    <section id="sec-materiel" class="mb-10">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        2. Matériel &amp; Mise en place
      </h2>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-5 text-sm">
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
          <h3 class="font-bold text-forest-900 mb-2">🌳 Le plateau circulaire</h3>
          <ul class="space-y-1.5 text-xs text-slate-700 list-disc pl-4">
            <li><strong>${n} rayons de Forêt</strong> (un par joueur), composés chacun de <span class="dyn-span"><strong>${pMax} parcelles</strong></span> allant de la <strong>parcelle 1 (bordure)</strong> jusqu’à la <strong>parcelle ${pMax} (cœur)</strong>.</li>
            <li>Chaque parcelle affiche un chiffre gravé : c’est à la fois sa <strong>dotation initiale d’Arbres</strong> et son <strong>Seuil de Parade imprimé</strong> (<span class="dyn-span">${dotationStr}</span>, soit <span class="dyn-span"><strong>${totalArbres} Arbres</strong></span> pour toute la table).</li>
            <li><strong>${n} lisières</strong> séparent les joueurs voisins. Chacune porte une <strong>Piste de Furtivité</strong> parallèle aux parcelles (chaque case possède <strong>4 emplacements jumeaux</strong> : 2 côté joueur de gauche, 2 côté joueur de droite) et accueille en bordure <strong>2 Tuiles de Synergie</strong> communes aux deux Peuples voisins.</li>
          </ul>
        </div>
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4">
          <h3 class="font-bold text-forest-900 mb-2">🧭 Les pistes centrales &amp; le matériel</h3>
          <ul class="space-y-1.5 text-xs text-slate-700 list-disc pl-4">
            <li><strong>Piste des Tactiques (fixe) :</strong> 6 cases numérotées <strong>1 à 6</strong> portant de façon permanente les 6 Tactiques des machines (<code>T1</code> à <code>T6</code>).</li>
            <li><strong>Piste des Gardiens (fixe) :</strong> 6 cases numérotées <strong>1 à 6</strong> correspondant aux 6 déclencheurs de la partie (<em>1. Parade, 2. Piégeage, 3. Sabotage, 4. Gardien, 5. Rêve, 6. Insecte</em>).</li>
            <li><strong>Par joueur :</strong> 1 paravent, 2 dés à 6 faces et <strong>2 jetons Défenseur</strong> double face (un côté <em>Réflexion</em>, un côté <em>Définitif</em>).</li>
            <li><strong>Machines &amp; Réserves :</strong> 1 Abatteuse et 1 Bulldozer double face (face normale / face <em>Ratissage</em>) par rayon, les cartes Machine correspondantes, ainsi que des réserves illimitées d’Arbres/Souches, Pièges, Insectes, jetons Puissance (face rouge / face bleue <em>Surchauffe</em>) et cartes Sabotage identiques.</li>
          </ul>
        </div>
      </div>

      <h3 class="text-base font-bold text-forest-900 mb-2">Mise en place en 5 gestes</h3>
      <ol class="space-y-1.5 text-sm text-slate-700 list-decimal pl-5 mb-5">
        <li><strong>Formez le cercle de la forêt :</strong> chaque joueur choisit un Peuple et s’installe face à son rayon. Garnissez chaque parcelle de sa dotation initiale d’Arbres (<span class="dyn-span">${dotationStr}</span>).</li>
        <li><strong>Placez les Tuiles de Synergie en lisière :</strong> entre chaque paire de Peuples voisins, posez face visible (Face 1) les 2 Tuiles de Synergie correspondantes (voir le tableau ci-dessous pour votre table).</li>
        <li><strong>Installez les Machines :</strong> <span class="dyn-span">${placementTxt}</span>, toutes sur leur face normale et sans jeton Puissance.</li>
        <li><strong>Composez le paquet Machine :</strong> réunissez les <strong>${2 * n} cartes Machine</strong> (Abatteuse et Bulldozer de chaque rayon), mélangez-les face cachée et placez la réserve de cartes Sabotage à proximité.</li>
        <li><strong>Distribuez les accessoires :</strong> chaque joueur prend son paravent, ses 2 dés et ses 2 jetons Défenseur. Désignez un premier <strong>Coordonnateur</strong> (qui donne le tempo des étapes). Vous êtes prêts pour le Tour 1 !</li>
      </ol>

      <h3 class="text-base font-bold text-forest-900 mb-2">Tuiles de Synergie actives pour votre table (${2 * n} tuiles en lisière)</h3>
      <div class="overflow-x-auto border border-slate-200 rounded-xl">
        <table class="w-full text-xs text-left border-collapse">
          <thead class="bg-forest-900 text-white">
            <tr>
              <th class="p-2.5">Lisière</th>
              <th class="p-2.5">Tuile &amp; Famille</th>
              <th class="p-2.5">Peuple d’origine</th>
              <th class="p-2.5">Effet en jeu</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            ${lisieres.map(l => l.tuiles.map((tId, idx) => {
              const t = CATALOGUE_TUILES[tId];
              const pLetter = state.profileOverrides[tId] || 'A';
              const prof = t.profils[pLetter] || t.profils.A;
              const famLabel = t.famille === 'GARDIEN'
                ? '<span class="px-1.5 py-0.5 rounded bg-amber-100 text-amber-900 font-semibold">Gardien</span>'
                : t.famille === 'REVE'
                  ? '<span class="px-1.5 py-0.5 rounded bg-purple-100 text-purple-900 font-semibold">Rêve</span>'
                  : '<span class="px-1.5 py-0.5 rounded bg-lime-100 text-lime-900 font-semibold">Nid</span>';
              const origName = PEUPLES[t.origine] ? `${PEUPLES[t.origine].icon} ${PEUPLES[t.origine].nom}` : t.origine;
              return `
                <tr class="hover:bg-slate-50">
                  ${idx === 0 ? `<td rowspan="2" class="p-2.5 font-bold bg-slate-50 border-r border-slate-200 align-middle whitespace-nowrap">Lisière ${l.index}<br><span class="text-forest-700">${PEUPLES[l.p1].icon} ${PEUPLES[l.p1].nom} ↔ ${PEUPLES[l.p2].icon} ${PEUPLES[l.p2].nom}</span></td>` : ''}
                  <td class="p-2.5 align-top whitespace-nowrap">
                    <div class="font-bold text-slate-900">${prof.nom}</div>
                    <div class="mt-1">${famLabel}</div>
                  </td>
                  <td class="p-2.5 align-top whitespace-nowrap font-medium text-forest-800">${origName}</td>
                  <td class="p-2.5 align-top text-slate-700 leading-relaxed">${prof.texte}</td>
                </tr>
              `;
            }).join('')).join('')}
          </tbody>
        </table>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 3. VUE D'ENSEMBLE D'UN TOUR                                         -->
    <!-- =================================================================== -->
    <section id="sec-vue-tour" class="mb-10">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5 mb-4">
        3. Vue d’ensemble d’un tour
      </h2>
      <p class="text-sm text-slate-700 mb-4">
        Une partie se joue en <strong>8 tours maximum</strong>. Chaque tour suit toujours les <strong>6 étapes</strong> ci-dessous dans l’ordre :
      </p>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3 text-xs">
        <div class="border border-slate-200 rounded-xl p-3.5 bg-slate-50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">Étape 1 · Préparation</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Passage en Ratissage des machines au cœur, pioche secrète d’1 carte par joueur et lancer de 2 dés sous paravent.</p>
        </div>

        <div class="border border-slate-200 rounded-xl p-3.5 bg-slate-50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">Étape 2 · Défenseurs</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🤫 Silence</span>
          </div>
          <p class="text-slate-600">Pose locale irrévocable d’un premier jeton Défenseur, puis pose globale muette de votre autre Défenseur (<em>Réflexion → Définitif</em>).</p>
        </div>

        <div class="border border-emerald-200 rounded-xl p-3.5 bg-emerald-50/50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">Étape 3 · Révélation</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🗣️ Paravents ouverts</span>
          </div>
          <p class="text-slate-600">Construction obligatoire des tuiles complètes, puis ouverture simultanée des paravents : Sabotages, déviations Insectes et Rêves.</p>
        </div>

        <div class="border border-emerald-200 rounded-xl p-3.5 bg-emerald-50/50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">Étape 4 · Forêt vivante</span>
            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-semibold">🗣️ Libre</span>
          </div>
          <p class="text-slate-600">Résolution de la Furtivité (Pièges &amp; Sabotages), production des Nids actifs, puis Migration des Insectes.</p>
        </div>

        <div class="border border-rose-200 rounded-xl p-3.5 bg-rose-50/50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-rose-900 text-sm">Étape 5 · Attaques &amp; Bilan</span>
            <span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-semibold">⚔️ Résolution</span>
          </div>
          <p class="text-slate-600">Attaques des machines (Tactiques 1 à 6 puis Ratissages), retrait des Pièges utilisés, verdict des Gardiens et test de fin de partie.</p>
        </div>

        <div class="border border-slate-200 rounded-xl p-3.5 bg-slate-50">
          <div class="flex items-center justify-between mb-1">
            <span class="font-bold text-forest-900 text-sm">Étape 6 · Fin de tour</span>
            <span class="px-2 py-0.5 rounded bg-slate-200 text-slate-700 font-semibold">🔄 Remélange</span>
          </div>
          <p class="text-slate-600">Récupération de tous les Défenseurs, passage du Coordonnateur et remélange du paquet Machine avec les Sabotages.</p>
        </div>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 4. DÉROULÉ D'UN TOUR ÉTAPE PAR ÉTAPE                                -->
    <!-- =================================================================== -->
    <section id="sec-deroule" class="mb-10 space-y-6">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        4. Déroulé d’un tour étape par étape
      </h2>

      <!-- ÉTAPE 1 -->
      <div class="space-y-2.5">
        <h3 class="text-lg font-bold text-forest-900">Étape 1 — Préparation, Ratissage &amp; Dés secrets</h3>
        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>1.1 Passage en Ratissage :</strong> toute machine se trouvant sur la <strong>dernière parcelle non rasée</strong> de son rayon est retournée définitivement sur sa <strong>face Ratissage</strong> et sa carte est retirée du paquet Machine. Elle conserve tous ses jetons Puissance précédents, bénéficie d’un bonus imprimé de <strong>+1 puissance rouge</strong> et attaquera automatiquement chaque tour en fin d’Étape 5 avec la Tactique <code>T1</code> (Sur place).</li>
          <li><strong>1.2 Distribution secrète :</strong> chaque joueur pioche secrètement <strong>1 carte</strong> du paquet Machine (qui contient aussi toutes les cartes Sabotage intégrées au fil de la partie) et la place derrière son paravent. <em>En cas de pénurie</em> (moins de cartes que de joueurs), distribuez dans le sens horaire en commençant par le Peuple possédant le plus d’Arbres debout (en cas d’égalité, le plus proche du Coordonnateur dans le sens horaire).</li>
          <li><strong>1.3 Lancer de dés secret :</strong> si vous avez pioché une <strong>carte Machine</strong>, lancez vos 2 dés derrière votre paravent et retenez la <strong>plus petite valeur</strong> : ce chiffre (de 1 à 6) indique la case visée sur la <strong>Piste des Tactiques</strong>. Si vous avez pioché une <strong>carte Sabotage</strong> (ou aucune carte), vous ne lancez pas les dés : le Contremaître perd cette activation.</li>
        </ul>
      </div>

      <!-- ÉTAPE 2 -->
      <div class="space-y-2.5">
        <h3 class="text-lg font-bold text-forest-900">Étape 2 — Pose silencieuse des Défenseurs</h3>
        <p class="text-sm text-slate-700">
          Pendant toute cette étape, les paravents restent fermés et le silence tactique est total. Vous engagez vos <strong>2 jetons Défenseur</strong> en deux temps :
        </p>
        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>2.1 Pose locale (irrévocable) :</strong> simultanément, chaque joueur place l’un de ses deux Défenseurs (face <em>Définitif</em>) sur une parcelle non rasée de <strong>son propre rayon</strong>, sur une case libre de <strong>l’une de ses deux Pistes de Furtivité</strong>, ou sur l’une des <strong>Tuiles de Synergie non construites</strong> de ses deux lisières. Une fois posé, ce jeton ne bouge plus jusqu’à l’ouverture des paravents.</li>
          <li><strong>2.2 Pose globale (Réflexion puis Définitif) :</strong> chaque joueur place ensuite son <strong>autre Défenseur</strong> n’importe où sur le plateau, d’abord sur sa face <strong>Réflexion</strong> :
            <ul class="list-circle pl-5 mt-1 space-y-1 text-slate-600">
              <li>une parcelle non rasée de n’importe quel rayon de Forêt ;</li>
              <li>une case de Furtivité (maximum 2 Défenseurs par case) ;</li>
              <li>une Tuile de Synergie en lisière (maximum 2 Défenseurs par tuile) ;</li>
              <li>une tuile <strong>Rêve</strong> présente sur la Piste des Tactiques (pour activer son annulation) ;</li>
              <li>une tuile <strong>Gardien</strong> déjà construite sur la Piste des Gardiens (pour parier sur son déclenchement, dans la limite de <strong>2 Défenseurs par Gardien</strong>).</li>
            </ul>
            En observant silencieusement les placements de vos partenaires, vous pouvez déplacer librement votre jeton tant qu’il est face <em>Réflexion</em>. Dès que votre choix est arrêté, retournez-le <strong>sur place</strong> sur sa face <strong>Définitif</strong>. Lorsque tous les joueurs ont retourné leur jeton, passez à l’Étape 3.
          </li>
        </ul>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
          <div class="bg-emerald-50 border-l-4 border-emerald-600 rounded-r-xl p-3.5 text-xs text-emerald-950">
            <div class="font-bold uppercase tracking-wider text-emerald-800 mb-1">✨ Règle d’or — Communication muette</div>
            <p>Aucune parole, aucun signe de tête, aucun doigt pointé tant que les paravents sont fermés. Vos placements face <em>Réflexion</em> sont votre langage : poser un Défenseur sur le rayon d’un voisin lui signale un danger ; venir compléter une case de Furtivité lui confirme votre soutien.</p>
          </div>
          <div class="bg-amber-50 border-l-4 border-amber-500 rounded-r-xl p-3.5 text-xs text-amber-950">
            <div class="font-bold uppercase tracking-wider text-amber-800 mb-1">💡 Exemple concret — Furtivité à 4 emplacements</div>
            <p>Une case de Furtivité comporte 2 emplacements côté gauche et 2 côté droite. Les Mammifères y posent un Défenseur côté gauche. En 2.2, les Reptiles entrent sur la même case côté droit : le pion des Mammifères <strong>glisse aussitôt sur l’emplacement jumeau côté droit</strong>. Les deux pions font aussitôt face à la parcelle des Reptiles et agiront pour eux ! Retourner son jeton de <em>Réflexion</em> à <em>Définitif</em> se fait toujours sur place, sans jamais déplacer le partenaire.</p>
          </div>
        </div>
      </div>

      <!-- ÉTAPE 3 -->
      <div class="space-y-2.5">
        <h3 class="text-lg font-bold text-forest-900">Étape 3 — Construction obligatoire &amp; Ouverture des paravents</h3>
        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>3.1 Construction avant ouverture :</strong> toute Tuile de Synergie en lisière qui réunit <strong>2 Défenseurs</strong> est obligatoirement construite <em>avant</em> de lever les paravents (en cas de plusieurs constructions, le Coordonnateur choisit l’ordre) :
            <ul class="list-disc pl-5 mt-1 space-y-1 text-slate-600">
              <li><strong>Gardien :</strong> placez-le Face 1 sur une case libre (1 à 6) de la Piste des Gardiens choisie par son Peuple d’origine.</li>
              <li><strong>Rêve :</strong> posez-le par-dessus la <strong>case libre la plus à droite</strong> de la Piste des Tactiques (case 6, puis 5 si 6 porte déjà un Rêve, etc.). Il est immédiatement actif pour l’étape 3.2.</li>
              <li><strong>Nid :</strong> placez-le sur une parcelle non rasée de l’un de ses deux rayons adjacents ne contenant aucune machine ni aucun autre Nid ; ses Défenseurs bâtisseurs l’accompagnent sur cette parcelle.</li>
              <li><strong>Sort des bâtisseurs (Gardien / Rêve) :</strong> ${n === 3 ? '<span class="dyn-span">dans une partie à <strong>3 joueurs</strong>, le Peuple d’origine libère <strong>1 des 2 Défenseurs</strong> bâtisseurs sur la première parcelle non rasée de l’un des deux rayons de la lisière ; l’autre reste en bordure jusqu’à la fin du tour.</span>' : '<span class="dyn-span">dans une partie à <strong>' + n + ' joueurs</strong>, les 2 Défenseurs bâtisseurs restent en bordure de lisière jusqu’à la fin du tour.</span>'}</li>
            </ul>
          </li>
          <li><strong>3.2 Ouverture simultanée des paravents :</strong> tous les joueurs révèlent ensemble leurs cartes et leurs dés. <strong>La parole est libre !</strong> Résolvez dans cet ordre :
            <ol class="list-decimal pl-5 mt-1 space-y-1 text-slate-600">
              <li>Les <strong>cartes Sabotage</strong> révélées sont mises de côté (elles rejoindront le paquet à l’Étape 6) et allument le déclencheur <strong>3. Sabotage</strong>.</li>
              <li>Les éventuelles <strong>déviations d’Insectes</strong> sur la Piste des Tactiques décalent un dé de −1 ou +1 rang et allument le déclencheur <strong>6. Insecte</strong>.</li>
              <li>Chaque carte Machine dont le dé retenu pointe sur un <strong>Rêve</strong> (et qui n’a pas été déviée par un Insecte) allume le déclencheur <strong>5. Rêve</strong>. Les Défenseurs posés sur ce Rêve annulent alors les machines (1 Défenseur annule 1 machine ; voir section 5.2).</li>
              <li>Balayez ensuite la Piste des Gardiens de 1 à 6 pour résoudre les Gardiens déclenchés.</li>
            </ol>
          </li>
        </ul>
      </div>

      <!-- ÉTAPE 4 -->
      <div class="space-y-2.5">
        <h3 class="text-lg font-bold text-forest-900">Étape 4 — Furtivité, Production des Nids &amp; Migration</h3>
        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>4.1 Actions de Furtivité :</strong> chaque case de Furtivité réunissant un binôme complet sur la même rive (<strong>2 Défenseurs</strong>, ou <strong>1 Défenseur + 1 Insecte défaussé</strong>) accomplit <strong>une seule action</strong>, décidée par le joueur de cette rive, en observant la parcelle de Forêt juste en face :
            <ul class="list-disc pl-5 mt-1 space-y-1 text-slate-600">
              <li><strong>Aucune machine présente :</strong> posez <strong>1 Piège</strong> sur cette parcelle (s’il n’y en a pas déjà un).</li>
              <li><strong>Au moins 1 machine présente et aucune active ce tour</strong> (ni carte révélée active, ni en Ratissage — une machine annulée par un Rêve est inactive !) : prenez <strong>1 carte Sabotage</strong> de la réserve et mettez-la de côté pour l’intégrer définitivement au paquet Machine à l’Étape 6.</li>
            </ul>
          </li>
          <li><strong>4.2 Production des Nids :</strong> chaque Nid présent en Forêt et occupé par <strong>au moins 1 Défenseur</strong> produit des Insectes, dans l’ordre choisi par le joueur Insectes (voir section 5.3).</li>
          <li><strong>4.3 Migration des Insectes :</strong> chaque jeton Insecte présent sur la roue peut se déplacer de <strong>0 ou 1 cran</strong> (voir section 5.3).</li>
        </ul>
      </div>

      <!-- ÉTAPE 5 -->
      <div class="space-y-3">
        <h3 class="text-lg font-bold text-forest-900">Étape 5 — Attaques des Machines &amp; Bilan de fin de tour</h3>
        <p class="text-sm text-slate-700">
          Les machines actives attaquent dans l’ordre croissant de la <strong>Piste des Tactiques (de la case 1 à la case 6)</strong>, suivies en <strong>5.2</strong> par toutes les machines en <strong>Ratissage</strong> (qui appliquent <code>T1</code>). Si deux machines d’un même rayon agissent au même rang (ou en Ratissage), l’<strong>Abatteuse agit toujours avant le Bulldozer</strong>. Entre rayons différents au même rang, les joueurs choisissent librement l’ordre.
        </p>

        <p class="text-sm text-slate-700">
          Résolvez chaque machine <strong>entièrement</strong> avant de passer à la suivante : lisez ses cibles depuis sa position réelle à cet instant, résolvez ses frappes une par une, appliquez son éventuelle avancée (<code>T3</code>, <code>T6</code>) puis son gain de jeton Puissance rouge (<code>T4</code>, <code>T5</code>, <code>T6</code>), et terminez par un balayage 1 à 6 de la Piste des Gardiens.
        </p>

        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 text-sm space-y-2">
          <div class="font-bold text-forest-900">🛡️ Comment arrêter une frappe (ordre impératif)</div>
          <p class="text-xs text-slate-600">
            Le <strong>Seuil de Parade</strong> d’une frappe vaut : <span class="dyn-span">${seuilOffsetTxt}</span>. <span class="dyn-span">${synergieMachineTxt}</span>
          </p>
          <ol class="list-decimal pl-5 space-y-1.5 text-xs text-slate-700">
            <li><strong>Effet spécial de parade automatique</strong> (si un Gardien ou une loi active permet de parer automatiquement cette frappe) → allume <strong>1. Parade</strong>.</li>
            <li><strong>Piège armé (Embuscade) :</strong> s’il y a un Piège sur la parcelle et que la <strong>Défense totale</strong> sur place (Défenseurs + Insectes) vaut <strong>au moins 1</strong>, le Piège bloque automatiquement la frappe sans dépenser d’Insecte ! Marquez le Piège comme <em>déclenché</em> (il sera retiré en 5.3) → allume <strong>2. Piégeage</strong>.</li>
            <li><strong>Parade classique :</strong> si la Défense totale atteint le Seuil de Parade :
              <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600">
                <li>Si les <strong>Défenseurs seuls</strong> suffisent : la frappe est bloquée → allume <strong>1. Parade</strong>.</li>
                <li>Si des <strong>Insectes</strong> complètent le Seuil : défaussez immédiatement le nombre exact d’Insectes manquants → allume <strong>6. Insecte</strong>.</li>
              </ul>
            </li>
            <li><strong>Frappe non parée (Dégâts) :</strong>
              <ul class="list-disc pl-5 mt-1 space-y-0.5 text-slate-600">
                <li><strong>Abatteuse :</strong> <span class="dyn-span">${abatteuseTxt}</span>.</li>
                <li><strong>Bulldozer :</strong> coupe jusqu’à <strong>1 Arbre debout</strong> en Souche, puis retire <strong>toutes les Souches</strong> non protégées de la parcelle.</li>
              </ul>
            </li>
          </ol>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-amber-50 border-l-4 border-amber-500 rounded-r-xl p-3.5 text-xs text-amber-950">
            <div class="font-bold uppercase tracking-wider text-amber-800 mb-1">💡 Exemple concret — Chaîne Piège → Parade → Insectes</div>
            <p>Un Bulldozer avec 1 jeton rouge attaque une parcelle de Seuil imprimé 3 avec <code>T1</code> (Seuil total = <strong>4</strong>). Sur place se trouvent <strong>1 Défenseur, 2 Insectes et 1 Piège</strong>. Bien que la Défense totale (3) soit inférieure à 4, le Piège est armé (Défense totale ≥ 1) : il bloque la frappe tout seul, les 2 Insectes restent intacts et seul <strong>2. Piégeage</strong> s’allume. Sans Piège, si le Seuil était de 3, le Défenseur (1) et les 2 Insectes défaussés sur-le-champ pareraient la frappe et allumeraient <strong>6. Insecte</strong>.</p>
          </div>
          <div class="bg-amber-50 border-l-4 border-amber-500 rounded-r-xl p-3.5 text-xs text-amber-950">
            <div class="font-bold uppercase tracking-wider text-amber-800 mb-1">💡 Exemple concret — Pont routier &amp; Repli</div>
            <p>Lorsqu’une parcelle tombe à <strong>0 Arbre et 0 Souche</strong>, elle devient une <strong>Route Forestière</strong> définitivement rasée (défaussez tout pion dessus). Les machines qui s’y trouvaient effectuent aussitôt un <strong>Repli</strong> vers la première parcelle non rasée côté bordure (ou côté cœur si toute la bordure est rasée ; si tout le rayon est rasé, elles quittent la partie). Ensuite, le long du rayon, les Routes sont toujours <strong>sautées comme un pont</strong> (avancer, reculer ou viser devant passe directement à la parcelle non rasée suivante), mais restent infranchissables depuis les lisières.</p>
          </div>
        </div>

        <p class="text-sm text-slate-700">
          <strong>5.3 Bilan de fin d’attaques :</strong> retirez du plateau tous les Pièges déclenchés ce tour-ci, résolvez le <strong>verdict des paris Gardiens</strong> (voir section 5.1), puis vérifiez si l’une des <strong>3 conditions de fin de partie</strong> est atteinte (voir section 6). Si la partie continue, passez à l’Étape 6.
        </p>
      </div>

      <!-- ÉTAPE 6 -->
      <div class="space-y-2">
        <h3 class="text-lg font-bold text-forest-900">Étape 6 — Fin de tour &amp; Remélange</h3>
        <ul class="space-y-1.5 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Récupération :</strong> chaque joueur reprend en main ses <strong>2 jetons Défenseur</strong> (y compris ceux glissés sous les Gardiens ou engagés sur les Rêves). Les effets temporaires du tour prennent fin.</li>
          <li><strong>Remélange &amp; Coordonnateur :</strong> rassemblez toutes les cartes Machine actives (hors machines en Ratissage) et <strong>toutes les cartes Sabotage</strong> (celles déjà présentes, celles révélées ce tour et celles nouvellement acquises), puis mélangez-les pour reformer le paquet Machine. Passez le jeton <strong>Coordonnateur</strong> au joueur suivant dans le sens horaire et entamez le tour suivant !</li>
        </ul>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 5. LES PEUPLES ET LEURS MÉCANIQUES PROPRES                          -->
    <!-- =================================================================== -->
    <section id="sec-peuples" class="mb-10 space-y-6">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        5. Les Peuples et leurs mécaniques propres
      </h2>

      <!-- 5.1 ANIMAUX SAUVAGES -->
      <div class="bg-amber-50/40 border border-amber-200 rounded-2xl p-5 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <h3 class="text-lg font-bold text-amber-950">5.1 Animaux Sauvages (🐆 Mammifères, 🐍 Reptiles, 🦜 Oiseaux) &amp; Piste des Gardiens</h3>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${reveilActif ? 'bg-amber-200 text-amber-950' : 'bg-slate-200 text-slate-600'}">
            ${reveilActif ? `Actif sur votre table (${nbAnimauxSauvages} Peuple${nbAnimauxSauvages > 1 ? 's' : ''})` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${reveilActif
            ? '<span class="dyn-span">Au moins un Peuple Animal Sauvage siège autour de votre table : la <strong>Piste des Gardiens</strong> et le <strong>Réveil de la Forêt</strong> sont pleinement actifs.</span>'
            : '<span class="dyn-span">Aucun Peuple Animal Sauvage ne siège autour de votre table : la Piste des Gardiens et le Réveil de la Forêt restent inactifs durant cette partie.</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Le pari d’activation (Étape 2.2) :</strong> un Gardien construit sur la Piste des Gardiens (cases 1 à 6) ne s’active durant le tour que si des joueurs posent <strong>1 ou 2 Défenseurs</strong> dessus lors de la pose globale (<strong>maximum 2 Défenseurs par Gardien</strong> ; un Gardien sans Défenseur reste paisiblement inactif et demeure en piste sans risque).</li>
          <li><strong>Déclenchement &amp; balayage à plat (1 → 6) :</strong> chaque fois que l’événement associé à sa case se produit, terminez l’action en cours puis parcourez la Piste des Gardiens de la case 1 à la case 6. Pour chaque case allumée portant un Gardien muni d’au moins un Défenseur dessus : <strong>glissez 1 Défenseur sous la tuile</strong> et appliquez immédiatement le pouvoir du Gardien. S’il possède 2 Défenseurs dessus et que son déclencheur se produit deux fois dans le tour, il s’active deux fois !</li>
          <li><strong>Verdict des paris en 5.3 :</strong>
            <ul class="list-disc pl-5 mt-1 space-y-1 text-slate-600">
              <li><strong>Pari gagné</strong> (tous les Défenseurs posés sur le Gardien ont été glissés sous la tuile) : le Gardien reste fièrement sur sa case ; s’il s’agit d’un Gardien évolutif double-face encore en Face 1, <strong>retournez-le sur sa Face 2</strong> pour les tours suivants !</li>
              <li><strong>Pari perdu</strong> (il reste encore 1 ou 2 Défenseurs non glissés sur la tuile) : le Gardien retourne immédiatement en lisière sur sa Face 1 (reconstructible plus tard), sauf si un Insecte présent sur sa case active le <em>Bouclier de lisière</em> (voir section 5.3).</li>
            </ul>
          </li>
        </ul>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-amber-50 border-l-4 border-amber-500 rounded-r-xl p-3 text-xs text-amber-950">
            <div class="font-bold uppercase tracking-wider text-amber-800 mb-1">💡 Exemple concret — Pari à 2 Défenseurs</div>
            <p>Le <em>Bond du Jaguar</em> (Face 1) est posé sur la case <strong>1. Parade</strong>. En 2.2, deux joueurs misent chacun un Défenseur dessus (2 Défenseurs au total). Pendant l’Étape 5, une première attaque est parée par Défenseurs seuls : un Défenseur est glissé sous le Jaguar et son effet Face 1 s’applique. Plus tard dans le tour, une nouvelle attaque est parée par Défenseurs seuls : l’autre Défenseur est glissé et le Jaguar agit une deuxième fois ! En 5.3, aucun Défenseur ne reste sur la tuile : <strong>le pari est gagné</strong> et le Jaguar passe sur sa <strong>Face 2</strong> pour le prochain tour.</p>
          </div>
          <div class="bg-emerald-50 border-l-4 border-emerald-600 rounded-r-xl p-3 text-xs text-emerald-950">
            <div class="font-bold uppercase tracking-wider text-emerald-800 mb-1">✨ Règle d’or — 1 événement = au plus 1 déclencheur</div>
            <p>Chaque carte révélée en 3.2 et chaque frappe bloquée en 5.1/5.2 n’allume <strong>au maximum qu’une seule case</strong> de la Piste des Gardiens selon une hiérarchie claire, sans cumul ambigu. Les actions de Furtivité (4.1) et la production des Nids (4.2) n’allument jamais la Piste des Gardiens.</p>
          </div>
        </div>

        <h4 class="text-sm font-bold text-amber-950 pt-1">Les 6 déclencheurs de la Piste des Gardiens</h4>
        <div class="overflow-x-auto border border-amber-200 rounded-xl bg-white">
          <table class="w-full text-xs text-left border-collapse">
            <thead class="bg-amber-900 text-white">
              <tr>
                <th class="p-2 w-28">Case</th>
                <th class="p-2 w-36">Moment</th>
                <th class="p-2">Condition exacte d’allumage (partition stricte)</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-amber-100 text-slate-700">
              <tr>
                <td class="p-2 font-bold text-amber-950">1. Parade</td>
                <td class="p-2">Étape 5 (Attaques)</td>
                <td class="p-2">Une frappe est bloquée par <strong>Défenseurs seuls</strong> (sans Piège ni dépense d’Insecte) ou par un effet automatique de parade.</td>
              </tr>
              <tr>
                <td class="p-2 font-bold text-amber-950">2. Piégeage</td>
                <td class="p-2">Étape 5 (Attaques)</td>
                <td class="p-2">Un <strong>Piège armé</strong> arrête une frappe de machine (prioritaire sur la Parade et les Insectes).</td>
              </tr>
              <tr>
                <td class="p-2 font-bold text-amber-950">3. Sabotage</td>
                <td class="p-2">Étape 3.2 (Révélation)</td>
                <td class="p-2">Une <strong>carte Sabotage</strong> est révélée à l’ouverture des paravents.</td>
              </tr>
              <tr>
                <td class="p-2 font-bold text-amber-950">4. Gardien</td>
                <td class="p-2">Tout le tour</td>
                <td class="p-2">Lors de la <strong>première ouverture du tour de chaque autre Gardien distinct</strong> (cases 1, 2, 3, 5 ou 6 ; un Gardien qui s’ouvre deux fois ne l’allume qu’une fois, et la case 4 ne s’auto-alimente jamais).</td>
              </tr>
              <tr>
                <td class="p-2 font-bold text-amber-950">5. Rêve</td>
                <td class="p-2">Étape 3.2 (Révélation)</td>
                <td class="p-2">Une carte Machine (non déviée par un Insecte) pointe avec son dé retenu sur une case occupée par un <strong>Rêve</strong> (qu’elle soit annulée ou qu’elle joue la Tactique imprimée dessous).</td>
              </tr>
              <tr>
                <td class="p-2 font-bold text-amber-950">6. Insecte</td>
                <td class="p-2">Étape 3.2 ou Étape 5</td>
                <td class="p-2">Un Insecte de la Piste des Tactiques <strong>dévie un dé</strong> en 3.2 (prioritaire sur 5. Rêve) <strong>OU</strong> une Parade classique en Étape 5 défausse <strong>au moins 1 Insecte</strong> (prioritaire sur 1. Parade).</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 5.2 PEUPLES ONIRIQUES -->
      <div class="bg-purple-50/40 border border-purple-200 rounded-2xl p-5 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <h3 class="text-lg font-bold text-purple-950">5.2 Peuples Oniriques (🏹 Humains, ✨ Entités Magiques) &amp; Rêves</h3>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${nbRevesEnJeu > 0 ? 'bg-purple-200 text-purple-950' : 'bg-slate-200 text-slate-600'}">
            ${nbRevesEnJeu > 0 ? `${nbRevesEnJeu} tuiles Rêve sur votre table` : 'Inactif sur votre table'}
          </span>
        </div>

        <p class="text-sm text-slate-700">
          ${nbRevesEnJeu > 0
            ? `<span class="dyn-span">Votre table compte <strong>${nbRevesEnJeu} tuiles Rêve</strong> en jeu. Pour remporter le <strong>Sommeil du Contremaître</strong> avant le 8<sup>e</sup> tour, rassemblez toutes ces ${nbRevesEnJeu} tuiles en un bloc continu sur les <strong>cases 1 à ${nbRevesEnJeu}</strong> de la Piste des Tactiques.</span>`
            : '<span class="dyn-span">Aucun Peuple Onirique ne siège autour de votre table : aucune tuile Rêve n’est présente et le Sommeil du Contremaître est inactif durant cette partie.</span>'}
        </p>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Pose sur la Piste des Tactiques fixe :</strong> lorsqu’un Rêve est construit en 3.1, posez-le par-dessus la <strong>case libre la plus à droite</strong> (case 6, puis case 5 si la 6 porte déjà un Rêve, etc.). Les Tactiques <code>T1</code> à <code>T6</code> restent imprimées en permanence sur la piste.</li>
          <li><strong>Activer un Rêve (coût en Défenseur) :</strong> en 2.2, un ou plusieurs joueurs peuvent poser leur Défenseur sur un Rêve présent sur la piste. À l’ouverture des paravents (3.2), <strong>chaque Défenseur posé sur ce Rêve annule 1 carte Machine</strong> dont le dé pointe sur ce rang (en neutralisant d’abord la machine la plus menaçante si plusieurs pointent sur la même case). Toute machine non annulée exécute normalement la Tactique imprimée sous le Rêve.</li>
          <li><strong>Effet &amp; Avancée vers la gauche :</strong> dès qu’un Rêve annule au moins 1 machine, son pouvoir se résout (<span class="dyn-span">${reveMultiTxt}</span>). De plus, <strong>si toutes les machines pointant sur ce rang ont été annulées ce tour-ci</strong>, le Rêve avance d’1 case vers la gauche (s’il rencontre d’autres Rêves collés à sa gauche, il pousse l’ensemble du bloc d’un cran vers la première case libre à gauche).</li>
        </ul>
      </div>

      <!-- 5.3 PEUPLE INSECTES -->
      <div class="bg-lime-50/40 border border-lime-200 rounded-2xl p-5 space-y-3">
        <div class="flex flex-wrap items-center justify-between gap-2">
          <h3 class="text-lg font-bold text-lime-950">5.3 Peuple Insectes (🐜) : Nids, Migration, Déviation &amp; Bouclier de lisière</h3>
          <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${hasInsectes ? 'bg-lime-200 text-lime-950' : 'bg-slate-200 text-slate-600'}">
            ${hasInsectes ? 'Actif sur votre table' : 'Absent de votre table'}
          </span>
        </div>

        <ul class="space-y-2 text-sm text-slate-700 list-disc pl-5">
          <li><strong>Production des Nids (Étape 4.2) :</strong> chaque Nid portant au moins 1 Défenseur se résout comme un <strong>bloc indivisible</strong> :
            <ol class="list-decimal pl-5 mt-1 space-y-0.5 text-slate-600">
              <li>Posez <strong>+1 Insecte</strong> sur sa parcelle s’il y a 0 ou 1 Insecte à cet instant précis, ou <strong>+2 Insectes</strong> s’il y en a déjà 2 ou plus.</li>
              <li>Appliquez aussitôt le pouvoir propre de ce Nid.</li>
            </ol>
          </li>
          <li><strong>Fragilité des Nids (Contact Machine-Nid) :</strong> dès qu’une machine entre (par avancée, recul ou repli) sur la parcelle d’un Nid, le Nid est immédiatement renvoyé en lisière (reconstructible plus tard) et tous les Insectes de cette parcelle sont défaussés. Les Défenseurs et un éventuel Piège restent en place.</li>
          <li><strong>Migration (Étape 4.3) :</strong> chaque Insecte présent sur la roue peut se déplacer de <strong>0 ou 1 cran</strong> : vers une parcelle non rasée voisine sur le même rayon (en sautant les Routes), ou latéralement entre une parcelle et l’une de ses deux cases de Furtivité adjacentes (sauf à travers une Route). Retournez chaque Insecte déplacé pour le repérer, puis remettez-les tous à l’endroit en fin de Migration.</li>
          <li><strong>Aller simple vers les pistes centrales :</strong> depuis la <strong>dernière parcelle non rasée</strong> d’un rayon, 1 cran de Migration permet d’envoyer définitivement un Insecte sur n’importe quelle case (1 à 6) de l’une des deux pistes centrales (sans limite par case) :
            <ul class="list-disc pl-5 mt-1 space-y-1 text-slate-600">
              <li><strong>Sur la Piste des Tactiques — ${bugProf.nom} :</strong> <span class="dyn-span">${bugProf.texte}</span></li>
              <li><strong>Sur la Piste des Gardiens — ${colonieProf.nom} :</strong> <span class="dyn-span">${colonieProf.texte}</span></li>
            </ul>
          </li>
        </ul>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 6. FIN DE PARTIE & REPOUSSE FINALE                                  -->
    <!-- =================================================================== -->
    <section id="sec-fin" class="mb-10 space-y-4">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        6. Fin de partie &amp; Repousse Finale
      </h2>

      <p class="text-sm text-slate-700">
        La fin de partie est vérifiée à un unique moment : à l’<strong>Étape 5.3</strong>, juste après le retrait des Pièges déclenchés et le verdict des paris Gardiens. Dès qu’une condition de fin est remplie, l’Étape 6 est ignorée et vous passez directement à la <strong>Repousse Finale</strong>.
      </p>

      <div class="space-y-2.5 text-sm text-slate-700">
        <div class="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
          <div class="font-bold text-slate-900">1. Fin du 8<sup>e</sup> tour (priorité absolue)</div>
          <p class="text-xs text-slate-600 mt-0.5">Au terme de l’Étape 5.3 du <strong>Tour 8</strong>, la partie s’achève toujours sur cette fin temporelle, quelle que soit la disposition des Rêves ou des Gardiens.</p>
        </div>

        <div class="p-3.5 rounded-xl bg-purple-50/70 border border-purple-200">
          <div class="font-bold text-purple-950">2. Sommeil du Contremaître (Tours 1 à 7)</div>
          <p class="text-xs text-slate-700 mt-0.5">
            ${nbRevesEnJeu > 0
              ? `<span class="dyn-span">Les <strong>${nbRevesEnJeu} tuiles Rêve</strong> de la partie sont toutes construites et regroupées côte à côte sur les <strong>cases 1 à ${nbRevesEnJeu}</strong> de la Piste des Tactiques.</span>`
              : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Onirique autour de la table).</span>'}
          </p>
        </div>

        <div class="p-3.5 rounded-xl bg-amber-50/70 border border-amber-200">
          <div class="font-bold text-amber-950">3. Réveil de la Forêt (Tours 1 à 7)</div>
          <p class="text-xs text-slate-700 mt-0.5">
            ${reveilActif
              ? `<span class="dyn-span">Les <strong>${n} joueurs</strong> de la table ont tous engagé un Défenseur sur la Piste des Gardiens en 2.2 et <strong>tous les paris du tour sont gagnés</strong> en 5.3 (aucun Défenseur restant sur une tuile Gardien ; un Gardien sauvé par un Bouclier de lisière reste un pari perdu).</span>`
              : '<span class="dyn-span">Condition inactive dans cette partie (aucun Peuple Animal Sauvage autour de la table).</span>'}
          </p>
        </div>
      </div>

      <div class="bg-emerald-50 border-2 border-emerald-300 rounded-2xl p-4 text-sm text-emerald-950">
        <h3 class="font-bold text-base text-emerald-900 mb-1.5">🌱 Repousse Finale &amp; Score coopératif</h3>
        <p class="text-xs sm:text-sm leading-relaxed">
          Sur <strong>chaque parcelle non rasée</strong> contenant encore <strong>au moins 1 Souche</strong>, la nature reprend ses droits : <strong>retournez 1 Souche en Arbre debout</strong> (sans dépasser la dotation initiale imprimée sur la parcelle). Additionnez ensuite tous les Arbres debout sur l’ensemble des ${n} rayons : c’est votre <strong>score final sur ${totalArbres} Arbres possibles</strong> !
        </p>
      </div>
    </section>

    <!-- =================================================================== -->
    <!-- 7. MÉMENTO DE TABLE (AIDE DE JEU)                                   -->
    <!-- =================================================================== -->
    <section id="sec-memento" class="mb-4 space-y-5">
      <h2 class="text-2xl font-bold text-forest-900 border-b-2 border-forest-200 pb-1.5">
        7. Mémento de table (Aide de jeu)
      </h2>

      <!-- 7.1 TABLEAU DES 6 TACTIQUES -->
      <div>
        <h3 class="text-sm font-bold uppercase tracking-wider text-forest-800 mb-2">Les 6 Tactiques fixes de la Piste des Tactiques</h3>
        <div class="overflow-x-auto border border-slate-200 rounded-xl">
          <table class="w-full text-xs text-left border-collapse">
            <thead class="bg-forest-900 text-white">
              <tr>
                <th class="p-2">Case</th>
                <th class="p-2">Tactique</th>
                <th class="p-2">Parcelles ciblées</th>
                <th class="p-2">Modif. Seuil</th>
                <th class="p-2">Avancée</th>
                <th class="p-2">Gain Puissance</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-200 text-slate-700">
              <tr>
                <td class="p-2 font-bold">1</td>
                <td class="p-2 font-semibold"><code>T1</code> · Sur place <em>(aussi en Ratissage)</em></td>
                <td class="p-2">Sur place</td>
                <td class="p-2">0</td>
                <td class="p-2">—</td>
                <td class="p-2">—</td>
              </tr>
              <tr>
                <td class="p-2 font-bold">2</td>
                <td class="p-2 font-semibold"><code>T2</code> · Devant</td>
                <td class="p-2">Prochaine parcelle non rasée vers le cœur</td>
                <td class="p-2">0</td>
                <td class="p-2">—</td>
                <td class="p-2">—</td>
              </tr>
              <tr>
                <td class="p-2 font-bold">3</td>
                <td class="p-2 font-semibold"><code>T3</code> · Progression</td>
                <td class="p-2">Sur place, puis Devant</td>
                <td class="p-2">−1</td>
                <td class="p-2">+1 parcelle vers le cœur</td>
                <td class="p-2">—</td>
              </tr>
              <tr>
                <td class="p-2 font-bold">4</td>
                <td class="p-2 font-semibold"><code>T4</code> · Pression sur place</td>
                <td class="p-2">Sur place</td>
                <td class="p-2">−1</td>
                <td class="p-2">—</td>
                <td class="p-2">+1 jeton rouge</td>
              </tr>
              <tr>
                <td class="p-2 font-bold">5</td>
                <td class="p-2 font-semibold"><code>T5</code> · Pression devant</td>
                <td class="p-2">Prochaine parcelle non rasée vers le cœur</td>
                <td class="p-2">−1</td>
                <td class="p-2">—</td>
                <td class="p-2">+1 jeton rouge</td>
              </tr>
              <tr>
                <td class="p-2 font-bold">6</td>
                <td class="p-2 font-semibold"><code>T6</code> · Assaut total</td>
                <td class="p-2">Sur place, puis Devant</td>
                <td class="p-2">−2</td>
                <td class="p-2">+1 parcelle vers le cœur</td>
                <td class="p-2">+1 jeton rouge</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 7.2 ORDRE DE RÉSOLUTION & PARTITION COMPACTE -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-1.5">
          <h3 class="font-bold uppercase tracking-wider text-forest-800">⚔️ Résolution d’une frappe (dans l’ordre)</h3>
          <ol class="list-decimal pl-4 space-y-1 text-slate-700">
            <li><strong>Parade automatique</strong> par effet de tuile → <em>1. Parade</em>.</li>
            <li><strong>Piège armé</strong> (Défense totale ≥ 1) → bloque sans dépense → <em>2. Piégeage</em>.</li>
            <li><strong>Parade classique</strong> (Défense totale ≥ Seuil) : Défenseurs seuls → <em>1. Parade</em> ; sinon défausse immédiate des Insectes manquants → <em>6. Insecte</em>.</li>
            <li><strong>Dégâts :</strong> Abatteuse = 2 Arbres → Souches ; Bulldozer = 1 Arbre → Souche + retrait des Souches (0/0 = Route + Repli).</li>
          </ol>
        </div>

        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-1.5">
          <h3 class="font-bold uppercase tracking-wider text-forest-800">⚡ Partition des 6 déclencheurs (1 événement = 1 case)</h3>
          <ul class="list-disc pl-4 space-y-1 text-slate-700">
            <li><strong>À l’ouverture des paravents (3.2) :</strong> <em>3. Sabotage</em> &gt; <em>6. Insecte</em> (déviation) &gt; <em>5. Rêve</em>.</li>
            <li><strong>Pendant les attaques (5.1 / 5.2) :</strong> <em>2. Piégeage</em> &gt; <em>6. Insecte</em> (Parade avec Insecte) &gt; <em>1. Parade</em> (Défenseurs seuls).</li>
            <li><strong>4. Gardien :</strong> 1<sup>re</sup> ouverture du tour de chaque autre Gardien distinct (sans boucle).</li>
            <li><strong>Jamais déclenché</strong> par la Furtivité (4.1) ni par la production des Nids (4.2).</li>
          </ul>
        </div>
      </div>
    </section>
  `;
}
